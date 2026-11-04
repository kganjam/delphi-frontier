# Challenge 52: the "low-Re Strouhal" correction to S24

**Claim under review (not written by me):** "S24 applied the Strouhal CRUISING band 0.2-0.3, but
the law library records that small, low-Reynolds swimmers sit ABOVE it (goldfish 0.54 at Re
7.1e3, tadpole 0.79, lungfish 1.02). A 4 cm zebrafish is that case, so the required tail-beat
frequency is 132-199 Hz, not 49-73 Hz, and the shortfall against the 52 Hz measured maximum is
2.5-3.8x rather than 1.4x."
Recorded as `derived`, value 2.5 (ratio). Source: `library/laws/strouhal.yaml` `where_it_breaks`
(Eloy 2012 values), recomputed. The claim first appears in commit `aebc0736`.

**Verdict: WEAKENED.** The arithmetic is mostly reproducible. But the reason given for it fails
at the operating point. A zebrafish taxiing at 1.95 m/s is at Re ≈ 7.8 × 10⁴, not 7 × 10³. Most
of the cited taxa are also the wrong body plan. The upper bound of 199 Hz cannot be reproduced
from any value the claim cites. And the claim raises St while keeping an amplitude that S24
calibrated *assuming* St 0.3.

The claim's *direction* is not refuted, though. Adult zebrafish do show high Strouhal numbers at
slow speed (Mwaffo et al. 2017, below). And one of the two measured Ucrit values gives a required
frequency inside the claimed range. The honest result is a wider band, not a corrected point.

Every number below is a **calculation (derived)** unless marked otherwise. All inputs are from
S24 (`02279553:docs/research/fish/S24-behaviour.md`): U = 1.95 m/s, TL = 0.04 m, peak-to-peak
A = 0.20 TL = 8 mm (an S24 *assumption*), 52 Hz escape and 21 Hz steady maxima (Kyriakatos 2011,
measured), and Ucrit 0.548 m/s (Palstra 2010) vs 0.19-0.28 m/s (Wakamatsu 2019).

---

## 1. Independent arithmetic

The formula is f = St·U/A, with U = 1.95 m/s and A = 0.008 m (calc):

| St | Taxon it comes from | f (Hz) | ÷ 52 Hz |
|---|---|---|---|
| 0.20 | band, low edge | 48.8 | 0.94 |
| 0.30 | band, S24 central | 73.1 | 1.41 |
| 0.54 | goldfish | **131.6** | **2.53** |
| 0.79 | bullfrog tadpole | 192.6 | 3.70 |
| 1.02 | West African lungfish | 248.6 | 4.78 |

- **The lower bound reproduces.** 132 Hz and 2.5× match goldfish St 0.54.
- **The upper bound does not reproduce.** 199 Hz needs St = 199 × 0.008 / 1.95 = **0.816**.
  That is not tadpole 0.79 (193 Hz, 3.7×) or lungfish 1.02 (249 Hz, 4.8×). It is close to
  Eloy's model ceiling of "0.8 for the smallest tadpoles" (195 Hz). Either the author used a
  value the claim does not name, or used a different amplitude. I cannot tell which. The claim
  names lungfish 1.02 as evidence but then drops it from the range without saying so.
- **The baseline is misquoted.** S24's own range of 49-73 Hz against 52 Hz is a **0.94-1.4×**
  ratio, not "1.4×". The low edge clears 52 Hz.

## 2. The proxy: body size stands in for Reynolds number

The claim reasons "small swimmer, therefore low Re, therefore high St". The library's own regime
variable, however, is **Re at the operating speed**, not body length. The `domain_of_validity`
gives `reynolds_min: 1.0e4`. Using Re = U·L/ν with ν = 1e-6 m²/s (calc):

| Condition | Re |
|---|---|
| Goldfish, cited | 7.1 × 10³ |
| Lungfish, cited | 7.0 × 10³ |
| Zebrafish at Wakamatsu Ucrit 0.236 m/s | 9.4 × 10³ |
| Zebrafish at Palstra Ucrit 0.548 m/s | 2.2 × 10⁴ |
| **Zebrafish taxiing at 1.95 m/s (the quantity S24 needed)** | **7.8 × 10⁴** |

At the speed the requirement is computed for, the zebrafish sits **11× above** the cited goldfish
Reynolds number. It is also inside the library's stated validity domain for the cruising band.
The claim's sentence "a 4 cm zebrafish is that case" therefore does not hold at 1.95 m/s. It
does hold at slow swimming speeds; see §5.

Eloy's model puts St_opt ∝ Li^(1/3), where Li depends on the drag coefficient (library
`contested_by`). Drag coefficients fall as Re rises, so *by inference* that model also predicts
a lower optimum at 7.8 × 10⁴ than at 7 × 10³. I did not compute Eloy's Li for a zebrafish,
because I have no zebrafish C_d. This step is inference, not calculation.

## 3. The taxa are mostly the wrong body plan

The library line the claim draws on reads "small, low-Reynolds **and elongate** swimmers". Of the
listed taxa, tadpole, lungfish, hagfish, gar and eel are anguilliform or elongate. Zebrafish is a
subcarangiform fish with a forked caudal fin. Goldfish is the only morphological analogue in the
list. Using tadpole and lungfish values to set the upper bound treats body plan as irrelevant,
and the library entry itself does not say that.

## 4. The hidden assumption: fixed amplitude under a calibration that assumed St

S24 did not measure A. It **calibrated** it: at Ucrit 0.548 m/s, St 0.3 and 21 Hz give A = 7.8 mm
≈ 0.20 TL (S24 §3.2). The claim swaps in St 0.54 but keeps the A = 8 mm that came from St 0.3.
That pair is internally inconsistent with S24's measured inputs. At A = 8 mm, St 0.54 at Ucrit
0.548 m/s needs **37 Hz**, which is above the 21 Hz measured steady maximum (calc).

Relaxing the assumption means keeping S24's calibration and letting St be whatever it is, but
holding it constant across speed. Then St cancels: f_req = f_cal · U/Ucrit (calc). In this form
the answer depends on **which measured Ucrit is right**, and the sources disagree:

| Ucrit (source) | Implied peak-to-peak St at 21 Hz, A 8 mm | f_req at 1.95 m/s | ÷ 52 Hz |
|---|---|---|---|
| 0.548 m/s (Palstra 2010) | 0.31 | **75 Hz** | 1.44 |
| 0.28 m/s (Wakamatsu 2019, high end) | 0.60 | 146 Hz | 2.81 |
| 0.236 m/s (Wakamatsu 2019, 26 °C PET) | 0.71 | **173 Hz** | 3.34 |
| 0.19 m/s (Wakamatsu 2019, low end) | 0.88 | 216 Hz | 4.14 |

So the claim's range is *reachable*, but only under the Wakamatsu Ucrit and a constant-St
extrapolation. Under Palstra it is not, and S24's ~73 Hz survives. I preserve this
disagreement; I do not resolve it.

This relaxation still carries assumptions. It assumes a fish at Ucrit beats at the 21 Hz
maximum, but Kyriakatos and the Ucrit papers used different fish and rigs (challenge 37 flagged
the same circularity). It also assumes St does not fall with speed. That trend is plausible, but
I did not retrieve a source for it in zebrafish.

## 5. Zebrafish-specific data the claim missed

**Mwaffo, Zhang, Romero Cruz & Porfiri 2017, *PeerJ* 5:e4041, doi:10.7717/peerj.4041.**
Read level: **full-text**, through an automated page summariser, first 100k of 103k characters.
I did not read the figures.

- These are **measured** values: adult zebrafish, body length 3.4 ± 0.2 cm, flow 26, 39 and
  52 mm/s. "St was 0.366 ± 0.026 when cruising, compared to St = 0.515 ± 0.035 during bursting."
- The convention matters. The paper defines "St = fA∕V" with "A ... half of the maximum tail tip
  displacement". That is a **semi-amplitude** in the formula without the factor of 2. In the
  peak-to-peak convention used by the library and S24, the values become **≈ 0.73 cruising and
  ≈ 1.03 bursting** (my conversion, calc). This is exactly the factor-of-2 trap the library warns
  about. A reader comparing 0.366 directly to the 0.2-0.4 band would be misled.
- The regime is low: Re ≈ 900-3,400 if V is near the flow speed (calc; the paper reports no
  numeric V or Re in the text). The authors report "St was independent of Re" across their
  narrow range.

This **supports the claim's premise for slow-swimming zebrafish**. Adult zebrafish do sit above
0.2-0.4 at low Re, more strongly than goldfish. It does **not** measure St at 1.95 m/s, which is
23-75× faster than those flow speeds. Extrapolating it there with St 0.73 gives 178 Hz (3.4×),
and with St 1.03 gives 251 Hz (calc). That extrapolation crosses about 1.5 decades of Re and is
not justified by the paper's narrow range.

A university thesis summary says adult fish are usually near St 0.2-0.3, against 0.72 for larvae
at the highest larval Re (WUR thesis summary, "How fish larvae swim"). Read level:
**search-summary**. I don't know its amplitude convention, and I did not use it numerically.

**Negative search, with its scope:** I ran one web search ("adult zebrafish Strouhal number tail
beat amplitude swimming speed kinematics") and fetched one paper. I found **no measurement of
zebrafish St, tail-beat amplitude or frequency at U > ~0.6 m/s**. St at 1.95 m/s is **unknown**.

## 6. Evidence level

The `derived` label is honest for the frequency and ratio. The claim also states as fact that "a
4 cm zebrafish is that case". That is a regime classification, and it is wrong at the stated
speed. Presenting it as settled, rather than as an assumption, is the defect. The commit message
on `aebc0736` goes further: it calls this a correction that holds "A FORTIORI". That overstates
it, because the "correction" is one assumption swapped for another, with a different taxon basis.

## 7. What survives

- S24's qualitative conclusion survives both readings: a sustained taxi at 1.95 m/s needs more
  tail-beat frequency than any measured adult maximum, under every row except the band's low
  edge.
- The specific replacement figure, "132-199 Hz, 2.5-3.8×", does not survive as a correction. The
  supportable statement is a band that the Ucrit disagreement and the unknown St at high speed
  leave wide open:
  **≈ 49-250 Hz (0.94-4.8×)**, with **75 Hz (1.4×)** under Palstra calibration and **173 Hz
  (3.3×)** under Wakamatsu calibration (both derived, constant-St assumption).
- What would settle it is the zebrafish tail-beat frequency and peak-to-peak amplitude at
  U ≥ 1 m/s, or at least at Ucrit in the same fish that set Ucrit.

## Sources

| Source | Read level | Used for |
|---|---|---|
| `library/laws/strouhal.yaml` (branch `origin/swarm-architecture`) | full-text | Eloy values, `reynolds_min`, "elongate", convention warning |
| S24-behaviour.md and S24_calcs.py (commit `02279553`) | full-text | all inputs, calibration |
| Commit `aebc0736` message | full-text | origin of the claim |
| Eloy 2012, J Fluids Struct 30:205 | could-not-access by me; values taken only as relayed by the library entry | taxon St values |
| Mwaffo et al. 2017, PeerJ 5:e4041 ([PMC5691796](https://pmc.ncbi.nlm.nih.gov/articles/PMC5691796), [peerj.com/articles/4041](https://peerj.com/articles/4041)) | full-text (summarised, 100k/103k chars, figures not read) | adult zebrafish St and its convention |
| [WUR thesis summary, "How fish larvae swim"](https://www.wur.nl/es/article/Summary-of-the-thesis-How-fish-larvae-swim-from-motion-to-mechanics.htm) | search-summary | context only, not used numerically |

```swarm-challenge
{"claim_id": 52, "outcome": "weakened", "reason": "At the 1.95 m/s operating point a 4 cm zebrafish is at Re ~7.8e4 (inside the band's stated domain, 11x the cited goldfish Re), most cited taxa are elongate, the 199 Hz upper bound is not reproducible from any cited St, and holding A=8 mm while raising St contradicts S24's own calibration; the higher requirement is reachable only under the Wakamatsu Ucrit with a constant-St extrapolation.", "corrected_value": "49-250 Hz (0.94-4.8x the 52 Hz maximum); 75 Hz (1.4x) under Palstra-Ucrit calibration, 173 Hz (3.3x) under Wakamatsu-Ucrit calibration; St at 1.95 m/s unknown"}
```
