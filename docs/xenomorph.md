# Xenomorph: dissociated cells aggregating into a compact body, and a printable model made of cells

Written 2026-11-01 (Seattle, PST). Branch `claude/xenomorph-20261101`.

> **What this is.** A *simulated aggregate morphology*: generic cells with differential adhesion, in a Cellular Potts
> model (Morpheus 2.3.9), cross-checked by an off-lattice engine. **It is not a Xenobot and not any organism.**
> **No frog parameter is used.** Every energy, temperature and size is dimensionless (lattice units, Monte Carlo
> steps). The published constructs (Kriegman 2020 PNAS; Blackiston 2021 Sci Robot, both read at abstract level only)
> **move by cilia. Cilia are not modelled here, and neither is contraction**; contraction is this project's own
> modelling choice elsewhere and is absent from this simulation. A printed object is **a physical model of a
> simulation**: not a living construct, not a biological validation, and it demonstrates nothing about viability.

RESULTS_PLACEHOLDER

## Model

**Cellular Potts (Morpheus 2.3.9, binary sha256 `3d9a6e5a…5d94`, source tag v2.3.9 = `29a26b0`).** Each cell is a set of
lattice voxels with id σ. The engine minimises, by Metropolis copy attempts at temperature T,

  H = Σ_(neighbour pairs i,j; σi≠σj) J(τ(σi), τ(σj)) + Σ_cells λ_V (V_σ − V_target)²

on a 100³ cubic lattice, neighbourhood order 2, no-flux boundaries, T = 3, λ_V = 1, V_target = 257 voxels (a radius-4
sphere). Template: Morpheus's own `Examples/CPM/CellSorting_3D.xml` (Graner & Glazier 1992), re-parameterised.

**Differential adhesion.** With surface tensions γ_xM = J_xM − J_xx/2 and γ_AB = J_AB − (J_AA + J_BB)/2
(Glazier & Graner 1993), a population compacts when every γ_xM > 0, and type B engulfs type A when
γ_AM > γ_AB + γ_BM.

| arm | J_AA | J_BB | J_AB | J_AM = J_BM | γ_AM | γ_BM | γ_AB | expectation |
|---|---|---|---|---|---|---|---|---|
| `dah` (main) | 2 | 8 | 7 | 10 | 9 | 6 | 2 | compact; 9 > 2 + 6 so B engulfs A (A core, B shell) |
| `equal` (control) | 4 | 4 | 4 | 10 | 8 | 8 | 0 | compact, must **not** sort |
| `zero` (control) | 20 | 20 | 20 | 10 | 0 | 0 | 0 | contact carries no energy: must **not** compact |

**Dissociated start.** 128 cells (64 A, 64 B by seeded shuffle) on the 128 sites of a simple-cubic lattice nearest
the centre, spacing 2r + gap + 2·jitter = 10 voxels, each jittered ±0.5 per axis, so no two cells touch at t = 0
(checked in every run: 128 aggregates at t = 0). Horizon 20 000 MCS, snapshots every 500.

**Off-lattice engine (second engine, GPU).** `engineering/xenomorph/offlattice.py`, PyTorch, overdamped, PhysiCell-1.x
potential form: repulsion c_r(1 − d/2r)² for d < 2r, adhesion −c_ij(1 − d/R_A)² for d < R_A = 2.5 r, plus Brownian
noise √(2 D dt) ξ. r = 1, c_r = 10, 256 cells, start with no pair inside adhesion range. Swept c_AA ∈ {0, 0.5, 1, 2, 4},
c_BB/c_AA ∈ {1, 0.5, 0.25}, c_AB = √(c_AA c_BB), D ∈ {0.005, 0.02}, dt ∈ {0.02, 0.01}, 4 seeds: 208 systems in one
batched GPU run. This is **not PhysiCell**; it reimplements its published potential form. A PhysiCell 1.14.2
run of the three arms is reported separately below.

## Protocol, frozen before production

`engineering/xenomorph/protocol.json` sha256 `b4e329ba…3e4f` (commit `f6a67d98`), then
`protocol_addendum_1.json` (own sha256 in `protocol_addendum_1.sha256`, commit `e671f14e`) written while the
production job ran and before any of its results were read. The addendum's text says "~09:05 PST"; the
commit was actually made at about 08:50 PST. Two pilots ran before the freeze (seeds 98, 99; `results/xenomorph/pilot/`):
- a low-density start stalled in ~21 clusters that never merged;
- the dense start compacts.

The zero-adhesion gate was set on Rg because jammed cells touch without cohesion.

Measurements per snapshot (`analyze.py`): aggregate count (contact-graph components, face adjacency), largest-cluster
fraction, sphericity of the largest cluster (marching-cubes area), cell–cell and cell–medium contact area (voxel
faces), radius of gyration (normalised by (N·V)^(1/3)), homotypic contact fraction (sorting index), core–shell index.

## Printable model

`engineering/xenomorph/printable.py`, built on the repo's print stack (`engineering/geometry/validate.py`
for every check, manifold3d 3.5.4 for every boolean and for ray-cast wall sampling), following `docs/printing.md`.

- **Units and scale.** The simulation is dimensionless. A nominal voxel length **h = 20 µm** is *declared*, not
  measured. It makes the compact aggregate about 0.8 mm across, the order the brief gives. It is not a frog cell
  size. The display scale is **75**, so `prop_mm = biological_m × 1000 × 75`: 1 voxel = 1.5 mm and the compact
  aggregate is about 63 mm.
- **Cell-resolved solid (`*-cells.stl`).** Every cell is a sphere of its equal-volume radius at its voxel centroid.
  The spheres are unioned, so the print is visibly made of cells. Two cells count as joined only if their spheres
  intersect in a neck of radius ≥ 1.25 mm.
  - If a snapshot is not one body (dissociated and clustering stages), the report states the piece count and the
    radius factor that would join it.
  - It then adds **print-only connector struts**: r = 1.25 mm, fixed, never scaled from biology, grey in the renders.
    They run along a minimum spanning tree between pieces.
  - Sealed internal cavities are filled so they cannot trap resin.
- **Surface solid (`*-surface.stl`).** Marching cubes (level 0.5) on the occupancy field after Gaussian smoothing
  (σ = 1 voxel).
- **Checks on every STL.**
  - Closed, consistently oriented 2-manifold, recomputed from the triangle arrays and again after an STL round trip.
  - One face-connected body.
  - Fits a 120 mm box.
  - Wall ≥ 1.0 mm on 3 000 ray-cast samples (the repo's provisional rule).
  - Volume, and mass at an *assumed* 1.18 g/cm³.
  - A sha256 per file.
- **Not checked.** Self-intersection (manifold3d booleans produce none by construction), slicing, supports, cups,
  resin-specific limits. **Printer and resin are unknown.** Run the `docs/printing.md` operator checklist in PreForm
  before printing.

## Reproduce

```
uv venv --python 3.13 .venv-xm && VIRTUAL_ENV=.venv-xm uv pip install numpy==2.4.4 scipy scikit-image tifffile trimesh==5.2.0 manifold3d==3.5.4 matplotlib==3.11.2 imageio
python -m engineering.xenomorph.cpm_model --arm dah --seed 1 --out RUN      # needs the Morpheus 2.3.9 binary (MORPHEUS_BIN)
python -m engineering.xenomorph.analyze RUN && python -m engineering.xenomorph.pack_fields RUN
python -m engineering.xenomorph.printable --fields RUN/fields.npz --metrics RUN/metrics.json --out OUT
python -m pytest --noconftest tests/test_xenomorph.py
```
