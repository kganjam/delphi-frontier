# Challenge 163: adversarial review of S21-D-D (fastest-adult fast-start speed and stall margin)

Written 2026-11-04. Claim under review: harvest `deepen-s21-sensitive-input-mxp5t8`, i.e.
`docs/research/fish/S21-D-deepen.md` and `S21-D-deepen-sim.py` on branch
`claude/deepen-s21-sensitive-input-mxp5t8`, commit `6b64006b` (read-level: full-text, repo).

**Outcome: WEAKENED.** The binary conclusion ("gap not closed") survives every test I ran. Three parts
of the claim do not survive as written:

1. the 0.88–1.40× bias band mixes a *mean* (lower edge) with a *95th percentile* (upper edge);
2. "ruling out S21-D's 2× under-read" holds only if the speed pulse rises in ≥5 ms, and the author
   says they have no source for that;
3. the recorded evidence level "measured" is wrong for the key number, which is simulated and
   calculated.

I did no new literature search in this review. Every external source below is as the author reported it,
and I have not read it myself. My own work here is arithmetic and simulation only.

## 1. Arithmetic, redone independently

I calculated V_s = √(2mg/(ρ S C_L)) with m = 0.4 g, g = 9.81, ρ = 1.2 kg/m³ and S = 3.2×10⁻⁴ m². These are the
author's premises.

| C_L,max | V_s (my calculation) | Author |
|---|---|---|
| 0.6 | 5.836 m/s | 5.84 |
| 0.9 | 4.765 m/s | 4.77 |
| 1.07 | 4.370 m/s | 4.37 |
| 1.15 | 4.216 m/s | 4.22 |

- Margin M = V_s/U: 4.37/1.38 = 3.17, 4.22/1.58 = 2.67 and 4.77/0.99 = 4.82 (calculated). These match.
- Elasticities: M ∝ U⁻¹ · m^½ · S^-½ · C_L^-½. With M₀ = 3.17, a flip needs U ×3.17, or a ~10× (3.17²) error in a
  square-root input. That matches as well. "No single 2× error flips the conclusion" is correct: the worst case,
  U ×2, gives M = 1.58.
- Inversion: 1.38/0.875 = 1.577 and 1.38/1.40 = 0.986 (calculated). These match.

**No arithmetic error found.**

## 2. Hidden assumption that carries the bias band: pulse rise time t_p ≥ 5 ms

The author's simulation assumes an alpha-shaped speed pulse with t_p ∈ {5, 10, 20} ms. The author's
own text says "I have no adult zebrafish source for it." The claim "rules out a 2× under-read" is
true only inside that assumed range. I reran the model (`challenge-163-sim.py`, seed 7, 3000 replicates per cell).
All the numbers below are **simulated, not observed**: measured/true peak at 120 fps, max of 4 trials.

| Pulse | σ_x | mean | p5 | p95 |
|---|---|---|---|---|
| alpha, t_p 2.5 ms (outside author range) | 0 | **0.604** | **0.366** | 0.695 |
| alpha, t_p 2.5 ms | 1 mm | 0.684 | 0.447 | 0.949 |
| alpha, t_p 5 ms | 0 | 0.877 | **0.815** | 0.897 |
| alpha, t_p 10 ms | 0 | 0.966 | 0.948 | 0.972 |
| alpha, t_p 20 ms | 1 mm | 1.231 | 1.098 | **1.396** |
| Gaussian, FWHM 5 ms (no coasting tail) | 0 | 0.587 | 0.523 | 0.607 |
| Gaussian, FWHM 8 ms | 0 | 0.774 | 0.700 | 0.797 |
| Gaussian, FWHM 12 ms | 0 | 0.883 | 0.835 | 0.899 |

What these results show (my inference, conditional on the model):

- **Inconsistent band statistic.** The author's lower edge, 0.875, is a *mean*. The upper edge, 1.40, is a *p95*.
  If I use p5 to p95 consistently over the author's own range (alpha, t_p 5–20 ms, σ_x 0–1 mm), the band
  becomes **~0.82–1.40×**. That puts the fastest fish's true peak at **~0.99–1.69 m/s** and the margin at
  4.22/1.69 = **2.5×** up to 4.8× (calculated). This is wider than the author's 2.7–4.8×. It still does not flip the conclusion.
- **The 2× under-read is not ruled out by the simulation itself. Only the unsourced t_p floor rules it out.**
  - At t_p 2.5 ms, or with a symmetric pulse of FWHM ≤ 5 ms, 120 fps under-reads by ~1.65–1.7× on the mean. In the
    p5 tail, at t_p 2.5 ms, it under-reads by ~2.7×.
  - Worst case in this relaxed set: true peak 1.38/0.366 ≈ 3.8 m/s, M = 4.22/3.8 ≈ **1.1** (calculated). That
    is still above 1, but only just.
  - Whether t_p ≈ 2.5 ms is physically possible is **unknown** to me; I have no source for adult zebrafish
    fast-start kinematics. As a plausibility check, the arithmetic is mine: reaching 2.3 m/s in 2.5 ms needs a mean acceleration of
    ~900 m/s² (~90 g). I *suspect* this is above what fish fast-starts achieve, but I have not checked it
    against any source, so it cannot be used as a refutation.
- **Pulse shape matters as much as rise time.** The alpha pulse has a long coasting tail, and that tail is what makes a
  two-frame difference (8.3 ms) close to the peak. A symmetric 8 ms pulse already gives a 0.77× mean. The author did not
  test any non-alpha shape.
- **The noise inflation is slightly overstated, which is conservative.** The author simulated at V = 1 m/s. At the
  actual V = 1.38 m/s with σ_x = 1 mm, the inflation is 1.09 (t_p 10 ms) and 1.16 (t_p 20 ms) on the mean, with p95 1.23–1.28,
  against the author's 1.14–1.23 and 1.40. This is simulated. It narrows the high-speed-noise side, so it slightly *raises* the low-margin
  edge. It does not help the author's lower U bound much (0.99 → ~1.08 m/s).

## 3. Proxy check

- **The measured point is a body-fixed point at 0.35 BL, not the COM.** This is the author's report of the Miln methods. During a C-bend the
  anterior body rotates, so that point's speed can exceed COM speed. This *probably* biases U upward, which is
  conservative for "gap not closed". The magnitude is unknown.
- **Burst speed in water vs. airspeed at water exit.** The author flags this. Exit speed should be ≤ in-water peak, so it is conservative.
- **Capability vs. elicited performance.** The author reports that Miln used 30 mm water depth, a tail-tap stimulus and 23 °C. Each
  could depress the speed below the fish's true maximum. The author flags only temperature. Together these are an *unquantified*
  upward risk on U. To flip the conclusion they would have to combine with the bias above to reach ~3.2×. I can't
  quantify that, and I am not asserting it happens.

## 4. Evidence level

The claim is recorded as **measured**. The key number, "true peak ~0.99–1.58 m/s", is a measured *digitisation* (the author's
read of Miln Fig. 1a, not printed values) corrected by a **simulation**. The margin is **calculated** from a
threshold that itself rests on a search-summary proxy (C_L,max from dragonfly wings) and on a premise of unknown
source (0.4 g mass). The claim's sentence does say "a simulation bounds", which is honest. The recorded
level is not. **Correct level: simulated/calculated, anchored on one measured-by-digitisation value.**

## 5. Missed regime or counter-example

- I did not search the literature in this review (scope: none). So I cannot offer a published counter-example,
  and I do not claim that none exists.
- The regime the author missed is **short or symmetric speed pulses** (§2). That regime is internal to their model.

## Verdict

**WEAKENED.**

- "Gap not closed" survives every case I simulated (minimum M ≈ 1.1, in an extreme relaxed case of unknown physical
  plausibility).
- Within the author's own assumed rise-time range, the defensible margin is **~2.5–4.8×**, not 2.7–4.8×. The bias band is
  ~0.82–1.40× (consistent p5–p95), not 0.88–1.40×.
- "Ruling out a 2× under-read" should read "ruling it out *if* the speed pulse rises in ≥5 ms with a coasting tail
  (unsourced)".
- The evidence level should be simulated/calculated, not measured.

```swarm-challenge
{"claim_id": 163, "outcome": "weakened", "reason": "Arithmetic and the 'gap not closed' verdict reproduce, but the 0.88-1.40x bias band mixes a mean lower edge with a p95 upper edge (consistent p5-p95 gives ~0.82-1.40x, true peak ~0.99-1.69 m/s, margin ~2.5-4.8x), 'ruling out a 2x under-read' rests on an unsourced >=5 ms alpha-pulse rise time (t_p 2.5 ms or a symmetric <=5 ms pulse gives ~1.7x mean and up to ~2.7x p5 under-read in simulation), and the recorded evidence level 'measured' should be simulated/calculated.", "corrected_value": "fastest adult true peak ~0.99-1.69 m/s (simulated, t_p 5-20 ms, consistent p5-p95); margin to 4.22-4.77 m/s stall speed ~2.5-4.8x (calculated); worst relaxed case (t_p 2.5 ms, p5) margin ~1.1x", "depends_on": ["S21-D-D (commit 6b64006b) digitisation of Miln et al. 2021 Fig. 1a: fastest fish 1.38 m/s, 120 fps, max of 4 trials (not re-read by me)", "simulation model: alpha or Gaussian speed pulse, rise time 2.5-20 ms, tracking noise 0-1 mm, random frame phase (my rerun, seed 7)", "stall speed V_s = sqrt(2mg/(rho S C_L,max)) with m 0.4 g, S 3.2e-4 m^2, rho 1.2 kg/m^3, C_L,max 0.9-1.15 (replicate-24, Wakeling & Ellington 1997 search-summary proxy)", "assumption: in-water burst speed is an upper proxy for water-exit speed"]}
```
