# Xenobot design space — working notes

**The design space:** a biological machine that does work on something other than itself.

**Verdict asked for up front, because it is the main finding.** The voxel-actuation
artifact's gait ranking **should not be quoted as a ranking of gaits for a xenobot.**
Not because the simulation is wrong — it reproduces bit-for-bit, here and on a
different machine — but because five of the six patterns it ranks are time-reciprocal,
and the object it is about lives at a Reynolds number where a time-reciprocal stroke
produces exactly zero net displacement. Its 2nd and 3rd places are dead, not slower.
What can still be quoted is the artifact's own `extracted_relation` — that net
displacement comes from spatial asymmetry of the actuation phase field rather than from
amplitude — which is correct and, as it happens, is the scallop theorem arriving by
another route.

---

## 1. What I did

Three studies, all simulation, no organism measured.

| study | question | answer |
|---|---|---|
| `regime-check` | does the gait ranking transfer to the regime a real construct occupies? | **no**, and the failure is qualitative |
| `convergence` | does the model converge, and was the flagged swing a resonance? | **no**, and **neither** — it was the encoding |
| `cargo-work` | does the best self-mover also push best? | **yes**, which refutes my own predeclared expectation |

Voxelyze was built at the pinned commit `4287e365e11416dd108f2f361e9ec4c5a011a16c`
(dropping `-DPARDISO_5=1` from `FLAGS`, as the handoff packet says you must) and
reproduces the published travelling-wave run **exactly**: `0.0145773 m` against the
stored `0.014577281 m`. It also reproduced it to the full nine stored decimals on a
Nebius L40S node under a different OS image, which is a stronger determinism check than
the protocol's claim of bitwise-identical repeat runs on one host.

### The three results, briefly

**1. Regime.** Re = ρUL/μ in water at 20 °C. From the sizes and speeds the papers
themselves report, anthrobots sit at **Re = 1.5×10⁻⁴ to 2.5×10⁻²** (Gumuskaya et al.
2023, 30–500 µm at 5–50 µm/s); a nominal 1 mm xenobot at 0.1 mm/s is at **Re = 0.0996**.
The artifact's own body, at its own simulated 50 mm and 12.9 mm/s, would be at
**Re = 643** — 3.8 orders of magnitude away. (It contains no fluid at all, so that is a
comparison of scales, not a property of it.)

Then the exact part. Writing the drive as `T(t) = sin(ωt)·cos(φ) + cos(ωt)·sin(φ)`, the
control traces a closed curve in the span of those two vectors, and it is a retraced
segment — time-reciprocal — exactly when that 2×N matrix has rank ≤ 1. Transcribing
`phaseFor` from the pinned driver: **uniform, longitudinal, lateral, dorsoventral and
checker assign only the phases 0 and π**, so `sin(φ) ≡ 0`, rank 1, enclosed area
1.9×10⁻¹⁶. Only `travelling` (φ = 2πx/nx, five distinct phases) has rank 2. An RPY
bead-model Stokes swimmer confirms it numerically.

**2. Convergence.** On a parity-matched refinement — outer envelope and *physical*
actuation field held fixed while the lattice refines 4× from 45 to 2880 voxels — the
travelling wave spans **41%** of its coarsest value and the longitudinal split **54%**,
and **both series turn over**. The winner is stable at all four levels; the margin falls
from 19.4× to 10.4× and is still moving at the finest grid.

Temporal error does not explain this. Repeating levels 1–3 at **half the timestep**
leaves the travelling wave's spread essentially unchanged (22.4% → 21.8%) while any
single level moves by at most 1.3%, so spatial error dominates by about 17×. For the
longitudinal split the temporal error is **not** negligible — up to 15.5% at level 2 —
but halving dt still only moves its spread from 54.4% to 48.5%, so it does not explain
that either. (This does not contradict the artifact's own arm F, which found 0.9%: arm F
ran nx = 5, the *asymmetric* split, whose displacement is an order of magnitude larger,
so the same absolute error is a much smaller relative one.)

**Why it does not converge, found by accident and then measured.** Cross-checking the
local series against an independent run of the same 14 configurations on a Nebius L40S
node, **12 of 14 were bit-identical** — a stronger determinism check than the protocol's
claim about repeat runs on one host. The two that disagreed were exactly the level-3
grids, where voxel = 1/300 m: locally I passed the full double-precision value, the
remote job a 10-digit literal. Re-running locally with the 10-digit value reproduces the
remote number **exactly**, so the engine is not at fault — but the size of the
disagreement is the finding. A relative input perturbation of **1.0 × 10⁻⁸** changes net
displacement by **1.2 × 10⁻²** for the symmetric longitudinal split, an amplification of
about **10⁶**, and by 1.1 × 10⁻⁴ for the travelling wave, about 10⁴. The quantity being
refined is not a well-conditioned function of its inputs at these configurations. That
explains the non-convergence directly, and it predicts further refinement would not cure
it: the spread is not discretisation error shrinking with h. (One perturbation of one
parameter at one level per pattern — it establishes ill-conditioning, it is not a
condition number, and should not be quoted as one.)

The flagged "non-monotone ten-fold swing" is the **encoding**. `longitudinal` splits at
index `nx/2`, so odd nx gives an asymmetric actuator layout and even nx a symmetric one;
sweeping nx = 3…16 gives **two smooth monotone branches interleaved**, and the four
points the audit flagged are two adjacent points of each. Two discriminators declared in
advance both fail for a resonance: the alternation is absent from `travelling` (median
factor 1.008 against longitudinal's 20.3), and the optimum frequency does not move with
body length (12 Hz at both nx = 4 and nx = 8, while the body doubles).

**3. Cargo.** Contact-gated, 40 cycles. Travelling is first on every metric: 103.6 mm of
cargo moved against 35.8 and 21.7; transport ratio 0.95 of its own path transferred
against 0.51 and 0.26; 7× the useful work per unit actuation energy. All three
contacting gaits stall at the same **64 g** cargo and efficiency peaks just below it.
The swarm **disperses** rather than aggregating, in 28 of 30 runs — and the two exceptions,
both at the largest swarm size, turned out to be a **boundary effect** rather than an
onset (below).

---

## 2. Corrections and qualifications to the existing artifact

Stated openly, as asked, rather than fixed silently.

1. **The gait ranking does not transfer.** Covered above. The artifact never claimed it
   would — its `what_this_cannot_establish` says "that a pattern ranking in this
   simulator transfers to another simulator or to matter" — so this is a *confirmation*
   of a limit it declared, made specific. What is new is that the failure is not a
   gradual loss of accuracy but an exact zero for four of six.

2. **Arm G's "no convergence" holds, and removing the parity confound does not fix it.**
   The audit's `G_actual_SI_coarse_to_fine_ratio = 7.25` and its status line "spatial G
   unresolved" are now resolved **as a negative**. Most of the 7.25 was parity; what
   remains still does not converge, on either pattern, across four levels.

3. **The parity diagnosis was right and can be stated much more strongly.** The
   artifact's post-hoc marked hypothesis 2 `SUPPORTED` from four points (nx = 4,5,6,7)
   and correctly cautioned it was "a DIAGNOSTIC, not an isolated cause" because count,
   length and mass vary together. Fourteen points plus a parity-free control plus a
   frequency sweep turn that into a much firmer claim: it is the encoding, each branch
   is smooth and monotone, and it is not a resonance. The caveat about count/length/mass
   still stands and I have not removed it.

4. **One thing I think the artifact's framing gets wrong, and the audit did not catch.**
   Its premise is that spatial actuation phase patterns are how a xenobot-like construct
   locomotes. Read from Kriegman et al. 2021's Materials and Methods, the published
   simulations of cilia-driven constructs model propulsion as **an impulse force on each
   surface voxel**, not as a volumetric gait; and Kriegman et al. 2020's contractile
   designs give each voxel a **random fixed phase offset** from a 2 Hz central pattern
   generator and evolve the *geometry* to rectify that randomness. Neither is a
   hand-designed deterministic phase field. So the six-gait comparison describes a
   machine the literature does not build. This does not make the artifact wrong — it is
   explicit that "Xenobot-inspired names the design pattern, not biology" — but the page
   should say which published construct, if any, each result is about.

5. **The strongest single source finding, and it cuts both ways.** Kriegman et al.
   2020's **first pass used dry gravity-plus-friction ground contact and failed**: it
   produced "highly performant but nontransferable designs with powerful, bounding
   gaits", airborne for 47% of the cycle, while the real deciliated organisms "always
   kept part of their ventral surfaces in contact with the surface of the dish due to
   negative buoyancy". They fixed it by adding first-order hydrodynamics — reduced
   effective gravity for buoyancy, drag on every surface voxel face — after which ground
   contact went from **52.7% to 93.3%** of the evaluation period. The voxel-actuation
   artifact uses the configuration they abandoned. That is a much more concrete
   indictment than my theoretical argument, and it is *their* measurement, not mine.

---

## 3. What I could not do

- **voxcraft-sim does not build at its pin against a modern toolkit, and that is now a
  measured result rather than a gap.** It is the GPU engine this literature actually
  uses, so building it would have been the strongest available check on everything here.
  The probe ran on a Nebius L40S node in `nvidia/cuda:12.4.1-devel-ubuntu22.04`
  (nvcc 12.4.131, CMake 3.22.1). Pin verified, `PIN-OK`. **Both arms configured cleanly
  (`cmake rc=0`) and both failed to compile (`MAKE-EXIT=2`)**, for two independent
  reasons:
  1. **CUDA.** voxcraft-sim calls `cudaDeviceSynchronize()` from `__device__` functions,
     which CUDA 12 removed. Verbatim first error:
     `VX3_VoxelyzeKernel.cu(269): error: calling a __host__ function("cudaDeviceSynchronize") from a __device__ function("VX3_VoxelyzeKernel::doTimeStep") is not allowed`,
     at seven sites (lines 232, 269, 303, 312, 428, 437, 446) across `doTimeStep`,
     `updateTemperature` and `updateAttach`.
  2. **Boost.** Independently, nvcc cannot compile Boost.Asio's trait machinery reached
     through `boost::process` when building `VX3_SimulationManager.cu`:
     `/usr/include/boost/asio/traits/static_query.hpp:85:47: error: ''indirect_ref' not supported by dump_decl<declaration error>' is not a template`.
     This would remain even if (1) were patched.

  The PTX arm (`arch=compute_75,code=compute_75`) does not help, because the failure is
  at **compile** time, so there is no PTX to JIT forward. Also confirmed from the file
  bytes: the LICENSE at that commit is **CC0 1.0 Universal**, against the project
  website's claim of Attribution-NonCommercial — the conflict is quoted, not resolved.
  **No cross-engine comparison is offered anywhere on this page and none should be
  inferred.** What this does NOT establish: that voxcraft-sim cannot be built at all. We
  tested one toolkit on one platform; the pinned `cuda:10.2-devel-ubuntu18.04` route was
  not attempted. Full receipt in `data/voxcraft-probe.json`, log in
  `logs/voxcraft-probe-full.log`, job `aijob-e00n37n2d6cn00af86`.
- **The Nebius refinement eventually ran in full** (14/14, after the fix below) and is
  what made the conditioning finding above possible. The first attempt produced nothing:
  **it reported `COMPLETED` while every run inside exited `rc=127`**, because I used
  `/usr/bin/time -v` and never installed `time` in the `ubuntu:24.04` image. I only
  found that by reading the log rather than the status.
- **The first Nebius refinement job ran and produced nothing**, which I only found by
  reading its log rather than its status. It reported `COMPLETED`; inside, all 14 runs
  exited `rc=127` because I used `/usr/bin/time -v` and never installed `time` in the
  `ubuntu:24.04` image. The regression control inside that same job *did* run, which is
  where the cross-machine bit-identical reproduction above comes from. The refinement
  series in this page is therefore **local**, and a corrected job was resubmitted.
- **No measured biological parameter anywhere.** Every mechanical number in all three
  studies is `assumed`. There is no measured modulus for xenobot tissue, and Pai et al.
  2025 give a specific reason to doubt that one borrowed from embryonic epidermis would
  apply: at least 537 non-epidermal transcripts are upregulated in these cells relative
  to age-matched embryos.
- **bioRxiv was not searched by keyword.** The available tool takes date range and
  category only, not keywords. The negative in §5 is scoped accordingly.
- **Only two of six gaits were refined.** So no corrected ranking at a fine grid exists.
- **Level 4 was not repeated at the halved timestep**, so the temporal/spatial separation
  covers levels 1–3 only.

---

### The one hint I chased rather than hedged

The main swarm arm showed the field dispersing at every N from 1 to 6 in all five seeds,
then at N = 8 the median dispersion fell 2.6-fold and **2 of 5 seeds turned negative**.
That is the shape of an onset, so instead of writing "within the seed spread" I widened
the field in y, held particle **density** fixed, and pushed N to 16 — 20 more runs.

It is not an onset. In the wider field, N = 8 shows **nothing** (0 of 5), and so does a
*larger* swarm at N = 12. Pooling all ten configurations across both fields, the thing
that predicts aggregation is not swarm size but **how much of the arena the swarm
spans**:

| swarm span ÷ field half-width | configurations | aggregating seeds |
|---|---|---|
| ≤ 0.68 | 8 | **0** of 40 |
| ≥ 0.84 | 2 | 3 of 10 |

N = 8 is the controlled comparison: span ratio 0.84 in the narrow field (2/5 aggregate),
0.44 in the wide field (0/5), same swarm size. What looked like corralling is the swarm
reaching the edge of its dish and sweeping particles into a narrower band. The main
conclusion stands and is stronger for having been attacked: **a uniform, sensorless,
single-gait swarm sweeps and does not corral, over N = 1 to 16.**

Two honest caveats: the cut sits between 0.68 and 0.84 with nothing in between, so the
threshold is *bracketed, not located*; and two field widths is not a scan over field
width. Also worth recording: the arm's own automatic test — "does the median fall
monotonically with N and cross zero?" — returned *"consistent with seed scatter"*. That
verdict is in the artifact, superseded, because the pooled span analysis is a better
explanation than the one I had pre-registered for that arm.

## 4. Mistakes I made, and how they were caught

Recorded because they bear on how much to trust the rest.

1. **The swarm arm's first version was silently degenerate.** Constructs were
   auto-spread over a square field, which pushed the outermost ones *outside* it at
   N = 6 and N = 8 — so those two sizes returned **bit-identical** particle outcomes.
   Caught by noticing two identical medians, not by any check I had written. That run is
   discarded and not reported. The driver now **exits 4** if any construct is placed
   outside the field, and the guard was tested against a case it must refuse.
2. **The first cargo arm measured reach, not push.** With the cargo one clear lattice
   site away the surfaces are 7.5 mm apart and only `travelling` covers that in 5
   cycles, so every other gait scored exactly zero for a reason that has nothing to do
   with pushing. Fixed by adding a contact-gated 40-cycle arm; the 5-cycle result is
   kept and reported as a *reach* result, because it is a real engineering fact.
3. **My own declared efficiency metric breaks past the stall threshold.** M4 uses the
   cargo's *path length*, so a stalled cargo being jiggled still accumulates friction
   work: travelling at 256 g reports the **highest** M4 of the whole sweep (0.134) while
   moving the cargo 0.105 mm. Found only because I swept far enough to stall. Both M4
   and a net-displacement version are reported; M4 is the declared metric and is not
   deleted.
4. **A units error in a figure**: body length labelled "30 cm" for a 3 cm body, from
   `(nx-1)*10` read as centimetres. Caught by looking at the rendered figure.
5. **A stale number survived into two routes** — `app-heavy-cargo-efficiency` quoted
   efficiencies from the superseded reach-limited 5-cycle arm (0.43%/4.6% instead of
   0.8%/8.2%), and `body-parity-of-the-split` quoted a parity range of "5× to 30×" when
   my own 13 adjacent pairs span 7.6× to 66×, median 23×. Both were caught by
   `code/verify_numbers.py`, which now reconciles every headline number in prose against
   the data file it comes from and exits 1 on a mismatch. It is worth re-running after
   any edit.
6. **Two figures initially misled.** Clamped bars on a log axis made five exactly-zero
   values look substantial, and a dual-axis panel let me choose the comparison. Both
   rebuilt.

---

## 5. Source disagreements and scoped negatives

- **Licence conflict, unresolved and quoted both ways.** `cdorgs.github.io/code` states
  the code is under Attribution-NonCommercial Creative Commons; the repositories it
  links carry **CC0-1.0** LICENSE files. (Relayed from the handoff packet, not
  re-verified by me.) Separately, Voxelyze has **no LICENSE file** at the pinned commit,
  so the GitHub API reports `license: null` while every source header declares
  LGPL-3.0-or-later. Null means "no detectable LICENSE file", not "unlicensed".
- **Object transport versus object aggregation, which are routinely blurred.** Read from
  Kriegman et al. 2020's full text: debris/particle **aggregation** is observed *in
  vivo*, individually and in groups over 24 h. Object **transport** via a pouch is *in
  silico only* — the pouch topology was realised in vivo but "was not layered with
  contractile tissue", so that organism could not move. The page must not merge them.
- **Scoped negative on the application question.** Searching PubMed and Consensus for a
  xenobot or anthrobot deliberately transporting a *defined external cargo* found
  nothing. What exists is aggregation as a reported side effect of locomotion, plus
  transport in simulation. bioRxiv keyword search was unavailable. The positive control
  on that search is that the same queries *did* return the aggregation results, the
  self-replication paper and the anthrobot papers, so the search was working.
- **Read-levels are mostly `listing`.** I verified 36 PMIDs through PubMed — title,
  journal, volume, pages, DOI — but read the *abstract* for only about 18 of them and
  the *full text* for two (Kriegman 2020 and 2021). Four physics citations (Purcell
  1977, Najafi & Golestanian 2004, Lauga 2007, Lauga & Powers 2009) are not in PubMed
  and are labelled `search-summary`: **their volume, page and DOI details were not
  independently verified by me** and should be checked before the page prints them.

---

## 6. Should the existing gait ranking be quoted at all?

**As a ranking of gaits for a xenobot: no. Withdraw it.** Four of its six entries are
exactly zero in the regime the object occupies, and the two that are not — travelling
first, longitudinal second — have a margin that moves by 2× under grid refinement and is
still moving at the finest grid I ran.

**As a property of a particular numerical soft-body model under declared parameters:
yes, and it is correctly labelled that way already.** The artifact's own scope statement
and `what_this_cannot_establish` list are accurate. The problem is not that it
overclaimed; it is that a correct, carefully-hedged result about a 50 mm dry-friction
object is easy for a later reader to quote as a result about a 1 mm construct in water.

**What I would put in its place, because it survives the regime change and is cheaper
than any simulation:** the rank test. Write the per-unit drive as
`sin(ωt)·cos(φ) + cos(ωt)·sin(φ)` and take the rank of that 2×N matrix. Rank 1 means
reciprocal means zero. It takes a minute, it needs no simulator, and it eliminates five
of the six published patterns before anyone spends a CPU-hour on them.

**And the limit on my own claim, which I will not bury.** The scallop theorem is about a
*free swimmer*. A xenobot crawling on a dish bottom with its ventral surface in contact
is not one: surface friction is not Stokes drag and sits outside the theorem's
assumptions, so a reciprocal gait *can* rectify against a surface. The defensible
statement is narrower than "the ranking is wrong everywhere" — for a free or
near-neutrally-buoyant construct the ranking is void; for a surface crawler the
dry-friction model's *mechanism* may be qualitatively right while its magnitudes come
from an object 3.8 orders of magnitude away in Reynolds number. And most published
constructs are cilia-driven, where there is no body gait to rank at all.
