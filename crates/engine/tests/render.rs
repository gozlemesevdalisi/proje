//! Grafik kartında çizim testleri (ekransız).
#![allow(clippy::unwrap_used, clippy::expect_used, clippy::panic)]

mod common;

use common::{assert_close, assert_snapshot, renderer};
use engine::color::Color;
use engine::glam::{Affine2, UVec2, Vec2};
use engine::paint::{Gradient, GradientKind, GradientStop, Paint, Spread};
use engine::render::{ColorTransform, DrawList, LETTERBOX_COLOR};
use engine::shape::{Shape, Stroke, VectorImage, circle_path, polygon_path, rect_path};
use engine::tessellate::tessellate;
use engine::viewport::{LOGICAL_SIZE, Viewport};

fn hex(s: &str) -> Color {
    Color::from_hex(s).unwrap()
}

fn image(shapes: Vec<Shape>) -> VectorImage {
    VectorImage {
        shapes,
        size: Vec2::splat(100.0),
    }
}

/// 100×100 mantıksal alanı 100×100 piksele çizer.
fn small_viewport() -> Viewport {
    Viewport::fit(Vec2::splat(100.0), UVec2::splat(100))
}

#[test]
fn solid_shapes_have_exact_colors() {
    let mut r = renderer();
    let mesh = r.upload(
        &tessellate(
            &image(vec![
                Shape::filled(
                    rect_path(Vec2::new(10.0, 10.0), Vec2::new(40.0, 40.0)),
                    hex("#A3241A"),
                ),
                Shape::filled(circle_path(Vec2::new(70.0, 70.0), 20.0), hex("#23406E")),
            ]),
            0.05,
        )
        .unwrap(),
    );
    let mut list = DrawList::new(hex("#F1E3C2"));
    list.draw(&mesh, Affine2::IDENTITY);
    let img = r.render_to_image(&small_viewport(), &list).unwrap();
    assert_eq!(img.pixel(30, 30), [0xA3, 0x24, 0x1A, 255]);
    assert_eq!(img.pixel(70, 70), [0x23, 0x40, 0x6E, 255]);
    assert_eq!(img.pixel(95, 5), [0xF1, 0xE3, 0xC2, 255]);
    assert_snapshot("duz-sekiller", &img);
}

#[test]
fn linear_gradient_matches_cpu() {
    let mut r = renderer();
    let g = Gradient::linear(
        Vec2::new(0.0, 0.0),
        Vec2::new(100.0, 0.0),
        vec![
            GradientStop::new(0.0, hex("#1E4FA6")),
            GradientStop::new(0.6, hex("#9FCBEA")),
            GradientStop::new(1.0, hex("#F3E2B0")),
        ],
    );
    let paint = Paint::Gradient(g.clone());
    let mesh = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::ZERO, Vec2::splat(100.0)),
                paint.clone(),
            )]),
            0.05,
        )
        .unwrap(),
    );
    let mut list = DrawList::new(Color::BLACK);
    list.draw(&mesh, Affine2::IDENTITY);
    let img = r.render_to_image(&small_viewport(), &list).unwrap();
    for x in [0u32, 13, 37, 50, 61, 80, 99] {
        let expected = paint.sample(Vec2::new(x as f32 + 0.5, 50.5)).to_rgba8();
        assert_close(img.pixel(x, 50), expected, 3, &format!("x={x}"));
    }
}

#[test]
fn radial_and_focal_gradients_match_cpu() {
    let mut r = renderer();
    let stops = vec![
        GradientStop::new(0.0, hex("#FFF6D2")),
        GradientStop::new(1.0, hex("#3B7BCB")),
    ];
    let mut focal = Gradient::radial(Vec2::new(50.0, 50.0), 40.0, stops.clone());
    focal.kind = GradientKind::Radial {
        center: Vec2::new(50.0, 50.0),
        radius: 40.0,
        focal: Vec2::new(35.0, 40.0),
    };
    let mut reflect = Gradient::radial(Vec2::new(50.0, 50.0), 15.0, stops);
    reflect.spread = Spread::Reflect;
    for (name, g) in [("odakli", focal), ("aynali", reflect)] {
        let paint = Paint::Gradient(g);
        let mesh = r.upload(
            &tessellate(
                &image(vec![Shape::filled(
                    rect_path(Vec2::ZERO, Vec2::splat(100.0)),
                    paint.clone(),
                )]),
                0.05,
            )
            .unwrap(),
        );
        let mut list = DrawList::new(Color::BLACK);
        list.draw(&mesh, Affine2::IDENTITY);
        let img = r.render_to_image(&small_viewport(), &list).unwrap();
        for (x, y) in [
            (50u32, 50u32),
            (35, 40),
            (20, 20),
            (80, 60),
            (10, 90),
            (65, 50),
        ] {
            let expected = paint
                .sample(Vec2::new(x as f32 + 0.5, y as f32 + 0.5))
                .to_rgba8();
            assert_close(img.pixel(x, y), expected, 3, &format!("{name} ({x},{y})"));
        }
    }
}

#[test]
fn edges_are_antialiased() {
    let mut r = renderer();
    let mesh = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                polygon_path(&[
                    Vec2::new(0.0, 0.0),
                    Vec2::new(100.0, 30.0),
                    Vec2::new(0.0, 100.0),
                ]),
                Color::WHITE,
            )]),
            0.05,
        )
        .unwrap(),
    );
    let mut list = DrawList::new(Color::BLACK);
    list.draw(&mesh, Affine2::IDENTITY);
    let img = r.render_to_image(&small_viewport(), &list).unwrap();
    let partial = img
        .data
        .as_chunks::<4>()
        .0
        .iter()
        .filter(|p| p[0] > 10 && p[0] < 245)
        .count();
    assert!(
        partial > 50,
        "yumuşatılmış kenar pikseli bulunamadı ({partial})"
    );
}

#[test]
fn transforms_and_color_transforms() {
    let mut r = renderer();
    let mesh = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::ZERO, Vec2::splat(10.0)),
                Color::WHITE,
            )]),
            0.05,
        )
        .unwrap(),
    );
    let mut list = DrawList::new(Color::BLACK);
    // Yarı saydam beyaz: siyah üstünde ~%50 gri.
    list.draw_with(
        &mesh,
        Affine2::from_translation(Vec2::new(5.0, 5.0)),
        ColorTransform::alpha(0.5),
    );
    // Ölçek ve kaydırma; kırmızıyla çarpılmış beyaz.
    list.draw_with(
        &mesh,
        Affine2::from_scale_angle_translation(Vec2::splat(3.0), 0.0, Vec2::new(50.0, 50.0)),
        ColorTransform::multiply(hex("#C8372D")),
    );
    let img = r.render_to_image(&small_viewport(), &list).unwrap();
    assert_close(img.pixel(10, 10), [128, 128, 128, 255], 2, "yarı saydam");
    assert_close(
        img.pixel(78, 78),
        [0xC8, 0x37, 0x2D, 255],
        1,
        "renklendirilmiş",
    );
    assert_eq!(img.pixel(45, 45), [0, 0, 0, 255]);
}

#[test]
fn letterbox_bars_outside_logical_area() {
    let mut r = renderer();
    let mesh = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::new(-500.0, -500.0), Vec2::splat(3000.0)),
                Color::WHITE,
            )]),
            0.05,
        )
        .unwrap(),
    );
    let mut list = DrawList::new(hex("#3B7BCB"));
    list.draw_with(&mesh, Affine2::IDENTITY, ColorTransform::alpha(0.0));
    // 16:9 alanı 4:3 resme sığdır: üstte ve altta şerit kalır.
    let vp = Viewport::fit(LOGICAL_SIZE, UVec2::new(400, 300));
    let img = r.render_to_image(&vp, &list).unwrap();
    let bar = LETTERBOX_COLOR.to_rgba8();
    assert_close(img.pixel(200, 5), bar, 1, "üst şerit");
    assert_close(img.pixel(200, 295), bar, 1, "alt şerit");
    assert_close(img.pixel(200, 150), hex("#3B7BCB").to_rgba8(), 1, "içerik");

    // Mantıksal alanın dışına taşan şekil şeritlere çizilmez.
    let mut list = DrawList::new(Color::BLACK);
    list.draw(&mesh, Affine2::IDENTITY);
    let img = r.render_to_image(&vp, &list).unwrap();
    assert_close(img.pixel(200, 5), bar, 1, "kırpılmış üst şerit");
    assert_eq!(img.pixel(200, 150), [255, 255, 255, 255]);
}

#[test]
fn transparent_background_without_bars_stays_transparent() {
    // Ölçüm araçları çizimleri saydam zeminde ister: şerit yoksa boş pikseller saydam kalır.
    let mut r = renderer();
    let mesh = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::new(25.0, 25.0), Vec2::splat(50.0)),
                hex("#A3241A"),
            )]),
            0.05,
        )
        .unwrap(),
    );
    let mut list = DrawList::new(Color::TRANSPARENT);
    list.draw(&mesh, Affine2::IDENTITY);
    let img = r.render_to_image(&small_viewport(), &list).unwrap();
    assert_eq!(img.pixel(5, 5), [0, 0, 0, 0], "boş köşe");
    assert_eq!(img.pixel(50, 50), hex("#A3241A").to_rgba8(), "şekil");
}

#[test]
fn many_paints_and_instances_grow_buffers() {
    let mut r = renderer();
    let mut list = DrawList::new(Color::BLACK);
    let mut meshes = Vec::new();
    for i in 0..300 {
        let t = i as f32 / 299.0;
        let g = Gradient::linear(
            Vec2::ZERO,
            Vec2::new(4.0, 0.0),
            vec![
                GradientStop::new(0.0, Color::rgba(t, 0.0, 0.0, 1.0)),
                GradientStop::new(1.0, Color::rgba(t, 0.0, 0.0, 1.0)),
            ],
        );
        meshes.push(
            r.upload(
                &tessellate(
                    &image(vec![Shape::filled(
                        rect_path(Vec2::ZERO, Vec2::splat(4.0)),
                        g,
                    )]),
                    0.05,
                )
                .unwrap(),
            ),
        );
    }
    for (i, m) in meshes.iter().enumerate() {
        let x = (i % 20) as f32 * 5.0;
        let y = (i / 20) as f32 * 5.0;
        list.draw(m, Affine2::from_translation(Vec2::new(x, y)));
    }
    let img = r.render_to_image(&small_viewport(), &list).unwrap();
    // Son kare (i = 299): x = 95, y = 70; rengi tam kırmızı.
    assert_close(img.pixel(97, 72), [255, 0, 0, 255], 2, "son kare");
    assert_close(img.pixel(2, 2), [0, 0, 0, 255], 1, "ilk kare");
}

#[test]
fn composed_scene_snapshot() {
    let mut r = renderer();
    let sky = Gradient::linear(
        Vec2::new(0.0, 0.0),
        Vec2::new(0.0, 60.0),
        vec![
            GradientStop::new(0.0, hex("#1E4FA6")),
            GradientStop::new(1.0, hex("#9FCBEA")),
        ],
    );
    let sun = Gradient::radial(
        Vec2::new(30.0, 20.0),
        18.0,
        vec![
            GradientStop::new(0.0, hex("#FFE9A0")),
            GradientStop::new(1.0, hex("#FFE9A0").with_alpha(0.0)),
        ],
    );
    let hill = Gradient::linear(
        Vec2::new(0.0, 55.0),
        Vec2::new(0.0, 100.0),
        vec![
            GradientStop::new(0.0, hex("#8DBF4A")),
            GradientStop::new(1.0, hex("#3B6E2C")),
        ],
    );
    let mut b = engine::shape::VectorImage::new(Vec2::splat(100.0));
    b.push(Shape::filled(
        rect_path(Vec2::ZERO, Vec2::new(100.0, 70.0)),
        sky,
    ));
    b.push(Shape::filled(circle_path(Vec2::new(30.0, 20.0), 18.0), sun));
    b.push(Shape::filled(
        circle_path(Vec2::new(30.0, 20.0), 6.0),
        hex("#FFF6D2"),
    ));
    b.push(Shape::filled(
        polygon_path(&[
            Vec2::new(0.0, 100.0),
            Vec2::new(0.0, 62.0),
            Vec2::new(30.0, 52.0),
            Vec2::new(60.0, 60.0),
            Vec2::new(100.0, 50.0),
            Vec2::new(100.0, 100.0),
        ]),
        hill,
    ));
    b.push(
        Shape::filled(circle_path(Vec2::new(70.0, 75.0), 8.0), hex("#A3241A"))
            .with_stroke(Stroke::round(hex("#3A0E0A"), 1.5)),
    );
    let mesh = r.upload(&tessellate(&b, 0.02).unwrap());
    let mut list = DrawList::new(Color::BLACK);
    list.draw(&mesh, Affine2::IDENTITY);
    let img = r
        .render_to_image(&Viewport::fit(Vec2::splat(100.0), UVec2::splat(256)), &list)
        .unwrap();
    assert_snapshot("bilesik-sahne", &img);
}

#[test]
fn masks_clip_drawings_and_nest() {
    // Flash maskesi: maske şeklinin kendisi görünmez; maske açıkken çizilenler yalnız onun içinde
    // görünür. İç içe maskelerde ikisinin kesişimi kalır; maske kapanınca çizim yine her yerdedir.
    let mut r = renderer();
    let red = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::ZERO, Vec2::splat(100.0)),
                hex("#C00000"),
            )]),
            0.05,
        )
        .unwrap(),
    );
    let left = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::ZERO, Vec2::new(50.0, 100.0)),
                hex("#00FF00"),
            )]),
            0.05,
        )
        .unwrap(),
    );
    let top = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::ZERO, Vec2::new(100.0, 50.0)),
                hex("#0000FF"),
            )]),
            0.05,
        )
        .unwrap(),
    );
    let blue = r.upload(
        &tessellate(
            &image(vec![Shape::filled(
                rect_path(Vec2::ZERO, Vec2::splat(10.0)),
                hex("#2040A0"),
            )]),
            0.05,
        )
        .unwrap(),
    );
    let mut list = DrawList::new(hex("#FFFFFF"));
    list.push_mask(&[(left.clone(), Affine2::IDENTITY)]);
    list.draw(&red, Affine2::IDENTITY);
    list.push_mask(&[(top.clone(), Affine2::IDENTITY)]);
    list.draw_with(
        &red,
        Affine2::IDENTITY,
        ColorTransform::multiply(hex("#000000")),
    );
    list.pop_mask();
    list.pop_mask();
    list.draw(&blue, Affine2::from_translation(Vec2::new(85.0, 85.0)));
    let img = r.render_to_image(&small_viewport(), &list).unwrap();
    // Sol üst: iki maskenin kesişimi (siyah); sol alt: yalnız dış maske (kırmızı); sağ: maske dışı (beyaz)
    assert_eq!(img.pixel(25, 25), [0, 0, 0, 255]);
    assert_eq!(img.pixel(25, 75), [0xC0, 0, 0, 255]);
    assert_eq!(img.pixel(75, 25), [255, 255, 255, 255]);
    assert_eq!(img.pixel(75, 75), [255, 255, 255, 255]);
    // Maske şekilleri (yeşil, mavi) hiç görünmez; maskeler kapandıktan sonraki çizim her yerde görünür
    assert_eq!(img.pixel(90, 90), [0x20, 0x40, 0xA0, 255]);
}
