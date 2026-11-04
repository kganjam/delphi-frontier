# Replicate-297: independent re-derivation of S3-D-D's "CL needed falls from 2.16 to 1.76"

**Status: derived (calculation).** Nothing here is a measurement. Every number is printed by
`python3 -I docs/research/fish/replicate-297_calc.py`.

## What I read, and what I avoided

- **Read in full (for the setup):** S3 (`S3-organism.md`, `S3_budget.py`, branch
  `claude/s3-organism-mass-budget-000ync`) and S3-D (`S3-deepen.md`, branch
  `claude/s3-mass-power-budget-rcrklv`). These define the "most generous launch" and the 2.16 baseline.
- **Not read before deriving:** `S3-D-deepen.md` / `S3-D-deepen_calc.py` on
  `claude/deepen-s3-sensitive-input-gqmmly` (the derivation under test) and `challenge-297.md` on
  `claude/challenge-s3-d-power-budget-yjfkjp`.
- **Disclosure:** listing branches showed me two commit subject lines. One is the claim restated. The
  other, from challenge-297, says "four power inputs tie CL at a 1% margin, and the hop is ~0.014 mm,
  not ~1 mm". I did not open that file. I did not use its content, and I did not attempt the hop.
- **After** finishing my number, I grepped the recorded calc script for its body-area input (§4).

## 1. Result

**My value: CL needed ≈ 1.88 (bracket 1.75–1.95)** for the most generous launch to close. This is
a calculation. It assumes the zebrafish body planform lifts at the same whole-fish CL and carries no
wing mass.

| Quantity | My value |
|---|---|
| CL needed, wing only | 2.158 (reproduces S3-D's 2.16) |
| CL needed, body included | 1.88 (1.75–1.95) |
| Power shortfall at CL 1.10, body included | 2.23× (2.01–2.36×) |
| Lift margin, body included | 1.71× (1.59–1.77×) |
| Lift margin, wing only, CL 1.10 | 1.96× |

**Verdict.** The direction is the same as the claim's: body lift narrows the margin and does not
close it. S3-D's "power budget does not close" stands under steady lift.

## 2. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| m_body | 0.40 g | project brief, via S3 | via S3 |
| Wing planform S_w (S10, most generous) | 1070 mm² | S10, via S3 | via S3 |
| Fin areal density σ | 0.138 kg m⁻² (1150 kg m⁻³ × 120 µm, partly assumed) | S3 §3.1 | via S3 |
| Run-up s | 2 BL = 0.08 m | S3 §3.5 (assumed) | via S3 |
| η_h | 0.37 | Frith & Blake, pike, via S29/S3 | abstract via S29 |
| f_m | 0.6 | S29 (secondary / assumed) | via S3 |
| Available muscle power | 142.7 W kg⁻¹ | Wakeling & Johnston 1998, via S3 | abstract via S3 |
| Best steady fin-wing CL | 1.10 (top of 1.0–1.1) | Park & Choi IUTAM 2007, via S3-D | search-summary via S3-D. I tried to fetch the IUTAM PDF; the host did not resolve (could-not-access) |
| **Park & Choi CL reference area** | "the sum of the planform areas of the pectoral (A1) and pelvic (A2) fins and body (A3)" | Park & Choi 2010, *J Exp Biol* 213:3269, doi:10.1242/jeb.046052 | **full-text** (journals.biologists.com, this session; first ~100k of 157k characters, then the remainder queried). Table 1 is an image and not readable, so **A1/A2/A3 are `unknown`** |
| Body share of lift in Park & Choi | "less than 7%" at α ≤ 10°; "almost 20%" at α = 40° | same | full-text |
| Zebrafish wetted area | adult 777 ± 452 mm² (L 35.4 mm, m 485 mg, N = 3); 660 mm² used in their Fig 8 | McHenry & Lauder 2005, *J Exp Biol* 208:2289 | full-text (first 100k characters) |
| Body cross-section | elliptical | McHenry & Lauder 2005 (their modelling assumption) | full-text |
| **Body width/depth ratio** | **assumed** 0.4–1.0, central 0.5 | none: `unknown` | — |

**Disagreement preserved on the reference area.** A search-engine summary of the 2007 IUTAM paper
says it normalises by pectoral + pelvic fin area only (search-summary). The 2010 JEB full text
includes the body. I use the 2010 definition, because the claim names it. If the 1.0–1.1 values
come from the 2007 paper with fins-only normalisation, then crediting the body is not "consistent"
with that number. In that case the wing-only 2.16 is the right comparison.

**Search scope for the negative on zebrafish width.** I searched for a measured adult zebrafish body
width or dorsal planform area: 1 standard and 1 extended web search, plus a full-text fetch of
McHenry & Lauder 2005. A bioRxiv microCT morphometrics preprint returned HTTP 429. I found **no
measured value.** typeset.io and the monash IUTAM host did not resolve from this session.

## 3. Arithmetic

**S3 model.**
- V_to² = 2Mg / (ρ CL S_lift), with M = m_b + σS_w = 0.4 + 0.1382 × 1070e-6 kg = **0.5478 g**.
- P_muscle = V³ / (4s) / η_h × M / (f_m m_b).
- Control: CL 1.07 and S_lift = S_w give V = 2.768 m/s and P = 408.7 W kg⁻¹, which is 2.864× short.
  This reproduces S3's 409 W kg⁻¹ and 2.87×.

**Closure speed.** Set P = 142.7 W kg⁻¹:
- V_c³ = 4 s η_h f_m m_b P / M = 4 × 0.08 × 0.37 × 0.6 × 0.4e-3 × 142.7 / 0.5478e-3
- V_c = **1.949 m/s**

**Lifting area × CL needed.**
- CL·S = 2Mg / (ρ V_c²) = 2 × 0.5478e-3 × 9.81 / (1.225 × 1.949²) = **2309 mm²**
- Wing only: 2309 / 1070 = **2.158**, which matches S3-D's 2.16.

**Body planform.** The body is treated as having an elliptical cross-section (depth h, width w).
- Dorsal projection / wetted area = w / perimeter. This is 0.174, 0.206, 0.260 and 0.318 for
  w/h = 0.4, 0.5, 0.7 and 1.0 (Ramanujan perimeter).
- The wetted area was taken as 660, 777, or 683 mm². The 683 mm² is 777 × (0.40/0.485)^(2/3).
- That gives S_body = **115–247 mm²**. The central value is ~136–160 mm² at w/h 0.5. Zebrafish are
  laterally compressed, which is why I take w/h well below 1; that reading is my inference, not a
  measurement.

**CL needed** = 2309 / (1070 + S_body):

| S_body (mm²) | CL needed | Shortfall at 1.10, = (CL_needed/1.10)^1.5 | Lift margin |
|---|---|---|---|
| 115 | 1.949 | 2.36× | 1.77 |
| 141 (683 mm², w/h 0.5) | 1.907 | 2.28× | 1.73 |
| 160 (777 mm², w/h 0.5) | 1.877 | 2.23× | 1.71 |
| 210 | 1.804 | 2.10× | 1.64 |
| 247 (777 mm², circular section) | 1.753 | 2.01× | 1.59 |

**Uncertainty.**
- The bracket 1.75–1.95 spans only the body-area assumption.
- It excludes the ±58 % SD on McHenry & Lauder's wetted area (N = 3).
- It excludes the possibility that the body lifts less per unit area than the whole-fish average.
  Park & Choi's 7–20 % body share hints at this, but A3 is unknown, so I cannot test it. My
  inference is that equal-CL body credit is therefore an **upper bound** on the body's help.

## 4. Comparison with the recorded value (done after the above)

- **Recorded:** CL needed 1.76, 2.03× shortfall, ~1.6× lift margin.
- I grepped the recorded script (`S3-D-deepen_calc.py`) after deriving. It states: "Zebrafish dorsal
  planform area: unknown (no measured value found). Bracket assumed: 0, 120, 240 mm^2". It quotes
  1.76 at **240 mm²**, the top of that bracket, using the same lifting-but-massless body formulation.
- **AGREE, with a stated bias.**
  - The recorded 1.76 / 2.03× / 1.6 lies inside my bracket (1.75–1.95 / 2.01–2.36× / 1.59–1.77),
    but at its generous edge.
  - Reaching ~240 mm² from measured wetted area needs a circular cross-section and the largest
    wetted area. For a laterally compressed fish my central estimate is **1.88** (margin ~1.7×).
  - So the claim's "margin narrowed to ~1.6×" is the most generous end. "~1.6–1.8×" is the fairer
    statement.
  - The verdict, that the power budget does not close on steady lift, is unchanged.
- **Not replicated:** the transient impulsive-start part of the claim (~14.5 ms, ~1 mm hop). I found
  no read-level source for a transient CL value and did not attempt it.
- **Independence caveat:** the body formulation (extra lifting area at the same CL, no added mass)
  is the obvious one, and the recorded script uses it too. The independent element is the body-area
  input. That input was assumed in the recorded work and derived here from measured wetted area,
  with an assumed cross-section.

```swarm-replication
{"claim_id": 297, "my_value": "CL needed ~1.88 (bracket 1.75-1.95) with body planform lift; 2.23x (2.01-2.36x) power shortfall at CL 1.10; wing-only baseline 2.158", "agrees": true,
  "note": "The recorded 1.76 sits at the generous edge of my bracket: it needs a ~240 mm2 body planform, which measured zebrafish wetted area (McHenry & Lauder 2005) only reaches with a circular cross-section, so the margin is better stated as ~1.6-1.8x; the verdict that the power budget does not close stands, and the transient-lift hop was not replicated."}
```
