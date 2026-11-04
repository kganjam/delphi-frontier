# Challenge 137: adversarial review of S10-D-D-D (muscle power at 21.9 Hz)

**Claim under review:** `harvest:deepen-s10-d-d-juuuwn`.
- File: `docs/research/fish/S10-D-D-deepen.md` on branch `claude/deepen-s10-d-d-juuuwn`, read in full.
- Recorded evidence level: *derived*.

**The claim's key number:**
- P_muscle at 21.9 Hz is 58–67 W/kg.
- Its bracket is 58–88 W/kg at 8% strain, with a "strict upper bound" of 126 W/kg.
- These replace 134.4 W/kg measured at 80 Hz.
- Verdict: **strengthens**.
  - Every R = 4 cm hover margin doubles.
  - The forward-flight corners return to "fails".
  - The only exceptions it allows are an idealised rectangular loop or an unmeasured large strain.

**My script:** `docs/research/fish/challenge-137_calc.py`.
- **Every number below that is not attributed to Mead et al. is a calculation, not an observation.**

## 1. Independent arithmetic

I recomputed these from the stated inputs with my own code, not the author's script:

| Quantity | Mine | Author |
|---|---|---|
| Design frequency at R = 4 cm (S10 §3c method) | 21.94 Hz | 21.9 |
| Hover requirement, R = 4 cm, M = 1.5, f = 0.0138 / 0.0164 / 0.0276 | 730 / 614 / 365 W/kg | same |
| Forward-flight minimum, upper f, C_D,pro = 0.05 / 0.10 / 0.20 | 96.5 / 120.5 / 168.4 W/kg | 97 / 121 / 168 |
| Plateau reading, 2.63 J/kg × 21.9 Hz | 57.7 W/kg | 58 |
| Linear extrapolation of work per cycle, 40→80 Hz trend, giving 3.06 J/kg | 67 W/kg | 67 |
| Rectangle at 8% strain: 76 kPa × 0.08 / 1060 kg/m³ = 5.74 J/kg | 125.8 W/kg | 126 |
| Loop fill at 40 / 80 Hz | 0.46 / 0.29 | same |

**The arithmetic survives.** I first got the linear extrapolation wrong with a sign error, giving 48 W/kg. The author's value of 67 W/kg is correct.

## 2. Source check: Mead et al. 2020

Source: Mead et al. 2020, *Biophys J* 119:806, PMC7451861. **Read-level: full-text** (pmc.ncbi.nlm.nih.gov HTML, fetched 2026-11-04).

These are the authors' statements, confirmed verbatim:
- 2.63 ± 0.18 J/kg per cycle at 40 Hz.
- 134.4 ± 19.9 W/kg at 80 Hz.
- 122.9 ± 11.1 W/kg at 100 Hz.
- Loops at 40, 60, 80, 100 and 120 Hz only.
- Myotome length cycled from 1.01 to 1.09 × starting length (8%).
- "a single supramaximal 0.4-ms" pulse before shortening in each of the first five cycles.
- 76 ± 3 mN/mm².
- Twitch/tetanus ratio 0.91.
- Twitch "complete within 25 ms", with a full width at half-maximal stress of 11 ± 1 ms.
- A fully fused tetanus at a 300 Hz stimulus rate.

Two further statements matter here and were **not used by the author**:
- At a constant shortening speed of 7 ± 1 lengths/s, the muscle develops 86 ± 2% of isometric stress.
- The authors estimate V_max ≥ 45 lengths/s.

The author's quotations are faithful. The measured values are labelled as measured, and the 21.9 Hz values are labelled as calculated. **I found no evidence-level defect in the prose.**

There is one labelling issue. The key number calls 126 W/kg a "strict upper bound". It is a bound only under three conditions:
- 8% strain;
- larval isometric stress;
- shortening force ≤ isometric force.

The body text says this, but the key number drops the qualifiers. This is a scope defect, not a refutation.

## 3. The proxy the claim's central value rests on

**The quantity that matters** is the net work per cycle that a muscle can deliver at 21.9 Hz under the activation pattern it would actually receive.

**The proxy used** is the 40–80 Hz single-twitch-per-cycle values, taken as either a plateau or a linear trend.

**Why the proxy is the wrong one:**
- Single-pulse stimulation was a feature of the protocol, matched to larval swimming at 40–100 Hz.
- At 21.9 Hz the shortening half-cycle lasts 22.8 ms, and the twitch FWHM is 11 ms.
- A single pulse therefore leaves most of the shortening phase poorly activated. The author's "plateau" reasoning (§3b) assumes exactly that limitation is fixed.
- *My inference, not measured:* a muscle driven at 22 Hz would receive a burst of pulses per cycle. The author lists 1–3 pulses only as a future measurement (§3e). It never enters their bracket.
- Velocity does not limit force at this frequency. The peak shortening speed of an 8% sinusoid at 21.9 Hz is π × 21.9 × 0.08 = **5.5 L/s** (calculation). That is below the 7 L/s at which Mead measured 86% of isometric stress.
- So nothing in the measured force–velocity data stops a well-activated loop at 21.9 Hz from approaching the rectangle. The limit is activation and relaxation kinetics, and the claim did not model those.

## 4. Testing the hidden assumption: a model calibrated to Mead's own loops

**Model** (calculation; the model is my assumption):
- Force = σ₀ · A(t) · FV(v).
- FV is linear on the shortening side, set to 0.86 at 7 L/s (V_max = 50 L/s).
- Lengthening force is modestly enhanced, up to 1.3 × σ₀.
- A(t) is a saturating sum of twitches, scaled so that a single twitch peaks at 0.91 of tetanus.
- Sinusoidal 8% strain; net work is computed at steady state; stimulus phase and inter-pulse interval are optimised.

**Part 1: a fixed 11 ms twitch, (t/tp)·e^(1−t/tp), fails calibration.**
- It gives 2.26 J/kg at 40 Hz, against 2.63 measured.
- It gives *negative* work at 80 Hz, against +1.68 measured.
- I report it and discard it. Isometric twitch kinetics do not describe these loops.

**Part 2: an in-loop activation fitted to the three measured single-twitch points.**
- The shape is (1−e^(−t/tr))·e^(−t/td).
- The three best fits all have td = 3 ms and tr = 0.5–1.5 ms.
- Fitted work at 40 / 80 / 100 Hz is 2.59 / 1.59 / 0.85 J/kg, against 2.63 / 1.68 / 1.23 measured. The 100 Hz point is underfit.
- The fitted FWHM is about 4 ms, compared with the 11 ms isometric twitch. I read this as shortening deactivation absorbed into an effective activation. **It is a fit, not a measurement.**

**Prediction at 21.9 Hz, 8% strain** (calculation; ranges span the three best fits):

| Pulses per cycle | Work per cycle (J/kg) | P_muscle (W/kg) | Loop fill | Corner: upper f, C_D,pro 0.05 (needs 96.5) | Corner: C_D,pro 0.10 (needs 120.5) |
|---|---|---|---|---|---|
| 1 | 1.78–2.11 | 39–46 | 0.31–0.37 | fails | fails |
| 2 | 2.97–3.39 | 65–74 | 0.52–0.59 | fails | fails |
| 3 | 3.69–4.06 | 81–89 | 0.64–0.71 | fails | fails |
| 4 | 4.18–4.48 | 92–98 | 0.73–0.78 | borderline | fails |
| 5–8 | 4.46–4.83 | **98–106** | 0.78–0.84 | **flips** | fails |

### What this does to the claim

1. **The central value 58–67 W/kg is not the single-twitch value.**
   - The calibrated single-twitch value at 21.9 Hz is *lower*, at 39–46 W/kg. The work per cycle does not plateau, because a short in-loop activation covers only part of the 23 ms shortening phase.
   - It is not the multi-pulse value either, which is higher.
   - So the central value is an interpolation that matches no stimulation regime.
2. **The statement "no reading of the measured data reaches 97 W/kg at 22 Hz and 8% strain" does not survive.**
   - A model fitted to the measured data reaches 98–106 W/kg with a 5–8 pulse burst at a 3–4 ms pulse interval. That is roughly the measured fusion regime.
   - It does this at the *measured* 8% strain, with a non-rectangular loop (fill 0.78–0.84).
   - So there is a third route to flipping the most generous forward-flight corner (upper f, C_D,pro 0.05). The claim omitted it, and it needs neither an idealised loop nor an unmeasured strain.
   - The C_D,pro = 0.10 corner (120.5 W/kg) still fails in every regime I modelled. The claim treats it as flipping only under the rectangle or large strain, and I agree.
3. **The hover margins do not double.**
   - At the burst-calibrated 98–106 W/kg, central f gives 614 / 106–98 = **×5.8–6.3** (calculation), compared with ×4.6 at 134.4 W/kg and the claim's ×9.2–10.6.
   - Upper f gives **×3.4–3.7**, compared with ×2.7 at 134.4 W/kg and the claim's ×5.4–6.3.
   - The verdict *direction* survives for hover: every frequency-matched value I found is still below 134.4 W/kg. The *magnitude* ("doubles every margin") does not survive.
4. **The 126 W/kg ceiling stands** at 8% strain with larval σ₀. My model never exceeded it at 8% strain.

**My model's weaknesses, stated against my own result:**
- It has three calibration points, and the 100 Hz point is underfit.
- It uses one functional form.
- It assumes activation sums linearly and then saturates, an assumption not tested in these tails.
- It has no fatigue. Mead stimulated only 5 of 10 cycles.
- It uses an assumed lengthening enhancement.
- With an *isometric-like* slow relaxation (Part 1), bursts top out at 88–91 W/kg, below 96.5 W/kg. In that case the claim's forward-flight conclusion holds.
- So the corner sits on the line, between **91 and 106 W/kg against 96.5 W/kg** (calculation). In-loop relaxation kinetics at 22 Hz decide it, and those are `unknown`.

## 5. Regimes and counter-examples

- **Adult fish fast muscle at low frequency** (read-level: **search-summary**; I could not open the abstracts because openpolar.no is outside this session's network allowlist and journals.biologists.com returned 403):
  - Atlantic cod fast fibres: about 16–28 W/kg at their optimal frequency, falling with body length. Maximum stress was about 51–82 kPa.
  - *Myoxocephalus scorpius* fast fibres: 25–35 W/kg at 5–7 Hz at 4 °C.
  - These are temperatures colder than 28 °C. They agree with the claim's direction, since adult fish fast muscle performs worse. They do not test 22 Hz.
- **Adult zebrafish myofibrils:** a search result reports adult skeletal myofibril force at about half the larval value (18 vs 40 nN/µm²). Read-level: **search-summary** only. I could not identify or open the paper (par.nsf.gov was outside the allowlist), and I did not use this number.
- **Mouse EDL:** 132 W/kg at 9 Hz (37 °C), cited by Mead et al. (full-text). It shows that a vertebrate fast muscle can reach ~130 W/kg at low cycle frequency when its kinetics match that frequency. This is a matching-of-kinetics point; it is not a fish datum.
- **Negative search scope:** I found no work loop on zebrafish (larval or adult) below 40 Hz, and none with multiple pulses per cycle, in Mead 2020 or in the author's Europe PMC search (§3d of the claim). I ran two further Europe PMC queries for adult zebrafish isometric stress and cod scaling; neither returned anything usable. Web of Science, Scopus and theses were not searched.

## 6. Verdict: WEAKENED

**What survives:**
- The arithmetic.
- The source quotations.
- The evidence labelling of the prose.
- The direction of the hover verdict: 134.4 W/kg overstated the muscle at 21.9 Hz.
- The 126 W/kg ceiling at 8% strain.

**What does not survive:**
1. The central 58–67 W/kg. It rests on a single-twitch-per-cycle proxy for activation, and the claim never models multi-pulse activation.
2. The claim that "no reading of the measured data reaches 97 W/kg at 22 Hz and 8% strain". A calibrated burst model gives 98–106 W/kg.
3. The statement that every R = 4 cm hover margin "doubles". It rises by about ×1.3–1.4.

**The forward-flight corner (upper f, C_D,pro 0.05)** is open on the measured strain alone. It is not restored to "fails". The C_D,pro 0.10 corner stays "fails" except under the claim's own rectangular or large-strain exception.

**Decisive measurement:** the claim's own §3e, extended to **3–8 pulses per cycle at about 300 Hz**. One larval rig session at 20–25 Hz would settle it.

```swarm-challenge
{"claim_id": 137, "outcome": "weakened", "reason": "The arithmetic and sources check out, but the 58-67 W/kg value assumes one twitch per cycle; a model fitted to Mead's measured 40/80/100 Hz loops gives 39-46 W/kg for one pulse and 98-106 W/kg for a 5-8 pulse burst at 21.9 Hz and the measured 8% strain, so hover margins grow about x1.3-1.4 (not x2) and the upper-f, CDpro 0.05 forward-flight corner (needs 96.5 W/kg) is open rather than restored to 'fails'.", "corrected_value": "P_muscle(21.9 Hz, 8% strain) = 39-46 W/kg with 1 pulse/cycle, 81-89 W/kg with 3 pulses, 98-106 W/kg with 5-8 pulses (all calculated from a model fitted to measured larval single-twitch loops); ceiling 126 W/kg at 8% strain and larval stress; hover margin at R = 4 cm, central f, about x5.8-6.3", "depends_on": ["Mead et al. 2020 (full-text): net work 2.63 J/kg at 40 Hz, 134.4 W/kg at 80 Hz, 122.9 W/kg at 100 Hz, 8% sinusoidal strain (1.01-1.09 L0), single 0.4 ms pulse per cycle, 28 C", "Mead et al. 2020 (full-text): 76 mN/mm2 isometric stress, twitch/tetanus 0.91, twitch FWHM 11 ms, complete within 25 ms, fused tetanus at 300 Hz, 86% of isometric stress at 7 L/s, Vmax >= 45 L/s, density 1.06 g/cm3", "model assumption: force = sigma0 x saturating summed activation x linear force-velocity (Vmax 50 L/s), lengthening enhancement up to 1.3; in-loop activation shape fitted to the three measured single-twitch points (tr 0.5-1.5 ms, td 3 ms), 100 Hz underfit", "inference (unmeasured): a muscle driven at 22 Hz would receive multi-pulse bursts per cycle rather than a single twitch", "S10 design frequency 21.9 Hz at R = 4 cm (CL 1.5, stroke 120 deg, AR 6, r2 = 0.55R)", "S10 hover model: Rankine-Froude, k = 1.2, full disc, M = 1.5, m = 0.4 g", "S10-D-D f = 0.0138-0.0276 (central 0.0164)", "challenge-77 forward-flight model as re-implemented: body frontal area 2.2e-5 m2, CD body 0.4, CD profile 0.05-0.2, CLmax 1.5, AR 6; flip thresholds 96.5 and 120.5 W/kg at upper f", "larval axial myotome as stand-in for adult pectoral muscle (inherited from the claim; adult cod and sculpin fast-muscle data at search-summary level only)"]}
```
