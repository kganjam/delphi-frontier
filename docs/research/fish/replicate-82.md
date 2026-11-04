# Independent re-derivation — claim 82 ("CONSEQUENCE FOR BUILD")

**Outcome: PARTIAL. I derived a defensible consequence-for-build number, but I could not
read claim 82's own wording, so I cannot be sure I answered the same question.**

## What I was given, and what was missing

The question text I was handed was reduced to its heading, `CONSEQUENCE FOR BUILD`, with
the note that the inputs live in "inference from the two claims above". The two upstream
claims were not supplied, and this repository holds no numbered claim registry — there is
no file mapping `82` (or any integer id) to a claim statement on any branch I examined.
`seeds/frontier-problems.json` carries `claim_ids` arrays but no claim bodies;
`bench/bench-v1.1-freeze.json` uses string ids (`fisher-ftns`, `kimura-fixation-time`, …),
not integers. The numbering therefore lives in the swarm harness, not in the repo.

**I located another agent's working and did not read it.** A grep for the question heading
across every remote branch (74 refs) returned exactly one file:
`docs/research/fish/challenge-82.md` on `origin/claude/slc43a2a-t200k-numbering-b2ak09`.
I stopped at the path. I did not `git show` it, open it, or read any diff containing it.
Its branch name is the only thing I used from it, and only to tell me the subject matter was
zebrafish **slc43a2a / Lat4a T200K numbering** — which is also inferable from
`data/genomics/daane2021_pins.json` on `origin/claude-organ/sims`.

So the question I actually answered is my reconstruction of it:

> Given (1) Daane et al. 2021 number two Lat4a residues — T200K and F326L — and (2) the only
> public zebrafish `slc43a2a` protein record is a 153-aa fragment, what is the consequence for
> a build that validates residue claims against public reference proteins?

If claim 82's two upstream claims were different, this derivation answers a different
question and the comparison at the bottom is void.

## My value

**0 of 2 (zero of the two numbered Lat4a residues can be placed on the public zebrafish
`slc43a2a` protein record).** Equivalently, as a positional shortfall:

- **T200 lies 47 residues past the C-terminus** of `NP_956545.1` (153 aa).
- **F326 lies 173 residues past** it.
- The public record covers **26.7 % (153 / 572)** of the protein my own reconstruction
  produces — range **25.6–26.7 %** across the two reconstructions below.

Uncertainty: the counts 47 and 173 are exact arithmetic on two integers that are both
directly read off records (153 aa; positions 200 and 326 as printed in the paper), so they
carry no error. The **0 of 2** is categorical, not estimated. The percentage carries the
model-length uncertainty: ±15 aa in the denominator (572 vs 587) and roughly **±3 aa of
positional slack** in my reconstruction, from indel placement in the spliced alignment.

**The consequence for build**, stated as the claim: a build step that numbers Lat4a variants
against the public RefSeq zebrafish `slc43a2a` protein fails on **100 % of the paper's
residue claims** — not with a wrong answer, but with an out-of-range index. Such a build must
either carry its own full-length Lat4a model or record the residue claims as unverifiable
against RefSeq. It cannot verify them and report success.

## Inputs, each with source and read-level

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| 1 | T200K in lat4a, nr21 mutant, mapped to chromosome 15 | "we mapped nr21 to chromosome 15 and identified a nonsynonymous mutation (T200K) in a conserved domain of the L-type amino acid transporter, lat4a" | Daane et al. 2021, *Curr Biol*, doi 10.1016/j.cub.2021.08.054, PMC9172250 | **full-text** (PMC XML via NCBI efetch) |
| 2 | F326L, convergent across gliding lineages | "we detected a shared amino acid substitution in lat4a that is found across multiple lineages having enlarged pectoral fins (F326L…)" | same | **full-text** |
| 3 | No protein accession given for the Lat4a numbering | searched the full text for `NP_`, `XP_`, `NM_`, `ENSDARP`, `accession`, `RefSeq` — no hit anchors the lat4a residue numbering; methods cite Ensembl BioMart (Jan 2020) and a Zv9 exome capture | same | **full-text** (negative, scope: this one article's body, methods and figure legends) |
| 4 | Only public RefSeq protein for zebrafish slc43a2a is `NP_956545.1`, **153 aa** | 153 aa, `DBSOURCE REFSEQ: accession NM_200251.2`, `PROVISIONAL REFSEQ`, 5 exons, CDS 1..153 | NCBI efetch, `NP_956545.1` GenPept | **full-text** (record) |
| 5 | That record is the gene's only RefSeq protein | NCBI Gene 393221 (`slc43a2a`, chr 15, `NC_141035.1`:31,099,368–31,139,242, 5 exons); elink `gene_protein_refseq` → `[41053786]`, one id | NCBI esummary + elink | **full-text** (record) |
| 6 | UniProt holds no full-length zebrafish slc43a2a | `Q7ZUS0` and `A0A8N7V006`, both 153 aa, both unreviewed, both ending `…ILNSVTRTASVQLYYQ` | UniProtKB REST search, `gene:slc43a2a AND organism_id:7955` | **full-text** (records) |
| 7 | Negative scope for #6 | a wider UniProt query over `slc43a2a/b`, `slc43a1a/b`, `slc43a3a/b` and `protein_name:"amino acid transporter 4"` in taxid 7955 returned 16 entries; every slc43a2**a** entry was 153 aa. Scope: UniProtKB, 2026-11-04. | UniProtKB REST | **full-text** (listing) |
| 8 | Paralogue `slc43a2b` is full length but is a different gene | `Q5PR35` 592 aa, chr **10** (`NC_141030.1`, Gene 494042, 15 exons); its residue 200 is M and 326 is D — neither matches T200/F326 | UniProt + NCBI Gene | **full-text** (records) |
| 9 | Human LAT4 does **not** carry these residues at these positions | `Q8N370` (LAT4_HUMAN), 569 aa, residue 200 = **I**, residue 326 = **L** | UniProtKB | **full-text** (record) |
| 10 | Genomic DNA for the locus | `NC_141035.1`:31,079,368–31,159,242 (79,875 bp, the gene span ±20 kb), GRCz13ab; md5 of the FASTA I used: `ade590cfd25d977c736abc6d28b2f575` | NCBI efetch | **full-text** (sequence) |
| 11 | Ensembl's own zebrafish Lat4a model (what the paper's methods point at) | unknown | `rest.ensembl.org` | **could-not-access** — the session's egress proxy refused the connection (`connect_rejected`). I did not substitute a guess for it. |
| 12 | Claim 82's own two upstream claims | unknown | not in this repo (see above); the only file carrying them is another agent's working, which I did not read | **could-not-access** (by choice) |

## The arithmetic in full

Positional shortfall against the public record (input #4 = 153 aa; inputs #1, #2 for the
positions):

```
T200:  200 - 153 =  47 residues beyond the C-terminus of NP_956545.1
F326:  326 - 153 = 173 residues beyond the C-terminus of NP_956545.1
```

Both are positive, so neither index exists in the record. Count of the paper's two numbered
residues that the record can host:

```
hostable = |{p in {200, 326} : p <= 153}| = |{}| = 0        → 0 of 2 (0 %)
failures = 2 of 2                                            → 100 %
```

Coverage of the record against my reconstruction (153 aa out of 572 aa, input #4 over the
computed model below):

```
153 / 572 = 0.26748...  → 26.7 %
153 / 587 = 0.26065...  → 26.1 %   (alternative model)
153 / 598 = 0.25585...  → 25.6 %   (longest slc43a2b isoform length, as a loose upper bound on protein length)
```

## The reconstruction — this is a COMPUTED result, not an observation

I built a spliced protein-to-genome alignment myself. **No part of the following is an
observation or a database record**; it is the output of a program I ran on input #10.

Method: miniprot (Heng Li; cloned from `github.com/lh3/miniprot` at depth 1 and compiled in
this container) run as `miniprot --gff --trans` on the 79,875-bp chr15 region, with two
independent queries: human LAT4 `Q8N370` (569 aa) and zebrafish Slc43a2b `Q5PR35` (592 aa).
Both queries aligned to the same locus and the same strand (+), spanning genomic offsets
22,029–56,798 of the extracted region, with 14 and 15 exon blocks respectively.

| Query driving the model | Translated model length | Residue 200 | Residue 326 | Identity to query |
|---|---|---|---|---|
| Human LAT4 `Q8N370` | 572 aa | **T** ✓ | **F** ✓ | 0.766 |
| Zebrafish Slc43a2b `Q5PR35` | 587 aa | **T** ✓ | Q ✗ | 0.765 |

The human-guided model satisfies **both** of the paper's wild-type residue identities at
**both** of the paper's exact positions. That is a non-trivial check rather than a
tautology: the human query has I at 200 and L at 326 (input #9), so the matching T and F
were read out of zebrafish genomic DNA, not copied from the query. The second model agrees
on T200 and disagrees on F326 (Q), which is why I quote ±3 aa of positional slack — the
F326 register depends on indel placement near the exon-8 region, and the two reconstructions
differ there. **I preserve that disagreement rather than averaging it.**

My model and `NP_956545.1` are **identical over their first 139 residues**, then diverge:
the RefSeq record ends `…ILNSVTRTASVQLYYQ` where the model continues
`…ILISYGASDPQNLSILIFFALA…`. So the public record is not a different gene; it is a truncated,
`PROVISIONAL`-flagged reading of the same locus that stops in the middle of the transporter.

My own inference, separate from any author's claim: Daane et al. (who cite Ensembl BioMart,
input #3) must have numbered T200K and F326L on a full-length Lat4a of roughly 570–590 aa,
and my reconstruction is consistent with that at both positions. The paper itself asserts
nothing about RefSeq or about numbering provenance — that gap (input #3) is a negative result
of my search of its text, not a statement by its authors.

## What I did not do

- I did not read `docs/research/fish/challenge-82.md` or its branch.
- I did not reach Ensembl (input #11), so I could not confirm which exact Ensembl protein the
  paper's numbering used. The reconstruction stands in for it, labelled as computed.
- I did not fabricate the two upstream claims of claim 82. Where they are needed, the answer
  above is conditional on my reconstruction of the question.
- I did not model the effect of T200K or F326L on transport. Nothing here is a functional
  claim.

## Comparison with the recorded value

**CANNOT TELL.** The recorded value exists in this repository — in the one file named above —
and reading it is precisely what this exercise forbids, so I did not. I also never saw claim
82's own wording, which means that even if I read their number now I could not tell whether a
mismatch reflected a different answer or a different question. I leave `agrees` as `null`
rather than claim an agreement I have not earned.

A third party can settle it cheaply: compare the `0 of 2` / `47 residues` / `26.7 %` triple
above against `challenge-82.md`, and check whether that file's question is the one I
reconstructed in the second section.

```swarm-replication
{"claim_id": 82, "my_value": "0 of 2 Lat4a residues placeable on public RefSeq slc43a2a (T200 is 47 aa past, F326 is 173 aa past the 153-aa NP_956545.1; record covers 26.7% = 153/572 aa of my reconstructed model); build consequence: 100% of the paper's lat4a residue claims are unverifiable against RefSeq", "agrees": null,
  "note": "Derived from primary sources only; I found the other agent's challenge-82.md and deliberately did not read it, and claim 82's two upstream claims were never supplied, so no honest comparison is possible."}
```
