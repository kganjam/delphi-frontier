# Challenge 141: adversarial review of claim [S1-D-D] (escape-speed sensitivity)

Status: desk review, 2026-11-04. **No experiment was run.** Every number with no citation is
**[calculated]** by `docs/research/fish/challenge_141_calc.py` (run it from the repo root). I wrote
none of the claim under review. "Author" below means the author of S1-D-D, on branch
`claude/deepen-s1-d-sensitive-input-3mdmls` (`docs/research/fish/S1-D-deepen.md` and
`s1_d_deepen_calc.py`). I read both in full (**read-level: full-text**).

## Claim under review

> The S1-D answer is most sensitive to adult escape speed (it enters squared; a 13% drop flips the
> ballistic reading); a second independent source (Danos & Lauder 2012, derived 0.84 m/s)
> contradicts S1-D's 0.95 m/s lower bound, so the no-aerial-takeoff conclusion stands (lift <=31%
> of weight under both sources) while the ballistic-exit claim falls back to marginal (1.03 SL
> drag-free upper bound).

## 1. Independent arithmetic [calculated]

I wrote my own formulas instead of reusing the author's script: L/W = ρ_air·S·C_L·v²/(2mg) and
h = v²/(2g), with the claim's inputs m = 0.4 g, ρ_air = 1.20 kg m⁻³, S·C_L = 2 cm² (central) or
6 cm² (generous), and SL = 3.5 cm.

| Check | Mine | Claim | Agree? |
|---|---|---|---|
| L/W generous at 1.84 m/s (Demesmay peak + 1 SD) | 0.311 | ≤ 31 % | yes, to rounding |
| L/W central at 1.57 m/s | 0.075 | 0.075 | yes |
| Speed to clear 3.5 cm drag-free | 0.829 m/s | 0.83 | yes |
| Fractional drop from 0.95 that flips (B) | 0.872, i.e. 12.8 % | 13 % | yes |
| Danos U = Re·μ/(ρ_w·TL) | 0.842 m/s | 0.84 | yes |
| Apex at 0.84 m/s | 3.60 cm = 1.03 × 3.5 cm | 1.03 SL | yes, arithmetically |

"Enters squared" is correct. v has elasticity 2 in both L/W and h. S, C_L and m have elasticity 1
in L/W, and SL has elasticity 1 in h/SL. **The arithmetic survives.**

I also checked whether Danos & Lauder's three Reynolds numbers agree with each other. With
ρ = 1000 kg m⁻³ assumed and TL = 33 mm, Re 2350 at 10 mPa s gives 0.71 m s⁻¹, and Re 820 at
20 mPa s gives 0.50 m s⁻¹ [calculated]. Speed falls steadily as viscosity rises, so the
inversion behaves sensibly.

## 2. Source check: Danos & Lauder 2012

doi:10.1242/jeb.068957, publisher HTML (**read-level: full-text via a summarising fetch**,
characters 0–100,000 of about 121,000; figures and tables not read). The fetch returned these
author statements verbatim:

- "Reynolds number calculations using fish length, maximum linear velocity per sequence"
- "mean total length 33.0±1.3 mm"
- "The mean maximum Reynolds number in 1 mPa s water was 27,800 (±2140 s.e.m.)"
- The fetch found no velocity in m s⁻¹, cm s⁻¹ or BL s⁻¹, no fish mass, and **no water
  temperature**. Those negatives cover only the portion read.

These confirm that the author's 0.84 m s⁻¹ is honestly labelled **derived**. They also confirm
that the paper does not say which length went into Re. I found no misstatement of the source.

## 3. Attacks

### 3a. Hidden assumption: the body size behind "1.03 SL". This is the defect

The claim's 1.03 SL takes a speed measured on Danos's fish (TL 33.0 mm, so SL ≈ 26.4 mm using the
author's own SL ≈ 0.8 TL) and divides the resulting apex by **S1-D's assumed SL of 35 mm**, which
is about 33 % longer than the fish that produced the speed. Normalising the same speed by the
measured fish's own length gives **1.37 SL** [calculated]. That is no worse than S1-D's own
1.31 SL.

Using 35 mm is legitimate only if escape speed is the same at every body size. My inference, not
a sourced value: absolute fast-start speed generally rises with body length. If I scale Danos's
speed up to a 35 mm SL fish as v ∝ L^a [calculated]:

| exponent a | v (m s⁻¹) | apex |
|---|---|---|
| 0 (size-independent, the claim's implicit choice) | 0.84 | **1.03 SL** |
| 0.5 | 0.97 | 1.37 SL |
| 1 (constant BL s⁻¹) | 1.12 | 1.82 SL |

So **1.03 SL is the extreme end of the plausible range, not its centre**. It comes from comparing
a smaller fish's speed against a larger fish's length.

Limits of this attack:

- I did not find a measured zebrafish speed-versus-length exponent. Its value is `unknown`. I
  searched no literature for it; the exponents in the table are illustrative.
- I did not verify that SL = 35 mm fits a 0.4 g fish. That value is inherited from S1-D and is
  `unknown` to me.

What survives: the qualitative word "marginal" can still be defended. Drag, entrained water and a
non-vertical exit all lower a drag-free apex, and the author's lower-bound contradiction (3b) is
untouched. **What is weakened is the quantitative reason the claim gives for the downgrade.**
Measured against its own fish, the second source gives about the same ballistic margin as S1-D.

### 3b. Is the "contradiction" sound?

A derived peak of 0.84 m s⁻¹ below Demesmay's 40-ms mean of 0.95 m s⁻¹ is a genuine tension
**only for fish of the same size**. The author's script uses Demesmay fish of 2.6–3.6 cm. I did
not verify that range against Demesmay (could-not-access in this session; I did not try).
If those fish are up to about 36 % longer than Danos's 2.64 cm SL, a constant-BL s⁻¹ scaling
brings Danos up to 0.84 × 3.6/2.64 ≈ 1.15 m s⁻¹ [calculated]. That is above 0.95, and the
contradiction would disappear. The author lists "fish size" as one possible explanation, so this
point does not refute the claim. My inference is that "contradicts" is stronger than the evidence
supports, and "in tension, possibly size-confounded" would be more accurate.

### 3c. Hidden assumption: the viscosity used in the Re inversion

The paper reports no water temperature (negative over characters 0–100,000). If the authors
computed Re with the true viscosity of warm water rather than the nominal 1 mPa s, the derived
speed would be lower. For example, μ = 0.83 mPa s, roughly water at 28 °C, gives 0.70 m s⁻¹
[calculated]. That temperature is my **assumption**, not reported. Because the authors label
the treatment "1 mPa s", my inference is that they used the nominal value, so 0.84 is the more
likely reading. The claim does not flag this, but the claim states μ = 1 mPa s openly, and the
effect would only push in the claim's own direction. **Not a defect, but an unrecorded
dependency.**

### 3d. Proxy check

Reading (B) needs the speed at water exit for an upward escape. Both sources measured
horizontal escapes. The author already flags this as an assumption, so it is not a new defect.
Reading (A) uses burst speed, which is the right quantity for a takeoff run, not a proxy.

### 3e. Evidence levels

- 0.84 m s⁻¹ is tagged **derived**, which is correct.
- 1.57 ± 0.27 m s⁻¹ is tagged **observed**, citing the author's full-text read. I did not
  re-read Demesmay.
- The lift values and the apex are calculated, and the claim says so.

No mislabelling found.

### 3f. Counter-examples

I ran no new literature search for a third adult zebrafish escape speed. The author's negative
search (Europe PMC, scope stated in S1-D-deepen §3b) stands unchallenged by me. Nothing I read
flips reading (A). Lift is at most 0.311 of weight even at the high source + 1 SD with generous
lift [calculated], and reaching 1 would need v ≈ 3.3 m s⁻¹.

## Verdict: WEAKENED

- **Survives:**
  - the sensitivity ranking (v enters squared, and a 12.8 % drop flips reading (B));
  - all the arithmetic;
  - the evidence labelling;
  - the headline that there is no aerial takeoff (L/W ≤ 0.311 under both sources).
- **Weakened:**
  - "The ballistic-exit claim falls back to marginal (1.03 SL)". The 1.03 SL comes from dividing
    a 26-mm-SL fish's speed by a 35-mm SL. Normalised to the measured fish it is about 1.37 SL
    drag-free, equal to S1-D's margin, so the second source does not by itself lower the
    ballistic margin.
  - "Contradicts" is likewise possibly confounded by body size.
- **Corrected value:** Danos-derived drag-free apex ≈ 1.37 SL of the measured fish (SL ≈ 0.8 TL
  assumed). The range is 1.03–1.82 SL for a 35 mm SL fish, depending on an unknown size-scaling
  exponent. Reading (B) remains "marginal", for the reasons of drag and exit angle, not because
  of this source.

```swarm-challenge
{"claim_id": 141, "outcome": "weakened", "reason": "Arithmetic, sensitivity ranking and the no-aerial-takeoff verdict all reproduce, but the 1.03 SL ballistic figure divides the apex from a 26-mm-SL fish's derived speed (Danos & Lauder, TL 33 mm) by S1-D's assumed 35-mm SL; normalised to the measured fish it is ~1.37 SL, equal to S1-D's margin, so the downgrade rests on a body-size mismatch and the 'contradiction' may be size-confounded.", "corrected_value": "Danos-derived drag-free apex ~1.37 SL of the measured fish (range 1.03-1.82 SL for a 35 mm SL fish depending on unknown speed-length scaling exponent 0-1)", "depends_on": ["measured: Danos & Lauder 2012 doi:10.1242/jeb.068957 mean max Re 27,800 at 1 mPa s, mean TL 33.0 mm, Re uses 'fish length' (basis unstated), no temperature reported (full-text via summarising fetch, chars 0-100,000)", "derived: Danos U = Re*mu/(rho_w*TL) = 0.84 m/s assuming mu = 1 mPa s nominal, rho_w = 1000 kg/m3", "assumption: SL = 0.8 TL (author's ratio) -> Danos fish SL 26.4 mm", "assumption: S1-D SL = 3.5 cm for the 0.4 g fish (inherited, unverified)", "inference: escape speed scales with length as L^a, a in [0,1]; a unknown (no source searched)", "measured: Demesmay et al. 2025 peak 1.57 +/- 0.27 m/s and 3.8 cm in 40 ms (as reported by S1-D-D; not re-read by me)", "assumption: Demesmay fish 2.6-3.6 cm (from S1-D-D script; not verified)", "premise: m = 0.4 g; assumption: S*CL = 2-6 cm^2; constants rho_air = 1.20 kg/m3, g = 9.81 m/s2", "model: drag-free ballistic apex h = v^2/(2g)", "law: lift = 0.5*rho*S*CL*v^2 (takeoff-stall-speed)", "S1-D-D claim text and script (claude/deepen-s1-d-sensitive-input-3mdmls, full-text)"]}
```
