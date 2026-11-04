# Claim 95: what it requires at the tissue and organism scales

**Source claim (organ scale, evidence: derived).** S6 and S26 compared the flexural rigidity (EI) of a
40.3 mm bluegill (*Lepomis macrochirus*) pectoral fin ray, 3.8e-6 N m^2, with the requirement for a
120 mm ray, 6.3e-4 N m^2. Under isometric L^4 scaling the factor between them is 78.6. That makes the
scaled passive EI 3.0e-4 N m^2, so the gap is 2.1x, not the 165x reported.

**Status of this document.** Literature and arithmetic only. Nothing here was measured by me. Each
number is tagged *measured* (by the cited authors), *calculated* (by me, `python3 -I`; the
inputs are given beside each result) or *assumption*.

## 0. Upstream provenance (read from repository branches, read-level full-text)

- **S6-D** (`origin/claude/deepen-fin-ray-s6-cj2i2x:docs/research/fish/S6-deepen.md`, §1, read). The
  requirement EI_req = 6.3e-4 N m^2 is **calculated** from four **assumptions**: body mass m = 0.10 kg,
  N = 14 load-bearing rays per fin, ray span L = 0.12 m, and load factor n = 1. The failure criterion
  is δ/L > 0.10 for a uniformly loaded cantilever. S6-D says the requirement is **not a measurement of any
  flying fish**. It is a 100 g, exocoetid-sized scenario. It is not a zebrafish.
- **S26-D** (`95578def:docs/research/fish/S26-deepen.md`, read). The 3.8e-6 is Puri et al. 2018 relaying
  Flammang et al. 2013 for bluegill. The 40.3 mm length is Alben et al. 2007's group-maximum ray length,
  measured on a *different* set of bluegill.
- **replicate-95** (`0ad5eb19`, read). It agrees on the 78.6 arithmetic, and notes that nobody has shown the
  40.3 mm length belongs to the ray behind 3.8e-6.
- **A parallel entailment of this same claim** exists at `origin/claude/claim-95-entail-p91b6z`
  (commit `228b9ae7`; I read it before writing this one). I reuse none of its verdicts without re-checking them. Where I
  reach a different reading, I say so below. The main new evidence here is Puri et al. 2018, which I read in
  full text. That paper did not appear in the parallel document.

**Arithmetic re-check (calculated).** (120/40.3)^4 = 78.61. 3.8e-6 × 78.61 = 2.99e-4 N m^2.
6.3e-4 / 2.99e-4 = 2.11. The unscaled ratio is 6.3e-4 / 3.8e-6 = 165.8. The claim's arithmetic is right
for its inputs.

**A consequence the claim does not state (calculated, conditional on joint isometry).** EI_req ∝ m·L^2/N
(S6-D's model). If mass scales isometrically (m ∝ L^3) and EI_passive ∝ L^4 at constant E, then
EI_req / EI_passive ∝ L. **The gap is therefore not a property of the ray type. It depends on size**:
0.71x at 40.3 mm, 1.05x at 60 mm, 2.11x at 120 mm and 3.5x at 200 mm. The "2.1x" holds only at the
single size S6-D assumed. This is my derivation from S6-D's equations. No author has claimed it.

---

## Constraints

### C1 · tissue · range: the passive EI of the ~40 mm bluegill ray being scaled

*Requirement.* The 2.1x figure stands, within a factor of 2, only if the passive flexural rigidity of a
~40 mm bluegill pectoral ray lies in **[1.9e-6, 7.6e-6] N m^2**. Above about 8e-6, the scaled passive ray
already meets the requirement.

*Check: **open**. Bluegill is on both sides, and the same-species sources disagree.*

| Source (all bluegill) | Value | What it is | Read-level |
|---|---|---|---|
| Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861 | EI ≈ 1e-6 to 1e-5 N m^2 | measured, three-point bending of excised rays (relayed by S26-D). The base condition is not stated | full-text via summarizer, *as relayed by S26-D*; I did not re-read it |
| S26-D back-calculation from Alben's 1.98 N/m point stiffness | 1.07e-6 (one hemitrich free) to 1.28e-5 (clamped) | calculated by S26-D, assuming L = 40.3 mm | full-text (repo) |
| Puri et al. 2018, *J Exp Biol* 221:jeb171777, PMC5868929 | 3.8e-6 N m^2 | **relay** of Flammang 2013 in the Discussion. No specimen length or method is given | **full-text** (Europe PMC XML, read directly by me) |
| Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161 | 565e-6 N m^2 | "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2". The context is an **in-vivo** vortex-jet perturbation | **abstract** (Europe PMC REST, read directly). Full text **could-not-access**: Wiley returns 403, and sites.harvard.edu is outside this session's network allowlist |

- The window [1.9e-6, 7.6e-6] sits *inside* Alben's 1e-6 to 1e-5 range. But that range is wider than the
  window, and its base condition is unstated. So Alben does **not** pin the value into the window. That is
  why this is not `satisfied`.
- **Why 565e-6 does not make this `unsatisfiable`.** It is a measurement on the same species, but it is
  probably **not the same quantity**. It is "calculated" from an in-vivo perturbation of a fin under muscular
  control, whereas the constraint concerns a *passive* ray. I add two checks of my own. Both are
  inferences, not author statements:
  1. *Internal consistency (calculated).* The abstract's own numbers are an impact force of 67 mN and a
     peak curvature of 9.38 mm^-1. Put the force at the tip of a 40.3 mm ray (an upper bound on moment
     arm, giving M ≤ 2.7e-3 N m) and apply linear beam theory, EI = M/κ. That gives EI ≤ 2.9e-7 N m^2,
     about 2000x below 565e-6. A curvature of 9.38 mm^-1 is a local buckle, so linear theory may not
     apply. The check therefore shows that 565e-6 **cannot be recovered from the abstract alone**. It does
     not show that 565e-6 is wrong.
  2. *Cross-species scaling test (calculated from Puri's numbers; the species differ).* Puri et al.
     measured **zebrafish** caudal fins in vivo and found whole-fin EI = **1.5e-9 to 4e-9 N m^2**. This is
     measured, zebrafish, full-text. They scaled the bluegill value by ray diameter^4 and stated that it is
     "in reasonable agreement". Their inputs were bluegill rays 1–2 mm across, zebrafish rays 0.1–0.2 mm,
     and 16–18 rays per fin. Redoing that route, I get 3.8e-6 × 1e-4 × 16–18 = 6.1e-9 to 6.8e-9, which
     is 1.5–4.5x above the zebrafish measurement. (The authors give 2e-9 to 5e-9 for this step. I could
     not reproduce that from the inputs they state, and I keep that discrepancy as it stands.) The same
     route applied to 565e-6 gives 0.9e-6 to 1.0e-6, which is **230–680x** above the zebrafish
     measurement. **Under d^4 scaling, the zebrafish data favour 3.8e-6 over 565e-6.** This crosses
     species (bluegill → zebrafish), so it is evidence and not a refutation.
- The specimen length behind 3.8e-6 remains `unknown`. If that ray was shorter than 40.3 mm, the scale
  factor rises: 256 at 30 mm (calculated by replicate-95). The gap could then vanish. This sensitivity
  lies outside the EI window but bears directly on the claim.

### C2 · tissue · range: fin-ray modulus must not change with size

*Requirement.* L^4 scaling assumes the same effective Young's modulus at 40 mm and 120 mm. The 2.1x
figure is meaningful within a factor of 2 only if **E(120 mm ray) / E(40.3 mm ray) ∈ [0.5, 2.0]**.
A ratio of 2.1 or more closes the gap on its own.

*Check: **open**. I found no size series in any species. "Not measured" is distinct from "measured and invariant".*

- Search scope: Europe PMC query `"fin ray" (stiffness OR flexural) (allometry OR "body size" OR ontogeny OR scaling)`
  (25 hits, titles screened; none was a size series). A web search on "fin ray lepidotrichia diameter scaling
  body size ontogeny allometry flexural stiffness" returned SICB abstracts on gar, sturgeon, coho and wrasse,
  all inter-fin or interspecific (search-summary). Not searched: Web of Science, Google Scholar, and
  theses behind blocked hosts. Aiello's University of Chicago dissertation came up in the results but its host
  (uchicago.cottagelabs.com) is blocked, so it is **could-not-access**.
- Indirect, cross-species support, not a size series:
  - Aiello et al. 2018, *J Morphol*, doi:10.1002/jmor.20830 (**abstract**). Two labrids with
    "similarly sized fins": "segmentation patterns and E were similar between species", and "variation in
    I always explained the majority of the variation in flexural stiffness". This holds E roughly fixed
    while *species* changes, not *size*.
  - Puri et al. 2018 (above). EI ∝ d^4 at constant E carries bluegill → zebrafish across roughly 10x in
    diameter to within 1.5–4.5x (my recalculation) or "reasonable agreement" (the authors' words). This is
    a downward extrapolation, on a relayed input, across species.
- Within-fin spread is larger than the window: Aiello et al. 2018, *J Exp Biol* 221:jeb163360
  (**abstract**) give labrid ray EI of 0.0001–1.5109 µN m^2 (1e-10 to 1.5e-6 N m^2) along and across a
  single fin. Most of that spread is attributed to I, not E.

### C3 · tissue · spatial: ray cross-section must scale in proportion to ray length

*Requirement.* Isometry gives d_120 = 2.98 × d_40.3. The deficit conclusion survives only if the 120 mm
ray's effective diameter is **less than 1.205x the isometric prediction**, since 2.11^(1/4) = 1.205
(calculated). A 20% positive thickness allometry closes the gap entirely.

*Check: **open**. No growth series of ray diameter was found, and the bluegill diameter is itself contested.*

- **Bluegill diameter, two inconsistent values (my inference; the sources do not discuss each other).**
  Puri et al. 2018 (full-text) state "the diameter of bluegill rays of 1–2 mm", with no primary
  source given. Alben et al. 2007 give I ≈ 1e-6 cm^4 = 1e-14 m^4 (relayed by S26-D). The equivalent
  solid-rod diameter for that I is **0.67 mm** (calculated). Further, 3.8e-6 N m^2 at d = 1–2 mm implies
  an effective solid-rod modulus of only **4.8–77 MPa** (calculated). That is far below the 0.1–1 GPa
  composite modulus Alben reports. The bilaminar, partly hollow section may explain it, but the
  inconsistency means the cross-section of the ray being scaled is not pinned down.
- **Zebrafish (measured, Puri 2018, full-text).** Caudal rays are 0.1–0.2 mm across, measured on live
  images and calipers. Fin thickness tapers from 200 to 40 µm proximal to distal. These are a different species
  and a different fin, so they do not bear on the bluegill-to-120 mm extrapolation.
- No measured lepidotrichial diameter for any exocoetid was found. The Plazi treatments cited in the
  parallel document give ray *lengths* only (listing level; I did not re-open them).

### C4 · organism · conservation: the per-ray load must balance a body mass consistent with a 120 mm ray

*Requirement.* In steady glide, lift = weight (S6-D: P = n·m·g / 2N). EI_req is linear in m, so the
"2.1x deficit" survives only if the body mass of a fish that carries 120 mm load-bearing rays is
**at least 0.047 kg** (calculated: 0.10 kg / 2.11). Below that, the scaled passive ray already carries the
load. The assumed value is 0.10 kg. The window I test is m ∈ [0.05, 0.20] kg.

*Check: **open**. I found no sourced mass for an exocoetid with 120 mm pectoral rays.*

- The minimum body length for a 120 mm fin follows from Davenport 1992 (abstract, relayed by S6-D), who
  states pectoral fin length "cannot be greater than 78–79% of standard length". That gives SL ≥ 152–154 mm
  (calculated).
- The mass-length exponent is near-isometric in exocoetids. Four Kuroshio flyingfish species (Frontiers in
  Marine Science 2021, doi:10.3389/fmars.2021.747382; **full-text via summarizer**, first 100k characters)
  give b = 2.908, 2.910, 3.011 and 2.971. The coefficients *a* and the fork-length ranges appear only in a
  figure I could not read, so **I cannot turn this into a mass at SL ≈ 150–210 mm**. A Bay of Bengal
  *Cheilopogon* study reports b = 2.852–3.126 (**search-summary**). This supports the m ∝ L^3 assumption
  behind the size-dependent gap in §0. It does not test the 0.10 kg value.
- Search scope: one web search for exocoetid length–weight relationships, and one for Park & Choi 2010
  *Cypselurus hiraii* morphometrics. The second did not return body masses.

### C5 · organism · spatial: the 120 mm span must be the pectoral ray length of the animal the requirement is for

*Requirement.* The 120 mm used for scaling must match the actual load-bearing pectoral ray length of the
target organism within a factor of 1.5 (ratio ∈ [0.67, 1.5]). Otherwise both the 78.6 factor and EI_req,
which goes as L^2, are for the wrong animal.

*Check: **open**, because the target animal is set by assumption. The two readings must be kept apart.*

- **Reading A: the target is an exocoetid, which is what S6-D wrote.** This is consistent but not confirmed.
  Park & Choi 2010, *J Exp Biol* 213:3269, *Cypselurus hiraii*, report SL ≈ 199–209 mm and span 233–261 mm
  (relayed from the parallel document at **search-summary**; I could not re-retrieve these numbers).
  Those values imply about 115–130 mm per fin (a derivation). S6-D's own sourcing is Davenport's 78–79% SL
  bound, an abstract. **Animal on both sides: exocoetid (C. hiraii) and an assumed exocoetid-sized fish.**
- **Reading B: the target is the project's zebrafish.** The constraint would then fail badly. Adult
  zebrafish first show secondary sexual characters at **17.5 ± 0.6 mm SL (males) and 18.3 ± 0.7 mm SL
  (females)** (Parichy et al. 2009, *Dev Dyn*, PMC3030279; **full-text via summarizer**, first 100k
  characters). Danos & Lauder 2007 (*J Exp Biol* 210:3374; **abstract**) studied fish up to 1.97 cm fork
  length. A 120 mm ray would be roughly 6x the whole fish. **But claim 95 and S6-D do not make this
  claim.** S6-D scopes the requirement to a 100 g fish. Using zebrafish size against an exocoetid-sized
  requirement would repeat the cross-species error the brief warns about, in the opposite direction. So
  this is **not** an `unsatisfiable`. What it does establish is that **the 2.1x conclusion says nothing about the zebrafish**.
  Given the size dependence in §0 (gap ∝ L under isometry), extrapolating to a zebrafish-scale ray would
  make the gap shrink, not grow. That rests on bluegill EI scaled down, which C1 and C2 leave unverified, and
  on a zebrafish mass I have not sourced.

---

## Summary

- The arithmetic in claim 95 is correct for its inputs (calculated, agrees with replicate-95).
- **No constraint is `satisfied`, and none is `unsatisfiable`.** All five are `open`.
- **New since the parallel entailment.** Puri et al. 2018 (full text, zebrafish, measured) gives a
  cross-species d^4 test. It agrees with the 3.8e-6 input within 1.5–4.5x and disagrees with Flammang's
  565e-6 by 230–680x. This weakens, though it does not remove, the same-species conflict that most
  threatened C1. The parallel document leaned toward 565e-6 as a possible refutation from below. On this
  evidence I read 565e-6 as most likely a different quantity (in vivo or under buckling). That is my
  inference, and the disagreement stays unresolved until Flammang's methods are read.
- **The 2.1x is a single-size number.** Under joint isometry the gap scales ∝ L (calculated), and S6-D chose
  that size by assumption (L = 0.12 m, m = 0.10 kg).
- **The single most useful next read** is the Flammang et al. 2013 methods: the specimen ray length behind the
  stiffness values, and how 565e-6 was obtained. It needs the full text, which this session could not reach
  (Wiley returned 403, sites.harvard.edu is not on the network allowlist).

## Sources and read-levels

- Puri, Aegerter-Wilmsen, Jaźwińska & Aegerter 2018, *J Exp Biol* 221:jeb171777, PMC5868929: **full-text** (Europe PMC XML).
- Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161: **abstract** (Europe PMC REST). Full text **could-not-access**.
- Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861: values relayed from S26-D/replicate-95, which read it as full-text via summarizer. Not re-read by me (**listing**, for my purposes).
- Aiello et al. 2018, *J Morphol*, doi:10.1002/jmor.20830: **abstract**.
- Aiello et al. 2018, *J Exp Biol* 221:jeb163360: **abstract**.
- Parichy et al. 2009, *Dev Dyn*, PMC3030279: **full-text via summarizer** (partial, first 100k characters).
- Danos & Lauder 2007, *J Exp Biol* 210:3374, doi:10.1242/jeb.007484: **abstract**.
- Kuroshio flyingfish growth study, *Front Mar Sci* 2021, doi:10.3389/fmars.2021.747382: **full-text via summarizer** (partial; figure values not read).
- Bay of Bengal *Cheilopogon* length–weight study: **search-summary**.
- Park & Choi 2010, *J Exp Biol* 213:3269: **search-summary**, relayed from the parallel entailment and not re-retrieved.
- Davenport 1992: **abstract**, relayed by S6-D.
- Aiello PhD dissertation (University of Chicago): **could-not-access** (host blocked).

```swarm-entail
{"source_claim": 95, "source_scale": "organ",
  "constraints": [
    {"target_scale": "tissue", "kind": "range",
      "statement": "The passive flexural rigidity of the ~40 mm bluegill pectoral ray being scaled must lie within a factor of 2 of the value used, or the 2.1x gap does not stand",
      "quantity": "passive EI of a ~40.3 mm bluegill pectoral fin ray", "lo": 1.9e-6, "hi": 7.6e-6, "units": "N m^2",
      "status": "open",
      "satisfied_by": "Bluegill on both sides, and the sources disagree. Alben et al. 2007 excised-ray bending gives 1e-6 to 1e-5 (wider than the window, base condition unstated). The Puri 2018 relay gives 3.8e-6 (no method or length). Flammang 2013 abstract gives 565e-6, 'calculated' from an in-vivo perturbation, so probably not a passive quantity, and not recoverable from the abstract's own force and curvature under linear beam theory (calculated EI <= 2.9e-7). A cross-species d^4 test against measured zebrafish fin EI (1.5e-9 to 4e-9, Puri 2018) favours 3.8e-6 (1.5-4.5x off) over 565e-6 (230-680x off); this is evidence, not a refutation",
      "satisfied_evidence": "literature",
      "note": "Puri et al. 2018 J Exp Biol 221:jeb171777 PMC5868929 (full-text); Flammang et al. 2013 J Morphol 274:1044 (abstract; full text could-not-access, Wiley 403 and sites.harvard.edu blocked); Alben et al. 2007 PMC2359861 (relayed by S26-D). The specimen length behind 3.8e-6 is unknown"},
    {"target_scale": "tissue", "kind": "range",
      "statement": "The effective Young's modulus of fin-ray bone must be size-invariant within a factor of 2 between a 40 mm and a 120 mm ray, as L^4 isometric scaling assumes",
      "quantity": "E(120 mm ray) / E(40.3 mm ray)", "lo": 0.5, "hi": 2.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No size series in any species was found, so this is not measured rather than found invariant. Indirect cross-species support: E is similar between two similarly sized labrids, with I dominating EI variation (Aiello et al. 2018 J Morphol). EI scales as d^4 at constant E from bluegill to zebrafish within ~1.5-4.5x (Puri 2018, recalculated). Neither is a growth series",
      "satisfied_evidence": "unknown",
      "note": "Searched: Europe PMC '\"fin ray\" (stiffness OR flexural) (allometry OR \"body size\" OR ontogeny OR scaling)' (25 hits, none a size series); one web search (SICB abstracts, interspecific or inter-fin only). Aiello PhD thesis could-not-access (host blocked). Web of Science and Scholar not searched"},
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "Ray cross-section must scale in proportion to ray length: the 120 mm ray's effective diameter must stay below 1.205x the isometric prediction (2.98x the 40.3 mm ray), otherwise the passive gap closes",
      "quantity": "d_120 / (2.98 * d_40.3)", "lo": null, "hi": 1.205, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No growth series of lepidotrichial diameter was found for any species. The bluegill source diameter is itself inconsistent: Puri 2018 states 1-2 mm (no primary source), while Alben 2007's I ~1e-14 m^4 implies a 0.67 mm equivalent solid rod (calculated). 3.8e-6 at 1-2 mm implies an effective modulus of only 4.8-77 MPa (calculated). Zebrafish rays are 0.1-0.2 mm (measured, Puri 2018), but that is a different species and fin. No exocoetid ray diameter found",
      "satisfied_evidence": "unknown",
      "note": "Puri et al. 2018 (full-text); Alben 2007 I via S26-D relay. Searches as in C2. The diameter inconsistency is my inference; the sources do not address each other"},
    {"target_scale": "organism", "kind": "conservation",
      "statement": "Lift must balance weight with a body mass consistent with a fish carrying 120 mm load-bearing pectoral rays. Since EI_req is linear in mass, the deficit needs m >= 0.047 kg; the assumed value is 0.10 kg",
      "quantity": "body mass of a fish with 120 mm load-bearing pectoral rays", "lo": 0.05, "hi": 0.2, "units": "kg",
      "status": "open",
      "satisfied_by": "No sourced mass for such a fish was found. Davenport's fin <= 78-79% SL bound gives SL >= 152 mm (calculated). Exocoetid mass-length exponents are near-isometric (b = 2.908-3.011 in four Kuroshio species; 2.852-3.126 in Bay of Bengal Cheilopogon), but the coefficients a were not readable, so no mass at that length could be computed",
      "satisfied_evidence": "unknown",
      "note": "Front Mar Sci 2021 doi:10.3389/fmars.2021.747382 (full-text via summarizer, partial; a only in a figure); Bay of Bengal LWR (search-summary); Davenport 1992 via S6-D (abstract). Searched: one web search for exocoetid length-weight, one for Park & Choi 2010 morphometrics (no masses returned). Derived corollary: under joint isometry the gap scales as L (0.71x at 40.3 mm, 2.11x at 120 mm), so 2.1x is a single-size number"},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "The 120 mm span used for both the scaling factor and the requirement must match the load-bearing pectoral ray length of the organism the requirement is meant for, within a factor of 1.5",
      "quantity": "120 mm / actual pectoral ray length of the target organism", "lo": 0.67, "hi": 1.5, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "The target organism is set by assumption (S6-D: an unnamed 100 g fish). If the target is an exocoetid it is consistent: C. hiraii SL ~199-209 mm and span 233-261 mm imply ~115-130 mm per fin (derived; search-summary relay, not re-retrieved). If the target is the project's zebrafish it fails: adults reach 17.5-18.3 mm SL at maturity (Parichy 2009) and up to 1.97 cm FL in Danos & Lauder 2007, so a 120 mm ray is ~6x the whole fish. That reading crosses species against S6-D's stated scope, so it is not a refutation. It means the 2.1x conclusion says nothing about the zebrafish",
      "satisfied_evidence": "derived",
      "note": "Parichy et al. 2009 Dev Dyn PMC3030279 (full-text via summarizer, partial), zebrafish; Danos & Lauder 2007 J Exp Biol 210:3374 (abstract), zebrafish; Park & Choi 2010 J Exp Biol 213:3269 (search-summary via the parallel entailment), exocoetid; S6-D parameter table (full-text, repo)"}
  ]}
```
