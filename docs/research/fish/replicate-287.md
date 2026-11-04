# Replicate 287 — re-derivation attempt, independence compromised

## Status

Incomplete as an independent replication, and recorded here as such.

To find the inputs I had to open `challenge-257.md` on branch
`claude/challenge-257-boltz2-batching-goiema`. That file is the prior worker's
working, and it states their corrected value. I stopped reading once that was
clear, but by then I had seen it, so nothing below can count as a blind
re-derivation. The branch's commit message carries the conclusion too, so there
was no route to the inputs that avoided the answer. `agrees` is therefore `null`.

## What I checked at primary sources myself

| source | read-level | what it gave |
|---|---|---|
| `jwohlwend/boltz` `docs/prediction.md` (raw.githubusercontent.com, main) | full-text | one input file "specifies the components of the complex"; the sequences section "has one entry per unique chain or molecule"; running many inputs means passing a **directory**, where "predictions will be run on all `.yaml` and `.fasta` files inside"; `--diffusion_samples` (default 1) is "the number of diffusion samples to use for prediction", and the output folder holds `diffusion_samples` structures **of that one input**, ranked by confidence; confidence output includes `chains_ptm` and `pair_chains_iptm` (per-chain-pair interface scores) |
| `jwohlwend/boltz` `src/boltz/model/layers/triangular_mult.py` | full-text | triangle multiplication is `torch.einsum("bikd,bjkd->bijd", a, b)` (outgoing) and `torch.einsum("bkid,bkjd->bijd", a, b)` (incoming) over the token x token pair tensor |
| `jwohlwend/boltz` `src/boltz/model/layers/pairformer.py` | full-text | each `PairformerLayer` applies `TriangleMultiplicationOutgoing`/`Incoming` and `TriangleAttentionStartingNode`/`EndingNode` |
| Nebius MCP `https://89.169.99.188/mcp` | could-not-access | agent proxy returned `403` to `CONNECT` for `89.169.99.188:443` (`connect_rejected`). I could not read `boltz2_predict_native`'s inputSchema at all, so the `polymers` `maxItems: 8` and the `diffusion_samples` cap are **unverified by me** |
| this repo, working tree at `3272d3e` | full-text | no record of the boltz2 schema, the 3-protein payload, or the admission response. Scope of that negative: case-insensitive content search for `257`, `boltz2_predict_native`, `polymers`, `diffusion_samples` and `maxItems` across tracked `.md`, `.json`, `.py` and `.yaml` files outside `node_modules`; zero hits |

## The derivation, in full

Two steps, and only the second is arithmetic.

**Step 1 — what one operation returns.** From the upstream docs, full-text, quoted
above: a single input is one complex, and many inputs are many files in a
directory. My inference from those two sentences, not the author's claim: a list
of k chains submitted in one operation is a k-chain co-folded assembly, so the
count of independent single-chain predictions returned is

    1 per operation, for any k

not k. The `pair_chains_iptm` output is corroboration from the same source —
interface scores between chain pairs exist only because the chains were folded
together.

**Step 2 — cost, if one nevertheless packs k chains in.** Let L be tokens per
chain and N = kL the total. The pair tensor is N x N, so its element count is
k^2 L^2. The triangle einsums contract one index across the pair tensor, giving
N^3 = k^3 L^3 multiply-accumulates per triangle update.

    k separate 1-chain operations:  pair  k * L^2        triangle  k * L^3
    one k-chain operation:          pair  k^2 * L^2      triangle  k^3 * L^3
    ratio, at k = 8:                pair  8x more        triangle  64x more

**This is calculated from the einsum shapes I read in the source. It is not a
measurement — I ran no Boltz-2 job and hold no timing of my own.** The exponents
2 and 3 follow from the shapes, but the conclusion's sign does not depend on
them: any superlinear trunk makes one k-chain operation dearer than k 1-chain
operations, never cheaper.

**My value: 1 independent prediction per operation, independent of chain count**
(uncertainty: exact, conditional on the upstream chain semantics holding
unchanged through the Nebius wrapper — which I could not check, 403). The honest
work-per-slot axis is `diffusion_samples`, which returns that many structures of
a single input at roughly proportional wall-clock; its cap I could not read.

## Comparison with the recorded value

**CANNOT TELL.** Not because the sources are thin — on the semantics they are
full-text and unambiguous — but because I saw the prior worker's conclusion
before deriving mine. Two derivations agreeing is evidence only when the second
did not read the first. A clean replication needs an agent handed
`boltz2_predict_native`'s inputSchema and the upstream docs without the challenge
file, and, for step 2, one completed pair of jobs: the same monomer alone, and as
chain 1 of a multi-chain payload.

```swarm-replication
{"claim_id": 287, "my_value": "1 independent prediction per operation, independent of chain count (chains are co-folded, not batched); packing k=8 chains costs ~8x the pair elements and ~64x the triangle ops of 8 separate jobs, calculated from the einsum shapes, not measured", "agrees": null,
  "note": "Independence was compromised: the inputs live inside the prior worker's challenge file, which states their corrected value, so agreement here would not be evidence."}
```
