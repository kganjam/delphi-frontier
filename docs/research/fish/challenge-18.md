# Challenge 18: "Boltz2 reaches 0.0% >pLDDT 70 on and1/and2 and does worse than OpenFold2 because the MSA has depth 1"

**Verdict: WEAKENED.** The recorded number holds up as a recorded number. The comparison and its
explanation do not: "worse" and "because the MSA has depth 1" are inferences, and the data in the
record does not support either one.

## The claim under review (the author's words, not mine)

> "and1 and and2 reach 0.0% of residues above pLDDT 70 under Boltz2, which performed WORSE than
> single-sequence OpenFold2 for both -- the expected behaviour of an MSA-dependent model given an
> MSA of depth 1"
>
> Recorded evidence level: `simulated`. Value: 0 percent of residues with pLDDT>70. Source: Nebius
> `boltz2_predict_native`.

Where it was found: commit `ba1dd261` on `origin/swarm-architecture`. The files are
`docs/research/fish/proteins-findings.md` lines 74–76 and `docs/research/fish/proteins-results.md`,
which the author says `report.py` regenerated from downloaded artifacts. Read-level: full-text,
because I read the repository files directly.

The table I worked from (copied from `proteins-results.md`):

| protein | model | residues | mean pLDDT | pTM | %>70 | MSA depth |
|---|---|---|---|---|---|---|
| and1 | OpenFold2 (single-sequence dummy MSA) | 570 | 47.6 | 0.219 | 4.9% | 1 |
| and1 | Boltz2 + PDB70 MSA | 570 | 38.1 | 0.219 | 0.0% | 1 |
| and2 | OpenFold2 (single-sequence dummy MSA) | 508 | 44.3 | 0.234 | 1.0% | 1 |
| and2 | Boltz2 + PDB70 MSA | 508 | 36.1 | 0.184 | 0.0% | 1 |

## 1. Arithmetic, redone independently

- **Residue counts: verified.** I counted residues in the committed FASTA files myself.
  `E7F5V5.fasta` (and1) has 570 aa and `A0ACM8QEN9.fasta` (and2) has 508 aa. Both match the table.
- **Converting percentages to residue counts (my calculation).** 0.0% of 570 is below 0.29 residues,
  so the count is 0/570. 0.0% of 508 is 0/508. On the OpenFold2 side, 4.9% of 570 is about 28
  residues (28/570 = 4.91%), and 1.0% of 508 is about 5 residues (5/508 = 0.98%). So "worse" on this
  metric means 28 → 0 residues for and1 and 5 → 0 residues for and2.
- **Mean pLDDT gaps (my calculation).** and1: 47.6 − 38.1 = 9.5 points. and2: 44.3 − 36.1 = 8.2
  points.
- **pTM.** and2: 0.234 → 0.184, lower under Boltz2. and1: 0.219 → 0.219, **a tie**. So on pTM,
  "worse for both" is false for and1.
- **Things I could not recompute.** The per-residue pLDDT for the and1/and2 runs is not in any
  commit I could find. `git ls-tree` of `results/fish-proteins/` on `origin/swarm-architecture` has
  only the kcnk5b structures. The files the README lists (`boltz2_<tag>/<tag>_boltz2.cif`,
  `operations.jsonl`, `RESULTS.md`) are not committed for and1 or and2. I also searched `git log
  --all` for `operations.jsonl`, `pipeline.py` and `stage2.py` and found nothing. So **the 0.0% can
  be checked for internal consistency but not reproduced.**
- **A gap in the record.** In the README operations table, every row says `SUCCEEDED` except the
  and2 Boltz2 fold (`op-b56860ee55e67b62`, key `boltz2-and2-1793775012`), which has no terminal
  status. Numbers for that run appear in the results table, so it probably finished, but the record
  does not show it.

## 2. Proxy: "performed worse" uses lower self-confidence in place of lower accuracy

pLDDT is a model's confidence in its own output. The source documents say exactly this. No
experimental structure of and1 or and2 exists, and none was compared. So "Boltz2 performed worse"
compares two confidence values, not two accuracies. The quantity that matters is error against a
real structure or ensemble, and for these proteins it is `unknown`.

For these particular proteins the proxy can point the wrong way:

- The same branch's `proteins-disorder.md` uses sequence-only FoldIndex. It predicts **and1 is
  intrinsically unfolded** (global FI −0.056; 65.1% of windows below 0). If and1 is mostly
  disordered, a model that puts 0 residues above 70 may be **closer to the truth** than one that
  puts 28 residues above 70. That would make the Boltz2 output better calibrated, not worse. This
  is my inference. It is not established, because FoldIndex is a predictor, not a measurement.
- Published work treats low AlphaFold pLDDT as a useful but imperfect disorder indicator. Ruff &
  Pappu 2021 (J Mol Biol 433(20)) warn against reading AlphaFold models of IDRs as structures;
  read-level: listing/search-summary. Later studies report that pLDDT tracks residue-wise disorder,
  with exceptions such as conditionally folded IDRs; read-level: search-summary. Under that reading,
  lower pLDDT on a disordered chain is the expected *correct* output, not a failure.
- **pLDDT is not calibrated the same way across models.** OpenFold2's pLDDT head and Boltz2's
  confidence module are different networks trained on different objectives. Subtracting one
  model's pLDDT from the other's ignores that. An 8–10 point gap between two architectures does not
  show one is worse on the same scale.

The neutral statement the data supports is: "Boltz2 was *less confident* than OpenFold2 on both
actinodins." "Worse" goes beyond that.

## 3. The hidden assumption: MSA depth explains the gap. Relaxing it breaks the explanation.

The author explains the gap as "an MSA-dependent model given an MSA of depth 1." But the author's
own table shows that **OpenFold2 also had MSA depth 1** (a single-sequence dummy MSA, by
construction of `infer_openfold2_native`). OpenFold2 is also an MSA-dependent architecture, since it
reproduces AlphaFold2.

So both arms had the same MSA depth, and MSA depth does not differ between the conditions being
compared. "Depth 1" can explain why **both** models give low confidence. It cannot explain why
Boltz2 is **lower than** OpenFold2. The gap must come from something else, for example:

- architecture and training (how each model was trained to handle a missing MSA)
- confidence-head calibration
- sampling settings: recycles, diffusion samples, seed
- noise from a single run

None of these was varied, and each model ran once: one operation per protein per model, with no
seed or sample sweep recorded. So **the mechanism in the claim is untested, and the obvious
version of it is ruled out by the claim's own data.** This is my inference, drawn from the
author's table.

A second assumption: "depth 1" describes the database, not the protein family. The MSA came from
`msa_search_native` against `pdb70_220313`, which is a structure database. The author states this
scope ("the negative is against a STRUCTURE database"). Zhang et al. 2010 (Nature 466:234–237,
doi:10.1038/nature09137) report actinodin sequences in several teleosts and in the elephant shark;
read-level: abstract/search-summary. So a sequence-database MSA (UniRef or a metagenomic set) would
almost certainly be deeper than 1. That alignment was not built. The run labelled "Boltz2 + PDB70
MSA" was therefore effectively **Boltz2 in single-sequence mode**, and says nothing about Boltz2
with a real evolutionary MSA. Scope of my own search for such an alignment in the repository:
`git grep` for `boltz|plddt|openfold` on six branches, plus `git log --all` commit-message greps.
No actinodin UniRef or ColabFold alignment was found.

## 4. Is the evidence level honest?

Partly not.

- `simulated` is the wrong word. These are **model predictions**, meaning computed outputs of
  trained networks. Nothing was simulated (no physics or dynamics) and nothing was measured. The
  label should be "predicted/computed".
- The claim combines three kinds of statement under one evidence level:
  - a computed value: 0.0%
  - a comparison that depends on the proxy above: "WORSE"
  - a mechanism that was never tested: "the expected behaviour of… depth 1"

  Only the first is covered by the run. The other two are the author's interpretation and should be
  labelled as inference.
- The value cannot be traced to a committed artifact (see section 1). Calling it backed by a
  `boltz2_predict_native` source is accurate about the operation. It is not reproducible from the
  repository.

## 5. Missed regimes and counter-examples

- **Disordered or low-complexity proteins.** For an IDP, low confidence is the expected correct
  output, so "worse" is the wrong frame (section 2). The author's later disorder document calls
  and1 unfolded and leaves and2 open. The comparison may mean different things for the two
  proteins.
- **MSA-free models.** On kcnk5b the same project found that ESMFold2 (no MSA) beat Boltz2 + PDB70
  by a wide margin: 90.0% vs 38.8% of residues >70. ESMFold2 was not run on and1 or and2 (the
  esmfold2 lane wedged at admission). So the project's own best MSA-independent model is missing
  from this comparison, and the actinodin result is `unknown` for it.
- **Deeper MSAs.** As in section 3, this is untested.

## What survives

- As a recorded model output, under the default single-run settings: and1 and and2 have 0/570 and
  0/508 residues above pLDDT 70 under Boltz2 with a depth-1 PDB70 alignment. This is consistent with
  the residue counts I verified. It is not reproducible here because the artifacts are not
  committed.
- Boltz2's mean pLDDT is 9.5 and 8.2 points lower than OpenFold2's. Its pTM is lower for and2 and
  tied for and1.
- Neither model is confident about either actinodin, which fits the author's wider "no fold to
  improve" reading.

## What does not survive

- "Performed WORSE." This is a confidence comparison between differently calibrated models, with no
  ground truth. For the protein predicted to be disordered, it may point the wrong way. On pTM it is
  a tie for and1.
- "Expected behaviour… given an MSA of depth 1." Both arms had depth 1, so depth cannot explain the
  gap between them.

```swarm-challenge
{"claim_id": 18, "outcome": "weakened", "reason": "The 0.0% (0/570, 0/508 residues >pLDDT 70) is internally consistent but not reproducible from committed artifacts; 'worse' compares differently calibrated self-confidence with no ground truth (pTM ties for and1, and lower confidence may be correct for the FoldIndex-unfolded and1); and the MSA-depth explanation cannot account for the gap because OpenFold2 also ran at MSA depth 1.",
  "corrected_value": "0 of 570 (and1) and 0 of 508 (and2) residues above pLDDT 70 under Boltz2 (model prediction, single run, depth-1 PDB70 MSA); Boltz2 was less confident than OpenFold2 by 9.5 and 8.2 mean-pLDDT points; no accuracy difference established"}
```
