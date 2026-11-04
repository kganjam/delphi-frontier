# Replication 270: at the low-end exit (0.45 m/s) the S32 taxi fails on weight support, not thrust

**Kind of result:** calculated. Nothing here is an observation. It is a re-computation of a vertical force balance, using the model and inputs that S32 declares.

## Disclosure (read this before the numbers)

- The only copy of `S32-organism.md` is on branch `claude/s32-multi-stroke-launch-qpq9g2` (path `docs/research/fish/S32-organism.md`). It is not on this branch.
- To find the inputs I ran a keyword `grep` over that file. The grep output included the result lines: §3.1 table rows, the `answer:` line, and §6. So **I saw the recorded value before I computed mine.**
- After that I read only §1 (model equations) and §2 (input table). I did not read `S32_taxi.py` or any other replication or challenge branch.
- This is therefore an **arithmetic and model re-derivation with prior exposure**. It is not a blind derivation. Weigh the agreement accordingly.
- A second limit: I used S32's own model, its vertical balance and the CL_z ≤ 1 cap. My agreement checks the arithmetic and the internal logic, not whether the model is physically right.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Body mass m | 0.25 g (design) and 0.40 g (heavy case) | S32 §2/§3.3, inherited from S28 | full-text (of S32; S28 itself not read) |
| g | 9.81 m/s² | constant | n/a |
| Exit speed U | 0.45 m/s (low end) | the question / S32 | full-text (S32) |
| Wing lift share | (U/V_to)². V_to = 4.41 m/s (0.25 g) or 5.58 m/s (0.40 g) | S32 §2, from the S28 case-C wing (192 mm², AR 5, CL_max 1.07), itself unmeasured | full-text (S32); S28 not read |
| Lower caudal lobe area | 18.9 mm² (half of 0.7·6 mm·9 mm) | S32 §2, **ASSUMED** there; fin chord 6 mm is Wakamatsu 2019 via S24 | full-text (S32); primary not read |
| Immersed fraction φ | 0.25 / 0.5 / 1.0 | S32 §2, **ASSUMED** and never measured | full-text (S32) |
| Lobe CL_z,max | 1.0 | S32 §2, **ASSUMED** | full-text (S32) |
| Meniscus pull-down | F_σ,v = 2σc·cosθ. σ = 0.072 N/m, c = 6 mm, cosθ 0–1 (assumed) | S32 §1–2 | full-text (S32) |
| Water density | 998 and 1000 kg/m³ (both run) | physical constant | n/a |

## Model (S32 §1, vertical)

Weight support requires L_wing + F_z,lobe = W + F_σ,v, with:

- F_z,lobe = ½ρ_w U² S_imm CL_z
- S_imm = φ·18.9 mm²
- L_wing = W·(U/V_to)² below V_to

So:

  CL_z,req = [W(1 − (U/V_to)²) + 2σc·cosθ] / (½ρ_w U² φ S_lobe)

Support fails if CL_z,req > 1. The minimum supportable speed is where CL_z,req = 1:

  U_min² = (W + F_σ,v) / (½ρ_w φ S_lobe + W/V_to²)

## Arithmetic

**Common quantities at U = 0.45 m/s, ρ_w = 998 kg/m³:**

- q = ½ × 998 × 0.45² = **101.0 Pa**.
- W = 0.25e-3 × 9.81 = **2.453 mN** and 0.40e-3 × 9.81 = **3.924 mN**.
- Wing share = (0.45/4.41)² = **1.04 %** and (0.45/5.58)² = **0.65 %**.
- Meniscus = 2 × 0.072 × 0.006 × cosθ = **0 to 0.864 mN**.

**Generous corner** (0.25 g, φ = 1, cosθ = 0):

- Lobe force available at CL_z = 1: q·S = 101.0 × 18.9e-6 = 1.909 mN.
- Required: 2.453 × (1 − 0.0104) = 2.427 mN.
- CL_z,req = 2.427 / 1.909 = **1.27**.
- U_min = √(2.453e-3 / (0.5 × 998 × 18.9e-6 + 2.453e-3/4.41²)) = √(2.453e-3 / (9.431e-3 + 1.261e-4)) = **0.507 m/s**.

**Stingy corner** (0.40 g, φ = 0.25, cosθ = 1):

- Required: 3.924 × (1 − 0.0065) + 0.864 = 4.762 mN.
- Lobe force available: q × 4.725e-6 = 0.4773 mN.
- CL_z,req = 4.762 / 0.4773 = **9.97**.
- U_min = √(4.788e-3 / (2.358e-3 + 1.260e-4)) = **1.388 m/s**.

**Full sweep** (2 masses × 3 φ × 3 cosθ, script inline below): CL_z,req ranges from **1.27 to 9.97** at 0.45 m/s, and U_min from **0.507 to 1.388 m/s**. Using ρ_w = 1000 kg/m³ changes the last digit only: 1.27–9.95 and 0.506–1.387 m/s.

Every one of the 18 cases has CL_z,req > 1, so support fails at 0.45 m/s throughout the swept assumption space.

**"Not thrust" check (my inference, generous case only).** Take G = 0.52 m²/s², φ = 1 and C_D = 0.08:

- T_lobe = ½ × 1000 × 18.9e-6 × (0.52 − 0.08 × 0.45²) ≈ **4.8 mN**.
- Air drag on the wing and body at 0.45 m/s is ~µN.

So in the generous case thrust exceeds the non-support drags, and the binding failure is the vertical balance. In the stingier S32 scenarios, net force is also negative at 0.45 m/s. That deficit comes mainly from the lobe's induced drag, which is itself a cost of trying to support the weight. I did not recompute those rows.

```python
for m,V in ((0.25e-3,4.41),(0.40e-3,5.58)):
  W=m*9.81
  for phi in (0.25,0.5,1.0):
    for cth in (0,0.5,1):
      S=phi*18.9e-6; F=2*0.072*0.006*cth; q=0.5*998*0.45**2
      CL=(W*(1-(0.45/V)**2)+F)/(q*S); Um=((W+F)/(0.5*998*S+W/V**2))**0.5
```

## Result

**My value:** at U = 0.45 m/s the immersed lobe needs **CL_z ≈ 1.3–10** (1.27–9.97) to hold the body up, against an assumed cap of 1.0. The wing carries only **0.65–1.04 %** of the weight. The minimum supportable speed is **0.51–1.39 m/s**.

The uncertainty is dominated by the assumed immersed fraction φ (a factor of 4), then by mass (a factor of 1.6) and the meniscus term (up to +35 % of W). None of these is measured. The conclusion, support fails, holds across the whole declared sweep. It would only flip if φ·CL_z,max·S_lobe were about 1.3× larger than S32's most generous combination: for example, a larger lobe than the assumed 18.9 mm², or CL_z,max > 1.27.

## Comparison with the recorded value

Seen through the grep (see the disclosure), S32 records:

- "lobe would need CL 1.3–10 to hold the body out of the water (minimum supportable speed 0.51–1.39 m/s)"
- "wing carries 1 % of the weight"
- 2.5–3.9 mN weight on a 5–19 mm² lobe at ~100 Pa

My values match to the stated precision. **AGREE.** This agreement is weaker than a blind one, for two reasons:

1. I had seen the recorded number.
2. I reused S32's model and assumed inputs, rather than independently sourcing the lobe area, immersed fraction or CL_z cap. All of these are unmeasured.

```swarm-replication
{"claim_id": 270, "my_value": "CL_z required 1.27-9.97 (cap 1.0) at 0.45 m/s; wing carries 0.65-1.04% of W; min supportable speed 0.51-1.39 m/s", "agrees": true, "note": "Arithmetic reproduces S32's vertical-balance numbers across the full 18-case sweep, but I saw the recorded value via grep before computing and used S32's own unmeasured lobe-area/immersion/CL_z assumptions, so this confirms the arithmetic, not the physics."}
```
