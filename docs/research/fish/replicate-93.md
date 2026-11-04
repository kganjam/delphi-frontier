# Replicate 93: does S6-D-D falsify S6-D's "passive-ray mechanism falls" verdict?

**Status:** an independent re-derivation. **Calculation and literature only. Nothing here was measured by me.**
Each number is tagged *reported* (by the cited authors), *calculated* (by me, in
[`replicate-93_calc.py`](replicate-93_calc.py); run it with `python3 -I`), or *assumption*.

## Contamination disclosure (read this first)

Blindness was only partial, for two reasons:

1. **The commit subject.** To find the files, I ran `git log` on `origin/claude/deepen-s6-d-sensitive-input-fc1hm8`.
   The subject and first body lines of commit `dc6acca` were printed before I could avoid them:
   *"the passive-ray 'falls' verdict falls to unresolved"*. The lines also gave β = 0, "1.98 N/m", "EI ≤ 4.3e-5 N m²"
   and "40 mm bluegill → ~120 mm flying-fish ray". So I knew the direction of the recorded answer before I derived anything.
2. **The doc's preamble.** The task says the inputs live in `S6-D-deepen.md`. I read lines 1–40 only: §0, which
   restates S6-D's claim and inputs, and the first lines of §1. I stopped there because §1 begins the author's
   working. I read the rest of the doc only after my derivation was finished (see Comparison).

The original S6-D file (`docs/research/fish/S6-deepen.md` on `origin/claude/deepen-fin-ray-s6-cj2i2x`) is not on
any branch fetched in this session. I did not read it. S6-D's claim below is as S6-D-D's §0 relays it.

## The claim being tested

As S6-D-D §0 relays it, S6-D models one lepidotrichial ray as an equal-share, uniform-load Euler–Bernoulli
cantilever. It requires a tip deflection of δ/L ≤ c and concludes that the passive ray "falls".

## Inputs

| Input | Value | Source | Read-level | Tag |
|---|---|---|---|---|
| Fish mass m | 0.10 kg | S6-D, via S6-D-D §0–1 | listing (secondary relay) | assumption (S6-D's) |
| Flying-fish ray length L | 0.12 m | same | same | assumption (S6-D's) |
| Rays per fin N, 2 fins | 14 | same | same | assumption (S6-D's) |
| Deflection criterion c | 0.10 | same | same | assumption (S6-D's) |
| Bluegill ray, force–displacement slope, both hemitrich bases clamped | 1.98 N m⁻¹ | Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, doi:10.1098/rsif.2006.0181, PMC2359861 | full-text, via WebFetch summarizer (verbatim quotes requested; I did not read the PDF directly) | reported |
| Point of load application | "about two-thirds of the way along the ray" | same | same | reported |
| Bluegill maximum ray length | 40.3 ± 0.8 mm | same | same | reported |
| Authors' EI estimate | "B = EI ≈ 10⁻⁶–10⁻⁵ J m" (J m = N m²) | same | same | reported |
| Bluegill pectoral ray flexural stiffness | 565 × 10⁻⁶ N m², "calculated" by the authors | Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161 | abstract (Europe PMC) | reported |
| 3.8 × 10⁻⁶ N m² | — | S6-D, via §0; S25 reports it as untraced | listing | provenance unknown |
| Scaling exponent β in EI ∝ L^β, bluegill → Exocoetidae | **unknown** | No source found. Scope: I searched for nothing beyond the two papers above. I did not search the allometry of lepidotrichia | — | — |

The Flammang abstract has an internal tension. It calls the ray "very flexible", with "small bending rigidity",
yet gives 565 × 10⁻⁶ N m². That value is 13–130 times larger than the Alben range for the same species and ray. My
inference, not the authors' claim, is that this could be a unit or rendering issue, or a different (active or
whole-ray) condition. The full text is unread, so I cannot resolve it.

## Arithmetic (all *calculated*)

**Required EI.** With a uniform load w = P/L on a cantilever, δ_tip = wL⁴/(8EI), so δ/L = PL²/(8EI).

- P = mg/(2N) = 0.10 × 9.81 / 28 = 0.03504 N.
- EI_req = PL²/(8c) = 0.03504 × 0.0144 / 0.8 = **6.31 × 10⁻⁴ N m²**.

**EI from the Alben measurement.** A point load at distance a from the clamp gives deflection Fa³/(3EI) under the
load, so EI = k a³/3.

- Load at a = (2/3)(0.0403 m) = 0.02687 m, as Alben reports: EI = 1.98 × 1.939×10⁻⁵ / 3 = **1.28 × 10⁻⁵ N m²**.
  This sits at the top of the authors' own 10⁻⁶–10⁻⁵ range, so the two values are consistent.
- Load at the tip, a = 0.0403 m: EI = 1.98 × 6.545×10⁻⁵ / 3 = 4.32 × 10⁻⁵ N m². This is an upper bound only, and
  Alben's stated load point makes it loose.

**Transfer to L = 0.12 m.** λ = 0.12 / 0.0403 = 2.978, and λ⁴ = 78.6. The exponent needed to flip the verdict is
β_flip = ln(EI_req / EI_bg) / ln λ.

| EI_bg (N m²) | β = 0: EI/EI_req | β = 0: δ/L* | β = 4: EI/EI_req | β_flip |
|---|---|---|---|---|
| 1.28×10⁻⁵ (Alben k, 2/3 load) | 0.020 (×49 short) | 4.9 | **1.60 (passes)** | 3.57 |
| 4.32×10⁻⁵ (Alben k, tip bound) | 0.068 (×14.6 short) | 1.46 | 5.38 (passes) | 2.46 |
| 1×10⁻⁵ (Alben upper) | 0.016 | 6.3 | 1.25 (passes) | 3.80 |
| 1×10⁻⁶ (Alben lower) | 0.0016 | 63 | 0.125 (fails) | 5.91 |
| 3.8×10⁻⁶ (untraced) | 0.006 | 16.6 | 0.47 (fails) | 4.68 |
| 5.65×10⁻⁴ (Flammang, abstract) | 0.90 | 0.112 | 70 | 0.10 |

\*Any δ/L > ~0.2 is outside small-deflection beam theory. These rows mean "fails grossly", not a literal deflection.

## Result

The original S6-D question asks whether a passive ray can carry its share of glide lift. **My value: unresolved.**
S6-D's verdict that "the passive-ray mechanism falls" is not supported as stated. I mean that it is not established
in either direction, not that the opposite has been shown.

- With S6-D's implicit β = 0, every Alben-derived passive value fails, by ×15–630. So the "falls" verdict
  holds, and holds more firmly than S6-D said: the only marginal pass was the Flammang value, whose status is
  unclear.
- With isometric scaling (β = 4), the Alben measured-k value passes, with margin ×1.6 at Alben's stated load point
  and ×5.4 at the tip bound.
- The verdict flips at β ≈ 2.5–3.6 for the measured k, and at β ≈ 3.8–5.9 across the authors' range. No source I
  found gives β for lepidotrichia between bluegill and Exocoetidae. That makes β the deciding input, and it is
  `unknown`.
- Uncertainty: the ±0.8 mm in ray length changes a³ by about ±6%, which is negligible next to the β dependence. The
  load-side assumptions (m, L, N, c) are S6-D's own and were not re-sourced here.

So S6-D-D's claim that its deepening makes S6-D's verdict fall is **correct as a falsification of S6-D's
conclusion**. My inference is that the conclusion goes to *unresolved*, not to its negation.

## Comparison with the recorded value (read only after the derivation above)

S6-D-D §4 says: **"Verdict on S6-D's conclusion: FALLS."** Its supporting numbers are an EI_req of 6.31×10⁻⁴, an
Alben-k bound of ≤4.3×10⁻⁵ with δ/L 1.46 at β = 0, β ≥ 2.5 for the k-bound, β ~3.8–5.9 across Alben's range, and
3.4×10⁻³ "yes" at β = 4. Mine match all of these.

There is one small difference. S6-D-D uses the tip-load upper bound and treats the load point as a range (10–30 mm).
Alben 2007 states the load point (≈2/3 of the length, ~27 mm). That gives a point estimate of 1.28×10⁻⁵ N m² and
β_flip of 3.57. This tightens the numbers but does not change the verdict.

**AGREE.** The contamination disclosed above weakens this as independent evidence: I knew the direction of the
recorded answer in advance. The arithmetic and the Alben inputs were re-derived from the primary source.

```swarm-replication
{"claim_id": 93, "my_value": "S6-D verdict falls to unresolved: passive ray fails at beta=0 (EI 1.3e-5 N m^2 vs 6.3e-4 required, x49 short) but passes at isometric beta=4 (x1.6); flip at beta~2.5-3.6, beta unknown", "agrees": true,
  "note": "Re-derived from Alben 2007 (load at 2/3 length gives EI=1.28e-5 N m^2, tighter than the recorded tip bound 4.3e-5) and matches the recorded FALLS verdict, but blindness was partial because the recorded commit subject was seen before deriving."}
```
