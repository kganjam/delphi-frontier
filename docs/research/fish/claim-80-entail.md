# Claim 80: entailment at the adjacent scale (`dna` → `protein`)

**Source claim (scale `dna`, evidence: derived).**
"lat4a = slc43a2a, resolved by the paper's OWN MAPPING rather than name similarity: Daane et al. map
nr21 to chromosome 15, and of the two zebrafish SLC43A2 paralogs slc43a2a is on chr15 while slc43a2b
is on chr10. LAT4 is the protein name of SLC43A2."

**Adjacent scale:** `protein`. **Date of all reads:** 2026-11-04.

**Subject on both sides of every comparison.** Every constraint below is about the **zebrafish**
(*Danio rerio*) slc43a2a/slc43a2b products. The only other organism used is **human** (SLC43A1/2/3),
and only as an orthology reference, never as a measurement that could refute a zebrafish claim. I used
**no flying-fish (exocoetid) numbers**. No constraint is marked `unsatisfiable`.

## Sources and read-levels

| Source | Used for | Read-level |
|---|---|---|
| Daane JM et al. 2021, *Curr Biol* 31:5052, doi:10.1016/j.cub.2021.08.054, PMID 34534441, PMC9172250 (NCBI efetch, db=pmc) | nr21 → chr15; "nonsynonymous mutation (T200K) in a conserved domain of … lat4a"; gain-of-function; cis frameshift reverts; lat4a nulls show no fin phenotype | full-text (author manuscript main text; figures and supplement **not** seen) |
| UniParc UPI000188A62B (xref Ensembl ENSDARP00000120945, gene slc43a2a, 571 aa) and UPI00062E34B4 (xref ENSDARP00000138218, 577 aa) | full-length chr15 product | full record (sequence and xrefs) |
| NCBI Protein NP_001008585.1 (slc43a2b, 592 aa); UniProt Q5PR35 (slc43a2b, 592 aa) | chr10 paralog | full record (sequence) |
| UniProt Q7ZUS0 (slc43a2a, 153 aa) | short product | full record |
| UniProt Q8N370 (LAT4_HUMAN, SLC43A2, 569 aa), O75387 (LAT3_HUMAN, SLC43A1, 559 aa), Q8NBI5 (SLC43A3, 491 aa) | orthology references; TM annotation; function comment | full record (JSON/FASTA) |
| NCBI Gene esummary 393221 / 494042 | slc43a2a chr15 (NC_141035.1); slc43a2b chr10 (NC_141030.1); a symbol search `slc43a2*[sym] AND Danio rerio[orgn]` returns exactly these two | listing (E-utilities) |
| Dong Z et al. 2026, *Integr Zool* 21:1425, doi:10.1111/1749-4877.13018, PMID 40689752 | only other lat4a fin paper found | **abstract** (the PMC record holds no body text) |
| Prior repo work: challenge-80, challenge-292, challenge-186, claim-185-entail (branches on origin) | context only; every number below was re-derived here | full-text (repo) |

Alignments are **my own calculations** (Biopython PairwiseAligner, global, BLOSUM62, gap open −10,
extend −0.5). The script is `docs/research/fish/claim-80-entail-aln.py`. None of the numbers it
produces is an observation.

---

## 1. ENTAIL: what claim 80 requires at `protein`

If the nr21 lesion is in slc43a2a, and slc43a2a is LAT4, then at protein scale:

| id | kind | requirement (generic) |
|---|---|---|
| C1 | existence | The chr15 gene's product must carry the paper's wild-type residue (Thr) at the paper's position 200. The chr10 paralog's own numbering must **not** put that residue at 200, or else the position stops telling the paralogs apart. |
| C2 | spatial | Some product of the chr15 gene must be long enough to be a full-length LAT4-family transporter: within a factor ~1.3 of human SLC43A2 (569 aa), i.e. **427–740 aa**. A product shorter than ~200 aa cannot carry residue 200 at all. |
| C3 | range | "LAT4 is the protein name": the chr15 product must be closer to human SLC43A2 (LAT4) than to its nearest paralog SLC43A1 (LAT3). Bounded quantity: identity to LAT4 minus identity to LAT3, **> 0 percentage points**. |
| C4 | range | "A conserved domain": the 15-residue window centred on position 200 must align to human SLC43A2 at **≥ 0.6 identity** (this threshold is my operationalisation, an `assumed` cut-off, not something from the paper), and the aligned human residue must be Thr. |
| C5 | existence | The paper calls nr21 gain-of-function (a cis frameshift reverts it, and nulls have no fin phenotype). So the T200K form of the chr15 product must have a property the wild-type product lacks, and that property should be detectable at protein level (transport, localisation, stability, or a binding partner). |

---

## 2. CHECK

### C1: existence, T at position 200 in the chr15 product only: **satisfied** (with a refinement)

These are database gene models read directly. The positional arithmetic is mine.

| product | chromosome (NCBI Gene) | residue 200 | window 195–205 |
|---|---|---|---|
| slc43a2a, ENSDARP00000120945 (571 aa) | 15 | **T** | `ASSAV[T]FPGIK` |
| slc43a2a, ENSDARP00000138218 (577 aa) | 15 | **T** | same |
| slc43a2b, NP_001008585.1 / Q5PR35 (592 aa) | 10 | **M** | `LTLPN[M]FGDLR` |

**Refinement, not stated by claim 80 or challenge 80 (my alignment):** the residue *homologous* to
slc43a2a T200 is **also Thr in slc43a2b**. It sits at slc43a2b position **222**, in the window
`SYASSAVTFPGVKVI`. slc43a2b carries an extra ~22 residues upstream (my inference from the alignment
offset). So the *amino acid* does not tell the paralogs apart. Only the *number* does: in slc43a2b
numbering, the paper's mutation would have been called T222K, not T200K. That means C1 discriminates
only if the paper numbered against a slc43a2a-like sequence. The paper does not state its reference
accession (full-text). The chromosome-15 argument, which is the claim's actual basis, does not depend
on this. C1 is satisfied as consistent, independent support. It is not a second proof.

### C2: spatial, full-length product exists: **satisfied by the Ensembl gene models; failed by the RefSeq/UniProt record**

- ENSDARP00000120945: 571 aa, ratio to human SLC43A2 (569 aa) **1.00**. ENSDARP00000138218: 577 aa,
  ratio **1.01**. Both are inside 427–740 aa.
- Q7ZUS0 / NP_956545.1: 153 aa, ratio **0.27**. This is outside the window and cannot carry residue
  200, as already established in claim 185 and challenge 292.

Scope of the "satisfied": the satisfying records are **computational gene models** (Ensembl
annotation, reached via UniParc). They are not a measured protein. I did **not** search proteomics
resources (PRIDE, PeptideAtlas) for peptides beyond residue 139, so the full-length product's
existence *as a protein* is unmeasured within my scope. This does not refute claim 80. The 153-aa
record is a property of one annotation, not of the gene's chromosome.

### C3: range, closer to LAT4 than LAT3: **satisfied** (my calculation)

| query (zebrafish) | vs human SLC43A2 (LAT4) | vs human SLC43A1 (LAT3) | vs human SLC43A3 | LAT4 − LAT3 |
|---|---|---|---|---|
| slc43a2a, chr15 (571 aa) | 442/563 = **78.5%** | 323/539 = **59.9%** | 162/460 = 35.2% | **+18.6 pp** |
| slc43a2b, chr10 (592 aa) | 433/563 = 76.9% | 324/540 = 60.0% | 159/459 = 34.6% | +16.9 pp |

Identity is computed over aligned columns. The chr15 product is clearly a LAT4 (SLC43A2) orthologue,
so the claim's clause "LAT4 is the protein name of SLC43A2" holds for it. Scope: this constraint
confirms the *family* assignment. It does **not** discriminate a from b, since both pass it by similar
margins. That job is done by the chromosome mapping (DNA scale) and partly by C1.

### C4: range, position 200 sits in a conserved region: **satisfied** (my calculation; threshold assumed)

| target | aligned residue | 15-residue window identity |
|---|---|---|
| human SLC43A2 | **T193** (`SYASSAVTFPGIKLI`) | **14/15 = 0.93** |
| human SLC43A1 | T181 | 13/15 = 0.87 |
| zebrafish slc43a2b | T222 | 14/15 = 0.93 |
| human SLC43A3 (outgroup) | V172 | 5/15 = 0.33 |

The window passes the 0.6 cut-off, and the human orthologous residue is Thr. In UniProt Q8N370, human
T193 lies at the C-terminal end of the annotated helix **177–197**, with the next helix at 203–223. That
annotation's evidence code is ECO:0000255 (sequence-analysis prediction), not a structure. So "in a
transmembrane helix" is predicted, not observed. This agrees with the paper's "conserved domain"
(author's claim). The cross-family conservation inside SLC43A1/2 and its loss in SLC43A3 is my
inference from these four alignments only.

### C5: existence, a protein-level gain-of-function property of T200K: **unsatisfied (nobody has measured it, within scope)**

What the paper shows (full-text): nr21 is dominant; frameshift mutations made *in cis* revert the fin
phenotype to wild type; lat4a-null fish have no fin phenotype. The authors conclude "gain-of-function"
from this. That is a genetic inference. It is not a protein measurement.

What I searched:
- PubMed `(slc43a2 OR lat4) AND zebrafish`: 2 hits. Both are unrelated to T200K (PMID 38388846, a
  teleost T-cell paper; PMID 23268354, a SLC43 family review).
- PubMed `(slc43a2a OR lat4a OR nr21) AND (fin OR zebrafish)`: 2 hits, Daane 2021 and Dong 2026.
- One web search for T200K transport activity: no assay found (search-summary).

Result: I found **no transport assay, localisation, stability or interaction measurement of
zebrafish Lat4a T200K**. This is "nobody has looked, as far as this scope reaches". It is **not**
"people looked and found nothing", so it says nothing against claim 80.

Note on Dong et al. 2026 (abstract only). The authors report "a convergent amino acid change in the
lat4a gene shared by syngnathids and some flying fishes, with in vitro analysis confirming its role in
fin size evolution". The subjects are **syngnathids and flying fishes, not zebrafish**. The residue,
the assay and whether it is T200K are all **unknown**, because I could not read the body. It may bear
on C5, but it cannot satisfy C5 for the zebrafish nr21 allele, and I have not counted it.

---

## Summary

- Four of five protein-scale requirements are met by named zebrafish records, checked against human
  orthologues:
  - C1: T200 exists in slc43a2a and not at position 200 in slc43a2b.
  - C2: a full-length 571/577-aa model exists.
  - C3: the product is closer to LAT4 than LAT3 by +18.6 pp.
  - C4: position 200 is in a 14/15-conserved window, aligned to human T193.
- Two of these come with scope limits that should travel with them:
  - C1 discriminates by **numbering only**, because the homologous residue is Thr in both paralogs.
  - C2 rests on **gene models**, not measured protein.
- C5, the protein-level gain-of-function property the paper's genetics imply, is unmeasured within my
  search scope.
- Nothing contradicts claim 80 at protein scale.

```swarm-entail
{"source_claim": 80, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "The chr15 gene product must carry the paper's wild-type residue (Thr) at the paper's numbered position 200, and the chr10 paralog's own numbering must not place that residue at 200",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "slc43a2a Ensembl models ENSDARP00000120945 (571 aa) and ENSDARP00000138218 (577 aa) have T200 (window ASSAVTFPGIK); slc43a2b NP_001008585.1/Q5PR35 has M200. Caveat: the homologous Thr is also present in slc43a2b, at its position 222, so only the numbering discriminates the paralogs, and the paper does not state its reference accession",
      "satisfied_evidence": "derived",
      "note": "Zebrafish on both sides. Sequences from UniParc UPI000188A62B/UPI00062E34B4 and NCBI NP_001008585.1 (full record, read 2026-11-04); positional alignment is my calculation; Daane et al. 2021 Curr Biol PMC9172250 (full-text) for T200K"},
    {"target_scale": "protein", "kind": "spatial",
      "statement": "Some product of the chr15 gene must be a full-length LAT4-family transporter, within a factor ~1.3 of the human SLC43A2 length",
      "quantity": "product length", "lo": 427, "hi": 740, "units": "amino acids",
      "status": "satisfied",
      "satisfied_by": "Ensembl gene models ENSDARP00000120945 (571 aa, ratio 1.00) and ENSDARP00000138218 (577 aa, ratio 1.01) versus human Q8N370 (569 aa). The RefSeq/UniProt record NP_956545.1/Q7ZUS0 (153 aa, ratio 0.27) does not meet it",
      "satisfied_evidence": "literature",
      "note": "Satisfying records are computational gene models, not a measured protein; proteomics resources (PRIDE, PeptideAtlas) were not searched. Zebrafish product vs human length reference"},
    {"target_scale": "protein", "kind": "range",
      "statement": "The chr15 product must be closer in sequence to the LAT4 orthologue (SLC43A2) than to its nearest paralog family member LAT3 (SLC43A1)",
      "quantity": "percent identity to human SLC43A2 minus percent identity to human SLC43A1", "lo": 0, "hi": null, "units": "percentage points",
      "status": "satisfied",
      "satisfied_by": "slc43a2a (571 aa): 78.5% identity to human SLC43A2 vs 59.9% to SLC43A1, a difference of +18.6 pp; 35.2% to SLC43A3",
      "satisfied_evidence": "derived",
      "note": "My global BLOSUM62 alignments (script docs/research/fish/claim-80-entail-aln.py) of UniProt/UniParc sequences read 2026-11-04. Confirms the family assignment only: slc43a2b also passes (+16.9 pp), so this does not discriminate the paralogs"},
    {"target_scale": "protein", "kind": "range",
      "statement": "The site of the mutation must lie in a region conserved across LAT4 orthologues: the 15-residue window centred on position 200 aligns to the human orthologue at identity >= 0.6, and the aligned human residue is Thr",
      "quantity": "15-residue window identity to human SLC43A2", "lo": 0.6, "hi": 1.0, "units": "fraction identical",
      "status": "satisfied",
      "satisfied_by": "Window SYASSAVTFPGIKVI aligns to human SLC43A2 SYASSAVTFPGIKLI at 14/15 = 0.93; the aligned human residue is T193, at the end of UniProt-predicted helix 177-197 (ECO:0000255). For comparison: SLC43A1 13/15, SLC43A3 5/15",
      "satisfied_evidence": "derived",
      "note": "The 0.6 cut-off is my assumed operationalisation of the paper's 'conserved domain' (Daane 2021, full-text). The TM placement is a sequence-analysis prediction, not a structure. Zebrafish vs human"},
    {"target_scale": "protein", "kind": "existence",
      "statement": "The T200K form of the chr15 product must have a protein-level property the wild-type form lacks (transport, localisation, stability or a binding partner), consistent with the genetic gain-of-function call",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "No transport, localisation, stability or interaction measurement of zebrafish Lat4a T200K was found. Searched: PubMed '(slc43a2 OR lat4) AND zebrafish' (2 unrelated hits), PubMed '(slc43a2a OR lat4a OR nr21) AND (fin OR zebrafish)' (Daane 2021, Dong 2026), and one web search (search-summary). This is 'nobody has measured it', not 'measured and found nothing'",
      "satisfied_evidence": "unknown",
      "note": "Gain-of-function is the authors' genetic inference (dominance, cis-frameshift reversion, null has no phenotype; Daane 2021 full-text). Dong et al. 2026 Integr Zool PMID 40689752 (abstract only) reports in vitro analysis of a convergent lat4a change in syngnathids and flying fishes. That is a different subject and an unknown residue and assay, so it is not counted"}
  ]}
```
