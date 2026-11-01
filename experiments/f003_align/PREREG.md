# F003 alignment preregistration: which link breaks between the linear prediction and the converged nonlinear outcome?

Author: `claude-fseries` (Claude Opus 5.5), single reader, not independently reviewed. Written 2026-11-01, Seattle PST (DST ended 02:00 today),
**before any run of the code in this directory**. Issue: kganjam/delphi-frontier#3 (F003). Evidence kind of every number this produces:
`simulated` (declared equations) and `computed` (linear algebra on declared Jacobians). Nothing here is observed; nothing is about any tissue.

## Why this exists (the alignment problem, stated before running)
F003's bounded action is "align the existing runner's observables and convergence categories before interpreting its movies or aggregates".
The existing runner is the frozen delphi-evolve nonlinear sweep (`scopedesk/oracles/nonlinear_sweep`, PREREG `cb27cf2`, results `1067cdb`,
`rows.jsonl` sha256 `a32c2bf7dd3c10162317974ae6a0ecbefa06c1c180a6886dea1bcb8ea4d4c882`, 2,520 cells; vendored here under
`frontier_compute/vendor/scopedesk/oracles/`). Reading its code and receipts, I find four misalignments between what it compares:

1. **Observable mismatch.** R3 compares the *fastest-growing linear mode* n\* (a property of the dispersion relation alone) with the
   *dominant DCT mode of the final state at T*. Linear theory with a finite random initial condition predicts a time-dependent spectrum;
   at the time a pattern forms, the dominant linear mode can be a slower-growing mode with a larger initial coefficient. And the final
   state can differ from the pattern that first formed. R3 lumps "linear theory is wrong in its own regime", "n\* is the wrong linear
   observable at finite time", "nonlinear selection during growth" and "post-saturation mode change" into one count.
2. **Regime mismatch.** At ε = 0.1 and 0.3 the initial perturbation std equals 0.1 or 0.3 |u\*|, i.e. at or above the sweep's own pattern
   threshold (0.1 |u\*|). For those cells the linear (small-amplitude) regime may never exist, so a linear prediction is not being tested.
3. **Convergence-category mismatch.** The sweep's `settled` flag compares 0.9 T with T only (a time-settling check, not numerical convergence).
   Step convergence was examined afterwards by other workers (PROTOCOL8 P8-1 dt 0.02 vs 0.01 over all cells; P8-2 dt 0.005 on 81 cells).
   Grid convergence was examined only in a 26-cell CPU pilot (`gpu_replay_cpu_pilot_grid_double_ids_mod_100_0.jsonl`). Horizon
   convergence (does the mode change after T?) was not examined.
4. **Solver-B linear set.** Solver B (finite differences, N_B = ⌈1.5 N_A⌉) has a modified discrete dispersion relation; near onset its set
   of unstable modes can differ from the continuum/spectral set, so some `solver_disagree_*` unresolved cells may be discretisation of the
   *linear* problem, not of the nonlinear one.

## Frozen inputs (reuse, not re-decision)
* Cells: `ensemble.build(10)` from the vendored copy (same parameters, Dv, L, ε, seeds, grid N_A, K, horizon T rule as the frozen sweep).
* Solver B results: field `B` of the frozen `rows.jsonl` (not rerun).
* Step-sensitivity: `results/compute/p8/report/frozen_grid_dt_report.json` (P8-1 category changes / mode flips dt 0.02→0.01) and
  `results/compute/infra_dt4/dt4_report.json` (P8-2). Reused as published; not rerun.

## Runner (new code, same scheme)
`experiments/f003_align/align.py`: solver A of the frozen sweep (Strang splitting, exact cosine-mode diffusion by orthonormal DCT-II,
RK4 reaction, dt 0.02, float64, same initial cosine series), batched across cells sharing (model, N) with numpy. It integrates every cell to
**2T** and records: u at 0.9 T, T, 1.8 T, 2 T; the DCT-II amplitude spectrum of u − mean(u) and std(u) every 1 τ up to T; and the
one-step time derivative norm at T.
**Reproduction gate R0 (must pass before any new quantity is interpreted):** at T, pattern flag and dominant mode equal the frozen row's
field A on every non-diverged cell, and relative amplitude difference ≤ 1e-6 on patterned cells. Cells failing R0 are listed and excluded
from the decomposition (kept in denominators as `R0_fail`). If more than 1% of cells fail R0 the run is reported as a failed reproduction
and no decomposition is reported.

## Independent linear calculation
`experiments/f003_align/linear_indep.py`, written by me, not importing `scopedesk.oracles.linear`:
* Jacobian from the analytic kinetics at the steady state (closed form), Du = 1, Dv from the cell, modes n = 1 … N_A − 1, q_n = (nπ/L)².
* σ_n = max Re eig(J − q_n diag(1, Dv)) by the closed-form 2×2 trace/determinant formula, cross-checked against `numpy.linalg.eigvals`.
* Unstable set U, fastest mode n\* = argmax σ_n, σ\* — compared with the frozen rows (`linear`, `n_unstable_linear`, `linear_fastest_mode`,
  `sigma_fast`). Agreement required: same verdict and same n\* on all cells, |σ\* − sigma_fast| ≤ 1e-9 (1 + |σ\*|). Disagreements listed.
* Solver-B discrete set U_B with q_n^B = (2N_B/L)² sin²(nπ/(2N_B)), n = 1 … N_B − 1: cells with U_B ≠ U (as a set of mode indices, and
  whether non-empty) are listed and cross-tabulated with the frozen `why` reasons.
* IC-weighted linear prediction: for each mode n the exact linear solution w_n(t) = expm((J − q_n D) t) w_n(0), with w_n(0) the
  DCT-II coefficients of the initial (u − u\*, v − v\*); predicted dominant u-mode at time t: L3(t) = argmax_n |w_{n,u}(t)|.

## Observables and categories (fixed now)
Let a(t) = std(u(t)), a_T = a(T), s(t) the measured spectrum, m(t) = argmax_{n≥1} s_n(t) (the frozen dominant-mode definition).
* **Linear regime exists (LIN_OK)**: a(0) ≤ 0.1 a_T. Otherwise the cell is `finite_amplitude_start` — the linear prediction is not tested.
* t_e = the last recorded time ≤ T with a(t) ≤ 0.1 a_T and t before the first time a(t) ≥ 0.5 a_T (small-amplitude regime, end).
* t_g = the first recorded time with a(t) ≥ 0.5 a_T (pattern-forming time).
* Linear validity at t_e: relative L2 difference between s(t_e) and |w_{·,u}(t_e)| over modes 1 … N−1, tolerance **0.2**; and m(t_e) = L3(t_e).
* **First-broken-link attribution** for linear-unstable (`applies`), frozen-resolved `pattern` cells that pass R0 and have LIN_OK, along the
  chain n\* → L3(t_e) → m(t_e) → m(t_g) → m(T):
  * `L_fastest_not_dominant`: L3(t_e) ≠ n\* (linear theory itself, given the initial condition, does not predict n\* at the end of its regime);
  * `L_linear_departure`: L3(t_e) = n\* but m(t_e) ≠ L3(t_e) (measured spectrum departs from linear prediction while amplitude is small);
  * `N_growth_selection`: m(t_e) = n\* but m(t_g) ≠ m(t_e) (mode changes during nonlinear growth);
  * `N_post_saturation`: m(t_g) = n\* but m(T) ≠ m(t_g) (mode changes after the pattern formed);
  * `match`: m(T) = n\*.
  Cells whose chain re-converges to n\* after a break are counted under the break and flagged `returned`. All counts reported by model, ρ, x, ε.
* **Convergence categories (aligned), per cell, each reported separately and then combined:**
  * `horizon`: pattern flag and dominant mode equal at T and 2T and amplitude within 5% → `horizon_stable`, else `horizon_changed`.
  * `stationarity` at T: ‖(u(T+dt) − u(T))/dt‖_∞ / max(|u\*|, 1) ≤ 1e-4 → `stationary`, else `transient` (reported, not gating).
  * `step`: `step_sensitive` iff the cell's NCA category or patterned mode changed in P8-1 (dt 0.02→0.01); else `step_ok_dt0.01`
    (dt 0.01 itself is not shown converged for all cells; P8-2 found 2 of 33 sensitive cells still changing).
  * `grid` (subset only, ids ≡ 0 mod 10, 252 cells, the gpu_replay preselected subset): solver A at 2 N_A, same continuous IC, to T;
    `grid_sensitive` iff pattern flag or patterned dominant mode differs, or patterned amplitude differs by > 10%.
  * **Aligned outcome**: `unresolved` if the frozen category is unresolved, or `R0_fail`, or `horizon_changed`, or `step_sensitive`,
    or (subset) `grid_sensitive`; else the frozen category. R1, R2, R3 recomputed under aligned outcomes with unresolved kept in every
    denominator; R3 additionally split by the attribution above.

## Predictions (registered before running; each can fail)
* Q1: the independent linear calculation agrees with the frozen linear fields on all 2,520 cells.
* Q2: at least half of the 461 frozen R3 mismatches are attributed to a post-linear link (`N_growth_selection` or `N_post_saturation`)
  among cells with LIN_OK; `L_linear_departure` is under 10% of LIN_OK linear-unstable cells.
* Q3: LIN_OK fails for most ε = 0.3 cells and holds for most ε = 0.01 cells.
* Q4: `horizon_changed` is under 5% of cells, and concentrated in Brusselator and ρ ≥ 1.5.
* Q5: U_B ≠ U occurs mainly at ρ = 1.03.

## Limits and non-claims
Same ensemble, author-chosen prior, 1-D Neumann, two kinetics, one IC family; solver A only for the new observables (B reused). Tolerances
(0.1 a_T, 0.5 a_T, 0.2 spectral, 5%, 10%, 1e-4) are my operationalisations, not field standards. "Dominant mode" remains a one-number summary.
No universal biological threshold is claimed or implied; nothing about fins or fish. Any amendment after this file is committed is written
as `AMENDMENT_n.md` with time and reason, and numbers from before and after are both kept.

## Budget and stop rule
Local CPU only, ≤ 3 capped processes (`systemd-run --user --scope -p TasksMax=256 -p MemoryMax=6G -p MemorySwapMax=0 -p RuntimeMaxSec=1800`),
OMP_NUM_THREADS=1. If the full 2T run cannot finish within 90 min wall, the horizon arm is restricted to the 252-cell subset and that is stated.
