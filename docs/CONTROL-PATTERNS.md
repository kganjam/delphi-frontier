# What the controls caught, and what each one looked like

Every row below is a real failure from a single session (2026-11-04/05) on this repository.
Each would have produced a confident, plausible, **wrong** result. Each was caught by a control
that took a few lines. None was caught by reading the code.

The entries are ordered by how hard they were to see.

| # | The failure | What it would have reported | The control that caught it |
|---|---|---|---|
| 1 | `fetch_fulltext.py` took `<body>` and dropped `<floats-group>`, where JATS keeps every figure and caption | "0 values in 368k characters" — read as a fact about the papers | A **must-find** arm: a passage known to contain a value must yield one |
| 2 | Extraction quote-check guarded against fabrication but not vacuity | An extractor replying `{"values": []}` to everything passed every check | A **synthetic positive** control — one written sentence that must be extracted |
| 3 | `corpus_gap.py` classified papers by one-line descriptions containing none of the lexicon words | "genetics UNCOVERED" on a genetics-heavy corpus, **with all four controls passing** | A **must-NOT-flag** arm beside the must-flag one |
| 4 | Energy metric used air-relative speed in a wind | A leaf stationary in 12 m/s wind scores 7.3 m of "energy" | Asking what the metric returns for a thing that is **doing nothing** |
| 5 | Wingless control set `CL=0`, but drag was `L/(L/D)`, so drag vanished too | A vacuum projectile "proving" that lift caused the energy gain | Making drag an **independent coefficient** so the control can fail |
| 6 | Criterion declared in the docstring was never implemented in the code | "The soaring cycle closes" — while every trajectory ended in the water | Printing **why** a test failed, not just whether |
| 7 | Euler integrator gained energy at zero shear | A real gain, four orders of magnitude smaller than the claimed one | **Convergence test**: halve `dt`, see whether the artifact halves |

## The three patterns underneath

**A guard against one failure is silent about its opposite.** #2 and #3 are the same shape: a
check that catches fabrication says nothing about vacuity, and a must-flag arm is satisfied by a
checker that flags everything. **Every control needs a case it must flag and a case it must
not.** Three of the seven above passed their own happy path.

**A control that cannot fail is not a control.** #5 is the sharpest: the wingless arm looked
decisive and was structurally incapable of showing advection, because zeroing lift also zeroed
drag. Before trusting a control, ask what would have to be true for it to fail, and check that
that state is reachable.

**Prose drifts from the numbers beside it; generated text does not.** In the same session, five
hand-written summary paragraphs contradicted the generated tables directly beneath them, and the
table was right every time. The fix was not more care — it was generating the summary from the
same source as the body (`swarm/design_spec.py`). The first time it mattered, a route closure was
withdrawn and the headline count followed without anyone touching it.

## What this does not claim

These are seven instances from one session on one repository. They are not a survey, and the
ordering reflects how hard they were to notice here rather than how common they are anywhere.
What is measured is narrow and real: in this session, **every number fetched from the claim graph
was correct, and five of five summaries composed by hand were wrong.**
