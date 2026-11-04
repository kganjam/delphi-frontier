# Claim 185 — entailments at the `protein` scale

**Source claim (scale `dna`, evidence: measured):**
> BUILD BLOCKER: every UniProt slc43a2a entry (Q7ZUS0, A0A8N7V006) and RefSeq NP_956545.1 are 153 aa -- a truncated gene model that CANNOT carry a residue 200, so the T200K substitution is unrepresentable in the databases anyone would reach for first. Only Ensembl GRCz11 has the full-length product

**Adjacent scale checked:** `protein`.
**Date of all database queries:** 2026-11-04.

## Bottom line

All four checked constraints are **satisfied** by database records I retrieved today. One more (evidence for the full-length product at the transcript level) stays **open**. No measured value contradicts the claim. There is one disagreement between sources. UniProt says its Ensembl-derived full-length entries were *deleted from Ensembl*, but UniParc lists the same Ensembl translations as *active*. I report both below and do not settle it.

**Access limits, which bound everything below.** The proxy refused `rest.ensembl.org`, `www.ensembl.org`, `useast.ensembl.org` and `ftp.ensembl.org` (connect rejected). I could not read Ensembl directly. Everything I say about Ensembl comes second-hand from **UniParc cross-references** and the **EBI Search `ensembl_gene` index**. Neither of these tells me the assembly. So the claim's phrase "Ensembl **GRCz11**" is **not verified** here. I verified only that active Ensembl translations exist. `zfin.org` also refused the connection.

## Sources (with read-level)

| # | Source | What was read | Read-level |
|---|---|---|---|
| S1 | UniProtKB Q7ZUS0, A0A8N7V006 (rest.uniprot.org, FASTA + flat file) | sequences, DR/FT/PE/DT lines | full-text (database record) |
| S2 | UniProtKB search `gene:slc43a2a AND organism_id:7955` | all hits | listing |
| S3 | NCBI Protein NP_956545.1, AAH47854.1 (efetch / esummary) | sequence, length | full-text (database record) |
| S4 | NCBI Gene 393221 (esummary, elink gene→protein) | location history, exon count, linked proteins | full-text (database record) |
| S5 | UniParc search `gene:slc43a2a AND taxonomy_id:7955`; UniParc UPI000188A62B, UPI00062E34B4, UPI0001A2C44F (JSON) | sequences, cross-references with active flags and dates | full-text (database record) |
| S6 | UniProtKB F1Q5Y9, A0A0R4IP58, F1Q850 | inactive-reason fields | full-text (database record) |
| S7 | EBI Search `ensembl_gene` for slc43a2a, taxon 7955 | gene IDs | listing |
| S8 | UniProtKB Q8N370 (human SLC43A2 / LAT4) | sequence, TRANSMEM features | full-text (database record) |
| S9 | UniProtKB search `gene:slc43a2b AND organism_id:7955` | lengths | listing |
| S10 | NCBI Nucleotide search `slc43a2a[gene] AND Danio rerio[orgn]` | hits | listing |
| — | Ensembl REST / web / FTP; ZFIN | — | could-not-access (proxy 403 / connect rejected) |

## Observations (measured = read from a database record today)

- **Measured.** Q7ZUS0 is 153 aa, A0A8N7V006 is 153 aa, and NP_956545.1 is 153 aa. All three have identical sequences (S1, S3). The UniProt search returns exactly these two slc43a2a entries (S2). The NCBI Protein search `slc43a2a[gene] AND Danio rerio[orgn]` returns only NP_956545.1. Gene→protein elink also returns AAH47854.1, which is 153 aa (S3, S4).
- **Measured.** NCBI Gene 393221 annotates the gene with **5 exons**. The current RefSeq annotation (RS_2026_08) is on GRCz13ab (NC_141035.1) and on an alternate assembly (NC_133190.1). It is **not** on GRCz11 (S4, S10).
- **Measured.** UniParc holds two full-length slc43a2a sequences. Their Ensembl cross-references are flagged `active=True`, last updated 2026-03-30 (S5):
  - UPI000188A62B is **571 aa**. Cross-refs: Ensembl **ENSDARP00000120945** (active) and VEGA OTTDARP00000030624 (active). The former UniProt entry F1Q5Y9 is inactive.
  - UPI00062E34B4 is **577 aa**. Cross-ref: Ensembl **ENSDARP00000138218** (active). The former UniProt entry A0A0R4IP58 is inactive.
  - A third Ensembl translation, ENSDARP00000045860 (153 aa, UPI0001A2C44F), is **inactive** (last updated 2018-01-12).
- **Measured.** Residue 200 is **T** in both full-length sequences. Local context: residues 190–210 = `MIGSYASSAVTFPGIKVIYDL` (S5).
- **Measured, but sources disagree.** UniProt marks F1Q5Y9 and A0A0R4IP58 as `DELETED — "Deleted from sequence source (ENSEMBL)"`, with UniParc dating that to 2022-12-14 (S6). UniParc, in the same records, flags the Ensembl translations behind those entries as **active**, updated 2026-03-30 (S5). I cannot tell from here which is current, because Ensembl is inaccessible. *Inference, not checked:* one possible reconciliation is that UniProt stopped importing these translations, for example after a reference-proteome or assembly switch, while Ensembl kept them. That is speculation.
- **Calculated.** I ran a local pairwise check (Biopython PairwiseAligner, BLOSUM62, gap −10/−0.5, global):
  - The 153-aa product matches the 571-aa product for exactly **residues 1–139**, then diverges: short `…SVTRTASVQLYYQ` vs long `…SYGASDPQN…`.
  - The 571 and 577 isoforms match for residues 1–366, so position 200 means the same residue in both.
  - Zebrafish T200 aligns to human SLC43A2 (Q8N370) **T193**. The human context `MIGSYASSAVTFPGIKLIYDA` aligns to the zebrafish context with 18 of 21 positions identical.
  - Human T193 falls inside the UniProt TRANSMEM 177..197 segment of Q8N370 (S8). That segment is a sequence-based prediction, not a structure.
  - *Inference:* the 153-aa model's last 14 residues probably come from an alternative exon or read-through. I did not examine this at the exon level.

## Constraints and checks

### C1 — existence: a database translation of the gene must carry a residue 200
*Requirement:* if the claim is true, at least one public, current protein product of this locus must be ≥ 200 aa. Otherwise "only Ensembl has the full-length product" would be false.
**Status: satisfied** (measured; seen via UniParc, not Ensembl directly). ENSDARP00000120945 (571 aa) and ENSDARP00000138218 (577 aa) are flagged active in UniParc (S5). EBI Search confirms the Ensembl gene ENSDARG00000036848 = slc43a2a (S7).
**Caveats:**
- The assembly (GRCz11) is **not verified**, because Ensembl itself could not be reached.
- UniProt's "deleted from Ensembl" note (S6) contradicts UniParc's active flag. See Observations.

### C2 — range: every UniProt and RefSeq slc43a2a protein record must be shorter than 200 aa
*Quantity:* length of each active UniProtKB / RefSeq slc43a2a protein. *Bound:* [1, 199] aa.
**Status: satisfied** (measured). Q7ZUS0, A0A8N7V006 and NP_956545.1 are all 153 aa (S1, S3).
**Scope of the "every":** the UniProtKB search `gene:slc43a2a AND organism_id:7955` returned exactly 2 entries (S2). The NCBI Protein search `slc43a2a[gene] AND Danio rerio[orgn]` returned 1 (S3). I did not search by sequence (BLAST). An entry filed under a different gene symbol would therefore be missed. The three full-length UniProt entries that did exist (F1Q5Y9, A0A0R4IP58) are now inactive (S6).

### C3 — range: the full-length product must have a family-typical length
*Requirement:* an SLC43 transporter product should be about the length of its orthologue and paralogue, not some other fragment that happens to pass residue 200.
*Quantity:* full-length slc43a2a translation length. *Bound:* [500, 650] aa. **I set this bound myself (derived)**: human SLC43A2 is 569 aa (S8), and zebrafish slc43a2b is 592–598 aa (S9).
**Status: satisfied** (measured). The lengths are 571 and 577 aa (S5).
**Calculated support:** the 571-aa product has 442 positions identical to human SLC43A2 after global alignment.

### C4 — existence: the wild-type residue at position 200 of the full-length product must be threonine
*Requirement:* "T200K" presupposes that residue 200 is T in the reference product. If it were not T, the substitution would be misnamed, whatever the database lengths.
**Status: satisfied** (measured).
- Residue 200 is T in both ENSDARP00000120945 and ENSDARP00000138218 (S5).
- The two isoforms are identical through residue 366 (calculated), so the numbering does not depend on which isoform is used.
- *Calculated:* this T aligns to human T193 in a conserved stretch (18 of 21 identical). That residue lies in a predicted transmembrane segment. The orthologue match is calculated, and the TM placement is a UniProt sequence prediction.

### C5 — existence: the full-length product must have transcript- or protein-level support, not just a gene-model prediction
*Requirement:* for the claim's practical message ("use Ensembl's full-length product") to hold, something beyond a model prediction should show that the ≥ 200-aa product is made.
**Status: open.**
- What I checked: the NCBI Nucleotide search `slc43a2a[gene] AND Danio rerio[orgn]` (S10) found only NM_200251 (3230 nt, the 153-aa RefSeq transcript) and two chromosome records. No full-length mRNA is filed under that gene symbol.
- What I could **not** check: Ensembl's supporting-evidence tracks (inaccessible), ENA/EST/RNA-seq data, and any proteomics. The VEGA cross-ref OTTDARP00000030624 (S5) suggests the 571-aa model went through manual (Havana/VEGA) curation. *That is my inference from the cross-ref's existence; I did not read the VEGA record's evidence.*
- This is "not checked within reach". It is **not** "searched and found nothing".

```swarm-entail
{"source_claim": 185, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "At least one current public translation of the locus must be long enough to contain residue 200 (the full-length product must exist somewhere).",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Ensembl translations ENSDARP00000120945 (571 aa) and ENSDARP00000138218 (577 aa), flagged active (last updated 2026-03-30) in UniParc UPI000188A62B / UPI00062E34B4; Ensembl gene ENSDARG00000036848 = slc43a2a per EBI Search.",
      "satisfied_evidence": "measured",
      "note": "UniParc full-text records, EBI Search ensembl_gene listing, read 2026-11-04. Ensembl itself could not be accessed (proxy refused), so the assembly (GRCz11) is NOT verified. Disagreement preserved: UniProt marks F1Q5Y9/A0A0R4IP58 'Deleted from sequence source (ENSEMBL)' (2022-12-14) while UniParc flags the same Ensembl xrefs active."},
    {"target_scale": "protein", "kind": "range",
      "statement": "Every active UniProtKB and RefSeq protein record for the gene must be shorter than 200 aa.",
      "quantity": "protein record length", "lo": 1, "hi": 199, "units": "aa",
      "status": "satisfied",
      "satisfied_by": "Q7ZUS0 = 153 aa, A0A8N7V006 = 153 aa, NP_956545.1 = 153 aa (identical sequences); AAH47854.1 = 153 aa.",
      "satisfied_evidence": "measured",
      "note": "UniProt REST and NCBI efetch, full-text records. Scope of 'every': UniProtKB query gene:slc43a2a AND organism_id:7955 (2 hits); NCBI Protein slc43a2a[gene] AND Danio rerio[orgn] (1 hit); no BLAST, so records under other symbols would be missed. Former full-length UniProt entries F1Q5Y9 and A0A0R4IP58 are inactive."},
    {"target_scale": "protein", "kind": "range",
      "statement": "The full-length product must have a length typical of an SLC43-family transporter (comparable to orthologue/paralogue), not an unrelated longer fragment.",
      "quantity": "full-length translation length", "lo": 500, "hi": 650, "units": "aa",
      "status": "satisfied",
      "satisfied_by": "Ensembl-derived products are 571 and 577 aa; human SLC43A2 Q8N370 = 569 aa; zebrafish slc43a2b = 592-598 aa.",
      "satisfied_evidence": "measured",
      "note": "Bounds are derived by me from Q8N370 and slc43a2b lengths (UniProt). Calculated support: 442/571 positions identical to human SLC43A2 in a global BLOSUM62 alignment (Biopython)."},
    {"target_scale": "protein", "kind": "existence",
      "statement": "The reference residue at position 200 of the full-length product must be the wild-type residue named by the substitution (threonine), unambiguously across isoforms.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Residue 200 = T in both ENSDARP00000120945 and ENSDARP00000138218 (context 190-210 MIGSYASSAVTFPGIKVIYDL); isoforms identical through residue 366.",
      "satisfied_evidence": "measured",
      "note": "UniParc full-text sequences. Calculated (not observed): aligns to human SLC43A2 T193, within UniProt-predicted TRANSMEM 177..197 of Q8N370; 18/21 identical in the 21-residue window. The 153-aa product matches the 571-aa product only for residues 1-139 then diverges (calculated)."},
    {"target_scale": "protein", "kind": "existence",
      "statement": "The full-length (>=200 aa) product must be supported by transcript- or protein-level evidence, not only by a gene-model prediction.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Not determined. NCBI Nucleotide slc43a2a[gene] AND Danio rerio[orgn] found only NM_200251 (the 153-aa transcript) plus chromosome records. A VEGA xref (OTTDARP00000030624) exists for the 571-aa product, which suggests manual curation (inference, evidence not read).",
      "satisfied_evidence": "unknown",
      "note": "Scope: only a gene-symbol-field NCBI Nucleotide search was done. Ensembl supporting evidence, ENA/EST, RNA-seq and proteomics were not checked (Ensembl could-not-access). This is 'not checked within reach', not 'searched and found nothing'."}
  ]}
```
