# Geliştirme

## Belgeler

- [docs/TASARIM.md](docs/TASARIM.md): oyunun tasarımı
- [docs/SANAT.md](docs/SANAT.md): sanat rehberi; her yeni çizimden önce okunur
- [docs/MOTOR.md](docs/MOTOR.md): motorun kararları ve yapısı
- [docs/YOL_HARITASI.md](docs/YOL_HARITASI.md): aşamalar ve yapılacaklar
- [docs/gunluk/](docs/gunluk/): geliştirme günlüğü; her çalışma gününün sonunda ne yapıldığı,
  durum ve sıradaki adım

## Gerekenler

- Rust: https://rustup.rs (sürüm `rust-toolchain.toml` dosyasında sabittir; rustup doğru sürümü kendisi kurar)
- Linux'ta derlemek için: `libx11-dev libxkbcommon-dev libwayland-dev` ve bir Vulkan sürücüsü.
  Ekransız görüntü testleri için grafik kartı gerekmez: `mesa-vulkan-drivers` (lavapipe) yeterlidir.

## Komutlar

Hepsi depo kökünde çalıştırılır.

| İş                          | Komut                                                     |
| --------------------------- | --------------------------------------------------------- |
| Oyunu çalıştır              | `cargo run -p game`                                       |
| Testler                     | `cargo test --workspace`                                  |
| Beklenen resimleri yenile   | `UPDATE_SNAPSHOTS=1 cargo test --workspace`               |
| Biçim                       | `cargo fmt --all` (denetim: `cargo fmt --all --check`)    |
| Lint                        | `cargo clippy --workspace --all-targets -- -D warnings`   |
| Lisans denetimi             | `cargo deny check licenses bans sources`                  |
| Sürüm derlemesi             | `cargo build --release -p game`                           |
| Sahneyi resme çiz           | `cargo run -p game -- --goruntu cikti.png --boyut 3840x2160` |
| Bir SVG'yi resme çiz        | `cargo run -p engine --example svg-png -- girdi.svg cikti.png 2` |
| Örnek çizimleri yeniden üret | `python3 tools/art/ciz_birlikler.py` (ayrıca `ciz_manzara.py`, `ciz_pencere.py`) |
| Karakter ölçülerini karşılaştır | `python3 tools/art/kukla_olc.py` (önce `tools/referans/cikar.sh`) |
| Sanat kurallarını denetle   | `cargo test -p game --test art_rules`                     |

Çizimler elle değil, `tools/art/` içindeki betiklerle üretilir; betikler renkleri yalnızca
`tools/art/palet.txt` paletinden adıyla alır. Üretilen SVG'ler `content/art/` altına yazılır ve
commit edilir. `art_rules` testi her çizimi sanat rehberindeki kurallara göre denetler (palet,
kontur, degrade, eğri oranı, saydamlık); kurala aykırı çizim CI'ı kırmızıya düşürür.

Görüntü testleri: çizilen ve fark resimleri `target/goruntu-testleri/` altına yazılır. Bir test
"beklenen resim yok" ya da "farklı" derse önce bu resimlere bakılır; değişiklik bilerek yapıldıysa
beklenen resimler `UPDATE_SNAPSHOTS=1` ile yenilenir ve değişiklikle birlikte commit edilir.

## Kurallar

Dil:

- Kod tanımlayıcıları (değişken, işlev, tür adları) İngilizce; yorumlar, belgeler, commit mesajları ve
  oyunda görünen metinler Türkçe.
- Commit mesajlarının ilk satırı kısa ve emir kipinde ("Savaşa moral ekle"). Mesajın sonuna ek imza
  ya da etiket satırı eklenmez.
- Commit'ler `gozlemesevdalisi <333462860+gozlemesevdalisi@users.noreply.github.com>` adıyla atılır
  (depoda `git config user.name` ve `user.email` ile ayarlıdır).

Kod:

- `cargo fmt` ve `cargo clippy -D warnings` temiz olmadan push yapılmaz.
- `unsafe` kullanılmaz.
- Kütüphane kodunda `unwrap()`/`expect()`/`panic!` yerine hata türleri döndürülür (testler hariç).
- `sim` grafik, pencere ya da ses kütüphanesine bağlanmaz ve belirlenimci kalır (bkz. MOTOR.md).
- Oyun içeriği ve metinler koda gömülmez, `content/` altındaki veri dosyalarına yazılır.
- Her yeni işlev testleriyle gelir. Bir hata düzeltilirken önce o hatayı yakalayan test yazılır.

Görseller ve lisanslar:

- Bütün görseller, adlar ve metinler özgündür. Feudalism serisinin ya da başka bir oyunun dosyaları,
  adları ve çizimleri kullanılmaz.
- Dışarıdan alınan her varlık (yazı tipi, ses, müzik) eklenmeden önce lisansı doğrulanır ve kaynağıyla
  birlikte `docs/LISANSLAR.md` içine yazılır. AGPL ve ticari kullanımı yasaklayan lisanslar kabul edilmez.

Görsel güvenlik:

- Hiçbir efekt saniyede 3'ten fazla parlama üretmez; ani tam ekran beyaz ya da kırmızı geçiş yoktur.

## Yayın

- Her gönderimde (hangi dal olursa olsun) GitHub Actions çalışır (`.github/workflows/derleme.yml`):
  Linux'ta biçim, lint ve testler; lisans denetimi; ardından Windows'ta testler ve sürüm derlemesi.
  Hepsi geçerse `oyun.exe` "test-surumu" Release'ine konur. İndirme linki sabittir:
  https://github.com/lahmacunveayran/proje/releases/download/test-surumu/oyun.exe
- Rust sürümü `rust-toolchain.toml` ve iş akışında birlikte sabittir; yükseltirken ikisi birlikte değişir.
- Sürüm numarası `Cargo.toml` (çalışma alanı) içindedir.
