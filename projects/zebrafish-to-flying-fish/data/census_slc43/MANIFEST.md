# Manifest — claude-zf2ff-slc43-tree-1, and why it could not settle the question

| | |
| --- | --- |
| Nebius job | `aijob-e00bkn68ckf6jkqdsh`, name `claude-zf2ff-slc43-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` (CPU-only work; tenant non-GPU vCPU quota exhausted) |
| Input | `slc43_tree_input.faa`, 16 sequences, sha256 `1c1b2882e721dfecc6a6c468d0ea4822dbf4432d9d3c763e54007805b9829e18`, **re-hashed in-container to the same value** |
| Upstream scan | `scripts/census_slc43.sh`, miniprot 0.18-r281, `-N 10 --outs=0.5 --trans`, 6 zebrafish SLC43 queries, exit 0 → `census.paf`, merged into **8 loci** |
| Software | MAFFT; IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, seed 12345 |
| Output | treefile sha256 `c765cc9ead89f0ea5099a3047dba635b4bbfd242b431cab43d20be585e466a6f` |
| Result | `slc43_analysis.json` |

## Why this ran

`lat4a` is the **second** locus the flying-fish phylogenomic study names, and the project's open
Problem `zf2ff-problem-lat4a-identifier` records that the papers say "lat4a" while UniProt offers
zebrafish `slc43a2a` as a **153 aa fragment** and `slc43a2b` as a 592 aa full-length LAT4. The same
machinery that settled `kcnh2` was pointed at it.

## What the census found

**Two full-length LAT4-like loci**, not one:

| locus | scaffold | predicted aa | best query | cov / id |
| --- | --- | --- | --- | --- |
| `slc43locus01` | JAGFBZ010000485.1 | 593 | `slc43a2b_LAT4` | 1.00 / 0.786 |
| `slc43locus02` | JAGFBZ010001224.1 | 570 | `slc43a2b_LAT4` | 1.00 / 0.734 |

`slc43locus02` sits on the scaffold where round 2's **153 aa fragment** query had hit. With a
full-length prediction it is a real second locus, not a fragment artefact. Six further loci map to
the `slc43a1`/`slc43a3` subfamilies.

## The tree, and the honest limit it ran into

| locus | closest reference | support |
| --- | --- | --- |
| `slc43locus01` | medaka `slc43a2b` | **100/99** (2-tip clade) |
| `slc43locus02` | medaka `slc43a2b` group | 94.7/92 (4-tip clade) |
| `slc43locus04` | medaka `slc43a1a` | 97.9/98 |
| `slc43locus03` | zebrafish `slc43a1b` | 90.5/88 |
| `slc43locus05` | zebrafish `slc43a3a` | 98.9/90 |
| `slc43locus06/07/08` | zebrafish `slc43a3a` | **33.3/55 — unresolved** |

**Both** LAT4-like loci fall on the `slc43a2b` side, and **neither** resolves to `slc43a2a`. That is
not evidence that the `a` paralog is absent, because **the reference could not have shown it**: the
only zebrafish `slc43a2a` sequence in the input was the 153 aa fragment, which carries almost no
phylogenetic signal. So this tree **cannot** discriminate the `a` and `b` paralogs of `slc43a2`, and
the Problem record stays open — but for a newly specific reason rather than for not having looked.

## The fix, found and run

Ensembl **does** have a full-length zebrafish `slc43a2a`: `ENSDARG00000036848` on chromosome 15,
longest translation **577 aa**. UniProt simply does not carry it. The tree was therefore rebuilt with
that sequence replacing the fragment and submitted as `claude-zf2ff-slc43-full-tree-1`
(`data/tree9/`). That job's input ledger states the question it tests: whether either flying-fish
LAT4-like locus groups with the full-length `slc43a2a` rather than with `slc43a2b`.

## Scope

Protein-to-genome mapping and a protein gene tree on an unannotated draft assembly. Medaka is a
labelled proxy. Three locus assignments are weakly supported (33.3/55) and are to be read as
unresolved. Nothing here is evidence of expression, transport activity or function, and none of it
addresses what the published `lat4a` amino-acid change is — that still needs the paper's full text.
