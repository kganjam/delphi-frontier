# The design loop

*The one mechanism the swarm reuses for every artifact, at every scale, in every project.*

This document names a pattern. It is deliberately short, because a pattern that needs ten pages to
state will not be followed. The schema that implements it is `designswarm` (21 tables); the research
behind each choice is gathered in the sibling documents on CAD/PLM practice, artifact identity, and
evaluation.

---

## 1. The loop

Every artifact this system produces — a designed protein, an actuator, a scaffold, a genetic edit
stack, a rig, a whole assembly — passes through the same six steps.

```
   PROPOSE  ──▶  CHARACTERISE  ──▶  GRADE  ──▶  CHALLENGE  ──▶  RANK  ──▶  RELEASE
      ▲                                                                      │
      └──────────────────────────  next generation  ◀───────────────────────┘
```

| Step | What happens | Where it lands |
|---|---|---|
| **Propose** | A generator emits candidates. Diversity matters as much as quality; a loop that collapses onto one mode has stopped searching. | `candidate` |
| **Characterise** | Each candidate is run through models, simulations or literature lookup to produce a **spec sheet** — parameters with values, conditions and evidence levels. | `spec_parameter` |
| **Grade** | A rubric, registered *before* the candidates existed, is applied by one or more graders. | `grade`, `comparison` |
| **Challenge** | An adversary tries to break the leading candidates. Its job is to attack, not to agree. | `challenge` |
| **Rank** | Survivors are ordered, with the uncertainty carried, not discarded. | `comparison` → Bradley-Terry |
| **Release** | A winner becomes an immutable revision with a part number and a timestamp. | `part_revision` |

The loop is not novel. What makes it work or fail is entirely in the four principles below.

---

## 2. The four principles

### P1 — The rubric is an artifact, registered before the candidates

A rubric is a row in `rubric` with an id, a version and a `frozen` flag. It is written **before** the
candidates are scored. If it must change after results are seen, that is a *supersession* with a
mandatory `change_reason`, not an edit.

The failure this prevents is the most common one in design work and the hardest to see afterwards:
scoring the candidates, noticing the winner is not the one you liked, and adjusting the weights. The
record then shows a principled evaluation. Freezing the rubric does not stop anyone changing their
mind — it stops them changing it *invisibly*.

### P2 — The grader is calibrated before it is trusted

An LLM grader is an instrument, and an uncalibrated instrument measures itself. Before a grader's
output is used, it runs `benchmark_item` rows with **known answers** — and critically, `known-bad`
items it must reject. A grader that passes a seeded-bad candidate is recorded `untrusted` and its
grades are not aggregated.

This is the same rule as the one that governs every check in this repository: *a guard ships with a
case it must flag*. A grader that has never rejected anything is not known to be a grader.

### P3 — Pairwise, both orders, named graders

Absolute scores from language models are poorly calibrated and drift between sessions; relative
judgements are far more stable. So ranking runs on `comparison` rows, each pair evaluated in **both
orders** with `order_swapped` recorded. Position bias then becomes a *measurable quantity* —
disagreement between the two orders is the measurement — instead of an assumption.

Graders are named, never pooled anonymously, because a grader that systematically favours its own
family's output is a real effect and can only be seen if you can group by grader.

### P4 — Every number carries how it was obtained

`spec_parameter.evidence` is a required field with a closed vocabulary: `measured`, `simulated`,
`predicted`, `derived`, `literature`, `assumed`, `unknown`. A value without `conditions` is not a
specification — a modulus at an unstated temperature, or a binding constant at an unstated pH, is a
number, not a parameter.

This makes the honesty floor **queryable** rather than aspirational. "Show me every released part
whose load-bearing parameters are `assumed`" is one `select`, and it is the first query to run before
anyone believes an assembly works.

---

## 3. Why the CAD analogy, and where it breaks

Mechanical engineering solved artifact management forty years ago, and the solution is a parts
library: stable part numbers, immutable released revisions, multi-level bills of materials, interface
control, and datasheets that state operating envelopes rather than single numbers. We take all of it.

**Three things transfer cleanly.**

1. **Identity that survives change.** A `part` is an identity; a `part_revision` is an immutable
   released state. A content hash alone cannot say "the same part, revision B"; an assigned id alone
   cannot prove integrity. We carry both — `part.id` assigned, `part_revision.content_sha256`
   derived.
2. **The datasheet as a table of characterised parameters**, each with its own test conditions. We
   already have one working example: the chromatophore study's 22-row actuator datasheet, which
   states stroke, blocked force, work density, rise time and bandwidth, each with its source. That
   artifact was produced before this schema existed, which is the strongest evidence the shape is
   right.
3. **Interfaces as first-class.** `part_interface` is an interface control document: what a part
   *provides*, what it *requires*, and what must hold for two to mate. Composition failures are
   interface failures, and systems that leave interfaces implicit discover this late.

**Three things do not transfer, and pretending otherwise would be the real danger.**

1. **A protein has no machining tolerance.** A bearing's bore is 25.00 ± 0.01 mm and the tolerance is
   a manufacturing property. A designed protein's behaviour is a *distribution* over contexts, and its
   "tolerance" is an expression level, a temperature, a binding partner and a cellular background.
   `spec_parameter` therefore carries `value_min`/`value_max` as an **operating envelope** and a
   mandatory `conditions` field — not a fake ± that would imply a precision nobody measured.
2. **Qualification is a probability, not a stamp.** An aerospace part is qualified or it is not. A
   predicted structure has a pLDDT; a predicted stability change has a confidence interval; a
   published phenotype has an n. The `evidence` vocabulary exists because `released` must never be
   readable as `verified`.
3. **Composition is not guaranteed.** Two bolted brackets behave like two bolted brackets. Two
   genetic edits that each work alone routinely do something else together, and nothing in a BOM
   predicts it. So a `bom_line` is a *claim about intent*, not about behaviour, and an assembly's
   spec sheet must be characterised in its own right rather than computed from its children.

---

## 4. The smallest honest instance

The loop is worth running even with one candidate, because the discipline is in the record, not the
tournament. A minimal pass is:

1. `rubric` row, frozen, with at least two criteria and their anchors.
2. One `benchmark_item` of kind `known-bad`, and a `grader_calibration` row showing the grader caught it.
3. One `candidate`, one `grade`, one `challenge` with an honest outcome.
4. A `part` + `part_revision` with at least one `spec_parameter` carrying `conditions` and `evidence`.

If any of those four is missing, the result is a preference, not an evaluation. That is an acceptable
thing to have — provided it is not recorded as the other one.

---

## 5. What this does not establish

- Nothing here makes a bad model good. The loop organises and records judgement; it does not supply it.
- The ranking mathematics is specified but not yet validated on our own artifacts; sample complexity
  for a reliable top-k is an open question, pursued in the evaluation research document.
- `bom_line` currently has no cycle check, so a part could in principle contain itself.
- No part has yet been through the full loop. Until one has, this document is a design, not a report.
