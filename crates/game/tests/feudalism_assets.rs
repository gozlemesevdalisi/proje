//! Aktarılan Feudalism içeriğinin (content/feudalism) ve Türkçe çevirinin motorca okunabildiğini denetler.
#![allow(clippy::unwrap_used, clippy::expect_used, clippy::panic)]

use std::collections::HashMap;

use game::content::EMBEDDED;

use engine::svg::load_svg;
use engine::tessellate::tessellate;
use engine::text::Font;

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

fn embedded(name: &str) -> &'static [u8] {
    EMBEDDED
        .iter()
        .find(|(n, _)| *n == name)
        .map(|(_, d)| *d)
        .unwrap_or_else(|| panic!("{name} gömülü değil"))
}

fn json(name: &str) -> serde_json::Value {
    serde_json::from_slice(embedded(name)).unwrap_or_else(|e| panic!("{name}: {e}"))
}

/// texts.json'daki yazı tipi kimliği → açık lisanslı karşılığı (yüklenmiş).
fn substitute_fonts(texts: &serde_json::Value) -> HashMap<String, (String, Font)> {
    let mut out = HashMap::new();
    for (fid, font) in texts["fonts"].as_object().expect("fonts") {
        let file = font["file"]
            .as_str()
            .unwrap_or_else(|| panic!("yazı tipi {fid} için karşılık yok"));
        let loaded = Font::from_bytes(embedded(file).to_vec(), None)
            .unwrap_or_else(|e| panic!("{file} okunamadı: {e}"));
        out.insert(fid.clone(), (file.to_string(), loaded));
    }
    out
}

#[test]
fn every_font_has_an_open_substitute_with_turkish_letters() {
    for game in ["f1", "f2"] {
        let texts = json(&format!("feudalism/{game}/texts.json"));
        for (fid, (file, font)) in substitute_fonts(&texts) {
            for c in "çğıİöşüÇĞÖŞÜ".chars() {
                assert!(
                    font.has_char(c),
                    "{game} yazı tipi {fid} ({file}): '{c}' yok"
                );
            }
        }
    }
}

#[test]
fn every_translated_text_can_be_drawn_with_its_font() {
    let drawable = |c: &char| !c.is_whitespace() && !c.is_control();
    for game in ["f1", "f2"] {
        let texts = json(&format!("feudalism/{game}/texts.json"));
        let fonts = substitute_fonts(&texts);
        let mut missing = Vec::new();
        // Sabit yazılar: her parça orijinaldeki bir kayda denk gelir; yazı tipi önceki kayıttan sürer
        let statics = json(&format!("feudalism/{game}/ceviri/sabit.json"));
        for (tid, entry) in statics.as_object().expect("sabit").iter() {
            if tid.starts_with('_') {
                continue;
            }
            let records = texts["texts"][tid]["records"].as_array().expect("kayıtlar");
            let mut font = String::new();
            for (record, part) in records
                .iter()
                .zip(entry["parcalar"].as_array().expect("parçalar"))
            {
                if let Some(f) = record["font"].as_u64() {
                    font = f.to_string();
                }
                let (file, f) = &fonts[&font];
                for c in part.as_str().expect("parça").chars().filter(drawable) {
                    if !f.has_char(c) {
                        missing.push(format!("sabit yazı {tid}: '{c}' {file} içinde yok"));
                    }
                }
            }
        }
        // Ekran kutuları: kutunun kendi yazı tipiyle (HTML etiketleri harf sayılmaz)
        let boxes = json(&format!("feudalism/{game}/ceviri/kutular.json"));
        for (eid, value) in boxes.as_object().expect("kutular").iter() {
            if eid.starts_with('_') {
                continue;
            }
            let Some(font) = texts["edit_texts"][eid]["font"].as_u64() else {
                continue;
            };
            let raw = value
                .as_str()
                .or_else(|| value["metin"].as_str())
                .expect("kutu yazısı");
            let raw = raw.strip_prefix("html:").unwrap_or(raw);
            let mut text = String::new();
            let mut in_tag = false;
            for c in raw.chars() {
                match c {
                    '<' => in_tag = true,
                    '>' => in_tag = false,
                    _ if !in_tag => text.push(c),
                    _ => {}
                }
            }
            let (file, f) = &fonts[&font.to_string()];
            for c in text.chars().filter(drawable) {
                if !f.has_char(c) {
                    missing.push(format!("ekran kutusu {eid}: '{c}' {file} içinde yok"));
                }
            }
        }
        assert!(
            missing.is_empty(),
            "{game}: çizilemeyen harfler:\n{}",
            missing.join("\n")
        );
    }
}

#[test]
fn translation_tables_and_drawn_texts_are_embedded() {
    for (game, drawn) in [("f1", "2019"), ("f2", "3094")] {
        for table in [
            "adlar",
            "kod",
            "sabit",
            "kutular",
            "yazitipleri",
            "sekiller",
        ] {
            json(&format!("feudalism/{game}/ceviri/{table}.json"));
        }
        let svg = embedded(&format!("feudalism/{game}/ceviri/sekiller/{drawn}.svg"));
        let image = load_svg(svg).expect("Öldün... çizimi okunur");
        tessellate(&image, 0.1).expect("Öldün... çizimi üçgenlenir");
    }
}
