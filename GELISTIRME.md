# Geliştirme

## Belgeler

- [docs/TASARIM.md](docs/TASARIM.md): oyunun tasarımı
- [docs/MOTOR.md](docs/MOTOR.md): motorun kararları ve yapısı
- [docs/YOL_HARITASI.md](docs/YOL_HARITASI.md): aşamalar ve yapılacaklar
- [docs/gunluk/](docs/gunluk/): geliştirme günlüğü; her çalışma gününün sonunda ne yapıldığı,
  durum ve sıradaki adım

## Gerekenler

- Rust (kararlı sürüm): https://rustup.rs
- Linux'ta derlemek için: `libx11-dev libxkbcommon-dev libwayland-dev` ve bir Vulkan sürücüsü.
  Ekransız görüntü testleri için grafik kartı gerekmez: `mesa-vulkan-drivers` (lavapipe) yeterlidir.

## Komutlar

Hepsi depo kökünde çalıştırılır.

| İş                   | Komut                                              |
| -------------------- | -------------------------------------------------- |
| Oyunu çalıştır       | `cargo run -p game`                                |
| Testler              | `cargo test --workspace`                           |
| Biçim                | `cargo fmt --all` (denetim: `cargo fmt --all --check`) |
| Lint                 | `cargo clippy --workspace --all-targets -- -D warnings` |
| Lisans denetimi      | `cargo deny check licenses bans sources`           |
| Sürüm derlemesi      | `cargo build --release -p game`                    |

## Kurallar

Dil:

- Kod tanımlayıcıları (değişken, işlev, tür adları) İngilizce; yorumlar, belgeler, commit mesajları ve
  oyunda görünen metinler Türkçe.
- Commit mesajlarının ilk satırı kısa ve emir kipinde ("Savaşa moral ekle"). Mesajın sonuna ek imza
  ya da etiket satırı eklenmez.

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

- `main` dalı her güncellendiğinde Windows sürümü otomatik derlenir ve "Test sürümü" Release'i yenilenir.
- Sürüm numarası `crates/game/Cargo.toml` içindedir.
