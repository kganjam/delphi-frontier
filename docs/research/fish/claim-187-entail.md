# Claim 187 — entailments at the `dna` and `cell` scales

**Source claim (scale `protein`, evidence `measured`):** *stab-ddg is unavailable, measured not
relayed: a SCHEMA-VALID submit_stab_ddg request returns MODEL_MAINTENANCE with admission
not-submitted and creates no operation. So no ddG model was available and no stability prediction
was made.*

**Headline: the claim is about the availability of a software service, not about a physical
system, so it puts no physical `range`, `timescale` or `spatial` requirement on DNA or cells.**
I did not invent one to fill the preferred categories. What it does require one scale down and one
scale up is bookkeeping: if no prediction was made, then no DNA-variant-level ΔΔG value and no
cell-level inference built on one may exist anywhere in the project's record. Those two
requirements I checked against the repository, and both hold. No literature search applies to
either one, because both are about what this project's own record contains. Neither depends on
anything published.

Single reader. Nothing here was simulated, and I did not re-probe the endpoint.

---

## Sources and read-levels

| source | what it contributes | read-level |
|---|---|---|
| `results/2026-10-31-kcne1-binding-ddg-STOPPED.md` §6–§8 (commit `dd231c9`, amended `3272d3e`) | the 503 `MODEL_MAINTENANCE` record, `admission: "not-submitted"`, "No job was created", attempts 10:59–11:02 PDT; "No ΔΔG was computed"; the coverage arithmetic | full-text (read in this repo) |
| `preregistrations/2026-10-31-kcne1-binding-ddg.md` | the planned computation and its readout (ProteinGym `KCNE1_HUMAN_Muhammad_2023_expression`, N = 2,339; MaveDB `urn:mavedb:00000674-a`) | full-text (read in this repo) |
| `findings/README-no-gpu-problem.md` §"Corrections" | catalogue text for `submit_stab_ddg`: *"mutation-induced binding energy changes from a wild-type PDB"* | full-text (read in this repo); the catalogue itself was **not** re-read by me, so for the catalogue wording this is a relay |
| full git history, all branches (30 commits) | search for any ΔΔG output | full-text (searched by me) |

What I did **not** do: I did not call the Nebius MCP endpoint, so the 503 is **relayed from the
results file** in this document, not re-measured. The ProteinGym/MaveDB CSVs are not in the repo,
so I did not re-read them. Their sizes, sha256 values and N come from the results file (a relay).

---

## C1 — `dna`, conservation: variant accounting must close with zero predictions

**Requirement.** Every assay variant (each one a single-nucleotide-level missense allele of KCNE1,
mapped to a residue substitution) must fall into exactly one bucket: *predicted* or *not
predicted*. If the claim is true, the *predicted* bucket is empty. The partition must sum to the
assay total, and no file that carries a per-variant ΔΔG may exist.

**Check: satisfied (derived from the repo's records).**
- The results file's accounting closes: 2,339 assay variants = 474 at positions resolved in 9VEC +
  1,865 unresolved. Of the 474, 455 are usable and 19 sit at position 41, which carries the
  engineered K41C (wild type mismatched, so they could not be submitted). Predicted: **0**, because
  "No ΔΔG was computed" (§header) and "No job was created" (§6). 474 + 1,865 = 2,339 and
  455 + 19 = 474. I did that arithmetic on the reported numbers myself. I did not count the
  variants from the CSV.
- Negative search, with its scope: across every path ever committed on every branch (30 commits),
  only two files mention `ddg`, `stab`, `kcne1` or `9vec` in their path: the preregistration and the
  STOPPED result. A content search of the working tree for `ddg_pred`, `predicted_ddg`, `"ddg"` and
  `ddg,` found **no matches**. The scope is this repository only. A staged 9VEC PDB is mentioned
  (§6) but it is not committed, and it is an input, not an output. Outputs on the Nebius side were
  not searched, because I could not reach them.
- DNA-level caveat carried from the source: the assay was run on the **Gly38 allele
  (rs1805127)** and the structure carries canonical Ser38. That would have mattered for a
  prediction and does not matter for zero predictions. Position 38 is unmodelled in 9VEC in any case.

## C2 — `cell`, existence: no cell-scale conclusion may rest on a ΔΔG value

**Requirement.** The planned readout lives at cell scale (KCNE1 surface expression, i.e.
trafficking, in cultured cells). If no prediction was made, any statement the project makes about
trafficking must rest only on the measured cell readout or on published model scores. None may
rest on a stab-ddg value.

**Check: satisfied (derived from the repo's records).**
- The results file states the negative explicitly (§7): it *"Does not establish anything about
  whether interface binding ΔΔG predicts KCNE1 trafficking. That question is untouched."* The
  trafficking-related numbers it does report (the L51H expression of −0.056, percentile 0.0; D76N
  +1.053; the restricted-set ρ values of +0.434, +0.5877 and so on) are described there as measured
  assay values or ProteinGym's published and recomputed model scores. None of them is a ΔΔG.
- Scope: the files in this repository only. The `ledger/` README does not list claim 187, and I
  did not find the external `scopedesk/ledger/kill_ledger.json`, so I did not search it.

---

## What the claim does **not** entail at these scales, stated so the absence is not read as a skip

- **No `range` constraint.** A ΔΔG bound (kcal/mol) would arise only if a prediction had been
  made. The claim says none was.
- **No `timescale` constraint at dna/cell.** The only time in the claim is the duration of the
  service outage. That is a property of the infrastructure, not of transcription, folding or
  trafficking.
- **No `spatial` or `energetic` constraint.** Nothing physical is asserted. The GPU energy
  consumed is zero by the claim, but that sits at no biological scale.

## Problems with the claim at its own scale (outside this task, recorded because I saw them)

1. **"No *stability* prediction was made" is true, but for the wrong reason.** The repo's own
   correction (`findings/README-no-gpu-problem.md`) quotes the catalogue: `submit_stab_ddg` predicts
   *binding* ΔΔG, not folding stability. That service never makes stability predictions, so the
   clause would hold even if the call had succeeded. The claim should say "no binding-ΔΔG
   prediction".
2. **"No ddG model was available" over-generalises the measurement.** What was observed is that one
   App (`stab-ddg`, revision `stab-ddg-b19a5d7-29c874d-20261024`) refused admission on every attempt
   from 10:59 to 11:02 PDT, about 3 minutes. That does not show that no other ΔΔG model was
   reachable (the endpoint lists 69 tools, and I did not check them), or that the outage covered
   the whole decision window. The results file says a 60-second retry probe "is still running",
   and its outcome is not recorded in the repo: `unknown`.
3. **"SCHEMA-VALID" is not documented.** The results file records a successful
   `get_model_schema` fetch and a finalized artifact upload. It does **not** record validating the
   submitted request against that schema. With a 503 at admission, the server may never have
   validated the request body. The word should carry a citation or be dropped.

None of these refutes the claim from below. They narrow its wording. Each is my inference from
the repo text, not a new measurement.

```swarm-entail
{"source_claim": 187, "source_scale": "protein",
  "constraints": [
    {"target_scale": "dna", "kind": "conservation",
      "statement": "Assay variant accounting must close: every variant is either predicted or not predicted, the predicted count is zero, and no per-variant ddG output exists in the record",
      "quantity": "number of assay variants with a ddG prediction", "lo": 0, "hi": 0, "units": "variants",
      "status": "satisfied",
      "satisfied_by": "STOPPED result: 2,339 = 474 resolved + 1,865 unresolved; 474 = 455 usable + 19 K41C; 'No ddG was computed', 'No job was created'. No ddG output file in any of 30 commits on any branch",
      "satisfied_evidence": "derived",
      "note": "results/2026-10-31-kcne1-binding-ddg-STOPPED.md sections 1, 6, 7 (full-text, in repo). Arithmetic checked on the reported counts, not recounted from the CSV. Negative search scope: path names across the full git history, plus a content grep of the working tree for ddg_pred, predicted_ddg, \"ddg\" and ddg,; Nebius-side outputs not searched (not reachable). The 503 itself is relayed from the results file, not re-probed"},
    {"target_scale": "cell", "kind": "existence",
      "statement": "No cell-scale (trafficking or surface-expression) conclusion may rest on a ddG value; any such statement must rest only on the measured cellular readout or on published model scores",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "STOPPED result section 7 states the trafficking question is 'untouched'; every reported trafficking number there is a measured assay value (ProteinGym KCNE1_HUMAN_Muhammad_2023_expression, MaveDB urn:mavedb:00000674-a) or a published or recomputed language-model score, never a ddG",
      "satisfied_evidence": "derived",
      "note": "Scope: this repository only. Claim 187 is not listed in ledger/README.md; the external scopedesk/ledger/kill_ledger.json was not found or searched. The assay CSVs are not in the repo, so their contents are relayed via the results file"}
  ]}
```
