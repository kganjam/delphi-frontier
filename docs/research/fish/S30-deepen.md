# S30-D — deepening S30 by attacking its most sensitive input: the spring-loading work density w

**Parent:** S30, `docs/research/fish/S30-organism.md` and `S30_scaling.py` on branch `claude/s30-launch-budget-mass-k71prf` (commit `59f421da`). Read in full.
**Also read:** S29 (`claude/s29-launch-energy-2iuixr`) and S29-D (`claude/s29-deepen-launch-energy-0r1gju`), in full.

**Status: derived.** This is a recalculation of S30's crossover with one input replaced. **Nothing here is a measurement, by this project or by me.** Every number comes from `python3 docs/research/fish/S30-deepen_calc.py`. Literature values carry their read level in the sentence where they are used.

## 0. Result

**Verdict: FALLS for S30's headline number (the 39 mg window). STANDS for S30's sign (the crossover is an upper bound).**

- S30's m\* = 39 mg rests on w = 53 J/kg muscle. That is the energy a **Cuban tree frog plantaris** stores in its own tendon in one tetanic contraction. It is a frog jumping muscle, the highest-scoring of the three frog species measured, transferred unchanged to teleost myotome.
- In m\*, w enters cubed. A factor-of-2 error moves m\* by 8× (§1).
- I could not find a measured teleost value. **None found** (scope in §3.3).
- The best I can do is a **derived upper bound** for teleost fast muscle, ½·σ₀·ε/ρ. Inputs: measured fibre isometric stress (200–300 kPa) and measured fibre shortening in C-starts (≈10–15 %, sonomicrometry). Result: **w ≈ 15 J/kg muscle (9–21; 34 at a curvature-derived strain ceiling)**. That is **3.5× below the frog value**.
- **Recomputed** (calculated, not observed):
  - Central m\* = **0.94 mg**, against S30's 38.9 mg.
  - One-side range **0.22–14 mg** across S30's own β bracket.
  - The 0.4 g zebrafish becomes **~425× too large** (29–1,800×), not ~10×.
- **Why this removes the window rather than just shrinking it.** S30's 39 mg sat almost exactly at the bottom of the CL_max data. The scaled wing reaches Re_air = 700 only at m ≥ 37.5 mg. Every recomputed one-side m\* is below that, at Re_air 111–428.
  - S30 applied this rule to its own muscle route: "the honest statement is 'no threshold', not 'a threshold of 4 mg'". Applied consistently here, it gives the same answer for the LaMSA route: **there is no realisable single-impulse window at any mass where S30's scaling is valid.**
- **Combined with S29-D's measured spring-release chain** (0.10 instead of 0.323), the central m\* drops to **0.03 mg**.

**What survives intact:**
- The sign: β > α, so smaller is easier. Nothing in this document touches β or α.
- "The zebrafish is too large, not too small" survives and is strengthened.
- So does S30's conclusion that real gliders must use multi-stroke launch. That conclusion never depended on w.

---

## 1. Which input m\* is most sensitive to (recomputed)

S30: m\* = m₀ · R₀^(1/(β−α)), with R₀ = f·w·η_s·η_h / need = 0.30·53·0.93·0.37 / 10.17 = **0.538**. This gives m\* = **38.9 mg**, reproducing S30 exactly (script §0).

Each input was doubled and halved, with everything else held central (script §1):

| Input (S30 value) | m\* at ×2 | m\* at ÷2 | Effect on m\* |
|---|---|---|---|
| **w, spring-loading density (53 J/kg muscle)** | 311 mg | **4.9 mg** | ×8 / ÷8 (elasticity 3) |
| η_h, hydromechanical efficiency (0.37) | 311 mg | 4.9 mg | ×8 / ÷8 |
| f, muscle fraction (0.30) | 311 mg (= the 0.60 physical ceiling) | 4.9 mg | ×8 / ÷8 |
| need (10.17 J/kg) | 4.9 mg | 311 mg | ÷8 / ×8 |
| β, wing-loading exponent (1/3) | 99 mg | 6.1 mg | ×2.5 / ÷6.4 |
| η_s, spring return (0.93) | 48 mg (capped at 1.0) | 4.9 mg | ×1.24 / ÷8 |
| m₀, anchor mass (0.25 g) | 78 mg | 19 mg | ×2 / ÷2 |

**What a factor-of-2 error does to the conclusion:**
- **w ÷ 2** puts m\* at 4.9 mg. The scaled design there is SL 8.1 mm with Re_air 252. That is the regime S30 itself ruled out as "no realisable crossover" for the muscle route (S30 §2.3: ≤4 mg, Re_air ≈ 230). **The window disappears.**
- **w × 2** puts m\* at 311 mg. The zebrafish is then only 1.3× too large.
- So **whether a realisable single-impulse window exists at all flips on a factor of 2 in w**.
- The sign of the result does not depend on w. It depends only on β − α, and halving β still leaves it positive.

**Why w, among the four R₀ inputs with elasticity 3** (my judgement, with reasons):
- **need** is a specification (4.37 m/s), inherited from S28. It is not a measured quantity S30 could be wrong about.
- **f** is physically capped at ×2 (all skeletal muscle).
- **η_h** has already been attacked, by S29-D. S30 did not take up S29-D's result, and I carry it in §4.3 rather than re-attack it.
- **w** is the input that S30 itself flags as unresolved. S30 §4: Mendoza & Azizi's 53 J/kg is 12.6× Sutton's modelled 4.2 J/kg, and "should be checked against Mendoza & Azizi's methods before the 39 mg figure is relied on". It is also a measurement on the wrong taxon.

## 2. How well is w = 53 J/kg established?

**Primary source:** Mendoza & Azizi 2021, "Tuned muscle and spring properties increase elastic energy storage", *J. Exp. Biol.* 224(24): jeb243180, doi:10.1242/jeb.243180.

**Read level: full-text,** via journals.biologists.com, with the caveat that the last ~2,800 characters of the page text were not read. Table 1 and Figs 3–4 are images and could not be read, so morphology and per-species stress values are `unknown` to me.

**What the authors report** (quoted from the text):

| Item | Value |
|---|---|
| Stored energy, Cuban tree frog | "could store mass-specific energies averaging **53 J kg⁻¹ muscle mass**" |
| Stored energy, cane toad and bullfrog | "stored an average of **22 and 37 J kg⁻¹** muscle mass, respectively" |
| Cuban tree frog range | 32–81 J kg⁻¹ muscle mass (Discussion) |
| Internal disagreement | The Discussion gives 20 and 36 J kg⁻¹ for toad and bullfrog, against 22 and 37 in Results. **Both are preserved here; the text does not explain the difference** |
| Normalisation | **Per kg of the plantaris longus muscle itself.** The units say so. The text never states the division explicitly, but it says "we measured muscle mass (in grams)" |
| Protocol | Isolated plantaris longus muscle–tendon unit, distal tendon clamped to a servomotor. Tetanic stimulation, 80 pulses s⁻¹ for 400 ms. Sonomicrometry on **one** fascicle. "The area under [fascicle length vs force] corresponded to the work done", assuming "any shortening of the muscle fascicles resulted in an equal stretch of the elastic elements" |
| Stress across species | "peak muscle stress did not differ across species" |
| Mass-specific force | Differed: Cuban tree frogs have shorter fascicles |

**Assessment.**

| Question | Answer |
|---|---|
| Measured? | **Yes, in frogs.** It is a direct measurement of the right *kind* of quantity: muscle work into a series spring in one slow contraction. Its weakness is not its kind. |
| Measured in the animal S30 applies it to? | **No.** It is anuran hindlimb jumping muscle. **S30 used the highest of three frog species' means, with the taxon transfer to teleost myotome unexamined.** The three species span 22–53 J/kg, a 2.4× spread, inside a single clade of jumpers. |
| Proxy for what? | For "J stored per kg of *zebrafish fast myotomal muscle* loading an axial series spring". Teleosts have no such spring (S29 §6), so for fish this is an **assumption repeated until it read as measured**. S29 says "the best *measured* vertebrate rate". That is true, but by S30 the number is used as if it were the fish's. |
| The Sutton discrepancy | **Partly resolved.** Sutton 2019 (full text, PMC6907395) does not say whether its 15.0 J/kg "energy density" is per kg muscle or per kg accelerated mass. Its 4.2 J/kg is a model output: 28 % of the integrated length–tension curve for an optimised linear spring. Mendoza & Azizi is a measurement per kg muscle. **The two are not the same quantity, and the measurement should not be overridden by the model.** But neither number is a teleost number. |
| Evidence level as S30 used it | **Measured value, wrong taxon (jumping-specialist frog), full-text read, applied without a transfer argument.** |

**Inference (mine, not the authors').** The paper reports that peak stress did *not* differ between species, while stored energy per kg differed 2.4×. Energy per kg scales as stress × fascicle strain / density. The between-species difference must therefore lie mostly in how far the fascicles shorten against the tendon. That is a property of the tuned muscle–tendon pairing, the paper's thesis. A fish myotome has no tuned pairing, and its fibre strains are limited by myotomal geometry.

## 3. Improving it

### 3.1 Is there a measured teleost value? No.

I looked for a measurement of **energy stored per kg of teleost muscle into a series elastic element in one contraction**. None was found.

The nearest teleost systems are the syngnathid feeding LaMSA, where epaxial muscle loads a tendon:
- **Avidan, Day & Holzman 2023,** *Proc. R. Soc. B* 290:20230520, PMC10089724. **Read level: full-text** (PMC, via fetch extraction). It reports suction power (3,266–4,263 W kg⁻¹ muscle), tendon power and a 48 % bar compression. It reports **no stored energy, no J kg⁻¹ value and no muscle mass**. The tendon force–length data are in supplementary material I did not read.
- **Van Wassenbergh et al. 2008,** pipefish, *J. R. Soc. Interface* 5:285. **Read level: search-summary.** It gives power (5,795 W kg⁻¹), not energy per kg.

### 3.2 The real quantity, bounded from teleost measurements (DERIVED)

A muscle whose force is capped at F₀ = σ₀A, shortening by ε·L_f into a linear (Hookean) spring, stores at most **½·F₀·ε·L_f**. A collagen spring, which is J-shaped and stiffening, stores less for the same end force and stretch. Per kg muscle:

**w_max = ½ σ₀ ε / ρ_muscle**, with ρ = 1060 kg m⁻³ (assumed).

**Teleost inputs:**
- **σ₀, fast-fibre isometric stress, 200–300 kN m⁻².**
  - Sculpin fast fibres: 281 kN m⁻²; sculpin myotomes at 5 °C: 220 kN m⁻².
  - "P₀ values at physiological temperatures (200–300 kN m⁻²)", similar across Antarctic, temperate and tropical species.
  - **Read level: search-summary** (abstract snippets). The paper behind each snippet was not confirmed beyond what the search returned. **No zebrafish value found.**
- **ε, fast-fibre shortening during a C-start, ≈ 0.10–0.15.** All measured by sonomicrometry in vivo:
  - Rainbow trout: 13 ± 5 % at 0.4 L and 15 ± 8 % at 0.7 L (Goldbogen & Shadwick).
  - Rainbow trout: up to 11.3 % shortening after a 2.5 % prestretch (Ellerby & Altringham).
  - Antarctic rock cod: up to 13 %.
  - Sculpin: 12 % peak-to-peak.
  - **Read level: search-summary.**
  - **A source that disagrees,** carp (curvature-derived, not sonomicrometry): white fibres up to 24 % anteriorly and 10 % posteriorly. I keep 0.24 as a separate ceiling and do not average it in.

**Result** (script §3; calculated, not observed): **w ≈ 15.3 J/kg muscle (σ₀ 250 kPa, ε 0.13).** The sonomicrometry range is **9.4–21.2**, with a **34** ceiling at the carp strain.

**Three cross-checks:**
- S29 back-calculated **8.6 J/kg muscle per stroke** from the zebrafish's measured 1.38 m/s burst (with η_h 0.37). That is the same order. It is not independent, because it carries η_h.
- Sutton's modelled 4.2 J/kg is 0.27× this bound. A bound may sit above a model, so they do not conflict.
- The frog's 53 J/kg implies σ₀ε = 112 kJ m⁻³, which is ε ≈ 0.37 at 300 kPa (derived; **the authors do not report fascicle strain**). That is about 3× the fibre shortening measured in fish fast-starts.

**The caveat that could undo §3.2, stated in full.** ε here is the strain fish fibres *do* reach in a C-start. It is **not** a measured *ceiling* on the strain they *could* reach shortening against a compliant spring.
- Myotomal fibre geometry ("gearing") keeps fibre strain small relative to body bending. A hypothetical series spring would change that boundary condition.
- If teleost fast fibres can operate over ~35 % shortening on their force–length curve, w could approach the frog value.
- **I found no teleost fast-muscle force–length curve wide enough to settle this.** The sarcomere working range of zebrafish fast fibres is `unknown` here.
- **This is why §3.2 is a bound on what the myotome as built delivers, not a measurement of what the muscle could deliver.**

### 3.3 Scope of the negative searches

- Six standard web searches:
  - Mendoza & Azizi values;
  - fish fast-muscle work per cycle;
  - James & Johnston 1998 scaling;
  - fast-fibre isometric stress;
  - syngnathid tendon energy;
  - C-start fibre strain.
- Full-text fetches: Mendoza & Azizi 2021 (journals.biologists.com, two passes); Sutton 2019 (PMC); Avidan 2023 (PMC).
- James & Johnston 1998, *J. Exp. Biol.* 201:913, **abstract only** (the full text is paywalled). It gives a size-independent maximum instantaneous power of 307 W kg⁻¹ (C-bend) and 222 W kg⁻¹ (contralateral), but no work in J kg⁻¹ and no strain amplitudes in the abstract.
- **Blocked host:** cob.silverchair.com (DNS not resolvable in this session); I did not retry it.
- **Not searched:** non-English literature, theses, Web of Science or Scopus.
- **Within that scope:** no measured teleost J kg⁻¹ into a series spring, and no zebrafish fast-fibre σ₀ or force–length width.

## 4. Recompute and verdict

### 4.1 Recomputed m\* with teleost w (S30's η chain unchanged; script §4)

| w (J/kg muscle) | β = 1/3 | 0.36 | 0.40 | 0.533 |
|---|---|---|---|---|
| teleost low, 9.4 | 0.22 mg | 0.37 | 0.71 | 3.1 |
| **teleost central, 15.3** | **0.94 mg** | 1.4 | 2.4 | 7.6 |
| teleost high, 21.2 | 2.5 mg | 3.5 | 5.4 | 14.0 |
| ceiling (carp strain), 34.0 | 10.2 mg | 13.0 | 17.4 | 33.9 |
| central, all muscle (f = 0.6) | 7.5 mg | 9.8 | 13.5 | 28.0 |
| ceiling, all muscle (f = 0.6) | 82 mg | 89 | 99 | 124 |
| *S30 (frog, 53)* | *38.9 mg* | *44.6* | *53.0* | *78.1* |

**Validity.**
- The scaled design reaches Re_air ≥ 700 only at m ≥ **37.5 mg**. That is the floor of the CL_max data S30 used (Re 700–2,400; inherited from S2).
- **Every one-side teleost value lies below that floor.** At the central 0.94 mg the design is SL 4.7 mm, chord 0.96 mm, Re_air 111. At the high corner (14 mg) it is SL 11.5 mm, Re_air 428.
- Only the all-muscle rows at the carp-strain ceiling (82–124 mg) clear 37.5 mg. Each stacks three optimistic choices: every skeletal muscle loading one spring, the curvature-derived strain, and S30's η chain.

### 4.2 Each part of S30's conclusion

| S30 claim | With the improved w | Status |
|---|---|---|
| The crossover is an upper bound (budget closes as mass decreases) | Unchanged. It depends on β − α, not w | **STANDS** |
| LaMSA m\* ≈ 39 mg (8.5–173 mg), a fish ~16 mm SL | Central **0.94 mg**; one-side 0.22–14 mg; all below the CL_max data floor. By S30's own rule (§2.3), there is **no realisable window** | **FALLS** |
| A 0.4 g zebrafish is ~10× (2.3–47×) too large | **~425× (29–1,800×)** too large | **STRENGTHENS** |
| The muscle-only route has no realisable crossover | Unaffected | STANDS |
| Real gliders use multi-stroke launch | Unaffected by w. Its weakest input is still the search-extract-only taxi source (S30's own flag) | STANDS (not re-tested here) |
| The 39 mg is "the optimistic end of a range whose pessimistic end is 'no window'" | The improved input lands on the pessimistic end | Resolved toward "no window" |

### 4.3 Compounded with S29-D (not taken up by S30)

S29-D replaced S29's implied spring-release chain η_s·η_h/(1 + drag) = 0.323 with the measured mechanical-fish analogue, KE/E_stored ≈ 0.10 (Conte et al. 2010, abstract via S29-D). Applying both replacements (script §5; calculated):

| Case | m\* |
|---|---|
| Teleost central | **0.028 mg** |
| Teleost ceiling, all muscle | 2.4 mg |
| Frog 53, one side | 1.2 mg |
| Frog 53, all muscle | 9.2 mg |

**No combination reaches the 37.5 mg validity floor.**

### Verdict

**FALLS** for the quantitative window that S30's answer reported.

**STANDS** for the sign, and **STRENGTHENS** "the zebrafish is too large, not too small".

**Precise statement.** With w bounded from teleost fast-muscle stress and C-start fibre strain (derived, ~15 J/kg muscle), S30's single-impulse LaMSA crossover drops from 39 mg to ~1 mg (0.2–14 mg). That is below the smallest mass (37.5 mg) at which S30's own CL_max inputs are valid. **The single-impulse route therefore has no realisable mass window for a fish-like animal**, and is not "closed below ~40 mg".

**What would restore the window:**
- teleost muscle storing ≳ 50 J/kg in one contraction; or
- all skeletal muscle loading one spring, at the carp strain ceiling, with S29's (not S29-D's) efficiency chain.

## 5. What measurement would settle w, and what it would cost

**The quantity:** energy stored per kg of **zebrafish fast myotomal muscle** shortening against a compliant series load in one tetanic contraction. Mendoza & Azizi's protocol applied to fish.

**Design** (mine):
1. Use a dissected adult zebrafish fast-muscle bundle (or a whole myotomal block) on a dual-mode muscle lever.
2. A real tendon is unavailable, so the servo emulates a series spring ("virtual tendon"). The stiffness is swept so that the bundle shortens by 5–40 % of L₀ at peak force.
3. Integrate force over fibre shortening, measured by laser diffraction of sarcomere length or by video.
4. Stimulate tetanically at 28 °C.
5. **Outputs:**
   - w(stiffness), the peak over stiffness being the answer;
   - the force–length curve width (the §3.2 caveat);
   - σ₀ for zebrafish fast fibres (currently `unknown`).
6. **Controls:**
   - *Positive:* the same rig on a frog plantaris, which must reproduce 22–53 J/kg.
   - *Must-fail:* an infinitely stiff series load (isometric), which must give w ≈ 0.
   - A physical spring of known stiffness, to validate the virtual tendon.
7. **Decision rule** (script §1/§4):
   - w ≥ ~50 J/kg restores S30's 39 mg window.
   - w ≤ ~25 J/kg confirms "no realisable window" even before S29-D's chain.

**Estimated cost** (estimates, not quotes):
- In a lab that already runs work-loop rigs, roughly 2–6 weeks of one person, with consumables under ~US$2,000.
- Without such a rig, a commercial dual-mode lever system and stimulator are a five-figure purchase. **That is the dominant cost.**
- The output would be **measured**.

## 6. Sources

| # | Source | Read level | Used for |
|---|---|---|---|
| 1 | S30-organism.md and S30_scaling.py (`claude/s30-launch-budget-mass-k71prf`, 59f421da) | full-text | Formula, anchor and every baseline input |
| 2 | S29-organism.md (`claude/s29-launch-energy-2iuixr`) | full-text (grep of w-related passages plus S29-D's summary) | Provenance of w, f, η_s, need |
| 3 | S29-deepen.md (`claude/s29-deepen-launch-energy-0r1gju`) | full-text | Spring-release chain 0.10 vs 0.323 |
| 4 | Mendoza & Azizi 2021, *J. Exp. Biol.* 224:jeb243180 | full-text (last ~2.8 k characters, Table 1 and figures not read) | 53 (32–81), 37, 22 J kg⁻¹ muscle; protocol; stress not different across species |
| 5 | Sutton et al. 2019, *Integr. Comp. Biol.* 59:1609, PMC6907395 | full-text (fetch extraction) | 15.0 J/kg and 4.2 J/kg are model values; normalisation unstated |
| 6 | Avidan, Day & Holzman 2023, *Proc. R. Soc. B* 290:20230520, PMC10089724 | full-text (fetch extraction) | Syngnathid tendon LaMSA: no J kg⁻¹ reported |
| 7 | James & Johnston 1998, *J. Exp. Biol.* 201:913 | abstract | Escape power size-independent (307 / 222 W kg⁻¹); no work value |
| 8 | Fast-fibre P₀ 200–300 / 281 / 220 kN m⁻² (sculpin, eel, cross-latitude comparison) | search-summary | σ₀ |
| 9 | C-start fibre strains: Goldbogen & Shadwick (trout), Ellerby & Altringham (trout), Antarctic rock cod, sculpin, carp (curvature) | search-summary | ε |
| 10 | Van Wassenbergh et al. 2008, *J. R. Soc. Interface* 5:285 | search-summary | Power only; not used numerically |

## 7. Honesty ledger

- **Measured, by others:**
  - Frog spring-loading 22 / 37 / 53 (32–81) J kg⁻¹ muscle (full text).
  - Teleost fast-fibre σ₀ and C-start fibre strains (search-summary).
  - Syngnathid power values (full text, not used numerically).
- **Model, by others:** Sutton's 4.2 J kg⁻¹.
- **Derived here:**
  - The teleost upper bound w = ½σ₀ε/ρ and its table.
  - Every m\*, ratio, scaled design and the 37.5 mg validity floor.
  - The frog-implied strain of 0.37.
- **Assumed:**
  - Muscle density 1060 kg m⁻³.
  - A linear spring is the most favourable realistic spring.
  - The C-start fibre strain represents what a myotome loading a spring could reach. **This is the load-bearing assumption of S30-D. If teleost fast fibres can shorten ~35 % at near-full force against a compliant load, the verdict reverts toward S30.**
  - All of S30's other inputs, unchanged.
- **Not done:** I did not re-test S30's multi-stroke reinterpretation or its β values.

```swarm-result
{"subproblem": "S30-D", "evidence": "derived: recalculation of S30's crossover m* = m0*R0^(1/(beta-alpha)) with w replaced by a teleost upper bound w = 0.5*sigma0*eps/rho built from search-summary teleost fast-fibre P0 (200-300 kPa) and sonomicrometry C-start fibre shortening (10-15%); primary source of S30's w read at full-text (Mendoza & Azizi 2021: 53 J/kg is Cuban tree frog plantaris, per kg muscle; toad 22, bullfrog 37); no measured teleost spring-loading value found (scope: 6 web searches, 3 full-text fetches; cob.silverchair.com blocked)", "answer": "S30's most sensitive input, the spring-loading density w (elasticity 3 on m*), is a frog-jumping-muscle measurement transferred to fish without argument; bounding it from teleost fast-muscle stress and C-start fibre strain gives ~15 J/kg muscle (9-21, ceiling 34), which drops the single-impulse LaMSA crossover from 39 mg to ~0.94 mg (0.22-14 mg one-side), below the 37.5 mg at which S30's own CL_max data are valid, so the realisable window falls while the upper-bound sign stands and the zebrafish becomes ~425x (29-1800x) too large.", "key_number": "teleost spring-loading work density w ~15 J/kg muscle (derived upper bound, range 9.4-21.2, ceiling 34.0) vs 53 J/kg muscle frog (Mendoza & Azizi 2021); m* 0.94 mg (0.22-14 mg) vs 38.9 mg", "verdict": "falls", "depends_on": ["S30 crossover formula m* = m0*R0^(1/(beta-alpha)) (S30-organism.md, commit 59f421da)", "S30 alpha = 0 for LaMSA (Sutton2019 size-independent spring output)", "S30 beta = 1/3 geometric and 0.36-0.533 measured (Fish1990 Table II, PROJECT-TRANSCRIBED)", "S28 anchor m0 = 0.25 g, V_to 4.37 m/s, SL 30 mm, chord 6.2 mm", "S29 need 10.17 J/kg body delivered (incl. 6.5% drag)", "S29 f = 0.30 one-side muscle fraction (assumed) and 0.60 all-muscle (secondary)", "Ker1981 tendon return eta_s 0.93 (via S29)", "Frith-Blake1995 eta_h 0.37 (via S29; model-derived)", "S29-D spring-release chain KE/E_stored 0.10 (Conte2010, abstract) vs 0.323", "Mendoza-Azizi2021 frog spring-loading 22/37/53 (32-81) J/kg muscle, full-text", "Sutton2019 model spring 4.2 J/kg (normalisation unstated)", "teleost fast-fibre isometric stress P0 200-300 kN/m2 (search-summary; no zebrafish value)", "C-start fast-fibre shortening 0.10-0.15 sonomicrometry (trout, rock cod, sculpin; search-summary) and 0.24 carp curvature-derived ceiling", "muscle density 1060 kg/m3 (assumed)", "ASSUMPTION: linear series spring is the most favourable realistic spring (w <= 0.5*sigma0*eps/rho)", "ASSUMPTION: in-vivo C-start fibre strain approximates the strain a myotome could reach loading a spring (load-bearing)", "S2 CL_max data range Re_air 700-2400, giving the 37.5 mg validity floor", "S30 rule: m* below the CL_max/isometry validity range counts as no realisable crossover", "S30 multi-stroke reinterpretation (bioRxiv765560 taxi, search-extract) - carried, not re-tested"]}
```
