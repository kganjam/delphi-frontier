# Challenge 75: adult zebrafish fast-start maxima, 0.45–1.38 m/s (Miln et al. 2021)

**Claim under review (S21-D):** "S21-D VERDICT STRENGTHENS: directly measured adult zebrafish fast-start
maxima span 0.45-1.38 m/s (Miln et al. 2021, n=50, 120 fps, full text, values digitised from Fig 1a),
BRACKETING the Reynolds-derived 0.842 m/s. The fastest individual is still ~4.2x below the 5.84 m/s
threshold."
Recorded evidence level: *measured*. Value: 1.38 m/s. Source document: `docs/research/fish/S21-deepen.md`
(branch `claude/zebrafish-fast-start-velocity-pgqbck`).

**Verdict: SURVIVED.** I could not break the numbers. Two framing points need correcting, and the
margin is conditional on the threshold (§3, §5), but none of that makes the claim's own sentences false.

---

## 1. Independent re-digitisation (not copied from S21-D)

**Source:** Miln C, Ward AJW, Seebacher F (2021), *R Soc Open Sci* 8:210146, doi:10.1098/rsos.210146.
**Read-level: full-text.** I fetched the Europe PMC XML for PMC8025299 and the figure JPEGs from the
Europe PMC supplementary-files bundle myself.

**Methods, as the authors state them (author's claims):**
- Fish: adult short-fin zebrafish of mixed sex. Groups were size-matched to within 2 mm SL.
- Arena: escapes were induced by a mechanical stimulus to the tail, in a tank 405 × 600 mm with
  30 mm of water.
- Filming: 120 frames s⁻¹ (GoPro Hero 6), with a submerged 300 mm ruler as the scale, tracked in
  Tracker 4.01.
- Tracking point: "centre of mass … 0.35 body lengths from the tip to the snout".
- Value used: "four escape responses were analysed for each fish and the fastest speed was used".
- The text gives **no numeric summary** of fast-start speed.

**My pixel measurements.** I located the axis ticks and the extreme ring centres with a colour mask
on the JPEGs. These are calculations from the image, not the authors' numbers.

**Fig. 1a** (x = fast start speed)
- Ticks: 0 → px 78.5, 0.5 → 160.5, 1.0 → 241.5, 1.5 → 323.5. That gives 163 px per m s⁻¹.
- Rightmost ring centre: px ≈ 304, which is **1.38 m/s**.
- Leftmost ring centre: px ≈ 152, which is **0.45 m/s**.

**Fig. 2c** (an *independent* panel with the same x-variable; S21-D did not use it)
- Ticks: 0.4 → px 499, 1.4 → px 647. That gives ≈148 px per m s⁻¹.
- Rightmost ring centre: px ≈ 644, which is **1.38 m/s**.
- Leftmost ring centre: px ≈ 506, which is **0.45 m/s**.

The two panels agree to about 0.005 m/s. I take the read uncertainty to be roughly ±0.01–0.02 m/s,
allowing for JPEG artefacts and a ring radius of about 5 px.

**On the over-count.** Fig. 1a plots each fish's single fast-start value three times (day 1, 4 and 7
colours), which is why a ring detector "over-counts". The authors report df = 137, consistent with
≈ 3 × 50 observations. This explains S21-D's 54–142 rings without undermining the range.

**Range: confirmed, 0.45–1.38 m/s.**

**Where the maximum sits.** At x ≈ 1.38 there is one ring in each of the three colours, so 1.38 m/s
is **one fish**. That fish is separated by about 0.2 m/s from the next-fastest cluster (≈1.15 m/s).
This is my reading of the figure.

**Arithmetic, recomputed:**
- 5.84 / 1.383 = **4.22×**.
- With the 5.8 m/s threshold that S21 used: 4.19×.
- **"~4.2×" is correct.** 0.842 lies inside [0.45, 1.38], so **"bracketing" is correct.**

## 2. Evidence level

"Measured" is defensible, because the quantity is a direct kinematic measurement by the authors.
However, the *number* 1.38 is **figure-digitised by a reviewer, from a single fish**. The claim says
"values digitised from Fig 1a" in the same sentence, so the disclosure is in place. I would record it
as `measured (figure-digitised; figshare raw data could-not-access)`. I tried
`api.figshare.com/v2/collections/5359401/articles` and got a proxy CONNECT 403, the same result
S21-D reported.

## 3. Proxies: is the right quantity being compared?

**(a) S21's 0.842 m/s is not the weak proxy S21-D says it is.**
- S21-D (§1–2) writes that S21's source was unknown and that its Re "may be built from the mean
  speed … circular at best".
- The S21 write-up exists on branch `claude/zebrafish-fast-start-velocity-pxsv7e`
  (`docs/research/fish/S21-behaviour.md`). It quotes Danos & Lauder 2012 (*J Exp Biol* 215:1854;
  S21 records read-level full-text HTML; I did not re-read it). In that paper Re was computed
  "using fish length, **maximum linear velocity per sequence**", filmed at **1000 fps**,
  n = 5 adults, TL 33 mm.
- So 0.842 m/s is a mean of per-sequence peaks recovered from a 1000 fps measurement. That is a
  better-resolved instrument than Miln's 120 fps.
- The fairer description of S21-D is therefore **independent corroboration at larger n**, not "a
  direct measurement replaces the proxy". This is my inference. It does not change the claim's
  numbers, and the word "STRENGTHENS" is still apt, because two labs and two instruments agree on
  the magnitude.

**(b) "Bracketing" compares unlike statistics.**
- One side is a mean of per-sequence peaks (n = 5).
- The other is a spread of per-fish best-of-4 maxima (n = 50).
- Best-of-4 should sit *above* a mean of peaks. Coarse frame rate should push it *below*.
- My visual estimate of the Miln centre, ≈0.75–0.85 m/s, lands on 0.84. That suggests the two
  biases roughly offset. This is an inference, not a measurement.

**(c) The quantity that matters for the threshold is water-exit airspeed, not in-water COM peak.**
- What the threshold is: 5.84 m/s is the glide/stall-type design speed for a 1-BL-span wing at
  AR 5, C_L 0.6 (`zebrafish-glide-physics.md`; challenges 1, 3, 5). It is the speed needed in air.
- What the measurement is: peak in-water centre-of-mass speed, in a 30 mm-deep tank, moving
  horizontally.
- Why this is conservative for the claim: breaking the surface and climbing against gravity can
  only lose speed. So the in-water peak is an **upper bound** on exit speed, and the proxy errs in
  favour of feasibility.
- Not covered: a surface-taxi phase that adds thrust after exit (S24) is outside this claim.

## 4. Hidden assumption: 120 fps does not badly under-read the peak (tested relaxed)

I modelled the peak as Gaussian in time and frame-differenced at 120 fps (8.33 ms). The worst case is
the peak landing on a frame boundary. These figures are **calculated**, not measured:

| COM velocity-peak FWHM | Worst-case read / true | Fastest fish, true | Margin to 5.84 |
|---|---|---|---|
| 20 ms | 0.86 | 1.61 m/s | 3.6× |
| 15 ms | 0.78 | 1.78 m/s | 3.3× |
| 10 ms | 0.61 | 2.28 m/s | 2.6× |
| 5 ms | 0.32 | 4.33 m/s | 1.35× |

- **To close the gap**, the COM peak would need a FWHM of about 3–4 ms and the worst phase alignment.
- **Is a pulse that narrow plausible?** A narrow pulse would make Miln's 120 fps bulk read about 3×
  below the 1000 fps Danos & Lauder value. Instead the two sit together near 0.8 m/s. This empirical
  cross-check bounds the under-read to well under 2× for the typical fish. The cross-check is my
  inference. I did not find a published adult zebrafish COM velocity trace to measure the FWHM
  directly; that remains `unknown`.
- **Temperature.** Miln tested at 23 °C rather than 28 °C. The full text says "Water temperature was
  23°C (± 0.5°C) during all experiments", which I confirmed. That could also under-read.
- **Combined worst case.** A hypothetical 1.4× temperature factor combined with the 10 ms row gives
  ≈3.2 m/s, still about 1.8× below 5.84. The 1.4× is an assumed bounding value, not a sourced Q10.

**The 4.2× point estimate survives this relaxation.** Its honest band is roughly 2–4×, because the
biases all push the true value up. That is consistent with S21-D's own "~4–7×" wording and its
hypothetical 2× row.

## 5. The margin depends on a contested threshold

The claim states the margin against 5.84 m/s and is correct against that number. That threshold is
itself *derived*, and sibling challenges marked it **weakened**:

| Threshold (source) | Fastest fish 1.38 m/s is below it by |
|---|---|
| 5.84 m/s, 1-BL, AR 5, C_L 0.6 (design point) | 4.2× |
| 4.2–4.7 m/s, C_L,max 0.93–1.15 (challenge 1, relayed search-summary) | 3.0–3.4× |
| 4.37 m/s, C_L 1.07 (challenge 5) | 3.2× |
| 2.0–3.7 m/s, same 1-BL span at AR 1–2 (challenge 3) | 1.45–2.7× |
| 1.95 m/s, 3-BL span (S24) | 1.41× |

The ratios are my calculations. At the low-threshold corners, a fastest fish with a plausible
under-read (§4, 10–15 ms rows) would reach the threshold. **That does not falsify the claim as
written.** It means anyone reusing "~4.2×" must carry the C_L/AR/span assumption with it.

## 6. Counter-examples searched

**Scope:**
- One standard web search: adult zebrafish escape fast-start maximum velocity m/s Seebacher.
- Cross-branch `git grep` of this repository for `5.84` and the S21 records.

**Result:**
- No adult *Danio* fast-start speed above 1.38 m/s turned up.
- Danos & Lauder 2012 Table 1 (direct max COM velocity, 1000 fps) is still unread, and is image-only
  per S21. If it reported a fastest-sequence value well above 1.38 m/s, the bracket would still hold
  but the "fastest individual" margin would shrink.
- Not covered: theses, Chinese-language literature, Condon et al. 2010 Fig. 1 (200 Hz), and other
  *Danio* species or strains.

## 7. Sources

| Source | Read-level |
|---|---|
| Miln, Ward & Seebacher 2021, *R Soc Open Sci*, doi:10.1098/rsos.210146 | full-text (Europe PMC XML) + Fig. 1 and Fig. 2 images, digitised by me |
| Miln et al. figshare doi:10.6084/m9.figshare.c.5359401 | could-not-access (proxy 403) |
| Danos & Lauder 2012, *J Exp Biol*, doi:10.1242/jeb.068957 | not read by me; relayed from S21-behaviour.md, where it is recorded as full-text HTML |
| `S21-deepen.md`, `S21-behaviour.md`, `challenge-1/3/5.md`, `S24-behaviour.md` (this repo, other branches) | full-text |
| Web search results: [PMC11930232](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11930232/), [PMC5394678](https://pmc.ncbi.nlm.nih.gov/articles/PMC5394678) | listing only; no adult m/s value |

```swarm-challenge
{"claim_id": 75, "outcome": "survived", "reason": "Independent digitisation of Miln et al. 2021 Fig 1a and the separate Fig 2c both give 0.45-1.38 m/s (the 1.38 is a single fish), 0.842 lies inside that range, and 5.84/1.383 = 4.22x; relaxing the 120 fps and 23 C biases plausibly narrows the margin to ~2-4x but not to closure, though the margin is only as firm as the derived 5.84 m/s design-point threshold, and S21's 0.842 came from 1000 fps per-sequence maxima (Danos & Lauder), so it is corroborated rather than replaced.", "corrected_value": null,
  "depends_on": ["Miln et al. 2021 Fig 1a and Fig 2c fast-start axis (full-text, digitised by me)", "5.84 m/s threshold (derived: 1-BL span, AR 5, C_L 0.6; weakened in challenges 1, 3, 5)", "Danos & Lauder 2012 mean maximum Re 27,800 at 1000 fps, as relayed by S21-behaviour.md (not read by me)", "assumption: COM velocity-peak FWHM >= ~10 ms, so 120 fps under-reads by < ~1.6x (calculated, unmeasured)"]}
```
