# LLM review log: engineering/neuro (claude-neuro, 2026-11-01)

The raw reviews are in this folder. The prompts were sent with the full source of caudal_cpg.py, fast_start.py and glide_stab.py (round 1 also included NEURAL_IMPLEMENTATION.md). The API key was sent in the x-goog-api-key header only.

## Round 1: gemini-4-argon (deep critique), after the first model versions
| Finding | Decision | What changed |
|---|---|---|
| M2 `lock_analytic` uses the wrong topology; it should be per-link \|dw\| <= c | **Rejected.** In a locked unidirectional chain every follower runs at the leader's realised frequency, so c sin(psi_i - lag) = w_0 - w_i = -i dw, and the last link binds: \|(N-1) dw\| <= c. | The locking check now covers all 48 cases, including the 5 near the boundary (all agree). The rebuttal is in the module docstring. |
| Taxi omits surface-piercing (spray/wave) drag; the feathering limit drives the result | Accepted | Added `taxi_water_drag` (Hoerner spray drag plus a residual wetted-hull fraction). The fraction (0-10%) and the feathering limit (6-15 deg) are now sampled priors in M1 and swept in M2. |
| lambda is independent of f and H | Acknowledged | Swept independently (0.8-1.2 L); listed as a limitation. |
| M1 treats the C-start as a pitch turn | Accepted | 3D kinematics: the C-start is a yaw turn to the escape trajectory; the climb is a separate pitch-steering stage plus an assumed small vertical component. |
| M1 throws away the vertical kinetic energy and launches the glide from h0 = 1 m | Accepted | Taxi start is bracketed (optimistic V = U_e; pessimistic V = U_e cos gamma_e). Release is at h0 = 0.1 m with gamma0 = 0; the h0 = 1 m result is kept only to compare with the glide-fixed-launch card. |
| M3 inertia scaling and ballast for the 50 g case | Clarified | Stated as an explicit assumption: same geometry, CG and radii of gyration. |
| M3 roll: dihedral restoring needs sideslip, but the otoliths were made blind by assuming "coordination" | **Accepted (important)** | Replaced by a 4-state lateral model [beta, p, r, phi] with the caudal fin as vertical surface. The otolith signal is derived from the side force (phi_oto = -Y_beta beta / (m g)); the assumed 0.1 gain is gone. M4 text revised. |
| M3 uses one shared delay for canal and vision | Accepted | One delay chain per sensed channel. Exactness is checked against an explicit-buffer simulation. |

## Round 2: gemini-3.8-flash (quick check), after the revisions
- It confirmed that all five round-1 fixes are in place (yes on each).
- It proposed three new bugs, all **rejected**:
  - (a) Yaw clamp: `psi_t` is wrapped relative to the initial heading 0, so sign(psi_t) min(\|psi_t\|, cap) already turns the short way.
  - (b) Pitch-gravity term: the alpha-dot row's -g sin(gamma)/V theta is the standard stability-axis term for a gliding reference state, and u-dot correctly carries -g cos(gamma) theta.
  - (c) Lobe thrust sign: for a heaving foil the lift is tilted forward by beta = atan(v/U), so its forward component is +L sin(beta) and drag contributes -D cos(beta) (Knoller-Betz). Zero heave gives T <= 0 (control check).

## Found by our own controls (not by the reviewers)
- Body length bug: 0.037 m instead of 0.171 m (a factor 100 was missing from the Fulton condition factor). The Bainbridge comparison could not catch it, because both sides scale with L. There is now an assert and a test.
- Air-density mismatch: 1.204 against the glide model's 1.225. Caught by the "reproduce glide-fixed-launch 25.14 m" control (M1 run exited 3). M1 and M2 now use engineering.simulation.controlled.RHO.

## Round 3: gemini-3.8-flash (quick bug check of m5_mcell.py and sobol_m3.py)
- It reported no defects that would change a reported number. That is weak evidence from a quick model, not a verification; the numerical controls in each manifest remain the primary check.
- A known modelling choice the reviewer did not flag: the M5 noise increment sigma*sqrt((1-a^2)/2) gives a stationary membrane-noise SD of sigma/sqrt(2), not sigma. The reported "sigma ~0.45-0.6 of threshold" is therefore the parameter value; the stationary SD is about 0.32-0.42 of threshold.
