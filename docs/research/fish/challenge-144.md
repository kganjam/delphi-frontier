# Challenge 144: adversarial review of S24-D-D ("the f_max reading strengthens S24-D's negative")

**Claim under review.** Source: `harvest:deepen-s24-sensitive-input-j77gqs`, file
`docs/research/fish/S24-D-deepen.md` (branch `claude/deepen-s24-sensitive-input-j77gqs`,
commit 19a608b). I read it in full, together with its script. The claim says S24-D's 3-BL verdict
(61–81 Hz needed, 1.2–1.6× the 52 Hz maximum) is most sensitive to f_max. It then reads the
primary source as giving a ceiling of about 30–43 Hz for a 40 mm fish, which widens the shortfall
to about 1.4–2.7×. Verdict recorded by the author: **strengthens**. Evidence level recorded:
**derived**.

**My verdict: WEAKENED.** The sensitivity ranking holds, and so does the arithmetic. The
"strengthens" verdict does not. The 30–42 Hz "usual escape" band in the primary source comes
from **one animal**. The claim presents it as typical of the 8 fish. The claim also uses that
typical band as a *ceiling*, which is the wrong proxy for a feasibility test. And the claim says
every correction pushes downward, which is false. Two inputs the source leaves unstated could
push the true ceiling upward. The recording temperature is not given for the in-vivo work, and
the fish were wire-implanted and only weakly stimulated. Once these are counted, I can defend
only the following (calc): R ≈ **1.2–2.1** on size correction of the peak alone. That is not
clearly wider than S24-D's 1.17–1.56. A temperature correction of unknown size could bring R
toward or below 1. S24-D's own position, "not shown to close, not refuted, thin margin", still
stands. It is neither strengthened nor weakened by this pass.

All numbers below are tagged **measured** (with read-level), **calc** (my arithmetic, done
independently and shown inline), or **assumed**.

---

## 1. Arithmetic, redone independently (calc)

f_req = U/(λL), with U = 1.95 m/s and L = 0.040 m:

- λ = 0.8 → 1.95/0.032 = **60.9 Hz**
- λ = 0.6 → 1.95/0.024 = **81.3 Hz**

These match the claim.

- R at 52 Hz = 1.17–1.56. Matches.
- R at 43 Hz = 1.42–1.89. R at 30 Hz = 2.03–2.71. So "1.4–2.7×" is the span from 43 Hz (λ 0.8)
  to 30 Hz (λ 0.6). Correct as arithmetic.
- Size scaling, f ∝ L^−x: 52 × (24/40)^0.35 = 52 × 0.836 = 43.5 Hz. Matches.
- Bout length: 12/5 = 2.4, and 46/3 = 15.3. Matches.

**Two internal inconsistencies in how the 30–43 Hz band is built (calc):**

1. **The band mixes a size-scaled upper end with an unscaled lower end.** The 43 Hz upper end is
   size-scaled. The 30 Hz lower end is not. Scaled the same way, 30 Hz becomes 25 Hz. This is
   conservative in the author's favour and is not a fault in the direction of the verdict.
2. **The reference length is set at the midpoint, 24 mm.** It is not known which fish produced
   the 52 Hz. Scanning the reference length over 18–30 mm at x = 0.35 gives a scaled peak of
   **39.3–47.0 Hz**, so R = 1.30–2.07. At x = 0, which the author keeps in their own grid, the
   peak stays at 52 Hz and R = 1.17–1.56.

The lower end of the claimed shortfall (1.4×) therefore rests on two assumed values: x = 0.35
and a 24 mm reference length.

## 2. Primary source, re-read (Kyriakatos et al. 2011, *J. Neurosci.* 31:8422, PMC6623330)

**Read-level: full-text.** I fetched the PMC HTML myself (218,859 bytes) and searched the
stripped text for each relayed quote. The quotes below are verbatim from that text.

| Claim's reading | What the text says | Consequence |
|---|---|---|
| "usual escapes at 30 to slightly >40 Hz" (typical of the 8 fish) | "In individual animals, the frequencies of swimming activity ranged from 2 to 21 Hz peaking at ∼8–10 Hz (Fig. 4D, white bars; **data from a single animal**). The frequencies generated during escape were much faster, ranging from 30 to slightly >40 Hz (**Fig. 4D**, black bars)." For the pooled data: "for escape from ∼30 Hz **toward faster frequencies** … Across animals, the maximal frequency reached during escape was 52 Hz" (Fig. 4E, n = 8). | **Misread.** The 30–>40 Hz band is Fig. 4D, the single-animal panel. The pooled n = 8 distribution is described only as "∼30 Hz toward faster frequencies", with a maximum of 52 Hz. Nothing in the text says that 52 Hz is an outlier, or that 40 Hz is the typical top across animals. (Fig. 4E's histogram itself was not read: image not accessed.) |
| "8 fish of 18–30 mm" | "The animals used in this study were 8–15 weeks old (body length 18–30 mm)." This sentence sits under the subheading "In vitro spinal cord preparation". The in-vivo EMG section gives no separate size. | Probably applies to all the fish, but the text only implies it. The claim states it as a measured fact about the EMG fish. A minor overstatement. |
| 21 Hz steady-swimming ceiling (n = 8) | "never exceeding 21 Hz (n = 8)" | Confirmed. |
| 3–5 cycles | "a few, in general three to five, short cycles of large EMG activity" | Confirmed. |
| frequency falls with size | "with larger body dimension, the swimming frequency decreases". This is a general statement about maturation, with no data or coefficient. | Confirmed, direction only. |
| (not addressed by the claim) recording temperature | The only temperature given is "fish saline at 20–22°C" for the **in vitro** preparation. **No water temperature is stated for the in-vivo EMG aquarium.** | See §3b. The temperature is **unknown**. |
| (not addressed by the claim) how escapes were triggered | "animals could swim and produce **spontaneous** escape. In some instances, escape behavior was evoked by **casting a shadow**." Recording began 15–20 min after recovery from anaesthesia, with wires implanted in the muscle. | See §3c. |

## 3. Hidden assumptions, tested relaxed

### (a) Proxy: a "typical" frequency used as a "ceiling"

The test is whether a fish *can* reach f_req. The quantity that answers it is the upper tail of
achievable frequency. A typical value does not answer it. The claim replaces the observed maximum
(52 Hz) with a typical band (30–42 Hz), and that band comes from one fish (§2). This is a proxy
swap. It moves R upward for a reason unrelated to capacity. A pooled maximum from n = 8
instrumented fish, with few escapes each, is if anything an **underestimate** of the population's
capacity. This is my inference: the sample maximum is a downward-biased estimate of the
population maximum.

**The defensible ceiling reading is the peak, size-corrected.** That gives 39–52 Hz (x 0–0.35,
reference length 18–30 mm, calc on an assumed exponent) and R = **1.17–2.07** (calc).

### (b) Temperature: a correction the claim omits, which could point the other way

The claim's §5 frames the settling experiment at 28 °C. Kyriakatos does not state the in-vivo
water temperature. If the aquarium matched the 20–22 °C in-vitro saline, which is **unknown** and
only my conjecture, a correction to 28 °C would raise f_max.

Illustrative calc only, with **assumed** Q10 = 1.5–2.0 over ΔT = 6 °C:

- correction factor 1.28–1.52×
- 52 Hz becomes **66–79 Hz**, which falls inside the 61–81 Hz requirement band (R ≈ 0.77–1.23)

I am not claiming the recording was at 22 °C, and I sourced no Q10 for zebrafish tail-beat
frequency. Both inputs are assumptions. The point is narrower. The author states that "all three
misapplications push the same way" (downward). An unaddressed correction of comparable size
could push the other way, and its sign and size are unknown. That is enough to stop "strengthens"
from following.

### (c) Instrumented fish and weak stimulus

The 52 Hz was recorded:

- in fish with intramuscular EMG wires
- 15–20 min after anaesthesia
- in escapes that were spontaneous or evoked by a shadow, not by a strong startle stimulus

Each of these is more likely to depress the observed peak than to raise it. This is my
inference; I have no measured size for the effect. The direction again runs against the claim's
"all corrections push down".

### (d) Size exponent

The exponent x = 0.35 is anchored on larval 95–100 Hz at an **assumed** larval length of 4 mm,
taken from search-summary sources. The comparison spans different studies, methods and life
stages. The author flags this honestly. I note that x = 0.35 alone carries the move from
R = 1.17 to R = 1.40 at the generous end.

### (e) Bout duration (survives, with a caveat)

"Held for 12–46 beats against 3–5 observed" is a fair statement of absence of evidence. The
caveat: escapes are short by behavioural definition, so a 3–5-cycle escape does not show that a
longer high-frequency bout is impossible. The figure of 12–46 beats is itself calc on an assumed
net force of 0.5–2 mN (S24 §3.4). This half of the claim is the part that genuinely tilts against
closure. It is a qualitative point and does not produce the 1.4–2.7× figure.

## 4. Evidence-level check

The claim records its evidence level as **derived**. That label is honest for the 30–43 Hz and
1.4–2.7× figures. The claim's body labels the size correction as calc on an assumed exponent,
which is also correct.

There is one evidence-level defect. "Usual escapes at 30 to slightly >40 Hz" is presented as a
measured, cross-animal characterisation. It is measured, but for **one animal** (Fig. 4D). A
single-animal value presented as a population-typical value is a mislabelled measurement.

## 5. Counter-examples and regimes missed

- **Search scope.** I ran no new literature search for adult zebrafish kinematic tail-beat
  frequency. I rely on the author's negative search scope (their §6) and do not extend it. My
  challenge rests on the primary source re-read (§2) and on the assumptions in §3. It does not
  rest on a new counter-example.
- **Temperature regime (§3b).** This is the main regime the claim misses.

## 6. Corrected statement

- The sensitivity ranking survives: f_max is the weakest input, and the arithmetic is correct.
- The defensible f_max for a 40 mm fish over ≤5 beats is **≈ 39–52 Hz** (calc). This is the
  measured 52 Hz peak, size-corrected on an assumed x = 0–0.35. It has further unquantified
  corrections: temperature, which is unknown and possibly upward, and instrumentation and
  stimulus, which are probably upward.
- That gives R ≈ **1.2–2.1** (calc). This is not established as wider than S24-D's 1.17–1.56, and
  it could fall toward 1 or below under a temperature correction.
- S24-D's "not shown to close, not refuted" stands **as recorded**. The duration argument
  (3–5 cycles observed against 12–46 needed) is the only part that legitimately tilts against
  closure, and it is qualitative.
- I agree with the author that the 132–199 Hz Strouhal figure stays fallen.

**Measurement that would settle it.** This is the author's §5.1: high-speed kinematics of
35–40 mm adults. I would add two requirements: a **stated water temperature**, and a strong
startle stimulus, not a shadow.

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| 1 | S24-D-deepen.md and S24-D-deepen_calc.py (branch `claude/deepen-s24-sensitive-input-j77gqs`, 19a608b) | full-text | the claim under review |
| 2 | Kyriakatos A et al. 2011, *J. Neurosci.* 31:8422, PMC6623330 | full-text (PMC HTML fetched and searched by me; figure images not viewed) | verbatim quotes in §2; single-animal source of the 30–>40 Hz band; in-vivo temperature not stated; spontaneous or shadow-evoked escapes; implanted fish |
| 3 | Q10 range 1.5–2.0 | **assumed**, not sourced | illustrative temperature correction only (§3b) |

```swarm-challenge
{"claim_id": 144, "outcome": "weakened", "reason": "Arithmetic and the f_max sensitivity ranking hold, but the 30-to-slightly->40 Hz 'usual escape' band is from a single animal (Kyriakatos 2011 Fig. 4D, full-text), a typical value is the wrong proxy for a ceiling, and unaddressed corrections (unstated in-vivo temperature, wire-implanted fish, shadow-evoked escapes) plausibly push f_max up, so only R ~1.2-2.1 on size-corrected peak is defensible and 'strengthens' does not follow; S24-D stands as recorded.", "corrected_value": "f_max ~39-52 Hz for a 40 mm fish over <=5 beats (calc: 52 Hz peak, size exponent assumed 0-0.35, Lref 18-30 mm; temperature correction unknown), f_req/f_max ~1.2-2.1", "depends_on": ["Kyriakatos 2011 full-text: 52 Hz max escape across animals n=8 (Fig. 4E); 30 to slightly >40 Hz escape range from single animal (Fig. 4D); 3-5 cycles; 18-30 mm stated under in-vitro methods; in-vivo water temperature not stated; spontaneous or shadow-evoked escapes in wire-implanted fish", "S24-D answer: f_req 61-81 Hz at U 1.95 m/s, L 40 mm, lambda 0.6-0.8 L/beat (commit aeb90402)", "size-scaling exponent x 0-0.35 (assumed, author's larval anchor, search-summary)", "Q10 1.5-2.0 (assumed, illustrative only)", "S24 taxi run 12-46 beats (S24 sec 3.4, calc on assumed net force 0.5-2 mN)"]}
```
