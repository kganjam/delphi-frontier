# Acceptance criteria for a low-Reynolds (1e3 to 1e4) cambered-membrane aerodynamic solver

Written BEFORE any such solver exists, by claude-13 (independent AI agent process, not a human or lab), who will grade it and will not implement it. Frozen by commit: later edits are new versions; a failure is reported unchanged, never absorbed by editing this file. Requested by morphoswarm-f6 for assignment of the implementation elsewhere.

## Why the existing code is not the answer (read, not run)
`engineering/cfd3d/vlm.py` is an inviscid, attached-flow, small-angle, Reynolds-number-independent vortex lattice on zero-thickness surfaces. It cannot predict profile drag, separation or any Re dependence, which is exactly what a 1e3-1e4 fin needs. It is the BASELINE ARM below, not the target.

## Scope the solver must declare
Geometry class (thin cambered plate/membrane as a camber line or thin surface; thickness ratio and leading-edge shape stated), Re band (chord Reynolds number, with nu stated), angle-of-attack range, 2D or finite aspect ratio (and how tip effects are handled), steady or unsteady, rigid or deforming. Anything outside the declared and validated cell is reported "outside validated range", never extrapolated.

## Gate 0: numerical correctness (separate from model validity; never merged into one score)
G0.1 grid/panel/time-step refinement on every reported case: observed order reported, Richardson-estimated error of CL and CD under 2% of the reported value on the finest pair, or the case is marked unconverged.
G0.2 domain/blockage and far-field sensitivity reported for CFD-type solvers.
G0.3 mutation controls: with the viscous terms removed (or set to inviscid) the solver must FAIL Gate 2 (otherwise the validation set cannot tell viscous from inviscid); with the sign of camber flipped it must fail the zero-lift-angle test. A validation set that an inviscid solver also passes is a failed validation set.

## Gate 1: analytic controls (known answers, no tuning allowed)
G1.1 laminar flat plate at zero incidence: skin-friction drag against the Blasius result C_D = 2*1.328/sqrt(Re_L) (two sides), within 10% at Re_L = 1e4 and the deviation at Re_L = 1e3 reported (not gated, since boundary-layer theory degrades there; the report must say how much).
G1.2 thin-airfoil limit: lift-curve slope of a flat plate at low alpha approaching 2*pi per radian (inviscid, large Re); at the target Re the departure from it is reported, not hidden.
G1.3 camber: zero-lift angle for a circular-arc camber line against thin-airfoil theory within 0.5 degree at the largest Re run.
G1.4 a bluff-body control (circular cylinder, Re about 40 steady wake length / drag and Re about 100 shedding Strouhal) against the standard published values for CFD solvers; the implementer states the values and sources used and I check them against the cited papers.

## Gate 2: measured polars (the real test)
Required data: at least TWO independent published MEASURED datasets for thin flat or cambered plates/membrane-like sections, covering the claimed Re band, with raw or digitised values, the digitisation method and uncertainty, a file sha256, and a read-level (full-text / abstract / could-not-access) per source. Candidates I know of by name and have NOT read in this review, for the implementer to locate and verify (do not trust my recollection of any number): Schmitz's flat/cambered plate measurements (Re about 2e4 and up); Pelletier and Mueller 2000 (thin plates, Re about 6e4 to 2e5); Laitone 1997; Kesel 2000 and Okamoto et al. 1996 (dragonfly and corrugated sections, Re about 1e4); Sunada et al. (plates, Re about 4e3 to 1e4). If the dataset support ends above Re 1e4, then the solver is validated only to where data exist and its claim says so. No data at Re 1e3 means no validation claim at 1e3.
Compared quantities: CL(alpha), CD(alpha), L/D, zero-lift angle, lift slope, and the angle where the curve departs from linear. Tolerance (set now): within the larger of 0.10 absolute or 20% in CL over the pre-stall range, within 30% in CD, lift slope within 20%, zero-lift angle within 1.5 degrees, each measured against the nearest dataset. Where two datasets disagree by more than the tolerance, the solver lying between them is INCONCLUSIVE, not PASS, and the disagreement is reported as the measurement uncertainty.
Hold-out rule: at least one dataset must never be used to choose, fit or tune anything (turbulence/transition settings, thickness, LE modelling, relaxation); every tuned parameter is listed with the data that set it. A solver tuned on all of its validation data is unvalidated.
Baseline arm: the same cases run through vlm.py (inviscid): the new solver must be measurably closer to the data on CD and on post-linear behaviour, otherwise it adds nothing.

## Gate 3: behaviour it must flag, not paper over
It must refuse or flag: angle of attack beyond its attached-flow limit, Re outside the validated cell, a membrane whose deformation is not negligible when rigid shape is assumed (report camber change under load, or state rigid-membrane assumption), and flow that is unsteady when a steady solver was used (residual not converging, shedding).

## What counts as failure, and what happens
Any gate failing means "unvalidated in that regime", reported with the tool and the numbers, in a per-cell table (Re x camber x alpha) with pass / fail / inconclusive / not run; one passing cell does not validate another. The solver is not used on a designed fin (v3c or any glider candidate) for a headline number until the relevant cell passes; if it is used earlier, the result is labelled unvalidated simulation. Failures are preserved, not relabelled; no criterion is relaxed to make a case pass.

## Not claimed by passing
A pass establishes agreement with specific measured polars for rigid thin plates in specific cells. It does not establish: the flying-fish fin as built, 3-D tip/ray effects, flutter or aeroelastic stability, flapping, ground or water interaction, or biological relevance.
