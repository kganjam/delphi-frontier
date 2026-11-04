# Replication 30 — Tyrosine spatial clustering in zebrafish actinodin 1 / actinodin 2

**Status:** independent re-derivation (computed, not observed). The derivation was done without
seeing the original agent's working. A grep of this repository for `tyrosine` / `and2` found
nothing relevant (the only hit, `findings/gemini-triage-267-problems.json`, is unrelated), so no
prior working was read.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| and1 protein, *Danio rerio* | UniProt **E7F5V5**, 570 aa, 47 Tyr (8.25 %) | `rest.uniprot.org/uniprotkb/search?query=gene:and1 AND organism_id:7955` | full-text (sequence record) |
| and2 protein, *Danio rerio* | UniProt **A9JRX1**, 508 aa, 29 Tyr (5.71 %). (A0ACM8QEN9 has an identical sequence.) | same query with `gene:and2` | full-text (sequence record) |
| Test statistic | **unknown from the source** — inferred, see below | — | could-not-access |

## Method (my inference, not the author's stated method)

The definition of the clustering statistic was not given. I tested candidate definitions and kept the one
that reproduced the and2 figures in the question. **Warning:** I picked this metric *because* it matched
the and2 numbers. That makes the and2 match a fit, not an independent confirmation. The and1 figures were
not used to choose the metric, so they are the independent check.

- Statistic: for the n Tyr positions in order, take the n−1 gaps between consecutive Tyr. The statistic is
  the fraction of those gaps that are ≤ 4 residues.
- Null: 2000 full-sequence shuffles, which keep amino-acid composition and so keep Tyr content.
  z = (obs − mean_null)/sd_null. p = (1 + #{null ≥ obs})/2001 (one-sided).
- Rejected candidates: "fraction of Tyr with another Tyr within ±k" for k = 1–5 did not give 0.393/0.211.
  Gap thresholds other than ≤4 also failed to match (table in the script output).
- Code: `docs/research/fish/replicate-30-tyr-gap.py`

## Arithmetic

- and2: 28 gaps, of which 11 are ≤ 4 → **11/28 = 0.393** (observed).
  Simulated null mean is 0.211 (seed 1). Across 5 more seeds it ranged 0.208–0.211.
  z = 2.73 (2.58–2.69 across seeds). p = 0.0105 (0.009–0.015 across seeds).
- and1: 46 gaps, of which 18 are ≤ 4 → **18/46 = 0.391** (observed).
  Simulated null mean is 0.293 (0.291–0.293 across seeds).
  z = 1.72 (1.70–1.81). p = 0.064 (0.0545–0.0665 across seeds).
  Monte-Carlo SE of p is √(0.064·0.936/2000) ≈ 0.0055.

**My value:**
- and1: observed 0.391 vs shuffled 0.293 ± 0.002, z ≈ 1.75 ± 0.05, p ≈ 0.06 ± 0.006 → not significant.
- and2: observed 0.393 vs 0.210, z ≈ 2.65, p ≈ 0.012 ± 0.003.

Interpretation (my inference): the observed clustering fraction is almost the same in the two proteins
(0.391 vs 0.393). The difference in significance comes from the null baseline. and1 has a higher Tyr
density (8.25 % vs 5.71 %), so random shuffles already give short Tyr gaps more often (0.293 vs 0.211).
That fits the claim's wording that "Tyr content alone explains" the and1 value.

## Comparison with the recorded value

The question's text gives and2 as 0.393 vs 0.211, z = 2.74, p = 0.011, and and1 as p = 0.064. I reproduce
all of these. The z of 2.73 vs 2.74 is within seed noise. The answer was removed from the claim's tail, and
I could not find a recorded value in this repository (search scope: `grep -ri tyrosine|and2` over the
working tree). So I cannot check that truncated part directly.

Verdict: **AGREE** on every stated number. There is one caveat: the metric definition was reverse-engineered
from the and2 figures, so only the and1 result counts as independent evidence.

```swarm-replication
{"claim_id": 30, "my_value": "and1: 0.391 observed vs 0.293 shuffled (z≈1.75, p≈0.06±0.006, n.s.); and2: 0.393 vs 0.210 (z≈2.65, p≈0.012)", "agrees": true,
  "note": "Reproduced from UniProt E7F5V5/A9JRX1 using the fraction of consecutive Tyr gaps ≤4 aa against 2000 composition-preserving shuffles; the metric was inferred by matching the and2 numbers, so only the and1 p=0.064 is an independent check."}
```
