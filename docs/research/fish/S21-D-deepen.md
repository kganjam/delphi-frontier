# S21-D-D: deepening S21-D on its most sensitive input

Project: `zebrafish-flight` · Scale: behaviour · Written 2026-11-04

**Parent answer (S21-D, commit `9ae82754`, branch `claude/zebrafish-fast-start-velocity-pgqbck`; read-level
full-text):**

- Miln et al. 2021 measured per-fish maximum fast-start speeds in n = 50 adults at 120 fps.
- S21-D digitised those speeds as ~0.45–1.38 m/s. That range brackets S21's Re-derived 0.842 m/s.
- The fastest fish is ~4.2× below a **5.84 m/s** threshold.
- S21-D's verdict was **strengthens**, with the margin revised to "~4–7×". S21-D also floated a
  hypothetical 2× under-read at 120 fps.

> **Short answer.**
>
> - **The input the margin is most sensitive to:** the fastest fish's peak speed, U_fast = 1.38 m/s.
>   It enters the margin linearly. Every threshold input enters only as a square root.
> - **No single input wrong by 2× flips the binary conclusion.** I recomputed this; it is not
>   asserted. A flip needs U_fast to be wrong by ≥3.2×.
> - **I bounded the 120 fps measurement bias by simulation, not by measurement.** Under stated
>   assumptions the recorded max-of-4 speed is 0.88–1.40× the true peak. That rules out S21-D's
>   hypothetical 2× under-read. It places the fastest fish's true peak at **≈0.99–1.58 m/s**.
> - **S21-D compared against a stale threshold.** It used the C_L = 0.6 stall speed (5.84 m/s). The
>   project's corrected value is 4.37 m/s (C_L,max 1.07; replicate-24).
> - **Recomputed margin: ≈2.7–4.8× for the fastest fish** (central 3.2×), and ≈5.2× for a typical fish.
>   S21-D's "~4–7×" margin does not survive.
> - **Verdict: STANDS.** The qualitative conclusion holds: the gap is not closed.

---

## 0. Corrections to S21-D's provenance (from reading the repository)

- **S21-D said "the S21 write-up is not in this repository." That is wrong.**
  - It is `docs/research/fish/S21-behaviour.md`, commit `68f929cb`. Read-level: full-text (repo doc).
  - S21 read Danos & Lauder 2012 in full-text HTML. Its Re was computed "using fish length,
    **maximum linear velocity per sequence** and the appropriate viscosity", filmed at **1000 fps**
    (author's words, as quoted by S21).
  - S21-D suspected that Re came from a *mean* speed. **That suspicion is not supported.** It was a
    mean over sequences of per-sequence *peaks*, which is what S21 itself said.
- **The 5.84 m/s threshold has a known origin in this repository.** It is the stall speed of the
  reference wing:
  - 0.4 g fish, span 1 BL = 4 cm, AR 5, S = 3.2×10⁻⁴ m², at **C_L = 0.6**.
  - After the C_L,max correction to 1.07 (Wakeling & Ellington 1997 dragonfly wings; read-level
    search-summary, as relayed by `replicate-24.md`), the threshold is **4.37 m/s**.
  - Source: `docs/research/fish/replicate-24.md` (commit `922d3d1d`; full-text repo doc).
  - S21-D quoted the older 5.84.
- **The Miln et al. data are on Dryad, not figshare.** The paper's Data accessibility statement says
  "Data has been deposited in Dryad (https://doi.org/10.5061/dryad.v15dv41tr)". Figshare holds only
  the electronic supplementary material. Read-level: full-text (Europe PMC XML, PMC8025299).

## 1. Which input is the conclusion most sensitive to? (recomputed)

S21-D's conclusion compares two numbers:

- margin M = V_s / U_fast, with V_s = √(2mg / (ρ·S·C_L,max))
- "gap not closed" ⇔ M > 1

**Central case** (calculated): V_s = 4.37 m/s (C_L,max 1.07) and U_fast = 1.38 m/s, so **M = 3.17**.
With S21-D's stale 5.84 m/s, M would be 4.23.

| Input wrong by 2× (one at a time) | Exponent in M | M if input ×2 | M if input ÷2 | Factor needed to reach M = 1 |
|---|---|---|---|---|
| **U_fast (fish peak speed)** | **−1** | **1.58** | 6.33 | **×3.17** |
| fish mass m | +½ | 4.48 | 2.24 | ÷10.0 |
| wing area S (span², AR) | −½ | 2.24 | 4.48 | ×10.0 |
| C_L,max | −½ | 2.24 | 4.48 | ×10.0 (C_L ≈ 10.7, physically excluded) |
| air density ρ | −½ | (physical constant, not a free input) | | |

All entries are calculated.

- **No single 2× error changes the binary conclusion.**
- **U_fast is the most sensitive input.** It is the only one with unit elasticity, and it is the only
  one where a single error of ~3× would close the gap.
- The threshold inputs need ~10× errors, because they enter through a square root.
- **The input to attack is therefore U_fast = 1.38 m/s.**

## 2. How well established is U_fast?

**Evidence level: measured by the authors, digitised by S21-D and re-digitised by me. Its bias is
unquantified in every source.**

### Where the number comes from

- **Authors' method (Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146; read-level full-text,
  Europe PMC PMC8025299):**
  - mechanical tail stimulus, 30 mm water depth, GoPro Hero 6 at **120 frames s⁻¹**;
  - manual tracking in Tracker of a body-fixed point at 0.35 BL from the snout;
  - "four escape responses were analysed for each fish and the fastest speed was used".
- **Peer-review history (read-level full-text, `rsos210146_review_history.pdf` in the Europe PMC
  supplementary bundle):**
  - Two reviewers objected to using the fastest of four trials.
  - The authors answered that "it is a standard procedure to measure several fast starts and then use
    the maximal speed".
  - Nobody in the review discussed frame rate or tracking error.
- **No numeric value is printed.** The speeds exist only in Figure 1a.

### My re-digitisation of Fig. 1a

This is my measurement of a figure, not the authors' number:

- **Calibration.** x-axis ticks at px 78.5 / 160.5 / 241.5 / 323.5 for 0 / 0.5 / 1.0 / 1.5 m/s, so
  163.3 px per m/s (≈0.006 m/s per px).
- **Fastest fish.** The rightmost circles span px 299–309, a centre of **1.38 m/s**. The red, blue and
  green circles sit at the same x, so they are the same fish on days 1, 4 and 7.
- **Next-fastest fish.** No circles fall between px 274 and 298. The next fish's centre is about
  px 268, which is **≈1.16 m/s**.
- So the fastest fish is an **isolated outlier, ~0.22 m/s above the next fish**. It is one individual's
  best trial out of four.

This matters because S21-D's 1.38 m/s is the **largest of ~200 noisy trials** (50 fish × 4).
Measurement noise inflates an extreme order statistic. The coarse 120 fps sampling deflates it. Neither
the authors nor S21-D quantified either effect.

### What else would test the number

| Source | What it gives | Read-level |
|---|---|---|
| Danos & Lauder 2012, J Exp Biol 215:1854 (doi:10.1242/jeb.068957) | Mean of per-sequence maximum Re 27,800 ± 2,140 s.e.m. (n = 5 adults, TL 33 mm, 1000 fps, unsmoothed frame differencing). S21 converts this to 0.84 m/s. Table 1, the direct velocity, is unread. | Re: full-text (via S21); Table 1: **could-not-access** (this session: journals.biologists.com 403; sites.harvard.edu, dash.harvard.edu, researchgate.net, core.ac.uk, scholar.archive.org, unpaywall, semanticscholar all refused by proxy) |
| McKee & McHenry 2020, Integr Org Biol (PMC7750966) | Adult zebrafish, 1000 fps. "mean escape speed measured in response to the live predator (v = 3.7 cm s⁻¹, N = 63)". This is a *mean* over an unspecified window, not a peak. It is not comparable to U_fast, and I do not average it in. Its disagreement with peak values (~20×) reflects definition, not a contradiction I can resolve. | full-text (keyword-scanned) |
| Miln et al. raw data (Dryad doi:10.5061/dryad.v15dv41tr) | Exact per-fish fast-start speeds and standard lengths | **could-not-access** (datadryad.org refused by proxy) |

**Scope of the negative search for another adult peak value (this session):**

- Europe PMC, open access only, two queries:
  - (Danio OR zebrafish) AND (fast-start OR fast start OR escape response) AND (m s-1 OR cm s-1 OR BL s-1)
    NOT larva*: **15 hits**, all titles screened. Zebrafish-adult hits were only Miln 2021 and McKee &
    McHenry 2020.
  - AUTH:"Seebacher F" AND zebrafish AND (fast start OR escape OR sprint): **4 hits**. PMC6546753 and
    PMC11340812 were keyword-scanned in full text. They contain U_crit / U_Cfast flume data only, with
    no fast-start speeds.
- One extended web search for Danos & Lauder Table 1 values found no numbers.
- Paywalled journals, theses and non-English literature were not covered.

## 3. Improving U_fast: bounding the measurement bias (SIMULATION, not observation)

The real quantity is each fish's true instantaneous peak centre-of-mass speed. The authors' raw data
are unreachable, so I bounded how far a 120 fps max-of-4 reading can sit from the true peak.

**Model (all assumptions are mine):**

- Centre-of-mass speed follows an alpha pulse, v(t) = V·(t/t_p)·e^(1−t/t_p).
- Time to peak t_p = 5, 10 or 20 ms. This range is an assumption; I have no adult zebrafish source for
  it.
- Sampling at 120 fps with random phase. Gaussian position error σ_x per frame of 0, 0.25, 0.5 or
  1.0 mm. Assumed: about 1–3 px at an unknown GoPro resolution over a 600 mm tank.
- Two-point differencing, maximum over 4 trials, 1500 replicates per cell, V = 1 m/s.
- For comparison, 1000 fps with one trial and σ_x = 0–0.12 mm, the Danos & Lauder-like case.
- Script: `docs/research/fish/S21-D-deepen-sim.py`, numpy, seed fixed.

| Setup (simulated) | t_p = 5 ms | t_p = 10 ms | t_p = 20 ms |
|---|---|---|---|
| 120 fps, max of 4, σ_x = 0 | 0.875 | 0.966 | 0.991 |
| 120 fps, max of 4, σ_x = 0.5 mm | 0.916 | 1.039 | 1.094 |
| 120 fps, max of 4, σ_x = 1.0 mm | 0.992 | 1.143 | 1.232 (p95 1.399) |
| 1000 fps, 1 trial, σ_x = 0.06 mm | 1.078 | 1.106 | 1.132 |
| 1000 fps, 1 trial, σ_x = 0.12 mm | 1.186 | 1.241 | 1.295 |

Values are mean measured / true peak (simulated).

**Reading of the simulation** (my inference, conditional on the model):

- **120 fps under-reads a smooth peak by at most ~12%**, and only for a 5 ms rise time with zero
  tracking noise. A two-frame difference spans 8.3 ms, which is short against a rising-and-coasting
  speed pulse. **S21-D's hypothetical "2× under-read" is not supported.** It would need a rise time
  well under 5 ms.
- **Tracking noise biases the max-of-4 reading *upward*** by up to ~1.23× (mean) or ~1.40× (95th
  percentile) at σ_x = 1 mm. The fastest of 50 fish is exactly the kind of value this inflates.
- **The Danos & Lauder 1000 fps figure may also be biased upward**, by about 1.08–1.30× at sub-pixel
  noise. Unsmoothed 1 ms differencing amplifies position error. So the two adult sources do not
  disagree as much as their nominal values imply, but I keep them separate.
- **Improved input** (calculated as 1.38 / [0.875 … 1.40]): true peak of the fastest fish
  **U_fast ≈ 0.99–1.58 m/s**, central ≈1.38 m/s. For a typical fish, the Danos & Lauder mean of peaks
  of 0.84 m/s corresponds to ≈0.65–0.82 m/s after removing the simulated 1.03–1.30× noise inflation
  (calculated).

**What would settle it, and the cost** (these are estimates):

1. **Allow `datadryad.org` in this session's network settings.** Then read Miln's per-fish values and
   standard lengths. Cost: $0. This replaces my digitisation and gives BL/s.
2. **Read Danos & Lauder Table 1.** It needs `sites.harvard.edu`, or library access at about $0–50.
   It gives a 1000 fps COM maximum directly.
3. **Run a definitive measurement:**
   - 20 adults at 28 °C, filmed at ≥1000 fps with a calibrated scale;
   - silhouette-centroid COM, with filtering validated by a synthetic-motion test like the one above;
   - report every trial, not just the max.
   - Estimated cost: ~1–2 person-weeks with a borrowed high-speed camera.

## 4. Recomputed conclusion

The threshold uses the corrected V_s = 4.37 m/s (band 4.22–4.77 for C_L,max 1.15–0.9). The old C_L 0.6
value is shown for continuity. All entries are calculated.

| Fish speed used | U (m/s) | M at V_s = 4.37 | M across V_s 4.22–4.77 | M at old 5.84 |
|---|---|---|---|---|
| S21-D fastest fish, as digitised | 1.38 | **3.17** | 3.06–3.46 | 4.23 |
| Fastest fish, simulated upper bound on true peak | 1.58 | 2.77 | **2.67**–3.02 | 3.70 |
| Fastest fish, simulated lower bound on true peak | 0.99 | 4.43 | 4.28–**4.83** | 5.92 |
| Next-fastest Miln fish (my digitisation) | 1.16 | 3.77 | 3.64–4.11 | 5.03 |
| Typical fish (Danos & Lauder mean of peaks, S21) | 0.84 | 5.19 | 5.02–5.67 | 6.95 |

- **The gap does not close under any combination in the table.** Closing it at the most favourable
  corrected threshold (4.22 m/s) needs a true peak 2.7× above the simulated upper bound for the fastest
  fish.
- **S21-D's "~4–7×" falls.** It used the uncorrected threshold, and the fastest fish is likely
  noise-inflated rather than under-read. The defensible margin is **≈2.7–4.8× for the fastest adult**
  (central 3.2×) and **≈5× for a typical adult**.
- **S21-D's "strengthens" was partly right.** A direct measurement does now support the magnitude.
  But it overstated the margin.

**Verdict: STANDS.** The conclusion "adult zebrafish fast-start peak speed is well below the take-off
stall speed of the reference wing; the gap is not closed" holds under every input I could improve.
The quantitative margin narrows from ~4–7× to **~2.7–4.8×**. Whoever cites S21-D should cite the
narrower band.

### Remaining caveats

- The bias band comes from a simulation with an assumed pulse shape, rise time and noise level. It is
  not a measurement.
- Miln fish lengths are unknown to me (they are on Dryad), so BL/s and any scaling to the 4 cm design
  fish are not computed.
- Miln tested at 23 °C. A 28 °C test would plausibly raise speed; the size of that effect is `unknown`.
- V_s depends on design premises (0.4 g mass, 1-BL span, AR 5) and on a dragonfly-wing C_L,max proxy.
  The primary source for the 0.4 g mass is `unknown`. These enter only as square roots, so a 2× error
  in any of them moves M by 1.41× and does not flip the conclusion (§1).
- This is the in-water burst speed, not a water-exit speed.

## Sources

| Source | Read-level |
|---|---|
| S21: `docs/research/fish/S21-behaviour.md` (commit 68f929cb) | full-text (repo) |
| S21-D: `docs/research/fish/S21-deepen.md` (commit 9ae82754) | full-text (repo) |
| Replication 24: `docs/research/fish/replicate-24.md` (commit 922d3d1d) | full-text (repo) |
| Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146, doi:10.1098/rsos.210146 (PMC8025299), incl. Fig. 1 and review history | full-text |
| Miln et al. Dryad data, doi:10.5061/dryad.v15dv41tr | could-not-access |
| Danos & Lauder 2012, J Exp Biol 215:1854, doi:10.1242/jeb.068957 | Re value: full-text via S21; Table 1: could-not-access |
| McKee & McHenry 2020, Integr Org Biol, doi:10.1093/iob/obaa023 (PMC7750966) | full-text (keyword-scanned) |
| Seebacher-lab zebrafish papers PMC6546753, PMC11340812 | full-text (keyword-scanned; no fast-start speeds) |
| Wakeling & Ellington 1997 (C_L,max 1.07), via replicate-24 | search-summary |

```swarm-result
{"subproblem": "S21-D-D", "evidence": "measured (Miln et al. 2021 Fig. 1a, full-text, re-digitised by me) + simulated bias bound (my Monte Carlo, not observation) + corrected threshold from repo replicate-24", "answer": "The input the S21-D conclusion is most sensitive to is the fastest adult's fast-start speed (unit elasticity; no single 2x error in any input flips the conclusion, a ~3.2x error in this one would); a simulation bounds the 120 fps max-of-4 reading at 0.88-1.40x of the true peak, ruling out S21-D's hypothetical 2x under-read and giving a true peak of ~0.99-1.58 m/s; against the corrected 4.37 m/s stall threshold (S21-D used the stale 5.84 m/s) the margin is ~2.7-4.8x (typical fish ~5x), so the gap is still not closed but S21-D's ~4-7x margin is withdrawn.", "key_number": "fastest adult true peak fast-start speed ~0.99-1.58 m/s (central 1.38 m/s; simulated bias band 0.88-1.40x on a 120 fps max-of-4 reading); margin to 4.37 m/s stall speed ~2.7-4.8x", "verdict": "stands", "depends_on": ["Miln, Ward & Seebacher 2021 (doi:10.1098/rsos.210146) Fig. 1a per-fish fast-start speeds, 120 fps, max of 4 trials, as digitised by me (fastest 1.38 m/s, next 1.16 m/s)", "S21-D (commit 9ae82754) digitised range 0.45-1.38 m/s", "S21 (commit 68f929cb): Danos & Lauder 2012 mean maximum Re 27,800 +/- 2,140, TL 33 mm, 1000 fps -> 0.84 m/s (derived)", "simulation assumptions: alpha-pulse speed profile, rise time 5-20 ms, tracking noise sigma_x 0-1.0 mm at 120 fps and 0-0.12 mm at 1000 fps", "law level_flight_lift / stall speed V_s = sqrt(2mg/(rho S C_L,max))", "replicate-24 (commit 922d3d1d): corrected stall speed 4.37 m/s at C_L,max 1.07", "C_L,max 1.07 (band 0.9-1.15) from Wakeling & Ellington 1997 dragonfly wings, search-summary proxy for fin membrane", "design premise: fish mass 0.4 g (primary source unknown)", "design premise: reference wing span 1 BL = 0.04 m, AR 5, S = 3.2e-4 m^2", "air density 1.2 kg/m^3", "assumption: in-water burst speed is an upper proxy for water-exit speed"]}
```
