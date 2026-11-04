# S15 — The minimal edit stack

**Project:** `zebrafish-flight` · **Scale:** dna · **Date:** 2026-11-04

---

## 1. The question, restated with the numbers that make it hard

Project premise (given, not measured by me): *Danio rerio*, 4 cm standard length,
~0.4 g.

> **Q.** What is the minimal ordered set of germline edits that would carry
> *D. rerio* from its wild morphology to an animal capable of a powered launch
> and a sustained aerial glide, and does every edit in that set have a
> *demonstrated zebrafish phenotype* attached to a *real allele or construct*?

The refutation criterion set by the project is sharp and I apply it literally:
**any edit in the stack lacking a demonstrated zebrafish phenotype refutes the
stack.** So the question is not "can I write a plausible gene list" — it is
"does every slot in the list have a published zebrafish mutant in it".

Three numbers make this hard.

1. **Weight to be carried: 3.92 mN.** 0.4 g × 9.81 m/s². Small, but it must be
   carried by a surface that currently does not exist.
2. **Wing area needed at a low launch speed: ~20 cm² (computation, §3).** The
   whole dorsal silhouette of a 4 cm zebrafish is on the order of 1.4 cm²
   (computation, §3, from assumed body width). The required lifting surface is
   therefore *larger than the entire animal viewed from above*, by about an
   order of magnitude, unless launch speed is high.
3. **Reynolds number: 10³–10⁴ (computation, §3).** A zebrafish-scale wing works
   in a regime where I could not source a lift coefficient or a lift-to-drag
   ratio for a ray-supported membrane at all. The aerodynamic coefficient that
   the area calculation depends on is **unknown**.

The hard part is that (1) and (2) are about *size* — and size is exactly the
axis along which zebrafish fin genetics is best developed. (3) is about
*stiffness, speed and control* — and along those axes the demonstrated-allele
cupboard is, as far as my searches reached, bare.

---

## 2. What is measured

Read-levels are per-source. Where a source and I disagree, or two sources
disagree, the disagreement is preserved and labelled.

### 2.1 Fin-size alleles with demonstrated zebrafish phenotypes

| Gene | Allele / construct | Demonstrated phenotype (author's claim) | Source | Year | Read-level |
|---|---|---|---|---|---|
| `kcnh2a` | `lof^dt2` (*longfin*); chromosome-2 inversion causing *cis* ectopic `kcnh2a` expression | "The inversion results in ectopic overexpression of the voltage-gated potassium channel kcnh2a in the fin … which we show is sufficient to drive coordinated overgrowth of the fin." All fins of `kcnh2a^lof/+` are overgrown. | Daane, Blum, Lanni, Boldt, Iovine, Higdon, Johnson, Lovejoy, Harris — bioRxiv 2021.03.05.434157 | 2021 | **full-text** (PDF text-extracted) |
| `kcnh2a` | `lof^dt2` + revertants `lfr1` (Y669N), `lfr2` (L739Q), `WL7` (Y418X); deletion line `lof^j6e1` = `lof^Df(Chr02:csnk1g2a,rnf2,kifap3b)j6g1/j6g1`, ZIRC `ZL1494` | Revertant nonsynonymous mutations in `kcnh2a` *in cis* were "essential for expression of the long-finned phenotype" | same preprint, Methods | 2021 | **full-text** |
| `kcnh2a` | *longfin* regulatory allele | Overgrowth is "a prolonged outgrowth period rather than increased maximal growth rate"; acts tissue-autonomously in the intra-ray mesenchymal lineage; late-stage Kcnh2a inhibition fully suppresses it | Stewart et al., *Development* 148(11) | 2021 | **search-summary** |
| `lat4a` | `lat4a^nr21` (= `dmh26`), T200K, **dominant gain-of-function**; `lat4a^del` (= `mh152`) | `nr21/+` adults have small fins and shortened lepidotrichial segments; no statistically significant effect on overall body size; *in-cis* CRISPR frameshift reverts to wild-type fin (proving gain-of-function, not haploinsufficiency); homozygous loss-of-function is "phenotypically normal and viable" | same preprint | 2021 | **full-text** |
| `kcnk5b` | `alf` (*another longfin*), gain-of-function point mutations | "alf mutants carry gain-of-function mutations in kcnk5b … Electrophysiological analysis in Xenopus oocytes reveals that these mutations cause an increase in K+ conductance." "Mutant Kcnk5b acts locally within the mesenchyme of fins and barbels to increase appendage size." | Perathoner et al., *PLoS Genetics* 10:e1004080 | 2014 | **search-summary** |
| `kcnk5b` | Ser345 | Calcineurin modification of S345 "regulates channel activity to scale the fin" | follow-up work indexed as PMC8110307 | 2021 | **search-summary** |
| `slc12a7a` / `kcc4a` | `schleier` (missense, loss-of-function; dominant-negative Kcc4a in wild-type also tested) | Heterozygotes show altered proportions across **all fins and barbels**; dominant-negative Kcc4a in wild-type removes growth restriction in fins and barbels; abrogating `kcnk5b` reverses the `schleier` overgrowth (epistasis → shared bioelectric pathway) | Lanni, Peal, Ekstrom, Chen, Stanclift, Bowen, Mercado, Gamba, Kahle, Harris — *Developmental Biology* | 2019 | **search-summary** |
| `cx43` | `sof^b123` (*short fin*; reduced mRNA, no coding lesion) + three ENU missense alleles | Fins "half the length of wild-type"; reduced segment length; reduced proliferation in regenerates; morpholino knockdown recapitulates. Authors propose Cx43-expressing cells are "a biological ruler that measures segment size." | Iovine et al. | 2005 | **search-summary** |
| `cx43` | `stp` vs `sof` alleles | Hemichannel vs gap-junction functions differ: `stp` shows ~50× wild-type transmembrane hemichannel currents; `sof` shows reduced gap-junction coupling | Misu et al. | 2016 | **search-summary** |

**Direction note:** `cx43^sof` and `lat4a^nr21` are size *reducers*. They enter
the stack only as modulators, never as wing-builders.

### 2.2 The one combination that has actually been built

This is the single most important measured fact in this file, and it is a
*combination*, which is what the project usually cannot get.

> "Double transheterozygous mutants between `kcnh2a^lof/+` and `lat4a^nr21/+`
> are viable and show specific variation in proportion among fins. While all
> fins of `kcnh2a^lof/+` are overgrown and all fins of `lat4a^nr21/+` are
> shortened, the `lat4a^nr21/+; kcnh2a^lof/+` transheterozygous fish showed
> wild-type sized medial fins while the paired fins were overgrown … the caudal
> fin … is hypocercal, with an elongated ventral lobe. The overall fin
> morphology pattern, and general bauplan, of the transheterozygous fish is
> thus remarkably similar to the fin phenotype of flying fishes."
> — Daane et al., bioRxiv 2021.03.05.434157, **full-text**

Published version: Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW,
Johnson SL, Lovejoy NR, Harris MP. "Modulation of bioelectric cues in the
evolution of flying fishes." *Current Biology* 31(22):5052–5061 (2021), DOI
10.1016/j.cub.2021.08.054; ZFIN `ZDB-PUB-210918-31`. **Read-level for the
journal version: search-summary.** My full-text read is of the preprint, whose
title differs ("Novel regulators of growth identified in the evolution of fin
proportion in flying fish"). I did not reconcile preprint and journal text, so
any number above may have changed in review.

**What the authors did *not* claim:** nothing in the text I read reports
gliding, aerial launch, aerial behaviour, or any out-of-water measurement on
these fish. My negative search for that is scoped in §5.

### 2.3 Muscle-mass alleles

| Gene | Construct | Phenotype (author's claim) | Source | Year | Read-level |
|---|---|---|---|---|---|
| `mstnb` | two independent **TALEN** knockout lines | Enhanced muscle growth via increased fibre *number*; no visible difference before juvenile stage; divergence after ~80 dpf; visceral and subcutaneous fat decreased, lipid accumulated in muscle | *Frontiers in Endocrinology* 7:88 | 2016 | **search-summary** |
| `mstnb` | CRISPR/**dCas9** targeted methylation of exon 2 (not a cut) | Raised methylation, suppressed `mstnb` mRNA; adults significantly longer and heavier than controls after 140 days | indexed summary of a methylation study | unknown | **search-summary** |

**Disagreement, preserved:** a review cites a zebrafish `mstnb`-deficient weight
increase of **~6.8 %**, which is much smaller than gains reported in grass carp
and blunt snout bream CRISPR `mstnb` mutants (**search-summary**, Research
Square preprint rs-9135348). The two are not averaged here. Note also the
mechanism disagreement across species: zebrafish and grass carp reports say
*more fibres, unchanged fibre thickness*; the blunt snout bream report says
*larger fibres*. I did not find a zebrafish `mstnb` CRISPR *knockout* (as
opposed to dCas9 methylation) in my searches.

### 2.4 Appendage-identity alleles

| Gene | Allele | Phenotype (author's claim) | Source | Year | Read-level |
|---|---|---|---|---|---|
| `hoxa13a`; `hoxa13b` | CRISPR double mutant (ZFIN `ZDB-CRISPR-190403-2`, `-3`) | Fin folds ~**30 % shorter** than wild type at 72 and 96 hpf; endochondral disk cell number ~**10 % greater**; "dramatic reduction and loss of fin rays … associated with an increased number of endochondral distal radials" | Nakamura et al., *Nature* 537 (doi 10.1038/nature19322) | 2016 | **search-summary** (PMC5161576 listed, not opened) |
| `hoxa13a` / `hoxa13b` / `hoxd13a` | single mutants | Each: four proximal radials and 6–8 distal radials, similar to wild type; `hoxa13a−/−` and `hoxa13b−/−` retained fin rays *shorter* than wild type | same | 2016 | **search-summary** |
| `hox13` | triple mutant | "highly ossified fin rays as seen in spines" | University of Ottawa thesis (ruor.uottawa.ca), author unknown to me | unknown | **search-summary** |

ZFIN phenotype terms for the double mutant, as reported: *pectoral fin distal
radial increased amount, abnormal*; *pectoral fin lepidotrichium decreased
length, abnormal* (**search-summary**).

### 2.5 Flying-fish aerodynamics (the target to be hit)

| Quantity | Value | Source | Year | Read-level |
|---|---|---|---|---|
| Max lift-to-drag ratio, stuffed flying-fish models in a wind tunnel | **~4.4**, described as greater than hawk (3.8) and petrel (4.0) | Park & Choi | 2008/2010 | **search-summary** |
| Drag reduction in ground effect, just above the water surface | up to **14 %** | same line of work | — | **search-summary** |
| Wing loading (body weight / wing area), Exocoetidae | **unknown** — numeric values not obtained | Fish (1990), 199 preserved specimens, 6 genera, 33 species; defined wing loading = weight/area and aspect ratio = span²/area; concluded exocoetid wing morphology resembles birds and bats more than other gliders | 1990 | **could-not-access** — the host `health-sciences.wcupa.edu` failed DNS resolution in this session; it must be added to the session's allowed network domains before I can read it |
| Aspect ratio, Exocoetidae | **unknown** — same failure | same | 1990 | **could-not-access** |
| Flying-fish launch / taxiing speed | **unknown** | — | — | **could-not-access**; not searched to exhaustion |

**Caveat carried from the source:** the wind-tunnel numbers are from stuffed
models, and commentators in the same search noted that inferring natural
behaviour from stuffed specimens has inherent limits. The 1990 morphometric
study and the wind-tunnel study used different methods and their numbers "should
not be compared directly" (**search-summary**).

### 2.6 Values I needed and could not measure or source

| Quantity | Status | What I tried |
|---|---|---|
| Adult zebrafish pectoral fin **area** (mm²) | **unknown** | Searched for adult zebrafish pectoral fin surface area and morphometrics; results returned taxonomic fin-*length* tables for other species and two zebrafish figure pages (a PMC box-plot figure; ZFIN figure from Gioia et al. 2017) that do not report pectoral fin area. No value obtained. |
| Fold-change in pectoral fin length in `lat4a^nr21/+; kcnh2a^lof/+` | **unknown** | Grepped the full preprint text. Fig 8B–C plots pectoral fin length normalised by standard length with Tukey HSD significance markers (`****` p≤0.0001, `**` p≤0.01), but **no fold-change or absolute length appears in the text I extracted**. The decisive magnitude is in a figure I did not read off. |
| Adult zebrafish burst/escape speed (BL s⁻¹ or m s⁻¹) | **unknown** | Searched for measured adult burst and escape speeds. Found only relative statements ("small fish capable of much higher relative speeds"), a flume study reporting *U*max differences of 18–24 % between sexes and a 14–20 % age-related reduction without absolute values, and critical-speed protocols. No absolute burst speed obtained. |
| C_L,max or L/D of a ray-supported fin membrane at Re 10³–10⁴ | **unknown** | Not found in the searches run; no source consulted. |
| Any zebrafish allele for aerial gas exchange / desiccation tolerance | **unknown / negative** | Scope in §5.3. |

---

## 3. What I computed

**Everything in this section is computation, not observation.** No value here
was measured by anyone.

### 3.1 Wing area required for steady gliding

Assumptions, stated: steady equilibrium glide with lift ≈ weight (shallow glide
angle); air density ρ = 1.225 kg m⁻³ (ISA sea level, a standard constant);
m = 4.0 × 10⁻⁴ kg from the project premise; g = 9.81 m s⁻²; and an **assumed**
lift coefficient C_L = 0.8, which I could not source for this Reynolds regime
(§2.6) and which is **generous** — a lower true C_L makes the required area
*larger*.

W = mg = 4.0 × 10⁻⁴ × 9.81 = **3.92 × 10⁻³ N**

S = 2W / (ρ V² C_L)

| Launch speed V | Arithmetic | Required wing area S |
|---|---|---|
| 1 m s⁻¹ | 7.84×10⁻³ / (1.225 × 1 × 0.8) = 7.84×10⁻³ / 0.98 | 8.0 × 10⁻³ m² = **80 cm²** |
| 2 m s⁻¹ | 7.84×10⁻³ / (1.225 × 4 × 0.8) = 7.84×10⁻³ / 3.92 | 2.0 × 10⁻³ m² = **20 cm²** |
| 5 m s⁻¹ | 7.84×10⁻³ / (1.225 × 25 × 0.8) = 7.84×10⁻³ / 24.5 | 3.2 × 10⁻⁴ m² = **3.2 cm²** |
| 10 m s⁻¹ | 7.84×10⁻³ / (1.225 × 100 × 0.8) = 7.84×10⁻³ / 98 | 8.0 × 10⁻⁵ m² = **0.80 cm²** |

The required area spans **two orders of magnitude** across a plausible launch-
speed range, and the launch speed is one of the values I could not source
(§2.6). **This, not the gene list, is the binding uncertainty.**

### 3.2 The area available to be re-grown

Assumption, stated and weakly held: a 4 cm zebrafish of maximum body width
~0.5 cm, with a planform shape factor ~0.7. These body dimensions are **my
assumption**, not a sourced measurement.

Dorsal silhouette ≈ 4 cm × 0.5 cm × 0.7 = **1.4 cm²** (computation)

Comparison (computation): the 20 cm² needed at a 2 m s⁻¹ launch is **≈ 14 ×
the entire dorsal silhouette of the animal**. The 0.80 cm² needed at 10 m s⁻¹
is **≈ 0.6 ×** it — i.e. at high launch speed the requirement falls inside the
range a pair of greatly enlarged pectoral fins could plausibly occupy.

I cannot convert either figure into "how many fold must the pectoral fin grow",
because adult pectoral fin area is **unknown** (§2.6).

### 3.3 Reynolds number

Assumptions: kinematic viscosity of air ν = 1.5 × 10⁻⁵ m² s⁻¹; mean chord c
taken from each candidate wing geometry. Re = Vc/ν.

- S = 20 cm², span 8 cm (2 × body length) → c = 2.5 cm; at V = 2 m s⁻¹:
  Re = 0.025 × 2 / 1.5×10⁻⁵ = **3.3 × 10³**
- S = 0.80 cm², span 4 cm → c = 0.2 cm; at V = 10 m s⁻¹:
  Re = 0.002 × 10 / 1.5×10⁻⁵ = **1.3 × 10³**
- Reference, a real flying fish wing, assuming c = 3 cm and V = 10 m s⁻¹
  (both **assumed**, since §2.5 values were inaccessible):
  Re = 0.03 × 10 / 1.5×10⁻⁵ = **2.0 × 10⁴**

So a zebrafish-scale wing operates at roughly **6–15 × lower Reynolds number**
than my assumed flying-fish reference (computation). The measured L/D ≈ 4.4 for
flying fish therefore cannot be transferred to this design, and I have no
sourced coefficient for the zebrafish regime.

### 3.4 Wing loading of the design

W/S at S = 20 cm²: 3.92×10⁻³ / 2.0×10⁻³ = **1.96 N m⁻²** (computation).
I cannot say whether this is above or below the exocoetid value, because that
value is **unknown** (§2.5, could-not-access).

---

## 4. The answer

### 4.1 The minimal edit stack, ordered

**Tier A — slots that are filled: real alleles, demonstrated zebrafish
phenotypes.** Evidence level: **literature**.

**A1. `kcnh2a`** — allele `lof^dt2` (*longfin*), a chromosome-2 inversion
driving *cis* ectopic `kcnh2a` in the intra-ray fin mesenchyme.
Demonstrated phenotype: coordinated overgrowth of all fins, by prolongation of
the outgrowth period rather than a faster growth rate. Available as the
characterised deletion line `lof^j6e1` at ZIRC (`ZL1494`); revertant alleles
`lfr1`, `lfr2`, `WL7` are reported as **no longer maintained nor frozen**.
*This is the wing-area module.*

**A2. `lat4a`** — allele `lat4a^nr21` (= `dmh26`), dominant gain-of-function
T200K. Demonstrated phenotype alone: small fins, shortened lepidotrichial
segments, body size unaffected.
*This is the proportioning module: it subtracts median-fin growth that A1 adds.*

**A1 × A2 is the minimal demonstrated stack, and it is two edits.** The
transheterozygote `lat4a^nr21/+; kcnh2a^lof/+` is viable and has enlarged paired
fins, wild-type median fins and a hypocercal caudal fin — a flying-fish-like
*bauplan*, demonstrated, by the authors' own claim, as a morphological
phenocopy. **My inference, separated from theirs:** this makes S15's stack
unusual in that the *combination*, not merely the parts, has a published
phenotype — which is exactly what this project normally cannot obtain.

Interchangeable alternatives for A1, each individually demonstrated:
`kcnk5b^alf` (gain-of-function; fins and barbels), `slc12a7a^schleier`
(loss-of-function/dominant-negative; all fins and barbels). The authors note
these are **not** equivalent to `kcnh2a^lof`: `kcnk5b^alf` and `kcc4a^schleier`
have irregular segmentation and blood-vessel patterning, whereas `kcnh2a^lof`
fins "appear to have normal segmentation and vessel patterning". For a wing,
that distinction is probably not cosmetic — see §6.

**A3 (optional) `mstnb`** — TALEN knockout lines. Demonstrated phenotype:
increased muscle mass via fibre number, from ~80 dpf. Magnitude disputed
(~6.8 % by one review; larger in other species). *Launch-power module, at best
partial.*

**A4 — a demonstrated edit that must be left OUT.** `hoxa13a;hoxa13b` double
mutant is the only demonstrated route toward a limb-like distal endoskeleton
(more distal radials) — and it achieves that **by losing the fin rays** and
shortening the fin fold ~30 %. The rays and their membrane *are* the airfoil.
**My inference:** the only demonstrated "make it more limb-like" edit in
zebrafish is aerodynamically destructive, and the stack must therefore keep the
ray-based fin and reject the limb analogy entirely. This is a substantive
finding, not a caveat.

**Tier B — slots that are EMPTY. No allele, no construct, no demonstrated
zebrafish phenotype found.** Evidence level: **unknown**.

| # | Required function | Demonstrated zebrafish edit |
|---|---|---|
| B1 | Spanwise flexural stiffness of the ray-and-membrane surface sufficient to carry ~3.92 mN of aerodynamic load without collapse | **unknown — none found** |
| B2 | Launch speed in the 5–10 m s⁻¹ band that §3.1 requires | **unknown — none found**; `mstnb` (A3) adds mass, not demonstrated speed |
| B3 | Aerial pitch/roll/yaw stability and fin kinematic control out of water | **unknown — none found** |
| B4 | Vestibular and visual function in air | **unknown — none found** |
| B5 | Gas exchange and desiccation tolerance across a seconds-long aerial phase | **unknown — none found** |
| B6 | Mass reduction (skeletal lightening) to offset A3's added muscle | **unknown — none found** |

### 4.2 The verdict

**Evidence level: `literature`** — for what exists. The flight claim itself is
**refused**.

A minimal **two-allele** stack (`kcnh2a^lof` + `lat4a^nr21`) is individually and
jointly demonstrated in zebrafish and produces flying-fish-like fin allometry.
That is the honest, positive deliverable. But by the project's own refutation
criterion the stack *for gliding* is **refuted**: six required slots (B1–B6)
contain no demonstrated zebrafish edit, so the minimal edit stack for flight
cannot presently be written down at all. What exists is a stack for a
**shape**, not for a **behaviour**, and no published zebrafish of any genotype
has been reported to glide.

---

## 5. What this does NOT establish

**5.1 It does not establish that the demonstrated stack produces any
aerodynamic function.** The Daane et al. claim is morphological phenocopy of
fin *proportion*. In the full text I read there is no gliding assay, no launch
measurement, no aerial behaviour, no wind-tunnel test, and no fin stiffness
measurement on these fish. "Looks like a flying fish's fin proportions" is not
"generates lift". I am explicitly **not** extrapolating from their claim to
function, and anyone who reads this file as a feasibility green light has
misread it.

**5.2 It does not establish the magnitude of the fin enlargement.** The single
number that would let me compare the demonstrated phenotype against §3.1 — the
fold-change in pectoral fin area or length in the transheterozygote — is
**unknown**. It is plotted in Fig 8B of the preprint as length normalised to
standard length with significance stars, and I did not read a value off the
figure. Without it, I cannot state whether the demonstrated stack closes 5 % or
80 % of the area gap. **The stack's adequacy is therefore undetermined, not
favourable.**

**5.3 Scope of my negative searches.** Each of these is a *negative result with
a stated scope*, not a proof of absence:

- *Gliding/flying zebrafish:* one web search ("zebrafish transgenic mutant
  aerial gliding airborne flight phenotype engineered"), search-summary level.
  Returned the Daane flying-fish work and a flying-fish *robot* paper. **No
  study of a zebrafish that glides or flies was found.** I did not search ZFIN
  phenotype ontology systematically, nor any patent or thesis literature.
- *Aerial respiration / desiccation:* one web search, search-summary level.
  Returned comparative work on *Kryptolebias marmoratus*, *Protopterus*,
  *Calamoichthys*, *Arapaima* and *Xenopus* — **no zebrafish mutant, engineered
  lung, or out-of-water survival study appeared.** I did not search zebrafish
  swim-bladder-to-lung literature, which plausibly exists and was recommended
  to me as the next step.
- *Burst speed, fin area, low-Re coefficients:* one search each; all returned
  nothing usable (§2.6). None of these is exhausted.

**5.4 It does not establish gene identity beyond what the authors wrote.**
`lat4a` is the symbol used in the paper. ZFIN search returned **no gene with
the symbol `lat4a`**; the closest record is `slc43a2a` (`ZDB-GENE-040426-964`),
zebrafish ortholog of human *SLC43A2*, for which *LAT4* is an older human name.
**I did not verify that the authors' `lat4a` is ZFIN `slc43a2a`.** Anyone
ordering a line on the strength of this file must resolve that first. A second
nomenclature discrepancy: the Daane preprint Discussion writes `kcnk5a^alf`,
whereas Perathoner et al. and every other source I read give the *another
longfin* gene as **`kcnk5b`**. I preserve the discrepancy rather than silently
correcting it; my reading is that `kcnk5a` is a typo in the preprint, but that
is my inference.

**5.5 It does not establish that the two edits are compatible with the rest of
the stack.** Demonstrated viability of `lat4a^nr21/+; kcnh2a^lof/+` says nothing
about a four- or ten-allele animal. `lat4a` is an amino-acid transporter whose
authors themselves warn of "complex and pleiotropic effects on cell nutrient
sensing and growth pathways", and note Lat4 knockout mice are smaller than
littermates. `kcnh2a` is the ether-à-go-go channel class; cardiac
electrophysiology in a stacked genotype is untested in anything I read.

**5.6 It does not establish the aerodynamic requirement itself.** §3 is
arithmetic on an assumed C_L of 0.8 in a Reynolds regime where I have no
coefficient at all, and on an assumed body width. If the true C_L at Re ~10³ is
0.3, every area in §3.1 roughly triples. The 20 cm² figure is a **computed
estimate under stated assumptions**, not a measurement and not a settled
requirement.

**5.7 It does not establish read-depth parity.** Only the Daane et al. preprint
was read as full text. Perathoner 2014, Lanni 2019, Iovine 2005, Nakamura 2016,
Stewart 2021, the `mstnb` work and the Park & Choi aerodynamics are all
**search-summary** level: I am relying on quoted abstract fragments and database
records, and a full-text read could change any phenotype description in §2.

**5.8 The Exocoetidae comparison is missing entirely.** Wing loading and aspect
ratio for real flying fish are **could-not-access** because
`health-sciences.wcupa.edu` would not resolve in this session. Until that host
is allowed in the session's network settings, or the 1990 Fish paper is obtained
another way, §3.4's computed 1.96 N m⁻² floats without a biological referent.

---

## 6. What would change the answer

Ordered by how much each would move the verdict per unit effort.

1. **Read the launch speed.** A measured adult zebrafish burst speed, and a
   measured exocoetid launch speed, would collapse the two-order-of-magnitude
   spread in §3.1 to a single number. Right now the design requirement is
   undefined, and that — not the gene list — is what blocks S15. *Measurement:
   high-speed video of C-start escape in adult *D. rerio*, absolute m s⁻¹.*
2. **Read Fig 8B off the published paper.** The fold-change in pectoral fin
   length in `lat4a^nr21/+; kcnh2a^lof/+`, together with a measured adult
   pectoral fin area, converts §4.1 from "a stack exists" to "the stack closes
   X % of the gap". This is the cheapest single number in the file and would
   move the answer immediately.
3. **Measure fin flexural stiffness.** B1 is the slot most likely to be
   quietly fatal: an enlarged fin membrane at 1.96 N m⁻² may simply fold.
   *Measurement: bending stiffness of excised `kcnh2a^lof` pectoral fins versus
   wild type, under static load in the mN range.* A result showing stiffness
   scaling worse than area would **refute the stack on physics**, independent
   of genetics — and note that `kcnk5b^alf` and `kcc4a^schleier` fins are
   reported to have *irregular segmentation*, which is a plausible stiffness
   liability and a reason to prefer `kcnh2a^lof` for A1.
4. **A low-Reynolds coefficient.** Any sourced C_L,max and L/D for a thin,
   ray-supported membrane at Re 10³–10⁴ would turn §3.1 from assumption-driven
   arithmetic into a bounded requirement.
5. **Exhaust the B5 search properly.** The zebrafish swim-bladder and
   gas-exchange literature was explicitly flagged as unsearched. A demonstrated
   zebrafish allele there would fill one of six empty slots; confirming its
   absence with a systematic ZFIN phenotype-ontology query would firm up a
   negative that is currently supported by one web search.
6. **Resolve `lat4a` → ZFIN.** A nomenclature check is near-free and is a
   prerequisite for the stack being *buildable* rather than merely *writable*.
7. **Design change that would most improve feasibility:** abandon the
   equilibrium glide and target a ballistic, ground-effect-assisted hop. §3.1
   shows the area requirement falls by 25× between 2 and 10 m s⁻¹, and ground
   effect is measured to cut drag up to 14 %. That shifts the project's burden
   from Tier A (fin area, where demonstrated alleles exist) to B2 (launch power,
   where none do) — which is a *worse* genetic position, and is itself a result
   worth recording.

---

```swarm-result
{"subproblem": "S15", "evidence": "literature",
  "answer": "The minimal demonstrated stack is two alleles — kcnh2a^lof(dt2) (longfin, cis-ectopic kcnh2a; coordinated fin overgrowth) and lat4a^nr21/dmh26 (dominant T200K; fin-size suppressor) — whose viable transheterozygote is published as a flying-fish-like fin-allometry phenocopy, but six required slots (membrane stiffness, launch power, aerial stability, vestibular/visual function in air, aerial gas exchange, mass reduction) contain no demonstrated zebrafish edit, so a minimal edit stack for gliding cannot be written and the stack is refuted by the project's own criterion.",
  "key_number": "~2.0e-3 m2 (20 cm2) computed wing area required at a 2 m/s launch with assumed C_L=0.8, versus ~1.4 cm2 whole-body dorsal silhouette — a ~14x shortfall that falls to ~0.6x only if launch speed reaches 10 m/s",
  "blocked_on": "measured adult zebrafish burst/launch speed; measured adult pectoral fin area and the fold-change plotted in Daane et al. Fig 8B; any C_L/L-D coefficient for a ray-supported membrane at Re 1e3-1e4; Exocoetidae wing loading and aspect ratio (Fish 1990 host health-sciences.wcupa.edu failed DNS and must be allowed in the session's network settings)"}
```
