# Replicate 3: speed and kinetic-energy deficit for a zebrafish with a 1-BL wing

**Status:** desk calculation. Nothing was measured or simulated. Every deficit number below is
**calculated** from the inputs listed. None is an observation.

**Claim being checked (claim_id 3):** for the "1-BL wing case", the speed deficit and the
kinetic-energy deficit of a gliding zebrafish. The source is `zebrafish-glide-physics.md`.

## Procedure and independence

- I first derived the value from my own inputs and model.
- Only after that did I open the recorded working, on branch
  `origin/claude/zebrafish-glide-physics-j176og`, files `docs/research/fish/zebrafish-glide-physics.md`
  and `zebrafish_glide_calc.py`.
- When I located those files, I listed their names but did not read them until my own numbers
  existed (next section).
- The task prompt itself states 10.4x and 109x in the question line. So my derivation was not
  blind to the target numbers. It was only blind to the recorded inputs and method.

## My model (my framing, chosen before reading the recorded working)

Deficit = (airspeed needed for steady glide on a wing of span 1 BL) / (best measured sustained
swimming speed). Kinetic-energy deficit = (speed deficit)², because KE = ½mv² at fixed mass.

Lift equals weight in a shallow steady glide:

    V_req = sqrt( 2·m·g / (ρ_air · S · C_L) ),   with S = b²/AR and b = 1 BL.

### Inputs

| Input | Value used | Source | Read-level |
|---|---|---|---|
| U_crit, adult zebrafish | 0.549 m/s = 18.0 SL/s (n = 10) | Palstra et al. 2010, PLoS ONE, as quoted in a search result | search-summary (doaj.org fetch blocked by the network policy) |
| U_crit, alternative | 0.560 m/s = 15.5 SL/s, attributed to Plaut | same PLoS ONE paper, citing Plaut | search-summary, secondary |
| Body length L | 0.549 / 18.0 = **3.05 cm SL** | my inference from the Palstra pair above | derived |
| Mass m | **0.4 g** (bracket 0.3–0.53 g) | BioNumbers 102573 gives 0.18–0.73 g (citing Chizinski et al. 2008). FishBase length–weight relation a = 0.00977, b = 3.04 (TL in cm): my calculation gives 3.5 cm TL ≈ 0.4 g and 3.7 cm TL ≈ 0.53 g | search-summary for both |
| ρ_air | 1.204 kg/m³ (20 °C, sea level) | standard value | n/a |
| g | 9.81 m/s² | standard | n/a |
| Aspect ratio AR | **3** central (bracket 2–5) | my assumption: a broad membrane fin | assumption |
| C_L | **1.0** central (bracket 0.8–1.2) | my assumption for a cambered plate at Re ~ 10³–10⁴. No source was retrieved | assumption |
| Adult fast-start (burst) peak speed | **unknown** | One search, plus a fetch of PMC8025299 (an adult escape study): the text and captions report no value. Search scope: one web search and one full-text fetch | full-text (PMC8025299), no number present |

Because burst speed is unknown, the denominator is U_crit. That makes the deficit an
**upper-side** figure. A real burst speed would be higher than U_crit and would shrink the deficit.

### Arithmetic (central case)

- b = L = 0.0305 m, so S = b²/3 = 9.30e-4/3 = 3.10e-4 m² = 3.10 cm².
- W = 4.0e-4 × 9.81 = 3.924e-3 N, so wing loading W/S = 12.7 N/m².
- V_req = sqrt(2 × 3.924e-3 / (1.204 × 3.10e-4 × 1.0)) = sqrt(7.848e-3 / 3.732e-4) =
  sqrt(21.03) = **4.59 m/s**.
- Speed deficit = 4.59 / 0.549 = **8.4x**.
- KE deficit = 8.4² = **70x**.

### Sensitivity (all calculated)

Over m ∈ {0.30, 0.40, 0.53} g, AR ∈ {2, 3, 5}, C_L ∈ {0.8, 1.0, 1.2}, with L = 3.05 cm and
U_crit = 0.549 m/s: the speed deficit runs from **5.4x to 13.9x**, and the KE deficit from
**29x to 193x**. Changing C_L to 0.6 with AR 5 gives 13.9x and 194x.

**My value: speed deficit ≈ 8x (range 5–14x). KE deficit ≈ 70x (range 30–190x).** Both are
calculated, both are against U_crit, and both are dominated by the assumed C_L and AR, not by
the fish data.

## Comparison with the recorded value (read after the derivation above)

From the recorded working, its stated inputs:

- m = 0.4 g and L = 4 cm SL, both "given in brief".
- ρ = 1.2 kg/m³.
- 1-BL span at AR 5, so S = 3.2 cm².
- C_L = 0.6, justified as a Laitone (1997) steady-wing value at Re ≈ 2×10⁴, read at
  search-summary level.
- Denominator 0.56 m/s, the Plaut value via a secondary source.

I re-ran that arithmetic independently:

- V = sqrt(2 × 3.924e-3 / (1.2 × 3.2e-4 × 0.6)) = sqrt(34.06) = 5.836 m/s.
- 5.836 / 0.56 = **10.42x**.
- 10.42² = **108.6 ≈ 109x**.

So the arithmetic is internally consistent. 109 is the square of the unrounded 10.42, not of
10.4, which would give 108.2. That difference is only rounding.

Where the derivations differ, both on inputs:

1. **C_L: 0.6 recorded, 1.0 mine.** The recorded choice is more conservative and is supported by
   its one retrieved steady-wing value. Mine is an unsourced assumption. I do not claim mine is
   better. This one input alone moves the speed deficit by a factor of sqrt(1/0.6) = 1.29.
2. **AR 5 recorded, 3 mine.** A higher AR means a smaller wing for the same span, so a higher
   required speed.
3. **L = 4 cm recorded, 3.05 cm mine.** A longer L gives a bigger 1-BL wing, so a lower required
   speed. Note that the recorded denominator, 0.56 m/s, belongs to a fish of about 3.6 cm SL by
   the recorded working's own cross-check. That is a mild mismatch with the 4 cm wing; it makes
   the wing bigger than that fish's own 1 BL and slightly understates the deficit.

With the recorded inputs, I reproduce 10.4x and 109x exactly. With my inputs, I get 8.4x and
70x. The recorded value lies inside my calculated bracket of 5.4–13.9x and 29–193x. The two
central values differ by about 25% in speed and about 55% in energy, and the difference is
entirely assumption-driven, from C_L and AR.

**Verdict: CANNOT TELL** as to the physical claim. Separately, I **AGREE** with the
arithmetic. Both derivations agree on the qualitative conclusion: the required launch speed is
roughly an order of magnitude above measured sustained swimming speed, and roughly two orders of
magnitude in kinetic energy. Neither derivation has a measured adult burst speed, so both are
upper-side estimates.

## Sources

- Palstra et al. 2010, PLoS ONE, zebrafish U_crit. Read-level: search-summary (doaj.org fetch blocked).
- Plaut U_crit 0.560 m/s, via the same paper. Read-level: search-summary, secondary.
- BioNumbers 102573, zebrafish mass range: https://bionumbers.hms.harvard.edu/bionumber.aspx?id=102573. Read-level: search-summary.
- FishBase, Danio rerio length–weight relation: https://www.fishbase.se/summary/4653. Read-level: search-summary.
- PMC8025299, adult zebrafish escape study: https://pmc.ncbi.nlm.nih.gov/articles/PMC8025299. Read-level: full-text via fetch tool. It contains no adult peak-speed number.
- Park & Choi 2010, J. Exp. Biol. 213:3269, flying fish. Read-level: search-summary. Not used numerically.

```swarm-replication
{"claim_id": 3, "my_value": "speed deficit ~8.4x (calculated range 5.4-13.9x); KE deficit ~70x (range 29-193x), vs Ucrit 0.549 m/s", "agrees": null,
  "note": "Recorded 10.4x/109x is reproduced exactly from its own inputs (CL 0.6, AR 5, L 4 cm, 0.56 m/s) and sits inside my bracket, but my independent central differs by ~25% in speed because the result is set by assumed CL and AR, not by measured data."}
```
