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

## 6. Cost attribution, done once: 58.7 % of spend left no trace

`SPEC-evaluation-kernel` rule 6 asks for a cost-attribution query and its **no-output bucket**. It
had never been run. Joining `agent_session.branch` to the `harvest:<leaf>` tag that appears in
`claim.source`, `artifact_signal.voter_id` and `constraint_entailed.note`:

| | |
|---|---|
| sessions with a cost and a branch | **722** ($935.49) |
| of those leaving **no artefact** anywhere | **465** (**$549.15**) |
| | **58.7 % of attributable spend** |

**It is not a harvest coverage gap** — that was checked first. `work_log` records **all 732**
`claude/*` branches as harvested.

**What the figure means.** *"Nothing that reached the graph"* is not *"nothing produced"*. An agent
that wrote a prose research document without a machine-readable block leaves no artefact by this
join, and so does one killed mid-flight when the credit ran out — 30 challenges were marked
`not-run` for that reason. **The figure bounds what the pipeline captured, not what the agents
did.**

**The first attempt at this number was wrong**, and the way it was wrong is this document's own
subject. Joining through `subproblem_id` alone gave 632 sessions and $740 — because **627 of those
are challenge, replicate and entail work that carries no `subproblem_id` at all.** The query would
have reported $740 of waste by looking in a column that the majority of sessions legitimately
leave empty.

## 7. The sweep's own blind spot: it reads the database, not the repository

§4 reported `run` holding **0 rows** and concluded that *"the provenance mechanism for simulation
has never been exercised"* and that *"every simulated claim traces to an agent's prose and no
further."*

**That was a statement about the database presented as one about the project.** `results/` holds
**972 committed files**, including **19 GPU and CPU compute run families** — `evo2zf` (a zebrafish
genomic model on an H100, 496 s, rc=0), Navier–Stokes flow refinement, a wind tunnel, held-out
validation sets.

**And the correction needs its own correction, because the record is thin as well as real.** Of
the 19 families, **exactly one** (`evo2zf`) carries an `entry.json` with full environment capture,
a `SHA256SUMS.json`, and a `control_check.json` — whose control is a good one: natural zebrafish
sequence at **0.452** nats/nt against mono-shuffles at **1.394/1.396** and iid-random at **1.398**.
**14 have only a `job.log`. At least one failed.**

So the accurate statement is neither "no provenance" nor "extensive provenance": **one run is
fully provenanced, most are logged, and none of it is linked to the graph.** That is a *linking*
problem, which is a better position than the one §4 described and a worse one than a file count
suggests.

**Linked, 2026-11-04.** All 14 runs the manifests describe are now `run` rows with their exit
codes, wall times and result hashes — the table goes from 13 to **27**.

**And the link surfaced a result nobody had recorded.** Four of the 14 are marked `failed`, and
**all three `heldout-validation-h100` runs are among them.** Two exited `rc=0` and were *still*
judged failed — the job ran cleanly and **the validation did not pass**.

> A project's held-out validation failing **three times out of three** is a finding. It appeared in
> no document, no claim and no summary until these rows existed.

**Read, 2026-11-04.** One of the three (`fgpuho2`) crashed in 2 s with 171 bytes — infrastructure,
not science. But `fgpuho3` ran 151 s, produced field data and a trajectory video, exited `rc=0`,
and was still judged failed. Its `exp2_comparison.json` is a Schnakenberg reaction–diffusion
CPU-vs-GPU comparison over **96 parameter cells**:

| | |
|---|---|
| max CPU/GPU numerical error | **3.4 × 10⁻¹⁰** |
| cells agreeing on **pattern formation** | **96 / 96** |
| cells disagreeing on the **dominant mode** | **26 / 96 (27 %)** |
| cells that **did not converge** | **30 / 96** |
| "old" criterion passes | 70 / 96 (72.9 %) |
| "revised" criterion passes | **96 / 96 (100 %)** |

**The good half is genuinely good:** zero disagreement on whether a Turing pattern appears, which
is the biologically meaningful outcome.

**The bad half is specific:** a discrete mode classification that flips between platforms in 27 %
of cells *despite* 10⁻¹⁰ agreement is sitting on a near-degenerate selection. Any claim about a
*particular* mode from this solver inherits that instability.

**And one line looked like it needed a person — it did not.** A criterion was **revised**, and the
pass rate went from 72.9 % to 100 %. That is the exact shape *"never relax an acceptance criterion
to make a task pass"* exists to catch, so it was recorded as an open question rather than an
accusation. **Then it was checked, and the revision is principled.** `frontier_compute/compare2.py`
holds both functions:

| | `agree_old` | `agree_revised` |
|---|---|---|
| `pattern` must match | yes | yes |
| `settled` must match | yes | yes |
| `mode` must match | **always** | **only if a pattern formed** |
| numerical error within `tol` | **not checked at all** | yes |

So the revision **drops one requirement and adds another**. The dropped one is the argmax of a
spectrum that has no peak: when no pattern forms, "dominant mode" is a readout of noise, and
requiring two platforms to agree on it is a requirement no correct solver could be expected to
meet. Three measurements say that is exactly what was happening, not a story told after the fact:

- All **26** cells failing the old criterion are mode disagreements, and **0 of the 26** had a
  pattern on either platform. Not most — all of them.
- **0** cells pass `old` and fail `revised`, so on this data the revision is a strict superset:
  nothing that used to pass was let go of.
- Pattern agreement is **96/96**, so the criterion that survived is the one that was never in
  doubt.

**What this does not establish, stated because the new clause is the interesting half.** The added
tolerance check **never binds on this run**: max error 3.4 × 10⁻¹⁰ against `tol` 1 × 10⁻⁹, so all 96
cells clear it and it has not yet rejected anything. It is stricter *in principle* and **untested in
practice** — this very document's subject. And this is a reading of the **code**, not of the
author's rationale: `compare2.py` carries no comment saying why the mode clause was conditioned, so
the inference is mine from the clause's structure and the 26/26 count, not a statement anyone made.

**The lesson is one I had already written down and failed to apply.** The flag said this *"needs a
person"*. The answer was one `git grep` away, in a committed file in the same repository. That is
the fifth time today I have called something unreachable and been wrong — four of the five — which
is now a worse hit rate than the sweeps this document criticises. **"Blocked route ≠ blocked
question" means: name the question without the route, then look for it, *before* writing that a
human is required.** Escalating is not the cautious option; it is an answer, and it can be wrong in
the direction that stops work.

**One run also gave an abstract gap its first instance.** `fevo2smoke1` failed with no result and
therefore no content hash. ASK rule 3 requires a `code_sha` **or** a stated
`not_executable_because`, and the schema has no such column — which is precisely D3's recorded gap.
Until this row existed, that gap had nothing to point at.

**The lesson is the document's own, turned on itself.** A sweep that counts rows in a schema
reports the schema's emptiness, and reads as though it had reported the project's. The vacuity
sweep ships with a positive control for each *mechanism*; it has none for its own *domain*.

## 5. What this does not establish

- The sweep covers **tables in one Postgres schema**. A mechanism implemented in files, in a
  checker's own logic, or in prose is out of scope — ASK rule 7, the sharpest instance here, would
  **not** have been found by it, because its subject set was a missing branch in a script.
- 11 of 21 is a count of empty tables, not of defects. Deciding which emptiness is a gap and which
  is a mechanism correctly idle is a reading, and this document does not automate it.
- The four instances in §1 were found by hand, over one session. The rate at which this shape
  occurs is unknown; four is what one session surfaced once someone was looking for it.
