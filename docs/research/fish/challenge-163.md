# Challenge 163: adversarial review of S21-D-D (fast-start sensitivity)

Written 2026-11-04 · Reviewer: adversarial challenger (I did not write the claim)

**Claim under review (author's words, `harvest:deepen-s21-sensitive-input-mxp5t8`):**
"The input the S21-D conclusion is most sensitive to is the fastest adult's fast-start speed (unit
elasticity; no single 2x error in any input flips the conclusion, a ~3.2x error in this one would);
a simulation bounds the 120 fps max-of-4 reading at 0.88-1.40x of the true peak, ruling out S21-D's
hypothetical 2x under-read and giving a true peak of ~0.99-1.58 m/s; against the corrected 4.37 m/s
stall threshold the margin is ~2.7-4.8x (typical fish ~5x)… VERDICT: stands."
Recorded evidence level: **measured**.

Source read: `docs/research/fish/S21-D-deepen.md` and `S21-D-deepen-sim.py` on branch
`origin/claude/deepen-s21-sensitive-input-mxp5t8` (read-level: full-text, repo).

> **Outcome: WEAKENED.**
>
> - **What survives:** the sensitivity ranking, the arithmetic, and the qualitative conclusion that
>   the gap is not closed.
> - **What fails:** the claim that "a simulation … rules out S21-D's hypothetical 2x under-read", and
>   the bias band 0.88–1.40× built on it.
>   - The simulation hard-codes forward two-frame differencing. Miln et al. do not state how they
>     differentiated their fast-start positions.
>   - Under central differencing, which I believe (unverified) is Tracker's default, the same model
>     gives a 1.5× under-read at the author's shortest rise time.
>   - The band also mixes a mean on one side with a 95th percentile on the other.
> - **Corrected values (calculated from a simulation, not observed):**
>   - true peak of the fastest fish ≈ 0.99–2.1 m/s;
>   - margin to the 4.37 m/s stall speed ≈ 2.1–4.4×, or ≈ 2.0–4.8× across the 4.22–4.77 m/s band.
> - **Evidence label:** the key number is derived (a digitised reading divided by a simulated bias),
>   not measured.

---

## 1. Arithmetic, redone independently

All values below are **calculated** by me from the stated inputs: m = 0.4 g, g = 9.81, ρ = 1.2 kg/m³,
S = 3.2×10⁻⁴ m².

- **Stall speed.** V_s = √(2mg/(ρ S C_L)), and 2mg/(ρS) = 7.848×10⁻³ / 3.84×10⁻⁴ = 20.44 m²/s².
  - C_L 0.6 → 5.84 m/s
  - C_L 1.07 → 4.37 m/s
  - C_L 1.15 → 4.22 m/s
  - C_L 0.9 → 4.77 m/s
  - All four match the author.
- **Central margin.** M = 4.37/1.38 = 3.17, which matches.
- **Flip factors.** A U_fast error of ×3.17 flips the conclusion. Each square-root input needs
  M² = 10.0×. Both match.
- **Bias band → true peak.** 1.38/0.875 = 1.58 m/s and 1.38/1.40 = 0.986 m/s.
- **Margins.** 4.22/1.58 = 2.67 and 4.77/0.986 = 4.84. Both match.
- **Typical fish.** 4.37/0.84 = 5.2, which matches.
- **Upstream check.** S21's 0.84 m/s uses ν = 1.0×10⁻⁶ m²/s. That is consistent with the authors'
  stated "1 mPa s water" (S21-behaviour.md line 48; read-level full-text, repo).

**I find no arithmetic error.** The sensitivity ranking (U_fast has elasticity −1; every threshold
input has ±½) follows from the functional form and is correct.

## 2. Proxy check

- **The quantity that matters for take-off is the speed at water exit, in air.**
  - The claim uses in-water peak burst speed instead. The author flags this.
  - Exit speed should be at or below the in-water peak, so the proxy biases toward closing the gap.
  - This is my inference. It makes "gap not closed" conservative and does not hurt the claim.
- **The tracked point is not a true centre of mass.** Miln et al. track a fixed body point at
  0.35 BL from the snout, which they call the "centre of mass".
  - Quote from Miln et al. 2021: "using the fish centre of mass as the tracking point. Centre of mass
    was defined as the location at 0.35 body lengths from the tip to the snout". Read-level:
    full-text, Europe PMC XML PMC8025299, fetched this session.
  - During the C-bend, a body-fixed point near the head can move faster than the true COM (my
    inference).
  - That again inflates the reading and works in the claim's favour.
- **The stall threshold is quasi-steady.** A transient dynamic-stall C_L of about 2–3 would lower V_s
  to about 2.6–3.2 m/s (calculated).
  - That still leaves M > 1 at U = 1.38–2.1 m/s.
  - Closing the gap at U = 1.58 m/s needs C_L ≈ 8.2 (calculated).

**No proxy breaks the claim.**

## 3. The hidden assumption that carries the "rules out 2×" sentence: the differencing scheme

The author's script (`S21-D-deepen-sim.py`) computes speed as `np.diff(xs)/dt`. That is a forward
difference over **one** frame interval (8.3 ms at 120 fps).

**What Miln et al. actually state** (read-level full-text, PMC8025299, fetched this session):

- For **fast starts**: "four escape responses were analysed for each fish and the fastest speed was
  used". They give no differencing method.
- For the separate **realized** speed, they do state one: "the maximum speed calculated across two
  video frames".
- **The fast-start differencing scheme is therefore `unknown`.**
- Tracker, the software they used, computes velocity by central finite difference,
  v_i = (x_{i+1} − x_{i−1})/(2Δt), as I recall from its documentation.
  - Read-level for that statement: **could-not-access**. physlets.org was refused by this session's
    proxy, so treat it as unverified.
  - A central difference spans 16.7 ms at 120 fps, twice the author's window.

**Relaxed-assumption rerun.** I kept the author's alpha pulse and noise model and added central
differencing.

- Script: `docs/research/fish/challenge-163-sim.py`, seed 163, 1500 replicates, max of 4 trials,
  120 fps.
- **Everything in this table is a simulation, not an observation.**
- Each cell gives the ratio of measured to true peak as mean [p5–p95].

| Profile, scheme | t_p 3 ms (outside author's range) | t_p 5 ms | t_p 10 ms | t_p 20 ms |
|---|---|---|---|---|
| alpha, forward, σ 0 | 0.69 | 0.88 [0.82–0.90] | 0.97 | 0.99 |
| alpha, forward, σ 1 mm | 0.77 | 1.00 | 1.15 | 1.23 [1.09–1.41] |
| alpha, **central**, σ 0 | 0.42 | **0.67 [0.58–0.70]** | 0.89 | 0.97 |
| alpha, central, σ 1 mm | 0.45 | 0.71 | 0.97 | 1.07 [1.00–1.17] |
| alpha, forward, σ 2 mm | 1.03 | 1.20 | 1.39 | 1.53 [1.28–1.86] |

**Checks on the author's own numbers:**

- My forward-difference rows reproduce the author's table within ~0.01, for example 0.877 vs 0.875
  and 1.232 vs 1.232. The author's simulation is implemented as described.
- **The band is asymmetric.**
  - The lower edge (0.875) is a mean.
  - The upper edge (1.40) is a 95th percentile.
  - Under the author's own forward scheme, the matching 5th percentile at t_p = 5 ms, σ = 0 is 0.82.
    That gives a true peak of up to 1.69 m/s, not 1.58 (calculated).

**What follows** (my inference, conditional on this model):

- With central differencing and the author's own shortest rise time (5 ms), 120 fps **under-reads by
  1.5×** on the mean and by up to 1.7× at the 5th percentile.
  - The true fastest-fish peak would then be **1.38/0.67 ≈ 2.06 m/s**, or up to 2.38 m/s at the 5th
    percentile (calculated).
- At t_p = 3 ms with central differencing, the under-read is 2.4×.
  - The claim's "rules out S21-D's hypothetical 2x under-read" therefore holds **only if** forward
    differencing was used **or** t_p ≥ ~4 ms.
  - Neither is established. The author also says the 5–20 ms rise-time range has no adult zebrafish
    source.
- **The 2× under-read is constrained by external data, not by the simulation.**
  - Danos & Lauder 2012 report a 1000 fps mean of per-sequence peaks of ≈0.84 m/s (S21 derivation,
    read-level full-text via S21; derived).
  - A true fastest-fish peak of ~2.8 m/s (2 × 1.38) would be ~3.3× that independent high-frame-rate
    mean.
  - I judge that implausible but not excluded. It is 1 fish of 50 against a mean of 5.
- I also ran a sharper two-stage Gaussian pulse with no coast, shown in the script output but not in
  the table. It produces larger under-reads, 0.34–0.80 under central differencing.
  - Real centre-of-mass speed coasts after stage 2, so I treat that profile as an unrealistic stress
    case, not as evidence.

## 4. Recomputed margin under the relaxed assumption

All entries are calculated. The true peak is the 1.38 m/s reading divided by the simulated ratio.

| Case | True peak U (m/s) | M at 4.22 | M at 4.37 | M at 4.77 |
|---|---|---|---|---|
| Author's upper bound (forward, mean) | 1.58 | 2.67 | 2.77 | 3.02 |
| Forward, 5th percentile | 1.69 | 2.50 | 2.59 | 2.82 |
| **Central, t_p 5 ms, mean** | **2.06** | **2.05** | **2.12** | 2.31 |
| Central, t_p 5 ms, 5th percentile | 2.38 | 1.77 | 1.84 | 2.00 |
| Central, t_p 3 ms, mean (outside the 5–20 ms range) | 3.29 | 1.28 | 1.33 | 1.45 |
| Author's lower bound (noise-inflated) | 0.99 | 4.28 | 4.43 | **4.84** |

- **The gap stays open in every row, including the stress row** (t_p 3 ms). So the author's
  qualitative verdict survives.
- **The lower edge of the margin drops from 2.7× to ≈2.0–2.1×.** In the tail it is ≈1.8×.
- **The flip distance shrinks.** The claim says a ~3.2× error in U_fast would flip the conclusion.
  - That is correct against the 1.38 m/s reading.
  - Against a plausible true peak of 2.06 m/s, the remaining factor is only ~2.1×.

## 5. Evidence level

- The claim is recorded as **measured**.
- Its key number, "true peak ~0.99–1.58 m/s", is a **derived** number: a re-digitised figure reading
  divided by a **simulated** bias band.
- Its margin, "2.7–4.8×", is **calculated**.
- The claim's own sentence does say "a simulation bounds…", and the author's swarm-result lists
  "measured + simulated + …". The *recorded* level of "measured" is still wrong for the key number.
- Correct label: **derived (a digitised measurement corrected by simulation; margin calculated)**.

## 6. Regimes and counter-examples looked for

- **Temperature.** Miln tested at 23 °C (full-text). The 28 °C husbandry standard would plausibly raise
  speed, but the magnitude is `unknown`. The author already flags this.
- **Fig. 1a structure.** I confirmed from the full-text legend that the x-axis is fast-start speed and
  colours mark day 1/4/7 realized speed.
  - The same fish therefore appears three times at one x value by construction.
  - That supports the author's reading. It is not evidence of a reproducible 1.38 m/s.
- **Other adult zebrafish peak data.** I did not repeat the author's Europe PMC search. My negative
  scope is limited to this session's attempts:
  - the Europe PMC full text of Miln et al. (fetched);
  - Tracker documentation (refused by the proxy).
  - **No published counter-example was found, but that search was minimal.**

## Sources

| Source | Read-level |
|---|---|
| S21-D-D write-up and simulation script, branch `claude/deepen-s21-sensitive-input-mxp5t8` | full-text (repo) |
| S21: `docs/research/fish/S21-behaviour.md`, branch `claude/zebrafish-fast-start-velocity-pxsv7e` | full-text (repo; grep of relevant lines) |
| Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146 (PMC8025299), methods and Fig. 1 legend | full-text (Europe PMC XML, fetched this session) |
| Tracker (Open Source Physics) velocity algorithm | could-not-access (physlets.org refused by proxy); my statement of its default is unverified recollection |
| Danos & Lauder 2012 (0.84 m/s via S21) | full-text via S21 (derived value) |

```swarm-challenge
{"claim_id": 163, "outcome": "weakened", "reason": "Arithmetic, sensitivity ranking and 'gap not closed' survive, but the bias band (and so 'rules out 2x under-read') rests on an unstated forward-difference assumption: with central differencing (plausibly Tracker's default; Miln do not state the scheme) the same simulation gives a ~1.5x under-read at t_p = 5 ms, the band mixes a mean with a p95, and the key number is derived, not measured.", "corrected_value": "fastest adult true peak ~0.99-2.1 m/s (simulated bias, either differencing scheme, t_p >= 5 ms; p5 tail to ~2.4 m/s); margin to 4.37 m/s stall speed ~2.1-4.4x (~2.0-4.8x over V_s 4.22-4.77 m/s; tail ~1.8x); evidence level derived, not measured", "depends_on": ["Miln, Ward & Seebacher 2021 (doi:10.1098/rsos.210146, PMC8025299) methods: 120 fps, Tracker, fastest of 4 escapes, differencing scheme for fast starts not stated (full-text)", "S21-D-D digitised fastest-fish reading 1.38 m/s from Miln Fig. 1a", "assumption: Tracker default velocity is central finite difference (unverified; physlets.org could-not-access)", "simulation assumptions: alpha-pulse COM speed profile, rise time 5-20 ms (3 ms stress case), Gaussian position noise 0-2 mm, max of 4 trials (challenge-163-sim.py, seed 163)", "replicate-24 corrected stall speed 4.37 m/s (band 4.22-4.77, C_L,max 1.15-0.9)", "stall speed law V_s = sqrt(2mg/(rho S C_L,max)) with m 0.4 g, S 3.2e-4 m^2, rho 1.2 kg/m^3", "Danos & Lauder 2012 mean per-sequence peak ~0.84 m/s at 1000 fps via S21 (derived), used as external plausibility check on a 2x under-read", "assumption: in-water burst speed is an upper proxy for water-exit speed"]}
```
