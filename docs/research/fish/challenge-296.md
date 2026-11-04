# Challenge 296: adversarial review of S18-D-D (loop delay)

Claim under review: claim 296, `[S18-D-D]`, from `harvest:deepen-s18-sensitive-input-rmpica`. I read the source document `docs/research/fish/S18-D-deepen.md` in full on `origin/claude/deepen-s18-sensitive-input-rmpica`. Recorded evidence level: **derived**.
Date: 2026-11-04. Evidence level of this review: **derived**. It contains my own numerical computations plus one literature detail at search-summary level. Nothing here is a new observation.

**Outcome: WEAKENED.** The arithmetic survives an independent recomputation. The conclusion survives: active control is undetermined, and passive stability is the default at ≥ 2 m/s. Two parts of how the claim gets there do not survive:

- **(a)** For the pitch axis, the latencies do not "straddle" the limit.
- **(b)** 118 ms is the limit for delayed PD control only, not for a delayed controller in general.

## 1. Arithmetic, redone independently

I used a different method from the author's. The author used D-subdivision with a curve expansion. I used Chebyshev pseudospectral discretisation of the delay equation and computed its rightmost eigenvalue. For the acceleration-feedback case I counted right-half-plane roots with an argument-principle winding count. Scripts: `challenge-296.py`.

| Quantity | Author | Mine | Status |
|---|---|---|---|
| I_y = mL²/12 | (implicit) | 5.33×10⁻⁸ kg m² | — |
| λ at 1 / 2 / 3 m/s | 6 / 12 / 18 s⁻¹ | 6.00 / 12.00 / 18.00 s⁻¹ | reproduced |
| PD hard limit √2/λ at 2 m/s | 118 ms | 117.9 ms | reproduced (a stabilising PD gain set exists at λτ = 1.0; none found at λτ ≥ 1.43) |
| Gain-margin metric | k_p,max/k_p,min across the whole stable pocket | **Loop-gain margin K_max/K_min**, with k_p and k_d scaled together along a fixed controller direction. This is the conventional definition, and the one I tested to see whether the author's metric overstated robustness. | see next row |
| Margin at λτ = 0.3 / 0.5 / 0.61 / 0.84 / 1.0 / 1.26 | 6.6 / 2.7 / 2.0 / 1.34 / 1.14 / 1.02 | 6.55 / 2.70 / 1.98 / 1.33 / 1.14 / 1.008 | reproduced. My suspected flaw did not materialise: the two metrics agree. |
| Robust (6 dB) limit at 2 m/s | 51 ms | 0.609/12 = 50.8 ms | reproduced |
| V_max at 70 ms, hard / robust | 3.4 / 1.45 m/s | 3.37 / 1.45 m/s | reproduced |
| Aerodynamic tail pitch damping (author ignored it) | — | c = 0.72·V s⁻¹. The unstable root falls from 12.0 to 11.3 s⁻¹ at 2 m/s. | My inference: this moves the limits by about +6 %, which is immaterial. |

## 2. Proxy: the right axis is pitch, and pitch does not straddle

The author left the axis open: "I do not know which axis the non-roll jet strikes excited, and pitch is the axis that matters." A search summary of Webb 2004 (*J Exp Biol* 207:955–961, doi:10.1242/jeb.00854; read-level **search-summary**, full text could-not-access in this session) says this:

> "There were no differences in latencies for slip, heave, yaw and pitch disturbances within each species … Rolling disturbances produced a shorter response, with an overall latency of 70±15 ms."

So, per that summary, **pitch belongs to the non-roll group: 123 ± 19 ms (chub), 201 ± 24 ms (bass), 208 ± 52 ms (bluegill).** The 70 ms value is the roll latency.

My inference from that, under the claim's own PD model at 2 m/s (λ = 12 s⁻¹):

- **Pitch proxies.** The chub value gives λτ = 1.48. All three pitch values exceed the 118 ms hard limit. The cyprinid's 123 ± 19 ms overlaps the limit only at its lower 1-SD edge.
- **"Straddle".** The two measurements straddle 118 ms only because one of them is a roll measurement. For the pitch mode that S18 models, the proxies sit on the infeasible side.
- **"Favourable proxy".** The phrase "robust only below ~1.45 m/s even with the favourable proxy" applies an off-axis number. For pitch at 123 ms, the robust limit is 0.83 m/s and the hard limit is 1.9 m/s. Both are computed, and both are the author's own table values.

A further proxy problem the author did not name: Webb's stimuli were flow-refuge removal and water-jet strikes on the body. Detecting those may involve the lateral line and touch, not just the vestibular system. In air the lateral line has no flow to sense. That is my inference, and I cannot quantify it. So even the pitch value is a latency to an in-water mechanosensory stimulus, not a vestibular pitch loop in air. It is the right axis but not the right sensory channel.

These points push the claim toward **less** feasibility. The claim's bottom line, "undetermined, passive stability default", is not threatened by them. What is wrong is the description that the claim is "on the boundary at 2 m/s".

## 3. Hidden assumption: PD-only. Relaxed, the hard limit moves

The claim calls √2/λ "the exact delayed-PD limit". That is correct as stated. A search summary (read-level **search-summary**) cites three things:

- Insperger, Milton & Stépán, *J R Soc Interface* 10:20120763 (2013), "Acceleration feedback improves balancing against reflex delay".
- A 2022 *J Sound Vib* paper (doi 10.1016/j.jsv.2022.116898). It states that a delayed PDA (proportional–derivative–acceleration) controller's critical delay is about 1.73× (√3, inferred from garbled text) that of PD.
- For PD, the summaries did **not** confirm √2, so that value rests on the author's derivation and my numerical check above.

**My computation, not a citation.** For θ̈ − λ²θ = −k_p θ(t−τ) − k_d θ̇(t−τ) − k_a θ̈(t−τ), I found stabilising gain sets (zero right-half-plane roots by winding count):

- at λτ = 1.48, with (k_p, k_d, k_a) = (1.002λ², 1.498λ, 0.30). This is the chub pitch latency at 2 m/s.
- at λτ = 1.6, with (1.01λ², 1.67λ, 0.50).
- at λτ = 1.75 (146 ms at 2 m/s), with (1.002λ², 1.772λ, 0.65).

My coarse grids found none at λτ ≥ 1.9. Those grids had k_a ≤ 0.9, and the pocket shrinks as k_a → 1, so this is **not** evidence of a limit at 1.9. I did not pin down the PDA limit. The literature's √3 × 118 ≈ 204 ms is **unverified by me**.

**What this means (my inference).** With delayed angular-acceleration feedback, 123 ms is stabilisable at 2 m/s in principle. "Any controller" therefore does not exclude the pitch proxy. The stable pockets I found are knife-edge (k_p within 0.2 % of λ²), so robust 2 m/s control is still not shown. Whether a fish's canals or other sensors provide usable angular-acceleration feedback in air: **unknown**, not searched.

The claim does disclose a related limitation in its source document ("a predictive controller can in principle exceed PD limits"). PDA is not prediction, though, and the claim sentence presents 118 ms as "the exact limit" without the PD qualifier being load-bearing.

A second relaxable assumption, which the author disclosed: λ = 6V assumes the unstable static margin has the same magnitude as the stable one. Since λ ∝ √|SM|, a margin at 25 % of that magnitude halves λ. Then the PD hard limit at 2 m/s becomes 236 ms and the robust limit 102 ms (computed). An only-mildly-unstable airframe tolerates the pitch proxy. This does not refute "passive stability is the default". It does mean the thresholds in the claim belong to one airframe, not to "an unstable airframe" in general.

## 4. Evidence level

"Derived" is honest. The latencies are labelled search-summary, and both the heuristic and the computed limits are labelled as computations. One defect of wording: the key number puts the 70 ms roll value beside the pitch-mode limit as if they were commensurate.

## 5. Counter-examples and scope of my searches

- I ran 2 web searches on 2026-11-04 (standard mode): Webb 2004 methods, and delayed PDA critical delay. I did not find adult *Danio* pitch latency, and did not search for it beyond what the author had already searched. Webb's fish sizes, frame rate and latency definition remain **unknown**: the search summary gave only "the interval from a disturbance to the fish's response".
- Taxon: in Webb 2004 the latencies vary by species (123 to 208 ms for non-roll disturbances). The cyprinid (chub) is the fastest of the three and the closest relative of *Danio*. I preserve the spread and do not average it.

## 6. Verdict

- **Arithmetic:** survived. I reproduced it with an independent method.
- **"Straddle the limit" and "robust below ~1.45 m/s even with the favourable proxy":** weakened. Per Webb 2004 (search-summary), pitch is in the 123–208 ms group. Under PD, all pitch proxies exceed 118 ms at 2 m/s, and the 1.45 m/s figure uses a roll latency.
- **"Exact limit 118 ms":** exact for PD only. Under delayed PDA feedback I computed knife-edge stabilisability at λτ up to at least 1.75 (≥ 146 ms at 2 m/s).
- **Conclusion** ("active control undetermined; passive stability default for ≥ 2 m/s"): survives, and the pitch-axis correction pushes it further toward passive stability.

```swarm-challenge
{"claim_id": 296, "outcome": "weakened", "reason": "Arithmetic reproduces independently (118 ms, 51 ms, 1.45 m/s), but per Webb 2004 (search-summary) pitch belongs to the 123-208 ms non-roll group, so for the pitch mode the latencies do not straddle the PD limit (chub lambda*tau = 1.48), and 118 ms is a PD-only limit: delayed acceleration feedback is computed to stabilise (knife-edge) up to at least lambda*tau = 1.75 (146 ms at 2 m/s).",
  "corrected_value": "pitch-axis proxy 123+/-19 ms (chub) > 118 ms PD hard limit at 2 m/s (lambda*tau = 1.48, computed); with delayed PDA feedback, stabilisable but knife-edge to >=146 ms at 2 m/s (computed)",
  "depends_on": [
    "S18 reference geometry: m=0.4 g, L=4 cm, I_y=mL^2/12, S_t=1 cm^2, l_t=2 cm, a_t=1.6/rad, rho=1.2 kg/m^3 (assumed)",
    "S18 convention lambda = 6.0*V s^-1 (unstable |static margin| equal to stable margin; assumed)",
    "Webb 2004 J Exp Biol 207:955: roll latency 70+/-15 ms; slip/heave/yaw/pitch 123+/-19 (chub), 201+/-24 (bass), 208+/-52 ms (bluegill), pitch grouped with non-roll (search-summary only)",
    "Linear single-axis pitch model with delayed PD or PDA feedback (my Chebyshev pseudospectral and argument-principle computations)",
    "Robustness criterion: loop-gain margin >= 2 (6 dB)",
    "Insperger, Milton & Stepan 2013 J R Soc Interface 10:20120763 and 2022 J Sound Vib PDA critical-delay result (search-summary; used only qualitatively, sqrt(3) ratio not verified)",
    "Cross-species, cross-medium transfer of teleost in-water postural latency to adult zebrafish pitch control in air (unverified)"
  ]}
```
