# Replicate 11: how many sequences the kcnk5b PDB70 search returned, and what the top hits are

**Claim with the number removed:** "PDB70 search on kcnk5b returns N sequences whose top hits are real K2P channel structures". The inputs are from `msa_search_native` against PDB70.

**My value:** the MSA file has **76 sequences, which is the query plus 75 PDB70 hits**. Those 75 hit chains come from **73 distinct PDB entries**: 6UWM contributes chains A and B, and so does 7T4X. Uncertainty: none for the count. It is an exact count of records in a file whose hash I checked. This is an **observation** of the archived search output; I did **not** re-run the search.

**Top hits:** the first 13 hits are all real K2P (two-pore-domain K⁺) channel structures, and hit 1 is the nearest ortholog family (TASK-2 = KCNK5). Hits 14–75 are other K⁺-channel pore domains, aligned only over the P-loop/selectivity-filter region (19–64 residues). So the qualitative part of the claim holds.

## Inputs, sources and read-levels

| Input | Source | Read-level |
|---|---|---|
| The MSA (`kcnk5b_core.a3m`, 152 lines, sha256 `d65d3773…160b01`) | branch `origin/claude/mol-sims-20261101` @ `7bc704ed`, path `results/mol-sims/claude-20261101/structures/msa/kcnk5b_core.a3m`, added in commit `c97ff8d4` (the only commit touching it) | full-text (primary tool output) |
| Search provenance: tool `msa_search_native`, model `msa-search-pdb70`, database `pdb70_220313`, query `Q6PFU3 1-265`, op `op-71484e57aa8b6dcb`, status SUCCEEDED | `.../msa/kcnk5b_core_receipt.json`, same branch | full-text. I read it **after** my own count. |
| Receipt field `a3m_n_seqs: 76` and `a3m_sha256` | same receipt | full-text. Its hash equals the hash I computed on the file, and its embedded a3m matches the file. |
| Identities of the hit PDB entries (titles) | PDBe REST API `https://www.ebi.ac.uk/pdbe/api/pdb/entry/summary/<id>`, queried 2026-11-04 for all 73 entries. All returned. RCSB `data.rcsb.org` did not respond (HTTP 000) from this container. | listing (entry titles only) |

## Arithmetic

- `grep -c '^>' kcnk5b_core.a3m` → **76** header lines.
- The first record is `>query`, a 265-aa sequence. So 76 − 1 = **75** hit records.
- Distinct hit headers: 75, with no duplicate chain IDs.
- Distinct 4-character PDB IDs among the hits: 73. Two entries have two chains each: 6UWM_A/6UWM_B and 7T4X_A/7T4X_B. 75 − 2 = 73.

## Top hits

My calculation: identity counts query-aligned match columns only; lowercase a3m insertions are dropped. Coverage counts the non-gap aligned columns out of 265.

| # | Hit | Aligned cols | Identity | PDBe title (abridged) |
|---|---|---|---|---|
| 1 | 6WLV_A | 263 | 64.3% | TASK2 in lipid nanodisc pH 6.5 |
| 2 | 6WM0_A | 263 | 64.3% | TASK2 in lipid nanodisc pH 8.5 |
| 3–5 | 4XDK_D, 4XDL_A, 4BW5_B | 245 | 40.4% | human TREK2 (K2P10.1) |
| 6 | 6W88_B | 228 | 38.2% | K2P2.1 (TREK-1):ML335 |
| 7–9 | 4WFE_B, 7LJ5_A, 7LJ4_B | 231 | 40.3–40.7% | human TRAAK |
| 10 | 4TWK_B | 228 | 36.8% | human TREK1 (K2P2.1) |
| 11–12 | 3UKM_D, 7SK1_B | 220 | 34.1% | human K2P1 (TWIK-1) |
| 13 | 6RV3_D | 184 | 41.3% | human TASK-1 (K2P3.1) |
| 14–75 | BK/Slo1, NaK, KcsA, MthK, Kv1.2/1.3/3.1/4.2, KCNQ1/2/4, hERG, Eag1, SK4, SthK, MloK1, KAT1, AKT1, GsuK | 19–64 | 28.6–63.2% | non-K2P K⁺ channels, filter region only |

Inference, not an observation: the query is zebrafish Kcnk5b residues 1–265, UniProt Q6PFU3 according to the receipt. Its top hit is TASK-2 (KCNK5) at 64% identity over 263/265 columns, which fits it being a K2P5/TASK-2 ortholog. I did not open UniProt to confirm Q6PFU3. My read-level for that accession is the receipt only.

## Scope of what I did not do

- I did not re-run HHblits/HHsearch against `pdb70_220313`. This container has no PDB70 database or HH-suite. The count comes from the archived output, not from an independent search.
- To find inputs I searched branch contents for `pdb70|msa_search_native|kcnk5` (file names only) across all remote branches. To find the recorded claim I searched only `origin/claude/mol-sims-20261101` and `origin/main` for `72 (sequences|hits|aligned)` in `*.md`/`*.json`, with no match. I did not search every branch.
- Disclosure: while printing the receipt I also printed the start of `structures/msa_identity.json`. That file is the earlier author's ranking working. I saw only its `fgf10a_core` and `fgfr2b_d2d3` entries, stopped there, and did **not** read its `kcnk5b_core` entry.

## Comparison with the recorded value

The recorded value comes from the question text: **72 sequences**. I did not locate the document that states it.

- My observed count: 76 sequences in the a3m, which is 75 hits plus the query. 73 distinct PDB entries.
- 72 does not match any count I can get from this file: all records (76), hits (75), distinct PDB entries (73), or distinct entries minus the query (n/a). If the recorded claim was based on another run, another database version or another filter (for example an E-value or coverage cutoff), that source is `unknown` to me.
- The qualitative half of the claim ("top hits are real K2P channel structures") **agrees**: hits 1–13 are TASK-2, TREK-2, TREK-1, TRAAK, TWIK-1 and TASK-1 structures.

**Verdict: DISAGREE on the number** (76 sequences / 75 hits vs. 72). **AGREE on the top-hit identity.**

```swarm-replication
{"claim_id": 11, "my_value": "76 sequences in the a3m (query + 75 PDB70 hit chains from 73 distinct PDB entries); top 13 hits are K2P structures (TASK-2, TREK-2, TREK-1, TRAAK, TWIK-1, TASK-1)", "agrees": false,
  "note": "The archived kcnk5b_core.a3m (sha256 matches its receipt, which itself reports a3m_n_seqs=76) has 76 records, not 72, though the claim that the top hits are real K2P structures holds."}
```
