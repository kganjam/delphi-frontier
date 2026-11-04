# Challenge 270: adversarial review of the S32 low-end exit claim

**Claim under review** (from S32-organism.md, branch `claude/s32-multi-stroke-launch-qpq9g2`, §3.1 and the answer line):

> "FROM THE LOW-END EXIT (0.45 m/s) it fails on WEIGHT SUPPORT, not thrust: the lobe would need CL 1.3-10 to hold the body clear of the water. Minimum supportable speed is 0.51-1.39 m/s"

Recorded evidence level: derived. Recorded value: 10 (CL required).

**Verdict: WEAKENED.** The arithmetic reproduces exactly. The "fails, not thrust" conclusion survives at the central and stingy ends. **The generous end (CL 1.27, U_min 0.51 m/s) is not a shown failure.** Two things carry it: an unswept assumed cap CL_z,max = 1, and the assumption that the lobe's vertical force can come only from forward-speed lift. Relax either one, within ranges the literature supports, and the generous case can be supported at 0.45 m/s.

Source read-level: S32-organism.md and S32_taxi.py were read in **full-text** from the git branch above.

---

## 1. Independent arithmetic

I took the inputs from S32's tables (§2, §3.1) and the scenario dictionary in S32_taxi.py, not from its working:

| Input | Value |
|---|---|
| Body mass | 0.25 g (generous, central), 0.40 g (stingy) |
| Lower lobe area | 18.9 mm² |
| Immersed fraction φ | 1 / 0.5 / 0.25 |
| Fin chord c | 6 mm |
| Surface tension σ | 0.072 N/m |
| Contact angle cosθ | 0 / 0.5 / 1 |
| V_to | 4.41 m/s, or 5.58 m/s for the 0.40 g fish |

Wing lift below V_to is W·(U/V_to)², because the wing is at CL_max. The vertical balance is:

½ρ_w U² S_imm CL_z = W[1 − (U/V_to)²] + 2σc·cosθ

My script is `docs/research/fish/challenge-270_check.py`. These numbers are **calculated, not observed**:

| Case | W (mN) | Needed from lobe (mN) | q·S_imm at 0.45 m/s (mN) | **CL_z needed** | **U_min at CL_z = 1** |
|---|---|---|---|---|---|
| Generous | 2.453 | 2.427 | 1.914 | **1.27** | **0.51 m/s** |
| Central | 2.453 | 2.859 | 0.957 | **2.99** | **0.77 m/s** |
| Stingy | 3.924 | 4.762 | 0.478 | **9.95** | **1.39 m/s** |

These match S32 to the stated precision. **No arithmetic fault.**

I also checked "not thrust" by removing the support requirement, which sets the induced drag D_ind to 0. S32's own §3.1 forces at 0.45 m/s then give these net values (my inference from the author's tabulated terms):

- generous: +4.09 mN (no D_ind was large here)
- central: 1.76 − 0.01 − 0.09 = **+1.66 mN**
- stingy: 0.61 − 0.01 − 0.26 = **+0.34 mN**

So the negative nets S32 reports for central and stingy at 0.45 m/s come entirely from induced drag on the support lift. **"Fails on weight support, not thrust" is internally consistent.**

## 2. Proxy check: is ½ρ_w U² S_imm CL_z the right quantity for vertical force?

It is a proxy, and the error runs in **both directions**:

- **More pessimistic than stated.** S_imm is the *lateral* area of a vertical, uncanted fin. S32 notes this itself under "Not modelled". For a fin like that, the area that can make vertical force from forward speed by angle of attack is near zero unless the lobe rolls or cups. On this reading the generous case is worse than CL 1.27.
- **More optimistic than stated.** The flow that matters for a flapping lobe is not U alone. The lobe's peak lateral speed is π·f·A_pp = **1.04–1.41 m/s** (calculated from S32's f·A_pp = 0.33–0.45 m/s). That is 2.3–3.1× the 0.45 m/s forward speed. The same flapping produces S32's thrust term G, which does not depend on U. Restricting vertical force to the U-based term ignores the larger, flapping-driven force.

The right quantity is the **time-averaged vertical component of the total hydrodynamic force on the flapping lobe**. Forward-speed lift is only one part of it.

## 3. Hidden assumptions, relaxed

### 3a. CL_z,max = 1 is assumed and was never swept

S32 §2 labels it "ASSUMED". The §3.3 sensitivity table covers nine factors but not this one. My calculation of U_min against the cap:

| CL_z,max | Generous | Central | Stingy |
|---|---|---|---|
| 1.0 | 0.51 | 0.77 | 1.39 |
| 1.3 | **0.44** | 0.68 | 1.22 |
| 1.5 | **0.41** | 0.63 | 1.14 |
| 2.0 | **0.36** | 0.55 | 0.99 |

The generous case needs CL_z 1.27, only 27 % above the assumed cap. Steady low-AR plates already reach CL around 1.2 at high incidence. That figure is from memory, not read this session (Torres & Mueller 2004 is the reference I have in mind; read-level **could-not-access**).

Flapping and unsteady foils at Re ~10²–10⁴ hold CL ≈ 2 for 2–4 chords of travel by delayed stall (read-level **search-summary**: Wu & Sun; and a Beihang NACA 0012 study at Re 100 reporting a mean CL > 2 against a steady value of 0.9). The lobe's chord Re at 0.45 m/s is about 2,700, which is inside that range.

**Result: with any cap ≥ 1.3, the generous end supports at 0.45 m/s.** The central and stingy ends still fail up to CL_z,max ≈ 3. Stingy fails even at a cap of 2.

### 3b. Thrust-vector tilt (heterocercal-type lift from a flapping homocercal tail)

S32 assumes that the zebrafish lobe, having no hypocercal cant, makes no vertical force except by U-based lift. Published work contradicts the general form of that assumption:

- Bluegill homocercal tails work asymmetrically top to bottom. The wake implies an anterodorsal reaction force, i.e. lift.
- A robotic bluegill caudal fin produced lift **of similar magnitude to thrust** under undulatory ray motion (Esposito, Tangorra, Flammang & Lauder 2011, J. Exp. Biol.).

Both are read-level **search-summary**: abstracts and excerpts via the search engine. I did not read the papers, and I have not confirmed their quantitative values.

Applied as a bound to S32's own forces at 0.45 m/s (my inference, using S32's calibrated thrust):

| Case | Lobe force available (mN) | Vertical force needed (mN) | Ratio needed / available | Outcome |
|---|---|---|---|---|
| Generous | 4.66 | 2.43 | **0.52** | A ~31° tilt would hold the body up and leave ~4.0 mN of forward force |
| Central | 1.76 | 2.86 | 1.62 | Fails even if all of the force were redirected vertically |
| Stingy | 0.61 | 4.76 | 7.8 | Fails even if all of the force were redirected vertically |

There is no measured evidence that a zebrafish lobe can do this **with the body in air and the lobe piercing the surface**. No search I ran found one; the scope is stated below. This is a demonstrated *possibility*, not a demonstrated mechanism. Even so, it is enough to stop "fails" from standing as a result at the generous end.

## 4. Is the evidence level honest?

Yes. "Derived" is correct, and the source states it is computed from an RK4 script with assumed φ, CL_z,max and contact angles. The recorded value "10" is the stingy upper bound of the 1.3–10 range. It is not mislabelled, but on its own it overstates the typical case.

One wording defect: the claim says "it fails" without qualification across the whole range. At the generous end, the failure is an artefact of the assumed CL_z,max = 1.

## 5. Regimes and counter-examples the author missed

- **Unsteady or flapping lift** (§3a) and **asymmetric homocercal tail lift** (§3b), as above.
- **Partial-immersion swimming.** The binary "airborne or ordinary surface swimming" leaves out a body partly submerged and partly carried by buoyancy. That regime is not modelled here or in S32. Its drag lies between the two extremes, so the outcome is `unknown`, not shown to be worse.
- I found **no counter-example** of a sub-gram fish holding its body clear of the water at about 0.45 m/s.
  - The guppy data S32 cites (1.02 → 1.24 m/s in air) start above the generous U_min and do not test this point.

**Scope of negative searches:** two web searches, both read-level search-summary:
1. homocercal caudal-fin vertical lift (bluegill, Lauder);
2. flapping-foil time-averaged CL above 1 at low Re.

I did not search for surface-piercing flapping-fin vertical force measurements at zebrafish scale, and found none in passing.

## 6. Corrected statement

From the 0.45 m/s exit, holding the body airborne would need CL_z 1.27 / 2.99 / 9.95 (generous / central / stingy). This is calculated, and the arithmetic is confirmed.

- **Central and stingy fail on weight support, robustly.** The vertical force they need is 1.6–7.8× the *total* force the lobe produces, so neither a higher CL cap nor tilting the thrust rescues them.
- **The generous case is not a demonstrated failure.** Its 0.51 m/s minimum depends on the unswept CL_z,max = 1. It falls to 0.36–0.44 m/s for CL_z,max 1.3–2, and tilting the flapping thrust could also support it.

The defensible range for the minimum supportable speed is therefore **about 0.36–1.39 m/s**, conditional on CL_z,max between 1 and 2. It is not 0.51–1.39 m/s.

This does not rescue the taxi overall. S32's ceiling argument is separate from this claim and is not examined here.

```swarm-challenge
{"claim_id": 270, "outcome": "weakened", "reason": "Arithmetic reproduces exactly and central/stingy cases robustly fail on support, but the generous end (CL 1.27, U_min 0.51 m/s) rests on an unswept assumed CL_z,max = 1 and on excluding flapping-driven (thrust-tilt) vertical force, either of which, relaxed within published ranges, permits support at 0.45 m/s.",
  "corrected_value": "CL_z required 1.27/2.99/9.95 (gen/cen/stingy); 'fails' holds for central and stingy only; minimum supportable speed ~0.36-1.39 m/s for CL_z,max 1-2 (not 0.51-1.39 m/s)",
  "depends_on": ["S32 low-end exit speed 0.45 m/s", "S32 lower-lobe area 18.9 mm2 (assumed) and immersed fraction 0.25/0.5/1.0 (assumed)", "body mass 0.25/0.40 g", "S28 V_to 4.41/5.58 m/s with wing lift W(U/V_to)^2", "meniscus force 2*sigma*c*cos(theta), c 6 mm, cos(theta) 0/0.5/1 (assumed)", "S32 burst-calibrated lobe thrust at 0.45 m/s: 4.66/1.76/0.61 mN", "S32 force terms at 0.45 m/s (D_wing, F_sigma,h) for the not-thrust check", "flapping-foil CL ~2 by delayed stall at Re 1e2-1e4 (search-summary, Wu & Sun; Beihang NACA0012)", "homocercal tail lift comparable to thrust (search-summary, Esposito et al. 2011 JEB; Lauder bluegill)"]}
```
