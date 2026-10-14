//! Aşama 0 deneme sahnesi: motorun temel yeteneklerini gösterir.

use std::error::Error;

use engine::app::{Control, FrameInfo, Game};
use engine::assets::Assets;
use engine::color::Color;
use engine::glam::{Affine2, Vec2};
use engine::input::{Input, Key};
use engine::render::{DrawList, GpuMesh, Renderer};
use engine::svg::load_svg;
use engine::tessellate::tessellate;
use engine::text::{Align, Font, TextStyle};

use crate::texts::Texts;

/// Sahnenin kullandığı metin anahtarları (testler hepsinin dosyada olduğunu denetler).
pub const TEXT_KEYS: &[&str] = &[
    "demo_title",
    "demo_subtitle",
    "demo_help",
    "demo_fps",
    "demo_sample_text",
];

/// Ekranda çizilecek kadar inceltilmiş üçgenleme payı (mantıksal piksel).
const TOLERANCE: f32 = 0.05;

struct Placed {
    mesh: GpuMesh,
    transform: Affine2,
}

pub struct DemoScene {
    texts: Texts,
    small_font: Font,
    background: Placed,
    card: Placed,
    card_size: Vec2,
    labels: Vec<Placed>,
    fps: Option<(i32, GpuMesh)>,
    /// Deneme çiziminin yatay kayması (← → ile).
    offset: f32,
    previous_offset: f32,
    velocity: f32,
}

fn load_font(assets: &Assets, path: &str, weight: Option<f32>) -> Result<Font, Box<dyn Error>> {
    Ok(Font::from_bytes(assets.read(path)?.into_owned(), weight)?)
}

impl DemoScene {
    pub fn new(renderer: &mut Renderer, assets: &Assets) -> Result<Self, Box<dyn Error>> {
        let texts = Texts::load(assets, "tr")?;
        let title_font = load_font(assets, "fonts/AlegreyaSC-Bold.ttf", None)?;
        let body_font = load_font(assets, "fonts/Alegreya-Variable.ttf", Some(400.0))?;
        let small_font = load_font(assets, "fonts/AlegreyaSans-Regular.ttf", None)?;

        let background = load_svg(&assets.read("art/test/arka-plan.svg")?)?;
        let card = load_svg(&assets.read("art/test/deneme.svg")?)?;
        let card_size = card.size;

        let parchment = Color::from_hex("#F1E3C2")?;
        let cream = Color::from_hex("#FFF6D2")?;
        let mut labels = Vec::new();
        let mut text = |font: &Font,
                        key: &str,
                        style: TextStyle,
                        color: Color,
                        at: Vec2|
         -> Result<(), Box<dyn Error>> {
            let image = font.text_image(texts.get(key), &style, color)?;
            labels.push(Placed {
                mesh: renderer.upload(&tessellate(&image, TOLERANCE)?),
                transform: Affine2::from_translation(at),
            });
            Ok(())
        };
        text(
            &title_font,
            "demo_title",
            TextStyle::new(72.0),
            cream,
            Vec2::new(96.0, 80.0),
        )?;
        text(
            &body_font,
            "demo_subtitle",
            TextStyle::new(34.0),
            parchment,
            Vec2::new(100.0, 180.0),
        )?;
        text(
            &body_font,
            "demo_sample_text",
            TextStyle::new(30.0).wrap(760.0),
            parchment,
            Vec2::new(100.0, 300.0),
        )?;
        text(
            &small_font,
            "demo_help",
            TextStyle::new(24.0).wrap(1728.0).align(Align::Center),
            parchment,
            Vec2::new(96.0, 1010.0),
        )?;

        Ok(DemoScene {
            background: Placed {
                mesh: renderer.upload(&tessellate(&background, TOLERANCE)?),
                transform: Affine2::IDENTITY,
            },
            card: Placed {
                // Deneme çizimi küçük tasarlandı; vektör olduğu için büyütünce de keskin kalır.
                mesh: renderer.upload(&tessellate(&card, TOLERANCE / 4.0)?),
                transform: Affine2::IDENTITY,
            },
            card_size,
            texts,
            small_font,
            labels,
            fps: None,
            offset: 0.0,
            previous_offset: 0.0,
            velocity: 0.0,
        })
    }

    fn fps_mesh(&mut self, renderer: &mut Renderer, fps: f32) -> Option<GpuMesh> {
        let value = fps.round() as i32;
        if let Some((v, mesh)) = &self.fps
            && *v == value
        {
            return Some(mesh.clone());
        }
        let text = self
            .texts
            .format("demo_fps", &[("fps", &value.to_string())]);
        let color = Color::rgba(0.95, 0.89, 0.76, 0.8);
        let image = self
            .small_font
            .text_image(
                &text,
                &TextStyle::new(22.0).wrap(200.0).align(Align::Right),
                color,
            )
            .ok()?;
        let mesh = renderer.upload(&tessellate(&image, TOLERANCE).ok()?);
        self.fps = Some((value, mesh.clone()));
        Some(mesh)
    }
}

impl Game for DemoScene {
    fn update(&mut self, input: &Input, control: &mut Control) {
        if input.key_pressed(Key::Escape) {
            control.quit();
        }
        let mut dir = 0.0;
        if input.key_down(Key::ArrowLeft) || input.key_down(Key::KeyA) {
            dir -= 1.0;
        }
        if input.key_down(Key::ArrowRight) || input.key_down(Key::KeyD) {
            dir += 1.0;
        }
        self.previous_offset = self.offset;
        // Yumuşak hızlanma ve yavaşlama.
        self.velocity += (dir * 9.0 - self.velocity) * 0.15;
        self.offset = (self.offset + self.velocity).clamp(-400.0, 300.0);
    }

    fn draw(&mut self, renderer: &mut Renderer, frame: &FrameInfo) -> DrawList {
        let mut list = DrawList::new(Color::from_hex("#1E4FA6").unwrap_or(Color::BLACK));
        list.draw(&self.background.mesh, self.background.transform);
        let offset = self.previous_offset + (self.offset - self.previous_offset) * frame.alpha;
        let scale = 640.0 / self.card_size.x;
        let card = Affine2::from_translation(Vec2::new(1180.0 + offset, 290.0))
            * Affine2::from_scale(Vec2::splat(scale))
            * self.card.transform;
        list.draw(&self.card.mesh, card);
        for label in &self.labels {
            list.draw(&label.mesh, label.transform);
        }
        if let Some(mesh) = self.fps_mesh(renderer, frame.fps) {
            list.draw(&mesh, Affine2::from_translation(Vec2::new(1690.0, 24.0)));
        }
        list
    }
}

/// Sahnenin bir karesini ekransız çizer (komut satırı ve testler için).
pub fn render_frame(
    scene: &mut DemoScene,
    renderer: &mut Renderer,
    size: engine::glam::UVec2,
) -> Result<engine::image::RgbaImage, Box<dyn Error>> {
    let viewport = engine::viewport::Viewport::fit(engine::viewport::LOGICAL_SIZE, size);
    let frame = FrameInfo {
        alpha: 0.0,
        viewport,
        fps: 60.0,
    };
    let list = scene.draw(renderer, &frame);
    Ok(renderer.render_to_image(&viewport, &list)?)
}
