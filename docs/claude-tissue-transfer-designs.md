# Tissue and developmental simulations: transfer functions between scales and the experiments that would measure them

Harness `claude-tissue`, 2026-11-01. Branch `claude-tissue/sims-20261101`.

**Scope.** Everything below is **simulated**, not observed. The only observed data used are the 49 flying-fish rows
of `artifacts/observed-allometry/source-observations.csv` (pectoral fin length vs standard length, SL). They are used
once for anchoring (fin-growth) and once for fitting (identifiability and transfer regimes). Turing-type results are
dimensionless. Mapping them to fin rays or scales is an **assumption**: the repo holds no measured ray spacing,
morphogen diffusivity or turnover rate. No simulation here validates a biological mechanism.

Each simulation folder `artifacts/simulations/claude-tissue-*/` contains:
- a figure
- a `manifest.json` (file hashes, code hashes, run list with exit codes)
- one receipt per run (command, exit code, seed, wall time, input and output hashes)

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
- So a static Turing mechanism gives ray-like stripes only if the kinetics are tuned close to onset.

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
- Directional growth does **not** turn spots into stripes.
- So, in this model, a ray-like pattern needs both near-onset kinetics and outgrowth slower than a threshold
  between v = 0.1 and 0.4 (in units of λ per pattern time).

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
- Proximo-distal stripes come from *growth along the proximo-distal axis* starting from a fold shorter than one
  wavelength (8 rows against λ ≈ 11), together with near-onset kinetics. Edge-specific insertion is not needed.
- Fast *edge* growth is the condition that breaks the orientation (A = −0.53); uniform growth at the same speed
  keeps it (0.99).
- In this model, then, the edge mode adds a speed constraint that the uniform mode does not have.
- Neither mode turns spots into stripes.

**Prediction, revised.** If rays were laid down by such a mechanism, they would align with the axis of fold elongation.
Under marginal (edge) outgrowth, but not uniform outgrowth, speeding up outgrowth beyond a threshold would disorder them.
The follow-up job `claude-tissue-edge2d-cases` narrows that threshold and tests other stripe-regime kinetics.

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
9. A `gemini-3.8-flash` overclaim check flagged four sentences ("data favour", "probably shares", "needs"). All four were softened.

**Not changed: the call for reduced major axis (RMA) regression.** The question here is predicting fin length from SL.
SL error is small relative to the range, so this is noted as a limitation instead.
<!--REVIEW-->
