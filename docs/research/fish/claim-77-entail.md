# Claim 77: what it requires at the cell and organ scales

**Source claim (tissue scale, evidence: derived).** S10-D verdict strengthens: the measured teleost
pectoral-muscle fraction is ~1.4% of body mass for both fins (*Abudefduf saxatilis*, 0.69% per fin,
Mansuit & Herrel 2021 Table 1), against a computed threshold of 7.5-20%. Hover demand is
730-1950 W/kg, 5-15x above measured warm zebrafish fast muscle.

**What the claim says.** A teleost, and the zebrafish in particular, cannot hover in air on its
pectoral fins. The muscle is too small (organ scale), and each kilogram of it cannot deliver the
power hovering needs (cell scale).

**What kind of numbers it rests on.** The 7.5-20% threshold and the 730-1950 W/kg demand are
model outputs (derived), not observations. The 1.4% fraction is a measurement, but of a damselfish,
not a zebrafish. The "measured warm zebrafish fast muscle" value is a measurement on zebrafish.

## Limits of this check

- **Network.** These hosts could not be reached from this session (DNS blocked):
  hal.sorbonne-universite.fr, pubmed.ncbi.nlm.nih.gov and orbi.uliege.be. So **no paper was read in
  full text**. Every source below is at `search-summary` or `abstract` read-level, and is labelled.
- **The cited table was not checked.** I could not confirm Mansuit & Herrel 2021 Table 1. My search
  for it found Mansuit, Huby, Herbin & Herrel 2021 (*Biol. J. Linn. Soc.*), a paper on the paired-fin
  muscles of the coelacanth *Latimeria chalumnae* (read-level: listing). The search summary did not
  say whether that paper includes an *Abudefduf* comparison table. The 0.69%-per-fin figure is
  therefore carried forward from the claim, **unverified by me**.

---

## C1 (cell, range): the muscle's cyclic power per kilogram must be below 730 W/kg

**Requirement.** If the claim is true, then the net power that the pectoral muscle can deliver over
a full contraction cycle, per kilogram of muscle, must lie below the lower bound of the computed
hover demand, 730 W/kg. If any teleost muscle fibre could sustain more than that in repeated cycles,
the power half of the claim would fail.

**Evidence.**
- **Zebrafish, but a different tissue.** Mead, Kennedy, Palmer, Ebert & Warshaw 2020 (*Biophys. J.*
  119:806-820) measured larval zebrafish tail muscle, not pectoral fin muscle, at 5 days old.
  - The authors report a net power of **134 ± 20 W/kg at 80 Hz** in work-loop experiments.
  - Read-level: abstract, via search summary. I could not confirm the test temperature.
  - This is presumably the "warm zebrafish fast muscle" value in the claim. 730/134 ≈ 5.4, which
    matches the claim's "5x" end. That match is my inference.
- **Ceiling across vertebrates.** The highest cyclic value I found for any vertebrate is the
  blue-breasted quail pectoralis during take-off.
  - It is about **350-400 W/kg**, measured two ways: in vivo (Askew & Marsh 2001, *J. Exp. Biol.*
    204:3587) and by aerodynamic analysis (Askew, Marsh & Ellington 2001, *J. Exp. Biol.* 204:3601).
  - Read-level: abstract and search summary.
  - The sources disagree, and I am not averaging them. The raw in vivo net figure in Askew & Marsh
    2001 is **80 W/kg**. The authors attribute it to an artefact in the force record during
    lengthening. The ~350-400 W/kg value comes after that correction.
- **Higher numbers that do not count.** Frog jumps give larger values: over 750 W/kg average and
  2000 W/kg peak in the Cuban tree frog (read-level: search summary).
  - These are single jumps boosted by elastic energy storage in tendons. Hovering is repeated
    cycling, so they do not meet the requirement.
  - The same summary gives the frog's own available muscle power as about 313 W/kg.

**Verdict: satisfied, with a tissue caveat.**
- The zebrafish measurement (134 W/kg) and the vertebrate ceiling (~400 W/kg) both lie below
  730 W/kg.
- The zebrafish number is from larval tail muscle, not adult pectoral fin muscle.
- I found no power measurement of zebrafish pectoral fin muscle, so that specific subject has not
  been checked. My search also found no measurement of slow versus fast fibre proportions in the
  adult pectoral muscle. Patterson & Devoto 2008 (read-level: search summary) report that slow
  fibres appear in the fin only at the juvenile stage.
- The satisfaction rests on the cross-vertebrate ceiling. It is not a pectoral-specific measurement.

## C2 (cell, timescale): beating the fin faster must not close the gap

**Requirement.** Power equals work per cycle times cycle frequency. For the claim to hold, the
needed power must not be reachable just by contracting faster. Concretely, the cycle frequency
required, (730 W/kg) ÷ (work per cycle), must exceed the fastest rate at which zebrafish muscle can
cycle.

**Evidence, as arithmetic on measured numbers (derived, not observed).**
- From Mead et al. 2020: 134 W/kg ÷ 80 Hz ≈ **1.7 J/kg of work per cycle**.
- Holding that work per cycle fixed, reaching 730 W/kg needs about **435 Hz**. Reaching 1950 W/kg
  needs about **1160 Hz**.
- Mead et al. report work loops up to **100 Hz** (read-level: abstract). In most muscles, work per
  cycle falls as frequency rises, so the true required frequency would likely be even higher. That
  last point is my inference.

**Verdict: open.**
- I found no zebrafish muscle data above 100 Hz. The search scope was the abstract of Mead et al.
  2020 plus one search on zebrafish work-loop power. Whether faster cycling is impossible has
  therefore not been measured.
- The arithmetic points toward the claim, but frequencies more than 4x beyond the tested range are
  an extrapolation, not a measurement.
- The fin's own aerodynamics at high frequency are not addressed here either.

## C3 (organ, range): zebrafish pectoral muscle must be below 7.5% of body mass

**Requirement.** The claim needs the zebrafish's measured pectoral-muscle fraction (both fins
combined) to fall below the lower end of the computed threshold, which is 7.5% of body mass.

**Evidence.**
- **The claim's own number is from another species.** The 1.4% value is from *Abudefduf saxatilis*,
  a damselfish, not the zebrafish. I could not verify it either (see "Limits of this check").
- **A related survey I could not read.** Thorsen & Westneat 2005 (*J. Morphol.*,
  doi 10.1002/jmor.10173) measured pectoral muscle masses in 12 species of fish that swim mainly with
  their pectoral fins (read-level: abstract). The abstract reports "broad variation among species",
  but I could not get percent-of-body-mass values.
- **No zebrafish measurement found.** I searched for zebrafish pectoral fin muscle mass, adductor and
  abductor mass, and pectoral fin area against body mass.
  - Thorsen & Hale 2005 and a later paper (PMC5770327) describe the adult muscle layout, with seven
    named muscles, but give no masses (read-level: search summary).
  - This is "nobody has measured it, as far as this search reaches". It is not "people looked and
    found nothing".

**Verdict: open.**
- The two species differ: the measured number is for *A. saxatilis*, while the claim is about
  *Danio rerio*.
- My inference, not an observation: a damselfish swims mainly by flapping its pectoral fins, while a
  zebrafish swims mainly with its body and tail. A zebrafish's fraction is therefore more likely
  lower than higher. That is a prior, not a measurement, and it does not settle the constraint.

## C4 (organ, range): the minimum muscle fraction for weight support must fall within 7.5-20%

**Requirement.** The claim's threshold is computed. If it is right, an independent measurement of
how much lift flying animals get per kilogram of flight muscle should give a minimum fraction inside
7.5-20%. To support body weight, the muscle fraction must be at least g ÷ (lift per kg of muscle).

**Evidence.**
- Marden 1987 (*J. Exp. Biol.* 130:235-258; read-level: abstract and search summary) added weights
  to insects, birds and bats until they could no longer take off.
  - Maximum lift was **54-63 N per kg of flight muscle** for most taxa.
  - It was **72-86 N/kg** for insects using clap-and-fling wingbeats.
  - The same abstract gives a flight-muscle ratio of **0.115-0.56** across the species studied.
- My arithmetic (derived): 9.81 ÷ 86 ≈ **11.4%**, and 9.81 ÷ 54 ≈ **18.2%**. Both lie inside the
  claim's 7.5-20% band.
- The same arithmetic applied to a 1.4% fraction means the muscle would have to produce about
  **700 N of lift per kg**. That is 8-13x Marden's ceiling.

**Verdict: satisfied.**
- An independent, measured cross-taxon value supports the computed threshold.
- The taxa differ: Marden's animals are insects, birds and bats, not fish. That is acceptable here,
  because this constraint is about the physics of supporting weight in air, which is the same for
  any flyer. It is not about a zebrafish property.
- Fish muscle is weaker per kilogram than flight muscle (see C1), which would push the real fish
  threshold higher, not lower. That is my inference.
- This supports the claim. It does not refute it.

## C5 (organ, spatial + conservation): the fin area must be too small for the available power

**Requirement.** To hover, the fins must push air downward at a rate whose momentum equals the
fish's weight. With ideal actuator-disc theory (a standard simplified model of a rotor or flapping
wing), the minimum power is P = √((mg)³ / (2ρA)). Here m is body mass, g is gravity, ρ is air
density and A is the area the fins sweep.
- For the claim to hold, A must be small enough that this ideal power, divided by pectoral muscle
  mass, is at least the C1 ceiling.
- Equivalently, A must be smaller than the area that would bring the power demand down to what the
  muscle can supply.

**Evidence.**
- I found no measured adult zebrafish pectoral fin area or swept area. The search covered zebrafish
  pectoral fin area in mm², body-mass morphometrics, and fin length datasets.
  - A ZooKeys table gives fin lengths only.
  - Danos & Lauder 2007 report fin kinematics but no area.
  - Read-level for both: search summary.
- I did not substitute a guessed area, because that would produce a derived number from an
  invented input.

**Verdict: open.** The area is unknown, so the constraint cannot be checked yet. A measured adult
zebrafish pectoral fin span and area would close it with no simulation needed.

---

## Summary

| # | Scale | Kind | Status | Animal(s) behind the number |
|---|---|---|---|---|
| C1 | cell | range | satisfied (tissue caveat) | zebrafish larval tail muscle; quail pectoralis |
| C2 | cell | timescale | open | zebrafish larval tail muscle (extrapolated) |
| C3 | organ | range | open | *A. saxatilis*, not zebrafish |
| C4 | organ | range | satisfied | insects, birds and bats (physics of weight support) |
| C5 | organ | spatial | open | no zebrafish fin area found |

**No constraint is unsatisfiable.** No measured number found here contradicts claim 77.

The claim's weakest link is C3. Its organ-scale fraction is a damselfish measurement applied to a
zebrafish, and I could not verify it. One measurement each would decide C3 and C5:
- the dissected pectoral muscle mass of an adult zebrafish;
- the area of an adult zebrafish pectoral fin.

```swarm-entail
{"source_claim": 77, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "range",
      "statement": "Net cyclic mass-specific power deliverable by the pectoral fin-actuating muscle fibres must lie below the lower bound of computed hover demand",
      "quantity": "net cyclic muscle power per kg muscle", "lo": null, "hi": 730, "units": "W/kg",
      "status": "satisfied",
      "satisfied_by": "Zebrafish larval (5 dpf) tail muscle net work-loop power 134 +/- 20 W/kg at 80 Hz (Mead et al. 2020); highest cyclic vertebrate value found ~350-400 W/kg, quail pectoralis take-off (Askew & Marsh 2001; Askew, Marsh & Ellington 2001)",
      "satisfied_evidence": "measured",
      "note": "Mead et al. 2020 Biophys J 119:806 (abstract via search-summary; temperature not confirmed). Askew & Marsh 2001 JEB 204:3587 and Askew et al. 2001 JEB 204:3601 (abstract/search-summary); raw in vivo net 80 W/kg vs corrected ~350-400 W/kg, disagreement preserved. Tissue caveat: no zebrafish PECTORAL muscle power measurement found; satisfaction rests on axial-muscle proxy plus vertebrate ceiling. Frog-jump values >750 W/kg are elastic single-shot, not cyclic, so excluded."},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "The power deficit must not be closable by raising contraction frequency: the cycle frequency required at measured work-per-cycle must exceed the fibres' maximum cycling rate",
      "quantity": "required cycle frequency at measured work per cycle", "lo": 435, "hi": 1160, "units": "Hz",
      "status": "open",
      "satisfied_by": "Derived: 134 W/kg / 80 Hz = 1.7 J/kg/cycle, so 730-1950 W/kg needs ~435-1160 Hz; zebrafish work loops measured only to 100 Hz. No data above 100 Hz found.",
      "satisfied_evidence": "derived",
      "note": "Mead et al. 2020 (abstract). Search scope: that abstract plus one search on zebrafish isolated-muscle work-loop power; no supra-100 Hz zebrafish data found. Extrapolation, not measurement."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Bilateral pectoral muscle mass of the subject species (zebrafish) must lie below the computed minimum fraction for hover",
      "quantity": "bilateral pectoral muscle mass / body mass", "lo": null, "hi": 7.5, "units": "% body mass",
      "status": "open",
      "satisfied_by": "Only measurement available is Abudefduf saxatilis (damselfish, labriform swimmer) 1.4% bilateral, carried from the claim and NOT verified here; no Danio rerio pectoral muscle mass found",
      "satisfied_evidence": "unknown",
      "note": "Species mismatch: number is A. saxatilis, claim is D. rerio, so open. Mansuit & Herrel 2021 Table 1 could-not-access (hal.sorbonne-universite.fr blocked; search found Mansuit et al. 2021 BJLS on Latimeria, listing). Thorsen & Westneat 2005 JMorph doi 10.1002/jmor.10173 (abstract) has labriform muscle masses, percentages not obtained. Thorsen & Hale 2005 and PMC5770327 describe adult zebrafish fin muscles without masses (search-summary). Scope: not-measured-as-far-as-searched, not looked-and-absent."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The minimum flight-muscle fraction for weight support, from independently measured maximum lift per unit flight muscle, must fall within the computed 7.5-20% threshold",
      "quantity": "minimum flight muscle fraction = g / (max lift per kg muscle)", "lo": 7.5, "hi": 20, "units": "% body mass",
      "status": "satisfied",
      "satisfied_by": "Marden 1987 maximum lift 54-63 N/kg flight muscle (72-86 N/kg clap-and-fling) gives 11.4-18.2%, inside the band; flight-muscle ratio of studied flyers 0.115-0.56",
      "satisfied_evidence": "literature",
      "note": "Marden 1987 JEB 130:235-258 (abstract/search-summary). Taxa are insects, birds, bats, not fish; used for the physics of aerial weight support, not a fish property. Fraction arithmetic is derived. At 1.4% the fish would need ~700 N/kg, 8-13x Marden's ceiling."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "Pectoral fin swept area must be small enough that actuator-disc induced power, sqrt((mg)^3/(2 rho A)), per unit pectoral muscle mass exceeds the cyclic muscle power ceiling (momentum flux must balance body weight)",
      "quantity": "pectoral fin swept area", "lo": null, "hi": null, "units": "mm^2",
      "status": "open",
      "satisfied_by": "No measured adult zebrafish pectoral fin area or swept area found; did not substitute a guessed area",
      "satisfied_evidence": "unknown",
      "note": "Searched zebrafish pectoral fin area/morphometrics: ZooKeys morphometric table gives fin lengths only, Danos & Lauder 2007 kinematics without area (search-summary). Closable by one measurement of adult fin span/area."}
  ]}
```
