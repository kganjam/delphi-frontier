# Challenge 169: adversarial review of [S20-D-D], the guppy-class exit-speed comparator

**Claim under review** (author's words, harvest `s20-d-sensitive-input-77m8c9`, recorded level *derived*):
S20-D's 1.51 m/s "guppy-class" comparator, rebuilt from Soares & Bierman 2013 plus Chang et al. 2019's
H/L ~ L^-1/3 scaling, becomes **1.37 m/s** (band 1.02–1.37; extreme single jump 1.82 m/s). A 1 m launch
needs 3.13 m/s, so it stays out of reach "by 1.7x–3.7x" and S20-D's conclusion stands.

**Verdict: WEAKENED.** The headline conclusion (a 1 m launch is out of reach for a guppy-class jumper
scaled to 33 mm) **survives every relaxation I tried**. Two of the claim's stated numbers do not survive:
the **3.7x** upper bound cannot be reproduced from the stated inputs (the most it gives is 3.07x), and the
**1.7x floor** depends on the exponent of a cross-taxon fit. Relax that exponent to the isometric case
and the floor drops to **1.56x** (calculated). Choosing 1.37 over 1.50 m/s for the mean comparator is also
a choice between two primary measurements that disagree. It is not a correction of S20-D's value.

I did not see S20-D or the harvest note. Neither is in this repository: `grep -ri "S20\|guppy\|danio\|zebrafish"`
over the working tree found only two unrelated JSON files. I judged the claim from its own text and the
primary sources.

## Sources and read-levels

| Source | Read-level | What I used |
|---|---|---|
| Soares & Bierman 2013, *PLoS ONE* 8:e61617, "Aerial jumping in the Trinidadian guppy" (PMC3629028) | full-text (via web fetch and summariser; quoted values checked against the Table 1 wording) | SL 1.85±0.35 cm; jump height 6.54±1.92 cm = 3.52±0.96 BL; max velocity in water 102.36±33.75 cm/s (Discussion gives a conflicting 100.16±33.9); max velocity in air 123.57±30.0 cm/s; one Fig. 2 jump with 128 cm/s in water and 150 cm/s in air; launch angle 77.4°±24.91°; 1000 fps; n = 20 + 22 jumps from 9 fish |
| Chang et al. 2019, *J. R. Soc. Interface* 16:20190014, "Jumping dynamics of aquatic animals" (PMC6451394) | full-text (via web fetch and summariser) | H/L ~ L^-1/3 ~ Fr²; fitted exponent **−0.35 ± 0.12 (r² = 0.57)** across 35 species spanning about 5 orders of magnitude in L; U0² = 2gH; H is the topmost point of the body; animal exit speeds *inferred, not measured*; air drag neglected; guppy cited at about 3.5 BL from the literature |

## 1. Arithmetic, redone independently (all values below are **calculated**, not observed)

- Length factor under the claim's law: v ∝ √H ∝ L^(1/3), so (33/18.5)^(1/3) = **1.213**.
- Scaled in-water peak: 1.024 × 1.213 = 1.24 m/s. Scaled in-air peak: 1.236 × 1.213 = **1.50 m/s**.
- Height route: H_guppy = 6.54 cm, so H_33mm = 6.54 × (33/18.5)^(2/3) = 9.62 cm and v = √(2gH) = **1.37 m/s**.
  This reproduces the claim's 1.37. The mean of the scaled water and air peaks also gives 1.37, so the
  number is reproducible either way.
- Extreme: 1.50 m/s (the Fig. 2 in-air value) × 1.213 = **1.82 m/s**. Reproduced.
- Needed speed: a 1 m horizontal range at 45°, launched from the surface with no drag, needs v = √(g·1 m) =
  **3.13 m/s**. Reproduced. The claim does not say "range". A 1 m *vertical* launch needs 4.43 m/s, and
  every ratio below would be 1.41x larger.
- S20-D's 1.51: √(2g · 3.5 · 0.033 m) = 1.505 m/s. Reproduced. Its floor, 3.13/1.51 = 2.07x, matches "at least 2.1x".
- Shortfall ratios: 3.13/1.82 = **1.72x**; 3.13/1.37 = 2.29x; 3.13/1.02 = **3.07x**.
  **The claim's 3.7x is not reproducible from any stated input.** The lowest stated speed (1.02) gives 3.07x.
  A speed of 0.85 m/s would be needed to give 3.7x, and the claim states no such value. My unverified guess,
  marked as inference: 3.7x may be 4.43/1.2 (the vertical-1-m speed over an unscaled speed), which would mix two
  different launch definitions.
- Hop range at 45° (v²/g): 1.02 gives 10.6 cm; 1.37 gives 19.1 cm. This reproduces "11–19 cm". The claim's own
  extreme speed (1.82 m/s) gives **33.8 cm**, which the stated band leaves out.

## 2. Proxy check

The quantity that matters is the ballistic take-off speed of *Danio rerio* when it aims for range. The claim
uses a *guppy* speed instead, measured on **near-vertical** jumps (77°±25°). Two proxy choices are hidden:

1. **Which guppy speed.** The kinematic in-air peak (1.24 m/s), scaled, gives **1.50 m/s**. The speed implied
   by the measured height (1.13 m/s, or 1.16 m/s after correcting for the 77° launch angle), scaled, gives
   **1.37–1.41 m/s**. These are two primary-source routes that disagree by about 10%, and I do not average
   them. The in-air peak was partly *estimated* from deceleration for jumps that left the frame (Methods),
   and H is the height of the body's topmost point rather than its centre of mass (Chang). Both biases are
   real, and I cannot rank them. **Inference:** on the in-air route the corrected mean comparator equals
   S20-D's 1.51 m/s and the mean-case floor stays at 2.1x. So "1.51 → 1.37" is a change of proxy, not a
   correction.
2. **Vertical to 45°.** Converting speed to range assumes Danio can produce the same take-off speed at 45°
   as a guppy does at about 77°. Neither paper tests this. It is untested in both directions.

## 3. Hidden assumption carrying the result: the length-scaling law, relaxed

The L^-1/3 law is a cross-taxon fit (r² = 0.57) over five orders of magnitude, and here it is applied across
a 1.78x length step between two species. Its exponent CI (−0.23 to −0.47) gives v-scaling factors of
1.17–1.25. Bracketing with the two textbook limits:

| Scaling assumption | Scaled mean speed | Scaled extreme | Shortfall at extreme (calculated) |
|---|---|---|---|
| v size-invariant (Hill-type isometric jumper) | 1.13–1.24 m/s | 1.50 m/s | 2.09x |
| Chang L^-1/3 (claim) | 1.37–1.50 m/s | 1.82 m/s | 1.72x |
| H/L size-invariant, i.e. constant Fr (S20-D's original assumption) | 1.51–1.65 m/s | **2.00 m/s** | **1.56x** |

Even the most generous scaling leaves the fish **at least 1.56x short in speed** (about 2.4x short in
energy), so the conclusion survives. The claim's stated floor of "1.7x" is not robust. Within the
assumptions the claim itself discusses, it is 1.56x.

Smaller relaxations, all of which make reaching 1 m *harder*, so the conclusion is unaffected:
- **Air drag**, which Chang neglects. This is an order-of-magnitude estimate with an assumed 0.4 g fish, a
  frontal area of about 4×10⁻⁵ m² and Cd of about 1, all *my assumptions and not sourced*. Drag is then
  about 6% of weight at 3.13 m/s, which raises the needed speed slightly.
- **Length basis.** The guppy value is SL. Whether the 33 mm zebrafish value is SL or TL is `unknown`
  (S20-D was not available to check). If it is TL, the zebrafish SL is shorter and the comparator falls.

## 4. Evidence level

"Derived" is honest. Every number in the claim is calculated from measured guppy kinematics through a
model. The claim labels 1.37 "(calculated)". However, "exit 1.02 m/s in water, 1.24 m/s in air" are
*maximum* speeds, and the paper never uses the term "exit velocity". Calling them "exit" speeds is a small
mislabel. The Chang scaling law is itself partly built on *inferred*, not measured, animal exit speeds, so
it is a model input, not an observation.

## 5. Missed regimes and counter-examples

- **Scope of my search:** two web searches (the guppy paper and Chang 2019) plus full-text reads of both.
  I did **not** search for measured jump kinematics of *Danio rerio* itself, adult zebrafish fast-start
  speeds, or specialised small jumpers such as hatchetfish (Gasteropelecidae), splash tetra (*Copella
  arnoldi*) or mangrove killifish (*Kryptolebias marmoratus*). A specialised small jumper is the most
  plausible counter-example: a fish under 5 cm with take-off speeds above about 2 m/s. Whether one exists
  is `unknown` from this review. That is the open risk to the conclusion.
- Copepods reach H/L ≈ 10 (Chang), which shows that small aquatic jumpers can far exceed 3.5 BL. They are
  not fish and do not entrain fluid, so they do not bear directly on Danio.

## Bottom line

The conclusion stands: no route I tried gets a guppy-class jumper scaled to 33 mm within 1.5x of the
3.13 m/s needed. The corrected numbers are:
- **Mean comparator:** 1.37–1.50 m/s, depending on whether the height-implied or in-air kinematic route is used.
- **Speed shortfall:** **1.56x–3.07x** across the scaling assumptions and stated inputs. The claim's
  1.7x–3.7x is not supported at either end.
- **Reachable 45° hop:** 11–34 cm when the claim's own extreme speed is included.

```swarm-challenge
{"claim_id": 169, "outcome": "weakened", "reason": "The 1 m launch stays out of reach under every scaling relaxation, but the stated 3.7x upper bound is unreproducible from the stated inputs (max 3.07x) and the 1.7x floor falls to 1.56x if the cross-taxon L^-1/3 exponent is relaxed to S20-D's own size-invariant H/L; the 1.37 vs 1.50 m/s mean comparator is a choice between disagreeing primary routes, not a correction.",
  "corrected_value": "comparator 1.37-1.50 m/s (mean), 1.82-2.00 m/s (extreme); speed shortfall vs 3.13 m/s = 1.56x-3.07x",
  "depends_on": ["Soares & Bierman 2013 guppy SL 18.5 mm, max water speed 1.02 m/s, max air speed 1.24 m/s, height 6.54 cm, single-jump 1.50 m/s air", "Chang et al. 2019 H/L ~ L^-0.35+/-0.12 cross-taxon fit", "zebrafish length 33 mm as used by S20-D (SL vs TL unknown)", "1 m launch defined as 1 m horizontal range at 45 deg from surface, no drag (3.13 m/s)"]}
```
