# Ayıklama denetimi

`python3 araclar/aktar/denetim.py --gorsel` üretir. Oyuna aktarılanı FFDec'in kendi
ayrıştırıcısıyla ürettiği XML dökümüyle kayıt kayıt karşılaştırır; şekilleri motorun çizimiyle
FFDec'in çizimi arasında piksel piksel karşılaştırır.

## Feudalism (f1)

| Denetim | Denetlenen | Sorun |
|---|---|---|
| Etiket türlerinin sayıları | 37291 | 0 |
| Karakterler (tür ve yer) | 2093 | 0 |
| Zaman çizelgeleri: her yerleştirme ve kaldırma, etiketler, sesler | 27161 | 0 |
| Düğmeler (her kayıt) | 411 | 0 |
| Dışa aktarılan adlar | 89 | 0 |
| Sabit yazılar (glif glif ve çözülmüş yazı) | 226 | 0 |
| Yazı alanları (değişken, yazı, yazı tipi, boy) | 250 | 0 |
| Sesler (baytlar SWF'deki veriyle aynı) | 16 | 0 |
| Resimler (açılıyor, boyutu SWF'dekiyle aynı) | 18 | 0 |
| Kod parçaları (kare, sınıf, düğme, klip eylemleri) | 622 | 0 |
| Resim dolgulu şekiller (desen matrisi ve resmi SWF'dekiyle aynı) | 19 | 0 |
| İnce çizgi işaretleri (FFDec'in SVG'sindekilerle aynı) | 1178 | 0 |
| Morph sınırları (iki ucun SWF'deki sınırlarının birleşimi) | 11 | 0 |
| Şekiller: motorun çizimi FFDec'inkiyle piksel piksel (en kötü fark %1.80) | 1159 | 0 |
| Morph başlangıç ve bitişleri piksel piksel (en kötü fark %0.67) | 22 | 0 |

## Feudalism 2 (f2)

| Denetim | Denetlenen | Sorun |
|---|---|---|
| Etiket türlerinin sayıları | 65626 | 0 |
| Karakterler (tür ve yer) | 3183 | 0 |
| Zaman çizelgeleri: her yerleştirme ve kaldırma, etiketler, sesler | 49419 | 0 |
| Düğmeler (her kayıt) | 387 | 0 |
| Dışa aktarılan adlar | 258 | 0 |
| Sabit yazılar (glif glif ve çözülmüş yazı) | 131 | 0 |
| Yazı alanları (değişken, yazı, yazı tipi, boy) | 193 | 0 |
| Sesler (baytlar SWF'deki veriyle aynı) | 16 | 0 |
| Resimler (açılıyor, boyutu SWF'dekiyle aynı) | 24 | 0 |
| Kod parçaları (kare, sınıf, düğme, klip eylemleri) | 1126 | 0 |
| Resim dolgulu şekiller (desen matrisi ve resmi SWF'dekiyle aynı) | 31 | 0 |
| İnce çizgi işaretleri (FFDec'in SVG'sindekilerle aynı) | 2147 | 0 |
| Morph sınırları (iki ucun SWF'deki sınırlarının birleşimi) | 25 | 0 |
| Şekiller: motorun çizimi FFDec'inkiyle piksel piksel (en kötü fark %1.80) | 2116 | 0 |
| Morph başlangıç ve bitişleri piksel piksel (en kötü fark %1.73) | 50 | 0 |

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
- Aktarılmayanlar (yerel arşivde): sponsor logoları, Macromedia/Adobe arayüz bileşenleri, gömülü
  yazı tipleri. Listesi ve nedenleri `kaynak/feudalism/<oyun>/manifest.json` içindedir.
