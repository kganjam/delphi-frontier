# Claim 95: what it requires at the tissue and organism scales

**Source claim (organ scale, evidence: derived).** S6 and S26 compared the EI of a 40.3 mm
bluegill (*Lepomis macrochirus*) pectoral fin ray (3.8e-6 N m^2) with the requirement for a
120 mm ray (6.3e-4 N m^2). With isometric L^4 scaling the passive EI becomes 3.0e-4, so the gap
is 2.1x, not the 165x that was reported.

**Arithmetic re-check (derived, done here, not an observation).** (120/40.3)^4 = 78.6;
3.8e-6 x 78.6 = 2.99e-4 N m^2; 6.3e-4 / 2.99e-4 = 2.11; and 6.3e-4 / 3.8e-6 = 165.8, which is the
unscaled ratio. The claim's arithmetic is correct *given its inputs*. Everything below is about
those inputs and the assumptions behind the scaling.

**What I could not access.** S6 and S26 are not in this repository, so I could not tell which
animal the 6.3e-4 N m^2 requirement was derived for, or what load case it uses. Full-text fetches
failed because these hosts are outside the session's network allowlist: `sites.harvard.edu`,
`deepblue.lib.umich.edu`, `pubmed.ncbi.nlm.nih.gov` and `public.websites.umich.edu`. As a result
every literature source below was read at **search-summary** level unless stated otherwise.

---

## Constraints

### C1 · tissue · range: the input passive EI of the bluegill ray

*Requirement.* For the 2.1x gap to stand, the passive flexural rigidity of a ~40 mm bluegill
pectoral ray must actually be about 3.8e-6 N m^2. The window is a factor of 2 either side,
[1.9e-6, 7.6e-6] N m^2. Below the window the gap grows past ~4x. Above about 8e-6 the scaled
passive ray meets the requirement.

*Check: **open**, because the two sources disagree by 149x for the same species.*

- **Animal on both sides: bluegill.** Flammang, Alben, Madden & Lauder (2013), *J. Morphol.*
  274:1044–1059, doi:10.1002/jmor.20161 (read-level: **search-summary** of the abstract). They report
  that the "flexural stiffness of the fin ray was calculated to be 565 × 10^-6 N m^2" for the
  third left pectoral ray of six bluegill. That is 148.7x the claim's 3.8e-6.
- If 565e-6 is the right number for a comparable ray, then 565e-6 x 78.6 = 4.4e-2 N m^2
  (derived). That would be a **~70x surplus** over the requirement, not a 2.1x deficit, and the
  claim would be refuted from below.
- **Why this is not marked `unsatisfiable`.** The reasons are about evidence quality, not about
  the claim being ours. (i) The paper says the value was *calculated*, and I could not see from
  what. It may be model-fitted rather than a direct bending measurement. (ii) The search tool noted
  that the PDF text layer is garbled at this number ("565 3 1026 Nm2"), so I have not confirmed the
  exponent against the typeset page. (iii) The paper's ray length is unknown to me, so I cannot
  confirm it is comparable to the 40.3 mm ray. (iv) I do not know where S6/S26's 3.8e-6 comes from.
- **Order-of-magnitude cross-check (derived, not measured).** Treat the ray as a solid circular
  rod with E = 1.34 GPa. That is the mean proximal fin-ray modulus reported in Lauder et al. 2011
  (*Smart Mater. Struct.*, read-level: search-summary), with a range of 0.24–3.7 GPa. EI = 3.8e-6
  then needs a diameter of about 0.49 mm, and EI = 565e-6 needs about 1.71 mm. I found no measured
  bluegill ray basal diameter, so this cross-check cannot settle which value is right. It only shows
  that the two numbers imply very different ray thicknesses.
- **Also relevant (bluegill, search-summary).** Alben, Madden & Lauder (2007), *J. R. Soc.
  Interface* 4:243 (PMC2359861). Ray stiffness varies by more than an order of magnitude depending on
  how the base is actuated. A "passive EI" therefore depends on the boundary condition, and the two
  numbers may come from different boundary conditions. This is my inference, not something either
  paper states.

**This is the highest-priority item.** Reading the full text of Flammang et al. 2013 (methods and
the stiffness table) should settle C1, and it would turn the verdict either to `satisfied` or to
`unsatisfiable`.

### C2 · tissue · range: bone modulus must not change with size

*Requirement.* L^4 isometric scaling assumes the same Young's modulus in a 40 mm and a 120 mm ray.
For the 2.1x figure to be meaningful within a factor of 2, the modulus ratio E(120 mm ray) /
E(40.3 mm ray) must lie in [0.5, 2.0]. A ratio of 2.1 or more on its own closes the gap.

*Check: **open**. No measurement of modulus against body size was found.*

- Search scope: "fin ray lepidotrichia Young's modulus scaling fish size / allometry". There were
  no hits reporting modulus against body length, or an allometric exponent, in any species. This
  means **nobody appears to have measured it**, not that someone looked and found invariance.
- The spread across rays within a fin is far wider than the factor-2 window. Lauder et al. 2011
  (species set limited; read-level: search-summary) report proximal moduli of 0.24–3.7 GPa (15x)
  and distal moduli of 0.11–0.67 GPa. Separately, a SICB abstract on labriform wrasses reports that
  most stiffness variation came from the second moment of area I, not from E (search-summary).
- The animal for the 120 mm side is unknown (see C4), so even a measured cross-size modulus would
  have to be for that animal.

### C3 · tissue · spatial: ray cross-section must scale with ray length

*Requirement.* The L^4 law also assumes that ray diameter scales with ray length. The gap
conclusion (passive EI is too low) holds only if the 120 mm ray's effective diameter is less than
2.1^(1/4) = 1.20x the isometric prediction. That prediction is 2.98x the 40.3 mm ray's diameter.
A 20% positive allometry in thickness closes the gap entirely (derived).

*Check: **open**.*

- I searched flying-fish fin-ray morphology. Taxonomic accounts on Plazi (read-level: **listing**)
  give first-pectoral-ray *lengths* for *Cypselurus starksi* (2.4–2.8 in SL),
  *C. clariangulatus* (2.60–2.95 in SL at 128–153 mm SL) and *Cheilopogon spilopterus* (2.2–2.8 in
  SL). They give no diameters or second moments of area. The accounts also disagree on whether the
  first ray lengthens with growth (*C. starksi*) or stays proportionally constant
  (*Ch. spilopterus*). I am keeping that disagreement rather than averaging it away.
- I found no measured ray diameter for either bluegill or any exocoetid. **Not looked at in the
  literature I could reach**, which is different from "found isometric."
- My inference, not a measurement: a ±20% departure from isometry is small compared with the
  15x modulus spread in C2. The 2.1x gap therefore sits inside the uncertainty of the scaling
  assumption and should be reported as "within a factor of a few", not as a sharp number.

### C4 · organism · spatial: the 120 mm target must be a real ray of the intended animal

*Requirement.* The 120 mm ray length must match the pectoral-fin ray length of the organism for
which the 6.3e-4 N m^2 requirement was derived, within a factor of 1.5 (ratio in [0.67, 1.5]).

*Check: **open**, because the target animal is not stated in the claim and S6/S26 are not available.*

- **If the target is an exocoetid, the requirement is consistent.** Park & Choi (2010), *J. Exp.
  Biol.* 213:3269–3279, on *Cypselurus hiraii* (read-level: search-summary of the paper and a
  morphology table) report standard lengths of about 199–209 mm and wing spans of 233–261 mm. That
  makes each pectoral fin about 115–130 mm long from midline to tip, minus the body half-width.
  This is my derivation, not their statement. A 120 mm ray fits.
- **If the target is a zebrafish, the requirement is not consistent.** I did not retrieve a sourced
  measurement of adult zebrafish standard length or pectoral ray length (search: "adult zebrafish
  standard length pectoral fin length lepidotrichia"; it returned staging-paper definitions only, no
  numbers). I am not quoting a number. If, as is generally expected, adult zebrafish are a few
  centimetres long, then a 120 mm ray would be longer than the whole fish. That would put the
  requirement far outside the C4 window and change the scaling factor completely.
- **Animal on each side.** The input ray is bluegill. The 120 mm length matches exocoetid
  morphology. Whether the project's zebrafish is the intended target is unknown. This comparison
  crosses species on purpose, so it can only feed an `open` verdict, never a refutation.

### C5 · organism · existence: something must close the remaining 2.1x

*Requirement.* If the claim is right that passive EI falls about 2.1x short, then an animal that
uses a 120 mm ray under the S6/S26 load must have a mechanism that adds at least 2.1x effective
stiffness over passive. Examples include active basal actuation of the ray, fin curvature, or
membrane tension.

*Check: **open** for the target animal. A mechanism with enough range is documented in other species.*

- **Bluegill** (Alben, Madden & Lauder 2007, read-level: search-summary of the abstract): actuating
  the ray base varies ray stiffness "over more than an order of magnitude". Alben & McGee (2010,
  *J. Mech. Phys. Solids*, search-summary) cite 10–100x increases in effective bending modulus with
  the ray base clamped. A SICB abstract on *Lepomis macrochirus* reports a stiffness range of nearly
  two orders of magnitude across rays. That abstract is a different study from the 2007 paper, so
  I am keeping its figures separate.
- **Mackerel** (*Scomber japonicus*): arXiv:1608.05891 ("Curvature-induced stiffening of a fish fin") (read-level: **abstract**)
  show that fin curvature modulates whole-fin stiffness. No numeric factor appears in the abstract.
- Neither measurement is for an exocoetid or a zebrafish. They show that a mechanism with more
  than 2.1x range **exists in ray-finned fishes**. They do not show that the target animal has it.

### Not checked
- **Conservation (momentum, organism).** The 6.3e-4 requirement should follow from lift = weight
  spread over the fin, plus a deflection limit. I could not check it: S6/S26's load case is
  unavailable, and Park & Choi's body masses were not in the snippets I could read. Status:
  `open`, not included as a constraint.

---

## Summary

The arithmetic correction in claim 95 is correct given its inputs. Its conclusion (a 2.1x
*deficit*) depends on three inputs that none of the literature I could reach confirms:

1. **The input EI (C1).** A same-species source (Flammang et al. 2013, bluegill) reports a value
   149x higher. If that holds for a comparable ray, the deficit becomes a ~70x surplus. That would
   be a refutation from below, but it is not one yet: the source was read only at search-summary
   level, it is "calculated", its exponent is OCR-garbled, and its ray length is unknown.
2. **Size-invariant modulus and isometric thickness (C2, C3).** Nobody appears to have measured
   either. The documented within-fin spread in modulus (15x) is larger than the gap itself.
3. **The animal behind the 120 mm requirement (C4).** It fits an exocoetid, not a zebrafish.

Nothing reached `unsatisfiable`, and nothing was marked `satisfied` on plausibility.

## Sources (read-level)
- Flammang, Alben, Madden & Lauder 2013, *J. Morphol.* 274:1044, doi:10.1002/jmor.20161: **search-summary** (full text could-not-access, host blocked).
- Alben, Madden & Lauder 2007, *J. R. Soc. Interface* 4:243, PMC2359861: **search-summary**.
- Alben & McGee 2010, "Optimizing a fin ray for stiffness", *J. Mech. Phys. Solids*: **search-summary**.
- Lauder et al. 2011, *Smart Mater. Struct.* (fin ray moduli): **search-summary**.
- arXiv:1608.05891, "Curvature-induced stiffening of a fish fin" (authors not retrieved): **abstract**.
- Park & Choi 2010, *J. Exp. Biol.* 213:3269: **search-summary**.
- Plazi treatments of *Cypselurus starksi*, *C. clariangulatus*, *Cheilopogon spilopterus*: **listing**.
- SICB meeting abstracts (wrasse fin-ray I vs E; *Lepomis* ray stiffness range): **search-summary**.
- Tangorra et al. 2010, *J. Exp. Biol.* 213:4043: **search-summary**. It gave no EI values, so it is not used for any number.

```swarm-entail
{"source_claim": 95, "source_scale": "organ",
  "constraints": [
    {"target_scale": "tissue", "kind": "range",
      "statement": "The passive flexural rigidity of a ~40 mm bluegill pectoral fin ray (the input to the scaling) must lie near the value used, within a factor of 2, for the 2.1x gap to stand",
      "quantity": "passive EI of a 40.3 mm bluegill pectoral ray", "lo": 1.9e-6, "hi": 7.6e-6, "units": "N m^2",
      "status": "open",
      "satisfied_by": "Same-species conflict: Flammang et al. 2013 report a calculated 565e-6 N m^2 for the bluegill third pectoral ray, 149x the 3.8e-6 used. Scaled by 78.6 that would give a ~70x surplus. Not marked unsatisfiable because the value is 'calculated', its exponent is OCR-garbled in the search snippet, its ray length is unknown, and the full text could not be accessed",
      "satisfied_evidence": "literature",
      "note": "Flammang, Alben, Madden & Lauder 2013 J Morphol 274:1044 doi:10.1002/jmor.20161 (search-summary; full text blocked by the network allowlist). Bluegill on both sides. Derived cross-check: at E=1.34 GPa a solid rod needs d~0.49 mm for 3.8e-6 and ~1.71 mm for 565e-6; no measured diameter found. Source of S6/S26's 3.8e-6 unknown"},
    {"target_scale": "tissue", "kind": "range",
      "statement": "The Young's modulus of fin-ray bone must be roughly the same in a 40 mm and a 120 mm ray, as isometric L^4 scaling assumes",
      "quantity": "E(120 mm ray) / E(40.3 mm ray)", "lo": 0.5, "hi": 2.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No measurement of lepidotrichial modulus against body size was found in any species. The within-fin spread of 0.24-3.7 GPa proximal and 0.11-0.67 GPa distal is wider than the window",
      "satisfied_evidence": "unknown",
      "note": "Searched 'fin ray lepidotrichia Young's modulus scaling fish size allometry': no size-series data, so not measured rather than found invariant. Lauder et al. 2011 Smart Mater Struct (search-summary) for the moduli; limited species set"},
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "Ray cross-section must scale with ray length: the 120 mm ray's effective diameter must be less than 1.20x the isometric prediction, or the passive gap closes",
      "quantity": "d_120 / (2.98 * d_40.3)", "lo": null, "hi": 1.2, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No measured fin-ray diameters or second moments of area found for bluegill or any exocoetid. Exocoetid first-ray lengths are known (2.2-2.95 in SL) but not thicknesses",
      "satisfied_evidence": "unknown",
      "note": "Plazi treatments of Cypselurus starksi, C. clariangulatus, Cheilopogon spilopterus (listing); they disagree on whether the first ray lengthens with growth. Diameter scaling not found in the literature reached; not shown to be isometric"},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "The 120 mm target ray length must match, within a factor of 1.5, the pectoral ray length of the organism for which the 6.3e-4 N m^2 requirement was derived",
      "quantity": "120 mm / actual pectoral ray length of target organism", "lo": 0.67, "hi": 1.5, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Consistent with an exocoetid: Cypselurus hiraii SL ~199-209 mm and span 233-261 mm give ~115-130 mm per fin (derived). Not consistent with an adult zebrafish if it is a few cm long, but no sourced zebrafish fin length was retrieved. The target animal is not stated in the claim, and S6/S26 are not in the repo",
      "satisfied_evidence": "derived",
      "note": "Park & Choi 2010 J Exp Biol 213:3269 (search-summary), exocoetid. Zebrafish search ('adult zebrafish standard length pectoral fin length lepidotrichia') returned no numbers. Cross-species comparison, so open, not a refutation"},
    {"target_scale": "organism", "kind": "existence",
      "statement": "A mechanism must exist in the target animal that raises effective fin-ray stiffness by at least 2.1x over passive",
      "quantity": "active/passive effective stiffness ratio", "lo": 2.1, "hi": null, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Shown in other species only: bluegill basal hemitrich actuation varies ray stiffness by more than 10x (Alben et al. 2007), 10-100x with the base clamped (Alben & McGee 2010). Mackerel fin curvature stiffens the fin (arXiv:1608.05891, no factor in abstract). Nothing found for an exocoetid or zebrafish",
      "satisfied_evidence": "literature",
      "note": "Alben, Madden & Lauder 2007 J R Soc Interface 4:243 PMC2359861 (search-summary); Alben & McGee 2010 JMPS (search-summary); arXiv:1608.05891 (abstract). Bluegill and mackerel are not the target animal, so not satisfied for the target"}
  ]}
```
