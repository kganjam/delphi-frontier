# Replicate 26: independent re-derivation (negative result)

**Claim under test (answer withheld from me):** "An MSA-dependent model's confidence tracks ALIGNMENT
DEPTH, not disorder." The stated inputs were "recomputed here from the ESMFold2 CIF; MSA depth profile from
the running agent."

## My value

**unknown.** I could not derive a number because neither input was available to me. This is a negative
result. It is not an estimate.

## What I tried (scope of every negative search)

| Input needed | Where I looked | Result | Read-level |
|---|---|---|---|
| ESMFold2 CIF (per-residue pLDDT in the B-factor column) | `git ls-files` for the whole working tree (51 files); filename filter `esm\|fold\|plddt\|cif\|pdb`; `find . -iname '*.cif*'` | No structure file of any kind | could-not-access (absent) |
| MSA depth profile (per-residue alignment depth) | filename filter `msa\|a3m\|depth`; `find` for `*msa*` / `*a3m*` | Absent | could-not-access (absent) |
| The protein / UniProt accession the claim is about | the question text; ripgrep over the tree for `alignment depth\|ESMFold\|msa depth\|pLDDT` (case-insensitive) | No match. The question does not name the protein. | could-not-access |
| The prior derivation or the recorded value | `git log --all` (30 commits, branches `claude/msa-confidence-rederivation-q72vhs` and `work/frontier-foundation`): commit-message grep for `msa\|esmfold\|plddt\|claim 26\|alignment depth`; every path ever committed, filtered for `fish\|esm\|cif\|msa\|replic` | No match. `docs/research/fish/` did not exist before this file. I did not see the other agent's working. | could-not-access |

The MSA depth profile is said to come "from the running agent". That is session state from another process.
It was never committed, and I can't reach it from this container. Without the protein's identity, I couldn't
regenerate either input myself, for example by rerunning a fold or an MSA search: I wouldn't know what sequence
to submit.

## Arithmetic

None was performed. Had the inputs been present, the test I planned was this:
1. Per-residue pLDDT from the CIF B-factor column (CA atoms).
2. Per-residue MSA depth (non-gap sequences per column), log-transformed.
3. A per-residue disorder proxy (for example, an IUPred-style score or a pLDDT-independent disorder
   predictor). It must not be pLDDT itself, or the comparison is circular.
4. Spearman ρ(pLDDT, log depth) against ρ(pLDDT, disorder), plus a partial correlation of pLDDT with depth
   controlling for disorder. The claim holds only if the partial correlation stays substantial.

Any number from this test would be **calculated**, not observed.

## A substantive concern with the claim as worded (my inference, not a measurement)

- The claim calls the model "MSA-dependent", but the confidence comes from an "ESMFold2 CIF". Background
  knowledge (not re-read in this session, read-level: none): ESMFold, as published (Lin et al., *Science*
  2023), is a single-sequence predictor driven by a protein language model. It takes no MSA at inference. I
  cannot confirm that a model called "ESMFold2" exists or how it works (`unknown`, not searched).
- If the model is MSA-free, a correlation between its pLDDT and an external MSA depth profile would not show
  that "confidence tracks alignment depth" by mechanism. Both quantities plausibly co-vary with evolutionary
  conservation and with disorder, since disordered regions align poorly. That is exactly the confound the
  claim says it rules out. My inference: the claim needs the partial-correlation control in step 4 above
  before it can be accepted, whatever the recorded value is.

## Comparison with the recorded value

Not found (scope: this repository, all branches and history). **CANNOT TELL.**

```swarm-replication
{"claim_id": 26, "my_value": "unknown (inputs absent: no ESMFold2 CIF, no MSA depth profile, protein not named)", "agrees": null,
  "note": "Neither the CIF nor the MSA depth profile is in the repo or its history and the protein is unnamed, so no independent value could be derived; also, ESMFold-family models are single-sequence, which undercuts the 'MSA-dependent' framing unless disorder is partialled out."}
```
