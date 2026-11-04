# S30-D-D — deepening S30-D by attacking the input its verdict is most sensitive to: lift below Re_air 700

**Parent:** S30-D, `docs/research/fish/S30-deepen.md` and `S30-deepen_calc.py` on branch `claude/deepen-s30-launch-budget-jb7qj4` (commit `efe54c57`). Read in full.
**Grandparent:** S30, `S30-organism.md` on `claude/s30-launch-budget-mass-k71prf` (commit `59f421da`). Read in full.
**Also read:** S2 (`claude/s2-low-reynolds-aero-acdwr7`) and S28 (`claude/s28-organism-design-5z0vjz`), the passages on CL_max, Re and wing geometry.

**Status: derived.** This document recalculates S30-D's verdict with one input replaced. **Nothing here is a measurement, by this project or by me.** The replacement value is itself a **computed** (DNS) result by other authors, and I read it off their figure by eye. Every number below is printed by `python3 docs/research/fish/S30-D-deepen_calc.py`.

## 0. Result

**Verdict: STRENGTHENS.** S30-D concluded that single-impulse spring (LaMSA) launch has **no realisable mass window** for a fish-like glider. That conclusion stands, and its weakest point is now firmer.

1. **What the verdict actually compares.** S30-D's "no window" is a comparison of two masses:
   - the crossover mass m\*, which is 0.94 mg at the centre and 14 mg at the most favourable one-side corner;
   - a **validity floor** of 37.5 mg, the mass at which the scaled S28 wing reaches Re_air = 700.
   - **Re 700 is not a physical threshold. It is the lower edge of the one dataset used,** Wakeling & Ellington 1997 (dragonfly wings, Re 700–2,400), which S2 read only at level S, secondary.
   - Below that edge, S30 and S30-D **both kept CL_max = 1.07, by extrapolation.** That is a number repeated across three documents until it reads as measured.
2. **Sensitivity, recomputed (§1).**
   - At S30-D's central case, **no single input flips the verdict at a factor of 2**. The margin floor/m\* is 40.
   - At S30-D's best one-side corner (w 21.2 J/kg, β 0.533), the margin is only **2.7**. Four inputs flip the verdict at ×2: w, η_h, f, and **CL below Re 700**. The Re floor flips it at ÷2.
   - Of these, CL below Re 700 is the only one with **no evidence at all** behind the value used. That is why I attack it.
3. **The improved input (§2).** Zhang & Taira 2020 is a DNS of finite wings at **Re = 400**: NACA 0015 section, semi-aspect-ratio 2 (AR 4, the closest to S28's AR 5). **Read level: full-text** (arXiv 2011.12336).
   - Time-averaged **CL ≈ 0.6 at α = 30°**, still rising at the edge of their range, so it is *not* a CL_max. CL ≈ 0.38–0.40 at the max-L/D angle of 16°. These are **my readings of their Fig. 3c**, not numbers printed in the text.
   - The authors state: "the lift-to-drag ratio remains below 1.5 for the cases considered herein."
   - **This is a computed value, not an observation.** It is for a 15 %-thick section, not a thin fin.
4. **Recomputed** (calculated, not observed):
   - **Central m\* = 0.17 mg (CL 0.6), or 0.046 mg (CL 0.39)**, against S30-D's 0.94 mg.
   - **Best one-side corner m\* = 4.7 mg (2.1 mg)**, against 14.0 mg.
   - The corner's margin below the floor rises from **2.7 to 7.9**. A ×2 error in w, f or η_h **no longer flips the verdict** there; it now takes ×3.0.
   - The 0.4 g zebrafish is ~**2,400×** (CL 0.6) too large for single-impulse launch at its own shape, against S30-D's 425×.
5. **Restoring a window needs CL ≥ 3.3** at every Re for the best corner, and ≥ 6.8 for the centre. The best values in this project are 1.07 measured steady (S2, level S) and ~1.75 for revolving wings with an attached leading-edge vortex (S2, level S). **Neither comes close.**
6. **A finding that cuts against S30's own number (§4).** S30's 39 mg window sat at Re 713, only just inside the data. Wakeling & Ellington's **free-glide** CL_max is 0.93, against 1.07 in the wind tunnel (search-summary; the two values are kept separate, not averaged). **At 0.93, S30's 39 mg window drops to 25.6 mg (Re 619), outside the data.** S30's headline was fragile to a disagreement inside its own source, before S30-D replaced w.
7. **A second, separate weakening below Re 700 (§6).** At L/D < 1.5 (computed, Re 400), even a fish that left the water at V_to would glide at ≥ 34° below horizontal, gaining 1.5 m of range per metre of height. S28 assumed 4–6. **Below the floor, the product of the launch is not a glide in any useful sense.**

**What I could not settle.** The best evidence would be thin-plate or real-fin lift at Re 100–700. I could not read Dickinson & Götz 1993 (2-D plate, Re ≈ 236) or Taira & Colonius 2009 (flat plates, Re 300/500); scope in §3.3. Zhang & Taira write that "airfoil shape is influential even at these low Reynolds numbers" when they compare with Taira & Colonius's flat plates. **The direction of that difference is not stated in the text I read.** So a thin fin could lift more than 0.6 at Re 400: `unknown`. §5 shows that the verdict survives even at CL = 1.07, the unimproved value.

---

## 1. Which input S30-D's verdict is most sensitive to (recomputed)

S30-D's verdict is **margin = m_floor / m\* > 1 means no window**. Here m\* = m₀·R₀^(1/β) with R₀ = f·w·η_s·η_h/need, and need ∝ WL/(ρ·CL), so **R₀ ∝ CL**. m_floor = 37.5 mg is where Re_air(m) = 700 for the isometrically scaled S28 wing.

Script §1, each input ×2 and ÷2 with everything else held at the stated case:

| Input | Central (margin 39.9) ×2 / ÷2 | Best one-side corner (margin 2.68) ×2 / ÷2 |
|---|---|---|
| w, spring-loading density (or fibre strain ε) | 4.98 / 319, holds | **0.73 FLIPS** / 9.8 |
| **CL below Re 700 (1.07, extrapolated)** | 4.98 / 319, holds | **0.73 FLIPS** / 9.8 |
| Re floor (700) | 159 / 10.0, holds | 10.7 / **0.67 FLIPS** |
| η_h (0.37) | 4.98 / 319, holds | **0.73 FLIPS** / 9.8 |
| f (0.30) | 4.98 / 319, holds | **0.73 FLIPS** / 9.8 |
| β | 2.45 / 10,579, holds | **0.63 FLIPS** / 47.7 |

**How to read this.**
- The central verdict survives every single factor-of-2 error.
- The corner verdict, the case S30-D itself said came closest, fails under a ×2 error in any R₀ factor, because m\* ∝ R₀^(1/0.533) = R₀^1.88 there.
- So the question in step 1 has no unique answer by sensitivity alone. **CL, w, f and η_h enter identically.** I choose CL below Re 700, and give my reasons, as a judgement rather than a computation:

| Input | Why it is or isn't the target |
|---|---|
| w | Already attacked by S30-D. Its remaining load-bearing assumption (C-start strain ≈ achievable strain) needs a new lab measurement; S30-D §5 specified it. Nothing more in the literature to improve it with today. |
| η_h | Already attacked by S29-D. S30-D carried it. |
| f | Physically capped at ×2, which is all skeletal muscle. |
| β | Measured allometry (Fish 1990, PROJECT-TRANSCRIBED). |
| **CL below Re 700** | **Not measured, not proxied, not derived. Extrapolated flat from the edge of a single dataset, and that dataset is held at read-level S.** It also *defines* the floor. It is the only input on the list that has never been checked against anything. |

## 2. How well is CL_max = 1.07 established, and where?

| Question | Answer |
|---|---|
| Primary source | Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543. Real wings of *Sympetrum sanguineum* and *Calopteryx splendens*, Re 700–2,400 (search-summary in this session; S2 held it at level S). I did not read the full text. |
| Value disagreement inside the source | **0.93** from free glides, the value the authors give "may not be the maximum the wings can produce", and **1.07** from the wind tunnel (search-summary, relayed by a later computational paper). S2 also relays "Sympetrum ≈ 1.05–1.07; other species ≈ 0.7–0.9". **These are kept separate.** S28 picked 1.07, the highest. |
| Range of validity | Re 700–2,400 only |
| How S30 and S30-D used it | At every mass. S30 noted that its 8.5 mg end (Re 334) was "an extrapolation". S30-D turned the data edge into a **rule**: m\* below Re 700 means "no realisable window". **Neither document used any lift value measured or computed below Re 700.** |
| Evidence level, as used below Re 700 | **Assumption, repeated.** |

**One consequence worth stating on its own.** The floor rule cuts both ways. S30-D used it to say that a window below 37.5 mg is "not realisable", meaning *unvalidated*. Unvalidated is not the same as impossible. If thin fins lifted *more* below Re 700, a window could exist there and S30-D would have been wrong to discard it. That is the real risk in this input, and it is the reason to look below the floor instead of stopping at it.

## 3. Improving it: lift below Re 700

### 3.1 What I found

**Zhang & Taira 2020**, "Aerodynamic characterization of low-aspect-ratio swept wings at Re = 400", arXiv 2011.12336. **Read level: full-text** (PDF; text extracted, figures rendered and read by eye).

| Item | Value | Kind |
|---|---|---|
| Method | "direct numerical simulations", incompressible, laminar | **computed** |
| Section | NACA 0015 (15 % thick, symmetric, no camber) | as stated |
| Reynolds number | "fixed at 400" | as stated |
| Geometry | semi-AR 0.5, 1, 2 (full AR 1, 2, 4); sweep 0–45°; α 0–30° | as stated |
| CL, sAR 2, Λ = 0, α = 30° | **≈ 0.6**, still rising | **my reading of Fig. 3c** |
| CL, sAR 2, α ≈ 16° (max L/D) | **≈ 0.38–0.40** | my reading of Fig. 3c |
| CL, sAR 0.5 and 1, α = 30° | ≈ 0.43–0.45 | my reading of Fig. 3a–b |
| Max L/D | "remains below 1.5 for the cases considered herein"; ≈ 1.4–1.5 at sAR 2 | text, and Fig. 5c |
| vs the inviscid limit | "significantly smaller than the inviscid limit for all three aspect ratios" | text |
| vs Taira & Colonius 2009 flat plates at Re 300 | "the airfoil shape is influential even at these low Reynolds numbers". **Direction not stated** in the text. | text |

**How it maps onto the S28 wing:**
- S28's case C is AR 5, so sAR 2 (AR 4) is the closest case.
- S28's fin is thin and possibly cambered. NACA 0015 is thick and symmetric.
- Laitone 1997 (abstract, via S2) found thin plates "fairly steady" with Re, while NACA 0012 degraded badly below Re 5×10⁴. That makes thick sections the **pessimistic** case.
- **My inference, not the authors' claim:** a thin cambered fin at Re 400 would plausibly lift more than 0.6. How much more is `unknown`.

### 3.2 What the improved input is and is not

- It is **one computed datum at one Re**, for a geometry that differs from the fin in the direction known to hurt lift.
- It is **not** a CL_max: the α = 30° curve is still rising.
- It is still better than the alternative. The alternative was no datum at all, with 1.07 extended from Re 700 down to Re 40–430.
- I use it as a **bracket**, CL 0.39–0.6 below Re 700. I do not use it as a point value, and I do not interpolate between it and Wakeling & Ellington. The two sources differ in shape, method (computed vs measured) and Re, and averaging them would hide that.

### 3.3 Scope of the searches, and the negatives

- **Four standard web searches:**
  - Dickinson & Götz 1993 lift at Re ~200;
  - Taira & Colonius 2009 lift at Re 300;
  - Wakeling & Ellington 1997 CL_max;
  - measured flat-plate lift at Re 100–500.
- **Could not access:**
  - **Dickinson & Götz 1993**, *J. Exp. Biol.* 174:45. journals.biologists.com returned a robot-verification page; cob.silverchair.com was blocked in S30-D. A search summary says the profile translated at 12 cm/s, Re 236 (relayed from Dickinson 1994). It also says the abstract reports an ~80 % transient lift increase from a leading-edge vortex that stayed attached for ~2 chord lengths, with "a broad lift plateau up to 54°". **No steady CL value was obtained: `unknown`.**
  - **Taira & Colonius 2009**, *J. Fluid Mech.* 623:187, and **Taira's 2008 thesis.** resolver.caltech.edu and thesis.library.caltech.edu do not resolve in this session's network policy. Cambridge gives the abstract only, via search. **CL values: `unknown`.**
- **Within that scope:** I found **no measured** steady lift coefficient for any wing or plate at Re 100–700. The only quantitative value I found is the computed Zhang & Taira one.
- **Not searched:** Web of Science or Scopus, theses other than Taira's, and non-English literature.

## 4. Recompute and verdict

### 4.1 m\* with lift below Re 700 replaced (script §2; calculated, not observed)

need ∝ 1/CL, so R₀ ∝ CL. V_to is raised by √(1.07/CL) when Re is evaluated at m\*.

| CL used below Re 700 | m\* central | Re_air at m\* | m\* best one-side corner | Re_air | zebrafish ÷ m\* (central) |
|---|---|---|---|---|---|
| 1.07 (S30/S30-D extrapolation) | 0.94 mg | 111 | 14.0 mg | 428 | 425× |
| 0.93 (W&E free glide; measured at Re ≥ 700, extrapolated) | 0.62 mg | 96 | 10.8 mg | 402 | 647× |
| **0.60 (Z&T, Re 400, α 30°; computed)** | **0.17 mg** | 62 | **4.7 mg** | 332 | **2,408×** |
| 0.39 (Z&T, Re 400, max-L/D α; computed) | 0.046 mg | 40 | 2.1 mg | 275 | 8,770× |

**Caveats on this table:**
- Every m\* lies at Re_air < 700, which is the regime where the replaced value is meant to apply.
- The central rows land at Re 40–110. That is **below even the Re 400 datum**, so CL there is `unknown` and is plausibly lower still. I have not extrapolated further down.
- **Best-corner margin:** 37.5 / 4.74 = 7.9 at CL 0.6, against 2.7 before. A flip there now needs w, f or η_h to be ×3.0 (7.9^0.533), not ×2.

### 4.2 Cases that cleared the floor in S30-D (script §3)

Only S30-D's "teleost ceiling, all muscle" rows clear the floor: 82 mg (Re 1,034) and 124 mg (Re 1,274). They lie inside the Wakeling & Ellington range, so this document does not change them.
- They still stack three optimistic choices: all skeletal muscle loading one spring, the curvature-derived carp strain, and S29's rather than S29-D's efficiency chain. S30-D said so.
- If the W&E free-glide 0.93 applies instead of 1.07, those values fall to 54 mg (×0.66) and 96 mg (×0.77). Both stay above the floor. *(This is my hand calculation, (0.93/1.07)³ at β = 1/3, and (0.93/1.07)^1.88 at β = 0.533, giving 124 → 96. The script does not print it.)*

### 4.3 S30's own number under its source's internal disagreement (script §4)

| CL | m\* (frog w 53) | Re_air | Inside the CL data? |
|---|---|---|---|
| 1.07 (wind tunnel) | 38.9 mg | 713 | yes, just |
| 0.93 (free glide) | 25.6 mg | 619 | **no** |

### 4.4 What would restore a window (script §5)

Hold a single CL at every Re and treat the floor self-consistently (a higher CL lowers V_to, and so Re). A window then opens only at:
- **CL ≥ 3.29** for the best corner, opening at 115 mg;
- **CL ≥ 6.76** for the centre, opening at 237 mg.

For comparison, the measured steady values are 0.93–1.07 (level S), and the revolving-wing LEV value is ~1.75 (S2, level S). Restoring a window needs about 2–6× more lift than any value in this project.

### 4.5 Each part of S30-D's conclusion

| S30-D claim | With the improved lift input | Status |
|---|---|---|
| The crossover is an upper bound | Unchanged. It depends on β − α. Lower CL at small Re makes small fish worse off than computed, but cannot reverse R(m) | **STANDS** |
| No realisable single-impulse window | It was robust at the centre and fragile at the corner (margin 2.7). Below Re 700 it no longer rests on "no data": the one value found is 0.39–0.6, and the corner margin becomes 7.9. A window needs CL ≥ 3.3 | **STRENGTHENS** |
| The zebrafish is ~425× too large | ~2,400× at CL 0.6 (647× at 0.93). The direction is the same and the size larger | **STRENGTHENS** (bracket widens) |
| S30's 39 mg was "the optimistic end" | It was also fragile to its own source's 0.93 vs 1.07 split (§4.3) | Confirmed, for a second reason |
| Real gliders use multi-stroke launch | Not tested here. Its weakest input is still a search-extract taxi source | carried |

### Verdict: **STRENGTHENS**

**Precise statement.** S30-D's "no realisable single-impulse window" rested on a validity floor (Re_air 700, 37.5 mg). Below it, CL_max = 1.07 had been extrapolated, with no supporting value. The one quantitative value I could reach below the floor is a **computed** DNS result at Re 400 (AR 4, NACA 0015): time-averaged CL ≈ 0.6 at α 30° and L/D < 1.5. With that bracket the single-impulse LaMSA crossover falls further:
- from 0.94 mg to **0.05–0.17 mg** at the centre;
- from 14 mg to **2.1–4.7 mg** at the most favourable one-side corner.

The corner's margin below the floor rises from 2.7× to 7.9×. Reopening a window would need a steady CL of ≥ 3.3 at all Re. **The verdict strengthens. It is qualified by the fact that a thin fin at Re 100–700 has no measured or computed lift value I could read.**

## 5. What measurement would settle it, and what it would cost

**The quantity:** steady CL(α) and L/D of a **thin, fin-like wing at AR ≈ 5** at Re_air = 100, 200, 400 and 700. Ideally the wing is a replica of a spread zebrafish pectoral fin, ray-supported membrane, in the S28 case-C planform.

**Two routes:**

1. **Measured:** a towing tank or wind tunnel with Re matched by scale and fluid.
   - Example: a 5 cm-chord plate in water–glycerol at a few cm s⁻¹, or a 6 mm-chord replica in air at 0.25–1.7 m/s on a micro-balance.
   - Sweep α from 0 to 45°. Run the S2 thin plate and a NACA 0015 as controls. The NACA 0015 must reproduce Zhang & Taira's ≈ 0.6 at Re 400, α 30°, as a positive control for the rig against the DNS.
   - **Cost, estimated and not quoted:** in a lab that already has a robotic-wing tow tank, 1–3 weeks of one person and under ~US$1,000 of materials. Without such a rig, the six-axis force sensor and traverse are a five-figure purchase.
2. **Computed (cheaper; still not an observation):** DNS of a 2–4 %-thick cambered plate at AR 5, Re 100–700, with the same solver class as Zhang & Taira.
   - About 10⁴–10⁵ core-hours, a few days on a cluster.
   - The output would be labelled **computed**.

**Decision rule**, from §1 and §4.4: in this geometry, the verdict reverses only if **CL ≥ ~3.3**. Any value at or below ~1.8 leaves "no realisable window" intact even at S30-D's best corner. **No plausible steady-wing result reverses it.** The measurement is therefore worth more to S2 and S28 than to S30. In particular it would test whether L/D < 1.5 below Re 700 turns S28's glide into a steep fall.

## 6. Sources

| # | Source | Read level | Used for |
|---|---|---|---|
| 1 | S30-D: `S30-deepen.md`, `S30-deepen_calc.py` (`claude/deepen-s30-launch-budget-jb7qj4`, efe54c57) | full-text | Formula, every baseline input, the floor rule |
| 2 | S30: `S30-organism.md` (`claude/s30-launch-budget-mass-k71prf`, 59f421da) | full-text | Origin of the extrapolated CL and the rule for "no realisable crossover" |
| 3 | S2: `S2-low-reynolds-aero.md` (`claude/s2-low-reynolds-aero-acdwr7`) | full-text (grep of CL and Re passages) | W&E 1997 at level S; 0.93–1.07; Laitone 1997 abstract; revolving-wing CL ≈ 1.75 |
| 4 | S28: `S28-organism.md` (`claude/s28-organism-design-5z0vjz`) | full-text (grep of geometry passages) | AR 5, 1-BL span, CL 1.07, L/D 4–6 assumption |
| 5 | Zhang & Taira 2020, arXiv 2011.12336 | **full-text** (text and figures; values read from figures by eye) | CL ≈ 0.6 (α 30°), 0.38–0.40 (α 16°), L/D < 1.5 at Re 400; DNS |
| 6 | Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543 | search-summary | Re 700–2,400; CL 0.93 free glide vs 1.07 wind tunnel |
| 7 | Dickinson & Götz 1993, *J. Exp. Biol.* 174:45 | could-not-access (captcha); abstract content via search-summary | Re ≈ 236 (relayed); no CL used |
| 8 | Taira & Colonius 2009, *J. Fluid Mech.* 623:187; Taira 2008 thesis | could-not-access (hosts not resolvable); listing via search | Not used numerically |

## 7. Honesty ledger

- **Measured, by others:** dragonfly-wing CL_max 0.93 (glide) and 1.07 (tunnel) at Re 700–2,400 (search-summary).
- **Computed, by others:** CL and L/D at Re 400 (Zhang & Taira, DNS). The values in this document are **my readings of their figures**, accurate to about ±0.02 in CL.
- **Derived here:**
  - every m\*, margin, flip factor and Re value;
  - the restoring-CL bound;
  - the 34° glide angle;
  - the hand calculation in §4.2.
- **Assumed:**
  - need ∝ 1/CL exactly, with the 6.5 % drag share scaling with KE as in S30-D;
  - a step change in CL at Re 700, not a curve;
  - every S30-D input except CL, unchanged: teleost w 15.3 (9.4–21.2), f 0.30, η_s 0.93, η_h 0.37, β 1/3–0.533, isometry.
- **Not done:**
  - no lift value for a thin plate below Re 700 (`unknown`, §3.3);
  - no extrapolation of CL below Re 400, although the central m\* sits at Re 40–110;
  - no re-test of S30's multi-stroke reinterpretation.

```swarm-result
{"subproblem": "S30-D-D", "evidence": "derived: recalculation of S30-D's verdict (m* vs the Re_air=700 validity floor, 37.5 mg) with CL below Re 700 replaced. The replacement is a COMPUTED value (Zhang & Taira 2020 DNS, arXiv 2011.12336, full-text, values read by eye from Fig. 3c/5c: NACA 0015, AR 4, Re 400, time-averaged CL ~0.6 at alpha 30 deg, ~0.39 at max-L/D alpha, L/D < 1.5). The previous value was CL_max 1.07, extrapolated below the edge of Wakeling & Ellington 1997 (Re 700-2400, search-summary; free-glide 0.93 vs tunnel 1.07 kept separate). No measured lift below Re 700 found. Dickinson & Gotz 1993 and Taira & Colonius 2009 could not be accessed (captcha; caltech hosts not resolvable).", "answer": "S30-D's 'no realisable single-impulse window' was robust at its central case (margin 40x) but fragile at its best one-side corner (margin 2.7x, flipped by a x2 error in w, f, eta_h or the extrapolated CL). Replacing the extrapolated CL_max 1.07 below Re 700 with the only quantitative value found there (computed CL ~0.39-0.6 at Re 400, L/D < 1.5) moves m* from 0.94 to 0.05-0.17 mg (centre) and from 14 to 2.1-4.7 mg (corner). That raises the corner margin to 7.9x. A window would need a steady CL >= 3.3 at all Re, so the verdict strengthens. Separately, S30's original 39 mg window falls outside its own data at the source's free-glide CL of 0.93.", "key_number": "CL at Re_air 400 ~0.6 (alpha 30 deg, still rising) and ~0.39 (max L/D), L/D < 1.5 (computed DNS, AR 4, NACA 0015) vs 1.07 extrapolated; resulting m* 0.17 mg central (0.046 at CL 0.39), 4.7 mg best one-side corner (2.1), vs 0.94 / 14.0 mg", "verdict": "strengthens", "depends_on": ["S30-D verdict rule: m* below the Re_air=700 CL-data floor counts as no realisable window (S30-deepen.md, commit efe54c57)", "S30-D teleost w = 0.5*sigma0*eps/rho: 15.3 J/kg central, 9.4-21.2 range (search-summary sigma0 200-300 kPa, eps 0.10-0.15)", "S30-D load-bearing assumption: C-start fibre strain approximates the strain achievable against a spring", "S30 crossover formula m* = m0*R0^(1/(beta-alpha)), alpha = 0 for LaMSA (Sutton2019)", "S30 beta = 1/3 geometric and 0.36-0.533 measured (Fish1990 Table II, PROJECT-TRANSCRIBED)", "S28 anchor m0 = 0.25 g, V_to 4.37 m/s at CL 1.07, SL 30 mm, chord 6.2 mm, AR 5 (case C, unmeasured fin area)", "S29 need 10.17 J/kg at CL 1.07, scaled here as 1/CL", "S29 f = 0.30 one-side muscle fraction (assumed); 0.60 all-muscle", "Ker1981 eta_s 0.93 (via S29)", "Frith-Blake eta_h 0.37 (via S29)", "Wakeling-Ellington1997 CL_max 1.07 tunnel / 0.93 free glide, Re 700-2400 (search-summary; S2 level S)", "Zhang-Taira2020 arXiv 2011.12336 DNS Re 400: CL ~0.6 at alpha 30, ~0.39 at alpha 16, L/D < 1.5 (computed; read from figures)", "ASSUMPTION: NACA 0015 DNS lift brackets a thin fin from below (Laitone1997 abstract via S2; direction vs flat plates not stated by Zhang-Taira)", "ASSUMPTION: CL is a step at Re 700 and is not extrapolated below Re 400", "S2 revolving-wing CL ~1.75 (Usherwood-Ellington2002, level S) as the high-lift comparator", "isometric scaling of the S28 design (Re_air ~ m^0.5)", "S30 multi-stroke reinterpretation (bioRxiv765560, search-extract) - carried, not re-tested"]}
```
