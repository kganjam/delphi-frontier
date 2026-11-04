# Claim 211: what it requires at the DNA and cell scales, and whether those requirements hold

**Source claim (protein scale, evidence: measured).** Per-residue MSA depth, recomputed from the
committed `kcnk5b_pdb70.a3m` (72 sequences), is 21.4 mean over residues 1–250, 0.5 over 261–end,
and 0.0 from residue 326 on. The claim says this explains Boltz2's low confidence in that region.

**Adjacent scales checked:** `dna`, `cell`.

## 0. First, re-running the protein-scale numbers

The A3M is not on this branch. It is on `origin/swarm-architecture` at
`results/fish-proteins/structures/kcnk5b_pdb70.a3m`. I extracted it and recomputed the depth with a
short script. **This is a calculation from the committed file, not a new observation.** Depth at a
position = the number of non-query rows with a non-gap match state there. Lowercase insertions are
removed first, and the query row is not counted.

| quantity | claim 211 | my recomputation |
|---|---|---|
| rows | 72 | 72 (query + 71 hits) |
| query length | — | 448 |
| mean depth, residues 1–250 | 21.4 | 21.404 |
| mean depth, 261–448 | 0.5 | 0.521 |
| depth from 326 on | 0.0 | 0 (maximum over 326–448 is 0) |
| last residue covered by any hit | not stated | **311** |
| depth, residues 251–260 | not stated | 2 at every position |

The claim reproduces. Two refinements the claim does not state:

1. **Depth is zero from residue 312, not just from 326.** "0.0 from 326" is true, but it is the
   weaker version.
2. **Every position past 255 is covered by only two rows: `6WLV_A` and `6WM0_A`.** Those are the
   two mouse TASK2 cryo-EM entries. All other 69 hits end at or before residue 255 (my
   calculation). Li et al. 2020 (details in C4) report that only **amino acids 6–260** were modelled
   into those maps. So the two rows' alignment over query ~261–311 most likely comes from the
   deposited construct sequence, which spans residues 1–335, and not from residues with
   coordinates. This is my inference: I could not open the PDB entry files to check which residues
   are observed (`data.rcsb.org` was refused by this session's network proxy). If it holds, then
   from roughly residue 261 onward the PDB70 alignment supplies **no structural template at all**,
   which makes the claim's explanation stronger.

## 1. ENTAIL: what claim 211 requires

The claim is about information content, not about a physical process. It therefore implies no
timescale, energetic or conservation (mass, charge, momentum) requirement, and I have not
invented one to fill the list. It does imply the following.

| # | scale | kind | requirement (generic) |
|---|---|---|---|
| C1 | dna | existence | A transcribed coding sequence must exist that encodes the whole query, including the 137-residue segment (312–448) that no hit covers. Otherwise the zero-depth region could be a gene-model artefact rather than real protein. |
| C2 | dna | range | The annotated product of that coding sequence must have the same length as the query (448 aa) and the same sequence, so that the depth profile describes the real gene product. |
| C3 | cell | existence | A cellular context must exist in which the full-length protein, tail included, is expressed and functional. Otherwise "low confidence on the tail" describes a region the cell never makes. |
| C4 | cell | spatial | The position of the depth cliff must match, within a factor of about 1.1, the boundary between the membrane-embedded part of the channel (the part solved experimentally in an ortholog) and its cytoplasmic part (which was not solved). If depth explains confidence, the high-depth core and the solved core must be the same segment. |

C4 is stated as cell scale because the boundary in question is the membrane–cytoplasm interface.
It sits close to the protein/cell border, and I flag that rather than hide it.

## 2. CHECK

### C1 (dna, existence): **satisfied**

- UniProt **Q6PFU3** (zebrafish `kcnk5b`; ZFIN ZDB-GENE-040426-1297), "Evidence at transcript
  level". It is cross-referenced to **EMBL BC057416 (mRNA), protein AAH57416.1**, and to RefSeq
  NP_956927.1. I fetched the entry from `rest.uniprot.org` and compared its sequence with the A3M
  query row by string equality: **they are identical (448 aa)**. That comparison is my
  calculation; the mRNA record is a measured cDNA sequence. *Read-level: full-text (the UniProt
  flat-file record).*
- Perathoner et al. 2014, *PLoS Genet* 10:e1004080 (PMC3894163): "Full length kcnk5b was cloned
  into pGEM-T Easy from cDNA of fin blastema." The part I read gives no clone length or accession,
  so it shows that a full-length transcript exists in fin, but not that it is 448 codons.
  *Read-level: full-text (the first ~100k of 118k characters; the rest was not read).*

### C2 (dna, range: product length 448–448 aa): **satisfied**

- Q6PFU3 length is 448. A second UniProt entry, A0A8M1PBI1 ("Inferred from homology", RefSeq
  NP_956927.1), is also 448 aa with an identical sequence. I found no disagreement between them.
- **Scope of the check.** Only UniProt was queried, with `gene_exact:kcnk5b AND
  organism_id:7955`. Ensembl (`rest.ensembl.org`) was refused by the session proxy, so I have
  **not** checked whether Ensembl annotates alternative transcripts with a different C-terminus.
  Read-level for Ensembl: could-not-access.

### C3 (cell, existence: full-length protein expressed and functional in some cell): **satisfied, with the caveats stated**

- Perathoner et al. 2014 (full-text, partial). The authors report that full-length kcnk5b from fin
  blastema cDNA was subcloned into pSGEM and expressed in *Xenopus* oocytes, where wild-type and the
  *alf* mutants (W169L, F241Y) carry K⁺ current. The mutants show increased conductance and cell
  hyperpolarisation. By RT-PCR, the gene "is expressed in fins of adult fish".
- **Disagreement within that same source, kept as is.** In situ hybridisation on adult fins gave
  **no signal above background**, while RT-PCR detected expression. Transcript is present, but its
  cellular localisation in fin was not resolved by ISH in that paper.
- **Caveat (my inference).** Oocyte current and fin RT-PCR show that the full-length transcript is
  made and that the channel conducts. Neither shows that residues 312–448 are present in the mature
  protein in fin cells. No protein-level (proteomic or antibody) evidence for the zebrafish tail
  was searched for or found. Scope of that negative: I did not search for it, so this is "nobody
  checked here", not "looked and found nothing".
- **Related ortholog finding (authors' claim, mouse TASK2).** Li et al. 2020 (PMC8628578) report
  that the truncated TASK2(1–335) "retained the hallmark features of TASK2 when expressed in cells"
  and was "indistinguishable from full length TASK2" for responses to extracellular and
  intracellular alkalisation and to PIP2 (P > 0.05). So the tail is not needed for those gating
  properties in that assay. It does not follow that the tail has no function, and I did not check
  tail-specific functions such as G-protein modulation.

### C4 (cell, spatial: depth cliff matches the solved membrane core within ×1.1): **satisfied**

- **Measured (ortholog structure).** Li, Rietmeijer & Brohawn 2020, *Nature* 586:457–462
  (PMC8628578; *read-level: full-text, via a summarising fetch that quoted the sentences*):
  - "Amino acids 6-260 from each chain … corresponding to the transmembrane and extracellular
    regions" were modelled.
  - "The distal intracellular C-terminal region was not resolved, suggesting it is conformationally
    heterogenous or unstructured."
  - The construct was TASK2(aa1-335)-…-EGFP-His10, after "a truncation of the C-terminal 167 amino
    acids, which are predicted to be largely unstructured".
- **Predicted topology of the zebrafish query.** UniProt Q6PFU3 places TM4 at residues
  **229–250** (Phobius; a prediction, not a measurement) and a disordered region at **382–448**
  (MobiDB-lite; also a prediction).
- **Comparison (my calculation).** The depth cliff falls between residues 250 (end of predicted
  TM4) and 251, where depth drops to 2. The ortholog's solved region ends at 260. 260/250 = 1.04,
  inside the ×1.1 window. This assumes that mouse and zebrafish residue numbering roughly agree in
  this region. The A3M supports that: `6WLV_A` aligns from query residue 1 continuously, but I have
  not mapped mouse residue 260 to a zebrafish number exactly.
- **What this shows (my inference).** The high-depth segment is the membrane core that
  experiments have solved; the zero-depth segment is the cytoplasmic tail that the same experiment
  left out (residues 336 onward) or could not resolve (261–335). The low depth reflects the
  coverage of structure databases (truncated constructs, unresolved density), not the absence of
  homologous sequences. That fits claim 211, and it also points to an alternative or additional
  explanation for low Boltz2 confidence: genuine conformational heterogeneity, which the authors
  suggest. **Claim 211's evidence cannot tell "low depth" apart from "intrinsically disordered" as
  the cause.** Both predict low confidence, and the PDB70 depth is low *because* the region was
  either unresolved or truncated away. This is a confound in the explanation, not a refutation.

## 3. Summary

- No constraint is **unsatisfiable**. No measured number I found contradicts claim 211.
- C1–C4 are **satisfied**, with these scopes:
  - C2 was checked against UniProt only; Ensembl could not be accessed.
  - C3 has transcript and oocyte evidence, but no protein-level evidence for the tail.
  - C4 rests on predicted zebrafish TM boundaries and an ortholog structure.
- **New, stated precisely.** Coverage ends at residue **311**, not 326. Every position past 255 is
  covered by just two rows, and for those rows the mouse residues past 260 have no modelled
  coordinates. The explanation "depth is low, so confidence is low" is confounded with "the region
  is unresolved or disordered, so it is absent from structural databases". A deeper sequence-only
  MSA (UniRef or a colabfold-style search, rather than PDB70) would separate the two. That was not
  run here and remains **open**.

## Sources

| source | what was used | read-level |
|---|---|---|
| `origin/swarm-architecture:results/fish-proteins/structures/kcnk5b_pdb70.a3m` | depth recomputation | full-text |
| `origin/swarm-architecture:results/fish-proteins/structures/kcnk5b-HITS.md` | hit identities (6WLV/6WM0 = mouse TASK2) | full-text |
| UniProt Q6PFU3 and A0A8M1PBI1 (`rest.uniprot.org`) | length, sequence, EMBL/RefSeq cross-references, predicted TM and disorder | full-text (record) |
| Li, Rietmeijer & Brohawn 2020, *Nature* 586:457, PMC8628578 | construct 1–335, modelled residues 6–260, C-terminus unresolved, truncated construct indistinguishable from full length | full-text (fetched, quoted sentences) |
| Perathoner et al. 2014, *PLoS Genet* 10:e1004080, PMC3894163 | full-length cDNA from fin blastema, oocyte expression, RT-PCR vs ISH | full-text (first ~85%) |
| RCSB `data.rcsb.org` entries 6WLV, 6WM0 | observed-residue ranges | could-not-access (proxy refused) |
| Ensembl REST `kcnk5b` | alternative transcripts | could-not-access (proxy refused) |

```swarm-entail
{"source_claim": 211, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "A transcribed coding sequence must exist that encodes the full query, including the C-terminal segment (312-448) that has zero PDB70 coverage, so that the zero-depth region is real gene product and not an annotation artefact.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "EMBL BC057416 mRNA -> UniProt Q6PFU3 (transcript-level evidence), sequence identical to the A3M query over all 448 residues (string comparison by me); full-length kcnk5b cloned from fin blastema cDNA (Perathoner 2014).",
      "satisfied_evidence": "measured",
      "note": "UniProt Q6PFU3 record (full-text); Perathoner et al. 2014 PLoS Genet 10:e1004080, PMC3894163 (full-text, ~85% read). The Perathoner clone length is not given in the part read."},
    {"target_scale": "dna", "kind": "range",
      "statement": "The annotated product length of the coding sequence must equal the query length used for the depth profile.",
      "quantity": "annotated protein length", "lo": 448, "hi": 448, "units": "amino acids",
      "status": "satisfied",
      "satisfied_by": "UniProt Q6PFU3 = 448 aa and A0A8M1PBI1 (RefSeq NP_956927.1) = 448 aa, both with sequence identical to the query; no disagreement between them.",
      "satisfied_evidence": "literature",
      "note": "Scope: UniProt only (gene_exact:kcnk5b AND organism_id:7955). Ensembl REST refused by proxy (could-not-access), so alternative transcripts with a different C-terminus are not excluded."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "A cellular context must exist in which the full-length channel, tail included, is expressed and functional.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Full-length kcnk5b cDNA expressed in Xenopus oocytes carries K+ current (WT and alf W169L/F241Y gain-of-function); RT-PCR detects kcnk5b in adult fin.",
      "satisfied_evidence": "literature",
      "note": "Perathoner 2014, PMC3894163 (full-text, partial). Disagreement kept: in situ hybridisation in adult fin gave no signal above background, while RT-PCR detected expression. No protein-level evidence that residues 312-448 are present in fin cells; that was not searched (not looked), as opposed to looked and found nothing. Li 2020 reports truncated mouse TASK2(1-335) indistinguishable from full length for pH and PIP2 gating in cells."},
    {"target_scale": "cell", "kind": "spatial",
      "statement": "The depth cliff must coincide, within a factor of about 1.1, with the boundary between the experimentally solved membrane-embedded core and the unsolved cytoplasmic region of the channel.",
      "quantity": "ratio of ortholog solved-region end to query depth-cliff position", "lo": 0.91, "hi": 1.1, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Depth cliff after query residue 250 (end of Phobius-predicted TM4, 229-250); mouse TASK2 cryo-EM modelled residues 6-260 only, distal C-terminus not resolved, construct truncated at 335. 260/250 = 1.04 (my calculation).",
      "satisfied_evidence": "derived",
      "note": "Li, Rietmeijer & Brohawn 2020 Nature 586:457, PMC8628578 (full-text via quoted fetch). Zebrafish TM boundaries are predicted (Phobius), not measured; exact mouse-to-zebrafish residue mapping was not done. Confound: low depth and unresolved/disordered tail are not separable with PDB70 alone; a UniRef-depth MSA would separate them (open, not run). RCSB observed-residue ranges could-not-access."}
  ]}
```
