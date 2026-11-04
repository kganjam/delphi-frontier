# S21 — Peak fast-start velocity of adult *Danio rerio*

Project: `zebrafish-flight` · Scale: behaviour · Written 2026-11-04

> **Short answer.** I could not read a *directly reported* peak escape velocity for adult zebrafish.
> The one adult study filmed at ≥1000 fps that I reached is Danos & Lauder 2012. It reports a
> **measured** mean maximum Reynolds number of 27,800 ± 2,140 (s.e.m.) in normal water, for adults of
> 33.0 mm total length. Working backwards from that number, **I compute** a peak speed of
> **≈0.84 m/s (≈25 body lengths/s), plausible range 0.78–0.93 m/s**. This speed is my calculation from
> their measurement. It is not printed in the paper. It is about 1.5× the Ucrit proxy (0.548 m/s)
> and about 7× below the 5.8 m/s refutation threshold.

---

## 1. The question, stated precisely

The question is the highest instantaneous speed an **adult** zebrafish reaches during a fast-start
(C-start escape). It must be:

- measured from high-speed video at **≥1000 fps**,
- given in m/s and in body lengths per second (BL/s),
- reported with the method and the fish size.

**Why the number is hard to pin down:**

- **The current launch verdict rests on a sustained-swimming proxy.** That proxy is Ucrit =
  0.548 m/s. At 4 cm body length that is already 13.7 BL/s (my arithmetic). I did not check where
  0.548 m/s came from: it is not in this repository.
- **The refutation threshold is 5.8 m/s.** A 4 cm fish would need **145 BL/s** to reach it. A
  3.3 cm fish would need **176 BL/s**.
- **Burst speed is not reported where you would expect it.** The zebrafish fast-start literature is
  overwhelmingly about larvae (3–28 dpf). Adult escape studies mostly report timing, angles and
  neural data, not linear speed.

## 2. What is measured

Read-level legend: full-text | abstract | listing | search-summary | could-not-access.

### 2a. Adult zebrafish, ≥1000 fps: the only qualifying study

| Quantity | Value | Source | Read-level |
|---|---|---|---|
| Fish | adults, n = 5, **total length 33.0 ± 1.3 mm** | Danos N, Lauder GV (2012) *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957 | full-text HTML (Methods/Results text) |
| Filming | ventral view, **1000 frames/s**, Photron PCI 1024 camera | same | full-text HTML |
| Arena | circular container, 12 cm diameter, 10 cm water depth | same | full-text HTML |
| Stimulus | a flat-based cylinder (~1.5 cm diameter) dropped into the tank | same | full-text HTML |
| Velocity method | "Linear velocity and acceleration were calculated by dividing displacement by the time between consecutive image frames." No smoothing is described in the text I read. | same | full-text HTML |
| **Peak Re, normal water (1 mPa·s)** | **"The mean maximum Reynolds number in 1 mPa s water was 27,800 (±2140 s.e.m.)"** | same | full-text HTML |
| How Re was calculated | "using fish length, maximum linear velocity per sequence and the appropriate viscosity" | same | full-text HTML |
| Peak Re at 10 and 20 mPa·s | 2,350 and 820 | same | full-text HTML |
| Latency | 8.9 ms in normal water | same | search-summary (not re-checked in full text) |
| **Max centre-of-mass velocity, max tail velocity (Table 1)** | **unknown to me.** Table 1 is published only as an image. | same | **could-not-access** (see below) |
| Water temperature | not given in the text I read | same | full-text HTML |

**What I tried in order to read Table 1:**

1. **Journal page.** It rendered as text, but Table 1 is an image (`m_table016.jpeg`) behind a signed
   CDN link.
2. **Direct download with curl.** The journal page returned a 5.6 kB stub instead of the article, and
   the lab's PDF host returned "CONNECT 403".
3. **Other copies.** The Lauder lab PDF (sites.harvard.edu), Harvard DASH and zendy.io were all
   unreachable: their hostnames are not allowed by this session's network policy.
4. **Europe PMC.** It lists the paper as not open access and has no full text.

Allowing `sites.harvard.edu` in the network settings would very likely give the full PDF, Table 1
included.

### 2b. Adult zebrafish, but below the frame-rate bar

| Quantity | Value | Source | Read-level |
|---|---|---|---|
| Startle Umax vs temperature | **values only in Figure 1; no number in the text** | Condon CH, Chenoweth SF, Wilson RS (2010) *J Exp Biol* 213:3705–3709 | full-text HTML (text only) |
| Method | 200 Hz camera; tap on the arena; head digitised; first 40 ms; 3-point moving average; highest Umax per fish per temperature; standard length 25–30 mm | same | full-text HTML |

This study does not meet the bar: 200 Hz is far below 1000 fps. It also probably underestimates the
peak, because the frame rate is coarse and the data are smoothed. That underestimate is my
inference, not the authors' claim. I did not read the figure values.

### 2c. Values found but excluded, kept here so nobody reuses them

- **"0.71 ± 0.03 m/s, 17.1 ± 1.4 m/s², N = 7 fish" (centre of gravity, escape responses).**
  - It came up in two web-search summaries described as zebrafish. One summary called it larval; the
    other said the life stage was not stated.
  - I could not find its source. Its context (viscosity having "no detectable effect" at 20 °C) matches
    Johnson, Cullum & Bennett (1998), *Partitioning the effects of temperature and kinematic viscosity
    on the C-start performance of adult fishes*. As far as I could see from search summaries, that
    study used goldfish and guppies, not zebrafish.
  - Read-level: search-summary.
  - **Excluded: the species is unconfirmed and probably not *Danio*.**
- **Larval zebrafish speeds.** All search-summary only, and not adult:
  - up to 8 BL/s at 14 dpf (Müller & van Leeuwen 2004, *J Exp Biol* 207:853);
  - ">50 body lengths per second" in strong larval escapes (a conference abstract);
  - 0.15 m/s for one 5 dpf larva;
  - a simulated (CFD) larval peak of about 7.4 BL/s.

  None of these are used.
- **Ontogeny claim.** A search summary of a zebrafish escape-development study says length-specific
  peak speed rises during larval growth, the gains "cease when fish become juveniles", and absolute
  speed in m/s keeps increasing. I did not identify the paper or read it.
  - Read-level: search-summary.
  - If true, BL/s is roughly flat from juvenile to adult. That reading is my inference.

### 2d. Studies checked and found to contain no adult linear speed

- Issa et al. 2011, *J Exp Biol* 214:1028. Larvae 3–5 dpf, 1000 fps; reports only angular velocity
  (20 ± 3.1 and 8.4 ± 4.4 deg/ms). Read-level: full-text HTML.
- Ravel et al. 2025, *iScience* 28:112056. 5 dpf larvae at 10,000 fps; velocities appear only in
  figures. Read-level: full-text HTML.
- Conradsen & McGuigan 2015, *J Fish Biol* 87:1219. Adults, but Ucrit only, no fast-start.
  Read-level: abstract via search-summary.

**What the negative search covered.**

- About 12 web searches (standard and extended) on combinations of: adult zebrafish / *Danio rerio*,
  fast-start / C-start / escape / startle, peak / maximum velocity, m/s, cm/s, BL/s, 1000 fps,
  burst / sprint speed, Fu & Cao (cyprinid fast-starts), and Fontaine / Müller ontogeny.
- Direct reads of Danos & Lauder 2012, Condon et al. 2010, Issa et al. 2011, Ravel et al. 2025 and
  Europe PMC metadata.
- **What it did not cover:** Chinese-language literature; theses; paywalled full texts on blocked
  hosts (sites.harvard.edu, dash.harvard.edu, zendy.io, sicb.org, discovery-pp.ucl.ac.uk); and
  figure digitisation.
- I could not retrieve the Domenici & Blake (1997) fast-start review (my guessed journal URLs led
  to unrelated papers). So I have **not** checked its cross-species tables for *Danio*.

## 3. What I computed (calculation, not observation)

By definition, Re = U·L/ν, so **U = Re·ν/L**.

**Assumptions** (these are mine; the paper does not state them in the text I read):

- **ν = 1.0×10⁻⁶ m²/s.** That is 1 mPa·s divided by ρ = 1000 kg/m³. Using ρ = 998 changes U by
  less than 0.3%.
- **L = 0.033 m**, the reported mean total length. The authors say "fish length". If they used
  standard length, or each fish's own length, U shifts. For example, an assumed L of 0.030 m gives
  0.93 m/s.
- **Averaging.** "Mean maximum Re" is the mean over sequences of each sequence's peak, so U below is
  a **mean of peaks**, not the single fastest event.
- **Which point is tracked.** "Maximum linear velocity" is most likely the centre of mass, since
  that is the variable the abstract discusses. If it was the tail tip instead, the body's peak speed
  is lower than computed.

| Re (normal water) | U = Re·ν/L (m/s) | U/L (TL/s) |
|---|---|---|
| 27,800 − 2,140 (−1 s.e.m.) | 0.78 | 23.6 |
| **27,800 (mean)** | **0.84** | **25.5** |
| 27,800 + 2,140 (+1 s.e.m.) | 0.91 | 27.5 |

**Ratios (calculation):**

- **Against the Ucrit proxy:** 0.84 / 0.548 = **1.54×**.
- **Against the refutation threshold:** 0.84 / 5.8 = **0.145**. The threshold is **6.9×** the
  derived peak.
- **Scaled to the 4 cm target fish, assuming BL/s does not change with size:** 25.5 × 0.04 =
  **1.02 m/s**, still **5.7×** below 5.8 m/s. This is an extrapolation. Within a species, BL/s
  usually falls or stays flat as fish grow (the ontogeny claim in 2c points the same way), so
  1.02 m/s is probably an upper estimate for a 4 cm adult. That reading is my inference.

## 4. The answer and its evidence level

**Evidence: `derived`.**

- **Measured by the authors:** a mean peak Re of 27,800 ± 2,140 for adult zebrafish (TL 33 mm),
  filmed at 1000 fps, frame-differenced video, in normal water.
- **Derived by me:** a mean peak escape speed of about **0.84 m/s (≈25 TL/s)**, range 0.78–0.93 m/s
  under the stated assumptions.
- No source I read reports a measured adult zebrafish peak velocity anywhere near 5.8 m/s. The
  derived value sits **about 7× below** the refutation threshold.

**Consequences for the launch verdict:**

- **The refutation condition is not met** by any number I found.
- **Swapping Ucrit for burst speed makes the launch deficit about 1.5× smaller, not the "several
  times" the project premise assumed.** The project's "burst ≈ several × Ucrit" expectation is **not
  borne out** for this species by this one data point. A likely contributor is that the 0.548 m/s
  Ucrit is itself high for a 3–4 cm fish (≈14–17 BL/s). This disagreement stays open; I have not
  resolved it.

## 5. What this does NOT establish

- **It is not a directly reported velocity.** Table 1 of Danos & Lauder (2012) almost certainly
  gives the maximum COM velocity directly. I did not read it. If Table 1 disagrees with 0.84 m/s,
  Table 1 wins.
- **It is not the maximum fish.** n = 5 fish, the mean of per-sequence peaks, a ±1 s.e.m. band. The
  fastest single escape is higher than the mean by an unknown amount. Elite individuals and
  best-of-N trials were not assessed.
- **The length convention is unconfirmed.** Total length vs standard length, and mean vs
  per-individual L, each shift U by about 10%. The BL/s figure uses total length.
- **Temperature is unknown.** No water temperature was found in the text I read. Fast-start speed in
  ectotherms depends on temperature (Johnson et al. 1998, search-summary; Condon et al. 2010), so
  the derived value is tied to an unstated lab temperature, probably around 26–28 °C. That
  temperature is an assumption, not read from the paper.
- **The stimulus may not draw out the fastest escape.** A dropped object in a 12 cm dish may not
  produce maximal escapes. Being confined could also cap stage-2 acceleration.
- **Measurement noise.** Frame differencing at 1 ms with no stated smoothing tends to *inflate*
  noisy peak velocities, while digitisation error can push either way. The direction of the net bias
  is unknown.
- **It is not a launch speed.** This is the in-water body speed during a C-start, not the speed at
  water exit. Breaking the surface, a changed body plan, and any fin or tail-taxi phase (in which
  flyingfish keep accelerating while partly airborne) are untouched here. It also says nothing about
  sustained thrust, power density or muscle limits.
- **It does not settle how BL/s scales between 3.3 cm and 4 cm.** The 1.02 m/s figure for a 4 cm fish
  is an extrapolation.
- **The adult literature has not been ruled out.** The negative search scope is in §2. A paper
  with an explicit adult peak velocity may exist behind the blocked hosts or in theses.
- **It does not verify the 0.548 m/s Ucrit**, which this work takes from the project brief.

## 6. What would change the answer

1. **Read Table 1 of Danos & Lauder 2012** (full PDF; needs `sites.harvard.edu` allowed in the
   network policy, or institutional access). This turns `derived` into `literature`/`measured` and
   pins down COM vs tail and the length convention.
2. **Digitise Fig. 1 of Condon et al. 2010.** This gives a second adult value with a temperature
   series, at 200 Hz, so treat it as a lower bound.
3. **Run a new measurement.** Adult AB/WIK zebrafish, 3.5–4.5 cm SL, filmed at ≥2000 fps in a large
   arena (≥10 body lengths) at 28 °C, with acoustic, vibrational and looming stimuli. Track the
   centre of mass with a validated filter, and report the per-fish maximum alongside the mean. Only a
   value **≥5.8 m/s (≥145 BL/s at 4 cm)** would overturn the launch verdict. On present evidence
   that is about 7× beyond the derived value. Reaching it would require a body change (muscle mass
   fraction, power output, body form), not a better measurement.
4. **Re-examine the 0.548 m/s Ucrit source.** If it is wrong or inflated, the burst-to-Ucrit ratio
   and the size of the headline deficit both move.

```swarm-result
{"subproblem": "S21", "evidence": "derived", "answer": "No directly reported adult zebrafish peak fast-start velocity could be read; from the measured mean maximum Reynolds number (27,800 ± 2,140 s.e.m.; adults TL 33 mm, 1000 fps; Danos & Lauder 2012, full-text) I compute a mean peak speed of ~0.84 m/s (~25 TL/s, range 0.78-0.93 m/s), about 1.5x the Ucrit proxy and ~7x below the 5.8 m/s refutation threshold.", "key_number": "0.84 m/s (derived from Re = 27,800, L = 0.033 m, nu = 1.0e-6 m^2/s)", "blocked_on": "Table 1 of Danos & Lauder 2012 (direct max COM velocity) is image-only; full PDF hosts (sites.harvard.edu, dash.harvard.edu, zendy.io) are outside this session's network policy"}
```
