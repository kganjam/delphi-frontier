# Replication 24: take-off speed deficit, from the corrected C_L,max and the S21 burst speed

**My value (calculated, not observed):** the required take-off (stall) airspeed is **4.37 m/s at C_L,max = 1.07**.
Against the S21 burst speed of 0.842 m/s, that is a **5.2× speed deficit (range 4.8–5.6× over the ±1 s.e.m. burst band)**.
The kinetic-energy ratio at equal mass is **27×**, which is just the speed ratio squared and adds no independent evidence.

If C_L,max is taken over the whole corrected band of challenge-23 (0.7–1.15), the deficit is **5.0–6.4×** at the central burst speed, and **4.6–6.9×** when the burst ±1 s.e.m. is included.
I report the band because challenge-23 itself says 1.07 sits at the top of the range and is not typical.

## Order of work (how independence was kept)

1. I read the input documents only: S21 (`S21-behaviour.md`), replicate-21, challenge-23 (the C_L,max correction) and the parent glide-physics doc (for mass, area and air density).
2. I derived the numbers below.
3. Only after that did I open `challenge-24.md` (branch `origin/claude/challenge-takeoff-speed-claim-bsocad`), which contains the recorded value. See the last section.

**Disclosure:** challenge-23's §1 table already contains V_stall for each C_L,max (for example 4.37 m/s at 1.07). I read it as part of an input document before computing. So my V_stall is not blind to that table. I recomputed it from the raw inputs rather than copying it.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Body mass m | 0.4 g = 4.0×10⁻⁴ kg | project brief, as recorded in `zebrafish-glide-physics.md` (branch `origin/claude/zebrafish-glide-physics-j176og`), "given in brief". It is a design assumption, not a measurement. | full-text (repo doc) |
| Weight W = m·g | 3.924×10⁻³ N (g = 9.81) | calculated | — |
| Air density ρ | 1.2 kg/m³ | same doc, "assumed (sea level, ~20 °C)" | full-text (repo doc) |
| Wing (fin) area S | 3.2 cm² = 3.2×10⁻⁴ m² (span 4 cm = 1 BL, AR 5) | same doc §3, and challenge-23 §1. It is a design scenario, not a measured fin. | full-text (repo doc) |
| Corrected C_L,max | point value 1.07 (*Sympetrum sanguineum* isolated wing). Corrected band 0.7–1.15. | Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543, relayed by challenge-23 (branch `origin/claude/cl-max-ceiling-challenge-ustmov`). Challenge-23 gives the band; 1.07 is the recorded claim-23 value. | **search-summary** (primary paper not read by anyone in the chain; I did not read it either) |
| Burst speed U_burst | 0.842 m/s, ±1 s.e.m. band 0.78–0.91 m/s | S21 (`S21-behaviour.md`, branch `origin/claude/zebrafish-fast-start-velocity-pxsv7e`) and replicate-21, both **derived** as U = Re·ν/L from Danos & Lauder 2012, *J. Exp. Biol.* 215:1854 (Re 27,800 ± 2,140 s.e.m.; TL 33.0 mm; ν assumed 1.0×10⁻⁶ m²/s) | full-text of the repo docs; the docs record the paper as full-text HTML. I did not re-read the paper. |

## Arithmetic (calculated)

Level flight at stall: W = ½ρV²S·C_L,max, so V = √(2W / (ρ·S·C_L,max)).

At C_L,max = 1.07:
- 2W = 7.848×10⁻³ N
- ρ·S·C_L = 1.2 × 3.2×10⁻⁴ × 1.07 = 4.1088×10⁻⁴ m²·kg/m³
- V² = 7.848×10⁻³ / 4.1088×10⁻⁴ = 19.10 m²/s²
- **V = 4.370 m/s**

Speed deficit = V / U_burst:
- 4.370 / 0.842 = **5.19**
- 4.370 / 0.91 = 4.80 (the faster end of the burst band)
- 4.370 / 0.78 = 5.60 (the slower end)

KE ratio at equal mass = (V/U)² = 5.19² = **26.9**. This is not independent of the speed ratio.

Sensitivity to C_L,max (V in m/s, then V/U at U = 0.78 / 0.84 / 0.91, and the KE ratio at U = 0.84):

| C_L,max | V | V/U (0.78 / 0.84 / 0.91) | KE ratio |
|---|---|---|---|
| 0.7 | 5.40 | 6.93 / 6.43 / 5.94 | 41 |
| 0.8 | 5.05 | 6.48 / 6.02 / 5.55 | 36 |
| 0.9 | 4.77 | 6.11 / 5.67 / 5.24 | 32 |
| **1.07** | **4.37** | **5.60 / 5.20 / 4.80** | **27** |
| 1.15 | 4.22 | 5.40 / 5.02 / 4.63 | 25 |

Note: the middle V/U column divides by 0.84 m/s (rounded). At exactly 0.842 m/s and C_L 1.07 the ratio is 5.19.

## Caveats (my inference, not the sources' claims)

- **Both main inputs are themselves second-hand.** The 1.07 is relayed at search-summary level. The 0.842 m/s is inverted from a Reynolds number, not a reported speed (Table 1 of Danos & Lauder was not read).
- **The mass and area are scenario values** (a 0.4 g, 4 cm fish with a 1-BL-span, AR-5 fin). They are not measurements. V scales as √(m/S).
- **This compares a still-air stall airspeed with a fully submerged burst water speed.** Wind and surface taxiing (lower drag with the body out of the water) are not in the ratio.
- **C_L,max of a fin membrane in air is unknown.** 1.07 is a dragonfly wing, which challenge-23 calls the upper end of the thin-wing band.

## Comparison with the recorded value (read only after deriving)

The recorded claim, quoted in `challenge-24.md` (branch `origin/claude/challenge-takeoff-speed-claim-bsocad`, read in full-text), is: "required takeoff 4.37 m/s against a measured burst of 0.842 m/s is a 5.2x speed and 27x kinetic-energy deficit". Recorded value: 5.2 (ratio).

- My 4.370 m/s, 5.19× and 26.9× **match** at the same inputs. **AGREE.**
- **One wording disagreement:** the claim calls 0.842 m/s a "measured burst". S21 and replicate-21 both say it is *derived* from a measured Re, not measured directly.
- **One scoping note:** the recorded 5.2× uses the top-end C_L,max (1.07). Over challenge-23's corrected band 0.7–1.15 the same calculation gives 5.0–6.4×. Including the burst s.e.m. it gives 4.6–6.9×. The claim's conclusion, that a large deficit remains, holds across that whole band.
- **Limit of this agreement:** both derivations use the same relayed inputs. This confirms the arithmetic and the choice of inputs. It does not check the inputs themselves.

```swarm-replication
{"claim_id": 24, "my_value": "5.19x speed deficit (4.37 m/s required at CL_max 1.07, rho 1.2, S 3.2 cm^2, m 0.4 g, vs 0.842 m/s derived burst); 4.8-5.6x over burst +/-1 s.e.m.; 4.6-6.9x over the corrected CL_max band 0.7-1.15; KE ratio 26.9x (= speed ratio squared)", "agrees": true,
  "note": "Recomputed V = sqrt(2W/(rho S CL)) independently and match 4.37 m/s / 5.2x / 27x, but the burst is derived not measured, 1.07 is the top of the corrected CL band, and both inputs are relayed rather than read at primary source."}
```
