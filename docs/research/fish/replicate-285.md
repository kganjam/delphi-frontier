# Replicate 285: an independent re-derivation of the challenger-survival audit

**What kind of result this is.** These are **observations** of git objects in `kganjam/delphi-frontier`: branch
refs, blobs, and commit times. They also include **calculations**, meaning tallies and Wilson intervals I computed
from those objects. There is no simulation and no laboratory measurement.

## Disclosures (read before the numbers)

- **I was given** the title "Replication of the challenger-survival audit" and the context line "branch
  `claude/replicate-207-challenger-audit-1mwyh0` replicate-207.md; harvester DB query". The value had been removed.
- **What I saw before my value was fixed.** I listed that branch's files with `git diff --stat`. That output showed
  its commit subject: "Replicate claim 207: blind sampled audit of challenge evidence (10/10 docs reproduce)".
  - I saw that subject **by accident**. I did not open `replicate-207.md` or its scripts until my tallies below were
    computed. My harvester also excludes that branch.
- **To learn what claim 207 says,** I read `docs/research/fish/challenge-207.md` on
  `origin/claude/challenge-207-audit-yrcec6` in full (read-level: full-text).
  - That file is an adversarial **challenge** of claim 207. It is not the derivation behind claim 285.
  - It quotes claim 207: "156 resolved challenges returned 109 weakened, 26 survived, 21 refuted -- a 17% survival
    rate", plus an audit of 6 weakened verdicts.
  - It also restates the arithmetic 26/156. **I read the author's input counts before deriving.** What I derived
    myself is the counts from primary records, not the arithmetic.
- **Harvester DB: could-not-access.**
  - The repository has no DSN or credentials for a harvester or swarm database. I checked the environment variables
    and the checkout.
  - A TCP connect to `127.0.0.1:5436` was refused. I chose that port only after reading the comparison document; I
    did not try it blind.
  - So I read **no** database row, and every count below comes from git.

## Primary source and method

The challenger writes `docs/research/fish/challenge-N.md`, ending in a fenced `swarm-challenge` JSON block that
carries `claim_id` and `outcome`. I confirmed that format on the challenge-207 branch (full-text).

1. **Harvest** (`replicate-285/harvest.py`).
   - Fetched all 736 remote branch refs on 2026-11-04.
   - Ran `git grep -l swarm-challenge <ref> -- '*.md'` on each ref, then parsed every block with `json.loads`. All
     276 blocks parsed as JSON.
   - Excluded `claude/replicate-207-challenger-audit-1mwyh0`.
   - **Read-level:** full-text (git objects).
2. **Deduplicate** (`replicate-285/tally.py`).
   - Keyed each block on its blob SHA, `claim_id` and `outcome`.
   - All 276 blocks are distinct blobs. No branch reuses another branch's challenge file. They cover 223 distinct
     claim IDs. 53 claims have more than one challenge, and in 8 of those the challenges disagree on the outcome.
3. **Time-match.** I dated each challenge by the commit that first added its file. Claim 207 states n = 156, so I
   took the first 156 challenges in that order, which is the snapshot closest to when claim 207 was written.
   - All 276 were added between 2026-11-04T06:13 and 09:51 UTC.
   - The 156th falls at 09:06:35, 11 s before the challenge of claim 207 was committed (09:06:46). That is consistent
     with this snapshot predating that challenge.

## Results (observed counts, calculated rates)

| Population | n | weakened | survived | refuted | survival | Wilson 95 % CI |
|---|---|---|---|---|---|---|
| **First 156 challenges by add-time (time-matched)** | 156 | 104 | 45 | 7 | **28.8 %** | 22.3–36.4 % |
| All challenges before the challenge-207 commit | 160 | 108 | 45 | 7 | 28.1 % | 21.7–35.5 % |
| Earliest challenge per claim ID | 223 | 160 | 51 | 12 | 22.9 % | 17.8–28.8 % |
| All 276 challenge blobs (snapshot 2026-11-04 ~09:52 UTC) | 276 | 205 | 57 | 14 | 20.7 % | 16.3–25.8 % |
| *Claim 207's counts (database, not accessed)* | 156 | 109 | 26 | 21 | 16.7 % | 11.6–23.3 % |

**Arithmetic.**

- 45/156 = 0.2885.
- 104 + 45 + 7 = 156.
- Wilson interval with z = 1.96: centre (p + z²/2n)/(1 + z²/n), half-width z·√(p(1−p)/n + z²/4n²)/(1 + z²/n). This
  gives 0.223 to 0.364.
- 57/276 = 0.2065. 51/223 = 0.2287.

**My value:** in git, the challenger-survival rate time-matched to claim 207 is **28.8 % (45/156; 95 % CI 22.3–36.4
%)**.

- Across all challenges currently in git it is **20.7 % (57/276)**.
- The git records contain at most **14 refuted** outcomes in any population, against the 21 that claim 207 states.

**Interpretation (my inference, not verified).** Git and the database the claim counted are not the same population,
or they record different outcomes. Possible reasons:

- challenge rows whose documents were never pushed, or were on branches since deleted;
- outcomes revised in the database after the block was committed;
- a different definition of "resolved".

I cannot tell which record is wrong.

**Scope of the negative** ("git cannot give 17 %"):

- It covers the `swarm-challenge` blocks in `*.md` files at the tips of the 736 remote branches on 2026-11-04.
- It does not cover blobs in a branch's history that its tip has since overwritten, deleted branches, or the
  database.
- Even counting every blob, survival stays at or above 20.7 %. I did **not** independently re-audit whether the
  weakened verdicts are substantive (the "sampled audit" half of claim 207).

## Comparison with the recorded value (read only after the numbers above were fixed)

I then read `docs/research/fish/replicate-207.md` on `origin/claude/replicate-207-challenger-audit-1mwyh0` (full-text).
It records two things:

- From git: survival **28.5 %** (49/172, latest verdict per claim ID) and **29.5 %** (46/156, the first 156 claim IDs
  resolved), with git refuted counts of at most 10.
- A seeded audit in which 10/10 sampled documents (27/27 assertions) reproduce. Its conclusion is DISAGREE with
  claim 207's 17 %.

| Quantity | Recorded (claim 285) | Mine | Status |
|---|---|---|---|
| Survival, time-matched n = 156 | 29.5 % (46/156, first 156 claim IDs) | 28.8 % (45/156, first 156 challenges) | **AGREE**: within 1 count. The populations differ slightly: theirs is per claim ID, mine per challenge |
| Survival, broad population | 28.5 % latest-per-claim (172 IDs); 25.1 % all 215 blobs | 22.9 % earliest-per-claim (223 IDs); 20.7 % all 276 blobs | Same direction. Mine is lower because my snapshot is later: I found 276 blobs against their 215, and the later challenges are mostly "weakened" |
| Refuted count in git vs 21 claimed | ≤ 10 | ≤ 14 | **AGREE**: git cannot reach 21 |
| Git cannot reproduce 17 % | yes | yes | **AGREE** |
| 10/10 evidence audit | 10/10 docs, 27/27 assertions | not attempted | **CANNOT TELL** |

**Overall: AGREE** on the survival half. Two derivations independently reach about 29 % (time-matched) from the git
challenge blocks, not 17 %. I did not test the evidence-audit half.

```swarm-replication
{"claim_id": 285, "my_value": "28.8% survival (45/156 time-matched git challenge blocks; Wilson 95% CI 22.3-36.4%); 20.7% (57/276) over all git challenges; git refuted <=14 vs 21 claimed", "agrees": true,
  "note": "Independently harvested swarm-challenge blocks from all 736 remote branches give ~29% time-matched survival, matching the recorded 29.5% and its finding that git cannot reproduce claim 207's 17%; the 10/10 evidence-audit half was not re-tested and the harvester DB was not accessible."}
```
