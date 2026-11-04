# Claim 192: what it requires at the organ and behaviour scales

**Source claim (organism scale, evidence: derived).** S28, `docs/research/fish/S28-organism.md`, branch
`origin/claude/s28-organism-design-5z0vjz`:

> A 3x leap would require a 2.39 m/s exit, 1.73x the measured maximum. Flight requires 4.37 m/s: 3.2x the
> speed and 10x the kinetic energy.

The claim rests on three things.
- **One measured input.** 1.38 m/s is the adult *Danio rerio* maximum swimming-burst speed (Miln et al. 2021,
  as S28 relays it).
- **One project-derived input.** 4.37 m/s is the take-off speed for a 0.25 g fish with a 192 mm², AR-5
  pectoral "wing" at CL_max 1.07.
- **Ballistics.** Range scales as V², so a 3× range needs √3 × V.

Challenge 192 (`origin/claude/challenge-claim-192-7ss3xi`) already re-did the arithmetic and the verdict was
SURVIVED. This note does not repeat it. It asks what must be true one scale down (organ) and one scale up
(behaviour) if the claim holds, and then checks each requirement against the literature.

**Labels used throughout.**
- **calculated**: arithmetic I did in this session (inline Python). It is not an observation.
- **measured**: a number reported by the cited authors from experiments.
- **author's claim**: what a paper asserts, as distinct from my inference, which I mark as such.

## Sources and read-levels

| Source | What I used | Read-level |
|---|---|---|
| Demesmay L et al. 2025, *PLoS Biol* 23(11):e3003484, PMC12604801 | Adult escape max speed, frame rate, stimulus | **full-text**: Europe PMC fullTextXML downloaded this session; quotes are verbatim |
| Miln, Ward & Seebacher 2021, *R Soc Open Sci* 8:210146 | Per-fish burst maxima 0.45–1.38 m/s at 120 fps | **listing**: relayed by S28 and `challenge-75.md`; I did not open the paper |
| Wakeling JM & Johnston IA 1998, *J Exp Biol* 201:1505, doi 10.1242/jeb.201.10.1505 | Whether fast-starts run at the muscle power limit; 142.7 W kg⁻¹ | **abstract** (Europe PMC) |
| Wakeling JM, Kemp KM & Johnston IA 1999, *J Exp Biol* 202:3057 | Carp ontogeny: fast-start gains are met by muscle power | **abstract** |
| Gibb AC, Ashley-Ross MA, Pace CM & Long JH 2011, *J Exp Zool A*, doi 10.1002/jez.711 | *Danio* makes terrestrial tail-flip jumps | **abstract** |
| SICB abstract on stranded *D. rerio* and *G. affinis* (sicb.org/?p=24820) | Terrestrial jump distance about 0.10 m mean, 0.27 m max | **search-summary**: sicb.org is blocked from this session's network (ENOTFOUND); I saw only a search engine's summary |
| Ravel G et al. 2025, *iScience*, PMC11930232 | Checked for adult power numbers; it covers only 5 dpf larvae | **full-text** (XML), not used for a number |

---

## Behaviour scale

### B1 (range). The "measured maximum" must be about 1.38 m/s. **UNSATISFIABLE as stated**

**Requirement.** The 3.2× and 10× ratios are 4.37/1.38 and (4.37/1.38)². They need the highest measured adult
escape or burst speed to be 1.38 m/s. A *measured mean* above 1.38 m/s contradicts "measured maximum".

**Measured contradiction.** Demesmay et al. 2025 (full-text, verbatim):
- Speed: "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants)".
- Video: escape responses filmed "at … 240 frames/s (escape response, 1 s long videos)".
- Stimulus: "Two similar objects (1 g) placed at approximately 30 cm above" the tank and dropped to evoke the
  escape.

So the mean of adult control fish is 1.57 m/s (mean ± SD), above the value the claim calls the maximum.

**Consequences (calculated), using 1.57 m/s as the baseline.**
- Flight needs 4.37/1.57 = **2.78×** the speed and **7.7×** the kinetic energy, not 3.2× and 10×.
- With the mutant mean of 1.61 m/s: **2.71×** and **7.4×**.
- The 1.73× figure for the 3× leap is √3. It does not depend on the baseline, so it survives. The absolute
  2.39 m/s does not: from a 1.57 m/s baseline, a 3× leap needs √3 × 1.57 = **2.72 m/s**.

**The disagreement, kept as it is.**
- **The two studies used different methods.**
  - Miln 2021: per-fish best of 4 trials at 120 fps (listing only).
  - Demesmay 2025: phone camera at 240 fps, manual tracking in Fiji, falling-object stimulus, n ≥ 11 per
    genotype.
- **Peak speed in Demesmay 2025 rests on very few frames.** The authors report a "latency to attain maximal
  speed (8 ± 4 ms …)", which is about 2 frames at 240 fps.
- **My inference, not the authors' claim:** a peak taken from so few frames with manual digitisation is prone
  to upward noise. That could inflate the mean. I cannot test this without the per-frame data.
- **Neither number is a water-exit speed** (see B3).

**What this result means.**
- It refutes the claim's *specific* ratios (3.2×, 10×) from below. It does so with a measured number, so no
  simulation is needed.
- It does **not** refute the qualitative conclusion. Even the corrected deficit of 2.7–2.8× in speed is large.

### B2 (range). Attainable adult burst or exit speed must stay below the 3×-leap speed, hi = 2.39 m/s. **SATISFIED within the scope searched**

**Requirement.** The claim implies that a 3× leap is out of reach. If any adult fish already reached 2.39 m/s,
the "1.73× deficit" would not exist for that fish.

**Measured values.**
- Miln 2021 reports a per-fish best of **1.38 m/s** (listing).
- Demesmay 2025 reports 1.57 ± 0.27 and 1.61 ± 0.33 m/s. The text does not give per-fish maxima.

**Calculated, assuming a normal distribution.** 2.39 m/s sits 3.0 SD above the control mean and 2.4 SD above
the mutant mean. Mean + 2 SD is 2.11 m/s (controls) and 2.27 m/s (mutants).

**Scope.**
- These are the two studies found.
- I did not read the Demesmay 2025 supplementary per-fish data. An individual above 2.39 m/s is therefore
  *not excluded*. It is only unreported.
- If B1's baseline is adopted, the bound becomes 2.72 m/s, and B2 is satisfied with more room.
- Flight (4.37 m/s) is far above every measured value.

### B3 (existence). A water-exit leap must exist in *Danio*, with its exit speed measured. **UNSATISFIED; nobody appears to have measured it**

**Requirement.** The claim's "3× leap" is a multiple of a wild-type leap. That leap is the 19.4 cm ballistic
range S28 computes from 1.38 m/s. The requirement is that adult *Danio* leap out of water, and that their exit
speed is bounded by their swimming burst. Burst speed is used as a proxy for exit speed, on the argument that
crossing the surface costs momentum.

**Found.**
- **Terrestrial jumping, not water exit.** Gibb et al. 2011 (abstract) show that *D. rerio* makes tail-flip
  terrestrial jumps that are "kinematically distinct from aquatic escapes".
- **Distances on land only.** A SICB abstract (search-summary only; sicb.org was unreachable) reports land-jump
  distances of about 0.10 m on average and 0.27 m at most. It gives no exit or take-off speed.
- **Converting the distance, with caveats (calculated).** At 45° with no drag, 0.27 m implies a take-off speed
  of about 1.63 m/s. That is take-off from a substrate, not exit from water, and the take-off angle is assumed.
  It cannot stand in for exit speed.

**Not found: any measured aquatic water-exit speed or leap height for *Danio*.** Searches run:
- WebSearch (standard): "zebrafish Danio rerio jumping out of water leap height aerial jump measured".
- Europe PMC: `(zebrafish OR "Danio rerio") AND (jump OR leap OR leaping) AND (water OR aerial OR surface)`
  returned 1635 hits. I inspected only the top 12, all irrelevant.
- Europe PMC: `(zebrafish OR "Danio rerio") AND ("water exit" OR "out of the water" OR "aerial jump" OR
  "jumping out")` returned 362 hits. I inspected the top 15, all husbandry, toxicology or stress protocols.

**Scope of the negative.** It is shallow: top-ranked hits only, and no Google Scholar or Web of Science.
- No paper I saw reports *looking* for zebrafish water-exit speed and failing to find it.
- I therefore read this as "nobody appears to have measured it", **not** "people looked and found nothing".
- S28 and Challenge 192 had already listed it as unmeasured. Neither searched.

---

## Organ scale

### O1 (energetic). The axial musculature must have no large power reserve beyond what the maximal escape already uses. **OPEN: supported in other teleosts, untested in *Danio***

**Requirement.** The claim treats the measured maximum burst as a ceiling. That is only true if the burst is
limited by the power the propulsive organ (axial fast muscle plus tail) can deliver, rather than by motivation
or the stimulus.

**What a 3× leap and flight would demand (calculated).**
- Kinetic energy per unit body mass at exit:
  - 0.95 J kg⁻¹ at 1.38 m/s;
  - 2.86 J kg⁻¹ for the 3× leap (2.39 m/s);
  - 9.55 J kg⁻¹ for flight (4.37 m/s).
- If the fast-start keeps the same duration and the same muscle fraction and hydrodynamic efficiency, the mean
  mass-specific muscle power must rise by:
  - 3.0× for the 3× leap and 10× for flight, at fixed duration;
  - 5.2× and 32×, at fixed acceleration distance.
- So, at fixed duration, a 3× leap needs muscle power at least 3× what produced the 1.38 m/s burst. The organ
  must lack that reserve for the claim's "deficit" to be physical rather than motivational.

**Evidence found.**
- Wakeling & Johnston 1998 (abstract, author's claim) studied six marine teleosts. No *Danio* or other
  cyprinid was included.
  - They report "predicted mean muscle-mass-specific power outputs, as calculated from swimming sequences,
    were similar to the muscle power outputs measured from work-loop experiments".
  - Their measured work-loop figure is "142.7 W kg⁻¹" for fast fibres of *Scorpaena notata* at 20 °C.
- Wakeling, Kemp & Johnston 1999 (abstract) studied carp, a cyprinid like *Danio*. They report that fast-start
  gains during ontogeny "can be explained by size-dependent increases in muscle power output".

**Why this stays open.**
- The claim is about *Danio*. Carrying the result over from other species is my inference, not a measurement.
- No *Danio* adult work-loop or in-vivo fast-start power measurement turned up in my searches. Scope: the
  Europe PMC author query `AUTH:"Wakeling JM" AND "fast-start" AND power` and one WebSearch, "adult zebrafish
  fast-start escape peak acceleration m/s2 muscle power output". The only zebrafish power paper found (Ravel et
  al. 2025) covers 5 dpf larvae.
- The *Danio* white-muscle mass fraction is also **unknown**. I did not find it.

### O2 (spatial). A lifting surface of about 192 mm² (span about 1 SL, AR about 5) must exist on a 0.25 g fish for V_to = 4.37 m/s. **UNSATISFIED: never measured, and nothing found**

**Requirement.** The 4.37 m/s figure is not a property of the wild-type fish. It needs a pectoral planform of
S ≈ 192 mm². That is a wing loading of 12.5 N m⁻², per S28: 0.5·1.225·4.37²·1.07.

**If the area is smaller (S28's own derived cases, not re-derived here).**
- S ≈ 57 mm² (case A) gives V_to = 8.10 m/s.
- S ≈ 125 mm² (case B) gives 5.47 m/s.
- Either way the flight deficit is larger.

**Evidence.**
- S28 records that the pectoral fin area of the Daane et al. 2021 elongated-fin double heterozygote was never
  measured. S28 also assumed the wild-type fin area (10 mm²).
- My search turned up no measured adult *Danio* pectoral fin area. Query: Europe PMC
  `(zebrafish OR "Danio rerio") AND "pectoral fin" AND ("fin area" OR "surface area") AND adult`, 78 hits, top
  15 inspected, none relevant.
- Scope: top-ranked hits only. I did not read Daane et al. 2021 Fig. 4B, which gives length, not area.

**Status.** Unsatisfied, in the sense that no known measurement shows such a surface. Nothing contradicts it
either: no measured number says the area *cannot* be 192 mm². So it is not unsatisfiable.

**Direction of the effect.** If the true area is smaller, the claim's 3.2× understates the deficit. A
violation here would *strengthen* the conclusion that flight is impossible while falsifying the exact
4.37 m/s.

---

## Summary

| # | Scale | Kind | Status | One-line reason |
|---|---|---|---|---|
| B1 | behaviour | range | **unsatisfiable** | A measured mean of 1.57 m/s (Demesmay 2025) exceeds the claimed 1.38 m/s maximum. Flight ratios become 2.78× and 7.7× (calculated) |
| B2 | behaviour | range | satisfied | No measured value reaches 2.39 m/s. Per-fish maxima for Demesmay were not read |
| B3 | behaviour | existence | unsatisfied | No measured *Danio* water-exit speed was found. Only terrestrial jumps are documented. The search was shallow and nobody appears to have looked |
| O1 | organ | energetic | open | Muscle-power-limited fast-starts are shown in 6 marine teleosts and in carp, but not tested in *Danio* |
| O2 | organ | spatial | unsatisfied | The 192 mm² lifting surface has never been measured. A smaller area would make the flight deficit worse |

**Net effect on claim 192.**
- The *numbers* "3.2× the speed and 10× the kinetic energy" are refuted from below by a measured adult escape
  speed. On that baseline they read 2.7–2.8× and 7.4–7.7×.
- "1.73×" for a 3× leap is √3 and stands.
- The conclusion that both the leap and flight are out of reach is not refuted by anything found.
- Its weakest support is B3. The quantity that actually matters, water-exit speed, has never been measured in
  this species.

```swarm-entail
{"source_claim": 192, "source_scale": "organism",
  "constraints": [
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The highest measured adult escape/burst speed must equal the claim's stated maximum, so that the flight ratios 4.37/v_max = 3.2x and (4.37/v_max)^2 = 10x hold",
      "quantity": "maximum measured adult burst/escape speed", "lo": null, "hi": 1.38, "units": "m/s",
      "status": "unsatisfiable",
      "satisfied_by": "Contradicted by a measured value: Demesmay et al. 2025 report adult control maximal escape speed 157 +/- 27 cm/s (mean +/- SD; mutants 161 +/- 33), so the population MEAN exceeds the claimed maximum. Recomputed (calculated): flight needs 2.78x speed and 7.7x KE vs 1.57 m/s; the 1.73x leap ratio is sqrt(3) and survives, but its absolute speed becomes 2.72 m/s",
      "satisfied_evidence": "measured",
      "note": "Demesmay L et al. 2025 PLoS Biol 23(11):e3003484, PMC12604801, full-text (240 fps phone camera, manual Fiji tracking, dropped-object stimulus, n>=11/genotype). Disagrees with Miln et al. 2021 R Soc Open Sci 8:210146 (per-fish best 1.38 m/s at 120 fps; listing via repo relay, not opened). My inference, not the authors': a peak speed reached in 8 +/- 4 ms (about 2 frames) may be noise-inflated. Neither study measures water-exit speed. The qualitative flight deficit is not refuted."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "Attainable adult burst/exit speed must stay below the speed a 3x leap requires (else no deficit exists)",
      "quantity": "attainable adult burst or water-exit speed", "lo": null, "hi": 2.39, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "No measured value reaches 2.39 m/s: Miln 2021 per-fish best 1.38 m/s; Demesmay 2025 means 1.57 and 1.61 m/s with mean+2SD = 2.11 / 2.27 m/s (calculated, normality assumed)",
      "satisfied_evidence": "measured",
      "note": "Scope: two studies. Demesmay 2025 per-fish maxima (supplementary data) were NOT read, so an individual >2.39 m/s is unreported rather than excluded. On the B1-corrected baseline the bound is 2.72 m/s and is met with more margin."},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "An aquatic water-exit leap behaviour must exist in adult Danio with a measured exit speed, defining the 1x baseline and validating burst speed as an upper-bound proxy for exit speed",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Not found. Only TERRESTRIAL tail-flip jumping is documented for D. rerio (Gibb et al. 2011, abstract), plus a SICB abstract reporting land-jump distance ~0.10 m mean / 0.27 m max (search-summary only). No measured aquatic exit speed or leap height located",
      "satisfied_evidence": "unknown",
      "note": "Searches: WebSearch 'zebrafish Danio rerio jumping out of water leap height aerial jump measured'; Europe PMC '(zebrafish OR \"Danio rerio\") AND (jump OR leap OR leaping) AND (water OR aerial OR surface)' (1635 hits, top 12 inspected) and '... AND (\"water exit\" OR \"out of the water\" OR \"aerial jump\" OR \"jumping out\")' (362 hits, top 15 inspected). Shallow scope. No study was found that looked and failed, so this reads as 'nobody appears to have measured it', not 'looked and found nothing'. sicb.org was unreachable from this session."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "The propulsive musculature must already operate near its maximal mass-specific power during the maximal escape (no reserve of ~3x for a 3x leap or ~10x for flight at fixed fast-start duration)",
      "quantity": "ratio of available to used muscle-mass-specific power in a maximal fast-start", "lo": null, "hi": 3.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Supported in other taxa: Wakeling & Johnston 1998 report in-vivo fast-start muscle power similar to work-loop maxima (142.7 W/kg, Scorpaena notata fast fibres, 20 C) across six marine teleosts; Wakeling, Kemp & Johnston 1999 attribute carp fast-start gains to muscle power. No Danio measurement found; the Danio white-muscle mass fraction is unknown",
      "satisfied_evidence": "literature",
      "note": "Wakeling JM & Johnston IA 1998 J Exp Biol 201:1505 (abstract); Wakeling JM, Kemp KM & Johnston IA 1999 J Exp Biol 202:3057 (abstract). Required power ratios are calculated (v^2 scaling: 3.0x leap, 10x flight; v^3 at fixed distance: 5.2x, 32x). Applying these results to Danio is my inference. Search scope: Europe PMC AUTH:\"Wakeling JM\" fast-start power; one WebSearch for adult zebrafish fast-start power/acceleration. The only zebrafish power study found (Ravel et al. 2025, iScience, PMC11930232) is on 5 dpf larvae."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "A paired lifting surface of ~192 mm2 (span ~1 SL, AR ~5) must exist on a ~0.25 g fish for take-off speed to be as low as 4.37 m/s",
      "quantity": "total pectoral planform area", "lo": 192, "hi": null, "units": "mm^2",
      "status": "unsatisfied",
      "satisfied_by": "No measured adult Danio pectoral fin area found, wild-type or Daane et al. 2021 elongated-fin double heterozygote; S28 assumed wild-type ~10 mm2 per fin. Nothing measured contradicts 192 mm2, so not unsatisfiable",
      "satisfied_evidence": "unknown",
      "note": "Europe PMC '(zebrafish OR \"Danio rerio\") AND \"pectoral fin\" AND (\"fin area\" OR \"surface area\") AND adult' (78 hits, top 15 inspected, none relevant). Daane et al. 2021 Curr Biol 31:5052 not read (reports length, not area). A smaller true area raises V_to (S28 cases: 5.47 m/s at 125 mm2, 8.10 m/s at 57 mm2), which would worsen, not rescue, the flight deficit."}
  ]}
```
