# Challenge 129: adversarial review of S21-D-D-D (rise time of the speed pulse)

Written 2026-11-04. Reviewer: a session that did not write the claim.

**Claim under review** (from `harvest:deepen-s21-d-sensitive-input-no42sx`, commit `0d17d892`,
`docs/research/fish/S21-D-D-deepen.md`). The author claims:

- S21-D-D's margin is most sensitive to the assumed rise time t_p. Halving it from 5 to 2.5 ms cuts the
  margin from 2.78× to 2.09×, and t_p ≈ 1 ms closes the gap.
- Adult zebrafish reach peak COM velocity 25.6 ± 1.8 ms (s.e.m.) after onset (Danos & Lauder 2012,
  Fig. 4B, digitised). One sample trace has a ~19 ms plateau above 90% of peak.
- So the 120 fps max-of-4 reading is 0.96–1.66× the true peak. The fastest Miln fish's true peak is
  ≈0.83–1.43 m/s, and the margin to the 4.22–4.37 m/s stall speed is ≈2.9–5.3× (floor 2.94×).
- Verdict: strengthens. Recorded evidence level: **measured**.

> **Verdict: WEAKENED.** The conclusion survives: the gap is not closed. Two parts of the claim do not.
>
> - **A hidden assumption moves every simulated number.** The author's model gets velocity by
>   differencing two consecutive frames. Miln et al. used Tracker. In Tracker's source code, the
>   default velocity is a central difference over three frames, (x[n+1] − x[n−1]) / 2Δt. That
>   window is 16.7 ms at 120 fps, not 8.3 ms. Re-run with that estimator (simulated):
>   - b falls to **0.930–1.270**, not 0.964–1.657;
>   - the margin is **≈2.8–4.0×**, not 2.9–5.3×; the floor is **2.84×**, below the claimed 2.94×;
>   - the rise time that closes the gap is **≈2 ms**, not ≈1 ms.
> - **The evidence label is wrong.** "Measured" applies only to the 25.6 ms time-to-peak, and that
>   number is the author's digitisation of a figure. The bias band b and the margin are simulated or
>   calculated. The claim sentence gives "0.96–1.66×" with no "simulated" beside it.
> - **The verdict still stands.** Even a 2 ms rise time is ~13× shorter than the measured 25.6 ms
>   mean. A 2 ms peak is also ≥6 SD from that mean (SD ≥ 7 ms inferred from s.e.m. 1.8, n ≥ 15).

---

## 1. Arithmetic, redone independently

I re-ran the author's script `S21-D-D-deepen-sim.py` unchanged (numpy, seed 1). It reproduced every
printed number: A0 0.875/0.966/0.991; t_p 2.5 ms b = 0.660; t_p 1.0 ms b = 0.320; measured-shape
phase min 0.964; σ_x = 1 mm p95 1.657; plateau 19.4 ms; 10→90% rise 16.5 ms. All of these are
**simulated**.

I then computed the margin M = V_s · b / U_read myself, with U_read = 1.38 m/s (calculated):

| b | Source | U_true (m/s) | M at 4.22 | M at 4.37 |
|---|---|---|---|---|
| 0.877 | alpha pulse, t_p 5 ms | 1.574 | 2.68 | **2.78** ✓ |
| 0.660 | alpha pulse, t_p 2.5 ms | 2.091 | 2.02 | **2.09** ✓ |
| 0.320 | alpha pulse, t_p 1.0 ms | 4.31 | 0.98 | 1.01 ✓ |
| 0.964 | measured shape, floor | 1.432 | **2.95** ✓ | 3.05 |
| 1.657 | measured shape, σ_x 1 mm p95 | 0.833 | 5.07 | **5.25** ✓ |

- **The author's arithmetic is correct** for the author's model.
- The quoted band "2.9–5.3×" uses the 4.22 m/s stall speed at the low end and 4.37 m/s at the high
  end. This matches the stated C_L,max range of 1.07–1.15. It is not an error.

## 2. Proxy check

- **The speed point is a fair proxy.** Miln et al. tracked "the fish centre of mass … defined as the
  location at 0.35 body lengths from the tip to the snout". Danos & Lauder used the midpoint between the
  pectoral fins. These are similar body-fixed points. Neither is a true COM in a bending body. The
  difference is not shown to matter, and I do not claim it does.
- **Time-to-peak is a partial proxy.** What sets the 120 fps under-read is the *width of the peak*, not
  the time from onset to peak.
  - The author handled this correctly: §3.3 simulates on a digitised trace shape, not on 25.6 ms alone.
  - That width comes from **one** sample sequence (Fig. 2B, peak 0.62 m/s, below the 0.86 m/s group
    mean). The claim sentence says "adult zebrafish actually reach … with a ~19 ms plateau". The source
    doc caveats this, but the sentence generalises from one trace to the species.

## 3. Hidden assumption: the velocity estimator (tested relaxed)

**The author's assumption.** Both S21-D-D and S21-D-D-D compute speed as |x[n+1] − x[n]| / Δt, a
two-point difference over one 8.3 ms interval. Neither document cites Miln for this.

**What Miln et al. state** (read-level: full-text, Europe PMC XML PMC8025299, keyword-scanned this
session):

- "We analysed videos (in Tracker Video Analysis and Modelling software, 4.01, Open Source Physics …)
  using the fish centre of mass as the tracking point."
- "four escape responses were analysed for each fish and the fastest speed was used".
- **No velocity algorithm or smoothing is stated for the fast start.** For the separate "realized speed"
  measure they write "the maximum speed calculated across two video frames". That phrase is ambiguous
  between the two estimators, and it does not describe the fast-start measure.

**What Tracker does by default** (read-level: full-text source code, fetched this session from
`raw.githubusercontent.com/OpenSourcePhysics/tracker/master/src/.../PointMass.java` and
`FirstDerivative.java`):

- `protected int algorithm = FINITE_DIFF;` and `protected int vDerivSpill = 1;`.
- With spill = 1, `xDeriv[i] = (- x[i - step] + x[i + step]) / 2`, divided by
  `dt_v = (tf - to) / (2 * vDerivSpill)`.
- So the default speed is a **central difference spanning two frame intervals** (16.7 ms at 120 fps).
- **Caveat:** this is the current `master` branch. Miln used version 4.01. I did not check the 4.01
  source. I also cannot tell whether Miln changed the default, or read speeds some other way. **Miln's
  actual estimator is `unknown`.** Central differencing is the software default, not an observation of
  what Miln did.

**Re-run under central differencing (SIMULATED).** Script: `docs/research/fish/challenge-129-sim.py`
(numpy, seed 7). It uses the same alpha pulse, the same digitised Fig. 2B trace, the same 3 ms smoothing,
the onset-corrected phase and max of 4. The only change is the estimator.

| Profile | Estimator | b (mean) | M at 4.37 |
|---|---|---|---|
| alpha t_p 5 ms, σ_x 0 | two-point | 0.877 | 2.78 |
| alpha t_p 5 ms, σ_x 0 | **central** | **0.683** | **2.16** |
| alpha t_p 2.5 ms, σ_x 0 | central | 0.401 | 1.27 |
| alpha t_p 2.0 ms, σ_x 0 | central | 0.325 | **1.03 (≈ gap closes)** |
| alpha t_p 25.6 ms, σ_x 0 | central | 0.982 | 3.11 |
| measured shape, single trial, worst phase | two-point / **central** | 0.964 / **0.930** | 3.05 / **2.95** |
| measured shape, max of 4, σ_x 1 mm, p95 | two-point / **central** | 1.664 / **1.270** | 5.27 / **4.02** |
| measured shape, max of 4, σ_x 2 mm, p95 (outside author's grid) | central | 1.617 | 5.12 |

**Reading** (my inference, conditional on Miln having used Tracker's default):

- **Bias band:** b ≈ 0.930–1.270 at σ_x 0–1 mm. The central difference widens the time window, so it
  under-reads the peak slightly more. It also averages position noise, so it inflates the max-of-4
  less.
- **Margin (calculated):** **≈2.84× (at 4.22) to ≈4.02× (at 4.37)**. The low end falls just below the
  claimed floor of 2.94×. The high end falls well below the claimed 5.3×.
- **Sensitivity statement:** "halving t_p 5 → 2.5 ms cuts the margin 2.78 → 2.09×" becomes 2.16 → 1.27×.
  "~1 ms closes the gap" becomes **~2 ms**. So the author's sensitivity ranking holds, and is even
  stronger: t_p matters more than the author computed.
- **What does not change:** a 2 ms peak against a measured 25.6 ± 1.8 ms (s.e.m.) mean time-to-peak.
  The inferred SD is ≥ 7 ms, which is the author's inference and mine too. So 2 ms sits ≥ 3 SD from the
  mean on any reading, and ~13× short of it. **The under-read loophole stays shut under the relaxed
  assumption.**
- **The upper end of b is still set by an assumed σ_x**, not by a measurement. Manual Tracker clicking
  on a GoPro frame could exceed 1 mm. At σ_x 2 mm the p95 rises back to 1.62. Larger noise only lowers
  U_true, so it cannot close the gap. It does mean the top of any margin band is assumption-driven.

## 4. Is the evidence level honest?

**No. The recorded level "measured" overstates the claim.**

- **Measured:** time to maximum COM velocity 25.6 ms, s.e.m. ≈ 1.8 ms. This is a value Danos & Lauder
  measured at 1000 fps. The number itself is the author's digitisation of their Fig. 4B bar.
  - I could **not** check the digitisation. `journals.biologists.com/jeb/article-pdf/215/11/1854/1444827/1854.pdf`
    returned HTTP 403 to curl this session.
  - Read-level for Danos & Lauder in this review: **could-not-access**. The values are relayed from the
    author.
- **Simulated:** b = 0.964–1.657. The source doc labels it simulated. The claim sentence does not
  ("the 120 fps max-of-4 reading is 0.96-1.66x the true peak").
- **Calculated:** true peak 0.83–1.43 m/s and margin 2.9–5.3×.
- **"Shut by measurement"** should read "shut by a simulation run on one measured profile shape, plus a
  measured mean time-to-peak". The correct level for the claim as a whole is **simulated, on measured
  inputs**.

## 5. Missed regimes and counter-examples

- **Velocity estimator:** see §3. This is the one substantive omission, and it moves the numbers.
- **Larval zebrafish** have much faster time courses. **I did not search for or quantify this**, so no
  value is given. Larvae are not the population in either source, so they are not a counter-example to
  an adult claim.
- **Faster escapes may have narrower peaks.** The shape comes from a 0.62 m/s sequence; the fish in
  question reads 1.38 m/s. I found no adult zebrafish trace for a faster sequence.
  - **Scope of that negative:** I did no literature search of my own. I rely on the author's Europe PMC
    screen of 40 of 73 hits.
  - For the gap to close under central differencing, the peak would have to be ≈2 ms wide, ~10× narrower
    than the sample trace. I have no evidence for or against a narrowing of that size.
- **Miln's Dryad data** (doi:10.5061/dryad.v15dv41tr) would give the actual frame series and settle the
  estimator question. I did not retry it this session; read-level: could-not-access, as reported by the
  author.

## Sources

| Source | Read-level |
|---|---|
| S21-D-D-D: `docs/research/fish/S21-D-D-deepen.md`, `S21-D-D-deepen-sim.py`, `S21-D-D-fig2b-trace.txt` (branch `claude/deepen-s21-d-sensitive-input-no42sx`, commit 0d17d892) | full-text (repo); script re-run |
| S21-D-D: `docs/research/fish/S21-D-deepen.md` (commit 6b64006b) | full-text (repo), grep-read for Miln methods |
| Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146, PMC8025299 | full-text XML, keyword-scanned (Tracker, frames, speed, fastest, 0.35) |
| Tracker source, OpenSourcePhysics/tracker `master`: PointMass.java, FirstDerivative.java | full-text (source code). Version 4.01 not checked |
| physlets.org Tracker help pages | could-not-access (proxy 403) |
| Danos & Lauder 2012, J Exp Biol 215:1854 | could-not-access (HTTP 403); figure values relayed from the author |

```swarm-challenge
{"claim_id": 129, "outcome": "weakened", "reason": "The gap is still not closed, but the author assumed two-point frame differencing while Miln et al. used Tracker, whose default velocity is a 3-frame central difference; re-simulated, that gives b 0.930-1.270, a margin of ~2.8-4.0x (floor 2.84x < claimed 2.94x) and ~2 ms (not ~1 ms) to close the gap, and the 'measured' evidence label overstates what are simulated/calculated outputs.", "corrected_value": "margin ~2.84-4.02x (simulated, central-difference estimator, sigma_x 0-1 mm); gap-closing rise time ~2 ms; evidence level: simulated on measured inputs", "depends_on": ["S21-D-D-D chain M = V_s * b / U_read (commit 0d17d892)", "Miln et al. 2021 (PMC8025299) fastest-fish fast-start 1.38 m/s at 120 fps, max of 4, as digitised by S21-D-D", "Miln et al. 2021 methods: speed from Tracker 4.01, estimator not stated", "assumption: Miln used Tracker's default FINITE_DIFF velocity with spill 1 (central difference), from Tracker master source, not version 4.01", "Danos & Lauder 2012 Fig 4B time to max COM velocity 25.6 +/- 1.8 ms s.e.m., as digitised by the author (not re-checked: could-not-access)", "Danos & Lauder 2012 Fig 2B single sample trace (S21-D-D-fig2b-trace.txt) as profile shape", "inferred SD of time-to-peak >= 7 ms from s.e.m. 1.8 ms and n >= 15", "simulation assumptions: 3 ms running mean as true profile, random frame phase, Gaussian sigma_x 0-1 mm, max of 4", "replicate-24 stall speed V_s 4.22-4.37 m/s (C_L,max 1.15-1.07)"]}
```
