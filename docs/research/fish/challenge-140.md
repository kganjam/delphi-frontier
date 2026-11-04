# Challenge 140: S20-D-D-D Danio-as-guppy exit speed (upper tail 2.06 m/s)

**Claim under review (S20-D-D-D):** S20-D-D's flip-prone input was its "extreme" Danio-as-guppy exit
speed of 1.82 m/s. The claim replaces it with a within-species jump/C-start ratio from Soares &
Bierman 2013, applied to *Danio*'s own C-start burst. That gives a typical 1.39 m/s (1.20–1.61) and
an upper tail of 2.06 m/s (1.79–2.39). These are calculated, not measured in *Danio*. On these
numbers a 1 m aerial escape (3.13 m/s) is still out of reach, the speed floor falls from 1.7× to
about 1.3×, and a 0.5 m escape is no longer excluded at the most generous corner. Verdict: stands.

Recorded evidence level: `derived`.
Source: `docs/research/fish/S20-D-D-deepen.md` and `S20-D-D-deepen_calc.py` on branch
`claude/deepen-s20-d-subproblem-b4iz3k`. I read both in full.

**Verdict: SURVIVED.** I tried five lines of attack, set out in §1–§5. None breaks the claim. Two
points should travel with it:

- The "~1.3× floor" is a corner-of-band number. The like-for-like point estimate is 1.52×.
- A jump-specialist cyprinid, the silver carp, scales to a speed closer to 3.13 m/s than any route
  in the claim. It still stays below 3.13 m/s, and it uses the same cross-taxon scaling the claim
  set out to avoid (§5).

Every number below that has no source attached is **my calculation**, not an observation.

---

## 1. Independent arithmetic

I recomputed from the stated inputs in a fresh script. I did not re-run the author's script.

| Quantity | My value |
|---|---|
| Speed needed for 1 m at 45°, drag-free: √(g·1 m) | 3.132 m/s |
| Speed needed for 0.5 m: √(g·0.5 m) | 2.215 m/s |
| Typical: 1.2357 × (0.78/0.80, 0.842/0.75, 0.91/0.70) | 1.205 / 1.387 / 1.606 m/s |
| Tail: 1.2357 + 2 × 0.30 = 1.8357, then the same factors | 1.790 / 2.061 / 2.386 m/s |
| Deficit for 1 m: tail midpoint / corner | 1.52× / 1.31× |
| S20-D-D's old floor: 3.132 / (1.50 × 1.2128) | 1.72× |
| Range at the 2.386 m/s corner, 45° | 0.580 m (this exceeds 0.5 m) |

**Every number in the claim reproduces to rounding.**

**Framing note.** The old 1.7× was S20-D-D's floor. The new ~1.3× is also a floor: the most generous
corner, low Danio burst combined with the high ratio. So "floor to floor" is a fair comparison. At
the tail **midpoint** the deficit is 1.52×. A reader should not quote 1.3× as the central estimate.

## 2. Source check: are the guppy inputs what the claim says?

**Source:** Soares & Bierman 2013, *PLoS ONE* 8:e61617 (PMC3629028).
**Read-level: full-text.** I fetched the Europe PMC fullTextXML and parsed it myself.

I confirmed these verbatim:

- Table 1:
  - "Maximum velocity in air (cm/sec) 123.57±30.0"
  - "Maximum velocity in water (cm/sec) 102.36 cm/sec ±33.75"
  - "Angle of attack of jump 77.4° ±24.91"
  - "Height of jump … 6.54±1.92"
  - "Fish weight (gm) 98±10"
- Fig. 2 caption: "** indicates the highest speed in the air (150 cm/sec)". This describes the
  illustrated jump. The text does not say it is a sample maximum, so the claim's diagnosis of
  S20-D-D is correct.
- The burst-speed sentence: "The burst speed, achieved with a C-start in animals of the same
  species and length, is about 70 to 80 cm/sec (extrapolated from [45] and this study)."

**An extra detail that supports the ratio framing.** The very next sentence reads: "In comparison,
the fastest speed we recorded in water was 100.16±33.9 cm/sec, and in the air … 123±30.0 cm/sec".

- So the authors themselves set the jump **means** against the 70–80 cm/s burst. That is the same
  pairing the claim uses for its ratio.
- The in-water figure here is 100.16, while Table 1 gives 102.36. This is an internal inconsistency
  in the source. It does not touch the in-air ratio, which is the one carrying the claim.

## 3. Proxies

**(a) Peak air speed used as the ballistic exit speed.**
- The authors say the peak occurs at about ¾–1 body length out of the water, while the tail is still
  thrusting. The ballistic speed that sets range can only be at or below this.
- So using the peak overstates range, which is generous to feasibility. The "1 m out of reach"
  conclusion is conservative in this respect.
- The 0.5 m corner statement is optimistic in the same respect.

**(b) The Danio C-start burst, 0.842 m/s.**
- The author left open whether this is a stage-1 maximum. If it were, the full burst would be
  higher, and the result would be fragile.
- Calculation: the corner flips at 1 m if the true Danio burst is ≥ 1.19 m/s. The midpoint flips if
  it is ≥ 1.28 m/s.
- Two pieces of evidence argue against a large understatement:
  - **The Re definition (relayed).** Challenge 75 (branch
    `claude/challenge-75-zebrafish-fast-start-im1x80`) relays from S21 that Danos & Lauder computed
    Re "using fish length, maximum linear velocity per sequence" at 1000 fps. If so, 0.842 m/s is a
    whole-sequence peak, not a stage-1 value. **Read-level for me: relayed. I did not read the
    Danos & Lauder full text.**
  - **An independent measurement (relayed).** Challenge 75 also digitised Miln et al. 2021
    (*R Soc Open Sci* 8:210146). Its adult zebrafish fast-start maxima span 0.45–1.38 m/s, as
    per-fish best of 4. These are figure-digitised, measured values; I relay them and did not
    re-digitise them.
    - Applying the claim's guppy mean-jump ratios (1.54–1.77) to the **fastest Miln fish** gives
      2.13–2.44 m/s. This is my calculation.
    - That lands at the claim's corner, not above it, and still below 3.13.
    - This is a cross-check only. Pairing a fastest individual with a tail ratio would count the
      tail twice.
- **Viscosity check.** The Danos & Lauder abstract (**read-level: abstract**, Europe PMC) defines
  the control as "1 mPa s (normal water)". So the claim's ν = 1.0×10⁻⁶ m²/s inversion matches the
  authors' own baseline. I tested whether a 28 °C ν (≈0.84×10⁻⁶) would cut U by about 16%; the
  abstract's statement removes that concern.

**(c) The guppy C-start, 70–80 cm/s.** This is the weakest link. The authors call it
*extrapolated*, and they do not say which statistic it is.
- Calculation: the 1 m conclusion flips at the tail only if the true guppy C-start is ≤ 0.49 m/s
  (with Danio at 0.842) or ≤ 0.53 m/s (with Danio at 0.91).
- That is about 27–29 SL/s for an 18.5 mm fish, against the authors' ~38–43 SL/s.
- That would need the authors' estimate to be roughly 1.4× too high. I could not reach Chappell &
  Odell 2004 to test this; I did not retry the route the author reported as 403.
- So the guppy C-start is **`unknown` beyond the authors' estimate**. The margin is real but not
  large.

## 4. Hidden assumption: a normal tail at mean + 2 s.d., tested relaxed

The upper tail rests on n = 20 lateral jumps by 5 males, with normality assumed. The raw per-jump
values are not published in the text. I relaxed it in two ways (calculated):

- **Mean + 3 s.d.** The guppy value is 2.14 m/s. That gives Danio 2.40 m/s at the midpoint and
  2.78 m/s at the corner. Both are still below 3.13.
- **How far the tail must stretch to flip 1 m.**
  - The corner needs a guppy jump at mean + **3.9 s.d.**
  - The midpoint needs mean + **5.2 s.d.**
  - Under normality, a 3.9 s.d. jump is about 1 in 20,000.
  - With a fat right tail it would be rarer than 1 in 40 but plausibly reachable. I cannot test the
    tail shape without the raw data.

An escape that happens 1 time in 20,000 is not a strategy that selection can build flight on. The
conclusion is robust to this relaxation.

## 5. Counter-examples and regimes

**Search scope:** one web search ("small freshwater fish jumping out of water exit velocity
high-speed video cyprinid OR killifish OR hatchetfish m/s"), first page of results, plus the two
Europe PMC fetches above. **Read-level: search-summary.**

**Killifish and hatchetfish.** The search returned no exit-speed values for either. This is a
negative result within the scope above.

**Silver carp, *Hypophthalmichthys molitrix*: a jump-specialist cyprinid.**
- A search summary of a 2020 *N Am J Fish Manag* study (doi 10.1002/nafm.10388) reports:
  - mean escape velocities of 4.71–6.28 m/s across three rivers;
  - a maximum of 7.71 m/s.
- **Read-level: search-summary.** I did not open the paper, and the body length of the jumping fish
  is `unknown` to me.
- **Illustrative scaling only.** At assumed lengths of 0.6–0.8 m, the max scales by v ∝ L^1/3 to
  **2.66–2.93 m/s** for a 33 mm fish. This is my calculation, and it uses the cross-taxon scaling the
  claim deliberately avoided.
- What it shows:
  - It is higher than every route in the claim, including the 2.39 m/s corner and the 2.38 m/s
    uncalibrated power model.
  - It is still below 3.13 m/s.
  - So a cyprinid jumping specialist does not overturn "1 m out of reach". It does reinforce the
    claim's own caveat that 0.5 m (2.21 m/s) is not safely excluded.
  - It also implies the claim's sentence "no route reaches 3.13 m/s" would come within about 7–15%
    under this route.

**Archer fish.** A search summary relays an MIT news quote putting exit speeds "on the order of …
2 meters per second". It gives no body length and no primary datum. I record it as qualitative only
and do not use it in any calculation.

## 6. Evidence level

`derived` is honest. In its own sentence the claim says "calculated, unmeasured in Danio". It labels
the jump/C-start ratio transfer as an assumption, and the normal tail as an assumption. I found no
derived number presented as measured.

## 7. Why it survived

- The arithmetic reproduces.
- The guppy inputs are quoted correctly from the full text.
- The source text itself supports pairing mean jump speed with the C-start estimate.
- The Danio burst's viscosity baseline matches the source abstract.
- Two independent relayed checks, the Re definition and Miln et al.'s measured maxima, put the Danio
  burst near or inside the claim's band. Neither puts it near the 1.19 m/s needed to flip the
  corner.
- Flipping the 1 m conclusion needs one of three things:
  - a guppy C-start about 1.4× lower than the authors' extrapolation;
  - a Danio burst about 1.4× higher than the 1000 fps measurement;
  - a jump about 3.9 s.d. above the guppy mean.

  None of these is supported by anything I could reach.

The claim's own caveats are correct and should be kept: the result is unmeasured in *Danio*, the
ratio transfer is assumed, and 0.5 m is not excluded.

### Sources

| Source | Read-level |
|---|---|
| S20-D-D-deepen.md + calc, branch `claude/deepen-s20-d-subproblem-b4iz3k` | full-text |
| Soares & Bierman 2013, *PLoS ONE* 8:e61617 (Europe PMC XML, parsed by me) | full-text |
| Danos & Lauder 2012, *J Exp Biol* 215:1854 (Europe PMC) | abstract |
| Challenge 75 (Miln et al. 2021 digitisation; S21's relayed Danos & Lauder Re definition), branch `claude/challenge-75-zebrafish-fast-start-im1x80` | full-text of the repository document; the primary sources are relayed |
| Silver carp escape velocity, *N Am J Fish Manag* 2020, doi 10.1002/nafm.10388 | search-summary |
| Archer fish exit speed, MIT news ([meche.mit.edu/node/1706](https://meche.mit.edu/node/1706)) | search-summary |
| Chappell & Odell 2004 | could-not-access (not retried) |

```swarm-challenge
{"claim_id": 140, "outcome": "survived", "reason": "Arithmetic reproduces (tail 1.79/2.06/2.39 m/s vs 3.13 m/s needed), guppy inputs verified in full text, the Danio burst's 1 mPa s baseline matches the source abstract and relayed Miln 2021 maxima keep it near the band, and flipping 1 m needs a ~1.4x error in the extrapolated guppy C-start or Danio burst or a ~3.9 s.d. jump; the ~1.3x floor is a corner (midpoint 1.52x) and a silver-carp L^1/3 scaling (2.66-2.93 m/s, search-summary) narrows but does not close the gap.",
  "corrected_value": null,
  "depends_on": ["Soares & Bierman 2013 in-air peak 123.57 +/- 30.0 cm/s (Table 1, full-text, verified)", "Soares & Bierman 2013 guppy C-start 70-80 cm/s, author extrapolation from Chappell & Odell 2004 (primary could-not-access)", "Danos & Lauder 2012 Re 27,800 at 1 mPa s, TL 33 mm -> 0.842 m/s (0.78-0.91) (abstract + relayed)", "relayed: Danos & Lauder Re uses maximum linear velocity per sequence (challenge 75 / S21)", "relayed: Miln et al. 2021 adult zebrafish fast-start maxima 0.45-1.38 m/s (challenge 75 digitisation)", "assumption: Danio jump/C-start ratio equals guppy's (unmeasured)", "assumption: guppy in-air speeds approximately normal (raw data unavailable)", "law: drag-free ballistic range R = v^2 sin(2a)/g at 45 deg", "S20 framing: 1 m aerial phase as the escape that must pay", "search-summary: silver carp escape velocity 4.71-6.28 m/s mean, 7.71 m/s max (doi 10.1002/nafm.10388), body length unknown", "assumption: silver carp 0.6-0.8 m length and v ~ L^1/3 for the illustrative scaling"]}
```
