# Manifest — claude-zf2ff-slc43-broad-tree-1 (the last sequence test available for `lat4a`)

| | |
| --- | --- |
| Nebius job | `aijob-e00vqt5q32bjca4ktb`, name `claude-zf2ff-slc43-broad-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` (CPU-only work; tenant non-GPU vCPU quota exhausted) |
| Input | `slc43_broad_tree_input.faa`, 18 sequences, sha256 `9d899dce7e613cd22a3fcc0bc22eb313147c2090c5a96bb4a93cf8bbcfae777f`, **re-hashed in-container to the same value** |
| Added | Takifugu `slc43a2b` (`ENSTRUG00000003499`, 598 aa) and stickleback `slc43a2b` (`ENSGACG00000020606`, 598 aa); per-sequence digests in `slc43_broad_tree_input_ledger.json` |
| Software | MAFFT; IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, seed 12345 |
| Output | treefile sha256 `fff0780d0106218f8c68fc8cd34fb540fd444488de45fa44515815b0bdaa8d60` |
| Result | `slc43_broad_analysis.json` |

## The test

With four `slc43a2b` reference taxa instead of two, the *b* clade has real structure, so a locus that
belongs on the *a* side should stand out. The question was written into the input ledger before the
job ran.

## Result

- **`slc43locus01` is confirmed as a *b*-side locus**: it sits **inside** the clade containing all
  four reference `slc43a2b` sequences (5 tips, support 78.5/73). Its nearest-neighbour support fell to
  50.6/73 simply because Takifugu and stickleback now compete with medaka for "closest"; the
  meaningful statement is **clade membership**, not nearest neighbour.
- **`slc43locus02` pairs with full-length zebrafish `slc43a2a` at 66.7/78**, up from 36.2/65, and it
  stays **outside** the *b* clade in both trees.

## What this does and does not settle

Three trees now point the same way for `slc43locus02` — it is not in the `a2b` clade and it pairs with
`slc43a2a` whenever a full-length `a2a` is present — and the support rose each time the input improved
(36.2/65 → 66.7/78). **It is still below conventional thresholds** (UFBoot ≥ 95, SH-aLRT ≥ 80), so
this project does **not** claim `slc43locus02` is the `slc43a2a` ortholog. A consistent direction
across three underpowered trees is exactly the kind of result that should not be promoted to a claim.

**The sequence route for `lat4a` is now exhausted at this project's disposal.** Both available
improvements — a full-length reference and more taxa — have been applied, and both left the question
short. What remains is a **literature** step, not a compute step: PMID 34534441 and PMID 40689752 must
be read in full text for their own gene identifiers and the residue position of the reported
convergent change. `zf2ff-problem-lat4a-identifier` stays open and now records exactly that.

## Scope

Protein gene tree over Ensembl/UniProt references and miniprot predictions from an unannotated draft
assembly. No synteny. Nothing here is evidence of transport activity, expression or function. One
run, one operator, not independently reviewed.
