# S41-D — Deepening C5: the decay length of the "kcnh2a/kcnk5b-driven" fin potential gradient

**Parent question (S41, tissue, claim C5):** what is the decay length of the kcnh2a/kcnk5b-driven
potential gradient, and is it within a factor of 3 of the 0.1–120 mm fin ray length it is claimed
to pattern?

**Date:** 2026-11-04. **No experiment was run.** Every number below is either *retrieved* from a
named source (with read-level) or *calculated* by me from retrieved numbers, and says which.

---

## 0. What I was given, and what was missing

The task handed me S41's recorded answer as an **empty string**. I searched this repository
(`git grep` over all 30 commits on all branches for `S41`, `kcnh2a`, `kcnk5b`, `decay length`)
and found only one mention of Kcnk5b, in `findings/gemini-triage-267-problems.json` (a triage
summary that lists no length). **So there is no recorded S41 number to deepen.** I therefore
treated the claim C5 itself as the "answer" under test, found the input it is most sensitive to,
and went for primary data. The verdict in §4 is a verdict on C5, not on a prior answer I could not
see.

The "0.1–120 mm fin ray length" range is taken from the question as given. **Its provenance is
unknown**; I did not find a source for either bound.

---

## 1. Sensitivity: which input moves the conclusion?

The test is `1/3 ≤ λ / L ≤ 3`, where λ is the decay length and L the ray length. Two inputs.

**(a) λ, the decay length.** Before this work, λ for any fin tissue was not in hand; it would have
had to come from cable theory with assumed membrane and junctional resistances, which span orders
of magnitude. After §3, λ is measured at ≈ 0.19–0.21 mm (one study). Perturbing it by 2× — a
*calculation*:

| λ (µm) | λ/L, L = 0.16 mm (larval finfold) | λ/L, L = 5 mm (adult-scale ray) |
|---|---|---|
| 103 (÷2) | 0.64 — passes | 0.021 — fails |
| 206 (measured) | 1.29 — passes | 0.041 — fails |
| 412 (×2) | 2.58 — passes | 0.082 — fails |

A factor of 2 in λ does **not** change the verdict at either scale.

**(b) L, the ray length the gradient is supposed to pattern.** The question's range is 1200-fold
wide (0.1 → 120 mm). Using the measured λ (CI-bounded 163–254 µm), the verdict flips at
**L ≈ 0.49–0.76 mm** (L = 3λ; calculated):

| L | λ/L (λ = 163 / 187 / 206 / 254 µm) | within 3×? |
|---|---|---|
| 0.1 mm | 1.6 / 1.9 / 2.1 / 2.5 | yes |
| 0.16 mm | 1.0 / 1.2 / 1.3 / 1.6 | yes |
| 0.6 mm | 0.27 / 0.31 / 0.34 / 0.42 | borderline |
| 1 mm | 0.16 / 0.19 / 0.21 / 0.25 | no |
| 5 mm | 0.033 / 0.037 / 0.041 / 0.051 | no |
| 120 mm | 0.0014 / 0.0016 / 0.0017 / 0.0021 | no |

**The conclusion is most sensitive to L — which tissue, at which stage, the gradient is compared
against — not to λ.** The question's L is not one number; across its own range the answer is both
"yes" and "no by 600×".

**(c) A categorical input that sits above both:** whether the measured gradient is
*kcnh2a/kcnk5b-driven* at all. See §2.

---

## 2. How well are the inputs established?

| Input | Status | Evidence level / read-level |
|---|---|---|
| λ of a fin Vmem gradient | **measured**, once, in WT 2-dpf larval finfold epithelium, 0.1 s after laser injury | Liu et al. 2026, full-text |
| That this gradient is "kcnh2a/kcnk5b-driven" | **not established; the evidence I read argues against it** | see below |
| L = 0.1–120 mm | **stated in the question, unsourced** | unknown |
| Adult zebrafish caudal ray length "mm scale" | inferred from scale bars (1 cm whole-fin; 2–4 mm regenerates) and from the phrase "millimetre-long gradients spanning from the distal tip to the amputation site" | Le Bleu 2025, Rich 2026, full-text; **no numeric ray length retrieved** |
| Larval finfold extent ≈ 0.16 mm beyond the notochord | retrieved: EM sections "at the notochord level (∼160 μm from finfold tip)" | Liu 2026, full-text |

**On "kcnh2a/kcnk5b-driven".** In the one study that measures λ, the gradient is a WT
*injury-induced depolarization*. Liu et al. use `kcnh2a^lof/lof` (the gain-of-function *longfin*
allele) and FK506 (which holds Kcnk5b open) as "Vmem-hyperpolarizing conditions", **citing earlier
work for the hyperpolarization (their refs 47, 54, 68–71)**. In their main text they report Ca²⁺
flashes and proliferation in these conditions; **I found no Voltron2 λ fitted in either condition**
(scope: grep of the main text and figure legends of the PMC full text; the supplementary theory
notes and figures S1–S20 were **not** read). So the measured λ is a proxy: same organ, same
channel family as perturbation, but neither the driver nor the stage named in C5.

The adult papers make a claim that cuts against a long-range gradient. These are **the authors'
claims, not my inference**:

- Stewart et al. 2021 (full-text): *longfin*-ectopic kcnh2a "acts tissue autonomously within the
  fin intra-ray mesenchymal lineage" and controls size "by tuning outgrowth periods rather than
  altering positional information". They list "characterizing membrane potentials" as a *future*
  step, i.e. not measured there.
- Le Bleu et al. 2025 (full-text): fibroblast-lineage Ca²⁺ transients in the distal blastema;
  isolated fin fibroblasts show voltage-gated-Ca²⁺-channel-dependent transients, "indicating cell
  autonomous initiation of membrane potential fluxes".
- Daane et al. 2018 (full-text): Kcnk5b electrophysiology is in *Xenopus* oocytes (voltage clamp),
  not in fin tissue; no fin Vmem gradient or length reported.
- Rich et al. 2026 (full-text): the gradient that *does* scale with the regenerate is **Erk**, not
  Vmem — its "length scale matches the regenerate length", and the authors say it has the
  potential to eliminate "the need for active, millimeter-long cell-cell communication".

**Disagreement preserved.** Liu et al. 2026 (full-text) claim the opposite emphasis: an
"organ-wide signal spreading" via interstitial electrodiffusion, and that VSP stimulation "leads to
longer finfolds, supporting a role for tissue-wide electrical signals as a potential general
mechanism contributing to organ size". Their "organ" is the 2-dpf finfold, ~0.2 mm, where the two
views do not conflict numerically. They conflict only if extrapolated to the adult ray, which Liu
et al. do not measure.

---

## 3. The improved input — primary source

**Liu J, Nerli E, Duclut C, Vishen AS, Berbee N, Kaufmann S, Ponce C, Arrenberg AB, Jülicher F,
Mateus R. "Injury-induced electrochemical coupling triggers organ growth." *Science Advances*
(2026). doi:10.1126/sciadv.aec0687, PMID 41637501, PMC12871474.** Read-level: **full-text**
(main text and legends, via Europe PMC full-text XML; supplement not read). *Retrieved.*

Observed (authors' measurement, quoted):

- Voltron2 FRET voltage reporter, 0.1 s post-cut: "the spatial gradient of V mem depolarization
  displays an exponential profile with comparable characteristic lengths l for both epithelial
  layers (**apical: 206 ± 48 μm, basal: 187 ± 24 μm**; Fig. 1K)". Error is 95% CI of the fit.
- Fit window: cells 30–150 µm from the cut (0–30 µm discarded as laser-damaged; beyond 150 µm
  samples "contribute unevenly"). **Note: the fitted λ (~200 µm) exceeds the fitting window
  (120 µm wide); the exponential is only partly sampled.** That is my observation about their
  method, not theirs.
- Ca²⁺ wavefront stops at ~120 µm (apical 118.4 ± 14.3 µm; basal 118.7 ± 8.5 µm); in high KCl it
  runs >300 µm.

Their model (authors' claim): after ~100 ms the interstitial potential is exponential with
characteristic length "l = D / Λ" as rendered in the XML; they back out **Λ = 0.05 s⁻¹** ≈
**~200 Ω·cm²** epithelial resistance. *My calculation:* D/Λ has units of µm², so the length must be
√(D/Λ): √(1334/0.05) = 163 µm (Na⁺), √(2032/0.05) = 202 µm (Cl⁻), which reproduces the measured
λ. So I read the formula as √(D/Λ); the square root was likely lost in text extraction. This
inference was not checked against note S2.

**What would extend it to the C5 tissue (calculated, under assumptions I name).** If the same
electrodiffusive mechanism held in the adult ray and Λ scaled as 1/R at fixed geometry (an
assumption — the adult fin has a multilayered epidermis and a different interstitial geometry, so
both D_eff and the geometric factor in Λ will change), reaching λ = L/3 needs:

| target L | λ needed | Λ needed | fold-reduction of Λ | implied R_epi |
|---|---|---|---|---|
| 1 mm | 333 µm | 1.5×10⁻² s⁻¹ | 3.3× | ~660 Ω·cm² |
| 5 mm | 1.7 mm | 6.1×10⁻⁴ s⁻¹ | 83× | ~1.7×10⁴ Ω·cm² |
| 10 mm | 3.3 mm | 1.5×10⁻⁴ s⁻¹ | 330× | ~6.6×10⁴ Ω·cm² |
| 120 mm | 40 mm | 1.1×10⁻⁶ s⁻¹ | 4.8×10⁴× | ~10⁷ Ω·cm² |

Adult rays of a few mm would need a tight-epithelium resistance (10⁴ Ω·cm²) to carry this kind of
gradient; I did not find a measured value of adult zebrafish fin epidermal resistance (scope:
not searched beyond the five full texts above), so that requirement stays **unknown**, not ruled
out. The 120 mm end needs ~10⁷ Ω·cm², implausible on general physiology grounds, but I have no
retrieved source for an upper bound, so this is *remembered*, not retrieved.

**The measurement that would settle C5.** Voltron2 (or ASAP-family) live voltage imaging in adult
regenerating caudal fins — WT, `kcnh2a^lof` (longfin^t2), `kcnk5b` gain-of-function, and a
*shortfin*/cx43 background — fitting a proximodistal λ along a single ray at 3–7 dpa, together
with transepithelial resistance. The transgenic lines and the imaging pipeline already exist in
the Liu (Mateus) and Le Bleu/Stewart (Stankunas) groups. Cost: unknown; my guess (*not
retrieved*) is a few months of one person's work with existing lines, the main obstacle being
voltage imaging through adult pigment and scale-covered tissue.

---

## 4. Recomputed conclusion

With the improved input λ ≈ 0.19–0.21 mm (measured; CI 0.16–0.25 mm):

- **Larval finfold (~0.1–0.16 mm, no rays yet):** λ/L ≈ 1.0–2.5 → **within 3×** (calculated).
- **Adult rays, mm scale:** λ/L ≈ 0.02–0.2 for L = 1–10 mm → **outside 3×, short by 5–50×**
  (calculated). Crossover at L ≈ 0.5–0.8 mm.
- **120 mm:** short by ~600× (calculated).
- **"kcnh2a/kcnk5b-driven":** the only measured gradient is injury-driven in WT larvae. No λ was
  found for either genotype (scope above), and the adult kcnh2a papers claim a tissue-autonomous
  mechanism that sets outgrowth duration, not positional information.

**Verdict: FALLS.** C5 as posed — a kcnh2a/kcnk5b gradient whose decay length matches 0.1–120 mm
rays — is not supported. The only measured fin Vmem decay length is ~0.2 mm. That matches only the
bottom of the range, in a larval tissue without rays and with a driver that is not
kcnh2a/kcnk5b, and the adult kcnh2a/kcnk5b literature claims cell- or tissue-autonomous action.
It is a null on one study, not a refutation. An adult measurement (§3) could reverse it if the
adult epidermis turns out to be ~10⁴ Ω·cm² tight.

---

## 5. Sources and read-levels

| Source | Read-level | Used for |
|---|---|---|
| Liu et al. 2026, *Sci Adv*, doi:10.1126/sciadv.aec0687, PMC12871474 | full-text (main + legends; supplement **not** read) | λ = 206 ± 48 / 187 ± 24 µm; Λ = 0.05 s⁻¹; ~200 Ω·cm²; finfold geometry |
| Stewart et al. 2021, *Development* 148:dev199384, doi:10.1242/dev.199384, PMC8217709 | full-text (PMC HTML) | kcnh2a acts tissue-autonomously; outgrowth duration, not positional information; Vmem not measured |
| Le Bleu et al. 2025, PMC13078715 (PMID 41321290) | full-text (PMC HTML) | cell-autonomous Ca²⁺ in distal blastema; scale bars |
| Daane et al. 2018, *Sci Rep*, PMC6039437 | full-text (Europe PMC XML) | Kcnk5b electrophysiology in oocytes only; no fin gradient |
| Rich et al. 2026, *Nat Phys*, doi:10.1038/s41567-026-03426-w, PMC13557033 | full-text (PMC HTML) | mm-long Erk gradients scale with regenerate |
| Perathoner et al. 2014, *PLoS Genet*, doi:10.1371/journal.pgen.1004080 | could-not-access in practice (listing only; URL returned HTTP 200, not read) | not used for any number |
| Europe PMC search listings ("kcnk5b fin zebrafish", 48 hits; "kcnh2a longfin", 17 hits; top 25 titles read) | listing | finding the papers above; Aramaki & Kondo 2024 and Silic & Zhang 2023 seen in listings, **not read** |

**Search controls (rule 8).** Positive: `EXT_ID:41637501` → exactly 1 hit, the Liu paper.
Must-fail: `EXT_ID:99999999999` → 0 hits. A third ID I tried from memory as Perathoner 2014
(`24391517`) returned an unrelated cattle-genetics paper. That number was **remembered and wrong**,
and was not used. Europe PMC full-text XML returned HTTP 500 for four of the PMCIDs; I re-read
those from PMC HTML, and every text I used was checked to be the real article and not an error
body. `pubmed.ncbi.nlm.nih.gov` was unreachable from this session's network policy.

**Negative-search scope.** "No fin Vmem λ in kcnh2a/kcnk5b genotypes" covers the main texts of the
five full texts above, plus listing-level reading of 42 Europe PMC records. It does not cover the
Liu supplement, Aramaki & Kondo 2024, Silic & Zhang 2023, or Perathoner 2014.

```swarm-result
{"subproblem": "S41-D", "evidence": "measured-proxy (one study, full-text; WT larval injury-induced gradient, not kcnh2a/kcnk5b-driven)", "answer": "The only measured fin Vmem decay length is ~0.19-0.21 mm (Voltron2, WT 2-dpf larval finfold, injury-induced). That is within 3x only of sub-millimetre larval tissue and 5-600x short of mm-to-120 mm rays, and the adult kcnh2a/kcnk5b papers claim tissue-autonomous action, so C5 is unsupported.", "key_number": "lambda = 206 +/- 48 um (apical), 187 +/- 24 um (basal), 95% CI; Liu et al. 2026 Sci Adv PMC12871474", "verdict": "falls", "depends_on": ["measured: Vmem depolarization decay length 206+/-48 um apical / 187+/-24 um basal, Liu 2026 Fig 1K (WT, 2 dpf, 0.1 s post-injury, fit window 30-150 um)", "assumption: the injury-induced larval Vmem gradient is a valid proxy for a kcnh2a/kcnk5b-driven gradient", "claim (Liu 2026, cited not measured there): kcnh2a lof/lof and FK506 are Vmem-hyperpolarizing", "claim (Stewart 2021): longfin kcnh2a acts tissue-autonomously in intra-ray mesenchyme and tunes outgrowth duration, not positional information", "claim (Le Bleu 2025): fin fibroblast Ca2+/voltage fluxes initiate cell-autonomously", "claim (Rich 2026): mm-long Erk gradients scale with regenerate length", "question input: fin ray length range 0.1-120 mm (provenance unknown)", "inferred: adult zebrafish caudal ray length is mm-scale (from scale bars and Rich 2026 wording; no numeric value retrieved)", "measured: larval finfold extends ~160 um beyond notochord tip (Liu 2026 methods)", "model: electrodiffusive l = sqrt(D/Lambda), Lambda = 0.05 s^-1 ~ 200 ohm cm2 (Liu 2026); sqrt is my reading", "assumption: Lambda scales as 1/R_epi at fixed geometry when extrapolating to adult fins", "unknown: adult zebrafish fin epidermal transepithelial resistance", "negative search scope: main texts of 5 full texts plus 42 Europe PMC listings; Liu supplement not read"]}
```
