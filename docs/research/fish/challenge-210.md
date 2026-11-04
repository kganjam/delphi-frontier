# Challenge 210: the kcnk5b MSA "reproducibility gap", and Boltz2 36.4 vs 41.4

**Claim under review (not written by me):** "REPRODUCIBILITY GAP: kcnk5b_pdb70.a3m was never
committed, so the MSA depth profile behind the 'alignment ran out, not disorder' finding cannot be
independently reproduced. A challenge also reports Boltz2 reads 36.4 over 326-448 where 41.4 was the
261-448 mean." Recorded value: 36.4 pLDDT, evidence level unknown.

**Verdict: WEAKENED.** The gap was real when it was written, but it has since been closed. The file is
committed and I reproduced the depth profile from it here. Both pLDDT numbers are correct. They cover
two different residue windows, so they don't contradict each other. One small gap remains: the file
is not on `main`.

## 1. Was the a3m committed? (git inspection, observed)

- `results/fish-proteins/structures/kcnk5b_pdb70.a3m` was committed in **8bf7ee39** ("Commit the MSA
  files, and confirm our own finding by recomputing it", 2026-11-04 01:02 -0800). That commit's own
  message agrees that the file had not been committed before and credits the challenge. **So the
  claim was true when it was made.**
- Scope of the search: I ran `git ls-tree` on every one of the ~509 remote branches after
  `git fetch origin`. Exactly **one** blob of this file exists (`cc2802f2…`, 32,986 bytes), and it is on
  **`origin/swarm-architecture` only**. Commit 8bf7ee39 is **not** an ancestor of `origin/main`, and
  `origin/main` has no `results/fish-proteins/` tree. Many challenge/replicate branches carry
  `kcnk5b_boltz2.cif` and `kcnk5b-confidence.json` but **not** the a3m. So a reviewer working from
  `main`, or from one of those branches, still cannot reproduce the profile. That is the remaining gap.

## 2. Depth profile recomputed independently (computed from the committed file)

My own script (not the author's code). It parses the a3m, drops lowercase insertions, and counts
non-gap match columns per query position over the 71 hit rows.

| quantity | value (computed) |
|---|---|
| rows in a3m | 72 (query + 71) |
| query length | 448 |
| mean depth, res 1-250 | 21.4 (max 57) |
| mean depth, res 261-448 | 0.52 (max 2) |
| mean depth, res 326-448 | **0.0 (max 0)** |
| mean depth, res 261-325 | 1.51 (max 2) |
| last residue covered by any hit | 311 |

These match the numbers in 8bf7ee39 (21.4 / 0.5 / 0.0) exactly.

**Disagreement to preserve, not average away:** replicates 72430c85 / 7c79bf79 report "76 sequences".
That count comes from a **different file**,
`results/mol-sims/claude-20261101/structures/msa/kcnk5b_core.a3m` on `origin/claude/mol-sims-20261101`
(receipt `a3m_n_seqs: 76`, op-71484e57aa8b6dcb). Its query is a **265-residue core construct**
(I computed that its last covered residue is 263), so it says nothing about the 326-448 tail. The
72-row file is the one the Boltz2 tail argument depends on.

## 3. Boltz2 / ESMFold2 pLDDT recomputed (computed from committed CIFs)

I took per-residue pLDDT from the CA `B_iso_or_equiv` column of the committed CIFs on
`origin/swarm-architecture`. Both files have 448 residues, and the values are already on a 0-100 scale.

| window | Boltz2 | ESMFold2 |
|---|---|---|
| 1-448 | 62.03 | 83.63 |
| 1-260 | 76.95 | 88.87 |
| 261-448 (n=188) | **41.39** | 76.38 |
| 326-448 (n=123) | **36.37** | 76.43 |
| 261-325 (n=65) | 50.88 | 76.30 |

Both 36.4 (326-448) and 41.4 (261-448) are correct for their windows. The claim reports them side by
side as if they conflict, but they are different spans. Window 261-325 still has some MSA depth (1-2)
and Boltz2 reads 50.9 there, so the narrower window gives the lower mean. The "76.4" ESMFold2 figure
in 8bf7ee39 holds for either window (76.38 / 76.43). This is model self-confidence computed from the
files, not an observation of structure.

## 4. Proxy and hidden assumption (my inference, beyond the claim's scope)

- **Proxy:** the depth used here comes from a PDB70 (template) MMseqs2 search, not a UniRef/
  evolutionary MSA. It stands in for "evidence Boltz2 had", and it is the right proxy only if Boltz2
  was given this a3m as its MSA. Commit ba1dd261 says it was ("Boltz2 given a 72-sequence PDB70 MSA").
  I did **not** find a Boltz2 run receipt naming the a3m's sha256, so that link is the author's claim,
  not something I verified.
- **Confound the downstream finding does not address:** crystallised K2P constructs are often
  truncated *because* their C-terminal tails are flexible. In that case zero PDB70 depth past residue
  311 is expected whether or not the tail is disordered, so the depth profile can't by itself tell
  "evidence ran out" apart from "disorder". This affects the "not disorder" finding, not the
  reproducibility claim judged here, so I don't use it in the verdict.

## Sources (read-level)

- git objects in this repo (commits 8bf7ee39, ba1dd261, 72430c85, 7c79bf79; blobs listed above):
  full-text.
- No external literature consulted.

```swarm-challenge
{"claim_id": 210, "outcome": "weakened", "reason": "The a3m was uncommitted when the claim was made but is now committed (8bf7ee39, origin/swarm-architecture only, not main) and the depth profile reproduces exactly (0.0 over 326-448); both pLDDT figures are correct, and they cover different windows rather than disagreeing.", "corrected_value": "36.37 pLDDT (Boltz2 CA mean, residues 326-448, n=123, computed from committed CIF); 41.39 over 261-448", "depends_on": ["origin/swarm-architecture:results/fish-proteins/structures/kcnk5b_pdb70.a3m (blob cc2802f2)", "origin/swarm-architecture:results/fish-proteins/structures/kcnk5b_boltz2.cif", "origin/swarm-architecture:results/fish-proteins/structures/kcnk5b_esmfold2.cif", "commit 8bf7ee39 not ancestor of origin/main", "assumption (from ba1dd261, unverified): Boltz2 was run with this a3m"]}
```
