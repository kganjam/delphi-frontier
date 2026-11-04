# Claim 281: what it requires one scale down (dna → protein)

**Source claim (dna scale, evidence: derived).** "MECHANISTICALLY THIS IS ENLARGER PLUS SUPPRESSOR, not
uniform enlargement. That is why the published result is about fin PROPORTIONS rather than fin size, and it
means the design lever is differential allometry across fins rather than growth of one fin."

**Target scale:** protein.

**Date:** 2026-11-04.

## 0. Which published result the claim refers to

The claim does not cite a paper, and nothing in this repository mentions it (I searched the repo for
"enlarger", "suppressor" and "fin proportion" and found no matches). I took it to refer to the paper below,
because that paper's own Figure 4 legend uses the word "suppressor" and its result is about fin
*proportion*. **This identification is my inference, not something the claim says.**

- **[D21]** Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP.
  "Modulation of bioelectric cues in the evolution of flying fishes." *Curr Biol* 31(22):5052–5061.e8
  (2021). doi:10.1016/j.cub.2021.08.054, PMID 34534441, PMC9172250.
  **Read-level: full-text** (the NIH author manuscript, retrieved through the PMC OAI-PMH service; I read the
  extracted text, not the figure panels).
- **[S21]** Stewart S, Le Bleu HK, Yette GA, Henner AL, Robbins AE, Braunstein JA, Stankunas K. "longfin
  causes cis-ectopic expression of the kcnh2a ether-a-go-go K+ channel to autonomously prolong fin
  outgrowth." *Development* 148(11):dev199384 (2021). doi:10.1242/dev.199384, PMID 34061172, PMC8217709.
  **Read-level: abstract** for the published version (Europe PMC). For the timing numbers I used the
  bioRxiv preprint 10.1101/790329v3. **Read-level: full-text, but through an automated extractor.** I did
  not check the quoted sentences against the PDF by hand, and the extractor read only the first 100,000 of
  about 157,000 characters.

The facts from [D21] that everything below rests on (the authors' statements, read in full text):

1. `lat4a` allele **nr21** carries a predicted **T200K** substitution in "a conserved domain of the L-type
   amino acid transporter". It is **dominant** and shortens **all** fins. Frameshift mutations made in cis
   revert it to wild type, "indicating that the mutation in lat4a nr21 results from a gain-of-function
   effect." Body size (standard length) is not significantly reduced.
2. `kcnh2a` allele **lof^dt2** (longfin) is an **inversion** that puts the *prrx1a* regulatory region
   upstream of *kcnh2a* without touching either coding sequence. It causes "coordinated overgrowth of **all**
   fins", and the effect is dose-sensitive. Loss-of-function *kcnh2a* alleles in cis revert it, so it is a
   gain of function. "Expression of kcnh2a was not detected (n.d.) in wild-type fins." Mosaic
   *ubi:hKCNH2* clones give "localized overgrowth of rays autonomous to the fin clone", with GFP+
   **fibroblast** clones under the overgrown rays.
3. Double heterozygotes *lat4a^nr21/+; kcnh2a^lof/+* show "specific, **non-additive** variation in
   proportion among fins". In the authors' words: "while all fins of kcnh2a lof/+ are overgrown and all fins
   of lat4a nr21/+ are shortened, the [double heterozygotes] show wild-type-sized medial fins, while the
   paired fins are overgrown". The caudal fin is hypocercal. The authors call nr21 "a **medial fin
   suppressor** of kcnh2a lof/+".
4. qRT-PCR: "kcnh2a expression does not vary significantly in pectoral or dorsal fins containing the nr21
   mutation", and the Fig. 4E legend says "no significant difference in lat4a expression across fins and
   genotypes". The authors conclude that the fin-specific suppression "is occurring downstream of
   bioelectric signaling signals".
5. The allele that evolved in flying fishes is a different substitution, **F326L** ("Convergent amino acid
   substitution in a highly conserved region of Lat4a"), not T200K.

**What the paper supports and where the claim goes further.** The claim's mechanism is supported. Each allele
on its own acts *uniformly*: one enlarges every fin, the other shrinks every fin. The difference between fin
types appears only in the **interaction** (fact 3). So "not uniform enlargement" is right, and "enlarger plus
suppressor" is the authors' own framing. A distinction the claim leaves implicit matters at the protein
scale: the suppressor does not suppress *differentially* on its own. The fin-type specificity comes from the
epistasis, which is why the third constraint below is needed.

## 1. Constraints at the protein scale

### C1 — existence: a growth-extending activity gained in fin outgrowth tissue

*Requirement.* A protein activity must exist that, when gained in the cells that set fin outgrowth, extends
outgrowth in **every** fin type. The enlarger must be uniform, so that suppressing it partially gives
proportion rather than size.

*Check: **satisfied** (literature, with measured observations in the source).* Kcnh2a, a voltage-gated K+
channel, is expressed ectopically from the lof^dt2 inversion. It is not detected in wild-type fins, it
overgrows all fins, cis loss-of-function alleles revert it, and the overgrowth is clone-autonomous in
fibroblasts [D21, full-text]. [S21, abstract] independently reports that the ectopic *kcnh2a* "acts tissue
autonomously within the fin intra-ray mesenchymal lineage" (shown by cell transplantation) and suggests
Kcnh2a "inhibits calcineurin output to supersede growth cessation signals". The calcineurin link is the
authors' interpretation of epistasis experiments, not a direct biochemical measurement. Other K+ channels can
satisfy the same generic requirement: [D21] cites overexpression of *kcnk5b*, *kcnj13* and *kcnk9* as
sufficient for fin overgrowth. I did not read those primary sources (read-level for them: **listing**, via
the [D21] text only).

### C2 — existence: a dominant growth-limiting activity that acts downstream of the enlarger's expression

*Requirement.* A second protein activity must exist that limits fin growth when gained, and that suppresses
the enlarger **without** lowering the enlarger's expression. If it simply lowered expression, the double
mutant would just be a weaker enlarger, and the result would be a uniform size change rather than a
proportion change.

*Check: **satisfied** (literature, with measured qRT-PCR in the source).* Lat4a T200K (nr21) is a dominant
gain of function that shortens fins and suppresses the lof overgrowth in medial fins. qRT-PCR shows no
significant change in *kcnh2a* mRNA in nr21 pectoral or dorsal fins [D21, full-text]. Mammalian Lat4 moves
Ile, Leu, Met and Phe "into the cell in an ion- and pH-independent manner" (as [D21] reports, citing its
ref. 16, which I did not read; read-level **listing**). *What T200K does to transport* (more flux, less flux,
altered specificity, or a non-transport "transceptor" role) is **unknown**. [D21] reports no transport assay
for it, so C2 is satisfied at the level of genetic action only. The caveat is that the qRT-PCR shows no
*significant* change, and the group sizes are in the figure, which I did not read. Absence of significance is
not proof of equal expression.

### C3 — existence: something that differs between paired and medial fins must gate the interaction, and it is not transcript level

*Requirement.* The enlarger is uniform and the suppressor alone is uniform, yet the combination is fin-type
specific. So some protein-level factor must differ between paired fins (pectoral, pelvic) and medial fins
(dorsal, anal, caudal) and decide whether Lat4a(gain) cancels Kcnh2a(gain). Examples would be a partner,
substrate supply, protein abundance or localisation, or the downstream node they converge on. Without such a
factor the claimed "differential allometry lever" has nothing to act on.

*Check: **unsatisfied**. People looked at one level and found nothing; the protein level has not been
looked at.*
- **Looked, found nothing:** [D21] measured *lat4a* mRNA "across fins and genotypes" and found no
  significant difference. It measured *kcnh2a* mRNA in pectoral versus dorsal fins and found no significant
  change with nr21. So differential **transcript** abundance of either gene is not, as far as measured, the
  gate.
- **Not looked at (within the scope I searched):** Lat4a or Kcnh2a **protein** abundance, localisation or
  activity by fin type; amino-acid supply by fin; any candidate gating factor that differs between paired
  and medial fins. [D21] proposes none and calls the suppression "downstream of bioelectric signaling". The
  calcineurin node in [S21] is a natural place for the two pathways to meet. That is my inference: neither
  paper tests a Lat4a–calcineurin interaction, and [S21] makes no fin-type comparison in its abstract.
- **Search scope for this negative:** the full text of [D21]; the abstract of [S21]; Europe PMC queries
  "slc43a2a AND (fin OR zebrafish)" (3 hits, none relevant) and "LAT4 SLC43A2 amino acid transporter system
  L Km" (no fin-related hits). I did **not** query zebrafish fin single-cell atlases, ZFIN expression
  records (zfin.org returned HTTP 503 and its mirror host is outside this session's network allowlist), or
  later citing papers.
- **Not unsatisfiable.** A version of the claim saying "the suppressor is differentially expressed across
  fins" would be in tension with the measured result in [D21] Fig. 4E. But that result is a
  non-significant difference, not a measured value that excludes a stated range, so it does not reach
  `unsatisfiable`. Claim 281 as written does not require differential suppressor expression anyway.

### C4 — timescale: the suppressor must act within the enlarger's late outgrowth window, not only during early patterning

*Requirement.* The enlarger works by **prolonging the outgrowth period**, not by raising peak growth rate
[S21]. The suppressor cancels it in medial fins, so the suppressor's protein activity must be present and
effective in the same late window. A suppressor active only early (before about 6 dpa in regeneration, or
during fin-fold patterning in development) could not cancel a late-acting enlarger.

*Bounded quantity:* the window in which the enlarger acts, measured in **regeneration**: from about 6 to about
30 days post-amputation (dpa).

*Check: **open**. The enlarger side is measured; the suppressor side has not been checked.*
- Enlarger side (measured, [S21] preprint full-text via extractor): "Wildtype and lof^t2 fish had
  indistinguishable maximal growth rates reached between 3 and 5 dpa"; "Wildtype fins largely ceased
  regenerative outgrowth by 21 dpa, whereas lof^t2 fins continued to extend through the 30 dpa period";
  astemizole (a Kcnh2a inhibitor) from 7–30 dpa suppressed the overgrowth, and "starting astemizole treatment
  at 6 dpa was as effective as administration throughout regeneration". These are regeneration numbers. Their
  transfer to **developmental** fin growth, which is what [D21]'s adult proportions reflect, is an assumption.
- Suppressor side: [D21] reports adult fin lengths and qRT-PCR on adult and regenerating tissue. I found no
  measurement of when Lat4a(T200K) acts, no regeneration time course for nr21 or the double mutant, and no
  temporal inhibition of Lat4a. That is "not found in the sources read", not "shown absent".

### C5 — spatial: the suppressor must act in, or within signalling range of, the mesenchymal lineage where the enlarger acts

*Requirement.* The enlarger acts **cell- or clone-autonomously** in intra-ray mesenchyme or fibroblasts:
[D21] saw overgrowth localized to the hKCNH2 clone, and [S21] showed autonomy by transplantation. So the
suppressor must act on the same cells, or on cells close enough to them that a non-autonomous signal reaches
them. A suppressor confined to another compartment (epidermis, osteoblasts only, or systemic) is allowed only
if a non-autonomous route exists, and that would need its own constraint.

*Bounded quantity:* the distance between the cells where Lat4a acts and the cells where Kcnh2a acts. I give
no numeric bound. [D21] reports clone-level autonomy, but I found no measured clone or ray width I could cite,
and I will not invent one.

*Check: **open**.* [D21] measured *lat4a* only in whole-fin homogenates (qRT-PCR), which cannot resolve cell
type. I found no in situ, reporter or single-cell localisation of *lat4a*/Lat4a in zebrafish fins (scope as
in C3: two Europe PMC queries, [D21] full text, no atlas query). Whether nr21 acts autonomously (by clone
analysis or transplantation) has not been reported in [D21].

## 2. Caveat on the design lever (outside the six kinds, recorded so it is not lost)

The claim's lever, "differential allometry across fins", depends on the flying-fish allele behaving like the
zebrafish one. It is not the same substitution: **F326L** in flying fishes, **T200K** in zebrafish nr21
[D21]. [D21] did not test whether F326L is a gain of function in the same direction, and I found no such
test. The authors also note that *Parexocoetus brachypterus* lacks F326L and has an elongated dorsal fin.
That observation fits a medial-fin suppressor whose loss lets the medial fin grow, but it is a single
species and the fit is my inference.

## 3. Summary

| # | kind | status | one-line reason |
|---|------|--------|-----------------|
| C1 | existence | satisfied | Kcnh2a ectopic gain from the lof inversion; clone-autonomous overgrowth of all fins [D21, S21] |
| C2 | existence | satisfied | Lat4a T200K, dominant gain of function, suppresses lof without changing *kcnh2a* mRNA [D21]; effect on transport unknown |
| C3 | existence | unsatisfied | the paired-vs-medial gate is not *lat4a* or *kcnh2a* transcript level (measured, n.s.); protein level not examined |
| C4 | timescale | open | enlarger acts from about 6 to 30 dpa (measured, in regeneration); suppressor timing not measured |
| C5 | spatial | open | enlarger is mesenchyme-autonomous; suppressor's cellular site not reported |

No constraint is `unsatisfiable`: I found no measured value that contradicts the claim at the protein
scale. The most informative next measurement is C3: compare Lat4a protein, or a downstream readout such as
calcineurin/NFAT activity, between pectoral and dorsal fins of double heterozygotes.

```swarm-entail
{"source_claim": 281, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "A protein activity must exist that, when gained in fin outgrowth-determining cells, extends outgrowth uniformly across all fin types (the enlarger).",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Ectopic Kcnh2a voltage-gated K+ channel from the lof^dt2 inversion (prrx1a regulatory region placed upstream of kcnh2a); not detected in WT fins; all fins overgrown; reverted by cis kcnh2a loss-of-function; hKCNH2 mosaic clones give clone-autonomous ray overgrowth in fibroblasts.",
      "satisfied_evidence": "literature",
      "note": "Daane et al. 2021 Curr Biol 31:5052, doi:10.1016/j.cub.2021.08.054, PMC9172250 (full-text); Stewart et al. 2021 Development 148:dev199384, doi:10.1242/dev.199384 (abstract): tissue-autonomous in intra-ray mesenchyme by transplantation; calcineurin link is the authors' epistasis-based inference."},
    {"target_scale": "protein", "kind": "existence",
      "statement": "A second protein activity must exist that limits fin growth when gained and suppresses the enlarger without lowering the enlarger's expression.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Lat4a (L-type amino acid transporter) T200K, allele nr21: dominant, gain-of-function (reverted by cis frameshift), shortens all fins, suppresses lof overgrowth in medial fins; kcnh2a mRNA not significantly changed in nr21 pectoral or dorsal fins.",
      "satisfied_evidence": "literature",
      "note": "Daane et al. 2021 (full-text). Effect of T200K on transport activity is unknown (no transport assay reported). qRT-PCR result is non-significance, group sizes not read (in figure)."},
    {"target_scale": "protein", "kind": "existence",
      "statement": "A factor that differs between paired and medial fins must gate whether the suppressor cancels the enlarger, and it cannot be differential transcript abundance of either the enlarger or suppressor gene.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Nothing found. Transcript level was examined and showed no difference: lat4a mRNA shows no significant difference across fins and genotypes, and kcnh2a mRNA is unchanged by nr21 in pectoral vs dorsal fins. Protein abundance, localisation or activity by fin type, and any candidate gate, have not been examined in the sources read.",
      "satisfied_evidence": "unknown",
      "note": "Daane et al. 2021 Fig 4D-E (full-text). Search scope: Daane 2021 full text; Stewart 2021 abstract; Europe PMC 'slc43a2a AND (fin OR zebrafish)' (3 hits, none relevant) and 'LAT4 SLC43A2 amino acid transporter system L Km' (no fin hits). Not searched: fin single-cell atlases, ZFIN expression (zfin.org HTTP 503), later citing papers. Transcript-level negative is 'looked, found nothing'; protein-level is 'nobody has looked' within this scope."},
    {"target_scale": "protein", "kind": "timescale",
      "statement": "The suppressor's protein activity must act during the enlarger's late outgrowth-prolonging window, not only during early outgrowth or patterning.",
      "quantity": "window of enlarger action in fin regeneration (days post-amputation)", "lo": 6, "hi": 30, "units": "dpa",
      "status": "open",
      "satisfied_by": "Enlarger side measured: WT and lof^t2 maximal growth rates indistinguishable at 3-5 dpa; WT outgrowth largely ceases by 21 dpa, lof^t2 continues through 30 dpa; astemizole from 6 or 7 dpa fully suppresses overgrowth. Suppressor side not measured: no timing, regeneration time course or temporal inhibition of Lat4a(T200K) found.",
      "satisfied_evidence": "unknown",
      "note": "Stewart et al. bioRxiv 10.1101/790329v3 (full-text via automated extractor, first ~100k of ~157k chars; quotes not hand-verified against PDF). Numbers are from regeneration; transfer to developmental growth is assumed. Suppressor-side negative scope: Daane 2021 full text only."},
    {"target_scale": "protein", "kind": "spatial",
      "statement": "The suppressor must act in, or within signalling range of, the intra-ray mesenchymal/fibroblast lineage in which the enlarger acts cell-autonomously.",
      "quantity": "distance between Lat4a-acting cells and Kcnh2a-acting cells", "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Enlarger compartment established (clone-autonomous in fibroblasts; tissue-autonomous in intra-ray mesenchyme). Suppressor compartment not reported: lat4a measured only in whole-fin homogenates; no in situ, reporter, single-cell, or autonomy test for nr21 found.",
      "satisfied_evidence": "unknown",
      "note": "Daane et al. 2021 (full-text); Stewart et al. 2021 (abstract). No numeric bound given because no measured ray or clone width was found to cite. Search scope as for the transcript-gate constraint; fin single-cell atlases not queried."}
  ]}
```
