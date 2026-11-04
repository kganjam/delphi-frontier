# Challenge 194 — "a possibly detectable 5–10 % reduction in ascent deceleration"

**Claim under review** (S28-organism.md, §3.6 and swarm-result; branch `claude/s28-organism-design-5z0vjz` @ e8ba4191):
"THE DELIVERABLE: a falsifiable small aerodynamic phenotype — a possibly detectable 5–10 % reduction in ascent
deceleration — in an animal that ALREADY EXISTS."
Recorded evidence level: derived.

**Verdict: WEAKENED.** The 5–10 % figure is the wing's *lift-to-weight ratio* (10 % at water exit, 5 % at apex). It is not the
reduction in ascent deceleration. I recomputed the deceleration itself. Under the author's own most generous inputs it is
**≈ 4.5–4.9 %**, and under the other inputs it is lower. So the corrected figure sits *below* the claimed range, not inside it.

Every number in this document is **derived** (a calculation or simulation on the author's stated inputs). None is a measurement.
Reproduce: `python3 docs/research/fish/challenge-194-scripts/c194.py`.

## Sources and read-levels
- S28-organism.md and S28_organism.py (project files): **full-text**.
- Miln et al. 2021 (burst speed 0.45–1.38 m/s) and Daane et al. 2021, Curr. Biol. 31:5052: **listing**. I know them only as
  S28 cites them. I did not access either paper, so I have not checked the allele names, the fin-length values or the
  burst-speed range. S28 itself states that it did not read the numeric values of Daane Fig. 4B.

## 1. Independent arithmetic
I wrote my own point-mass integrator (`c194.py`) and did not reuse S28's `traj()`. It uses S28's stated inputs: m = 0.25 g,
span 31 mm, CL 1.07 held constant, Oswald e = 0.8, CD0 0.08–0.20, body drag CD 0.3 on 24 mm², and fin areas A/B/C = 57/125/192 mm².
WT (fins folded) and mutant (fins spread) are compared at the **same** launch angle and exit speed. The program integrates
the ascent until v_y = 0 and reports three quantities:
- **mean ascent deceleration** = v_y0 / t_ascent;
- a **quadratic-fit vertical acceleration** to y(t), which is what a video analysis would actually estimate;
- **apex height**.

The lift ratios check out. My recomputation gives L/W = 0.098 at exit and 0.045 at apex (case C, 1.38 m/s, 45°), matching
S28's 10 % and 5 %.

Reduction in ascent deceleration vs WT (derived, simulation):

| Exit speed | Launch | Case C (192 mm²) | Case B (125 mm²) | Case A (57 mm²) |
|---|---|---|---|---|
| 1.38 m/s | 45° | **4.5–4.9 %** | 3.1–3.3 % | 1.4–1.6 % |
| 1.38 m/s | 60° | 2.2–2.6 % | 1.6–1.8 % | 0.8–0.9 % |
| 1.38 m/s | 80° | −0.1 to +0.3 % | 0.0–0.3 % | 0.0–0.2 % |
| 0.90 m/s | 45° | 2.0–2.1 % | 1.3–1.4 % | 0.6–0.7 % |
| 0.45 m/s | 45° | 0.5 % | 0.3–0.4 % | 0.2 % |

(Each range spans CD0 0.08–0.20. The quadratic-fit acceleration agrees with the mean deceleration to within 0.1 percentage point.)

## 2. Proxy
- **The proxy is L/W**, the lift-to-weight ratio, standing in for the reduction in vertical deceleration.
- **What actually reduces vertical deceleration** is the vertical component of the aerodynamic force, (L cos γ − D_wing sin γ)/W,
  where γ is the flight-path angle.
  - At a 45° exit, cos γ = 0.71, so only 7 % of the 10 % lift acts against gravity.
  - Wing drag removes about a further 1 %.
  - Lift then decays as V² towards the apex.
- **The time-average over the ascent** is therefore ≈ 5 %, not 5–10 %. The upper half of the claimed range (6–10 %) does not
  occur anywhere in the parameter space I tested (the table above).

## 3. Hidden assumptions, relaxed
These are my inferences, drawn from the table:
- **Fin area (case C).** S28 itself labels case C as extrapolated and unmeasured. Case B gives ~3 % and case A ~1.5 %.
- **Launch angle 45°.** The effect falls quickly for steeper exits: ~2.4 % at 60° and ~0 at 80°, because cos γ → 0.
  The actual leap angles of zebrafish are `unknown` to me; I found none in S28's inputs.
- **Exit speed = maximum burst (1.38 m/s).** At mid-range speeds (0.9 m/s) the effect is ≤ 2.1 %. At the low end it is ≤ 0.5 %.
  The claim's range applies only to the fastest fish in the cited dataset.
- **Fins held spread at CL_max = 1.07 for the whole ascent.** S28 already flags this as generous and unobserved. I have not relaxed
  it further, so the numbers above remain upper bounds.

## 4. Evidence level
- **"Derived" is honest.** S28 does not present this number as measured.
- **However, the number is mislabelled within the derived level.** It is presented as an ascent-deceleration figure, but it is
  a lift-ratio figure. That is a quantity substitution, not an overclaim of evidence level.
- **"Possibly detectable" is not supported by any calculation in S28.** The claimed 5–10 % reduction would show up as a vertical
  displacement difference of ≈ ½·(0.05·g)·t² ≈ 2.7 mm over the ~0.1 s ascent (my derived estimate, case C). Whether video can
  resolve this against leap-to-leap variance in exit speed and angle is `unknown`; no variance data were among the inputs.

## 5. Counter-examples and missed regimes
- **Apex height.** S28 reports "apex unchanged or lower" (4.75–4.84 cm). That figure is at the *range-optimised* launch angle.
  At a matched 45° launch, my integrator gives the apex **+4.9 to +5.4 %** higher (case C).
  - This is not a contradiction: the optimiser picks a shallower angle.
  - It does mean that apex height measured at a matched angle is a direct observable of the same effect.
- **Published counter-examples.** I did not search the literature for zebrafish leap kinematics. That negative is scoped to this
  document: I ran no web or database search.
- **"Already exists."** This part rests on Daane 2021 at listing level only. I could not verify it, and I have not refuted it.

## Corrected statement
A derived (calculation-only) upper bound of **≈ 5 % (4.5–4.9 %) mean reduction in vertical ascent deceleration**. It applies to a
1.38 m/s, 45° exit with the unmeasured AR-5 fin held at CL 1.07. It falls to ≈ 1.5–3 % for the length-only and isometric fin
areas, ≤ 2.6 % for steeper (≥ 60°) exits, and ≤ 0.5 % at the slow end of the cited burst range. Whether it is detectable has
not been calculated.

```swarm-challenge
{"claim_id": 194, "outcome": "weakened", "reason": "The 5-10% figure is the lift-to-weight ratio at exit/apex, not the ascent-deceleration reduction; integrating the vertical force component over the ascent gives at most ~4.5-4.9% (case C, 1.38 m/s, 45 deg) and 0-3% under the other stated fin areas, angles and speeds.", "corrected_value": "<=4.9% mean vertical ascent-deceleration reduction (upper bound; 1.4-4.9% across fin cases A-C at 1.38 m/s, 45 deg; <=0.5% at 0.45 m/s)", "depends_on": ["S28 inputs: m=0.25 g, span 31 mm, CL 1.07, e=0.8, CD0 0.08-0.20", "S28 fin-area cases A/B/C (57/125/192 mm2, unmeasured)", "Miln2021-burst 0.45-1.38 m/s (listing only)", "Daane2021-genetics (listing only)", "launch angle 45-80 deg (assumed; zebrafish leap angle unknown)"]}
```
