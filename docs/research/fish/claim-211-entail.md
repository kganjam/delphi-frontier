# Claim 211: entailments at the dna and cell scales

**Source claim (protein scale, recorded evidence: measured; author's words, not mine):**
"REPRODUCIBILITY GAP CLOSED and the finding CONFIRMED: recomputed per-residue MSA depth directly
from the now-committed kcnk5b_pdb70.a3m (72 sequences) gives 21.4 mean over residues 1-250, 0.5
over 261-end, and LITERALLY 0.0 from residue 326 on. The alignment-depth explanation for Boltz2 low
confidence holds and is now independently checkable."

Context already on record: `challenge-211.md` (branch `claude/challenge-kcnk5b-msa-depth-wduwx4`,
read-level full-text) reproduced every number. It found that the zero actually starts at residue
312, and it argued the evidence level should be *derived*, not *measured*. I don't re-litigate
those points here. This document asks a different question: if the claim is true, what has to
hold one scale down (the gene that encodes the query) and one scale up (the cells that made the
only structural template, and the cells where the channel acts)?

**Summary.** Five constraints. Four are **satisfied**, one is **open**, none is **unsatisfiable**.
The most informative result is constraint C4. The construct end of the only template, mouse TASK2
residue 335, maps to query residue **313**, and depth falls to zero at query **312**. The
construct-truncation mechanism, which challenge-211 left `unknown`, is therefore confirmed. The
same source also measures that the template's own density stops at residue 260, and its authors
truncated the construct *because* the C-terminus is predicted to be unstructured. So the
"evidence ran out" explanation is now established. That same evidence also shows it is not
independent of disorder.

## Inputs and read-levels

| source | what I used | read-level |
|---|---|---|
| `kcnk5b_pdb70.a3m` @ `8bf7ee39` (sha256 `5eb89c812d003ca2…`) | query sequence, 72 records | full-text |
| UniProt Q6PFU3 (zebrafish kcnk5b), O95279 (human KCNK5), Q9JK62 (mouse Kcnk5), JSON + FASTA via rest.uniprot.org | sequences, features, PDB cross-refs | full-text (database records) |
| UniProt fish orthologs A0A6P6M099, A0A2D0PX72, A0A6J2V4H0, A0A4W6D0U6, A0A672ZYS1, Q32PR9 | sequences | full-text (database records) |
| NCBI NP_956927.1 GenPept, BC057416.1 esummary (eutils) | RefSeq status, CDS, source mRNA | full-text (database records) |
| PDBe API `entry/molecules/6wlv`, `entry/polymer_coverage/6wlv` | construct sequence, host, observed residues | full-text (database records) |
| Li, Rietmeijer & Brohawn 2020, *Nature* 586:457–462, doi:10.1038/s41586-020-2770-2, PMC8628578 | construct rationale, modelled residues, HEK293T comparison | full-text, but read through an automated fetch-and-summarise step. The quotes below are as returned by that step, not checked by eye against the PDF. |
| Añazco et al. 2013, *Pflügers Arch* 465:1715–1726, doi:10.1007/s00424-013-1314-0 | C-terminal lysines and Gβγ | search-summary |
| Perathoner et al. 2014, *PLoS Genet* 10:e1004080 | kcnk5b expressed in Xenopus oocytes | search-summary (abstract-level) |
| RCSB data API | — | could-not-access (proxy refused `data.rcsb.org`); I used PDBe instead |

**Computed** below means a calculation I ran (scripts `claim-211-entail-mapping.py`,
`claim-211-entail-tail.py`, Biopython 1.88, BLOSUM62, gap −11/−1). These numbers are calculations
on database sequences. They are not observations.

---

## C1. dna / existence: a transcript-backed ORF must encode the zero-depth region

**Requirement.** The claim treats residues 312–448 as part of the protein and attributes their
zero depth to the database. That requires a real coding sequence covering those residues. A gene-model
artefact, such as a mispredicted terminal exon, would also produce zero depth.

**Status: satisfied** (database records, full-text).
- The a3m query (448 aa) is identical to UniProt Q6PFU3 and to RefSeq NP_956927.1 (computed:
  exact string equality).
- NP_956927.1: "CDS 1..448 /coded_by=NM_200633.1:68..1414". The record is a PROVISIONAL RefSeq
  "derived from BC057416.1". BC057416.1 is "Danio rerio potassium channel, subfamily K, member 5,
  mRNA (cDNA clone MGC:63921 IMAGE:6790750), complete cds", 2,576 nt. The exon-combination evidence
  also cites EST EG585395.1.
- So a full-length cDNA clone supports the 448-codon ORF. Caveat: the status is "provisional", not
  "validated". I did not check whether the EST covers the 3′ exon specifically.

## C2. dna / range: the encoded length must equal the query length

**Requirement.** Depth "from 326 on" is only meaningful up to the true C-terminus. Encoded protein
length L ∈ [448, 448] aa.

**Status: satisfied** (database records). NP_956927.1 is 448 aa (CDS 68..1414 = 1,347 nt =
448 codons + stop). Q6PFU3 is 448 aa. No alternative longer zebrafish kcnk5b isoform was
returned by the UniProt query `gene:kcnk5b AND organism_id:7955`, which returned Q6PFU3 and A0A8M1PBI1,
both 448 aa. Scope: I checked UniProt only, not the Ensembl transcript set.

## C3. dna / existence: homologous coding sequence for the tail must exist in other genomes

**Requirement.** "Alignment depth ran out" is a statement about PDB70. For it to be a
*database-composition* effect, not a property of the sequence itself, homologous sequence for
residues 312–448 has to exist somewhere. Orthologous genes in other genomes would do. If no
ortholog anywhere carried an alignable tail, depth would be zero in every database, and
"a deeper MSA would fix it" would be false.

**Status: satisfied, with a disagreement preserved** (computed, on UniProt sequences).

Local alignment of query 312–448 against each target, compared with 200 shuffles of the same
segment (computed):

| target | covers query | identity | score | shuffled max |
|---|---|---|---|---|
| goldfish kcnk5b A0A6P6M099 | 312–448 | 0.74 | 449 | 58 |
| milkfish kcnk5b A0A6J2V4H0 | 318–443 | 0.42 | 174 | 52 |
| channel catfish kcnk5b A0A2D0PX72 | 315–438 | 0.40 | 185 | 54 |
| barramundi kcnk5b A0A4W6D0U6 | 316–443 | 0.30 | 132 | 55 |
| cardinalfish kcnk5b A0A672ZYS1 | 314–437 | 0.32 | 101 | 63 |
| zebrafish kcnk5a Q32PR9 | 327–421 | 0.32 | 101 | 55 |
| **mouse Kcnk5 Q9JK62** | 342–418 | 0.27 | **45** | **55** |
| **human KCNK5 O95279** | 405–446 | 0.33 | **47** | **52** |

For reference, the TM core (query 1–250) aligns to mouse and human at 0.64 identity, with score
about 905–914.

- Teleost orthologs carry a clearly homologous tail. Every score is above its shuffled maximum.
  A sequence database containing fish kcnk5 genes would give nonzero depth over 312–448.
- **Disagreement with challenge-211.** That review inferred, without running a search, that
  "K2P C-termini are present in sequence databases" and would give depth. That inference holds
  for **fish** sequences only. Against mammalian TASK2 the zebrafish tail scores **inside the
  shuffled range** (45 vs 55; 47 vs 52). My inference from this: the tail is not detectably
  homologous to mammalian tails by pairwise alignment, so a deeper MSA would be shallow and
  teleost-only over 312–448, while the TM core would be deep. These are pairwise alignments, not
  a profile search. A profile/HMM search might detect more. I ran none, because no MMseqs2/HHblits
  is available here.

## C4. cell / spatial: the only template's expressed construct must end where depth ends

**Requirement.** The claim's mechanism, as recorded elsewhere in the project, is "the
structural template does not contain the tail". The only template rows that reach past residue
240 are 6WLV_A and 6WM0_A (challenge-211). These are mouse TASK2 expressed in yeast cells and
imaged by cryo-EM. If the mechanism is right, the C-terminus of that cell-expressed construct,
mapped into query numbering, must sit at the onset of zero depth. Quantity: query-equivalent
position of the template construct's last residue, in [305, 326]. The bounds are the claim's
stated zero point (326) and a 7-residue margin below the observed onset (312) for alignment
uncertainty.

**Status: satisfied** (construct boundary measured and deposited; mapping computed).
- PDBe `6wlv` entity 1: length 343, "Mus musculus", expression host "Komagataella pastoris", UniProt
  mapping residues 1–335, plus an 8-residue tag `SNSLEVLF`. The construct's residues 1–335 are
  identical to Q9JK62 1–335 (computed). UniProt Q9JK62 lists 6WLV and 6WM0 as "A/B=1-335".
- Li et al. 2020 (full-text via automated fetch): "Removing the predicted unstructured C-terminal
  region of Mus musculus TASK2 (resulting in TASK2 1-335) increased expression and biochemical
  stability", and "A truncation of the C-terminal 167 amino acids, which are predicted to be largely unstructured".
- Global alignment of query vs mouse Q9JK62 (computed): mouse 335 → **query 313**. Query 311 →
  mouse 309. Depth reaches zero at query 312 (challenge-211, computed from the a3m). The template
  sequence ends within about 1 residue of where depth ends. **313 ∈ [305, 326].**
- This resolves the item challenge-211 left `unknown` ("its construct length is unknown"). The
  zero from 312 on is explained by template truncation, not by MMseqs2 failing to extend into
  sequence that was present.

**What the same source also measures, and it cuts the other way.** PDBe polymer coverage
reports observed residues **5–260** in both chains of 6WLV. Li et al. state that amino acids
"6-260 from each chain" were modelled and that "the distal intracellular C-terminal region was not
resolved", which the authors attribute to "conformational heterogeneity or disorder". The two
sources give 5 vs 6 for the first residue; I report both. The consequences:
1. Query 241–311 has depth 2, but the template rows supplying it have **no coordinates** past
   mouse 260. That is a measured absence of density, not a computed one.
2. The tail was truncated *because* it is predicted disordered. That is the authors' stated
   rationale, and the predictions are theirs, not measurements. So "no template" and "disorder"
   are causally linked, not rival explanations. Challenge-211 inferred this link from general
   practice; it is now documented for this template.

Neither fact contradicts any number in the claim. Depth is still 0 from 312. Both facts bound
the reading: "alignment ran out" is confirmed as the proximate cause. It is not evidence
*against* disorder. UniProt's MobiDB-lite annotations, which are predictions and not measurements,
mark zebrafish 382–448 and human 312–335, 360–388 and 428–499 as disordered.

## C5. cell / existence: the full-length product including the tail must exist in the cells where kcnk5b acts

**Requirement.** This is weaker than C1–C4. For the zero-depth tail to matter for the biology,
not just for Boltz2 on a sequence, the protein that cells actually make must include residues
312–448, with no processing that removes them.

**Status: open.**
- What exists: zebrafish kcnk5b was expressed in Xenopus oocytes for electrophysiology
  (Perathoner 2014, search-summary). The summary does not say whether the construct was full-length,
  and I did not read the methods.
- For the mammalian ortholog, the measurements don't answer the question directly but bear on
  it. In HEK293T cells, TASK2 1–335 "retained the hallmark features of TASK2" and was
  "indistinguishable from full length TASK2" for pH_ext and pH_int activation (Li 2020, full-text
  via fetch). C-terminal lysines K257-K258 and K296-K297 are required for Gβγ inhibition
  (Añazco 2013, search-summary). Both lie *inside* the 1–335 construct. My inference: the measured
  cell functions I found map to the template-covered region, not to the zero-depth tail.
- What I did not find: no measurement of endogenous zebrafish kcnk5b protein length in vivo
  (western blot, mass spectrometry). Scope: two web searches and the sources above. I did **not**
  search PRIDE/ProteomicsDB or ZFIN antibody records. This is "not looked for thoroughly", not
  "looked for and absent".

---

## Bottom line for claim 211

- No measured value at the dna or cell scale contradicts the claim. Nothing is **unsatisfiable**.
- C4 upgrades the mechanism from asserted to checked. The template construct ends at query ~313,
  and the measured construct boundary plus a computed mapping is enough to show it.
- C3 and C4 together sharpen how the claim should be read. The tail has homologs only in fish
  (computed), and the only template omits it because it was predicted unstructured (authors'
  claim). Its resolved density stops at 260 (measured). "Alignment depth explains Boltz2 low
  confidence" holds. "…and therefore not disorder" is not supported by anything I found.

```swarm-entail
{"source_claim": 211, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "A transcript-supported open reading frame must encode the residues that show zero alignment depth, so that the zero is not a gene-model artefact",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "RefSeq NP_956927.1 (CDS 1..448, coded_by NM_200633.1:68..1414) derived from full-length cDNA clone BC057416.1 (MGC:63921, 'complete cds') with EST EG585395.1; sequence identical to a3m query and UniProt Q6PFU3",
      "satisfied_evidence": "measured",
      "note": "NCBI GenPept/esummary via eutils, full-text database record. RefSeq status is PROVISIONAL, not validated. Did not check that the EST covers the 3' exon."},
    {"target_scale": "dna", "kind": "range",
      "statement": "The encoded protein length must equal the query length over which depth was computed",
      "quantity": "encoded kcnk5b protein length", "lo": 448, "hi": 448, "units": "amino acids",
      "status": "satisfied",
      "satisfied_by": "NP_956927.1 = 448 aa (1347-nt CDS); UniProt Q6PFU3 and A0A8M1PBI1 = 448 aa; a3m query = 448 aa and identical to Q6PFU3",
      "satisfied_evidence": "measured",
      "note": "UniProt query gene:kcnk5b AND organism_id:7955 returned no longer isoform. Ensembl transcripts not checked."},
    {"target_scale": "dna", "kind": "existence",
      "statement": "Homologous coding sequence for the zero-depth C-terminal region must exist in other genomes, so that zero depth is a property of the structure database rather than of the sequence",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Teleost kcnk5b/kcnk5a orthologs align to query 312-448 above shuffled controls (goldfish A0A6P6M099 score 449 vs shuffled max 58, 0.74 id; catfish A0A2D0PX72 185 vs 54; milkfish A0A6J2V4H0 174 vs 52; barramundi, cardinalfish, zebrafish kcnk5a 101-132 vs 55-63). Mouse Q9JK62 (45 vs 55) and human O95279 (47 vs 52) tails are NOT distinguishable from shuffled",
      "satisfied_evidence": "derived",
      "note": "Computed pairwise local alignments (BLOSUM62, gap -11/-1, 200 shuffles) on UniProt sequences. Satisfied for fish only; this contradicts challenge-211's unsearched inference that mammalian-inclusive sequence DBs would cover the tail. No profile/HMM search was run (no MMseqs2/HHblits available)."},
    {"target_scale": "cell", "kind": "spatial",
      "statement": "The C-terminus of the cell-expressed construct that supplies the only structural template must map, in query numbering, to where alignment depth falls to zero",
      "quantity": "query-equivalent position of the template construct's last residue", "lo": 305, "hi": 326, "units": "residue index",
      "status": "satisfied",
      "satisfied_by": "6WLV/6WM0 construct = Mus musculus TASK2 1-335 (+8-aa tag) expressed in Komagataella pastoris; mouse 335 maps to query 313 by global alignment; depth is zero from query 312",
      "satisfied_evidence": "measured",
      "note": "Construct boundary: PDBe API entry/molecules/6wlv (full-text record), UniProt Q9JK62 PDB xref 'A/B=1-335', Li, Rietmeijer & Brohawn 2020 Nature 586:457 (PMC8628578, full-text via automated fetch). Mapping is computed. Same sources measure observed density only for residues 5-260 (PDBe) / modelled 6-260 (paper), and the authors truncated because the C-terminus is 'predicted to be largely unstructured', so template absence and predicted disorder are causally linked."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "The protein made in the cells where the channel acts must include the zero-depth C-terminal region (no processing that removes it)",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Not found: no in-vivo measurement of endogenous zebrafish kcnk5b protein length. Related: Perathoner 2014 expressed kcnk5b in Xenopus oocytes (construct length not stated in abstract); in HEK293T, mouse TASK2 1-335 is indistinguishable from full length for pH gating (Li 2020); Gbg-sensing lysines K257-K258/K296-K297 lie inside 1-335 (Anazco 2013)",
      "satisfied_evidence": "unknown",
      "note": "Scope: two web searches plus the cited papers (Perathoner 2014 search-summary/abstract; Anazco 2013 search-summary; Li 2020 full-text via fetch). PRIDE/ProteomicsDB and ZFIN antibody records not searched, so this is 'not looked for thoroughly', not 'looked for and absent'."}
  ]}
```
