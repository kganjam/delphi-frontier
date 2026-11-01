# Manifest — claude-zf2ff-kcnh-census-tree-1 (is `kcnh2a` specifically absent, or is the family incomplete?)

| | |
| --- | --- |
| Nebius job | `aijob-e00nvq278rsze2f6bp`, name `claude-zf2ff-kcnh-census-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` — CPU-only work; tenant non-GPU vCPU quota exhausted by other teams |
| Done | `2026-11-01T16:04:12Z` |
| Job script | `scripts/job_run_tree3.sh`; input built by the inline step recorded in `census_tree_input_ledger.json` |
| Log | `job_log_aijob-e00nvq278rsze2f6bp.log` |

## Inputs

| Item | Digest |
| --- | --- |
| `census_tree_input.faa` (26 sequences) | sha256 `771f8160a3a2dca5ec4795eb9674e9237fa1d1d199dd3da64f63bfe6399b9c84`, **re-hashed in-container to the same value** |
| per-locus provenance | `census_tree_input_ledger.json` (scaffold, interval, top query, AS, coverage, identity, protein sha256) |
| upstream mapping | `census.paf` — miniprot 0.18-r281, **all 10** zebrafish KCNH queries, `-N 10 --outs=0.5 --trans`, 5 whole-scaffold chunks, exit 0 |

Overlapping hits on the same scaffold were merged into one locus, so a locus is a genomic region,
not a query. 65 raw hit intervals merged to **14 loci**, each represented by its longest predicted
protein, plus the 10 zebrafish paralogs and 2 human outgroups.

## Software

MAFFT (rc 0); IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, `--seed 12345`.
Outputs: treefile sha256 `0f322f8477c5f302cfd9ae91482f9f6a8aa124d35ad12f32dce2930997690b68` (1402 B),
contree `fa89c77a63d71d6525ea13dc717c43ee17e28fa05ff4448b1abfeb64f8725328`,
`.iqtree` `7ba455c374fc553493cadba9dccb796c7a7710dce5f95aa932bc946a95635a3e`,
`.log` `353bd702a9b9be9182ffbc6b92c04248d29720b01a9a4a7995e8619828854a6b`.

## Result (`census_analysis.json`)

**9 of the 10 zebrafish KCNH paralogs have at least one flying-fish locus placed with them. The one
exception is `kcnh2a`.**

| zebrafish paralog | loci assigned |
| --- | --- |
| `kcnh1a`, `kcnh1b`, `kcnh2b`, `kcnh6a`, `kcnh6b` | 1 each |
| `kcnh3`, `kcnh5a`, `kcnh7` | 2 each |
| `kcnh4a` | 3 |
| **`kcnh2a`** | **0** |

So the family is **not** generally missing from this assembly — it is well represented, 14 loci
across 9 paralogs — and the `kcnh2a` gap is **specific** rather than a symptom of general draft
incompleteness. That is the sharper of the two explanations left open by the second tree.

## What this still does not establish

- **It is a statement about this assembly, not about the species.** A draft, scaffold-level,
  unannotated assembly can miss one gene; and if the Exocoetid `kcnh2a` were divergent enough, its
  locus could be placed with a neighbouring paralog instead of appearing as a `kcnh2a` sister.
- Three assignments are **weakly supported and should be read as unresolved**: `locus03`
  (42.7/68), `locus14` (23.4/62) and `locus11` (no support value recovered). Excluding all three
  does not change the headline, because none of them was assigned to `kcnh2a`.
- 14 loci against 10 queries is expected, not anomalous: zebrafish has more KCNH genes than the 10
  retrievable from UniProt for this project (`kcnh8a`/`kcnh8b` could not be fetched), so some loci
  may belong to paralogs absent from the reference set.
- A gene tree places sequences by substitution likelihood. **No synteny was used here**; a separate
  local synteny test of the `kcnh2a` neighbourhood is reported in `data/synteny/`.
- One run, one operator, not independently reviewed. A model-sensitivity re-run
  (`claude-zf2ff-census-sensitivity-1`, ModelFinder instead of a fixed `LG+G4`, seed 777) was
  submitted to check that this conclusion is not an artefact of the substitution model.
