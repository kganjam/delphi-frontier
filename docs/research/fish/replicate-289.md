# Replication 289: does the S32 model "validate against a real animal"?

**Claim under test** (S32, `docs/research/fish/S32-organism.md` on `origin/claude/s32-multi-stroke-launch-qpq9g2`, read in full):

> "THE MODEL VALIDATES AGAINST A REAL ANIMAL: the same equations reproduce the exocoetid taxi to 15 m/s and Deng 2019's 36 W ONLY with Reynolds-dependent lobe C_D. With a constant C_D a flying fish could not taxi at all."

Two challengers (`claude/challenge-273-exocoetid-taxi-hid0nd`, `claude/challenge-273-exocoetid-taxi-x5n6z2`) refuted this claim. My job was to re-derive the result without their working.

**Contamination disclosure.**
- To find where the claim lived, I read the first 25 lines of hid0nd's `challenge-273.md`. Those lines contain its verdict and three bullet reasons. I then stopped reading it.
- I did not open hid0nd's script, or either file on x5n6z2. I saw only x5n6z2's commit subject, which says "refute".
- So this derivation is independent in its arithmetic. It is **not** blind to hid0nd's headline conclusion.

**Everything below is calculated, not observed.** It is the author's steady force balance, re-implemented by me in `docs/research/fish/replicate-289.py` (run with `python3 -I docs/research/fish/replicate-289.py`) and fed the author's inputs or inputs I name. The only external number that is not the author's is Deng 2019's abstract, and Deng's numbers are themselves CFD (simulated), not measurements of an animal.

## My value

**The claim does not hold.** On the claim's own equations:
1. The 36 W match cannot tell the two C_D branches apart. The power law has no C_D term, so both branches give **36.3 W**.
2. Deng reports 10 m/s at 36 W as a *steady state*. Neither branch is steady there at the author's kinematics:
   - scaled C_D: net **+0.55 N**, so the fish accelerates, to U_eq 15.6 m/s;
   - constant C_D: net **−1.10 N**, so it decelerates, to 7.0 m/s.
3. If I force a steady state at 10 m/s and 50 Hz instead, the predicted power is off by about a factor of 2 in both branches, in opposite directions:
   - constant C_D: **72 W** (A_pp 3.67 cm);
   - scaled C_D: **18 W** (A_pp 1.84 cm).
4. Deng's second pair, 350 W for 16.5 m/s, fits the **constant** branch (**324–339 W**). The scaled branch gives **62–63 W**, 5.6× too low. This holds across A_pp 2.0–3.1 cm.
5. "Could not taxi at all" holds only for the assumed amplitude. With constant C_D at 50 Hz:
   - A_pp 5.0 cm (0.2 L) gives U_eq **13.6 m/s**;
   - A_pp 6.0 cm (0.24 L) gives U_eq **16.5 m/s**, above V_to (15.0 m/s).
6. "Reproduces the taxi to 15 m/s" is partly a matter of construction. 15.0 m/s is the model's own V_to, computed with an *assumed* CL_max of 1.07, and it is where the integration stops. The animal number it stands in for, "taxi to 15–20 m/s", is a search-engine extract that S32 carries as SEARCH-EXTRACT.

**Uncertainty.**
- The model inputs φ (0.5), lobe chord (2.5 cm), A_pp (2.0–3.1 cm) and CL_max (1.07) are all assumed by S32.
- Deng's abstract does not give the deflection or frequency behind the 350 W / 16.5 m/s case, so I cannot be sure that point is comparable with the 50 Hz runs.
- Result 4 holds for every A_pp in the tested range, and in that range the conclusion does not depend on the frequency chosen. It is still a model-to-CFD comparison, not a model-to-animal one.

## Inputs, sources and read levels

| Input | Value | Source | Read level |
|---|---|---|---|
| Equations, constants, exocoetid geometry, kinematics | as coded | S32_taxi.py and S32-organism.md (author) | full-text |
| Floryan 2017 thrust law c₆ 2.55, C_D 0.08, Re 4,780–9,560; power law c₈ 7.78, c₉ 4.89 | — | taken from the author's script. I did not read Floryan myself | listing, via the author. Not independently verified |
| Fish 1990 allometries: WL = 285.0·M^0.400, hypocaudal area 0.003·M^0.650 | — | the author's project transcription | listing, via the author |
| Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560 | 0.25 m, 0.191 kg; taxi steady state at 10 m/s needs a minimum of 36 W at 15° and 50 Hz; 350 W gives 16.5 m/s; underwater cruise at 10 m/s needs 350 W at 10° and 145 Hz | Europe PMC REST `search?query=DOI:10.1101/765560&resultType=core` | **abstract, verbatim** (JSON field `abstractText`). Full text not attempted |
| Exocoetid exit ~10 m/s, taxi to 15–20 m/s | — | S32 via S30 | search-summary (second-hand). Not re-checked |

No measurement of flying-fish taxi kinematics, thrust or power was read. My search was limited to the S32 sources plus the Deng abstract, so I make no claim about the wider literature.

## Arithmetic

Exocoetid case, M = 0.191 kg:
- 0.191^0.65 = e^(0.65 × ln 0.191) = e^(0.65 × −1.6555) = e^(−1.0761) = 0.3409.
- S_hypo = 0.003 × 0.3409 = 1.023 × 10⁻³ m².
- S_imm = φ · S_hypo = 0.5 × 1.023 × 10⁻³ = **5.11 × 10⁻⁴ m²**.
- WL = 285.0 × 0.191^0.4 = 147.0 N/m², so S_w = M·g / WL = 0.01275 m².
- V_to = √(2W / (ρ_a S_w CL_max)) = **14.98 m/s**.

**Power (no C_D term).** At A_pp 2.6 cm, f 50 Hz, U 10 m/s, chord 2.5 cm:
- St = 50 × 0.026 / 10 = 0.13;
- f* = 50 × 0.025 / 10 = 0.125;
- C_P = 7.78 × 0.0169 + 4.89 × 0.0169 × 0.125 = 0.1315 + 0.0103 = 0.1418;
- P = ½ × 1000 × 10³ × 5.11 × 10⁻⁴ × 0.1418 = **36.3 W**, in either branch.

**Foil-only ceiling.** U_max = f·A_pp·√(c₆ / C_D).
- Constant C_D, A_pp 2.6 cm: 1.30 × √(2.55 / 0.08) = 1.30 × 5.646 = 7.34 m/s. The full model, with the other drag terms, gives 6.95 m/s.
- To reach V_to with the foil alone needs f·A_pp ≥ 15.0 / 5.646 = 2.65 m/s, that is A_pp ≥ 5.3 cm at 50 Hz. The full model gives 16.5 m/s at 6.0 cm.

**Full force balance**, net = T − D_wing − D_body − D_ind − F_σ,h, with cosθ 1 and Δcosθ 0.3 as in S32:

| Case | Constant C_D | Scaled C_D (Re^−½ above 9,560) |
|---|---|---|
| Net at 10 m/s, A_pp 2.6 cm | −1.098 N; U_eq 6.95 m/s | +0.547 N; U_eq 15.58 m/s |
| Net at 10 m/s, A_pp 3.1 cm | −0.634 N; U_eq 8.40 m/s | +1.012 N; U_eq 20.53 m/s |
| A_pp for steady state at 10 m/s, 50 Hz | 3.67 cm, giving **72.4 W** | 1.84 cm, giving **18.3 W** |
| f for U_eq = 16.5 m/s, A_pp 2.0 cm | 150 Hz, giving **339 W** | 67 Hz, giving **63 W** |
| f for U_eq = 16.5 m/s, A_pp 2.6 cm | 116 Hz, giving **330 W** | 52 Hz, giving **62 W** |
| f for U_eq = 16.5 m/s, A_pp 3.1 cm | 97 Hz, giving **324 W** | 43 Hz, giving **62 W** |

The 2.6 cm and 3.1 cm net-force rows match the author's §4.2 table (−1.10 N and +0.55 N at 2.6 cm; +1.01 N at 3.1 cm), so my re-implementation reproduces the author's equations.

The comparison with Deng's 350 W / 16.5 m/s pair:
- constant C_D: 324–339 W against 350 W, a ratio of 0.93–0.97;
- scaled C_D: 62–63 W against 350 W, a ratio of 0.18.

**My inference, not the author's claim and not Deng's.** Deng's two simulated points pull in opposite directions:
- the 10 m/s steady state sits between the two branches;
- the 16.5 m/s / 350 W point favours constant C_D.

Neither point singles out the Reynolds-scaled branch. And because both points are CFD results, neither is "a real animal".

## Comparison with the recorded value

The recorded value is S32's "15 m/s exocoetid taxi reproduced", which the claim offers as validation. The challengers' recorded outcome is REFUTED. From hid0nd's header, which I saw before deriving, its reasons are:
- the 36 W match does not involve C_D;
- Deng's high-speed pair fits the constant branch better;
- the result reverses at a 0.2 L amplitude.

I derived all three independently and got the same direction on each. I also add two points: the 10 m/s steady-state test fails in both branches, and the 15 m/s figure is the model's own V_to.

**AGREE** with the refutation. I **DISAGREE** with S32's claim that the model validates against a real animal.

This agreement is weaker than a fully blind one, because I saw hid0nd's headline reasons before I derived mine. I did not compare against hid0nd's or x5n6z2's numbers.

```swarm-replication
{"claim_id": 289, "my_value": "claim not supported: 36 W match is C_D-independent (36.3 W in both branches); Deng 350 W @ 16.5 m/s fits constant C_D (324-339 W) not scaled (62-63 W); constant C_D reaches 13.6-16.5 m/s at A_pp 5-6 cm (V_to 15.0 m/s)", "agrees": true,
  "note": "Independent re-implementation of S32's force balance reproduces the author's net forces and agrees with the challengers' refutation, but I saw hid0nd's headline verdict before deriving, and Deng's figures are CFD, not animal observations."}
```
