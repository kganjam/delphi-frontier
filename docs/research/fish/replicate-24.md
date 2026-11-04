# Replication 24: launch-speed deficit from the corrected CL_max and the S21 burst speed

Project: `zebrafish-flight` · Written 2026-11-04 · Independent re-derivation (I was not shown the answer)

> **My value (calculated, not observed).** The stall speed of the reference wing (0.4 g fish, 1 body-length
> span = 4 cm, AR 5) at the corrected C_L,max of 1.07 is **4.37 m/s**. Divided by the S21 burst speed of
> 0.84 m/s, that gives a **launch-speed deficit of ≈5.2×**. In kinetic-energy terms it is **≈27×**.
> **Uncertainty band: 4.1–6.1× in speed (≈17–38× in KE)**, spanning C_L,max 0.9–1.15 and burst
> speeds 0.78–1.02 m/s.

## 0. How I read the question

The question text I received was truncated to "Current best evidence", with the context "computed here
from the corrected CL_max and the S21 burst speed". I take the quantity to be the project's headline
launch deficit: the required (stall) speed for the reference 1-BL, AR 5 wing, divided by the fish's
achievable exit speed. In the original analysis the stall speed used C_L = 0.6 and the fish speed used
the Ucrit proxy. **If claim 24 means some other quantity, this replication does not test it.** That
reading is my inference about what the question asks.

To find the inputs I read only these input documents (all on remote branches of this repository):
`S21-behaviour.md` (the burst speed); the parent glide-physics report (the reference wing and mass);
and the C_L,max rows in `challenge-1.md`, `challenge-5.md` and `replicate-5.md`. I did this before
looking for any recorded value of claim 24.

## 1. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Body mass m | 0.4 g | Project design premise, from the parent report `zebrafish-glide-physics.md` (branch `claude/zebrafish-glide-physics-j176og`). I did not verify it against zebrafish morphometrics. | full-text (repo doc); primary source **unknown** |
| Wing span b | 1 BL = 0.04 m (reference wing) | same parent report | full-text (repo doc) |
| Aspect ratio | 5 | same, a design assumption | full-text (repo doc) |
| Air density ρ | 1.2 kg/m³ | standard sea-level value (my choice, matches the parent) | — |
| Air kinematic viscosity ν | 1.5×10⁻⁵ m²/s | standard (used only for an Re check) | — |
| **Corrected C_L,max** | **1.07** (central), band 0.9–1.15 | Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543–556: steady C_L,max **1.07** (*Sympetrum sanguineum*) and **1.15** (*Calopteryx splendens*), real wings, Re ≈ 700–2,400. The same abstract gives a highest in-glide C_L of 0.93, "not necessarily the maximum". | **search-summary** (I confirmed it by my own web search this session; I did not read the full text) |
| Lower C_L,max bound | 0.9 | Relayed by `challenge-5.md` ("about 0.9–1.15") and `replicate-5.md` (best estimate ~1.0, range 0.9–1.1, cambered membrane) | full-text (repo docs); their underlying sources are search-summary |
| **S21 burst speed** | **0.84 m/s** (0.78–0.91 m/s at ±1 s.e.m.) | Danos & Lauder 2012, *J. Exp. Biol.* 215:1854, doi:10.1242/jeb.068957. Mean maximum Re 27,800 ± 2,140 (s.e.m.), adults TL 33.0 mm, 1000 fps, as relayed by `S21-behaviour.md`. U = Re·ν/L is S21's **calculation**, not a printed velocity. | **could-not-access** by me. sites.harvard.edu returned CONNECT 403; doi.org gave a 5.6 kB stub. The Europe PMC abstract (abstract read-level) confirms the 1000 fps setup and the three viscosities, but contains no Re or velocity number. The Re value rests on S21's full-text read. |
| Burst speed scaled to 4 cm | 1.02 m/s | S21's extrapolation at constant BL/s, which S21 calls an upper estimate | full-text (repo doc) |

The fish speed is the burst speed **inside the water**. It is not a measured water-exit speed.

## 2. Arithmetic

W = m·g = 0.4×10⁻³ × 9.81 = 3.924×10⁻³ N
S = b²/AR = 0.04² / 5 = 3.20×10⁻⁴ m² (chord c = 8 mm)

Stall speed: V_s = √(2W / (ρ·S·C_L,max))

- C_L,max = 1.07: ρ·S·C_L = 1.2 × 3.20e-4 × 1.07 = 4.109e-4. 2W = 7.848e-3. V_s = √(19.10) = **4.370 m/s**.
- Check by scaling: 5.836 m/s (the C_L = 0.6 value) × √(0.6/1.07) = 5.836 × 0.7488 = 4.370 m/s. ✓
- Re check: 4.370 × 0.008 / 1.5e-5 = **2,331**. That falls inside the 700–2,400 band where Wakeling &
  Ellington measured C_L,max, so the correction is consistent in Re. It is still a dragonfly wing, not
  a fin membrane (see §4).

Burst speed: U = Re·ν_water/L = 27,800 × 1.0e-6 / 0.033 = **0.842 m/s** (S21's method, which I reproduced).

**Deficit (speed): 4.370 / 0.842 = 5.19 ≈ 5.2×. Deficit (KE): 5.19² = 26.9 ≈ 27×.**

Sensitivity grid (all calculated). Each cell gives speed ratio, then KE ratio.

| C_L,max | V_s (m/s) | U = 0.78 | U = 0.84 | U = 0.91 | U = 1.02 (4 cm scaled) |
|---|---|---|---|---|---|
| 0.6 (uncorrected) | 5.84 | 7.5× / 56× | 6.9× / 48× | 6.4× / 41× | 5.7× / 33× |
| 0.9 | 4.77 | 6.1× / 38× | 5.7× / 32× | 5.3× / 28× | 4.7× / 22× |
| 1.0 | 4.52 | 5.8× / 34× | 5.4× / 29× | 5.0× / 25× | 4.4× / 20× |
| **1.07** | **4.37** | 5.6× / 32× | **5.2× / 27×** | 4.8× / 23× | 4.3× / 18× |
| 1.15 | 4.22 | 5.4× / 29× | 5.0× / 25× | 4.6× / 22× | 4.1× / 17× |

Band across the corrected rows (0.9–1.15) and all four U columns: **4.1–6.1× in speed, 17–38× in KE**.

For context, the old headline used C_L 0.6 against Ucrit 0.548 m/s: 5.84/0.548 = 10.65×. The two
corrections together roughly halve the speed deficit: C_L,max contributes √(1.07/0.6) = 1.34×, and
burst over Ucrit contributes 1.54×. **The deficit does not close.**

## 3. Author claims vs my inference

- Wakeling & Ellington *claim* steady C_L,max of 1.07 and 1.15 for dragonfly wings. Applying that
  number to a zebrafish fin membrane is **my inference** (and the challenge authors' inference). It is
  not their claim.
- Danos & Lauder *report* a mean maximum Re. Converting it to 0.84 m/s is S21's calculation, which I
  reproduced. Treating it as an exit speed is an inference.
- Sources disagree on the C_L,max proxy, and I keep that disagreement visible. The parent report used
  0.6 as a central value and called the true value unknown. `replicate-5.md` gives 0.5–1.1 overall,
  with ~0.4–0.55 for an ideal flat plate on weak, single-source support. `challenge-5.md` gives
  0.9–1.15. If the fin behaves like a flat plate (C_L,max ~0.5), the deficit is **above** the 0.6 row
  (≈7.6× against 0.84 m/s; calculated), not below it.

## 4. What this does not establish

- Nobody has measured fin-membrane C_L,max in air. My search scope was the single web search above
  plus the repo docs. The "corrected" value is a dragonfly-wing proxy.
- The 0.84 m/s value is a mean of per-sequence peaks from n = 5 fish. Table 1 of Danos & Lauder (the
  direct velocity) was not read by me or by S21.
- The 0.4 g mass and the 1-BL, AR 5 wing are design premises. A larger wing lowers V_s as S^-½.
- This assumes stall at L = W in steady glide. It ignores ground effect, taxiing thrust, and dynamic
  stall during launch.

## 5. Comparison with the recorded value

I looked for the recorded value only after finishing §1–§4 and writing them down. A grep of all remote
branches for "corrected CL_max" / "S21 burst" found one file:
`docs/research/fish/challenge-24.md` (branch `claude/challenge-takeoff-speed-claim-bsocad`). It quotes
the claim as: "required takeoff 4.37 m/s against a measured burst of 0.842 m/s is a 5.2x speed and 27x
kinetic-energy deficit". Read-level: full-text (repo doc). I read only its claim statement and its
arithmetic and proxy sections.

| Quantity | Recorded | Mine |
|---|---|---|
| Required (stall) speed | 4.37 m/s | 4.370 m/s |
| Burst speed | 0.842 m/s | 0.842 m/s |
| Speed deficit | 5.2× | 5.19× |
| KE deficit | 27× | 26.9× |

**AGREE** on the central value.

Caveats on that agreement:

- **The agreement is not fully independent on the burst speed.** Neither of us read Danos & Lauder's
  velocity table. Both values rest on S21's Re-to-speed conversion, which I reproduced but could not
  check against the primary source.
- **The claim calls 0.842 m/s "measured".** It is *derived*: S21 calculated it from a measured Re. That
  wording overstates the evidence level.
- **The recorded claim gives no uncertainty.** My band is 4.1–6.1×, driven by the C_L,max proxy and
  the burst-speed definition.
- I also agree with challenge-24 that the 27× KE figure is the 5.2× speed ratio squared, so it is not
  a second, independent piece of evidence.

```swarm-replication
{"claim_id": 24, "my_value": "5.2x speed deficit (4.37 m/s stall at C_L,max 1.07 / 0.842 m/s burst; 27x KE), band 4.1-6.1x", "agrees": true, "note": "Independent arithmetic reproduces 4.37 m/s / 0.842 m/s = 5.19x (26.9x KE), but the burst speed is Re-derived not measured and both derivations share S21's unverified input, so the agreement is partial evidence only."}
```
