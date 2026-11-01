# Manifest — claude-zf2ff-outgroup-tree-1 (the control that decides whether "loss" is the right word)

| | |
| --- | --- |
| Nebius job | `aijob-e00hnvzmx6a1jjedq1`, name `claude-zf2ff-outgroup-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` — CPU-only work; tenant non-GPU vCPU quota exhausted by other teams |
| Done | `2026-11-01T16:28:02Z` |
| Job script | `scripts/job_run_tree6_outgroup.sh` |
| Input | `outgroup_tree_input.faa`, 37 sequences, sha256 `48da84ef0016fd97fb9c68a929fe93d71952abda5bc924eeead1053ed212e454`, **re-hashed in-container to the same value** |
| Added sequence | *Takifugu rubripes* `kcnh2a`, Ensembl `ENSTRUG00000010880`, 930 aa, protein sha256 in `outgroup_tree_input_ledger.json` |
| Software | MAFFT; IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, `--seed 12345`; log-likelihood −46108.7061 (s.e. 831.3867) |
| Outputs | treefile sha256 `09a5cb5ab117594b16f7e6b4b8bc7d7a3decb75a3d0cdb10cf1b0cd4b651063c` (1933 B); contree `1508e3d6ef1d981a5cd3e054852ecea2bf29b5b0930e987bef53319f977358a7` |

## Why this job existed

The previous job (§R7e) found the flying-fish `kcnh2`-like locus pairing with medaka `kcnh2b`, which
looked like retention of the *b* copy and loss of *a* in Beloniformes. But Takifugu's **single**
`kcnh2` gene is *named* `kcnh2a` while medaka's single gene is *named* `kcnh2b` — so the suffixes
could have been per-species annotation labels rather than orthology statements, and in that case
"loss" would be the wrong word. The alternative hypotheses were explicit:

- **If Takifugu's gene falls with zebrafish `kcnh2a`:** the *a* copy existed in acanthomorphs, so the
  Beloniform lineage lost it. "Loss" is earned.
- **If it falls with the `kcnh2b`/Beloniformes clade:** the zebrafish `a`/`b` split is narrower than
  assumed and "loss" is the wrong description.

## Result — the first hypothesis, unambiguously

**Takifugu `kcnh2a` + zebrafish `kcnh2a` form a 2-tip clade at 100/100**, and zebrafish `kcnh2a` is
Takifugu's single closest relative among all 20 reference proteins. The five `kcnh2`-family sequences
form one clade (99.7/100) containing two paralog sub-clades:

```
( (TAKIFUGU_kcnh2a , ZF_kcnh2a)100/100 , (ZF_kcnh2b , (OL_kcnh2b , HSPEC_locus01)99.5/100 ) )99.7/100
```

Reading it:

- The `kcnh2a`/`kcnh2b` duplication **predates** the split between cyprinids (zebrafish) and
  acanthomorphs (Takifugu, medaka, Exocoetidae), consistent with the teleost whole-genome duplication.
- Both copies are retained in zebrafish. **Takifugu retains the `a` copy. Medaka and the flying fish
  carry the `b` copy.**
- So the per-species annotation names were **right**, and the caution about them, while warranted, is
  resolved in their favour by sequence.
- **The Beloniformes lineage lacks the `a` copy** while a non-Beloniform acanthomorph retains it.
  That is what "loss in Beloniformes" means, and it is now supported by an outgroup rather than by
  the absence of a symbol.

## Limitations that remain

- **Two Beloniformes only**: medaka, and a draft-assembly prediction from one flying fish. A third
  Beloniform genome would strengthen this considerably and was not run.
- "Takifugu's single `kcnh2`" means the only gene carrying that symbol in Ensembl. An unnamed or
  unannotated Takifugu `kcnh2b` was **not** excluded; that would not disturb the `a`-clade placement
  but would weaken the "retains `a`, lacks `b`" phrasing, which this manifest therefore avoids.
- A protein gene tree places sequences by substitution likelihood. **No synteny** supports the
  Takifugu–zebrafish-`a` pairing, though 100/100 on a 2-tip clade is strong.
- The flying-fish sequence is a miniprot prediction from an unannotated draft assembly, not a
  sequenced transcript.
- One run, one operator, not independently reviewed.

## What it means for this project

`kcnh2a` — the gene the `longfin` literature characterises and this plan's primary candidate — is
**absent from the Beloniform lineage that contains flying fishes**, not merely missing from a draft
assembly. Perturbation row P1 therefore cannot be transferred gene-for-gene from zebrafish: the
target gene is not there to edit. Any design resting on the published flying-fish `kcnh2a` signal
(PMID 34534441) needs that paper's own gene identifiers read in full text first. **This project has
not read its methods and does not claim the paper is wrong.**
