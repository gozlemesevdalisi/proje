# Feudalism 1 ve 2: içerik dökümü

`python3 araclar/aktar/envanter.py` üretir; elle değiştirmeyin. Oyunların neyi var, neyi yok ve
her birinin oyunumuza aktarılma durumu. Görseller hak sahibinin izniyle kullanılır
(bkz. `docs/LISANSLAR.md`).

## Feudalism (f1)

Sahne 800×600 piksel, saniyede 30 kare, arka plan `#35567B`. Kaynak: `feudalism-orijinal.swf`.

| İçerik | Sayı | Durum |
|---|---|---|
| Şekil (vektör çizim) | 1234 | 1159 aktarıldı; 19 resim dolgulu şekil bekliyor |
| Sprite (hareketli sembol) | 246 | 194 aktarıldı (zaman çizelgesiyle) |
| Düğme | 175 | 174 aktarıldı |
| Ekran (kök film karesi) | 92 | aktarıldı |
| Morph (biçim değiştiren şekil) | 16 | bekliyor |
| Resim (bit eşlem) | 18 | bekliyor |
| Ses | 16 | bekliyor |
| Müzik | 0 | oyunda müzik yok |
| Sabit yazı | 122 | bekliyor (Türkçeye çevrilip kendi yazı tiplerimizle çizilecek) |
| Yazı alanı (oyunun doldurduğu) | 251 | bekliyor |
| Yazı tipi | 15 | aktarılmayacak: lisansları yazı tipi yapımcılarında |
| Oyun kodu (ActionScript 2 sınıfı) | 29 | görsel değil; oyun mantığı kendi kodumuzla yazılır |
| Macromedia arayüz bileşeni | 0 | aktarılmayacak: Adobe'nin; oyunda kullanılmıyor |
| Sponsor logosu | 1 | aktarılmayacak: sponsorun |

### Ekranlar (kök film)

| Kare | Ne |
|---|---|
| 1–3 | açılış: yükleme, sponsor logoları (aktarılmadı), giriş animasyonu |
| 4 | ana menü |
| 5–84 | savaş alanı arka planları (80 kare) |
| 85 | kamp / kasaba (`TOWN_SCREEN`) |
| 86 | dünya haritası (`WORLD_MAP`) |
| 87 | savaşa hazırlık (`SPLASH_SCREEN`) |
| 88 | kayıt yükleme (`GAME_LOAD`) |
| 89 | oyun bitti (`GAME_OVER`) |
| 90 | zafer (`VICTORY`) |
| 91 | korsan kopya uyarısı (`STOLEN`) |
| 92 | savaş öğreticisi (`BATTLE_TUT`) |

### Dışa aktarılan semboller (oyunun kodla çağırdığı)

`Ammun`, `Amount window`, `Arrow`, `ArrowShower`, `ArrowWall`, `BarnUnit`, `BarracksUnit`, `BarracksUnit - tutorial`, `Barrel`, `BlackSquare`, `Blood_1`, `Blood_2`, `Bush_1`, `Bush_2`, `Bush_3`, `Bush_4`, `Cities`, `Crate_1`, `Crate_2`, `FlyCritDamage`, `FlyDamage`, `GrenSymb`, `Grenade`, `Head_on_spear`, `HealAnim`, `Horseman`, `Horseman_Player`, `Human`, `Human_Player`, `ICON Equipment`, `ICON Inventory`, `ICON Mouse`, `Lantern`, `RIP_1`, `RIP_2`, `RageAnim`, `RiseAnim`, `Screen`, `SelectBorder`, `Sign`, `Sign2`, `SkullTower`, `Sword_in_ground_1`, `Sword_in_ground_2`, `TreeBroken_1`, `Tree_1`, `Tree_10`, `Tree_11`, `Tree_12`, `Tree_2`, `Tree_3`, `Tree_4`, `Tree_5`, `Tree_6`, `Tree_7`, `Tree_8`, `Tree_9`, `Well_1`, `WorldMap`, `slash.wav`

### Sesler

Hepsi kısa ses efekti; müzik yok.

| Kimlik | Ad | Süre | Biçim | Nerede çalıyor |
|---|---|---|---|---|
| 530 |  | 1.4 sn | MP3 11025 Hz mono | Human.body / sword / kare 12; Horseman.body / sword / kare 12 |
| 531 |  | 0.8 sn | MP3 11025 Hz mono | Human.body / twohanded_sword / kare 53; Horseman.body / twohanded_sword / kare 53 |
| 532 |  | 1.8 sn | MP3 11025 Hz mono | Human.body / twohanded_axe / kare 94; Horseman.body / twohanded_axe / kare 94 |
| 533 |  | 1.5 sn | MP3 11025 Hz mono | Human.body / double / kare 116; Human.body / double / kare 130; Human.body / katana / kare 307 |
| 534 |  | 0.8 sn | MP3 11025 Hz mono | Human.body / spear / kare 149; Horseman.body / spear / kare 120 |
| 535 |  | 0.5 sn | MP3 11025 Hz mono | Human.body / bow / kare 187; Human.body / crossbow / kare 225; Horseman.body / bow / kare 161; Horseman.body / crossbow / kare 194 |
| 536 |  | 0.4 sn | MP3 11025 Hz mono | Human.body / dagger / kare 276; Human.body / fists / kare 367; Human.body / fists / kare 377; Horseman.body / fists / kare 259 |
| 537 |  | 0.4 sn | MP3 11025 Hz mono | Human.body / staff / kare 321 |
| 538 |  | 0.7 sn | MP3 11025 Hz mono | Human.body / staff / kare 337 |
| 539 |  | 0.5 sn | MP3 11025 Hz mono | Human.body / suriken / kare 400; Horseman.body / suriken / kare 291 |
| 540 |  | 0.9 sn | MP3 11025 Hz mono | Human.body / die_ranged / kare 736 |
| 541 |  | 0.8 sn | MP3 11025 Hz mono | Human.body / die_twohanded / kare 776 |
| 542 |  | 1.0 sn | MP3 11025 Hz mono | Human.body / die_onehanded / kare 826 |
| 565 |  | 1.4 sn | MP3 11025 Hz mono | Horseman.body / die_horse / kare 566 |
| 578 |  | 2.5 sn | MP3 11025 Hz mono | Grenade / blow / kare 2 |
| 930 | slash.wav | 0.6 sn | MP3 11025 Hz mono | kodla çalınır |

### Resimler

| Kimlik | Boyut | Not |
|---|---|---|
| 1327 | 70×71 |  |
| 1341 | 800×200 | savaş alanı zemin dokusu |
| 1352 | 800×200 | savaş alanı zemin dokusu |
| 1362 | 800×200 | savaş alanı zemin dokusu |
| 1372 | 800×200 | savaş alanı zemin dokusu |
| 1382 | 800×200 | savaş alanı zemin dokusu |
| 1389 | 800×200 | savaş alanı zemin dokusu |
| 1394 | 800×200 | savaş alanı zemin dokusu |
| 1398 | 800×200 | savaş alanı zemin dokusu |
| 1401 | 800×200 | savaş alanı zemin dokusu |
| 1405 | 800×200 | savaş alanı zemin dokusu |
| 1409 | 800×200 | savaş alanı zemin dokusu |
| 1412 | 800×200 | savaş alanı zemin dokusu |
| 1417 | 800×200 | savaş alanı zemin dokusu |
| 1431 | 800×200 | savaş alanı zemin dokusu |
| 1434 | 800×200 | savaş alanı zemin dokusu |
| 1439 | 800×200 | savaş alanı zemin dokusu |
| 1442 | 800×200 | savaş alanı zemin dokusu |

### Yazı tipleri (aktarılmayacak)

| Kimlik | Ad | Biçem | Gömülü glif |
|---|---|---|---|
| 45 | Arial | kalın | 10 |
| 49 | _sans | kalın | yok (sistem yazı tipi) |
| 156 | Times New Roman | kalın, italik | yok (sistem yazı tipi) |
| 159 | Times New Roman | normal | 43 |
| 176 | _serif | normal | yok (sistem yazı tipi) |
| 889 | _serif | kalın | yok (sistem yazı tipi) |
| 1038 | Book Antiqua | kalın | 51 |
| 1153 | Bookman Old Style | kalın | 52 |
| 1253 | _sans | normal | yok (sistem yazı tipi) |
| 1483 | Book Antiqua | kalın, italik | 11 |
| 1521 | _serif | kalın, italik | yok (sistem yazı tipi) |
| 1758 | Bookman Old Style | italik | 38 |
| 1837 | _sans | kalın, italik | yok (sistem yazı tipi) |
| 1983 | Monotype Corsiva | kalın | 18 |
| 2008 | Century Gothic | kalın | 29 |

### Oyun kodunun sınıfları

`Armor`, `Arrow`, `ArrowStorm`, `BarnIcon`, `BarracksIcon`, `Cage`, `Cities`, `Creature`, `Enchant`, `EquipmentIcon`, `Grenade`, `Hero`, `Horse`, `Item`, `ItemInfo`, `Player`, `Projectile`, `Quest`, `Screen`, `SelectBorder`, `Soldier`, `StoreIcon`, `Town`, `Tree`, `Unit`, `UnitInfo`, `Weapon`, `WeaponClass`, `WorldMap`

## Feudalism 2 (f2)

Sahne 800×600 piksel, saniyede 30 kare, arka plan `#35567B`. Kaynak: `feudalism-2-orijinal.swf`.

| İçerik | Sayı | Durum |
|---|---|---|
| Şekil (vektör çizim) | 2184 | 2116 aktarıldı; 31 resim dolgulu şekil bekliyor |
| Sprite (hareketli sembol) | 441 | 266 aktarıldı (zaman çizelgesiyle) |
| Düğme | 179 | 178 aktarıldı |
| Ekran (kök film karesi) | 116 | aktarıldı |
| Morph (biçim değiştiren şekil) | 25 | bekliyor |
| Resim (bit eşlem) | 24 | bekliyor |
| Ses | 16 | bekliyor |
| Müzik | 0 | oyunda müzik yok |
| Sabit yazı | 104 | bekliyor (Türkçeye çevrilip kendi yazı tiplerimizle çizilecek) |
| Yazı alanı (oyunun doldurduğu) | 194 | bekliyor |
| Yazı tipi | 16 | aktarılmayacak: lisansları yazı tipi yapımcılarında |
| Oyun kodu (ActionScript 2 sınıfı) | 43 | görsel değil; oyun mantığı kendi kodumuzla yazılır |
| Macromedia arayüz bileşeni | 85 | aktarılmayacak: Adobe'nin; oyunda kullanılmıyor |
| Sponsor logosu | 0 | aktarılmayacak: sponsorun |

### Ekranlar (kök film)

| Kare | Ne |
|---|---|
| 1–3 | açılış: yükleme, sponsor logoları, giriş animasyonu |
| 4 | ana menü |
| 5–108 | savaş alanı arka planları (104 kare) |
| 109 | kamp / kasaba (`TOWN_SCREEN`) |
| 110 | dünya haritası (`WORLD_MAP`) |
| 111 | savaşa hazırlık (`SPLASH_SCREEN`) |
| 112 | kayıt yükleme (`GAME_LOAD`) |
| 113 | oyun bitti (`GAME_OVER`) |
| 114 | zafer (`VICTORY`) |
| 115 | korsan kopya uyarısı (`STOLEN`) |
| 116 | öğretici (`TUTORIAL`) |

### Dışa aktarılan semboller (oyunun kodla çağırdığı)

`Ammun`, `Amount window`, `Arrow`, `ArrowShower`, `ArrowWall`, `BalanceAnim`, `BansheeCryAnim`, `BarnUnit`, `BarracksUnit`, `BarracksUnit - tutorial`, `Barrel`, `BarrierAnim`, `BigStone_1`, `BigStone_2`, `BlackSquare`, `Blood_1`, `Blood_2`, `Blow 3x3`, `Blow 5x5`, `Bush_1`, `Bush_2`, `Bush_3`, `Bush_4`, `Choose Active Skill`, `Choose Aura Skill`, `Choose Nation`, `Choose Skill`, `Cities`, `Crate_1`, `Crate_2`, `DummyHorseman`, `DummyHuman`, `FlyCritDamage`, `FlyDamage`, `FlyHeal`, `FlyMiss`, `GrenSymb`, `Grenade`, `Head_on_spear`, `HealAnim`, `Horseman`, `Horseman_Player`, `Human`, `Human_Player`, `ICON Equipment`, `ICON Inventory`, `ICON Mouse`, `Lantern`, `LifeLeechAnim`, `LightningAnim`, `MouseHint`, `Position mark`, `RIP_1`, `RIP_2`, `RageAnim`, `RiseAnim`, `Screen`, `SelectBorder`, `Sign_1`, `Sign_2`, `Sign_3`, `SkullTower`, `SoulDrainAnim`, `StarsAnim`, `Sword_in_ground_1`, `Sword_in_ground_2`, `TreeBroken_1`, `Tree_1`, `Tree_10`, `Tree_11`, `Tree_12`, `Tree_2`, `Tree_3`, `Tree_4`, `Tree_5`, `Tree_6`, `Tree_7`, `Tree_8`, `Tree_9`, `TutorialBattle`, `UnholyBreathAnim`, `VenomCluodAnim`, `Well_1`, `Willow_1`, `Willow_2`, `WorldMap`, `slash.wav`

### Sesler

Hepsi kısa ses efekti; müzik yok.

| Kimlik | Ad | Süre | Biçim | Nerede çalıyor |
|---|---|---|---|---|
| 990 |  | 1.4 sn | MP3 11025 Hz mono | Human.body / shield / kare 12; Horseman.body / shield / kare 12 |
| 991 |  | 0.8 sn | MP3 11025 Hz mono | Human.body / 2H_sword / kare 171; Horseman.body / 2H_sword / kare 79 |
| 995 |  | 1.8 sn | MP3 11025 Hz mono | Human.body / 2H_axe / kare 362; Horseman.body / 2H_axe / kare 120 |
| 996 |  | 1.5 sn | MP3 11025 Hz mono | Human.body / dual / kare 535; Human.body / dual / kare 549; Human.body / katana / kare 1567 |
| 998 |  | 0.8 sn | MP3 11025 Hz mono | Human.body / spear / kare 837; Horseman.body / spear / kare 146 |
| 1008 |  | 0.5 sn | MP3 11025 Hz mono | Human.body / bow / kare 995; Human.body / crossbow / kare 1183; Horseman.body / bow / kare 187; Horseman.body / bow_2 / kare 302 |
| 1009 |  | 0.4 sn | MP3 11025 Hz mono | Human.body / dagger / kare 1446; Human.body / fists / kare 1867; Human.body / fists / kare 1877 |
| 1027 |  | 0.4 sn | MP3 11025 Hz mono | Human.body / staff / kare 1686 |
| 1028 |  | 0.7 sn | MP3 11025 Hz mono | Human.body / staff / kare 1702 |
| 1030 |  | 0.5 sn | MP3 11025 Hz mono | Human.body / throwing / kare 1900; Horseman.body / crossbow / kare 364 |
| 1031 |  | 0.9 sn | MP3 11025 Hz mono | Human.body / die_ranged / kare 2386 |
| 1032 |  | 0.8 sn | MP3 11025 Hz mono | Human.body / die_twohanded / kare 2426 |
| 1033 |  | 1.0 sn | MP3 11025 Hz mono | Human.body / die_onehanded / kare 2476 |
| 1056 |  | 1.4 sn | MP3 11025 Hz mono | Horseman.body / die_horse / kare 1071 |
| 1060 |  | 2.5 sn | MP3 11025 Hz mono | Grenade / blow / kare 2 |
| 1743 | slash.wav | 0.6 sn | MP3 11025 Hz mono | kodla çalınır |

### Resimler

| Kimlik | Boyut | Not |
|---|---|---|
| 1789 | 70×71 |  |
| 1790 | 800×200 | savaş alanı zemin dokusu |
| 1845 | 800×200 | savaş alanı zemin dokusu |
| 1852 | 800×200 | savaş alanı zemin dokusu |
| 1859 | 800×200 | savaş alanı zemin dokusu |
| 1870 | 800×200 | savaş alanı zemin dokusu |
| 1875 | 800×200 | savaş alanı zemin dokusu |
| 2163 | 800×200 | savaş alanı zemin dokusu |
| 2192 | 800×200 | savaş alanı zemin dokusu |
| 2199 | 800×200 | savaş alanı zemin dokusu |
| 2207 | 800×200 | savaş alanı zemin dokusu |
| 2210 | 800×200 | savaş alanı zemin dokusu |
| 2214 | 800×200 | savaş alanı zemin dokusu |
| 2218 | 800×200 | savaş alanı zemin dokusu |
| 2221 | 800×200 | savaş alanı zemin dokusu |
| 2226 | 800×200 | savaş alanı zemin dokusu |
| 2240 | 800×200 | savaş alanı zemin dokusu |
| 2243 | 800×200 | savaş alanı zemin dokusu |
| 2248 | 800×200 | savaş alanı zemin dokusu |
| 2251 | 800×200 | savaş alanı zemin dokusu |
| 2353 | 800×200 | savaş alanı zemin dokusu |
| 2365 | 800×200 | savaş alanı zemin dokusu |
| 2382 | 800×200 | savaş alanı zemin dokusu |
| 2387 | 800×200 | savaş alanı zemin dokusu |

### Yazı tipleri (aktarılmayacak)

| Kimlik | Ad | Biçem | Gömülü glif |
|---|---|---|---|
| 45 | Arial | kalın | 10 |
| 77 | _sans | normal | yok (sistem yazı tipi) |
| 222 | _sans | normal | yok (sistem yazı tipi) |
| 224 | _sans | kalın | 27 |
| 350 | Times New Roman | kalın, italik | yok (sistem yazı tipi) |
| 353 | Times New Roman | normal | 44 |
| 461 | _serif | normal | yok (sistem yazı tipi) |
| 482 | Monotype Corsiva | kalın | 32 |
| 1702 | _serif | kalın | yok (sistem yazı tipi) |
| 1964 | Book Antiqua | kalın | 54 |
| 2043 | Bookman Old Style | kalın | 50 |
| 2298 | Book Antiqua | kalın, italik | 11 |
| 2339 | _sans | kalın, italik | yok (sistem yazı tipi) |
| 2400 | _serif | kalın, italik | yok (sistem yazı tipi) |
| 2417 | Monotype Corsiva | normal | 114 |
| 3083 | Century Gothic | kalın | 29 |

### Oyun kodunun sınıfları

`ActiveSkillChooser`, `Armor`, `Arrow`, `ArrowStorm`, `Aura`, `AuraSkillChooser`, `BarnIcon`, `BarracksIcon`, `Cage`, `Cities`, `Creature`, `DamageData`, `Enchant`, `EquipmentIcon`, `Grenade`, `Hero`, `Horse`, `Item`, `ItemInfo`, `MochiAd`, `MouseHint`, `MovieDummy`, `NationChooser`, `PassiveSkillChooser`, `Player`, `Projectile`, `Quest`, `Rune`, `Screen`, `SelectBorder`, `Skill`, `SkillChooser`, `Soldier`, `Status`, `StoreIcon`, `Town`, `Tree`, `Tutorial`, `Unit`, `UnitInfo`, `Weapon`, `WeaponClass`, `WorldMap`

## Ek: oyunlardaki sabit yazılar

Ekranlarda çizili İngilizce yazılar (çeviri için). Yazı alanlarının başlangıç değerleri ayrıca listelenir.

### Feudalism

| Kimlik | Yazı |
|---|---|
| 160 | Hold Position [Home] / Makes the selected soldiers  / to stay at current position. |
| 161 | Swap weapons [PageUp] / Switches to ranged and  / back. Some units have no  / weapon to swap. |
| 162 | Small potion / Heals 50 HP |
| 163 | Medium potion / Heals 300 HP |
| 164 | Large potion / Completely heals hero |
| 165 | Small heal scroll / Heals all your unit for 1/3  / of their max HP. |
| 166 | Large heal scroll / Heals all your unit for 2/3  / of their max HP. |
| 167 | Scroll of rage / Makes your units attack  / much faster. |
| 168 | Arrow Shower / An area attack, which can  / hurt friendly units too. |
| 169 | Arrow Wall / An attack which shots  / several crossbow bolts to  / selected positions. |
| 901 | Scotland |
| 908 | England |
| 1039 | TUTORIAL |
| 1040 | NEW GAME |
| 1041 | RESUME GAME |
| 1042 | OPTIONS |
| 1043 | CONTROLS |
| 1044 | MORE GAMES |
| 1045 | PUT THIS GAME ON YOUR SITE |
| 1046 | E-MAIL ME |
| 1140 | Choose your hero |
| 1141 | START JOURNEY |
| 1154 | Medium / quality |
| 1155 | High / quality |
| 1156 | Low / quality |
| 1159 | Highlight troops |
| 1160 | Show help tips |
| 1162 | Save slot 1 |
| 1164 | Load |
| 1167 | Save slot 2 |
| 1169 | Save slot 3 |
| 1171 | Auto save |
| 1175 | Load game... |
| 1176 | ...which slot? |
| 1484 | Press a button |
| 1487 | Move up: |
| 1488 | Move down: |
| 1489 | Move left: |
| 1490 | Move right: |
| 1491 | Attack: |
| 1492 | Swap weapons: |
| 1493 | SAVE AND EXIT |
| 1606 | Your items: |
| 1607 | Merchant's items: |
| 1608 | Drag'n'drop items to buy or sell them for 1/2 of their price |
| 1609 | Don't ask amount, just sell all |
| 1629 | Click on a potion or scroll to buy it. Shift-click to by 5 potions per time. |
| 1631 | Reserve troops - they will fight, when someone from 1st or 2nd line will die |
| 1632 | 2nd line |
| 1633 | 1st line |
| 1644 | Troops available to recruit |
| 1757 | Piercing |
| 1759 | Increases hit chance by  / 10% |
| 1761 | Bloody |
| 1762 | Increases critical strike  / chance by 10% |
| 1763 | Bleeding |
| 1764 | Increases critical strike  / chance by 20% |
| 1766 | of Massacre |
| 1767 | Increases critical strike  / chance by 10% and  / damage by 0-20 |
| 1769 | Increases critical strike  / chance by 30%, but  / reduces dodge chance  / by 20% of its value |
| 1770 | Creeping |
| 1772 | Increases damage by  / 20 points and HP by  / 20% |
| 1773 | Strong |
| 1775 | Increases critical strike  / chance by 30%, but  / decreases damage by 5  / points and HP by 50% |
| 1776 | Cursed |
| 1778 | Increases damage by  / 20-70, but decreases  / HP by 30% and defence  / by 50% |
| 1779 | Undead |
| 1781 | Increases damage by  / 100-300 and defence  / by 150%, but decreases  / HP by 90% and dodge  / chance by 99% |
| 1782 | ~~Unholy~~ |
| 1784 | Increases damage by  / 20-50, HP by 20%,  / defence by 10% and  / dodge chance by 2% |
| 1785 | Great |
| 1787 | Increases damage by  / 50-350, but decreases  / HP and defence by  / 50%, and dodge chance  / by 20% |
| 1788 | Glorious |
| 1789 | of Sacrifice |
| 1791 | Increases HP by 100%  / and defence by 20%,  / and dodge chance by  / 4%, but decreases hit  / chance by 15% |
| 1792 | of Compassion |
| 1794 | of Valor |
| 1795 | Increases damage by  / 50-100, defence by  / 50%, but decreases  / dodge chance by 70% |
| 1797 | Immortal |
| 1798 | Increases HP by 200%  / and defence by 100%,  / but decreases damage  / by 5-15, hit chance by  / 20% critical strike  / chance by 10% |
| 1800 | ~~Mysterious |
| 1801 | Increases hit chance by  / 100%, critical strike  / chance by 90% and  / damage by 0-1000, but  / sets defence and dodge  / chance to 0 and  / decreases HP by 80% |
| 1802 | of Death~~ |
| 1804 | Marksman's |
| 1805 | Increases hit chance by  / 5% |
| 1807 | Lucky |
| 1808 | Increases hit chance by  / 20%, crical strike  / chance by 20% and  / damage by 0-20 |
| 1810 | Sleeping |
| 1811 | Increases damage by 0- / 50, defence and HP by  / 30%, but decreases hit  / chance by 5%, crical  / strike chance by 5%  / and dodge chance by  / 10% |
| 1813 | Suffering |
| 1814 | Increases damage by  / 50, hit and crical strike  / chance by 30%, dodge  / chance by 2%, but  / decreases  defence and  / HP by 30% |
| 1816 | Blind |
| 1817 | Increases damage by  / 30-80, crical strike  / chance by 20% and  / defence by 50%, but  / decreases  hit chance  / by 10% |
| 1819 | Increases damage by  / 60-160, crical strike  / chance by 40% and  / defence by 80%, but  / decreases  hit chance  / by 30% and dodge  / chance by 60% |
| 1820 | of Rage |
| 1822 | Breaking |
| 1823 | Increases crical strike  / chance by 70% and hit  / chance by 10% |
| 1825 | Crushing |
| 1826 | Increases damage by  / 100-300, but decreases  / crical strike chance by  / 90% |
| 1828 | ~~Saint |
| 1829 | Increases defence and  / HP by 200%, but  / decreases hit chance by  / 40% and dodge chance  / by 90% |
| 1830 | of Divine Light~~ |
| 1846 | Save |
| 1867 | No, maybe something else? |
| 1877 | Sell your horse |
| 1880 | Click on a horse to buy it. Notice, that some kind of weapons can't be used from a horse |
| 1891 | Okay, let's fight |
| 1894 | ... hmm Okay |
| 1984 | Hero level: |
| 1985 | Gold gained: |
| 1986 | Max Hero damage: |
| 1987 | Max Hero HP: |
| 2009 | Prepare |
| 2010 | Battle... |
| 2011 | for |
| 2020 | Load game? |
| 2022 | MAIN MENU |
| 2029 | Continue |
| 2033 | Victory! |
| 2034 | Experience: |
| 2035 | Gold: |
| 2037 | Items obtained: |

Yazı alanlarının başlangıç değerleri (Feudalism): oyun bunların çoğunu çalışırken değiştirir; burada tasarımdaki örnek değerleri var.

| Kimlik | Yazı |
|---|---|
| 46 | miss |
| 50 | 100% |
| 157 | 2222/2222 |
| 177 | 9999/9999 |
| 236 | 999 |
| 237 | 999 |
| 238 | 999 |
| 239 | 999 |
| 240 | 999 |
| 241 | 999 |
| 793 | 3000 |
| 799 | OK |
| 802 | Cancel |
| 805 | miss |
| 890 | RIP |
| 1020 | v1.041k |
| 1052 | Strength |
| 1053 | Dexterity |
| 1054 | Constitution |
| 1055 | Intelligence |
| 1056 | Sword |
| 1057 | Axe |
| 1058 | Mace |
| 1059 | Staff |
| 1060 | Far East Weapons |
| 1061 | Dagger |
| 1062 | Spear |
| 1063 | Dual Weapons |
| 1064 | Bow |
| 1065 | Crossbow |
| 1066 | Throwing |
| 1067 | Art of War |
| 1068 | Patriotism |
| 1069 | 999 |
| 1070 | 999 |
| 1071 | 999 |
| 1072 | 999 |
| 1073 | 999 |
| 1074 | 999 |
| 1075 | 999 |
| 1076 | 999 |
| 1077 | 999 |
| 1078 | 999 |
| 1079 | 999 |
| 1080 | 999 |
| 1081 | 999 |
| 1082 | 999 |
| 1083 | 999 |
| 1084 | 999 |
| 1085 | 999 |
| 1102 | Free points |
| 1103 | 999 |
| 1147 | Back |
| 1179 | Hello, wanderer! I'll guide you through the  / basics and teach how to survive in this  / world. |
| 1181 | Next |
| 1240 | This is the screen of your city. There are  / several buildings: |
| 1242 | City Hall. Here you can view your hero  / stats, ask for a quest, or declare war on the  / town. |
| 1244 | Forge. Here you can buy and sell weapons  / and armor. |
| 1246 | Barracks. Here you can recruit and disband  / your troops. |
| 1248 | Temple. Here you can buy healing potions  / and scrolls. |
| 1250 | Also, there're a barn and a harbor in some  / towns. |
| 1254 | Wanderburg |
| 1256 | Endem |
| 1258 | Hoffen |
| 1260 | Braunburg |
| 1262 | Gerlitz |
| 1264 | Sturmburg |
| 1266 | Jana |
| 1268 | Konstanz |
| 1270 | Trapezus |
| 1272 | Lutetia |
| 1274 | Arretium |
| 1276 | Alexandria |
| 1278 | Lacrimosa |
| 1280 | Ravenna |
| 1282 | Carthage |
| 1284 | Caesarea |
| 1286 | Grouzeno |
| 1288 | Medvedevo |
| 1290 | Dobrov |
| 1292 | Dubkee |
| 1294 | Ra-Gorod |
| 1296 | Losevo |
| 1298 | Dalnevodye |
| 1300 | Echigo |
| 1303 | Nagoya |
| 1305 | Fukushima |
| 1307 | Omi |
| 1309 | Kozuke |
| 1311 | Suo |
| 1313 | Matsuyama |
| 1315 | Izumo |
| 1318 | Zlatograd |
| 1324 | Once you leave a town, you'll find yourself  / on the world map. |
| 1326 | Click at the map to move your hero. |
| 1455 | 120/120 |
| 1464 | This is battle screen. Here you'll fight for  / the glory and gold. |
| 1466 | Control your hero with WASD or directional  / keys and attack with Space or Numpad 0 |
| 1468 | These guys are your troops. You have no  / need to order them. They're wise enough to  / fight on their own. |
| 1471 | But if you want them to stop or swap their  / weapons (if they have a weapon to swap  / to), use these buttons. |
| 1473 | The enemies start at the left, at these  / positions. |
| 1476 | If you or your soldiers will get injured, click  / these buttons (or hotkeys 1-6) to use  / healing potions and scrolls. |
| 1478 | That's all I wanted to tell. Now go, and start  / your long journey to the world domination!MWA HA HA HA HAaaaa!!!! |
| 1518 | The trade camp of Trapezus |
| 1522 | City HallHere you can view  / your hero stats, ask  / for a quest, or  / declare war. |
| 1524 | ForgeHere you can buy  / and sell weapons  / and armor. |
| 1526 | BarracksHere you can recruit  / and disbandyour troops. |
| 1528 | TempleHere you can buy  / healing potionsand scrolls. |
| 1530 | HarborYou can board a  / ship there totravel by sea. |
| 1532 | BarnBuy and sell horses  / here. |
| 1534 | ExitExit to the world  / map. |
| 1541 | Inventory |
| 1547 | 999 |
| 1604 | 3000 gold |
| 1605 | Money: |
| 1619 | Scroll of Bloody Rage |
| 1620 | Makes your units attack much faster. Units with low attack speed gain a huge bunus, perhaps fast attacking units get a very small bonus. |
| 1621 | 3000 gold |
| 1622 | Money: |
| 1623 | 999 |
| 1624 | 999 |
| 1625 | 999 |
| 1626 | 999 |
| 1627 | 999 |
| 1628 | 999 |
| 1636 | 3000 gold |
| 1637 | Money: |
| 1650 | Strength |
| 1651 | Dexterity |
| 1652 | Constitution |
| 1653 | Intelligence |
| 1654 | Sword |
| 1655 | Axe |
| 1656 | Mace |
| 1657 | Staff |
| 1658 | Far East Weapons |
| 1659 | Dagger |
| 1660 | Spear |
| 1661 | Dual Weapons |
| 1662 | Bow |
| 1663 | Crossbow |
| 1664 | Throwing |
| 1665 | Art of War |
| 1666 | Patriotism |
| 1667 | 999 |
| 1668 | 999 |
| 1669 | 999 |
| 1670 | 999 |
| 1671 | 999 |
| 1672 | 999 |
| 1673 | 999 |
| 1674 | 999 |
| 1675 | 999 |
| 1676 | 999 |
| 1677 | 999 |
| 1678 | 999 |
| 1679 | 999 |
| 1680 | 999 |
| 1681 | 999 |
| 1682 | 999 |
| 1683 | 999 |
| 1700 | Free points |
| 1701 | 999 |
| 1702 | 999 |
| 1753 | Michael KlobovLevel 49 |
| 1756 | Full Plate Of Holy Light |
| 1838 | View your hero's stats |
| 1839 | Try to capture this town |
| 1840 | Ask for a quest |
| 1872 | Michael KlobovLevel 49 |
| 1878 | 3000 gold |
| 1879 | Money: |
| 1883 | Yes! |
| 1885 | No.. |
| 1888 | You don't rule our city!We don't want to sell our troops to strangers!(You need to capture this town to recruit troops  / here) |
| 1890 | What the... ??Enemy himself has come at our gates! We'll  / punish you for all our captured cities.To arms, my men, to arms!! |
| 1893 | Sire! This town is already ours!We can't kill our own people for nothing! |
| 1896 | Are you sure want to fight us?! |
| 1899 | The trade camp of Lutetia |
| 1903 | The trade camp of Arretium |
| 1905 | The trade camp of Ravenna |
| 1906 | The trade camp of Lacrimosa |
| 1908 | The city of Caesaria |
| 1909 | The Great city of Carthage |
| 1910 | The Glorious city of Alexandria |
| 1911 | Capital of the Great Trade Republic |
| 1916 | The village of Jana |
| 1917 | The small town of Konstanz |
| 1918 | The small town of Gerlitz |
| 1919 | The town of Sturmburg |
| 1920 | Order's south keep |
| 1922 | The village of Hoffen |
| 1923 | The village of Endem |
| 1924 | The Great city of Braunburg |
| 1925 | Order's major city |
| 1926 | The Glorious city of Wanderburg |
| 1927 | The Capital of Order of Holy Cross |
| 1932 | The small village of Dubkee |
| 1933 | The village of Dalnevodye |
| 1934 | The village of Losevo |
| 1935 | The town of Dobrov |
| 1936 | The city of Zlatograd |
| 1937 | Forest Lands' Trade Center |
| 1938 | The village of Medvedevo |
| 1939 | The small village of Grouzeno |
| 1940 | All Heroes' Motherland |
| 1941 | The Gloriuos city of Ra-Gorod |
| 1942 | The Capital of Forest Lands |
| 1948 | The small village of Omi |
| 1949 | The small village of Kozuke |
| 1950 | The small town of Matsuyama |
| 1951 | The village of Fukushima |
| 1952 | The city of Izumo |
| 1953 | Far East Empire's Trade Center |
| 1954 | The village of Suo |
| 1955 | The Glorious city of Nagoya |
| 1956 | The Capital of Far East Empire |
| 1957 | The small village of Echigo |
| 1958 | Black Samurai Academy |
| 1988 | 0 |
| 1989 | 0 |
| 1990 | 0 |
| 1991 | 0 |
| 1996 | Click anywhere at the map  / to move your hero. |
| 1997 | Show help tips. |
| 2036 | Sword Of Storms,Full Plate Of Holy Light x4, |
| 2038 | 1500/2000 |
| 2039 | 15000 gp. |
| 2054 | This is battle screen. Here you'll fight for  / the glory and gold. |
| 2055 | This is your hero. Control him with WASD  / or directional keys and attack with Space or  / Numpad 0. |
| 2056 | These guys are your troops. You have no  / need to order them. They're wise enough to  / fight on their own. |
| 2057 | But if you want them to stop or swap their  / weapons (if they have a weapon to swap  / to), use these buttons. |
| 2058 | The enemies start at the right, at these  / positions. |
| 2059 | If you or your soldiers will get injured, click  / these buttons (or hotkeys 1-6) to use  / healing potions and scrolls. |
| 2060 | If there're some bowmen in your reserve  / you can oder them to attack an area by  / klicking this button. Attack will be the most  / powerful when there're 7 or more bowmen  / in reserve. |
| 2061 | If there're some crossbowmen in your  / reserve you can oder them to fire a line of  / arrows by klicking this button. Attack will  / be the most powerful when there're 5 or  / more crossbowmen in reserve. / |
| 2063 | That's all you need to know. Good luck.  / Gain some levels by killing rogues and then  / recruit a huge army and try to capture a  / small village to gain acces to better troops. |

### Feudalism 2

| Kimlik | Yazı |
|---|---|
| 354 | Hold Position / Makes the selected soldiers  / to stay at current position. |
| 355 | Swap weapons / Switches to ranged and  / back. Some units have no  / weapon to swap. |
| 356 | Small potion [Z key] / Heals 40 HP |
| 357 | Medium potion [X key] / Heals 300 HP |
| 358 | Large potion / Completely heals hero |
| 359 | Small heal scroll / Heals all your unit for 1/3  / of their max HP. |
| 360 | Large heal scroll / Heals all your unit for 2/3  / of their max HP. |
| 361 | Scroll of rage / Makes your units attack  / much faster. |
| 362 | Arrow Shower / An area attack, which can  / hurt friendly units too. |
| 363 | Arrow Wall / An attack which shots  / several crossbow bolts to  / selected positions. |
| 483 | Active Skills |
| 484 | Aura Skills |
| 1714 | Scotland |
| 1721 | England |
| 1965 | NEW GAME |
| 1966 | RESUME GAME |
| 1967 | OPTIONS |
| 1968 | CONTROLS |
| 1969 | MORE GAMES |
| 1970 | PUT THIS GAME ON YOUR SITE |
| 1971 | E-MAIL ME |
| 1972 | Play Feudalism 1 |
| 2027 | Choose your hero |
| 2028 | START JOURNEY |
| 2029 | BACK |
| 2044 | Medium / quality |
| 2045 | High / quality |
| 2046 | Low / quality |
| 2049 | Highlight troops |
| 2050 | Show help tips |
| 2051 | Save slot 1 |
| 2053 | Load |
| 2057 | Save slot 2 |
| 2059 | Save slot 3 |
| 2061 | Auto save |
| 2065 | Load game... |
| 2066 | ...which slot? |
| 2299 | Press a button |
| 2302 | Move up: |
| 2303 | Move down: |
| 2304 | Move left: |
| 2305 | Move right: |
| 2306 | Attack: |
| 2307 | Swap weapons: |
| 2308 | SAVE AND EXIT |
| 2324 | Special moves |
| 2325 | Passive skills |
| 2326 | Aura skills |
| 2327 | Nation |
| 2328 | Gender |
| 2329 | Name: |
| 2336 | Choose Difficultly |
| 2337 | EASY |
| 2338 | NORMAL |
| 2570 | Your items: |
| 2571 | Merchant's items: |
| 2572 | Drag'n'drop items to buy or sell them for 1/2 of their price |
| 2573 | Don't ask amount, just sell all |
| 2576 | SELL ALL |
| 2584 | Refine level |
| 2587 | Rune to enchant |
| 2588 | Refine! |
| 2589 | Enchant rune! |
| 2612 | Click on a potion or scroll to buy it. Shift-click to by 5 potions per time. |
| 2616 | Reserve troops - they will fight, when someone from 1st or 2nd line will die |
| 2617 | 2nd line |
| 2618 | 1st line |
| 2627 | Troops available to recruit |
| 2781 | Save |
| 2804 | No, maybe something else? |
| 2814 | Sell your horse |
| 2817 | Click on a horse to buy it. Notice, that some kind of weapons can't be used from a horse |
| 2818 | Also remember that only bow, crossbow and throwing weapons' special  / moves can be performad from a horse. You can't use any melee  / weapons' special moves when mounted. And it's impossipbe to fight  / with dual wepons, daggers, katars or staffs from a horse. |
| 2830 | Okay, let's fight |
| 2833 | Duel |
| 2835 | Fight with army |
| 2837 | Maybe later... |
| 2892 | Special moves |
| 2896 | Passive skills |
| 2897 | Auras |
| 2920 | View all skill descriptions (opens in a new window) |
| 2997 | South Desert |
| 3001 | Great Trade Republic |
| 3005 | Forest Lands |
| 3009 | Black |
| 3010 | Horde's |
| 3011 | Lands |
| 3015 | Order of Holy |
| 3016 | Cross |
| 3020 | Far East |
| 3021 | Empire |
| 3063 | CONTINUE PLAYING |
| 3065 | MAIN MENU |
| 3084 | Prepare |
| 3085 | Battle... |
| 3086 | for |
| 3095 | Load game? |
| 3096 | MAIN MENU |
| 3103 | Continue |
| 3107 | Victory! |
| 3108 | Experience: |
| 3109 | Gold: |
| 3111 | Items obtained: |
| 3139 | START GAME |

Yazı alanlarının başlangıç değerleri (Feudalism 2): oyun bunların çoğunu çalışırken değiştirir; burada tasarımdaki örnek değerleri var.

| Kimlik | Yazı |
|---|---|
| 46 | miss |
| 223 | Character throws his dagger at enemy, then jumps, catches the dagger in the air and hits the ground. Flying dagger hits the enemy 3 times, each hit deals 50+10*SkillLv% damage. The ground hit damages all enemies in 5x5 area around the character for 50+20*SkillLv%. |
| 225 | Horsemen Defense Mastery |
| 226 | Passive skill |
| 242 | SP cost: 100 |
| 251 | Horseman Twohanded Sword |
| 252 | Two Handed Sword |
| 253 | Damage: 50-93Critical rate: 10Attack speed +5%Requires 49 STRPrice: 580 |
| 257 | Legionary |
| 258 | STR: 32DEX: 10CON: 19SPR: 10Price: 100000 |
| 265 | 99 |
| 338 | HP: 9999 SP: 9999Defense: 500 Dodge: 200Damage: 200-300 (100% crit)Attack speed: 4.88Sword mastery: 73 |
| 340 | Strength is a very very very important stat. It is required for using loooots of weapons and armor. You should master it to the max XD |
| 351 | 2222/2222 |
| 462 | 9999/9999 |
| 475 | 9999/9999 |
| 479 | 999 |
| 480 | 999 |
| 490 | 1 |
| 492 | 2 |
| 493 | 3 |
| 494 | 4 |
| 495 | 5 |
| 496 | 6 |
| 1458 | 3000 |
| 1464 | OK |
| 1467 | Cancel |
| 1470 | miss |
| 1624 | miss |
| 1627 | miss |
| 1703 | RIP |
| 1777 | Click anywhere to skip |
| 1949 | Copyright Vitaly Zaborov 2008 |
| 1950 | v1.02 |
| 2018 | ? |
| 2019 | Customize |
| 2021 | ? |
| 2022 | Custom Characters Only Available  / from ArcadeTown.com.  Click Here  / to create your own character. |
| 2037 | Back |
| 2069 | Hello, wanderer! I'll guide you through the  / basics and teach how to survive in this  / world. |
| 2071 | Next |
| 2130 | This is the screen of your city. There are  / several buildings: |
| 2132 | City Hall. Here you can view your hero  / stats, ask for a quest, or declare war on the  / town. |
| 2134 | Forge. Here you can buy and sell weapons  / and armor. |
| 2136 | Barracks. Here you can recruit and disband  / your troops. |
| 2138 | Temple. Here you can buy healing potions  / and scrolls. |
| 2140 | Also, there're a barn and a harbor in some  / towns. |
| 2147 | Once you leave a town, you'll find yourself  / on the world map. |
| 2149 | Click at the map to move your hero. |
| 2269 | 120/120 |
| 2279 | This is battle screen. Here you'll fight for  / the glory and gold. |
| 2281 | Control your hero with WASD or directional  / keys and attack with Space or Numpad 0 |
| 2283 | These guys are your troops. You have no  / need to order them. They're wise enough to  / fight on their own. |
| 2286 | But if you want them to stop or swap their  / weapons (if they have a weapon to swap  / to), use these buttons. |
| 2288 | The enemies start at the left, at these  / positions. |
| 2291 | If you or your soldiers will get injured, click  / these buttons (or hotkeys 1-6) to use  / healing potions and scrolls. |
| 2293 | That's all I wanted to tell. Now go, and start  / your long journey to the world domination!MWA HA HA HA HAaaaa!!!! |
| 2316 | Male |
| 2318 | Female |
| 2330 | Player |
| 2340 | No army size limits,  / stats does not  / depend on level, max  / stat is 200, your units  / have more HP, no  / attack can hit hero  / for more than 90% of  / his max HP, weapon  / upgrade chances are  / boosted. |
| 2341 | Max army size is 30,  / max stat is 100 and  / depends on level,  / random battles  / happen more often,  / weapon upgrade  / chances are normal. |
| 2376 | T i f l i s |
| 2401 | City HallHere you can view  / your hero stats, ask  / for a quest, or  / declare war. |
| 2403 | ForgeUpgrade your  / weapons here |
| 2405 | BarracksHere you can recruit  / and disbandyour troops. |
| 2407 | TempleHere you can buy  / healing potionsand scrolls. |
| 2409 | HarborYou can board a  / ship there totravel by sea. |
| 2411 | BarnBuy and sell horses  / here. |
| 2413 | ExitExit to the world  / map. |
| 2415 | Marketplace.Buy and sell items  / here |
| 2418 | Glorious city of Caesarea, capital of Great Trade Republic |
| 2423 | Inventory |
| 2426 | Skills |
| 2432 | 999 |
| 2569 | 3000 gold |
| 2582 | Money: 3000 gold |
| 2585 | 10 |
| 2586 | Success chance: 100%Price: 100000 gold |
| 2599 | Note: each point of weapon  / refine adds 3 points to base  / damage and increases variable  / part of damage by 10% / These bonuses are not shown  / in weapon stats / |
| 2608 | 3000 gold |
| 2609 | Money: |
| 2610 | 999 |
| 2611 | 999 |
| 2613 | You don't rule our city! So we won't allow to  / recruit troops here!(You have to capture this town to recruit troops) |
| 2621 | 3000 gold |
| 2622 | Money: |
| 2634 | Michael KlobovLevel 49exp: 99999/10000000 |
| 2635 | 999 |
| 2768 | View your hero's stats |
| 2769 | Ask for a quest |
| 2772 | Try to capture this town |
| 2773 | Fight town  champion |
| 2809 | Michael KlobovLevel 49 |
| 2815 | 3000 gold |
| 2816 | Money: |
| 2822 | Yes! |
| 2824 | No.. |
| 2827 | You don't rule our city!We don't want to sell our troops to strangers!(You need to capture this town to recruit troops  / here) |
| 2829 | What the... ??Enemy himself has come at our gates! We'll  / punish you for all our captured cities.To arms, my men, to arms!! |
| 2831 | So, you are challenging me... intersting...Will it be a 1 vs 1 fight or you'll hide behind your  / soldiers' back? |
| 2839 | Are you sure want to fight us?! |
| 2846 | Strength |
| 2847 | Dexterity |
| 2848 | Constitution |
| 2849 | Spirit |
| 2850 | Sword |
| 2851 | Axe |
| 2852 | Mace |
| 2853 | Staff |
| 2854 | Far East Weapons |
| 2855 | Dagger |
| 2856 | Spear |
| 2857 | Dual Weapons |
| 2858 | Bow |
| 2859 | Crossbow |
| 2860 | Throwing |
| 2861 | 999 |
| 2862 | 999 |
| 2863 | 999 |
| 2864 | 999 |
| 2865 | 999 |
| 2866 | 999 |
| 2867 | 999 |
| 2868 | 999 |
| 2869 | 999 |
| 2870 | 999 |
| 2871 | 999 |
| 2872 | 999 |
| 2873 | 999 |
| 2874 | 999 |
| 2875 | 999 |
| 2890 | Free points |
| 2891 | 999 |
| 2893 | Two handed sword skills |
| 2894 | Two handed axe and mace skills |
| 2895 | Crossbow skills |
| 2898 | Lv. 5 |
| 2900 | Lv. 5 |
| 2901 | Lv. 5 |
| 2902 | Lv. 5 |
| 2903 | Lv. 5 |
| 2904 | Lv. 5 |
| 2906 | Lv. 5 / |
| 2907 | Lv. 5 / |
| 2908 | Points left: / |
| 2909 | 50 |
| 2910 | Lv. 1 / |
| 2911 | Lv. 1 / |
| 2912 | Lv. 1 / |
| 2913 | Lv. 1 / |
| 2914 | Katar |
| 2915 | 999 |
| 2918 | ? |
| 3028 | Byzantium city |
| 3030 | Russian city |
| 3032 | Mongol city |
| 3034 | German village |
| 3036 | Japaneese village |
| 3039 | Arabian village |
| 3041 | Byzantium village |
| 3043 | Russian village |
| 3045 | German city |
| 3047 | Mongol village |
| 3049 | Japaneese city |
| 3051 | Arabian city |
| 3078 | Start battle! / |
| 3110 | Sword Of Storms,Full Plate Of Holy Light x4, |
| 3112 | 1500/2000 |
| 3113 | 15000 gp. |
| 3125 | If you see this message on any other site please  / contact developer by email: zaborov@mail.ru / If you're a webmaster and want to place Feudalism 2  / on your site please take the game from this link: / |
| 3126 | This version were probably  / stolen from ArmorGames.Com  / or AddictingGames.com |
| 3127 | ЭТУ ИГРУ СПЕРЛИ!!! |
| 3128 | it is absolutely free and the game is the same. |
| 3129 | And the last thing. If somehow happened that this message appears on  / ArmorGames.com or AddictingGames.com please contact me ASAP and I'll fix it  / as fast as I can. |
| 3130 | http://www.arcadetown.com/free_content/index.asp / |
| 3132 | The game is playable at ArcadeTown / |
| 3136 | Skip |
