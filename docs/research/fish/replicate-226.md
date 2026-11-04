# Replication 226: "POWER PASSES" (S29, LaMSA launch of a 0.4 g teleost)

**Status:** an independent calculation. Nothing here is a new measurement. Every power figure below is **calculated** from stated inputs; none of it is observed.

## Disclosure of contamination (read this first)
- `S29-organism.md` is not on `main` or on this branch. I found it only on `origin/claude/s29-launch-energy-2iuixr` (commit `44ed2195`).
- **Before I derived anything**, I saw two things from that commit:
  - Its **commit message**, printed by `git show --stat`. It says "power (within insect LaMSA range) pass[es]". So I knew the *direction* of the verdict, but not the number.
  - Its **§1 literature table and §2.1 energy line**, which I read deliberately as the input set.
- I did **not** read S29 §0, §2.2–§6 or `S29_launch_energy.py` until my numbers below were fixed.
- **Consequence:** this is an independent re-derivation of the *magnitude*. It is **not** blind to the *verdict*.

## Inputs

| Input | Value | Source | Read level |
|---|---|---|---|
| Body mass m | 0.40 g | S29 §2 brief ("unless stated otherwise") | full-text (repo doc) |
| Target exit speed V | 4.37 m/s | S28-organism.md (project target, back-solved at 0.25 g) | full-text (repo doc) |
| Mass-scaled V | 5.53 m/s = 4.37·√(0.40/0.25) | S28 scaling rule; my arithmetic | full-text (repo doc) |
| Standard length SL | 3.0 cm, **assumed** | S28 table ("assumed typical adult") | full-text (repo doc) |
| Acceleration distance d | 0.25, 0.5 or 1.0 SL | **my assumption**, a bracket | — |
| Muscle fraction φ (driving muscle ÷ body mass) | 0.4–0.6, **assumed** | **unknown**. A standard web search found no body-mass fraction for zebrafish myotome. The only hit was an area fraction (~67 % of tail cross-section, larva), and that is not a mass fraction | search-summary |
| Hydromechanical efficiency η | 1.0 (ideal); 0.2 as a pessimistic stress test | **my assumption**, unsourced | — |
| Froghopper LaMSA power | 36 W/g mean, 74 W/g best (= 36,000 / 74,000 W/kg muscle) | Burrows 2003, Nature 424:509 | search-summary (I confirmed it independently of S29) |
| Pipefish / seahorse / snipefish LaMSA | 5,795 / 3,266–4,263 / 2,800 W/kg muscle | S29 §1.2 table (it cites Van Wassenbergh 2008, Avidan 2020, Longo 2018) | listing (I took these from S29 and did not re-read the primaries) |
| Vertebrate muscle maximum | 1,121 W/kg | S29 §1.1 (Askew & Marsh 2001, which S29 read as SECONDARY) | listing |

## Arithmetic
Model: the body starts at rest and accelerates at a constant rate a = V²/(2d) over distance d to exit speed V. Then:

- t = 2d/V
- KE per kg = ½V²
- Mean power per kg body = ½V² / t = V³/(4d)
- Peak power = F·V = 2 × mean

**Kinetic energy per kg:**
- ½ · 4.37² = **9.548 J/kg**, which is 3.819 mJ for 0.40 g.
- ½ · 5.53² = 15.29 J/kg, which is 6.116 mJ.

**V = 4.37 m/s, η = 1:**

| d | t | Mean, W/kg body | Peak, W/kg body | Mean, W/kg muscle (φ 0.6–0.4) | Peak, W/kg muscle |
|---|---|---|---|---|---|
| 0.25 SL (0.75 cm) | 3.43 ms | 2,782 | 5,564 | 4,636–6,954 | 9,273–13,909 |
| **0.5 SL (1.5 cm)** | **6.86 ms** | **1,391** | **2,782** | **2,318–3,477** | 4,636–6,954 |
| 1.0 SL (3 cm) | 13.73 ms | 695 | 1,391 | 1,159–1,739 | 2,318–3,477 |

Check of the central row: 4.37³ = 83.45, and 83.45 / (4 × 0.015) = 1,391 W/kg. ✓

**V = 5.53 m/s, η = 1:** the mean is 1,409–5,637 W/kg body (d 1.0–0.25 SL), and the peak per kg muscle reaches 28,185 W/kg at worst.

**Pessimistic stress test, η = 0.2, φ = 0.4, peak power:**
- 17,386 / 34,772 / 69,545 W/kg muscle for d = 1 / 0.5 / 0.25 SL.
- So at d ≤ 0.5 SL this reaches the froghopper range.

**Break-even:** at φ = 0.4 and η = 1, the mean demand would reach 36,000 W/kg muscle only if the release took **0.66 ms**. That is about 10× faster than the 3–14 ms range above.

## My value
At V = 4.37 m/s, d = 0.5 SL and η = 1, the required **mean launch power is ≈1.4 kW per kg of body**. The bracket is 0.7–2.8 kW/kg for d = 1–0.25 SL. Per kg of driving muscle, that is **≈1.2–7 kW/kg mean** and 2.3–14 kW/kg peak.

Measured against the reference systems:
- It is **1–6×** the 1,121 W/kg vertebrate muscle maximum.
- It overlaps the measured fish LaMSA range (2.8–5.8 kW/kg).
- It is **5–30× below** froghopper LaMSA (36–74 kW/kg).

**Verdict (inference):** power passes against the insect-LaMSA benchmark. It needs real amplification, more than direct muscle can give, but no more than LaMSA systems are measured to give. It fails only if the hydromechanical efficiency is as low as ~0.2 **and** the stroke is ≤ 0.5 SL. The main uncertainty is a factor of about 4 from the stroke distance, compounded by the unknown muscle fraction and η.

## Comparison with the recorded value (read only after the above was fixed)
S29 §0 and §6 record **7,400–18,400 W per kg of driving muscle (mean), over a 14 → 5 ms release**. S29 says this is "1.3–3.2× pipefish, well inside froghopper 36,000–74,000", so power is "not binding".

S29 §2.2 per-kg-body figures match mine exactly at the strokes we share:
- 1,391 W/kg at ½ BL (6.86 ms)
- 695 W/kg at 1 BL (13.73 ms)

Its muscle figures are higher than mine for two reasons:
- It divides by η_h = 0.37. S29 attributes this to Frith & Blake (pike) and read it as ABSTRACT; I did not verify it.
- It divides by a one-side muscle fraction of 0.30, and its energy term includes drag.

On those inputs, 1,391 / 0.37 / 0.30 ≈ 12,500 W/kg, which falls inside S29's range. So the difference comes from those inputs, not from the arithmetic.

**Where we disagree:** relative to fish LaMSA, my ideal-η figures overlap the fish range, while S29's sit 1.3–3.2× above it. That gap comes from the η and φ choices above. Both derivations put the demand below froghopper levels.

**AGREE** that power passes against the insect-LaMSA benchmark, and on the per-kg-body numbers. **CANNOT TELL** independently about S29's η = 0.37 and φ = 0.30 inputs, which I did not verify.

## Negative-search scope
- **Muscle mass fraction:** one standard web search ("zebrafish myotomal muscle mass fraction of body mass percent"). It returned no mass fraction, so φ is recorded as unknown and bracketed.
- **η_h:** not searched in this run.

Sources: [Burrows 2003 (doi)](https://doi.org//10.1038/424509a), [Olin copy of Burrows 2003](https://www.olin.edu/sites/default/files/froghopper-burrows.pdf). Both were read at search-summary level.

```swarm-replication
{"claim_id": 226, "my_value": "~1.4 kW/kg body mean (0.7-2.8 kW/kg for 1-0.25 SL stroke, eta=1), i.e. ~1.2-7 kW/kg muscle mean, 5-30x below froghopper 36-74 kW/kg", "agrees": true,
  "note": "Per-kg-body power matches S29 exactly at 1/2 and 1 BL and the pass verdict against insect LaMSA holds, though I saw the verdict direction in the S29 commit message before deriving and did not verify S29's eta_h=0.37 and 0.30 muscle-fraction inputs that raise its muscle-normalised figure to 7.4-18.4 kW/kg."}
```
