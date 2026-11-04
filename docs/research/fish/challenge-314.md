# Challenge 314 — "Nebius manifest path is undocumented"

Adversarial review of a claim I did not write. Verdict: **WEAKENED**. The core observation probably
stands, but I could not reproduce it. The universal negative reaches further than the surfaces that
were actually searched. And the workaround reads as tested when nothing in the record shows that it
was.

## What I could and could not check

| Check | Result | Read-level |
|---|---|---|
| Re-probe the Nebius MCP endpoint (`https://89.169.99.188/mcp`, the address in `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6) | **could not access**: this container's egress proxy refuses the tunnel (`CONNECT tunnel failed, response 403`). I ran no `submit_esmfold2_fast`, `get_model_schema` or `list_scientific_models` call. | could-not-access |
| Search this repo (all tracked files, case-insensitive) for `semantic_type`, `semantic type`, `esmfold`, `manifest`, `_native` | **zero hits** for every term. The repo holds no log, transcript or JSON of the six rejected values, the 18 native tools, or the alphafold3/isaac/monai/holoscan/lerobot semantic types. | full-text (repo) |
| Repo context on the same server | `findings/README-no-gpu-problem.md` and the KCNE1 STOPPED result record **69 tools**, server `Nebius Scientific AI 0.1.0`, and a working upload path (`begin_` → presigned PUT → `finalize_scientific_artifact_upload`). Neither mentions semantic types. | full-text |
| Public web, one standard search (`Nebius "Scientific AI" MCP semantic_type input manifest esmfold`) | **no public documentation** of this server, its manifest format or `semantic_type`. Hits were unrelated community ESMFold MCP servers and a third-party Nebius AI Studio listing with 4 tools. Scope: one English search; this is absence at that depth. | search-summary |

So the "measured" content of the claim rests **entirely on the host session's report**. I did not
observe any of it. That is not a fault in the claim. It does mean this review tests the claim's
logic and scope, and does not re-measure it.

## 1. Arithmetic

There is none to redo. The numbers in the claim are counts: 6 values rejected, 18 `*_native` tools,
5 model families with published semantic types. I cannot recount them: the endpoint is unreachable
and the repo holds no record of them. I mark each of them `unknown (unverified here)`.
The 69-tool total is consistent with the repo's earlier record. It is not checkable against "18".

## 2. Proxy

The claim says "the manifest path is blocked". The proxy standing in for that is "six guessed
`semantic_type` strings were rejected". The quantity that matters is whether *any* accepted value
exists that a client can discover. Six guesses from an open string space sample almost none of it.
The claim's real force comes from the second leg, "no value is published". That leg is the one to
attack.

## 3. Hidden assumptions, relaxed

**A. "Published anywhere reachable" was searched on three surfaces, not everywhere.** The claim
names `list_scientific_models`, `get_model_schema`, and the model's `input_artifact_contract`. It
does not say that these were checked:
- the **MCP `tools/list` `inputSchema` of `submit_esmfold2_fast` itself**, where an `enum` on
  `input_manifest[].semantic_type` would normally live;
- **MCP `resources/list` / `prompts/list`** on the same server;
- the **upload tools' schemas** (`begin_scientific_artifact_upload`), and the **full error body**
  of the rejection, which validators often extend with an allowed-values list;
- the **alphafold3** semantic types. AF3 also takes protein sequences, so its published types are
  the obvious seventh candidate. The claim calls them "model-specific" and does not say whether one
  was tried.
"Anywhere reachable" is therefore wider than the evidence. The scoped form that is supported:
*not found on these three catalog surfaces*.

**B. The semantic type may be bound at upload, not chosen in the manifest.** The repo's verified
flow assigns metadata at `begin_scientific_artifact_upload`. The error "input semantic type is
invalid" fits two readings. In one, the string is not in the server's vocabulary. In the other,
it does not match the type recorded for the referenced artifact, or it is not allowed for *this
model's* contract. The second reading is plausible given that the contract is **empty**. If it
holds, no string would ever pass, whatever the docs said. The diagnosis would then be "ESMFold2's
manifest path is unconfigured", not "undocumented". The practical conclusion, *blocked*, is the
same either way. The stated cause is not established. This is my inference, not something the
author or I measured.

**C. An empty `input_artifact_contract` is itself evidence.** It reads more naturally as "this
model has no manifest inputs wired" than as "the inputs exist but are undocumented". The claim
treats it as a missing doc.

## 4. Evidence level — partly overstated

"Measured" is honest for what was observed: six rejections, each with `admission: not-submitted`,
plus the empty-manifest refusal. It is **not** honest for two other parts:
- **the workaround.** The claim says the `*_native` tools "are the usable path for a sequence".
  The record gives no successful native submission and no native folding result. It does not even
  name a native tool that folds a sequence. "Take inline input and need no manifest" is a
  schema reading. "Usable" is an inference from it. This repo has already seen this failure once:
  `submit_stab_ddg` had a verified upload path and then returned **HTTP 503 `MODEL_MAINTENANCE`**
  at admission (KCNE1 STOPPED §6). A well-formed input path is not a usable compute path.
- **"no allowed value is published anywhere".** This is a scoped negative search presented as a
  universal measured fact. See 3A.

## 5. Counter-examples and regimes missed

- An **alphafold3** protein or sequence semantic type accepted cross-model. This is untested in
  the record, as far as the claim states.
- **Server version drift.** The server reports `0.1.0`, and `stab-ddg` carries a dated runtime
  revision (`…-20261024`). An undocumented manifest vocabulary on a 0.1.0 server may be filled in
  without notice. The negative is dated: **2026-11-04**.
- I found no published counter-example: one web search found nothing. So the core observation is
  **not refuted**.

## Corrected statement

> On 2026-11-04 (host-session report, not re-measured here), `submit_esmfold2_fast` refused six
> guessed `semantic_type` values and an empty manifest at admission. No accepted protein-sequence
> semantic type was found in `list_scientific_models`, `get_model_schema`, or the model's empty
> `input_artifact_contract`. Not reported as checked: the tool's own MCP `inputSchema`,
> `resources/list`, the upload-tool schemas, the full error body, and the alphafold3 types. It
> is unknown whether the cause is missing documentation or an unconfigured contract. The
> `*_native` tools accept inline input per their schemas. That they *work* for a sequence is
> **untested**. Treat the manifest path as blocked and the native path as the next thing to try,
> not as a confirmed path.

## Sources

- `findings/README-no-gpu-problem.md` — full-text (repo)
- `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6 — full-text (repo)
- Nebius MCP endpoint — could-not-access (proxy 403 from this container, 2026-11-04)
- Web search, 2026-11-04 — search-summary: [lobehub esmfold mcp](https://lobehub.com/mcp/biomolecular-design-nexus-esmfold_mcp),
  [conare ESMfold MCP](https://conare.ai/marketplace/mcp/esmfold-mcp),
  [MCPBundles Nebius AI](https://docs.mcpbundles.com/skills/nebius-ai). None of them document the Nebius Scientific AI manifest.

```swarm-challenge
{"claim_id": 314, "outcome": "weakened", "reason": "The reported rejections were not refuted (unreproducible here, proxy 403), but 'published anywhere reachable' outruns the three surfaces searched (tool inputSchema, resources, upload schemas, error body and alphafold3 types were not reported as checked), the cause (undocumented vs unconfigured contract) is not established, and the *_native workaround is labelled usable without any successful native run in the record.", "corrected_value": null, "depends_on": ["host-session report of six semantic_type rejections with admission=not-submitted (2026-11-04, unverified here)", "host-session report that input_artifact_contract for esmfold2-fast is empty", "host-session report of 18 *_native tools taking inline input", "results/2026-10-31-kcne1-binding-ddg-STOPPED.md §6: upload path verified but submit refused with MODEL_MAINTENANCE", "this container could not reach https://89.169.99.188/mcp (proxy 403)", "repo full-text search: no record of semantic_type/esmfold/manifest/_native", "one standard web search found no public Nebius Scientific AI manifest documentation"]}
```
