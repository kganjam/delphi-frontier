# S10 (tissue): is there enough muscle power for flapping?

Project: `zebrafish-flight`. Scale: tissue. Status: **derived** answer. The requirement comes from my own computation; the muscle capacities come from published measurements.

Short answer: **For sustained flapping, no.** The fish muscle that can run aerobically, which is slow/red muscle, has measured cycle-averaged power of about 5–10 W/kg muscle. My most generous computation of the hover requirement is about 34 W/kg flight muscle, and every other case I ran is higher. **For burst flapping lasting seconds, possibly.** Warm fast muscle from larval zebrafish has been measured at 134 W/kg in work loops. That reaches the computed requirement only if roughly a fifth or more of body mass is flight muscle at the pectoral girdle, and present-day zebrafish anatomy is nowhere near that (I have no measured value; see §5).

---

## 1. The question, restated with the numbers that make it hard

Can fish skeletal muscle deliver the cycle-averaged, mass-specific mechanical power that flapping flight needs for a 0.4 g, 4 cm *Danio rerio*, at the wingbeat frequency such a wing would need? The comparison has to be made at matched (a) temperature, (b) cycle frequency and (c) duration (sustained aerobic versus burst glycolytic).

Why it is hard:
- **Small fliers need high mass-specific power.** Momentum theory gives induced power ∝ √(W³/A). At 0.4 g, with no wing area to spare, that comes to several W per kg of *body* (§3). Only the flight-muscle fraction of the body produces it, so the requirement per kg of *muscle* is several times larger.
- **The fish muscle that can run sustainably is the weakest.** Teleost red (slow, aerobic) muscle is a thin lateral strip. Fast (white, glycolytic) muscle is powerful but fatigues within seconds. That is an inference from the general physiology of fish fibre types. I did not retrieve a source for the fatigue time course in zebrafish specifically.
- **Frequency.** The wing sized in §3 needs about 20 Hz (computed). The fish muscle measurements were made at 2–7 Hz (cold adult muscle) or at 40–100 Hz (warm larval muscle). None was made at 20 Hz.

## 2. What is measured

Every value below is a published measurement. "Read-level" says how much of the source I actually saw. Where a value reached me through a search engine's summary of the paper rather than the paper itself, it is marked *search-summary*.

### 2a. Fish muscle: cycle-averaged net power from work loops

| Value | Tissue / species / conditions | Source (year) | Read-level |
|---|---|---|---|
| **25–35 W/kg** muscle, maximum at 5–7 Hz | Fast fibres, short-horned sculpin *Myoxocephalus scorpius*, isolated fibre bundles, ~4 °C (temperature from the search summary) | Altringham & Johnston, *J Exp Biol* 157:409 (year **not confirmed**; I have not verified it) | search-summary (the publisher page cob.silverchair.com is blocked from this session) |
| **5–8 W/kg**, maximum at 2 Hz | Slow fibres, same preparation | same | search-summary |
| 20–25 W/kg, little seasonal change at 4 °C | Fish fast muscle fibres (species not confirmed in the summary) | Johnson & Johnston (1991) | search-summary |
| 27.5 W/kg (10 cm cod) to 16.4 W/kg (60 cm cod) | Cod fast muscle; power falls as body size rises | Anderson & Johnston (year not confirmed) | search-summary |
| **134.4 ± 19.9 W/kg at 80 Hz**; 122.9 ± 11.1 W/kg at 100 Hz | Larval zebrafish (5 dpf, wild type) myotomal muscle, work loops at **28 °C** | Mead, Kennedy, Palmer, Ebert & Warshaw, *Biophys J* 119:806–820 (2020), PMC7451861 | full-text (first ~100k of ~120k characters, read through an automated summarising fetch) |
| Net work 2.63 ± 0.18 J/kg at 40 Hz; 0.43 ± 0.27 J/kg at 120 Hz | same | same | full-text (as above) |
| Twitch force fell 15.5 ± 1.7% from the first twitch to the last | same (fatigue control during the protocol) | same | full-text (as above) |
| ~10 W/kg, plateau at 3–5 Hz | Largemouth bass red muscle | Johnson et al. (1994), per the search summary | search-summary |
| **8.8 W/kg** maximum at 4 Hz; maximum work 2.7 J/kg | Skipjack tuna deep red muscle | Syme & Shadwick, *J Exp Biol* 205:189 (2002) | search-summary of the abstract |
| **79 (anterior) vs 133 (posterior) W/kg** | Skipjack tuna "fibers", same authors | Society for Integrative and Comparative Biology (SICB) conference abstract (year not confirmed) | search-summary |

**Disagreement I am preserving.** The two skipjack values from the same authors differ by roughly 10–15×: 8.8 W/kg in the paper's abstract against 79–133 W/kg in the conference abstract. I could not read either source in full. The conditions behind them (temperature, fibre type, strain or phase) are therefore `unknown` to me, and I have not reconciled them. If the 133 W/kg figure is a sustained, aerobic red-muscle value, it changes the answer (§6).

**Not comparable, listed so nobody misuses it.** Johnston & van Leeuwen (1995) report sculpin escape-response power of 307 W/kg (C-bend) and 222 W/kg (contralateral contraction). These are **instantaneous** peak values, not cycle averages, so they are not comparable with any requirement in §3. Read-level: search-summary.

### 2b. Reference ceilings from fliers (for calibration only)

| Value | What | Source (year) | Read-level |
|---|---|---|---|
| ~350 W/kg cycle-averaged net shortening power; >400 W/kg in some preparations; 433 W/kg highest in vitro | Blue-breasted quail pectoralis, in vivo length cycle replayed in vitro, take-off | Askew & Marsh, *J Exp Biol* 204:3587 (2001) | search-summary of the abstract |
| 390 W/kg average required (one bird 530 W/kg) | Same species, from kinematics and aerodynamics | Askew, Marsh & Ellington, *J Exp Biol* 204:3601 (2001) | search-summary of the abstract |
| 98–133 W/kg muscle (assumes perfect elastic storage) | Hummingbird hovering, normal air to aerodynamic failure | Chai & Dudley, *Nature* 377:722 (1995) (attribution inferred from the URL nature.com/articles/377722a0) | search-summary |
| 167–186 W/kg muscle, aerodynamic power | Three hovering insects | Ellington (1984), as cited by a later paper | search-summary (secondary) |
| Proposed theoretical limits for striated muscle: 100 W/kg (Josephson), 230–250 (Weis-Fogh & Alexander 1977), 250 (Ellington), up to 430 (Pennycuick & Rezende) | Theoretical ceilings, which disagree with each other | Listed in a 2025 arXiv paper (arxiv.org/pdf/2510.02819) | search-summary (secondary); I did not read the originals |

Those ceilings disagree with each other by about 4×. I am not averaging them.

## 3. What I computed

**Everything in this section is my computation, not an observation.**

### 3a. Inputs and assumptions
- Mass m = 0.4 g, so weight W = m·g = 3.92 × 10⁻³ N. Air density ρ = 1.2 kg/m³.
- Wing semispan R = 2 cm (total span = body length) or R = 4 cm (total span = 2× body length, generous). **These are design assumptions.** No upstream subproblem (S1/S2) has fixed them; this repository has no S1/S2 file.
- Induced power for hovering, from Rankine–Froude momentum theory: P_ind = k·√(W³ / (2ρA)), with A = πR² and k = 1.2. Using the full disc πR² is generous: real flapping sweeps only part of the disc, which raises the power.
- Total aerodynamic power = M × P_ind, with M = 1.5 or 2.0 to cover profile power. This is an assumption. I did not compute profile power from wing drag.
- Flight-muscle fraction f (flight-muscle mass / body mass) = 0.1, 0.2 or 0.3. **Assumption.** I did not retrieve a measured flight-muscle fraction for birds or insects, and I have no measured pectoral-fin muscle fraction for zebrafish (`unknown`).
- Assumed elastic energy storage is perfect, so no inertial power is charged (generous).

### 3b. Arithmetic

R = 4 cm: A = π(0.04)² = 5.03 × 10⁻³ m²
W³ = 6.03 × 10⁻⁸; 2ρA = 1.207 × 10⁻²; √(W³/2ρA) = 2.24 × 10⁻³ W; × 1.2 → **P_ind = 2.69 mW = 6.7 W/kg body**

R = 2 cm: A = 1.257 × 10⁻³ m² → **P_ind = 5.37 mW = 13.4 W/kg body**

Required cycle-averaged power per kg of flight muscle = M · P_ind / (m · f):

| R | M | f = 0.1 | f = 0.2 | f = 0.3 |
|---|---|---|---|---|
| 4 cm | 1.5 | 101 | 50 | **34** (most generous case) |
| 4 cm | 2.0 | 134 | 67 | 45 |
| 2 cm | 1.5 | 201 | 101 | 67 |
| 2 cm | 2.0 | 269 | 134 | 90 |

(values in W/kg flight muscle)

### 3c. Design frequency (computed)

Wing area for R = 4 cm with aspect ratio 6: S = (2R)²/6 = 1.07 × 10⁻³ m². Mean lift coefficient assumed to be C_L = 1.5 (unsteady flapping; assumption).

Required speed at the second-moment radius r₂ = 0.55R:
U = √(2W/(ρ C_L S)) = 2.02 m/s

With a stroke amplitude of Φ = 120°, U = 2Φ r₂ f, which gives **f ≈ 22 Hz**. That is a computation, not a measurement.

### 3d. Placing the measurements against the requirement (computed)
- Larval zebrafish at 40 Hz: 2.63 J/kg × 40 Hz = **105 W/kg**. I calculated this from the measured work per cycle. The paper's own power value at 40 Hz is only in its Fig. 8E, which I did not read.
- At 22 Hz, the work needed per cycle is P_req / f. The most generous case gives 34/22 = 1.5 J/kg. The R = 2 cm, f = 0.2 case gives 134/22 = 6.1 J/kg. The larval data give 2.63 J/kg at 40 Hz. The value at 20 Hz is `unknown`: no measurement was retrieved, and I did not extrapolate one.
- Temperature: the sculpin and cod values were measured at about 4 °C. Scaling them to 28 °C with an assumed Q₁₀ of 2 multiplies them by 2^2.4 = 5.3, which would give roughly 130–185 W/kg. **This is a speculative extrapolation, not data.** The real Q₁₀ for power is not established here, and the Mead 2020 larval value is the measured warm reference.
- Forward flight: power at the minimum-power speed is lower than hover power. I did not compute it, because S1/S2 have not fixed the wing or the flight speed. It could lower every requirement in the table by an unknown factor below 1.

## 4. The answer

**Evidence level: derived.** Published muscle measurements (§2) are compared with my own momentum-theory requirement (§3).

- **Sustained flapping (aerobic, minutes or more): not supported.** Measured red/slow fish muscle gives 5–10 W/kg (sculpin slow 5–8, bass red ~10, skipjack red 8.8 per the paper abstract). My most generous hover requirement is 34 W/kg flight muscle, 3–7× higher. The more realistic cases are 10–50× higher. The single exception is the skipjack conference abstract reporting 79–133 W/kg, which disagrees with the same authors' paper and whose conditions I could not establish.
- **Burst flapping (seconds, glycolytic fast muscle): physically within range, but only under conditions zebrafish do not meet.** Warm larval zebrafish fast muscle at 134 W/kg (measured, 80 Hz, 28 °C) covers every computed case with f ≥ 0.2, and the R = 4 cm, M = 2, f = 0.1 case at exactly 134. Cold adult fast muscle at 16–35 W/kg (measured at ~4 °C) covers only the single most generous case, and only at its upper end.
- **The binding constraint therefore looks like muscle *quantity at the fin*, not tissue power density.** That is my inference from the table, not a measurement. Even the 134 W/kg tissue works only if about 10–30% of body mass is flight muscle, and that muscle would have to be fast and glycolytic, which rules out sustained flight.

## 5. What this does NOT establish

- **It does not establish that zebrafish fast muscle cannot sustain flight in principle.** It establishes that no *measured* fish muscle I retrieved delivers aerobic power at the level computed for flight. Search scope: about six web searches (Altringham/Johnston sculpin work loops; zebrafish work loops; quail pectoralis; skipjack red muscle; Ellington's limits; the Mead 2020 abstract) and one full-text read (Mead 2020, via PMC). I made **no** search of databases (Web of Science, Scopus) and no systematic review of teleost work-loop data. The Journal of Experimental Biology publisher site is blocked from this session, so most JEB values are search-summary only.
- **No adult zebrafish work-loop measurement was found.** The only zebrafish value is from 5-day larvae. Adult muscle may differ in either direction. The cod data show power falling as body size rises (Anderson & Johnston), which is suggestive but untested for zebrafish.
- **No zebrafish pectoral-fin muscle mass fraction was found** (`unknown`). I did not search for it specifically. The answer depends on it most strongly.
- **No fish muscle measurement exists at the ~20 Hz design frequency** in what I retrieved, and none under a flight-like strain and phase regime. Work-loop power depends strongly on strain amplitude and stimulus phase, so values optimised for swimming may not transfer.
- **The requirement is a lower-bound style estimate.** It uses momentum theory with the full disc, generous profile multipliers, perfect elastic storage and no inertial cost, and it is a hover estimate. Forward flight could be cheaper. Take-off and climb would be dearer. Ground (water-surface) effect and a gliding-assisted gait were not modelled.
- **The skipjack 79–133 W/kg figure is unresolved.** If it is aerobic red muscle at a realistic temperature, the sustained "no" weakens substantially (see §6).
- **This file says nothing about metabolic supply** (oxygen delivery, mitochondrial density, heat), fatigue time courses, or whether the required power could be delivered by tendon/elastic or asynchronous-like mechanisms. Those belong to other subproblems or remain open.
- **The flier comparison values (quail, hummingbird, insects) are search-summary or secondary readings.** I used them only as calibration, not as evidence about fish.
- **No calculation here has been checked against a simulation or a measured fish flier.**

## 6. What would change the answer

- **A measured cycle-averaged power of ≥ ~35 W/kg from fish *aerobic* (red) muscle**, under sustainable stimulation at 15–30 Hz and ≥ 25 °C, would refute the sustained "no" for the most generous design. A value ≥ ~100 W/kg would refute it for the realistic designs. The skipjack 79–133 W/kg report is the first thing to check: read Syme & Shadwick 2002 in full, and the SICB abstract.
- **An adult zebrafish fast-muscle work-loop measurement at ~20 Hz and 28 °C.** This would replace the larval proxy and the Q₁₀ extrapolation.
- **A measured pectoral-girdle muscle mass fraction for zebrafish**, and an S-level design that raises it towards 0.2–0.3 of body mass. Together these decide the burst case.
- **Larger wings or lower wing loading from S1/S2.** Doubling R cuts the induced power by 2× (P_ind ∝ 1/R). A design that is mostly gliding, with intermittent flapping, would turn the comparison into a burst-power question, which fast muscle can answer.
- **Fixing the flight mode.** A computed forward-flight minimum power, once S1/S2 fix the wing and the speed, would replace the hover numbers used here.

---

### Sources (with read-levels)
- Mead AF, Kennedy GG, Palmer BM, Ebert AM, Warshaw DM (2020) Mechanical characteristics of ultrafast zebrafish larval swimming muscles. *Biophys J* 119:806–820. https://pmc.ncbi.nlm.nih.gov/articles/PMC7451861/ — full-text (partial, via an automated summarising fetch)
- Altringham JD, Johnston IA. Power output of fish muscle fibres performing oscillatory work: effects of acute and seasonal temperature change. *J Exp Biol* 157:409. https://cob.silverchair.com/jeb/article/157/1/409/6208/ — search-summary; could-not-access the full text (host blocked)
- Syme DA, Shadwick RE (2002) *J Exp Biol* 205:189 (skipjack red muscle). https://www.sciencegate.app/document/10.1242/jeb.205.2.189 — search-summary
- SICB conference abstract, skipjack anterior vs posterior power. https://sicb.org/?p=37437 — search-summary
- Askew GN, Marsh RL (2001) *J Exp Biol* 204:3587. https://cob.silverchair.com/jeb/article-split/204/21/3587/32912/ — search-summary
- Askew GN, Marsh RL, Ellington CP (2001) *J Exp Biol* 204:3601 — search-summary
- Johnston IA, van Leeuwen JL (1995), sculpin escape-response instantaneous power — search-summary
- Johnson & Johnston (1991); Anderson & Johnston (year unknown), cod — search-summary
- Hummingbird hover power, *Nature* 377:722 (1995). https://www.nature.com/articles/377722a0 — search-summary
- Theoretical muscle-power limits, as listed in https://arxiv.org/pdf/2510.02819 — search-summary (secondary)

```swarm-result
{"subproblem": "S10", "evidence": "derived",
  "answer": "Sustained flapping is not supported: measured fish aerobic (red/slow) muscle gives 5-10 W/kg, below the computed hover requirement of at least ~34 W/kg flight muscle even in the most generous case; burst flapping is within reach of warm fast muscle (134 W/kg measured in larval zebrafish) only if roughly 10-30% of body mass were pectoral flight muscle.",
  "key_number": "~34 W/kg flight muscle required (most generous computed hover case) vs 5-10 W/kg measured for sustained fish red/slow muscle",
  "blocked_on": "Full texts of JEB work-loop papers (publisher host blocked); no adult zebrafish work-loop data, no measurement at ~20 Hz, no zebrafish pectoral muscle mass fraction; skipjack red-muscle values (8.8 vs 79-133 W/kg) unresolved; S1/S2 wing geometry not yet fixed"}
```
