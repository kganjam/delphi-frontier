# S18-D: Deepening "Could a zebrafish control attitude in air?"

Project: `zebrafish-flight`. Subproblem S18-D (deepens S18).
Date written: 2026-11-04.
Parent document: `docs/research/fish/S18-behaviour.md` on branch `origin/claude/zebrafish-aerial-attitude-k8hgr8`. It is not merged into this branch. I read it in full from that branch with `git show`.
Evidence level of this document: **derived**. It combines my arithmetic with literature, which I read at full text through a fetch tool's summary, at abstract level, or at search-summary level, as marked. Nothing here is a new observation.

---

## 0. What S18 concluded, and what it rested on

The task prompt left the recorded answer blank, so I took it from the parent file's `swarm-result`. S18's answer has two parts.

- **(a) Passive.** An engineered 0.4 g glider could hold attitude only if it is passively stable. That needs a rear stabiliser and a positive static margin. On S18's reference geometry, the computed pitch mode is about 1–3 Hz, and roll rate damps out in 1–4 ms.
- **(b) Active.** S18 does not support active vestibular attitude control. Its stated `key_number` was:

> "computed pitch short-period ~1.9 Hz at 2 m/s (reference design) versus highest measured zebrafish vestibular-reflex test frequency 0.5 Hz"

S18 §3.6 states the core argument for (b): the required 1–3 Hz band "lies above every measured zebrafish vestibular/gaze frequency I found, by a factor of about 2–10". S18 gave three supporting legs:

1. The utricle loses its gravity reference in free fall. This is physics.
2. The best measured reflex gain is low: roll-VOR 0.33 at about 0.25 Hz in larvae.
3. No small non-exocoetid teleost has been shown to correct attitude in air. This is a negative literature search.

## 1. The input the answer is most sensitive to

Answer (a) depends on geometry. S18 already says (a) holds only *if* the design adds a rear surface, so (a) is conditional by construction. Answer (b) is the substantive claim. It is a ratio of required to available frequency:

  R = f_req / f_avail.  "Too slow" means R > 1.

There are two candidate inputs.

- **f_req**: the airframe's pitch frequency, f_n ∝ V·√(S_t l_t / I_y), on S18's made-up reference design.
- **f_avail**: the bandwidth of the fish's attitude sensing. S18 put 0.5 Hz here.

**Sensitivity, recomputed** (my computation; script in §6; same constants and geometry as S18):

Halving or doubling the geometry term (S_t·l_t/I_y) at V = 2 m/s gives f_req = **1.35 / 1.91 / 2.70 Hz**. A factor of 2 in geometry moves f_req by only √2. With f_avail = 0.5 Hz, R stays between 2.7 and 5.4. **Conclusion (b) does not care about a factor of 2 in geometry.**

f_avail is a different story. R at each glide speed V:

| f_avail (Hz) | R at V = 1 m/s (f_req 0.95 Hz) | R at V = 2 (1.91 Hz) | R at V = 3 (2.86 Hz) |
|---|---|---|---|
| 0.25 | 3.8 | 7.6 | 11.5 |
| **0.5 (S18)** | 1.9 | 3.8 | 5.7 |
| 1 | 0.95 | 1.9 | 2.9 |
| 2 | 0.48 | 0.95 | 1.4 |
| 4 | 0.24 | 0.48 | 0.72 |
| 10 | 0.10 | 0.19 | 0.29 |

R is linear in f_avail. Doubling it once (0.5 → 1 Hz) flips the low-speed case. Doubling it twice (→ 2 Hz) flips the design case at 2 m/s. **f_avail is the input the conclusion is most sensitive to.** The "factor of about 2–10" in S18 is just this ratio, so an error in f_avail passes straight into the conclusion.

## 2. How well established was f_avail = 0.5 Hz?

**It was not a bandwidth measurement. It was the highest stimulus frequency anyone had used.** I re-read S18's own sources:

- V1 (Mo et al. 2010) used one frequency only, 0.25 Hz. S18 records: "No gain-vs-frequency curve exists in this paper."
- V4 (Sun et al. 2018) used one stimulus, ≈ 0.5 Hz.
- V5 (Burkhardt et al. 2026) tested 0.0625–0.25 Hz. S18 records: "No formal cutoff frequency or bandwidth is reported." The "no response above 0.5 Hz" in V5 is for vertical *OKR*, which is a visual reflex, not a vestibular one.
- Every one of these is larval or early juvenile, at an age when S18's own source V6 says the canals are too small to work.

So the number is a **proxy, twice over**:

1. It is a protocol ceiling standing in for a bandwidth. A reflex tested only at ≤ 0.5 Hz tells you nothing about its response at 2 Hz.
2. It is a larval gaze reflex driven by the utricle, standing in for an adult attitude sensor driven by the canals. In flight it is the angular-rate sensor that matters, and S18 leg 1 itself argues the utricle is useless there.

Honest grade for f_avail = 0.5 Hz as a *bandwidth*: **assumption that reads as measured.** The measurements behind it are real (V1, V4, V5 at full text through fetch summaries). Their use as an upper frequency limit is not supported by any of them.

## 3. Improving it: the real quantity

The real quantity is **the frequency response, gain and phase versus Hz, of adult *Danio rerio* semicircular-canal afferents, or of a canal-driven reflex, over 0.5–5 Hz.** Below is what I could find. All searches were run on 2026-11-04 with the session's WebSearch and WebFetch.

### 3.1 Adult or large zebrafish canal reflex

| # | Finding | Source | Read-level |
|---|---|---|---|
| D1 | "Best AVOR measured in cyprinids was a large zebrafish (gain = 0.20)", at **0.5 Hz, ±60° s⁻¹**. Adult goldfish AVOR gain averaged about 0.9 at 0.125 Hz, ±16° s⁻¹. The paper's abstract-level summary says VOR gain increased in proportion to size. | Beck, Gilland, Tank, Baker, *J Neurophysiol* 92:3546–3561 (2004), doi:10.1152/jn.00311.2004 | **search-summary.** The full text is **could-not-access**: `journals.physiology.org` does not resolve in this session (`getaddrinfo ENOTFOUND`). It has to be allowed in the session's network settings. The quoted numbers came only from a search engine's summary of the page. I could not confirm them, the fish's size or age, or whether any frequency above 0.5 Hz was tested. |

This **corrects S18 V9**, which said that a canal-driven VOR in adult or large zebrafish was "not found". A datum exists at search-summary level. It is still at 0.5 Hz, so it does not give a bandwidth either. If it is correct, it shows a *low* gain (0.20) in the largest zebrafish tested, against about 0.9 in adult goldfish.

**Adult *D. rerio* canal-afferent or canal-reflex gain and phase above 0.5 Hz: unknown.** Searches tried: "adult zebrafish semicircular canal vestibulo-ocular reflex rotation frequency gain" (extended), and "Beck Gilland Tank Baker 2004 'large zebrafish' angular VOR gain 0.20 0.5 Hz" (extended). Both searches returned larval work, and the 2004 paper, which I could not open.

### 3.2 Adult fish canal frequency response (another species: the best available real quantity)

| # | Finding | Source | Read-level |
|---|---|---|---|
| T1 | 66 horizontal-canal afferents tested with sinusoids from **0.001–10 Hz** at 5–100° s⁻¹. "Low-gain" afferents respond with "a relatively linear response re: stimulus velocity across most of the frequency and amplitude spectra tested". "High-gain" afferents show "high-frequency gain enhancement and phase advance". "Acceleration" afferents are more in phase with acceleration across the tested band. **The abstract gives no corner frequencies.** | Boyle & Highstein, *J Neurosci* 10(5):1557–1569 (1990), toadfish *Opsanus tau* (PMC6570080) | abstract (fetch-tool summary of the PMC page) |
| T2 | Sinusoidal stimuli of **0.1–20 Hz**. The microphonic was "relatively flat across the frequency range". The paper refers to frequencies "above the lower corner (>0.1 Hz)". | Rabbitt, Boyle, Holstein, Highstein, *J Neurophysiol* 93(1):424–436 (2004/2005), toadfish (PMC3000937) | full-text, first 100k of about 131k characters, via fetch-tool summary |
| T3 | Mechanical stimuli at < 5 Hz give "afferent responses [that] closely correspond to those using actual head rotations". 2 Hz and 4 Hz were used. | Boyle, Rabbitt, Highstein, *J Neurophysiol* 102(3):1513–1525 (2009), toadfish (PMC2746798) | full-text, first 100k of about 111k characters, via fetch-tool summary |
| — | Two figures from a search summary, a cupula adaptation time constant of about 36 s (lower corner about 0.0044 Hz) and a microphonic resonance near 30 Hz, were **not found** in the T2 or T3 text I could read. **I do not use them.** | — | search-summary only; unconfirmed |

**The authors' claim:** adult toadfish canal afferents and hair cells respond across 0.1–10 or 20 Hz, and one afferent class responds *more* strongly at high frequency.
**My inference:** in at least one adult teleost, the peripheral angular-rate sensor passes the 1–3 Hz band that S18's airframe needs. So the peripheral sensor's f_avail in an adult fish is **≥ 10 Hz**, not 0.5 Hz. This is a cross-species transfer. Toadfish are large benthic batrachoidiforms, not cyprinids, and their canal size is unknown to me (I did not retrieve it).

### 3.3 Does the transfer to a small fish hold? (computation, labelled)

In the textbook Steinhausen torsion-pendulum model, the canal's upper corner is set by the short time constant τ_s ≈ r²/(8ν). Here r is the duct radius and ν the endolymph kinematic viscosity, which I **assume** is ≈ water, 1 × 10⁻⁶ m² s⁻¹. The upper corner f_u = 1/(2π τ_s) falls to 3 Hz only if r ≈ **0.65 mm**, and to 10 Hz if r ≈ 0.36 mm. Smaller ducts push f_u *higher* (computed, §6).

The adult zebrafish duct radius is **unknown**; I did not find it. **My inference** is that a duct of 1.3 mm diameter in a 4 cm fish is implausible, so mechanics will not cap a functional adult zebrafish canal below 3 Hz. Small canals are limited in *sensitivity*, through gain and the low-frequency corner, not in high-frequency bandwidth. That fits S18 V6, where larval canals are "too small to transduce" at all. The model is a simplification and has not been validated for zebrafish.

### 3.4 The measured zebrafish *postural* loop (not gaze)

Gaze reflexes are not postural reflexes, as S18 itself warned. I looked for a measured postural-loop rate.

| # | Finding | Source | Read-level |
|---|---|---|---|
| P1 | Larvae aged 4–9 dpf correct pitch **in discrete bouts**: they "rotate their bodies during bouts to restore posture", and posture destabilises passively between bouts. Basal bout rate is **0.50–0.51 Hz** in controls (4 and 7 dpf). Median bout duration is 0.13–0.15 s, the refractory period 0.25 s, and the pitch-correction gain 0.29 (4 dpf) and 0.44 (7 dpf). **The paper reports no tilt-correction latency in ms.** | Hamling, Harmon, Kimura, Higashijima, Schoppik, "The vestibulospinal nucleus is a locus of balance development", bioRxiv 2023.12.06.570482 v2 (2024) (PMC10723429) | full-text, first 100k of about 136k characters, via fetch-tool summary. This is a preprint. |
| P2 | Synaptic latencies onto vestibulospinal neurons of about 2.3 ms for a slow component (4–7 dpf, translational sled). | bioRxiv 2021.07.05.451142, "Synaptic Encoding of Vestibular Sensation Regulates Movement Timing and Coordination" | search-summary. This is a synaptic latency, not the latency of a behavioural reflex. |

**Computation on P1** (§6). Take a 2 s inter-bout interval at 0.5 Hz. An *unstable* airframe grows by e^(λT) over one interval: 1.6 × 10⁵ at 1 m/s, 2.6 × 10¹⁰ at 2 m/s and 4.3 × 10¹⁵ at 3 m/s. A *stable* but lightly damped mode cannot be damped either, because 0.5 Hz sampling is below the Nyquist rate (2 × f_req) at every speed. **If the larval bout-sampled postural controller were the adult controller, answer (b) would be a firm negative.** It probably is not. Adults swim continuously rather than in bouts. That is my inference; I did not source an adult postural-loop measurement. **Adult zebrafish postural-reflex latency and loop rate: unknown.** Search tried: "zebrafish vestibulospinal latency postural reflex milliseconds tilt" (standard).

### 3.5 What would settle it, and what it costs

**Measurement:** canal-afferent or vestibulospinal recordings, or the angular VOR measured with a head-fixed rotating stage, in adult *D. rerio* (≥ 90 dpf, about 3–4 cm). Sinusoids at 0.25–10 Hz, ±20–100° s⁻¹, in pitch and roll. Report gain and phase per frequency, and the latency from stimulus to fin or axial EMG.

**Cost:** this is my estimate, not a sourced figure. The behavioural AVOR version uses existing larval eye-tracking rotary rigs with a larger fish holder. It is roughly one person-month in a lab that already runs larval VOR. Afferent recording in adults is a harder surgical preparation, roughly several person-months. Exact costs are unknown.

**Decision thresholds** (S18 §6 plus §6 below): gain ≳ 0.5 with phase lag ≲ 45° at 2–3 Hz, and sensor-to-fin latency ≲ 40 ms (2 m/s) or ≲ 28 ms (3 m/s), would make active stabilisation plausible.

## 4. Recomputing the conclusion

With f_avail(peripheral) ≥ 10 Hz (toadfish, T1/T2, cross-species), R = **0.10 / 0.19 / 0.29** at 1 / 2 / 3 m s⁻¹, against 1.9–5.7 in S18 (my computation). So S18's central quantitative claim, that the required band is "above every measured … frequency by a factor of about 2–10, so the sensor is too slow", **falls**. The sensor bandwidth was never measured to be low. The best real quantity available, from an adult teleost, says it is high.

**What survives, and on what footing:**

- **S18 leg 1 (utricle in free fall) stands.** It is physics, and it is untouched by this work. It argues for canals plus vision, and canals are exactly what §3.2–3.3 say may have enough bandwidth.
- **Reflex gain is low wherever it has been measured.** Larval roll-VOR is 0.33 (S18 V5). Large-zebrafish AVOR is 0.20 at 0.5 Hz (D1, search-summary only). Larval pitch-correction gain is 0.29–0.44 (P1). This is now the strongest *measured* reason for caution. It concerns gain, not bandwidth.
- **The larval postural loop is bout-sampled at about 0.5 Hz (P1).** If that applied to adults, it would rule out active control by a margin of 10⁵–10¹⁵ (computed). Its transfer to adults is unestablished.
- **Loop latency in adults is unknown.** The binding constraint for an unstable design is now the latency (≲ 42 ms at 2 m/s, computed), not sensor bandwidth.
- **Answer (a), passive stability, is unchanged.** Its geometric sensitivity is only √2 per factor of 2.

**Revised answer (b):** whether a zebrafish could actively control attitude in air is **undetermined, not disfavoured on bandwidth grounds**. The angular-rate sensor in an adult teleost is fast enough (toadfish, cross-species). What is unknown, or measured only as unfavourable, is reflex *gain* (low wherever measured), postural *loop rate* (bout-sampled at 0.5 Hz in larvae) and *latency* (unknown in adults). The engineering recommendation "design for passive stability" still stands as prudence. It no longer stands on the claim that the sensor is too slow.

**Verdict on S18's conclusion as stated (with its key number): FALLS.** S18's "the evidence leans against relying on it" was argued from a 2–10× bandwidth shortfall that does not exist in the best available real quantity. The recommendation survives on different, weaker grounds.

## 5. What this does NOT establish

- It does **not** measure the adult zebrafish canal. The ≥ 10 Hz figure is toadfish, from an abstract (T1) and two fetch-summarised full texts (T2, T3).
- It does **not** show that a zebrafish *can* fly an airframe actively. It removes one argument against that.
- D1 (gain 0.20 at 0.5 Hz in a large zebrafish) is search-summary only, and could be misquoted.
- The canal-scaling computation (§3.3) assumes endolymph ν ≈ water and the classic Steinhausen model, with no adult zebrafish duct radius.
- P1 is a preprint and larval. P2 is a synaptic latency, not a reflex latency.
- The negative searches are narrow: 6 WebSearch calls (3 standard, 3 extended) and 5 WebFetch calls, one of which failed on DNS. I did not search for goldfish canal-afferent dynamics successfully (one standard search returned other species), for adult cyprinid canal dimensions, or for adult zebrafish fin-reflex latency beyond one search.
- Disagreement preserved: S18 V2 versus V3 on canal-VOR onset (about 35 dpf versus 3 dpf) is not resolved here. D1, if correct, supports a late, low-gain canal VOR in zebrafish, which sits closer to V2.

## 6. Reproduction (computation)

```python
import math
rho=1.2; m,L=0.4e-3,0.04; Iy=m*L**2/12
St,lt,at=1e-4,0.02,1.6
def fn(V,k=1.0):  # k scales St*lt/Iy
    q=0.5*rho*V**2; Ma=q*St*lt*at*k; w=math.sqrt(Ma/Iy); return w/(2*math.pi), w
for V in (1,2,3):                       # f_req, doubling time, delay bound 0.5/lambda
    f,w=fn(V); print(V, round(f,2), round(1000*math.log(2)/w), round(1000*0.5/w))
for fa in (0.25,0.5,1,2,4,10):          # ratio R = f_req/f_avail
    print(fa, [round(fn(V)[0]/fa,2) for V in (1,2,3)])
print([round(fn(2,k)[0],2) for k in (0.5,1,2)])   # geometry x0.5, x1, x2 at 2 m/s
nu=1e-6                                  # ASSUMED endolymph viscosity ~ water
for fu in (3,10): print(fu, 1e3*math.sqrt(8*nu/(2*math.pi*fu)), "mm")
for V in (1,2,3):                        # larval bout-sampled loop, 0.5 Hz
    f,w=fn(V); print(V, "%.1e"%math.exp(w*2.0), 0.5>2*f)
```

Output (my run, 2026-11-04): f_req = 0.95 / 1.91 / 2.86 Hz. Doubling times are 116 / 58 / 39 ms, and the delay bounds 83 / 42 / 28 ms. Geometry ×0.5/×1/×2 at 2 m/s gives 1.35 / 1.91 / 2.70 Hz. The duct radius for f_u = 3 Hz is 0.65 mm, and for 10 Hz 0.36 mm. Growth per 2 s interval is 1.6e5 / 2.6e10 / 4.3e15, and the Nyquist check fails at every speed.

## Sources (read-level)

- Beck, Gilland, Tank, Baker 2004, *J Neurophysiol* 92:3546, doi:10.1152/jn.00311.2004: **search-summary**; full text could-not-access (DNS-blocked host).
- Boyle & Highstein 1990, *J Neurosci* 10:1557, PMC6570080: **abstract**.
- Rabbitt, Boyle, Holstein, Highstein 2004/5, *J Neurophysiol* 93:424, PMC3000937: **full-text** (partial, via fetch summary).
- Boyle, Rabbitt, Highstein 2009, *J Neurophysiol* 102:1513, PMC2746798: **full-text** (partial, via fetch summary).
- Hamling, Harmon, Kimura, Higashijima, Schoppik, bioRxiv 2023.12.06.570482, PMC10723429: **full-text** (partial, via fetch summary; preprint).
- bioRxiv 2021.07.05.451142 (vestibulospinal synaptic encoding; authors not retrieved): **search-summary**.
- S18 parent sources V1–V9 as graded in `S18-behaviour.md`; I did not re-read them, apart from re-reading S18's own descriptions of their stimulus ranges.

```swarm-result
{"subproblem": "S18-D", "evidence": "derived",
  "answer": "S18's 0.5 Hz 'vestibular frequency' was a larval test-protocol ceiling, not a bandwidth; adult teleost (toadfish) canal afferents respond across 0.1-10/20 Hz, which makes the required/available ratio 0.1-0.3 instead of 2-6, so the bandwidth argument against active attitude control falls. Active control becomes undetermined, now limited by low measured reflex gain (0.20-0.44), the larval bout-sampled ~0.5 Hz postural loop and unknown adult latency, while 'design for passive stability' survives only as prudence.",
  "key_number": "peripheral angular-rate sensor bandwidth >=10 Hz (toadfish Opsanus tau canal afferents, tested 0.001-10 Hz; hair cells 0.1-20 Hz; cross-species) replacing 0.5 Hz (highest larval zebrafish test frequency)",
  "verdict": "falls",
  "depends_on": [
    "S18 conclusion (b) and key_number: pitch mode ~1.9 Hz at 2 m/s vs 0.5 Hz",
    "S18 reference geometry: m=0.4 g, L=4 cm, I_y=mL^2/12, S_t=1 cm^2, l_t=2 cm, a_t=1.6/rad (assumed)",
    "Glide speeds 1-3 m/s (assumed; anchored to guppy max air speed 1.24 m/s, Soares & Bierman 2013)",
    "Boyle & Highstein 1990 J Neurosci 10:1557: toadfish canal afferents 0.001-10 Hz, velocity-linear / high-frequency enhancement (abstract)",
    "Rabbitt et al. 2004 J Neurophysiol 93:424: toadfish hair-cell microphonic relatively flat over 0.1-20 Hz (partial full text)",
    "Boyle, Rabbitt, Highstein 2009 J Neurophysiol 102:1513: afferent responses to <5 Hz mechanical stimuli match head rotation (partial full text)",
    "Claim: toadfish canal bandwidth transfers to adult Danio rerio (cross-species inference, unverified)",
    "Steinhausen canal model, upper corner f_u=8nu/(2 pi r^2), endolymph nu ~1e-6 m^2/s (assumed); adult Danio duct radius unknown",
    "Beck et al. 2004 J Neurophysiol 92:3546: large-zebrafish AVOR gain 0.20 at 0.5 Hz, goldfish ~0.9 at 0.125 Hz (search-summary only)",
    "Burkhardt et al. 2026 JEB jeb251770: larval roll-VOR gain 0.33, tested <=0.25 Hz (via S18 V5)",
    "Mo et al. 2010 and Sun et al. 2018: larval single-frequency VOR at 0.25 and ~0.5 Hz (via S18 V1, V4)",
    "Hamling et al. bioRxiv 2023.12.06.570482: larval postural correction is bout-based, bout rate ~0.5 Hz, pitch-correction gain 0.29-0.44 (preprint, partial full text)",
    "Claim: adult zebrafish postural control is continuous rather than bout-sampled (my inference, unsourced)",
    "Physics: otolith senses specific force, ~0 in ballistic flight (S18 leg 1)",
    "Control rule of thumb: delay tau_d <= 0.5/lambda; sampling rate > 2 f_mode (Nyquist)",
    "Adult Danio sensorimotor latency: unknown",
    "S18 negative literature search: no small non-exocoetid teleost shown correcting attitude in air (13 searches, mostly abstract level)"
  ]}
```
