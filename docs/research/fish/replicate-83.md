# Replicate 83 — kcnk5b PDB70 a3m: sequence count, distinct entries, top-hit identity

Independent re-derivation. I counted from the primary file before looking for any recorded value.
I did not read `replicate-11.md` before deriving; after deriving I read only its commit message and
its final `swarm-replication` block (see Comparison).

## Inputs

| Input | Source | Read-level |
|---|---|---|
| `kcnk5b_core.a3m` (20,906 bytes, sha256 prefix `d65d377353a647de`) | `results/mol-sims/claude-20261101/structures/msa/kcnk5b_core.a3m` on branch `claude/mol-sims-20261101` | full-text |
| PDB header records (TITLE, MOLECULE, ORGANISM) for the top 18 hits | `https://files.rcsb.org/header/<ID>.pdb` | full-text (header only) |

`data.rcsb.org` REST was refused by the proxy (HTTP 403); `files.rcsb.org` headers worked.

## Arithmetic (all counts are observations of the file, not simulations)

- Lines starting with `>`: **76**.
- Minus the record named `query`: 76 − 1 = **75** hit chains.
- Distinct 4-character PDB IDs among the 75 hits: **73**.
  75 − 73 = 2, because two entries contribute two chains each: `6UWM` (A, B) and `7T4X` (A, B).
  No header line appears twice.
- Query match-state length: 265 columns. Every record's uppercase-plus-gap length equals 265, so the a3m is well-formed.

Identity to the query over aligned columns for the top hits. I calculated these; the file does not report them:
6WLV_A 0.64 (263 cols), 6WM0_A 0.64, 4XDK_D/4XDL_A/4BW5_B 0.40, 6W88_B 0.38, 4WFE_B 0.41,
7LJ5_A 0.41, 7LJ4_B 0.40, 4TWK_B 0.37, 3UKM_D 0.34.

## Identity of top hits (observed from PDB headers, in a3m order)

| Rank | Entry | Header says | K2P? |
|---|---|---|---|
| 1–2 | 6WLV, 6WM0 | TASK2 in nanodisc, pH 6.5 / 8.5; *Mus musculus* | yes (KCNK5) |
| 3–5 | 4XDK, 4XDL, 4BW5 | human TREK2 (KCNK10) | yes |
| 6 | 6W88 | mouse K2P2.1 TREK-1 : ML335 | yes |
| 7–9 | 4WFE, 7LJ5, 7LJ4 | human TRAAK (KCNK4) | yes |
| 10 | 4TWK | human TREK1 (KCNK2) | yes |
| 11–12 | 3UKM, 7SK1 | TWIK-1 (KCNK1), human / rat | yes |
| 13 | 6RV3 | human KCNK3 (TASK-1) | yes |
| 14–16 | 6ND0, 6V35, 6V22 | human BK (Slo1) | no |
| 17–18 | 6UFE, 2Q67 | *B. cereus* NaK-family | no |

My inference: the a3m lists hits in HHblits/hhsearch rank order. I did not have the `.hhr` file
to confirm scores, so "top" here means "first in the a3m". Scope of the negative search: I did not check the headers of
ranks 19–75, so further K2P entries may appear deeper in the list.

Correction to my own prior belief: from memory I expected 6WLV/6WM0 to be zebrafish TASK2. The header
says *Mus musculus*, and the header governs.

## My value

76 sequences (query + 75 PDB70 hit chains from 73 distinct PDB entries). Hits 1–13 are K2P
structures (TASK-2, TREK-2, TREK-1, TRAAK, TWIK-1, TASK-1); hits 14–18 are BK/NaK.
Uncertainty: none on the counts, which are an exact integer count of the file. The "top hits" description
depends on a3m order matching rank order.

## Comparison (done after derivation)

Recorded value, from the result block of `replicate-11.md` on branch `claude/pdb70-kcnk5b-search-s7699q`
(read-level: full-text for that block only): 76 sequences, 75 hits, 73 distinct entries, top 13 K2P. The question as posed
also gives 76 / 75 / 73 and "top hits are K2P structures". I **AGREE** on every number and on the K2P
description. Replicate-11 marked `agrees: false` against an *earlier* claim of 72. That figure
disagrees with the file, and I do not reproduce it.

```swarm-replication
{"claim_id": 83, "my_value": "76 sequences (query + 75 PDB70 hit chains, 73 distinct PDB entries; 6UWM and 7T4X contribute 2 chains each); hits 1-13 are K2P (TASK-2, TREK-2, TREK-1, TRAAK, TWIK-1, TASK-1)", "agrees": true,
  "note": "A direct count of kcnk5b_core.a3m plus RCSB header lookups for the top 18 hits reproduces 76/75/73 and the K2P top hits exactly."}
```
