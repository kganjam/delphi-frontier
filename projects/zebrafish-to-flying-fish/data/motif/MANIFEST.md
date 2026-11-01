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
