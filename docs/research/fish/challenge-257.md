# Challenge 257 — "work per slot can be raised 8x by batching chains into one Boltz-2 call"

**Verdict: REFUTED.** The schema fact is probably right and the inference drawn from it is wrong.
`polymers` is the chain list of **one complex**, not a batch of independent targets, so eight
polymers in one operation buy **one** prediction, not eight. The evidence level is also
mis-stated: a declared `maxItems` is a read of a constraint, not a measurement of throughput, and
the batch that "reached admission" was **3 chains and never executed**.

Reviewer did not write the claim. Single-reader review.

---

## 0. The claim as recorded

> WHAT CAN BE RAISED IS WORK PER SLOT: `boltz2_predict_native` takes `polymers` with `maxItems` 8
> and `diffusion_samples` up to 8, so one operation can carry eight chains. We had been submitting
> one sequence at a time, leaving 8x unused. A 3-protein batch was built and validated — it reached
> admission and was refused only because the slot was occupied by our own test.

Recorded evidence level **measured**, value **8 chains per operation**, source
*`boltz2_predict_native` inputSchema; 3-protein batch reached admission*.

## 1. What I could and could not read

| source | read-level | what it gave |
|---|---|---|
| Nebius MCP `https://89.169.99.188/mcp` | **could-not-access** | agent proxy answered **403 to CONNECT** for `89.169.99.188:443` (`__agentproxy/status` → `recentRelayFailures: connect_rejected, 2026-11-04T09:38:58Z`). I could not re-read `boltz2_predict_native`'s inputSchema, so **`maxItems: 8` and the `diffusion_samples` cap of 8 are unverified here** and are carried as the author's claim. |
| `jwohlwend/boltz` `docs/prediction.md` | **full-text** | the authoritative upstream semantics of multi-chain input and of `diffusion_samples` |
| NVIDIA NIM for Boltz-2 API (`polymers` array, `diffusion_samples` 1–25) | **search-summary** (docs.nvidia.com is not resolvable from this session and must be allowed in the session's network settings to read it) | the only public API that uses the key name `polymers`; its documented `diffusion_samples` range is **1–25**, which **disagrees** with the claim's cap of 8 |
| this repo, working tree at `3272d3e` | **full-text** | no record of the boltz2 schema, the 3-protein payload, or the admission response |

**Scope of the negative repo search:** case-insensitive content search for `boltz2`, `polymers`,
`diffusion_samples` and `admission` over every tracked and untracked file outside `.git` at commit
`3272d3e`. The only hit for `admission` is `results/2026-10-31-kcne1-binding-ddg-STOPPED.md`. The
payload, the schema dump and the refusal code behind this claim **are not in the repository**, so
nothing about them could be checked against an artifact.

**Disagreement preserved, not averaged:** the claim says the `diffusion_samples` cap is 8; NVIDIA's
Boltz-2 NIM documents 1–25; the `boltz` upstream option defaults to 1 with no cap named; a
third-party wrapper surfaced in search caps it at 50. A Nebius-specific narrowing to 8 is entirely
plausible and I cannot confirm or deny it. Nothing below depends on which cap is right.

## 2. The arithmetic, redone from the stated inputs alone

The claim offers two capacity axes and one factor:

- `polymers` ≤ 8 → ×8
- `diffusion_samples` ≤ 8 → ×8
- prior usage: 1 sequence per operation
- stated headroom: **8x**

Independently: if both axes are unused headroom, the product is **64**, not 8. If only chains
count, it is 8. If only samples count, it is 8. **The claim's own two inputs do not produce the
claim's own stated factor** — it has silently dropped one axis while citing both as support. That is
a defect in presentation even before the semantics are examined, and it matters because the axis it
kept (chains) is the invalid one and the axis it dropped (samples) is the valid one.

Second arithmetic point: the thing that was actually built and validated carried **3** polymers.
3/8 = **37.5%** of the declared cap. Even on the claim's own (mistaken) reading, the demonstrated
figure is 3x, not 8x; **8 is a schema ceiling that was never populated**.

## 3. The proxy — and the quantity that matters

**Proxy in use:** *chains accepted per operation.*

**Quantity that matters:** *independent, usable predictions returned per slot per unit wall-clock.*

These come apart completely, because `polymers` is not a batch dimension. Upstream, read full-text:

> the input "specifies the components of **the complex**"; the sequences section "has one entry per
> unique chain or molecule"; "if multiple identical entities exist, set `id` as a list (e.g.
> `[A, B]`)"

and confidence output includes **per-chain-pair interface scores** — a thing that only exists
because the chains were folded *together*. Batching is a separate mechanism entirely: upstream you
pass a **directory**, and "predictions will be run on all `.yaml` and `.fasta` files inside," each
input getting its own output subfolder. `--max_parallel_samples` applies to diffusion samples
*within* one prediction, not across inputs.

So (my inference from those quoted semantics, not the author's claim): putting eight unrelated
monomers into one `polymers` list does not return eight monomer predictions. It returns **one
eight-chain co-folded assembly**, in which every chain's conformation is conditioned on seven
partners that are not present in the biology being studied — manufactured interfaces, pTM/ipTM
computed over a complex nobody asked about, and per-chain coordinates that are *not* the
single-chain prediction a 1-chain job returns. Independent usable monomer predictions per
operation: **1**.

`diffusion_samples` is the one axis that does raise work per slot honestly: upstream calls it "the
number of diffusion samples to use for prediction," default 1, and the outputs are
`diffusion_samples` structures of **the same input**, ranked by confidence. More samples per slot
is real extra work and real extra information (pose diversity, a confidence ranking). It is also
the axis the claim's headline factor discards.

## 4. The hidden assumption, relaxed

**Hidden assumption: runtime per operation is independent of how many chains it carries** — without
it, "8 chains per operation" cannot mean "8x work per slot" even if the chains were independent.

Relaxed, it fails, and in the wrong direction. Boltz-2 is an AlphaFold3-class architecture: the
trunk carries a **pairwise** token×token representation and triangle-update/attention operations
over it. Let `L` be per-chain tokens and `k` chains, `N = kL`. Pair tensor elements scale as `N²`;
triangle multiplicative updates and triangle attention scale as `N³`.

| | pair elements | triangle ops |
|---|---|---|
| `k` separate 1-chain operations | `k·L²` | `k·L³` |
| one `k`-chain operation | `k²·L²` | `k³·L³` |
| ratio at `k = 8` | **8x more** | **64x more** |

**This is derived from the architecture's scaling, not measured — I ran no Boltz-2 job and have no
timing of my own.** But the sign of the result does not depend on the exponents being exactly 2 and
3: any superlinear trunk makes one 8-chain operation *more* expensive than eight 1-chain
operations, never cheaper. The slot does not do 8x the work for free; it does less useful work for
more of it. And where the stack imposes a per-job wall-clock deadline — this repo records
`graph_deadline_s = 1800` for the sibling `stab-ddg` App
(`results/2026-10-31-kcne1-binding-ddg-STOPPED.md`, full-text; **the boltz2 deadline is unknown to
me**) — the large-complex job is the one that gets killed, taking all eight results with it instead
of one.

A second hidden assumption, smaller: that eight chains each arrive with what they need. Upstream
requires an MSA per protein chain; co-folding does not amortise that.

## 5. "Reached admission" is not evidence of feasibility

The strongest-sounding evidence is the weakest. A payload refused at admission demonstrates exactly
one thing: **it passed input validation**. It does not show the job runs, fits the deadline, fits
GPU memory, or returns per-chain output anyone can use. **Zero operations completed.** The
claim's own framing concedes this and then reads past it.

The refusal's own content also cuts against the conclusion. The claim asserts it was refused "only
because the slot was occupied by our own test." If that is right, the binding constraint is
**operations in flight — one at a time — which batching chains does not relax at all**; the claim
has found the real bottleneck and then proposed a lever that does not touch it. If it is wrong, the
same endpoint is on record in this repo returning `admission: "not-submitted"` under a **503
`MODEL_MAINTENANCE`** for reasons having nothing to do with occupancy, so "refused only because the
slot was occupied" requires the actual error code to distinguish, and that code is **not in the
repository** (scope in §1).

## 6. Evidence level

**Not honest as recorded.** Three distinct problems:

1. **`measured` → `listing`.** What was read is a *declared constraint* in an inputSchema. A
   schema's `maxItems` is a statement of what the server will accept, not an observation of what it
   delivers. Nothing was measured; one payload was validated.
2. **The value is a ceiling, not an observation.** 8 is the declared maximum; 3 is what was built;
   0 ran.
3. **The headline is derived and presented as read.** "Leaving 8x unused" is an inference from the
   schema, and a false one. Marking it `measured` borrows the schema read's credibility for the
   throughput claim stacked on top of it.

Honest restatement of what the author's own work supports: *the inputSchema declares `polymers`
`maxItems: 8` (listing, re-read blocked here); a 3-chain payload passed validation and was refused
at admission; no operation has completed.*

## 7. Regime in which the claim is right — and the real lever

This is not empty, and the salvage is worth more than the refutation.

**Where multiple polymers per operation is exactly correct:** when the target *is* a complex.
Homo-oligomers (upstream even collapses identical chains with `id: [A, B]`), binder–target pairs,
receptor–peptide, and — directly relevant to this repo's one surviving candidate — the
KCNQ1–KCNE1 assembly of `findings/README-no-gpu-problem.md` and
`results/2026-10-31-kcne1-binding-ddg-STOPPED.md`, whose 9VEC staging is chains C + A, G, J. There,
multiple polymers do work that **cannot** be done by separate operations at all, which is a stronger
claim than cheapness. The claim's mistake is not using `polymers`; it is believing `polymers` is a
batch axis for unrelated sequences.

**The two levers that do raise usable work per slot:**

1. `diffusion_samples` > 1 — genuine, bounded by the real cap (8 per the claim, 25 per NVIDIA's
   Boltz-2 NIM, unresolved), and it costs roughly proportional diffusion wall-clock, so it is extra
   work, not free work.
2. More operations — serial throughput or concurrency. The claim's own refusal says the slot is the
   constraint; that is where the headroom question belongs.

## 8. What would settle it

One completed operation. Submit the same monomer twice — once alone, once as chain 1 of an
8-polymer payload — and compare the single-chain coordinates and confidence. If co-folding is
harmless the two agree; if §3 is right they do not. Cost: two jobs. Until then nothing about
batching is measured, in either direction.

## 9. What this review does and does not establish

- **Establishes:** Boltz-2's multi-sequence input is a complex specification, full-text from
  upstream docs; `diffusion_samples` is samples-of-one-input, same source; upstream batching is
  per-file, not per-chain; the claim's two cited axes do not yield its stated factor of 8; the
  demonstrated chain count is 3, not 8; no operation completed; `measured` is the wrong level.
- **Does not establish:** that `maxItems` is not 8 (I could not read the schema — 403 at the
  proxy); what the real refusal code was; any Boltz-2 timing, since I ran none; that an 8-chain
  payload would fail to execute. The compute table in §4 is **derived from architecture, not
  observed**.
- **Does not establish** anything about any protein, variant or phenotype.

---

```swarm-challenge
{"claim_id": 257, "outcome": "refuted", "reason": "polymers is the chain list of one co-folded complex, not a batch axis, so eight polymers buy one prediction and not eight, superlinearly dearer than eight separate jobs; the 8 is a declared schema ceiling recorded as measured while only 3 chains were validated and zero operations ever ran.",
  "corrected_value": "1 independent prediction per operation regardless of chain count; the one honest axis is diffusion_samples (<=8 per the claim, 1-25 per NVIDIA's Boltz-2 NIM, unresolved), which yields extra samples of a single target at proportional wall-clock cost, not extra targets",
  "depends_on": ["boltz2_predict_native inputSchema declares polymers maxItems 8 (author's read; could-not-access from this session, agent proxy 403 on 89.169.99.188:443)", "boltz2_predict_native inputSchema declares diffusion_samples max 8 (author's read; unverified, and NVIDIA's Boltz-2 NIM documents 1-25)", "boltz2_predict_native wraps Boltz-2 with upstream polymers/chain semantics unchanged", "jwohlwend/boltz docs/prediction.md: multi-sequence input specifies one complex; diffusion_samples is samples per input; batching is per-file (full-text)", "Boltz-2 is AlphaFold3-class with an O(N^2) pair representation and O(N^3) triangle updates, so trunk cost is superlinear in total tokens (architecture, not measured here)", "the 3-protein batch was refused at admission and no operation completed (author's report; payload and refusal code absent from the repo at 3272d3e)", "the submission slot admits one operation at a time (author's stated reason for the refusal)"]
}
```
