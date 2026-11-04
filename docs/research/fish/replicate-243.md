# Replication 243: is there a measured fin-mesenchyme Vmem behind the bioelectric fin-size mechanism?

**Claim, with the answer removed:** "The published bioelectric mechanism therefore has an UNSATISFIED
EXISTENCE CONSTRAINT at its centre."

**How I worked:** I re-derived this from primary papers. I did not see the original derivation.
- I searched the working tree and both branches (`claude/bioelectric-existence-constraint-8st1ge` and
  `work/frontier-foundation`) for `bioelectric`, `GXL`, `existence constraint`, `kcnk5b`, `kcnh2a` and
  `longfin`.
- The only hits were `findings/gemini-triage-267-problems.json` (a triage verdict on the problem
  `bioelectric-fin-size`) and `findings/README-no-gpu-problem.md`. Neither has the original working or
  its number, so I had nothing to stop reading.
- I could not find any definition of the "GXL check" in this repository, so I do not know what it is.
  I did not reproduce it.

## What I take the existence constraint to be (my inference)

**What the mechanism says (the authors' claim):** a K+ channel changes the membrane potential (Vmem)
of intra-ray fin mesenchyme, and that changed Vmem sets fin size. The channels are Kcnk5b in *alf*
and Kcnh2a in *longfin*.

**What it therefore requires (my inference):** a Vmem change in fin mesenchyme, in vivo, of the
predicted sign. The constraint is met only if that Vmem state has been shown to exist. So the quantity
I derive is the number of published quantitative (mV) in vivo measurements of fin-mesenchyme Vmem in
these mutants, plus whether the sign agrees with the prediction.

## Inputs

| # | Input | Source | Read-level |
|---|---|---|---|
| 1 | *alf* gain-of-function Kcnk5b "lead[s] to stronger hyperpolarization causing a shift in the membrane potential towards −90 to −100 mV". This was measured in **Xenopus oocytes**, not fin cells. | Perathoner et al. 2014, *PLoS Genet* 10:e1004080, PMC3894163 | full-text (read via a fetch summarizer; sentences quoted) |
| 2 | In vivo DiSBAC2(3) dye on juvenile caudal fins, Fig. S4: wild-type fins showed "hyperpolarization localized to discrete regions", while "*alf* fins in contrast show high levels of **depolarization** across the fin". The output is fluorescence only, with no mV values. DiBAC4(3) gave "similar effects". DiSC3(5) was "uninformative". | Perathoner 2014, Fig. S4 legend and Methods | full-text (quoted) |
| 3 | The authors themselves write: "we cannot exclude that this, in turn, triggers a depolarization… experiments employing depolarization-sensitive dyes, suggest that this might indeed be the case". | Perathoner 2014, Discussion | full-text (quoted) |
| 4 | *longfin* = cis-ectopic *kcnh2a*. No Vmem was measured. The authors list "characterizing membrane potentials" among the "Key next steps". | Stewart et al., bioRxiv 790329 v1 (published in *Development* 148:dev199384, 2021) | full-text, first 100k characters of the preprint |
| 5 | Calcineurin–Kcnk5b scaling: patch clamp in **HEK293T** cells only. The paper states hyperpolarization as the expected consequence of channel opening and reports no in vivo Vmem and no mV values. | Yi et al. 2021, *eLife* 10:e60691 | full-text, first 100k characters |
| 6 | Blastema Ca2+ / voltage-gated channel work: the abstract says "potential origins from dynamic membrane voltages have not been explored". The abstract gives no mV values. | bioRxiv 2024.08.21.608903, PMC11370486 | abstract |

## Arithmetic

| Paper | Quantitative in vivo fin-mesenchyme Vmem measurements |
|---|---|
| Perathoner 2014 | 0 (oocytes only; the in vivo dye result is qualitative) |
| Stewart 2021 | 0 |
| Yi 2021 | 0 (HEK293T only) |
| 2024 Ca2+ preprint | 0, as far as the abstract shows |
| **Total** | **0** |

- **Predicted sign:** *alf* should be **hyperpolarized**, by roughly −90 to −100 mV in oocytes. This is a
  heterologous-expression result. It is not a fin observation.
- **Only in vivo readout of sign:** *alf* fins look **depolarized**. This is a qualitative dye
  observation.
- **Result:** the predicted and observed directions are opposite (−1 versus +1), so the signs disagree.

## My value

**Zero quantitative in vivo measurements of intra-ray-mesenchyme Vmem exist in the four papers above.**
- The single qualitative in vivo readout (Perathoner 2014, Fig. S4) has the opposite sign to the
  oocyte-based prediction.
- So the Vmem state the mechanism needs has not been shown to exist in fin tissue, in either sign.
- On this evidence, I find the existence constraint unsatisfied.

**Uncertainty:**
- **Scope of the negative search:** the four papers above plus three web searches, run 2026-11-04.
  The searches covered GEVIs and voltage dyes in adult zebrafish fins, DiBAC with fin regeneration
  with *kcnh2a*, and *alf*/*kcnk5b*. Each was a single English-language search. I did not read the last
  18–96k characters of the three long papers.
- A mV-level fin measurement could exist in literature outside this scope.
- **Disagreement I am keeping, not resolving:**
  - The oocyte data say the mutant hyperpolarizes.
  - The fin dye data say it depolarizes.
  - The authors themselves offer a secondary depolarization as one possible reconciliation. That is
    their hypothesis. It has not been measured.

## Comparison with the recorded value

**CANNOT TELL.**
- I could not find the recorded value or the original working anywhere in this repository (scope: see
  "How I worked" above).
- Qualitatively, my result supports the claim's wording, an unsatisfied existence constraint. But I
  cannot check it against the specific number the claim used, and I do not know what its "GXL check"
  computed.

```swarm-replication
{"claim_id": 243, "my_value": "0 quantitative (mV) in vivo fin-mesenchyme Vmem measurements; sole qualitative in vivo readout (alf, DiSBAC2(3)) shows depolarization vs oocyte-predicted hyperpolarization to -90 to -100 mV", "agrees": null,
  "note": "Independently the constraint looks unsatisfied (no measured Vmem, and a sign conflict in Perathoner 2014), but the recorded value and the GXL check were not findable in the repo, so I cannot compare numbers."}
```
