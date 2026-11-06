# SPEC — The evaluation kernel

**Status:** normative. Implemented in `designswarm` (`rubric`, `candidate`, `grade`, `comparison`,
`benchmark_item`, `grader_calibration`, `challenge`).

This spec is written **after** a night of running the mechanism on 166 resolved challenges, so most
of it is measured rather than designed.

---

## 1. What the kernel is for

Choosing between candidates, and deciding whether a claim holds. Both reduce to the same problem:
**an instrument whose readings nobody has checked.**

---

## 2. Rubrics

**REQUIRED:** an id, a version, a `criteria` array where each criterion has a `key`, a `question`,
a scale and **anchors** naming what each score means, and an `aggregation`.

**REQUIRED:** `frozen = true` before any candidate is scored against it.

**A rubric is superseded, never edited.** Changing it after seeing results creates a new row with
`superseded_by` and a mandatory `change_reason`.

**INVALID:** scoring against an unfrozen rubric; editing `criteria` in place; a criterion with no
anchors, since an unanchored 1-to-5 scale is a preference with a number attached.

---

## 3. Graders must be calibrated before they are trusted

**REQUIRED before a grader's output is aggregated:** a `grader_calibration` row over
`benchmark_item`s with known answers, **including at least one `known-bad` item it must reject.**

**A grader that passes a seeded-bad item is recorded `untrusted` and its grades are excluded.**

**INVALID:** aggregating grades from a grader with no calibration row.

**Status: NOT ENFORCED.** No `benchmark_item` exists and no grader has been calibrated. Every
challenge verdict recorded tonight came from an uncalibrated instrument. That is the single largest
gap in this system and it is stated here rather than discovered later.

---

## 4. Challenges, and what the base rate actually showed

A `challenge` is an attack on a specific claim. The challenger is told to **try**, and to report
honestly when the claim survives, because an agent rewarded for finding faults manufactures them.

**Measured, 2026-11-04, 156 resolved challenges:**

| Outcome | Count | Share |
|---|---|---|
| weakened | 109 | 70% |
| survived | 26 | **17%** |
| refuted | 21 | 13% |

**A 17% survival rate looks like manufactured faults, and I checked whether it was.** Sampling six
`weakened` verdicts found all six substantive: a re-derivation that reproduced and then caught an
upper bound treating the floor of a range as a ceiling; a precise correction of a mean computed over
the wrong residue span; a primary-source reading that changed a boundary condition; and a correction
of a claimed inaccessibility that was not real.

The recurring shape is **"the arithmetic reproduces, *but* the inference overreaches."**

So the honest reading is not that the challengers are over-firing. It is that **most claims in this
project were stated more confidently than their inputs justified** — which is a finding about us.

**This inference is itself uncalibrated** (§3). Six sampled by hand is not a measurement of 109.

---

## 5. Ranking

Pairwise, each pair in **both orders**, with `order_swapped` recorded, so position bias is a
measured quantity. Graders are **named, never pooled**, so self-preference is visible.

**Status: NOT RUN.** No `comparison` rows exist. Ranking is specified and unexercised.

---

## 6. What the night measured about the kernel itself

Three faults, all found by auditing *what the spend bought* rather than how much:

1. **31 challenges were dispatched against bookkeeping rows** — `LAWENTRY <slug> dispatched` was in
   the `claim` table, so the selector picked it up. Real sessions attacked strings.
2. **Deepening recursed on its own output** to `S21-D-D-D`, each level thinner than the last.
3. **Law entries were re-dispatched** that already existed, four under different slugs, which would
   have landed duplicate entries that could disagree while neither knew the other existed.

**All three were invisible in the headline counts, which rose throughout.** Claims, branches and
commits all went up while the marginal session was worthless.

**So the kernel needs a cost-attribution check as a first-class part of itself**, not as
housekeeping: group sessions by what they produced, and look at the bucket that produced nothing.
That query is what found all three.

---

## 7. Acceptance

1. No grade recorded against an unfrozen rubric.
2. No rubric edited in place.
3. No grader aggregated without a calibration row that includes a caught `known-bad` item.
4. Every challenge outcome recorded, **including `survived`**.
5. Every pairwise comparison run in both orders with the order recorded.
6. A cost-attribution query run after every batch, and its no-output bucket read.

---

## 8. What this does not establish

- **Measured 2026-11-04: §1, §2 and §5 cannot fail, because the kernel was never used.**
  `grade`, `rubric`, `candidate` and `comparison` all hold **0 rows**. The calibration this
  project cites is real and recorded — one `grader_calibration` row, `cloud:claude-opus-5-5`,
  7/7 items, **4/4 known-bad caught**, verdict `trusted`, behind 7 `benchmark_item` rows — but it
  calibrated a grader that then graded **nothing through this kernel**. All 747 resolved verdicts
  came from the `challenge` path, which has no frozen rubric, no registered criteria and no
  both-orders requirement.

  So a checker reporting those three rules green is not evidence that grading is disciplined. It
  is evidence that grading did not happen — the same vacuous-over-an-empty-set defect this
  project already documented for universally quantified acceptance clauses. The honest status of
  this spec is **unimplemented**, not **satisfied**.
- **§3 is not enforced and not satisfied.** Every verdict in the system is from an uncalibrated
  grader. Nothing downstream should be read as more certain than that allows.
- §5 has never run.
- §4's conclusion rests on six hand-sampled verdicts out of 109.
- No rubric has been written, so §2 is specified and untested.
- The three faults in §6 were found by hand. Nothing runs that query automatically.
