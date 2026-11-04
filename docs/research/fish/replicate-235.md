# Replicate 235: the body mass at which a single LaMSA impulse can launch a fish into a glide

**Claim under test:** the largest body mass m* at which one latch-mediated spring (LaMSA) impulse supplies
enough energy per kg to launch a fish into a glide, and where a 0.4 g zebrafish sits relative to m*.

**My value (calculated, not observed): m* ≈ 27 mg (central). The plausible range is 0.75 mg to 2.2 g with
geometric wing-loading scaling, and 50–570 mg with the measured-exponent variant.** A 0.4 g zebrafish is
≈ 15× above my central m*. That makes it too large for a single impulse, not too small. At the optimistic
corners of my input ranges, the sign flips.

## Contamination disclosure (read this first)

- I did not open `S30-organism.md`, any S29 file or any other derivation file. I listed only its section
  headings (`git show … | grep '^#'`) to find the question.
- **I did read the S30 commit message (59f421da) before deriving.** It names the method: required energy
  scales with wing loading (m^1/3 geometric, m^0.36–0.53 measured, citing Fish 1990); LaMSA supply per kg
  is m^0 (Sutton 2019). It also states the recorded result (39 mg, 8.5–173 mg; 0.4 g is about 10× too
  large).
- So this derivation is **not** independent in method. I chose my own inputs and anchor numbers, and did
  my own arithmetic. Count it as a check on the inputs and arithmetic, not on the framing.

## Model (my own, calculated)

A fish has to leave the water at a speed v where wing lift supports its weight:

  v² = 2 (W/S) / (ρ_air C_L,max), so the required specific energy is e_req = ½v² = (W/S) / (ρ_air C_L,max).

Wing loading scales as W/S = (W/S)₀ (m/m₀)^b, with b = 1/3 for geometric similarity.
For a single LaMSA impulse, energy supplied per kg of body, S, does not depend on mass.
The launch closes when e_req ≤ S, which gives

  **m* = m₀ (S / e₀)^(1/b)**, where e₀ = (W/S)₀ / (ρ C_L).

e_req rises with m and S is constant, so m* is an **upper** mass bound. I ignore the energy lost to
water drag, added mass and climbing out of the water (½v² ≫ g·h for h of a few cm). Including those
losses would only make m* smaller.

## Inputs

| Input | Value used | Source | Read-level |
|---|---|---|---|
| Anchor wing loading (W/S)₀ | 78 N m⁻² | Taxiing model of flying-fish take-off, bioRxiv 10.1101/765560. As reported, it lies "within the range reported for six genera". | search-summary (the full text returned HTTP 429 twice) |
| Anchor mass m₀ | 0.1 kg (range 0.05–0.2 kg) | **My assumption** for an adult exocoetid. The bioRxiv model mass is `unknown`; I could not access the paper. | none (assumption) |
| C_L,max | 1.0 (range 0.8–1.2) | ≈1.03 maximum, and 1.0–1.1 in a separate model study (Park & Choi 2010 JEB 213:3269; IUTAM 2007 proceedings) | search-summary; JEB page text read in part (full-text, partial). Its numeric C_L is in a table image I could not read. |
| ρ_air | 1.2 kg m⁻³ | standard | n/a |
| Cross-check speed | "10∼20 m s⁻¹" natural flight speed | Park & Choi 2010, Introduction | full-text (partial) |
| LaMSA supply S | 4.2 J kg⁻¹ (range 2–12) | Sutton et al. 2019 ICB (PMC6907395): muscle energy density 15.0 J/kg, of which a spring can store at most 28% = 4.2 J/kg, independent of size. Model value, not measured. | full-text, read through a summarising fetch |
| Range on S | 2–12 J kg⁻¹ | **My inference.** The upper end allows a fish myotome of about 50% of body mass at 40–85 J per kg of muscle, times 0.28. The lower end allows transfer losses. | inference |
| Exponent b | 1/3 (geometric); 0.36 and 0.53 as a variant | Geometry. 0.36–0.53 were reported for Fish 1990 J Zool 221:391 in a search summary, and also appear in the commit message. I could not confirm that they are wing-loading exponents. | search-summary only. The Fish 1990 PDF hosts (wcupa.edu, scribd) and cambridge.org are blocked by this session's network policy. |

Anchor check: v = √(2·78/(1.2·1.0)) = 11.4 m s⁻¹. That falls inside the 10–20 m s⁻¹ reported flight
speed, so the anchor is consistent.
e₀ = 78/1.2 = **65 J kg⁻¹**.

## Arithmetic

Central case (m₀ = 0.1 kg, S = 4.2, e₀ = 65, b = 1/3):
 S/e₀ = 0.0646; (0.0646)³ = 2.70×10⁻⁴; m* = 0.1 × 2.70×10⁻⁴ = 2.7×10⁻⁵ kg = **27 mg**.
 0.4 g / 27 mg = **14.8×**.

Zebrafish check: a 0.4 g fish with flying-fish wing proportions needs e_req = 65 × (0.004)^(1/3) = **10.3 J
kg⁻¹**. One LaMSA impulse supplies 4.2 J kg⁻¹, which is short by a factor of 2.5 in energy. Because m* goes
as the cube of the energy ratio, that becomes about 15× in mass.

| Case | m₀ (kg) | S (J/kg) | e₀ (J/kg) | b | m* | 0.4 g / m* |
|---|---|---|---|---|---|---|
| central | 0.1 | 4.2 | 65 | 1/3 | 27 mg | 15× |
| pessimistic corner | 0.05 | 2 | 81 | 1/3 | 0.75 mg | 530× |
| optimistic corner | 0.2 | 12 | 54 | 1/3 | 2.2 g | 0.18× (feasible) |
| measured-exponent variant | 0.1 | 4.2 | 65 | 0.36 | 50 mg | 8× |
| measured-exponent variant | 0.1 | 4.2 | 65 | 0.53 | 570 mg | 0.7× (feasible) |

The range is wide because m* depends on the cube of an energy ratio. A factor of 2 in S moves m* by 8×.

**Muscle-only route (inference, brief):** Sutton's model gives direct muscle output below the spring's
4.2 J/kg for animals under about 2.5 g. At 2.5 g, e_req = 65 × (0.025)^(1/3) ≈ 19 J/kg, which exceeds
the full 15 J/kg muscle density. Under Sutton's parameters, then, muscle-only does not close at any mass I
checked. If a fish could put its whole myotome into one stroke, at about 40 J/kg body, the bound becomes
0.1 × (40/65)³ ≈ 23 g at best. Whether a fish can do that is `unknown`.

## Comparison with the recorded value

I read the recorded value from the commit message only: m* = 39 mg (8.5–173 mg), with 0.4 g about 10×
(2.3–47×) too large.

- Central value: 27 mg against 39 mg, within a factor of 1.5. The direction also matches: m* is an upper
  bound, and a 0.4 g zebrafish is above it. **AGREE.**
- Range: **DISAGREE in part.** My inputs give a wider range (0.75 mg–2.2 g). Two cases make the 0.4 g
  zebrafish feasible: the optimistic corner, and the b = 0.53 variant. The recorded 2.3–47× range never
  lets it close.
- The recorded mass anchor and supply range are `unknown` to me, because I did not read S29/S30. The gap
  between ranges may come from my looser S upper bound (12 J/kg).
- Shared-method caveat: I saw the method in the commit message, so this result agrees on the arithmetic
  and inputs, not on an independently chosen framing.

## Negative searches and access failures

- Fish 1990 tables: not accessed. wcupa.edu, scribd.com and cambridge.org are all blocked by the network
  policy (ENOTFOUND).
- bioRxiv 765560 full text: HTTP 429 on two attempts.
- No measured minimum take-off airspeed for *Cheilopogon* turned up in two web searches (standard +
  extended).

```swarm-replication
{"claim_id": 235, "my_value": "m* ≈ 27 mg (0.75 mg–2.2 g geometric; 50–570 mg measured-exponent variant); 0.4 g zebrafish ≈ 15x too large", "agrees": true, "note": "Central value (27 vs 39 mg) and direction (upper bound, zebrafish too large) agree, but my input range is wider and its optimistic corners make 0.4 g feasible; method was seen in the commit message so this is not framing-independent."}
```
