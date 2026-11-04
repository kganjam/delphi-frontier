# Claim 95, propagated to adjacent scales (tissue, organism)

**Source claim (scale `organ`, recorded evidence: derived), not written by me:**
> SCALE ERROR FOUND: S6 and S26 compared a 40.3 mm bluegill ray's EI (3.8e-6 N m^2) against the
> requirement for a 120 mm ray. Under isometric L^4 scaling that is a factor of 78.6, so the scaled
> passive EI is 3.0e-4 against a 6.3e-4 requirement -- a gap of 2.1x, NOT the 165x reported

**Result:**
- **2 satisfied**, both at `organism`:
  - A ~0.10 kg flying fish does have pectoral fins about 120 mm long (Fish 1990, measured).
  - The pectoral fins carry at most the body weight; the measured pectoral share is 0.76–0.92.
- **3 open**, all at `tissue`:
  - modulus held constant across the transfer;
  - cross-section scaling isometrically;
  - a stiffening mechanism of at least 1.6–2.1x existing in the target animal.
- **0 unsatisfiable.** No measured number about the target animal contradicts any constraint.
- **0 unsatisfied.** For the three open constraints, nobody has measured the flying-fish quantity in any source
  I could reach. That is a gap in what has been looked at. It is not a finding that people looked and found
  nothing.

Nothing in this document was measured by me. Every number is tagged *reported* (by the cited authors),
*calculated* (by me, in [`claim-95-entail_calc.py`](claim-95-entail_calc.py); run it with `python3 -I`), or
*assumption*.

---

## 0. Which animal is on each side

This matters more than anything below, so it comes first.

- **Source (where the EI number comes from):** bluegill sunfish, *Lepomis macrochirus*.
  - I re-read Puri et al. 2018 in full text (Europe PMC XML, PMC5868929). It states: "the bending stiffness
    of bluegill rays of 3.8×10⁻⁶ N m²". That sentence attributes the value to bluegill but gives no citation.
    The nearby citation is Flammang et al. 2013, and S25 found 3.8e-6 is not in Flammang's abstract (which
    says 565×10⁻⁶; I re-read it, see Sources).
  - So the species is bluegill **as Puri relay it**. The original measurement and its ray length are
    `unknown` (challenge 97, condition C3).
  - The 40.3 mm figure is the maximum bluegill pectoral-ray length from a different study, Alben et al.
    2007, relayed through S26.
- **Target (where the 6.3e-4 requirement comes from):** the S6 scenario, a gliding fish of 0.10 kg with
  14 pectoral rays 120 mm long. That is a flying fish (Exocoetidae). It is **not a zebrafish**. An adult
  zebrafish weighs well under a gram, and none of S6, S6-D, S26 or S26-D is about zebrafish. So the
  zebrafish/exocoetid trap described in the brief does not arise for claim 95 the way it did for S32.
  - The real risk here goes the other way. Every tissue-scale number available is from bluegill (or from
    labrid wrasses, or zebrafish). Any of those being applied to the flying-fish ray is exactly the kind of
    transfer the claim itself is about.
  - So no tissue-scale constraint below can be marked satisfied or unsatisfiable with a non-exocoetid number.
    Where that is the only evidence, the verdict is `open`, and I say which animal the number came from.

## 0b. Arithmetic, reproduced (*calculated*)

- (120 / 40.3)⁴ = **78.6**.
- 3.8e-6 × 78.6 = **2.99e-4 N m²**.
- 6.31e-4 / 2.99e-4 = **2.11x**. Unscaled, the gap is 6.31e-4 / 3.8e-6 = **166x**.

The claim's arithmetic is correct, as challenge 97 also found. The constraints below ask what has to be true
at the tissue and organism scales for "2.1x, not 165x" to be the right number.

## Sources and read-levels

| source | what it gives | read-level |
|---|---|---|
| Fish FE 1990, *J Zool Lond* 221:391–403, "Wing design and scaling of flying fish with regard to flight performance" (PDF from health-sciences.wcupa.edu, which this session could reach; earlier passes were refused) | 199 specimens, six exocoetid genera, 0.003–0.53 kg. Measured reduced-major-axis regressions of SL, wing span, wing area and wing loading against mass (Tables I, II). Pectoral % of wing area (Table III). Span is defined as "twice the distance from the fin base to tip plus the body width" | **full-text** (pdftotext; tables read from the text layer, which has OCR-like artefacts, so each value I use was checked against the column structure) |
| Puri S et al. 2018, *J Exp Biol* 221:jeb171777, PMC5868929 | the 3.8e-6 bluegill relay; bluegill ray diameter "1–2 mm"; zebrafish whole-fin EI 1.5–4e-9 N m² | **full-text** (Europe PMC XML) |
| Flammang BE et al. 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161 | bluegill: 565×10⁻⁶ N m² "calculated"; proximal 40% unsegmented, distal 60% segmented | **abstract** (Europe PMC REST). Full-text PDFs at umich.edu, njit.edu and harvard.edu: **could-not-access** (proxy 403) |
| Aiello BR et al. 2018, *J Exp Biol* 221:jeb163360 | two labrid wrasses. EI as a single variable ("E and I cannot be separated"). Leading-edge proximal EI means 0.8899 µN m² (*Gomphosus varius*, n=7, 7.8–39.8 g) vs 0.1671 µN m² (*Halichoeres bivittatus*, n=8, 6.0–64.6 g). Same EI–mass slope, significantly different intercepts (P = 7.52×10⁻⁷) | **full-text, first 100k of 162k characters**, through an automated summarizer (WebFetch). Slopes are in Tables S4/S5, which I did not read: `unknown` |
| Alben S, Madden PGA, Lauder GV 2007, *J R Soc Interface* 4:243 | bluegill: ~12x clamped/free stiffness (n=1); E 1e8–1e9 Pa; max ray length 40.3 mm | **relayed full-text** via S26 and S6-D-D. I did not re-access it |
| S6-D-D (`docs/research/fish/S6-D-deepen.md`, branch `claude/deepen-s6-d-sensitive-input-fc1hm8`); challenge 97 (`claude/challenge-97-fish-ray-ei-pee0i7`) | prior scope of the negative searches; the C3 source-length condition; the EI_req model | **full-text** |
| Web searches (3, this pass) | see each constraint for the query and the scope | **search-summary** |

Refused this pass: fao.org, umich.edu, njit.edu and harvard.edu (proxy 403), and the Park & Choi IUTAM 2007 PDF
(monash.edu, 403).

---

## 1. Constraints and checks

### C1 · `tissue` · range: the effective ray-tissue modulus is the same at both sizes, within ×2

**Requirement.** The L⁴ rule assumes that EI scales only through geometry. The full form is:

gap = 2.11 × (E_source / E_target) × (I_iso / I_target).

For the stated 2.1x to be right within a factor of 2 (that is, 1.05–4.2x, which is still "~2x, not 165x"), the
ratio **E_target / E_source must lie in [0.5, 2]**. Here E_source is the effective composite modulus of the
bluegill ray and E_target that of a 120 mm exocoetid ray. (*calculated* window)

**Check: open.**
- **Bluegill (source):** E is given only as a range, 1e8–1e9 Pa (Alben 2007, relayed). The "0.24–3.7 GPa"
  bracket in S6-D-D is search-summary. One decade within a single species is already wider than the ×2
  window. My inference: the window cannot be checked even from the source side to better than ~×10.
- **Flying fish (target):** no modulus, mineral density or material measurement of an exocoetid fin ray found.
  - Searched: web, "flying fish pectoral fin ray diameter lepidotrichia morphology Exocoetidae micro-CT".
    It returned FAO identification sheets, Wikipedia species pages and a Socotra faunal survey. None is a
    tissue measurement.
  - Also searched: "fin ray flexural stiffness scaling with body size ontogeny second moment of area Young's
    modulus lepidotrichia". No exocoetid hit.
  - The earlier Europe PMC scope in S6-D-D (103 hits, 60 titles read) also found none.
  - So nobody appears to have measured it. This is not a case of people looking and finding nothing.
- **Cross-taxon, labrids (Aiello 2018): not usable here.** E and I could not be separated, so no modulus
  comparison is possible.

### C2 · `tissue` · spatial: the ray cross-section scales isometrically with ray length, within 2^¼

**Requirement.** Isometry means the base diameter (or I^¼) of the 120 mm ray is (120/40.3) = 2.98× the source
ray's. The ×2 tolerance on the gap gives a **diameter ratio in [2.50, 3.54]**.

With Puri's bluegill diameter of 1–2 mm (reported, bluegill), the target ray's base solid-equivalent diameter
must be **2.5–7.1 mm** (*calculated*).

For reference (*calculated*):
- β = 0 (no size correction) gives the 165x figure.
- The exponent at which the passive ray exactly meets the requirement is β = 4.69 (a gap of 1x).
- The claim's β = 4 sits between them.

**Check: open.**
- **Flying fish:** no ray diameter, cross-section or I for an exocoetid pectoral ray found (same searches and
  scope as C1). The FAO sheets in the search results give ray counts and pectoral length as % SL, not
  ray cross-sections. I could not open them (fao.org refused); the summary is search-summary.
- **Bluegill:** I found no within-species exponent for EI against ray length.
  - A search-summary said Flammang 2013 reports that stiffness "increases with ontogeny". That sentence is not
    in the abstract I read, and I could not reach the full text, so I treat it as unverified and give no
    exponent.
- **Labrids (Aiello 2018; species: *G. varius*, *H. bivittatus*; neither bluegill nor exocoetid):**
  - EI rises with ray length and with body mass in both species, with the same slope against mass. The slope
    value is `unknown` (supplementary tables not read).
  - At almost equal mean mass (22.4 vs 22.0 g), proximal leading-edge EI differs **5.3x** between the two
    species (*calculated* from the reported means). Ray lengths were measured on different specimens and
    their ranges differ (12.7–29.5 vs 12.9–23.8 mm), so part of the 5.3x may be length rather than
    proportion. That part is `unknown`.
  - My inference: species identity alone moves ray EI at a given body size by more than the ×2 tolerance this
    claim needs. So a bluegill-to-exocoetid transfer has an uncertainty in EI of at least the same order as
    the 2.1x it reports.
  - This is a cross-taxon comparison. It weakens confidence in the precision of "2.1x". It **does not refute**
    the claim, because neither species is the source or the target.
- **The 1x and 165x endpoints in diameter terms (*calculated*):**
  - The 165x endpoint needs a 120 mm ray no thicker than a 40 mm bluegill ray.
  - The 1x endpoint needs a ray (6.31e-4/2.99e-4)^¼ = 1.21x thicker than isometric.
  - Thin, high-aspect-ratio exocoetid wings (Fish 1990: pectoral AR up to 16.9 in *Exocoetus*) do not, by
    themselves, say which way ray thickness goes. Aspect ratio is a planform property, not a ray
    cross-section.

### C3 · `organism` · spatial: a fish of the S6 mass has pectoral rays near 120 mm

**Requirement.** The 78.6 factor is (L_target/40.3)⁴. For it to hold within ×2 in EI, the target ray length must
be in **[101, 143] mm** (*calculated*), and this must be the real fin length of a gliding fish of the mass
(0.10 kg) used for EI_req. If real 0.10 kg flying fish had 60 mm fins, the 78.6 would be an artefact of the
scenario.

**Check: satisfied, for the *Cypselurus*-design genera and *Parexocoetus*.**
- Source: Fish 1990, measured, **full-text**, **flying fish (same animal as the target)**.
- The wing-span regressions (Table I) evaluated at M = 0.10 kg give spans (*calculated* from the reported
  coefficients):

  | genus | span (mm) |
  |---|---|
  | *Fodiator* | 222 |
  | *Parexocoetus* | 254 |
  | *Cypselurus* | 275 |
  | *Hirundichthyes* | 282 |
  | *Danichthyes* | 305 |
  | *Exocoetus* | 323 |

- Fish defines span as 2 × (fin base to tip) + body width. With a body width of 15–25 mm (*assumption*,
  unsourced), base-to-tip is (*calculated*):

  | genus | base-to-tip (mm) | vs window |
  |---|---|---|
  | *Fodiator* | 98–103 | at the lower edge |
  | *Parexocoetus* | 115–120 | inside |
  | *Cypselurus* | 125–130 | inside |
  | *Hirundichthyes* | 128–133 | inside |
  | *Danichthyes* | 140–145 | at the upper edge |
  | *Exocoetus* | 149–154 | above |

- So a 120 mm pectoral fin on a 0.10 kg flying fish is what the measurements predict, within the window for
  four of six genera.
- Caveats:
  - Base-to-tip of the spread fin is not exactly the longest ray's length. Rays leave the base at an angle,
    so the longest ray is probably slightly longer (my inference, unmeasured).
  - The regressions are fitted across 0.003–0.53 kg. 0.10 kg lies inside that range, so this is
    interpolation, not extrapolation.
- *Evidence: derived* (measured regressions + an assumed body width).

### C4 · `organism` · conservation: the pectoral rays carry at most the weight share their fins support

**Requirement.** In a steady glide, vertical momentum balance gives total lift ≈ m g cos γ. The 6.3e-4
requirement assumes the pectoral fins carry all of it (share s = 1), split equally over N = 14 rays. For a real
gap to remain (≥1x) at isometry, the **pectoral share s must lie in [0.47, 1.0]** (*calculated*). The upper
bound is the conservation limit: the fins cannot carry more than the weight in a steady glide.

**Check: satisfied.**
- Source: Fish 1990 Table III, measured, **full-text**, **flying fish**. The pectoral share of total wing area
  is:

  | genus | pectoral share |
  |---|---|
  | *Cypselurus* | 76.0% |
  | *Hirundichthyes* | 76.6% |
  | *Danichthyes* | 77.4% |
  | *Parexocoetus* | 81.5% |
  | *Exocoetus* | 91.8% |

- If lift share equals area share (*assumption*; pelvic fins sit in the pectoral wake in biplane designs, so
  this may not hold), EI_req falls to 4.8–5.8e-4 and **the isometric gap becomes 1.6–1.9x** (*calculated*),
  not 2.1x.
- Ray count:
  - A search-summary of an FAO sheet gives 17–19 pectoral rays for one exocoetid species (species not named
    in the summary; fao.org refused, so not verified).
  - If N = 17–19 rather than 14, the gap falls further, to 1.6–1.7x at s = 1 (*calculated*).
  - S6's N = 14 is therefore conservative, not just unsourced.
- Wing loading at 0.10 kg from Fish's Table II is 113–131 N m⁻² for *Cypselurus*, *Hirundichthyes* and
  *Exocoetus* (*calculated* from the reported regressions). I record it for later passes. It does not enter
  EI_req directly.
- So the claim's 2.1x is, if anything, an **upper** estimate of the gap at the organism scale. This is
  consistent with the claim's direction ("not 165x") and sharpens it.

### C5 · `tissue` · existence: something supplies ≥1.6–2.1x stiffening beyond the passive isometric ray

**Requirement.** If claim 95 is right, then a passive, isometrically scaled ray still falls 1.6–2.1x short of
δ/L ≤ 0.10 (C4-corrected). But flying fish do glide with pectorals spread (Fish 1990 relays flights of 15–92 m
for *Cypselurus*, after Hubbs). So at least one of the following must exist in the target animal:
- (a) a tissue mechanism that raises effective ray EI by ≥1.6–2.1x (active hemitrich offset/locking,
  membrane pre-tension, curvature-induced stiffening);
- (b) rays more than 1.13–1.21x thicker than isometric (*calculated*; this is C2 again);
- (c) tolerance of more deflection than δ/L = 0.10. The 0.10 is an S6 *assumption*, unmeasured.

Stated generically: **a stiffening factor of at least 1.6–2.1x must be available to the ray in vivo.**

**Check: open. The species differ.**
- **Bluegill:** Alben 2007 reports a ~12x clamped/free stiffness ratio on one ray (n = 1; relayed full-text
  via S26; I did not re-access it). That meets the bound by 6–7x, **in bluegill**.
- **Flying fish:** no measurement of active ray stiffening, fin-ray musculature, in-glide fin deflection or
  camber found.
  - Searched: web, "flying fish pectoral fin deformation during gliding camber fin ray stiffness muscle".
    The hits were a cownose-ray simulation, a 2026 conference abstract on a flying-fish-*inspired* membrane
    wing model (no measurement), a sunfish/perch ray comparison, a mackerel curvature-stiffening result, and
    Cortes et al. 2022 on glide stability (fins treated as lifting surfaces, no ray mechanics). All are
    **search-summary**.
  - Nobody appears to have measured this in Exocoetidae. That is unexamined, not a negative.
- Requirement (c), the tolerated δ/L, is likewise unmeasured for flying fish. If gliding fins tolerate
  δ/L ≈ 0.2, a gap of ≤2x closes without any mechanism (*calculated*: δ/L at a 2.1x gap is 0.21).
- I am not marking this satisfied on bluegill evidence. That would repeat the very transfer the claim is
  about.

---

## 2. What this does to claim 95

- **Arithmetic:** correct (§0b).
- **Organism scale:** the two checkable entailments, fin length at the S6 mass and load conservation, are
  **satisfied by measured flying-fish morphometrics** (Fish 1990, full-text, read for the first time in this
  project). The load correction moves the gap **down**, from 2.1x to 1.6–1.9x, and a higher ray count moves
  it further down. Nothing at the organism scale contradicts the claim.
- **Tissue scale:** everything the claim actually rests on is **open**:
  - the L⁴ rule needs constant modulus (C1) and isometric cross-section (C2);
  - nothing has been measured for an exocoetid ray.
  - The only cross-species data I could reach (two wrasses, Aiello 2018) show a 5.3x EI difference at equal
    body mass. My inference: the bluegill-to-exocoetid transfer is uncertain by at least as much as the 2.1x
    it reports.
- **The honest form of claim 95** (my wording):
  - "Size-corrected at constant modulus and proportion, the gap is ~1.6–2.1x, not 165x."
  - "The 165x figure was a β = 0 artefact, and that part stands."
  - "Whether the true gap is 0.5x or 10x depends on an exocoetid ray cross-section and modulus that nobody has
    measured."
- **Cheapest decisive measurement** (as in S6-D-D §3d, and unchanged): micro-CT or calipers on the base of
  the leading pectoral rays of museum *Cypselurus* / *Hirundichthys* specimens of ~0.1 kg. That settles C2
  directly and C3 more precisely. C1 and C5 would still need fresh tissue.

```swarm-entail
{"source_claim": 95, "source_scale": "organ",
  "constraints": [
    {"target_scale": "tissue", "kind": "range",
      "statement": "The effective composite modulus of the ray tissue must be the same at source and target size within a factor of 2, so that EI transfers through geometry alone",
      "quantity": "E_target / E_source (exocoetid 120 mm ray / bluegill <=40 mm ray)", "lo": 0.5, "hi": 2.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Nothing found for the target. No exocoetid fin-ray modulus or material measurement. Bluegill source E is itself only a 1e8-1e9 Pa range (Alben 2007, relayed), already wider than the window.",
      "satisfied_evidence": "unknown",
      "note": "Searched: web 'flying fish pectoral fin ray diameter lepidotrichia morphology Exocoetidae micro-CT' and 'fin ray flexural stiffness scaling with body size ontogeny second moment of area Young's modulus lepidotrichia' (search-summary), plus S6-D-D's Europe PMC scope (103 hits, 60 titles). Unexamined, not looked-and-absent. Aiello 2018 (labrids) could not separate E from I."},
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "Ray cross-section must scale isometrically with ray length: the target ray's base diameter is (120/40.3) times the source ray's, within 2^(1/4)",
      "quantity": "base diameter ratio, 120 mm exocoetid ray / bluegill ray", "lo": 2.5, "hi": 3.54, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No exocoetid ray diameter or second moment of area found. Bluegill d = 1-2 mm (Puri 2018, full-text) implies a target of 2.5-7.1 mm (calculated). Cross-taxon only: two labrids (Aiello 2018) differ 5.3x in proximal leading-edge EI at equal mean mass (22.4 vs 22.0 g, calculated from reported means). Informative, not a refutation, because neither is source nor target species.",
      "satisfied_evidence": "unknown",
      "note": "Puri SR et al 2018 JEB 221:jeb171777 (full-text); Aiello BR et al 2018 JEB 221:jeb163360 (full-text to 100k of 162k chars via summarizer; slopes in supp. tables S4/S5 not read). Same exocoetid search scope as C1. Flammang 2013 'stiffness increases with ontogeny' is search-summary only and not in the abstract, so unverified. Unexamined for Exocoetidae."},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "A gliding fish of the mass used for the requirement (0.10 kg) must actually have pectoral fins of the length that sets the L^4 factor",
      "quantity": "pectoral fin base-to-tip length at 0.10 kg", "lo": 101, "hi": 143, "units": "mm",
      "status": "satisfied",
      "satisfied_by": "Fish 1990 measured wing-span regressions (199 exocoetids, 6 genera, 0.003-0.53 kg) give base-to-tip at 0.10 kg of 115-145 mm for Parexocoetus, Cypselurus, Hirundichthyes and Danichthyes (calculated, with an assumed body width of 15-25 mm). Fodiator 98-103 mm is at the lower edge; Exocoetus 149-154 mm is above.",
      "satisfied_evidence": "derived",
      "note": "Fish FE 1990 J Zool Lond 221:391-403, Table I, full-text. Same animal as the target (Exocoetidae). Base-to-tip is not the longest-ray length, and the difference is unmeasured."},
    {"target_scale": "organism", "kind": "conservation",
      "statement": "In steady glide the lift carried by the pectoral rays cannot exceed the body weight, and for a real gap to remain at isometry the pectoral share must exceed ~0.47",
      "quantity": "pectoral share s of glide lift (taken as share of wing area)", "lo": 0.47, "hi": 1.0, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Fish 1990 Table III measured pectoral % of wing area: Cypselurus 76.0, Hirundichthyes 76.6, Danichthyes 77.4, Parexocoetus 81.5, Exocoetus 91.8. This lowers EI_req to 4.8-5.8e-4 and the isometric gap to 1.6-1.9x (calculated). Lift share = area share is an assumption.",
      "satisfied_evidence": "measured",
      "note": "Fish FE 1990 Table III, full-text, Exocoetidae (same animal as the target). Ray count 17-19 for one exocoetid species is search-summary of an FAO sheet (fao.org refused). If true, it lowers the gap further to 1.6-1.7x."},
    {"target_scale": "tissue", "kind": "existence",
      "statement": "A mechanism must exist in the target animal that raises in-vivo ray stiffness by at least the residual gap over the passive isometric value (or the tolerated deflection must exceed the assumed delta/L = 0.10)",
      "quantity": "in-vivo stiffening factor over passive", "lo": 1.6, "hi": null, "units": "dimensionless (x)",
      "status": "open",
      "satisfied_by": "Met in BLUEGILL only: Alben 2007 ~12x clamped/free stiffness ratio, n=1 (relayed full-text via S26, not re-accessed). No exocoetid measurement of active ray stiffening, fin-ray musculature or in-glide fin deflection found. The species differ, so this is not satisfied for the target.",
      "satisfied_evidence": "unknown",
      "note": "Searched: web 'flying fish pectoral fin deformation during gliding camber fin ray stiffness muscle' (search-summary). Hits: cownose-ray simulation, a flying-fish-inspired membrane-wing model abstract (no measurement), sunfish/perch and mackerel ray results, Cortes et al 2022 glide stability (no ray mechanics). Unexamined for Exocoetidae, not looked-and-absent."}
  ]}
```
