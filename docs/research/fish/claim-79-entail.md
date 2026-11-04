# Claim 79: entailments at the protein scale

**Source claim (scale `dna`, evidence: measured).** The gene symbol `lat4a` used by
Daane et al. does not resolve in UniProtKB or NCBI Gene for *Danio rerio*. Four
positive controls (kcnh2a, slc43a2a, slc43a2b, kcnk5b) resolved with the same query
form, so the zero is a real absence and not a malformed query.

**Adjacent scale examined:** `protein`.
**Date of all database queries:** 2026-11-04.

## Summary

| # | kind | requirement at the protein scale | status |
|---|------|----------------------------------|--------|
| C1 | existence | A *D. rerio* protein product exists, under some official identifier, for the gene the authors call `lat4a`. The absence is of a **name**, not of a **protein**. | **satisfied** (derived): slc43a2a |
| C2 | range | Zero *D. rerio* protein records carry `lat4a` as a name or synonym in any field. | **satisfied** (measured): 0 records |
| C3 | spatial | The reference protein the authors' coordinates refer to is at least 200 residues long, because they report a substitution at residue 200. | **unsatisfied**: every curated slc43a2a protein record is 153 aa |
| C4 | existence | The wild-type reference protein has Thr at position 200, the "T" of the reported T200K. | **unsatisfied**: no curated record has a residue 200 at all. The nearest Thr in a reconstruction I calculated is at about 204 |

There is no `unsatisfiable` finding. C3 comes closest, but I did not raise it to
`unsatisfiable`, for the reason given under C3: the contradicting number is a
gene-model annotation, not a measured protein length.

---

## Sources and read-levels

| Source | What it is | read-level |
|---|---|---|
| Daane JM et al. 2021, *Curr Biol* 31:5052–5061.e8, doi:10.1016/j.cub.2021.08.054, PMID 34534441, PMCID PMC9172250 | The paper that uses `lat4a` | **full-text** (author manuscript, main text and STAR Methods, fetched as PMC XML). Supplementary Figures S2D–S2I and the Figure 3C alignment *image*: **could-not-access** (only the caption text was read) |
| PubMed 34534441 | Abstract | abstract |
| NCBI Gene 393221 (slc43a2a), 494042 (slc43a2b) | Gene summaries: aliases, chromosome, exon count, annotation release | listing (esummary) |
| RefSeq NP_956545.1 (coded_by NM_200251.2:175..636), NP_001008585.1, XP_009303545.2 and the XP_0871254xx / XP_087077278 isoforms | Protein sequences | full record (sequence fetched) |
| UniProtKB Q7ZUS0, A0A8N7V006 (slc43a2a); Q5PR35, A0A8M1N3P6, A0ACD6B803 (slc43a2b); Q8N370 (human LAT4/SLC43A2) | Protein sequences and annotation fields | full record (sequence and fields fetched) |
| GenBank NC_141035.1:31,089,368–31,149,242 (*D. rerio* chr15, header "GRCz13ab") and NC_141030.1:28,013,048–28,051,843 (chr10, the slc43a2b span ±10 kb) | Genomic sequence | full record (sequence fetched) |
| ZFIN figures ZDB-FIG-221222-34/35, publication ZDB-PUB-210803-12 | Figure captions and gene links | **could-not-access** (zfin.org returned HTTP 503. The franklin/crick mirrors were refused by this session's egress proxy.) A web-search summary of those pages was seen, but I rely on nothing from it that the full text does not also say. |
| Ensembl REST (`lookup/symbol/danio_rerio/slc43a2a`) | Alternative gene model | **could-not-access** (refused by the egress proxy) |

---

## What the authors say (author's claims, quoted from the full text)

- "we mapped nr21 to chromosome 15 and identified a nonsynonymous mutation (T200K) in a
  conserved domain of the L-type amino acid transporter, lat4a (Figures 3C and S2D–S2F)."
- The frameshift revertant allele in cis is named "L106Rfs39" (Figure 3A caption).
- The Figure 3C caption reads: "Multiple sequence alignment of Lat4a showing the predicted
  T200K substitution of nr21".
- "CRISPR guide RNAs (gRNAs) were designed against the third coding exon of lat4a".
  The paper lists five gRNA target sequences and a qPCR primer pair for lat4a in the key
  resources table.
- Allele names in the paper: "lat4 nr21 (dmh26), and lat4a del (mh152)". The authors use
  both `lat4` and `lat4a` for the same gene.
- The authors cite mammalian Lat4 as Slc43a2 (refs 16, 17: Bodoy et al. 2005 *JBC*;
  Guetg et al. 2015 *J Physiol*). Those two papers were read at **listing** level only,
  as entries in Daane's reference list.
- The text I read names **no** zebrafish accession, Ensembl ID or RefSeq ID for lat4a.
  The reference sequence behind "position 200" is therefore not stated.

---

## C1: existence. A protein product exists under an official identifier

**Requirement.** Claim 79 says the zero is a real absence of the *symbol*. For the paper's
genetics to refer to anything, a protein-coding gene matching the authors' description
(an LAT4/SLC43A2-family transporter mapping to chr15) must exist under another official
identifier.

**Status: satisfied. Evidence: derived.** The protein is **slc43a2a** (NCBI Gene 393221,
chr15; RefSeq NP_956545.1; UniProtKB Q7ZUS0 and A0A8N7V006). This assignment is **my
inference**. The authors never write "slc43a2a". It rests on four independent checks,
each of which I ran:

1. **Chromosome (database listing).** NCBI Gene places slc43a2a on chr15 (NC_141035.1:
   31,099,368–31,139,242) and slc43a2b on chr10. The authors mapped nr21 to chr15.
2. **The authors' oligos (sequence match, calculated by exact string search).** All five
   lat4a gRNA protospacers (20-mers minus the 5′ "GG" added for SP6) occur exactly in
   the slc43a2a genomic window. They fall within about 180 bp of each other, at
   chr15:31,107,617 (g1, reverse strand), 31,107,666 (g2), 31,107,669 (g3),
   31,107,672 (g4) and 31,107,775 (g5, reverse strand). Both lat4a qPCR primers also occur
   there: forward at 31,123,338 and reverse at 31,128,510 (reverse strand). **None** of
   the seven sequences occurs in the slc43a2b span (chr10, ±10 kb), so the paralog is
   excluded.
3. **Exon placement (calculated).** In my six-frame scan (below), the gRNA cluster lies
   in the coding segment that aligns to slc43a2b residues 84–151. That is the third
   LAT4-homologous coding segment along the gene, consistent with "third coding exon",
   provided a small second exon (slc43a2b 55–83) lies between the first two segments.
   I did not locate that small exon in the scan. It may be too short for my 25-aa cutoff.
4. **Residue 106 (record).** NP_956545.1 residue 106 is **Leu**
   (context `IGSFLLSAITLP`, residues 101–112). This matches the "L" in the authors'
   revertant allele L106Rfs39, and it lies inside that same third coding segment.

**Scope and caveats.** ZFIN, which would state the authors' own gene link, was not
reachable (see the sources table), so the curated ZFIN allele-to-gene association was not
checked. The gene-level NCBI aliases for slc43a2a are `si:dkey-118k5.2, slc43a2,
zgc:56271`. Neither `lat4` nor `lat4a` appears among them.

## C2: range. The symbol is also absent at the protein-record level

**Requirement.** If the DNA-level zero is real and not an artefact of a gene-symbol-only
query, then a *D. rerio* protein search across all fields, including synonyms, must also
return zero. Quantity: the number of *D. rerio* UniProtKB entries matching `lat4a` or
`lat4`. Bounds: [0, 0].

**Status: satisfied. Evidence: measured (database query, 2026-11-04).**
- UniProtKB `lat4a AND organism_id:7955`: **0** entries. `gene:lat4a AND organism_id:7955`:
  **0**. `lat4 AND organism_id:7955`: **0**. `gene:lat4 AND organism_id:7955`: **0**.
- Control, same query form: UniProtKB `lat4a` with no organism filter returns 2 entries,
  both unrelated (Q1ELU5, a *Lachesana tarabaevi* spider protein, and A0A9P6H1T5,
  `LAT4A`, *Nosema granulosis*). The query form therefore works and returns hits when
  the string exists.
- NCBI Gene `lat4a` (any field, any organism): **0**.
- Positive controls: `gene:slc43a2a AND organism_id:7955` returns Q7ZUS0 and A0A8N7V006.
  `gene:slc43a2b AND organism_id:7955` returns Q5PR35, A0A8M1N3P6 and A0ACD6B803.
  Human Q8N370 lists `LAT4` as a gene synonym. "LAT4" is therefore a human synonym of
  SLC43A2, and `lat4a` appears to be the authors' teleost-paralog extension of it.
  That last point is **my inference**.

## C3: spatial. The reference protein must be at least 200 residues long

**Requirement.** The authors give a residue coordinate of 200, so the protein sequence
their numbering refers to must be at least 200 residues long. Quantity: reference protein
length. lo = 200, hi = null, units = residues.

**Status: unsatisfied, as far as any curated record goes.**
- **Measured (curated annotation): 153 aa.** RefSeq NP_956545.1 (NM_200251.2, CDS
  175..636; NCBI annotation release RS_2026_08, 5 exons), UniProtKB Q7ZUS0 ("Evidence at
  transcript level", not flagged as a fragment) and UniProtKB A0A8N7V006 ("Predicted")
  are all **153 aa**. NP_956545.1 is the only slc43a2a protein that NCBI Protein returns.
  No XP_ model was found.
- The paralog does reach length 200: slc43a2b is 592 aa (NP_001008585.1, Q5PR35) or
  598 aa (XP_009303545.2, A0ACD6B803). Human LAT4 (Q8N370) is 569 aa. But C1 excludes
  slc43a2b as the authors' gene.

**Why this is not `unsatisfiable`.** The 153-aa figure is a gene-model annotation, not a
measured length of the protein *in vivo*. My own six-frame calculation contradicts it as
a full-length description:
- **Calculated, not observed.** I translated chr15:31,089,368–31,149,242 in all six frames,
  split the translations at stop codons, and locally aligned every open segment of at least
  25 aa (BLOSUM62, gap −11/−1) to slc43a2b Q5PR35 and to human Q8N370. LAT4-homologous
  segments on the + strand, all inside the annotated slc43a2a gene span, cover slc43a2b
  residues 1–54, 84–151, 152–181, 196–228, 227–272, 272–338, 338–391, 384–429, 429–474,
  474–498, 492–541 and 538–592. Most local alignment scores are 150–270 (the weakest
  segments score 75–120). This coverage spans essentially the whole slc43a2b length.
- In the region where the NP_956545.1 model leaves the transporter frame, the record and
  the genomic segment diverge. The 153-aa record reads `GSASFAISCI|LNSVTRTASVQLYYQ*`.
  The genomic segment continues instead in the slc43a2b-homologous frame:
  `SASFAISCIL|ISYGASDPQSMYANHLRPLLLILAT` (aligned to slc43a2b 151–181).
- I did not check splice-site consensus, and I did not check whether the segments chain
  into a single uninterrupted ORF. A premature stop or frameshift in this assembly
  (the header reads "strain M-AB") cannot be ruled out from this analysis.

So two things disagree, and I keep both as stated. **The curated records say 153 aa.
The genomic coding capacity, which I calculated, says roughly 570 aa.** No full-length
slc43a2a cDNA or measured protein length was found. Ensembl, the most likely source of
the gene model the authors used (their methods cite Ensembl BioMart downloads from
January 2020), could not be reached. The searches that came up empty: NCBI Protein
(`slc43a2a[gene] AND danio rerio[orgn]`, with and without the RefSeq filter, and the
protein name "solute carrier family 43 member 2" in *D. rerio*) and UniProtKB (gene
name, and protein name "L-type amino acid transporter 4" or "solute carrier family 43
member 2", in organism 7955). Neither database has a slc43a2a entry of 200 aa or more.

## C4: existence. Thr at the authors' position 200 in the wild-type reference

**Requirement.** "T200K" requires a Thr at residue 200 of the wild-type reference protein,
in what the authors call a "conserved domain".

**Status: unsatisfied.** Searched: every *D. rerio* SLC43A2 protein record listed above.
- slc43a2a records (153 aa): **no residue 200 exists.**
- slc43a2b records: residue 200 is **Met** in Q5PR35, XP_009303545.2 and A0ACD6B803
  (context 195–205: `LTLPNMFGDLR`). This rules out a simple paralog mix-up as the source
  of the coordinate.
- Human Q8N370 residue 200 is **Ile**.
- **Calculated reconstruction, not an observation.** I stitched together NP_956545.1
  residues 1–129, the genomic segment `SASFAISCILISYGASDPQSMYANHLRPLLLILAT`, an assumed
  gap of 14 residues (copied from the slc43a2b length between its residues 181 and 196),
  and the genomic segment `LPNMFGDLRSTFIALMIGSYASSAVTFPGIKV`. In this reconstruction the
  nearest Thr residues are at about **189** (`DLRSTFIAL`) and about **204**
  (`SSAVTFPGI`). The Thr at about 204 sits in a motif conserved in slc43a2b
  (`SSAVT…`, Thr 222) and human LAT4 (`SSAVT…`, Thr 193). That motif is a plausible
  match to the authors' phrase "a conserved domain". The exact position depends on the
  assumed gap length, which I did not measure, so I cannot place a Thr at exactly 200.
- The authors' Figure 3C/S2 alignment image, which would settle their numbering, was not
  accessed (only its caption).

**Scope of the negative.** This is "looked and did not find" for curated records, and
"nobody has published the reference sequence" for the authors' numbering: the text names
no accession. It is **not** a contradiction. No measured sequence shows a non-Thr residue
at the authors' position 200 in the authors' reference.

---

## What this means for claim 79

- Claim 79 is **not refuted from below**. At the protein scale the symbol is absent (C2),
  while the protein exists under the official symbol slc43a2a (C1). That is exactly what a
  "real absence of the name" predicts.
- A consequence for downstream claims: anyone reproducing Daane et al. from database
  records will meet two gaps. The name does not resolve, and the T200 coordinate cannot be
  located on any curated slc43a2a protein (C3, C4). Claims that depend on the T200K allele
  should carry this as an open dependency. Resolving it needs the authors' reference
  transcript, the Figure 3C/S2 alignment image, or the Ensembl slc43a2a model, none of
  which this session could reach.

## Reproduction

All queries were run against public REST endpoints on 2026-11-04:
`rest.uniprot.org/uniprotkb/search` (queries as quoted above) and NCBI E-utilities
(`esearch`/`esummary`/`efetch` on gene, protein, nuccore and pmc). The six-frame scan and
the oligo search were short Biopython scripts (`Bio.Align.PairwiseAligner`, local mode,
BLOSUM62, open −11, extend −1, minimum segment 25 aa, minimum reported score 45). Their
outputs are **calculated** results.

```swarm-entail
{"source_claim": 79, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "A Danio rerio protein product must exist, under some official identifier other than the unresolved symbol, for the chr15 LAT4-family gene the authors call lat4a; the absence is of a name, not of a protein.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "slc43a2a (NCBI Gene 393221, chr15; RefSeq NP_956545.1; UniProtKB Q7ZUS0, A0A8N7V006). Assignment inferred by us: all 5 of the authors' lat4a gRNA protospacers and both lat4a qPCR primers match the slc43a2a locus exactly (chr15:31,107,617-31,107,795 and 31,123,338/31,128,510) and none matches the slc43a2b locus; NP_956545.1 residue 106 is Leu, consistent with the authors' L106Rfs39 revertant.",
      "satisfied_evidence": "derived",
      "note": "Daane et al. 2021 Curr Biol 31:5052, PMC9172250 (full-text; oligo table, chr15 mapping, L106Rfs39). NCBI Gene/RefSeq/UniProt records (full record). ZFIN gene link not checked: zfin.org HTTP 503, mirrors blocked by proxy (could-not-access). The authors never write 'slc43a2a'; the mapping is our inference."},
    {"target_scale": "protein", "kind": "range",
      "statement": "The number of Danio rerio protein records carrying the unresolved symbol as a name or synonym in any field must be zero.",
      "quantity": "D. rerio UniProtKB entries matching lat4a or lat4 (all fields, and gene field)", "lo": 0, "hi": 0, "units": "entries",
      "status": "satisfied",
      "satisfied_by": "UniProtKB 'lat4a AND organism_id:7955' = 0, 'gene:lat4a AND organism_id:7955' = 0, 'lat4 AND organism_id:7955' = 0, 'gene:lat4 AND organism_id:7955' = 0; NCBI Gene 'lat4a' any organism = 0. Query-form controls: unfiltered UniProt 'lat4a' returns 2 unrelated non-fish entries; gene:slc43a2a/b in 7955 return 2 and 3 entries.",
      "satisfied_evidence": "measured",
      "note": "Database queries run 2026-11-04 (listing). Scope: UniProtKB (reviewed + unreviewed) and NCBI Gene only; ZFIN aliases not checked (could-not-access). Human Q8N370 lists LAT4 as a synonym of SLC43A2."},
    {"target_scale": "protein", "kind": "spatial",
      "statement": "The reference protein to which the authors' residue numbering refers must be at least as long as the highest coordinate they report (residue 200).",
      "quantity": "length of the reference protein for the lat4a gene", "lo": 200, "hi": null, "units": "residues",
      "status": "unsatisfied",
      "satisfied_by": "No curated slc43a2a protein meets it: RefSeq NP_956545.1 (NM_200251.2, annotation RS_2026_08, 5 exons), UniProtKB Q7ZUS0 and A0A8N7V006 are all 153 aa, and no XP_ model exists. Our six-frame calculation (calculated, not observed) finds LAT4-homologous + strand coding segments within the annotated slc43a2a span covering slc43a2b residues 1-592, implying ~570 aa coding capacity; splice sites and a continuous ORF were not verified.",
      "satisfied_evidence": "unknown",
      "note": "Not marked unsatisfiable: the contradicting 153 aa is a gene-model annotation, not a measured protein length, and the calculated coding capacity disagrees with it; both are preserved. Searched: NCBI Protein (slc43a2a[gene] D. rerio, with and without RefSeq filter; protein name 'solute carrier family 43 member 2') and UniProtKB (gene name; protein names 'L-type amino acid transporter 4' / 'solute carrier family 43 member 2', organism 7955). Ensembl (likely source of the authors' 2020 model) could-not-access (proxy refused)."},
    {"target_scale": "protein", "kind": "existence",
      "statement": "The wild-type reference protein must carry Thr at the authors' position 200 (the T of the reported T200K) within a conserved domain.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "No record places Thr at 200: slc43a2a records (153 aa) have no residue 200; slc43a2b residue 200 is Met (Q5PR35, XP_009303545.2, A0ACD6B803); human Q8N370 residue 200 is Ile. Our stitched reconstruction of slc43a2a (calculated, with an assumed 14-residue gap) puts the nearest Thr at ~189 and ~204, the latter in a SSAVT motif conserved with slc43a2b (Thr222) and human LAT4 (Thr193); exact position not determinable.",
      "satisfied_evidence": "unknown",
      "note": "Daane et al. 2021 (full-text) give no accession for the reference sequence; Figure 3C/S2 alignment images could-not-access (caption only). Negative is 'looked in curated records and did not find' plus 'reference numbering never published', not a measured contradiction."}
  ]}
```
