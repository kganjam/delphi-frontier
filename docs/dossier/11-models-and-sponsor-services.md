# 11. Models and sponsor services actually used

Compiled 2026-11-01, ~10:50am PST (Seattle). Every row carries a receipt: a file path, a job
id, or the command that produced the number. Where a claim could not be verified, this file
says **no receipt found** rather than estimating. Access to a service is not use of a service.

Base of the repo reads: worktree `/data/worktrees/delphi-frontier/dossier` at `origin/main`
`7e45e98e`.

---

## 1. Nebius — serverless GPU/CPU job harness

**141 distinct jobs** under our own name prefixes.

How the number was obtained, and its limit: `nebius --profile hackathon ai job list` returns
**one page of 100** and the CLI exposes **no page-token flag** (`nebius ai job list --help`
lists only `--parent-id`; passing `page_token:` through `-f req.yaml` is ignored and returns
the same first page). The live page covers `2026-11-01T02:08:12Z` → `2026-11-01T18:27:44Z`.
To reach the older jobs the live page was unioned by job id with the repo's own snapshot
`results/resources/hackathon-usage.json` → `own_jobs` (48 rows, observed
`2026-11-01T07:39:28Z`). Union = **141 unique job ids** (100 live-only + 41 snapshot-only).
This is a **lower bound**: any job that is neither in the newest 100 nor in that snapshot is
not counted.

Name prefixes in the union: `claude-` 91, `delphi-` 46, `bioservices-` 3, `kiln-` 1.

### Terminal state, all 141

| state | count |
|---|---|
| COMPLETED | 110 |
| FAILED | 13 |
| CANCELLED | 11 |
| RUNNING | 5 |
| IMAGE_PULLING | 1 |
| ERROR | 1 |

Platform: `gpu-h100-sxm` 94, `gpu-l40s-a` 33, `cpu-d3` 14.

### Grouped by what the job ran

Grouping is by job name regex over the union (names are the only engine signal the job API
returns; the `spec.args` of the live page corroborate them — e.g. `pzoner.py`, `md_job.py`,
`evo2_tiling_job.py`, `mc_runner.cpp`).

| group | jobs | COMPLETED | FAILED | CANCELLED | RUNNING | other | platforms |
|---|---|---|---|---|---|---|---|
| Tissue pattern solver (`pzone*`, `edge2d*`, `fan*`, `uniform2d*`, `phasemap`) | 22 | 19 | 0 | 2 | 0 | 1 pulling | h100 22 |
| Phylogenetics (MSA / tree builds, `*-tree*`, `zf2ff-*`) | 16 | 15 | 0 | 0 | 0 | 1 | l40s 14, cpu 2 |
| COPS / infra harness, probes, frozen-assay controls | 15 | 12 | 1 | 2 | 0 | 0 | h100 12, cpu 3 |
| **Evo2 7B** genome language model (`evo2*`, `evo-finscale*`) | 14 | 13 | 1 | 0 | 0 | 0 | h100 12, cpu 2 |
| Neuro / MCell + atlas sims (`neuro-j*`, `p1-logprobe`) | 12 | 11 | 0 | 1 | 0 | 0 | h100 8, cpu 4 |
| CFD / flow (NS2D shear, PDE bench, wind tunnel, AoA) | 12 | 9 | 2 | 1 | 0 | 0 | h100 10, l40s 1, cpu 1 |
| Voxelyze / voxcraft GPU soft-body (`voxgpu-*`) | 11 | 5 | 1 | 3 | 2 | 0 | h100 7, l40s 4 |
| **OpenMM** MD (collagen `md*`, `mol-shhn-md40*`) | 11 | 6 | 3 | 0 | 2 | 0 | h100 11 |
| Organ morphogenesis sweep (`organ-r*`) | 8 | 6 | 2 | 0 | 0 | 0 | l40s 8 |
| Reaction-diffusion inverse design (`rd*`) | 7 | 5 | 2 | 0 | 0 | 0 | h100 7 |
| Xenobot replay (Voxelyze) (`xeno*`) | 6 | 5 | 0 | 0 | 1 | 0 | l40s 6 |
| Neural cellular automata (`nca*`) | 4 | 3 | 0 | 1 | 0 | 0 | h100 4 |
| **Morpheus** CPM tissue | 2 | 1 | 1 | 0 | 0 | 0 | cpu 2 |
| MACE ML interatomic potential (`kiln-mace-h100-s0`) | 1 | 0 | 1 | 0 | 0 | 0 | h100 1 |

Receipt: `/tmp` analysis over the union file; the two inputs are the live CLI call above and
`results/resources/hackathon-usage.json`. Named per-job manifests for several of these groups
are in the repo, e.g. `results/compute/evo2zf/manifest-fevo2zf1.json` (Evo2 zebrafish),
`results/infra/md-v3/manifest-infra21.json` (OpenMM 900 ps),
`results/infra/morpheus-v2/manifest-infra17.json`, `results/infra/nca-seed/manifest-infra28.json`.

All Nebius jobs ran the pinned NGC image
`nvcr.io/nvidia/pytorch@sha256:11e9976339d08669ede155cdbc601b1df5f57772fcee772b23527efc54e05602`
(`results/resources/voxcraft-image-diagnostic.json`, `inputs/items_infra_*.json`).

---

## 2. Nebius Scientific AI MCP — 69 tools exposed, 1 invoked

Endpoint `https://forge.nebius.cloud/mcp`, authenticated. The tool catalog was enumerated and
is recorded verbatim: **69 tools** in
`results/resources/scientific-ai-capabilities-20261101.json` (`len(d['tools']) == 69`,
observed `2026-11-01T05:43:04Z`).

| tool | model | what we ran | count | receipt |
|---|---|---|---|---|
| `infer_openfold2_native` | **OpenFold2** | Zebrafish protein structure prediction from exact NCBI/UniProt sequences | **5 successful operations** | `artifacts/bio-services/kcnj13_openfold2/operation_receipt.json` (Kcnj13, op `op-5ba1d104dbbcd293`, `final_status: SUCCEEDED`, mean pLDDT 52.86, 362 aa, inference 15.54 s) + 4 rows in `/data/artifacts/delphi-evolve-rethink/claude-bioservices-20261101/call_ledger.jsonl` (`fgf10a:Q8AY90`, `hoxd13a:Q90472`, `shha:Q92008`, `kcnk5b:Q6PFU3`, all `operation_status: SUCCEEDED`) |

The OpenFold2 receipt states `runtime_origin: upstream-source-not-nim` — this was the
upstream OpenFold2, **not** an NVIDIA NIM.

**68 of the 69 tools were available and not invoked.** They include `submit_alphafold3`,
`submit_boltzgen`, `submit_esm2_650m`, `submit_esm2_3b`, `submit_stab_ddg`,
`submit_rfdiffusion`, `infer_proteinmpnn_native`, `molmim_run_native`, `boltz2_predict_native`,
`submit_gromacs_workflow`, `submit_openmm_workflow`, `submit_amber_workflow`,
`submit_namd_workflow`, `submit_lammps_workflow`, `msa_search_native`, `infer_diffdock_native`,
`submit_scvi_scanvi`, the Isaac session tools and the speech models. Evidence of non-use:
`grep -rl` for each tool name across `*.json`/`*.jsonl` returns only the two catalog files
(`results/resources/scientific-model-catalog-summary.json`,
`artifacts/bio-services/live_capability_subset.json`), never an operation receipt; and the
capability snapshot itself records `model_inference_calls: 0` at the time it was taken.

**ESM2 was run, but locally, not through this MCP.** `facebook/esm2_t33_650M_UR50D` scored 256
rows on 8 local CPUs in 118.2 s — `results/bioservices/kir21_pilot_receipt.json`,
`results/bioservices/kir21_analysis.json`. Provider field reads "local CPU execution; no hosted
inference provider".

---

## 3. Bio-service HTTP APIs — the harvest ledger

Ledger: `/data/artifacts/delphi-evolve-rethink/claude-bioservices-20261101/call_ledger.jsonl`
— **110 rows**, of which **98 are HTTP calls** (rows carrying `request_url`). A call counts as
ok when `200 <= http_status < 300` and `error is null`.

| service | calls | ok | failed | example endpoint |
|---|---|---|---|---|
| BioModels (EMBL-EBI) | 36 | 28 | 8 | `www.ebi.ac.uk/biomodels/BIOMD0000000201`; the 8 failures are HTTP 400 on `/biomodels/search` from a bad `curationstatus` filter |
| Ensembl REST | 23 | 22 | 1 | `rest.ensembl.org/homology/symbol/danio_rerio/fgf10a`; the failure is HTTP 400 on `lookup/symbol/danio_rerio/msxb` |
| UniProt | 17 | 17 | 0 | `rest.uniprot.org/uniprotkb/Q0KIZ7.json` |
| Europe PMC | 11 | 11 | 0 | `www.ebi.ac.uk/europepmc/webservices/rest/search` |
| NCBI E-utilities | 4 | 4 | 0 | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` |
| NCBI Datasets | 3 | 3 | 0 | `api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/Beloniformes/dataset_report` |
| ZFIN | 1 | 1 | 0 | `zfin.org/downloads` |
| Google Gemini (same ledger) | 2 | 2 | 0 | `generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent` |
| Nebius MCP probe | 1 | 1 | 0 | `[REDACTED]/mcp` initialize |
| **Total HTTP** | **98** | **89** | **9** | |

The seven named bio-data services alone: **95 calls, 86 ok, 9 failed.**

The remaining 12 ledger rows are not HTTP calls and carry no `request_url`:
4 `nebius-openfold2` operations (SUCCEEDED, counted in §2), 5 `biomodels-sim-cpu` local
libRoadRunner runs, 2 `gcp` gcloud checks (exit 0), 1 `nvidia-brev` CLI check (exit 1).

---

## 4. Local and simulator engines

"Recorded run" below means a result artifact exists in the repo. It does **not** mean the
result was scientifically checked.

| engine | version | pinned at | recorded run? |
|---|---|---|---|
| libRoadRunner | 2.10.0 | `pyproject.toml:16` (`libroadrunner==2.10.0`), `connectors/biomodels/frontier_mapping.py:31` | **Yes** — `artifacts/molecular/cross-scale-gate.json:115` `"engine": "libroadrunner 2.10.0 (CVODE)"`; plus 5 `biomodels-sim-cpu` rows in the harvest ledger |
| BETSE | 1.5.0 ("Nicest Nestor") | `artifacts/bioelectric-tissue/summary.json:3` | **Yes** — 5 scenarios, 5 trajectory files, 5 configs, `bioelectric_tissue.mp4`; sensitivity run in `sensitivity-v1/` |
| Morpheus | 2.3.9 (binary `3d9a6e5a…`) | `docs/epithelial-repair-card.md:8`, `artifacts/multicell/packet/run_packet.sh:8` | **Yes** — two sets: `artifacts/multicell/{baseline,nofeedback,seed2,full}` (3 arms with `logger.csv` + MP4) and `artifacts/epithelial/results.json`, `results-r2.json` |
| OpenMM | 8.4 | `artifacts/molecular/cuda-v3/production/receipt.json:6` | **Yes** — ≥3 production CUDA runs (`trajectory-1173{1,2,3}.npz`), plus the Nebius H100 collagen runs: 3 × 100 ps (`results/infra/md-v2/manifest-infra15.json`) and 3 × 900 ps (`results/infra/md-v3/manifest-infra21.json`) |
| Voxelyze | pin `4287e365e11416dd108f2f361e9ec4c5a011a16c`, lib string `voxelyze.0.9.92` | `docs/simulation-roadmap.md:241`, `artifacts/simulator-catalog/catalog.json` | **Yes** — `artifacts/voxel-actuation/` (protocol, candidates, controls, trajectory, summary); xenobot replay receipt `artifacts/audits/xenobot/replay-receipt.json`, build exit 0 in 12.6 s, 7 replay cases |
| WaterLily.jl | 1.10.0 | `artifacts/cfd3d/gpu-v1/logs/env.log:213` (`[ed894a53] + WaterLily v1.10.0`), `resolved-Manifest.toml` | **Yes** — 2 CPU cases + 4 GPU cases (`gpu_fish_L64_Re200` … `L192_Re1000`) with `receipt.json`, `telemetry.csv` |
| Zebrafish-GEM | commit `846f0b7b34701801b2f5e15f549807d2e71ffa62` (no semantic version) | `artifacts/metabolism/manifest.json` (`stored_in_repo: false`) | **Yes** — `metabolism_results.json`, `flux_table_baseline_o2_20.csv`, `basic-nutrients-v2/`, `-v3/` (pFBA, `o2_sweep.mp4`); run with cobra 0.32.1 on glpk |
| **PhysiCell** | 1.14.2 | `artifacts/simulator-catalog/catalog.json`, `docs/simulation-roadmap.md:81` | **No — source-only.** Catalog status `source-only`; roadmap says "do not install alongside working Morpheus" |
| **voxcraft-sim** | pin `dd8668f99ff74fb2fc2ee60deb91287a3b519d8f` | `artifacts/simulator-catalog/catalog.json`, `docs/simulation-roadmap.md:474` | **No — blocked.** Catalog status `blocked`. Only a frozen H100 probe packet exists (`artifacts/voxcraft-gpu-probe/probe.json`, `no_claim_yet`); no result or receipt file. The one `voxcraft` Nebius job FAILED |

Also in the catalog and **source-only, never run**: `voxcraft-viz`, `reconfigurable-organisms`,
CompuCell3D 4.10.0, `sofa-softrobots`, `sofa-softrobots-inverse`, `cpm-ddpm-surrogate`, and
IKA-FLOW (OpenFOAM fish-undulation cases, `docs/simulation-roadmap.md:83`).

---

## 5. Google — Gemini models and Google Cloud

### Gemini models with receipts

| model id | what we ran | count | receipt |
|---|---|---|---|
| `gemini-embedding-001` | Discovery index embedding | **2,444 documents, 49 requests, 0 failed**, 768 dims, 2 truncated inputs, run id `95caa34e4a03491a82a81ffe48049063`, window `2026-10-31T20:20:14Z`–`20:20:59Z` | `imports/2026-10-31-discovery-live-index-receipt.json`; mirrored in `results/resources/hackathon-usage.json` → `model_usage.gemini_embedding_index` |
| `gemini-3.8-flash` | Capability-agency pilot (v2) | **27 calls, all HTTP 200**; 38,934 prompt + 364 candidate + 10,328 thought = 49,626 tokens. One `thinkingLevel=minimal` smoke test rejected HTTP 400 | `results/capability-agency/runs/capability-agency-pilot-20261031-v2/post_run_summary.json`, `results/capability-agency/gemini_model_probe.json` |
| `gemini-3-pro-image-preview` | Bioservices protocol critique + data-access audit | **2 calls**, 3,778 in / 3,984 out incl. thinking | `results/bioservices/gemini_usage_ledger.json` |
| `gemini-3.1-pro-preview` | Same two audit prompts, second model | **2 calls**, 3,778 in / 5,716 out incl. thinking | same ledger; outputs in `results/bioservices/gemini_audit_text_model/` |
| `gemini-3-flash-preview` | Formalize extraction run `oca2-gemini-1` | 1 run, status **refused** (`CAUSAL_GENOTYPE_PHENOTYPE_NO_MECHANISM`) | `engineering/formalize/runs/oca2-gemini-1/receipt.json` |

The bioservices audit ledger totals **4 calls, 7,556 input tokens, 9,700 output tokens
including thinking** (`results/bioservices/gemini_usage_ledger.json`). The two smaller
per-model ledgers are subsets of it, not extra calls.

**`gemini-4-argon`: no receipt found.** It appears in `docs/dossier/ASKS.md` row 6 (status
"partial": identified on the Gemini API and wired into harness briefs, the Argon pass listed as
outstanding), in `docs/dossier/09` and `10`, and as an assessor IRI
`https://w3id.org/probknow/resource/model/gemini-4-argon` in the morpholib bundles. There is no
request, token or ledger entry for it anywhere in `results/`, `engineering/`, `imports/` or
`artifacts/`. **Do not list it on the slide as a model we ran.**

### Google Cloud

Project `scienceclaw26bos-3016` (184 matches across the repo).
From `results/resources/hackathon-usage.json` → `google_compute`, observed
`2026-11-01T02:09:32Z`:

| fact | value | receipt |
|---|---|---|
| global CPU quota | **32 vCPU** | `google_compute.global_cpu_limit` |
| GPU quota | **granted = 1** (not zero) | `google_compute.gpu_quota_granted`; `results/resources/gcp/gpu-quota-approved.json` (`GPUS-ALL-REGIONS-per-project` approved to 1, created `2026-11-01T00:06:35Z`) |
| GPU VM created | **true**, NVIDIA **L4**, `g2-standard-8`, `us-central1-c`, id `4266786588371661074` | `google_compute.l4_admission`, `artifacts/gcp/cfd-r2-l4-overnight/hardware-capacity-attempt.json`, `results/resources/gcp/cfd-r2-l4-verified.json` |
| L4 environment gate | **passed**, 735.4 s after start, `actual_device: NVIDIA L4` | `google_compute.l4_environment_gate` |
| L4 science pass | **`actual_cuda_science_pass: null`** — admission and environment only; no R2 case started | same |
| instances | 5 recorded; 16 active vCPU at the snapshot, 0 active GPU | `google_compute.instances`, `active_allocated_vcpus`, `active_allocated_gpus` |
| workloads run on GCP CPU | BETSE k-sensitivity, aeroelastic fidelity, ecology (28 pairs complete), genomics, controlled CFD argv repair | `results/resources/gcp/{betse-instance,betse-completion,aeroelastic-completion,ecology-missing-completion,genomics-completion}.json`; `artifacts/gcp/{aeroelastic,betse-k-sensitivity,cfd,cfd-argv-repair,cfd-r2-l4,ecology,ecology-missing,lat4a,lat4a-r2}` |
| failures | 2 captured | `results/resources/gcp/cfd-bootstrap-failure.json` and sibling; L4 attempt followed "terminal g2-standard-4 capacity stockouts in central1-c and east4-a/c" |

Network `frontier-workers-20261031`, priority-0 deny-all ingress, bucket-only metadata
identity, no embedded keys. **Cost: `null` — billing meters were never queried.**

---

## 6. NVIDIA

| item | status | receipt |
|---|---|---|
| CUDA / NGC container stack | **Used.** Every Nebius job ran the pinned NGC PyTorch image `nvcr.io/nvidia/pytorch@sha256:11e9976…e05602`; `nvcr.io/nvidia/pytorch:25.12-py3` is the tag form in `PROTOCOL3.md`, `PROTOCOL7.md` and `frontier_compute/vendor/compute_ops/batch.py` | `results/resources/voxcraft-image-diagnostic.json`, 12 × `inputs/items_infra_*.json`, `results/infra/voxcraft-probe/.../receipt.json` |
| H100 / L40S / L4 hardware | **Used.** Nebius: 94 H100 jobs, 33 L40S jobs. GCP: 1 L4 VM, environment gate passed | §1 and §5 |
| CUDA run receipts | `artifacts/cfd3d/gpu-v1/nvidia-smi.txt`, `receipt.json`; `artifacts/molecular/cuda-v3/production/` | — |
| **BioNeMo / NIM** | **Not established. 0 model inference calls.** `bionemo_nim_execution_established: false`, `model_inference_calls: 0`. Credential checks: `nvidia_env_exists` false, `ngc_config_exists` false, `ngc_cli_available` false. The one OpenFold2 receipt explicitly reports `upstream-source-not-nim`; the Boltz-2 contract on the MCP is "portable protein-only with supplied A3M, explicitly not full NVIDIA NIM" | `results/resources/bionemo-capability-boundary.json` (observed `2026-11-01T05:44:33Z`); `artifacts/demo-video-90/sources/provenance/bio-model-usage.json` → `bionemo_nim` |
| **Brev** | **Logged in, and one instance exists** — correcting the brief. `~/.local/bin/brev ls` returns `You have 1 instances in Org kganjam-c5d0a6-7kae` / `df-boltz2-kcnj13  RUNNING  BUILD COMPLETED  SHELL READY  uf28ow3oi  massedcompute_L40S  L40S`. `~/.brev/credentials.json` exists, mode 600, with `access_token` and `refresh_token`. **But no Boltz-2 inference result is receipted anywhere in the repo**, so the honest statement is: an L40S Brev instance named `df-boltz2-kcnj13` was provisioned and is ready; no Boltz-2 run output has been recorded | `brev ls` (run 2026-11-01 ~10:45am PST); `ls -la ~/.brev` |

An earlier automated check recorded Brev as unavailable — `call_ledger.jsonl` row
`{"exit": 1, "label": "brev-cli", "service": "nvidia-brev", "stdout": "0", "t_utc":
"2026-11-01T13:16:04Z"}`. That row reports **0 instances at that moment**, and the instance was
created afterwards. Both observations stand; the later one is current.

---

## 7. MiniMax

| model | what we ran | count | receipt |
|---|---|---|---|
| `speech-2.8-turbo` (TTS) | Final demo-video voice pass, cuts `frontier-120s` and `frontier-60s` | **7 provider calls, 892 reported characters** | `artifacts/demo-video/tts-manifest.json`; entry `minimax-demo-video-final-voice-pass` in `artifacts/demo-video-90/sources/provenance/bio-model-usage.json` |

---

## 8. Formlabs — nothing was printed

366 `.stl` files exist in the repo and five glider print manifests were generated
(`artifacts/glider/r1-light`, `r1-strong`, `r2-light`, `r3-daane`, `r4-daane-printfix`), plus
four print bundles (`artifacts/print`, `print-v2`, `print-v3`, `print-v4`).

Every part in every glider manifest carries **`"printed": false`** — 93 occurrences across the
five manifests, **0 occurrences of `"printed": true` anywhere**. The printer field is
`"printer": {"assumed": "Form Studio 1", …}` — an *assumed* model used for geometry
constraints, not a printer that was driven. The resin is a named pin
(`alpha-grey-v1-default-post-cure`) used as a material-property row, not a cartridge that was
consumed.

**No Formlabs printer was used and no physical part was produced.** The correct slide line is
"print-ready STLs and manifests generated; nothing printed."

---

## Available but not used

| sponsor / service | available | used |
|---|---|---|
| Nebius Scientific AI MCP | 69 tools | 1 (`infer_openfold2_native`) — **68 unused**, including AlphaFold3, BoltzGen, ESM2 650M/3B, stab_ddg, RFdiffusion, ProteinMPNN, MolMIM, Boltz-2, GROMACS, AMBER, NAMD, LAMMPS, DiffDock, scVI/scANVI, MSA search, Isaac, speech models |
| NVIDIA BioNeMo / NIM | reachable via `forge.nebius.cloud/mcp` | **0 inference calls**; no NGC credentials on the host |
| NVIDIA Brev | logged in, 1 L40S instance READY | instance provisioned; **no run output receipted** |
| Simulator catalog | 16 engines | 7 with recorded runs; PhysiCell, voxcraft-sim, voxcraft-viz, reconfigurable-organisms, CompuCell3D, SOFA (×2), cpm-ddpm-surrogate, IKA-FLOW are **source-only or blocked** |
| Google Cloud GPU | L4 quota granted (1), VM created, environment gate passed | **no R2 scientific case ran on it** (`actual_cuda_science_pass: null`) |

## What we did NOT do

- **Nothing was physically printed.** No Formlabs printer was driven; `printed: false` on every
  part; the printer name in the manifests is an assumption, not a device.
- **No BioNeMo or NIM execution.** Zero model inference calls; no NGC config, no NGC CLI, no
  NVIDIA env credentials on the host.
- **No Boltz-2, AlphaFold3, ProteinMPNN, MolMIM, stab_ddg or GROMACS run.** These were in the
  MCP catalog and were never invoked. A Brev L40S instance named for Boltz-2 exists but has no
  recorded output.
- **No `gemini-4-argon` call is receipted.** It was identified and wired into briefs; the
  design-review pass is outstanding.
- **No GPU science case completed on Google Cloud.** Quota, VM and environment gate only.
- **Billing was never read.** `cost: null`; `actual_billing: "unknown; billing meters were not
  queried"` (`artifacts/demo-video-90/sources/provenance/bio-model-usage.json` → `accounting`).
- **Total provider LLM usage is unknown.** Every ledger here covers only its own named task.
  The usage units above (API requests, tokens, job runtime, simulation runtime, TTS characters)
  **are not additive**.
- **Model fidelity is not biological validity.** Several of these runs completed and failed
  their scientific predicates — e.g. the NCA inverse-pattern comparison passed 0 of 48 executed
  design targets (`results/resources/nca-completion.json`) while the computation itself
  completed.

## Corrections to the working summary this file was compiled against

1. **Nebius jobs: 141, not 140**, and the CLI cannot page past 100 — the figure is a union with
   a repo snapshot and is a lower bound.
2. **Bioservices ledger: 110 rows / 98 HTTP calls / 89 ok / 9 failed**, not 105 / 95 / 10. The
   "10 failed" counted the Brev CLI check, which is not an HTTP call.
3. **Brev was logged in**, with a RUNNING L40S instance.
4. **Google Cloud GPU quota was 1, not 0**, and an L4 VM was created and gated.
5. **`gemini-4-argon` has no receipt**; the audit models were `gemini-3-pro-image-preview` and
   `gemini-3.1-pro-preview`, and `gemini-3-flash-preview` ran the formalize extraction.
6. **ESM2 ran locally on CPU**, not through the Nebius MCP.
7. **Print manifests do not say "unknown"** — they record an *assumed* printer and a material
   pin, with `printed: false` on every part.
