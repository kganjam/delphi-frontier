# Challenge 186 — do the two lat4a reference failures compound before guide RNA design?

**Claim under review** (recorded evidence level `derived`, value `n/a`, source: "inference from the
two verified findings"):

> "The two reference failures COMPOUND: the symbol `lat4a` resolves to nothing, and the gene it
> actually is (`slc43a2a`) has a truncated reference model. An implementer working from standard
> sources fails twice before designing a guide RNA"

**Verdict: REFUTED.** Both component facts hold — I reproduced each from primary records — and the
claim's `derived` label is honest. What fails is the inference the claim adds on top of them: the
operational prediction. The truncated reference model does **not** obstruct guide RNA design. All
**five** of the guide RNAs the source paper actually used for *lat4a* target nucleotides 331–508 of
`NM_200251.2`, i.e. **codons 53–112, entirely inside the 153-codon annotated CDS** — within the
truncated model itself. An implementer holding only that provisional record has everything needed to
design exactly those guides. So before guide RNA design the implementer fails **once** (the symbol),
not twice; the truncation bites later and only on residue-level work, which is precisely what
claims 82/89/90 were about.

Separately, I did find a real compounding mechanism the claim does not describe, which pushes toward
the **wrong paralog**. It is reported in §3 because it partly rescues the word "compound" while
further undermining the sentence the claim uses it in.

All sequence facts below are **retrieved database records** (NCBI E-utilities, accessed 2026-11-04)
or **my own calculations** over sequences I downloaded myself. Nothing here is a bench observation.
I did not reuse any prior challenge's working; every number was recomputed.

---

## 1. Arithmetic redone independently from the stated inputs

The claim states no arithmetic. What I re-derived is the only quantity its operational prediction
depends on: **where do the guide RNAs fall relative to the truncated model?**

### 1a. The truncation, recounted (calculated by me from downloaded FASTA)

| Record | Quantity | My independent value | Method |
|---|---|---|---|
| `NP_956545.1` (*slc43a2a*, the only RefSeq protein of GeneID 393221) | length | **153 aa** | `len(seq)` over fetched FASTA |
| `NM_200251.2` (*slc43a2a* mRNA) | length | **3230 nt** | `len(seq)` |
| same | annotated CDS | **175..636** = 462 bp = 153 codons + stop | GenBank flatfile; `636−175+1=462`, `462/3=154` incl. stop |
| same | 5′UTR / 3′UTR | **174 nt / 2594 nt** | `174` and `3230−636` |
| same | longest ORF, six-frame scan | **153 aa at nt 175** (next: 122, 76, 57, 53) | my own scan, standard code |
| `NP_001008585.1` (*slc43a2b*) | length | **592 aa** | `len(seq)` |

I also translated CDS 175..636 myself and confirmed it reproduces `NP_956545.1` exactly. The record
carries `PROVISIONAL REFSEQ` and `RNAseq introns :: partial sample support` (retrieved, full-text
flatfile). Gene summaries (retrieved): *slc43a2a* = chr 15, `NC_141035.1:31099368-31139242`,
**5 exons**; *slc43a2b* = chr 10, `NC_141030.1`, **15 exons**. Neither alias list contains `lat4a`
(*slc43a2a*: `si:dkey-118k5.2, slc43a2, zgc:56271`).

**So the claim's phrase "truncated reference model" is correct, and correctly worded.** Note it says
*model*, not *protein*. Challenge 90 argued the 153 aa is a frameshift artifact and therefore not the
protein's real length; that objection does not touch this claim, because "reference model" is exactly
the narrow thing that is truncated. Credit to the author for the narrow phrasing.

### 1b. Where the guides actually land (the load-bearing computation)

I took the guide sequences from the **primary source, not from any prior challenge document**:
Daane et al. 2021, *Curr Biol* 31:5052, doi:10.1016/j.cub.2021.08.054, PMC9172250, fetched as JATS
XML with `efetch db=pmc` in this session. **Read-level: full-text.** Its key-resources table lists
**five** guides, "Lat4a gRNA #1"–"#5" (a prior repo review tested only four; #5 is
`GGAGTGTGATGGCGCTCAGG`). Each is printed as the SP6 oligo `ATTTAGGTGACACTATA` + 20-mer +
`GTTTTAGAGCTAGAAATAGCAAG`.

I fuzzy-matched each 20-mer, and its 19-mer suffix (dropping the leading G commonly added for SP6
transcription), against `NM_200251.2` on both strands. Minimum-mismatch hit per guide:

| Guide (from the paper) | Best match in `NM_200251.2` | Strand | 5′ position | Codon span (my calc) | Inside annotated CDS 175..636? |
|---|---|---|---|---|---|
| #1 `GGCCCTGTACCGTTACCTGG` | 2 mm (20-mer) / **1 mm** (19-mer) | − | 331 | 53–59 | **yes** |
| #2 `GGTGAATGCCACAAGACTTG` | **1 mm** | + | 378 | 68–74 | **yes** |
| #3 `GGATGCCACAAGACTTGAGG` | **1 mm** | + | 381 | 69–75 | **yes** |
| #4 `GGCCACAAGACTTGAGGAGG` | 1 mm / **0 mm** (19-mer) | + | 384 | 70–76 | **yes** |
| #5 `GGAGTGTGATGGCGCTCAGG` | **1 mm** | − | 489 | 105–112 | **yes** |

Codon positions are mine: `(nt − 175)//3 + 1`. The whole published guide window is **codons 53–112**.
The truncated model runs to codon 153. **Every guide is covered by the truncated model.**

**This is the refutation.** The claim predicts a failure at the guide-design step. At that step the
implementer needs nucleotide sequence, and the nucleotide sequence is complete and public: a 3230-nt
transcript and a ~39.9 kb annotated chr15 locus. The protein model's incompleteness is invisible to
guide design. The claim's second failure is real but **misplaced in the pipeline**.

### 1c. Even the hardest sub-case is not a guide-design failure

The one reading that could rescue the claim: an implementer wanting a guide at the T200K site
specifically (e.g. for a precise knock-in) needs a reference covering codon 200, which does not
exist. I tested it. Under a naive continuation of the annotated frame from nt 175, codon 200 would
occupy **nt 772–774**, which *is present* in the 3230-nt transcript — annotated as 3′UTR, since the
CDS stops at 636. (That triplet reads `ACC` = Thr: **calculated by me**, and I flag it as
un-validated, because challenge 90's +22-register argument implies the frame does not run straight
through. It is a coincidence worth recording, not evidence.)

So even here the *sequence* for guide design exists. What is missing is the *annotation* that fixes
the frame and confirms the codon. That is a residue-mapping failure wearing a guide-design costume.

## 2. Is a proxy standing in for the quantity that matters?

**Yes — the claim's central defect after the ordering error.**

- **Proxy used:** "has a truncated reference model" — a property of the *protein* record.
- **Quantity that matters at the step named:** whether a usable *nucleotide* reference exists.

These are different records with different completeness. The claim treats "the reference model is
truncated" as a single global defect of the gene's reference data. It is not. For GeneID 393221 the
reference data splits cleanly:

| Artifact | State | Blocks guide design? | Blocks T200K numbering? |
|---|---|---|---|
| Genomic locus `NC_141035.1:31099368-31139242` | complete | no | no (but gives no protein numbering) |
| mRNA `NM_200251.2`, 3230 nt | complete as a transcript | **no** | — |
| CDS annotation 175..636 | **incomplete** (153 codons) | no | **yes** |
| Protein `NP_956545.1`, 153 aa | **incomplete** | no | **yes** |

**The right quantity, named:** the claim should be scoped to *the CDS/protein annotation*, and its
consequence to *residue-numbered edits* (`accession.version:p.Thr200Lys`), not to guide RNA design.
Corrected, it is a true and useful claim — just not the one written.

## 3. The hidden assumption, tested relaxed — and a real compounding the claim missed

**Assumption carrying the result:** that the two failures sit in **series on one path**, so an
implementer meets both before the first bench step. Relaxed, the path forks and the failures sit on
*different branches*:

- **Branch A (nucleotide/positional).** Paper maps *nr21* to chromosome 15 (full-text). Retrieved:
  *slc43a2a* = chr15, *slc43a2b* = chr10. The mapping picks *slc43a2a* **uniquely**, using no protein
  data at all. Guide design proceeds. One failure total.
- **Branch B (protein/orthology).** Human `SLC43A2` carries alias `LAT4` (retrieved). An implementer
  resolving `lat4a` by protein similarity to the human ortholog meets the truncation head-on.

Branch B is where something real happens, and it is **not what the claim describes**. I aligned human
`NP_689559.1` (569 aa) against both zebrafish proteins with my own Smith-Waterman
(**calculated**; match +2 / mismatch −1 / linear gap −2 — *not* BLOSUM62 or BLAST, so treat the ratio
as scheme-dependent):

| Query → target | SW score (my calc) | Alignment reaches |
|---|---|---|
| human SLC43A2 → *slc43a2b* (592 aa) | **687** | i=569, j=592 (full length) |
| human SLC43A2 → *slc43a2a* (153 aa) | **166** | i=132, j=139 |

A **~4× score gap created by coverage, not divergence** (153 vs 592 aa of target). The direction is
robust to the scoring scheme — it follows from the length ratio alone — even though the exact ratio
is not.

**My inference, stated as mine:** the truncation does compound with the symbol failure, but on
branch B only, and the failure mode is **silent misidentification toward chr10 *slc43a2b*** —
contradicting the paper's own chr15 mapping — rather than the implementer "failing twice." A silent
wrong answer is worse than a second visible failure, so this finding does not rescue the claim's
sentence; it replaces its mechanism and inverts its character. The author's word "compound" survives;
the clause it modifies does not.

## 4. Is the evidence level honest?

**Yes.** The claim is recorded `derived`, value `n/a`, source "inference from the two verified
findings." It presents no measurement as an observation and attaches no number it did not earn.
Under rubric item 4 this is a clean record. **The defect is not mislabeling — it is that the
derivation is invalid.** I want that distinction kept, because a correctly-labelled bad inference and
a mislabelled good number are different faults with different fixes.

One provenance caveat: "the two **verified** findings" is accurate only under a narrow reading.
Finding 1 (symbol absence) survived adversarial review as claim 79. The truncation *fact* is
verified — I counted 153 aa myself. But the claims built on that fact were not: claim 82 was refuted,
and claim 90 refuted 82's correction in turn. The claim's own wording ("truncated reference model")
stays on the verified side of that line, so this is a caution for downstream readers, not a charge
against the claim.

## 5. Regimes, taxa and counter-examples

- **The source paper is its own counter-example.** Daane et al. designed and used five working guides
  against this gene, published them, and recovered the `mh152` deletion allele — all while the
  reference model was in the state the claim says causes failure. An implementer who fails to design
  a guide here is not failing for lack of reference sequence.
- **Knockout vs knock-in regime.** For a knockout (what the paper did) any early-exon guide suffices
  and the truncation is irrelevant. For a residue-precise knock-in at T200K the implementer is
  genuinely blocked — but at frame/codon assignment, after guide design. The claim does not
  distinguish the regimes and is false in the one it names.
- **Paralog regime.** The claim asserts "the gene it actually is (`slc43a2a`)". That identification is
  sound on chromosome (chr15) and on the paper's own guide sequences (§1b: 0–1 mismatches to
  `NM_200251.2`). I am not disputing it, and my verdict does not depend on it — if the true target
  were *slc43a2b* the claim's guide-design prediction would fail even more plainly, since that model
  is full-length.
- **Not checked:** ZFIN and Ensembl were not queried in this session (prior repo probes record both as
  unreachable under this network policy); off-target/specificity scoring of the five guides; whether
  any non-RefSeq GenBank translation of *slc43a2a* is full-length. None of these could reverse §1b,
  which turns only on guide coordinates within a sequence I hold.

## Scope of my negatives

- "No published *lat4a* guide falls outside the annotated 153-codon CDS": scope = the five guides
  printed in the key-resources table of PMC9172250, matched against `NM_200251.2` only, both strands,
  20-mer and 19-mer forms. I did not search for guides in other papers.
- "The truncation does not block guide design": scope = guide design against `NM_200251.2` or the
  chr15 genomic locus, both retrieved 2026-11-04. Not evaluated: guide design workflows that consume
  only protein/CDS annotation.

## Sources and read-levels

| Source | Read-level |
|---|---|
| Daane et al. 2021, *Curr Biol* 31:5052, PMC9172250 (JATS XML, `efetch db=pmc`) | **full-text** |
| `NM_200251.2` FASTA + GenBank flatfile | **full-text** (primary record) |
| `NP_956545.1`, `NP_001008585.1`, `NP_689559.1` FASTA | **full-text** (primary record) |
| NCBI Gene esummary 393221, 494042 | **full record** |
| Repo challenges 79, 81, 82, 90 (`docs/research/fish/`, on their own branches) | **full-text** |
| `fish-alleles/README.md` (the ultimate source of the upstream claims) | **could-not-access** — not present on this branch |
| ZFIN, Ensembl | **could-not-access** — not attempted this session; prior repo probes record TLS/proxy failure |

```swarm-challenge
{"claim_id": 186, "outcome": "refuted", "reason": "Both component facts hold and the 'derived' label is honest, but the operational conclusion is false: all five of the paper's published lat4a guide RNAs target codons 53-112 of NM_200251.2, entirely inside the truncated 153-codon model, so the truncation does not obstruct guide RNA design -- the implementer fails once before that step (the symbol), and the truncation bites only later, on residue-level numbering.",
  "corrected_value": "One reference failure before guide RNA design (symbol lat4a = 0 hits), not two; the truncated 153-aa CDS annotation of GeneID 393221 blocks residue-numbered edits (e.g. NP_956545.1:p.Thr200Lys) but not guide design, since NM_200251.2 (3230 nt) and NC_141035.1:31099368-31139242 are complete and cover all five published guides (nt 331-508)",
  "depends_on": ["claim 79 (survived): symbol lat4a returns 0 hits in NCBI Gene and UniProtKB for Danio rerio (taxon 7955)", "NP_956545.1 is 153 aa and is the only RefSeq protein of GeneID 393221 (recounted by me from fetched FASTA, 2026-11-04)", "NM_200251.2 is 3230 nt with annotated CDS 175..636; my six-frame scan finds no longer ORF (longest = 153 aa at nt 175)", "Daane et al. 2021 Curr Biol PMC9172250 full-text key-resources table: five Lat4a gRNA oligo sequences as printed", "my fuzzy-match of those five 20-mer/19-mer spacers against NM_200251.2: best hits at nt 331, 378, 381, 384, 489 with 0-2 mismatches, all within CDS 175..636", "NCBI Gene esummary: slc43a2a = chr15 NC_141035.1:31099368-31139242, 5 exons; slc43a2b = chr10, 15 exons", "human SLC43A2 NP_689559.1 alias LAT4, 569 aa (used only for the branch-B orthology argument in section 3, computed with my own non-BLOSUM Smith-Waterman)"]}
```
