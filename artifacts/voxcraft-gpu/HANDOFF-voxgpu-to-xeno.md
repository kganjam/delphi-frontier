# voxgpu -> ff-xeno: voxcraft-sim on GPU and your three preregistered endpoints, executed
From claude-voxgpu. Branch `claude/voxgpu-20261101` of kganjam/delphi-frontier. Updated 2026-11-01 ~10:45 PST.
Every number below comes from a completed job with a receipt in `artifacts/voxcraft-gpu/`. All are simulations, not observations.

## 0. One-paragraph summary
The published CDO engine (voxcraft-sim dd8668f, CC0 per its LICENSE; the cdorgs website says CC BY-NC, conflict unresolved)
**runs unmodified on Nebius L40S** when built in its own pinned CUDA 10.2 image with a PTX-only gencode. It **cannot run on
H100 with any toolchain**, because the driver refuses device-side `cudaDeviceSynchronize` on sm_90+ (error 225). On the
unmodified engine your endpoints come out **passive-control PASS, pattern-dependence PASS, mirror-symmetry FAIL**, all
thresholds frozen before data. The mirror failure is systematic and deterministic, not noise: a post-hoc perturbation
ensemble shows it at 18–500 standard errors. It also appears tied to contraction/contact dynamics, because the same solver
under voxcraft's own cilia-thrust model is mirror-symmetric to ~2e-5, except right at the friction threshold.

## 1. Engine status
| arm | GPU | result | receipt |
|---|---|---|---|
| B: pinned `cuda:10.2-devel-ubuntu18.04` @sha256:8bd2ef1f, unmodified, `-DCUDA_ARCH=arch=compute_75,code=compute_75` | L40S (sm_89), driver 580.173.02 | build rc 0 (26 s); stock demo PASS | armb/RECEIPT.md |
| same | H100 (sm_90) | build rc 0; RUN_FAIL at the first cudaMalloc | armb/RECEIPT.md |
| minimal discriminator | H100 | plain PTX kernel runs; CDP1 module -> error 225, driver JIT log: `ptxas fatal: Unsupported Function 'cudaDeviceSynchronize' on arch 'sm_90' or higher` | h100-diag/job.log |
| disclosed FORK (child grids -> serial loops; `fork/`) | H100 | runs (demo PASS). It is NOT the published engine and no physics result from it is used below | fork/README.md |

Throughput of the unmodified engine on L40S is about 17k simulation-steps/s regardless of batch size, because device-side kernel
launches are the bottleneck. At E = 1e6 Pa (dt ≈ 4.5e-5 s), 1000 bodies × 6 s did not finish in 1 h. That is the practical limit
on population scale with this engine on this hardware.

## 2. Your endpoints (`scripts/voxgpu/PREREGISTRATION.md`, committed before the first sweep job)
Model: solid 8×4×3 block of 10 mm voxels (80×40×30 mm, E = 1e6 Pa, ρ = 1000, ν = 0.35), gravity, floor, Coulomb friction
μs = 1 / μd = 0.8. Every voxel contracts via voxcraft's thermal proxy (contraction only, 10% peak strain, 4 Hz). Patterns
differ only in phase, so commanded actuation is equal; this is not equal mechanical work. d = COM(6 s) − COM(1 s), i.e. the
first 1 s is a stated transient window. Refinements: DtFrac 0.9 / 0.45 / 0.225 and a 16×8×6 mesh at 5 mm. 132 runs, 0 diverged,
and 3 replicates per case that are bitwise identical.

| endpoint | verdict | numbers |
|---|---|---|
| passive-control | **PASS** | max \|d\| = 2.5e-9 m over 12 runs (tolerance 1e-5 m) |
| pattern-dependence (travelling wave vs synchronous) | **PASS** | 45.01 mm vs 0.025 mm; difference 45.0 mm > largest refinement change 6.4 mm (mesh: 45.0 → 51.4 mm) |
| mirror-symmetry | **FAIL** | x-mirrored wave 0.95% (within the 1% bound); x-mirrored half-split 1.48%; y-mirrored diagonal 1.39%; y-mirrored short-axis wave **15.1%** (5.19 vs 4.41 mm) |

Per your falsifier, the mirror failure marks an anisotropy artifact in the solver: body and phase fields are exactly
mirrored. What I measured about it:
- **It is not perturbation noise** (post-hoc, `ensemble-l40s-e2-unmodified/`). Over 24 members with every phase perturbed by
  N(0, 1e-7 cycles), the spread is 0.006–0.09 mm, while the mirror error of the ensemble means is 0.25–1.0 mm (18–500 SE).
- **It depends on discretisation.** The transverse drift of the y-symmetric wave is +0.55 / +0.75 / −1.26 mm at
  DtFrac 0.9 / 0.45 / 0.225.
- **It is tied to contraction/contact dynamics** (cilia arm, below). With constant-thrust cilia, the same solver is
  mirror-symmetric to ≤ 2e-5 relative.

Practical rule: with this engine at these settings, mirror or chirality statements below about 1–2 mm (about 2–3% of |d|)
are not supported, and short-axis patterns are unresolved at 10 mm (5.2 mm coarse vs 22.5 mm fine for the y-wave).
**Do not read pattern-to-motion differences smaller than the refinement change (6.4 mm here).**

## 3. Cilia arm: the sources' actual mechanism (prereg Addendum A, written before the run)
voxcraft has a cilia model: `EnableCilia`, plus a per-voxel `BaseCiliaForce` that applies a constant body-frame thrust on
surface voxels. Same block and floor; |f| is the same on every voxel and in every pattern.
- C1 passive **PASS**: 2.5e-9 m.
- C2 pattern-dependence **PASS**: uniform +x gives 762.9 mm, swirl gives 0; dt change 0.0035 mm.
- C3 mirror **FAIL**: 23 of 24 pairs pass, most to < 1e-5. The single failure is at the friction threshold: F = 0.01 N/voxel,
  +y stuck at 11.7 mm while −y slid 71.1 mm at DtFrac 0.9, and both slid 71.1 mm at 0.45. Per the rule fixed in advance, the
  asymmetry is therefore not specific to contraction. Near a stick/slip threshold, outcomes are dt-sensitive and
  mirror-sensitive.
- Displacement vs force is a threshold: 0.005 N gives 0, 0.010 N gives 71 mm, 0.020 N gives 763 mm over 5 s.

This is frictional sliding under a prescribed thrust, NOT ciliary swimming: there is no fluid, and the force values are
arbitrary.

## 4. What this does not say
- Not tissue. Not calibrated: there is no measured modulus, contractility or ciliary force.
- No fluid, so deformation-to-motion is ground contact only.
- None of your four missing couplings is closed. Contraction remains the project's modelling choice; the sources report cilia.
- Not a reproduction of Kriegman 2020 or Blackiston 2021.
- No convergence claim: the mesh changes the wave by 14% and the short-axis wave by 4.3×.

## 5. Population (lite config, disclosed: E = 1e5 Pa, self-collision off, 4 s run, 1 s transient)
- 250 seeded random bodies (6×6×5 box, smooth random active/passive tissue and phase field, seed 20261101), each run four ways:
  actuated, passive control, x-mirror and exact duplicate. That is 1000 simulations on the unmodified engine (L40S). The same
  1000 were rerun on the FORK on H100 and are **bitwise identical, 1000/1000** (plus 33/33 lite endpoint bodies; report
  sha256 identical). Duplicates are bitwise identical, 250/250.
- **79/250 (32%) passive controls move ≥ 10 µm** after the transient (up to 11 mm): random bodies keep settling or toppling.
  Under your passive-control rule, their actuated motion cannot be read as pattern-driven.
- Among the 171 bodies whose passive control holds: median |d| is 1.36 mm, and the x-mirror error has a median of **9% of |d|**
  (90th percentile 34%); only 0.9% meet the 1% bound. On this engine and config, ranking random bodies by displacement
  partly ranks solver asymmetry. A CDO-style search here would need a mirror-consistency filter, and probably finer dt and mesh.
- More fork population runs on H100 (candidates 250–2999) are in flight. They will only be added if they complete.
- Results page (private to the owner until shared): https://claude.ai/artifact/SZVbUyApekVWkrpMmi3sd5

## 6. Suggested use on the tissue-microcarrier page
Your three endpoints are executable and they discriminate: two pass, and mirror fails with a measured cause. I suggest
quoting them as "voxcraft-sim dd8668f, unmodified, L40S: passive PASS, pattern-dependence PASS, mirror-symmetry FAIL
(systematic solver asymmetry under contraction-on-friction; ±1–2 mm at 45 mm)", with the scope line from section 4.
Do not quote any fork number as the published engine.
