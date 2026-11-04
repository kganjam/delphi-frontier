# Claim 30: what it requires at the dna and cell scales

**Source claim.** Claim 30. Scale: protein. Evidence: derived.

> Tyrosine spatial clustering is significant in and2 (0.393 observed vs 0.211 shuffled, z=2.74, p=0.011) but
> NOT in and1 (p=0.064, where Tyr content alone explains most of it); kcnk5b control p=0.72

**Subject of the claim.** Zebrafish, *Danio rerio*. The proteins are the and2 precursor (UniProt A9JRX1 =
A0ACM8QEN9 = RefSeq NP_001104660.1, 508 aa, 29 Tyr) and the and1 precursor (UniProt E7F5V5, 570 aa, 47 Tyr).

**What the statistic is.** The claim never defines it. Two replications and one challenge reconstructed it the
same way (`replicate-30.md` on branches `claude/replicate-30-tyrosine-q48jq0` and
`claude/tyrosine-clustering-replication-tx87zl`, and `challenge-30.md` on `claude/tyrosine-clustering-challenge-p9fma6`;
all three read in full this session):
- the statistic is the fraction of consecutive Tyr–Tyr gaps that are ≤ 4 residues;
- the null is a composition-preserving full-sequence shuffle;
- and2 scores 11/28 = 0.393 and and1 scores 18/46 = 0.391.

The challenge rated the claim **weakened**. Its reasons: the result depends on the threshold, the and1/and2
contrast is not a tested difference, and kcnk5b is underpowered as a control. I do not redo that work. I take the
claim as stated and ask what has to hold one scale down (the gene) and one scale up (the cell) for it to be a true
statement about a zebrafish protein.

**The animal on both sides.** Every measurement and record used below is from *Danio rerio*. No flying-fish
(Exocoetidae) number is used anywhere in this document. For that reason none of the verdicts below runs into the
cross-species problem.

**Labels.**
- **computed**: arithmetic or a permutation test I ran this session on public sequence records. It is not an
  observation.
- **measured**: reported by the cited authors from experiments.
- **predicted**: a computational annotation made by someone else, such as SignalP.
- **author's claim / my inference**: kept apart in each sentence where both appear.

## Sources and read-levels

| Source | Animal | Used for | Read-level |
|---|---|---|---|
| RefSeq NM_001111190.1 / NP_001104660.1 (and2 mRNA and protein). PROVISIONAL, "derived from BC155829.1"; exon support BC155829.1 and EH579653.1 | *D. rerio* | exon/CDS structure and the protein analysed | full-text (GenBank flat file and FASTA, NCBI E-utilities, fetched 2026-11-04) |
| UniProt A9JRX1 (EMBL BC155829 mRNA; "Evidence at transcript level") and A0ACM8QEN9 (sourced from NP_001104660.1) | *D. rerio* | signal peptide annotation (SignalP: 1–23; chain 24–508) | full-text (UniProt JSON) |
| Genomic and2 locus in three assemblies: GRCz11 NC_007113.7 c31767651–31763200 (strain Tübingen); GRCz12tu NC_133177.1 c34736892–34732441 (Tübingen); GRCz13ab NC_141022.1 c35126006–35121555 (strain M-AB). Coordinates from NCBI Gene 566702 location history | *D. rerio* | whether the genome encodes the analysed CDS | full-text (sequence, NCBI efetch) |
| RefSeq NP_001184183.2 (and1; VALIDATED, "derived from genomic sequence", JBMGRA010000024.1) and UniProt E7F5V5 | *D. rerio* | whether the and1 statistic depends on which gene model is used | full-text (FASTA) |
| König D, Page L, Chassot B, Jaźwińska A 2018, *Dev Biol*, doi 10.1016/j.ydbio.2017.07.024, PMID 28760345 | adult *D. rerio*, regenerating caudal fin | And2 protein in cells | abstract |
| Hanzelova P, Baird C, Keshinro B, Kadhom R, Lalonde RL, Akimenko M-A 2026, *Development*, doi 10.1242/dev.204990, PMC13120675 | *D. rerio* embryos, larvae and adults | and2 transcription in fin-fold cells; single-mutant phenotype | full-text (Europe PMC XML; keyword passages read, not every section) |
| Zhang J et al. 2010, *Nature*, doi 10.1038/nature09137, PMID 20574421 | *D. rerio* | And1/And2 as structural components of actinotrichia (elastoidin) | abstract |
| Nolte H et al. 2015, *Proteomics*, doi 10.1002/pmic.201400316, PMID 25504979 | adult *D. rerio* fin | MS detection of "two actinodin family members" | abstract (does not say which two) |
| Kimura S & Kubota M 1969, *J Biochem*, doi 10.1093/oxfordjournals.jbchem.a128981, "Tyrosine derivatives in a structural protein, elastoidin" | **unknown**: the listing does not name the species | context only | listing (no abstract on Europe PMC) |

The script is `docs/research/fish/claim30_and2_genome_check.py`. To run it, put the NCBI FASTA files in a
directory: `nm.fa`, which is NM_001111190.1, and `g_<accession>.fa`, which is each genomic range above fetched
with `strand=2`. Then run `python3 -I claim30_and2_genome_check.py <dir>`.

---

## DNA scale

### D1 (existence). A genomic locus must exist whose spliced coding sequence translates to exactly the analysed protein, with the analysed Tyr positions. **SATISFIED**

**Why the claim requires it.** The 0.393 / p = 0.011 figure belongs to one specific 508-aa sequence. Suppose
that sequence came from a mis-assembled cDNA, or from a gene model that the genome does not support. The claim
would then describe a sequence the animal does not encode.

**Check (computed from measured sequence records).**
- I took the five exons of NM_001111190.1 (mRNA coordinates 1–71, 72–146, 147–191, 192–319, 320–2006; CDS
  92–1618) and searched for each one in the and2 genomic region of three assemblies.
- In all three assemblies, every exon is an **exact, colinear, gap-free match**: GRCz11 (Tübingen), GRCz12tu
  (Tübingen) and GRCz13ab (M-AB).
- The one exception is base 1 of the mRNA, which is 5′ UTR. That leaves the CDS unaffected.
- The genomic offsets, in gene orientation, are 0, 818, 1456, 1915 and 2764 in all three.
- So the genome-encoded CDS is identical to the CDS the claim analysed: 508 aa, 29 Tyr, 11 of 28 gaps ≤ 4.
- Re-running the permutation (20 000 shuffles, computed) gives p = 0.0104.

**Independence.**
- The cDNA BC155829 and the genome assemblies are independent sequencing products. GRCz13ab also comes from a
  different laboratory strain (M-AB) than the two Tübingen assemblies.
- They are **not** independent of the RefSeq annotation pipeline, which placed the gene model on each assembly.
- The exact matching was my own computation, so it does not rely on that annotation.

**and1 (the other half of the claim), computed.**
- UniProt E7F5V5 and RefSeq NP_001184183.2 differ at four positions: L45I, P49T, A143V and I353S (E7F5V5 → RefSeq).
- None of those positions is a Tyr.
- Both models therefore give 47 Tyr and 18 of 46 gaps ≤ 4, so the and1 statistic does not depend on which model
  is used.
- I did not align and1 to the genome myself. The RefSeq note says its sequence "was derived from genomic sequence"
  (JBMGRA010000024.1).

**What this does not show.** It shows only that the reference haplotypes encode the sequence. D2 covers the
population.

### D2 (range). Across natural and2 alleles, the number of consecutive Tyr gaps ≤ 4 aa must stay in [10, 28]. In practice that means at most one of the 11 close Tyr pairs can be lost to polymorphism. **OPEN**

**Why the claim requires it (computed).**
- The claim is about the zebrafish protein, not about one clone.
- I computed how the and2 shuffle null (50 000 shuffles, and2 composition held fixed) responds to the count of
  close gaps out of 28:

| close gaps / 28 | fraction | one-sided p (computed) |
|---|---|---|
| 12 | 0.429 | 0.0028 |
| 11 (reference) | 0.393 | 0.011 |
| 10 | 0.357 | 0.035 |
| 9 | 0.321 | 0.092 |
| 8 | 0.286 | 0.20 |

- If a common allele carried a missense change at a Tyr codon in two close pairs, the claim would fail for that
  allele.
- This is an approximation, and that is my inference. Losing a Tyr also changes the gap count, and I held that
  count at 28.
- The bound is therefore lo = 10 close gaps.

**What was checked.**
- Three reference haplotypes from two strains (D1) all carry 11. They satisfy the bound.
- The two and1 gene models differ at four residues, so allelic variation clearly exists in this gene family. This
  is my inference from D1. None of those differences touches a Tyr.

**What was not checked.**
- I did not query any population variant resource, such as EVA or ZFIN mutation and SNP records, for missense
  variants at the 29 and2 Tyr codons (positions 55, 65, 84, 87, 103, 111, 151, 155, 158, 195–197, 227, 233, 235,
  245, 257, 271, 274, 334, 351, 354, 389, 392, 395, 459, 490, 502, 506).
- Ensembl REST was blocked by this session's network proxy (HTTP 403).
- So this is **"not looked at by me"**, not "looked and found nothing". It stays open.

---

## Cell scale

### C1 (existence). A cell population in the zebrafish must transcribe and2 and translate it into a protein that enters the secretory pathway. **SATISFIED**

**Why the claim requires it.** A statement about the spatial organisation of a protein's residues is about a
protein. If and2 were a pseudogene or never translated, the claim would describe a conceptual translation, not a
zebrafish protein.

**Satisfied by:**
- **Transcript, measured.** Hanzelova et al. 2026 (full-text) reports by in situ hybridisation: "At 2 days post
  fertilization (dpf), and1 and and2 are both strongly expressed in the developing pectoral and median FF [fin
  fold] of wild-type embryos". The animal is *D. rerio* embryos.
- **Protein, measured.** König et al. 2018 (abstract), using immunofluorescence on regenerating fins of adult
  *D. rerio*: "Both proteins [And1/2] were detected in the secretory organelles in the mesenchymal cells of the
  blastema, but only And1 was detected in the epithelial cells of the wound epithelium."
- **Supporting evidence.** Zhang et al. 2010 (abstract) calls And1 and And2 "essential structural components of
  elastoidin", which is the material of actinotrichia.
- Nolte et al. 2015 (abstract) detected "two actinodin family members" by MS at the actinotrichia. The abstract
  does not say which two, so I do not count it as And2-specific evidence.

**Caveats.**
- I read König 2018 at abstract level only, so I have not seen how the And2 antibody was validated.
- Hanzelova 2026 cites König 2018 as having validated the **And1** antibody. The passages I read do not mention
  an And2 antibody.

### C2 (spatial). The signal-peptide cleavage site must lie N-terminal to the first Tyr, so that the clustered Tyr pattern is carried into the mature, secreted chain. Bound: first Tyr position − cleavage site ≥ 1 residue. **SATISFIED (from a prediction, not a measured N-terminus)**

**Why the claim requires it.** The protein the cell exports is the mature chain. Suppose Tyr residues were
removed with the signal peptide. The precursor statistic would then not describe the secreted protein.

**Check.**
- UniProt annotates a signal peptide at 1–23 and a chain at 24–508. That annotation is **predicted** by SignalP,
  not measured.
- The first Tyr is at position 55 (computed), which gives a margin of 32 residues.
- The challenge also found that excluding residues 1–20 leaves and2 at p = 0.014 (computed, `challenge-30.md`).

**Scope.** No experiment that I found has determined the N-terminus of mature And2 (see C3). The verdict rests on a
prediction with a 32-residue margin. I label the evidence `derived` for that reason, not `measured`.

### C3 (existence). Between the cell and the fibre, no further proteolytic processing may remove or separate the Tyr-dense segments. The clustered pairs sit at residues 151–158, 195–197, 233–235, 271–274, 351–354, 389–395 and 502–506. **OPEN: nobody appears to have looked**

**Why the claim requires it.** A protein-scale claim about Tyr spacing has a cell-scale meaning only if those
segments stay on the same chain once secreted and deposited. My inference: if the protein were cleaved inside the
308–389 region, the statistic for each fragment would be different.

**What I searched.** Europe PMC, 2026-11-04:
- `actinodin AND (cleavage OR proteolytic OR "mass spectrometry" OR proteomic)` returned 6 hits.
- `actinodin` alone returned 46 hits; I scanned the titles.

None of the titles or abstracts I read reports how And2 is processed, its mature mass, or a peptide map. This is a
scoped negative at abstract and title level. I did not read the full texts of Zhang 2010 or Nolte 2015, and either
could contain a western blot showing the mature size.

---

## Not entailed, and kept out on purpose

- **Di-Tyr crosslinking.** It is an interpretation of the claim and is not required by it. The challenge already
  noted that linear spacing is neither necessary nor sufficient for 3D Tyr proximity.
  - Older literature is relevant here. Hanzelova 2026, full-text: elastoidin is "a complex containing collagen and
    a tyrosine-rich non-collagenous compound (Krukenberg, 1885; Gross and Dumsha, 1958)".
  - Kimura & Kubota 1969, which I have only as a listing, has the title "Tyrosine derivatives in a structural
    protein, elastoidin". I could not see which animal it studied, and elastoidin was classically studied in shark
    fins.
  - Neither source is about zebrafish And2's sequence spacing, so neither checks this claim.
- **A function for the clustering.** Hanzelova 2026 (full-text) reports that "Adult single mutants had no
  observable fin defects" and that only and1/and2 double mutants lose actinotrichia.
  - My inference: whatever the and2 Tyr spacing does, it is not individually required for adult fin form under
    lab conditions.
  - The claim makes no functional statement, so this is context and not a constraint.
- **Conservation across species.** This would be required only if the claim asserted selection. It does not.

## Summary

| # | Scale | Kind | Status | Basis |
|---|---|---|---|---|
| D1 | dna | existence | satisfied | computed exact match of the CDS in 3 assemblies and 2 strains; and1 models agree on all Tyr |
| D2 | dna | range | open | reference haplotypes carry 11 close gaps (≥ 10 needed); population variants not searched |
| C1 | cell | existence | satisfied | and2 ISH in fin fold (Hanzelova 2026); And2 protein in blastema mesenchyme secretory organelles (König 2018, abstract) |
| C2 | cell | spatial | satisfied (predicted) | SignalP 1–23 versus first Tyr at 55 |
| C3 | cell | existence | open | And2 processing unreported in the literature I searched |

No constraint is unsatisfiable. No measured value at the dna or cell scale contradicts claim 30. That is a weak
result, because the claim is a statistical statement about one sequence and asks little of the scales around it.
The challenge's objections (threshold choice, the untested and1-vs-and2 contrast, and the underpowered control)
are all protein-scale, and nothing found here repairs or worsens them.

```swarm-entail
{"source_claim": 30, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "A genomic locus must exist whose spliced CDS translates to exactly the analysed and2 protein (508 aa, 29 Tyr, 11/28 consecutive Tyr gaps <=4 aa); likewise the and1 Tyr pattern must not depend on which gene model is used",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "All five NM_001111190.1 exons match exactly and colinearly (CDS identical) in the D. rerio and2 locus of GRCz11 (NC_007113.7, Tuebingen), GRCz12tu (NC_133177.1, Tuebingen) and GRCz13ab (NC_141022.1, M-AB); recomputed and2 statistic 11/28, p=0.0104 (20000 shuffles). and1: E7F5V5 vs NP_001184183.2 differ at 4 non-Tyr residues (L45I, P49T, A143V, I353S), Tyr statistic identical (18/46)",
      "satisfied_evidence": "derived",
      "note": "Computed this session from NCBI/UniProt sequence records (full-text), fetched 2026-11-04; script docs/research/fish/claim30_and2_genome_check.py. Zebrafish on both sides. Shows the reference haplotypes only; and1 not aligned to the genome by me (RefSeq says it was derived from JBMGRA010000024.1)."},
    {"target_scale": "dna", "kind": "range",
      "statement": "Across natural and2 alleles the number of consecutive Tyr gaps <=4 aa must remain at or above the level that keeps the shuffle test significant, i.e. at most one of the 11 close Tyr pairs may be lost to polymorphism",
      "quantity": "close (<=4 aa) consecutive Tyr gaps out of 28 in the and2 protein", "lo": 10, "hi": 28, "units": "gaps",
      "status": "open",
      "satisfied_by": "Three reference haplotypes (2 strains) carry 11 (computed). Threshold computed: 10/28 gives p=0.035, 9/28 gives p=0.092 (50000 shuffles, gap count held at 28, an approximation). No population variant data searched",
      "satisfied_evidence": "derived",
      "note": "Not searched: EVA / ZFIN variant records for missense at and2 Tyr codons; Ensembl REST blocked (HTTP 403) in this session. This is 'not looked at', not 'looked and found nothing'."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "A zebrafish cell population must transcribe and2 and translate it into a protein that enters the secretory pathway",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "and2 mRNA strongly expressed in pectoral and median fin fold at 2 dpf by ISH (Hanzelova et al. 2026); And1/2 protein detected in secretory organelles of blastema mesenchymal cells of regenerating adult fin by immunofluorescence (Koenig et al. 2018)",
      "satisfied_evidence": "measured",
      "note": "Hanzelova P et al. 2026 Development doi 10.1242/dev.204990 (full-text, keyword passages); Koenig D et al. 2018 Dev Biol doi 10.1016/j.ydbio.2017.07.024 (abstract; And2 antibody validation not seen). Zhang et al. 2010 Nature doi 10.1038/nature09137 (abstract) supports And2 as an elastoidin component. All D. rerio."},
    {"target_scale": "cell", "kind": "spatial",
      "statement": "The signal-peptide cleavage site must lie N-terminal to the first Tyr so the clustered Tyr pattern is carried into the mature secreted chain",
      "quantity": "first Tyr position minus signal-peptide cleavage position", "lo": 1, "hi": null, "units": "residues",
      "status": "satisfied",
      "satisfied_by": "SignalP signal peptide 1-23 (UniProt A9JRX1/A0ACM8QEN9 annotation) vs first Tyr at residue 55: margin 32 residues; challenge-30 found excluding 1-20 leaves p=0.014",
      "satisfied_evidence": "derived",
      "note": "Cleavage site is a computational prediction, not a measured N-terminus; no experimental And2 N-terminus found (see next constraint's search scope)."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "No further proteolytic processing between secretion and fibre deposition may remove or separate the Tyr-dense segments of the mature chain",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Nothing found either way: no report of And2 processing, mature mass or peptide map",
      "satisfied_evidence": "unknown",
      "note": "Searched Europe PMC 2026-11-04: 'actinodin AND (cleavage OR proteolytic OR \"mass spectrometry\" OR proteomic)' (6 hits) and 'actinodin' (46 hits), titles/abstracts only. Full texts of Zhang 2010 and Nolte 2015 (Proteomics doi 10.1002/pmic.201400316) not read and could contain a western blot. Status is 'nobody appears to have looked', scoped to abstracts."}
  ]}
```
