# S1-D-D: Deepening S1-D. Attacking the burst speed it rests on

Status: desk analysis, 2026-11-04. **No experiment was run.** Tags: **[observed]** means measured
and reported by the cited authors. **[derived]** means a number computed by someone, me or a
sibling branch, from author-reported values the authors did not state themselves. **[calculated]**
means model output from `docs/research/fish/s1_d_deepen_calc.py` (run it from the repo root).
**[assumed]** means an input that was not retrieved. Every number below that has no citation
comes from that script.

## 0. What is being deepened

S1-D's answer lives on branch `claude/zebrafish-takeoff-deepen-2gwq0o`
(`docs/research/fish/S1-deepen.md`; **full-text**, read in this repo). The question it answered,
from `claude/zebrafish-launch-velocity-cmgwix:docs/research/fish/S1-launch-velocity.md` (**full-text**),
is whether a 0.4 g zebrafish can reach takeoff speed. S1-D replaced S1's sustained-speed proxy,
Plaut 2000 U_crit = 0.56 m s⁻¹, with an adult escape burst speed from **one** study, Demesmay et
al. 2025: a 1.57 ± 0.27 m s⁻¹ peak, with a lower bound of 0.95 m s⁻¹ from distance over 40 ms.
It concluded:

- **(A) Aerial takeoff: no, and the verdict STANDS.** The speed gap is about 3.6× at the central
  case (S = 2 cm², C_L = 1, v_req = 5.72 m s⁻¹).
- **(B) Ballistic exit: moves from marginal to supported.** At the 0.95 m s⁻¹ lower bound, the
  drag-free apex is 1.31 standard lengths (SL).

S1-D's key number, `key_number`, was "0.95 to 1.57 m/s". Its `depends_on` field was empty.

## 1. The most sensitive input, recomputed [calculated]

I perturbed every input by a factor of 2 at the S1-D operating point (script §1):

| Perturbation | (A) L/W, central (S = 2 cm², C_L = 1) | (A) L/W, generous (S = 4 cm², C_L = 1.5) | (B) apex at v = 0.95 m/s |
|---|---|---|---|
| baseline, v = 1.57 m/s | 0.075 | 0.226 | 1.31 SL (clears) |
| **v × 2** | 0.302 | **0.905** (almost flips) | — |
| **v ÷ 2** | 0.019 | 0.057 | **0.33 SL (flips)** |
| S × 2 or C_L × 2 | 0.151 | 0.452 | no effect |
| m ÷ 2 | 0.151 | 0.452 | no effect |
| SL × 2 | no effect | no effect | 0.66 SL (flips) |

Factor needed to flip each conclusion:

- **(A), central case:** v × 3.64, or S·C_L/m × 13.3.
- **(A), generous case:** v × 2.10, or S·C_L/m × 4.4.
- **(B):** v × 0.87. A **13 %** drop below 0.95 m s⁻¹, to 0.83 m s⁻¹, puts the apex under one body
  length.

**The answer is most sensitive to the escape speed v**, because it enters squared. Its effect on
reading (A) is twice that of S, C_L or m. Reading (B) is so finely balanced that a 13 % error in v
decides it. SL enters (B) linearly, and its ×2 range is implausible for a 0.4 g fish. That is my
assumption, not a measurement.

## 2. How well established is v? Evidence level and read-level

In S1-D, v rested on **one study**: Demesmay L. et al. 2025, *PLOS Biol* 23(11): e3003484,
doi:10.1371/journal.pbio.3003484, PMC12604801. **Read-level: full-text** (Europe PMC fullTextXML,
re-read in this session). What I re-verified as verbatim author statements **[observed]**:

- "the calculated maximal speed (157 ± 27 cm/s for controls …)"
- latency to peak speed 8 ± 4 ms
- distance covered in 40 ms: 3.8 ± 0.8 cm
- escape videos at "240 frames/s" on "a Xiaomi camera (Redmi Note 13 Pro+)"
- tracked "with Fiji software (angle tool and manual tracking plugin)"
- fish 4–12 months old, "minimum of 11 per genotype", mean ± SD

**The tracked body point is not stated in anything I read.** Scope of that negative: a regex
search of the full text for head, snout, centroid, centre/center of mass and point, near
track/speed/position. My inference, not the authors' claim: a C-start swings the head laterally,
so a head-tracked peak would exceed the centre-of-mass peak. Manual tracking with a peak taken
from about two frames is also biased upward, as S1-D already noted.

**Evidence level of v as S1-D used it: measured, single source, consumer-camera frame rate,
tracked point unspecified, per-fish data not deposited** (S1-D checked the S1 Data file). It is
the right kind of quantity, a burst speed, so it is not a proxy. But nothing independent
corroborated it, and S1-D's `depends_on` did not record that.

## 3. Improving it: a second, independent primary source

**Danos N. & Lauder G.V. 2012**, "Challenging zebrafish escape responses by increasing water
viscosity", *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957, PMID 22573764.
**Read-level: full-text via a summarising fetch** (publisher HTML, characters 0–100,000, read with
WebFetch in this session; Tables 1–2 and the figures are images and were **not** read). I quote
only what the fetch returned verbatim:

- "Video images from below (ventral view) were captured at **1000 frames s–1** using a Photron PCI
  1024 camera"
- velocity "was calculated as the linear distance traveled by the **midpoint between the pectoral
  fins**"
- "Linear velocity and acceleration were calculated by dividing displacement by the time between
  consecutive image frames." The fetch reported that no smoothing was mentioned. That is a
  negative over the portion read.
- "Fish (mean total length **33.0±1.3 mm**)"; "**Five fish** were used"
- "The mean maximum Reynolds number in 1 mPa s water was **27,800 (±2140 s.e.m.)**"

This study is better instrumented for this quantity: about 4× the frame rate, a scientific camera,
and a stated point near the centre of mass. It has fewer fish: N = 5, against at least 11.

**The paper states no speed in m s⁻¹.** The fetch found none, and sibling branch
`claude/challenge-danos-lauder-com-t2q9e3` (`challenge-22.md`, full-text) found none either. The
speed has to be **derived** by inverting Re = ρUL/μ, with ρ_water = 1000 kg m⁻³ **[assumed]** and
μ = 1 mPa s (the authors' treatment value). Script §2 gives:

- **U_max = 0.84 ± 0.065 m s⁻¹ [derived]**, on a total-length basis (25.5 TL s⁻¹). The range is
  0.81–0.88 across ±1 SD of length.
- If the authors used standard length, U_max = 1.05 m s⁻¹ [derived]. That assumes SL ≈ 0.8 TL.
- Challenge-22 reached the same 0.84 independently, which reproduces the arithmetic. My inference:
  the length basis is the main unresolved part of the derivation. The paper text I read does not
  say which length went into Re.

### 3a. The sources disagree. Kept as a disagreement, not averaged

| Source | Frame rate | Point tracked | N | Peak v (m s⁻¹) | Length-specific |
|---|---|---|---|---|---|
| Demesmay 2025 | 240 fps, phone | not stated | ≥11 | **1.57 ± 0.27 (SD) [observed]** | 44–60 BL s⁻¹ [calculated] |
| Danos & Lauder 2012 | 1000 fps | pectoral-fin midpoint | 5 | **0.84 ± 0.065 (s.e.m.) [derived]**, 1.05 on an SL basis | 25.5 TL s⁻¹ |

- The ratio between them is **1.86×** on the total-length basis, or 1.49× on the standard-length
  basis [calculated]. That is close to the ×2 that section 1 shows matters.
- **This is a direct contradiction, not just a spread.** Danos's derived *peak* (0.84 m s⁻¹) is
  below Demesmay's 40-ms *mean* (0.95 m s⁻¹), which S1-D called a robust lower bound. A peak cannot
  be below a mean of the same quantity in the same kind of fish. So at least one of these holds:
  1. the tracked points differ;
  2. Danos's Re used SL (the 1.05 m s⁻¹ reading removes the contradiction);
  3. the stimulus, temperature or fish size differed enough to matter;
  4. one measurement is biased.

  I cannot decide between these from what I read. That is my inference.
- Demesmay's 44–60 BL s⁻¹ is also above the ~38 BL s⁻¹ larval figure that S1 cited. Small animals
  usually reach higher length-specific speeds, so this points toward Demesmay reading high. That
  is an inference, and a weak one.

### 3b. Searches that found nothing, and their scope

- **No third adult-zebrafish peak escape speed was found as a number.** Searches:
  - Europe PMC: `("Danio rerio" OR zebrafish) AND adult AND ("fast-start" OR "fast start" OR
    "C-start" OR "escape response") AND (velocity OR speed) AND (kinematics OR "high-speed")`.
    240 hits; I took the top 40 by relevance and regex-scanned the open-access full texts of
    PMC11930232, PMC7750966, PMC13139440, PMC12021243 and PMC9962924 for speed units.
  - A second Europe PMC query, restricted to abstracts (14 hits; titles screened).
  - One web search.
- **Akiyama et al. 2025** (*PLOS Biol*, PMC12021243, full-text) report adult escape responses
  only as turn angles, plus U_crit.
- **McKee & McHenry 2020** (PMC7750966, full-text) give a mean escape speed of 3.7 cm s⁻¹. That
  is a mean over an evasion, not a fast-start peak, so it is not comparable.
- **Ravel et al. 2025** (PMC11930232, full-text) cite Danos & Lauder only qualitatively.
- **Miln et al. 2021**, the third candidate S1-D named, still has its values only in figures and
  on figshare. Figshare and api.figshare.com were unreachable from this session (curl status 000),
  so its value remains `unknown`. The Demesmay Zenodo deposit (zenodo.org) was also unreachable.
  sicb.org (a meeting abstract on the ontogeny of zebrafish escape) was outside the network policy.
- **Control:** the gibberish query `TITLE:"zzqxjv flying zebrafish"` returned 0 hits. Plaut 2000
  was retrieved by PMID as a positive control for the endpoint.

### 3c. What would settle it, and what it would cost

1. **Cheapest, about 1 hour:** digitise the Danos & Lauder Fig. 3I velocity bar. That needs the
   figure image, which neither this session nor challenge-22 could read, or the PDF (the Lauder
   lab site is outside the network policy). It would turn the derived 0.84/1.05 into a read value
   and settle the length-basis question.
2. **About 1 email:** ask Demesmay et al. for the per-fish Fig. 4C data and the tracked point.
3. **Definitive, a few bench days** (my estimate, not a sourced cost): weigh adult wild-type fish,
   then film them at ≥1000 fps with a calibrated scale and centre-of-mass tracking. Elicit escapes
   directed **toward the surface**, and read the water-exit speed and apex directly. Both sources
   measured horizontal escapes. Neither measured an exit, which is the quantity reading (B)
   actually needs.

## 4. Recompute with the improved input [calculated]

The improved input is **not a single number**. It is a bracket whose two ends come from sources
that contradict each other: **v_burst ∈ [0.84 (derived, Danos & Lauder), 1.57 (observed,
Demesmay)] m s⁻¹**.

| v (m s⁻¹) | L/W central | L/W generous | Shortfall to v_req, central / generous | Ballistic apex |
|---|---|---|---|---|
| 0.84 Danos, TL basis | 0.022 | 0.065 | ×6.79 / ×3.92 | 3.6 cm = **1.03 SL** |
| 1.05 Danos, SL basis | 0.034 | 0.102 | ×5.43 / ×3.14 | 5.7 cm = 1.61 SL |
| 0.95 Demesmay, 40-ms mean | 0.028 | 0.083 | ×6.02 / ×3.48 | 4.6 cm = 1.31 SL |
| 1.57 Demesmay, peak | 0.075 | 0.226 | ×3.64 / ×2.10 | 12.6 cm = 3.59 SL |
| 1.84 Demesmay, peak + 1 SD | 0.104 | 0.311 | ×3.11 / ×1.79 | 17.3 cm = 4.93 SL |

- **(A) Aerial takeoff: STANDS.** Lift stays at or below 31 % of weight across both sources and
  both lift brackets. The better-instrumented source makes the central-case gap larger, ×6.8
  against ×3.6. I do not call this "strengthens", because the worst-case end of the bracket is
  still Demesmay's value, which is unchanged. The conclusion now holds under two independent
  measurements instead of one. A flip would need, for example, the generous lift surface together
  with v ≥ 3.30 m s⁻¹, which is 2.1× the higher source.
- **(B) Ballistic exit: FALLS back from "supported" to "marginal".** Under Danos's total-length
  reading, the drag-free upper bound is **1.03 SL**, at the threshold. Drag, entrained water and a
  non-vertical exit can only lower it. S1-D's claim that 0.95 m s⁻¹ is a robust lower bound is
  contradicted by an independent source. Reading (B) should not be cited as supported until the
  section 3c measurement exists.

**Verdict on S1-D's headline conclusion (no aerial takeoff): STANDS.** It is now robust to an
unresolved 1.5–1.9× disagreement between two primary sources. S1-D's secondary conclusion, that
ballistic exit is supported, **falls** to marginal.

```swarm-result
{"subproblem": "S1-D-D", "evidence": "two independent primary measurements that disagree: Demesmay et al. 2025 peak 1.57+/-0.27 m/s observed (full-text, 240 fps phone, n>=11, tracked point unstated) vs Danos & Lauder 2012 ~0.84 m/s derived from reported Re (full-text via summarising fetch, 1000 fps, pectoral-midpoint, n=5); no third value found; lift inputs assumed; all verdict numbers calculated", "answer": "The S1-D answer is most sensitive to adult escape speed (it enters squared; a 13% drop flips the ballistic reading); a second independent source (Danos & Lauder 2012, derived 0.84 m/s) contradicts S1-D's 0.95 m/s lower bound, so the no-aerial-takeoff conclusion stands (lift <=31% of weight under both sources) while the ballistic-exit claim falls back to marginal (1.03 SL drag-free upper bound).", "key_number": "adult zebrafish peak escape speed 0.84 m/s (derived from Re 27,800, TL 33 mm; 1.05 m/s if SL basis) to 1.57 +/- 0.27 m/s (observed), sources unreconciled", "verdict": "stands",
  "depends_on": ["S1-D conclusion (claude/zebrafish-takeoff-deepen-2gwq0o docs/research/fish/S1-deepen.md)", "S1 conclusion (claude/zebrafish-launch-velocity-cmgwix docs/research/fish/S1-launch-velocity.md)", "law: takeoff-stall-speed (V_s = sqrt(2W/(rho S CL_max)), lift = weight in steady 1-g flight)", "law: lift-coefficient-lowre (CL_max at low Re; CL bracket 0.5-1.5 assumed)", "measured: Demesmay et al. 2025 doi:10.1371/journal.pbio.3003484 peak escape speed 1.57 +/- 0.27 m/s, 3.8 +/- 0.8 cm in 40 ms, 240 fps, adult controls", "measured: Danos & Lauder 2012 doi:10.1242/jeb.068957 mean max Re 27,800 +/- 2140 at 1 mPa s, TL 33.0 +/- 1.3 mm, N=5, 1000 fps, pectoral-fin midpoint", "derived: Danos & Lauder U_max = Re*mu/(rho*L) = 0.84 m/s assuming L = total length (1.05 m/s if SL = 0.8 TL) and rho_water = 1000 kg/m3, mu = 1 mPa s (challenge-22, claude/challenge-danos-lauder-com-t2q9e3)", "assumption: Danos Re velocity = maximum pectoral-midpoint velocity (approx. centre of mass)", "assumption: horizontal escape speed approximates water-exit speed (no exit measurement exists)", "premise: body mass m = 0.4 g (S1 question)", "assumption: standard length SL = 3.5 cm", "assumption: lifting area S = 1-4 cm^2 (no measured zebrafish planform/pectoral area)", "constant: rho_air = 1.20 kg/m3, g = 9.81 m/s2", "model: drag-free ballistic apex h = v^2/(2g), an upper bound ignoring drag, added mass and exit angle", "measured: Plaut 2000 doi:10.1242/jeb.203.4.813 Ucrit 0.56 m/s (baseline the sensitivity is compared against)", "negative search: no third adult zebrafish peak escape speed in Europe PMC queries listed in section 3b; Miln et al. 2021 value unknown (figshare unreachable)"]}
```
