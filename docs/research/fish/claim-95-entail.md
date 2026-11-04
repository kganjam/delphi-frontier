# Claim 95: what it requires at the tissue and organism scales, and whether those requirements hold

**Source claim (organ scale, evidence: derived).** S6 and S26 compared the EI of a 40.3 mm bluegill
ray (3.8e-6 N m^2) with the requirement for a 120 mm ray (6.3e-4 N m^2). Under isometric L^4
scaling the factor is 78.6, so the scaled passive EI is 3.0e-4 N m^2. That leaves a gap of 2.1x,
not the 165x that was reported.

**Bottom line.** None of the five constraints below is `unsatisfiable`. One is `satisfied`, and only
for the flying-fish scenario the claim is really about (C4). Four are `open`. The input EI (C1)
has three same-species values that disagree. The scaling assumptions (C2, C3) have never been
measured in any species I could reach. The load partition (C5) has an area proxy but no measured
lift split. Within that scope, the claim's arithmetic is right. Its 2.1x is a number conditional on
two unmeasured scaling assumptions and one disputed input. It is not a property of rays.

Tags used throughout: *measured* (by the cited authors), *calculated* (arithmetic done here, shown
inline, never an observation), *assumption*, *inference* (my reading, not the authors' claim).

---

## 0. Which animal is the claim about? (this decides every verdict below)

I checked this before entailing anything, because the project's claims are mostly about zebrafish
and the nearest literature is mostly about something else.

- **The 120 mm / 6.3e-4 N m^2 side is a 100 g flying-fish scenario, not a zebrafish.** S6-D-D
  (`docs/research/fish/S6-D-deepen.md`, commit f43d1afb, read in full) records the scenario inputs as
  *assumptions*: m = 0.10 kg, N = 14 rays per fin, L = 0.12 m, failure at δ/L > 0.10. It also
  records that S6-D "reconstructed an S6 answer about a **100 g flying fish**". The original S6
  (branch `claude/s6-fin-ray-load-kqweu7`) is about a **0.4 g zebrafish** and used a measured
  zebrafish caudal-fin EI.
- **Consequence (my inference).** Claim 95's "S6" means S6-D's flying-fish scenario. The claim says
  nothing about the zebrafish S6, and the scale error it corrects does not exist there.
- **Requirement reproduced (calculated).** All weight is shared equally by 2 × 14 rays, each a
  uniformly loaded cantilever with δ/L = 0.1. Then EI = (mg/28)·L^2/(8·0.1) =
  (0.981/28)·0.0144/0.8 = **6.31e-4 N m^2**. That matches the 6.3e-4 in the claim, and it fixes the
  load case used in C5.
- **The 40.3 mm side is bluegill (*Lepomis macrochirus*).**
- **So the claim is cross-species by construction:** a bluegill ray scaled to a flying-fish ray.
  Every check below names the animal on each side.

**Claim arithmetic re-checked (calculated).**
- (120/40.3)^4 = 78.61.
- 3.8e-6 × 78.61 = 2.99e-4 N m^2.
- 6.3e-4 / 2.99e-4 = **2.11**.
- The unscaled ratio is 6.3e-4 / 3.8e-6 = 165.8.

The claim is correct given its inputs.

---

## 1. Constraints and checks

### C1 · tissue · range: the passive EI of a ~40 mm bluegill pectoral ray must be near 3.8e-6 N m^2

**Requirement.** The "2.1x" stands within a factor of 2 (a gap of 1.05–4.2x, calculated) only if the
unlocked (passive) EI of the 40.3 mm bluegill ray lies in **[1.9e-6, 7.6e-6] N m^2**.

**Animal on both sides:** bluegill.

**Status: open.** Three bluegill values are available and they disagree. None of them is a direct,
replicated measurement of passive EI at known ray length.

| Value (N m^2) | What it is | Gap it implies (calculated) | Source, read-level |
|---|---|---|---|
| 3.8e-6 | value used by the claim | 2.1x | Puri et al. 2018 (PMC5868929). S6-D-D read it at **full-text** and reports that the sentence carries **no citation**; its attribution to Flammang 2013 is an upstream reading, not Puri's statement. I did not re-read it. |
| 1e-6 to 1e-5 | the authors' order-of-magnitude E·I (E ≈ 1e8–1e9 Pa, I ≈ 1e-6 cm^4) | 8.0x to 0.80x | Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861. **full-text** as read and quoted verbatim by challenge-209 (`docs/research/fish/challenge-209.md`, commit 8fa40789). My own fetch hit a reCAPTCHA wall and Europe PMC fullTextXML returned HTTP 500, so for me it is **could-not-access**. I rely on challenge-209's quotes. |
| 1.07e-6 to 1.87e-6 | one-base-free EI, back-calculated from the measured 1.98 N/m clamped slope ÷ 12, uniform cantilever, L assumed 40.3 mm | **7.5x to 4.3x** | challenge-209 §3 (calculated there; I reproduced the gap arithmetic). The underlying slope and the 12x ratio are *measured*. The EI is *calculated*, and the tested ray's length is not reported. |
| 565e-6 | "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2" | 0.014x (a ~70x surplus) | Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161. **abstract**, retrieved verbatim by me from the Europe PMC REST API. Not open access. |

**Why this is not `satisfied`.** Only Puri's uncited 3.8e-6 sits in the window. Alben's
order-of-magnitude range straddles the whole window and cannot resolve a factor of 2.

**Why the Alben back-calculation does not make it `unsatisfiable`.** The back-calculation falls just
below the window, which would make the gap 4.3–7.5x. But it is a *calculated* EI that rests on an
assumed ray length and a uniform-beam model. It is not a measured EI, and the rule requires a
measured number.

**Why Flammang does not make it `unsatisfiable` either.** The animal is the same, but the value
cannot carry a refutation:

- The abstract says the value was *calculated* from an in-vivo vortex-jet perturbation. It is not a
  bending test.
- The same abstract says, a few lines later, that the rays have "small bending rigidity".
- **Internal consistency check (calculated by me, and weak).** The abstract reports a 67 mN impact
  force and a maximum curvature of 9.38 mm^-1. Take a moment arm no longer than the 40.3 mm maximum
  ray length (Alben 2007, a different set of fish). Then EI = M/κ ≤ 0.067 × 0.0403 / 9380 =
  **2.9e-7 N m^2**, about 2000x below 565e-6.
- The check assumes elastic Euler–Bernoulli bending. The abstract says the ray *buckled* locally at
  impact, so this is not a clean inversion. It shows only that the abstract's three numbers do not
  hang together as printed.

I preserve all four values and do not average them.

**What would settle C1:** the Flammang 2013 methods and units in full text, or a three-point bend of
an excised bluegill ray of known length with the bases free.

### C2 · tissue · spatial: ray cross-section must scale in proportion to ray length from 40.3 mm to 120 mm

**Requirement.** EI ∝ L^4 assumes diameter ∝ length at a fixed section shape. The 2.1x holds within a
factor of 2 only if the real 120 mm ray's diameter, divided by the isometric prediction
(2.98 × d_40.3), lies in **[0.84, 1.19]** (calculated: 0.5^(1/4) to 2^(1/4)).

**Animal on both sides:** bluegill (40 mm) and exocoetid (120 mm). This is an *interspecific*
extrapolation, not an ontogenetic one.

**Status: open. Nobody has measured it, as far as the searches reached.** This is not a finding
that someone looked and found non-isometry.

- **My search.** Europe PMC REST:
  `("fin ray" OR lepidotrichia OR lepidotrichium) AND (ontogen* OR allometr* OR "body size") AND
  ("Young's modulus" OR "elastic modulus" OR stiffness OR "cross-section" OR "second moment" OR thickness)`.
  - 129 hits. I screened the first 60 titles.
  - None measures lepidotrichial diameter or I against ray length or body size.
  - The nearest were a sturgeon pectoral *spine* (2026, a different structure) and Aiello et al. 2017
    PNAS (labrid, one size class).
- **My second search.** `(Exocoetidae OR "flying fish" OR Cypselurus OR Cheilopogon OR Exocoetus) AND
  ("fin ray" OR lepidotrich* OR "pectoral fin")`.
  - 45 hits, all titles screened.
  - None measures exocoetid ray diameter, I or EI.
- **Positive control.** `"fin ray" AND hemitrich*` returned 30 hits, so the index does cover
  fin-ray mechanics.
- **Upstream searches agree.** S6-D-D (20-hit and 42-hit Europe PMC queries) and S26-D-D (3 web
  searches plus an 11-hit Europe PMC query) found no fin-ray EI–size exponent and no exocoetid ray
  dimension.
- **Not searched:** Google Scholar, Web of Science, MorphoSource. An oVert *Exocoetus volitans* CT,
  UF 231939, is reported upstream at listing level and was not opened.
- **Tangential evidence (measured; exocoetid; whole fin, not ray section).** Fish 1990,
  *J Zool* 221:391, read at **full-text** (PDF text layer, extracted by me). The wing-span exponent
  against mass is 0.375 (95% CI 0.364–0.387) in *Cypselurus*, against 0.33 for geometric scaling. So
  fin *length* is positively allometric within that genus. This says nothing about ray *diameter*,
  and it does not bear on C2's window.
- **Sensitivity (calculated upstream in S26-D-D, and consistent with the window above).** Because
  diameter enters at the 4th power, this is the input the conclusion is most sensitive to.

### C3 · tissue · range: ray-bone modulus must be size-invariant between the two rays

**Requirement.** L^4 scaling also assumes the same composite modulus E. For the 2.1x to hold within a
factor of 2, the ratio E(120 mm exocoetid ray) / E(40.3 mm bluegill ray) must lie in **[0.5, 2.0]**.

**Animal:** bluegill on one side. On the other side there is no data.

**Status: open, not measured.**

- The first Europe PMC query in C2 included modulus terms and found no size series of lepidotrichial
  modulus in any species. This rests on the same scope and controls as C2.
- **Within-species spread is wider than the window.** Proximal moduli of 0.24–3.7 GPa in bluegill
  (Lauder group, relayed upstream at **search-summary**), and Alben 2007's E ≈ 1e8–1e9 Pa (full-text
  via challenge-209).
- **My inference:** E varies enough within one fin that a cross-species E ratio of 2 is entirely
  possible in either direction. That is not evidence that it does vary.

### C4 · organism · spatial: a 100 g fish of the scenario's kind must have pectoral rays about 120 mm long

**Requirement.** The 120 mm in the claim must match the pectoral-fin length (base to tip) of a 0.1 kg
fish of the scenario within a factor of 1.5. That is, 120 mm / fin length must lie in
**[0.67, 1.5]**. Otherwise the L^4 factor is applied to the wrong length.

**Animal on both sides:** exocoetid. The requirement is S6-D's 100 g flying-fish scenario, and the
data are measured on Exocoetidae.

**Status: satisfied (derived from a measured regression).**

- **Source.** Fish 1990, Table I, reduced-major-axis fits on 199 preserved exocoetids, 0.003–0.53 kg.
  Read at **full-text**.
  - *Cypselurus* (n = 113): wing span = 0.651 M^0.375.
  - *Exocoetus* (n = 26): wing span = 0.774 M^0.380.
  - Span is defined as "twice the distance from the fin base to tip plus the body width".
  - The fitted units (m, kg) are my reading. They are confirmed by the paper's own statement that a
    0.1 kg *Cypselurus* would need a 0.51 m span, "2.5 times the length of the fish and 1.8 times
    the wing span". That implies a span of 0.28 m. My calculated value is 0.275 m.
- **At M = 0.1 kg (calculated).**
  - *Cypselurus*: span 0.275 m, so fin length = (0.275 − w)/2 = 0.137 m at w = 0, or 0.122 m at a
    body width w = 30 mm. The ratio 120/fin is **0.87–0.98**.
  - *Exocoetus*: fin length 0.147–0.161 m, so the ratio is **0.74–0.82**.
  - The body width w is not reported in the text I read. The window fails only if w > 115 mm on a
    203 mm fish. The fish length, 0.460 M^0.355 = 203 mm, is calculated from the same table.
- **Assumption.** The longest pectoral ray runs approximately the full fin length from base to tip.
- **Scope warning.** This satisfies C4 only for a flying-fish target. If anyone reads claim 95 as a
  statement about the project's zebrafish, C4 is not satisfied, because the requirement was never
  derived for a zebrafish (§0). I did not retrieve a sourced zebrafish ray length, so I quote none.

### C5 · organism · conservation: weight must be carried by the pectoral rays in the proportion the requirement assumes

**Requirement.** The 6.3e-4 N m^2 rests on vertical-momentum balance in a steady glide. All of the
weight is carried by the pectoral fins and split equally over 2 × 14 rays (§0, calculated). The
per-ray requirement scales as f_p × 14 / N. Here f_p is the fraction of glide lift on the pectoral
fins, and N is the real ray count per pectoral fin. For the 2.1x to hold within a factor of 2,
**f_p × 14 / N must lie in [0.5, 2.0]**.

**Animal:** exocoetid on both sides.

**Status: open.** There is an area proxy inside the window, but no measured lift partition and no ray
count.

- **Area proxy (measured; exocoetids; full-text).** Fish 1990, Table IV. The pectoral fins make up
  **75.99 ± 0.57 %** of wing area in *Cypselurus* and **91.83 ± 0.38 %** in *Exocoetus*. Other genera
  fall at 76.6–83.2 %.
  - If lift ∝ area, then f_p ≈ 0.76–0.92, and with N = 14 the product sits inside the window. That
    is an *assumption*. Fish also notes the ventrally flattened *Cypselurus* body may add lifting
    surface, which would lower f_p.
- **Lift partition: not found.**
  - Park & Choi 2010, *J Exp Biol* 213:3269 (*Cypselurus*, wind tunnel), read at **search-summary**.
    They report that the pelvic fins *increase* lift and L/D.
  - An earlier Park & Choi IUTAM 2007 paper, also **search-summary**, reports that models with both
    fin pairs enlarged had *lower* lift coefficients than pectoral-only models.
  - These two summaries disagree. I keep both. Neither gave me a numeric f_p.
  - The full text could not be accessed: the JEB URL returned an unrelated article, and typeset.io
    is outside this session's network allowlist and failed DNS.
- **Ray count N = 14 for an exocoetid pectoral fin: unknown.** It is an *assumption* in S6-D. My
  Europe PMC search (C2, 45 hits) returned no meristic count, and I did not search taxonomic keys.
- **Not addressed:** load factors above 1 g at take-off, taxi or landing; unequal load between rays.
  Upstream work (S26-organ, M8) records that ray stiffness varies by about two orders of magnitude
  across one bluegill fin, so equal sharing is optimistic. That is my inference from a cross-species
  observation.

---

## 2. What this does not establish

- **No constraint is refuted, and none is shown to hold at the tissue scale.** The tissue-scale
  inputs to the 2.1x (C1–C3) are respectively disputed, unmeasured and unmeasured. So "2.1x" should
  be read as "within a factor of a few, conditional on L^4". It is not a sharp number. S26-D-D
  reached the same conclusion by sensitivity analysis.
- **The claim's correction is an arithmetic correction about a flying-fish scenario.** It cannot be
  carried over to the zebrafish S6.
- **Nothing here tests whether the remaining ~2x can be closed.** That was claim 96 and S26-D's
  question: hemitrich locking, the measured 12x in bluegill, n = 1.

## 3. Sources and read-levels

- Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161: **abstract**
  (Europe PMC REST, retrieved by me).
- Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861: **could-not-access** for me
  (reCAPTCHA; Europe PMC XML HTTP 500). Quotes used are from challenge-209's **full-text** read.
- Puri et al. 2018, PMC5868929: **full-text** as read by S6-D-D. Not re-read by me.
- Fish 1990, "Wing design and scaling of flying fish with regard to flight performance", *J Zool*
  221:391–403: **full-text** (PDF from health-sciences.wcupa.edu; text layer extracted with
  pdftotext; some table OCR noise, and values were cross-checked against the paper's own prose
  where possible).
- Park & Choi 2010, *J Exp Biol* 213:3269; Park & Choi IUTAM 2007 proceedings: **search-summary**.
- Lauder-group proximal modulus 0.24–3.7 GPa: **search-summary**, relayed upstream (S26-organ).
- Repo documents, all read in full: S26-organ.md (b5ac55ae), S26-D-deepen.md (55fdeae1),
  challenge-209.md (8fa40789), S6-D-deepen.md (f43d1afb).
- **Prior attempt.** An earlier claim-95 entailment on `origin/claude/claim-95-entail-p91b6z`
  (228b9ae7) marked all five of its constraints `open`; I read it. This document differs in four
  ways: it identifies the requirement's animal from S6-D-D, it upgrades Flammang to abstract-level,
  it adds the Fish 1990 full-text checks (C4 satisfied, C5 area proxy), and it uses a conservation
  constraint in place of an existence constraint.

```swarm-entail
{"source_claim": 95, "source_scale": "organ",
  "constraints": [
    {"target_scale": "tissue", "kind": "range",
      "statement": "The passive (unlocked) flexural rigidity of the ~40 mm source ray must lie within a factor of 2 of the value used, or the 2.1x gap is not 2.1x",
      "quantity": "passive EI of a 40.3 mm bluegill pectoral ray", "lo": 1.9e-6, "hi": 7.6e-6, "units": "N m^2",
      "status": "open",
      "satisfied_by": "Three bluegill values disagree: Puri 2018 3.8e-6 (uncited relay, in window); Alben 2007 order-of-magnitude 1e-6 to 1e-5 (straddles), with an Alben-based back-calculated one-free EI of 1.07e-6 to 1.87e-6 (calculated, gap 4.3-7.5x, just below window); Flammang 2013 565e-6 (calculated in-vivo, 70x surplus), whose own abstract numbers (67 mN, 9.38 mm^-1) imply EI <= 2.9e-7 under elastic bending (my calculation, weak because the ray buckled). No measured passive EI at known length",
      "satisfied_evidence": "literature",
      "note": "Bluegill on both sides. Flammang et al. 2013 J Morphol 274:1044 (abstract, Europe PMC); Alben et al. 2007 J R Soc Interface 4:243 PMC2359861 (full-text via challenge-209; could-not-access for me); Puri et al. 2018 PMC5868929 (full-text via S6-D-D). Not unsatisfiable: the out-of-window values are calculated, not measured EIs"},
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "Ray cross-sectional diameter must scale in proportion to ray length between the 40.3 mm source ray and the 120 mm target ray",
      "quantity": "d(120 mm ray) / (2.98 x d(40.3 mm ray))", "lo": 0.84, "hi": 1.19, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Not measured in any species found: no fin-ray diameter/second-moment vs size series, and no exocoetid ray cross-section. Fish 1990 shows positive allometry of exocoetid fin span (b=0.375 vs 0.33) but nothing on diameter",
      "satisfied_evidence": "unknown",
      "note": "Cross-species (bluegill to exocoetid). Scope: Europe PMC lepidotrich*/allometry/stiffness/cross-section query (129 hits, first 60 titles screened) and exocoetid fin-ray query (45 hits, all screened), positive control 30 hits; upstream S6-D-D and S26-D-D searches concur. Not searched: Google Scholar, WoS, MorphoSource (oVert Exocoetus UF 231939 not opened). Nobody has looked, as far as reached; not a negative finding"},
    {"target_scale": "tissue", "kind": "range",
      "statement": "Composite ray modulus must be approximately size- and species-invariant between the source and target rays",
      "quantity": "E(120 mm exocoetid ray) / E(40.3 mm bluegill ray)", "lo": 0.5, "hi": 2.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No exocoetid ray modulus and no size series of lepidotrichial modulus in any species found; within-fin bluegill spread (0.24-3.7 GPa proximal) exceeds the window",
      "satisfied_evidence": "unknown",
      "note": "Same Europe PMC scope as C2 (query included modulus terms). Bluegill moduli: Lauder group via S26-organ (search-summary), Alben 2007 E ~1e8-1e9 Pa (full-text via challenge-209). Not measured, not found invariant"},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "The target organism of the requirement (0.1 kg) must have pectoral rays whose length matches the 120 mm used in the scaling, within a factor of 1.5",
      "quantity": "120 mm / pectoral fin base-to-tip length of a 0.1 kg fish", "lo": 0.67, "hi": 1.5, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Exocoetid wing-span regressions at M=0.1 kg: Cypselurus span 0.275 m -> fin 122-137 mm (ratio 0.87-0.98); Exocoetus span 0.323 m -> fin 147-161 mm (ratio 0.74-0.82), for body width 0-30 mm (assumed); fails only if body width >115 mm",
      "satisfied_evidence": "derived",
      "note": "Exocoetid on both sides: requirement is S6-D's 100 g flying-fish scenario (S6-D-deepen.md, f43d1afb); Fish 1990 J Zool 221:391 Table I (full-text), span = 0.651 M^0.375 (Cypselurus, n=113), 0.774 M^0.380 (Exocoetus, n=26). Assumes longest ray ~ fin length. Does NOT hold if the claim is read as about the project's zebrafish; the original S6 was a 0.4 g zebrafish"},
    {"target_scale": "organism", "kind": "conservation",
      "statement": "In steady glide, the weight must be carried by the pectoral rays in the proportion the per-ray requirement assumes (all weight on pectorals, shared equally over 14 rays per fin)",
      "quantity": "f_p x 14 / N (pectoral lift fraction x assumed/actual ray count)", "lo": 0.5, "hi": 2.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Area proxy only: pectoral fins are 76.0% (Cypselurus) to 91.8% (Exocoetus) of wing area (measured), giving 0.76-0.92 if lift scales with area (assumption) and N=14. No measured lift partition found; Park & Choi 2010 and their 2007 IUTAM paper (both search-summary) disagree on whether pelvic fins add lift. Exocoetid pectoral ray count unknown",
      "satisfied_evidence": "literature",
      "note": "Exocoetid on both sides. Fish 1990 J Zool 221:391 Table IV (full-text). Park & Choi 2010 J Exp Biol 213:3269 full text could-not-access (journal URL returned wrong article; typeset.io blocked by network allowlist). Requirement 6.3e-4 reproduced as (mg/28) L^2 / (8 x 0.1). Ray count: not found in Europe PMC exocoetid query (45 hits); taxonomic keys not searched. Excludes >1 g take-off/landing loads and unequal ray loading"}
  ]}
```
