# Manifest — claude-zf2ff-halfbeak-tree-1 (the chromosome-level sister-family test)

| | |
| --- | --- |
| Nebius job | `aijob-e00w2q5tkmgw74bcr5`, name `claude-zf2ff-halfbeak-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` (CPU-only work; tenant non-GPU vCPU quota exhausted) |
| Input | 51 sequences, uncompressed sha256 `a155b178465d91d568b6d7e2803545326b1f273a660745e4bb725fce5b3b67a4`, **re-hashed in-container to the same value** |
| Transport note | At 55 KB the input exceeded the inject-file plaintext limit (65536 bytes), so it was gzipped and base64-encoded and decoded in-container; `scripts/job_run_tree11_halfbeak.sh` records that step |
| Halfbeak assembly | `GCA_056149455.1`, *Hemiramphus limbatus*, **Chromosome level**, genome FASTA sha256 `4eb5eacf08983a12c93ca6013504ff12dd9205a7347a5b51bee986fc30b30cb3` |
| Upstream scan | `scripts/census_kcnh_halfbeak.sh` — the **same** 10 zebrafish KCNH queries and the **same** miniprot parameters as the flying-fish census, so the two are comparable; exit 0; 14 merged loci |
| Software | MAFFT; IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, seed 12345; log-likelihood −52466.7093 (s.e. 970.2845) |
| Output | treefile sha256 `d6469502955c9a0de7acd4b291c36002fb9c47eb6084497f3f27268c2c60b430` |

## Why this job existed

The `kcnh2a`-loss result rested on **two** Beloniformes, one of them a scaffold-level draft. This adds
a third: *Hemiramphus limbatus*, in **Hemiramphidae — the sister family to Exocoetidae** — on a
**chromosome-level** assembly. If the halfbeak also lacks an `a`-side locus while carrying the rest of
the family, the result stops depending on a draft assembly.

## Controls reproduce

- Takifugu `kcnh2a` + zebrafish `kcnh2a`: **100/100** (unchanged across three trees and two models).
- flying-fish `locus01` + medaka `kcnh2b`: **98.6/100**.

## Result

The halfbeak's 14 KCNH-like loci distribute across the family — `kcnh1a`, `kcnh3` ×2, `kcnh4a`,
`kcnh4b`, `kcnh5a`, `kcnh5b`, `kcnh6a`, `kcnh6b`, `kcnh7` ×2, `kcnh8`, and one `kcnh2`-side locus —
most at 99.5–100/100. Two are weakly placed and are to be read as unresolved (`locus02` at 63.6/82,
`locus11` at 4.9/31).

**The two clades that answer the question:**

| clade | members | support |
| --- | --- | --- |
| **`kcnh2a`** | Takifugu `kcnh2a`, zebrafish `kcnh2a` — **and nothing else** | 100/100 |
| **`kcnh2b`** | zebrafish `kcnh2b`, medaka `kcnh2b`, **flying-fish `locus01`**, **halfbeak `locus01`** | **98.2/99** |

**Three Beloniformes — medaka, halfbeak and the flying fish — each contribute exactly one
`kcnh2`-family locus, and all three fall in the `b` clade. The `a` clade contains only the two
non-Beloniformes.** The halfbeak is chromosome-level and carries the rest of the KCNH family, so
"missing because the assembly is a draft" is no longer available as an explanation.

Note on the "no halfbeak locus" list printed by the analysis: it names many zebrafish paralogs, but
that is an artefact of scoring each locus by its *closest* reference — medaka is phylogenetically
nearer to the halfbeak than zebrafish is, so medaka entries win those comparisons. The meaningful
statement is **clade membership**, given above, not nearest neighbour.

## What is now established, and what still is not

**Established across three Beloniformes, one chromosome-level, with a non-Beloniform outgroup
retaining the `a` copy and controls reproducing under two substitution models:** the `kcnh2a` paralog
is absent from the Beloniform lineage that contains flying fishes, and each of these species carries
the `b` copy instead.

**Still not established:** orthology in the strict sense (no synteny was run in any of these trees);
anything about expression, conductance or phenotype; and what the published flying-fish `kcnh2a`
signal (PMID 34534441) actually refers to — that needs the paper's full text, which this project has
not read. Four Beloniform genomes beyond medaka remain unexamined and could still overturn this.

## Consequence

Perturbation row **P1 — the plan's headline edit — targets a gene the clade does not have.** It cannot
be transferred from zebrafish by sequence identity, and any design resting on the published
flying-fish `kcnh2a` result needs that paper's own gene identifiers read first.
