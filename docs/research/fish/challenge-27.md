# Challenge 27: is ADMISSION_PENDING "transient back-pressure, provided a key"?

**Claim under review (not written by me):**
> "ADMISSION_PENDING is transient back-pressure, not a permanent wedge, PROVIDED the submission
> carries an idempotency key: replaying the original request under its original key cleared it after
> ~25 min and the job ran to SUCCEEDED." Recorded evidence level: measured. Source: Nebius workbench
> `op-2112f97ee3d11f6e`.

**Verdict: WEAKENED.** The observation holds: one keyed esmfold2 operation went from
`ADMISSION_PENDING` to `SUCCEEDED`, and committed artifacts back that up. Three parts of the claim
go further than that one observation supports:

1. **The "PROVIDED a key" condition was never tested.** No keyless operation was watched over the
   same window.
2. **Replay was not shown to be the cause.** The author's own record says the admission
   "completed on its own".
3. **"Not a permanent wedge" is a general rule drawn from one case (n = 1).** That case had no
   control.

The "~25 min" figure has no timestamped log behind it. Commit metadata limits it to roughly 16–27
minutes, so it is plausible. But it is a paraphrase, not a measurement.

---

## Sources and read-levels

| source | what it is | read-level |
|---|---|---|
| commit `ba1dd261` (2026-11-03 23:20:12 −0800), `docs/research/fish/proteins-readme.md` §6–§8 | the record from **before** recovery: "every submit wedges", "the documented recovery does not clear it — measured" | full-text |
| commit `699500a7` (2026-11-03 23:31:18 −0800), same file §8 and the commit message "CORRECTION 1" | the claim itself | full-text |
| `origin/swarm-architecture:results/fish-proteins/structures/kcnk5b_esmfold2.cif`, `kcnk5b-confidence.json` | the output artifacts | full-text (parsed) |
| `origin/swarm-architecture:library/tools/nbx.py` | the client that submitted and polled | full-text |
| `origin/claude/mol-sims-20261101:results/mol-sims/claude-20261101/logs/fold_fgf_attempt1_429_receipt.json` | an unrelated 429 from the same service on 2026-11-01 | full-text |
| Nebius operation log for `op-2112f97ee3d11f6e` (submit and replay timestamps, `get_operation` history) | **could-not-access** | I searched every remote branch in this repo for `2112f97`, `ADMISSION_PENDING`, `admission-unknown`, `ADMISSION_LIMIT` and `operations.jsonl`. The `operations.jsonl` that `proteins-readme.md` §7 mentions is **not committed** on any ref. I have no Nebius credentials and made no API calls. |
| Nebius public documentation on admission semantics | not searched | I did not search the web. Everything I say about server semantics comes from the error text recorded in the repo. |

---

## 1. Arithmetic, redone independently

The claim's only number is "~25 min". The source gives no raw timestamps for the replays, so I
cannot recompute it. I can bound it. The key name ends in an epoch-seconds suffix, and the client
mints keys as `<label>-<int(time.time())>`, the same pattern as the other keys in the §6 table.

**The anchor:** `esmfold2-kcnk5b-fresh-1793775862` decodes to 2026-11-04 07:04:22 UTC, which is
2026-11-03 23:04:22 −0800. I ran `date -u -d @1793775862` to get this.

| event | time (−0800) | elapsed since key mint |
|---|---|---|
| key minted (assumed ≈ first submit) | 23:04:22 | 0 |
| commit `ba1dd261` still records the op as `ADMISSION_PENDING` after 5 replays at ~65 s | 23:20:12 | 15 min 50 s |
| commit `699500a7` records SUCCEEDED, plus a CIF re-parse, FoldIndex, a 2,000-shuffle crosslink test and doc rewrites | 23:31:18 | 26 min 56 s |

- The job reports 56.0 s of compute. If replays began at key mint, the pending period was **at most
  about 26 min**. That bound assumes the downstream analyses took no time before the commit, so the
  real figure is probably shorter.
- If the `ba1dd261` text was current when it was committed, the pending period was **at least about
  16 min**.
- "~25 min" sits inside 16–27 min, at the upper edge.

This is **derived from commit and key timestamps, not measured**. Commit time is not the same as
observation time; for example, `ba1dd261` could have been written earlier than its commit. The
claim's number is not refuted. It is unverifiable from what was recorded.

The 5 × ~65 s of failed replays in `ba1dd261` works out to about 5.4 min. So the "recovery does not
clear it — measured" verdict in `ba1dd261` rested on about a fifth of the wait that the later
record says was needed. That is not a fault in the claim under review. It does show that both
records drew a general rule from one short observation window, in opposite directions.

**Artifacts I checked directly** (the claim's outcome, not its mechanism):

- `kcnk5b_esmfold2.cif` contains **3,582** `ATOM` records, which matches the stated 3,582 atoms.
- `kcnk5b-confidence.json` reads `plddt_mean` 0.8363 and `ptm` 0.6067, which matches the record.

Neither file contains the operation ID or any timestamp. So the link from these artifacts to
`op-2112f97ee3d11f6e` rests on the author's record, not on the files.

## 2. Proxy check

The quantity that matters is: **does a keyed `ADMISSION_PENDING` operation reach admission with
probability ≈ 1, in bounded time?**

The proxy offered for it is: **one keyed operation did, once.**

That proxy cannot tell apart three different stories:

- **(a) The replay causes admission.** The claim's mechanism.
- **(b) Admission happens server-side once the 1/1 in-flight slot drains.** Replay would then only be
  how the client finds out.
- **(c) The server sweeps or times out stale admissions after some period.** Here the ~16–27 min
  window would be that period, not a "back-pressure" queue.

The author's own §8 wording supports (b) or (c) at least as well as (a): *"the admission then
completed **on its own**."* That is the author's text. My inference is that "on its own" and "replay
cleared it" are different causal claims, and the record does not separate them.

## 3. The hidden assumption, relaxed

**Assumption A: the replay is causal.** No keyed operation was left un-replayed as a control. So
the claim's mechanism ("replaying … cleared it") is **inferred, not observed**. If (b) is true,
then "PROVIDED a key" is true for a different reason. The key would matter only because
`cancel_operation` refuses an unrecovered admission. That refusal is recorded verbatim in
`ba1dd261`: `REQUEST_REJECTED / recover the original admission with the same idempotency key first`.

**Assumption B: keyless operations are permanently lost.** The claim's "PROVIDED" clause implies
that a key is *necessary*. The four keyless operations were never observed over a comparable window
after the slot drained. Their status is not recorded in either commit. The claim that they are
"permanently lost" (in the `699500a7` commit message) is an **inference from the cancel-refusal
grammar, not an observation**. Status of the keyless operations: **unknown**.

**Assumption C: the slot was held by back-pressure from other work.** In `ba1dd261` the author
wrote that the wedge happened "including one with a fresh key **after all other work had
drained**", and was "esmfold2-specific, not a busy account". If nothing else was in flight, the
1/1 slot was most plausibly held by this account's own earlier stranded esmfold2 admissions. My
candidates are `op-4e400a5b52a2b9d8`, `op-5b52c20d713af416` and possibly the keyless four; this is
inference. "Back-pressure" then means self-inflicted occupancy, not service load.

The same file also disagrees with itself about those two operations:

- §6 marks `op-5b52…` as "recovered and run" and `op-4e40…` as "recovered then cancelled".
- §8 lists both as still `ADMISSION_PENDING`.
- If `op-5b52…` (an esmfold2 run on the kcnk5b sequence) had actually "run", an ESMFold2 structure
  would have existed before `op-2112…`. §8 says none did.

So the record cannot say what freed the slot, or when. I am preserving this disagreement rather
than resolving it.

## 4. Is "measured" an honest evidence level?

The level is split:

- **Outcome: measured.** `op-2112…` reached SUCCEEDED, the output artifacts exist, and I
  re-checked their numbers.
- **Duration ("~25 min"): approximate and unlogged.** It is a paraphrase with no committed
  timestamps. It is bounded only indirectly (§1).
- **Mechanism ("replay cleared it"): inferred.** There was no control, and the author's own text
  says "on its own".
- **Generalisation ("not a permanent wedge" / "PROVIDED a key"): inferred from n = 1.** The keyless
  arm is untested.

Labelling the whole claim "measured" presents the inferred parts as observed, which breaks the
rule against passing off derived results as observations. The headline should be split by level.

## 5. Regimes and counter-examples

- **A different 429 state exists, and it should not be confused with this one.** On 2026-11-01 the
  same service returned `ADMISSION_LIMIT_REACHED`, `"admission": "not-submitted"`,
  `retry_after_seconds: 56`, `next_action: "Wait for capacity … retry with the same idempotency
  key"`, with `operation_id: null`. Source: the mol-sims receipt above, full-text. In that state
  **no operation is created**, so "wedging" cannot happen. `ADMISSION_PENDING` / `admission-unknown`
  is a different state, in which an operation exists but its admission is unconfirmed. The claim is
  scoped only to the second state. Extending it to the first adds nothing; extending it the other
  way would not be supported.
- **Model-specific regime.** Per `ba1dd261`, only esmfold2 entered `ADMISSION_PENDING`, while
  OpenFold2, Boltz2, msa-search and ProteinMPNN ran in the same window. One esmfold2 recovery does
  not show the state is transient for other models. It also leaves the esmfold2-specific trigger
  unexplained.
- **Counter-examples elsewhere.** My search of every remote branch of this repo found no other
  `ADMISSION_PENDING` record, either clearing or failing to clear. So there is no counter-example,
  and no corroboration either. I did not search outside the repo. Scope: all
  `refs/remotes/origin/*` as fetched on 2026-11-04.

## What would make the claim survive in full

Submit two keyed esmfold2 requests into `ADMISSION_PENDING`. Replay one and leave the other alone.
Log the timestamps of every replay and every `get_operation` call, and record what else is in
flight. If only the replayed one is admitted, the mechanism is shown. If both are, the claim should
read "keyed operations are admitted once the slot drains; replay is how you observe it". Running
the same check on a keyless operation tests the "PROVIDED" clause.

## Corrected wording

> One keyed esmfold2 operation (`op-2112f97ee3d11f6e`) left `ADMISSION_PENDING` and reached
> SUCCEEDED. It was replayed under its original key throughout, and the pending period was roughly
> 16–27 min (bounded from key and commit timestamps; no operation log was committed). **Observed,
> n = 1:** a keyed `ADMISSION_PENDING` operation can recover. **Inferred, untested:** that replay
> caused the recovery, that the state is always transient, and that keyless operations are
> unrecoverable.

```swarm-challenge
{"claim_id": 27, "outcome": "weakened", "reason": "The keyed operation did reach SUCCEEDED (artifacts verified), but n=1 with no unreplayed or keyless control cannot attribute recovery to the replay (the author's own record says admission 'completed on its own'), the keyless 'PROVIDED' arm was never tested, and the ~25 min figure is an unlogged paraphrase, so 'measured' overstates everything except the outcome.", "corrected_value": null}
```
