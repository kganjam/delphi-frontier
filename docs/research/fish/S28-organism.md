# S28 — The integrative question: what is the best achievable organism, and what can it actually do?

**Status:** derived (calculation on stated inputs). **Nothing in this document is a new measurement.**
Reproduce every number with `python3 docs/research/fish/S28_organism.py`.

## 0. Short answer

The best design we can build from alleles with a demonstrated zebrafish phenotype **cannot fly, cannot glide, and cannot skim.**
It does no better than a **wild-type leap**. At the fastest measured adult burst (1.38 m/s), the designed pectoral "wing" makes
**2–3 % of body weight in lift averaged over the arc**. It extends the best leap from **19.4 cm to at most 19.8–20.0 cm (+1.5 % to +3 %)**.
At the median-to-low end of the measured burst range (0.45 m/s) the gain is **+0.2 %**.

The honest name for this phenotype is **"a long-finned zebrafish whose leap is aerodynamically indistinguishable from wild type
within ordinary measurement error"**. It is *not* an extended leap, and calling it one would already be an overstatement.
A 3× longer leap would need an exit speed of **2.39 m/s**, which is **1.73× the measured maximum**. The wing cannot supply it.

This is a precisely quantified negative. Section 3 states the real phenotype that remains achievable and measurable.

---

## 1. Inputs, with evidence levels

| Symbol | Value | Level | Source / note |
|---|---|---|---|
| g, ρ_air, ν_air | 9.81 m s⁻², 1.225 kg m⁻³, 1.5e-5 m² s⁻¹ | constant | — |
| Adult burst speed, U_b | 0.45–1.38 m/s | **measured** | Miln et al. 2021, n = 50, high-speed video. This is *swimming* burst, not water-exit speed (see §4) |
| Max tail-beat frequency | 52 Hz | **measured** | project input |
| CL_max (corrected) | 1.07 | derived (project) | used unchanged |
| Required takeoff speed V_to | 4.37 m/s | derived (project) | 1-BL span, AR 5, CL_max 1.07 |
| Standard length SL | 3.0 cm | **assumed** typical adult | |
| Body mass m | 0.25 g | **assumed**, back-solved | it is the mass at which the project's V_to = 4.37 m/s is self-consistent: W/S = ½ρV²CL = 0.5·1.225·4.37²·1.07 = **12.5 N m⁻²**, so S = 2.45e-3 N / 12.5 = **196 mm²**. A 0.40 g fish (also typical) raises every V_to below by √(0.40/0.25) = 1.26× |
| Tail amplitude A (peak-to-peak) | 11.9 mm (≈ 0.4 SL) | back-solved | the value that reproduces the project's 132–199 Hz: f = St·U/A → 0.36·4.37/0.0119 = 132 Hz; 0.54·4.37/0.0119 = 198 Hz |
| Daane et al. 2021 double het (lat4a^nr21/+ ; kcnh2a^lof/+) | elongated paired fins, reduced median fins, "phenocopies flying-fish proportions" | **literature, length only** | Curr. Biol. 31:5052, doi 10.1016/j.cub.2021.08.054. Fig. 4B reports pectoral length / SL. **I did not read the numeric values of Fig. 4B for this note.** Fin AREA, ray stiffness, lift and glide were never measured |

**Consistency flag (the project's own numbers).** From the inputs as stated, the speed deficit is 4.37/1.38 = **3.17×** to 4.37/0.45 = **9.71×**. The kinetic-energy deficit is 3.17² = **10.0×** to 9.71² = **94.3×**. The project summary says "4–7× speed, 27–48× energy". Those figures do not follow from 4.37 vs 0.45–1.38 m/s. They must have used other burst values, or added the energy needed to clear the surface. I do not resolve this here. Every result below uses the stated 0.45–1.38 m/s directly, so it does not depend on which deficit figure is right.

## 2. The best achievable design

### 2.1 Allowed changes
Only alleles with a **demonstrated zebrafish fin phenotype** are used:
- `kcnh2a^lof/+` (*longfin*, a dominant cis-regulatory gain of channel function). It elongates all fins.
- `lat4a^nr21/+` (slc43a2a, GeneID 393221, chr15). In trans with *lof*, it suppresses median-fin overgrowth and leaves the paired fins long (Daane 2021, Fig. 4).

Excluded, because no demonstrated phenotype exists: pectoral-muscle enlargement, ray stiffening (S26), any change in burst speed.

So the organism is the **existing Daane double heterozygote**. It is not a new construct.

### 2.2 Geometry
**Fin length:** set by the allele, but the numeric value is *not read here* (see the table). **Fin area:** never measured. I therefore give the geometry as three bracketing cases. All share the same span:

- Span b = 2 × fin length + body width = 2 × 13.5 mm + 4 mm = **31 mm ≈ 1.0 SL**.
  - **EXTRAPOLATION.** 13.5 mm = 0.45 SL per fin. That is a "flying-fish-proportion" pectoral. I assume it to match the project's 1-BL span, and I have not taken it from the measured allele. If Fig. 4B shows less, every lift number below falls further.

| Case | Area assumption | S (mm²) | AR = b²/S | V_to = √(2W/(ρ S CL_max)) |
|---|---|---|---|---|
| **A — length-only** | rays elongate, fin base/chord unchanged (~3 mm). 2 fins × 0.7 × 13.5 × 3 = 57 | **57** | 961/57 = **16.9** | √(2·2.45e-3/(1.225·57e-6·1.07)) = **8.10 m/s** |
| **B — isometric** | fin keeps wild-type shape, area ∝ length². Assumed WT fin ≈ 10 mm² each, scaled ×2.5² | **125** | 961/125 = **7.7** | **5.47 m/s** |
| **C — project prior** | AR 5 imposed | **192** | **5.0** | **4.41 m/s** (≈ the project's 4.37) |

- **Mass:** 0.25 g body (assumed) + fin membrane 192 mm² × 50–100 µm × 1100 kg m⁻³ = **10.6–21.1 mg** (estimate).
  - This adds 4–8 % to the mass and raises V_to by a further 2–4 %. I do not charge it below; doing so would only make every result worse.
- **Wing Reynolds number** (chord 6.2 mm, case C): at 1.38 m/s, Re = 1.38 × 0.0062 / 1.5e-5 = **570**. At 4.37 m/s, Re = **1806**.

**Case C is the most generous, and it is not supported by any measurement.** Case A is the closest to what the *longfin* allele is known to do (it lengthens rays). **I use case C as the headline, so every conclusion below is an upper bound.**

## 3. What it can actually do

### 3.1 Ballistic leap from a measured burst (wing off = wild type)
I assume the exit speed equals the burst speed. This is generous: burst is measured while swimming, and breaking the surface costs speed.
Over a short hop at these speeds, drag is about 0.6 % of weight (body: ½·1.225·1.38²·0.3·2.4e-5 = 1.4e-5 N vs W = 2.45e-3 N), so the hop is effectively vacuum ballistics:

| Exit speed | Max range R = V²/g (45°) | Apex at 45°, V²/(4g) | Vertical leap V²/(2g) | Airtime at 45°, 2V sin45°/g |
|---|---|---|---|---|
| 0.45 m/s | 0.2025/9.81 = **2.06 cm** (0.7 SL) | **0.52 cm** | **1.03 cm** | 0.065 s |
| 1.38 m/s | 1.904/9.81 = **19.4 cm** (6.5 SL) | **4.85 cm** | **9.71 cm** | **0.199 s** |

The numerical integration with body drag gives 19.36 cm at 1.38 m/s, which agrees.

### 3.2 Leap with the designed wing spread
Point-mass integration: gravity, body drag (CD 0.3 on 24 mm² frontal area), wing lift perpendicular to velocity at fixed CL, wing drag CD0 + CL²/(π·0.8·AR). Launch angle is optimised for range.

| Case | CD0 | Exit 1.38 m/s: range | gain vs WT | Exit 0.45 m/s: gain |
|---|---|---|---|---|
| C (192 mm², AR 5), CL 1.07 | 0.08 | **19.82 cm** | **+2.4 %** | +0.2 % |
| C, CL 1.07 | 0.20 | 19.64 cm | +1.5 % | +0.1 % |
| B (125 mm²) | 0.12 | 19.65 cm | +1.5 % | +0.1 % |
| A (57 mm²) | 0.12 | 19.50 cm | +0.7 % | ~0 % |
| **Upper bound:** case C with zero wing drag | 0 | **19.94 cm** | **+3.0 %** | — |

**Why it is so small.** At launch, lift is (V/V_to)² × W = (1.38/4.37)² = **0.0997 W**, i.e. 10 % of weight. That fraction falls as V² while the fish climbs. At the apex only the horizontal component remains, 1.38·cos45° = 0.98 m/s, giving (0.98/4.37)² = **5 %**. Lift is perpendicular to the path, so on the way down part of it points *backwards*. The net effect is +1.5–3 % range, about **3–6 mm**. The apex is *unchanged or lower* (4.75–4.84 cm vs 4.85 cm), because wing drag cancels the small lift.

**3× wild-type range** would need an exit speed of 1.38 × √3 = **2.39 m/s**, which is **1.73× the measured maximum**. The wing contributes nothing towards it.

### 3.3 Glide ratio and glide range at the measured maximum
- **A steady glide does not exist at 1.38 m/s.** A glide needs L = W, which requires V ≥ V_to = 4.37 m/s. At 1.38 m/s the wing gives 10 % of W at CL_max, so the "glide" is just the ballistic arc of §3.2.
- **Glide range from a 1.38 m/s exit: none. The trajectory is the ballistic 19.4–19.9 cm above.**
- *Conditional only, for an animal that somehow reached 4.37 m/s:*
  - The wing's best glide ratio is L/D_max = 1/(2√(CD0·k)) with k = 1/(π·0.8·5) = 0.0796.
  - CD0 = 0.08 → 1/(2√0.00637) = **6.3**. CD0 = 0.12 → **5.1**. CD0 = 0.20 → **4.0**.
  - The optimum CL* = √(CD0/k) = 1.00–1.59. That is at or above CL_max, so the wing could only glide right at stall speed.
  - Glide range = (L/D) × height, i.e. 4–6 cm per cm of height.
  - **This is not a capability of the designed organism. It is the wing's ceiling if the launch problem were solved.**

### 3.4 Lowest speed at which the wing produces "useful" lift
Lift fraction f = (V/V_to)². So V_f = 4.37 √f (case C; ×1.24 for case B, ×1.85 for case A):

| Lift as fraction of weight | V needed |
|---|---|
| 10 % | 4.37·√0.10 = **1.38 m/s** — exactly the measured maximum burst |
| 25 % | 4.37·0.5 = **2.19 m/s** |
| 50 % | 4.37·0.707 = **3.09 m/s** |
| 100 % (flight / glide / airborne skim) | **4.37 m/s** |

Even in the generous case C, the fastest measured zebrafish sits **exactly at the 10 %-of-weight threshold**, and only at the instant it leaves the water.

### 3.5 Water-surface skim (body airborne, tail still driving)
In an airborne skim the wing must carry essentially all of the weight. Only the lower caudal lobe is in the water, and it contributes negligible buoyancy and little planing lift.

The highest speed the tail can drive at 52 Hz is U = f·A/St:
- St 0.54: 52 × 0.0119 / 0.54 = **1.15 m/s** → lift (1.15/4.37)² = **6.9 % of W**.
- St 0.36: 52 × 0.0119 / 0.36 = **1.72 m/s** → lift (1.72/4.37)² = **15.5 % of W**.

Both values assume the *whole* tail is thrusting. With only a lobe submerged, thrust and speed are lower still. **The skim is not reachable.** Below about 4.4 m/s the remaining 85–93 % of the weight must be carried by buoyancy, which means the body is in the water. That is ordinary surface swimming, not a skim. The tail-frequency shortfall for a skim is the project's taxiing result: **132–199 Hz needed vs 52 Hz, 2.5–3.8× short.**

### 3.6 Honest capability statement
- **Not flight.** It cannot reach V_to: 3.2× short in speed and 10× short in kinetic energy, even against the best measured fish.
- **Not gliding.** No steady glide exists below 4.37 m/s.
- **Not a skim.** The tail can drive the fish to 7–16 % lift at most.
- **Not even a meaningfully extended leap.** The gain is +1.5 to +3.0 % range (≈ 3–6 mm on 19.4 cm), and only with the unmeasured AR-5 fin area at the top of the measured burst range. The gain is ≈ 0 % at the low end and +0.7 % for the length-only (case A) fin.

**The deliverable phenotype that remains real and measurable** is the *existing* Daane double heterozygote, characterised aerodynamically. The question becomes "does a genetically elongated pectoral fin change leap mechanics at all?"

Prediction: the effective downward acceleration during the ascent is reduced by about 5–10 % (lift 10 % at exit, 5 % at apex) **if the fish spreads its pectorals during the leap.** Whether it does so has never been observed.

That is a concrete, falsifiable aerodynamic phenotype for an engineered fin. It is the most that can honestly be claimed, and it would be worth publishing as such. A "3× leap" is not achievable from fin changes. Only a 1.73× faster exit speed would produce one.

## 4. Shortest path to a falsifiable experiment

Each candidate, ranked by how far its outcome could move this document:

1. **Pectoral fin AREA (and spread-fin span) in the existing Daane double het. RECOMMENDED.**
   - **Cost:** anaesthetise, spread the fin, take one calibrated photograph. The animal exists, and the authors measured length but not area. Hours of work.
   - **Why it moves the picture:** S enters every lift number linearly. It decides whether the design is case A, B or C, and therefore whether the only achievable phenotype (§3.6) is **detectable**.
   - **Decision rule:**
     - S ≤ ~60 mm² (AR ≥ 15): lift at exit ≤ 3 % W. Declare the aerodynamic phenotype undetectable and close the line.
     - S ≥ ~190 mm²: lift is 10 % W at exit. Proceed to film leaps.
   - **It cannot flip the flight verdict.** Flying at 1.38 m/s would need S = 192 × (4.37/1.38)² = **1925 mm² (19 cm²)**. That is two fins of about 10 cm² each on a 3 cm fish, roughly 10× the fish's own lateral area.
2. **Water-exit speed of a leaping adult** (high-speed video at the surface).
   - This is the *only* measurement that could flip the flight verdict, which needs ≥ 4.37 m/s.
   - Miln et al. measured swimming burst, not exit speed. My prior is that exit speed is ≤ burst, so the expected change is small. It is the runner-up because a positive result would overturn everything.
   - Combine it with (1) in the same session: film WT siblings and double hets leaping, and fit the ascent acceleration.
3. **Direct ray stiffness (S25).**
   - At leap loads (10 % W) the required EI is about 0.1 × 6.3e-4 = **6.3e-5 N m²**. If 3.8e-6 is right, the fin is still **17× too soft** and deflects even in a leap. If 565e-6 is right, it holds.
   - This changes whether case C's lift is actually realised. It cannot rescue launch.
4. **Pectoral muscle mass in zebrafish.**
   - Only relevant to flapping, which the launch deficit already rules out. **This is the least informative of the four.**

## 5. What would have to be true for powered flight instead of a leap

All of the following must hold **jointly**. "Short by" is required ÷ current.

| # | Required (measured) value | Current | Short by | Level of "current" |
|---|---|---|---|---|
| 1 | Water-exit speed ≥ **4.37 m/s** (case C; 5.47 B; 8.10 A) | 1.38 m/s max (0.45 low) | **3.2×** speed / **10×** KE (best fish); 9.7× / 94× (low) | measured (burst, not exit) |
| 2 | *or* tail-beat frequency for a taxi/skim to 4.37 m/s: **132–199 Hz** | 52 Hz | **2.5–3.8×** | measured |
| 3 | Pectoral fin area ≥ **192 mm²** at 1-BL span (AR ≤ 5) | unmeasured; length-only allele suggests ~57–125 mm² | **1.5–3.4×** (estimate) | **never measured** |
| 4 | Fin span ≥ **1.0 SL** (0.45 SL per fin) | Daane Fig. 4B, value not read here | unknown — **extrapolation** | literature, unread |
| 5 | Ray flexural stiffness EI ≥ **6.3e-4 N m²** | ≤ 3.8e-6 (or 565e-6, S25 open) | **166×** (or 1.1×) | literature, disputed |
| 6 | Pectoral muscle ≥ **7.5–20 %** of body mass (flapping) | ~1.4 % (teleost) | **5.4–14×** | measured (teleost, not zebrafish) |
| 7 | Leap or launch pathway with no surface-break penalty | — | unquantified | — |

Rows 1/2, 5 and 6 each fail by a factor between **2.5× and 166×** on present evidence. No allele with a demonstrated phenotype addresses rows 1, 2, 5 or 6. Powered flight is not a near miss. It would need at least three independent organism-level changes, none of which has been demonstrated.

## 6. Honesty ledger
- **Measured:** burst 0.45–1.38 m/s; tail-beat 52 Hz; teleost pectoral fraction ~1.4 %; the existence of the double-het fin-length phenotype.
- **Derived here:** everything in §3, from the inputs in §1 and the script.
- **Assumed:**
  - m = 0.25 g, SL = 3.0 cm, wild-type fin area 10 mm² and chord 3 mm, body drag CD 0.3, Oswald e = 0.8, CD0 0.08–0.20.
  - Exit speed = burst speed. This is generous.
  - The fish holds the fins spread at CL 1.07 throughout the leap. This is generous and unobserved.
- **Extrapolated beyond any measured allele:** fin length 0.45 SL; the fin area of cases B and C; AR 5.
- **Inconsistency left open:** the project's "4–7× / 27–48×" vs the 3.2–9.7× / 10–94× implied by its own stated inputs (§1).

```swarm-result
subproblem: S28
evidence: derived (point-mass trajectory integration and closed-form aerodynamics on measured burst 0.45-1.38 m/s and 52 Hz tail-beat; fin geometry extrapolated, fin area never measured; script docs/research/fish/S28_organism.py)
answer: The best design buildable from demonstrated alleles is the existing Daane lat4a^nr21/+;kcnh2a^lof/+ zebrafish. Even granting an unmeasured 1-BL span and AR-5 fin (S=192 mm2), it cannot fly, glide or skim. At the measured maximum exit speed of 1.38 m/s the wing gives 10% of weight at launch and about 5% at the apex, and lengthens the 19.4 cm ballistic leap by only +1.5 to +3.0% (3-6 mm; ~0% at 0.45 m/s). A 3x leap would need a 2.39 m/s exit, 1.73x the measured maximum. The tail at 52 Hz can drive a skim to only 1.15-1.72 m/s, giving 7-16% lift. The honest phenotype is a possibly detectable 5-10% reduction in ascent deceleration, not an extended leap. Cheapest decisive measurement: pectoral fin AREA in the existing double het, which decides whether even that phenotype is detectable. Only water-exit speed of 4.37 m/s or more could flip the flight verdict.
key_number: +3.0% maximum leap-range gain (19.4 -> 19.9 cm) at the measured 1.38 m/s burst; flight needs 4.37 m/s (3.2x speed, 10x energy)
verdict: NEGATIVE - not flight, not glide, not skim, not a meaningfully extended leap; deliverable is a falsifiable small aerodynamic leap phenotype in an existing animal
depends_on: [launch, taxiing, structure/S25, S26, muscle, Daane2021-genetics, Miln2021-burst]
```
