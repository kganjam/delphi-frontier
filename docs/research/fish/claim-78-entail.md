# Claim 78: what it requires at the cell and organ scales

**Source claim (tissue scale, evidence: derived):** "Flapping requires a 5-15x enlargement
of the pectoral musculature. No zebrafish pectoral-muscle mass measurement was found in the
sources searched."

**Subject animal:** zebrafish (*Danio rerio*). Every number below is labelled with the animal
it comes from. No number from another species is used to refute anything here.

## Bottom line

- **No constraint is `unsatisfiable`.** I found no measured zebrafish value that contradicts the
  claim. The comparison numbers I did find come from birds, bats and *larval* zebrafish axial
  muscle, and none of them is about the subject (adult zebrafish pectoral muscle).
- **No constraint is `satisfied` outright.** The constraint about fibre power comes closest: a
  zebrafish muscle (larval tail, 5 dpf) does produce power in the range flying birds' pectoralis
  produces. But that is a different muscle at a different life stage, so I left it `open`.
- **The weak point is structural, not empirical.** A "5-15x" factor is a ratio:
  required muscle ÷ current muscle. The claim itself says the current zebrafish pectoral-muscle
  mass has not been measured. So the multiplier must have been obtained by dividing a required
  mass by an *assumed* baseline. *(This is my inference from the claim's wording. I have not seen
  the derivation.)* Constraints C1 and C4 cannot be checked until that baseline is measured.
  As far as I searched, **nobody has measured it**. That is different from "measured and found
  inconsistent".

## Sources and read-levels

None of the full texts below was read. Every entry is the abstract or snippet text that came
back from web search. The read-level for each one is stated, and the figures are quoted as the
search returned them.

| # | Source | Animal | Read-level |
|---|---|---|---|
| S1 | Mead et al. 2020, "Mechanical characteristics of ultrafast zebrafish larval swimming muscles", *Biophys. J.* 119(4):806-820 (bioRxiv 10.1101/2020.04.02.010298; NSF PAR 10377057) | zebrafish, 5 dpf larva, myotomal (tail) muscle | abstract (via search-summary) |
| S2 | Green, Ho & Hale 2011, "Movement and function of the pectoral fins of the larval zebrafish (*Danio rerio*) during slow swimming", *J. Exp. Biol.* (ZFIN ZDB-PUB-110901-13) | zebrafish larva | abstract (via search-summary) |
| S3 | Thorsen & Hale 2005, "Development of zebrafish (*Danio rerio*) pectoral fin musculature", *J. Morphol.* 266:241-255 (PMID 16163704) | zebrafish larva to adult | abstract (via search-summary) |
| S4 | Patterson, Mook & Devoto 2008, *Dev. Dyn.* (pectoral fin muscle growth) | zebrafish | search-summary (PDF listed, not opened) |
| S5 | SICB meeting abstract on adult zebrafish pectoral fin use (sicb.org/?p=34461) | adult zebrafish | search-summary |
| S6 | Askew & Marsh 2001, *J. Exp. Biol.* 204:3587, quail pectoralis power from work loops | blue-breasted quail | search-summary |
| S7 | Pigeon, starling and mallard in-vivo pectoralis power (Biewener and co-workers; *J. Exp. Biol.*; starling: *J. Exp. Biol.* 164:1) | birds | search-summary |
| S8 | Bat flight-muscle fraction 9-23 % of body mass (publish.csiro.au/ZO/ZO04036) | Western Australian bats | search-summary |
| S9 | Statements that pectoralis is roughly 8-11 % of bird body mass, can reach 20 %, and that <9 % is correlated with flightlessness (kiwis, rails, ducks). These came back in one search; I did **not** verify which of the returned papers (Auk 113:151; PMC3130450; jeb.205591) says which. | birds | search-summary, attribution unverified |

### Searches that found nothing (scope of the negatives)

- `zebrafish pectoral fin muscle abductor adductor mass adult`: no mass or volume measurement
  of any adult zebrafish pectoral fin muscle was returned. Only anatomy and development
  (S3, S4, Diogo et al. myology) came back. The full texts of S3, S4 and Diogo et al. were
  **not** opened, so a mass or volume table inside them has not been ruled out.
- `adult zebrafish pectoral fin beat frequency Hz kinematics`: no adult value was returned. S5
  reports that adults use the pectoral fins for maneuvering and hovering, and tuck them against
  the body during fast swimming. It gives no frequency.
- `flying fish Exocoetidae pectoral fin muscle mass percent body mass`: no value was returned,
  only fin-length and wing-loading morphometrics. I did not pursue this further, because a
  flying-fish number would be about the wrong animal for refuting this claim.

## Constraints

### C1 (organ, `range`): the enlarged pectoral muscle must land in the flapping-vertebrate band

*Requirement.* If flapping works after enlargement, the enlarged flight musculature should sit
inside the mass-fraction range that flapping vertebrates actually have. The bands found:
- Bats: 9-23 % of body mass (S8, measured, bats).
- Birds: pectoralis roughly 8-11 %, up to about 20 %. Below about 9 % is correlated with
  flightlessness (S9, birds, attribution unverified).

I take **9-23 % of body mass** as the band. *(This is my choice: it is the bat range, and its
lower end is the bird flightlessness threshold.)*

*Consequence (derived, my arithmetic).* For a 5-15x multiplier to land in that band, the current
adult zebrafish pectoral musculature must be between 9/15 = **0.6 %** and 23/5 = **4.6 %** of
body mass.

*Check.* The baseline fraction for adult zebrafish is **unknown**. The claim says so, and my
search (scope above) found no measurement either. **Status: open.** Nobody has looked, as far
as I searched. The bird and bat bands are a cross-species envelope for what the requirement
looks like. They are not a test of zebrafish.

### C2 (cell, `range`): pectoral fibres must deliver flapping-level cyclic power

*Requirement.* The muscle fibres must deliver net cyclic mechanical power in the range that
flapping flyers' pectoralis delivers. The measured bird values (S6, S7) are:
- pigeon: 51-70 W/kg in level flight, 119 W/kg at take-off;
- starling: 104 W/kg;
- mallard: 131 W/kg muscle in slow flight;
- quail: about 350 W/kg, more than 400 W/kg in some preparations. This value comes from work
  loops replaying in-vivo strain.

Lower bound used here: **about 50 W/kg** of muscle (pigeon level flight). The upper bound is
null, because the requirement is "at least".

*Check.* There is one zebrafish measurement. **Larval (5 dpf) myotomal tail muscle delivers
134 ± 20 W/kg at 80 Hz in work loops** (S1, measured, abstract). That is inside the bird band,
and shows that zebrafish muscle *can* reach this power level. It is a different muscle (axial,
not pectoral) at a different life stage (larva, not adult). S4 also reports that slow fibres
appear in the pectoral fin only at the juvenile stage, which suggests the pectoral fin's fibre
make-up changes with age. No adult zebrafish pectoral-fibre power measurement was found.
**Status: open.** The measurement supports the requirement (same species, wrong muscle and
stage) but does not satisfy it.

### C3 (cell, `timescale`): fibres must keep doing positive work at the flapping frequency

*Requirement.* The time for one activation-relaxation cycle must be short compared with the
flapping period. Otherwise the fibres cannot do net positive work at the flapping frequency.

*Check.* The claim does not state a required flapping frequency, so `lo` is null. I did not
invent one.
- Larval zebrafish pectoral fins beat at **28.2 ± 3.5 Hz** (S2, measured, larvae).
- Larval axial muscle does net-positive work at 80 Hz, with peak instantaneous power at 100 Hz
  (S1).

So, in larvae, the fibre timescale is not limiting up to about 80 Hz. No adult zebrafish fin-beat
frequency or adult pectoral-fibre kinetics were found (search scope above). **Status: open.**

### C4 (organ, `conservation`): the extra muscle mass must be accounted for

*Requirement.* The extra muscle mass, (k − 1) × M_pec,0 with k between 5 and 15, must come from
somewhere. There are two options:
- It is **added** to the body. Then the load on the fins rises, and the k that was derived must
  still hold once that extra load is included. In other words, k must be a self-consistent
  solution, not a one-pass estimate.
- It is **reallocated** from other tissue, such as axial muscle. Then the tissue that gives up
  mass, and the function that tissue loses, must be named.

*Check.* This cannot be evaluated without M_pec,0, the starting pectoral muscle mass, which is
unknown (see C1). I also could not tell whether the claim's derivation included the feedback
from added mass, because I have not seen the derivation. **Status: open.**

### C5 (cell, `existence`): a growth route must exist that can take pectoral muscle past normal allometry

*Requirement.* Some cellular growth mechanism, either adding fibres (hyperplasia) or enlarging
them (hypertrophy), must be able to grow the pectoral muscle 5-15x beyond its normal allometric
size.

*Check.* The normal growth mode is known: pectoral fin muscle grows **predominantly by
stratified hyperplasia, with no mosaic hyperplasia at any stage examined** (S4, search-summary).
Fibre number rises through the juvenile stage (S3). No study was found that pushes zebrafish
pectoral muscle beyond normal size by any means, genetic or training. *(Scope: only the searches
listed above. I ran no dedicated search for myostatin-type or other hypertrophy manipulations
of zebrafish fin muscle.)* **Status: open.** The normal mechanism exists. Whether it, or
anything else, can reach 5-15x has not been tested in anything I found.

## What would close these constraints

1. Measure adult zebrafish pectoral fin muscle mass, dissected and weighed or volumetric from
   micro-CT, as a fraction of body mass. One number moves C1 and C4 out of `open`. If it falls
   outside 0.6-4.6 %, C1 becomes `unsatisfiable` for the stated multiplier, and that would be a
   zebrafish-on-zebrafish refutation.
2. Run work-loop measurements on adult zebrafish pectoral fin muscle. These close C2 and C3.

```swarm-entail
{"source_claim": 78, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "After enlargement, pectoral flight musculature must fall within the body-mass fraction observed in flapping vertebrates; with a 5-15x factor this bounds the current pectoral muscle fraction to 0.6-4.6% of body mass",
      "quantity": "enlarged pectoral muscle mass / body mass", "lo": 9, "hi": 23, "units": "% body mass",
      "status": "open",
      "satisfied_by": "Not checkable: adult zebrafish baseline pectoral muscle mass is unmeasured. Searched 'zebrafish pectoral fin muscle abductor adductor mass adult' and found only anatomy/development (Thorsen & Hale 2005; Patterson et al. 2008; Diogo et al.), full texts not opened",
      "satisfied_evidence": "unknown",
      "note": "Band from bats 9-23% (publish.csiro.au ZO04036, search-summary) and birds <9% correlated with flightlessness (search-summary, attribution unverified). These are cross-species envelope numbers, not a zebrafish test. 0.6-4.6% is derived arithmetic. Negative is 'nobody has measured', not 'measured and failed'"},
    {"target_scale": "cell", "kind": "range",
      "statement": "Pectoral muscle fibres must deliver net cyclic mechanical power at least at the level flapping flyers' flight muscle delivers",
      "quantity": "net cyclic mass-specific power of muscle", "lo": 50, "hi": null, "units": "W/kg muscle",
      "status": "open",
      "satisfied_by": "Zebrafish larval (5 dpf) myotomal tail muscle: 134 +/- 20 W/kg at 80 Hz in work loops (Mead et al. 2020). Same species but different muscle and life stage. No adult zebrafish pectoral-fibre power measurement found",
      "satisfied_evidence": "measured",
      "note": "Mead et al. 2020 Biophys J 119:806 (abstract via search-summary). Bird band: pigeon 51-70 W/kg level flight and 119 W/kg take-off, starling 104, mallard 131, quail ~350-400 (Askew & Marsh 2001), all search-summary and all birds. Patterson et al. 2008: slow fibres appear in the pectoral fin only at the juvenile stage, so the larval axial value may not transfer"},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "The muscle activation-relaxation cycle must be short relative to the flapping period, so fibres do net positive work at the flapping frequency",
      "quantity": "highest cycle frequency with net positive work vs required flapping frequency", "lo": null, "hi": null, "units": "Hz",
      "status": "open",
      "satisfied_by": "Required flap frequency not stated by the claim. Larval zebrafish: pectoral fin beat 28.2 +/- 3.5 Hz (Green et al. 2011) and axial muscle net-positive work at 80 Hz (Mead et al. 2020). No adult zebrafish fin-beat frequency or pectoral kinetics found",
      "satisfied_evidence": "unknown",
      "note": "Searched 'adult zebrafish pectoral fin beat frequency Hz kinematics': adults use the fins for maneuvering/hovering and tuck them in fast swimming (SICB abstract, search-summary), no frequency reported. Larval values are abstract-level"},
    {"target_scale": "organ", "kind": "conservation",
      "statement": "The extra muscle mass must be either added (and the multiplier must be self-consistent with the extra load it creates) or reallocated from a named tissue",
      "quantity": "added pectoral muscle mass (k-1) x baseline mass", "lo": null, "hi": null, "units": "g",
      "status": "open",
      "satisfied_by": "Not checkable: baseline pectoral muscle mass is unknown, and the claim's derivation was not available to confirm whether it includes the added-mass feedback",
      "satisfied_evidence": "unknown",
      "note": "Depends on the same missing measurement as constraint 1. That the derivation may be a single pass is my inference from the claim's wording, not a finding"},
    {"target_scale": "cell", "kind": "existence",
      "statement": "A fibre-addition or fibre-enlargement growth route must exist that can take pectoral muscle 5-15x beyond its normal allometric size",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Normal growth mode known: predominantly stratified hyperplasia, no mosaic hyperplasia (Patterson, Mook & Devoto 2008), fibre number rising through the juvenile stage (Thorsen & Hale 2005). No study found that drives zebrafish pectoral muscle beyond normal size",
      "satisfied_evidence": "literature",
      "note": "Both sources search-summary/abstract only. I ran no dedicated search for genetic or training-based hypertrophy of zebrafish fin muscle, so the negative covers only the searches listed in the doc"}
  ]}
```
