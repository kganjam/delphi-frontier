# S23 — Can actinotrichia be stiffened by gain-of-function, given only loss-of-function is demonstrated?

Project: `zebrafish-flight`. Scale: protein. Date of work: 2026-11-04.

---

## 1. The question, restated precisely

S6 (ray stiffness) needs the paired fin of a 4 cm, ~0.4 g *Danio rerio* to act as a
load-bearing aerofoil spar. The protein-scale question routed here is narrower:

> Actinotrichia — the unmineralised fibrillar rods at the distal fin margin — are
> **necessary** for normal fin-fold and ray morphogenesis (demonstrated by `and1`/`and2`
> loss of function). Does any evidence, model, or design show that actinotrichia can be
> made **more numerous or stiffer** by gain-of-function, and would that raise fin
> flexural stiffness enough to matter for S6?

The numbers that make it hard, all pulled together in §2–§3:

| quantity | value | status |
|---|---|---|
| Whole adult zebrafish caudal fin bending stiffness `EI` | 1.5×10⁻⁹ – 4×10⁻⁹ N·m² | **measured** (Puri 2018) |
| `EI` required for a 0.4 g glider, 4 cm semi-span, 10 % tip deflection | 3.9×10⁻⁶ N·m² | **computed** (§3.1) |
| Shortfall factor | ~10² – 10³ × | **computed** |
| Measured Young's modulus of actinotrichia | **unknown** — no measurement found (§2.5) | — |
| Published gain-of-function experiment raising actinotrichia number or stiffness | **none found** (§2.3) | — |
| Structure-prediction model run on a designed And1/And2 variant | **not performed** (§3.3) | — |

The question therefore has two separable halves, and they have different answers.
**(a)** Is actinotrichial gain-of-function demonstrated? **(b)** Even if it were, is
actinotrichial stiffness the quantity S6 is limited by?

---

## 2. What is measured

Read-levels: `full-text` | `abstract` | `listing` | `search-summary` | `could-not-access`.
I accessed sources through a web search/fetch tool in a sandboxed container with no
institutional journal subscription; several primary PDFs were therefore reachable only at
abstract or search-summary level, and that is marked per item.

### 2.1 Actinotrichia composition and the loss-of-function result

- **Zhang J, Wagh P, Guay D, Sanchez-Pulido L, Padhi BK, Korzh V, Andrade-Navarro MA,
  Akimenko MA (2010). "Loss of fish actinotrichia proteins and the fin-to-limb transition."
  *Nature* 466(7303):234–237. doi:10.1038/nature09137.** — read-level: `search-summary`
  (bibliographic record + abstract text returned by search; PDF at nature.com not opened).
  - Authors' claim: And1 and And2 are "essential structural components of elastoidin";
    double morpholino knockdown of `and1` + `and2` gives "absence of actinotrichia and
    impaired fin folds"; `and` genes are present in teleosts and elephant shark, absent in
    tetrapods.
  - Rescue reported in the same work (via the double-knockdown description retrieved in a
    later search summary): rescue "in 85 % and 92 % of double morphants by injection of
    4 ng of `and1` or `and2` messenger RNA." Read-level: `search-summary`.
    *My inference, not the authors' framing:* this is a **restoration-to-wild-type** rescue,
    not a demonstration of supra-normal actinotrichia. It shows exogenous mRNA can supply
    missing protein; it does not show that adding protein above wild-type level adds
    actinotrichia.

- **Actinotrichia collagens.** A 2011 study (ZFIN record ZDB-PUB-110425-4) reports
  actinotrichia are formed by Collagen I plus a fish-specific second Collagen II encoded by
  `col2a1b`, and that these collagens plus `lh1` are required for actinotrichia and fin-fold
  morphogenesis. Read-level: `search-summary` (ZFIN listing + search snippet; primary
  article not opened). So actinotrichia are a **collagen-I/II fibril with And1/And2 as the
  non-collagenous partner**, not an And-only polymer.

### 2.2 The CRISPR null — and the part of it that cuts against the premise

- **Hanzelova P, Baird C, Keshinro B, Kadhom R, Lalonde RL, Akimenko MA (2026). "An
  essential role for actinotrichia in zebrafish fin patterning and courtship behavior."
  *Development* 153(16):dev204990. doi:10.1242/dev.204990. PMCID PMC13120675.** —
  read-level: `full-text` (open-access PMC text read, first ~100 k characters; final
  ~29 k characters not read).
  - Alleles (authors' description; no formal allele designations given in the text I read):
    `and1` 669 bp deletion removing exon 2 including the start codon; `and2` 269 bp deletion
    producing a truncated protein lacking 8 of 10 C-terminal repeats. Double homozygote
    `and1⁻/⁻;and2⁻/⁻`.
  - Authors' claim: double mutants **lack actinotrichia**; reduced fin-fold size; disorganised
    cell migration. Single mutants: no observable adult fin defect. This **confirms the
    morpholino result in a genetic null**, which removes the usual morpholino caveat.
  - Adult double mutants: fin length and width (normalised to standard length) significantly
    reduced; ray number significantly reduced; rays "shorter and wider … with irregularly
    spaced bone segments"; bifurcation rare or absent; hypural elements 4.5 ± 0.189 vs
    5.9 ± 0.125 in wild-type siblings.
  - **Each hemiray was thicker than in the wild type**, and hemirays were also wider.
  - No mechanical measurement of any kind is reported. No gain-of-function experiment is
    reported.

  *Separating claim from inference:* the authors report thicker, wider hemirays as a
  patterning phenotype. **My inference** is that this is mechanically load-bearing in the
  wrong direction for the S23 premise: rays still form without actinotrichia, and the
  second moment of area of the individual hemiray goes **up**, not down. See §3.2.

### 2.3 Gain-of-function: the negative search, with its scope stated

I searched for any published experiment that increases actinotrichia number, length,
diameter, or stiffness.

- Queries run (web search, English, no date restriction, run 2026-11-04):
  `actinodin and1 overexpression gain-of-function zebrafish fin fold ectopic expression`
  (extended mode); `and1 and2 zebrafish CRISPR mutant actinotrichia morpholino phenotype not
  recapitulated` (extended mode); `actinotrichia stiffness measurement atomic force
  microscopy nanoindentation fin fold mechanical` (extended mode); plus three standard-mode
  queries on actinotrichia composition and fin-ray mechanics.
- **Scope of the negative:** web-search index only; no PubMed/Web-of-Science systematic
  query, no preprint-server sweep beyond what the index surfaced, no hand-search of
  *Developmental Biology* / *Development* / *Dev Dyn* tables of contents, no patent search.
  A gain-of-function experiment published in a venue the index ranks poorly would be missed.
- **Finding:** no study found that overexpresses `and1` or `and2` above wild-type level, or
  otherwise augments actinotrichia, with a reported morphological or mechanical consequence.
  Related work found instead:
  - `and1` enhancer dissection: a 2 kb upstream fragment ("2P") recapitulates endogenous
    `and1` fin-fold expression (Lalonde et al., *Dev Biol*, 2016, S0012160616301245).
    Read-level: `search-summary`. This is a **reporter**, not an overexpression.
  - Overexpression in the fin fold has been done for *other* genes and goes the wrong way:
    `hoxd13a` overexpression causes distal endochondral expansion with **reduction** of the
    fin fold; `bmp2b` overexpression also **reduces** the fin fold with increased cell death.
    Read-level: `search-summary` (PMC8009906 snippet).

### 2.4 Fin mechanics that *is* measured

- **Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018). "In vivo quantification of
  mechanical properties of caudal fins in adult zebrafish." *J Exp Biol* 221(4):jeb171777.
  doi:10.1242/jeb.171777. PMCID PMC5868929.** — read-level: `full-text` (open-access PMC
  text read; supplementary figures S5B/S5C **not** accessed).
  - Whole-fin bending stiffness `EI` = **1.5×10⁻⁹ to 4×10⁻⁹ N·m²** along the
    proximal–distal axis, non-monotonic with a peak at ~2–4 mm from fixation that the
    authors state is *not* explained by fin geometry alone.
  - Fin thickness 200 → 40 µm; fin width ~5 → 8 mm; ray diameter 0.1–0.2 mm.
  - Effective area moment of inertia for the whole fin 7×10⁻¹⁶ → 3×10⁻¹⁶ m⁴.
  - Surgically cutting the interray tissue produced **no significant change** in bending
    stiffness; the authors conclude "the flexibility of the fin … predominantly relies on
    the mechanical properties of the rays."
  - Interray tissue effective modulus **4 ± 2 kPa**, stated by the authors as an upper bound.
  - Ray-level effective Young's modulus: reported only in supplementary Fig. S5C, which I
    could not access — `could-not-access`. A numeric ray modulus for zebrafish is therefore
    **unknown** to this analysis.
  - Cross-species anchor given by the authors: bluegill sunfish ray `EI` = 3.8×10⁻⁶ N·m².

- **Bony fin-ray modulus, other species** — read-level: `search-summary` (search snippet of
  a fin-ray mechanics study surfaced via sicb.org / Flammang et al. 2013 *J Morphol*; primary
  PDF not opened): mean proximal fin-ray modulus 1.34 GPa, range 0.24–3.7 GPa across rays;
  distal region 0.11–0.67 GPa. **Disagreement preserved:** this ~1 GPa-scale bony-ray figure
  and Puri's kPa-scale interray figure are measurements of different tissues, not competing
  estimates of one; but the >5-order spread means any "fin stiffness" number is meaningless
  without saying which element it refers to.

### 2.5 Actinotrichia mechanical properties: not measured

- No measurement of actinotrichial Young's modulus, fibril modulus, or bending stiffness was
  found. Scope of negative: the three search queries in §2.3 plus
  `elastoidin mechanical properties tensile modulus shark fin ray collagen measurement` and
  `actinotrichia elastoidin collagen type II zebrafish fin mechanical stiffness Young's modulus`
  (web index, 2026-11-04). No AFM, nanoindentation, or tensile study of actinotrichia or of
  elastoidin surfaced. **Value: `unknown`.**
- Published descriptions of actinotrichial mechanics are **qualitative only**: reviews
  describe elastoidin as conferring "a combination of rigidity and flexibility" and
  actinotrichia as "rigid, unmineralized fibrils that keep the fold straight."
  Read-level: `search-summary`.
- **Nakagawa, Kuroda, Aramaki, Kondo (2022). "Mechanical role of actinotrichia in shaping the
  caudal fin of zebrafish." *Dev Biol* 481:52–63. doi:10.1016/j.ydbio.2021.09.003.** —
  read-level: `abstract` (abstract + ZFIN figure listings; full text not opened). Using a
  `col9a1c` knockout, the authors report actinotrichia initially form and align normally but
  decrease in number and become disordered with growth; the caudal fin tip shortens
  dorsoventrally, the fin becomes oval, rays fuse instead of branching, and normally flat
  epithelial cells become spherical. Authors' conclusion: actinotrichial alignment "provides
  physical support in the dorsal-ventral direction." *My inference:* this is the strongest
  published support for a mechanical role, but it is a **shape/alignment** argument at the
  tissue scale, with no modulus or stiffness number attached.

### 2.6 Collagen fibril modulus — the material ceiling, with the disagreement intact

Read-level: `search-summary` across several AFM studies and reviews; no single primary
paper opened in full.

| state | reported modulus | source character |
|---|---|---|
| dry type-I fibril | 5 ± 2 GPa | AFM, one group |
| hydrated fibril (PBS) | 0.2 – 0.5 GPa | same group |
| hydrated sea-cucumber fibril | ~550 MPa | Eppell et al. |
| dry fibril | 1.9 ± 0.5 GPa | Yadavally et al. |
| hydrated fibril | 1.2 ± 0.1 **MPa** | Yadavally et al., Hertzian fit |
| hydrated, DMT contact model | 5 – 10 MPa | review-reported range |

**The disagreement is real and I am not averaging it.** Hydrated single-fibril modulus is
reported anywhere from ~1 MPa to ~0.5 GPa — a 500× spread — attributed by reviews to
hydration state, probe calibration, and choice of contact model. The 1.2 MPa figure may be a
unit error for GPa; the source summary itself flags it. For §3 I carry the **range**, not a
point value.

---

## 3. What I computed

Everything in this section is **computation**, not observation. Assumptions are stated
inline; each is a place the result can break.

### 3.1 How much flexural stiffness a 0.4 g glider needs

Assumptions:
1. Steady glide, so total lift = body weight; no gust or manoeuvre factor (this is the
   *generous* case — a gust factor of 2–3 would multiply the requirement).
2. Two wings share the load equally; each wing is modelled as a **cantilever beam** of
   length `L` (semi-span) with a **uniformly distributed** load `q = (W/2)/L`.
3. Uniform `EI` along the span (false in a real fin — Puri 2018 measures a non-monotonic
   profile — so this is an order-of-magnitude treatment only).
4. Serviceability criterion: tip deflection ≤ 10 % of semi-span. This is a convention
   borrowed from aeroelastic practice, **not** a measured avian/insect value, and is the
   softest assumption in the chain.

Arithmetic:

```
W   = 0.4e-3 kg × 9.81 m s^-2        = 3.924e-3 N
δ_tip for UDL cantilever              = q L^4 / (8 EI)   with q = (W/2)/L
  ⇒ δ_tip                             = (W/2) L^3 / (8 EI)
Set δ_tip = 0.10 L:
  EI_req  = (W/2) L^2 / (8 × 0.10)   = (W/2) L^2 / 0.8
```

| semi-span `L` | tip-deflection limit | `EI_req` (N·m²) |
|---|---|---|
| 2 cm (half a body length) | 5 % | 1.96×10⁻⁶ |
| 2 cm | 10 % | 9.81×10⁻⁷ |
| 2 cm | 20 % | 4.91×10⁻⁷ |
| 4 cm (one body length) | 5 % | 7.85×10⁻⁶ |
| 4 cm | 10 % | **3.92×10⁻⁶** |
| 4 cm | 20 % | 1.96×10⁻⁶ |

Against the measured whole-caudal-fin `EI` of 1.5–4×10⁻⁹ N·m² (Puri 2018):

- `L` = 2 cm, 10 % criterion → shortfall **245× to 654×**
- `L` = 4 cm, 10 % criterion → shortfall **981× to 2616×**

Sanity check that is not mine: Puri et al. note bluegill sunfish ray `EI` = 3.8×10⁻⁶ N·m²,
which lands inside my required band — i.e. the zebrafish would need the per-fin stiffness of
a fish two orders of magnitude heavier. That is an independent-of-my-algebra plausibility
check on the magnitude, not a confirmation of it.

**Caveat that weakens my own number:** Puri's `EI` is for the *caudal* fin, measured
in vivo on the whole fin. A glide wing would be the *pectoral* fin, which is not what was
measured. Using a caudal number as a pectoral proxy is an assumption with no calibration
behind it; I flag this junction as **uncalibrated**.

### 3.2 The lever arm: can a protein change reach 10³?

`EI` factorises into a material term and a geometric term. For a roughly cylindrical
element, `I ∝ r⁴`.

- **Geometric lever:** to gain 10³ in `I` alone, radius must rise by `1000^(1/4) = 5.6×`.
  A 5.6× thicker ray is a *developmental/geometric* change, not a protein-sequence change.
- **Material lever:** the honest upper bound for swapping a hydrated collagenous fibril for
  the stiffest plausible non-mineralised biopolymer. Taking the **most favourable** endpoints
  in §2.6 and the most favourable comparator:
  - hydrated collagen fibril, low end 0.2 GPa → dry-collagen-like 5 GPa = **25×**
  - hydrated collagen fibril, high end 0.5 GPa → dragline-silk-like ~10 GPa = **20×**
  - to reach cortical-bone-like ~20 GPa requires **mineralisation**, which is precisely what
    actinotrichia are not (they are defined as unmineralised); that is a different tissue,
    i.e. lepidotrichia, which the fish already has.

  So a material-only ceiling of roughly **20–25×**, and that is an upper bound assuming a
  protein redesign that fully converts hydrated-collagen mechanics into dry-collagen or
  silk-grade mechanics *in a wet tissue* — which nothing in §2 shows is achievable.

- **And the actinotrichial share of `EI` is not 100 %.** Puri 2018 measured that cutting the
  interray tissue did not change fin stiffness and concluded the rays dominate. In the adult
  fin the rays are **lepidotrichia** — mineralised bone — and actinotrichia are confined to
  the distal growing margin. **Computed consequence:** even a 25× material gain applied to a
  component that contributes a small and unmeasured fraction `f` of adult `EI` yields an
  overall gain of `1 + f(25−1)`, which is bounded by 25× and is far below that for small `f`.
  `f` is **unknown** — no study partitions zebrafish fin `EI` between lepidotrichia and
  actinotrichia.

**Computed bottom line:** best-case material-only gain ≈ 25×, against a requirement of
~10²–10³×, with the actinotrichial share of adult stiffness unmeasured and probably small.
The protein-scale lever is one to two orders of magnitude short even before discounting by `f`.

### 3.3 Sequence-level computation on the real And1/And2 proteins

I retrieved the actual sequences from UniProt (real accessions, fetched 2026-11-04):

- **And1: `E7F5V5`** (`Actinodin1 precursor`, *Danio rerio*, 570 aa)
- **And2: `A9JRX1`** (`Zgc:175106 protein`, 508 aa); a second entry `A0ACM8QEN9`
  (`Actinodin2 precursor`) carries the same length. I analysed `A9JRX1`.

Computation (Python, exact counts over the retrieved sequences — this is **computation on
real data**, not a measurement and not a simulation of structure):

| | And1 (570 aa) | And2 (508 aa) |
|---|---|---|
| Pro | 67 (11.8 %) | 60 (11.8 %) |
| Ala | 56 (9.8 %) | 54 (10.6 %) |
| **Tyr** | **47 (8.25 %)** | **29 (5.71 %)** |
| Cys | 16 (2.81 %) | 20 (3.94 %) |
| Gly | 31 (5.44 %) | 23 (4.53 %) |
| K+R / D+E (net) | 63 / 77 (−14) | 56 / 63 (−7) |
| perfect `Gly-X-Y` triple-helix windows (`G..G..G`) | **0** | **0** |
| exact repeated 12-mers | 0 | 0 |

Interpretation, marked as **my inference** from the computation:

1. **Zero canonical `Gly-X-Y` repeats confirms, by sequence, that actinodins are not
   collagens.** They are the non-collagenous partner in a collagen-I/`col2a1b` fibril
   (consistent with §2.1). A protein-design strategy that treats And1/And2 as the
   load-bearing tensile element is therefore likely mis-targeted; the tensile element is the
   collagen.
2. **Tyrosine enrichment (8.25 % in And1 vs ~3 % typical) is consistent with the published
   description of actinodins as "tyrosine-rich"** and is the one compositional feature that
   suggests a crosslinking role — di-tyrosine crosslinking is the mechanism by which
   tyrosine-rich matrix proteins stiffen elsewhere in biology. *This is a hypothesis
   generated from composition, not a measurement and not a model prediction.*
3. **Cys at 2.8 %/3.9 %** (16 and 20 residues) is consistent with disulphide-mediated
   network formation, again a crosslinking rather than a load-bearing role.
4. Hanzelova et al. describe And2 as having 10 C-terminal repeats; my exact 12-mer search
   found **no** exactly repeated 12-mers, so those repeats are **degenerate**, not identical.
   My search was for exact matches only and is the weaker test; I did not run a proper
   profile/HMM repeat analysis.

### 3.4 What I did **not** run, and why — this is the gap the deliverable asked to close

The subproblem asked for "candidate sequence or regulatory designs with a predicted
structural or mechanical consequence **from a real model run**."

**I did not run a structure-prediction or mechanics model, and I am not going to present
anything as if I had.** What I attempted and what blocked it:

- Sequence retrieval from UniProt: **succeeded** (§3.3).
- Structure prediction (AlphaFold/ESMFold class) on And1/And2 and on designed variants:
  **not attempted to completion.** The container is CPU-only with an ephemeral per-session
  disk allowance; ESMFold-class weights are multi-gigabyte and AlphaFold needs MSA databases
  far beyond the allowance. I did not find a usable hosted prediction endpoint reachable
  through the agent proxy within this task.
- Even if a fold had been predicted: actinotrichia stiffness is a **fibril-assembly** property,
  not a monomer-fold property. A predicted monomer structure would not yield a mechanical
  number. A coarse-grained fibril model would need the actinodin–collagen interaction
  geometry, which is **unknown** (§2.5).

Consequently the candidate designs below are listed as **hypotheses with no model run behind
them**, explicitly *not* as predictions:

| candidate | rationale | status |
|---|---|---|
| Increase di-tyrosine crosslink density (raise Tyr in And1 low-complexity regions) | And1 is Tyr-rich; di-Tyr crosslinking stiffens other matrix proteins | **hypothesis, untested, no model run** |
| Add cysteines for additional interchain disulphides | existing 16–20 Cys suggest a disulphide network | **hypothesis, untested, no model run** |
| Regulatory: drive `and1` from the validated 2 kb "2P" enhancer at higher copy, or extend its temporal window | 2P is reported sufficient to recapitulate endogenous expression | **hypothesis; note that no `and` overexpression phenotype is published at all** |
| Increase `col2a1b`/`col1a1` fibril diameter rather than And content | collagen is the tensile element (§3.3.1) | **hypothesis; and this is a collagen problem, not an actinodin one** |

None of these has a predicted structural or mechanical consequence attached, because no
model was run. Writing a number next to them would violate the honesty floor.

---

## 4. The answer

**Evidence level: `derived`** — resting on `full-text` reading of two primary papers
(Hanzelova 2026, Puri 2018), `abstract`/`search-summary` reading of the rest, real sequence
data, and explicit computation; **not** on any model run of a designed variant.

**Answer, in one line:** No — actinotrichial gain-of-function is not demonstrated anywhere
in the literature I could reach, *and* the computed leverage shows that even a best-case
protein-level stiffening (~25× material ceiling) falls 1–2 orders of magnitude short of the
~10²–10³× flexural-stiffness increase a 0.4 g glider needs, so S23 does not rescue S6.

Three findings, in decreasing confidence:

1. **(a) Gain-of-function is undemonstrated.** `literature`, negative, scope stated in §2.3.
   Every published actinodin manipulation is a loss: double morpholino (Zhang 2010), double
   CRISPR deletion (Hanzelova 2026), `col9a1c` knockout (Nakagawa 2022). The only
   gene-addition experiment is **rescue to wild type** with 4 ng mRNA, which restores and does
   not exceed. No overexpression, no supra-normal actinotrichia, no stiffness measurement.

2. **(b) The computed leverage is insufficient.** `derived`, §3.1–3.2. Requirement
   ~3.9×10⁻⁶ N·m² vs measured 1.5–4×10⁻⁹ N·m²; material-only ceiling ~20–25×; geometric
   lever (`r⁴`) is the dominant one and is not a protein-sequence variable.

3. **(c) The refutation criterion is partially met from the measured side.** `measured`
   (Hanzelova 2026, full-text; Puri 2018, full-text). Actinotrichia-null adults *still form
   rays*, and their **hemirays are thicker and wider** than wild type. Puri's cut experiment
   shows adult fin stiffness is dominated by the rays. Taken together — and this is **my
   inference**, not either paper's stated conclusion — actinotrichia look like a *patterning
   and alignment* element rather than the stiffness-limiting element of the adult fin. That
   is evidence that actinotrichial stiffness **is not what limits S6**, which is one of the
   two things the brief said would refute the premise.

The honest summary of the three: the question as posed ("can we stiffen actinotrichia?") is
probably the **wrong lever** for S6. If S6 fails on ray stiffness, the protein-scale target
that matters is the mineralised lepidotrichium and its geometry, not the unmineralised
actinotrichium and its matrix protein.

---

## 5. What this does NOT establish

Read this as carefully as §4. The negative above is narrower than it sounds.

1. **It does not show actinotrichia cannot be augmented.** It shows nobody has published
   trying. Absence of a gain-of-function paper is absence of evidence. My search was
   web-index-only (§2.3 scope) — no systematic PubMed/WoS query, no preprint sweep, no
   hand-search, no patent search, no correspondence with the Akimenko or Kondo labs.
   A successful overexpression could exist and be invisible to this search.

2. **It does not measure actinotrichial stiffness.** That number is `unknown` (§2.5). My
   §3.2 material-ceiling argument substitutes generic collagen-fibril moduli for
   actinotrichia. If actinotrichia are mechanically unlike generic hydrated collagen — and
   the elastoidin literature's "rigidity and flexibility" language hints they might be — the
   ceiling I computed is wrong by an unknown factor.

3. **It does not know `f`, the actinotrichial share of fin `EI`.** Every statement in §3.2
   about "probably small" is an inference from the *anatomical* fact that actinotrichia sit
   at the distal margin while lepidotrichia span the fin. No experiment partitions fin
   stiffness between them. If `f` is near 1 in the distal third — where a wing's torsional
   behaviour may actually matter most — my dismissal is too quick.

4. **The required-`EI` number rests on four soft assumptions** (§3.1): steady glide with no
   gust factor, uniform `EI`, UDL cantilever, and a 10 %-tip-deflection criterion I borrowed
   rather than derived. The last is the worst: no measured avian, chiropteran, or
   exocoetid tip-deflection tolerance backs it. Moving it to 50 % cuts the requirement 5×;
   adding a gust factor of 3 raises it 3×. The ~10²–10³ band is an order-of-magnitude
   statement, nothing finer.

5. **I used a caudal-fin measurement as a pectoral-fin proxy.** Uncalibrated junction,
   flagged in §3.1. Pectoral fins differ in ray count, ray geometry, and musculature.

6. **It does not establish that actinotrichia are dispensable.** Hanzelova 2026 shows the
   opposite for *patterning*: null fins are shorter, narrower, fewer-rayed, non-bifurcating,
   with fused hypurals and altered courtship behaviour. Any design that perturbs
   actinotrichia risks wrecking ray formation — which is the brief's second refutation
   condition, "cannot be raised without blocking ray formation," and I have **no** evidence
   either way on whether *raising* actinotrichia is as disruptive as removing them.

7. **No model was run** (§3.4). The candidate designs in §3.3/§3.4 have no predicted
   structural or mechanical consequence. The deliverable's own bar — "a real model run" —
   is **not met**, and this document should not be cited as if it were.

8. **Supplementary data I could not reach** may already contain the ray-level Young's
   modulus: Puri 2018 Figs. S5B/S5C. That is the single most valuable unread number here.

9. **Thicker hemirays in the null are open to the opposite reading.** I read them as evidence
   that ray stiffness is not actinotrichia-limited. They could equally be a disorganised,
   mechanically *worse* ray that happens to be thicker — the paper reports no mechanics, so
   neither reading is supported by data.

---

## 6. What would change the answer

Ordered by how much the answer moves per unit of effort.

1. **Measure actinotrichial modulus.** AFM or microtensile testing of isolated actinotrichia
   from larval fin folds, with hydration state controlled and reported. This converts the
   central `unknown` in §2.5 into a number and makes the §3.2 ceiling real rather than
   borrowed. *Single highest-value experiment.*
2. **Partition fin `EI` between lepidotrichia and actinotrichia.** Repeat Puri's in-vivo
   bending protocol on `and1⁻/⁻;and2⁻/⁻` adults versus wild-type siblings. The mutants exist
   (Hanzelova 2026). If null-fin `EI` is unchanged, S23 is closed negatively and definitively.
   If it drops substantially, `f` is large and this subproblem reopens.
3. **Read Puri 2018 Figs. S5B/S5C.** Zero-cost relative to the above; supplies the ray-level
   effective modulus and `I_eff` that §3.1 currently lacks.
4. **Do the overexpression experiment that does not exist.** A heat-shock-inducible or
   fin-fold-enhancer-driven `and1`/`and2` line, scored for actinotrichia number, diameter,
   and alignment. Any result — more, same, or developmental disruption — converts the §4(a)
   negative from "unpublished" to "tested." Note this needs no protein design at all, which
   is itself informative about where the real bottleneck sits.
5. **Run an actual model.** Coarse-grained fibril mechanics of a collagen-I/`col2a1b`
   fibril with and without And1/And2 crosslinking, parameterised by (1). Monomer folding
   alone will not answer the question (§3.4).
6. **Re-aim the subproblem.** If (2) shows actinotrichia are not stiffness-limiting, the
   protein-scale question S6 actually needs is about lepidotrichial mineralisation and
   geometry — a different gene set and a different document.
7. **A systematic literature search** (PubMed + Web of Science + bioRxiv, with recorded query
   strings) to properly bound the §2.3 negative, which is currently web-index-only.

---

## Sources

- [Zhang et al. 2010, *Nature* 466:234–237 — ZFIN record](https://zfin.org/ZDB-PUB-100625-29) · [nature.com](https://www.nature.com/articles/nature09137) — `search-summary`
- [Hanzelova et al. 2026, *Development* 153(16):dev204990 — PMC13120675](https://pmc.ncbi.nlm.nih.gov/articles/PMC13120675/) · [journal](https://journals.biologists.com/dev/article/153/16/dev204990/371312/An-essential-role-for-actinotrichia-in-zebrafish) — `full-text` (partial: first ~100 k chars)
- [Puri et al. 2018, *J Exp Biol* 221(4):jeb171777 — PMC5868929](https://pmc.ncbi.nlm.nih.gov/articles/PMC5868929/) — `full-text` (main text; supplements `could-not-access`)
- [Nakagawa et al. 2022, *Dev Biol* 481:52–63 — ZFIN record](https://zfin.org/ZDB-PUB-210922-3) — `abstract`
- [Lalonde et al. 2016, *Dev Biol* — "Differential actinodin1 regulation in zebrafish and mouse appendages"](https://www.sciencedirect.com/science/article/pii/S0012160616301245) · [related PMC6497306](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6497306/) — `search-summary`
- [Actinotrichia collagens (col2a1b, lh1) — ZFIN ZDB-PUB-110425-4](https://zfin.org/ZDB-PUB-110425-4) — `search-summary`
- [Hoxd13/Bmp2 finfold overexpression — PMC8009906](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8009906/) — `search-summary`
- [Flammang et al. 2013, *J Morphol* — fin ray mechanics](https://sites.harvard.edu/glauder/files/2022/03/Flammang.etal_.2013.JMorph_finrays.pdf) — `search-summary`
- Collagen fibril modulus values — `search-summary` across [PMC2257912](https://pmc.ncbi.nlm.nih.gov/articles/PMC2257912), [PMC4213719](https://pmc.ncbi.nlm.nih.gov/articles/PMC4213719), [encyclopedia.pub review](https://encyclopedia.pub/entry/21308)
- UniProt sequences, fetched 2026-11-04: [E7F5V5 (And1)](https://rest.uniprot.org/uniprotkb/E7F5V5), [A9JRX1 (And2)](https://rest.uniprot.org/uniprotkb/A9JRX1) — `full-text` (sequence records)

```swarm-result
{"subproblem": "S23", "evidence": "derived",
  "answer": "No published gain-of-function raises actinotrichia at all, and the computed material-only ceiling for stiffening an unmineralised collagenous fibril (~20-25x) is one to two orders of magnitude short of the ~10^2-10^3x fin flexural-stiffness increase a 0.4 g glider needs, while actinotrichia-null adults still form rays with thicker hemirays - so actinotrichial stiffness is probably not what limits S6.",
  "key_number": "shortfall factor 245x-2616x between required EI 9.8e-7 to 3.9e-6 N*m^2 (computed) and measured adult zebrafish caudal fin EI 1.5e-9 to 4e-9 N*m^2 (Puri et al. 2018)",
  "blocked_on": "no measured Young's modulus for actinotrichia anywhere in the literature; no structure/fibril-mechanics model run performed (CPU-only ephemeral container, no usable hosted prediction endpoint); Puri et al. 2018 supplementary Figs. S5B/S5C (ray-level effective modulus and I_eff) could not be accessed"}
```
