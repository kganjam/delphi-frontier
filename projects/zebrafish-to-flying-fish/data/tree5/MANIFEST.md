# Manifest — claude-zf2ff-beloniform-tree-1

| | |
| --- | --- |
| Nebius job | `aijob-e00fx0t755je2ghg49`, name `claude-zf2ff-beloniform-tree-1` |
| State read from the CLI | `COMPLETED` |
| Platform / preset | `gpu-l40s-a` / `1gpu-8vcpu-32gb` — CPU-only work; tenant non-GPU vCPU quota exhausted by other teams |
| Done | `2026-11-01T16:21:14Z` |
| Job script | `scripts/job_run_tree5_beloniform.sh` |
| Input | `beloniform_tree_input.faa`, 36 sequences, sha256 `4f54fd77b1c15159f233377061e1193d72777ddee0d9abae57543b6184f96574`, **re-hashed in-container to the same value** |
| Provenance | `beloniform_tree_input_ledger.json` — per-sequence UniProt accession, length and FASTA sha256 for the 10 medaka proteins; the other 26 are the census input unchanged |
| Software | MAFFT; IQ-TREE 2, `LG+G4`, `-B 1000`, `--alrt 1000`, `--seed 12345`; log-likelihood −45052.1777 (s.e. 818.9061) |
| Outputs | treefile sha256 `0962cb1512f709cc77c6d78d2644d85b169c8fa6680a830ded5b152423285c7f` (1854 B); contree `6774f0541bff807980b9ab877b28bb696b56e84a41908aa5d824ea36f5e1819a`; `.iqtree` and `.log` hashed in-container but not printed, so not committed |

## The test and its result

**Prediction, stated before the job ran** (`beloniform_tree_input_ledger.json`): if Beloniformes
retain only the *b* paralog, the single `kcnh2`-like locus of `GCA_018398805.1` should group with
**medaka `kcnh2b`**.

**Confirmed, and it is the locus's single closest relative among all 20 reference proteins:**

```
(ZF_kcnh2a , (ZF_kcnh2b , (OL_kcnh2b , HSPEC_locus01)99.5/100 )97.5/99 )99.5/100
```

- flying-fish `locus01` + medaka `kcnh2b`: a **2-tip clade at 99.5/100**
- that pair + zebrafish `kcnh2b`: 97.5/99
- only then zebrafish `kcnh2a`: 99.5/100

**Sanity checks pass.** Medaka and zebrafish same-name paralogs pair as they should: `kcnh6a`
(99.3/100), `kcnh1b` (99.2/76), `kcnh7` (99.9/100), `kcnh4a` (98.8/99), `kcnh1a` (clade recovered,
support value not parsed). So the medaka sequences behave in this tree, which is what licenses
reading the `locus01` placement.

**Why the topology matters.** Zebrafish `kcnh2a` and `kcnh2b` are **not** sister to each other here:
zebrafish `kcnh2b` is closer to the two Beloniform genes than to zebrafish `kcnh2a`. That is the
signature of a duplication **predating** the zebrafish–Beloniformes split, with the Beloniform
lineage carrying the *b*-side copy — not of a cyprinid-specific duplication, which would have put
the two zebrafish genes together.

## The caveat this result immediately ran into

Takifugu rubripes, a non-Beloniform acanthomorph, has a single `kcnh2` gene that Ensembl names
**`kcnh2a`** (ENSTRUG00000010880), while medaka's single gene is named **`kcnh2b`**. The `a`/`b`
suffixes are therefore **per-species annotation labels, not orthology statements**, which makes the
earlier symbol-absence argument weaker than it looked and means the word "loss" is not yet earned:
the alternative is that the zebrafish `a`/`b` pair is narrower than assumed.

That is a control, not a cosmetic point, so it was run: `claude-zf2ff-outgroup-tree-1` adds the
Takifugu protein to this same tree. If it falls with zebrafish `kcnh2a`, the `a` copy existed in
acanthomorphs and the Beloniform lineage lost it. If it falls with the `kcnh2b`/Beloniformes clade,
"loss" is the wrong word.

## Scope

Medaka is a **proxy**: it is the nearest annotated Beloniformes genome, not a flying fish. A gene tree
places sequences by substitution likelihood; it does not prove orthology without synteny. The
flying-fish sequence is a miniprot prediction from an unannotated draft assembly, not a sequenced
transcript. One run, one operator, not independently reviewed.
