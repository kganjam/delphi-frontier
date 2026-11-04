# Replication 305: S32-D-D says S32-D's "negative STANDS at every mean input" FALLS

**Method.** I re-derived this without reading the S32-D-D write-up (`S32-D-deepen.md`) or its script (`S32-D-deepen_calc.py`). I read only the parent scripts: `S32_taxi.py` (S32) and `S32-deepen_calc.py` (S32-D), from branch `origin/claude/deepen-s32-sensitive-input-sy9vpn`. I opened the recorded document only after §1–§4 below were computed. That comparison is in §5.

**Status.** Everything in §3–§4 is **calculated**. None of it is observed. The only measured quantity I bring in is McHenry & Lauder's adult zebrafish coasting drag coefficient. All other inputs are model assumptions inherited from S32/S32-D.

**Limit on independence.** I used the *same* force model as S32-D. I executed S32-D's script, kept its definitions, and changed only Cd_b and U_b. So my threshold arithmetic is a re-run of a shared model, not an independent physics check. The independent parts are:
- my choice of input to attack;
- my literature search for Cd_b;
- my area-basis conversion;
- my reading of what "falls" means.

## 1. What S32-D claims (from its script, read-level: full-text, repository)

S32-D swept the calibration burst speed U_b with every other input held at S32's GENEROUS or CENTRAL values. It found U_eq/V_to < 1 at every measured *mean* U_b, including the Demesmay 2025 control mean of 1.57 m/s. There it gets 0.77 (GEN) and 0.60 (CEN). It flips only at U_b ≥ 1.94 m/s (GEN) or 2.36 m/s (CEN), which is mean + 1–3 SD. I reproduced all of these numbers by running the script.

S32-D's own §1–2 tables show the other uncertain fact-of-the-world input. Thrust is calibrated as G = (Cd_b·A_front/S_caudal + C_D)·U_b². The body drag coefficient Cd_b is S32's "assumed (S29)" 0.1–0.3 on 24 mm² of frontal area. Its flip factors are ×2.30 (GEN) and ×3.82 (CEN) at U_b 1.38 m/s. So the question becomes: what is a measured Cd_b, and does it flip the result at mean U_b?

## 2. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Adult zebrafish coasting drag coefficient | C_inert ≈ 0.024 | McHenry MJ & Lauder GV 2005, *J Exp Biol* 208:2289, PMID 15939771. Authors' words: "in vivo drag measurements showed adults to operate with a drag coefficient (Cinert approximately 0.024)" | **abstract** (Europe PMC REST, fetched this session). Full text: **could-not-access** (cob.silverchair.com and sites.harvard.edu do not resolve in this session; the wpmucdn mirror of McHenry & Lauder 2006 does not resolve either). |
| Reference area of C_inert | wetted area | search summary (web search) | **search-summary**. Not verified. Whether the ½ is included: `unknown`. |
| Adult wetted area used by McHenry & Lauder 2005 in simulations | 660 mm² | search summary. Body length of those adults: `unknown` | **search-summary** |
| Frontal area | 24 mm² | S28 via S32 script | listing (inherited) |
| Design standard length | 30 mm | S32-D script comments (30 mm SL) | listing (inherited, assumed) |
| U_b, mean C-start max speed | 1.57 m/s (SD 0.27) | Demesmay 2025 via S32-D script | listing (inherited; not re-read) |
| U_b, S32 input | 1.38 m/s | Miln 2021 via S32 | listing (inherited) |
| All other model inputs | GENEROUS / CENTRAL as in S32 | S32_taxi.py | full-text (repository) |

### My wetted-area conversion (calculated, assumed shape)

- **Body depth.** I assume 6 mm (0.2 SL). This is not a measurement.
- **Body width.** An elliptic section with 24 mm² frontal area gives width = 4·24/(π·6) = 5.09 mm.
- **Perimeter.** Ramanujan's formula gives 17.45 mm.
- **Body wetted area.** Perimeter × length × 0.7 (taper factor, assumed) = 17.45 × 30 × 0.7 = **367 mm²**.
- **Fins.** These add an unknown amount. The two-sided caudal area alone is 2 × 37.8 = 76 mm² under S32's assumed fin.
- **Bracket carried.** S_wet = **280 (body only, slimmer taper) / ~450 (body + fins, central) / 660 (McHenry & Lauder simulation value, size unknown) mm²**.

Cd_front = C_inert · S_wet / A_front = 0.024 × S_wet / 24 mm²:
- 0.024 × 280/24 = **0.28**
- 0.024 × 450/24 = **0.45** (central)
- 0.024 × 660/24 = **0.66**

If C_inert omits the ½, every value doubles. That is `unknown`, so I do not carry it as central.

## 3. Arithmetic

**Model.** S32-D's `ratio()` with only Cd_b and U_b overridden. All values are calculated, and V_to = 4.41 m/s at 0.25 g.

**Flip value.** Cd_b* is the Cd_b at which U_eq = V_to, found by bisection on Cd_b:

| Scenario | U_b 1.38 m/s | U_b 1.57 m/s (mean) |
|---|---|---|
| GENEROUS | Cd_b* = 0.691 | Cd_b* = **0.505** |
| CENTRAL | Cd_b* = 0.764 | Cd_b* = **0.561** |

**U_eq/V_to at the derived Cd_b values:**

| Cd_b | GEN 1.38 | GEN 1.57 | CEN 1.38 | CEN 1.57 |
|---|---|---|---|---|
| 0.28 (low) | 0.632 | 0.749 | 0.587 | 0.703 |
| **0.45 (central)** | 0.795 | **0.942** | 0.749 | **0.890** |
| 0.66 (high) | 0.975 | **1.163** | 0.922 | **1.101** |
| 1.0 (if ½ omitted, ~0.9) | 1.246 | 1.482 | 1.183 | 1.411 |

**Check on the G values.** At Cd_b 0.45, G = (0.45 × 24/37.8 + 0.08) × 1.57² = (0.2857 + 0.08) × 2.465 = 0.901 m²/s². The script prints 0.901.

## 4. My value

**At strictly mean inputs, the negative still stands, narrowly.** The inputs are zebrafish coasting C_inert 0.024 converted to a central Cd_front of 0.45, and mean U_b 1.57 m/s. That gives U_eq/V_to = **0.94 (GENEROUS) / 0.89 (CENTRAL)**, which is below 1 with a 6% / 11% margin.

**It falls within the input uncertainty.** The flip needs Cd_front ≥ **0.51 (GEN) / 0.56 (CEN)**. That is ×1.12 / ×1.25 the central value, and it lies inside my derived bracket of 0.28–0.66. The top of that bracket uses McHenry & Lauder's own 660 mm² wetted area; it flips the result at mean U_b with no swimming-drag augmentation at all.

**Value:** U_eq/V_to at mean inputs = 0.94 (+0.22 / −0.19) GEN and 0.89 (+0.21 / −0.19) CEN. The flip Cd_b is 0.51 / 0.56, against a derived Cd_b of 0.45 (0.28–0.66).

**Inference, labelled as mine.**
- S32's "GENEROUS" Cd_b of 0.3 is at the *low* end of what the one zebrafish measurement implies. It is not the generous end.
- S32-D's "every mean input" margin (77% → 94%) is much thinner than S32-D reported.
- Whether it actually falls depends on two unknowns: the ½ convention and the wetted area, and drag augmentation during undulation. All of these are unmeasured for this case.

**Negative search, scoped.** I ran 3 web searches (standard/extended) on adult zebrafish drag coefficient, frontal area and coasting.
- They found no adult zebrafish drag measured *during* a burst.
- They found no frontal-area-based Cd.
- They found no measured adult wetted area for a 30 mm fish.
- Full texts were not reachable, so the coefficient's definition is not verified.

## 5. Comparison with the recorded value (read only after §1–4)

The recorded document (`S32-D-deepen.md`) says:
- central Cd_front = 0.45 (0.36–0.48), from McHenry 0.024 × a wetted/frontal ratio of 15–20;
- flip at Cd_front ≥ 0.50 (GEN) / 0.56 (CEN) at U_b 1.57;
- U_eq/V_to = 0.94 / 0.89 at the central value;
- verdict **FALLS (scoped)**. The fall rests on a ≥ ×1.12 / ×1.24 undulation increase, which the author calls small and inside published friction-enhancement ranges.

**Numbers: AGREE.**
- The central Cd_front matches: 0.45 vs 0.45.
- The flip thresholds match: 0.505 / 0.561 vs 0.50 / 0.56.
- The ratios match: 0.942 / 0.890 vs 0.94 / 0.89.
- The flip-threshold agreement is partly guaranteed, because both derivations use S32-D's model. It is not independent evidence about the physics. The Cd_front agreement is semi-independent: we used different shape assumptions and reached the same 0.45.
- **Disagreement on range.** My upper bracket is 0.66, from McHenry & Lauder's own 660 mm² simulation wetted area (search-summary). The recorded upper bracket is 0.48. On my bracket the result flips at mean U_b with no augmentation; on the recorded bracket it needs augmentation. I keep both and do not average them.

**Verdict: CANNOT TELL.**
- Taken literally, "negative STANDS at every mean input" still holds at the central measured-coefficient input (0.94 / 0.89 < 1).
- It falls only with either:
  - an unmeasured swimming-drag multiplier (the recorded route), or
  - the upper end of the wetted-area / ½-convention uncertainty (my route).
- The recorded verdict is "FALLS (scoped)", downgrading S32-D to "undetermined". I agree with "undetermined", and I agree the margin collapsed from 23% to 6%.
- I do not find that the claim *falls* at mean inputs without adding an input that is not a measured mean. The recorded document scopes its verdict that way too ("with margin"). Whether that counts as FALLS is a judgement, not something the arithmetic settles.

```swarm-replication
{"claim_id": 305, "my_value": "U_eq/V_to = 0.94 (GEN) / 0.89 (CEN) at mean U_b 1.57 m/s with derived Cd_front 0.45 (0.28-0.66); flips at Cd_front >= 0.51 / 0.56", "agrees": null,
  "note": "Numbers agree with the recorded 0.45, 0.50/0.56 and 0.94/0.89 (shared S32-D model, so the thresholds are not independent), but at strictly mean inputs the negative still stands by 6-11%, and FALLS needs an unmeasured undulation multiplier or the upper end of the wetted-area/half-convention uncertainty, so whether it falls is a judgement I cannot confirm."}
```
