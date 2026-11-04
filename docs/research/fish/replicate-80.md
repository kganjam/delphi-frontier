# Replicate 80: lat4a = slc43a2a by the paper's own mapping

**Question (answer withheld from me):** Which zebrafish gene is the "lat4a" of Daane et al. 2021? Resolve it from the paper's own mapping evidence, not from how similar the names are.

**My value:** lat4a = **slc43a2a** (NCBI GeneID 393221, chromosome 15). Confidence: high for the gene. The residue numbering rests on my own computed gene model, described below.

Independence note: I worked this out before looking at any earlier answer. `fish-alleles/README.md` and `docs/research/fish/` do not exist on this branch, so I read nothing there. I opened the recorded resolution only after my derivation was finished (see Comparison).

## Sources and how much of each I read

| # | Source | Read-level | Used for |
|---|---|---|---|
| S1 | Daane JM et al. 2021, *Curr Biol*, "Modulation of bioelectric cues in the evolution of flying fishes". PMID 34534441, PMC9172250, doi:10.1016/j.cub.2021.08.054. Fetched as PMC XML with efetch. | full-text (main text, STAR Methods, figure legends). The supplement (Data S1 xlsx, PDF) was **not read**. | the authors' mapping claims, qPCR primers, residue numbers |
| S2 | NCBI Gene esummary for 393221 | full record | symbol slc43a2a; chr 15; NC_141035.1:31,099,368–31,139,242; 5 exons |
| S3 | NCBI Gene esummary for the SLC43 paralogs: 494042 slc43a2b, 334395 slc43a1a, 100009631 slc43a1b, 572234 slc43a3a, 556206 slc43a3b | full record | chromosome of each paralog |
| S4 | NC_141035.1 (GRCz13ab chr15), positions 31,000,000–31,250,000, fetched with efetch | full sequence | primer placement and exon assembly |
| S5 | NM_200251.2 / NP_956545.1 (slc43a2a RefSeq) | full record | cDNA exon boundaries; the RefSeq protein is only 153 aa |
| S6 | NP_689559.1, human SLC43A2 isoform 2 (569 aa); XP_009303545.1 and NP_001008585.1, zebrafish slc43a2b | full sequence | homology guide; paralog control |
| S7 | UniProt search for zebrafish slc43a2*/lat4* | listing | confirms no full-length slc43a2a protein exists in UniProt (153 aa only) |
| — | Ensembl REST, ZFIN | could-not-access (blocked by the egress proxy with 403) | — |

## What the authors claim (from S1, quoted)

- "we mapped nr21 to chromosome 15 and identified a nonsynonymous mutation (T200K) in a conserved domain of the L-type amino acid transporter, lat4a"
- The convergent flying-fish substitution is "F326L" in Lat4a.
- The lat4a qPCR primers are 5′-ACGCAGGACGGCAATAAA-3′ and 5′-GCTGAAGATACTCCGCATGAA-3′.
- The alleles are lat4 nr21 (dmh26) and lat4a del (mh152). CRISPR guides target "the third coding exon of lat4a".
- In the main text, the only place "Slc43a2" appears is the title of reference 17 ("Lat4 (Slc43a2)", a mouse paper). **The authors print no zebrafish symbol or accession for lat4a.** The mapping below is therefore my inference from their evidence, not their statement.

## My derivation (inference, with every input shown)

1. **Chromosome (S1 + S3, observed records).** The authors put nr21 on chromosome 15. Of the six zebrafish SLC43-family genes in NCBI, only slc43a2a is on chromosome 15:

   | Gene | Chromosome |
   |---|---|
   | slc43a2a | 15 |
   | slc43a2b | 10 |
   | slc43a1a | 14 |
   | slc43a1b | 1 |
   | slc43a3a | 1 |
   | slc43a3b | 14 |

   This is necessary but not sufficient: it only rules out the paralogs.

2. **The authors' own primers (S1 + S4; exact string match I computed).**
   - Forward primer: exact match on the + strand at chr15:31,123,338.
   - Reverse primer: its reverse complement matches exactly at 31,128,510.
   - Both lie inside the slc43a2a gene span (31,099,368–31,139,242) and face each other, about 5.2 kb apart in the genome (they span an intron, as qPCR primers usually do).
   - Neither primer matches any of the five slc43a2b mRNAs (S6) or the truncated NM_200251.2.
   - Scope of this negative: I searched only the 250 kb window plus those mRNAs. I did not BLAST the whole genome.

3. **Residue numbering (computed gene model, not an observed protein).** No database has a full-length slc43a2a protein: NP_956545.1 and the UniProt entries are 153 aa. So I built the coding sequence myself:
   - I aligned human SLC43A2 against 3-frame translations of S4 to get 13 collinear exon hits.
   - I took exon 1 through the first 20 nt of exon 4 from the NM_200251.2 cDNA exon structure. (The cDNA leaves the gene model after that point.)
   - I placed the remaining splice sites at canonical GT…AG dinucleotides.

   Resulting exons (GRCz13ab chr15):
   ```
   31101396-31101555, 31107621-31107849, 31109596-31109651, 31109732-31109808,
   31121258-31121350, 31121521-31121654, 31123205-31123407, 31128502-31128645,
   31131765-31131891, 31132026-31132158, 31132412-31132485, 31133814-31133937,
   31135938-31136168
   ```
   - All 12 junctions are GT-AG.
   - The CDS is 1,782 nt plus the stop codon, encoding **593 aa**.
   - Residues 1–139 are identical to the cDNA-derived NP_956545.1.
   - Only one donor was ambiguous: the exon ending at 31,109,808 (GTAAGT) versus 31,109,820. The 31,109,820 choice inserts 4 aa ("VSVH") that neither human SLC43A2 nor zebrafish slc43a2b has, so I used 31,109,808.

   Results:
   - **Residue 200 = T, codon ACA at chr15:31,121,333.** T200K would be ACA→AAA, a single C→A change. This is consistent with the authors' "T200K".
   - **Residue 326 = F.** This is consistent with "F326L". The paper may number F326 on a medaka or other reference, but zebrafish F326 fits either way.
   - Paralog control: zebrafish slc43a2b has M at 200 and D at 326 in both XP_009303545.1 and NP_001008585.1, so it does not fit.
   - Caveat: under the rejected donor choice, the Thr would sit at 204 instead of 200. So the residue match depends on that splice-site choice. The choice is supported by homology, but it is not observed.

   Assembled protein (computed):
   ```
   MAPTLATAFSRRWWMAITAVIENLLFSAVLLGWGSLLIMLKSEGFYSYLCREAGNGTGHN
   VSESENGTMNATRLEEEDNLQMNGWPICKEQDEMLNLAFTIGSFLLSAITLPLGIIMDKY
   GPRKLRLLGSASFAISCILISYGASDPQNLSILIFFALALNGFGGMCMTFTSLTLPNMFG
   DLRSTFIALMIGSYASSAVTFPGIKVIYDLGAAFITILLVWAGCAGLVFINCFFNWPLEP
   FPGPEDMDFTVKIKFSWLGFDHKITGKQFYRQVTTVGRRLSVGNSMKTNPKQLATQDGNK
   LCLSTLDLEVQCKPEEESQSFMRSIFSPIFMLSLITMCVTQLRLIFYMGAMNNILESLAD
   GDLTKVSTYTSIFGVLQLLCLLTAPVIGYIMDWRLKECEEENEKQSAKDPTQPKKRDRQI
   QKISNATRAFIFTNLLLVGFGMTCLVPNLYVQILSFVLHTIVRGFIHSAVGGLYAAVYPS
   SQFGSLTGMQSLISALFALLQQPLFMAMMGPLEGDPLWSHVCWVHQKLPLNLIGSCFSLQ
   VNVGLLVLSMLGFCLPSYLLCYGRRLRREKAEREEDPKIYVQINNSTNTEAFV
   ```

There is no arithmetic beyond these coordinate offsets. The number "200" comes from translating the assembled CDS codon by codon, starting at the ATG at 31,101,396.

## What stays open

- The NCBI record for slc43a2a currently has a 153-aa protein and 5 exons. My 13-exon, 593-aa model **disagrees with that annotation**. I treat the RefSeq as a truncated cDNA model, because the cDNA leaves my model inside exon 4 and stops early. I have not resolved this against Ensembl, which I could not reach.
- I did not read the Data S1 supplement, Figures S2D–S2F (the mapping interval), or the ZFIN records for the alleles dmh26 and mh152.
- The authors never state which zebrafish gene lat4a is. Every link from their evidence to slc43a2a above is my inference.

## Comparison with the recorded value (read only after the derivation)

The record is `data/genomics/lat4a_resolution_v3.json` on `main`. It concludes **slc43a2a** (ZDB-GENE-040426-964, ENSDARG00000036848) by a different route:

- the medaka gene ENSORLG00000009715 is labelled lat4a in Data S1G/H and slc43a2a in Data S1J;
- Ensembl lists one-to-one orthology from that medaka gene to the zebrafish gene;
- the chromosome-15 location is consistent.

The record lists the T200K/F326L residue check as "still inconclusive", because NP_956545.1 is 153 aa. My computed full-length model is not an observed protein, but it provides that check: T at 200 and F at 326.

**AGREE.** The two derivations are independent: theirs uses supplement naming plus Ensembl orthology; mine uses the chromosome, the authors' primers and the residue numbers. They share only the chromosome-15 fact.

```swarm-replication
{"claim_id": 80, "my_value": "lat4a = slc43a2a (NCBI GeneID 393221, chr15); paper qPCR primers map exactly inside it, and a computed 593-aa GT-AG model gives T200 and F326 (slc43a2b: M200, D326)", "agrees": true,
  "note": "Independent of the record's supplement+Ensembl-orthology route, I reach slc43a2a from the chr15 location, the authors' own lat4a primers and the T200/F326 residues; the residue numbering depends on my computed gene model, because NCBI's slc43a2a protein is truncated at 153 aa."}
```
