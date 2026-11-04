# S29 — Can launch energy be engineered? Latch-mediated spring actuation in a 0.4 g teleost

**Status:** derived (calculation on stated inputs, plus a read-levelled literature survey). **Nothing in this document is a new measurement.**
Reproduce every number with `python3 docs/research/fish/S29_launch_energy.py`.
**Depends on:** S28 (`claude/s28-organism-design-5z0vjz`, `docs/research/fish/S28-organism.md`). S28 supplies the 4.37 m/s target, the 1.38 m/s burst and the 24 mm² frontal area.

## 0. Short answer

**No. But this route fails by about 2×, where every wing route failed by 10× or more.** The way it fails changes what the barrier is.

1. **The spring is not the problem.** Storing the launch energy takes **0.8–4 % of body volume** of tendon-grade collagen at mammalian working stress. At the strain a fish tendon is actually *measured* to reach, it takes **13–24 %**. Either way the spring fits inside the animal.
2. **Power is not the binding term either.** If the spring releases over 5–14 ms, the demand is **7,400–18,400 W per kg of driving muscle**. That is 1.3–3.2× what fish LaMSA systems already achieve (pipefish 5,795 W/kg). It is well inside what insect LaMSA achieves (froghopper 36,000–74,000 W/kg).
3. **The binding term is energy per stroke.** A spring amplifies **power, not energy**. Every joule it releases was put in by muscle, and less than half of it reaches the fish, because the fish pushes off water and not ground.
   - The stroke needs **29.6 J per kg of body stored**.
   - One side of the axial musculature, storing work at the best *measured* vertebrate rate for loading a spring (frog: mean 53 J/kg muscle, max 81), supplies **only 54–82 %** of that.
   - **Short by 1.2–1.9×.** A frog-like 20 % body-mass jumping muscle is **short by 2.8×**.
   - It only closes if **essentially all of the fish's skeletal muscle (~60 % of body mass)** loads a single spring through a single latch in a single stroke. Even then the ratio is 1.08 (at 53 J/kg) to 1.64 (at 81 J/kg).
4. **The latch has no locomotor precedent in any fish.** The only measured teleost LaMSA systems are the *feeding* systems of Syngnathiformes: seahorses, pipefish and snipefish. Their four-bar over-centre latch rotates the head. None is in a cyprinid, and none is in the body axis.

**The deeper conclusion.** S28's wall was not a wing problem, and it is not a muscle-power problem. It is an **energy-per-stroke × push-off-medium** problem. In the central case that product is 11.5× what the fish delivers today. A spring raises the muscle's per-stroke work by 3.7–9.4×, because slow loading escapes the force–velocity penalty. The remaining 1.2–3.1× is set by how much muscle the animal has and by the measured ~37 % efficiency of pushing off water. **No spring touches either term.** The barrier is therefore a property of *a single-impulse launch from water by an animal this size*, not of any one mechanism. That is the only result here that generalises.

---

## 1. Power-amplification literature (read-levelled)

**Read levels.**
- **FULL** — I read the full text.
- **PREPRINT-FULL** — I read the full bioRxiv text.
- **ABSTRACT** — I read the abstract, or a search-engine extract of it.
- **SECONDARY** — the value comes from another paper's citation or a reproduced table, and I did not read the primary source.
- **NOT READ** — named for context only. No number is used.

Several primary PDFs could not be fetched: the session's network policy blocked `cob.silverchair.com`, `media.physics.hmc.edu`, `par.nsf.gov` and `typeset.io`. Wherever that limited the read level, it is stated.

### 1.1 Baseline: muscle

| Quantity | Value | Basis | Source | Read level |
|---|---|---|---|---|
| Vertebrate muscle, max instantaneous power | **1,121 W/kg muscle** | in vitro | Askew & Marsh 2001, as cited by Longo et al. 2018 and Avidan et al. 2020 | SECONDARY |
| Fish fast myotomal muscle in a fast-start | **142.7 W/kg muscle** (*Scorpaena notata*, 20 °C) | work loop, agrees with kinematics | Wakeling & Johnston 1998, J. Exp. Biol. 201:1505 | ABSTRACT |
| Largemouth bass epaxial muscle | ~216 W/kg | in vitro | Coughlin & Carroll 2006, as cited by Longo 2018 | SECONDARY |
| Bluegill suction-feeding power | 321 ± 18 W/kg | PIV | Avidan, Day & Holzman 2020 (bioRxiv 10.1101/2020.08.13.249466) | PREPRINT-FULL |

The brief's ~250–450 W/kg "vertebrate ceiling" sits between the fish values and the 1,121 W/kg instantaneous maximum. I compute amplification factors against **1,121 W/kg**, which is the conservative denominator, and also against bluegill 321 W/kg.

### 1.2 What LaMSA achieves

All values in this table are **per kg of muscle** unless stated otherwise.

| System | Measured power density | ÷ 1,121 | ÷ 321 | Source | Read level |
|---|---|---|---|---|---|
| Snipefish *Macroramphosus scolopax*, head rotation | **2,800 ± 560** (range 1,090–5,500) | 2.5× | 8.7× | Longo, Goodearly & Wainwright 2018, Proc. R. Soc. B 285:20181078 | FULL |
| Seahorses *Hippocampus* spp., net suction power | **3,266–4,263** | 2.9–3.8× | 10–13× | Avidan, Day & Holzman 2020 | PREPRINT-FULL |
| Bay pipefish *Syngnathus leptorhynchus*, head rotation | **5,795** (instantaneous) | 5.2× | 18× | Van Wassenbergh et al. 2008, J. R. Soc. Interface 5:285 | ABSTRACT |
| Froghopper *Philaenus spumarius*, jump | **36,000** mean, **74,000** best jumps (reported as 36 and 74 W g⁻¹ muscle) | 32–66× | 112–230× | Burrows 2003, Nature 424:509 | ABSTRACT |
| Mantis shrimp, strike | **4 × 10⁴ per kg muscle** vs **3.8 × 10⁶ per kg spring** | ~36× | — | Patek et al. 2023 LaMSA review, J. Exp. Biol. 226:jeb245262 | ABSTRACT |
| Trap-jaw ant *Odontomachus bauri*, mandible | 35.5–64.3 m/s peak, ~10⁵ g, 0.06–0.13 ms. **No W/kg reported.** | — | — | Patek et al. 2006, PNAS 103:12787 | FULL |

Notes on the table:
- **Burrows 2003:** the search extract gave the best take-off velocity as ~4 m/s and the mean as 2.8 m/s. **I could not confirm the commonly quoted 4.7 m/s and do not use it.**
- **Mantis shrimp:** the Patek et al. 2004 (Nature 428:819) abstract extract renders its figure as "4.7 × 10⁻⁵ W/kg", which is plainly a garbled exponent. I therefore use the 2023 review's figure instead. The 2023 review warns that per-muscle and per-spring normalisations are not comparable across systems.
- **Trap-jaw ant:** Patek et al. 2006 give speed, acceleration and duration but no power density, so no amplification factor can be computed.
- **Ilton et al. 2018** (Science 360:eaao1082) is the framework paper on cascading motor → spring → latch limits. **ABSTRACT only.** The full text was blocked, so I take no number from it. Its stated framing is that springs circumvent motor power limits, and that the spring's material and the latch's dynamics then set new limits.
- **Bhamla:** I read no Bhamla paper for this note.
- **Fungal ballistospores and plant cases (*Pilobolus*, *Sphagnum*):** NOT READ. They are cited only as a category: systems loaded by osmotic or evaporative engines rather than muscle.

**Measured amplification factors** (power ÷ 1,121 W/kg):
- **Fish:** 2.5–5.2×.
- **Insects:** 32–66×.
- **Stomatopods:** ~36× per muscle mass.

**What sets the upper bound.**

1. **Energy conservation, the bound that matters here.** A spring cannot release more energy than muscle put into it, less hysteresis (~7–10 % for tendon: Ker 1981, ABSTRACT; Gosline 2002 resilience 90–92 %, SECONDARY). Power amplification is achieved entirely by shortening the *release time*, and the energy is fixed by the *loading* stroke.
2. **Spring material and mass.** The spring has to accelerate its own mass, and its material wave speed and energy density cap release speed (Ilton 2018, ABSTRACT framing).
3. **Length–tension losses in loading.** In a model, Sutton et al. 2019 (Integr. Comp. Biol. 59:1609, FULL) find that a muscle-loaded spring stores only **~28 %** of the muscle's available energy. They place the size **crossover at ~2.5 g**: below it, spring actuation beats direct muscle. A 0.4 g fish is on the spring-favoured side, which is the one point in this hypothesis's favour.
4. **What is actually stored.** Mendoza & Azizi 2021 (J. Exp. Biol. 224:jeb243180, FULL) measured muscle stretching its own series tendon in situ in Cuban tree frogs. The muscle stored **53 J/kg muscle on average, 32–81 J/kg range**. This is the best measured "muscle work into spring" density I found, and §6 uses it.
5. **Resilin is not the main spring.** Rogers et al. 2024 (PNAS, FULL) knocked down resilin in locusts. Take-off velocity fell only 15–19 %, and the authors conclude that **stiff cuticle is the principal energy store and resilin is protective.** Nothing here should be costed on resilin alone.

## 2. What the launch needs

Unless stated otherwise, body mass is m = 0.40 g and the target is V = 4.37 m/s.

### 2.1 Energy
- KE = ½ · 0.40×10⁻³ · 4.37² = ½ · 0.40×10⁻³ · 19.10 = **3.819 mJ = 9.55 J/kg**.
  - In J/kg this is mass-independent. At S28's 0.25 g it is 2.387 mJ, still 9.55 J/kg.
  - **Caveat:** the 4.37 m/s target was derived by S28 at 0.25 g. With S28's case-C fin, a 0.40 g fish needs 4.37 · √(0.40/0.25) = **5.53 m/s**, which is **15.28 J/kg**, 1.6× more. I use the brief's 4.37 m/s, so **everything below is the optimistic case.**
- Today, at the measured 1.38 m/s burst: ½ · 1.38² = **0.95 J/kg**. The ratio is **10.03×**, which confirms S28's 10× energy gap.

### 2.2 Distance and time
The stroke must be delivered **in water and next to the surface**. In the central case (Cd 0.2, ASSUMED), drag at 4.37 m/s is 45.8 mN, which is **11.7 body weights**. Coasting 1 cm loses 4.37 → 4.10 m/s. The acceleration therefore has to end within about a centimetre of breaking the surface.

Constant acceleration, a = V²/2s, t = 2s/V:

| Stroke s | t | a | Mean power, per kg body | Peak power (2× mean) |
|---|---|---|---|---|
| 0.50 cm | 2.29 ms | 1,910 m/s² (195 g) | 4,173 W/kg | 8,345 W/kg |
| **1.09 cm** | **4.99 ms** (seahorse/pipefish timescale) | 876 m/s² (89 g) | 1,914 W/kg | 3,828 W/kg |
| 1.50 cm (½ BL) | 6.86 ms | 637 m/s² (65 g) | 1,391 W/kg | 2,782 W/kg |
| 3.00 cm (1 BL) | 13.73 ms | 318 m/s² (32 g) | 695 W/kg | 1,391 W/kg |

Drag work during the stroke is W_d = ½ρ Cd A V² s/2, since v² is linear in x under constant acceleration:
- Cd 0.2, s 1.09 cm: W_d = 0.5 · 1000 · 0.2 · 24×10⁻⁶ · 19.10 · 0.0109/2 = **0.250 mJ (6.5 % of KE)**.
- Range across cases: 3–27 % of KE (Cd 0.1–0.3, s 1–3 cm).

### 2.3 Energy that must be stored

**Floor** (no drag, no wake loss): 3.819 / 0.93 = **4.107 mJ = 10.27 J/kg body**.

**Central case**, step by step:
1. Body work: 3.819 + 0.250 = 4.069 mJ.
2. Divide by the hydromechanical efficiency η_h = 0.37: **11.00 mJ**.
   - η_h = 0.37 is the best measured C-start value, for pike (range 0.34–0.39; S-start 0.27). Source: Frith & Blake, energetics of fast-starts in *Esox lucius*. ABSTRACT, from a UBC record. Acceleration of added water mass was 39 % of power output.
   - If Frith & Blake's "useful power" already excludes drag work, this double-counts ~6 %. That error is small and conservative.
3. Divide by spring return 0.93: **11.83 mJ = 29.56 J/kg body**.

**Why η_h is there.** A flea pushes on rigid ground. A fish's only reaction surface is water, and every impulse sheds a wake. That loss belongs to the medium, not to the actuator.

### 2.4 Spring volume as a fraction of body volume

Body volume = 0.40 g / 1050 kg m⁻³ (ASSUMED density) = **381 mm³**.

| Spring material (energy density u) | u (MJ m⁻³) | Floor: mm³ / % body | Central: mm³ / % body |
|---|---|---|---|
| Collagen tendon at 100 MPa, E = 1.65 GPa: u = σ²/2E = 10¹⁶/3.3×10⁹ | 3.03 | 1.36 / **0.36 %** | 3.90 / **1.02 %** |
| Same, at 50 MPa | 0.76 | 5.42 / 1.42 % | 15.6 / **4.10 %** |
| Tuna caudal tendon, E 1.2 GPa, at the **measured** burst strain 2 %: u = ½Eε² | 0.24 | 17.1 / 4.49 % | 49.3 / **12.9 %** |
| Same, E 0.65 GPa | 0.13 | 31.6 / 8.29 % | 91.0 / **23.9 %** |
| Resilin, toughness **to failure** 4 MJ m⁻³ | 4.0 | 1.03 / 0.27 % | 2.96 / 0.78 % |
| Collagen, toughness **to failure** 6 MJ m⁻³ | 6.0 | 0.68 / 0.18 % | 1.97 / 0.52 % |

Sources for the table:
- Ker 1981 (J. Exp. Biol. 93:283, ABSTRACT): sheep plantaris tendon E ≈ 1.65 GPa, ~7 % dissipated. The 50–100 MPa working stress is Ker's quoted figure for a galloping antelope.
- Shadwick, SICB abstract on tuna axial tendons (ABSTRACT): E 0.65–1.2 GPa, 7–25 % dissipation, strain under 1 % in steady swimming and 1.5–2 % at maximal burst. The authors conclude that **"the caudal tendons in tunas do not function as energy saving locomotor springs, even at maximal swimming effort."**
- Gosline et al. 2002 Table 2 (Phil. Trans. R. Soc. B 357:121): SECONDARY, from a reproduction of the table. Failure toughness is an upper bound, not a working energy density.

**This is the number the brief asked for. The spring is 1–4 % of body volume if teleost collagen can be worked like mammalian tendon, and 13–24 % at the strains fish tendon is measured to reach.** Either way it fits. On volume alone, the mechanism is plausible.

## 3. Does any fish already do this?

**Feeding: yes, measured, and only in Syngnathiformes.**
- **Pipefish:** the head-rotation requirement reaches 5,795 W/kg muscle. Epaxial EMG begins **more than 300 ms** before the strike, which is the signature of slow loading (Van Wassenbergh 2008, ABSTRACT).
- **Snipefish:** prey capture in 2.0–7.5 ms and up to ~8,700° s⁻¹ of head rotation, at 2,800 W/kg mean. The spring is a pair of large unossified epaxial tendons (Longo 2018, FULL).
- **Seahorses:** a *dual* spring, with the epaxial tendon driving the head and the sternohyoideus tendon (which shortens by up to 53–55 %) driving the suction flow, at 3,266–4,263 W/kg. Avidan et al. describe vertebrate LaMSA as "extremely rare" (Avidan 2020, PREPRINT-FULL).
- **Function:** every one of these systems rotates the head and drives suction. None moves the body through the water.

**Locomotion: I found no measured elastic energy storage that does useful launch work in any teleost.**
- The best-studied candidates, tuna caudal tendons, reach only 1.5–2 % strain at burst and are judged not to be locomotor springs (Shadwick, ABSTRACT). A 2013 ISB poster hypothesises the opposite, but it is untested.
- No LaMSA has been reported for zebrafish or any cyprinid. My search was limited by the network policy.

**What exists to be modified:**
- **Myotomal muscle that already fires slowly before release.** This is an assumption from the pipefish EMG precedent; whether zebrafish muscle can do it is unmeasured.
- **Collagenous myosepta.** These are short, and their stiffness is unmeasured here.
- **The Mauthner escape circuit as a fast neural trigger.** Background knowledge, NOT READ for this note.

**What does not exist:** a long series tendon gathering the axial muscle force, and a latch on the body axis.

## 4. The latch

| Mechanism | Where | Stores energy? | Releases on cue? | Status for a zebrafish locomotor latch |
|---|---|---|---|---|
| Four-bar **over-centre (torque-reversal) latch** of the hyoid–neurocranium linkage; release thought to be triggered by sternohyoideus/hypaxial action | Seahorse, pipefish, snipefish *feeding* apparatus | Yes (with epaxial tendons) | Yes | **Exists, measured** (Longo 2018 FULL; Avidan 2020 PREPRINT-FULL). Phylogenetically distant from zebrafish (Cypriniformes vs Syngnathiformes) and anatomically in the head, not the axis. Moving it into the axial skeleton would be an **invention by analogy**, not a modification |
| Dorsal-spine locking (triggerfish) and pectoral-spine locking (catfish) | Fin spines | No — these are positional locks | Yes (unlocking) | Background knowledge, NOT READ for this note. These show that teleosts can evolve skeletal locks. **They are not springs.** Zebrafish has neither |
| Muscle-as-latch: antagonist co-contraction, with release by relaxing the antagonist | Frogs, locusts | Indirectly | Yes | No measured instance in teleost locomotion |

**Concretely**, a zebrafish needs three things it does not have:
1. A series elastic element loaded by the axial muscle of one side. It must hold 11.8 mJ: 3.9–16 mm³ of mammal-grade tendon, or ~49–91 mm³ at tuna strains.
2. A geometric latch that holds the body straight (or pre-bent) against that load.
3. A trigger.

Item 1 is a large *modification* of myoseptal collagen. Item 2 is an **invention with no locomotor precedent in any fish**. Item 3 plausibly already exists (Mauthner circuit). On the brief's own credibility scale, this is closer to invention than to modification.

## 5. The binding term: energy per stroke

The supply delivered to the body, per kg of body, is:

**supply = f_muscle · w_muscle · η_spring(0.93) · η_h(0.37)**

where f_muscle is the fraction of body mass that loads the spring and w_muscle is the energy each kg of muscle stores (J/kg).

The fish needs **10.17 J/kg** at the body in the central case. The floor (η_h = 1, no drag) is **9.55 J/kg**.

| Muscle loading the spring (f) | w = 32 | w = 53 (mean) | w = 81 (max) |
|---|---|---|---|
| 10 % (lower jumper value, Sutton 2019 data set, SECONDARY) | 1.10 (×0.11) | 1.82 (×0.18) | 2.79 (×0.27) |
| 20 % (upper jumper value) | 2.20 (×0.22) | **3.65 (×0.36)** | 5.57 (×0.55) |
| **30 % = one side of the axial muscle (ASSUMED half of 60 %)** | 3.30 (×0.32) | **5.47 (×0.54)** | **8.36 (×0.82)** |
| 60 % = all skeletal muscle (SECONDARY review figure; primary not read) | 6.61 (×0.65) | 10.94 (×1.08) | 16.72 (×1.64) |

Cells give supply in J/kg body, with the fraction of the 10.17 J/kg central need in brackets. w values are the measured range from Mendoza & Azizi 2021.

**Muscle fraction of body mass needed to load the spring** (central case; floor in brackets):
- 56 % at w = 53 J/kg (19 % at the floor).
- 37 % at w = 81 J/kg (13 %).
- 92 % at w = 32 J/kg (32 %).

**The same result, framed against today's fish.** This framing is derived and uses the same η_h and one-side assumption:
- Today's 1.38 m/s burst implies one-side muscle work of 0.381 mJ / 0.37 = 1.03 mJ, which is **8.6 J/kg muscle per stroke**. That figure is force–velocity limited.
- The launch needs **98.5 J/kg** from the same muscle: 10.17 / (0.30 · 0.93 · 0.37). That is **11.5×** today's figure.
- Slow loading into a spring is measured at 32–81 J/kg in frogs, which is 3.7–9.4× today's figure. That is exactly the gain LaMSA offers a small animal (Sutton 2019's crossover logic).
- **The shortfall is 1.2–3.1×.**

## 6. Verdict

**NEGATIVE, narrowly, and on a different term from every earlier failure.**

| Term | Required | Available (best measured analogue) | Status |
|---|---|---|---|
| Spring volume | 1–4 % of body (mammal-grade tendon) / 13–24 % (fish tendon at measured strain) | the body | **PASSES** |
| Power density | 7,400–18,400 W/kg muscle mean (14 → 5 ms release, one-side muscle) | 5,795 (fish) / 36,000–74,000 (insect) | Fish LaMSA short 1.3–3.2×. Insect-grade LaMSA would pass. **Not binding** |
| **Energy per stroke** | **98.5 J/kg muscle** (one side), i.e. 10.17 J/kg body delivered | 53 (32–81) J/kg muscle, measured in frogs | **FAILS by 1.86× (1.22–3.08×)** |
| Latch | locomotor latch on the body axis | over-centre latch in the syngnathiform head only | **No precedent. Invention** |
| Target | 4.37 m/s | — | Optimistic: at 0.40 g, S28's own fin needs 5.53 m/s, which is **15.3 J/kg, 1.6× more**. That turns the 1.86× into **~3.0×** |

**By what factor, on which term.** The best case still fails on **muscle energy per stroke × hydromechanical efficiency**:
- 1.86× short with one-sided axial muscle at the mean measured spring-loading work, 4.37 m/s target.
- About 3.0× short at the mass-consistent 5.53 m/s target.
- It reaches break-even (1.08×) only if **all** skeletal muscle (~60 % of the body) loads one spring through a latch no fish has, in one stroke, at the best measured pike efficiency.

**This is a second, precisely quantified failure, and it is a different kind of failure.** The wing routes failed by 10× or more, against a wall nobody was pushing on. This route removes the power wall, which LaMSA genuinely does. It then lands about 2× short on a wall no spring can move: **the joules one muscle stroke can put in, times the ~37 % of them that survive pushing off water.** That points to a property of the organism and its medium, not of a mechanism. It is also consistent with the fact that real aquatic launchers do not launch from a single impulse. They accumulate energy over many strokes while the tail is still in the water, which is the taxiing route that S24 found tail-frequency limited.

**What measurement would test it.** The result is within about 2×, so it is arguably testable rather than closed. In order of decisiveness:
1. **Single-stroke spring-loading work density of zebrafish fast myotomal muscle**, measured in situ against a compliant series load, using Mendoza & Azizi's protocol on a myotomal preparation.
   - **Decision rule:** w ≥ ~99 J/kg muscle → the energy term closes for one-sided loading. w ≤ ~53 J/kg → closed at ≥1.86×.
   - Nothing in the literature I read gives this number for any teleost.
2. **Hydromechanical efficiency of an adult zebrafish C-start (PIV).** The 0.37 is pike, a much larger fish at higher Re. η_h enters linearly. A zebrafish value of 0.6 or more would cut the shortfall to about 1.1×. A value of 0.2 would make it about 3.4×.
3. **Dissected axial muscle mass fraction of adult zebrafish.** The 60 % comes from a secondary review. The one-side 30 % is my assumption.
4. Only if (1)–(3) jointly close: **a teleost locomotor latch**. This has no precedent and cannot be "measured", only built. It is the step that turns a plausible energy budget into an organism.

## 7. Honesty ledger
- **Measured (by others, read-levelled in §1):**
  - LaMSA power densities: fish 2,800–5,795 W/kg; insects 36,000–74,000 W/kg (per kg muscle).
  - Frog spring-loading work: 32–81 J/kg muscle.
  - Tendon E: 0.65–1.65 GPa.
  - Tuna tendon burst strain: 1.5–2 %.
  - Pike C-start η_h: 0.34–0.39.
  - Zebrafish burst: 1.38 m/s (via S28).
- **Derived here:** every energy, distance, time, power, volume and ratio in §2–6.
- **Assumed:**
  - Body density 1050 kg m⁻³ and Cd 0.1–0.3 in water on S28's 24 mm² frontal area.
  - Constant-force stroke, so peak power = 2× mean.
  - One side = 30 % of body mass.
  - η_h transfers from pike to zebrafish.
  - Frog muscle's spring-loading work transfers to fish myotomal muscle.
- **Not used, though named:** Ilton 2018 numbers (full text blocked), Bhamla, the fungal and plant cases, the froghopper "4.7 m/s", and fin-spine locking mechanics.
- **Optimism left in on purpose:**
  - The 4.37 m/s target, not the mass-consistent 5.53 m/s.
  - No surface-break penalty (S28 row 7 is still unquantified).
  - No loss for the spring accelerating its own mass.
  - No Sutton-type length–tension loss beyond what the frog measurement already contains.
  - Every one of these would widen the 1.86× gap.

```swarm-result
subproblem: S29
evidence: derived (closed-form energy/power/volume budget, script docs/research/fish/S29_launch_energy.py) on read-levelled literature - FULL: Longo 2018 snipefish 2800 W/kg, Patek 2006 trap-jaw, Sutton 2019 ICB crossover ~2.5 g, Mendoza & Azizi 2021 frog spring-loading 32-81 J/kg muscle, Rogers 2024 resilin RNAi; PREPRINT-FULL: Avidan 2020 seahorse 3266-4263 W/kg; ABSTRACT: Van Wassenbergh 2008 pipefish 5795 W/kg, Burrows 2003 froghopper 36000-74000 W/kg, Ker 1981 tendon E 1.65 GPa, Shadwick tuna tendon E 0.65-1.2 GPa at 1.5-2% strain, Frith & Blake pike C-start eta 0.37, Wakeling & Johnston 1998 142.7 W/kg, Ilton 2018 (framing only); SECONDARY: Askew & Marsh 1121 W/kg, Gosline 2002 toughness, zebrafish muscle 60% body mass
answer: Latch-mediated spring actuation removes the POWER wall but not the ENERGY wall. A 0.4 g body at 4.37 m/s needs KE 3.82 mJ = 9.55 J/kg; with in-water drag (6.5%) and the best measured C-start hydromechanical efficiency (0.37) and tendon return (0.93) the spring must store 11.8 mJ = 29.6 J/kg body. That spring is small - 1-4% of body volume as mammal-grade tendon, 13-24% at fish-tendon measured strains - so volume passes. Power for a 5-14 ms release is 7400-18400 W/kg muscle, 1.3-3.2x beyond fish LaMSA (5795) but within insect LaMSA (36000-74000), so power is not binding. Energy per stroke is binding: one-sided axial muscle (30% body) at the best measured spring-loading work (frog 53, max 81 J/kg muscle) supplies 54-82% of need; the muscle would have to store 98.5 J/kg vs 8.6 J/kg it effectively delivers today (11.5x) and slow spring loading only buys 3.7-9.4x. Break-even needs ~all skeletal muscle (60%) loading one spring in one stroke. No teleost has a locomotor spring or latch; the only fish LaMSA (syngnathiform over-centre head latch) is in feeding. Decisive test: in-situ single-stroke spring-loading work of zebrafish fast myotomal muscle (>=~99 J/kg closes the energy term), plus zebrafish C-start PIV efficiency.
key_number: energy-per-stroke shortfall 1.86x (range 1.22-3.08x; ~3.0x at the mass-consistent 5.53 m/s target) vs >=10x for every wing route; spring volume only 1-4% (13-24% at fish tendon strain) of body
verdict: NEGATIVE (narrow) - fails by ~2x on muscle energy per stroke x hydromechanical efficiency, not on spring volume or power; latch would be an invention with no locomotor precedent in fish. Barrier is a property of single-impulse launch from water at this size, not of any one mechanism
depends_on: [S28, launch, taxiing/S24, Miln2021-burst, Mendoza-Azizi2021, Frith-Blake-pike-efficiency, Longo2018, Avidan2020, VanWassenbergh2008, Sutton2019, Ker1981, Shadwick-tuna-tendon]
```
