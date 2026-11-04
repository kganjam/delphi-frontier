# Challenge 207: adversarial review of the challenger-audit claim

**Claim under review (the author's words):** "CHALLENGER AUDIT: 156 resolved challenges returned 109
weakened, 26 survived, 21 refuted -- a 17% survival rate. I suspected the challengers were
manufacturing faults, sampled six weakened verdicts, and found the opposite: all six were
substantive, several correcting real errors against primary sources."
Recorded evidence level: derived. Value: 17 percent survival. Source: sampled audit of
`challenge.evidence`.

**Verdict: WEAKENED.** The arithmetic holds. The qualitative conclusion ("found the opposite")
claims more than a non-random-or-unknown sample of six can support, and I could not access the
underlying records to check either part.

## 0. What I could and could not access

- `challenge.evidence` / the 156 challenge records: **could-not-access.** I searched this repository
  (`kganjam/delphi-frontier`, branch `claude/challenge-207-audit-yrcec6`, every file plus
  `git log --all` and `git grep` over all reachable commits) for "challenge", "challenger",
  "weakened", "survival rate", "109" and "156". The only hits are the refutation ledger
  (`ledger/README.md`, read-level: full-text) and `CONTRIBUTING-VERIFICATION.md` (full-text). Neither
  holds the 156 verdicts or the six sampled ones. There is no swarm database in the checkout.
  Scope of that negative: this repository only. The data may exist elsewhere.
- So I **cannot** check the counts 109/26/21 independently, which six verdicts were sampled, how
  they were picked, or whether "substantive" holds for each one. Everything below takes the
  author's counts as given inputs.

## 1. Arithmetic, redone independently

From the stated inputs (calculated, not observed):

- 109 + 26 + 21 = **156**. The partition is consistent.
- Survival: 26/156 = **0.1667, i.e. 16.7%**. "17%" is a fair rounding.
- Weakened: 109/156 = 69.9%. Refuted: 21/156 = 13.5%.
- Sampling uncertainty on the survival rate (Wilson 95% interval, n = 156, calculated):
  **11.6% to 23.3%**. The claim gives a point value with no interval. That is a minor omission, not
  an error.

The arithmetic part **survives**.

## 2. Proxy check

- "Survival rate" (26/156) is being read as a measure of how good the claims are. Calculated from
  the author's inputs, it is just as much a measure of how far challengers are **incentivised to
  return a non-"survived" outcome**. The audit is aimed at exactly that confound, which is to its
  credit. But the quantity it needs is **the share of "weakened"/"refuted" verdicts that are
  substantive**, not the survival rate. The six-item sample is the only evidence on that share
  (see §3).
- **Denominator selection:** "156 *resolved* challenges". Unresolved or abandoned challenges are
  left out. If resolution depends on outcome (for example, a challenger who can't break a claim
  never files), 17% is biased low as a measure of claim robustness. Effect size: unknown, because the
  count of unresolved challenges is not stated and I could not access it.
- "Weakened" pools very different severities, from a scope caveat to a corrected central value.
  "Substantive" doesn't separate them, so 109 weakened verdicts do not mean 109 material defects.

## 3. The hidden assumption that carries the result: six items stand in for 109

The author observed that 6 of 6 sampled weakened verdicts were substantive. That observation is
theirs and I can't re-check it. My inference, calculated from 0 non-substantive in n = 6 and
**assuming a simple random sample**:

- One-sided 95% upper bound on the share of manufactured (non-substantive) weakened verdicts:
  1 − 0.05^(1/6) = **39.3%**. The two-sided Clopper–Pearson upper bound is 45.9%.
- So the data still allow **up to about 43 of the 109** weakened verdicts to be manufactured.
  A 6/6 result cannot tell "challengers do not manufacture faults" apart from "about a third of
  them do". "Found the opposite" states the first, which the sample cannot establish.

Relaxing the assumption makes this worse:

- **Sampling method not stated.** If the author picked the six (most recent, most readable, from
  domains they know), the bound above doesn't apply at all, and the true rate is unconstrained by
  this sample.
- **Only "weakened" was sampled.** The "refuted" (21) and "survived" (26) verdicts were not audited.
  A challenger who manufactures faults would show up in "refuted" as well. A lazy challenger would
  show up as false "survived" verdicts. Neither stratum was examined.
- **The judge is not independent.** "Substantive" was decided by one reader with no written
  criterion, possibly the same agent whose claims were challenged. That is not a reproducible
  measurement.

## 4. Is the evidence level honest?

- The **value** (17%) is correctly labelled *derived*: it is calculated from counts. No defect there.
- The **conclusion** ("all six were substantive … found the opposite") is a qualitative judgement
  on an n = 6 sample of unstated provenance. It is reported inside the same "derived" record, which
  makes it look as solid as the arithmetic. It should carry its own label (sampled qualitative
  audit, n = 6, selection method unstated) and its own uncertainty.

## 5. Counter-regimes the author missed

- **Base-rate regime:** a challenger that returns "weakened" by default would produce mostly
  verdicts that *are* defensible, because almost any real claim has some scope caveat. So "each
  weakened verdict is substantive" is compatible with "the weakened rate is inflated by the
  incentive". The audit doesn't separate these. Separating them would need blinded re-challenge of
  a random subset, or a calibration set of seeded-true claims with known answers. This is
  inference: I found no such calibration run in the repository (scope: this checkout).
- The repository's own ledger records one case where a refutation was itself mis-operationalised
  (`ledger/README.md`, row 9, read-level: full-text). So challenge outcomes in this project have
  been wrong before. That makes a "challengers are reliable" conclusion from n = 6 especially
  premature. This is an in-project precedent, not a published counter-example. I did not search the
  external literature.

## Summary

| Element | Status |
|---|---|
| 109 + 26 + 21 = 156; 26/156 = 16.7% ≈ 17% | survives (calculated) |
| Counts themselves | unverified: `challenge.evidence` could-not-access |
| "Six weakened verdicts were substantive" | the author's observation, not re-checkable here |
| "Found the opposite" (challengers aren't manufacturing faults) | overstated: with 0/6 the manufactured share is bounded only to ≤ 39% (95%, one-sided, random-sample assumption). Unbounded if the sample wasn't random. Refuted and survived strata not audited |
| Evidence label | value honestly "derived"; the qualitative conclusion needs its own label |

```swarm-challenge
{"claim_id": 207, "outcome": "weakened", "reason": "The 156/109/26/21 arithmetic and 16.7% survival are correct, but a 6/6 sample of unstated selection, drawn only from the weakened stratum and judged by one reader without a criterion, bounds the manufactured-fault share of weakened verdicts only to <=39% (95% one-sided, if random), so 'found the opposite' overstates what was shown.",
  "corrected_value": "survival 16.7% (26/156; Wilson 95% CI 11.6-23.3%); manufactured share of weakened verdicts not established, 0-39% (95% one-sided upper bound from 0/6, assuming random sampling)",
  "depends_on": ["author's counts: 156 resolved = 109 weakened + 26 survived + 21 refuted (not independently accessed)", "author's report that 6 of 6 sampled weakened verdicts were substantive (not independently accessed)", "assumption that the 6 were a simple random sample of the 109 (method unstated)", "ledger/README.md row 9 (in-project precedent of a mis-operationalised refutation)"]}
```
