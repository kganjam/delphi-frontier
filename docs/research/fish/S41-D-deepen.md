# S41-D-D — Deepening S41-D: attack the ray length L, then the decay length λ it exposes

**Parent:** S41-D, "Deepen S41: attack its most sensitive input" — recorded in
`docs/research/fish/S41-deepen.md` on branch `claude/s41-deepen-kcnh2a-decay-zmra54`
(commit `07e6a011`). That file is not on this branch. Read-level for it: full-text (I read the whole file).

**Parent's claim under test (C5):** a kcnh2a/kcnk5b-driven fin membrane-potential gradient has a
decay length λ within a factor of 3 of the fin-ray length L it is said to pattern, i.e. 1/3 ≤ λ/L ≤ 3.

**Parent's answer:** FALLS. The parent found λ ≈ 0.19–0.21 mm (Liu et al. 2026, WT 2-dpf larval
finfold, injury-induced). It held that adult rays are "mm-scale", so λ/L falls 5–50× short for
L = 1–10 mm. The parent named L as its most sensitive input. It also said L was **never retrieved
as a number**: it was inferred from scale bars.

**Date:** 2026-11-04. **No experiment was run.** Every number here is labelled as *retrieved*
(from a named source, with a read-level) or *calculated* (by me, from retrieved numbers).

---

## 1. Which input is the parent's answer most sensitive to? (recomputed, not asserted)

The test is 1/3 ≤ λ/L ≤ 3. The verdict flips where L = 3λ.

*Calculated* crossover lengths, using the retrieved λ values (§3):

| λ (µm) | 158 (apical CI low) | 187 (basal) | 206 (apical) | 254 (apical CI high) | 412 (206 × 2) |
|---|---|---|---|---|---|
| crossover L = 3λ | 0.47 mm | 0.56 mm | 0.62 mm | 0.76 mm | 1.24 mm |

- **L.** The parent's "FALLS" holds only if the relevant L is above ~0.6–0.8 mm. A 2× error in L
  matters only if the true L is between ~0.3 and ~1.5 mm. The parent never retrieved L, so it could
  not tell whether L falls in that band. **This was the weakest input**, and I attacked it first (§2).
- **λ.** In the parent's framing (L ≥ 5 mm), a 2× error in λ changed nothing. That stops being
  true once L is pinned down (§4).
- **Epithelial resistance R.** In the Liu model λ = √(D/Λ) and Λ ∝ 1/R (§3), so λ ∝ √R. A 2× error
  in R moves λ by only 1.41×. This is the least sensitive of the three, *calculated*.

---

## 2. Improving L: from "inferred from scale bars" to a measured range

**Retrieved.** Rich et al. 2026, *Nature Physics*, "Decaying and expanding Erk gradients process
memory of skeletal size during zebrafish fin regeneration", doi:10.1038/s41567-026-03426-w,
PMC13557033. Read-level: **full-text** (PMC HTML).

The authors state (quoted):
- "the fraction of osteoblasts cycling has an invariant relationship with fraction regenerated
  across **lengths amputated ranging from 0.7 to 4 millimeters**".
- Erk gradients "were obtained from rays with lengths amputated ranging from 0.7 to 4 millimeters
  and across post-amputation times ranging from 3 to 14 days."
- "Over time they extend and flatten out so that their length scale matches the regenerate length."

**What kind of number this is.** It is a *measured* range: the experimental amputation lengths of
adult caudal rays, in a study whose patterning gradient is shown to scale with them. For C5 it is
the right L. A regeneration patterning signal must span the tissue that was removed, not the whole
ray. It is **not** the length of a whole adult ray. I still found no numeric value for whole-ray
length. In Le Bleu et al. 2025 (full-text) I found only scale bars (1 cm, 4 mm, 2 mm) and a method
("third fin ray, from the amputation plane to the fin tip"), and no tabulated mm values in the text
I read. The question's 0.1–120 mm range is still **unsourced**.

**One caveat on the definition of L.** Each regenerate is shorter than its final amputated length
until it finishes growing. If C5 means the *current* regenerate length rather than the target
length, then L is below 0.7 mm early in regeneration. I found no numeric regenerate-length time
course in the text I read. A value for early regenerates is therefore `unknown`, not assumed.

---

## 3. The λ input, re-read from the supplement the parent did not read

**Retrieved.** Liu et al. 2026, *Sci. Adv.* 12:eaec0687, doi:10.1126/sciadv.aec0687, PMC12871474.
Read-level: **full-text**, now **including the Supplementary Materials PDF** (theory notes S1–S6,
legends of Figs. S1–S20 and Movies S1–S11). I got these through the Europe PMC
`supplementaryFiles` endpoint.

The supplement shows four things the parent had only inferred or had not seen.

1. **The square root is confirmed.** Note III.1 gives ϕ_I = ϕ_ss(1 − e^(−√(Λ/D)·x)) and
   "l = √(D/Λ)". The parent read the formula as √(D/Λ) without seeing the supplement. That
   reading now has a source.
2. **Main text and supplement disagree on Λ and R. Both values are kept here.**
   - Main text: "Λ = 0.05 s⁻¹ … an epithelium resistance in unit area of ~200 ohm·cm²".
   - Supplement: with D = 1683 µm²/s (the mean of D_Na and D_Cl), "Λ = 0.0397 ± 0.0185 s⁻¹ for
     apical cells" and "R ≃ 245 ± 154 Ω·cm²". The simulations use Λ = 0.042 s⁻¹.

   *My calculation:* D/λ² = 1683/206² = 0.0397 s⁻¹ (apical) and 1683/187² = 0.048 s⁻¹ (basal).
   The "0.05" in the main text looks like a rounded or basal-layer figure. That is my inference;
   the authors do not say so.
3. **The λ values and their uncertainty, quoted:** "apical: 206 ± 48 µm, basal: 187 ± 24 µm",
   95% CI of the fit. The CI union is **158–254 µm**. (The parent wrote 163–254. 163 is the
   basal lower bound; the apical lower bound is 158.)
4. **No voltage gradient was measured in the kcnh2a or kcnk5b conditions.** In the supplement,
   `kcnh2a^lof/lof` and FK506 appear only in Ca²⁺ (GCaMP6f) data (Figs. S6C–D, S7), proliferation
   data and finfold-length data (Figs. S9, S10), and Movie S9. Voltron2 appears only for WT injury
   (Fig. S4) and KCl perfusion (Figs. S6E, S15).
   *Scope of this negative:* I grepped the whole supplement text for Voltron, FRET, Vmem and
   membrane potential, and read every matching legend. **λ in a kcnh2a or kcnk5b gradient: not
   measured in Liu et al. 2026, main text or supplement.** The parent's proxy (a WT injury-induced
   gradient standing in for a kcnh2a/kcnk5b-driven one) is therefore confirmed to be a proxy.

**A weakness in the measurement itself.** The authors fit "cells that are in the range of 30 to
150 µm from the cut site". Beyond 150 µm, samples "contribute unevenly". *My calculation:* for an
exponential with λ = 206 µm, the 120 µm-wide window sees only 1 − e^(−120/206) ≈ **44 %** of the
decay. With λ = 412 µm it would see 25 %. A fit that sees less than half the decay constrains long
λ poorly, so the true upper uncertainty may be larger than the reported +48 µm. This is my
inference about their method; the authors do not state it.

**I tried to refit λ from the raw data. It is not accessible.** The authors deposit data on
Edmond (doi:10.17617/3.6WBOSZ) and code on Zenodo (10.5281/zenodo.15038032, .15037932,
.17397026, .15019089). Both `edmond.mpg.de`/`doi.org` and `zenodo.org` were refused by this
session's egress proxy (HTTP 403 on CONNECT). Read-level for both: **could-not-access**.

---

## 4. Recomputed conclusion with the improved L

All values are *calculated* from the retrieved λ (158–254 µm; central values 187 and 206 µm) and
the retrieved L = 0.7–4 mm.

| L (amputated) | λ/L at λ = 158 / 187 / 206 / 254 µm | λ/L if λ is 2× (412 µm) | λ needed for λ/L = 1/3 | implied R, if adult behaves as larval model |
|---|---|---|---|---|
| 0.7 mm | 0.23 / 0.27 / 0.29 / **0.36** | **0.59 (passes)** | 233 µm (1.13× of 206) | 1.3 × 245 ≈ 310 Ω·cm² |
| 1.0 mm | 0.16 / 0.19 / 0.21 / 0.25 | **0.41 (passes)** | 333 µm (1.6×) | 2.6 × 245 ≈ 640 Ω·cm² |
| 2.0 mm | 0.08 / 0.09 / 0.10 / 0.13 | 0.21 (fails) | 667 µm (3.2×) | 10 × 245 ≈ 2.6×10³ Ω·cm² |
| 4.0 mm | 0.04 / 0.05 / 0.05 / 0.06 | 0.10 (fails) | 1333 µm (6.5×) | 42 × 245 ≈ 1.0×10⁴ Ω·cm² |

What this shows:
- **For most of the measured range (≈ 1–4 mm), "FALLS" stands.** λ falls short by 1.6–6.5×. A 2×
  error in λ does not rescue the 2–4 mm end. That would need a 10–42× tighter adult epidermis.
- **At the short end (0.7 mm) the result is marginal, not a clear fail.** The central λ/L is
  0.27–0.29, just under 1/3. The upper CI bound (0.36) already passes. A 2× error in λ, well
  within the doubt the fit-window problem raises, passes too.
- **The parent overstated the gap.** It said "short by 5–50×" for L = 1–10 mm. With measured L
  the gap is **~1.1–6.5×**. Ten-mm regenerates are not in the measured set.

**What would settle it, and the rough cost:**
1. **A refit of λ from the Liu Voltron2 data**, with the plateau ϕ_ss free and a profile-likelihood
   CI. It needs access to Edmond doi:10.17617/3.6WBOSZ. Cost: about a day of analysis once the data
   are reachable (my estimate, *not retrieved*). It would show whether 206 µm can be trusted to the
   ~1.1× precision the 0.7 mm case needs.
2. **The decisive measurement:** live Voltron2 or ASAP voltage imaging in adult regenerating caudal
   rays. Use WT, `kcnh2a^lof` (longfin) and a kcnk5b gain-of-function line, with amputation lengths
   spanning 0.7–4 mm, plus transepithelial resistance of adult fin epidermis. No such data were
   found. Cost: `unknown`. The parent's guess of a few person-months with existing lines is
   repeated here as a guess, not a retrieved figure.
3. **Adult fin epidermal resistance.** I searched Europe PMC
   (`zebrafish AND (transepithelial resistance OR "epithelial resistance") AND (skin OR epidermis OR fin)`,
   549 hits; `fish skin transepithelial resistance ohm`, 61 hits) and read the top 15 titles of
   each at listing level. None reports adult zebrafish fin epidermal resistance. *Scope:* 30
   titles only; abstracts not read. Value: **unknown**.

---

## 5. Verdict: STANDS (with a narrower margin and a scoped exception)

C5 as posed still does not hold. It needs a **kcnh2a/kcnk5b-driven** gradient whose λ is within 3×
of the ray length it patterns.
- **The driver part is firmer than before.** The only fin λ ever measured is a WT injury-induced
  one. The full supplement now confirms that no voltage profile was measured in kcnh2a or kcnk5b
  conditions. The adult kcnh2a papers the parent read claim tissue-autonomous action (Stewart 2021;
  Le Bleu 2025; authors' claims, carried forward from the parent, not re-read here).
- **The length part is weaker than the parent said.** With measured amputation lengths of
  0.7–4 mm, the measured larval λ fails for most of the range by 1.6–6.5×. At 0.7 mm it sits on
  the boundary, inside the uncertainty of a fit that sees only ~44 % of its own decay.

The verdict is not "strengthens", because the length margin shrank. It is not "falls" (that is, the
parent's conclusion is not overturned), because nothing measured places λ within 3× of L across the
range, and the driver requirement is still unmet.

**A negative result, stated precisely:** the parent's conclusion stands for 1–4 mm amputations. It
is **undetermined for amputations ≲ 1 mm**. There, a 1.1–1.6× longer adult λ, or a 1.3–2.6× tighter
adult epidermis, would be enough. Neither has been measured.

---

## 6. Sources and read-levels

| Source | Read-level | Used for |
|---|---|---|
| Parent S41-D, `docs/research/fish/S41-deepen.md` @ `07e6a011` | full-text | answer under test; inherited claims |
| Liu et al. 2026, *Sci Adv*, doi:10.1126/sciadv.aec0687, PMC12871474, main text | full-text (Europe PMC XML) | λ values; fit window 30–150 µm; Λ = 0.05 s⁻¹, ~200 Ω·cm² |
| Liu et al. 2026, Supplementary Materials PDF | full-text (theory notes + all figure and movie legends) | l = √(D/Λ); Λ = 0.0397 ± 0.0185 s⁻¹; R ≃ 245 ± 154 Ω·cm²; no Voltron2 in kcnh2a/FK506 |
| Liu et al. 2026 raw data (Edmond doi:10.17617/3.6WBOSZ) and code (Zenodo ×4) | could-not-access (proxy 403) | intended refit of λ, not done |
| Rich et al. 2026, *Nat Phys*, doi:10.1038/s41567-026-03426-w, PMC13557033 | full-text (PMC HTML) | **L = 0.7–4 mm amputated**; Erk length scale matches regenerate |
| Le Bleu et al. 2025, PMC13078715 | full-text (PMC HTML) | no numeric ray length found; scale bars only |
| Stewart et al. 2021, PMC8217709 | could-not-access this session (PMC returned a reCAPTCHA page; Europe PMC XML HTTP 500); claim carried from parent's full-text read | tissue-autonomous kcnh2a |
| Europe PMC searches (two queries, 30 titles) | listing | negative search for adult fin epidermal resistance |

```swarm-result
{"subproblem": "S41-D-D", "evidence": "measured-proxy (lambda: one study, full-text incl. supplement, WT larval injury-induced gradient; L: measured amputation lengths, full-text)", "answer": "Replacing the parent's scale-bar-inferred ray length with measured adult amputation lengths of 0.7-4 mm, the measured larval Vmem decay length (158-254 um) is still 1.6-6.5x too short for 1-4 mm but borderline at 0.7 mm, and no kcnh2a/kcnk5b-specific Vmem gradient was measured even in the Liu supplement, so C5 still fails, with a narrower margin than the parent claimed and undetermined below ~1 mm.", "key_number": "L = 0.7-4 mm amputated ray length (Rich et al. 2026, measured); lambda/L = 0.23-0.36 at 0.7 mm and 0.04-0.06 at 4 mm (calculated)", "verdict": "stands", "depends_on": ["measured: amputated adult caudal ray lengths 0.7-4 mm, Rich et al. 2026 Nat Phys PMC13557033", "claim (Rich 2026): Erk gradient length scale matches regenerate length", "assumption: the relevant L for C5 is the amputated (to-be-patterned) length, not whole-ray length or instantaneous regenerate length", "measured: Vmem depolarization decay length 206+/-48 um apical, 187+/-24 um basal (95% CI), Liu 2026 Fig 1K, WT 2-dpf larval finfold, 0.1 s post-injury, fit window 30-150 um", "inferred: the 30-150 um fit window sees only ~44% of a 206 um decay, so the upper CI on lambda may be underestimated", "model: l = sqrt(D/Lambda), D = 1683 um2/s, Liu 2026 supplement note III.1", "disagreement kept: Lambda = 0.05 s-1 and R ~200 ohm cm2 (Liu main text) vs Lambda = 0.0397+/-0.0185 s-1 and R = 245+/-154 ohm cm2 (Liu supplement)", "assumption: lambda scales as sqrt(R_epi) when extrapolating to adult fin epidermis", "unknown: adult zebrafish fin epidermal transepithelial resistance (Europe PMC listing search, 30 titles)", "negative: no Voltron2/Vmem profile in kcnh2a lof/lof or FK506 conditions, Liu 2026 main text + full supplement text", "assumption: the WT injury-induced larval gradient is a valid proxy for a kcnh2a/kcnk5b-driven gradient", "claim (Stewart 2021, via parent; not re-read): longfin kcnh2a acts tissue-autonomously and tunes outgrowth duration", "claim (Le Bleu 2025): fin fibroblast Ca2+/voltage fluxes initiate cell-autonomously", "question input: fin ray length range 0.1-120 mm (provenance unknown)", "parent: S41-D verdict falls, docs/research/fish/S41-deepen.md @ 07e6a011"]}
```
