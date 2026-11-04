# Challenge 130: adversarial review of S21-D-D (fastest-adult fast-start speed vs stall speed)

Project: `zebrafish-flight` · Written 2026-11-04 · Reviewer: did not write the claim

**Claim under review (S21-D-D, `docs/research/fish/S21-D-deepen.md`, commit `6b64006b` on branch
`claude/deepen-s21-d-sensitive-input-no42sx`; read-level full-text, repo doc):**

- The S21-D conclusion is most sensitive to the fastest adult's fast-start speed.
- A simulation "bounds" the 120 fps max-of-4 reading at 0.88–1.40× the true peak.
- That gives a true peak of ≈0.99–1.58 m/s, and a margin of ≈2.7–4.8× to the 4.37 m/s stall speed.
- Verdict: stands. Recorded evidence level: **measured**.

> **Verdict: WEAKENED.** The qualitative conclusion (the gap is not closed) survives every test below.
> Two things fail:
>
> 1. **The evidence level is wrong.** The key number is not measured. It is a simulation-corrected,
>    calculated quantity built on one digitised figure value.
> 2. **"Bounds 0.88–1.40×" is not a bound under the author's own model.** The low edge is a *mean*
>    (0.875). The high edge is a *95th percentile* (1.399). With the same percentile on both sides, the
>    low edge is ≈0.79×. So the true-peak band is ≈0.99–1.75 m/s and the margin is ≈2.4–4.8×
>    (simulated + calculated).

## 1. Arithmetic, redone independently

All values below are calculated by me (`docs/research/fish/challenge-130-sim.py`).

- **Stall speed.** V_s = √(2mg / (ρ S C_L)) with m = 0.4 g, g = 9.81, ρ = 1.2, S = 3.2×10⁻⁴ m².
  - C_L 0.6 → 5.836 m/s; C_L 1.07 → 4.370 m/s; C_L 1.15 → 4.216 m/s; C_L 0.9 → 4.765 m/s.
  - These match the author's 5.84, 4.37 and 4.22–4.77.
- **Central margin.** 4.37 / 1.38 = 3.17. That matches.
- **Flip factors.** U_fast must rise ×3.17 to reach M = 1. Inputs under a square root need
  ×3.17² = ×10.0. That matches, so "no single 2× error flips it" is correct.
- **True-peak band.** 1.38 / 1.40 = 0.986 and 1.38 / 0.875 = 1.577. That matches 0.99–1.58.
- **Margin band.** 4.22 / 1.58 = 2.67 and 4.77 / 0.99 = 4.82. That matches 2.7–4.8.
  - **Labelling defect (minor).** The KEY says "margin to 4.37 m/s stall speed ~2.7–4.8×". At exactly
    4.37 m/s the band is **2.77–4.41×**. The 2.7–4.8 edges need the V_s band 4.22–4.77, which the KEY
    does not state.
- **Typical fish.** 4.37 / 0.84 = 5.20. That matches "~5×".

## 2. The simulation, re-run independently

- **Method (mine).** I did not reuse the author's code. My script uses the closed-form position of
  the same alpha pulse, x(t) = V·t_p·e·(1 − e^(−t/t_p)(1 + t/t_p)), instead of the author's
  cumulative-sum integration. It uses 20,000 replicates, random frame phase, 120 fps, two-point
  differencing, and max of 4 trials.
- **Means reproduce.** These are simulated values:
  - t_p 5 ms, σ 0 → 0.877
  - t_p 10 ms, σ 0 → 0.966
  - t_p 20 ms, σ 0 → 0.991
  - t_p 20 ms, σ 1 mm → mean 1.230, p95 1.398
  - The author got 0.875, 0.966, 0.991 and 1.232 / 1.399. **The author's simulation is reproduced.**
- **The defect is the mixed statistic.** The claimed band takes its high edge from a p95 and its low
  edge from a mean. My percentiles (simulated, measured/true, 120 fps, max of 4):

| t_p | σ_x | mean | p5 | p50 | p95 |
|---|---|---|---|---|---|
| 5 ms | 0 | 0.877 | 0.815 | 0.890 | 0.897 |
| 5 ms | 0.5 mm | 0.918 | **0.790** | 0.920 | 1.042 |
| 5 ms | 1.0 mm | 0.991 | **0.787** | 0.985 | 1.217 |
| 20 ms | 1.0 mm | 1.230 | 1.096 | 1.220 | **1.398** |

- **A symmetric p5–p95 band over the author's own grid is ≈0.79–1.40×.**
  - True peak: 1.38/1.40 to 1.38/0.787, which is **≈0.99–1.75 m/s** (calculated from simulation).
  - Margin: 4.22/1.75 = 2.41 to 4.77/0.99 = 4.82, which is **≈2.4–4.8×** (calculated).
  - The gap is still not closed.
- **Mitigating point (my inference).** The 1.38 m/s fish is the top of ~200 noisy trials. Selection on
  the maximum favours readings in the *upper* tail of the bias distribution, not the p5 tail. So the
  author's mean-based low edge is not unreasonable as a central-ish estimate. But it is not a
  "bound", and the claim calls it one.

## 3. Proxies

- **Tracked point vs centre of mass.** Miln et al. tracked a body point at 0.35 BL from the snout. The
  quantity that matters for take-off is centre-of-mass speed. During the C-bend a body point can move
  faster than the COM, because rotation adds to its speed. If anything this inflates the reading,
  which is the conservative direction for the conclusion. This is my inference; I did not quantify it.
- **In-water burst speed vs airborne speed.** The quantity that matters is the speed in air after
  exit, and that is lower than the in-water burst. The author states this caveat. Using the burst
  speed is again conservative.
- **Neither proxy can flip the conclusion. Both push U_fast down.**

## 4. Hidden assumptions, relaxed

- **Rise time t_p ≥ 5 ms.** In the author's model, b falls to ≈0.60 at t_p = 2.5 ms (my simulation),
  which gives M ≈ 1.9–2.1.
  - The follow-on S21-D-D-D (same branch, commit `0d17d892`; read-level full-text, repo doc) reports
    Danos & Lauder 2012: time to maximum COM velocity 25.6 ± 1.8 ms, digitised from Fig. 4B.
  - I did not re-read Danos & Lauder myself. Conditional on that digitisation, t_p < 5 ms is excluded.
    The 5 ms floor was conservative, not optimistic.
- **Body-size transfer (not tested by the author).** U_fast comes from Miln fish of unknown length
  (their data are on Dryad, could-not-access per the author). It is compared with a stall speed for a
  4 cm design fish.
  - Suppose the Miln fish are ~3 cm and speed scales ∝ L. That is an assumption of mine; no source.
  - The 4 cm equivalent of the worst-case true peak is then 1.75 × 4/3 ≈ 2.33 m/s, and
    M = 4.22 / 2.33 ≈ 1.8 (calculated).
  - That narrows the margin further but **does not flip it**.
- **Tracking noise up to 1 mm.** At σ_x = 2 mm the upward inflation grows (my simulation: mean 1.53,
  p95 1.85 at t_p 20 ms). That lowers the true-peak estimate, so the margin widens. The direction is
  safe.

## 5. Counter-examples searched

- **Search.** One standard web search: "adult zebrafish C-start escape maximum velocity m/s high-speed
  video peak speed".
  - It found no adult zebrafish peak escape speed above 1.6 m/s.
  - The results were J Exp Biol PDFs (jeb168609, jeb203091), PMC5394678, PMC4295168 and PMC3044078, the
    Danos & Lauder record on dash.harvard.edu, and a killifish 3D fast-start paper.
  - Read-level: **search-summary** only. I opened none of them.
- **Scope of this negative.** It covers one query in English on the open web. Paywalled literature,
  theses and non-English sources were not covered.
- **The author's own cross-check.** The author's Danos & Lauder value (0.84 m/s, 1000 fps) is lower
  than the Miln maximum, not higher. S21-D-D-D's digitisation of Danos & Lauder Fig. 3I (856 mm/s)
  agrees with it (repo doc, full-text).

## 6. Evidence level

- **Recorded level: "measured". This is a defect.**
  - The key number (true peak 0.99–1.58 m/s; margin 2.7–4.8×) is **derived**: a Monte Carlo bias
    correction under assumed pulse shape, rise time and noise, applied to one value the author
    digitised from Miln et al. Fig. 1a, and then divided into a calculated stall speed.
  - The only measured element is the authors' plotted per-fish speed, and the author re-digitised it.
- **The author's own prose is honest.** It says "SIMULATION, not observation" and its swarm-result
  `evidence` field lists the mixture. The recorded level for the claim should read
  **derived (simulated + calculated)**.

## Sources

| Source | Read-level |
|---|---|
| S21-D-D, `docs/research/fish/S21-D-deepen.md` + `S21-D-deepen-sim.py` (commit 6b64006b) | full-text (repo) |
| S21-D-D-D, `docs/research/fish/S21-D-D-deepen.md` (commit 0d17d892) | full-text (repo), §§0–3.2 read |
| Miln, Ward & Seebacher 2021, doi:10.1098/rsos.210146 | not read by me; relied on author's full-text reading and digitisation |
| Danos & Lauder 2012, doi:10.1242/jeb.068957 | not read by me; relied on S21-D-D-D's full-text digitisation |
| Web search results listed in §5 | search-summary |

```swarm-challenge
{"claim_id": 130, "outcome": "weakened", "reason": "The qualitative verdict (gap not closed) and all arithmetic reproduce, but the key number is a simulated-and-calculated quantity recorded as 'measured', and the '0.88-1.40x bound' mixes a mean (low edge) with a p95 (high edge); a consistent p5-p95 band under the author's own model is ~0.79-1.40x, widening the true peak to ~0.99-1.75 m/s and lowering the margin floor to ~2.4x.", "corrected_value": "fastest adult true peak ~0.99-1.75 m/s (simulated p5-p95 bias band 0.79-1.40x on 1.38 m/s reading); margin ~2.4-4.8x to V_s 4.22-4.77 m/s (2.5-4.4x at 4.37 m/s); evidence level derived (simulated + calculated), not measured", "depends_on": ["Miln, Ward & Seebacher 2021 Fig. 1a fastest-fish reading 1.38 m/s at 120 fps, max of 4 trials (as digitised by S21-D-D)", "S21-D-D simulation model: alpha-pulse speed profile, t_p 5-20 ms, sigma_x 0-1.0 mm, 120 fps two-point differencing (reproduced independently in challenge-130-sim.py)", "stall speed V_s = sqrt(2mg/(rho S C_L,max)) with m 0.4 g, S 3.2e-4 m^2, rho 1.2 kg/m^3, C_L,max 1.07 (band 0.9-1.15) from replicate-24", "S21-D-D-D digitisation of Danos & Lauder 2012 time-to-max COM velocity 25.6 ms (used only to judge the t_p floor conservative)", "assumption: in-water burst speed and 0.35 BL body-point speed are upper proxies for airborne COM speed"]}
```
