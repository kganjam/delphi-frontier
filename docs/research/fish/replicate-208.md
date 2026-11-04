# Replicate 208: what the low challenge survival rate is evidence of

**Question (answer withheld from me):** *The recurring challenge shape is "the arithmetic
reproduces, BUT the inference overreaches". So the low survival rate is not evidence of bad
challengers; it is ...*

**My answer:** it is evidence of **systematic inferential overreach in the claims** (sound
arithmetic, conclusions/labels/scope stated more strongly than the arithmetic licenses), i.e. a
property of the claims, not of the challengers. Quantitatively (all **calculated** from committed
challenge records, not observed in any experiment):

| quantity | value | 95% CI (Wilson) |
|---|---|---|
| challenge verdicts with outcome `survived` | **52 / 213 = 24.4%** | 19.1–30.6% |
| … `weakened` | 151 / 213 = 70.9% | — |
| … `refuted` | 10 / 213 = 4.7% | 2.6–8.4% |
| claims (172 distinct) where every challenge said `survived` | 44 / 172 = 25.6% | 19.6–32.6% |
| `weakened` verdicts whose reason has the shape "computation reproduces/holds, BUT inference/label/scope overreaches" (hand-coded random sample) | **17 / 24 = 71%** (18/24 = 75% counting one non-numeric "facts check out, but proxy presented as measured") | 51–85% |
| implied count of that shape among the 151 `weakened` | ≈ 107 (calculated: 0.71 × 151) | ≈ 77–128 |

So roughly three quarters of claims fail to "survive", but only ~5% are refuted; the modal
failure is a downgrade in which the challenger **confirms the number** and objects to what is
inferred from it. A challenger who reproduces the author's arithmetic exactly is evidence of a
competent challenger; the non-survival comes from the inference step.

## Inputs, sources and read-levels

- **Primary data:** every ```` ```swarm-challenge ```` JSON block in `docs/research/**/*.md` on all
  623 remote branches of `kganjam/delphi-frontier` that do not contain "208" in their name (fetched
  `--depth=1` on 2026-11-04). Read-level: **full-text** (machine-readable blocks parsed; 0 parse
  errors). 213 unique records after de-duplicating identical JSON across branches; 172 distinct
  `claim_id`s; 41 (claim, file) pairs appear with more than one distinct record (independent
  challengers or revisions — I could not tell which, and counted each).
- **Exclusions (deliberate):** records with `claim_id` 207 or 208, any file with "208" in its path,
  and any branch with "208" in its name (including `claude/challenge-claim-208-el83jm`), so as not
  to read prior working on this claim. Claim 207 was excluded because the brief's "audit inference"
  context suggested it might be the audit itself.
- **Shape coding:** a random sample of 24 of the 151 `weakened` reasons (`random.seed(208)`), coded
  by me. "Yes" = the reason states the arithmetic/numbers/recomputation reproduce, hold or are
  correct, and then faults an inference, label (e.g. evidence level `measured`), comparison,
  extrapolation or scope. "No" = the number itself is not reproducible, or a factual/citation claim
  is false. Yes: sample items 0,2,3,5,7,8,9,10,11,12,15,17,18,19,20,21,23. No: 1,4,6,13,14,16.
  Borderline counted only in the 75% figure: 22. This is **my judgment, not the challengers'
  label** — the schema has no field for it.
- A crude regex (arithmetic/numbers/calculation within 4 words of reproduce/hold/check/correct,
  plus "but/however/yet") flags 64/151 weakened; on the sample it had 12 hits, all true positives,
  and missed 5 ("exact", "recomputes", "is correct"), so it is a floor, not the estimate.

## Arithmetic

- 52/213 = 0.2441; 151/213 = 0.7089; 10/213 = 0.0469; 52+151+10 = 213.
- Claim level: 44/172 = 0.2558; 7 claims had challengers who disagreed on outcome (preserved, not
  averaged).
- Sample: 17/24 = 0.7083, Wilson 95% [0.508, 0.851]; × 151 = 107 (77–128).

## Uncertainty and limits

- The 71% rests on n = 24 hand-coded items; ±~17 points.
- "Survival" here is the claim surviving its challenge (`outcome == "survived"`), which is my reading
  of the question; if the source meant a different denominator (e.g. one swarm round only), the
  rate would differ. Scope of the record search: `docs/research/` on the 623 branches above only;
  challenges recorded elsewhere (PR comments, other repos such as `scopedesk`) were not searched.
- Nothing here tests whether challengers are *good*; it shows only that their dominant objection is
  not to the arithmetic, so a low survival rate does not by itself indict them.

## Comparison with the recorded value (read only after the derivation above was written)

Found on branch `swarm-architecture` (read-level: full-text of the lines quoted):

- `library/pages/project/claims.md` row 208: the claim, tier `derived`, **no numeric value**, source
  "audit inference". It depends on row 207: *"156 resolved challenges returned 109 weakened, 26
  survived, 21 refuted -- a 17% survival rate."*
- `docs/FINDINGS.md` l.117-120: *"231 challenges have been resolved ... 70% weakened, 17% survived,
  13% refuted. Sampling six weakened verdicts found all six substantive ... the low survival rate is
  a finding **about us**, not about the challengers."*
- `docs/specs/SPEC-evaluation-kernel.md` l.67-70: *"most claims in this project were stated more
  confidently than their inputs justified"*.

**Conclusion: AGREE.** The recorded completion ("a finding about us": claims overstated relative to
their inputs) is the same as mine, reached independently.

**Rates: DISAGREE, preserved, not averaged.** The recorded rates (17% survived, 13% refuted; n = 156
or 231) differ from what the git-committed records give me (24.4% survived, 4.7% refuted, 70.9%
weakened; n = 213). The weakened share agrees (70% vs 70.9%). The recorded figures appear to come from
a store ("challenge.evidence") I did not query; my count covers only `swarm-challenge` blocks
committed to `docs/research/` and excludes claims 207/208. The refuted share is the largest gap (21/156
vs 10/213) — I cannot tell whether refutations are under-committed to git or over-counted in the
store. Neither difference changes the conclusion: both sources put survival well under a third with
the modal outcome a downgrade, and my 71% (n=24) sample is a larger, consistent version of their 6/6.

```swarm-replication
{"claim_id": 208, "my_value": "evidence of systematic inferential overreach in the claims (a finding about the authors, not the challengers): calculated from 213 committed challenge records, 24.4% survived (95% CI 19-31%), 70.9% weakened, 4.7% refuted, and ~71% (17/24 sample, CI 51-85%) of weakened verdicts confirm the arithmetic while faulting the inference", "agrees": true,
  "note": "Same qualitative conclusion as the recorded claim, but my git-record rates (24% survived, 5% refuted, n=213) disagree with the recorded 17% survived / 13% refuted, which come from a store I did not query."}
```
