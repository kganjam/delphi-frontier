# Replicate 28 — is zebrafish and2 (actinodin 2) intrinsically disordered?

Claim under test (answer withheld from me): "and2 is NOT supported as intrinsically disordered",
with a sequence analysis by the running agent and kcnk5b at +0.166 as the positive control.

I did this derivation on my own. My repository search for `and2`/`kcnk5b` found only
`findings/gemini-triage-267-problems.json`. The one fragment I saw there was about Kcnk5b and cell
proliferation and had nothing on disorder. I did not read the rest of that file. I found no earlier
working for this claim.

## Result

**Whole-sequence FoldIndex of zebrafish and2 is +0.070 (full precursor, 508 aa) and +0.035
(signal peptide 1–23 removed, 485 aa).** These are *calculated* values, not observations. A positive
FoldIndex means the sequence falls on the "folded" side of the Uversky charge–hydropathy boundary. On
this metric and2 is therefore **not called disordered**, and that supports the claim as written.

Uncertainty: the formula is deterministic, so the only spread comes from input choices. Removing the
signal peptide moves the value from +0.070 to +0.035. That gives **+0.035 to +0.070 (dimensionless)**.
Both values sit close to the 0 boundary, so the call is marginal, not strong.

### Which metric the control implies (my inference)
I did not know the metric in advance. I identified it from the control value. Whole-sequence FoldIndex
(Prilusky et al. 2005, Bioinformatics 21:3435; formula as I recall it, read-level: not re-accessed in
this session) gives exactly **+0.1657 ≈ +0.166** for kcnk5b Q6PFU3. The Uversky distance
⟨H⟩b − ⟨H⟩ gives −0.060 for kcnk5b, which does not match. My conclusion that the recorded analysis used
whole-sequence FoldIndex is an **inference**, based only on this match.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| and2 sequence | A9JRX1 (508 aa); A0ACM8QEN9 is identical | UniProt REST `rest.uniprot.org/uniprotkb/A9JRX1.fasta` (taxon 7955, gene_exact:and2) | full-text (sequence record) |
| kcnk5b sequence | Q6PFU3 (448 aa); A0A8M1PBI1 is identical | UniProt REST | full-text (sequence record) |
| Kyte–Doolittle scale | standard values, rescaled (KD+4.5)/9 to the 0–1 range | Kyte & Doolittle 1982 (from memory) | could-not-access (not re-fetched) |
| FoldIndex formula | FI = 2.785⟨H⟩ − \|⟨R⟩\| − 1.151 | Prilusky 2005 / Uversky 2000 boundary (from memory) | could-not-access (not re-fetched) |
| and2 signal peptide | residues 1–23 (my assumption from the hydrophobic N-terminus, "precursor" in the name) | my inference | — |

## Arithmetic (calculated)

⟨H⟩ = mean of (KD+4.5)/9 over the sequence; ⟨R⟩ = (K+R − D−E)/N.

- **kcnk5b Q6PFU3**: N=448, K+R=58, D+E=47 → ⟨R⟩=11/448=0.0246; ⟨H⟩=0.4816.
  FI = 2.785×0.4816 − 0.0246 − 1.151 = 1.3412 − 0.0246 − 1.151 = **+0.1657**. This matches the stated control.
- **and2 A9JRX1 (full)**: N=508, K+R=56, D+E=63 → ⟨R⟩=−7/508=−0.0138; ⟨H⟩=0.4434.
  FI = 2.785×0.4434 − 0.0138 − 1.151 = 1.2349 − 0.0138 − 1.151 = **+0.0700**.
- **and2 mature (24–508)**: N=485, ⟨R⟩=−0.0165, ⟨H⟩=0.4319 → FI = 1.2028 − 0.0165 − 1.151 = **+0.0353**.

### Windowed check (calculated, FoldIndex with a 51-aa window, the standard FoldIndex window)

| Sequence | windows with FI<0 | residues covered by a FI<0 window | min window FI |
|---|---|---|---|
| kcnk5b (full) | 147/398 (36.9 %) | 272/448 (60.7 %) | −0.331 |
| kcnk5b C-tail (256–448) | 118/143 (82.5 %); whole-segment FI −0.161 | 193/193 | −0.331 |
| and2 (full) | 178/458 (38.9 %) | 298/508 (58.7 %) | −0.368 |
| and2 mature | 169/435 (38.9 %) | 289/485 (59.6 %) | −0.368 |

## Caveats (read these before using the claim)

1. **kcnk5b at +0.166 does not work as a positive control for disorder.** On FoldIndex a positive value
   means "folded". So the control lands on the *same* side as and2. kcnk5b is a multi-pass
   membrane channel, and its global FoldIndex is pulled up by the transmembrane helices. Its C-terminal tail
   (residues 256–448, a boundary I chose) scores −0.161 on its own, which is disordered. Inference: the
   whole-sequence metric cannot detect a disordered region inside a protein that is otherwise
   hydrophobic. A control that sits on the same side as the test case cannot tell the two apart.
2. **In the windowed profile, and2 looks like kcnk5b, not like a folded protein.** The share of windows
   below 0 is about 39 % for and2 and 37 % for kcnk5b. and2 also has the deeper minimum (−0.368). So
   "NOT supported as intrinsically disordered" holds for the *global* score only. It does **not** show
   that and2 lacks disordered regions. A windowed reading would support "partially disordered", about
   as much as for kcnk5b.
3. FoldIndex is a composition heuristic. I did not run a trained predictor. I tried to pip-install
   metapredict, but the install did not finish within the session limits and I abandoned it. I did not run
   IUPred or AlphaFold pLDDT.
4. Negative-search scope: I did no literature search on actinodin disorder. The only repository search
   was a grep for `and2`/`kcnk5b`. I make no claim about published experimental disorder data for and2.
   Status: `unknown`.

## Comparison with the recorded value

I could not find the recorded and2 value in the repository. The only hit was a triage JSON that I
deliberately did not read in full. The claim text gives only the verdict ("NOT supported") and the
control (+0.166). I reproduced the control exactly (+0.1657). The metric that does so gives and2 a
positive value (+0.070), which matches the verdict. **AGREE on the verdict.** I CANNOT TELL whether the
recorded and2 number is +0.070, because that number is not available to me. I add caveats 1–2: the
verdict holds only for the global score, and the control does not test what it is said to test.

```swarm-replication
{"claim_id": 28, "my_value": "whole-sequence FoldIndex +0.070 (full precursor) / +0.035 (mature), dimensionless; calculated, folded side of 0", "agrees": true,
  "note": "Reproduced the kcnk5b control exactly as whole-sequence FoldIndex (+0.1657), and and2 is also positive so it is not called disordered, but kcnk5b is a folded-side score rather than a true disorder control, and windowed FoldIndex shows and2 has about as many disorder-prone windows (39%) as kcnk5b (37%)."}
```
