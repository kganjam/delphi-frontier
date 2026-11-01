# Design review: gemini-4-argon, 2026-11-01 (PDT morning)
Reviewer: Google `gemini-4-argon`, asked to critique the voxcraft sweep design (prompt = design summary in commit).
Points raised and what changed:
1. Passive bodies may topple/roll after the 1 s transient -> nonzero passive displacement. **Kept as a measurement**: that is exactly the falsifier of `passive-control`; reported, not hidden. t=0 phase impulse for non-sync patterns is absorbed by the stated 1 s transient window; not removed (would need a source patch).
2. Mesh refinement in a lattice model changes contact count, phase gradient sampling. **Kept**: the endpoint asks for the refinement change and it is reported whatever it is. Checker is defined on coarse cells (2x2x2 blocks on the fine mesh) so it does not alias.
3. "Equal total actuation" = equal commanded amplitude x active voxel count (identical per-voxel time integral of commanded contraction), NOT equal mechanical work. **Disclosed** as the operational definition.
4. Mirror symmetry may break via float summation order + stick-slip chaos. **Changed**: added an identical-duplicate arm (`rep`) per population candidate and 3 replicates per endpoint pattern, so the mirror error is compared against run-to-run noise.
5. Relative mirror error blows up for |d|~0. **Changed analysis**: ratio reported only where |d| exceeds 10x the passive-control floor; absolute errors reported for all.

# Second review: gemini-4-argon on the E3 (mirror) failure interpretation, 2026-11-01 ~09:15 PST
Points: (1) dy is not dt-converged, so mirror error on these trajectories may be chaotic amplification (stick-slip Coulomb
friction) of a rounding-order seed rather than a systematic directional solver bias; (2) "sign-consistent within a dt" is a
tautology for a deterministic code; (3) state precision; (4) a 1% relative bound is harsh for small |d|.
Changes: precision stated (fp64, VX3_Vec3D<double>); wording changed from "solver anisotropy" to "a deterministic asymmetry
of the discrete solver, amplified to mm scale; seed vs amplification not yet separated"; the prereg bound is NOT changed and
absolute errors are reported beside it; added POST-HOC diagnostic `gen_sweep.py --ensemble` (unmirrored O(1e-7)-cycle phase
perturbations, 24 members x 9 patterns) to test whether perturbation spread ~ mirror error.
