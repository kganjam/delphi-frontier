# Claim 27, propagated to dna and cell: what has to be true there

**Source claim (scale `protein`, recorded evidence: measured):**
> ADMISSION_PENDING is transient back-pressure, not a permanent wedge, PROVIDED the submission
> carries an idempotency key: replaying the original request under its original key cleared it after
> ~25 min and the job ran to SUCCEEDED.

Single reader. I made no API calls and I hold no Nebius credentials.

## 0. The main finding: this claim has no biological content to propagate

`docs/architecture/cross-scale-constraints.md` (commit `415dae51`) defines scales as biological levels.
A claim at scale N is supposed to require a mechanism, a length scale or a timescale at N±1.
Claim 27 is not a claim about a protein. It describes the **job-admission layer of a compute
service** (Nebius Scientific AI, operation `op-2112f97ee3d11f6e`, an ESMFold2 job). It sits at
`protein` only because the job folded a protein (kcnk5b).

**Read as biology, it requires nothing at the DNA scale or the cell scale.** No genome, gene product,
membrane or cell has to exist, take a value or move at a particular rate for this claim to be true
or false. Any biological constraint I wrote here would be made up. So the scale tag itself is a
category error, and I am recording it as a finding.

The output schema needs `target_scale` ∈ {dna, cell}. The constraints below are therefore
**operational**. They state what has to be true of the same admission layer when the
neighbouring-scale workloads go through it:

- **dna**: sequence-level jobs such as `msa_search_native`.
- **cell**: downstream jobs that chain on a protein output and are bound by a deadline.

That mapping is my own choice of interpretation. Neither the claim nor the architecture doc implies
it. Anyone consuming the `swarm-entail` block should treat these rows as constraints on
infrastructure, not as biological support for or against anything at those scales.

## Sources and read-levels

| source | what it gives | read-level |
|---|---|---|
| commit `ba1dd261` and `699500a7`, `docs/research/fish/proteins-readme.md` §4, §5, §8 | the claim; the server text `429 SCIENTIFIC_STAGE_ADMISSION_PENDING … key concurrency limit reached (1/1 operations in flight)`, `retry_same_idempotency_key: true`; the cancel refusal `REQUEST_REJECTED / recover the original admission with the same idempotency key first`; "esmfold2-specific, not a busy account"; "admission then completed on its own" | full-text |
| `origin/claude/mol-sims-20261101:results/mol-sims/claude-20261101/logs/fold_fgf_attempt1_429_receipt.json` | a boltz2 429 `ADMISSION_LIMIT_REACHED`, `"key concurrency limit reached (1/1 operations in flight)"`, `next_action: "… retry with the same idempotency key."`, `retry_after_seconds: 56` | full-text (lines 33–40 read) |
| `docs/research/fish/challenge-27.md` (commit `f87134f0`) | the pending interval bounded at **15 min 50 s to 26 min 56 s** from key-epoch and commit times; verdict WEAKENED | full-text |
| `docs/research/fish/challenge-277.md` (commit `eeadea3f`) | four keyless operations "held ADMISSION_PENDING since before this session"; 0 of 4 admitted in a 2026-11-04 burst | full-text |
| `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6 | `graph_deadline_s = 1800` in the **stab-ddg** model schema | full-text |
| `origin/swarm-architecture:library/tools/nbx.py` | the client; `EXPIRED` is listed as a terminal state, which is a client-side constant and not a server statement | full-text (grepped) |
| Nebius operation log for `op-2112f97ee3d11f6e`; `operations.jsonl` | timestamps of replays and polls | **could-not-access**. Not committed on any ref (challenge-27 searched all `refs/remotes/origin/*`). |
| `origin/claude-organ/sims:results/resources/scientific-ai-capabilities-20261101.json` | the service's own tool catalogue, captured 2026-11-01. `msa_search_native` and other tools carry: *"Durable operation: submit once with an idempotency key; poll get_operation …"*. Graph Apps carry: *"Reuse that key after response loss … An omitted key creates fresh one-shot work and cannot recover a lost response."* The catalogue gives **no** retention period and **no** admission or ADMISSION_PENDING semantics. | full-text (grepped for admission, concurrency, retain, ttl, expire, deadline, hours, days) |
| Web: `Nebius "ADMISSION_PENDING" idempotency key operation` and `Nebius AI Studio idempotency key retention period operations API` | server semantics and key retention | **search-summary**. Two standard searches returned **no Nebius result**; only other vendors' idempotency docs (e.g. Mastercard: keys removed after 24 h), which say nothing about this service. |

---

## 1. dna · existence: a key-to-operation record that re-attaches replays

**Requirement.** For a keyed replay to *clear* a pending admission, the admission layer must hold a
server-side record keyed on (account, idempotency key). A replay must re-attach to the original
operation instead of creating a new one. If this is a property of the admission layer rather than of
one model, it must apply to sequence-level (dna) jobs as well.

**Status: satisfied** for the existence of the mechanism (generic, model-agnostic). The evidence is
measured server responses recorded verbatim in the repo:

- esmfold2 returned `retry_same_idempotency_key: true`.
- On 2026-11-01, **boltz2** returned "retry with the same idempotency key". That is a second model on a
  different day.
- `cancel_operation` refuses with "recover the original admission with the same idempotency key
  first".
- The operation that reached SUCCEEDED, `op-2112…`, is the one created under the original key
  `esmfold2-kcnk5b-fresh-1793775862`. A new operation was not created.

Two caveats are in the note field:

- The server's text is the server's description of itself. I take it as reported.
- No **sequence-level** job was ever *observed* in a keyed replay. The service's own catalogue does
  *document* the same contract for `msa_search_native`: "Durable operation: submit once with an
  idempotency key". So for dna-scale jobs the mechanism is documented but not observed. The
  catalogue's wording is about recovering a *lost response*, not a *pending admission*. My inference
  is that the two may share a mechanism. The catalogue does not say they do.

## 2. dna · timescale: the key must be retained for longer than the pending interval

**Requirement.** The server must keep the idempotency record, and the pending admission it points
at, for at least as long as the pending interval. Otherwise a replay at minute 25 would be treated
as new. Bound: retention ≥ **950 s** (the lower edge of challenge-27's 15 min 50 s to 26 min 56 s
interval, derived from timestamps, not measured), and preferably ≥ 1616 s.

**Status: open.** The only evidence that retention exceeds about 16 to 27 min is the recovery event
itself. That evidence is **circular**: the claim cannot certify its own precondition. I found no
independent retention value:

- **Repo:** all refs were searched by challenge-27 for the operation log, and `nbx.py` was grepped
  for ttl/expire/deadline. The only hit is the client constant `EXPIRED`. I also checked a
  branch-wide `git grep` of all 765 remote branches for `ADMISSION_PENDING` or `idempotency key`, and
  read the service's own 2026-11-01 capability catalogue. The catalogue documents the key contract but
  states no retention period.
- **Web:** two standard searches returned no Nebius documentation.

So the gap is "nobody has published it where we could find it", not "measured and found short". The
service may document this under its hackathon tenant. That is unknown.

## 3. cell · timescale: pending plus runtime must fit inside any hard per-job deadline

**Requirement.** For "transient" to mean "the job eventually runs", the pending interval plus the
runtime must stay under any hard deadline whose clock starts at submission. Otherwise long pendings
end in `EXPIRED`, and "transient" means "not a wedge, but not a success either". Downstream
cell-scale jobs that chain on this output inherit that deadline.

**Arithmetic (derived, not measured).** The pending interval is 950 to 1616 s, and the runtime is 56.0 s
(server-reported), giving **1006 to 1672 s**. Against `graph_deadline_s = 1800` that leaves a margin
of 128 to 794 s. At the upper bound the job used **93%** of the deadline.

**Status: open.** I have two unknowns:

1. The 1800 s figure is from the **stab-ddg** schema. The esmfold2 deadline is **unknown**, because no
   esmfold2 schema read is recorded.
2. Whether the deadline clock starts at submission or at RUNNING is **unknown**.

The job succeeded, so whatever deadline applied was not exceeded. That makes the case consistent but
not informative. It does not contradict the claim, so this constraint is not unsatisfiable. What
it does show is my inference: **if** a submission-clock deadline of 1800 s applies to esmfold2, the
claim holds only for pendings shorter than about 29 min. Pendings longer than that would not be
"transient" in any useful sense. The claim states no such ceiling.

## 4. cell · conservation: occupancy of the 1/1 slot must balance

**Requirement.** "Back-pressure" means something is pushing back. With a server-reported cap of
**1/1 operations in flight**, the following must hold:

- In-flight ≤ 1 at all times.
- A keyed replay creates zero new operations, and a fresh key creates one.
- For the whole pending interval of `op-2112…`, **one identifiable operation** must occupy the slot,
  and its release must precede admission.

**Status: unsatisfied.** People looked and found no occupant in the committed record. Scope:

- challenge-27 and challenge-277 searched all `refs/remotes/origin/*` for the operation listing and
  the IDs of the occupants.
- I reran `git log --all -S ADMISSION_PENDING`. It gives 7 commits, and none of them names the
  occupant.
- Nobody queried the live service, so a live listing has **not** been looked for, and I did not do
  it either.

The parts that do hold:

- The replay-versus-new-key arm is consistent with the records: "minting a fresh key adds another
  stuck operation" (`699500a7`).

The parts that work against the balance, kept rather than averaged away:

- The author wrote that the wedge struck "after all other work had drained" (`ba1dd261` §8). Taken
  at face value, that leaves the 1/1 slot with **no known occupant**.
- The candidates are the four keyless operations, pending "since before this session"
  (`challenge-277`).
- At least 11 jobs, plus `op-2112…`, reached SUCCEEDED in the same account afterwards (`ba1dd261`).
  So a keyless ADMISSION_PENDING operation **cannot** be permanently holding a 1/1 slot. My inference
  is that one of two things is true:
  - (a) A pending operation does not count as in flight, in which case the "back-pressure" has a
    different source.
  - (b) The keyless operations do release, which would undercut the claim's "PROVIDED a key" clause.

  The records cannot tell (a) from (b).

## 5. dna · existence: the transient state must be a property of shared capacity, not of one model

**Requirement.** "Back-pressure" is a statement about shared capacity. If that is right, then
workloads other than esmfold2 that reach the same contention must also enter ADMISSION_PENDING and
recover under replay. The dna-scale sequence tools are one such case.

**Status: unsatisfied, and nobody has looked.** Only esmfold2 has ever been recorded in
ADMISSION_PENDING (scope: `git log --all -S ADMISSION_PENDING` on all fetched refs, 2026-11-04). The
other models that hit the cap got `ADMISSION_LIMIT_REACHED` with `admission: "not-submitted"`, which
is a *different* state that creates no operation (boltz2 receipt; challenge-277 burst).

The author's own record points against this requirement: "**This is esmfold2-specific, not a busy
account.** OpenFold2, Boltz2, msa-search and ProteinMPNN …" ran in the same window (`ba1dd261` §8).
That is the author's statement, and it is not a measured contradiction of a number. So I am not
marking this unsatisfiable. If a controlled test confirmed it, though, "back-pressure" would be the
wrong mechanism word for claim 27, even though the recovery outcome would still stand.

---

## Summary

| # | scale | kind | status |
|---|---|---|---|
| 1 | dna | existence: key-to-operation re-attachment | satisfied (two models; dna-scale jobs never checked) |
| 2 | dna | timescale: key retention ≥ 950 s | open (only evidence is circular; no Nebius doc found) |
| 3 | cell | timescale: pending + run (1006–1672 s) < deadline | open (esmfold2 deadline and clock start unknown) |
| 4 | cell | conservation: 1/1 slot occupancy balances | unsatisfied (no occupant identifiable in any committed record) |
| 5 | dna | existence: transience is model-agnostic | unsatisfied (nobody has looked; author says esmfold2-specific) |

**Nothing is unsatisfiable.** No measured number contradicts claim 27. The strongest result is the
one in §0: the claim is filed at a biological scale it does not belong to, so propagating it to dna
and cell yields constraints on infrastructure only. The tag should be changed so that it cannot be
counted as multiscale biological support.

```swarm-entail
{"source_claim": 27, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "A server-side record keyed on (account, idempotency key) must exist that re-attaches a replayed request to its original operation instead of creating a new one, and it must be model-agnostic so that sequence-level jobs inherit it",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Server responses recorded verbatim: esmfold2 429 with retry_same_idempotency_key: true; boltz2 429 (2026-11-01) next_action 'retry with the same idempotency key'; cancel refusal 'recover the original admission with the same idempotency key first'; op-2112f97ee3d11f6e reached SUCCEEDED under its original key",
      "satisfied_evidence": "measured",
      "note": "ba1dd261/699500a7 proteins-readme.md section 4 and 8 (full-text); mol-sims fold_fgf_attempt1_429_receipt.json lines 33-40 (full-text). The server text is the server's own description, taken as reported. Observed for two protein models only. For sequence-level (dna-scale) jobs the contract is documented, not observed: the service catalogue (origin/claude-organ/sims results/resources/scientific-ai-capabilities-20261101.json, full-text) says of msa_search_native 'Durable operation: submit once with an idempotency key'. That wording covers response loss; extending it to pending admission is inference. Category note: claim 27 is about compute infrastructure; this is an operational constraint, not a biological one."},
    {"target_scale": "dna", "kind": "timescale",
      "statement": "Server retention of the idempotency record and its pending admission must exceed the pending interval",
      "quantity": "idempotency-record retention time", "lo": 950, "hi": null, "units": "s",
      "status": "open",
      "satisfied_by": "No independent retention value found. The only evidence that retention exceeds the 950-1616 s pending interval is the recovery event itself, which is circular",
      "satisfied_evidence": "unknown",
      "note": "Lower bound 950 s is derived (challenge-27.md, key-epoch and commit timestamps), not measured. Searched: all origin refs for the operation log (challenge-27 scope), nbx.py for ttl/expire/deadline (only client constant EXPIRED), a git grep of all 765 remote branches, the service's own 2026-11-01 capability catalogue (full-text; documents the key contract, states no retention period), and two standard web searches for Nebius ADMISSION_PENDING and idempotency key retention (search-summary, no Nebius result). Scope: nobody has published it where we could find it; not measured and found short."},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "Pending interval plus runtime must stay below any hard per-job deadline that starts at submission, or 'transient' ends in EXPIRED rather than SUCCEEDED for downstream jobs that chain on the output",
      "quantity": "pending interval + runtime", "lo": null, "hi": 1800, "units": "s",
      "status": "open",
      "satisfied_by": "Observed case: 950-1616 s pending (derived) + 56.0 s runtime (server-reported) = 1006-1672 s, i.e. 56-93% of 1800 s. The 1800 s deadline is from the stab-ddg schema; the esmfold2 deadline and whether its clock starts at submission are unknown",
      "satisfied_evidence": "derived",
      "note": "graph_deadline_s=1800 from results/2026-10-31-kcne1-binding-ddg-STOPPED.md section 6 (full-text, stab-ddg schema). No esmfold2 schema read is recorded. The job succeeded, so this is consistent but uninformative; if a submission-clock 1800 s deadline applies, the claim holds only for pendings under ~29 min, a ceiling the claim does not state (inference)."},
    {"target_scale": "cell", "kind": "conservation",
      "statement": "Occupancy of the 1/1 in-flight slot must balance: at most one operation in flight, keyed replays create no new operation, and for the whole pending interval an identifiable occupant must hold the slot and release it before admission",
      "quantity": "operations in flight", "lo": 0, "hi": 1, "units": "operations",
      "status": "unsatisfied",
      "satisfied_by": "No occupant of the slot during op-2112f97ee3d11f6e's pending interval is identifiable in any committed record; the author states 'all other work had drained'. The replay-versus-new-key arm is consistent ('minting a fresh key adds another stuck operation')",
      "satisfied_evidence": "unknown",
      "note": "Searched: all origin refs by challenge-27 and challenge-277; git log --all -S ADMISSION_PENDING (7 commits, none names the occupant). The live service was not queried (no credentials), so a live operations listing has not been looked for. Tension preserved: four keyless ops pending 'since before this session' (challenge-277) cannot permanently hold a 1/1 slot while 11+ jobs and op-2112 later SUCCEEDED (ba1dd261), so either pending does not count as in flight or keyless ops release; the second would weaken 'PROVIDED a key'. That is inference, not observation."},
    {"target_scale": "dna", "kind": "existence",
      "statement": "If ADMISSION_PENDING is back-pressure from shared capacity, non-esmfold2 workloads (including sequence-level jobs) that reach the same contention must also enter it and recover under keyed replay",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Nobody has looked. Only esmfold2 has ever been recorded in ADMISSION_PENDING; other models at the cap received ADMISSION_LIMIT_REACHED / not-submitted, a different state that creates no operation",
      "satisfied_evidence": "unknown",
      "note": "Scope: git log --all -S ADMISSION_PENDING over all fetched origin refs on 2026-11-04; boltz2 receipt (mol-sims, full-text); challenge-277 0-of-4 burst. The author's own statement 'This is esmfold2-specific, not a busy account' (ba1dd261 section 8, full-text) points against the back-pressure reading; it is not a measured number, so this is not marked unsatisfiable."}
  ]}
```
