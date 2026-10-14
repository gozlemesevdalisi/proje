# Sanat rehberi

Oyunun görünüşünü belirleyen kurallar. Yeni bir çizim yapılmadan önce bu belge okunur; çizim bitince
sondaki kontrol listesinden geçirilir. Belge yaşayan bir belgedir: kesinleşen kurallar **Kural:** diye,
henüz denenen fikirler **Deneme:** diye işaretlenir.

## Ruh

Flash döneminin el çizimi vektör oyunlarının sıcaklığı: temiz ve yumuşak hatlar, belirgin şekiller,
parlak gök, yemyeşil çayır, toprak tonları, yumuşak degradeler. Karakterler stilize ve abartılı oranlı;
gerçekçi değil, sevimli de değil. Hafif çizgi roman havası olan bir ciddiyet.

Tek cümleyle: **elle boyanmış bir masal kitabı değil, elle kesilmiş renkli kâğıtlardan kurulmuş, güneşli
bir ortaçağ sahnesi.**

**Kural:** Bütün çizimler bu oyun için özgün olarak yapılır. Esin kaynağı olan oyunların çizimleri,
yerleşimleri, adları ve metinleri kopyalanmaz, izlenmez, değiştirilerek kullanılmaz.

## Esin kaynağının çözümlemesi

Esin kaynağı olan iki Flash oyununun ekranları incelendi ve dosyalarındaki ~3.400 vektör şekil sayısal
olarak çözümlendi. Tarzı yapan şeyler:

| Ne                  | Ölçülen                                                                                       | Bizim için anlamı                                         |
| ------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Kontur              | Şekillerin ~%85'inde hiç çizgi yok; kenarların yalnızca %7–8'i çizgili; çizgilerin %85'i ≤1 px | Şekiller renk ve ton farkıyla ayrılır, çizgiyle değil     |
| Dolgu               | Dolguların ~%65'i düz renk, ~%30'u doğrusal, ~%5'i radyal degrade                             | Düz renk esastır; degrade hacim vermek içindir            |
| Degrade durakları   | Degradelerin %92'si iki renkli, kalanı üç renkli                                              | Degrade sade tutulur                                      |
| Degrade yönü        | Neredeyse hepsi yatay ya da dikey                                                             | Basit, okunur gölgeleme                                    |
| Degrade farkı       | İki uç arasındaki parlaklık farkı ortanca ΔL\* ≈ 21                                           | Yumuşak ama görünür hacim                                 |
| Renk karıştırma     | Bütün degradeler sRGB uzayında karışıyor                                                      | Motor da sRGB uzayında karıştırır                         |
| Eğri oranı          | Kenarların yarısı eğri (ikinci derece Bézier)                                                 | Yumuşak, akan hatlar                                       |
| Saydamlık           | Dolguların %2'sinden azı yarı saydam                                                          | Saydamlık yalnızca ışık, gölge ve sis için                |
| Işık yönü           | Her nesne kendi içinde, rastgele yönden gölgelenmiş                                           | **Bizde düzeltilir:** ışık her zaman sol üstten gelir     |
| Karakterler         | 6,5–7,5 baş boyu; geniş omuz, iri el ve ayak; parçalı kukla (12–22 parça)                      | Oranlar korunur; kukla yapısı motorun merkezindedir       |
| Çeşitlilik          | Askerler kahraman çizimlerinin küçültülmüşü; şehirler aynı şablon                              | **Bizde düzeltilir:** her asker, şehir ve savaş farklıdır |

Esin kaynağının zayıf yanları da not edildi ve bizde tekrarlanmaz: sıradan yazı tipleri (Arial,
Times), tarza uymayan düz beyaz konuşma kutuları, tutarsız ışık, bütün şehirlerin aynı yerleşimi,
sabit ve tek katmanlı savaş arka planları.

## Temel ilkeler

1. **Şekil önce gelir.** Her nesne önce tek renk bir siluet olarak tanınabilmelidir. Ayrıntı, siluet
   oturduktan sonra eklenir.
2. **Az ama doğru ton.** Her parça en fazla üç tondan oluşur: ana renk, gölge, ışık. Ara tonları
   degrade sağlar.
3. **Işık sol üstten gelir.** Yaklaşık 45° açıyla, sol üstten. Aydınlık yüzler sola ve yukarıya,
   gölgeler sağa ve aşağıya bakar. Gün saati ışığın rengini değiştirir, yönünü değiştirmez.
4. **Sıcak ışık, serin gölge.** Gündüz ışık hafif sarıya, gölge hafif maviye ya da mora kayar.
   Gölge, ana rengin koyulaştırılmışı değil, tonu kaydırılmışıdır.
5. **Uzak olan soluk ve mavidir.** Hava perspektifi: katman uzaklaştıkça gök rengine karışır.
6. **Oyun alanı okunur kalır.** Süs, savaşın ve arayüzün okunmasını hiçbir zaman engellemez.

## Renk paleti

**Kural:** Renkler sRGB değerleriyle verilir ve sRGB uzayında karıştırılır (esin kaynağındaki gibi).
Çizimlerde bu paletteki renkler ve bunların degradeleri kullanılır. Palete yeni renk gerekirse önce
buraya eklenir.

### Gök ve ışık

| Ad              | Renk      | Kullanım                               |
| --------------- | --------- | -------------------------------------- |
| gök-tepe        | `#1E4FA6` | Gündüz göğün üst kenarı                |
| gök-orta        | `#3B7BCB` | Gündüz göğün ortası                    |
| gök-ufuk        | `#9FCBEA` | Ufuk çizgisi                           |
| ufuk-sıcak      | `#F3E2B0` | Sabah ve akşam ufku                    |
| güneş           | `#FFF6D2` | Güneş diski                            |
| güneş-parıltı   | `#FFE9A0` | Güneşin radyal parıltısı (saydamlaşır) |
| bulut           | `#FFFFFF` | Bulutların aydınlık yüzü               |
| bulut-gölge     | `#D6E2EF` | Bulutların alt yüzü                    |
| gece-tepe       | `#0A1530` | Gece göğün üst kenarı                  |
| gece-ufuk       | `#2E4A6E` | Gece ufku                              |
| ay              | `#F4F1E0` | Ay diski                               |
| ay-parıltı      | `#9FB3C8` | Ayın radyal parıltısı                  |

### Çayır, toprak, taş, su

| Ad            | Renk      | Ad             | Renk      |
| ------------- | --------- | -------------- | --------- |
| çimen-açık    | `#8DBF4A` | toprak-açık    | `#8A6A3B` |
| çimen         | `#5E9A3A` | toprak         | `#6B4E2A` |
| çimen-koyu    | `#3B6E2C` | toprak-koyu    | `#47331D` |
| çimen-gölge   | `#24461F` | yol            | `#C9A96E` |
| kuru-ot       | `#B8A23C` | taş-açık       | `#A39E92` |
| saman         | `#D9C26A` | taş            | `#7D776C` |
| su-açık       | `#2F7FB5` | taş-koyu       | `#57534B` |
| su            | `#1C5A8E` | kar            | `#F4F7FA` |
| su-derin      | `#0F3D66` | kar-gölge      | `#C5D3E3` |
| köpük         | `#E3F1F7` |                |           |

### Ağaç ve bitki

| Ad              | Renk      | Ad              | Renk      |
| --------------- | --------- | --------------- | --------- |
| yaprak-açık     | `#6FAE3F` | gövde           | `#6E4B2A` |
| yaprak          | `#3F7F2E` | gövde-koyu      | `#4A3019` |
| yaprak-koyu     | `#24552A` | huş-gövde       | `#EDEBE4` |
| çam             | `#2E6B3E` | huş-leke        | `#3A3A35` |
| çam-koyu        | `#1F4D2E` | çiçek-kırmızı   | `#C8372D` |
| çalı            | `#4C8A3A` | çiçek-sarı      | `#F2C744` |

### Ten ve saç

Her ten tonunun bir gölge rengi vardır; gölge, ana rengin tonu kırmızıya kaydırılarak elde edilir.

| Ten        | Ana       | Gölge     | Saç       | Renk      |
| ---------- | --------- | --------- | --------- | --------- |
| açık       | `#F2CFA8` | `#D9A97E` | siyah     | `#231A14` |
| buğday     | `#E0B07E` | `#C08A5A` | kahve     | `#5A3A22` |
| esmer      | `#B67E50` | `#915F38` | kızıl     | `#A8431E` |
| koyu       | `#7D5233` | `#5E3B22` | sarı      | `#E8C66A` |
|            |           |           | kır       | `#B9B3A8` |

### Kumaş, deri, metal

| Ad                | Renk      | Ad              | Renk      |
| ----------------- | --------- | --------------- | --------- |
| kırmızı           | `#A3241A` | çelik-açık      | `#DCE2E8` |
| kırmızı-gölge     | `#6E140F` | çelik           | `#9AA4AE` |
| lacivert          | `#23406E` | çelik-koyu      | `#5C646C` |
| lacivert-gölge    | `#142748` | demir           | `#6E6A66` |
| yeşil             | `#3E7A35` | altın-açık      | `#FFD966` |
| hardal            | `#C9962E` | altın           | `#E8B22C` |
| mor               | `#5E3A6E` | altın-koyu      | `#A6781C` |
| keten             | `#E6DCC3` | bronz           | `#C08A3E` |
| keten-gölge       | `#BFAE8C` | bronz-koyu      | `#7A5222` |
| deri              | `#8B5A2B` | ahşap-açık      | `#9C6A3C` |
| deri-koyu         | `#5C3A1B` | ahşap           | `#7A4E2A` |
|                   |           | ahşap-koyu      | `#5A3719` |

### Arayüz

| Ad                | Renk      | Kullanım                                   |
| ----------------- | --------- | ------------------------------------------ |
| parşömen          | `#F1E3C2` | Pencere zemini (ortası)                    |
| parşömen-kenar    | `#CDB284` | Pencere zemininin kenarları                |
| parşömen-koyu     | `#8C6B3F` | Kıvrık uçlar, yırtık kenar gölgesi         |
| mürekkep          | `#2E2116` | Parşömen üstündeki yazı                    |
| mürekkep-soluk    | `#6B5A44` | İkincil yazı                               |
| çerçeve-altın     | `#F5C842` | Çerçevenin aydınlık yüzü                   |
| çerçeve-altın-koyu| `#A6781C` | Çerçevenin gölge yüzü                      |
| mühür             | `#A61E1E` | Onay düğmesi, önemli uyarı                 |
| mühür-koyu        | `#6B0F0F` | Mührün gölgesi                             |
| tahta             | `#7A4E2A` | Tahta panolar                              |
| tahta-yazı        | `#F1E3C2` | Tahta üstündeki yazı                       |
| uyarı             | `#8E1B12` | Parşömen üstünde uyarı yazısı              |

### Bölge paletleri

Her bölge, ana paletin üstüne kendi baskın renklerini koyar. Bir ekran görüntüsünden hangi bölgede
olunduğu anlaşılabilmelidir.

| Bölge              | Baskın renkler                                                         | Hava                                 |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------ |
| Bozkır Beylikleri  | altın çayır `#C9B04A`, hardal `#9E9034`, keçe kırmızısı, at kahvesi     | Geniş, açık gök, uzun ufuk           |
| Kıyı Kentleri      | badana `#F2EEE4`, kiremit `#C0603A`, turkuaz deniz `#2E9AA8`, zeytin `#7C8A3A` | Parlak, beyaz ışık, deniz meltemi |
| Dağ Kaleleri       | gri taş `#8C8A85`, mavi gölge `#5D6B7A`, koyu çam `#24452E`, demir      | Serin, keskin gölgeler, yükseklik    |
| Orman Sınırı       | koyu yeşil `#2F5A2A`, yosun `#6E8A3A`, sis yeşili `#9DB39A`, ahşap      | Loş, katman katman ağaç, sis         |
| Kuzey Akıncıları   | buz mavisi `#CFE3EE`, kar, koyu deniz `#233B52`, pas ahşap `#7A3B26`    | Soğuk, alçak güneş, uzun gölgeler    |
| Kum Yolları        | kum `#E8C77A`, turuncu kum `#D99A4E`, kum gölgesi `#B07A45`, vaha yeşili `#4E9A55`, çivit `#2C4F8A` | Sıcak, beyaza yakın gök, titreşen ufuk |

### Gün saati

Gün saati, katmanların renklerine çarpan ve eklenen bir renk dönüşümüyle verilir (Flash'taki
renk dönüşümü gibi). Çizimler gündüz renkleriyle yapılır; saat ayarı motordan gelir.

| Saat    | Işık                         | Gölge             | Gök                                  |
| ------- | ---------------------------- | ----------------- | ------------------------------------ |
| Sabah   | Altın sarısı, yumuşak        | Mavi-mor          | Ufuk sıcak, tepe açık mavi           |
| Öğle    | Nötr, parlak                 | Serin mavi        | Doygun mavi                          |
| Akşam   | Turuncu-pembe                | Mor               | Ufuk turuncu, tepe lacivert          |
| Gece    | Mavi ay ışığı, düşük doygunluk | Lacivert        | Gece paleti, ay ve yıldızlar         |

**Kural:** Saat geçişleri yavaştır (en az birkaç saniye); ani tam ekran renk değişimi yoktur.

## Degrade kuralları

- **Kural:** Bir degradede en fazla üç durak olur; varsayılan iki duraktır.
- **Kural:** Degradeler sRGB uzayında karışır; uçlar "pad" (son renk devam eder) yayılır.
- Doğrusal degrade **hacim** içindir: aydınlık uç sol üste, koyu uç sağ alta bakar. Silindir biçimli
  parçalarda (kol, bacak, kütük, sütun) yatay degrade kullanılır; aydınlık bant soldan üçte birdedir.
- İki uç arasındaki parlaklık farkı ΔL\* 12–30 arasında kalır. Daha azı görünmez, daha fazlası
  plastik ve parlak durur.
- Radyal degrade **ışık ve gölge** içindir: güneş ve ay parıltısı, parşömenin aydınlık ortası,
  ayak altı gölgesi, büyü parıltısı. Parıltılar saydamlığa doğru söner.
- Gök ve zemin büyük dikey degradelerdir.
- Gölgeler ayrı bir şekil olarak da çizilebilir (düz, yarı saydam koyu şekil); bu, esin kaynağının
  da sık kullandığı, kâğıt kesimi hissini güçlendiren bir yoldur.

## Kontur kuralları

**Kural:** Ortam (gök, arazi, ağaç, bina, eşya) **kontursuzdur**. Şekiller birbirinden renk ve ton
farkıyla ayrılır.

**Kural:** Karakterler (insan, at, hayvan) okunabilirlik için **ince, koyu renkli bir dış hat** alır:

- Dış hat yalnızca karakterin dış çevresinde ve parçalar birbirinin üstüne bindiği yerlerde çizilir.
- Rengi **saf siyah değildir**: dış hattın bittiği parçanın renginin koyulaştırılmış ve tonu
  kaydırılmış hâlidir (parlaklık %30–40'a düşer). Siyah saç ya da kumaşta `#1A1410` kullanılır.
- Kalınlığı karakter çizim ölçeğinde **5 birimdir** (aşağıya bakınız); savaşta ekranda ~1,3 piksele
  denk gelir.
- Kol, bacak gibi silindir parçalarda dış hat uçlarda biraz incelir (kalem baskısı hissi); bu,
  hattın dolgu olarak çizilmesiyle sağlanır.

**Kural:** İç çizgiler (yüz, kumaş kıvrımı, zırh perçini) ince ve azdır: 2–2,5 birim, dış hattın
rengindedir. Bir parçada üç-dört iç çizgiden fazlası olmaz.

**Kural:** Simgeler ve arayüz süsleri kontursuz çizilir; okunabilirlik için dış çevrelerine 2 birimlik
koyu kenar ya da hafif gölge verilebilir.

## Ölçek ve birimler

Bütün çizimler SVG olarak tutulur. Bir SVG biriminin ekranda kaç piksel olduğu çizimin türüne göre
sabittir:

| Tür               | Çizim alanı                                    | Ekrana ölçek                                         |
| ----------------- | ---------------------------------------------- | ---------------------------------------------------- |
| Ekran ve arayüz   | 1 birim = 1 mantıksal piksel (1920×1080 ekran) | 1                                                    |
| Manzara katmanı   | 1 birim = 1 mantıksal piksel; genişlik ekrandan büyük olabilir | Paralaksa göre kayar                    |
| Karakter          | Baş yüksekliği 64 birim; yetişkin boyu 7 baş = 448 birim | Savaşta ~0,27 (≈120 piksel), seçim ekranında 1–1,4 |
| Simge             | 128×128 birim                                  | Arayüzde 48–96 piksel                                |

Mantıksal ekran 1920×1080'dir; motor bunu pencere boyutuna ölçekler. Çizimler vektör olduğu için
her ölçekte keskindir.

## Karakterler

### Oranlar

| Ölçü                   | Değer (baş = 64 birim) |
| ---------------------- | ---------------------- |
| Boy                    | 7 baş (kahraman 7–7,5; iri savaşçı 6,5–7) |
| Omuz genişliği (erkek) | 2,2–2,6 baş            |
| Omuz genişliği (kadın) | 1,7–2 baş              |
| El boyu                | 0,85 baş (bilerek iri) |
| Ayak boyu              | 1,15 baş (bilerek iri) |
| Bacak boyu             | Boyun yarısı           |

- Baş küçük, gövde ve omuzlar güçlü; kahramanca ama gerçekçi değil.
- Yüz: belirgin kaş ve çene; gözler küçük (badem ya da nokta), burun tek çizgi ya da küçük bir gölge
  şekli, ağız tek çizgi. **Büyük göz, yuvarlak bebek yüzü, sevimli oran yok.**
- Duruş: ağırlık bir bacakta, hafif öne eğik; silah elde, hazır.
- Eller ve ayaklar abartılıdır: silah tutuşu ve adım ekranda küçükken de okunur.

### Siluet

**Kural:** Her birlik türü, tek renk siluetinden ayırt edilebilmelidir. Siluetin farkı miğfer biçimi,
silah uzunluğu, kalkan biçimi ve duruştan gelir; renk farkı ikinci sıradadır.

### Parçalı kukla

Karakterler ayrı parçalardan kurulur; parçalar kemiklere bağlıdır ve döndürülerek canlandırılır.

| Parça                       | Not                                                      |
| --------------------------- | -------------------------------------------------------- |
| baş, saç, yüz ayrıntısı     | Yüz parçaları değiştirilebilir (kaş, burun, ağız, sakal) |
| boyun, gövde, kalça         | Zırh gövdenin üstüne giyilir                             |
| üst kol, ön kol, el (×2)    | Arka kol bir ton koyu çizilir                            |
| üst bacak, alt bacak, ayak (×2) | Arka bacak bir ton koyu çizilir                      |
| silah, kalkan, miğfer, pelerin | Donanım; değişince görünüş değişir                    |

- **Kural:** Eklem yerlerinde parçalar yuvarlak uçla birbirinin altına girer (bindirme payı en az
  0,2 baş); parça döndüğünde boşluk görünmez.
- **Kural:** Her parçanın dönme noktası (eklemi) parçanın SVG'sinde işaretlenir.
- Arka plandaki kol ve bacak, öndekinden bir ton koyudur; derinlik böyle verilir.

### Her asker bir kişidir

Aynı birlikten iki asker yan yana durduğunda farkı görülmelidir:

- Yüz parçaları kataloğu: kaş, burun, ağız, bıyık ve sakal, saç biçimi; ten tonu (4) ve saç rengi (5).
- Boy ölçeği 0,94–1,06; omuz genişliği ölçeği 0,92–1,10.
- Donanımda küçük farklar: yıpranma, yama, renkli şerit, tüy.
- Gaziler görünüşünden tanınır: yara izi, nişan, farklı pelerin ya da sancak.

## Manzara katmanları

Savaş alanları ve şehir sahneleri katmanlardan kurulur; katmanlar kamera kayarken farklı hızlarda
kayar (paralaks).

| Sıra | Katman            | Paralaks | Gök rengine karışım | İçerik                                   |
| ---- | ----------------- | -------- | ------------------- | ---------------------------------------- |
| 1    | Gök               | 0        | —                   | Dikey degrade, güneş ya da ay, bulutlar   |
| 2    | Uzak              | 0,1–0,2  | %50–60              | Dağ ve tepe siluetleri                   |
| 3    | Orta uzak         | 0,3–0,4  | %25–35              | Ağaç sıraları, kale siluetleri           |
| 4    | Yakın arka plan   | 0,6–0,8  | %0–10               | Ağaçlar, yapılar, çitler                 |
| 5    | Savaş zemini      | 1        | —                   | Lekeli çayır, yollar, su; oyun alanı     |
| 6    | Ön plan           | 1,2–1,4  | —                   | Çimen öbekleri, çalılar (kenarlarda)     |

- Zemin düz tek renk değildir: iki-üç tonlu, yumuşak kenarlı büyük lekelerden oluşur.
- Ön plan oyun alanını kapatmaz; ekranın alt ve yan kenarlarında kalır.
- Karakterlerin altında yumuşak, yarı saydam koyu bir elips gölge vardır.
- Arazi, hava, saat ve amaç birlikte her savaşı farklı gösterir; aynı katman takımı iki savaşta aynı
  dizilimle kullanılmaz.

## Arayüz

Arayüz, oyunun dünyasından yapılmış nesneler gibi görünür: parşömen, tahta, altın, mühür, kalkan.

| Öğe              | Görünüş                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------- |
| Pencere          | Parşömen yaprak: ortası aydınlık (radyal degrade), kenarları koyulaşır; kenar hafif dalgalı; köşeler kıvrık |
| Çerçeve          | İnce altın çerçeve (iki duraklı altın degrade) ya da tahta pano                              |
| Başlık           | Kurdele (uçları çatallı) ya da tahta tabela                                                   |
| Ana menü düğmesi | Kılıç ya da sancak biçimli; üstüne gelince hafif altın parıltı                               |
| Onay düğmesi     | Kırmızı mühür (dalgalı kenarlı oval)                                                          |
| Seçim düğmesi    | Kalkan biçimli; içinde arma ya da simge                                                       |
| Bilgi kutusu     | Kıvrık uçlu parşömen tomarı                                                                   |
| Konuşma          | Konuşanın portresi + parşömen; **düz beyaz baloncuk yok**                                     |
| Simgeler         | El çizimi iksir şişeleri, parşömenler, silahlar; kontursuz, ışık sol üstten                   |

Davranış:

- Üstüne gelince: yumuşak altın parıltı (0,15 saniyede belirir).
- Basınca: 2 piksel aşağı iner ve bir ton koyulaşır.
- Klavyeyle seçilen öğenin etrafında altın odak çerçevesi vardır.

### Yazı

| Kullanım           | Yazı tipi        | Boyut (1080p) |
| ------------------ | ---------------- | ------------- |
| Oyunun adı         | Alegreya SC Bold | 96–128        |
| Başlık             | Alegreya SC      | 40–56         |
| Düz metin          | Alegreya         | 26            |
| Küçük metin, sayı  | Alegreya Sans    | 20–22         |

- Satır aralığı yazı boyunun 1,3 katıdır.
- Parşömen üstünde yazı `mürekkep`, tahta üstünde `tahta-yazı` rengindedir.
- **Kural:** Türkçe büyük harf dönüşümü Türkçe kurallarla yapılır (i → İ, ı → I).

## Dünya haritası

Elle çizilmiş, yaşayan bir harita:

- Deniz: lacivertten açık maviye degrade; kıyıya yakın açık şerit; elle çizilmiş dalga kıvrımları.
- Kara: bölge rengine göre yumuşak degradeli büyük lekeler; kıyı boyunca açık renkli bir "kalınlık"
  şeridi (kara parçası kâğıttan kesilip yapıştırılmış gibi durur).
- Şehirler: kültürüne göre farklı, 3/4 kuşbakışı küçük simgeler; her şehrin simgesi kendine özgü
  bir ayrıntı taşır (liman, kule, kubbe).
- Süsler: dağlar, ağaç kümeleri, palmiye ve vaha, kum tepecikleri, yol izleri.
- Kenar: eski harita süsleri (pusula gülü, kenar bordürü); yazılar Alegreya.
- Mevsim haritaya yansır: kışın kuzey beyazlaşır, baharda nehirler genişler.

## Şehirler

**Kural:** İki şehir aynı yerleşimle çizilmez. Her şehrin kendi manzarası (dağ yamacı, liman, vaha,
nehir adası), kendi mimarisi ve kendi özel binası vardır. Bir şehir ekran görüntüsünden tanınabilmelidir.

## Hareket ve efektler

- Kukla animasyonu yumuşak geçişlidir (yavaşlayarak başlayan ve biten); vuruşlarda kısa bir ön
  hazırlık ve vuruş anında 2–3 karelik duraklama olur.
- Efektler (kıvılcım, toz, kan) küçük ve yereldir; vektör parçacıklarla çizilir.

**Kural (görsel güvenlik):**

- Hiçbir efekt saniyede 3'ten fazla parlama üretmez.
- Ani tam ekran beyaz ya da kırmızı geçiş yoktur; ekran geneli renk değişimleri en az 0,5 saniyede olur.
- Doygun kırmızıyla yanıp sönen efekt yoktur.

## SVG yazım kuralları

Motorun okuduğu SVG alt kümesi:

- Kullanılır: `path`, `rect`, `circle`, `ellipse`, `polygon`, `polyline`, `line`, `g`, `transform`,
  `fill`, `stroke`, `opacity`, `fill-opacity`, `linearGradient`, `radialGradient`, `stop`.
- Kullanılmaz: filtreler (bulanıklaştırma, gölge), maske, desen, gömülü resim, SVG içinde yazı.
  Yazılar motorda çizilir.
- Grup saydamlığı (`<g opacity>`) yerine her şeklin kendi saydamlığı kullanılır.
- Kimlikler (`id`) İngilizce ve küçük harflidir: `head`, `torso`, `arm-upper-front`.
- Renkler bu belgedeki paletten seçilir.

## Yapılmayacaklar

- Esin kaynağı oyunların çizimlerini, yerleşimlerini, adlarını ve metinlerini kullanmak, izlemek ya da
  değiştirerek kopyalamak.
- Saf siyah kalın kontur; ortamda kontur.
- Fotoğraf dokusu, resim dosyası, gürültü dokusu.
- Neon ya da çok doygun "dijital" renkler; gökkuşağı degradeleri; üçten fazla duraklı degrade.
- Plastik parlaklık: çok güçlü degrade, keskin parlama lekeleri.
- Sevimli (büyük baş, büyük göz) ya da gerçekçi anatomi.
- Tutarsız ışık yönü.
- Bulanıklaştırma, mercek parlaması, yanıp sönen ışık efektleri.
- Arial, Times gibi sıradan yazı tipleri; düz beyaz konuşma baloncukları.
- İki şehri, iki savaşı ya da iki askeri birebir aynı çizmek.

## Kontrol listesi

Her yeni çizim için:

- [ ] Tek renk siluet olarak tanınıyor mu?
- [ ] Renkler paletten mi?
- [ ] Işık sol üstten mi geliyor? Gölgeler serin mi?
- [ ] Degradeler en fazla üç duraklı ve ΔL\* 12–30 arasında mı?
- [ ] Ortam kontursuz mu? Karakterde dış hat ince ve koyu renkli (siyah değil) mi?
- [ ] Oranlar bu belgeye uyuyor mu?
- [ ] Kukla parçalarında bindirme payı ve dönme noktası var mı?
- [ ] SVG yalnızca izin verilen öğeleri mi kullanıyor?
- [ ] Başka bir şeyin kopyası değil, özgün mü?

## Örnek çizimler

Tarzın onayı için dört örnek hazırlanır: bir kahraman, bir asker, bir manzara, bir arayüz penceresi.
Örneklerin SVG dosyaları `content/art/samples/`, motorun çizdiği görüntüleri `docs/sanat/` altında
durur. Örnekler onaylanana kadar çizim üretimi artırılmaz.
