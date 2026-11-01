# Pre-outcome addendum to the frozen horizon protocol `7afb713`

Written **before any horizon outcome exists**, at the admission review's requirement. The
frozen protocol itself is **not edited** — it stands as frozen, with its history. This file
narrows two claims its rationale made more broadly than the evidence supports.

## 1. The middle J columns: "cannot set the statistic" was too strong

The protocol justifies selecting only the lowest and highest J column per gap by saying the
middle columns "cannot set the statistic under test". That is true **of the old, fixed-horizon
extrema, and only of them**.

Precisely what holds: at StopTime 1000, the minimum feasible spread
`max(lo/J) / min(hi/J)` was set by J=35 and J=560 at both gaps. Nothing in the middle columns
entered that number **as measured at that horizon**.

What does **not** hold: that the middle columns are irrelevant at longer horizons. A longer
horizon moves brackets **up**, and it can move a middle column's bracket further than it moves
either extreme. If that happened, a middle column could become the new argmax or argmin and set
the spread. **This study does not test that**, and a result from it must not be read as showing
the middle columns stay irrelevant. They are **untested at longer horizons**, which is a gap in
coverage, not a demonstrated absence of effect.

The selection remains the right first probe — it targets the columns that currently set the
statistic, in both directions — but its scope claim is the narrower one above.

## 2. The negative control cannot establish "arrest fragile everywhere"

The protocol's negative control says that if the deep-arrested arm (λ_V = 12.8) closes, "arrest
is horizon-fragile everywhere and no bracket in the study is interpretable."

The second half is a sound operating rule and is kept: a deep-arrested arm closing would
undermine the arrested classification this study rests on, so refusing to interpret is correct.

The first half overstates. There are **two** negative controls, one per gap, each at a single
(gap, J, seed, λ_V) condition. A failure in one condition establishes that arrest is fragile
**in that condition**. It does not establish anything "everywhere" — not across gaps, not
across J, not across seeds, and not at λ_V values other than the one tested. The analyzer
reports a failed control as **UNINTERPRETABLE**, which is the right action, and this addendum
is what the word in the protocol should have said.

## 3. What this addendum does not change

- No threshold, bound, arm, horizon or criterion is altered.
- The frozen protocol `7afb713` keeps its text and its history.
- The 240-arm FAIL, the 36-run records, every earlier protocol and result, and the `dff5e58`
  publication bundle are untouched.
- No outcome exists for this study yet, and none is anticipated here.

## 4. Record of the implementation repair this accompanies

The admission review demonstrated a **false pass**: the packet at archive `9b9c0895` /
source `3b1f17b`, run against the real 1000-only native logs, returned rc0 and
*"SUPPORTED at these horizons"* while all 30 arms falsely marked horizon 8000 as observed.
Reproduced here before repair; the evidence is frozen at
`artifacts/epithelial/fixtures/truncated-1000-only/` and the regression that rejects it is
control H5. The repair is described in the commit that carries it, and the five required items
are implemented and fixture-tested at 36/36.
