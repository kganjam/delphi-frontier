# Challenge 19: adversarial review of the PDB70 scope statement

**Claim under review** (the running agent's scope statement, not mine):
> "The no-homolog result is scoped to PDB70, a STRUCTURE database. It does not establish the absence of sequence homologs, and this workbench exposes no sequence-database search to test that."

Recorded evidence level: `unknown`. Value: n/a.

**Verdict: WEAKENED.** The main point holds: a PDB70 null does not rule out sequence homologs. But two of the claim's supporting statements are wrong or not checked.

## What I had to work with

- I searched this repository (`git grep`-style search for `pdb70|hhpred|hhblits|hhsearch|uniref|mmseqs|colabfold|workbench`) for the underlying search: the query, the tool, the E-value cut-off and the hit table. **None of it is in the repo**. The only matches were the unrelated substring "blast" in "blastema" or "blastomere" in `findings/gemini-triage-267-problems.json`. So I could not re-run or inspect the original no-hit search. Everything below about that search is my inference from how PDB70 is built and searched, not something I observed.
- There is no arithmetic in the claim, so check 1 has nothing to recompute.

## 1. "PDB70, a STRUCTURE database": mislabelled (proxy problem)

From the HH-suite documentation (read-level: my own background knowledge of the docs, not re-fetched in this session): PDB70 is a library of **profile HMMs**. Each one is built from the *sequence* of a PDB chain plus its MSA. The chains are clustered at a maximum of 70 % pairwise sequence identity. HHsearch/HHpred searches it by **profile–profile sequence comparison**, which can be boosted by secondary-structure scoring. It does not superpose 3-D coordinates. Foldseek or DALI against PDB/AFDB would be a true structure search.

So the quantity actually measured is: *no detectable sequence-profile homolog among proteins that have an experimental structure* (inference). The claim calls it a structure search. That matters for two reasons:
- A reader may think fold-level (structural-analog) similarity was ruled out. HHsearch does not test for structural analogs, so it is not.
- The real reason the null doesn't generalise is **database coverage** (only PDB-deposited proteins, redundancy-reduced), not the **search method**. The search method was already a sequence-homology method. The claim's conclusion is right, but its stated reason is wrong.

## 2. Hidden assumption: no sequence database was touched

In standard HHpred use, the query's profile is first built by an HHblits search against a large sequence database (UniRef30/UniClust30). Only then is PDB70 searched. If the workbench tool followed that pipeline, then:
- a sequence-database search **did** run, as a hidden intermediate step. Its MSA (number of sequences, Neff) would directly show whether sequence homologs exist, which contradicts the spirit of "no sequence-database search to test that";
- if instead the query was searched against PDB70 as a **single sequence** (no MSA), sensitivity drops a lot. In that case the PDB70 null is weaker than "no PDB homolog" too.

Which of the two happened is `unknown`, because the tool's parameters and output aren't recorded. The claim should say which.

## 3. "This workbench exposes no sequence-database search": not checked, and partly contradicted where I could test

The author gives no inventory of the workbench's tools, so this negative has no stated scope. I can't see the author's workbench. From this session's environment (2026-11-04, outbound through the agent proxy), I got:

| Endpoint | HTTP status | Read-level |
|---|---|---|
| `https://www.ebi.ac.uk/Tools/services/rest/ncbiblast/parameters` | 200; database list includes `uniprotkb`, `uniprotkb_swissprot`, `uniprotkb_trembl` | listing |
| `https://www.ebi.ac.uk/Tools/services/rest/hmmer3_phmmer/parameters` | 200 | listing |
| `https://rest.uniprot.org/uniprotkb/search?...` | 200 | listing |
| `https://blast.ncbi.nlm.nih.gov/Blast.cgi` | no response (000) | could-not-access |
| `https://toolkit.tuebingen.mpg.de/` (HHpred) | no response (000) | could-not-access |
| `https://search.foldseek.com/` | no response (000) | could-not-access |
| local `blastp`, `hhblits`, `hhsearch`, `mmseqs`, `jackhmmer`, `phmmer` | not on PATH | n/a |

These are **observations** (HTTP status codes and a parameter listing). I did **not** submit a BLAST or phmmer job: the query sequence isn't recorded in the repo, so there was nothing to submit. The checks show that, at least in this environment, a UniProtKB-wide sequence search (EBI NCBI-BLAST+ or phmmer REST) was reachable. If the author's workbench has the same network access, "no sequence-database search to test that" is false in practice. If it is limited to a fixed tool list, the claim needs that list as its scope. Either way, the statement is a tool-inventory claim with no inventory behind it.

## 4. Evidence level

`unknown` understates the problem, because the claim has two parts:
- "PDB70 null ≠ absence of sequence homologs": a **definitional/methodological** statement. It is correct, and it needs no measurement.
- "Workbench exposes no sequence search": an **unverified assertion** about tooling. It should be labelled as such, with a tool list as its scope.

## 5. Regime the author missed

Fast-evolving, lineage-restricted or orphan-like proteins (common in teleost fish after the teleost-specific whole-genome duplication) often have many sequence homologs in UniProt or Ensembl among fish and vertebrates, but none in PDB. Those are exactly the cases where a PDB70 null tells you the least (inference). The opposite case also exists: very divergent homologs with a known fold that only structure search (Foldseek) finds. HHsearch–PDB70 also misses those, so a PDB70 null rules out neither sequence homologs nor structural homologs.

## Corrected statement

> "No hit was found in PDB70: profile HMMs of PDB chains clustered at ≤70 % sequence identity, searched by HHsearch profile–profile comparison (query-MSA construction method: unknown; E-value cut-off: unknown). This rules out only *detectable sequence-profile homologs among proteins that have experimental structures*. It does not test sequence homologs in UniProt or genomes, and it does not test structural analogs (no Foldseek/DALI run). A UniProtKB search (EBI BLAST/phmmer) was reachable from at least one session environment but was not run."

```swarm-challenge
{"claim_id": 19, "outcome": "weakened", "reason": "The conclusion that a PDB70 null does not exclude sequence homologs is correct, but PDB70 is a sequence-profile HMM library of PDB chains searched by profile-profile comparison, not a structure search, and the claim that no sequence search was available is an unscoped, unverified tool assertion contradicted by EBI BLAST/phmmer REST endpoints returning HTTP 200 from this session.", "corrected_value": null}
```
