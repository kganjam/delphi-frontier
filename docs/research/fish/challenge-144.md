# Challenge 144: adversarial review of S24-D-D ("the f_max input strengthens S24-D's negative")

**Claim under review** (from `harvest:deepen-s24-sensitive-input-j77gqs`; document
`docs/research/fish/S24-D-deepen.md` on branch `claude/deepen-s24-sensitive-input-j77gqs`, which I
read in full along with its calc script). The claim says S24-D's 3-BL verdict is most sensitive to
f_max. It reads the Kyriakatos 2011 value of 52 Hz as a 40 mm fish's ceiling of about 30–43 Hz,
which widens the shortfall to about 1.4–2.7×. It adds that the fish would have to hold that rate
for 12–46 beats, against 3–5 cycles observed. Verdict: **strengthens**. Recorded evidence level:
**derived**.

**My outcome: WEAKENED.** The direction holds: every reading of the source that I can defend gives
f_req/f_max > 1. But two of the three legs are larger than the evidence supports:

- The **upper end (2.7×)** uses the bottom of the typical escape range as if it were a ceiling.
- The **duration leg** uses the length of observed behaviour as if it were an endurance limit.

A third issue, the unstated recording temperature, is untested and could push the opposite way.

I ran no experiment. Every number below is tagged **measured** (literature, with read-level),
**calc** (my own arithmetic, redone from the stated inputs), or **assumed**.

---

## 1. Independent arithmetic (calc)

I recomputed from U = 1.95 m/s, L = 0.040 m, λ = 0.8 / 0.6 / 0.48 L per beat, and f ∝ L^(−x)
from a 24 mm reference length.

| Quantity | My value | Author's value | Match? |
|---|---|---|---|
| f_req at λ 0.8 and 0.6 | 60.9 and 81.25 Hz | 61–81 Hz | yes |
| f_req at λ 0.48 | 101.6 Hz | 102 Hz | yes |
| R against 52 Hz | 1.17–1.56 | 1.17–1.56 | yes |
| Scale factor (24/40)^0.35 | 0.836, giving 52 → 43.5 Hz and 42 → 35.1 Hz | 43 Hz and 35 Hz | yes |
| Larval-anchor exponent x, from ln(95–100/52) / ln(18–30/4) | 0.30–0.43 | 0.30–0.43 | yes |
| Beats needed vs beats observed | 12/5 = 2.4 and 46/3 = 15.3 | 2.4–15× | yes |

**No arithmetic error.** The problems are in what the numbers are taken to mean.

**Internal inconsistency (calc).** The headline range "30–43 Hz" combines two kinds of number:

- The 43 Hz upper end has been size-scaled.
- The 30 Hz lower end has not. Scaled the same way (x = 0.35), it would be 25 Hz.

So the range is neither consistently scaled nor consistently raw. This is not what weakens the
claim, though; see §2.

## 2. Proxy check: is the right quantity standing in?

The quantity that matters is **the highest tail-beat frequency a 40 mm zebrafish can hold for about
12–46 beats.** The claim replaces it with two proxies, and both are biased.

**(a) The "ceiling" is partly a typical value.** I confirmed the source wording myself
(Kyriakatos et al. 2011, *J. Neurosci.* 31:8422, PMC6623330; **read-level: full-text** via an
automated fetcher, characters 0–100,000 of 101,006). The paper says escape frequencies ranged "from
30 to slightly >40 Hz", that escape activity never fell below 29 Hz, and that "Across animals, the
maximal frequency reached during escape was 52 Hz."

So 30 Hz is the **lower edge of the distribution of escape frequencies**, not a limit on what the
fish can do. A ceiling should come from the upper tail of that distribution. The only measured
upper-tail value is 52 Hz.

Scaling only the 52 Hz peak gives (calc):

| Exponent x | Basis | f_max at 40 mm | R (λ 0.8–0.6) |
|---|---|---|---|
| 0 | no size effect | 52 Hz | 1.17–1.56 |
| 0.30–0.43 | the author's own larval anchor | 41.7–44.6 Hz | 1.37–1.95 |
| 1 | assumed steepest bracket, not anchored | 31.2 Hz | 1.96–2.60 |

The larval-anchored reading (x = 0.30–0.43) is the defensible central reading, and it gives
**R ≈ 1.4–1.9**. The 2.7× needs both a typical value and an unscaled bottom value treated as the
ceiling.

**My inference:** the widening of the margin is real but modest, from 1.2–1.6 to about 1.4–1.9. It
is not the 1.4–2.7 the claim states.

**(b) "3–5 cycles observed" is a behaviour length, not an endurance limit.** The source (as above,
full-text) says these escapes happened "either spontaneously or upon casting a shadow on the
animals", in a still aquarium measuring 0.35 × 0.25 × 0.25 m. It reports no flow tunnel and no
forced swimming.

A C-start escape sequence is short because escape is a short behaviour. Nothing in the paper tests
how many cycles a fish *could* sustain at 40–52 Hz. A 35 cm tank is about 12–19 body lengths, which
also limits how long any fast bout can last.

At 42–52 Hz, 12–46 beats takes **0.23–1.1 s (calc)**. Fish burst swimming is conventionally
described as sustainable for seconds, not fractions of a second. That is my background knowledge
from fish-physiology convention (the Beamish-style classification of burst activity), **not read in
this session**, so I give it no number.

**My inference:** "would have to be held for 12–46 beats against 3–5 observed" shows that the long
bout was **not observed**. It does not show that the long bout **cannot happen**. As written, the
claim presents an absence of data as evidence of a limit.

**(c) "21 Hz for long bouts" is spontaneous still-water swimming.** The source says swimming
frequencies were "never exceeding 21 Hz". That is the fastest spontaneous swimming seen in a static
tank. It is not a forced maximum.

The author's own §4 keeps a vendor-protocol table of 26–33 Hz at Ucrit, with unknown provenance.
Despite that provenance, the table alone shows that 21 Hz cannot be taken as a ceiling for long
bouts. The key number "(21 Hz for long bouts)" mislabels the proxy.

## 3. Hidden assumption, relaxed: recording temperature

The source **does not state a water temperature for the in vivo EMG recordings**. My fetch found
only 20–22 °C, and that is for the separate in vitro preparation. The premise fish is taken to live
at a husbandry temperature of about 28 °C (inherited project premise, not re-checked here).

Muscle and pattern-generator frequencies in ectotherms rise with temperature. If the recordings were
made near room temperature, the 52 Hz peak **understates** f_max at 28 °C. That pushes against the
claim.

The size of this effect is **unknown**. I found no Q10 for zebrafish burst frequency in this session
(the search scope is in §5). It cannot reverse the result unless f_max reaches 61 Hz or more, which
would need about a 1.17× rise above 52 Hz before any size correction is applied. That rise is not
implausible over several degrees.

This is an open bias in the opposite direction, and the claim does not mention it.

## 4. Other points

- **"Most sensitive to f_max" is a framing overstatement.** R = U / (λ L f_max), so R has elasticity
  ±1 with respect to every input. f_max is not mathematically *more* sensitive than λ, L or U. The
  author's §1 says so and chooses f_max because it is the least well established input, which is a
  reasonable choice. The headline wording, however, claims a sensitivity ranking that the algebra
  does not support. This does not change the verdict.
- **Evidence level "derived" is honest.** The document tags the size correction as calc on an
  assumed exponent, and it explicitly declines to call the result a measured refutation. I found no
  derived number presented as measured, apart from the proxy mislabels in §2(b) and §2(c), which are
  problems of interpretation rather than of tagging.
- **The "1-BL closed" side remark is unaffected.** 195 Hz against any reading of 31–52 Hz is 3.8× or
  more (calc).
- **The refusal to restore the 132–199 Hz Strouhal figure is correct.** I agree that the two
  arguments should stay separate.

## 5. Counter-example search and its scope

I looked for any measured adult zebrafish kinematic burst or escape tail-beat frequency above
52 Hz, or any measure of burst endurance. **None found.**

- **Search 1:** one standard web search, "adult zebrafish tail beat frequency Hz critical swimming
  speed swim tunnel kinematics". It returned:
  - a vendor swim-tunnel protocol (ConductScience) whose example table, according to the search
    summary, has no values filled in (read-level: search-summary);
  - Mwaffo et al. 2017, *PeerJ* 5:e4041 (search-summary; I did not open it);
  - PMC8634626, a 2021 multi-species kinematics paper (search-summary);
  - a Bio-protocol Ucrit paper (search-summary).
  None of them gave an adult zebrafish frequency in Hz.
- **Search 2:** one full-text fetch of Kyriakatos 2011 (characters 0–100,000 of 101,006), for the
  temperature and setup.
- **Not searched:** Web of Science, Google Scholar, theses, Müller et al. 2000, and temperature
  (Q10) studies of zebrafish locomotor frequency.

So the claim's central fact still stands within this search scope: no measured adult zebrafish
frequency at or above 61 Hz is on record.

## 6. Verdict

**WEAKENED.**

What survives:

- The direction of the claim. On every defensible reading, f_max ≤ 52 Hz and f_req = 61–81 Hz, so
  R > 1.
- The finding that 52 Hz is a pooled single peak, not a typical value.

What does not survive as stated:

- **(i) The 2.7× upper end.** It treats the bottom of the typical escape range as a ceiling. With
  only the peak scaled on the author's own larval anchor, R ≈ **1.4–1.9 (calc)**. The steepest
  assumed exponent gives up to 2.6.
- **(ii) The duration leg.** "12–46 beats vs 3–5 observed" compares a requirement with the length of
  a behaviour seen in a still tank, not with a measured endurance limit.
- **(iii) "21 Hz for long bouts".** This is spontaneous still-water swimming, not a ceiling.
- **(iv) The unstated recording temperature.** It is an untested bias that could raise f_max.

The negative becomes "modestly firmer on the size and peak argument". It does not become
"substantially strengthened".

```swarm-challenge
{"claim_id": 144, "outcome": "weakened", "reason": "Arithmetic reproduces, but the 2.7x upper end treats the 30 Hz bottom of the usual escape range as a ceiling and the 12-46 vs 3-5 beat comparison treats the length of a spontaneous or shadow-evoked behaviour in a still 0.35 m tank as an endurance limit; scaling only the 52 Hz peak on the author's own larval anchor gives a modest widening, with an unstated in vivo recording temperature as an untested bias that could raise f_max.", "corrected_value": "f_max approx 42-52 Hz for a 40 mm fish (calc: 52 Hz peak scaled with x = 0-0.43), giving f_req/f_max approx 1.2-1.9 (1.4-1.9 at the anchored x 0.30-0.43); duration limit unknown (not measured)",
  "depends_on": ["S24-D f_req 61-81 Hz at U 1.95 m/s, L 40 mm, lambda 0.6-0.8 L/beat (commit aeb90402)", "Kyriakatos 2011 (full-text, chars 0-100000): 52 Hz max escape across animals; usual escape 30 to slightly >40 Hz; never below 29 Hz; 3-5 cycles; fish 18-30 mm; swimming never >21 Hz", "Kyriakatos 2011 setup: still 0.35x0.25x0.25 m aquarium, spontaneous or shadow-evoked escapes, in vivo temperature not stated (full-text)", "size exponent x 0.30-0.43 from larval 95-100 Hz at assumed 4 mm (author's anchor, search-summary; length assumed)", "EMG burst frequency = tail-beat frequency 1:1 (assumed)", "S24 sec 3.4 taxi run 12-46 beats (calc on assumed net force)", "burst swimming sustainable for seconds (background convention, not read this session)"]}
```
