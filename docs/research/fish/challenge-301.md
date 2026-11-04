# Challenge 301: adversarial review of claim [S3-D] (S3 launch-power shortfall vs CL_max)

**Claim under review** (the author's, quoted from the claim card, source `harvest:s3-mass-power-budget-rcrklv`):
> S3's launch-power shortfall scales as CL_max^-1.5, and CL_max is the only input whose factor-2 error reaches parity. Replacing the Re-matched dragonfly-wing proxy (1.07) with the flying-fish fin-wing bracket 1.0-1.1 gives a calculated 2.75-3.17x shortfall in the most generous case. Closure needs CL_max >= 2.16, about 2x any steady insect or fin-wing value found. The power verdict stands. The sub-claim "fin tissue cannot carry itself at 1.38 m/s" weakens to near break-even (margin 1.01-1.25).

**Outcome: WEAKENED.** The arithmetic holds. The numerical bound holds for a *steady*, fixed-wing CL. The claim's label "most generous case" is not supported, because the input is a steady-state CL_max proxy. Published evidence from the same proxy taxon says free-flying wings beat that value. The power verdict is not refuted, but the closure gap is open, not settled.

**Scope note.** The source harvest (`s3-mass-power-budget-rcrklv`) and any S3 design document are **not in this repository**. I searched every branch for "S3", "CL_max", "dragonfly", "flying fish", "1.38 m/s" and "launch power"; none were found. Everything below therefore works only from the inputs stated in the claim. That means I could not check the S3 mass, power or speed inputs, nor how CL^-1.5 was derived for S3.

---

## 1. Independent arithmetic (calculated by me, not copied)

Starting from the stated law P_short ∝ CL_max^-1.5 and the stated endpoint 2.75x at CL = 1.1:

| Quantity | My calculation | Claim | Match |
|---|---|---|---|
| Shortfall at CL = 1.0 | 2.75 × (1.1/1.0)^1.5 = 2.75 × 1.1537 = **3.173** | 3.17 | yes |
| Shortfall at the 1.07 proxy | 2.75 × (1.1/1.07)^1.5 = **2.87** | (not stated) | — |
| CL_max for closure (shortfall = 1) | 1.1 × 2.75^(2/3) = **2.159**; also 1.0 × 3.17^(2/3) = 2.158 | 2.16 | yes |
| Closure CL ÷ dragonfly proxy | 2.16/1.07 = **2.02** | "about 2x" | yes |

The range, the closure threshold and the "about 2x" figure all follow from the stated law. **No arithmetic defect.**

**Fin-tissue margin 1.01-1.25: I cannot reproduce it from the stated inputs.** Self-support lift scales as CL to the power 1 at fixed speed and area. A CL span of 1.0-1.1 should therefore give a margin span ratio of 1.10. The stated span ratio is 1.25/1.01 = 1.24, which would need margin ∝ CL^2.24 (calculated). So that range must also carry some other input that the claim does not state, such as the tissue areal density. I am not calling it wrong. It is **unverified**, because its inputs are not in the claim or the repo.

## 2. Proxy: a steady fixed-wing CL_max stands in for the launch lift coefficient

The quantity that matters for launch is the **mean lift coefficient the wing actually reaches during the launch stroke**. Both the 1.07 and the 1.0-1.1 values are **steady-state (fixed-wing or gliding) maxima**:

- **Flying fish.** Park & Choi measured lift and drag on stuffed whole-fish models in a wind tunnel (J. Exp. Biol. 2010; also IUTAM 2007 proceedings). Read-level: **search-summary** (abstract text quoted in a search result, not opened). This is a whole-body, gliding, fixed-geometry coefficient, not a coefficient for a fin-wing that flaps or is driven.
- **The CFD value 1.03** is attributed in my search to **Deng, Zhang, Liu & Mao (2019)**, a CFD model built on Park & Choi's fish morphology, and not to Park & Choi themselves. Read-level: **search-summary**. The claim tags "1.03 CFD, abstract" without naming this paper. That is an attribution gap, not a numeric error.
- **Dragonfly.** Wakeling & Ellington 1997, *Dragonfly flight I* (J. Exp. Biol. 200:543-556). Read-level: **search-summary**. The highest *gliding* CL it records is 0.93, with a note that this may not be the maximum. The search did **not** surface the 1.07 value, so I cannot confirm where the claim's 1.07 comes from. Its value: `unknown` to me (not checked against the full text).

**Counter-evidence in the proxy's own taxon.** Wakeling & Ellington 1997, *Dragonfly flight III: quasi-steady lift and power requirements* (J. Exp. Biol. 200:583-600). Read-level: **search-summary of the abstract**. In free flight of *Sympetrum sanguineum* and *Calopteryx splendens*, the **maximum mean lift coefficient required exceeded the steady maximum CL**. The damselfly's mean CL was higher still, which the authors attribute to clap-and-fling. Companion *Part II* (J. Exp. Biol. 200:557, search-summary) states that quasi-steady mechanisms appear insufficient to explain the lift flying dragonflies need. Separately, Usherwood & Ellington 2002 (*Aerodynamics of revolving wings I/II*, J. Exp. Biol. 205:1547, 1565; search-summary) report "high" lift coefficients on steadily *revolving* model wings, from a stable leading-edge vortex. I could **not** obtain their numerical CL_max: `unknown`. I tried two searches and did not open the full-text PDFs.

**My inference** (not the author's): a launch is a short, powered, unsteady event. Using the steady CL_max as the "most generous case" is therefore not generous. It is a quasi-steady lower bound on what a flapping or driven wing can reach. The phrase "about 2x any *steady* insect or fin-wing value" is literally true. But "steady" is precisely the restriction that makes the gap look closed. No unsteady insect or fin-wing value was compared against 2.16.

## 3. Hidden assumptions, tested relaxed

1. **The CL^-1.5 law holds CD fixed.** P = W·v·CD/CL with v ∝ CL^-0.5 gives P ∝ CD·CL^-1.5 (my derivation; the claim gives no derivation). Near CL_max, CD climbs steeply. Relaxing this assumption makes the real shortfall *larger* at CL_max, so it **favours the verdict**: the 2.75x is optimistic in that respect.
2. **Lift is steady and quasi-static (see §2).** Relaxing this assumption **cuts against the verdict**. The mean launch CL may exceed 1.1, by an amount the stated evidence does not bound. Whether it reaches 2.16 is `unknown`. I found no published unsteady fin-wing CL, and I make no claim that 2.16 is reachable.
3. **"CL_max is the only input whose factor-2 error reaches parity."** I cannot test this, because the other inputs (mass, muscle power density, launch speed) are not in the repo. Unverified.

Net effect: (1) and (2) push in opposite directions. The claim's single bracket captures neither.

## 4. Evidence level

The claim is recorded as **derived**. That is honest: the shortfall range and the 2.16 threshold are calculations, and the claim says "calculated". The CL inputs are cited at **search-summary / abstract** level, which is also correctly disclosed. One small defect: the 1.03 CFD value is not attributed to its actual source (Deng et al. 2019, per my search-summary).

## 5. Verdict

- **Survives:** all the arithmetic; the closure threshold of 2.16 (calculated); the fact that no *steady* value found comes near 2.16.
- **Weakened:** the "most generous case" framing, and with it the force of "the power verdict stands". The bound rests on a steady CL_max proxy. Wakeling & Ellington 1997 (III, abstract via search-summary) shows that free-flying dragonflies, the claim's own proxy taxon, exceed that proxy. The verdict should read: *the shortfall is 2.75-3.17x under quasi-steady aerodynamics; whether unsteady launch lift closes the remaining ~2x gap is unknown.*
- **Unverified:** the 1.01-1.25 tissue margin (cannot be reproduced from the stated inputs) and the 1.07 dragonfly value (not found in the search-summary of the cited source).

Sources (all search-summary unless stated):
- Wakeling & Ellington 1997, Dragonfly flight I, II, III, J. Exp. Biol. 200:543, 557, 583: https://cob.silverchair.com/jeb/article-pdf/200/3/557/3403905/jexbio_200_3_557.pdf ; https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/3806925
- Usherwood & Ellington 2002, J. Exp. Biol. 205:1547 and 1565: https://cob.silverchair.com/jeb/article-split/205/11/1547/8997/The-aerodynamics-of-revolving-wings-I-Model
- Park & Choi, IUTAM 2007 proceedings and J. Exp. Biol. 2010: https://eng-web77-v02.ocio.monash.edu/intranet/proceedings/iutam2007/pages/pdf/S1_Park.pdf
- Deng et al. 2019, flying-fish CFD: https://pure.bit.edu.cn/zh/publications/numerical-prediction-of-aerodynamic-performance-for-a-flying-fish/

```swarm-challenge
{"claim_id": 301, "outcome": "weakened", "reason": "Arithmetic reproduces exactly (3.17x at CL 1.0, closure at CL_max 2.16), but every CL input is a steady fixed-wing/gliding maximum while launch is unsteady, and Wakeling & Ellington 1997 (III, abstract) report free-flying dragonflies exceeding their steady CL_max, so 2.75x is a quasi-steady bound and not the 'most generous case'; the 1.01-1.25 tissue margin cannot be reproduced from the stated inputs.", "corrected_value": "shortfall 2.75-3.17x under quasi-steady aerodynamics only (2.87x at the 1.07 proxy, calculated); unsteady-lift shortfall unknown", "depends_on": ["shortfall scales as CL_max^-1.5 with CD held fixed (stated by author, derivation not in repo)", "anchor shortfall 2.75x at CL_max 1.1 (author, source harvest not in repo)", "flying-fish CL_max 1.0-1.1 steady/whole-model (Park & Choi, search-summary)", "Wakeling & Ellington 1997 Dragonfly flight III: free-flight mean CL exceeds steady CL_max (abstract via search-summary)", "S3 launch is a powered unsteady stroke rather than steady gliding (my inference; S3 design not in repo)"]}
```
