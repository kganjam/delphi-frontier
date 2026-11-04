# Replication 268: THRUST PASSES (S32, step 3: thrust vs drag at the exit speed)

## 0. Independence disclosure (read this first)

This derivation is **not fully blind**. To find the context file, I ran a grep for `thrust|pass|density`
on `docs/research/fish/S32-organism.md` (branch `origin/claude/s32-multi-stroke-launch-qpq9g2`, commit
c1b761eb). That grep printed S32's short-answer and closing `answer:` lines, so I saw the recorded
result before I derived anything. I then read S32's inputs table (§2) on purpose, because the brief
says the inputs live there. I did **not** read S32's equations (§1), its trajectory or sensitivity
sections (§3–4), or `S32_taxi.py`. The density ratio and the drag and thrust arithmetic below are
computed from primary constants with my own script. Weigh this as a **partially independent check**,
not a blind replication.

## 1. What I take the claim to be

At the measured burst exit speed U = 1.38 m/s, once the body is in air, does the net thrust of the
still-immersed caudal lobe exceed the drag? The claim includes the water/air density ratio
("density ratio verified here").

## 2. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| ρ fresh water | 999.10 (15 °C), 998.21 (20 °C), 996.23 (28 °C) kg/m³ | Standard tabulated values (CRC Handbook / IAPWS), from memory and not re-fetched this session | could-not-access (standard constant, not re-read) |
| ρ dry air, 1 atm | 1.2250 (ISA 15 °C), 1.2041 (20 °C), 1.172 (28 °C) kg/m³ | ISA / ideal gas, ρ = p/(R_d T) | standard constant (computed, not read) |
| Exit (burst) speed U | 1.38 m/s | S32 table, citing a measured zebrafish burst | listing (S32 table read; primary not read by me) |
| Body frontal area A_b | 24 mm² | S32 table "from S29" | listing (S29 not read) |
| Body C_d | 0.1 / 0.2 / 0.3 | S32: ASSUMED | listing |
| Foil thrust law | C_T = 2.55 St² − 0.08 | Floryan, Van Buren, Rowley & Smits 2017 (arXiv 1704.07478), as quoted in S32 | listing (I did **not** re-read Floryan) |
| Whole caudal fin area S | 37.8 mm²; lower lobe 18.9 mm² | S32: ASSUMED | listing |
| Immersed fraction φ | 0.25 / 0.5 / 1 | S32: ASSUMED | listing |
| Mass, V_to, wing k, CD0 | 0.25 g; 4.41 m/s; 0.0796; 0.08–0.20 | S32 citing S28 (wing not measured) | listing |
| Wing CL_max (for wing area) | 1.0 | **my assumption**. S28 was not read | assumed |

## 3. Arithmetic (all calculated, none observed)

**Density ratio ρ_w/ρ_a** (calculated):
- 999.10/1.2250 = 815.6 (15 °C water, ISA air)
- 998.21/1.2041 = 829.0 (20 °C, both)
- 996.23/1.172 = 850.0 (28 °C, both: typical zebrafish husbandry temperature)
- Full temperature-mixing range: 813–852.

**Body drag at U = 1.38 m/s** (calculated, 20 °C):
- q_water = ½·998.21·1.38² = 950.5 Pa; q_air = ½·1.2041·1.38² = 1.1465 Pa
- D_water = C_d·q·A_b = 2.28 / 4.56 / 6.84 mN for C_d 0.1 / 0.2 / 0.3
- D_air = 2.75 / 5.50 / 8.26 µN for the same C_d
- At equal C_d the drag ratio is exactly the density ratio, 829 (20 °C).

**Thrust calibration** (calculated): at the burst peak dU/dt = 0, so the whole-fin net foil force
equals body water drag: ½ρS(G − 0.08U²) = D_water, with G = 2.55 (fA)².
- G = 0.08U² + D_water/(½ρS) = 0.273 / 0.394 / 0.515 m²/s² → f·A = 0.327 / 0.393 / 0.449 m/s.

**Net lobe force in the taxi at U = 1.38 m/s** (calculated): ½ρ_w·φ·S_lobe·(G − 0.08U²). Because
the tail speed is held at its calibrated value, this reduces algebraically to **φ·(S_lobe/S)·D_water
= (φ/2)·D_water**:

| C_d (calibration) | φ = 0.25 | φ = 0.5 | φ = 1 |
|---|---|---|---|
| 0.1 | 0.29 mN | 0.57 mN | 1.14 mN |
| 0.2 | 0.57 mN | 1.14 mN | 2.28 mN |
| 0.3 | 0.86 mN | 1.71 mN | 3.42 mN |

**Drag to beat in air** (calculated, partial):
- Body in air: 3–8 µN.
- Wing (my estimate): W = 2.45 mN; S_w = W/(½·1.225·4.41²·CL_max=1) = 206 mm²; the wing carries
  (1.38/4.41)² = 9.8 % W, so CL = 1.0; D = (CD0 + k·CL²)·q·S_w = **38–67 µN**.
- **Not derived:** induced or support drag on the immersed lobe as it carries the remaining ~90 % of
  weight (needs a lobe aspect ratio and lift model I did not set up). This is the main gap in my check.

## 4. My value

**Density ratio ρ_w/ρ_a = 830 (range 813–852, set by water and air temperature); calculated, not
observed.** Net immersed-lobe thrust at 1.38 m/s is **0.29–3.4 mN** across the assumed φ and C_d
(1.1–3.4 mN at φ = 1). Air drag on the body plus wing is **≈ 0.04–0.08 mN** (calculated, CL_max
assumed). That makes thrust/drag about 4–80×, **excluding lobe support drag**. On this partial
accounting thrust passes at 1.38 m/s in every case, and with the widest margin at φ ≥ 0.5.

## 5. Comparison with the recorded value (read after deriving, apart from the disclosure in §0)

S32 records: ρ_w/ρ_a = 816; body drag 4.6 mN in water → 8 µN in air, "816-fold"; lobe thrust
1.1–3.4 mN against 0.09–0.43 mN total drag; "thrust exceeds drag by 3–40×"; step 3 PASSES at 1.38 m/s.

- **Density ratio: AGREE within uncertainty.** 816 matches 15 °C water against ISA air (815.6). At
  zebrafish husbandry temperature (28 °C) I get 850, which is 4 % higher. That difference does not
  change any conclusion.
- **Lobe thrust 1.1–3.4 mN: AGREE.** I reproduce 1.14 and 3.42 mN exactly at φ = 1. These
  are the φ = 1 values. At φ = 0.25 the thrust is only 0.29–0.86 mN, which S32's "generous and
  central cases" wording does not show.
- **Internal inconsistency in S32 (my inference):** 4.57 mN / 8.4 µN = **544**, not 816. Back-
  calculating, S32's 8.4 µN uses C_d 0.3 in air (with ρ_a = 1.225), while its 4.57 mN uses C_d 0.2 in water.
  The "816-fold" figure holds only at equal C_d. The two quoted drag numbers imply a 544-fold drop.
  This is a presentation error. It does not affect the pass: either way, body drag in air is negligible.
- **Total drag 0.09–0.43 mN and the "3–40×" margin: CANNOT TELL.** My body plus wing drag (0.04–0.08 mN)
  sits below S32's lower end, as it should if S32 adds lobe support drag, which I did not derive.
  Even if the support drag were S32's maximum of 0.43 mN, the φ ≥ 0.5 cases (≥ 0.57 mN) still pass. The
  φ = 0.25, C_d 0.1 case (0.29 mN) would not.

**Overall: AGREE** that thrust exceeds drag at the 1.38 m/s exit for φ ≥ 0.5, and on the density
ratio (≈ 816–850). The agreement is weakened by the contamination in §0, by inheriting all of S32's
assumed inputs (fin area, φ, C_d, the Floryan law not re-read), and by the 816-vs-544 inconsistency.

```swarm-replication
{"claim_id": 268, "my_value": "rho_w/rho_a = 830 (813-852 by temperature); net lobe thrust 0.29-3.4 mN (1.14-3.42 mN at phi=1) vs body+wing air drag ~0.04-0.08 mN at U=1.38 m/s (lobe support drag not derived)", "agrees": true,
  "note": "Density ratio and the 1.1-3.4 mN lobe thrust reproduce, and thrust > drag holds for phi>=0.5, but this check is only partly blind (S32's conclusion lines were seen during file search) and S32's quoted 4.57 mN -> 8.4 uN is a 544-fold drop, not 816, because it mixes Cd 0.2 (water) with Cd 0.3 (air)."}
```
