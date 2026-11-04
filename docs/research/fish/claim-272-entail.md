# Claim 272: what it requires at the organ and behaviour scales, and whether those requirements hold

**Source claim** (organism scale, evidence: derived). Extracted from S32, `docs/research/fish/S32-organism.md` on `origin/claude/s32-multi-stroke-launch-qpq9g2`, §0 and §4.1:

> THE SIZE ARGUMENT RETURNS, CORRECTLY LOCATED. Zebrafish and exocoetids share f·A_pp/V_to at 0.09–0.10. They differ ONLY in lobe C_D at their Reynolds number: 0.06–0.08 at Re ~1e4 against ~0.01 at Re ~3e5, giving U_max/V_to of 0.58–0.68 versus 1.3–1.5. The barrier is a property of the TAXI, not of the single impulse S29 wrongly blamed.

The claim stands on S32's ceiling law, U_max = f·A_pp·√(c₆/C_D(Re)), with c₆ = 2.55 (the Floryan 2017 pitching fit). If the claim is true, three things must hold one scale down (organ: the caudal lobe as a propulsor) and two things must hold one scale up (behaviour: what the animal does on the water surface).

**Summary.**

| # | Scale | Kind | Requirement | Status |
|---|---|---|---|---|
| C1 | organ | range | Exocoetid lobe drag offset C_D at Re 2.5–4×10⁵, surface-piercing, ≤ 0.019–0.023 | **unsatisfied**: never measured in anything I reached |
| C2 | organ | range | Zebrafish-scale lobe C_D at Re 8×10³–2.6×10⁴ > 0.023–0.027 | **satisfied** by a measured proxy (Floryan 2017: 0.08 pitch, 0.15 heave at Re 4,780) |
| C3 | organ | range | Exocoetid taxi tail speed f·A_pp/V_to in 0.087–0.103, the same as the zebrafish | **unsatisfied**: no measured amplitude; the measured frequencies disagree with each other 3.7-fold |
| C4 | behaviour | timescale | An exocoetid taxi lasts many tail beats: on the order of ≥ 64 strokes, ≥ 1.3 s, ≥ 16 m | **open**: the likely primary sources could not be reached |
| C5 | behaviour | range | Any fish that taxis to a glide with lobe Re ≲ 3×10⁴ must have f·A_pp/V_to ≥ 0.14–0.16 | **unsatisfied**: juvenile flying fish of ~5 cm are reported to fly, but nothing on their taxi was found |

**No constraint is unsatisfiable.** No measured number contradicts claim 272.

The result is lopsided:
- The zebrafish half of the comparison (C2) is supported by a measurement.
- Every requirement on the exocoetid half (C1, C3, C4), where the word "ONLY" does its work, is unmeasured.

So the claim is **not refuted from below. It is also not supported from below.** The discriminator it names ("ONLY lobe C_D") rests on an assumed exocoetid amplitude (C3) and an extrapolated exocoetid C_D (C1). Neither has a measured value at the organ scale.

C5 is the sharpest route to an outright refutation. It needs no flume, only film of a small flying fish taking off.

All bounds below are **derived**: arithmetic on S32's law with S32's inputs. Nothing derived here is a measurement. Reproduce with `python3 -I docs/research/fish/claim-272-entail_check.py`.

## Sources and read levels

| Source | Read level | Used for |
|---|---|---|
| S32-organism.md (author's document) | full-text | the claim, the ceiling law, the inputs |
| Challenge 273 (`origin/claude/challenge-273-exocoetid-taxi-hid0nd`, docs/research/fish/challenge-273.md) | full-text | the amplitude escape; the flat-plate friction estimate; Deng's speed–power pair |
| Challenge 269 (`origin/claude/challenge-269-taxi-stall-pyusap`, docs/research/fish/challenge-269.md) | full-text | sensitivity of the zebrafish ceiling to C_D |
| Floryan, Van Buren, Rowley & Smits 2017, arXiv 1704.07478v1 | **full-text** (arXiv v1 PDF, pdftotext, read by me this session; the JFM published version was not read) | C2: the measured C_D |
| Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560 | **abstract** (Europe PMC record PPR91964, read through a summarising fetch tool, so paraphrased). Full text: **could-not-access** (bioRxiv HTTP 429 on two attempts; Europe PMC fullTextXML HTTP 500) | C3, C4 |
| Davenport 1994, "How and why do flying fish fly?" | **search-summary** (the abstract as shown by a bibliographic listing site, data.zhenzhi.com, through a search engine) | C3: "tail beating in the water at up to 50 beats s⁻¹" |
| APS March Meeting 2024 abstract, "Flying fish taxiing on the water's surface" (meetings-archive.aps.org/mar/2024/s27/13) | **search-summary**. Direct fetch: could-not-access (host outside this session's network allowlist) | C3: tail slapping at 13.5 Hz |
| Edgerton & Breder 1941, "High speed photographs of flying fishes in flight", *Zoologica* (BHL part 203598; BioStor 194322) | **listing** (title and authors seen in search results). Full text: **could-not-access** (biodiversitylibrary.org and archive.org outside the allowlist) | C3, C4: the likely primary film source, not read |
| Davenport 1994, via a Live Science article, "juveniles begin flying at about 5 cm" | **search-summary** (livescience.com outside the allowlist) | C5 |
| Senturk & Smits 2019 (AIAA J.), "Reynolds number scaling of the propulsive performance of a pitching airfoil" | **search-summary** (repository host outside the allowlist) | C1, C2: Re-dependence of the coefficients (**simulated**, 500 ≤ Re ≤ 32,000) |
| Breslin & Skalak 1959; arXiv 2503.18015 (2025) and the TU Delft dataset on ventilation of surface-piercing hydrofoils | **search-summary** | C1: steady surface-piercing foils only |
| Fish 1990 wing-loading allometry WL = 285.0·M^0.400 | via S32 (project-transcribed); not re-read by me | C5 |
| Wiest 1995, J. Zool. 236:571–592 (hatchetfish); Animal Diversity Web account of *Gasteropelecus sternicla* | **search-summary** | C5 scope note |

**Hosts this session could not reach:** meetings-archive.aps.org, biodiversitylibrary.org, archive.org, livescience.com and acikerisim.ege.edu.tr were outside the network allowlist. www.biorxiv.org rate-limited (HTTP 429). Allowing these hosts is the cheapest way to move C3 and C4.

## The bounds, derived from the claim

The ceiling law gives U_max/V_to = r·√(c₆/C_D), where r = f·A_pp/V_to. The claim needs U_max/V_to ≥ 1 for the exocoetid and < 1 for the zebrafish. Its own r values are 0.087–0.095 (exocoetid) and 0.095–0.103 (zebrafish), from S32 §4.1. Hence (derived):

- exocoetid: C_D ≤ c₆·r² = **0.0193–0.0230** (0.0255 at r = 0.10);
- zebrafish: C_D > c₆·r² = **0.0230–0.0271**.

The two thresholds are almost the same number, about 0.023–0.027. That is the content of "they differ ONLY in C_D": the same r, with C_D on either side of ~0.025.

## C1 (organ, range): the large lobe's drag offset must be small

**Requirement.** A surface-piercing caudal lobe at Re 2.5–4×10⁵ oscillating at taxi kinematics must have a cycle-mean drag offset C_D ≤ 0.019–0.023, in the same thrust-law form, with spray, ventilation and wave drag *included*. If spray and ventilation add more than about 0.01, the requirement fails even if friction alone is 0.011.

**Status: unsatisfied.**
- **What meets it only by calculation.** S32's "scaled" extrapolation gives 0.010–0.011 (assumed Re^−½ law). Challenge 273 gives 0.011–0.012 from the turbulent flat-plate formula 0.074·Re^−0.2, two sides (derived). Both are **calculations**, not observations, and both are friction-only.
- **What I searched.** One query on surface-piercing flapping-foil thrust and drag at Re ~10⁵ with ventilation (search-summary). It returned only *steady* surface-piercing hydrofoil and strut work:
  - Breslin & Skalak 1959: ventilation cut lift by up to 70 %;
  - arXiv 2503.18015 and the TU Delft dataset: ventilation inception and steady drag, lift and moment.

  None is a flapping foil, and none reports a thrust-law drag offset.
- **Simulated Re-dependence.** Senturk & Smits 2019 (search-summary, simulated, Re 500–32,000) report that the scaling coefficients vary as √Re, and that thrust is relatively insensitive above Re ~1.6×10⁴. Their range stops 8–12× below the exocoetid lobe's Re, so it cannot test C1.
- **Scope of the negative.** This is "nobody has looked, within what I reached", not "people looked and found nothing". I found no flapping, surface-piercing foil experiment at Re 10⁵–10⁶ at all. That is one query, plus S32's and challenge 273's searches.
- **Direction of the unknown (my inference).** The unmodelled terms (spray, ventilation, wave-making at Froude numbers of order 20) all *add* drag. Challenge 273 §4 makes the same point. So the friction-only figure is a lower bound, and C1 asks it to stay within about a factor of two of that bound.

## C2 (organ, range): the small lobe's drag offset must be large

**Requirement.** An oscillating caudal lobe at Re 8×10³–2.6×10⁴ must have a cycle-mean drag offset C_D > 0.023–0.027. Otherwise the zebrafish ceiling reaches V_to and the claimed barrier disappears.

**Status: satisfied, by a measured value on a proxy foil.**
- **The measurement.** Floryan et al. 2017 (full-text, read this session) fitted C_D = **0.08** for pitching and **0.15** for heaving, by least-squares regression on measured thrust (§5, §4). Conditions: rigid teardrop foil, c = 80 mm, AR 3.5, Re = 4,780 at 60 mm/s (tunnel run 60–120 mm/s), fully immersed, with a free-surface plate.
- **The margin.** That is 3–6.5× the threshold.
- **Proxy caveats.**
  1. The foil is rigid and fully immersed, not a surface-piercing fish lobe.
  2. Re 4,780 is 1.7–5.4× below the zebrafish range.

  On (2): S32's Re^−½ extrapolation gives 0.060 at 1.7×10⁴ and 0.049 at 2.6×10⁴ (derived), still 1.8× above the threshold. To fall below 0.027 by Re 2.6×10⁴, C_D would have to scale as Re^−0.65 or steeper (derived: ln(0.08/0.027)/ln(2.6e4/4780)). That is steeper than laminar friction. Senturk & Smits 2019 (simulated, search-summary) report √Re scaling over a range that covers this one. On (1): surface piercing would add drag, which only widens the margin (my inference).
- **Evidence label.** `measured`, on a proxy. The measurement is real. The zebrafish lobe itself has never been tested (S32 §5 names this as the deciding experiment).

## C3 (organ, range): the exocoetid lobe must move at the shared tail speed

**Requirement.** During the taxi, the exocoetid lobe must have f·A_pp/V_to in **0.087–0.103**, the band the claim says both taxa share. If it is higher, the discriminator is kinematics, not C_D, and "ONLY in lobe C_D" is false. Challenge 273 §3 shows that A_pp = 0.2 L at 50 Hz gives r = 0.17, and lets even the constant-C_D branch taxi.

Converted to an amplitude (derived, V_to 15 m/s, L 0.256 m):

| f | A_pp required | as a fraction of L |
|---|---|---|
| 13.5 Hz | 9.7–11.4 cm | 0.38–0.45 L |
| 50 Hz | 2.6–3.1 cm | 0.10–0.12 L |
| 70 Hz | 1.9–2.2 cm | 0.07–0.09 L |

**Status: unsatisfied.**
- **No measured exocoetid taxi tail amplitude was found.** The searches behind this:
  - S32 (could not access any source);
  - challenge 273 (one query);
  - two queries of mine this session: Edgerton & Breder high-speed film with tail-beat amplitude; Hertel 1966 or Davenport 1994 with tail-beat rate.

  The most likely primary source, the Edgerton & Breder 1941 photographs, was located but **could not be accessed**. So the negative is "not found in reachable sources", not "measured and absent".
- **The frequency measurements disagree, and I am not averaging them.**
  - Davenport 1994 (search-summary of the abstract): "up to 50 beats s⁻¹".
  - Deng 2019 (search-summary of the full text): 50–70 strokes per second, attributed to earlier literature I did not trace.
  - An APS 2024 abstract (search-summary, species not given): tail slapping at **13.5 Hz**.

  The gap is 3.7-fold. Different species, a different definition of a stroke, or peak versus sustained rate are all possible, and I could not tell which. My inference: if 13.5 Hz is the taxi rate, the claim needs A_pp ≈ 0.4 L. That is not contradicted by any measured amplitude, but it would make S32's assumed 2.0–3.1 cm (at 50 Hz) the wrong kinematic picture.
- **The claim's 0.087–0.095 for the exocoetid is assumed, not measured** (S32 §2: lobe 4–6 cm and 15° deflection are ASSUMED, and the deflection is taken from Deng's CFD inputs).

## C4 (behaviour, timescale): the taxi must be a long, many-stroke process

**Requirement.** "The barrier is a property of the TAXI, not of the single impulse" requires that the speed gain on the surface accumulates over many tail beats. The taxi must last much longer than one stroke period, and long enough to approach the steady ceiling. In S32's own scaled-branch runs (§4.2, derived), the 191 g fish needs **64–221 strokes, 1.3–4.4 s and 16–59 m** to go from 10 to 15 m/s. An observed exocoetid taxi much shorter than this would contradict the mechanism S32 uses to reach V_to. The bound I carry is ≥ 64 strokes, as an order-of-magnitude floor.

**Status: open.**
- **What I tried.** One query on flying-fish taxi duration and distance (search-summary). It returned whole-flight figures only: glides of 5–10 s and up to 45 s from popular sites; 400 m in 30 s "by repeated taxiing" from Deng 2019's text. None is a single-taxi duration. Edgerton & Breder 1941 describe a taxi stage that resumes between glides (search-summary), but I could not read their timings.
- **Why open, not unsatisfied.** The likely primary sources were unreachable (biodiversitylibrary.org, archive.org, bioRxiv 429). I am not reporting this as a negative.
- **One partial pointer, my inference only.** "Repeated taxiing" between glides (Edgerton & Breder via search-summary; Deng's abstract) fits a multi-stroke surface process better than a single impulse. It gives no number to test the bound.

## C5 (behaviour, range): small fish that taxi to a glide would need a much faster tail

**Requirement.** If the barrier is lobe C_D at Re ~10⁴, it is a property of *size*, not of zebrafish. Any fish that reaches glide speed by a surface taxi while its lobe works at Re ≲ 3×10⁴ must therefore beat the ceiling another way. Under the claim's own law and drag branch, that means f·A_pp/V_to ≥ **0.14–0.16** (derived), 1.4–1.7× the "shared" value. Alternatively it must launch without a taxi, which S32 and S30 say gliders do not do.

The test case is a juvenile flying fish of ~5 cm. Scaled geometrically from S32's adult (25.6 cm, 191 g, chord 2.5 cm), all derived:
- M ≈ 1.4 g and chord ≈ 4.9 mm;
- V_to ≈ 5.6 m/s, extrapolating the Fish 1990 allometry about 130-fold below its fitted mass range, an assumption that may well be wrong;
- lobe Re ≈ 1.4–2.7×10⁴, which is the zebrafish regime;
- scaled C_D ≈ 0.047–0.067, giving U_max/V_to ≈ 0.59–0.70 at r = 0.095.

That is the zebrafish result. **If 5 cm juveniles taxi to a glide with adult-like r, claim 272 is refuted.**

**Status: unsatisfied.**
- **What exists.** Live Science attributes to Davenport 1994 that juveniles "begin flying at about 5 cm" (search-summary; the article host was unreachable and the review was not read).
- **What does not.** I found nothing on whether juveniles taxi, or on their tail kinematics. My search was one query on juvenile flying-fish size, glide and taxi.
- **Status reasoning.** No known mechanism or measurement meets the requirement, and none contradicts it. This is the highest-value next check.
- **Scope note.** Freshwater hatchetfish (Gasteropelecidae, a few cm) are described as taxiing at the surface and skimming 3–4 m (Animal Diversity Web, search-summary; Wiest 1995, search-summary). They use the pectoral fins with the tail, and are described as hydroplaning rather than gliding (Davenport 1994, via the same summary). My inference is that they are not a clean counter-example: they may never reach a wing-supported V_to. I did not read Wiest 1995.

## What this does to claim 272

- **Not refuted from below.** No measured number contradicts any of the five requirements.
- **One-sided support.** The zebrafish lobe C_D (C2) is backed by a real measurement with a 3–6× margin. The exocoetid half (C1, C3) is assumed or extrapolated. So "they differ ONLY in lobe C_D" is, at the organ scale, a statement about one measured value and one calculated value. Its competitor, "they differ in tail kinematics", is not excluded (C3, and challenge 273 §3).
- **The second sentence** ("a property of the TAXI, not of the single impulse") rests on C4. C4 is open, not failed.
- **Cheapest decisive checks, in order:**
  1. Read Edgerton & Breder 1941 (BHL) for tail frequency, amplitude and taxi duration (C3, C4). This needs biodiversitylibrary.org allowed.
  2. Read Deng 2019 in full for the cited 50–70 Hz source and the 16.5 m/s kinematics (C3).
  3. Find any high-speed film of a ≤ 6 cm flying fish taking off (C5).
  4. Flume test of a surface-piercing oscillating lobe at Re ~3×10⁵ (C1), the only check that needs new apparatus.

```swarm-entail
{"source_claim": 272, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "A surface-piercing oscillating caudal lobe at Re 2.5-4e5 must have a cycle-mean drag offset small enough that the thrust-law ceiling exceeds take-off speed at the shared tail-speed ratio, including spray, ventilation and wave drag",
      "quantity": "exocoetid lobe drag coefficient C_D in C_T = c6*St^2 - C_D (c6 = 2.55), at Re 2.5-4e5", "lo": null, "hi": 0.023, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "Only calculations meet it: S32 Re^-1/2 extrapolation 0.010-0.011 and challenge-273 turbulent flat-plate friction 0.011-0.012, both friction-only and both derived. No flapping surface-piercing foil drag measurement at Re 1e5-1e6 found.",
      "satisfied_evidence": "derived",
      "note": "Derived bound C_D <= c6*r^2 = 0.0193-0.0230 for r = 0.087-0.095. Search: one query on surface-piercing flapping-foil thrust/drag at Re~1e5 with ventilation (search-summary) found only steady surface-piercing hydrofoil/strut work (Breslin & Skalak 1959; arXiv 2503.18015; TU Delft dataset) and Senturk & Smits 2019 (simulated, Re 500-32000, search-summary). Scope: nobody has looked, within the sources reached; not a measured absence. Unmodelled spray/ventilation terms add drag, so the friction estimate is a lower bound."},
    {"target_scale": "organ", "kind": "range",
      "statement": "An oscillating caudal lobe at Re 8e3-2.6e4 must have a cycle-mean drag offset large enough that the thrust-law ceiling stays below take-off speed at the shared tail-speed ratio",
      "quantity": "zebrafish-scale lobe drag coefficient C_D at Re 8e3-2.6e4", "lo": 0.027, "hi": null, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Floryan et al. 2017 measured fitted drag offsets of 0.08 (pitching) and 0.15 (heaving) on a rigid teardrop foil (c 80 mm, AR 3.5) at Re 4780; Re^-1/2 extrapolation to 2.6e4 gives 0.049 (derived), still 1.8x the bound",
      "satisfied_evidence": "measured",
      "note": "Floryan, Van Buren, Rowley & Smits 2017, arXiv 1704.07478v1, full-text (sections 3-5). Proxy: rigid, fully immersed, Re 1.7-5.4x below the zebrafish range; failing the bound needs C_D ~ Re^-0.65 or steeper (derived). Senturk & Smits 2019 report sqrt(Re) coefficient scaling over Re 500-32000 (simulated, search-summary). Derived bound c6*r^2 = 0.0230-0.0271 for r = 0.095-0.103."},
    {"target_scale": "organ", "kind": "range",
      "statement": "During the taxi the large fish's lobe tail speed relative to take-off speed must equal the small fish's, so that drag rather than kinematics is the only difference",
      "quantity": "exocoetid taxi f*A_pp/V_to", "lo": 0.087, "hi": 0.103, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "No measured exocoetid taxi tail amplitude found; the S32 value is assumed (lobe 4-6 cm, 15 deg). Measured tail frequencies conflict: up to 50 beats/s (Davenport 1994, search-summary), 50-70 strokes/s (Deng 2019 text, search-summary), 13.5 Hz (APS 2024 abstract, search-summary).",
      "satisfied_evidence": "assumed",
      "note": "At V_to 15 m/s, L 0.256 m the band requires A_pp 0.10-0.12 L at 50 Hz, 0.07-0.09 L at 70 Hz, 0.38-0.45 L at 13.5 Hz (derived). Challenge 273: A_pp 0.2 L at 50 Hz gives r 0.17 and breaks the premise. Searches: S32, challenge 273 (one query), and two queries this session. Edgerton & Breder 1941 (Zoologica; BHL part 203598) located at listing level but could-not-access (host not allowed); Deng 2019 full text could-not-access (HTTP 429). Scope: not found in reachable sources, not a measured absence. Frequency disagreement preserved, not averaged."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "The surface taxi must be a multi-stroke process lasting long compared with one stroke period, long enough to approach the steady thrust-drag ceiling, so that the speed gain is set by the taxi and not by a single impulse",
      "quantity": "number of tail beats in one exocoetid taxi from ~10 m/s to take-off (S32 scaled-branch model: 64-221 strokes, 1.3-4.4 s, 16-59 m)", "lo": 64, "hi": null, "units": "tail beats",
      "status": "open",
      "satisfied_by": "Not checked to a conclusion: single-taxi durations not found; whole-flight figures only (glides 5-45 s, popular sources; 400 m in 30 s by repeated taxiing, Deng 2019). Edgerton & Breder 1941 describe a taxi stage resuming between glides (search-summary) but their timings were not readable.",
      "satisfied_evidence": "unknown",
      "note": "Lower bound is from S32 section 4.2 model output (derived), an order-of-magnitude floor, not a measurement. One query this session. Primary sources unreachable (biodiversitylibrary.org and archive.org not allowed; bioRxiv HTTP 429), so this is open rather than a negative finding."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "Any fish that reaches glide speed by a surface taxi while its propulsor works at Re below ~3e4 must have a tail-speed ratio well above the shared value, or must launch without a taxi",
      "quantity": "f*A_pp/V_to required for U_max >= V_to at lobe Re 1.4-2.7e4 (e.g. a ~5 cm juvenile flying fish)", "lo": 0.14, "hi": null, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "Juvenile flying fish are reported to begin flying at ~5 cm (Davenport 1994 via Live Science, search-summary), but no measurement of whether or how they taxi, or of their tail kinematics, was found. Hatchetfish surface skimming (Wiest 1995; Animal Diversity Web, search-summary) uses pectoral fins and is described as hydroplaning, so it is not a clean test case.",
      "satisfied_evidence": "unknown",
      "note": "Derived for a 5 cm juvenile scaled geometrically from S32's adult: M 1.4 g, chord 4.9 mm, V_to 5.6 m/s (Fish 1990 allometry extrapolated about 130x below its mass range, assumed), lobe Re 1.4-2.7e4, scaled C_D 0.047-0.067, required r 0.136-0.162, U_max/V_to 0.59-0.70 at r 0.095. One query on juvenile flying-fish glide/taxi; livescience.com could-not-access. Scope: nobody found to have measured juvenile taxi kinematics. A juvenile taxiing to a glide at r ~0.09-0.10 would refute claim 272."}
  ]}
```
