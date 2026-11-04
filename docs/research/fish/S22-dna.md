# S22 (dna) — What exactly did Daane et al. achieve in phenocopying flying-fish fin proportions?

Project: `zebrafish-flight`. Scale: DNA. Date of work: 2026-11-04.

---

## 1. The question, restated precisely

Daane et al. (2021) is the closest published result to this project's goal: a
genetic manipulation of *Danio rerio* reported to "phenocopy" the fin
proportions of flying fishes. The project needs to know **exactly what was
changed, by how much, measured along which axis, and what was never tested.**

The numbers that make this hard:

- A zebrafish is ~4 cm standard length (SL) and ~0.4 g. Its pectoral fin is a
  short paddle, not a wing.
- A two-wing flying fish (*Exocoetus volitans*) carries pectoral fins at
  **70–75% of SL** (FAO species guide, read-level: search-summary), i.e. a
  pectoral fin nearly as long as the entire body.
- Gliding needs **wing area** (and hence wing loading, N·m⁻²), not fin length.
  Area scales as roughly the square of a linear fin dimension, so an axis
  mismatch between what Daane et al. measured and what a glider needs is not a
  detail — it is potentially the whole gap.

So the question decomposes into three sharp sub-questions:

1. Which genes and alleles, named exactly?
2. What was quantified — fin **length/SL**, or fin **area**? With what effect size?
3. Was any aerodynamic or locomotor property measured? (Anticipated answer: no.)

---

## 2. What is measured

### 2.1 The paper

| Field | Value |
|---|---|
| Title | *Modulation of bioelectric cues in the evolution of flying fishes* |
| Authors | Jacob M. Daane, Nicola Blum, Jennifer Lanni, Helena Boldt, M. Kathryn Iovine, Charles W. Higdon, Stephen L. Johnson, Nathan R. Lovejoy, Matthew P. Harris |
| Journal | *Current Biology* |
| Year | 2021 (online 16 Sep 2021; issue 22 Nov 2021) |
| Volume/pages | 31(22): 5052–5061.e8 |
| DOI | `10.1016/j.cub.2021.08.054` |
| PMID / PMCID | 34534441 / PMC9172250 |
| Earlier preprint | bioRxiv `10.1101/2021.03.05.434157`, titled *Novel regulators of growth identified in the evolution of fin proportion in flying fish* |
| Read-level | **full-text** for main text and Methods (PMC author manuscript, PMC9172250); **could-not-access** for figures, figure panels and supplementary tables (not rendered in the PMC author manuscript; Table S1, which the Results cite as holding the fin-length data, was not retrievable) |

Note the title change between preprint and journal version: the preprint framed
the result as *fin proportion*, the published version as *bioelectric cues*. The
underlying experiment is the same.

### 2.2 Genes and alleles, as named by the authors (read-level: full-text)

- **`lat4a`** — an L-type amino acid transporter. Alleles:
  - `lat4a^nr21` (also designated `dmh26`), a **dominant short-fin** allele; the
    lesion is the missense substitution **T200K**.
  - `lat4a^del` (also designated `mh152`), a deletion allele.
  - `lat4a` **F326L** is reported as a convergent amino acid substitution found
    in gliding beloniforms; a frameshift revertant `L106Rfs39` is also named.
- **`kcnh2a`** — a voltage-gated potassium channel, implicated via the classical
  dominant **`longfin` (`lof`)** locus. Alleles named: `lof^dt2`, `lof^j6e1`
  (listed as `lof^Df(Chr02:csnk1g2a,rnf2,kifap3b)j6g1/j6g1`), `lof^lfr1`
  (Y669N), `lof^lfr2` (L739Q), `lof^WL4` and `lof^WL7` (Y418X).
- Other genes discussed in the paper's comparative-genomic analysis: `kcnk5b`
  (incl. the `alf` mutant), `kcnk5a`, `kcnk9`, `kcnj13`, `prrx1a`, `cx43`
  (`gja1`), `evx1`, `cyp26b1`, `cyp27c1`, `aldh1a2`, `sall1a`.

**The phenocopy genotype is the double heterozygote `kcnh2a^lof/+ ; lat4a^nr21/+`.**
It is a cross of two pre-existing zebrafish mutant alleles — not an engineered
flying-fish allele, not a transgene, not a knock-in of a flying-fish sequence.
(Author's claim: the epistatic interaction is "sufficient to phenocopy this key
innovation." My inference: the manipulation is therefore a *genetic-background
recombination* result, and carries no evidence that the flying-fish orthologues
themselves were tested in zebrafish.)

### 2.3 The phenotype, as described (read-level: full-text for prose)

- Paired fins: **overgrown / "elongated paired fins"** (Fig. 4A legend).
- Caudal fin: **"generally wild type in size"** but **hypocercal**, with an
  elongated ventral lobe — the authors call this "remarkably similar" to flying
  fishes.
- Medial (dorsal/anal) fins: **wild-type size**; `lat4a^nr21/+` acts as a
  "medial fin suppressor" of the `lof` overgrowth. This fin-type-specific
  suppression is the actual novelty of the paper.
- Abstract (preprint): the interaction "closely phenocopies the observed fin
  proportions of flying fishes."
- `lat4a^nr21` has smaller lepidotrichial segments (Fig. S2A–B), reported
  without values in the text.

### 2.4 Quantification as reported in text (read-level: full-text)

- Measurement convention: **fin length normalized to standard length (SL)**.
  Stated for Figs. 3B, 3D, 4B, 4C (and in the preprint for Figs. 5D, 8).
- Statistics: one-way ANOVA with Tukey HSD pairwise comparisons (Figs. 3B, 3D,
  4B–4E, S2B, S2I). Boxplots show quartiles and median.
- Significance levels quoted: Fig. 3B adjusted p ≤ 0.0001 and ≤ 0.001; Fig. 3D
  Tukey HSD adjusted p ≤ 0.0001; Fig. 4 legend p ≤ 0.0001, ≤ 0.01, ≤ 0.05;
  Fig. 2C p < 0.05 (two-tailed t test).
- **Effect sizes: `unknown`.** The main text reports no numeric value for
  pectoral fin length as a fraction of SL for wild type, either single mutant,
  or the double mutant. The Results direct the reader to Table S1 for fin-length
  data. See §2.6 for access attempts.
- **Fin area: not reported anywhere in the text I could read.** Searching the
  accessible full text and Methods for area/wing-area/wing-loading
  quantification of the zebrafish mutants returned nothing (scope of negative
  search: PMC9172250 full text including STAR Methods and Quantification
  section, plus the bioRxiv full text; figures and supplements not accessible).

### 2.5 Comparative / phylogenomic measurements (read-level: full-text)

- 35 species sequenced; 78.3% average coverage at 38.3-fold depth; 4,683 genes
  used for the phylogeny.
- 44 convergent amino acid substitutions in gliding beloniforms vs 14–28 in
  control comparisons (Fig. S1C).
- 48 of 17,937 genes showed convergent rate shifts after FDR correction.
- Allometry (qualitative in text): halfbeaks and needlefishes show "only subtle
  increases in pectoral fin length as the body grows"; flying-fish pectoral fin
  length "increases rapidly"; the body-size/pectoral-fin-length relationship was
  **"identical across the two- and four-wing flying fishes"** (Fig. 1B); gliding
  halfbeaks are intermediate. No slopes or exponents given in text.

### 2.6 Independent flying-fish morphometrics (for the axis comparison)

These are **not** from Daane et al. They are the external anchors that let the
project judge whether the phenocopy is in the right axis. Read-level:
**search-summary** for all of them — I did not open these papers.

| Quantity | Value | Source | Read-level |
|---|---|---|---|
| Pectoral fin length, *Exocoetus volitans* | 70–75% of SL | FAO species identification guide | search-summary |
| Upper bound on pectoral fin length before swimming is impaired | 78–79% of SL | Davenport, NE Atlantic Exocoetidae (JMBA) | search-summary |
| Same bound, alternative figure | 76% of SL ("tips interfere with propulsive tail beat") | separate abstract located in same search | search-summary |
| Total wing area definition | pectoral + pelvic fin areas + intervening body rectangles; n = 199 specimens, 6 genera | Fish 1990, *J. Zool.* 221:391–403 | search-summary |
| Pectoral share of wing area across body size | approximately constant | Fish 1990 | search-summary |
| Wing loading vs SL | positive allometry, exponent b ≈ 2.36 | Davenport | search-summary |
| Wing area / wing loading allometry | described as **negative** allometry | a second abstract in the same search | search-summary |

**Disagreement preserved, not averaged:** (a) the swimming-impairment bound on
fin length is given as 76% in one source and 78–79% in another; (b) the
wing-loading allometric direction is reported as positive in one source and
negative in another. I did not resolve either; both pairs are recorded as stated.

### 2.7 Access attempts for the missing numbers (scope of negative search)

What I tried, and what happened:

1. PMC9172250 full text, three passes (offsets 0, 55k, 100k) — main text and
   STAR Methods obtained; **figures, figure panels and supplementary tables are
   not included in the PMC author manuscript**, so no axis values or Table S1.
2. bioRxiv `2021.03.05.434157v1.full`, two passes — same outcome; the preprint
   Methods do not state the fin-measurement protocol in the accessible portion,
   and Table S1 is referenced but not inline.
3. ZFIN figure record `ZDB-FIG-221222-35` (Daane et al. 2021, Fig. 4) —
   **HTTP 503, could-not-access.**
4. bioRxiv full text first attempt — **HTTP 429**, retried successfully.
5. ScienceDirect version (`S0960982221011908`) — not attempted after the PMC
   author manuscript proved to be the fuller accessible copy; the publisher copy
   is paywalled for figures/supplements.

Not tried: emailing the lead contact (the paper's data-availability statement
says reanalysis information is available from the lead contact on request);
digitizing values off a figure image. I deliberately did **not** estimate values
from figure images, because a digitized estimate presented in a table reads like
a reported measurement.

---

## 3. What I computed

**This section is computation, not observation.** It is one order-of-magnitude
check, done to make the axis problem explicit. It uses no number from Daane
et al.; it uses the external flying-fish value from §2.6.

**Assumptions**, each of which is a weakness:
- Fin area scales as the square of fin length at fixed fin shape (constant
  aspect ratio). Daane et al. report no aspect-ratio data for the mutants, so
  this is unverified for the phenocopy.
- Zebrafish pectoral fin length as a fraction of SL in wild type is `unknown`
  (see §2.4), so I cannot anchor the ratio at the zebrafish end. I therefore
  compute only the *sensitivity*, not the gap.

**Arithmetic.** If a mutant achieves a fractional increase *f* in pectoral fin
length/SL, and shape is preserved, then fin **area** per unit body area changes
by (1 + *f*)². Wing loading, for fixed mass, changes by 1/(1 + *f*)².

- *f* = 0.25 → area factor 1.5625 → wing loading × 0.64
- *f* = 0.50 → area factor 2.25 → wing loading × 0.44
- *f* = 1.00 → area factor 4.0 → wing loading × 0.25

**What this computation shows:** a length-axis result cannot be converted into a
wing-loading statement without (i) the measured *f* for the double mutant and
(ii) evidence that fin shape, not just length, was preserved. I have neither.
Both are required before S22 can feed any aerodynamic subproblem.

---

## 4. The answer

**Evidence level: `literature`** (with the decisive effect-size number
`unknown` — see §2.4 and §2.7).

Daane et al. (2021, *Current Biology* 31:5052–5061.e8,
`10.1016/j.cub.2021.08.054`) achieved a **morphometric phenocopy of flying-fish
fin proportions in zebrafish, by crossing two pre-existing dominant mutant
alleles** — `lat4a^nr21/+` (missense T200K, a short-fin allele) and the
`longfin` allele `kcnh2a^lof/+` — producing double heterozygotes with
**elongated paired fins, a hypocercal caudal fin with an elongated ventral lobe,
and wild-type-sized medial fins**, the fin-type-specific pattern that
distinguishes flying fishes from generic long-finned mutants. The measured axis
was **fin length normalized to standard length**, tested by one-way ANOVA with
Tukey HSD (adjusted p ≤ 0.0001 for the main comparisons). The mechanistic claim
is that `lat4a` modulates a bioelectric (potassium-channel) growth cue in a
fin-type-specific way.

**The authors' claim** is that the epistatic interaction is "sufficient to
phenocopy this key innovation" and is "remarkably similar to the fin phenotype
of flying fishes." **My inference, stated separately:** this is a claim about
*proportion and pattern*, not about *wing area, wing loading, fin stiffness, or
any aerodynamic property*, and the paper contains no test of the latter.

**Lift, gliding, flight and locomotor performance were not tested.** Gliding is
treated throughout as a known behaviour of flying fishes, cited to prior
literature (Davenport); the anti-predator origin of gliding is offered as a
hypothesis, not a result. The zebrafish experiments measured fin size and shape
only. (Read-level: full-text; this is an explicit absence across the accessible
main text and Methods.)

**Key number:** `null`. The single number that would decide the magnitude of the
achievement — pectoral fin length/SL in `kcnh2a^lof/+ ; lat4a^nr21/+` versus
wild type — lives in figure panels and Table S1, which I could not access.

### On the stated refutation criterion

The brief says the answer is refuted by "evidence the phenocopy was morphometric
only and did not alter pectoral fin area in the relevant axis." **The first half
is confirmed: the phenocopy was morphometric only.** The second half is
**partially confirmed and partially unknown**: the paper altered and measured fin
**length**, and reports no measurement of fin **area** at all. So the phenocopy
is not demonstrated to be in the axis the project needs (area → wing loading);
whether fin area in fact increased is untested-but-likely (a longer fin of
similar shape has more area), and that likelihood is my inference, not a
measurement. Anyone reading this deliverable as support for feasibility is
reading it wrong.

---

## 5. What this does NOT establish

- **It does not establish that the double mutant can glide, generate lift, or
  leave the water.** No aerodynamic, hydrodynamic or kinematic measurement was
  made on these fish.
- **It does not establish a wing area or wing-loading change.** Area was never
  reported. §3's conversion is arithmetic on an assumption, not data.
- **It does not establish that fin shape (aspect ratio) is flying-fish-like.**
  Aspect ratio governs lift-to-drag; it is unreported for the mutants.
- **It does not establish that the double mutant approaches 70–75% SL pectoral
  fins.** The magnitude is `unknown`. "Remarkably similar" is a qualitative
  authorial judgement about pattern, and I have no basis to translate it into a
  fraction of SL.
- **It does not establish fin stiffness, ray architecture, or musculature
  changes.** Flying fishes have stiffened rays, enlarged pectoral musculature
  and modified semicircular canals; the paper cites these from prior work and
  does not reproduce them. Indeed `lat4a^nr21` is reported to have *smaller*
  lepidotrichial segments — a ray-architecture change of unstated sign for
  stiffness.
- **It does not establish that flying-fish alleles were tested.** The experiment
  crossed zebrafish laboratory alleles. The convergent flying-fish substitution
  `lat4a` F326L is a comparative-genomic observation, not something the paper
  reports installing in zebrafish. (Scope: I found no knock-in of F326L in the
  accessible text; figures/supplements not checked.)
- **It does not establish viability, swimming competence, or fitness cost.**
  Independent work (§2.6, search-summary) suggests pectoral fins beyond ~76–79%
  SL impair swimming in flying fishes themselves; the double mutant's swimming
  was not assessed in anything I could read.
- **It does not establish body-mass or body-shape change.** Flying-fish gliding
  depends on a mass-and-area package; only fins were altered here.
- **It does not establish that the epistasis is dosage-reproducible**, e.g. that
  homozygotes go further, or that the effect holds across genetic backgrounds.
- **Read-level honesty:** every value in §2.6 is search-summary. If this
  deliverable is used to set a target fin proportion, those sources must be read
  in full first.

---

## 6. What would change the answer

In descending order of how much it would move S22:

1. **Obtain Table S1 and the Fig. 4B–4E panel values** from *Current Biology*
   (institutional access) or by request to the lead contact (Matthew P. Harris).
   This yields the missing key number: pectoral fin length/SL for wild type,
   `lat4a^nr21/+`, `kcnh2a^lof/+`, and the double mutant, with n. Cheapest
   decisive step. Would promote the key number from `null` to `measured`.
2. **Any planar fin-area measurement** (photograph + area integration) on the
   double mutant, giving fin area and hence wing loading at ~0.4 g. This is the
   measurement that converts S22 from a proportion result into an input for the
   aerodynamic scales. It is also the measurement whose absence currently
   satisfies half the refutation criterion.
3. **Aspect-ratio measurement** of the double-mutant pectoral fin, compared with
   Fish (1990) values for Exocoetidae genera.
4. **A glide or lift test** — even a passive drop/tow test on a fixed specimen —
   would be the first aerodynamic datum on a genetically modified zebrafish and
   would decide whether the proportion change buys anything.
5. **Reading Fish (1990) and Davenport in full** to resolve the two preserved
   disagreements (76% vs 78–79% fin-length bound; positive vs negative
   wing-loading allometry). Both bear on what the project should target.
6. **Checking whether `lat4a` F326L or any flying-fish allele has since been
   installed in zebrafish** (literature after Sep 2021). If it has, the
   precedent is stronger than this paper and S22 should be re-answered against
   that work instead.

---

```swarm-result
{"subproblem": "S22", "evidence": "literature",
  "answer": "Daane et al. 2021 (Curr Biol 31:5052-5061.e8, doi:10.1016/j.cub.2021.08.054) phenocopied flying-fish fin proportions in zebrafish by crossing two dominant alleles, lat4a^nr21/+ (T200K) and the longfin allele kcnh2a^lof/+, yielding double heterozygotes with elongated paired fins, a hypocercal caudal fin with elongated ventral lobe, and wild-type-sized medial fins, measured as fin length normalized to standard length only, with no measurement of fin area, aspect ratio, lift, gliding or flight.",
  "key_number": null,
  "blocked_on": "The magnitude of the fin proportion change: pectoral fin length/SL for wild type vs kcnh2a^lof/+;lat4a^nr21/+ is in Table S1 and the Fig. 4 panels, which are absent from the PMC author manuscript (PMC9172250) and the bioRxiv preprint text; ZFIN figure record ZDB-FIG-221222-35 returned HTTP 503. Fin area was never reported by the authors at all."}
```
