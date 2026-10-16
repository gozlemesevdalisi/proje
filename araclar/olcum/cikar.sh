#!/usr/bin/env bash
# Esin kaynağının çizimlerini ölçüm için çıkarır (yalnızca bu bilgisayarda kalır).
#
# Kullanım (depo kökünden):  araclar/olcum/cikar.sh [swf-oyunlar klasörü]
#
# Çıktılar `referans/` klasörüne yazılır ve git'e GİRMEZ (.gitignore). Esinin çizimleri oyunda
# kullanılmaz, kopyalanmaz, izlenmez; yalnızca ölçülür. Depoya yalnızca ölçüm sonuçları (olcum/,
# docs/KARAKTER_OLCULERI.md) girer.
#
# Adımlar:
#   1. FFDec ile bütün şekiller SVG ve PNG (4×) olarak: referans/<oyun>/svg, referans/<oyun>/png
#   2. Savaş kuklasının sprite'ları (kukla ve parçaları) SVG olarak: referans/<oyun>/sprite
#   3. Oyunun kodu (kukla kare formülleri için): referans/<oyun>/kod
#   4. Birlikler oyunun formülleriyle birleştirilir: referans/<oyun>/birlikler
#   5. Kukla yapısı ve bütün karelerin eklemleri: olcum/kukla-<oyun>.json, referans/<oyun>/pozlar.json
#   6. Parça ölçüleri: docs/KARAKTER_OLCULERI.md
#   7. Görsellerin oyuna aktarımı: content/feudalism/<oyun> (bkz. araclar/aktar/aktar.py)
# Gerekenler: Java 17+, Python 3 + Pillow, curl, unzip, sha256sum, cargo.
set -euo pipefail

KOK="$(cd "$(dirname "$0")/../.." && pwd)"
SWF_KOK="${1:-$KOK/../swf-oyunlar}"
REF="$KOK/referans"
FFDEC_SURUM="24.1.1"
# İndirilen dosyanın değiştirilmediğini doğrulamak için SHA-256 özeti (swf-oyunlar/araclar/derle.sh ile aynı)
FFDEC_SHA256="dfa3a36575fd62bccc19750707a2f9d3a01bfc183763a061f07cb4f8cf1e38ed"
FFDEC="$REF/.araclar/ffdec"

if [ ! -f "$FFDEC/ffdec-cli.jar" ]; then
  echo "FFDec $FFDEC_SURUM indiriliyor..."
  mkdir -p "$FFDEC"
  curl -fsSL -o "$FFDEC/ffdec.zip" \
    "https://github.com/jindrapetrik/jpexs-decompiler/releases/download/version$FFDEC_SURUM/ffdec_$FFDEC_SURUM.zip"
  echo "$FFDEC_SHA256  $FFDEC/ffdec.zip" | sha256sum -c --quiet -
  unzip -q -o "$FFDEC/ffdec.zip" -d "$FFDEC"
  rm "$FFDEC/ffdec.zip"
fi

FF="java -Djava.awt.headless=true -jar $FFDEC/ffdec-cli.jar"
sessiz() { grep -v -e "JAVA_TOOL_OPTIONS" -e "^Exported" || true; }

cd "$KOK"
cargo build -q --release -p engine --example svg-png
for oyun in f1 f2; do
  if [ "$oyun" = f1 ]; then
    swf="$SWF_KOK/oyunlar/feudalism/feudalism-orijinal.swf"
    kukla="547,205,529,486,495,279,309,478"
  else
    swf="$SWF_KOK/oyunlar/feudalism-2/feudalism-2-orijinal.swf"
    kukla="1038,432,989,914,927,562,903,849"
  fi
  echo "$oyun: şekiller (SVG, PNG), kukla sprite'ları ve kod çıkarılıyor..."
  rm -rf "$REF/$oyun/svg" "$REF/$oyun/png" "$REF/$oyun/sprite"
  $FF -format shape:svg -export shape "$REF/$oyun/svg" "$swf" 2>&1 | sessiz | tail -1
  $FF -format shape:png -zoom 4 -export shape "$REF/$oyun/png" "$swf" 2>&1 | sessiz | tail -1
  $FF -format sprite:svg -selectid "$kukla" -export sprite "$REF/$oyun/sprite" "$swf" 2>&1 | sessiz | tail -1
  $FF -export script "$REF/$oyun/kod" "$swf" 2>&1 | sessiz | tail -1
  echo "$oyun: birlikler birleştiriliyor..."
  python3 araclar/olcum/birlikler.py "$oyun" "$swf" "$REF/$oyun/svg" "$REF/$oyun/birlikler"
  mkdir -p "$REF/$oyun/birlikler-png"
  for f in "$REF/$oyun/birlikler"/*.svg; do
    ./target/release/examples/svg-png "$f" "$REF/$oyun/birlikler-png/$(basename "$f" .svg).png" 3 >/dev/null
  done
  SWF_KOK="$SWF_KOK" python3 araclar/olcum/kukla_yapisi.py "$oyun"
done
SWF_KOK="$SWF_KOK" python3 araclar/olcum/olc.py "$REF" docs/KARAKTER_OLCULERI.md
echo "Görseller oyunun içerik klasörüne aktarılıyor (content/feudalism)..."
python3 araclar/aktar/aktar.py "$SWF_KOK"
