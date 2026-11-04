# Challenge 193: adversarial review of the S28 tail-driven skim number

**Claim under review.** The claim comes from S28, branch `claude/s28-organism-design-5z0vjz`, file `docs/research/fish/S28-organism.md` §3.5. Its recorded evidence level is *derived*, with the value "16 percent of lift". The claim reads: "A tail-driven skim at the measured 52 Hz maximum reaches only 1.15–1.72 m/s, giving 7–16% of the lift needed."

**Outcome: WEAKENED.** I found no arithmetic error. The evidence label "derived" is honest. The qualitative conclusion also survives: the tail cannot drive a skim to the 4.37 m/s that full wing support needs, and no corner of my input box gets there. What does not survive is the word "only", along with presenting 1.72 m/s / 16 % as a ceiling. That range comes entirely from the author's Strouhal band of St 0.36–0.54. The band leaves out the lower half of the published cruising band, St 0.2–0.4, which the project's own replicate-36 used. Inside the defensible box the wing lift fraction at 52 Hz spans **≈2–50 % of weight**, not 7–16 %.

This was a desk review. I ran no experiment. Every number is labelled **calc** (my own arithmetic, done in Python one-liners), **measured** (literature, with read-level) or **assumed**.

## 1. Arithmetic, redone independently (calc)

The inputs are as stated in S28 §1: f = 52 Hz, peak-to-peak A = 0.0119 m, St = 0.36 and 0.54, and V_to = 4.37 m/s. Lift fraction = (U/V_to)² at CL_max, using case C's area.

- U = 52 × 0.0119 / 0.54 = **1.146 m/s**, giving (1.146/4.37)² = **6.9 %**. This matches the claim.
- U = 52 × 0.0119 / 0.36 = **1.719 m/s**, giving (1.719/4.37)² = **15.5 %**. This matches; the claim rounds it to 16 %.

**Structural observation (my inference).** S28 back-solved A from the project's taxi frequencies of 132–199 Hz, which were themselves computed at U = 4.37 m/s with the same St values. So A, St and V_to cancel. The claim is algebraically (52/132)² = 0.155 and (52/198)² = 0.069 (calc). In other words, it is the square of the S24/replicate-36 tail-frequency shortfall, restated. It is **not independent evidence**. It carries every assumption of that taxi calculation and adds none of its own. If the taxi shortfall is refuted, this claim falls with it.

## 2. Proxies

1. **52 Hz is an escape EMG burst maximum, not a sustainable tail-beat frequency.** It is measured: Kyriakatos et al. 2011, *J. Neurosci.* 31:8422, recorded across 8 adults of 18–30 mm. I did not read it myself; my read-level is listing, taken second-hand from `replicate-36.md` and `challenge-145.md` in this project, which read it at full-text. A skim is sustained locomotion. The same source gives a free-swimming maximum of 21 Hz ("never exceeding 21 Hz"). At 21 Hz on S28's own A and St, U = 0.46–0.69 m/s and the lift fraction is **1.1–2.5 %** (calc). This proxy makes the claim *generous* to the fish, which strengthens the negative.
2. **The Strouhal number is used as a speed ceiling.** St = fA/U describes the band where cruising swimmers and flyers are efficient. It is not a thrust cutoff. Taylor, Nudds & Thomas 2003, *Nature* 425:707, give the band as 0.2–0.4 (read-level: search-summary, via replicate-36). The speed a skimming tail actually reaches is set by thrust = drag. With the body out of the water, drag falls sharply, so the tail would settle at a *lower* St, not at 0.36–0.54. The quantity that matters is the thrust-balanced speed. Nobody in the project has computed it.

## 3. Hidden assumptions, relaxed (calc)

U and the lift fraction at 52 Hz, with V_to = 4.37 m/s:

| A (peak-to-peak) | St 0.2 | St 0.3 | St 0.36 | St 0.54 |
|---|---|---|---|---|
| 6.8 mm (0.2 L, Bainbridge 1958; other species; search-summary via replicate-36) | 1.77 m/s / **16.4 %** | 1.18 / 7.3 % | 0.98 / 5.1 % | 0.66 / 2.2 % |
| 10 mm (Gilbert et al. 2014, second-hand citation; listing) | 2.60 / **35.4 %** | 1.73 / 15.7 % | 1.44 / 10.9 % | 0.96 / 4.9 % |
| 11.9 mm (S28's value, back-solved and ≈ 0.4 SL) | 3.09 / **50.1 %** | 2.06 / 22.3 % | 1.72 / 15.5 % | 1.15 / 6.9 % |

- **St band.** This assumption carries the result. At the low edge of Taylor's band (St 0.2) with S28's own A, the lift fraction is **50 %**, three times the claimed maximum. Reaching 100 % (U = 4.37 m/s) at 52 Hz and A = 11.9 mm needs St = **0.14** (calc). That is below the published band, so "not a skim" still holds. It holds by a factor of about 1.4 in St, though, not by the 2.5–3.8× the claim implies.
- **Amplitude.** S28's A of 11.9 mm (≈ 0.4 SL peak-to-peak) is about 1.75× the measured maximum for other species, 0.2 L. This pushes the opposite way. At A = 6.8 mm the whole St 0.2–0.54 box gives 2–16 %, so the claim's upper value happens to coincide with the measured-amplitude/low-St corner. The two errors partly offset. The author's specific pairing of them is unsupported.
- **Independent cross-check by stride length** (my inference; it uses neither A nor St). For an undulating body, U ≤ body-wave speed. With U = (0.6–1.0 L per beat) × 52 Hz × 0.030 m, U = 0.94–1.56 m/s and the lift fraction is **4.6–12.7 %** (calc). This backs the claim's range for whole-body undulation. It does *not* apply cleanly to a skim, where only a lobe is in the water and behaves more like a heaving foil than a travelling wave.
- **The denominator ("the lift needed" = all of W from the wing).** S28 asserts, without calculation, that the submerged lobe gives "negligible buoyancy and little planing lift". Dimensional check (calc; the 10 mm² lobe area and lobe CL of 0.5 are **assumed**, not measured): ½ × 1000 × 1.5² × 10⁻⁵ × 0.5 = 5.6 mN, against W = 2.45 mN. Water is about 800× denser than air, so a small submerged lobe could in principle carry a large share of the weight at skim speeds. Whether a zebrafish's homocercal tail, oscillating laterally and piercing the surface (ventilation), produces any net vertical force is **unknown**. I found no measurement of it. The claim's "of the lift needed" therefore rests on an untested assumption. The direction of the error is unknown, and its size could be large.

## 4. Evidence level

"Derived" is correct. The claim does not present 7–16 % as measured. One minor point: S28's input table labels 52 Hz as "measured / project input" and does not say it is an escape EMG maximum. The claim's phrase "the measured 52 Hz maximum" is literally true, but it invites the reader to treat that frequency as sustainable.

## 5. Taxon counter-check: flying fish

Flying fish (Exocoetidae) taxi with only the lower caudal lobe in the water. The tail-beat sources disagree, and I report both without averaging them:

- A bioRxiv preprint ("Why does a flying fish taxi on sea surface before take-off?", 10.1101/765560; read-level: search-summary) cites **50–70 Hz** taxiing tail beats. It also implies about 41.7 Hz, and its CFD model uses 50 Hz at 10 m/s.
- An APS March Meeting 2024 abstract ("Flying fish taxiing on the water's surface"; read-level: search-summary) reports **13.5 Hz**, along with a minimum tail force of about 2 N for a 200 g fish.

On the 50 Hz figure and an *assumed* 25 cm body, a 10 m/s taxi is ≈ 0.8 body lengths per beat (my inference, calc). Scaling that to a 3 cm zebrafish at 52 Hz gives ≈ 1.25 m/s, inside the claim's range. On the 13.5 Hz figure, flying fish make ≈ 3 L per beat. If that held for zebrafish, it would give ≈ 4.7 m/s and break the claim. I cannot resolve the conflict between the two sources. The counter-example therefore supports the claim on one source and contradicts it on the other. Scope of this search: one standard web search ("flying fish taxiing tail beat frequency caudal lobe speed Exocoetidae"). I found no source giving lower-lobe amplitude or lobe vertical force.

## 6. Verdict

- **Holds:** the arithmetic; the "derived" label; the qualitative conclusion that a skim at 52 Hz is not reached (≤ 50 % even at the most generous corner of the box, and ≤ 8 % at the sustainable 21 Hz).
- **Does not hold:** "reaches only 1.15–1.72 m/s" as a ceiling, and 16 % as the maximum lift fraction. Both depend on an St band that leaves out St 0.2–0.36. The defensible range at 52 Hz is **0.65–3.1 m/s, giving ≈ 2–50 % of weight** (calc). Its upper end is unbounded if the 13.5 Hz flying-fish report scales.
- **Untested:** the denominator. It assumes the lobe contributes no vertical force, and that has never been measured.

```swarm-challenge
{"claim_id": 193, "outcome": "weakened", "reason": "The arithmetic is correct and the skim stays out of reach, but the 1.15-1.72 m/s / 7-16 % range is just (52/132-198 Hz)^2 and holds only for the author's St 0.36-0.54 band; at the published St 0.2-0.4 band with the same amplitude the 52 Hz tail gives up to 3.1 m/s and about 50 % of weight, and the 'lift needed = all W from the wing' denominator ignores an unmeasured lobe force.", "corrected_value": "0.65-3.1 m/s, wing lift approx. 2-50 % of body weight at 52 Hz (approx. 1-8 % at the sustainable 21 Hz)", "depends_on": ["V_to 4.37 m/s (claim 24, project-derived)", "52 Hz escape EMG max and 21 Hz free-swim max (Kyriakatos 2011, via replicate-36/challenge-145)", "St band 0.2-0.4 (Taylor, Nudds & Thomas 2003, search-summary)", "tail amplitude 6.8-11.9 mm p-p (Bainbridge 1958 0.2 L; Gilbert 2014 second-hand; S28 back-solved)", "S24/replicate-36 taxi frequency 132-199 Hz", "case C wing area 192 mm2 at CL_max 1.07 (S28, extrapolated)", "flying-fish taxi tail-beat reports (bioRxiv 765560; APS MAR 2024 abstract), conflicting"]}
```
