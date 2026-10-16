//! Aktarılan Feudalism görsellerinin (content/feudalism) motorca okunabildiğini denetler.

use game::content::EMBEDDED;

use engine::svg::load_svg;
use engine::tessellate::tessellate;

#[test]
fn every_imported_shape_loads_and_tessellates() {
    let mut count = 0;
    let mut failures = Vec::new();
    for (name, data) in EMBEDDED
        .iter()
        .filter(|(n, _)| n.starts_with("feudalism/") && n.ends_with(".svg"))
    {
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
        let name = format!("feudalism/{game}/library.json");
        assert!(
            EMBEDDED.iter().any(|(n, _)| *n == name),
            "{name} gömülü değil"
        );
    }
}
