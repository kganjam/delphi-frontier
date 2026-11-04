# Challenge 132: adversarial review of S21-D-D-D (zebrafish true peak fast-start speed)

Written 2026-11-04 · Branch `claude/zebrafish-peak-speed-challenge-0bdllt` · Script:
`docs/research/fish/challenge-132-sim.py` (numpy, seed 132). **Every number from the script is calculated or
simulated, none is observed.**

**Claim under review** (S21-D-D-D, branch `claude/s21-d-d-sensitive-input-c6ylbu`, commit `ac961f1f`,
`docs/research/fish/S21-D-D-deepen.md` and `-sim.py`; read-level: full-text, repo):

> Hiding a stall-speed peak behind the 120 fps reading needs a ≤1.7 ms rise, ~600–860 g and ≥10,900 W/kg of
> muscle (≥23× the 461 W/kg traced ceiling). So the true peak is ≤~1.48 m/s (≤1.76 m/s even at an unverified
> 1200 W/kg), the gap stays open, and the remaining margin (~2.4–4.8×) is now set by C_L,max.
> Verdict: strengthens.

**My verdict: WEAKENED.** The qualitative conclusion survives every relaxation I tried: in no case is the
margin M ≤ 1, and the lowest margin I found is 1.55×. But the headline numbers hold only under two sampling
assumptions that the author did not state or test, and both are biased **toward** the author's conclusion.
Once they are relaxed:

- closing the gap needs a rise time as long as **4.2 ms**, not ≤1.7 ms;
- it needs as little as **~4,300 W/kg of muscle**, not ≥10,900. That is **≈9×** the 461 W/kg ceiling, not ≥23×;
- the power-bounded true peak can reach **~1.74 m/s** at 461 W/kg and **~2.3 m/s** at 1,200 W/kg.

## 1. Arithmetic, redone independently

I wrote a new simulation. It does not reuse the author's code: the alpha-pulse displacement is integrated
analytically, X(t) = V·t_p·e·[1 − (1+s)e^(−s)], rather than by `cumsum`, and the seed is different.

- **Power factor.** I solved max s(1−s)e^(2−2s) analytically. The maximum is at s = 1 − 1/√2, and the value
  is **0.8519**. This matches the author's 0.852.
- **Stall speed.** V_s = √(2mg/(ρ S C_L)), with m = 0.4 g, S = 3.2e-4 m² and ρ = 1.2 kg/m³. This gives
  **4.370 / 4.215 / 3.573 m/s** at C_L = 1.07 / 1.15 / 1.6. These match the author.
- **Base case.** I used the author's assumptions: forward 1-frame difference, 4 trials all at the same peak,
  and the mean reading. My results:
  - under-read r(t_p) of 0.190 at 1 ms, 0.340 at 1.5 ms, 0.878 at 5 ms;
  - closing requires t_p ≤ **1.42 ms** (850 g, 11,400 W/kg of body) at C_L 1.07, and t_p ≤ **1.65 ms**
    (601 g, **11,000 W/kg of muscle** at muscle fraction 0.6) at C_L 1.6;
  - the self-consistent maximum true peak is **1.41 / 1.49 m/s** at 461 W/kg and **1.54 / 1.77 m/s** at
    1,200 W/kg, for muscle fractions 0.3 / 0.6.

  **This reproduces the author's numbers to within Monte Carlo error. Their arithmetic is correct.**
- **Units.** "600–860 g" in the claim means gravitational acceleration units (5,900–8,400 m/s²), not grams
  of mass. Readers could take it as mass, so it should be written "g₀" or given in m/s².

## 2. Hidden assumptions that carry the numbers, tested relaxed (calculated / simulated)

| Sampling model | Rise time t_p needed to close (C_L 1.07 → 1.6) | Muscle power needed, at fraction 0.6 | Max true peak: 461 W/kg (mf 0.3–0.6) | Max true peak: 1,200 W/kg (mf 0.3–0.6) | Lowest M |
|---|---|---|---|---|---|
| Author: forward difference, 4 equal trials, mean reading | ≤1.42–1.65 ms | 19,000–11,000 W/kg | 1.41–1.49 m/s | 1.54–1.77 m/s | 2.02 |
| Forward difference, 5th-percentile reading | ≤2.32–2.59 ms | 11,700–7,000 | 1.43–1.53 | 1.59–1.90 | 1.88 |
| Forward difference, only 1 trial at V (other 3 at 0.8V) | ≤1.60–1.87 ms | 17,000–9,700 | 1.43–1.54 | 1.61–1.87 | 1.91 |
| **Tracker-style central difference**, 4 equal trials, mean | ≤2.37–2.80 ms | 11,500–6,500 | 1.48–1.63 | 1.72–2.06 | 1.73 |
| **Central difference, 1 trial at V, 5th percentile** | **≤3.61–4.17 ms** | **7,500–4,300** | **1.52–1.74** | **1.87–2.30** | **1.55** |

The three assumptions, and why each one matters:

1. **Which differencing estimator produced the 1.38 m/s?** This assumption carries the result.
   - The author's model is a 1-frame forward difference over an 8.3 ms window.
   - Miln et al. 2021 tracked the fish manually in **Tracker**. That is the author's full-text reading of
     Miln; I did not re-read Miln myself.
   - According to search results (read-level: **search-summary**), Tracker's built-in velocity is the
     average velocity over a **2-step interval** centred on the frame, i.e. (x₍ᵢ₊₁₎ − x₍ᵢ₋₁₎)/2Δt.
     That is a 16.7 ms window at 120 fps.
   - I could not read Tracker's help page itself: `opensourcephysics.github.io` does not resolve from this
     session (could-not-access).
   - Whether Miln exported Tracker's own velocity column or differentiated the positions themselves is
     `unknown`.
   - If they used Tracker's estimator, the under-read is roughly twice as deep at every t_p, and the bound
     loosens accordingly.
2. **Mean reading versus a plausible low reading.** The author asks whether the *average* max-of-4 reading
   equals 1.38 m/s. For a fastest-of-N fish, a lower-tail sampling phase is a legitimate way for a high true
   peak to read low. At the 5th percentile, the reading at t_p = 2 ms is 0.23V, against a mean of 0.48V.
3. **All 4 trials share the same true peak.** This is optimistic for the conclusion. If only the best trial
   reaches V, the other three trials add little chance of a well-phased frame.

**Inference (mine):** all three assumptions favour a tighter bound, i.e. the author's conclusion. Relaxed
together, the "≥23×" headline becomes **≥~9×** (4,300 vs 461 W/kg) and **≥~3.6×** against the unverified
1,200 W/kg. The power-bounded upper edge of U_true rises from ~1.48 m/s to **~1.74 m/s** (461 W/kg) and
**~2.3 m/s** (1,200 W/kg). Under C_L 1.6, the margin floor falls from 2.4× to **≈2.05×** (461 W/kg) and from
2.0× to **≈1.55×** (1,200 W/kg). M stays above 1 in every case.

## 3. Proxy check

- **The author's proxy.** Muscle mass-specific power ceilings from frog plantaris (461 W/kg, adjusted to
  28 °C) and quail. Neither is fish white muscle, and Miln's fish were at 23 °C. The author discloses this.
  The muscle fraction of 0.3–0.6 is also assumed and has no source.
- **The quantity that actually matters.** The achievable peak centre-of-mass acceleration (and jerk) of an
  adult small teleost. It constrains the rise time directly, without any proxy for muscle fraction or
  efficiency.
  - Search results (read-level: **search-summary**) put measured maximum fast-start accelerations at about
    23–40 m/s² for angelfish (Domenici & Blake 1993, Can J Zool) and roughly 40–50 m/s² for pike
    (Harper & Blake).
  - I did not read those papers. Film-based values are known to under-estimate maximum acceleration; the
    title "On the error involved in high-speed film when used to evaluate maximum accelerations of fish" is
    a listing-level hit and I did not read it. So the true ceiling may be higher; by how much is `unknown`.
  - **Even a cap 10× above these values (~500 m/s², ~50 g₀) is far below the 237–850 g₀ the
    gap-closing pulse needs.** That holds in every row of the §2 table.
  - Under the alpha-pulse shape, a ≤500 m/s² cap at V ≈ 1.5 m/s forces t_p ≥ e·V/a ≈ 8 ms. At that rise
    time r ≥ ~0.72, even with the worst-case central difference at the 5th percentile, so U_true ≲ 1.9 m/s.
- **Inference (mine):** the acceleration route independently backs the qualitative conclusion "the gap stays
  open". It does not rescue the author's specific numbers, because the measured acceleration ceiling is
  itself only search-summary and film-biased.
- **Shape caveat**, also flagged by the author. An alpha pulse starts at its maximum acceleration (e·V/t_p
  at t = 0). That is unphysical, and it inflates the acceleration figures relative to a smooth onset. I did
  not test other pulse shapes.

## 4. Evidence level

- The claim was recorded at evidence level **"measured"**. That is **not honest for the claim's content**.
  - Every quantitative element of it is a calculation or simulation: t_p ≤ 1.4–1.7 ms, 600–860 g, ≥10,900
    W/kg, U_true ≤ 1.48 m/s, and the 2.4–4.8× margin.
  - These rest on an assumed pulse shape, an assumed muscle fraction, and unverified or non-fish power
    ceilings.
  - The only measured input is the 1.38 m/s reading from Miln Fig. 1a, which S21-D-D digitised.
- The author's own `swarm-result` labels the evidence correctly as "calculated + simulated bound … on a
  measured input". The ledger's "measured" tag should be corrected to **calculated/simulated**.

## 5. Counter-examples and regimes missed

- **Searched:** no published adult zebrafish time-to-peak COM speed was found. Scope: one standard web search
  on fast-start accelerations, plus the author's documented Europe PMC search. Danos & Lauder 2012 Table 1
  remains could-not-access.
- **Not found (scope: the same searches):** any fish white-muscle power above ~1,000 W/kg. That is short of
  the ≥4,300 W/kg needed even in my most permissive row, so I found no counter-example that flips the
  verdict.
- **Not tested:**
  - tracking noise (the author argues it biases upward; I did not re-check that);
  - lateral motion of the 0.35 BL tracking point, which would inflate the reading and so make the claim
    conservative;
  - non-alpha pulse shapes.

## Sources

| Source | Read-level |
|---|---|
| S21-D-D-D doc and script, commit `ac961f1f` | full-text (repo) |
| Miln, Ward & Seebacher 2021 (Tracker, 120 fps), as relayed by S21-D-D-D | not re-read by me (relayed full-text) |
| Tracker help, Point Mass page (opensourcephysics.github.io) | could-not-access; method relayed at search-summary |
| Domenici & Blake 1993 Can J Zool (angelfish 22.7–39.5 m/s²); Harper & Blake (pike ~40–50 m/s²) | search-summary |
| "On the error involved in high-speed film when used to evaluate maximum accelerations of fish" | listing |
| Domenici & Blake 1997 J Exp Biol 200:1165 | listing |

```swarm-challenge
{"claim_id": 132, "outcome": "weakened", "reason": "Arithmetic reproduces exactly and no relaxation flips the gap (min M 1.55), but the headline numbers depend on unstated sampling assumptions (1-frame forward difference although Miln used Tracker, whose velocity is a 2-step central average; mean rather than low-quantile reading; all 4 trials at equal peak) whose relaxation loosens closing requirements to t_p <= ~4.2 ms and ~4,300 W/kg muscle (~9x not >=23x) and raises the power-bounded true peak to ~1.74 m/s (461 W/kg) / ~2.3 m/s (1200 W/kg), and the 'measured' evidence tag is wrong for a calculated/simulated bound.", "corrected_value": "fastest adult zebrafish true peak <= ~1.41-1.74 m/s at 461 W/kg muscle (<= ~2.3 m/s at 1200 W/kg), calculated; closing the gap requires t_p <= ~1.4-4.2 ms and >= ~4,300 W/kg muscle (>= ~9x the 461 W/kg ceiling); margin floor ~1.55-2.05x at C_L,max 1.6", "depends_on": ["Miln et al. 2021 fastest-fish reading 1.38 m/s at 120 fps, max of 4 trials (as digitised by S21-D-D)", "Tracker velocity = 2-step centred average (search-summary; Tracker help could-not-access); whether Miln used it is unknown", "alpha-pulse speed profile v=V(t/tp)exp(1-t/tp)", "power demand = peak COM KE rate 0.852 V^2/t_p, no added mass or drag", "muscle fraction 0.3-0.6 (assumed, no source)", "muscle power ceilings 461 W/kg (law library, Marsh 2022) and 1200 W/kg (unverified)", "V_s = sqrt(2mg/(rho S C_L,max)) with m=0.4 g, S=3.2e-4 m^2, rho=1.2, C_L,max 1.07-1.6", "fish fast-start accelerations ~23-50 m/s^2 (Domenici & Blake 1993; Harper & Blake; search-summary) as independent corroboration only"]}
```
