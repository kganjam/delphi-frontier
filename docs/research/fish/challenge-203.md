# Challenge 203: S10 tissue claim (sustained vs burst flapping power)

**Claim under review** (from `harvest:s10-tissue-flapping-power-2kag3x`, file `docs/research/fish/S10-tissue.md` on branch `claude/s10-tissue-flapping-power-2kag3x`, read in full):

> Sustained flapping is not supported: measured fish aerobic (red/slow) muscle gives 5-10 W/kg, below the computed hover requirement of at least ~34 W/kg flight muscle even in the most generous case; burst flapping is within reach of warm fast muscle (134 W/kg measured in larval zebrafish) only if roughly 10-30% of body mass were pectoral flight muscle.

Recorded evidence level: derived. **Verdict: WEAKENED.** The hover arithmetic holds. The claim goes wrong in three places. "At least ~34 W/kg" is not a floor. "Sustained flapping" is wider than the hover case the computation actually covers. And the 10% lower bound for burst flight uses power measured at 80 Hz, while the wing is designed for ~22 Hz.

No new literature was consulted for this challenge: no web searches and no fetches. Every measured value below is the author's, at the author's read-levels (mostly *search-summary*, and Mead et al. 2020 *full-text, partial*). Everything I add is **my own calculation**, and I label it that way where it appears.

---

## 1. Independent arithmetic (my calculation)

Inputs as the author stated them: m = 0.4 g, g = 9.81 m/s², ρ = 1.2 kg/m³, A = πR², P_ind = k·√(W³/2ρA).

| Case | P_ind (mW) | W/kg body |
|---|---|---|
| R = 4 cm, k = 1.2 | 2.686 | 6.71 |
| R = 2 cm, k = 1.2 | 5.371 | 13.43 |

The author's most generous case is R = 4 cm, k = 1.2, M = 1.5, f = 0.3. It gives 6.71 × 1.5 / 0.3 = **33.6 W/kg flight muscle**, which **reproduces** the author's ~34. I also re-derived the rest of the author's table (101/50/34, 134/67/45, 201/101/67, 269/134/90) and it is consistent.

## 2. "At least ~34 W/kg" is the generous end of the author's grid, not a floor (my calculation)

The value 34 depends on k = 1.2 and M = 1.5. If those are set to the ideal-rotor floor (k = 1.0, profile power ignored, M = 1.0), with R = 4 cm and f = 0.3, the result is **18.6 W/kg flight muscle**. At f = 0.5 it is 11.2 W/kg. Both are still above the 5-10 W/kg red-muscle band, so **the conclusion for sustained hover survives this relaxation.** The words "at least ~34" overstate the bound, though. The true momentum-theory floor at f = 0.3 is about 19 W/kg, and the margin over red muscle drops from 3-7× to about 2-4×.

## 3. Hidden assumption that carries the headline: hover (my calculation)

The headline says *sustained flapping*. The computation is for *hover* only. The author says this in their §3d and §5 but not in the claim sentence. Forward flight at the minimum-power speed is the gait a sustained flier would actually use. I estimated it with the author's own generous wing (span 8 cm, AR 6, S = 1.07 × 10⁻³ m²) using a quasi-steady model:

P = 1.2·W²/(2ρ·S_d·V) + ½ρ·C_D,pro·S·V³ + ½ρ·C_D,body·A_f·V³, with S_d = πb²/4 and A_f = 3.5 × 10⁻⁵ m².

A_f, C_D,pro (0.05-0.2) and C_D,body (0.4-1.0) are **my assumptions**. None of them is measured.

| C_D,pro | V_mp (m/s) | W/kg body | W/kg muscle, f = 0.3 | f = 0.2 |
|---|---|---|---|---|
| 0.05 | 1.8-1.9 | 2.7-2.9 | **9.0-9.7** | 13.5-14.5 |
| 0.1 | 1.6 | 3.1-3.3 | 10.4-10.9 | 15.7-16.3 |
| 0.2 | 1.4 | 3.7-3.8 | 12.2-12.5 | 18.4-18.8 |

This model leaves out the profile drag caused by the flapping velocity itself, so it is optimistic. As a cross-check, I charged hover-level profile power (0.5 × hover P_ind ≈ 1.3 mW) on top of forward-flight induced and parasite power. That gives about 4.5 W/kg body, which is **~15 W/kg flight muscle at f = 0.3 and ~22 at f = 0.2**. This is still my calculation.

**Inference (mine):** in forward flight, the required power per kg of flight muscle is about 9-22 W/kg. That band overlaps the measured 5-10 W/kg band at its generous end, or sits up to ~2-4× above it. The 3-7× hover gap does not carry over to forward flight. So the claim "sustained flapping is not supported" is shown only for **sustained hover**. For sustained forward flight the margin is marginal, and it depends on assumptions (f, C_D,pro, the Re ≈ 2,000-3,000 regime) that nobody has measured.

Two things argue against my own weakening:
- **Frequency mismatch.** The red/slow values were measured at their 2-5 Hz optimum. Slow fibres lose power above their optimum frequency, and the design wingbeat is ~22 Hz. Red muscle power at 22 Hz is therefore probably *below* 5-10 W/kg. That is an inference from general fibre-type physiology, and I retrieved no value at 20 Hz (`unknown`). It would push the sustained verdict back toward "no".
- **Anatomy.** f = 0.3 *red* pectoral muscle would be far outside teleost anatomy. No zebrafish value was retrieved (`unknown`).

## 4. Proxy problems

1. **Temperature for the sustained band.** The sculpin slow value (5-8 W/kg) was measured at ~4 °C, and the zebrafish case is at 28 °C. The author applied a Q₁₀ extrapolation to the cold *fast* values but not to the cold *slow* values. With the same speculative Q₁₀ = 2 (×5.3), sculpin slow muscle would come out at ~26-42 W/kg. That is speculation, not data. The warm red-muscle values that hold the band at ~10 W/kg are bass (~10) and skipjack (8.8). Both are *search-summary* only, and their test temperatures were not reported to me (`unknown`). So the 5-10 W/kg "sustained" band combines one cold measurement with two warm search-summary values.
2. **Frequency for the burst case.** The 134 W/kg value was measured at 80 Hz, against a design frequency of ~22 Hz. The author's own derived value at 40 Hz is 2.63 J/kg × 40 = 105 W/kg (I recomputed it and it reproduces). Mead et al. place peak power near 80 Hz, so power at 22 Hz is probably **≤ ~105 W/kg**, but it is `unknown`. Only one f = 0.1 case (101 W/kg) fits under 105, and only just. The lower end of "roughly 10-30%" depends on the off-design 80 Hz value. "Roughly 20-30%" is what the design-frequency evidence supports. That is my inference.
3. **The unresolved skipjack conflict** (8.8 vs 79-133 W/kg from the same authors) is preserved by the author and stays unresolved here. I made no attempt to fetch either source.

## 5. Evidence level

"Derived" is honest. The claim names the 34 W/kg as computed and the 5-10 and 134 W/kg as measured. One defect: the measured values reached the author mostly as *search-summary* reads. The claim sentence does not carry that read-level, but the source file does.

## 6. Regimes and counter-examples not covered

- Sustained forward flight at the minimum-power speed (§3 above). Not computed by the author. My estimate weakens the headline.
- Intermittent flap-glide, and ground effect over the water surface: neither the author nor I modelled them. Both lower the requirement.
- Negative-search scope for this challenge: I searched only the source file and the repository branches for related work. I ran no literature searches, so I cannot say whether a published fish flier power measurement exists.

## Corrected statement (my wording)

For hover: sustained flapping is not supported. The computed requirement is ≥ ~19 W/kg flight muscle (ideal floor, f = 0.3) and ~34 W/kg (author's generous case), against 5-10 W/kg measured red/slow muscle. For forward flight at the minimum-power speed, the computed requirement of ~9-22 W/kg flight muscle (f = 0.2-0.3, my quasi-steady estimate) overlaps or sits near the measured red-muscle band, so the sustained "no" there is unproven. The likely loss of red-muscle power at ~22 Hz (unmeasured) is the factor most likely to restore it. Burst flapping needs roughly 20-30% (not 10%) of body mass as fast muscle once power is taken at ≤ ~105 W/kg near the design frequency, rather than 134 W/kg at 80 Hz.

```swarm-challenge
{"claim_id": 203, "outcome": "weakened", "reason": "The 34 W/kg hover arithmetic reproduces (33.6), but it is not a floor (k=1, M=1 gives ~19 W/kg at f=0.3), the sustained 'no' is shown only for hover (my quasi-steady minimum-power forward-flight estimate gives ~9-22 W/kg flight muscle, overlapping the 5-10 W/kg red-muscle band), and the 10% burst lower bound relies on 134 W/kg measured at 80 Hz rather than the ~22 Hz design frequency.",
  "corrected_value": "hover >=~19-34 W/kg flight muscle (f=0.3; ideal floor to author's generous case); forward flight at V_mp ~9-22 W/kg flight muscle (f=0.2-0.3, computed); burst needs ~20-30% body mass fast muscle",
  "depends_on": ["m=0.4 g, rho=1.2 kg/m3, R=4 cm semispan (author's design assumption)", "flight-muscle fraction f=0.2-0.3 (assumption; zebrafish value unknown)", "red/slow muscle 5-10 W/kg (Altringham & Johnston sculpin slow, bass ~10, Syme & Shadwick skipjack 8.8; search-summary)", "Mead et al. 2020 larval zebrafish 134 W/kg at 80 Hz and 2.63 J/kg at 40 Hz (full-text, partial)", "design wingbeat ~22 Hz (author's computation)", "my forward-flight assumptions: C_D,pro 0.05-0.2, C_D,body 0.4-1.0, frontal area 3.5e-5 m2"]}
```
