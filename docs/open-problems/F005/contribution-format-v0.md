# Delphi contribution format v0 (proposed for F005; not yet agreed with any other participant)

A **contribution** is something a second participant can consume to change one of *their* research actions. It is offered as a
`frontier_propose` Action draft and answered with an Evidence record. Every field below maps onto the live node's existing schemas
(`frontier://schema/Action`, `frontier://schema/Evidence`, read anonymously on 2026-11-01); no new record kind is needed.

## What the offering side publishes (Action, `intent: replication` or `curation`)
| Field | Meaning | Live schema field |
|---|---|---|
| target | the exact Problem version the work feeds | `target` (Ref with 64-hex `version`) |
| consumed inputs | exact record versions **and** byte digests of the files to consume | `inputs[]` (Refs) + `cache_key.input` (sha256) |
| acceptance | mechanical check + non-author review; a mismatch is a valid result | `acceptance_criteria[]`, `cache_key.acceptance_policy` (= checker sha256) |
| bounds | CPU/GPU/time/person-hours; stop rule | `cost_stop_bounds` |
| decision consequence | which recorded number/category moves on agree vs disagree | `proposal.outcomes[].decision_consequence` |
| non-reuse | what project code the participant must **not** reuse for the work to count as independent | `acceptance_criteria` |

## What the consuming side returns (submission JSON → Evidence)
`participant` (attributable principal), `consumed` (input sha256 + Ref, exactly as offered), `solver`/`method` (own code sha256 and what was
not reused), results, `receipt` (command, exit code, wall time, host class), `cost` (CPU seconds, participant minutes) and the checker's
output. Recorded as Evidence with `produced_by` = the Action, `relation` supports/refutes, artifact digests as `urn:sha256:` pointers.

## Applicability check (consumer side, before using it)
The consumer states why the consumed version applies to their action (same model, parameters, version) and rejects stale or incompatible
versions (`is_head`, matching sha256). A contribution consumed without this check does not count for F005.

## First offered task
`replay-task.md`: independent replay of sweep cells 240 and 1306, checker `check_replay.py`, draft `replay-task.action-draft.json`.
