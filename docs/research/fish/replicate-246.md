# Replicate 246: second independent re-derivation of the S28 ascent-deceleration number (claim 194 / replicate-194)

**Status: calculation on stated inputs. Nothing here is a measurement.** Script:
`docs/research/fish/replicate-246-scripts/r246.py` (point-mass integration, dt = 1 µs).

## Contamination disclosure (read this first)

- The question was given as "Replication", with `replicate-194.md` on branch
  `claude/replicate-194-rederivation-12i93y` named as where the inputs live.
- Before deriving, **I saw the commit message of that branch**. `git show --stat` printed it. It states:
  "lift ratios (10 % W exit, 5 % W apex) replicate; … the vertical net is ~6 % at a 45-degree climb". So I
  knew replicate-194's headline before I derived anything. My derivation is therefore **not blind to the
  recorded value**. Weigh any agreement below with that in mind.
- From `replicate-194.md` I then read only lines 1–20 (its question statement) before deriving. They contain
  S28's claim with digits masked.
- From the S28 source (`docs/research/fish/S28-organism.md`, branch `claude/s28-organism-design-5z0vjz`)
  I read §1 inputs and §2 geometry in full, which include case C (S = 192 mm²). I read §3.2 and the
  prediction/summary lines with digits masked (`sed 's/[0-9]/#/g'`). The quantity, from the masked text:
  *"the effective downward acceleration during the ascent is reduced by about #–## % (lift ## % at exit,
  # % at apex) if the fish spreads its pectorals."*
- I read the rest of `replicate-194.md` only after my numbers below were computed.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| g, ρ_air | 9.81 m s⁻², 1.225 kg m⁻³ | constants (S28 §1) | full-text (project file) |
| Body mass m | 0.25 g → W = 2.4525e-3 N | S28 §1, marked **assumed, back-solved** | full-text (project file); primary: none exists |
| CL | 1.07 | S28 §1, "derived (project)" | full-text (project file); not re-derived |
| Wing area S | 192 mm² (case C, headline); 125 (B), 57 (A) | S28 §2.2. **None of these is measured.** S28 says fin area was never measured | full-text (project file) |
| Exit speed V₀ | 1.38 m/s (top), 0.45 m/s (bottom) | S28 §1 cites "Miln et al. 2021, n = 50" for *swimming burst* speed. **I did not attempt to access Miln et al. 2021**, so it is unverified by me. Using it as water-exit speed is an assumption | listing (project table); primary not attempted |
| Launch angle θ | 45° (also 30°, 60°) | **my assumption** (range-optimal ballistic). S28 optimises angle, but its value was masked | — |
| Wing CD/CL | 0 (lift-only) and 0.17 | **my assumption**: CD0 ≈ 0.1 at Re ≈ 600 plus induced CL²/(π·0.9·5) = 0.081, so CD ≈ 0.18 and CD/CL ≈ 0.17 | — |
| Body drag | excluded | Wild type has the same body drag, so it is not part of the fin-attributable *reduction* | — |

No primary literature was read for this note. The scope of that negative: I made no web or PMC fetches. Every
number traces to the project file or to my own stated assumptions.

## Arithmetic

V_to = √(2W/(ρ S CL)) = √(2·2.4525e-3 / (1.225·192e-6·1.07)) = √(4.905e-3 / 2.5166e-4) = √19.49 = **4.415 m/s**.

Lift magnitude: L/W = (V/V_to)².
- At exit: (1.38/4.415)² = 1.9044/19.49 = **9.77 %** (S28's V_to = 4.37 gives 9.97 %).

Lift is normal to the path. With path angle γ and horizontal speed u = V cos γ, the vertical lift is
L_z/W = (V²/V_to²)·cos γ = u·V / V_to².
- **Exit**, 45°: u = 0.976 m/s, so 0.976·1.38/19.49 = **6.9 %**.
- **Apex**, analytic with u held constant: u²/V_to² = 0.952/19.49 = **4.9 %**. The integration gives
  **4.6 %**, because the backward component of lift slows u during the climb.
- **Time-mean over the ascent**, analytic: w falls linearly in t, so mean V = u·mean√(1+x²) over [0,1].
  That is u·(√2 + asinh 1)/2 = 0.976·1.148 = 1.120 m/s, so mean L_z/W = 0.976·1.120/19.49 = **5.6 %**.
  The integration gives **5.40 %**.
- **Wing drag** adds a downward component D sin γ = W(V w/V_to²)(CD/CL) while climbing. Its time-mean is
  u²·(2^{3/2} − 1)/3 / V_to² × 0.17 = 0.581/19.49 × 0.17 ≈ **0.5 %**. Net (integration): **4.85 %**.

Script output (simulated, case C, V₀ = 1.38 m/s):

| θ | exit L/W | apex L/W | mean vertical lift | mean net incl. wing drag |
|---|---|---|---|---|
| 30° | 9.77 % | 7.12 % | 7.58 % | 7.13 % |
| 45° | 9.77 % | 4.58 % | **5.40 %** | **4.85 %** |
| 60° | 9.77 % | 2.17 % | 3.17 % | 2.59 % |

Sensitivity at 45°, mean net:
- Case B: 3.2 %. Case A: 1.5 %.
- V₀ = 0.45 m/s: 0.5 % (case C).
- m = 0.40 g: multiply every result by 0.625.

## My value

**Fin-attributable reduction in effective downward acceleration during the ascent of a 45° leap, case-C wing
(192 mm², unmeasured), 0.25 g, V₀ = 1.38 m/s: ≈ 5 % of g.**
- The time-mean is 5.4 % from lift alone and 4.9 % net of wing drag.
- The instantaneous value runs from 6.9 % at exit to 4.6 % at the apex.
- Uncertainty: ±1 percentage point from launch angle (30–60° gives 2.6–7.1 %) and from the wing-drag assumption.
  On top of that, the input conditionals dominate: S scales the result linearly and is unmeasured, V₀ enters
  squared and is unverified as an exit speed, and m enters inversely and is assumed.
- For case A (closest to what *longfin* is known to do), the value is ≈ 1.5 %. At the bottom of the burst
  range it is < 1 %.

The raw lift ratios are 9.8 % W at exit and 4.6–4.9 % W at apex. These match S28's masked "## % at exit,
# % at apex" pattern as 10 % and 5 %. That is my inference: the digits I saw later confirm 10 and 5.

## Comparison with the recorded value

Recorded (replicate-194, read after deriving): "≈ 5–6 % of g net vertical reduction during ascent of a
45-degree leap (lift/W 10 % at exit, 5 % at apex), only for S ≈ 196 mm², 0.25 g, 1.38 m/s; ≈ 1–3 % for 40–80 mm²
fins". Its verdict on S28's "5–10 %" is DISAGREE on the upper end.

- **Lift ratios: AGREE.** Mine are 9.8 % / 4.6–4.9 %; theirs are 10 % / 5 %. The difference comes from S = 192 vs 196 mm² and
  from my including the slowdown of u.
- **Net vertical reduction: AGREE within uncertainty, with a small preserved difference.** Replicate-194
  reports instantaneous values: 5.9 % at exit (with wing drag, CD0 0.08) and 5.0 % at apex. I report a
  time-mean over the ascent: 4.9 % net (5.4 % lift-only). My apex is 4.6 %, not 5.0 %, because the backward
  lift component decelerates u. So my central value sits at the low edge of their 5–6 %, not in its middle.
- **On S28's "5–10 %": AGREE with replicate-194 that the 10 % end is not supported.** 10 % is the full lift
  magnitude at exit, not its vertical component. No point in the ascent of a ≥ 30° leap reaches more than about 8.5 % vertical
  (30°, exit). This is my calculation.
- **Conditionality: AGREE.** Both derivations depend on the unmeasured case-C area. Neither applies to a
  measured Daane fin.

Verdict: **AGREE** with replicate-194's value (≈ 5–6 % of g; mine ≈ 5 %). The caveat is that I saw their headline
in a commit message before deriving, so this is weaker evidence than a blind agreement.

```swarm-replication
{"claim_id": 246, "my_value": "~5 % of g (time-mean 5.4 % lift-only, 4.9 % net of wing drag; 6.9 % at exit to 4.6 % at apex) for a 45-degree leap, case-C 192 mm2 unmeasured wing, 0.25 g, 1.38 m/s; ~1.5 % for case A; <1 % at 0.45 m/s", "agrees": true,
  "note": "Agrees with replicate-194's ~5-6 % net vertical reduction (and that S28's 10 % upper end is a lift-magnitude proxy), though my time-averaged value sits at its low edge and I had seen its headline in a commit message before deriving."}
```
