# Challenge 64 — "LAWENTRY adder-cell-size dispatched"

**Verdict: SURVIVED.** One note on the evidence level is below. It understates the evidence; it does not overstate it.

## What the claim says

The claim is about a process, not a number: a worker was dispatched to write the `adder-cell-size` law entry. Its recorded evidence level is `unknown` and its value is `n/a`. The source given is session `session_01QbcBRaDLAg6rKXcZc68Kbn`.

## What I checked, and how (every item below is an observation from a primary record)

| Check | Method | Result |
|---|---|---|
| Does the source session exist? | `get_session` on the session ID (read-level: full record) | Yes. Title "Adder model of cell-size homeostasis", created 2026-11-04T08:14:41Z, status bucket COMPLETED, output branch `claude/adder-cell-size-law-5baqub`. |
| Did the dispatched work produce anything? | `git ls-remote origin`, `git fetch` of that branch | The branch exists at `71ff96ca`. That commit adds `library/laws/adder-cell-size.yaml` (230 lines), and its trailer cites the same session. |
| Does the session's own summary agree? | The `post_turn_summary` in the session record | Partly. The summary says "Commit not confirmed in tail." I confirmed the commit and push independently, from the git ref above. |
| Does the delivered entry pass the repository's gate? | Ran `library/tools/check_laws.py` in a worktree checked out at `71ff96ca` | `3 entries, 0 problems`. `adder-cell-size.yaml` is `ok`. This is a measurement taken in this session. |

## Adversarial points

1. **Arithmetic.** The claim contains no arithmetic. I spot-checked the delivered entry anyway, independently; this goes beyond what claim 64 asks.
   - 1 − 0.31 = 0.69, which follows from slope(V_d on V_b) = slope(Δ on V_b) + 1, because Δ = V_d − V_b.
   - 0.69 / 2 = 0.345.
   - The halving series runs V_b = 2Δ → V_d = 3Δ → 1.5Δ → 2.5Δ → 1.25Δ → 1.125Δ.

   All of these are correct. I did not re-derive the −0.25 mother–daughter generation-time correlation. It is out of scope for this claim and remains unverified by me.
2. **Proxy.** "Dispatched" stands in for the quantity that matters, which is whether a law entry was delivered and accepted. I measured that quantity directly:
   - **Delivered: yes.** The commit was pushed and passes the dimension gate.
   - **Accepted: no, not yet.** `71ff96ca` is **not** an ancestor of `origin/work/frontier-foundation` (`3272d3e4`) as fetched here.

   So the stronger statement "the law entry is in the library" would be **false today**. The claim does not say that, and "dispatched" remains true.
3. **Hidden assumption.** The claim assumes that a dispatched session actually ran. I relaxed this by checking that the session completed and that its output is real. It holds.

   A residual oddity, not a fault: the branch carries about 1,385 commits that are not reachable from the fetched `work/frontier-foundation`. These include the commits that create the law library itself (`343e8f15`, `fc97b80d`). My clone may be shallow, so I cannot say whether the branch base differs from the stated source revision. It is recorded here as unresolved, not as a defect.
4. **Evidence level.** The recorded level is `unknown`. The correct level is **observed**: a session record plus a pushed git ref, both read directly. This understates the evidence, so it is not the honesty defect the floor targets (a derived result presented as measured). It should still be upgraded.
5. **Counter-example regime.** For a dispatch claim, the failure modes are:
   - the session never started;
   - the session failed;
   - the session ran but pushed nothing.

   None of the three applies.

## Scope of negative searches

- I searched all of `git grep` over the current checkout for "LAWENTRY", "adder" and "cell size". The only hit was "ladder" in `ledger/README.md`, so there is no prior record of this claim on the working branch.
- I did not review the scientific content of the law entry (its literature read-levels and its where_it_breaks list). That needs its own challenge.

```swarm-challenge
{"claim_id": 64, "outcome": "survived", "reason": "Session session_01QbcBRaDLAg6rKXcZc68Kbn exists, completed, and pushed commit 71ff96ca adding library/laws/adder-cell-size.yaml, which passes check_laws.py (0 problems); evidence level should read observed, and the entry is not yet merged into work/frontier-foundation.",
  "corrected_value": null,
  "depends_on": ["get_session record for session_01QbcBRaDLAg6rKXcZc68Kbn (status COMPLETED)", "origin ref claude/adder-cell-size-law-5baqub at 71ff96ca", "library/tools/check_laws.py output at 71ff96ca: 3 entries, 0 problems", "origin/work/frontier-foundation at 3272d3e4 does not contain 71ff96ca"]}
```
