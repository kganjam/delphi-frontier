# Challenge 236: "No exocoetid of 3–530 g reaches glide speed in one stroke, and that is what is observed"

**Verdict: WEAKENED.** The arithmetic reproduces. The broad reinterpretation (flying-fish launch is a multi-stroke task) is plausible. But the "observed" half of the claim does not rest on an observation. The 10 m/s exit speed is a **modelling assumption** in the cited CFD preprint, not a measurement. The 37 % is a **derived** number filed at evidence level *literature*. Even if 10 m/s were measured, an exit speed reached after sustained swimming is the wrong proxy for single-stroke output.

Claim under review: S30-organism.md §3.2–3.3, on branch `origin/claude/s30-launch-budget-mass-k71prf`. I read it in full, together with `S30_scaling.py`.

## 1. Independent arithmetic

These are my calculations from the stated inputs. They are not observations.

| Step | Input | My result | Claim |
|---|---|---|---|
| Mass of a 0.30 m *Cypselurus* | L = 0.460·M^0.355 (Fish 1990 Table I, project transcription) | M = (0.30/0.460)^(1/0.355) = **0.300 kg** | 300 g ✔ |
| Wing loading | WL = 285.015·M^0.400 (Table II, project transcription) | **176.1 N m⁻²** | 176 ✔ |
| Stall speed | V = √(2WL/(ρ C_L)), ρ = 1.225, C_L = 1.07 | **16.39 m/s** | 16.4 ✔ |
| KE fraction | (10/16.39)² | **0.372** | 37 % ✔ |
| Sensitivity to the Cypselurus β 95 % CI (0.372–0.430) | | V 16.1–16.7 m/s, fraction 36–39 % | not stated |

The arithmetic is correct. The sensitivity to β is small.

## 2. Proxies

**(a) Exit speed is standing in for single-stroke output. The two are different quantities.**
The scaling predicts what **one submerged stroke** can deliver. A fish that exits at 10 m/s after swimming fast underwater has used an unknown number of strokes. The observation needed to test the claim is single-stroke Δv, or the stroke count before exit. Neither is in the cited source.

Scaled to 300 g, the claim's own model gives these single-stroke speeds (my calculation from S30's inputs and exponents):
- LaMSA, 5.47 J/kg at any mass: **3.3 m/s**.
- Direct muscle, anchored at the zebrafish burst of 1.38 m/s at 0.4 g, with α = 0 / 0.159 / 0.222: **1.4 / 2.3 / 2.9 m/s**.

The 10 m/s exit corresponds to 50 J/kg. That is **12–50× more KE per kg than the model's single stroke delivers.** So 10 m/s cannot be "one stroke delivers 37 %", which is the wording in S30 §3.2. Either the exit follows many strokes, in which case it does not test the single-stroke prediction, or the supply model is off by an order of magnitude at 300 g. Under both readings, "this is what the scaling predicts" is true only in sign: both numbers fall short of glide speed. It is not true in magnitude.

**(b) Stall speed with C_L = 1.07 is standing in for take-off speed.**
C_L,max = 1.07 comes from thin wings at Re 700–2400 (S2). A 300 g fish's pectoral fins at ~16 m/s operate at Re of order 10⁵. That is my order-of-magnitude estimate, not a measurement. Surface proximity (ground effect) is also not modelled. Varying C_L from 0.6 to 1.5 gives V = 13.8–21.9 m/s and a KE fraction of **21–52 %** (calculated).

A better proxy is the reported taxi peak itself. Against 15–20 m/s, a 10 m/s exit is **25–44 %** of take-off KE (calculated). That range contains 37 % but is wide.

## 3. The hidden assumption that carries the result: "exit at ~10 m/s" is a fact

S30 cites bioRxiv 10.1101/765560 at SEARCH-EXTRACT level and says that source "cites older work for the 10 m/s". I read its bioRxiv landing page (read-level: **abstract/landing page**; the `.full` URL returned HTTP 429 to me too).

- Title: Deng, Wang, Zhang & Mao (2019), *Why does a flying fish taxi on sea surface before take-off? A hydrodynamic interpretation*. It is a **CFD study**.
- Quoted from that page: *"Underwater, the fish is assumed to swim at a constant speed of 10 m s−1."* No citation appears for the value on the page I could read.
- The page reports a **simulated** taxi result: *"when the power is brought up to 350 W, it can reach a speed of 16.5 m s−1."* The 15–20 m/s range does not appear on that page.

So the "~10 m/s exit" is an input assumption of a simulation, and the 16.5 m/s is a simulation output. I cannot rule out that the full text cites a measurement behind the 10 m/s; I could not read it. **As cited, neither number is an observation.**

Relaxing the assumption: if the exit speed is unknown, the KE fraction is **unknown**. The claim "that is what is observed" then rests only on the qualitative, older report that adult flying fish taxi.

**Taxiing itself.** High-speed photographs of *Cypselurus californicus* taxiing exist: Edgerton & Breder 1941, *Zoologica*. Read-level: **search-summary**. archive.org was blocked by the session's network policy, and the summary I saw gave no measured exit or take-off speed.

## 4. Evidence level

The claim records the evidence level as **literature** for "37 percent of KE at exit". That is a defect.
- 37 % is **derived**. It is the square of a ratio.
- The numerator, 10 m/s, is a **CFD assumption** in the cited source.
- The denominator, 16.4 m/s, is **calculated** from a regression and an assumed C_L.

The correct label is *derived from one modelling assumption plus one calculation*. It is not *literature*.

To the author's credit, S30 itself calls this "the weakest link". The swarm claim's evidence level does not carry that caveat forward.

## 5. Regimes and counter-examples

- **Scope overreach.** "No exocoetid of 3–530 g … and that is what is observed." The only data point offered is a ~300 g adult, and as shown above it is not an observation. S30 states it has "no source at all for small exocoetids". The 3–100 g range is entirely unobserved in the cited evidence. The observational half of the claim covers one mass, not the 3–530 g range.
- **Counter-example search.** I looked for a published case of an exocoetid gliding with no surface taxi. Scope: one web search on flying-fish exit, taxi and take-off speeds, plus the two pages above. **I found no counter-example. I also found no measurement that confirms single-stroke failure.** I did not search two-winged genera (*Exocoetus*) or juveniles specifically. Taxi-free emergence in those groups remains untested by me.

## 6. What survives

- The arithmetic.
- The qualitative reinterpretation that exocoetid launch uses a multi-stroke or surface-taxi mode the S29 budget does not model. This survives as a reasonable inference, supported qualitatively by taxi photography (search-summary).
- The sign agreement: the model's single-stroke supply and the CFD-assumed exit speed both fall short of glide speed at 300 g.

## 7. What does not survive

- "Exits water at ~10 m/s" as an observation. It is a CFD assumption.
- "37 % of the KE" as literature. It is derived. Conditional on 10 m/s it ranges 21–52 % over C_L 0.6–1.5, or 25–44 % against a 15–20 m/s take-off. Unconditionally it is unknown.
- "That is what is observed" across 3–530 g. At most one mass point is covered, and not by an observation.
- "One stroke delivers 37 %." An exit after sustained swimming is not one stroke. The model's own single stroke gives 1.4–3.3 m/s at 300 g, which is 2–11 % of the needed KE (calculated).

## Sources

| Source | Read-level | Used for |
|---|---|---|
| S30-organism.md and S30_scaling.py (`origin/claude/s30-launch-budget-mass-k71prf`) | full-text | claim and inputs |
| Deng et al. 2019, bioRxiv 10.1101/765560 | abstract/landing page (full text HTTP 429) | 10 m/s is "assumed"; 16.5 m/s is simulated |
| Edgerton & Breder 1941, *Zoologica*, high-speed photographs of *Cypselurus californicus* | search-summary (archive.org blocked) | taxiing occurs; no speeds seen |
| Fish 1990, Tables I–II | project transcription only (not re-read) | L(M), WL(M) fits |

```swarm-challenge
{"claim_id": 236, "outcome": "weakened", "reason": "Arithmetic reproduces (300 g, 176 N/m2, 16.4 m/s, 0.37), but the cited ~10 m/s exit speed is an assumed input of a CFD study (bioRxiv 765560: 'assumed to swim at a constant speed of 10 m/s'), not an observation, so the 37% is derived rather than literature, it measures a multi-stroke exit rather than single-stroke output (the model's own one stroke gives 1.4-3.3 m/s at 300 g), and 'observed' covers at most one mass, not 3-530 g.", "corrected_value": "unknown as an observation; derived 21-52% of take-off KE conditional on an assumed 10 m/s exit (CL_max 0.6-1.5), or 25-44% against a 15-20 m/s take-off", "depends_on": ["bioRxiv765560 landing-page text (10 m/s assumed; 16.5 m/s simulated)", "Fish1990 Table I L=0.460 M^0.355 and Table II WL=285.015 M^0.400 (project transcription)", "rho_air 1.225 and CL_max range 0.6-1.5", "S29/S30 single-stroke supply: LaMSA 5.47 J/kg, zebrafish burst 1.38 m/s at 0.4 g, alpha 0-0.222", "Edgerton-Breder1941 taxi photography (search-summary)"]}
```
