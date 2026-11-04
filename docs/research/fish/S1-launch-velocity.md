# S1: Launch velocity: can a 4 cm, 0.4 g zebrafish reach takeoff speed?

Status: research note, 2026-11-04. Arithmetic: `docs/research/fish/S1_launch_velocity_calc.py`
(run it from the repository root; every number below that is not attributed to a source comes from it).

## Verdict first

**No. With the measured data available, a 0.4 g fish cannot take off from water into sustained
flight by speed alone. The shortfall is a factor of about 4 to 13 in speed (about 18 to 160 in
kinetic energy) for any wing proportioned like a real flying fish.**

- **Hardest number.** Give a 0.4 g fish flying-fish wing loading (Fish 1990 genus fits,
  extrapolated) and its takeoff speed is **2.4 to 7.2 m/s** across genera and CL_max of 0.6 to 1.2.
  The best adult zebrafish speed I could find measured is **0.56 m/s** (Ucrit, Plaut 2000, a
  *prolonged* speed, not a burst). That gives a ratio of **0.08 to 0.23**. The most favourable
  combination, the Danichthys fit with CL_max 1.2, needs 2.41 m/s. That is 4.3 times the measured
  speed and 60 body lengths per second at 4 cm.
- **The only grid cell where the ratio exceeds 1** is a massless wing of 24 cm span (6 times body
  length), aspect ratio 3, at CL_max 1.2: stall speed 0.53 m/s, ratio 1.06. Any wing with an areal
  density of at least about 0.5 mg/cm² pushes it below 1 (0.56 / 0.59 = 0.95). Even if it were
  reached, leaving the water at stall speed buys a hop: a ballistic apex of 0.4 to 1.2 cm and a
  glide of 1 to 6 cm at an assumed L/D of 2 to 5. That is not flight.
- **The largest unknown is the adult zebrafish peak escape (burst) speed.** I did not find it
  measured in any source I could reach. It is `unknown` here. Ucrit is a lower bound on it. I also
  checked an inference-grade stretch value: 1.52 m/s, the larval length-specific escape speed
  (about 38 BL/s) applied to a 4 cm adult. It still gives a ratio of only **0.21 to 0.63** against
  flying-fish-proportioned wings.

## Honesty and access notes

- This session's network policy blocked every journal host (journals.biologists.com,
  cob.silverchair.com, pmc.ncbi.nlm.nih.gov, biorxiv.org, archive.org, the author-hosted Fish 1990
  PDF). Only web search worked. **So, apart from Fish 1990, every source below is at read-level
  `search-summary` or worse.** A search summary is a tool's paraphrase of snippets, not my reading
  of the paper. Every number from one should be re-checked against the full text before anyone
  relies on it.
- Fish 1990 values come from this repository's own records (`data/research/flying-fish-source-cards.json`
  card FISH-1990, read-level `full-text`; `data/fish-controls/fish1990_tables.json`, transcribed
  from page images). That reading was done in an earlier session. I did not re-read the paper in
  this one.
- "**Measured**" means the authors' number. "**Inference**" means my arithmetic or reasoning.
  "**Assumed**" means a parameter I chose that no retrieved source supplies.

## Sources and read-levels

| ID | Citation | Read-level | What I took from it |
|---|---|---|---|
| FISH-1990 | Fish FE 1990, Wing design and scaling of flying fish with regard to flight performance, *J Zool Lond* 221:391-403 | full-text (repo record from an earlier session; not re-read here) | WL fits (Table II), span/length fits (Table I), hypocaudal lobe 63.1 ± 0.5% of caudal area, smallest WL 11.7 N/m² (0.001 kg *Hirundichthys*, text). Taxi speed rising **10 → 16-20 m/s** (p.397), **relayed** by Fish from Shoulejkin 1929 et al., not Fish's own measurement |
| EDGERTON-BREDER-1941 | Edgerton HE, Breder CM 1941, High speed photographs of flying fishes in flight, *Zoologica* 26:311-314 | search-summary | Photographs of *Cypselurus californicus* leaving the water with the lower caudal lobe still immersed. No speed seen in the snippets: `unknown` from this source |
| MAKIGUCHI-2013 | Makiguchi Y et al., Take-off performance of flying fish *Cypselurus heterurus doederleini* measured with miniature acceleration data loggers, *Aquatic Biology* 18:105-111 (doi 10.3354/ab00494) | search-summary (abstract) | Aquarium study. Estimated water-exit speed 3.9-5.2 m/s, which the authors put at 38.7-51.5% of previously reported maximum swimming speeds. Stroke frequency 21.2 ± 4.6 Hz. Speeds are **estimated** from accelerometry |
| TAXI-BIORXIV | "Why does a flying fish taxi on sea surface before take-off? A hydrodynamic interpretation", bioRxiv 10.1101/765560 (authors not captured) | search-summary | **Model**, not a measurement: an 80 Hz tail beat gives 16.5 m/s taxi; 120 Hz is called "out of the physical limit". Relays a 50-70 strokes/s lower-lobe beat from older literature, and "~10 m/s swimming, 15-20 m/s glide" for a 0.3 m fish from a cited source |
| APS-2024 | "Flying fish taxiing on the water's surface", APS March Meeting 2024, abstract S27.13 | search-summary (abstract) | Tail beat 13.5 Hz while taxiing. About 2 N estimated as the minimum force to hold a 200 g fish above the surface, which is roughly its weight |
| VOESENEK-2019 | Voesenek CJ, Pieters RPM, Muijres FT, van Leeuwen JL 2019, Reorientation and propulsion in fast-starting zebrafish larvae: an inverse dynamics analysis, *J Exp Biol* 222:jeb203091 | search-summary | 5 dpf larvae, 4.2 ± 0.14 mm, five-camera high-speed video. **One example start peaked at 0.15 m/s** (about 36 BL/s, my division). Speed scales with start duration^-1.42. Peak forces not retrieved |
| MULLER-2004 | Müller UK, van Leeuwen JL 2004, Swimming of larval zebrafish: ontogeny of body waves and implications for locomotory development, *J Exp Biol* 207:853-868 | search-summary (partial abstract) + secondary | 2-21 dpf, high-speed video. "Up to 38 body lengths per second" appears only in a **secondary** citation (a Wageningen thesis). I could not confirm it in the abstract |
| BUDICK-2000 | Budick SA, O'Malley DM 2000, Locomotor repertoire of the larval zebrafish: swimming, turning and prey capture, *J Exp Biol* 203:2565-2579 | listing | 6-9 dpf escape and routine turns. **No escape peak velocity retrieved** |
| VISCOSITY-2012 | "Challenging zebrafish escape responses by increasing water viscosity", *J Exp Biol* (doi 10.1242/jeb.068957; PMID 22573764). Authors not confirmed | search-summary (abstract) | Maximum centre-of-mass velocity is in its Table 1, **values not retrieved**. Life stage not confirmed |
| PLAUT-2000 | Plaut I 2000, Effects of fin size on swimming performance, swimming behaviour and routine activity of zebrafish *Danio rerio*, *J Exp Biol* 203:813-820 (PMID 10648223) | search-summary (abstract) | **Adult Ucrit, wild type ≈ 56 cm/s = 15.5 SL/s** (N = 21, 28 °C, Brett-type tunnel). Long-finned fish 12.5 SL/s. The implied SL is ≈ 3.6 cm |
| PALSTRA-2010 | Palstra AP et al. 2010, Establishing zebrafish as a novel exercise model…, *PLoS ONE* 5:e14483 | search-summary | Adult **0.548 ± 0.007 m/s = 18.0 BL/s** (a Ucrit-type swim-tunnel speed; protocol not read) |
| FLUME-2018 | Open-source microcontroller flume for larval, juvenile and adult zebrafish (PMC6019105; authors not captured) | search-summary | Ucrit about 3 cm/s at 5 dpf, about 40-55 cm/s in adults |
| ZF-MUSCLE | Superfast excitation-contraction coupling in adult zebrafish skeletal muscle fibers (PMC9247716) | search-summary | Adult startle swimming tail-beat frequency up to about 50 Hz |
| GIBB-2011 | Gibb AC, Ashley-Ross MA, Pace CM, Long JH 2011, Fish out of water: terrestrial jumping by fully aquatic fishes, *J Exp Zool* 315A:649-653 (doi 10.1002/jez.711) | search-summary (abstract) | *Danio rerio* makes tail-flip jumps on land that are kinematically distinct from aquatic fast starts. **No velocities retrieved** |
| WIEST-1995 | Wiest FC 1995, The specialized locomotory apparatus of the freshwater hatchetfish family Gasteropelecidae, *J Zool* 236:571-592 | search-summary **of a secondary (hobbyist) page** | Reported via that page: high-speed video shows the pectorals act during the leap but not while airborne, so this is a powered jump, not powered flight. Speeds `unknown` |
| VANWASSENBERGH-2008 | Van Wassenbergh S, Strother JA, Flammang BE, Ferry-Graham LA, Aerts P 2008, Extremely fast prey capture in pipefish is powered by elastic recoil, *J R Soc Interface* 5:285-296 | search-summary (abstract) | Elastic energy in epaxial tendons powers head rotation for feeding. It does not power whole-body launch |
| ASTLEY-2012 | Astley HC, Roberts TJ 2012, Evidence for a vertebrate catapult: elastic energy storage in the plantaris tendon during frog jumping, *Biol Lett* 8:386-389 | search-summary | Non-fish comparator for a tendon catapult |
| LAITONE-1997 / PELLETIER-MUELLER-2000 | Laitone EV 1997 (*Exp Fluids*); Pelletier A, Mueller TJ 2000 (*J Aircraft*) | search-summary | Laitone: below Re 70,000 a thin plate with 5% circular-arc camber did best, tested down to Re ≈ 20,000. Pelletier & Mueller: Re 60,000-200,000. **Neither reaches Re 2,000-4,000. No CL_max number retrieved.** One summary gave CL_max 0.55-0.7 for wings at Re 60,000-160,000 (source paper not identified) |
| ZUFFEREY-2026 | Zufferey R et al. 2026, Leaping out of the water: aerial-aquatic locomotion with flapping wings, *Science* | search-summary of press coverage | A ~250 g robot with ~80 cm span flaps at ~10 Hz to exit water versus 5-6 Hz in cruise. Engineering existence proof only |

## 1. Measured zebrafish burst speed

| Stage | Quantity | Value | BL/s | Method | Source (read-level) |
|---|---|---|---|---|---|
| Larva 5 dpf, 4.2 mm | peak speed, **one example** fast start | 0.15 m/s | ≈ 36 (my division) | 5-camera high-speed video | VOESENEK-2019 (search-summary) |
| Larva 2-21 dpf | escape speed "up to" | `unknown` in m/s | 38 (secondary claim) | high-speed video | MULLER-2004 (secondary, unconfirmed) |
| Larva 6-9 dpf | escape peak velocity | `unknown` (not retrieved) | | high-speed digital imaging | BUDICK-2000 (listing) |
| Adult, wild type, SL ≈ 3.6 cm | Ucrit (prolonged, **not burst**) | 0.56 m/s | 15.5 SL/s | Brett tunnel, 28 °C, N = 21 | PLAUT-2000 (search-summary) |
| Adult | Ucrit-type | 0.548 ± 0.007 m/s | 18.0 BL/s | swim tunnel | PALSTRA-2010 (search-summary) |
| Adult | Ucrit | 0.40-0.55 m/s | | flume | FLUME-2018 (search-summary) |
| Adult | **peak escape (C-start) velocity** | **`unknown`** | **`unknown`** | n/a | none found. VISCOSITY-2012 has a max-velocity table I could not read |

**Disagreement, not averaged away:**

- The two adult Ucrit values agree on absolute speed (0.55-0.56 m/s) but differ in length-specific
  speed (15.5 against 18.0 BL/s). That points to different length definitions or fish sizes. Plaut
  also gives 12.5 SL/s for long-finned fish, and some secondary citations misattribute that figure
  to wild type.
- The larval values are about 36-38 BL/s, more than twice the adult Ucrit in BL/s. They measure a
  different thing (peak instantaneous escape speed against sustained speed) at a different size.

**Inference:**

- Adult peak escape speed must exceed Ucrit. By how much is not established by anything I read.
- A stretch value of 38 BL/s × 4 cm = **1.52 m/s** is used below only as an optimistic,
  clearly labelled "what if". Length-specific speed generally *falls* with size (a trend stated in
  the developmental-fast-start literature summary I retrieved, not a zebrafish adult measurement).

## 2. Required takeoff speed in air

V = √(2mg / (ρ S CL_max)), with m = 0.4 g (W = 3.924 mN) and ρ = 1.225 kg/m³. Span b = k × 4 cm
for k = 1-6, S = b²/AR for AR = 3-8. The wing's own mass is **excluded** (it is treated in §3).
Re is the chord Reynolds number at stall speed, with ν_air = 1.5e-5 m²/s.

**CL_max justification.** The grid's Reynolds numbers are only **1,700-4,000**. Every lift source I
retrieved stops at Re ≥ 20,000, so CL_max at this Re is **`unknown`** from the literature I reached.

- **0.6 (conservative, attainable).** This is at the low end of the 0.55-0.7 reported for thin
  wings at Re 60,000-160,000 (search-summary). Thin flat plates are reported to change little with
  Re, so a flat or lightly cambered plate should reach roughly this value at Re ~10³.
- **0.9 (plausible, unverified).** This assumes a thin cambered plate (Laitone's 5% arc being best
  below Re 70,000) holds or improves its CL_max as Re falls to about 3,000. No number confirms it.
- **1.2 (optimistic upper bound).** No retrieved steady-wing source supports it at this Re. It would
  need low-aspect-ratio vortex lift or unsteady leading-edge-vortex effects to be sustained. I keep
  it as a best case and do not treat it as attainable. I did not use 1.5.

**CL_max = 0.6: stall speed V (m/s) [chord Re]**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 4.47 [3977] | 5.17 [3444] | 5.78 [3081] | 6.33 [2812] | 6.83 [2604] | 7.31 [2436] |
| 2×L (8 cm) | 2.24 [3977] | 2.58 [3444] | 2.89 [3081] | 3.16 [2812] | 3.42 [2604] | 3.65 [2436] |
| 3×L (12 cm) | 1.49 [3977] | 1.72 [3444] | 1.93 [3081] | 2.11 [2812] | 2.28 [2604] | 2.44 [2436] |
| 4×L (16 cm) | 1.12 [3977] | 1.29 [3444] | 1.44 [3081] | 1.58 [2812] | 1.71 [2604] | 1.83 [2436] |
| 5×L (20 cm) | 0.89 [3977] | 1.03 [3444] | 1.16 [3081] | 1.27 [2812] | 1.37 [2604] | 1.46 [2436] |
| 6×L (24 cm) | 0.75 [3977] | 0.86 [3444] | 0.96 [3081] | 1.05 [2812] | 1.14 [2604] | 1.22 [2436] |

**CL_max = 0.9: stall speed V (m/s) [chord Re]**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 3.65 [3247] | 4.22 [2812] | 4.72 [2515] | 5.17 [2296] | 5.58 [2126] | 5.97 [1989] |
| 2×L (8 cm) | 1.83 [3247] | 2.11 [2812] | 2.36 [2515] | 2.58 [2296] | 2.79 [2126] | 2.98 [1989] |
| 3×L (12 cm) | 1.22 [3247] | 1.41 [2812] | 1.57 [2515] | 1.72 [2296] | 1.86 [2126] | 1.99 [1989] |
| 4×L (16 cm) | 0.91 [3247] | 1.05 [2812] | 1.18 [2515] | 1.29 [2296] | 1.40 [2126] | 1.49 [1989] |
| 5×L (20 cm) | 0.73 [3247] | 0.84 [2812] | 0.94 [2515] | 1.03 [2296] | 1.12 [2126] | 1.19 [1989] |
| 6×L (24 cm) | 0.61 [3247] | 0.70 [2812] | 0.79 [2515] | 0.86 [2296] | 0.93 [2126] | 0.99 [1989] |

**CL_max = 1.2: stall speed V (m/s) [chord Re]**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 3.16 [2812] | 3.65 [2436] | 4.08 [2178] | 4.47 [1989] | 4.83 [1841] | 5.17 [1722] |
| 2×L (8 cm) | 1.58 [2812] | 1.83 [2436] | 2.04 [2178] | 2.24 [1989] | 2.42 [1841] | 2.58 [1722] |
| 3×L (12 cm) | 1.05 [2812] | 1.22 [2436] | 1.36 [2178] | 1.49 [1989] | 1.61 [1841] | 1.72 [1722] |
| 4×L (16 cm) | 0.79 [2812] | 0.91 [2436] | 1.02 [2178] | 1.12 [1989] | 1.21 [1841] | 1.29 [1722] |
| 5×L (20 cm) | 0.63 [2812] | 0.73 [2436] | 0.82 [2178] | 0.89 [1989] | 0.97 [1841] | 1.03 [1722] |
| 6×L (24 cm) | 0.53 [2812] | 0.61 [2436] | 0.68 [2178] | 0.75 [1989] | 0.81 [1841] | 0.86 [1722] |

The cheapest cell is 24 cm span, AR 3, CL_max 1.2: **V = 0.53 m/s**. That wing is 192 cm² with an 8 cm chord (twice the body length), at a wing loading of 0.20 N/m². Fish 1990's lightest measured wing
loading is 11.7 N/m², 57 times higher.

**What a real flying fish of 0.4 g would need (inference, extrapolated).** Fish 1990's fits cover
0.003-0.53 kg. At 0.4 g (7.5 times below the smallest specimen) they give:

- span/SL of **1.0-1.7**, which puts it in grid rows 1×L to 2×L;
- WL of **4.3-18.8 N/m²**;
- stall speed of **2.41-7.16 m/s** (Danichthys at CL_max 1.2 up to Parexocoetus at 0.6).

Fish's smallest *measured* WL of 11.7 N/m² gives 3.99-5.64 m/s.

**Model check on real flying fish.** The Cypselurus WL fit at 0.1-0.2 kg, inside its measured range,
gives stall speeds of 12.4-20.2 m/s across CL_max 0.6-1.2. The relayed taxi speeds (10 → 16-20 m/s)
sit in that band, and the 10 m/s at the start of the taxi sits below it. That is consistent with the
taxi being necessary to reach flying speed. It is a consistency check, not a validation.

## 3. The gap (ratio = available speed / required stall speed)

**CL_max = 0.6: ratio 0.56 m/s (adult Ucrit, measured) / V_stall**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 0.13 | 0.11 | 0.10 | 0.09 | 0.08 | 0.08 |
| 2×L (8 cm) | 0.25 | 0.22 | 0.19 | 0.18 | 0.16 | 0.15 |
| 3×L (12 cm) | 0.38 | 0.33 | 0.29 | 0.27 | 0.25 | 0.23 |
| 4×L (16 cm) | 0.50 | 0.43 | 0.39 | 0.35 | 0.33 | 0.31 |
| 5×L (20 cm) | 0.63 | 0.54 | 0.48 | 0.44 | 0.41 | 0.38 |
| 6×L (24 cm) | 0.75 | 0.65 | 0.58 | 0.53 | 0.49 | 0.46 |

**CL_max = 0.9: ratio 0.56 m/s (adult Ucrit, measured) / V_stall**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 0.15 | 0.13 | 0.12 | 0.11 | 0.10 | 0.09 |
| 2×L (8 cm) | 0.31 | 0.27 | 0.24 | 0.22 | 0.20 | 0.19 |
| 3×L (12 cm) | 0.46 | 0.40 | 0.36 | 0.33 | 0.30 | 0.28 |
| 4×L (16 cm) | 0.61 | 0.53 | 0.47 | 0.43 | 0.40 | 0.38 |
| 5×L (20 cm) | 0.77 | 0.66 | 0.59 | 0.54 | 0.50 | 0.47 |
| 6×L (24 cm) | 0.92 | 0.80 | 0.71 | 0.65 | 0.60 | 0.56 |

**CL_max = 1.2: ratio 0.56 m/s (adult Ucrit, measured) / V_stall**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 0.18 | 0.15 | 0.14 | 0.13 | 0.12 | 0.11 |
| 2×L (8 cm) | 0.35 | 0.31 | 0.27 | 0.25 | 0.23 | 0.22 |
| 3×L (12 cm) | 0.53 | 0.46 | 0.41 | 0.38 | 0.35 | 0.33 |
| 4×L (16 cm) | 0.71 | 0.61 | 0.55 | 0.50 | 0.46 | 0.43 |
| 5×L (20 cm) | 0.88 | 0.77 | 0.69 | 0.63 | 0.58 | 0.54 |
| 6×L (24 cm) | 1.06 | 0.92 | 0.82 | 0.75 | 0.70 | 0.65 |

**CL_max = 0.6: ratio 1.52 m/s (INFERENCE: 38 BL/s × 4 cm, not measured) / V_stall**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 0.34 | 0.29 | 0.26 | 0.24 | 0.22 | 0.21 |
| 2×L (8 cm) | 0.68 | 0.59 | 0.53 | 0.48 | 0.44 | 0.42 |
| 3×L (12 cm) | 1.02 | 0.88 | 0.79 | 0.72 | 0.67 | 0.62 |
| 4×L (16 cm) | 1.36 | 1.18 | 1.05 | 0.96 | 0.89 | 0.83 |
| 5×L (20 cm) | 1.70 | 1.47 | 1.32 | 1.20 | 1.11 | 1.04 |
| 6×L (24 cm) | 2.04 | 1.77 | 1.58 | 1.44 | 1.33 | 1.25 |

**CL_max = 0.9: ratio 1.52 m/s (INFERENCE: 38 BL/s × 4 cm, not measured) / V_stall**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 0.42 | 0.36 | 0.32 | 0.29 | 0.27 | 0.25 |
| 2×L (8 cm) | 0.83 | 0.72 | 0.64 | 0.59 | 0.54 | 0.51 |
| 3×L (12 cm) | 1.25 | 1.08 | 0.97 | 0.88 | 0.82 | 0.76 |
| 4×L (16 cm) | 1.66 | 1.44 | 1.29 | 1.18 | 1.09 | 1.02 |
| 5×L (20 cm) | 2.08 | 1.80 | 1.61 | 1.47 | 1.36 | 1.27 |
| 6×L (24 cm) | 2.50 | 2.16 | 1.93 | 1.77 | 1.63 | 1.53 |

**CL_max = 1.2: ratio 1.52 m/s (INFERENCE: 38 BL/s × 4 cm, not measured) / V_stall**

| span | AR 3 | AR 4 | AR 5 | AR 6 | AR 7 | AR 8 |
|---|---|---|---|---|---|---|
| 1×L (4 cm) | 0.48 | 0.42 | 0.37 | 0.34 | 0.31 | 0.29 |
| 2×L (8 cm) | 0.96 | 0.83 | 0.74 | 0.68 | 0.63 | 0.59 |
| 3×L (12 cm) | 1.44 | 1.25 | 1.12 | 1.02 | 0.94 | 0.88 |
| 4×L (16 cm) | 1.92 | 1.66 | 1.49 | 1.36 | 1.26 | 1.18 |
| 5×L (20 cm) | 2.40 | 2.08 | 1.86 | 1.70 | 1.57 | 1.47 |
| 6×L (24 cm) | 2.88 | 2.50 | 2.23 | 2.04 | 1.89 | 1.77 |

**Best case, stated honestly.**

- **Measured speed (0.56 m/s, Ucrit):**
  - Ratio ≥ 1 only in the single cell 6×L, AR 3, CL_max 1.2 (1.06), with a massless wing.
  - Wing mass is **assumed**, since no areal density was retrieved for any fin. Including it, the
    same geometry needs 0.59, 0.64, 0.74 and 0.82 m/s at 0.5, 1, 2 and 3 mg/cm²; the ratio falls
    to 0.95, 0.88, 0.76 and 0.68.
  - As S → ∞, stall speed tends to √(2gσ/(ρ CL)), so oversized wings run into their own weight.
- **Flying-fish-proportioned wings (rows 1-2×L, or the Fish fits):** ratio **0.08-0.35**.
- **Stretch value (1.52 m/s, inferred):** ratio ≥ 1 for every AR at span ≥ 4×L with CL_max ≥ 0.9.
  At 3×L it reaches 1 only at low AR. Against the Fish-fit wings, 0.21-0.63.

**Why reaching stall speed is not enough.** Stall speed is the speed at which lift equals weight.
A fish crossing the surface at exactly that speed has no thrust in air, so it decelerates
immediately. Leaving at 0.56 m/s and 30-60° reaches an apex of **0.4-1.2 cm**. Even at 1.52 m/s and
60° the apex is 8.8 cm. Gliding from that apex at an **assumed** L/D of 2-5 adds 1-6 cm (0.56 m/s)
or up to 44 cm (1.52 m/s, 60°, L/D 5). Takeoff into anything that could be called flight needs
either exit speed well above stall, or thrust in air. That is the job taxiing does in exocoetids.

## 4. Water-to-air transition: the taxi

**Published (all search-summary, except Fish 1990 at the repo's full-text level):**

- Fish 1990 (relaying Shoulejkin 1929 et al.) reports that the taxi raises speed from **10 to
  16-20 m/s**. The hypocaudal (lower) lobe is **63.1 ± 0.5%** of caudal area, conserved across
  genera, and is the taxiing propulsor.
- Edgerton & Breder 1941 photographed the fish clear of the water with the long lower lobe still
  immersed.
- Tail-beat frequency during taxi is **reported inconsistently**:
  - 50-70 strokes/s, older literature relayed by TAXI-BIORXIV;
  - 21.2 ± 4.6 Hz, aquarium accelerometry, MAKIGUCHI-2013;
  - 13.5 Hz, APS-2024 abstract.

  These differ by up to 5 times, which probably reflects species, setting and the definition of a
  "stroke". I do not reconcile them.
- **Thrust:** no measured taxi thrust found. APS-2024 *estimates* about 2 N minimum to hold a
  200 g fish above the surface, which is about its weight. TAXI-BIORXIV is a model (80 Hz → 16.5 m/s).
- Exit speed in the aquarium study (3.9-5.2 m/s, estimated) was only 39-52% of previously
  reported maximum swim speeds. The authors attribute this to confinement.

**Zebrafish equivalent.**

- *Measured zebrafish tail-beat thrust: `unknown`.* I found none in N or mN, larval or adult.
  VOESENEK-2019 reconstructed larval fast-start forces by inverse dynamics, but I did not retrieve
  the peak values.
- Partial context:
  - larvae reach accelerations up to 40,000 BL/s² at 3 dpf (SICB abstract, search-summary);
  - adult startle tail beats run up to about 50 Hz (ZF-MUSCLE, search-summary).
- The zebrafish caudal fin is externally symmetric, with no enlarged lower lobe. That is general
  morphology, not sourced here. So it lacks the structure that keeps a propulsor in the water while
  the body is in the air.

**Requirement (inference).** If taxi speed scales with stride, V ≈ s·L·f, then reaching the
smallest flying-fish-proportioned stall speed (2.41 m/s) with L = 4 cm needs:

| Stride s (body lengths per beat, **assumed**) | Tail-beat frequency needed for 2.41 m/s |
|---|---|
| 1.0 | 60 Hz |
| 0.7 | 86 Hz |
| 0.5 | 121 Hz |

Reaching 4 m/s would need 100-200 Hz. These are lower bounds, because a partly immersed tail
tip is a less effective propulsor than a whole tail. Against about 50 Hz for the adult startle,
the requirement is **1.2-4 times above the reported maximum frequency**. That holds even before
asking whether a 3-4 mm-tall symmetric fin tip can make thrust while the body is airborne.

The energy needed is 2.75 J/kg to go from 0.56 to 2.41 m/s. Flying fish add roughly 78-150 J/kg
during their taxi (10 → 16-20 m/s), but those fish are hundreds of times heavier.

## 5. Can the gap be closed at all?

| Route | What it must achieve (inference) | Status |
|---|---|---|
| **Ballistic jump only** | Exit speed ≥ stall speed, plus margin, because there is no thrust in air: **≥ 2.4-7.2 m/s** for flying-fish wings. That is 4.3-13 times Ucrit, 18-160 times its kinetic energy, and 60-180 BL/s. With a giant 6×L wing, ≥ 0.6-0.8 m/s, which yields a hop of about 1 cm, not flight | Adult burst speed `unknown`. No evidence that it reaches 60 BL/s; larvae are reported at about 36-38 BL/s |
| **Tail-taxi augmentation** | A propulsor that stays immersed while the body is airborne, beating ≥ 60-120 Hz (stride-assumed) to reach 2.4 m/s | Zebrafish has no hypocaudal lobe. Adult tail beat ≈ 50 Hz max (search-summary). Thrust `unknown` |
| **Catapult or elastic storage** | Store and release ≥ **2.9-26 J per kg body** (V²/2 for 2.4-7.2 m/s) in one event, against 0.16 J/kg of kinetic energy at Ucrit. For a 0.4 g fish that is 1.2-10 mJ | Fish do use elastic recoil, but in the **feeding** strike (pipefish and seahorse head rotation, VANWASSENBERGH-2008). **No fish found using elastic storage for whole-body launch.** Frogs (ASTLEY-2012) and fleas do, with specialised latches that fish lack |
| **Flapping** | Thrust and lift from low speed. Ideal actuator-disk induced power to support 0.4 g at zero airspeed is **1.9 W/kg body (24 cm span) to 11 W/kg (4 cm span)**. Real power is higher by an unknown inefficiency factor (profile power and the efficiency of a flapping fin are not retrieved) | No fish is documented flying under its own flapping power. The hatchetfish claim is reported as disproven (WIEST-1995 via a secondary source: a powered jump, not flight). A 250 g robot does exit water by flapping (ZUFFEREY-2026), showing the physics allows it with a dedicated actuator, not with any known fish musculature. Pectoral muscle mass and power density for zebrafish: `unknown` |

## 6. Verdict and what would change it

**A 4 cm, 0.4 g zebrafish cannot take off from water by its own speed.** Measured speed is 0.56 m/s
(Ucrit; burst `unknown`). Required speed is ≥ 2.41 m/s for any wing proportioned like a real
flying fish. That is a ratio of ≤ 0.23, a shortfall of ≥ 4.3 times in speed and ≥ 18 times in
energy. At a realistic CL_max of 0.9 and the median-like Cypselurus fit (4.76 m/s) it is 0.12,
about 8.5 times in speed and about 72 times in energy. The single cell that closes on paper (a
massless 24 cm-span wing at CL_max 1.2) closes by 6%, disappears with 0.5 mg/cm² of wing, and
yields a centimetre-scale hop.

**Single hardest number: 2.41 m/s ≈ 60 BL/s** is the lowest exit speed a 0.4 g fish with
flying-fish-proportioned wings needs, even at an optimistic CL_max of 1.2. The best measured adult
zebrafish number is 0.56 m/s.

**What would change it:**

1. **A measured adult zebrafish peak escape or water-exit speed.** I did not find one. It would need
   to be ≥ 2.4 m/s (about 4.3 times Ucrit) to close the gap for flying-fish-like wings; the
   inference-grade 1.52 m/s does not. Reading VISCOSITY-2012 Table 1 and GIBB-2011 at full text is
   the cheapest next step.
2. **CL_max measured at Re 2,000-4,000** for a thin cambered or low-aspect-ratio fin-like plate. If
   it exceeded about 1.2, the oversized-wing corner would widen. Below about 0.9, the gap widens.
3. **Areal density of a fin-ray-and-membrane wing.** It sets the floor √(2gσ/ρCL) for oversized
   wings. At ≥ 0.5 mg/cm², even the 24 cm wing fails at measured speeds.
4. **Measured tail thrust of a partly immersed zebrafish caudal fin.** Nothing found. Without it,
   taxiing is a hypothesis, not a route.
5. **Changing the question.** A fish built around a dedicated flapping actuator or a latch-and-spring
   launcher is no longer limited by swimming speed. Nothing in the retrieved biology says zebrafish
   tissue provides either.
