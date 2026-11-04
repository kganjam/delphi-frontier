# Claim 77: what it requires at the cell and organ scales

**Source claim (tissue scale, evidence: derived):** "S10-D VERDICT STRENGTHENS: the measured
teleost pectoral-muscle fraction is ~1.4% of body mass for both fins (*Abudefduf saxatilis*,
0.69% per fin, Mansuit & Herrel 2021 Table 1, full text) against a computed threshold of
7.5-20%. Hover demand is 730-1950 W/kg, 5-15x above measured warm zebrafish fast muscle."

**Subject animal:** an adult zebrafish (*Danio rerio*) of 0.4 g fitted with a design wing of
semispan R = 2-4 cm. This is S10's hypothetical flapping fish (`S10-tissue.md`, branch
`claude/s10-tissue-flapping-power-2kag3x`). The 1.4% muscle fraction comes from a **damselfish**
(*Abudefduf saxatilis*, Pomacentridae). The 134.4 W/kg muscle benchmark comes from **larval
(5 dpf) zebrafish axial muscle**. Below, every number carries the animal it was measured in. No
number from another species is used to refute or confirm anything.

Inputs carried over from S10 (all assumptions or calculations, not observations): m = 0.4 g,
ρ = 1.2 kg/m³, k = 1.2, M = 1.5-2.0, R = 2-4 cm, design flap frequency ≈ 22 Hz (computed in
S10 §3c). The claim's own numbers were re-derived exactly in `challenge-77.md` (branch
`claude/challenge-s10-d-pectoral-muscle-vmlxc6`).

## Bottom line

- **No constraint is `unsatisfiable`.** I found no measured value about the subject that
  contradicts the claim.
- **Three constraints are `satisfied`:**
  - Cell energetic (C1). Measured zebrafish muscle parameters bound the work per cycle far below
    what 730 W/kg at 22 Hz needs.
  - Cell timescale (C2). Zebrafish fast muscle peaks in power well above 22 Hz, so the 80-Hz
    benchmark is not an underestimate.
  - Organ body-mass range (C4). The measured adult masses all lie in the band where the
    shortfall survives.

  Each `satisfied` rests on a zebrafish measurement. In C1 and C2 that measurement is **larval
  axial** muscle (plus one adult myofibril value), not adult pectoral muscle. I say so in each
  case.
- **Two constraints are `open`:**
  - The adult zebrafish pectoral-muscle fraction (C3). As far as I searched, nobody has measured
    it. Nobody has measured it and found it too high either.
  - The available wing semispan (C5). Adult zebrafish pectoral-fin length was not found.

## Sources and read-levels

| # | Source | Animal | Read-level |
|---|---|---|---|
| S1 | Mead AF, Kennedy GG, Palmer BM, Ebert AM, Warshaw DM (2020) Mechanical characteristics of ultrafast zebrafish larval swimming muscles. *Biophys J* 119:806-820. https://pmc.ncbi.nlm.nih.gov/articles/PMC7451861/ | zebrafish, 5 dpf larva, myotomal (axial) muscle, 28 °C | full-text (characters 0-100,000 of ~120,000, read through an automated summarising fetch; Figs 6G and 8D/E not seen) |
| S2 | Chevalier C, Denis C, Nedjar SA, Ledoré Y, Silvestre F, Schaerlinger B, Milla S (2024) Comparative study of the growth, stress status and reproductive capabilities of four wild-type zebrafish lines. *Biol Res* 57:67. doi:10.1186/s40659-024-00549-3. https://pmc.ncbi.nlm.nih.gov/articles/PMC11411999/ | zebrafish, wild-type AB/SJD/TU/WIK, 52-157 dpf | full-text (text only, via automated summarising fetch; per-line figures not seen) |
| S3 | Frontiers in Veterinary Science review, doi:10.3389/fvets.2020.590057: adult live weight "roughly 500-900 mg", length 22-38 mm | zebrafish | search-summary |
| S4 | J Gen Physiol article (figure URL rupress.org …jgp_201010568…, so doi presumably 10.1085/jgp.201010568; authors not verified): myofibrils from adult zebrafish skeletal white muscle, Fmax 18.4 ± 1.5 nN/µm² at 10 °C; larval myofibrils ~40 kPa | zebrafish, adult and larva, isolated myofibrils | search-summary (the search summary itself says the table's column layout was ambiguous) |
| S5 | Mansuit R, Herrel A (2021) *Front Ecol Evol* 9:702576, Table 1 | *Abudefduf saxatilis* (damselfish) | full-text in challenge-77 and replicate-77. I did not re-read it here (read-level for this doc: listing) |
| S6 | Gasteropelecidae pectoral muscle ~25% body mass (Wikipedia; ADW citing Hems 1983), as reported in challenge-77 | hatchetfish | search-summary (carried over) |

### Searches that found nothing (scope of the negatives)

1. `zebrafish pectoral fin adductor abductor muscle volume mass adult micro-CT percent body`
   (one standard web search).
   - **Result:** no zebrafish pectoral-muscle mass or volume was returned.
   - The nearest hit was Leyhr et al. 2023 (*Front Endocrinol*, synchrotron micro-CT of
     juvenile zebrafish). The search summary says it reports jaw-muscle volumes; I did not open
     it.
   - Upstream searches by S10-D, claim-78 and replicate-77 also found no measurement.
   - Combined scope: about four web searches plus ZFIN figure listings. No bibliographic
     database was searched, and no micro-CT repository (e.g. MorphoSource) was searched.
2. `adult zebrafish pectoral fin length mm morphometrics`,
   `"Danio rerio" pectoral fin length standard length ratio adult measured`,
   `adult zebrafish pectoral fin ray length mm regeneration pectoral fin size adult` (three
   standard web searches).
   - **Result:** no adult zebrafish pectoral-fin length in mm was returned.
   - One hit (PMC5523162, Table 4) gives pectoral-fin length ≈ 18-21% SL. I downloaded its
     full-text XML from Europe PMC and found that it is about ***Capoeta*** (a different
     cyprinid). I **discarded** it as the wrong animal.
3. `adult zebrafish fast skeletal muscle fibre specific force kPa isometric tension skinned or
   intact` (one standard web search).
   - **Result:** no adult intact-fibre or skinned-fibre specific force was found. Only the
     myofibril value S4 came back.

## Constraints

### C1 (cell, `energetic`): fibres must be unable to supply the generous-case work per cycle at the flap frequency

*Requirement.* The claim says the demand (≥ 730 W/kg muscle) is above what zebrafish fast muscle
can deliver. At S10's design frequency of ≈ 22 Hz, delivering 730 W/kg needs 730/22 =
**33 J/kg muscle per cycle**. The realistic end needs 1950/22 = **89 J/kg** (my arithmetic).
For the claim to be true, zebrafish fast fibres must not reach 33 J/kg per cycle at ~22 Hz.

*Check against measured zebrafish values:*
- **Measured work.** Net work is 2.63 ± 0.18 J/kg at 40 Hz (S1, larval zebrafish, 28 °C, 8%
  strain). That is 12.6x below 33 J/kg.
- **Derived ceiling.** I computed an upper bound for a rectangular work loop: stress × strain
  range ÷ density. With S1's measured larval isometric stress (76 ± 3 mN/mm²), its 8% strain
  and its assumed density of 1.06 g/cm³, the ceiling is **5.7 J/kg per cycle**. That equals
  126 W/kg at 22 Hz. Both numbers are calculations.
- **Strain needed to close the gap.** At 76 kPa, reaching 33 J/kg would need a strain range of
  **46%** (calculation).
- **Adult myofibrils.** S4 reports 18.4 kPa for adult zebrafish white-muscle myofibrils at
  10 °C (search-summary). That gives an even lower ceiling, 1.4 J/kg at 8% strain
  (calculation).

*Status: **satisfied**, evidence derived.* Each input is a zebrafish measurement. The limits
are:
- The muscle measured is larval axial muscle (and adult myofibrils), not adult pectoral fibres.
- The 8% strain is the protocol's choice, not a physiological maximum.
- *Inference, flagged as such:* adult fast muscle of other teleosts is commonly quoted at
  higher stress than 76 kPa. I have no measured adult-zebrafish whole-fibre stress. A stress of
  ~250 kPa would bring 33 J/kg within reach of a ~14% strain range. So this `satisfied` holds
  for the measured zebrafish preparations, and would need re-checking against an adult
  pectoral-fibre stress.

### C2 (cell, `timescale`): the fibre's power-optimal cycle frequency must lie at or above the flap frequency

*Requirement.* The claim's 5-15x shortfall divides demand at ~22 Hz by power measured at
**80 Hz**. That comparison is not biased against the fish only if the muscle's power optimum
is at or above 22 Hz. Power per cycle-time then falls toward 22 Hz rather than rising. The
same condition means relaxation must take less than the half-period, which is 1/(2·22) =
**22.7 ms**.

*Check (S1, larval zebrafish, 28 °C):*
- Measured power is 134.4 ± 19.9 W/kg at 80 Hz and 122.9 ± 11.1 W/kg at 100 Hz.
- Net work at 40 Hz is 2.63 J/kg, which gives **105 W/kg** (my calculation; the paper's own
  40-Hz power is in Fig. 8E, not seen).
- Power therefore rises from 40 to 80 Hz and falls by 100 Hz. The optimum lies between 40 and
  100 Hz, ≥ 1.8x the flap frequency.
- The twitch full width at half-maximal stress is **11 ± 1 ms**. Force returned to baseline
  within 25 ms.

*Status: **satisfied**, evidence measured* (for larval zebrafish axial muscle).
- *My inference:* power at 22 Hz is then probably below 105 W/kg, which makes the claim
  conservative. 20 Hz was not tested in S1, so the 22-Hz value itself is `unknown`.
- Adult pectoral-fin muscle kinetics were not found. If adult fibres are slow enough to peak
  below 22 Hz, this constraint would need re-checking. C1's work ceiling would still apply.

### C3 (organ, `range`): the subject's pectoral muscle mass must lie below the computed threshold

*Requirement.* "Shortfall" requires the adult zebrafish pectoral-muscle fraction to be below the
generous-case threshold of **7.5%** of body mass. Above that, 134.4 W/kg muscle would already
suffice in hover.

*Check.*
- The adult zebrafish value is **unknown** (search scope: negative #1 above).
- The 1.38% in the claim is a damselfish value. Two × 0.69% is derived; *A. saxatilis*,
  Pomacentridae, labriform swimmer (S5).
- The only other teleost value seen is hatchetfish ~25% (Gasteropelecidae, an otophysan like
  zebrafish; S6, search-summary). It sits on the other side of the threshold.
- Neither is about the subject. I do not average them: they bracket the threshold from below
  and above.

*Status: **open**.* Nobody has measured it, as far as I searched. This is the constraint the
whole claim rests on. Upstream S10-D (§3) already gives the measurement that would close it:
dissect and weigh the four pectoral-fin muscles in ~10 adults; 1% of a 0.4 g fish is 4 mg.

### C4 (organ, `range`): body mass must lie where the shortfall survives

*Requirement.* For fixed R, M and f, hover demand per kg of muscle scales as √m (actuator-disk
momentum balance; weight supported by downwash momentum flux). The generous-case 5.43x
shortfall closes only if m < 0.4 g / 5.43² = **0.014 g** (calculation). So the claim requires
adult zebrafish mass ≥ 0.014 g. It also requires S10's 0.4 g to sit within the measured adult
range, which keeps the quoted 730-1950 W/kg meaningful.

*Check (zebrafish):*
- 100 dpf males: AB 89 ± 24 mg, WIK 99 ± 36 mg, SJD 136 ± 38 mg (S2, full-text via fetch).
- 157 dpf adults of both sexes: 205-300 mg (S2).
- Adult live weight "roughly 500-900 mg" (S3, search-summary).

*Disagreement preserved:* the two sources differ by about 2-4x. S2 is a single facility on a
defined diet. S3 is a review value. 0.4 g lies between them, so it is not contradicted.
Re-scaling the generous case:
- at 0.089 g it gives 730·√(0.089/0.4) = **344 W/kg**, 2.6x over 134.4;
- at 0.9 g it gives **1095 W/kg**.

Both are calculations.

*Status: **satisfied**, evidence measured.* Every measured adult mass exceeds 0.014 g by ≥ 6x.

### C5 (organ, `spatial`): the available wing semispan must be well below the length that would close the gap

*Requirement.* At fixed mass, hover power ∝ 1/R. The generous-case shortfall (5.43x at
R = 4 cm) closes only for a semispan ≥ 4 cm × 5.43 = **21.7 cm** (calculation). For the claim
to be true, any wing the fish carries must be shorter than ~22 cm. The claim's R = 2-4 cm must
also not understate the real wing, otherwise the demand is overstated.

*Check.*
- Adult zebrafish pectoral-fin length was **not found** (negative #2; the one ratio returned was
  *Capoeta* and was discarded).
- Body length is the only zebrafish size I have:
  - SL 18.4 ± 2.6 and 20.7 ± 2.9 mm at 110 dpf (S2; the second line label is ambiguous in the
    text);
  - 22-38 mm (S3, search-summary).
- *Inference, not measurement:* a natural pectoral fin is shorter than the body, so the real fin
  is ≪ 2 cm. The claim's 2-4 cm design semispan therefore already overstates the natural wing,
  and the real demand is higher (replicate-77 computes 1.6-12 × 10³ W/kg for 4-8 mm fins).
- A side note: S10's "4 cm" body is at or above the top of the measured length range (S2, S3).

*Status: **open**.* No measured fin length was found. The fish's measured body length is 6-12x
below the 22 cm closing value, but turning body length into a fin-length bound is my inference.

## What would change these verdicts

- **A dissection of adult zebrafish pectoral muscle above 7.5% of body mass** would make C3
  `unsatisfiable` and refute the claim from below. A value below ~1.4% would satisfy it.
- **An adult zebrafish pectoral (or fast axial) fibre work loop at ~20 Hz, 28 °C**, would
  replace the larval proxy in C1 and C2. Reaching C1's 33 J/kg would refute the claim.

```swarm-entail
{"source_claim": 77, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "energetic",
      "statement": "Fast flight-muscle fibres must be unable to deliver the net work per cycle that the generous hover demand requires at the flap frequency (730 W/kg / 22 Hz)",
      "quantity": "net mechanical work per cycle per kg muscle at ~22 Hz", "lo": null, "hi": 33, "units": "J/kg muscle per cycle",
      "status": "satisfied",
      "satisfied_by": "Larval zebrafish myotomal muscle: measured 2.63 J/kg at 40 Hz, 28 C; derived rectangular-loop ceiling from measured larval stress 76 kPa x 8% strain / 1.06 g/cm3 = 5.7 J/kg (126 W/kg at 22 Hz); 33 J/kg would need 46% strain. Adult zebrafish myofibril Fmax 18.4 kPa at 10 C gives an even lower ceiling",
      "satisfied_evidence": "derived",
      "note": "Mead et al. 2020 Biophys J 119:806 (full-text, partial, larval zebrafish); J Gen Physiol doi 10.1085/jgp.201010568 adult zebrafish myofibrils (search-summary, column ambiguity). Same species but not adult pectoral fibres; an adult whole-fibre stress ~250 kPa (not measured in zebrafish, my inference from other teleosts) would loosen the bound to ~14% strain, so re-check against adult pectoral fibres"},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "The fibre's power-optimal cycle frequency must lie at or above the flap frequency, and relaxation must be shorter than the half-period, so that a benchmark measured at 80 Hz does not underestimate power at ~22 Hz",
      "quantity": "power-optimal work-loop frequency", "lo": 22, "hi": null, "units": "Hz",
      "status": "satisfied",
      "satisfied_by": "Larval zebrafish axial muscle, 28 C: 105 W/kg at 40 Hz (derived from measured 2.63 J/kg), 134.4 W/kg at 80 Hz, 122.9 W/kg at 100 Hz (measured), so optimum between 40 and 100 Hz; twitch FWHM 11 +/- 1 ms vs 22.7 ms half-period",
      "satisfied_evidence": "measured",
      "note": "Mead et al. 2020 (full-text, partial; 20 Hz not tested, so power at 22 Hz itself is unknown). Larval axial, not adult pectoral; adult pectoral kinetics not found in what I searched"},
    {"target_scale": "organ", "kind": "range",
      "statement": "The subject's pectoral muscle mass fraction (both fins) must lie below the computed generous-case threshold at which measured warm fast muscle would suffice for hover",
      "quantity": "adult zebrafish pectoral muscle mass / body mass", "lo": null, "hi": 7.5, "units": "% body mass",
      "status": "open",
      "satisfied_by": "No adult zebrafish measurement found. Searched 'zebrafish pectoral fin adductor abductor muscle volume mass adult micro-CT percent body' (1 web search; nearest hit Leyhr et al. 2023 juvenile micro-CT, jaw muscles, not opened), plus upstream S10-D/claim-78/replicate-77 searches (~3 more). Cross-species only: Abudefduf saxatilis 1.38% (damselfish) and Gasteropelecidae ~25% (hatchetfish)",
      "satisfied_evidence": "unknown",
      "note": "Mansuit & Herrel 2021 Table 1 (full-text upstream; listing here), hatchetfish via Wikipedia/ADW (search-summary). Neither species is the subject; they bracket the threshold and are not averaged. Negative = nobody has measured, not measured-and-failed. No bibliographic database or micro-CT repository searched"},
    {"target_scale": "organ", "kind": "range",
      "statement": "Body mass must lie where the hover shortfall survives; per-kg-muscle demand scales as sqrt(m) by momentum balance, so the generous 5.43x gap closes only below 0.4 g / 5.43^2",
      "quantity": "adult zebrafish body mass", "lo": 0.014, "hi": null, "units": "g",
      "status": "satisfied",
      "satisfied_by": "Measured wild-type zebrafish: 89-136 mg (100 dpf males, AB/WIK/SJD) and 205-300 mg (157 dpf) (Chevalier et al. 2024); 500-900 mg adult live weight (review). Re-scaled generous demand 344 W/kg at 0.089 g, 1095 W/kg at 0.9 g (calculation), still above 134.4 W/kg",
      "satisfied_evidence": "measured",
      "note": "Chevalier et al. 2024 Biol Res 57:67 (full-text text only via fetch); Front Vet Sci doi 10.3389/fvets.2020.590057 (search-summary). Sources disagree 2-4x; preserved, not averaged; S10's 0.4 g lies between"},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "The wing semispan actually available must be far below the length at which hover power (proportional to 1/R) would fall to the measured muscle benchmark, and the claim's 2-4 cm must not understate the real wing",
      "quantity": "pectoral fin / wing semispan", "lo": null, "hi": 21.7, "units": "cm",
      "status": "open",
      "satisfied_by": "Adult zebrafish pectoral fin length not found (3 web searches; one 18-21% SL ratio returned was Capoeta, verified from full-text XML and discarded). Only body length known: SL 18.4-20.7 mm at 110 dpf (Chevalier et al. 2024), 22-38 mm (review). That the fin is shorter than the body is my inference, not a measurement",
      "satisfied_evidence": "unknown",
      "note": "21.7 cm = 4 cm x 5.43 (calculation). If the inference holds, the real fin is << 2 cm and the claim's demand is an underestimate (replicate-77: 1.6-12e3 W/kg for 4-8 mm fins). S10's assumed 4 cm body is at or above the top of the measured range"}
  ]}
```
