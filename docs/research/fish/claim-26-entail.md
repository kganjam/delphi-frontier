# Claim 26 — entailment to the `dna` and `cell` scales

**Source claim (protein scale, evidence: derived):**
> An MSA-dependent model's confidence tracks ALIGNMENT DEPTH, not disorder: PDB70 depth falls
> to 0.0 from residue 326 because crystallised K2P constructs are truncated, and Boltz2 reads
> 41.4 there while MSA-independent ESMFold2 reads 76.4.

Date of checks: 2026-11-04. UniProt release 2026_03.

## 0. What subject I assumed, and what I could not see

- **Subject.** The claim names no gene or species. The only K2P protein in this project's fish
  work is zebrafish (*Danio rerio*) Kcnk5b, the *another longfin* (*alf*) channel. I assume the
  query is zebrafish Kcnk5b, UniProt **Q6PFU3** (448 aa). I checked the residue numbering against
  the literature: position 241 is F, the *alf* F241Y site in Daane et al. 2018, and position 290 is
  I, their I290A calcineurin-motif mutant. The numbering is consistent, but **the assumption is
  mine**. If claim 26 is about another protein, nothing below applies.
- **The run itself is not in this repository.** I found no Boltz2 or ESMFold2 output, no PDB70
  hit table and no claim-26 source file (I grepped the repo for `ESMFold`, `Boltz`, `PDB70`, `326`,
  `41.4` and `76.4`). So I have **not** re-checked the protein-scale numbers 41.4, 76.4 and
  "0.0 from 326". They are taken as stated.
- **Blocked tools.** The proxy rejected api.colabfold.com, data.rcsb.org and NCBI BLAST. EBI
  Job Dispatcher BLAST refused the job under its fair-use block. EBI HMMER returned 405. The
  sequence-depth check in C2 therefore uses a local substitute, described there.

## 1. Constraints entailed

If claim 26 is true, the following must hold at the adjacent scales:

| # | scale | kind | requirement (generic) |
|---|---|---|---|
| C1 | dna | existence | The coding sequence for the low-confidence segment (residues ≥326) must exist in the subject's genome and transcript. It must not be a gene-model artefact. Otherwise there is no real segment for the two models to disagree about. |
| C2 | dna | range | "Confidence tracks **alignment** depth" through an **MSA-dependent** model needs the *sequence-database* homolog depth over ≥326 to be well below the depth over the folded core. Template (PDB70) depth alone is not the input that makes a model MSA-dependent. Bound: ratio of mean aligned-homolog count (326–448) / (1–250) in [0, 0.5]. The 0.5 cut-off is my choice, not a published threshold. |
| C3 | cell | existence | The mechanism says templates stop because structural constructs are truncated. That requires the truncated construct the templates come from to remain a functional channel in cells. If removing the tail destroyed function, the truncation would be a sign of misfolding, not of convenience. |
| C4 | cell | existence | The segment ≥326 must actually be present in the mature protein inside cells: not cleaved, and on the cytoplasmic side. Otherwise its predicted confidence has no cellular referent. |

## 2. Checks

### C1 — dna / existence: **satisfied**

- UniProt Q6PFU3 (read-level: full record via REST). Zebrafish `kcnk5b`, 448 aa, protein
  existence "Evidence at transcript level". It is backed by EMBL cDNA **BC057416** and RefSeq
  **NP_956927.1**, ZFIN ZDB-GENE-040426-1297. The cDNA covers the full ORF, residues 326–448
  included.
- Daane et al. 2018, *Sci Rep* 8:10391, PMC6039437 (read-level: full-text, via a summarising
  fetch). The authors state that "the fifth and terminal exon of zebrafish kcnk5b encodes the last
  transmembrane domain and cytoplasmic C-terminus". So the tail is encoded in a real exon.
- Species: zebrafish on both sides. **Measured** (cDNA sequencing), not inferred.

### C2 — dna / range: **satisfied** (computed, with two caveats that cut against the claim's wording)

**Method. This is a calculation, not an observation.** I downloaded all 31,060 UniProt
reference-proteome sequences in InterPro IPR003280 (two-pore-domain K⁺ channel family,
UniProt 2026_03). I ran `phmmer` (pyhmmer, E ≤ 1e-3) with Q6PFU3 as the query and counted,
at each query position, how many included hits put an aligned residue there. These are raw
counts. They are not redundancy-weighted Neff, and they are not the ColabFold MMseqs2 MSA that
Boltz2 would actually use. The database is restricted to the K2P family, so it cannot see
homologs of the tail outside that family.

**Result (computed).** 29,199 sequences were included.

| query segment | mean aligned seqs | min | max |
|---|---|---|---|
| 1–250 (TM core) | 17,958 | 738 | 24,905 |
| 251–300 | 2,220 | 1,060 | 5,938 |
| 301–325 | 850 | 585 | 1,066 |
| **326–381** | **551** | 345 | 666 |
| 382–448 | 285 | 25 | 422 |

The ratio (326–448)/(1–250) is about 0.023. Using 326–381 alone it is about 0.031. Both are well
inside [0, 0.5], so the constraint is met.

**Caveat (a): sequence depth does not fall to 0.0, and it has no step at 326.** Single-position
counts are 1,060 at 300, 588 at 315, 681 at 325, 658 at 330 and 634 at 335. The fall is a
gradual slope from TM4 (about residue 250) onward, with a drop near 315. There is no cliff at 326.
- The claim's "0.0 from residue 326" is therefore about **template (PDB70) coverage only**.
  The *sequence* alignment over that segment is shallow but non-empty: hundreds of raw hits.
- My inference, not the claim's: the claim's evidence (PDB70 depth) and its stated mechanism
  (an MSA-dependent model) refer to two different alignments.
- If Boltz2 was run with templates, its drop could follow the template edge. If it ran without
  templates, the drop has to come from the shallower sequence MSA, which this computation
  supports in direction but not in shape.
- I cannot tell which applies without the run configuration. Flagged for the protein-scale owner.

**Caveat (b): 326 is not reproduced as the template edge by my own mapping.** This is protein
scale, so it goes in a note rather than a verdict.
- The mouse TASK2 cryo-EM construct is residues 1–335 (C3). A pairwise phmmer of mouse Q9JK62
  against zebrafish Q6PFU3 (computed) aligns mouse 1–311 to zebrafish 1–313. Beyond that point
  there is no significant alignment.
- The coordinates actually modelled stop at mouse residue 260, which is zebrafish 260 (PDBe
  polymer coverage: 6WLV 5–260, 6WM0 6–260).
- So a TASK2-derived template edge would fall near zebrafish 313 (construct SEQRES) or 260
  (modelled atoms), not at 326. Another K2P template, or an HMM–HMM alignment that extends
  further, could account for 326. I have not seen the PDB70 hit list, so the status of "326"
  is `unknown`.
- Also, the claim says "crystallised". The TASK2 structures are cryo-EM (3.45 Å and 3.52 Å,
  PDBe), not crystal structures.

### C3 — cell / existence: **satisfied for the template species (mouse); untested for zebrafish**

- Li, Rietmeijer & Brohawn 2020, *Nature* 586:457–462, PMID 32999458, PMC8628578 (read-level:
  full-text, via a summarising fetch).
- Mouse TASK2 1–335 ("a truncation of the C-terminal 167 amino acids, which are predicted to be
  largely unstructured") was made because it "increased expression and biochemical stability".
- Expressed in HEK293T, the construct "retained the hallmark features of TASK2". Its activation by
  extracellular alkalisation, intracellular alkalisation and PIP2 was "indistinguishable from full
  length". The authors report P = 0.45, 0.72 and 0.54 for the three comparisons. **Measured.**
- The authors also state that "the distal intracellular C-terminal region was not resolved"
  (modelled residues 6–260).
- **Species, both sides.** The construct and the recordings are mouse protein in human cells. The
  claim's query is (by my assumption) zebrafish. C3 is a requirement on *the template's* construct,
  so mouse is the right subject for it, and the requirement is met.
- Whether a zebrafish Kcnk5b truncated near 326 is functional is **unknown**. Daane et al. 2018
  report no electrophysiology of truncated Kcnk5b. Their Xenopus-oocyte recordings cover wild type,
  I290A and drug treatments only (full-text scope).

### C4 — cell / existence: **open**

- The requirement is that residues ≥326 are present in the mature zebrafish protein in cells, and
  are cytoplasmic.
- **Topology is predicted, not measured.** UniProt Q6PFU3 places TM4 at 229–250 using Phobius,
  which makes the tail intracellular. MobiDB-lite marks 382–448 as disordered, also a prediction.
- **Functional evidence exists but does not isolate ≥326.** Daane et al. 2018 (zebrafish,
  full-text) recovered CRISPR frameshifts "leading to early termination" in exon 5, and these
  caused fin-ray overgrowth in somatic clones. They also identify a calcineurin-binding motif
  with I290 as a key residue. That shows the C-terminal region matters in zebrafish fin cells.
  However, the paper gives no residue positions for the truncations. I290 lies upstream of 326,
  and the guides tiled "the start of" exon 5, which also encodes TM4.
- My inference: these truncations most likely remove much more than 326–448, so they do not show
  that 326–448 itself is present or functional.
- **Scope of the negative.** I searched the web and the full text of Daane 2018 for zebrafish
  Kcnk5b C-terminal mass-spectrometry coverage, C-terminal antibody or epitope-tag localisation,
  and proteolytic processing. I found none. Two other kinds of evidence I did **not** search:
  proteomics repositories (PRIDE / PeptideAtlas) and the Perathoner et al. 2014 *PLoS Genet* full
  text. So this is "not found within that scope", **not** "looked for and absent".
- For comparison (mouse/human, not zebrafish, so it is not used for the verdict): Añazco et al.
  2013, *Pflügers Arch*, doi:10.1007/s00424-013-1314-0 (read-level: abstract via search-summary)
  show Gβγ regulation through C-terminal lysines K257/K258 and K296/K297 in HEK-293. These sit
  upstream of the equivalent of 326 and are mammalian.

## 3. Nothing here is `unsatisfiable`

No measured value contradicts any constraint. The two things that cut against the claim's wording
are:
1. the sequence MSA over 326+ is shallow, not empty;
2. 326 is not reproduced as the TASK2 template edge.

Both are **my calculations**, not measurements, and both concern how the protein-scale evidence was
described. Neither contradicts a dna- or cell-scale requirement. All cross-species material is
labelled: mouse TASK2 for C3 and the Añazco comparison, zebrafish for C1, C2 and C4. No flying-fish
(exocoetid) data was used anywhere.

## Sources

| source | read-level |
|---|---|
| UniProt Q6PFU3, Q9JK62, O95279; IPR003280 reference-proteome set (release 2026_03) | full record via REST |
| PDBe API: 6WLV and 6WM0 UniProt mapping, polymer coverage, experiment | full record |
| Li B, Rietmeijer RA, Brohawn SG. *Nature* 586:457 (2020), PMC8628578 | full-text (summarising fetch) |
| Daane JM et al. *Sci Rep* 8:10391 (2018), PMC6039437 | full-text (summarising fetch) |
| Añazco C et al. *Pflügers Arch* (2013), doi:10.1007/s00424-013-1314-0 | search-summary |
| Perathoner S et al. *PLoS Genet* (2014), doi:10.1371/journal.pgen.1004080 | listing only; not used for any verdict |

The computation scripts (`depth.py`, `map.py`) were run from a scratch directory. Their method is
described in full under C2.

```swarm-entail
{"source_claim": 26, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "The coding sequence for the low-confidence segment (residues >=326) must exist in the subject's genome/transcript rather than being a gene-model artefact",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Zebrafish kcnk5b full-length cDNA BC057416 / RefSeq NP_956927.1 encodes a 448-aa ORF (UniProt Q6PFU3, PE=transcript level); terminal exon 5 encodes TM4 and the cytoplasmic C-terminus",
      "satisfied_evidence": "measured",
      "note": "UniProt Q6PFU3 (full record, release 2026_03); Daane et al. 2018 Sci Rep 8:10391 PMC6039437 (full-text). Subject assumed to be zebrafish Kcnk5b; numbering checked against F241 (alf) and I290. Species: zebrafish on both sides."},
    {"target_scale": "dna", "kind": "range",
      "statement": "For confidence in an MSA-dependent model to track alignment depth, sequence-database homolog depth over the segment must be well below that over the folded core, not only template depth",
      "quantity": "mean aligned-homolog count over 326-448 divided by mean over 1-250", "lo": 0, "hi": 0.5, "units": "dimensionless ratio",
      "status": "satisfied",
      "satisfied_by": "Computed: phmmer (E<=1e-3) of Q6PFU3 against 31,060 IPR003280 reference-proteome sequences gives mean 17,958 aligned seqs over 1-250, 551 over 326-381 and 285 over 382-448 (ratio ~0.023). Depth is NOT zero and has no step at 326: 681 at 325, 658 at 330, sloping from about residue 250",
      "satisfied_evidence": "simulated",
      "note": "This is a calculation, not an observation: raw counts, not Neff; a K2P-family-restricted database, not the ColabFold MMseqs2 MSA Boltz2 uses. ColabFold, NCBI BLAST, RCSB and EBI BLAST/HMMER were unreachable. The 0.5 threshold is the author's choice. Flag: the claim's 0.0 is template (PDB70) depth only; whether Boltz2 used templates is unknown. The 326 template edge was not reproduced: mouse TASK2 1-335 aligns to zebrafish only up to 313, and modelled atoms end at 260."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "The truncated structural construct that templates derive from must remain a functional channel in cells, so the truncation reflects convenience rather than misfolding",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Mouse TASK2 1-335 in HEK293T showed extracellular-pH, intracellular-pH and PIP2 activation indistinguishable from full length (P=0.45, 0.72, 0.54); distal C-terminus unresolved in cryo-EM (modelled 6-260)",
      "satisfied_evidence": "measured",
      "note": "Li, Rietmeijer & Brohawn 2020 Nature 586:457, PMC8628578 (full-text). Species: mouse protein in human cells, which is the template's own species and so the correct subject for this constraint. Equivalent zebrafish truncation electrophysiology: unknown; none in Daane 2018 (full-text scope). Structures are cryo-EM, not crystallographic."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "The segment >=326 must be present in the mature protein in cells (not cleaved) and located cytoplasmically",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Nothing found that isolates residues >=326 in zebrafish cells. Topology (TM4 229-250, intracellular C-terminus) is a Phobius prediction. Daane 2018 exon-5 frameshift truncations cause fin overgrowth, but their positions are not reported and likely remove far more than 326-448 (I290 motif upstream)",
      "satisfied_evidence": "unknown",
      "note": "Searched: web and Daane et al. 2018 full text for zebrafish Kcnk5b C-terminal mass-spec coverage, C-terminal antibody/epitope-tag localisation and proteolytic processing; none found. NOT searched: PRIDE/PeptideAtlas proteomics, Perathoner 2014 full text. 'Not found in this scope', not 'shown absent'. Mammalian Anazco et al. 2013 (search-summary) is cross-species and was not used for the verdict."}
  ]}
```
