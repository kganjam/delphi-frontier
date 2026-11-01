# Organ- and organism-scale simulations (claude-organ, 2026-11-01)

Every result here is **simulated, not observed**. Nothing was printed, thrown, swum or measured. Each run writes
`artifacts/organ-sims/<run>/manifest.json`. A manifest holds the command, input SHA-256s, the SHA-256 of every
`engineering/organ_sims/*.py` file at run time, the git HEAD and dirty paths, seeds, the checks with pass/fail, and
figures. A run exits non-zero if any gated check fails. Local runs used `systemd-run` caps; no GPU jobs were needed.
Code: `engineering/organ_sims/`. Logs: `artifacts/organ-sims/logs/`.

| Run | Question | Exit | Checks |
|---|---|---|---|
| R1 `r1-v3b-convergence` | Why does v3b's VLM CL not converge? | 0 (report run 2; run 1 exited 3, see R1) | 18/18 |
| R2 `r2-glide-sweep` | Wing area, AR and placement vs launch-glide range, under printed-mass constraints | 0 | 8/8 |
| R3 `r3-underwater-drag` | Underwater drag of the same bodies, fins spread vs folded | 0 | 13/13 |
| R4 `r4-aeroelastic-stiffness` | Fin bending over the sourced fin-ray stiffness range | 0 | 6/6 |
| R5 `r5-school-launch` | Collective launch in PyBullet (6-DOF, contacts, wake coupling) | 0 (run 2; run 1 exited 3, see R5) | 8/8 |

## Project scales and what each run does NOT establish

`artifacts/organ-sims/index.json` (written by `engineering/organ_sims/index.py`) holds one card per run with its
project scale(s), its "does not establish" statement, the check tally and the manifest hash. The cards cover:

| Run | Scales | Does not establish |
|---|---|---|
| R1 | organ | Fin loads, flight or biology. Inviscid lattice convergence only. |
| R2 | organism, organ | Any achieved range, or hand-launch feasibility. |
| R3 | organism | Drag at the target Re, or swimming and taxiing. |
| R4 | organ, tissue | Flying-fish fin stiffness (the source is bluegill), twist, or membrane mechanics. |
| R5 | **collective**, organism | Any schooling behaviour. Rigid gliders, assumed dispersion, no control. Population and behaviour layers are ff-eco's. |

## R1. v3b non-convergence is a lattice defect, plus a pose that is mostly negative twist

**Diagnosis.** `engineering/cfd3d/vlm.py::lattice` places each collocation point on the outline chord at mid-span.
The bound vortex sits on the chords at the panel's span edges. Where the outline curves, the collocation point
leaves its own panel. It lands up to about 2 chords **upstream of its own bound vortex** at 24 chordwise panels
(170–220 points per lattice; the red points in `ladder2.png`).

The error grows as chordwise panels shrink, so **every** variant drifts with chordwise refinement under the committed
lattice:

| Variant | CL at ns 24, nc 8 / 16 / 24 |
|---|---|
| v3a | 0.250 / 0.238 / 0.217 |
| v3c | 0.253 / 0.238 / 0.228 |
| v3b (source normals) | 0.161 / 0.276 / 0.328 |

v3a and v3c only *looked* converged because the committed ladder refined span and chord together, and the errors
partly cancelled. v3b's cambered normals sample the displaced points differently at each lattice, so it diverged
visibly (26%).

**Fix tested.** Put the collocation point at the bilinear 3/4-chord point of the panel's own corners
(`r1_v3b_convergence.lattice_consistent`; `vlm.py` itself is unchanged). With that:
- For the planar v3a and v3c, CL is independent of the chordwise panel count to 3e-5. For v3b's twisted surface,
  CL changes 6% from nc 8 to 16 and 0.4% from nc 16 to 24, so v3b needs ≥ 16 chordwise panels.
- CL changes by ≤0.45% (48×16 → 72×24) between the last two diagonal lattices for all three variants.
- The committed v3a and v3c CL values move <1% (v3c: 0.2511 → 0.2494 at 72×24; v3a 0.2477), so their downstream uses stand.

**v3b's true number.** CL(4°) = 0.162 and CL(0°) = −0.065 (72×24; the committed lattice gave 0.161 → 0.208 → 0.246 → 0.182 along the same ladder), vs 0.229 for the same planform flat.

Fitting the pose surface (`v3b_pose_decomposition` in the manifest) shows it is mostly not aerofoil camber. The
"pectoral_camber 0.06" knob is applied *along each ray*, and the rays fan backward. The result is a trailing-edge-up
chord slope that grows from +0.5° at the root to +12.5° at the tip: geometric washout. True chordwise camber is only
2–6% (argon review #3).

- **Design change:** apply camber across the rays (chordwise), or flip its sign outboard, or add about +5° root
  incidence. Otherwise the v3b pose loses about 30% of the lift at 4°. Patch `vlm.lattice` upstream: a one-line
  collocation fix that the other users of the VLM should adopt.
- **Constraints violated:** none from printing (the pose is a deployment knob). Biologically, the camber value is
  "assumed (Park & Choi 2010 not readable)" in the candidate, so the sign and placement are not sourced either way.

**Run record.**
- The 72×24 lattices ran only for the corrected lattice with source normals and for the committed lattice with
  source normals. The flat-normal 72×24 rows were dropped after the first ladder run hit its 30-minute cap.
- Report run 1 exited 3 on two gates:
  - The planar pose-decomposition tolerance of 1e-6 was below the 1e-7 m storage precision of the input. It is now
    1e-3° and 1e-4.
  - The "max/min over nc 8–24 ≤ 1%" convergence criterion fails for v3b. That failure is real, and it is now
    recorded as a finding (the nc = 8 under-resolution). The gate is now the last refinement step in each direction.
- The run-1 log is kept as `logs/r1-report2-run1-exit3.log`.

## R2. Wing area, AR and placement sweep (point-mass glide, printed masses)

- **Grid:** 8,820 configurations: pectoral area 0.6–1.8×, whole-wing AR 0.7–1.4×, root shift −4 to +24 mm,
  CLmax 0.6/0.8/1.0, V0 4/6/8 m/s, release 0°/10°, and a low-Re profile-drag penalty of 0 or +0.02.
- **Inputs:** r3-daane printed part masses (identical to r4-printfix), with ballast to CG = NP − 8% MAC.
- **Controls:** the repo's 26.07 g trimmed mass within 2.5%; dry mass exact; ballistic range exact (this control
  was broken in the predecessor draft, which passed CL = 0 and got an infinite stall speed; fixed); dt convergence;
  energy bound.

**Results.**

| V0 (CLmax 0.8) | Baseline r3 range | Best range meeting every hard constraint |
|---|---|---|
| 4 m/s | 2.55 m | 2.82 m |
| 6 m/s | 4.68 m | 5.82 m |
| 8 m/s | 10.6 m | 16.1 m |

The best feasible designs always use pectoral area 1.4–1.8×, AR 0.7–0.85× and the root moved 4 mm aft. They sit at
the **115 mm print-length limit** (L_fin 111–114 mm) and CG ≈ 57.9 mm, near the 60 mm window edge. The design is
unchanged under the +0.02 CD0 penalty.

- **Design change:** broader, lower-AR pectorals at the maximum printable length, root 4 mm aft.
- **Constraints violated:** none of the hard constraints (bay, CG window, slot clearance, print length, biological
  band) for that design. Separately, **every** configuration (8,820/8,820) fails the soft hand-launch rule of thumb (V_trim ≤ 8 m/s at CL 0.5). The unconstrained optimum (up to 32 m) breaks the
  print length, the CG window and the biological pectoral/SL band (0.584–0.77).
- **Caveat (argon #2):** fixed-CL point-mass ranges at V0 ≥ 6 m/s include a zoom-climb phugoid. Range can even rise
  slightly with more drag, which is a phase artifact. Read the ranges as ±20%; the design *ranking* is robust. The
  6-DOF model in R5 flies the assembled glider at its *trim* CL (0.24 at the assembled pelvic key), not 0.8. It
  reaches 5.2 m at V0 8 m/s, against R2's 10.6 m. The two models disagree by about 2×, and R5 is the more physical.
- **Not done (argon #4):** the 0.85× NP-shift rule is linear. A two-surface NP inside the sweep is the next step.

## R3. Underwater drag of the same bodies

Component build-up from the committed STLs: N1, v3a, v3b, v3c and the r4 print, plus R2's 1.8× pectoral. Each
surface uses its own Re. Friction is a band of laminar Blasius / Prandtl–Schlichting / ITTC-57; the body uses a
Hoerner form factor. Wave drag, undulation and separation are excluded (deep-water rigid body only).

**Results at 10 m/s (transitional law):**

| Body | Fins spread | Fins folded |
|---|---|---|
| v3a | 3.85 N | 3.19 N |
| v3c | 4.15 N | 3.33 N |
| r4 print | 3.72 N | 2.91 N |
| R2 1.8× fin | 4.50 N | 3.30 N |

- Fins carry 57–64% of the drag when spread (68–74% at 5 m/s). Folding saves 17–27% at 10 m/s (21–31% at 5 m/s).
- **R2's bigger fins cost +21% drag spread and +13% folded.**
- 10 m/s rigid needs about 40 W, roughly 1,500 W/kg body. That is far above any plausible muscle power density, so
  the printed glider is not a swimmer: launch it by band.
- **Strength:** a printed pectoral spread under water at only 1–2° misalignment reaches half its UTS (43 MPa) at
  **2.2–3.1 m/s**.
- **Design change:** keep the fins folded (or detachable) for any water contact. The underwater penalty of R2's
  bigger fins is real but second-order once folded.
- **Constraints violated:** spread printed fins exceed half-UTS above 3 m/s in water. The Re 1000 WaterLily
  comparison (CFD/build-up 0.66) is a consistency check only: it is 1600× below the target Re, and the CFD sphere
  gate failed.

## R4. Fin bending over the sourced fin-ray stiffness range

**Setup.** The committed two-way static model (VLM + constant-EI cantilever, torsion-rigid; v3a fins), on the
corrected lattice. The rigid CL moves only 0.5% from the lattice change.

**Stiffness source.** Alben, Madden & Lauder 2007 §3.4: bluegill pectoral rays, three-point bending, EI ≈ 1e-6 to
1e-5 N·m². This was read in `aeroelastic-sources/alben2007.txt`. Whole-fin EI = 15 rays × ray EI, which is an
upper bound.

**Critical EI** (below it, the tip leaves the linear domain at tip/span 0.1):

| Speed | Critical EI |
|---|---|
| 8 m/s | 3.2e-4 N·m² |
| 12 m/s | 5.6e-4 N·m² |
| 16 m/s | 1.0e-3 N·m² |
| 20 m/s | 1.8e-3 N·m² |

**How the bands compare:**
- **Sourced band (1.5e-5 to 1.5e-4):** below critical at every speed. With bluegill-stiff rays at flying-fish size, the
  fin's tip deflection would exceed the linear-beam domain (tip/span > 0.1) at glide loads. That means large
  deflection outside the model, not a computed collapse.
- **Same band with 10× active stiffening (abstract of the source):** reaches 1.5e-3, which covers ≤ 16 m/s.
- **Isometric size scaling (scenario):** 3.7e-4 to 3.7e-3.
- **Printed r4 section (Alpha Grey, E 2.08 GPa):** 2.9e-3 at the tip and 7.4e-3 at the root. That is 9–23× above
  critical at 8 m/s, with bending lift loss ≤ 0.3% and cruise root stress 0.4 MPa vs 43 MPa UTS.

- **Design change:** for the print, the fins are 10–20× stiffer than flight loads need. The spar and ridges could
  be thinned to cut mass, which R2 shows is the binding constraint. Launch loads (≈1000 m/s² in-plane, in
  `print-requirements.json`) and the R3 water loads set the real floor. Do not thin before checking those.
- **Biology (model-conditional):** *within this torsion-rigid linear model*, a fin would need roughly 10× the
  bluegill-ray EI at the same ray count to stay in the small-deflection regime at 16–20 m/s. This is a hypothesis
  for measurement, not an established property of flying-fish fins.
- **Constraints:** none violated for the print. The sourced-biology band is outside the model's linear domain.
- **Limitation (argon #1):** the model is torsion-rigid. Constraint torsion is 29% of root bending (committed
  review), and twist or washout could change CL by far more than bending does. The <1% CL loss is a bending-only
  lower bound.

## R5. Collective launch in PyBullet

**Model.**
- 8 rigid 6-DOF printed gliders with the r4 computed mass and inertia, plus ballast to the R2 trim rule.
- Quasi-steady aero per surface: pectorals and pelvics from the flight model; dorsal, anal and caudal from v3a
  STLs. Forces act at the quarter chord, with velocity taken at the 3/4-chord point.
- Pectoral downwash on the pelvics, the Munk moment, and ground effect.
- Inter-fish wake: each fish is a horseshoe with Γ = L/(ρVb′) and a cored Biot–Savart term (argon #5/#7/#8).

**Controls.** Ballistic range matches PyBullet exactly. A symmetric launch stays symmetric. Widely spaced fish
behave like a single fish. Moving the CG behind the NP destabilises pitch. Wake coupling at 2 m is negligible.

**Trim (a finding in itself).**
- The 6-DOF static margin at the assembled pelvic key (dec+2) is 0.097 MAC. That agrees with R2's 0.08 rule.
- That key trims at **CL 0.24** (L/D 5.5).
- Only the highest printed key, **dec+4**, trims near best L/D: CL 0.55, L/D 9.6. Single-glider range at 8 m/s
  goes from 5.23 m to 6.38 m (+22%).
- **Design change:** assemble with pelvic key dec+4, or print a dec+5/+6 key.

**School results.**

Values are fractions of 8-fish launches with at least one mid-air contact (8 seeds each). "Lane drift" is the RMS
landing deviation from each fish's own lane.

| Spacing | Small spread, wake on | Small spread, no wake | Large spread, wake on | Large spread, no wake |
|---|---|---|---|---|
| 0.25 m | 0.88 | 0.88 | 0.88 | 0.75 |
| 0.30 m | 0.63 | 0.63 | 0.63 | 0.63 |
| 0.40 m | 0.13 | 0.13 | 0.25 | 0.25 |
| 0.60 m | 0.00 | 0.00 | 0.13 | 0.25 |

- **Mean range:** 6.1 m with the small spread, 5.7 m with the large one.
- **Range spread within a launch:** 3.4 m (small) and 5.3 m (large).
- **Lane drift:** 0.36–0.39 m RMS (small) and 0.72–0.77 m RMS (large).
- **Contacts:** at ≤ 0.30 m spacing they roll fish past 90°.
- **Wake coupling** changes contact rates by at most one launch in eight. Collisions are set by release dispersion,
  not aerodynamics.
- **First run exited 3.** It failed check C3: with the wake on, fish 2 m apart shifted each other's range by
  1e-4 m, against a tolerance of 1e-6 m. C3 now tests rigid-body independence with the wake off; C6 bounds the
  wake separately. The run-1 log and manifest are kept as `logs/r5-run1-exit3.*`.

- **Design change:** for a side-by-side collective release, keep lanes ≥ 0.6 m apart (≈2.7 wingspans) with launch spread at the 'small' level, or ≥ 1 m with the 'large' level. Pitch-rate control at release matters more than spacing: lane drift scales with dispersion, not with the wake. Pelvic key dec+4.
- **Constraints violated:** a launcher holding 8 lanes at 0.6 m is 4.2 m wide, far beyond a hand or slingshot rig, so a practical collective launch needs a staggered release (not simulated). Biologically, real flying fish do not hold lanes and steer; this run has no sensing or control, so it does not establish anything about schooling behaviour. That layer is ff-eco's.
- **Not modelled:** unsteady wakes, the band and hook stroke, splash.
- **Dispersion is an assumed scenario:** no launch has been measured.

## LLM review

`gemini-4-argon` critiqued all five runs (prompt and answer in `artifacts/organ-sims/review/`).

**Changed in response:**
- #2: low-Re CD0 penalty scenario in R2.
- #3: v3b pose decomposed into chord slope and camber.
- #5: 3/4-chord velocity for each surface's own damping.
- #6: R3 water-strength check, and the Re 1000 comparison demoted.
- #7: inter-fish horseshoe wake coupling.
- #8: ground effect in R5.

**Kept as stated limitations:**
- #1: torsion.
- #4: two-surface NP inside the R2 sweep.

**Not adopted:**
- Deleting the Re 1000 comparison. It is kept but labelled "consistency only".
- Replacing the bluegill source with unread flying-fish papers. The brief asks for the sourced range, and R4's
  finding is precisely that this range is insufficient.

A quick overclaim check with `gemini-3.8-flash` flagged four sentences. All four were reworded: the R4 biology
claim, R4's "would fold", R3's fold-saving range, and the R2 hard-vs-soft constraint wording. Prompt and answer are in
`artifacts/organ-sims/review/flash-*`.
