# S32-D: Deepening the multi-stroke launch answer by attacking its most sensitive input

**Parent:** S32 (`origin/claude/s32-multi-stroke-launch-qpq9g2`, commit c1b761eb, `docs/research/fish/S32-organism.md` + `S32_taxi.py`). I read it in full.
**Status:** derived. **Every number in §1, §4 and §5 is calculated** by `python3 docs/research/fish/S32-deepen_calc.py` (under 1 s). That script uses S32's force model unchanged, with each hard-coded input made a parameter. Its §0 reproduces S32's 2.88 m/s (GENEROUS) and 2.19 m/s (CENTRAL) exactly. **No number here is a new measurement.**

## 0. Short answer

- **The most sensitive input is the calibration burst speed U_b = 1.38 m/s.** S32 sets the airborne lobe's thrust parameter G from the condition that, at the peak of the measured burst, caudal-fin thrust equals body drag. The ceiling scales **linearly** with U_b. Every other input enters under a square root or more weakly.
  - **Calculated:** U_b ×2 flips the conclusion in both GENEROUS and CENTRAL. No other input does so at ×2 or ×0.5 (§1).
  - **Calculated:** a 1.40× error (GENEROUS) or 1.71× error (CENTRAL) is enough to flip it.
- **How well established is it?** It is **measured, but it is a proxy, and it is an extreme value of that proxy.**
  - It is the fastest of about 50 fish: per-fish best-of-4 C-start peaks, filmed at 120 fps and digitised from a figure.
  - It is a single-stroke *transient* escape peak.
  - The taxi needs the stroke-averaged thrust of *repeated* tail beats. S32's text calls the 1.38 m/s "the measured burst" and treats it as a thrust balance, which a transient peak is not (§2).
- **Improving it.** Two kinds of measurement bear on it, and they **disagree by 3–4×**. I preserve that disagreement rather than averaging it.
  - **Repeated-stroke maxima:** flume U_max. Adult zebrafish run 13.0–17.9 SL/s across 8 entries from 5 studies, which is **0.39–0.54 m/s** at the design's 30 mm SL. That is about 3× below 1.38.
  - **Single-stroke peaks:** C-start maxima. These run from **0.80 m/s** (Miln centre) to **1.57 ± 0.27 m/s** (Demesmay et al. 2025, 240 fps, full text). The newer figure is about 14% *above* S32's input.
- **Recomputed** (calculated):
  - **Repeated-stroke calibration.** The taxi decelerates from the first stroke. Net force at the 1.38 m/s exit is −0.75 to −1.10 mN, and the equilibrium is ≤ 0.92 m/s (≤ 21% of V_to).
  - **C-start-mean calibrations.** The taxi stalls at 32–77% of V_to.
  - **The conclusion flips only in the GENEROUS case**, and only if U_b ≥ 1.94 m/s. That is Demesmay's control mean + 1.4 SD, about 65 SL/s, read as a *stroke-averaged* repeated-stroke speed. CENTRAL needs 2.36 m/s (mean + 2.9 SD).
- **Verdict: STANDS.** It does not strengthen, because the input that would strengthen it (flume U_max) measures over 30-s stages and is a lower bound on 1-s capacity, not the right quantity either. The quoted band "2.2–2.9 m/s, 50–65% of V_to" should be widened to **≤ 0.9 to 3.4 m/s (≤ 21–77%) at mean inputs**, with the flip condition stated explicitly.

---

## 1. Step 1: which input is the conclusion most sensitive to? (recomputed)

Each S32 input was multiplied by 0.5 and by 2, one at a time, from S32's GENEROUS and CENTRAL scenarios (calculated, script §1). The entries are U_eq/V_to, and **≥ 1.00 means the conclusion falls**.

| Input (S32 value, status in S32) | GEN ×0.5 | GEN ×1 | GEN ×2 | CEN ×0.5 | CEN ×1 | CEN ×2 |
|---|---|---|---|---|---|---|
| **U_b, calibration burst (1.38 m/s, "measured")** | 0.28 | 0.65 | **1.57** | 0.01 | 0.50 | **1.22** |
| Body Cd in water, calibration only (0.3/0.2, assumed) | 0.49 | 0.65 | 0.93 | 0.35 | 0.50 | 0.70 |
| Frontal area (24 mm², S28) | 0.49 | 0.65 | 0.92 | 0.35 | 0.50 | 0.70 |
| Caudal fin area (37.8 mm², **assumed**) | 0.90 | 0.65 | 0.50 | 0.64 | 0.50 | 0.40 |
| Foil residual C_D (0.08, Floryan 2017) | 0.90 | 0.65 | 0.50 | 0.64 | 0.50 | 0.40 |
| Lobe chord (6 mm; sets Re) | 0.57 | 0.65 | 0.77 | 0.48 | 0.50 | 0.54 |
| Body mass (0.25 g) | 0.92 | 0.65 | 0.46 | 0.72 | 0.50 | 0.01 |
| Wing area (192 mm², S28) | 0.47 | 0.65 | 0.90 | 0.36 | 0.50 | 0.68 |
| Wing CL_max (1.07) | 0.46 | 0.65 | 0.89 | 0.35 | 0.50 | 0.67 |
| Immersed fraction φ (capped at 1) | 0.63 | 0.65 | 0.65 | 0.01 | 0.50 | 0.53 |
| Wing CD0 | 0.66 | 0.65 | 0.65 | 0.50 | 0.50 | 0.48 |

A value of 0.01 means no positive-net equilibrium exists: weight-support drag exceeds thrust at every speed.

**Flip factors** (calculated, script §2). This is the multiplier on one input needed to reach U_eq = V_to:

| Input | GENEROUS | CENTRAL |
|---|---|---|
| **U_b** | **×1.40 → 1.94 m/s** | **×1.71 → 2.36 m/s** |
| Body Cd (calibration) | ×2.30 → 0.69 | ×3.82 → 0.76 |
| Frontal area | ×2.34 | ×4.05 |
| Caudal fin area (lower) | ×0.40 | ×0.13 |
| Foil C_D (lower) | ×0.40 → 0.032 | ×0.13 |
| Wing area | ×2.51 | ×5.27 |
| Wing CL_max | ×2.70 → 2.89 | never |
| Mass (lower) | ×0.43 | ×0.26 |

**Why U_b dominates** (analytic, script §4):
- With constant C_D and air drag neglected, the calibrated ceiling is U_max = U_b·√(1 + Cd·A_front/(S_fin·C_D)).
- The square-root factor is 1.84 (GENEROUS) and 1.61 (CENTRAL).
- U_b enters linearly. Cd, A_front, 1/S_fin and 1/C_D enter only under the root, so each needs ≥ 2.3× to do what 1.4× in U_b does.
- This is a structural property of S32's calibration, not a numerical accident.

**One consequence for S32's own sensitivity table.** S32 §3.3 swept every *assumed* input but treated U_b as fixed, because it was labelled "measured". The input that was not swept is the one the answer hangs on.

## 2. Step 2: how well established is U_b = 1.38 m/s?

### 2.1 What it is (Miln, Ward & Seebacher 2021, *R Soc Open Sci* 8:210146; PMC8025299)

Read-level: **full-text** (Europe PMC XML, downloaded and searched this session). I also viewed **Fig. 1a myself**, from the Europe PMC supplementary bundle.

Author's methods, verbatim:
- "Escape responses were induced by a mechanical stimulus to the tail of the fish in a shallow tank (405 × 600 mm, 30 mm water depth). We filmed the escape response from above at 120 frames s⁻¹."
- "using the fish centre of mass as the tracking point … 0.35 body lengths from the tip to the snout."
- "four escape responses were analysed for each fish and the fastest speed was used."
- "Water temperature was 23°C (± 0.5°C)."

My reading of Fig. 1a (image viewed, not digitised to pixels):
- Fast-start speeds span about 0.45 to about 1.38 m/s.
- The rightmost points sit at about 1.38 m/s. They are one fish, plotted on three days.
- The bulk lies between 0.5 and 1.1 m/s, with its centre near 0.8 m/s.
- This agrees with the pixel digitisation in `challenge-75.md` (branch `origin/claude/challenge-75-zebrafish-fast-start-im1x80`, listing-level relay), which reported 0.45–1.38 m/s.

### 2.2 Evidence level, honestly

| Aspect | Status |
|---|---|
| Is it a measurement? | Yes. Direct kinematic tracking by the authors. |
| Is the *number* measured? | **Figure-digitised** by project reviewers. The raw data (figshare) is could-not-access: proxy 403 reported by challenge-75 and S21-D; not re-attempted here. |
| Which statistic? | **The maximum of ~50 per-fish maxima**, each a best-of-4. It is an extreme of extremes, not a typical capacity. |
| Instrument bias | At 120 fps, a transient peak is under-read. challenge-75 *calculated* 0.61–0.86× for a 10–20 ms peak width. At 23 °C rather than 28 °C, speed also probably reads low; magnitude `unknown`. |
| **Is it the right quantity?** | **No. It is a proxy.** (§2.3) |

### 2.3 The proxy problem: one transient peak standing in for repeated-stroke thrust

S32 calibrates G as "whole caudal fin thrust = body water drag at the burst speed peak, where dU/dt = 0". It then uses G as a **stroke-averaged, repeatable** thrust for 38–74 consecutive strokes. Three problems follow. Each is my inference from the sources, not a claim the sources make.

1. **dU/dt = 0 at a C-start peak is an instantaneous balance, not a periodic one.**
   - The peak is reached during the first stroke: Demesmay et al. report "latency to attain maximal speed (8 ± 4 ms)" after the head turn.
   - Much of the acceleration up to that instant comes from stage-1 whole-body bending, not from steady caudal flapping.
   - S32 itself flags that assigning all of it to the tail is "generous".
2. **The speed a fish holds under repeated strokes is measured separately, and it is much lower.**
   - Flume U_max (incremental velocity, stages of seconds to minutes) is the repeated-stroke analogue of "thrust = drag".
   - Widrick et al. 2018 (§3.2) compile adult values of **13.0–17.9 SL/s**, against roughly 27–52 SL/s for C-start peaks.
3. **The taxi sits between the two timescales.** A taxi of 38–74 strokes at 52 Hz lasts 0.7–1.4 s.
   - Flume stages last 6–30 s or more, and include fatigue. That makes flume U_max a **lower bound** on 1-s capacity.
   - A single C-start peak is plausibly an **upper bound**, because in the C-start literature, speed after stage 2 does not keep rising stroke over stroke. That is an inference: I did not read Domenici & Blake 1997 this session.
   - **The quantity that actually matters, the stroke-averaged thrust of a ~1 s run of maximal tail beats, is unmeasured for zebrafish.**

## 3. Step 3: going and improving it

### 3.1 A newer, faster C-start measurement

**Demesmay L et al. 2025, *PLoS Biol* 23(11):e3003484, PMC12604801.** Read-level: **full-text** (Europe PMC XML, downloaded and searched this session).

Verbatim:
- "240 frames/s (escape response, 1 s long videos)"
- "Two similar objects (1 g) placed at approximately 30 cm above the water were simultaneously dropped into two adjacent tanks (1.6 L) containing … 3 or 4 adult fish by tank"
- "Body length … 2.6 ± 0.2 cm for 4-month-old and 3.6 ± 0.2 for 12-month-old fish"
- "Videos were processed with Fiji software (angle tool and manual tracking plugin)"
- "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants) and latency to attain maximal speed (8 ± 4 ms …)"
- "Distance covered in 40 ms from the escape response start … (3.8 ± 0.8 cm for controls …)"
- "minimum of 11 per genotype", "mean ± SD"

My reading, as inference:
- The control **mean** (1.57 m/s) exceeds Miln's **single fastest fish** (1.38 m/s).
- 240 fps resolves the peak better than 120 fps does.
- Maximal speed from manually clicked positions over 1–2 frames (4–8 ms) is biased **upward** by click noise. The magnitude is `unknown`: the pixel scale and tracked point are not stated in the text I searched.
- The 40-ms average, 3.8 cm / 40 ms = **0.95 m/s**, is a noise-robust floor on the peak.

### 3.2 The repeated-stroke quantity: flume U_max

**Widrick JJ et al. 2018, *PLoS ONE* 13:e0199712, PMC6019105.** Read-level: **full-text** (Europe PMC XML).

Their Table 2 compiles "maximal swimming speeds expressed as mean SL s⁻¹". I parsed the table's cell structure; the first, naive parse mis-assigned columns, and I corrected it. **Adult column:**

| Study (as cited by Widrick; **primaries not read: listing-level**) | °C | Adult U_max (SL/s) |
|---|---|---|
| Plaut 2000 | 28 | 15.5 |
| Seebacher & Walter 2012 | 25 | 13.7 |
| Gilbert et al. 2014 | 28 | 14.4; 16.3 (two protocols) |
| Conradsen et al. | 28 | 14.8 (f); 17.9 (m) |
| Widrick 2018 (present study) | 25 | 13.0 (f); 15.9 (m) |

- Range: **13.0–17.9 SL/s**. At the design's 30 mm SL (S32: fin height 9 mm = 0.3 SL), that is **0.39–0.54 m/s**.
- Fiaz et al.'s 10.3 is a **14-dpf** value. I initially mis-assigned it and then excluded it.
- Widrick's own text: "U crit rises from ≈ 3 cm s⁻¹ in 5 dpf larvae to 40 − 55 cm s⁻¹ in adults … U max exceeds U crit by about 15%". This is an author claim citing Gilbert et al.; I did not read Gilbert et al.

**Miln et al. 2021 also measured a repeated-stroke maximum.** Verbatim: "the maximum attained speed (U10) in a 10 s constant acceleration trial … flow … increased by an average of 0.05 m s⁻¹ every 1 s". That is the closest published protocol to a ~1-s taxi, on the same 50 fish. Its values are in **ESM Fig. S1a**, which is not in the Europe PMC supplementary bundle. That bundle contains only Figs 1–3 and the review history; I checked it. **U10 values: `unknown`.**

### 3.3 What measurement would settle it, and what it would cost

**The real quantity** is the stroke-averaged thrust, or equivalently the steady speed, of an adult zebrafish making ~40–70 consecutive maximal tail beats.

**Cheapest settling measurement:**
1. Obtain Miln's U10 raw data. The figshare collection is doi:10.6084/m9.figshare.c.5359401; access needs a network path not blocked by the proxy. Cost: about zero, and it gives n = 50.
2. Alternatively, re-run a 1-s-scale sprint: a constant-acceleration flume ramp of 0.5–1 m s⁻² for 1–2 s, filmed at ≥ 500 fps to get tail-beat f and A_pp. Cost: a Blazka tube plus a pump (Widrick's open-source flume reaches 70 cm/s, which is enough), a high-speed camera, and about 1–2 weeks for 20 fish.
3. **The decisive version** measures thrust directly: a tethered adult zebrafish on a force transducer, or a PIV wake-momentum estimate, during startle-evoked tail-beat trains. Cost: a µN–mN force sensor or a PIV rig, roughly 1–2 months.
4. A partially immersed robotic lobe in a flume (S32 §5 item 1) remains the test of the foil law itself. It does not settle U_b.

## 4. Step 4: the conclusion recomputed with the improved input

Calculated (script §3). All other inputs are at S32's GENEROUS or CENTRAL values. V_to = 4.41 m/s (0.25 g). The exit speed is held at 1.38 m/s.

| U_b source (read-level) | U_b (m/s) | GEN U_eq (%V_to) | GEN net at 1.38 m/s exit | CEN U_eq (%V_to) | CEN net at exit |
|---|---|---|---|---|---|
| Flume U_max low, 13.0 SL/s (Widrick Tbl 2; full-text, primaries listing) | 0.39 | none | **−1.10 mN** | none | −0.98 |
| Flume U_max high, 17.9 SL/s (same) | 0.54 | 0.92 (21%) | **−0.75** | none | −0.84 |
| Miln C-start centre (Fig 1a viewed) | 0.80 | 1.43 (32%) | +0.10 | none | −0.52 |
| Demesmay 40-ms mean (full-text) | 0.95 | 1.75 (40%) | +0.77 | none | −0.27 |
| **Miln fastest fish (S32's input)** | 1.38 | 2.88 (65%) | +3.33 | 2.19 (50%) | +0.71 |
| Demesmay control mean max (full-text) | 1.57 | 3.41 (77%) | +4.76 | 2.66 (60%) | +1.26 |
| Demesmay mean + 1 SD | 1.84 | 4.15 (94%) | +6.94 | 3.26 (74%) | +2.07 |
| Demesmay mean + 2 SD | 2.11 | **4.93 (112%)** | +9.40 | 3.85 (87%) | +2.98 |

"none" means net force is negative at every speed: weight-support drag exceeds thrust.

**U_b needed to flip:**

| Mass | GENEROUS | CENTRAL |
|---|---|---|
| 0.25 g | **1.94 m/s** (65 SL/s) | 2.36 m/s (79 SL/s) |
| 0.40 g | 2.35 m/s | 2.88 m/s |

### Reading it

- **On the repeated-stroke branch,** the conclusion is **much stronger** than S32 stated.
  - At the 1.38 m/s exit, the airborne lobe's thrust is below drag. The taxi decelerates from the first stroke.
  - Its equilibrium (≤ 0.92 m/s) lies below or near the 0.51–0.77 m/s needed for the lobe to support the body.
  - The "speed genuinely rises, doubling in ~10 strokes" part of S32's answer **does not survive** this calibration.
- **On the single-stroke branch,** the newer, better-resolved measurement (Demesmay) moves the ceiling **up**: 77% of V_to at the mean, GENEROUS.
  - It flips only for individuals ≥ mean + 1.4 SD, in the GENEROUS corner.
  - That corner already assigns all C-start thrust to the tail, puts the whole lower lobe in water with no ventilation loss, and ignores surface tension.
- **What a flip requires.** A *stroke-averaged* repeated-stroke speed of ≥ 65 SL/s. That exceeds the *peak transient* C-start speed of the average fish in the fastest dataset (≈ 50 SL/s at Demesmay's mean length; my arithmetic, 1.57 m/s ÷ ~3.1 cm). It is 3.6–5× the flume U_max of every adult entry in Widrick's table.
- **No measurement I found puts the right quantity at or above the flip value.**

### Verdict: STANDS

- The negative answer holds on every mean-valued input, from both measurement families.
- It does **not** strengthen. The strengthening branch (flume U_max) is itself a biased-low proxy for 1-s capacity. The correct quantity is unmeasured, and the best single-stroke measurement moved the number in the feasible direction.
- What changes:
  1. **The headline band.** "Stalls at 2.2–2.9 m/s, 50–65% of V_to" should read **"stalls at ≤ 0.9 to 3.4 m/s, ≤ 21–77% of V_to, depending on which measured burst calibrates thrust"**.
  2. **"Speed genuinely rises"** is conditional on calibrating with a C-start peak ≥ ~0.8 m/s. It is false on the repeated-stroke calibration.
  3. **The reopening condition.** It is now stated in terms of a measurable quantity: a ~1-s, stroke-averaged burst speed ≥ 1.94 m/s (65 SL/s) for the GENEROUS case, or ≥ 2.36 m/s (CENTRAL). This replaces S32's "1.4–2.2× the tail speed of the best measured burst", which was a multiplier on a proxy.

## 5. Disagreements preserved

| Sources | Value | Notes |
|---|---|---|
| Miln 2021 | C-start centre ~0.8 m/s, maximum 1.38 | 120 fps, 23 °C, COM tracking, best-of-4, n ≈ 50 |
| Demesmay 2025 | Mean 1.57 ± 0.27 m/s | 240 fps, manual tracking, n ≥ 11 |

- These differ by ~2× in the mean. Frame rate, temperature, stimulus (tail touch vs dropped object), tracked point and click noise could each contribute. **I do not average them.**
- Danos & Lauder 2012 (0.842 m/s by Re inversion, 1000 fps) is relayed via challenge-75 and S21 only. I did not read it; read-level is listing (repository relay).
- Sibling documents (challenge-140, `origin/claude/challenge-danio-exit-speed-35kkas`; S20-D-D-D) **disagree on method**: Danio burst as exit speed vs burst × guppy ratio. That bears on the exit speed, which is a separate S32 input from U_b. Here the exit is held at S32's 1.38 m/s.

## 6. Searches and their scope

- **Europe PMC full-text XML.** Downloaded for PMC8025299 (Miln), PMC12604801 (Demesmay) and PMC6019105 (Widrick), and keyword-searched for: fps/frames, speed, maximal, U10, temperature, body length.
- **Europe PMC supplementary bundle for PMC8025299.** Contains Figs 1–3 and the review history PDF. **No ESM Fig. S1, so no U10 values.** The review history mentions "U10 speed (Supplementary Fig. 1a)" but gives no values.
- **NCBI/Europe PMC figure URLs.** HTTP 403/404; the bundle was used instead.
- **Web search.** One query, standard mode: "adult zebrafish maximum sprint speed constant acceleration test U burst m/s Seebacher". Results: [Widrick et al. 2018, PMC6019105](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6019105/), [Miln et al. 2021, PMC8025299](https://pmc.ncbi.nlm.nih.gov/articles/PMC8025299), [PeerJ 4292](https://peerj.com/articles/4292.pdf) (not read), and [ZFIN ZDB-PUB-120127-12](https://zfin.org/ZDB-PUB-120127-12) (not read).
- **Cross-branch `git grep`** of this repository for `1.38 m/s` and `Miln`, to find the provenance chain: S32 → S28 → S21-D → challenge-75.
- **Not searched:**
  - Direct thrust measurements on adult zebrafish tail-beat trains.
  - Burst-and-coast kinematics papers.
  - Domenici & Blake 1997 (cited by Miln, not read).
  - Theses.
  - Non-English literature.
- **Negative finding, within that scope:** no measured adult zebrafish stroke-averaged speed or thrust on a ~1-s timescale was found.

## 7. Sources and read-levels

| Source | Read-level |
|---|---|
| S32-organism.md + S32_taxi.py (c1b761eb) | full-text (repository) |
| Miln, Ward & Seebacher 2021, *R Soc Open Sci* 8:210146, PMC8025299 | full-text (Europe PMC XML) + Fig. 1a image viewed |
| Miln 2021 ESM Fig. S1a (U10) | could-not-access (not in Europe PMC bundle; figshare 403 per challenge-75, not re-attempted) |
| Demesmay et al. 2025, *PLoS Biol* 23:e3003484, PMC12604801 | full-text (Europe PMC XML) |
| Widrick et al. 2018, *PLoS ONE* 13:e0199712, PMC6019105 | full-text (Europe PMC XML), Table 2 parsed |
| Plaut 2000; Seebacher & Walter 2012; Gilbert et al. 2014; Conradsen et al. (as tabulated by Widrick) | listing (via Widrick Table 2) |
| challenge-75.md (Miln digitisation; 120 fps under-read calculation) | full-text (repository); its primaries relayed |
| challenge-140.md (Demesmay vs Miln disagreement) | full-text (repository) |
| Danos & Lauder 2012 | could-not-access (not attempted; relayed via challenge-75) |
| Floryan et al. 2017 foil law; Fish 1990; Deng 2019 | inherited from S32 at its stated read-levels; not re-read |

```swarm-result
{"subproblem": "S32-D", "evidence": "derived (S32's force model re-run with each input as a parameter, script docs/research/fish/S32-deepen_calc.py, reproduces S32's 2.88/2.19 m/s) on measured inputs read this session at full-text: Miln et al. 2021 (C-start 0.45-1.38 m/s, 120 fps, best-of-4, centre ~0.8, Fig 1a viewed), Demesmay et al. 2025 (C-start 1.57 +/- 0.27 m/s, 240 fps, manual tracking; 3.8 cm in 40 ms), Widrick et al. 2018 Table 2 (adult flume U_max 13.0-17.9 SL/s, primaries listing-level); the right quantity (stroke-averaged ~1 s burst thrust) is unmeasured", "answer": "The S32 negative STANDS: its most sensitive input is the thrust-calibration burst speed U_b (ceiling linear in U_b; x2 flips both scenarios, x1.40 flips GENEROUS, no other input flips at x2), which is a single-fish 120-fps C-start peak used as a proxy for repeated-stroke thrust; recomputed with measured alternatives the taxi stalls at <=0.9-3.4 m/s (<=21-77% of the 4.41 m/s glide speed) at every mean input, decelerating from the first stroke on a flume-U_max calibration (0.39-0.54 m/s), and flips only in the GENEROUS corner if a stroke-averaged ~1 s burst reaches >=1.94 m/s (65 SL/s; CENTRAL 2.36 m/s), which no measurement found reaches.", "key_number": "calibration burst speed U_b: flume repeated-stroke U_max 0.39-0.54 m/s (13.0-17.9 SL/s at 30 mm SL) vs single-stroke C-start 0.80 (Miln centre) to 1.57 +/- 0.27 m/s (Demesmay 2025), against S32's 1.38 m/s; flip threshold 1.94 m/s (GENEROUS) / 2.36 m/s (CENTRAL)", "verdict": "stands",
  "depends_on": ["S32 (origin/claude/s32-multi-stroke-launch-qpq9g2 c1b761eb) force model and GENEROUS/CENTRAL scenarios", "S32 thrust calibration: caudal thrust = body water drag at burst peak (assumption)", "Floryan et al. 2017 foil law C_T = 2.55 St^2 - 0.08, C_D 0.08 at Re 4780-9560 (via S32, FULL arXiv)", "C_D Re^-1/2 extrapolation outside measured span (S32 assumption)", "Miln, Ward & Seebacher 2021 fast-start maxima 0.45-1.38 m/s, 120 fps, 23 C, best-of-4 (measured, full-text, figure-read)", "Miln 2021 U10 constant-acceleration sprint (measured; values unknown, ESM not accessed)", "Demesmay et al. 2025 adult escape maximal speed 157 +/- 27 cm/s controls, 240 fps manual tracking, 3.8 cm in 40 ms (measured, full-text)", "Widrick et al. 2018 Table 2 adult flume U_max 13.0-17.9 SL/s (compiled; primaries Plaut 2000, Seebacher & Walter 2012, Gilbert 2014, Conradsen listing-level)", "design standard length 30 mm (S32 implicit: fin height 9 mm = 0.3 SL; assumed)", "exit speed 1.38 m/s (S28/S32; held fixed here)", "S28 designed wing 192 mm2, CL_max 1.07, V_to 4.41 m/s at 0.25 g / 5.58 m/s at 0.40 g (derived, unmeasured)", "S28 frontal area 24 mm2", "S29 body water Cd 0.1-0.3 (assumed)", "caudal fin area 37.8 mm2 and chord 6 mm (assumed / Wakamatsu 2019 via S24)", "immersed fraction, CLz_max 1, contact angles, wing CD0 (S32 assumptions)", "Kyriakatos 2011 52 Hz (via S24; stroke counts only)", "inference: C-start peak is an upper bound and 30-s-stage flume U_max a lower bound on ~1 s stroke-averaged burst speed (unverified)", "challenge-75 120-fps under-read calculation 0.61-0.86x (relayed)"]}
```
