# Challenge 129: adversarial review of S21-D-D-D (rise-time sensitivity and the measured time course)

Project: `zebrafish-flight` · Written 2026-11-04 · Reviewer did not write the claim.

**Claim under review (author's words, from `harvest:deepen-s21-d-sensitive-input-no42sx`, branch
`claude/deepen-s21-d-sensitive-input-no42sx`, commit `0d17d892`, doc `docs/research/fish/S21-D-D-deepen.md`):**
the margin is most sensitive to the assumed rise time t_p. Adult zebrafish reach peak COM velocity
25.6 ± 1.8 ms (s.e.m.) after onset, with a ~19 ms plateau above 90% of peak. The 120 fps max-of-4 reading
is therefore 0.96–1.66× the true peak, the true peak is ~0.83–1.43 m/s, and the margin is ~2.9–5.3×.
Verdict: strengthens.

**Reviewer verdict: WEAKENED.**

- The core conclusion survives: the gap is not closed, and the low end of the margin (≈2.9×) reproduces.
- The **upper half of the stated band is wrong.** The b upper bound of 1.66 comes from applying tracking
  noise to a 0.61 m/s profile. The fish being corrected moves at 1.38 m/s. Scaled correctly, b ≈ 0.96–1.26,
  the true peak ≈ 1.10–1.43 m/s, and the margin ≈ **2.9–4.0×**, not 2.9–5.3×. These are calculated and
  simulated values (my simulation).
- The recorded evidence level of "measured" overstates two of the three headline numbers.

**Sources used in this review:**

- The author's doc, sim script and digitised trace (`S21-D-D-deepen.md`, `S21-D-D-deepen-sim.py`,
  `S21-D-D-fig2b-trace.txt` at commit 0d17d892). Read-level: **full-text (repo)**.
- Danos & Lauder 2012 (doi:10.1242/jeb.068957). Read-level for me: **could-not-access / not re-fetched**. I
  rely on the author's digitised trace and values.
- Miln et al. 2021. Read-level for me: **not re-read**. The values are as relayed in the claim.

---

## 1. Independent arithmetic

I wrote my own simulation for this review: `docs/research/fish/challenge-129-check.py`. It uses numpy with
seed 7 and an independent implementation, though the same model family. All outputs below are **calculated
or simulated**, not observed.

| Check | Author | Mine | Status |
|---|---|---|---|
| Gap-closing b = 1.38/4.37 | 0.316 | 0.316 | ✔ |
| Alpha pulse, t_p = 5 ms, noise-free max-of-4 (onset-fixed) | b 0.877, M 2.78 | b 0.877, M 2.78 | ✔ |
| t_p = 2.5 ms | b 0.660, M 2.09 | b 0.659, M 2.09 | ✔ |
| t_p = 1.0 ms | b 0.320, M 1.01 / 0.98 | b 0.321, M 1.02 / 0.98 | ✔ (gap closes at V_s 4.22) |
| Smoothed trace peak; time ≥ 90% of peak | 0.613 m/s; 19.4 ms | 0.6126 m/s; 19.37 ms | ✔ |
| Measured shape, noise-free max-of-4 | 0.975 [0.971, 0.977] | 0.975 [0.971, 0.977] | ✔ |
| Measured shape, σ_x = 1 mm, p95 **at the trace's own 0.61 m/s peak** | 1.657 | 1.653 | ✔ (reproduces) |
| Low-end margin 4.22 / (1.38/0.964) | 2.94 | 2.95 | ✔ |
| High-end margin 4.37 / (1.38/1.657) | 5.25 | 5.25 | arithmetic ✔, input ✘ (see §2) |

The sensitivity ranking, the low end of b and the low end of the margin all reproduce independently.

## 2. The defect: tracking noise is scaled to the wrong speed

In the author's section (B), position noise σ_x is added to the Danos & Lauder sample trace at its own
amplitude, a 0.61 m/s peak. The resulting b is then applied to the Miln fish at 1.38 m/s.

- A two-point 120 fps difference turns σ_x into velocity noise of √2·σ_x·120. At σ_x = 1 mm that is
  ≈0.17 m/s, whatever the fish's speed (calculated).
- That noise is 28% of a 0.61 m/s peak, but only ~12% of a ~1.4 m/s peak.
- So the noise-driven over-read depends on speed. Borrowing it from a fish 2.3× slower inflates b.

**Rerun with the measured shape rescaled to a 1.415 m/s true peak (simulated, mine):**

| σ_x | b mean | p5 | p95 |
|---|---|---|---|
| 0 | 0.975 | 0.972 | 0.977 |
| 0.5 mm | 1.049 | 0.995 | 1.116 |
| 1.0 mm | 1.137 | 1.036 | **1.259** |

**Corrected values (my calculation from these simulated b):**

- b ≈ 0.964–1.26.
- True peak = 1.38/b ≈ 1.10–1.43 m/s.
- Margin at V_s 4.22–4.37 m/s ≈ **2.95–3.99×**, against the claim's 2.9–5.3×.

**What this changes:**

- The claim's statement that the band "widens at the top (4.8 → 5.3×)" is an artefact of the scaling error.
  The corrected top, ≈4.0×, is *narrower* than the parent's 4.8×. My inference is that the parent's
  alpha-pulse sim, run at a 1 m/s peak, carried a smaller version of the same issue. I did not rerun the
  parent to confirm this.
- The error is on the safe side for the verdict. A smaller b-upper means a *higher* lower bound on the true
  speed, which shrinks the margin's top end. It does not move the bottom end, which is set by the noise-free
  under-read. **It cannot close the gap.**
- The upper end also rests on σ_x = 0–1 mm, which is assumed. Miln's σ_x is `unknown`, as the author says. A
  larger σ_x would raise b-upper again. The top of the band is assumption-bounded either way, and should not
  be reported as a measured result.

## 3. Proxy check

| Quantity that matters | Proxy used | Assessment |
|---|---|---|
| Speed-time profile of the *fastest Miln fish* (1.38 m/s, 23 °C, tail-touch stimulus) | One "sample" Danos & Lauder sequence (one fish, 0.62 m/s, temperature unstated, dropped object), rescaled in amplitude | The proxy is weak in shape but has a very large timescale margin. The ~19 ms plateau comes from **one** trace. The claim sentence presents it as a property of adult zebrafish, which overgeneralises one sequence. The 25.6 ms time-to-peak is a group mean (n ≥ 15), so it is the better-supported input. |
| True COM velocity | Velocity of a fixed body point (the midpoint between the pectoral fins, in a stretched-straight frame) | During a C-bend, a fixed body point is not the COM. Its velocity peak may be sharper or offset. Miln's tracked point is `unknown` to me. This affects both datasets similarly and is unlikely to be a 25× effect. Not quantified. |
| Rise time from COM onset | Time from the *first snout movement* | Snout motion leads COM motion, so 25.6 ms slightly *over*states the COM rise. The bias is a few ms at most (my inference), against a ~1 ms rise needed to close the gap. |

## 4. Hidden assumption, relaxed

The result rests on this assumption: **the fastest Miln fish does not have a ≥25× shorter rise than the
Danos & Lauder group mean.**

**Relaxed as far as the data allow (calculated):**

- Take the author's inferred SD of ≥7 ms, which is itself an inference from the s.e.m. with n ≥ 15. A
  2-SD-fast escape still peaks at ≈11 ms.
- An alpha pulse with t_p ≥ 5 ms gives M ≥ 2.68 even in the parent's model.
- **Independent physical bound (my calculation, not in the claim):**
  - Danos & Lauder's mean max speed over their mean time-to-peak implies a mean acceleration of
    0.856/0.0256 ≈ 33 m/s².
  - Reaching a 4.3 m/s true peak in ~1 ms would need a mean acceleration of ~4300 m/s². That is ~130× the
    implied mean.
  - I did not look up published peak-acceleration maxima for adult zebrafish, so I give no comparator
    number.
- **Temperature.** Miln's fish were at 23 °C. Danos & Lauder's temperature is unstated. If Danos & Lauder
  ran warmer (unknown), Miln's fish would be slower-twitch, which lengthens the rise and favours the claim.
  I found no source either way. Search scope: none beyond the author's.

The assumption survives relaxation by more than an order of magnitude.

## 5. Evidence level

The recorded evidence level is **"measured"**. It is honest only for the 25.6 ± 1.8 ms time-to-peak. Even
that is the reviewer-author's digitisation of a published bar chart, so it is "measured (digitised)".

| Headline number | Actual level |
|---|---|
| b = 0.964–1.657 | **Simulated** on an assumed σ_x range. The upper end is also mis-scaled (§2). |
| True peak 0.83–1.43 m/s | **Calculated** from simulated b. |
| Margin 2.9–5.3× | **Calculated**. |
| ~19 ms plateau | **Measured from one trace**, generalised in the claim sentence to "adult zebrafish". |

The claim's key_number field does label b as "(simulated)", which is to its credit. The record's single
evidence level of "measured" is still a defect, and should read: measured input (digitised), simulated
bias, calculated margin.

## 6. Missed regimes and counter-examples

- **Larval zebrafish** have much shorter fast starts (ms-scale stage 1). They are a different regime and do
  not bear on the adult Miln fish. I did not search for them. This is not a counter-example.
- **Other fast-start species** (e.g. pike) were not searched. They would be proxies at best.
- I found no published adult-zebrafish time course with a sub-5 ms rise. **Scope:** I ran no new literature
  search. I relied on the author's Europe PMC screen (40 of 73 hits) and one web search. The negative result
  is only as wide as that.

## Verdict

**WEAKENED.**

- The direction and the low end hold. The gap is not closed (M ≥ 2.9×), and the under-read loophole is
  closed by a measured mean time-to-peak.
- The b upper bound (1.66) and the margin upper bound (5.3×) are inflated, because noise was applied at a
  0.61 m/s amplitude rather than at ~1.4 m/s. Corrected (simulated/calculated): b ≈ 0.96–1.26, true peak
  ≈ 1.10–1.43 m/s, margin ≈ 2.9–4.0×.
- "Measured" overstates the level of the simulated and calculated headline numbers.
- The "~19 ms plateau" rests on a single sample trace.

```swarm-challenge
{"claim_id": 129, "outcome": "weakened", "reason": "The gap-not-closed conclusion and the 2.9x floor reproduce independently, but the b upper bound of 1.66 (and margin top of 5.3x) comes from tracking noise applied to a 0.61 m/s trace instead of the 1.38 m/s fish; rescaled, b is 0.96-1.26 and the margin 2.9-4.0x, and the 'measured' evidence label overstates simulated/calculated numbers.", "corrected_value": "b = 0.964-1.26 (simulated, sigma_x 0-1 mm, measured shape rescaled to 1.415 m/s peak); true peak 1.10-1.43 m/s; margin 2.95-3.99x at V_s 4.22-4.37 m/s (calculated)", "depends_on": ["S21-D-D-D doc and sim at commit 0d17d892 (docs/research/fish/S21-D-D-deepen.md, S21-D-D-deepen-sim.py)", "Danos & Lauder 2012 Fig 2B single sample COM-velocity trace as digitised by the claim author (S21-D-D-fig2b-trace.txt), taken as profile shape", "Danos & Lauder 2012 Fig 4B time to max COM velocity 25.6 +/- 1.8 ms s.e.m. (claim author's digitisation)", "Danos & Lauder 2012 Fig 3I mean max COM velocity 0.856 m/s (claim author's digitisation)", "Miln et al. 2021 fastest-fish 120 fps max-of-4 reading 1.38 m/s (as relayed via S21-D-D)", "stall speed V_s 4.22-4.37 m/s from replicate-24 (C_L,max 1.07-1.15)", "assumption: tracking noise sigma_x 0-1 mm, Gaussian, two-point differencing at 120 fps", "assumption: measured profile shape scales in amplitude only (timing unchanged) from 0.61 m/s to ~1.4 m/s", "my simulation docs/research/fish/challenge-129-check.py (seed 7)"]}
```
