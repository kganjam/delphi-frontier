# Challenge 168: adversarial review of claim S1-D (zebrafish escape speed vs. airborne lift)

**Claim under review (author's text, not mine):** "No: replacing Plaut's sustained U_crit (0.56 m/s)
with a measured adult escape burst speed (0.95 m/s robust lower bound, 1.57 m/s reported peak) still
leaves a 0.4 g zebrafish ~3.6x short of the ~5.7 m/s airspeed its body could need to support its weight
in air (calculated), although the same speed would, drag-free, suffice to throw it clear of the water
(calculated, not observed)." The recorded evidence level is `measured`, with no value given.
Source: harvest:zebrafish-takeoff-deepen-2gwq0o.

**Verdict: WEAKENED.** The "No" survives every relaxation I tried, and most of them make it stronger.
Three things are wrong. The headline ratio is the most favourable one the author's inputs allow. The
claim is recorded as `measured` although its conclusion is calculated. The lift assumption behind the
5.7 m/s figure is never stated.

## 1. Arithmetic, redone independently (all calculated, nothing observed)

Inputs: m = 0.4 g = 4.0e-4 kg, g = 9.81 m/s², ρ_air = 1.2 kg/m³.

- Weight W = 3.92e-3 N.
- Lift L = ½ρV²·S·C_L. Setting L = W at V = 5.7 m/s requires **S·C_L ≈ 2.0 cm²**. The claim does not
  state this. It holds, for example, with a planform of about 2 cm² (roughly a 3.5 cm × 0.6 cm side
  profile) and C_L ≈ 1. My reconstruction matches the author's 5.7 m/s (I get 5.72 m/s).
- Speed ratios against 5.7 m/s:

| Speed used | Source as stated in the claim | Speed shortfall | Lift-force shortfall (∝V²) | Ballistic rise v²/2g |
|---|---|---|---|---|
| 0.56 m/s | Plaut's U_crit, sustained | 10.2x | 104x | 1.6 cm |
| 0.95 m/s | escape mean over 40 ms, "robust lower bound" | **6.0x** | 36x | 4.6 cm |
| 1.57 m/s | escape, "reported peak" | **3.6x** | 13x | 12.6 cm |

**Fault 1, the headline ratio.** "~3.6x short" is correct only for the 1.57 m/s peak. Against the
0.95 m/s figure, which the claim itself calls the *robust* bound, the shortfall is **6.0x**. Quoting the
best case is conservative for a "No" verdict, so this does not overturn the claim. It does misstate its
precision. The honest headline is "3.6x to 6.0x in speed, or 13x to 36x in lift force".

## 2. Proxy check

- *Speed as a proxy for weight support.* What matters is lift force, and lift goes as V². A 3.6x speed
  gap is a 13x force gap. Expressing the gap in speed understates the deficit; it does not create a
  false one.
- *Escape speed as a proxy for exit speed.* The 0.95 and 1.57 m/s figures are fast-start (C-start)
  speeds. These are normally measured as roughly horizontal, mid-water bursts, and peak speed is
  reached for only milliseconds. Throwing the fish clear needs speed **normal to the surface, at the
  surface**. That quantity is not measured anywhere I found (`unknown`). This weakens only the
  secondary "would suffice to throw it clear" clause, not the "No".

## 3. Hidden assumptions, relaxed

- **S·C_L.** A fish trunk is a poor lifting body, so C_L ≈ 1 is generous. With S·C_L = 1 cm², the speed
  needed is 8.1 m/s. Making the assumption *more favourable to the fish*, with fins fully spread
  (S = 3 cm², C_L = 1.2), still requires 4.3 m/s: 2.7x above the 1.57 m/s peak and 4.5x above 0.95 m/s.
  **Across every value I tried, the "No" holds.**
- **Drag-free ballistic exit.** For the throw-clear clause, 0.95 m/s gives a 4.6 cm drag-free rise,
  which is more than one adult body length (about 3 to 4 cm, my assumption). The following are not
  modelled: underwater drag during the run-up, added mass at the surface, the launch angle (anything
  other than vertical cuts the vertical rise by sin²θ), and meniscus or surface-tension forces at exit.
  My rough upper bound for the surface-tension force is 2π·(3 mm)·0.072 N/m ≈ 1.4 mN, about a third
  of body weight (calculated, order-of-magnitude only). A margin of 2.9x (height) over the 1.6 cm rise
  needed, or 3.9x at the low end, probably absorbs these, but the clause is less certain than
  "would suffice" implies.

## 4. Evidence level, the main defect

The record labels the claim `measured`. Only the inputs (0.56, 0.95 and 1.57 m/s) are presented as
measured, and **I could not verify them**. The search
"adult zebrafish escape response peak velocity m/s C-start" (standard web search, one query) returned
no source giving 0.95 m/s or 1.57 ± 0.27 m/s for adults. Their read-level is therefore
`could-not-access`. The claim's conclusion, the 5.7 m/s requirement and the 3.6x gap, is
**calculated**, and the claim's own sentence says so. Recording a calculated conclusion under the
evidence level `measured` breaks the honesty floor even though the numbers are right. **Corrected
level: calculated, from measured inputs (inputs unverified in this review).**

## 5. Counter-examples and missed regimes

- **Zebrafish do leave the water.** A search for zebrafish jumping out of aquaria returned the ZFIN
  Zebrafish Health and Welfare Glossary (read-level: **search-summary**). Fetching the page failed
  because the host is outside this session's network allowlist. According to the search summary, the
  glossary lists "jumping out of the water of an undisturbed tank" as a welfare indicator. If that
  holds, the claim's "(calculated, not observed)" is accurate only for the author's *calculation*.
  Leaving the water appears to be a recognised husbandry observation, although I found no source that
  ties it to a measured exit speed. This *supports* the throw-clear clause and does not touch the "No".
- **Small fish that are airborne.** Freshwater hatchetfishes (Gasteropelecidae) are of broadly similar
  size and are reported to travel over the surface. This is my recollection and was not checked in
  this review. As far as I know, their aerial travel is generally described as jumping or surface
  taxiing rather than sustained weight-supporting flight, so they would not falsify the claim that a
  zebrafish body would need about 5.7 m/s to *support its weight in air*. Scope: no search was run on
  hatchetfishes, so treat this as unverified.
- **Flying fishes (Exocoetidae)** need greatly enlarged pectoral fins and take-off speeds far above
  1.57 m/s (general knowledge, not checked here). They show what the zebrafish lacks and do not
  contradict the claim.

## Bottom line

Every relaxation I tried leaves the "No" standing: the speed shortfall is 3.6x to 6.0x, and the lift
shortfall 13x to 36x (calculated). The claim is weakened on three points:

1. Its "~3.6x" is the best case rather than the robust figure.
2. The S·C_L ≈ 2 cm² assumption behind 5.7 m/s is unstated.
3. A calculated conclusion is recorded as `measured`, and the measured inputs could not be traced to a
   source in this review.

```swarm-challenge
{"claim_id": 168, "outcome": "weakened", "reason": "The 'No' holds under every relaxation tried (shortfall 3.6x-6.0x in speed, 13x-36x in lift), but the headline 3.6x uses the peak rather than the stated robust 0.95 m/s bound, the 5.7 m/s rests on an unstated S*C_L of about 2 cm^2, and a calculated conclusion is recorded as 'measured'.",
  "corrected_value": "speed shortfall 3.6x (vs 1.57 m/s peak) to 6.0x (vs 0.95 m/s robust bound); lift-force shortfall 13x-36x; evidence level: calculated",
  "depends_on": ["body mass 0.4 g", "air density 1.2 kg/m^3", "S*C_L about 2 cm^2 (reconstructed from the author's 5.7 m/s; range 1-3.6 cm^2 tested)", "adult escape speed 0.95 m/s (author's input, source not verified)", "adult escape speed 1.57 +/- 0.27 m/s (author's input, source not verified)", "adult body length about 3-4 cm (my assumption)", "ZFIN welfare glossary lists jumping out of the tank (search-summary only)"]}
```
