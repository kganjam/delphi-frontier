# S20-D-D-D: Deepening S20-D-D by attacking its weakest input

Parent: `docs/research/fish/S20-D-deepen.md` (S20-D-D, branch `origin/claude/s20-d-sensitive-input-77m8c9`).
Earlier links in the chain:
- S20-D: `docs/research/fish/S20-deepen.md`, branch `origin/claude/deepen-s20-zebrafish-flight-9smifx`.
- S20: `docs/research/fish/S20-ecology.md`, via S20-D.

Arithmetic: `docs/research/fish/S20-D-D-deepen_calc.py`. Run it from the repository root.
Any number below that is not attributed to a source is a **calculation** from that script, not an
observation. The parent files are not on this branch. I read them from the branches named above.
Date: 2026-11-04.

**What S20-D-D said.**

- S20-D's "guppy-class" comparator was 1.51 m/s, derived by assuming size-invariance. S20-D-D
  replaced it with primary guppy measurements (Soares & Bierman 2013), scaled to a 33 mm fish by
  Chang et al. 2019's H/L ∼ L^−1/3.
- That gives a central exit speed of **1.37 m/s** and an extreme of **1.82 m/s**.
- The 1 m launch S20 priced needs 3.13 m/s. So S20-D-D concluded that the launch "remains out of
  reach by 1.7×–3.7× in speed". Verdict: S20-D **stands**.
- S20-D-D also flagged an unresolved disagreement:
  - The guppy exits at about 55 SL/s.
  - The *Danio* burst that S20-D inverted from Danos & Lauder's Reynolds number is 25.5 TL/s
    (0.84 m/s).
  - S20-D-D could not tell which of the two is wrong.

---

## 1. Which input is S20-D-D most sensitive to? (recomputed)

I set each speed input to ×0.5, ×1 and ×2 (script, section 1). The 1 m launch needs v ≥ 3.13 m/s
(drag-free, 45°).

| Input | ×0.5 | ×1 | ×2 |
|---|---|---|---|
| D&L Re inversion, 0.84 m/s | deficit ×7.4 | ×3.7 | ×1.86 |
| Guppy mean, Chang-scaled, 1.37 m/s (S20-D-D central) | ×4.6 | ×2.3 | ×1.14 |
| Guppy fastest single jump, Chang-scaled, 1.82 m/s (S20-D-D floor) | ×3.4 | ×1.7 | **×0.86: FLIPS** |

Other inputs, recomputed:

- **Chang exponent.** b = −0.35 ± 0.12. Even b = 0 only moves the central value to 1.51 m/s and the
  extreme to 2.00 m/s. Not a flip.
- **The 1 m target.** Halving it to 0.5 m gives v_need = 2.21 m/s. That is still above every value
  in the table at ×1.

So the input that flips at ×2 is the **adult *Danio* exit speed itself**. S20-D-D never had a
*Danio* measurement of it. Every route was one of three things:
- a Reynolds-number inversion;
- a cross-species scaling from an 18.5 mm poeciliid;
- the single fastest jump of that poeciliid.

The extreme route sets S20-D-D's 1.7× floor, and it flips under ×2. The real quantity behind all
three proxies is one number: **the peak speed an adult *D. rerio* can reach in an escape**.

## 2. How well was it established in S20-D-D?

- **Not measured in the species.** S20-D-D says this itself: "Every *Danio* number here is either
  a calculation from a reported Re or a cross-species scaling."
- **Evidence level:** `derived`. Two of its parts were `measured` in another species (guppy
  heights and speeds, read-level as S20-D-D recorded it: full-text via an automated
  fetch-and-summarise tool). The third part was an `inferred` extrapolation of a cross-taxon fit
  (r² = 0.57) over a 1.8× size step.
- **The two proxies disagreed by about 1.6×** (0.84 vs 1.37 m/s). S20-D-D kept both and did not
  resolve them.

## 3. Improving it: a direct measurement in adult *D. rerio*

### 3.1 Access record (this session)

| Source / host | Result | Read-level |
|---|---|---|
| Web search: "adult zebrafish fast-start escape peak velocity m/s high-speed video" (extended mode) | Surfaced Demesmay et al. 2025. All other hits were larval or other species | search-summary |
| Web search: "cyprinid jumping out of water exit velocity…" | Found the Morán-López & Uceda Tolosa 2017 weir study (barbel, goldfish). These are large fish, at heights of about 80–150 cm. Body-length multiples come only from secondary summaries | search-summary |
| Search: "Relative leaping abilities of native versus invasive cyprinids…" | Goldfish obstacle criterion 81.2 cm (author claim, relayed). **Not used**: the fish are 10× larger and no speeds are given | search-summary |
| Demesmay L et al. 2025, *PLoS Biol* 23(11):e3003484, doi:10.1371/journal.pbio.3003484, PMC12604801. Europe PMC `fullTextXML` | Downloaded and searched directly; quotes below are verbatim from the XML | **full-text** |
| Same paper, S1 Data (`pbio.3003484.s015.xlsx`, journals.plos.org) | Downloaded. The caption says it covers Figs "S1, 2D, 3B, 4C, S7D and S8B", but the file has **one sheet, with Fig S1 resting potentials only**. Per-fish Fig 4C speeds are absent | could-not-access (for Fig 4C values) |
| Journal of Freshwater Ecology jumping test on 10 stream species of 30–100 mm, doi:10.1080/02705060.2015.1048539 | Host www.tandfonline.com is blocked by this session's network policy. Species list and speeds `unknown` | could-not-access |
| Danos & Lauder 2012 Table 1 | Not re-attempted. S20-D-D had already recorded it as paywalled, and this session's measurement makes it less decisive | could-not-access (per S20-D-D) |

**Negative finding, with its scope.** Two searches this session found no measured adult *D. rerio*
**surface exit** speed, leap height or jump trajectory: the extended query above and the cyprinid
query. S20-D-D's four queries and S20/S20-D's roughly 14 earlier ones also found none. Every
number below is an **in-water** escape speed, not an exit speed.

### 3.2 The measurement (Demesmay et al. 2025, author claims, full-text)

- **Animals.** Adult fish, "4–12-months of age, both sex". Body length "2.6 ± 0.2 cm for
  4-month-old and 3.6 ± 0.2 for 12-month-old fish".
  - Controls are homozygous *scn4aa*+/+; *scn4ab*+/+ siblings of an ENU-mutant cross, from the
    "same laying".
  - Rearing was at 28 ± 0.5 °C. The filming temperature is not stated.
- **Method.**
  - "Videos… were recorded with a Xiaomi camera (Redmi Note 13 Pro+) at… 240 frames/s (escape
    response, 1 s long videos)."
  - "Two similar objects (1 g) placed at approximately 30 cm above the water were simultaneously
    dropped into two adjacent tanks (1.6 L)… (3 or 4 adult fish by tank)."
  - "Videos were processed with Fiji software (angle tool and manual tracking plugin)."
  - "Maximal and mean speed… were calculated for each responding fish within the 40 ms from the
    initial response."
- **Result.**
  - "The calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants)"
  - "Latency to attain maximal speed (8 ± 4 ms for controls…)"
  - "Distance covered in 40 ms… (3.8 ± 0.8 cm for controls…)"
  - The Fig 4C legend reads "mean ± SD", "minimum of 11 per genotype".
  - The mutants lack skeletal-muscle Na_V. The authors report no difference from controls. The
    mutant value is therefore a second, independent group of adults: n ≥ 11 each.

### 3.3 How far to trust 1.57 m/s (my assessment, not the authors')

**Reasons it could be biased high.**
- The speed comes from manual clicks on frames 4.17 ms apart. Differentiating clicked positions
  amplifies click error. Per-axis velocity noise would be 0.08, 0.17 or 0.34 m/s for click errors
  of 0.25, 0.5 or 1 mm. That is a calculation; the click error is `unknown`.
- Taking the maximum over about 10 noisy frames biases the peak upward.
- The tracked body point is not stated. A head point moves faster than the centre of mass during
  the C-bend.

**Reasons it could be biased low.**
- Peak latency is 8 ± 4 ms, only about 2 frames. At 240 fps a short peak is smoothed.
- A phone camera at 240 fps is a low frame rate for adult fast-starts. The least-killifish 3-D
  study used 470 fps (search-summary).

**A noise-robust floor.** 3.8 cm in 40 ms is a mean of **0.95 m/s** over a window that includes the
roughly 13 ms C-bend. So the peak must exceed 0.95 m/s, which already sits above the D&L inversion
of 0.84. Per-axis click noise is zero-mean, so the 40-ms displacement is only weakly inflated by it.
Whether "distance covered" means path length or net displacement is not stated.

**Per-body-length check.** 1.57 m/s is 44–60 TL/s across the 2.6–3.6 cm fish. The guppy measured
about 55 SL/s. These are close.

### 3.4 What it does to the disagreement S20-D-D left open

S20-D-D could not say whether "jumping specialists exit faster than horizontal C-start peaks, or
the Danos & Lauder inversion understates burst speed". The direct measurement favours the
**second** explanation.

- A horizontal *Danio* C-start peak measured in another lab is 1.57 m/s. That is **×1.86** the
  Re inversion.
- It sits at guppy-like relative speed, with no jumping specialisation needed.

**Preserved, not averaged.** The two *Danio* numbers come from different labs, frame rates,
stimuli, tracking methods and possibly temperatures. Danos & Lauder's own velocity column is still
unread. It remains possible that the Re they reported was computed from a different length or
stage than S20-D assumed. I cannot resolve that without their Table 1. As things stand, 0.84 m/s
is a back-calculation and 1.57 m/s is a direct (if coarse) measurement, so I weight the second.

## 4. Recomputing S20-D-D with the improved input

All of the following are calculations. They are drag-free, at 45°, and assume exit speed equals
the in-water peak. They use S20's m = 0.4 g, η = 0.10 and SMR of 15–37 J/day.

| Line of evidence | v (m/s) | 45° range | Apex | 1 m deficit (speed / KE) |
|---|---|---|---|---|
| D&L Re inversion (S20-D) | 0.84 | 7 cm | 3.6 cm | ×3.7 / ×14 |
| Demesmay 40-ms mean (floor on the peak) | 0.95 | 9 cm | 4.6 cm | ×3.3 / ×11 |
| S20-D-D guppy central | 1.37 | 19 cm | 9.6 cm | ×2.3 / ×5.2 |
| **Demesmay control peak, mean (measured)** | **1.57** | **25 cm (7.6 TL)** | **12.6 cm** | **×2.0 / ×4.0** |
| Demesmay mutant peak, mean (measured) | 1.61 | 26 cm | 13.2 cm | ×1.95 / ×3.8 |
| Demesmay +1 SD | 1.84 | 35 cm | 17 cm | ×1.7 / ×2.9 |
| Demesmay mean × guppy air/water ratio 1.22 (*inference*) | 1.91 | 37 cm | 19 cm | ×1.64 / ×2.7 |
| Demesmay +2 SD | 2.11 | 45 cm | 23 cm | ×1.48 / ×2.2 |
| Demesmay +2 SD × air ratio (*inference*) | 2.57 | 67 cm | 34 cm | ×1.22 / ×1.5 |
| S20 1 m launch | 3.13 | 100 cm | 50 cm | — |

**1. The 1 m launch remains out of reach.**
- The central deficit moves from S20-D-D's ×2.3 to **×2.0**. The measured value is about 15%
  above S20-D-D's central proxy.
- To reach 3.13 m/s, an individual would need to sit **5.8 SD** above the control mean. If the
  guppy-style in-air speed gain transferred to *Danio*, it would need 3.7 SD. That gain transferring
  is an unmeasured inference.
- These SD counts are a normal-tail extrapolation. The per-fish values were not available, so the
  real upper tail is `unknown`.

**2. S20-D-D's floor gets a *Danio* basis, and it moves down.**
- The guppy-extreme floor (1.82 m/s, ×1.72) now sits at about +1 SD of the measured *Danio*
  distribution (1.84). So it is a plausible individual, not an outlier.
- Honest band across the measured distribution: **×1.5 (at +2 SD) to ×2.0 (mean) in speed**, or
  ×1.2 if the in-air gain is stacked on top.
- S20-D-D's "1.7×–3.7×" should now read about **"1.5×–2.0× for measured *Danio* (3.7× only under
  the Re inversion, which the measurement contradicts)"**.

**3. The reachable aerial phase grows again.**
- At the measured mean it is about 25 cm horizontal, or about 12.6 cm vertical apex.
- That compares with S20-D's 7 cm and S20-D-D's 11–19 cm.
- S20-D-D set a revision threshold: exit ≥ 1.2 m/s would "materially revise S20-D" (hop about
  15 cm or more). The in-water peak now exceeds that threshold. It is still not an exit speed.

**4. "Almost free" stands.** One launch costs 4.9 mJ, which is 1.3–3.3 × 10⁻⁴ of daily SMR.

**5. Gliding remains infeasible.** The required area is 26.5 cm² at C_L = 1, about 9× the
roughly 3 cm² planform. I did not re-derive the planform; it is S20-D's figure.

**Verdict on S20-D-D: STANDS.**

- The headline holds: a 1 m / flight-scale aerial phase is out of reach, and flight would not pay.
- It now rests on a measurement in the species instead of a cross-species scaling.
- The margin **narrows slightly**, from ×2.3 to ×2.0 at the mean, with a floor of about ×1.5 at
  +2 SD.
- S20-D's hop estimate (7 cm) and its "Re-inverted burst is an upper bound" inference both
  **fall**. S20-D-D had already doubted them.
- The benefit side ("is a 25–45 cm hop enough to break a predator's pursuit?") is still
  unquantified. Predator strike distances against *Danio* remain `unknown`, as in S20 and S20-D.

## 5. What would settle it, and what it would cost

1. **Ask Demesmay et al. for the per-fish Fig 4C values.** The published S1 Data omits them,
   although the caption lists them. They would replace the normal-tail SD extrapolation with the
   real maximum individual.
   - Cost: one email.
   - Flip condition: any individual at ≥ 2.6 m/s. With the inferred air gain, that would put a
     1 m launch within reach.
2. **Measure surface exits directly**, as S20-D-D proposed, using the Soares & Bierman protocol at
   ≥ 1000 fps, with a looming stimulus from below.
   - A dropped object from above, as Demesmay used, drives fish *away from* the surface. It is the
     wrong stimulus for jumps.
   - Cost: about 1–2 person-weeks with a high-speed camera. This is S20-D-D's estimate, unsourced.
   - Flip condition: any measured adult exit speed ≥ 3.13 m/s.
3. **Danos & Lauder 2012 Table 1.** This would show whether their velocity column agrees with
   1.57 m/s or with 0.84 m/s. It needs institutional access.

## 6. What this does not establish

- It measures a **horizontal, in-water** escape peak. It does not measure a surface exit. The
  mapping "exit speed ≈ in-water peak" is the assumption S20-D used. The guppy data suggest exit
  speed can exceed it (author claim, Soares & Bierman 2013, relayed).
- The control fish are ENU-line siblings, not a named wild-type strain. Their filming temperature
  is not stated.
- The ±27 cm/s spread mixes 4- and 12-month-old fish (2.6 vs 3.6 cm). It is not one size class.
- Drag, launch angle and the S20 mass assumption (0.4 g) were not revisited.

### Sources

| Source | Read-level |
|---|---|
| S20-D-D: `S20-D-deepen.md` and `S20-D-deepen_calc.py` (branch `claude/s20-d-sensitive-input-77m8c9`) | full-text (repository) |
| Demesmay L, Idoux R, Berthier C, Bernat C, Espinosa L, Jacquemond V, Brunet F, Maunier-Mercier A, Lory P, Nicole S, Allard B. 2025. *PLoS Biol* 23(11):e3003484. doi:10.1371/journal.pbio.3003484 | full-text (Europe PMC XML, read directly) |
| Same paper, S1 Data xlsx | full-text of file. **Fig 4C values absent** (could-not-access for those) |
| Soares D, Bierman HS 2013, *PLoS ONE* 8:e61617 | via S20-D-D (full-text, relayed); not re-read |
| Chang B et al. 2019, *J R Soc Interface* 16:20190014 | via S20-D-D (full-text, relayed); not re-read |
| Danos N, Lauder GV 2012, *J Exp Biol* 215:1854–1862 | via S20-D-D (abstract + partial); Table 1 could-not-access |
| Morán-López R, Uceda Tolosa O 2017, *Biol Invasions*, doi:10.1007/s10530-016-1328-6 | search-summary; not used |
| *J Freshwater Ecol* jumping test, doi:10.1080/02705060.2015.1048539 | could-not-access (host blocked) |
| Least-killifish 3-D fast-start, *J Exp Biol* 221:jeb168609 (470 fps) | search-summary; frame-rate comparison only |

```swarm-result
{"subproblem": "S20-D-D-D", "evidence": "measured", "answer": "S20-D-D's conclusion was most sensitive to adult Danio exit speed, which it had only as cross-species proxies (its 1.82 m/s guppy-extreme floor flips the 1 m conclusion at x2); a direct measurement in adult D. rerio (Demesmay et al. 2025, PLoS Biol, full-text: escape maximal speed 157 +/- 27 cm/s SD, n>=11, 240 fps manual tracking; mutant group 161 +/- 33) replaces it, giving a calculated 1 m-launch speed deficit of x2.0 at the mean and ~x1.5 at +2 SD, so the out-of-reach conclusion stands on a conspecific basis with a slightly narrower margin, while S20-D's 7 cm hop and its Re-inverted 0.84 m/s burst fall (the measurement is x1.86 that inversion).", "key_number": "adult D. rerio escape peak speed 1.57 +/- 0.27 m/s (mean +/- SD, in water, 240 fps; controls) replacing S20-D-D's proxy 1.37 m/s (central) / 1.82 m/s (extreme); speed needed for a 1 m 45-deg launch 3.13 m/s", "verdict": "stands", "depends_on": ["S20-D-D: docs/research/fish/S20-D-deepen.md conclusion (branch claude/s20-d-sensitive-input-77m8c9), including its comparators 1.37 and 1.82 m/s", "S20-D: docs/research/fish/S20-deepen.md and its Danos & Lauder Re inversion U = Re*nu/L = 0.842 m/s", "Demesmay et al. 2025 PLoS Biol 23:e3003484 control escape maximal speed 157 +/- 27 cm/s (mean +/- SD, n>=11) (measured, author claim, full-text)", "Demesmay et al. 2025 mutant escape maximal speed 161 +/- 33 cm/s (measured, author claim)", "Demesmay et al. 2025 distance in first 40 ms 3.8 +/- 0.8 cm (measured, author claim)", "Demesmay et al. 2025 body length 2.6 +/- 0.2 cm (4 mo) and 3.6 +/- 0.2 cm (12 mo) (author claim)", "Demesmay et al. 2025 method: 240 fps phone camera, Fiji manual tracking, dropped-object stimulus from above (author claim); click error and tracked body point unknown", "assumption: Demesmay 'mean +/- SD' in Fig 4C legend applies to the text values", "assumption: adult exit speed at the surface ~= in-water escape peak (inherited from S20-D; unmeasured)", "inference: guppy air/water peak ratio 1.24/1.02 = 1.22 (Soares & Bierman 2013, relayed via S20-D-D) may transfer to Danio", "assumption: normal distribution of individual peaks for SD-tail extrapolation (per-fish Fig 4C values not published in S1 Data)", "Soares & Bierman 2013 guppy exit speeds 1.02 (water) / 1.24 (air) m/s, fastest 1.50 m/s, SL 18.5 mm (measured, relayed via S20-D-D)", "Chang et al. 2019 scaling H/L ~ L^-1/3, exponent -0.35 +/- 0.12, r2 = 0.57 (author claim, via S20-D-D)", "Danos & Lauder 2012 Re 27,800 +/- 2,140 and TL 33.0 mm (author claim, via S20-D/S20-D-D); Table 1 velocity unknown", "assumed nu = 1.0e-6 m^2/s for the Re inversion (assumption, via S20-D)", "law: drag-free ballistic range R = v^2/g at 45 deg and apex v^2/(2g)", "law: glide lift S = 2mg/(rho C_L v^2) with C_L = 1, rho_air = 1.2 kg/m^3 (assumption)", "S20 assumed mass m = 4e-4 kg (assumption)", "S20 assumed launch efficiency eta = 0.10 (assumption)", "S20 daily SMR 15-37 J/day from Lucas et al. 2014 allometry with ambiguous units (search-summary)", "S20 framing that a ~1 m / flight-scale aerial phase is what would have to pay (S20 claim)", "S20-D adult body planform ~3 cm^2 (not re-derived)", "predation benefit of a 25-45 cm hop against Danio predators: unknown (Parichy 2015 via S20)", "negative search: no measured adult D. rerio surface-exit speed or leap height (scope: 2 web queries this session plus S20-D-D's 4 and S20/S20-D's ~14)"]}
```
