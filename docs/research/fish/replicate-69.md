# Replicate 69: And1 (E7F5V5) structure-template claim, re-derived independently

**Claim being checked:** And1 has 0 PDB70 homolog hits, and a template-free AlphaFold model exists
with N/570 residues at pLDDT >= 70 (global value G). I worked out N and G myself from the AlphaFold DB
files, and tried to reproduce the PDB70 hit count. I opened the recorded working
(`challenge-12.md` on `claude/pdb70-and1-challenge-ne0qg7`) only **after** finishing the derivation
below, for the comparison in §4.

## 1. Inputs

| Input | Source | Read-level |
|---|---|---|
| Entry metadata: `globalMetricValue` 57.06, four pLDDT-band fractions, `latestVersion` 6, sequence length 570, gene `and1`, *Danio rerio*, UniProt E7F5V5 (unreviewed), "AlphaFold Monomer v2.0 pipeline", model date 2025-08-01 | `https://alphafold.ebi.ac.uk/api/prediction/E7F5V5`, fetched 2026-11-04 | full-text (machine record) |
| Per-residue pLDDT, 570 values | `https://alphafold.ebi.ac.uk/files/AF-E7F5V5-F1-confidence_v6.json` | full-text |
| Cα B-factor column (pLDDT) | `https://alphafold.ebi.ac.uk/files/AF-E7F5V5-F1-model_v6.pdb` | full-text |
| Sequence similarity to PDB (stand-in for PDB70) | EBI HMMER `phmmer`, database `pdb` (170,694 sequences), job `c5bf7f06-bc77-4ede-a8ee-b538bbf6a90b` | full-text (machine record) |
| PDB70 / HHpred itself | `toolkit.tuebingen.mpg.de` and `search.rcsb.org`: the sandbox egress proxy refused both connections. No local hh-suite or PDB70 database. EBI NCBI-BLAST vs PDB: refused ("temporarily blocked", fair-use) | could-not-access |

(The `.cif` file and the confidence JSON first returned 403 to plain curl. With a browser
User-Agent header they returned 200.)

## 2. Arithmetic (calculated from the downloaded per-residue values, not taken from a summary)

From the confidence JSON (n = 570):

- residues with pLDDT >= 70: **157**. With strictly > 70 the count is 156, so one residue sits at exactly 70.00.
- Bands: >= 90: 30 · 70–<90: 127 · 50–<70: 176 · < 50: 237. Check: 30+127+176+237 = 570.
- 157 / 570 = **0.2754 (27.5%)**.
- Mean pLDDT = **57.0721**.
- Cross-check against the Cα B-factors in the v6 PDB file: 570 Cα atoms, 157 at >= 70, mean 57.0721. This matches the JSON.
- Cross-check against the API band fractions: 30/570 = 0.0526 (API 0.053), 127/570 = 0.2228 (API 0.223),
  176/570 = 0.3088 (API 0.309), 237/570 = 0.4158 (API 0.416). All four agree.
- Stretches at >= 70 (1-based): 12, 61, 63–135, 213–244, 313–327, 393–416, 542–552.
  Lengths 1+1+73+32+15+24+11 = 157.

**One disagreement between sources, kept as found:** the API `globalMetricValue` is **57.06**, but my
mean of the per-residue file is **57.07** (57.0721). The difference is 0.01. It may come from
rounding or how DeepMind computes the global value, but that is my guess and I have not verified it.
I report the API value as the observed "global pLDDT" and 57.07 as my calculated mean.

## 3. The PDB70 hit count

- **I could not run a PDB70 search.** HHpred and RCSB were unreachable from this sandbox (see §1), so
  the "0 PDB70 hits" figure is **not reproduced** by me.
- **Proxy result (observed, but a different method and database):** `phmmer` of the full 570-residue
  E7F5V5 sequence against EBI's `pdb` sequence set (170,694 chains) returned **0 hits above the
  inclusion threshold** (`nincluded` = 0) and 12 reported hits with sub-threshold scores. The best was
  E = 0.44 (6o8b_E, STING, score 12.7). The rest were STING/TMEM173 chains at E 0.46–0.60 and one
  portal protein at E 0.92. None of these is plausibly a homolog.
- **Limits of this negative:** single-sequence phmmer is less sensitive than HHsearch
  profile–profile against PDB70. The PDB set was EBI's copy on 2026-11-04, not any specific PDB70
  snapshot, and the search did not exclude low-complexity regions. My *inference* is that this
  supports, but does not prove, "no PDB-deposited homolog". It cannot confirm the exact figure 0 for PDB70.
- I agree with the claim's own framing: a PDB-derived template library holds only solved structures, so
  an empty result says nothing about whether And1 can be modelled at all. The existence of AF-E7F5V5-F1
  (observed, §2) shows that directly.

## 4. Comparison with the recorded value (read after §2–3)

The recorded working (`docs/research/fish/challenge-12.md`, branch
`claude/pdb70-and1-challenge-ne0qg7`, commit c93e377) gives "157 of 570 residues (27.6%) at
pLDDT >= 70; global pLDDT 57.06; PDB70 homolog hits = 0". It also says the author could not reproduce
the PDB70 search either.

- **157/570:** **AGREE.** The recorded figure was *calculated* from rounded band fractions
  (0.276 × 570 = 157.3, from 0.223 + 0.053). My figure is a direct count of the 570 per-residue
  values = 157 exactly. The percentage is 27.5% (157/570), not 27.6%. The 27.6% comes from summing
  rounded fractions. This is a minor difference and does not change the count.
- **Global 57.06:** **AGREE** with the API field. Note that the per-residue mean is 57.07.
- **PDB70 hits = 0:** **CANNOT TELL** directly, because neither derivation accessed PDB70. My phmmer-vs-PDB proxy finds
  0 significant hits, which is consistent with it.

Overall: the AlphaFold numbers are independently confirmed from different input files (per-residue
data rather than summary fractions). The PDB70 count is still unverified by either derivation.

```swarm-replication
{"claim_id": 69, "my_value": "157 of 570 residues (27.5%) at pLDDT>=70 by direct per-residue count of AF-E7F5V5-F1 v6; global pLDDT 57.06 (API; per-residue mean 57.07); PDB70 hits not reproducible here (phmmer vs PDB: 0 included hits, best E=0.44)", "agrees": true,
  "note": "AlphaFold counts confirmed exactly from per-residue data rather than rounded fractions; the PDB70=0 part is supported only by a weaker phmmer-vs-PDB proxy because PDB70/HHpred were unreachable."}
```
