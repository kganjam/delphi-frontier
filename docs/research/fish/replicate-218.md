# Replicate 218: independent re-derivation of the correction to claim 90 (slc43a2a residue 200 / T200K)

**Question as given:** "Correction to claim 90 (which corrected 82)". The inputs are in
`docs/research/fish/challenge-90.md` on branch `claude/slc43a2-t200k-challenge-wkixy4`.

**What I derived:** I built a genome-based, full-length slc43a2a protein model and used it to
re-derive the quantities claim 90 is about: slc43a2a residue 200, the slc43a2a/slc43a2b register at
that position, the slc43a2b residue homologous to slc43a2a-200, and how NP_956545.1 comes to be
153 aa.

## 0. Contamination disclosure (read this first)

- I read **`challenge-90.md` in full** and the commit message of that branch. The task named it as
  the input location. It is the text of claim 90 (value: slc43a2a-200 = unknown, register +22,
  homologous slc43a2b residue = Thr222, truncation = "frameshift"). So I knew claim 90's numbers
  before I started. I did not take any of them as an input. I recomputed every number below from
  NCBI records I fetched myself.
- I did **not** read claim 218's own record (`challenge-218.md` on branch
  `claude/slc43a2-t200k-numbering-m30txd`) until §6, after my derivation and all computed numbers
  were finished. I found it while looking for the recorded value to compare against.

## 1. Result

| Quantity | My value | Kind |
|---|---|---|
| slc43a2a residue 200 (full-length, genome-based model) | **Thr (T200)**, context `SSAV`**T**`FPGIK` (196–206) | **calculated**: my own gene prediction, not an observation or annotation |
| Register slc43a2a→slc43a2b at residue 200 | **+22** (gapless block model 62–287 ↔ b 84–309) | calculated |
| slc43a2b residue homologous to slc43a2a-200 | **Thr222** (NP_001008585.1) | calculated alignment; the residue identity was read from the record |
| slc43a2b residue 200 | Met | read from the record |
| Full-length slc43a2a model length | 571 aa, 13 coding exons, every intron GT…AG | calculated |
| Why NP_956545.1 is 153 aa | **not a frameshift**. Its source cDNA joins exon-3 sequence directly to the gene's own 3'UTR, about 27 kb downstream, skipping exons 4–13 at a non-canonical junction | calculated: my mapping of the cDNA onto the genome |

**Uncertainty.** Residue 200 = Thr depends on one discrete choice: the exon-3 splice donor.
- With the GTATGT donor at the end of a 56-nt exon 3 (my choice), residue 200 = **Thr**.
- With the alternative GTGATC donor 12 nt upstream (a 44-nt exon), every downstream residue
  shifts by +4, and residue 200 becomes **Ile** (model residue 204).
- A ±1 residue error would give Val (199) or Phe (201).

No transcript confirms the exon-3 donor or anything downstream of it, so this is a prediction. I
would put it at "likely", not "established". Other caveats: the model has a 15-aa N-terminal loop
variant (§3), and I could not cross-check against Ensembl (§5).

## 2. Inputs, with sources and read-levels

All fetched on 2026-11-04 via NCBI E-utilities `efetch`/`esummary`, except where stated.

| Input | Source | Read-level |
|---|---|---|
| NP_956545.1 sequence (153 aa, my count) | NCBI protein FASTA | full-text |
| NP_001008585.1 sequence (592 aa; residue 200 = M, residue 222 = T, my count) | NCBI protein FASTA | full-text |
| NM_200251.2, 3230 bp. CDS 175..636 translates exactly to NP_956545.1 + stop (I checked this). COMMENT: "PROVISIONAL REFSEQ … derived from BC047854.1"; "RNAseq introns :: partial sample support" | NCBI nuccore FASTA + GenBank flatfile | full-text |
| Gene 393221 (slc43a2a): chr15, NC_141035.1 31099368–31139242, `exoncount` 5. Gene 494042 (slc43a2b): chr10 | NCBI gene esummary | listing |
| NC_141035.1:30950000–31300000 (GRCz13ab, strain M-AB) genomic sequence | NCBI nuccore FASTA | full-text |
| NC_133190.1:30870000–30920000 (GRCz12tu, strain Tübingen) genomic sequence | NCBI nuccore FASTA | full-text |
| UniProt slc43a2a entries: Q7ZUS0 and A0A8N7V006, both unreviewed, both 153 aa, both cross-referencing NP_956545.1. No full-length slc43a2a in UniProt (query: gene slc43a2/slc43a2a/slc43a2b, organism 7955) | rest.uniprot.org TSV | listing |
| Ensembl | rest.ensembl.org: proxy `CONNECT tunnel failed, response 403` | could-not-access |
| Tools: miniprot (github lh3/miniprot, commit 81f9b93), Biopython 1.88 PairwiseAligner (BLOSUM62, open −11, extend −1) | — | — |

## 3. Derivation, step by step

**3a. Does the slc43a2a locus contain the missing coding sequence?** I took 30-aa windows of
slc43a2b (step 15) and searched each against a six-frame translation of the 350 kb chr15 window,
using local alignment. Every window from b1 to b585 finds a strong hit (scores 67–178, against
about 40 for noise). All hits are on the + strand, in order, between 31101396 and 31136055, which
is inside the annotated slc43a2a gene span. The downstream exons exist in the genome.

Example hits:
- b196–225 → `LPNMFGDLRSTFIALMIGSYASSAVTFPG` at about 31121258
- b241–270 → `LVWAGCAGLVFINCFFNWPLEPFPGPEDMD`

**3b. Spliced model.** I ran miniprot with slc43a2b as the query against the chr15 window. It
returned a 586-aa slc43a2a model. That model carries a 15-aa insertion
`VIRLLNLSLALSNPP` between `…LCREA` and `GNGTGHN…`, from an exon-2 acceptor 45 nt upstream.

The BC047854-derived transcript (NM_200251.2 / NP_956545.1) is experimental evidence, and it uses
the downstream acceptor (`…REA|GNGTGHN…`). So I removed the 15 aa, which gives a **571-aa model**.

I then re-aligned that model to the genome with miniprot. It returns 13 CDS exons, every intron
GT…AG. Exon lengths in nt are 160/229/56/77/93/134/203/144/127/133/74/124/162, which sum to 1716,
i.e. 571 codons + stop. Residue 200 falls in exon 5 (NC_141035.1 31121258–31121350, model residues
175–205).

The model is identical to NP_956545.1 for residues 1–139, where both read `…SASFAISCIL`. After
that, the genome reads `ISYGASDPQ|NLSILIFF…` and the cDNA reads `NSVTRTASVQLYYQ*`.

**3c. Second assembly.** miniprot with the 571-aa model against GRCz12tu (another strain) gives a
571-aa translation identical at every position, with residue 200 = T. This shows the sequence
agrees across the two assemblies and the model can be spliced in both. It does **not** discover the
exon structure independently, because the model was the query.

**3d. Residue 200 and the register.** I aligned the model globally to NP_001008585.1. The aligned
blocks are:

| slc43a2a model | slc43a2b | offset |
|---|---|---|
| 1–61 | 1–61 | +0 |
| 62–287 | 84–309 | +22 |
| 290–294 | 310–314 | +20 |
| 296–399 | 315–418 | +19 |
| 400–571 | 421–592 | +21 |

Identity is 452/568 aligned columns = 79.6%.

So model residue 200 = T maps to b 200 + 22 = **222 = T**, and b200 = M maps to model 178. The
local context is identical: a `ASSAVTFPG` / b `ASSAVTFPG`.

**3e. Exon-3 donor check.** The genome at exon 3 reads
`GTGCCTCGTTTGCTATCTCCTGCATCCTGATTTCATACGGAGCCAGTGATCCTCAAAG|GTATGT`. There is a second GT
candidate (`GCCA|GTGATC`) 12 nt upstream. I chose the 3' donor for two reasons:
1. GTATGT matches 5 of 6 positions of the consensus GTRAGT; GTGATC matches 4 of 6.
2. The 56-nt exon keeps `SYGASDPQ` gapless against slc43a2b `AYGASNPN`.

This choice is the main uncertainty in the result (§1).

**3f. Why the RefSeq is 153 aa.** I mapped 20-nt pieces of the cDNA to the genome:
- cDNA nt 541 → 31107827 (exon 2)
- cDNA nt 565 → 31109597 (exon 3)
- cDNA nt 589 onward (`CTGAATAGTGTTACACGCAC…`) → 31136618, 31136642, 31136654, …, 31136726

So the cDNA jumps from about 29 nt into exon 3 straight to a position about 450 nt *past the model
stop codon* (the model stop is at about 31136163–165). Neither side of the junction is a GT/AG
splice site. The genome after `…CATCCTG` reads `ATTTCA`.

I also translated the NM_200251.2 sequence downstream of the CDS in all three frames and aligned
each against slc43a2b 156–592. The best scores were 36–39, which is noise. A frameshift would have
left slc43a2b-homologous coding sequence in another frame. None is there.

The 13 non-homologous C-terminal residues are therefore read from the gene's own 3'UTR. The
"2594 bp 3'UTR" is mostly genuine 3'UTR. Exon skipping, or more likely a cDNA cloning/RT artifact,
explains the truncation. A frameshift does not.

## 4. Comparison with claim 90's inputs (author's claim vs my inference)

Claim 90 says, and I agree:
- 153 aa is an annotation artifact.
- The register is +22 near aa 95–140.
- slc43a2b-222 = Thr is the homolog of slc43a2a-200.

Claim 90 also says:
- **"constant +22 offset through aa 140":** my alignment gives +0 over aa 1–61 and +22 only from
  aa 62. That is a minor wording point.
- **"frameshift-truncated":** my inference is that this is wrong (§3f).
- **"slc43a2a residue 200 is unknown":** it was unknown from the records claim 90 used. From the
  genome, my calculated value is Thr, subject to the exon-3 donor caveat.

## 5. Negative searches and their scope

- **No full-length slc43a2a protein record exists.** Scope: UniProt REST only, gene names
  slc43a2/slc43a2a/slc43a2b, organism 7955, queried 2026-11-04.
- **Ensembl was not checked** (could-not-access, proxy 403). An Ensembl gene model is the obvious
  independent check on the exon-3 donor and the 13-exon structure, and it remains undone.
- **No RNA-seq or EST evidence** for the exon-3/exon-4 junction was examined. I did not search SRA
  or EST databases.

## 6. Comparison with the recorded value (done after §1–§5 were finished)

The recorded value is in `challenge-218.md` on `claude/slc43a2-t200k-numbering-m30txd` (read-level:
full-text, read after my derivation). Claim 218 records **value 222**, i.e. slc43a2b-Thr222 is the
residue homologous to slc43a2a-200. It also states that slc43a2a residue 200 is **UNKNOWN** and
that the truncation is a frameshift.

- **On the recorded value 222: I AGREE.** I get +22 at residue 200 and b222 = Thr.
- **On "slc43a2a residue 200 = UNKNOWN": I disagree.** My calculated value is Thr. The challenge
  document on that branch reaches the same conclusion by its own route: Thr200, the same five exon-1
  to exon-5 coordinates, the same GRCz12tu replication, and the same exon-3 donor caveat
  (alternative → Ile200 / Val226).
- **On "frameshift": I disagree.** The challenge document also calls it a non-canonical
  cDNA-junction artifact.
- **One disagreement with that challenge, which I am leaving unresolved:** it reports 10 coding
  blocks spanning 31101303–31133964. My model has 13 exons ending at 31136165, with the C-terminal
  exon (b541–592 homolog) at 31136004–31136165. This does not affect residue 200.

These two derivations agree, but both are genome predictions that rely on the same exon-3 donor
choice. That makes their agreement weaker evidence than an independent transcript would be.

```swarm-replication
{"claim_id": 218, "my_value": "slc43a2b residue homologous to slc43a2a-200 = Thr222 (register +22, gapless slc43a2a 62-287 <-> slc43a2b 84-309); slc43a2a residue 200 itself = Thr in my genome-based 571-aa 13-exon model (calculated, contingent on the 56-nt exon-3 GTATGT donor; alternative 44-nt donor gives Ile200)", "agrees": true, "note": "I independently reproduce the recorded value 222 (Thr), but the claim's accompanying statements that slc43a2a residue 200 is unknown and that NP_956545.1 is frameshift-truncated are not supported: the genome yields Thr200 (prediction) and the 153 aa arises from a non-canonical cDNA junction into the gene's own 3'UTR, not a frameshift."}
```
