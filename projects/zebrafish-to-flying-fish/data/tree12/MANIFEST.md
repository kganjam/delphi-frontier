# Manifest — claude-zf2ff-slc43-bel-tree-1 (four Beloniformes, and the a/b structure resolves)

| | |
| --- | --- |
| Nebius job | `aijob-e00wj350bydkkdkzkb`, name `claude-zf2ff-slc43-bel-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` (CPU-only work; tenant non-GPU vCPU quota exhausted) |
| Input | 24 sequences, sha256 `426255c786e5ee07c92ffe1370454ca91cd4dc358c59378a9454542c03279653`, **re-hashed in-container to the same value** |
| Added | the two longest `slc43a2`-family predictions from each of *Hemiramphus limbatus*, *Xenentodon cancila* and *Cololabis saira*; per-sequence digests in `slc43_beloniform_tree_input_ledger.json` |
| Software | MAFFT; IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, seed 12345 |
| Output | treefile sha256 `00a484b0016d17d9c86ed495ed2858b2d44d1e28c890d71b6d6c5ca6467f98ed` |
| Result | `slc43_beloniform_analysis.json` |

## Result — two parallel clades, one locus per species in each

**`b`-side clade (8 tips, support 79.8/76):** zebrafish, medaka, Takifugu and stickleback
`slc43a2b`, plus the **first** `slc43a2`-like locus of each of the four Beloniformes — flying-fish
`slc43locus01`, halfbeak, needlefish, saury.

**`a`-side clade (5 tips, support 49.4/69):** zebrafish `slc43a2a`, plus the **second**
`slc43a2`-like locus of each of the same four Beloniformes — flying-fish `slc43locus02`, halfbeak,
needlefish, saury.

Every one of the four Beloniformes carries **both** an `a`-like and a `b`-like `slc43a2` locus, and
the two clades have exactly the composition an ancestral duplication retained across all these
species should produce: one locus per species per side, with the matching zebrafish paralog.

## What this settles, and what it does not

**Settles, by composition:** `slc43locus02` groups with the `a` paralog, alongside its halfbeak,
needlefish and saury counterparts. That is the fourth and strongest version of an assignment whose
support climbed as the input improved — 36.2/65 with two taxa, 66.7/78 with four, and now a
structurally coherent 1:1 pattern.

**Does not settle, and is not claimed:** the `a`-side clade's own support is **49.4/69**, below
conventional thresholds. The argument here rests on **clade composition** — the parallel 1:1 pattern
— not on the bootstrap value, and that distinction is the honest one. Orthology still has no synteny
behind it.

## The thing this validates, which matters more

The F326 residue comparison in `FULLTEXT-FINDING.md` §5 compared the flying fish against a halfbeak,
a needlefish and a saury. This tree shows those four sequences are the **`a`-side locus of each
species** — that is, the comparison was made between **homologous loci**, not between a glider's `a`
paralog and a non-glider's `b` paralog. Without this tree that comparison would have been
unvalidated; with it, the F/L/F/F/I pattern is read across one orthologous group.

## Scope

Protein gene tree over Ensembl/UniProt references and miniprot predictions from public assemblies.
No synteny. Nothing here measures transport activity, expression or phenotype. One run, one operator,
not independently reviewed.
