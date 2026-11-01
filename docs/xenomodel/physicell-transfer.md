# PhysiCell 1.14.2 at the cellular scale of the microcarrier: what transfers

2026-11-01, harness `claude-xenomodel`. Engine: PhysiCell 1.14.2, commit
`dbd3499250141b27600e91e501c54c46f68f2763`, BSD-3-Clause (`licenses/PhysiCell.txt`;
the BioFVM, MaBoSS and pugixml licence files sit beside it, and there is no root
LICENSE file). This is the first install here. The build recipe for other harnesses
is in `/data/artifacts/delphi-evolve-rethink/messages/claude-xenomodel-status.md`.

## What was run

The custom module is `engineering/xenomodel/physicell_contractile/` (the build
script copies a pristine upstream tree and overlays `main.cpp`, `custom_modules/`
and the settings). The protocol was frozen and committed *before* the runs
(commit `e4cecc3e`). Results:

- 20 preregistered arms with 18 checks, all passing
  (`artifacts/xenomodel/physicell-results.json`);
- an N-node convergence series (`physicell-chain-convergence.json`);
- a 324-run descriptive sweep (`physicell-sweep.json`).

Every run has a receipt (argv, exit code, binary, settings and source hashes,
seed). No stochastic term is used, and OMP_NUM_THREADS=1.

The model is a 2-D cell sheet (2-cell pair, 29-cell hex strip, or 5–65-node chain)
joined by neighbour springs. The springs' rest length is shortened periodically
(prescribed contraction, standing or travelling). A "native" arm instead uses
PhysiCell's own repulsion/adhesion potentials with a prescribed cyclic cell radius.
Substrate drag is either stock (isotropic, unit mobility) or direction-dependent
(x-velocity divided by ξ₊ or ξ₋ by sign).

## What transfers (to the microcarrier modelling, as model statements)

1. **No net motion without an external symmetry-breaking force.** In stock
   PhysiCell mechanics (overdamped, unit mobility, pairwise forces), no internal
   actuation can translate an aggregate. Travelling waves, asymmetric bodies and
   native potentials with cyclic radius all fail. This holds to 10⁻¹³ µm in all 85
   isotropic runs and is Lean-proved for the Euler and AB2 updates. It also applies
   to the ff-xenomorph aggregation work: compaction by differential adhesion cannot
   move the aggregate's centroid in stock PhysiCell.
2. **The crawler law** `ΔX = κ·TV(L)`, with `κ = (ξ₋ − ξ₊)/(2(ξ₊ + ξ₋))`, holds in
   the engine to 1.1·10⁻⁵ at the finest dt. In the strip sweep, the drag-ratio factor
   `(r − 1)/(r + 1)` captures the leading dependence to about ±10 %, and motion is
   linear in contraction amplitude.
3. **Controlling parameters, ranked by the sweep:**
   - first, the substrate anisotropy `r` (zero motion at r = 1);
   - second, k·T, the drive period relative to the spring relaxation time;
   - then contraction amplitude (linear);
   - then the wavelength / standing-vs-travelling choice (about 18 % in the
     converged chain).

   Wave direction is close to irrelevant (0.03 % in the converged chain).

## What does not transfer

- **Cilia.** The sources report ciliary locomotion. A cell-centre model with
  isotropic drag has no surface-slip mechanism and no hydrodynamic interactions,
  so it says nothing about ciliary propulsion, which needs a Stokes / boundary
  element solver.
- **Units.** Time is nominal. Only k·T and r matter, and neither is measured for
  any tissue or substrate.
- **Tissue rheology.** Cell-centre springs are not a continuum modulus. Mapping
  `k` to E needs measurement M2 in `artifacts/xenomodel/calibration-design.json`.
- **The anisotropy itself.** ξ₋/ξ₊ is imposed. Whether any real substrate or medium
  gives one is measurement M3. If it is ≈ 1 and linear, the model predicts no
  contraction-driven motion.
- **3-D, contact mechanics, growth, cell turnover, oxygen.** All are off here
  (no proliferation, no death, inert substrate field).
- **The Voxelyze scale.** PhysiCell is overdamped and Voxelyze is inertial with
  Coulomb friction. Both obey the same momentum statement (Theorems 1 and 2), but
  the mechanism of motion differs: in Voxelyze, Coulomb friction lets a travelling
  wave work, while linear drag in PhysiCell does not.
