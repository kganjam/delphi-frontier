# Challenge 223: the grader-benchmark scope statement

**Claim (author's text, verbatim):** "SCOPE: one grader, seven items, one run. It establishes that
this grader catches these four defect classes, not that it catches every class, and not that other
graders do. The benchmark should grow as new defect classes are found."

Recorded evidence level: `unknown`. Value: n/a. Source: scope statement.

**Verdict: WEAKENED.** The three things the statement rules out are ruled out correctly. The one
thing it rules in, "establishes that this grader catches these four defect classes", claims more
than one run over seven items can show.

## What I could and could not read

- I could not find the benchmark this statement scopes. I searched this repository's working tree
  and every commit on both branches (`claude/grader-scope-challenge-7jql8r`,
  `work/frontier-foundation`) for "grader", "seven items", "defect class" and "four defect". I
  also ran a GitHub code search for `"seven items" grader repo:kganjam/delphi-frontier`, which
  returned 0 results. Read-level for the benchmark itself: **could-not-access**.
- So I do not know which four classes it uses, how the seven items are split across them, whether
  any items are clean controls, what the grader is, or whether it was deterministic. I treat all of
  these as `unknown` and do not guess them.
- What follows is a review of the scope statement **as text**, with the counts it states as its
  only inputs. Every number below is **calculated** from those counts. None of it is observed.

## 1. Arithmetic, redone independently

The statement gives two counts: 7 items and 4 defect classes.

- 7 items across 4 classes is 1.75 items per class on average. By pigeonhole, at least one class
  has at most 1 item, and that is before any items are set aside as clean controls. If 3 are
  controls, every class has exactly 1 item. *(Calculated.)*
- Suppose the grader caught every item in a class. The exact (Clopper–Pearson) two-sided 95% lower
  bound on its per-class detection rate is 0.025^(1/n). *(Calculated. The formula for k = n is
  closed-form, and I checked it in Python.)*
  - n = 1: lower bound **0.025**
  - n = 2: lower bound **0.158**
  - n = 7, all classes pooled: lower bound **0.590**
- So even a perfect score cannot exclude a per-class detection rate as low as 2.5–16% for the
  thinnest classes. "Catches this class" is a statement about a rate. The data support "caught
  these one or two instances on this run".

## 2. Proxy

- **Proxy:** caught the seeded instance(s) of class X.
  **Quantity that matters:** the probability the grader flags a new, unseen defect of class X.
  Instances written by the same people who chose the classes, possibly with the grader in mind,
  are a weak sample of the class. The statement treats the instance as standing in for the class.
- **Missing second half:** "catches" reports sensitivity only. A grader that flags everything
  catches all four classes. Unless some of the seven items are clean and the grader passed them,
  the benchmark does not show the grader **discriminates**. Whether such controls exist is
  `unknown`, because I could not read the benchmark.

## 3. Hidden assumption: one run is representative

"One run" is honest only if the grader is deterministic. If it is an LLM or otherwise sampled,
one run tells you nothing about how much the result varies between runs.

This project has already measured that sort of instability. `findings/README-third-assessor.md`
(read-level: **full-text**) reports a kappa of 0.369 when a third assessor's verdicts are compared
with the two-assessor majority. The author of that finding attributes the disagreement partly to
a different prompt ("the verdict label is unstable across assessor setups").

**My inference, not that author's claim:** that finding is about a different instrument, so it
proves nothing about this grader. It does show that, in this project, a single assessor
configuration evaluated once has given unstable labels. So whether this grader gives stable
results across runs is an open question the scope statement should name, not a default it can
assume. With the assumption dropped, "establishes" falls to "was observed once".

## 4. Is the evidence level honest?

`unknown` is wrong for the positive half of the statement. "This grader catches these four
classes" is an empirical result: **measured, single run, n = 7**, with per-class n of about 1–2.
The rest of the statement (what it does not establish, and that the benchmark should grow) is a
limitation plus a recommendation, and needs no evidence level. Recording the whole statement as
`unknown` hides that one part of it is a measurement, and a very small one.

## 5. Regimes the author missed

- **Item–grader co-design:** if the items were written or tuned while the grader was being
  developed, the result measures fit to the benchmark, not generalisation (Goodhart's law). The
  statement says nothing about how the items were made. I cannot check this.
- **Within-class variation:** one instance of a class does not cover subtler versions of the same
  class (paraphrased, partial, or combined with another defect). "Grow as new defect classes are
  found" adds classes but does not deepen existing ones, and both are needed.

## What survives

The statement correctly says the result does not extend to all defect classes or to other graders,
and the call to grow the benchmark is sound. It is not a manufactured overclaim. It is a careful
statement with one verb that is too strong.

## Corrected wording (proposed)

> SCOPE: one grader, seven items, one run, about 1–2 items per class. On this run the grader
> flagged the seeded instances of four defect classes. That is evidence it *can* catch each class,
> not an estimate of how often it does: with n = 1 per class, a perfect score is consistent with a
> per-class detection rate as low as 2.5% (exact 95% lower bound, calculated). Specificity is
> [measured on k clean controls | unmeasured]. Variation between runs is unmeasured. Nothing here
> extends to other classes or other graders. The benchmark should grow in depth (more instances per
> class, clean controls, repeated runs) as well as in breadth (new classes).

```swarm-challenge
{"claim_id": 223, "outcome": "weakened", "reason": "The exclusions are correct, but 'establishes that this grader catches these four defect classes' turns about 1-2 seeded instances per class in a single run into a class-level detection claim, with no specificity or run-to-run variation measured, and records a measured n=7 result as evidence level 'unknown'.",
  "corrected_value": "caught the seeded instances of 4 classes on 1 run (n=7, ~1-2 per class); per-class detection rate exact 95% lower bound 0.025 at n=1, 0.158 at n=2 (calculated); specificity and run-to-run variation unknown",
  "depends_on": ["claim text: 7 items, 4 defect classes, 1 run, 1 grader", "Clopper-Pearson exact bound for k=n: 0.025^(1/n)", "assumption: items are split across the 4 classes with none counted twice (benchmark could-not-access)", "findings/README-third-assessor.md kappa 0.369 (supporting context only, different instrument)"]}
```
