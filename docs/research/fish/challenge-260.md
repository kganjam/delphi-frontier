# Challenge 260: adversarial review of claim S18 (zebrafish glider attitude control)

**Claim under review (the author's words, from `harvest:zebrafish-aerial-attitude-k8hgr8`):**
An engineered 0.4 g zebrafish glider could hold attitude only passively (rear stabiliser, positive
static margin; computed pitch mode ~1–3 Hz, roll-rate damping 1–4 ms). Active vestibular attitude
control is not supported, because the utricle loses its gravity reference in flight, all measured
zebrafish vestibular and gaze-reflex data are larval and ≤0.5 Hz, adult canal bandwidth is unknown,
and no small non-exocoetid teleost was found controlling attitude in air. KEY: computed pitch short
period ~1.9 Hz at 2 m/s versus a highest measured zebrafish vestibular-reflex test frequency of 0.5 Hz.

**Recorded evidence level:** derived. **Value:** n/a.

**Source access:** the harvest record and the author's reference-design inputs are **not in this
repository** (I searched the tree and its branches). I could not see the author's working, so I rebuilt
the numbers from first principles with stated assumptions. That independence is what the review
asked for, but it also means I cannot check the specific 1.9 Hz figure against its own inputs.

## 1. Independent arithmetic (calculated by me, not observed)

These assumptions are mine: m = 0.4 g, V = 2 m/s, ρ = 1.2 kg/m³ (so q = 2.4 Pa), cruise C_L of
0.6–1.0, giving a wing area S = mg/(qC_L) of 16–27 cm². Aspect ratio is 3–5, with C_Lα = 2πA/(A+2).
Static margin is 0.05–0.15 c̄. I_yy = 1.5 × mL²/12 for a body length L of 3–4 cm, where the 1.5
factor allows for wing and tail mass. The undamped short-period frequency is
f = (1/2π)·√(q S c̄ C_Lα SM / I_yy).

- **Pitch short-period, undamped: 2.2–7.9 Hz** across that grid (lowest case: C_L 1.0, AR 5,
  SM 0.05, L 4 cm). With damping ratio ζ ≈ 0.3–0.7, the damped frequency is 0.7–0.95 × that.
  - My estimate is **at or above the top of the author's 1–3 Hz band**. The author's 1.9 Hz is
    reachable only with a low static margin, a high C_L and a large pitch inertia. It is a plausible
    lower bound, not a central value.
- **Roll-subsidence time constant:** τ = I_xx / L_p, with C_lp = −C_Lα/8. I_xx counts wing
  mass of 10–50 mg spread over the span. **τ = 1.0–9.7 ms.**
  - The author's 1–4 ms is the light-wing end of that range. With 50 mg of wing structure, τ is
    5–10 ms.

**Effect on the claim:** both corrections strengthen the author's conclusion rather than weaken it.
A higher pitch mode widens the gap to any 0.5 Hz reflex, and the roll time constant is still at least
two orders of magnitude below any measured reflex period. The arithmetic does **not** break the claim.
The stated bands are a little narrow, and the pitch band is biased low.

## 2. Proxy defect in the KEY comparison (real)

The KEY compares a mode frequency with the **"highest measured zebrafish vestibular-reflex test
frequency" (0.5 Hz)**. That number is the highest frequency anyone happened to test. It is not a
measured bandwidth or cutoff. The quantity that matters is the closed-loop bandwidth of the sensor,
the neural path and the effector (−3 dB or phase-crossover frequency). Not having tested above 0.5 Hz
is a **negative search result, not a limit**. Presented as "versus", it reads like a measured ceiling.

Counter-evidence from other teleosts, which the author did not cite:
- **Goldfish (*Carassius auratus*), adult:** the dark VOR is near-ideal (gain ≈ 1, phase ≈ 180°)
  from about 1/32 to **2 Hz** (Pastor et al. 1992, J Neurophysiol; read-level: **search-summary**).
  That is four times the claim's 0.5 Hz ceiling, in a cyprinid close to zebrafish.
- **Toadfish (*Opsanus tau*), adult:** horizontal-canal afferents were tested from 0.001 to
  **10 Hz** (Boyle & Highstein 1990). Transfer functions run to about 0.02–**30 Hz**, and the
  high-gain units show a high-frequency gain boost and phase lead (Highstein et al. 1996).
  Read-level for both: **abstract / search-summary**. So teleost *canal transduction* reaches at
  least about 10 Hz.
- **Larval zebrafish:** Bianco et al. 2012 (Curr Biol) report a utricle-driven VOR that works "over a
  broad frequency range". Read-level: **search-summary**, and I could not get the numbers. Mo et al.
  2010 used 0.25 Hz. I found no larval data at 1–2 Hz, which fits the author's ≤0.5 Hz statement
  *as a statement about tested frequencies*.

**My inference, kept separate from the author's claim:** the gap to the pitch mode is smaller than the
claim implies. Using cyprinid VOR data (≈2 Hz) and teleost canal afferent data (≥10 Hz), a reflex
loop with roughly 2 Hz bandwidth is plausible for an adult cyprinid. That is comparable to my
2–8 Hz pitch short period, not 4–15× below it. Whether adult *zebrafish* reach this is
**unknown**. I found no adult zebrafish VOR or canal frequency-response data (scope: 3 web searches,
listed below).

## 3. Hidden assumption: "the utricle loses its gravity reference in flight" (overstated)

An otolith senses specific force, which is the non-gravitational force per unit mass.
- **Ballistic phase** (leaving the water before lift builds): specific force ≈ 0, so the utricle
  really has no reference. The author is right here.
- **Steady glide:** aerodynamic force = −weight, so the specific force is about 1 g along the true
  vertical. The utricle **keeps** a correct gravity reference. This is the basic physics of every
  accelerometer on a gliding aircraft.
- **Coordinated turns and transient manoeuvres:** the utricle reads the apparent vertical. Bank and
  the turn acceleration cannot be told apart (the somatogravic ambiguity). The reference is ambiguous,
  not lost.

So the sub-claim holds only for the ballistic phase. For steady glide it is wrong as worded. Even so,
the canals sense angular rate, which is what you need to damp a short-period mode, and they do not
need a gravity reference at all.

## 4. Relaxing the conclusion's framing

"Could hold attitude **only** passively" partly follows from the author's own numbers. A roll time
constant of 1–10 ms is far faster than any neural loop (fish reflex latencies are at least several ms
of synaptic and muscle delay, and I have no zebrafish adult number: **unknown**). So passive roll
damping is the only option on that axis. For **pitch**, a passively stable airframe does not need a
controller faster than the mode. A slow (<1 Hz) loop that trims glide angle or corrects drift on top
of passive stability is not ruled out by any evidence the claim cites. "Only passively" should read
"stabilised passively; any active vestibular contribution is limited to slow trim and is
unsupported by zebrafish data".

## 5. Evidence level

"derived" is honest for the mode frequencies, which are calculated. The KEY's 0.5 Hz is a
literature-search summary of tested frequencies, not a measured limit. It needs its own label, and the
"versus" framing should say this is a **test-range edge, not a bandwidth**. The negative search
("13 web searches, mostly abstract-level") is scoped, which is good. My 3 searches found two adult
teleost datasets above 0.5 Hz that the scope missed.

## 6. Counter-example taxa

I did not search for, and do not know of, a small non-exocoetid teleost actively controlling attitude
in air. That part of the claim stands with the author's scope plus mine (I did no taxon search:
**not tested**). Freshwater hatchetfishes (Gasteropelecidae) are often described as jumping or
"flying". I did not verify any attitude-control data for them, so I record this as a lead, not a
counter-example.

## Verdict: WEAKENED

- **The core conclusion survives.** Passive stabilisation is required: roll subsidence takes 1–10 ms,
  my pitch mode is 2–8 Hz, and there are no adult zebrafish frequency-response data.
- **The KEY comparison is weakened.** 0.5 Hz is the highest frequency tested in larval zebrafish, not
  a bandwidth. Adult goldfish VOR is near-ideal to 2 Hz, and toadfish canal afferents respond to at
  least 10 Hz.
- **The "utricle loses gravity reference" sub-claim is wrong for steady glide.** It holds only for
  the ballistic phase.
- **The pitch band is biased low.** My independent estimate is 2.2–7.9 Hz, against the author's
  1–3 Hz. The roll band is too narrow: mine is 1.0–9.7 ms, against 1–4 ms.

## Sources (read-levels)

- Boyle R., Highstein S.M. 1990, J Neurosci, toadfish horizontal-canal afferents, 0.001–10 Hz:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6570080 (**search-summary/abstract**).
- Highstein S.M. et al. 1996, J Neurophysiol 75:575–596, toadfish canal transfer functions
  ~0.02–30 Hz: https://pmc.ncbi.nlm.nih.gov/articles/PMC2774407 (**search-summary/abstract**).
- Rabbitt, Boyle, Highstein, canal microphonic flat to ~10 Hz with a resonance near 30 Hz:
  https://ntrs.nasa.gov/citations/20020060743 (**listing/abstract**).
- Pastor A.M. et al. 1992, J Neurophysiol, goldfish VOR from 1/32 to 2 Hz:
  https://read.qxmd.com/read/1491254 (**search-summary**).
- Bianco I.H. et al. 2012, Curr Biol, larval zebrafish utricular VOR: https://www.zfin.org/ZDB-PUB-120702-13
  (**search-summary**; frequency values unknown).
- Mo W. et al. 2010, BMC Neurosci, larval zebrafish at 0.25 Hz: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2941499/
  (**search-summary**).

**Search scope for my negatives:** 3 web searches (toadfish canal afferent frequency response,
goldfish VOR frequency range, and larval zebrafish VOR at 1–2 Hz), all at search-summary or abstract
level. I did no taxon search for aerial attitude control. The calculation in §1 is mine. It is not the
author's, and none of it is measured.

```swarm-challenge
{"claim_id": 260, "outcome": "weakened", "reason": "The passive-only conclusion survives my independent aerodynamics (pitch 2.2-7.9 Hz, roll tau 1-10 ms), but the KEY's 0.5 Hz is the highest frequency tested in larval zebrafish rather than a bandwidth (adult goldfish VOR is near-ideal to 2 Hz and toadfish canal afferents respond to at least 10 Hz), and the utricle keeps a gravity reference in steady glide, losing it only in the ballistic phase.", "corrected_value": "pitch short-period (undamped) 2.2-7.9 Hz at 2 m/s; roll-subsidence tau 1.0-9.7 ms; teleost vestibular reflex tested to >=2 Hz (goldfish VOR), canal afferents >=10 Hz (toadfish)", "depends_on": ["assumed design: m=0.4 g, V=2 m/s, C_L 0.6-1.0, AR 3-5, static margin 0.05-0.15, body length 3-4 cm, wing mass 10-50 mg", "Pastor et al. 1992 goldfish VOR near-ideal 1/32-2 Hz (search-summary)", "Boyle & Highstein 1990 / Highstein et al. 1996 toadfish canal afferents 0.001-10 Hz and ~0.02-30 Hz (abstract)", "otolith specific-force physics: steady glide aerodynamic force = -weight", "absence of adult zebrafish vestibular frequency-response data (3 searches)"]}
```
