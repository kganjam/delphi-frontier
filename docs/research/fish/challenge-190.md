# Challenge 190: wing lift at launch and apex (S28)

**Claim under review (the author's words, S28-organism.md §3.2 and swarm-result):** "Granting an unmeasured 1-BL span
and AR-5 fin (S = 192 mm²), the wing produces 10 % of body weight at launch and ~5 % at the apex."
Recorded level: *derived*. Value: 10 % of weight.

**Source read-level:** `docs/research/fish/S28-organism.md` and `S28_organism.py` on branch
`origin/claude/s28-organism-design-5z0vjz` (commit e8ba4191), **full-text**.

**Status of this review:** every number below is **calculated by me** with `docs/research/fish/challenge_190.py`.
None of it is a measurement.

**Verdict: WEAKENED.** The arithmetic is right. The 10 % is not a central value, though. It is an upper bound that
depends on a back-solved body mass that the claim's "granting" clause does not mention. Every relaxation I tested
moves the number down. None of them changes S28's negative conclusion; they make it stronger.

---

## 1. Independent arithmetic

I computed lift directly from L = ½ρV²S·CL and did not use the author's (V/V_to)² shortcut.

- ρ = 1.225 kg m⁻³, V = 1.38 m/s, S = 192e-6 m², CL = 1.07
- L = 0.6125 × 1.9044 × 192e-6 × 1.07 = **2.40e-4 N**
- W = 0.25e-3 kg × 9.81 = 2.45e-3 N
- **L/W = 9.77 %**, so "10 %" is correct after rounding.

At the apex, assuming a 45° launch and no drag, the horizontal speed is 1.38·cos45° = 0.976 m/s. That gives
L/W = **4.89 %**, so "~5 %" is also correct.

I integrated the trajectory myself (wing CL 1.07, CD0 0.08, body drag, 45° launch). Drag lowers the apex speed to
0.935 m/s, which gives **4.5 %**. Across launch angles of 40–50° the result is 3.6–5.3 %. "~5 %" holds.

**A minor internal inconsistency (calculated).** S = 192 mm² with m = 0.25 g gives V_to = **4.41 m/s**, not the 4.37 m/s
that the author's shortcut uses. 4.37 m/s corresponds to S = 196 mm², as the author's own §1 says. The effect is 2 %
(9.97 % vs 9.77 %) and changes nothing.

## 2. Is a proxy standing in for the quantity that matters?

**Partly.** "Lift as a % of body weight" is the lift **magnitude**. The quantity that matters for the leap is the
**vertical** component that offsets gravity. At launch, lift is perpendicular to a 45° path, so its vertical share is
9.77 % × cos45° = **6.9 % of W** (calculated). The rest points horizontally. During the ascent it points
**backwards**: in the script, a_x = −L·u_y/m with u_y > 0.

So the claim's 10 % is correct as a magnitude. As weight support at launch it overstates the vertical effect by about
1.4×. Only at the apex do the two quantities coincide, at ~5 %.

This matters downstream. S28 §3.6 predicts that "ascent deceleration [is] reduced by about 5–10 %". By my calculation the
vertical offset is about 7 % at launch, falling to about 5 % at the apex, so the reduction is about 5–7 %, not 5–10 %.

*Aside, my reading of the author's text:* §3.2 says lift points backwards "on the way down". The author's own script puts
the backward component on the **way up** and a forward component on the way down. This is a mistake in the prose only;
the integrated numbers are not affected.

## 3. Hidden assumptions, relaxed

All results below are calculated with the script.

| Assumption carried by the claim | Relaxed to | Launch L/W | Apex L/W |
|---|---|---|---|
| Baseline (author) | — | 9.8 % | 4.9 % |
| m = 0.25 g, **back-solved** so that V_to = 4.37 m/s (author §1, "assumed") | m = 0.40 g, which the author's §1 calls "also typical" | **6.1 %** | **3.1 %** |
| Fin membrane mass not charged (author §2.2: 10.6–21.1 mg) | +21.1 mg | 9.0 % | 4.5 % |
| Quasi-steady CL_max = 1.07 reached at the **instant** of exit | Impulsive start. Under thin-aerofoil (Wagner) theory, circulation starts at about half its steady value and needs several chord lengths of travel to build up | below 9.8 % at the instant of exit (not quantified here) | barely affected (~0.2 s ≈ 40 chords later) |
| Fin fully out of the water and spread at stall incidence | Fin still wetted at exit; spreading never observed (author flags this too) | lower; not quantified | — |

**The load-bearing hidden assumption is the mass.** The claim's "granting" clause names span, AR and S, but not mass.
Lift fraction scales as 1/m. The author's own §1 admits that 0.40 g is equally typical, and at that mass the claim
becomes about **6 % at launch and about 3 % at the apex**. I did **not** search the literature for zebrafish
length–mass data in this review, so I cannot say which mass is better supported. The range 0.25–0.40 g is the author's.

## 4. Is the evidence level honest?

**Yes.** S28 labels the value *derived* and says so in the document header ("Nothing in this document is a new
measurement"). It flags span, AR and area as extrapolation. I found no derived-as-measured defect. The only labelling
gap is that the claim sentence presents a value that is conditional on mass as a plain number.

## 5. Regimes or counter-examples the author missed

- **Ground effect** (my inference). At the moment of exit the fin is within a chord or so of the water surface. Ground
  effect raises lift and lowers induced drag at small height-to-chord ratios. This is the **only** factor I found that
  would push the launch figure **up**. It decays within a few chord lengths of climb, so it cannot rescue the leap. I did
  not quantify it.
- **Unsteady / delayed-stall lift** (my inference). A *flapping* fin could exceed the steady CL_max. S28 models a fin held
  rigidly spread, and the muscle row of S28 §5 already rules out flapping power. So this regime does not apply to the
  claim as framed.
- **Search scope:** I did no literature search for this review. All sources were the S28 files (full-text) and standard
  aerodynamic theory from background knowledge (read-level: could-not-access this session; not cited as a measurement).

## 6. Conclusion

The 10 % / 5 % figures are arithmetically correct for m = 0.25 g, steady CL_max, and the lift magnitude. They are an
**upper bound**, not a central estimate:

- with the author's alternative mass (0.40 g): **6 % / 3 %**;
- with the membrane mass charged: **9 % / 4.5 %**;
- as a vertical weight offset at a 45° launch: **7 %** at launch;
- with an impulsive start (Wagner): lower still at the exit instant.

The claim should read **"≤ 10 % of body weight at launch (≈ 6–10 % for m = 0.25–0.40 g; ≈ 7 % vertical at a 45° launch)
and ≤ 5 % at the apex (≈ 3–5 %)"**.

S28's negative verdict (no flight, glide or skim) is **strengthened, not threatened**. The downstream predicted phenotype
"5–10 % reduced ascent deceleration" should be revised down to about **3–7 %**. That makes it harder to detect.

```swarm-challenge
{"claim_id": 190, "outcome": "weakened", "reason": "Arithmetic is correct (9.8% launch, 4.5-4.9% apex), but the 10% rests on a back-solved 0.25 g mass not named in the granting clause and on quasi-steady CL_max at the exit instant; at the author's own alternative 0.40 g it is 6%/3%, and the vertical (weight-offsetting) component at a 45 deg launch is only 7%, so 10% is an upper bound, not a value.",
  "corrected_value": "<=10% of body weight at launch (6-10% for m=0.25-0.40 g; ~7% vertical at 45 deg launch); <=5% at apex (3-5%)",
  "depends_on": ["S28 body mass 0.25 g (assumed, back-solved)", "S28 alternative mass 0.40 g (author-stated typical)", "CL_max 1.07 (derived, project)", "S = 192 mm2 case C (extrapolated)", "Miln2021 burst 1.38 m/s (measured swimming burst, assumed = exit speed)", "S28 fin membrane mass 10.6-21.1 mg (estimate)", "Wagner impulsive-start theory (background knowledge, not accessed)"]}
```
