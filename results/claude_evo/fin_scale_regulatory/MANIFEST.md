# Manifest — Evo 2 fin/ray/scale regulatory sequences, zebrafish + flying fish

**Harness:** claude-evo. **Written:** 2026-11-01 15:15 UTC / 08:15 PDT.
**Branch:** `claude/evo2-fin-scale-20261101`.
**Outcome kind:** computed sequence likelihoods and model-generated sequence.
**Not** observation, **not** functional design, **not** an epigenetic claim.

## Jobs — states read from the Nebius CLI, not inferred

| job id | name | state | exit | GPU | runtime |
| --- | --- | --- | --- | --- | --- |
| `aijob-e00cd0nepn7c42q9sm` | `claude-evo-finscale-a1` | COMPLETED | `EVOFS_RC=0` | 1× NVIDIA H100 80GB HBM3, cap 9.0 | 965.5 s |
| `aijob-e00pya60nwmwjd5df7` | `claude-evo-finscale-baseline-a1` | COMPLETED | `EVOBL_RC=0` | 1× NVIDIA H100 80GB HBM3, cap 9.0 | 22.7 s |
| `aijob-e00bvd85xvypgq1j6a` | `claude-evo-finscale-cond-a1` | COMPLETED | `EVOCD_RC=0` | 1× NVIDIA H100 80GB HBM3, cap 9.0 | 29.8 s |

The JASPAR motif scan has **no Nebius job id**: it needs no GPU and was written
as a CPU job, but `compute.instance.non-gpu.vcpu` is saturated tenant-wide
(limit 24; 8, 4 and 2 vCPU presets all refused with `ResourceExhausted`). Other
teams hold that quota and nothing was cancelled to make room. It ran locally
under the mandated `systemd-run` cap; `motif/local_run.log.gz` is its full log
and `experiments/.../run_motif.sh` + `motif_scan_job.py.gz.b64` are the
submittable bundle, ready if CPU frees. Its result is therefore **not** backed by
a Nebius job receipt and is labelled local throughout.

Submitted by me this session. Prior work I did **not** re-run and do **not**
claim: `aijob-e00pwp8khfdwnwm9ps` (run 1), `aijob-e00qkdb12x8zv9yckb`
(bioservices scoring, the brief's leg 1, already COMPLETED before I started),
`aijob-e00pywdm4ta362pwrh` (arm B). Receipts for those are the bioservices
harness's.

## Inputs

`input_set.json` — id `fin-scale-regulatory-2kb/v1`, frozen 2026-11-01T14:09:10Z
by my predecessor, **sha256
`b38f905fe397c8fb14011e5f7cd8b46a832bc4b66773701fb903671dae92882c`**. Both jobs
printed that same hash for the decoded payload inside the container, so what ran
is what was frozen.

19 targets × (1 kb prompt + 1 kb held-out, never shown to the model):
10 *Danio rerio* (GRCz11/danRer11, Ensembl gene start = TSS, includes UTR) and
9 *Hirundichthys speculiger* (**GCA_018398805.1**, the only Exocoetidae
assembly; windows upstream of a **predicted start codon** from a CDS-only
GeneWise model, no TSS/UTR). Genes: `tbx5a fgf10a fgf20a shha msx1b hoxd13a sp7
runx2b lef1 kcnk5b`. `hoxd13a` is zebrafish-only — no flying fish ortholog with
a clean 2 kb ACGT window.

Sources: zebrafish — Ensembl REST coordinates + UCSC danRer11 sequence; flying
fish — figshare `10.6084/m9.figshare.14600634.v1` (CC BY 4.0), file hashes
recorded in `input_set.json`.

## Software and environment, from inside the jobs

`evo2_7b`, bfloat16, seed 0, image `nvcr.io/nvidia/pytorch:25.12-py3`,
Python 3.12.3, torch `2.10.0a0+b4e4ee81d3.nv25.12`, `flash_attn 2.7.4.post1`,
`transformer_engine 2.10.0+769ed778`, pip freeze sha256 `f3487791bb834b0a`
(identical in both jobs). Generation: 1000 bp, temperature 1.0, top_k 4,
2 samples per target, arm A (native-context continuation) only.

## Files and hashes

| file | sha256 |
| --- | --- |
| `armA/candidates.json` | `323dea45560d64af2efc429db0df9e0caa5e47cdb209bf881439704766eb5a25` |
| `armA/controls.json` | `cdbd5f134152e267c2ee88a005674f39baf9a269fff77d2c38a7f6cc098fee2d` |
| `armA/scores.json` | `64ee87825b448cf3866e7cf229f4c8c47fa9cd2f5be95f1578b9eb75bd8041ab` |
| `armA/manifest.json` | `a121aa5ed401e2cd7e8d2c9b5735a6e9550555a78a0ce16ff750229e05ce1af4` |
| `armA/scoring_self_check.json` | `748e86800019e19e297f4bc35dea7ecbe5bbc5ed21c284480eccfa3f109d4f21` |
| `armA/screen.json` | `ffe2d70c2db577c33abc8b409c71dc3094e33610b8028631a625d092e36c2029` |
| `armA/summary.json` | `d4f7274dffe9a0bfeb88ba5314f6b32d3a1587ac966620ce48e77f01df4ff27d` |
| `armA/job_log_aijob-e00cd0nepn7c42q9sm.log.gz` | `83227160a1bc76e8b9890e5001f1ea0cdd7da53d85d5bf2bc44aaf0e2b283993` |
| `baseline/baseline_scores.json` | `71d3a5e0fb7d0e047c7129363f684c5d87f8445e984452dfe5cd5275572497ca` |
| `baseline/positional_logprobs.json.gz` | `abb29f4895b523aace19d1c03e09cf99e6bacb1141154ca993b999dd33923697` |
| `baseline/manifest.json` | `11c337fc75fd0f0572a11e697c70ff7fa22500147be33b393c5b1091d5cbd8ac` |
| `baseline/scoring_self_check.json` | `748e86800019e19e297f4bc35dea7ecbe5bbc5ed21c284480eccfa3f109d4f21` |
| `baseline/job_log_aijob-e00pya60nwmwjd5df7.log.gz` | `23f211cbdfc20e1fd54f780df55f892a5b124e7bb9759d1068d35d31f05d0c43` |
| `baseline/positional_report.json` | see git; derived from `positional_logprobs.json.gz` |
| `conditional/conditional_scores.json` | `e98ea1996ec759af161589da0f349abc6c8992bae72de2b5bf286171f1133855` |
| `conditional/manifest.json` | `e7de6757a7d2b63d8e5adbac44226b86db4d480980d6935c2fe5431eca43f92d` |
| `conditional/scoring_self_check.json` | `47656882def9ff2499e686c441d7159b42a5ff285ab5034cad1d081fda31e168` |
| `conditional/job_log_aijob-e00bvd85xvypgq1j6a.log.gz` | `e859252de33ecd8fff27e5e1ee122e002033aa92e0e3fcc9cdc8105e14f07452` |
| `motif/motif_hits.json` | `06cbb8d8d2919466e24aa6ebd6e9b06cfb6ccfbdd6070007522d05a1e86b56fa` |
| `motif/manifest.json` | `6fd884dad6039939b7ae2a393ddffa46383319845362759d7342504e58a50a97` |
| `motif/local_run.log.gz` | `f04b869cbf7fede042f2a7100da55c5c3e6895f48ec3ffb5b504049d9a1599d9` |

The two `scoring_self_check.json` files are the same file by hash because both
jobs produced bit-identical self-checks.

## Controls — verified, not asserted

**Scoring-path gate, before anything was reported.** A uniform random 1 kb
sequence must score near −ln 4 = −1.3863 or the job refuses to report. Both
jobs: `iid_random` **−1.3996587991714478**, `poly_C` −0.0192153826,
`natural_first_target` −1.2162884474, `scoring_path_sane: true`. These are
bit-identical to each other **and** to the earlier bioservices `score-a2` value
of −1.3997, across three independently submitted jobs.

**Determinism across jobs.** The 19 real held-out windows were scored
independently in both of my jobs: **19/19 bit-identical, max |difference|
exactly 0.0**.

**Hash chain.** 19/19 scored held-out sequences hash to the frozen input set;
the input set is internally self-consistent 19/19 on both the `prompt_sha256`
and `held_out_sha256` fields.

**Control sequences are auditable although they were not exported.** All 38
baseline control sequences reproduce **bit-exactly** on local CPU from seed 0
alone, replaying the job's RNG call order — across Python 3.12.3 (job) and
3.13.12 (local). 19/19 dinucleotide shuffles preserve dinucleotide counts
exactly (Eulerian-walk rejection sampling, verified before return, so a stall
raises rather than silently degrading the control).

**Control ordering is coherent, not merely significant.** Each control strips
one more layer of structure and loses likelihood in the right order:
real −1.2058 > dinucleotide shuffle −1.3502 > GC-matched random −1.3698 >
uniform random −1.3997.

## Results

See `RESULT.md`. One-line version: the real windows beat their own
composition-matched scrambles, at likelihood level (+0.1444 unconditional,
+0.1685 conditional, p≈2–4×10⁻⁶) and independently at motif level (+125.3
JASPAR hits, p=0.00069), with both effects holding in the out-of-corpus species
where memorisation cannot explain them.

**One earlier claim is corrected in §2/§7:** the real-vs-generated gap was
reported as significant from unconditional scoring (p=0.017). Under the fair
conditional test it is **not** significant (+0.0577, p=0.122), because
conditioning helps the generated sequences about twice as much as the real ones.
The species ordering survives; the reliable-gap claim does not.

## Reproduction

```
experiments/claude_evo/fin_scale_regulatory/
  prepare_inputs.py              # builds input_set.json (predecessor)
  run.sh, evo2_fin_scale_job.py           # arm A, as submitted
  run_baseline.sh, evo2_heldout_baseline_job.py  # baseline, as submitted
  run_conditional.sh, evo2_conditional_job.py    # conditional scoring, as submitted
  run_motif.sh, motif_scan_job.py                # JASPAR scan (submittable; ran locally)
  recover_bundle.py              # log -> output bundle
  analyze_outputs.py             # artefact screen (CPU)
  summarize.py                   # group statistics (CPU)
  positional_analysis.py         # per-position advantage by bin (CPU)
  review/argon_design_review.md  # adversarial review and what changed
```

**The `--inject-file` cap is on BASE64, not raw plaintext.** It is 65536 bytes
of encoded payload, so only **~49152 bytes of raw plaintext** across all files.
The inherited bioservices note said 65536 raw and so did an earlier commit of
mine; both were wrong. A 53,124 B set was rejected at exactly 53124×4/3 = 70832,
and every accepted set obeys the 4/3 rule (43,314 / 33,054 / 32,718). The fix is
to inject the job script gzip+base64 too and print its sha256 inside the job:
the conditional job's log shows `fa71252d12f3f6d0…`, matching its repo copy, so
the log proves which code ran.

**Recovery gotcha that nearly cost the baseline data.** `nebius ai job logs`
defaults to the last **100 lines** and silently truncated a 224-chunk payload:
`EVOBL_END` present, `EVOBL_BEGIN` gone, gzip refused the blob. `--tail 1000`
returns the whole log; 1000 is a hard API cap (`limit` above it returns 400).
Any payload needing more than ~1000 log lines is unrecoverable this way and
needs a mounted bucket instead.
