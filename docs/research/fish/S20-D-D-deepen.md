# S20-D-D-D: Deepening S20-D-D by attacking its weakest input

Parent: `docs/research/fish/S20-D-deepen.md` (S20-D-D, branch `origin/claude/s20-d-sensitive-input-77m8c9`).
Ancestors: `S20-deepen.md` (S20-D, `origin/claude/deepen-s20-zebrafish-flight-9smifx`) and
`S20-ecology.md` (S20, `origin/claude/zebrafish-flight-ecology-z4f08c`).
Arithmetic: `docs/research/fish/S20-D-D-deepen_calc.py`. Run it from the repository root.
Any number below that is not attributed to a source is a **calculation** from that script, not an
observation. Date: 2026-11-04.

**What S20-D-D said.**

1. The "guppy-class" comparator should be rebuilt from Soares & Bierman 2013's measured guppy exit
   speeds, then scaled from an 18.5 mm guppy to a 33 mm zebrafish using Chang et al. 2019's
   H/L ∼ L^−1/3 (v ∼ L^1/3).
2. That gives about 1.37 m/s typical and 1.82 m/s extreme.
3. So the 1 m launch S20 priced (which needs 3.13 m/s) is out of reach by 1.7× to 3.7× in speed.
4. The reachable 45° hop is 11–19 cm if *Danio* jumps like a guppy.
5. Verdict on S20-D: **stands**, with a speed floor of 1.7×.

---

## 1. Which input is S20-D-D most sensitive to? (recomputed)

I set each load-bearing input to ×0.5 and ×2 (script §1). The headline under test is "1 m is out of
reach, and the floor is 1.7×".

| Input | ×0.5: speed deficit | ×2: speed deficit |
|---|---|---|
| **Extreme comparator, 1.82 m/s (one illustrated guppy jump, 1.50 m/s, × Chang factor 1.213)** | ×3.44 | **×0.86: FLIPS** |
| Typical comparator, 1.37 m/s | ×4.57 | ×1.14 (does not flip, barely) |
| Chang velocity exponent (1/3) | ×1.90 | ×1.42 |
| Target aerial distance (1 m, S20's framing) | ×1.22 | ×2.43 |
| Danos & Lauder burst inversion, 0.842 m/s | ×7.44 | ×1.86 |

Only the **extreme comparator** flips the headline at ×2. It is also the input that *sets* the 1.7×
floor. So the single input S20-D-D is most sensitive to is **the upper-tail exit speed a 33 mm
*Danio* could reach if it jumped like a guppy**, which S20-D-D put at 1.82 m/s.

That number has two parts:

- one guppy datum, 1.50 m/s;
- a cross-taxon size transfer, ×1.213.

## 2. How well was that input established in S20-D-D?

**It was a measured datum carried across species by an extrapolated scaling law.** It also used
the wrong statistic for an "extreme".

- **The 1.50 m/s figure comes from a figure caption.** Soares & Bierman 2013 give it in the Fig. 2
  caption: "** indicates the highest speed in the air (150 cm/sec)". It describes the single
  illustrated jump. It is **not** stated to be the maximum of the sample. This session I read the
  paper as `full-text` (Europe PMC XML, parsed by me, not a summarising tool), and the quote is
  confirmed there.
  - So a value read from one jump was used as if it were the bound of the distribution.
  - The paper gives in-air peak speed as **123.57 ± 30.0 cm/s (mean ± s.d.)** over the 20 jumps
    filmed laterally (5 males). The text says values are means ± s.d.
  - A 1-in-40 upper tail (mean + 2 s.d., assuming normality, which is my assumption) is
    **1.84 m/s**. That is above the 1.50 S20-D-D used. **S20-D-D's "extreme" was not extreme.**
- **The size transfer, ×1.213 from Chang et al. 2019 (H/L ∼ L^−1/3, fitted exponent −0.35 ± 0.12,
  r² = 0.57), is a fit across taxa.**
  - It spans copepods to whales. The main text lists N fish = 10 for the power fit.
  - Applying it from one guppy population to a zebrafish is extrapolation.
  - It also mixes guppy **standard** length (18.5 mm) with *Danio* **total** length (33 mm).
    S20-D-D flagged that mismatch itself.

Evidence level of the 1.82 m/s input: `derived`. It is one `measured` datum, misread as a sample
maximum, then multiplied by an `extrapolated` cross-taxon exponent.

## 3. Improving it

### 3.1 Access record (this session)

| Source | Result | Read-level |
|---|---|---|
| Soares D, Bierman HS 2013, *PLoS ONE* 8:e61617, doi:10.1371/journal.pone.0061617 (PMC3629028), Europe PMC fullTextXML | Reached. Methods, Table 1, Results, Fig. 2 caption and reference list read directly | **full-text** |
| Chang B et al. 2019, *J R Soc Interface* 16:20190014 (PMC6451394), pmc.ncbi.nlm.nih.gov HTML | Main text reached. No *Danio*, zebrafish or cyprinid appears in it. Supplementary Table S1 (species list) was not reached. royalsocietypublishing.org returned 403 (Cloudflare) | full-text (main); S1 could-not-access |
| Danos N, Lauder GV 2012, *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957 | Europe PMC: abstract only. journals.biologists.com: 403 (Cloudflare challenge). Table 1 / Fig. 3 still unread | abstract |
| Chappell M, Odell J 2004, *Physiol Biochem Zool* 77:27–38, doi:10.1086/378920 (guppy burst speed; S&B's ref. 45) | Europe PMC abstract reached, but it gives no speed values. The author PDF at biology.ucr.edu was refused by the proxy (403) | abstract; numbers could-not-access |
| Gibb AC et al. 2011, *J Exp Zool A* 315:649–653, doi:10.1002/jez.711 (*Danio* terrestrial jumps) | Europe PMC abstract: kinematics only, no speeds | abstract |
| Web search: (a) Chappell & Odell guppy burst speed in cm/s; (b) adult zebrafish jumping out of water, velocity, high-speed | No measured adult *D. rerio* exit speed, leap height or aerial velocity found. Scope: these 2 queries, first page of results, plus the 4 searches in S20-D-D, the 2 in S20-D and about 12 in S20 | search-summary |

### 3.2 The real quantity: a transfer that uses *Danio*'s own burst speed

Soares & Bierman 2013 contain a within-species number that S20-D-D did not use. I read it this
session (author claim): "The burst speed, achieved with a C-start in animals of the same species and
length, is about **70 to 80 cm/sec** (extrapolated from [45] and this study)." Ref. 45 is
Chappell & Odell 2004.

This gives a **jump-to-C-start ratio measured within one species**. It replaces the cross-species
length scaling:

> Danio exit speed ≈ (guppy jump speed ÷ guppy C-start burst) × Danio C-start burst (0.842 m/s, 0.78–0.91)

This route cancels body length, so the SL/TL mismatch drops out. It also uses the only
*Danio*-specific speed available. It rests on my **assumption** that jumping specialisation
multiplies C-start speed by the same factor in both species. That assumption is **unmeasured**:
*Danio* may not jump like a guppy at all.

Results (calculated, script §2):

| Guppy statistic (Soares & Bierman, measured) | Ratio to C-start | *Danio* estimate (m/s), low / mid / high | 45° range | 1 m speed deficit |
|---|---|---|---|---|
| In-water peak, mean 1.02 | 1.28–1.46 | 1.00 / 1.15 / 1.33 | 10–18 cm | ×2.35–×3.14 |
| **In-air peak, mean 1.24** | 1.54–1.77 | **1.20 / 1.39 / 1.61** | 15–26 cm | ×1.95–×2.60 |
| Fig. 2 single jump, air 1.50 (S20-D-D's "extreme") | 1.88–2.14 | 1.46 / 1.68 / 1.95 | 22–39 cm | ×1.61–×2.14 |
| **In-air mean + 2 s.d., 1.84 (my tail statistic)** | 2.29–2.62 | **1.79 / 2.06 / 2.39** | 33–58 cm | **×1.31–×1.75** |
| (Chang route, same tail statistic) | – | 2.23 | 51 cm | ×1.41 |

For the typical jump the two transfer routes agree: 1.39 m/s by the ratio and 1.37 m/s by Chang
scaling. **I am treating that agreement as corroboration, not as a measurement.**

At the tail the ratio route gives 2.06 m/s, with a corner of 2.39 m/s. That is above S20-D-D's
1.82 m/s.

### 3.3 Checks and disagreements, preserved

**The in-air peak is the right speed to use.**

- The authors say peak air speed occurs "at approximate ¾ to 1 body length out of the water", with
  tail beats continuing.
- The ballistic speed implied by H = 6.54 cm at the mean attack angle of 77.4° is 1.16 m/s
  (calculated). The measured mean air peak is 1.24 m/s.
- So the reported height and speeds are mutually consistent. This also explains S20-D-D's puzzle
  (air speed higher than water speed). The fish is still pushing on the water as it exits.

**Guppies jump nearly vertically.**

- Mean attack angle is 77.4° ± 24.9° (author claim).
- At 77° the horizontal range is only **0.43** of the 45° range (calculated).
- Every range above assumes *Danio* would choose 45°. That is the most generous case for the "out
  of reach" conclusion.

**Air drag is negligible.**

- At 3.13 m/s, drag is about 1.5 % of weight (calculated; frontal area 2×10⁻⁵ m² and C_d = 0.5 are
  my assumptions).
- Leaving drag out is therefore conservative and does not move any conclusion.

**Table 1 reads "Fish weight (gm) 98±10".**

- In grams this is impossible for an 18.5 mm fish. In milligrams (98 mg) it is plausible for a male
  guppy.
- That the unit is a typo is **my inference**. I use 98 mg only in the calibration check below.

**The Chang power-balance model, k·M = ½ρC_dU³S, disagrees, and I keep the disagreement.**

- The authors' constants are k = 16.9 W/kg and C_d = 0.05.
- The predicted *Danio* exit speed depends on what "projected area S" means. The paper does not
  define it further, so this is ambiguous:
  - With an assumed frontal area of 2×10⁻⁵ m², it predicts **2.38 m/s**.
  - With S20-D's ~3 cm² lateral planform, it predicts **0.97 m/s**.
- With frontal area, the same model predicts 1.92 m/s for the guppy, against 1.24 m/s measured. So
  it overpredicts the one small fish I can check by 1/0.64 ≈ 1.56×.
- Calibrated against the guppy, it gives 1.54 m/s for *Danio*.
- The uncalibrated 2.38 m/s is the highest *Danio* number any route produces. It is still below
  3.13 m/s.

**Stage ambiguity in Danos & Lauder remains open.**

- Their abstract reports viscosity effects on "maximum velocity of the center of mass … during
  stage 1".
- If 0.842 m/s is a stage-1 maximum, it may understate the full burst. Every ratio-route number
  would then rise in proportion.
- Table 1 is still unread, so this is `unknown`.

## 4. Recomputing S20-D-D with the improved input

- **The 1 m launch is still out of reach.**
  - Typical *Danio*-as-guppy exit speed is 1.39 m/s (1.20–1.61), a deficit of ×1.95–×2.60.
  - The improved upper tail is 2.06 m/s (1.79–2.39), a deficit of **×1.31–×1.75** in speed, or
    1.7–3.1× in kinetic energy.
  - The uncalibrated power model gives 2.38 m/s, a deficit of ×1.32.
  - **No route reaches 3.13 m/s.**
- **S20-D-D's floor of 1.7× falls to about 1.3×.** S20-D-D's "extreme" was a single illustrated
  jump, not a tail statistic.
- **The margin now depends on S20's choice of 1 m.**
  - A 0.5 m aerial phase needs 2.21 m/s. The most generous corner (2.39 m/s, 58 cm at 45°)
    **would** reach it.
  - The tail midpoint (2.06 m/s, 43 cm) would not.
  - So "a flight-scale escape is out of reach" holds at 1 m. At half a metre it is no longer safe at
    the upper corner. This is calculation layered on an unmeasured assumption that *Danio* jumps
    like a guppy.
- **The typical hop is corroborated.** It is 15–26 cm at 45° (6–11 cm at the guppy's own 77°),
  against S20-D-D's 11–19 cm. S20-D's 7 cm still reads as an underestimate, *if* *Danio* jumps
  like a guppy. Whether it does is `unknown`.
- **Cost:** unchanged. Every route stays below about 10⁻³ of daily SMR (S20 and S20-D; not
  re-derived here).
- **Gliding:** unchanged in kind. Even at 2.39 m/s, S = 2mg/(ρC_Lv²) ≈ 11 cm² at C_L = 1. That is
  still several times S20-D's ~3 cm² planform (calculated; planform not re-derived).

**Verdict on S20-D-D: STANDS, with a narrower margin.**

- The qualitative conclusion survives the improved input: a cheap hop is possible, a 1 m aerial
  escape is not, and so flight would not pay.
- The quantitative floor S20-D-D stated (1.7×) does not survive. The improved floor is about 1.3×.
- The conclusion is now sensitive to S20's 1 m framing, not only to exit speed.

## 5. What would settle it, and what it would cost

1. **Measure adult *D. rerio* surface exits.** This is the protocol S20-D-D proposed, with one
   change: report the per-jump distribution and its maximum, not only the mean.
   - 1000 fps side view; spontaneous jumps plus jumps evoked by a looming stimulus.
   - About 5–10 adults, each jump digitised.
   - My unsourced estimate: 1–2 person-weeks in a lab that has a high-speed camera.
   - **Flip thresholds:**
     - Any single *Danio* exit ≥ 3.13 m/s (≈ 95 TL/s) falsifies S20, S20-D, S20-D-D and this note.
     - Exits ≥ 2.2 m/s would make a 0.5 m escape physically available. That reopens the cost-benefit
       question at half a metre.
     - Exits ≤ 1.0 m/s would confirm S20-D's 7 cm hop and remove the guppy analogy altogether.
2. **Read Danos & Lauder 2012 Table 1 / Fig. 3** to fix the stage of the 0.842 m/s peak. This needs
   an allowed route to journals.biologists.com or the author PDF. Cost: zero once access exists.
3. **Read Chappell & Odell 2004** for the measured guppy burst speed behind "70–80 cm/s". This
   replaces an author extrapolation with data. It needs the proxy to allow biology.ucr.edu, or
   journal access.
4. **Chang et al. 2019 Supplementary Table S1.** Whether it contains any cyprinid is still `unknown`.

## 6. What this does not establish

- No *Danio* exit speed has been measured. Every *Danio* number here is a calculation from a
  reported Re combined with a guppy-derived ratio, or a cross-taxon scaling.
- The jump-to-C-start ratio rests on the guppy C-start of "70–80 cm/s", which the authors describe
  as *extrapolated*. Its primary source (Chappell & Odell 2004) could not be read.
- The mean + 2 s.d. tail assumes the n = 20 in-air speeds are roughly normal. The raw per-jump
  values were not available.
- Guppy jumps in the source were **spontaneous** (dispersal-like), not startle-evoked. Escape jumps
  could be faster or slower, and that is `unknown`.
- Predation benefit of any hop remains `unknown`, as in S20.

### Sources

| Source | Read-level |
|---|---|
| S20-D-deepen.md + calc (S20-D-D); S20-deepen.md (S20-D); S20-ecology.md (S20) | full-text (repository branches) |
| Soares & Bierman 2013, *PLoS ONE* 8:e61617 | full-text (Europe PMC XML, read directly) |
| Chang et al. 2019, *J R Soc Interface* 16:20190014 | full-text main text (PMC HTML); supplementary could-not-access |
| Danos & Lauder 2012, *J Exp Biol* 215:1854–1862 | abstract; Table 1 could-not-access |
| Chappell & Odell 2004, *Physiol Biochem Zool* 77:27–38 | abstract; numbers could-not-access |
| Gibb et al. 2011, *J Exp Zool A* 315:649–653 | abstract |
| Web searches listed in §3.1 | search-summary |

```swarm-result
{"subproblem": "S20-D-D-D", "evidence": "derived", "answer": "S20-D-D's flip-prone input was its 'extreme' Danio-as-guppy exit speed (1.82 m/s, built from one illustrated guppy jump read as a sample maximum and a cross-taxon L^1/3 scaling); replacing it with a within-species jump/C-start ratio from Soares & Bierman 2013 applied to Danio's own C-start burst gives a typical 1.39 m/s (1.20-1.61) and an upper tail of 2.06 m/s (1.79-2.39) (calculated, unmeasured in Danio), so a 1 m aerial escape (3.13 m/s) is still out of reach and the conclusion stands, but the speed floor falls from 1.7x to ~1.3x and a 0.5 m escape is no longer excluded at the most generous corner.", "key_number": "Danio-as-guppy exit speed, upper tail 2.06 m/s (corner band 1.79-2.39 m/s; typical 1.39 m/s, 1.20-1.61), replacing S20-D-D's 1.82 m/s; required for 1 m at 45 deg: 3.13 m/s", "verdict": "stands", "depends_on": ["S20-D-D: docs/research/fish/S20-D-deepen.md conclusion and comparator 1.37/1.82 m/s", "S20-D: Danio C-start burst 0.842 m/s (0.78-0.91) inverted as U = Re*nu/L", "Danos & Lauder 2012 max Re 27,800 +/- 2,140 s.e.m., TL 33.0 mm, N = 5 (author claim, relayed; stage of peak unknown)", "assumed nu = 1.0e-6 m^2/s for the Re inversion", "Soares & Bierman 2013 guppy in-air peak 123.57 +/- 30.0 cm/s (s.d., n = 20 lateral jumps) and in-water peak 102.36 +/- 33.75 cm/s (measured, full-text)", "Soares & Bierman 2013 Fig. 2 single jump 150 cm/s air / 128 cm/s water (measured, one jump)", "Soares & Bierman 2013 guppy C-start burst 70-80 cm/s, 'extrapolated from' Chappell & Odell 2004 (author estimate; primary numbers could-not-access)", "Soares & Bierman 2013 jump height 6.54 +/- 1.92 cm, SL 1.85 +/- 0.35 cm, attack angle 77.4 +/- 24.9 deg (measured)", "assumption: Danio jump/C-start speed ratio equals the guppy's (unmeasured)", "assumption: guppy in-air speeds approximately normal, so mean + 2 s.d. is a ~1-in-40 tail", "Chang et al. 2019 scaling H/L ~ L^-1/3, exponent -0.35 +/- 0.12, r2 = 0.57 (author claim; cross-check route)", "Chang et al. 2019 power balance k M = 1/2 rho Cd U^3 S, k = 16.9 W/kg, Cd = 0.05 (author claim; S definition ambiguous)", "assumed Danio frontal area 2e-5 m^2 and guppy frontal area 9.4e-6 m^2 (assumptions)", "inference: Soares & Bierman Table 1 'gm' weight is mg (98 mg)", "S20 assumed mass m = 4e-4 kg", "law: drag-free ballistic range R = v^2 sin(2a)/g; air drag ~1.5% of weight at 3.13 m/s (calculated, assumed Cd 0.5)", "S20 framing: 1 m aerial phase is the escape that would have to pay (target distance)", "law: glide lift S = 2mg/(rho C_L v^2), C_L = 1, rho_air = 1.2 kg/m^3", "S20-D adult planform ~3 cm^2 (not re-derived)", "S20/S20-D launch cost < ~1e-3 of daily SMR (eta = 0.10, SMR 15-37 J/day; not re-derived)", "predation benefit of a short hop: unknown (S20)", "negative search: no measured adult D. rerio exit speed or leap height (scope: 2 queries this session + 4 in S20-D-D + 2 in S20-D + ~12 in S20)"]}
```
