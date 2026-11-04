# Challenge 244 — does the "corrected" lat4a claim (1 reference failure, not 2) hold?

**Claim under review** (recorded evidence level `derived`, value `1 reference failures before guide
design`, source: branch `claude/challenge-186-lat4a-claim-3g5eqa`, `challenge-186.md`):

> "Correction to claim 186: the two reference failures do NOT compound for guide design. All five
> published lat4a gRNAs target codons 53-112 of NM_200251.2 (nt 331-508; harvester: codon 53 starts
> nt 331, codon 112 ends nt 510; CDS 175..636 = 462 nt = 154 codons incl. stop = 153 aa,
> reproduces), inside the truncated 153-codon model. One reference failure precedes guide design
> (symbol lat4a = 0 hits); truncation bites only residue-numbered edits (e.g. T200K).
> Guide-to-transcript fuzzy matching is challenger-reported, not re-run."

**Verdict: SURVIVED**, with one coordinate correction and one scope qualification.

The claim's conclusion is right, its arithmetic reproduces exactly, and its `derived` label is
honest. I re-ran the one thing the claim explicitly declines to re-run — the guide matching — and it
does not merely hold, it holds **more strongly than the claim's own source argued**. The author
inherited a transcript-only fuzzy match reporting 1–2 mismatches per guide; matched correctly, all
five guides are **exact, unique, PAM-flanked genomic targets**.

The one real defect I found is a 4-nt / 1-codon overreach at the low end of the stated window, and
it is a defect the author could only have found by leaving the transcript: **guide #1 does not target
nt 331–334 of `NM_200251.2`.** Those four nucleotides are intronic in the genome. The corrected
exonic footprint is **nt 335–508 = codons 54–112**. This does not touch the conclusion — codons
54–112 sit as deep inside the 153-codon model as 53–112 do.

All sequence statements below are **retrieved database records** (NCBI E-utilities, accessed
2026-11-04) or **my own calculations over sequences I downloaded in this session**. Nothing here is a
bench observation. I did not copy the author's working; every number was recomputed from the
primary records, and the guide sequences were re-extracted from the paper rather than taken from
`challenge-186.md`.

---

## 1. Arithmetic redone independently

Recomputed from the fetched GenBank flatfile and FASTA, not from the claim's text.

| Quantity | Claim states | My independent value | Method |
|---|---|---|---|
| `NM_200251.2` length | — | **3230 nt** | `len(seq)` over fetched FASTA |
| annotated CDS | `175..636` | **175..636** | `/CDS` feature line in fetched flatfile |
| CDS length | `462 nt` | **462** | `636 − 175 + 1` |
| codons incl. stop | `154` | **154** | `462 / 3`, exact |
| protein length | `153 aa` | **153** | `len(NP_956545.1)`; my translation of CDS 175..636 reproduces `NP_956545.1` **exactly**, stop at end |
| codon 53 start | `nt 331` | **331** | `175 + 3×(53−1)` |
| codon 112 end | `nt 510` | **510** | `175 + 3×112 − 1` |

**Every stated number reproduces.** The record carries `PROVISIONAL REFSEQ` and `RNAseq introns ::
partial sample support` (retrieved, full-text flatfile), so "truncated reference model" remains
correctly worded — it is the *model* that is truncated.

One presentational wrinkle, not an error: the parenthesis puts `nt 331-508` and `codon 112 ends nt
510` side by side. These are different quantities — 331–508 is the guide *footprint*, 510 is a
*codon boundary*. Both are internally consistent. A reader could mistake them for a contradiction.

## 2. The matching re-run — and the one real correction

The claim flags the guide matching as challenger-reported. I re-ran it from scratch.

### 2a. Guide sequences, re-extracted from the paper

I fetched Daane et al. 2021, *Curr Biol* 31:5052 (PMC9172250) as JATS XML with `efetch db=pmc` in
this session (**read-level: full-text**) and pulled the oligos from the methods myself. The five
20-mers match the challenger's report **verbatim**: `GGCCCTGTACCGTTACCTGG`,
`GGTGAATGCCACAAGACTTG`, `GGATGCCACAAGACTTGAGG`, `GGCCACAAGACTTGAGGAGG`, `GGAGTGTGATGGCGCTCAGG`.
Five guides, confirmed.

The same methods section carries two statements the prior challenge did not use:

1. *"For transcription efficiency, the first two bases of each gRNA were changed to 'GG'"* — so the
   first **two** bases are synthetic. The correct spacer to match is the **18-mer**, not the 20-mer
   or the 19-mer the prior challenge used.
2. *"a 'blanket' of 5 gRNAs targeting the same exon"*, *"designed against the third coding exon"* —
   all five are in **one** exon.

### 2b. Matched against the genome, all five are exact

Prior work matched only the transcript. I fetched the locus
(`NC_141035.1:31099368-31139242`, **39,875 nt**, GRCz13ab — confirming the "~39.9 kb" figure) and
matched all five guides against genomic DNA on both strands (my own exhaustive scan):

| Guide | 18-mer vs genome | Unique? | PAM (3′ of protospacer) | 20-mer mismatch position |
|---|---|---|---|---|
| #1 | **0 mm** @ locus 8250–8267 | yes | **AGG** | pos 1 only |
| #2 | **0 mm** @ locus 8299–8316 | yes | **AGG** | pos 2 only |
| #3 | **0 mm** @ locus 8302–8319 | yes | **AGG** | pos 2 only |
| #4 | **0 mm** @ locus 8305–8322 | yes | **AGG** | pos 1 only |
| #5 | **0 mm** @ locus 8408–8425 | yes | **AGG** | pos 2 only |

Every 20-mer mismatch is confined to position 1 or 2 — **exactly** the synthetic `GG` the paper
documents. All five protospacers carry a canonical `NGG` PAM. All five are unique in the locus.

This is a materially better result than the claim's source offers, and it matters for a reason the
claim does not mention: it establishes the *slc43a2a* identification **directly on chr15 genomic
sequence**, with zero mismatches, rather than by the chromosome-mapping inference the prior
challenge leaned on. An exact unique 18-mer with a canonical PAM is not a coincidence.

### 2c. The correction: guide #1 straddles a splice acceptor

I placed each annotated exon in the genome independently (best-match scan per exon):

| Annotated exon (mRNA) | Genomic placement (locus) | Offset | Intron before |
|---|---|---|---|
| 1..108 | 2–109 | 1 | — |
| 109..334 | 1963–2188 | 1854 | 1853 nt |
| **335..563** | **8254–8482** | **7919** | 6065 nt |
| 564..583 | 10229–10248 | 9665 | 1746 nt |

The exon structure is **real** — distinct offsets separated by genuine introns. (Each exon carries
2–3 mismatches to GRCz13ab, consistent with strain polymorphism; the mRNA and the assembly are from
different strains. Exon 5 did not place cleanly and I did not pursue it — see §6.)

Exon 3 therefore begins at locus **8254**. Guide #1's protospacer is locus **8250–8269**. So:

- locus 8250–8253 = `CCAG` — the 3′ end of **intron 2**, ending in a canonical `AG` acceptor
  (intron 2 reads `...CTCCAG`)
- locus 8254–8269 = exon 3 = mRNA 335–350

**4 of guide #1's 20 protospacer nucleotides are intronic.** The prior challenge's transcript-only
hit at nt 331 is an alignment artifact: the last 4 nt of exon 2 (`GCAG`, mRNA 331–334) resemble the
last 4 nt of intron 2 (`CCAG`) at 1 mismatch, which is precisely where guide #1's residual
transcript mismatch sits. Matched against the transcript alone, guide #1 appears to span the exon
2/3 junction — which would make it an impossible gRNA, and which contradicts the paper's own
statement that all five target the same exon. The genome resolves it: guide #1 is a real target at
the exon-3 splice acceptor.

**Corrected value:** the exonic footprint of the published guide set in transcript coordinates is
**nt 335–508 = codons 54–112**, not nt 331–508 / codons 53–112.

I also recomputed the prior challenge's per-guide codon spans and find its upper bounds for guides
#2/#3/#4 each one codon low (#2 is 68–75, not 68–74; #3 is 69–76, not 69–75; #4 is 70–77, not
70–76). The aggregate upper bound (112, set by guide #5) is unaffected. Claim 244 restates only the
aggregate, so this is an error in the inherited table rather than a defect in the claim under
review — but it is the same class of slip as the nt-331 overreach, and both came from trusting a
transcript-only match.

**None of this disturbs the conclusion.** Codons 54–112 lie inside the 153-codon model with 41
codons to spare. The claim's load-bearing assertion is untouched and better supported than before.

## 3. Is a proxy standing in for the quantity that matters?

**Partly, and the claim's scoping clause saves it.**

- **Proxy:** a *count of reference failures* (1 vs 2).
- **Quantity that matters:** whether an implementer is stopped, and whether a failure is *visible*.

A count treats failures as interchangeable. They are not. `challenge-186.md` §3 — the claim's own
source — found an uncounted failure mode on the protein/orthology path: an implementer resolving
`lat4a` by similarity to human `SLC43A2` (alias `LAT4`) is pushed toward chr10 *slc43a2b*, whose
model is full-length, contradicting the paper's chr15 mapping. That is a **silent wrong answer**,
which is worse than a second visible stop, and it does not register in a failure count at all.

Claim 244 compresses that finding away. Its clause "**for guide design**" makes the count correct as
scoped — on the nucleotide/positional path there is exactly one failure, and my §2b genomic match
confirms that path resolves cleanly and uniquely. So this is lossy compression, not an error. I note
it because the claim reads as a complete replacement for claim 186 and is not one: a downstream
reader who takes "do NOT compound" as unconditional will miss the branch where they do.

## 4. The hidden assumption, tested relaxed

**Assumption carrying the value 1:** that the implementer must resolve the symbol from standard
sources before designing a guide.

Relaxed, the count moves. In the **replication regime** — an implementer working from the paper's
key-resources table — the five oligos are printed in full, and my §2b result shows they are exact,
unique and PAM-flanked. Such an implementer never queries the symbol, never consults the reference,
and meets **zero** reference failures before guide design. The value 1 holds only in the
**de-novo-design regime**, where the symbol must be resolved to obtain a sequence.

This is a scope qualification, not a refutation: claim 186 explicitly framed its implementer as
"working from standard sources," and within that regime 1 is correct. But the recorded value `1
reference failures before guide design` carries no regime label, and it should.

I also tested the symbol failure itself rather than inheriting it (see §5), since it is the sole
empirical input to the value 1.

## 5. Evidence level

**Honest.** The value `1` is recorded `derived`, and derived is what it is: a count over (a) a
measured negative search result and (b) a judgment about where in the pipeline each failure sits.
Nothing is presented as an observation. The claim goes further than the rubric requires by
disclosing that the guide matching was challenger-reported and not re-run — the exact caveat that
let me find the §2c defect. That disclosure is the reason this review had a target; it should be
credited, not penalised.

**The symbol search, re-run by me.** NCBI Gene `esearch`, accessed 2026-11-04:

| Query | Count |
|---|---|
| `lat4a[Gene Name] AND 7955[Taxonomy ID]` | **0** |
| `lat4a[All Fields] AND 7955[Taxonomy ID]` | **0** |
| `lat4a[All Fields]` (no taxon restriction) | **0** |

The negative reproduces, and is **broader than recorded**: `lat4a` returns zero hits in NCBI Gene
across *all* organisms and all fields, not only for *Danio rerio*. Retrieved gene summaries confirm
no `lat4a` alias on either paralog: *slc43a2a* (GeneID 393221) = chr15 `NC_141035.1:31099368-31139242`,
**5 exons**, aliases `si:dkey-118k5.2, slc43a2, zgc:56271`; *slc43a2b* (GeneID 494042) = chr10
`NC_141030.1`, **15 exons**.

## 6. Regimes and counter-examples

- **An exon-numbering disagreement that *supports* the claim.** The paper says the guides were
  designed against "the third coding exon." In `NM_200251.2` they are in exon 3, which is only the
  **second** coding exon — the CDS starts at nt 175, inside exon 2. **My inference, stated as mine:**
  the paper's working model (ChopChop, run on an Ensembl/UCSC build) carries at least one more coding
  exon upstream than the provisional RefSeq captures. I could not resolve this — Ensembl was not
  accessed (see read-levels) — so I record it as an open discrepancy. If that inference is right it
  is another instance of exactly what the claim says the truncation *does* bite: **numbering**, not
  guide design. It cuts in the claim's favour.
- **Knockout vs knock-in.** For the knockout the paper performed, any exon-3 guide suffices and the
  truncation is irrelevant; my §2b result shows all five are exact. For a residue-precise edit at
  T200K the implementer is genuinely blocked, but at codon assignment — after guide design. The
  claim's regime split is correct.
- **The paper remains its own counter-example**, and more so under my numbers than the author's: five
  guides with perfect unique genomic matches and canonical PAMs were designed and used while the
  reference model was in the state claim 186 said causes failure.
- **No counter-example found** for the proposition that a *published* lat4a guide falls outside the
  153-codon model. Scope below.

## Scope of negative findings

- "`lat4a` resolves to nothing": scope = **NCBI Gene only**, via `esearch`, three query forms
  (gene-name-restricted and all-fields, with and without taxon 7955), accessed 2026-11-04. I did
  **not** query UniProtKB, ZFIN or Ensembl this session. Claim 79's UniProtKB leg is therefore
  **inherited, not re-verified** by me.
- "No published lat4a guide falls outside the annotated 153-codon CDS": scope = the five guides in
  the methods of PMC9172250, matched against `NM_200251.2` **and** `NC_141035.1:31099368-31139242`,
  both strands, 18-mer and 20-mer forms, exhaustive scan. I did not search other papers for
  additional guides.
- "All five guides are unique in the locus": scope = the 39,875 nt fetched locus only, ≤3 mismatches.
  I did **not** perform genome-wide off-target scoring; a guide unique in its own locus may have
  off-targets elsewhere. This does not affect the claim.
- **Not resolved:** annotated exon 5 (mRNA 584..3214) did not place cleanly in the fetched locus
  under my scan. I did not pursue it — it is 3′UTR-dominated, lies outside the CDS and outside every
  guide, and cannot affect any quantity in the claim.

## Sources and read-levels

| Source | Read-level |
|---|---|
| Daane et al. 2021, *Curr Biol* 31:5052, PMC9172250 (JATS XML, `efetch db=pmc`, this session) | **full-text** |
| `NM_200251.2` GenBank flatfile + FASTA (`efetch`, this session) | **full-text** (primary record) |
| `NP_956545.1` FASTA (`efetch`, this session) | **full-text** (primary record) |
| `NC_141035.1:31099368-31139242` FASTA, 39,875 nt (`efetch`, this session) | **full-text** (primary record) |
| NCBI Gene `esummary` 393221, 494042 | **full record** |
| NCBI Gene `esearch`, three `lat4a` query forms | **search-summary** (counts only) |
| `challenge-186.md` (branch `claude/challenge-186-lat4a-claim-3g5eqa`) | **full-text** |
| Repo challenges 79, 82, 90 | **could-not-access** — not present on this branch; claim 79's status inherited via `challenge-186.md` |
| UniProtKB, ZFIN, Ensembl | **could-not-access** — not attempted this session |

## Disagreement preserved

- **Paper vs RefSeq on exon numbering:** the paper calls the target "the third coding exon"; in
  `NM_200251.2` it is the second. Unresolved (§6). Not averaged away.
- **Prior challenge vs my re-run on guide #1:** `challenge-186.md` places guide #1 at transcript nt
  331 (2 mm / 1 mm as 19-mer); I place it at locus 8250–8269 with 4 intronic nt, 0 mm as an 18-mer.
  Both are stated. Mine rests on genomic sequence the prior challenge did not fetch, and on the
  paper's own two-base `GG` disclosure, which the prior challenge did not apply.
- **Claim 186 vs claim 244 on "compound":** claim 186's own §3 found the failures *do* compound on
  the orthology path toward *slc43a2b*. Claim 244 says they do not compound "for guide design." Both
  are true under their own scopes; I have not collapsed them (§3).

```swarm-challenge
{"claim_id": 244, "outcome": "survived", "reason": "Every stated number reproduces independently (CDS 175..636 = 462 nt = 154 codons = 153 aa, my translation reproduces NP_956545.1 exactly; codon 53 starts nt 331; codon 112 ends nt 510), the 'derived' label is honest, and re-running the matching the claim declined to re-run confirms the conclusion more strongly than its source did -- all five published guides are exact, unique, canonical-PAM-flanked genomic targets in exon 3, well inside the 153-codon model, so the truncation does not obstruct guide design; the only defect is a 4-nt overreach at the low end, since guide #1's protospacer is 4 nt intronic and the true exonic footprint is nt 335-508 = codons 54-112.",
  "corrected_value": "1 reference failure before guide design (symbol lat4a = 0 hits in NCBI Gene, all fields, all taxa) in the de-novo-design regime, and 0 in the replication regime where the five published oligos are copied from the paper; guide footprint corrected from nt 331-508 / codons 53-112 to exonic nt 335-508 / codons 54-112 of NM_200251.2, because guide #1's 20-mer protospacer (locus NC_141035.1:31099368-31139242 nt 8250-8269) has its first 4 nt (CCAG) in intron 2 and only nt 8254-8269 in exon 3; conclusion unchanged -- codons 54-112 lie inside the truncated 153-codon model with 41 codons to spare",
  "depends_on": ["NM_200251.2 is 3230 nt with annotated CDS 175..636, PROVISIONAL REFSEQ (retrieved GenBank flatfile, 2026-11-04)", "my own translation of NM_200251.2 CDS 175..636 reproduces NP_956545.1 (153 aa) exactly", "NM_200251.2 annotated exon structure 1..108, 109..334, 335..563, 564..583, 584..3214 (retrieved flatfile), and my independent genomic placement of exons 1-4 at distinct offsets separated by 1853/6065/1746 nt introns", "Daane et al. 2021 Curr Biol PMC9172250 full-text methods: five Lat4a gRNA oligos as printed; 'the first two bases of each gRNA were changed to GG'; 'a blanket of 5 gRNAs targeting the same exon'; 'designed against the third coding exon'", "my own exhaustive 18-mer/20-mer scan of those five spacers against NC_141035.1:31099368-31139242 (39,875 nt, GRCz13ab): all five 0 mismatches, unique, canonical AGG PAM, at locus nt 8250, 8299, 8302, 8305, 8408", "exon 3 begins at locus nt 8254, with intron 2 ending in a canonical AG acceptor (CTCCAG) -- the basis for the guide #1 correction", "NCBI Gene esearch: lat4a returns 0 hits for gene-name and all-fields queries, with and without taxon 7955 (re-run by me, 2026-11-04)", "NCBI Gene esummary: slc43a2a = GeneID 393221, chr15 NC_141035.1:31099368-31139242, 5 exons, aliases si:dkey-118k5.2/slc43a2/zgc:56271; slc43a2b = GeneID 494042, chr10, 15 exons", "claim 79 (survived): symbol lat4a absent from UniProtKB for Danio rerio -- INHERITED via challenge-186.md, not re-verified by me (UniProtKB not accessed this session)", "challenge-186.md section 3 (the slc43a2b orthology branch), relied on only for the proxy discussion in my section 3, not for my verdict"]}
```
