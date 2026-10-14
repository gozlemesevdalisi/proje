# Motor

Oyunun çalıştığı altyapının kararları ve yapısı.

## Karar: kendi motorumuz, sağlam kütüphanelerin üstünde

**Karar:** Oyun, **Rust** ile yazılmış kendi motorumuzda çalışır. Motor sıfırdan değil, yıllardır
kullanılan ve sınanmış açık kaynak kütüphanelerin üstüne kurulur: grafik kartıyla konuşmayı, pencereyi,
ses kartını bu kütüphaneler yapar; oyun döngüsü, çizim düzeni, vektör görseller, kukla animasyonu,
arayüz, savaş benzetimi ve kayıt bizimdir.

Seçenekler ve neden bu:

| Seçenek                          | Artısı                                                    | Eksisi                                                                                   |
| -------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Tamamen sıfırdan motor           | Her şey bizim                                             | Yıllar sürer; grafik sürücüsü, ses aygıtı gibi oyuna bir şey katmayan işlere zaman gider |
| Hazır motor (Godot, Unity)       | İlk oynanabilir sürüme hızlı varılır                      | Görsel editör odaklı; motorun sınırları ve güncellemeleri bize dayatılır                 |
| **Kütüphaneler üstüne kendi motorumuz** | Her şey kodda ve denetimimizde; tam istediğimiz görsel tarz; çok hızlı benzetim; tek küçük `.exe` | İlk oynanabilir sürüm hazır motordan biraz geç gelir                                     |

Bu oyun için kendi motorumuzu öne çıkaran nedenler:

- **Görsel tarz**: Flash tarzı vektör çizim ve parçalı kukla animasyonu hazır motorlarda ikinci sınıftır;
  bizde merkezdedir. Her çözünürlükte keskin, kontur ve renkler tam istediğimiz gibi.
- **Kalabalık savaşlar**: yüzlerce asker, moral, arazi ve yapay zekâ; Rust bunu rahatça kaldırır.
- **Belirlenimci benzetim**: savaş kuralları görüntüden tamamen ayrıdır. Aynı başlangıç aynı sonucu
  verir; savaşlar ekransız, saniyede yüzlerce kez oynatılıp denge otomatik sınanır.
- **Her şey metin ve kod**: birlikler, şehirler, görevler, çizimler ve animasyonlar okunabilir metin
  dosyalarıdır. Değişiklikler git'te izlenir, testlerle denetlenir.
- **Uzun ömür**: oyun bir motor şirketinin kararlarına ya da sürüm değişikliklerine bağlı kalmaz.

## Kullanılan kütüphaneler

| İş                     | Kütüphane                   | Lisans             |
| ---------------------- | --------------------------- | ------------------ |
| Pencere ve girdi       | `winit`                     | Apache-2.0         |
| Grafik (DirectX 12/Vulkan) | `wgpu`                  | MIT / Apache-2.0   |
| Vektör şekilleri üçgenlemek | `lyon`                 | MIT / Apache-2.0   |
| SVG okumak             | `usvg`                      | MIT / Apache-2.0   |
| Yazı tipi okumak       | `ttf-parser`                | MIT / Apache-2.0   |
| Matematik              | `glam`                      | MIT / Apache-2.0   |
| Veri dosyaları         | `serde`, `ron`              | MIT / Apache-2.0   |
| Ses                    | `kira` (sonra eklenecek)    | MIT / Apache-2.0   |

Yeni bir kütüphane eklenmeden önce lisansı denetlenir (`cargo deny`). AGPL ve ticari kullanımı
yasaklayan lisanslar kabul edilmez.

## Yapı

```
crates/
  engine/   Oyundan bağımsız motor: pencere, çizim, vektör şekiller, yazı, girdi, zaman, arayüz
  sim/      Oyunun kuralları: savaş benzetimi, ordu, kahraman, dünya. Grafik bilmez; belirlenimci.
  game/     Oyunun kendisi (çalışan program): sim ile engine'i birleştirir, ekranları yönetir
content/    Oyunun verileri: birlikler, silahlar, şehirler, metinler, vektör çizimler, animasyonlar
docs/       Belgeler
```

Kurallar:

- `sim` hiçbir grafik, pencere ya da ses kütüphanesine bağlı değildir. Sabit adımla (saniyede 60)
  ilerler, kendi rastgele sayı üretecini kullanır, kayan nokta sonuçları platformdan bağımsız kalacak
  şekilde yazılır. Aynı tohum ve aynı girdiler her zaman aynı savaşı verir.
- `engine` oyun kuralı bilmez; başka bir oyunda da kullanılabilecek kadar genel kalır.
- Oyun içeriği kodda değil `content/` altındaki veri dosyalarındadır. Ekranda görünen bütün metinler
  Türkçe metin dosyalarındadır; ileride başka dil eklemek yeni bir dosya eklemek demektir.

## Çizim

- Bütün görseller vektördür. SVG dosyaları açılışta okunur, `lyon` ile üçgenlere çevrilir ve grafik
  kartında çizilir. Kenar yumuşatma çok örneklemeyle (MSAA) yapılır.
- Ekran 1920×1080 mantıksal alan üzerinden düzenlenir ve pencereye göre ölçeklenir; vektör olduğu için
  her boyutta keskin kalır.
- Yazılar da yazı tipinin vektör çizgilerinden çizilir; Türkçe harflerin hepsini içeren, lisansı uygun
  yazı tipleri kullanılır.
- Karakterler parçalardan oluşur (baş, gövde, kollar, bacaklar, silah, kalkan); parçalar kemiklere
  bağlıdır ve anahtar karelerle oynatılır. Donanım değişince ilgili parça değişir.

## Sınama

- **Birim testleri**: her modülün yanında (`cargo test`).
- **Benzetim testleri**: belirli savaşlar ekransız oynatılır ve sonuçları denetlenir (kim kazandı,
  kaç kare sürdü, aynı tohum aynı sonucu verdi mi).
- **Görüntü testleri**: sahneler ekransız çizilip resim dosyasına kaydedilir; beklenen resimle
  karşılaştırılır. Böylece bir değişiklik görüntüyü bozarsa testler yakalar.
- **Denge araçları**: iki ordu binlerce kez çarpıştırılır, kazanma oranları raporlanır.

## Dağıtım

- Hedef: Windows 10 ve 11, 64 bit. Grafik: DirectX 12 (yoksa Vulkan).
- Her güncellemede GitHub Actions oyunu Windows'ta derler ve "Test sürümü" Release'ine koyar;
  indirme linki sabittir (README'de).
- Oyun tek bir `.exe` ve yanında `content/` klasörü olarak dağıtılır; kurulum gerektirmez.
  Kayıtlar ve ayarlar kullanıcının `AppData` klasöründe tutulur.
- Oyun internete bağlanmaz; telemetri yoktur.
