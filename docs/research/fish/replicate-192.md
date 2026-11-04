# Replication of claim 192: exit speed needed for a 3× leap, and flight speed

**Question (answer removed):** "A 3x leap would require a 2.39 m/s exit, 1.73x the measured maximum. Flight requires 4.37 m/s."
**Input location given:** S28-organism.md

## Blindness disclosure (read first)

This re-derivation was **not blind**. S28-organism.md is not on `main`. I found it on branch
`origin/claude/s28-organism-design-5z0vjz` (`docs/research/fish/S28-organism.md`). To locate the inputs I ran a
keyword grep (`leap|exit|m/s|...`) over that file, and the output showed the original author's working along with
the inputs, including lines 15, 29, 31, 92 and 109–112. I stopped reading the file after that grep and did not open
`S28_organism.py`. The arithmetic below is my own, but I knew the recorded figures before I did it.
Treat this as an **arithmetic check, not an independent derivation**.

## Inputs

| Input | Value | Kind | Source | Read-level |
|---|---|---|---|---|
| Max adult burst speed U_max | 1.38 m/s (range 0.45–1.38) | the author's claim, attributed to measurement | S28-organism.md table, citing "Miln et al. 2021, n = 50, high-speed video" | S28: listing (grep lines). Miln et al. 2021: **could-not-access**. Two web searches ("Miln 2021 zebrafish adult burst swimming speed", "Miln Wilson 2021 zebrafish burst swimming speed n = 50") did not find the paper. **I cannot verify 1.38 m/s.** |
| g | 9.81 m s⁻² | constant | standard | n/a |
| Exit speed = burst speed | assumption | **assumed** by S28 | S28 §3.1 says this is generous, because a swimming burst speed is not a water-exit speed | listing |
| Takeoff (flight) speed V_to | 4.37 m/s | **derived (project)**, not measured | S28 table: 1-BL span, AR 5, CL_max 1.07 | listing |
| Body mass m | 0.25 g | **assumed and back-solved** so that V_to = 4.37 m/s | S28 table | listing |
| Air density ρ | 1.225 kg m⁻³ | constant | standard sea level | n/a |

An unrelated data point turned up in the search, for scale only. Adult zebrafish U_crit is 0.548 ± 0.007 m/s, n = 10 (Palstra et al. 2010, PLoS ONE). Read-level: search-summary. It is a sustained speed, not a burst speed, so it does not test the 1.38 m/s value.

## Arithmetic (calculated, not observed)

**3× leap.** A drag-free ballistic range is R = V² sin2θ / g, so R ∝ V² at a fixed angle.
- R(1.38 m/s, 45°) = 1.38² / 9.81 = 1.9044 / 9.81 = **0.1941 m (19.4 cm)**. This is calculated.
- 3R needs V₃ = 1.38 × √3 = 1.38 × 1.73205 = **2.390 m/s**. This is calculated.
- Ratio to the claimed measured maximum: V₃ / U_max = √3 = **1.732×**. This is calculated. The ratio is exactly √3 and does not depend on the value of U_max.

Body drag lowers the range, so including it would raise the required speed a little. A drag-free 2.39 m/s is therefore a
**lower bound**. This is my inference.

**Flight speed.** Steady flight needs L = W, which gives V_to = √(2mg / (ρ S C_L)). I took span = 1 BL. My inference that BL = 30 mm comes from S28's own "13.5 mm = 0.45 SL".

| m (assumed) | S | V_to (calculated) |
|---|---|---|
| 0.25 g | 180 mm² (= 30²/5, AR 5 from span) | 4.56 m/s |
| 0.25 g | 192 mm² (S28 case C area) | 4.41 m/s |
| 0.40 g | 180 mm² | 5.77 m/s |
| 0.40 g | 192 mm² | 5.58 m/s |

I **cannot independently reproduce 4.37 m/s**. That value comes from a mass back-solved to fit it, so any check against
it is circular. Plausible inputs give **4.4–5.8 m/s**. The flight-speed figure is therefore model-dependent, and 4.37 m/s sits at
the low end of that range. This is my inference. The conclusion is qualitative, and it does not change anywhere in that range: 4.37 / 1.38 = 3.17× in speed and 10.0× in
kinetic energy, so a measured burst is far below the speed flight needs.

## My value

- **3× leap exit speed: 2.39 m/s (drag-free lower bound), = √3 = 1.73× the stated 1.38 m/s maximum.** The uncertainty is
  carried entirely by U_max, which I could not verify (could-not-access). The ratio of √3 is exact under the ballistic model.
- **Flight speed: 4.4–5.8 m/s** over plausible mass and area. The recorded 4.37 m/s cannot be independently checked, because its mass is back-solved.

## Comparison with the recorded value

I saw the recorded values (2.39 m/s, 1.73×, 4.37 m/s) during the disclosed grep.
- 2.39 m/s and 1.73×: **AGREE**. This is arithmetic only, conditional on the unverified 1.38 m/s input.
- 4.37 m/s: **CANNOT TELL**. It is a project-derived number, its mass was back-solved, and my range is 4.4–5.8 m/s.

Because I was not blind, two derivations agreeing here is weak evidence. The arithmetic is trivial. The real risks are in
the inputs: the unverified Miln 2021 burst speed, and the assumption that exit speed equals burst speed.

Sources searched: [PLoS ONE, Palstra et al. 2010](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0014483) (search-summary), [JoVE swim endurance protocol](https://www.jove.com/t/63240/assessment-of-swim-endurance-and-swim-behavior-in-adult-zebrafish) (search-summary, not relevant to burst speed).

```swarm-replication
{"claim_id": 192, "my_value": "2.39 m/s (= 1.38 x sqrt3, 1.73x stated max; drag-free lower bound); flight speed 4.4-5.8 m/s depending on assumed mass/area", "agrees": true,
  "note": "Not blind (the recorded working was seen in a grep); the 3x-leap arithmetic agrees exactly, but the 1.38 m/s input (Miln 2021) could not be accessed and 4.37 m/s cannot be checked independently because its mass was back-solved."}
```
