# Challenge 125: adversarial review of S9-D-D (the root-compliance correction to the zebrafish fin EI)

Date: 2026-11-04 · Claim source: `docs/research/fish/S9-D-deepen.md` and `S9-D-deepen_calc.py` on
`origin/claude/deepen-s9-d-sensitive-input-8jtunz` (full-text, read from the branch) · My script:
`docs/research/fish/challenge-125_calc.py`. **Every number my script prints is a calculation, not an
observation.**

**Read-levels:** full-text | abstract | listing | search-summary | could-not-access.

## Verdict: WEAKENED

Four parts of the claim survive testing:

- **The qualitative answer survives.** S9's 1.34 GPa falls, and carrying EI rather than E is the
  right call.
- **The rigid-clamp misfit survives.** It holds even when I replace the author's error yardstick with
  Puri's own, larger measurement error.
- **The direction of the correction survives.** Any series compliance in the root, the contact or the
  shear path raises the bending-only EI.
- **The arithmetic reproduces.**

The key number does not survive. "Corrected whole-fin EI ~2–8 × 10⁻⁹ N·m²" is set by the functional
form chosen for the compliance, and the data cannot choose between forms:

- **The author's own clamp-offset mechanism fits as well and gives a higher range.** The author
  raises this mechanism in their §1 but never fits it. It fits the rising limb as well as the
  translational and shear forms do (χ² p = 0.43–0.96), and it gives ~4.5–14 × 10⁻⁹ N·m².
- **That higher range changes the conclusion about bone.** With it, the thin-wall (t = 11 µm)
  uncoupled-plate bound reaches ~24–26 GPa. That equals the vertebral nanoindentation E (23–25 GPa,
  search-summary). So "narrows but does not close" the bone gap is not robust; closure becomes
  possible.
- **"Is a lower bound" is conditional, not established.** It holds only under readings (i) and (ii)
  in the claim's own §3. It does not hold under reading (iii), the authors' interpretation, which the
  claim itself says it cannot exclude.

## 1. Arithmetic, redone independently

I took the author's plot readings as given (Fig. S5B and S5C), because I could not re-digitize the
supplement in this session. I refit them with my own code (scipy `least_squares`, not the author's
grid search). All results below are calculations.

- **Rise of E_eff with span.** Max/first ratios: fish 4 = 1.16, fish 13 = 1.60, fish 12 = 2.51,
  fish 11 = 2.58, fish 5 = 3.65. This matches "1.2–3.7×".
- **Constant-E rmse.** I get 1.82, 2.34, 2.92, 0.54 and 1.11 MPa. This matches the claim (fish 4,
  with 2 points, is excluded from "1.1–2.9").
- **Corrected ranges.** Translational: 2.10–6.14 × 10⁻⁹. Shear: 3.20–8.29 × 10⁻⁹. The author got
  2.11–6.03 and 3.17–7.83. The small differences come from grid versus continuous optimization.
- **Per ray.** 2.1 × 10⁻⁹ / 18 = 1.17 × 10⁻¹⁰ and 7.8 × 10⁻⁹ / 16 = 4.9 × 10⁻¹⁰. This matches.
- **Pure-hinge ceiling.** Under a pure rotational spring at the root, E(L₂)/E(L₁) can never exceed
  L₂/L₁. The algebra is correct, and the observed ratios exceed that ceiling (also correct).

No arithmetic error found.

## 2. The hidden yardstick: reading error is not measurement error

The claim says the rigid-clamp model misfits "vs ~0.15 MPa reading error". That is the author's
digitizing error, not the noise in Puri's data.

Puri et al. 2018 (full-text, Fig. 2 legend and Methods) state these standard deviations:

- **L: ±0.1 mm.** E_app ∝ L³, so this alone gives a 3σ_L/L error. That is ~23% at L = 1.3 mm and
  ~10% at 3 mm.
- **Deflection: ±20 µm.**
- **Force: ±5 µN.**

Converted to E_app, this is ~0.4–1.0 MPa per point (my calculation), which is 3–6× the reading error.

I refit with that error (χ², calculations):

| fish | const χ² / dof (p) | trans p | shear p | clamp-offset p |
|---|---|---|---|---|
| 13 | 22.9 / 4 (<0.001) | 0.27 | 0.40 | 0.43 |
| 12 | 23.2 / 3 (<0.001) | 0.86 | 0.73 | 0.66 |
| 5 | 78.0 / 4 (<0.001) | 0.96 | 0.89 | 0.74 |
| 11 | 29.8 / 3 (<0.001) | 0.96 | 0.98 | 0.96 |
| 4 | 0.70 / 1 (0.40) | 0 dof | 0 dof | 0 dof |

- **The rigid-clamp rejection survives the relaxed yardstick.** This part of the claim is robust.
- **"Fits within reading error" was the wrong test.** With honest error bars, the series models fit
  comfortably. That is unsurprising for 2 parameters on 4–5 points. They are therefore not
  distinguished from each other.

## 3. The assumption that carries the number: which compliance form is used

E_∞ is an extrapolation beyond every observed value. The rising limb fixes the shape at short span
but not the asymptote, so the asymptote is set by the form chosen.

I added the form the author raised but never fitted: an effective clamp δ proximal of p0, so that
E_app = E(L/(L+δ))³. All results are calculations.

| form | fitted δ or term | whole-fin EI range (N·m²) | t = 11 µm plate bound | t = 16.5 µm |
|---|---|---|---|---|
| translational root (claim) | b = 4.5–11.7 mm³ | 2.1–6.1 × 10⁻⁹ | ≤ 11.5 GPa | ≤ 3.4 GPa |
| core shear (claim) | c = 2.1–11 mm² | 3.2–8.3 × 10⁻⁹ | ≤ 15.6 GPa | ≤ 4.6 GPa |
| clamp offset (claim's §1, unfitted there) | δ = 0.5–1.8 mm | **4.5–13.7 × 10⁻⁹** | **≤ 25.8 GPa** | ≤ 7.6 GPa |

These forms are not equally plausible a priori, and the table should be read with that in mind:

- **The offset form is not driven by the claim's outlier fish.** The claim dismissed its own
  rot + trans fit (1.66 × 10⁻⁸) as "driven by fish 13's unconstrained fit". The offset form is
  different. Without fish 13, fish 12 and fish 5 give ~12.5 × 10⁻⁹. My Monte Carlo 16–84% interval
  for fish 5 is 10.4–15.0 × 10⁻⁹ (400 draws at Puri's stated SDs; calculation).
- **The offset form is probably an over-correction.** It assumes the hidden segment proximal of p0
  bends with the fin's own EI. The peduncle and hypural region is probably stiffer than the fin, and
  that would pull the true correction back toward the translational form. This is my inference; I
  found no measurement of peduncle EI.
- **Even the claim's own forms are uncertain.** The shear form's Monte Carlo interval for fish 13 is
  6.7–11.0 × 10⁻⁹. Its upper end is set by fish 13, the fish the claim concedes does not fit within
  reading error.

**Consequence.** A defensible statement is: whole-fin bending-only EI is ~2–14 × 10⁻⁹ N·m²
(calculated, form-dependent), with the form unidentified. The stated "~2–8 × 10⁻⁹" is the
low-correction half of that.

**What this does to the bone comparison.** S9-D asked whether the uncoupled-hemitrich bound sits
below vertebral bone E. Under the offset form, the t = 11 µm bound reaches the 23–25 GPa vertebral
value. So the claim's "narrows but does not close" holds for the translational and shear forms only.
That vertebral E is itself search-summary only (inherited from S9), which further limits how firm any
"gap" statement can be.

## 4. Proxy check

- **Under reading (ii), the corrected number answers a different question.** If the compliance is
  core shear (real biology), then "corrected EI" = E_∞·I is the beam-bending term only. The
  structural stiffness a fin actually presents at short span is the uncorrected F/y. The claim
  acknowledges this in its body (§4, claim 2), but the headline "is a lower bound" drops the caveat.
- **Under reading (iii), it is not a lower bound at all.** Reading (iii) is a genuine proximal rise
  in E. Then EI_app is the correct span-averaged stiffness, and nothing is bounded.
- **The headline therefore overstates the body.** The claim's own §3/§5 says the fit cannot
  separate (i), (ii) and (iii). "The reported 1.5–4 × 10⁻⁹ is a lower bound" should read: "is a lower
  bound on bending-only EI *if* the rise is series compliance".

## 5. Regimes and mechanisms the author missed (inference, not tested)

Two more mechanisms produce the same constant-compliance signature (the b/L³ form). Both are artefacts,
so both push in the same direction as reading (i). This strengthens the "the true EI is higher if it is
an artefact" direction and weakens any attribution to the foam mount specifically.

- **Local contact or indentation compliance at the 0.4 mm pin.** The pin size is from Puri's
  full-text Methods.
- **Through-thickness compression of the soft fin base.**

A related observation from Puri's full-text:

- **Facts (full-text):** deflections went up to 2 mm at spans as short as ~1.3 mm (y/L up to ~1.5),
  and Puri reports force–deflection curves of "a high degree of linearity" up to 2 mm.
- **My inference:** bending a slender beam to y/L ~ 1 would normally be geometrically nonlinear.
  Linearity at that level is mild support for a large linear non-bending compliance at short spans.
  That is consistent with the claim's direction, but I did not model the elastica.

On the descending limb:

- **The claim fits only the points up to each fish's maximum.** Constant E plus any monotone series
  compliance cannot produce the later decline. So constant E is already contradicted on the full
  curve unless I(L) is wrong distally, and assuming it on the rising limb is a choice, not a finding.
  The claim admits this. I flag it because it limits how much weight E_∞ can carry.

## 6. Evidence-level check

- **The claim's sentence is honest.** It labels the corrected values "(calculated)" and calls the
  inputs plot readings.
- **The recorded level is a mislabel.** The claim is recorded as "literature", but its key number is
  a calculation on the author's own raster-plot readings. The record should read
  "calculation (on literature plot readings)".
- **Fish count.** All five intact fish come from one study (Puri 2018; n = 5 intact).
- **Replication.** I did not repeat the author's search for independent replication. My verdict does
  not depend on it.

## Sources

- **Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018).** *J. Exp. Biol.* 221:jeb171777,
  PMC5868929.
  - **full-text** (Europe PMC `fullTextXML`, read this session). I used: foam-pad fixation; the
    0.4 mm pin and line load; deflection ≤ 2 mm; "high degree of linearity"; SDs of ±0.1 mm in L,
    ±20 µm in y and ±5 µN in F; 16–18 rays; abstract range 1.5–4 × 10⁻⁹ N·m².
  - **Supplement: not re-read.** Fig. S5B/S5C values are **the claim author's plot readings**, which
    I used unchanged.
- **The claim document and script** (`S9-D-deepen.md` and `S9-D-deepen_calc.py`): full-text.
- **Vertebral E 23–25 GPa:** inherited from S9, search-summary. I did not re-open it.
- **Hemitrich t = 11–16.5 µm:** inherited from S9-D (PMC12956070). I did not re-open it.

```swarm-challenge
{"claim_id": 125, "outcome": "weakened", "reason": "The qualitative answer and the rigid-clamp misfit survive refitting with Puri's own measurement SDs (const-E chi2 p<0.001 in 4 fish), but the corrected EI is set by an unidentified compliance form: the clamp-offset form the claim itself raised fits as well (p=0.43-0.96) and gives ~4.5-14e-9 N m^2, which lets the t=11 um uncoupled-plate bound reach ~24-26 GPa (vertebral E), so the '~2-8e-9' range and 'narrows but does not close' are form-dependent, and 'lower bound' holds only if the rise is series compliance.",
  "corrected_value": "zebrafish whole caudal fin bending-only EI ~2-14e-9 N m^2 (calculated, form-dependent: translational 2.1-6.1e-9, core-shear 3.2-8.3e-9, clamp-offset 4.5-13.7e-9; form not identified by the data); reported 1.5-4e-9 is a lower bound only under the series-compliance readings",
  "depends_on": [
    "Puri et al. 2018 J Exp Biol 221:jeb171777 Fig. S5C E_eff(L) for 5 intact fish, as read off the plot by the claim author (not re-digitized by me)",
    "Puri et al. 2018 Fig. S5B ray-only I_eff(L), claim author's plot reading",
    "Puri et al. 2018 stated SDs: L +-0.1 mm, deflection +-20 um, force +-5 uN (full-text, Fig. 2 legend)",
    "Puri et al. 2018 methods: foam-pad peduncle fixation, 0.4 mm pin line load, deflection <=2 mm, EI=(F/y)L^3/3 (full-text)",
    "Series-compliance model forms: translational b/L^3, shear c/L^2, clamp offset (L/(L+delta))^3, fitted to the rising limb only",
    "S9-D hemitrich wall thickness t = 11-16.5 um and uncoupled flat-plate model with 16 rays, w = 150 um (not re-read)",
    "S9 zebrafish vertebral nanoindentation E ~23-25 GPa (search-summary only)"
  ]}
```
