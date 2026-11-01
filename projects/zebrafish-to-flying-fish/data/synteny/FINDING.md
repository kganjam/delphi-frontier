# Synteny around zebrafish `kcnh2a` (analysis G3b) — and why it walks back this project's own headline

Local run, `scripts/synteny_kcnh2a.py`, exit 0. 36 protein-coding genes flanking `kcnh2a` on GRCz11
chr2:23.6–24.7 Mb, one protein each from Ensembl, mapped onto `GCA_018398805.1` with miniprot
0.18-r281 (`-N3 --outs=0.6`). Receipts: `synteny.json` (per-gene protein sha256, hit, coverage,
identity), `synteny.paf`, `neighbourhood.faa`.

## The method works: a 12-gene block in perfectly conserved order

33 of 36 neighbourhood proteins map. Twelve of them — everything from `mrpl34` to `mast3a` on the
3′ side — land on **JAGFBZ010000844.1** with zebrafish gene order and flying-fish coordinate order
**monotonically matching**:

| zebrafish gene | GRCz11 start | → | JAGFBZ010000844.1 |
| --- | --- | --- | --- |
| `mrpl34` | 24,317,465 | | 381,197 |
| `ano8a` | 24,321,751 | | 387,290 |
| `plvapa` | 24,365,452 | | 423,599 |
| `nr2f6a` | 24,374,305 | | 448,880 |
| `ocln1` | 24,386,453 | | 463,689 |
| `marveld2l` | 24,400,725 | | 481,559 |
| `kcnn1a` | 24,410,494 | | 507,906 |
| `si:rp71-39b20.4` | 24,495,804 | | 658,392 |
| `rps28` | 24,507,597 | | 663,337 |
| `angptl4` | 24,536,762 | | 689,667 |
| `cnn2` | 24,548,249 | | 722,504 |
| `mast3a` | 24,638,367 | | 809,963 |

So the neighbourhood is **present** in the assembly and carries conserved blocks. A further 5 genes
form a second ordered block on JAGFBZ010000990.1. The rest scatter across 11 more scaffolds, which is
what a scaffold-level draft looks like.

## The part that contradicts §R7/§R7b

`slc12a7a` is `kcnh2a`'s **immediate 5′ neighbour** in zebrafish — it ends at 24,069,434 and `kcnh2a`
starts at 24,080,694, a gap of about 11 kb. In the flying-fish assembly `slc12a7a` best-hits
**JAGFBZ010001591.1:1,760,495–1,814,132** (coverage 1.00) — **the same scaffold** as the `kcnh2`-like
region at 1,301,510–1,579,457, about **181 kb** away.

A kcnh2-family gene and `kcnh2a`'s immediate zebrafish neighbour on one scaffold is what the
**`kcnh2a`** neighbourhood should look like. And checking the alternative: zebrafish `slc12a7b` sits on
chr24 at 39.78–39.89 Mb, and the 22 protein-coding genes around it contain **no `kcnh2`-family gene**
at all. So the `slc12a7` + `kcnh2` arrangement is a feature of the **a** block, not the **b** block.

That points the opposite way from the gene trees, which placed this region with `kcnh2b` at 99/100
with passing controls, and from the census, which found no `kcnh2a` locus.

## What this project now claims, which is less than it claimed an hour ago

**Withdrawn:** "no `kcnh2a`-like region exists anywhere in this assembly". That was too strong.

**Current statement:** no region in `GCA_018398805.1` is *identifiable as* `kcnh2a` by gene tree, and
the synteny evidence is **in tension** with the tree's assignment of the one `kcnh2`-like region. The
identity of JAGFBZ010001591.1:1,301,510–1,579,457 is therefore **unresolved**.

Candidate resolutions, none tested here:

1. The `slc12a7a`-like hit on JAGFBZ010001591.1 is really the **`slc12a7b`** locus. This project has
   documented the same paralog trap twice already (`kcnh2a`/`kcnh2b`, `kcnk5a`/`kcnk5b`), and only
   `slc12a7a` was used as a query. **Test: map `slc12a7b` and tree-test both hits.** Weakened but not
   excluded by the observation above that zebrafish `slc12a7b` has no `kcnh2` neighbour.
2. The Exocoetid `kcnh2a` is divergent enough that the tree misplaces it with `kcnh2b`. **Test: a
   tree with more Beloniformes outgroups**, e.g. medaka KCNH proteins, so the fish-specific branch is
   better sampled than by two human sequences.
3. 181 kb is simply too far to infer adjacency in a draft assembly, and the co-location is a
   coincidence of a larger ancestral block. **Test: nothing cheap; needs a contiguous assembly.**
4. Zebrafish `kcnh2b` may also sit near an `slc12a7` paralog, which would dissolve the argument. This
   **could not be checked**: Ensembl has no `kcnh2b` symbol for zebrafish, so the gene's GRCz11
   location was not retrievable here.

## Scope

Protein-to-genome mapping onto an unannotated assembly. Co-location of best hits is evidence about
assembly content and gene order, not an orthology proof, and not evidence of expression or function.
Every hit is a best hit of a single query protein and carries the paralog ambiguity this project has
documented elsewhere. One operator, not independently reviewed.
