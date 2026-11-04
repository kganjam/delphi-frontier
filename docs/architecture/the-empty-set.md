# A mechanism that works, walking an empty set

*The most recurrent defect in this project, named after it appeared four times in one session, and
the sweep that finds the rest.*

---

## 1. The shape

> **A check that passes and a check that was never run produce the same two characters on screen.**

Every instance below is a mechanism that is *correct* — installed, tested, doing exactly what it
was written to do — operating over a collection with nothing in it. None of them failed. All of
them reported success.

| Instance | The mechanism | Its subject set | What the green meant |
|---|---|---|---|
| Evaluation kernel | rules 1, 2, 5 of [SPEC-evaluation-kernel](../specs/SPEC-evaluation-kernel.md) | `grade` **0 rows**, `rubric` **0** | grading never happened |
| Dependency propagation | trigger `trg_claim_superseded`, installed and correct | `claim_depends` **6 edges / 330 claims** | 29 of 35 supersessions flagged nothing |
| ASK rule 7 | the spec's own *"rule that makes the other six honest"* | **absent from the checker** | five rules looked like a complete list |
| Acceptance clauses | *"every unmutated pair carries a review"* | **0 pairs** | satisfied by producing nothing |

The fourth is the purest: a universally quantified clause over a collection the task itself
produces is satisfied **by producing none of it**.

---

## 2. Why it survives review

Each of these was read by someone who was looking. They survive because the evidence of the defect
is *identical to* the evidence of correctness:

- **The query succeeds.** No error, no timeout, no stack trace.
- **The count is a number.** `0` is a perfectly good number, and in a passing check it is the
  number you *want*.
- **The mechanism is defensible on inspection.** Reading `trg_claim_superseded` tells you it walks
  the graph correctly. It does. The graph is empty, and the trigger cannot tell you that.
- **The absent case leaves no trace at all.** ASK rule 7 was not wrong; it was *missing*, and a
  list of five rules does not look short.

---

## 3. The only defence is to count the subject set and say so

Three things, in increasing order of how much they buy:

**Print `UNCHECKED` in the same column as `PASS` and `FAIL`.** Not as a footnote, not folded into
either. `scripts/check_specs.py` does this, and its own output says why: *a rule this script cannot
evaluate is exactly as unenforced as it was before the script existed.* It currently reports 7
UNCHECKED of 24 — a number that would otherwise have been quietly banked as "mostly passing".

**Give every rule a positive control that must see rows.** A rule whose control returns 0 is
reported `UNCHECKED` rather than `PASS`, because a violation query pointing at an empty table and
one pointing at a clean table are indistinguishable.

**Ship every check with a case it must flag.** `check_specs.py`'s ASK rule 7 has four: the real
spec passes, a deleted dimension row fails, **a dimension kept but with its gap column emptied
fails**, and an unreadable spec returns `UNCHECKED`. The third is the one worth having — it is the
failure that looks like success.

---

## 4. The sweep, and what it found

`swarm/check_vacuity.py` counts the subject set of every mechanism in the schema and names what
each would silently satisfy. It is **not a gate**: an empty table is often correct, a mechanism
that has not been needed yet is not a defect, and a build that failed over one would get the check
switched off within a day. What is never correct is a *check reporting green over one*.

**Measured 2026-11-04: 11 of 21 mechanisms have no subject set at all.**

```
grade, rubric, candidate, comparison     the evaluation kernel, entire
idea_score                               idea scoring
run                                      ASK rule 3, and ALL simulation provenance
artifact                                 ASK rule 1
part                                     the parts library
need                                     the needs / pressure loop
experiment                               anything proposing bench work
retraction                               ASK D4
```

**`run` is the one that matters most, and it was not on the list of four.** It holds **0 rows**.
This project has produced simulations — equations of motion for the taxi phase, a launch energy
budget, aerodynamic area calculations — and **not one of them is recorded as a `run` with a
`code_sha`**. So the provenance mechanism for simulation, the thing that separates a computed
result from an asserted one, has never been exercised. Every simulated claim in the graph is
traceable to an agent's prose and no further.

That is a direct qualification on this project's central promise of grounded, non-hallucinated
simulation, and it was invisible until something counted the rows.

**Partly closed, 2026-11-04, and the fraction matters more than the fix.** Seven runs are now
recorded with a `code_sha` and zero missing one, so ASK rule 3 moves from `UNCHECKED` to `PASS`:
three ESMFold2 folds and a ProteinMPNN design, each pinned by its model revision
(`8fc3ff47…`, `v_48_020`) and operation id; an MSA search pinned by its database version; and two
local analyses pinned by the sha256 of scripts committed under `analysis/`, both of which
re-derive their reported numbers on demand.

**Nine runs now, and the headline number is among them.** `analysis/lift_budget.py` re-derives
v_min and the required lifting area from mass, area and C_L,max alone, and agrees with the Delphi
Lean registry's **independently written** C9 evaluator to **0.00000 %** on both — 7.561853784 m/s
and 4.116303686 cm². It also reproduces this project's own *"~20 cm² at 2 m/s"* as **20.01**. So
the number the whole argument rests on is now a command anyone can run, checked against an
implementation we do not maintain.

`analysis/collagen_signature.py` **refuses to report a negative** unless its positive control
separates first: a real collagen must come back collagen-like, or the actinodin result is not
printed at all.

**But only 5 of 11 simulated claims and 3 of 49 measured ones carry a `run_id`.** The rest were
produced by agents in prose, and nothing can retroactively give them a command — writing one would
invent provenance, which is the exact failure this field exists to prevent. So the mechanism is now
exercised and the backlog is unchanged: **the great majority of this project's computed numbers
still trace to an agent's prose and no further.** ASK rule 3 passing says the runs that exist are
well-formed. It does not say the computations are covered.

---

## 5. What this does not establish

- The sweep covers **tables in one Postgres schema**. A mechanism implemented in files, in a
  checker's own logic, or in prose is out of scope — ASK rule 7, the sharpest instance here, would
  **not** have been found by it, because its subject set was a missing branch in a script.
- 11 of 21 is a count of empty tables, not of defects. Deciding which emptiness is a gap and which
  is a mechanism correctly idle is a reading, and this document does not automate it.
- The four instances in §1 were found by hand, over one session. The rate at which this shape
  occurs is unknown; four is what one session surfaced once someone was looking for it.
