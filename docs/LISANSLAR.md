# Dışarıdan alınan varlıklar ve lisansları

Oyuna eklenen her yazı tipi, ses, müzik ya da başka dış varlık burada kaynağı ve lisansıyla listelenir.
Kod kütüphanelerinin lisansları `cargo deny` ile denetlenir.

| Varlık | Kaynak | Lisans | Nerede |
| ------ | ------ | ------ | ------ |
| Feudalism ve Feudalism 2 görselleri: şekiller, animasyonlar, düğmeler, ekranlar | Orijinal oyunların SWF dosyaları (`feudalism-orijinal.swf`, `feudalism-2-orijinal.swf`); SHA-256 özetleri `content/feudalism/<oyun>/library.json` içinde | Hak sahibinin izniyle (oyunun sahibinin 16 Ekim 2026'da bildirdiği). Oyunlarda yazan hak sahibi: Vitaly Zaborov ("Copyright Vitaly Zaborov 2008"). İznin tarihi ve kapsamı: **eklenecek** | `content/feudalism/` |
| Alegreya (değişken kalınlık) | [google/fonts](https://github.com/google/fonts/tree/main/ofl/alegreya), yapımcı: Huerta Tipográfica | SIL Open Font License 1.1 | `content/fonts/Alegreya-Variable.ttf`, lisans: `content/fonts/OFL-Alegreya.txt` |
| Alegreya SC (normal, kalın) | [google/fonts](https://github.com/google/fonts/tree/main/ofl/alegreyasc), yapımcı: Huerta Tipográfica | SIL Open Font License 1.1 | `content/fonts/AlegreyaSC-*.ttf`, lisans: `content/fonts/OFL-AlegreyaSC.txt` |
| Alegreya Sans (normal, kalın) | [google/fonts](https://github.com/google/fonts/tree/main/ofl/alegreyasans), yapımcı: Huerta Tipográfica | SIL Open Font License 1.1 | `content/fonts/AlegreyaSans-*.ttf`, lisans: `content/fonts/OFL-AlegreyaSans.txt` |

Notlar:

- Feudalism görsellerinden aktarılmayanlar (izin oyunun yazarının kendi eserini kapsar; bunlar ona ait
  değildir):
  - açılıştaki sponsor logoları (ArcadeTown, Newgrounds);
  - Macromedia/Adobe v2 arayüz bileşenleri (`mx.*`: düğme, kaydırma çubuğu, liste);
  - gömülü yazı tipleri: lisansları yazı tipi yapımcılarındadır; oyunda kendi yazı tiplerimiz kullanılır.

- SIL Open Font License 1.1 ticari kullanıma ve yazı tipinin oyunla birlikte dağıtılmasına izin verir;
  yazı tipinin tek başına satılmasını yasaklar. Lisans metinleri yazı tiplerinin yanında durur ve oyunla
  birlikte dağıtılır.
- Yazı tipleri 14 Ekim 2026'da indirildi; SHA-256 özetleri:
  - `Alegreya-Variable.ttf`: `ba5564634b93a8f8ba57b48cd4f1ae7417d2b4656fbac779028679b00de3cf12`
  - `AlegreyaSC-Regular.ttf`: `5c8fba800b848b851e308dfdfdc573b64135e498db41cbd0b6d78ba9d267d9a1`
  - `AlegreyaSC-Bold.ttf`: `3ef96cbf3be7b84d9dff9b1aa1e2ac40eec0cf323ccd0638395cdef9c5a91528`
  - `AlegreyaSans-Regular.ttf`: `8fab634196007afca839f1e5a6fb300976daff55d8528b590ef032f01b14ea10`
  - `AlegreyaSans-Bold.ttf`: `a3055a1893759bdbd7504bb22abc583769e7974c49353176eac0b03792c9fb8e`
