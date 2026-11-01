# Zebrafish to flying fish: what would it take?

Project: `projects/zebrafish-to-flying-fish` · branch `claude/zf2ff-20261101` · 2026-11-01 (PDT)
Owner: claude-zf2ff. Single operator, **not independently reviewed**.

**This document is a plan, not a result.** The only results this project has produced are in
[`RESULTS.md`](RESULTS.md): two protein-to-genome alignment runs against the one available
Exocoetidae assembly, and a source index built from 45 Europe PMC queries. Everything else below
is decomposition, hypothesis and proposed experiment.

**Nothing here is an observation in a flying fish.** No Exocoetid was handled, imaged, sequenced or
perturbed by this project. No zebrafish was either. Every biological statement is either (a) read
from a published abstract, (b) computed here from public sequence, or (c) labelled a hypothesis.

## 0. The read-level and evidence ladder used throughout

Every row in every table below carries one evidence level. The ladder is about **what was read or
run**, never about how plausible the idea feels.

| Level | Meaning | What it is NOT |
| --- | --- | --- |
| `S-full` | The paper's **full text** was read. True for exactly one source: PMID 34534441 (`FULLTEXT-FINDING.md`). | Still a single-operator read, and reading a paper is not reproducing it. |
| `S-abs` | A published abstract was read (Europe PMC `resultType=core` body saved verbatim, sha256 in [`SOURCES.md`](SOURCES.md)). Every `S-abs` row should be read as *"the abstract of this paper states X"*, never as *"X"*. | Not a full-text read. Whether the paper's data support its own abstract was not checked, and whether the paper is the **primary** source of the finding was not checked either (see the provenance caution below). |
| `S-meta` | Only metadata was retrieved (title/journal, no abstract in the response). | Not a content read at all. |
| `C-here` | Computed in this project, with a receipt in [`RESULTS.md`](RESULTS.md) (command, exit code, input sha256, tool version, seed). | A sequence alignment is not an annotation, an ortholog call, an expression measurement or a function. |
| `C-other` | Computed by another harness in this repo, with its own receipt (OpenFold2 structures, BioModels simulations). | A predicted structure or a published-model simulation is not a measurement of a fish. |
| `H` | Hypothesis. No read and no run supports it; it is written down so it can be attacked. | Not evidence of any kind. |
| `U` | Declared unknown. The thing that would have to be measured, and nobody here measured it. | Not a gap to be filled with a plausible number. |

**Full text was read for zero sources.** That is the single biggest limitation of this document and
it bounds every `S-abs` row: an abstract states a conclusion, and this project did not verify that
the paper's figures support it.

**Provenance caution (added after review).** Europe PMC relevance ranking surfaces recent papers.
Several phenotypes cited below are cited from a 2024–2026 paper that *reports* them, which is not
the same as the paper that *first established* them. The clearest case: the actinodin/actinotrichia
loss-of-function phenotype is cited here from PMIDs 41885168 and 42741580, and a targeted query for
the primary actinodin literature (`data/epmc3/actinodin_primary_2010.json`, 28 hits) did **not**
return the original knockdown report in its top results. So the reads below establish *that these
statements are in the recent literature*; they do not establish priority or the original evidence.
`U` for primary provenance throughout.

## 1. Trait decomposition by scale

The target phenotype is not "a flying fish". It is a *set* of separable traits that, in extant
Exocoetidae, co-occur. Decomposing it matters because the traits have very different read-levels:
fin *allometry* has a named genetic handle, while launch *behaviour* has essentially none.

Scale names are the `Scale` literal in `frontier/models.py` so these rows can be attached to
records without re-coining a vocabulary.

| # | Trait | Scale(s) | Zebrafish state | Exocoetid state | Read-level of the Exocoetid side | Measurable readout |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | Pectoral fin length / standard length (wing allometry) | `organ`, `developmental`, `evolutionary` | Small pectoral fins; fin proportion set during bud growth and adult outgrowth | Greatly enlarged pectoral fins enabling gliding | `S-abs`: 35-species phylogenomic study describes "convergent evolution of increased paired fin size and aerial gliding" (PMID 34534441). No measurement of any individual fish here. | fin length / SL, ray count, fin area; ratio distribution across stages |
| T2 | Pelvic fin enlargement ("four-winged" forms) | `organ`, `developmental` | Pelvic fins appear ~3 wpf at metamorphosis; small | Enlarged in four-winged genera (e.g. *Cheilopogon*); not in two-winged | `S-abs`: 80 species have "one or two pairs of expanded fins" (PMID 42325591). Which genus has which is not resolved from what was read. | pelvic length / SL; onset stage |
| T3 | Caudal fin asymmetry (hypocercal, enlarged lower lobe) | `organ`, `tissue` | Symmetric caudal fin patterned by a central and two peripheral organizers | Lower lobe longer; used for taxiing/thrust at the surface | Exocoetid side still `U`. The zebrafish/teleost side is now `S-abs` and has **two** handles: a transient `shha` pulse in a critical late-embryonic window re-patterns adult caudal shape (PMID 40853969), and CRISPR of duplicated `szlA`/`szlB` produces caudal bifurcation at 45–80% penetrance in goldfish (PMID 42653322). | upper/lower lobe length ratio |
| T4 | Fin ray geometry: segment length, branching, joint number | `tissue`, `organ` | `sof`/cx43 and bioelectric manipulations change segment length; hox13 loss shortens and thickens rays and deletes joints and bifurcations | Rays must support a membrane under aerodynamic load. **No ray-level description is given here**: nothing read by this project describes Exocoetid ray segmentation, branching or joint counts, and an earlier draft of this table contained a guess, which has been removed. | `U` for Exocoetidae (no ray-level morphometry read). Zebrafish side `S-abs` (PMIDs 41739864, 38527087, and the Dev 2024 bioelectric paper). | segment length, joints/ray, bifurcation index, ray count |
| T5 | Ray/membrane material properties (modulus, actinotrichia collagen architecture) | `macromolecular`, `tissue` | `and1`/`and2` encode actinotrichia collagen; double mutants lose actinotrichia and all fin-fold-derived skeleton | Must carry aerodynamic load without collapse | `U` for Exocoetidae. Zebrafish/teleost side `S-abs` (PMIDs 41885168, 42741580), plus the finding that **spiny-ray development is actinotrichia-independent** and involves BMP-positive osteoblast condensation (PMID 41690953). | bending stiffness EI, fibre orientation, collagen cross-section |
| T6 | Burst muscle power for launch | `cellular`, `organ`, `organism` | Normal teleost axial muscle | High-power burst swimming to exit water | Exocoetid side `U`. Zebrafish side now `S-abs`: `klhl41b` is required for sarcomere assembly and both radial and longitudinal growth, assayed with force generation (PMID 42870309), and myosin light chains promote sarcomere growth in fast-twitch muscle (PMID 42243126, title level). | fibre type fractions, power density, tail-beat frequency |
| T7 | Scales, keel, body armour and skin | `tissue`, `organ` | `eda-/-` zebrafish lose scales, fin rays, pharyngeal teeth and gill rakers | Streamlined body; scale cover | `U` for Exocoetidae specifics. Zebrafish/teleost side `S-abs` (PMID 41344457). | scale count/size, skin thickness |
| T8 | Glide and launch behaviour, sensing and control | `neural`, `organism`, `collective` | No aerial behaviour | Launch, glide, taxi, wind use | `S-abs` for ecology only (foraging in wind, PMID 40758188). Mechanism `U`. | launch angle/speed, glide duration, control surface use |
| T9 | Karyotype / genome background | `evolutionary` | `U` — not read here | 2n = 48 in three species examined; karyotypic divergence between genera | `S-abs` (PMID 42325591) | karyotype, synteny |
| T10 | Ecology: epipelagic life history | `ecological` | Freshwater, benthopelagic | Epipelagic, interoceanic | `S-abs` (PMID 42325591) | out of scope for this project |
| T11 | **Pectoral girdle and fin musculature** (the wing's root, not its blade) | `organ`, `tissue`, `developmental` | Cleithrum + scapulocoracoid sized for labriform swimming; the cleithrum forms from four adjoining embryonic populations; a gli3/Hedgehog ossification trade-off can reconfigure the girdle toward stem-tetrapod character | Must transmit aerodynamic load from a large wing into the body wall | `U` for Exocoetidae. Zebrafish side `S-abs` (PMIDs 39060278, 40442084), and for the **muscle** half specifically: `met` mutants lose migrating muscle progenitors to the paired appendages, with reduced fibre number in the **pectoral abductor** and disturbed pectoral fin function (PMID 31287821). | girdle element dimensions, glenoid articulation, abductor/adductor muscle mass |
| T12 | **Whole-animal locomotor cost of enlarged fins** | `organism` | A published comparison of wildtype vs **longfin** strains tested tail-flip jump kinematics, voluntary jumping and exhaustion. Its **result was not read**, so the direction and size of any cost are `U` here. | Exocoetids presumably pay a drag cost in water for the wing | `S-abs` for the zebrafish comparison (PMID 38232499); the Exocoetid side is `H` | jump distance, exhaustion, swimming cost |

**What this decomposition buys:** T1/T2/T4 are the only traits with a *named genetic handle* that is
both (i) published in zebrafish and (ii) flagged by a comparative study in flying fishes. T3, T5, T6,
T8 are, at this read-level, **unknowns with no candidate gene** — and writing them as unknowns is the
honest output, not a weakness to be patched with guesses.

## 2. Candidate genes and regulatory regions, as hypotheses with evidence levels

### 2.1 The one locus pair with both a flying-fish signature and a zebrafish mutant

| Locus | What the source says | Evidence | Status for this project |
| --- | --- | --- | --- |
| `kcnh2a` (Kv11.1, *ether-a-go-go*-related K+ channel) | The classic mutant `longfin^t2` is a **cis-regulatory** allele that overexpresses `kcnh2a`; disrupting `kcnh2a` in cis rescues it; overgrowth comes from a **prolonged outgrowth period**, acting tissue-autonomously in the intra-ray mesenchymal lineage, and Kcnh2a appears to inhibit calcineurin output. | `S-abs` PMID 34061172 | Primary candidate for T1/T4. The engineering-relevant part of the abstract is that the allele is *regulatory*: as the abstract describes it, the phenotype followed from changing *where/when* the channel is expressed rather than the protein. That is an abstract's description, not a verified fact. |
| `lat4a` in Exocoetidae | **FULL TEXT READ** (`FULLTEXT-FINDING.md`). The comparative signal is in **`lat4a`**: elevated relative evolutionary rate in gliding beloniforms, phyloP acceleration **p = 0.008** on the flying-fish ancestral node, and a convergent **F326L** substitution present in both flying-halfbeak lineages and all sequenced Exocoetidae **except** *Parexocoetus brachypterus*. `lat4a` is SLC43A2 (the paper's own citation). | `S-full` PMID 34534441 | The strongest published bridge from zebrafish genetics to flying-fish morphology, and **this project reproduced the F326L state independently** in *H. speculiger* (`RESULTS.md` §R7l). |
| `kcnh2a` in the same paper — **zebrafish-side only** | The `kcnh2a` evidence is **not** comparative. `longfin^dt2` (`lof`) is a **chromosome-2 inversion** with breakpoints upstream of the `prrx1a` TSS and between `kcc4a` and `kcnh2a`, coding regions untouched; revertant alleles map to `kcnh2a` loss of function. | `S-full` PMID 34534441 | An earlier version of this plan treated the paper as reporting an Exocoetid `kcnh2a` signal. **It does not.** That error is corrected here and in `FULLTEXT-FINDING.md`. |
| `lat4a` convergence | A convergent amino-acid change in `lat4a` is shared by syngnathids and **some flying fishes**, with in vitro analysis reported as confirming a role in fin size evolution in both lineages. | `S-abs` PMID 40689752 | Independent second source naming the same gene. Note: "some flying fishes" — not all, so this is not a universal Exocoetid feature. |

**Unresolved identifier problem (declared, not patched).** The two papers name `lat4a`. UniProt's
zebrafish entries are `slc43a2a` (accession Q7ZUS0, 153 aa — a fragment) and `slc43a2b`
(Q5PR35, 592 aa — full-length "L-type amino acid transporter 4"). Which of these the papers' `lat4a`
denotes was **not resolved** at this read-level. Round 2 of the mapping run therefore carried both,
labelled. This is recorded as a Problem, not silently decided. `U`.

### 2.2 Bioelectric / size-scaling module (T1, T4)

| Locus | Source statement | Evidence |
| --- | --- | --- |
| `kcnk5b` (K+-leak channel) | Retinoic acid lowers intracellular K+ in the pectoral fin bud and up-regulates `rcan2`; `rcan2` overexpression increases bud growth and decreases K+; CRISPR targeting of `rcan2` does the reverse; Rcan2-mediated growth **depends on Kcnk5b**; Kcnk5b-induced `shha` transcription and bud growth require IP3R-mediated Ca2+ release and CaMKK. | `S-abs` PMID 38527087 |
| `kcnk5b^W169L`, `cx43^T154A`, cell-type-specific | Hyperactive `kcnk5b` or dominant-negative Cx43 under cell-type-specific promoters: manipulation in **keratinocytes** mainly changed fin **size**, in **osteoblasts** mainly changed fin-ray **segment length**; combinations gave large fins with short segments and vice versa; optogenetic manipulation showed membrane potential itself suffices. | `S-abs` (Development 2024, no PMID in the retrieved record) |
| `cacna1g` (T-type Ca2+ channel) | `cacna1g` homozygous mutants regenerate **extraordinarily long fins** through prolonged outgrowth; L-/N-type channels act during regenerative outgrowth to restore original scale. | `S-abs` PMID 41321290 |
| `gja1`/`cx43` (`short fin`, `sof`) | The UniProt entry for zebrafish Gja1 carries the `shf`/`sof` symbols ("Short fin protein"). | `S-abs` (UniProt O57474 annotation only — a database annotation, weaker than a read paper) |
| `fgf20a` + Erk gradient | Osteoblast Erk activity scales with the amount of amputated tissue and predicts regenerated skeletal size; gradients are millimetre-long, FGF-receptor dependent; epidermal `fgf20a` expression scales with amputation extent. | `S-abs` PMID 42719339 |

**Why this module matters for the design — and the limits of that reading.** Three abstracts place
membrane potential in a specific cell lineage upstream of fin size. They are **not** three
measurements of one thing, and an earlier draft of this section wrongly merged them:

- PMID 34061172 and PMID 41321290 are about outgrowth **duration**, and both are *adult regeneration*.
- PMID 38527087 is about the *embryonic* pectoral fin **bud**, and its abstract describes coordinated
  K+ decrease and bud **proportion**, not a duration.

So "duration sets final size" is supported (abstract-level) for regenerating adult fins, and
**not** for the embryonic bud. Since a wing has to be built developmentally, the regeneration
evidence is the weaker half of this module for this project's purpose, despite being the larger half.
`H`, stated so it can be attacked: if the Exocoetid wing is built by the same mechanism, the edit to
make extends outgrowth in the pectoral ray mesenchyme and nowhere else. Nothing read or run here
tests that in an Exocoetid. `U`.

### 2.3 Patterning module: where a fin forms, how many elements, what shape (T2, T3, T4)

| Locus | Source statement | Evidence |
| --- | --- | --- |
| `hoxba`;`hoxbb` clusters | Double cluster deletion mutants **completely lack pectoral fins**, with loss of early `tbx5a` induction in the lateral plate mesoderm and loss of retinoic-acid competence; `hoxb4a`, `hoxb5a`, `hoxb5b` named as pivotal. | `S-abs` PMID 41268905 |
| `hoxaa`;`hoxab`;`hoxda` clusters | Triple cluster deletion shortens the endoskeletal disc and fin fold; the defect is in **post-bud growth**; adults show posterior pectoral defects. | `S-abs` PMID 39384796 |
| `hoxa13a`/`hoxa13b`/`hoxd13a` | Triple mutant rays are shorter and thicker, lose joints, bifurcations and actinotrichia, and resemble acanthomorph **spiny** rays; `alx4a` domain expands, `grem1b` falls; `hoxa13a/b` matter more than `hoxd13a`. | `S-abs` PMID 41739864 |
| `hhip` | `hhip` mutants gain radial bones in a localized region; notable early `hhip` expression is a zebrafish characteristic absent in basal species; Hox13 region-specific expression indicates the median region is expanded in `hhip-/-`. | `S-abs` PMID 39417578 |
| `shha` (and `shhb`/`twhh`) | `shha` transcription is downstream of Kcnk5b in bud scaling (PMID 38527087); caudal fin shape imprinted in late embryogenesis is re-patterned by Shh signalling (PMID 40853969, title-level). | `S-abs` / `S-meta` |
| `tbx5a` | Required downstream of HoxB for pectoral fin field specification (via PMID 41268905). A `tbx5a` *enhancer* specific to pectoral fin was **not** identified at this read-level — the enhancer query returned unrelated papers. | `S-abs` for the gene, `U` for the enhancer |
| `pitx1` + pelvic enhancer | `pitx1` transcripts appear briefly in posterior lateral plate mesoderm early; the **pelvic-fin-specific `pitx1` enhancer is in a poised state at the larval stage and activated at the juvenile stage** — a named, stage-gated regulatory element. | `S-abs` PMID 37691823 |
| `and1`/`and2` (actinodins) | Double mutants lack actinotrichia; reduced fin fold, disorganized migration, all fin-fold-derived skeleton disrupted in adults; collagen reorientation turns the fin bud into a **limb-bud-like** configuration. | `S-abs` PMIDs 41885168, 42741580 |
| `eda`/`edar` | `eda-/-` zebrafish lack scales, fin rays, pharyngeal teeth and gill rakers; intermuscular bones shortened; Eda/Edar/NF-κB disrupted. | `S-abs` PMID 41344457 |

### 2.4 Girdle and musculature module (T11) — added after review

An earlier draft decomposed the "wing" into dermal fin rays only. That is a design error: a long
stiff blade attached to a girdle sized for labriform swimming folds at the body wall. Two reads give
the only handles this project has on the root of the wing.

| Locus / finding | Source statement | Evidence |
| --- | --- | --- |
| `gli3` + Hedgehog compound knockouts | Zebrafish pectoral girdle mesodermal cells expressing `gli3` differentiate into **both** intramembranous and endochondral bone; Gli/Hedgehog compound knockouts showed a combination of actinopterygian and **stem-tetrapod** girdle characteristics; the abstract frames this as a tunable trade-off between the two ossification pathways. | `S-abs` PMID 40442084 |
| Cleithrum embryonic origin | Cleithrum development combines **four adjoining embryonic populations** (photoconversion + genetic lineage tracing). | `S-abs` PMID 39060278 |
| Pectoral girdle plasticity in another teleost | Domesticated paddy-field carp show girdle morphological shifts with Wnt-associated expression modules. | `S-abs` PMID 42685484 — a different species, correlative transcriptomics, weak. |

`H`: the girdle is the *more* likely binding constraint than the blade, because it has to carry a
load that no fish fin carries. Nothing read here measures a load anywhere. `U`.

### 2.4b Candidate genes for the traits that had none (added after a targeted query round)

Earlier versions of this plan recorded T3, T5, T6 and T11 as having **no candidate gene at all**.
A focused Europe PMC round (`data/epmc4/`, 6 queries) found handles for all four. They are
abstract-level reads in zebrafish or another teleost, not Exocoetid observations.

| Trait | Locus / mechanism | What the abstract states | Evidence |
| --- | --- | --- | --- |
| T3 caudal asymmetry | `shha` **timing** | A transient `shha` overexpression pulse during late embryogenesis causes excess growth of the **central** rays, turning the adult forked fin triangular/truncate. After that critical window the same overexpression does nothing. | `S-abs` PMID 40853969 |
| T3 caudal asymmetry | `szlA`/`szlB` (sizzled) | CRISPR disruption of both duplicated goldfish paralogs gives twin-tail-like caudal bifurcation in 45–80% of larvae across three biological replicates, with separation of distal rays and partial splitting of the caudal skeletal complex, and reduced `chdA`/`eve1`. | `S-abs` PMID 42653322 |
| T5 ray material | spiny-ray programme | In rainbowfish and filefish, **spiny-ray development is independent of actinotrichia**, and lateral protrusions associate with BMP-positive osteoblast condensation. | `S-abs` PMID 41690953 |
| T6 burst muscle | `klhl41b` | Required for sarcomere formation and organisation, supporting **both radial and longitudinal** muscle growth; characterised with force-generation assays in zebrafish. | `S-abs` PMID 42870309 |
| T6 burst muscle | myosin light chains | Cooperatively promote sarcomere growth in fast-twitch muscle. | `S-meta` PMID 42243126 (title) |
| T11 fin musculature | `met` (HGF receptor) | `met` mutants have severely affected migrating-muscle-progenitor-derived musculature of the paired appendages, reduced fibre number **particularly in the pectoral abductor**, and disturbed pectoral fin function. | `S-abs` PMID 31287821 |

**This changes one of the plan's own conflicts.** §4.1 #1 said the edit that stiffens rays
(`hox13` loss) necessarily shrinks the fin fold and deletes actinotrichia, because the spiny-like
character and the fold come through the same genes. PMID 41690953 states that spiny rays develop
**without** actinotrichia at all, via osteoblast condensation and BMP. So a route to stiff rays that
does not run through actinotrichia loss may exist. That conflict is **downgraded from a hard
trade-off to an open question**, and the downgrade rests on one abstract in two non-model species.

### 2.5 Regulatory regions: what is actually named in the literature read here

This is deliberately short, because it is where the plan is weakest.

| Element | What is known | Evidence | Coordinates |
| --- | --- | --- | --- |
| The `longfin^t2` lesion upstream of `kcnh2a` | A cis-regulatory allele causing ectopic `kcnh2a` expression in intra-ray mesenchyme. | `S-abs` PMID 34061172 | **`U` — no coordinates read.** The abstract names chromosome 2 and the gene; it does not give the lesion's boundaries, and this project did not read the paper or its supplements. |
| Pelvic-fin-specific `pitx1` enhancer (zebrafish) | Exists, is poised at larval stage, activates at juvenile stage. | `S-abs` PMID 37691823 | `U` |
| Stickleback *Pel* enhancer of `Pitx1` | Named in the query; the retrieved records were about repeated pelvic-spine loss in brook stickleback (PMID 39906589), not the *Pel* element itself. | `S-meta` | `U` |
| Regeneration-responsive enhancers | "Changes in regeneration-responsive enhancers shape regenerative capacities in vertebrates" (PMID 32883834) and "Modulation of tissue repair by regeneration enhancer elements" (PMID 27049946). | `S-meta` (titles) | `U`; the repo's existing `artifacts/genetic-blueprints/blueprints.json` already carries a `LEN-P2:EGFP` design with **null coordinates** and says so. |
| Exocoetid regulatory divergence | PMID 34534441 reports signatures "in both coding and regulatory regions" genome-wide. | `S-abs` | `U` — which regions, in which species, at what coordinates: not read. |

#### Candidate regulatory windows that now have coordinates (added after the Evo 2 handoff)

An earlier version of this section said this project could not name a single coordinate interval.
That is no longer true, and the upgrade came from another harness, not from here. The Evo 2 harness
handed over **19 two-kilobase candidate windows with coordinates, strands and per-window sha256**
(`messages/evo-to-zf2ff.md`; 10 zebrafish on GRCz11, 9 flying fish on `GCA_018398805.1`), for
`tbx5a`, `fgf10a`, `fgf20a`, `shha`, `kcnk5b`, `hoxd13a`, `msx1b`, `runx2b`, `sp7` and `lef1`.

What they are and are not, stated at the same level of care their author used:

| | |
| --- | --- |
| What they are | Windows **anchored** on a gene: TSS-anchored for zebrafish, upstream of a *predicted* start codon for flying fish, where no TSS or UTR annotation exists. |
| Evidence that they carry structure | `C-other`: all 19 beat their own dinucleotide scramble on Evo 2 likelihood, aggregate +0.1444, CI [0.0980, 0.1908], n = 19. Flying fish alone +0.0993, CI [0.0453, 0.1533]. |
| Evidence added here | `C-here`: three motif-scan passes (`RESULTS.md` §R6–R6c). Under the honest held-out design, real windows exceed composition-matched shuffles of themselves in **both** species (zebrafish +27.1 [7.9, 46.3]; flying fish +26.8 [12.0, 41.6]). **Aggregate only** — only 2/10 and 4/9 windows reach z > 2, so these windows cannot be ranked against each other. |
| Independently placed? | `C-here`: 2 of 9 flying-fish windows (`shha`, `tbx5a`) are confirmed **flush to the base** by this project's independent protein mapping. 2 (`kcnk5b`, `fgf10a`) are at loci this project assigns to a **different paralog**, and 1 (`fgf20a`) disagrees on scaffold (`CROSSCHECK-EVO.md`). |
| What they are **not** | Not enhancers. Not validated elements. Not functional. Their author states plainly that the per-window ranking is exploratory and that the cross-species comparison is void; this plan does not use either. |

So a construct design can now cite a **coordinate interval and a digest** for ten genes, which is a
real advance over a `null`. It still cannot cite a **validated element**, because nobody has shown
any of these windows drives anything. The `null` in §5's cargo row moves from "no coordinates" to
"coordinates with no functional evidence" — a different and better-defined gap.

**Honest summary of §2.** This project can name genes with real evidence, and can now name candidate
regulatory *intervals* with digests, two of them independently placed by two methods. It still cannot
name a single enhancer that is **known to do anything**. Any construct design below that needs a
functional element therefore still has a `null` where the validated sequence goes — exactly as
SPEC-012 requires.

### 2.6 Inputs reused from this repository (other harnesses' artifacts, not re-verified here)

This project did not re-run or re-verify any of these; it uses them as the repo's existing sourced
layers so the plan's stages, cell compartments and construct layers are not re-coined here.

| Artifact | What it supplies to this plan | Boundary it carries |
| --- | --- | --- |
| `data/fish-lifecycle/stages.json` + `docs/fish-lifecycle.md` | The stage vocabulary every perturbation readout below should be reported against: **embryo** (to ~72 hpf at 28.5 °C, protruding-mouth stage), **larva**, **juvenile** (entry at complete squamation and loss of the larval fin fold, SSL 11.0 mm), **adult** (viable gametes; 17.5 mm SL males, 18.3 mm females). Also the one fitted quantity in the pectoral fin bud this repo has: a BMP gradient length scale of **about 28 µm at 60 hpf**, fitted 48–78 hpf (Mateus 2020), and the size index **SL = 3.56·HAA + 4.40** (Parichy 2009). | Zebrafish only, single-operator, unreviewed. Stage boundaries are laboratory conventions. The gradient is a fit to zebrafish data, not a transferable law, and this project did not use it quantitatively anywhere. |
| `artifacts/fish-regulatory-map/map.json` + `docs/research/fish-regulatory-map-2026-10-31.md` | Measured cell compartments with marker lists for the fin: basal and superficial epithelium, **mesenchymal fibroblast states** (`prrx1b`/`msx1b`), **osteoblast/joint states** (`sp7`/`bglap`; `lmx1ba`/`pthlha`/`evx1`), haematopoietic, and the **embryonic pectoral fin field** (`tbx5a`–`fgf24`, `hand2`-labelled lateral plate mesoderm). These are the populations rows P1, P4 and P5 need to name as targets and comparisons. | Markers are **identification aids, not validated drivers**. The underlying multiome (GSE261907, GRCz11/Ensembl104) measures **adult caudal regeneration**, two biological replicates per time point — not embryonic paired-fin development, which is what a wing needs. |
| `artifacts/genetic-blueprints/blueprints.json` (SPEC-012) | The construct-layer vocabulary and four existing designs spanning reporter-first characterization, BAC-carried locus and landing-site options. | Its element coordinates and sequences are **null** and it says so. This plan inherits those nulls; §2.5 does not improve on them. |
| The same regulatory-map review's Evo 2 assessment | Why `G7` below is not treated as available even if a model call were possible: the published accessibility evidence is in mouse and human cells, and that review states calibration in fish is unknown. | A predictor score is not a measurement. |

**Consequence for the readouts in §4.** Every row's readout should be reported at a named stage from
that stage list, with the target and comparison populations named from the regulatory map's
compartments. Neither is done in the table below, because no row has been executed — but a row that
reports "fin length" without a stage and a comparison population would not be usable evidence under
SPEC-012, and that is a known gap in this plan, not an oversight to be discovered later.

## 3. Comparative genomics that can actually be run

Constraints, measured or read, that bound what is runnable at all:

- **One** Exocoetidae assembly exists in NCBI Datasets: *Hirundichthys speculiger* `GCA_018398805.1`
  ("Draft Genome of the Mirrorwing Flyingfish", PMID 34306036, `S-meta`). **Scaffold level, no
  annotation.** `C-here`: 1,008 MB of FASTA, sha256 in `data/round2/mapping_summary_round2.json`.
- **Ensembl has no Exocoetidae.** Medaka (*Oryzias latipes*) is the nearest Beloniformes proxy in
  Ensembl and must be labelled as a proxy everywhere it is used. (`S-abs`, bioservices harvest.)
- No Exocoetid RNA-seq, ATAC-seq or Hi-C was found by the queries run. All regulatory inference in
  Exocoetidae is therefore sequence-only. `U`.

| # | Analysis | Runnable today? | Inputs that exist | What it would and would not show |
| --- | --- | --- | --- | --- |
| G1 | **Protein-to-genome mapping of candidate loci onto `GCA_018398805.1`** | **Done.** `C-here`, three rounds, 27 distinct candidate proteins + 4 controls. See `RESULTS.md`. | zebrafish UniProt proteins; the assembly | Shows the locus is detectable and how diverged the best-aligning region is. Does **not** establish orthology, copy number or expression. Secondary-hit counts are per-chunk artefacts and must not be read as copy number. |
| G1b | **Span audit of every best hit** (assembly-gap fraction, largest intron, frameshifts) | **Done.** `C-here`, `SPAN-AUDIT.md`. Added after review, because two hits span ~0.3 Mb. | G1 alignments + the assembly | Separates "large-intron gene" from "possible chaining artefact". Does not decide which; it reports the numbers that let a reader discount a row. |
| G1c | **Paralog controls** (`kcnh2b`, `tbx5b`, `fgf10b`, `kcnk5a` mapped alongside their `a` paralogs) | **Done.** `C-here`, round 3. Added after review: with the teleost whole-genome duplication, an `a`-paralog query could best-hit the `b` region. | UniProt; the assembly | Shows whether the `a` and `b` queries resolve to different scaffolds. Still not an orthology test. |
| G2 | **Reciprocal best-hit test within each gene family** (miniprot `--trans` prediction from the collision scaffold, aligned back against every zebrafish family member) | **Done.** `C-here`, `RESULTS.md` §R3. Run instead of the medaka-proxy version because the collisions are between zebrafish paralogs, which medaka cannot arbitrate. | the assembly; 15 zebrafish family proteins | **Resolved** the `shha`/`shhb` collision (5/5 predictions rank `shha` first) and **did not resolve** the `kcnh2a`/`kcnh2b` one: score and percent-identity rankings disagree on the same sequence. Also showed `kcnh2a`'s second-best scaffold is a `kcnh6a`-like locus. Not an orthology proof; a gene tree is still owed. |
| G2b | **Gene tree for the `kcnh2` region with outgroups and a positive control** | **Done.** `C-here`, Nebius CPU job `claude-zf2ff-kcnh-tree-1`, `RESULTS.md` §R4 and `data/tree/MANIFEST.md`. | 20 proteins: the family, 2 human outgroups, 4 predictions from the collision scaffold, 4 from a control scaffold | **Settled the paralog assignment**: the region is `kcnh2b`-like (99/100), control passes (94.4/97). Still not orthology without synteny. |
| G10 | **Beloniformes + non-Beloniform outgroup trees** | **Done.** `C-here`, jobs `…beloniform-tree-1` and `…outgroup-tree-1`, `RESULTS.md` §R7e/§R7f. | medaka and Takifugu KCNH proteins; the census loci | **`kcnh2a` is absent from the Beloniform lineage**: Takifugu `kcnh2a` pairs with zebrafish `kcnh2a` at 100/100 while medaka and the flying fish carry the `b` copy. Two Beloniformes only; no synteny. |
| G3b | **Synteny around zebrafish `kcnh2a`'s neighbourhood** | **Running** (`scripts/synteny_kcnh2a.py`): the 36 protein-coding genes flanking `kcnh2a` on GRCz11 chr2, mapped onto the assembly. | Ensembl GRCz11; the assembly | Distinguishes "the whole neighbourhood is missing" from "the neighbourhood is present with a gap where `kcnh2a` should be". Scaffold fragmentation limits it; a negative is uninformative. |
| G9b | **Family-wide KCNH census** | **Done.** `C-here`, job `claude-zf2ff-kcnh-census-tree-1`, `RESULTS.md` §R7b. | all 10 zebrafish KCNH proteins; the assembly | **9 of 10 paralogs have a flying-fish locus; `kcnh2a` has none.** The gap is gene-specific in this assembly, not general incompleteness. Not a statement about the species. |
| G8b | **Motif-scan robustness: two re-designs** | **Done.** `C-here`, jobs `…motif-robust-1` and `…motif-heldout-1`, `RESULTS.md` §R6b/§R6c. | the same windows and motif set, held constant by digest | Pass 1's species asymmetry **withdrawn**; the aggregate signal survives in both species; **no per-window claim survives**. |
| G3 | Scaffold co-occurrence / micro-synteny of the candidate loci | Yes, partially: scaffold identity per hit is already in the round-1/round-2 summaries. Weak because the assembly is scaffold-level. | G1 output | Would show whether neighbouring zebrafish genes land on the same Exocoetid scaffold. Fragmentation will cause false negatives; a negative is uninformative. |
| G4 | Coding-change screen at `lat4a`/`kcnh2a` (does the Exocoetid allele carry the convergent residue?) | Yes in principle: extract the aligned region from the assembly and inspect the codon. Not run; blocked on the identifier problem in §2.1 and on not having read which residue PMID 40689752 means. | G1 alignments | Would be a direct, cheap test of a published claim in a *different* Exocoetid species than the paper used. Species mismatch must be stated. |
| G5 | Conserved-non-coding-element scan around candidate loci (zebrafish/medaka/*H. speculiger*) | Yes technically (whole-genome alignment of the three), heavy; not run. | assemblies | Would produce candidate elements. Conservation is not activity: a conserved element is a hypothesis, not a driver (SPEC-012). |
| G6 | Phylogenomic convergence scan across Exocoetidae | **No.** Needs the 35-species variation data behind PMID 34534441; only one assembly is public here. | — | `U` |
| G7 | Evo 2 scoring of candidate regulatory sequences | **Delivered by the Evo 2 harness**, not run here: 19 windows with coordinates and per-window likelihood deltas arrived during this session. Its two action items for this project are both **done** (`RESULTS.md` §R5). | their `fin-scale-regulatory-2kb/v1` input set | Gives candidate intervals with digests. Beating a dinucleotide shuffle shows structure above k = 2 and nothing about *cis*-regulatory syntax, which is their own stated boundary. |
| G8 | **Motif scan of those windows against their shuffles** | **Done.** `C-here`, Nebius job `claude-zf2ff-motif-scan-2`, `RESULTS.md` §R6. This was the job the handoff said neither harness had run. A robustness re-run is in flight. | their 19 windows + 76 control sequences; JASPAR 2024 CORE vertebrates (879 motifs) | Aggregate above-composition motif signal. The zebrafish arm alone is null and the species asymmetry is **unresolved**, pending the robustness run. A motif match is not a bound factor. |
| G9 | **Low-stringency whole-assembly hunt for `kcnh2a`** | **Done.** `C-here`, `scripts/hunt_kcnh2a.sh`, exit 0. Found **no new region**: the same 7 `kcnh2a`-aligning regions. 5 are untested and are now in a second gene tree. | the assembly; the `kcnh2a` query alone | Can locate a candidate; cannot prove the gene is absent from a fragmented assembly. |

## 4. Perturbation table

One row per proposed edit. Columns are exactly the ones the brief asks for. **No row has been
executed.** "In-silico model" names the specific artifact that would be run, including other
harnesses' outputs; where no model exists the cell says so.

| # | Edit | Scale | Readout | In-silico model | Wet-lab test | Evidence for the premise | Expected failure mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Re-create a `longfin`-like cis state at `kcnh2a`: targeted insertion of a mesenchyme-active regulatory cassette at the endogenous locus | `developmental`, `organ` | pectoral + caudal fin length / SL across stages; outgrowth **duration** (not rate) | SPEC-012 expression ODE (`dm/dt = k_tx(...) - γ_m m`) with **unknown `k_tx`** — it cannot predict the fin length and must not be used as if it could; fin-ray mechanics surrogate in `artifacts/claim-reuse` (clamped-free ray EI) for the resulting geometry | Tol2 reporter first, then knock-in F0 mosaic → F1 germline; fin morphometry at 30/60/90 dpf | `S-abs` PMID 34061172 (cis allele, prolonged outgrowth), PMID 34534441 (locus has an Exocoetid signature) | Ectopic expression in heart (Kv11.1 is cardiac) → arrhythmia/lethality. This is the predictable blocker and the reason for a cell-type-restricted driver. |
| P2 | **`lat4a` F326L knock-in (single codon), now fully specified** — zebrafish `slc43a2a` F326 → L, the state this project found in *H. speculiger* `slc43locus02` | `molecular`, `organ` | fin proportion; amino-acid transport in vitro | None usable. OpenFold2 from the bioservices run gave pLDDT 41–56 for four fin-relevant proteins (`C-other`) — too low to predict a transporter residue effect. A membrane transporter would need a different pipeline. | Prime editing / HDR single-codon edit; fin morphometry; transport assay in vitro | `S-full` PMID 34534441 names the residue and the lineage distribution; `S-abs` PMID 40689752 reports an in vitro role; `C-here` confirms the `L` state in a second Exocoetid | **No longer blocked by the identifier problem** — the target is zebrafish `slc43a2a` position 326. What remains unknown is whether the substitution does anything: this project checked a residue, not a transport activity or a phenotype. |
| P3 | `kcnh2a` × `lat4a` double perturbation (the published phenocopy) | `organ`, `developmental` | fin proportion vs the flying-fish ratio | None. The interaction is an epistasis result; no quantitative model of it was read. | Cross the two F1 lines; morphometry | `S-abs` PMID 34534441 states the interaction "closely phenocopies" flying-fish fin proportions | If the phenocopy is proportional but not mechanically sufficient, T1 is achieved and T5 (material) still fails. |
| P4 | Keratinocyte-restricted `kcnk5b^W169L` | `cellular`, `organ` | fin **size** with segment length held near wild type | Bioelectric tissue model in `artifacts/`/`bioelectric` (BETSE-family, `C-other`, published-model simulation only) | Existing published constructs; cell-type promoter; morphometry | `S-abs` Development 2024 cell-type-specific paper | Promoter leak into osteoblasts collapses the size/segment separation that is the whole point. |
| P5 | Osteoblast-restricted `cx43^T154A` (dominant negative) | `cellular`, `tissue` | ray **segment length**, joint count | same as P4 | same as P4 | `S-abs` Development 2024 | Joint loss → ray mechanical failure under aerodynamic load (couples to T5). |
| P6 | `cacna1g` loss of function | `subcellular`, `organ` | regenerative outgrowth length; Ca2+ transients (GCaMP) | None quantitative | Existing mutant line; fin amputation + regrowth | `S-abs` PMID 41321290 | Regeneration-specific; may not transfer to **developmental** fin size, which is what a wing needs. |
| P7 | `hoxa13a`/`hoxa13b` partial loss (ray character shift) | `tissue`, `developmental` | joints/ray, bifurcations, ray thickness, actinotrichia presence | Ray-mechanics surrogate (`artifacts/claim-reuse` EI claim, `C-other`) to ask whether spiny-like rays are *stiffer* in the way a wing needs | Existing mutant alleles; micro-CT | `S-abs` PMID 41739864 | Loses actinotrichia → the fin fold shrinks. Opposes T1. Recorded as a **conflict**, see §4.1. |
| P8 | `and1`/`and2` dosage increase (opposite direction to the published knockout) | `macromolecular`, `tissue` | collagen fibre orientation, fin fold size, ray architecture | None. No model couples collagen orientation to ray modulus here. | Overexpression / extra copy; high-sensitivity 3D collagen imaging as in PMID 42741580 | `S-abs` PMIDs 41885168, 42741580 establish loss-of-function only. **Gain-of-function direction is `H`.** | Over-deposition may stiffen without lengthening, or be dominant-lethal. Untested. |
| P9 | `pitx1` pelvic-enhancer timing change (de-repress earlier) | `developmental`, `organ` | pelvic bud onset stage; adult pelvic size (T2) | None | Enhancer reporter first (poised→active transition is the measurable), then enhancer edit | `S-abs` PMID 37691823 | The enhancer's coordinates are `U`; cannot design the edit yet. |
| P10 | `eda` dosage / `edar` modulation for scale and keel traits | `tissue` | scale count/size, intermuscular bone, **and** fin rays | None | Existing `eda-/-` plus dosage series | `S-abs` PMID 41344457 | `eda-/-` **also removes fin rays** — pleiotropy that directly destroys T4. Recorded as a conflict. |
| P11 | Caudal asymmetry (T3) | `organ` | upper/lower lobe ratio | None | — | **Superseded by P16 and P17**, which found two handles — both producing the wrong phenotype. The hole is now "no handle with the right sign", which is narrower than "no handle". | `U` for the direction needed. |
| P12 | Glide control and launch behaviour (T8) | `neural`, `organism` | launch angle/speed, glide duration | CFD/aeroelastic harnesses in this repo could consume a geometry, but nothing maps a genotype to behaviour | — | **Still no candidate gene.** T6's muscle half is now P18; T8 remains empty. The escape-circuit query returned Mauthner-cell regeneration and circadian papers, nothing about launch power or aerial control. | `U`. The one trait of the twelve with no handle at all. |
| P16 | **`shha` timing pulse to re-pattern caudal lobe proportion (T3)** | `developmental`, `organ` | upper/lower lobe length ratio; central vs peripheral ray length | None. No model here links a signalling pulse to lobe geometry. | Heat-shock or inducible `shha` overexpression inside the published critical window, then adult morphometry | `S-abs` PMID 40853969: a transient late-embryonic `shha` pulse lengthens central rays and turns the forked fin truncate; after the window it does nothing | The published effect makes the fin **more truncate**, i.e. symmetric — an Exocoetid needs an **asymmetric** enlargement of the lower lobe. So this is a handle on caudal shape, **not** on the direction the target needs. Recorded as a handle with the wrong sign. |
| P17 | **`szlA`/`szlB` disruption (T3, dorsoventral caudal patterning)** | `developmental`, `organ` | caudal bifurcation; distal ray separation; `chdA`/`eve1` levels | None | The published goldfish CRISPR design, repeated in a species with a normal single tail | `S-abs` PMID 42653322: 45–80% penetrance across three biological replicates, with partial splitting of the caudal skeletal complex | Produces **bifurcation**, not a longer lower lobe. Again the wrong phenotype, and in goldfish, a different family. Listed because it is the only dorsoventral caudal handle found, not because it is the edit to make. |
| P18 | **`klhl41b` dosage for burst-muscle power (T6)** | `cellular`, `organ`, `organism` | sarcomere organisation; force generation; swimming/escape kinematics | None. Nothing in this repo maps a sarcomere phenotype to launch power. | Existing zebrafish CRISPR model; force assays as published | `S-abs` PMID 42870309: required for sarcomere assembly and both radial and longitudinal growth, with force-generation assays | The published work is **loss**-of-function causing myopathy. The gain direction a wing would need is `H` and untested; over-expression of a sarcomere assembly factor may simply disorganise. |
| P19 | **`met` dosage for pectoral fin musculature (T11)** | `cellular`, `organ` | abductor fibre number; pectoral fin function | None | Existing `met` mutant as the loss reference; gain direction undesigned | `S-abs` PMID 31287821: `met` mutants lose migrating-progenitor-derived appendicular muscle, with reduced fibre number **particularly in the pectoral abductor** and disturbed fin function | This is the first row that addresses the **root** of the wing rather than the blade. `met` is pleiotropic across many migrating populations, so a fin-restricted perturbation does not exist in anything read here. |
| P13 | **`gli3`/Hedgehog dosage to reconfigure the pectoral girdle (T11)** | `organ`, `developmental` | girdle element dimensions; intramembranous vs endochondral bone fraction; glenoid geometry | None. No model in this repo couples girdle geometry to a load. The repo's clamped-free ray surrogate is about the blade, not the root. | Existing Gli/Hh compound mutant lines; micro-CT of the girdle; load-to-failure on the fin–body joint | `S-abs` PMID 40442084 (compound knockouts shift girdle character), PMID 39060278 (cleithrum lineage) | Hedgehog dosage is pleiotropic across the whole embryo; a girdle-restricted perturbation does not exist in anything read here. Likely lethal or grossly abnormal. |
| P14 | **`hhip` loss of function (radial number, T4)** | `tissue`, `developmental` | number and position of pectoral radials; Hox13 expression domains | None | Existing `hhip-/-` line; micro-CT | `S-abs` PMID 39417578 | Added after review: §2.3 cited `hhip` but the table had no row for it. More radials is not obviously *better* for a wing; the trait direction is a guess. `H` |
| P15 | **Measure the locomotor cost before editing anything (T12)** | `organism` | tail-flip jump kinematics, voluntary jumping, exhaustion; swimming cost | None needed — this is a measurement, not a model | Wildtype vs **longfin** zebrafish, the comparison already published as PMID 38232499; repeat with any new line | `S-abs` PMID 38232499 | Added after review as the **first** row that should be run, because it is cheap and it can kill the programme: if existing long-finned zebrafish already pay an unacceptable locomotor cost, every row above inherits it. |

### 4.1 Conflicts the table exposes (these are the useful output)

1. **P7 vs T1 — downgraded from a hard trade-off to an open question.** The edit that makes rays
   spiny-like (`hox13` loss) also shrinks the fin fold and deletes actinotrichia, so bigger and
   stiffer appeared to pull against each other through the same genes. But spiny-ray development in
   two other teleosts is reported to be **actinotrichia-independent**, proceeding via BMP-positive
   osteoblast condensation (`S-abs` PMID 41690953). A route to stiff rays that does not run through
   actinotrichia loss may therefore exist. The downgrade rests on one abstract in two non-model
   species and is not a solution.
2. **P10 vs T4.** `eda` loss removes scales *and* fin rays. A keel/scale edit is not separable from
   the ray programme at this read-level.
3. **P1 cardiac risk.** `kcnh2a` is Kv11.1; human mutations cause arrhythmia (`S-abs` PMID 42496271,
   general KCNH statement). An edit that is not cell-type-restricted is predictably dangerous.
4. **Regeneration ≠ development.** P6 and much of §2.2's strongest evidence come from *regenerating*
   adult fins. A wing must be built during *development*. PMID 38527087 is the one read that puts the
   K+ mechanism in the embryonic **bud**, which is why it carries extra weight here.
5. **Size without material is not a wing.** Every row that achieves T1 leaves T5 untouched. Nothing
   read here connects a genotype to a ray bending stiffness.
6. **The blade was designed and the root was forgotten** (found by review, not by this project).
   T1–T5 are all about dermal fin rays. A long stiff blade on a girdle and musculature sized for
   labriform swimming transmits its load into the body wall at a joint that nothing read here has
   measured. T11 and row P13 exist because of this; they are the weakest-sourced part of the plan and
   plausibly the binding constraint.
7. **Enlarging fins has a measured cost in the only organism in play.** A published comparison of
   wildtype and **longfin** zebrafish tested exactly the trait this plan proposes to amplify, across
   jump kinematics, voluntary jumping and exhaustion (`S-abs` PMID 38232499). This project read the
   abstract's hypothesis and design but **did not read the result**, so the direction and size of the
   effect are `U` here. Whatever it is, it bounds the whole programme, which is why P15 is first.
8. **Secondary hits are not copy number.** In the computed results, `-N5 --outs=0.6` was applied per
   assembly chunk, so a query can show more than five alternative hits. Those counts say nothing
   about duplication in the genome (see `RESULTS.md` §R2).

## 5. Engineering methods and feasibility

Layers kept separate per SPEC-012. Feasibility ratings are about *the method in zebrafish*, which is
the only organism any of this is established in.

| Layer | Option | Feasibility in zebrafish | Feasibility in an Exocoetid | Notes |
| --- | --- | --- | --- | --- |
| Regulation | Cell-type-specific promoter driving an effector | Established — the Development 2024 paper did exactly this for `kcnk5b`/`cx43` (`S-abs`) | `U` | Promoter leak is the dominant risk and must be measured, not assumed. |
| Regulation | Enhancer swap (Exocoetid element → zebrafish locus) | Method exists (Tol2 enhancer reporters, `S-meta`) | **Blocked**: no Exocoetid element coordinates. `U` | This is the experiment the project most wants and least can do. |
| Cargo | Reporter (EGFP) under a candidate element | Established | `U` | Reporter specificity does **not** establish an effector phenotype (SPEC-012). Reporter-first is mandatory. |
| Cargo | Effector (ion channel variant, TF) | Established for the named channels | `U` | — |
| Carrier | Plasmid / Tol2 | Established, small capacity | `U` | Mosaic in F0; germline needed for morphometry. |
| Carrier | BAC (recombineering) | Established in fish; the targeted query returned mostly unrelated records (`S-meta`), and a medaka transposon transgenesis paper (PMID 41068540) | `U` | A BAC is a **bacterial construct**, not an autonomous fish chromosome (SPEC-012). Large regulatory landscapes (Hox clusters) are the case for it. |
| Delivery | Injection at 1-cell | Established | `U` — no Exocoetid husbandry, spawning or embryo access was found at all. | **This is the hard stop for anything "in a flying fish".** |
| Integration | Targeted knock-in / HDR / prime editing | Published and improving (`S-meta` PMID 42411453, prime editors in zebrafish) | `U` | Efficiency is the cost driver; not quantified here. |
| Integration | Autonomous fish chromosome | **Not established.** | **Not established.** | Mammalian demonstrations do not transfer (SPEC-012). Research option only. |
| Validation | Morphometry + micro-CT + reporter distribution + viability | Established | `U` | Cell counts are not animal replicates (SPEC-012). |

**Feasibility verdict, stated plainly.** Making a *zebrafish with flying-fish-like fin proportions*
is a bounded, already-partly-published programme: PMID 34534441 reports that a `kcnh2a`×`lat4a`
interaction phenocopies flying-fish fin proportions in zebrafish. Making a *flying fish* is not a
genetics problem that this project can scope: it needs T3, T5, T6 and T8, for which this project
found **no candidate genes at all**, and it needs an organism (Exocoetidae) with no annotated genome,
no established husbandry, no transgenesis protocol and no embryo access in anything read here.

## 6. Known / inferred / unknown

**What a source states** — abstract-level, single operator, priority unverified. Read every item as
"the abstract of the cited paper states this", not as established biology; that distinction is the
whole point of §0 and an earlier draft of this section wrongly titled it "Known":
`longfin^t2` is a cis-regulatory `kcnh2a` allele acting through outgrowth duration in intra-ray
mesenchyme; a 35-species flying-fish phylogenomic study names `kcnh2a` and `lat4a` and reports a
zebrafish phenocopy of flying-fish fin proportion; RA→`rcan2`→Kcnk5b→Ca2+→`shha` scales the pectoral
fin bud; cell-type-specific bioelectric manipulation separates fin size from ray segment length;
`cacna1g` loss prolongs regenerative outgrowth; `hox13` loss shifts rays toward spiny character
while spiny rays in two other teleosts form without actinotrichia at all; a `shha` timing pulse and
`szlA`/`szlB` loss change caudal shape; `klhl41b` builds sarcomeres and supports muscle growth; `met`
brings migrating muscle progenitors into the paired fins; `hhip` constrains radial number; `hoxB` clusters position the pectoral fin via `tbx5a`; `and1/and2`
build actinotrichia and set fin-fold shape; `eda` loss removes scales and fin rays; a `pitx1` pelvic
enhancer is poised then activated; three Exocoetid species share 2n = 48; exactly one Exocoetidae
assembly is public and it is unannotated.

**Inferred / computed here** (`C-here`, receipts in `RESULTS.md`):
all 27 distinct candidate zebrafish query proteins have a detectable best-aligning region in
`GCA_018398805.1`; controls behaved (conserved actb1 at 0.989 identity, and all three shuffled
negative controls returned no hit); best-hit amino-acid identity spans 0.447 (hoxd13a) to 0.989 (the
actb1 control); `msxb` mapped identically in two independent runs. Three results limit the rest:
`shha`/`shhb` best-hit the same region, and a reciprocal test resolves that one in favour of `shha`
(5 of 5 predicted proteins); **the one `kcnh2`-like region is `kcnh2b`-like by a gene tree with a
passing positive control (99/100), so the plan's primary candidate locus `kcnh2a` is not located in
this assembly at all**;
and the `kcnh2a`, `kcnh2b` and `cacna1g` spans are each dominated by one ~0.1 Mb gap with 2–4
frameshifts, so those three are "something channel-like is there", not located genes. These are
alignments, not orthology calls.

**Unknown** (declared, not filled):
the coordinates and sequence of **every** regulatory element this plan would use; which UniProt
paralog the papers' `lat4a` is; **whether the detected `kcnh2`-like region is the `a` or the `b`
paralog**; where the Exocoetid `kcnh2a` is, if it is in this assembly at all; whether the `kcnh2b`-like region
is truly orthologous (no synteny was run); whether any Exocoetid locus is expressed, where or when; T3 caudal asymmetry, T5 ray
material properties, T6 launch muscle and T8 behaviour have no candidate gene; T11 girdle and T12
locomotor cost are sourced in zebrafish only; the *result* of the one published wildtype-vs-longfin
performance comparison, whose abstract was read but whose findings were not;
whether the zebrafish phenocopy is mechanically sufficient for gliding; Exocoetid husbandry,
spawning, embryo access and transgenesis — all absent; and whether any paper's figures support the
abstract sentences this plan leans on, since **no full text was read**.

## 7. Next actions, in order of information gained per unit cost

1. **Settled this session, and it went against the plan.** `kcnh2a` is **absent from the Beloniform
   lineage that contains flying fishes** — shown with a non-Beloniform outgroup (*Takifugu*) that
   retains the `a` copy at 100/100 while medaka and the flying fish carry the `b` copy (§R7f). The
   evidence within the assembly: the one `kcnh2`-like region is `kcnh2b`-like with a passing control (§R4), a
   low-stringency hunt found no new region (G9), a second tree assigned all five untested regions to
   other paralogs (§R7), and a family census found 9 of 10 KCNH paralogs do have a flying-fish locus
   while `kcnh2a` has none (§R7b). So the `longfin` gene has **no located target** in the only public
   Exocoetidae assembly and perturbation row **P1 cannot be designed against this genome**. It is a **lineage fact, not an assembly gap**: row **P1 has no
   target gene to edit**, and the next step is a literature one — read PMID 34534441's own gene
   identifiers in full text to see what its flying-fish `kcnh2a` signal refers to. This project has
   not read that paper's methods and does not claim it is wrong. Strengthening the result itself
   needs a **third Beloniform genome**, which was not run.
2. **Read the result of PMID 38232499** (wildtype vs longfin locomotor performance). One abstract-
   to-full-text step that can invalidate the whole programme, which makes it the cheapest possible
   kill test.
3. **Resolve the `lat4a` identifier** (§2.1). One full-text read; unblocks G4 and row P2.
4. **G4**: inspect the `lat4a`/`kcnh2*` aligned regions in `GCA_018398805.1` for the convergent
   residue. Pure computation on data already on disk, blocked only by steps 1 and 3.
5. **Read full texts** for PMIDs 34534441, 34061172, 38527087 — the three loads this plan rests on.
6. **G5** conserved-element scan, only after 1–5, and only reported as hypotheses.

## Receipts, sources, claims

- Computed results and receipts: [`RESULTS.md`](RESULTS.md)
- Source index (45 queries, verbatim bodies + sha256): [`SOURCES.md`](SOURCES.md), `data/source_index.json`
- Claim drafts in the repo's record format: [`claims/zf2ff-claims.json`](claims/zf2ff-claims.json)
- Review record (what an LLM critique changed): [`REVIEW.md`](REVIEW.md)
