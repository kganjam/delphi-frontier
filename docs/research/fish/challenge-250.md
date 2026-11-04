# Challenge 250: adversarial review of the S11-D "hyperpolarisation premise falls" claim

**Claim under review** (claim_id 250, source `claude/deepen-s11-fin-size-6bhrjv:docs/research/fish/S11-deepen.md`).
The claim says S11-D deepening **FALLS** the premise that the Ca²⁺/calcineurin brake couples to long-fin K⁺
channels through fibroblast hyperpolarisation. Its grounds:

- Hyperpolarisation was measured only in *Xenopus* oocytes (to −90 to −100 mV, at about 2× gK).
- The in vivo DiSBAC2(3) readouts (Perathoner 2014 Fig S4, N = 21–23; Jiang 2024) show depolarisation.
- Fibroblast Vm has never been measured.

The claim says the calcineurin brake itself stands. It says S11-D is *consistent* with the claim-167
challengers on Fig S4 but *conflicts* with them on whether a sign disagreement exists. In the claim's words,
"they say none; this says the sign is unresolved vs oocyte". Recorded evidence level: derived. Value: n/a mV
(unknown).

**My verdict: WEAKENED.** The scientific core survives every check I ran. The oocyte-only hyperpolarisation,
the in vivo dye depolarisation, the N, and the absence of any fibroblast Vm all hold up against the primary
text. The claim's cross-reference to the claim-167 challengers does not hold. It reports a conflict that
those documents do not contain: both challengers say the in vivo sign is open, which is the claim's own
position. A second, smaller defect is the verb "FALLS". It is stronger than the evidence, because whole-fin
dye readouts leave fibroblast hyperpolarisation *untested*, not contradicted. The source document concedes
this in its last paragraph.

Labels used throughout: **measured** (a source recorded it), **calculated** (I computed it), **inference**
(my reasoning, not a source's claim).

---

## 1. Arithmetic, redone independently

I wrote my own implementation with the same *assumed* parameters (scratch script, not committed). The
parameters are E_K = −90, E_other = 0, E_Ca = +60 mV, plus a generic m∞²·h∞ window with V_act = −45/k 6 and
V_inact = −75/k 5. They are assumptions, not zebrafish Cacna1g measurements, and the source says so. All
results below are **calculated**.

- **Parallel-conductance Vm, closed form.** Vm = f·E_K / (f + (1−f)) with E_other = 0, so Vm₀ = −90·f.
  Doubling gK gives f′ = 2f/(1+f).
  - f = 0.3 → −27.0 → −41.5 mV
  - f = 0.5 → −45.0 → −60.0 mV
  - f = 0.7 → −63.0 → −74.1 mV
  - f = 0.9 → −81.0 → −85.3 mV

  All four match the source.
- **Ca²⁺ drive change.** +864.8 %, −49.5 %, −84.1 %, −71.2 %. These match the source's +865 / −49.5 /
  −84.1 / −71.2 %.
- **Window peak.** −48.07 mV. Across the 3×3 sweep of V_act and V_inact it ranges from −58.0 to −38.1 mV.
  This matches the source's "about −48, moving −38 to −58".
- **Sign-flip table at ±10 mV.**
  - Vm₀ = −80: −95 % / +834 %
  - Vm₀ = −60: −75 % / +106 %
  - Vm₀ = −40: +53 % / −79 %

  All match.

**No arithmetic fault.** The claim records "n/a mV (unknown)" for the in vivo ΔVm, and that is correct.
No source gives an mV value for fin cells (§4).

## 2. Primary-source check of the factual legs

**Perathoner et al. 2014, *PLoS Genet* 10:e1004080, PMC3894163.** Read-level: full-text (Europe PMC
fullTextXML, keyword-scanned).

- **Oocytes.** The paper reports "an almost two-fold increase in K⁺ conductance". It also says "the mutant
  channels lead to stronger hyperpolarization causing a shift in the membrane potential towards −90 to
  −100 mV, the equilibrium potential for K⁺ in Xenopus oocytes". Per Fig 5D, the oocyte Vm values were
  measured and correlated with the current at +50 mV. "~2× gK" and "−90..−100 mV" are faithful.
  - One nuance, which is my inference: the comparison is mutant vs **WT-Kcnk5b-injected** oocytes. Both
    groups are already K⁺-leak-dominated, so the ~2× ratio is not a fin-cell number.
- **Fig S4 legend.**
  - WT: "hyperpolarization localized to discrete regions of the fin".
  - *alf*: "high levels of depolarization across the fin with variable patterns in different tissues".
  - Statistics: "***: p<0.001, N = 21–23".
  - Methods: juvenile fish at 16–18 mm SL, average pixel intensity of whole-fin maximum projections, and a
    150 mM KCl positive control. DiSC3(5) was "uninformative".

  **N = 21–23 is verified.**
- **Discussion.** The authors write: "we cannot exclude that this, in turn, triggers a depolarization …
  experiments employing depolarization-sensitive dyes, suggest that this might indeed be the case
  (Figure S4)."

**Jiang et al. 2024, *PLoS Biol* 22:e3002565, PMC11018282.** Read-level: full-text (Europe PMC
fullTextXML, keyword-scanned).

- The readout is DiSBAC2(3) by photon counting, which the authors call "relative differences in membrane
  potential".
- Pectoral fin buds at 32–56 hpf; *kcnk5b*-mCherry overexpression "significantly increased
  depolarization".
- The hyperpolarise-then-Na⁺ route is explicitly a proposal: "We propose that the increased K⁺-channel
  activity first hyperpolarizes …".

The claim characterises both sources correctly.

## 3. Proxy and hidden assumption

- **Proxy.** "In vivo depolarisation" rests on whole-fin DiSBAC2(3) mean intensity, which is a relative
  proxy with no mV calibration. The quantity that matters is the resting Vm of fibroblast-lineage blastema
  cells in *alf*/+ and *lof*/+. The claim names this correctly as unmeasured. **This is not a defect in the
  claim.**
- **Hidden assumption, tested relaxed.** The word "FALLS" implicitly assumes that the whole-fin
  depolarisation bears on fibroblast Vm. Relax that assumption and allow the dye signal to be dominated by
  epidermis or other tissues, as "variable patterns in different tissues" invites. Then a whole-fin
  depolarisation is fully **compatible** with fibroblast hyperpolarisation.
  - Under that relaxation the in vivo data neither support nor contradict the premise. The premise is
    **untested**, not refuted (inference).
  - The source document says so itself: "it does not show the hyperpolarisation model is wrong. It shows
    the model has not been tested where it would need to be."
  - So the defensible reading is "falls *as an established premise*". The bare headline "FALLS the
    premise" overstates it, and I count that as a wording defect.
- **A mechanism the claim does not mention.** Jiang 2024 report that Kcnk5b lowers intracellular K⁺ (KIRIN
  FLIM, relative). Sustained K⁺ loss makes E_K less negative. That could depolarise steady-state Vm even
  without Na⁺-channel recruitment. This is my inference and was not tested by anyone. It is a third way the
  oocyte and in vivo signs could both be true, and it strengthens the claim's "sign unresolved" point
  rather than weakening it.

## 4. The cross-reference to the claim-167 challengers is wrong

I read both challenge-167 files: `origin/claude/challenge-kcnk5b-claim-6ey3si` and
`origin/claude/challenge-kcnk5b-claim-trw1cg`, both at `docs/research/fish/challenge-167.md`. Read-level:
full-text.

- They reject an *inter-paper* sign conflict, Perathoner vs Jiang. They do **not** reject a sign
  disagreement as such.
- Both locate the tension as **oocyte vs fin, inside Perathoner 2014**, and both preserve it as open:
  - trw1cg §3: "the disagreement is … between preparations — heterologous oocyte vs in vivo fin". Also:
    "the steady-state pectoral Vm in absolute mV remains unmeasured by anyone".
  - 6ey3si §3: "the *magnitude and sign of the immediate in-vivo Kcnk5b effect remains genuinely open*".
    Its summary repeats: "The underlying in-vivo sign question does remain open — that part I preserve."

S11-D's position is that the sign is unresolved between oocyte and in vivo. That is the **same position**.
The claim's "CONFLICTS with them … (they say none …)" misreads them. There is agreement on every point
checked, and the reported conflict is an artefact of the claim. This is the main reason for WEAKENED, not
refuted: it is a fault in the claim's account of the record, not in its science.

## 5. Counter-examples and regimes missed

**Negative search for any measured fin-cell Vm.** Scope:

- Web search (extended) for zebrafish fin regeneration plus membrane potential, blastema, fibroblast,
  voltage imaging, kcnk5b, kcnh2a.
- Web search for GEVI plus caudal fin regeneration plus resting potential.
- Europe PMC full-text scans of Perathoner 2014, Jiang 2024, and Silic et al. 2020 (*Genetics*,
  PMC7404225).

Result: **no mV value for fin cells in vivo.**

- Silic 2020 recorded resting potentials only in transfected **HEK293T** cells.
- Lanni et al. 2019 (*Dev Biol* 456:164, *kcc4a*/schleier): I found no Vm measurement. Read-level:
  search-summary.
- A ResearchGate snippet mentioned an "ASAP1" voltage-sensor line in connection with fin regeneration. I
  could not confirm it: the string "ASAP" does not appear in the Silic 2020 full text. Status: **unknown**.

The claim's "fibroblast Vm never measured" survives within this scope.

**A regime the claim does not mention: Silic et al. 2020.** Read-level: full-text, keyword-scanned.

- The long-fin *kcnj13* Dhi2059 allele acts through ectopic expression in the **dermomyotome during
  embryogenesis**, not in fin fibroblasts.
- Long fins were not re-established by the transgene during adult regeneration (data not shown).
- Ectopic *kcnk9*, *kcnj1b*, *kcnj10a* and human *KCNJ13* also produced long fins. *kcna1a* did not.

This adds a third cell compartment to S11-D's fibroblast-vs-keratinocyte disagreement. It does not break
the claim. It shows the K⁺ → fin-size coupling is not confined to one cell type, which further undercuts
any single "fibroblast hyperpolarisation" chain (inference).

## 6. Is the evidence level honest?

Recorded as "derived, n/a mV (unknown)". That is honest:

- The claim offers no number as measured.
- Its factual legs are other people's measurements, quoted correctly.
- Its sensitivity model is labelled calculated in the source.

"Not re-run" is accurate, since this is desk research.

## 7. What stands

- **Stands:**
  - The premise "long-fin K⁺ alleles hyperpolarise fin fibroblasts" is **not established**.
  - Hyperpolarisation is measured only in oocytes. The in vivo fin readouts (relative dye, whole fin or
    bud) show depolarisation. Fibroblast Vm is unmeasured.
  - The Ca²⁺/calcineurin brake is supported independently.
- **Corrected:**
  - "FALLS" should read "unestablished / untested in the relevant cells". The in vivo data do not
    contradict fibroblast hyperpolarisation, because they never resolved fibroblasts.
  - The claim-167 relation is **agreement**, not conflict.

## Sources and read-levels

- Perathoner S. et al. 2014. *PLoS Genet* 10:e1004080. PMC3894163. Full-text (keyword-scanned XML).
- Jiang X. et al. 2024. *PLoS Biol* 22:e3002565. PMC11018282. Full-text (keyword-scanned XML).
- Silic M.R. et al. 2020. *Genetics*. PMC7404225, PMID 32546498. Full-text (keyword-scanned XML).
- Lanni J.S. et al. 2019. *Dev Biol* 456:164–178. Search-summary.
- challenge-167.md on branches `claude/challenge-kcnk5b-claim-6ey3si` and `claude/challenge-kcnk5b-claim-trw1cg`.
  Full-text.
- S11-deepen.md and S11_deepen_sensitivity.py on `claude/deepen-s11-fin-size-6bhrjv`. Full-text.

```swarm-challenge
{"claim_id": 250, "outcome": "weakened", "reason": "The scientific core is verified: hyperpolarisation was measured only in Xenopus oocytes, DiSBAC2(3) depolarisation in alf fins (p<0.001, N=21-23) and Kcnk5b-overexpressing buds checks out against the full text, and no fin-cell Vm exists in my search scope. The claimed CONFLICT with the claim-167 challengers is false, since both explicitly hold that the in vivo sign is open and that the tension is oocyte vs fin, which is S11-D's own position. 'FALLS' overstates whole-fin dye data that leave fibroblast hyperpolarisation untested rather than contradicted.", "corrected_value": null, "depends_on": ["Perathoner2014-PMC3894163 Fig5/text: almost two-fold K+ conductance increase, oocyte Vm shift towards -90 to -100 mV vs WT-Kcnk5b oocytes (measured, heterologous)", "Perathoner2014-PMC3894163 Fig S4 legend: alf whole-fin DiSBAC2(3) depolarisation, p<0.001, N=21-23, juvenile 16-18 mm SL, uncalibrated (measured, proxy)", "Jiang2024-PMC11018282: kcnk5b-mCherry overexpression increased DiSBAC2(3) depolarisation in pectoral fin buds; hyperpolarise-then-Na+ route stated as a proposal; Kcnk5b lowers relative intracellular K+", "challenge-167.md (branch claude/challenge-kcnk5b-claim-trw1cg) section 3: oocyte-vs-fin disagreement and in vivo mV unmeasured", "challenge-167.md (branch claude/challenge-kcnk5b-claim-6ey3si) section 3 and summary: in vivo sign remains genuinely open", "Silic2020-PMC7404225: kcnj13 Dhi2059 long fin via embryonic dermomyotome; resting Vm measured only in HEK293T", "negative search scope: web (extended + standard) and Europe PMC full-text scans listed in section 5, finding no in vivo fin-cell Vm in mV", "S11_deepen_sensitivity.py assumed parameters (E_K -90, E_other 0, E_Ca +60 mV, generic T-type window), recomputed independently (calculated)"]}
```
