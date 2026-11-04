# Replication of claim 296 (S18-D-D): the fish's sensorimotor loop delay

**Status:** an independent re-derivation of the loop delay τ_d. τ_d is S18-D's most sensitive input.
**Date:** 2026-11-04. **Evidence level:** derived. This is a bottom-up estimate built from literature latencies read only at search-summary level. Nothing here is a new observation.

## Contamination disclosure

- **What I did not see.** I did not open the deepen branch (`claude/deepen-s18-sensitive-input-rmpica`) until my value below was fixed.
- **What I did see first.** To learn what S18-D is, I grepped the *parent* file (`claude/deepen-s18-zebrafish-air-3u64z4:docs/research/fish/S18-deepen.md`) for "latenc|delay". That grep showed me three things before I derived anything:
  - S18-D's admissible-delay rule, τ_d ≤ 0.5/λ, which gives 83 / 42 / 28 ms at 1 / 2 / 3 m/s;
  - P2, a synaptic latency of about 2.3 ms;
  - the statement that adult *Danio* latency is "unknown".

  Those numbers are S18-D's *threshold*, not claim 296's value for τ_d.
- **What I read for the airframe model.** I took S18's pitch model from `replicate-284.md` on `claude/s18-vestibular-frequency-z22u8e`.

## Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| A1 | Unstable pitch-mode rate of S18's made-up 0.4 g airframe | λ = ω_n = 6.0·V s⁻¹ | S18 formula and parameters, as reproduced in replicate-284.md. I re-checked the arithmetic: √(½·1.2·1e-4·0.02·1.6 / 5.333e-8) = 6.0. Taking λ = ω_n for the unstable case is S18-D's convention, which I adopted. | listing (secondhand) |
| L1 | Goldfish horizontal VOR latency to a head-velocity step: **18 ms (adducting eye), 20 ms (abducting eye)**, "independent of the initial VOR gain" | Pastor, de la Cruz, Baker, *J Neurophysiol* 72(3):1383–1394 (1994), "Cerebellar role in adaptation of the goldfish vestibuloocular reflex". This is the attribution the search summary gave. | **search-summary**. Fetching the abstract failed: read.qxmd.com, pesquisa.bvsalud.org and pubmed.ncbi.nlm.nih.gov are all DNS-blocked in this session. |
| L1b | Goldfish vertical VOR: eye velocity rises "after a latency of approximately 15 ms" | Search summary of a Dow/Anastasio-related goldfish study. Exact citation: **unknown** (not resolved). | **search-summary** |
| M1 | Pectoral fin muscle (sand dab, in vitro, 17–20 °C): twitch reaches peak in 10–15 ms and relaxes in 20–30 ms | Scanned OCR text (miller-library.github.io taxa-ocr). Original citation: **unknown**. | **search-summary** |
| E1 | Mauthner short-latency C-starts at about 2–12 ms (larval zebrafish) | Search summaries (zfin.org; a JEB 2021 escape-latency paper) | **search-summary**. **Not used for τ_d**: the C-start is a ballistic, all-or-none escape, not a graded corrective reflex. |

**Negative searches**, each one a single standard WebSearch on 2026-11-04:

- "fish vestibular reflex latency milliseconds fin postural response tilt goldfish": no fish fin or postural latency in ms was found.
- "larval zebrafish vestibular tilt evoked swim bout latency ms Schoppik": no behavioural tilt latency was found.
- "fish pectoral fin muscle electromechanical delay": no electromechanical delay value was found.

**Adult *D. rerio* sensor-to-fin latency: unknown.** I did **not** search for whole-body postural-perturbation latencies in adult teleosts. That gap matters (see the comparison section).

## Derivation (my inference, built bottom-up)

τ_d = (vestibular-to-motor-command latency) + (conduction) + (muscle force rise).

- **Central plus sensory latency.** The VOR is the shortest vestibular arc, about three neurons, and it measures 15–20 ms (L1, L1b). That figure already includes the onset of eye-muscle force. I take it as the floor for any vestibular-to-actuator loop.
- **Conduction.** A 3–4 cm fish has a path of a few centimetres. At metres-per-second axon velocities that adds well under 1 ms, which I neglect. This is an assumption: I sourced no conduction velocity.
- **Force rise.** Useful corrective fin force needs muscle force near its peak. That adds up to about 10–15 ms (M1, a different species and an in-vitro preparation). Fin–air force build-up is ignored.

**Result: τ_d ≈ 15–40 ms**, central value about 30 ms. This is calculated, not observed.

- **Lower end, 15 ms:** the VOR onset alone.
- **Upper end, about 40 ms:** 20 ms + 15 ms + slack for an extra spinal synapse and for the vestibulospinal arc being longer than the VOR arc.

### Consequence against the airframe (calculated)

λτ_d at τ_d = 15 / 20 / 35 / 40 ms:

| V (m/s) | λ (s⁻¹) | λτ_d |
|---|---|---|
| 1 | 6 | 0.09 / 0.12 / 0.21 / 0.24 |
| 2 | 12 | 0.18 / 0.24 / 0.42 / 0.48 |
| 3 | 18 | 0.27 / 0.36 / 0.63 / 0.72 |

Three delay limits apply:

- **S18-D's heuristic, 0.5/λ:** 83 / 42 / 28 ms.
- **Proportional-only, 1/λ:** 167 / 83 / 56 ms. A first-order unstable plant with delay and P control is stabilisable only if λτ < 1. This comes from my own control-theory knowledge, not a source I read.
- **Delayed PD on θ'' = λ²θ + u, √2/λ:** 236 / 118 / 79 ms. This is the standard delayed-PD result for an inverted-pendulum plant. It also comes from my own knowledge, not a source I read this session.

With my τ_d of 15–40 ms, the delay heuristic is met at 1–2 m/s and is marginal at 3 m/s. The hard limits are met at every speed.

## My value

**τ_d ≈ 15–40 ms, central about 30 ms**, for a teleost vestibular-to-fin-force loop. This is a bottom-up estimate from a goldfish eye reflex (18/20 ms, search-summary) plus a fin-muscle twitch rise (10–15 ms, search-summary, sand dab).

The uncertainty is large and one-sided:

- The VOR is the *fastest* vestibular arc, so 15–20 ms is a firm lower bound.
- The upper end is a guess. Nothing I read measured a fin or postural reflex latency.
- The estimate is cross-species, made in water, and read only at search-summary level.

## Comparison with the recorded value

I read the deepen branch only after the section above was written. Recorded value (S18-D-D, `docs/research/fish/S18-D-deepen.md`):

- **Main proxy:** τ_d = **70 ± 15 ms**, the roll postural latency in creek chub, smallmouth bass and bluegill (Webb 2004, *J Exp Biol* 207:955).
- **Other disturbances:** 123–208 ms (non-roll).
- **Lower bound:** 18–20 ms (goldfish VOR).
- **Hard delay limit:** √2/λ = 118 ms at 2 m/s.

**Verdict on τ_d: DISAGREE.**

- **Where we agree.** The 18–20 ms goldfish VOR floor matches mine: the same paper, but with a different year attribution. The recorded file itself preserves a 1992-versus-1994 dispute, and my search summary gave the 1994 paper. The √2/λ = 118 ms and 0.5/λ = 42 ms limits also match my arithmetic.
- **Where we differ.** My operative value (15–40 ms) is **2–5× shorter** than the recorded proxy (70 ms, or 123 ms for the cyprinid non-roll case).
- **Which is likely more reliable (my inference).** The recorded value rests on a *whole-animal* behavioural measurement. Mine is a sum of component latencies, and a bottom-up sum is likely to underestimate the true loop delay: it leaves out central integration, motor-pool recruitment and any decision stage. On that basis I judge the recorded proxy more likely to be closer to the operative τ_d. But Webb's latency definition and frame rate are unknown to both of us, and the recorded value is also search-summary only.
- **The disagreement changes the conclusion.** At 2 m/s my τ_d gives λτ ≤ 0.48, which is robustly stabilisable. The recorded 70–123 ms gives 0.84–1.48, which runs from knife-edge to impossible. I am preserving the disagreement, not averaging it.

```swarm-replication
{"claim_id": 296, "my_value": "tau_d ≈ 15-40 ms (central ~30 ms; bottom-up: goldfish VOR 18/20 ms + fin-muscle twitch rise 10-15 ms; all search-summary, cross-species; 15-20 ms is a firm lower bound)", "agrees": false,
  "note": "I reproduce the 18-20 ms VOR floor and the 42/118 ms delay limits, but my bottom-up loop delay is 2-5x shorter than the recorded 70±15 ms (roll) / 123-208 ms (non-roll) whole-body teleost proxy, which I did not find and which is probably the better estimate, so the disagreement is real and moves the 2 m/s verdict from robust to knife-edge/impossible."}
```
