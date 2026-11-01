# Actuation to motion: the equations behind the contractile microcarrier

Status: model mathematics plus one cell-scale engine test, 2026-11-01. Harness
`claude-xenomodel`, branch `claude/xenomodel-20261101`.

**What this is.** A derivation of when a periodically actuated soft body can and
cannot translate. It covers the soft-voxel engine we run (Voxelyze), the cell-scale
engine we just installed (PhysiCell 1.14.2), and the two-node crawler that connects
them. Lean 4 checks the discrete statements in
`engineering/formalize/lean/ActuationMotion.lean`. Machine-readable records in the
repo's equation-registry format (`engineering/assurance/equations.py`) are in
`artifacts/xenomodel/equations.json`.

**What this is not.** Nothing here is an observation. No parameter is measured on
Xenopus tissue. **The cited sources (Kriegman 2020 PNAS; Blackiston 2021 Sci Robot,
read at abstract level) report _ciliary_ locomotion. Contraction is this project's
modelling choice.** Section 6 says what changes if the real mechanism is ciliary.

---

## 1. Model: an actuated lattice with damping and ground contact

Nodes (voxels or cells) `i = 1..N`.

| Symbol | Meaning | Unit |
|---|---|---|
| `x_i(t)` | node position (horizontal part `x_i^h`) | m |
| `m_i` | node mass | kg |
| `F_ij` | internal force on `i` from `j` (bond, spring, beam) | N |
| `L_ij(t)` | prescribed rest length of bond `ij` (the actuation) | m |
| `C_i` | absolute-frame damping coefficient on node `i` | kg s⁻¹ |
| `N_i ≥ 0` | floor normal reaction | N |
| `f_i` | horizontal contact (friction) force | N |
| `g` | gravity | m s⁻² |
| `ε` | actuation strain amplitude | 1 |
| `ω = 2π/T` | actuation angular frequency | rad s⁻¹ |
| `φ_i` | actuation phase of node / bond `i` | rad |
| `q = 2π/λ` | phase wavenumber; phase velocity `c = ω/q` | rad m⁻¹; m s⁻¹ |

Actuation (Voxelyze form): a voxel's zero-stress size is
`s_i(t) = s₀ (1 + α T_i(t))` with `T_i(t) = A sin(ωt + φ_i)`, so `ε = αA`
(source `include/VX_Voxel.h:88`, pinned commit `4287e365`). In the cell model the
rest length is `L_ij(t) = r₀ (1 − ε (1 − cos(ωt − q x̄_ij))/2)`.

**Equation of motion (E0)**

    m_i ẍ_i = Σ_j F_ij(x, t) − C_i ẋ_i + N_i ẑ + f_i + m_i g

Assumptions: internal forces obey Newton's third law, `F_ij = −F_ji`. For Voxelyze
this is an assumption about the link code, not something proven here. The
frictionless control D (horizontal COM constant to 9 decimals over 241 samples)
corroborates it numerically. Scope: rigid flat floor, no fluid.

## 2. Momentum balance and the frictionless theorem

Summing E0 over nodes, the internal forces cancel:

**(E1)** `d/dt Σ m_i ẋ_i^h = − Σ C_i ẋ_i^h + Σ f_i`

**Theorem 1 (homogeneous, frictionless).** Take `m_i = m`, `C_i = C` and `f_i ≡ 0`.
Then the horizontal COM velocity obeys `V̇ = −(C/m) V`, so

    V(t) = V₀ e^{−Ct/m},   X(t) = X₀ + V₀ (m/C)(1 − e^{−Ct/m}).

If `V₀ = 0` then `X(t) ≡ X₀` for **every** actuation pattern, phase gradient and
body shape.

*Discrete form actually run.* Voxelyze `CVX_Voxel::timeStep` does
`linMom += F·dt; pos += linMom·dt/m` with `F` including `−C·v`. Summed momentum
gives `P_{n+1} = (1 − dt C/m) P_n + dt Σ F_ext`. Lean proves
`com_fixed_absolute_damping`, `total_momentum_closed_form` and the contrapositive
`com_motion_requires_external_force`: if the COM moved, some step carried a nonzero
external horizontal force, or the initial momentum was nonzero.

*Voxelyze's actual damping coefficient* is `C = ζ_global · 2√(m E s)`
(`include/VX_MaterialVoxel.h:43`, `src/VX_MaterialVoxel.cpp:75`), so the damping
ratio `C/m = 2ζ√(E s / m)` is uniform for a homogeneous material. The general form
proved in Lean is `com_fixed_uniform_damping_ratio`: per-node masses with
`C_i = γ m_i` keep the **mass-weighted** COM fixed. Relative (bond) damping is
internal and cancels with `F_ij`.

*Hypothesis that cannot be dropped.* Lean proves `heterogeneous_mass_breaks_com`.
With masses 1 and 2, one damping `C` and an equal-and-opposite internal force, the
mass-weighted COM moves. So uniform `−C·v` damping on unequal masses is itself
a propulsion mechanism. It is a numerical-model artifact unless the damping is
physical. Mass-proportional damping (`C_i = γ m_i`) restores the theorem. Voxelyze's √m scaling does **not**: varying voxel density
at fixed E makes `C_i/m_i ∝ m_i^{-1/2}` non-uniform, which is propulsion by
numerical damping.

**Theorem 1′ (heterogeneous linear damping, periodic steady state; derived here,
not in Lean).** For any `C_i > 0`, let `Y = Σ C_i x_i / Σ C_i` be the
damping-weighted centroid and `M = Σ m_i`. Integrating E1 with `f ≡ 0` gives
`M(V(t) − V₀) = −C_tot (Y(t) − Y₀)`. Take an orbit that is periodic in **shape
and velocity**: `ẋ_i(t+T) = ẋ_i(t)` and `x_i − x_j` is T-periodic. Then
`V(t+T) = V(t)`, so `Y(t+T) = Y(t)`. And `X − Y` depends only on the relative
coordinates `x_i − x_j`, so it is T-periodic. So a periodic shape
change gives **zero net displacement per cycle**, whatever the phase pattern or body
asymmetry.

**Consequence (necessity).** With only linear, lab-frame, velocity-proportional
external forces, nothing translates. Net locomotion needs a horizontal external
force that is *not* such a force:

- Coulomb friction: nonlinear and unilateral, active only while in contact.
- Direction-dependent friction (Section 4).
- Configuration-dependent anisotropic drag: resistive-force theory, slender-body
  hydrodynamics. **This is how cilia and flagella propel.**

A phase gradient or an asymmetric body is not sufficient on its own. It only helps
once one of these nonlinear or anisotropic forces is present.

## 3. The overdamped (cell-scale) limit

At cell scale the Reynolds number is tiny and inertia is negligible. PhysiCell
integrates exactly this regime (velocity = summed force; `Cell::update_position`
uses Adams–Bashforth-2).

**(E2)** `ξ_i ẋ_i = Σ_j F_ij + f_i^{ext}`, with `ξ_i` the drag coefficient
[N s m⁻¹; PhysiCell uses unit mobility, so velocity is in µm min⁻¹ per unit force].

**Theorem 2 (linear drag).** If `f^{ext} = 0`, then `Σ ξ_i ẋ_i = 0`. The
drag-weighted centroid is invariant at every step, for any heterogeneous `ξ_i`.
Lean: `drag_weighted_centroid_fixed` (forward Euler) and
`drag_weighted_centroid_fixed_ab2`, the two-step Adams–Bashforth update PhysiCell
runs, with any first-step coefficient. Corollary `linear_drag_no_net_displacement`:
after any cycle that returns the body to a translated copy of its shape, the
translation is zero. `linear_drag_near_cycle_bound` removes the need for exact
periodicity: if every node lands within `η` of a common translation `d`, then
`|d| ≤ η`.

This is the substrate analogue of Purcell's scallop theorem, but **stronger**: it
does not need reciprocal strokes. A travelling wave fails too, because the drag is
isotropic and does not depend on configuration. In real Stokes flow the drag does
depend on configuration, so non-reciprocal strokes *can* swim. The PhysiCell
cell-centre model omits that hydrodynamic coupling, and this is its main
limitation for ciliary transport.

**Engine test (PhysiCell, preregistered arms I1–I3 and N1).** A 29-cell strip with
a travelling contraction wave (`λ = 80 µm`, `ε = 0.1`) and isotropic drag moved its
centroid by **1.3·10⁻¹⁴ µm** in 10 cycles, while its x-extent oscillated by
7.7 µm. PhysiCell's own repulsion/adhesion potentials with prescribed cyclic radius
gave 4.5·10⁻¹⁴ µm. Details: Section 7.

## 4. Breaking the symmetry: the anisotropic-friction crawler

Two nodes, rear `a₁` and front `a₂`, with a prescribed length change `δ = a₂ − a₁`
per step. The friction force is direction-dependent:

    f(v) = ξ₊ v  (v ≥ 0),   f(v) = ξ₋ v  (v < 0)

Force balance: `f(a₁) + f(a₂) = 0`.

**(E3) Per-step law.** The midpoint moves by `κ |δ|`, with

    κ = (ξ₋ − ξ₊) / (2 (ξ₊ + ξ₋)).

This holds for contraction and extension alike. Lean: `crawler_step`, all four sign
cases.

**(E4) Pathwise law.** Over any actuation history, `ΔX = κ · TV(L)`, where
`TV(L) = Σ|δ_k|` is the total variation of the **realised** length. Lean:
`crawler_path`; the trajectory form with an explicit midpoint state `X(n)` is
`crawler_trajectory`.

Because E4 uses the *realised* length, the lag between prescribed rest length and
realised length (spring stiffness, period) drops out of the comparison. It only
sets how large `TV(L)` is. In continuous time E4 is exact, since `f(ẋ₁) + f(ẋ₂) = 0`
holds at every instant. In discrete time the per-step balance holds for the step
*velocities* `v_n`, but AB2 moves the node by `dt(1.5 v_n − 0.5 v_{n−1})`. That
mismatch is the 10⁻⁴ deviation, and it vanishes as dt → 0.

**(E5) Cycle law.** One contraction and one extension of amplitude `A` give

    D = A (ξ₋ − ξ₊) / (ξ₊ + ξ₋).

Lean: `crawler_cycle`.

Properties, all proved in Lean:

- `D = 0 ⇔ ξ₊ = ξ₋` (for `A ≠ 0`). Isotropy gives no motion, and anisotropy is
  **necessary and sufficient**: `crawler_zero_iff_isotropic`.
- Forward motion (`D > 0`) exactly when `ξ₋ > ξ₊`: `crawler_forward_iff`.
- Mirror law: swapping `ξ₊ ↔ ξ₋` negates `D`. `crawler_mirror` states this
  algebraically for the cycle formula. The node-level, dynamical statement is
  `crawler_step_equivariant`: reflecting and relabelling a balanced step
  `(a₁, a₂) → (−a₂, −a₁)` gives a balanced step for the exchanged drags, with the
  same `δ` and the negated midpoint. It rests on `fric_mirror`.
- `D` is linear in amplitude: `crawler_linear_in_amplitude`.

**Leading-order dependences in the overdamped crawler:**

| Dependence | Result |
|---|---|
| Amplitude | `D ∝ A` |
| Frequency | `D` independent of `ω` at fixed realised amplitude: the law is rate-independent |
| Damping / drag | enters only through the ratio `r = ξ₋/ξ₊`: `D/A = (r − 1)/(r + 1)`, saturating at 1 |
| Stiffness and period | enter only through the realised amplitude `A(kT)`. For a spring of stiffness `k` and drag `ξ`, `A → ε r₀` when `kT/ξ ≫ 1` and `A ≈ ε r₀ (kT/ξ)/(2π)` when `kT/ξ ≪ 1` (first-order low-pass) |
| Mean speed | `U = D/T` |

**Engine test.** The PhysiCell two-cell arm matches E4 with ratio 0.99989 at
dt 0.1, 0.99995 at 0.05 and 0.999989 at 0.025. The error falls ×2.3, then ×4.3, as dt halves; this is the AB2 discretisation of a law that is exact in continuous time. The
mirror arm gives exactly `−ΔX`, and the amplitude arms keep the same ratio.

## 5. Symmetry under nonlinear (Coulomb) friction: what the Voxelyze patterns can and cannot do

With Coulomb friction, E1 has no closed form. A symmetry argument still constrains
the motion. Let `R: x ↦ −x` be the mirror and suppose:

- (i) the body is mirror-symmetric;
- (ii) friction and damping are isotropic, so the dynamics are R-equivariant;
- (iii) the solution is unique.

**Caveat (gemini-4-argon review).** With dry Coulomb friction, (iii) can fail:
stick-slip indeterminacy, Painlevé-type non-uniqueness, Filippov set-valued
friction at zero slip. Nonsmooth systems also often have several coexisting
attracting periodic orbits. The argument below is therefore conditional on (iii).
A symmetric body can break symmetry spontaneously or through solver tie-breaking,
and the predictions P-V1 to P-V3 partly test exactly this.

Then mirroring the actuation pattern, `φ ↦ φ∘R`, maps the trajectory to its mirror,
so `D(φ∘R) = −D(φ)`. This is the `mirror-symmetry` endpoint. If the pattern is
itself mirror-symmetric, `D = −D = 0`.

Half-period shift. A front/back antiphase pattern is mirror-symmetric up to a
half-period time shift. On a *unique attracting* periodic orbit, the per-cycle
displacement does not depend on that shift, so the steady per-cycle displacement is
again zero. The transient is not constrained.

**Post-hoc check against stored runs (NOT a preregistered test).** The driver's
`longitudinal` pattern is `φ = 0` for `x < nx/2`, else `π`
(`scripts/voxel_actuation/soft_actuation.cpp:55`). For odd `nx` this splits 2 vs 3
(or 3 vs 4) voxels, which breaks (i). Stored runs:

| nx | split | net, 5 cycles | per-cycle dx, cycles 2–3 |
|---|---|---|---|
| 4 | symmetric | 0.020 BL | −0.012, −0.007 mm |
| 6 | symmetric | 0.0086 BL | −0.014, −0.014 mm |
| 5 | asymmetric | 0.153 BL | −1.20, −1.20 mm |
| 7 | asymmetric | 0.080 BL | −0.91, −0.91 mm |

The even-nx motion is transient-dominated: −0.54 and −0.33 mm in cycle 1, then
small and irregular. The odd-nx drift is steady from cycle 1. The same rule explains
`lateral` (ny = 3, odd split along y): 0.141 BL in **y**, with x ≈ 0. It also
explains `dorsoventral` (split along z, x-mirror intact): 0.003 BL in x.

**This reframes the existing six-pattern ranking.** Part of what was read as
"pattern dependence" is a body/pattern *asymmetry from integer division*, not
an effect of the phase pattern itself.

**Forward prediction for ff-xeno (falsifiable):**

- **P-V1.** With the frictional floor on and `nx ∈ {4, 6, 8}` (symmetric split),
  the mean per-cycle x-displacement over cycles 6–20 is below 10 % of the `nx = 5`
  value and shrinks under dt refinement.
- **P-V2.** For `nx ∈ {5, 7}`, mirroring the pattern (`φ(x) → φ(nx − 1 − x)`)
  negates the steady per-cycle x-displacement to within the dt-refinement change.
- **P-V3.** For frictionless contact (μ = 0) with homogeneous mass, every pattern
  gives zero horizontal COM displacement (Theorem 1). With deliberately
  heterogeneous voxel density, the COM moves (the Lean counterexample); this
  separates numerical-damping propulsion from friction propulsion.

**Falsifiers.**

- P-V1 fails if symmetric-split bodies keep a steady drift of the same order as
  asymmetric ones. That would mean a symmetry-breaking element is missing from this
  account: float32 ordering, floor-contact asymmetry, or multiple attractors.
- P-V3 fails if a frictionless homogeneous body moves, which would contradict the
  source force law.

## 6. Ciliary versus contractile: what transfers

| Item | Contractile body (modelled here) | Ciliated surface (what the sources report) |
|---|---|---|
| Mechanism | shape change of the body; needs a nonlinear or anisotropic substrate force | surface slip velocity `u_s` from ciliary beating; the body does not need to deform |
| Leading-order speed | crawler: `U = A f (r − 1)/(r + 1)` | squirmer: `U = (2/3) B₁` (standard Lighthill–Blake squirmer result, quoted, not derived or checked here), with `B₁` the first slip mode, set by cilia density and beat |
| Does Theorem 2 apply? | yes: isotropic linear drag means no motion | no: the propulsive force is an active surface traction, not internal |
| Which engine fits? | Voxelyze (inertial, friction) and PhysiCell (overdamped) | neither: needs a Stokes / boundary-element solver |

The Lean family is about the contractile mechanism. It does **not** model the
reported ciliary mechanism. It only says that if the construct moves by
contraction alone on a surface or in fluid, a named symmetry-breaking ingredient
must be present.

## 7. PhysiCell results

### 7a. Preregistered protocol (`artifacts/xenomodel/physicell-protocol.json`)

All 18 frozen checks pass (`artifacts/xenomodel/physicell-results.json`):

- Passive controls (ε = 0): ΔX = 0 exactly.
- Isotropic drag, pair / travelling strip / standing strip: |ΔX| ≤ 1.3·10⁻¹⁴ µm.
- Native PhysiCell potentials with a travelling radius wave: 4.5·10⁻¹⁴ µm.
- Anisotropic drag (ξ₋/ξ₊ = 3):
  - pair: 7.63 µm per 10 cycles, matching `κ·TV(L)` to 1.1·10⁻⁵ at the finest dt;
  - strip, standing wave: 7.21 µm;
  - strip, travelling +x: 12.44 µm;
  - strip, travelling −x: 12.39 µm.
- Mirror arms: exactly negated.
- Pattern dependence (equal total actuation): standing vs travelling differ by
  5.24 µm against a dt-refinement change of 1.8·10⁻⁴ µm, so the pass is decisive.
  Travelling +x vs −x differ by only 0.058 µm, which still passes (it is 320× the
  refinement change) but is small.

**Correction after the convergence check (7b):** the +x vs −x difference is mostly
a discretisation effect. The preregistered pass stands as recorded, but it does
**not** license a claim that wave *direction* controls motion in this model. What
survives refinement is travelling vs standing.

### 7b. N-node convergence (not preregistered; requested by the argon review)

`artifacts/xenomodel/physicell-chain-convergence.json`. Setup: a chain of fixed
length 128 µm, N = 5 to 65 nodes, continuum scaling (node drag ∝ r₀, spring
k ∝ 1/r₀, dt ∝ r₀²), ξ₋/ξ₊ = 3, λ = 64 µm.

| N | standing ΔX (µm) | travelling +x | travelling −x | (+x) − (−x) |
|---|---|---|---|---|
| 5 | 6.351 | 12.138 | 12.054 | 0.0842 |
| 9 | 7.386 | 10.739 | 10.708 | 0.0308 |
| 17 | 7.883 | 10.221 | 10.211 | 0.0093 |
| 33 | 8.105 | 10.082 | 10.077 | 0.0048 |
| 65 | 8.207 | 10.043 | 10.039 | 0.0037 |

- Standing ΔX converges at first order (successive-difference ratio ≈ 2.1),
  extrapolating to ≈ 8.31 µm.
- Travelling converges faster (ratio ≈ 3.6), to ≈ 10.03 µm.
- The direction difference falls 23×. Its successive differences shrink about 4×
  per refinement, so it approaches ≈ 0.003 µm (0.03 % of ΔX). Whether the
  continuum limit is exactly zero is **not resolved**.
- Travelling vs standing (≈ 18 %) persists.

### 7c. Descriptive factorial sweep (not preregistered)

`artifacts/xenomodel/physicell-sweep.json`: 324 strip runs over λ ∈ {standing, 40,
80, 160, 320 µm} × direction × ε ∈ {0.05, 0.1, 0.2} × period ∈ {6, 30, 150 min}
(k·T = 3, 15, 75) × ξ₋/ξ₊ ∈ {1, 1.5, 3, 10}. All exit 0.

- **All 81 isotropic runs:** |ΔX| ≤ 1.6·10⁻¹³ µm (Theorem 2 across the whole sweep).
- **Amplitude:** the normalised displacement per cycle,
  `ΔX/cycle ÷ ((r−1)/(r+1) · ε · r₀)`, averages 1.455, 1.456 and 1.457 at
  ε = 0.05, 0.1, 0.2. The motion is linear in ε, as in the crawler law.
- **Drag ratio:** after dividing by `(r−1)/(r+1)`, the means are 1.53, 1.44 and
  1.39 for r = 1.5, 3, 10. The crawler factor captures the leading-order
  dependence to about ±10 %.
- **Stiffness × period:** the strongest remaining lever. Means are 0.62, 1.34 and
  2.41 for k·T = 3, 15, 75, because a stiffer or slower drive realises more of the
  prescribed length change.
- **Wave direction:** median relative effect 0.47 % (max 4.6 %), consistent with 7b.

*Not established:* any of this in physical units. Nothing is established about any real substrate's drag anisotropy, any real
tissue's contraction, or any physical-unit speed. Section 8 lists the measurements
that would supply these.

## 8. Calibration that would close the couplings

See `artifacts/xenomodel/calibration-design.json`. It names the measurement for the
actuation-to-stress and stress-to-deformation ports, and for the anisotropy ratio
`r` that this model shows to be the controlling parameter.
