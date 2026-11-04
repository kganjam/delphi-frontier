# Challenge 143: adversarial review of S20-D-D-D (adult *Danio* escape speed)

Claim under review: S20-D-D-D, `docs/research/fish/S20-D-D-deepen.md` on branch
`origin/claude/deepen-s20-d-d-sensitive-input-5jvia6` (harvest id
`deepen-s20-d-d-sensitive-input-5jvia6`). I read it in full from that branch, along with its script.

Independent arithmetic: `docs/research/fish/challenge-143_calc.py`. Run it from the repository root.
Every number below that is not attributed to a source is a **calculation** from that script.
Date: 2026-11-04.

**Verdict: SURVIVED.** The headline holds. The source exists and says what the author says it
says. The SD really is an SD. The arithmetic reproduces. Every bias I could find in the proxy either
strengthens the "out of reach" conclusion or is too small to close a ×2 gap. I found three small
defects in the parent document, all outside the claim's sentence (§6). None of them changes the
verdict.

---

## 1. Arithmetic, redone from the stated inputs

I wrote my own script and did not copy the author's working. Drag-free; R = v² sin 2α / g.

| Quantity | Mine | Claim |
|---|---|---|
| v for a 1 m range at 45° | 3.132 m/s | 3.13 |
| Deficit at the control mean, 1.57 | ×1.995 | ×2.0 |
| Deficit at +2 SD, 2.11 | ×1.484 | ~×1.5 |
| Deficit at +1 SD, 1.84 | ×1.70 | (×1.7 in doc) |
| Deficit at the mutant mean, 1.61; at mutant +2 SD, 2.27 | ×1.95; ×1.38 | (×1.95 in doc; +2 SD not given) |
| SDs above the control mean needed to reach 3.13 | 5.79 | 5.8 |
| SDs needed with a guppy air/water gain of 1.24/1.02 | 3.73 | 3.7 |
| 1.57 ÷ Danos & Lauder Re inversion (27 800 × 10⁻⁶ / 0.033 = 0.842) | ×1.864 | ×1.86 |
| S20-D-D extreme, 1.50 × (33/18.5)^(1/3) | 1.819; ×2 = 3.64, which flips | 1.82, flips at ×2 |
| 45° range at 1.57 | 25.1 cm | 25 cm |

Everything reproduces. The mutant +2 SD row (×1.38) is the most generous single-group reading. The
claim did not quote it, but it is still well short of ×1.

## 2. Is the source real, and does it say this? (full-text check)

I fetched Demesmay et al. 2025, *PLoS Biol* 23(11):e3003484, independently from the Europe PMC
`fullTextXML` endpoint for PMC12604801. Read-level: **full-text**. Every quoted value is there
verbatim:

- "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants)".
- "latency to attain maximal speed (8 ± 4 ms for controls and 9 ± 3 ms for mutants)".
- "Distance covered in 40 ms … (3.8 ± 0.8 cm for controls and 3.8 ± 0.9 cm for mutants)".
- The Fig 4C legend reads "Graphs represent mean ± SD with individual values … (minimum of 11 per
  genotype)".
- Methods: Xiaomi Redmi Note 13 Pro+ at "240 frames/s (escape response, 1 s long videos)". Objects
  of 1 g were dropped from about 30 cm into 1.6 L tanks holding 3–4 fish each. Analysis used Fiji's
  "manual tracking plugin". The lengths are "2.6 ± 0.2 cm for 4-month-old and 3.6 ± 0.2 for
  12-month-old fish".

**SD or SEM?** This was the obvious way to break the claim. The paper's general statistics
paragraph says data are "means ± SEM", but it names only Figs 2B and 2C. The Fig 4C legend
explicitly says SD. If these were SEMs with n ≈ 11, the SD would be about 27 × √11 ≈ 90 cm/s, and a
1 m launch would sit only about 1.7 SD away. The text values match the Fig 4C legend, so I accept
SD. This rests on the legend, which is author text.

**Per-fish values.** I independently re-downloaded S1 Data (`pbio.3003484.s015`). It has one sheet,
"Feuil1", headed "Numerical values of resting membrane potentials in Fig. S1". I confirm that the
**Fig 4C per-fish speeds are absent**. Two other supplements are PDFs: s014 (gel images) and s016
(the response to reviewers, which repeats the same sentence). Neither contains per-fish speeds. I
did not inspect s013 (a .docx) or s017 (a PDF). So the real individual maximum is still `unknown`.

## 3. Is a proxy standing in for the quantity that matters?

Yes, and the author says so in the document (§3.1, §6). The quantity that matters is **the
centre-of-mass velocity at the moment the body clears the surface, on an upward launch**. The
measurement is **the 2-D peak speed of an unstated tracked point, in a horizontal in-water escape
from an overhead drop**. Here is how each gap pushes the result.

| Gap | Direction for the "out of reach" verdict | Can it close ×2? |
|---|---|---|
| Tracked point may be the head, not the CoM | 1.57 overstates CoM speed, which **strengthens** the verdict | n/a |
| Max-of-noisy-frames bias (manual clicks) | overstates, which **strengthens** it | n/a |
| 240 fps smooths a short peak | understates, which weakens it | No. Smoothing cannot hide a ×2 peak when the 40-ms mean is only 0.95 m/s |
| 2-D projection, view axis unstated | understates by a factor of 1/cos(out-of-plane angle) | Only if the motion is about 60° out of the image plane, implausible for the bulk of an escape |
| Stimulus may be submaximal; jumps are a different behaviour | understates | Partly. The only reference available, a heterospecific guppy air/water ratio, is ×1.22 (Soares & Bierman 2013, relayed via S20-D-D, not re-read). The author already tested it: 3.7 SD |

**Something I tried that failed (reported, not used).** I first suspected that the 8 ms peak latency
falls *before* the 13 ms maximal C-bend. That would make 1.57 m/s a rotational head speed during
stage 1. My rotation-only estimate of stage-1 head speed is 0.7–1.3 m/s mean (script), which is
compatible with that idea. But the Fig 4C legend groups "maximal speed latency" under the
"following swim". So the latency may be counted from the end of the C-bend, not from onset. The
paper does not say which. I cannot resolve this, so I make no claim from it. Either reading leaves
the verdict standing, because a head-speed reading only lowers the CoM value.

## 4. Hidden assumptions, relaxed

- **Drag-free.** I assumed 0.4 g, 0.25 cm² frontal area and C_d 0.5. Air-drag deceleration at
  3.13 m/s then comes to about 0.18 m/s², which is 2% of g (calculation). Drag can only raise
  v_need. Relaxing this assumption does not help the fish.
- **Normal tail at +2 SD.** n ≥ 11 per group, so the largest of 11 normal draws sits around +1.6 SD.
  To flip the verdict, some fish would have to reach 3.13 m/s (5.8 SD), or 2.58 m/s with the
  inferred air gain (3.7 SD). This needs a heavy right tail that the reported SD does not suggest.
  It is untestable without per-fish data, as the author says.
- **The 1 m target.** This framing is inherited from S20. At 0.5 m, v_need is 2.21 m/s, which sits
  at about +2.4 SD. That is still out of reach at the mean. The author tested this too.
- **Pooled ages.** The SD mixes 2.6 cm and 3.6 cm fish. If bigger fish are faster in absolute
  terms, the 12-month subgroup mean is higher than 1.57. The subgroup values are `unknown`. Even a
  subgroup mean of 2.0 would leave ×1.57.

## 5. Counter-examples from other regimes or taxa

I ran two web searches this session (scope stated):

1. "adult zebrafish fast-start escape maximum velocity m/s kinematics high-speed". Read-level:
   search-summary. **No second adult *D. rerio* peak-speed value was found.** The hits were larval
   work, a least-killifish 3-D study and Danos & Lauder 2012.
2. "small fish leap height body lengths … hatchetfish splash tetra exit velocity". Read-level:
   search-summary.
   - Relayed figures: guppy about 3.5 body lengths; archerfish and *Toxotes microlepis* up to
     2.5 BL at ≤ 1.4 m/s (fish 6.8–11.1 cm).
   - Hatchetfish (Gasteropelecidae) are described as ballistic jumpers. No height or speed was
     found.
   - A 1 m 45° launch needs a vertical-equivalent speed of √(2gH) at H = 50 cm. For a 3.3 cm fish,
     that is about 15 BL (calculation). No small-fish leap of that size was found.

**Negative-search scope.** Two queries, both search-summary only. No hatchetfish or splash-tetra
kinematics were read. The hatchetfish literature is the most likely place a counter-example in a
small fish could hide. It is unread here, not ruled out.

- Danos & Lauder 2012 PDF: `sites.harvard.edu` is outside this session's allowed network domains.
  **could-not-access.** So the question of whether their velocity column matches 0.84 or 1.57 m/s
  is still open.
- Chang et al. 2019 via Europe PMC (PMC6451394): the full-text endpoint returned an empty record.
  **could-not-access.** That paper notes, as relayed in the search summary, that exit velocity is
  inferred from leap height rather than measured. This matches the author's negative finding that
  no adult *Danio* exit speed exists.

## 6. Defects found (author's document, not the claim sentence)

1. **Mislabelled "Apex" column.** In the parent's §4 table, "Apex" sits next to "45° range" but is
   computed as v²/2g. That is the height of a *vertical* jump. The apex of the 45° trajectory is
   v²/4g, half as high: 6.3 cm at 1.57 m/s, not 12.6 cm, and 25 cm for the 1 m launch, not 50 cm
   (calculation). The prose's "or about 12.6 cm vertical apex" can be read correctly, but the table
   row "S20 1 m launch | 100 cm | 50 cm" is wrong as a 45° apex. This is cosmetic: no deficit uses
   it.
2. **Strain description understated.** The parent says the controls are "not a named wild-type
   strain". The paper states that mutant lines "were established on AB genetic background by
   outcross with WT animals over a minimum of 5 generations" (full-text). The controls are
   +/+ siblings on that background. This is minor and slightly *strengthens* the source.
3. **Evidence-level label.** "measured" is right for the 1.57 ± 0.27 m/s in-water escape peak. The
   claim's headline is a deficit, and the claim correctly calls that "calculated". It also correctly
   says "in water" in the key number. Even so, the claim's opening ("a direct measurement … replaces
   [exit speed]") reads as though exit speed was measured. It was not; it is a proxy. I note this as
   a wording risk, not a defect, because the key number states the regime.

## 7. Why SURVIVED

- **Author's claim:** the 1 m launch is out of reach at ×2.0 (mean) to about ×1.5 (+2 SD) in
  speed, now on a conspecific basis.
- **My inference:** the claim holds, for four reasons.
  1. The source exists and says this (full-text, re-fetched).
  2. The dispersion is an SD (legend).
  3. The arithmetic reproduces to three figures.
  4. The biases split two ways. Those that inflate 1.57 (head point, max of noisy frames) make the
     launch harder still. Those that deflate it (frame rate, projection, submaximal stimulus, the
     air gain) are each well under the ×2 needed. The one tested numerically, the air gain, still
     leaves the fish 3.7 SD short.
- **The sub-claim that the 0.84 m/s Re-inverted burst "falls".** This holds in the sense S20-D used
  it, as an *upper bound*. Both the 1.57 m/s peak and the noise-robust 40-ms mean of 0.95 m/s
  exceed it. What remains unresolved is the reason (Danos & Lauder Table 1 could-not-access). As the
  author did, I keep the two sources' disagreement rather than averaging it.

**What would break it:** either of these would flip the verdict.
- Fig 4C per-fish data showing any fish ≥ 2.6 m/s (with the air gain) or ≥ 3.13 m/s (without).
- A measured small-fish surface exit at ≥ 3 m/s. The hatchetfish literature is unread.

### Sources

| Source | Read-level |
|---|---|
| S20-D-D-D: `docs/research/fish/S20-D-D-deepen.md` and its `_calc.py` (branch `claude/deepen-s20-d-d-sensitive-input-5jvia6`) | full-text (repository) |
| Demesmay L et al. 2025, *PLoS Biol* 23(11):e3003484, doi:10.1371/journal.pbio.3003484, PMC12604801 | full-text (Europe PMC XML, fetched this session) |
| Same paper: S1 Data (s015) and supplements s014, s016 | full-text of files; Fig 4C per-fish values absent |
| Danos N, Lauder GV 2012, *J Exp Biol* 215:1854–1862 | could-not-access (host not allowed in this session) |
| Chang B et al. 2019, *J R Soc Interface* (PMC6451394) | could-not-access (empty Europe PMC record); one point via search-summary |
| Soares D, Bierman HS 2013, *PLoS ONE* 8:e61617 | not re-read; values relayed via S20-D-D |
| Small-fish leap figures (guppy, archerfish, *T. microlepis*, hatchetfish) | search-summary |

```swarm-challenge
{"claim_id": 143, "outcome": "survived", "reason": "Demesmay et al. 2025 full text independently confirms 157 +/- 27 cm/s as mean +/- SD (Fig 4C legend), the deficits reproduce (x1.995 mean, x1.484 at +2 SD, 5.8 SD to 3.13 m/s), and every proxy bias found either strengthens the out-of-reach verdict or is far smaller than the x2 gap; only cosmetic defects (45-deg apex column computed as v^2/2g, strain understated) were found outside the claim sentence.",
  "corrected_value": null,
  "depends_on": ["Demesmay et al. 2025 PLoS Biol 23:e3003484 control escape maximal speed 157 +/- 27 cm/s and mutant 161 +/- 33 cm/s (measured, author claim, full-text re-fetched)", "Demesmay et al. 2025 Fig 4C legend: values are mean +/- SD, n >= 11 per genotype (author claim, full-text)", "Demesmay et al. 2025 distance in first 40 ms 3.8 +/- 0.8 cm (measured, author claim)", "Demesmay et al. 2025 method: 240 fps phone camera, Fiji manual tracking, dropped-object stimulus; tracked point and view axis unstated", "S1 Data s015 contains only Fig S1 resting potentials (checked this session); per-fish Fig 4C maximum unknown", "assumption: surface exit speed ~= in-water escape peak, possibly x1.22 in air (Soares & Bierman 2013 via S20-D-D, not re-read)", "assumption: normal tail for SD extrapolation", "law: drag-free ballistic range R = v^2 sin(2a)/g; air drag at 3.13 m/s ~2% of g under assumed 0.4 g, 0.25 cm^2, Cd 0.5", "S20 framing: a 1 m 45-deg launch is the threshold that matters", "Danos & Lauder 2012 Re 27800, TL 33 mm, nu 1e-6 (via S20-D); Table 1 could-not-access", "negative search: no second adult D. rerio peak speed and no small-fish leap >= ~15 BL found (scope: 2 web queries, search-summary; hatchetfish literature unread)"]}
```
