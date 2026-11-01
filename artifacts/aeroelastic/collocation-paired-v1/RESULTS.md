# Paired collocation study v1: returned state and independent audit

**Status.** The audit passed. The study is valid: all 10 gating controls pass, re-derived independently.
- **Arms:** 43 of 45 repaired arms are valid. The other 2 are native model-domain exits, kept as returned.
- **Repaired variant:** in χ0.8 at 16 m/s and χ0.2 at 20 m/s, every decision input is `resolved`.
  - χ0.8, 16 m/s: **retain bending, one-way sufficient**.
  - χ0.2, 20 m/s: **reject bending, one-way sufficient**.
- **χ0.8 at 20 m/s is not assessable,** because its coarsest-lattice coupled arms left the beam model's valid range.
- **These decisions are conditional on the diagnostic collocation variant.** Production decisions stay fidelity-v1's, which are all `undetermined`. Nothing was rerun, and no criterion, status or decision was changed.

## What returned
- **Run:** VM04, packet `4be2b9ec…dfffa` (source `5a8f5c9`, packet commit `9dfabbb`). Admitted by infra at 12:21:39am PDT; finished at 12:32:01am PDT on 2026-11-01 with exit 0.
- **Resources:** native wall time 541.7 s (estimate 500–560 s; cap 1200 s); output 45.4 MB (cap 64 MB). The estimate came from measured v1 runtimes rather than being a guess.
- **Raw return:** `/data/artifacts/delphi-evolve-rethink/gcp/coupled-collocation-v1/coupled-collocation-v1/frontier-cpu-20261031-04/final-9aab24f5032f4cfca540705a27d64e6d`, collected by infra.
- **Rehashed here:** 233 of 233 collection files (45,469,659 bytes), every file in the native receipt, and all 15 executed sources against the admitted packet. Environment: Python 3.12.3, NumPy 2.5.4, SciPy 1.17.1.

## Independent audit (`return-audit-report.json`)
`python -m engineering.aeroelastic.audit_collocation`, code sha256 `e00befd5…bc9c`, read-only on the raw tree.

**How independent it is, stated plainly.**
- **Per arm:** the checks are the frozen fidelity-v1 return audit (`audit_fidelity.py`, unchanged). They cover:
  - closed-form cantilever shapes, saved-load and CL reproduction;
  - closed-form reproduction of the domain exits;
  - one fresh VLM solve on each stored final pose (49 poses; the 2 exits have no final valid pose).
  - Each arm is audited with the collocation that produced it.
- **Study-specific checks:** identity, cardinality, K1–K7 and the agreement with the native summary were written **after** the return arrived and after its native `summary.json` had been read. They apply the frozen protocol's thresholds and change none.

**Result:** `audit_passed: true`. There are 6,493 comparisons, 4,103 of them exact, and the worst is 2.2e-15. No finding blocks.
- **The only findings** are the two native domain exits, `chi0.8-u20-main-one-way-frozen-load` and `-two-way-static-feedback`.
  - Both exit at the first proposed shape.
  - The closed form reproduces them: pectoral tip/span 0.10127 against the 0.1 gate, slope 0.132 rad against 0.2.
- **K1–K4c:** recomputed locally by rigid unit solves (54 s, one thread) and compared value by value. They also match cfd04's returned CL exactly. Every verdict was re-derived from the numbers.
- **K5–K7:** re-derived from the raw files.
  - K5: `upstream_force` (reported, not gating) fails on `main` only, as in the preflight.
  - K6: the rigid arms are bitwise identical across the two 20 m/s contexts.
  - K7: the six baseline arms reproduce fidelity-v1 with every compared value exact.
- **Classification:** the audit's separate three-grid implementation reproduces every native status and decision.

**Controls the audit must fail on** (`tests/test_aeroelastic_audit_collocation.py`): a repaired arm audited with the production collocation fails the fresh-solve check, and so do a changed control number and verdict, a nondeterministic rigid arm, a changed baseline arm, tampered, unlisted or foreign source bytes, and a changed native decision.

## Paired comparison and numerical error (`paired-comparison.json`)
All values are fixed-α CL on the fixed source area, or range in m. "GCI" is the frozen T2 three-grid estimate. It covers **lattice error only**.

| Context | Effect | 64×16 repaired | T2 extrapolated ± GCI | observed order p | repaired − production at 64×16 |
|---|---|---|---|---|---|
| χ0.8, 16 m/s | ΔCL bending | −0.003540 | −0.003478 ± 7.7e-5 (2.2 %) | 1.03 | −0.08 % |
| | ΔCL feedback | 2.935e-5 | 2.872e-5 ± 7.9e-7 (2.7 %) | 0.95 | +0.36 % |
| | Δrange bending | −0.0955 m | −0.0931 ± 0.0030 m (3.1 %) | 1.06 | −0.09 % |
| χ0.2, 20 m/s | ΔCL bending | −0.001319 | −0.001297 ± 2.8e-5 (2.1 %) | 1.04 | −0.08 % |
| | ΔCL feedback | 3.634e-6 | 3.566e-6 ± 8.6e-8 (2.4 %) | 0.91 | +0.34 % |
| | Δrange bending | −0.1182 m | −0.1143 ± 0.0048 m (4.0 %) | 1.09 | −0.11 % |
| both | rigid CL | 0.24795 | 0.24573 ± 0.0028 (1.1 %) | 1.00 | +0.01 % |

**Decision margins (repaired variant, numerical error only).**
- **χ0.8, 16 m/s, bending.** The bending/rigid ratio is 1.415 %, and its GCI interval is 1.37–1.46 %, against the 1 % convention. It is 1.43–1.47 % on every individual lattice.
- **χ0.2, 20 m/s, bending.** The ratio is 0.528 %, with interval 0.51–0.55 %. It is 0.53–0.55 % on every lattice.
- **Feedback.** The feedback/bending ratio is at most 0.87 % (χ0.8, 16 m/s) and 0.29 % (χ0.2), against the 10 % convention.
- **Agreement of the two triples.** In every resolved effect, T2 and T1.5 agree within their GCIs, as the frozen rule requires.

**What changed and what did not.**
- **The repair resolved the triples; it did not move the answer much.**
  - The production lattice series zigzag: T2 is divergent in all 27 v1 cases.
  - The repaired series are monotone at observed order about 1 in every decision input.
  - At 64×16 the two schemes differ by 0.08 % in bending and 0.35 % in feedback. That is 0.04–0.14 of the repaired GCI.
- **The descriptive magnitudes v1 reported per lattice are essentially those now resolved.** The production collocation's bias on these coupled effects is small at the finest lattice and large at the coarse ones. On `main`, repaired − production rigid CL is +1.5 %.
- **The repaired five-lattice spread is larger, not smaller.** Bending spreads 5.3–5.5 %, against 2.2–2.3 % for production. The repair turns irregular noise into a smooth first-order drift, and the drift can be extrapolated.
- **There is still no converged absolute reference.** The rigid-CL extrapolation sits 0.9 % below the 64×16 value.
- **Pelvic tip/span stays `sign_resolved`.** Its T2 triple is still divergent, with a five-lattice spread of 0.5 %. It is not a decision input.

**χ0.8, 20 m/s (not assessable).**
- **Why it is not assessable:** on `main` (16×4) the repaired collocation raises the load enough to put the pectoral tip at 0.1013. The production collocation gave 0.0985 there.
- **The other lattices:** the repaired one-way pectoral tip is 0.0998 on `fine`, 0.0991 on l32x8, 0.0989 on l36x9 and 0.0981 on l64x16. That is 0.2–1.9 % inside the gate.
- **Descriptive values on the four valid lattices** (not decisions): bending/rigid 2.32–2.36 %, feedback/bending 1.48–1.49 %.
- **Frozen policy applies:** the domain exits are a model result, not a failure to repair, and the context cannot be decided under the frozen rules on this ladder.

## Visuals (actual returned states)
- **`paired-ladder.png`:**
  - **What it shows:** production (fidelity-v1 return) and repaired values on all five lattices, for rigid CL, bending, feedback and range, in 3 contexts. Each panel title carries both native statuses.
  - **Diamonds:** the T2 extrapolation ± GCI, drawn only where the triple is monotone.
  - **χ0.8, 20 m/s:** the excluded `main` group is labelled with its domain exit.
- **`collocation-controls.png`:** the returned K4c control, rigid CL under chordwise and spanwise refinement for the four fins and the elliptic AR 6 wing.
  - Over 32×4 to 32×16 the repaired collocation is flat (fins 4.2e-5, ellipse 2.2e-5), while production drifts (7.4e-3 and 8.7e-3).
- **`render-l64x16-chi0.8-u20/`:**
  - **What it is:** the unchanged `render.render` run on the **repaired** 64×16 χ0.8, 20 m/s arms. It shows 18 actual static iterations, unscaled deflection, and the separately integrated fixed-α descent.
  - **Caveats:** static iterations are not physical time. The poster's own text does not name the variant, because the renderer is frozen. `provenance.json` names the repaired arm files.
- **Provenance:** `collocation-figures.provenance.json` and `render-…/provenance.json` carry the sha256s of every input, the code and every output. Figures were made with matplotlib 3.11.2 in a scratch venv, outside the scientific environment.

## Decision relevance
- **What the frozen protocol says follows:**
  - The resolved repaired decisions justify a separate, labelled change to production VLM collocation **by its owner (cfd04)**.
  - They do not change production decisions by themselves.
- **What the paired difference bounds:** how much the production collocation biases each coupled effect at these lattices. It is small at 64×16.
- **No further run is requested here,** and no finer ladder.

## Scope
- **The model:** this is the bending-only, torsion-rigid, fixed-α scaffold with assumed constant EI.
- **The aerodynamics:** inviscid thin-surface VLM with a fixed straight wake, here in a labelled diagnostic collocation variant (`collocation-repair/1`). The flight model is a separate rigidized-shape point-mass descent.
- **What it is not:** nothing here is a tissue measurement, a trimmed glide, a continuous FSI result, or evidence about real fish.
- **Error estimates:** the GCI values are numerical lattice error only, not model-form error. Model fidelity is not biological validity. `biological_success_probability` is null.
