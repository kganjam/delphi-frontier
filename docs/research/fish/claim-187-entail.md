# Claim 187 — entailments at `dna` and `cell`

**Source claim (scale `protein`, evidence `measured`):** *stab-ddg is unavailable, measured not
relayed: a SCHEMA-VALID `submit_stab_ddg` request returns `MODEL_MAINTENANCE` with admission
`not-submitted` and creates no operation. So no ddG model was available and no stability prediction
was made.*

Single reader. Nothing below is simulated. No request was sent to the Nebius endpoint in this pass
(a schema-valid submit would create a GPU job if the App has come back; that is not mine to start).

## 0. What kind of claim this is, before entailing anything

Claim 187 is a claim about **a software service's admission state during a time window**, not about
a protein. Its truth entails **no physical requirement** at the `dna` or `cell` scale: no length,
rate, energy or concentration has to take any value for an HTTP 503 to have been returned. I am not
going to dress bookkeeping up as biophysics. What the claim *does* entail at the neighbouring scales
is **evidential**: if no prediction was made, then nothing at the variant (`dna`) or trafficking
(`cell`) scale may rest on one, and the variant accounting must balance with zero predictions in it.
Those are the constraints below. The `range` / `timescale` / `spatial` kinds the brief prefers have
no honest instance here, and I did not invent one.

Sources and read-levels:

| source | read-level |
|---|---|
| `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` (commit `dd231c9`) — the primary record of the 503 | full-text |
| `findings/README-no-gpu-problem.md` — catalogue description of `submit_stab_ddg` | full-text |
| `preregistrations/2026-10-31-kcne1-binding-ddg.md` | full-text (searched) |
| Whole repository at `3272d3e`, grepped for `stab_ddg`, `stab-ddg`, `ΔΔG`, `ddg`, `not-submitted`, `MODEL_MAINTENANCE` | full-text (grep) |
| Nebius MCP server operation list / job history | **could-not-access** — not queried (see C2) |
| Raw HTTP request/response bodies of the 503 attempts | **could-not-access** — not committed anywhere in the repo |

## 1. Problems with the claim's own wording (protein scale; reported, not entailed)

These are not adjacent-scale constraints, but they bound what the constraints can mean.

1. **"stability prediction" is the wrong noun.** The live catalogue description, as quoted in
   `findings/README-no-gpu-problem.md` (full-text), says `submit_stab_ddg` predicts *"mutation-induced
   binding energy changes from a wild-type PDB"* — binding ΔΔG, not folding stability. So the
   last clause is true but vacuous: this App would never have produced a stability prediction.
   Correct wording: *no binding-ΔΔG prediction was made.*
2. **"no ddG model was available" over-reaches.** What was measured is that **one** App
   (`stab-ddg`, revision `stab-ddg-b19a5d7-29c874d-20261024`) refused admission. No other ΔΔG
   predictor was tried, so their availability is *not looked at*, not *looked at and absent*.
   Correct scope: *the `stab-ddg` App was unavailable.*
3. **"unavailable" has a window.** The record reports refusals *"on every attempt from 10:59 to
   11:02 PDT"* on 2026-10-31 (≈180 s) and a 60 s retry probe *"still running"* with no reported end.
   The measured statement is unavailability over that ≈3-minute window only.
4. **"SCHEMA-VALID" is asserted, not shown.** The record shows `get_model_schema` returned the schema
   and the workload archive finalized; it does not show the submit body validated against that
   schema, and it does not say whether admission checks the schema before or after the maintenance
   gate. If maintenance is checked first, a 503 is uninformative about validity. Status: `unknown`.
5. **"creates no operation" is inferred from `admission: "not-submitted"`,** not from a listing of
   operations on the server (see C2).

## 2. Constraints and checks

### C1 — `dna`, existence (negative): no variant-level ΔΔG annotation may exist

*If no prediction was made, then no allele/variant-level ΔΔG value attributable to `stab-ddg`
exists in the project record for any of the 2,339 assay variants.*

**Status: satisfied, within the scope of the repository.** Grep of the full tree at `3272d3e` for
`stab_ddg|stab-ddg|ΔΔG|ddg` hits only five prose files (the result, the preregistration, the
preregistration README, the no-GPU finding, and an unrelated Addgene string in a JSON triage file).
No CSV, JSON or table of per-variant ΔΔG values exists. The result itself states *"No ΔΔG was
computed, so there is no ρ to report."* Evidence: measured (direct inspection of the record).
Scope of the negative: this repository only; not the Nebius side, not any agent's untracked scratch.

### C2 — `dna`, existence (negative): no server-side operation may exist for those variants

*If the request "creates no operation", the service's own operation/job list must contain no
`stab-ddg` operation for this workload.*

**Status: open.** Nobody has looked. The record's "No job was created" is an inference from the
admission field of the refusal, not a read of the server's operation list. I did not query the
endpoint. This is "nobody has looked", not "looked and found nothing".

### C3 — `cell`, existence (negative): no trafficking/surface-expression conclusion may rest on a ΔΔG

*If no prediction was made, no cell-scale claim (KCNE1 surface delivery / trafficking) in the record
may cite a `stab-ddg` output as its evidence.*

**Status: satisfied.** The result's §7 states it *"Does not establish … anything about whether
interface binding ΔΔG predicts KCNE1 trafficking. That question is untouched."* Every cell-scale
number in the result (surface-expression scores of L51H −0.056 and D76N +1.053; the Mann-Whitney
p = 4.95 × 10⁻¹² resolved-vs-unresolved comparison; the ProteinGym ρ values) is computed from the
ProteinGym assay CSV and zero-shot score file, none from a ΔΔG. Evidence: measured (record
inspection). Scope: the repository at `3272d3e`.

### C4 — `dna`, conservation: the variant ledger must balance with zero predictions in it

*Every assay variant must be accounted for as either predicted or not-predicted, with the predicted
count equal to zero.*

**Status: satisfied (derived, arithmetic on the record's measured counts).** From the result:
2,339 variants = 455 usable + 19 at position 41 (unusable: structure carries engineered K41C) +
1,865 at positions unresolved in 9VEC (2,339 − 474). 455 + 19 + 1,865 = 2,339. Predicted = 0,
because the 455 usable variants were the submission set and every submission was refused. The
balance closes. Note the claim is *not* the reason they are unpredicted for the 1,884 non-usable
variants — those were unscorable on 9VEC regardless of the App's state; the 503 accounts for zero
predictions only on the 455.

## 3. Verdict

No constraint is `unsatisfiable`: nothing measured contradicts the claim. Two cell/dna entailments
are satisfied in repository scope, one balance closes, and the server-side "no operation" half of
the claim is **open** because it was inferred, not checked. The larger finding is §1: the claim
should be narrowed to *"the `stab-ddg` App refused admission (HTTP 503 `MODEL_MAINTENANCE`,
`not-submitted`) on every attempt 10:59–11:02 PDT 2026-10-31; no binding-ΔΔG prediction was made"* —
dropping "no ddG model was available", "stability", and "SCHEMA-VALID" until the request body's
validity is shown.

```swarm-entail
{"source_claim": 187, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "existence",
      "statement": "No variant-level ddG annotation attributable to the unavailable predictor may exist in the record for any assay variant",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Repository audit at 3272d3e: grep for stab_ddg|stab-ddg|ΔΔG|ddg finds only prose; no per-variant ddG table exists; result states 'No ΔΔG was computed'",
      "satisfied_evidence": "measured",
      "note": "results/2026-10-31-kcne1-binding-ddg-STOPPED.md (full-text). Negative scope: this repository only; not the Nebius server, not untracked agent scratch."},
    {"target_scale": "dna", "kind": "existence",
      "statement": "The service's own operation/job list must contain no operation for the refused workload",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "open",
      "satisfied_by": "Not checked. 'No job was created' in the record is inferred from admission: not-submitted, not from a listing of server operations; I did not query the endpoint",
      "satisfied_evidence": "unknown",
      "note": "Nobody has looked (not 'looked and found nothing'). Nebius operation list: could-not-access in this pass."},
    {"target_scale": "cell", "kind": "existence",
      "statement": "No cell-scale (trafficking / surface-expression) conclusion in the record may use a ddG prediction as evidence",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Result §7 states the ddG-predicts-trafficking question is 'untouched'; all cell-scale numbers (L51H -0.056, D76N +1.053, MWU p=4.95e-12, ProteinGym rho) come from ProteinGym CSVs, none from a ddG",
      "satisfied_evidence": "measured",
      "note": "results/2026-10-31-kcne1-binding-ddg-STOPPED.md (full-text). Scope: repository at 3272d3e."},
    {"target_scale": "dna", "kind": "conservation",
      "statement": "Assay variants must balance as predicted + not-predicted = total, with predicted = 0",
      "quantity": "assay variants accounted", "lo": 2339, "hi": 2339, "units": "variants",
      "status": "satisfied",
      "satisfied_by": "455 usable + 19 at K41C position + 1865 unresolved in 9VEC = 2339; predicted = 0 (all submissions refused)",
      "satisfied_evidence": "derived",
      "note": "Arithmetic on measured counts in the STOPPED result (full-text). The 503 explains zero predictions only for the 455 usable variants; the other 1884 were unscorable on 9VEC regardless. Claim wording also needs narrowing: stab-ddg is a binding-ddG App per catalogue (findings/README-no-gpu-problem.md, full-text), only one App was tested, unavailability measured only 10:59-11:02 PDT 2026-10-31, and schema validity of the submit body is not shown in the record (unknown)."}
  ]}
```
