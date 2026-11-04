# Challenge 208: is the low survival rate really about overconfident claims, not about challengers?

**Claim under review.** Another author wrote this claim; I did not.

> "The recurring challenge shape is 'the arithmetic reproduces, BUT the inference overreaches'. So the
> low survival rate is not evidence of bad challengers; it is evidence that most claims in this project
> were stated more confidently than their inputs justified."

The claim's recorded evidence level is `derived`, its value is `n/a`, and its source is `audit inference`.

**Verdict: WEAKENED.**

- **First sentence: largely holds, as a majority rather than "the" shape.** I classified the 75 science claims that did not survive. The "reproduces but overreaches" shape covers 44 of them (58.7%). In another 24 (32.0%), a stated number, an input reading or a factual premise is itself wrong. "The arithmetic reproduces" does not describe those 24.
- **Second sentence: does not follow from the evidence, and parts of the record contradict it.**
  - The survival rate depends heavily on what kind of claim is challenged: 27 of 31 status claims survived (87.1%), against 13 of 92 science claims (14.1%).
  - Claims written by challengers and replicators fail when re-challenged too: 5 of 7 did not survive.
  - Two challengers of the same claim reached different outcomes in 4 of 29 cases.
  - In 4 cases a challenger marked a claim it had confirmed true as WEAKENED, because of defects outside the claim.
  - Survival rate is a proxy for overconfidence that cannot separate the claimant's errors from the challenger's choices.

Every number below is **calculated by me** from verdict blocks committed in this repository, or is **my
own manual classification** (a judgement, labelled as such). None of it is an observation of an organism.

---

## 0. Locating the claim and its population

- **Source document: not found.** On 2026-11-04 I ran `git grep` over all 512 remote refs of `kganjam/delphi-frontier` for these phrases:
  - "recurring challenge shape"
  - "not evidence of bad challengers"
  - "survival rate"
  - "stated more confidently than"

  None of them matched the claim. ("survival rate" matched only coral-literature text.) So I judge the claim as quoted. I could not see the audit's own denominator or coding. Read-level for the audit: `could-not-access`.
- **Population.** I collected every `docs/research/**/challenge-<n>*.md` file on all 512 refs and deduplicated identical files by git blob, which gave 189 files.
  - 37 of those files have no parseable `swarm-challenge` block. They are excluded, which is a scope limit.
  - The rest give 152 verdict blocks covering 123 distinct claim IDs.
  - Script: `challenge-208/collect.py`. Snapshot: `challenge-208/verdicts-snapshot.json`. Tally: `challenge-208/tally.py`. Read-level for all of them: `full-text`, read straight from git.
- **Scope.** This population is the fish/zebrafish-flight challenge swarm. It is not "this project" as a whole: claims that were never challenged are not in it.

## 1. Arithmetic, redone independently

The claim states no numbers, so I computed the ones it implies (calculated, `tally.py`).

| Stratum | Claims | Survived | Weakened | Refuted | Split (challengers disagree) |
|---|---|---|---|---|---|
| Status ("LAWENTRY x dispatched", IDs 32–35, 41–51, 53–68) | 31 | 27 (87.1%) | 4 | 0 | 0 |
| Science (all others) | 92 | 13 (14.1%) | 68 | 7 | 4 |
| All | 123 | 40 (32.5%) | 72 | 7 | 4 |

"Low survival" is true for science claims (14.1%) and false for status claims (87.1%).

**Is the "reproduces but overreaches" shape real? Two independent checks:**

- **Keyword check (calculated).** There are 103 non-survived verdict files on science claims.
  - 62 of them (60.2%) say in their `reason` that the arithmetic or numbers reproduce.
  - 22 of them (21.4%) say the conclusion or its direction still stands.
  - 21 of them (20.4%) complain about evidence-level or "measured" labelling.
- **Manual coding (my judgement, single coder, no inter-rater check; `codes.json`).** I read each of the 75 non-survived science claims and placed it in one class:
  - **A, 44 (58.7%).** The numbers reproduce, but the inference, scope, proxy or wording overreaches. Examples: 1, 3, 24, 28, 84, 91, 145.
  - **B, 24 (32.0%).** A stated number, an input reading or a premise is itself wrong or cannot be reproduced. Examples:
    - 26: the value reads 36.4, not 41.4.
    - 29: the result sits at the 89th percentile, not below the null.
    - 93 and 135: the load was applied at 2/3 of the length, not at the tip.
    - 129: the noise was applied to the wrong trace.
    - 167: the KEY number cannot be reproduced.
    - 200: the stated upper bound cannot be reproduced.
  - **C, 4 (5.3%).** Only evidence-level or provenance labelling is wrong (6, 86, 130, 131).
  - **N, 3 (4.0%).** A negative or absence statement is wrong (4, 81, 160).

Both checks agree on the first sentence: the shape is the **most common one, at about 3 in 5**. It is not universal. In about 1 in 3 failures the arithmetic or its inputs are themselves wrong.

## 2. The proxy: survival rate stands in for "the claims were overconfident"

To support its conclusion, the claim needs a measure of the gap between a claim's stated confidence and what its inputs justify. What it actually uses is the share of claims that a challenger did not mark as SURVIVED. That proxy mixes three things:

1. **How strict the outcome scale is.** WEAKENED absorbs any defect anywhere in a claim. 22 of 103 non-survived science verdicts say the conclusion still stands. These claims are overconfident in a detail, not in their result. This partly supports the claim: the wording was more confident than the inputs. But it also means the 14.1% figure is a measure of "no defect at all". It is not a measure of claims whose confidence was unjustified.
2. **Challenger scope choices.** Claims 42, 51, 57 and 60 each said only "LAWENTRY x dispatched".
   - In each case the challenger confirmed that the dispatch happened (`full-text` from git).
   - In each case the challenger still recorded WEAKENED, because of defects in the delivered entry's content.
   - Challenge 42 says so directly: "I also tested what 'dispatched' stands in for."

   In these 4 cases the claim as stated was true, so the lower survival comes from the challenger's choice of scope. This is a direct counter-example to the claim's dichotomy, which says the low survival rate reflects either the claims or the challengers.
3. **Which claims get challenged.** Many science claims in this population are "sensitive-input" or "deepen" (`-D-D`) harvests. They were picked because they carry a fragile KEY number. A low survival rate in a sample chosen for fragility tells us little about "most claims in this project".

## 3. The hidden assumption: the challengers' verdicts are accurate

The second sentence only follows if a non-survival verdict is correct. I tested that assumption with the evidence available in the repo.

- **Challenger-authored claims fail too (calculated, small n).** Seven claims in the population were written by a challenger or a replicator:
  - 23: output of challenge-5. Weakened.
  - 69: output of challenge-12. Weakened.
  - 70: output of challenge-28. Survived.
  - 71: output of challenge-29. Survived.
  - 90: claim 89's correction to challenge-82. Refuted.
  - 84: output of replicate-52. Weakened.
  - 86: output of replicate-5. Weakened.

  Only 2 of 7 survived (29%). That is higher than the 14.1% for science claims overall, but with n = 7 the difference does not separate the groups. Two examples:
  - Challenge 90 refuted a correction to an earlier refutation. That earlier challenge's own inference overreached.
  - Challenge 69 found that challenge-12's REFUTED verdict rested on "template-free", which is not established.

  So the agents who write challenges are fallible in the same way as the agents who write claims. The data do not show that challengers are good. They show that both groups produce this shape of error.
- **Challengers disagree with each other (calculated).** Of the 29 claims challenged more than once, 4 split between SURVIVED and WEAKENED (128, 138, 140 and 159), which is 13.8%. In 140, the split depends on whether the challenger happened to find one full-text measurement (Demesmay et al. 2025). So the outcome depends partly on how far a challenger's search reached. That is a property of the challengers, not of the claim.
- **Relaxing the assumption.** There is no ground truth, so the challengers' error rate is `unknown`.
  - If challengers err at even the 13.8% split rate, the science survival rate stays low. On that point the claim's direction is robust.
  - But "not evidence of bad challengers" is a claim that the challengers' error rate is low. Nothing in the population measures that rate, and the two checks above measure it as non-zero.

## 4. Is the evidence level honest?

The claim is recorded as `derived` from "audit inference". It is not derived in any sense I can check.

- It gives no denominator, no survival figure and no coding rule.
- Its source document cannot be found (§0).
- Its second sentence is a **causal attribution** ("not evidence of X; evidence of Y"), and tallying outcomes cannot establish one.

The honest level is **inference/hypothesis**. The claim itself states its conclusion more confidently than its inputs justify, which is the very defect it diagnoses.

## 5. Counter-examples the author missed

- **Claims that were too cautious, not too confident:**
  - Claim 160 said 3.8e-6 N m² "could not be traced". Two challengers found it in Puri et al. 2018 (`full-text`, according to those challengers; I did not re-read it).
  - Claim 4 called adult zebrafish peak speed "unknown", but a bound existed.
  - Challenge 139 found one clause "stronger than the author establishes".
  - Challenge 32 says the claim "understates what happened".

  "Stated more confidently than inputs justified" does not describe these cases.
- **Status claims (31)** survive at 87.1%, so the word "most" fails for the population as a whole. It holds only for challenged science claims.

## What survives

These parts of the claim hold under every relaxation I tried:
- Within challenged **science** claims, the single most common failure is that the numbers reproduce but the inference overreaches (about 59% by manual coding, 60% by keyword).
- Survival is low (14.1%).

These parts do not hold:
- "The" recurring shape, which ignores the 32% of failures with real numeric or input errors.
- "Most claims in this project", because survival is stratum-dependent and the sample was selected for fragility.
- "Not evidence of bad challengers", because challengers' own outputs fail, challengers split 13.8% of the time, and 4 confirmed-true claims were downgraded on scope.

**Corrected statement:** "Among the 92 challenged science claims (14.1% survived), the most common failure is that the numbers reproduce but the inference overreaches: 44 of 75 failures (58.7%), by single-coder judgement. In 24 (32.0%), a number or input was itself wrong. Status claims survived at 87.1%. The tallies cannot separate claim overconfidence from challenger error: challenger-authored claims also failed (5 of 7), and repeat challenges split in 4 of 29 cases. Evidence level: inference."

```swarm-challenge
{"claim_id": 208, "outcome": "weakened", "reason": "The reproduces-but-overreaches shape is the majority failure mode for challenged science claims (44/75, 58.7%, single-coder judgement) but 24/75 (32.0%) involve wrong numbers or inputs, survival is stratum-dependent (science 13/92 vs status 27/31), and the 'not bad challengers' attribution is unsupported since challenger-authored claims also failed (5/7), repeat challenges split 4/29, and 4 confirmed-true status claims were downgraded on out-of-scope content.", "corrected_value": "science-claim survival 14.1% (13/92); overreach shape 58.7% (44/75) of science failures; numeric/input error 32.0% (24/75); evidence level should be inference, not derived", "depends_on": ["swarm-challenge verdict blocks on all 512 origin refs as of 2026-11-04 (challenge-208/verdicts-snapshot.json, 152 blocks, 123 claims; 37 unparseable files excluded)", "manual single-coder A/B/C/N classification in challenge-208/codes.json", "status-claim stratum = claim IDs 32-35, 41-51, 53-68", "identification of claims 23, 69, 70, 71, 84, 86, 90 as challenger/replicator outputs", "challenge-42, -51, -57, -60 verdicts (dispatch confirmed, weakened on entry content)", "split verdicts on claims 128, 138, 140, 159", "challenge-160 finding that 3.8e-6 N m^2 is traceable to Puri et al. 2018"]}
```
