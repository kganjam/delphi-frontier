# S30 — At what body mass does the launch budget close?

**Status:** derived (a scaling argument on stated inputs, plus read-levelled literature). **Nothing in this document is a new measurement.**
Reproduce every number with `python3 docs/research/fish/S30_scaling.py`.
**Depends on:**
- S28 (`claude/s28-organism-design-5z0vjz`): the anchor design. Case-C fin, 0.25 g, WL 12.5 N m⁻², V_to 4.37 m/s, SL 30 mm, chord 6.2 mm.
- S29 (`claude/s29-launch-energy-2iuixr`): the per-kg budget. Need 10.17 J/kg delivered; LaMSA supply 3.30 / 5.47 / 8.36 J/kg.
- S2 (`claude/s2-low-reynolds-aero-acdwr7`): CL_max at low Re.
- The project's transcription of Fish 1990, Tables I–III (`connectors/fish_controls/fish1990.py` on `main`).

## 0. Short answer

**The question has the wrong sign. In a single-impulse launch, getting bigger does not close the budget. Getting smaller does.**

1. **What sets the sign.** S29's budget is written per kilogram. Under isometry, both "energy per kg the animal can deliver in one stroke" and "energy per kg it needs" depend on mass only through their exponents:
   - **Need** scales as wing loading, ∝ m^β. β = 1/3 is geometric; β = 0.36–0.53 is measured across six exocoetid genera (Fish 1990).
   - **Supply, LaMSA:** ∝ m⁰, because spring output is size-independent (Sutton 2019).
   - **Supply, direct muscle:** ∝ m^α with α between 0 and 0.22 (§1).
   - In every combination, **β ≥ α**. Supply/need is therefore flat or *falling* with mass. **No exponent set gives a minimum mass above which a single stroke suffices.**
2. **What the crossover actually is.** The crossover is an **upper** mass bound, the mass *below* which a single stroke suffices.
   - **LaMSA route:** **m\* ≈ 39 mg (range 8.5–173 mg).** A fish of the S28 design shape at that mass is ~16 mm SL.
   - **Muscle-only route:** **m\* ≤ 4 mg**, and as small as 10⁻¹⁰ g for some exponent pairs. That is below any size where the scaling still holds (§2.3). **In practice, the muscle-only route has no crossover at all.**
3. **Where a 0.4 g zebrafish sits.** It is **~10× too *large* (2.3–47×)** for a single-impulse LaMSA launch at its own design shape. It is not "too small". If all ~60 % of its skeletal muscle loaded one spring, the bound rises to ~0.3 g, and the zebrafish is 1.3× too large.
4. **Reality check against exocoetids (Fish 1990: 0.003–0.53 kg).**
   - The literal check passes: the crossover is not above 0.003 kg.
   - But it passes for a reason the brief did not anticipate. My scaling **predicts that no exocoetid, at any mass in that range, can reach glide speed from a single submerged stroke.** A 300 g *Cypselurus* needs ~16 m/s and exits the water at ~10 m/s. It gets there by **taxiing**, which matches the reported taxi peak of 15–20 m/s.
   - So the check does not refute the scaling. It shows that **what flying fish do is a different task (multi-stroke launch) from what the S29 budget describes (single-impulse launch).** This is the revision the check forces.
   - It is falsifiable: a ≥1 g exocoetid shown to reach glide speed from one submerged stroke, with no taxi, would refute this scaling.
5. **Sutton 2019's ~2.5 g crossover is a different crossover from ours.** It is the mass below which a spring gives **more energy per kg than muscle does** in a ground jumper. It says which actuator wins, not whether any task is achievable. Under Sutton's own parameters the spring delivers 4.2 J/kg at any size, less than half the 9.55 J/kg launch needs even on rigid ground. Muscle exceeds 9.55 J/kg only above ~1 kg (11.25 J/kg), and only on rigid ground. Once the ~0.37 water push-off efficiency is applied, neither reaches it (§4).
6. **The empirical floor is not a physical floor.** The smallest animals demonstrated to get airborne and glide are exocoetids of **~1–2 g**. Davenport 1994 gives flight onset at ~50 mm, which is ≈1.1–1.9 g via Fish's length fits. Fish 1990's text cites a "0.001 kg *Hirundichthyes*" at 11.7 N m⁻².
   - That fish needs **4.23 m/s**, essentially the 4.37 m/s the zebrafish design needs. Its wing loading (11.7 N m⁻²) is lower than the zebrafish design's (12.5 N m⁻²).
   - **A 0.4 g zebrafish is 2.5–5× lighter than the smallest known fish glider, but its takeoff requirement is the same.** Size is not what separates them. What separates them is how the energy is delivered: the zebrafish has one stroke at 1.38 m/s, and the flying fish has a multi-stroke route (inferred, not verified at 1 g).

**What this does to S29.** S29 concluded that the barrier is "a property of single-impulse launch from water AT THIS SIZE". **The "at this size" part is wrong.** The barrier does belong to single-impulse launch from water. Within that mode, a smaller fish of the same shape does better, not worse. And the animals that do glide are 2.5–1,300× heavier than zebrafish, and do not use that mode.

---

## 1. How each budget term scales with body mass

Notation: m is body mass and L ∝ m^(1/3) is length under isometry. Each term is written ∝ m^x.

**Read levels:**
- **FULL**: I read the full text in this session.
- **PROJECT-TRANSCRIBED**: transcribed from the paper's page images by earlier project work. I used the transcription and did not re-read the paper.
- **PROJECT**: inherited from S2, S28 or S29 at their stated read levels.
- **SEARCH-EXTRACT**: a search-engine extract only.
- **NOT READ**: named for context only. No number is used.

| # | Term | Exponent x | Kind | Basis and read level |
|---|---|---|---|---|
| 1 | **Required takeoff speed²**, so required KE per kg: e_req = V_to²/2 = WL/(ρ_air CL_max) | **β = 1/3** (geometric); **β = 0.360–0.533** measured, six genera; 95 % CI envelope 0.257–0.663 | geometric / **measured allometry** | WL ∝ m/S ∝ m^(1/3) under isometry. Measured: Fish 1990 Table II, reduced-major-axis fits WL = a·M^b. Four of six genera have b significantly above 0.33 (P marks as printed). **PROJECT-TRANSCRIBED.** |
| 2 | **Wing area** at fixed span:length and AR | **2/3** (geometric); measured **0.479–0.741** | geometric / measured | Fish 1990 Table I, PROJECT-TRANSCRIBED. Hirundichthyes 0.479 and Danichthyes 0.485 are *negatively* allometric, which is why their WL rises fastest (0.53). |
| 3 | **CL_max** (via the wing Reynolds number Re ∝ V·c ∝ m^(β/2+1/3) ≈ m^0.5) | **≈ 0** | **assumed** | S2 (PROJECT): CL_max 0.93–1.07 over Re 700–2,400 for real wings (Wakeling & Ellington 1997). Thin cambered plates are "fairly steady" with Re (Laitone 1997, abstract). No measured CL_max(Re) slope exists in this range, so I assume 0. If CL_max rises with Re, β falls slightly; that is a sensitivity, not a rescue (§2.4). |
| 4 | **Muscle mass**, as a fraction of body | **0** (mass ∝ m¹) | **assumed (isometry)** | The zebrafish 60 % figure is SECONDARY (S29). I read no fish muscle-fraction allometry. |
| 5a | **Energy per stroke per kg, LaMSA** | **α = 0** | model result, cited | Sutton et al. 2019, ICB 59:1609, **FULL** (PMC6907395): "jump height in spring-actuated systems is independent of size." This is the textbook isometric argument: stored energy ∝ spring volume ∝ m. |
| 5b | **Energy per stroke per kg, direct muscle** | **α ∈ [0, 0.22]**; Sutton model two-point slope **0.165** | bounded by derivation; model slope cited | **Lower bound, 0:** work-limited (Hill's argument that work ∝ muscle mass, so e is constant). Hill 1950 NOT READ; Sutton states it. **Model slope:** Sutton 2019 FULL, from 3.6 J/kg at 1 g and 11.25 J/kg at 1 kg: log(11.25/3.6)/log 1000 = 0.165. Sutton's mechanism: "as the system gets smaller, reaching a given velocity … requires a higher shortening strain-rate", which force–velocity penalises. **Upper bound, 2/9, derived here:** if output is purely power-limited, e = P·t with t ∝ s/V ∝ m^(1/3)/e^(1/2), so e^(3/2) ∝ m^(1/3), so e ∝ m^(2/9). No measured fish fast-start energy allometry was readable (§7). |
| 6 | **Spring volume as a fraction of body**, at fixed material energy density | **β** (it follows e_req) | geometric | S29's 1–4 % at 0.4 g becomes 0.5–1.9 % at m\* = 39 mg. **It never binds**, and it gets easier at smaller size. |
| 7 | **Drag during water exit**, as a fraction of KE: W_d/KE = ρ_w C_d A s/(2m) | **0** × C_d(Re) | geometric + assumed | A ∝ L², s ∝ L, m ∝ L³. Body Re_water stays at 5×10⁴–10⁵ over the range of interest, and C_d drift is assumed small. In S29 this term is 6.5 % of need, so even a 2× change in C_d moves the crossover by under ~20 %. |
| 8 | **Hydromechanical efficiency η_h** | **unknown**; treated as 0 | **assumed** | Only pike was measured (0.37; Frith & Blake, ABSTRACT via S29). That is a large fish at high Re, used as the best case *at every mass*. A real Re dependence would make η_h lower in small fish. **This is the one term that could favour larger animals.** §2.4 bounds it. |
| 9 | **LaMSA power per kg** (not an energy term) | **1/6** | geometric | P = e/t with e ∝ m^(1/3) and t ∝ s/V ∝ m^(1/3−1/6). At m\* it is 0.68× the 0.4 g value. S29 already found power not binding. |

**Which exponents carry the result:** β (row 1) against α (row 5). Both are bracketed by geometry, with β also bracketed by a measured allometry. The sign of β − α is never negative across the brackets.

## 2. The crossover

Let R(m) = supply/need. Then R(m) = R₀·(m/m₀)^(α−β), and the crossover R = 1 is at

**m\* = m₀ · R₀^(1/(β−α))**

Because R₀ < 1 and β − α > 0, the exponent is positive, so **m\* < m₀**. The budget closes *below* the anchor mass.

### 2.1 LaMSA route (α = 0)

**Anchor:** m₀ = 0.25 g, the mass at which S28's case-C design is self-consistent at 4.37 m/s.

**R₀ comes from S29:** supply / 10.17 J/kg.
- One side of the axial muscle (30 % of body), w = 32 / 53 / 81 J/kg muscle (Mendoza & Azizi 2021, FULL via S29): R₀ = **0.324 / 0.538 / 0.822**.
- All skeletal muscle (60 %), w = 53: R₀ = 1.076.

| Supply | β = 1/3 | β = 0.36 | β = 0.40 | β = 0.533 |
|---|---|---|---|---|
| w = 32 (min) | 8.5 mg | 11.0 mg | 15.0 mg | 30.3 mg |
| **w = 53 (mean)** | **38.9 mg** | 44.6 mg | 53.0 mg | 78.1 mg |
| w = 81 (max) | 138.9 mg | 145.0 mg | 153.2 mg | 173.1 mg |
| all muscle, w = 53 | 311 mg | 306 mg | 300 mg | 287 mg |

**Central: m\* = 39 mg; range 8.5–173 mg** across one-sided supply and the full β bracket.

- **0.4 g zebrafish ÷ m\* = 10.3× (2.3–46.8×) too large.**
- With all muscle: m\* ≈ 0.3 g, and the zebrafish is 1.3× too large.
- In the all-muscle row β has the opposite effect, because R₀ > 1 there and the bound sits *above* the anchor.

**What a 39 mg fish of this design looks like:** SL 16.1 mm, chord 3.3 mm, V_to 3.20 m/s. Wing Re_air ≈ 712, which is just inside S2's CL_max data (700–2,400). Body Re_water ≈ 5×10⁴. At the 8.5 mg low end, Re_air drops to 334. That is outside the CL_max data, so the low end of the range is an extrapolation.

### 2.2 Why the crossover is an upper bound, in words

The required exit speed rises with mass because wing loading rises: V_to ∝ m^(1/6) at isometry, and m^(0.18–0.27) for real flying fish. A spring's energy per kg does not rise with mass at all. A larger animal of the same shape therefore needs more joules per kilogram and gets the same joules per kilogram. This is the same reason small insects are the champion spring-jumpers. It is also why the measured exocoetid wing-loading allometry (β > 1/3) makes things **worse** for large fish, not better.

### 2.3 Muscle-only route

**Anchor:** a 0.40 g zebrafish at its measured best burst, 1.38 m/s (Miln 2021, via S28).
- The design scaled to 0.40 g needs 4.37·1.6^(1/6) = 4.73 m/s.
- So R₀ = (1.38/4.73)² = **0.0853**.

| α | β | β − α | m\* |
|---|---|---|---|
| 0 | 1/3 | 0.333 | 0.25 mg |
| 0 | 0.533 | 0.533 | 3.9 mg |
| 0.165 | 1/3 | 0.168 | 1.8×10⁻⁴ mg |
| 0.165 | 0.533 | 0.368 | 0.50 mg |
| 0.222 | 1/3 | 0.111 | 9.5×10⁻⁸ mg |
| 0.222 | 0.533 | 0.311 | 0.15 mg |

**m\* ≤ 4 mg in every case.** At 4 mg the scaled design is ~7.6 mm long, with a 1.6 mm chord and V_to ≈ 2.2 m/s, so Re_air ≈ 230. That is well below any CL_max data used here, and it is a larval size where the isometric body and muscle assumptions do not hold. **The muscle-only route has no crossover in any regime where this argument is valid.** The honest statement is "no threshold", not "a threshold of 4 mg".

### 2.4 What could flip the sign, and whether it does

A *minimum* mass would need some term with a net positive exponent larger than β − α ≥ 1/3 (LaMSA). The candidates:

- **η_h rising with Re.** It is the only plausible candidate. But the budget already uses the best measured value, pike at 0.37, at *every* mass. A rising η_h(m) can only *lower* R at small masses relative to what I computed. It cannot raise R above my curve at large masses unless large fish beat pike, and no measurement says they do.
  - **Consequence:** the true crossover is at or below the computed m\*, and the conclusion "no minimum mass" is unaffected.
  - What is genuinely uncertain is how far *below* m\* a small fish's lower η_h pushes the bound. If zebrafish-size η_h were 0.2, R₀ falls by 0.54×. The central m\* then becomes ~6 mg (0.54³ × 39 mg), which moves the window toward larval sizes.
- **CL_max rising with Re.** This lowers β by at most the CL_max slope. To make β < α = 0, CL_max would have to scale faster than m^(1/3), which means doubling for each 8× mass. That conflicts with S2's flat 0.93–1.07 over a 3.4× Re span.
- **Allometric muscle fraction.** Not measured. A fraction rising as m^(≥1/3) would be needed.

**None of these can create a minimum mass under any measured value.**

## 3. Reality check: exocoetids, 0.003–0.53 kg (Fish 1990)

### 3.1 The literal test
"If the crossover comes out above 0.003 kg, the scaling is wrong."
- LaMSA m\* = 0.0085–0.17 g. Muscle m\* ≤ 0.004 g. **Both are below 3 g. The literal test passes.**

### 3.2 But the scaling makes a stronger and riskier prediction
Because the crossover is an upper bound, it says **exocoetids, at every mass from 3 to 530 g, cannot reach glide speed from one submerged stroke.** The brief's premise is that "animals of that mass demonstrably do this". If that means *single-impulse* launch, the scaling is contradicted. So the question becomes: what do flying fish actually do?

Required takeoff speeds from Fish 1990's wing-loading fits, with CL_max 1.07 **assumed** (flying-fish CL_max not read):

| Genus | 1 g (extrap.) | 3 g | 100 g | 530 g |
|---|---|---|---|---|
| Cypselurus | 5.24 m/s | 6.53 | 13.16 | 18.37 |
| Danichthyes | 3.26 | **4.37** | 11.12 | 17.34 |
| Exocoetus | 6.17 | 7.52 | 14.14 | 19.09 |
| Fodiator | 6.10 | 7.74 | 16.56 | 23.78 |
| Hirundichthyes | 3.97 | 5.29 | 13.31 | 20.64 |
| Parexocoetus | 6.46 | 8.08 | 16.53 | 23.23 |

What the table shows:
- **Large flying fish:** a 0.30 m *Cypselurus* is 300 g by Table I (L = 0.460·M^0.355). It has WL 176 N m⁻² and needs **16.4 m/s**.
  - The reported underwater speed before exit is **~10 m/s** for a ~0.3 m fish, and taxiing then raises it to **15–20 m/s** before take-off. Source: bioRxiv 10.1101/765560, **SEARCH-EXTRACT**. The full text returned HTTP 429 and was not read; it cites older work for the 10 m/s.
  - One stroke delivers (10/16.4)² = **37 %** of the needed KE. Taxiing makes up the rest.
  - **This is what the scaling predicts.** A large exocoetid cannot launch on a single impulse, and it doesn't.
- **Small flying fish:** a 3 g *Danichthyes* needs exactly the zebrafish design's 4.37 m/s, at WL 12.5 N m⁻². This is an extrapolation below that genus's sampled range.
  - Fish's smallest quoted wing loading, 11.7 N m⁻², needs **4.23 m/s**.
  - For a ~50 mm fish, 4.23 m/s is **85 body lengths per second**. The best measured zebrafish burst is 46 BL/s (1.38 m/s at 30 mm).
  - **I found no measurement of how the smallest exocoetids leave the water.**

### 3.3 What the check forces me to revise
1. **The task changes.** The S29 budget, and every scaling built on it, describes **single-impulse** launch. The only fish known to glide do not launch that way, at least at adult size (taxi: SEARCH-EXTRACT). The "minimum mass to leave water fast enough to glide" is therefore **not given by this budget at all.** Empirically it is ~1–2 g, set by a multi-stroke mechanism the budget does not model.
2. **The S29 sentence "a property of … launch … at this size" is wrong in its size clause.** Within single-impulse launch, size helps in the *downward* direction.
3. **Falsifiable prediction carried forward:** small exocoetids (1–3 g) also use a multi-stroke route, such as taxiing or tail-assisted acceleration at the surface. **If a ≥1 g exocoetid is filmed reaching ≥4 m/s from a single submerged stroke and gliding with no surface taxi, this scaling is wrong.** It would mean single-stroke specific energy rises with mass faster than wing loading does, which contradicts every exponent in §1.

I did **not** adjust any exponent to make the check pass. The literal test passed on the first computation. The non-trivial content is the reinterpretation in 3.3, and that reinterpretation rests on one search-extract source about adult taxiing, with no source at all for small exocoetids. **That is the weakest link in this document.**

## 4. Sutton et al. 2019: what its ~2.5 g crossover means

**Source:** Sutton, Mendoza, Azizi, Longo & Olberding 2019, "Why do large animals never actuate their jumps with latch-mediated springs? Because they can jump higher without them", *Integr. Comp. Biol.* 59:1609–1618. Read FULL via PMC6907395, through a fetch tool that extracts on request; quotes below are as returned.

- **What crosses over:** "For masses >2.5 g … the modeled mass specific output of a muscle-actuated system is higher than that of a spring-actuated system." Below 2.5 g a spring gives more kinetic energy per kg of accelerated mass. The quantity is *output energy density of a jump*, compared between two actuators.
- **Model:**
  - Isometric scaling: F ∝ L², m ∝ L³.
  - Muscle energy density 15.0 J/kg (bullfrog plantaris).
  - Hill-type force–velocity, with maximum strain rate 10 s⁻¹.
  - Cat-soleus length–tension curve.
  - Spring stores 28 % of muscle energy, so 4.2 J/kg, independent of size.
  - Rigid ground. **No fluid push-off is discussed.**
- **Robustness:** the authors state that activation dynamics etc. "would only move the location of the crossover point, but would not eliminate it."

**How it differs from S30's crossover.**

| | Sutton 2019 | S30 |
|---|---|---|
| Compares | spring output vs muscle output | supply vs a *task requirement* |
| Question | which actuator gives more energy per kg | can *any* actuator reach glide speed |
| Requirement term | none | e_req = WL/(ρ CL_max), which scales with mass |
| Medium | rigid ground | water (η_h ≈ 0.37) |
| Direction | spring favoured **below** 2.5 g | single impulse feasible **below** m\* ≈ 39 mg (LaMSA) |

**They are compatible, and S29 read Sutton correctly:** at 0.4 g, a spring is the better actuator. But "better actuator" does not mean "sufficient actuator".
- Under Sutton's own numbers, a spring jumper reaches √(2·4.2) = **2.90 m/s** at any size, on rigid ground, with no water loss.
- A muscle jumper reaches 2.68 m/s at 1 g, 4.74 m/s at 1 kg, and 5.48 m/s at the 15 J/kg ceiling.
- Neither reaches the **9.55 J/kg (4.37 m/s)** required at the 0.25 g anchor once η_h ≈ 0.37 is applied.

**A discrepancy I flag but do not resolve.** S29's supply uses Mendoza & Azizi's *measured* 53 J/kg muscle stored in a frog tendon, which is 12.6× Sutton's modelled 4.2 J/kg.
- If Sutton's value applied, R₀ = 0.043 and the LaMSA m\* collapses to **0.02–0.7 mg**. That is effectively no realisable crossover, the same as the muscle route.
- The two numbers are probably normalised differently. Mendoza & Azizi give energy per kg of the specific muscle loading the tendon; Sutton gives 28 % of a 15 J/kg whole-muscle work density. That should be checked against Mendoza & Azizi's methods before the 39 mg figure is relied on.
- **The 39 mg is therefore the optimistic end of a range whose pessimistic end is "no window".**

## 5. The answer

**Minimum body mass at which a fish-like animal can leave water fast enough to glide:**

- **By single impulse (S29's mode):** there is **no minimum.** The budget closes *below* an upper bound.
  - LaMSA: **m\* ≈ 39 mg (8.5–173 mg)** at S29's measured spring-loading density. It falls to ~0.02–0.7 mg (effectively none) at Sutton's modelled density.
  - Direct muscle: no realisable crossover (≤ 4 mg, outside the validity of the scaling).
- **By any mode, empirically:** **~1–2 g**, the smallest gliding exocoetids. This is not a physical floor that the scaling recovers. It belongs to a multi-stroke mode the budget does not cover.

**Where a 0.4 g zebrafish sits:**
- **~10× too large (2.3–47×)** for single-impulse LaMSA launch at its own design shape. Making it smaller helps.
- **2.5–5× smaller than the smallest known fish glider**, and that glider needs the same ~4.2–4.4 m/s. Making it bigger would not help: a 3 g fish of the same shape needs 4.37·12^(1/6) = **6.6 m/s**.

**The precise, falsifiable statement.** *The zebrafish is not too small. At fixed shape, its single-impulse launch deficit grows with mass as m^(β−α), with β − α between 0.11 and 0.53 for every bracketed exponent. A spring-launched glider of this design closes its energy budget only below ~40 mg (≈16 mm SL), and only if fish muscle loads a tendon as well as frog muscle does. Real fish gliders (≥1 g) are predicted to use multi-stroke launch at every size.*

## 6. What would test this, in order of decisiveness

1. **How a 1–3 g exocoetid leaves the water.** High-speed video of juvenile flying fish, single stroke versus surface taxi. This tests §3.3 directly and is the cheapest way to break the argument.
2. **Single-stroke spring-loading work density of teleost fast muscle** (S29's test 1). This decides between the 39 mg window and no window (§4).
3. **η_h of a small-fish C-start (PIV) at Re_water ~10⁴–10⁵.** This decides how far below 39 mg the true bound sits (§2.4).
4. **A measured fast-start energy allometry,** e_burst ∝ m^α across a size series in one species (e.g. Wakeling, Kemp & Johnston 1999 carp ontogeny, which I could not fetch). This replaces the bracket α ∈ [0, 0.22] with a number. It cannot flip the sign unless α > β.

## 7. Honesty ledger

- **Measured, by others:**
  - Exocoetid wing-loading, wing-area and length allometries (Fish 1990, PROJECT-TRANSCRIBED from page images; the paper's own text/table inconsistency on 0.001 vs 0.003 kg is kept as is).
  - Adult flying-fish exit speed ~10 m/s and taxi to 15–20 m/s (SEARCH-EXTRACT only).
  - Flight onset ~50 mm (Davenport 1994, via S20 at search-summary level).
  - Zebrafish burst 1.38 m/s (via S28).
  - Frog spring-loading 32–81 J/kg (via S29).
- **Model results cited:** Sutton 2019 (FULL): spring output size-independent; muscle output 3.6 J/kg at 1 g and 11.25 J/kg at 1 kg; crossover ~2.5 g.
- **Derived here:**
  - The α ≤ 2/9 power-limited bound.
  - Every exponent combination, crossover and ratio.
  - The exocoetid V_to table.
  - The length→mass conversions.
- **Assumed:**
  - Isometry of the design shape (fin grows with body) and of muscle fraction. **If muscle fraction rises with mass faster than m^(1/3), §2 breaks.** No fish data were read on this.
  - CL_max independent of Re (supported only over Re 700–2,400).
  - η_h = 0.37 at every mass.
  - CL_max = 1.07 for flying fish.
  - Drag fraction mass-independent.
- **Could not read** (network policy blocked the hosts): the Fish 1990 PDF itself (wcupa.edu, Wiley, ResearchGate, scribd), Davenport 1992 (cambridge.org), Wakeling et al. 1999 (ucl.ac.uk), Domenici & Blake 1997 (core.ac.uk), and bioRxiv 765560 (HTTP 429). For fish fast-starts, search extracts consistently state that length-specific speed falls with size while absolute speed rises (Domenici & Blake 1993/1997, Webb 1978). No exponent was obtained, so none is used.
- **Not invented:** no exponent in this document is fitted to make the exocoetid check pass. β comes from Fish's table or geometry. α comes from Sutton's two points or the derived bounds.

```swarm-result
subproblem: S30
evidence: derived (power-law scaling of the S29 per-kg budget; script docs/research/fish/S30_scaling.py) on - PROJECT-TRANSCRIBED: Fish 1990 J Zool 221:391 Tables I-III (wing loading b=0.360-0.533, CI envelope 0.257-0.663; wing area b=0.479-0.741; length fits; mass range 0.003-0.53 kg; text cites 0.001 kg Hirundichthyes at 11.7 N/m2); FULL: Sutton et al. 2019 ICB 59:1609 (PMC6907395; spring output size-independent; muscle 3.6 J/kg at 1 g, 11.25 J/kg at 1 kg; crossover 2.5 g = spring-vs-muscle output, rigid ground); PROJECT: S28 anchor (0.25 g, WL 12.5 N/m2, 4.37 m/s), S29 supply/need (10.17 J/kg need; 3.30/5.47/8.36 J/kg LaMSA supply; eta_h 0.37), S2 CL_max 0.93-1.07 at Re 700-2400, S20 Davenport 1994 onset ~50 mm; SEARCH-EXTRACT: adult flying fish ~10 m/s underwater then taxi to 15-20 m/s (bioRxiv 765560); NOT READ: Wakeling 1999, Domenici & Blake 1997, Davenport 1992 (hosts blocked)
answer: The launch budget does not close with increasing mass; it closes with DECREASING mass. Required specific energy scales as wing loading, m^beta (beta 1/3 geometric, 0.36-0.53 measured in exocoetids); single-stroke supply per kg scales as m^0 for LaMSA (Sutton 2019) and m^0-0.22 for direct muscle. beta >= alpha in every bracket, so the crossover is an UPPER mass bound. LaMSA: m* = 39 mg (8.5-173 mg) at S29's measured frog spring-loading density, collapsing to 0.02-0.7 mg (effectively none) at Sutton's modelled 4.2 J/kg. Direct muscle: m* <= 4 mg in every case, outside the scaling's validity, i.e. no threshold. Reality check: the literal test (crossover not above 3 g) passes, but the scaling predicts no exocoetid of 3-530 g can reach glide speed by one stroke; adults indeed taxi (300 g Cypselurus needs 16.4 m/s, exits at ~10 m/s = 37% of KE, taxis to 15-20 m/s). So exocoetid flight is a multi-stroke task, not S29's single-impulse task, and S29's 'at this size' clause is wrong. Sutton's 2.5 g crossover is a different quantity (spring vs muscle energy per kg, ground) and is not a feasibility threshold; under Sutton's own numbers the spring gives 4.2 J/kg at any size, and muscle exceeds 9.55 J/kg only above ~1 kg on rigid ground; neither does after water push-off (eta_h 0.37). Empirical minimum glider mass ~1-2 g (smallest exocoetids, WL 11.7 N/m2, V_to 4.23 m/s - the same requirement as the zebrafish design), set by a mode the budget does not model.
key_number: single-impulse LaMSA launch closes only BELOW m* = 39 mg (range 8.5-173 mg); a 0.4 g zebrafish is ~10x (2.3-47x) too LARGE, not too small; muscle-only route has no realisable crossover; smallest real fish glider ~1-2 g needs the same 4.2-4.4 m/s as the zebrafish design
verdict: PREMISE REVISED - no minimum mass exists for single-impulse launch (the bound is an upper one); zebrafish is not too small; S29's 'property of size' is wrong in sign; the exocoetid check passes literally but forces the reinterpretation that real gliders use multi-stroke launch (falsifiable: a >=1 g exocoetid gliding from a single submerged stroke would refute this scaling)
depends_on: [S28, S29, S2, S20, Fish1990-tables, Sutton2019, Mendoza-Azizi2021, Frith-Blake-pike-efficiency, Miln2021-burst, bioRxiv765560-taxi]
```
