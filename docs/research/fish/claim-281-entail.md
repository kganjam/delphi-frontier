# Claim 281 — entailment at the protein scale

**Source claim** (scale `dna`, recorded evidence `derived`):

> MECHANISTICALLY THIS IS ENLARGER PLUS SUPPRESSOR, not uniform enlargement. That is why the
> published result is about fin PROPORTIONS rather than fin size, and it means the design lever is
> differential allometry across fins rather than growth of one fin.

**Adjacent scale propagated to:** `protein`.

**Headline.** Four of five requirements survive contact with the literature; three are satisfied by
named, measured mechanisms. The one that fails is the one the claim's own conclusion rests on: the
claim says the design lever is *differential* allometry across fins, and at the protein scale
**nothing measured supplies the differential**. Both effectors' transcript levels are reported as
not differing significantly between pectoral and dorsal fins, and the only protein-level functional
assay of the suppressor variant produces a *uniform* growth decrease with no fin-type dependence.
That is `unsatisfied`, not `unsatisfiable`: the numbers that would contradict the requirement sit in
figure panels and a supplementary table I could not access, so no measured value can be quoted
against it. Scope of that negative is stated in full in §C4.

---

## Sources and read-levels

| # | Source | Read-level | Scope of what I actually got |
|---|---|---|---|
| S1 | Daane, Blum, Lanni, Boldt, Iovine, Higdon, Johnson, Lovejoy, Harris (2021), *Modulation of bioelectric cues in the evolution of flying fishes*, **Curr Biol** 31(22):5052–5061.e8, doi `10.1016/j.cub.2021.08.054`, PMC9172250 | **full-text**, characters 0–100,000 of the PMC author manuscript | Main text and Methods prose. Figure panels and Table S1 **could-not-access**. Final 49,104 characters not read. |
| S2 | Stewart et al., *longfin* / `kcnh2a` study, PMC8217709 (2021). Journal name `unknown` — I did not retrieve the citation block | **full-text**, characters 0–100,000 | Results, drug windows, chimera counts. Final 19,574 characters not read. |
| S3 | *Comparative Genomic Screening Identifies Developmental Constraint Loci Underscoring the Phenotypic Evolution of Syngnathids*, PMC13574186. Authors and year `unknown` — not retrieved | **full-text**, characters 0–100,000 | Section 2.10 and 3.2, Fig. 2D legend. Final 51,000 characters not read. |
| S4 | Taslimifar et al. (2017), *Sci Rep*, model-input table of leucine-transporter kinetics (`srep40628`) | **search-summary** | Numbers only via a search summariser that **self-flagged garbled column alignment**. Not used as a bound. See §C5. |
| S5 | Takayama et al. (2018), leucine/glutamine–mTORC1 in position-dependent regeneration, PMC5974189 | **search-summary** | One finding only. Paper not opened. |
| S6 | Mouse *Slc43a2*/LAT4 knockout and tissue-specific deletion papers (PMC7693055 and a ResearchGate listing) | **listing** / **search-summary** | Phenotype summary only. Not opened. |
| S7 | Kcnk5b/calcineurin allometry work (*Sci Rep* 2018, PMID 29991812; *PLoS Genet* 2014; PNAS 2021 `10.1073/pnas.2009539118`) | **search-summary** | Used only to scope the §C4 negative. |
| S8 | Five web searches, listed verbatim in §C4 and §C5 | **search-summary** | Result lists; conclusions drawn only about absence. |

**Caveat that applies to every quotation from S1, S2 and S3.** I read those three through a fetch
tool that passes the page through a summarising model. The quoted strings are what that tool
returned as verbatim. They should be re-checked against the PDFs before being cited downstream.

**Presupposition, checked and satisfied, carried by the claim's word "enlarger."** S2 reports
`kcnh2a` elevated **+25.8-fold** by RNA-seq in 4-dpa caudal-fin regenerates of *longfin*^t2^/+
relative to wild-type clutchmates, below detection by RT-qPCR in wild type, and calls *lof*^t2^ "a
regulatory neomorph allele of *kcnh2a*" whose lesion is "likely a chromosomal inversion linking
kcnh2a to a displaced enhancer" — which S2 itself marks as a hypothesis. S2 also reports that
`kcnh2a` mutant fins are "indistinguishable from wild-type," i.e. endogenous Kcnh2a does not set
normal fin length. Read-level full-text. So the enlarger is a **dosage/ectopic-expression** allele,
not an altered-protein allele. Note on nomenclature, because it is a trap: "lof" here is the
*longfin* **locus name**, not "loss of function," and the `Y418X` alleles S1 lists are *in-cis
revertants*. The two papers agree on mechanism direction; they do not disagree.

---

## The constraints

### C1 — `existence`. The suppressor must act through an altered protein activity, not through less protein.

*Requirement, generically stated.* If the medial-fin arm of the phenotype is **suppression** rather
than absence of enlargement, then there must exist a protein whose *activity is qualitatively
changed* in the suppressor genotype. A reduction in that protein's abundance or gene dose must not
be sufficient to produce the suppression — otherwise the mechanism is dosage, not an enlarger-plus-
suppressor pair, and the claim's mechanistic distinction collapses.

**Status: `satisfied`.** By Lat4a, an L-type amino-acid transporter, carrying the `nr21` (T200K)
substitution. Three independent measured facts, all from S1 at full-text, meet the requirement:

- "We identified a dominant mutant, *nr21*, as having small adult fins compared to wild-type
  siblings," and "*nr21* is dominant and without an obvious homozygous phenotype."
- "zebrafish lacking *lat4a* have no fin phenotype." (S1 does not state the zygosity tested for the
  deletion allele `mh152`; that detail is `unknown`.) **This is the load-bearing datum**: removing
  the protein does nothing, so the suppression cannot be a dosage effect.
- An induced in-cis frameshift (`L106Rfs39`) reverts the fin phenotype: "These induced mutations
  resulted in reversion of *nr21* to a wild-type fin phenotype, indicating that the mutation in
  *lat4a*^nr21^ results from a gain-of-function effect." The gain-of-function reading is **the
  authors' inference from reversion**, not a protein assay; S1 does not show that the frameshift
  produces a null protein.
- Consistent, independent, and at the protein level: S3 §2.10/3.2 transfected HEK293T cells with
  empty plasmid, human *SLC43A2* WT, F326L or T200K, counted cells daily for three days from 48 h
  post-transfection, and report "Overexpression of F326L and T200K LAT4 (SLC43A2) led to decreased
  growth of 293T cells in vitro," significant at day 2 for T200K and day 3 for both, one-way ANOVA,
  `** p < 0.01`. **S3 reports no n, no percentage and no fold-change**, and S3's own text says "the
  precise molecular mechanism underlying this effect requires further investigation" while its
  abstract claims the in-vitro work "confirm[s]" the role. I preserve that internal disagreement
  rather than picking a side.

**What is still missing, and I am not counting it as satisfied.** No transport measurement exists for
this protein in any system. S1: no uptake, substrate, Km, oocyte or cell transport assay for
wild-type or T200K Lat4a — absent from the text I read. S3: "Amino acid uptake/transport: Not
measured." A targeted search (§C5) found no published uptake assay in zebrafish *lat4a*/*slc43a2*
mutants. So **the direction of the activity change is `unknown`**: "gain-of-function" here means
"the phenotype requires the ORF," not "transport is increased." Anyone designing on this lever
should treat the biochemistry as unmeasured.

### C2 — `timescale`. The enlarger's protein activity must be required during growth *termination*, slowly relative to channel gating and late relative to the proliferative phase.

*Requirement.* "Not uniform enlargement" implies the effector does not simply raise growth rate from
the start; it must act on the decision to *stop*. So the window in which the protein's activity is
required must be late within an outgrowth episode, and must be long compared with the protein's own
gating kinetics — otherwise the lever is kinetic, not a sustained set-point, and cannot be tuned by
an allele.

**Bounded quantity:** required-activity window, **6–30 days post-amputation** out of a ~30-day
regenerative outgrowth.

**Status: `satisfied`, in the regenerating caudal fin.** From S2, read-level full-text, all measured:

- Astemizole (an ether-à-go-go channel blocker) at **500 nM**, water changed every 48 h, applied
  **7–30 dpa**, "fully suppresses *loft2*/+ overgrowth to wild-type levels (P<0.0001)."
- "Starting astemizole at 6 dpa was as effective as treating throughout regeneration."
- Early `kcnh2a` expression at 4 dpa "had negligible functional impact."
- S2's conclusion, their words: ectopic Kcnh2a "exclusively causes regenerative fin overgrowth by
  actively preventing growth termination," from about 7 dpa onward.
- Companion timing on the pathway, same paper: calcineurin inhibition (FK506, 500 nM, 4 h daily)
  from 1–5 dpa had no effect; 6–21 dpa or 1–21 dpa gave the same pronounced overgrowth. FK506 did
  not further enhance *loft2* overgrowth, and still overgrew astemizole-treated *loft2*/+ fins;
  S2 concludes Kcnh2a "is not downstream of calcineurin" and "likely disrupts calcineurin
  signaling," placing it upstream or downstream — S2 explicitly leaves that open.

**My inference, separated from the authors' claim:** a ≥6-day requirement window against
millisecond-scale K⁺-channel gating is a ratio of order 10⁸, so the lever is the channel's
**time-averaged activity level**, not its kinetics. That ratio is my arithmetic from the two
timescales, **derived, not measured.**

**Scope limit that keeps this from being a stronger result than it is.** Every number above is from
**regenerating caudal fin** in the single *longfin* heterozygote. The claim 281 phenotype is
**ontogenetic growth of paired fins in the double heterozygote.** No equivalent window has been
measured there, as far as the text I read shows. The transfer is an assumption.

### C3 — `spatial`. The length scale at which the growth decision is made must match a single fin or a single ray, not the animal.

*Requirement.* Differential allometry *across fins* requires that the growth set-point be settable
independently per fin. So the effector must act at a length scale no larger than one fin field —
and if the claim's "differential across fins" is to be a design lever at all, the decision must not
be systemic (endocrine, whole-animal). Fin and ray widths in an adult zebrafish are of order
10² µm to a few mm, so the requirement is: determination length scale ≲ 1 mm, within a factor of a
few.

**Status: `satisfied`, for the enlarger.** From S2, measured:

- Blastula transplants of EGFP⁺ *loft2*/+ cells into wild-type hosts gave overgrown chimeric fins
  in **39 fins from 28 of 214 chimeras (13%)**. "All overgrown chimeric rays contained EGFP⁺
  intra-ray mesenchyme. Thirty overgrown fins contained only EGFP⁺ mesenchyme." Chimeras with only
  EGFP⁺ epidermis were of normal length (**n = 3** — a very small negative control).
- Mosaic F0 CRISPR knockouts gave "partial, regionalized overgrowth" in **17 of 78 fish (21.8%)**,
  which S2 reads as fin-autonomous rather than systemic action.
- RNAscope put `kcnh2a` in Msx⁺ or *tph1b:mCherry*⁺ proximal regenerating intra-ray cells, lower in
  distal blastema.
- Qualitatively, "a few crispant and chimeric animals showed asymmetrically sized pectoral fins,
  with one fin near wild-type length and the contralateral fin overgrown." **No numbers are given**
  for those cases, so the left–right asymmetry is an observation without an effect size.

The decision is therefore made at or below ray scale, which satisfies the spatial requirement with
room to spare. **Scope:** `kcnh2a` only, caudal and pectoral fins. No equivalent mosaic or chimeric
experiment for Lat4a appeared in the text I read.

### C4 — `existence`. A fin-type-differential component must exist, and it cannot be the abundance of either effector.

*Requirement.* This is the claim's own conclusion turned into a protein-scale demand. If the same two
protein activities are present in paired and medial fins, yet paired fins overgrow while medial fins
stay at wild-type size, then **something at the protein scale must differ between fin fields** —
either a differential abundance of one of the two effectors, or a third fin-type-specific component
that changes the sign of the readout. One of those two must exist, or there is no mechanism for
"differential allometry across fins."

**Status: `unsatisfied`.**

The first branch — differential abundance — is reported as absent. From S1, read-level full-text for
the prose, **could-not-access for the panels**:

- `kcnh2a` "expression does not vary significantly in pectoral or dorsal fins containing the *nr21*
  mutation" (qRT-PCR, pectoral vs dorsal compared; Fig. 4D also notes `kcnh2a` was "not detected
  (n.d.) in wild-type fins").
- `lat4a`: "no significant difference in *lat4a* expression across fins and genotypes" (Fig. 4E
  legend).
- No baseline comparison of either gene between paired and medial fins in the absence of the
  mutations is reported. Pelvic and anal fins are not assayed for expression at all.

The second branch — a third, fin-type-specific component — I searched for and did not find. **Scope
of the negative, stated so it can be audited:** three web searches, read-level search-summary:
(i) "fin-type specific growth modifier zebrafish paired versus median fin positional identity
differential allometry kcnk5b tbx5 hoxd13"; (ii) `"dorsal" "anal" fin versus pectoral fin
differential response calcineurin FK506 longfin overgrowth fin-type specific suppression zebrafish`;
(iii) the *lat4a* allele search in §C1. What those returned, and why none of it meets the
requirement:

- Kcnk5b/calcineurin (S7) is the nearest body of work. Its own conclusion is that FK506 "do[es] not
  re-specify positional memory in the fin, but rather act[s] to maintain heightened rate of growth,"
  i.e. this pathway is explicitly reported as *not* a positional/identity input. Mutant Kcnk5b acts
  locally in fin and barbel mesenchyme. Experiments are on pectoral and caudal fins.
- The PNAS calcineurin-polarity paper notes proximal-column-type regeneration "also occurred" in
  anal and dorsal fins after FK506, but does not measure whether that response differs from
  pectoral. Read-level search-summary.
- A 2024 study (PMC11664171, search-summary) reports a real developmental difference between the fin
  classes — dorsal and anal fin skeletons derive from sclerotome/paraxial mesoderm rather than
  carrying significant neural-crest contribution. **My inference, not the authors':** that is a
  plausible *origin* for a fin-type difference, but it is a lineage fact, not a measured protein-
  level modulator of the Kcnh2a/Lat4a axis, and I am not going to score a plausible candidate as a
  satisfied constraint.

This is the distinction the brief insists on, so I state it explicitly: **for branch one, people
looked and reported no difference; for branch two, nobody appears to have looked.** They must not be
merged.

**Why this is `unsatisfied` and not `unsatisfiable`.** To call it unsatisfiable I would need a
measured number contradicting the requirement — an expression ratio between fin types with a
confidence interval tight enough to exclude a biologically sufficient difference. "Does not vary
significantly" is not that number: the effect sizes live in Fig. 4D/4E panels and Table S1, both
**could-not-access** (PMC author manuscript omits panels and supplements; see S1 row). A
non-significant qRT-PCR comparison with unknown n and unknown variance cannot refute anything. I
record the requirement as unmet, not as contradicted.

**The sharpest counter-datum available, flagged as such.** The only protein-level functional assay of
the suppressor variant anywhere (S3, HEK293T, §C1) yields a **uniform** proliferation decrease.
HEK293T cells have no fin identity, so this cannot refute the requirement — but it does mean that
the entire protein-scale evidence base for the suppressor currently exhibits *no* fin-type
differentiality whatsoever. **My inference:** claim 281's assertion that "the design lever is
differential allometry across fins" is, at the protein scale, a statement about a mechanism that has
not been identified. The genetic phenotype is real; the protein-level source of its differentiality
is unknown. Any design that proposes to tune fins independently is tuning a parameter nobody has
located.

### C5 — `conservation`. Essential neutral amino-acid influx must still balance the biosynthetic demand of the *faster*-growing paired fins.

*Requirement.* The suppressor is a transporter for essential neutral amino acids (S1, citing
mammalian work: "Mammalian Lat4 shuttles isoleucine, leucine, methionine, and phenylalanine into the
cell"). In the double heterozygote, paired fins grow *more* than wild type while the suppressor
variant is present throughout. Mass balance therefore demands that net essential-AA influx into
paired-fin mesenchyme remain at or above the rate consumed by protein synthesis in that tissue. If
the variant acted by reducing substrate supply below demand, the outcome would be tissue-wide
wasting, not a proportion change — so there is a floor on influx that the mechanism must respect.

**Bounded quantity:** net essential neutral amino-acid influx per unit growing fin mass, relative to
the tissue's protein-synthesis demand. Ratio must be ≥ 1. **Absolute lo/hi: `unknown`** — I have no
measured value for either side of the inequality.

**Status: `open`.** Nothing I found measures either term in the relevant tissue. Scope of the search,
read-level search-summary throughout:

- "Lat4a zebrafish amino acid transporter fin growth transport assay slc43a2 mutant uptake" — no
  published uptake assay in zebrafish *slc43a2*/*lat4a* mutants.
- "zebrafish fin regeneration blastema amino acid flux leucine mTORC1 requirement protein synthesis
  rate measurement" — no isotope-tracer amino-acid flux and no measured protein-synthesis rate in
  the blastema. Nearest results: S5 (Takayama et al. 2018) reports that leucine or glutamine
  *individually* did not activate mTORC1 during fin regeneration while the two together did — which
  bears on whether a single-substrate transporter can be rate-limiting, and cuts *against* a naive
  leucine-supply model; and an IGFR/mTOR paper reporting elevated global translation in blastema
  cells, method not seen. Not pursued: puromycin/SUnSET or OPP labelling searches, which is the
  obvious next move.
- Whole-animal mammalian anchor only, S6: *Slc43a2* knockout mice show growth restriction, postnatal
  malnutrition and early death. That is organismal, not fin-tissue, and the zebrafish *lat4a*
  deletion has no fin phenotype (§C1), so the mouse null does not transfer.

I am recording this `open` rather than `unsatisfied` because my search was two queries deep and
aimed at transport assays, not at the fin bioenergetics literature. The honest statement is: the
mass-balance requirement is checkable in principle from a tracer experiment, and as far as I looked,
the experiment has not been done in this tissue.

---

## What a reader should take from this

1. The mechanistic half of claim 281 — enlarger plus suppressor, acting by different protein-level
   routes — is **supported**, and more specifically than the claim states it: the enlarger is a
   +25.8-fold ectopic-expression neomorph of a channel that is dispensable at endogenous levels
   (C2 presupposition), the suppressor is an altered-activity transporter variant whose null has no
   fin phenotype (C1), the activity is required in the late termination window (C2), and the
   decision is made at ray scale (C3). Read-levels: full-text for all four.
2. The design half — "the design lever is differential allometry across fins" — is **not supported
   at the protein scale** (C4). No measured protein-level quantity differs between fin types in
   either effector, no third differentiating component has been identified, and the sole protein-
   level functional assay of the suppressor shows a uniform, non-differential growth effect.
3. The biochemistry of the suppressor is **unmeasured** in every system: no uptake, no Km, no
   substrate flux (C1, C5). "Gain-of-function" is a genetic inference from in-cis reversion.

None of the above is a simulation. The only arithmetic I performed is the ~10⁸ timescale ratio in
C2, which is labelled `derived` there and in the block below.

```swarm-entail
{"source_claim": 281, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "A protein must exist whose qualitatively ALTERED activity (not reduced abundance or gene dose) is what suppresses enlargement; loss of that protein must not reproduce the suppression, or the mechanism is dosage rather than an enlarger-plus-suppressor pair.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Lat4a (L-type amino-acid transporter) carrying the nr21 T200K substitution. Daane et al. 2021 report nr21 'is dominant and without an obvious homozygous phenotype', that 'zebrafish lacking lat4a have no fin phenotype', and that an induced in-cis frameshift (L106Rfs39) reverts the fin phenotype, which the authors read as gain-of-function. Independent protein-level support: human SLC43A2 T200K overexpressed in HEK293T reduces proliferation (one-way ANOVA, p<0.01).",
      "satisfied_evidence": "measured",
      "note": "Daane et al. 2021 Curr Biol 31(22):5052-5061.e8, doi 10.1016/j.cub.2021.08.054, PMC9172250, read-level full-text for chars 0-100000 of the PMC author manuscript (figure panels and Table S1 could-not-access; final 49104 chars unread). HEK293T assay: PMC13574186 (syngnathid comparative-genomics paper, authors and year unknown), read-level full-text chars 0-100000, section 2.10 and Fig 2D legend; that paper reports no n, no percentage and no fold-change, and its own text says the mechanism 'requires further investigation' while its abstract says the in-vitro work confirms the role - disagreement preserved, not averaged. The DIRECTION of the activity change is unknown: no uptake, substrate or Km measurement exists for wild-type or T200K Lat4a in any system (Daane et al.: absent from text read; PMC13574186: 'Amino acid uptake/transport: Not measured'; search 'Lat4a zebrafish amino acid transporter fin growth transport assay slc43a2 mutant uptake', read-level search-summary, found no published uptake assay). Quotations passed through a summarising fetch tool and should be re-checked against the PDFs."},

    {"target_scale": "protein", "kind": "timescale",
      "statement": "The enlarger protein's activity must be required during the growth-TERMINATION phase of an outgrowth episode rather than the early proliferative phase, and that requirement window must be long compared with the protein's own gating kinetics, so that the tunable lever is a sustained activity set-point and not a kinetic parameter.",
      "quantity": "window of required channel activity within a ~30-day regenerative outgrowth",
      "lo": 6, "hi": 30, "units": "days post-amputation",
      "status": "satisfied",
      "satisfied_by": "Ectopic Kcnh2a in longfin. Astemizole 500 nM applied 7-30 dpa fully suppressed loft2/+ overgrowth to wild-type levels (P<0.0001); starting at 6 dpa was as effective as treating throughout; kcnh2a expression at 4 dpa had negligible functional impact; kcnh2a mutant fins were indistinguishable from wild type, so endogenous Kcnh2a does not set fin length. Authors' conclusion: ectopic Kcnh2a 'exclusively causes regenerative fin overgrowth by actively preventing growth termination' from about 7 dpa.",
      "satisfied_evidence": "measured",
      "note": "Stewart et al., PMC8217709 (2021; journal name unknown, citation block not retrieved), read-level full-text chars 0-100000 (final 19574 unread). Same paper: kcnh2a +25.8-fold by RNA-seq in 4-dpa loft2/+ caudal regenerates, below RT-qPCR detection in wild type, lof-t2 called 'a regulatory neomorph allele of kcnh2a' with the inversion/enhancer lesion flagged by the authors as hypothesis. Calcineurin companion timing: FK506 500 nM 4 h daily, 1-5 dpa no effect, 6-21 dpa and 1-21 dpa equal overgrowth; authors place Kcnh2a not downstream of calcineurin and leave up/downstream open. MY DERIVED arithmetic, not an observation: a >=6-day window against millisecond K+ channel gating is a ratio of order 1e8, hence time-averaged activity is the lever. SCOPE LIMIT: every number is regenerating CAUDAL fin in the single longfin heterozygote; the claim-281 phenotype is ontogenetic PAIRED-fin growth in the double heterozygote, where no equivalent window has been measured - that transfer is an assumption."},

    {"target_scale": "protein", "kind": "spatial",
      "statement": "The length scale at which the growth set-point is determined must match a single fin field or single ray rather than the whole animal, within a factor of a few; a systemic (endocrine, whole-body) determination scale cannot support per-fin differential allometry.",
      "quantity": "determination length scale of the growth decision",
      "lo": 0.1, "hi": 1.0, "units": "mm (adult zebrafish ray-to-fin width)",
      "status": "satisfied",
      "satisfied_by": "Tissue-autonomous, intra-ray action of ectopic Kcnh2a. Blastula transplants of EGFP+ loft2/+ cells into wild-type hosts gave overgrown chimeric fins in 39 fins from 28 of 214 chimeras (13%); all overgrown chimeric rays contained EGFP+ intra-ray mesenchyme, 30 overgrown fins contained only EGFP+ mesenchyme, and epidermis-only chimeras were of normal length (n=3). Mosaic F0 CRISPR knockouts gave partial regionalized overgrowth in 17 of 78 fish (21.8%). RNAscope localised kcnh2a to Msx+ / tph1b:mCherry+ proximal intra-ray cells.",
      "satisfied_evidence": "measured",
      "note": "Stewart et al., PMC8217709, read-level full-text chars 0-100000. The epidermis-only negative control is n=3, which is very small. Reported left-right asymmetry (one pectoral fin near wild-type length, contralateral overgrown) in 'a few' crispants and chimeras is qualitative - no numbers given. SCOPE: kcnh2a only, caudal and pectoral fins; no mosaic or chimeric experiment for Lat4a appeared in the text I read."},

    {"target_scale": "protein", "kind": "existence",
      "statement": "Since the same two effector activities are present in both paired and medial fin fields while the growth outcomes have opposite sign, something at the protein scale must differ between fin fields: either a differential abundance/activity of one effector, or a third fin-type-specific component that flips the sign of the readout. Without one of these there is no protein-scale mechanism for differential allometry across fins.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "NOT FOUND. Branch one (differential effector abundance) is reported ABSENT: Daane et al. 2021 report kcnh2a 'expression does not vary significantly in pectoral or dorsal fins containing the nr21 mutation' (qRT-PCR) and 'no significant difference in lat4a expression across fins and genotypes' (Fig 4E legend); no baseline paired-vs-medial comparison without the mutations is reported, and pelvic and anal fins are not assayed for expression at all. Branch two (a third fin-type-specific component) returned nothing measured: the nearest pathway, Kcnk5b/calcineurin, is explicitly reported by its own authors as NOT re-specifying positional memory but acting on growth rate, and its experiments are on pectoral and caudal fins. A lineage difference does exist (dorsal/anal fin skeleton from sclerotome/paraxial mesoderm rather than neural crest, PMC11664171) but that is a developmental-origin fact, not a measured protein-level modulator of the Kcnh2a/Lat4a axis, and is not scored as satisfying this constraint.",
      "satisfied_evidence": "literature",
      "note": "NEGATIVE SCOPE, stated so it can be audited. Branch one: Daane et al. 2021 PMC9172250, read-level full-text for prose, COULD-NOT-ACCESS for Fig 4D/4E panels and Table S1 - people looked and reported no difference. Branch two: three searches at read-level search-summary - 'fin-type specific growth modifier zebrafish paired versus median fin positional identity differential allometry kcnk5b tbx5 hoxd13'; '\"dorsal\" \"anal\" fin versus pectoral fin differential response calcineurin FK506 longfin overgrowth fin-type specific suppression zebrafish'; plus the lat4a allele search - nobody appears to have looked. Those two negatives are different findings and are NOT merged. Supporting search-summary sources: Kcnk5b/calcineurin allometry (PMID 29991812; PLoS Genet 2014 pgen.1004080); calcineurin blastema polarity (10.1073/pnas.2009539118), which notes proximal-column regeneration 'also occurred' in anal and dorsal fins after FK506 without comparing it to pectoral. WHY NOT unsatisfiable: calling it unsatisfiable would need a measured expression ratio with variance tight enough to exclude a sufficient difference; 'does not vary significantly' with unknown n and unknown variance, in panels I could not open, is not that number. SHARPEST COUNTER-DATUM, flagged as inference not refutation: the only protein-level functional assay of the suppressor variant anywhere (human SLC43A2 T200K in HEK293T, PMC13574186) produces a UNIFORM proliferation decrease with no fin-type dependence; HEK293T cells have no fin identity so this cannot refute the requirement, but it means the protein-scale evidence base currently supplies no differentiality at all. MY INFERENCE, separate from any author's claim: claim 281's 'the design lever is differential allometry across fins' names a protein-scale mechanism that has not been identified - the genetic phenotype is real, its protein-level source of differentiality is unknown."},

    {"target_scale": "protein", "kind": "conservation",
      "statement": "Net influx of the suppressor transporter's essential neutral amino-acid substrates into paired-fin mesenchyme must balance or exceed that tissue's protein-synthesis demand, because paired fins grow FASTER than wild type while the suppressor variant is present; a mechanism acting by pushing substrate supply below demand would produce tissue-wide wasting, not a change in proportion.",
      "quantity": "net essential neutral amino-acid influx per unit growing fin mass, as a ratio to the tissue's protein-synthesis consumption rate",
      "lo": 1, "hi": null, "units": "dimensionless ratio (influx/demand); absolute rates unknown",
      "status": "open",
      "satisfied_by": "NEITHER TERM MEASURED in the relevant tissue. Searched for the supply term: 'Lat4a zebrafish amino acid transporter fin growth transport assay slc43a2 mutant uptake' - no published uptake assay in zebrafish slc43a2/lat4a mutants. Searched for the demand term: 'zebrafish fin regeneration blastema amino acid flux leucine mTORC1 requirement protein synthesis rate measurement' - no isotope-tracer amino-acid flux and no measured protein-synthesis rate in the blastema. Nearest measured results, neither of which closes the constraint: Takayama et al. 2018 (PMC5974189) report that leucine or glutamine individually did NOT activate mTORC1 during fin regeneration while the two together did, which cuts against a naive single-substrate supply model; and an IGFR/mTOR study reporting elevated global translation in blastema cells, method not seen.",
      "satisfied_evidence": "unknown",
      "note": "Read-level search-summary for both searches and for Takayama et al. 2018 and the IGFR/mTOR paper - neither opened. Mammalian anchor at read-level listing/search-summary only: Slc43a2 knockout mice show growth restriction, postnatal malnutrition and early death (PMC7693055 and a ResearchGate listing, not opened); that is organismal, and since the zebrafish lat4a deletion has no fin phenotype the mouse null does not transfer. Recorded 'open' rather than 'unsatisfied' deliberately: my search was two queries deep and aimed at transport assays, not at fin bioenergetics - puromycin/SUnSET or OPP-labelling searches were not run. The honest statement is that this is checkable in principle from a tracer experiment and the experiment appears not to have been done in this tissue."}
  ]}
```
