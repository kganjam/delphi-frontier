# Challenge 134: adversarial review of S26-D, "S26's 'no' falls"

**Claim under review** (claim 134, from `harvest:deepen-s26-active-stiffening-48xj8q`):

> S26's 'no' falls. Its 165x gap compares a <=40 mm bluegill ray's passive EI (3.8e-6 N m^2) with a per-ray
> requirement for a 120 mm ray (6.3e-4 N m^2). Under isometric L^4 scaling the passive gap shrinks to ~2.1x.
> The single measured ~12x hemitrich-locking factor closes that with ~5.7x margin (calculated). So active
> stiffening can carry the load, conditional on isometry and on muscles reaching the excised-ray clamping
> factor in vivo.
>
> KEY: ~3.0e-4 N m^2, giving a required active factor of ~2.1x, not 165x. VERDICT: falls.
>
> Recorded evidence level: **measured**. Value: n/a.

**What I read:**

- `docs/research/fish/S26-deepen.md` and `S26_deepen_calc.py` at commit `95578def` on
  `origin/claude/deepen-s26-active-stiffening-48xj8q`. Read-level: **full-text**.
- The earlier challenge on the same claim, `challenge-92.md` (commit `4466af5a`). Read-level: **full-text**.
  I read it only after doing my own arithmetic.
- Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861. Read-level: **full-text via an automated
  page summarizer**, fetched in this session.

I measured nothing. Every number below is **calculated** by me with `python3 -I` from the stated inputs,
unless it is tagged otherwise.

## Verdict: WEAKENED

The structural point survives: an unscaled 40 mm ray cannot be fairly compared with a 120 mm requirement.
So the 165x gap cannot by itself support S26's "no".

What fails is the step to "yes, with a 5.7x margin". That step multiplies the 12x locking ratio onto the wrong
baseline. The record also labels the claim's evidence level wrongly: it is a calculation, not a measurement.
On my reading, the honest answer to S26 is **undetermined**, not "falls to yes".

## 1. Independent arithmetic

- (120 / 40.3)^4 = **78.61**
- 3.8e-6 × 78.61 = **2.99e-4 N m^2**
- Factor needed: 6.3e-4 / 2.99e-4 = **2.109x**
- Margin of the 12x: 12 / 2.109 = **5.69x**

These match the author. **There is no arithmetic fault.**

## 2. Proxy: the 12x multiplies the wrong baseline

This is the main defect. I agree with challenge-92 here, and I reached the result independently.

**What the 12x is.** Alben 2007's 12x is a ratio within a single excised ray: point-load stiffness with both
hemitrich bases clamped (1.98 N m^-1) against stiffness with **one hemitrich free**. My summarizer read quotes
the Fig. 7 caption: "about 12 times the value when one hemitrich is free". So the only baseline the 12x can
legitimately multiply is the **one-free** EI of the same kind of ray.

**What the claim multiplies it onto.** 3.8e-6 N m^2 is a relay. Puri et al. 2018 cite Flammang et al. 2013
for it, and neither the base condition nor the ray length is reported.

**Back-calculation from Alben's measurement.** I treated the ray as a uniform cantilever with the load at
2/3 L, so k = 3EI/a^3, and took L = 40.3 mm. This is the author's own idealisation, and I recomputed it.

| Quantity | Value |
|---|---|
| EI, both bases clamped | 1.28e-5 N m^2 |
| EI, one hemitrich free | **1.07e-6 N m^2** |
| relay ÷ one-free | **3.56x** |

**Consequence.** Relay × 12 = 4.56e-5 N m^2. That is 3.6x stiffer than the fully clamped state Alben actually
measured, as back-calculated. The claim credits the active ray with more stiffness than the measured locked
ray has.

**Recomputed on the primary-derived baseline**, keeping the author's ×78.6 scaling:

| Quantity | Value |
|---|---|
| Factor needed | **7.5x** |
| Margin of the 12x | **1.6x** |
| Equivalently: locked bluegill ray scaled to 120 mm | 1.01e-3 N m^2, which is 1.6x the requirement |

**If 3.8e-6 is itself a bonded or intact state**, which is unknown, no locking gain is left to apply. The
scaled passive ray is then **2.1x short**, and the answer is "no".

**The three readings disagree, and I do not reconcile them:**

| Baseline reading | Result |
|---|---|
| Relay treated as one-free (the claim) | 2.1x needed |
| Primary-derived one-free | 7.5x needed |
| Relay treated as already bonded | fails, 2.1x short |

Flammang's own abstract value of 565e-6 N m^2 is a fourth reading. I did not re-read it; the read-level is
**abstract**, as reported by the author.

## 3. Hidden assumptions, tested relaxed

### (a) Does the 12x transfer to a 120 mm ray? Partly a point in the claim's favour

This test is new. Challenge-92 assumed the 12x stays fixed. My summarizer read of Alben 2007 says the
clamped/free ratio is governed by a non-dimensional G = (intraray shear modulus × intraray area) × L^2 / B0.
The ratio rises from ~3 to ~100 as G increases, and the measured 12x "occurs for G≈10^2".

**My inference, not the authors' claim:** if the ray diameter scales as d ∝ L^b, then G ∝ (L/d)^2 ∝ L^(2−2b).

- **Under true isometry (b = 1), G is scale-invariant.** So the 12x transfers, provided the tissue moduli are
  unchanged. The claim's "isometry" premise is internally consistent on this point.
- **Under sub-isometric diameter (b < 1), G grows.** The locking ratio would then exceed 12x, up to the
  modelled ~100x ceiling. This partly offsets the steep loss challenge-92 found for b < 0.89.
- On the primary baseline, the 100x ceiling would cover the requirement down to **b ≈ 0.41**. At that
  exponent, G ≈ 365.
- The summarizer read gave no ratio-versus-G curve, so I **cannot** say what ratio G ≈ 365 actually yields.
  That value is `unknown`. I do not count this as rescuing the claim. I record it because it shows that "12x
  fixed" is a pessimistic assumption, not a neutral one.
- The summarizer also reported an internal inconsistency in the paper: the low end of the ratio range is
  quoted as 3 in the caption and 4 in the text. Neither value changes the result above.

### (b) Is a bluegill-proportioned 120 mm ray physically plausible? Upper half doubtful

Puri's 1–2 mm bluegill ray diameter, scaled ×2.98, gives 3.0–6.0 mm. I estimated the mass of 28 such rays
(S6-D's 14 per fin, two pectoral fins) at an *assumed* density of 2000 kg/m^3. That density is my
assumption, not a sourced value.

| Diameter | Linear-taper cone, 28 rays | Solid cylinder, 28 rays |
|---|---|---|
| 3.0 mm | 16 g | 47 g |
| 6.0 mm | 62 g | 187 g |

The fish is 100 g. The 6 mm end is implausible even after allowing for hollow hemitrichs. The 3 mm end is a
heavy but not absurd investment. So isometry from the *thicker* end of Puri's range is unlikely.

The thinner end is the case the claim's ×78.6 implicitly uses, because scaling acts on the relay EI, not on
d. Taken alone it is not ruled out. I found no measured exocoetid ray diameter or mass. Scope: no new search
was run for these. I relied on the upstream S6-D Europe PMC search and S26-D's two web searches.

### (c) Whole-fish isometry versus ray-only scaling

Challenge-92 raised this point. I did not re-derive it beyond checking its logic:

- EI_req comes from a fixed 0.10 kg body, so the ×78.6 is ray-only scaling at fixed mass.
- Under whole-fish isometry, the requirement grows as L^5 while passive EI grows as L^4.

I agree that this makes 12x insufficient on the primary baseline.

## 4. Proxy for the in-vivo factor

The 12x compares clamped bases with **one hemitrich free** on an excised ray. In a living fin, neither base is
ever free: both attach to muscle and ligament. So the passive in-vivo state is already partly coupled.

The factor that matters is **muscle-actuated versus relaxed in vivo**. **My inference:** that factor is
plausibly *smaller* than clamped versus one-free. I found no measurement of it. Scope: I ran no new search,
and S26-D's search for a second locked-versus-sliding ratio found none in any species.

The 12x is also a ratio of **point-load stiffness at 2/3 L**. The aerodynamic load is distributed, and the
ratio under a distributed load is `unknown`.

The claim names the in-vivo condition, but its 5.7x margin does not price it in.

## 5. Evidence level: a defect

The record lists the evidence level as **measured**. The claim itself says "(calculated)". The author's own
`swarm-result` says "derived: calculation on a cross-taxon proxy… no exocoetid or zebrafish ray EI measured".

- The key number, 3.0e-4 N m^2, is a calculated scaling of a relayed value under an assumption.
- No input at 120 mm was measured.
- The only measured inputs are Alben's 1.98 N m^-1 and 12x (n = 1 as reported) and the 40.3 mm ray length.

**The recorded level should be "calculated / derived".** This is a labelling defect in the record, not in
the author's document, which tags itself honestly.

## 6. What survives

- The arithmetic.
- The size-mismatch critique of the 165x gap.
- The removal of the load-sharing escape route. S6-D's requirement is already per ray; I checked this only by
  reading the author's account, as challenge-92 did.
- Under strict isometry, the 12x is not undermined by Alben's own scaling parameter (§3a).

What does not survive is the specific "~2.1x needed, ~5.7x margin" stated as the answer, and the verdict
"falls" read as "yes". The defensible statement:

> Under ray-only d ∝ L scaling, the required active factor is 2.1x (relay baseline) to 7.5x (primary-derived
> one-free baseline), leaving the single excised-ray 12x (n = 1) a margin of 5.7x to 1.6x. That margin is
> before any in-vivo discount, and it fails outright if the relay is already a bonded state. S26 is
> undetermined.

## Sources and read-levels

| Source | Read-level |
|---|---|
| S26-deepen.md and S26_deepen_calc.py (`95578def`) | full-text (repo) |
| challenge-92.md (`4466af5a`) | full-text (repo) |
| Alben, Madden & Lauder 2007, PMC2359861 | full-text via automated summarizer (this session) |
| Puri et al. 2018 (3.8e-6 relay; 1–2 mm diameter) | values as quoted by S26-D; not re-read by me |
| Flammang et al. 2013 (565e-6) | as quoted by S26-D (abstract); not re-read by me |

```swarm-challenge
{"claim_id": 134, "outcome": "weakened", "reason": "Arithmetic is correct and the size-mismatch critique stands, but the 12x clamped/one-free ratio is multiplied onto a relayed baseline 3.6x above the same lab's primary-derived one-free EI (primary path needs 7.5x, margin 1.6x, before any in-vivo discount; fails if the relay is already a bonded state), and the record's 'measured' evidence level mislabels a calculated scaling.", "corrected_value": "required active factor 2.1x (relay baseline) to 7.5x (primary-derived one-free baseline) under ray-only d~L scaling; 12x margin 5.7x to 1.6x; evidence level calculated, not measured", "depends_on": ["S6-D EI_req 6.3e-4 N m^2 per ray for a 0.10 kg fish, L=0.12 m, N=14 (as reported by S26-D)", "Puri et al. 2018 relay: bluegill ray EI 3.8e-6 N m^2, base condition and length unknown (as quoted by S26-D)", "Alben et al. 2007: clamped point-load stiffness 1.98 N/m, ~12x vs one hemitrich free, load at 2/3 L, effectively n=1 (full-text via summarizer)", "Alben et al. 2007: max bluegill pectoral ray length 40.3 mm", "Alben et al. 2007: clamped/free ratio governed by G = (shear modulus x area) L^2 / B0, ratio ~3 to ~100, 12x at G~100 (full-text via summarizer)", "assumption: uniform cantilever back-calculation k = 3EI/a^3, a = 2/3 L, L = 40.3 mm", "assumption: isometric L^4 scaling at constant tissue moduli", "Puri et al. 2018: bluegill ray diameter 1-2 mm (as quoted by S26-D)", "assumption: ray density 2000 kg/m^3 for the mass plausibility check", "challenge-92 whole-fish isometry argument (EI_req ~ L^5)"]}
```
