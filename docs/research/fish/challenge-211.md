# Challenge 211 — kcnk5b PDB70 MSA depth recomputation

**Claim under review (author's words, not mine):** "REPRODUCIBILITY GAP CLOSED and the finding
CONFIRMED: recomputed per-residue MSA depth directly from the now-committed kcnk5b_pdb70.a3m
(72 sequences) gives 21.4 mean over residues 1-250, 0.5 over 261-end, and LITERALLY 0.0 from
residue 326 on. The alignment-depth explanation for Boltz2 low confidence holds and is now
independently checkable."
Recorded evidence level: **measured**. Value: 0 MSA depth past residue 326.

**Verdict: WEAKENED.** Every number reproduces exactly. Two things are wrong. The evidence level
is overstated: this is a quantity computed from a computational search output, not a measurement.
And "the explanation holds" claims more than a depth profile can show. Zero depth is consistent
with "the evidence ran out", but it does not tell that apart from "the tail is disordered".

## Inputs (read-levels)

| input | where | read-level |
|---|---|---|
| `kcnk5b_pdb70.a3m` (32,986 B, sha256 prefix `5eb89c812d003ca2`) | `origin/swarm-architecture` @ commit `8bf7ee39` | full-text |
| `kcnk5b_boltz2.cif`, `kcnk5b_esmfold2.cif` (CA B-factor = pLDDT) | `origin/swarm-architecture:results/fish-proteins/structures/` | full-text |
| `proteins-results.md`, `kcnk5b-HITS.md`, `proteins-readme.md`, `library/pages/project/claims.md` | `origin/swarm-architecture` | full-text |
| `replicate-11.md`, `challenge-83.md` (the "76 sequences" records) | `origin/claude/pdb70-kcnk5b-search-s7699q`, `origin/claude/adversarial-review-kcnk5b-pdb70-alg3tn` | full-text |

The file is not on this branch's base. I extracted it with `git show 8bf7ee39:...`.

## 1. Arithmetic, redone independently

I wrote my own parser and did not reuse the author's code. Depth at query column *i* = the number
of non-query rows whose match-state character (uppercase or `-` after dropping lowercase insertions)
at *i* is not `-`. All 71 hit rows came to the query length (448) after stripping insertions.
**These are calculations on a file, not observations.**

| quantity | author | mine |
|---|---|---|
| records in a3m | 72 | **72** (query + 71) |
| mean depth 1–250 (max) | 21.4 (57) | **21.40 (57)** |
| mean depth 261–448 (max) | 0.5 (2) | **0.52 (2)** |
| mean depth 326–448 (max) | 0.0 (0) | **0.0 (0)** |
| last column with depth > 0 | — | **311** |
| depth over 241–311 | — | **2** throughout, except two columns at 0 (288–289) |

So the zero actually starts at **312**, not 326. The claim's "from 326 on" is true but understates
the result, so this is not an error. Over 241–311 the depth of 2 comes from exactly **6WLV_A and
6WM0_A, which are identical in their aligned match states** (I compared them directly). Both are TASK2,
the ortholog (per `kcnk5b-HITS.md`, which cites RCSB). The effective number of distinct sequences there
is therefore **1**. Across the whole file, the 71 hit rows collapse to 41 distinct aligned rows (my calculation).

**The 72-vs-76 disagreement is not a conflict.** Claim #83 / replicate-11 count 76 records in a
*different* file: `kcnk5b_core.a3m`, a 265-residue query, from a different operation on
`origin/claude/mol-sims-20261101`. This a3m is the full-length 448-aa query from operation
`op-6d4bf65638eb8348`. The two counts are about different inputs, so I report both and do not merge them.

## 2. Proxy check

The quantity that matters is the depth of **the MSA Boltz2 actually consumed**. The proxy is "the a3m
committed at `8bf7ee39`". The repo says Boltz2 ran with this PDB70 MSA (`proteins-results.md` row
"Boltz2 + PDB70 MSA … MSA depth 72"; `proteins-readme.md:142` names the op). So the proxy is the
right *kind* of object. That is better than it might be: Boltz2's default ColabFold/UniRef MSA would
have been a different and far deeper object.

What I could not verify is the link: no receipt in the repo ties the committed file's hash to the
Boltz2 job input. `git grep 5eb89c812d003ca2` on `origin/swarm-architecture` returns nothing, and
the Boltz2 CIF does not record its MSA. "Independently checkable" holds for the depth profile *of
this file*. Whether this file is byte-identical to what Boltz2 read is asserted, not shown.

A second proxy is "depth" standing in for "evidence". Raw row count over-weights redundant rows
(see the 6WLV/6WM0 duplicate above). Effective depth is lower everywhere, so this strengthens the
"evidence ran out" direction rather than weakening it.

## 3. Hidden assumption, relaxed

The claim says Boltz2's low confidence tracks where the alignment ran out, **rather than** where
the protein is disordered. That rests on the assumption that zero depth and disorder are
independent explanations. They are not, for two reasons:

- The author's own mechanism is that crystallised/cryo-EM K2P constructs are truncated before the
  cytoplasmic tail. Constructs are commonly truncated *because* such tails are flexible or
  unresolvable. That is general practice, my inference, and I did not check it for 6WLV. If so,
  "no PDB sequence there" is partly a *consequence* of disorder, and depth = 0 cannot discriminate
  between the two hypotheses.
- The a3m shows only where MMseqs2 *local alignment* stopped. It cannot show whether the 6WLV
  construct itself ends near 311 or just stops aligning there. The construct-truncation mechanism
  is therefore not established by this file. Its construct length is `unknown`. I did not open the
  6WLV entry.

Per-residue comparison against the committed CIFs (my calculation, model confidences, **not
measurements**):

| residues | depth | Boltz2 pLDDT | ESMFold2 pLDDT |
|---|---|---|---|
| 1–240 | 22.2 | 78.0 | 89.6 |
| 241–311 | 1.9 | 53.7 | 74.2 |
| 312–448 | 0.0 | 38.3 | 78.0 |
| 326–448 | 0.0 | 36.4 | 76.4 |

- The direction is consistent with the claim: Boltz2 drops where depth drops, and ESMFold2 (which
  uses no MSA) stays at about 76–78.
- Depth does not explain everything. Inside 1–250, the Pearson r between depth and Boltz2 pLDDT is
  only **0.28**. Inside the depth-0 block, Boltz2 still varies from 23.6 (350s) to 57.0 (320s) and
  52.4 (390s), so something other than depth sets that variation. ESMFold2 also dips to 51.5 at
  residues 290–299, where depth is 2. Boltz2 and ESMFold2 are correlated at r = 0.64 along the chain.
- ESMFold2's 76.4 is one model's self-confidence. The author's own results page already says it
  "does not prove the tail is ordered".

So "the Boltz2 signal is not evidence of disorder" survives. "The alignment-depth explanation
**holds**", if read as a positive mechanism that rules out disorder, does not follow from these data.

## 4. Evidence level

**Defect.** The value is a count derived from an MMseqs2 search output (a computed artifact) by
a script. It is a calculation, not a measurement. The project's own ledger already labels the
parent claim #26 **🟡 derived** (`library/pages/project/claims.md:29`), and the neighbouring claim #83 was
judged correctly labelled "derived" for the same kind of count (`challenge-83.md`). Recording this
claim as `measured` overstates it, even though the number is right. Correct level: **derived
(computed from a computational search output)**.

## 5. Counter-regimes / missed cases

- **Database regime.** PDB70 is a structure database (`pdb70_220313`). A sequence database
  (UniRef/ColabFold env) would almost certainly give nonzero depth over the tail, because K2P
  C-termini are present in sequence databases even where they are absent from structures. That
  is my inference; I ran no such search, because this container has no MMseqs2 or databases.
  So "0.0 past 326" is a property of **PDB70 at 2022-03-13**, not of kcnk5b. The author's
  proteins-findings.md already scopes it this way ("A deeper MSA than PDB70 (UniRef/BFD) — the
  single biggest lever").
- **Published counter-example.** I did not search the literature for an experimental disorder
  measurement (NMR, HDX, cryo-EM density) of the TASK2/KCNK5 C-terminus. Scope of that negative:
  no literature search performed. It remains `unknown` whether the tail is disordered.

## Scope of my searches

- `git log --all -- '*kcnk5b_pdb70.a3m'`: one commit, `8bf7ee39`.
- `git grep` on `origin/swarm-architecture` for `pdb70|use_msa_server|msa_server|colabfold|mmseqs`,
  for the file's sha256 prefix, and for the op ID. Nothing links the file hash to the Boltz2 job.
- Read the diffs of the three kcnk5b-pdb70 replicate/challenge branches. I did not read all 509 remote branches.
- No PDB/RCSB, UniProt or literature access was used for this verdict.

```swarm-challenge
{"claim_id": 211, "outcome": "weakened", "reason": "Numbers reproduce exactly (72 records; depth 21.40 / 0.52 / 0.0, and zero actually begins at residue 312), but the evidence level 'measured' is wrong for a count computed from a search output, and zero PDB70 depth cannot discriminate 'alignment ran out' from disorder, so 'the explanation holds' overreaches beyond 'Boltz2 pLDDT is not evidence of disorder'.",
  "corrected_value": "0.0 PDB70 MSA depth (derived, not measured) from residue 312 to 448; 2 rows (one distinct sequence, TASK2 6WLV/6WM0) over 241-311",
  "depends_on": ["origin/swarm-architecture@8bf7ee39:results/fish-proteins/structures/kcnk5b_pdb70.a3m (sha256 prefix 5eb89c812d003ca2)", "origin/swarm-architecture:results/fish-proteins/structures/kcnk5b_boltz2.cif", "origin/swarm-architecture:results/fish-proteins/structures/kcnk5b_esmfold2.cif", "origin/swarm-architecture:library/pages/project/claims.md (claim #26 labelled derived)", "origin/swarm-architecture:docs/research/fish/proteins-results.md (Boltz2 run used the PDB70 MSA)", "unverified assumption: committed a3m is byte-identical to Boltz2's input MSA"]}
```
