# Challenge 140: S20-D-D-D's ratio-route Danio exit speed (tail 2.06 m/s)

**Claim under review (S20-D-D-D, branch `origin/claude/deepen-s20-d-subproblem-b4iz3k`, commit
b147cbdc, file `docs/research/fish/S20-D-D-deepen.md`).**

> Replacing S20-D-D's 1.82 m/s with a within-species jump/C-start ratio from Soares & Bierman 2013,
> applied to Danio's own C-start burst, gives a typical 1.39 m/s (1.20–1.61) and an upper tail of
> 2.06 m/s (1.79–2.39). So a 1 m aerial escape (3.13 m/s) is still out of reach, and the conclusion
> stands. The speed floor falls from 1.7× to about 1.3×.

Recorded evidence level: `derived`.

**Verdict: WEAKENED.**
- The arithmetic is right.
- The conclusion "1 m is still out of reach" does not hold up. It depends entirely on using
  0.842 m/s (Danos & Lauder Reynolds-number inversion) as *Danio*'s C-start burst.
- The claim's own ratio route reaches 3.13 m/s once that burst is ≥ 1.19–1.37 m/s.
- A direct adult *D. rerio* measurement exceeds that threshold: Demesmay et al. 2025, 1.57 ± 0.27 m/s,
  which I read in full text. With it, the same route gives a tail of 3.84 m/s, which is above 3.13.
- The claim never mentions that measurement. A sibling S20-D-D-D on another branch does.

Arithmetic: `docs/research/fish/challenge-140_calc.py`. Every number below without a source is a
**calculation** from that script, not an observation.

---

## 1. Independent arithmetic

These are my recomputations from the stated inputs, done with my own script.
- Guppy in-air peak: 1.2357 ± 0.300 m/s.
- Guppy C-start: 0.70–0.80 m/s.
- *Danio* burst: 0.842 m/s (range 0.78–0.91).
- Required speed: v = √(gR) at 45°, no drag.

| Quantity | Claim | Mine |
|---|---|---|
| v needed, 1 m / 0.5 m | 3.13 / 2.21 | 3.132 / 2.215 |
| Typical (air mean) low / mid / high | 1.20 / 1.39 / 1.61 | 1.205 / 1.387 / 1.606 |
| Tail (mean + 2 s.d.) low / mid / high | 1.79 / 2.06 / 2.39 | 1.790 / 2.061 / 2.386 |
| 1 m deficit at the tail corner | ×1.31 | ×1.31 |
| Range at 2.39 m/s | 58 cm | 58 cm |

**The arithmetic reproduces.** I found two framing defects. Neither changes the verdict.

- **"Floor falls from 1.7× to about 1.3×" compares unlike statistics.**
  - S20-D-D's 1.7× is a *point* value: 3.13 / 1.82.
  - The claim's 1.3× is its *most generous corner*: 3.13 / 2.39.
  - Compared like for like (tail midpoint), the deficit is **×1.52**.
- **The "agreement" between the two routes, 1.39 vs 1.37 m/s, uses different guppy statistics.**
  - The Chang-scaled 1.37 m/s comes from S20-D-D's 1.13 m/s ballistic-from-height speed.
  - Scaling the *same* in-air mean of 1.2357 m/s by Chang gives **1.50 m/s**.
  - So the two routes differ by about 8%. That is still close, but the coincidence is weaker than
    stated.

## 2. The hidden assumption that carries the result: Danio's C-start burst is 0.842 m/s

In the ratio route, the *Danio* exit speed is proportional to the *Danio* burst speed. Any doubt
about the burst passes through one-for-one. The flip thresholds below are calculated (script §2).

| Ratio assumption | 1 m flips (tail) if *Danio* burst ≥ | 0.5 m flips (tail) if ≥ | Typical reaches 1 m if ≥ |
|---|---|---|---|
| Mid (guppy C-start 0.75 m/s) | **1.28 m/s** | 0.91 | 1.90 |
| Generous (0.70 m/s) | **1.19 m/s** | 0.85 | 1.77 |
| Strict (0.80 m/s) | **1.37 m/s** | 0.97 | 2.03 |

The claim's band of 0.78–0.91 m/s is ±1 s.e.m. of a Reynolds-number back-calculation. Its own
author records the stage of that peak as `unknown`, because Danos & Lauder's Table 1 was not read.
The claim treats it as the *Danio* burst without testing the burst against any direct measurement.

### 2.1 Direct adult *D. rerio* burst measurements that bear on it

**Demesmay L et al. 2025, *PLoS Biol* 23(11):e3003484, PMC12604801.**
- **Read-level: full-text.** I downloaded the Europe PMC fullTextXML this session and searched it
  myself. The quotes below are verbatim author claims.
- Result: "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants)".
- Frame rate: "240 frames/s (escape response…)".
- Fish: adults "4–12-months of age, both sex", body length "2.6 ± 0.2 cm … 3.6 ± 0.2".
- Statistics: "minimum of 11 per genotype", "mean ± SD".
- Stimulus: an object dropped from about 30 cm into 1.6 L tanks.
- Tracking: manual tracking in Fiji.
- Taken at face value, this is **×1.86** the 0.842 m/s inversion. It is above every flip threshold
  in the table.

**Miln, Ward & Seebacher 2021, *R Soc Open Sci* 8:210146** (as re-digitised in this repository's
`challenge-75.md`, branch `origin/claude/challenge-75-zebrafish-fast-start-im1x80`).
- **Read-level: listing (repository relay).** I did not re-read the paper.
- Per-fish best-of-4 maxima at 120 fps span 0.45–1.38 m/s. The fastest is one fish. Challenge 75
  places the visual centre at about 0.75–0.85 m/s.
- This *supports* 0.842 m/s as a typical value.

So the direct measurements **disagree with each other**. Two estimates (Danos & Lauder's inversion
from 1000 fps data, n = 5, and Miln's centre at 120 fps, n = 50) sit near 0.8 m/s. One (Demesmay,
240 fps manual clicks, n ≥ 11 twice over) sits near 1.6 m/s. I preserve that disagreement and do
not average it.

### 2.2 What the claim's own route gives under each input

These figures are calculated (script §3) and use the guppy tail statistic exactly as the claim
does.

| *Danio* burst input | Typical | Tail low / mid / high | Tail mid vs 3.13 |
|---|---|---|---|
| D&L inversion 0.842 (the claim) | 1.39 | 1.79 / 2.06 / 2.39 | ×1.52 short |
| Miln centre ~0.80 | 1.32 | 1.84 / 1.96 / 2.10 | ×1.60 short |
| Demesmay noise-robust floor 0.95 (3.8 cm in 40 ms, from the sibling S20-D-D-D; my inference) | 1.57 | 2.18 / 2.33 / 2.49 | ×1.35 short |
| **Demesmay control mean 1.57** | **2.59** | 3.60 / **3.84** / 4.12 | **reaches 1 m** |
| Demesmay mean − 1 s.d. 1.30 | 2.14 | 2.98 / 3.18 / 3.41 | reaches 1 m |

I left Miln's fastest fish (1.38 m/s) out of the headline. Multiplying an individual maximum by the
guppy tail ratio counts tail variation twice.

**Consequence, my inference.**
- With the Demesmay input, the claim's own method puts the *typical* *Danio*-as-guppy exit at
  2.59 m/s. That alone clears 0.5 m (2.21 m/s needed).
- With the same input, the tail clears 1 m.
- The claim's sentence "a 1 m aerial escape is still out of reach" is therefore true only on the
  0.8 m/s branch of a measured disagreement.

### 2.3 Why this is weakened, not refuted

The ratio route applied to Demesmay's number is not clearly the right calculation either.
- The guppy denominator, "about 70 to 80 cm/sec (extrapolated from [45] and this study)", is an
  author *extrapolation*. Its primary source is Chappell & Odell 2004, which no session has read.
- If *Danio* bursts really run near 1.6 m/s (about 45–60 TL/s), a guppy burst of 0.70–0.80 m/s
  (38–43 SL/s) may be underestimated in the same way. That would shrink the ratio.
- The ratio is only meaningful if numerator and denominator are measured comparably. For the
  existing inputs that is untested.
- The sibling S20-D-D-D (branch `origin/claude/deepen-s20-d-d-sensitive-input-5jvia6`, commit
  17c6d933) uses Demesmay's 1.57 m/s directly as the exit speed, without the ratio. It finds the
  1 m launch short by ×2.0 at the mean and about ×1.5 at +2 s.d.
- So the two S20-D-D-D branches disagree on method:
  - Danio's own burst taken as the exit speed: 1 m stays out of reach.
  - Danio's burst multiplied by the guppy jump/C-start ratio: 1 m is reachable at the tail.
- Which method is right is `unknown` without a measured *Danio* surface exit.

## 3. Proxy check

- **The quantity that matters** is the speed at the moment the body fully leaves the water.
- **The proxy** is the guppy in-air *peak*, which Soares & Bierman place "at approximate ¾ to 1 body
  length out of the water" with propulsion continuing (full-text).
- Speed after full release should be at or slightly below this peak. So the proxy errs toward
  feasibility, which is a conservative choice for an "out of reach" claim. This is not a defect.
- **The C-start burst** in both species is an in-water, roughly horizontal peak. It is a reasonable
  denominator only if both are measured the same way (see §2.3).

## 4. Further relaxations that do not break it

These are calculated (script §5), with the D&L input held fixed.
- **Normality tail.** The mid route needs a guppy jump of 2.79 m/s, which is mean + 5.2 s.d., to
  reach 3.13 m/s.
  - At mean + 3 s.d., the mid estimate is 2.40 m/s and the corner is 2.78.
  - At mean + 4 s.d., the corner reaches 3.17 m/s. That stacks extreme corners and is not a
    credible flip.
- **Soares & Bierman internal consistency** (full-text, read this session):
  - Table 1 gives in-air 123.57 ± 30.0 and in-water 102.36 ± 33.75 cm/s.
  - The Results text gives "100.16±33.9" for water and "123±30.0" for air.
  - The water mean is reported two ways (102.36 vs 100.16). That is immaterial here, because the
    claim uses the in-air value.
- **Spontaneous vs startle.** Guppy jumps were spontaneous ("No stimulation was necessary", full-text).
  Escape jumps could be faster. The direction is `unknown`, so this neither breaks nor supports the
  claim.

## 5. Evidence level

`derived` is honest. The claim says "(calculated, unmeasured in Danio)" in the same sentence.

One honesty gap remains. The claim's own access record (§3.1) lists the searches it ran and found
"no measured adult *D. rerio* exit speed". It does not report that the C-start input had a direct
adult measurement available that disagrees with it by 1.86×. That measurement was found by a
parallel session on the same day. This is an omission of a counter-source, not a mislabelled level.

## 6. Counter-examples and regimes

- **In-taxon counter-source.** Demesmay et al. 2025 (§2.1) is the decisive one.
- **Other taxa.** Soares & Bierman name *Carnegiella strigata* (hatchetfish) and *Pantodon
  buchholzi* as startle-driven aerial escapers (full-text, their intro). I found no exit speeds for
  them. Scope: one web search this session ("adult zebrafish fast-start escape peak velocity…",
  standard mode), plus the full texts of Soares & Bierman and Demesmay. This is not a search of the
  hatchetfish literature.

## 7. What would settle it

1. **A measured adult *D. rerio* surface exit, using the per-jump maximum** (the protocol in S20-D-D-D
   §5). This resolves both the ratio question and the burst disagreement.
2. **A second method on Demesmay-type escapes:** ≥ 500 fps, with a stated tracked point. This would
   test whether 1.57 m/s is inflated by manual click noise or by a head-point bias.
3. **Chappell & Odell 2004 primary guppy burst numbers.** These would test whether the guppy
   denominator is underestimated.

## Sources

| Source | Read-level |
|---|---|
| S20-D-D-D (b147cbdc) `S20-D-D-deepen.md` + calc | full-text (repository) |
| Sibling S20-D-D-D (17c6d933) `S20-D-D-deepen.md` | full-text (repository), first 150 lines |
| Soares & Bierman 2013, *PLoS ONE* 8:e61617, PMC3629028 (Europe PMC XML) | full-text |
| Demesmay et al. 2025, *PLoS Biol* 23(11):e3003484, PMC12604801 (Europe PMC XML) | full-text |
| Miln et al. 2021 via `challenge-75.md` | listing (repository relay; paper not re-read) |
| Danos & Lauder 2012 | could-not-access (not attempted; relayed via the claim) |
| Web search, 1 query (results: PMC8025299 = Miln 2021, larval studies) | search-summary |

```swarm-challenge
{"claim_id": 140, "outcome": "weakened", "reason": "The arithmetic reproduces exactly, but the ratio route's 1 m conclusion flips once Danio's C-start burst is >= 1.19-1.37 m/s, and a full-text adult D. rerio measurement (Demesmay et al. 2025, 1.57 +/- 0.27 m/s, n >= 11) exceeds that, giving a tail of 3.84 m/s (3.60-4.12) > 3.13 m/s with the claim's own method; the claim also compares its 2.39 m/s corner (1.31x) against S20-D-D's point value (like-for-like tail midpoint is 1.52x).", "corrected_value": "Danio-as-guppy tail exit speed unresolved: 2.06 m/s (1.79-2.39) with the 0.842 m/s Re-inversion burst vs 3.84 m/s (3.60-4.12) with the 1.57 m/s Demesmay burst; the 1 m threshold of 3.13 m/s lies between them", "depends_on": ["Soares & Bierman 2013 guppy in-air peak 123.57 +/- 30.0 cm/s, n = 20 (measured, full-text)", "Soares & Bierman 2013 guppy C-start 70-80 cm/s, author 'extrapolated from' Chappell & Odell 2004 (author estimate; primary not read)", "Danos & Lauder 2012 Re inversion 0.842 m/s (0.78-0.91), stage unknown (relayed via the claim)", "Demesmay et al. 2025 adult D. rerio escape maximal speed 157 +/- 27 cm/s controls, 161 +/- 33 mutants, 240 fps manual tracking, n >= 11 per genotype (measured, full-text)", "Miln et al. 2021 adult fast-start maxima 0.45-1.38 m/s, centre ~0.8 (figure-digitised in challenge-75; relayed)", "assumption: guppy jump/C-start ratio transfers to Danio (unmeasured, as in the claim)", "assumption: guppy in-air speeds approximately normal (as in the claim)", "law: drag-free ballistic range R = v^2 sin(2a)/g at 45 deg; S20 1 m target"]}
```
