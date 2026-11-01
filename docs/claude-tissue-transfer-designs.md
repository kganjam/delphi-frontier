# Tissue and developmental simulations: transfer functions between scales and the experiments that would measure them

Harness `claude-tissue`, 2026-11-01. Branch `claude-tissue/sims-20261101`.

**Scope.** Everything below is **simulated**, not observed. The only observed data used are the specimen rows of
`artifacts/observed-allometry/source-observations.csv` (pectoral fin length vs standard length, SL): 49 flying fish
for anchoring and fitting, plus flying halfbeaks, halfbeaks and needlefish for the developmental-programme comparison. Turing-type results are
dimensionless. Mapping them to fin rays or scales is an **assumption**: the repo holds no measured ray spacing,
morphogen diffusivity or turnover rate. No simulation here validates a biological mechanism.

Each simulation folder `artifacts/simulations/claude-tissue-*/` contains:
- a figure
- a `manifest.json` (file hashes, code hashes, run list with exit codes)
- one receipt per run (command, exit code, seed, wall time, input and output hashes)

## Summary for the studio panel

**Developmental scale (organ proportions)** (`claude-tissue-dev-programme`, also `-identifiability`, `-fin-growth`).
- A growth-zone programme, dL/dSL = c within the observed sizes, links adult fin/SL to one coefficient c.
- c is 0.73 for flying fish (three species agree, 0.71–0.77), 0.25–0.40 for flying halfbeaks, 0.15 for halfbeaks and 0.08 for needlefish.
- The flying-fish difference is carried by c, not by an early offset. This holds only within the observed sizes, ≥ 1.7 cm SL.
- The data cannot tell which molecular parameters set c. A graded morphogen-dose series could: its predicted slope
  ranges from 0.08 to 0.99 across data-compatible regimes.

**Developmental and tissue scale (ray-like patterning)** (`-phase-map`, `-edge2d`, `-uniform2d`, `-uniform2d-y0`,
`-edge2d-cases`, `-edge2d-gamma`, `-fan`, `-fan-video`, `-growing-rd`, `-rd-wavelength`).
- In one generic Turing model (Schnakenberg), proximo-distal ray-like stripes appeared only with two things: kinetics near onset (deeper in, the
  pattern is spots) and growth along the fin axis.
- With growth confined to a narrow apical zone, the pattern forms bands parallel to the edge. Ray-like orientation needs
  a proliferating zone wider than about **one third of a pattern wavelength** at slow outgrowth (refined grid: 0.32 λ at
  γ = 2 and 0.35 λ at γ = 1), rising to about half a wavelength at 4× faster outgrowth (refined, γ = 1). Refinement also removed the γ = 2 failure window as a discretisation artifact.
  Coarse-grid values, biased upward: 0.37, 0.39 and 0.39 at three rate scales, and a
  prediction made from two of them was confirmed on the third (12 seeds each). The switch rises with outgrowth speed,
  reaching 0.48 λ at v = 0.4 (L_p* ≈ 3.9 + 3.3·v at γ = 1). This is partly a scaling consistency check, and grid
  sensitivity is under test. Above the switch, newly grown tissue is almost perfectly
  ray-like (distal-half A 0.94–1.00). The earlier γ = 2 failure window near L_p ≈ 10 was a coarse-grid artifact.
- With row insertion from a very short fold, orientation is lost above an outgrowth speed of about 0.2–0.4 pattern
  units. That threshold tracks λ·σ (pooled slope 0.50). A reversal of orientation behind a moving front is a known
  phenomenon.
- On a fan-shaped fold, slow distal growth gives radial stripes that multiply as the fan widens.
- 1-D runs: uniform growth gives frequency doubling, edge growth gives one-at-a-time insertion.

**Not established anywhere here:** that fin rays are a Turing pattern; the identity of any morphogen; any physical
length or time scale. Every Turing result is dimensionless and the kinetics are generic.

## 0. Priority deliverable: developmental programme → adult fin proportions (studio "developmental" scale)

The studio gap text asks for a model that links adult proportions to a developmental programme. The model is
`artifacts/simulations/claude-tissue-dev-programme/`, run by `dev_programme.py` (exit 0).

**Model.**
- Fin growth per unit body growth: dL/dSL = (r/s)∫₀ᴸ m/(K+m) dx.
- In the tip-saturated limit that the best fit to the flying-fish data runs to (section 4), though the profile does not exclude other regimes,, this becomes
  dL/dSL → c = (r/s)·√(D/k)·ln(1+p).
- So L = a + c·SL, and the **adult proportion is L/SL = c + a/SL → c**. The offset a is the *extrapolated* intercept
  of this phase, not a measured early fin length. A negative a, as for flying fish, means the linear phase cannot extend
  below the observed range.

**Fit.** Ordinary least squares per group on observed specimens, with a 2000-sample bootstrap (seed 20261101):

| Group | n | c (growth-zone output) | 95% CI | a (cm) |
|---|---|---|---|---|
| Flying fish | 49 | 0.729 | 0.704–0.750 | −0.33 |
| Flying halfbeak | 19 | 0.245 | 0.19–0.30 | 0.56 (CI −0.08 to 1.6) |
| Halfbeak | 22 | 0.152 | 0.14–0.17 | −0.13 |
| Needlefish | 19 | 0.075 | 0.07–0.09 | 0.33 |

**Decomposition.** At SL = 20 cm, flying fish exceed halfbeaks in fin/SL by 0.566. Of that, +0.576 comes from c and
−0.010 from a. Against flying halfbeaks the split is +0.484 from c and −0.045 from a. Within this model and **within the observed size range (≥ 1.68 cm SL)**, the adult proportion difference is carried by
the growth-zone coefficient c, not by the intercept. Whether flying fish also have an early larval head start cannot be
decided: their fin/SL is already about 0.54 at 1.68 cm, and no smaller specimens exist in the repo.

**Species-level check** (`dev_programme_species.py`, exit 0; answers the pseudoreplication point). Each species is fitted
separately, and group c is estimated by a two-stage bootstrap (species, then specimens; 4000 draws).
- **Flying fish:** all three species agree. *H. rondeleti* 0.711, *C. furcatus* 0.730, *E. volitans* 0.765.
- **Flying halfbeak:** the two species differ. *E. velox* 0.274, *O. micropterus* 0.397.
- **Contrasts on c, flying fish minus each group:**

| Comparison | Δc | 95% CI |
|---|---|---|
| vs flying halfbeak | +0.38 | 0.25–0.49 |
| vs halfbeak | +0.59 | 0.53–0.64 |
| vs needlefish | +0.65 | 0.59–0.70 |

The group difference survives species-level resampling. With only 2–3 species per group, these intervals are coarse,
and no phylogenetic covariance is modelled.

**Alternative model.** A power law L = b·SL^α, fitted by nonlinear least squares on the same raw-length scale (corrected
after review), is modestly preferred in every group, by ΔAIC 0.3 to 2.9.
- Flying fish: α = 1.07, a mild positive allometry.
- Halfbeak: α = 1.10. Needlefish: α = 0.86. Flying halfbeak: α = 0.79.

So the linear programme is an *interpretable* description, not the statistically preferred one. It offers a candidate
developmental reading of the coefficient (c as composite growth-zone output) that is **untested**. c lumps six
unmeasured parameters.

**What it does NOT establish.**
- A morphogen, or the parameters r, s, D, k, P, K individually.
- Growth trajectories: the specimens are cross-sectional, with species pooled within groups.
- Valid confidence intervals: there is no phylogenetic or species-level correction, so the bootstrap CIs are anticonservative.
- Regression dilution: ordinary least squares ignores measurement error in SL. That error is small next to the
  1.7–55 cm range, but it is unquantified.
- Anything below 1.68 cm SL.
- An evolutionary cause.
- Any aerodynamic consequence.

The flying-halfbeak group mixes two species with visibly different proportions.

**Experiment that tests it.** Longitudinal measurement of fin and body length in individually tracked juveniles
(rank 3 → 4) separates r from s inside c. The section-5 dose series then tells a saturated zone from a gradient-limited one.

## 1. rd-wavelength: kinetic parameters → pattern wavelength (molecular → tissue)

**Model.** Schnakenberg reaction–diffusion (a=0.1, b=0.9), 2-D periodic, IMEX pseudo-spectral.

**v2 run.** 256² grid, L=128, t=600 on one Nebius H100 (`aijob-e00n2jw5g99ejffr8t`, 147.5 s). The sweep covers 10 diffusion ratios d × 3 rate scales γ × 3 seeds, 90/90 rows collected.

**v1 defects, kept and marked superseded.**
- The L=32 domain resolved k only in steps of 0.196. Its "flat" wavelength-vs-d curve was a quantization artifact.
- The convergence control found 1 of 3 checked v1 cases still changing at t=150.

**Simulated transfer function.**
- **Rate scale:** λ ∝ γ^−0.505 (range −0.494 to −0.520 across d). This matches the exact scaling λ ∝ √(D_u/γ).
- **Diffusion ratio:** λ ∝ d^0.14 in the simulations, against d^0.21 for the linear-theory fastest mode.
- **Nonlinear selection:** the selected wavenumber is 3–18% above linear theory, so linear theory is not an adequate stand-in.
- **Convergence:** 82/90 runs end in the same k-shell at half time and at the end; the largest relative k change is 3.4%.

**Pattern type.** Near onset (d≈10) the pattern is stripes or labyrinth; for d ≥ 20 it is spots. Within this model, a ray-like (striped)
readout would need a near-onset regime or an anisotropy the model does not contain.

**Organism for wet-lab rungs.** FRAP, transgenes and live imaging are feasible in medaka or zebrafish, not in flying
fish. Flying-fish material is limited to fixed specimens and field-caught larvae, so flying fish would contribute only
measured ray spacing and fin-fold width.

**What converts it to biology.** λ_physical = λ_nondim × √(D_u / k_u), where D_u is activator diffusivity and k_u its
turnover rate. Neither is measured for any candidate fin-ray pathway in this repo.

**Experiment design.**
1. **Measure the scale factor.** Use FRAP or photoconversion of a tagged candidate ligand in the fin fold at the
   ray-patterning stage to get D_u and k_u. Combine with the measured ray spacing s_ray to infer λ_nondim, then check
   whether it falls inside the simulated band (6.5–19 in these units).
2. **Elasticity test.** Run a graded pharmacological or heat-shock dose series that changes the candidate pathway's
   effective reaction rate. The model predicts d log s_ray / d log γ ≈ −0.5, while ray *number* scales with fin-fold
   width at patterning. A slope near 0 rejects a γ-controlled Turing spacing for that pathway.
3. **Controls.** Use the same dose on a non-patterning readout (fin-fold area) to separate spacing changes from growth
   changes. Score blinded across replicate clutches.

## 2. growing-rd: domain growth → peak (ray-candidate) number (tissue → organ)

**v1.** 1-D Schnakenberg, growth 4× (W 12→48). Static controls gave 3–4 peaks depending on the seed; every growth
rate gave 4 peaks in all 5 seeds. Growth made the outcome reproducible but did not change the count.

**v2.** Growth 12× (W 12→144), growth times T ∈ {250, 1000, 4000}, d ∈ {15, 20, 30}, 5 seeds.
45/45 runs completed locally.

**Slow and moderate growth (T = 1000 and 4000).** Every seed follows the same exact
**frequency-doubling** sequence: 2 → 4 → 8 → 16 peaks, each peak splitting in place (see the kymographs).
- d = 15 and 20 end at 16 peaks, where W/λ* predicts 11.9 and 11.2.
- d = 30 ends at 8 peaks, where W/λ* predicts 10.3.

The final count is set by a power of two times the initial count, not by width. This reproduces the published
behaviour of Schnakenberg under uniform domain growth (Crampin, Gaffney & Maini 1999), which acts here as a
correctness check on the scheme rather than a new result.

**Fast growth (T = 250).** The events become irregular ±1 insertions and fusions, and the final count depends on the
seed: 13–16 at d = 15 and 10–16 at d = 20.

**Transfer function.** Peak number vs width is a staircase in powers of two, not a ramp. Its steps sit at widths set
by the kinetics (d), and the growth rate controls whether the staircase holds or breaks into noisy insertion.

**Counting limitation.** Peak counts use an interior-maximum rule, so edge peaks may be under-counted.

**v3: edge (apical) growth contrast**, added after the review noted that rays are added at the margins.
`edge_growth_rd.py`: the same kinetics, but the domain grows only by appending cells at one edge (W 12 → 144). The runs
cover 3 edge speeds (0.5, 0.1, 0.03, matching growth times of about 264, 1320 and 4400) × 3 values of d × 5 seeds.
All 45 runs completed, in three capped processes plus a merge, every exit code 0.

- **Event type.** Every peak is added sequentially at the growing edge (+1 events, max jump 1 in 44/45 runs) and
  never by doubling. The final count stays close to W/λ*: 8–12 peaks against 10.3–11.9 expected.
- **Regularity.** Spacing is highly regular, with CV ≤ 0.04.
- **Speed dependence.** Spacing *widens as the edge slows*. At d = 15 it goes from 12.0 to 13.7 (λ* 12.1); at d = 20 from
  13.1 to 15.1 (λ* 12.9); at d = 30 from 15.1 to 17.9 (λ* 14.0). That is up to +28% above the fastest linear mode.
- **Transfer function.** Under edge growth, ray number ≈ W / s(v), where spacing s rises as outgrowth speed v falls.
  Under uniform growth, the count is a power-of-two staircase.

**Discriminating prediction.** Margin-addition with spacing that depends on outgrowth speed (edge model) vs
synchronous splitting (uniform model). Slowing fin outgrowth, for example by temperature in medaka, should *widen* new
ray spacing under the edge model.

**Experiment design.**
1. **Longitudinal live imaging.** Image ray-primordium (or scale-primordium) markers in a growing fin fold of flying fish and
   in an outgroup with short fins. Score the insertion events: +1 at an edge, +1 in the interior, or near-doubling.
   The model's discriminating readout is the size distribution of jumps, not the final count.
2. **Growth-rate perturbation.** Temperature or nutrition shifts change the growth time T. A W/λ*-tracking mechanism
   predicts a final count independent of T. A doubling mechanism predicts counts locked to powers of two times the
   initial count.
3. **Biology check (argon review).** Teleost fin rays (lepidotrichia) are reported to be added sequentially at the fin
   margins, with distal growth by segment addition and branching, not by simultaneous splitting. The uniform-growth
   doubling regime is therefore probably *not* how basal ray number is set. It is kept as a rejected-mechanism
   contrast; an edge-growth model is the next model to build.
4. **Prediction to test.** Under these kinetics, uniform growth produces doubling, so peak spacing ends below λ*
   (W_END/16 = 9 vs λ* ≈ 11–12). If imaging shows rays added one at a time at an edge (not checked here against the
   developmental literature), that would argue for non-uniform (edge) growth or a different mechanism.
   That is a model-selection experiment, not a confirmation.

## 2b. Two dimensions: what turns a Turing pattern into proximo-distal "rays" (H100 runs)

**Phase map** (`claude-tissue-phase-map`, job `aijob-e00tqm60xz297scrcv`, COMPLETED, 110.9 s). The map covers an 8 × 8 grid
of the kinetic parameter b and the diffusion ratio d, with 3 seeds per cell.
- 18 of 64 cells are Turing-unstable.
- **Stripes appear only in the band next to onset** (the smallest unstable d for each b); spots fill the rest.
- So in this model, stripes of any orientation appear only near onset. Static patterning gives *unoriented* stripes
  (labyrinths), not rays.

**Distal-edge growth in 2D** (`claude-tissue-edge2d`, job `aijob-e00e9hk4jpkgxy6n3n`, COMPLETED, 1094.6 s). A 96-wide fold
grows from 8 to 192 rows at its distal edge. There are 4 seeds per condition, compared with a static fold patterned all
at once. The orientation index A runs from +1 (stripes along the growth axis, ray-like) through 0 (isotropic) to −1
(bands parallel to the edge).

| d | Edge speed 0.4 | Edge speed 0.1 | Edge speed 0.04 | Static |
|---|---|---|---|---|
| 10 (stripe regime) | −0.53 ± 0.16 (oblique / edge-parallel bands) | **0.99 ± 0.01** (9 PD stripes, all seeds) | **1.00 ± 0.00** | −0.06 ± 0.18 (labyrinth) |
| 20 (spot regime) | −0.08 | −0.08 | 0.01 | −0.03 |
| 30 (spot regime) | −0.10 | 0.00 | −0.13 | −0.02 |

**Reading.**
- In the stripe regime, *slow* distal growth turns an isotropic labyrinth into perfectly ray-like proximo-distal stripes.
- *Fast* growth instead lays down oblique or edge-parallel bands.
- In the two spot-regime cells tested (d = 20 and 30), directional growth did not turn spots into stripes.
- First reading, later revised by the controls below: under *edge* growth, ray-like stripes needed near-onset kinetics
  and outgrowth slower than a threshold between v = 0.1 and 0.4. The uniform-growth control shows that threshold is
  specific to the edge mode.

**Testable prediction.** If rays were laid down by such a mechanism, accelerating early fin-fold outgrowth past a
threshold would disorder ray orientation. Ray number across the fold would stay about width/λ, here 9.

**Uniform-growth control** (`claude-tissue-uniform2d`, job `aijob-e00ywezw2nkjrnkfxf`, COMPLETED, 696.2 s). The same fold,
speeds and seeds, but every row stretches instead of new rows being added at the edge.

| d | Uniform speed 0.4 | Uniform speed 0.1 | Uniform speed 0.04 |
|---|---|---|---|
| 10 | **0.99 ± 0.02** | **1.00** | **1.00** |
| 20 | −0.09 | −0.23 | −0.23 |
| 30 | −0.11 | −0.17 | −0.12 |

**Corrected reading** (the control changes the interpretation of the edge2d run):
- Proximo-distal stripes come from *growth along the proximo-distal axis* together with near-onset kinetics; edge-specific
  insertion is not needed. A start shorter than one wavelength (8 rows against λ ≈ 11) gives the cleanest result, but
  the starting-length test below shows it is not necessary.
- Fast *edge* growth is the condition that breaks the orientation (A = −0.53); uniform growth at the same speed
  keeps it (0.99).
- In this model, then, the edge mode adds a speed constraint that the uniform mode does not have.
- Neither mode turned spots into stripes in the two spot-regime cells tested.

**Prediction, revised.** If rays were laid down by such a mechanism, they would align with the axis of fold elongation.
Under marginal (edge) outgrowth, but not uniform outgrowth, speeding up outgrowth beyond a threshold would disorder them.
The follow-up job `claude-tissue-edge2d-cases` narrows that threshold and tests other stripe-regime kinetics.

**Speed threshold and other kinetics** (`claude-tissue-edge2d-cases`, job `aijob-e00ya0sp5zmqdstjxs`, COMPLETED, 978.3 s).
This extends the edge-growth run to two more stripe-regime cells from the phase map, with 4 seeds each.

| Kinetics | Edge speed 0.4 | 0.3 | 0.2 | 0.15 | 0.1 | 0.04 | Static |
|---|---|---|---|---|---|---|---|
| b = 0.9, d = 10 | −0.53* | −0.33 | 0.51 | 0.67 ± 0.47 | 0.99* | 1.00* | −0.06* |
| b = 1.1, d = 13 | −0.59 | — | 0.59 | — | 0.98 | 1.00 | −0.25 |
| b = 1.8, d = 30 | −0.63 | — | 0.51 | — | 0.99 | 1.00 | −0.15 |

\* from the first edge2d run.

**Result.** The edge-growth transition is **the same for all three stripe-regime kinetics**:
- At edge speeds of 0.1 or below, stripes are fully proximo-distal (ray-like).
- Around 0.2 the stripes are partly oriented.
- At 0.3–0.4 the pattern becomes oblique or edge-parallel bands.

The threshold, roughly 0.15–0.25 wavelength-units of new tissue per unit pattern time, is similar for these three
cells. All three lie near the onset boundary of one model, so this is *not* evidence of model independence.

**Does the threshold scale with pattern-formation speed?** (`claude-tissue-edge2d-gamma`, job `aijob-e00kgg8wfcq6694170`,
COMPLETED, 668.9 s; `threshold_scaling.py`). Run at b = 0.9, d = 10 with rate scale γ = 0.5 and 2; the γ = 1 points
are pooled from the earlier runs. Linear theory gives λ·σ_max = 0.45, 0.64 and 0.90 for γ = 0.5, 1 and 2, which scales
as √γ.

| γ | Edge speed where A crosses 0 | Where A crosses 0.5 |
|---|---|---|
| 0.5 | 0.22 | 0.16 |
| 1 | 0.26 | 0.20 |
| 2 | 0.41 | 0.19 |

- **The A = 0 crossing** (where orientation is lost) rises with γ, with a log-log slope of 0.47. That is close to the
  0.5 predicted if outgrowth must stay slower than pattern formation, v* ∝ λ·σ_max.
- **The A = 0.5 crossing** does not scale. The γ = 2 points near 0.2 are noisy (SD ≈ 0.5).

**Reading.** The evidence is weak:
- the slope rests on three interpolated points;
- the A = 0.5 crossing does not scale;
- the domain width was not rescaled with λ, so it held about 6, 9 and 13 stripes for γ = 0.5, 1 and 2, which is a confound.

**What it would mean.** If confirmed, the measurable prediction is a single dimensionless ratio: outgrowth speed
divided by (ray spacing × patterning rate). Ray orientation should degrade when that ratio exceeds about 0.3–0.4,
reading the threshold as v*/(λσ).

**Starting-length test** (`claude-tissue-uniform2d-y0`, job `aijob-e00dy3kv6127nqa3dj`, COMPLETED, 307.9 s). Uniform growth
at d = 10 to the same final length 192, starting from different lengths Y0. λ ≈ 11, so Y0 = 96 starts about 9
wavelengths long.

| Starting length Y0 | 8 | 24 | 48 | 96 |
|---|---|---|---|---|
| A at speed 0.4 | 0.99 | 0.93 | 0.93 | 0.87 |
| A at speed 0.1 | 1.00 | 0.98 | 0.92 | 0.74 ± 0.20 |

**Reading.** The short-start hypothesis is only partly supported. A start shorter than one wavelength gives perfect
stripes, but even a long starting fold ends mostly proximo-distally oriented with residual defects. The dominant
orienting factor is **anisotropic stretching along the growth axis**; a short start removes the remaining defects.

**Fan-shaped fold** (`claude-tissue-fan`, job `aijob-e00jd38fyzb9kahcda`, COMPLETED, 777.2 s). An annular sector
(R0 = 30, final radius 190, Θ = 1.2 rad) grows at its distal arc, at d = 10 with 4 seeds. Stripes are counted along the
arc at five radii (45 to 174) and compared with r·Θ/λ* (5.1 to 19.5).

| Condition | Stripes along the arc, inner → outer | Radial orientation A |
|---|---|---|
| Slow edge growth (0.1) | 2.5 → 5.5 → 9.8 → 13.2 → 17.2 | +0.60 |
| Fast edge growth (0.4) | 2.8 → 2.8 → 3.5 → 3.8 → 6.5 | −0.88 |
| Static | 2.8 → 3.5 → 6.2 → 8.8 → 11.0 | −0.20 |

- **Slow distal growth.** Stripes run radially (ray-like) and are **added as the fan widens**, roughly parallel to
  the fixed-spacing line, and new stripes appear distally.
- **Fast growth.** Gives circumferential arcs.
- **Static.** Gives a mixed pattern.
- **Counting caveat.** The innermost count is limited by the short inner arc, and the counting uses a simple
  ring-peak rule.

**Prediction.** If rays were laid down by such a mechanism under slow outgrowth, ray number would rise with distal fin
width at fixed spacing. Insertion or branching events would sit distally. That is testable against how rays are added
or branch in widening pectoral fins (not checked here).

**Reviewer-requested control: continuous growth in a distal proliferation zone, from a long start**
(`claude-tissue-pzone`, job `aijob-e00st593zksc50npka`, COMPLETED, 883.0 s). The fold starts at length 48 (more than 4
wavelengths) and grows to 192 by finite-volume growth confined to the distal L_p of tissue. New tissue inherits the
local field, so no rows are inserted at steady state. There are 12 seeds per condition; values are mean A with 95% CI.

| Proliferation zone | v = 0.1 | v = 0.25 | v = 0.4 |
|---|---|---|---|
| L_p = 2 (apical) | −0.78 ± 0.05 | −1.00 | −1.00 |
| L_p = 12 (≈ 1 λ) | 0.66 ± 0.06 | 0.51 ± 0.08 | 0.39 ± 0.10 |
| L_p = 48 | 0.86 ± 0.02 | 0.88 ± 0.02 | 0.83 ± 0.04 |
| Whole length (uniform) | 0.94 ± 0.03 | 0.95 ± 0.01 | 0.94 ± 0.01 |
| Static | 0.02 ± 0.11 | | |

**Reading.** This changes the edge-growth conclusion.
- From a long start, a **narrow apical zone gives bands parallel to the distal edge at every speed tested**.
- Ray-like proximo-distal stripes need a proliferation zone **wider than about one wavelength**. Orientation improves
  steadily with zone width, and for wide zones the speed hardly matters.
- The ray-like stripes under slow row-insertion growth (edge2d) therefore depended on the short 8-row start and/or the
  row-insertion scheme. A run of the same finite-volume model from an 8-row start is queued to separate the two
  (`claude-tissue-pzone-y8`).

**Limitation.** With L_p = 2 the zone is about one cell wide, so the effective elongation was slightly below v:
final length 187, not 192.

**Testable prediction, revised.** If rays were patterned by such a mechanism, ray-like orientation would need
proliferation spread over a distal zone at least about one ray-spacing long. That can be checked with a proliferation
marker (EdU or PCNA) in the fin fold at the time rays are laid down.

**Zone-width sweep and short-start control** (`claude-tissue-pzone-lp`, job `aijob-e00ysdr0hbbm0s2pqe`, 601.4 s;
`claude-tissue-pzone-y8`, job `aijob-e00fz6wvwm0p4bcz9f`, 624.3 s; both COMPLETED; 12 seeds; same script as `pzone`).

Long start (Y0 = 48), v = 0.1, mean orientation A:

| L_p | 2 | 4 | 6 | 8 | 12 | 16 | 24 | 48 | Uniform |
|---|---|---|---|---|---|---|---|---|---|
| A | −0.78 | −0.49 | **0.63** | 0.71 | 0.66 | 0.72 | 0.75 | 0.86 | 0.94 |

- **Sharp switch.** The orientation flips from edge-parallel to proximo-distal between L_p = 4 and 6, at about half a
  wavelength (λ ≈ 11).
- **Above the switch,** orientation improves gradually with zone width.

Short start (Y0 = 8):

| | L_p = 2 | L_p = 12 | Uniform |
|---|---|---|---|
| v = 0.1 | 0.52 ± 0.27 | 0.98 | 0.99 |
| v = 0.4 | −0.79 | 0.92 | 0.95 |

Static control: 0.02.

**Reading.**
- **A short start helps:** at L_p = 12 and v = 0.1, A rises from 0.66 to 0.98.
- **Row insertion also mattered:** under continuous apical growth (L_p = 2) at slow speed, the short start reaches only
  0.52, against 0.99 when rows were inserted at the edge.
- **So the clean rays in the first edge-growth run came from both** the very short start and the row-insertion scheme.
- **The robust result across schemes and starts:** ray-like orientation needs a proliferating zone wider than about
  half a pattern wavelength. A narrower apical zone gives bands parallel to the edge.

**Does the zone-width switch scale with the wavelength?** (`claude-tissue-pzone-g0p5`, job `aijob-e00b14p611r3epqsx2`,
860.4 s; `claude-tissue-pzone-g2p0`, job `aijob-e00ae8ktbgy1rmmn9d`, 855.2 s; both COMPLETED; 12 seeds; v = 0.1, long
start.)

| γ (λ) | L_p = 3 | 4 | 5 | 6 | 8 | 10 | 12 | Static |
|---|---|---|---|---|---|---|---|---|
| 0.5 (λ ≈ 15.8) | −0.62 | −0.50 | −0.47 | −0.48 | **0.53** | 0.49 | 0.54 | −0.03 |
| 2 (λ ≈ 7.9) | **0.56** | 0.68 | 0.50 | 0.39 | 0.61 | **−0.49 ± 0.07** | 0.61 | −0.04 |

**Switch position against the λ/2 prediction:**

| γ | Predicted λ/2 | Observed switch |
|---|---|---|
| 0.5 | 7.9 | between L_p = 6 and 8 |
| 1 | 5.5 | between 4 and 6 |
| 2 | 3.9 | below 3 |

All three brackets contain λ/2, so **L_p* ≈ λ/2** is consistent with the data. This is a coarse bracket, not a fit.

**Anomaly, and a metric problem it exposed.** At γ = 2, L_p = 10 (≈ 1.3 λ) is negative in all 12 seeds while 8 and 12
are positive. The snapshots show the cause:
- the proximal part of the fold keeps the pattern that formed in the 48-row starting fold (bands or spots);
- only the newly grown distal tissue carries proximo-distal stripes;
- the whole-domain A mixes the two, and at L_p = 10 the proximal half locked into edge-parallel bands.

So the whole-domain A numbers above understate how the newly grown tissue is oriented. The γ = 2 and γ = 1 follow-ups
were cancelled before running and resubmitted with a regional-metric script (`pzone_regional_gpu.py`). It reports A for
the distal half, the proximal quarter, and the tissue descended from growth: `claude-tissue-pzone-g2r` and
`claude-tissue-pzone-g1r`, jobs `aijob-e00gczy89devejh5js` and `aijob-e00zqkxgb98px1a1mf`.

**Regional orientation** (`claude-tissue-pzone-g2r`, job `aijob-e00gczy89devejh5js`, 726.3 s; `claude-tissue-pzone-g1r`, job
`aijob-e00zqkxgb98px1a1mf`, 741.7 s; both COMPLETED; 12 seeds; v = 0.1; long start). Values are A in the **distal half**
(grown tissue), mean ± 95% CI:

| γ | L_p = 2 | 3 | 4 | 6 | 8 | 10 | 12 | 48 | Uniform | Static |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | −0.04 ± 0.40 | **0.97** | | 0.98 | 0.97 | 1.00 | 0.93 | −0.04 |
| 2 | −0.64 | **0.88** | | 0.94 | 0.99 | **0.01 ± 0.13** | 0.99 | | | −0.14 |

The γ = 1 whole-domain values reproduce the earlier run exactly, a determinism check.

**Reading.**
- Measured on the newly grown tissue, ray-like orientation is close to perfect (0.94–1.00) once the proliferation zone
  is wider than the switch.
- The switch sits at L_p ≈ 2.5 for γ = 2 (λ ≈ 7.9), ≈ 5 for γ = 1 (λ ≈ 11) and ≈ 7 for γ = 0.5 (λ ≈ 15.8, from the
  whole-domain run). That is about 0.6–0.9 × λ/2: **the switch scales with the pattern wavelength.**
- The proximal quarter keeps the starting-fold pattern; its A is mostly negative.

**Later resolved as a grid artifact (see Grid refinement).** At γ = 2, L_p = 10 (≈ 1.3 λ), even the distal half is unoriented (0.01 ± 0.13 over 12 seeds),
while L_p = 8 and 12 give 0.99. The follow-up `claude-tissue-pzone-g2r2` (job `aijob-e00zamme1qkx4bgsxj`, COMPLETED, 403.3 s)
shows the dip is isolated to exactly L_p = 10:

| L_p | 9 | 10 | 11 |
|---|---|---|---|
| Distal A | 0.98 | 0.01 (reproduced) | 0.99 |

A single integer width failing points to a discretisation effect: the zone boundary is a step applied to cell
centres. Non-integer widths were then tested (`claude-tissue-pzone-g2r3`, job `aijob-e00xeqsd6t1y722cjc`, COMPLETED, 625.3 s):

| L_p | 9.7 | 9.9 | 10.0 | 10.1 | 10.3 |
|---|---|---|---|---|---|
| Distal A | 0.34 | −0.01 | 0.01 | 0.66 | 0.97 |

**The integer-artifact explanation is ruled out.** Orientation fails smoothly across a narrow window about 0.5 wide,
centred near L_p ≈ 10 ≈ 1.27 λ. A resonance between zone width and wavelength is possible but unverified. A run at γ = 1 near 1.27 λ ≈ 14 tested whether the window recurs (`claude-tissue-pzone-g1res`, job
`aijob-e00sjqac5mkk26xx38`, COMPLETED, 632.4 s).

| L_p | 13 | 13.5 | 14 | 14.5 | 15 |
|---|---|---|---|---|---|
| Distal A | 0.97 | 0.95 | 0.98 | 0.97 | 0.96 |

**There is no window at γ = 1.** The γ = 2 failure near L_p ≈ 10 is therefore not a general zone-to-wavelength
resonance. It remained unexplained at that point. **The grid-refinement run below later showed it to be a coarse-grid discretisation artifact.** **γ = 0.5 regional run** (`claude-tissue-pzone-g05r`, job `aijob-e00wxw6fcavbvv05j5`, COMPLETED, 760.2 s):

| L_p | 4 | 6 | 7 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|
| Distal A | −0.12 | −0.10 | **0.81** | 0.93 | 0.97 | 0.98 |

The switch lies between L_p = 6 and 7.

**Switch estimates across rate scales:**

| γ | λ | Switch L_p* | L_p* / λ |
|---|---|---|---|
| 2 | 7.9 | ≈ 2.5 | 0.32 |
| 1 | 11 | ≈ 5 | 0.45 |
| 0.5 | 15.8 | ≈ 6.5 | 0.41 |

The switch grows with the wavelength at roughly 0.3–0.45 λ. The brackets are about 1 unit wide, so a precise scaling
exponent is not determined.

**Finer γ = 1** (`claude-tissue-pzone-g1f`, job `aijob-e00qgy5b2vwv66xzjw`, COMPLETED, 397.6 s):

| L_p | 4 | 4.5 | 5 | 5.5 |
|---|---|---|---|---|
| Distal A | −0.04 | 0.79 | 0.91 | 0.97 |

The γ = 1 switch is therefore at about **4.25 ≈ 0.39 λ**.

**Finer γ = 2** (`claude-tissue-pzone-g2f`, job `aijob-e00rp3a4jf55jhdwq2`, COMPLETED, 392.5 s):

| L_p | 2.25 | 2.5 | 2.75 | 3 (earlier run) |
|---|---|---|---|---|
| Distal A | −0.82 | −0.77 | −0.99 | 0.88 |

The γ = 2 switch is sharp, between 2.75 and 3: about **2.9 ≈ 0.37 λ**.

So two rate scales give **L_p* ≈ 0.37–0.39 λ**, which predicts about 6.0 at γ = 0.5.

**Finer γ = 0.5** (`claude-tissue-pzone-g05f`, job `aijob-e00hypmth0jdhj7zkb`, COMPLETED, 397.1 s):

| L_p | 6 (earlier run) | 6.25 | 6.5 | 6.75 |
|---|---|---|---|---|
| Distal A | −0.10 | 0.54 | 0.71 | 0.84 |

The switch is about **6.1 ≈ 0.39 λ**. **The prediction holds.**

**Result.** Across a fourfold change in rate scale (λ from 7.9 to 15.8), the proliferation zone width at which newly
grown tissue switches from edge-parallel bands to ray-like proximo-distal stripes is

  **L_p* ≈ 0.38 λ** (0.37, 0.39, 0.39).

That is a dimensionless rule: newly grown tissue is ray-like only when the proliferating zone is wider than about 0.4
pattern wavelengths. Below it, the tissue is unoriented or, for the narrowest zones, banded parallel to the edge.

**Review of this rule** (`gemini-4-argon`; saved as `artifacts/simulations/claude-tissue-pzone/review-gemini-4-argon-rule.txt`).
Accepted, and how each point is handled:
1. **Partly expected from scaling.** Changing γ rescales length (λ ∝ γ^−1/2) and time. Because v was held fixed in
   absolute units, the dimensionless speed changed too, so a constant L_p*/λ also says the switch is insensitive to
   speed over that range. A direct speed test followed (`claude-tissue-pzone-g1v25`, job `aijob-e00ersmqcfgkf5s3ye`, COMPLETED, 325.0 s), at
γ = 1 with v = 0.25:

| L_p | 3.5 | 4 | 4.5 | 5 | 6 |
|---|---|---|---|---|---|
| Distal A | −0.83 | −0.83 | −1.00 | 0.52 | 0.88 |

- The switch is about **4.75 ≈ 0.43 λ**, against about 4.25 ≈ 0.39 λ at v = 0.1.
- So a 2.5× faster outgrowth moves the switch up by roughly 12%, a modest dependence on speed.
- Below the switch, faster growth gives true edge-parallel bands rather than unoriented tissue.
- **v = 0.4** (`claude-tissue-pzone-g1v40`, job `aijob-e00snmkfw2d3s4kfbe`, COMPLETED, 242.4 s): distal A is −1.00 at
  L_p = 4.5, −0.97 at 5.0, 0.50 at 5.5, 0.74 at 6.0 and 0.84 at 7.0. The switch is about **5.25 ≈ 0.48 λ**.

**Speed dependence at γ = 1:**

| v | 0.1 | 0.25 | 0.4 |
|---|---|---|---|
| L_p* | 4.25 | 4.75 | 5.25 |
| L_p* / λ | 0.39 | 0.43 | 0.48 |

Roughly linear, **L_p* ≈ 3.9 + 3.3·v** (three points). The rule therefore needs a speed term:
**L_p* ≈ 0.35 λ + c·v**, where c is a time scale of a few pattern units. A γ = 2 run at v = 0.25 (`claude-tissue-pzone-g2v25`, job `aijob-e00jxmjjpzbr3wwx7b`, COMPLETED, 310.3 s) tested
whether this collapses across rate scales:

| L_p | 2.75 | 3.0 | 3.25 | 3.5 | 4.0 |
|---|---|---|---|---|---|
| Distal A | −1.00 | 0.55 | 0.57 | 0.65 | 0.87 |

- The switch stays between 2.75 and 3.0, the same as at v = 0.1, so **no shift is detected** at this 0.25 resolution.
- That is consistent with a speed term c·v whose time scale c shrinks as 1/γ (pattern time). At γ = 2 the expected
  shift would be about 0.25, within one bin.
- **γ = 2, v = 0.4** (`claude-tissue-pzone-g2v40`, job `aijob-e00fzv2zsdj29g7zct`, COMPLETED, 241.7 s):

  | L_p | 2.75 | 3.0 | 3.25 | 3.5 | 4.0 |
  |---|---|---|---|---|---|
  | Distal A | −1.00 | −0.97 | −0.97 | −0.07 | 0.64 |

  The switch is about 3.6, up about 0.7 from v = 0.1. The predicted shift was about 0.5, assuming a speed term that
  scales with pattern time (1/γ), so it roughly fits. These are coarse-grid values; the refinement runs above show the
  coarse grid biases γ = 2 switch positions upward.
2. **Below the switch is not always "bands".** At γ = 1 and 0.5 the tissue just below the switch is *unoriented*
   (distal A ≈ −0.1 to 0). Edge-parallel bands appear only for the narrowest zones, for example L_p ≤ 2.75 at γ = 2.
3. **Resolution.** At γ = 2 the switch zone is only 2–3 cells wide, so "0.37" is not resolved to two digits. A
   grid-refinement run at γ = 2 with half the cell size (same physics) is queued. Until it returns, read the rule as
   **L_p* ≈ 0.4 λ, with grid sensitivity untested**.
4. **Statistics.** 95% CIs near the switch are wide (±0.26 at γ = 0.5, L_p = 6.25 to 6.5). They are listed in each
   `claude-tissue-pzone-*` manifest card.
5. **The unexplained γ = 2 window** lowers confidence in the scheme until it is resolved; the refinement run also
   covers it.
6. **Possible physical reading** (reviewer's, not tested here): a zone narrower than about half a stripe period acts
   like a moving boundary that sheds bands parallel to it, while a wider zone can carry the transverse mode.
   This links the rule to front-locking in apical-growth models.

Other caveats: one model family (Schnakenberg), one diffusion ratio (d = 10), mostly one speed (v = 0.1).

**Rate-scale refinement** (`claude-tissue-edge2d-gamma-fine`, job `aijob-e00qha72mgcdbtqp1b`, COMPLETED, 489.9 s).
- Finer speeds near the threshold, re-running the same script with the same seeds. The γ = 1 points at speeds 0.2 and
  0.3 reproduce the earlier run exactly, a determinism check.
- **Pooled**, the A = 0 crossing scales with γ at log-slope 0.50, matching the √γ prediction. The A = 0.5 crossing
  still does not scale (0.13).
- So "orientation lost" tracks λ·σ, while "partly oriented" is noise-dominated: SD 0.3–0.5 near the threshold with
  4 seeds. This applies to the row-insertion scheme only (see the proliferation-zone control above).

**Grid refinement** (`claude-tissue-pzone-refine`, job `aijob-e00ffdpmy003ye6fvv`, COMPLETED, 1526.5 s). Run at γ = 2,
v = 0.1, with the same physics at **half the cell size**: grid lengths doubled, diffusivities × 4, time step ÷ 4.
12 seeds; distal-half A:

| Physical L_p | Coarse grid | Refined grid |
|---|---|---|
| 2.75 | −0.99 | **0.91 ± 0.03** |
| 3.0 | 0.88 | 0.92 ± 0.02 |
| 10 | 0.01 | **0.93 ± 0.03** |

**This corrects two earlier statements.**
1. **The γ = 2 failure window near L_p ≈ 10 was a discretisation artifact.** It disappears on the refined grid, so the
   reviewer's suspicion was right.
2. **The γ = 2 switch is grid-sensitive.** On the refined grid it lies **below 2.75** (< 0.35 λ). The coarse-grid
   value of 0.37 λ was an overestimate caused by resolving the zone with only 2–3 cells.

So the rule **L_p* ≈ 0.4 λ is an upper estimate** until refined runs bracket the switch. Two follow-ups are queued:
a refined γ = 1 run at physical L_p = 3.5–4.5 (`claude-tissue-pzone-refine-g1`), and a refined γ = 2 run with a lower
bracket (`claude-tissue-pzone-refine-g2b`).

**Refined γ = 1** (`claude-tissue-pzone-refine-g1`, job `aijob-e00w7ytqha1g4er39e`, COMPLETED, 1589.7 s). Half cell
size, v = 0.1 physical; distal A:

| Physical L_p | 3.5 | 4.0 | 4.5 |
|---|---|---|---|
| Refined grid | −0.21 | 0.51 | 0.86 |
| Coarse grid | — | −0.04 | 0.79 |

- The refined switch is about **3.8 ≈ 0.35 λ**, against 4.25 on the coarse grid: a downward shift of about 10%.
- With about 4 cells across the zone at γ = 1, grid sensitivity is moderate. It is larger at γ = 2, where the zone is
  only 2–3 cells.
**Refined γ = 2, lower bracket** (`claude-tissue-pzone-refine-g2b`, job `aijob-e00s5meh1qdnxcst63`, COMPLETED, 1526.2 s);
distal A:

| Physical L_p | 2.0 | 2.25 | 2.5 | 2.75 (earlier refined run) |
|---|---|---|---|---|
| Distal A | −0.73 | −0.76 | 0.09 ± 0.37 | 0.91 |

The refined switch is about **2.55 ≈ 0.32 λ**.

**Refined-grid rule.**

| γ | Refined switch | L_p* / λ |
|---|---|---|
| 2 | ≈ 2.55 | 0.32 |
| 1 | ≈ 3.8 | 0.35 |

So **L_p* ≈ 0.33 λ (one third of a pattern wavelength) at slow outgrowth**. The coarse-grid values (0.37–0.39 λ)
were biased upward by under-resolving the zone. **Refined speed term** (`claude-tissue-pzone-refine-g1v40`, job `aijob-e00f85t1emb5ty63tb`, COMPLETED, 649.9 s), at
γ = 1 with physical v = 0.4; distal A:

| Physical L_p | 4.5 | 5.0 | 5.5 |
|---|---|---|---|
| Distal A | −0.65 | −0.41 | 0.50 |

- The refined switch is about **5.4 ≈ 0.5 λ**, against 3.8 ≈ 0.35 λ at v = 0.1.
- The speed dependence survives refinement and is somewhat stronger: a slope of about 5 per unit speed, against about
  3.3 on the coarse grid.
- **Refined rule:** L_p* ≈ λ/3 at slow outgrowth, rising to about λ/2 at v = 0.4.

**Refined γ = 0.5** (`claude-tissue-pzone-refine-g05`, job `aijob-e00v75w09fwhswm2e1`, COMPLETED, 1578.8 s), physical
v = 0.1; distal A:

| Physical L_p | 5.0 | 5.5 | 6.0 |
|---|---|---|---|
| Distal A | −0.20 | −0.26 | −0.40 |

All three are unoriented, with wide CIs (±0.43), so the refined switch is **at or above 6.0 (≥ 0.38 λ)**.

**Reading.** On the refined grid, L_p*/λ rises as γ falls: 0.32 (γ = 2), 0.35 (γ = 1), ≥ 0.38 (γ = 0.5). The speed
term explains this. Physical v was fixed at 0.1, so the dimensionless speed v/√γ is about 0.07, 0.10 and 0.14
respectively, and faster dimensionless outgrowth pushes the switch up (refined γ = 1 at v = 0.4: 0.5 λ).

So **the switch is one function of dimensionless speed, not a single constant**: about λ/3 at the slowest speeds,
rising to about λ/2 at 4× faster outgrowth. An upper-bracket refined γ = 0.5 run is running (`claude-tissue-pzone-refine-g05b`).

**Smooth zone edge** (`claude-tissue-pzone-smooth`, job `aijob-e00k9ebxtrnpnnmpe3`, COMPLETED, 613.7 s). The step-shaped
zone is replaced by a logistic edge of width 1, and growth is normalised so total elongation is exactly v (final length
exactly 192). γ = 1, v = 0.1, coarse grid, 12 seeds; distal A:

| L_p | 3.5 | 4.0 | 4.5 | 5.0 | 6.0 |
|---|---|---|---|---|---|
| Distal A | 0.81 | 0.88 | 0.87 | 0.96 | 0.98 |

**Reading.**
- With a smooth edge, newly grown tissue is already ray-like at L_p = 3.5. With a step edge, the switch was 4.25 on
  the coarse grid and 3.8 refined.
- **So the switch depends on how sharp the zone edge is, not only on its width.** "About λ/3" holds for a sharp step
  edge; a softer edge gives rays from narrower zones.
- The smooth-edge lower bracket (L_p = 1.5–3.0) is running (`claude-tissue-pzone-smooth-b`).
- For biology, the comparison to make is between the sharpness of the distal proliferation boundary and the ray
  spacing, not just the zone width.

**Review of section 2b** (`gemini-4-argon`; text saved in `artifacts/simulations/claude-tissue-edge2d/`). Accepted and acted on:
1. **Prior work.** A reversal of stripe orientation behind a moving front above a critical speed is a known phenomenon;
   the reviewer cites prior analyses such as Míguez et al. 2006 and Krause et al. 2021, which I have not checked here.
   The threshold reported above is a numerical instance of that, not a new finding.
2. **"Model-independent."** Withdrawn.
3. **√γ scaling.** Downgraded to weak, with the width confound stated.
4. **What A measures.** It is an orientation measure only: spots and an isotropic labyrinth both give A ≈ 0. Pattern type
   comes from the phase-map component density.
5. **New-row initialisation.** Rows are added at the homogeneous steady state plus 1% noise, which creates a front.
   Fast edge growth producing edge-parallel bands is that front's signature.
6. **Fin biology.** The reviewer states that teleost rays branch apically, so interior insertion in the fan run may not
   match pectoral-fin ontogeny (not checked here).
7. **Quasi-1D start.** Partly answered already by the starting-length test, where long starts still orient
   (A 0.74–0.87). The reviewer's main requested control is queued: a long start with a continuous proliferation zone
   of variable width (apical to uniform), using a finite-volume growth scheme and 12 seeds.

## 3. fin-growth: morphogen production → pectoral/SL ratio (molecular → organ)

**Model.** 1-D quasi-steady distal-source gradient m(x) with a saturating local growth law. The growth law is declared,
not sourced. SL grows linearly. The rate r is anchored so the baseline equals the observed flying-fish mean ratio
0.717 at SL > 15 cm (observed range 0.656–0.757, n=13). That is an anchor, not a validation.

**Simulated elasticities of fin/SL at SL = 24 cm** (from ×0.5 and ×2 one-at-a-time perturbations):

| Parameter | Elasticity |
|---|---|
| Production P | +0.70 |
| Receptor threshold K | −0.70 (exact P/K symmetry) |
| Decay k | −0.82 |
| Diffusivity D | +0.12 |
| Growth rate r | +1.01 |
| Body growth s | −1.01 (exact r/s symmetry) |

**Shape mismatch.** The baseline log-log slope is 1.29, against an observed 1.06 for flying fish. The anchored
baseline has the wrong shape.

**Video.** `fin-growth.mp4` shows baseline and morphogen ×2 / ×0.4 fins growing against SL.

## 4. identifiability: what the observed allometry pins down

**v1 defects, superseded.**
- Its rank-4 result was a time-step artifact.
- Its fit sat on a parameter bound.

**v2.** The model depends on (P, D, k, K, r, s) only through p = P·l/(D·K), l = √(D/k) and ρ = r/s.
The native Jacobian has rank 3 of 6: singular values 5.05, 0.45, 0.028, then 9e−7 and below, with a
finite-difference noise floor of 2e−4.

**Best fit to the 49 rows.** The fit runs to the tip-saturated limit: p ≈ 7e9, l ≈ 0.009 cm, ρ ≈ 4.0 per cm, with a
residual σ of 0.081 log10. In that limit dL/dSL → ρ·l·ln(1+p), which takes the value 0.81. This fit has L0 fixed and is
misspecified; with L0 free, section 0's linear fit gives c = 0.729. The best fit lies on an unphysical boundary
(p → 7e9), so read it as "the data prefer the saturated limit", not as a parameter estimate.

**Profile-likelihood 95% intervals** (Gaussian iid assumption):

| Parameter | 95% interval | Constrained? |
|---|---|---|
| p | [1, 1e8] | No: open at both ends of the grid |
| l | [0.002, 20] cm | Only from below, weakly |
| ρ | ≥ 1.5 per cm | Only from below |

In practice the cross-sectional allometry pins about one combination, not three.

**Model misspecification found.** Freeing the initial fin length L0 (fixed at 0.45 cm at SL = 1.5 cm in fin-growth)
cuts RSS from 0.298 to 0.116, a 46-unit deviance improvement. The observed flying-fish fin/SL is already 0.54–0.76
at SL 1.7–3.0 cm. The fin-growth simulation starts at fin/SL = 0.30, a value the data contradict. Section 0 shows
the data are consistent with near-isometric growth and a high growth coefficient across the observed range
(log-log slope 1.06). An elongation burst below that range is neither shown nor excluded. Whether any burst happens below 1.7 cm SL is untestable with the repo's specimens.

**Readout ladder** (local Jacobian rank of 6 when each readout is added; this is the measurement design):

| Readouts | Rank of 6 | What the new rung adds |
|---|---|---|
| Cross-sectional L(SL), the current data | 3 | Only p, l and ρ, and practically fewer |
| + Longitudinal, time-stamped individuals L(t), SL(t) | 4 | Separates r from s |
| + Imaged gradient length | 4 | No new direction; the smallest retained singular value rises from 0.03 to 0.20, so the existing ones become much better determined |
| + FRAP / photoconversion kinetics | 5 | Separates D from k |
| + Calibrated concentration and receptor dose-response | 6 | Separates P from K |

The FRAP and dose-response rungs are structural, derived from the model equations; those experiments are not simulated.

## 5. Transfer regimes: one dose series that the allometry cannot replace

**Run.** `transfer_regimes.py`, exit 0. For each gradient length l on a grid, (p, ρ, L0) are re-fitted to the 49
flying-fish rows with L0 free. Each fitted regime is then perturbed with graded morphogen production (×0.25 to ×4),
and the response of fin/SL at SL = 24 cm is recorded.

**Result.** Six of seven gradient lengths fit the data within a deviance of 3.84; l = 0.003 cm is rejected with 8.9.
Their dose responses differ by more than tenfold:

| Gradient length l | Δ deviance | Production elasticity of fin/SL | ×4 production gives |
|---|---|---|---|
| 0.01 cm | 0.95 | 0.08 | ×1.11 |
| 0.03 cm | 1.0 | 0.22 | ×1.30 |
| 0.1 cm | 0.04 | 0.99 | ×4.6 |
| 0.3 cm | 0.92 | 0.93 | ×3.8 |
| 1 cm | 0.49 | 0.70 | ×2.4 |
| 3 cm | 0.0 | 0.87 | ×3.4 |

At l = 0.1 and 0.3 cm, ρ sits on its upper fit bound (54.6), so those two rows are bound-limited. Where a fit is on a
bound, the χ² 3.84 cutoff is not asymptotically valid, so "compatible" means *not clearly rejected*, not a calibrated
interval. The tenfold spread does not depend on those two rows: l = 0.01 (0.08) vs l = 1 and 3 cm (0.70, 0.87) are interior fits.

**Design.**
- **The test.** A graded perturbation of the candidate distal signal's production (for example an inducible transgene or
  a bead-implant dose series) during the observed growth phase. The model reads off the slope of
  log(fin/SL) against log(dose).
- **Reading the slope.** A slope near 0.1 favours a tip-saturated growth zone; a slope near 1 favours a gradient-limited zone.
- **Why it is decisive.** The 49 observed specimens cannot separate these two regimes, but four doses × about 10 fish
  would. The model's residual σ is 0.08 log10, so a slope difference of 0.8 over a 16-fold dose range is roughly a 1 log10 effect.
- **Controls.** A vehicle-only arm and body length SL measured on the same fish. Do **not** use the pelvic fin as a
  specificity control: in four-winged flying fishes such as *Cheilopogon* and *Hirundichthys* it is also enlarged and
  may share the outgrowth network (an assumption, not checked). The dorsal fin is a better within-fish comparison.
- **Organism.** Flying fish are pelagic spawners and are not lab-tractable for transgenics. Run the dose series in medaka
  (*Oryzias latipes*), a lab beloniform relative, over a defined juvenile window rather than to 24 cm SL.
  This measures the *form* of the transfer function, not flying-fish parameters.
- **Systemic confounds.** Long systemic treatments change body growth s and therefore r/s. Use local, inducible
  perturbation, and report fin length and SL separately, not only their ratio. Bead implants deplete within days and
  suit only short windows.
- **What it would not show.** Which molecule is the morphogen. The perturbed signal is the hypothesis being tested.

## LLM review

**Reviewer.** `gemini-4-argon` (deep critique), 2026-11-01. Its review is saved at `artifacts/simulations/claude-tissue-dev-programme/review-gemini-4-argon.txt`.

**Changes made in response:**
1. The power law is refitted on the raw-length scale so the AIC comparison is like for like. Result: the power law is
   now modestly preferred in all groups, and the doc says so.
2. The intercept a is reinterpreted as an extrapolated quantity. The "no early head start" claim is rescoped to the
   observed size range.
3. Bound-hitting fits are flagged, and the χ² cutoff is reworded to "not clearly rejected". The tenfold dose-response
   spread is shown to rest on interior fits.
4. A species-pooling, anticonservative-CI limitation and a regression-dilution limitation are added.
5. The pelvic-fin control is replaced with the dorsal fin, because four-winged flying fishes have enlarged pelvic fins.
6. Wet-lab rungs move to medaka or zebrafish, with local inducible perturbation and fin length and SL reported separately.
7. The sequential addition of fin rays is noted, and the uniform-growth doubling regime is recast as a rejected-mechanism contrast.
8. The 0.81 vs 0.729 slope difference is explained: it comes from the misspecified fixed-L0 fit.
10. A second `gemini-3.8-flash` pass on the summary and section 2b flagged four more overgeneralisations, all reworded:
    static patterning gives labyrinths, not rays; the speed threshold is specific to edge growth; a short start is not
    necessary; and "no spots to stripes" is limited to the two cells tested.
9. A `gemini-3.8-flash` overclaim check flagged four sentences ("data favour", "probably shares", "needs"). All four were softened.

**Not changed: the call for reduced major axis (RMA) regression.** The question here is predicting fin length from SL.
SL error is small relative to the range, so this is noted as a limitation instead.
<!--REVIEW-->
