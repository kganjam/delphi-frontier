# S20-D-D: Deepening S20-D (ecology) by attacking its weakest input

Parent: `docs/research/fish/S20-deepen.md` (S20-D, branch `origin/claude/deepen-s20-zebrafish-flight-9smifx`).
Grandparent: `docs/research/fish/S20-ecology.md` (S20, branch `origin/claude/zebrafish-flight-ecology-z4f08c`).
Arithmetic: `docs/research/fish/S20-D-deepen_calc.py`. Run it from the repository root.
Any number below that is not attributed to a source is a **calculation** from that script, not an
observation. Date: 2026-11-04.

**What S20-D said.** S20-D found that S20's conclusion is most sensitive to adult exit speed v. It
replaced S20's back-solved 3.13 m/s with 0.84 m/s, a speed it inverted from the Reynolds number
reported by Danos & Lauder (2012). From that it concluded:

1. the reachable aerial phase is about 7 cm;
2. the 1 m launch S20 had priced is out of reach "by at least 2.1× in speed, even against a
   guppy-class jumper";
3. this **strengthens** "flight would not pay a zebrafish".

---

## 1. Which input is S20-D most sensitive to? (recomputed)

S20-D's conclusion has two load-bearing numbers. I set each to ×0.5 and ×2 (script, section 1).

| Input (×0.5 / ×1 / ×2) | Exit speed v (m/s) | 45° range (cm) | Speed deficit for a 1 m launch |
|---|---|---|---|
| Burst speed inverted from Danos & Lauder (0.842 m/s) | 0.42 / 0.84 / 1.68 | 1.8 / 7.2 / 28.9 | ×7.4 / ×3.7 / ×1.9 |
| S20-D "guppy-class" comparator (1.51 m/s) | 0.76 / 1.51 / 3.02 | 5.8 / 23.2 / 93.0 | ×4.2 / ×2.1 / **×1.04** |

The inputs to the burst number (reported Re, the 33 mm length, the assumed ν) each enter
U = Re·ν/L linearly. A ×2 error in any one of them doubles v. That still leaves a 1.9× gap, so on
its own the burst number cannot flip the 1 m conclusion. It would need to be ×3.7.

The input that **does** flip at ×2 is the guppy-class comparator. That number is what turned
S20-D's claim from "the typical burst is too slow" into "**even the optimistic case** is too
slow". It is what licensed the words "at least 2.1×". If it doubles, the gap closes to 1.04×, and
a guppy-class *Danio* could cover roughly 0.9 m. So the single input S20-D is most sensitive to
is the **comparator speed for a small fish that is specialised for jumping out of water: 1.51 m/s**.

A ×2 error in the burst inversion would also move the hop from 2.2 TL to 8.8 TL. That weakens
S20-D's separate inference that the hop is "too short to break pursuit". But that inference was
never quantified against any predator, so it cannot "flip" in a calculable sense.

## 2. How well was that input established in S20-D?

**It was a proxy, built from a relayed number by an unstated assumption.**

- S20-D took "a small fish like the Trinidadian guppy can jump around 3.5 body lengths" from
  Chang et al. 2019. That is a review sentence citing Soares & Bierman 2013; I re-read it this
  session (`full-text`, through an automated fetch-and-summarise tool, quotes relayed).
- S20-D then multiplied 3.5 by the *zebrafish* length (33 mm) to get H = 11.6 cm, and solved
  v = √(2gH) = 1.51 m/s.
- That step assumes jump height in body lengths does not change with size. Chang et al. 2019
  report the opposite: H/L ∼ L^−1/3, with a fitted exponent of −0.35 ± 0.12 (author claim,
  read-level as above).
- S20-D never went to the primary guppy paper. That paper reports **measured** exit speeds, so
  there was no need to back-solve a speed from height.

Evidence level of 1.51 m/s in S20-D: `derived` from a `relayed` review sentence plus an
`assumed` size-invariance. It was **not a measurement**, although S20-D's table presents it
alongside measured lines.

## 3. Improving it

### 3.1 Access record (this session)

| Source / host | Result | Read-level |
|---|---|---|
| Soares D, Bierman HS 2013, *PLoS ONE* 8(4):e61617, doi:10.1371/journal.pone.0061617 (PMC3629028) | Reached | full-text (automated fetch-and-summarise; quotes relayed) |
| Chang B et al. 2019, *J R Soc Interface* 16:20190014 (PMC6451394) | Reached. Supplementary Table S1 (species list) not reached | full-text (same caveat) |
| Danos N, Lauder GV 2012, *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957: Europe PMC REST | Reached. Not open access, no PMC id | abstract |
| Same paper, journals.biologists.com, article id 10837 | WebFetch reached it. Re = 27,800 ± 2,140 s.e.m. and TL = 33.0 ± 1.3 mm re-confirmed. No temperature or Re formula in the text. **Table 1 and Fig. 3 are images, and the rest of the body is behind a paywall**, so no velocity value could be read. Plain `curl` returned HTTP 403 | full-text (partial); Table 1 `could-not-access` |
| Ravel et al. 2025, *iScience* 28:112056 (PMC11930232) | Reached. **Larvae** at 5 dpf, so not usable for adults | full-text (first 100k chars) |
| Web searches: (a) adult zebrafish jumping out of water, height/velocity; (b) adult zebrafish C-start peak velocity; (c) adult *D. rerio* escape "maximum velocity" (extended mode); (d) zebrafish tank-jump height | **No measured adult *D. rerio* exit speed, leap height or burst speed in m/s was found.** Scope: these four queries, first-page results, plus S20's ~12 and S20-D's 2 searches. | search-summary |

### 3.2 The real quantity: a measured exit speed for a small jumper

Soares & Bierman 2013 filmed guppy jumps at 1000 fps. They recorded 20 jumps by 5 males in one
set-up and 22 jumps by 4 fish in a second. Author claims, as relayed:

- standard length **1.85 ± 0.35 cm**;
- jump height **6.54 ± 1.92 cm (3.52 ± 0.96 body lengths)**;
- maximum velocity in water, "right before or at the moment" of exit, **102.36 ± 33.75 cm/s**;
- peak velocity in air **123.57 ± 30.0 cm/s**;
- the fastest single values, from the Fig. 2 caption, were **128 cm/s in water** and **150 cm/s in air**.

Disagreements inside the source, preserved:

- The Discussion gives 100.16 ± 33.9 cm/s for the in-water peak, against 102.36 in Results and
  Table 1.
- Table 1 reportedly lists body weight as "98±10 g". That cannot be right for a 1.85 cm fish, and
  it is either a relay error or a typo in the paper. **I do not use it.**

**Consistency check (calculated).** v = √(2gH) for H = 6.54 cm gives 1.13 m/s. That lies between
the measured water and air means, so the paper's heights and speeds agree with each other.

**What S20-D got wrong (calculated).** The guppy's 3.5 BL is per **18.5 mm** of standard length,
not per 33 mm. Rebuilding S20-D's comparator three ways:

| Route | v (m/s) | 45° range | 1 m speed deficit |
|---|---|---|---|
| S20-D: 3.5 BL × 33 mm, size-invariant (superseded) | 1.51 | 23 cm | ×2.07 |
| Guppy measured, in water (mean) | 1.02 | 10.6 cm | ×3.07 |
| Guppy measured, in air (mean) | 1.24 | 15.7 cm | ×2.53 |
| Guppy mean height scaled to a 33 mm fish by Chang's H/L ∼ L^−1/3 (v ∼ L^1/3) | **1.37** | **19 cm** | **×2.28** |
| Same, with an *assumed* SL of 27 mm for the zebrafish (no sourced SL/TL ratio) | 1.28 | 17 cm | ×2.45 |
| Fastest single guppy jump (air, 1.50), Chang-scaled to 33 mm | 1.82 | 34 cm | ×1.72 |

The improved central comparator is **1.37 m/s** (band 1.02–1.37 across routes). It is lower than
S20-D's 1.51 m/s. The extreme single-jump route, which S20-D did not consider, is higher, at 1.82.
Both are kept rather than averaged: the first describes a typical specialised jumper, the second
an outlier.

### 3.3 A disagreement this uncovers (my inference)

- **The measured guppy exit speed is about 55 SL/s.** The *Danio* burst inverted from Danos &
  Lauder is 25.5 TL/s.
- S20-D inferred that a submerged C-start peak is "probably an upper bound" on exit speed,
  because the interface should cost speed.
- In the only measured small-fish case, speed in air is *higher* than in water (1.24 vs 1.02 m/s,
  author claim). My reading is that the tail is probably still pushing as the body leaves the
  water. That reading is unmeasured.
- So the one primary measurement available **does not support** S20-D's upper-bound inference.
  Either jumping specialists exit faster than horizontal C-start peaks, or the Danos & Lauder
  inversion understates burst speed. One possible cause is a ν mismatch; S20-D also noted that
  which stage the peak comes from is not stated, and the fetched text does not settle it.
- I cannot tell these apart without Danos & Lauder Table 1. It could not be accessed this session.

## 4. Recomputing S20-D with the improved input

All calculations use S20's m = 0.4 g, η = 0.10 and SMR of 15–37 J/day.

- **The 1 m launch remains out of reach.**
  - Against the improved typical-jumper comparator (1.37 m/s), the speed deficit is **×2.28**,
    which is ×5.2 in kinetic energy. S20-D's figure was ×2.07.
  - Against the *Danio*-specific burst inversion it is still ×3.7.
  - Against the single fastest guppy jump scaled up by size, it is ×1.72.
  - **No line of evidence reaches 3.13 m/s.**
- **"At least 2.1×" does not survive as written.**
  - At the mean, the margin is a little larger (2.3×).
  - On an extreme single jump, the floor is **1.7×**.
  - The defensible statement is "1.7× to 3.7× short in speed (3× to 14× in kinetic energy) across
    every line of evidence, including a scaled-up best single jump of a specialist".
- **Reachable aerial phase.**
  - If *Danio* jumps like a typical guppy, a 45° trajectory spans about **11–19 cm (3–6 TL)**
    with a 5–10 cm vertical apex. S20-D said 7 cm (2.2 TL).
  - The calculated M8 stranded-jump minimum (10 cm, 0.99 m/s) sits inside that band.
  - S20-D's "hop of about two body lengths" is therefore probably an **underestimate by about
    2×** (my inference). It holds only if *Danio* does not jump better than its horizontal C-start.
- **Cost.** At most 4.4×10⁻⁴ of daily SMR per launch, even for the extreme jump. The "almost free"
  sub-claim **stands**.
- **Gliding.** At 1.37 m/s, S = 2mg/(ρ C_L v²) is about 35 cm² at C_L = 1. That is still about 10×
  a 4 cm body's planform, using S20-D's ~3 cm² planform figure, which I did not re-derive. Gliding
  stays infeasible.

**Verdict on S20-D: STANDS.**

- The headline holds: the launch is cheap, the 1 m / flight-scale escape is out of reach, and
  flight would not pay.
- The weakest input has been replaced with a primary measurement. The typical margin barely
  moves, from 2.1× to 2.3×.
- The quantitative wording changes. "At least 2.1×" becomes a floor of 1.7×. "About 7 cm"
  becomes 7–19 cm, depending on whether *Danio* jumps like a C-starter or like a guppy.
- The benefit-side argument ("too short to break pursuit") rests on a hop that may be 2–3× longer
  than S20-D stated. It remains an unquantified inference, as before. Predator strike distances
  against *Danio* remain `unknown`.

## 5. What would settle it, and what it would cost

1. **Read Danos & Lauder 2012 Table 1 / Fig. 3.**
   - This replaces the Re inversion with the authors' own peak COM velocity and says which stage
     it comes from.
   - It needs institutional access or an allowed host (sites.harvard.edu, cob.silverchair.com).
   - Cost: zero once access exists.
2. **Measure adult *D. rerio* surface exits directly**, using the Soares & Bierman protocol:
   - side-view at 1000 fps at the surface;
   - spontaneous jumps, plus jumps evoked by a looming stimulus from below;
   - about 5–10 adults, about 5–10 jumps each;
   - record v in water at exit, v in air, height and angle.
   - My unsourced estimate: about 1–2 person-weeks in a facility that has a high-speed camera.
   - **What would flip S20 and S20-D:** a measured adult exit speed ≥ 3 m/s. **What would materially
     revise S20-D:** an exit speed ≥ 1.2 m/s. That would confirm the hop is about 15 cm or more,
     not 7 cm.
3. **Chang et al. 2019 Supplementary Table S1.** Whether any cyprinid or *Danio* is in the
   100-jump dataset is `unknown`. The main text does not mention zebrafish or *Danio*.

## 6. What this does not establish

- It does not measure *Danio* exit speed. Every *Danio* number here is either a calculation from a
  reported Re or a cross-species scaling.
- The L^1/3 scaling is a cross-taxon fit with r² = 0.57. Applying it from an 18.5 mm guppy to a
  33 mm zebrafish is my extrapolation.
- It does not address juveniles, larvae, the dispersal-hop benefit between pools, or
  surface-taxiing (challenge-24). These are all left open, as in S20 and S20-D.

### Sources

| Source | Read-level |
|---|---|
| S20-deepen.md, S20-deepen_calc.py (S20-D); S20-ecology.md (S20); replicate-21.md (repository notes) | full-text (repository) |
| Soares D, Bierman HS 2013, *PLoS ONE* 8:e61617, doi:10.1371/journal.pone.0061617 | full-text (automated fetch-and-summarise, quotes relayed) |
| Chang B, Myeong J, Virot E, Clanet C, Kim HY, Jung S 2019, *J R Soc Interface* 16:20190014, doi:10.1098/rsif.2019.0014 | full-text (same caveat); supplementary S1 could-not-access |
| Danos N, Lauder GV 2012, *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957 | abstract (Europe PMC) + partial full-text (publisher HTML via fetch tool); Table 1 / Fig. 3 could-not-access |
| Ravel G et al. 2025, *iScience* 28:112056, PMC11930232 | full-text (partial). Larval study, excluded |
| Palstra AP et al. 2010 (Ucrit 0.548 m/s) | search-summary (via challenge-2 / S20-D), not re-read |
| SICB stranded-*Danio* abstract (M8) | search-summary (via S20), not re-read |

```swarm-result
{"subproblem": "S20-D-D", "evidence": "derived", "answer": "S20-D's most flip-prone input was its 'guppy-class' comparator (1.51 m/s, from a review's 3.5 BL multiplied by the 33 mm zebrafish length under an unstated size-invariance); rebuilt from the primary guppy measurements (Soares & Bierman 2013: exit 1.02 m/s in water, 1.24 m/s in air at 18.5 mm SL) and Chang et al. 2019's H/L ~ L^-1/3 scaling, it becomes 1.37 m/s (calculated; 1.82 m/s for the single fastest jump), so the 1 m launch S20 priced remains out of reach by 1.7x-3.7x in speed and S20-D's conclusion stands, though its 'at least 2.1x' floor becomes 1.7x and its ~7 cm reachable hop may be 11-19 cm if Danio jumps like a guppy.", "key_number": "small-jumper exit-speed comparator scaled to a 33 mm fish: 1.37 m/s (route band 1.02-1.37 m/s; extreme single jump 1.82 m/s), replacing S20-D's 1.51 m/s; speed needed for a 1 m launch 3.13 m/s", "verdict": "stands", "depends_on": ["S20-D: docs/research/fish/S20-deepen.md conclusion and its burst inversion U = Re*nu/L = 0.842 m/s", "Danos & Lauder 2012 reported max Re 27,800 +/- 2,140 s.e.m. in 1 mPa s water (author claim, re-read this session)", "Danos & Lauder 2012 mean TL 33.0 +/- 1.3 mm, N = 5 (author claim)", "assumed nu = 1.0e-6 m^2/s for the Re inversion (assumption, from replicate-21)", "Soares & Bierman 2013 guppy SL 1.85 +/- 0.35 cm, jump height 6.54 +/- 1.92 cm (3.52 BL) (measured, relayed)", "Soares & Bierman 2013 guppy exit speed 102.36 +/- 33.75 cm/s in water and 123.57 +/- 30.0 cm/s in air; fastest 128 / 150 cm/s (measured, relayed; Discussion gives 100.16 for the water mean)", "Chang et al. 2019 scaling H/L ~ L^-1/3, fitted exponent -0.35 +/- 0.12, r2 = 0.57 (author claim)", "extrapolation of the Chang scaling from an 18.5 mm guppy to a 33 mm zebrafish (my inference)", "law: drag-free ballistic range R = v^2/g at 45 deg and apex v^2/(2g) (no aerodynamic drag)", "law: glide lift S = 2mg/(rho C_L v^2) with C_L = 1, rho_air = 1.2 kg/m^3 (assumption)", "S20 assumed mass m = 4e-4 kg (assumption)", "S20 assumed launch efficiency eta = 0.10 (assumption)", "S20 daily SMR 15-37 J/day from Lucas et al. 2014 allometry with ambiguous units (search-summary)", "S20 framing that a ~1 m / flight-scale aerial phase is what would have to pay (S20 claim)", "Palstra et al. 2010 Ucrit 0.548 m/s (search-summary via challenge-2)", "SICB stranded-Danio jump ~0.10 m (M8, search-summary)", "predation benefit of a short hop against Danio predators: unknown (Parichy 2015 via S20)", "S20-D adult body planform ~3 cm^2 for a 4 cm fish (not re-derived)", "negative search: no measured adult D. rerio exit speed or leap height found (scope: 4 web queries this session plus S20 and S20-D searches)"]}
```
