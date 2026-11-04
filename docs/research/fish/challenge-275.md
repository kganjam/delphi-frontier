# Challenge 275: adversarial review of S3 (organism mass and power budget)

**Claim under review:** S3's answer and key number, from branch `claude/s3-organism-mass-budget-000ync` (commit d0fd062f, files `docs/research/fish/S3-organism.md` and `S3_budget.py`). I read both in full in this session. I did not write that claim.

**Verdict: WEAKENED.** The central negative survives: with central-thickness tissue at the measured η_h of 0.37, no designed planform closes. But the key number is wrong, and two of the claim's universal statements are false **within the author's own input brackets**:

- the "most generous case" is **1.94×** short, not 2.9×;
- at η_h = 1 the best designed case **closes** (0.72×). It is not "1.06× short";
- at the author's own low-thickness bracket, two designed planforms **close at η_h 0.37** (0.86–0.92×). So "fails for every designed planform" is false as stated.

**Evidence level of this challenge: derived.** It is my own recomputation from S3's stated inputs. **No new measurement and no new source.** The script is `docs/research/fish/challenge-275_check.py`. I wrote it from the formulas stated in S3 §3, not by editing S3's script.

---

## 1. Independent arithmetic

The formulas are taken as stated in S3 §3:
- σ = ρ_fin·t;
- V_to = √(2Mg / (ρ_air S CL));
- launch power per kg of muscle = [V_to³ / (4s)] / η_h · M / (f_m·m_body), with s = run-up distance.

Constants as S3 gives them: g 9.81 m s⁻²; ρ_air 1.225 kg m⁻³; CL 1.07; m_body 0.40 g; one body length (BL) = 4 cm.

**What reproduces exactly (computed):**
- σ = 0.0420 / 0.1382 / 0.3114 / 0.4375 kg m⁻².
- V_self = 0.79 / 1.44 / 2.16 / 2.56 m s⁻¹.
- Lift per area at 1.38 m s⁻¹ = 0.127 kg m⁻². So "central tissue cannot lift itself at 1.38 m/s" is **arithmetically correct**.
- Every wing-mass percentage in S3 §3.2. This includes 2.0–21.0 % for the 192 mm² wing, 31–211 % for the large wings, and the crossover at 0.4 g / 0.3114 kg m⁻² = **1,285 mm²**.
- V_to for the S28 192 mm² wing: 5.77 m s⁻¹ (central) and 5.99 m s⁻¹ (high).
- S10 at 2 BL, f_m 0.6, η_h 0.37: **409 W kg⁻¹ (2.87×)**.
- The S28-C range of 20–161×.

**What does not reproduce: the power table omits two of S3's own designed planforms.**

S3 §3.5 and `S3_budget.py` section 5 iterate only over `[PLANFORMS[2], PLANFORMS[4], PLANFORMS[5]]`, which are S28-C, S2-mid and S10. That list leaves out **S2-large (1,800 mm²)** and **S28 "fly at 1.38 m/s" (1,925 mm²)**. Both are listed in S3's own §3.2 and both are counted in the claim's "31–211 %" mass range. They are the two planforms with the lowest V_to, and launch power scales as V_to³·M.

Recomputed at 2 BL, f_m 0.6 (all computed, W kg⁻¹ muscle, multiple of the 142.7 W kg⁻¹ measured value):

| Planform | tissue | V_to (m/s) | η_h = 0.37 | η_h = 1 |
|---|---|---|---|---|
| S10 1,070 mm² (S3's "most generous") | central | 2.77 | 409 (2.87×) | 151 (1.06×) |
| **S2-large 1,800 mm²** | central | 2.32 | **286 (2.00×)** | **106 (0.74×, closes)** |
| **S28 1,925 mm²** | central | 2.28 | **276 (1.94×)** | **102 (0.72×, closes)** |
| S2-large 1,800 mm² | low (40 µm, 1.05) | 1.99 | **132 (0.92×, closes)** | 49 (0.34×) |
| S28 1,925 mm² | low | 1.93 | **122 (0.86×, closes)** | 45 (0.32×) |
| S10 1,070 mm² | low | 2.49 | 243 (1.70×) | 90 (0.63×) |
| S2-mid 900 mm² | low | 2.70 | 303 (2.12×) | 112 (0.78×) |

**Consequences (my inference from the table):**
1. **Key number.** The most generous designed case at central tissue and η_h 0.37 is **1.94×** (S28 1,925 mm²), not 2.9×. The stated range "409–23,000 W/kg" should start at **276 W kg⁻¹** at central tissue, or at **122 W kg⁻¹** across the brackets S3 itself declares.
2. **"Even at η_h = 1 the best case is 1.06× short"** is false. At central tissue, two designed planforms close at η_h = 1. They would close at η_h ≥ 0.37 × 1.94 ≈ **0.72** (S28 1,925 mm²) or ≥ 0.74 (S2-large). S3 §6 item 1 also says "No η_h ≤ 1 closes any planform on its own". That statement is false for the same reason.
3. **"The power budget fails for every designed planform"** is false over S3's declared tissue bracket. It holds only at central or higher σ. At the low bracket (Puri's 40 µm distal value, soft density), the 1,800 and 1,925 mm² wings close at η_h 0.37 and f_m 0.6. The low bracket is the regime S3 itself proposes as the target in §6 item 2: "If σ ≤ 0.05 kg m⁻², the mass budget closes for every planform". **That is where the power budget also closes for the largest wings.** At f_m 0.3 they remain 1.7–1.9× short.
4. **A continuous optimum, outside the designed set.** Over planform area at 2 BL, f_m 0.6, η_h 0.37, the minimum required power is ~225 W kg⁻¹ (1.58×) at ~4,300 mm² for central tissue, and ~38 W kg⁻¹ (0.26×) at ~14,000 mm² for low tissue. These planforms are not designed by any sibling, so they do not falsify "every designed planform". They do show that S3's 2.9× is not a property of the tissue.

## 2. Proxies

- **Muscle power.** The comparison value, 142.7 W kg⁻¹, is a *Scorpaena notata* fast-start work-loop mean at 20 °C (S3 P1, abstract-level). It stands in for adult zebrafish white muscle at 28 °C, which is `unknown` (S3 found no adult value). Mean power from a cycled work loop is a mean over one tail-beat cycle. The requirement here is a mean over a 40–60 ms, multi-beat acceleration. These are different averaging windows, and I did not quantify the mismatch.
- **η_h.** The 0.37 is a pike C-start value (abstract, via S29), standing in for a 4 cm fish accelerating a wing-laden body. S3 flags this itself. I note only that the corrected central closure threshold is η_h ≈ 0.72, not >1. **That makes η_h a live, not merely formal, route to closure.**
- **Fin density and thickness.** These are caudal-fin values and density proxies, as S3 states. Not re-litigated here.

## 3. Hidden assumption

The model assumes a constant-acceleration submerged run-up of 0.5–2 BL. S3's own calibration (148 W kg⁻¹ for today's fish over 1 BL at η_h 0.37) depends on choosing 1 BL. If real zebrafish reach 1.38 m s⁻¹ in a shorter distance, the same model would demand more than 142.7 W kg⁻¹ for a performance fish actually achieve. That would mean the η_h × muscle-power inputs are pessimistic, and would weaken every shortfall. **I did not find or search for a measured adult zebrafish distance-to-peak-speed. It is `unknown` here**, so this point is a flagged sensitivity, not a correction.

## 4. Evidence level

S3 labels the claim "derived" and marks computed numbers as computation. **That is honest.** One defect: the claim states "409–23,000 W/kg … for every designed planform" as if every designed planform had been computed. Two were not. That is a coverage error, not a mislabelled measurement.

## 5. Regimes and counter-examples

- **Low-σ regime.** As shown in §1, this regime already exists inside S3's own bracket.
- **Small fish that leave the water ballistically: freshwater hatchetfishes (Gasteropelecidae).** I recall that small fish of this family leave the water and are sometimes described as pectoral-assisted. **Read-level: none. This is recalled, not searched or read in this session.** I do not rest the verdict on it, and I give no numbers for it.
- **Not searched:** taxi launches (S3 explicitly excludes them), and adult zebrafish kinematics.

## 6. What the corrected claim should say

> At central fin tissue and η_h 0.37, launch power is ≥1.94× short for every designed planform (276 W/kg vs 142.7; S28 1,925 mm², 2 BL, f_m 0.6). It closes at η_h ≥ ~0.72 for the 1,800–1,925 mm² wings. At the low thickness bracket (40 µm, 1.05 g/cm³) those wings close even at η_h 0.37 (0.86–0.92×). The power negative is therefore conditional on σ ≳ 0.05–0.14 kg/m² and η_h ≲ 0.7, not general.

The mass-budget half of the claim (2–21 %, 31–211 %, the 1,285 mm² crossover, V_self 1.44 m/s) **survives** my recomputation.

```swarm-challenge
{"claim_id": 275, "outcome": "weakened", "reason": "S3's power table omitted its own 1800 and 1925 mm2 planforms; including them the most generous central-tissue case is 1.94x short (not 2.9x), it closes at eta_h=1 (0.72x, not 1.06x short), and at the author's own low-thickness bracket those wings close even at eta_h 0.37 (0.86-0.92x), so 'fails for every designed planform' is false while the central-tissue negative survives.",
  "corrected_value": "1.94x launch-power shortfall in the most generous central-tissue designed case (276 W/kg muscle vs 142.7 W/kg; S28 1925 mm2, 2 BL, f_m 0.6, eta_h 0.37); 0.86-0.92x (closes) at low tissue sigma 0.042 kg/m2 for 1800-1925 mm2",
  "depends_on": ["S3 formulas and constants (CL_max 1.07, rho_air 1.225, m_body 0.40 g, BL 4 cm)", "S3 tissue brackets: Puri 2018 40-200 um caliper; Murciano 2018 281 um; density proxies 1.05 (Robertson 2008) and 1.557 g/cm3 (Tont 1977 via S9); 20% ray fraction assumption", "planform areas 1800 mm2 (S2-large) and 1925 mm2 (S28) as designed planforms", "142.7 W/kg fast-start muscle power (Wakeling & Johnston 1998, abstract)", "eta_h 0.37 (Frith & Blake via S29)", "muscle fraction 0.3/0.6 (S29 assumption/secondary)", "constant-acceleration run-up model of 0.5-2 BL"]}
```
