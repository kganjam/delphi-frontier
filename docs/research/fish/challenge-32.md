# Challenge 32: "LAWENTRY strouhal dispatched"

**Verdict: SURVIVED.** The claim is a statement about the work's status, not a physical result.
The record in git confirms it, and it understates what happened: the entry was dispatched,
written, committed and pushed. It has not been merged.

## What the claim is

The author (session `session_01EeoYQc1a6j7Ge7Do6Kmwjq`) claims that a task to write the
Strouhal law-library entry was dispatched. The claim gives no number ("value: n/a"), and its
evidence level is recorded as `unknown`. Because the claim is about status, the only thing
that can falsify it is the record: did the dispatched work exist?

## What I checked (on 2026-11-04)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | `list_events` on the source session | **could-not-access**: "requested resource was not found" | — |
| Dispatched work exists | `git branch -r`, `git grep strouhal` across remote branches | Branch `origin/claude/strouhal-law-8mv27w`, commit `7778dd5e` "Add Strouhal law entry…", dated 2026-11-04 08:01 UTC. Its `Claude-Session` trailer names the **same** source session. | observation (git record) |
| Files the commit adds | `git show --stat 7778dd5e` | `library/laws/strouhal.yaml` (+160), `library/pages/strouhal.md` (+118), `library/pages/index.md` (+1) | observation |
| Entry passes the repo's own gate | ran `library/tools/check_laws.py` on a checkout of that branch | `ok strouhal.yaml … 3 entries, 0 problems` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor … origin/main` | **NOT merged**. Only that one branch contains it. | observation |
| Local `main` | `grep -ri strouhal`, `grep -ri lawentry` in the working tree | No hits. Scope: this checkout of `main` at `3272d3e`. | negative, scoped |

## Adversarial points

1. **Arithmetic, redone independently.** The claim contains no arithmetic. I redid the two derived
   numbers in the entry it refers to: f = St·U/A = 0.3 × 2 / 0.01 = **60 Hz**, and
   Re = U·L/ν = 2 × 0.01 / 1.5e-5 = **1333.3**. Both are correct. Both are *calculated* from
   assumed inputs, and the entry labels them `evidence: derived`. That label is accurate.
2. **Proxy.** "Dispatched" stands in for the quantity that matters: whether a usable law entry now
   exists in the library. Measured directly, the answer is that the entry exists and passes the gate,
   but it is **not on `main`**. Anything that reads the library from `main` (the site build, other
   swarm agents) does not yet see the entry. The claim does not say the entry was merged, so this
   does not refute it. It is the gap a reader is most likely to fill in wrongly.
3. **Hidden assumption.** The claim assumes the dispatched task produced output. I relaxed that
   assumption (the task might have been dispatched and then failed), then tested it against git. The
   output exists, so the assumption holds.
4. **Evidence level.** `unknown` is under-specified, but it is not dishonest. Nothing is overstated.
   The correct level is "operational record, verified from git". My inference: the bookkeeping
   should record status claims at that level rather than as `unknown`.
5. **Counter-examples.** I found no counter-example to the status claim. One note about the
   *content* of the entry, outside the scope of this claim and offered as my inference only: the
   entry says a Re ~ 1e3 design "must NOT be checked against 0.2–0.4" because of observations of
   larval zebrafish swimming in *water*. The worked example it applies this to is a flapping *wing in
   air*. Taylor et al. (2003) included insects in their band, and the entry itself lists insects as
   "thin data". So carrying the low-Re failure from undulatory swimmers over to flapping wings at
   the same Re is a step the entry does not support with a citation. I did not read Taylor et al.
   (I tried no fetch). Its read level here is `could-not-access`, and I give no insect St values.

## Sources

- Git history of `kganjam/delphi-frontier`, branches as fetched 2026-11-04. Read level: full-text.
- `library/laws/strouhal.yaml` and `reynolds.yaml` on `origin/claude/strouhal-law-8mv27w`. Read level: full-text.
- Source session transcript. Read level: could-not-access.

```swarm-challenge
{"claim_id": 32, "outcome": "survived", "reason": "Git shows commit 7778dd5e from the same source session adding library/laws/strouhal.yaml, which passes check_laws.py; the work was dispatched and completed, though it is not yet merged to main.", "corrected_value": null}
```
