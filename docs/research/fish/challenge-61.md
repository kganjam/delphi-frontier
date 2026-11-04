# Challenge 61: "LAWENTRY bone-safety-factor dispatched"

**Verdict: SURVIVED, with two caveats.** The claim reports the status of a piece of work. It does not
assert a biological or physical result. The git record and the source session's own final report
both confirm it: the task was dispatched, and the entry was written, committed and pushed. Two facts
limit what a reader should infer from that. First, the entry is **not merged** to `main`. Second, on
its own branch the library's page-build check **fails** (`build_pages.py --check` exits 1), because
the generated page and the index row were never committed. The claim says neither "merged" nor
"rendered", so neither fact refutes it.

## What the claim is

The author (session `session_016kCs8GbdQ2HnFbeuVwAwjn`) claims that the task to write the
`bone-safety-factor` law-library entry was dispatched. The claim gives no value ("n/a"), and its
evidence level is recorded as `unknown`. Because the claim is about status, only the record can
falsify it.

## What I checked (2026-11-04)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session's final result | `list_events` (kind `result`) on the source session | One `success` result at 2026-11-04 08:20 UTC. It reports writing `library/laws/bone-safety-factor.yaml`, pushing commit `9938234b` to `claude/bone-safety-factor-022j5s`, and choosing not to commit generated pages. | observation (session record; read level: full-text of the result event only, not the whole transcript) |
| Dispatched work exists | `git branch -r --contains 9938234b` | Commit `9938234b`, "Add bone safety factor law entry: the 2-4 band holds only for mammal and bird limb bones". It is on `origin/claude/bone-safety-factor-022j5s` only, and its `Claude-Session` trailer names the **same** source session. | observation (git record) |
| Files the commit adds | `git show --stat` | `library/laws/bone-safety-factor.yaml` (+290) and **nothing else**. | observation |
| Dimension gate | ran `library/tools/check_laws.py` on a worktree of that branch | `ok bone-safety-factor.yaml … 3 entries, 0 problems` | observation (tool output) |
| Author's negative-control claim | changed `sigma_fail / sigma_peak` to `sigma_fail * sigma_peak` and re-ran the gate | Rejected: "'SF' is dimensionless, other side is M^2·L^-2·T^-4". This matches the commit message. | observation (tool output) |
| Page build | `library/tools/build_pages.py --check` on the same branch | **exit 1**: `{"stale": ['bone-safety-factor.md', 'index.md']}` | observation (tool output) |
| Rendered page anywhere | `git ls-tree` for `pages/bone-safety*` on every remote branch | None found | negative, scoped to remote branches as fetched today |
| Merged? | `git merge-base --is-ancestor 9938234b origin/main` | **NOT merged**. The base the entry needs (`reynolds.yaml`, `murray.yaml`, `check_laws.py`) is not on `main` either, and the author says so. | observation |

## Adversarial points

1. **Arithmetic, redone independently.** The claim contains no arithmetic. I recomputed every
   derived number in the entry from the inputs it states.
   - 157.1 / 14.9 = **10.54**, which rounds to the published 10.5. 157.1 / 18.9 = **8.31**. The entry gives 10.5 and 8.3. Correct.
   - 3 × 47.7 = **143.1 MPa**. The entry gives 143. Correct.
   - 3.5 / 1.9 = **1.842**. The entry gives 1.84. Correct.
   - Horse metacarpal: 37.7 / 4.0 = **9.4** and 68.9 / 5.7 = **12.1**. The entry gives "~9-12x". Correct.
   - Turtle femur: 13.9 / 6.9 = **2.0** and 13.9 / 4.4 = **3.2**. The entry gives "about 2-3x". Correct, though the upper end is slightly over 3.
   - 1/0.5 = 2 and 1/0.25 = 4, for the 25–50% to SF 2–4 conversion. Correct.

   All of these are *calculated*. The entry labels each one `evidence: derived` or "our arithmetic".
   That labelling is honest.
2. **Proxy.** "Dispatched" stands in for the quantity that matters, which is whether a usable,
   rendered law entry now exists in the library. Measured directly, the answer is partial. The YAML
   exists and passes the dimension gate. It is not on `main`, and its page exists on no branch. The
   author's report says "the page build ran cleanly". My inference: that means the build *ran*, not
   that the committed tree is current, because `--check` on the pushed branch reports the page as
   stale. The author's stated reason, that sibling law-entry branches commit only the YAML, is a
   process choice and not an error. The challenge-45 Hagen-Poiseuille entry ended in the same state.
3. **Hidden assumption.** The claim assumes the dispatched task produced output. I relaxed that
   assumption (dispatched, then failed or abandoned) and tested it against git and the session's
   result event (`is_error: false`, `terminal_reason: completed`). The output exists, so the
   assumption holds.
4. **Evidence level.** `unknown` is under-specified, but nothing is overstated. The accurate level is
   "operational record, verified from git, tool output and the source session's result event".
5. **Counter-examples.** I found none to the status claim. The entry's content is outside this
   claim's scope. I found no numerical error in it. The entry already flags its weak points: every
   source is at search-summary level or below, Biewener 1989 is cited from memory and marked
   `could-not-access`, the 2–4 versus 3–5 mammal bands are left unreconciled, and no teleost SF was
   found. I did no literature fetches in this review. So I have **not** independently verified any
   reported SF value (for example Blob & Biewener 1999, 5.5–10.8, or Skedros et al. 2003, 4.0–68.9).
   For this review their read level is `could-not-access` because I did not try to fetch them. I
   leave the author's stated read levels as recorded.

## Sources

- Git history of `kganjam/delphi-frontier`, remote branches as fetched on 2026-11-04. Read level: full-text.
- `library/laws/bone-safety-factor.yaml`, `library/tools/check_laws.py`, `library/tools/build_pages.py` on `origin/claude/bone-safety-factor-022j5s`. Read level: full-text.
- Source session `session_016kCs8GbdQ2HnFbeuVwAwjn`, final `result` event. Read level: full-text of that event; rest of transcript not read.
- `docs/research/fish/challenge-45.md` on `origin/claude/challenge-45-lawentry-kims5u` (format and precedent). Read level: full-text.
- Literature cited inside the entry. Read level: could-not-access (not attempted in this review).

```swarm-challenge
{"claim_id": 61, "outcome": "survived", "reason": "Commit 9938234b from the same source session adds library/laws/bone-safety-factor.yaml, which passes check_laws.py (a sigma-multiplied mutant is rejected) and the session's result event reports success, so the dispatch produced the entry; it is unmerged and its generated page was never committed (build_pages.py --check exits 1 on that branch).", "corrected_value": null,
  "depends_on": ["git commit 9938234b on origin/claude/bone-safety-factor-022j5s", "check_laws.py output on that branch", "build_pages.py --check output on that branch", "source session result event 2026-11-04T08:20Z", "git merge-base check against origin/main 43cb06c1"]}
```
