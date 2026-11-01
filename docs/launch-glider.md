# Launchable fish glider: dynamics, trim and launch (SPEC-010, claude-07)

Status: **protocol draft, not frozen.** Nothing here is calibrated, measured on a print, or flight-tested.
The protocol is frozen, and its hash sent to infra and to the independent reviewer, once two inputs exist:
claude-05's first `flight_model.json`, and cfd04's VLM table for it. Until then, every result is labelled
*placeholder geometry* and *nominal scenario coefficients*.

Owners (SPEC-010):
- claude-05: geometry, manufacturing and mass properties.
- claude-07 (this package): dynamics, trim and launch.
- claude-04: aerodynamic controls (VLM).
- root: materials and integration.

Independent review is a separate assignment (`launchable-fish-review`).

## Code (`engineering/launch_glider/`)
| module | what it does |
|---|---|
| `print_requirements.py` | Conservative fin-root, spar, doubler and hook sizing. It also gives the mass budget, a hand NP bracket and the CG window. |
| `mass_props.py` | Exact polyhedral mass, CG and inertia for closed solids and thin sheets, plus parallel-axis combination. It recomputes claude-05's STLs independently. |
| `dynamics.py` | Batched pitch-plane rigid body: slingshot stroke, then free flight to first ground contact. Also scenario aero, trim, and Jacobian modes. |
| `candidate.py` | Placeholder candidate built from the v3a meshes at declared print thicknesses (shell body, membrane fins, R1/R2 spars, R3 hardware, ballast). |
| `sweep.py` | Feasibility map. Every row includes a same-mass, same-CD0, no-lift control that starts from the same release state. |

Reproduce:
- `python -m engineering.launch_glider.print_requirements artifacts/fish3d/fish3d-v3a-fan/panels.json data/materials/formlabs-studio-2026-10-31.json artifacts/launch-glider/print-requirements.json`
- `python -m engineering.launch_glider.sweep artifacts/launch-glider/feasibility-map.json`

Both run single-threaded.

## Frames and units
- SI throughout.
- **Geometry frame** (v3a and claude-05): x aft from the snout, z up.
- **Dynamics:**
  - World X is forward and horizontal, Z is up.
  - Body pitch θ is the nose angle above the horizon; q = dθ/dt, nose-up positive.
  - A body point is (ξ, ζ): ξ ahead of the CG, ζ above it.
- **Coefficients** use S_ref = paired flat fin area (52.93 cm² for v3a) and c_ref = pectoral MAC (26.48 mm).
- Cm is about the manufactured CG.
- Re is computed with ν = 1.5×10⁻⁵ m²/s (declared, about 20 °C).

## Equations
- **Stroke.** The band force acts at the hook and is directed at the fork, a fixed point s ahead along the aimed
  line.
  - Displacement profiles (each has a mean of 1 over displacement, so the mean force is F̄ and a_mean = V0²/2s):

    | profile | shape | peak/mean |
    |---|---|---|
    | constant | 1 | 1 |
    | quarter-cosine | (π/2)·cos(πξ/2s) | π/2 |
    | linear (ideal elastic band) | 2(1 − ξ/s) | 2 |

  - Peaks above 2 (band slack, a jerked pouch) are an **unbounded case, stated and not covered**.
  - F̄ is iterated so that the CG speed at release equals V0.
  - Release is complete at ξ = s.
  - Aero and gravity act throughout the stroke.
- **Flight.** Integrated with RK4 at dt 1 ms (0.1 ms in the stroke). It ends at the first ground contact of any hull
  point (the convex hull of every component vertex in the pitch plane).
- **Aero, scenario model:**
  - attached: CL = CLα(α − α₀) + CL_q·q̂ and CD = CD0 + CL²/(π e AR);
  - separated: flat plate, CL = k·sin 2α and CD = CD0 + 2k·sin²α, blended by a C1 smoothstep over CL_max/CLα ± dα;
  - moment: Cm0 (attached), the normal force at x_np + s·dx_cp_post, the Munk slender-body couple 2·q·Vol·(k₂ − k₁)·sin α·cos α
    (destabilising), and Cm_q·q̂.
  - Cm0 is chosen to trim at the design C_L. Decalage is what sets it on the model, and cfd04's VLM maps one to the
    other.

## Scenario coefficients
Nominal value with its bracket. None is measured for this glider.

| coefficient | nominal [bracket] | source and read level | applicability |
|---|---|---|---|
| CLα | 4.8 [4.4, 5.2] /rad | Helmbold plus a declared downwash; hand estimate | VLM replaces it |
| x_np (fins only) | 60.1 [58.3, 61.9] mm | hand estimate | VLM replaces it; Park & Choi hints it is further aft (below) |
| e | 0.75 [0.6, 0.9] | declared | — |
| CD0 | 0.07 [0.04, 0.12] | declared; laminar Cf build-up about 0.045 at Re 1×10⁴ | Park & Choi CD_min 0.055 on body-inclusive area (≈ 0.08 on paired area) is a comparison only |
| CL_max | 0.7 [0.6, 0.9] | declared | Park & Choi stuffed fish 0.78 at 35°, body-inclusive area, Re 2×10⁴; comparison only |
| dα (stall width) | 2° [1, 4] | declared | thin-airfoil stall is broad (Park & Choi, read in full text) |
| k_post | 0.9 [0.8, 1.0] | declared flat-plate value | — |
| Cm_q | −4.5 [−8, −2] | pelvic tail-volume estimate; declared | cfd04 may compute it (onset field Ω×r) |
| k₂ − k₁ (Munk) | 0.9 [0.8, 0.95] | slender-body value for fineness about 6, recalled | small-α theory; overestimates at large α |
| dx_cp_post | 5.7 [2, 10] mm | paired-fin area centroid minus the hand NP; declared | — |

**Sources:**
- **Park & Choi 2010** (J Exp Biol 213:3269): **full text** read here from the author PDF via r.jina.ai PDF
  extraction. Direct fetch timed out after 60 s. What it is: stuffed *Cypselurus hiraii* in a wind tunnel at 12 m/s,
  Re 1.9–2.2×10⁴, with the reference area including the body. What was read:
  - Table 1: morphometrics; x_CG/SL 0.39–0.47.
  - Table 2: L3 L/D_max 4.37 at α 0°, CL_max 0.78 at 35°, CD_min 0.055.
  - Fig. 6: dCm/dα < 0 with pelvics, > 0 for the body alone.

  These are used only as comparison bounds. They are not a calibrated polar for this glider (SPEC-010 source
  context).
- **Saro-Cortes et al. 2022** (ICB, doi 10.1093/icb/icac101): **abstract only**, via Europe PMC (PMID 35771996).
  The OUP page is behind Cloudflare. Per the abstract, pitch stability is not achievable with positive pelvic pitch
  angles, or with the pelvics directly below the pectorals. That is a trade-off, at Re 3×10⁴.
- **Material:** root's card `data/materials/formlabs-studio-2026-10-31.json` @ `f1796ec`, id
  `alpha-grey-v1-default-post-cure`: 1220 kg/m³, flexural E 2.08 GPa, UTS 43 MPa. These are Form Studio 1 coupon
  data. The TDS was also read here.

## Controls (`tests/test_launch_glider.py`)
- **Closed forms:** the beam (tip deflection, root moment, stress), the section's parallel-axis theorem, in-plane
  root stress, and hook stem sizing.
- **Mass properties:** a box solid (exact), a cube shell, and a sphere shell and solid.
- **Projectile and energy:** the vacuum projectile matches to 10⁻⁶. Energy is conserved to 10⁻⁶ with lift on and
  drag off, because lift does no work.
- **Trim:** the trimmed 3-DOF run reproduces `engineering/simulation/glide.py`'s point-mass range to 10⁻⁶, with tan γ
  = CD/CL.
- **Numerics:** dt halving changes range by < 0.5%, for the dynamics and for a sweep row. expm(J·t) matches the
  nonlinear small-perturbation response within 2%.
- **Stroke:** with a constant force, a = V²/2s and t = 2s/V. The peak/mean ratios are 1, π/2 and 2.
- **Hook attitude:** a hook below the CG holds its equilibrium attitude atan(−ζ/ξ).
- **Munk term:** its slope is exactly +2·Vol·k.

**Retained invalid candidates and mutants:**
- CG behind the NP gives an unstable eigenvalue.
- A hook behind the CG lets the misalignment grow.
- A trim C_L above the attached-branch peak is retained as `TRIM_ABOVE_CL_PEAK`.
- A bare-membrane pectoral fails stress and deflection.
- Hand mutants are each caught: Munk sign, spar side, downwash sign, halved pressure, in-plane arm, band-torque sign,
  moment-arm sign and lift direction.

## Findings so far (placeholder geometry, nominal coefficients)
1. **The release speed is below the trim speed.** The placeholder's dry mass is 11.2 g (0.5 mm body) to 14.7 g
   (0.8 mm body), with the dry CG at x ≈ 72.6–72.9 mm. Trim speed at C_L 0.45 is 9–12 m/s, depending on the NP
   scenario and ballast. SPEC-010's 4, 6 and 8 m/s releases are therefore all below trim.
2. **Range alone is not evidence.** The no-lift control reaches 1.8–7.0 m over the same launches. The headline is
   the glide gain.
3. **The launch transition dominates.** Two effects leave a nose-up pitch rate at release that is sensitive to catch
   height and hook arm: the body swings like a pendulum about the hook, and the CG sags while the band pulls toward
   the fork.
   - The first R3 rule (catch below the CG) is refuted and withdrawn.
   - The catch height and hook arm must be adjustable by test.
4. **The hand NP may be too far forward.** Park & Choi's stable stuffed fish had x_CG/SL 0.39–0.44. The NP is
   therefore a sweep axis (60, 66 and 72 mm), not a value.

## Limits
- Pitch plane only: no roll, yaw, spiral or Dutch roll. Lateral behaviour is reported as static derivatives once
  cfd04 provides β = 5°.
- No ground effect, walls or ceiling; still air.
- The launcher's speed, force profile and alignment are chosen scenarios.
- Membrane torsion is not modelled, nor layer anisotropy, fatigue or impact.
- A scenario distribution is not a probability of physical success (SPEC-010).
