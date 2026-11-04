# Challenge 50: "LAWENTRY allometry-huxley dispatched"

**Verdict: SURVIVED.** This is a claim about the work's status, not a physical result. The git
record confirms it. The dispatched entry was written, committed, pushed, and it passes the
repo's own gate. It is **not merged** to `main`.

## What the claim is

The author (session `session_01QbcBRauLUrSgpVGSVRjvc7`) claims that the task to write the Huxley
allometry law-library entry was dispatched. The claim gives no value ("n/a"), and its evidence level
is recorded as `unknown`. Only the record can falsify a status claim: does the dispatched work exist?

## What I checked (2026-11-04)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | `list_events` on the source session | **could-not-access**: "the requested resource was not found" | — |
| Dispatched work exists | `git fetch origin`, `git branch -r` | Branch `origin/claude/allometry-huxley-law-cac07u`, commit `35f84eb2` "Law library: Huxley allometry y = a x^b…", dated 2026-11-04 08:09 UTC. Its `Claude-Session` trailer names the **same** source session. | observation (git record) |
| Files the commit adds | `git show --stat 35f84eb2` | `library/laws/allometry-huxley.yaml` (+200), `library/pages/allometry-huxley.md` (+128), `library/pages/index.md` (+1) | observation |
| Entry passes the repo's own gate | ran `library/tools/check_laws.py` in a worktree of that branch | `ok allometry-huxley.yaml … 3 entries, 0 problems` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor 35f84eb2 origin/main`; `git branch -r --contains` | **NOT merged**. Only `origin/claude/allometry-huxley-law-cac07u` contains it. | observation |
| `main` working tree | `grep -ri allometr`, `grep -ri lawentry` | No `library/` hits. Scope: this checkout of `main` at `3272d3e`. | negative, scoped |

## Adversarial points

1. **Arithmetic, redone independently.** The claim itself contains no arithmetic. I recomputed the
   entry's derived numbers in Python, starting from the inputs the entry states:
   (10^3)^(3/4 − 2/3) = **1.7783**. 0.675 / 0.9 = **0.75**. exp(0.3²/2) = **1.0460**, and
   1 − 1/1.0460 = **4.40 %**. exp(0.6²/2) = **1.1972**. All of them match the entry. All of them
   are *calculated*, not observed.
2. **Proxy.** "Dispatched" stands in for the quantity that matters: whether a usable entry is in
   the library that readers see. Measured directly, the entry exists and passes the gate, but it is
   not on `main`. The site build and any agent reading `main` cannot see it yet. The claim does not
   say the entry was merged, so this gap does not refute it.
3. **Hidden assumption.** The claim assumes the dispatched task produced output. I relaxed that
   assumption: the task could have been dispatched and then failed or stalled. I tested this against
   git. The output exists, so the assumption holds.
4. **Evidence level.** `unknown` is under-specified, but it overstates nothing. The correct level is
   "operational record, verified from git". *My inference:* status claims should be recorded at
   that level. I also found an evidence-level defect **inside the entry**, outside the scope of this
   claim. Worked example 1 has `value: 1.778` with `evidence: literature`. 1.778 is computed from
   the two theoretical exponents, so it is `derived`. The entry's own note says "CALCULATED, not
   observed", so the prose is honest and only the field is mislabeled. The literature values in
   that example (0.69, 0.68, 0.65) are not the `value`.
5. **Counter-examples / regimes.** The status claim has no counter-example. On content, the entry
   already lists the main ones I would raise: curvature (Kolokotrones 2010), threshold allometry
   (*Onthophagus*), the OLS-vs-SMA method gap, the error-model dispute (Packard vs
   Kerkhoff & Enquist) and phylogenetic non-independence. I did not search the literature
   independently for this challenge. I read no new papers, so I add no new citations.

## Sources

- Git history of `kganjam/delphi-frontier`, branches as fetched on 2026-11-04. Read level: full-text.
- `library/laws/allometry-huxley.yaml` on `origin/claude/allometry-huxley-law-cac07u`. Read level: full-text.
- Source session transcript. Read level: could-not-access.

```swarm-challenge
{"claim_id": 50, "outcome": "survived", "reason": "Git shows commit 35f84eb2 from the same source session adding library/laws/allometry-huxley.yaml, which passes check_laws.py; the work was dispatched and completed but is not yet merged to main (minor in-entry defect: worked example 1's derived 1.778 is tagged evidence: literature).", "corrected_value": null}
```
