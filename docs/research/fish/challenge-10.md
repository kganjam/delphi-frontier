# Challenge 10: OpenFold2 single-sequence on kcnk5b, and "the MSA doubles pTM"

**Claim under review (not mine):** "Single-sequence OpenFold2 on kcnk5b gives mean pLDDT 56.1,
pTM 0.258; the MSA roughly doubles pTM, which is the expected effect of evidence rather than of a
better model."
Recorded evidence level: `simulated`. Value: 0.258 pTM. Source: Nebius workbench
`infer_openfold2_native`.

**Verdict: WEAKENED.** The OpenFold2 numbers hold up. The causal half of the claim does not. The
"doubling" compares two different models (OpenFold2 with no MSA against Boltz2 with an MSA), so
the record cannot separate the effect of the MSA from the effect of the model. The project's own
third run argues against the claim's explanation: ESMFold2, which uses no MSA at all, beats
Boltz2+MSA both on pTM and on agreement with an experimental TASK-2 structure.

---

## Sources and read-levels

| source | what it is | read-level |
|---|---|---|
| commit `ba1dd261` + `docs/research/fish/proteins-{findings,results,readme}.md` on `origin/swarm-architecture` | author's write-up, operation IDs | full-text |
| `results/fish-proteins/structures/kcnk5b_boltz2.cif`, `kcnk5b_esmfold2.cif`, `kcnk5b-confidence.json` (same branch) | raw model outputs | full-text |
| `results/bioservices/claude-20261101/openfold2/kcnk5b_Q6PFU3_{rank1.pdb,receipt.json}` on `origin/claude/bioservices-20261101` | a **separate** OpenFold2 run on the same sequence (op-83bc718db408cd89, 2026-11-01) | full-text |
| RCSB 6WLV coordinates (`files.rcsb.org/download/6WLV.pdb`, fetched 2026-11-04) | cryo-EM, mouse TASK2 (Kcnk5, UniProt Q9JK62), pH 6.5, released 2020-07-15 | full-text |
| OpenFold2 raw output for op-deac3f5087a199b3 (the run the claim cites) | — | **could-not-access**: not committed on any branch (I searched every remote branch for `kcnk5b`/`of2` paths) |

---

## 1. Arithmetic, redone independently

**Boltz2 and ESMFold2: reproduced from the committed CIFs.** I parsed CA B-factors myself
(`challenge-10/plddt_from_cif.py`):

| | mean pLDDT | % > 70 | TIGYG 98–102 | TVGFG 203–207 | res 1–250 | res 261–448 |
|---|---|---|---|---|---|---|
| Boltz2 + PDB70 MSA | 62.0 | 38.8% | 80.2 | 82.6 | 77.5 | 41.4 |
| ESMFold2 (no MSA) | 83.6 | 90.0% | 96.5 | 96.3 | 89.2 | 76.4 |

All of these match the author's tables exactly. ESMFold2 pTM 0.6067 also appears in the committed
`kcnk5b-confidence.json`.

**OpenFold2 mean pLDDT 56.1: reproduced, but from a different run.** The run cited in the claim
(op-deac3f5087a199b3) has no committed output. A separate `infer_openfold2_native` run on the same
448-aa sequence (op-83bc718db408cd89; PDB REMARK `OpenFold2 model_3_ptm; no external MSA or
template`) gives:

- mean CA pLDDT 56.10 (receipt: 56.099)
- 66/448 = 14.7% of residues > 70
- TIGYG 40.1, TVGFG 41.3

The author has 41.4 for TVGFG, a 0.1 gap that I cannot trace without their file. The two runs
agree to the reported precision on everything else, which suggests (my inference) that the native
lane is deterministic for this input.

**OpenFold2 pTM 0.258: not reproduced and not verifiable from the repository.** The committed
OpenFold2 receipt has `"ptm": null`. That harness did not capture the `ptm_score` key, even though
the result listed one. The only place 0.258 appears is the author's prose and tables. I am not
calling it wrong, only unverified. Its provenance is weaker than that of every other number in
the table.

**Ratio.** 0.479 / 0.258 = 1.857, an increase of 0.221. "Roughly doubles" is a fair description
of 1.86×. Mean pLDDT moved far less (56.1 → 62.0, ×1.105), so the "doubling" applies to pTM only.

## 2. Proxy check: pTM is self-confidence, not accuracy

pTM and pLDDT are each model's estimate of its own error. The question that matters is whether the
MSA brought the model closer to the real structure. That is testable here because an
experimental ortholog exists: 6WLV is mouse TASK2 (gene Kcnk5), and it is already a row in the
author's MSA. I ran TM-align (`tmtools`, `challenge-10/tm_vs_6wlv.py`) of each kcnk5b model
against 6WLV chain A (256 resolved CA). The ESMFold2 alignment covers 253 residues at **60.9%
sequence identity**.

| model | MSA | pTM (self-reported) | **TM-score vs 6WLV-A** (norm. by 6WLV-A) | RMSD (Å) |
|---|---|---|---|---|
| OpenFold2 single-seq (op-83bc…) | none | 0.258 (unverified) | **0.279** | 6.11 |
| Boltz2 | PDB70, 72 rows | 0.479 | **0.643** | 3.73 |
| ESMFold2 | none | 0.607 | **0.898** | 2.19 |

These TM-scores are *calculated* by me from predicted coordinates and an experimental homolog
structure. They are not measurements of kcnk5b itself. Caveats:

- 6WLV is mouse, at about 61% identity. It is a stand-in for the zebrafish structure.
- 6WLV was released in 2020, so Boltz2's and ESMFold2's training data may include it. Some of the
  agreement could be memorisation rather than prediction.
- It is a monomer from a dimeric channel.

With those caveats, the accuracy ranking matches the confidence ranking. The OpenFold2
single-sequence model is close to unrelated to the fold (TM < 0.3). The author's qualitative
reading, that the single-sequence model failed, therefore **survives the proxy check**.

## 3. The hidden assumption: same model, different evidence

The phrase "the effect of evidence rather than of a better model" assumes a controlled
comparison. The comparison is not controlled. The 0.258 → 0.479 change switches **two** variables
at once:

1. the model: OpenFold2 (AF2-style Evoformer, `model_3_ptm` weights) → Boltz2 (a different
   architecture with different training data and a different pTM head);
2. the evidence: dummy MSA of depth 1 → PDB70 A3M of depth 72.

pTM from two different heads is not even on a shared calibration. **Relaxing the assumption:**
does a better model *without* more evidence reach or exceed the MSA run? The project already
holds that experiment. ESMFold2, with no MSA, gets pTM 0.607 against Boltz2+MSA's 0.479, and
TM-score 0.898 against 0.643. Measured from the 0.258 baseline:

- the "better model, no evidence" change: +0.349 pTM (×2.35)
- the "MSA (+ model change)" change: +0.221 pTM (×1.86)

On this protein, therefore, a model change alone produced a larger effect than the claimed
"evidence" effect.

This does not show that the MSA did nothing. The author's per-region evidence is real and I
reproduced it: Boltz2 is confident at residues 1–250, where MSA depth averages 21.4, and collapses
at 261–448, where depth averages 0.5. That pattern points to the MSA as a driver *within Boltz2*.
What the record cannot support is the size of the OpenFold2→Boltz2 gap being attributed to
evidence, or the "rather than a better model" clause.

The controlled runs that would settle it were **not done**, so their results are `unknown`:

- (a) Boltz2 on kcnk5b with an empty or single-sequence MSA;
- (b) OpenFold with the same 72-row A3M. `infer_openfold2_native` takes no A3M per the author's
  readme, but `infer_openfold3_native` accepts a supplied A3M.

## 4. Evidence level

`simulated` is acceptable in the sense that this is a model output and not an observation, and
the author's write-up states plainly that these are predictions. Two problems remain:

- **pTM 0.258 is "reported", not "recorded".** No committed artifact contains it; the one
  committed OpenFold2 receipt has `ptm: null`. It should be labelled as transcribed from an
  uncommitted run.
- The source is given as `infer_openfold2_native`, but the "doubling" half of the claim depends
  equally on `boltz2_predict_native`. The claim's single source label hides that it is a
  cross-model comparison.

## 5. Regimes and counter-examples

- **Same-record counter-example:** ESMFold2 (no MSA) > Boltz2 (MSA) on this exact protein, by
  both self-confidence and agreement with an experimental homolog (§2–3).
- **Regime where the claim would hold:** the claim's mechanism, that MSA depth raises AF2-family
  confidence, is the well-known AF2/OpenFold behaviour. Accuracy degrades sharply at low MSA
  depth, which is consistent with what the author saw. I am citing this from background knowledge
  of the AlphaFold2 paper (Jumper et al., *Nature* 2021); for this review the read-level is
  **search-summary/recall, not re-read**. The mechanism is plausible. Only its attribution in
  this comparison is untested.
- **Regime where MSA cannot help:** residues 326–448 have MSA depth 0 (author's count). There,
  Boltz2+MSA (41.4 mean pLDDT on 261–448) is *no better* than single-sequence models. A global
  pTM averages over this region, so "the MSA doubles pTM" describes the N-terminal core and not
  the whole chain.

Scope of my negative search: every remote branch of `kganjam/delphi-frontier` (191 refs), path
names matching `kcnk5b` or `of2`, plus `git log -S"of2-kcnk5b"`. No OpenFold2 output for
op-deac3f5087a199b3 was found. I did not query the Nebius workbench directly.

## Reproduction

```
python3 -I docs/research/fish/challenge-10/plddt_from_cif.py     # run in a dir holding boltz2.cif, esmfold2.cif
python3 -I docs/research/fish/challenge-10/tm_vs_6wlv.py 6WLV.pdb  # also needs of2_bios.pdb; pip install tmtools
```
Inputs come from `origin/swarm-architecture:results/fish-proteins/structures/` and
`origin/claude/bioservices-20261101:results/bioservices/claude-20261101/openfold2/kcnk5b_Q6PFU3_rank1.pdb`.

```swarm-challenge
{"claim_id": 10, "outcome": "weakened", "reason": "OpenFold2 mean pLDDT 56.1 reproduces from an independent run (pTM 0.258 is uncommitted and unverified), but the 0.258->0.479 'doubling' compares OpenFold2-no-MSA with Boltz2+MSA and so confounds model with evidence, and the project's own ESMFold2 run with no MSA beats Boltz2+MSA on pTM (0.607 vs 0.479) and on TM-score against experimental TASK2 6WLV (0.898 vs 0.643), contradicting 'evidence rather than a better model'.", "corrected_value": "OpenFold2 single-seq: mean pLDDT 56.1, pTM 0.258 (unverified); MSA-attributable share of the +0.221 pTM gain: unknown (confounded with model change)"}
```
