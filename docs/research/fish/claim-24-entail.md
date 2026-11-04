# Claim 24: what it requires at the organ and behaviour scales, and whether those requirements hold

**Source claim.** Claim 24, organism scale, evidence level *derived*:

> Current best evidence: required takeoff 4.37 m/s against a measured burst of 0.842 m/s is a 5.2x speed
> and 27x kinetic-energy deficit. Both corrections tonight were favourable and the conclusion survives both.

Written 2026-11-04, branch `claude/claim-24-entail-r0tm61`.

## 0. Which animal the claim is about

The subject is a **designed adult zebrafish, *Danio rerio***. I established this from `replicate-24.md`
(branch `origin/claude/fish-replicate-24-4dc5w4`, read in full this session), which reconstructs both
numbers:

- **4.37 m/s** is a *calculated* stall airspeed, V = √(2mg / (ρ·S·C_L,max)).
  - Inputs: m = 0.4 g, wing span 1 BL = 4 cm, AR 5 (S = 3.2 cm², chord 8 mm), ρ = 1.2 kg/m³, C_L,max = 1.07.
  - The mass and wing are design premises from `zebrafish-glide-physics.md`, not measurements of an animal.
  - The 1.07 is a **dragonfly** value (Wakeling & Ellington 1997, *J Exp Biol* 200:543), applied to a fin
    membrane by inference. This was "correction 1", from 0.6.
- **0.842 m/s** is *derived*, not printed in any paper: U = Re·ν/L = 27,800 × 1.0×10⁻⁶ / 0.033 m.
  - The Re is the mean maximum Re of adult *D. rerio* escapes in Danos & Lauder 2012 (*J Exp Biol*
    215:1854), as relayed by the project document S21.
  - This was "correction 2", replacing a U_crit of 0.548 m/s.

So every behaviour-scale check below has to be about **adult *Danio rerio***. A flying-fish (Exocoetidae)
number cannot refute anything here.

**Prior work I used, and how far.**
- `challenge-24.md` (branch `origin/claude/challenge-takeoff-speed-claim-bsocad`, read in full) raised the
  still-air and surface-taxi conditions.
- A parallel attempt at this same task, `claim-24-entail.md` on branch `origin/claude/claim-24-entail-yi97fa`,
  is unmerged. I read it in full.
  - **Re-checked myself this session:** Demesmay 2025, Danos & Lauder 2012 (abstract) and Miln 2021.
  - **Taken from it as relayed, not re-checked:** the S32/S32-D taxi simulation figures and the Widrick 2018
    flume values.
  - The 40-ms average-speed argument in B1 is new here.

**Labels used in every sentence that needs one.**
- *measured*: reported by the cited authors from experiments.
- *calculated*: my arithmetic. It is not an observation.
- *simulated*: a project model output. It is not an observation.
- *author's claim* and *my inference* are kept apart within each sentence.

## Sources and read-levels

| Source | Animal | Read-level (this session) |
|---|---|---|
| Demesmay L … Allard B 2025, *PLoS Biol* 23(11):e3003484, doi 10.1371/journal.pbio.3003484, PMC12604801 | adult *D. rerio*, 4–12 months, body length 2.6 ± 0.2 to 3.6 ± 0.2 cm | **full-text** (Europe PMC full-text XML; quotes below are verbatim) |
| Danos N & Lauder GV 2012, *J Exp Biol* 215:1854, doi 10.1242/jeb.068957 | adult *D. rerio* | **abstract** (Europe PMC; not in PMC, `inEPMC = N`). The abstract gives no Re and no velocity; the Re 27,800 is relayed from S21 |
| Miln C, Ward AJW, Seebacher F 2021, *R Soc Open Sci* 8:210146, PMC8025299 | adult *D. rerio* | **full-text** for methods (escapes at 120 frames/s, best of 4). The article text gives **no** escape-speed number. The ~0.45–1.38 m/s values are S21-D's digitisation of Fig. 1a, which I did not check |
| Ravel G et al. 2025, *iScience*, doi 10.1016/j.isci.2025.112056, PMC11930232 | *D. rerio* **larvae** | **listing** (title, this session); abstract relayed by the parallel attempt |
| Wakeling JM & Johnston IA 1998, *J Exp Biol* 201:1505 | six marine teleosts, **no *Danio*** | relayed from the parallel attempt (abstract-level there); **not read by me** |
| Wakeling JM & Ellington CP 1997, *J Exp Biol* 200:543 | dragonflies | **search-summary**, relayed via replicate-24 |
| Park H & Choi H 2010, *J Exp Biol* 213:3269 | *Cypselurus hiraii* model (Exocoetidae) | relayed (abstract-level in the parallel attempt); **not read by me** |
| S32 / S32-D project documents | designed zebrafish and exocoetid, both **simulated** | relayed via the parallel attempt; **not read by me** |

---

## Behaviour scale

### B1 (range). The adult animal's maximal attainable escape speed must not exceed ≈ 0.91 m/s. **UNSATISFIABLE**

**Why the claim requires it.**
- The claim calls 0.842 m/s *the* measured burst and builds 5.2× = 4.37 / 0.842 on it.
- That treats 0.842 m/s as the top of what the animal can do in a burst.
- I set the bound at the top of replicate-24's ±1 s.e.m. band on the Danos & Lauder Re: **hi = 0.91 m/s**.
  At that bound the ratio is already 4.80× (calculated).
- An upper bound on *attainable* speed has a logical asymmetry:
  - a lower same-species measurement does not establish it;
  - a higher same-species measurement breaks it.

**The animal on each side.**
- **The claim:** adult *D. rerio*. The scenario fish is 4 cm; the input comes from 33 mm TL adults.
- **The measurement:** adult *D. rerio* wild-type controls (scn4aa⁺/⁺; scn4ab⁺/⁺ siblings), 4–12 months old.
- Same species, same life stage, same behaviour (a startle-evoked escape). **No number in this section
  comes from a flying fish.**
- The measured fish (2.6–3.6 cm) are, if anything, *smaller* than the 4 cm scenario fish. My inference is
  that a larger fish would be faster in absolute terms, which moves the result further from the bound.

**Measured (Demesmay 2025, full-text, verbatim).**
- "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants) and latency to
  attain maximal speed (8 ± 4 ms for controls and 9 ± 3 ms for mutants) were not different. Distance covered
  in 40 ms from the escape response start was also not altered … (3.8 ± 0.8 cm for controls and 3.8 ± 0.9
  cm for mutants)."
- Methods: escapes recorded "at … 240 frames/s (escape response, 1 s long videos)". The stimulus was "Two
  similar objects (1 g) placed at approximately 30 cm above the water … simultaneously dropped into two
  adjacent tanks (1.6 L)". Tracking used "Fiji software (angle tool and manual tracking plugin)".
- Statistics: "Graphs represent mean ± SD", "minimum of 11 per genotype".

**Two independent reads of the same dataset, both contradicting the bound (calculated).**
1. **Peak speed.**
   - The control mean of 1.57 m/s is 1.73× the 0.91 bound.
   - The bound lies (1.57 − 0.91)/0.27 = 2.4 SD below the control mean.
2. **Average over the first 40 ms.** This is new here and is robust to the sampling objection that applies
   to the peak.
   - 3.8 cm / 0.040 s = **0.95 m/s**.
   - It is a ~10-frame displacement, not a 2-frame finite difference.
   - The window includes the C-bend (stage 1, about 13 ms to maximal head turn), during which the centre of
     mass moves little.
   - A maximum cannot be below the mean over the same interval. So even this conservative figure puts the
     average fish's peak above 0.91 m/s.
   - The margin is small (0.95 vs 0.91), so I rest the verdict mainly on read 1 and use read 2 as a floor.

**A caveat on the peak, which is my inference.** The peak is reached in 8 ± 4 ms, which is about 2 frames at
240 frames/s. A finite-difference peak from manual tracking at that rate is noisy and could read high. That
objection does not apply to read 2.

**Disagreement, kept as it is.** These sources measure different things. I do not average them.

| Source (all adult *D. rerio*) | Quantity | Value | Read-level |
|---|---|---|---|
| Danos & Lauder 2012 via S21 | max centre-of-mass velocity, as Re; 1000 frames/s, n = 5 | 0.842 m/s (*derived* from Re 27,800 ± 2,140 s.e.m.) | abstract + relay |
| Demesmay 2025 | maximal escape speed; 240 frames/s, ≥ 11 per group | 1.57 ± 0.27 m/s (SD) | full-text |
| Demesmay 2025 | mean speed over 40 ms (calculated from the measured distance) | 0.95 ± 0.20 m/s | full-text |
| Miln 2021 via S21-D digitisation | best of 4 escapes per fish; 120 frames/s | ~0.45–1.38 m/s | text read, numbers relayed |

- The Danos & Lauder abstract confirms that their quantity is "maximum velocity of the center of mass". So
  the two sources measure the same thing with different equipment and samples.
- Danos & Lauder used a smaller sample (n = 5) and a higher frame rate. Demesmay used a lower frame rate and
  manual tracking.
- I cannot say which value is closer to the truth. For an *upper bound on attainable speed*, only the higher
  one matters.

**Verdict.**
- The constraint the 5.2× figure needs is contradicted by a measured value for the same species and the same
  behaviour. **"5.2× speed / 27× KE" and "a measured burst of 0.842 m/s" are refuted from below.**
- Corrected by the claim's own method (calculated):
  - 4.37 / 1.57 = **2.78× speed** and **7.7× KE** against the control mean;
  - 2.38× and 5.6× against mean + 1 SD.
- **This does not refute** the conclusion that a deficit exists (deficit > 1); see B2.
- **It does contradict** "both corrections were favourable … the conclusion survives both" as a summary of
  the evidence. A third correction, from a better-sampled same-species source, also moves toward
  feasibility and roughly halves the deficit again.

### B2 (range). Every measured adult locomotor speed must stay below the required take-off airspeed, v < 4.37 m/s. **SATISFIED**

**The animal on each side.** Adult *D. rerio* for the claim and for every number used here.

**Measured.**
- Demesmay 2025 escape maxima: controls 1.57 ± 0.27 m/s, mutants 1.61 ± 0.33 m/s.
- Miln 2021 per-fish maxima: up to ~1.38 m/s (S21-D's digitisation, relayed).

**Calculated.**
- 4.37 m/s lies (4.37 − 1.57)/0.27 = **10.4 SD** above the control mean, assuming normality.
- Mean + 3 SD is 2.38 m/s, which is 54 % of 4.37 m/s.

**Scope.**
- I did not read Demesmay's S1 Data per-fish values, so an individual outlier is unreported rather than
  excluded.
- My Europe PMC search (below) found no other adult *Danio* escape-speed measurement that could approach
  4.37 m/s.

### B3 (range). The animal's top speed at the air–water interface must not exceed its submerged burst speed (ratio ≤ 1). **UNSATISFIED: nobody appears to have looked in *Danio***

**Why the claim requires it.**
- The claim divides an airspeed by a speed through water.
- That holds only if the animal has no surface mode that beats its submerged burst, such as taxiing with the
  body partly out of the water.
- Challenge-24 raised this, together with a separate unstated **still-air** condition. A headwind adds
  directly to airspeed; challenge-24 calculates that a 3.53 m/s headwind closes the gap. I do not repeat
  that here.

**The animal on each side.**
- **The claim:** adult *D. rerio*.
- **The only measured evidence that surface taxiing beats underwater speed:** flying fish (Exocoetidae).
  **That is the wrong animal, and I do not use it for a verdict.**
- The project's own S32 reportedly reproduces an exocoetid taxi with the same equations. It fails for the
  zebrafish only through Reynolds-dependent drag on the caudal lobe. So an exocoetid taxi measurement
  *confirms* that model; it refutes nothing here. That is relayed via the parallel attempt; I did not read
  S32.

**Simulated, not observed (relayed, not re-checked by me).**
- S32 gives a designed-zebrafish taxi ceiling of 2.2–2.9 m/s; S32-D widens it to ≤ 0.9–3.4 m/s.
- Against 2.2–2.9 m/s the deficit would be 1.5–2.0× (calculated on simulated inputs).
- If that model is right, B3 as stated is too strict: the binding speed would be the taxi ceiling, not
  0.842 m/s.

**Search and scope of the negative.**
- My Europe PMC query, `(zebrafish OR "Danio rerio") AND (leap* OR "jumping out" OR "water exit" OR
  "surface skimming" OR "aerial")`, returned 2,519 hits. I inspected the top 30. They covered toxicology,
  stress protocols and shoaling, with **no surface-locomotion speed**.
- The parallel attempt's WebSearch and its 343-hit Europe PMC query (top 25) found none either. That is
  relayed.
- Not searched: Google Scholar, Web of Science, aquarium-husbandry literature.
- No study looked for surface locomotion in adult *Danio* and reported its absence. **This is "nobody
  appears to have looked", not "looked and found nothing".**

---

## Organ scale

### O1 (range). The paired lifting surface must reach a steady C_L,max in air of 0.7–1.15 at chord Re ≈ 2.3×10³. **OPEN**

**Why the claim requires it.**
- 4.37 m/s assumes C_L,max = 1.07.
- The project's corrected band is 0.7–1.15, which gives V = 5.40–4.22 m/s (calculated in replicate-24 and
  challenge-23).
- The *existence* of the deficit is much less sensitive to this than the number. Closing the gap with C_L
  alone would need (calculated):
  - C_L,max ≈ 1.07 × 26.9 ≈ 28.8 against 0.842 m/s;
  - ≈ 1.07 × 7.75 ≈ 8.3 against Demesmay's 1.57 m/s.

**The animal on each side.**
- **The claim:** a zebrafish fin-derived membrane.
- **The evidence:** a dragonfly wing (1.07 and 1.15 at Re ≈ 700–2,400; search-summary, relayed) and a
  flying-fish whole-body model (Park & Choi 2010; no numeric C_L,max in the abstract as relayed).
- Both are cross-species, so they can neither satisfy nor refute the band.

**Search and scope.**
- My Europe PMC query, `("pectoral fin" OR "fin membrane" OR "fin ray") AND ("lift coefficient") AND (air OR
  "wind tunnel")`, returned 9 hits: beetle wings, robotic fish, sharks, a robotic dolphin and reviews.
  **None** measured a fish fin in air.
- This is a shallow search, one database. The negative means "not found", not "shown absent".

### O2 (energetic). The axial fast musculature must already be at or near its maximal power in a maximal escape, so that the measured burst is a physiological ceiling (available/used power ≤ ~1). **OPEN**

**Why the claim requires it.**
- A measured burst is a ceiling only if the propulsive organ is power- or work-limited. It must not be
  limited by stimulus strength, motivation or tank geometry.
- Kinetic energy per unit mass (calculated):
  - 0.35 J/kg at 0.842 m/s;
  - 1.23 J/kg at 1.57 m/s;
  - 9.55 J/kg at 4.37 m/s.
- At the same fast-start duration, the reserve this framing denies is 27× from the claim's baseline, or 7.7×
  from the Demesmay baseline.

**The animal on each side.**
- **Same species, wrong stage:** Ravel et al. 2025 is about *D. rerio* larvae; its title says the escape swim
  "reveals maximum neuromuscular power output". I read the title only; the abstract is relayed.
- **Adult, wrong species:** Wakeling & Johnston 1998, six marine teleosts, no *Danio*. Relayed, not read by
  me.
- **Danos & Lauder 2012 (abstract, read):** maximal power is stated as a *hypothesis*, not a measurement:
  "hypothesized maximal or near-maximal muscle power output".
- Applying any of these to adult *Danio* is my inference, so the constraint stays open.

**A point against the framing, not against the constraint (my inference).** Demesmay's stimulus was a 1 g
object dropped from about 30 cm into a 1.6 L tank. That such a mild stimulus produced 1.57 m/s escapes in
small tanks suggests nothing about a reserve either way. It does show that the Danos & Lauder figure was
not a ceiling.

**Search and scope.**
- My Europe PMC query, `(zebrafish OR "Danio rerio") AND ("work loop" OR "work-loop" OR "muscle power
  output") AND (adult OR "fast muscle")`, returned 18 hits.
  - Zebrafish-relevant hits were **larval** only: PMC7451861 (larval swimming-muscle mechanics) and
    PMC13535098 (larval axial strain).
  - **No adult *Danio* fast-muscle work-loop power was found.**
- The adult white-muscle mass fraction is `unknown`; I found no value.

---

## Search for other adult *Danio* escape speeds (affects B1 and B2)

- Europe PMC query: `(zebrafish OR "Danio rerio") AND ("escape response" OR "fast-start" OR "fast start" OR
  "C-start") AND adult AND (velocity OR speed)`. It returned 555 hits; I listed the top 60.
- I fetched the full text of three candidates and checked them for speed values:
  - **PMC7750966** (2020, looming stimulus): its speeds are stimulus approach speeds, plus a mean escape speed
    of 3.7 cm/s to a live predator. That is not a peak fast-start speed.
  - **PMC12021243** (2025, Na_V1.4): Ucrit flume protocol only.
  - **PMC12180146** (2025, DMD kinematics): larval.
- Result: **no further adult peak escape speed was found** in this search. Demesmay 2025 and Danos & Lauder
  2012 remain the only two adult values I have, and they disagree.

## Summary

| # | Scale | Kind | Status | One line |
|---|---|---|---|---|
| B1 | behaviour | range | **unsatisfiable** | Adult *D. rerio* escape: measured mean peak 1.57 ± 0.27 m/s, and a 40-ms mean of 0.95 m/s calculated from measured distance, both exceed the ≤ 0.91 m/s the 5.2× figure needs. Same species on both sides |
| B2 | behaviour | range | satisfied | All measured adult *Danio* speeds are far below 4.37 m/s (10.4 SD above the mean) |
| B3 | behaviour | range | unsatisfied | No adult *Danio* surface-speed measurement exists; nobody appears to have looked. The exocoetid evidence is the wrong animal |
| O1 | organ | range | open | C_L,max of a fin membrane in air is unmeasured; the proxies are a dragonfly and an exocoetid |
| O2 | organ | energetic | open | Escape power-limitation is shown only in larval *Danio* and in non-*Danio* adults |

**Net effect on claim 24.**
- **Refuted from below:** the specific "5.2× / 27×" and the word "measured" on 0.842 m/s, which is derived
  from Re. The same-species correction is **2.8× / 7.7×** (calculated).
- **Standing:** that a deficit exists, i.e. take-off from a submerged escape is out of reach in still air
  (B2).
- **Not standing:** "survives both corrections" as a description of the evidence trend. Every correction
  identified so far has moved the number toward feasibility:
  - 10.7× → 5.2× (the two named corrections) → 2.8× (Demesmay) → about 1.5–2.0× if the simulated S32 taxi is
    right.
- My inference: the robust content of the claim is "> 1 in still air". The multiple itself is not robust.

```swarm-entail
{"source_claim": 24, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The adult animal's maximal attainable escape (fast-start) speed must not exceed about the claimed burst speed, so that the 5.2x speed and 27x KE ratios hold",
      "quantity": "maximal escape speed of adult Danio rerio", "lo": null, "hi": 0.91, "units": "m/s",
      "status": "unsatisfiable",
      "satisfied_by": "Contradicted by a same-species, same-behaviour measurement: Demesmay et al. 2025, adult Danio rerio wild-type controls (scn4aa+/+;scn4ab+/+, 4-12 months, body length 2.6-3.6 cm), maximal escape speed 157 +/- 27 cm/s (mean +/- SD, >=11 per genotype, 240 frames/s, manual Fiji tracking). Independent floor from the same paper: measured distance 3.8 +/- 0.8 cm in the first 40 ms gives a mean speed of 0.95 m/s (calculated), and a peak cannot be below the mean over the same interval. Corrected by the claim's own method (calculated): 4.37/1.57 = 2.78x speed, 7.7x KE",
      "satisfied_evidence": "measured",
      "note": "Demesmay L et al. 2025 PLoS Biol 23(11):e3003484, doi 10.1371/journal.pbio.3003484, PMC12604801, full-text read this session, quotes verbatim. Animal on both sides: adult Danio rerio (the claim's input is Danos & Lauder 2012 adults, 33 mm TL; the scenario fish is 4 cm). No flying-fish number used. Disagreement preserved, not averaged: Danos & Lauder 2012 J Exp Biol 215:1854 (abstract read; max CoM velocity, 1000 frames/s, n=5) gives 0.842 m/s DERIVED from Re 27,800 relayed by S21. A lower same-species value cannot establish an upper bound that a higher one breaks. Caveat (my inference): the peak is reached in ~2 frames at 240 frames/s and may read high; the 40-ms floor (0.95 m/s) is not subject to that. The qualitative deficit (>1) is not refuted. Search for further adult escape speeds: Europe PMC 555 hits, top 60 listed, 3 full texts checked (PMC7750966, PMC12021243, PMC12180146); none gave an adult peak escape speed."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "Every measured locomotor speed of the adult animal must lie below the required take-off airspeed",
      "quantity": "measured adult Danio rerio locomotor speed", "lo": null, "hi": 4.37, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Demesmay 2025 adult escape maxima: controls 1.57 +/- 0.27 m/s, mutants 1.61 +/- 0.33 m/s; 4.37 m/s is 10.4 SD above the control mean (calculated, normality assumed); Miln 2021 per-fish maxima up to ~1.38 m/s (S21-D digitisation, relayed)",
      "satisfied_evidence": "measured",
      "note": "Demesmay 2025 PMC12604801 full-text; Miln C et al. 2021 R Soc Open Sci 8:210146 PMC8025299 full text read for methods (120 frames/s, best of 4), but the speed values are not in the text and are relayed from S21-D. Same species on both sides. Per-fish S1 Data not read, so an individual outlier is unreported rather than excluded."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The animal's top speed at the air-water interface (e.g. surface taxiing with the body partly out of water) must not exceed its submerged burst speed, so that the submerged burst is the binding speed",
      "quantity": "ratio of maximal surface-locomotion speed to submerged burst speed, adult Danio rerio", "lo": null, "hi": 1.0, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "No measured adult Danio surface-locomotion speed found. The only measured evidence of taxi speeds exceeding underwater speeds is from Exocoetidae (wrong animal, not used for a verdict). Project simulation S32/S32-D (simulated, relayed, not read by me) predicts a designed-zebrafish taxi above the burst but stalling at 2.2-2.9 m/s, which would make this constraint too strict and the binding deficit ~1.5-2.0x (calculated on simulated inputs)",
      "satisfied_evidence": "unknown",
      "note": "My search: Europe PMC '(zebrafish OR \"Danio rerio\") AND (leap* OR \"jumping out\" OR \"water exit\" OR \"surface skimming\" OR \"aerial\")', 2519 hits, top 30 inspected, none relevant. The parallel attempt (branch claude/claim-24-entail-yi97fa) ran a WebSearch and a 343-hit Europe PMC query (top 25) with the same null result (relayed). Not searched: Google Scholar, Web of Science, husbandry literature. No study looked and reported absence: 'nobody appears to have looked', not 'looked and found nothing'. The still-air condition (a headwind adds to airspeed) is a separate unstated premise, covered in challenge-24."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The paired lifting surface must reach a steady maximum lift coefficient in air within the corrected band at its chord Reynolds number (~2.3e3)",
      "quantity": "steady C_L,max of a fin-membrane lifting surface in air at Re ~2.3e3", "lo": 0.7, "hi": 1.15, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No fish-fin measurement in air found. The proxies are other animals: dragonfly wings 1.07/1.15 at Re ~700-2400 (Wakeling & Ellington 1997, search-summary, relayed); a flying-fish (Cypselurus hiraii) whole-body model (Park & Choi 2010, relayed, no numeric C_L,max in the abstract). Closing the deficit by C_L alone would need ~28.8 (vs 0.842 m/s) or ~8.3 (vs 1.57 m/s), calculated",
      "satisfied_evidence": "literature",
      "note": "Cross-species on the evidence side (insect, exocoetid), so open, not satisfied or refuted. My search: Europe PMC '(\"pectoral fin\" OR \"fin membrane\" OR \"fin ray\") AND (\"lift coefficient\") AND (air OR \"wind tunnel\")', 9 hits, none a fish fin in air. Shallow, single-database scope: 'not found', not 'shown absent'."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The propulsive axial musculature must already deliver near its maximal power in a maximal escape, so that the measured burst is a physiological ceiling rather than a stimulus- or context-limited value",
      "quantity": "ratio of available to used muscle power in a maximal adult fast-start", "lo": null, "hi": 1.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Supported only off-target: Ravel et al. 2025 (D. rerio larvae; title read, abstract relayed) report escape swims maximize neuromuscular power output; Wakeling & Johnston 1998 (six marine teleosts, no Danio; relayed, not read by me) report in-vivo fast-start power near work-loop maxima. Danos & Lauder 2012 (abstract read) state near-maximal power only as a hypothesis. No adult Danio fast-muscle power measurement found; adult white-muscle mass fraction unknown",
      "satisfied_evidence": "literature",
      "note": "Ravel G et al. 2025 iScience doi 10.1016/j.isci.2025.112056 PMC11930232 (listing). KE per mass calculated: 0.35, 1.23, 9.55 J/kg at 0.842, 1.57, 4.37 m/s. Extending larval or non-Danio results to adult Danio is my inference. My search: Europe PMC '(zebrafish OR \"Danio rerio\") AND (\"work loop\" OR \"work-loop\" OR \"muscle power output\") AND (adult OR \"fast muscle\")', 18 hits; the only zebrafish-relevant hits were larval (PMC7451861, PMC13535098)."}
  ]}
```
