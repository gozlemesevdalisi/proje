# Dışarıdan alınan varlıklar ve lisansları

Oyuna eklenen her yazı tipi, ses, müzik ya da başka dış varlık burada kaynağı ve lisansıyla listelenir.
Kod kütüphanelerinin lisansları `cargo deny` ile denetlenir.

| Varlık | Kaynak | Lisans | Nerede |
| ------ | ------ | ------ | ------ |
| Feudalism ve Feudalism 2 görselleri: şekiller, animasyonlar, düğmeler, ekranlar | Orijinal oyunların SWF dosyaları (`feudalism-orijinal.swf`, `feudalism-2-orijinal.swf`); SHA-256 özetleri `content/feudalism/<oyun>/library.json` içinde | Hak sahibinin izniyle (oyunun sahibinin 16 Ekim 2026'da bildirdiği). Oyunlarda yazan hak sahibi: Vitaly Zaborov ("Copyright Vitaly Zaborov 2008"). İznin tarihi ve kapsamı: **eklenecek** | `content/feudalism/` |
| Feudalism ve Feudalism 2'nin Türkçe çevirisi: sabit yazılar, ekran kutuları, koddaki metinler, silah/zırh/birlik adları, "Öldün..." çizimi | Oyunların sahibinin `swf-oyunlar` deposu (`oyunlar/<oyun>/ceviri/`, sürüm `a679d21`, 14 Ekim 2026) | Oyunların sahibinin kendi çevirisi | `content/feudalism/<oyun>/ceviri/` (tablolar değiştirilmeden), çevrilmiş kod `kaynak/feudalism/<oyun>/kod-tr/` |
| Liberation Sans ve Liberation Serif 2.1.5 (normal, kalın, kalın italik) | [liberationfonts](https://github.com/liberationfonts/liberation-fonts), yapımcı: Red Hat; dosyalar `swf-oyunlar/yazitipleri/` içinden | SIL Open Font License 1.1 | `content/fonts/Liberation*.ttf`, lisans: `content/fonts/OFL-Liberation.txt` |
| TeX Gyre Pagella (kalın, kalın italik), Bonum (kalın, italik), Chorus, Adventor (kalın) | [GUST](https://www.gust.org.pl/projects/e-foundry/tex-gyre); dosyalar `swf-oyunlar/araclar/yazitipleri/` içinden | GUST Font License (LaTeX Project Public License 1.3c) | `content/fonts/texgyre*.otf`, lisans: `content/fonts/GUST-Font-License.txt` |
| Alegreya (değişken kalınlık) | [google/fonts](https://github.com/google/fonts/tree/main/ofl/alegreya), yapımcı: Huerta Tipográfica | SIL Open Font License 1.1 | `content/fonts/Alegreya-Variable.ttf`, lisans: `content/fonts/OFL-Alegreya.txt` |
| Alegreya SC (normal, kalın) | [google/fonts](https://github.com/google/fonts/tree/main/ofl/alegreyasc), yapımcı: Huerta Tipográfica | SIL Open Font License 1.1 | `content/fonts/AlegreyaSC-*.ttf`, lisans: `content/fonts/OFL-AlegreyaSC.txt` |
| Alegreya Sans (normal, kalın) | [google/fonts](https://github.com/google/fonts/tree/main/ofl/alegreyasans), yapımcı: Huerta Tipográfica | SIL Open Font License 1.1 | `content/fonts/AlegreyaSans-*.ttf`, lisans: `content/fonts/OFL-AlegreyaSans.txt` |

Notlar:

- Feudalism görsellerinden aktarılmayanlar (izin oyunun yazarının kendi eserini kapsar; bunlar ona ait
  değildir):
  - açılıştaki sponsor logoları (ArcadeTown, Newgrounds);
  - Macromedia/Adobe v2 arayüz bileşenleri (`mx.*`: düğme, kaydırma çubuğu, liste);
  - gömülü yazı tipleri: lisansları yazı tipi yapımcılarındadır. Yazılar açık lisanslı karşılıklarıyla
    çizilir: Arial ve `_sans` → Liberation Sans, Times New Roman ve `_serif` → Liberation Serif, Book Antiqua
    → TeX Gyre Pagella, Bookman Old Style → TeX Gyre Bonum, Monotype Corsiva → TeX Gyre Chorus, Century
    Gothic → TeX Gyre Adventor. Eşleme çevirinin kendi tablosundan (`yazitipleri.json`) gelir; tabloda
    olmayanlar ad ve biçeme göre Liberation'a eşlenir. Her yazı tipinin karşılığı `texts.json` içinde
    (`fonts.<kimlik>.file`). Liberation, Arial ve Times New Roman ile aynı ölçülerdedir; yazılar sığar.

- SIL Open Font License 1.1 ticari kullanıma ve yazı tipinin oyunla birlikte dağıtılmasına izin verir;
  yazı tipinin tek başına satılmasını yasaklar. Lisans metinleri yazı tiplerinin yanında durur ve oyunla
  birlikte dağıtılır.
- GUST Font License (LPPL 1.3c) yazı tipinin değiştirilmeden, ticari olanlar dahil her yerde
  dağıtılmasına izin verir; değiştirilmiş sürümün başka adla dağıtılmasını ister. Yazı tipleri
  değiştirilmeden kullanılır; lisans metni yanlarında durur.
- Liberation ve TeX Gyre dosyaları 16 Ekim 2026'da `swf-oyunlar` deposundan alındı (aktarım aracı
  kopyalar, denetim kaynağıyla aynı olduğunu sınar); SHA-256 özetleri:
  - `LiberationSans-Regular.ttf`: `4659bc0c58c5028dd488ec928d41d9265db43d9b669fc14ca8b0832daca7b144`
  - `LiberationSans-Bold.ttf`: `3973aa5054fb467dd5627245d3dc82e37bf16fe075756156a570455871351582`
  - `LiberationSans-BoldItalic.ttf`: `c80fa7f2ffa0e01d4d8dcd6a6d1e43eda665222d1b4db597dde1174c456006cf`
  - `LiberationSerif-Regular.ttf`: `705903ae1382f0150f115d6f10a30f5b2f3d6ade649c474afe6366c39174fb65`
  - `LiberationSerif-Bold.ttf`: `9e66c25e20868756bf12eb24a520a4552727c9cd108f577f7ae33e3c0110e39c`
  - `LiberationSerif-BoldItalic.ttf`: `379010e87421a883f7bbfa7936d23dfe0257a54ce850819b74556e9f2c615a8a`
  - `texgyrepagella-bold.otf`: `dd4f9b69f0b24f1fb9be8634abf1fce2009e5c68a30842a3e9f5d6e535900abd`
  - `texgyrepagella-bolditalic.otf`: `556fd64655a92bd9f5485ae2c03f7b9cdaf745a27a91d7edb3c3abde997206d2`
  - `texgyrebonum-bold.otf`: `173710158270252ec1ddd5e69a07fc71853680c7188d67a84d794a465a4dff81`
  - `texgyrebonum-italic.otf`: `518836a0e5bd71f644ae131185be53b04fadb30ef7dbdc483deb5f69bd1fe47d`
  - `texgyrechorus-mediumitalic.otf`: `b26e0f8edc4c56d881be73c871fb3fbeed045873f9a3202ccad967256d192e65`
  - `texgyreadventor-bold.otf`: `e373ae29c808c6d9149e3add46564f9acdb6ebfcd0ee311f6a55560226994720`
  - `OFL-Liberation.txt`: `1e3d9be3b6014bc5269bca754ecf0d32b5704a489c8b63a792629c99acf3fa6a`
  - `GUST-Font-License.txt`: `4668a2a2e325e62c1928942f69e5215bdb70665970802dc2bd8513c9c9d31d4f`
- Alegreya yazı tipleri 14 Ekim 2026'da indirildi; SHA-256 özetleri:
  - `Alegreya-Variable.ttf`: `ba5564634b93a8f8ba57b48cd4f1ae7417d2b4656fbac779028679b00de3cf12`
  - `AlegreyaSC-Regular.ttf`: `5c8fba800b848b851e308dfdfdc573b64135e498db41cbd0b6d78ba9d267d9a1`
  - `AlegreyaSC-Bold.ttf`: `3ef96cbf3be7b84d9dff9b1aa1e2ac40eec0cf323ccd0638395cdef9c5a91528`
  - `AlegreyaSans-Regular.ttf`: `8fab634196007afca839f1e5a6fb300976daff55d8528b590ef032f01b14ea10`
  - `AlegreyaSans-Bold.ttf`: `a3055a1893759bdbd7504bb22abc583769e7974c49353176eac0b03792c9fb8e`
