#!/usr/bin/env bash
# Esin kaynağının karakter kuklalarını ölçüm için çıkarır ve ölçüm sayfasını yeniden üretir.
#
# Kullanım (depo kökünden):  tools/referans/cikar.sh [swf-oyunlar klasörü]
#
# Çıktılar `referans/` klasörüne yazılır ve git'e GİRMEZ (.gitignore). Esinin çizimleri oyunda
# kullanılmaz; yalnızca ölçülür. Ölçüm sonucu: docs/KARAKTER_OLCULERI.md (yalnızca sayılar).
# Gerekenler: Java 17+, Python 3 + Pillow, curl, unzip, sha256sum, cargo.
set -euo pipefail

KOK="$(cd "$(dirname "$0")/../.." && pwd)"
SWF_KOK="${1:-$KOK/../swf-oyunlar}"
REF="$KOK/referans"
FFDEC_SURUM="24.1.1"
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
  if [ "$oyun" = f1 ]; then swf="$SWF_KOK/oyunlar/feudalism/feudalism-orijinal.swf"
  else swf="$SWF_KOK/oyunlar/feudalism-2/feudalism-2-orijinal.swf"; fi
  echo "$oyun: şekiller ve kod çıkarılıyor..."
  $FF -format shape:svg -export shape "$REF/$oyun/sekiller" "$swf" 2>&1 | sessiz | tail -1
  $FF -export script "$REF/$oyun/kod" "$swf" 2>&1 | sessiz | tail -1
  echo "$oyun: birlikler birleştiriliyor..."
  python3 tools/referans/birlikler.py "$oyun" "$swf" "$REF/$oyun/sekiller" "$REF/$oyun/birlikler"
  mkdir -p "$REF/$oyun/png"
  for f in "$REF/$oyun/birlikler"/*.svg; do
    ./target/release/examples/svg-png "$f" "$REF/$oyun/png/$(basename "$f" .svg).png" 3 "#4C8F40" >/dev/null
  done
done
SWF_KOK="$SWF_KOK" python3 tools/referans/olc.py "$REF" docs/KARAKTER_OLCULERI.md
