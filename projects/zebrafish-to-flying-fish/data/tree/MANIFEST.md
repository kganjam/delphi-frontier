# Manifest — claude-zf2ff-kcnh-tree-1 (analysis G2b)

| | |
| --- | --- |
| Nebius job | `aijob-e00knz7gwwqck9nksp`, name `claude-zf2ff-kcnh-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `cpu-d3` / `4vcpu-16gb` (CPU only; submitted at `16vcpu-64gb` first and **refused**: tenant non-GPU vCPU quota 24, 36 requested) |
| Image | `debian:12` |
| Timeout / disk | 40m / 20Gi |
| Container start → done | `2026-11-01T15:38:32Z` → `2026-11-01T15:39:49Z` (77 s) |
| Full job log | `job_log_aijob-e00knz7gwwqck9nksp.log` (recovered with `nebius ai job logs --tail 1000`) |

## Inputs

| File | sha256 | Note |
| --- | --- | --- |
| `kcnh_tree_input.faa` | `7ace646d362dd37862787cd3b95fefd3d9aeaa964d5fa254417147bd4697d051` | 20 sequences. The job re-hashed it in-container and reported the **same** digest (`ZF2FF_INPUT_SHA256`), so the bytes that ran are the bytes on disk. |
| `kcnh_tree_input_ledger.json` | — | Per-sequence provenance: UniProt accession + FASTA sha256 for each reference protein, scaffold + predicted-from query + sha256 for each miniprot prediction. |
| `run_tree.sh` | — | Injected job script, reproduced in the log's own echoes. |

Input composition: 10 zebrafish KCNH family proteins, 2 human outgroups (KCNH2, KCNH1),
4 predictions from the **collision** scaffold JAGFBZ010001591.1 (the question), 4 predictions from
JAGFBZ010001790.1 (the **positive control**, called `kcnh6a`-like by the reciprocal test).

## Software, as reported by the job itself

| | |
| --- | --- |
| MAFFT | `v7.505 (2022/Apr/10)`, `--auto --thread 4`, rc 0 |
| IQ-TREE | `multicore version 2.0.7 for Linux 64-bit built Jan 21 2022`, rc 0 |
| Model / replicates / seed | `LG+G4`, `-B 1000` UFBoot, `--alrt 1000`, `--seed 12345` |
| Alignment | sha256 `b7a23dfdf772d79c7e30850babbb9af30195ece5aec95f4eceab7830610793f1` |
| Alignment columns | 1,915 (derived from IQ-TREE's own "566 constant sites = 29.5561%"; the in-container check printed empty because `python3` was absent from the image — a real gap in the script, recorded rather than hidden) |
| Sites | 566 constant, 925 parsimony-informative |
| Gamma shape alpha | 0.6204 |
| Log-likelihood | −27133.2124 (s.e. 480.0026) |

## Outputs, hashed in-container

| File | sha256 | bytes |
| --- | --- | --- |
| `zf2ff_kcnh.treefile` | `06c33bdd11fa53c7c15129f1d48661adccd61d481d284022438758853b2a51b8` | 1116 |
| `zf2ff_kcnh.contree` | `f7b637ea4cd6d351938d21beab28736cc6c05db45362e9724a4a06eb9d45b0fe` | 1037 |
| `zf2ff_kcnh.iqtree` | `199ee84a09500645cf0b614b60d49320dfba5e028116ee7575d285c37af7f5b1` | 10084 |
| `zf2ff_kcnh.log` | `1dd4a8da27319669451a2869a40c8efa62407368e1a40a0d60d693b239018c14` | 6601 |

The treefile and contree were recovered from the job log and are committed here as
`zf2ff_kcnh.treefile` and `zf2ff_kcnh.contree`. `.iqtree` and `.log` were hashed in-container but
**not** printed, so they are not recoverable from the log and are not committed — their digests are
recorded above and the two numbers quoted from them (log-likelihood, site counts) came from the
printed `ZF2FF_MODEL_LINES` block, not from the unrecovered files.

## Result

Analysed by `scripts/analyze_tree.py` → `tree_analysis.json`.

**Positive control: PASS.** The four predictions from JAGFBZ010001790.1 and zebrafish `kcnh6a` form a
clade containing nothing else, support **94.4/97** (SH-aLRT/UFBoot). The reciprocal test's call for
that scaffold is confirmed by an independent method.

**The question: resolved.** The four predictions from the collision scaffold JAGFBZ010001591.1 form a
clade (support **99.8/100**) that is **sister to zebrafish `kcnh2b`** (clade support **99/100**), with
`kcnh2a` falling **outside** that pair (support 99.2/100). So the one `kcnh2`-like region detectable in
`GCA_018398805.1` is **`kcnh2b`-like**, not `kcnh2a`-like.

## Scope and limitations

- A protein gene tree places sequences by substitution likelihood. It is **not** a synteny test, and
  orthology is not established without one.
- The four predictions come from **one** genomic region, so they are not independent sequences; their
  own clade is partly an artefact of that. The question was where the locus sits, which this answers.
- The zebrafish `kcnh2a` entry is 1253 aa and `kcnh2b`'s is 837 aa; the tree does not control for the
  length difference, which can affect alignment and branch length.
- Inputs are miniprot predictions from an unannotated assembly, not sequenced transcripts.
- This **contradicts** the alignment-score ranking of the reciprocal test on the longest prediction and
  **agrees** with its percent-identity ranking and with the forward mapping. The tree is the
  better-designed of the three tests — it has an outgroup and a passing positive control — but it is
  still one test, run once, by one operator, and not independently reviewed.
