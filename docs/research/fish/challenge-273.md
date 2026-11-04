# Challenge 273: does the S32 exocoetid taxi really validate the Reynolds-dependent lobe C_D?

**Claim under review** (S32-organism.md, branch `claude/s32-multi-stroke-launch-qpq9g2` @ `c1b761eb`, §4.2 and the swarm-result block):

> "THE MODEL VALIDATES AGAINST A REAL ANIMAL: the same equations reproduce the exocoetid taxi to 15 m/s and Deng 2019's 36 W ONLY with Reynolds-dependent lobe C_D. With a constant C_D a flying fish could not taxi at all. So the Reynolds effect is not a fitted excuse -- it is what makes the model describe the animal that succeeds."

Recorded evidence level: derived. Value: "15 m/s exocoetid taxi reproduced".

**Verdict: REFUTED** as worded. The 15 m/s integration reproduces when re-run. But the claim's three load-bearing parts fail:

1. **The "ONLY with Re-dependent C_D" for Deng's 36 W.** The 36 W cross-check uses Floryan's *power* law (c₈, c₉), which contains no C_D. It comes out the same in both branches. Read the way Deng states it (the power for **steady** taxi at 10 m/s), neither branch reproduces it.
2. **Deng's second number.** Deng's other abstract number (350 W → 16.5 m/s) is matched by the **constant**-C_D branch (311 W). The scaled branch gives 62 W, 5.6× too low.
3. **The extrapolation.** The Re-dependent branch that "succeeds" scales Floryan's *whole* residual drag as laminar friction (Re^−½) out 26–43× beyond the measured Re. If the friction part alone is scaled and the form part is held constant, the flying fish again cannot taxi (ceiling 8–9 m/s).

Everything below is **derived** (calculation). Nothing here is a measurement. Script: `docs/research/fish/challenge-273.py`. I reimplemented it from the equations as printed in S32 §1; it does not import `S32_taxi.py`. Run with `python3 docs/research/fish/challenge-273.py`.

## Sources and read levels

| Source | Used for | Read level |
|---|---|---|
| S32-organism.md and S32_taxi.py (`c1b761eb`) | The claim, its equations and inputs | full-text (re-ran the script) |
| Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560 | 36 W steady taxi at 10 m/s, 15°, 50 Hz; 350 W → 16.5 m/s. **CFD, simulated, not an observation** | abstract (fetched biorxiv.org this session). Full text not read |
| Floryan et al. 2017 (c₆ 2.55, C_D 0.08, c₈ 7.78, c₉ 4.89; Re 4,780–9,560) | Thrust and power laws | **inherited from S32 as quoted.** I did not re-read the paper |
| Fish 1990 Tables I–II allometries | Hypocaudal area, wing loading | inherited from S32 (PROJECT-TRANSCRIBED there) |
| Wang (H.-P.), APS March Meeting 2024, S27.13, "Flying fish taxiing on the water's surface" | Taxi tail slapping ≈ **13.5 Hz**; ≈ 2 N tail force to sustain a 200 g fish | **search-summary only.** meetings-archive.aps.org and meetings.aps.org do not resolve from this session (network policy), so the abstract text was not read |

## 1. Arithmetic redone independently

Inputs are S32's: M 191 g, φ 0.5, chord 2.5 cm, 50 Hz, CL_max 1.07, Fish 1990 fits.
- **Geometry.** S_w 127.5 cm², S_hypo 10.23 cm², S_imm 5.11 cm², V_to 14.98 m/s, W 1.874 N. These agree with S32.
- **Re.** 2.5×10⁵ at 10 m/s and 3.75×10⁵ at 15 m/s.
- **Ceiling by hand.** U_max = f·A_pp·√(c₆/C_D) at A_pp 2.6 cm:
  - 7.34 m/s at C_D 0.08 (const);
  - 19.6 m/s at C_D 0.0112 (S32's scaled value at the ceiling).
  - These agree with S32 §4.1.
- **Laminar extrapolation at 10 m/s.** 0.08·√(9560/2.5×10⁵) = **0.0156**. S32's "0.010–0.011" is the value at the ~20–25 m/s ceiling, not at taxi speeds.
- **Integration (scaled, A_pp 2.6 cm).** Reaches 14.98 m/s after **4.42 s, 59.3 m, 221 strokes**. This matches S32. Two limits on that "reproduction":
  - The margin is thin: U_eq 15.6 against V_to 15.0, so 4 % headroom.
  - It **fails** in S32's own runs at A_pp 2.0 cm (U_eq 11.1) and for the 300 g fish at A_pp 2.6 cm (U_eq 15.4 < V_to 16.4).
  - The 15 m/s target is itself derived, from an assumed CL_max of 1.07.
- **Power check.** P = ½ρU³S·(c₈+c₉f\*)·St² at A_pp 2.59 cm gives 36 W. This agrees with S32, and **C_D does not appear in it**.

## 2. Proxy: "matches 36 W" stands in for "matches steady taxi at 10 m/s"

Deng's abstract wording is "the minimum power required for a stead[y]-state locomotion at 10 m s⁻¹ is 36 W". So the quantity to test is **net force = 0 at 10 m/s when the stroke absorbs 36 W**. Equal power is only a proxy for it. Running the same equations on that test (derived):

| Test (Deng, abstract, CFD) | const C_D 0.08 | scaled C_D (Re^−½) | C_D the model needs |
|---|---|---|---|
| Net force at 10 m/s with the 36 W kinematics | −1.11 N (decelerates) | **+0.54 N (accelerates: not steady)** | **0.037** |
| Power the model needs for steady 10 m/s (Deng: 36 W) | 72 W (2.0× high) | 18 W (2.0× low) | — |
| Power the model needs for steady 16.5 m/s (Deng: 350 W) | **311 W (−11 %)** | **62 W (5.6× low)** | **0.091** |

**Reading it (my inference).**
- Deng's low point falls between the two branches.
- Deng's high point favours the **constant** branch.
- No single extrapolation fits both points. The implied C_D rises with speed (0.037 → 0.091), the opposite of the claimed Re trend.
- Deng's CFD runs at the animal's own Re. If it is taken as the reference, as S32 itself does, then it **contradicts** the claim that the Re-scaled C_D is what makes the model fit the animal.

**Caveats.**
- These rest on an abstract: Deng's immersed area, lobe shape and the kinematics at 350 W are unknown to me.
- I read "can reach 16.5 m/s" as steady at 16.5 m/s.
- I assumed 50 Hz at 350 W. At 50 Hz and 15°, 350 W needs A_pp 6.4 cm, which is a 12 cm lobe, so Deng's run probably changed frequency or angle. That makes this point weaker than the 36 W one.

## 3. Hidden assumption that carries the result: Re^−½ applied to the *whole* residual C_D

Floryan's 0.08 is the net residual drag of a thick teardrop foil.
- At Re 7,000, two-sided Blasius friction is only 2.656/√7000 = **0.032**, so about 60 % of the 0.08 is pressure/form drag.
- Form drag does not fall as Re^−½.

**Relaxed version.** Scale only the friction part and hold the form part constant (derived):

| Friction model | Form part | C_D at 10 m/s | Ceiling (A_pp 2.6 cm) | Net force at 10 m/s |
|---|---|---|---|---|
| Laminar Blasius | 0.048 | 0.054 | 9.0 m/s | −0.42 N |
| Turbulent 0.074·Re^−0.2 | 0.055 | 0.067 | 8.0 m/s | −0.77 N |

Under either, the exocoetid **cannot** taxi from 10 m/s at S32's assumed kinematics. The "success" therefore depends on choosing the most optimistic of the available extrapolations. The claim's line "not a fitted excuse" holds only in a narrow sense: no number was tuned. But the **functional form** of the extrapolation was chosen, and that choice decides the outcome.

## 4. Counter-example the author missed: taxi tail-beat frequency

The APS 2024 abstract (search-summary only, not read) reports taxi tail slapping at about **13.5 Hz**. S32 uses Deng's CFD optimum of 50 Hz. Results at 13.5 Hz (derived):
- At A_pp 2.6 cm the ceiling is 4.5 m/s (scaled) or 2.0 m/s (const). Both branches fail.
- Reaching V_to needs A_pp of **7.9 cm (scaled)** or **19.6 cm (const)**.

If 13.5 Hz is correct for real taxiing, the attribution moves back onto kinematics: amplitude and slapping mode. Slapping is also a different thrust mechanism from Floryan's submerged pitching foil. S32 §4.2 names this as "the one escape", and this source points toward it. **It is unverified until the abstract text is read.**

## 5. Evidence-level and wording defects

- **"Validates against a real animal".** Neither target is an animal measurement.
  - The 10 → 15–20 m/s taxi is SEARCH-EXTRACT in S32's own table.
  - The 36 W is a CFD simulation, read at abstract level.
  - What was actually done is a consistency check against a secondary report and a simulation. The recorded level "derived" is honest; the claim sentence is not.
- **"Could not taxi at all" with constant C_D.** At S32's assumed A_pp of ≤ 3.1 cm the fish decelerates (10 → 7–8.4 m/s). That is a statement about the assumed kinematics. My run gives:
  - net force > 0 at 10 m/s needs A_pp ≥ 3.7 cm;
  - a ceiling ≥ V_to needs ≥ 5.3 cm (foil alone).
- **"ONLY with Re-dependent C_D" for 36 W.** False by construction, because the power check is independent of C_D (§1).

## 6. What survives

- The arithmetic is correct and reproducible.
- With the laminar-scaled C_D and A_pp ≥ 2.6 cm at 50 Hz, the 191 g model does reach 15 m/s.
- It is fair to say that constant C_D 0.08 plus S32's assumed exocoetid kinematics gives deceleration.

What does **not** survive is the inference from these to "the Re effect is the operative mechanism, validated by the animal". The only quantitative reference at the animal's Re (Deng's CFD, abstract) does not favour the Re-scaled branch. And the only reported taxi frequency (APS 2024, search-summary) undercuts the kinematics that both branches assume.

## Negative searches (scope)

- **Measured exocoetid taxi duration, distance or tail amplitude.** One standard web search plus S32's own attempts. Nothing found beyond popular sources and the "400 m in 30 s by repeated taxiing" figure cited secondhand in Deng's preprint.
- **APS 2024 abstract text.** Two hosts tried; both blocked by the session's network policy.
- **Deng 2019 full text.** Not attempted beyond the abstract page.

```swarm-challenge
{"claim_id": 273, "outcome": "refuted", "reason": "The 36 W check is C_D-independent and, read as Deng's steady-state condition, matches neither branch (model needs C_D 0.037), Deng's 350 W -> 16.5 m/s point is matched by constant C_D (311 W) not the Re-scaled one (62 W), and scaling only the friction part of Floryan's C_D (form held constant) leaves the exocoetid unable to taxi (ceiling 8-9 m/s), so the Re effect is an assumed extrapolation form, not something the animal validates.", "corrected_value": "C_D implied by Deng 2019 steady-taxi CFD in the S32 equations: 0.037 at 10 m/s, 0.091 at 16.5 m/s (vs Re-scaled 0.016 / 0.012); the 15 m/s reproduction holds only for the laminar Re^-1/2 extrapolation of total C_D with A_pp >= 2.6 cm at 50 Hz", "depends_on": ["S32-organism.md and S32_taxi.py @ c1b761eb (equations, exocoetid inputs)", "Deng2019-taxi-CFD bioRxiv 765560 abstract: 36 W steady at 10 m/s, 350 W -> 16.5 m/s", "Floryan2017-foil-scaling c6 2.55, C_D 0.08, c8 7.78, c9 4.89 as quoted by S32 (not re-read)", "Fish1990-tables allometries as transcribed by S32", "Blasius / 0.074 Re^-0.2 flat-plate friction split of Floryan C_D (my assumption)", "Wang APS MAR24 S27.13 13.5 Hz taxi tail-slap (search-summary only; supporting, not load-bearing)"]}
```
