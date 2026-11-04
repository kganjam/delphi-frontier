# S7-D-D: Deepening S7-D. The weakest input, measured

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.

**Parents**
- S7: `docs/research/fish/S7-organ.md`, branch `claude/s7-organ-pectoral-girdle-xlxpkt`, commit `a61c9688`.
- S7-D: `docs/research/fish/S7-deepen.md`, branch `claude/deepen-s7-pectoral-girdle-b6j2hx`, commit `11551151`.

**Script:** `docs/research/fish/S7-D-deepen.py`.
- Part A is an **image measurement I made** from a published µCT movie. It is not a number the authors report.
- Part B is **calculation**.
- Every number in this document is labelled as one or the other.

## 0. What S7-D concluded, and what it rested on

S7-D's verdict was STANDS: girdle bone is "probably not the binding constraint". Its arguments:

- The worst-case root moment is 1.08×10⁻⁴ N·m per fin (calculated in S7; V = 3 m/s, n = 3, C_L = 0.78).
- With measured herring bone yield of 62.6 MPa, carrying that moment needs a solid-rod-equivalent section of **d_req ≈ 0.26 mm** (calculated).

S7-D also said:

- The conclusion is insensitive to every modelled input: a factor-of-2 error moves d_req by at most 27%, because d_req ∝ M^(1/3).
- The conclusion **flips** with a factor-of-2 error in the *actual* section of the receiving element, because stress scales as 1/size³.
- The receiving element is the row of four proximal radials plus the scapula (Keer 2019), not the cleithrum.
- That section was **unknown**. MorphoSource 000415918 was not reachable.
- For "radial-like rods ~0.25 mm deep" the outcome was "genuinely open".

## 1. The single most sensitive input (recomputed, not asserted)

I recomputed capacity divided by demand for the radial row treated as a locked cantilever, at the worst case and with the mid geometry measured in §3. This is a calculation (script B3). A ratio below 1 means the bone yields.

| Input varied ×0.5 / ×2 | Capacity / demand |
|---|---|
| (base) | 0.25 |
| **Plate thickness h** (out of the fin plane) | **0.06 / 0.99** |
| Summed plate width Σw | 0.12 / 0.49 |
| Bone yield σ_y | 0.12 / 0.49 |
| Load factor n | 0.49 / 0.12 |
| Speed V | 0.12 / 0.52 |

**Plate thickness h is the most sensitive input.** Z = Σw·h²/6, so a factor of 2 in h moves the ratio by a factor of 4. It is the only input whose doubling brings the worst case to the edge of passing (0.99). So S7-D's weakest input ("actual section") resolves more precisely into **the out-of-plane thickness of the proximal-radial plates.**

## 2. How well established was it before this step?

- **Evidence level: assumption.** S7 wrote that the section is "a few tenths of a mm", described as "plausible but unverified". S7-D kept it as `unknown`.
- Neither parent had a zebrafish girdle measurement of any kind.
- S7's headline "bone probably not limiting" therefore rested on an unmeasured comparison.

## 3. Improving it: measuring the radials from published µCT

### 3a. Where the data came from

**Source.** Ishizaka, Maeno, Nakazawa, Fujii, Oikawa, Tani, Kanno, Koita, Kawamura (2024). The functional roles of zebrafish HoxA- and HoxD-related clusters in the pectoral fin development. *Sci. Rep.* doi:10.1038/s41598-024-74134-9. PMC11464670.

- **Read-level: full-text**, Europe PMC fullTextXML, plus the figure and supplementary movies from the Europe PMC supplementaryFiles zip.
- **Authors' claims, as written:** dissected adult pectoral fins were µCT-scanned at "an isotropic resolution of 3.1–3.4 μm", with n = 3 wild type. Individual elements were "manually dissected using the Imaris contour surface feature". Wild type has four proximal radials (pr1–pr4).
- **Not reported by the authors:** fish standard length, fish age, and any dimension of any element. "Data … available from the corresponding author on reasonable request."

### 3b. What I measured

These are **my measurements, from rendered images**:

- **Supplementary Movie S4.** This is an Imaris rotation of the segmented wild-type proximal radials (grey) and distal radials (red), with a **100 µm scale bar of 124 px**, giving 0.806 µm/px. I sampled the 1920×1080 movie at 2 frames per second. In each frame I measured the grey-pixel extent per column.
- **Cross-check, Fig. 4G** (scale bar 250 µm = 58–59 px). It gives an overall radial-row length of about 0.85 mm, against 0.95 mm from the movie. These are consistent to about 10%.

| Quantity | Value (my image measurement) | How |
|---|---|---|
| Proximal-radial row length (proximodistal) | ≈ 0.95 mm | Long-axis span, constant across frames |
| Summed face-on width of the four plates, Σw, at mid-length | **0.36–0.44 mm** | Median per-column grey length; 0.44 in the most face-on frames, 0.36–0.40 in neighbouring frames |
| Plate thickness h (out of the fin plane), distal half | **≈ 55–100 µm** | Minimum projected thickness in the most edge-on frames (55 µm; 76–100 µm in adjacent frames) |

### 3c. How far the measurement can be trusted

- **This is not a section measurement.** It is the silhouette of a rendered isosurface.
- **Tilt.** Any tilt away from exactly edge-on *inflates* the projected thickness. So 55–100 µm is closer to an **upper bound** on h than a central value.
- **Segmentation threshold.** It sets the surface position, and it is unknown. One voxel is 3.1–3.4 µm.
- **Foramina ignored.** The plates have holes (visible in pr3 and pr4), so a solid-section Z overstates capacity.
- **Load sharing.** "Σw" assumes the four plates sit side by side in the fin plane and share the bending.
- **Fish size.** The **SL of the scanned fish is `unknown`**: it is not stated in the text, figure legends or supplementary PDF.

**Measured (image) vs. calculated.** The table in §3b is image measurement. Everything below is calculation.

### 3d. What I tried and could not use

| Source tried | Result |
|---|---|
| MorphoSource 000415918 (Nguyen 2022) | Still refused: proxy CONNECT 403 |
| Nguyen 2022 DataSheet1–4 (PMC9204358 supplement, *full-text*) | Interactive 3D PDFs. Each holds a single compressed U3D mesh ("VcgMesh01"), so bones are not separated. I did not decode it. |
| PMC article HTML | reCAPTCHA |
| Springer media server, zenodo, figshare, datadryad | Blocked |

Europe PMC full-text searches, all with no numeric girdle dimension found:
- "proximal radial" AND zebrafish AND µCT: 6 hits;
- zebrafish cleithrum thickness µm: 14 hits;
- zebrafish pectoral girdle bone volume / cross-sectional area: 10 hits;
- flying fish / hatchetfish girdle (open access): 17 hits.

Also read, with no numbers found: the fin-ray/distal-radial pattern paper (PMC6751676, full-text) and Ziadi-Künzli et al. 2024 *J. Anat.* mudskipper (PMC11424826, full-text).

Two web searches found no published zebrafish radial, scapula or adductor dimensions: one on zebrafish girdle element dimensions, one on adductor/abductor muscle area.

### 3e. What the receiving joint is (load path)

Askary, Smeeton, Paul, Schindler et al. 2016, *eLife* 5:e16415 (PMC4951194, **full-text**).

**Authors' claim:** they "observed similar cavities lined by flattened chondrocytes in joints of the pectoral fin in adult zebrafish, in particular between the proximal and distal radials and between the marginal ray and scapula". These joints are prg4b-dependent and synovial-like.

**My inference, not the authors' claim:** a synovial joint transmits force but not bending moment, unless it is locked. So in the wild-type fish, the radials cannot be the cantilever that carries the root moment. The moment must cross the joint row as a muscle (or ligament) couple, which is S7's "path 2". The radial row is then loaded mainly in compression and bearing.

## 4. Recomputation (all calculation, script B1–B4)

### 4a. Radial-row section from the measurement

| Geometry | Z (mm³) | Solid-rod-equivalent d (mm) |
|---|---|---|
| low (Σw 0.36, h 0.055) | 1.8×10⁻⁴ | 0.123 |
| mid (Σw 0.40, h 0.08) | 4.3×10⁻⁴ | **0.163** |
| high (Σw 0.44, h 0.10) | 7.3×10⁻⁴ | 0.195 |

### 4b. Path 1: radial row as a locked cantilever

Capacity divided by demand, with σ_y = 62.6 MPa and no safety factor:

| Case | M (N·m) | d_req (mm) | low | mid | high |
|---|---|---|---|---|---|
| V 3, n 3 (worst) | 1.08×10⁻⁴ | 0.260 | 0.11 | **0.25** | 0.42 |
| V 5, n 3 | 6.2×10⁻⁵ | 0.217 | 0.18 | 0.43 | 0.74 |
| V 3, n 1 | 3.6×10⁻⁵ | 0.180 | 0.32 | 0.74 | 1.27 |
| V 5, n 1 | 2.1×10⁻⁵ | 0.150 | 0.55 | 1.28 | 2.21 |

**Reading the table:**
- At the S7/S7-D worst case, the measured radial row would reach about **4× its yield stress** (mid geometry; 2.4–9× across the bracket).
- S7 itself named the flip threshold: "If ≤0.15 mm … **the answer flips to 'no'**". The measured solid-equivalent d is 0.12–0.20 mm.
- In steady glide (n = 1) the row is marginal: 0.3–2.2.

### 4c. Fish size (the remaining loophole)

- Z ∝ L³ under isometry.
- With the mid geometry, the worst case passes only if the scanned fish was at most **25 mm** long and the design fish is 40 mm. With a 1.5 safety factor the limit is 22 mm. With the most generous geometry it is 30 mm.
- The scanned fish's size is unknown. The design fish (0.4 g, about 40 mm) is an ordinary adult, so a large scale-up is not expected. **I have not verified this.**

### 4d. Path 2: the real load path (synovial hinge, muscle couple)

The radial row carries compression F = M/r. Mid area is 0.032 mm².

| Muscle moment arm r | Muscle force F | Compressive stress | Adductor PCSA (at 200 kPa) |
|---|---|---|---|
| 1.0 mm | 108 mN (28 W) | 3.4 MPa | 0.54 mm² |
| 0.5 mm | 216 mN (55 W) | 6.8 MPa | 1.08 mm² |
| 0.15 mm | 721 mN (184 W) | 22.5 MPa | 3.6 mm² |

All of these are below the 62.6 MPa yield. **In compression, bone is not the limit.** That holds for a different reason than S7-D gave.

## 5. Verdict: FALLS

S7-D's conclusion was that girdle bone is "probably not limiting", with the comparison at the radial row left open. It **falls as stated**. Measured from published wild-type µCT, the proximal-radial row has a solid-equivalent bending section of about 0.12–0.20 mm. That is below the 0.26 mm needed (calculated) and inside S7's own flip zone. As a locked cantilever it would yield at the worst case by about 4× (calculated).

**What replaces it** (inference):
- The wild-type radials are not a cantilever. They articulate through synovial joints (Askary 2016, the authors' observation), so they see compression, and in compression they are adequate (§4d, calculated).
- The constraint therefore sits **entirely** on the muscle/ligament couple across the joint row. That is S7's path 2, now with no bony fallback.
- **S7 §6.4's design option is weakened.** That option was to lock or fuse the radials so the root becomes "a true cantilever, which §3d shows is light work for the bone". With the measured geometry, fused wild-type radials would be about 4× under-strength at n = 3 (calculated). They would need roughly 2× thicker plates (h ×2 gives ratio 0.99), or 2.5× with a 1.5 safety factor.

**What would reverse this verdict:**
1. The scanned fish being ≤25–30 mm long, so that scaling to a 40 mm design rescues it.
2. Real sections being much thicker than the rendered silhouettes. This is unlikely, because tilt only inflates silhouettes.
3. Girdle bone yielding at more than 2× herring intermuscular-bone yield.

## 6. What this does NOT establish

- **No true cross-section was measured.** I measured silhouettes of a rendered isosurface, from one wild-type individual (specimen "#1" of n = 3) whose size is unknown. A proper Slice-Geometry measurement on the original volume would replace §3. Two ways to get it:
  - Ask the corresponding author of Ishizaka 2024 for the volume.
  - Use MorphoSource 000415918 (Nguyen 2022). This needs MorphoSource allowed in the environment's network policy, plus a MorphoSource login.

  Either costs about one to two analyst-days with free software (my estimate). No new scanning is needed.
- **The bending direction is assumed.** I assumed the plates lie in the fin plane and that lift bends them out of plane. If the root moment instead bends them in-plane (about an axis normal to the fin), Σw and h swap roles and the capacity rises by roughly (Σw/h) ≈ 5×. I judged out-of-plane to be correct because lift is normal to the fin surface, but I did not model fin twist or sweep.
- **The muscle moment arm r is still assumed.** It is r = 0.5–1 mm in S7. Fig. 4A shows hooked proximal processes on the ray bases. **By eye, without a pixel measurement, I read them as roughly 0.1–0.2 mm.** If the adductor acts on those processes, r is about 0.15 mm and the joint reaction rises to about 184 W, with about 3.6 mm² of PCSA. This is an untested lead, not a result. It is the natural next weakest input.
- **The bone material is still a proxy.** Herring intermuscular bone in tension stands in for zebrafish endochondral radial bone in bending. Radials also have cartilaginous articular ends (Askary 2016), which are weaker than bone in bearing. Joint contact stress was not computed.
- **Not checked:** scapula and coracoid sections, cleithrum thickness, the supracleithrum–posttemporal chain, fatigue, impact.

## Sources

- Ishizaka, Maeno, Nakazawa, Fujii, Oikawa, Tani, Kanno, Koita, Kawamura (2024). *Sci. Rep.* doi:10.1038/s41598-024-74134-9, [PMC11464670](https://europepmc.org/article/PMC/PMC11464670). Read-level: *full-text* (Europe PMC XML). Fig. 4 and Supplementary Movie S4 were downloaded from the Europe PMC supplementaryFiles endpoint and measured by me. Surnames as extracted from the XML; initials not verified, so omitted. The article's volume and page are not given here because I did not extract them.
- Askary, Smeeton, Paul, Schindler, et al. (2016). Ancient origin of lubricated joints in bony vertebrates. *eLife* 5:e16415. doi:10.7554/eLife.16415, [PMC4951194](https://europepmc.org/article/PMC/PMC4951194). Read-level: *full-text* (Europe PMC XML).
- Nguyen S.V., Lanni D., Xu Y., Michaelson J.S., McMenamin S.K. (2022). *Front. Physiol.* 13:875866, PMC9204358. Read-level: *full-text* (inherited from S7-D), and the supplementary 3D PDFs were inspected. MorphoSource 000415918: *could-not-access*.
- Keer S. et al. (2019). *Anat. Rec.*, PMC6800157. Read-level: *full-text* (inherited from S7-D). The Europe PMC XML returned empty this session.
- Fiedler I.A.K. et al. (2019). *J. Biomech.* 94:59–66, PMC6995032. Read-level: *full-text* (inherited from S7-D). Source of the 62.6 MPa yield value.
- Park H., Choi H. (2010). *J. Exp. Biol.* 213:3269. C_L 0.78: *search-summary* (inherited from S7).
- Thorsen D.H., Hale M.E. (2005). *J. Morphol.* 266:241–255. Read-level: *search-summary*; no adult muscle dimensions obtained.
- [PMC6751676](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6751676/), fin-ray/distal-radial pattern paper. Read-level: *full-text* (XML grep only); no dimensions.
- [PMC11424826](https://europepmc.org/article/PMC/PMC11424826), Ziadi-Künzli et al. 2024, *J. Anat.* Read-level: *full-text* (XML grep only); no zebrafish data.

```swarm-result
{"subproblem": "S7-D-D", "evidence": "derived", "answer": "Measured from published wild-type µCT (Ishizaka 2024 Movie S4, my image measurement), the proximal-radial row that receives the fin root moment has a solid-equivalent bending section of only ~0.12–0.20 mm (plates Σw 0.36–0.44 mm wide, ≤55–100 µm thick) against 0.26 mm required, so as a locked cantilever it would yield ~4× at the worst case and S7-D's 'girdle bone probably not limiting' falls as stated; bone survives only because the radials articulate through synovial joints (Askary 2016) and carry compression (≤23 MPa), which puts the whole root moment on the muscle couple and makes S7's 'lock the joint' design option require ~2–2.5× thicker radial plates.", "key_number": "proximal-radial plate thickness ≈55–100 µm (upper-bound silhouette), summed width 0.36–0.44 mm → solid-equivalent d 0.12–0.20 mm vs 0.26 mm required at 1.08e-4 N·m", "verdict": "falls", "depends_on": ["S7: root bending moment 1.08e-4 N·m per fin (V=3 m/s assumed, n=3 assumed, C_L=0.78 Park & Choi 2010 search-summary, AR=9 search-summary, elliptic loading, m=0.4 g, body half-width 2.5 mm)", "S7-D: bone yield 62.6 MPa (Fiedler 2019 herring intermuscular bone, tensile, full-text) as proxy for zebrafish radial bone", "Ishizaka 2024 Supplementary Movie S4 100 µm scale bar and segmented wild-type proximal radials (my image measurement: Σw 0.36–0.44 mm, h 55–100 µm)", "scanned fish standard length unknown; assumed comparable to 40 mm design fish (isometric scaling Z∝L^3)", "assumption: radial plates lie in fin plane and lift bends them out of plane; four plates share bending; foramina ignored; Euler–Bernoulli solid section", "Keer 2019: fin articulates with scapula via four proximal radials", "Askary 2016: adult zebrafish pectoral radial and ray–scapula joints are synovial-like (no moment transfer unless locked — my inference)", "S7: muscle moment arm r 0.5–1 mm (assumed) and muscle stress 200 kPa (assumed) for path-2 numbers", "safety factor 1.5 (engineering choice)"]}
```
