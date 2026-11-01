# AMENDMENT 1 to F003 PREREG (written 2026-11-01 08:49 PST, before any new quantity was read)

State at writing: `linear_check.json` (Q1, Q5) exists and was read; the solver-A base run (`align.py run ... --arm base`) started at 16:48Z and
no output of it has been opened. Trigger: critique by Google `gemini-4-argon` of PREREG.md (verbatim in `review/argon-prereg-critique.txt`).
All original definitions stay and are reported; the items below are ADDED reports or variants. Nothing is removed.

1. (argon 1, accepted) Besides the first-broken-link attribution, report the full contingency table of the four links
   n*→L3(t_e), L3(t_e)→m(t_e), m(t_e)→m(t_g), m(t_g)→m(T) (each equal/different), 16 cells, for the same population.
2. (argon 2, accepted as a variant) LIN_OK is defined relative to the nonlinear final amplitude a_T, which is circular. Add an absolute variant
   LIN_ABS: a(0) ≤ 0.02 |u*| (in this design this selects ε = 0.01). Both are reported; the attribution is reported under each.
3. (argon 3, accepted) Recording is every 1 τ. Cells with t_e = 0 are reported as `linear_regime_unresolved` and excluded from the
   L3(t_e)→m(t_e) test (at t = 0 the comparison is trivially true). Cells with t_g − t_e ≤ 1 τ are flagged `aliasing_limited` and counted.
4. (argon 4, accepted as a variant) Near-degenerate argmax: report |Δn| for every broken link, and a tolerant variant in which a link counts as
   broken only if the argmax mode's amplitude exceeds the reference mode's amplitude by more than 5% in the same spectrum.
5. (argon 5, not adopted, reason) L3 already evolves both species exactly (expm of the 2×2 mode matrix acting on (w_u, w_v)); the measured
   observable is the u spectrum, so comparing predicted and measured u components is like-for-like. Phase sensitivity concerns complex
   eigenvalues; I report the number of LIN_OK cells whose L3(t_e) mode has a complex eigenvalue pair.
6. (argon 6, accepted) Aligned R1–R3 are reported for the full 2,520 cells WITHOUT the grid check, and separately for the 252-cell subset WITH it.
7. (argon 7, accepted as a variant, limited) Add an aligned variant that also requires `stationary` at T. Stationarity is recorded only at T,
   not at 2T; 2T tests one doubling of the horizon and cannot bound slower coarsening. Stated as a limit.
