# Result — Evo 2 zebrafish regulatory candidates, run 1

**Kind:** candidate generation on public reference sequence. **Not functional
design.** No enzyme, binder or regulatory-function claim is made, and none will
be without an assay. Evo 2 does not model chromatin accessibility, so **no
epigenetic property is claimed from sequence alone.**

| | |
| --- | --- |
| Nebius job | **`aijob-e00pwp8khfdwnwm9ps`** `delphi-evolve-ops-fevo2zf1-evo2-zebrafish-h100-a1` |
| Provider state | **COMPLETED** |
| Submitted by | `dx-gpuops-r1` (this harness submitted no raw GPU job) |
| Hardware | 1× NVIDIA H100 80GB HBM3, driver 580.173.02 |
| Image | `nvcr.io/nvidia/pytorch:25.12-py3`, torch 2.10.0a0, flash_attn 2.7.4.post1 |
| Code | **this repository's** `experiments/bioservices/zebrafish_evo2_regulatory_candidates/gpu_job.py`, pinned |
| Model | `evo2_7b`, weights 13,766,621,200 bytes, sha256 `c66645929dc1b9c6…ecf4`, **`matches_pinned_lfs_oid: true`** |
| GPU window | 20:36:42–20:44:57 UTC, 493 telemetry samples, mean util 34.8%, max 89%, mean 16.6 GB |

## Outcome in one line

**16 candidate sequences were generated, recovered, and scored.** Run 1
generated them and crashed in scoring on a bug in my own code; run 2
(`aijob-e00qkdb12x8zv9yckb`, COMPLETED) scored them after the fix. Arm B, the few-shot in-context arm, ran
separately as `aijob-e00pywdm4ta362pwrh` and is reported below.

## What was produced

| artifact | n | sha256 verified against the job's `SHA256SUMS.json` |
| --- | --- | --- |
| `candidates.json` | **16** sequences, 1,000 bp each, all distinct | **yes** |
| `controls.json` | **32** (16 dinucleotide shuffles + 16 GC-matched random) | **yes** |
| `control_check.json` | model calibration | **yes** |
| `scores.json` | **57** scored sequences | written by run 2, `aijob-e00qkdb12x8zv9yckb` |

8 design targets × 2 samples, **arm A only** (`A_native_context`). Arm B
(few-shot in-context) was skipped on the internal time budget, so **the
unverified Arc in-context lead was not tested** and nothing is claimed about it.

## The model's own calibration passed, and it is the right control

`control_check.json`, run on the H100 before generation:

| sequence | mean NLL (nats/nt) |
| --- | --- |
| natural | **0.452** |
| mononucleotide shuffle ×2 | 1.394, 1.396 |
| i.i.d. random ×2 | 1.398, 1.395 |
| poly-C homopolymer (artifact doc) | 0.010 |

All three verdicts true: `iid_ge_ln4_minus_0.05`, `natural_below_shuffles_and_iid`,
`iid_sequences_use_all_four_bases`.

The first of those is the one that matters. An i.i.d. uniform sequence must score
at the entropy of a four-letter alphabet, **ln 4 = 1.3863** nats/nt; the two
random controls came in at 1.398 and 1.395. That is the random control gpuops
reported as broken in their earlier attempt, now landing where theory says it
must. The poly-C line is there to document the degenerate case: a model assigns
near-zero NLL to a trivial repeat, so low NLL alone is never evidence of quality.

## Independent assessment of the candidates — CPU, no model in the loop

Evo 2 scoring its own generations would not be independent: they are
high-likelihood by construction. So the candidates were placed on a PWM-based
scale whose endpoints were fixed **before any candidate existed**.

| group | n | GC | CpG o/e | mean z | 95% CI |
| --- | --- | --- | --- | --- | --- |
| **Evo 2 candidates** | 16 | 0.412 | **0.548** | **+0.69** | **[+0.06, +1.32]** |
| real held-out promoters | 8 | 0.352 | 0.497 | +1.23 | [+0.27, +2.19] |
| control: dinucleotide shuffle | 16 | 0.412 | 0.549 | −0.24 | [−0.82, +0.34] |
| control: GC-matched random | 16 | 0.415 | 0.987 | +0.41 | [−0.11, +0.93] |

What this supports:

- **The candidates reproduce vertebrate CpG depletion**: CpG o/e **0.548**, near
  the real promoters' 0.497 and far from GC-random's 0.987. That is a real,
  non-trivial property of vertebrate non-coding sequence, and the model was not
  asked for it.
- **They carry motif content above their own dinucleotide composition**:
  z = +0.69, interval excluding zero.

What it does **not** support, stated because the numbers invite the opposite reading:

- **Candidates are not distinguishable from real promoters here.** The two
  intervals overlap heavily; with n=16 and n=8 this diagnostic cannot separate
  them, and "indistinguishable from real" is not a claim that they are equivalent.
- **The GC-random control is not cleanly at zero** (+0.41, upper bound +0.93), so
  the scale's separation is weaker on this set than on the baseline. Any reading
  of the +0.69 should be discounted accordingly.
- **The candidates are GC-richer than the real held-out halves** (0.412 vs
  0.352), which is a difference from their target distribution, not a match to it.
- **None of this is function.** A motif is not a binding event; a binding event
  is not expression.

## The bug, which is mine

```
gpu_job.py line 163, in score
    return float(lp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1).mean())
RuntimeError: Index tensor must have the same number of dimensions as input tensor
```

Evo 2 returns `outputs, _` where the logits are `outputs[0]`. I treated
`outputs` as the logits, so `[:-1]` sliced the **batch** axis of a `(1, L, V)`
tensor to length 0 instead of dropping the final position, and the gather had
nothing to index. Fixed: the unwrapping is explicit and the shape is asserted,
because each GPU run is one shot. Arm B's budget break now exits both loops
rather than re-testing per target.

**A reporting hazard worth propagating:** the job's own `entry.json` records the
zebrafish stage as `"status": "ok"` while the same record carries `"rc": 1` and a
`readback_error` for the missing `scores.json`. The status is wrong and the
return code is right. A reader taking the status at face value would conclude the
stage succeeded.

`entry.json` also fails its own manifest hash (2,365 bytes actual against 2,341
recorded) — consistent with it being finalised after the manifest was written.
The two scientific payloads, `candidates.json` and `controls.json`, both verify
exactly.

## Run 2 — scoring completed

The missing artifact now exists. `aijob-e00r0910b83jyk88ak` **FAILED** before any
GPU compute (`bash: set: No such file or directory` — repeated `--args`
collapsed, `-c` was dropped, bash tried to execute the script text as a
filename). Resubmitted with the command in an injected `run_score.sh`:

| | |
| --- | --- |
| Job | **`aijob-e00qkdb12x8zv9yckb`** `bioservices-evo2zf-score-a2` |
| State | **COMPLETED**, `SCOREJOB_RC=0` |
| Submitted by | **this harness**, after posting the coordination note to gpuops |
| Compute | model load 14.3 s, scoring 21.8 s total, 57 sequences |

**The self-check passed before any score was reported.** A uniform random
sequence scored **−1.3997**, against the **−ln 4 = −1.3863** that a four-letter
uniform alphabet requires; a poly-C repeat scored −0.019, documenting that a
near-zero NLL proves nothing. The job was built to refuse to report scores if
that check failed, because scoring is the stage that crashed in run 1.

| group | n | mean log-prob/base | 95% CI |
| --- | --- | --- | --- |
| real held-out promoters | 9 | **−1.2031** | [−1.3136, −1.0925] |
| **Evo 2 candidates (arm A)** | 16 | **−1.2255** | [−1.2832, −1.1677] |
| control: dinucleotide shuffle | 16 | −1.3565 | [−1.3712, −1.3417] |
| control: GC-matched random | 16 | −1.3780 | [−1.3923, −1.3637] |
| *i.i.d. uniform floor* | — | *−1.3863 theory, −1.3997 measured* | |

What this supports: the candidates are **indistinguishable from real zebrafish
promoter-proximal sequence under the model's own likelihood** (CIs overlap
heavily), and both sit clearly above the composition controls, which cluster at
the random floor.

What it does **not** support, and this is the important part:

- **The candidates were scored by the model that generated them.** High
  likelihood is expected by construction and is **not** independent evidence of
  quality. The real held-out halves are the only unbiased row in that table,
  because the model did not produce them.
- **Everything sits within ~0.2 nats of the i.i.d. floor.** Evo 2 finds real
  zebrafish promoter-proximal sequence only modestly more predictable than
  random, so the dynamic range of this measure on this material is small.
- The independent motif diagnostic reached the same overlapping conclusion by a
  route with no model in it, which is the stronger of the two tests.
- **None of it is function.**

## Arm B — few-shot in-context

`aijob-e00pywdm4ta362pwrh`, **COMPLETED**, `SCOREJOB_RC=0`, 422.6 s. 16
candidates, 8 targets × 2 samples, 1,000 bp, all distinct. **Zero are identical
to any real held-out half**, so none is a copy of a prompt or of the comparator.

| group | n | mean log-prob/base | 95% CI |
| --- | --- | --- | --- |
| real held-out | 9 | −1.2031 | [−1.3136, −1.0925] |
| arm A native-context | 16 | −1.2255 | [−1.2832, −1.1677] |
| **arm B few-shot in-context** | 16 | **−1.2681** | [−1.3347, −1.2015] |
| dinucleotide shuffle | 32 | −1.3501 | [−1.3616, −1.3385] |
| GC-matched random | 16 | −1.3780 | [−1.3923, −1.3637] |

**arm B − arm A = −0.0426, 95% CI [−0.1308, +0.0455].** The interval spans zero:
at 16 per arm there is **no detectable difference** between native-context and
few-shot in-context prompting on this measure.

Independent motif diagnostic, same scale, no model in the loop:

| group | n | GC | CpG o/e | mean z | 95% CI |
| --- | --- | --- | --- | --- | --- |
| real held-out | 8 | 0.352 | 0.497 | +1.23 | [+0.27, +2.19] |
| arm A | 16 | 0.412 | 0.548 | +0.69 | [+0.06, +1.32] |
| **arm B** | 16 | 0.379 | 0.546 | **+0.60** | [+0.17, +1.03] |
| dinucleotide shuffle | 16 | 0.412 | 0.549 | −0.24 | [−0.82, +0.34] |
| GC-matched random | 16 | 0.415 | 0.987 | +0.41 | [−0.11, +0.93] |

Both arms agree and both overlap the real promoters.

### What arm B did NOT test

The 29 October Arc blog post claims **functional** regulatory sequences at
30–50% yield, with wet validation in mice. This arm tested whether few-shot
prompting changes **sequence likelihood and motif composition**. It did not test
function, yield, or any of their claims, and **a null here is not evidence
against them**. The lead remains unverified.

## What a further re-run would add

The fixed `score()` plus a budget large enough for arm B would give Evo 2
log-likelihoods for candidates, controls and real held-out halves, and would test
the in-context arm. Bundle for that re-run:
`evo2_zebrafish_job.py` sha256 `46a5767482a76adcdbcf0f692f9719beed3477a257022a976d40bafb0e64fc24`.

## Limitations

- One arm, 16 candidates, one model, one checkpoint, nine genes.
- No accessibility oracle exists for zebrafish, so no epigenetic claim is possible.
- Composition plausibility is not function and is not evidence of it.
- The held-out comparison is 8 sequences; intervals are wide and reported wide.
