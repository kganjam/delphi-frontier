# Replication of claim 189: "S28 VERDICT NEGATIVE"

**Everything here is a calculation (status: derived), not a measurement.** No new data was collected.

## What I read, and what I did not read
- `docs/research/fish/S28-organism.md` (branch `origin/claude/s28-organism-design-5z0vjz`). I read **only the §1 inputs table** before I derived anything. **Disclosure:** that table already contains the author's back-solved wing area (196 mm²) and a "consistency flag" paragraph that states a speed deficit of 3.17–9.71×. So my speed-deficit figure is not blind to theirs. I did not read §0 or §2–§6 until my numbers below were fixed.
- I did not open `S28_organism.py`.

## Inputs
| Input | Value | Source | Read-level |
|---|---|---|---|
| Adult burst speed U_b | 0.45–1.38 m/s | Miln et al. 2021, as cited in S28 §1 | **could-not-access**. One web search (standard mode) did not find the paper. The value is taken from the project's input table and is not checked against the primary source |
| CL_max | 1.07 | project-derived, from S28 §1 | listing |
| Wing geometry | span = 1 SL, AR = 5 | project, from S28 §1 | listing |
| SL | 3.0 cm | assumed (S28 §1) | listing |
| Body mass m | 0.25 g (sensitivity case: 0.40 g) | assumed (S28 §1) | listing |
| g, ρ_air | 9.81 m s⁻², 1.225 kg m⁻³ | constants | — |

## Arithmetic (mine)
1. **Wing area.** Wing only, no body added: S = b²/AR = 0.03²/5 = **180 mm²**. The author uses 196 mm², back-solved from their V_to. This is a small disagreement about which area to use.
2. **Takeoff speed.** W/S = 0.25e-3·9.81/180e-6 = 13.6 N m⁻². V_to = √(2·13.6/(1.225·1.07)) = **4.56 m/s**. With the 0.40 g mass: W/S = 21.8 N m⁻², V_to = **5.77 m/s**.
3. **Speed deficit**, V_to/U_b:
   - 0.25 g: **3.3× to 10.1×**. The kinetic-energy deficit is **10.9× to 103×**.
   - 0.40 g: 4.2× to 12.8×.
   - With the author's V_to of 4.37 m/s: 3.17× to 9.71×.
   - In every case the burst is far below the takeoff speed, so **sustained flight or a glide from launch is impossible**.
4. **Wild-type ballistic leap** (vacuum ballistics, exit speed = burst speed, which is generous):
   - Range R = U²/g: **2.06 cm** at 0.45 m/s and **19.4 cm** at 1.38 m/s.
   - Vertical height h = U²/2g: 1.03 cm and 9.71 cm.
5. **Upper bound on lift from the wing during the leap**, at 1.38 m/s and CL_max:
   - At launch: L = ½·1.225·1.38²·180e-6·1.07 = 2.25e-4 N. Weight W = 2.45e-3 N, so L/W = **9.2 %**.
   - Over a 45° vacuum arc, the time-average of V² is (2/3)V². So the arc-averaged L/W is at most **≈ 6 %**.
   - Treating that 6 % as a reduction in effective g, and ignoring wing drag, gives a range gain of **at most ≈ +6 %**. That is about 19.4 → 20.6 cm.
   - This is an **upper bound**, not a simulation. Real gains are lower, because wing drag and operation below CL_max both reduce them.
6. **Exit speed needed for a 3× longer leap:** √3·1.38 = **2.39 m/s**, which is 1.73× the measured maximum.

**My value:** the verdict is NEGATIVE. The design cannot fly or glide: V_to is 3.3–10× the burst speed (0.25 g, 180 mm²). The wild-type leap is ≤ 19.4 cm. The wing extends it by **at most ~+6 % (upper bound)**. A 3× leap would need 2.39 m/s.

## Comparison with the recorded value (read after deriving)
S28 §0 claims: cannot fly, glide or skim. Wing lift is 2–3 % of body weight averaged over the arc. The best leap goes from 19.4 cm to 19.8–20.0 cm (+1.5 % to +3 %). A 3× leap needs 2.39 m/s.

- **AGREE:** the negative verdict, the 19.4 cm baseline and the 2.39 m/s figure. I re-derived all three exactly.
- **CANNOT TELL independently:** the precise +1.5–3 % and the 2–3 % lift fraction. My bound (≤ ~6 % lift, ≤ ~+6 % range) contains their figures. Their lower numbers depend on wing drag, the operating CL and launch-angle optimisation, which I did not simulate.
- **Minor disagreement, preserved:** wing area. I used 180 mm² (wing only); the author back-solved 196 mm². This changes V_to by about 4 % and does not affect the verdict.
- **Not independent:** the speed-deficit figure. I saw the author's version in the inputs table before computing mine.

```swarm-replication
{"claim_id": 189, "my_value": "NEGATIVE: V_to 4.56 m/s vs burst 0.45-1.38 m/s (3.3-10.1x deficit); wild-type leap 19.4 cm; wing gain <= ~+6% (upper bound); 3x leap needs 2.39 m/s", "agrees": true,
  "note": "Re-derived the negative verdict, the 19.4 cm baseline and the 2.39 m/s requirement exactly; their +1.5-3% gain lies inside my <=6% upper bound but I did not simulate it, and the burst speeds are not verified against Miln 2021 (could not access)."}
```
