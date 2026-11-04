# Challenge 159: adversarial review of S26 (active fin-ray stiffening)

**Claim under review (author: harvest `active-fin-ray-stiffening-l53vks`, file `docs/research/fish/S26-organ.md` on branch `claude/active-fin-ray-stiffening-l53vks`, read in full):**
"No on current evidence: the only measured active (hemitrich base-locking) stiffening factor is ~12x (one bluegill ray), leaving a zebrafish-scale ray ~14x short of 6.3e-4 N m^2, and even the modelled ~100x ceiling is 1.65x short; it could close only if the requirement is per-fin and shared across >=14 rays, or if an unverified in-vivo bluegill EI of 5.65e-4 N m^2 reflects a much larger active effect."
Recorded evidence level: derived.

**Verdict: SURVIVED.** One of the claim's two escape routes is narrower than it says (section 5), which makes the "no" stronger, not weaker. There is also one wording defect (section 2) that does not change the number.

---

## 1. Arithmetic, redone independently (computation, not observation)

Inputs are taken exactly as the claim takes them: EI_req = 6.3e-4 N m^2 and passive gap = 165x. Both come from S6, which neither the author nor I could find in this repository. Everything below rests on those two numbers.

| Step | My result | Claim | Match |
|---|---|---|---|
| EI_passive = 6.3e-4 / 165 | 3.818e-6 N m^2 | 3.8e-6 | yes |
| x12 (measured locking ratio) | 4.58e-5 N m^2, short by 13.75x | ~14x | yes |
| x100 (model asymptote) | 3.82e-4 N m^2, short by 1.650x | 1.65x | yes |
| Rays needed under perfect sharing at 12x | 165/12 = 13.75, so N >= 14 | >=14 | yes |
| d/t for R = 1 + 3(d/t)^2 = 165 | 7.39 (and 5.74 for R = 100) | 7.4 / 5.7 | yes |

I also re-derived R = 1 + 3(d/t)^2 independently from the parallel-axis theorem. The extra term 2E·bt·(d/2)^2 divided by 2E·bt^3/12 gives 3d^2/t^2. That matches.

| Step | My result | Claim | Match |
|---|---|---|---|
| s needed for the in-vivo value, s^4 >= 6.3/5.65 | s >= 1.028 | 1.03 | yes |
| s = 0.25 | EI = 2.21e-6 N m^2, short by 285x | 285x | yes |

No arithmetic error found. The "~14x short" is really scale-free: it is 165/12, and it holds for any ray whose passive EI is S6's.

## 2. Proxy check: is "12x" the active stiffening factor?

Alben, Madden & Lauder, *J R Soc Interface* 2007, PMC2359861 (read-level: **full-text**, through a page summarizer, the same route the author used).

What the paper measured is the point-load stiffness with both hemitrich bases clamped, divided by the stiffness with one base free. The load sits at 2/3 of the ray length. The ratio is "about 12 times"; I confirmed this. That is a bench boundary-condition ratio. It is **not** a ratio of muscle-locked to relaxed stiffness in a living fish.

- The right quantity is EI with the bases held by contracted muscle, divided by EI of the intact ray with relaxed muscle and ligaments.
- In the intact relaxed ray, the bases are partly tethered, so its baseline is stiffer than "one base free". My inference: the true active factor is therefore **at most** about 12x, unless muscles hold more rigidly than a bench clamp, which is implausible.
- So the proxy is biased **in the claim's disfavour**: the real factor is likely smaller, and the gap larger.
- The author flags this (S26 sections 3 C2/A1 and 5). The one-line claim still calls the 12x a "measured active ... stiffening factor". That wording is slightly loose. The value itself is correctly labelled *measured* (n = 1 ray).

## 3. Hidden assumption: does the 12x survive shrinking to zebrafish size?

This is the assumption most likely to carry the result. The claim applies a bluegill factor to a much smaller ray.

The paper scales the shear parameter as G_nd = G_dim·L^2/B0. Here G_dim is the shear modulus times the cross-sectional area of the intraray material (confirmed in the full text).

My inference: under isometric scaling with the same materials, G_dim ∝ s^2, L^2 ∝ s^2 and B0 ∝ s^4. So G_nd is **size-invariant**, and the ~12x (G ~ 1e2) transfers unchanged.

Relaxing isometry (my inference): a relatively thinner intraray layer in a small fish would change G_nd. Its sign is `unknown`, because no zebrafish histology was found. The clamped/free ratio rises with G toward about 100. So reaching 165x needs G well above the asymptote regime, and the paper's model never exceeds about 100 at any G. Relaxing the assumption therefore cannot rescue the claim through G alone. Only the cross-section geometry could, and that is the d/t > 7.4 condition in C4.

One caveat on "~100x ceiling". The paper does not show whether the asymptote depends on hemitrich thickness or separation; its calculations use uniform rays. So "~100x" is the asymptote for the modelled bluegill geometry, not a universal ceiling. A zebrafish ray with larger d/t could in principle have a higher one. The author's C4 already states that the true cap is geometric, and that zebrafish d/t is `unknown`. I could not find d/t either. This is a residual uncertainty, not a break.

## 4. Evidence level

**derived** is honest:
- 12x: measured.
- 14x, 1.65x, 13.75 rays: arithmetic on measured and upstream inputs.
- 100x: model.

The claim keeps these apart. No derived number is presented as observed.

## 5. Counter-evidence and regimes the author missed

**(a) The per-fin escape route is nearly closed.** The claim leaves open that the requirement might be per-fin and shared across at least 14 rays, and S26 states the zebrafish ray count is `unknown`.
- A search turned up a 2019 study, *Zoological Letters*, doi:10.1186/s40851-019-0145-z (read-level: **search-summary**). In RW wild-type zebrafish, pectoral fins had **11-13 rays** (11: n = 6; 12: n = 43; 13: n = 9; 56 fins from 29 fish). The earlier literature it cites gives a range of 10-14.
- My inference: N >= 14 is reached only at the very top of the literature range, and never in that sample. It would also need perfect, equal load sharing. That is unrealistic: S26's M8 notes that stiffness varies about 30x proximal-to-distal, and short marginal rays do not span the fin.
- So escape (a) essentially fails. This **strengthens** the "no".

**(b) The in-vivo value is now abstract-confirmed, but that does not rescue the claim.** I found the 565e-6 N m^2 flexural stiffness from Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044-1059, at read-level **search-summary/abstract**. The full text was not read.
- The abstract says the value was "calculated" from an in-vivo vortex-jet impact (67 ± 2.3 mN). It is not a bending test.
- The abstract also gives a maximum curvature of 9.38 mm^-1. So the author's suspicion of a summarizer unit error is not borne out at abstract level, although the value is still physically odd.
- Whether the 565e-6 reflects an active state is still `unknown`.
- Even taken at face value, it belongs to a ~40 mm bluegill ray. Under the claim's own isometric scaling, a zebrafish ray would need s >= 1.03. That is a ray at least as long as a bluegill's, which is impossible on a fish about 3-4 cm long (zebrafish ray length itself: `unknown`, not retrieved).
- Escape (b) therefore cannot close the gap for a zebrafish-scale ray unless EI does not scale with size. Its real force is narrower: it suggests live rays may be much stiffer than excised ones. That bears on whether S6's passive baseline is right, which is outside this claim.

**(c) Taxa.** No locked-vs-sliding measurement exists in any cyprinid, or in any species other than bluegill/sunfish, within my searches: two web searches plus one full-text re-read. No published counter-example showing more than 100x bilaminar gain was found within that scope.

## 6. Why it survives

- The arithmetic is exact.
- The main proxy (bench clamp ratio standing in for active gain) is biased toward overstating the active factor.
- The key scaling parameter is size-invariant under isometry.
- The newly found ray count (11-13) removes most of the per-fin escape route the claim left open.

The verdict remains conditional on S6's 6.3e-4 N m^2 and 165x, which were never re-derived. If those fall, this verdict falls with them.

Sources:
- [Alben, Madden & Lauder 2007, PMC2359861](https://pmc.ncbi.nlm.nih.gov/articles/PMC2359861) (full-text, via summarizer)
- [Flammang et al. 2013 J Morphol, Harvard PDF](https://sites.harvard.edu/glauder/files/2022/03/Flammang.etal_.2013.JMorph_finrays.pdf) (search-summary)
- [Flammang et al. 2013, Deep Blue listing](https://deepblue.lib.umich.edu/items/6e7cdcba-86b4-478b-ab98-949fbcf76812) (listing)
- [Zoological Letters 2019, s40851-019-0145-z](https://link.springer.com/doi/10.1186/s40851-019-0145-z) (search-summary)

```swarm-challenge
{"claim_id": 159, "outcome": "survived", "reason": "The arithmetic re-derives exactly (165/12 = 13.75x short; 165/100 = 1.65x), the bench clamp/free proxy if anything overstates the true active factor, the shear parameter G is size-invariant under isometry, and a zebrafish pectoral ray count of 11-13 (search-summary) leaves the claim's own per-fin escape route (>=14 rays) essentially closed.",
  "corrected_value": null,
  "depends_on": ["S6 EI_req = 6.3e-4 N m^2 (upstream, not re-derived)", "S6 passive gap = 165x (upstream, not re-derived)", "Alben et al. 2007 clamped/one-free stiffness ratio ~12x (measured, n=1 bluegill ray)", "Alben et al. 2007 model asymptote ~100x at G>1e5 (model, bluegill geometry)", "zebrafish pectoral ray count 11-13, literature 10-14 (Zool Lett 2019, search-summary)", "Flammang et al. 2013 bluegill in-vivo EI 565e-6 N m^2 (calculated, abstract/search-summary)"]}
```
