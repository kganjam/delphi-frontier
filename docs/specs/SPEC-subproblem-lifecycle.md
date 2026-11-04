# SPEC — The subproblem lifecycle

**Status:** normative. Implemented in `designswarm` (`subproblem`, `subproblem_dep`, `review_flag`,
`agent_session`).

Written after a bug in exactly this area silently blocked the project's most important open question
for three hours, so §4 and §6 are measured rather than designed.

---

## 1. States

```
  open ──▶ running ──▶ answered
    │          │           │
    │          └──▶ open   └──▶ refuted ──▶ superseded
    └──▶ blocked                    
```

| State | Means |
|---|---|
| `open` | ready to be worked, dependencies satisfied |
| `running` | an agent session holds it **and that session is alive** |
| `answered` | a result recorded, with an `answer_kind` |
| `refuted` | asked and settled negatively — **a product, not a failure** |
| `blocked` | a dependency is unsatisfied, or an external blocker is named |
| `superseded` | re-posed, usually via a `regime_transition` |

**REQUIRED on `answered`:** an `answer` and an `answer_kind` from the evidence vocabulary.
**REQUIRED on `blocked`:** a named blocker. "Blocked" with no reason is indistinguishable from
abandoned.

---

## 2. Readiness

A subproblem is ready when `status = 'open'` and **every** row in `subproblem_dep` pointing at it
resolves to a subproblem in `answered` or `refuted`.

`refuted` satisfies a dependency. A question that was settled negatively has been settled.

---

## 3. Spawning, and promotion to a frontier

A subproblem may spawn children when its answer exposes a sharper question. **A subproblem that
spawns two or more children is a frontier** ([frontiers](../architecture/frontiers-and-the-delphi-layer.md) §1),
and that happened for real: S6 split into S25 and S26 with nobody deciding it.

**Deepening is capped at depth 2**, and the cap is set on evidence rather than intuition. It was
first set at 1 on the reasoning that deeper levels are thin. Harvesting then found two depth-2
results that were not: **S23-D-D** showed a conclusion was sensitive to E0 *only because* `f=1`
silently assumed actinotrichia span the whole fin, when in adult zebrafish they occupy the distal
200–300 µm of a ray; **S7-D-D** measured a bending section from published µCT. Both reach an
assumption buried under an answer, which depth 1 cannot. Depth 3 produced `S21-D-D-D` and nothing of
value.

---

## 4. `running` is a claim about a live session, and it must be checked

**This is the clause the spec exists for.**

A finished cloud session reports `session_status: idle`; `status_bucket: completed` is the
authoritative signal. Subproblems written with the raw `idle` sat in `running` indefinitely, and
because readiness treats `running` as in-flight, **a dead session silently blocked every dependent**.

**Measured:** S11's session finished at 06:06 and S11 stayed `running` until 09:4x. For those three
hours **S15 — the minimal edit stack, the project's buildable-DNA deliverable — was unreachable**,
and nothing surfaced it. Claims, branches and session counts all rose throughout.

**REQUIRED:** a subproblem in `running` whose session is not alive is resolved on the next poll —
to `answered` if it recorded a claim, to `open` if it did not.

**INVALID:** `running` with no `agent_session` row, or with a session in a terminal state.

**The general shape, which has recurred four times in one night:** a component that is finished and
a component that is working look identical unless something counts its output. Every instance was
found by rendering or auditing, never by a metric.

---

## 5. Review flags

When a claim is superseded, every subproblem owning a claim that depended on it is flagged `open`
([ASK spec](SPEC-ASK-artifact-graph.md) D4). A flag does **not** reopen the subproblem — it marks
the answer as resting on something withdrawn, and a human or agent decides.

---

## 6. What a subproblem must carry to be worth having

From the ones that worked:

1. **A number in the question.** "Can a fin ray carry load?" is unanswerable; "can it carry load
   without exceeding 10% tip deflection at the design lift?" is a calculation.
2. **A falsifier.** S21's was *"a measured adult peak velocity at or above 5.8 m/s"*. The question
   that found the answer was shaped by knowing what would overturn it.
3. **A stated dependency list**, so superseding an input propagates.

**The best subproblems named what would settle them before anyone looked**, and the measured outcome
supports this: every subproblem that produced a decisive result carried a falsifier, and the four
that stalled at zero claims did not have one that could be reached with available tools.

---

## 7. Acceptance

1. No `answered` without an `answer` and `answer_kind`.
2. No `blocked` without a named blocker.
3. No `running` without a live session; stale rows resolved on the next poll.
4. Readiness computed from `subproblem_dep`, with `refuted` satisfying a dependency.
5. Deepening capped at depth 2.
6. Every superseded claim flags the subproblems whose answers rest on it.

---

## 8. What this does not establish

- Rules 1, 2, 4 and 5 are enforced in code; **3 and 6 are enforced only by the poll and the
  trigger**, both of which have already failed once each tonight.
- §6 is generalised from roughly fifty subproblems in one project, which is an observation and not
  a measurement.
- Nothing checks that a `falsifier` is actually reachable with available tools, which is what
  distinguished the productive subproblems from the four that stalled.
