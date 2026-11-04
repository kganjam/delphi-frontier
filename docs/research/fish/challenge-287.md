# Challenge 287 — adversarial review of the correction to claim 257

**Verdict: SURVIVED**, with the units of its value field sharpened and one sub-claim marked
unverifiable.

Claim 287 is the correction entered against claim 257: that `polymers` is the chain list of one
co-folded complex rather than a batch axis, that eight polymers therefore buy one prediction at
superlinear cost, that `8` was a schema ceiling recorded as `measured` while 3 chains were
validated and nothing ran, and that `diffusion_samples` is the honest axis.

I did not write claim 287 or claim 257. I tried to break 287 on all five axes asked for. The core
assertion **got stronger under review**, because I found a vendor API reference — full-text, not
search-summary — that states the response-length rule directly. Two things in 287 are not as solid
as its wording implies, and neither is load-bearing: the cost clause holds for compute but is not
established for wall-clock against the alternative, and the process claim about the harvester is
not checkable from here.

---

## 1. What I could and could not read, independently

| source | read-level | what it gave |
|---|---|---|
| Nebius MCP `https://89.169.99.188/mcp` (`tools/list`) | **could-not-access** | agent proxy returned **`CONNECT tunnel failed, response 403`**; `__agentproxy/status` recorded `connect_rejected … gateway answered 403 to CONNECT`, host `89.169.99.188:443`, ts `2026-11-04T09:51:32.697Z`. I **independently reproduced** 257's inaccessibility. `boltz2_predict_native`'s inputSchema — the single document both claims rest on — **remains unread by any reviewer in this chain**. |
| `NVIDIA/skills`, `skills/bionemo-boltz2-nim/references/api.md` and `references/parameters.md` (raw.githubusercontent.com) | **full-text** | NVIDIA's own published API reference for the Boltz-2 NIM: field table, Polymer object, response-shape rules. This is the strongest source in the chain and **257 did not have it** — 257 carried NVIDIA at search-summary only. |
| `jwohlwend/boltz` `docs/prediction.md` | **full-text** | upstream semantics; `diffusion_samples` default `1`; `max_parallel_samples` default `5`; directory-level batching |
| `docs.nvidia.com` | **could-not-access** | `getaddrinfo ENOTFOUND`; the host must be allowed in this session's network settings to read the versioned docs or the OpenAPI spec |
| web search for the NIM schema | **search-summary** | fragmentary; surfaced a prose "minimum 1, maximum 12 polymers" and `diffusion_samples` 1–25, both of which the full-text read above then confirmed |
| this repo at `3272d3e` | **full-text** | the boltz2 schema, the 3-polymer payload and the admission refusal code are **absent** |

**Scope of my negative repo search:** case-insensitive content search for `boltz`, `polymer` and
`diffusion_sample` across every tracked file at `3272d3e`, excluding `.git`. Two hits only:
`findings/README-no-gpu-problem.md` (the string "BoltzGen" in a sentence about tooling) and a
ProteinGym row whose DMS label happens to contain the surname *Zinkus-Boltz*. **Neither is
evidence about the API.** So 287's statements that 3 chains were validated and that zero
operations ran are carried as **the original author's report**, re-stated by 257; no artifact in
this repository can corroborate or contradict them. I checked 257's two repo citations and both
are accurate: `graph_deadline_s = 1800` for the sibling `stab-ddg` App and `admission:
"not-submitted"` under maintenance are in `results/2026-10-31-kcne1-binding-ddg-STOPPED.md`, as is
the 9VEC chain staging C + A, G, J.

## 2. The axis question, re-tested against a source 257 did not have

257 argued from upstream *semantics* that `polymers` specifies one complex. That is an inference.
NVIDIA's API reference settles it mechanically, **full-text**:

> `polymers` | list[Polymer] | yes | — | **1–12 polymer chains**

> `diffusion_samples` | int | no | 1 | **Structures to generate (1–25)**

and, in the response section:

> - `structures`: **one entry per `diffusion_samples`**
> - `confidence_scores`: one float per structure

**This is a documentation read, not my calculation.** The number of returned structures is a
function of `diffusion_samples` alone. Adding polymers does not add structures; it adds chains
*inside* each returned structure. Three further fields in the same table only make sense if the
polymer list is one assembly: `constraints` accepts `Pocket | Bond` (a bond between two chains is
meaningless across unrelated jobs), `concatenate_msas` is described as "Merge MSAs across chains",
and `predict_affinity` is capped at "max 1 per request" — one binding site, one complex.

So the proxy question (asked as item 2 of the brief) was already answered correctly by 257, and I
confirm the substitution it identified: **`polymers` length stands in for returned predictions, and
the quantity that governs returned predictions is `diffusion_samples`.** My own addition is that
this is now readable in a vendor schema rather than derived from prose about complexes.

**Disagreement preserved, not averaged.** Three different polymer caps are now on the record and I
am not reconciling them: **8** (Nebius `boltz2_predict_native`, the original author's read,
unverified by anyone since, 403 at the proxy), **12** (NVIDIA Boltz-2 NIM, full-text, version
1.x — NVIDIA's docs index lists later versions I could not open, so this may move), and **no
documented maximum** (upstream `jwohlwend/boltz`, full-text; the only size limit it names is 128
atoms for an affinity ligand). 287's "maxItems 8" is therefore *vendor-specific and still
unverified*. Note that this cuts **against** the original claim 257 and **not** against 287:
287's argument does not need the cap to be 8, and if the true Nebius cap were 12 the headroom
factor the original claim asserted would be wrong by a further 50%.

## 3. Arithmetic, redone from the stated inputs without reading 257's working

The claim's cost word is "superlinear". Boltz-2 is an AlphaFold3-class trunk: a token×token pair
representation with triangle multiplicative updates and triangle attention over it. Let `L` be
tokens per chain, `k` chains, `N = kL`. Pair tensor entries go as `N²`; triangle operations as
`N³`. **Derived from the architecture — I ran no Boltz-2 job and hold no timing of my own.**

| quantity | `k` separate 1-chain calls | one `k`-chain call | ratio at `k = 8` |
|---|---|---|---|
| pair entries | `k·L²` | `k²·L²` | **8×** |
| triangle ops | `k·L³` | `k³·L³` | **64×** |

Worked once concretely, `L = 300`: eight separate calls touch `8 × 300² = 7.2 × 10⁵` pair
entries; one 8-chain call touches `2400² = 5.76 × 10⁶` — 8× more. At 128 pair channels in fp16
that single pair tensor is `5.76×10⁶ × 128 × 2 B ≈ 1.5 GB` for **one** buffer, against ≈23 MB for
the monomer; triangle updates need several live buffers. So the superlinear term lands on memory as
hard as on time, which is the failure mode a fixed per-job deadline (the repo records 1800 s for
the sibling App) punishes most. I reach the same 8× / 64× ratios as 257 by my own route; the
agreement is a check, not a copy.

**Where the cost clause is weaker than 287's wording.** "Superlinear cost" is true of trunk
compute. It does not by itself establish that one 8-chain call costs more *wall-clock than eight
separate calls*, because each separate call also pays fixed costs — model load, request setup,
and per-chain MSA work that co-folding does not avoid either. For short chains, where fixed cost
dominates `N³` work, one call could finish sooner than eight. **I have no timings for either
arrangement, so I am not asserting that regime occurs; I am saying 287 has not excluded it.** It
does not touch the verdict: in that regime the operation still returns one co-folded complex, so
the count stays 1 and the original claim's 8× headroom stays false. A cheaper way to get the wrong
object is not throughput.

A second hole in the same clause, in 287's favour this time: upstream's `max_parallel_samples`
defaults to **5** (full-text), so diffusion samples run partly in parallel. 257's corrected value
said `diffusion_samples` costs "roughly proportional wall-clock"; that is probably **too
pessimistic**, and 287 — which drops the cost adverb and says only "extra samples of one target" —
is the more defensible wording of the two.

## 4. Hidden assumption, relaxed

The assumption carrying 287 is: **`boltz2_predict_native` passes `polymers` through to Boltz-2 with
chain semantics unchanged.** Relax it and 287 fails outright — a wrapper free to fan a polymer list
out into `k` independent single-chain jobs would make the original claim right and this correction
wrong.

Tested as far as it can be: the tool name ends in `_native`, which reads as native-format
passthrough rather than fan-out; the only two public APIs that use the key name `polymers` both
treat it as one complex (NVIDIA full-text, upstream full-text); and a fan-out wrapper would have no
coherent meaning for `constraints: [Bond]`, `concatenate_msas`, or a single `predict_affinity`
site. **But the Nebius schema is 403 to me and was 403 to 257, so this is argument from convention
and from sibling APIs, not verification.** It is the one input whose failure would flip my verdict,
and it is unread. I record it as such rather than treating the matter as closed.

Smaller assumption, inherited and untested by anyone: that the per-chain coordinates returned from
an 8-chain co-fold are unusable as monomer predictions. That is biophysically well-motivated —
every chain is conditioned on seven partners absent from the biology — but it is **not measured**,
by 287, by 257, or by me. It is also not needed: the response-shape rule in §2 already caps
returned structures at `diffusion_samples` independent of chain count, which defeats the 8× claim
without any argument about quality.

## 5. Evidence level

287 records **derived**, and that is honest for the value it reports. It is derived: no operation
ran, and the conclusion comes from documented input/output semantics plus architecture, not from
observation. 287 is also right that 257's parent recorded `measured` for a declared `maxItems`,
which is a read of a constraint; `listing` is the correct level there, and the distinction matters
because the throughput inference was borrowing the schema read's credibility.

Two notes against 287's own bookkeeping:

1. **The value's unit is ambiguous.** "1 independent prediction per operation" is right if
   *prediction* means *target*, and wrong if it means *returned structure* — one operation returns
   up to `diffusion_samples` structures (≤25 per NVIDIA, full-text). The two readings differ by a
   factor of 25 and the field does not say which. Sharpened below.
2. **"not checked by harvester" is unverifiable from here.** I searched this repo at `3272d3e`
   for any harvester record, ledger entry or schema capture and found none (scope as in §1). The
   claim may be true; I cannot confirm it, and my verdict does not rest on it.

## 6. Regime and counter-example search

Scope of the negative search: upstream `docs/prediction.md` full-text; NVIDIA's published Boltz-2
NIM API reference and parameter guidance full-text; a web search for a documented polymer-list
`maxItems`; GitHub code search across the repositories this session can reach for
`diffusion_samples polymers boltz2` (328 hits, top results inspected — all NVIDIA NIM wrappers and
client code, none exposing a batch-of-targets endpoint). **I found no API, wrapper or published
example in which a polymer list is a batch of independent targets.** Absence of a counter-example
across these four sources is not proof that none exists, and none of this reaches the Nebius
endpoint itself.

The regime where multiple polymers is correct is the one 257 already named and 287 preserves: when
the target *is* an assembly — homo-oligomers, binder–target, receptor–peptide, and this repo's
KCNQ1–KCNE1 case. There, separate calls cannot produce the answer at all. Nothing in 287 denies
this, and nothing in my review disturbs it.

## 7. What this review establishes

- **Establishes:** NVIDIA's Boltz-2 NIM documents `polymers` as 1–12 chains of one complex and
  `structures` as one entry per `diffusion_samples` (full-text) — returned predictions are a
  function of samples, not of chain count, which is 287's central claim confirmed from a source
  stronger than the one 257 used; the polymer cap is vendor-specific with 8 / 12 / unbounded on
  the record and the Nebius value unverified by anyone; the 8× / 64× superlinear ratios reproduce
  independently; the Nebius schema is still 403, reproduced today; the repo holds no artifact of
  the payload, the refusal code or the harvester step.
- **Does not establish:** that the Nebius cap is or is not 8; that `boltz2_predict_native` does not
  fan out (convention and sibling APIs only, schema unread); any Boltz-2 timing or memory figure,
  since I ran nothing and the table in §3 is derived from architecture; that one 8-chain call is
  slower in wall-clock than eight separate calls; whether per-chain coordinates from a co-fold are
  usable as monomer predictions; the harvester process claim.
- **Does not establish** anything about any protein, variant or phenotype.

## 8. What would settle the remainder

One readable schema. Allow `89.169.99.188:443` at the agent proxy (or paste the `tools/list`
output) and the cap, the `diffusion_samples` range and the fan-out question all resolve in a single
read, with no GPU time. The quality question needs the two-job experiment 257 proposed; the cost
question needs one timing pair. Until then the axis conclusion is derived — correctly labelled, and
correct.

---

```swarm-challenge
{"claim_id": 287, "outcome": "survived", "reason": "I tried to break it and instead confirmed its core from a stronger source than it used: NVIDIA's Boltz-2 NIM API reference states full-text that polymers is 1-12 chains of one complex and that returned structures number one per diffusion_samples, so chain count cannot multiply predictions; the only defects I found are a value field whose unit is ambiguous between target and structure, a cost clause that holds for compute but has not excluded a fixed-overhead regime, and an unverifiable harvester process claim, none of them load-bearing.",
  "corrected_value": "1 independent target per operation regardless of chain count (polymers 1-12 per NVIDIA's Boltz-2 NIM full-text, 8 per the unverified Nebius read, no documented cap upstream); that one target is returned as up to diffusion_samples structures per operation (<=25 per NVIDIA, <=8 per the unverified Nebius read), so the honest axis yields samples of one target and not extra targets",
  "depends_on": ["NVIDIA/skills skills/bionemo-boltz2-nim/references/api.md (full-text, raw.githubusercontent): polymers is a 1-12 chain list, diffusion_samples 1-25, response field 'structures' has one entry per diffusion_samples", "NVIDIA/skills references/api.md same read: constraints accept cross-chain Bond, concatenate_msas merges MSAs across chains, predict_affinity max 1 per request - all single-complex semantics", "jwohlwend/boltz docs/prediction.md (full-text): one entry per unique chain, diffusion_samples default 1 as samples per input, batching is per input file, max_parallel_samples default 5, no documented chain cap", "boltz2_predict_native passes polymers through to Boltz-2 with chain semantics unchanged and does not fan the list out into independent jobs (argument from naming convention and sibling APIs only; the Nebius inputSchema is could-not-access, 403 to CONNECT on 89.169.99.188:443, reproduced 2026-11-04T09:51:32Z - this is the one input whose failure would flip my verdict)", "Boltz-2 is AlphaFold3-class with an O(N^2) pair representation and O(N^3) triangle operations, giving 8x pair and 64x triangle ratios at k=8 (derived from architecture, reproduced independently here, not measured)", "the original author's report that a 3-polymer payload passed validation and that zero operations completed (not corroborable: payload, schema dump and refusal code are absent from this repo at 3272d3e)", "claim 257's parent recorded evidence level 'measured' for a declared inputSchema maxItems"]
}
```
