# Challenge 228 — S29's "1.86× vs ≥10×" launch-energy shortfall

**Claim under review (the author's words, S29-organism.md):** "THE SHORTFALL IS ~1.86x (1.22-3.08), against >=10x for EVERY wing route. The launch-energy representation is an order of magnitude closer to feasible than the wing representation ever was."
**Recorded evidence level:** derived. **Value:** 1.86 shortfall ratio.
**Sources read:** `docs/research/fish/S29-organism.md` and `S29_launch_energy.py` on branch `origin/claude/s29-launch-energy-2iuixr` (full-text). `docs/research/fish/S28-organism.md` on `origin/claude/s28-organism-design-5z0vjz` (full-text, read by grep for every shortfall figure). I did not open any primary literature for this challenge. Every literature value below is S29's input, carrying S29's read level, and I have not checked it.
**My numbers:** every number I give is **derived** (a calculation) and comes from `python3 docs/research/fish/challenge-228.py`. None is a measurement.

## Verdict: WEAKENED

The arithmetic is correct. The comparison it is used for is overstated.

## 1. Independent arithmetic

I rewrote the budget as one expression:

shortfall = (½V² + ½ρ·Cd·A·V²·s/2/m) / (f·w·η_spring·η_h)

I did not reuse S29's intermediate values. With S29's central inputs (V 4.37 m/s, m 0.40 g, Cd 0.2, A 24 mm², s 1.09 cm, f 0.30, η_spring 0.93, η_h 0.37):

| w (J/kg muscle) | Shortfall |
|---|---|
| 81 | 1.217× |
| 53 | **1.859×** |
| 32 | 3.080× |

These reproduce S29's 1.86 (1.22–3.08). The other checks also reproduce:
- KE: 9.55 J/kg.
- Drag work: 0.250 mJ.
- The 11.5× gap between requirement and today's fish.
- The mass-consistent value of 2.98×.
- f = 0.60 gives 0.93× (S29 reports this as a surplus of 1.08).

**I found no arithmetic error.**

## 2. "An order of magnitude closer" fails on the author's own numbers

The wing figure is S28 row 1, the kinetic-energy gap at the best measured burst: (4.37/1.38)² = **10.03×**. That is the floor of "≥10×". Dividing it by S29's shortfall (derived):

| S29 case | Wing gap ÷ S29 shortfall |
|---|---|
| Central (1.86×) | **5.4×** |
| Best case, w = 81 (1.22×) | 8.2× |
| S29's own mass-consistent target, 5.53 m/s (2.98×) | 3.4× |

None of these reaches 10×. "An order of magnitude" holds only against S28's low-burst case (94×), but the claim compares against the ≥10× floor. **The accurate statement is about half an order of magnitude.**

## 3. "≥10× for EVERY wing route" is not what S28 reports

My inference from S28's table:
- **Row 2** (taxi/skim) reports the tail-beat frequency route short by **2.5–3.8×**.
- S28 §5 summarises its rows as failing by "between 2.5× and 166×".

So S28 does not support "≥10× for every wing route". It supports ≥10× only if every route is re-expressed as a kinetic-energy gap.

Converting the frequency gap to an energy or power gap would need a scaling law (for example, power ∝ f³). Neither S28 nor S29 states one. I do not supply one either, so I do not claim the taxi route is closer than 10× in energy terms. I claim only that the comparison as written mixes metrics.

## 4. Proxy and hidden assumption

**The proxy.** The number that closes the gap is **w**, the work one kg of muscle can store in a series spring in one slow stroke. S29 uses the Cuban tree frog in-situ value (Mendoza & Azizi 2021, read FULL by S29) as a stand-in for zebrafish fast myotomal muscle. The quantity that actually matters is that same w measured in a teleost myotomal preparation. S29 itself says this is unmeasured (its test #1).

**What the transfer carries.** Measured against today's fish, the requirement is **11.5×** (derived: 98.5 J/kg needed vs 8.58 J/kg delivered per stroke). That is no closer than the wing gap. The entire move from about 11× down to about 1.9× is the ratio 53/8.58 = **6.2×** (range 3.7–9.4×), and all of it comes from transferring frog w to fish.

- *Author's claim:* the representation is closer to feasible.
- *My inference:* it is closer only conditionally. The condition is a cross-taxon transfer of a value that has not been measured in any teleost.

**A plausibility bound on w.** This is ASSUMED physics, not a measurement: w ≈ stress × fibre strain / 1060 kg m⁻³.

| Assumed stress | Assumed fibre strain | w (J/kg) | Shortfall |
|---|---|---|---|
| 200–300 kPa | 0.10 | 19–28 | 3.5–5.2× |
| 200–300 kPa | 0.30 | 57–85 | 1.2–1.7× |

Neither the stress nor the strain values come from a source I read. Fish myotomal fibres are commonly described as working at small strains because of their helical geometry. I did not open a source for that in this session, so it stays an open risk, not a finding. If fish fibre strain does sit near 0.1, the shortfall moves to 3.5–5× and the comparison with the wing routes weakens further.

## 5. The stated range is too narrow

S29's range of 1.22–3.08 varies **only w**. I relaxed S29's own stated input ranges one at a time and then jointly (all derived).

**One at a time:**

| Input changed | Shortfall |
|---|---|
| η_h 0.34–0.39 (pike C-start) | 1.76–2.02× |
| η_h 0.27 (pike S-start) | 2.55× |
| Cd and stroke length (Cd 0.1–0.3, s 1.09–3 cm) | 1.80–2.22× |
| S28's 0.25 g mass | 1.93× |
| Mass-consistent 5.53 m/s target | 2.98× |

**Jointly** (w × η_h 0.34–0.39 × Cd × s × V, n = 108):
- **1.12–6.40×** overall.
- **1.12–3.99×** with V fixed at 4.37 m/s.

The central value of 1.86 stands. The upper bound of the stated range understates the uncertainty by about 2×.

The headline also uses a target speed that S29 admits is inconsistent with its 0.40 g mass. On S29's own correction, the like-for-like central value is about **3.0×**.

## 6. Evidence level

The "derived" label is honest. S29 states that nothing in it is a new measurement, and it labels each input MEASURED, PROJECT, ASSUMED or SECONDARY.

There is one framing defect. The phrase "closer to feasible" reads as a feasibility statement, but it covers only one term of a conjunction. On the same page, S29 classes the latch as an "invention with no locomotor precedent". That gap is not quantified, so it cannot be ranked against the wing routes' 10×.

## 7. Counter-examples and regimes

- **Not searched in this session:** I did no literature search for this challenge (scope: the two repository documents only). I therefore cannot report a published teleost single-stroke spring-loading w, or a zebrafish C-start η_h. Both are `unknown`.
- **η_h is a design variable:** this is my inference from momentum conservation. The hydromechanical efficiency of a single push-off rises with the mass of water accelerated, so it depends on tail and fin area. That makes S29's line "No spring touches either term" correct for springs, but η_h is not fixed by the medium alone. This could move the shortfall in either direction and does not change the verdict.

## 8. What survives

- The 1.86× central arithmetic.
- The qualitative ordering: on the energy term, the spring route is a smaller shortfall than S28's 10.03× KE gap.

## 9. What does not survive

- "Order of magnitude closer". The factor is 5.4× (3.4–8.2×).
- "≥10× for every wing route". S28 row 2 is 2.5–3.8× in its own metric.
- "1.22–3.08" as the uncertainty. It is 1.1–4.0× at 4.37 m/s, and up to 6.4× at the mass-consistent target.
- Any reading of the 1.86× as independent of the unmeasured frog-to-fish transfer of w. That transfer carries a 6.2× share of the closure.

```swarm-challenge
{"claim_id": 228, "outcome": "weakened", "reason": "The 1.86x central shortfall recomputes exactly, but it is only 5.4x (3.4-8.2x) below S28's 10.03x KE gap rather than an order of magnitude, S28 itself lists a wing-family route (taxi/skim) at 2.5-3.8x so 'every wing route >=10x' mixes metrics, the stated 1.22-3.08 range varies only w (S29's own input ranges give 1.1-4.0x at 4.37 m/s, up to 6.4x at the mass-consistent 5.53 m/s), and the whole closure from 11.5x to 1.86x rests on transferring unmeasured frog spring-loading work (6.2x) to zebrafish myotomal muscle.", "corrected_value": "shortfall 1.86x central (derived; joint range 1.1-4.0x at 4.37 m/s, ~3.0x at mass-consistent 5.53 m/s); improvement over wing KE gap 5.4x (3.4-8.2x), not >=10x", "depends_on": ["S29 central inputs: V 4.37 m/s, m 0.40 g, Cd 0.1-0.3, A 24 mm2, s 1.09-3 cm, f 0.30, eta_spring 0.93", "Mendoza & Azizi 2021 frog spring-loading work 32-81 J/kg (via S29, not read by me)", "Frith & Blake pike C-start eta_h 0.34-0.39, S-start 0.27 (via S29, not read by me)", "S28 row 1 KE gap 10.03x from 4.37 vs 1.38 m/s", "S28 row 2 taxi/skim tail-frequency shortfall 2.5-3.8x", "Miln 2021 zebrafish burst 1.38 m/s (via S28)"]}
```
