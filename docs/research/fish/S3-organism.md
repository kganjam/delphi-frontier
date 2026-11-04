# S3 (organism): does the mass and power budget close?

**Status: derived.** Measured inputs from published sources, combined by my own computation. **Nothing in this document is a new measurement.**
Every computed number is printed by `python3 docs/research/fish/S3_budget.py`, which takes no external inputs.

**Depends on (sibling branches, read in this session):**
- S28 (`claude/s28-organism-design-5z0vjz`): planforms A/B/C, 57 / 125 / 192 mm², with a 31 mm span (13.5 mm semispan per fin). It also gives the measured burst of 1.38 m/s (Miln et al. 2021, via S28). Separately, it computes that flying at 1.38 m/s would need 1,925 mm².
- S2 (`claude/s2-low-reynolds-aero-acdwr7`): planforms of 4.5 / 9 / 18 cm², and the project CL_max of 1.07.
- S10 (`claude/s10-tissue-flapping-power-2kag3x`): a flapping planform with R = 4 cm and AR 6 (10.7 cm²), the hover-power method, and the work-loop table.
- S29 (`claude/s29-launch-energy-2iuixr`): hydromechanical efficiency η_h = 0.37, and the assumed 30 % / 60 % muscle fraction.
- S9 (`claude/s9-fin-ray-materials-t0royp`): ray modulus and bone-density values.

I did not re-read the primary sources behind those inherited values. Each one keeps the read-level that its sibling gave it.

## 0. Short answer

**No. The mass budget closes for small wings, and closes only marginally for large ones. The power budget does not close for any designed planform once the measured hydromechanical efficiency is applied.** The two halves fail in opposite directions, so no single planform escapes both.

1. **Wing mass is not negligible, and a measured-thickness fin is barely able to carry itself at today's speeds (computed).**
   - Fin tissue is measured at 40–200 µm thick (Puri 2018, caliper). With a soft-tissue to bone density range of 1.05–1.56 g/cm³, that gives an areal density of **0.042–0.31 kg m⁻²**, with a central value of 0.138 kg m⁻².
   - At CL 1.07, a fin of that tissue generates its own weight in lift at **1.44 m/s** (central; range 0.79–2.16 m/s). The best measured zebrafish burst is **1.38 m/s**.
   - **So at today's best speed, a central-thickness fin of any size cannot even carry itself, never mind the body.** No planform lets a 0.4 g zebrafish take off at 1.38 m/s unless the fin's areal density is below 0.127 kg m⁻². The thinnest measured tissue (40 µm, soft density) is below that, but it would then need a 4,700 mm² wing weighing 0.20 g.
2. **Small wings: the mass budget closes, but the speed requirement is large.**
   - The S28 headline wing (192 mm²) weighs **8–84 mg**, which is **2–21 % of body mass**.
   - Charging that mass raises V_to from 5.58 to **5.77–5.99 m/s**.
3. **Large wings: the speed requirement falls, but the mass budget fails at the upper bound.**
   - The S2/S10 wings of 9–18 cm² bring V_to down to 2.3–3.4 m/s.
   - They weigh **0.12–0.79 g across the central to high+ thickness brackets**, which is **31–197 % of body mass**.
   - At high thickness (200 µm, bone-like density), **the wing outweighs the 0.4 g body from about 1,300 mm² upward** (S2-large and S28's 1,925 mm²: 140–150 %). At the thickest measured tissue (281 µm), the S10 wing already outweighs the body (117 %). **This meets the brief's refutation criterion at the upper bound of measured fin tissue.** At central thickness it does not (62–67 %).
4. **Power: the launch does not close.**
   - The launch must accelerate body plus wing from rest to V_to within the water. The required mean mechanical power is **409–23,000 W kg⁻¹ muscle** across all planforms and assumptions that use the measured η_h of 0.37.
   - The measured fast-start power of fish fast (white) muscle is **142.7 W kg⁻¹** (Wakeling & Johnston 1998, 20 °C).
   - The shortfall is therefore **2.9× in the most generous case**: S10 wing, 2 body lengths of run-up, 60 % of body mass as working muscle, η_h 0.37. For the S28 headline wing it is **20–161×**.
   - **Even at η_h = 1 it does not quite close.** That would be a fish that loses no energy to the water, which has never been measured; pike are measured at 0.34–0.39 (via S29). At η_h = 1 the best case reaches near-parity (151 vs 142.7 W kg⁻¹, **1.06× short**) and S2-mid is 1.23× short.
5. **A calibration check on the power model (computed, consistency only).** Applied to today's fish (1.38 m/s, 1 body length, η_h 0.37, 30 % muscle), the model asks for 148 W kg⁻¹ muscle. That is close to the measured 142.7 W kg⁻¹. **So the model does not over-ask by an order of magnitude for a performance fish actually achieve.** This is a consistency check, not a validation: η_h and the run-up distance were not measured for zebrafish.

**Evidence level: derived.** The negative is robust to every bracket I could set on thickness, density, muscle fraction and run-up distance. It is not robust to η_h, which is the one input that has never been measured for a small fish.

---

## 1. The question, restated with the numbers that make it hard

Take a 0.40 g, ~3–4 cm *Danio rerio* (the brief's numbers). Add a pectoral planform S of fin tissue with measured thickness t and density ρ_fin. Then two things must hold together:

- **(a) Mass.** The wing mass m_w = ρ_fin · t · S must leave the total mass M = m_body + m_w low enough that the wing can lift it at an attainable speed: M g ≤ ½ ρ_air V² CL S.
- **(b) Power.** The body's white (fast, glycolytic) muscle, which has no wing to drive it, must supply the mechanical power to accelerate M to the take-off speed V_to inside the water. This is done against a fluid that takes a large share of every push (η_h). For flapping, the muscle must additionally supply induced power, plus inertial power for the wing's own mass.

**Why it is hard. Both halves scale against each other:**
- Required speed falls as S^(−1/2), so a bigger wing helps (b).
- Wing mass rises as S at fixed thickness, so a bigger wing hurts (a). It rises faster than S if the fin must thicken to stay stiff.
- The density that matters is not body density but **areal density versus lift per area**: σ = ρ_fin t against ½ ρ_air V² CL / g. At the measured 1.38 m/s, lift per area is only **0.127 kg m⁻²** (computed). That is less than the central areal density of measured fin tissue.

**What was already established, and what this subproblem adds.** S28 found the design is 3.2× short in speed even at a 192 mm² wing, but it *did not charge wing mass*. It noted 10.6–21.1 mg and said "I do not charge it below". S10 assumed perfect elastic storage, so it charged no wing inertia. **This document charges both.**

## 2. What is measured

Read-levels: **full-text** (I read the article text in this session, through a summarising fetch tool that quotes sentences); **abstract**; **search-summary** (a search engine's extract only); **via S#** (inherited from a sibling at that sibling's stated read-level); **could-not-access**.

### 2a. Fin tissue geometry (zebrafish)

| # | Quantity | Value | Specimen / method | Source (year) | Read-level |
|---|---|---|---|---|---|
| T1 | Caudal-fin thickness along the proximal–distal axis | **"decreases from 200 to 40 µm"** | Adult zebrafish, in vivo work, digital calliper | Puri, Aegerter-Wilmsen, Jaźwińska & Aegerter, *J Exp Biol* 221:jeb171777 (2018), PMC5868929 | full-text (main text; supplement not read) |
| T2 | Caudal-fin width at the same positions | ~5 → 8 mm | same | same | full-text |
| T3 | Ray diameter | **0.1–0.2 mm** | same (stated in comparison to bluegill) | same | full-text |
| T4 | Whole caudal-fin flexural stiffness EI | **1.5–4 × 10⁻⁹ N m²** measured. The authors' bluegill-derived estimate is 2–5 × 10⁻⁹ | same | same | full-text |
| T5 | Effective I of whole fin | 7 → 3 × 10⁻¹⁶ m⁴ | same | same | full-text |
| T6 | Inter-ray **thickness**, adult caudal fin, at ray branching | central IR **82.4 ± 6.2 µm** (n = 40); marginal IR (abutting the ray) **275.8 ± 41.8 µm** (n = 46); branch IR **281.4 ± 52.3 µm** (n = 53) | Histological cross-sections (Mallory's trichrome / H&E). Fish described as 15–38 mm SL. Table 1, column "Thickness (μm)" | Murciano et al., *J Anat* 232:783–805 (2018), PMC6480674 | full-text, **first ~56 % only** (100k of 179k characters) |
| T7 | Regenerated IR thickness | central 117.6 ± 24.3; marginal 406 ± 147.3; branch 295.1 ± 14.6 µm | same | same | same |

**Caveats on T6, which I am keeping visible.**
- The methods text I read **does not state the axis** of the thickness measurement. The Fig. 3 legend says only "Thickness is shown by double-pointing arrows" on cross-sections. I read it as through-thickness because the column is labelled "Thickness" and is separate from the inter-ray *widths* (~99–111 µm) that the paper reports elsewhere. **That reading is my inference.**
- Ray (hemiray) thickness is listed as "nd" (not determined) in Table 1.
- Table 3 of the same paper gives ectopic-membrane "thickness" values of 2.8–11 µm. These are ~10× below Table 1 and I could not explain them from the text I read. I do not use them.

**Disagreement preserved.** Puri's caliper reads 40 µm distally. Murciano's histology reads 82 µm at the thinnest (central inter-ray) domain. The specimens, positions and methods all differ, and a caliper on soft tissue may compress it. I keep both values. The low bracket below uses Puri's 40 µm, and the central bracket uses a 120 µm mean that sits between them.

**Every T-row is the caudal fin, not the pectoral fin.** I found no measured pectoral-fin thickness for zebrafish (§5).

### 2b. Densities

| # | Quantity | Value | Source (year) | Read-level |
|---|---|---|---|---|
| D1 | Zebrafish body density with the swimbladder volume removed | **1.05 ± 0.04 g cm⁻³** (whole body 1.01 ± 0.09; swimbladder 5.1 ± 1.4 % of volume; fish 0.16–0.73 g) | Robertson, Lindsey, Dumbarton, Croll & Smith, *J Morphol* 269:666–673 (2008) | search-summary (abstract sentences quoted by the search engine) |
| D2 | Muscle density used to convert volume to mass | 1.06 g cm⁻³ (**assumed by the authors**, not measured) | Mead et al. 2020, *Biophys J* 119:806 | full-text (first ~83 %) |
| D3 | Hydrated bone tissue density | **1.557 g cm⁻³** (albacore bone); 1.856 (whale) | Tont, Pearcy & Arnold (1977), *Mar Biol* | via S9 (search-summary) |
| D4 | Teleost bone mineralisation | 1.04–1.39 g HA cm⁻³ (notothenioids and others; X-ray microradiography) | Meunier et al. (as surfaced by search, Cybium 2018 record) | search-summary |
| D5 | Fin-ray tissue density for any teleost | **unknown** | — | negative: S9's search, and two searches of mine (§5) |

**No fin tissue density has been measured.** I bracket it between soft tissue (D1, 1.05) and hydrated fish bone (D3, 1.557). For the central case I **assume** a ray volume fraction of 20 %, giving 1.15 g cm⁻³. D4 is not used numerically: it measures mineral per unit volume, not tissue density.

### 2c. Muscle power (fast / white muscle)

| # | Quantity | Value | Conditions | Source (year) | Read-level |
|---|---|---|---|---|---|
| P1 | Mean muscle-mass-specific power in a fast-start | **142.7 W kg⁻¹** | *Scorpaena notata* fast myotomal fibres, work loops at in vivo strain and timing, 20 °C. The authors state that power predicted from filmed swimming agreed with the work loops | Wakeling & Johnston, *J Exp Biol* 201:1505–1526 (1998) | abstract (fragments quoted by two search listings); full text could-not-access (silverchair host not resolvable from this session) |
| P2 | Net cycle-averaged power | **134.4 ± 19.9 W kg⁻¹ at 80 Hz**; 122.9 ± 11.1 at 100 Hz | 5 dpf **larval** zebrafish myotome, 28 °C | Mead, Kennedy, Palmer, Ebert & Warshaw, *Biophys J* 119:806–820 (2020), PMC7451861 | full-text (first ~83 %) |
| P3 | Peak instantaneous power, shortening phase | **498.9 ± 127.0 (80 Hz); 640.2 ± 151.5 W kg⁻¹ (100 Hz)** | same | same | full-text |
| P4 | Cold adult fast muscle | 25–35 W kg⁻¹ (sculpin, ~4 °C); 16.4–27.5 (cod, falling with size) | various | via S10 (search-summary) | via S10 |
| P5 | Instantaneous peak in an escape | 307 W kg⁻¹ (C-bend), 222 (contralateral) | sculpin | Johnston & van Leeuwen 1995, via S10 | search-summary |
| P6 | Hydromechanical efficiency of a C-start | **0.37** (0.34–0.39) | pike | Frith & Blake, via S29 | abstract (via S29) |
| P7 | Muscle fraction of body mass, zebrafish | **unknown**. S29 uses 60 % (a SECONDARY review figure) and 30 % for one side | — | via S29 | secondary |
| P8 | Adult zebrafish burst speed | 0.45–1.38 m/s | n = 50, high-speed video | Miln et al. 2021, via S28 | via S28 |

**Disagreement preserved.**
- P1 and P2 agree at ~135–143 W kg⁻¹, even though they come from different species, temperatures and life stages.
- The cold-muscle values (P4) are 4–9× lower.
- The instantaneous peaks (P3, P5) are 2–5× higher, but they are peaks, not means, and so they are **not** comparable with a mean requirement.

I compare against P1 as the measured *mean fast-start* value, and I show P3 only as a ceiling.

## 3. What I computed

**Everything in this section is computation. None of it is an observation.** Constants: g = 9.81 m s⁻², ρ_air = 1.225 kg m⁻³, CL_max = 1.07 (project value, derived, used unchanged), m_body = 0.40 g.

### 3.1 Fin areal density, and the speed at which a fin merely carries itself

The areal density is σ = ρ_fin · t_mean. The self-carry speed is V_self = √(2σg / (ρ_air CL)).

| Case | t (µm) | ρ_fin (g cm⁻³) | σ (kg m⁻²) | V_self (m/s) |
|---|---|---|---|---|
| low | 40 (T1, thinnest measured) | 1.05 (D1) | 0.0420 | **0.79** |
| **central** | 120 (mean of a linear 200→40 taper, **assumed**) | 1.15 (20 % ray, **assumed**) | **0.1382** | **1.44** |
| high | 200 (T1, thickest caliper value) | 1.557 (D3) | 0.3114 | **2.16** |
| high+ | 281 (T6, branch inter-ray) | 1.557 | 0.4375 | 2.56 |

Worked example (central): 1150 × 120×10⁻⁶ = 0.138 kg m⁻². Then 2 × 0.138 × 9.81 / (1.225 × 1.07) = 2.066, and √2.066 = 1.44 m/s.

Lift per area at the measured 1.38 m/s burst: ½ × 1.225 × 1.38² × 1.07 / 9.81 = **0.127 kg m⁻²**. That is below the central σ.

**Meaning (my inference from the computation).** Planform size cancels out of this test. At 1.38 m/s, a sheet of central-thickness fin tissue of *any* area produces less lift than it weighs. Making the wing bigger cannot fix this; only a faster fish or a thinner fin can.

### 3.2 Wing mass for every designed planform (m_body = 0.40 g)

Each cell gives wing mass and its percentage of body mass.

| Planform (source) | S (mm²) | low | central | high | high+ |
|---|---|---|---|---|---|
| S28 A, length-only | 57 | 2.4 mg, 0.6 % | 7.9 mg, 2.0 % | 17.7 mg, 4.4 % | 24.9 mg, 6.2 % |
| S28 B, isometric | 125 | 5.3 mg, 1.3 % | 17.3 mg, 4.3 % | 38.9 mg, 9.7 % | 54.7 mg, 13.7 % |
| **S28 C, AR 5 (headline)** | **192** | 8.1 mg, 2.0 % | **26.5 mg, 6.6 %** | 59.8 mg, 14.9 % | 84.0 mg, 21.0 % |
| S2 small | 450 | 18.9 mg, 4.7 % | 62.2 mg, 15.5 % | 140 mg, 35 % | 197 mg, 49 % |
| S2 mid | 900 | 37.8 mg, 9.5 % | 124 mg, 31 % | 280 mg, 70 % | 394 mg, 98 % |
| S10 flapping | 1070 | 44.9 mg, 11 % | 148 mg, 37 % | 333 mg, 83 % | **468 mg, 117 %** |
| S2 large | 1800 | 75.6 mg, 19 % | 249 mg, 62 % | **561 mg, 140 %** | **788 mg, 197 %** |
| S28 "fly at 1.38 m/s" | 1925 | 80.8 mg, 20 % | 266 mg, 67 % | **599 mg, 150 %** | **842 mg, 211 %** |

Cross-check against S28's own estimate: S28 put the 192 mm² membrane at 10.6–21.1 mg (50–100 µm × 1100 kg m⁻³). My 8.1–84 mg brackets that range. My range is wider because I use the measured 40–281 µm thickness instead of an assumed 50–100 µm.

**Take-off speed with wing mass charged:** V_to = √(2(m_body + σS) g / (ρ_air S CL)).

| Planform | wing-free | central | high |
|---|---|---|---|
| S28 A | 10.25 | 10.35 | 10.47 m/s |
| S28 B | 6.92 | 7.07 | 7.25 |
| **S28 C** | 5.58 | **5.77** | 5.99 |
| S2 small | 3.65 | 3.92 | 4.24 |
| S2 mid | 2.58 | 2.95 | 3.36 |
| S10 | 2.37 | 2.77 | 3.20 |
| S2 large | 1.82 | 2.32 | 2.83 |
| S28 1,925 mm² | 1.76 | 2.28 | 2.79 |

Charging wing mass lifts V_to by 1–7 % for the S28 wings and by **14–59 % for the wings of 900 mm² and larger**. **S28's computed claim that 1,925 mm² would fly at 1.38 m/s does not survive the charge: with wing mass included, that wing needs 2.28–2.79 m/s.**

### 3.3 Inverse problem: what planform takes off at a given speed, with wing mass charged?

Solve m_body + σS = (½ρV²CL/g)·S, which gives S = m_body / (½ρV²CL/g − σ). There is no solution when σ ≥ ½ρV²CL/g.

| V (m/s) | low σ | central σ | high σ | high+ σ |
|---|---|---|---|---|
| **1.38** (measured best burst) | 4,693 mm², wing 0.20 g | **no solution** | no solution | no solution |
| 2.0 | 1,776 mm², 0.07 g | 3,099 mm², **0.43 g (> body)** | no solution | no solution |
| 3.0 | 715 mm², 0.03 g | 864 mm², 0.12 g | 1,380 mm², **0.43 g (> body)** | 2,443 mm², 1.07 g |
| 4.37 | 324 mm², 0.01 g | 352 mm², 0.05 g | 415 mm², 0.13 g | 477 mm², 0.21 g |

### 3.4 Will the measured fin structure even hold the load? (structural spar mass)

**Model, entirely my assumption:**
- Each fin is a cantilever of semispan L carrying half of n·M·g, spread uniformly.
- The spar is one solid circular bone rod. Of the solid-rod layouts, a single rod gives the lowest mass for a given EI: splitting EI over k rods multiplies mass by √k.
- The tolerance is a tip deflection of 10 % of span, the same tolerance used in the project's replicate-199.
- Then EI_req = (nMg/2)·L²/(8 × 0.1). For a rod, EI = Eπr⁴/4 and mass = ρ_bone π r² L.
- Ray modulus E: 0.11 / 1.34 / 6.48 GPa, the distal bluegill ray, proximal bluegill ray, and sculpin rib values (via S9, search-summary).

| Planform | n | EI_req (N m²) | rod d at E = 1.34 GPa | spar mass (2 fins), E = 6.48 → 0.11 GPa |
|---|---|---|---|---|
| S28 C (13.5 mm) | 1 | 4.8 × 10⁻⁷ | 292 µm | 1.3–9.8 mg (0.3–2.5 %) |
| S28 C | 3 | 1.4 × 10⁻⁶ | 384 µm | 2.2–17 mg (0.6–4.3 %) |
| S2 mid (30 mm) | 1 | 2.9 × 10⁻⁶ | 458 µm | 7–54 mg (1.8–13 %) |
| S10 (40 mm) | 1 | 5.4 × 10⁻⁶ | 535 µm | 13–98 mg (3–24 %) |
| S10 | 3 | 1.6 × 10⁻⁵ | 704 µm | 22–169 mg (6–42 %) |

**Comparison with measured values:**
- The **measured whole caudal-fin EI is 1.5–4 × 10⁻⁹ N m²** (T4). The S28-C requirement at 1 g is therefore **~120–320× the measured whole-fin stiffness**, and for the S10 wing it is ~1,300–3,600×.
- The required rod diameters, **0.2–1.3 mm**, are **1–13× the measured 0.1–0.2 mm ray diameter**. They are comparable to or larger than the *total* measured fin thickness (40–281 µm), so the spar would have to bulge well out of the fin plane.

**Inference.** The thickness used in §3.1–3.3 is *measured* tissue that is far too floppy for the job. A wing stiff enough to bear 1 g adds the spar masses above **on top of** the membrane. For the large wings that is another 3–42 % of body mass. **§3.2 is therefore a lower bound on a working wing's mass.**

### 3.5 Launch power

**Model, assumed:**
- Accelerate M from rest to V_to under constant acceleration over a run-up s inside the water, so the duration is t = 2s/V_to.
- Mean mechanical power at the body is P = (V_to²/2)/t / η_h, per kg of total mass.
- Per kg of muscle, multiply by M / (f_m · m_body). The wing contributes mass but no muscle.
- s ∈ {0.5, 1, 2} body lengths of 4 cm; η_h ∈ {1, 0.37}; f_m ∈ {0.3, 0.6}.
- Central wing tissue throughout.

Required W kg⁻¹ muscle (multiple of the 142.7 W kg⁻¹ measured, P1):

| Planform (V_to) | s | η_h = 1, f_m 0.6 | η_h = 0.37, f_m 0.6 | η_h = 0.37, f_m 0.3 |
|---|---|---|---|---|
| **S28 C (5.77 m/s)** | 0.5 BL | 4,260 (30×) | 11,513 (81×) | 23,026 (161×) |
| S28 C | 1 BL | 2,130 (15×) | 5,756 (40×) | 11,513 (81×) |
| S28 C | 2 BL | 1,065 (7.5×) | **2,878 (20×)** | 5,756 (40×) |
| S2 mid (2.95 m/s) | 1 BL | 352 (2.5×) | 950 (6.7×) | 1,901 (13×) |
| S2 mid | 2 BL | 176 (1.2×) | 475 (3.3×) | 950 (6.7×) |
| S10 (2.77 m/s) | 1 BL | 303 (2.1×) | 818 (5.7×) | 1,636 (11×) |
| **S10** | **2 BL** | 151 (1.1×) | **409 (2.9×)** | 818 (5.7×) |

Worked example (S10, 2 BL, η_h 0.37, f_m 0.6):
- V_to = 2.77 m/s and t = 2 × 0.08 / 2.77 = 57.8 ms.
- (2.77²/2)/0.0578 = 66.4 W kg⁻¹ total. Dividing by 0.37 gives 179 W kg⁻¹ total.
- Multiplying by 0.548/(0.6 × 0.40) gives **409 W kg⁻¹ muscle = 2.9 × 142.7**.

**Calibration (consistency check only).** For today's wingless fish (1.38 m/s, 1 BL, f_m 0.3), the same model needs 55 W kg⁻¹ muscle at η_h = 1 and **148 W kg⁻¹ at η_h = 0.37**. Measured fast-start muscle gives 142.7 W kg⁻¹. The model therefore reproduces a performance that fish actually reach to within ~4 %. That agreement could be coincidental: neither η_h nor s is measured for zebrafish.

**Against the peak ceiling (P3, 499–640 W kg⁻¹ instantaneous).** Only the S10 and S2-mid wings, with 2 BL and f_m 0.6, need a *mean* power (409–475) below that *peak*. Holding peak power as a mean over 55–58 ms has not been measured in any fish I found (P2's means are 3.7–5.2× below their own peaks).

### 3.6 Flapping: what wing mass does to S10's hover estimate

S10's planform (R = 4 cm) with the wing mass charged:
- Induced power rises by (M/m_body)^1.5 = **1.17× / 1.60× / 2.48×** (low / central / high).
- If the wing's kinetic energy is not stored elastically (S10 assumed perfect storage), the inertial power at 22 Hz and 120° stroke is **11 / 36 / 82 mW**, which is **3.5–12×** the induced power. Model: rectangular wings, I = m_w R²/3, ω_max = 2πfΦ/2, KE lost every half-stroke.
- S10's "most generous" 34 W kg⁻¹ flight muscle therefore becomes ~54 W kg⁻¹ at central wing mass even with perfect storage: 34 × 1.60, ignoring that M/m_body also changes the profile term.
- With no storage, it rises to several hundred W kg⁻¹.

None of this is measured. It shows only that **S10's flapping requirement is a lower bound once the wing has mass.**

## 4. The answer

**Evidence level: derived.** Measured tissue thickness, density proxies and muscle power, combined by my own computation (§3). No simulation, no new measurement.

**The mass and power budget does not close for a 0.40 g zebrafish with any planform proposed in this project.**

- **Mass alone closes for small wings.** The S28 headline 192 mm² wing is 2–21 % of body mass (central 6.6 %).
- **Mass fails the brief's refutation test at the upper bound for large wings.** At the thickest measured fin tissue with bone density, wings of ≳1,300 mm² outweigh the body: 117–211 % for S10 / S2-large / S28-1,925 mm². At central thickness they do not (37–67 %). **So the refutation criterion is met only at the high end of measured thickness and assumed density, not at the centre. That is a bracketed result, not a single verdict.**
- **Speed-for-mass has no solution at today's performance.** At 1.38 m/s, central-thickness fin tissue cannot lift even itself (V_self = 1.44 m/s). This holds independent of planform area.
- **Power fails for every planform** once η_h = 0.37 is applied:
  - the most generous case is **2.9×** short (409 vs 142.7 W kg⁻¹ muscle);
  - the S28 headline wing is **20–161×** short;
  - even at η_h = 1, which is unmeasured and implausible for a fish pushing on water, the best case is still 1.06× short (near-parity, not closure).
- The two halves pull the planform in opposite directions. A small wing passes on mass and fails badly on power. A large wing roughly halves the power gap but approaches or exceeds body mass and needs a spar 3–42 % of body mass to stay rigid (§3.4).

## 5. What this does NOT establish

- **No pectoral-fin data.** Every thickness value (T1, T6) is from the **caudal** fin of wild-type adults, 15–38 mm SL. I found no measured zebrafish *pectoral*-fin thickness. Search scope: two standard and one extended web search on zebrafish fin thickness, hemiray dimensions and fin histology, plus full-text reads of Puri 2018 and the first 56 % of Murciano 2018. Pectoral fins may be thinner or thicker.
- **No fin tissue density.** That is `unknown` for any teleost (S9's search plus my two searches on fin-ray bone density). The 1.05–1.56 bracket is proxies: whole-body-minus-swimbladder, and albacore bone. The 20 % ray fraction in the central case is an assumption.
- **Thickness of an enlarged fin is unknown.** I applied the measured thickness of a normal-sized fin to wings 1–20× larger in area. If an enlarged fin thickens with its length (isometry), wing mass rises faster than S and every large-wing number in §3.2 is an *under*-estimate. If a mutant could make larger fins *without* thickening, the low bracket applies. **No measurement of thickness in long-fin mutants (e.g. *kcnh2a* / *longfin*) was found or searched specifically.**
- **The Murciano thickness axis is my reading**, not a stated method (§2a caveat). If those values are not through-thickness, the high+ case falls away. Puri's 40–200 µm caliper range still carries the central and high cases.
- **The spar model is crude.** It uses a single solid rod, uniform load, 10 % deflection tolerance and quasi-static loading. A hollow or sandwich section would be lighter. Real fins are multi-ray and pre-curved, and curvature stiffening is known to matter (S9). Active stiffening (S26) is ignored. The modulus spans a 59× bracket, and the yield and strength of the rays are `unknown`.
- **The launch model is crude.** It assumes constant acceleration from rest, a single submerged run-up, and no drag beyond η_h. I did **not** model a multi-stroke surface taxi, which S30 argues is how real flying fish launch. Taxi is a sustained-thrust problem, and S28 put the tail 2.5–3.8× short in frequency for it. **This document does not say a taxi launch is impossible; it does not compute one.**
- **η_h is the decisive unmeasured input.** It is measured only for pike, a large fish at high Re (via S29, abstract). For a 4 cm fish it could be lower, which worsens everything, or higher. The single closure case (η_h = 1) is a bound, not a claim.
- **Muscle fraction is not measured for zebrafish.** 30 % and 60 % are S29's assumption and a secondary figure. The power result scales as 1/f_m.
- **The muscle power comparators are not adult zebrafish.** P1 is *Scorpaena* at 20 °C (abstract only). P2 is 5 dpf larvae. **No adult zebrafish work-loop value was found** (one standard search, plus S10's searches). Adult zebrafish fast muscle at 28 °C could be higher than 142.7 W kg⁻¹.
- **CL_max 1.07 is a project value** (derived, S2/S28), not measured on a fish fin. If it were 1.5, every V and V_self falls by √(1.07/1.5) = 0.84×.
- **Stabilisation was not computed.** The brief asks whether the animal can "launch and stabilise". I computed launch power and structural stiffness, not control authority, moments of inertia about roll/pitch, or the mass of the control-surface musculature. Moving a heavy wing outboard raises roll inertia, which in principle damps disturbances and also slows corrections. **The sign of its net effect on stability is `unknown` here.**
- **Gliding power is zero, and this is not a statement that gliding is impossible once airborne.** A launched animal that reached V_to could glide at L/D ~3–5 (S2's estimate) with no muscle power at all. This document says it cannot reach V_to by its own muscle under the assumptions above.
- **Body mass held at 0.40 g.** S28 used 0.25 g. At 0.25 g, wing mass is a larger fraction of body (×1.6) and V_to slightly lower. Section 3 tables are for 0.40 g only. S30 argues that a smaller fish does better on single-impulse launch; I did not re-run that here.

## 6. What would change the answer

In order of how far each could move the result:

1. **A measured hydromechanical efficiency for a ~4 cm fish's C-start or water exit** (PIV). **No η_h ≤ 1 closes any planform on its own.** The S10 2-BL case would need η_h ≥ 0.37 × 2.87 ≈ 1.06 at f_m 0.6. η_h does, however, set how close the large wings come: at η_h ≈ 0.8 they are within ~1.3–1.5× (S10 and S2-mid, 2 BL, f_m 0.6), and a modest gain in muscle power (item 3) would then close them. For the S28 headline wing, even η_h = 1 leaves it 7.5× short.
2. **Pectoral-fin thickness and areal density, measured in a long-fin mutant** (*kcnh2a^lof* / Daane double het): weigh an excised fin and photograph its area. This one measurement gives σ directly and replaces T1/T6/D1/D3 together.
   - If σ ≤ 0.05 kg m⁻², the mass budget closes for every planform.
   - If σ ≥ 0.3 kg m⁻², the large wings fail the refutation criterion outright.
   - Cost: hours, on an existing animal.
3. **A measured adult zebrafish fast-muscle work-loop power** at 28 °C and fast-start timing. A value ≥ ~410 W kg⁻¹ (2.9× P1) would close the most generous case. Above ~3,000 W kg⁻¹ it would close the S28 headline wing. That exceeds every fish value in §2c and the vertebrate instantaneous maximum quoted in S29 (1,121 W kg⁻¹, secondary).
4. **Zebrafish muscle mass fraction**, by dissection. This moves the power result linearly. It cannot plausibly exceed ~0.6, so it cannot close the gap by itself.
5. **A computed or measured multi-stroke taxi launch.** This changes the task from a 50 ms burst to a sustained-thrust problem. It could change the verdict, but S28 shows the tail 2.5–3.8× short on frequency for it.
6. **Design changes that would move it:**
   - Thinner wing membrane, below the measured 40 µm, with stiffness carried by a few thick rays. This lowers σ but raises the spar mass (§3.4).
   - Elastic energy storage (LaMSA, S29/S30) to amplify power. It removes the power ceiling but not the energy ceiling, which S29 found 1.2–3× short for one-sided loading.
   - A smaller body at the same shape (S30).

```swarm-result
{"subproblem": "S3", "evidence": "derived",
  "answer": "No: charging wing mass from measured zebrafish fin tissue (40-281 um thick, 1.05-1.56 g/cm3 proxies, areal density 0.042-0.44 kg/m2) the mass budget closes for small wings (S28 192 mm2 wing = 2-21% of body, V_to 5.8-6.0 m/s) but large wings that lower V_to to 2.3-3.4 m/s weigh 31-211% of the 0.4 g body at central-to-high thickness (exceeding it from ~1300 mm2 at the high bracket), central-thickness fin tissue cannot lift even itself at the measured 1.38 m/s burst (V_self 1.44 m/s), and the launch needs 409-23,000 W/kg muscle at measured eta_h 0.37 versus 142.7 W/kg measured fast-start fish white-muscle power, so the power budget fails for every designed planform (even at eta_h = 1 the best case is 1.06x short).",
  "key_number": "2.9x launch-power shortfall in the most generous case (409 W/kg muscle required vs 142.7 W/kg measured; S10 1070 mm2 wing, 2 BL run-up, 60% muscle, eta_h 0.37); 20-161x for the S28 192 mm2 headline wing",
  "blocked_on": "No measured pectoral-fin thickness or fin tissue density for zebrafish or any teleost (caudal-fin values and density proxies used); no adult zebrafish white-muscle work-loop power; hydromechanical efficiency measured only in pike; Wakeling & Johnston 1998 and Puri 2018 publisher host (silverchair) unreachable from this session, so P1 is abstract-level"}
```
