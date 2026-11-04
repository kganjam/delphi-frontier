# S18-D-D: Deepening S18-D by attacking its weakest input (loop delay)

Project: `zebrafish-flight`. Subproblem S18-D-D (deepens S18-D, which deepened S18).
Date written: 2026-11-04.
Evidence level of this document: **derived**. It is my arithmetic (a delay-stability computation) applied to latency values from the literature. I read those values at **search-summary** level only, because the primary pages were blocked by this session's network policy (§3.4). Nothing here is a new observation.

Parent documents. Neither is merged into this branch. I read both in full with `git show`:

- `docs/research/fish/S18-behaviour.md` on `origin/claude/zebrafish-aerial-attitude-k8hgr8` (S18)
- `docs/research/fish/S18-deepen.md` on `origin/claude/deepen-s18-zebrafish-air-3u64z4` (S18-D)

The task prompt left "the recorded answer" blank, so I took S18-D's answer from its `swarm-result`.

---

## 0. What S18-D concluded

S18 argued that a 0.4 g, 4 cm zebrafish glider could not be flown actively. Its reason was a sensor-bandwidth gap: the computed pitch mode is about 1.9 Hz at 2 m/s, and the highest test frequency of any measured zebrafish vestibular reflex is 0.5 Hz.

S18-D showed that 0.5 Hz was a ceiling of the larval test protocol, not a bandwidth. It cited canal afferents in an adult teleost (toadfish) that respond across 0.1–10/20 Hz. On that basis S18-D concluded:

- The bandwidth argument **falls**.
- Active attitude control is **undetermined**. It is limited by low measured reflex gain, by the larval bout-sampled postural loop (about 0.5 Hz), and by unknown adult latency.
- In S18-D's words: "The binding constraint for an unstable design is now the **latency (≲ 42 ms at 2 m/s, computed)**, not sensor bandwidth." The adult value was "unknown".
- "Design for passive stability" survives only as prudence.

## 1. The input S18-D is most sensitive to

I recomputed S18-D's ratio with each candidate input halved or doubled. Script: §6. Geometry and constants are S18's: m = 0.4 g, L = 4 cm, I_y = mL²/12, S_t = 1 cm², l_t = 2 cm, a_t = 1.6 rad⁻¹, ρ = 1.2 kg m⁻³. All of these are **assumed**, not measured.

| Candidate input | Value in S18-D | Recomputed at ×½ / ×2 | Does the conclusion change? |
|---|---|---|---|
| Peripheral canal bandwidth f_avail | ≥ 10 Hz (toadfish) | At 5 Hz, R = f_req/f_avail = 0.19 / 0.38 / 0.57 at V = 1/2/3 m/s. Still < 1. It flips only below 2.86 Hz, a factor of 3.5. | **No** |
| Airframe geometry S_t·l_t/I_y | reference design | f_req at 2 m/s = 1.35 / 2.70 Hz. Still ≪ 10 Hz. | **No** (moves only √2 per factor of 2) |
| **Sensorimotor loop delay τ_d** | "unknown", threshold "≲ 42 ms at 2 m/s" | See below | **Yes** |

**Why τ_d is the most sensitive input.** Take the unstable-design pitch mode from S18: λ = ω_n = 6.0·V s⁻¹ (V in m/s). Stability is set by the dimensionless product λ·τ_d (§4). Take τ_d = 70 ms, the measured teleost roll-response latency in §3.2. At 2 m/s that gives λτ = 0.84: stabilisable, but the gain must be tuned to within a factor of 1.34. Halve τ_d to 35 ms and λτ = 0.42, which gives a robust gain range of more than 2.7×. Double it to 140 ms and λτ = 1.68, which is **not stabilisable by any delayed proportional-derivative (PD) controller** (computed, §4). A single factor of 2 in τ_d therefore moves the 2 m/s design between "robust", "knife-edge" and "impossible". No other input does that.

**A second, coupled problem I found while recomputing.** S18-D's threshold "≲ 42 ms" is S18's rule of thumb τ_d ≲ 0.5/λ. It is not a stability limit. The exact limit for this plant is √2/λ (§4). At 2 m/s that is **118 ms**, nearly 3× looser. So both sides of the comparison, the fish's delay and the airframe's admissible delay, were weak. I improve both.

## 2. How well established was τ_d?

**It was not established at all.** S18 §2.4 says: "Mauthner-cell or vestibulospinal loop latency: not searched in this session, so **unknown here**." S18-D found one synaptic latency of about 2.3 ms onto larval vestibulospinal neurons (bioRxiv 2021.07.05.451142, search-summary). It correctly labelled that as a synaptic latency, not a behavioural one, and left τ_d **unknown**.

The *threshold* τ_d is compared against, 42 ms at 2 m/s, was presented with "(computed)". It is a computation, but of a heuristic: a 0.5 rad phase allowance at ω = λ. It reads as a stability boundary and is not one. **Grade: assumption that reads as computed.**

## 3. Improving τ_d: what is measured

Searches were run on 2026-11-04 with the session's WebSearch (9 calls: 6 standard, 3 extended) and WebFetch (5 calls). Three of the five fetches failed on DNS: `pubmed.ncbi.nlm.nih.gov`, `read.qxmd.com` and `cob.silverchair.com` are outside this session's allowed network domains. `journals.physiology.org` was already known to be blocked (S18-D). As a result, **every latency below is search-summary read-level**. I could not open a primary page for any of them.

### 3.1 Fastest vestibular arc in a teleost (eye, not body)

| # | Value | Source | Read-level |
|---|---|---|---|
| L1 | Goldfish VOR latency to a horizontal head-velocity step (16° s⁻¹ zero-to-peak): **18 ms (adducting eye), 20 ms (abducting eye)**, "independent of the initial VOR gain". | Pastor, de la Cruz, Baker, "Characterization and adaptive modification of the goldfish vestibuloocular reflex by sinusoidal and velocity step vestibular stimulation", *J Neurophysiol* 68(6):2003–2015 (1992). | **search-summary** of the abstract. **Attribution disagreement, preserved:** one search summary attributed these numbers to the same group's 1994 paper (*J Neurophysiol* 72(3):1383–1394, "Cerebellar role in adaptation of the goldfish vestibuloocular reflex"). A second summary attributed them to the 1992 paper, and a third search for the 1994 paper "did not surface any mention of an 18 ms latency". I believe the 1992 paper is the source, but I could not open either one. |
| L2 | Goldfish Purkinje-cell discharge latency to a vestibular velocity step: **43 ms** (70 ms to a visual step). | Same 1992 abstract, per search summary. | **search-summary** |

**Author's claim versus my inference.** The authors report an 18–20 ms *ocular* latency. **My inference** is that this is a lower bound on any vestibular-to-fin loop. The VOR is the shortest vestibular arc, about three neurons, and it drives a low-inertia eye. A postural loop adds vestibulospinal conduction, a motor pool, muscle activation and the build-up of fin force. I have no measurement of how much those add in a fish.

### 3.2 Whole-body postural response latency in teleosts (the closest real quantity)

| # | Value | Source | Read-level |
|---|---|---|---|
| L3 | Postural disturbances in **creek chub** (*Semotilus atromaculatus*, a cyprinid), **smallmouth bass** and **bluegill**, applied either by removing a flow refuge or by striking the body with a narrow water jet. **Rolling disturbances: overall latency 70 ± 15 ms**, which "did not differ among species" and was significantly smaller than for other disturbances. **Other disturbances: 123 ± 19 ms (chub), 201 ± 24 ms (bass), 208 ± 52 ms (bluegill).** | Webb, "Response latencies to postural disturbances in three species of teleostean fishes", *J Exp Biol* 207(6):955–961 (2004), doi:10.1242/jeb.00854 | **search-summary** of the abstract and PubMed record. Full text **could-not-access** (cob.silverchair.com DNS-blocked). Body sizes, video frame rate, how latency was defined and n: **unknown**, because I could not read them. |
| — | Liao 2007 (*Phil Trans R Soc B* 362:1973) cites Webb 2004 only qualitatively: "rolling perturbations induced by jets of water were more quickly corrected". No ms values in the first 100k of 181k characters. | PMC2442850 | full-text (partial), via fetch-tool summary |

**Disagreement, preserved.** The roll latency (70 ms) and the non-roll latencies (123–208 ms) differ by 2–3×. I do not know which axis the non-roll jet strikes excited, and pitch is the axis that matters for S18. So I carry **both** values forward rather than pick one. The cyprinid value, 123 ± 19 ms in creek chub, is phylogenetically the closest to *Danio*.

### 3.3 Other latencies found (not used as τ_d)

- **Mauthner-mediated escape.** About 5–10 ms from stimulus to Mauthner discharge. In free-swimming goldfish the field potential precedes movement by about 8 ms (8.13 ± 0.17 ms, per search summary, source not resolved). Larval zebrafish short-latency escape has a minimum onset of 3 ms after 75 hpf (2012 study, search-summary). **Not used:** the C-start is an all-or-none ballistic escape, not a graded corrective reflex. Using it as τ_d would manufacture feasibility.
- **Larval zebrafish roll-correction body bend** (Sugioka, Tanimoto, Higashijima, *Nat Commun* 14:1217, 2023, PMC10006170; full-text first 100k of 139k characters via fetch summary). The 6 dpf larvae were tilted at 15° s⁻¹. Head roll peaks at about 1.7 s. **The paper reports no reflex onset latency**, and its calcium imaging ran at 10 fps, too coarse to resolve one.

### 3.4 Negative-search scope

**Adult *Danio rerio* vestibulospinal, fin or axial EMG latency to tilt or rotation: not found.** Searches: "fish vestibulospinal reflex latency fin or axial muscle EMG response to tilt or rotation ms" (extended); "zebrafish larvae tilt evoked escape or vestibular startle latency ms Mauthner" (standard); "fish pectoral fin reflex latency perturbation ms…" (standard). None returned a fish fin or axial EMG latency to vestibular stimulation in any species. **Pitch-specific** postural latency in any fish: not found (not searched separately).

### 3.5 What would settle it, and what it costs

**Measurement:** adult *D. rerio* (≥ 90 dpf, 3–4 cm) on a servo tilt table, with impulsive **pitch** and roll perturbations of 100–500° s⁻¹. Record (i) axial and pectoral EMG onset and (ii) the onset of corrective body or fin motion on 1000 fps video. Report τ_d as the time from stimulus onset to corrective torque onset, which is what the control model needs (§4), not just EMG onset.

**Cost:** my estimate, not a sourced figure. The behavioural version (video only) is about 2–4 person-weeks plus a high-speed camera and tilt stage, which many fish labs already have. The EMG version in a 0.4 g fish is harder, roughly 1–3 person-months.

**Decision thresholds (computed, §4, reference geometry):**

| Measured adult τ_d | What it means for an unstable airframe |
|---|---|
| ≤ 51 ms | robustly stabilisable at 2 m/s |
| 51–118 ms | stabilisable at 2 m/s only with a precisely tuned gain |
| > 118 ms | **not stabilisable** at 2 m/s by any delayed PD controller |

## 4. The improved threshold (computation, not observation)

The model is S18's unstable pitch mode with S18's (ignored) aerodynamic damping. The fish applies a delayed proportional-derivative correction:

  θ̈ = λ²θ − k_p θ(t − τ) − k_d θ̇(t − τ)

I solved it by D-subdivision, my derivation (script §6). The stability boundaries are k_p = λ² (a real root at s = 0) and the curve k_p = (λ² + ω²) cos ωτ, k_d = (λ² + ω²) sin(ωτ)/ω. A stable pocket exists only if that curve rises above k_p = λ² at small ω. Expanding gives (λ² + ω²)(1 − ω²τ²/2) ≈ λ² + ω²(1 − λ²τ²/2), so:

  **τ_crit = √2 / λ** (hard limit: no PD gains stabilise beyond it).

I also computed robustness as the widest ratio k_p,max / k_p,min available inside the stable pocket:

| λτ | 0.30 | 0.50 | 0.61 | 0.84 | 1.00 | 1.26 | 1.41 |
|---|---|---|---|---|---|---|---|
| Max gain ratio | 6.6 | 2.7 | **2.0** | 1.34 | 1.14 | 1.02 | 1.00 |

A gain ratio of 2 (6 dB) is a conventional minimum robustness margin. It requires λτ ≤ 0.61. That is close to S18's heuristic of 0.5. **So S18's "≲ 42 ms" was approximately a robustness bound, not a feasibility bound.** S18-D treated it as the binding feasibility constraint.

**Thresholds by glide speed (computed):**

| V (m/s) | λ (s⁻¹) | S18 heuristic 0.5/λ | Robust (gain ratio 2) 0.61/λ | Hard limit √2/λ |
|---|---|---|---|---|
| 1 | 6.0 | 83 ms | 101 ms | 236 ms |
| 2 | 12.0 | 42 ms | 51 ms | **118 ms** |
| 3 | 18.0 | 28 ms | 34 ms | 79 ms |

**λτ for each latency (computed):**

| τ_d | V = 1 m/s | V = 2 m/s | V = 3 m/s |
|---|---|---|---|
| 18 ms (L1, goldfish VOR) | 0.11 | 0.22 | 0.32 |
| **70 ms (L3, teleost roll)** | 0.42 | **0.84** | **1.26** |
| **123 ms (L3, chub, non-roll)** | 0.74 | **1.48 (unstabilisable)** | 2.21 (unstabilisable) |
| 208 ms (L3, bluegill, non-roll) | 1.25 | 2.50 (unstabilisable) | 3.74 (unstabilisable) |

**Highest glide speed at which an unstable design is still stabilisable** (computed, since λ ∝ V): V_max,hard = √2/(6.0·τ), V_max,robust = 0.61/(6.0·τ).

| τ_d | V_max,hard | V_max,robust |
|---|---|---|
| 18 ms | 13 m/s | 5.6 m/s |
| 70 ms | 3.4 m/s | 1.45 m/s |
| 123 ms | 1.9 m/s | 0.83 m/s |

S18 §3.2 computed that a glide needs about 14–20 cm² of wing at 2 m/s and 35–53 cm² at 1.24 m/s.

**What this model leaves out.** It ignores aerodynamic pitch damping, which would help. It ignores heave–pitch coupling, actuator bandwidth and sensor noise, which would all hurt. It also assumes S18's convention that the unstable root equals the stable design's ω_n (|static margin| unchanged). A designer can make λ smaller by making the margin only slightly negative.

## 5. Recomputing S18-D's conclusion

**Old:** τ_d unknown, admissible τ_d ≲ 42 ms at 2 m/s, so latency is "the binding constraint".

**New (derived):**

- **The admissible delay at 2 m/s is 118 ms (hard limit) or 51 ms (robust), not 42 ms** (computed).
- **The proxy delay is 70 ± 15 ms if the fish behaves like teleosts responding to roll, and 123–208 ms for other disturbances** (L3, search-summary, larger fish of unknown size, in water). The lower bound is 18–20 ms (L1, an eye reflex).
- With the roll proxy, an *unstable* zebrafish airframe is stabilisable in principle up to about 3.4 m/s, but **robustly only up to about 1.45 m/s**. At 2 m/s it would need its gain tuned within a factor of 1.34, and at 3 m/s within 1.6%.
- With the cyprinid non-roll proxy (123 ms), it is **unstabilisable at 2 m/s** and robust only below about 0.8 m/s, a speed at which S18 computes a glide needs more than 80 cm² of wing.
- The two measured teleost latencies **straddle the 2 m/s hard limit**. So the conclusion's sensitivity to τ_d is no longer hypothetical. It is visible in the disagreement between two measured values.

**Verdict on S18-D: STANDS.** "Active attitude control is undetermined" survives. It now has sharper edges:

- **Upgraded:** latency is no longer "unknown". Teleost proxies exist (search-summary), and they place the answer *on* the feasibility boundary at the design speed rather than clearly on either side.
- **Corrected:** S18-D's specific number "binding constraint ≲ 42 ms" was a robustness heuristic. The hard limit is about 2.8× looser (118 ms). This removes the reading "any realistic fish latency rules it out". With a 70 ms loop, low-speed active stabilisation is not excluded.
- **Not strengthened:** I cannot upgrade to "plausible". The relevant pitch latency in an adult zebrafish is unmeasured, and the cyprinid non-roll value (123 ms) excludes 2 m/s. The robust envelope with the *favourable* proxy (≤ 1.45 m/s) sits where S18 says the wing must be 35–80 cm², about 10–25× the fish's estimated silhouette.
- **Engineering consequence (my inference):** "design for passive stability" moves from prudence back to the recommended default for any design speed ≥ 2 m/s. Active stabilisation of an unstable airframe is defensible only at low speed, and only if an adult pitch latency ≲ 50 ms is measured (§3.5).

## 5a. What this does NOT establish

- It does **not** measure any zebrafish latency. Every τ_d value is another species (goldfish, chub, bass, bluegill), in water, read only at search-summary level.
- Webb's latency definition, frame rate, fish sizes and n are **unknown** to me. If latency there means "first visible movement", the delay to useful corrective torque is longer, which would make §5 less favourable.
- A smaller fish has shorter conduction paths, but I have no number for how much that shortens τ_d. I did not adjust for it.
- Gain is not addressed here. S18-D's point that reflex gains are low wherever measured (0.20–0.44) is untouched and remains a separate caution.
- The control model is linear, single-axis and PD-only, without prediction. A predictive (feedforward or internal-model) controller can in principle exceed PD delay limits. Whether a fish does this in a novel aerial context is unknown, and I do not claim it.
- In-air sensing: S18's otolith free-fall argument and the unknown performance of the eye in air both still apply.

## 6. Reproduction (computation)

```python
import numpy as np, math
def margin(t):   # max kp/kp_min in the stable pocket, lam=1, delay t (=lam*tau)
    w=np.linspace(1e-4,math.pi/(2*t),200000); kp=(1+w**2)*np.cos(w*t)
    if kp[1]<=1: return 1.0
    i=np.argmax(kp<1) if np.any(kp<1) else len(kp)
    return kp[:i].max()
print("tau_c*lam =",math.sqrt(2))
for lt in (0.3,0.5,0.84,1.0,1.2,1.26,1.35,1.41): print(lt, round(margin(lt),3))
rho=1.2; m,L=0.4e-3,0.04; Iy=m*L**2/12; St,lt_,at=1e-4,0.02,1.6   # S18 reference design (assumed)
lam=lambda V,k=1: math.sqrt(0.5*rho*V**2*St*lt_*at*k/Iy)
for V in (1,2,3):
    l=lam(V); print(V, round(l,1), round(500/l), round(1000*math.sqrt(2)/l), [round(l*t/1000,2) for t in (18,70,123,208)])
print([round(1000*math.sqrt(2)/lam(2,k)) for k in (0.5,1,2)])     # geometry sensitivity of the hard limit
print({t: round(math.sqrt(2)/(t/1000)/lam(1),2) for t in (18,35,70,85,123,208)})
a,b=0.3,1.0
for _ in range(50):
    c=(a+b)/2; a,b=(c,b) if margin(c)>2 else (a,c)
print("lam*tau for gain ratio 2:", round(c,3), [round(1000*c/lam(V)) for V in (1,2,3)])
```

Output (my run, 2026-11-04):

- τ_c·λ = 1.414.
- Gain ratios at λτ = 0.30 / 0.50 / 0.84 / 1.00 / 1.20 / 1.26 / 1.35 / 1.41: 6.59 / 2.70 / 1.34 / 1.14 / 1.03 / 1.02 / 1.00 / 1.00.
- λ = 6.0 / 12.0 / 18.0 s⁻¹ at 1 / 2 / 3 m/s.
- Heuristic thresholds 83 / 42 / 28 ms; hard limits 236 / 118 / 79 ms.
- The hard limit at 2 m/s for geometry ×½ / ×1 / ×2 is 167 / 118 / 83 ms.
- A gain ratio of 2 occurs at λτ = 0.609, which gives 101 / 51 / 34 ms.

f_avail sensitivity (§1) uses f_req = λ/2π = 0.95 / 1.91 / 2.86 Hz.

## Sources (read-level)

- Pastor, de la Cruz, Baker 1992, *J Neurophysiol* 68:2003–2015 (goldfish VOR latency 18/20 ms; Purkinje 43 ms): **search-summary**. Attribution versus their 1994 paper (*J Neurophysiol* 72:1383, PubMed 7807219) is disputed between search summaries (preserved, §3.1). Full text **could-not-access**: journals.physiology.org and pubmed are DNS-blocked.
- Webb 2004, *J Exp Biol* 207:955–961, doi:10.1242/jeb.00854 (roll latency 70 ± 15 ms; chub 123 ± 19, bass 201 ± 24, bluegill 208 ± 52 ms): **search-summary**. Full text **could-not-access**: cob.silverchair.com is DNS-blocked.
- Liao 2007, *Phil Trans R Soc B* 362:1973–1993, PMC2442850: **full-text** (partial, via fetch summary). Qualitative citation of Webb 2004 only.
- Sugioka, Tanimoto, Higashijima 2023, *Nat Commun* 14:1217, PMC10006170: **full-text** (partial, via fetch summary). No latency reported.
- Mauthner/C-start latencies (goldfish about 8 ms field-potential-to-movement; larval zebrafish minimum about 3 ms after 75 hpf): **search-summary**. Primary sources not resolved. Not used.
- S18 and S18-D sources as graded in those documents. I did not re-read them.

```swarm-result
{"subproblem": "S18-D-D", "evidence": "derived",
  "answer": "S18-D's most sensitive input is the fish's sensorimotor loop delay: S18-D left it unknown against a '<=42 ms at 2 m/s' threshold that was a robustness heuristic, while the exact delayed-PD limit for the unstable pitch mode is sqrt(2)/lambda = 118 ms (robust, 6 dB gain margin: 51 ms); measured teleost postural latencies (roll 70+/-15 ms; non-roll 123-208 ms, search-summary, larger non-zebrafish species) straddle that limit, so active control of an unstable airframe stays undetermined, robust only below ~1.45 m/s even with the favourable proxy, and passive stability remains the default for >=2 m/s designs.",
  "key_number": "teleost postural response latency 70 +/- 15 ms (roll) vs 123 +/- 19 ms (creek chub, non-roll), against computed hard delay limit 118 ms and robust limit 51 ms at 2 m/s",
  "verdict": "stands",
  "depends_on": [
    "S18-D conclusion: bandwidth argument falls; active control undetermined; latency the binding constraint (<=42 ms at 2 m/s), adult latency unknown",
    "S18 reference geometry: m=0.4 g, L=4 cm, I_y=mL^2/12, S_t=1 cm^2, l_t=2 cm, a_t=1.6/rad, rho_air=1.2 kg/m^3 (assumed)",
    "S18 convention: unstable-design divergence rate lambda equals stable-design omega_n = 6.0*V s^-1 (|static margin| unchanged; assumed)",
    "Glide speeds 1-3 m/s (assumed; anchored to guppy max air speed 1.24 m/s, Soares & Bierman 2013)",
    "S18 computed wing area needed: 14-20 cm^2 at 2 m/s, 35-53 cm^2 at 1.24 m/s, >80 cm^2 at <=1 m/s",
    "Control model: linear single-axis pitch, delayed PD feedback, aerodynamic damping and heave coupling ignored; derived tau_crit = sqrt(2)/lambda",
    "Robustness criterion: gain ratio >= 2 (6 dB) requires lambda*tau <= 0.61 (computed)",
    "Webb 2004 J Exp Biol 207:955: teleost roll-disturbance response latency 70+/-15 ms; non-roll 123+/-19 (creek chub), 201+/-24 (smallmouth bass), 208+/-52 ms (bluegill) (search-summary only)",
    "Claim: teleost postural latency in water transfers to a 4 cm adult zebrafish correcting pitch in air (cross-species, cross-medium inference, unverified)",
    "Pastor, de la Cruz & Baker 1992 J Neurophysiol 68:2003: goldfish VOR latency 18-20 ms, Purkinje 43 ms (search-summary; attribution vs their 1994 paper disputed)",
    "Inference: VOR latency is a lower bound on any vestibular-to-fin loop delay",
    "Adult Danio rerio pitch/roll sensorimotor latency: unknown (not found; search scope in section 3.4)",
    "S18-D: toadfish canal afferent bandwidth >=10 Hz (Boyle & Highstein 1990; Rabbitt et al. 2004) - f_avail no longer limiting",
    "S18-D / S18: reflex gains low where measured (0.20-0.44) - not addressed here",
    "S18 physics: otolith senses specific force, ~0 in ballistic flight"
  ]}
```
