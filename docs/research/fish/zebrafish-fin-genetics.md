# Zebrafish fin genetics, assessed against a gliding-flight target

**Question posed:** could real genetic manipulation of *Danio rerio* produce an animal that glides?

**Short answer, stated up front:** no — and the literature says why, not merely that evidence is
missing. The well-characterised fin-overgrowth alleles are real and some are startlingly clean
single-locus levers, but every one of them is documented as acting on **ray length, segment count,
or whole-body fin proportion**, through ion-flux control of how long outgrowth continues. None is
documented as producing a stiff, cambered, muscled, lift-bearing surface, and none is documented as
pectoral-restricted. The honest gap is not "untested combination"; it is that the trait being
engineered (fin *extent*) is not the trait gliding requires (span-wise flexural stiffness plus
launch kinematics plus body rigidity). Section 5 argues this quantitatively-as-possible and gives
the probability discussion.

This document is a literature assessment and candidate-target catalogue. It deliberately stops at
the level of *which genes are implicated by published work*. It is not a construction protocol, and
I have not written injection recipes, doses, or a germline procedure — partly because the honest
conclusion is that the stack does not work, and partly because animal-welfare review (§6) is a real
precondition, not a formality.

---

## 0. Access constraints — read this before trusting any row below

This matters more than usual, so it comes first.

**In this session I could not reach any primary source.** The sandbox network policy returned
`CONNECT tunnel failed, response 403` for `pmc.ncbi.nlm.nih.gov`, `zfin.org`, and
`journals.plos.org`, and DNS failed for `www.sciencedirect.com` and `www.biorxiv.org`. I verified
the proxy itself was healthy (`/__agentproxy/status` → `"enabled": true`) before concluding the
block was policy, not breakage. To read full text, those hosts need allowing in the session's
network settings.

Consequence, stated plainly:

- **Every citation below is read-level `search-summary`.** Not one is `full-text` or even
  `abstract`. I read search-engine summaries of these papers, not the papers.
- **Not one ZFIN allele ID (`ZDB-ALT-…`) in this document is verified, because ZFIN was
  unreachable.** Every such cell reads `unknown`. I have *not* filled them from recall. Some of
  these IDs are the kind of thing a model can half-remember, and a half-remembered accession that
  looks authoritative is exactly the failure mode this repo's rule 2 and rule 3 exist to stop.
- **Measured fold-changes are mostly `unknown`** for the same reason: effect sizes live in figures
  and results sections, which I did not see.
- Allele designations that *do* appear below (`sof b123`, `alf dty86`, `rapunzel c14`, `longfin t2`,
  `lat4a nr21`) appeared inside search summaries. They are reported at that read-level and should be
  re-checked against ZFIN before use.

Per `CONTRIBUTING-VERIFICATION.md` §3: treat this entire file as *unread-source* tier. It is a map
of where to look, not evidence.

---

## 1. Fin-overgrowth alleles — catalogue

One correction to the starting list before the table: **`short fin` (*sof*) is not a fin-overgrowth
mutant.** It is the opposite — a *short*-fin loss-of-function allele. It is kept in the table
because it is mechanistically informative (it is the segment-length lever run backwards), but it
belongs in a glider stack only as a gene to *avoid* disrupting.

| Locus | Gene symbol | ZFIN allele ID | Molecular lesion | Measured fold-change in fin length | Mechanism | Source (read-level) |
|---|---|---|---|---|---|---|
| `longfin` (*lof*) | *kcnh2a* (ether-a-go-go K⁺ channel) | `unknown` — ZFIN unreachable; allele appears as "longfin t2" in summaries | Chromosomal **inversion**; reported to place the *prrx1a* regulatory region upstream of the *kcnh2a* transcription start site → *cis*-ectopic *kcnh2a* expression in fin. Not a coding lesion. | `unknown` | Bioelectric. Authors report overgrowth comes from a **prolonged growth period, not faster growth**; late Kcnh2a blockade stopped extra growth; proposed to act by suppressing calcineurin signalling that would otherwise terminate growth. Transplant data placed the effect in intra-ray mesenchyme (cell-autonomous, not systemic). | Stewart et al. 2021, *Development* (search-summary) |
| `another longfin` (*alf*) | *kcnk5b* (two-pore-domain K⁺ channel) | `unknown`; allele appears as "alf dty86" | **Gain-of-function** point mutation (W169L appears in summaries as a variant used in overexpression) | `unknown` | Bioelectric. Overexpression alone is **sufficient** for overgrowth. A **non-conducting** channel version produced no phenotype — ion flux is the signal, not the protein's presence. Mosaic clones gave *localised* overgrowth. | Perathoner et al. 2014, *PLoS Genetics* (search-summary) |
| `schleier` | *slc12a7a* / *kcc4a* (K⁺-Cl⁻ cotransporter) | `unknown` | **C583Y** missense; reported to decrease Kcc4a expression in fin mesenchyme | `unknown` — reported as a *proportional* increase, not an absolute length | Ion-transport. **Dominant** increase in relative proportion of fins **and barbs**; separate recessive pigment-stripe phenotype. A Lanni-lab review notes the **null has no fin phenotype**, so the allele is interpreted as **dominant-negative** — an important distinction for any "knock it out" plan. | Lanni et al. 2019, *Developmental Biology* (search-summary); author list not confirmed |
| `rapunzel` (*rpz*) | *rpz* — teleost-specific gene family (*rpz*, *rpz2–4*), **no tetrapod homologue described** | `unknown`; allele appears as "rapunzel c14" | Missense, reported as **gain-of-function** (homozygous embryonic phenotype suppressed by *rpz* morpholino knockdown) | `unknown` in fold-change terms, but the *axis* is explicit: **excess number of ray segments**, with **no significant difference in segment length** vs wild type | `unknown` mechanistically — gene was uncharacterised. Not bioelectric, not calcineurin, not gap-junction as far as these summaries show. A 2025 preprint reports *rpz5* in haematopoiesis and homozygous *rapunzel* vascular/blood defects — i.e. **pleiotropy**. | Green et al. 2009 (search-summary); Goldsmith et al. 2003 (listing); rpz5 preprint 2025 (search-summary) |
| `short fin` (*sof*) — **short, not long** | *cx43* / *gja1* (connexin 43, gap junction) | `unknown`; allele appears as "sof b123" | *sof b123*: reduced *cx43* mRNA. Three further ENU alleles: missense. | **~half wild-type fin length** (*sof b123*) — the one quantitative figure I obtained | Gap junction. Short **segments**; reduced proliferation. Cx43 influences **joint placement** and may suppress joint formation. Morpholino knockdown recapitulates. | Iovine et al. 2005 (search-summary); Hoptak-Solga et al. 2008 (search-summary) |
| `lat4a` (added — not in the original list) | *lat4a* (amino-acid transporter) | `unknown`; allele appears as "lat4a nr21" | `unknown` | `unknown` | **Medial-fin suppressor** of *kcnh2a* overgrowth. `lat4a nr21/+` **shortens** all fins; double mutants viable; effects **non-additive** with *lof*. | Daane et al. 2021, *Current Biology* 31(22), doi 10.1016/j.cub.2021.08.054 (search-summary) |

### Mechanistic convergence — and why it is bad news for a stack

*kcnh2a*, *kcnk5b*, and *slc12a7a/kcc4a* are all **K⁺-flux genes feeding a shared
bioelectric→Ca²⁺→calcineurin axis**. Reported supporting links: FK506 (calcineurin inhibitor)
decreases conductance in *kcnk5b*-expressing cells; Kcnk5b bioelectric signalling is **required**
for calcineurin-inhibition-driven growth; a later preprint states K⁺ gain-of-function and
calcineurin inhibition "likely disrupt the same ion signalling mechanism."

**My inference, not the authors' claim:** if three of the five overgrowth levers are nodes on one
pathway, stacking them should be **sub-additive or saturating**, not multiplicative. The *lof* ×
*lat4a* non-additivity that Daane et al. *do* report is direct evidence that fin-size epistasis in
this system is non-additive. Anyone budgeting "4 edits × 1.5× each = 5× fin" is assuming additivity
the one published double-mutant measurement argues against.

---

## 2. Which axis does each allele control?

A glider needs **area**, **span**, and a **stiff spar**. Sorting the alleles by axis:

| Axis | Allele(s) | Comment |
|---|---|---|
| **Duration of ray outgrowth** (→ length) | *longfin* / *kcnh2a* | Explicitly a longer growth *period*, not faster growth. Gives length. |
| **Segment length** (joint spacing) | *alf* / *kcnk5b* (overlong segments via joint failure); *sof* / *cx43* (short segments) | *alf*'s overlong segments come from **joint failure**. See the stiffness note below — this is a liability, not an asset. |
| **Segment number** | *rapunzel* / *rpz* | More segments, **same length each**. More joints per unit span. |
| **Proportional / allometric scaling** | *schleier* / *kcc4a*; *alf* also described as allometric | Scales fins *and barbs* together — relative, not targeted. |
| **Ray branching** | `unknown` for all rows | I found no allele in these searches whose primary documented axis is bifurcation. Scope: five web searches on overgrowth alleles; I did not run a dedicated branching-morphogenesis search. Do not read this as "none exists." |
| **Ray number** | `unknown` for all rows | Same scope caveat. Ray number is plausibly set at fin-bud patterning, upstream of all of these. |
| **Inter-ray membrane** | `unknown`; *and1/and2* (§4) affect fin **fold** integrity in embryos | The membrane is what would carry area between rays, and it is the least characterised axis in what I could read. This is a real hole. |

### The answer to "which alleles move area and span with a stiff spar"

**None of them — and two of them actively work against stiffness.** This is the single most
important finding in the document.

- *alf* and *sof* both act on **joints**. *alf* lengthens segments by **failing to make joints**.
- A fin ray is a segmented, jointed structure; it is **compliant by design**, because a fin is an
  oscillating thrust surface, not a cantilever.
- *rapunzel* adds **more joints** per span — plausibly *more* compliant, not less. (My inference
  from the reported "excess segments, unchanged segment length"; the authors make no stiffness
  claim.)
- Flexural stiffness of a beam scales with the **fourth power of its depth** (`I ∝ d⁴` for a solid
  section) and **inversely with the cube of its length** in tip deflection under end load
  (`δ ∝ L³/EI`). So **lengthening a ray while holding its cross-section and material constant makes
  tip deflection grow as L³.** Doubling ray length at constant section is roughly an **8×** increase
  in tip droop for the same load. That is textbook beam theory applied by me, not a result from any
  cited paper — but the scaling is not controversial, and it means every length-increasing allele in
  §1 makes the stiffness problem *worse*, not better.

So the catalogue delivers exactly what the brief feared: **alleles that lengthen a flimsy ray.**
They move span and area; they do not deliver a spar.

---

## 3. Pectoral vs caudal — the targeting problem

**The alleles are not pectoral-specific.** Reported scope of action:

- *kcnh2a* / *lof*: **all fins** overgrown in `lof/+`. Daane et al. ran qRT-PCR on pectoral *and*
  dorsal fins of inversion carriers, and report *kcnh2a* **not detected in wild-type fins** — so the
  allele's effect is ectopic expression broadly across fins, not a pectoral programme.
- *lat4a* / `nr21`: **all fins** shortened; described as a **medial**-fin suppressor.
- *kcnk5b* / *alf*: fins **and barbels**; a 2018 report covers **both pectoral and caudal**
  regeneration.
- *kcc4a* / *schleier*: fins **and barbs**.

### Pectoral-restricted drivers: the honest negative

**I found no verified pectoral-*restricted* driver or enhancer in zebrafish.** Scope of that
negative, stated as required: it rests on **two** web searches (one on
`tbx5a`/`hoxd13a`/Gal4 pectoral drivers, one on pectoral-specific `kcnk5b` overexpression), with
**no access to ZFIN's transgenic-line catalogue**, which is precisely where such a line would be
registered. This is a weak negative. It means "I did not find one," not "there is none." A ZFIN
query is the obvious next step and I could not run it.

What I did find, per-candidate:

- ***tbx5a* CNS12** — a downstream enhancer, conserved fish-to-mammal. In reporter transgenics it
  drove expression in the pectoral fin field, and CNS12-driven *tbx5a* **partially rescued** the
  finless *heartstrings* mutant. **But it is not pectoral-restricted:** the same summary reports
  CNS12 driving GFP in the **dorsal eye** as well as pectoral fin. (search-summary)
- **Conflict in the sources, flagged rather than smoothed:** one study reports the **mouse** *Tbx5*
  intron-2 element **did not** drive pectoral-fin expression in zebrafish, which sits awkwardly with
  the broader conservation framing. I could not read either paper to adjudicate. (search-summary)
- ***hoxd13a* regulatory elements** — **nothing found.** My searches returned no *hoxd13a* pectoral
  enhancer or driver line. The nearest hit was a *Hoxd13/Bmp2* fin-fold study (listing only, not
  read) and *hoxba*/*hoxbb* cluster work where deletion **removes pectoral fins** and abolishes
  *tbx5a* induction — upstream patterning, not a usable tissue-restricted driver. (search-summary)
- **FGF-based drivers** — `unknown`. I did not find a characterised pectoral-restricted FGF driver;
  I also did not search for one specifically. Scope: not searched.
- **Gal4 enhancer-trap screens** exist at scale in zebrafish (one screen reported 63 tissue-specific
  driver lines). **None was reported as pectoral-restricted** in what I read. (search-summary)

**Why this is a hard structural problem, not a missing reagent.** Even granting a perfect
pectoral-restricted driver, *tbx5a* and *hoxd13a* are **limb/fin-field identity and patterning**
genes acting in the **embryonic bud**. The overgrowth alleles act on **post-embryonic ray
outgrowth** in a different tissue (intra-ray mesenchyme) at a different stage. A bud-stage
pectoral-identity enhancer is therefore **the wrong driver in the wrong window** for a ray-outgrowth
effector. The 2024 PLOS Biology work *does* show pectoral **bud** scale responds to *kcnk5b* /
*kcnk10a* overexpression via K⁺ → Ca²⁺ → CaMKK → *shha* — so the bud is K⁺-responsive — but that is
bud scaling, and I have no evidence it yields a persistent adult wing. (search-summary)

---

## 4. Stiffness — what is actually known

Two skeletal systems in a fin ray:

- **Actinotrichia** — unmineralised, collagenous/elastoidin fibrils, distal, act as the growth
  scaffold.
- **Lepidotrichia** — the mineralised bony ray segments, proximal.

Published genetic handles:

| Target | What is reported | Read-level |
|---|---|---|
| ***and1* / *and2*** (actinodins) | **Double** knockdown in embryos → **absence of actinotrichia** and **impaired fin folds**. Both contribute, with distinct expression patterns. Actinotrichia and lepidotrichia reported **complementary** during regeneration. Also the gene family whose **loss** is tied to the **fin-to-limb transition** — i.e. these are the fish-specific fin-stiffening proteins. | search-summary |
| ***entpd5*** | **Essential** for skeletal mineralisation; mutants **lack ossification**; expressed **only in osteoblasts**; rescued by high inorganic phosphate; acts with *enpp1* in a phosphate/pyrophosphate balance. | search-summary |
| ***sp7* / osterix** | Marker of **intermediate** osteoblast differentiation; reduced on *pth4*-cell ablation, interpreted as impaired osteoblast maturation. | search-summary |
| ***pth4*** | Targeted ablation of *pth4*-expressing cells **impairs** skeletal mineralisation. | search-summary |
| **Collagen genes** | `unknown` — my mineralisation search returned **nothing** on collagen in the actinotrichia/lepidotrichia context. Scope: one search. Given actinotrichia are collagenous, this is near-certainly a gap in *my search*, not in the literature. | could-not-access |

### Candidate stiffening targets — **my proposal, not published fact**

Flagged explicitly as proposal. None of these has been shown to stiffen a fin:

1. **Up-regulate *and1*/*and2*.** The *loss*-of-function direction is demonstrated (no actinotrichia).
   **Gain**-of-function stiffening is **not demonstrated** — and the loss-of-function result does not
   imply the gain works. Dose-response may saturate or mis-assemble fibrils.
2. **Increase lepidotrichia mineralisation** via the *entpd5*/*enpp1* phosphate–pyrophosphate axis.
   **Serious objection, mine:** *entpd5* is reported **essential and systemic**; pushing
   mineralisation organism-wide risks skeletal pathology. Without the pectoral-restricted driver
   §3 says I could not find, this is not targetable, and a systemic mineralisation push on a small
   fish is a welfare problem (§6), not a tuning knob.
3. **Suppress joint formation to make a continuous spar** — e.g. via the Cx43/joint-placement axis
   running *alf*-ward. **My inference:** fewer joints ≈ more continuous beam. **Counter-argument,
   also mine:** *alf*'s joint failure is a *defect* phenotype; a ray that fails to joint is not
   thereby a competent spar, and the fin also has to survive normal swimming loads. Unjointed long
   rays may simply break.
4. **Increase ray cross-sectional depth** rather than length — exploiting `I ∝ d⁴` instead of
   fighting `δ ∝ L³`. **I found no allele that does this.** This is the edit the biomechanics
   actually wants and the one the genetics does not offer. Noting it as the clearest unmet target.

---

## 5. A candidate stack, and the honest probability discussion

### Individually-demonstrated edits

Stated as what each is *demonstrated* to do — not as a buildable plan:

| # | Edit | Demonstrated in zebrafish? | What exactly is demonstrated |
|---|---|---|---|
| 1 | *kcnh2a* ectopic fin expression (*lof*-like) | **Yes** | Prolonged outgrowth → longer fins, all fins, cell-autonomous to intra-ray mesenchyme |
| 2 | *kcnk5b* gain-of-function / overexpression | **Yes** | Sufficient for overgrowth; conductance-dependent; localised in mosaic clones; enlarges pectoral **buds** |
| 3 | Dominant-negative *kcc4a* (*schleier*-like) | **Yes** | Loss of growth restriction in fins and barbs; **dominant** |
| 4 | *rpz* gain-of-function (*rapunzel*-like) | **Yes** | Extra ray **segments** at unchanged segment length |
| 5 | *and1*/*and2* manipulation | **Loss only** | Double knockdown removes actinotrichia. **Gain-of-function stiffening: not demonstrated.** |

### What is NOT demonstrated about combining them

- **No combination of 1–4 has been shown to produce a flight-capable or glide-capable surface.** The
  closest published result is Daane et al. phenocopying flying-fish **fin proportions** — proportions,
  not flight, not lift, not glide performance.
- **Additivity is not demonstrated and is positively contraindicated.** *lof* × *lat4a* is reported
  **non-additive**; edits 1–3 converge on one K⁺/calcineurin pathway.
- **No pectoral restriction is demonstrated** (§3). All four length/proportion edits hit all fins —
  including the caudal fin, the thrust surface. Enlarging that is a swimming-performance liability.
- **Stiffness is not demonstrated at all** (§4), and edits 1, 2, 4 each make the `L³` compliance
  problem worse.
- **Pleiotropy is documented, not speculative:** *rpz* family in haematopoiesis with vascular/blood
  defects in *rapunzel* homozygotes; *schleier* carries a recessive pigment phenotype; a 2025–26
  report finds altered fin vasculature in *longfin*. These are growth-and-patterning genes, not
  fin-only genes.

### Probability of working — and the reason it is not a stacking problem

My assessment: **very low, and the dominant obstacles are not genetic.**

A glider needs, at minimum: (a) lift-bearing span-wise **stiffness**; (b) a **launch** mechanism
reaching takeoff speed; (c) a **rigid body** to transmit loads without buckling; (d) **control
authority** in pitch/roll; (e) aerodynamically useful **planform and camber**. The §1 catalogue
addresses **area and span only** — part of (e), and in the direction that *degrades* (a).

Scale is the deeper problem, and it is physics, not genetics. Lift scales roughly with wing area
(`∝ L²`) while mass scales with volume (`∝ L³`), so small gliders need *relatively* larger wings,
but they also fly at low **Reynolds number** where lift-to-drag ratio is poor. An adult zebrafish is
~3–4 cm and a fraction of a gram. Flying fish — which actually glide — are an order of magnitude
longer, and achieve it with a **whole-body** configuration: enlarged pectorals *plus* a stiffened
vertebral column, an **asymmetric caudal fin** used to scull at the surface for launch, and
specific launch kinematics. Daane et al.'s point is that fin *proportion* differences can be
reached by simple allelic combinations; the gliding *apparatus* is not thereby reconstructed.

**So the failure mode is categorical.** Even a stack working perfectly and additively — which the
epistasis argues against — yields a zebrafish with large, floppy, over-jointed fins on all four fin
positions, a compliant body, no launch stroke, and no control surfaces. That animal swims worse and
does not glide. Running the stack harder does not approach flight; it approaches a fish that cannot
swim. There is no allele in the catalogue whose axis is "stiffness," and stiffness is the binding
constraint.

**Probability a 3–5 edit germline stack of demonstrated zebrafish alleles yields measurable
aerial glide (L/D > 1 over a ballistic baseline): I would put it near zero**, and I want to be clear
that is a *structural* judgement from §2 and §4 — the available levers move the wrong variable —
not a bet about effect sizes I could not read. I would revise on evidence of (i) a true
pectoral-restricted adult driver, and (ii) any allele increasing ray **flexural stiffness** or
cross-sectional depth. Absent (ii), effect size on length is irrelevant.

**What the catalogue *is* good for.** As a fin-size and allometry system it is genuinely
first-rate — single-locus, dominant, viable, quantifiable, with a convergent mechanism. The right
question for these alleles is how organ proportion is set and terminated, which is what the papers
actually claim. Reframing "build a glider" as "test whether K⁺/calcineurin dose sets fin proportion
continuously" is a tractable experiment; the glider is not.

---

## 6. Welfare, regulatory, and containment notes

Not an afterthought — a precondition, and part of why §5 stops at assessment.

- The predicted phenotypes are **impaired-swimming** phenotypes: oversized compliant fins on a
  small fish, with documented vascular, haematopoietic, and mineralisation pleiotropy. Harm is the
  *expected* outcome, not a side risk. Any such work needs institutional animal-ethics (IACUC or
  equivalent) review, with humane endpoints defined in advance.
- Multi-edit germline modification of a vertebrate for a **novel locomotor capability** sits outside
  routine disease-model or developmental-genetics justification. The scientific question (§5, last
  paragraph) is answerable with far less invasive designs.
- Zebrafish are a tropical species with established invasive potential in some watersheds;
  containment and sterility are standard requirements for GM aquatic organisms.

---

## 7. Provenance summary

| Claim group | Best read-level achieved | ZFIN IDs |
|---|---|---|
| All allele/gene/mechanism rows (§1) | `search-summary` | **all `unknown`** — ZFIN 403-blocked |
| Axis assignments (§2) | `search-summary`, plus my inference where marked | — |
| Pectoral drivers (§3) | `search-summary`; **negative result from 2 searches, no ZFIN** | — |
| Stiffness targets (§4) | `search-summary`; collagen = `could-not-access` | — |
| Beam-theory scaling (§2, §5) | standard mechanics, applied by me — **not from a cited paper** | — |
| Stack assessment (§5) | **my analysis**, built on the above | — |

**Nothing in this file has been read at full-text or abstract level.** No citation, gene symbol,
allele name, or accession here was invented; where I lacked a value I wrote `unknown` and said what
I tried. The flip side of that discipline: this document's factual tier is low, and it should be
re-verified against ZFIN and the primary papers before any of it is relied on.

### Sources consulted (all via search summaries only)

- Stewart et al. 2021, *Development* — *longfin*/*kcnh2a*. ZFIN pub listing `ZDB-PUB-210602-7`
  (listing seen in search results; page itself unreachable).
- Perathoner et al. 2014, *PLoS Genetics* 10(1):e1004080 — *alf*/*kcnk5b*.
- Lanni et al. 2019, *Developmental Biology* — *schleier*/*slc12a7a*. Author list **not confirmed**.
- Green et al. 2009 — *rapunzel*/*rpz* gain-of-function. Goldsmith et al. 2003 (ZFIN listing
  `ZDB-PUB-030728-7`) — earlier *rapunzel* fin-growth work.
- Iovine et al. 2005 (ZFIN listing `ZDB-PUB-050119-9`); Hoptak-Solga et al. 2008 — *sof*/*cx43*.
- Daane et al. 2021, *Current Biology* 31(22), doi 10.1016/j.cub.2021.08.054 — flying fishes,
  *kcnh2a* × *lat4a*.
- 2024, *PLoS Biology* — pectoral fin **bud** scale, K⁺ → Ca²⁺ → CaMKK → *shha*, *kcnk5b*/*kcnk10a*.
- 2018, *Scientific Reports* 8 — bioelectric–calcineurin module, allometric fin growth.
- Zhang et al. 2010, *Nature* 466 — actinodins *and1*/*and2*, fin-to-limb transition.
- 2013, *PNAS* — *entpd5* and skeletal mineralisation. 2017, *PLoS ONE* — *pth4* ablation.
- 2016, *PNAS* — *Tbx5* regulatory evolution / CNS12; 2018, *Cell Reports* — Tbx5 forelimb enhancer
  knockouts. **These two conflict** on the mouse intron-2 element in zebrafish; unresolved.
- 2025, *eLife* 105889 — *hoxba*/*hoxbb* clusters and pectoral fin positioning.
- 2025 bioRxiv preprint — *rpz5* in haematopoiesis (preprint, not peer-reviewed).
