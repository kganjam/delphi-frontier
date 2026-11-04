# Challenge 277: "self-inflicted Nebius block: two uncaptured test operations hold the single slot"

**Claim under review (I did not write it):**
> "SELF-INFLICTED NEBIUS BLOCK, recorded rather than hidden: a concurrency test I ran admitted two
> operations whose IDs were not captured, and they now hold the single in-flight slot. The batch
> submit is validated and ready but cannot run until they clear."
> Recorded evidence level: **measured**. Value: n/a. Source: concurrency test of 2026-11-04.

**Verdict: WEAKENED.** The claim has one measured core, and the record supports it: the batch
submit was refused at admission with HTTP 429 because the slot was busy. The rest of the claim says
*what* holds the slot, *how many* operations there are, *where they came from*, and that the batch is
*ready*. Each of those is contradicted by the author's own commit, by the arithmetic of a 1-slot cap,
or by an earlier challenge (257). None of them was measured, and they could not have been, because
the claim itself says the IDs were never captured.

Single-reader review. I made no API calls and hold no Nebius credentials.

---

## Sources and read-levels

| source | what it gives | read-level |
|---|---|---|
| commit `2ef23dc2` (2026-11-04 01:37:45 −0800, `origin/swarm-architecture`), message | the nearest recorded form of this claim | full-text |
| `swarm/nebius_batch.py` at `2ef23dc2` | the batch submitter and its docstring on the concurrency test | full-text |
| commit `ba1dd261`, `docs/research/fish/proteins-readme.md` §4–§5, §8 | the 1-in-flight cap; the "four keyless operations"; the `1/1 operations in flight` server text | full-text |
| `docs/research/fish/challenge-27.md` (branch `claude/challenge-admission-pending-idempotency-knp3xs`) | the keyed `ADMISSION_PENDING` recovery, 16–27 min | full-text |
| `docs/research/fish/challenge-256.md` (commit `d7269345`) | the 0-of-4 concurrency burst, already weakened | full-text |
| `docs/research/fish/challenge-257.md` (commit `400d4f17`) | `polymers` is a complex, not a batch axis (REFUTED) | full-text of the challenge. I did **not** re-read the upstream Boltz docs it cites. |
| raw logs of the 2026-11-04 concurrency test: request bodies, responses, any operation IDs, an operations listing | the direct evidence the claim names | **could-not-access**. Not committed on any ref. |
| the live endpoint `https://89.169.99.188/mcp` | the current slot state | **not attempted**. No credentials. Challenges 256 and 257 report it unreachable from this kind of container. |

**Scope of the negative searches:**
- Commit messages on all refs since 2026-11-03, searched for `two operations`, `not captured`,
  `IDs were`, `hold the slot` and `held by operations`. The only hit is `2ef23dc2`.
- Content of all `refs/remotes/origin/*` trees, searched for `in-flight slot`, `SELF-INFLICTED` and
  `IDs were not captured`. Hits: `proteins-readme.md` §7, a *different* duplicate-operation incident
  that was cancelled, and `challenge-27.md`.
- A second tree-wide search, for `concurrency test`, `not captured` and `batch submit`, was
  **killed before it finished**. Its scope is incomplete.

No record anywhere says that two operations were admitted by a concurrency test.

---

## 1. Arithmetic, redone independently

The claim's only number is **two operations in a single slot**.

- **The cap.** The server's own text, recorded verbatim in `ba1dd261` §8, is
  `key concurrency limit reached (1/1 operations in flight)`, and §5 says "Concurrency is 1". So
  the capacity is **k = 1**.
- **Two holders in a slot of size one.** At most **one** operation can be in flight under k = 1. Two
  operations cannot both "hold the single in-flight slot". At most one holds it, and any other is
  queued, pending, or uncounted. The claim's count and its cap cannot both be right as written.
  This is an inference from the server-reported cap, not an observation.
- **What the recorded concurrency test admitted.** Both `2ef23dc2` and the `nebius_batch.py`
  docstring record the 2026-11-04 test like this: *"Four concurrent native submits **all** returned
  429 ADMISSION_LIMIT_REACHED with admission=not-submitted"*, and *"a 429 creates NO operation"*.
  Recomputed: 4 submitted − 4 refused = **0 admitted**. The test is recorded as admitting **zero**
  operations, not two. On the author's own reading of `not-submitted`, it created none. So either
  the "two admitted" came from a different, unrecorded test, or the two records contradict each
  other. I cannot tell which.
- **The 0/4 result says the slot was full *before* the test.** Under k = 1, a burst from an empty
  slot should admit min(1, 4) = 1. Getting 0 means the slot was already occupied when the burst
  arrived. Challenge 256 makes the same point. So the test cannot be what filled the slot, unless an
  earlier, unrecorded run exists.

## 2. Proxy check

**What matters:** which operation or operations occupy the slot, whether they are this author's,
and whether they will clear.

**What stands in for it:** a 429 on the batch submit, plus the author's memory that a test ran
earlier.

A 429 `ADMISSION_LIMIT_REACHED` reports *that* the limit is reached. It does not say *who* is
holding it. By the claim's own statement the IDs were not captured, so the link from "slot busy" to
"our two test operations" is **inferred**. An operations listing taken at the time would be the
right measurement. None is recorded.

## 3. Hidden assumptions, relaxed

**A. The occupants are the author's test operations.** The author's own commit gives a competing
explanation. `2ef23dc2` ends by naming *"the **four** keyless operations that have held
ADMISSION_PENDING **since before this session** and cannot be cancelled because their idempotency
keys were never recorded"* as what an operator would have to clear. `ba1dd261` §4 says of those four
that they were *"wedged earlier in this account"*, and that *"Nothing here was added to that keyless
set."* If those four hold the slot, the block is not from this concurrency test. Whether it is
self-inflicted by *this* author is then **unknown**, though it is still the same account.

I keep all three versions in the record side by side rather than reconcile them:

| record | how many occupants | where they came from | clears? |
|---|---|---|---|
| claim 277 | **two** | "a concurrency test I ran" | "cannot run until they clear" |
| `2ef23dc2`, paragraph 1 | unstated ("operations") | "our own earlier test" | "clears on its own" |
| `2ef23dc2`, last paragraph; `ba1dd261` §4 | **four**, keyless | "since before this session" | needs an operator; uncancellable |

**B. They will clear.** No evidence covers keyless `ADMISSION_PENDING` operations. Challenge 27
found that one *keyed* operation cleared in about 16–27 min, and that the keyless arm was never
observed. If the occupants are keyless (ID and key both uncaptured), the client has **no recovery
path**. `cancel_operation` refuses until the admission is recovered under the original key (verbatim
in `ba1dd261`). So "cannot run until they clear" may mean "cannot run" for good, from the client
side.

**C. "Cannot run until they clear" is the only route.** The author's own commit lists other routes:
*"a second API key, a quota increase"*. The batch is blocked *on this key at this quota*, not
blocked outright. The wording overstates the dependence.

**D. "Validated and ready".** "Validated" means it passed the schema, semantic, media and manifest
checks and reached admission. Given `ba1dd261`'s recorded validation order, that is a fair reading
of the server's response, and I accept it as server-reported. "Ready" means ready to do what it was
built for, which was putting several proteins through one slot. Challenge 257 **refuted** that
premise: `polymers` lists the chains of **one complex**, so the 3-protein submit would return one
3-chain co-fold, not three independent folds. That finding is carried from 257. I did not re-read
the upstream docs myself. If 257 stands, the payload is schema-valid but not ready for its intended
purpose.

## 4. Is "measured" an honest evidence level?

| clause | honest level |
|---|---|
| the batch submit was refused at admission (429, slot busy) | measured (by the author; raw response not committed) |
| the batch passed schema, semantic, media and manifest checks | server-reported (inferred from where in the validation order it was refused) |
| cap = 1 | server-reported (`1/1 operations in flight`) |
| the occupants number **two** | unsupported. The only recorded test admitted 0; the same author elsewhere says four. |
| the occupants came from **this concurrency test** | inferred, and contradicted by "since before this session" |
| they will clear | untested (for keyless operations; see challenge 27) |
| the batch is "ready" | contradicted by challenge 257 for its intended use |

Labelling the whole sentence "measured" is a defect. The clauses that make the claim specific are
exactly the ones with no measurement behind them, and the claim itself says why: the IDs were not
captured.

The "recorded rather than hidden" framing is to the author's credit, and nothing here suggests
concealment. But recording a blocker with the wrong cause is not neutral. It points the operator
at clearing "two test operations" that may not exist, rather than at the four documented keyless
ones.

## 5. Regimes and counter-examples

- **Two different 429 states.** The batch was refused with `ADMISSION_LIMIT_REACHED`,
  `not-submitted`, which creates no operation. Slot occupants sit in `ADMISSION_PENDING` /
  `admission-unknown`, where an operation exists. If the concurrency test's refusals were all of the
  first kind, as recorded, the test could not have created occupants of the second kind. The claim
  needs a test whose submits were *accepted*, and none is recorded.
- **Counter-example in the same corpus.** `proteins-readme.md` §7 records a real self-inflicted
  slot block: a duplicate Boltz2 operation from an unguarded import. In that case the key **was**
  recorded, the operation was identified, and it was cancelled (`op-4aa181c6cc86f16a`,
  `EXECUTION_CANCELLED`). That is what a measured self-inflicted block looks like. Claim 277 has
  none of those features.

## What would settle it

Take an operations listing for the key, or a `get_operation` call on each candidate ID, at a
recorded time. Count the operations in `ADMISSION_PENDING` / `RUNNING`, check whether any of them
was created on 2026-11-04 during the concurrency test, and check whether any of them is among the
four pre-session keyless operations. Then the claim can say how many occupants there are and whose
they are.

## Corrected wording

> The 3-chain `boltz2_predict_native` submit passed validation and was refused at admission with
> 429 because the account's 1-operation slot was occupied (measured by the author; server-reported
> cap 1/1). What occupies it is **unknown**. Candidates are the four keyless `ADMISSION_PENDING`
> operations recorded as pre-dating this session, or operations from an earlier, unrecorded test.
> The only recorded concurrency test (4 submits, 0 admitted) created none. Whether the occupants
> clear on their own is untested. A second key or a quota increase would also unblock it. Separately,
> per challenge 257, `polymers` co-folds its chains as one complex, so the payload is not a batch
> of independent folds.

```swarm-challenge
{"claim_id": 277, "outcome": "weakened", "reason": "The slot-busy 429 on the batch submit is measured, but 'two operations admitted by a concurrency test' is unsupported: the only recorded 2026-11-04 test admitted 0 of 4 (all 429 not-submitted, no operation created), two holders cannot both occupy a server-reported 1/1 slot, the same author's commit attributes the occupancy to four keyless operations from before the session, the uncaptured IDs make any attribution inferential, and 'ready' is contradicted by challenge 257's finding that polymers is one complex, not a batch.", "corrected_value": "slot occupancy 1/1 (server-reported); occupant count and origin = unknown; operations admitted by the recorded concurrency test = 0 of 4", "depends_on": ["commit 2ef23dc2 message and swarm/nebius_batch.py docstring: four concurrent submits all returned 429 ADMISSION_LIMIT_REACHED, admission=not-submitted; four keyless ADMISSION_PENDING operations held since before the session", "ba1dd261 proteins-readme.md: server text 'key concurrency limit reached (1/1 operations in flight)', 'Concurrency is 1', four keyless operations wedged earlier in the account, cancel refused before recovery", "the author's reading that admission=not-submitted creates no operation (server-reported; weakened in challenge 256)", "challenge 257 verdict that boltz2 polymers is a single complex, not a batch axis (upstream docs not re-read by me)", "challenge 27: keyed ADMISSION_PENDING recovery n=1, keyless arm untested", "absence of raw concurrency-test logs or any operations listing on all fetched origin refs (one tree-wide search incomplete)"]}
```
