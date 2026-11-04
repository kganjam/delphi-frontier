# Claim 306: entailments at the `dna` and `cell` scales

**Source claim (protein scale, evidence: measured).** PDB70 (pdb70_220313) gives zero
alignment coverage at residue 200 of zebrafish slc43a2a (ENSDARP00000138218, 577 aa). The
maximum per-position depth is 2 and the median is 0; 474 of 577 positions have no coverage,
including every position from 195 to 205. The claim's scope note says that low PDB70 depth is
evidence about how well this transporter family is covered by solved structures. It is *not*
evidence that the position is evolutionarily unconserved.

**Subject animal throughout: zebrafish (*Danio rerio*)**, unless a line says otherwise. Every
number below is about zebrafish except where the animal is named. No flying-fish measurement is
used to judge any constraint. The one mouse source and the one flying-fish result are marked
as the animal they come from.

---

## 0. What the claim does and does not commit to

The claim is a measurement of how one sequence aligns against one database. On its own it
requires almost nothing physical. What it does presuppose is that "residue 200 of zebrafish
slc43a2a" is a real thing: a real codon in a real gene, carried in a product that real cells
make. If that fails, the measurement is about an annotation artefact. The claim also names a
variant, T200K. So the variant must be a possible DNA change, and it is worth knowing whether
the variant is real. The constraints below are those presuppositions, written so they can be
checked.

The claim's consequence, "low pLDDT at 200 would mean the alignment ran out, not disorder", is
a protein-scale statement. It entails nothing at dna or cell, so it is not propagated.

---

## 1. Constraints and checks

### D1. existence (dna): a Thr codon at codon 200 inside a coding exon

*Requirement.* The zebrafish genome must contain a coding sequence whose translation reproduces
ENSDARP00000138218, with codon 200 encoding Thr inside an exon.

*Check: **satisfied** (sequence lookups I did myself on public assemblies; the sequences are measured data).*
- The protein sequence comes from UniParc UPI00062E34B4 (577 aa). That record is active for
  Ensembl ENSDARP00000138218 under gene name slc43a2a, taxon 7955, and lists
  UniProtKB/TrEMBL A0A0R4IP58 as inactive. Residue 200 = **T**, with local context
  `MIGSYASSAV[T]FPGIKVIYDL` (residues 190–210). [read-level: full record, rest.uniprot.org]
- I translated the region in six frames and matched the protein exactly. Codon 200 is **ACA**
  in all three zebrafish assemblies I checked:
  - GRCz11 (Tübingen), NC_007126.7: chr15:28,390,801–28,390,803 (+ strand)
  - GRCz12tu (Tübingen), NC_133190.1: chr15:30,897,361–30,897,363
  - GRCz13ab (M-AB), NC_141035.1: chr15:31,121,333–31,121,335 (inside NCBI Gene 393221
    slc43a2a, chr15:31,099,368–31,139,242)
  - The flanking sequence is identical in all three:
    `…GGCTCGTATGCTTCATCCGCTGTC ACA TTCCCAGGAATTAAG|GTAAAT…`
- **Inferred from the sequence (my inference, not an annotation):** the exon carrying codon 200 encodes
  residues ~175–206. Its 3′ end is a GT splice donor 15 nt downstream of the codon. So
  residue 200 sits about 6 codons from an exon–intron boundary, which is outside the canonical
  donor consensus.

### D2. conservation (dna): the open reading frame balances to 577 codons plus a stop

*Requirement.* The exon model must hold the reading frame across every splice junction and
sum to 577 sense codons plus one stop codon: 1,731 coding nt, 1,734 with the stop.

*Check: **open**. I found most of the evidence but not all of it.*
- I searched GRCz11 within ±150 kb of codon 200 for exact 8-mer peptide matches that occur only
  once (my own calculation from the sequence). They recover **569/577 residues** in **13 frame-coherent
  blocks** on the + strand, spanning about chr15:28,370,864–28,405,635 (~35 kb).
- The codon after residue 577 (V, `GTC`) is **TGA**, so the stop is exactly where a 577-codon
  ORF puts it.
- **Not recovered:** residues 149, 318 and 366–371. These are probably codons split across
  junctions or a micro-exon, but I did not verify that. I did not run a spliced aligner, and
  Ensembl's own exon model could not be fetched (rest.ensembl.org was blocked, HTTP 403 at the
  proxy). Until those 8 residues are placed, the full 1,731-nt balance is unconfirmed.
- **Disagreement between annotations, kept as is:** NCBI RefSeq models slc43a2a as
  NM_200251.1, a 5-exon transcript whose CDS (176..637) encodes NP_956545.1, only **153 aa**.
  NP_956545.1 is identical to the 577-aa protein for residues 1–139 and then diverges. Neither
  NM_200251.1 nor NP_956545.1 contains residue 200. The UniProt slc43a2a entries currently live
  (Q7ZUS0, A0A8N7V006) are also the 153-aa form. Only the Ensembl/UniParc model contains the
  residue the claim is about.

### D3. existence (dna): a DNA change that makes T200K, and an allele that carries it

*Requirement.* Some nucleotide change in codon 200 must turn Thr into Lys. If T200K is to be
more than hypothetical, an allele carrying it must exist.

*Check: **satisfied**.*
- **Inferred from the genetic code (mine):** Lys is AAA or AAG. From ACA, the only single-nucleotide route is
  **ACA→AAA**, a C>A change at codon position 2 (a G:C→T:A transversion).
- **The allele exists (literature, zebrafish).** Daane et al. 2021, *Curr Biol* 31:5052–5061.e8,
  doi:10.1016/j.cub.2021.08.054, PMID 34534441, PMC9172250. [read-level: full-text, author
  manuscript via NCBI efetch. Figures and supplementary data not viewed]
  - The authors write that the dominant short-fin ENU mutant **nr21** (ZFIN allele **dmh26**)
    was "mapped … to chromosome 15" and carries "a nonsynonymous mutation (T200K) in a
    conserved domain of the L-type amino acid transporter, lat4a". It was found by
    heterogeneity mapping with exome capture designed on Zv9.
  - The text I read gives the substitution only as "predicted T200K". It does not give the
    nucleotide change, and it does not name the reference transcript. That this paper's T200K is the same residue as ENSDARP00000138218 T200 is **my
    inference**. It is consistent but not proven: this model has T at 200, and it also has F at
    326, which matches the paper's other numbered substitution, F326L.

### C1. existence (cell): zebrafish cells make the product that carries residue 200

*Requirement.* Some zebrafish cell must make the transcript, and the protein, that contains
residue 200. Otherwise PDB70 is being queried about a model that no cell makes. This matters
here because the RefSeq form (D2) does not contain residue 200.

*Check: **satisfied** at tissue level (literature, zebrafish, plus my mapping of the primers onto the gene).*
- **Transcript (Daane et al. 2021, full-text).** qRT-PCR detects lat4a in adult zebrafish
  pectoral, dorsal and caudal fins (Fig. 4E caption: "no significant difference in lat4a
  expression across fins and genotypes"). The authors do not say which isoform. **My mapping:**
  their lat4a primers (F `ACGCAGGACGGCAATAAA`, R `GCTGAAGATACTCCGCATGAA`) land in GRCz11 exons
  that encode residues ~251–317 and ~319–365 of the 577-aa model. The two sites are ~5.2 kb
  apart, so the amplicon spans an intron. Neither primer occurs in NM_200251.1. So the signal
  the paper measured comes from a transcript that has exons of the long form and not the 153-aa form.
- **Product (same paper, genetic evidence).** nr21 is dominant, and frameshift alleles made by
  CRISPR in cis to it (L106Rfs39) restore wild-type fins. The authors conclude that nr21 is
  gain-of-function, and that zebrafish lacking lat4a have no fin phenotype. **My inference:** a
  dominant effect of T200K that a frameshift in cis cancels requires the residue-200-containing
  product to be translated in fin tissue.
- **Scope.** This is tissue level, adult fin. No cell type is resolved, and I did not look for
  in-situ or single-cell data. The alliance summary in NCBI Gene 393221 says "expressed in dorsal
  fin and pectoral fin" [read-level: listing]. ZFIN itself returned HTTP 503 and could not be
  read [could-not-access].

### C2. existence (cell): the transporter sits in a cell membrane

*Requirement.* The claim describes the protein as a member of a transporter family. Read
generically, that requires the product to reach a membrane where it can transport. Of the five
constraints this is the weakest entailment, because it follows from how the claim describes the
protein, not from the measurement itself.

*Check: **open** (wrong-animal evidence only).*
- **Zebrafish:** I found only predicted localisation. UniProt's automatic annotation gives
  "basolateral cell membrane; multi-pass" (ARBA) for the 153-aa slc43a2a entries, and Phobius
  predicts 12 transmembrane segments for paralogue slc43a2b (Q5PR35). Predictions are not
  observations. [read-level: listing]
- **Mouse, not zebrafish:** Guetg et al. 2015, *J Physiol* 593:1273–1289, PMID 25480797, report
  Lat4 staining on the basolateral side of small-intestine, proximal-tubule and thick-ascending-
  limb epithelia, absent in knockouts. They also report low-affinity uniport (K0.5 ≈ 5 mM)
  measured in *Xenopus* oocytes. [read-level: search-summary]
  This does not satisfy C2: it is a different animal and a different gene copy (the mammalian
  single-copy orthologue versus the zebrafish "a" paralogue).
- **Scope of the negative.** I searched NCBI nuccore/gene, UniProt, Europe PMC and the web for
  zebrafish slc43a2a/lat4a localisation. I found no observed zebrafish localisation. I did not
  search ZFIN expression or antibody records, which were unreachable. This is "not found within
  that scope", not "looked for and absent".

---

## 2. What the checks mean for claim 306

- **Nothing refutes it.** No measured value at dna or cell contradicts the claim. None of the
  constraints is `unsatisfiable`.
- **The question is concrete.** The residue and variant are real. T200 is a real ACA codon
  in three assemblies (D1). T200K is a real zebrafish ENU allele with a dominant fin phenotype
  (D3). The long isoform that carries it is expressed in fins (C1). So the claim's limit — that
  PDB70 can support no conservation argument at residue 200 — applies to a residue that matters
  in zebrafish.
- **The authors and the claim do not disagree.** Daane et al. call T200 part of "a conserved
  domain", based on their own multiple alignment (Fig. 3C, not viewed; I do not know which
  species are in it). That is the case the claim's scope note anticipates: a sequence-database
  alignment can be deep where PDB70 is empty. It does not contradict claim 306. It also shows
  that a conservation argument about T200K has to come from that kind of alignment, not from PDB70.
- **Flying fish (named as a different animal).** The convergent lat4a substitution in flying
  fishes and flying halfbeaks is **F326L**, not T200K (Daane et al. 2021, full-text). It is a
  different residue in different animals. It neither supports nor refutes anything about
  zebrafish residue 200, and must not be cited as if it did.
- **Leads, not entailments.** Two things did not follow from the claim and were not checked.
  The ENU base-change spectrum: whether C>A is a common ENU outcome. I quote no figure because I
  have none sourced. A splice effect: the codon lies 15 nt upstream of a donor.

## 3. Sources and access

| Source | Used for | Read-level |
|---|---|---|
| UniParc UPI00062E34B4 (rest.uniprot.org) | 577-aa sequence, T at 200 | full record |
| UniProtKB search, *D. rerio* slc43a2a/b | 153-aa entries; predicted localisation | listing |
| NCBI NC_007126.7, NC_133190.1, NC_141035.1 (efetch) | codon 200, exon blocks | full sequence |
| NCBI NM_200251.1 / NP_956545.1; Gene 393221 | RefSeq 153-aa model; gene span; alliance summary | full record / listing |
| Daane et al. 2021 Curr Biol, PMC9172250 | nr21 T200K, phenotype, primers, F326L | full-text (author MS; figures/supplement not viewed) |
| Guetg et al. 2015 J Physiol, PMID 25480797 (mouse) | Lat4 localisation in mouse | search-summary |
| rest.ensembl.org | exon model | could-not-access (proxy 403) |
| zfin.org gene/figure pages | expression, allele records | could-not-access (HTTP 503) |
| EVA v1 segments API, drerio_grcz11 | natural variants at codon 200 | returned 0 variants over a 200 kb window, which I treat as a broken query rather than a true negative; nothing concluded |

```swarm-entail
{"source_claim": 306, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "The zebrafish genome must contain a coding sequence that translates to the queried 577-aa protein, with codon 200 encoding Thr inside a coding exon.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Codon 200 = ACA (Thr) in GRCz11 NC_007126.7 chr15:28390801-28390803, GRCz12tu NC_133190.1 chr15:30897361-30897363 and GRCz13ab NC_141035.1 chr15:31121333-31121335, inside NCBI Gene 393221 (slc43a2a); exon encodes ~res 175-206 and ends at a GT donor 15 nt after the codon",
      "satisfied_evidence": "measured",
      "note": "Zebrafish only. Protein: UniParc UPI00062E34B4 (active xref ENSDARP00000138218; inactive TrEMBL A0A0R4IP58), read-level full record. Genomic: NCBI efetch, full sequence; codon located by my own exact six-frame peptide match. Exon boundary is inferred from the sequence."},
    {"target_scale": "dna", "kind": "conservation",
      "statement": "The exon model must keep the reading frame across every splice junction and balance to 577 sense codons plus one stop.",
      "quantity": "coding nucleotides excluding stop", "lo": 1731, "hi": 1731, "units": "nt",
      "status": "open",
      "satisfied_by": "569/577 residues recovered in 13 frame-coherent + strand blocks over ~35 kb of GRCz11 chr15, with TGA immediately after residue 577; residues 149, 318, 366-371 not placed",
      "satisfied_evidence": "derived",
      "note": "Zebrafish GRCz11. Crude unique 8-mer exact matching, no spliced aligner; Ensembl exon model could-not-access (proxy 403). Annotation disagreement kept: RefSeq NM_200251.1/NP_956545.1 is a 5-exon 153-aa model identical to res 1-139 only and lacks residue 200."},
    {"target_scale": "dna", "kind": "existence",
      "statement": "A nucleotide change in codon 200 must exist that converts Thr to Lys, and for T200K to be more than hypothetical an allele carrying it must exist.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "ACA->AAA (single C>A, G:C->T:A) is the only single-nucleotide route (my inference from the code); ENU allele lat4a nr21 (ZFIN dmh26) carries 'predicted T200K', mapped to chr15 by exome-capture heterogeneity mapping",
      "satisfied_evidence": "literature",
      "note": "Zebrafish. Daane et al. 2021 Curr Biol 31:5052, doi:10.1016/j.cub.2021.08.054, PMC9172250, full-text author manuscript (figures/supplement not viewed). Paper does not state the nucleotide change or the reference transcript; equating its T200 with ENSDARP00000138218 T200 is my inference (consistent: model also has F at 326, matching the paper's F326L numbering)."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "Some zebrafish cell must express the transcript and protein product that contains residue 200 (not only the short isoform that lacks it).",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "lat4a qRT-PCR signal in adult pectoral, dorsal and caudal fins with primers that (my mapping) sit in long-isoform exons encoding ~res 251-365 and are absent from NM_200251; dominant gain-of-function fin phenotype of T200K reverted by in-cis frameshift L106Rfs39 implies the residue-200 product is translated in fin tissue",
      "satisfied_evidence": "literature",
      "note": "Zebrafish. Daane et al. 2021 (full-text): Fig. 4E caption, Methods primer sequences, Fig. 3A-D. Tissue-level only, no cell type resolved; in-situ/single-cell data not searched; ZFIN could-not-access (503). Primer-to-exon mapping is my derivation on GRCz11."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "As a member of a transporter family, the product must be delivered to a cellular membrane where it can transport substrate.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "No observed zebrafish slc43a2a/lat4a localisation found; only predictions (UniProt ARBA 'basolateral cell membrane', Phobius 12-TM for paralogue slc43a2b). Mouse Lat4 is observed basolateral in intestine and kidney epithelia, but that is a different animal and a single-copy orthologue",
      "satisfied_evidence": "unknown",
      "note": "Mouse source: Guetg et al. 2015 J Physiol 593:1273, PMID 25480797, search-summary; cross-species, so not used to satisfy. Negative scope: NCBI nuccore/gene, UniProt, Europe PMC and web search for zebrafish slc43a2a/lat4a localisation; ZFIN expression/antibody records not searched (503). 'Not found in this scope', not 'shown absent'. Weakest entailment: follows from the claim's 'transporter family' wording, not from the measurement."}
  ]}
```
