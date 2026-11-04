# Challenge 259: adversarial review of S30-D (teleost spring-loading density w)

**Claim under review (verbatim, not mine):** "S30's most sensitive input, the spring-loading density w (elasticity 3 on m\*), is a frog-jumping-muscle measurement transferred to fish without argument. Bounding it from teleost fast-muscle stress and C-start fibre strain gives ~15 J/kg muscle (9–21, ceiling 34). This drops the single-impulse LaMSA crossover from 39 mg to ~0.94 mg (0.22–14 mg one-side), below the 37.5 mg at which S30's own CL_max data are valid. So the realisable window falls, the upper-bound sign stands, and the zebrafish becomes ~425× (29–1800×) too large." Verdict claimed: **falls**. Recorded evidence level: **measured**.

**Sources read:**
- S30-D (`docs/research/fish/S30-deepen.md` and `S30-deepen_calc.py`, branch `claude/deepen-s30-launch-budget-jb7qj4`). **Read level: full-text.**
- S30 (`S30-organism.md`, branch `claude/s30-launch-budget-mass-k71prf`). **Read level: grep of the w, Re and validity passages only**, not the whole file.
- Two web searches; their sources and read levels are in §6.

**My numbers:** all come from `python3 docs/research/fish/challenge-259_calc.py`, written from the stated inputs without reusing S30-D's script. **They are calculated, not observed.**

## Verdict: WEAKENED

**What holds.**
- The arithmetic is correct.
- The evidence-level complaint about S30's input is fair.
- The sign (upper bound) stands.

**What does not hold.**
- The ~15 J/kg figure is not an upper bound on what teleost muscle can store. It is an estimate under two assumptions, and relaxing either one moves it upward.
- The central comparison, fish ~15 against frog 53 J/kg, compares two different quantities:
  - for the fish, strain reached **in vivo during a C-start**;
  - for the frog, a **maximal isolated-preparation** measurement.
- Apply the same in-vivo-strain bound to a frog and it gives 7–21 J/kg, which is the same band as the fish (§2).
- So the claimed 3.5× gap between taxa is not established. Teleost w, and with it the existence of the window, is still undetermined.
- The "falls" verdict replaces one unverified number (39 mg) with another (0.94 mg) that is no better grounded.

## 1. Independent arithmetic (calculated)

| Quantity | My value | Claim | Agrees? |
|---|---|---|---|
| R₀ = 0.30·53·0.93·0.37/10.17 | 0.5380 | 0.538 | yes |
| m\* at w = 53 | 38.92 mg | 38.9 mg | yes |
| w = ½σ₀ε/ρ at 250 kPa, 0.13, 1060 kg m⁻³ | 15.33 J/kg | 15.3 | yes |
| low (200 kPa, 0.10) / high (300 kPa, 0.15) / ceiling (300 kPa, 0.24) | 9.43 / 21.23 / 33.96 | 9.4 / 21.2 / 34.0 | yes |
| m\* central, β = 1/3 | 0.942 mg | 0.94 mg | yes |
| one-side range (low w at β = 1/3; high w at β = 0.533) | 0.220–14.04 mg | 0.22–14 mg | yes |
| zebrafish 0.40 g / m\* | 425× (29–1822×) | 425× (29–1800×) | yes (1822 rounded to 1800) |
| Re_air at the anchor, and mass where Re_air = 700 (Re ∝ m^½) | 1806; 37.55 mg | 37.5 mg | yes |

There are no arithmetic errors. My script adds one threshold the claim does not state: the w needed for m\* to reach the 37.5 mg floor.

| β | w needed to reach the floor |
|---|---|
| 1/3 | 52.4 J/kg |
| 0.36 | 49.8 J/kg |
| 0.40 | 46.1 J/kg |
| 0.533 | 35.9 J/kg |

## 2. The proxy (the main defect)

**The quantity that matters** is the energy teleost fast muscle *could* store in a series spring in one contraction, if a spring were present. S30's hypothetical spring-launched fish needs exactly that.

**The proxy S30-D used** is the fibre strain teleosts *do* reach in a C-start, with no spring present. Myotomal geometry ("gearing") and body curvature set that strain, not the muscle's capacity. S30-D's own §3.2 caveat and honesty ledger say this assumption is load-bearing. The claim sentence does not carry that caveat, and calls the result an "upper bound".

**Calibration test (my inference, from search-summary sources).** If in-vivo strain is a fair proxy for spring-loading capacity, it should reproduce the frog value in a frog.
- Astley & Roberts (*Rana pipiens*, X-ray cinefluoroscopy) report plantaris fascicle shortening of 7.8 % before joint movement, which is the tendon-loading phase, and 14.6 ± 5.6 % in total. **Read level: search-summary.**
- Putting those strains into the same bound, ½σ₀ε/ρ at 200–300 kPa, gives (calculated):
  - **7.4–11.0 J/kg** for the loading phase;
  - **13.8–20.7 J/kg** for total shortening.
- Mendoza & Azizi's isolated-preparation frog values are 22 / 37 / 53 J/kg (per S30-D's full-text read).
- So **the in-vivo-strain method underestimates the frog's isolated-preparation spring-loading by roughly 2–7×**.
- Measured the same way, frog and fish land in the **same 7–21 J/kg band**.

**What that means.** The claimed fish-vs-frog gap (53 vs 15, 3.5×) may come from the protocol (maximal tetanus against a compliant load, versus behaviour in vivo), not from the taxon.

**Caveats on this test, stated in full.**
- It is cross-species (leopard frog in vivo vs Cuban tree frog, bullfrog and cane toad isolated).
- Frog σ₀ in those animals is `unknown` to me. I used the fish 200–300 kPa range.
- In vivo, muscle may not be maximally activated.

None of these caveats restores the claim's bound. Each one makes the in-vivo number a *floor* on capacity rather than a ceiling.

**Is fish muscle intrinsically limited?** Not on the filament evidence found.
- Perch fast fibres have thin filaments ~0.94 µm with thick filaments of similar length to slow fibres (Granzier et al. 1991, **search-summary**). That is an ordinary vertebrate sarcomere architecture.
- Burkholder & Lieber's cross-species survey found muscles operating across 9–90 % of L₀ (**search-summary**).
- I found no evidence that teleost fast fibres have a narrower force–length range than frog fibres. The width of the zebrafish fast-fibre force–length curve remains `unknown`. Scope of the search: one web search.

## 3. Hidden assumptions, relaxed (calculated)

### A. "A linear spring is the most favourable realistic spring" (the ½ factor)

This is not a bound on stored energy. A muscle capped at F₀ can do up to F₀·ε·L if it shortens at near-constant force. LaMSA systems approach that with prestressed springs or with latches whose mechanical advantage changes during loading.

S30-D says a J-shaped (stiffening) spring stores less than a linear one. That is true, but it does not make the linear spring an upper bound. With shape factor 1.0 instead of 0.5:

| Case | w | m\* at β = 1/3 | m\* at β = 0.533 |
|---|---|---|---|
| central | 30.7 J/kg | 7.5 mg | 28 mg |
| high | 42.5 J/kg | 20 mg | **51.5 mg** |

At the high corner with β = 0.533, m\* is above the 37.5 mg floor. **So the claim "every one-side value is below the validity floor" depends on the ½ factor.**

### B. "C-start strain caps spring-loading strain"

At 250 kPa with a linear spring:

| ε | w | m\* at β = 1/3 | m\* at β = 0.533 |
|---|---|---|---|
| 0.30 | 35.4 J/kg | 11.6 mg | 36.6 mg (at the floor) |
| 0.35 | 41.3 J/kg | 18.4 mg | **48.9 mg** |

### What survives both relaxations

At the geometric β = 1/3, no relaxation I tried with w ≤ 42.5 J/kg reaches the floor, which needs 52.4 J/kg. **"No window at β = 1/3 unless w ≳ 50 J/kg" is robust. "No window at any β in S30's bracket" is not.**

## 4. Evidence level

**The recorded evidence level is wrong.**
- It says **measured**, but the claim is **derived**: a recalculation built on an assumed proxy.
- S30-D's own header says "Status: derived… Nothing here is a measurement".
- Its σ₀ and ε inputs are **search-summary** reads, not full text.

This is a defect in the ledger record, not in S30-D's prose. The value should be recorded as **derived (conditional estimate), inputs at search-summary**.

**"Transferred without argument" is partly unfair.** S30 did not hide the transfer. Its precise statement says the window holds "only if fish muscle loads a tendon as well as frog muscle does", and its §4 names teleost w as the deciding open input. The transfer was unargued but explicitly conditional.

## 5. Counter-examples and regimes

**Teleosts with a real spring.** Syngnathid feeding LaMSA (epaxial muscle loading a tendon) is a teleost spring-loading system that exists. Per S30-D (full text of Avidan et al. 2023), no J/kg value is reported, so it neither supports nor refutes the bound. It does show that teleost epaxial muscle loads a series spring, which is exactly the regime where the C-start proxy does not apply.

**"No realisable window" vs "no window".** Below Re_air 700 there are no CL_max data. That does not mean CL_max is zero. The floor marks where the analysis loses validation, not where the physics stops. S30-D follows S30's own rule here, so this is consistent, but the claim's wording ("no realisable single-impulse window … for a fish-like animal") reads as stronger than that.

## 6. Sources and read levels

| Source | Read level | Used for |
|---|---|---|
| S30-D md and script (jb7qj4) | full-text | claim, inputs, caveats |
| S30-organism.md (k71prf) | grep of w / Re / validity passages | conditional framing, validity rule |
| Astley & Roberts, *Rana pipiens* plantaris strain ([PMC3367733](https://pmc.ncbi.nlm.nih.gov/articles/PMC3367733), [PMC2871832](https://pmc.ncbi.nlm.nih.gov/articles/PMC2871832)) | search-summary | 7.8 % pre-movement, 14.6 % total fascicle shortening |
| Granzier et al. 1991, perch fast fibre filaments ([jci.org ref](https://jci.org/references/scholar/33005/B13)) | search-summary | thin filament ~0.94 µm |
| Burkholder & Lieber operating range (via the same search) | search-summary | 9–90 % L₀ |
| Mendoza & Azizi 2021 | not re-read; values taken from S30-D's full-text read | 22 / 37 / 53 J/kg |

**Scope of the negative searches:**
- Two standard web searches: fish fast-muscle force–length; bullfrog plantaris fascicle strain.
- Not found: any isolated-preparation teleost spring-loading measurement; the width of the zebrafish fast-fibre force–length curve; frog σ₀ for the Mendoza & Azizi species; a bullfrog-specific plantaris strain from Roberts & Marsh 2003.

```swarm-challenge
{"claim_id": 259, "outcome": "weakened", "reason": "Arithmetic reproduces exactly, but the ~15 J/kg 'upper bound' is a proxy (in-vivo C-start strain, linear-spring 1/2 factor) that is not a ceiling: the same in-vivo-strain method applied to frogs gives 7-21 J/kg versus their measured 22-53, so the claimed fish-vs-frog gap is unestablished, relaxing the 1/2 factor or the strain cap lifts the high/beta=0.533 corner above the 37.5 mg floor, and the recorded evidence level 'measured' should be 'derived'.", "corrected_value": null, "depends_on": ["S30-D arithmetic and inputs (S30-deepen.md / S30-deepen_calc.py, branch jb7qj4, full-text)", "S30 crossover m* = m0*R0^(1/(beta-alpha)) with alpha=0, R0 inputs f 0.30, eta_s 0.93, eta_h 0.37, need 10.17 J/kg, m0 0.25 g", "S30 beta bracket 1/3-0.533 (Fish 1990, project-transcribed)", "37.5 mg validity floor from Re_air 700 with Re proportional to m^0.5 (S2 CL_max range)", "Mendoza & Azizi 2021 frog isolated-prep 22/37/53 J/kg muscle (via S30-D full-text read)", "Astley & Roberts Rana pipiens in-vivo plantaris fascicle shortening 7.8% pre-movement, 14.6% total (search-summary)", "teleost fast-fibre P0 200-300 kPa (search-summary, via S30-D), assumed to apply to frog for the calibration test", "Granzier et al. 1991 perch fast-fibre thin filament ~0.94 um (search-summary)", "ASSUMPTION: near-constant-force loading (shape factor 1.0) is physically reachable by a latched/prestressed LaMSA", "muscle density 1060 kg/m3 (assumed)"]}
```
