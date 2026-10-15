# Sanat rehberi

Oyunun görünüşünü belirleyen kurallar. Kurallar esin kaynağı iki Flash oyununun dosyalarından ve
ekranlarından **ölçülerek** çıkarıldı. Sayıların hepsi ölçümdür, tahmin değildir.

Yeni bir çizim şu sırayla yapılır:

1. Bu belge okunur.
2. Çizim yalnızca paletteki renklerle yapılır.
3. Çizim bitince otomatik denetimden geçirilir.
4. Referansla yan yana konup farklar listelenir ve düzeltilir.
5. Sondaki kontrol listesinden geçirilir.

Belge yaşayan bir belgedir. Kesinleşen kurallar **Kural:** diye işaretlenir.

Belgedeki ölçü kısaltmaları:

| Kısaltma | Anlamı                                                                   |
| -------- | ------------------------------------------------------------------------ |
| L\*      | Açıklık: 0 siyah, 100 beyaz                                              |
| C\*      | Doygunluk: 0 gri; 60'ın üstü çok canlı                                   |
| ΔL\*     | İki ton arasındaki açıklık farkı                                         |
| baş      | Karakter çiziminde başın yüksekliği: 64 SVG birimi (başlık hariç)        |

## Ruh

Flash döneminin elle çizilmiş vektör oyunları. Hepsi aynı ilkeye dayanır:

- Keskin kenarlı, temiz şekiller vardır.
- Geniş, düz ve canlı renk alanları vardır.
- Hiç dış hat (kontur) yoktur.
- Komşu malzemeler arasında büyük açıklık farkı vardır.
- Az ama iri ve okunur ayrıntı vardır.

Karakterlerin oranları kahramancadır: küçük baş, geniş omuz, iri kol, iri el. Yüzleri sadedir ama
gözleri açıktır ve izleyiciye bakar. Karakterler gerçekçi değildir, sevimli de değildir.

Tek cümleyle: **renkli kâğıttan kesilmiş, keskin kenarlı, güneşli bir ortaçağ sahnesi.** Yumuşak
geçiş yalnızca büyük alanlarda ve azdır.

**Kural:** Bütün çizimler bu oyun için özgün olarak yapılır. Esin kaynağı olan oyunların çizimleri,
yerleşimleri, karakterleri, simgeleri, adları ve metinleri kopyalanmaz, izlenmez, değiştirilerek
kullanılmaz. Esin kaynağından yalnızca **tarz** alınır: şekil dili, renk yaklaşımı, oranlar,
gölgeleme yöntemi.

## Yasaklar

Bu liste kesindir. Bir çizimde bunlardan biri varsa çizim kabul edilmez.

| Yasak                                                    | Neden                                                     |
| -------------------------------------------------------- | --------------------------------------------------------- |
| **Low-poly** (düz kenarlı, köşeli çokgen şekiller)       | Esindeki sertlik çokgenden değil, keskin kenarlı Bézier eğrilerinden gelir |
| **Pul pul zırh dokusu** (pul, örgü, kapitone sıraları)   | Doku gibi yayılan ayrıntı göz yorar, figürü yavanlaştırır |
| **Perçin ayrıntısı**                                     | Aynı nedenle; metal iki tonla ve keskin bölünmeyle verilir |
| **Gerçekçi yüz** (anatomik ayrıntı, kırışık, gölge geçişi) | Yüz sade, simgesel ve okunur olmalıdır                  |
| Karakterde dış hat (kontur)                              | Esinde hiçbir karakterde kontur yok                       |
| Ortamda dış hat                                          | Aynı nedenle                                              |
| Soluk ve boz palet                                       | Esinde ana renkler C\* 65–80                              |
| Grileşmiş ya da mora kaymış gölge                        | Gölge aynı renk ailesinde kalır                           |
| Kapsül ya da sosis biçimli uzuv (iki ucu yarım daire, paralel kenar) | Uzuvlar bir yanı düz, bir yanı şişkin çizilir |
| İnce doku çizgileri (dikiş, damar, tahta damarı, kumaş kıvrım çizgisi) | Ayrıntı çizgiyle değil, şekille yapılır     |
| Çapraz ya da çok duraklı (4+) degrade                    | Esinde degradeler 2 duraklı, yatay ya da dikey            |
| Her yüzeyde degrade, tende degrade                       | Esinde ten düz, kumaşta degrade yardımcıdır               |
| Hava fırçası görünüşü, yumuşak kenarlı gölge             | Gölge keskin kenarlı ayrı bir şekildir                    |
| Büyük baş, büyük göz, yuvarlak bebek yüzü                | Sevimlilik tarzın tersidir                                |
| Kapalı ya da uykulu göz (uyku ve ölüm dışında)           | İfadeyi açık göz taşır                                    |
| Paletin dışında renk                                     | Renkler ölçülmüş paletten seçilir                         |
| Fotoğraf, resim dosyası, gürültü dokusu, bulanıklaştırma | Tarz saf vektördür                                        |
| Neon yeşil, saf `#000000` ile geniş siyah alan           | Esinin zayıf yanları; siyah yalnızca küçük alanlarda       |
| Sıradan yazı tipi (Arial, Times), düz beyaz konuşma balonu | Esinin zayıf yanları                                    |
| Aynı yerleşimle iki şehir, aynı dizilimle iki savaş, birebir aynı iki asker | Her biri farklı olmalıdır             |

## Referanslar

Ölçümler esin kaynağı iki oyunun dosyalarından ve ekranlarından yapıldı.

**Kural:** Referans görüntüleri ve esin kaynağının dosyaları bu depoya **konmaz**. Gerektiğinde
aşağıdaki yolla yeniden üretilir.

### Neler ölçüldü

| Kaynak                                       | Ne çıkarıldı                                                         |
| -------------------------------------------- | -------------------------------------------------------------------- |
| Birinci oyunun SWF dosyası, `Human` ve `Human_Player` kuklaları | Savaş kuklalarının dolgu ve çizgi istatistiği, düz renkleri |
| Aynı dosyada `Tree_1`…`Tree_12`, `Bush_1`…`Bush_4`, `Cities`, `WorldMap`, `Screen` | Ağaç, çalı, şehir, harita ve arayüz renkleri |
| Kahraman seçim ekranı (4× büyütülmüş)        | Yedi kahramanın malzeme renkleri, degrade uçları, oranlar, yüzler    |
| Gündüz huş ormanı savaşı (4×)                | Gök, ağaç, çimen, zemin renkleri; savaş arayüzü, parşömen kartlar    |
| Savaş öncesi orman resmi (4×)                | Çam katmanları, gece göğü                                            |
| Dünya haritası (4×)                          | Deniz, kara, kıyı renkleri                                           |
| Dükkân ekranı                                | Altın çerçeve, parşömen yuva, kırmızı ok düğmeleri                   |

### Yeniden üretmek

İnceleme deposu `swf-oyunlar`, oyunları tarayıcıda Ruffle ile oynatır.

1. Depoyu klonla ve kökünde `python3 -m http.server 8000` çalıştır.
2. Playwright ile Chromium aç: `deviceScaleFactor: 4`, `locale: "tr-TR"`.
   - Locale verilmezse Ruffle "yanlış yerel ayar" hatası verir.
3. `http://localhost:8000/` adresini aç ve oyunu seç. Sahne 800×600'dür; çevresinde siyah pay
   olabilir.
   - İlk tıklama sahneye odak verir.
   - Tıklama koordinatları sahneye göredir.
4. Ölçülen ekranlar:
   - **Kahraman seçimi:** ana menü → yeni oyun.
   - **Gündüz savaşı:** haritada ilk savaş.
   - **Savaş öncesi resim:** savaşa girerken.
   - **Harita:** yeni oyundan sonra.
5. Sahne alanının görüntüsünü al.

Ölçüm betikleri `tools/referans/` klasöründedir:

| Betik                 | Ne yapar                                                                      |
| --------------------- | ----------------------------------------------------------------------------- |
| `swfstats.py`         | SWF'deki şekilleri çözer (dolgu, çizgi, kenar)                                |
| `char_palette.py`     | Bir kuklaya bağlı bütün şekillerin renklerini sayar                           |
| `sample_materials.py` | Kahraman seçim ekranında malzeme başına ana, açık ve koyu rengi ölçer         |

Kutu koordinatları betiklerin içindedir; hepsi 800×600 sahne koordinatıdır.

## Ölçümler

### Savaş kuklaları (SWF'den sayıldı)

- **Dolgu:** 1022 düz renk dolgu, 0 degrade.
- **Çizgi:** kenarların yalnızca %1,4'ü çizgili; çizgiler yay kirişi gibi doğası çizgi olan şeyler.
- **Tonlar:** her parça 2 düz ton (ana renk ve keskin kenarlı gölge).

### Büyük resimler (kahraman seçimi, 4× ekran görüntüsünden)

| Ölçü                               | Esinde                                                            |
| ---------------------------------- | ----------------------------------------------------------------- |
| Kontur                             | Yok. Renk, araya çizgi girmeden doğrudan başka renge geçer        |
| Çok koyu piksel (L\* < 15)         | Figürün %0,4–0,5'i: saç, kaş, göz                                 |
| Gövdede düz renkli piksel          | %54–63                                                            |
| Gövdede degradeli piksel           | %26–29                                                            |
| Ana giysi doygunluğu               | C\* 65–80 (kırmızı 76–80, yeşil 79, altın 80)                     |
| Ten                                | L\* 83–85, C\* 34–37, düz                                         |
| Kumaş degradesinin farkı           | ΔL\* 3–12; örnek: kırmızı `#BA0101` → `#871212`                    |
| Beyaz kumaş ve metal degradesi     | Güçlü: beyaz `#FFFFFF` ↔ `#999999`; kılıç iki ton, keskin bölünmüş |
| Degrade durağı ve yönü             | 2 durak; yatay ya da dikey                                        |
| Kenarlardaki eğri oranı            | Yaklaşık %50; eğriler sivri köşelerde buluşur                     |
| Baş kütlesi / boy (başlık dahil)   | %14                                                               |
| Omuz genişliği / baş genişliği     | 3,5                                                               |
| Ön kol ve yumruk genişliği / yüz   | Yaklaşık 1,0                                                      |
| Komşu malzeme farkı                | Ten–kırmızı ΔL\* ≈ 50; beyaz şerit–kırmızı ≈ 69; siyah saç–yüz ≈ 85 |
| Bir kahramandaki renk sayısı       | 18–25; bir parçada 2–3 ton                                        |
| Ayrıntı öğesi                      | Yaklaşık 14; baş, bilek-kemer ve silah olmak üzere üç kümede      |

### Ortam

- **Gök:** düz ya da çok hafif dikey degradeli kobalt mavisi (`#00359B` → `#0057BD`). Bulut yok.
  Büyük, radyal bir güneş ya da ay parıltısı var.
- **Huş:** taç 2–3 yeşil tonda, düz ve tümsekli lekeler; gövde beyaz, üstünde siyah kısa çizgiler.
- **Çam:** iç içe, dalgalı kenarlı, koyu yeşil katmanlar.
- **Zemin:** ufuk çizgisinde sivri ve uzun ot yaprakları; zeminde birkaç tonlu büyük lekeler.
- **Harita:** deniz `#003366` → `#01597E`; kara yeşilden zeytine dikey degrade; kıyıda sarı bir
  "kalınlık" şeridi.

### Arayüz

| Öğe                  | Görünüş                                                                          |
| -------------------- | -------------------------------------------------------------------------------- |
| Parşömen             | `#AD936B` → `#CCBF91` → `#EBE1D8`                                                |
| Altın pervaz         | Silindir degrade `#745425` → `#D5B32B` → `#745425`; içte ince siyah çizgi        |
| Kırmızı düğme ve ok  | `#BA0101` → `#871212`                                                            |
| Savaş paneli         | Koyu yeşil zemin; koyu gri, kabartmalı yuvalar                                   |
| Parşömen kart        | Bkz. "Arayüz" bölümü; oyunun sahibinin en sevdiği öğe                            |

## Palet

**Kural:** Çizimlerde **yalnızca** bu renkler kullanılır.

- Renklerin hepsi esin kaynağından ölçüldü.
- Paletin kaynağı `tools/art/palet.txt` dosyasıdır; bu tablo onun kopyasıdır.
- Otomatik denetim, bu tabloda paletin bütün renklerinin bulunduğunu da denetler.
- Yeni renk gerekirse önce referanstan ölçülür, sonra iki yere birden eklenir.
- Saydamlık serbesttir. Yarı saydam şekillerde de renk paletten seçilir.

#### Ten

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| ten | `#FFCC99` | ten-gölge | `#F3B58C` | ten-derin | `#C69271` |
| ten-açık | `#FED8B4` | ten-buğday | `#F3C98B` | ten-pembe | `#F5C4A3` |
| ten-sarı | `#F4D0A0` | ten-sarı-gölge | `#F2BE8C` | dudak | `#CC3300` |
| dudak-açık | `#EF9C65` | dudak-pembe | `#F1A674` | ağız-koyu | `#881111` |
| ağız | `#660000` |  |  |  |  |

#### Saç ve sakal

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| saç-siyah | `#000000` | saç-siyah-ışık | `#333333` | saç-sarı | `#FEFDBC` |
| saç-sarı-gölge | `#FEDE5F` | saç-kızıl | `#CC3300` | saç-kızıl-gölge | `#A73403` |
| saç-ak | `#E6E6E6` | saç-ak-gölge | `#CCCCCC` |  |  |

#### Kırmızı kumaş

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| kırmızı-parlak | `#FF0000` | kırmızı | `#CC0000` | kırmızı-koyu | `#990000` |
| kırmızı-degrade-açık | `#BA0101` | kırmızı-degrade-koyu | `#871212` | kırmızı-gölge | `#57150F` |
| kırmızı-soluk | `#B92E2E` |  |  |  |  |

#### Beyaz, gri, siyah kumaş

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| beyaz | `#FFFFFF` | beyaz-gölge | `#E6E6E6` | gri-açık | `#CCCCCC` |
| gri | `#999999` | gri-koyu | `#666666` | kömür-açık | `#4D4D4D` |
| kömür | `#333333` | kömür-koyu | `#222222` | siyah-ışık | `#1A1A1A` |
| siyah | `#000000` |  |  |  |  |

#### Yeşil ve zeytin kumaş

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| yeşil-parlak | `#00CC00` | yeşil | `#009900` | yeşil-soluk | `#669966` |
| yeşil-soluk-gölge | `#558055` | zeytin | `#77773C` | zeytin-koyu | `#5A5A2E` |
| zeytin-derin | `#505027` | zeytin-sarı | `#E0CB16` | zeytin-açık | `#B2B27D` |
| zeytin-gri | `#9C8D52` | zeytin-sarı-gölge | `#C2B012` |  |  |

#### Çelik ve demir

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| çelik-parlak | `#D0D5D9` | çelik-lavanta | `#CCCCE6` | çelik-açık | `#B2B2B2` |
| çelik-mavi | `#A1A8AB` | çelik-gölge | `#778A9A` | çelik-koyu | `#646579` |
| çelik-derin | `#353642` |  |  |  |  |

#### Mavi

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| mavi | `#003399` | mavi-koyu | `#003366` | mavi-derin | `#000099` |
| mavi-soluk | `#395593` | mavi-açık | `#89ADFE` | lacivert-zemin | `#253C56` |

#### Altın ve sarı

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| altın | `#FFCC00` | altın-açık | `#FEDE5F` | altın-parlama | `#FEEDAB` |
| altın-gölge | `#C6A04A` | altın-koyu | `#A88535` | altın-derin | `#745425` |
| altın-çerçeve | `#D5B32B` | turuncu | `#FF9900` | altın-sarı | `#F3C81D` |
| altın-hardal | `#D6AC07` | altın-çizme | `#D0A706` |  |  |

#### Kahve, deri, ahşap

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| deri-açık | `#996633` | deri | `#795128` | deri-gölge | `#6C4824` |
| kahve | `#664422` | kahve-gölge | `#604020` | kahve-koyu | `#4D331A` |
| kahve-derin | `#392613` | kahve-siyah | `#2D1E0F` | ahşap-degrade-koyu | `#57390F` |
| ahşap-degrade-açık | `#A06A1B` | çizme-degrade-koyu | `#321E01` | çizme-degrade-açık | `#985B01` |
| sap | `#996600` | sap-koyu | `#4A2C01` |  |  |

#### Gök (gündüz ve gece)

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| gök-tepe | `#00359B` | gök | `#0045AB` | gök-ufuk | `#0057BD` |
| gece-tepe | `#001122` | gece | `#0D1D2D` | gece-ufuk | `#35567B` |
| ay-ışığı | `#C3CDD8` | ay | `#EBEEF2` |  |  |

#### Yaprak, çimen

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| yaprak-parlak | `#39DE10` | yaprak-açık | `#68B968` | yaprak | `#4DA94D` |
| yaprak-canlı | `#009900` | yaprak-koyu | `#14510D` | yaprak-derin | `#0D3309` |
| çam-koyu | `#003300` | çam | `#006600` | çam-açık | `#336633` |
| çam-ışık | `#339900` | çimen-açık | `#AFD3AB` | çimen-soluk | `#85BC7E` |
| çimen-gri | `#99BB9F` | gövde-kızıl | `#651F01` | gövde-koyu | `#3B3831` |
| gövde-gri | `#5B5346` |  |  |  |  |

#### Zemin ve kuru ot

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| zemin-açık | `#538548` | zemin | `#4C8F40` | zemin-koyu | `#307439` |
| zemin-derin | `#417336` | kuru-ot | `#9DA139` | kuru-ot-koyu | `#9B8528` |
| toprak | `#A08639` | toprak-koyu | `#867A23` |  |  |

#### Su ve harita

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| deniz-koyu | `#003366` | deniz | `#01597E` | deniz-açık | `#0B828E` |
| kara-koyu | `#1C8233` | kara | `#339933` | kara-açık | `#62AF23` |
| kara-sarı | `#82B013` | kıyı | `#C4C41A` | kıyı-koyu | `#B5B517` |

#### Taş ve yapı

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| taş-gri | `#5E5E5E` | taş-yeşil | `#4D7574` | badana | `#FFFFCC` |
| badana-sarı | `#EBDF78` | badana-açık | `#F1ECC0` | kiremit | `#831F1F` |
| kiremit-koyu | `#691E18` |  |  |  |  |

#### Arayüz: parşömen, çerçeve, düğme

| Ad | Renk | Ad | Renk | Ad | Renk |
| --- | --- | --- | --- | --- | --- |
| parşömen-koyu | `#AD936B` | parşömen | `#CCBF91` | parşömen-açık | `#EBE1D8` |
| parşömen-kenar | `#8F7145` | parşömen-mürekkep | `#453621` | parşömen-derin | `#221B11` |
| parşömen-kart | `#BCA97E` | parşömen-rulo | `#4D3F2B` | altın-rakam | `#E1CC7A` |
| altın-ışıltı | `#FFCC33` | yuva-gri | `#5F5F5F` | yuva-siyah | `#050505` |
| düğme-kırmızı-odak | `#CF5A5A` | düğme-kırmızı-koyu | `#A20000` | panel-yeşil-koyu | `#042607` |
| panel-yeşil | `#446130` | panel-yeşil-açık | `#54773C` | panel-yeşil-derin | `#07450D` |

### Bölge renkleri

Her bölge, paletin içinden kendi baskın renklerini seçer. Bir ekran görüntüsünden hangi bölgede
olunduğu anlaşılabilmelidir.

| Bölge              | Baskın renkler                                                            | Hava                               |
| ------------------ | ------------------------------------------------------------------------- | ---------------------------------- |
| Bozkır Beylikleri  | kuru-ot, toprak, mavi, kırmızı, altın                                     | Geniş, açık gök, uzun ufuk         |
| Kıyı Kentleri      | badana, kiremit, deniz-açık, zeytin                                       | Parlak, beyaz ışık, deniz meltemi  |
| Dağ Kaleleri       | taş-gri, taş-yeşil, çam-koyu, çelik                                       | Serin, keskin gölgeler, yükseklik  |
| Orman Sınırı       | çam, yaprak-koyu, yaprak-açık, ahşap                                      | Loş, katman katman ağaç            |
| Kuzey Akıncıları   | beyaz, çelik-mavi, mavi-koyu, gövde-kızıl                                 | Soğuk, alçak güneş, uzun gölgeler  |
| Kum Yolları        | badana-sarı, turuncu, toprak, yaprak, mavi                                | Sıcak, beyaza yakın ufuk           |

### Gün saati

Gün saati, katmanların renklerine çarpan ve eklenen bir renk dönüşümüyle verilir. Bu, Flash'taki
renk dönüşümünün karşılığıdır. Çizimler gündüz renkleriyle yapılır; saat ayarını motor yapar.

| Saat    | Işık                           | Gök                                  |
| ------- | ------------------------------ | ------------------------------------ |
| Sabah   | Altın sarısı                   | Ufuk sıcak                           |
| Öğle    | Nötr, parlak                   | Kobalt                               |
| Akşam   | Turuncu                        | Ufuk turuncu, tepe lacivert          |
| Gece    | Mavi ay ışığı                  | Gece paleti, ay parıltısı            |

**Kural:** Saat geçişleri yavaştır, en az birkaç saniye sürer. Ani tam ekran renk değişimi yoktur.

## Kontur

**Kural:** Karakterde de ortamda da **dış hat yoktur** (`stroke` kullanılmaz). Parçalar birbirinden
renk ve açıklık farkıyla ayrılır.

- **İnce çizgi istisnası:** yalnızca doğası çizgi olan şeylerde kullanılır: yay kirişi, ip, dizgin.
  - Kalınlığı en fazla 1,5 birimdir.
  - Rengi altındaki renkten ΔL\* 20–30 koyudur.
- **Komşu parçaların ayrımı:** iki parça arasında ΔL\* ≥ 15 olur. Bu sağlanamıyorsa renk tonları en
  az 40° farklı ve ΔL\* ≥ 8 olur.
- **Aynı renk üst üste binerse** (ör. kol kaftanın önünde): arkadaki parçaya, öndekinin kenarı boyunca
  keskin kenarlı bir temas gölgesi konur.
  - Genişliği 3–6 birimdir.
  - Bir ton koyudur (ΔL\* 8–12).
- **Figürün kenarı:** figür ile hemen arkasındaki zemin arasında ortalama ΔL\* ≥ 20 olur.
- **Çok koyu alanlar:** L\* < 15 olan alan figürün en fazla %3'ü olur (saç, kaş, göz bebeği).
- **Arayüz istisnası:** parşömenin ve tomarın kenarında 2–4 piksellik koyu kenar serbesttir.

## Ton ve gölge

**Kural:** Hacim, keskin kenarlı **ayrı bir gölge şekliyle** verilir. Degrade yalnızca yardımcıdır;
gölge şeklinin yerine geçmez.

**Kural:** Işık sol üstten gelir. Aydınlık yüzler sola ve yukarıya, gölgeler sağa ve aşağıya bakar.
Esin kaynağında ışık yönü tutarsızdır; bizde bu düzeltilir.

| Malzeme                 | Ana renk                 | Gölge şekli (keskin kenarlı)                  | Işık                       | Degrade                         |
| ----------------------- | ------------------------ | --------------------------------------------- | -------------------------- | ------------------------------- |
| Açık ten                | L\* 80–86, C\* 30–38     | En fazla 2 şekil (çene altı, burun), ΔL\* 5–8 | Yok                        | **Yok**                         |
| Esmer ten               | L\* 50–65                | ΔL\* 6–10                                     | Yok                        | **Yok**                         |
| Boyalı kumaş            | C\* ≥ 60                 | 1 şekil, ΔL\* 8–14, parçanın %20–35'i         | İsteğe bağlı, ΔL\* +6–10   | 2 durak, ΔL\* 3–10              |
| Beyaz kumaş             | L\* ≥ 90                 | 1 şekil, gri tarafa                           | —                          | 2 durak, beyaz ↔ gri, güçlü     |
| Şerit, süs, kol ağzı    | Ana renkle ΔL\* ≥ 35 ya da karşıt renk | —                               | —                          | —                               |
| Çelik                   | L\* 60–70                | Ortadan keskin bölünme, ΔL\* 20–35            | 1 parlama, L\* ≥ 90        | 3 durak, silindir               |
| Altın, pirinç           | C\* 70–80                | ΔL\* 15–20                                    | Nokta parlama              | 2–3 durak                       |
| Deri, çizme             | L\* 30–45                | ΔL\* 10–12                                    | —                          | Yatay silindir, ΔL\* 8–12       |
| Saç                     | Düz; koyu saçta L\* 6–15 | —                                             | 1–2 sivri tutam, ΔL\* +12–20 | Yok                          |

- **Renk sayısı:** bir kahramanda 18–28 ayrı renk; bir parçada en fazla 3 ton (ana, gölge, ışık ya da
  şerit).
- **Düz renk payı:** figürde düz renkli alan en az %55, degradeli alan en fazla %30–35 olur.
- **Savaş kuklası:** büyük resimlerden daha sadedir. Yalnızca 2 düz ton kullanılır; degrade yalnızca
  metalde olabilir.

## Degrade

- **Kural:** 2 durak kullanılır. 3 durak yalnızca metal ve silindir parçalarda (pervaz, kılıç, sütun)
  kullanılır. 4 ve daha fazla durak yasaktır.
- **Kural:** Doğrusal degrade yatay ya da dikeydir; eksenden en fazla 15° sapar.
- **Kural:** Bir karakterde degradeli şekillerin oranı en fazla %35'tir.
- **Kural:** Degradeler sRGB uzayında karışır. Uçlarda son renk devam eder ("pad").
- Duraklar arasında doygunluk farkı en fazla C\* 15'tir. Açık uç griye, koyu uç mora gitmez.
- Radyal degrade ışık ve gölge içindir: güneş ve ay parıltısı, parşömenin aydınlık ortası, yuvanın
  içi, büyü parıltısı. Parıltılar saydamlığa doğru söner.
- Gök ve zemin, büyük ve 2 duraklı dikey degradelerdir.

## Renk

| Kullanım                          | Doygunluk                                       |
| --------------------------------- | ----------------------------------------------- |
| Kırmızı giysi ve sancak           | C\* 65–80                                       |
| Yeşil giysi                       | C\* 60–80                                       |
| Mavi giysi                        | C\* 50–65                                       |
| Sarı ve altın                     | C\* 65–80                                       |
| Toprak tonları (zeytin, kahve, okra) | C\* 30–45; canlı renkleri dengeler           |
| Nötr metal                        | C\* ≤ 12                                        |

- **Gölge rengi:** ana rengin tonundan en fazla ±10° sapar; doygunluğu en fazla %25 düşer.
- **Renk dağılımı:**

  | Rol          | Figür yüzeyindeki payı | Örnek                |
  | ------------ | ---------------------- | -------------------- |
  | Baskın renk  | %35–50                 | Kaftan               |
  | İkincil renk | %15–25                 | Kuşak, çizme         |
  | Vurgu rengi  | En fazla %8            | Altın ya da beyaz şerit |

- **Yüz:** yüz figürün en açık yerlerinden biridir; göz önce yüze gider.

## Şekil, köşe ve eğri

- **Kural:** Şekiller eğridir, kenarları keskindir. Karakter yollarında eğri parçaların oranı
  **%50–65** olur.
  - Otomatik denetim %40–75 dışını reddeder.
  - %40'ın altı çokgen ve "low-poly" görünüş demektir; %75'in üstü yuvarlak ve yumuşak.
- **Kural:** Her ana şekilde en az bir **sivri köşe** bulunur. Sivri köşe, iki eğrinin teğet olmadan,
  kırılarak birleştiği yerdir.
- **Sivri uçlar:** kol ağzı, etek köşesi, çizme burnu, saç tutamı, sakal, tüy, yaprak, ot.
- **Uzuvlar:** bir kenar düze yakın, öbür kenar şişkin çizilir. Kapsül şekil yasaktır.
  - Pazı, ön kol ve baldır şişkindir.
  - Bilek, ön kolun en geniş yerinin %55–65'i kadar daralır.
  - Dirsek, diz ve ayak bileği de daralır.

## Karakterler

### Oranlar

Baş = 64 birim. Başlık hariç; kafatası ve çeneden ibarettir.

| Ölçü                                     | Kahraman                         | Asker                 | Esinde ölçülen |
| ---------------------------------------- | -------------------------------- | --------------------- | -------------- |
| Boy                                      | 7–7,5 baş                        | 6,8–7,2 baş           | 7,1–7,6        |
| Baş genişliği                            | Baş boyunun 0,62–0,7'si          | Aynı                  | 0,6            |
| Baş kütlesi (başlık, saç, sakal dahil)   | Boyun en fazla %18'i             | Boyun en fazla %18'i  | %14            |
| Omuz genişliği                           | Baş kütlesi genişliğinin 3,2–3,6 katı | 2,8–3,2 katı     | 3,5            |
| Omuz / bel                               | 1,4–1,6                          | 1,3–1,45              | —              |
| Boyun                                    | Baş genişliğinin en az %70'i     | Aynı                  | Kalın          |
| Ön kolun en geniş yeri                   | Yüz genişliğinin 0,8–1,0'ı       | 0,7–0,85              | ~1,0           |
| Yumruk                                   | Yüz genişliğinin 0,85–1,0'ı      | 0,75–0,9              | ~1,0           |
| Uyluk                                    | 0,65–0,8 baş                     | 0,6–0,7 baş           | 0,6–0,77       |
| Ayak ya da çizme                         | 1,15–1,3 baş; çizme ağzı ~0,6 baş | 1,1–1,2 baş          | —              |
| Bacak                                    | Boyun %47–50'si                  | Aynı                  | —              |

Sevimliliği küçük baş, gerçekçiliği iri kol ve el engeller.

### Yüz

64 birimlik bir baş için:

| Öğe    | Kural                                                                                   |
| ------ | --------------------------------------------------------------------------------------- |
| Göz    | Badem biçiminde, 8–10 birim genişliğinde. Göz akı beyaz (L\* ≥ 92). İris 3–4 birim, siyah ya da çok koyu, üst kapağa değer |
| Kaş    | 3–5 birim kalınlıkta, koyu. Kararlı ifade için buruna doğru 10–25° aşağı iner            |
| Burun  | Tenden bir ton koyu tek bir gölge şekli (ΔL\* 5–8) ya da profil kenarı. Boyu 0,25–0,32 baş |
| Ağız   | Küçük bir dudak şekli: `dudak-açık`, `dudak-pembe` ya da `dudak`. Genişliği 0,22–0,3 baş |
| Çene   | Köşeli; genişliği baş genişliğinin en az %60'ı                                          |
| Bakış  | Seçim ekranında yüz 3/4 cepheden, bakış izleyiciye. Savaş kuklasında 3/4 ya da profil   |
| İmza   | Her karakterde tek bir ayırt edici yüz öğesi: bıyık biçimi, yara izi, kanca burun, örgü |

**Kural:** Yüz gerçekçi değildir. Elmacık, kırışık ya da dudak çizgisi işlenmez. Gözü kapalı yüz
yalnızca uyku ve ölüm animasyonunda kullanılır.

### Duruş ve siluet

- **Çaprazlar:** her duruşta 20–50° açılı en az iki belirgin çapraz olur (silah, kol, bacak).
- **Silah:** gövdeye paralel durmaz; arada en az 15° açı olur.
- **Kollar:** kol ile gövde arasında en az bir yerde 0,15 baştan geniş bir boşluk kalır.
- **Ayaklar:** seçim ekranı duruşunda iki ayak arası en az 1 baştır (A duruşu). Göğüs dışarıdadır.
- **Kural (siluet testi):** figür 120 piksel yükseklikte tek renk çizildiğinde birlik türü tanınır.
  En az 3 çıkıntı görünür: başlık, silah, kalkan ya da pelerin.

### Ayrıntı

- **Sayı:** kahramanda 12–18, askerde 6–10 ayrıntı öğesi olur.
  - Kemer tokası, bilezik, sadak, tüy, nakış şeridi birer öğedir.
- **Kümelenme:** öğelerin en az %70'i üç kümede toplanır:
  - baş ve yüz;
  - bel ve eller;
  - silah ve kalkan.
- **Sakin alan:** figür alanının %50–60'ı düz, sakin yüzey kalır (göğüs, etek, uyluk).
- **Karşıtlık:** odak ayrıntısında komşuyla ΔL\* ≥ 30, ikincil ayrıntıda ΔL\* 10–20 olur.
- **Kural:** Ayrıntı çizgiyle değil, **şekille** yapılır.
  - Kıvrım gerekiyorsa koyu bir bant şekli kullanılır.
  - Kemer bir şerittir.
  - Zırh iki tonlu büyük plakalardır.

### Parçalı kukla

Karakterler ayrı parçalardan kurulur. Parçalar kemiklere bağlıdır ve döndürülerek canlandırılır.

| Parça                            | Not                                                      |
| -------------------------------- | -------------------------------------------------------- |
| baş, saç, yüz ayrıntısı          | Yüz parçaları değiştirilebilir (kaş, burun, ağız, sakal) |
| boyun, gövde, kalça              | Zırh gövdenin üstüne giyilir                             |
| üst kol, ön kol, el (×2)         | Arka kol bir ton koyu çizilir                            |
| üst bacak, alt bacak, ayak (×2)  | Arka bacak bir ton koyu çizilir                          |
| silah, kalkan, başlık, pelerin   | Donanım; değişince görünüş değişir                       |

- **Kural:** Eklem yerlerinde parçalar birbirinin altına girer; bindirme payı en az 0,2 baştır.
  Parça döndüğünde boşluk görünmez.
- **Kural:** Her parçanın SVG grubu İngilizce adla işaretlenir: `head`, `torso`, `arm-upper-front`.
- Arkadaki kol ve bacak, öndekinden bir ton koyudur; derinlik böyle verilir.

### Her asker bir kişidir

Aynı birlikten iki asker yan yana durduğunda farkları görülür:

- **Yüz kataloğu:** en az 4 kaş, 4 bıyık ve sakal, 3 burun; ten tonu ve saç rengi.
- **Boy ve omuz:** boy ölçeği 0,94–1,06; omuz genişliği ölçeği 0,92–1,10.
- **Donanım:** küçük farklar; kalkanlarda boyalı damga motifleri.
- **Yaş ve ifade:** genç acemi, yorgun gazi.
- **Gaziler:** yara izi, nişan, farklı pelerin ya da sancak.

## Ölçek ve birimler

Bütün çizimler SVG olarak tutulur. Bir SVG biriminin ekranda kaç piksel olduğu çizimin türüne göre
sabittir:

| Tür              | Çizim alanı                                         | Ekrana ölçek                                      |
| ---------------- | --------------------------------------------------- | ------------------------------------------------- |
| Ekran ve arayüz  | 1 birim = 1 mantıksal piksel (1920×1080 ekran)      | 1                                                 |
| Manzara katmanı  | 1 birim = 1 mantıksal piksel; ekrandan geniş olabilir | Paralaksa göre kayar                           |
| Karakter         | Baş 64 birim; boy 7–7,5 baş (450–480 birim)         | Savaşta ~0,27 (≈120 piksel), seçim ekranında 1–1,4 |
| Simge            | 128×128 birim                                       | Arayüzde 48–96 piksel                             |

Mantıksal ekran 1920×1080'dir; motor bunu pencere boyutuna ölçekler. Çizimler vektör olduğu için
her ölçekte, 4K'da da keskindir.

## Manzara

Savaş alanları ve şehir sahneleri katmanlardan kurulur. Katmanlar kamera kayarken farklı hızlarda
kayar (paralaks).

| Sıra | Katman           | Paralaks | Açıklık (gündüz)  | İçerik                                         |
| ---- | ---------------- | -------- | ----------------- | ---------------------------------------------- |
| 1    | Gök              | 0–0,05   | L\* 27–40         | 2 duraklı dikey kobalt degradesi, güneş parıltısı |
| 2    | Uzak             | 0,1–0,2  | L\* 55–70         | Tepe ve dağ siluetleri                          |
| 3    | Orta             | 0,3–0,4  | L\* 15–35 (koyu)  | Koyu ağaç dizisi                                |
| 4    | Yakın arka plan  | 0,6–0,8  | L\* 40–70         | Ağaçlar, yapılar; koyu dizinin önünde parlak    |
| 5    | Savaş zemini     | 1        | L\* 45–60         | Büyük lekeli çayır, yol; oyun alanı             |
| 6    | Ön plan          | 1,2–1,4  | L\* 20–35         | Koyu ot öbekleri, çalılar (yalnızca kenarlarda) |

- **Kural:** Komşu katmanlar arasında ΔL\* ≥ 10 olur. Uzaklık soluklaştırarak değil, **koyu
  siluetle** verilir. Gök rengine karışım uzak katmanda en fazla %25–35'tir.
- **Kural:** Bir katmanda şekillerin en fazla %10'u yarı saydamdır (siyah gölge ve beyaz ışık hariç).
  Lekeler üst üste bindirilmiş yarı saydam şekiller değil, düz şekillerdir.
- **Ağaç:**
  - 3–4 düz yeşil kullanılır; tonlar arasındaki her adım ΔL\* 8–14'tür.
  - Yaprak kümeleri tümsekli ya da sivri loblu, düz lekelerdir.
  - Dallar görünür; gövde 2 tonludur.
  - Bir ağaç 8–20 şekilden oluşur.
  - Tek top ağaç ve lolipop selvi yasaktır.
- **Ot:**
  - Ufuk çizgisinde sivri, alev biçimli uzun bir ot saçağı vardır (2 sarımsı yeşil).
  - Bir ot öbeği 5–9 sivri yapraktır.
- **Zemin:** az sayıda, büyük ve üç tonlu lekeler vardır. Yol doygun okradır ve kenarında koyu bir
  bant bulunur.
- **Küçük serpinti:** çakıl ve tek ot gibi serpintiler kümeler hâlinde olur; ekranda en fazla 15 tane
  bulunur.
- **Gölge:** karakterlerin ve ağaçların altında düz, yarı saydam siyah bir elips gölge vardır.
- **Kural:** Aynı katman takımı iki savaşta aynı dizilimle kullanılmaz.

## Arayüz

Arayüz ağır, metalik ve karşıtlığı yüksektir. Oyunun dünyasından yapılmış nesneler gibi görünür:
parşömen, altın, ahşap, mühür, kalkan.

### Parşömen kart (sahibin en sevdiği öğe)

Esin kaynağının savaş panelindeki parşömen kartlar ve tomar düğmeler oyunun sahibinin en sevdiği
arayüz öğeleridir. **Tarzları** bizim arayüzümüzün temelidir. İçlerindeki simgeler (haçlar, kanlı
kılıç) alınmaz; simgeler bizim dünyamıza göre baştan tasarlanır.

| Öğe            | Görünüş                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------- |
| Panel          | Koyu yeşil zemin (`panel-yeşil-derin` `#07450D`, `panel-yeşil-koyu` `#042607`)           |
| Yuva           | Koyu, kabartmalı çerçeve: dıştan içe `yuva-gri` `#5F5F5F` → `yuva-siyah` `#050505` silindir degradesi. İçi koyu yeşil, ortası hafif açık (radyal) |
| Kart           | Dik parşömen: üstten alta `parşömen-kart` `#BCA97E` → `parşömen-açık` `#EBE1D8`. Sol ve sağ kenar hafif S biçiminde dalgalıdır. Üst kenar rulo kıvrımlıdır; sol üstte `parşömen-rulo` `#4D3F2B` küçük bir kıvrım ucu vardır. Alt kenarın altında ince koyu bir rulo gölgesi bulunur |
| Simge          | Kartın ortasında, kartın %60–75'ini dolduran iri bir şekildir. Açık iç dolgunun çevresinde beyaz ya da altın bir kenar ve 2–3 sıra **ışıltı çizgisi** bulunur: şeklin dışına doğru aralıklı, kesik kesik eş biçimli çizgiler. Simge "parlıyor" gibi durur |
| Sayı           | Sağ altta, `altın-rakam` `#E1CC7A` |

### Tomar düğme

İki ucu rulo kıvrımlı, yatay bir parşömen tomarıdır.

- Üstünde koyu mürekkeple (`parşömen-mürekkep`) çizilmiş küçük bir simge ve düğmenin adı bulunur:
  "Beceriler", "Envanter" gibi.
- Simge tek renkli ve kalındır: yumruk, kılıç, kalkan.

### Öbür öğeler

| Öğe              | Görünüş                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------- |
| Pervaz (çerçeve) | 1080p'de 14–20 piksel kalınlıkta. 3 duraklı silindir degrade (`altın-derin` → `altın-çerçeve` → `altın-derin`, ΔL\* 35–50). İçte 2–3 piksel koyu çizgi; köşelerde metal köşebent |
| Pencere zemini   | Parşömen, radyal degrade: merkez L\* 86–90 (`parşömen-açık`), kenar L\* 65–72 (`parşömen-koyu`) |
| Başlık           | Kurdele: ön yüzü kırmızı degrade; kıvrımın arka yüzü ΔL\* 15–20 koyu (`kırmızı-gölge`); uçları çatallı |
| Onay düğmesi     | Kırmızı mühür: dalgalı kenarlı, kırmızı degradeli                                              |
| Ok düğmesi       | Elmas ya da üçgen biçimli, kırmızı degradeli                                                   |
| Geri düğmesi     | Metal kenarlı kalkan                                                                           |
| Bilgi kutusu     | Kıvrık uçlu parşömen tomarı; ad, özellikler (küçük simgelerle) ve fiyat (sikke simgesiyle)     |
| Konuşma          | Konuşanın portresi ve parşömen. **Düz beyaz baloncuk yok**                                     |

**Kural:** Simgeler kontursuzdur. Yuvalarının %70–85'ini doldururlar. 3 ton ve 1 parlama kullanırlar;
doygunlukları C\* ≥ 55'tir. Bir ekranda tek simge tarzı kullanılır: renkli simge ya da mürekkep
çizimi simge. İkisi aynı satırda karışmaz.

**Davranış:**

- **Üstüne gelince:** yumuşak altın parıltı 0,15 saniyede belirir.
- **Basınca:** öğe 2 piksel aşağı iner ve bir ton koyulaşır.
- **Klavyeyle seçilen öğe:** çevresinde altın odak çerçevesi olur.

### Yazı

| Kullanım           | Yazı tipi        | Boyut (1080p) |
| ------------------ | ---------------- | ------------- |
| Oyunun adı         | Alegreya SC Bold | 96–128        |
| Başlık             | Alegreya SC      | 40–56         |
| Düz metin          | Alegreya         | 26            |
| Küçük metin, sayı  | Alegreya Sans    | 20–22         |

- Satır aralığı, yazı boyunun 1,3 katıdır.
- Parşömen üstündeki yazının rengi `parşömen-mürekkep` `#453621`'dir. Kırmızı ve koyu zemin üstündeki
  yazı `parşömen-açık` `#EBE1D8` olur.
- **Kural:** Türkçe büyük harf dönüşümü Türkçe kurallarla yapılır (i → İ, ı → I).

## Dünya haritası

Elle çizilmiş, yaşayan bir haritadır.

- **Deniz:** `deniz-koyu` → `deniz` degradesi. Kıyıya yakın açık bir şerit ve dalga kıvrımları vardır.
- **Kara:** dikey yeşil → zeytin degradesiyle büyük lekelerdir. Kıyı boyunca `kıyı` renginde bir
  "kalınlık" şeridi vardır; kara kâğıttan kesilip yapıştırılmış gibi durur.
- **Şehirler:** kültürüne göre farklı, 3/4 kuşbakışı küçük simgelerdir. Aydınlık ve gölge yüzleri
  belirgindir. Her şehrin kendine özgü bir ayrıntısı vardır: liman, kule, kubbe.
- **Süsler:** dağlar, ağaç kümeleri, vaha, yol izleri. Kenarda pusula gülü ve bordür bulunur.
- **Mevsim:** haritaya yansır. Kışın kuzey beyazlaşır.

## Şehirler

**Kural:** İki şehir aynı yerleşimle çizilmez. Her şehrin kendine ait şunları vardır:

- manzara: dağ yamacı, liman, vaha ya da nehir adası;
- mimari;
- özel bir bina.

Bir şehir ekran görüntüsünden tanınabilmelidir.

## Hareket ve efektler

- Kukla animasyonu yumuşak geçişlidir: hareket yavaşlayarak başlar ve biter. Vuruşlarda kısa bir ön
  hazırlık ve vuruş anında 2–3 karelik duraklama olur.
- Efektler (kıvılcım, toz, kan) küçük ve yereldir; vektör parçacıklarla çizilir.

**Kural (görsel güvenlik):**

- Hiçbir efekt saniyede 3'ten fazla parlama üretmez.
- Ani tam ekran beyaz ya da kırmızı geçiş yoktur. Ekranın geneline yayılan renk değişimleri en az 0,5
  saniye sürer.
- Doygun kırmızıyla yanıp sönen efekt yoktur.

## SVG yazım kuralları

Motorun okuduğu SVG alt kümesi:

- **Kullanılır:** `path`, `rect`, `circle`, `ellipse`, `polygon`, `g`, `transform`, `fill`, `opacity`,
  `fill-opacity`, `linearGradient`, `radialGradient`, `stop`.
- **Kullanılmaz:** filtre (bulanıklaştırma, gölge), maske, kırpma, desen, gömülü resim, SVG içinde
  yazı, kesikli çizgi. Yazılar motorda çizilir.
- Grup saydamlığı (`<g opacity>`) yerine her şeklin kendi saydamlığı kullanılır.
- Kimlikler (`id`) İngilizce ve küçük harflidir.
- Renkler yalnızca paletten seçilir.

**Dosya düzeni:** Otomatik denetim çizimin türünü klasörden anlar.

| Klasör adı    | Tür                                              |
| ------------- | ------------------------------------------------ |
| `characters/` | Karakterler ve hayvanlar                         |
| `landscape/`  | Manzara katmanları                               |
| `ui/`         | Arayüz ve simgeler                               |

Örnek: `content/art/samples/characters/hero.svg`.

Çizimler elle değil, `tools/art/` içindeki Python betikleriyle üretilir. Betikler renkleri
`palet.py` üzerinden adıyla ister (`r("kırmızı")`); paletin dışında renk yazılamaz.

## Otomatik denetim

`cargo test -p game --test art_rules` her SVG'yi motorun okuduğu biçimde yükler ve şunları denetler:

| Denetim                                         | Sınır                                  |
| ----------------------------------------------- | -------------------------------------- |
| Bütün renkler paletten mi                       | Hepsi                                  |
| Degrade durak sayısı                            | En fazla 3                             |
| Doğrusal degradenin eksenden sapması            | En fazla 15°                           |
| Karakterde kontur                               | Yok (en fazla 1,5 birimlik ince çizgi) |
| Manzarada kontur                                | Yok                                    |
| Karakterde degradeli şekil oranı                | En fazla %35                           |
| Karakter yollarında eğri parça oranı            | %40–75 (hedef %50–65)                  |
| Manzarada yarı saydam şekil oranı               | En fazla %10 (siyah ve beyaz hariç)    |
| Sahne dosyalarındaki yazı renkleri              | Paletten                               |
| Bu belgede paletin bütün renkleri yazılı mı     | Hepsi                                  |

Denetim CI'da her gönderimde çalışır. Kurala aykırı bir çizim derlemeyi kırmızıya düşürür.

Ölçülerek bakılan ama henüz elle denetlenen kurallar:

- oranlar;
- çok koyu alan payı;
- komşu parça farkı;
- ayrıntı sayısı.

Bunlar her yeni çizimde kalite denetiminde ölçülür.

## Çizim yöntemi

1. **Önce çözümleme:** çizilecek şeyin referansta karşılığı bulunur. Kontur, ton sayısı, yüz, oranlar
   ve renkler bu belgeden okunur.
2. **Renk:** yalnızca palet kullanılır.
3. **Çizim:** önce tek renk siluet, sonra ana renkler, sonra gölge şekilleri, en son ayrıntı kümeleri
   çizilir.
4. **Yan yana karşılaştırma:** çizim aynı ölçekte referansın yanına konur. Farklar madde madde
   listelenir ve düzeltilir.
5. **Bağımsız denetim:** çizimi yapmayan biri, belge ve referans dosyalarının tek tek yollarıyla
   çizimi inceler, puan verir, farkları listeler. Bulgular düzeltilir.

## Kontrol listesi

Her yeni çizim için:

- [ ] Otomatik denetimden geçiyor mu?
- [ ] Yasaklar listesindeki hiçbir şey yok mu?
- [ ] Tek renk siluet olarak tanınıyor mu? En az 3 çıkıntı var mı?
- [ ] Hacim keskin kenarlı gölge şekilleriyle mi verilmiş? Degradeler yalnızca yardımcı mı?
- [ ] Işık sol üstten mi geliyor?
- [ ] Ana renkler canlı mı (C\* 60–80)? Gölgeler aynı renk ailesinde mi?
- [ ] Komşu parçalar arasında yeterli açıklık farkı var mı?
- [ ] Oranlar tabloya uyuyor mu? Baş kütlesi boyun en fazla %18'i mi?
- [ ] Uzuvlar şişkin ve daralan mı? Kapsül uzuv yok mu?
- [ ] Gözler açık mı, bakış izleyiciye mi? Yüzde bir imza öğe var mı?
- [ ] Duruşta en az iki çapraz var mı? Silah gövdeye paralel değil mi?
- [ ] Ayrıntılar üç kümede mi? Sakin alanlar korunmuş mu?
- [ ] Kukla parçalarında bindirme payı var mı?
- [ ] Esin kaynağındaki bir karaktere, simgeye ya da yerleşime benziyor mu? Benziyorsa değiştir.
