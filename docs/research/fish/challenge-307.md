# Challenge 307 — adversarial review of [S44] slc43a2a T200K ESM-2 scoring

**Claim under review** (source `harvest:s44-slc43a2a-esm2-scoring-pzc587`, evidence level
`refused`, value `n/a`):

> Not computed: ESM-2 masked-marginal scoring of slc43a2a T200K was blocked twice independently —
> every public slc43a2a reference protein (RefSeq NP_956545.1, UniProt Q7ZUS0/A0A8N7V006) is only
> 153 aa so position 200 does not exist and the 19-substitution site set cannot be built, and all
> ESM-2 weight hosts are denied by this environment's network policy; the allele itself is
> confirmed real, dominant and classified gain-of-function by Daane et al. 2021 (PMID 34534441),
> and the moderate-score prediction plus its falsifiers are registered here before any number
> exists.
>
> KEY: 153 aa (slc43a2a reference protein length; residue 200 lies 46 codons past the in-frame
> stop at mRNA position 634 of NM_200251.2)

**Verdict: REFUTED.** The claim's headline blocker — and the content of its KEY field — is wrong.
Residue 200 of Lat4a does exist; the 153 aa figure is an artifact of a demonstrably broken RefSeq
gene model. The claim's *bottom line* ("not computed") survives, but on one blocker, not two, so
"blocked twice independently" does not hold.

---

## 1. Arithmetic, redone independently from the stated inputs

Done from the primary record, not from the author's working. `NM_200251.2` (read-level:
**full-text**, NCBI E-utilities, 2026-11-04) annotates `CDS 175..636`:

- CDS length = 636 − 175 + 1 = **462 nt** = 462 / 3 = **154 codons** = 153 residues + 1 stop.
  → the 153 aa length is **confirmed**.
- Terminating stop codon therefore occupies **634..636**; I read the bases directly: `TAA`.
- The stop is codon 154. Residue 200 is codon 200. 200 − 154 = **46 codons past the stop**.
  → the "46 codons" figure is **confirmed**.

So the author's arithmetic reproduces exactly. Two precision notes, neither a defect in the number:

1. The stop codon **spans 634–636**; "the in-frame stop at mRNA position 634" is its first base.
2. `NM_200251.2` separately carries a `misc_feature 106..108` annotated
   `/note="upstream in-frame stop codon"` (a `TAG`, in frame with the CDS). The phrase "the
   in-frame stop" is ambiguous between the two features. The author's 46 is computed against the
   terminating stop, which is the correct one.

Protein lengths independently re-fetched (read-level: **full-text** for each):

| Accession | Source | Length | Note |
|---|---|---|---|
| NP_956545.1 | RefSeq | 153 aa | `LOCUS NP_956545 153 aa`; DBSOURCE NM_200251.2 |
| Q7ZUS0 | UniProt (unreviewed) | 153 aa | submission name Si:dkey-118k5.2, from cDNA AAH47854.1 |
| A0A8N7V006 | UniProt (unreviewed) | 153 aa | gene `slc43a2a` |
| **Q5PR35** | **UniProt, paralog `slc43a2b`** | **592 aa** | "Large neutral amino acids transporter small subunit 4" |
| A0ACD6B803 | UniProt, `slc43a2b` | 598 aa | |

`elink` from Gene 393221 returns exactly one RefSeq protein. So the claim's literal statement —
every public slc43a2a *reference protein entry* in RefSeq/UniProt is 153 aa — is **true as
stated, and I verified it independently.** That is also precisely where it goes wrong.

---

## 2. The proxy: a truncated annotation standing in for the protein that matters

**The claim's quantity:** the length of the RefSeq/UniProt `slc43a2a` database entry.
**The quantity that decides feasibility:** the length of the Lat4a protein in whose numbering the
T200K allele is defined, i.e. the gene's actual coding capacity.

Three independent lines show these are not the same thing.

### 2a. The paralog is 4× longer and aligns from residue 1

`slc43a2b` (Q5PR35) is 592 aa. The two proteins are plainly orthologous at the N-terminus:

```
slc43a2a  MAPTLATAFSRRWWMAITAVIENLLFSAVLLGWGSLLIMLKSEGFYSYLC...
slc43a2b  MAPTLATAFARRWWMAVTAIIENLLFSAVLLGWGSLLIMLKSEGFYSYLC...
```

The 153 aa entry ends mid-protein (`...TRTASVQLYYQ`) exactly where the paralog continues. Human
SLC43A2 (LAT4), to which NCBI Gene 393221 records slc43a2a as orthologous, is a ~541 aa 12-TM
transporter. A 153 aa product is not a plausible complete transporter.

### 2b. The RefSeq gene model is visibly broken, and NCBI flags it partial

From the genomic record `NC_141035.1:31,099,368–31,139,242` (read-level: **full-text**):

```
gene  2..>39875                /gene="slc43a2a"
mRNA  join(2..109,1963..2188,8254..8482,10229..10248,37246..>39875)
CDS   join(2029..2188,8254..8482,10229..10248,37246..37298)
```

- The CDS exon lengths are 160 + 229 + **20** + 53 = 462 nt — reproducing the 462 above.
- A **20 bp coding exon** is followed by a **~27 kb skip** (10,248 → 37,246).
- The mRNA is annotated `>39875` — **NCBI itself marks this transcript 3′-incomplete.**
- NCBI Gene 393221 lists `exoncount: 5` over ~40 kb. Human SLC43A2 has ~12 exons.
- 3,230 bp mRNA with a 462 nt CDS leaves a 2,594 nt "3′UTR" behind a 153-codon ORF.

### 2c. The skipped 27 kb contains the missing coding exons — measured, with controls

No BLAST or Biopython in this container, so I wrote a seeded-ungapped-extension tblastn
(BLOSUM62, 4-mer seeds, X-drop 12) and ran `slc43a2b` against the 6-frame translation of the
39,875 bp locus. **This is a computed homology search, not an observation of transcript
structure.** Script: `scripts/hsp.py` in the session scratchpad.

Per this repo's rule 8, controls in both directions:

- **Positive control** (must be found): the 153 aa slc43a2a protein against the locus → HSPs at
  95.1 % and 93.3 % identity, at locus offsets 2029, 8238 and 37251 — **reproducing the annotated
  exon joins exactly**. The method works and the frame bookkeeping is right.
- **Must-fail 1** (composition-matched shuffle of slc43a2b): **0 HSPs** at threshold 40.
- **Must-fail 2** (unrelated protein, human HBB): 1 HSP at score **exactly 40** — i.e. threshold
  40 sits *on* the noise floor. I therefore discount anything near 40 and rely only on HSPs ≫ 40.

Result — slc43a2b HSPs against the slc43a2a locus (all scores ≥ 149 except where noted):

| slc43a2b residues | locus offset | identity | score |
|---|---|---|---|
| 1–54 | 2,029 | 88.9 % | 261 |
| 84–151 | 8,277 | 75.0 % | 267 |
| 152–197 | 10,227–10,364 | 57–78 % | 72–114 |
| **197–228** | **21,891** | **93.8 %** | 155 |
| 227–272 | 22,151 | 87.0 % | 235 |
| 272–309 | 23,836 | 84.2 % | 174 |
| 338–391 | 29,137 | 77.8 % | 209 |
| 384–419 | 32,394 | 75.0 % | 154 |
| 429–474 | 32,657 | 73.9 % | 190 |
| 474–498 | 33,045 | 92.0 % | 119 |
| 492–541 | 34,427 | 84.0 % | 219 |
| 538–592 | 36,631 | 56.4 % | 149 |

The locus carries exons homologous to **the entire 592 aa paralog**, in correct 5′→3′ order, at
56–94 % identity. Every HSP from slc43a2b residue 197 onward falls at offsets 21.9 k–36.6 k —
**inside the 27 kb the RefSeq CDS skips.** The region is annotated as a single gene
(`gene 2..>39875 /gene="slc43a2a"`); no other gene feature occurs in it, so these exons are not a
neighbour's.

Pseudogene alternative, tested and rejected: NCBI Gene 393221 records slc43a2a as "Acts upstream
of or within fin morphogenesis… expressed in dorsal fin and pectoral fin", and Daane et al.
recovered a functional allele. This is an expressed, functional gene with a broken model.

### 2d. The T200K position itself

Anchoring on the HSP pair that shares one exon (slc43a2a 49–129 at offset 8238 ↔ slc43a2b 84–151
at offset 8277), slc43a2a residue 129 corresponds to slc43a2b residue 151, an offset of +22 from
the paralog's N-terminal insertion. Lat4a residue ~200 therefore corresponds to slc43a2b ~222,
which falls in the 93.8 %-identity HSP at locus offset 21,891:

```
slc43a2b   LPNMFGDLRATFIALMIGSYASSAVTFPGVKV
locus-tr   LPNMFGDLRSTFIALMIGSYASSAVTFPGIKV
                     ^ paralogy-corresponding column
```

At that column the locus translation gives **T**, codon **`ACA`**, at
**NC_141035.1:31,121,333**, within an unannotated coding exon spanning
**chr15:31,121,258–31,121,353**. The surrounding stretch
(`TFIALMIGSYASSAVTFPG`) is an unambiguous hydrophobic transmembrane helix.

So: a **threonine**, in a **conserved transmembrane helix**, at the **paralogy-corresponding
position** — inside the 27 kb the reference model discards. This matches Daane et al.'s own
description of T200K as sitting "within a highly conserved transmembrane domain."

**Scope limit, stated beside the finding:** this is a homology-based *computed* reconstruction. I
did **not** complete a full ORF assembly with splice-boundary phasing, so I do **not** certify
that the exact residue index is 200 rather than ~198–202, and I did not read RNA-seq evidence that
these exons are spliced into the mature message (the RefSeq record's own note reads "RNAseq introns
:: partial sample support"). What is certified: the gene's coding capacity extends far past
residue 153, and a Thr in a conserved TM helix sits at the corresponding position. "Position 200
does not exist" is false either way.

---

## 3. The hidden assumption, relaxed

The result is carried by: **"the public reference protein entry is the protein."**

Relaxed — if the reference entry may be a partial annotation — the blocker evaporates. The
operative sequence is the full-length Lat4a ORF (~590 aa by paralogy), obtainable by reconstructing
the ORF across the skipped 27 kb, or from the alignment Daane et al. used. Once that sequence
exists, position 200 is interior and the 19-substitution masked-marginal site set (20 amino acids
minus wild-type Thr = 19) is trivially constructible. The author stopped at a database field where
the gene model, not the biology, was the obstacle.

---

## 4. Is the evidence level honest?

Mixed — good in form, with one real defect.

**Honest:** value `n/a` and evidence level `refused` correctly record that no ESM-2 number was
produced. Nothing calculated is dressed as measured. Registering the prediction and its falsifiers
before any number exists is the right discipline. The arithmetic in KEY is correct and reproduces.

**The defect:** the KEY field presents **153 aa** as "slc43a2a reference protein length" as though
it were the operative fact about the protein. It is an accurate reading of a database field and a
misleading statement about the gene. A correct KEY would read: *"153 aa — the length of a RefSeq
model NCBI flags 3′-partial, containing a 20 bp exon and skipping 27 kb of coding sequence; the
gene's coding capacity is ~590 aa."* The number is right; what it is said to measure is not.

**Second defect — the claim's own citation contains its refutation.** The author cites Daane et al.
2021 for the allele while asserting residue 200 does not exist. That paper's Figure 4 legend
describes "the predicted T200K substitution of nr21 within a highly conserved transmembrane
domain" over a *multiple sequence alignment of Lat4a*. An alignment with a residue 200 in a TM
domain is incompatible with a 153 aa protein. The contradiction was available in the cited source.

**Unverified in the claim, flagged:** "classified gain-of-function." See §5.

---

## 5. Regime / counter-example the author missed

**The published counter-example is the author's own citation.** Read-level for Daane et al. 2021
(PMID 34534441, *Curr Biol* 31(22):5052–5061): **could-not-access** full text. biorxiv.org returned
HTTP 429, zfin.org returned HTTP 503 twice, and I did not retrieve cell.com. What I have is
**search-summary** level, quoting a ZFIN figure-legend record:

- The gene is **lat4a**, which *is* `slc43a2a` (L-type amino acid transporter 4a) — so the claim's
  gene assignment is **correct**. I specifically tested the alternative that T200K belonged to
  `kcnk5b` or `kcnh2a` (the other bioelectric fin genes in this literature); it does not.
- `nr21` is a **dominant** allele from an ENU screen for small adult fins → the claim's "real" and
  "dominant" are **corroborated**.
- The substitution is reported as a **predicted** T200K — predicted from the DNA lesion, not
  observed at the protein level. The claim's word "confirmed" is stronger than the source's
  "predicted."
- Authors generated CRISPR/Cas9 frameshift revertants **in cis** to `nr21`.

On **gain-of-function**: I could not verify that the authors use that classification, and I do not
assert it. My inference, separated from the claim: a *cis* frameshift that reverts the phenotype is
the standard test distinguishing an antimorph/neomorph from a loss-of-function allele, so a
gain-of-function reading is consistent with the described experiment. **Disagreement preserved,
not averaged:** the paper's framing (via ZFIN/figure summaries) has lat4a acting as a *suppressor*
of kcnh2a-driven fin overgrowth, with `nr21` giving *small* fins — consistent with increased
suppression; whereas a secondary popular account (Oceanbites, read-level **search-summary**)
describes the zebrafish lat4a mutation simply as making all fins short, which does not distinguish
mechanism. Anyone relying on "gain-of-function" should read the primary text.

**A second missed regime:** the paralog. Any reviewer who had pulled `slc43a2b` (592 aa) alongside
`slc43a2a` (153 aa) would have seen the 4× discrepancy between duplicates of one teleost gene
immediately. The 153 aa figure is self-flagging next to its own paralog.

---

## 6. What survives

The claim's **conclusion** is right for one of its two stated reasons.

- **Blocker 2 is real, and I confirmed it independently.** Scope of the negative: three URLs across
  two hosts — `huggingface.co/facebook/esm2_t33_650M_UR50D/resolve/main/config.json`,
  `huggingface.co/api/models/facebook/esm2_t6_8M_UR50D`, and
  `dl.fbaipublicfiles.com/fair-esm/models/esm2_t33_650M_UR50D.pt` — all returned
  `CONNECT tunnel failed, response 403` through this session's egress proxy on 2026-11-04. ESM-2
  weights are genuinely unreachable here. (`rest.ensembl.org` is blocked the same way, which is
  likely *why* the author saw only the truncated NCBI/UniProt entries.)
- **Blocker 1 is not real.** Residue 200 exists; the site set can be built.

So "blocked twice independently" is false: there is one blocker. The practical consequence is
real, though — the scoring still cannot be run in this environment, because of the weights, not the
sequence. A future attempt needs network access to ESM-2 weights **and** should carry a
reconstructed ~590 aa Lat4a ORF rather than NP_956545.1. Had the environment allowed weights, the
author's stated blocker would have wrongly aborted a feasible computation.

## Sources and read-levels

| Source | Read-level |
|---|---|
| RefSeq NP_956545.1 (GenPept) | full-text |
| RefSeq NM_200251.2 (GenBank, feature table + sequence) | full-text |
| RefSeq NC_141035.1:31,099,368–31,139,242 (GenBank + FASTA) | full-text |
| NCBI Gene 393221 (esummary, elink gene→protein) | full-text |
| UniProt Q7ZUS0, A0A8N7V006, Q5PR35, A0ACD6B803 | full-text |
| Daane et al. 2021, *Curr Biol* 31(22):5052–5061, PMID 34534441 | **could-not-access** (429/503); details at **search-summary**, quoting ZFIN figure-legend records |
| ZFIN ZDB-GENE-040426-964, ZDB-FIG-221222-35 | **could-not-access** (HTTP 503) |
| Ensembl REST (danio_rerio slc43a2a) | **could-not-access** (403, blocked by network policy) |
| Oceanbites secondary account of Daane et al. | search-summary |

Computed, not observed: the 6-frame homology search (`scripts/hsp.py`), the exon-homology table,
the Thr/`ACA` call at chr15:31,121,333, and the ~590 aa coding-capacity estimate. Observed from
primary records: all sequence lengths, the CDS/mRNA join coordinates, the 3′-partial flag, and the
HTTP status codes.

```swarm-challenge
{"claim_id": 307, "outcome": "refuted", "reason": "The 153 aa length is real but is a proxy for a RefSeq model NCBI itself flags 3'-partial — it contains a 20 bp exon and skips 27 kb that my controlled 6-frame homology search shows carries coding exons homologous to the entire 592 aa paralog slc43a2b, including a Thr (ACA) in a conserved TM helix at the T200K-corresponding position (chr15:31,121,333) — so residue 200 exists, the site set is constructible, and only the weight-host blocker is genuine.",
  "corrected_value": "slc43a2a coding capacity ~590 aa, not 153 aa; residue ~200 = Thr, codon ACA at NC_141035.1:31,121,333, in an unannotated coding exon at chr15:31,121,258-31,121,353. ESM-2 score itself remains uncomputed (weights unreachable: 403).",
  "depends_on": ["RefSeq NM_200251.2 CDS 175..636 and misc_feature 106..108", "RefSeq NP_956545.1 length 153 aa", "UniProt Q7ZUS0 and A0A8N7V006 length 153 aa", "UniProt Q5PR35 slc43a2b length 592 aa", "NC_141035.1 slc43a2a gene model join(2029..2188,8254..8482,10229..10248,37246..37298) with mRNA 3'-partial flag >39875", "NCBI Gene 393221 genomic span chr15:31,099,368-31,139,242, exoncount 5, human SLC43A2 orthology", "BLOSUM62 seeded-extension homology search in scripts/hsp.py, with positive control (slc43a2a vs locus, reproduces annotated joins) and must-fail controls (shuffled query 0 HSPs; HBB at noise floor 40)", "paralogy anchor slc43a2a residue 129 <-> slc43a2b residue 151", "Daane et al. 2021 PMID 34534441 nr21 T200K dominant allele of lat4a in a conserved TM domain (search-summary only; full text could-not-access)", "egress-proxy 403 responses for huggingface.co and dl.fbaipublicfiles.com on 2026-11-04"]}
```
