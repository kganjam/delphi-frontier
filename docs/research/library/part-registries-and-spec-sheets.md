# Reusable-part registries for engineered biology, and what a real spec sheet contains

**Status:** research note · single-reader (this session), NOT independently reviewed · 2026-11-04
**Purpose:** input to the design of our own parts library. Comparative, not neutral: the point is to
copy the two or three things that worked and refuse the things that failed.

> **Honesty floor.** Every external claim below carries a **read-level**:
> `full-text` (I read the text, or a fetch of the text, end to end for the claim),
> `extracted` (an automated reader returned the numbers from the full text; I did not see the page myself),
> `abstract` (abstract or record only), `listing` (bibliographic record only),
> `search-summary` (a search engine's summary of a page I could not open),
> `could-not-access` (named and tried, failed).
> Claims marked **INFERENCE** are mine and are not in any source.
>
> **Egress limits of this session, stated up front.** The following hosts were refused by this
> session's network policy, so nothing below is a first-hand read of them:
> `parts.igem.org`, `registry.igem.org`, `api.registry.igem.org`, `synbiohub.org`,
> `www.addgene.org`, `api.addgene.org`, `public-registry.jbei.org`, `biobricks.ai`,
> `sbolstandard.org`, `seva-plasmids.com`, `static.igem.org`, `openwetware.org`, `docs.rs`,
> `dspace.mit.edu`, `link.springer.com`, `academic.oup.com` (403), `www.uv.es`,
> `jakebeal.github.io`, `en.wikipedia.org`. `www.nature.com` resolves but paywalls.
> Reachable and used: `pmc.ncbi.nlm.nih.gov`, `eutils.ncbi.nlm.nih.gov`, `arxiv.org`,
> `pypi.org` (and therefore package source code), plus web search summaries.
> **Where a registry's own live behaviour matters, I read its official client library's source code
> instead of its website, and say so.** That is weaker evidence about the live service and stronger
> evidence about the data model.

---

## 0. The five-line version

1. The iGEM Registry solved *physical* composability (one assembly standard, one plasmid backbone,
   one distribution) and never solved *informational* composability. Its data model has no field
   that can hold a performance claim, so performance claims live in free prose or nowhere.
2. The one serious attempt at an engineering datasheet for a genetic part — Canton, Labno & Endy
   (2008) — was a demonstration, not a schema. Nothing in the Registry's record structure was
   changed to hold its contents, so it did not propagate.
3. The measurement-standards branch (RPU, calibrants) is the part of that programme that *did*
   survive, because it reduced a number people already reported, rather than asking for new work.
4. SBOL 3 is a good *structural* model (hierarchy, interfaces, constraints, provenance) with a
   deliberately thin *quantitative* model: `Measure` is a bare value+unit. No uncertainty, no
   conditions, no min/typ/max, no envelope, no failure boundary.
5. The registries that stayed alive distribute material and verify sequence (Addgene), or are
   vector-architecture standards with a maintained erratum trail (SEVA), or are toolkits where the
   characterisation *was the paper* (YTK/MoClo). Quality came from a gate at submission, not from
   hoping contributors would characterise after the fact.

---

## 1. BioBricks and the iGEM Registry, with the failure analysis

### 1.1 What RFC[10] actually specifies

RFC 10 is an *assembly* standard: a prefix and a suffix flanking the part, four restriction sites
placed in them, and a rule that those sites must not occur inside the part.

| element | value | read-level |
|---|---|---|
| prefix (general parts) | `GAATTCGCGGCCGCTTCTAGAG` | search-summary (`parts.igem.org/Help:BioBrick_Prefix_and_Suffix`, blocked to me) |
| prefix (part begins `ATG`) | the same, with the terminal `AG` dropped so the start codon is in frame | search-summary |
| suffix (always) | `TACTAGTAGCGGCCGCTGCAG` | search-summary |
| sites in prefix | EcoRI, XbaI | search-summary + `full-text` (see motif table below) |
| sites in suffix | SpeI, PstI | search-summary + `full-text` |
| standard scar | `TACTAGAG` (8 bp); `TACTAG` where the second part begins `AT` | search-summary |
| consequence | the 8 bp scar carries a frameshift and a stop, so RFC 10 cannot make in-frame protein fusions; RFC 23 ("Silver") exists to give a 6 bp scar | search-summary |

The *forbidden-motif* side of RFC 10 I was able to verify from code rather than from the blocked
wiki. The official-style Python client for the current Registry (`igem-registry-api` 0.1.0 on PyPI,
installed and read: `igem_registry_api/part.py`) hard-codes the motif sets it checks a submitted
sequence against — `full-text` of that source:

```
RFC10    : GAATTC (EcoRI), TCTAGA (XbaI), ACTAGT (SpeI), CTGCAG (PstI), GCGGCCGC (NotI)
RFC12    : the RFC10 five, plus GCTAGC (NheI), GCCGGC (NgoMIV), ACCGGT (AgeI)
RFC21    : GAATTC (EcoRI), AGATCT (BglII), GGATCC (BamHI), CTCGAG (XhoI)      # BglBrick
RFC23    : GAATTC, TCTAGA, ACTAGT, CTGCAG                                     # Silver
RFC25    : the RFC23 four, plus GCCGGC (NgoMIV), ACCGGT (AgeI)                # Freiburg
RFC1000  : GGTCTC / GAGACC (BsaI ±), GCTCTTC / GAAGAGC (SapI ±)               # Type IIS
```

The same file records the standards' identifiers as DSpace handles — RFC10 `1721.1/45138`,
RFC12 `1721.1/45139`, RFC21 `1721.1/46747`, RFC23 `1721.1/32535`, RFC25 `1721.1/45140`, and
RFC1000 "TypeIIS" with no handle given (`full-text`). I did **not** read the RFC documents
themselves; `dspace.mit.edu` is blocked here. **I am not asserting any RFC number beyond these
six, and I did not see RFC 95 implemented anywhere** (see §1.4).

### 1.2 The `BBa_` numbering scheme, old and new

- `BBa_` = "BioBrick alpha"-style namespace prefix; the letter following it encodes a rough
  category — e.g. `BBa_B…` generic basic parts (terminators, RBSs), `BBa_C…` protein coding; team
  and lab groups are allocated a *range* from which they pick the next free number
  (`BBa_K…` and `BBa_J…` ranges are the iGEM-team blocks). Read-level: `search-summary`
  (`parts.igem.org/Help:BioBrick_Part_Names`, `Part_Names`, blocked).
- The **current** Registry no longer treats `BBa_…` as the primary key. From the client source
  (`full-text`): every part has a `uuid` (UUID4), an integer `id`, and a URL **slug** of the form
  `bba-0000000001`; a part can be fetched by either `uuid` or `slug`
  (`GET {base}/parts/{uuid}`, `GET {base}/parts/slugs/{slug}`).
- **INFERENCE:** the move from a human-chosen, range-allocated mnemonic to a UUID + slug is the
  single correction most visible in the new Registry, and it is exactly what Peccoud et al.
  recommended in 2008 (§1.3: "give each clone a unique key separate from part numbers").

### 1.3 What a part record actually contains

Two generations, and the difference matters.

**Legacy part page (wiki-era).** The record was a MediaWiki page plus a sequence. The Registry's own
API guidelines told third-party tools that the *required* display fields were only: part number
(`BBa_…`) with a link, authorship, and date of entry; *recommended* were short description, part
type, sequence, and links to the Experience and Design pages (`search-summary`,
`parts.igem.org/Registry_API/Guidelines`). Characterisation lived on sub-pages — for BBa_F2620,
`:Specificity`, transfer-function, response-time and stability pages (`search-summary`) — i.e. as
free prose and images under a naming convention, not as fields.

**Current Registry part object**, read from the client source (`full-text`,
`igem_registry_api/part.py`). The fields are:

```
uuid, id, slug, name, status, title, source, description, type, categories,
license, sequence, deleted, audit, composition, authors, annotations
```

with related sub-resources `GET /parts/{uuid}/authors`, `/composition`, `/sequence-features`,
`/twins`, `/uses`, and a lifecycle `status` enum — `draft | screening | published | rejected`.
Part types and categories are controlled vocabularies served from `/parts/types` and
`/parts/categories`; the category vocabulary is a deep path hierarchy
(`//cds/enzyme/endonuclease/restriction`, `//biosafety/kill_switch`,
`//cds/reporter/gfp`, …), which the client enumerates in full.

**This is the central data-model finding of the whole note:** in that field list there is
**no field for a measured value, no field for measurement conditions, no field for a host context,
and no field for a performance envelope.** There is `description` (prose), `annotations`
(sequence-level), and `composition` (structure). A quantitative claim about a part has nowhere to
go except prose. `status: published` is an editorial state, not a functional one.

### 1.4 The quality problem, quantified as far as anyone has quantified it

**(a) Peccoud et al. 2008, PLoS ONE 3(7):e2671, "Targeted Development of Registries of Biological
Parts"** — the only systematic physical audit I could find. Read-level: `extracted` (full text via
PMC; numbers returned by an automated reader, not eyeballed by me).

- Registry held **4,856 entries** (July 2007); the physical clone collection **995 clones** —
  279 "Parts", 716 Devices/Systems.
- Of 4 × 384-well plates received: **216 clones failed to amplify**, **190 gave multiple peaks**,
  **789 gave a single product >120 bp and were sequenced**.
- Of those 789, only **509 had a published sequence** to compare against — i.e. **~280 (≈35%) of
  sequenced clones had no reference sequence in the Registry at all**.
- **591** of 789 assembled into contigs; **354** matched a Registry entry; **237 were undocumented**
  in that distribution; **334** produced a BLAST alignment with their published sequence.
- After length-consistency and coverage filters, **177** clones were comparable; all 177 were
  ≥97% identical to their published sequence and **162 were ≥99%**.
- Length agreement across all 509: **R² = 0.33**, rising to 0.98 only after manually removing
  **76 outliers**; **only 285 of 509 (56%) had length differences under 10%**.
- Abstraction-hierarchy violations: **49 part-in-part** and **12 design-in-part** inclusion
  relationships, which the authors flag as unexpected and inconsistent with the stated hierarchy.
- Reuse: **502 entries never reused**; **80% of reused entries used fewer than 3 times**; the
  most-used entry (a double terminator) appeared in **70 designs**.
- The paper explicitly **does not** report a "characterised" or "works" rate — it says the
  usefulness attribute (working / working with issues / not working) could not be analysed from the
  partial data dump available.

Derived, and flagged as arithmetic on their numbers rather than their claim: **162 of 789 sequenced
clones (≈21%) were confirmed at ≥99% identity to a published Registry sequence.** The honest reading
is that the other 79% are a mix of genuinely wrong clones, clones with no reference to check
against, and reads that failed for technical reasons — the paper is careful that its own filters do
most of the work, and calls itself "a snapshot of one distribution".

**(b) iGEM's own policy, which is the most important single quote here.** The Registry FAQ states
that iGEM HQ **"cannot make any qualitative statements on if a part functions as described"**, that
QC is Sanger sequencing, and that **parts under 1600 bp are fully sequence-confirmed while long
parts are not** (`search-summary`; `parts.igem.org/Help:FAQ`, blocked). Sequence QC results are
bucketed as Confirmed / Partially Confirmed / Inconsistent / Long Part (`search-summary`,
`parts.igem.org/Help:Quality_Control`).

**(c) Kwok 2010, Nature 463:288–290, "Five hard truths for synthetic biology"** — read-level
`search-summary` (paywalled; `doi:10.1038/463288a`). Reported: the Registry had **>5,000 parts
orderable** and, per then-director Randy Rettberg, **does not guarantee their quality**; the article
reports **about 1,500 parts confirmed as working**. First "hard truth" is that many parts are
undefined or work unpredictably in different configurations. **Caveat: I could not open the article;
the 1,500 figure is second-hand and its definition of "confirmed working" is unstated. Treat it as
an order-of-magnitude claim (≈30% at that date), not a measured rate.**

**(d) Alnahhas et al. 2014, J Biol Eng 8:28** (Barrick lab), "The case for decoupling assembly and
submission standards…". Read-level: `extracted` (full text via PMC).

- Most parts derived from natural sequences **longer than 710 bp** are predicted to contain at least
  one of the four RFC 10 sites; above **2,360 bp** the predicted fraction exceeds **90%**.
- Among parts marked **"Not Released"**, the share designed by recent iGEM teams containing an
  illegal site is **>15% and rising** (data to 2013-07-29).
- Survey of 44 team members/mentors: **43%** most often used one-pot assembly rather than
  restriction cloning; **52%** had used site-directed mutagenesis purely to remove illegal sites;
  **36% had decided not to submit a part at all because of illegal sites.**
- They propose **RFC 95**, a submission-only standard using homing-endonuclease sites (15–30 bp,
  unlikely to occur by chance below ~20 kb), decoupling "can be archived" from "can be assembled
  this one way".

That 36% is the sharpest number in this whole note for library design: **a submission standard that
rejects material makes the registry's coverage a function of the standard, not of the science.**
Note also that RFC 95 does **not** appear in the current Registry client's supported-standards enum
(§1.1) — so, on that evidence, it was not adopted (`full-text` of the client; **INFERENCE** as to
why).

**(e) Vilanova & Porcar 2014, Nat Biotechnol 32:420–424, "iGEM 2.0—refoundations for engineering
biology"** (`doi:10.1038/nbt.2899`). Read-level: **could-not-access** for the numbers. The figure
legend (Fig. 2c) does describe "proportions of verified parts (labeled as 'working' in the registry)
and untested or nonworking parts submitted to the registry … 2006–2013", and the text notes
ambiguous data for some teams, but both nature.com and the author's PDF host were unreachable from
this session. **I will not quote a percentage from this paper.** If we want that number it is one
library fetch away and should be done before we cite it.

**(f) Scale and current state.** The legacy `parts.igem.org` is now **archive/read-only**; the live
service is `registry.igem.org` (self-described beta), which received a **major overhaul in
August 2025 adding a REST API** whose **documentation is a Swagger listing with no schemas or field
definitions** — which is why an iGEM team (Munich 2025) reverse-engineered the backend to publish
the client library I have been reading (`search-summary` for all four claims; the library itself is
`full-text`).

### 1.5 So what went wrong: governance, incentive, or data model?

All three, in that causal order. This subsection is **INFERENCE** built on §1.3–1.4.

- **Data model (the root).** There was never a field whose type was "a measured number with its
  conditions". A registry cannot enforce, index, query, diff or review a claim it cannot represent.
  Everything downstream follows: you cannot make characterisation a *gate* if characterisation is
  prose. The current record list (§1.3) shows this was never fixed, only re-plumbed.
- **Incentive.** The contributor is a student team on an annual clock, and the reward (medals) was
  tied to *submitting* parts and later to *documenting* them — volume and prose, not reproducible
  measurement. The user of a part is a different team the following year, who bears the cost of the
  missing characterisation. Classic externality: the cost of a bad record falls on someone who had
  no say in making it.
- **Governance.** HQ explicitly declined to adjudicate function ("cannot make any qualitative
  statements…", §1.4b) while continuing to accept and ship the material. That is a coherent position
  for a teaching competition and a fatal one for an engineering catalogue, because the catalogue's
  only quality signal — "it is in the Registry" — then means "someone once sent us a tube".
  Simultaneously the *assembly* standard was enforced strictly enough to deter 36% of would-be
  submitters (§1.4d). The governance effort went to the axis where it could be mechanically checked
  (restriction sites in a string) and not to the axis that mattered.

**Design consequence for us:** do not accept a record whose performance claim cannot be
machine-checked for *form* (value, unit, conditions, method, n, uncertainty) even when nobody can
check it for *truth*. Form-checking is cheap, mechanisable, and is the thing iGEM never had.

---

## 2. The "datasheet for a biological part" literature

### 2.1 Canton, Labno & Endy (2008)

**Canton B, Labno A, Endy D. "Refinement and standardization of synthetic biological parts and
devices." Nat Biotechnol 26(7):787–793, July 2008. `doi:10.1038/nbt1413`, PMID 18612302.**
Read-level: `abstract` (full abstract retrieved via NCBI E-utilities), plus `search-summary` for the
datasheet contents and `could-not-access` for the article body (Nature paywall; the datasheet PDF
lives on the blocked `parts.igem.org`). There is a companion commentary, Nat Biotechnol
26(7):771–774 (`listing`, from PubMed's "Comment in").

From the abstract (`full-text` of the abstract): they "propose to adapt existing frameworks for
describing engineered devices to biological objects", apply it to one device — the cell–cell
communication receiver **BBa_F2620** — and summarise it "via a 'datasheet' similar to those widely
used in engineering", offering the process as "a starting template".

What the datasheet contained, from the Registry's F2620 pages and the datasheet PDF as summarised by
search (`search-summary`, not verified against the PDF itself):

| datasheet element | reported content for BBa_F2620 |
|---|---|
| input / output | input 3OC6HSL (AHL); output PoPS (polymerase per second), the proposed common signal carrier for gene expression |
| transfer function | max output **6.6 PoPS/cell**; half-maximal at **≈1.5 nM** 3OC6HSL; **Hill coefficient 1.6** |
| dynamic response | response time **under one minute** |
| input specificity | transfer function measured against **8 different input molecules**, error bars = 95% CI over **3 replicates** |
| stability | both **genetic** stability and **performance** stability over time |
| composability demonstration | behaves as a Boolean AND gate when combined with a TetR/aTc system |
| composition | built from BBa_R0040, B0034, C0062, B0015, R0062 |

**What is not evidenced:** I found no evidence of named "compatibility" or "reliability" fields, and
I am not going to invent the datasheet's section headings. The honest statement is: **the 2008
datasheet is a worked example with a transfer function, a response time, a specificity sweep and a
stability statement, measured under stated conditions — not a published field schema.**

### 2.2 Standard units: RPU and the reference-standard idea

**Kelly JR, Rubin AJ, Davis JH, Ajo-Franklin CM, Cumbers J, Czar MJ, de Mora K, Glieberman AL,
Monie DD, Endy D. "Measuring the activity of BioBrick promoters using an in vivo reference
standard." J Biol Eng 3:4, 2009. `doi:10.1186/1754-1611-3-4`, PMC2683166.** Read-level: `full-text`
of the structured abstract (via E-utilities); `extracted`/`search-summary` for the rest.

- Stated premise, in the authors' own words: BioBrick parts "are only standardized in terms of how
  individual parts are physically assembled … and **most parts remain uncharacterized**."
- Finding: **absolute** promoter activity varies across experimental conditions and measurement
  instruments.
- Remedy: nominate **BBa_J23101** as an *in vivo* reference standard; report activity relative to
  it; define the **Relative Promoter Unit (RPU)**; ship a **measurement kit** to lower adoption cost.
- Effect size: relative measurement **reduced variation due to test conditions and instruments by
  approximately 50%**; a test set distributed to multiple labs gave good agreement.

This lineage continued into calibration rather than datasheets:

- **Beal J et al., "Quantification of bacterial fluorescence using independent calibrants", PLoS ONE
  2018 (PMC6013168)** — `listing`/`search-summary`.
- **"Robust estimation of bacterial cell count from optical density" (PMC7499192)** — `listing`.
- **Comparative analysis of the 2016/2017/2018 iGEM interlab studies, PLoS ONE 2021
  (`doi:10.1371/journal.pone.0252263`)** — `search-summary`: plate-reader calibration precision
  held across all three years with **CV < 0.1** for LUDOX and water calibrants; **lab-to-lab
  variation reported as geometric standard deviation ≈2.4-fold (CFU calibration) and ≈2.21-fold
  (LUDOX/water and microsphere), improving to 2.02 / 1.84 / 1.83-fold after dropping problematic
  constructs**. The 2016 study ran at **92 institutions**; the first (2014–15) at **88**, where
  "few participants were able to measure absolute fluorescence" at all.

**Read those two numbers together:** a *relative* unit buys ~50% variance reduction; even with
calibrants, the residual between-lab spread on a simple constitutive construct is a factor of
~1.8–2.4. That is the empirical floor for how tight any "nominal value" in a biological spec sheet
can be without naming the lab.

### 2.3 Why datasheets did not take over

Documented facts first:

- The 2008 paper positions itself as a *template* and a *proposal*, and the follow-up effort in the
  same group went into units and calibration (§2.2), not into a datasheet schema.
- The Registry's record structure has **no fields** for datasheet content, in either generation
  (§1.3). The characterisation that was done lived on prose sub-pages.
- iGEM's own medal rules drove *documentation*, where "documentation may come in the form of a
  simple 'this works/doesn't work,' or an in-depth review" (`search-summary`,
  `registry.igem.org/help/part-and-part-collection-documentation`) — an explicitly unbounded
  quality bar.
- SBOL, the field's data standard, models a measurement as a bare value + unit (§3), i.e. the
  interchange format cannot carry a datasheet either.

**INFERENCE (mine):** the datasheet failed for four compounding reasons, none of which is "people
didn't care":
1. **Cost asymmetry.** The F2620 datasheet represents months of work on *one* device. Nothing paid
   for the second one, and the marginal user could not tell a characterised part from an
   uncharacterised one *in the catalogue UI*, so the characterised part captured no advantage.
2. **No slot to put it in.** A datasheet with no field is a PDF. A PDF is not queryable, diffable or
   reviewable, so it cannot gate anything, so it does not accumulate.
3. **The units problem is upstream of the datasheet.** PoPS was never directly measurable; RPU was,
   which is exactly why RPU partly survived and PoPS-denominated datasheets did not. A datasheet
   field whose unit nobody can measure is a dead field.
4. **Context dependence is real, not laziness.** With between-lab spread of ~2-fold *after*
   calibration, and strong host/background dependence, a single nominal value is genuinely close to
   meaningless unless the conditions travel with it — which is an argument for *more* schema
   (conditions as first-class fields), and was instead taken as an argument against datasheets.

---

## 3. SBOL 3, in detail

**Specifications.** SBOL 3.0.0 — J Integr Bioinform, 2020 (PMC7756618). SBOL 3.1.0 — J Integr
Bioinform 20(1), March 2023, `doi:10.1515/jib-2022-0058` (PMC10063177). SBOL Visual 3.0 —
2021 (PMC8560346). Read-levels: `abstract` for 3.1.0 (its PMC landing page; the PDF download was
blocked and `sbolstandard.org` is unreachable from here), `listing` for the others.

From the 3.1.0 abstract (`abstract`): 3.1.0 adds a complete set of **validation rules**; moves best
practices to an online repository; **removes the `Namespace` class** in favour of a `namespace`
property on each class; generalises `CombinatorialDerivation` to allow direct use of `Feature`s and
`Measure`s; lets `Interaction`s act as participants (higher-order interactions); uses Sequence
Ontology terms for feature orientation; generalises URIs to IRIs.

**The data model, read from the reference implementation.** Because the spec PDF was unreachable, I
installed and read **pySBOL3 1.2.0** (`sbol3` on PyPI, `github.com/SynBioDex/pySBOL3`), the SBOL
Developers' own Python implementation. Read-level: `full-text` of the package source. Property names
below are the RDF predicates the code emits (namespace `http://sbols.org/v3#`), with cardinalities
as declared in the code.

| class | key properties (cardinality) |
|---|---|
| `TopLevel` (abstract) | `hasNamespace`, `hasAttachment`*, `name`, `description`, `prov:wasDerivedFrom`*, `prov:wasGeneratedBy`*, `hasMeasure`* |
| `Component` | `type` (1..∞), `role`*, `hasSequence`*, `hasFeature`*, `hasInteraction`*, `hasConstraint`*, `hasInterface` (0..1), `hasModel`* |
| `Feature` (abstract) → `SubComponent`, `LocalSubComponent`, `ExternallyDefined`, `SequenceFeature`, `ComponentReference` | `role`*, `orientation`, plus per-subclass: `SubComponent.instanceOf` (1..1), `hasLocation`*, `sourceLocation`* |
| `Location` → `Range`, `Cut`, `EntireSequence` | `start`, `end`, `order`, `orientation` |
| `Constraint` | `restriction` (1..1), `subject` (1..1), `object` (1..1) |
| `Interface` | `input`*, `output`*, `nondirectional`* |
| `Interaction` / `Participation` | `type`* (SBO terms), `hasParticipation`*; `Participation.role`*, `participant` |
| `Sequence` | `elements`, `encoding` |
| `Model` | `source`, `language`, `framework` |
| `CombinatorialDerivation` / `VariableFeature` | `template`, `strategy`, `hasVariableFeature`*; `variable`, `variant`, `cardinality` |
| `Implementation` | `built` (0..1) → a `Component` |
| `ExperimentalData` | **(no properties of its own)** — inherits `TopLevel`, i.e. it is a named bag of `hasAttachment` links |
| `Experiment` (subclass of `Collection`) | `member`* which MUST refer to `ExperimentalData` |
| `Attachment` | `source` (1..1), `format` (0..1), `size` (0..1), `hash` (0..1), `hashAlgorithm` (0..1) |
| `om:Measure` | `om:hasNumericalValue` (1..1, float), `om:hasUnit` (1..1), `type`* |
| `om:Unit` family | `SingularUnit`, `CompoundUnit`, `Prefix` with `om:symbol`, `om:label`, alternatives, `factor` |
| PROV | `prov:Activity`, `prov:Usage` (`entity`, `hadRole`), `prov:Agent`, `prov:Plan`, `prov:Association` |

`Constraint.restriction` has a RECOMMENDED vocabulary, enumerated in the code with pointers to spec
tables 7–9: identity/orientation — `verifyIdentical`, `differentFrom`, `replaces`,
`sameOrientationAs`, `oppositeOrientationAs`; topology — `isDisjointFrom`, `strictlyContains`,
`contains`, `equals`, `meets`, `covers`, `overlaps`; sequential — `precedes`, `strictlyPrecedes`,
`finishes`, `starts`. Interaction types and participation roles are SBO terms (inhibition 0000169,
stimulation 0000170, genetic production 0000589, …). Design–build–test–learn predicates exist as
URIs (`design`, `build`, `test`, `learn`).

### 3.1 What SBOL 3 covers well

Structural hierarchy with re-use (`Component`/`SubComponent`/`ComponentReference`), an explicit
**interface** (inputs/outputs/nondirectionals), **relational constraints** between features
including partially-specified designs, combinatorial libraries, links from design → built artefact
(`Implementation.built`) → data files (`ExperimentalData` + `Attachment`, with content hash), and
**full PROV-O provenance** (activity, usage, agent, plan). Attachments carry `hash`/`hashAlgorithm`,
which is real content-addressing. For a *design* interchange format, this is a good model.

### 3.2 What SBOL 3 does not cover

Read-level: `full-text` of the implementation, i.e. these are absences in the class/property set.
I did not read §6 of the spec prose, so treat "the spec forbids it" as unproven; "the model has no
property for it" is what I am claiming.

- **A quantitative performance envelope.** `Measure` is `value` + `unit` + optional `type` URI.
  There is no `uncertainty`, no `n`, no `min`/`typical`/`max`, no distribution, no confidence
  interval. A single number is the atom.
- **Measurement conditions.** No property anywhere attaches a condition set (medium, temperature,
  inducer concentration, growth phase, host strain, instrument, gain) to a `Measure`. Conditions can
  only be smuggled in as (a) prose in `description`, (b) an `ExperimentalData`/`Attachment` file the
  reader must parse, or (c) a custom-annotation extension.
- **A failure boundary.** Nothing expresses "above 2 mM inducer this construct is cytotoxic",
  "loses function after 20 generations", or "absolute maximum". `Constraint` is about *structural*
  relations between features, not about operating limits.
- **Mechanical / physical properties.** No concept of force, stiffness, geometry, binding kinetics,
  thermostability, or any non-sequence physical quantity other than as a bare `Measure` with a
  unit — which means the *number* can be represented but its *meaning* cannot be typed, except by
  inventing a `Measure.type` URI, which the spec leaves to the user.
- **The link from a quantity to the conditions that produced it** is the single structural gap.
  `Measure` hangs off any `Identified`, including a `SubComponent` or an `Interaction`, but it hangs
  off it *unconditionally*.

### 3.3 What an extension would look like

**INFERENCE / design sketch.** SBOL 3 is extensible by design (custom classes and annotations in
your own namespace, and `Measure.type`), so this is additive rather than a fork:

1. **`PerformanceClaim`** (a new `TopLevel`): `about` → the `Component`/`Feature`/`Interaction`;
   `quantityKind` → a typed URI (promoter activity, Kd, kcat, fold-change, generation time,
   stiffness, …); `nominal`, `min`, `max`, `uncertainty` as `Measure`s; `n`; `distribution`;
   `derating` curve as a sampled table attachment plus a model reference.
2. **`ConditionSet`** (new `TopLevel`, referenced by `PerformanceClaim.underConditions`, 1..1 —
   *required*, so a claim without conditions is invalid): host strain/`Component`, plasmid copy
   number or integration locus, medium, temperature, inducer `Measure`s, growth phase, instrument,
   calibration standard (e.g. "RPU vs BBa_J23101", "microsphere-calibrated FITC").
   The required cardinality is the whole point: it is the one rule iGEM never had.
3. **`OperatingEnvelope`**: `recommendedRange` and `absoluteMaximum` per condition dimension, plus
   `failureMode` (free-text + a controlled vocabulary) and `failureBoundary` as a predicate over
   conditions.
4. **Reuse what exists:** `om:Measure`/`om:Unit` for all quantities; `prov:Activity`/`Plan` for who
   measured it with what protocol; `ExperimentalData` + `Attachment` (with `hash`) for the raw data
   behind every claim — so a claim is refusable if its attachment hash does not resolve.
5. **Validation rules**, in the style SBOL 3.1.0 added for structure: a `PerformanceClaim` MUST have
   a `ConditionSet`, MUST have a `quantityKind` from a registered vocabulary, MUST cite at least one
   `ExperimentalData`, and SHOULD name the calibration standard.

---

## 4. Other registries, compared

Caveat for the whole section: every registry website in it is blocked from this session, so
"identifier scheme" and "acceptance gate" come from the primary papers, official client/MCP source
code, or search summaries of the registries' own help pages — marked per row.

### 4.1 Addgene — material distribution with a real sequencing gate

| axis | what it does | read-level |
|---|---|---|
| identifier | Addgene plasmid number (catalogue ID, e.g. `#12345`); registered in Bioregistry as `addgene` | `search-summary` |
| acceptance gate | **every incoming plasmid is sequenced** — "we sequence all incoming plasmids using Next Generation Sequencing" and "each full plasmid sequence is verified prior to the plasmid being made available for distribution"; previously in-house Illumina MiSeq with **de novo circular assembly (no reference)**; in 2026 most QC sequencing moved to Plasmidsaurus | `search-summary` (Addgene help centre + blog) |
| discrepancies | NGS result is aligned to the depositor's full/partial sequence (which "can be assembled or theoretical"); differences are logged as **QC issues**; often distributed anyway if function is unaffected; if likely to affect function, **a sequence-verified replacement is requested and QC restarts**; if no full assembly is possible, a **partial sequence** is published | `search-summary` |
| physical material | yes — this is the core service | `search-summary` |
| characterisation | **not** a structured field. Addgene records sequence, vector backbone, markers, species, expression system, depositor and the associated publication. Functional characterisation is by reference to the paper. | `search-summary` + the field vocabularies in the community MCP client (`full-text`, see §6) |
| API | official read-only API via `developers.addgene.org`, **approval-gated**: an access request per scope with a data-access licence; catalogue scope currently plasmids + viral preps, more types planned late 2026; daily refreshed **bulk JSON** (PI names excluded). Website sequence viewing now requires login, explicitly in response to at-scale scraping. | `search-summary` |

**What works, and why it is the single most imitable thing here:** the gate is *mechanical and
universal* (sequence every deposit), the failure mode is *recorded rather than hidden* ("QC issue",
"partial sequence"), and the registry **never claims the part works** — it claims the molecule is
what the depositor said it is. Addgene separated "is this the right DNA" from "does it do the thing"
and then actually enforced the first. iGEM conflated them and enforced neither.

### 4.2 JBEI-ICE — the institutional registry platform

**Ham TS, Dmytriv Z, Plahar H, Chen J, Hillson NJ, Keasling JD. "Design, implementation and practice
of JBEI-ICE: an open source biological part registry platform and tools." Nucleic Acids Res
40(18):e141, 2012. `doi:10.1093/nar/gks531`, PMC3467034.** Read-level: `extracted` (full text via
PMC). The live instance `public-registry.jbei.org` is blocked from this session, so current
behaviour is unverified.

- **Identifier:** entries are keyed by **UUID**, explicitly so that names do not collide across
  independently run installations; part numbers also exist but the paper does not specify a format.
  (Our `search-summary` sources' "`JPUB_…`" style was **not** confirmed by the paper — I am not
  asserting it.)
- **Entry types:** plasmids, microbial host strains, *Arabidopsis* seeds, part libraries, DNA parts
  in assembly standards (BioBrick mentioned).
- **Acceptance gate:** essentially none beyond a name/number and short description; sequence
  annotations are stored "only when provided".
- **Physical material:** entries can be **associated with physical samples** (location/freezer
  tracking); the paper does not claim ICE distributes material.
- **Characterisation:** free **attachments**, plus **`.ab1` sequencing traces** aligned in a built-in
  SequenceChecker. **No structured characterisation schema.**
- **Access/federation:** per-entry read/write permissions, groups, admin collections; instances can
  **peer** with a public instance ("web of registries"); SOAP + Java ABI at publication (REST was
  noted as possible, not present); **SBOL import/export**, plus GenBank and FASTA.

**Lesson:** ICE got federation and permissions right early (UUIDs, peering, per-entry ACLs) and is
the clearest demonstration that *attachments are not characterisation*. A trace file and a PDF in a
blob store give you an audit trail and no queryable performance data.

### 4.3 SynBioHub — the SBOL-native design repository

**McLaughlin JA, Myers CJ, Zundel Z, Mısırlı G, Zhang M, Ofiteru ID, Goñi-Moreno A, Wipat A.
"SynBioHub: A Standards-Enabled Design Repository for Synthetic Biology." ACS Synth Biol
7(2):682–688, 2018. `doi:10.1021/acssynbio.7b00403`, PMID 29316788.** Read-level: `full-text` of the
abstract (E-utilities); `search-summary` for the API surface; `could-not-access` for the live site.

- **Identifier:** URI-based, SBOL-native — a design's identity *is* its IRI, and SynBioHub is
  positioned as "a central reference point for other resources to link to".
- **Acceptance gate:** submission of SBOL (or convertible formats); the paper's framing is sharing
  and reproducibility, not vetting. I found **no evidence of a quality gate**.
- **Physical material:** none. It is a design repository.
- **Characterisation:** whatever SBOL can carry (§3) — i.e. `Measure`s and attached
  `ExperimentalData`. No richer model than the standard's.
- **API:** documented at `synbiohub.github.io/api-docs` — a `search` endpoint with `key=value`
  filters plus `offset`/`limit`, "Search Similar", "Search Uses", **sequence search**, a
  **SPARQL** endpoint (`GET /sparql?query=…`, format via `Accept`), `/admin/sparql`, and a
  submission-endpoint section whose contents I could not retrieve. Auth via `X-authorization` token.
  (`search-summary`.)
- **Federation:** connects to the iGEM repository and JBEI ICE and to other SynBioHub instances
  (`full-text` of abstract).

**Lesson:** SynBioHub is the right *shape* — standards-native, URI-identified, SPARQL-queryable,
federating — and inherits the standard's quantitative thinness. A SPARQL endpoint over a model that
cannot express conditions lets you ask structural questions beautifully and performance questions
not at all.

### 4.4 Toolkit standards: Yeast Toolkit and MoClo

**Weber E, Engler C, Gruetzner R, Werner S, Marillonnet S. "A Modular Cloning System for
Standardized Assembly of Multigene Constructs." PLoS ONE 6(2):e16765, 2011.
`doi:10.1371/journal.pone.0016765`.** Read-level: `search-summary`.
Hierarchical Type IIS assembly: **level 0** modules = promoters, 5′UTRs, signal peptides, CDSs,
terminators; assembled transcription units are **level 1**; multigene constructs are **level 2**.
Demonstrated a **33 kb, 11-transcription-unit construct from 44 basic modules in three cloning
steps**.

**Lee ME, DeLoache WC, Cervantes B, Dueber JE. "A Highly Characterized Yeast Toolkit for Modular,
Multipart Assembly." ACS Synth Biol 4(9):975–986, 2015. `doi:10.1021/sb500366v`.** Read-level:
`search-summary` (the ACS host is blocked).
**96 parts in 8 part types** — connectors left/right, promoter, CDS, terminator, yeast marker,
origin, bacterial marker — with subtypes (3a/3b); overhangs assigned per type; **97% of isolated
transformants correct for an optimised 10-part assembly**; the parts are characterised for
promoters, terminators, degradation tags and copy number.

| axis | YTK / MoClo |
|---|---|
| identifier | part **type number** (1–8) + the publication's/Addgene kit's own IDs; distributed as an Addgene kit |
| acceptance gate | the *paper*: a part exists because the authors made and measured it |
| physical material | yes, via Addgene kits |
| characterisation | **in the paper and its supplement** — a fixed panel measured the same way for every part in the set |

**Lesson, and it is the strongest positive in this note:** the toolkits are the only entries here
where characterisation is *complete and comparable across the set*, and they achieved that by being
**closed collections produced by one group with one protocol**, not open registries. Comparability
came from a fixed measurement panel, not from a schema. **INFERENCE:** an open library can only
approximate this by publishing the panel ("to claim promoter strength you report RPU vs this
reference, in this host, by this method") and refusing claims that do not use it.

### 4.5 SEVA — vector standardisation with a maintained erratum trail

**Silva-Rocha R, Martínez-García E, Calles B, Chavarría M, Arce-Rodríguez A, de las Heras A, et al.
"The Standard European Vector Architecture (SEVA): a coherent platform for the analysis and
deployment of complex prokaryotic phenotypes." Nucleic Acids Res 41(D1):D666, 2013.
`doi:10.1093/nar/gks1119`, PMC3531073.** Updates: **SEVA 2.0**, NAR 43(D1):D1183 (PMC4383931);
**SEVA 4.0**, NAR 51(D1):D1558, `doi:10.1093/nar/gkac1059` (PMC9825617). Read-level:
`search-summary` for all (PMC landing pages were not fetched individually; `seva-plasmids.com` and
`academic.oup.com` are blocked).

- **Identifier:** `pSEVA` + a positional digit code — **antibiotic marker, replication origin,
  cargo**, plus a fourth position for "gadgets" (lowercase Greek letters); letter suffixes denote
  variants (e.g. `pSEVA9C9E13α` = marker 9C, origin 9E, cargo 13, gadget α, per SEVA 4.0).
  Cargo variants use letters (GFP = 7, YFP = 7Y, CFP = 7C, DsRed2 = 7D, mCherry = 7R).
  Default `pSEVA111` = Ap marker, R6K origin, default polylinker.
- **Architecture as the standard:** three interchangeable modules separated by **fixed flanking
  elements** — two transcriptional terminators and an `oriT` conjugation origin — so any
  marker/origin/cargo combination is swappable by the same cuts.
- **Acceptance gate:** membership of the architecture; the collection is curated by its authors.
- **Physical material:** yes, distributed by the consortium (and via repositories).
- **Characterisation:** vector-level properties (host range, copy number, marker), not per-part
  performance envelopes.
- **The thing worth copying:** SEVA 2.0 explicitly **revised the nomenclature after user feedback
  and fixed DNA sequence errors** in the existing collection. A registry that publicly repairs its
  own sequence errors and versions its own naming scheme is behaving like an engineering standards
  body. That is the opposite of the iGEM pattern, where a wrong sequence sat next to a part record
  nobody owned.

### 4.6 FreeGenes and the Open MTA — the legal layer

**Kahl L et al. "Opening options for material transfer." Nat Biotechnol 36:923–927, 2018.
`doi:10.1038/nbt.4263`.** Read-level: `search-summary` (paywalled; authorship of the article
confirmed only indirectly — a 2018 press release names Linda Kahl as BioBricks Foundation senior
counsel. **I did not verify the full author list.**)

- **Terms (Unilateral OpenMTA, as posted for FreeGenes):** the recipient **may redistribute** the
  material, progeny, unmodified derivatives and modifications **without the provider's consent**;
  the provider **disclaims all rights of notification** of third-party transfer; the recipient has
  **no obligation to acknowledge** the provider; transfer is **free or at a cost-recovery
  transmittal fee only**; the recipient **must comply with applicable law including export control
  and safety**. (`search-summary` of the posted terms.)
- **Stated limits:** the OpenMTA is **not suited to materials in limited supply or under strict
  biosecurity regulation** (`search-summary` of the Nature Biotechnology piece).
- **FreeGenes practice:** BioBricks Foundation project; community-requested sequences synthesised
  (with Twist Bioscience), **screened for biosecurity**, distributed free under the OpenMTA via a
  Stanford order store and Addgene. The **current iGEM Distribution is manufactured and distributed
  by the FreeGenes Project, with all physical material under the Unilateral OpenMTA**
  (`search-summary`, `igem-distribution.readthedocs.io`).

**Lesson:** the OpenMTA is the piece of this ecosystem that most clearly *worked* — it is now the
default under the largest teaching distribution in the field. It worked because it removed
per-transfer negotiation entirely rather than standardising it. **For us: licence/transfer terms
belong in the record as a controlled field (the current iGEM record has exactly that — a `license`
field), and "no redistribution restrictions" should be a filterable property, not a PDF.**

### 4.7 Side-by-side

| registry | identifier | gate before acceptance | physical material | characterisation representation |
|---|---|---|---|---|
| iGEM Registry (legacy) | `BBa_` + category letter + range-allocated number | RFC 10 compliance (string check); Sanger QC, full confirmation only <1600 bp; **no functional claim by HQ** | yes (annual distribution) | prose sub-pages; no fields |
| iGEM Registry (current) | `uuid` + slug `bba-0000000001` | `status: draft→screening→published/rejected`; RFC10/12/21/23/25/1000 motif check | yes (via FreeGenes) | **no field exists** |
| Addgene | catalogue number | **full-plasmid NGS of every deposit**, aligned to depositor sequence, QC issues recorded | yes (core service) | by reference to publication |
| JBEI-ICE | UUID (+ part number) | none beyond a name and description | sample tracking, not distribution | attachments + `.ab1` traces |
| SynBioHub | SBOL IRI | valid SBOL | no | SBOL `Measure` + `ExperimentalData` |
| YTK / MoClo | part type (1–8) + kit ID | authored by the toolkit's creators | yes (Addgene kits) | **fixed panel, whole set, in the paper** |
| SEVA | `pSEVA` positional code | fits the architecture; curator-maintained, errors publicly fixed | yes | vector-level properties |
| FreeGenes | FreeGenes/Addgene ID | **biosecurity screen** + synthesisability | yes, free, OpenMTA | n/a (it is a distribution layer) |

---

## 5. What a spec sheet must contain for our case

Our artefacts are not only DNA parts: designed proteins and complexes, actuators, scaffolds,
mechanisms, mathematical models, and software components. So the schema has to be
**artefact-kind-polymorphic** on top of a common spine. Below, every field is tagged by where the
practice comes from: **[ME]** mechanical/electrical datasheet practice, **[BIO]** biology-specific,
**[REG]** learned from a registry's success or failure above, **[REPO]** this repository's existing
evidence discipline.

### 5.1 Spine (every artefact kind)

| field | notes | origin |
|---|---|---|
| `id` | opaque UUID; never semantic | [REG] Peccoud 2008's own recommendation; ICE; current iGEM |
| `slug` | human-citable, stable, not meaning-bearing | [REG] current iGEM |
| `kind` | one of: `dna_part`, `protein`, `complex`, `actuator`, `scaffold`, `mechanism`, `model`, `software` | — |
| `version` | content-addressed digest of the record | [REPO] SPEC-001 |
| `status` | `draft` → `screening` → `published` / `rejected` / `superseded` | [REG] current iGEM lifecycle |
| `title`, `description` | prose is allowed, but never load-bearing for a claim | — |
| `type`, `categories` | controlled vocabularies, hierarchical paths | [REG] iGEM `/parts/types`, `/parts/categories` |
| `license`, `transfer_terms` | controlled field; `openmta_unilateral` as a filterable value | [REG] §4.6 |
| `authors`, `audit` | who, when, what changed | [REG] iGEM `audit`; ICE |
| `provenance` | PROV-style activity/agent/plan for *every* claim | [REG] SBOL 3 |
| `structure` | sequence / composition / subcomponents / interface / constraints | [REG] SBOL 3 §3.1 |
| `identity_verification` | how we know it is what we say: sequencing method, coverage, assembly, mismatches **recorded not hidden** | [REG] Addgene QC, incl. "QC issue" and "partial sequence" states |
| `characterisation_state` | **explicit enum, required**: `uncharacterised`, `self-reported`, `single-lab`, `multi-lab`, `calibrated-multi-lab` | [REPO] / [REG] the field iGEM lacked |

`characterisation_state` is the one field I would fight for. "Uncharacterised" must be *sayable and
visible*, because the failure mode of every registry above is that the absence of data looks
identical to the presence of data in the catalogue UI.

### 5.2 The performance block — mechanical-engineering practice, imported deliberately

One or more `PerformanceClaim`s per artefact. **[ME]** throughout, with the biology-specific
conditions attached (§5.3).

| field | ME datasheet analogue | notes for biology |
|---|---|---|
| `quantity_kind` | the parameter name | controlled vocabulary per `kind`: promoter activity, fold-change, Kd, kcat/KM, Tm, expression level, force, stiffness, stroke, duty cycle, latency, throughput |
| `nominal` | typical value | with unit; for us usually a geometric mean |
| `min` / `max` | min/max over the spec'd range | — |
| `tolerance` / `uncertainty` | tolerance | **report as a factor, not ±%**, and say whether it is within-lab or between-lab — §2.2's ~1.8–2.4× between-lab floor is the honest default |
| `n`, `replicate_structure` | — | biological vs technical replicates stated separately |
| `operating_envelope` | recommended operating conditions | per-dimension ranges over the condition set (§5.3) |
| `absolute_maximum_rating` | absolute maximum rating | the condition beyond which the artefact is damaged/irrecoverable — e.g. inducer concentration causing growth arrest, temperature causing irreversible unfolding |
| `derating` | derating curve | how the nominal degrades across a condition axis (temperature, copy number, growth rate, load); a sampled table + optional model reference |
| `failure_boundary` | — (ME's "limiting conditions") | a predicate over conditions where the function stops, **with the observed failure mode**: loss of function, toxicity, mutational escape, aggregation, plasmid loss, oscillation |
| `lifetime` / `stability` | MTBF, cycle life | **[BIO]** genetic stability over N generations; performance stability over time; proteolytic half-life |
| `test_conditions` | "test conditions" header | → mandatory `ConditionSet` reference (§5.3) |
| `test_method` | test circuit / method | instrument, protocol ID, calibration standard, analysis code version |
| `evidence` | — | content-hashed raw data + analysis artefact; **a claim with an unresolvable hash is invalid** |
| `claim_level` | — | **[REPO]** `VERIFIED` (a named test/experiment exercises it) vs `ASSUMED` (read from a source) — the repo's existing discipline, applied to parts |

### 5.3 `ConditionSet` — the biology-specific block, and it is mandatory

A performance claim without a condition set is rejected at the door. **[BIO]** unless noted.

`host_organism` and `strain` · `genetic_background` (knockouts, auxotrophies, competing circuits) ·
`chromosomal_integration_locus` or `plasmid_backbone` + `copy_number` ·
`expression_level` and how it was set (promoter/RBS/induction) and *measured* ·
`growth_medium`, `carbon_source`, `temperature`, `pH`, `aeration`, `osmolarity` ·
`growth_phase` / OD at measurement · `induction` (inducer identity + `Measure` + timing) ·
`measurement_method` (instrument, gain, filters, flow rate) ·
`calibration_standard` — e.g. RPU vs `BBa_J23101`, microsphere/FITC-calibrated fluorescence,
CFU-calibrated OD (**[REG]** §2.2: this is the single highest-leverage field in the whole schema,
because it is the only one with a measured effect size — ~50% variance reduction) ·
`cell_free_vs_in_vivo` · `date`, `operator`, `lab` (**[ME]**: datasheets name the test house).

For non-cellular artefacts the same slot takes the matching context: for a **protein**, buffer,
ionic strength, reducing agent, concentration, oligomeric state, tag and its position; for a
**mechanism/actuator**, load, medium viscosity, temperature, duty cycle, substrate;
for a **model**, the parameter set, solver, tolerances, and validity domain;
for a **software component**, platform, version pins, input distribution, hardware.

### 5.4 Which fields are ME imports and which are biology's own — stated plainly

- **Straight imports from ME/EE datasheet practice, unchanged in meaning:** nominal value,
  tolerance, min/typ/max, test conditions, test method, operating envelope, absolute maximum rating,
  derating curve, lifetime/cycle life, and the convention that the *test setup is part of the spec*.
- **Imports that need redefinition for biology:** tolerance becomes multiplicative, not additive;
  "absolute maximum rating" has to cover *evolutionary* failure (mutational escape, plasmid loss) as
  well as physical damage; "lifetime" splits into genetic stability and performance stability;
  "bin/grade" (ME's answer to process spread) maps onto strain/clone-to-clone variation, which
  biology usually hides in an error bar.
- **Genuinely biology-specific, with no ME analogue:** host context, genetic background, copy number,
  expression level, growth conditions and phase, calibration-to-a-living-reference (RPU),
  context-dependence of composition (two characterised parts need not compose), and biosecurity
  screening state.
- **INFERENCE about the hardest one:** ME datasheets can omit the test house because the artefact's
  behaviour is substrate-independent to a good approximation. Biology's equivalent assumption is
  false, and the measured residual is the ~1.8–2.4× between-lab spread of §2.2. Therefore
  **`calibration_standard` and `lab` are not metadata in our schema; they are part of the value.**

### 5.5 Gates I would enforce at submission (and not later)

Each is mechanically checkable, which is the entire lesson of §1.5.

1. Identity verification present, with method and coverage — or `characterisation_state:
   uncharacterised` and no performance claims permitted.
2. Every `PerformanceClaim` has a `ConditionSet`, a `quantity_kind` from the vocabulary, a unit, an
   `n`, and an uncertainty expressed as a factor.
3. Every claim cites content-hashed evidence that resolves.
4. Every claim carries `VERIFIED`/`ASSUMED`.
5. Licence/transfer terms from a controlled enum.
6. Assembly/format compliance checked **but never a condition of archiving** — record
   non-compliance as a property (§1.4d: 36% of submitters walked away over this).
7. No governance claim the registry cannot back: we never publish "works", only "measured under
   these conditions, by these people, with this evidence".

---

## 6. MCP servers and public APIs for biological part data

**Blanket caveat:** every endpoint below was *read from documentation, a paper, or client source
code*. **I could not reach any of these services from this session** (see the egress list at the
top), so **no endpoint here is verified live.** I state paths exactly as the sources give them and
flag anything I did not see in a primary artefact.

### 6.1 Per-registry

**iGEM Registry — a REST API, no MCP server found.**
- Base URLs, from the client source (`full-text`, `igem_registry_api/client.py`):
  `https://api.registry.igem.org/v1` and `https://api.igem.org/v1`.
- Endpoints the client calls (`full-text`): `GET /health`, `GET /parts`, `GET /parts/{uuid}`,
  `GET /parts/slugs/{slug}`, `GET /parts/types`, `GET /parts/types/{uuid}`,
  `GET /parts/categories`, `GET /parts/categories/{uuid}`, `GET /parts/accounts/{uuid}`,
  `GET /parts/{uuid}/authors`, `/composition`, `/sequence-features`, `/twins`, `/uses`,
  `GET /licenses`, `/licenses/{uuid}`, `GET /organisations`, `/organisations/{uuid}`,
  `/organisations/{uuid}/members`, `GET /accounts/{uuid}/affiliations`,
  `POST /accounts/opt-in|opt-out`, `GET /auth/me`, `/auth/sign-in`, `/auth/sign-out`,
  `/auth/oauth/default/login`.
- The official docs are reported to be a Swagger listing without schemas or field definitions, which
  is why this client exists (`search-summary`).
- Legacy endpoints `parts.igem.org/xml/…` and `parts.igem.org/fasta/parts/BBa_C0040` are described in
  older guidance (`search-summary`) — **unverified, and the legacy site is read-only.**
- **MCP: none found.** I searched; nothing surfaced.

**Addgene — an approval-gated official API, an official MCP connector, and a community MCP server.**
- **Official MCP connector exists.** Verified directly against this client's connector directory
  (`full-text` of the tool result): an **"Addgene"** connector, "Search Addgene's catalog of plasmids
  and viral preps", with tools `list_plasmids`, `get_plasmid`, `list_viral_preps`, `get_viral_prep`,
  `get_genbank_url`. Not installed in this session, and requires auth (`isAuthless: false`).
  **This is the one unambiguous MCP answer in the whole question.** (Whether Addgene itself operates
  it, or a partner does, I could not determine.)
- **Official HTTP API:** `developers.addgene.org`, read-only, per-scope access request + data-access
  licence; plasmids and viral preps now, more types planned late 2026; daily bulk JSON
  (`search-summary`).
- **Community MCP server:** `addgene-mcp` **0.1.3** on PyPI (verified live on PyPI; source read,
  `full-text`). Its tools are `search_plasmids`, `get_sequence_info`, `get_popular_plasmids`,
  `download_sequence`, `get_api_info`. **It is a Scrapy scraper**, not an API client — it fetches
  `https://www.addgene.org/search/catalog/plasmids/` and
  `https://www.addgene.org/{plasmid_id}/sequences/`. Given that Addgene added a login requirement
  for sequence viewing explicitly because of at-scale scraping (§4.1), **I would treat this server as
  likely broken and, more importantly, as the wrong thing to depend on.**
- There is also an unofficial REST wrapper (`github.com/moltinginstar/addgene-api`, last update
  reported Feb 2024) — `search-summary`.

**SynBioHub — public API, no MCP server found.**
Documented at `synbiohub.github.io/api-docs` (`search-summary`): `search` with `key=value` +
`offset`/`limit`, Search Similar, Search Uses, sequence search (`Accept: text/plain`,
`X-authorization`), `GET /sparql?query=…`, `/admin/sparql`, and a submission-endpoint section I could
not retrieve. **No MCP server found.** A SPARQL endpoint is, in practice, the easiest thing in this
list to wrap ourselves.

**biobricks.ai — not what the name suggests, and no MCP.**
**Gao Y, Mughal Z, … Hartung T, Luechtefeld T. "BioBricks.ai: A Versioned Data Registry for Life
Sciences Data Assets", arXiv:2408.17320 (2024-08-30), PMC11383443; a peer-reviewed version is noted
in Frontiers in Artificial Intelligence.** Read-level: `extracted` (full text via PMC).
It is **unrelated to the BioBricks Foundation and to DNA parts** — "BioBricks is a product developed
by Insilica LLC". It is a *data* package manager: **>90 biological and chemical datasets** ("bricks"
— ChEMBL, PubChem, Tox21, ClinVar, HGNC, …) delivered as Parquet/SQLite/HDT, each brick a
**DVC git repository** stored as `./{org}/{repo}/{commit-hash}` with a **content-MD5 cache**; CLI
`biobricks install|assets|init|pull|add`, Python `bb.assets('hgnc')`, token-gated downloads, MIT
licence. **The paper does not mention MCP or LLM agents.** The name collision is worth recording so
we never cite it as a parts registry.

### 6.2 The biological MCP landscape, as far as I can verify it

- **BioContextAI** — the strongest lead, and it checks out. A **registry of biomedical MCP servers**
  (`github.com/biocontext-ai/registry`, indexed with Schema.org, with a web interface) plus a
  reference server, **Knowledgebase MCP** (`github.com/biocontext-ai/knowledgebase-mcp`). I verified
  the package on PyPI directly: **`biocontext_kb` 0.2.1**, "A knowledgebase MCP server for biomedical
  research, part of the BioContextAI project" (`full-text` of the PyPI metadata). Reported wrapped
  resources: STRING, KEGG, PanglaoDB, Human Protein Atlas, Reactome, Open Targets, EuropePMC,
  UniProtKB, the Antibody Registry, Grants.gov, ClinicalTrials.gov, Drugs@openFDA
  (`search-summary`). Papers: preprint `doi:10.1101/2025.07.21.665729` (bioRxiv, 2025-07);
  "BioContextAI is a community hub for agentic biomedical systems", Nat Biotechnol 43:1755–1757
  (2025) (`search-summary`/`listing`). **Note the gap: no synthetic-biology parts registry is in
  that resource list.**
- **MCPmed** — **Flotho M, Diks IF, Flotho P, Molano LAG, Hirsch P, Keller A. "MCPmed: a call for
  Model Context Protocol-enabled bioinformatics web services for LLM-driven discovery."
  Briefings in Bioinformatics 27(1):bbag076, 2026. `doi:10.1093/bib/bbag076`, PMC12927880.**
  Read-level: `extracted` (full text via PMC). It names the existing servers it knows of —
  **GEOmcp** (NCBI GEO), **STRING MCP**, **UCSC Cell Browser MCP**, **PLSDB MCP** (a plasmid
  database) — plus scmcphub as related work; proposes a hub + cookiecutter template, HTML-embedded
  JSON "breadcrumbs" for services without native MCP, a curated registry with security review, and
  alignment to Schema.org / Bioschemas / EDAM. **It does not mention SynBioHub, Addgene, iGEM or
  synthetic-biology registries at all** — I asked explicitly and the answer was no.
- Other things that exist by name but which I did **not** verify beyond a listing: `bio-mcp`
  (GitHub org), `biothings-mcp` (PyPI), BioMCP, and an aggregator listing ~21 bioinformatics MCP
  servers on `mcp.so` (`listing`/`search-summary`).

### 6.3 Plainly: what I could not verify

- Whether **any** of the endpoints in §6.1 currently respond, including the Addgene official API, the
  iGEM REST base URLs, and the SynBioHub SPARQL endpoint. All blocked from this session.
- Whether the **Addgene MCP connector** is operated by Addgene or by a third party, and what its
  auth model is.
- The **iGEM Registry's official API documentation** — I never saw it, only a report that it is thin.
- The **SBOL 3 specification text** (§6 of the spec, validation rules, and whether the prose
  *forbids* rather than merely *omits* the things I list as gaps in §3.2). The PDF download was
  blocked and `sbolstandard.org` is unreachable.
- **Vilanova & Porcar's actual working/non-working proportions** (§1.4e).
- The **Canton 2008 article body**, so: the datasheet's real section headings, and whether it
  specified anything resembling a field schema.
- Addgene's **complete current QC criteria list** and its structured field set, beyond the help-centre
  statements quoted.
- The **YTK part-type 1–8 definitions and overhang sequences** (Supporting Information, blocked), and
  **MoClo's fusion-site standard** in detail.
- Whether **RFC 95** was ever used by anyone; absence from the current Registry client's enum is
  suggestive, not proof.

---

## 7. What to copy, what to refuse

**Copy**
1. Addgene's gate: one mechanical check applied to 100% of submissions, with failures *recorded as
   states* (`QC issue`, `partial sequence`) rather than hidden.
2. The toolkit pattern: a published **measurement panel** per artefact kind, so claims are
   comparable by construction rather than by hope.
3. RPU's lesson: **relative to a named reference** beats absolute, and shipping the kit matters more
   than publishing the unit.
4. SEVA's maintenance culture: version the naming scheme, publish the errata, fix the sequences.
5. SBOL's structural model (hierarchy, interface, constraints, PROV) and content-hashed attachments —
   adopt them rather than reinventing, and extend only the quantitative layer (§3.3).
6. OpenMTA as a **controlled field value**, so "freely redistributable" is filterable.
7. UUID identity + non-semantic slug, from day one (Peccoud 2008 asked for this in 2008).

**Refuse**
1. A record that can hold a performance claim only as prose. If there is no field, there is no claim.
2. A `published` state that reads as a quality signal while the governing body disclaims any
   functional judgement. Either gate it or label it `uncharacterised`.
3. A submission standard that silently *excludes* material (36% walked away from RFC 10). Check
   compliance; record it; never make it the condition of archiving.
4. Attachments-as-characterisation (ICE's honest limit): a blob store is an audit trail, not data.
5. A nominal value without its conditions and its calibration standard — given a ~2× between-lab
   floor, that number is not a specification, it is an anecdote.
6. Scraping as an integration strategy (`addgene-mcp`): it breaks, and it is the reason Addgene put
   sequences behind a login.

## 8. Source list with read-levels

| source | read-level |
|---|---|
| Canton, Labno & Endy 2008, Nat Biotechnol 26(7):787–793, `10.1038/nbt1413` | abstract (full abstract via E-utilities); body could-not-access |
| Nat Biotechnol 26(7):771–774 (comment on the above) | listing |
| Kelly et al. 2009, J Biol Eng 3:4, `10.1186/1754-1611-3-4`, PMC2683166 | full-text of structured abstract; body extracted/search-summary |
| Peccoud et al. 2008, PLoS ONE 3(7):e2671, PMC2441434 | extracted (full text via PMC) |
| Alnahhas et al. 2014, J Biol Eng 8:28, PMC4269934 | extracted (full text via PMC) |
| Kwok 2010, Nature 463:288–290, `10.1038/463288a` | search-summary (paywalled) |
| Vilanova & Porcar 2014, Nat Biotechnol 32:420–424, `10.1038/nbt.2899` | listing + figure-legend search-summary; numbers **could-not-access** |
| SBOL 3.1.0 spec, J Integr Bioinform 20(1), `10.1515/jib-2022-0058`, PMC10063177 | abstract; PDF could-not-access |
| SBOL 3.0.0 spec, PMC7756618; SBOL Visual 3.0, PMC8560346 | listing |
| **pySBOL3 1.2.0** (`sbol3` on PyPI, SynBioDex) — class/property extraction in §3 | **full-text of source** |
| **igem-registry-api 0.1.0** (PyPI) — endpoints, part fields, status enum, RFC motif table | **full-text of source** |
| **addgene-mcp 0.1.3** (PyPI) — tool names, scraping targets | **full-text of source** |
| **biocontext_kb 0.2.1** (PyPI metadata) | **full-text** |
| Claude connector directory — "Addgene" MCP connector and its five tools | full-text of tool result |
| Ham et al. 2012, Nucleic Acids Res 40(18):e141, PMC3467034 | extracted (full text via PMC) |
| McLaughlin et al. 2018, ACS Synth Biol 7(2):682–688, PMID 29316788 | full-text of abstract; API surface search-summary |
| Lee et al. 2015, ACS Synth Biol 4(9):975–986, `10.1021/sb500366v` | search-summary |
| Weber et al. 2011, PLoS ONE 6(2):e16765 | search-summary |
| SEVA 2013 NAR 41:D666 `10.1093/nar/gks1119`; SEVA 2.0 NAR 43:D1183; SEVA 4.0 NAR 51:D1558 `10.1093/nar/gkac1059` | search-summary |
| Kahl et al. 2018, Nat Biotechnol, `10.1038/nbt.4263`; Unilateral OpenMTA posted terms | search-summary (author list unverified) |
| Flotho et al. 2026, Brief Bioinform 27(1):bbag076, `10.1093/bib/bbag076`, PMC12927880 | extracted (full text via PMC) |
| BioContextAI preprint `10.1101/2025.07.21.665729`; Nat Biotechnol 43:1755–1757 (2025) | search-summary / listing |
| Gao et al. 2024, BioBricks.ai, arXiv:2408.17320, PMC11383443 | extracted (full text via PMC) |
| iGEM Registry help pages (FAQ, Quality Control, Part Names, Prefix/Suffix, API Guidelines, documentation help) | search-summary — host blocked throughout |
| Addgene help centre + blog QC articles | search-summary — host blocked |
| SynBioHub API docs (`synbiohub.github.io/api-docs`) | search-summary |
| iGEM interlab comparative analysis, PLoS ONE 2021 `10.1371/journal.pone.0252263`; Beal et al. 2018 PMC6013168; OD→cell count PMC7499192 | search-summary / listing |
| Siyari, Dilkina & Dovrolis 2019, arXiv:1906.02446 (iGEM sequence reuse) | abstract — reuse findings qualitative only, no usable numbers |
