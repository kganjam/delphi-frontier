# Challenge 203: adversarial review of S10 (tissue) flapping-power claim

Claim under review (author: harvest `s10-tissue-flapping-power-2kag3x`, file `docs/research/fish/S10-tissue.md` on that branch, read in full by me):

> Sustained flapping is not supported: measured fish aerobic (red/slow) muscle gives 5-10 W/kg, below the computed hover requirement of at least ~34 W/kg flight muscle even in the most generous case; burst flapping is within reach of warm fast muscle (134 W/kg measured in larval zebrafish) only if roughly 10-30% of body mass were pectoral flight muscle.

**Verdict: WEAKENED.** The direction of both conclusions holds up. The sustained "no" survives, but for a reason the claim does not give. The stated measured comparator, "5–10 W/kg", is too narrow. Its ceiling is set by cold or swimming-optimised preparations, and it leaves out at least one measured red-muscle value that is roughly three times higher. The burst fraction "10–30%" depends on applying a power measured at 80 Hz to a wing beating at about 22 Hz.

## 1. Arithmetic, redone independently

I recomputed every number below myself (a Python one-liner), using only the claim's stated inputs: m = 0.4 g, g = 9.81, ρ = 1.2, k = 1.2, full disc A = πR².

| Case | P_ind (computed) | per kg body | required per kg flight muscle |
|---|---|---|---|
| R = 4 cm | 2.686 mW | 6.71 W/kg | M = 1.5, f = 0.3 → **33.6 W/kg** |
| R = 2 cm | 5.371 mW | 13.43 W/kg | M = 2, f = 0.2 → 134 W/kg |

The author's figure of 34 W/kg is arithmetically correct. The minimum flight-muscle fraction at which 134 W/kg suffices is also correct, computed as f_min = M·P_ind/(m·134). It ranges from 0.075 (R = 4 cm, M = 1.5) to 0.20 (R = 2 cm, M = 2). "Roughly 10–30%" is a fair rounding of that range at 134 W/kg. **No arithmetic error found.**

## 2. Relaxing the hidden assumptions on the requirement (my computation)

- **Profile multiplier M = 1.5 is not a floor.** M can fall to 1.0 at the physical limit, where profile power is zero. With M = 1.0, R = 4 cm and f = 0.3, the requirement is 22.4 W/kg.
- **Semispan of 4 cm is not a ceiling.** P_ind ∝ 1/R. With R = 8 cm (a 16 cm span on a 4 cm fish), M = 1.0 and f = 0.3, the requirement is 11.2 W/kg.

So "at least ~34 W/kg" holds only within the author's own grid. It is not a physical lower bound. Under extreme but physically allowed relaxations the requirement falls to about 11 W/kg. That is roughly the top of the claim's own 5–10 W/kg band. The claim's wording ("even in the most generous case") is correctly scoped to "computed", so this is a margin caveat, not a refutation.

## 3. The proxy problem: is "5–10 W/kg" the right measured comparator?

The quantity that matters is the cycle-averaged power of aerobic (red) muscle at about 28 °C (zebrafish body temperature) and at about 22 Hz (the computed wingbeat frequency). The claim's band instead comes from:
- sculpin slow fibres at about 4 °C (5–8 W/kg),
- bass red muscle at about 10 W/kg (temperature not stated in the source),
- skipjack red muscle at 8.8 W/kg (a figure from the paper's abstract).

All three are search-summary readings in the author's own file.

**Counter-example the author missed.** Rome & Swank (1992), *J Exp Biol* 171:261, scup red muscle in optimised work loops. Read-level: search-summary.
- **27.9 W/kg at 20 °C** and 12.8 W/kg at 10 °C, with maximum power at 2.5 Hz and Q₁₀ = 2.29.
- That is a measured red-muscle value about 3× the claim's upper bound of 10 W/kg, and about 83% of the 34 W/kg requirement.
- My extrapolation, **not data**: carrying it to 28 °C with the paper's own Q₁₀ gives about 54 W/kg. That would exceed 34 W/kg at 2.5 Hz.

**Skipjack disagreement, not resolved by me.** The author preserved this disagreement. The headline claim drops it.
- The SICB abstract reports posterior versus anterior fibres at 133 versus 79 W/kg.
- The 2002 paper's abstract, in my search-summary reading, makes the same qualitative point that posterior red muscle produces more mass-specific power. That at least suggests the 79–133 W/kg figures refer to deep red muscle.
- I could not read either source in full, so the conditions remain `unknown`.
- I do not treat 133 W/kg as established. But a headline that says "5–10 W/kg measured" without flagging it understates the spread in the sources.

**Why the sustained "no" still survives (my inference, not a measurement).** Every red-muscle value above peaks at 2.5–5 Hz. A 22 Hz cycle lasts 45 ms. The skipjack SICB abstract gives red-fibre twitch rise times of 60–80 ms (search-summary). A muscle whose twitch takes longer to rise than a whole wingbeat cycle lasts cannot be cyclically activated and relaxed at that rate. Its net power at 22 Hz should be far below its 2.5–5 Hz peak. I found no red-muscle work-loop measurement at 15–30 Hz. The search scope was three web searches: scup red-muscle power, the Syme & Shadwick skipjack abstract, and the hatchetfish pectoral fraction. So the decisive constraint is frequency, not the 5–10 W/kg magnitude that the claim gives as its KEY number.

## 4. Burst case: a frequency-mismatched proxy

The figure of 134 W/kg was measured at **80 Hz**. The design needs about 22 Hz.

- The author's own data give 2.63 J/kg per cycle at 40 Hz, versus 1.68 J/kg per cycle at 80 Hz (computed as 134/80).
- My computation, conditional: if work per cycle at 22 Hz were no higher than at 40 Hz, available power would be 2.63 × 22 ≈ 58 W/kg. The fraction needed would then be **f ≈ 0.17–0.46**, not 0.075–0.20.
- Work per cycle usually rises as frequency falls, so 58 W/kg is plausibly a floor. The true value at 22 Hz is `unknown`, and I did not extrapolate it.

The "roughly 10–30%" therefore holds only if power at 22 Hz is close to the 80 Hz value. The author's §3d acknowledges this; the headline does not.

**Taxon check.** Freshwater hatchetfish (Gasteropelecidae) are the obvious real-world teleost case.
- Pectoral muscle is reported at about 25% of body mass, but only by hobbyist sources with no primary citation. Read-level: search-summary; I treat the figure as unverified.
- Wiest (1995) is reported (secondhand) to have disproven powered flapping flight in hatchetfish. I could not access it.

If both points hold, a teleost with roughly 25% pectoral muscle still does not sustain flapping flight. That is consistent with the claim, not a counter-example to it.

## 5. Evidence level

The "derived" level is honest: a computed requirement compared against published measurements. One wording defect: the KEY presents "5–10 W/kg measured" as though it were the established range for fish red muscle. It is a selection from search-summary readings, it is temperature-mismatched, and it leaves out the scup value of 27.9 W/kg at 20 °C.

## 6. Corrected statement

The computed requirement is ≥ ~34 W/kg in the author's grid, falling to about 11 W/kg under extreme relaxations. Measured red/slow fish muscle peak power is **5–28 W/kg at 2–5 Hz and 4–20 °C**, plus an unreconciled skipjack report of 79–133 W/kg. No measurement near 22 Hz was found. The sustained "no" rests on the frequency limit of slow muscle, not on its magnitude. The burst fraction is 7.5–20% if 80 Hz power transfers to 22 Hz, and up to about 17–46% if work per cycle stays at its 40 Hz value.

### Sources (with read-levels)
- Author's harvest file `docs/research/fish/S10-tissue.md` (branch `claude/s10-tissue-flapping-power-2kag3x`): full-text
- Rome LC, Swank D (1992) *J Exp Biol* 171:261, scup red muscle power versus temperature. https://cob.silverchair.com/jeb/article/171/1/261/6442/ — search-summary
- Syme DA, Shadwick RE (2002) *J Exp Biol* 205:189. https://www.sciencegate.app/document/10.1242/jeb.205.2.189 — search-summary
- SICB abstract, skipjack 133 vs 79 W/kg and twitch rise 60 vs 80 ms. https://sicb.org/?p=37437 — search-summary
- Hatchetfish ~25% pectoral muscle. https://www.practicalfishkeeping.co.uk/features/why-hatchetfish-tick-all-the-right-boxes/ and https://seriouslyfish.com/group/hatchetfishes — search-summary (hobby sources, unverified)
- Wiest (1995): could-not-access

```swarm-challenge
{"claim_id": 203, "outcome": "weakened", "reason": "Arithmetic is correct and the sustained 'no' survives on red muscle's frequency limit (twitch rise 60-80 ms vs a 45 ms wingbeat), but the KEY comparator '5-10 W/kg measured' omits scup red muscle at 27.9 W/kg (20 C; ~54 W/kg extrapolated to 28 C) and the 79-133 W/kg skipjack report, and the burst 10-30% fraction applies an 80 Hz power to a 22 Hz wing.",
  "corrected_value": "measured red/slow muscle peak 5-28 W/kg (2-5 Hz, 4-20 C; plus unreconciled 79-133 W/kg skipjack) vs computed >=34 W/kg (author grid; ~11 W/kg under extreme relaxation); burst flight-muscle fraction 7.5-20% at 80 Hz-equivalent power, up to ~17-46% if 22 Hz work/cycle equals the 40 Hz value",
  "depends_on": ["Rome & Swank 1992 scup red muscle 27.9 W/kg at 20 C, Q10 2.29 (search-summary)", "SICB skipjack abstract: red fibre twitch rise 60-80 ms and 79-133 W/kg (search-summary)", "Mead et al. 2020 larval zebrafish 134 W/kg at 80 Hz and 2.63 J/kg at 40 Hz (as reported by author)", "author's momentum-theory inputs: m=0.4 g, k=1.2, R=2-4 cm, M=1.5-2, f=0.1-0.3", "computed wingbeat ~22 Hz from author's S10 section 3c"]}
```
