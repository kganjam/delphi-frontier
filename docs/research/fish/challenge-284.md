# Challenge 284: adversarial review of S18-D ("0.5 Hz was a protocol ceiling; the bandwidth argument falls")

Date: 2026-11-04. Reviewer evidence level: **derived** (re-computation plus literature at the read-levels marked). Nothing here is a new observation.
Claim under review: `docs/research/fish/S18-deepen.md` on branch `origin/claude/deepen-s18-zebrafish-air-3u64z4`. I read it in full with `git show`. I did not re-read the parent `S18-behaviour.md`; where I describe S18 below, I rely on S18-D's quotations of it.

## Verdict in one line

**WEAKENED.** The diagnosis is correct: 0.5 Hz was a protocol ceiling, not a bandwidth, and the "undetermined" conclusion stands. But the headline swaps one proxy for another. The new ratio, 0.1–0.3, uses *peripheral afferent* bandwidth in a different order of fish, while S18's ratio of 2–6 used a *whole-animal reflex* frequency. The quantity that matters is closed-loop postural bandwidth. The only measurement of it in zebrafish, S18-D's own P1 (larval, bout-sampled at about 0.5 Hz), still gives R ≈ 1.9–5.7. So the sensor-bandwidth argument falls, but "the bandwidth argument" does not; it moves to the loop, where it is unmeasured in adults.

## 1. Arithmetic, redone independently

I recomputed from the stated inputs: m = 0.4 g, L = 4 cm, I_y = mL²/12 = 5.33×10⁻⁸ kg m², S_t = 1 cm², l_t = 2 cm, a_t = 1.6 rad⁻¹, ρ = 1.2 kg m⁻³. These are S18's assumed design values, not measurements. Results are **computed**.

| V (m/s) | f_req (Hz) | R at f_avail = 0.5 Hz | R at 10 Hz | R at 20 Hz | doubling time if unstable (ms) |
|---|---|---|---|---|---|
| 1 | 0.955 | 1.91 | 0.095 | 0.048 | 115.5 |
| 2 | 1.910 | 3.82 | 0.191 | 0.095 | 57.8 |
| 3 | 2.865 | 5.73 | 0.286 | 0.143 | 38.5 |

At 2 m/s: ω = √(0.5ρV²·S_t·l_t·a_t / I_y) = √(7.68×10⁻⁶ / 5.33×10⁻⁸) = 12.0 rad s⁻¹, so f = 1.91 Hz. This matches S18-D.

Steinhausen upper corner f_u = 8ν/(2πr²) with ν = 10⁻⁶ m² s⁻¹ (assumed): r = 0.65 mm gives 3.0 Hz, 0.36 mm gives 9.8 Hz, 0.2 mm gives 31.8 Hz and 0.1 mm gives 127 Hz. This matches S18-D. The scaling direction is also right: smaller ducts raise the upper corner. **No arithmetic error found.**

## 2. Proxy: what stands in for what

- **S18's f_avail (0.5 Hz)** was a *behavioural reflex* test frequency, the larval VOR. S18-D correctly shows it was a protocol ceiling, not a measured cutoff. I agree. S18's own key_number already called it the "highest measured … test frequency", so S18 did not itself mislabel it as a bandwidth. The defect was in S18 §3.6's use of it as a sensor-speed limit.
- **S18-D's replacement (≥ 10 Hz)** is *peripheral canal afferent* bandwidth in toadfish (*Opsanus tau*, order Batrachoidiformes). This is the bandwidth of the first stage of the loop only. It is an **upper bound** on what the loop can deliver, not the loop's bandwidth.
- **The quantity that matters** is the closed-loop bandwidth of an attitude controller: sensor → central processing → fin/axial actuator → body, including delay and gain. Its value in adult *Danio rerio* is **unknown**. The only zebrafish postural-loop datum in play is S18-D's own P1 (Hamling et al., preprint, larval): corrections arrive in bouts at about 0.50 Hz. Using that as f_avail gives R = 1.9 / 3.8 / 5.7. That is the *same* ratio S18 had (computed above).

So the claim's sentence "makes the required/available ratio 0.1-0.3 instead of 2-6" compares a sensor ratio with a reflex ratio. My inference: the 2–6 has not been replaced. It has been shown to rest on a reflex number rather than a sensor number, and a separate larval loop number now reproduces it. S18-D's body text (§4) does list the larval bout loop as a remaining limit. So the error is in the headline and key_number ("replacing 0.5 Hz", "the bandwidth argument … falls"), not in the body's final answer ("undetermined").

Bout rate is not a hard ceiling either. Ehrlich & Schoppik 2017 (*Curr Biol* 27:334–344; read-level **search-summary**) report that larvae initiate swims preferentially when unstable, and swim more often when instability is increased. So 0.5 Hz is a *basal* rate, and a perturbed fish could sample faster. That is another reason the loop-level R is **unknown**, rather than known to be 2–6. It cuts against S18 as much as against S18-D.

## 3. Hidden assumptions, relaxed

1. **"Tested to 10 Hz" is read as "bandwidth ≥ 10 Hz."** In the abstract of Boyle & Highstein 1990 (PMC6570080; read-level **abstract**, re-fetched by me), the stimuli ran from 0.001 to 10 Hz. Low-gain afferents are linear in velocity "across most of the frequency and amplitude spectra tested". The abstract gives no corner frequencies and no gain at 2–10 Hz (confirmed on my fetch). "Most of" leaves room for a roll-off inside the tested band. S18-D faults S18 for treating a test range as a bandwidth. Here it does the mirror image: it treats the top of a test range as a lower bound on bandwidth, without the gain at that top frequency. **Relaxed:** the claim needs only that the sensor corner is above about 3 Hz (R < 1 at 3 m/s). Rabbitt et al. 2005 reported a hair-cell microphonic "relatively flat" over 0.1–20 Hz (S18-D's partial full-text read; I did not re-read it). High-gain afferents show *enhancement* at high frequency. A corner between 3 and 10 Hz cannot be excluded at abstract level. Then R_sensor would sit between 0.29 and 0.95 at 3 m/s: still below 1. **The sensor-level conclusion survives this relaxation, but "≥ 10 Hz" should read "probably > 3 Hz; ≥ 10 Hz not shown at the read-level held".**
2. **Cross-species transfer (toadfish → zebrafish).** Under the Steinhausen model, a smaller duct raises f_u, so mechanics favour the transfer (computed). The model is not validated for zebrafish, and the adult *Danio* duct radius is **unknown**: I did not find it, and I did not search for it beyond what S18-D tried. What small canals lose is sensitivity, which feeds directly into the low measured reflex gains (0.20–0.44). Those gains are measured in zebrafish, unlike the bandwidth.
3. **Any active control is needed at all.** If the airframe is passively stable (S18 answer (a)), R is irrelevant. That is outside this claim, and both S18 and S18-D handle it correctly.

## 4. Evidence level

`derived` is honest. S18-D labels the toadfish transfer as cross-species and as inference, and keeps search-summary items (Beck et al. 2004 gain 0.20) flagged. One wording defect: the key_number says "peripheral angular-rate sensor bandwidth >=10 Hz" without "toadfish-measured test range, no corner frequency reported". A reader could take ≥ 10 Hz as a measured bandwidth. It is a measured *test range* with a qualitative response report (abstract level). Minor, but it is the same kind of defect S18-D found in S18.

## 5. Counter-examples and missed taxa

- **Goldfish (a cyprinid, closer kin to zebrafish than toadfish).** Hartmann & Klinke 1980, "Discharge properties of afferent fibres of the goldfish semicircular canal with high frequency stimulation", *Pflügers Arch* 388:111–121. Read-level for the title and citation: **listing**. Its findings are **could-not-access**: `link.springer.com` and `scilit.com` do not resolve in this session's network settings and would need to be allowed there. From the title alone, a cyprinid canal-afferent high-frequency dataset exists, and S18-D missed it. I cannot say whether it supports or undercuts ≥ 10 Hz. I do not use any number from it.
- **No published counter-example** showing a low (< 2 Hz) canal-afferent corner in an adult teleost was found. Scope: 2 WebSearch (standard) calls and 3 WebFetch calls, 2 of which failed on DNS. This is a narrow negative.

## 6. What I could not break

- Section 1's arithmetic is correct.
- 0.5 Hz was never a measured bandwidth. S18-D's re-reading of S18's own sources V1, V4 and V5 is consistent with what S18-D quotes. I did not re-read V1–V5 myself.
- At sensor level, the claim survives even with a corner well below 10 Hz.
- The revised answer, "active control undetermined; passive stability as prudence", is a fair reading of the evidence.

## 7. Corrected statement

"The 0.5 Hz figure was a larval test-protocol ceiling, so the *sensor-bandwidth* argument against active control falls. Adult toadfish canal afferents respond over a 0.001–10 Hz test range, giving R_sensor ≤ 0.1–0.3 if the canal passes 10 Hz, and < 1 if the corner is anywhere above about 3 Hz (cross-species, abstract-level). The *loop-bandwidth* question is unresolved. The only zebrafish postural-loop measurement (larval, basal bout rate about 0.5 Hz, preprint) still gives R ≈ 1.9–5.7, and the adult loop rate and latency are unknown. So active control is undetermined, not disfavoured by a demonstrated bandwidth shortfall."

## Sources (read-level)

- S18-D, `docs/research/fish/S18-deepen.md` @ `origin/claude/deepen-s18-zebrafish-air-3u64z4`: full-text.
- Boyle & Highstein 1990, *J Neurosci* 10:1557, [PMC6570080](https://pmc.ncbi.nlm.nih.gov/articles/PMC6570080/): abstract (re-fetched by me).
- Hartmann & Klinke 1980, *Pflügers Arch* 388:111–121: listing (title and citation via search); content could-not-access (DNS-blocked hosts).
- Ehrlich & Schoppik 2017, *Curr Biol* 27:334–344 ([ZFIN record](https://www.zfin.org/ZDB-PUB-170124-11)): search-summary.
- Rabbitt et al. 2005 and Hamling et al. preprint: not re-read by me; I used them as S18-D reported them.

```swarm-challenge
{"claim_id": 284, "outcome": "weakened", "reason": "The 0.5 Hz figure was indeed a protocol ceiling and the sensor-bandwidth argument falls, but the headline ratio 0.1-0.3 swaps a whole-reflex proxy for a peripheral-afferent proxy from another order; the quantity that matters is closed-loop postural bandwidth, whose only zebrafish measurement (larval basal bout rate ~0.5 Hz) still gives R~1.9-5.7, so 'the bandwidth argument falls' overstates and should read 'the sensor-bandwidth argument falls; loop bandwidth is unmeasured in adults'.",
  "corrected_value": "R_sensor <= 0.1-0.3 (toadfish, if canal passes 10 Hz; <1 if corner >~3 Hz); R_loop unknown in adults, ~1.9-5.7 using larval basal bout rate 0.5 Hz",
  "depends_on": [
    "S18 reference geometry and glide speeds 1-3 m/s as stated in S18-D (assumed design values)",
    "Boyle & Highstein 1990 J Neurosci 10:1557 abstract: toadfish canal afferents tested 0.001-10 Hz, no corner frequencies reported",
    "Rabbitt et al. 2005 J Neurophysiol 93:424: microphonic relatively flat 0.1-20 Hz (as reported by S18-D, not re-read)",
    "Hamling et al. bioRxiv 2023.12.06.570482: larval basal bout rate ~0.5 Hz (as reported by S18-D, preprint)",
    "Ehrlich & Schoppik 2017 Curr Biol 27:334: bout initiation increases with instability (search-summary)",
    "Steinhausen canal model with endolymph nu ~1e-6 m^2/s (assumed)",
    "Adult Danio rerio closed-loop postural bandwidth and latency: unknown",
    "Hartmann & Klinke 1980 Pflugers Arch 388:111: existence only (listing); content unread"
  ]}
```
