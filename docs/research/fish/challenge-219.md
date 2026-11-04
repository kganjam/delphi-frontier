# Challenge 219: Is the downstream EI recomputed from the 1.98 N/m fin-ray slope valid?

**Claim under review (I did not write it):**
> Alben, Madden & Lauder 2007 (PMC2359861, full text via challenger): 1.98 N/m is a TRANSFER
> stiffness. An excised bluegill pectoral ray was clamped at the base with both hemitrich bases fixed,
> a vertical point force was applied at ~2/3 base-to-tip, and the slope was fitted against TIP
> deflection. One-base-free ≈ 0.165 N/m by the paper's 12× ratio. … DOWNSTREAM: claim 93 used
> EI = kL³/3 (tip load); for load at 2/3 L and tip deflection, EI = 0.1728·k·L³ = 2.24e-5 N m², which
> is 1.93× lower than 4.3e-5 (recomputed).

Recorded level: literature. Value: 1.98 N/m. Source: `challenge-214.md` on branch
`claude/challenge-214-fish-stiffness-cml8qn`.

**Verdict: WEAKENED.** The description of the experiment survives my own reading of the full text.
The arithmetic is correct. But the downstream EI = 2.24e-5 N m² is still a proxy. It inverts an
Euler–Bernoulli single-beam formula for a ray that the same paper says is shear-coupled. The source
the claim cites (challenge 214) says this itself: in that regime the beam-theory conversion factor
"is not a valid conversion factor for this ray". So the claim replaces one invalid inversion (tip
load) with another (load at 2/3 L). The corrected number should not be used as a bending rigidity.

## Sources and read-levels

| Source | Route | Read-level |
|---|---|---|
| Alben, Madden & Lauder 2007, J R Soc Interface 4:243–256, PMC2359861 | `curl` to pmc.ncbi.nlm.nih.gov and www.ncbi.nlm.nih.gov/pmc → reCAPTCHA "Checking your browser" page (21 kB, no article) | could-not-access |
| same | WebFetch of `https://pmc.ncbi.nlm.nih.gov/articles/PMC2359861/` | full-text, but read **through a summarising model**, which gave quotes of at most 125 characters and paraphrased the rest. I did not see the figures themselves. |
| same | Europe PMC fullTextXML / fulltextRepo → HTTP 500; royalsocietypublishing.org PDF → 403 | could-not-access |
| challenge-214.md (branch above) | git | full-text |
| Claim 93 (EI = 4.3e-5) | `git grep` for `4.3e-5`, `kL^3`, `1.98 N` across all three remote branches visible here | could-not-access. Not present in any branch I can see, so I judge it only as the claim describes it. |

## 1. What I confirmed from the paper

These are the authors' words as returned by WebFetch.

- **Figure 7a:** "The ray is clamped horizontally at the base"; "a vertical point force is applied at
  two-thirds of the distance from the ray base to the tip". The slope is "1.98 N m−1", which is
  "about 12 times the value when one hemitrich is free".
- **§5.2:** "a probe pushes down on the fin ray at approximately two-thirds of the distance from the
  base to the tip" and "the force on the probe is measured as a function of tip deflection of the
  ray". The bases are either both clamped (ϕ0 = 0) or one is free.
- **§2:** "maximum ray length = 40.3 ± 0.8 mm". §3.4 uses L = 4 cm for "a typical bluegill fin ray".
  Mechanics were done on "24 separate rays".
- **Measured bending rigidity:** "the measured B = EI ≈ 10⁻⁶–10⁻⁵ J m" and, elsewhere,
  "we obtain B ≈ 10⁻⁶ J m".

The claim's description of the boundary condition matches these quotes. The figure 7a caption says
"deflection of the ray" and §5.2 says "tip deflection". The claim takes the tip reading without
noting the difference. Challenge 214 did flag it.

## 2. Arithmetic, redone independently

My inputs are k = 1.98 N/m, L = 0.0403 m and a = 2L/3. All values below are **calculated**. None of
them are measured.

- **Claim 93 as described:** kL³/3 = 4.32e-5 N m². Solving 4.3e-5 = kL³/3 back for L gives
  40.2 mm, so claim 93 evidently used the maximum ray length.
- **Tip deflection for a load at a:** δ_tip = P·a²(3L − a)/(6EI). At a = 2L/3 the coefficient is
  (4/9)(7/3)/6 = 28/162 = **0.17284**, so EI = 0.17284·k·L³ = **2.240e-5 N m²**.
  - Ratio to claim 93's value: 4.32/2.24 = **1.929**. The claim's "1.93×" is correct.
- **If the caption's "deflection" means load-point deflection:** the coefficient is
  (2/3)³/3 = 0.0988, which gives EI = 1.28e-5 N m². That is 1.75× lower again. This unresolved
  difference between caption and text moves the "corrected" value by 1.75×.
- **Sensitivity to L (EI ∝ L³):** L = 30, 35, 40.3 and 45 mm give 0.92, 1.47, 2.24 and
  3.12 (×1e-5 N m²).
  - 40.3 mm is the *maximum* ray length, a mean over 6 fishes.
  - Figure 2a shows ray 4 of 13. The length of the ray behind figure 7a, and its free length beyond
    the clip, are `unknown` from what I could read.
  - "Approximately two-thirds" adds further spread.

## 3. Proxy: the effective stiffness is not EI

This is the hidden assumption that carries the result. EI = 0.1728·k·L³ treats the ray as one
homogeneous Euler–Bernoulli beam. The paper's whole point is that it is not one: two hemitrichs are
coupled by an interray shear layer.

- With both bases clamped, the stiffness rises with the shear modulus G. Per the figure 7b
  paraphrase, at large G "the slope grows roughly in proportion to G".
- The experimental 12× ratio is matched near G ≈ 10².
- So the both-clamped slope is mostly shear-coupling stiffness, not hemitrich bending.

**Test with the assumption relaxed.** Apply the same formula to the one-base-free slope,
0.165 N/m. That slope is derived from the paper's 12× ratio, not read off the figure. When one base
is free, the coupling cannot carry a base moment.

- Result: 0.17284 × 0.165 × 0.0403³ = **1.87e-6 N m²**. This is my calculation.
- That sits inside the paper's own measured B ≈ 10⁻⁶–10⁻⁵ J m, and close to its "B ≈ 10⁻⁶".
- The both-clamped inversion, 2.24e-5, lies **above the top of the paper's measured B range**.

My inference: the 1.98 N/m slope gives an *apparent* or effective flexural rigidity. That value
includes about an order of magnitude of shear-coupling stiffening. It is not the material EI of the
ray.

Whether claim 93 needs that effective value or the bending rigidity depends on what it models,
which I could not read:

- A passive, base-locked ray under a distributed hydrodynamic load: the effective value may be
  defensible. But a single-point-load inversion still does not transfer to a distributed load in a
  shear-dominated beam, because the deflection shape differs.
- Anything that needs EI as a material or section property: the paper's measured B is the right
  input, and 2.24e-5 is too high by about 2–20×.

## 4. Evidence level

- **1.98 N/m as "literature":** honest. It is a measured linear-fit slope (figure 7a, experiment
  panel).
- **0.165 N/m:** derived from "about 12 times". The claim labels it that way ("by the paper 12x
  ratio"), which is acceptable. It is not a reported measurement, and "about" carries its own
  uncertainty.
- **2.24e-5 N m²:** a calculation that rests on a model assumption the source paper contradicts. The
  claim says "recomputed" but does not say it is still a single-beam inversion. That omission is a
  defect in presentation, not in the arithmetic.
- **"n" behind the 1.98:** 24 rays were tested in total. The number of rays behind the 1.98 slope
  is `unknown` from my read. It looks like one representative curve.

## 5. Other regimes and counter-examples

- **Actuation state:** with ϕ0 = 0 (both bases fixed), no muscle is shifting the hemitrichs. The
  paper's subject is active curvature control, where the base offset changes. Stiffness under
  active base offsets is outside this number.
- **Nonlinearity:** the curve is "linear with an offset", and collagen stiffening is modelled in
  figure 6c. The slope depends on the force range fitted.
- **Taxa:** I searched no taxa other than *Lepomis macrochirus* for this check. That search had zero
  scope.

## What survives and what does not

- **Survives:** the boundary condition (both bases clamped, load at about 2/3 L, slope against tip
  deflection per §5.2), the value 1.98 N/m, the derivation of 0.165 N/m, and all of the arithmetic
  (0.1728, 2.24e-5, 1.93×).
- **Does not survive as stated:** "EI = 2.24e-5 N m²" as a corrected bending rigidity for claim 93.
  - It is an apparent EI, from an Euler–Bernoulli inversion of a shear-coupled ray.
  - It is about 1.75× lower if the caption's load-point reading is right.
  - It changes with L³ when the true free length is unknown.
  - It exceeds the paper's own measured B ≈ 10⁻⁶–10⁻⁵ J m.

```swarm-challenge
{"claim_id": 219, "outcome": "weakened", "reason": "The boundary condition, the 1.98 N/m value and the 0.1728kL^3 = 2.24e-5 N m^2 arithmetic all check out, but that EI comes from an Euler-Bernoulli single-beam inversion of a both-bases-clamped ray. The same paper places that ray in the shear-coupled regime (G~10^2, 12x stiffening), so 2.24e-5 is an apparent stiffness above the paper's own measured B ~1e-6 to 1e-5 J m, not a bending rigidity. It also shifts 1.75x with the unresolved caption-versus-text deflection location and with L^3.", "corrected_value": "1.98 N/m stands (measured transfer stiffness). The downstream 2.24e-5 N m^2 is only an apparent EI for the base-locked ray, with a range of about 1.3e-5 to 2.2e-5 N m^2 for load-point versus tip deflection at L = 40.3 mm. For bending rigidity, use the paper's measured B ~1e-6 to 1e-5 N m^2. The one-free inversion is 1.9e-6 N m^2, calculated.", "depends_on": ["Alben, Madden & Lauder 2007 J R Soc Interface 4:243-256 PMC2359861, full text via WebFetch summary, Figure 7a caption (2/3 load point, 1.98 N/m, about 12x)", "same source, section 5.2 'force ... measured as a function of tip deflection'", "same source, measured B = EI ~1e-6 to 1e-5 J m and B ~1e-6 J m", "same source, Figure 7b: experimental ratio matched near G ~1e2, with stiffness growing with G at large G", "same source, section 2 maximum ray length 40.3 +/- 0.8 mm", "claim 93 EI = kL^3/3 = 4.3e-5 N m^2 as described in the claim (not readable in this repo)", "challenge-214.md on branch claude/challenge-214-fish-stiffness-cml8qn"]}
```
