# Challenge 285: adversarial review of the replication of claim 207

**Claim under review (the author's words):** "Replication of the challenger-survival audit: three populations
disagree and none reproduces claim 207 (156 resolved: 109 weakened/26 survived/21 refuted = 17% survival).
(a) Replicator, from git challenge blocks: 28.5% = 49/172 latest verdicts (29.5% = 46/156 first resolved), at most
10 refuted; sampled evidence audit 10/10 documents (27/27 assertions) reproduce, 95% LB 69%. (b) Harvester,
designswarm DB at pass 6, latest non-not-run verdict per claim: 27 survived / 137 weakened / 15 refuted of 179 =
15.1% survival (DB includes 23 rows inserted by the harvester, which are mostly refuted/weakened and thereby bias
survival downward). (c) Original 17%. The audit half (challengers are not manufacturing faults) agrees; the rate is
not established and depends on which record is the population."
Recorded level: derived. Value: 28.5 percent survival (git, replicator).

**Verdict: WEAKENED.** The arithmetic is right, and I reproduced the git counts independently. The central
conclusion also holds: the rate depends on which population you count, and git does not reproduce 17 %. Four
things are wrong or overstated:

1. The git "first 156" comparator is not matched in time.
2. The recorded headline value has already drifted.
3. "Three populations disagree" may count one population twice.
4. "Thereby bias downward" does not follow from "mostly".

## 0. What I could and could not access

- **Git.** I fetched all 733 remote branches on 2026-11-04 at about 09:50 UTC. I wrote my own collector
  (`challenge-285/collect.py`) without reusing the replicator's code. It takes every blob of
  `docs/research/fish/challenge-N.md` added or modified in any commit reachable from a remote ref, and parses the
  last `swarm-challenge` block in each. Read-level: full-text (git objects).
  - **Observed:** 277 unique blobs, all of which parsed.
  - **Observed:** in every blob, the filename number equals the block's `claim_id`.
  - **Observed:** weakened 204, survived 59, refuted 14.
- **The designswarm database:** could-not-access. A TCP connect to 127.0.0.1:5436 from this container was refused.
  I therefore **cannot check any number in (b) or (c)**. The 27/137/15 of 179, the 23 harvester rows and
  109/26/21 of 156 are all the author's inputs to me.
- **Read in full:** the replicator's `replicate-207.md` on `origin/claude/replicate-207-challenger-audit-1mwyh0`,
  and the first challenge of 207 (`origin/claude/challenge-207-audit-yrcec6:docs/research/fish/challenge-207.md`).
- **Scope of my search for other challenge records in git:** other `.md` paths containing "challeng" on any remote
  ref. I found only helper scripts (`challenge-N_calc.py` and similar), and no second store of verdicts.

## 1. Arithmetic, redone independently (calculation)

- 109+26+21 = 156, and 26/156 = 16.67 %.
- 114+49+9 = 172, and 49/172 = 28.49 %.
- 46/156 = 29.49 %.
- 27+137+15 = 179, and 27/179 = 15.08 %.
- 0.025^(1/10) = 0.6915.
  - This is the **two-sided** 95 % Clopper–Pearson lower limit for 10/10.
  - The replicator's file calls it "one-sided 95 %"; the one-sided 95 % bound is 0.05^(1/10) = 0.741.
  - The mislabel is conservative, so it is cosmetic.
- I spot-checked a few of the replicator's audit numbers and all reproduce:
  - 360/φ² = 137.508°
  - 1.98·0.0403³/3 = 4.320×10⁻⁵
  - (120/40.3)⁴ = 78.61
  - 5.84/0.548 = 10.66
  - 10.66² = 113.6
- Wilson 95 % intervals (calculation). The 17 % interval does not overlap either git interval, so the git–original
  gap is not sampling noise if both are treated as samples:

  | Count | Survival | Wilson 95 % interval |
  |---|---|---|
  | 26/156 | 16.7 % | 11.6–23.3 % |
  | 46/156 | 29.5 % | 22.9–37.1 % |
  | 49/172 | 28.5 % | 22.3–35.6 % |
  | 27/179 | 15.1 % | 10.6–21.1 % |

**Git counts reproduced (observation plus calculation).** I applied the cutoff of the replicator's fixing commit
`0660b9e8` (committer time 1793784747).

- First verdict per claim, for the first 156 claim IDs by first commit time: **101 W / 46 S / 9 R = 29.5 %**. This
  matches exactly.
- Blobs up to the cutoff: **10 refuted** of 223. This matches "at most 10".
- Latest per claim: my count is 180 claim IDs with 50 survived (27.8 %), not 172 with 49.
  - Probable cause: committer time is not push time. Branches pushed after 0660b9e8 can carry earlier timestamps.
  - So I cannot rebuild the exact ref set the replicator saw. The 28.5 % is plausible but not exactly
    reproducible after the fact.

## 2. Proxy: the "first 156" is not the population claim 207 counted

The replicator offers "the first 156 claim IDs resolved, by first commit time" as the time-matched comparator for
the original 156. My observation contradicts this.

- Claim 207 existed before its first challenge was committed. That commit is `ec98d152`, committer time 1793783206
  (09:06:46 UTC).
- **Observed:** at that time, git held challenge documents for at most **130 distinct claim IDs** (163 blobs), not
  156.
  - It is an upper bound, because late-pushed commits can only add to what was visible then, never remove from it.
- **Observed:** for that git state, the latest verdict per claim was **80 W / 43 S / 7 R = 33.1 % survival**.
- **Calculation:** the replicator's 156 therefore includes at least 26 claims whose documents were committed after
  claim 207 had already been challenged. Those claims cannot be in the author's 156.
- **My inference:** the author's "156 resolved challenges" cannot be a set of distinct-claim git documents. It is
  more likely DB challenge rows, which can be several per claim, or not pushed, or not parsed from git.
- **Effect on the claim:** the disagreement gets stronger. The truly time-matched git figure is 33 %, not 29.5 %.
  But the "29.5 % = 46/156 first resolved" parenthetical in (a) is a size match that looks like a population match,
  and it is not one.

A coincidence, which I report without interpreting it. Across all blobs at that same cutoff, the weakened count is
exactly **109**, the original's number. Survived (47 against 26) and refuted (7 against 21) do not match, so I
read this as chance.

## 3. The recorded value is a snapshot that has already moved

Observed now, 2026-11-04 about 09:50 UTC, over all remote refs:

| Population | W / S / R | Survival |
|---|---|---|
| Latest verdict per claim | 157 / 53 / 12 of 222 | **23.9 %** (Wilson 18.7–29.9 %) |
| All blobs | 204 / 59 / 14 of 277 | 21.3 % |

- Refuted now stands at **14 blobs**, on 12 claim IDs. "At most 10 refuted" was true only at the replicator's
  time.
- The recorded value, 28.5 %, carries no timestamp or ref set. In under an hour, the same procedure gives 23.9 %.
- The claim's own conclusion is that "the rate is not established and depends on which record is the population".
  Recording a single 28.5 % as the value contradicts that conclusion.
- The value should be dated, or replaced by the dependence itself.
- The evidence level, *derived*, is fair. The counts are observations of git and the percentages are calculations.
  The defect is the missing time scope, not the label.

## 4. "Three populations disagree": (b) and (c) may be one population

- **The author's inputs:** the DB at pass 6 has 179 claims, of which 23 rows were inserted by the harvester.
- **Calculation:** 179 − 23 = **156**, the original's denominator.
- **Calculation:** if *s* of the 23 harvester rows are "survived", the remainder has (27 − *s*)/156 survival. With
  *s* = 1, that is exactly 26/156 = 16.7 %, the original figure.
- **My inference, not verified** (the DB could not be accessed): (b) may be (c) plus the harvester's rows. In that
  case they are not two independent records that disagree.
- **A caution against this reading:** refuted is 15 in (b) against 21 in (c). Adding rows that are "mostly refuted"
  cannot lower the refuted count.
  - This fits a units difference. (c) may count challenge rows, while (b) counts claims by their latest verdict, and
    a later re-challenge can supersede an earlier refuted verdict.
  - It also shows that the reconciliation is not clean.
- **Either way:** the claim presents a possible two-versus-one split, DB (≈15–17 %) against git (≈24–33 %), as
  three-way disagreement. The live question is DB versus git, not three records.

## 5. "Mostly refuted/weakened, thereby bias survival downward" is a non-sequitur

- Removing the 23 rows raises survival only if their survival share is below that of the whole: 27/179 = 15.1 %.
  That means at most 3 of the 23 can be survived.
- "Mostly refuted/weakened" means at least 12 of 23 are not survived. That still allows up to 11 survived, which is
  48 %.
- **Calculation:** with 5 survived (22 %, still "mostly refuted/weakened"), removing the 23 *lowers* survival to
  22/156 = 14.1 %.
- So the stated direction needs the actual count, which the claim does not give. I could not access it.

## 6. The "audit half agrees" leans on a proxy

- The replicator checked that cited evidence **exists and is quoted or computed correctly**. They checked 2–4
  assertions per document, chosen by them, in 10 seeded-random documents: 8 weakened, 2 survived, 0 refuted.
- Claim 207's audit asserted that weakened **verdicts were substantive**. The replicator says plainly that these are
  different tests.
- A challenger can cite real evidence accurately and still over-apply it, for example weakening a claim on a caveat
  that does not bear on the claim. That kind of "manufactured fault" passes an evidence-fidelity check.
- The refuted stratum, the one that most directly tests manufactured faults, was not sampled.
- The sample also excludes the 11 claim IDs whose documents mention "207", a disclosed but non-random exclusion.
- So "agrees" is warranted for **"the cited evidence is not fabricated"** (10/10, two-sided 95 % LB 69 %). It is not
  warranted for **"challengers are not manufacturing faults"** as worded.

## 7. What survives

- Every number in the claim follows from its stated counts.
- I reproduced the git counts at the replicator's cutoff (46/156; ≤10 refuted) with independent code.
- No git population I can build, at any cutoff I tried, gives 17 % survival or 21 refuted. Every git population sits
  at 21–33 %.
- The core statement, that git and the DB disagree and the rate depends on the record chosen, is correct.

```swarm-challenge
{"claim_id": 285, "outcome": "weakened", "reason": "The arithmetic and the git counts reproduce, and git (21-33%) truly disagrees with the DB (15-17%), but the '46/156 first resolved' comparator is not time-matched (git held at most 130 claim IDs, 33.1% survival, when claim 207 was challenged), the recorded 28.5% has no time scope and is already 23.9% (53/222), (b) and (c) may be one DB population (179-23=156) rather than independent disagreement, 'mostly refuted/weakened' does not imply the stated downward bias, and the agreeing audit checked evidence fidelity, not whether verdicts are substantive.",
  "corrected_value": "git survival is time-dependent: 28.5% (49/172) at the replicator's snapshot; 33.1% (43/130) for git at the claim-207 challenge commit; 23.9% (53/222) on 2026-11-04 ~09:50 UTC. DB 15.1% and 16.7% unverified (could-not-access)",
  "depends_on": ["git swarm-challenge blocks in docs/research/fish/challenge-N.md over all remote refs fetched 2026-11-04 ~09:50 UTC (277 blobs, my collector challenge-285/collect.py)", "committer timestamps as an upper-bound proxy for visibility time", "commit ec98d152 (first challenge of claim 207, 09:06:46 UTC) as the time by which claim 207 existed", "author's DB inputs: 27/137/15 of 179 at pass 6 and 23 harvester-inserted rows (not independently accessed)", "author's original counts 109/26/21 of 156 (not independently accessed)", "replicator's replicate-207.md audit table (10 documents, 27 assertions; spot-checked arithmetic only)"]}
```
