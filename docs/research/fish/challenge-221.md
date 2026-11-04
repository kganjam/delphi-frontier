# Challenge 221: adversarial review of the harvester note on S7-D-D ("girdle bone probably not limiting" FALLS)

Date: 2026-11-04.

**Claim under review.** This is a harvester's note about S7-D-D, not S7-D-D itself:

> "Required d = 0.2600 mm at 62.6 MPa reproduces; but the stated '~4x yield' is NOT reproduced: sigma/yield = 2.2x at d=0.20 and 10.2x at d=0.12 (solid circular section)."

- Recorded evidence level: derived. Value: 0.26 mm required solid-equivalent diameter.
- Source: branch `claude/s7-d-sensitive-input-n67r40`, `docs/research/fish/S7-D-deepen.md` and `S7-D-deepen.py`. I read both in full (read-level: full-text, repository file).

**Verdict: WEAKENED.**
- The 0.26 mm number survives.
- The note's central objection, "~4× NOT reproduced", is wrong. It compares the author's mid-geometry figure with values computed at the rounded ends of the range.
- The note also labels a calculated quantity as "measured".

## 1. Independent arithmetic

Everything in this section is a **calculation** of mine, done in a fresh Python one-liner. I did not run the author's script.

### Inputs

All inputs are as stated in the claim and the source. They are assumptions or search-summary values; none are measurements of mine.

- m = 0.4 g, so W = 3.924 mN
- ρ = 1.2 kg m⁻³
- V = 3 m/s, n = 3, C_L = 0.78, AR = 9
- body half-width 2.5 mm
- elliptic loading, so the centroid sits at 4/(3π) of the semispan
- σ_y = 62.6 MPa

### Required section

| Step | Result (calculated) |
|---|---|
| Wing area S = 2W/(ρV²C_L) | 9.316×10⁻⁴ m² |
| Span b = √(AR·S) | 91.6 mm |
| Exposed semispan s = b/2 − 2.5 mm | 43.3 mm |
| Root moment M = n·(W/2)·(4/3π)·s | **1.081×10⁻⁴ N·m**, which reproduces S7 |
| Required section modulus Z_req = M/σ_y | 1.727×10⁻³ mm³ |
| Required diameter d_req = (32 Z_req/π)^(1/3) | **0.2601 mm**, which reproduces |

### Stress over yield

For a solid circular section, σ/σ_y = (d_req/d)³. All values below are calculated.

| d (mm) | σ/σ_y | Note |
|---|---|---|
| 0.20 (rounded upper end) | 2.20 | matches the harvester |
| 0.195 (author's actual "high") | 2.37 | author: 2.4 |
| **0.163 (author's "mid")** | **4.06** | **author: "~4×"** |
| 0.123 (author's actual "low") | 9.45 | author: 9 |
| 0.12 (rounded lower end) | 10.18 | matches the harvester |

The same result follows straight from the author's plate geometry, Z = Σw·h²/6. The ratio is Z_req/Z, calculated:

| Geometry | Ratio Z_req/Z |
|---|---|
| low (0.36 mm, 55 µm) | 9.5 |
| mid (0.40 mm, 80 µm) | 4.05 |
| high (0.44 mm, 100 µm) | 2.36 |

**Finding 1: the "NOT reproduced" objection fails.**

- S7-D-D §4b states "about **4×** its yield stress (**mid geometry**; 2.4–9× across the bracket)". The "~4×" is explicitly the mid value, and it reproduces at 4.06×.
- The harvester's 2.2× and 10.2× are correct arithmetic for d = 0.20 and d = 0.12 mm. But those are the rounded bracket ends, not the figure the author attached "~4×" to.
- They also differ from the author's 2.4× and 9× only because 0.195 was rounded to 0.20 and 0.123 to 0.12. Cubing amplifies a 2–3% rounding of d into 7–8% in the ratio.
- **There is no numerical disagreement between the author and the harvester.** One compared a mid value with the endpoints of the range.

## 2. Proxy check

The note says "measured proximal-radial solid-equivalent section 0.12–0.20 mm". The solid-equivalent d is **not measured**.

- The image measurements in S7-D-D are the silhouette quantities Σw (0.36–0.44 mm) and h (55–100 µm), taken from Ishizaka 2024 Movie S4 by the S7-D-D author.
- d_eq is **calculated** from them. The calculation assumes four plates bending independently, out of plane, as solid rectangles with the foramina ignored.
- The source document gets this right ("Everything below is calculation"). The harvester's wording collapses that distinction. **This is an evidence-level defect in the note.** It is not an error in the number.

The proxy itself, an equal-Z solid rod, is acceptable for first-yield comparison, since it preserves Z exactly. It does not capture other failure modes:
- buckling of 55–100 µm plates;
- the stress concentrations the author notes at the foramina.

Both would make the verdict worse, not better (my inference).

## 3. Hidden assumptions, relaxed

All of these are calculations of mine.

- **Bone yield.** For the most generous geometry (high, Z = 7.33×10⁻⁴ mm³) to pass at the worst case, σ_y would need to be ≥ **147 MPa**. That is 2.36× the herring proxy. Whether zebrafish radial bone reaches that is `unknown`: I did not search for zebrafish radial bone strength. The 2× relaxation the author tested (ratio 0.49 at mid) does not rescue the result.
- **Bending direction.** S7-D-D §6 says in-plane bending raises capacity "roughly (Σw/h) ≈ 5×". That holds only if the four plates act as **one connected section**: Z = h·(Σw)²/6, giving a mid ratio of 1.24 (passes). If the four plates bend independently in-plane, Z = Σ h·wᵢ²/6. With wᵢ ≈ 0.1 mm each, the mid ratio is 0.31 (fails). So even the author's named escape route is weaker than they state. This refines S7-D-D; it does not affect the harvester's note.
- **Fish size.** The scanned SL is unknown, as the author already states. I cannot test this.

None of these overturns the 0.26 mm value, which depends only on M and σ_y.

## 4. Evidence level

- "derived" for **0.26 mm** is honest. It is a calculation from assumed and search-summary inputs. The claim's last sentence lists those inputs correctly.
- The defect is the word "measured" applied to d_eq 0.12–0.20 mm. See §2.
- I re-made no image measurements of Movie S4, and neither did the harvester. Σw and h therefore remain the S7-D-D author's single-operator silhouette measurements.

## 5. Missed regime or counter-example

- I ran no literature search for this challenge, so the scope of negative search is **none**. I cannot report a published counter-example.
- Within the source's own tables, the "falls" verdict is regime-dependent:
  - at V = 3 m/s, n = 1, the mid ratio is 0.74 (yields at 1.35×);
  - at V = 5 m/s, n = 1, it is 1.28 (passes).
- The harvester's note does not mention this, but it does not claim otherwise either.

## Summary

| Element of the claim | Status |
|---|---|
| d_req = 0.2600 mm at 62.6 MPa | **Reproduced** (0.2601 mm, calculated) |
| "~4× yield NOT reproduced" | **Wrong**: mid geometry gives 4.06× (calculated). The note compared against bracket endpoints. |
| 2.2× at d = 0.20, 10.2× at d = 0.12 | Arithmetic correct, but at the rounded endpoints. The actual endpoints give 2.37× and 9.45×, consistent with the author's "2.4–9×". |
| "measured … solid-equivalent section" | **Mislabelled**: Σw and h are image measurements; d_eq is calculated. |
| Inputs flagged as assumptions or search-summary | Correct |

```swarm-challenge
{"claim_id": 221, "outcome": "weakened", "reason": "d_req = 0.260 mm reproduces independently, but the note's 'stated ~4x yield is NOT reproduced' is wrong: the author's ~4x is explicitly the mid geometry (d = 0.163 mm) and recomputes to 4.06x, while the note's 2.2x/10.2x are the rounded bracket endpoints (actual endpoints 0.195/0.123 mm give 2.37x/9.45x, matching the author's 2.4-9x), and the note labels the calculated solid-equivalent d as 'measured'.", "corrected_value": "sigma/yield = 4.06x at mid geometry (d_eq 0.163 mm), range 2.37-9.45x (d_eq 0.195-0.123 mm); d_req 0.260 mm unchanged (all calculated)", "depends_on": ["S7: root moment 1.08e-4 N m (m = 0.4 g, V = 3 m/s assumed, n = 3 assumed, C_L = 0.78 Park & Choi 2010 search-summary, AR = 9 search-summary, elliptic loading, body half-width 2.5 mm)", "S7-D: bone yield 62.6 MPa (Fiedler 2019 herring intermuscular bone, proxy)", "S7-D-D author's image measurements of Ishizaka 2024 Movie S4: summed width 0.36/0.40/0.44 mm and plate thickness 55/80/100 um (not re-made by me)", "S7-D-D geometry model: Z = sum(w) h^2/6, four plates bending independently out of plane, solid, foramina ignored", "S7-D-D section 4b text: '~4x' stated for mid geometry, '2.4-9x' across the bracket"]}
```
