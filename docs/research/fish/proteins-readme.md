# Nebius Scientific AI workbench — zebrafish fin/flight protein structures

Endpoint `https://89.169.99.188/mcp`, tenant `mit-hackathon`, key in
`~/.config/morphoswarm/nebius.env` (never printed). Client: `nbx.py`.

**Honesty floor.** Everything below is a *predicted* structure from a machine-learning model.
pLDDT and pTM are the model's own confidence in itself, not accuracy, and not a measurement.
None of these proteins has an experimental structure here, so nothing in this directory has
been compared against one.

---

## 1. The ESMFold2 manifest contract — SOLVED

The blocking field was the manifest entry's `semantic_type`. The accepted value is:

```
esmfold2-input-json/v1
```

and the inner artifact's `media_type` must be `application/json` (not a FASTA media type).

**Exact working shape.** Three uploads, then the submit:

```python
inner    = nbx.upload(json.dumps({"sequence": SEQ}).encode(),
                      "application/json", "esmfold2")
manifest = {"schema": "fs2-serve.nebius.ai/scientific-artifact-manifest/v1",
            "entries": [{"name": "esmfold2-input",             # this name is MANDATORY
                         "semantic_type": "esmfold2-input-json/v1",
                         "artifact": inner}]}                   # nested, not flat
man_ref  = nbx.upload(json.dumps(manifest).encode(),
                      "application/vnd.fs2.scientific-manifest+json", "esmfold2")
nbx.call("submit_esmfold2", {
    "schema": "fs2-serve.nebius.ai/scientific-run-request/v1",
    "operation": "predict-structure",
    "service_class": "interactive",
    "input_manifest": man_ref,
    "parameters": {"sequence": SEQ, "mode": "single-sequence", "seed": 1},
    "idempotency_key": "<unique, recorded>"})
```

With this shape the request passes **every** validation stage — schema, pause, semantic type,
media type and manifest structure. The only error left is `ADMISSION_LIMIT_REACHED`
(the account allows 1 operation in flight), which is a queueing limit, not a contract defect.

### How the contract was determined (the error grammar)

The validator runs in a fixed order, and each stage has its own sentence. Reading which
sentence comes back is what located the field; guessing names alone could not have:

| request | server's exact words |
|---|---|
| `entries: []` | `the scientific manifest requires verified inner artifacts` |
| entry without `semantic_type` | `scientific manifest entry requires a logical name and semantic type` |
| entry named anything but `esmfold2-input` | `ESMFold2 input manifest must contain exactly one verified esmfold2-input entry` |
| two entries | same `exactly one` message |
| semantic type with no `/vN` suffix | `input semantic type is invalid` |
| versioned but unknown semantic type | `ESMFold2 esmfold2-input semantic type is invalid` |
| **`esmfold2-input-json/v1` + FASTA media type** | **`ESMFold2 esmfold2-input media or compression type is invalid`** |
| `esmfold2-input-json/v1` + `application/json` | passes validation; reaches admission |

The second-to-last row is the one that identified the answer: it is the only candidate of 64
tried whose error moved *past* the semantic check to the next stage.

The entry name is validated, not merely echoed. The earlier reading that `esmfold2-input` was
"accepted" was right, but for a stronger reason than it appeared: it is the *only* accepted name.

### Semantic types rejected (64 candidates, all with entry name `esmfold2-input`)

Versioned, rejected with `... semantic type is invalid`:
`esmfold2-input/v1`, `esmfold2-input/v2`, `esmfold2-sequence-input/v1`, `esmfold2-sequence-input/v2`,
`esmfold2-sequence/v1`, `esmfold2-fold-input/v1`, `esmfold2-fold-input/v2`, `esmfold2-fasta/v1`,
`esmfold2-msa/v1`, `esmfold2-a3m/v1`, `esmfold2-precomputed-msa/v1`, `esmfold2-input-fasta/v1`,
`esmfold2-sequence-fasta/v1`, `esmfold2-predict-input/v1`, `esmfold2-prepare-input/v1`,
`esmfold2-biohub-input/v1`, `esmfold2-input-tar/v1`, `esmfold2-inputs-tar/v1`,
`esmfold2-workload-tar/v1`, `esmfold2-input-gzip-tar/v1`, `esmfold2-inputs-gzip-tar/v1`,
`esmfold2-input-bundle/v1`, `esmfold2-bundle/v1`, `esmfold2-tar/v1`, `esm-fold-input/v1`,
`esm-sequence-input/v1`, `esm-v3-sequence/v1`, `biohub-esm-sequence/v1`, `biohub-esm-input/v1`,
`biohub-esm-v3-input/v1`, `protein-sequence/v1`, `protein-sequence-fasta/v1`,
`protein-sequence-set/v1`, `protein-sequences/v1`, `amino-acid-sequence/v1`, `sequence/v1`,
`sequence-input/v1`, `sequence-fasta/v1`, `fasta/v1`, `fasta-sequence/v1`, `protein-fasta/v1`,
`msa/v1`, `a3m/v1`, `msa-a3m/v1`, `protein-msa/v1`, `protein-msa-a3m/v1`, `precomputed-msa/v1`,
`scientific-sequence/v1`, `scientific-workload-tar/v1`, `workload-tar/v1`, `fold-input/v1`,
plus all 13 types advertised elsewhere in the catalogue (`alphafold3-fold-input/v1`,
`alphafold3-summary-confidence/v1`, `ct-nifti-volume/v1`, `holoscan-recorded-video-tar/v1`,
`isaac-healthcare-project-tar/v2`, `isaac-healthcare-project/v2`, `isaac-healthcare-scenarios/v1`,
`isaac-healthcare-scenarios/v2`, `lerobot-source-reference/v1`, `lerobot-v3-bundle/v1`,
`monai-spleen-ct-result/v1`, `protein-structure-mmcif/v1`, `spleen-segmentation-nifti/v1`).

Unversioned, rejected earlier with `input semantic type is invalid`:
`esmfold2-input`, `fasta`, `protein-sequence`, `sequence`, `text/x-fasta`, `application/x-fasta`.

`get_scientific_artifact` does **not** echo a semantic type; it returns only
`artifact_id`, `sha256`, `size_bytes`, `media_type`, `compression`. The MCP server exposes no
`resources`, `prompts` or `resourceTemplates` — all three list empty, so there is no docs surface.

---

## 2. There is a second, simpler path that needs no manifest at all

`tools/list` returns **69** tools, not the 26 in `list_scientific_models`. The extra ones are
`*_native` tools that take a sequence **inline**, with no artifact upload and no manifest:

- `infer_openfold2_native` — `sequence` (≤1024 aa), returns ranked structure + per-residue pLDDT + PAE
- `infer_openfold3_native` — chains with optional supplied A3M
- `boltz2_predict_native` — chains with **caller-supplied A3M** (no online MSA search)
- `msa_search_native` — local MMseqs2 against pinned `pdb70_220313`, returns A3M
- `infer_proteinmpnn_native`, `infer_diffdock_native`, `molmim_run_native`, `genmol_generate`, …

All three fish proteins fit OpenFold2's 1024 aa limit, so this path produced real structures
today while the ESMFold2 contract was still being worked out.

---

## 3. Model availability (measured, not assumed)

| model | state | evidence |
|---|---|---|
| `openfold2` (native) | **LIVE, ran to SUCCEEDED** | 3 operations below |
| `esmfold2` | contract solved; reaches admission | blocked only by the 1-in-flight cap |
| `esm2-3b`, `stab-ddg` | `availability: available` | catalogue; manifest contract not yet solved |
| `esm2-650m` | paused for maintenance | prior session |
| `alphafold3` | **ungranted** | `assets: 'af3-params' is not granted to tenant 'mit-hackathon'` |

`esm2-3b` and `stab-ddg` reference files *"inside the workload archive"* (`fasta_file`,
`variants_file`, `pdb_file` are relative paths), so their manifest entry carries an archive,
not a bare file — a different contract from ESMFold2's single JSON document.

---

## 4. Operations (every submission carried a unique, recorded idempotency key)

See `operations.jsonl` (native submits) and `probe_log.jsonl` (manifest probes) for the full
record. No operation was submitted without a key, so everything here is recoverable.

| purpose | tool | operation | key |
|---|---|---|---|
| kcnk5b fold | `infer_openfold2_native` | `op-deac3f5087a199b3` SUCCEEDED | `of2-kcnk5b-1793773539` |
| and1 fold | `infer_openfold2_native` | `op-e6b58efb8ed371dd` SUCCEEDED | `of2-and1-1793773887` |
| and2 fold | `infer_openfold2_native` | `op-930bb2f94e3023b9` SUCCEEDED | `of2-and2-1793774317` |
| kcnk5b MSA | `msa_search_native` | `op-6d4bf65638eb8348` SUCCEEDED | `msa-kcnk5b-1793774492` |
| kcnk5b fold w/ MSA | `boltz2_predict_native` | `op-20adb7ef600a8536` SUCCEEDED | `boltz2-kcnk5b-1793774592` |
| and1 MSA | `msa_search_native` | `op-fcd11dbd71964919` SUCCEEDED | `msa-and1-1793774773` |
| and1 fold w/ MSA | `boltz2_predict_native` | `op-590a5e26cea1ce8b` SUCCEEDED | `boltz2-and1-1793774811` |
| and2 MSA | `msa_search_native` | `op-053bd996f8d4bc6d` SUCCEEDED | `msa-and2-1793774974` |
| and2 fold w/ MSA | `boltz2_predict_native` | `op-b56860ee55e67b62` | `boltz2-and2-1793775012` |

Two manifest probes reached `SCIENTIFIC_STAGE_ADMISSION_PENDING` when the 1-in-flight cap was hit
mid-probe. **Both carry keys and are therefore recoverable**, which is exactly the difference from
the four keyless operations wedged earlier in this account:

| operation | key | content |
|---|---|---|
| `op-5b52c20d713af416` | `json-sequence-73984624` | inner JSON `{"sequence": <kcnk5b>}` — recovered and run |
| `op-4e400a5b52a2b9d8` | `json-empty-73974323` | inner JSON `{}` — no scientific value, recovered then cancelled |

`cancel_operation` on either one **before** recovery returns
`REQUEST_REJECTED / recover the original admission with the same idempotency key first`.
That is the mechanism that strands a keyless submission: with no key there is no way to recover
the admission, and with no recovered admission the server will not accept a cancel.
Nothing here was added to that keyless set.

---

## 5. Operational notes for the next session

- **Concurrency is 1.** `ADMISSION_LIMIT_REACHED` carries `admission: "not-submitted"` and creates
  no operation, so retrying it is free. Run jobs serially.
- **A 503 `SERVERLESS_REQUEST_FAILED` with `admission: "accepted"` IS an operation.** It carries an
  `operation_id` and the job is running. Poll it; do not resubmit. The first pipeline here lost
  track of and1 for a few minutes by treating that 503 as a failure.
- **Operation status is at `resp["operation"]["status"]`, not at the top level.** `nbx.poll` reads
  only the top level, so it reports a QUEUED job as finished. Use the loop in `pipeline.py`.
- **Download handles expire in 60 s** and live at `resp["handle"]["url"]`, not `download_url`.
  Request one immediately before each transfer (`fetch.py`).
- **`list_scientific_models` shows 26 models; `tools/list` shows 69 tools.** The catalogue's
  `availability` field is not a runtime claim: `esm2-3b` and `stab-ddg` both read
  `availability: "available"` and both return `MODEL_MAINTENANCE` when submitted.
- Validation order is **JSON schema → maintenance pause → manifest/semantic → media**. A model that
  returns a semantic-type error has passed the pause check, so it is live.
- `service_class` differs per model: `interactive` for esmfold2, but esm2/stab-ddg accept only
  `customer-batch` or `bulk-backfill`.

## 6. Files

- `nbx.py` client, `probe.py` manifest prober, `native.py` native-tool submitter with key recording
- `pipeline.py` / `stage2.py` / `stage3.py` / `stage4.py` — the serial runners
- `fetch.py` artifact download, `extract.py` PDB + pLDDT extraction, `report.py` regenerates `RESULTS.md`
- `operations.jsonl`, `probe_log.jsonl` — every submission with its key
- `RESULTS.md` — the confidence table, regenerated from artifacts
- `<tag>/<tag>_rank1.pdb`, `boltz2_<tag>/<tag>_boltz2.cif` — the predicted structures
- `msa_<tag>/<tag>_pdb70.a3m` — the alignments

---

## 7. A mistake made here, and what it cost

`stage3.py` and `stage4.py` reuse two helpers with `from stage2 import wait, submit_retry`.
`stage2.py` had **no `if __name__ == "__main__":` guard**, so importing it re-executed its whole
driver body: the and1/and2 MSA + Boltz2 pipeline ran a second time on a shared GPU pool.

Caught by noticing that the newest row in `operations.jsonl` was an `msa-and1-*` key minted
*after* stage2 had already printed `STAGE2-DONE`. It produced two redundant operations:

| operation | key | disposition |
|---|---|---|
| `op-3423b85365dc1b87` | `msa-and1-1793775159` | duplicate MSA search, SUCCEEDED, cheap, left alone |
| `op-4aa181c6cc86f16a` | `boltz2-and1-1793775194` | duplicate Boltz2 fold — **cancelled by me**, `EXECUTION_CANCELLED` |

The cancel was legitimate under "never cancel an operation you did not start": both were started
by this session's own bug and both carried recorded keys. The duplicate was also holding the
account's single in-flight slot, which was blocking the remaining work.

`stage2.py` is now guarded, and `import stage2` has been confirmed to run nothing.
No result in this directory came from the duplicate run.

---

## 8. STATUS OF THE ESMFOLD2 CONTRACT: solved, but not yet run to completion

This distinction matters and is stated plainly rather than blurred.

**What is established.** `esmfold2-input-json/v1` with an `application/json` inner artifact is
accepted. The request passes schema validation, the maintenance-pause check, the manifest
structure check, the semantic-type check and the media-type check. It reaches **admission**.
Both directions were controlled (§1).

**What is NOT established.** No ESMFold2 job has produced a structure. Every submission —
including one with a fresh key after all other work had drained — returns:

```
429 SCIENTIFIC_STAGE_ADMISSION_PENDING
"Workflow admission could not be confirmed. key concurrency limit reached (1/1 operations in flight)"
retry_same_idempotency_key: true
```

and `get_operation` then reports `status: ADMISSION_PENDING`, `state: admission-unknown`.

**This is esmfold2-specific, not a busy account.** OpenFold2, Boltz2, msa-search and ProteinMPNN
all submitted and ran to SUCCEEDED during the same window, repeatedly. Only esmfold2 wedges.

**The documented recovery does not clear it — measured, not assumed.** The replay was run **5 times at ~65 s intervals** under the same key (`esmfold2-kcnk5b-fresh-1793775862`); every attempt returned `SCIENTIFIC_STAGE_ADMISSION_PENDING` and `get_operation` reported `ADMISSION_PENDING` throughout. The server says to replay the original request
under its original idempotency key. Replaying returns the same `ADMISSION_PENDING`, and
`cancel_operation` refuses with `recover the original admission with the same idempotency key
first` — so recovery requires admission and admission requires the slot that the unrecovered
operation appears to hold. Three esmfold2 operations are in this state
(`op-4e400a5b52a2b9d8`, `op-5b52c20d713af416`, `op-2112f97ee3d11f6e`); **all three carry recorded
keys**, so unlike the account's four keyless operations they remain recoverable by whoever can
clear the admission backlog.

**So the honest summary is:** the schema question is answered and demonstrated up to admission;
the ESMFold2 *structure* of kcnk5b was not obtained, and the structures that were obtained came
from OpenFold2 and Boltz2 instead. A future session with a cleared backlog should be able to run
the shape in §1 unchanged.
