# Claim 309: what it requires at the cell and organ scales, and whether those requirements are met

**Source claim (tissue, measured):** fast myotomal fibres of *Scorpaena notata*
(Scorpaenidae) produce a mean muscle-mass-specific power of 142.7 W/kg at 20 °C in a
work loop run at in vivo strain and shortening duration (Wakeling & Johnston 1998).

**Subject of every check below:** *Scorpaena notata*. This claim is **not** about zebrafish
and **not** about flying fish. A number from any other animal can be informative here,
but it cannot settle a constraint either way. I name the animal next to every number.

## Sources and how much of each I read

| # | Source | Animal | Read-level |
|---|--------|--------|-----------|
| S1 | Wakeling JM, Johnston IA (1998) Muscle power output limits fast-start performance in fish. *J Exp Biol* 201:1505–1526. doi:10.1242/jeb.201.10.1505, PMID 9556535 | *S. notata* (work loop); 6 marine teleosts (kinematics) | **abstract** (Europe PMC). Full text is paywalled; the journal page was blocked by a bot check. |
| S2 | Wakeling JM, Kemp KM, Johnston IA (1999) The biomechanics of fast-starts during ontogeny in the common carp. *J Exp Biol* 202:3057–3067. PMID 10539954 | *Cyprinus carpio* | abstract |
| S3 | Wakeling JM, Johnston IA (1999) Body bending during fast-starts in fish… *J Exp Biol* 202:675–682. PMID 10021321 | *C. carpio* | abstract |
| S4 | Wakeling JM, Cole NJ, Kemp KM, Johnston IA (2000) *Am J Physiol* 279:R657–665. PMID 10938257 | *C. carpio* | abstract |
| S5 | Langfeld KS, Altringham JD, Johnston IA (1989) *J Exp Biol* 144:437–448, and Langfeld's 1991 St Andrews PhD thesis | *Myoxocephalus scorpius* (short-horn sculpin), live fibre bundles | **search-summary** only. The St Andrews repository is outside this session's network allowlist. Which temperature goes with which value is garbled in the snippet. |
| S6 | Skinned-fibre force–velocity data for sculpin, and for icefish, cod and marlin (Johnston & Altringham 1985, PMID 4059035, and related papers) | several, **not** *S. notata* | search-summary |
| S7 | Resting white-muscle PCr of about 25–35 µmol/g, smaller fish higher (body-size study); creatine charge falling from 0.49 to 0.08 with exhaustive exercise (Schulte, Moyes & Hochachka 1992, *J Exp Biol*) | *Oncorhynchus mykiss* (rainbow trout) | search-summary. I have not confirmed which paper the 25–35 µmol/g figure comes from. |

**Searches I ran (this is the scope of every negative below):**
- Europe PMC: `"Scorpaena notata" AND (muscle OR fibre OR fiber)` gave 25 hits. Only S1 is about
  muscle mechanics; the rest are about peptides, parasites, contaminants or barcoding.
- Europe PMC: `"Scorpaena" AND "work loop"` gave 1 hit (S1).
- Europe PMC: `"fast-start" AND twitch AND "time to peak" AND fish` gave 0 hits.
- Web searches (standard and extended) for *S. notata* fast-fibre Vmax, P0 and twitch kinetics.
  These found nothing beyond S1. One search summary says S1's Table 2 contains V0 values,
  possibly including *S. notata*. **I could not read Table 2.**

So for *S. notata* cell properties, the finding is **"I could not read them"**, not
"people looked and found nothing". S1's full text may already hold them.

**A warning about one search summary.** An early search summary said S1's abstract mentions
10 Hz and 15 Hz cycle frequencies. The abstract I read in full on Europe PMC contains no
such numbers. I have not used them.

---

## Constraints

### C1 (cell, range): the fibres' own force–velocity properties must be able to deliver 142.7 W/kg

**Requirement.** Mean power in a work loop cannot be higher than the fibres' peak isotonic
power over the shortening phase. (This ignores force enhancement from active stretch, which
is small for fast fibres; that is an assumption.) So, at 20 °C, the fast fibres of *S. notata*
must have a peak isotonic power of at least 142.7 W/kg. If the 142.7 is averaged over the
whole cycle rather than only the shortening phase, the requirement is higher. S1's abstract
does not say which, and I did not read the methods.

**Restated as a bound on Vmax. This is a calculation, not an observation.** Assumptions:
- muscle density 1060 kg/m³, so the requirement is 1.51×10⁵ W/m³;
- a Hill hyperbola with curvature G = P0/a.

Then peak power = k(G)·P0·Vmax, where k = 0.134, 0.0955, 0.075, 0.0625 for G = 2, 4, 6, 8.
The minimum Vmax needed is:

| P0 \ G | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| 150 kPa | 7.5 | 10.6 | 13.4 | 16.1 L0/s |
| 200 kPa | 5.7 | 7.9 | 10.1 | 12.1 L0/s |
| 300 kPa | 3.8 | 5.3 | 6.7 | 8.1 L0/s |

For representative values (P0 ≈ 200 kPa, G ≈ 4), Vmax must be at least about 8 L0/s at 20 °C.

**Check: open.**
- **No *S. notata* fibre Vmax or P0 found** (scope above). S1 may report them in a table I could not read.
- **Other species. Neither number can settle C1, and the two disagree with each other:**
  - *Sculpin, live fibre bundles (S5, search-summary).* Vmax values of 4.3, 8.1 and 9.5 L0/s,
    and calculated power of 124 and 256 W/kg (the second at 8 °C), all below 18 °C. These
    numbers meet or exceed C1 at temperatures **below** 20 °C. Note that the 124/256 W/kg
    are the thesis author's values, calculated from a fitted force–velocity equation. They
    are not work-loop measurements.
  - *Sculpin, skinned fibres (S6, search-summary).* Vmax 1.54 L0/s at 20 °C and maximum force
    about 191 kPa. **My calculation:** with G = 4 these give a peak power of about 28 W/kg,
    roughly five times short of C1.
  - Skinned fibres are generally reported to be slower than intact ones, but I have not
    checked that against a source for this particular pair. **I am keeping the
    disagreement, not averaging it away:** live-fibre data from sculpin fit the claim, and
    skinned-fibre data from sculpin do not. Neither is from *S. notata*.
- **This is not `unsatisfiable`.** No *S. notata* measurement contradicts C1.

### C2 (cell, timescale): activation and relaxation must fit inside the in vivo shortening time

**Requirement.** High net power at in vivo shortening durations needs the fibre's force to
rise and fall within one shortening phase:

    (twitch time-to-peak + time to half-relaxation) ≲ in vivo shortening duration, at 20 °C

If relaxation is slower than that, the fibre is still generating force while it is being
re-lengthened, which costs negative work and lowers net work-loop power.

**Check: open.** Neither side has a number from *S. notata*:
- The in vivo shortening duration for *S. notata* is in S1's full text, which I could not read. Value: **unknown**.
- I found no twitch or Ca²⁺-transient kinetics for *S. notata* (scope above; the targeted Europe PMC search returned 0 hits).

The authors do state that their work loops used "similar strain and shortening durations to
those found in vivo" (S1 abstract) and still got 142.7 W/kg. If so, the fibres meet C2 in
the preparation. **That is my inference** from the result, not a separate measurement of
kinetics, so I leave C2 open.

### C3 (cell, energetic): stored high-energy phosphate must pay for the start without resupply

**Requirement.** A fast-start is over before glycolysis or oxidative metabolism can speed up,
so each fibre's own phosphagen store (ATP plus PCr) must cover the energy cost of the start.

**Calculation, not an observation.** The assumptions here are mine:
- the power-producing part of the start lasts 0.1 s;
- mechanical efficiency is 0.25.

Mechanical work is then 142.7 × 0.1 = 14.3 J/kg, and the chemical cost is about 57 J/kg.

**Check: open.** I found no *S. notata* PCr value. Rainbow trout (Salmonidae, S7, search-summary):
- Resting white-muscle PCr is about 25–35 µmol/g. Using about 43 kJ/mol, that is about
  1.1–1.5 kJ/kg, roughly 20 times the calculated cost of one start.
- Creatine charge falls from 0.49 to 0.08 with exhaustive exercise. So the store is used
  heavily in repeated bursts, but by many bursts, not one.

The margin is wide enough that a large difference between species would be needed to
break C3, but **trout are not scorpionfish**, so C3 stays open.

### O1 (organ, energetic): whole-body power demand per kg of fast muscle must not exceed what the muscle can supply

**Requirement.** Power derived from *S. notata* fast-start kinematics (hydrodynamic plus
inertial), divided by the mass of fast muscle that is active, must be no more than about
142.7 W/kg at 20 °C. If it were higher, the work-loop number could not be the power source.

**Check: satisfied (derived), but not by an independent source.** S1 (abstract) states: "At
all temperatures, the predicted mean muscle-mass-specific power outputs, as calculated from
swimming sequences, were similar to the muscle power outputs measured from work-loop
experiments."
- The demand side is **derived**: modelled from filmed kinematics and muscle mass.
- It comes from the **same paper** as the claim, and the claim text quotes it.

So O1 is met only within S1's own analysis. An independent estimate of fast-start power for
*S. notata* would turn this into a real check. I found none (scope above). I give no
numbers for the demand side because the abstract does not state them.

### O2 (organ, spatial): fibre strain must stay within the tested range at every point along the body

**Requirement.** A single work-loop strain can stand for the whole myotomal mass only if
white-fibre strain is similar along the body, within a factor of about 1.5 (my choice of
tolerance). That has to hold even though body curvature increases towards the tail. The
geometry has to supply this: fibre angles, or red-to-white gearing, must change along
the body.

**Check: open. The two sources disagree, and they are about different animals:**
- **S1 (six marine teleosts including *S. notata*; abstract):** "Gearing ratios must
  decrease towards the tail with a corresponding change in muscle geometry, resulting in
  similar white muscle fibre strains in all the myotomes during the start." Per the
  abstract, the gearing ratios came from combining the fast-start kinematics with
  **sonomicrometry from other studies**. So the uniform strain is a **derived** result,
  not strain measured directly in *S. notata*.
- **S2 (common carp; abstract):** "For all sizes, there was a decrease in
  muscle-mass-specific power output and an increase in muscle stress in a posterior
  direction along the body due to systematic variations in fibre strain."
- **S4 (common carp; abstract):** white-muscle fast-start strain changed by +33% with
  acclimation temperature and by −50% with acute temperature.

I have not merged these two positions. For *S. notata*, the only statement available is
S1's derived claim of uniform strain. The carp work (same lab, different family) found
strain that varies along the body. That is evidence that O2 can fail in some teleosts,
not evidence that it fails in *S. notata*.

**For this project, a remark rather than a check:** *Cyprinus* is a cyprinid, like
*Danio*. So the carp result is closer to zebrafish than S1 is. Any move from claim 309
to zebrafish should expect O2 **not** to hold and should not assume one strain fits the
whole body.

---

## Summary

| ID | Scale | Kind | Status | Basis |
|---|---|---|---|---|
| C1 | cell | range | open | No *S. notata* fibre data readable. Sculpin live fibres fit; sculpin skinned fibres fall short. Disagreement kept. |
| C2 | cell | timescale | open | Both sides unknown for *S. notata* |
| C3 | cell | energetic | open | Trout PCr about 20× the calculated need; wrong animal |
| O1 | organ | energetic | satisfied (derived) | S1's own kinematic power matches the work loop. Not independent. |
| O2 | organ | spatial | open | S1 (derived) says uniform strain; carp (S2) says strain varies along the body |

**No constraint is `unsatisfiable`.** No measured *S. notata* value contradicts any of them.
The most useful next step is to read S1's full text (Table 2 and the methods). That would
probably settle C1 and C2 directly, and say whether 142.7 W/kg is averaged over the whole
cycle or only the shortening phase.

```swarm-entail
{"source_claim": 309, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "range",
      "statement": "Intrinsic force-velocity properties of the fast fibres at 20 C must give a peak isotonic power at least as high as the work-loop mean power; with P0 about 200 kPa and Hill curvature G about 4 this means Vmax of at least about 8 L0/s",
      "quantity": "peak isotonic mass-specific power of S. notata fast fibres at 20 C", "lo": 142.7,
      "hi": null, "units": "W/kg",
      "status": "open",
      "satisfied_by": "No S. notata fibre Vmax or P0 found or readable (Europe PMC 'Scorpaena notata' AND muscle: 25 hits, only Wakeling & Johnston 1998 relevant; its Table 2 is paywalled). Other species only: sculpin live fibre bundles 4.3-9.5 L0/s and 124-256 W/kg calculated from a fitted force-velocity curve, below 18 C (meets the bound); sculpin skinned fibres 1.54 L0/s and about 191 kPa at 20 C, which by my calculation gives about 28 W/kg (falls short). Disagreement kept.",
      "satisfied_evidence": "unknown",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505 (abstract); Langfeld et al. 1989 J Exp Biol 144:437 and Langfeld 1991 thesis (search-summary, temperature labels garbled); skinned-fibre data, Johnston & Altringham 1985 and related (search-summary). Vmax bound derived by me, not measured. Different species, so cannot refute."},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "Fibre activation plus relaxation (twitch time-to-peak plus half-relaxation) must be shorter than the in vivo shortening duration at 20 C, so that force is not still present during re-lengthening",
      "quantity": "(t_peak + t_half-relax) / in vivo shortening duration", "lo": null,
      "hi": 1.0, "units": "dimensionless ratio",
      "status": "open",
      "satisfied_by": "Neither twitch kinetics nor in vivo shortening duration found for S. notata. Europe PMC 'fast-start AND twitch AND time to peak AND fish' returned 0 hits; the shortening duration is in Wakeling & Johnston 1998's full text, which I could not access.",
      "satisfied_evidence": "unknown",
      "note": "That the work loops at in vivo durations gave 142.7 W/kg suggests the preparation meets this constraint; that is my inference, not a kinetic measurement."},
    {"target_scale": "cell", "kind": "energetic",
      "statement": "Each fibre's stored phosphagen (ATP plus PCr) must pay for one fast-start without metabolic resupply",
      "quantity": "phosphagen free-energy store per kg fast muscle, compared with the cost of one start (about 57 J/kg, derived assuming 0.1 s and efficiency 0.25)", "lo": 57,
      "hi": null, "units": "J/kg",
      "status": "open",
      "satisfied_by": "No S. notata PCr found. Rainbow trout white muscle resting PCr about 25-35 umol/g, about 1.1-1.5 kJ/kg at 43 kJ/mol (my conversion), about 20 times the calculated need; creatine charge falls from 0.49 to 0.08 after exhaustive exercise (Schulte et al. 1992).",
      "satisfied_evidence": "derived",
      "note": "Trout numbers are search-summary only, and the source of the 25-35 umol/g figure is unconfirmed. Wrong species (Salmonidae vs Scorpaenidae), so the status stays open despite the wide margin."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "Whole-body fast-start power demand (hydrodynamic plus inertial), divided by the mass of active fast muscle, must not exceed the work-loop power available",
      "quantity": "kinematics-derived muscle-mass-specific power of S. notata fast-starts at 20 C", "lo": null,
      "hi": 142.7, "units": "W/kg",
      "status": "satisfied",
      "satisfied_by": "Wakeling & Johnston 1998: predicted mean muscle-mass-specific power from swimming sequences was similar to work-loop power at all temperatures",
      "satisfied_evidence": "derived",
      "note": "J Exp Biol 201:1505 (abstract only; the numbers on the demand side are not in the abstract). Same paper as the claim, so this is not an independent check; I found no independent S. notata fast-start power estimate."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "White-fibre strain during the start must be similar (within a factor of about 1.5) along the body despite curvature rising towards the tail, which requires myotomal geometry or gearing to vary along the body, so that one work-loop strain represents the whole muscle",
      "quantity": "ratio of maximum to minimum white-fibre strain amplitude along the body during the start", "lo": null,
      "hi": 1.5, "units": "dimensionless ratio",
      "status": "open",
      "satisfied_by": "Wakeling & Johnston 1998 (six marine teleosts incl. S. notata) derive similar white-fibre strains in all myotomes, using gearing ratios from kinematics combined with sonomicrometry from other studies; Wakeling, Kemp & Johnston 1999 (common carp) report systematic variation of strain along the body, with posterior power falling and stress rising",
      "satisfied_evidence": "derived",
      "note": "All abstracts (PMIDs 9556535, 10539954, 10938257). The disagreement is across species (Scorpaenidae and others vs Cyprinidae) and is kept. The carp result is the closer guide for Danio. The 1.5 tolerance is my choice."}
  ]}
```
