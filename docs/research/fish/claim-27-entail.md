# Claim 27, propagated to adjacent scales (dna, cell)

**Source claim (scale `protein`, recorded evidence: measured), not written by me:**
> ADMISSION_PENDING is transient back-pressure, not a permanent wedge, PROVIDED the submission
> carries an idempotency key: replaying the original request under its original key cleared it after
> ~25 min and the job ran to SUCCEEDED.

**Result:**
- **1 satisfied:** a server-side key-to-operation map exists.
- **1 unsatisfied:** no documented key-retention window covers the pending time. I searched and found none.
- **2 open.**
- **0 unsatisfiable.** No measured number contradicts any constraint.

---

## 0. A scale mismatch, stated before anything else

Claim 27 is about a compute service's admission state machine (Nebius workbench, operation
`op-2112f97ee3d11f6e`). It sits at `protein` only because the job was an ESMFold2 fold of kcnk5b. It
says nothing about kcnk5b, about protein physics, or about any organism. **Read literally, it entails
nothing at the biological `dna` or `cell` scales.** No transcription rate, cell size or membrane
potential has to take any value for it to be true or false. I am not going to invent biological
constraints to fill the template.

So that the exercise still checks something, I use **my own mapping** of "adjacent scale" onto the
system that produced the protein-scale result:

- **`dna`** means the layer below: the request record. That is the payload plus the idempotency
  key, and the server-side state that resolves a key to an operation. It is the "encoding" the
  operation is built from.
- **`cell`** means the layer above: the account and workflow. That is the shared 1/1 in-flight slot,
  the other operations competing for it, and the population of operations whose fate the claim
  generalises over.

This mapping is an inference of mine, not something the claim or the task specifies. A reader who
rejects it should treat every constraint below as **vacuous at the biological scales**. That is
also a correct reading.

## Sources and read-levels

| source | what it gives | read-level |
|---|---|---|
| commit `ba1dd261` (2026-11-03 23:20:12 −0800), `docs/research/fish/proteins-readme.md` §4–§8 | the verbatim server responses (`429 SCIENTIFIC_STAGE_ADMISSION_PENDING`, `retry_same_idempotency_key: true`, `key concurrency limit reached (1/1 operations in flight)`, the cancel refusal); the keyed-operation table; the "four keyless operations" | full-text |
| commit `699500a7` (2026-11-03 23:31:18 −0800), same file §8 | the claim; `op-2112f97ee3d11f6e` SUCCEEDED, 56.0 s compute | full-text |
| commit `2ef23dc2` (2026-11-04 01:37:45 −0800), commit message | the 0-of-4 concurrency burst; keyless operations "have held ADMISSION_PENDING since before this session" | full-text |
| `docs/research/fish/challenge-27.md` (branch `claude/challenge-admission-pending-idempotency-knp3xs`, commit `f87134f0`) | pending duration bounded to ~16–27 min from key and commit timestamps; verdict WEAKENED | full-text |
| `docs/research/fish/challenge-277.md` (commit `eeadea3f`) | the three disagreeing records of who holds the slot | full-text |
| `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6 (this branch) | `graph_deadline_s = 1800` for the **stab-ddg** App, a different App from esmfold2 | full-text |
| Nebius operation log / `operations.jsonl` | timestamps of submit, replays and admission | **could-not-access**. Not committed on any ref (searched by challenge 27, and confirmed here for `ADMISSION_PENDING` with `git log --all -S`). No credentials, no API calls. |
| Web: Nebius public docs on idempotency-key retention | the key retention window | **search-summary**. Two searches (below). No Nebius page on the subject was returned. |
| Web: Mastercard Processing, Toolpath and Nuvei idempotency docs | retention windows at **other** providers | **search-summary**. These pages were not opened, so their numbers are not quoted as Nebius facts. |

---

## 1. Constraints and checks

### C1 · `dna` · existence: a key-to-operation resolver must exist

**Requirement.** Some server-side state must persist the idempotency key and map a replay of the
original request back onto the **same** operation, rather than creating a new one. Without it,
"replaying under its original key" cannot "clear" anything. It would only add operations.

**Check: satisfied, by records of measurement made by the original author. I re-read them; I did
not re-measure.**
- The server's own response, recorded verbatim in `ba1dd261` §8, says
  `retry_same_idempotency_key: true`. `cancel_operation` refuses with *"recover the original
  admission with the same idempotency key first"*.
- The 2026-11-01 `ADMISSION_LIMIT_REACHED` receipt (cited full-text in challenge 27) also says
  *"retry with the same idempotency key"*.
- The same operation ID, `op-2112f97ee3d11f6e`, under the same key,
  `esmfold2-kcnk5b-fresh-1793775862`, is recorded as `ADMISSION_PENDING` at 23:20 (`ba1dd261`) and as
  `SUCCEEDED` at 23:31 (`699500a7`).

This shows that a resolver exists and that it preserved operation identity across replays. It does
**not** show that the replay caused admission. That was challenge 27's main point and I keep it.

### C2 · `dna` · timescale: the key must outlive the pending period

**Requirement.** The server's idempotency-key retention window T_key must exceed the time T_pend
that an operation spends in `ADMISSION_PENDING`. If the key expires first, a "replay under its
original key" becomes a fresh submission, and the "PROVIDED a key" condition cannot do any work.

- For the observed case, T_pend is between about **960 s and 1620 s**. Challenge 27 derived this
  from key and commit timestamps; it was not measured.
- So T_key ≥ 960 s is necessary, and T_key ≥ 1620 s is needed to be safe.
- For the claim's general form ("transient … provided a key"), T_key must exceed the longest
  pending period that can occur. Nothing records an upper bound on that.

**Check: unsatisfied. I looked, and found no independent value.**
- **What I searched.** Two web searches, read-level search-summary:
  - "Nebius idempotency key retention window ADMISSION_PENDING scientific workflow"
  - "Nebius AI Studio API "idempotency" key operations docs"

  Neither returned a Nebius page that documents idempotency-key retention or `ADMISSION_PENDING`.
  I also searched this repo for the terms on all refs (`git log --all -S"ADMISSION_PENDING"`). Its
  only Nebius-specific evidence is the claim's own episode.
- **Why the claim's own episode does not count.** Operation identity did survive at least
  ~960 s, so T_key ≥ ~960 s can be derived from it. That is **circular**: it uses the claim to
  satisfy the claim's own entailment. I am recording it, not counting it.
- **Other providers vary widely.** The search summaries report:
  - 24 h for Mastercard Processing and Toolpath;
  - **15 min (900 s)** for Nuvei's cached response, which is *below* the 960 s floor.

  These numbers are not Nebius and do **not** contradict the constraint. They show that it is not
  satisfied automatically by industry convention.
- **Scope of the negative.** Public web, two queries, plus this repository. I did not search Nebius
  support channels, any SDK source, or the live API. This is "people looked in public docs and
  found nothing". It is not "the window was measured and is too short".

### C3 · `cell` · timescale: whatever occupies the slot must drain faster than T_pend

**Requirement.** The server reports a **1/1** in-flight cap:
`key concurrency limit reached (1/1 operations in flight)`, verbatim in `ba1dd261`. "Back-pressure"
that clears means the slot's occupant leaves within the pending window. Its residence time must be
≤ T_pend, which is about **1620 s** at most (derived). If the occupant cannot leave on that timescale,
`ADMISSION_PENDING` is a wedge, not back-pressure.

**Check: open. The occupant was never identified, so no measured residence time can be compared.**

The records constrain it in two directions. I keep both.
- **The keyless operations cannot have been the occupant.** `2ef23dc2` says four keyless operations
  "have held ADMISSION_PENDING since before this session" as of 01:37:45 on 11-04. `ba1dd261` already
  mentions them at 23:20:12 on 11-03.
  - Their residence is therefore ≥ **~2 h 17 min (≈ 8,200 s)**. This is derived from commit times
    and rests on the author's assertion; no listing was committed.
  - If they had held the 1/1 slot, `op-2112…` could not have been admitted at ~23:31. It was
    admitted. My inference is that `ADMISSION_PENDING` operations, at least the keyless ones, do not
    occupy the counted slot.
  - This undercuts the claim's *mechanism*. "Back-pressure" from pending operations is not what
    the cap counts. It does not refute the *outcome*.
- **A per-job deadline exists, but for another App.** The stab-ddg App reports
  `graph_deadline_s = 1800` (`results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6). If esmfold2
  carried the same deadline, a normal running occupant would leave within 1800 s. That is the same
  order as T_pend, but not guaranteed to be below 1620 s. The esmfold2 deadline is **unknown**. I did
  not find it in any committed schema.
- **The occupant was already present before the burst.** At 01:37 the slot was full before a burst
  of 4 submits (0 admitted; challenges 256 and 277). Who held it is recorded three incompatible ways
  (table in challenge 277). That disagreement is preserved, not resolved.

### C4 · `cell` · range: keyed `ADMISSION_PENDING` operations must recover, as a fraction of the population

**Requirement.** "Not a permanent wedge, PROVIDED a key" is a statement about the population of
keyed operations. The fraction of keyed `ADMISSION_PENDING` operations that go on to reach
admission must lie in **[1, 1]** (dimensionless). One permanently stuck keyed operation would
falsify it.

**Check: open. No keyed failure was measured, so it is not unsatisfiable. The population is too
small, and recorded inconsistently, to call it satisfied.**

`ba1dd261` records three keyed esmfold2-path operations that entered `ADMISSION_PENDING`:

| operation | key | §6 table (`ba1dd261`) | §8 text (`ba1dd261`, kept as "superseded" in `699500a7`) |
|---|---|---|---|
| `op-5b52c20d713af416` | `json-sequence-73984624` | "recovered and run" | listed as still `ADMISSION_PENDING` |
| `op-4e400a5b52a2b9d8` | `json-empty-73974323` | "recovered then cancelled" | listed as still `ADMISSION_PENDING` |
| `op-2112f97ee3d11f6e` | `esmfold2-kcnk5b-fresh-1793775862` | — | `ADMISSION_PENDING` at 23:20, then `SUCCEEDED` (`699500a7`) |

- **Fraction recovered:** 3/3 by the §6 table, 1/3 clean by the §8 text plus the later commit.
  Neither reading records a keyed operation that *failed* to recover. That is why this is not
  unsatisfiable.
- **Population is tiny:** n ≤ 3, all esmfold2, all from one account on one evening.
- **The keyless arm, which the "PROVIDED" clause needs, has no recovery path.** The four keyless
  operations have been pending ≥ ~2 h 17 min (C3). That is *consistent* with keyless operations
  staying wedged. But they could not be replayed, so they cannot show that the key is what makes the
  difference. That would need a keyless operation watched under the same conditions as a keyed one.
  That has not been done; nobody has looked.

---

## 2. Why nothing is `unsatisfiable`

For a constraint to be `unsatisfiable`, a measured number has to contradict it. Two numbers come
close; neither qualifies:

- **The keyless operations' ≥ 2 h 17 min residence (C3).** It would contradict C3 only if those
  operations were the slot's occupant. The keyed admission at 23:31 shows they were not. It counts
  against the "back-pressure" *mechanism*, not against the constraint.
- **Nuvei's 900 s key retention (C2).** It is below the 960 s floor. But it belongs to a different
  provider, so it says nothing about Nebius.

I am not softening anything here. The negatives that do exist are stated with their scope under C2
and C4.

## 3. What would close the open items

- **C2:** obtain Nebius's documented key-retention window. Or measure it: replay a completed keyed
  operation at increasing delays, and log the first delay at which it returns a new operation ID.
- **C3:** while an operation is in `ADMISSION_PENDING`, capture an operations listing with
  timestamps. That identifies the slot occupant and its residence time. Also read esmfold2's
  `graph_deadline_s` from its schema.
- **C4:** run challenge 27's controlled design. Keyed-replayed, keyed-unreplayed and keyless
  operations each go into `ADMISSION_PENDING`. Log every `get_operation`. Repeat to n > 1.

```swarm-entail
{"source_claim": 27, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "A persistent server-side resolver must exist that maps a replay carrying the original idempotency key onto the same operation rather than creating a new one",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Server-reported key-recovery grammar (retry_same_idempotency_key: true; cancel refusal 'recover the original admission with the same idempotency key first') and op-2112f97ee3d11f6e retaining its ID under key esmfold2-kcnk5b-fresh-1793775862 from ADMISSION_PENDING (ba1dd261) to SUCCEEDED (699500a7)",
      "satisfied_evidence": "measured",
      "note": "Measured by the original author; I re-read the records full-text (commits ba1dd261, 699500a7, proteins-readme.md section 8) and did not re-measure. Shows identity preservation, not that replay caused admission (challenge-27). 'dna' here is my mapping to the request/key layer below the operation; read biologically, the claim entails nothing at dna."},
    {"target_scale": "dna", "kind": "timescale",
      "statement": "The idempotency-key retention window must exceed the time an operation spends in ADMISSION_PENDING",
      "quantity": "key retention window T_key relative to pending duration T_pend (T_pend derived 960-1620 s)", "lo": 960, "hi": null, "units": "s",
      "status": "unsatisfied",
      "satisfied_by": "Searched for a documented Nebius key-retention window and found none; the only Nebius datum is the claim's own episode (circular, not counted)",
      "satisfied_evidence": "unknown",
      "note": "Scope: two web searches, read-level search-summary ('Nebius idempotency key retention window ADMISSION_PENDING scientific workflow'; 'Nebius AI Studio API \"idempotency\" key operations docs'), plus all refs of this repo. No Nebius support, SDK source or live API checked. People looked in public docs and found nothing; nobody measured it. Other providers per search summaries: Mastercard Processing and Toolpath 24 h, Nuvei 15 min (900 s, below the 960 s floor), so not satisfied by convention, and not Nebius, so no contradiction. 1620 s is the safe lower bound; T_pend bounds are derived from key and commit timestamps in challenge-27, not measured."},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "Whatever occupies the account's 1/1 in-flight slot must drain on a timescale no longer than the pending period, or the state is a wedge rather than back-pressure",
      "quantity": "residence time of the slot occupant", "lo": null, "hi": 1620, "units": "s",
      "status": "open",
      "satisfied_by": "Occupant never identified: no operations listing or operations.jsonl was committed on any ref",
      "satisfied_evidence": "unknown",
      "note": "Derived from commit times and the author's assertion (2ef23dc2, ba1dd261): four keyless ADMISSION_PENDING operations persisted at least about 8,200 s yet op-2112 was admitted, so they cannot have held the slot. My inference is that pending operations are not what the cap counts, which undercuts the back-pressure mechanism, not the outcome. stab-ddg graph_deadline_s = 1800 (results/2026-10-31-kcne1-binding-ddg-STOPPED.md section 6) is a different App; the esmfold2 deadline is unknown. Slot-holder records disagree three ways (challenge-277); preserved."},
    {"target_scale": "cell", "kind": "range",
      "statement": "Across the population of keyed operations that enter ADMISSION_PENDING, the fraction that later reach admission must be 1",
      "quantity": "fraction of keyed ADMISSION_PENDING operations later admitted", "lo": 1, "hi": 1, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "n <= 3 keyed operations (op-5b52c20d713af416, op-4e400a5b52a2b9d8, op-2112f97ee3d11f6e); 3/3 recovered per ba1dd261 section 6 table versus 1/3 clean per section 8 text plus 699500a7; no keyed failure recorded",
      "satisfied_evidence": "measured",
      "note": "Records full-text, internally inconsistent; disagreement preserved, not averaged. Not unsatisfiable: no keyed failure was measured. Not satisfied: n is tiny, all esmfold2, one account, one evening. The keyless control that the PROVIDED clause needs was never run; nobody has looked."}
  ]}
```
