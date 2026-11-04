# Challenge 143 — adversarial review of [S20-D-D-D] (adult *Danio rerio* escape speed vs a 1 m launch)

**Claim under review (author's, not mine):** a direct measurement of adult *D. rerio* escape peak speed
(Demesmay et al. 2025, *PLoS Biol*: 157 ± 27 cm/s SD controls, 161 ± 33 cm/s mutants, n ≥ 11, 240 fps,
manual tracking) replaces S20-D-D's cross-species proxies (1.37 m/s central, 1.82 m/s guppy extreme).
Calculated deficit for a 1 m, 45° launch (3.13 m/s needed) is ×2.0 at the mean and ~×1.5 at +2 SD, so
"out of reach" stands; S20-D's 7 cm hop and 0.84 m/s Re-inverted burst fall. Recorded evidence level: measured.

**Verdict: SURVIVED.** I could not break it. Two minor caveats are noted below; neither changes the outcome.

## 1. Source check

- Demesmay et al. 2025, "Zebrafish fast muscle contractions avoid the mammalian requirement for
  voltage-gated Na+ channels", *PLoS Biol*, doi:10.1371/journal.pbio.3003484, PMC12604801.
  **Read-level: full-text** (methods, results and Fig 4 legend; the last ~38% of the page text, mostly references and supplements, was not read).
- Values in the paper match the claim exactly: maximal speed 157 ± 27 cm/s (controls), 161 ± 33 cm/s
  (*scn4aa−/−; scn4ab−/−* mutants); time to maximal speed 8 ± 4 / 9 ± 3 ms; distance in 40 ms 3.8 ± 0.8 /
  3.8 ± 0.9 cm; mean ± SD; "minimum of 11 per genotype"; 240 fps; Fiji manual tracking plugin; adults 4–12
  months, body length 2.6 ± 0.2 cm (4 mo) to 3.6 ± 0.2 cm (12 mo).
- Details the claim did not state: the camera was a **smartphone** (Xiaomi Redmi Note 13 Pro+) in slow-motion
  mode. The escape was triggered by a 1 g object dropped from ~30 cm into a 1.6 L tank holding 3–4 fish.
  The paper does not say which body point was tracked, how speed was differentiated or smoothed, the tank
  depth, or whether escapes were horizontal.

## 2. Independent arithmetic (calculated, not observed)

| Input | Value | Needed / input (3.132 m/s) | Level-ground 45° range v²/g |
|---|---|---|---|
| Required speed, 1 m range at 45°, no drag: v = √(gR) | 3.132 m/s | — | 1.00 m |
| Control mean | 1.57 m/s | ×1.99 | 0.25 m |
| Control +2 SD | 2.11 m/s | ×1.48 | 0.45 m |
| Mutant +2 SD | 2.27 m/s | ×1.38 | 0.53 m |
| Old proxy central | 1.37 m/s | ×2.29 | 0.19 m |
| Old proxy extreme | 1.82 m/s | ×1.72 | 0.34 m |
| S20-D Re-inverted burst | 0.84 m/s | ×3.73 | 0.072 m (matches the "7 cm hop") |

- 157/84 = ×1.87 (the claim says ×1.86, a rounding difference that doesn't matter).
- Flipping the conclusion needs a control fish at (3.13 − 1.57)/0.27 = **5.8 SD** above the mean, or 4.6 SD
  above the mutant mean. "Slightly narrower margin" is correct: ×2.29 → ×2.0 central, ×1.72 → ×1.48 extreme.
- If "1 m" means a 1 m **height**, the vertical exit speed needed is √(2gh) = 4.43 m/s, which is further out of reach.
  So the claim's 45°-range reading is the more lenient one.
- Air drag (my order-of-magnitude estimate: frontal area ~5×10⁻⁵ m², C_d ~0.5, mass ~0.3 g, all assumed)
  is ~5% of body weight at 3.1 m/s. It can only *raise* the speed needed, so ignoring it is conservative.
  (Calculated.)

## 3. Proxy check

The quantity that matters is **water-exit (launch) speed**. The measurement is **in-water peak C-start
speed**, reached ~8 ms after onset, in a horizontal-view startle. This is still a proxy, though now in the right
species. In my inference it acts as an **upper bound** on launch speed, not a lower one: a fish must also turn
its trajectory upward and break through the surface (added mass and surface work) before going ballistic.
The proxy's bias therefore favours the claim. I found no measurement of zebrafish water-exit speed.
Search scope: two web searches (standard + extended) on Demesmay/zebrafish escape speed. I did not search
specifically for *Danio* jumping kinematics, so that remains **unknown**.

## 4. Hidden assumptions, tested relaxed

1. **Measurement noise and undersampling.** Peak speed comes 8 ± 4 ms after onset, i.e. ~2 frames at
   4.17 ms/frame, from manual tracking of smartphone slow-motion video. Two biases pull in opposite
   directions. Undersampling and smoothing would *lower* the peak. Frame-differencing a manually clicked
   position and then taking the maximum would *raise* it: a 1 mm click error over one frame gives ±0.24 m/s.
   Plausibility check (my inference): 3.8 cm in 40 ms is a 0.95 m/s mean, which fits a ~1.6 m/s transient
   peak. The true peak would need to be ×2 the reported value to flip the conclusion. Neither bias is plausibly that large.
2. **Launch and landing at the same level.** The 3.13 m/s figure assumes a level-ground 45° trajectory.
   If the launch point is above the landing point (fish jumping *down* 1 m horizontally across a drop),
   the speed needed falls and the conclusion could change. I do not have S20-D-D's geometry, so for that
   regime the claim is **unverified**, not refuted.
3. **±2 SD as the extreme.** Individual values were plotted (Fig 4C) but I did not read them off. With n ≥ 11,
   the sample maximum is unknown. Still, 5.8 SD is far outside any tail the data could plausibly hide.
4. **Size.** The fish were 2.6–3.6 cm. Larger *Danio* would be faster in absolute terms, but adult *D. rerio*
   rarely exceed ~4–5 cm (general knowledge, not checked against a source here). A ×2 speed gain would need
   far more length than that.

## 5. Evidence level

The input speed is **measured** (from a full-text read), which is honest. The ×2.0 and ×1.5 deficits are
**calculated**, and the claim says so in its sentence. The recorded level "measured" with value "n/a" is acceptable
because the measured item is the input. A reader should not treat "out of reach" as an observation: no one has
observed a zebrafish failing to make a 1 m jump. It is a ballistic calculation on a measured in-water speed.

## 6. Counter-examples

I found no published report of *D. rerio* jumping close to 1 m (scope: the searches above only, which were not
designed to find one). Zebrafish jumping out of aquaria is common husbandry lore, but I have no figure for its
height or range, so that remains **unknown**.

## Sources
- Demesmay et al. 2025, PLoS Biol 10.1371/journal.pbio.3003484 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12604801/ (full-text)
- PLoS article page — https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.3003484 (search-summary)

```swarm-challenge
{"claim_id": 143, "outcome": "survived", "reason": "Source values verified in full text and arithmetic reproduces (3.13 m/s needed; x1.99 at mean, x1.48 at +2 SD; a flip needs a 5.8 SD outlier), and the remaining proxy gap (in-water C-start peak vs water-exit speed) biases toward the claim; caveat: an elevated-launch/downhill geometry was not tested.", "corrected_value": null, "depends_on": ["Demesmay et al. 2025 PLoS Biol adult D. rerio escape max speed 157 +/- 27 cm/s SD (controls) and 161 +/- 33 cm/s (mutants), n>=11, 240 fps", "1 m target interpreted as level-ground 45-deg ballistic range, no drag (v=sqrt(gR)=3.13 m/s)", "in-water C-start peak speed is an upper bound on water-exit speed"]}
```
