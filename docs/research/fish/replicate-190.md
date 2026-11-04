# Replication of claim 190: wing lift as a fraction of body weight (S28 organism, case C)

**Claim, with the answer removed:** granting an unmeasured 1-BL span and an AR-5 fin (S = 192 mm²), the wing produces ? % of body weight at launch and ? % at the apex.

**My value:** L/W = **9.8 % at launch** (range 1.0–9.8 % across the measured burst speeds 0.45–1.38 m/s) and **4.9 % at the apex** for a 45° launch (0.5–4.9 %). Every number here is **calculated**. None was observed. No lift on this fin has ever been measured.

## Method and order of work
1. The input file `docs/research/fish/S28-organism.md` exists only on branch `origin/claude/s28-organism-design-5z0vjz`. I found it with a filename search over every remote ref.
2. I read §1 (Inputs) and §2 (Design and geometry) only. I did **not** open §3, where the result sits, or the companion script `S28_organism.py` until my arithmetic below was finished.
3. Only after that did I read §3.2 to compare.

## Inputs
| Input | Value | Kind | Source | Read-level |
|---|---|---|---|---|
| ρ_air | 1.225 kg m⁻³ | constant | standard sea-level air | — |
| g | 9.81 m s⁻² | constant | — | — |
| Fin planform area S | 192 mm² | **assumed** (the project's AR-5 prior, case C; the doc says no measurement supports it) | S28-organism.md §2.2 | full-text (§1–2) |
| CL_max | 1.07 | derived by the project (a "corrected" value), not measured | S28-organism.md §1 | full-text (§1–2) |
| Body mass m | 0.25 g | **assumed**, back-solved so that the project's V_to = 4.37 m/s is self-consistent | S28-organism.md §1 | full-text (§1–2) |
| Launch (exit) speed U | 0.45–1.38 m/s | the measured *swimming* burst speed, assumed equal to water-exit speed | Miln et al. 2021, as cited in S28-organism.md §1 | the paper itself: **could-not-access** (not attempted; I used the project's citation of it) |
| Launch angle θ | 45° | **my assumption** (range-optimal for vacuum ballistics) | — | — |

## Arithmetic
W = m g = 0.25e-3 × 9.81 = **2.4525e-3 N**

Lift at launch, fixed CL = CL_max:
L = ½ ρ U² S CL = 0.5 × 1.225 × 1.38² × 192e-6 × 1.07
 = 0.6125 × 1.9044 × 192e-6 × 1.07 = **2.396e-4 N**

L/W = 2.396e-4 / 2.4525e-3 = **0.0977 → 9.8 %**

Equivalently, L/W = (U/V_to)², where V_to = √(2W/(ρ S CL)) = √(2 × 2.4525e-3 / (1.225 × 192e-6 × 1.07)) = **4.415 m/s**. Then (1.38/4.415)² = 0.0977.

At U = 0.45 m/s: L/W = **0.0104 → 1.0 %**.

**Apex.** At the apex the vertical velocity is zero. In near-vacuum ballistics only the horizontal component U cos θ remains, so L/W at the apex = (L/W at launch) × cos²θ.
- θ = 45°: 0.0977 × 0.5 = **0.0489 → 4.9 %** (0.45 m/s: 0.5 %)
- Sensitivity to θ, at 1.38 m/s: 30° gives 7.3 %; 60° gives 2.4 %.

**Other sensitivities** (all calculated):
- With a 0.40 g fish (the doc says this is also typical), launch L/W = 6.1 %.
- Adding fin-membrane mass of 10.6–21.1 mg (the doc's estimate) gives 9.4–9.0 %.
- CL_max = 1.07 at a wing Reynolds number of about 570 is itself unmeasured. A lower real CL lowers every value in proportion.

**My uncertainty statement:** the launch value is about 10 % (+0 / −4 % from the mass and membrane assumptions at 1.38 m/s; down to about 1 % at the slow end of the burst range). The apex value is about 5 % at 45°, scaling as cos²θ. These are upper bounds, because every input is set at its generous end.

## Comparison with the recorded value
I read this after the derivation above was finished. S28-organism.md §3.2 states: "(1.38/4.37)² = 0.0997 W, i.e. 10 % of weight … 1.38·cos45° = 0.98 m/s, giving (0.98/4.37)² = 5 %."

**AGREE.** I used the same formula. The only difference is that the recorded value uses the project's V_to = 4.37 m/s. I recomputed V_to from S = 192 mm², which gives 4.415 m/s (the doc's own §2.2 table also lists 4.41 m/s for case C). The results are 9.97 % (recorded) vs 9.77 % (mine). Both round to 10 %, and both apex values round to 5 %.

Caveats on what this agreement means:
- It checks the arithmetic, given shared inputs. It does **not** check the inputs. S = 192 mm², CL = 1.07 and m = 0.25 g are all assumed or back-solved, not measured.
- The recorded claim gives only the fast end (1.38 m/s). At the slow end of the measured burst range (0.45 m/s), the fractions are ~1 % and ~0.5 %.
- The apex figure depends on a 45° launch, which is an assumption, not a measurement.

Negative-search scope: I did not search the literature for measured flying-fish or zebrafish fin lift coefficients. I did not open Miln et al. 2021 or Daane et al. 2021.

```swarm-replication
{"claim_id": 190, "my_value": "L/W = 9.8% of body weight at launch (1.38 m/s) and 4.9% at the apex (45° launch); calculated, not observed", "agrees": true,
  "note": "Same (U/V_to)^2 arithmetic; recorded value uses V_to=4.37 m/s, recomputing from S=192 mm2 gives 4.415 m/s (9.8% vs 10.0%), and all inputs (S, CL_max, mass, launch angle) are assumed rather than measured."}
```
