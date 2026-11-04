# Challenge 193: tail-driven skim at 52 Hz

**Claim under review** (S28-organism.md §3.5 and §3.6, branch `claude/s28-organism-design-5z0vjz`):
"A tail-driven skim at the measured 52 Hz maximum reaches only 1.15-1.72 m/s, giving 7-16% of the lift needed."
Recorded evidence level: **derived**. Recorded value: 16 percent of lift.

**Verdict: SURVIVED.** The arithmetic is right. The hidden assumptions all push toward *more* lift, not less, so the
number is an upper bound. An independent speed estimate (Bainbridge's stride relation) lands inside or below the range.
Below I list three defects. None of them changes the conclusion: the source's 6.9–15.5 % rounds up to "16 %", the
amplitude is circular, and the 52 Hz input has no citation.

Every number in this file is **calculated by me**. None of it is an observation.

---

## 1. Independent arithmetic

Inputs, as stated in the source: f = 52 Hz, peak-to-peak tail amplitude A = 11.9 mm, Strouhal number St = 0.36–0.54,
takeoff speed V_to = 4.37 m/s (case C, AR 5, CL_max 1.07). Lift as a fraction of weight is (U/V_to)².

| St | U = f·A/St | lift/W (case C, V_to 4.37) | case B (5.47) | case A (8.10) | implied stride U/(f·L), L = 3 cm |
|---|---|---|---|---|---|
| 0.54 | 1.146 m/s | **6.88 %** | 4.39 % | 2.00 % | 0.73 L |
| 0.36 | 1.719 m/s | **15.47 %** | 9.87 % | 4.50 % | 1.10 L |

- Speeds: 1.15 and 1.72 m/s. **Confirmed.**
- Lift: 6.9 % and 15.5 %. The source body says 15.5 %. The headline "7–16 %" and the recorded "16 percent" round
  15.47 up. The correct rounding is **15 %**. This is a 0.5-point presentational issue and does not affect the verdict.
- The source's script line `U=52*A/St; (U/Vto)**2` reproduces the same numbers.

## 2. Proxy check

**(a) The amplitude cancels, so this is not an independent result.** The source back-solved A = 11.9 mm from "132–199 Hz
needed at St 0.36–0.54 for 4.37 m/s". It then reuses the same A and the same St values. Algebraically, the lift fraction
is therefore just (52/f_needed)²:
(52/132.2)² = 0.155 and (52/198.3)² = 0.069.
The 7–16 % is the project's "2.5–3.8× frequency shortfall" squared. It inherits that result's validity and adds no
evidence of its own. The source does say so ("the tail-frequency shortfall … is the project's taxiing result"), but
the reader should not count the two as two confirmations.

**(b) The right physical quantity is stride length (distance per tail beat), not a Strouhal number paired with a
back-solved amplitude.**
- The source's A = 0.4 SL peak-to-peak is about twice the ~0.2 L maximum amplitude that Bainbridge (1958) reports.
- With Bainbridge's empirical relation U = L(3f − 4)/4 (cm/s, L in cm, f in Hz):
  - L = 3.0 cm (SL): U = 1.14 m/s → **6.8 %** of weight (case C).
  - L = 3.6 cm (my rough total length; *assumed*, not sourced): U = 1.37 m/s → **9.8 %**.
- **Caveat on this check:** Bainbridge fitted dace, trout and goldfish at lower frequencies. Applying the relation at
  52 Hz to a 3 cm fish is an extrapolation by me.

The source's upper end implies a stride of 1.10 L, which is long. I infer that the 16 % upper end is generous, and that a
more physical estimate sits at roughly 7–10 %. This *strengthens* the claim's direction.

## 3. Hidden assumptions, tested relaxed

| Assumption | Relaxed | Result | Breaks claim? |
|---|---|---|---|
| St ≥ 0.36 | St 0.25 / 0.20 (lower efficient cruising values) | 32 % / 50 % of W, case C | No. These need strides of 1.6 / 2.0 L at 52 Hz, which I consider physically implausible. Even then lift is < 100 %. |
| Case C fin area (the most generous case) | case B / case A | 4.4–9.9 % / 2.0–4.5 % | No. The claim already uses the upper bound. |
| No ground effect near the water surface | Hypothetical ×2 on lift. This is my illustrative number, not a sourced one. | ≤ 31 % | No. The wing would need a ×6.5 gain over 15.5 % to carry the weight. |
| Whole tail thrusting | Only the lower lobe submerged (real skim posture) | U lower | No. The source already notes this makes it worse. |
| 52 Hz is the ceiling | — | — | **Untested.** In the source this input is labelled "measured / project input" with no citation. I did **not** search for adult zebrafish maximum tail-beat frequency in this review. The lift fraction scales as f², so the verdict is only as good as this number. |
| V_to = 4.37 m/s at m = 0.25 g (an assumed mass) | 0.40 g, so V_to ×1.26 | lift ÷1.6 | No. It gets worse. |

Every relaxation I could justify physically either lowers the lift fraction or leaves it well short of 100 %.

## 4. Evidence level

The claim is recorded as **derived**, and the source labels it as a calculation ("Status: derived … Nothing in this
document is a new measurement"). That is **honest**.

One upstream labelling issue: the source's input table marks "52 Hz" as **measured** but cites only "project input". I
could not trace that number to a primary measurement inside the source document. That is a provenance gap in the input,
not a mislabelled output.

## 5. Counter-regimes and taxa

- **Freshwater hatchetfishes (Gasteropelecidae)** are small fish that leave the water and travel over the surface. Some
  sources describe this as "hydroplaning" or skimming. A search summary attributes to Wiest (1995) high-speed video
  showing that the pectoral fins work during take-off but not while airborne.
  - **Read-level: search-summary. I did not access Wiest 1995 itself.**
  - This is not a counter-example to the claim. The propulsion is pectoral, and the source's design explicitly excludes
    pectoral-muscle enlargement. The mode is also hydroplaning, not an airborne wing.
  - **It does mark a scope limit (my inference).** The claim proves that an *airborne-wing* skim is unreachable. It does
    not address a *hydroplaning* mode, in which body-water contact supplies lift. At U ≈ 1.7 m/s, the length Froude
    number is U/√(gL) = 1.72/√(9.81·0.03) ≈ 3.2 (my calculation). Small planing bodies operate in that range.
  - The source defines skim as "body airborne", so the 7–16 % claim stands as stated. The broader §3.6 line "Not a skim"
    should be read with that definition attached.
- I did not search for flying-fish (Exocoetidae) taxiing tail-beat data in this review. The claim concerns a 3 cm
  zebrafish, and I would not transfer those numbers without size scaling.

## 6. Sources

| Source | Read-level | Used for |
|---|---|---|
| S28-organism.md and S28_organism.py (branch `claude/s28-organism-design-5z0vjz`) | full-text | inputs, claim |
| Bainbridge R. 1958, J. Exp. Biol., "The speed of swimming of fish as related to size and to the frequency and amplitude of the tail beat". Page numbers disagree between listings (35:109–133 vs 129–153). | search-summary | U = L(3f−4)/4; max amplitude ≈ L/5 |
| Wiest 1995 (hatchetfish take-off), full citation not retrieved | search-summary (secondary source only) | counter-regime |

## 7. Bottom line

The 1.15–1.72 m/s and 6.9–15.5 % figures are correct arithmetic on the stated inputs. They are the generous end of
the plausible range: an independent stride estimate gives about 7–10 %. The claim survives, with these riders:

1. "16 %" is 15.5 %, rounded up.
2. The result is the project's frequency-shortfall result squared, not independent corroboration.
3. It rests entirely on the uncited 52 Hz input and the 4.37 m/s V_to.
4. It covers airborne skimming only, not hydroplaning.

```swarm-challenge
{"claim_id": 193, "outcome": "survived", "reason": "Independent arithmetic reproduces 1.15-1.72 m/s and 6.9-15.5% of weight, every justifiable relaxation (fin case, mass, lobe-only thrust, Bainbridge stride ~0.73 L giving 6.8-9.8%) lowers or keeps the lift far below 100%, and the 'derived' label is honest; only the '16%' is a round-up of 15.5%.", "corrected_value": "6.9-15.5 % of body weight (rounding only; physical stride estimate ~7-10 %)", "depends_on": ["max tail-beat frequency 52 Hz (source: 'project input', uncited)", "V_to 4.37 m/s (case C, AR 5, CL_max 1.07, mass 0.25 g assumed)", "tail amplitude 11.9 mm back-solved from the project's 132-199 Hz at St 0.36-0.54", "Bainbridge 1958 U = L(3f-4)/4 and amplitude ~L/5 (search-summary)", "skim defined as body-airborne, wing carries weight (S28 §3.5)"]}
```
