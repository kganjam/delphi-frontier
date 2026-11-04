# Challenge 130: adversarial review of S21-D-D

Project: `zebrafish-flight` · Scale: behaviour · Written 2026-11-04

**Claim under review:** S21-D-D. File `docs/research/fish/S21-D-deepen.md`, commit `6b64006b`, branch
`claude/deepen-s21-d-sensitive-input-no42sx`. Read-level: full-text (repo doc and its script).

**Recorded evidence level:** `measured`.

**Key number as claimed:**

- The fastest adult's true peak fast-start speed is ≈0.99–1.58 m/s (central 1.38).
- This rests on a simulated bias band of 0.88–1.40× on a 120 fps max-of-4 reading.
- The margin to the 4.37 m/s stall speed is ≈2.7–4.8×.
- The gap is not closed. Verdict: stands.

> **Outcome: WEAKENED.**
>
> - **The qualitative conclusion survives every attack I made.** That covers: the gap is not closed,
>   U_fast is the most sensitive input, and no single 2× input error flips the result.
> - **Defect 1: the evidence level is mislabelled.** The key number is *derived*: a digitised
>   measurement (1.38 m/s) divided by *simulated* bias factors. The margin is *calculated*. None of it is
>   `measured`. The claim's own sentence says "a simulation bounds", and the author's swarm-result says
>   "measured + simulated". The recorded level drops that qualifier.
> - **Defect 2: the 0.88–1.40× band depends on an unstated choice.** The author's simulation assumes
>   two-point forward differencing. Miln et al. do not say how fast-start speed was differenced.
>   - Under a three-point central difference, at the author's own t_p = 5 ms floor, my simulation gives a
>     bias of 0.67×. That puts the true peak at ≈2.07 m/s and the margin at ≈2.0–2.1×.
>   - So the band, and the claim that it "rules out" S21-D's 2× under-read, are conditional on that
>     choice. The conclusion survives this case.
> - **The band also disagrees with a later measured-shape re-run.** S21-D-D-D gives an upper bias of
>   1.66×, which puts the lower true peak at 0.83 m/s rather than 0.99 m/s. I preserve that disagreement
>   rather than average it.

---

## 1. Arithmetic, redone independently

I recomputed everything from the stated inputs. Every value in this section is calculated, not
observed.

- **Stall speed.** V_s = √(2mg / (ρ S C_L)), with m = 0.4 g, g = 9.81, ρ = 1.2 kg m⁻³ and
  S = 3.2×10⁻⁴ m². Script: `challenge-130-sim.py`.
  - C_L = 0.6 gives **5.836 m/s**, so the claim's 5.84 is correct.
  - C_L = 1.07 gives **4.370 m/s**, which is correct.
  - C_L = 1.15 gives 4.216 m/s and C_L = 0.9 gives 4.765 m/s. The author's 4.22–4.77 band is correct.
- **Margins:**
  - 4.37 / 1.38 = 3.17.
  - 4.37 / 1.58 = 2.77, and 4.22 / 1.58 = 2.67.
  - 4.37 / 0.99 = 4.41, and 4.77 / 0.99 = 4.82.
  - So the "≈2.7–4.8×" range is reproduced.
- **True-peak band:** 1.38 / 0.875 = 1.577 and 1.38 / 1.40 = 0.986. Both are reproduced.
- **Sensitivity.** M ∝ U⁻¹ · m^½ · S^−½ · C_L^−½.
  - A 2× error in U moves M to 1.58 or 6.33.
  - A 2× error in any square-root input moves M to 2.24 or 4.48.
  - A flip needs U ×3.17, or a square-root input wrong by 3.17² ≈ 10×.
  - **All of this is reproduced.**
  - One caveat. Mass and wing area are both design premises tied to body length. A *correlated* error,
    such as a heavier fish with an unchanged wing, compounds them. "No single 2× error flips it" is true
    as stated, but it does not cover joint errors. A 2× mass error together with a 2× area shortfall moves
    M by 2×, to 1.58. That still does not flip the conclusion.

**Arithmetic: no error found.**

## 2. Proxy check

The claim compares two numbers: the in-water peak speed of a body point, and the level-flight stall
speed of a reference wing.

- **The quantity that matters is the speed at water exit.** Miln's fish were in 30 mm of water. Exit
  speed is not measured anywhere in the chain.
  - The author lists "in-water burst speed is an upper proxy for water-exit speed" as an assumption.
  - The direction is conservative for "gap not closed". Breaking the surface and the drop in thrust as
    the tail leaves the water can only lower the speed.
  - So the stated margin is best read as a **lower bound** on the relevant margin, not the margin itself.
    This is my inference.
- **The tracked point is not the centre of mass.** Miln tracked a point at 0.35 BL from the snout.
  Read-level: full-text, Europe PMC XML PMC8025299, Methods §2.2.
  - During stage-1 C-bend rotation, a point on the body can move faster than the true centre of mass.
  - That bias is upward, which is again conservative for the conclusion. I did not quantify it.

**No proxy problem flips the conclusion.**

## 3. Hidden assumption: how speed was differenced (tested relaxed)

The author's script (`S21-D-deepen-sim.py`) computes speed as `np.diff(xs)/dt`. That is a two-point
forward difference over one 8.3 ms frame interval.

**What Miln et al. actually state** (read-level: full-text, PMC8025299):

- For *realized* speed: "maximum speed calculated across two video frames".
- For *fast-start* speed, they say only that videos were analysed in Tracker 4.01 "using the fish centre
  of mass as the tracking point", and that "the fastest speed was used". **The differencing scheme for
  fast starts is not stated.**
- To my knowledge, Tracker's default velocity estimate is a central finite difference,
  (x_{i+1} − x_{i−1}) / 2Δt, which spans 16.7 ms at 120 fps. **I could not verify this in this
  session.** physlets.org is not in the session's allowed network domains (ENOTFOUND). Treat it as an
  unverified prior, not a fact.

**I re-ran the author's model under both schemes.** It uses an alpha pulse, random frame phase, Gaussian
σ_x and max of 4, with 1500 replicates. Script: `docs/research/fish/challenge-130-sim.py`, seed 130.
Entries are mean measured / true peak (simulated, not observed).

| t_p | σ_x | forward (author's scheme) | central (Tracker default?) |
|---|---|---|---|
| 3 ms | 0 | 0.69 | 0.42 |
| 5 ms | 0 | 0.88 | **0.67** |
| 5 ms | 1.0 mm | 1.00 | 0.71 |
| 10 ms | 0 | 0.97 | 0.89 |
| 10 ms | 1.0 mm | 1.15 | 0.97 |
| 20 ms | 1.0 mm | 1.23 (p95 1.41, p98 1.47) | 1.07 (p95 1.17) |
| 20 ms | 1.5 mm | 1.38 (p95 1.62) | 1.14 (p95 1.27) |

My forward-difference column reproduces the author's table (0.875 / 0.966 / 1.232 / p95 1.40) to
within Monte Carlo noise.

**Consequences.** These are my inferences, conditional on the model.

- **Under central differencing at the author's own floor (t_p = 5 ms):**
  - The bias is 0.67×, giving a true peak of 1.38 / 0.67 ≈ **2.07 m/s**.
  - M = 4.37 / 2.07 ≈ **2.1**, or 2.04 at V_s = 4.22.
  - The claimed lower margin of 2.7× is therefore not a bound under the author's stated t_p range. It is
    a bound only under forward differencing.
- **When a 2× under-read becomes possible (noise-free):**
  - Forward differencing needs t_p ≈ 2 ms (b = 0.50).
  - Central differencing needs t_p ≈ 3.5–4 ms. At 3 ms, b = 0.42.
  - So "rules out S21-D's hypothetical 2× under-read" holds only if t_p is above ~4 ms. That is a model
    condition, not a measurement.
- **When the gap would flip:**
  - Under central differencing, M reaches 1 when b ≈ 1.38 / 4.22 ≈ 0.33. That needs t_p ≈ 2.5 ms
    (b = 0.34) with zero noise.
- **Is that regime plausible?**
  - The sibling deepening S21-D-D-D (commit `0d17d892`) digitised Danos & Lauder 2012. Read-level for me:
    listing (their swarm-result and summary only; I did not re-read Danos & Lauder).
  - It reports a time to peak COM velocity of 25.6 ± 1.8 ms (s.e.m.) in adult zebrafish at 1000 fps,
    with a ~19 ms plateau above 90% of peak.
  - If that time course transfers to Miln's fish, t_p ≪ 5 ms is excluded.
  - At t_p of 10–20 ms, the central-difference bias is 0.89–1.27 (p95). That lies within or near the
    author's band.
  - **So the differencing gap does not threaten the conclusion. It does show that the author's band and
    "rules out" wording were conditional on an unstated choice.**
- **Selection effect.** The fastest of 50 fish is roughly a 98th-percentile draw, not a 95th.
  - Forward, t_p = 20 ms, σ = 1 mm: p98 = 1.47 against p95 = 1.41. That moves the lower true peak from
    0.99 to ≈0.94 m/s.
  - Small, but the author's band edge is p95, not the order statistic that applies.

## 4. Evidence level

The claim is recorded as `measured`, with value `n/a`.

- 1.38 m/s is a digitisation of a measured figure (Miln Fig. 1a). It is measurement-derived, and
  second-hand.
- 0.88–1.40× is **simulated**.
- 0.99–1.58 m/s is **derived**: the measurement divided by a simulation output.
- 2.7–4.8× is **calculated**, using a threshold that itself depends on an unsourced 0.4 g mass and a
  dragonfly-wing C_L,max proxy (search-summary).

**The correct level is `derived` (measurement + simulation + calculation).** Labelling it `measured`
lets the bias band inherit an authority it does not have. The author's own write-up is honest about
this; the ledger label is not. Under the honesty floor, this is a defect regardless of whether the
numbers are right.

## 5. Counter-examples and regimes missed

- **Disagreement with S21-D-D-D (preserved, not averaged):**
  - S21-D-D-D's simulation on a measured profile shape gives a bias of b = 0.96–1.66. That puts the true
    peak at 0.83–1.43 m/s and the margin at 2.9–5.3×.
  - S21-D-D gives b = 0.88–1.40, a true peak of 0.99–1.58 m/s and a margin of 2.7–4.8×.
  - The upper bias edges disagree: 1.40 vs 1.66.
  - Both runs use forward differencing. Neither tests central differencing.
- **Temperature.** Miln tested at 23 °C; the design premise is not stated at 28 °C. The author flags
  this as `unknown`. I did not find a value either. I made no search beyond what the author recorded.
- **Searches I made in this session, and their scope:**
  - Europe PMC full-text XML of PMC8025299, keyword scan for Tracker, frames, fastest, velocity,
    smoothing and GoPro.
  - One attempt on the Tracker help pages, which could not be accessed.
  - I did not search the published literature for a taxon or regime that contradicts the conclusion.
    The author's recorded search (Europe PMC open access, 15 + 4 hits) is the only literature scope here.

## 6. Verdict

**WEAKENED, not refuted.**

- **What survives:** "The gap is not closed", and U_fast as the input with unit elasticity. The
  arithmetic is correct.
- **What does not survive as stated:**
  - **The evidence label.** It should be `derived`, not `measured`.
  - **The tightness of the band.** Under central differencing, which may be Tracker's default (unverified
    here), the author's own t_p range gives a bias as low as 0.67×. That means a true peak of ≈2.07 m/s
    and a margin of ≈2.0×.
  - **"Rules out the 2× under-read".** That rests on t_p ≳ 4 ms, not on the simulation alone. Only the
    Danos & Lauder time course (via S21-D-D-D) supports that condition.
- **Corrected statement.** The margin is ≥ ~2.0× under the author's model across both differencing
  schemes, and ≈2.7–4.8× under forward differencing. The fastest-fish true peak is ≈0.83–2.07 m/s across
  this review and S21-D-D-D. That figure is derived, not measured.

```swarm-challenge
{"claim_id": 130, "outcome": "weakened", "reason": "Conclusion (gap not closed, U_fast most sensitive) and all arithmetic reproduce, but the key number is derived (digitised measurement / simulated bias), not measured, and the 0.88-1.40x bias band assumes unstated two-point forward differencing; under central differencing at the author's own t_p=5 ms floor the bias is ~0.67x, giving a true peak ~2.07 m/s and margin ~2.0x (simulated).", "corrected_value": "fastest-adult true peak ~0.83-2.07 m/s (derived, not measured; upper end if central differencing and t_p=5 ms, lower end from S21-D-D-D); margin to 4.22-4.37 m/s stall speed >= ~2.0x (calculated), ~2.7-4.8x only under forward differencing", "depends_on": ["S21-D-D (commit 6b64006b) chain M = V_s / (U_read / b) and its simulation script S21-D-deepen-sim.py", "Miln, Ward & Seebacher 2021 (doi:10.1098/rsos.210146, PMC8025299) Methods: 120 fps, Tracker 4.01, max of 4 trials, differencing scheme for fast starts not stated (full-text)", "Miln Fig. 1a fastest fish 1.38 m/s as digitised by S21-D-D (not re-digitised by me)", "unverified prior: Tracker default velocity is central difference (x[i+1]-x[i-1])/(2 dt); physlets.org not reachable this session", "my simulation challenge-130-sim.py: alpha pulse, t_p 3-20 ms, sigma_x 0-1.5 mm, random phase, max of 4, forward vs central differencing (simulated)", "S21-D-D-D (commit 0d17d892): Danos & Lauder 2012 time to peak COM velocity 25.6 +/- 1.8 ms and bias b = 0.96-1.66 (read-level listing via repo doc)", "replicate-24 (commit 922d3d1d): V_s = 4.37 m/s at C_L,max 1.07, band 4.22-4.77", "design premises: mass 0.4 g (source unknown), S = 3.2e-4 m^2, rho 1.2 kg/m^3", "assumption: in-water burst speed is an upper proxy for water-exit speed"]}
```
