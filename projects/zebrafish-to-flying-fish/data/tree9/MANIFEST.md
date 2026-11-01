# Manifest — claude-zf2ff-slc43-full-tree-1 (the full-length `slc43a2a` rerun)

| | |
| --- | --- |
| Nebius job | `aijob-e00g2dmdpfbabd4kx9`, name `claude-zf2ff-slc43-full-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` (CPU-only work; tenant non-GPU vCPU quota exhausted) |
| Input | `slc43_fulllength_tree_input.faa`, 16 sequences, sha256 `82e89eb4b5f948ac6729ebb6886adf6bd04a9e0538d21106cf9fe42da466fbe7`, **re-hashed in-container to the same value** |
| The sequence that made the difference | zebrafish `slc43a2a`, Ensembl `ENSDARG00000036848`, chromosome 15, longest translation **577 aa** — replacing UniProt's 153 aa fragment, which is dropped from this input and kept in `data/census_slc43/` for the record |
| Software | MAFFT; IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, seed 12345 |
| Output | treefile sha256 `84cc64615682785a3debb5e902b7655b81d4c598d6e31ab1ad37554ac12d34a6` |
| Result | `slc43_fulllength_analysis.json` |

## Result

| locus | closest reference | support | reading |
| --- | --- | --- | --- |
| `slc43locus01` (JAGFBZ010000485.1, 593 aa) | medaka `slc43a2b`, 2-tip clade | **100/99** | a confident **`slc43a2b`/LAT4** ortholog |
| `slc43locus02` (JAGFBZ010001224.1, 570 aa) | **full-length zebrafish `slc43a2a`**, 2-tip clade | **36.2/65** | **unresolved** — suggestive only |

All five `slc43a2`-family sequences form one clade at 97.5/98 containing both zebrafish paralogs,
medaka `slc43a2b`, and both flying-fish loci.

**What changed by swapping the reference.** With the 153 aa fragment, both flying-fish loci fell on
the `slc43a2b` side and `slc43a2a` could not attract anything. With the full-length sequence,
`slc43locus02` moves to pair with `slc43a2a` instead. So the earlier result **was** an artefact of the
fragment, exactly as the previous manifest predicted it might be.

**What is still not claimable.** 36.2/65 is weak support on a short internal branch. This project
therefore does **not** claim `slc43locus02` is the `slc43a2a` ortholog. What it claims is narrower and
checkable: the assembly carries **two** `slc43a2`-family loci, one of which is confidently `a2b`, and
the other's paralog assignment is unresolved.

## Where that leaves the open Problem

`zf2ff-problem-lat4a-identifier` stays open, with its blocker now identified and partly removed:

1. **Removed:** the claim that no full-length zebrafish `slc43a2a` reference exists. Ensembl has one;
   UniProt does not. Any future work should take SLC43 references from Ensembl.
2. **Remaining:** the support on the `a`-side placement. The named next test — adding `slc43a2b` from
   more percomorphs so the `b` clade has structure and an `a`-side locus stands out — was submitted as
   `claude-zf2ff-slc43-broad-tree-1` (`data/tree10/`).
3. **Untouched by any of this:** which gene the *papers* mean by "lat4a", and what the reported
   convergent amino-acid change is. That needs the full text of PMID 34534441 and PMID 40689752 and
   cannot be settled by sequence work here.

**Annotation pattern worth recording:** only zebrafish has an annotated `slc43a2a`. Ensembl lists
`slc43a2b` and **no** `slc43a2a` for Takifugu, stickleback and medaka — the same pattern this project
found for `kcnh2a`, and the same caution applies: that is an annotation fact, not a genome-content
proof.

## Scope

Protein gene tree over UniProt/Ensembl references and miniprot predictions from an unannotated draft
assembly. Medaka is a labelled proxy. No synteny. Nothing here is evidence of transport activity,
expression or function. One run, one operator, not independently reviewed.
