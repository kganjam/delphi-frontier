# 2-D laminar flow engine: capability-proof protocol (frozen before any comparison run)

Owner delphi-rethink-nca (Claude Sonnet 5.5). Branch `work/nca-flow` (kganjam/delphi-frontier). Evidence kind: **simulated**. This is a *simulation-engine capability proof*, not biological aerodynamics: no flying-fish Reynolds number, no calibrated polar, no fin-tissue coupling. Re is dimensionless and stated only to document stability of the numerics.

## Engine choice
A maintained open-source LBM/CFD package is not installed here and is not obviously quick to audit; I implement an **auditable D2Q9 BGK lattice-Boltzmann solver** (`lbm.py`, ~200 lines, torch float64, same code on CPU or CUDA). Standard references (not re-read this session; equations are verified by the controls below, not by citation): Qian, d'Humieres & Lallemand 1992 (D2Q9 BGK), Guo, Zheng & Shi 2002 (forcing), Ladd 1994 / Ladd & Verberg 2001 (bounce-back, momentum exchange), Zou & He 1997 (velocity boundary). Lattice units: dx = dt = 1, c_s^2 = 1/3, nu = (tau - 1/2)/3, pressure p = rho/3.

## Controls (thresholds fixed now; all must pass before any obstacle result is reported)
C1 **Poiseuille** (force-driven channel, mid-way bounce-back walls, periodic in x), tau 0.8, channel widths H = 16, 32, 64: relative L2 error of the steady u(y) profile against u = F/(2 nu) (y - y0)(y1 - y) with walls at y0 = 1/2, y1 = NY - 3/2; require error(H=64) <= 1e-3 and errors decreasing with H, observed order >= 1.5 between H = 16 and 64.
C2 **Taylor-Green decay** (periodic box N = 32, 64, 128, tau 0.8, U0 = 0.02): velocity amplitude decays as exp(-2 nu k^2 t) with k = 2 pi / N; fit the decay rate over the run and require relative error of nu_eff <= 1e-2 at N = 128, decreasing with N.
C3 **Mass conservation**: total mass relative drift <= 1e-10 in the closed periodic cases (C1, C2) over the whole run.
C4 **Obstacle case self-checks** (idealized fin section = thin ellipse, thickness ratio 0.12, chord c, angle of attack 10 deg, in a box of 20 c x 8 c; equilibrium inflow at left/top/bottom, zero-gradient outflow at right; U = 0.05 (Mach about 0.087), Re = U c / nu = 100 (dimensionless, stability only), tau = 0.5 + 3 U c / Re): (a) |inflow flux - outflow flux| / inflow flux <= 3% averaged over the final 10% of the run, (b) no non-finite values, max Mach <= 0.3, (c) force coefficients stationary: relative change of the mean drag over the last two 10% windows <= 1% (else the run is labelled UNSTEADY and reported as such), (d) grid refinement at c = 40 and c = 80 lattice cells (c = 160 only if the GPU job is approved): the drag-coefficient difference between successive levels is reported; refinement is declared "consistent" only if the difference shrinks with c.
Stop rule: after 2 failed repairs of any control the item is reported as failed and the video is not made for the failing configuration.

## Outputs
Saved states (every 400 steps of the chosen run; u, v, rho as float64 npz) -> derived pressure coefficient Cp = (p - p_inf)/(0.5 rho U^2), vorticity omega c / U (central differences), speed |u|/U. Time in convective units t U / c (1 convective unit = c/U lattice steps); lengths in chords. Manifest with sha256 of code, states, frames, video, units and ffmpeg command. Video 10-20 s, < 8 MB, one saved state per video frame (no interpolation).

## Compute
CPU baseline first for c = 40 (and all controls). The c = 80 level (4x the nodes, 2x the steps = 8x the cost) and optionally c = 160 are handed to dx-gpuops as ONE bounded H100 job (<= 30 min, one GPU; gpuops alone submits) only if the measured CPU time extrapolation exceeds the CPU budget; the pilot timing and extrapolation are recorded in `results/cpu_pilot.json` before any handoff.
