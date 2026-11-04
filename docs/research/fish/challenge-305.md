# Challenge 305: adversarial review of S32-D-D ("S32-D falls on body Cd")

**Claim under review** (claim 305, author's, branch `origin/claude/deepen-s32-sensitive-input-sy9vpn`, `S32-D-deepen.md`):
the most sensitive input after U_b is the assumed body drag coefficient Cd_b. Replacing S32's assumed 0.1–0.3 (frontal) with McHenry & Lauder 2005's zebrafish C_inert ≈ 0.024 (wetted), which is about 0.45 on frontal area, lowers S32-D's threshold to 1.64 / 1.72 m/s (GENEROUS / CENTRAL). On that basis, a swimming-drag increase of only ×1.12 / ×1.24 flips S32-D at the Demesmay mean C-start speed. Recorded level: derived; value 1.64 m/s.

**Verdict: WEAKENED.** All of the arithmetic reproduces. But the "only ×1.12 / ×1.24" margin depends on one assumption that was never tested: that McHenry's coefficient is independent of Reynolds number from his (unknown) adult coasting Re up to the design Re of 47,100. If that assumption is relaxed using flat-plate scaling, the margin S32-D claimed largely comes back.

**Status of every number below:** *calculated* by `docs/research/fish/challenge-305_check.py` (`python3 -I challenge-305_check.py`, under 5 s). That script imports only S32-D's force model, `S32-deepen_calc.py`, copied unchanged from the author's branch. The threshold search and the Re sweep are my own code. I did not run the author's `S32-D-deepen_calc.py`. **Nothing here is a measurement.**

## 1. Independent arithmetic

Method (mine, not the author's). In S32's force model, U_b and Cd_b enter only through the calibration constant G = (Cd_b·A/S_fin + C_D(U_b))·U_b². So I first solve, by bisection, for the G* at which U_eq = V_to. I then invert G* for U_b at each Cd_b, using S32's Re-scaled foil C_D.

Results:

| Quantity | Author | Mine (calculated) |
|---|---|---|
| G* GEN / CEN | not stated | 0.987 / 1.076 m²/s² |
| Threshold at S32's Cd_b (0.3 / 0.2) | 1.94 / 2.36 | 1.94 / 2.36 |
| Threshold at Cd_b ×2 | 1.46 / 1.81 | 1.46 / 1.81 |
| Wetted/frontal ratio, prolate spheroid of 30 mm, 24 mm² | 17.3 | 17.3 (S_wet 415 mm²) |
| Threshold at 0.024 × 15 / 18.9 / 20 | 1.64 central (GEN), 1.72 (CEN) | GEN 1.80 / 1.64 / 1.60; CEN 1.89 / 1.72 / 1.68 |
| Multiplier on 0.454 needed to flip at U_b 1.57 | ×1.12 / ×1.24 | ×1.11 / ×1.24 |

**The arithmetic survives.** The author's "0.36–0.48 reproduces 1.64 / 1.72" holds only at the central ratio of 18.9. At ratio 15 the threshold is 1.80 m/s (GEN). The headline gives the central value without stating this band.

## 2. The proxy

There are two proxy steps, and the author names both:
- A coasting coefficient stands in for the drag on a body that is bent at a C-start peak.
- A C-start peak speed stands in for a stroke-averaged burst speed.

I add one point to the second. S32-D's own table includes the **Demesmay 40-ms mean, 0.95 m/s** (inherited from S32-D at full-text; I did not re-read it). That window is closer to the ~1-s stroke-averaged quantity than the instantaneous peak is. At 0.95 m/s, McHenry's coefficient needs a ×3.5 (GEN) or ×3.9 (CEN) swimming-drag increase to flip the result (calculated). That is Lighthill-scale, not +20%. The author's "feasibility NOT established" already covers this direction, so I do not count it against the claim. I record it because "flips at the Demesmay mean" holds only for the peak statistic.

## 3. The hidden assumption: Re-invariance of C_inert

The claim carries McHenry's adult value of 0.024 unchanged to the design condition. At U_b = 1.57 m/s and 30 mm length, that condition is **Re = 47,100** (calculated).

- **What the abstract says** (McHenry & Lauder 2005, read-level **abstract**, Europe PMC, retrieved this session): "Measurements of drag on tethered dead fish suggest that adult fish operate in an inertial regime by coasting at relatively high Reynolds numbers (Re > 1000), and in vivo drag measurements showed adults to operate with a drag coefficient (Cinert approximately 0.024)".
- **My inference:** "inertial regime" in that abstract contrasts drag ∝ U² with the viscous regime at Re < 300. The abstract does **not** state that the coefficient stays constant up to Re ≈ 5×10⁴. The author's §3.2 paraphrase, "authors claim an inertial, constant-coefficient regime above Re 1000", is therefore stronger than the text I could read.
- **McHenry's adult coasting Re is `unknown`.** It is not in the abstract. Full text could-not-access: `journals.biologists.com` returned 403, and `jeb.biologists.org` and `api.semanticscholar.org` were refused by the proxy. These were the only attempts.

**Relaxing the assumption** (calculated). Scale C ∝ Re^(−n) from an assumed McHenry Re, Re_M, to 47,100 at wetted/frontal ratio 18.9. The two exponents are the flat-plate bounds the author already uses in §3.2. The Re_M values are a sweep, not data.

| n | Re_M | Cd_front | Threshold GEN / CEN (m/s) | Multiplier to flip at 1.57, GEN / CEN |
|---|---|---|---|---|
| 0 (author) | any | 0.454 | 1.64 / 1.72 | ×1.11 / ×1.24 |
| 0.2 (turbulent) | 20,000 | 0.382 | 1.76 / 1.84 | ×1.32 / ×1.47 |
| 0.2 | 10,000 | 0.333 | 1.86 / 1.95 | ×1.52 / ×1.69 |
| 0.2 | 3,000 | 0.262 | 2.04 / 2.14 | ×1.93 / ×2.15 |
| 0.5 (laminar) | 10,000 | 0.209 | 2.22 / 2.33 | ×2.42 / ×2.69 |
| 0.5 | 3,000 | 0.114 | 2.71 / 2.85 | ×4.41 / ×4.90 |

**Reading this.**
- The author's ×1.12 is the value at the **extreme** of this sweep, which requires Re_M ≥ 47,100. That would mean adult zebrafish were coasting at about 1.5 m/s at 30 mm, or at a correspondingly lower speed if they were longer. I have no evidence on this either way (`unknown`).
- At any Re_M ≤ 20,000 with even the weakest exponent (0.2), the required swimming increase is ≥ ×1.32 (GEN) or ×1.47 (CEN). That is no longer "only" a few percent. It sits in the middle or top of the author's own search-summary range of +20% to +60%.
- With n = 0.5 and Re_M ≤ 10,000, the threshold is 2.2–2.7 m/s. S32-D then stands with more margin than it originally claimed.
- This direction agrees with the source the author set aside. Tandler 2019 (bluegill, Re-matched, abstract) gives Cd_front 0.29, which lies inside the n = 0.2, Re_M ≈ 3,000–10,000 rows above.

The author did note an Re^(−½) caveat (§3.2, giving about 0.19 frontal at Re 5–10k), but treated it as secondary because of the "constant-coefficient claim". The abstract does not support that claim as worded. So the caveat should carry equal weight with the central reading, and the headline should not state ×1.12 without it.

## 4. Evidence level

"Derived" is honest. The thresholds are calculated, and the author says so.

One wording defect in the claim string: "C_inert ~0.024 **wetted**" is stated flatly. The author's own document puts the wetted-area basis at **search-summary** and the factor ½ at `unknown`. If the basis were volume^(2/3), my calculation for the same spheroid (V = 480 mm³, V^(2/3) = 61 mm², ratio about 2.5) gives Cd_front ≈ 0.06, and S32-D would stand easily. My inference is that the value "consistent with previously published estimates" fits wetted-area fish values of about 0.01–0.03 better than the alternatives, so wetted is the likely basis. It is still unverified, and the claim string should say so.

## 5. Counter-examples and regimes

- **Tandler 2019 (bluegill):** already preserved by the author as a disagreement. Section 3 shows it is what McHenry's own value turns into under ordinary Re scaling, so the two are not necessarily in conflict.
- **No published adult zebrafish drag at Re ≈ 4–5×10⁴ was found.** Scope: Europe PMC abstract record for PMID 15939771 and the three full-text URLs listed above. I ran no new literature search beyond the author's §6. Searches by the author that I did not repeat: their Europe PMC queries.

## 6. What survives and what does not

- **Survives:** every number in the claim, recomputed independently. Cd_b's rank as the most sensitive non-design input after U_b. "Feasibility NOT established". The disagreement with claim 299 *conditional on* Re-invariance.
- **Does not survive as stated:** "a swimming-drag increase of **only** ×1.12 / ×1.24 flips the result". Corrected: ×1.11–×1.24 if C_inert is Re-invariant up to Re 47,100. Otherwise ×1.3–×4.9 across Re_M 3,000–20,000 and exponents 0.2–0.5. The GENEROUS threshold is **1.64–2.71 m/s**, not 1.64 m/s.
- **Effect on S32-D (claim 299):** it is neither restored nor refuted. Whether it stands is decided by two inputs nobody has: McHenry's adult coasting Re (and full-text definition of C_inert) and the swimming-drag multiplier. The cheapest decisive action is the one the author already names: read McHenry & Lauder 2005 in full. The same reading would also settle the Re question.

```swarm-challenge
{"claim_id": 305, "outcome": "weakened", "reason": "All arithmetic reproduces (thresholds 1.64/1.72 m/s, flip multipliers x1.11/x1.24), but these rest on carrying McHenry & Lauder's C_inert 0.024 unchanged from an unknown adult coasting Re to the design Re 47,100, which the abstract does not support; under flat-plate Re^-0.2 to Re^-0.5 scaling from Re_M 3,000-20,000 the GENEROUS threshold is 1.76-2.71 m/s and the swimming-drag multiplier needed to flip at 1.57 m/s is x1.3-x4.4, so 'only x1.12' is the extreme case, not the central one.", "corrected_value": "GENEROUS threshold 1.64-2.71 m/s (1.64 only if C_inert is Re-invariant to Re 47,100); flip multiplier at U_b 1.57 m/s x1.11-x4.4 (GEN), x1.24-x4.9 (CEN)", "depends_on": ["S32-D force model S32-deepen_calc.py (copied unchanged from origin/claude/deepen-s32-sensitive-input-sy9vpn), GENEROUS/CENTRAL scenarios", "McHenry & Lauder 2005 J Exp Biol 208:2289 abstract: C_inert ~0.024, inertial regime Re > 1000 (read-level abstract); adult coasting Re unknown; full text could-not-access", "C_inert area basis = wetted (search-summary via author, unverified) and factor 1/2 (unknown)", "flat-plate Re scaling exponents 0.2 (turbulent) and 0.5 (laminar) as bounds on Re dependence of coasting Cd (theory, assumed applicable)", "assumed sweep of McHenry adult coasting Re_M 3,000-47,100 (not data)", "wetted/frontal ratio 15-20, central 18.9, prolate spheroid 30 mm, 24 mm2 (calculated, assumed shape)", "design Re 47,100 at U_b 1.57 m/s, L 30 mm (calculated)", "Demesmay et al. 2025 C-start control mean 1.57 m/s and 40-ms mean 0.95 m/s (inherited from S32-D at full-text, not re-read)", "Tandler et al. 2019 bluegill coasting Cd 0.0154 at Re 41k (abstract, via author)"]}
```
