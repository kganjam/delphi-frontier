# Claim 306 — entailments at the DNA and cell scales

**Source claim (protein scale, evidence: measured).** PDB70 (pdb70_220313, via ColabFold) gives zero
alignment coverage at residue 200 of zebrafish slc43a2a (ENSDARP00000138218, 577 aa): 5 hits, max depth 2,
median 0, 474/577 positions uncovered, including all of 195–205. The claim is explicitly scoped: it bounds
what PDB70 can say, it does not say the residue is unconserved or disordered.

**Subject animal throughout: zebrafish (*Danio rerio*)** unless a line says otherwise. No flying-fish
(exocoetid) measurement is used as evidence for or against any constraint below. Where a number comes from
human or mouse, it is labelled as such and is not used to refute anything.

**Date of checks:** 2026-11-04. Ensembl REST/website was **not reachable** from this session (proxy 403), so
Ensembl-side facts were obtained via EBI UniParc / EBI Search, which index Ensembl.

---

## 0. What T200K is (context found while checking; changes the stakes of the claim)

The claim mentions "T200K" without saying where it comes from. It is a published zebrafish allele:

- Daane JM, …, Harris MP (2021) *Modulation of bioelectric cues in the evolution of flying fishes.*
  Curr Biol 31(22):5052–5061.e8. doi:10.1016/j.cub.2021.08.054. PMID 34534441, PMCID PMC9172250.
  **Read-level: full-text** (PMC XML via NCBI E-utilities).
  - Author's claim, quoted: "We identified a dominant mutant, *nr21*, as having small adult fins … we
    mapped *nr21* to chromosome 15 and identified a nonsynonymous mutation (T200K) in a conserved domain of
    the L-type amino acid transporter, *lat4a*."
  - Author's claim: CRISPR frameshifts *in cis* to the *nr21* allele revert the fin phenotype to wild type,
    "indicating that the mutation in *lat4a nr21* results from a gain-of-function effect"; zebrafish lacking
    *lat4a* "have no fin phenotype".
  - Alleles listed in the key-resources table: "lat4 nr21 (dmh26)" and "lat4a del (mh152)".
- ZFIN lists *slc43a2a*^dmh26 and *slc43a2a*^mh152 genotypes from the Harris lab, attributed to Daane et al.
  2021, under gene ZDB-GENE-040426-964 (slc43a2a). **Read-level: search-summary** (zfin.org returned 503 on
  direct fetch). My inference: *lat4a* in the paper = *slc43a2a* in ZFIN; this rests on the shared allele
  names and gene ID, not on a statement I read in ZFIN itself.

**Inference (mine, not the authors'):** T200K is a dominant **gain-of-function** allele. A
gain-of-function missense allele is more likely to work through a folded, functional protein than through
loss of structure. That makes the claim's warning ("low predicted confidence at 200 would mean the alignment
ran out, NOT that the region is disordered") consequential. It does not prove the region is ordered.

The authors also report a convergent **F326L** substitution in flying fishes and flying halfbeaks. That is a
different residue in a different animal. It is not used below.

---

## 1. Constraints and checks

### C1 — DNA, existence: codon 200 must be a real coding triplet from which Thr→Lys is reachable in one step
For the claim to be about a real residue, position 200 of the 577-aa model has to correspond to a genomic
codon in frame. For "T200K" to be an ordinary point allele, that codon must be **ACA or ACG**: of the four
Thr codons, only these reach a Lys codon (AAA/AAG) by one substitution. ACT and ACC give Asn.

**Check (derived, my computation):**
- The 577-aa sequence was fetched from EBI UniParc **UPI00062E34B4**, whose Ensembl cross-reference
  ENSDARP00000138218 is flagged active (the UniProtKB/TrEMBL cross-ref A0A0R4IP58 is flagged *inactive*).
  Length 577; residues 195–205 = `ASSAVTFPGIK`; residue 200 = **T**. Read-level: full record (API).
- I fetched GRCz13ab chr15 (NC_141035.1:30,950,000–31,300,000) from NCBI and translated it in six frames.
  Several 8–14-aa peptides spanning residue 200 (e.g. `IALMIGSYASSAVT`, `GSYASSAVTFPGIK`) each match
  **once**, all on the + strand in the same frame. Codon 200 = **ACA** at NC_141035.1:31,121,333–31,121,335,
  local context `TCCGCTGTC[ACA]TTCCCAGGA`.
- ACA→AAA (Lys) is a single C>A transversion at the codon's middle base (NC_141035.1:31,121,334 on GRCz13ab).
  The paper does not say which nucleotide change *nr21* carries (not in the text I read; Figure S2 was not
  read). **The C>A change is my inference**, since it is the only single-base route from ACA to Lys.
- The allele's existence is measured: Daane et al. 2021 found T200K by pooled sequencing of *nr21* fish
  (full-text).

Caveat: the ENSDARP model was built on GRCz11 and I checked GRCz13ab. The 14-aa match is exact and
unique, so the codon assignment holds, but I did not compare assemblies directly.

**Status: satisfied.**

### C2 — DNA, existence: a transcript that includes codon 200 must be expressed (the 577-aa model must be real)
The claim's measurement is about position 200 of a 577-aa model. If no expressed transcript included that
codon, the measurement would be about an annotation artefact.

**Check, with sources in disagreement (both kept):**
- **Ensembl:** ENSDARG00000036848 (*slc43a2a*) has transcripts ENSDART00000142298 and ENSDART00000168453
  (EBI Search, read-level: listing). EBI Search maps ENSDARP00000138218 to this gene (listing). UniParc
  shows the 577-aa product as active (full record).
- **NCBI RefSeq** (gene 393221, annotated on GRCz13ab, 5 exons, chr15:31,099,368–31,139,242): the **only**
  RefSeq protein is **NP_956545.1, 153 aa** (NM_200251.2). A search of NCBI Protein for "slc43a2a AND
  Danio rerio" returned only this record. Comparing 10-mers, NP_956545.1 is identical to the 577-aa model
  up to about residue 140, then diverges. **Position 200 does not exist in NCBI's product.** UniProt has
  two 153-aa *slc43a2a* entries (Q7ZUS0, A0A8N7V006) and no active 577-aa *slc43a2a* entry.
- **Indirect support for the long form (my inference):** the *nr21* phenotype maps to T200K, and frameshifts
  *in cis* revert it (Daane 2021). That only makes sense if a product containing residue 200 is made. This
  is genetic inference, not a transcript measurement. Daane's *lat4a* qRT-PCR primer positions relative to
  the two isoforms are unknown to me (I did not map them).
- Mammalian orthologues are full-length: human SLC43A2 is 569 aa, mouse 568 aa (UniProt Q8N370, Q8CGA3).
  This is cross-species and bears on plausibility only.

Not done: an RNA-seq or EST check that a read spans the exon containing codon 200. I could not reach
Ensembl, and I did not run BLAST against SRA or EST.

**Status: open.** Genetic evidence favours the long form. NCBI RefSeq's current annotation contradicts it at
the level of gene models. Neither is a direct expression measurement of the codon-200 exon.

### C3 — DNA, existence: homologous coding sequences outside PDB70 must align over codons 195–205
The claim's scope clause predicts that sequence databases could be deep where PDB70 is empty. At minimum,
some homologous sequences must cover this window.

**Check (derived, my computation):** global Needleman–Wunsch alignment (Biopython, BLOSUM62, gap −11/−1) of
the 577-aa zebrafish sequence against three UniProt sequences (EBI Proteins API, full records):

| sequence | species | identity over the zebrafish length | aligned to zf 195–205 | residue at zf T200 |
|---|---|---|---|---|
| Q8N370 LAT4_HUMAN | human | 76.6 % | `ASSAVTFPGIK` | T193 |
| Q8CGA3 LAT4_MOUSE | mouse | 75.4 % | `ASSAVTFPGIK` | T193 |
| Q5PR35 (*slc43a2b*) | zebrafish paralogue | 78.3 % | `ASSAVTFPGVK` | T222 |

These are three sequences, not an MSA depth. They show coverage exists outside PDB70 and that Thr is shared
across these four sequences. They do **not** measure UniRef or BFD depth, which I did not run. Daane et al.
call the site "a conserved domain" (author's claim, full-text). The basis is presumably in Figure S2, which I
did not read. This agrees with the claim: PDB70 emptiness was never evidence of non-conservation.

**Status: satisfied** (existence only; how deep is still unknown).

### C4 — cell, existence: slc43a2a must be expressed in zebrafish cells where the T200K phenotype appears
If T200K has a cellular consequence in fins, the gene must be transcribed there.

**Check:** Daane et al. 2021, Figure 4E legend (full-text): "qRT-PCR of *lat4a* showing no significant
difference in *lat4a* expression across fins and genotypes". The genotypes include wild type, *nr21*/+ and
*lof*/+, and the fins include pectoral and dorsal. This is zebrafish and measured. The Alliance/NCBI gene
summary says "Is expressed in dorsal fin and pectoral fin" (listing).

Limits: qRT-PCR shows transcript, not protein. It does not tell which isoform (see C2). I did not see
absolute levels, only fold changes.

**Status: satisfied** (transcript level, zebrafish fin).

### C5 — cell, spatial: residue 200 must sit in a membrane-embedded, ordered segment
The claim says low pLDDT at 200 should not be read as disorder. For that to apply, the segment around 200
must be structured. For a polytopic transporter, that means the protein reaches a membrane and the segment
lies in or at the edge of a bilayer-spanning helix. Generic bound: the hydrophobic stretch containing or
flanking residue 200 should be about the length of a TM helix, roughly 17–25 residues (about 2.5–3.8 nm at
0.15 nm per residue, matched to a bilayer hydrophobic core of about 3 nm within a factor of about 1.3).

**Check:**
- *Membrane localisation, zebrafish:* **not measured.** The NCBI/Alliance summary says "Predicted to be
  located in basolateral plasma membrane" (listing). I found no zebrafish localisation experiment. The
  search covered PubMed for "slc43a2a" (0 hits; the paper uses "lat4a") and the Daane 2021 full text,
  which reports no localisation data.
- *Membrane localisation, human/mouse (cross-species):* UniProt Q8N370 gives "Cell membrane; multi-pass"
  with experimental evidence (ECO:0000269) and basolateral membrane by similarity (ECO:0000250). Guetg et
  al. 2015 (J Physiol; read-level: search-summary) report mouse Lat4 at the basolateral membrane of
  enterocytes and kidney tubule cells, with knockout mice as controls.
- *Segment topology:* UniProt annotates human TM helices 177–197 and 203–223. Both are **predicted**
  (ECO:0000255, sequence analysis), not measured. Human T193, which aligns to zebrafish T200, falls inside
  the predicted 177–197 helix near its end. My own Kyte–Doolittle 19-residue windows centred on zebrafish
  185–215 range from 0.54 to 1.94. The window centred on 200 scores 0.67, below the conventional 1.6 TM
  threshold. Windows from 209 onwards are 1.39–1.94, and only those centred on 212 and 215 pass 1.6.
  Hydropathy alone therefore puts residue 200 near the end of a helix or in a short connecting stretch, not
  clearly inside one. All of this is prediction.

No measured value contradicts the constraint, and none satisfies it.

**Status: open.** The zebrafish subject is unmeasured. The human and mouse data are cross-species. Topology
is predicted only.

---

## 2. Summary

| # | scale | kind | status | basis |
|---|---|---|---|---|
| C1 | dna | existence | **satisfied** | codon ACA at GRCz13ab chr15:31,121,333 (derived); T200K/*nr21* observed in zebrafish (Daane 2021, full-text) |
| C2 | dna | existence | **open** | Ensembl 577 aa vs RefSeq 153 aa disagree; genetic evidence favours the long form |
| C3 | dna | existence | **satisfied** | human, mouse and zebrafish-paralogue sequences align across 195–205 with conserved Thr (derived); depth unknown |
| C4 | cell | existence | **satisfied** | *lat4a* qRT-PCR in zebrafish pectoral and dorsal fins (Daane 2021, full-text) |
| C5 | cell | spatial | **open** | zebrafish localisation unmeasured; TM placement of 200 predicted only and ambiguous |

**No constraint is unsatisfiable.** No measured number contradicts the claim at either adjacent scale.

**Biggest result:** C2. The claim measured coverage on the Ensembl 577-aa model. NCBI's current reference
annotation (GRCz13ab) has no residue 200 at all. Anyone who reruns the PDB70 or structure search must say
which gene model they used, or the result will not reproduce.

**Second:** C3 and Daane's "conserved domain" agree with the claim's scope clause. Sequence-level coverage
of 195–205 exists, and Thr is conserved in these four sequences, even though PDB70 has none.

## 3. Sources and read-levels

| source | used for | read-level |
|---|---|---|
| Daane et al. 2021 Curr Biol, PMC9172250 | T200K = *nr21*, gain-of-function, fin qRT-PCR, alleles dmh26/mh152 | full-text |
| EBI UniParc UPI00062E34B4 | 577-aa sequence, ENSDARP00000138218 xref (active) | full record |
| EBI Search (ensembl_gene index) | ENSDARP00000138218 → ENSDARG00000036848; transcript IDs | listing |
| NCBI Gene 393221 / NP_956545.1 / NC_141035.1 (GRCz13ab) | RefSeq model, gene summary, genomic sequence | full record |
| UniProt Q8N370, Q8CGA3, Q5PR35 (EBI Proteins API) | orthologue/paralogue sequences, human topology/localisation | full record |
| ZFIN ZDB-GENE-040426-964 and genotype pages | allele names | search-summary (site returned 503) |
| Guetg et al. 2015 J Physiol (mouse Lat4 knockout) | mouse basolateral localisation | search-summary |
| Ensembl REST / website | — | could-not-access (proxy 403) |
| repository.library.noaa.gov | — | could-not-access (DNS blocked) |

```swarm-entail
{"source_claim": 306, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "Position 200 of the queried protein must correspond to an in-frame genomic codon from which a single nucleotide substitution yields Lys (i.e. a Thr codon of the form ACA or ACG).",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Codon 200 = ACA at NC_141035.1:31121333-31121335 (GRCz13ab, zebrafish), located by unique six-frame match of 8-14 aa peptides spanning residue 200; ACA->AAA is a single C>A change (derived). The T200K allele nr21 (dmh26) was observed by sequencing in zebrafish (Daane et al. 2021).",
      "satisfied_evidence": "literature",
      "note": "Daane JM et al. 2021 Curr Biol 31:5052, PMC9172250 (full-text): 'identified a nonsynonymous mutation (T200K) in a conserved domain of ... lat4a'. Codon identity is my own computation; the paper does not state the nucleotide change in the text read (Fig S2 not read). Ensembl model is GRCz11-based; check done on GRCz13ab."},
    {"target_scale": "dna", "kind": "existence",
      "statement": "An expressed transcript must include the exon encoding residue 200, i.e. the full-length 577-aa gene model must correspond to a real product rather than an annotation artefact.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Sources disagree. Ensembl ENSDARG00000036848 has a 577-aa product (UniParc UPI00062E34B4, ENSDARP00000138218 active). NCBI RefSeq gene 393221 on GRCz13ab has a single protein NP_956545.1 of 153 aa, identical to the long model to about residue 140 and then divergent, with no residue 200. Genetic evidence (T200K phenotype reverted by in-cis frameshifts) implies a product containing residue 200 is made, but that is inference, not a transcript measurement.",
      "satisfied_evidence": "unknown",
      "note": "Searched: NCBI Protein 'slc43a2a AND Danio rerio' (1 record, 153 aa); EBI Proteins API gene=slc43a2a (two 153-aa entries; TrEMBL A0A0R4IP58 577-aa xref inactive). Not done: RNA-seq/EST reads spanning the codon-200 exon. Ensembl was unreachable (proxy 403)."},
    {"target_scale": "dna", "kind": "existence",
      "statement": "Homologous coding sequences outside PDB70 must exist that align across codons 195-205, so that a sequence-database MSA can in principle be non-empty there.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Global BLOSUM62 alignments (my computation) of zebrafish slc43a2a to human SLC43A2 Q8N370 (76.6% identity), mouse Q8CGA3 (75.4%) and zebrafish slc43a2b Q5PR35 (78.3%) each align 195-205 gaplessly (ASSAVTFPGIK / ASSAVTFPGVK) with Thr at the T200 position (human/mouse T193, slc43a2b T222).",
      "satisfied_evidence": "derived",
      "note": "Three sequences only; this shows existence, not depth. UniRef/BFD depth was not measured. Daane et al. 2021 (full-text) call the site 'a conserved domain' (author's claim; basis in Fig S2, not read). Consistent with the claim's scope clause."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "The gene must be transcribed in zebrafish cells of the tissue where the T200K phenotype manifests (fin).",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "lat4a (slc43a2a) qRT-PCR in zebrafish pectoral and dorsal fins across wild-type, nr21/+ and lof/+ genotypes, with no significant difference in expression (Daane et al. 2021, Fig 4E).",
      "satisfied_evidence": "measured",
      "note": "Daane et al. 2021 Curr Biol, PMC9172250 (full-text). Zebrafish. Transcript-level only; isoform not resolved; fold changes only. NCBI/Alliance summary 'expressed in dorsal fin and pectoral fin' (listing)."},
    {"target_scale": "cell", "kind": "spatial",
      "statement": "Residue 200 must lie in an ordered, membrane-associated segment: the product must reach a cell membrane, and the hydrophobic stretch containing or adjoining residue 200 must be of transmembrane-helix length matched to bilayer hydrophobic thickness.",
      "quantity": "length of hydrophobic helical segment containing/adjoining residue 200",
      "lo": 17, "hi": 25, "units": "residues (~2.5-3.8 nm at 0.15 nm/residue)",
      "status": "open",
      "satisfied_by": "Zebrafish membrane localisation not measured (NCBI/Alliance: 'Predicted to be located in basolateral plasma membrane'). Human SLC43A2 is at the cell membrane by experiment (UniProt Q8N370, ECO:0000269) and mouse Lat4 is basolateral (Guetg et al. 2015), both cross-species. Human TM 177-197 and 203-223 are predicted only (ECO:0000255); aligned residue T193 falls inside predicted TM 177-197. My Kyte-Doolittle 19-residue window centred on zebrafish residue 200 = 0.67 (below 1.6 threshold); windows centred at 212 and 215 pass (1.74, 1.94). All topology is prediction.",
      "satisfied_evidence": "unknown",
      "note": "Negative scope: PubMed 'slc43a2a' = 0 hits (paper uses 'lat4a'); Daane 2021 full text has no localisation data; ZFIN not directly accessible (503). No measured value contradicts the constraint; zebrafish is unmeasured, so open rather than unsatisfied."}
  ]}
```
