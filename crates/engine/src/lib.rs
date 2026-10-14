//! Oyundan bağımsız motor: pencere, çizim, vektör şekiller, yazı, girdi ve zaman.
//!
//! Motor oyun kuralı bilmez. Ayrıntılı açıklama: `docs/MOTOR.md`.

pub mod assets;
pub mod color;
pub mod image;
pub mod input;
pub mod paint;
pub mod render;
pub mod shape;
pub mod snapshot;
pub mod tessellate;
pub mod time;
pub mod viewport;

pub use glam;
