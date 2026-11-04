# Replication of claim 37: zebrafish surface-taxi ceiling at sustainable tail-beat frequency

**Claim under test (answer withheld from me):** "At sustainable tail-beat frequencies the calculated
taxi ceiling is ~[X] m/s, which is Ucrit itself -- so taxiing adds essentially nothing to the launch."
The inputs live in `S24-behaviour.md` (branch `claude/s24-surface-taxiing-launch-tsepbn`).

**My value (calculated, not observed): 0.50–0.59 m/s for a 36–40 mm adult. Central value
≈ 0.55 m/s, uncertainty about ±0.05 m/s. The spread comes from the model choice (Strouhal vs
Bainbridge) and the length basis.** For the fish size that the frequency measurement actually came
from (18–30 mm), the same models give **0.34–0.44 m/s**. Across the plausible amplitude and
Strouhal range the full model band is about 0.3–1.4 m/s (§3).

## 0. Independence statement

I derived the speed relations and Ucrit from the literature before opening `S24-behaviour.md`.
Only then did I read it, for comparison. **One input was not independent: the 21 Hz frequency.**
Before reading S24 I had assumed "~20 Hz" without a zebrafish source. I took the specific 21 Hz
figure, and its citation (Kyriakatos et al. 2011), from S24. I then **re-read that primary
source myself** (§1). In doing so I found a size mismatch that S24 does not discuss. So the
frequency input is shared with the original author. The two derivations are independent in
model choice, length basis and arithmetic, but not in the frequency source.

## 1. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Ucrit, adult wild type | 0.5486 m/s = 18.0 SL/s (n = 10) | Palstra et al. 2010, *PLoS ONE* 5:e14483. Found via Leiden repository search result | search-summary |
| Ucrit, adult wild type, 28 °C | 0.560 m/s = 15.5 SL/s | Plaut 2000, *J. Exp. Biol.* 203:813, as cited by Palstra | search-summary (secondary) |
| Implied SL for Plaut's fish | 0.560 / 15.5 = 3.6 cm | calc from the line above | — |
| Max voluntary swimming frequency, intact adults | "ranged … from ∼1 Hz to slightly >20 Hz, but never exceeding 21 Hz (n = 8)"; peak of the distribution ~8–10 Hz | Kyriakatos, Mahmood, Ausborn, Porres, Büschges & El Manira 2011, *J. Neurosci.* 31:8422 (PMC6623330) | full-text (first 100,000 of 101,006 characters) |
| **Method and size behind that frequency** | **EMG** (wire electrodes in the muscle), not kinematics. Animals 8–15 weeks old, **body length 18–30 mm**. Temperature for the intact recordings not stated | Kyriakatos et al. 2011, Methods | full-text (same) |
| Max frequency during escape | 52 Hz | Kyriakatos et al. 2011 | full-text (same) |
| Speed–frequency relation | V = ¼·L·(3f − 4), V in cm/s, L in cm, f in Hz. Fitted for dace, trout and goldfish up to 30 cm, for f > 5 Hz | Bainbridge 1958, *J. Exp. Biol.* 35:109 (abstract as quoted in search results) | search-summary |
| Strouhal cruising band | St = fA/U ≈ 0.2–0.4 | Taylor, Nudds & Thomas 2003, *Nature* 425:707 | from memory, corroborated only by S24's citation. Treat as **search-summary at best** |
| Tail amplitude | A (peak-to-peak) = 0.2 L | **assumption** (conventional value for carangiform/subcarangiform fish). I found no measured adult zebrafish amplitude | — |
| Adult zebrafish tail-beat kinematics vs speed in a flume | **unknown** | Searched web (standard + extended) for adult tail-beat frequency/amplitude vs speed. Returned only larval kinematics and general reviews | search-summary (negative, scope = two web searches) |

**Disagreement noted, not resolved here:** S24 also records Wakamatsu et al. 2019 Ucrit values of
0.19–0.28 m/s. I did not re-read that paper. I use only the Palstra/Plaut value, because the
claim compares against that value.

## 2. Arithmetic

"Taxi ceiling" here means the forward speed the tail can drive at a given tail-beat frequency
under a kinematic constraint. This is a frequency-limited ceiling, not a force balance. I take
f = 21 Hz as the "sustainable" frequency.

**(a) Strouhal model.** U = f·A/St, with A = 0.2 L and St = 0.3:

| L | A | U = 21 × A / 0.3 |
|---|---|---|
| 0.024 m (midpoint of Kyriakatos' 18–30 mm) | 4.8 mm | **0.336 m/s** |
| 0.030 m (top of Kyriakatos' range) | 6.0 mm | **0.420 m/s** |
| 0.036 m (Plaut SL) | 7.2 mm | **0.504 m/s** |
| 0.040 m (project TL premise) | 8.0 mm | **0.560 m/s** |

**(b) Bainbridge 1958.** V = ¼·L·(3·21 − 4) = 14.75·L (cm/s, L in cm):

| L | V |
|---|---|
| 2.4 cm | 35.4 cm/s = **0.354 m/s** |
| 3.0 cm | 44.3 cm/s = **0.443 m/s** |
| 3.6 cm | 53.1 cm/s = **0.531 m/s** |
| 4.0 cm | 59.0 cm/s = **0.590 m/s** |

**(c) Sensitivity at L = 0.04 m, f = 21 Hz (Strouhal):** A 0.15 L & St 0.4 → 0.32 m/s; A 0.25 L
& St 0.15 → 1.40 m/s. **(d) At 52 Hz** (escape, transient), central Strouhal at L = 0.04 m →
1.39 m/s. That frequency is not sustainable, so it falls outside the claim.

**Compare with Ucrit (0.549–0.560 m/s):** for a 36–40 mm fish, the 21 Hz ceiling is 0.50–0.59
m/s, which is **0.91–1.08 × Ucrit**. Calculated, not observed.

## 3. My inferences (not author claims)

1. **The kinematic ceiling cannot tell taxiing from swimming.** U = fA/St and Bainbridge's
   relation have no term for whether the body is submerged or riding the surface. At a given
   frequency they return the free-swimming speed. So "taxi ceiling ≈ Ucrit at sustainable f"
   is close to built in. It shows the tail cannot beat faster during a taxi than in a Ucrit
   test, not that the surface condition limits the speed. The conclusion still follows: without
   a higher frequency there is no speed gain.
2. **The surface makes things worse, not better, for a hull-like body** (calc). At 0.56 m/s the
   length Froude number is U/√(gL) = 0.89 (L = 0.04 m). That is far above the displacement
   "hull speed" (Fr ≈ 0.4 → 0.25 m/s), where wave drag dominates. A fish that is not planing
   would hit a wall well below Ucrit at the surface. This strengthens "adds nothing". It is my
   inference, and I did not quantify the wave drag.
3. **Partial circularity in the central 0.56 value.** Choosing A = 0.2 TL with TL = 40 mm and
   St 0.3 gives fA = 0.168 m/s at 21 Hz. Back-solving from Ucrit at the same St gives fA = 0.164
   m/s. So the central estimate lands on Ucrit partly because the amplitude matches what Ucrit
   implies. The Bainbridge relation was fitted on other species and is independent of zebrafish
   Ucrit. It gives 0.53–0.59 m/s for 36–40 mm and confirms the number without that circularity.
4. **Size mismatch.** The 21 Hz ceiling was measured in 18–30 mm fish. Combining it with
   L = 40 mm mixes sizes. Smaller fish beat faster, so a 40 mm fish's ceiling frequency is
   probably ≤ 21 Hz, and a consistent-size estimate is **0.34–0.44 m/s**. That lower value is
   *below* Ucrit, which supports the qualitative claim more strongly.
5. **"Sustainable" is overstated.** 21 Hz is the maximum voluntary EMG frequency observed in a
   small tank (n = 8), not a measured sustained or Ucrit tail-beat frequency. No adult zebrafish
   tail-beat frequency at Ucrit was found (scope: two web searches plus this paper).

## 4. Comparison with the recorded value

I read `S24-behaviour.md` §3.2 and `S24_calcs.py` only after §0–§2 were written. **Recorded
value: 0.56 m/s.** S24 computes it as U = fA/St = 21 Hz × (0.2 × 0.040 m) / 0.3, and calls it
"Ucrit itself (0.56 vs 0.548 m/s)". S24 does state that its Strouhal band and amplitude are
assumptions and that the 52 Hz value is EMG.

**Verdict: AGREE.** For the same 40 mm premise I get the same number by the same model (0.560
m/s), and an independent empirical relation (Bainbridge) gives 0.59 m/s. The qualitative claim,
that the taxi ceiling at sustainable frequency is ≈ Ucrit and so taxiing adds essentially
nothing, holds. The size-consistent correction (inference 4) and surface wave drag (inference 2)
both push it lower, not higher.

**Two caveats S24 does not state.** First, the 21 Hz input comes from 18–30 mm fish, not 40 mm.
Second, the agreement with Ucrit is partly by construction, because the amplitude is
Ucrit-consistent and the kinematic model has no surface term. The frequency input is shared
between the two derivations, so this agreement is weaker evidence than two fully independent
derivations would be.

```swarm-replication
{"claim_id": 37, "my_value": "0.50-0.59 m/s for a 36-40 mm fish at 21 Hz (calc; 0.34-0.44 m/s if length matched to the 18-30 mm fish the 21 Hz was measured in)", "agrees": true,
  "note": "Strouhal and Bainbridge both put the 21 Hz tail-beat ceiling at ~0.5-0.6 m/s, about Ucrit, matching the recorded 0.56 m/s; the 21 Hz input is shared, comes from smaller 18-30 mm EMG-recorded fish, and the kinematic model cannot tell taxiing from swimming, so the agreement is partly built in, and size-matched values fall below Ucrit."}
```
