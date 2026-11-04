# S21-D-D-D: deepening S21-D-D on its weakest input

Project: `zebrafish-flight` · Scale: behaviour · Written 2026-11-04

**Parent answer (S21-D-D, `docs/research/fish/S21-D-deepen.md`, commit `6b64006b`; read-level full-text,
repo doc):**

- The fastest of Miln et al.'s (2021) 50 adults reads 1.38 m/s. That is a 120 fps, max-of-4-trials value.
- A Monte Carlo bounds the reading at 0.88–1.40× the true peak, which puts the true peak at ≈0.99–1.58 m/s.
- Against the corrected take-off stall speed of 4.37 m/s, the margin is **≈2.7–4.8×**. The gap is not
  closed. Verdict: **stands**.

> **Short answer.**
>
> - **The weakest input is the speed-pulse rise time t_p.** S21-D-D assumed t_p = 5–20 ms with "no adult
>   zebrafish source for it". t_p sets the bias factor b, and b sets the true peak.
> - **It is also the most sensitive input.** I recomputed this under S21-D-D's own model. Halving t_p
>   from 5 to 2.5 ms cuts the margin from 2.78× to 2.09×. At t_p ≈ 1.0 ms the gap closes (M ≈ 1.0).
>   No threshold input can do that with a 2× error.
> - **Improved with a primary source.** I read Danos & Lauder 2012 in full text and digitised its
>   figures. Adult zebrafish reach maximum centre-of-mass velocity **25.6 ± 1.8 ms (mean ± s.e.m.)** after
>   the first movement. Their sample trace rises over 16.5 ms and then holds ≥90% of peak for 19.4 ms.
>   That is ~25× longer than the ~1 ms a flip needs.
> - **Re-run on the measured profile shape (simulated):** b = **0.96–1.66**. The true peak of the fastest
>   fish is **≈0.83–1.43 m/s**. The margin is **≈2.9–5.3×** at C_L,max 1.07–1.15 (up to 6.5× at C_L,max
>   0.7).
> - **Verdict: STRENGTHENS.** The low end of the margin rises from 2.7× to 2.9×. The under-read scenario
>   is now excluded by a measured time course, not by an assumption.

---

## 1. Which input is S21-D-D's conclusion most sensitive to? (recomputed)

S21-D-D's chain (all its terms, nothing added):

- M = V_s / U_true, and U_true = U_read / b.
- U_read = 1.38 m/s, digitised from Miln et al. Fig. 1a.
- b = (120 fps max-of-4 reading) / (true peak), from a Monte Carlo of an alpha-pulse speed profile.
- V_s = √(2mg / (ρ S C_L,max)) = 4.37 m/s (replicate-24).

The gap closes when M ≤ 1. That needs **b ≤ 1.38/4.37 = 0.316**, or ≤ 0.327 at the most favourable
V_s of 4.22 m/s.

**Rank by elasticity (calculated):**

- M ∝ U_read⁻¹ · b¹ · m^½ · S^−½ · C_L,max^−½.
- U_read is a digitised measurement with ±0.006 m/s pixel resolution. Its next-fish neighbour is 1.16 m/s.
- The square-root inputs need ~10× errors to flip M (S21-D-D §1, which I did not re-derive).
- **b is the only elasticity-1 term that is not a measurement.** It is a simulation output, and its low
  end is driven entirely by one assumption, the rise time t_p.

**Sensitivity of M to t_p, recomputed in S21-D-D's own model.** Script `S21-D-D-deepen-sim.py`,
section (A). It uses 120 fps, max of 4, noise-free, and onset-corrected sampling (see §3.3). All
values are simulated or calculated.

| t_p (assumed) | b (simulated mean) | U_true = 1.38/b (m/s) | M at V_s 4.37 | M at V_s 4.22 |
|---|---|---|---|---|
| 5 ms (S21-D-D's floor) | 0.877 | 1.57 | 2.78 | 2.68 |
| **2.5 ms (÷2)** | **0.660** | **2.09** | **2.09** | 2.02 |
| 1.25 ms (÷4) | 0.393 | 3.51 | 1.24 | 1.20 |
| **1.0 ms (÷5)** | **0.320** | **4.31** | **1.01** | **0.98: gap closed** |

- **A 2× error in t_p moves M by 25%.** That is more than a 2× error in any of m, S or C_L,max can
  achieve in the same direction, once U_read is held fixed.
- **A 5× error closes the gap.** No other input in the chain gets to M = 1 with less than a ~3× error,
  and the only one that can is U_read, which is measured.
- **t_p is therefore the input to attack.** It is the most sensitive non-measured input, and the
  least established one.

## 2. How well established was t_p?

**Evidence level in S21-D-D: assumption.** S21-D-D said so in its own words: "This range is an
assumption; I have no adult zebrafish source for it."

- No number in the chain constrained it.
- The alpha-pulse shape was also assumed. It ties rise and decay to one timescale, so a short t_p also
  forces an implausibly short burst.
- S21-D-D listed Danos & Lauder 2012 Table 1 as `could-not-access`. **I have now read it. Table 1
  contains ANOVA P-values only.** The kinematic means are plotted in Figs. 3 and 4, not tabulated. So
  even full access to Table 1 would not have supplied t_p.

## 3. Improving it: a measured time course

### 3.1 Primary source

Danos N, Lauder GV (2012). *Challenging zebrafish escape responses by increasing water viscosity.*
J Exp Biol 215:1854–1862, doi:10.1242/jeb.068957.

- **Read-level: full-text.** The PDF was fetched this session via WebFetch from
  journals.biologists.com/jeb/article-pdf/215/11/1854/1444827/1854.pdf, then extracted with `pdftotext`
  and rendered with `pdftoppm`.
- The HTML page, Silverchair CDN images, OpenAlex and bioRxiv were all refused by the proxy or returned
  403 for direct curl.

**Authors' methods (their words or close paraphrase):**

- Five fish, "mean total length 33.0±1.3 mm".
- Filmed at "1000 frames s⁻¹" with a Photron PCI 1024 (1024×1024 px).
- Escapes elicited by a dropped object.
- 52 escapes across three viscosities. "At least three" sequences per fish per viscosity, so the
  1 mPa s n is ≥15. The exact count is not stated.
- COM = "the midpoint between the pectoral fins" of a stretched-straight fish.
- "Linear velocity and acceleration were calculated by dividing displacement by the time between
  consecutive image frames". No smoothing is described.
- "For all maxima calculated, we also recorded the time it took for the maximum to be reached from
  the beginning of the escape response". Stage 1 begins "in the frame of the first visible movement of
  the fish's snout".
- **Water temperature is not stated.** I searched the extracted text for "°C" and "temperature"; the
  only hits are in the discussion of other studies.

### 3.2 My digitisation (my measurements of the authors' figures, not the authors' numbers)

These are all at 1 mPa s (normal water), from the PDF rendered at 400 dpi. Each axis was calibrated
on ≥6 tick marks.

| Quantity | Figure | Value | Method |
|---|---|---|---|
| **Time to maximum linear COM velocity** | Fig. 4B, orange bar | **25.6 ms, s.e.m. ≈1.8 ms** (error bar top 27.4) | ticks 0–50 ms, 14.75 px/ms |
| Maximum COM velocity | Fig. 3I, black bar | **856 mm/s, s.e.m. ≈65** (error bar top 921) | ticks 0–2500, 0.276 px per mm/s |
| Stage 1 / stage 2 duration | Fig. 3G | ≈18.5 / ≈22 ms (read by eye) | n/a |
| Sample COM-velocity trace (one sequence, one fish) | Fig. 2B, left | rises from 0.11 m/s at t = 0, reaches ~0.53 m/s at 17 ms, plateaus ~0.59–0.62 m/s from 18 to 32 ms, then 0.54 m/s at 37 ms. Raw max **0.624 m/s at 29.8 ms** | column-wise curve trace, 507 points, `S21-D-D-fig2b-trace.txt` |

**Checks and inferences.**

- **Re cross-check.** The Fig. 3I maximum of 0.856 m/s agrees with S21's Re-derived value:
  27,800 × 10⁻⁶ / 0.033 = 0.842 m/s. This is a consistency check within one paper, not an independent
  confirmation.
- **Inferred SD of time-to-peak.** With s.e.m. ≈ 1.8 ms and n ≥ 15, the SD is ≈7 ms or more. This is my
  inference; the authors give no SD. So a fast sequence two SDs below the mean still peaks at ~11 ms or
  later. That is ~10× the ~1 ms a flip needs.

### 3.3 Re-running the bias calculation on the measured shape (SIMULATION, not observation)

Script: `docs/research/fish/S21-D-D-deepen-sim.py` (numpy, seed 1). Section (B) uses the digitised Fig. 2B
trace.

**Setup:**

- **"True" profile.** A 3 ms running mean of the trace, which removes the authors' 1 ms differencing
  jitter. Its smoothed peak is 0.613 m/s at 30.4 ms.
- **Sampling.** The profile is integrated to position, then sampled at 120 fps with random phase and
  two-point differenced.
- **Maximum over 4 trials**, with the same σ_x grid as S21-D-D.

**Correction to S21-D-D's script.** It began sampling at a random time in [0, 1/120 s) *after* motion
onset. That silently drops the first partial frame of displacement.

- I start sampling one frame before onset instead.
- Section (A0) reproduces S21-D-D's numbers with the original sampling: 0.875 / 0.966 / 0.991 at
  t_p = 5 / 10 / 20 ms.
- With the fix the values are 0.877 / 0.966. **For t_p ≥ 5 ms the artefact is immaterial (<0.3%).**
  It matters only for t_p ≤ 2.5 ms, where it exaggerated the under-read.

**Results (simulated):**

| Setup | b (mean) | p5 | p95 |
|---|---|---|---|
| Measured shape, single trial, noise-free, all 200 phases | 0.971 (range **0.964**–0.977) | n/a | n/a |
| Measured shape, max of 4, σ_x = 0 | 0.975 | 0.971 | 0.977 |
| Measured shape, max of 4, σ_x = 0.25 mm | 1.062 | 1.001 | 1.135 |
| Measured shape, max of 4, σ_x = 0.5 mm | 1.165 | 1.046 | 1.307 |
| Measured shape, max of 4, σ_x = 1.0 mm | 1.376 | 1.154 | **1.657** |
| *For comparison:* alpha pulse at t_p = 25.6 ms, σ_x = 1 mm | 1.249 | 1.120 | 1.399 |

**Reading (my inference, conditional on the trace being representative):**

- **The worst-case 120 fps under-read is 3.6%, not 12%.** The measured profile has a ~19 ms plateau
  above 90% of peak, and a 8.3 ms two-frame window cannot miss it.
- **The noise-driven over-read is larger than S21-D-D found.** At σ_x = 1 mm the p95 is 1.66 rather
  than 1.40. A flat-topped profile gives the max-of-N noise more frames near the peak to exploit.
  This moves the true peak *down*, which widens the margin.
- **The Danos & Lauder 1 ms values look much less noise-inflated than S21-D-D simulated.** The trace's
  residual SD about its 3 ms smooth is **0.013 m/s**, and its raw max is only **1.019×** its smoothed max.
  S21-D-D had simulated 1.08–1.30× for the 1000 fps case.
  - This is one trace, and the residual includes my ±1 px digitisation error (~0.002 m/s).
  - I record the disagreement rather than resolve it: S21-D-D's figure was simulated from an assumed
    σ_x; mine is measured from one published trace.

### 3.4 Improved input

- **b ∈ [0.964, 1.657]**: the min over phase noise-free, to the p95 at σ_x = 1 mm (simulated, measured
  shape). It replaces S21-D-D's [0.875, 1.40].
- **True peak of the fastest Miln fish ≈ 0.83–1.43 m/s**, central ≈ 1.42 m/s if tracking noise is
  negligible (calculated: 1.38 / b).
- Miln's own σ_x is `unknown`. It would follow from the GoPro resolution and Tracker settings, which
  are not in the paper.

### 3.5 Scope of the negative search for an independent adult zebrafish rise time

**This session:**

- **Europe PMC**, query `(zebrafish OR "Danio rerio") AND ("fast start" OR "fast-start" OR "C-start" OR
  "escape response") AND ("time to peak" OR "time to maximum" OR "stage 1 duration" OR "duration of stage
  1" OR "maximum velocity")`: 73 hits, top 40 titles screened. The only adult-zebrafish kinematic paper
  with a time-to-peak-velocity measure was Danos & Lauder 2012. The others were larval, neural or
  disease-model papers. Hits 41–73 were not screened.
- **One extended web search** for Danos & Lauder time-to-maximum values returned no other source.
- **Not covered:** paywalled journals, theses, non-English literature, and other species (goldfish,
  bluegill), which I did not pull in as proxies.

### 3.6 What would settle it, and what it would cost (estimates)

- **Miln's per-trial frame data on Dryad** (doi:10.5061/dryad.v15dv41tr; still `could-not-access`,
  datadryad.org is blocked by the proxy):
  - Cost: $0 once the host is allowed.
  - Gives the actual speed-vs-frame series, so b no longer has to be simulated.
  - Caveat: the deposit may contain only per-fish maxima. Its contents are `unknown`.
- **The definitive experiment** is unchanged from S21-D-D: ≥1000 fps, ≥20 adults at the Miln
  temperature, every trial reported.

## 4. Recomputed conclusion

M = V_s / U_true. All entries are calculated.

- **V_s at the four C_L,max values:** 1.15 → 4.22 m/s, 1.07 → 4.37 m/s, 0.9 → 4.77 m/s, 0.7 → 5.40 m/s.
- **The C_L,max band is disputed between two replications of claim 24:**
  - `fish-replicate-24-4dc5w4` (commit 922d3d1d) gives **0.9–1.15**.
  - `fish-replicate-24-jyx1cf` (commit f73af564) gives **0.7–1.15**.
  - I show both rather than pick one. Both rest on a search-summary read of Wakeling & Ellington 1997.

| Speed used | U (m/s) | M at 4.22 | **M at 4.37** | M at 4.77 | M at 5.40 |
|---|---|---|---|---|---|
| Fastest fish, simulated upper bound (b = 0.964) | 1.43 | **2.94** | 3.05 | 3.33 | 3.77 |
| Fastest fish, noise-free central (b = 0.975) | 1.42 | 2.98 | **3.09** | 3.37 | 3.82 |
| Fastest fish, as read (b = 1) | 1.38 | 3.05 | 3.17 | 3.45 | 3.92 |
| Fastest fish, σ_x = 0.5 mm mean (b = 1.165) | 1.18 | 3.56 | 3.69 | 4.02 | 4.56 |
| Fastest fish, simulated lower bound (b = 1.657) | 0.83 | 5.06 | **5.25** | 5.72 | 6.49 |
| Next-fastest Miln fish (S21-D-D digitisation) | 1.16 | 3.63 | 3.77 | 4.11 | 4.66 |
| Typical adult, Danos & Lauder Fig. 3I mean max | 0.856 | 4.92 | 5.11 | 5.57 | 6.31 |

**Results:**

- **Margin for the fastest adult: ≈2.9–5.3×** at C_L,max 1.07–1.15, and up to ≈6.5× at C_L,max 0.7.
  S21-D-D gave ≈2.7–4.8×.
- **The low end rises from 2.67× to 2.94×.** The lowest margin anywhere in the table is 2.94×.
- **To close the gap, the true peak would have to be 2.9× the highest value my improved bias band
  allows.** Equivalently, the rise time would have to be ~1 ms against a measured 25.6 ± 1.8 ms.

**Verdict: STRENGTHENS.**

- S21-D-D's conclusion holds: the gap between adult zebrafish fast-start speed and the reference wing's
  stall speed is not closed.
- Its most dangerous corner, a short-rise-time under-read, is no longer only assumed away. It is
  contradicted by a measured adult time-to-peak.
- The margin band narrows at the bottom (2.7 → 2.9×) and widens at the top (4.8 → 5.3×), because
  tracking noise now biases the reading further upward.

### Caveats that remain (not resolved here)

- **The shape is one published sequence.** Fig. 2B is one sequence from one fish, called "a sample"
  by the authors. It also peaks at 0.62 m/s, below the 0.86 m/s group mean, so it is a slower-than-average
  escape. The mean time-to-peak (Fig. 4B) supports its timescale, but the plateau width of other
  sequences is `unknown`.
- **The populations differ.** Danos & Lauder: TL 33 mm, temperature not stated, dropped-object
  stimulus. Miln: 23 °C, tail-touch stimulus, lengths `unknown`. I have no zebrafish source for how
  time-to-peak scales with temperature or size. The factor needed to matter is ~25×.
- **b's upper end is driven by σ_x**, which is assumed (0–1 mm) for Miln's set-up. A larger σ_x only
  lowers U_true and widens the margin. It cannot close the gap.
- **The threshold side is unchanged and only as good as before:**
  - mass 0.4 g, primary source `unknown`;
  - span 1 BL = 4 cm and AR 5 are design premises;
  - C_L,max is a dragonfly-wing proxy, read only at search-summary level.
  These enter as square roots (S21-D-D §1).
- **The comparison is an in-water burst speed against an in-air stall speed.** That is a proxy for
  water-exit speed, not a measurement of it.

## Sources

| Source | Read-level |
|---|---|
| S21-D-D: `docs/research/fish/S21-D-deepen.md` + `S21-D-deepen-sim.py` (commit 6b64006b) | full-text (repo) |
| Danos & Lauder 2012, J Exp Biol 215:1854, doi:10.1242/jeb.068957: methods, Table 1 (P-values only), Figs. 2B, 3G, 3I, 4B | **full-text** (PDF; figure values digitised by me) |
| Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146, doi:10.1098/rsos.210146 | not re-read; values as relayed by S21-D-D (full-text there) |
| Miln et al. Dryad data, doi:10.5061/dryad.v15dv41tr | could-not-access (not retried) |
| replicate-24 (two branches: 922d3d1d, f73af564) | full-text (repo), grep-read for V_s, C_L,max band, mass provenance |
| Wakeling & Ellington 1997, J Exp Biol 200:543 (C_L,max 1.07 / 1.15) | search-summary, as relayed by replicate-24 |
| Europe PMC search (§3.5) | listing |

```swarm-result
{"subproblem": "S21-D-D-D", "evidence": "measured time course (Danos & Lauder 2012 full-text PDF, Figs 2B/3I/4B digitised by me) + simulated 120 fps bias on that measured shape (my Monte Carlo, not observation) + calculated margin", "answer": "S21-D-D's margin is most sensitive to its assumed speed-pulse rise time (halving it from 5 to 2.5 ms cuts the margin from 2.78x to 2.09x, ~1 ms closes the gap); adult zebrafish actually reach peak COM velocity 25.6 +/- 1.8 ms (s.e.m.) after onset with a ~19 ms plateau above 90% of peak, so the 120 fps max-of-4 reading is 0.96-1.66x the true peak, the fastest Miln fish's true peak is ~0.83-1.43 m/s, and the margin to the 4.22-4.37 m/s stall speed is ~2.9-5.3x: the gap is not closed and the under-read loophole is shut by measurement.", "key_number": "time to maximum COM velocity 25.6 ms (s.e.m. ~1.8 ms, adult zebrafish, 1000 fps, Danos & Lauder 2012 Fig 4B, digitised); resulting bias factor b = 0.964-1.657 (simulated) and margin >= 2.94x", "verdict": "strengthens", "depends_on": ["S21-D-D (commit 6b64006b) chain M = V_s / (U_read / b)", "Miln, Ward & Seebacher 2021 (doi:10.1098/rsos.210146) Fig. 1a fastest-fish fast-start speed 1.38 m/s at 120 fps, max of 4 trials, as digitised by S21-D-D", "Miln next-fastest fish 1.16 m/s (S21-D-D digitisation)", "Danos & Lauder 2012 (doi:10.1242/jeb.068957) Fig. 4B time to max COM velocity 25.6 +/- 1.8 ms s.e.m. at 1 mPa s (my digitisation)", "Danos & Lauder 2012 Fig. 2B single sample COM-velocity trace, 1 mPa s (my digitisation, S21-D-D-fig2b-trace.txt), taken as representative of profile shape", "Danos & Lauder 2012 Fig. 3I mean max COM velocity 856 +/- 65 mm/s (my digitisation)", "assumption: Danos & Lauder (TL 33 mm, temperature unstated, dropped-object stimulus) time course transfers to Miln fish (23 C, tail stimulus, lengths unknown)", "simulation assumptions: 3 ms running mean as true profile, random frame phase, Gaussian tracking noise sigma_x 0-1.0 mm, two-point differencing, max of 4 trials", "law level_flight_lift / stall speed V_s = sqrt(2mg/(rho S C_L,max))", "replicate-24 (commit 922d3d1d) V_s = 4.37 m/s at C_L,max 1.07, band 0.9-1.15", "replicate-24 (commit f73af564) C_L,max band 0.7-1.15 (disagrees on lower bound)", "C_L,max 1.07 from Wakeling & Ellington 1997 dragonfly wings, search-summary proxy for fin membrane", "design premise: fish mass 0.4 g (primary source unknown)", "design premise: reference wing span 1 BL = 0.04 m, AR 5, S = 3.2e-4 m^2", "air density 1.2 kg/m^3", "assumption: in-water burst speed is an upper proxy for water-exit speed"]}
```
