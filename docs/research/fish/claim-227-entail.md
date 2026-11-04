# Claim 227: what it requires at the organ and behaviour scales, and whether those requirements hold

**Source claim (organism scale, evidence: derived):** Energy per stroke is the binding term. One-sided axial muscle (30% of body mass) loading a spring with the best measured work (frog mean 53 J/kg muscle, max 81) supplies only 54–82% of what is needed. The muscle would have to store 98.5 J/kg against the 8.6 J/kg it effectively delivers today, an 11.5x gap. Slow loading buys only 3.7–9.4x.

**Adjacent scales checked:** organ (muscle and series-elastic tissue) and behaviour (how a stroke is timed and loaded).

**Repository context:** No other document on claim 227 exists in this repository. I searched for `fish`, `stroke`, `frog`, `98.5` and `spring-loading` and found nothing. I therefore do not know how the 98.5 J/kg need and the 8.6 J/kg baseline were derived, beyond what the claim says. The arithmetic below is my own check on the claim's numbers.

## 0. Where the claim's numbers come from (traced, not re-derived)

| Claim number | Source found | Read-level |
|---|---|---|
| 53 J/kg muscle ("frog") | Mendoza & Azizi 2021, *J Exp Biol* 224:jeb243180 (PMC10658917). Cuban tree frog (*Osteopilus septentrionalis*) plantaris, mean energy stored during fixed-end tetanic contractions (400 ms train, 80 pulses/s, 22±1 °C), per kg of muscle mass. | full-text (PMC, through an automated fetch-and-summarise tool, so quotes are second-hand) |
| 81 J/kg ("max") | Same paper. The Discussion gives the range as "32–81 J kg−1 muscle mass". | same |
| 3.7–9.4x | Calculated: 32/8.6 = 3.72 and 81/8.6 = 9.42. The claim's lower end therefore uses the **minimum** of the Mendoza & Azizi range (32). | derived |
| 54–82% | Calculated: 53/98.5 = 0.54 and 81/98.5 = 0.82. This uses the **mean** (53), not the minimum. | derived |
| 11.5x | Calculated: 98.5/8.6 = 11.45. | derived |

**Inconsistency in the claim (my inference):** "54–82%" spans mean to maximum, while "3.7–9.4x" spans minimum to maximum. These are different ranges. Using the mean, the slow-loading gain would be 53/8.6 = 6.2x. Either way the conclusion stands, but the two ranges should not be read as describing the same spread.

**Other sources that disagree with the 81 J/kg maximum (kept separate, not averaged):**
- Mendoza & Azizi cite Olberding & Deban 2018 as reaching up to 73 J/kg. I did not read Olberding & Deban myself (read-level: listing, cited inside Mendoza & Azizi).
- Marsh 2022, *J Exp Biol* 225:jeb244525 (PMC9659324), *O. septentrionalis* in vivo jumps (read-level: full-text through the fetch tool):
  - Highest whole-hindlimb muscle work: "approximately 60 J kg−1". The Results give a range of 9.5–63.
  - An idealised length–tension ceiling of about 70 J/kg.
  - These in-vivo values are below the 81 J/kg isolated-preparation maximum. Their denominator is all hindlimb muscle, not plantaris alone.

**Derived quantity used below:** 98.5 J/kg muscle × 0.30 = 29.6 J/kg body per stroke. This is calculated from the claim's own numbers, not observed.

---

## 1. Constraints

### C1. Organ, range: the best measured energy a vertebrate muscle can load into a series spring in one loading must lie below 98.5 J/kg muscle

For the claim to be true, no measured muscle-to-spring loading may reach the 98.5 J/kg need. The claim also assumes that the best values lie in about [32, 81] J/kg muscle.

- **Status: satisfied.**
- **Measured values:**
  - Mendoza & Azizi 2021: range 32–81 J/kg, mean 53 (Cuban tree frog); bullfrog mean 37 (36 in the Discussion); cane toad mean 22 (20 in the Discussion). Fixed-end tetanic contractions, measured.
  - Marsh 2022: in-vivo hindlimb work of at most about 60–63 J/kg, with an idealised ceiling of about 70 J/kg.
  - Olberding & Deban 2018 (cited only): at most 73 J/kg.
- **Negative scope:** In the sources above and two web searches on frog spring-loading work, I found no measured value at or above 98.5 J/kg. I did not survey insects or other arthropods, or vertebrate tongue projection. A tongue-projection or arthropod value above 98.5 would weaken "best measured", though not necessarily for vertebrate axial muscle.

### C2. Organ, range: fish axial fast muscle must deliver about 8.6 J/kg muscle per single stroke today, and not much more

The 11.5x gap holds only if measured single-stroke work of fish fast axial muscle is near 8.6 J/kg. A measured value of 98.5 or more would erase the gap. A value several times 8.6 would shrink it. I set the bounds at [2.7, 20] J/kg: 2.7 is the lowest measured cyclic value, and 20 is my judgement of where the 11.5x figure would become materially wrong.

- **Status: open (contested).**
- **Measured cyclic work-loop values (read-level: search-summary):**
  - Atlantic sculpin fast fibres: about 3.5 J/kg (Johnston et al. 1993).
  - Carp: 2.7 J/kg at 15 °C (*J Exp Biol* 205).
  - Pumpkinseed pectoral-fin muscle: 6.2 J/kg at 1 Hz (Stevens & Luiker; not axial muscle).
  - These are net work per cycle at swimming frequencies, not single maximal escape strokes. They are therefore lower bounds for a stroke, not tests of it.
- **Measured fast-start power (read-level: abstract via search-summary):** Wakeling & Johnston 1998, *J Exp Biol* 201:1505, *Scorpaena notata* fast fibres in work loops at in-vivo strains and durations: mean 142.7 W/kg muscle at 20 °C.
- **Power inferred from hydrodynamics (read-level: search-summary):** Frith & Blake 1995, *J Exp Biol* 198:1863, pike (*Esox lucius*): 449.0 W/kg for C-starts and 394.9 W/kg for S-starts, reported per kg of muscle fibre. A UBC thesis on the same species gives 406–412 W/kg. The two disagree slightly, and both are kept.
- **Why it stays open:** Turning W/kg into J/kg per stroke needs the duration of one stroke. I did not obtain a measured stroke duration for these species, so I have not done the conversion.
  - **Conditional inference, not a result:** 449 W/kg sustained for 20 ms gives about 9 J/kg; sustained for 50 ms it gives about 22 J/kg.
  - So if the Frith & Blake power applies to one side's stroke, the 8.6 J/kg baseline could be low by up to about 2–3x. That would cut the gap from 11.5x to roughly 4–6x, but would not close it.
  - Wakeling & Johnston's directly measured 142.7 W/kg is about 3x lower than Frith & Blake's inferred value. This disagreement between sources is real and unresolved here.

### C3. Organ, existence: a series elastic element and a latch able to hold axial bending energy while the muscle loads must exist

Spring-loading at frog-like levels requires two things in the fish axial system:
- a compliant element in series with the muscle that can absorb at least 98.5 J/kg muscle; and
- a catch that keeps the body from moving while it is loaded. In frogs, a changing mechanical advantage plays this role (Astley & Roberts 2011/2012).

- **Status: unsatisfied.**
- **Scope:** Two web searches on fish myoseptal tendon elastic energy, energy storage, latches and pre-loading returned only frog, grasshopper and locust work. Results on tendon energy density covered turkey and human tendon only.
- **This is "not found in my search", not "people looked and found none".** I did not reach the primary literature on teleost myoseptal or tendon mechanics: Gemballa's myoseptal anatomy, and the tuna and scombrid tendon work. Some journal and library hosts could not be reached from this session (see Access).
- No measured energy density for fish myoseptal collagen was obtained. **Unknown.**

### C4. Behaviour, timescale: for the 3.7–9.4x gain to apply, the behaviour must allow a loading phase of about 65–400 ms before release

The frog values behind 3.7–9.4x come from long loading times:
- Mendoza & Azizi used 400 ms tetanic trains (measured protocol).
- In vivo, Astley & Roberts measured fascicle shortening beginning 107 ± 42 ms before joint movement, so 65 ms or more (measured, *Biol Lett* 8:386, PMC3367733, read-level: full-text through the fetch tool).
- Marsh 2022 reports activation more than 100 ms before the centre of mass accelerates (measured).
- Rosario et al. 2016, *Proc R Soc B* 283:20161561 (PMC5031668, full-text through the fetch tool), bullfrog model: maximum stored energy of 5.09 mJ at 50 ms loading, 14.46 mJ at 100 ms and 20.43 mJ at 300 ms. Loading in 50 ms stores about 25% of the 300 ms value (calculated from **simulated** numbers).

So the requirement is that fish loading time be at least about 65 ms (lo) and approach about 400 ms (hi) for the frog-derived gain to transfer.

- **Status: unsatisfied.**
- **Measured fish timing:** larval zebrafish form the C-bend within about 5–6 ms (read-level: search-summary; primary paper not identified in the summary).
- **Scope:** I found no fish fast-start or leap with a held, motionless pre-loading phase of 65 ms or more, in two web searches on fast-start stage-1 duration and fish pre-loading. Stage-1 durations for adult fish were not obtained.
- **Consequence (my inference):** If fish strokes are limited to times well under 50 ms, the Rosario simulation suggests the achievable gain is below the claim's 3.7–9.4x. This makes the claim's "slow loading buys only 3.7–9.4x" an **upper bound**. It strengthens the claim rather than refuting it.

### C5. Behaviour, energetic: per-stroke body-level demand of about 29.6 J/kg body must exceed what fish strokes are observed to deliver

The claim's need, 98.5 J/kg muscle × 0.30, equals 29.6 J/kg body per stroke (derived). For the binding-term argument to hold, observed fish strokes must deliver well under this.

- **Status: open.**
- **The one candidate number:** a search snippet attributes "mean energetic cost of fast-starts … 26.5 J/kg for C-starts and 18.6 J/kg for S-starts" to the UBC thesis by H. R. Frith on pike energetics (read-level: search-summary; the thesis host could not be reached).
  - The mass basis (body or muscle) is **unknown**.
  - Whether it is mechanical work or metabolic cost is **unknown**.
- **Two readings, both inference:**
  - If it is mechanical work per kg body over a two-stroke C-start, it implies about 13 J/kg body per stroke. At 30% muscle that is about 44 J/kg muscle, roughly 5x the 8.6 baseline and within a factor of about 2.2 of the 98.5 need. This would substantially weaken the 11.5x figure.
  - If it is metabolic cost, at the thesis's reported muscle efficiency of about 0.25 the mechanical work would be roughly 4x smaller, consistent with the claim.
- I cannot decide between these readings without the full text. So I mark this open rather than unsatisfiable.

## 2. Summary

- **No constraint is unsatisfiable:** no measured number I found contradicts the claim.
- **C1 is satisfied** by measured frog data, and that is where the claim's 53/81 come from.
- **C3 and C4 are unsatisfied within a narrow search scope.** Neither gap counts against the claim's conclusion that spring-loading cannot close the energy gap. C4 suggests the slow-loading gain is, if anything, overstated.
- **C2 and C5 are open, and C5 is the main risk to the claim.**
  - The pike fast-start literature reports very high mass-specific power (394–449 W/kg muscle, inferred from hydrodynamics) and a 26.5 J/kg C-start cost of unknown basis.
  - Read one way, these imply fish already deliver several times the 8.6 J/kg baseline.
  - Resolving them needs the full text of Frith & Blake 1995 and the Frith thesis, plus measured stage durations.
- **Internal inconsistency:** the claim's 54–82% and 3.7–9.4x use different lower ends of the Mendoza & Azizi range (mean 53 against minimum 32).

## Access

These hosts failed to resolve from this session (outside its network allowlist), so I read their content only as search summaries or not at all:
- `cob.silverchair.com` and `journals.biologists.com` (J Exp Biol full text)
- `open.library.ubc.ca` (Frith thesis)
- `escholarship.org` (Mendoza dissertation)
- `pubmed.ncbi.nlm.nih.gov`

`pmc.ncbi.nlm.nih.gov` was reachable. To close C2 and C5, add the first three hosts to the session's network settings.

## Sources

- Mendoza E, Azizi E (2021) Tuned muscle and spring properties increase elastic energy storage. *J Exp Biol* 224:jeb243180. https://pmc.ncbi.nlm.nih.gov/articles/PMC10658917/ (full-text through the fetch tool)
- Marsh RL (2022) Muscle preactivation and the limits of muscle power output during jumping in the Cuban tree frog. *J Exp Biol* 225:jeb244525. https://pmc.ncbi.nlm.nih.gov/articles/PMC9659324 (full-text through the fetch tool)
- Astley HC, Roberts TJ (2012) Evidence for a vertebrate catapult: elastic energy storage in the plantaris tendon during frog jumping. *Biol Lett* 8:386–389. https://pmc.ncbi.nlm.nih.gov/articles/PMC3367733 (full-text through the fetch tool)
- Rosario MV, Sutton GP, Patek SN, Sawicki GS (2016) Muscle–spring dynamics in time-limited, elastic movements. *Proc R Soc B* 283:20161561. https://pmc.ncbi.nlm.nih.gov/articles/PMC5031668 (full-text through the fetch tool)
- Frith HR, Blake RW (1995) The mechanical power output and hydromechanical efficiency of northern pike fast-starts. *J Exp Biol* 198:1863. https://journals.biologists.com/jeb/article-abstract/198/9/1863/7098 (search-summary)
- Frith HR. Energetics of fast-starts in northern pike, *Esox lucius* (UBC thesis). https://open.library.ubc.ca/soa/cIRcle/collections/ubctheses/831/items/1.0100459 (search-summary; host could not be reached)
- Wakeling JM, Johnston IA (1998) Muscle power output limits fast-start performance in fish. *J Exp Biol* 201:1505–1526 (abstract via search-summary)
- Johnston IA et al. (1993) Atlantic sculpin fast-fibre work loops, *J Exp Biol* 185:251 (search-summary)
- Carp work loops, *J Exp Biol* 205 (search-summary; the authors were not identified, so this is cited only as a listing)
- Olberding JP, Deban SM (2018), cited in Mendoza & Azizi (listing only)

```swarm-entail
{"source_claim": 227, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The best measured mass-specific energy a vertebrate muscle can load into a series elastic element in one loading must lie below the 98.5 J/kg-muscle need",
      "quantity": "muscle-to-spring stored energy per kg muscle, best measured", "lo": 32, "hi": 81, "units": "J/kg muscle",
      "status": "satisfied",
      "satisfied_by": "Measured: Cuban tree frog plantaris fixed-end tetanic contractions store 32-81 J/kg muscle (mean 53); bullfrog mean 37, cane toad mean 22. In vivo maximum ~60-63 J/kg, idealised ceiling ~70 J/kg (Marsh 2022). No measured value >=98.5 found.",
      "satisfied_evidence": "measured",
      "note": "Mendoza & Azizi 2021 J Exp Biol 224:jeb243180 (PMC10658917, full-text through the fetch tool); Marsh 2022 J Exp Biol 225:jeb244525 (PMC9659324, full-text through the fetch tool); Olberding & Deban 2018 up to 73 J/kg (listing, cited only). Negative scope: frog/anuran literature only; arthropods and tongue projection not surveyed."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Fish fast axial muscle must currently deliver about 8.6 J/kg muscle per single stroke, not several-fold more, for the 11.5x gap to hold",
      "quantity": "single-stroke work of fish fast axial muscle", "lo": 2.7, "hi": 20, "units": "J/kg muscle",
      "status": "open",
      "satisfied_by": "Cyclic work loops give 2.7-6.2 J/kg (lower bounds, not single maximal strokes). Fast-start power: 142.7 W/kg measured in work loops (Wakeling & Johnston 1998) against 394.9-449 W/kg inferred from hydrodynamics (Frith & Blake 1995). No measured stroke duration obtained, so W/kg could not be converted to J/kg.",
      "satisfied_evidence": "unknown",
      "note": "Hypothetical conversion, not a result: 449 W/kg x 20-50 ms (assumed durations) = ~9-22 J/kg, which would shrink but not close the gap. Sources read at search-summary/abstract level; J Exp Biol full text could not be reached from this session."},
    {"target_scale": "organ", "kind": "existence",
      "statement": "A series elastic element plus a latch able to hold axial bending energy while the muscle loads must exist in the fish axial system",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "None found. Two web searches (fish myoseptal tendon elastic energy storage, latch, pre-loading; tendon strain-energy density) returned only frog, insect, turkey and human tendon data.",
      "satisfied_evidence": "unknown",
      "note": "Scope: not found in a narrow web search; NOT a finding that the literature looked and found none. Teleost myoseptal/tendon mechanics primary literature (e.g. scombrid tendons) not reached. Fish myoseptal energy density: unknown."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "For the frog-derived 3.7-9.4x slow-loading gain to apply, the behaviour must allow a held loading phase before release comparable to the frog's",
      "quantity": "pre-release loading duration", "lo": 65, "hi": 400, "units": "ms",
      "status": "unsatisfied",
      "satisfied_by": "Frog side measured: preload 107+/-42 ms (Astley & Roberts 2012), activation >100 ms before acceleration (Marsh 2022), 400 ms tetanus in Mendoza & Azizi 2021. Simulated: 50 ms loading stores ~25% of the 300 ms value (Rosario et al. 2016). Fish side: larval zebrafish C-bend ~5-6 ms (search-summary); no fish behaviour with a >=65 ms held preload found.",
      "satisfied_evidence": "measured",
      "note": "Scope: two web searches on fast-start stage-1 duration and fish pre-loading; adult stage-1 durations not obtained. Inference: the claim's 3.7-9.4x is an upper bound for fish, which strengthens the claim. Astley & Roberts Biol Lett 8:386 (PMC3367733); Rosario et al. Proc R Soc B 283:20161561 (PMC5031668)."},
    {"target_scale": "behaviour", "kind": "energetic",
      "statement": "The per-stroke body-level energy demand implied by the claim (98.5 J/kg muscle x 0.30 = 29.6 J/kg body, derived) must exceed what observed fish strokes deliver",
      "quantity": "mechanical energy per stroke per kg body", "lo": 29.6, "hi": null, "units": "J/kg body",
      "status": "open",
      "satisfied_by": "Candidate: pike fast-start 'energetic cost' 26.5 J/kg (C-start) and 18.6 J/kg (S-start) from the Frith UBC thesis (search-summary). Mass basis and whether this is mechanical or metabolic cost are unknown.",
      "satisfied_evidence": "unknown",
      "note": "If mechanical per kg body over two strokes, it implies ~44 J/kg muscle per stroke (inference), about 5x the 8.6 baseline and a serious challenge to the gap. If metabolic, with ~0.25 muscle efficiency it is consistent with the claim. The thesis host (open.library.ubc.ca) could not be reached from this session."}
  ]}
```
