# S32-D-D: Deepening S32-D by attacking its most sensitive remaining input, the body drag coefficient

**Parents:**
- S32 (`origin/claude/s32-multi-stroke-launch-qpq9g2`, `S32-organism.md` + `S32_taxi.py`). Read in full.
- S32-D (`origin/claude/deepen-s32-multi-stroke-launch-d1g2ra`, `S32-deepen.md` + `S32-deepen_calc.py`). Read in full.

Both scripts are copied onto this branch unchanged, so the new script can import S32-D's force model.

**Status:** derived. Every number in §1, §3 and §4 is **calculated** by `python3 docs/research/fish/S32-D-deepen_calc.py` (about 4 s). That script imports S32-D's force model unchanged, and its §0 reproduces S32's 2.88 / 2.19 m/s and S32-D's thresholds of 1.94 / 2.36 m/s exactly.

**No number in this document is a new measurement.** The drag coefficients come from other authors' measurements, read at the levels stated beside them.

## 0. Short answer

**What S32-D's conclusion is.** S32-D turned S32's negative into a threshold. The taxi reaches glide speed only if the thrust-calibration burst speed satisfies U_b ≥ 1.94 m/s (GENEROUS) or 2.36 m/s (CENTRAL). S32-D found no measurement that reaches this at mean values, and concluded that the negative holds at every mean input.

**1. The most sensitive input.** S32-D already attacked U_b. The input that moves the threshold most is the **body drag coefficient used in the thrust calibration, Cd_b**. S32 calls it "assumed (S29)", at 0.1 / 0.2 / 0.3 on 24 mm² of frontal area.
- U_b and Cd_b enter only through the calibration drag ½ρ·Cd_b·A·U_b². So the threshold scales as Cd_b^(−½).
- **Recomputed:** doubling Cd_b moves the threshold from 1.94 to **1.46 m/s** (GENEROUS) and from 2.36 to 1.81 m/s (CENTRAL).
- Both new values are below Demesmay et al. 2025's control mean + 1 SD (1.84 m/s). The GENEROUS value is below the control mean itself (1.57 m/s).
- Frontal area moves the threshold identically, because only the product Cd_b·A enters. Body mass moves it slightly more (spread ×1.75 against ×1.70), but mass is a design choice that S32 already brackets (0.25 / 0.40 g), not an uncertain fact. Fin area and foil C_D move it slightly less (×1.64).

**2. How well established is it?** It is **an assumption that has been repeated until it reads as measured.**
- S32 cites S29 for it. S32 itself lists it under "Assumed". No measured fish drag is behind it.
- It is also the wrong kind of quantity. A rigid-body Cd stands in for the drag on a strongly bent, undulating body at a C-start peak.

**3. Improving it.** I found the primary zebrafish measurement.
- **McHenry & Lauder 2005** (*J Exp Biol* 208:2289, abstract): adult zebrafish coast with **C_inert ≈ 0.024**, measured in vivo. A search summary, which I could not verify, says this is based on wetted area.
- Converted to frontal area with a calculated wetted-to-frontal ratio of 15–20 (central 18.9), that gives **Cd_front ≈ 0.36–0.48 (central 0.45)**. That is 1.5× S32's most generous 0.3.
- A Reynolds-matched coasting value for a different species points the other way. **Tandler et al. 2019** (bluegill, abstract) measured 0.0154 ± 0.0070 at Re 41,000 ± 14,000, which gives **Cd_front ≈ 0.29 (0.13–0.45)**. That is close to S32's 0.3.
- Flat-plate friction theory gives 0.12–0.17.
- **These sources disagree. I do not average them.**
- On top of coasting drag, drag during swimming is higher. Li et al. 2021 (full text, CFD, simulated) state that undulating-body drag is "much higher in magnitude" than straight-body drag, but give no factor in the text. Search-summary values for the increase range from +20% to +60% (skin friction) up to ×3–5 (Lighthill's unconfirmed theory).

**4. Recomputed** (calculated).

At the zebrafish-measured coasting value (Cd_front 0.45), the threshold falls from 1.94 to **1.64 m/s** (GENEROUS) and from 2.36 to **1.72 m/s** (CENTRAL). At the Demesmay mean U_b (1.57 m/s) the taxi then reaches **94% / 89% of V_to**, against 77% / 60% in S32-D.

The undulation increase needed to flip the result at that mean U_b is small:
- **×1.12 (GENEROUS) or ×1.24 (CENTRAL).** Both are inside the lowest published range of +20% to +60%.
- At ×1.6, even S32's original 1.38 m/s flips the result (103% / 97% of V_to).

**Verdict: FALLS.** What falls is S32-D's specific claim that the negative holds at every mean-valued input with margin.
- **Before:** the threshold (1.94 m/s) sat above the whole measured bracket for the right quantity. The bracket was flume U_max 0.39–0.54 m/s as a lower bound, and the C-start mean 1.57 m/s as an upper bound.
- **Now:** with the only zebrafish drag measurement, the threshold is 1.35–1.64 m/s, which sits **inside** that bracket.

Negative is no longer guaranteed at mean inputs. **Feasibility is not established either:**
- On the repeated-stroke (flume) calibration, the taxi still stalls at ≤ 59% of V_to, even with Lighthill's ×5.
- The answer now depends on where the unmeasured ~1-s stroke-averaged burst speed lies inside the bracket.
- With the bluegill coefficient instead, S32-D stands essentially unchanged (threshold 1.96 m/s).

---

## 1. Step 1: which input is S32-D's conclusion most sensitive to? (recomputed)

S32-D's result is a threshold, U_b* = the U_b at which U_eq = V_to. The script (§1) multiplies each input by 0.5 and by 2, with the others held at GENEROUS or CENTRAL, and recomputes U_b*. A threshold that falls below **1.57 m/s**, the Demesmay control mean that S32-D treats as the upper-bound proxy, means the conclusion flips at a mean input.

| Input (S32 value, status) | GEN U_b* ×0.5 | GEN ×2 | CEN ×0.5 | CEN ×2 | Spread (GEN) |
|---|---|---|---|---|---|
| Base | 1.94 | | 2.36 | | |
| **Body Cd_b (0.3/0.2, ASSUMED)** | 2.49 | **1.46** | 2.97 | 1.81 | ×1.70 |
| Frontal area (24 mm², S28) | 2.48 | 1.47 | 2.95 | 1.82 | ×1.69 |
| Caudal fin area (37.8 mm², ASSUMED) | 1.50 | 2.45 | 1.93 | 2.86 | ×1.64 |
| Foil C_D (0.08, Floryan 2017) | 1.50 | 2.45 | 1.93 | 2.86 | ×1.64 |
| Body mass (0.25 g, design) | 1.47 | 2.57 | 1.77 | 3.16 | ×1.75 |
| Wing area / CL_max (S28 design) | 2.54 | 1.49–1.51 | 3.06–3.10 | 1.85–1.87 | ×1.70 |
| Lobe chord | 2.25 | 1.71 | 2.65 | 2.16 | ×1.32 |
| Immersed fraction φ; wing CD0 | ~1.94–1.99 | | 2.28–2.53 | | ≤ ×1.11 |

**Why Cd_b is the target and not mass or wing area.**
- Mass, wing area and CL_max are **design variables** of the organism (S28). S32 already reports both 0.25 g and 0.40 g. They are not uncertain facts about the world.
- Among the inputs that are facts about the world, Cd_b and frontal area tie, because only the product Cd_b·A enters. Frontal area comes from S28's geometry. Cd_b is an unsupported assumption.
- Fin area and foil C_D come next (×1.64). Fin area is also assumed; it is the natural next target (§5).

**Analytic form** (script §7, constant C_D, air drag ignored): U_max/U_b = √(1 + Cd_b·A/(S_fin·C_D)). This is 1.84 at Cd_b 0.3, 2.08 at 0.42 and 2.50 at 0.66.

## 2. Step 2: how well is Cd_b established?

| Aspect | Status |
|---|---|
| Source in S32 | "Cd 0.1–0.3 on 24 mm², from S29", listed by S32 under **Assumed** |
| Measured? | **No.** It is a chosen range. No fish drag measurement is cited in S32 or S32-D. |
| Right quantity? | **No, it is a proxy.** The calibration needs the drag on the body at the instant of peak C-start speed. The body is then bent and undulating. A rigid-body Cd at best gives a lower bound on that drag (my inference, supported qualitatively by Li et al. 2021, §3.3). |
| Area basis | Frontal (24 mm²). Most fish drag literature reports wetted-area coefficients, so the conversion factor is itself an input (§3.1). |

**Honest classification:** an assumption repeated across S29 → S32 → S32-D. S32-D swept U_b but carried Cd_b at S32's values.

## 3. Step 3: going and improving it

### 3.1 Converting area basis (calculated, assumed shape)

The body is modelled as a prolate spheroid of length 30 mm (the design SL that S32 implies) with S28's 24 mm² frontal area.
- With a circular section, S_wet = 415 mm², so **S_wet/A_front = 17.3**.
- With a 2:1 elliptic section of the same area, S_wet = 453 mm², so the ratio is **18.9**.
- I carry **15 / 18.9 / 20**.

No measured adult zebrafish wetted area was read (`unknown`). McHenry & Lauder 2006 on body shape over growth may contain one; I did not access it.

### 3.2 Coasting (passive) drag coefficients

| Source | Read-level | Value (author's) | Cd_front (my conversion) |
|---|---|---|---|
| **McHenry MJ & Lauder GV 2005**, "The mechanical scaling of coasting in zebrafish (*Danio rerio*)", *J Exp Biol* 208:2289, doi:10.1242/jeb.01642, PMID 15939771 | **abstract** (Europe PMC). Full text could-not-access: cob.silverchair.com is outside the network allowlist; journals.biologists.com returned 403. | "in vivo drag measurements showed adults to operate with a drag coefficient (Cinert approximately 0.024) that was consistent with previously published estimates." Inertial regime claimed for Re > 1000. | **0.36 / 0.45 / 0.48** |
| Same: area basis and the factor ½ | **search-summary** | A search summary says C_inert normalises drag by "water density, speed squared, and wetted area". **Whether the ½ is included is `unknown`.** If it is omitted, the conventional Cd is 0.048. | 0.72–0.96 (if no ½) |
| **Tandler T, Gellman E, De La Cruz D & Ellerby DJ 2019**, *J Fish Biol*, doi:10.1111/jfb.13906, PMID 30671967 | **abstract** | Bluegill: "0.0154 ± 0.0070 at a Reynolds number of 41,000 ± 14,000 … lower than values obtained from dead drag measurements" | **0.29** (0.13–0.45 at ±1 SD and ratio 15–20). Basis assumed wetted. |
| Laminar flat plate, 1.328·Re^−½ | theory (calculated) | 0.0065 at Re 41,400 | 0.10–0.13 |
| Turbulent flat plate, 0.074·Re^−0.2 | theory (calculated) | 0.0088 | 0.13–0.18 |

**Reading this.**
- The zebrafish-specific measurement (McHenry) is **1.5× S32's most generous value**, and 2.2× its CENTRAL value.
- The Reynolds-matched value (Tandler: Re 41k ± 14k against the design's 41,400 at 1.38 m/s) agrees with S32's GENEROUS 0.3. But it is a deep-bodied centrarchid, not a zebrafish.
- **Disagreement preserved.** These are different species, different protocols and possibly different Reynolds numbers. McHenry's adult Re is not stated in the abstract (`unknown`).
- My inference: if McHenry's adults coasted at Re ≈ 5–10k and the coefficient falls as Re^−½, the value at 41k would be about 0.010, i.e. Cd_front ≈ 0.19. But the authors claim an inertial, constant-coefficient regime above Re 1000. I report their claim as the central reading and my scaling only as a caveat.
- Tandler's abstract says coasting coefficients are **lower** than dead-drag measurements. So a dead-towed value would be higher again; I did not read one.

### 3.3 From coasting drag to drag at a C-start peak

| Source | Read-level | Claim |
|---|---|---|
| **Li G, Liu H, Müller UK, Voesenek CJ, van Leeuwen JL 2021**, *Proc R Soc B*, PMC8634626 | **full-text** (Europe PMC XML) | Author's claim, from CFD (simulated, not observed), on a 20 mm model body: undulating-fish drag coefficient "scales with Re in a similar way as other three-dimensional objects (sphere, coasting fish), but drag varies as the body undulates and is **much higher in magnitude**." **No multiplier is given in the text**; it is in Fig. 5b, which I did not digitise. |
| Ehrenstein, Marquillie & Eloy 2014, *Phil Trans R Soc A*, doi:10.1098/rsta.2013.0345 | **abstract** | The boundary-layer model shows longitudinal friction scaling with √(normal velocity), which "lends credit" to the Bone–Lighthill thinning hypothesis. **No magnitude in the abstract.** |
| Ehrenstein & Eloy 2013 (+~20% friction); Patankar group (friction increase ≤ 60%); Anderson et al. (friction only modestly above a flat plate); Lighthill 1971 (×3–5, not confirmed) | **search-summary** only. Primaries not read. | Skin-friction enhancement from +20% to +60% in later work, against ×3–5 in Lighthill's original theory. **The sources disagree.** All of them concern friction, not total drag. |

**My inference.** For a body that is bent and undulating at the moment of peak speed, drag is at least the coasting drag. This rests on Li 2021 qualitatively (CFD). How much higher is **unmeasured** for adult zebrafish. The +20–60% figures apply to the friction component only. Applying them to total drag is an upper-side assumption for the friction share and ignores the extra pressure drag of a bent body, so the sign of the error is `unknown`.

### 3.4 What measurement would settle it, and what it would cost

1. **Read McHenry & Lauder 2005 in full.** This gives the C_inert definition (the ½), the adult Re, the area basis, and whether fins are included. Cost: about zero. It needs `cob.silverchair.com` or `journals.biologists.com` allowed in the session's network settings. **This alone resolves a factor-of-two ambiguity** (Cd_front 0.45 against 0.91).
2. **Coasting deceleration of 30 mm SL adult zebrafish at 1–1.5 m/s**, filmed at ≥ 500 fps just after startle-evoked bursts. This gives Cd at the design Re. Cost: a high-speed camera and about one week.
3. **The decisive quantity is not Cd_b at all.** It is the stroke-averaged caudal thrust over a ~1-s burst (S32-D §3.3): a force transducer on a tethered fish, or PIV wake momentum. Cd_b matters only because S32 infers thrust from drag. Measuring thrust directly removes both Cd_b and U_b from the calibration. Cost: roughly 1–2 months with a µN–mN force rig.

## 4. Step 4: the conclusion recomputed

All values are calculated (script §5, §8, §9). Other inputs are at S32's GENEROUS or CENTRAL values, and V_to = 4.41 m/s (0.25 g). Columns give U_eq/V_to at U_b = 1.38 m/s (S32) and 1.57 m/s (Demesmay control mean), followed by the U_b threshold. A ratio ≥ 1.00 means the conclusion falls.

| Cd_front source | Cd_b | GEN 1.38 | GEN 1.57 | GEN U_b* | CEN 1.38 | CEN 1.57 | CEN U_b* |
|---|---|---|---|---|---|---|---|
| S32 assumed (GEN 0.3 / CEN 0.2) | 0.3 / 0.2 | 0.65 | 0.77 | 1.94 | 0.50 | 0.60 | 2.36 |
| Laminar plate (theory) | 0.12 | 0.46 | 0.54 | 2.65 | 0.39 | 0.49 | 2.79 |
| Turbulent plate (theory) | 0.17 | 0.51 | 0.60 | 2.40 | 0.45 | 0.56 | 2.52 |
| Tandler bluegill, central | 0.29 | 0.64 | 0.76 | **1.96** | 0.60 | 0.72 | 2.05 |
| **McHenry zebrafish, central** | **0.45** | 0.80 | **0.94** | **1.64** | 0.75 | 0.89 | **1.72** |
| McHenry, ratio 20 | 0.48 | 0.82 | 0.97 | 1.60 | 0.78 | 0.92 | 1.68 |
| McHenry × 1.2 (friction +20%) | 0.54 | 0.88 | **1.04** | 1.52 | 0.83 | 0.98 | 1.59 |
| McHenry × 1.6 (friction ≤ +60%) | 0.72 | **1.03** | 1.23 | 1.35 | 0.97 | 1.16 | 1.41 |
| McHenry if C_inert omits ½ | 0.91 | 1.17 | 1.40 | 1.23 | 1.11 | 1.33 | 1.28 |
| McHenry × 3 (Lighthill, unconfirmed) | 1.36 | 1.50 | 1.78 | 1.02 | 1.43 | 1.70 | 1.07 |

**Flip conditions** (script §6, §9):
- Cd_front ≥ 0.69 at U_b 1.38, or ≥ 0.50 at U_b 1.57 (GENEROUS).
- Cd_front ≥ 0.76 at U_b 1.38, or ≥ 0.56 at U_b 1.57 (CENTRAL).
- Equivalently, an undulation multiplier on McHenry's coasting value of **×1.12 (GEN) or ×1.24 (CEN)** at the Demesmay mean.

**The repeated-stroke branch is unchanged in sign** (script §8, GENEROUS, U_b = flume U_max 0.39 / 0.54 m/s):
- With McHenry's central value: U_eq/V_to ≤ 0.25, and net force at the 1.38 m/s exit is −0.96 / −0.48 mN.
- With ×1.6: ≤ 0.31.
- If the ½ is missing: ≤ 0.35.
- Even with Lighthill ×5: ≤ 0.59.
- On a repeated-stroke calibration, **no drag value in any source reaches glide speed.**

### Verdict: FALLS (scoped)

- **What falls.** S32-D stated that the negative "holds on every mean-valued input", with a threshold (1.94 m/s) above even the upper-bound proxy (1.57 m/s).
  - Using the **only zebrafish-specific drag measurement**, the threshold drops to **1.64 m/s (GEN) / 1.72 m/s (CEN)**. The margin to the Demesmay mean shrinks from 24% to 4% (GEN).
  - Any undulation increase ≥ 12% (GEN) or ≥ 24% (CEN) closes it. Li et al. 2021 (CFD) state that the increase is "much higher" than zero.
  - The threshold now lies **inside** S32-D's bracket for the right quantity: 0.39–0.54 m/s (flume, lower bound) to 1.57 ± 0.27 m/s (C-start, upper bound). It no longer lies above it.
- **What does not follow.** **Feasibility is not established.** It would need the ~1-s stroke-averaged burst speed to sit near the C-start end of the bracket, and S32-D argued that it does not (an inference it flagged as unverified). On the flume end, the taxi still fails under every drag value.
- **The parent negative is therefore downgraded** from "holds at every mean input" to **"undetermined: decided by the unmeasured ~1-s burst thrust, with the C-start-calibrated upper case now at or above glide speed"**.
- **Disagreement that would reverse this verdict:** if the bluegill coefficient (Re-matched, 0.29) is the better proxy than McHenry's zebrafish value, S32-D **stands** almost unchanged (threshold 1.96 m/s). I do not choose between them. McHenry is the same species. Tandler is the same Re, and the Re of McHenry's measurement is `unknown` to me.

## 5. What this does to the S32 chain

- S32's sensitivity table (§3.3) gave "Body Cd 0.3 → 2.88 m/s" as its most generous corner. The zebrafish-measured coasting coefficient is **above** that corner. So S32's "GENEROUS" scenario was not the generous end of the measured range.
- The headline "stalls at 50–65% of V_to" should now read **"stalls at ≤ 21% (flume calibration) to ≥ 100% (C-start calibration with zebrafish-measured drag plus ≥ 12–24% swimming increase) of V_to"**. That is a spread wide enough that the model alone no longer decides the question.
- **Next weakest input:** caudal fin area (37.8 mm², assumed, "no adult zebrafish fin area was found"). It enters as Cd_b·A/S_fin, so a smaller real fin pushes the same way as a larger Cd_b. It should be measured from a lateral image of an adult. Cost: about one hour with published images. I did not attempt it here.

## 6. Searches and their scope

- **Europe PMC REST search** (title/abstract/full-text index), queries:
  - `zebrafish AND "drag coefficient"` (43 hits; first 15 titles scanned; none an adult body drag measurement)
  - `"adult zebrafish" AND drag AND swimming AND (hydrodynamic OR CFD)` (19 hits, 15 scanned)
  - `"dead drag" AND fish` (4 hits: Tandler 2019, Godoy-Diana & Thiria 2018, Tanaka 2019, Walker & Westneat 2000)
  - `"drag augmentation" AND (swimming OR undulatory)` (3)
  - `"fast-start" AND drag AND fish AND (coefficient)` (15)
  - `zebrafish AND "caudal fin area" AND adult` (26; all regeneration or toxicology; no absolute adult fin area seen in the titles)
  - `"Bone-Lighthill" OR "boundary layer thinning" AND swimming`; `"Ehrenstein" AND "Eloy"`; title searches for McHenry & Lauder 2005 and Tandler 2019.
- **Full-text attempts:**
  - PMC8634626 (Li 2021): obtained.
  - PMC6408347 (Quicazan-Rubio 2019, poeciliid drag on 3-D-printed models): Europe PMC fullTextXML gave HTTP 500, and NCBI efetch gave front matter and abstract only. The PDF render returned 403. **Abstract only, no numbers used.**
  - PMC5832724 (Godoy-Diana & Thiria 2018 review): same outcome. Abstract only.
  - McHenry & Lauder 2005 PDF: cob.silverchair.com was a proxy 403 and not resolvable by WebFetch; journals.biologists.com returned 403; sites.harvard.edu returned 403.
  - arXiv API: redirected to export.arxiv.org, which did not resolve.
- **Web search** (standard mode, 2 queries):
  - "swimming fish drag times dead drag undulating body drag augmentation factor Lighthill measured". Results included [arXiv 1409.7263](https://arxiv.org/pdf/1409.7263), [APS DFD 2012 G15.7](https://meetings-archive.aps.org/dfd/2012/g15/7) and [Patankar lab page](https://patankar.mech.northwestern.edu/aquaticlocomotion.html). **None of these was opened; the values in §3.3 are at search-summary level.**
  - "zebrafish adult body drag coefficient frontal area coasting deceleration". This found McHenry & Lauder 2005 ([JEB](https://cob.silverchair.com/jeb/article/208/12/2289/15486/The-mechanical-scaling-of-coasting-in-zebrafish), not accessible).
- **Negative finding, within this scope:** I found no measured drag on an adult zebrafish **during** a C-start or burst, and no measured adult zebrafish wetted area. Not searched: theses, non-English literature, dead-drag tow-tank studies on cyprinids, and Fig. 5b of Li 2021 (not digitised).

## 7. Sources and read-levels

| Source | Read-level |
|---|---|
| S32-organism.md, S32_taxi.py | full-text (repository) |
| S32-deepen.md, S32-deepen_calc.py (S32-D) | full-text (repository); script imported unchanged |
| McHenry & Lauder 2005, *J Exp Biol* 208:2289 | abstract; C_inert definition at search-summary; full text could-not-access |
| Tandler et al. 2019, *J Fish Biol*, doi:10.1111/jfb.13906 | abstract |
| Li et al. 2021, *Proc R Soc B*, PMC8634626 | full-text (Europe PMC XML); Fig. 5b not digitised |
| Ehrenstein, Marquillie & Eloy 2014, *Phil Trans R Soc A*, doi:10.1098/rsta.2013.0345 | abstract |
| Ehrenstein & Eloy 2013; Anderson et al.; Patankar group; Lighthill 1971 | search-summary |
| Quicazan-Rubio et al. 2019, PMC6408347; Godoy-Diana & Thiria 2018, PMC5832724 | abstract (no numbers used) |
| Demesmay et al. 2025; Widrick et al. 2018; Miln et al. 2021 | inherited from S32-D at full-text; not re-read |
| Floryan et al. 2017; S28 wing; Fish 1990; Deng 2019 | inherited from S32 at its read-levels; not re-read |

```swarm-result
{"subproblem": "S32-D-D", "evidence": "derived (S32-D's force model imported unchanged, script docs/research/fish/S32-D-deepen_calc.py, reproduces S32 2.88/2.19 m/s and S32-D thresholds 1.94/2.36 m/s) on: McHenry & Lauder 2005 adult zebrafish in-vivo coasting C_inert ~0.024 (abstract; wetted-area basis at search-summary; factor-1/2 definition unknown); Tandler et al. 2019 bluegill coasting Cd 0.0154 +/- 0.0070 at Re 41k (abstract); Li et al. 2021 CFD undulating drag 'much higher' than straight body (full-text, simulated, no factor); skin-friction enhancement +20% to +60% vs Lighthill x3-5 (search-summary, disagreeing); wetted/frontal ratio 15-20 calculated from an assumed spheroid", "answer": "After U_b, S32-D's threshold is most sensitive to the assumed body drag coefficient Cd_b used in S32's thrust calibration (x2 moves the GENEROUS threshold 1.94 -> 1.46 m/s); replacing S32's assumed 0.1-0.3 (frontal) with the only zebrafish measurement (McHenry & Lauder 2005, C_inert ~0.024 wetted, i.e. ~0.45 frontal) lowers the threshold to 1.64 / 1.72 m/s (GEN/CEN), so a swimming-drag increase of only x1.12 / x1.24 over coasting flips the result at the Demesmay mean C-start speed, and S32-D's claim that the negative holds at every mean input falls; feasibility is not established, because the repeated-stroke (flume) calibration still stalls at <=59% of V_to under every drag value, and the Re-matched bluegill coefficient (0.29 frontal) would leave S32-D standing, a disagreement preserved, not resolved.", "key_number": "body drag coefficient on frontal area Cd_b ~0.45 (0.36-0.48; zebrafish coasting, McHenry & Lauder 2005 C_inert 0.024 x calculated wetted/frontal 15-20), vs S32's assumed 0.1-0.3 and bluegill-derived 0.29 (0.13-0.45); flips S32-D at U_b 1.57 m/s if Cd_b >= 0.50 (GEN) / 0.56 (CEN)", "verdict": "falls",
  "depends_on": ["S32-D (origin/claude/deepen-s32-multi-stroke-launch-d1g2ra) threshold U_b* 1.94/2.36 m/s and its bracket: flume U_max 0.39-0.54 m/s lower bound, Demesmay 2025 C-start 1.57 +/- 0.27 m/s upper bound", "S32-D inference: C-start peak is an upper bound and flume U_max a lower bound on ~1 s stroke-averaged burst speed (unverified)", "S32 (origin/claude/s32-multi-stroke-launch-qpq9g2) force model and GENEROUS/CENTRAL scenarios", "S32 thrust calibration: caudal thrust = body water drag at burst peak, all thrust assigned to tail (assumption)", "McHenry & Lauder 2005 J Exp Biol 208:2289 adult zebrafish coasting C_inert ~0.024 (measured, abstract)", "McHenry & Lauder 2005 C_inert basis = wetted area (search-summary) and inclusion of factor 1/2 (unknown)", "McHenry & Lauder 2005 author claim: inertial regime, constant coefficient above Re 1000 (abstract); adult Re of measurement unknown", "Tandler et al. 2019 J Fish Biol bluegill coasting Cd 0.0154 +/- 0.0070 at Re 41000 +/- 14000 (measured, abstract)", "Li et al. 2021 Proc R Soc B PMC8634626 undulating-body drag much higher than straight body (CFD, simulated, full-text, qualitative)", "skin-friction enhancement in undulation: Ehrenstein & Eloy 2013 ~+20%, Patankar group <=+60%, Lighthill 1971 x3-5 (search-summary, disagreeing)", "inference: drag at C-start peak >= coasting drag", "wetted/frontal area ratio 15-20 (calculated, prolate-spheroid body 30 mm SL, assumed shape)", "design standard length 30 mm (S32 implicit; assumed)", "S28 frontal area 24 mm2", "S28 designed wing 192 mm2, CL_max 1.07, V_to 4.41 m/s at 0.25 g (derived, unmeasured)", "Floryan et al. 2017 foil law and C_D 0.08 at Re 4780-9560 with Re^-1/2 extrapolation (via S32)", "caudal fin area 37.8 mm2 (assumed) and chord 6 mm (Wakamatsu 2019 via S24)", "immersed fraction, CLz_max 1, contact angles, wing CD0 (S32 assumptions)", "Demesmay et al. 2025 C-start 1.57 +/- 0.27 m/s (via S32-D, full-text)", "Widrick et al. 2018 flume U_max 13.0-17.9 SL/s (via S32-D)", "exit speed 1.38 m/s (S28/S32, held fixed)"]}
```
