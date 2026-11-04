# Challenge 290: S18-D "the bandwidth argument against active attitude control falls"

**Claim under review** (S18-D, `docs/research/fish/S18-deepen.md` on branch `origin/claude/deepen-s18-zebrafish-air-3u64z4`): S18 used 0.5 Hz, but that figure was the highest frequency the larval test protocols used. Adult toadfish canal afferents respond over 0.1–10/20 Hz. The required/available ratio is therefore 0.1–0.3, not 2–6 (point value 0.19 = 1.9/10). Active control is undetermined. The claim itself flags that replicate-260's pitch mode of 3–7 Hz is not reconciled. The recorded evidence level is **derived**.

**What I read:** S18-deepen.md in full. S18-behaviour.md (branch `origin/claude/zebrafish-aerial-attitude-k8hgr8`), its geometry and §3.6 only, via grep. replicate-260.md and replicate-260-model.py in full (branch `origin/claude/zebrafish-glider-attitude-fpeh9d`). External sources are listed at the end with read-levels.

**Verdict: WEAKENED.** The qualitative core survives: on present evidence the peripheral angular-rate sensor is not what limits active control. The recorded value, 0.19 described as a "required/available bandwidth ratio", has three problems:

- It is a ratio against the peripheral sensor, standing in for the whole control loop.
- It is evaluated at a speed the reference airframe does not trim at.
- It is the low end of the band once the unreconciled replicate-260 geometry is included.

---

## 1. Independent arithmetic (computation; script `challenge-290.py`)

These are the stated S18 inputs: m = 0.4 g, L = 4 cm, I_y = mL²/12 = 5.33 × 10⁻⁸ kg m², S_t = 1 cm², l_t = 2 cm, a_t = 1.6 rad⁻¹, ρ = 1.2. I computed f = √(½ρV² S_t l_t a_t / I_y) / 2π myself.

| V (m/s) | f_req (Hz) | R at 0.5 Hz | R at 10 Hz | R at 20 Hz |
|---|---|---|---|---|
| 1 | 0.955 | 1.91 | 0.095 | 0.048 |
| 2 | 1.91 | 3.82 | 0.191 | 0.095 |
| 3 | 2.87 | 5.73 | 0.287 | 0.143 |

The author's figures reproduce: 1.9/10 = 0.19, 1.9/0.5 = 3.8, and the range 0.1–0.3 for V = 1–3 m/s. The replicate-260 band also reproduces (my division): 3.1 / 5.0 / 7.2 Hz ÷ 10 Hz gives **0.31 / 0.50 / 0.72**. The claim says "~0.3–0.7", which is correct. **No arithmetic error found.**

## 2. Proxy: peripheral sensor bandwidth standing in for loop bandwidth

S18's 0.5 Hz was a **whole-reflex** figure, sensor through brainstem to eye muscle, even though it was only a test ceiling. S18-D replaces it with a **peripheral afferent** figure: toadfish canal afferents (Boyle & Highstein 1990) and hair-cell microphonics (Rabbitt et al. 2004). The numerator and denominator of R therefore now refer to different things than they did in S18. The quantity that decides whether active control is possible is the closed-loop bandwidth of sensor + central processing + motor plant + delay. S18-D's ratio bounds only the first term.

The author does say this: "Active control undetermined (reflex gain…, unknown adult latency)". So I am not saying the claim hides it. My objection is to the label on the recorded value. "0.19 required/available bandwidth ratio" will be read as the controller's ratio, when it is the **sensor's** ratio. My corrected wording: *the required pitch frequency divided by the highest frequency at which toadfish canal afferents were tested and responded*.

A second proxy runs the other way and goes in the author's favour. 10 Hz is itself the upper end of the toadfish protocol, not a measured corner frequency. My fetch of the PMC6570080 abstract confirms "0.001–10 Hz" and reports no corner frequencies. So 10 Hz is a lower bound on sensor bandwidth, and every R computed against it is an **upper bound**. This is the same test-ceiling problem S18-D found in S18. Here it works in the conservative direction, so it does not undermine the "falls" verdict.

## 3. Hidden assumptions, relaxed

**(a) Threshold "too slow means R > 1".** A feedback sensor normally needs bandwidth a few times above the loop crossover. The crossover itself must be at or above the mode frequency (or the unstable pole), as S18's own rule of thumb says. I computed the sensor bandwidth needed for a margin of k = 3 / 5 / 10 over the mode:

- for f_mode = 1.9 Hz: 5.7 / 9.5 / 19 Hz
- for f_mode = 5 Hz: 15 / 25 / 50 Hz
- for f_mode = 7.2 Hz: 22 / 36 / 72 Hz

The demonstrated ≥ 10 Hz therefore gives a comfortable margin (about 5×) only at the S18 design point. Against the replicate-260 band, the demonstrated range gives a margin of 1.4–3×. That does not show the sensor is too slow, because 10 Hz is a floor. It does mean "bandwidth argument falls" is too strong for the upper half of the plausible airframe band. **"Not shown to be limiting"** is the accurate wording. My judgement is that k ≈ 3–10 is the ordinary range in control engineering; I did not derive or source it here.

**(b) V = 2 m/s as the design case.** S18 itself says its 10 cm² reference wing is undersized at 2 m/s. I computed the trim speed of that wing at 0.4 g as V = √(2mg/(ρ S C_L)): **2.56 / 2.95 / 3.62 m/s** for C_L = 1.0 / 0.75 / 0.5. That gives f_req = **2.44 / 2.82 / 3.45 Hz** and R at 10 Hz = **0.24 / 0.28 / 0.35**. The headline 0.19 is not a trim point of S18's own airframe. On S18's geometry the self-consistent value is 0.24–0.35. replicate-260 independently computes a trim speed of 3.0–5.0 m/s (calculated), which points the same way.

**(c) Toadfish to zebrafish transfer.** The author flags this. The scaling argument in §3.3 (smaller ducts raise the upper corner of the Steinhausen model and cost sensitivity) is a computation with an assumed ν and no measured duct radius. I did not find an adult *Danio* canal frequency response either (scope below). That leaves the transfer exactly as uncertain as the author says, no more and no less.

## 4. Evidence level

"Derived" is honest. The 0.19 is presented as a computation. The toadfish inputs are given at their read-levels (abstract; partial full text through a fetch summary), and the cross-species step is stated. I found no point where a calculated number is presented as an observation. The one presentational defect is the label described in §2.

## 5. Counter-examples and missed regimes

- **Taxon closer than toadfish (supports the author).** Montgomery, Macdonald & Housley 1990, *J Comp Physiol A* 166:407–410, doi:10.1007/BF00204814. They recorded central vestibular units in the Antarctic notothenioid *Pagothenia borchgrevinki* at 0.05–16 Hz. The abstract says vestibular function there "is comparable to that previously reported in goldfish" *primary afferents*. Read-level: **search-summary** (link.springer.com fails DNS in this session). This is an indirect hint that cyprinid (goldfish) canal afferents work up to the order of 10 Hz. I could not read the goldfish data themselves. **My inference:** this narrows the cross-species gap a little, from batrachoidiform to cyprinid, but only at the peripheral level, and only through a secondhand comparison.
- Hartmann & Klinke 1980, on goldfish canal afferents under high-frequency stimulation, was named in a search result. Read-level: **listing**. I could not access the abstract and use no numbers from it.
- **Adult teleost postural-reflex latency in ms: unknown.** One standard search ("fish vestibulospinal OR vestibular postural reflex latency milliseconds adult teleost fin response roll tilt") returned only larval zebrafish work (PMC10006170, a body-bend righting reflex). That reflex is a buoyancy-moment mechanism, not a fast fin loop. It is consistent with the author's point that larval posture control is slow and bout-like. It provides no adult number.
- I found **no published counter-example** in which an adult teleost canal shows a measured upper corner below about 3 Hz. Scope: 3 standard WebSearch calls and 2 WebFetch calls (one failed on DNS), all on 2026-11-04. This is a narrow search and the negative is weak.

## 6. Bottom line

The arithmetic is correct, and the evidence level is honest. The central qualitative move holds as far as the peripheral sensor goes: 0.5 Hz was a test ceiling, and the only adult fish canal data found respond to ≥ 10 Hz. The claim is weakened because the recorded value of 0.19 has three defects:

- It describes the sensor, but its label says "available bandwidth" for the whole controller.
- It uses V = 2 m/s, which the S18 airframe cannot trim at. The self-consistent value is 0.24–0.35.
- It sits at the low end of an unreconciled band that reaches 0.72 on replicate-260's geometry, where the demonstrated sensor margin is only 1.4–3×.

All of these R values are upper bounds, because 10 Hz is a test floor rather than a measured corner. "The bandwidth argument falls" should read **"sensor bandwidth is not shown to be limiting"**. Active control remains undetermined, as the author says.

## Sources (read-level)

- S18-deepen.md, S18-behaviour.md, replicate-260.md / -model.py (repo branches): full-text (S18-behaviour: grep-targeted sections).
- Boyle & Highstein 1990, *J Neurosci* 10:1557, PMC6570080: **abstract** (my own fetch; confirms 0.001–10 Hz, 5–100° s⁻¹, three afferent classes, no corners reported).
- Rabbitt et al. 2004/5, PMC3000937: **listing** for me (seen in search results; not re-fetched). I rely on S18-D's partial full-text read for 0.1–20 Hz.
- Montgomery, Macdonald & Housley 1990, *J Comp Physiol A* 166:407: **search-summary**; full text could-not-access (link.springer.com DNS-blocked).
- Hartmann & Klinke 1980 (goldfish canal afferents): **listing** only.
- Larval zebrafish postural body-bend study, PMC10006170 / bioRxiv 2022.09.22.508983: **search-summary**.

```swarm-challenge
{"claim_id": 290, "outcome": "weakened", "reason": "Arithmetic reproduces and the peripheral-sensor point stands, but 0.19 is a sensor-only ratio labelled as loop 'available bandwidth', is evaluated at 2 m/s where S18's own 10 cm2 wing cannot trim (trim 2.6-3.6 m/s gives 0.24-0.35), and rises to 0.31-0.72 on replicate-260's geometry where a 10 Hz floor gives only 1.4-3x sensor margin, so 'falls' should read 'sensor bandwidth not shown to be limiting'.",
  "corrected_value": "0.24-0.35 (S18 geometry at trim speed, C_L 0.5-1.0) to 0.31-0.72 (replicate-260 geometry); ratio of pitch-mode frequency to highest tested toadfish canal-afferent frequency (10 Hz), an upper bound, not a loop-bandwidth ratio",
  "depends_on": [
    "S18 reference geometry: m=0.4 g, L=4 cm, I_y=mL^2/12, S_t=1 cm^2, l_t=2 cm, a_t=1.6/rad, wing 10 cm^2 (assumed design)",
    "Trim-speed relation V=sqrt(2mg/(rho S C_L)) with C_L 0.5-1.0 (assumed)",
    "replicate-260 pitch-mode band 3.1-7.2 Hz (calculated, assumed geometry and static margin 0.05-0.25 c)",
    "Boyle & Highstein 1990 J Neurosci 10:1557: toadfish canal afferents tested 0.001-10 Hz, no corner reported (abstract)",
    "Rabbitt et al. 2004 J Neurophysiol 93:424: microphonic flat 0.1-20 Hz (via S18-D partial full text)",
    "Montgomery, Macdonald & Housley 1990 J Comp Physiol A 166:407: Antarctic fish central units 0.05-16 Hz comparable to goldfish afferents (search-summary)",
    "Control rule of thumb: sensor bandwidth should exceed mode frequency by k~3-10 (engineering judgement, not sourced here)",
    "Cross-species transfer of teleost canal bandwidth to adult Danio rerio (unverified)",
    "Adult Danio sensorimotor latency: unknown"
  ]}
```
