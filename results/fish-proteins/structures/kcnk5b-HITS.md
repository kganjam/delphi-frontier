# What the kcnk5b PDB70 search actually returned

`msa_search_native` (MMseqs2, pinned `pdb70_220313`), operation `op-6d4bf65638eb8348`,
key `msa-kcnk5b-1793774492`. **71 hits across 69 unique PDB entries**, plus the query = 72
rows in the A3M.

Five hit identities were checked against RCSB (`data.rcsb.org/rest/v1/core/entry/<id>`,
retrieved 2026-11-03) rather than recalled. The rest of the 69 are **not** individually
verified here:

| PDB | RCSB title |
|---|---|
| **6WLV** | **TASK2 in MSP1D1 lipid nanodisc at pH 6.5** |
| **6WM0** | **TASK2 in MSP1D1 lipid nanodisc at pH 8.5** |
| 4BW5 | human two pore domain potassium ion channel TREK2 (K2P10.1) |
| 4XDK | human two pore domain potassium ion channel TREK2 (K2P10.1), in complex |
| 4XDL | human two pore domain potassium ion channel TREK2 (K2P10.1), in complex |
| 4WFE | Human TRAAK K+ channel in a K+ bound conductive conformation |
| 2R9R | Shaker-family voltage-dependent K+ channel (Kv1.2–Kv2.1 paddle chimera) |
| 1ORQ | voltage-dependent potassium channel in complex with an Fab |
| 6U9Z | Wild-type MthK pore in 6 mM K+ |
| 7T4X | AKT1 K+ channel from *A. thaliana* |

**The important row is 6WLV/6WM0.** RCSB's polymer-entity record for 6WLV gives the entity
description `Potassium channel TASK2` and the gene name **`Kcnk5`** — so the alignment contains
the direct ortholog of the query, captured in two pH states (6.5 and 8.5).

**Scope of that claim.** The hit set is *not* all K2P: 2R9R, 1ORQ, 6U9Z and 7T4X are
voltage-gated, prokaryotic and plant potassium channels. So the alignment spans the potassium
channel superfamily broadly, with K2P members (and the ortholog itself) among it. A correction
worth recording: 4BW5 was first described in this session's reporting as TRAAK from memory;
RCSB says TREK-2. 4WFE is the TRAAK entry.

Full hit list is in `kcnk5b_pdb70.a3m`.
