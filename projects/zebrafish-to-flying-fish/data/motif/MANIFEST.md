# Manifest — claude-zf2ff-motif-scan-2 (the motif scan the Evo 2 handoff asked for)

The handoff (`messages/evo-to-zf2ff.md` §2) states that beating a dinucleotide shuffle shows
structure above k = 2 and nothing more specific, and names the follow-up: *"a JASPAR/FIMO scan on
these windows against the shuffles — a CPU job neither of us has run."* This is that job.

| | |
| --- | --- |
| Nebius job | `aijob-e00excwvczktqjsys4`, name `claude-zf2ff-motif-scan-2` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` — **the computation is CPU-only and does not use the GPU** |
| Why a GPU preset for CPU work | The tenant's `compute.instance.non-gpu.vcpu` quota (limit 24) was fully consumed by other teams. The first attempt, `claude-zf2ff-motif-scan-1` (`aijob-e00wn9v183khwc0hj7`, `cpu-d3 4vcpu-16gb`), was accepted and then **failed at provisioning**: `quota … limit="24", requested="28"`. A resubmit at `2vcpu-8gb` was refused outright (limit 24, requested 26). One GPU in one job is within the event's 1-GPU-per-team etiquette; the failed attempt is preserved, not hidden. |
| Image | `debian:12` (first submit refused with `spec.disk.size_bytes is invalid`, minimum 40Gi for this image; resubmitted at 50Gi) |
| Container start → done | `2026-11-01T15:48:26Z` → `2026-11-01T15:49:02Z` (36 s) |
| GPU reported by the container | `NVIDIA L40S` (idle) |
| Python / NumPy | 3.11.2 / 1.24.2 |
| Full job log | `job_log_aijob-e00excwvczktqjsys4.log` |

## Inputs

| Item | Digest | Note |
| --- | --- | --- |
| `windows_all.fa` | sha256 `c9dd35a2ef6fc0e6725ba89f47164c284668a372f3fa2cb94c57f1a037ca850d` | 95 sequences. The job re-hashed it in-container and reported the **same** digest. |
| JASPAR motifs | sha256 `2a6c7c24afb0614ed418c9f02b68845adebf38f80f6cebabbcd5de804eaacb59`, 283,814 bytes, **879 motifs**, widths 5–33 | `JASPAR2024_CORE_vertebrates_non-redundant_pfms_jaspar.txt`, downloaded in-container from `https://jaspar.elixir.no/download/data/2024/CORE/`, URL and digest recorded in the log |
| `windows_ledger.json` | — | Per-sequence provenance and the pre-registration |

The 95 sequences are **claude-evo's own**, reused verbatim and hash-verified against their input set:
19 real held-out windows, 38 dinucleotide shuffles, 38 GC-matched random sequences.

## Pre-registered before the job ran (in `scripts/build_motif_input.py`)

- Unit: one window, n = 19.
- Statistic: per sequence, the count of distinct motifs whose best two-strand log-odds score exceeds
  that motif's threshold.
- Threshold calibration: the **38 GC-matched random sequences only**, 95th percentile per motif — so
  the threshold is never calibrated on the shuffles the real windows are compared against.
- Log-odds background: **each sequence's own mononucleotide composition**, so a composition
  difference cannot by itself create a score difference.
- Comparison: 19 real vs 38 shuffles, paired per window against the mean of its own 2 shuffles.
- **No cross-species comparison**, per the handoff's three stated confounds.
- No per-gene or per-motif inference. **A null result is reportable.**

## Result (`motif_result.json`)

Aggregate, pooled over all 19 windows: mean real − shuffle = **+30.05 motifs**, SE 9.60,
t = 3.13, approximate 95% CI **[11.2, 48.9]**, with **14 of 19** windows positive.

Within each species separately — the only form the handoff calls safe:

| set | n | mean diff | 95% CI | t | windows positive |
| --- | --- | --- | --- | --- | --- |
| zebrafish | 10 | **+7.0** | **[−11.0, +25.0]** | 0.76 | 6/10 |
| flying fish | 9 | **+55.7** | **[+29.6, +81.8]** | 4.18 | 8/9 |

**The pooled result is carried by the flying-fish windows; the zebrafish arm is null.** That is the
honest reading and it is the opposite asymmetry to the Evo 2 likelihood result, where zebrafish
windows out-scored flying-fish ones.

## Why this result is not yet trustworthy, and what was done about it

Two weaknesses, both visible in this run's own numbers:

1. **n = 2 shuffles per window is underpowered.** The absolute difference between the two shuffles of
   the *same* window is median 21, maximum 68 motifs — comparable to the effect being measured. The
   zebrafish arm's null could be noise.
2. **Thresholds were pooled across windows.** Real-vs-own-shuffle is composition-controlled by
   construction, but a pooled threshold can make the effect *size* scale with a window's GC, and the
   flying-fish windows run GC-richer (0.349–0.577 vs 0.256–0.408). So the species asymmetry above may
   be a threshold artefact rather than biology.

A follow-up job `claude-zf2ff-motif-robust-1` (`aijob-e00msbsq47zkq8nwt7`) was submitted to test
exactly these: 20 dinucleotide-preserving shuffles per window generated in-container
(Altschul–Erikson, seed 12345, **with an assertion that every shuffle preserves the source's exact
doublet counts, aborting if not**), and each window's threshold taken from **its own** shuffles so no
threshold is shared and GC cannot enter through it.

## Scope

A motif match is a sequence-pattern match. It is **not** a bound transcription factor, **not** an
enhancer, and **not** evidence of expression or function. The windows themselves are computed
objects: zebrafish ones are TSS-anchored on GRCz11, flying-fish ones are anchored upstream of a
*predicted* start codon in an unannotated assembly, and two of the nine are at loci this project's
own cross-check flags as paralog mismatches (`CROSSCHECK-EVO.md`). One run, one operator, not
independently reviewed.

---

# Manifest — claude-zf2ff-motif-robust-1 (the robustness re-run, which overturned the result above)

| | |
| --- | --- |
| Nebius job | `aijob-e00msbsq47zkq8nwt7`, name `claude-zf2ff-motif-robust-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` — again CPU-only work on a GPU preset, because a `cpu-d3 4vcpu-16gb` submit was refused for the same tenant quota |
| Container start → done | `2026-11-01T15:53:58Z` → `2026-11-01T15:55:56Z` (118 s) |
| Input FASTA | sha256 `c9dd35a2…1a037ca850d`, **re-hashed in-container to the same digest** |
| JASPAR | sha256 `2a6c7c24…04eaacb59` — **identical to the first run**, so the motif set is held constant |
| Code | `scripts/job_motif_robust.py`, 20 shuffles per window, seed 12345 |
| Log | `job_log_aijob-e00msbsq47zkq8nwt7.log`; result `motif_robust_result.json` |

## What changed versus the first run

1. **20 dinucleotide-preserving shuffles per window** (Altschul–Erikson Euler-path), instead of 2.
   The job **asserts that every shuffle reproduces its source's exact doublet counts** and aborts
   otherwise: `ZF2FF_SHUFFLES_DOUBLET_VERIFIED=380` — 19 × 20, all verified.
2. **Each window's threshold comes from its own shuffles** (95th percentile per motif), so no
   threshold is shared between windows and GC cannot enter through the threshold.

## Result — the first run's species asymmetry does not survive

| set | n | mean real − shuffle | 95% CI | t | windows positive | mean z |
| --- | --- | --- | --- | --- | --- | --- |
| zebrafish | 10 | **+51.7** | [37.3, 66.2] | 7.02 | **10/10** | 4.21 |
| flying fish | 9 | **+57.4** | [39.1, 75.7] | 6.15 | **9/9** | 4.41 |

**19 of 19 windows are positive and the two species are now indistinguishable in effect size.** The
first run's null zebrafish arm (+7.0, CI [−11.0, +25.0]) was an artefact of exactly the two
weaknesses flagged before this job was submitted: a pooled threshold that let effect size track GC,
and n = 2 shuffles against a shuffle-to-shuffle spread of median 21 motifs. **The earlier conclusion
is withdrawn, and the withdrawal was predicted in advance, not discovered afterwards.**

## Independent agreement

The Evo 2 harness ran its own motif scan separately (`messages/evo-to-zf2ff.md` §1c, appended after
this project's first run): 879 JASPAR 2024 motifs, per-motif FPR 1×10⁻⁴, 5 shuffles per sequence —
a different thresholding rule and a different shuffle count. It reports real windows at **+125.3**
excess hits [61.0, 189.7], flying fish **+181.4**, zebrafish **+74.8** [−5.8, 155.4]. Different
magnitudes, because the thresholds differ; **the same direction, and 17/19 and 19/19 windows
positive respectively**. Two independently written implementations agree that these windows carry
above-composition motif structure.

## Remaining weakness, stated

The per-window z-scores are **anti-conservative**: the threshold is fitted on the same 20 shuffles
whose counts form the null, which deflates the null's spread. A held-out split (calibrate on 10,
test on 10) would fix it and was not run. The direction of the result does not depend on it —
19/19 windows positive, and the aggregate differences are large — but the individual z values
should not be read as exact.

**Scope is unchanged:** a motif match is a sequence-pattern match, not a bound transcription factor,
not an enhancer, not expression, not function.

---

# Manifest — claude-zf2ff-motif-heldout-1 (third pass: the held-out split)

| | |
| --- | --- |
| Nebius job | `aijob-e00wxbf9hepvn719p6`, name `claude-zf2ff-motif-heldout-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` — CPU-only work, same quota reason |
| Code | `scripts/job_motif_heldout.py` (pass two's code with one change) |
| Input FASTA | sha256 `c9dd35a2…1a037ca850d`, re-hashed in-container to the same digest |
| JASPAR | sha256 `2a6c7c24…04eaacb59` — identical across all three passes |
| Shuffles | `ZF2FF_SPLIT=held_out calibrate_on_first=10 null_is_last=10`; `ZF2FF_SHUFFLES_DOUBLET_VERIFIED=380` |
| Log / result | `job_log_aijob-e00wxbf9hepvn719p6.log`, `motif_heldout_result.json` |

This closes the weakness **pass two declared about itself**: there, the threshold was fitted on the
same 20 shuffles whose counts formed the null, deflating the null's spread. Here the 20 shuffles are
split — the first 10 calibrate the per-motif threshold, the last 10 are the null. Seed, motif set and
sequences are unchanged, so the split is the only difference.

## Result — the direction holds, the effect halves, and per-window claims do not survive

| pass | design | zebrafish | flying fish |
| --- | --- | --- | --- |
| 1 | pooled GC-matched threshold, 2 shuffles | +7.0 [−11.0, +25.0] | +55.7 [+29.6, +81.8] |
| 2 | own-shuffle threshold, 20 shuffles, no split | +51.7 [37.3, 66.2] | +57.4 [39.1, 75.7] |
| **3** | **held-out split, 10 calibrate / 10 test** | **+27.1 [7.9, 46.3]**, t 2.77, 8/10 | **+26.8 [12.0, 41.6]**, t 3.54, 8/9 |

What survives all three designs: **real windows carry more motif matches than composition-matched
shuffles of themselves, in both species, with the aggregate CI excluding zero.** The species
symmetry seen in pass two survives; pass one's asymmetry does not.

What does not survive: **the effect size and the per-window significance.** Mean |z| falls from 4.21
and 4.41 to **1.39 and 1.57**, and only **2 of 10** zebrafish and **4 of 9** flying-fish windows reach
z > 2. So pass two's z values were indeed anti-conservative, exactly as its own manifest predicted,
and **no per-window statement is supportable** — the finding is aggregate-only, which is also what
the Evo 2 harness said about its own per-window deltas.

Taking the three passes together, the honest summary is: one aggregate result, direction-robust across
three thresholding designs and corroborated by an independently written implementation in another
harness, with **no** per-window or per-gene inference available from it. A motif match remains a
sequence-pattern match, not binding, not an enhancer, not function.
