# Challenge 191: the ballistic-leap gain from the designed pectoral "wing"

**Claim under review (not written by me):** "At the measured maximum burst of 1.38 m/s the ballistic leap is 19.4 cm and the wing
lengthens it by only +1.5 to +3.0% (3-6 mm); at 0.45 m/s the gain is ~0%."
Recorded level: derived. Value: 3 percent range gain. Source: `docs/research/fish/S28-organism.md` on branch
`origin/claude/s28-organism-design-5z0vjz` (read-level: **full-text**, together with its script `S28_organism.py`, which I re-ran).

**Verdict: WEAKENED.** The arithmetic reproduces. The qualitative conclusion (the gain is a few millimetres, far from a "3× leap")
survives every relaxation I tried. But the quoted **bracket "+1.5 to +3.0 %" is mislabelled at both ends.**
- The lower end leaves out the author's own case A, which gives +0.7 %. The author calls case A the closest to what the allele is known to do.
- The upper end, "+3.0 %", is called "zero wing drag". It is actually zero *profile* drag, with induced drag still charged.
  A wing with no drag at all, or one with a higher (unsteady) CL, reaches about +3.7 to +3.9 % (≈ 7 mm).

**Everything below is calculation, not observation.** My independent script is
`docs/research/fish/challenge-191-scripts/c191.py`. It uses RK4 and a ½° launch-angle grid, and it is written separately from
`S28_organism.py`.

## 1. Independent arithmetic

| Quantity | Mine (calculated) | Claim | Match |
|---|---|---|---|
| Vacuum range V²/g at 1.38 m/s | 1.9044 / 9.81 = 0.19413 m = **19.41 cm** | 19.4 cm | yes |
| Same, with body drag (CD 0.3, 24 mm²) | **19.36 cm** | 19.36 cm | yes |
| Vacuum range at 0.45 m/s | **2.06 cm** | 2.06 cm | yes |
| Case C (192 mm², AR 5, CD0 0.08, CL 1.07) at 1.38 m/s | 19.818 cm, **+2.36 %** (+4.6 mm) | +2.4 % | yes |
| Case C, CD0 0.20 | **+1.45 %** (+2.8 mm) | +1.5 % | yes |
| Case B (125 mm²) | **+1.49 %** (+2.9 mm) | +1.5 % | yes |
| Case A (57 mm², length-only fin) | **+0.74 %** (+1.4 mm) | +0.7 % in S28 §3.2 table; **omitted from the claim** | number yes, framing no |
| 0.45 m/s, all cases | **+0.08 to +0.24 %** (≤ 0.05 mm) | "~0 %" | yes |
| "+3.0 % upper bound" (author: CD0 = 0, induced drag kept, AR 5) | the author's script prints 1.0298 | +3.0 % | yes, but see §3 |
| Truly drag-free wing (CD0 = 0, no induced drag) | **+3.69 %** (+7.2 mm) | not computed | **new** |

## 2. Proxy check
- **Burst swimming speed stands in for water-exit speed.** The author flags this and argues it is generous: breaking the
  surface costs speed. I agree with the direction. It is the input that dominates, because range ∝ V² and the lift fraction ∝ V².
- **Range is the horizontal distance of a point mass from surface to surface.** For a 3 cm fish this ignores where the
  centre of mass sits at exit and at re-entry. That offset is of order body length, so it affects WT and winged leaps
  equally and cancels in the *gain*. It does not cancel in the absolute 19.4 cm.
- I found no proxy substitution beyond the one the author already declares.

## 3. Hidden assumptions, relaxed (all calculated)

| Relaxation (case C, 1.38 m/s unless noted) | Gain |
|---|---|
| Truly zero wing drag (profile *and* induced) | **+3.69 %** |
| Unsteady / leading-edge-vortex CL = 2.0 throughout, CD0 0.08, induced drag charged | **+3.86 %** (+7.5 mm) |
| Fin feathered on the ascent (CL 0 up, 1.07 down) | +1.17 % (CD0 .08) … +0.27 % (case A) |
| CL 0 up, 2.0 down | +2.65 % |
| Mass 0.40 g instead of the back-solved 0.25 g | +1.47 % |

**Inference (mine):** the gain scales roughly as CL·S/m. No plausible relaxation of the stated inputs pushes it past about 4 %
(≈ 8 mm). So the "only a few millimetres" conclusion is robust. The specific "3.0 %" is not a bound. The specific "1.5 %" is
not the realistic floor. The *measured* fin area is unknown in every case (S28 says so), so the true value is anywhere from
about 0.3 % to about 3.9 %. Where it falls depends on an unmeasured S and CL.

**An error in the prose, not the numbers.** S28 §3.2 says "lift is perpendicular to the path, so on the way down part of it
points *backwards*." This is reversed. Lift = L·(−u_y, u_x), the sign used in both scripts. It tilts **backwards on the ascent**
and **forwards on the descent** (sign check in `c191.py` step 5). The integration is correct, so no number changes. The
mechanistic explanation in the source is wrong.

## 4. Evidence level
- "derived" is honest. S28 labels every trajectory number as calculation.
- **One defect:** the claim calls 1.38 m/s "the measured maximum burst", citing Miln et al. 2021 (n = 50).
  - I tried one web search ("Miln 2021 zebrafish adult burst swimming speed high-speed video"). It did **not** locate this paper.
    The closest hit was a 2021 adult-zebrafish swim-endurance methods paper (PubMed 34842242), read-level **search-summary**,
    which does not show the author list or a burst speed.
  - So the "measured" status of 0.45–1.38 m/s is **unverified by me** (scope: one standard web search; no full text accessed).
  - It is not refuted. It is the input the verdict rests on most.
- The recorded value "3 percent range gain" is the author's zero-profile-drag ceiling presented as a single value. A reader
  will take it as the expected gain. The central case-C estimate is 2.4 %, and the realistic-allele estimate is 0.7 %.

## 5. Regimes and counter-examples
- **Ground effect** near the water on the descent would raise the effective lift slightly. I did not model it. It acts only in
  the last few millimetres of height, so I expect it to be small (inference, not computed).
- **Flapping pectorals in air**, as in hatchetfishes, are excluded by design: no muscle allele. I did not search for a
  published zebrafish leap-with-spread-fins observation. S28 states that none is known; I have not confirmed this.
- I found no counter-example that overturns the negative.

## 6. Corrected statement
At an exit speed equal to the 1.38 m/s burst (an assumption), the ballistic leap is 19.4 cm (calculated). With an unmeasured
fin of 57–192 mm² at fixed CL 1.07, the wing lengthens it by **+0.7 % to +2.4 %** (1.4–4.6 mm, calculated). Relaxed bounds
(no drag, or CL 2) reach **≈ +3.7–3.9 %** (≈ 7 mm). At 0.45 m/s the gain is +0.1 to +0.4 % (≈ 0).

```swarm-challenge
{"claim_id": 191, "outcome": "weakened", "reason": "Arithmetic and the negative conclusion reproduce, but the quoted +1.5 to +3.0% bracket omits the author's own length-only case (+0.7%) and its '+3.0% upper bound' keeps induced drag; a truly drag-free or CL=2 wing gives +3.7 to +3.9% (~7 mm), and the descent-lift direction in the source prose is reversed.",
  "corrected_value": "+0.7 to +2.4% (1.4-4.6 mm) at fixed CL 1.07 for S=57-192 mm2; relaxed ceiling ~+3.9% (~7.5 mm) at 1.38 m/s; +0.1 to +0.4% at 0.45 m/s",
  "depends_on": ["Miln2021-burst 0.45-1.38 m/s (unverified, cited as measured)", "exit speed = burst speed (assumed)", "body mass 0.25 g (back-solved)", "fin area 57-192 mm2 (unmeasured, S28 cases A-C)", "CL 1.07 quasi-steady (project-derived)", "CD0 0.08-0.20, Oswald e 0.8 (assumed)", "body drag CD 0.3 on 24 mm2 (assumed)"]}
```
