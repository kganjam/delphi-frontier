# Challenge 234: adversarial review of S30's "S29 is wrong in sign" claim

**Claim under review** (S30-organism.md, branch `claude/s30-launch-budget-mass-k71prf`; recorded as *derived*, value "0.45 mass exponent beta"):
> S29's "property of size" conclusion is wrong in sign. Required specific energy scales as m^β (β 1/3 geometric, 0.36–0.53 measured in exocoetids, Fish 1990 Tables I–III). Single-stroke LaMSA supply per kg is size-independent (Sutton 2019). Since β > α, the budget closes as mass DECREASES, so the crossover is an UPPER bound.

**Verdict: WEAKENED.** The direction of the scaling argument survives under the stated assumptions. The claim as worded has four defects:
1. It leaves out the third exponent that decides the sign.
2. S30's own rebuttal of that exponent does not hold.
3. It records an exponent that is not the one carrying the result.
4. It miscounts Fish 1990's significance marks.

Everything below is my own computation (`docs/research/fish/challenge-234_check.py`) unless it is labelled as a source. Nothing in this file is a measurement.

## Sources and read levels
- **S30-organism.md and S30_scaling.py**: full-text (repository).
- **S29-organism.md**: full-text, relevant lines only (repository).
- **S28-organism.md**: full-text, relevant lines only (repository).
- **Fish 1990 Table II**: project transcription `data/fish-controls/fish1990_tables.json` on `origin/main`, full-text of the transcription. I did not read the paper itself.
- **Sutton et al. 2019**: not re-read. I rely on S30's FULL reading of it.
- **Wakeling, Kemp & Johnston 1999** (carp fast-start ontogeny): search-summary only, via one web search. The PDF was not opened.
- **van Leeuwen et al.** (larval zebrafish propulsive efficiency vs Re): search-summary only.

## 1. Arithmetic, redone independently
- **Formula:** m\* = m₀·R₀^(1/(β−α)), with m₀ = 0.25 g, need 10.17 J/kg (S29) and α = 0.
- **Ratios and crossovers:**
  - R₀ = 3.30/10.17 = 0.3245 gives m\* = 8.5 / 11.0 / 15.0 / 30.3 mg (for β = 1/3 / 0.36 / 0.40 / 0.533).
  - R₀ = 5.47/10.17 = 0.5379 gives m\* = 38.9 / 44.6 / 53.0 / 78.1 mg.
  - R₀ = 8.36/10.17 = 0.822 gives m\* = 138.9 / 145.0 / 153.2 / 173.1 mg.
  - All of these match S30's table.
- **Anchor check:** S28 back-solves 0.25 g as the mass at which 4.37 m/s is self-consistent (WL 12.5 N m⁻²), so S30's choice of m₀ is consistent with S28. (S29 attaches 4.37 m/s to a 0.4 g body, which is S29's inconsistency, not S30's. The per-kg need is mass-free at fixed V, so it does not propagate.)
- **No error in the crossover arithmetic.**

## 2. Arithmetic defect: Fish 1990 significance count
- **What S30 says:** "Four of six genera have b significantly above 0.33 (P marks as printed)."
- **What the transcription shows:** P is printed for only **three** genera: Cypselurus 0.002, Danichthyes 0.001, Hirundichthyes 0.001. Exocoetus, Fodiator and Parexocoetus are printed "ns".
- **Confidence intervals:** the 95 % CIs of Exocoetus (0.262–0.495), Fodiator (0.284–0.663) and Parexocoetus (0.257–0.649) all include 1/3.
- **Conclusion:** "three of six" is the correct count. This does not affect the sign, but it is a factual error in a measured input.

## 3. Proxy and evidence-level defects in the recorded value "0.45"
- **Where 0.45 comes from:** it appears nowhere in S30. The nearest numbers I can compute are the unweighted mean of the six genus b values (0.4435) and the N-weighted mean (0.418).
- **What β carries the result:** S30's headline m\* = 39 mg uses **β = 1/3**, not 0.45. With β = 0.45 the central crossover would be **63 mg** (my computation).
- **What the sign actually needs:** only β > α (plus γ, §4). The magnitude of β is irrelevant to the sign.
- **The measured exocoetid β is the wrong proxy for the design.** S30 scales a *fixed-shape* (isometric) zebrafish design. For that design, WL ∝ m^(1/3) is a geometric identity, not a measurement. The exocoetid excess over 1/3 comes from their negatively allometric wing area (Hirundichthyes 0.479, Danichthyes 0.485). That is a property of exocoetid ontogeny the design does not share. Quoting 0.36–0.53 as "measured" support for the design's exponent mixes a measured allometry of a different organism into a geometric argument.
- **Evidence-level fix:** the β values are **measured (by Fish 1990, project-transcribed)**. Any single "0.45" is an aggregate I can only reconstruct, not derive. The crossover and the sign are **derived**. The ledger entry should record β = 1/3 (geometric, carries the result), with exocoetid b = 0.36–0.53 (measured, three of six significant) as context.

## 4. Hidden assumption that carries the sign: the efficiency exponent γ
- **What the comparison should be:** the claim compares *stored* spring energy per kg (α = 0) with *required body KE* per kg (β). But the supply that matters is *delivered* KE: stored × η_spring × η_h × (1 − drag fraction). Stored energy is a proxy for it.
- **The true sign condition** is β − α − γ > 0, where η_h ∝ m^γ. **The claim's sentence omits γ.**
- **How S30 handles it:** S30 assigns γ "unknown, treated as 0" (§1 row 8). In §2.4 it argues that a rising η_h cannot flip the sign, because 0.37 (pike) is already used at every mass as the best case.
- **That argument treats 0.37 as a ceiling, and it is not one.** It is a single measured value (pike, Frith & Blake, abstract via S29). Physics bounds η_h only by 1. My bound on the mass-averaged γ is γ ≤ ln(1/η_small)/ln(span):

  | η_h at the small end | span 10× | span 100× | span 1000× |
  |---|---|---|---|
  | 0.37 | 0.43 | 0.22 | 0.14 |
  | 0.20 | 0.70 | 0.35 | 0.23 |
  | 0.10 | 1.00 | 0.50 | 0.33 |

- **What the table shows:**
  - Over a ~10× mass span, a γ above β = 1/3 is physically possible.
  - Over spans of ≥100× it requires η_h ≤ ~0.2 at the small end rising to ~1 at the large end.
- **A worked counter-case (my computation, hypothetical inputs):** take w = 81 J/kg muscle (S29 maximum) and assume η_h = 0.8 at 1 g. Then R(1 g) = 0.822 × (0.8/0.37) × 4^(−1/3) = **1.12**. That is a closed budget *above* the anchor mass.
- **Why the counter-case does not refute the claim:** it rests on an η_h of 0.8 for a C-start, which I found no measurement of. The only ontogenetic evidence I reached points the other way. Wakeling et al. 1999 (carp, 7–80 mm; **search-summary only**) report that their fast-start efficiency measure showed **no significant change** across ontogeny, and that performance gains came from muscle power. If that holds, γ ≈ 0.
- **Net:** the sign survives on present evidence. But it rests on γ ≈ 0, which comes from one search-summary source and one pike abstract. It does not rest on the "0.37 is best case" argument, which is invalid.

## 5. Other hidden terms tested (relaxed)
All of these are my computations.
- **C_d drift.** S30 assumes the drag fraction is mass-free. With laminar skin friction, C_d ∝ Re^(−1/2), and Re ∝ m^(1/2), so the drag fraction goes as m^(−1/4) and favours larger animals. The drag fraction rises from 6.5 % to 10.3 % at 39 mg and to 15.1 % at 8.5 mg. Re-solving gives m\* = **34.7 mg** instead of 38.9 mg. This works against the claim, but only by about 11 %, and it does not change the sign.
- **Surface energy to break the water surface,** about σ/(ρL) per kg: 0.0045 J/kg at 16 mm, 0.009 at 7.6 mm, 0.07 at 1 mm. These are negligible against ~10 J/kg, and the term matters only below about 0.1 mm.
- **Potential energy to clear the surface,** g·h per kg with h ∝ L, so ∝ m^(1/3). This has the same sign as the claim and reinforces it.
- **Fixed-fin-area scaling** (S28 §1 uses V ∝ √m at fixed fin area). This gives β = 1 and makes the claim stronger.

## 6. Does S29 actually say what is attributed to it?
- **What S29 says:** S29 line 20 states the barrier is "a property of *a single-impulse launch from water by an animal this size*". S29's verdict line says "at this size".
- **What S29 does not say:** S29 nowhere states that a *larger* animal would close the budget. It does cite Sutton's 2.5 g crossover, which puts 0.4 g "on the spring-favoured side".
- **So "wrong in sign" overstates S29.** S29 gives a scope qualifier with an implied, not stated, direction. A precise version would be: "S29's 'at this size' qualifier is misleading; within single-impulse launch at fixed shape, smaller is better (if γ ≈ 0)."

## 7. Counter-examples searched for
Scope: one web search (fast-start efficiency vs size and Re), plus the repository's S28–S30 and Fish 1990 transcription.
- **Single-stroke fish launches:** I found no published case of a fish whose *single-stroke* launch capability for gliding rises with size. **This is a negative result within that narrow scope only.**
- **Gliders smaller than ~1 g:** the absence of mg-scale fish gliders is not a counter-example. Below the empirical floor, S30's argument loses its CL_max support (Re_air < 700) and enters the low-Re regime where van Leeuwen-type results (search-summary) say propulsive efficiency falls. That is a γ > 0 regime, consistent with §4's caveat rather than refuting it.

## Corrected statement
For a geometrically similar design, required KE per kg ∝ m^(1/3) (geometric; exocoetid b 0.36–0.53 is measured context, three of six genera significant). Stored LaMSA energy per kg ∝ m⁰. The budget closes with decreasing mass, and the crossover is an upper bound, **provided the hydromechanical-efficiency exponent γ < 1/3**. γ is unmeasured. It is ≈ 0 by one search-summary ontogeny study (carp), and it is not bounded by S30's "0.37 is best case" argument. The central m\* is 39 mg at β = 1/3 (35 mg with laminar C_d drift), not a β = 0.45 figure.

```swarm-challenge
{"claim_id": 234, "outcome": "weakened", "reason": "The sign survives under stated assumptions but the claim omits the hydromechanical-efficiency exponent gamma (true condition beta-alpha-gamma>0, and S30's 'pike 0.37 is best case' rebuttal is invalid because 0.37 is not a ceiling), the result is carried by geometric beta=1/3 not the recorded 0.45 (exocoetid allometry is a proxy from a different wing-area scaling and only 3 of 6 genera, not 4, are significant), and S29 never stated a direction so 'wrong in sign' overstates it.", "corrected_value": "beta = 1/3 (geometric, dimensionless mass exponent; exocoetid measured 0.36-0.53, mean 0.44); sign condition beta - alpha - gamma > 0 with gamma unmeasured", "depends_on": ["Fish1990-tableII-transcription (data/fish-controls/fish1990_tables.json)", "Sutton2019 LaMSA alpha=0 (via S30 FULL read)", "S29 supply/need 3.30-8.36 vs 10.17 J/kg", "S28 anchor 0.25 g at 4.37 m/s", "Frith-Blake pike eta_h 0.37 (abstract via S29)", "Wakeling1999 carp ontogeny flat efficiency (search-summary)", "S29 line 20 wording"]}
```
