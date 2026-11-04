# Challenge 195: "Pectoral fin AREA in the Daane double het is the cheapest decisive measurement"

**Claim under review** (S28-organism.md §4 item 1 and the summary line, branch `origin/claude/s28-organism-design-5z0vjz`; read-level: full-text):
"CHEAPEST DECISIVE MEASUREMENT: pectoral fin AREA in the existing Daane double heterozygote. Daane et al. measured fin LENGTH only and never reported area, so the animal exists and the measurement does not. It decides whether even the small phenotype is detectable."
Recorded evidence level: derived. Value: n/a.

**Verdict: WEAKENED.** Both factual premises survive: the main text reports length only, and the line exists. "Decisive" does not survive as stated. Fin area can close the line, but it cannot open it. Exit speed, which is also unmeasured, moves the detectable lift more than area does.

## Sources and read-levels

| Source | Read-level | What I used |
|---|---|---|
| S28-organism.md (project) | full-text | the claim, inputs, and decision rule |
| Daane et al. 2021, *Curr. Biol.* 31:5052, PMC9172250 (author manuscript) | full-text of the main text, read through a fetch-and-summarise tool, so not line by line. **The supplementary PDF was not read.** | which measurements were made; allele availability |
| ZFIN figure records ZDB-FIG-221222-35 and the publication ZDB-PUB-210918-31 | search-summary (the fetch returned 503 or failed DNS) | Fig. 4 caption: "pectoral fin length ... normalized to standard length" |
| Stewart et al. 2021, *Development* (longfin = cis-ectopic kcnh2a) | search-summary | checked whether any study measured pectoral area in *lof* fish |

## 1. Premise check: did Daane measure only length?

**Survives, within scope.** In the main text I read (author's statement, as reported by the summariser):
- Fig. 4A brackets the "length of pectoral fin" in *lat4a^nr21/+ ; kcnh2a^lof/+* fish.
- Fig. 4B and 4C give "length normalized by SL".
- Fig. S2 reports segment length.

Ray number, fin width and fin area do not appear in the main text.

**Scope of this negative search:**
- Covered: the main text, figure legends and key-resources table of PMC9172250, plus one web search for pectoral fin area in *longfin*/*kcnh2a* fish. That search found only caudal-fin quantification and one qualitative pectoral image (Stewart 2021).
- Not covered: the supplementary PDF (Data S1, Fig. S2 panels).

Within that scope I found no fin area.

## 2. Arithmetic, redone independently

These are calculated values, not observations. The formula is L/W = ½ρV²·S·CL/W, with ρ = 1.225 kg m⁻³, CL = 1.07, W = 2.45e-3 N. All three inputs are taken from S28; W rests on S28's assumed 0.25 g mass.

| S (mm²) | V = 0.45 m/s | V = 0.90 m/s | V = 1.38 m/s |
|---|---|---|---|
| 57 (case A) | 0.31 % | 1.24 % | 2.90 % |
| 60 (rule threshold) | 0.33 % | 1.30 % | 3.06 % |
| 125 (case B) | 0.68 % | 2.71 % | 6.37 % |
| 192 (case C) | 1.04 % | 4.16 % | 9.78 % |

- The author's decision rule is "S ≤ ~60 → ≤ 3 % W; S ≥ ~190 → 10 % W". It reproduces at V = 1.38 m/s. The ≤ 3 % figure is very slightly loose: 60 mm² gives 3.06 %. That slip is immaterial.
- "Flying would need 1925 mm²": I get 192 × (4.37/1.38)² = 1925 mm². This reproduces.

## 3. The variable that carries the result is not area

**Inference (mine):** the decision rule is evaluated only at V = 1.38 m/s. That is the *maximum* measured *swimming* burst (Miln 2021). S28 itself states that exit speed is unmeasured and its prior is "exit ≤ burst".

Over the plausible ranges, the two unknowns move lift by different amounts:

| Unknown | Range | Factor on lift |
|---|---|---|
| Area | 57–192 mm² | 192/57 = **3.4×** |
| Exit speed | 0.45–1.38 m/s | (1.38/0.45)² = **9.4×** |

Relax the hidden assumption that V_exit = 1.38 m/s:
- At a mid-range exit of 0.9 m/s, even the most generous area (case C) gives 4.2 % W.
- At 0.45 m/s, case C gives 1.0 % W.

So an area result of S ≥ 190 mm² does **not** establish that the phenotype is detectable. Exit speed decides that at least as much, and the author ranks exit speed separately as item 2.

## 4. Proxy

The quantity that matters is the **effective lifting area times CL as deployed during the leap**: spread angle, angle of attack, camber, and fin flexibility at Re ≈ 500.

The proposed measurement is the static area of an anaesthetised fin spread by hand, which is a proxy for that quantity. S28 §3.6 itself says "whether [the fish] spreads its pectorals during the leap ... has never been observed." S28 §4 item 3 says ray stiffness may stop case-C lift from being realised.

So a large static area is necessary but not sufficient. A small static area is close to sufficient for a negative result.

**Conclusion (inference):** the measurement is decisive in **one direction only**. If S ≤ ~60 mm², it closes the line robustly, because lift is then ≤ 3 % W even at the best-case speed. If S is large, it decides nothing on its own.

## 5. No detection threshold is defined

"Decides whether the phenotype is detectable" needs a detection limit, and S28 gives none. As an order of magnitude (calculated by me, not measured), take a 45° launch at 1.38 m/s:
- Ascent time is 0.0995 s.
- An extra upward acceleration of f·g over that time shifts position by ½·f·g·t²:

| Lift fraction f | Position shift |
|---|---|
| 10 % | 4.9 mm |
| 7 % | 3.4 mm |
| 3 % | 1.5 mm |
| 1 % | 0.5 mm |

Whether 1–5 mm is resolvable depends on the video and tracking setup, which is not specified. This is mm-scale on a deforming 3 cm fish. Comparing against wild-type siblings also requires their own pectoral lift, about 1 % W with 20 mm² of fin (S28's assumed wild-type area), to be subtracted.

Without a stated threshold, the 60 / 190 mm² cut-offs are judgement, not a decision boundary.

## 6. "The animal exists": cheaper than claimed only for some labs

According to the key-resources table of PMC9172250 (the authors' statement):

| Allele | Availability |
|---|---|
| *lof^dt2* | ZIRC ZL86 |
| *lof^j6e1* | ZIRC ZL1494 |
| *lat4a^nr21* | listed as "This paper", with no ZIRC accession; lines are distributed on request, and sperm was deposited with Cryogenetics |

For anyone outside the authors' lab, "hours of work" therefore becomes:
1. obtain the lines;
2. make one cross;
3. raise the fish to adulthood, roughly 3 months (general zebrafish husbandry knowledge, not from this paper).

The animal exists as a *genotype*, not necessarily as a fish on hand. It is still probably the cheapest item on S28's list, because it needs no high-speed rig.

Two further points:
- **An even cheaper first pass exists (inference):** a rough area estimate from the published Fig. 4A images. These images are uncalibrated, and the fins may not be spread. I did not do this measurement, so I give no value.
- **The evidence level is honest:** "derived" with "n/a" is the right label for a recommendation built on calculated lift fractions. The claim does not present anything as measured.

## 7. Corrected statement

> Pectoral fin area in the Daane *lat4a^nr21/+ ; kcnh2a^lof/+* fish is unmeasured: Daane 2021 reports length/SL only (main text read; supplement unread). Measuring it is cheap if the line is on hand, or about one generation if not. It is a **one-sided** test. S ≤ ~60 mm² closes the aerodynamic-phenotype line (≤ 3 % W even at 1.38 m/s). S ≥ ~190 mm² does not establish detectability, because the lift fraction scales with V_exit², which is unmeasured and spans a 9.4× range, and because the fish may not deploy its pectoral fins during a leap. To decide detectability, measure area *together with* water-exit speed and fin deployment in filmed leaps.

```swarm-challenge
{"claim_id": 195, "outcome": "weakened", "reason": "The premises hold (Daane 2021 main text reports pectoral length/SL only; the alleles exist), but static fin area is a one-sided proxy: it can close the line if S <= ~60 mm2, yet cannot establish detectability, because lift scales with the unmeasured exit speed squared (9.4x range vs 3.4x for area) and with unobserved in-leap fin deployment, and no detection threshold is defined.",
  "corrected_value": null,
  "depends_on": ["S28-organism.md decision rule and inputs (rho 1.225, CL_max 1.07, W 2.45e-3 N from assumed 0.25 g)", "Miln2021-burst 0.45-1.38 m/s (swimming burst, not exit speed)", "Daane2021 PMC9172250 main text: fin length/SL only, supplement unread", "Daane2021 key resources table: nr21 'This paper' / lof at ZIRC ZL86, ZL1494", "S28 section 3.6: pectoral spreading during leap never observed"]}
```
