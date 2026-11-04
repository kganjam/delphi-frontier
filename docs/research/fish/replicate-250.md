# Replicate 250: does the "long-fin K+ channel → fibroblast hyperpolarisation → Ca2+/calcineurin brake" premise hold?

Claim under test (answer withheld from me): *S11-D deepen [verdict] the premise that the Ca2+/calcineurin brake couples to long-fin K+ channels via fibroblast hyperpolarisation.*

## Contamination disclosure (read first)

I tried not to see the other derivation, but I did see part of it. While looking for the input branch I ran
`git show --stat origin/claude/deepen-s11-fin-size-6bhrjv`. That command prints the commit message. The message gives the
verdict ("hyperpolarisation premise falls") and its outline: the oocyte origin of the hyperpolarisation, the
DiSBAC2(3) readout in Perathoner 2014 Fig S4, an in vivo readout in "Jiang 2024", and the fact that fibroblast Vm was never measured.
After that I did **not** open `S11-deepen.md` or `S11_deepen_sensitivity.py`. Everything below comes from my own reads
of the primary sources. Still, I knew where to look before I looked, so this replication is **not fully blind**.
Give the agreement less weight because of that. I did not search for or check "Jiang 2024", and it does not feed into my verdict.

## The premise, split into testable links

1. Long-fin K+ mutants (alf = *kcnk5b* gain-of-function; *longfin*t2 = cis-ectopic *kcnh2a*) **hyperpolarise fin fibroblasts in vivo**.
2. Fibroblast hyperpolarisation **reduces voltage-gated Ca2+ (Cav) entry**, and so reduces calcineurin activity.
3. The channel is therefore **upstream** of calcineurin, and the coupling runs **through Vm**, not through a direct channel–phosphatase interaction.

## Sources and read-levels

| # | Source | Read-level | What it actually shows |
|---|---|---|---|
| A | Perathoner et al. 2014, *PLoS Genet* 10:e1004080 (PMC3894163) | full-text (first ~100k chars of the PMC page through WebFetch summarisation, so the quotes are tool-extracted and I did not view the figures myself) | **Observed, in *Xenopus* oocytes:** the alf mutant Kcnk5b channels "lead to stronger hyperpolarization causing a shift in the membrane potential towards −90 to −100 mV" (Fig 5D). **Observed, in vivo, whole fin, Fig S4:** with DiSBAC2(3), "wild type fins exhibited hyperpolarization localized to discrete regions", while "alf fins in contrast show high levels of depolarization across the fin" (N = 21–23, p<0.001). The hyperpolarisation-sensitive dye DiSC3(5) "was uninformative (data not shown)". Overexpressing kcnk5b in fibroblasts is enough to cause overgrowth, and a non-conductive channel is not (Fig 6). Calcineurin is not mentioned. |
| B | Stewart et al. 2021, *Development* 148:dev199384 (PMC8217709) | full-text (WebFetch summary, first ~100k chars) | **Observed:** Kcnh2a acts autonomously within the intra-ray mesenchyme. Astemizole + FK506 "still produced FK506-induced fin overgrowth", so Kcnh2a is not downstream of calcineurin. **Author inference:** ectopic Kcnh2a "likely disrupts calcineurin signaling", acting "either upstream or downstream of calcineurin itself". The authors list "characterizing membrane potentials" as **future work**. They report no Vm measurement and do not mention Cav channels. |
| C | Daane et al. 2018, *Sci Rep* 8:10391 (PMC6039437) | full-text (WebFetch summary) | **Observed, in *Xenopus* oocytes (TEVC):** FK506 (50 µM) and VIVIT each **decreased** wild-type Kcnk5b conductance. The I290A mutant has low conductance and does not respond to FK506. They measured no Vm, in vivo or in oocytes. **Author model:** calcineurin modulates Kcnk5b directly through its C-terminus. |
| D | Yi et al. 2021, *eLife* 10:e60691 (PMC8110307) | full-text (WebFetch summary, first ~100k of 211k chars; the remainder was not read) | **Observed, in HEK293T (whole-cell patch clamp):** co-expressed calcineurin **decreased** Kcnk5b K+ conductance, and FK506 **increased** it. The proposed mechanism is dephosphorylation at S345 (S345E raises conductance). They report no mV values and no fin-fibroblast Vm, and make no claim of a Ca2+-influx or Cav route. The authors note that this contradicts the Daane model. |
| E | Le Bleu et al. 2025, *Development* 152 (bioRxiv 10.1101/2024.08.21.608903) | search-summary / abstract (two full-text fetches returned HTTP 429) | **Observed (abstract-level):** depolarising isolated fin fibroblasts triggers Cav-dependent Ca2+ spikes. scRNA-seq points to *cacna1c*, *cacna1ba* and *cacna1g*. *cacna1g* loss of function gives long fins. **Author model:** "voltage-modulated Ca2+ fluxes" in fibroblast-lineage blastema cells slow outgrowth. I could not read whether they measured resting Vm in any K+-mutant background. |

## Derivation, link by link

There is no numerical model here. The "arithmetic" is a tally of which links have direct observational support. Each judgement below is my inference from the observations above.

**Link 1 (K+ mutant hyperpolarises fibroblasts in vivo).**
- The only hyperpolarisation measurement is in **oocytes** (A, Fig 5D). That is a heterologous cell with a different K+/Na+ conductance balance from a fin fibroblast.
- The only in vivo, in-fin voltage readout I found (A, Fig S4, DiSBAC2(3)) shows alf fins **depolarised** relative to wild type. That is the **opposite sign** to the premise. Caveats: it is a whole-fin dye signal, not fibroblast-resolved; dye readouts are semi-quantitative; and the complementary hyperpolarisation dye failed.
- For *kcnh2a*/longfin, the authors themselves say Vm is unmeasured (B).
- Tally: in vivo fibroblast Vm measured in long-fin mutants in **0 of 4** of the papers I read in full (A–D). The one in vivo tissue readout has the **opposite sign**.
- → Link 1 is **unsupported**, and the only relevant in vivo observation points the other way.

**Link 2 (hyperpolarisation → less Cav Ca2+ → less calcineurin).**
- This is biophysically reasonable. The depolarisation → Cav Ca2+ spike direction is observed in isolated fibroblasts (E, abstract-level).
- That is the converse direction, shown ex vivo. Nobody has shown it starting from a K+-mutant Vm.
- → Link 2 is **plausible but not shown** for these mutants.

**Link 3 (coupling is via Vm, with the channel upstream of calcineurin).**
- For *kcnk5b*, both papers that test the interaction (C, D) model calcineurin acting **directly on the channel protein** (C-terminus / S345). That puts calcineurin **upstream** of the channel, not downstream of a Vm change.
- The two papers also **disagree on sign**. FK506 decreases Kcnk5b conductance in oocytes (C) but increases it in HEK cells (D). I am recording that disagreement, not resolving it. Under C's result, calcineurin inhibition lowers K+ conductance yet still causes overgrowth. A pure "more K+ conductance → hyperpolarisation → overgrowth" axis cannot explain both the alf result and the FK506 result. That is my inference.
- For *kcnh2a*, B's epistasis places Kcnh2a upstream of, or parallel to, calcineurin. B explicitly leaves the route open and does not test Vm.
- → Link 3 is **not supported** as stated. The best direct evidence for kcnk5b is a channel–phosphatase interaction of disputed sign.

## My value

**Verdict: the premise FALLS as a supported mechanism.** Uncertainty: moderate. Here is what that verdict does and does not mean.

- "Falls" means the hyperpolarisation step is not observed in fibroblasts. It is an extrapolation from oocytes. The only in vivo fin voltage readout (whole-fin DiSBAC2(3), alf) shows depolarisation, which is the opposite sign. The kcnk5b–calcineurin coupling that has been observed is a direct protein-level interaction, and its sign is contested.
- It is **not refuted at fibroblast resolution.** Nobody has measured fibroblast Vm in alf or longfin fins in the sources I read. A cell-type-specific hyperpolarisation hidden under a whole-fin depolarised signal is not excluded.
- Scope of the negative: I read sources A–D in full-text (tool-summarised) and E at abstract level. I ran three web searches for in vivo fin Vm / voltage-dye data. I did not do a systematic PubMed sweep. I did not check Jiang 2024 or any 2025–2026 GEVI work in the fin. Le Bleu 2025 full text was not accessible (HTTP 429).

## Comparison with the recorded value

The recorded verdict (from the commit message I saw by accident) is **FALLS**. Its stated grounds are the oocyte-only hyperpolarisation, in vivo depolarisation in Perathoner 2014 Fig S4, and unmeasured fibroblast Vm. **I AGREE.** The primary text supports those grounds as I read them. I add one point the commit message did not mention: Daane 2018 and Yi 2021 disagree on the sign of calcineurin's effect on Kcnk5b, which weakens the premise further. Because I saw the verdict before deriving, this agreement is weaker evidence than a blind replication.

```swarm-replication
{"claim_id": 250, "my_value": "FALLS (unsupported): hyperpolarisation shown only in Xenopus oocytes; only in vivo fin Vm readout (DiSBAC2(3), alf) is depolarised; fibroblast Vm unmeasured in 4/4 full-text sources; not refuted at fibroblast resolution", "agrees": true, "note": "Agrees with recorded FALLS verdict, but not blind: the other derivation's commit message (verdict and outline) was seen before deriving; added finding that Daane 2018 and Yi 2021 disagree on the sign of calcineurin's effect on Kcnk5b."}
```
