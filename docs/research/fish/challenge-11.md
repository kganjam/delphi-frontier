# Challenge 11: the kcnk5b PDB70 search ("72 sequences, top hits are real K2P structures")

**Claim under review (not written by me):** "PDB70 search on kcnk5b returns 72 sequences whose top
hits are real K2P channel structures: 4BW5/4WFE (TRAAK), 4XDK/4XDL (TREK-2), 6WLV". Recorded
evidence level: *derived*. Value: 72 sequences. Source: `msa_search_native` against PDB70.

**Verdict: WEAKENED.** The main qualitative point holds: the top of a kcnk5b PDB70 alignment
really is K2P channels, led by the TASK-2 ortholog. But the claim as worded has one wrong
identity, counts the query as a hit, and cannot be re-derived from anything committed. The number
"72" also stands in for alignment depth and overstates it.

## Sources and read-levels

| source | what it is | read-level |
|---|---|---|
| `origin/swarm-architecture:results/fish-proteins/structures/kcnk5b-HITS.md` (commit 699500a7) | the author's own record of the search, op `op-6d4bf65638eb8348`, `pdb70_220313` | full-text |
| `origin/swarm-architecture:docs/research/fish/proteins-findings.md`, `proteins-results.md` | the author's write-up | full-text |
| `origin/claude/mol-sims-20261101:results/mol-sims/claude-20261101/structures/msa/kcnk5b_core.a3m` + `kcnk5b_core_receipt.json` (commit c97ff8d4) | a **separate** PDB70 search (op `op-71484e57aa8b6dcb`, same `pdb70_220313`) on a 265-residue kcnk5b *core* construct. The A3M is committed, sha256 in receipt `d65d3773…` | full-text (I parsed the A3M) |
| RCSB `data.rcsb.org/rest/v1/core/entry/<id>` for 4BW5, 4WFE, 4XDK, 4XDL, 6WLV, 6WM0 | entry titles | **could-not-access**: the egress proxy refused the connection (`connect_rejected`, ×12) from this container on 2026-11-04 |

## 1. Arithmetic, redone independently

**"72 sequences" counts the query.** The author's own HITS.md says: "71 hits across 69 unique PDB
entries, plus the query = 72 rows in the A3M." So the search returned **71 hits**, not 72. The
A3M has 72 rows. Saying "returns 72 sequences" is off by one in the direction that flatters the
search. It is small, but it is the claim's only number.

**I could not recompute 71 or 72 from the claim's own run.** HITS.md points to
`kcnk5b_pdb70.a3m` for the full list, and `proteins-readme.md` gives its path as
`msa_<tag>/<tag>_pdb70.a3m`. `git log --all -- '*.a3m'` finds no such file in any branch of this
repository. The only kcnk5b A3Ms committed anywhere are `kcnk5b_core.a3m` (a different construct
and operation, below) and `kcnj13.a3m` (a different gene). So "72" is **relayed** from HITS.md and
not re-derived. The rule this project set for itself ("committed so the numbers can be re-derived
from the artifacts rather than trusted", commit 699500a7) is not met for this number.

**Independent replicate (a different run, so treat it as corroboration and not a re-derivation).**
I parsed `kcnk5b_core.a3m` here:

- 76 rows = query + **75 hits** on 73 unique PDB entries. The receipt's `a3m_n_seqs: 76` matches.
  No duplicate headers.
- Query length 265 (the core construct). The claim's run used the full 448-residue Q6PFU3.
- Hit order, ranks 1–13: **6WLV_A, 6WM0_A, 4XDK_D, 4XDL_A, 4BW5_B**, 6W88_B, **4WFE_B**, 7LJ5_A,
  7LJ4_B, 4TWK_B, 3UKM_D, 7SK1_B, 6RV3_D. Every one of these aligns across both pore domains
  (query columns ~1–263 down to ~15–211).
- Identity over aligned columns (I computed it): 6WLV/6WM0 **0.64** over 263 columns. 4XDK/4XDL/4BW5
  0.40 over 245. 4WFE 0.41 over 231.
- Hits 14–75 align only to ~40–60 residues of one pore region (for example 1ORQ at 87–139, 2R9R at
  87–128, 6U9Z and 7T4X at 186–209). These are non-K2P potassium channels.

The replicate puts all five of the claim's named entries in the top seven, with the TASK-2 pair
first. This **supports** the "top hits" part of the claim. My inference (not the author's claim): a
full-length query would likely rank the same pore-domain hits the same way, because the extra 183
residues are the cytoplasmic tail, and the author reports zero PDB70 coverage there. That is still
an inference about a run whose ranking was never recorded. HITS.md lists ten identities with no
rank, E-value or score.

## 2. Is a proxy standing in for the quantity that matters?

Yes. "72 sequences" is being used as a stand-in for **how much evolutionary information the
alignment gave Boltz2**, and it overstates that quantity in three ways:

1. **Coverage.** In the replicate, only **12 of 75** hits cover at least 80% of the query, and 13
   cover at least 50%. The mean per-position depth is **20.8** (sum of per-hit coverage fractions,
   which I computed), not 75. The author's own full-length numbers are worse: mean depth **0.5**
   over residues 261–448 and **0.0** from residue 326 on (`proteins-results.md`). Over about 40% of
   the protein, the "72-sequence MSA" is a one-sequence MSA.
2. **Redundancy.** The top hits are repeated structures of the same proteins: 6WLV and 6WM0 are
   both TASK-2, and 4XDK, 4XDL and 4BW5 are all TREK-2. Five of the top seven rows are two
   proteins. The author's "69 unique PDB entries" therefore still over-counts independent sequences.
   (My inference: the redundancy suggests either that the database was not filtered at 70% identity
   as its name implies, or that it keeps several members per cluster. Which one is `unknown`, and I
   could not check it.)
3. **Superfamily breadth.** Most rows are not K2P. The author says so in HITS.md ("The hit set is
   *not* all K2P"). The claim's summary drops that caveat.

The quantity that matters is coverage-weighted effective depth (Neff), reported per region. For the
claim's run it cannot be computed, because the A3M is missing.

## 3. The hidden assumption, relaxed

The assumption is that **a larger hit count means a better-informed structure prediction.** Relax
it, and the author's own data breaks it: Boltz2 with this MSA scored mean pLDDT 62.0 and pTM 0.479,
while MSA-free ESMFold2 scored 83.6 and 0.607 (`proteins-results.md`). The MSA did help Boltz2 at
the selectivity filters (40.1 → 80.2 and 41.4 → 82.6 against single-sequence OpenFold2), which is
where the coverage is. Elsewhere it misled the model. The author already caught one consequence (the
"disordered tail" that was really an MSA-coverage artifact, CORRECTION 2). The count "72" is the
headline that invited that misreading.

## 4. Is the evidence level honest?

The count is the size of a computed tool output, so it is closer to *computed observation* than
*derived*. Labelling it "derived" **understates** it, which is not the defect the honesty floor is
meant to catch. The real evidence-level problem is a different one: the value is **relayed** from a
markdown note whose backing A3M is not committed. It should carry "relayed, artifact missing", not a
level that implies someone re-derived it.

## 5. Identities, and anything the claim missed

- **4BW5 is mislabelled.** The claim groups "4BW5/4WFE (TRAAK)". The author's own HITS.md, which
  says it checked RCSB on 2026-11-03, records 4BW5 as "human two pore domain potassium ion channel
  TREK2 (K2P10.1)" and states the correction outright: "4BW5 was first described in this session's
  reporting as TRAAK from memory; RCSB says TREK-2. 4WFE is the TRAAK entry." So the claim repeats an
  error the author had already corrected. I could not re-check RCSB myself (proxy refused).
  4BW5 = TREK-2 and 4WFE = TRAAK also matches my background knowledge, but that is recall and not
  evidence here. The two written sources do not disagree: the claim is just older than the
  correction.
- **The most important hit is left unlabelled.** HITS.md records 6WLV/6WM0 as "TASK2 in MSP1D1 lipid
  nanodisc" with RCSB gene name `Kcnk5`. That makes it the direct mammalian ortholog of zebrafish
  kcnk5b. The replicate ranks it first, at 0.64 identity. The claim lists "6WLV" without saying
  what it is, which hides the strongest part of its own case.
- **Counter-example to "top hits are K2P" being informative:** none found. Scope of that search: the
  committed replicate A3M and the author's ten RCSB-checked identities. Hits ranked 14 and lower are
  Kv, KcsA-like, MthK, NaK, plant AKT1 and others, and they align only to pore segments.
- **Two different "pdb70_220313" runs, two different counts.** Full-length: 71 hits / 69 entries
  (author). Core: 75 hits / 73 entries (replicate, my count). The difference is expected for a
  different query and is preserved here, not reconciled. It does show that "72" belongs to one
  construct, and is not a property of kcnk5b.

## What survives

- A PDB70 search on kcnk5b returns K2P structures at the top, led by TASK-2 (6WLV/6WM0, gene
  `Kcnk5`, the ortholog), then TREK-2 (4XDK, 4XDL, 4BW5) and TRAAK (4WFE). The independent
  replicate A3M corroborates this.

## Corrected statement

> `msa_search_native` against `pdb70_220313` on full-length kcnk5b (Q6PFU3) returned **71 hits over
> 69 PDB entries** (A3M of 72 rows including the query; relayed from HITS.md, A3M not committed).
> The top of the alignment is K2P: 6WLV/6WM0 (TASK-2, gene `Kcnk5`, the ortholog), 4XDK/4XDL/4BW5
> (TREK-2) and 4WFE (TRAAK). Most other hits are non-K2P potassium channels aligned only to the pore,
> and coverage is about 0 past residue 326. An independent core-construct run (75 hits, committed
> A3M) gives the same top ranking.

```swarm-challenge
{"claim_id": 11, "outcome": "weakened", "reason": "The top hits really are K2P (an independent committed A3M ranks 6WLV/6WM0 TASK-2, then 4XDK/4XDL/4BW5, then 4WFE, in its top 7), but 4BW5 is TREK-2 not TRAAK by the author's own RCSB check, 72 includes the query (71 hits, 69 entries), the backing A3M is not committed so the count is relayed rather than re-derived, and the raw count overstates effective depth (only 12/75 hits cover 80% or more of the query in the replicate; 0.0 depth past residue 326 in the original).", "corrected_value": "71 hits (69 PDB entries) + query = 72 A3M rows; 4BW5 = TREK-2, 4WFE = TRAAK, 6WLV/6WM0 = TASK-2 (Kcnk5)"}
```
