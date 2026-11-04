# Challenge 187 — "stab-ddg is unavailable, measured not relayed"

**Claim under review (author's words):** "stab-ddg is unavailable, measured not relayed: a
SCHEMA-VALID submit_stab_ddg request returns MODEL_MAINTENANCE with admission not-submitted and
creates no operation. So no ddG model was available and no stability prediction was made."
Recorded evidence level: *measured*. Value: n/a. Source: `fish-alleles/probe_stab_ddg.json`.

**Verdict: WEAKENED.** The measurement in the first sentence is consistent with every independent
record I could find. The conclusion in the second sentence claims more than that measurement shows,
in two ways. (1) "No ddG model was available" stretches one hosted App, observed in one time window,
into a claim about every ddG model. (2) "No stability prediction" puts a stability label on a tool
whose own catalogue entry calls it a *binding*-ΔΔG predictor.

---

## Sources and read-levels

| source | what it is | read-level |
|---|---|---|
| `fish-alleles/probe_stab_ddg.json` (the claim's cited evidence) | the probe record | **could-not-access**. Not in this branch, and not in any of the ~480 `origin/*` branches. I checked with `git ls-tree -r` on every remote branch, matching `probe_stab` or `alleles`. A GitHub code search for `probe_stab_ddg` in `kganjam/delphi-frontier` returned 0 hits. |
| `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6 (main lineage) | an earlier session's live probes of `submit_stab_ddg`, 2026-10-31 | full-text |
| `docs/research/fish/proteins-readme.md` §3, §5, §9 and `proteins-findings.md` §3 (branch `origin/claude/adder-cell-size-law-5baqub`, commit 699500a, 2026-11-03) | another session's probes of esm2 and stab-ddg | full-text |
| `results/resources/scientific-ai-capabilities-20261101.json` and `scientific-model-catalog-summary.json` (branch `origin/claude-organ/sims`) | Nebius tool and model catalogue snapshot | full-text (repo copy of a live listing) |
| `findings/README-no-gpu-problem.md` "Corrections" | an earlier correction about what stab-ddg computes | full-text |
| Nebius MCP endpoint `https://89.169.99.188/mcp` | live re-measurement | **could-not-access**. From this session the agent proxy refuses the tunnel (`curl: (56) CONNECT tunnel failed, response 403`), and no Nebius credential is present. I did **not** re-submit anything. |

The cited evidence file could not be read, so I could **not** check the probe itself: its
timestamp, the request body, or the exact response. Everything below rests on the repo's other
records of the same endpoint.

## 1. Arithmetic

There is no number in the claim, so there is nothing to recompute. The one countable statement is
"creates no operation". Two other records support it: they report `admission: "not-submitted"`
and say the maintenance check "creates no operation" (KCNE1 §6: "No job was created — every
attempt was refused at admission"; proteins-readme §9). **Neither of them, as far as I can see,
records an independent `get_operation` or `list_operations` check.** "No operation" is read off
the admission field, not shown by a lookup. I could not find out whether the cited probe ran a
lookup, because I could not read the file.

## 2. Proxy check: the claim swaps one quantity for another

- **Binding ΔΔG standing in for stability.** The catalogue describes `submit_stab_ddg`, quoted
  exactly, as *"Predict mutation-induced binding energy changes from a wild-type PDB. Returns
  kcal/mol and Monte Carlo sampling error, not experimental affinity."* (capabilities JSON,
  full-text). The repo already logged this correction (README-no-gpu-problem: *"`submit_stab_ddg`
  is a binding ΔΔG predictor, not folding stability"*). So "no stability prediction was made" is
  literally true but wrongly framed. Even with the App up, it would have returned a
  binding-interface ΔΔG, not a folding-stability ΔΔG. The quantity that matters for "does this
  allele destabilise the protein" is folding ΔΔG (ΔΔG_fold). This tool does not produce it.
  *(My inference, from the catalogue text. I have not run the model.)*
- **One App standing in for "a ddG model".** The probe measured one hosted App: Nebius
  `stab-ddg`, runtime revision `stab-ddg-b19a5d7-29c874d-20261024` per the catalogue snapshot.
  "No ddG model was available" is a much wider claim. Its scope would have to cover CPU-side ΔΔG
  tools that need no GPU App, such as physics- or statistics-based estimators. **I did not search
  for or test any such tool**, so I can't say they *were* available. I can only say the claim
  gives no search scope that would let it say they were *not*. The negative is unscoped.

## 3. Hidden assumptions, tested by relaxing them

- **(a) "SCHEMA-VALID" is inferred from where the maintenance check sits.** The only support I
  found is another session's note: *"Validation order is JSON schema → maintenance pause →
  manifest/semantic → media"* (proteins-readme §5). The controlled test behind that note (§1, "Both
  directions were controlled") was run on **esmfold2**, not stab-ddg. If stab-ddg's gateway checks
  the pause before the schema, a MODEL_MAINTENANCE reply says nothing about schema validity.
  Without a stab-ddg-specific control (a deliberately malformed request that gets a schema error
  instead of MODEL_MAINTENANCE), "SCHEMA-VALID" is an **inference, not a measurement**. The cited
  probe may have run such a control. I could not read it.
- **(b) Schema-valid is not the same as runnable.** Even with (a) granted, schema validity is only
  the first of four gates. The same session recorded the stab-ddg **manifest contract as "not yet
  solved"** (proteins-readme §3): stab-ddg needs `pdb_file` and `variants_file` *inside a workload
  archive*. So "the App was down" is not the only thing that stood between this request and a
  prediction.
- **(c) An input precondition the claim never mentions.** The catalogue says stab-ddg needs a
  *wild-type PDB*, and the KCNE1 run notes that `wild_type` must match the PDB residue. The fish
  alleles in this series (*kcnk5b* W169L/F241Y and *kcc4a* C583Y, per
  `S11-network-and-alleles.md` on `origin/claude/kcnk5b-longfin-alleles-3hv53s`) are on zebrafish
  proteins. The repo's own PDB70 search found no solved structure resembling the fish fin proteins
  (proteins-findings §2, a PDB70-only negative). A binding ΔΔG would also need a **complex**.
  Relaxing "the App is up" therefore does not obviously lead to a prediction. *(My inference. I
  did not check which structures the probe used.)*
- **(d) Maintenance is a moment in time.** MODEL_MAINTENANCE says, word for word, *"temporarily
  paused"*. The claim drops the time. The records I could read show it on 2026-10-31, every attempt
  10:59–11:02 PDT (KCNE1 §6), and again in the 2026-11-03/04 session (proteins-readme). The
  probe's own timestamp is **unknown** (file not readable). "Unavailable" is honest only as
  "unavailable at <time>".

## 4. Is "measured" an honest evidence level?

**Partly.** The part that was observed, a 503 MODEL_MAINTENANCE with
`admission: "not-submitted"`, is a real measurement. It also replicates across at least two
independent sessions, so "measured not relayed" holds up against the obvious objection: the
catalogue reads `availability: "available"` while runtime refuses, and the probe took the runtime
answer. Three parts of the claim are *not* measured, and the claim does not say so:
"SCHEMA-VALID" (an inference from validation order, §3a), "creates no operation" (read off the
admission field, §1), and "no ddG model was available" (a generalisation, §2). One evidence label
covering all of these is a labelling defect, even though the core observation is right.

## 5. Regimes and counter-examples the author missed

- **Time:** the App may have come back later. No time window is stated.
- **Other ddG routes:** unscoped (§2). I did not test them, so this is a gap in the claim's scope,
  not a counter-example I can show.
- **Folding stability compared with binding:** for a gain-of-function K2P channel allele like
  *kcnk5b* W169L, what the question needs is probably neither a binding ΔΔG nor a folding ΔΔG. It
  is a conductance or gating effect. *(My inference. Perathoner et al. 2014 report a "~two-fold
  increase in K⁺ conductance" per S11, read at full-text by that session, not by me.)* So the
  missing number may not have answered the question even if it had been produced.

## Corrected statement

> On <timestamp unknown — probe file not accessible>, a `submit_stab_ddg` request to the Nebius
> Scientific AI App returned HTTP 503 `MODEL_MAINTENANCE`, `admission: "not-submitted"`
> (observed; consistent with independent observations on 2026-10-31 and 2026-11-03). The request's
> JSON-schema validity is inferred from the documented validation order, which was controlled on
> esmfold2, not stab-ddg. Its manifest/semantic validity was not tested. No binding-ΔΔG prediction
> was obtained from this App. No other ΔΔG tool was searched for or tried. stab-ddg predicts
> binding, not folding-stability, ΔΔG.

```swarm-challenge
{"claim_id": 187, "outcome": "weakened", "reason": "The observed MODEL_MAINTENANCE/not-submitted refusal is consistent with two independent records. But 'no ddG model was available' generalises one hosted App at one unstated time to all ddG models with no search scope, 'no stability prediction' mislabels a binding-ΔΔG tool as stability, and 'SCHEMA-VALID' and 'no operation' are inferred, not measured, while the cited probe file could not be accessed.", "corrected_value": null, "depends_on": ["fish-alleles/probe_stab_ddg.json (could-not-access; verdict rests on its absence)", "results/2026-10-31-kcne1-binding-ddg-STOPPED.md §6 (MODEL_MAINTENANCE, admission not-submitted, 2026-10-31 10:59-11:02 PDT)", "origin/claude/adder-cell-size-law-5baqub:docs/research/fish/proteins-readme.md §3/§5/§9 (validation order controlled on esmfold2; stab-ddg manifest contract not solved; catalogue vs runtime disagreement)", "origin/claude-organ/sims:results/resources/scientific-ai-capabilities-20261101.json (submit_stab_ddg description: binding energy changes from a wild-type PDB)", "findings/README-no-gpu-problem.md (stab-ddg is binding, not folding, ddG)"]}
```
