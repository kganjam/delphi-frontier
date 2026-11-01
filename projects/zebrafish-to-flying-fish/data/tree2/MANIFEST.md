# Manifest — claude-zf2ff-kcnh2a-hunt-tree-1

| | |
| --- | --- |
| Nebius job | `aijob-e00k03g7vbmk6smbkh`, name `claude-zf2ff-kcnh2a-hunt-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` — CPU-only work; the tenant's non-GPU vCPU quota was exhausted by other teams |
| Image | `debian:12`, disk 50Gi |
| Done | `2026-11-01T15:55:52Z` |
| Job script | `scripts/job_run_tree2.sh` |
| Log | `job_log_aijob-e00k03g7vbmk6smbkh.log` |

## Inputs

| Item | Digest |
| --- | --- |
| `kcnh2a_hunt_tree_input.faa` (19 sequences) | sha256 `585d9bd569c343f77d43f8e757623c756d370b7f69d525271720812147a28830`, **re-hashed in-container to the same value** |
| provenance per sequence | `kcnh2a_hunt_tree_input_ledger.json` |

Composition: the same 10 zebrafish KCNH proteins and 2 human outgroups as the first tree, the 5
untested `kcnh2a`-aligning regions from `scripts/hunt_kcnh2a.sh`, and **one sequence from each
already-assigned region carried forward as a positive control**.

## Software

MAFFT (rc 0), alignment sha256 `e6e0f878056f1ffff372534e5500468774595636fbb7f658e72da7341f07df3a`;
IQ-TREE 2 (rc 0), `LG+G4`, `-B 1000`, `--alrt 1000`, `--seed 12345`.
`python3` is absent from `debian:12`, so the in-container alignment-column check printed empty again —
the same known gap as the first tree job, recorded not hidden.

## Outputs

| File | sha256 | bytes |
| --- | --- | --- |
| `zf2ff_kcnh2a_hunt.treefile` | `cf70f3993c72498fbb36649cf56867191796d91d3d3b318830755d8c533b905e` | 961 |
| `zf2ff_kcnh2a_hunt.contree` | `3e2b701dcdd490bf4121fc01649771652a3ee06ebaf66b36a790f946292f46f6` | 889 |
| `zf2ff_kcnh2a_hunt.iqtree` | `40983e29d2993f4f6e4fc0763116bc9ee192ffe6e8635b90eb2f1bbe0662f7de` | 8976 |
| `zf2ff_kcnh2a_hunt.log` | `51f104b52da156ea13749d8b41f18b5855c735b0c503847a26cbdb964996d389` | 6592 |

The treefile and contree were printed and are committed; `.iqtree` and `.log` were hashed in-container
but not printed, so they are not recoverable from the log and are not committed.

## Result (`tree2_analysis.json`)

Controls first: both carried-forward sequences reproduce their earlier assignment in this
independent run — `HSPEC_ambiguous_1` with `ZF_kcnh2b` (99.3/100), the `kcnh6a`-like control with
`ZF_kcnh6a` (99.6/100).

All five untested regions fall with a **different** paralog: `kcnh6b` (100/100), `kcnh7` (100/100),
`kcnh7` (63.4/74, weak), `kcnh4a` (99.6/100), `kcnh5a` (99.3/100).

**No `kcnh2a`-like region exists anywhere in this assembly by this method.**

## Scope

A gene tree places sequences by substitution likelihood; orthology needs synteny, not run. The
JAGFBZ010000779.1 assignment carries weak support (63.4/74) and should be treated as unresolved
rather than as `kcnh7`. Absence of a located `kcnh2a` in an explicitly *draft*, scaffold-level,
unannotated assembly is **not** evidence that the species lacks the gene.
