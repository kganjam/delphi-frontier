# Independent bounded review of the frozen RD-DDPM pilot

Reviewed source: `origin/work/rd-diffusion` at
`4a5394f3d19601f3c7a75d08f7f3dc46acc6e1b5`.
Code SHA256 `25455430ef138b49e6bac151a144e338269a81ce5c2f576387f8805bbb1a400a`;
config `bc77ebc55010b9c8ac910c2b31868ec0dbf2d1e3785a06ec3ef1aa028ea2b210`;
PREREG `3f6f2c4d9187ced1e9a0d0979a73bd1532bb02c863634e924a9c89da70b5ab8f`.
This review did not edit the frozen code, config or preregistration, train a model,
load trained weights, or inspect held-out outputs. The admitted job may continue
unchanged; any affected claims need the qualifications below. Do not silently
replace its metric or tune using its holdouts.

## Executed quick checks versus source-only findings

Executed under one CPU / one thread / 4 GiB / zero swap / 128 tasks / 600 s:

- Enumerated split `(setting, seed)` identities: 4200 train,100 dev,600 test_param,
  300 test_seed and1280 ensemble pairs, with zero pairwise intersections.
- Instantiated the untrained network only:1,348,290 parameters. No optimizer step.
- Inspected actual convolution padding: `d1` and `d2` use zero padding; stride-one
  residual convolutions use replicate padding.
- Evaluated pure metric functions on explicitly synthetic software fixtures.
  For32 reference amplitudes1 and generated amplitudes31 zeros plus one32, all
  fields nonnegative, exact empirical relative W1 is1.9375; the frozen function
  reports1.453125. This is a25% underestimate for this fixture, not a heldout result.
- All-nonfinite input to `ens_metrics` produces `Infinity` and `NaN` in JSON text.
- Compared the Torch port with the original NumPy solver at frozen anchor cell240,
  N81, tau2, dt0.02: max u/v discrepancy3.24e-13/1.44e-13. This is a port check at
  one short anchor, not N64/prior-wide tau200 temporal/spatial convergence.

[Exact quick-check receipt](../artifacts/rd-diffusion-review/quick-checks.json).
All remaining statements below are code/contract inspection, not observed
training performance, actual CUDA checks, or empirical/biological validation.

## Publication/result-integrity findings

1. **The metric called W1 is not exact empirical Wasserstein-1.**
   `rd_ddpm.py:165–167` and the marginal implementation use midpoint quantiles with
   NumPy's default linear interpolation. This differs from the empirical-CDF
   integral; the fixture above demonstrates material error. Preserve the frozen
   result as an interpolated-quantile approximation, or preregister an explicit
   mathematical correction/secondary evaluation with a distinct source hash.
   Do not silently replace values after seeing holdouts. A second model training
   run is not needed merely to rename or separately audit a metric.

2. **The failure/output contract can produce a misleading complete result.**
   `evaluate:197` skips conditions with fewer than4 valid solver references;
   aggregation uses only surviving rows and `cmd_run:301` emits `ok:true` anyway.
   PREREG says missing holdouts make a failed run. Complete-case counts and failure
   masks must be checked independently; `ok:true` is not sufficient evidence.
   `jdump:17` permits nonstandard JSON NaN/Infinity. All-nonfinite generator metrics
   explicitly take that path, and marginal metrics/rollouts have further nonfinite
   paths. Preserve raw negatives and identify invalid/missing metrics with explicit
   status/nulls in any publication adapter; never drop them to obtain a green run.
   Infra owns the independent collector audit; this review adds no duplicate code.

3. **Equation/claim linkage is incomplete in the frozen deliverable.**
   PREREG:9 points to `MODEL_CARD.md` for full exact claim refs, but that file is
   absent. The code consumes `(a,b,d,L,tau)` in the advertised order, and its solver
   implements the stated Schnakenberg reaction terms and cosine diffusion. The
   checkpoint stores config SHA; evaluation stores code/config SHA. Thus a later
   adapter can attach these bytes to the existing equation, but the exact equation
   id, claim role/version pins, applicability and checkpoint/output hashes need a
   real model card/index entry before claiming a fully linked trained generator.
   Upstream snapshot claims are not independent local acceptance or fish evidence.

4. **The network's boundary assertion is too strong.**
   PREREG:16 and the Net comment associate replicate padding with zero-flux ends.
   Actual `d1/d2` downsampling convolutions use zero padding. More fundamentally,
   padding is an architectural choice, not a guarantee that generated grid fields
   satisfy the governing PDE. State precisely which layers replicate, retain the
   source solver's cosine/Neumann boundary convention, and keep equation satisfaction
   unknown. No architecture change to an already frozen/running model is proposed.

## Split, normalization, chronology and fair-comparison assessment

- Split identities are disjoint as enumerated. `test_seed` intentionally shares
  train settings but uses seed3; `ensemble` shares settings with `test_param` but
  uses distinct seeds100–131. These evaluation families are not independent new
  parameter samples and their four snapshots per run remain correlated.
- Source inspection supports training-only channel normalization: `cmd_run`
  builds train only, flattens its nonfailed rows, then passes only those rows to
  `train`, where mean/std are computed. Conditioning scales by the declared prior,
  not heldout statistics. I did not execute training to verify runtime normalization.
- Source inspection supports checkpoint-before-heldout generation: `train` writes
  checkpoint.pt; `cmd_run` hashes it; only then `evaluate` and `marginals` call
  heldout solvers. This is program order, not an independently measured runtime
  event. Verify returned code/config/checkpoint hashes and30,000 completed steps.
- Nearest1/5 pooled baselines and the nearest10 deterministic mean use training
  fields at the same requested tau. The shuffled-condition null preserves tau.
  This broadly matches the preregistration. Raw key `nearest10_pooled` actually
  means the deterministic mean-field baseline; its summary is renamed correctly.
  Label it consistently in the UI. Seed-count and method limits remain explicit.
- Conditioning is over four **snapshot times**50/100/150/200, not initial fields.
  It learns a conditional distribution over seed-induced snapshots, not a temporal
  integrator. Prior t range0–200 does not establish accuracy at unseen times.
  DDPM denoising steps are not RD biological/physical time. The short rollout
  statistic is PDE-flow drift magnitude from a sampled field, not a learned temporal
  consistency error or steady-state residual.

## Solver fidelity and recoverability limits

The copied Strang/DCT-II/RK4 algebra agrees at the checked anchor. Current numerical
controls test orthonormality, homogeneous steady state, deterministic CPU replay,
and CPU/CUDA agreement at four settings over10tau. I did not observe their remote
execution. These do not establish grid/time convergence for N64, tau200 over the
whole prior. The >1000/nonfinite run mask inspects saved snapshots, not every
intermediate integration state. Keep that scope visible; do not call generated fields accurate
solutions merely because the diffusion model was trained on solver data.

Training loss rows remain in memory until all30,000 steps finish (`train:149–156`),
and no intermediate checkpoint is saved. The final checkpoint contains EMA weights
and normalization, not a resumable optimizer/current-model/RNG state. Thus the
packet's proposed live step-rate stop rule has no streamed step-rate evidence;
a timeout may recover no weights. `evaluation.json` is written only after all
holdout analysis **and** timing, so a timing failure can leave a valid trained
checkpoint without a durable freeze/evaluation receipt. Preserve that as a partial
failed run, not a completed evaluation. Outer controller telemetry cannot supply
missing training-step information.

Only a display subset of generated/reference fields is saved in examples.npz;
the full160-condition generated ensemble is not retained. Per-condition metrics
can be audited from the exact code/checkpoint/RNG and regenerated solver data,
but not recomputed directly from every originally returned sample. Regeneration
is not guaranteed bitwise without deterministic backend controls. A separately
registered correction must retain its own source/artifacts. `job.sh` also returns
raw checkpoint plus its packed copy inside part2, which inflates outer transport;
verify actual part sizes, all mandatory files and full hashes rather than an
estimated size. No output-cap relaxation is proposed after truncation.

## Expected complete-run identities and counts

For the frozen no-failure design:

- Train:1400 settings ×3 seeds =4200 runs;4 times =16800 rows;30,000 training steps.
- Ensemble:40 settings1450–1489 ×32 seeds100–131 =1280 solver runs;
  160 setting/time conditions. Each condition must have all five method entries:
  `ddpm`, `ddpm_shuffled_condition`, `nearest1_pooled`, `nearest5_pooled`,
  `nearest10_pooled` (the last is actually the mean-field baseline).
- Each summary/paired count must use the declared160 conditions and agree with
  per-condition rows. Any excluded/failed solver runs must be explicitly retained
  and interpreted under the original complete-run failure rule, never hidden.
- test_param:300 settings ×2 seeds =600 runs,2400 rows,600 rows per tau.
- test_seed:300 settings ×1 seed =300 runs,1200 rows,300 rows per tau.
- Timing:1024 DDPM samples/batch,2 warmups,3 timed batches; note the actual code
  warms only64 samples even though the timed batch has1024. Solver same-device
  timing uses1024 runs, CPU timing64; no speedup is implied by mixed workloads.
- Required files:control.json, checkpoint.pt, evaluation.json, examples.npz,
  train_loss.jsonl, setup/model-evaluation parts; matching code/config/checkpoint
  hashes; explicit CUDA device and environment. Missing/truncated/nonfinite output
  is not a completed comparison even if stdout says `ok:true`.

No heldout outcome was used to choose these findings or suggested qualifications.
No shared source/config/preregistration was modified. Infra's collector owner and
the model owner must retain the frozen attempt and any later amendment separately.
