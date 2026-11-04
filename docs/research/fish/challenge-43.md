# Challenge 43: "LAWENTRY cost-of-transport dispatched"

**Verdict: SURVIVED.** This is a claim about the status of a piece of work. It is not a physical
result. Git confirms it: the dispatched entry was written, committed and pushed, and it passes
the repository's own gate. The entry has **not** been merged into `main`.

Source session: `session_016kCs8GSSjg9u5WmxYuCFgb`. Recorded evidence level: `unknown`. Value: n/a.

## What I checked (2026-11-04, about 08:10 to 08:20 UTC)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | `list_events` on the source session | **could-not-access**: "the requested resource was not found". The session also does not appear in the first 100 rows of `list_sessions`. | n/a |
| Dispatched work exists: **first pass** | `git branch -r` and a `git grep` for "cost of transport" across every remote branch, on the refs fetched at the start of this session | **Nothing found**. The only hit was the earlier catalogue `docs/research/library/biological-design-laws.md` §4.7 on `origin/claude/biological-design-laws-eh115j` (commit `aac0950b`, from a different session). No `library/laws/cost-of-transport.yaml` existed on any branch. | negative result, limited to the refs fetched at that moment |
| Dispatched work exists: **second pass** | `git fetch origin`, then the same checks again | Branch `origin/claude/cost-of-transport-6z04zs`, commit `1f91630c`, "Law library: cost of transport vs body mass across swimming, flying, running", dated **2026-11-04 08:11:57 UTC**. Its `Claude-Session` trailer names the **same** source session, `session_016kCs8GSSjg9u5WmxYuCFgb`. | observation (git record) |
| Files the commit adds | `git show --stat 1f91630c` | `library/laws/cost-of-transport.yaml` (+242). Nothing else. | observation |
| Entry passes the repository's gate | Ran `library/tools/check_laws.py` in a worktree of that branch | `ok cost-of-transport.yaml … 3 entries, 0 problems` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor origin/claude/cost-of-transport-6z04zs origin/main` | **NOT merged** | observation |

The first-pass negative mattered. Had I stopped there, I would have scored the claim as
refuted. The commit landed about 3 minutes after this challenge session was created
(08:08:29 UTC). A dispatch claim checked moments after dispatch can therefore look false. My
inference: the swarm should check dispatch claims only after the dispatched worker has had time
to finish, or re-fetch before recording a verdict.

## Adversarial points

### 1. Arithmetic, redone independently

The claim itself contains no arithmetic. I recomputed every derived number in the entry it
refers to, in Python, from the inputs the entry states. All of these are **calculations**, not
observations.

| Entry's number | My recomputation | Agrees? |
|---|---|---|
| 0.533 × 20.1 = 10.71 J kg⁻¹ m⁻¹; 0.300 × 20.1 = 6.03 W kg⁻¹ | 10.713; 6.030 | yes |
| Fish mass-specific exponent α − 1 = −0.20, CI (−0.31, −0.08), from α = 0.80 (0.69, 0.92) | −0.20, (−0.31, −0.08); the model's 0.72 gives −0.28 | yes |
| Flight exponent 0.83 − 1 − 0.14 = −0.31 (−0.35 with a speed exponent of 0.18) | −0.31; −0.35. COT = P/(M·v), so the mass-specific exponent is p − 1 − s. The derivation is correct. | yes |
| Duck: 5.77 kcal kg⁻¹ km⁻¹ = 24.1 J kg⁻¹ m⁻¹, "about twice" 10.7 | 24.14; ratio 2.26 | yes |
| Mouse (0.02 kg) vs human (70 kg): (0.02/70)^−0.316 = 13.2 | 13.18. With 0.03 kg I get 11.6, which matches Kram's "approximately 12 times". This supports the entry's statement that the gap comes from the choice of masses. | yes |
| Ant: 158 J kg⁻¹ m⁻¹ lies on the running line at a mass of 0.20 g | (158/10.7)^(−1/0.316) = 1.99 × 10⁻⁴ kg | yes |
| Danio (assumed 4 × 10⁻⁴ kg): running line gives 127 | 126.8 | yes |
| Danio relative to a 1.2 kg fish: 5.0×, interval 1.9× to 12.0× | 4.96×; 1.90× to 11.96× | yes |
| 4 × 10⁻⁴ kg is "about 20 times below" the smallest fish in the fit (8.3 × 10⁻³ kg) | 20.75× | yes |

I found no arithmetic error.

### 2. Proxy

"Dispatched" stands in for the quantity that matters, which is whether a usable
cost-of-transport entry is in the library. Measured directly, the entry exists and passes the
gate, but it is **not on `main`**. Anything that reads the library from `main` (the site build,
other agents) does not see it yet. The claim does not say the entry was merged, so this does not
refute it. It is the gap a reader is most likely to fill in wrongly.

A proxy is also at work inside the entry. The author named this one, and I have not caught them
out. The fish exponent comes from Hein & Keirsted's **gross, whole-animal minimum** COT. The
running line is **net**. Comparing the two across modes is a proxy comparison. The entry flags
this in the `E_net` symbol description and in failure (2). For this repository's zebrafish
question, the quantity that matters is the COT of a fish of about 0.4 g at its operating speed.
The entry correctly gives that as `unknown`, because the Hein & Keirsted prefactor could not be
read.

### 3. Hidden assumption

The claim assumes the dispatched task produced output. I relaxed that assumption: the task might
have been dispatched and then failed, or failed to push. I then tested it against git. On the
first fetch the assumption looked false. On the second fetch it held. So the claim's truth
depends on **when** it is checked. That makes it weaker than a claim checked after completion,
but it does not make it false.

### 4. Is the evidence level honest?

`unknown` is under-specified, but it is not dishonest, because nothing is overstated. The
accurate level is "operational record, verified from git (commit `1f91630c`)". Inside the entry,
the evidence labels I checked are honest:

- The Danio numbers are marked `derived` and say "Calculated, not observed".
- The flight exponent says "MY INFERENCE, calculated rather than measured".
- The Taylor coefficients state that they came from a search summary.

One small point: the duck worked example is labelled `evidence: literature`. It is a unit
conversion of a value the author read only at search-summary level. The note says so, so I do not
count it as a defect.

### 5. Regime or counter-example the author missed

- **A disagreement between sources, preserved here rather than resolved.** The new entry gives
  the domain of the Taylor 1982 running line as **15 g to 254 kg**, citing the full text of Kram
  2012. The earlier catalogue (`aac0950b`, §4.7) gives it as **"about 0.01–250 kg"** and marks
  that as remembered. The new figure has the higher read-level. I did not read Taylor 1982
  myself.
- **Net versus gross in the ant comparison** (my inference). Failure (6) places Lighton et al.'s
  158 J kg⁻¹ m⁻¹ against the **net** running line. The entry does not say whether the 158 is net
  or gross. If it is gross, the ant sits higher relative to a net line than the entry implies.
  The entry already says it lacks the ant's mass and treats the point as disputed, so this
  sharpens the entry rather than refuting it. I did not read Lighton et al. (could-not-access:
  not attempted), and I give no ant mass.
- **Searched for, not found as omissions:** the regimes I would raise (surface vs submerged
  swimming, endothermy and net vs total cost, the temperature dependence in fish, the low-Re
  cut-off, gait mixing, the mismatch between mechanical and metabolic COT) are all already in
  `where_it_breaks`. The entry also states its own unsearched regimes: bats, jet propulsion,
  insect flight regressions.

I found no counter-example to the status claim.

## Sources

- Git history of `kganjam/delphi-frontier`, branches as fetched on 2026-11-04 (two fetches).
  Read-level: full-text.
- `library/laws/cost-of-transport.yaml` on `origin/claude/cost-of-transport-6z04zs` (`1f91630c`).
  Read-level: full-text.
- `docs/research/library/biological-design-laws.md` §4.7 on
  `origin/claude/biological-design-laws-eh115j` (`aac0950b`). Read-level: full-text.
- Source session transcript. Read-level: could-not-access.
- The literature the entry cites (Taylor 1982, Kram 2012, Alexander 2005, Hein & Keirsted 2012,
  Williams 1999, Prange & Schmidt-Nielsen 1970, Lighton 1993 and others). Read-level:
  could-not-access by me, because I attempted no fetch. I checked the entry's arithmetic and
  internal consistency, not its quotations.

```swarm-challenge
{"claim_id": 43, "outcome": "survived", "reason": "Git shows commit 1f91630c from the same source session adding library/laws/cost-of-transport.yaml, which passes check_laws.py and whose derived numbers I reproduced; the entry is not yet merged to main, and it only appeared on a second fetch.", "corrected_value": null}
```
