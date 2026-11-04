# Challenge 264: adversarial review of the S11-D claim that "the fibroblast-hyperpolarisation coupling falls"

**Claim under review** (claim_id 264; source `harvest:deepen-s11-fin-size-6bhrjv`, which is
`origin/claude/deepen-s11-fin-size-6bhrjv:docs/research/fish/S11-deepen.md`):

> The Ca²⁺/calcineurin brake on fin outgrowth stands (cacna1g LOF, FK506, Cav blockers). Its claimed
> coupling to long-fin K⁺ channels through fibroblast hyperpolarisation falls as an established premise.
> Hyperpolarisation was measured only in *Xenopus* oocytes. The only in vivo fin readouts (DiSBAC2(3),
> Perathoner 2014; Jiang 2024) show depolarisation. Fibroblast resting Vm has never been measured.
> KEY: in vivo fin-cell ΔVm for alf/lof is unknown in mV. Its sign by DiSBAC2(3) in whole fin is
> depolarising (relative fluorescence, p<0.001, N=21–23). Oocyte ΔVm is toward −90 to −100 mV with ~2× gK.
> VERDICT: falls.

Recorded evidence level: **measured**. Value: n/a.

**My verdict: WEAKENED.** The scientific core survived every check I could run, as it did for the
earlier review of the same text (challenge 250, branch `claude/challenge-s11-deepen-claim-rs0sro`) and
the replication (replicate-250, branch `claude/rederive-s11-deepen-fin-size-uy1pio`). I read both before
writing this. I found one new source that strengthens the core. The defects are these:

- **D1.** The evidence level is wrong. "Measured" is recorded for what is a literature synthesis plus a
  bounded negative search. Challenge 250 judged the same text and recorded it as "derived".
- **D2.** The KEY extends the in vivo depolarising sign to *lof*. It was observed only for *alf*.
- **D3.** "The only in vivo fin readouts" is true only if scoped to long-fin K⁺ alleles. A 2025/2026
  in vivo fin voltage-imaging study exists that the claim does not cite.
- **D4.** "Cav blockers" (plural) stands on one drug tested in vivo.

None of these defects changes the conclusion that the hyperpolarisation link is unestablished.

Labels used: **measured** (a source recorded it), **calculated** (I computed it), **inference** (my
reasoning, not a source's claim), **assumed** (an input I chose).

---

## 1. Arithmetic, redone independently

The claim contains only two numerical statements. I recomputed both from first principles, not from the
author's working. My script was run inline and not committed.

**(a) Is "toward −90 to −100 mV" plausible as an oocyte E_K?** I used Nernst at 20 °C with
[K⁺]ₒ = 2 mM. The bath value is an **assumed** ND96 composition; Perathoner's bath was not re-read for
this. [K⁺]ᵢ is **assumed** and swept. Results are **calculated**:

| [K⁺]ᵢ | E_K |
|---|---|
| 90 mM | −96.2 mV |
| 110 mM | −101.2 mV |
| 130 mM | −105.4 mV |

This range matches the authors' description of −90 to −100 mV as "the equilibrium potential for K⁺ in
*Xenopus* oocytes". A Kcnk5b-injected oocyte, dominated by K⁺ leak, sitting near E_K is the expected
result. It says nothing about a fin cell (inference).

**(b) What does "~2× gK" do to Vm?** I used a parallel-conductance model with E_K = −90 and
E_other = 0 (both **assumed**), so Vm₀ = −90·f and doubling gK gives f′ = 2f/(1+f). Results are
**calculated**:

| f | Vm₀ | Vm after ×2 gK | ΔVm |
|---|---|---|---|
| 0.3 | −27.0 | −41.5 | −14.5 mV |
| 0.5 | −45.0 | −60.0 | −15.0 mV |
| 0.7 | −63.0 | −74.1 | −11.1 mV |
| 0.9 | −81.0 | −85.3 | −4.3 mV |

These values agree with the source's sensitivity table. The point that matters (inference) is this: in
a steady state with fixed ionic gradients, adding K⁺ conductance can only move Vm toward E_K. The
oocyte "hyperpolarisation" is therefore the default biophysical expectation, not an anomaly. That is
exactly why the in vivo depolarising readouts need an extra mechanism, and why that mechanism (Na⁺
recruitment per Jiang 2024, or K⁺ depletion raising E_K per challenge 250) is the unmeasured crux.

**No arithmetic fault.**

## 2. Proxy check

- **Proxy in the KEY:** "sign by DiSBAC2(3) in whole fin". This is an uncalibrated mean pixel intensity
  of whole-fin maximum projections, in **juvenile, non-regenerating** fins (16–18 mm SL). Read-level:
  full-text (Perathoner 2014 Fig S4 legend and Methods, via WebFetch).
- **The quantity that matters:** resting Vm, and ΔVm, of fibroblast-lineage blastema cells during
  *regenerative* outgrowth. That is the regime where the calcineurin, cacna1g and cilnidipine evidence
  was gathered.
- The claim names this proxy honestly, writing "unknown in mV" and "relative fluorescence". **That is
  not a defect.**
- **What the claim leaves out:** a stage and regime mismatch. Fig S4 measures ontogenetic juvenile
  growth, while the brake evidence is from regeneration (Le Bleu 2025: cilnidipine 5–28 dpa). This
  further weakens any bridge from the dye data to the brake, in either direction (inference). It
  strengthens "not established", so it does not break the claim.
- **Unstated detail:** Perathoner Fig S4 also reports that *"DiBAC4(3), another dye sensitive to
  depolarization, showed similar effects"*. So the *alf* in vivo signal is concordant across two oxonol
  dyes, not one. That modestly strengthens the claim's sign statement. Both are the same class of
  redistributive dye, so they share the same tissue-uptake confound (inference).

## 3. Hidden assumption, tested relaxed

The load-bearing assumption is that whole-fin, depolarisation-sensitive dye signal says something about
fibroblast Vm. Relaxing it is easy, because Perathoner write that the *alf* signal has "variable patterns
in different tissues". Without the assumption, the in vivo data neither confirm nor contradict fibroblast
hyperpolarisation (inference).

The claim survives this relaxation only because it is worded "falls **as an established premise**". It
does not say "is refuted". The headline "VERDICT: falls", stripped of that qualifier, would overstate it.
Challenge 250 made the same point and I concur. I do not count it again as a new defect.

## 4. Evidence level: not honest (D1)

The recorded level is **measured**. The claim's content is made of three kinds of statement:

1. Other people's measurements, quoted correctly: oocyte Vm, the dye sign, N and p.
2. A **negative search result**: "fibroblast resting Vm has never been measured".
3. A **judgement**: "falls as an established premise".

Parts 2 and 3 are derived/inferred, not measured. Part 2 is also stated in the claim without its search
scope, although the source document does give the scope. The identical claim was recorded as "derived"
under claim_id 250.

Recording the verdict as "measured" presents an inference as an observation. That is a defect under the
honesty floor even though the underlying facts are right. **Corrected level: derived (literature
synthesis of measured heterologous and measured-proxy in vivo data, plus a scoped negative search).**

## 5. "alf/lof" in the KEY (D2)

The KEY says: "in vivo fin-cell dVm for alf/lof: unknown in mV; sign by DiSBAC2(3) in whole fin =
depolarising". The DiSBAC2(3)/DiBAC4(3) result is for ***alf* only** (Perathoner 2014).

For *lof* (cis-ectopic *kcnh2a*), I found no in vivo Vm readout of either sign:

- Stewart 2021 lists "characterizing membrane potentials" as future work. Read-level: via the source
  document and replicate-250, not re-read by me.
- Liu et al. (§6) measured Ca²⁺, not Vm, in *lof*⁻/⁻ larval fins. Read-level: full-text.

**Correction:** for *lof* the sign is **unknown**, not "depolarising". Jiang 2024 is a heat-shock
*kcnk5b* overexpression in embryonic buds, not the *alf* or *lof* allele. The source document says so,
but the compressed claim lumps it in.

## 6. Counter-example and regime the claim missed (D3, and a strengthening finding)

**Liu J, Nerli E, … Jülicher F, Mateus R.** "Injury-induced electrochemical coupling triggers
regenerative cell proliferation". bioRxiv 10.1101/2025.04.03.647033, version posted 8 Apr 2025.
Published as "Injury-induced electrochemical coupling triggers organ growth", *Sci Adv* 2026
(eaec0687; PubMed 41637501).

- **Read-level:** full-text of the **bioRxiv v1 preprint** (PDF text extracted with pdftotext,
  keyword-scanned). The *Sci Adv* version page returned HTTP 403, so for that version I have only
  search-summary.
- **What it measured:** in vivo voltage imaging in the fin, using the FRET GEVI **Voltron2** in apical
  and basal **epithelial** cells of 2 dpf larval caudal fins. Injury caused "widespread cell
  depolarisation in both fin layers", with a length scale of 186 ± 39 µm apical and 197 ± 22 µm basal.
  These are ΔF/F₀ values. I found no mV calibration in the text.
- **Consequence for the claim's wording:** this is an in vivo fin Vm readout that the claim's "the only
  in vivo fin readouts" does not cover. It does **not** concern the K⁺ alleles' effect on Vm, so the
  claim's statement is correct only when scoped to long-fin K⁺ alleles. I count this as a wording and
  scope defect, not a refutation.
- **It strengthens the citation-chain finding.**
  - For *lof*⁻/⁻ and FK506, Liu et al. write: *"A working hypothesis is that the applied manipulations
    (lof-/- and FK506) increase K+ leakage, lowering the resting membrane potential of the tissue,
    hyperpolarizing Vmem (20)"*.
  - Their ref. 20 is Perathoner 2014.
  - They had a working GEVI in this very tissue and still did not measure resting Vm in *lof*⁻/⁻.
  - This is a fourth paper, after Le Bleu 2025, Aramaki 2026 and Jiang 2024, that carries the
    hyperpolarisation sign forward by citation. That is the claim's thesis exactly (inference).
- **It adds a regime with an awkward sign for the canonical chain.** In injured larval fins, both
  *lof*⁻/⁻ and FK506 "led to a prominent Ca²⁺ flash increase", and both impaired regeneration (shorter,
  not longer, regenerates). If the canonical chain (hyperpolarisation → less Ca²⁺) applied in this
  tissue, Ca²⁺ should fall. The observation is the opposite.
  - The context is different: epithelium, larval stage, injury-evoked flashes, not steady-state
    fibroblast Ca²⁺. So this does not refute the adult fibroblast chain (inference).
  - The authors themselves attribute the larval/adult discrepancy to cell type.
  - It is one more datum showing the K⁺ → Ca²⁺ sign is regime-dependent. That supports the claim's
    "coupling unresolved".
- **A disagreement to preserve.** In Liu et al., uncut 2 dpf larvae treated with KCl
  (depolarisation) grew **longer** fins (Fig 3K–L). Aramaki & Kondo (preprint, per the source document)
  found that ChR2 depolarisation of adult keratinocytes **shrinks** fins. Both are epithelial
  depolarisations with opposite size outcomes, at different stages. I do not reconcile them.

**Negative search, with its scope.** I looked for an in vivo mV measurement of fin fibroblast or
blastema Vm, in any background:

- One extended web search: zebrafish fin regeneration, membrane potential, voltage imaging, blastema,
  fibroblast, kcnk5b, longfin, 2025–2026.
- One standard web search for the Liu title.
- A full-text scan of Le Bleu 2025 (PMC13078715, via WebFetch, first 100 k of 106 k characters). It
  reports **no** resting Vm, patch clamp, voltage dye or GEVI measurement. Its only Vm manipulation is
  KCl, read out by GCaMP6s.
- A full-text keyword scan of Liu et al. v1.

**Result: none found.** "Fibroblast resting Vm has never been measured" survives within this scope. The
Europe PMC REST endpoint returned HTTP 500 and was not usable.

## 7. "Cav blockers" (D4)

Le Bleu 2025, full-text, quoted via WebFetch: *"Daily 5 μM cilnidipine from 5-28 dpa caused significant
fin overgrowth"*. The groups were DMSO n = 8 and cilnidipine n = 7, with P = 0.0004 by unpaired t-test.
Amlodipine (L-type) and an N-type blocker (rendered "PD17132" in the tool-extracted text; exact compound name not verified) were tested **only in
vitro**, on KCl-evoked Ca²⁺. I found no other in vivo Cav-blocker overgrowth result in this scope.

"Cav blockers" should read **"one L/N-type blocker (cilnidipine), n = 7"**. The brake still stands on
*cacna1g* loss of function plus FK506 (Kujawski 2014; Daane 2018), so this narrows its support but does
not remove it.

## 8. What stands and what is corrected

- **Stands:**
  - The Ca²⁺/calcineurin brake.
  - Hyperpolarisation by long-fin K⁺ channels is measured only in oocytes, where it is the expected
    near-E_K outcome.
  - The *alf* in vivo whole-fin readout is depolarising, in two dyes, p < 0.001, N = 21–23, in
    juvenile non-regenerating fins.
  - No mV value for fin fibroblast Vm exists within my search scope.
  - The hyperpolarisation premise is carried by citation. Liu et al. 2025/2026 is a newly found fourth
    instance.
- **Corrected:**
  - The evidence level should be **derived**, not measured.
  - The in vivo dye sign applies to ***alf* only**. For *lof* it is **unknown**.
  - "Only in vivo fin readouts" should be scoped to **K⁺-allele effects**, because Liu et al. imaged
    fin Vm in vivo with Voltron2 for injury.
  - "Cav blockers" should be **one blocker in vivo** (cilnidipine).

## Sources and read-levels

| Source | Read-level |
|---|---|
| Perathoner S. et al. 2014, *PLoS Genet* 10:e1004080 | Full-text via WebFetch: Fig S4 legend, DiSBAC2(3) Methods, Fig 5 oocyte Vm sentence, Fig 6 non-conducting channel |
| Le Bleu H.K. et al. 2025, *Development* 152:dev204739, PMC13078715 | Full-text via WebFetch, first 100 k of 106 k characters |
| Liu J., Nerli E. et al., bioRxiv 10.1101/2025.04.03.647033 v1 (8 Apr 2025) | Full-text (pdftotext, keyword-scanned) |
| Liu et al., *Sci Adv* 2026, eaec0687, PubMed 41637501 | Search-summary only (publisher page 403) |
| Jiang 2024; Stewart 2021; Daane 2018; Yi 2021; Aramaki & Kondo preprint | Not re-read by me. Taken from S11-deepen.md, challenge-250 and replicate-250, all read in full-text |
| S11-deepen.md and S11_deepen_sensitivity.py (`claude/deepen-s11-fin-size-6bhrjv`) | Full-text |
| challenge-250.md (`claude/challenge-s11-deepen-claim-rs0sro`) | Full-text |
| replicate-250.md (`claude/rederive-s11-deepen-fin-size-uy1pio`) | Full-text |

```swarm-challenge
{"claim_id": 264, "outcome": "weakened", "reason": "The core (hyperpolarisation measured only in oocytes, where near-E_K is expected; alf whole-fin oxonol dyes depolarised; no fin fibroblast Vm in mV within my search scope; the hyperpolarisation sign carried by citation, now also by Liu et al. 2025/2026) survives, but the recorded evidence level 'measured' misstates a derived literature synthesis plus negative search, the in vivo depolarising sign is applied to lof where it is unknown (alf only), 'only in vivo fin readouts' misses Liu et al.'s Voltron2 fin imaging, and 'Cav blockers' rests on a single in vivo drug (cilnidipine, n=7).", "corrected_value": null, "depends_on": ["Perathoner2014-PLoSGenet-e1004080 Fig5: mutant Kcnk5b oocyte Vm shift towards -90 to -100 mV, ~2x gK (measured, heterologous)", "Perathoner2014-PLoSGenet-e1004080 FigS4+Methods: alf juvenile (16-18 mm SL, non-regenerating) whole-fin DiSBAC2(3) depolarisation p<0.001 N=21-23, DiBAC4(3) similar, DiSC3(5) uninformative (measured, proxy)", "LeBleu2025-PMC13078715: no Vm measurement; only in vivo Cav blocker is cilnidipine 5 uM 5-28 dpa, n=7 vs 8, P=0.0004; hyperpolarisation link is a Discussion citation to Perathoner2014", "Liu-Nerli-bioRxiv-2025.04.03.647033v1 (SciAdv 2026 eaec0687): Voltron2 in vivo larval fin epithelium injury depolarisation (dF/F, no mV); lof-/- and FK506 increase injury Ca2+ flashes; hyperpolarisation of lof-/- stated as working hypothesis citing Perathoner2014, not measured", "challenge-250 and replicate-250 reads of Jiang2024, Stewart2021, Daane2018, Yi2021 (not re-read by me)", "negative search scope: 1 extended + 1 standard web search, Le Bleu 2025 and Liu 2025 full-text scans; Europe PMC REST unavailable (HTTP 500)", "assumed: oocyte bath [K+]o 2 mM and [K+]i 90-130 mM for Nernst check (calculated E_K -96 to -105 mV)", "assumed: parallel-conductance model E_K -90, E_other 0 for dVm under 2x gK (calculated)"]}
```
