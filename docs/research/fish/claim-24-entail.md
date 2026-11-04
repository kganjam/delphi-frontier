# Claim 24: what it requires at the organ and behaviour scales

**Source claim.** Claim 24. Scale: organism. Evidence: derived.

> Current best evidence: required takeoff 4.37 m/s against a measured burst of 0.842 m/s is a 5.2x speed and
> 27x kinetic-energy deficit. Both corrections tonight were favourable and the conclusion survives both.

**Subject of the claim.** A designed adult zebrafish, *Danio rerio*: 0.4 g body, 4 cm, with a paired lifting
surface of 3.2 cm² (span 1 BL = 4 cm, AR 5). The fish is a design scenario. The mass and wing are assumptions
recorded in `zebrafish-glide-physics.md` (branch `origin/claude/zebrafish-glide-physics-j176og`), as relayed by
`replicate-24.md`. Neither is a measured animal.

**How the two numbers were built** (from `replicate-24.md`, two versions on remote branches, and
`challenge-24.md`, branch `origin/claude/challenge-takeoff-speed-claim-bsocad`; all read in full in this
session):

- **4.37 m/s** is the stall airspeed V = √(2mg / (ρ·S·C_L,max)), with m = 0.4 g, S = 3.2 cm², ρ = 1.2 kg/m³ and
  C_L,max = 1.07.
  - The 1.07 is a dragonfly-wing value: Wakeling & Ellington 1997, *J Exp Biol* 200:543, *Sympetrum
    sanguineum*.
  - It replaced an earlier 0.6. That is "correction 1".
- **0.842 m/s** is U = Re·ν/L from Danos & Lauder 2012 (*J Exp Biol* 215:1854, doi 10.1242/jeb.068957).
  - Inputs: mean maximum Re 27,800 ± 2,140 (s.e.m.), adult TL 33 mm, ν = 1.0×10⁻⁶ m²/s.
  - This is a *derived* fast-start (escape) speed. It is not a printed velocity.
  - It replaced an earlier U_crit of 0.548 m/s. That is "correction 2".
- **Both prior reviewers agree with the arithmetic:** 4.370/0.842 = 5.19 and 5.19² = 26.9. Both also say that
  27× is 5.2× squared, not independent evidence. I do not redo this.

**Labels used in every sentence that needs one:**
- **measured**: reported by the cited authors from experiments.
- **calculated**: arithmetic I did in this session. It is not an observation.
- **simulated**: a project model run. It is not an observation.
- **author's claim / my inference**: kept apart in each sentence where both appear.

## Sources and read-levels

| Source | Animal | Used for | Read-level |
|---|---|---|---|
| Demesmay L, Idoux R, … Allard B 2025, *PLoS Biol* 23(11):e3003484, doi 10.1371/journal.pbio.3003484, PMC12604801 | adult *D. rerio*, 4–12 months, BL 2.6 ± 0.2 to 3.6 ± 0.2 cm | adult maximal escape speed | **full-text** (Europe PMC XML fetched this session; quotes verbatim) |
| Danos N & Lauder GV 2012, *J Exp Biol* 215:1854, doi 10.1242/jeb.068957 | adult *D. rerio* | method behind the 0.842 m/s input | **abstract** (Europe PMC, this session). The abstract has no Re or speed value. The Re 27,800 is relayed from S21 (full-text there; I did not read it) |
| Miln C, Ward AJW & Seebacher F 2021, *R Soc Open Sci* 8:210146, PMC8025299 | adult *D. rerio* | per-fish best-of-4 escape speeds | **relayed**. I did not read it. The values ~0.45–1.38 m/s are S21-D's own digitisation of Fig. 1a (`S21-deepen.md`, commit 9ae82754). Claim-192-entail confirms they are not in the article text |
| Widrick et al. 2018, Table 2 (compiled adult flume U_max 13.0–17.9 SL/s) | adult *D. rerio* | repeated-stroke maximum speed | **relayed** via S32-D (`S32-deepen.md`, commit 4976566b). That doc calls the primaries listing-level. I did not read them |
| Ravel G et al. 2025, *iScience*, doi 10.1016/j.isci.2025.112056, PMC11930232 | *D. rerio* **eleutheroembryos** (larvae), not adults | whether the fast-start is power-limited | **abstract** (this session) |
| Wakeling JM & Johnston IA 1998, *J Exp Biol* 201:1505, doi 10.1242/jeb.201.10.1505 | six marine teleosts, **no *Danio*, no cyprinid** | whether the fast-start is power-limited | **abstract** (this session) |
| Park H & Choi H 2010, *J Exp Biol* 213:3269, doi 10.1242/jeb.046052 | *Cypselurus hiraii* models (Exocoetidae, **not zebrafish**) | lift coefficient of a fish fin in air | **abstract** (this session). Full text **could-not-access**: the journals.biologists.com captcha blocked it, and typeset.io is outside this session's network allow-list |
| Wakeling JM & Ellington CP 1997, *J Exp Biol* 200:543 | dragonflies (insect wings) | C_L,max 1.07 / 1.15 | **search-summary**, relayed via replicate-24. My Europe PMC query did not find the record |
| S32 / S32-D (`S32-organism.md` c1b761eb, `S32-deepen.md` 4976566b) | designed zebrafish (simulated) and exocoetid (simulated) | surface-taxi ceiling | **full-text** (repo docs). Their results are **simulated**, not measured |

---

## Behaviour scale

### B1 (range). The fast-start (escape) peak speed of the adult animal must be ≲ 0.91 m/s. **UNSATISFIABLE**

**What the claim requires.** The ratio 5.2× is 4.37 / U.
- The claim calls U = 0.842 m/s the "measured burst".
- That makes 0.842 m/s the attainable top speed.
- U is a fast-start quantity: S21 converted it from Danos & Lauder's maximum escape Re.
- So for "5.2×" to hold, adult zebrafish must not reach much more than this in an escape.
- I take the bound as the top of replicate-24's own ±1 s.e.m. band: **hi = 0.91 m/s**.
  - At U = 0.91 the ratio is already 4.80× (calculated).

**The animal on each side.**
- **The claim:** adult *Danio rerio*. The scenario fish is 4 cm. The burst input comes from adults of 33 mm TL.
- **Demesmay 2025 (the contradicting measurement):** adult *Danio rerio* control fish (scn4aa⁺/⁺; scn4ab⁺/⁺
  siblings), 4–12 months old, "Body length … 2.6 ± 0.2 cm for 4-month-old and 3.6 ± 0.2 for 12-month-old fish".
- **Same subject on both sides:** same species, life stage, size class and behaviour (startle-evoked escape).
  **No number here comes from a flying fish.**
- If anything, the scenario fish (4 cm) is longer than Demesmay's fish. At constant BL/s it would be faster,
  not slower. That is my inference, assuming length scaling.

**Measurement (Demesmay 2025, full-text, verbatim).**
- Result: "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants) and latency
  to attain maximal speed (8 ± 4 ms for controls and 9 ± 3 ms for mutants) were not different".
- Methods: escape responses recorded "at … 240 frames/s (escape response, 1 s long videos)". "Two similar
  objects (1 g) placed at approximately 30 cm above the water were simultaneously dropped into two adjacent
  tanks (1.6 L) containing controls or mutants (3 or 4 adult fish by tank)". Tracking used Fiji manual
  tracking.
- Statistics: "Graphs represent mean ± SD", with a "minimum of 11 per genotype".

**Why this contradicts the bound (calculated).**
- The control **mean** is 1.57 m/s, which is 1.7× the bound of 0.91.
- The bound sits 2.4 SD below the control mean.
- A second, independent same-species dataset points the same way. S21-D's digitisation of Miln 2021 Fig. 1a
  gives per-fish maxima up to about 1.38 m/s. That is relayed, my read-level is none, and the reading is
  S21-D's, not the authors'.

**Disagreement, kept as it is.** These numbers measure different things. I do not average them.

| Source (all adult *D. rerio*) | Quantity | Value |
|---|---|---|
| Danos & Lauder 2012 via S21 | mean of per-sequence escape peaks; 1000 fps, n = 5; **derived** from Re | 0.842 m/s (0.78–0.91 at ±1 s.e.m.) |
| Miln 2021 via S21-D digitisation | best of 4 escapes per fish; 120 fps, n = 50 | ~0.45–1.38 m/s, bulk ~0.55–1.15 |
| Demesmay 2025 | maximal escape speed; 240 fps, manual tracking, ≥ 11 per group | 1.57 ± 0.27 m/s (SD) |
| Widrick 2018 Table 2 via S32-D | flume U_max, repeated-stroke, stages of seconds to minutes | 0.39–0.54 m/s at 30 mm SL |

**My inferences about the spread (not any paper's claim):**
- An Re built from a mean or centre-of-mass velocity would read lower than a peak.
- 240 fps manual tracking over a peak reached in 8 ± 4 ms could read high.
- Neither bias can be tested without per-frame data.
- The flume U_max is a sustained speed. It is a different quantity and does not support a 0.842 m/s *peak*.

**Verdict.**
- A measured mean in the same species and behaviour exceeds the attainable-speed bound that the 5.2× figure
  needs. **The number "5.2× speed / 27× KE" is refuted from below.**
- Corrected against Demesmay's control mean (calculated): 4.37 / 1.57 = **2.78× speed** and **7.7× KE**.
- Against the control mean + 1 SD (1.84 m/s): 2.38× and 5.6×.
- This is the same correction claim-192-entail made to a sibling claim.
- **What it does not refute:** the qualitative conclusion that take-off is out of reach. See B2.
- **It does contradict "both corrections were favourable … survives both" as an evidence statement.** A third,
  better-measured correction is also favourable to flight, and it halves the deficit again.

### B2 (range). Every measured adult speed must stay below the required take-off airspeed: v < 4.37 m/s. **SATISFIED**

**The animal on each side.** Adult *D. rerio* for the claim and for every measurement used.

**Measured.** Demesmay control mean 1.57 ± 0.27 m/s; mutants 1.61 ± 0.33 m/s.

**Calculated.**
- 4.37 m/s is (4.37 − 1.57)/0.27 = **10.4 SD** above the control mean. This assumes normality.
- The mean + 3 SD (2.38 m/s) is 54 % of 4.37 m/s.
- The highest relayed single-fish value, about 1.38 m/s (Miln, via S21-D), is 32 % of 4.37 m/s.

**Scope.** Three same-species datasets (one read in full by me, two relayed). Demesmay's per-fish S1 Data were not
read, so a single outlier is unreported rather than excluded. Nothing within the reported spread approaches
4.37 m/s.

### B3 (range). Top speed at the air–water interface must not exceed submerged fast-start speed (surface speed / submerged burst ≤ 1). **UNSATISFIED for *Danio*: nobody appears to have measured it**

**What the claim requires.**
- The claim divides an airspeed by a speed through water.
- That holds only if the animal has no mode of surface locomotion that beats its submerged burst.
- One such mode would be taxiing with the body out of the water. Challenge-24 raised this.
- A wind term is a separate unstated condition. Challenge-24 already covers it, so I do not repeat it.

**The animal on each side.**
- **The claim:** adult *D. rerio*.
- **The only measured evidence that surface taxiing beats underwater speed:** flying fish (Exocoetidae).
  - Challenge-24 found it at search-summary level.
  - An APS DFD 2013 listing reports juvenile flying fish at 5 g and gliding speeds "an order of magnitude higher
    than their steady swimming speed". That is search-summary this session.
- **That is the wrong animal.** I do not use it for a verdict on zebrafish.

**Project simulation (not an observation).** S32 is simulated, using a measured flapping-foil thrust law
(Floryan et al. 2017, relayed).
- It puts a *designed zebrafish* taxi ceiling at 2.2–2.9 m/s. S32-D widens that to ≤ 0.9–3.4 m/s.
- So in this model the surface speed **can** exceed the submerged burst, but stalls below 4.37/4.41 m/s.
- The same equations reproduce an exocoetid taxi above glide speed. They fail for the zebrafish only through
  the Reynolds-dependent drag on the caudal lobe.
- **Consequence:** an exocoetid taxi measurement would be consistent with the project's own model. It is no
  refutation of anything here.

**My inference.**
- If S32 is right, B3 as stated (ratio ≤ 1) is **too strict**: the surface speed can exceed the burst.
- In that case claim 24's 0.842 m/s is not the binding speed. The binding quantity becomes S32's taxi ceiling,
  2.2–2.9 m/s (simulated).
- That gives a deficit of 4.37 / 2.9 to 4.37 / 2.2 = **1.5–2.0×** (calculated on simulated inputs).
- This is smaller than 5.2× but still greater than 1.

**Search and scope.**
- WebSearch: "zebrafish surface swimming air-water interface skimming jumping out of water adult behavior
  speed". Hits: larval surfacing to fill the swim bladder (lateral-line paper), a swim-mill U_crit protocol,
  the upside-down catfish *Synodontis* (near-surface drag ~2× submerged), and flying fish. **No adult *Danio*
  surface-locomotion speed.**
- Europe PMC: `(zebrafish OR "Danio rerio") AND ("air-water interface" OR "water surface") AND (swimming OR
  jump*) AND adult`. 343 hits; I inspected the top 25. They are toxicology, anxiety (novel-tank) and larval
  papers, with **no surface-speed measurement**.
- Claim-192-entail's searches for water-exit leaps also found only terrestrial (substrate) jumping (Bai et al.
  2026, abstract).
- Not searched: Google Scholar, Web of Science, aquarium-husbandry literature.
- I found no study that *looked* for surface taxiing in *Danio* and reported its absence. **This is "nobody
  appears to have looked", not "looked and found nothing".**

---

## Organ scale

### O1 (range). The lifting surface's steady C_L,max in air at chord Re ≈ 2.3×10³ must lie in [0.7, 1.15]. **OPEN**

**What the claim requires.**
- 4.37 m/s uses C_L,max = 1.07.
- Challenge-23's corrected band is 0.7–1.15, which gives V = 5.40–4.22 m/s (calculated in replicate-24).
- The *conclusion* (deficit > 1) is far less sensitive than the number. Closing the gap with C_L alone needs
  C_L,max ≈ 1.07 × 26.9 = **28.8** against the 0.842 m/s burst, or 1.07 × 7.75 = **8.3** against Demesmay's
  1.57 m/s (calculated).
  - My inference: no steady-wing value in the sources here comes near either figure. Neither does any I know of.
- The organ-scale requirement is therefore the band itself: a fin-type membrane in air must reach 0.7–1.15 at
  this Re.

**The animal on each side.**
- **The claim:** a zebrafish fin-derived membrane at Re ≈ 2,300. That Re is replicate-24's calculation, with
  chord 8 mm and ν_air = 1.5×10⁻⁵ m²/s.
- **Wakeling & Ellington 1997:** **dragonfly** wings, 1.07 and 1.15 at Re ≈ 700–2,400. Insect, not fish. Read
  at search-summary only (relayed).
- **Park & Choi 2010:** a **flying-fish** model (*Cypselurus hiraii*), whole-animal, in a wind tunnel. The
  abstract says "the lift coefficient is largest at attack angles around 30∼35 deg". It gives no numeric
  C_L,max and no Re in the abstract. A 2019 CFD paper reportedly gives 1.03 for that model; that is a
  search-summary of a **simulation**, not used.

**Why open.**
- No measurement of a zebrafish (or any small teleost) fin membrane in air was found.
- The two numbers nearest to it come from an insect and from an exocoetid at a different, unreported Re.
- Neither can satisfy or refute the band for this animal.

**Search scope.**
- One WebSearch for Park & Choi C_L,max.
- A Europe PMC query for Wakeling & Ellington 1997 (record not found).
- The repo chain (challenge-23, replicate-5, replicate-24).
- I did not run a search specifically for "teleost fin aerodynamics in air". The negative for zebrafish fins is
  "not found in a shallow search".

### O2 (energetic). The axial fast muscle must already deliver near its maximal power in a maximal escape, with no reserve of ≈ 7.7–27× in kinetic energy per stroke. **OPEN**

**What the claim requires.** Calling 0.842 m/s, or any measured burst, a ceiling is physical only if the
propulsive organ is power- or work-limited. It must not be limited by stimulus, motivation or tank geometry.
- Kinetic energy per unit body mass (calculated): 0.35 J/kg at 0.842 m/s; 1.23 J/kg at 1.57 m/s; 9.55 J/kg at
  4.37 m/s.
- At fixed fast-start duration, the required reserve is therefore 27× (claim's baseline) or 7.7× (Demesmay
  baseline).
- **Ceiling on the bound (hi):** I set hi = 1.0. The muscle must be at or near its limit. A ratio of
  available to used power ≥ 7.7 would falsify the claim's framing.

**The animal on each side.**
- **The claim:** adult *D. rerio*.
- **Ravel et al. 2025 (abstract):** *D. rerio* **eleutheroembryos**. Same species, wrong life stage. Author's
  claim: "Eleutheroembryos maximize neuromuscular power output during the fast-start escape response."
- **Wakeling & Johnston 1998 (abstract):** six marine teleosts, no *Danio*. Author's claim: "the predicted mean
  muscle-mass-specific power outputs, as calculated from swimming sequences, were similar to the muscle power
  outputs measured from work-loop experiments". *Scorpaena notata* fast fibres gave 142.7 W/kg at 20 °C.
- **Danos & Lauder 2012 (abstract)** describe escape responses as a model behaviour "in which hypothesized
  maximal or near-maximal muscle power output is used". **Note:** that is stated as a *hypothesis*, not a
  measurement.

**Why open, not satisfied.**
- Two lines of evidence support the constraint. One is the same species at the larval stage; the other is
  adults of other species.
- Applying either to adult *Danio* is **my inference**.
- The repo's surface-taxi work (S30, S32) also argues the KE framing is the wrong constraint, because launch
  can integrate many strokes. On that reading, the 27× figure does not need a single-stroke reserve at all.

**Search scope.**
- Europe PMC: `(zebrafish OR "Danio rerio") AND ("work loop" OR "muscle power") AND adult`. 86 hits; I
  inspected the top 25. No adult *Danio* fast-muscle work-loop power was found. The relevant hits were larval
  (Ravel 2025; a 2026 larval axial-strain paper).
- The adult white-muscle mass fraction is **unknown**; I found no value.

---

## Summary

| # | Scale | Kind | Status | One line |
|---|---|---|---|---|
| B1 | behaviour | range | **unsatisfiable** | Same-species measured mean escape speed of 1.57 ± 0.27 m/s (Demesmay 2025, adult *D. rerio*) exceeds the ≤ 0.91 m/s the 5.2× figure needs. Corrected (calculated): 2.78× speed, 7.7× KE |
| B2 | behaviour | range | satisfied | All measured adult *Danio* speeds are far below 4.37 m/s (10.4 SD above Demesmay's control mean) |
| B3 | behaviour | range | unsatisfied | No adult *Danio* surface-locomotion speed exists. Nobody appears to have looked. S32 (simulated) says the taxi exceeds the burst but stalls at 2.2–2.9 m/s |
| O1 | organ | range | open | C_L,max of a fin membrane in air is unmeasured. The proxies are a dragonfly (1.07/1.15) and an exocoetid (no number in abstract) |
| O2 | organ | energetic | open | Fast-start is power-limited in *Danio* larvae and in six marine adult teleosts, but untested in adult *Danio* |

**Net effect on claim 24.**
- **Refuted from below:** the figures "5.2× speed / 27× kinetic energy" and the phrase "measured burst of
  0.842 m/s".
  - The input is derived from Re.
  - A better-resolved, same-species measured mean is 1.87× higher.
  - The deficit by the claim's own method is **2.8× / 7.7×** (calculated).
- **Standing:** the qualitative conclusion. Take-off from a submerged escape is out of reach (B2). It stays out
  of reach under the project's own simulated surface taxi (1.5–2.0×, B3), though by a much smaller margin.
- **Not standing:** "survives both corrections" as a description of the evidence trend.
  - Every correction so far has moved the number toward feasibility: C_L 0.6 → 1.07, then U_crit → burst,
    then Danos & Lauder → Demesmay, then submerged → taxi.
  - The headline has fallen 10.7× → 5.2× → 2.8× → ~1.5–2.0× (simulated).
  - My inference: the robust part of the claim is "> 1". The specific multiple is not robust.

```swarm-entail
{"source_claim": 24, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The fast-start (escape) peak speed attainable by the adult animal must not exceed about the claimed burst speed, so that v_to/v_burst = 5.2x and its square 27x hold",
      "quantity": "maximal escape (fast-start) speed of adult Danio rerio", "lo": null, "hi": 0.91, "units": "m/s",
      "status": "unsatisfiable",
      "satisfied_by": "Contradicted by a same-species, same-behaviour measurement: Demesmay et al. 2025 adult Danio rerio controls (scn4aa+/+;scn4ab+/+ siblings, 4-12 months, BL 2.6-3.6 cm) maximal escape speed 157 +/- 27 cm/s (mean +/- SD, >=11 per genotype, 240 fps, manual tracking). Population MEAN is 1.7x the bound. Corrected by the claim's own method (calculated): 4.37/1.57 = 2.78x speed, 7.7x KE",
      "satisfied_evidence": "measured",
      "note": "Demesmay L et al. 2025 PLoS Biol 23(11):e3003484, PMC12604801, full-text read this session. Animal on both sides: adult Danio rerio (claim input is Danos & Lauder 2012 adult D. rerio, 33 mm TL; claim scenario fish 4 cm). Not a flying-fish number. Disagreement preserved: Danos & Lauder 2012 J Exp Biol 215:1854 via S21, 0.842 m/s DERIVED from mean max Re 27,800 (1000 fps, n=5; abstract read, Re relayed); Miln et al. 2021 per-fish best-of-4 ~0.45-1.38 m/s (S21-D digitisation of Fig 1a, relayed, not read by me); Widrick 2018 flume U_max 0.39-0.54 m/s is a sustained-speed quantity (relayed via S32-D). My inference only: Re-from-mean would read low, 240 fps manual peak tracking could read high; untestable without per-frame data. Qualitative deficit (>1) not refuted."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "Every measured locomotor speed of the adult animal must lie below the required take-off airspeed",
      "quantity": "attainable adult Danio rerio locomotor speed", "lo": null, "hi": 4.37, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Demesmay 2025 adult control maximal escape speed 1.57 +/- 0.27 m/s (mutants 1.61 +/- 0.33); 4.37 m/s is 10.4 SD above the control mean and mean+3SD = 2.38 m/s (calculated, normality assumed); highest relayed single-fish value ~1.38 m/s (Miln 2021 via S21-D)",
      "satisfied_evidence": "measured",
      "note": "Demesmay et al. 2025 PMC12604801 full-text; Miln 2021 relayed. Same species on both sides. Scope: three same-species datasets; Demesmay per-fish S1 Data not read, so an individual outlier is unreported rather than excluded."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The animal's top speed at the air-water interface (e.g. by surface taxiing with the body out of water) must not exceed its submerged fast-start speed, so that a submerged burst is the binding speed",
      "quantity": "ratio of maximal surface-locomotion speed to submerged fast-start speed, adult Danio", "lo": null, "hi": 1.0, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "No measured adult Danio surface-locomotion or taxi speed found. Only cross-species measured evidence (Exocoetidae taxi exceeding underwater speed; APS DFD 2013 listing, search-summary) -- wrong animal, not used for a verdict. Project simulation S32/S32-D (simulated, not observed) predicts the designed zebrafish taxi DOES exceed the burst but stalls at 2.2-2.9 m/s (widened to <=0.9-3.4 m/s), i.e. the constraint is likely too strict and the binding deficit would be ~1.5-2.0x (calculated on simulated inputs)",
      "satisfied_evidence": "unknown",
      "note": "Searches: WebSearch 'zebrafish surface swimming air-water interface skimming jumping out of water adult behavior speed' (larval surfacing, swim-mill protocol, Synodontis catfish, flying fish -- no adult Danio surface speed); Europe PMC '(zebrafish OR \"Danio rerio\") AND (\"air-water interface\" OR \"water surface\") AND (swimming OR jump*) AND adult' 343 hits, top 25 inspected, none relevant; claim-192-entail found only terrestrial jumping (Bai 2026). No Google Scholar/Web of Science. No study looked and failed: 'nobody appears to have looked', not 'looked and found nothing'. S32 reproduces exocoetid taxi, so an exocoetid measurement would confirm the model, not refute anything here."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The paired lifting surface must reach a steady maximum lift coefficient in air within the corrected band at its chord Reynolds number (~2.3e3)",
      "quantity": "steady C_L,max of a fin-membrane lifting surface in air at Re ~2.3e3", "lo": 0.7, "hi": 1.15, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No fish-fin measurement at this Re found. Proxies are other animals: dragonfly wings 1.07/1.15 at Re ~700-2,400 (Wakeling & Ellington 1997, insect, search-summary relayed); flying-fish (Cypselurus hiraii) whole-model wind tunnel, lift largest at 30-35 deg, no numeric C_L,max or Re in abstract (Park & Choi 2010). Closing the deficit by C_L alone needs C_L,max ~28.8 (vs 0.842 m/s) or ~8.3 (vs 1.57 m/s), calculated",
      "satisfied_evidence": "literature",
      "note": "Park H & Choi H 2010 J Exp Biol 213:3269 doi 10.1242/jeb.046052, abstract (full text could-not-access: journals.biologists.com captcha; typeset.io outside network allow-list). Wakeling & Ellington 1997 J Exp Biol 200:543 search-summary via replicate-24; not found in Europe PMC. Animals: claim = zebrafish fin membrane; evidence = insect and exocoetid, so cross-species, open. Shallow scope: one WebSearch, one Europe PMC query, repo chain (challenge-23, replicate-5, replicate-24)."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The propulsive axial musculature must already deliver near its maximal power in a maximal escape, with no ~7.7-27x reserve in kinetic energy per stroke, so that the measured burst is a physiological ceiling",
      "quantity": "ratio of available to used muscle-mass-specific power in a maximal adult fast-start", "lo": null, "hi": 1.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Supported only off-target: Ravel et al. 2025 (D. rerio eleutheroembryos, larval stage) report escape swims maximize neuromuscular power output; Wakeling & Johnston 1998 (six marine teleosts, no Danio) find in-vivo fast-start power ~ work-loop maxima (Scorpaena notata fast fibres 142.7 W/kg, 20 C). Danos & Lauder 2012 state near-maximal power only as a hypothesis. No adult Danio fast-muscle power measurement found; adult white-muscle mass fraction unknown",
      "satisfied_evidence": "literature",
      "note": "Ravel G et al. 2025 iScience doi 10.1016/j.isci.2025.112056 PMC11930232 abstract; Wakeling JM & Johnston IA 1998 J Exp Biol 201:1505 abstract; Danos & Lauder 2012 abstract. KE/mass calculated 0.35, 1.23, 9.55 J/kg at 0.842, 1.57, 4.37 m/s. Extension to adult Danio is my inference. Search: Europe PMC '(zebrafish OR \"Danio rerio\") AND (\"work loop\" OR \"muscle power\") AND adult' 86 hits, top 25 inspected, only larval relevant. S30/S32 argue multi-stroke launch makes the single-stroke KE framing the wrong constraint."}
  ]}
```
