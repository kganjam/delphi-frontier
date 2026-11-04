# Claim 96 — entailment check at tissue and organism scales

**Source claim (organ scale, evidence: derived).** The single measured
hemitrich-locking factor (~12x, Alben, Madden & Lauder 2007, clamped 1.98 N/m
vs one-base-free) closes a 2.1x gap with 5.7x margin, so ACTIVE STIFFENING CAN
CARRY THE LOAD — conditional on isometry holding and on fin muscles achieving
the excised-ray clamping factor in vivo.

**Arithmetic check (derived, not observed):** 12 / 2.1 = 5.71, so the stated
margin is internally consistent with the stated factor and gap.

**Context limitation.** This repository checkout holds no fish-project files.
Searching the tree for `hemitrich`, `Alben`, `exocoet`, `flying fish` and
`lepidotrich` returned no fish-model hits. So I could not recover where the
2.1x gap comes from (which load case, which fin, which body size). Any
constraint that depends on the load case is therefore left `open`.

## Who the numbers are about (read this first)

| Number | Animal | Preparation | Source | Read-level |
|---|---|---|---|---|
| 1.98 N/m clamped stiffness; "about 12 times" vs one hemitrich free | **Bluegill sunfish, *Lepomis macrochirus***, pectoral fin, ray 4 of 13 | **Excised** rays tested in water within 48 h of euthanasia; both hemitrich bases clamped by the apparatus, not by muscle | Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243 (PMC2359861) | full-text (via PMC, read through a summarising fetch) |
| Model locked/free ratio 3–100 depending on shear modulus G; the experiment matched G≈10² | Bluegill (model parameterised on bluegill rays) | Simulation / analytical model | same | full-text |
| Max ray length 40.3 ± 0.8 mm | Bluegill | Excised | same | full-text |
| "nearly 12 times" stiffness increase when relative hemitrich displacement is prevented | Bluegill sunfish | Excised; 3-point and cantilever tests | Lauder, Madden & McHenry, SICB abstract ([sicb.org/?p=32702](https://sicb.org/?p=32702)) | search-summary |
| Whole-fin bending stiffness 1.5–4 × 10⁻⁹ N m²; ray diameter 0.1–0.2 mm; fin thickness 200→40 µm | **Zebrafish, *Danio rerio***, caudal fin, adults 6–12 months | **In vivo, anaesthetised in MS-222** | Puri et al. 2018, *J Exp Biol* 221:jeb171777 (PMC5868929) | full-text (via PMC, read through a summarising fetch); per-position values only in Fig. 2C, which I could not read |
| Bluegill ray flexural stiffness ~5.65 × 10⁻⁸ N m² (one ray); ~10⁻⁶ N m², 3.8 × 10⁻⁶ N m², ray diameter 1–2 mm | Bluegill | Excised | Flammang et al. 2013 *J Morph*: the 5.65 × 10⁻⁸ value is from a search summary; the other values are as quoted by Puri et al. 2018 | search-summary / secondary citation |
| Larval pectoral fin = one abductor and one adductor sheet, on either side of an endoskeletal disc; these split into subdivisions by the end of the juvenile period | Zebrafish | Anatomy | Thorsen & Hale 2005, *J Morph* 266:241 (PMID 16163704) | abstract (via search-summary) |
| Each ray = two apposed, contralaterally symmetric hemirays (dorsal/ventral in paired fins), held together by soft tissue | Zebrafish | Anatomy | PMC3036817; PNAS 2010 figure legend (PMC2851957) | search-summary |
| In vivo EMG of fin muscles "consistent with … stiffening" | Bluegill (dorsal inclinators: Jayne, Lozada & Lauder 1996; caudal intrinsic muscles: Flammang & Lauder 2008) | In vivo EMG | Harvard Lauder-lab PDFs, as listed by search | search-summary |

**What this means for the claim.** The 12x locking factor is a **bluegill,
excised-ray, apparatus-clamped** measurement. The project's claims are mostly
about **zebrafish**. No source below is about flying fish, so the
exocoetid-versus-zebrafish trap does not arise here. A bluegill-versus-zebrafish
trap of the same kind does, and every verdict below respects it.

## Constraints

### C1 — tissue / existence — satisfied (structure only)
**Requirement.** The target fin ray must be made of two laminae that can slide
relative to each other, coupled by compliant tissue that resists shear.
Without this there is no sliding to lock, and "locking" has no mechanism.

**Check.** Zebrafish rays are made of two apposed hemirays, symmetric across the
fin plane, held together by soft tissue (PMC3036817 and the PNAS 2010 figure
legend PMC2851957; both search-summary). The source states this anatomy
directly for zebrafish.

**Scope note (my inference).** This satisfies *existence of the bilaminar
architecture* only. The shear modulus of the zebrafish inter-hemiray tissue is
`unknown`: I found no measurement of it. Puri et al. 2018 do not mention
hemirays, hemiray sliding or intra-ray ligament at all.

### C2 — tissue / range — unsatisfied (nobody has measured it; not a negative measurement)
**Requirement.** In the target species' rays, the ratio of stiffness with
hemiray bases locked to stiffness with one base free must be **≥ 2.1**. That is
the factor the claim needs; there is no upper bound. The bluegill excised value
of ~12 is the reference, not the requirement.

**Check.**
- *Bluegill (measured, excised):* ~12x (Alben et al. 2007, full-text). The
  authors' bluegill-parameterised model gives 3–100x over their range of G
  (simulated). Even the bottom of that range, 3x, exceeds 2.1x. This is a
  statement about *their model at bluegill geometry*. It is not a zebrafish
  measurement.
- *Zebrafish:* I found **no measurement** of a locked/free ratio. Puri et al.
  2018 measured whole-fin bending stiffness in vivo, but with the fish
  anaesthetised, and they never manipulated hemiray bases. So their data cannot
  give this ratio.
- **Scope of the negative:** searches for zebrafish fin ray / hemiray bending
  stiffness, mechanical testing of lepidotrichia, and in vivo hemitrich offset
  or active stiffening (three web searches, standard mode), plus full reads of
  PMC2359861 and PMC5868929. I could not reach cob.silverchair.com or
  ikarus.physik.uzh.ch from this session. Finding: **"nobody has looked"** in
  the sources reachable here. It is not "looked and found nothing".
- **Cross-species, informative but not a verdict:** nothing contradicts ≥ 2.1x.
  The bluegill model floor of 3x makes satisfaction plausible *if* zebrafish G
  and geometry are similar, which is exactly what C3 asks.

### C3 — tissue / spatial — open
**Requirement (isometry).** For the bluegill factor to transfer, the target ray
must be geometrically similar to the bluegill test ray. Ray length / ray
diameter must match the bluegill value within a factor of ~2. (The model's
locked/free ratio depends on G and on the geometric ratios, including d/L.)

**Bound (derived).** Bluegill: L = 40.3 mm (Alben et al., full-text) and
diameter 1–2 mm (Flammang et al., as cited by Puri et al.), so L/D ≈ 20–40.
Within a factor of 2, that gives **L/D in [10, 80]**.

**Check.** The zebrafish ray diameter is 0.1–0.2 mm (Puri et al. 2018,
full-text). Zebrafish ray *length* was not reported in Puri et al. (no standard
length or fin length given), and I found it in no source I read. So zebrafish
L/D is `unknown`, and I did not compute it from a guessed fin length.

Puri et al. compare bluegill and zebrafish whole-fin flexural rigidity and find
"reasonable agreement" (the authors' own claim). My inference: that agreement
concerns EI, not the dimensionless shear-coupling ratio that sets the locking
factor. It therefore does not establish isometry for this purpose. Bluegill d/L
is also given only non-dimensionally in Alben et al., so even the bluegill side
of a d/L comparison is incomplete.

### C4 — organism / existence — open
**Requirement.** Fin muscles must act differentially on the two hemiray bases of
a ray, so that they can hold the bases against relative sliding in vivo. This
is the "fin muscles achieving the clamping factor" condition.

**Check.**
- *Zebrafish:* the pectoral fin has an abductor and an adductor on opposite
  faces of the fin (Thorsen & Hale 2005, abstract via search-summary). Because
  the two hemirays of a paired-fin ray sit dorsal and ventral (PMC3036817,
  search-summary), opposed muscle sheets are *anatomically positioned* to load
  them differentially. That is my inference. I did not find a zebrafish source
  stating that muscle inserts onto individual hemiray heads, nor any
  measurement of the forces involved.
- *Bluegill:* in vivo EMG of dorsal inclinators (Jayne et al. 1996) and of
  caudal intrinsic muscles (Flammang & Lauder 2008) is described by the
  authors as consistent with stiffening (search-summary). That is the wrong
  animal for a zebrafish claim, and the right kind of evidence.
- Alben et al. 2007 state that muscles apply forces and moments at the base but
  do not quantify them (full-text). **No study I found, in any species,
  measured the in vivo locked/free stiffness ratio achieved by muscle**, as
  opposed to an apparatus clamp. Scope: same searches as C2.

### C5 — organism / timescale — open
**Requirement.** Muscle-driven locking must reach the needed force faster than
the load it must resist builds up. Muscle force rise time must be shorter than
the loading event's duration (for a stroke-cycle load, shorter than one
fin-beat half-period).

**Check — not performed, and cannot be from what is here.** The load case
behind the 2.1x gap is not recoverable from this checkout (see the context
limitation above). So the target duration is `unknown`. I did not search for
zebrafish fin-muscle twitch kinetics, because without the load timescale there
is nothing to compare them to.

## Verdict summary

| # | Scale | Kind | Status | Why |
|---|---|---|---|---|
| C1 | tissue | existence | satisfied | Zebrafish rays are bilaminar hemirays (anatomy literature) |
| C2 | tissue | range | unsatisfied | ≥ 2.1x known only for excised **bluegill** rays (12x); never measured in zebrafish — "nobody has looked" |
| C3 | tissue | spatial | open | Zebrafish ray length unknown in the sources read; isometry untested |
| C4 | organism | existence | open | Zebrafish muscle layout is compatible; no in vivo locking measured in any species |
| C5 | organism | timescale | open | Load case not recoverable here |

**No constraint is unsatisfiable.** I found no measured number, about either
animal, that contradicts the claim. The claim remains what it says it is: a
bluegill excised-ray number carried to another animal under two explicit
conditions, isometry (C3) and in vivo muscle clamping (C4). Neither condition
has been tested in any source I could reach.

```swarm-entail
{"source_claim": 96, "source_scale": "organ",
  "constraints": [
    {"target_scale": "tissue", "kind": "existence",
      "statement": "Fin rays of the target species must consist of two laminae able to slide relative to one another, coupled by shear-compliant tissue, so that base locking has something to lock",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Zebrafish lepidotrichia are two apposed contralaterally symmetric hemirays held together by soft tissue",
      "satisfied_evidence": "literature",
      "note": "PMC3036817 and PNAS 2010 fig. legend PMC2851957 (search-summary). Satisfies architecture only; zebrafish inter-hemiray shear modulus unknown, not reported in Puri et al. 2018 (PMC5868929, full-text)."},
    {"target_scale": "tissue", "kind": "range",
      "statement": "Locked-base / one-base-free stiffness ratio of target-species rays must be at least the factor the load gap requires",
      "quantity": "locked/free ray stiffness ratio", "lo": 2.1, "hi": null, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "Only measurement is ~12x in EXCISED BLUEGILL (Lepomis macrochirus) pectoral rays with apparatus clamping; bluegill-parameterised model gives 3-100x (simulated). No zebrafish measurement found.",
      "satisfied_evidence": "unknown",
      "note": "Alben, Madden & Lauder 2007 J R Soc Interface 4:243, PMC2359861 (full-text); Lauder/Madden/McHenry SICB abstract (search-summary). Negative scope: 3 standard web searches (zebrafish ray/hemiray stiffness; lepidotrichia mechanical testing; in vivo hemitrich offset/active stiffening) + full reads of PMC2359861, PMC5868929; cob.silverchair.com and ikarus.physik.uzh.ch unreachable. Finding is 'nobody has looked', NOT 'looked and found nothing'. Not a refutation: species differ."},
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "Isometry: target-species ray length/diameter must match the ray on which the locking factor was measured within a factor of ~2",
      "quantity": "ray length / ray diameter", "lo": 10, "hi": 80, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Bluegill L/D ~20-40 (derived: L=40.3 mm, Alben 2007; D=1-2 mm, Flammang 2013 as cited by Puri 2018). Zebrafish D=0.1-0.2 mm (Puri 2018) but zebrafish ray length not reported in sources read.",
      "satisfied_evidence": "unknown",
      "note": "Puri et al. 2018 J Exp Biol 221:jeb171777, PMC5868929 (full-text) report bluegill/zebrafish EI 'reasonable agreement' -- authors' claim about flexural rigidity, which (my inference) does not test the dimensionless shear-coupling geometry. Bluegill d/L only given non-dimensionally."},
    {"target_scale": "organism", "kind": "existence",
      "statement": "Fin musculature must act differentially on the two hemiray bases so as to restrain relative sliding in vivo, reaching the clamping factor without an external clamp",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Zebrafish pectoral fin has opposed abductor/adductor sheets on the two fin faces (anatomically compatible, my inference); bluegill in vivo EMG consistent with fin stiffening. No in vivo locked/free ratio achieved by muscle measured in any species.",
      "satisfied_evidence": "unknown",
      "note": "Thorsen & Hale 2005 J Morph 266:241 (abstract via search-summary); Jayne, Lozada & Lauder 1996 and Flammang & Lauder 2008, bluegill (search-summary); Alben 2007 states muscle forces are not quantified (full-text). Negative scope as for the range constraint."},
    {"target_scale": "organism", "kind": "timescale",
      "statement": "Muscle-driven base locking must reach required force faster than the hydrodynamic load it resists builds up (rise time < loading duration)",
      "quantity": "muscle force rise time / load duration", "lo": null, "hi": 1, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Not checked: load case behind the 2.1x gap not recoverable from this checkout, so load duration unknown",
      "satisfied_evidence": "unknown",
      "note": "Unchecked constraint; no literature search for muscle kinetics was run because the comparison timescale is undefined."}
  ]}
```
