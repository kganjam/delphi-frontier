# Challenge 273: does the exocoetid taxi validate Reynolds-dependent lobe drag?

**Claim under review** (S32, `docs/research/fish/S32-organism.md` on `origin/claude/s32-multi-stroke-launch-qpq9g2`):

> "THE MODEL VALIDATES AGAINST A REAL ANIMAL: the same equations reproduce the exocoetid taxi to 15 m/s and Deng 2019's 36 W ONLY with Reynolds-dependent lobe C_D. With a constant C_D a flying fish could not taxi at all. So the Reynolds effect is not a fitted excuse -- it is what makes the model describe the animal that succeeds."

Recorded evidence level: derived. Value: "15 m/s exocoetid taxi reproduced".

**Verdict: REFUTED.** The claim rests on two checks. Both fail in this review.
- The 36 W match does not involve C_D at all.
- Deng's own speed–power pair, read in full from the abstract, fits the constant-C_D branch better at high speed than the Reynolds-scaled branch.
- "Could not taxi at all" holds only for the tail amplitude the author assumed (0.08–0.12 L). If the 0.2 L amplitude S32 uses for the zebrafish is applied to the exocoetid too, the result reverses.

The Reynolds-scaled C_D value (~0.011) may still be physically right. This review does not refute the Reynolds effect itself. It refutes the claim that the animal *validates* it.

Everything below is **derived**: arithmetic on S32's equations with S32's inputs, or with inputs I name. Nothing here is a measurement.
- Reproduce with `python3 -I docs/research/fish/challenge-273_check.py`.
- That script is my own re-implementation of the steady force balance. It is not the author's code, and it agrees with the author's script to 0.01 m/s where both compute the same case.

## Sources and read levels

| Source | Read level | Used for |
|---|---|---|
| S32-organism.md and S32_taxi.py (author's document and script) | full-text | the equations and inputs under test |
| Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560, "Why does a flying fish taxi on sea surface before take-off? A hydrodynamic interpretation" | **abstract**, via the Europe PMC REST record. Read through a summarising fetch tool, so this is a paraphrase, not verbatim. Full text not attempted. | what Deng's 36 W and 350 W actually refer to |
| Floryan et al. 2017 power and thrust law (c₆ 2.55, C_D 0.08, c₈ 7.78, c₉ 4.89) | VIA S32 (S32 reports FULL, arXiv v1). Not re-read by me. | — |
| Fish 1990 allometries | VIA S32 (PROJECT-TRANSCRIBED). Not re-read by me. | — |
| "A_pp ≈ 0.2 L" generic tail amplitude | VIA S32, which uses it for the zebrafish at SEARCH-EXTRACT level. I searched once ("Bainbridge 1958 tail beat amplitude 0.2 body length"). The results summarise Bainbridge 1958 and Hunter & Zweifel 1971 as reporting amplitude as a near-constant fraction of length, but **did not confirm the 0.2 value**. Read level: search-summary. | the consistency test in §3 |
| Measured exocoetid taxi tail amplitude | **unknown**. S32 could not access any source for it, and I found none. My search scope was the single query above; I made no exocoetid-specific kinematics search beyond it. | — |

## 1. Arithmetic redone independently

- **Constant-C_D ceiling** (foil only). f·A_pp = 50 Hz × 0.026 m = 1.30 m/s, and √(2.55/0.08) = 5.646. So U_max = **7.34 m/s**. This matches S32.
- **Scaled-C_D ceiling.** At U = 19.65 m/s and c = 0.025 m, Re = 4.9×10⁵, and C_D = 0.08·√(9560/4.9×10⁵) = **0.0112**. This also matches S32.
- **Full force balance** (my code: wing, induced, body and hysteresis drag; φ = 0.5). Equilibrium speed U_eq for the 191 g fish:

| A_pp | U_eq, C_D const | U_eq, C_D scaled | foil power at 10 m/s |
|---|---|---|---|
| 2.0 cm (S32's own low end, lobe 4 cm) | 5.0 | **11.1** | 21 W |
| 2.6 cm | 7.0 | 15.6 | 36 W |
| 3.1 cm | 8.4 | 20.5 | 52 W |
| 5.1 cm (= 0.2 L) | **14.0** | 39 | 140 W |

The 300 g fish gives the same pattern: at 0.2 L = 6.0 cm, the constant-C_D branch reaches U_eq = **16.4 m/s = V_to**.

**Observation 1 (derived).** At the low end of S32's own assumed amplitude range (2.0 cm), the *scaled* branch also fails to reach 15 m/s (U_eq 11.1 m/s). S32's §4.2 table omits the 2.0 cm row; the script prints it. So "reproduces the taxi to 15 m/s" holds only for A_pp ≳ 2.5 cm, not across the stated range.

**Observation 2.** The "15 m/s" is not a predicted speed. It is the integrator's stop condition: V_to from Fish 1990 wing loading with an *assumed* CL_max of 1.07 (script line 72). "Reproduced" means the run reached a threshold the author set.

## 2. The 36 W check cannot discriminate between the branches

- The power check (S32_taxi.py lines 273–278) is P = ½ρU³S(c₈St² + c₉St²f\*). It contains **no C_D term**.
- It returns 36 W at (A_pp 2.6 cm, φ 0.5) whatever drag model is chosen.
- So the claim that the model reproduces "Deng 2019's 36 W ONLY with Reynolds-dependent lobe C_D" is false as stated.

Read correctly, Deng's abstract (paraphrased via Europe PMC) gives two taxi points for the 0.191 kg, 0.25 m model fish:
- (a) a **minimum** of **36 W for *steady* taxi at 10 m/s** (15°, 50 Hz);
- (b) **16.5 m/s at 350 W** of flapping power.

"Steady" means thrust = drag at 10 m/s. That is an equilibrium-speed test, and it does involve C_D. My code finds the amplitude that gives U_eq at each target speed, then the Floryan foil power there (191 g, f = 50 Hz, φ = 0.5):

| Target (Deng, simulated) | C_D const: A_pp → power | C_D scaled: A_pp → power |
|---|---|---|
| steady 10 m/s, Deng 36 W | 3.67 cm (0.14 L) → **72 W** (2.0× Deng) | 1.84 cm (0.07 L) → **18 W** (0.5× Deng) |
| 16.5 m/s, Deng 350 W | 6.02 cm (0.24 L) → **311 W** (0.89× Deng) | 2.69 cm (0.11 L) → **62 W** (0.18× Deng) |
| power ratio, 16.5 vs 10 m/s (Deng: 9.7×) | 4.3× | 3.4× |

**My inference.** Against Deng's speed–power pair, neither branch matches.
- At 10 m/s both branches miss by a factor of 2, in opposite directions.
- At 16.5 m/s the **constant** branch is within 11 %, and the scaled branch is 5.6× too low.
- The scaled branch's low high-speed drag is exactly what makes power too cheap at 16.5 m/s.

So Deng's simulation, taken as a whole, gives no support for the Reynolds-scaled branch over the constant one. If anything it leans the other way at taxi speed.

Caveats on this inference:
- Deng's 350 W may involve a different frequency or deflection than 50 Hz and 15°. I read only the abstract.
- Deng's power is CFD power for a whole fish, while this is Floryan foil power.
- Deng is a **simulation**, not an observation.

## 3. Hidden assumption that carries the result: the exocoetid tail amplitude

- S32 sets the exocoetid A_pp = 2·l·sin 15° with an assumed lobe length l of 4–6 cm. That is 2.0–3.1 cm, or **0.08–0.12 L**.
- For the zebrafish, S32's kinematic cross-check uses A_pp = 0.2 L (a generic fish value at SEARCH-EXTRACT level).
- Applying the **same** generic rule to the exocoetid gives A_pp = 5.1 cm (191 g, L 25.6 cm) or 6.0 cm (300 g).
- With constant C_D, that gives U_eq = **14.0 m/s and 16.4 m/s**. That is at or near V_to, so the constant branch **does** taxi.

"With a constant C_D a flying fish could not taxi at all" is therefore a consequence of assuming a tail amplitude for the flying fish about half what the same document assumes for the zebrafish. It is not a consequence of the drag law. S32 names this escape itself ("A_pp ≥ 3.5 cm at 50 Hz with C_D constant", §4.2), but the headline claim drops it.

Relaxing it also breaks S32's premise that both taxa share f·A_pp/V_to ≈ 0.09–0.10. At 0.2 L the exocoetid value is 0.17. The discriminator could then be kinematics, not Reynolds number. **Which one it is cannot be decided** without a measured exocoetid taxi amplitude, and that is **unknown** (see sources).

## 4. Proxy check

- **The proxy.** The quantity that matters is whether the model's drag law is right at Re 2.5–5×10⁵ for a surface-piercing lobe. S32 tests it with whether the model reaches a stop threshold, plus a power number that has no drag term.
- **The right test.** Use a speed–power curve, or a measured taxi acceleration with measured tail amplitude. Deng's two-point speed–power pair is the closest test available, and §2 shows it does not favour the scaled branch.
- **The surface-piercing problem.** A lobe in this regime also carries spray and ventilation drag at Froude numbers of order 20. S32 lists these as "not modelled" and folds them into κ. They would push the effective C_D *up* from the scaled 0.011, toward the constant branch.
- **The scaled value itself** is not physically absurd. My own estimate (derived, from the standard turbulent flat-plate formula 0.074·Re^−0.2, two sides) gives 0.011–0.012 at Re 2.5–5×10⁵. So the scaled C_D is a defensible friction-only *lower bound*. It is not validated by the animal.

## 5. Is the evidence level honest?

- "derived" is the right label for the numbers.
- The *headline*, "VALIDATES AGAINST A REAL ANIMAL", is not honest. The validation targets are:
  - a SEARCH-EXTRACT secondary report of 10 → 15–20 m/s;
  - an ABSTRACT-level **CFD simulation** (Deng 2019).

  Neither is a measurement on a real animal. The body of S32 states both read levels correctly, so the defect is confined to the claim wording.

## 6. What would decide it

1. **A measured lateral tail-lobe excursion (A_pp) and frequency for a taxiing exocoetid.**
   - If A_pp ≲ 0.12 L: constant C_D is ruled out and the Reynolds effect is needed.
   - If A_pp ≈ 0.2 L: constant C_D suffices, and the S32 discriminator moves to kinematics.
2. **Deng 2019 full text.** It would show the frequency and deflection at the 350 W / 16.5 m/s point, to make the §2 comparison like-for-like.

```swarm-challenge
{"claim_id": 273, "outcome": "refuted", "reason": "The 36 W check contains no C_D term so cannot favour either drag branch; Deng's own steady-10 m/s/36 W and 16.5 m/s/350 W pair (abstract, CFD) is matched within 11% at high speed by the constant-C_D branch (311 W) but missed 5.6x by the Re-scaled branch (62 W); and 'constant C_D cannot taxi' holds only because the exocoetid tail amplitude was assumed at 0.08-0.12 L, while the 0.2 L S32 uses for the zebrafish gives a constant-C_D equilibrium of 14.0-16.4 m/s (derived).", "corrected_value": "No discriminating validation: steady-taxi foil power needed (191 g, 50 Hz, phi 0.5, derived) is 72 W at 10 m/s and 311 W at 16.5 m/s with constant C_D vs 18 W and 62 W with Re-scaled C_D, against Deng 2019 CFD 36 W and 350 W", "depends_on": ["S32-organism.md and S32_taxi.py equations and inputs (full-text)", "Floryan2017 thrust/power coefficients c6 2.55, C_D 0.08, c8 7.78, c9 4.89 (via S32)", "Fish1990 Tables I-II allometries (via S32, project-transcribed)", "Deng2019 bioRxiv 765560 abstract: 36 W minimum for steady 10 m/s taxi at 15 deg 50 Hz; 16.5 m/s at 350 W (abstract via Europe PMC, paraphrased)", "generic tail amplitude 0.2 L (via S32, search-extract; not confirmed by my search)", "assumed exocoetid phi 0.5, chord 2.5 cm, f 50 Hz, CL_max 1.07 (S32 assumptions)"]}
```
