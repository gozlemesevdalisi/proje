//! Aktarılan Feudalism görsellerinin (content/feudalism) motorca okunabildiğini denetler.

use game::content::EMBEDDED;

use engine::svg::load_svg;
use engine::tessellate::tessellate;

#[test]
fn every_imported_shape_loads_and_tessellates() {
    let mut count = 0;
    let mut failures = Vec::new();
    // Vektör şekiller ve morph şekillerin başlangıç / bitiş hâlleri motorca çizilir. Resim dolgulu
    // şekiller (shapes-bitmap) ve canlandırmalı özgün morph dosyaları henüz çizilmez.
    let drawable = |n: &str| {
        n.starts_with("feudalism/")
            && (n.contains("/shapes/") || n.ends_with(".start.svg") || n.ends_with(".end.svg"))
    };
    for (name, data) in EMBEDDED.iter().filter(|(n, _)| drawable(n)) {
        count += 1;
        let result = load_svg(data)
            .map_err(|e| e.to_string())
            .and_then(|image| tessellate(&image, 0.1).map_err(|e| e.to_string()));
        if let Err(e) = result {
            failures.push(format!("{name}: {e}"));
        }
    }
    assert!(
        count > 3000,
        "aktarılan şekil sayısı beklenenden az: {count}"
    );
    assert!(
        failures.is_empty(),
        "okunamayan şekiller:\n{}",
        failures.join("\n")
    );
}

#[test]
fn both_libraries_are_embedded() {
    for game in ["f1", "f2"] {
        for file in ["library.json", "texts.json"] {
            let name = format!("feudalism/{game}/{file}");
            assert!(
                EMBEDDED.iter().any(|(n, _)| *n == name),
                "{name} gömülü değil"
            );
        }
    }
}

#[test]
fn images_and_sounds_are_embedded() {
    for (game, images, sounds) in [("f1", 18, 16), ("f2", 24, 16)] {
        let count = |dir: &str| {
            let prefix = format!("feudalism/{game}/{dir}/");
            EMBEDDED
                .iter()
                .filter(|(n, d)| n.starts_with(&prefix) && !d.is_empty())
                .count()
        };
        assert_eq!(count("images"), images, "{game} resim sayısı");
        assert_eq!(count("sounds"), sounds, "{game} ses sayısı");
    }
}
