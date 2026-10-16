# Ayıklama denetimi

`python3 araclar/aktar/denetim.py --gorsel` üretir. Oyuna aktarılanı FFDec'in kendi
ayrıştırıcısıyla ürettiği XML dökümüyle kayıt kayıt karşılaştırır; şekilleri motorun çizimiyle
FFDec'in çizimi arasında piksel piksel karşılaştırır.

## Feudalism (f1)

| Denetim | Denetlenen | Sorun |
|---|---|---|
| Etiket türlerinin sayıları | 37291 | 0 |
| Karakterler (tür ve yer) | 2093 | 0 |
| Zaman çizelgeleri: her yerleştirme ve kaldırma, etiketler, sesler (durdurma, tekrar, zarf dahil) | 27161 | 0 |
| Düğmeler (her kayıt) | 411 | 0 |
| Dışa aktarılan adlar | 89 | 0 |
| Sabit yazılar (glif glif ve çözülmüş yazı) | 226 | 0 |
| Yazı alanları (değişken, yazı, yazı tipi, boy) | 250 | 0 |
| Sesler (baytlar, örnek sayısı ve MP3 gecikmesi SWF'dekiyle aynı) | 16 | 0 |
| Resimler (açılıyor, boyutu SWF'dekiyle aynı) | 18 | 0 |
| Kod parçaları (kare, sınıf, düğme, klip eylemleri) | 622 | 0 |
| Resim dolgulu şekiller (desen matrisi ve resmi SWF'dekiyle aynı) | 19 | 0 |
| İnce çizgi işaretleri (FFDec'in SVG'sindekilerle aynı) | 1178 | 0 |
| Türkçe çeviri tabloları (kaynağıyla bayt bayt aynı) | 6 | 0 |
| Çeviri hedefleri (her yazı, kutu, yazı tipi ve çizim SWF'de; parça sayısı kayıt sayısıyla aynı) | 266 | 0 |
| Koddaki çeviriler (çevirinin aracı FFDec'in kod dökümüne yeniden uygulanınca aynı) | 56 | 0 |
| Yazı tiplerinin açık lisanslı karşılıkları (dosya kaynağıyla aynı, lisansı yanında) | 15 | 0 |
| Morph sınırları (iki ucun SWF'deki sınırlarının birleşimi) | 11 | 0 |
| Şekiller: motorun çizimi FFDec'inkiyle piksel piksel (en kötü fark %1.80) | 1159 | 0 |
| Morph başlangıç ve bitişleri piksel piksel (en kötü fark %0.67) | 22 | 0 |
| Çizilmiş yazıların Türkçe hâlleri, Türkçe SWF'nin çizimiyle (en kötü fark %0.20) | 1 | 0 |

## Feudalism 2 (f2)

| Denetim | Denetlenen | Sorun |
|---|---|---|
| Etiket türlerinin sayıları | 65626 | 0 |
| Karakterler (tür ve yer) | 3183 | 0 |
| Zaman çizelgeleri: her yerleştirme ve kaldırma, etiketler, sesler (durdurma, tekrar, zarf dahil) | 49419 | 0 |
| Düğmeler (her kayıt) | 387 | 0 |
| Dışa aktarılan adlar | 258 | 0 |
| Sabit yazılar (glif glif ve çözülmüş yazı) | 131 | 0 |
| Yazı alanları (değişken, yazı, yazı tipi, boy) | 193 | 0 |
| Sesler (baytlar, örnek sayısı ve MP3 gecikmesi SWF'dekiyle aynı) | 16 | 0 |
| Resimler (açılıyor, boyutu SWF'dekiyle aynı) | 24 | 0 |
| Kod parçaları (kare, sınıf, düğme, klip eylemleri) | 1126 | 0 |
| Resim dolgulu şekiller (desen matrisi ve resmi SWF'dekiyle aynı) | 31 | 0 |
| İnce çizgi işaretleri (FFDec'in SVG'sindekilerle aynı) | 2147 | 0 |
| Türkçe çeviri tabloları (kaynağıyla bayt bayt aynı) | 6 | 0 |
| Çeviri hedefleri (her yazı, kutu, yazı tipi ve çizim SWF'de; parça sayısı kayıt sayısıyla aynı) | 221 | 0 |
| Koddaki çeviriler (çevirinin aracı FFDec'in kod dökümüne yeniden uygulanınca aynı) | 62 | 0 |
| Yazı tiplerinin açık lisanslı karşılıkları (dosya kaynağıyla aynı, lisansı yanında) | 16 | 0 |
| Morph sınırları (iki ucun SWF'deki sınırlarının birleşimi) | 25 | 0 |
| Şekiller: motorun çizimi FFDec'inkiyle piksel piksel (en kötü fark %1.80) | 2116 | 0 |
| Morph başlangıç ve bitişleri piksel piksel (en kötü fark %1.73) | 50 | 0 |
| Çizilmiş yazıların Türkçe hâlleri, Türkçe SWF'nin çizimiyle (en kötü fark %0.20) | 1 | 0 |

Toplam sorun: 0.

## Yöntem ve sınırlar

- Kaynak: SWF'yi bizim ayrıştırıcımızdan bağımsız okuyan FFDec 24.1.1'in XML dökümü (`-swf2xml`)
  ve FFDec'in kendi PNG çizimleri (şekiller ve morph uçları 4× büyütülmüş).
- Piksel farkı: iki çizim beyaz tuvale gerilmeden konur, ortalama renk farkı %2'yi aşarsa sorun
  sayılır (kenar yumuşatma farkları için pay).
- İnce çizgiler: Flash 1 pikselden ince çizgiyi ekranda 1 piksel çizer. Bu çizgiler
  `data-hairline` ile işaretli aktarılır ve library.json'da listelenir; denetim onları bu kuralla
  çizer. Motor kuralı oynatıcıda uygulayacak (Faz B).
- Morph uçları: FFDec'in morph PNG'leri sınıra belgelenmemiş bir pay ekler; çizimler mürekkep
  merkezi ve en iyi örtüşmeyle hizalanır. Sınırın kendisi XML'deki iki ucun sınırıyla sayısal
  olarak ayrıca denetlenir.
- Resim dolgulu şekiller (zemin dokuları): motor resim dolgusunu henüz çizmediği için sayısal
  denetlenir: kenarların kullandığı her resim dolgusunun SVG'deki desen matrisi SWF'deki dolgu
  matrisiyle, desenin resmi aktarılan resim dosyasıyla piksel piksel aynıdır. Görsel karşılaştırma
  motor resim dolgusunu çizdiğinde eklenecek (Faz B).
- Sesler: dosyalar SWF'deki MP3 verisiyle bayt bayt, örnek sayısı ve MP3 başlangıç gecikmesi
  XML'deki değerlerle aynıdır. Zaman çizelgelerindeki ses kayıtları durdurma, tekrar, giriş/çıkış
  noktası ve zarf bilgisiyle karşılaştırılır.
- Türkçe çeviri: tablolar kaynağıyla (swf-oyunlar) bayt bayt aynıdır; her girdinin hedefi FFDec'in
  dökümünde aranır, sabit yazıların parça sayısı XML'deki kayıt sayısıyla karşılaştırılır. Kod
  çevirisi, çevirinin kendi aracı FFDec'in kod dökümüne yeniden uygulanarak sınanır. "Öldün..."
  çizimi Türkçe SWF'nin FFDec çizimiyle piksel piksel karşılaştırılır.
- Aktarılmayanlar (yerel arşivde): sponsor logoları, Macromedia/Adobe arayüz bileşenleri, gömülü
  yazı tipleri (yerine açık lisanslı karşılıkları). Listesi ve nedenleri
  `kaynak/feudalism/<oyun>/manifest.json` içindedir.
