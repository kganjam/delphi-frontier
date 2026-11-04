# Challenge 16 — "the MSA raised pLDDT at both kcnk5b selectivity filters"

**Claim under review (verbatim):** "An MSA raised pLDDT at both functional sites from 40.1 to 80.2
(TIGYG) and 41.4 to 82.6 (TVGFG); the single-sequence model left both unmodelled."
Recorded evidence level: `simulated`, value 80.2 pLDDT. Source: Nebius OpenFold2 vs Boltz2+PDB70 MSA.

**Verdict: WEAKENED.** The numbers hold (one is off by 0.07). Two parts of the claim do not hold:
the claim that *the MSA* caused the rise, and the word "unmodelled".

Where the claim came from: commit `ba1dd261` and `docs/research/fish/proteins-findings.md` §1 on
`origin/swarm-architecture` (read-level: full-text). Structure files: `results/fish-proteins/structures/
kcnk5b_boltz2.cif` and `kcnk5b_esmfold2.cif` on that branch. The OpenFold2 model is
`results/bioservices/claude-20261101/openfold2/kcnk5b_Q6PFU3_rank1.pdb` on
`origin/claude/bioservices-20261101` (sha256 `d595b671…ddaa`, which matches the `pdb_sha256` in its
receipt). My scripts are in `scripts/challenge16/`.

---

## 1. Arithmetic, redone independently

**Method:** I took CA-atom B-factors (pLDDT) over each five-residue motif. For the CIFs I read the
column order from each file's `_atom_site.` header. The ESMFold2 CIF puts B_iso at field 13, not in
the standard position. I found the motifs by scanning Q6PFU3 for `[TS].[GAS][YFL]G`. That returned
exactly two hits, TIGYG at 98–102 and TVGFG at 203–207, which confirms the positions.

All values below are **computed** from **predicted** structures. None of them is an observation.

| model | TIGYG 98–102 (CA) | TVGFG 203–207 (CA) | mean (all res) | >70 | <50 |
|---|---|---|---|---|---|
| OpenFold2, single-seq dummy MSA | **40.08** | **41.33** | 56.10 | 14.7% | 34.2% |
| Boltz2 + PDB70 A3M (72 rows) | **80.22** | **82.55** | 62.03 | 38.8% | 33.0% |
| ESMFold2, no MSA | 96.55 | 96.30 | 83.63 | 90.0% | 0.9% |

- 40.1, 80.2 and 82.6 reproduce.
- **41.4 does not reproduce exactly.** My value is 41.33. Per-residue: 42.41, 31.76, 41.55, 40.17,
  50.75, which sum to 206.64, and 206.64 / 5 = 41.33. The all-atom mean is 40.31, so all-atom
  averaging does not explain 41.4 either.
  - The author cites OpenFold2 operation `op-deac3f5087a199b3`. Its output is not in the repo. I used
    `op-83bc718db408cd89`, which has the same sequence and identical global statistics (56.10 /
    14.7% / 34.2%).
  - So either the two runs differ slightly at 203–207, or 41.4 is a transcription slip. One
    candidate for the slip is the Boltz2 mean over residues 261–448, which I recomputed as 41.39 and
    which appears in the same document. That is my inference, not something I verified.
  - The difference is immaterial to the claim.

## 2. Proxy: pLDDT stands in for accuracy. I checked accuracy against an experimental ortholog

pLDDT is each model's confidence in its own output. What matters is whether the filter geometry is
right. No experimental kcnk5b structure exists that I could find. I did not search systematically;
I relied on the author's statement and RCSB. So I used **6WLV**, mouse TASK-2 (Kcnk5), downloaded
from files.rcsb.org (sha256 `f16b3d3b…ec68`, read-level: full-text coordinate file).

- Chain A numbering lines up with kcnk5b at both filters: TIGYG at 98, and TIGFG at 203.
- In 21-residue windows around each filter, sequence identity is 0.90 at P1 and 0.67 at P2.
- Method: ungapped CA correspondence, then Kabsch superposition. Computed, not measured.

| model | P1 window (21 CA) | P1 filter (5 CA) | P2 window | P2 filter | both filters jointly (10 CA) |
|---|---|---|---|---|---|
| OpenFold2 single-seq | 4.96 Å | 2.66 Å | 4.83 Å | 1.59 Å | **10.98 Å** |
| Boltz2 + MSA | 0.71 Å | 0.15 Å | 0.48 Å | 0.09 Å | **0.35 Å** |
| ESMFold2, no MSA | 0.65 Å | 0.24 Å | 0.40 Å | 0.12 Å | **0.28 Å** |

**This supports the confidence values.** The pLDDT ranking matches the accuracy ranking against the
ortholog:

- OpenFold2's two pore loops are each about 5 Å off, and they sit about 11 Å from their correct
  arrangement relative to each other.
- Boltz2 and ESMFold2 reproduce the TASK-2 filters to sub-ångström precision.

**Caveat on that comparison:** 6WLV/6WM0 are rows in the Boltz2 MSA (`kcnk5b-HITS.md`). They are also
probably in the training sets of all three models. 6WLV was released in 2020. I did not verify any
model's training cutoff. So this is agreement with a structure the models may have seen. It is not a
blind test.

## 3. Hidden assumption: that the MSA, and not the model, made the difference

This is where the claim breaks. The comparison changes **two variables at once**: the model
(OpenFold2 → Boltz2) and the input (dummy MSA → 72-row PDB70 A3M).

- **Relaxing the assumption:** a model with no MSA at all, ESMFold2 (run by the same author, commit
  `699500a7`), scores 96.5 and 96.3 at the filters. That is higher than Boltz2 with the MSA, and it
  is at least as accurate (table in §2). An MSA was therefore not necessary to get confident, correct
  filters.
- What the data does show: *OpenFold2 run without an MSA* fails at these sites. The author's own
  results file says the same: OpenFold2's low numbers are "a property of that lane, not a finding
  about the proteins" (`proteins-results.md`, read-level: full-text).
- The controls that would isolate the MSA effect were not run:
  - Boltz2 with a single-sequence (empty) A3M, or
  - OpenFold2 given the same 72-row A3M.
- The evidence is consistent with the MSA helping Boltz2 at the filters. My reason: depth over
  residues 1–250 is 21.4 by the author's count, against 0.5 over 261–448, and Boltz2's pLDDT drops
  where the depth drops. That is my inference, from a correlation, not a controlled test.
- "An MSA raised pLDDT", stated as a cause, has no controlled support.

## 4. Wording: "left both unmodelled"

OpenFold2 placed coordinates for all 448 residues, including both motifs. The sites were **modelled
with low confidence and modelled wrongly** (about 5 Å window RMSD to the ortholog). They were not
unmodelled. "Mis-modelled" is accurate, and it is actually the stronger statement.

## 5. Is the evidence level honest?

- The label `simulated` is loose. Nothing was simulated in the physical sense.
- The value 80.2 is a **predicted-structure confidence score**, read and averaged from model output.
  "Predicted (computed)" is the right label.
- The source document was candid about this ("These are PREDICTIONS"). The ledger label is the only
  imprecise part.
- No number was presented as measured.

## 6. Counter-examples or missed regimes

- The author's own ESMFold2 result (above) is the counter-example to the causal reading.
- Single-sequence failure of AlphaFold2-family models is generally known behaviour. I did not
  retrieve a specific citation for it here, so I state it without one. On that view, a low
  single-sequence OpenFold2 score is the expected baseline, not a discovery about kcnk5b.
- I found no regime in which the numerical result itself fails.
- **Scope of my searches:**
  - Every remote branch of this repo, for the motif strings, plus the commit log for
    pLDDT/MSA/TIGYG.
  - RCSB, for 6WLV only.
  - No literature search.

## Corrected statement

> Boltz2 given a 72-row PDB70 MSA scored 80.2 (TIGYG) and 82.6 (TVGFG) at the selectivity filters.
> Single-sequence OpenFold2 scored 40.1 and 41.3 there, and placed both pore loops about 5 Å from the
> mouse TASK-2 structure 6WLV. MSA-free ESMFold2 scored 96.5 and 96.3, and was as close to 6WLV as
> Boltz2. So the gain reflects the OpenFold2-without-MSA lane failing, and an MSA was not required.
> All values are model predictions and computed comparisons, not observations.

```swarm-challenge
{"claim_id": 16, "outcome": "weakened", "reason": "The numbers reproduce (TVGFG single-sequence is 41.33, not 41.4), but the comparison changes both model and MSA at once, the author's own MSA-free ESMFold2 scores 96.5/96.3 and matches TASK-2 6WLV as closely, and OpenFold2 mis-modelled the sites (~5 Å off) rather than leaving them unmodelled.",
  "corrected_value": "80.2 pLDDT (Boltz2+MSA, TIGYG); single-seq OpenFold2 TVGFG 41.3 pLDDT; MSA-free ESMFold2 96.5/96.3 pLDDT"}
```
