# Challenge 41 — "LAWENTRY kleiber dispatched"

Adversarial review of claim 41 (source session `session_01Hsfzfw15QmUJiFdb6V8mh8`;
recorded evidence level `unknown`, value `n/a`). This review did not write the claim.

## What kind of claim this is

The claim is about **process**, not biology. It says that a law-library task for Kleiber's law
(a `LAWENTRY`) was handed to a worker. It has no number. Breaking it means showing that the task
was never sent, or that nothing came of it. I did not read the source session's transcript. I
tested the claim against the repository.

## What I checked (my observations, from `git` in this container on 2026-11-04)

| Check | Result | Evidence level |
|---|---|---|
| Does a Kleiber law entry exist anywhere in the repo history? | Yes. Commit `b2b7cae3` is titled "Add Kleiber's law entry, with the 2/3 vs 3/4 controversy left unreconciled" and adds `library/laws/kleiber.yaml`, `library/pages/kleiber.md`, and edits `library/pages/index.md` and `docs/architecture/the-law-library.md`. | observed (git object) |
| Which branch is it on? | Only `origin/claude/kleiber-law-entry-ickbi0` (found with `git branch -r --contains b2b7cae3`). | observed |
| Is it on `main`? | No. `origin/main` is at `43cb06c1`, which does not contain `b2b7cae3`. | observed |
| Was it a real worker, not a stub? | The branch was cut from the law-library base commit `343e8f15`, the same base as five sibling law branches (`hagen-poiseuille`, `strouhal`, `wing-loading`, `second-moment`, `elastic-similarity`). That fits a fan-out dispatch. | observed (branch topology); "fan-out dispatch" is **my inference** |
| Does the entry pass the repo's own gate? | `python3 library/tools/check_laws.py` run on that branch printed `ok kleiber.yaml … 3 entries, 0 problems`. `--selftest` passed. | observed (I ran it) |

## Independent arithmetic on the delivered entry

I redid the entry's worked examples from their stated inputs. I did not copy the author's
working. All of these values are **calculated**, not observed.

- 70 kcal/day × 4184 J/kcal ÷ 86400 s/day = **3.390 W**. This matches the entry's 3.39 W.
- 70^0.75 = 24.20. Then 3.390 W × 24.20 = **82.0 W**, which is 1694 kcal/day. This matches the entry (82 W, 1694 kcal/day).
- Mass ratio 4000 / 0.02 = 2.0 × 10^5. Raised to the 3/4 power it gives **9457**; raised to the 2/3 power it gives **3420**. The ratio of the two is (2.0 × 10^5)^(1/12) = **2.765**, which matches the entry's "2.77, ~2.8".
- 10^3 raised to the 1/12 power is **1.778**, and 10^6 raised to the 1/12 power is **3.162**. Both match the entry (1.78 and 3.16).

None of the arithmetic breaks.

## The five probes

1. **Arithmetic.** I redid it above, and all of it matches. The claim itself has no arithmetic.
2. **Proxy.** "Dispatched" could stand in for the thing that matters, which is "a correct,
   admissible entry was delivered". Here the proxy *understates* the result. The entry exists
   and passes the dimension gate. It is not merged to `main`, so "in the canonical library" would
   be an overclaim. The claim does not make that overclaim.
3. **Hidden assumption.** The claim assumes that the `ickbi0` branch is the output of *this*
   dispatch and not of some other one. I cannot tie the branch to session
   `01Hsfzfw15QmUJiFdb6V8mh8` from the repo alone, because commits carry no session trailer that I
   checked. Even with that link dropped, a Kleiber LAWENTRY was dispatched *by someone* and was
   delivered, so the claim's content still holds.
4. **Evidence level.** `unknown` is honest but too weak. The claim could carry an *observed*
   level with a pointer (commit `b2b7cae3`, branch `claude/kleiber-law-entry-ickbi0`). This is a
   bookkeeping defect, not a falsehood. No derived number is presented as measured, because
   there is no number.
5. **Counter-example.** For the claim to fail, the entry would have to be missing, or the gate
   would have to reject it. I found neither. Scope of that negative search: all remote branches
   fetched into this container on 2026-11-04 (`git log --all --grep=kleiber`, `git grep -i
   kleiber` over the 200 most recent revisions), plus one run of `check_laws.py` on the delivering
   branch. I did not check the scientific content of the entry's sources (White & Seymour 2003,
   DeLong 2010, Kolokotrones 2010 and others) against the papers. Read-level for all of them in
   this review: **could-not-access** (not attempted). The entry's own read-levels are its
   author's claims.

## Verdict: SURVIVED

The dispatch happened, and it produced a delivered entry that passes the gate (observed). The
worked-example arithmetic reproduces to three significant figures (calculated). The only faults
are both minor and neither falsifies the claim:

- The evidence level `unknown` should have been `observed`, with a commit pointer.
- "Dispatched" undersells the status. The accurate status is "delivered on branch, not merged to `main`".

```swarm-challenge
{"claim_id": 41, "outcome": "survived", "reason": "Commit b2b7cae3 on origin/claude/kleiber-law-entry-ickbi0 delivers library/laws/kleiber.yaml, which passes check_laws.py and whose worked-example arithmetic reproduces independently; the entry is not yet on main and the claim's evidence level should be observed, not unknown.", "corrected_value": null}
```
