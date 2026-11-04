# Challenge 294: adversarial review of S32-D-D (body drag coefficient Cd_b)

**Claim under review.** Claim 294, from `harvest:deepen-s32-sensitive-input-sy9vpn`. The document is `origin/claude/deepen-s32-sensitive-input-sy9vpn:docs/research/fish/S32-D-deepen.md`; I read it and its script in full. The claim:

> After U_b, S32-D's threshold is most sensitive to Cd_b. Replacing S32's assumed 0.1–0.3 (frontal) with the only zebrafish measurement (McHenry & Lauder 2005, C_inert ~0.024 wetted, i.e. ~0.45 frontal) lowers the threshold to 1.64 / 1.72 m/s (GEN/CEN). A swimming-drag increase of only ×1.12 / ×1.24 over coasting then flips the result at the Demesmay mean C-start speed, so S32-D's claim that the negative holds at every mean input **falls**.

**Verdict: WEAKENED.**
- The arithmetic is correct. I reproduced it with independent code.
- The verdict "falls" does not follow from the evidence. It needs two things that are not measured:
  1. Transferring a routine-coasting drag coefficient, unchanged, to a Reynolds number that is probably several times higher. The authors' own companion paper says this coefficient falls with adult size.
  2. An undulation drag multiplier that exists only at search-summary level.
- With the measured coefficient taken at face value, S32-D's negative still holds at the mean inputs.

---

## 1. Independent arithmetic (calculated)

I re-implemented S32's taxi force model in `docs/research/fish/challenge-294_indep.py`. I wrote it from the equations stated in `S32_taxi.py` and `S32-deepen_calc.py`. It does not import them. All values below are **calculated**, not observed.

| Quantity | Claim | My recomputation |
|---|---|---|
| Baseline threshold U_b*, GEN / CEN | 1.94 / 2.36 m/s | 1.937 / 2.363 |
| Cd_b ×2 → threshold, GEN / CEN | 1.46 / 1.81 | 1.464 / 1.808 |
| Spheroid wetted/frontal ratio (30 mm, 24 mm², circular section) | 17.3 | 17.30 (S_wet 415 mm²) |
| 0.024 × ratio 15 / 18.9 / 20 | 0.36 / 0.45 / 0.48 | 0.360 / 0.454 / 0.480 |
| Threshold at Cd_front 0.45, GEN / CEN | 1.64 / 1.72 | 1.646 / 1.722 |
| U_eq/V_to at U_b 1.57, Cd 0.45, GEN / CEN | 0.94 / 0.89 | 0.942 / 0.890 |
| Cd_front needed to flip at U_b 1.57, GEN / CEN | 0.50 / 0.56 | 0.505 / 0.561 |
| Multiplier on 0.454 needed to flip, GEN / CEN | ×1.12 / ×1.24 | ×1.11 / ×1.24 |
| Flume branch, GEN, Cd ×5 (U_b 0.39 / 0.54) | ≤ 0.59 | 0.387 / 0.595 |
| Bluegill (0.0154 × 18.9 = 0.29) threshold, GEN / CEN | 1.96 / 2.05 | 1.960 / 2.053 |

**No arithmetic error found.**

One internal inconsistency, which I infer from the author's own inputs:
- The 30 mm × 24 mm² spheroid used for the area conversion has a volume of 480 mm³, i.e. about 0.48–0.50 g.
- The design mass it is paired with is 0.25 g.
- This does not change the conversion much, because the conversion uses a real fish's drag area. But the body shape is not self-consistent with the design.

## 2. Proxy: a routine-coasting coefficient stands in for drag at a C-start peak

**What the calculation needs.** It needs the drag area Cd·A of an adult zebrafish at the calibration instant: Re ≈ U·L/ν = 1.57 × 0.030 / 1e-6 ≈ **47,000** (calculated).

**What the claim uses.** C_inert ≈ 0.024. Read from the McHenry & Lauder 2005 abstract (read-level: **abstract**, Europe PMC):
- adults coast "at relatively high Reynolds numbers (Re > 1000)";
- C_inert comes from "in vivo drag measurements".

The companion paper fills in more. **McHenry & Lauder 2006**, *J Morphol* 267:1099, doi:10.1002/jmor.10462, "Ontogeny of form and function: locomotor morphology and drag in zebrafish" (read-level: **abstract**, Europe PMC):
- its drag coefficients were "calculated from high-speed video recordings of **routine swimming**";
- "the **inertial drag coefficient decreased** at a comparable rate in adults" as they grew.

**Hidden assumption 1: C_inert does not depend on Re between McHenry's adults and Re 47,000.**
- The author's claim calls this "the authors' claim of a constant-coefficient inertial regime". The 2005 abstract supports only that drag ∝ U² above Re 1000.
- The 2006 abstract says, in the authors' words, that C_inert is **not** constant across adult size.
- My inference: routine coasting of a ~30 mm adult is far slower than a 1.57 m/s escape peak. So McHenry's measurement Re is very likely well below 47,000. The actual value is `unknown`, because I could not read the full texts.

**Relaxing the assumption.** Calculated in script §Re-transfer, with the coefficient scaled from Re_M to 47,100:

| McHenry measurement Re_M (unknown, swept) | Cd_front at Re 47k, Re^−0.2 / Re^−0.5 | Multiplier needed to flip, GEN (Re^−0.2 / Re^−0.5) | Multiplier needed to flip, CEN (Re^−0.2 / Re^−0.5) |
|---|---|---|---|
| 47,100 (claim's implicit case) | 0.454 / 0.454 | ×1.11 / ×1.11 | ×1.24 / ×1.24 |
| 20,000 | 0.382 / 0.296 | ×1.32 / ×1.71 | ×1.47 / ×1.90 |
| 10,000 | 0.333 / 0.209 | ×1.52 / ×2.42 | ×1.69 / ×2.69 |
| 5,000 | 0.290 / 0.148 | ×1.74 / ×3.42 | ×1.94 / ×3.80 |
| 2,000 | 0.241 / 0.093 | ×2.09 / ×5.40 | ×2.33 / ×6.01 |

**What this shows.**
- If McHenry's adults coasted at Re ≲ 10,000, the coefficient falls back to S32's own range (0.09–0.33) at the design Re.
- The undulation multiplier needed then rises from ×1.1–1.2 to ×1.5–6.
- That is at or beyond the top of the "+20% to +60%" range the claim relies on. Even that range is friction-only and search-summary-level.
- Re^−0.2 (turbulent plate) and Re^−0.5 (laminar plate) are assumed scalings, not measured for zebrafish. I give them as a bracket, not a value.
- The 2006 abstract confirms the **direction**: the coefficient falls with adult size. The magnitude is `unknown`.

## 3. Hidden assumption 2: the flip needs an unmeasured multiplier

At face value, with McHenry central 0.45 and no multiplier, my recomputation gives U_eq/V_to = **0.94 (GEN) / 0.89 (CEN)** at the Demesmay mean U_b. That is **below 1**. So at the measured mean inputs, S32-D's negative still holds, with a 4% / 9% margin on the threshold.

The claim's "falls" therefore rests on the swimming-drag multiplier. Its sources, at the read-levels the author states:
- Li et al. 2021 (full-text but CFD, simulated): qualitative only, no factor.
- +20% / ≤ +60% / Lighthill ×3–5: **search-summary**, primaries not read, friction component only.

The author's own §3.3 says the sign of the error from applying those friction factors to total drag is `unknown`.

A verdict of "falls" built on a search-summary multiplier overstates the evidence. The honest status of S32-D is **undetermined at mean inputs**, not fallen. The author's body text actually says this ("downgraded to undetermined"), but the headline claim says "falls".

## 4. Evidence level and wording

- **"Simulated", value n/a.** Acceptable. The numbers are calculated from a model, and the claim does not present them as observed.
- **"The only zebrafish measurement" is wrong as worded.** McHenry & Lauder 2006 is a second published zebrafish drag-coefficient study. It may share data with 2005. The author named it in §3.1 only as a possible source of wetted area and did not read it. Its abstract bears directly on the coefficient.
- **"C_inert ~0.024 wetted" is stated as fact.** The author's own document puts the wetted-area basis at search-summary level.
  - Partial support: **Lei et al. 2022**, PLoS ONE, PMC9312365 (read-level: **full-text**), on the cyprinid *Sinocyclocheilus*. It cites McHenry & Lauder 2005/2006 for its added-mass coefficient, and fits coasting with a ½ρ·C_d·A form in which A is "the fish's surface area".
  - That is that paper's definition, not proof of McHenry's. The ½ and the area basis of C_inert remain `unknown` to me.
  - Its own measured coasting C_d,coast was 0.09 ± 0.01 at Re ≈ 1,280 (authors' value). That is a different species and an Re far below the design value, so I do not use it numerically.

## 5. Counter-examples and regimes

- **Bluegill** (Tandler et al. 2019, Re-matched, the author's source at abstract level) leaves S32-D standing (threshold 1.96 m/s). The author preserved this.
- **Zebrafish's own ontogenetic trend** (McHenry & Lauder 2006, abstract): C_inert falls with adult size. This points the same way as the Re-matched bluegill value, not as the claim's central reading.
- **Sources still disagree, and I do not average them.**
  - McHenry face-value (0.45, Re of measurement unknown) gives a flip only with a multiplier of ≥ ×1.11–1.24.
  - Re-corrected McHenry or Tandler gives S32-D standing unless the multiplier is ≥ ×1.5–6.
- **Repeated-stroke (flume) branch.** I confirm the claim: this branch stalls under every drag value (≤ 0.60 of V_to, even at ×5).

## 6. Searches and scope

- **Europe PMC REST:**
  - `EXT_ID:15939771` (McHenry & Lauder 2005 abstract)
  - `DOI:10.1002/jmor.10462` (McHenry & Lauder 2006 abstract)
  - `(REF:"coasting in zebrafish") AND OPEN_ACCESS:y` (13 hits; full texts pulled for PMC11930232, PMC7809443 and PMC9312365, and grepped for drag values, "McHenry", "0.024" and "wetted")
  - `"C_inert" OR "Cinert"` (15 hits; only the 2005 paper relevant)
  - `zebrafish AND drag AND (towed OR "dead drag" OR "drag force") AND adult` (57 hits; first 20 titles scanned; none an adult body drag measurement)
- **Result of the full-text greps.** PMC11930232 and PMC7809443 gave no drag-coefficient value or C_inert definition. PMC9312365 is the source used in §4.
- **Full text of McHenry & Lauder 2005:** could-not-access. doi.org and journals.biologists.com returned a Cloudflare 403; Unpaywall and Semantic Scholar were blocked by the proxy (403).
- **McHenry & Lauder 2006:** abstract only.
- **Negative finding, within this scope:** I found no source giving the Reynolds number or speed of McHenry & Lauder's adult in-vivo coasting measurements. Their Re is therefore `unknown`, and §2 sweeps it rather than fixing it.

## 7. Sources and read-levels

| Source | Read-level |
|---|---|
| S32-D-deepen.md, S32-D-deepen_calc.py, S32-deepen_calc.py, S32_taxi.py (claim branch) | full-text (repository) |
| McHenry & Lauder 2005, *J Exp Biol* 208:2289, doi:10.1242/jeb.01642 | abstract; full text could-not-access |
| McHenry & Lauder 2006, *J Morphol* 267:1099, doi:10.1002/jmor.10462 | abstract |
| Lei, Xu, Ji, Rose, Zakirov & Bisset 2022, PLoS ONE, doi:10.1371/journal.pone.0270967, PMC9312365 (*Sinocyclocheilus* coasting C_d) | full-text (Europe PMC XML) |
| Tandler et al. 2019; Li et al. 2021; undulation-multiplier sources | not re-read; taken at the author's stated read-levels |

```swarm-challenge
{"claim_id": 294, "outcome": "weakened", "reason": "Arithmetic reproduces exactly, but at the measured McHenry value S32-D's negative still holds at the mean inputs (U_eq/V_to 0.94 GEN / 0.89 CEN at U_b 1.57 m/s); the 'falls' verdict needs an unmeasured, search-summary undulation multiplier, and it assumes the routine-coasting C_inert carries over unchanged to Re ~47,000, which McHenry & Lauder 2006 (abstract) contradicts by reporting that the adult inertial coefficient falls with size. Moving the coefficient from a measurement Re of 2,000-10,000 raises the multiplier needed to flip from x1.11-1.24 to x1.5-6.", "corrected_value": "S32-D status undetermined at mean inputs, not fallen. Face-value Cd_front 0.45 gives a threshold of 1.65 / 1.72 m/s, above the 1.57 m/s mean; a flip needs a drag multiplier of >= x1.11 (GEN) / x1.24 (CEN) if C_inert is Re-invariant, and >= x1.5-5.4 (GEN) / x1.7-6.0 (CEN) if McHenry's Re was 2,000-10,000 and Cd scales as Re^-0.2 to Re^-0.5", "depends_on": ["S32 / S32-D force model as coded in S32_taxi.py and S32-deepen_calc.py (independently re-implemented in challenge-294_indep.py)", "Demesmay et al. 2025 C-start mean 1.57 m/s (via S32-D)", "McHenry & Lauder 2005 C_inert ~0.024, adults Re > 1000 (abstract)", "McHenry & Lauder 2006 abstract: drag coefficients from routine swimming; adult inertial drag coefficient decreases with growth", "inference: McHenry adult routine-coasting Re well below 47,000 (actual Re unknown, swept 2,000-47,100)", "assumed Re scaling of a streamlined-body Cd, Re^-0.2 to Re^-0.5 (flat-plate theory, not measured for zebrafish)", "wetted/frontal ratio 15-20 (author's calculated spheroid)", "undulation multiplier sources at search-summary level (author's section 3.3)", "Tandler et al. 2019 bluegill 0.0154 at Re 41k (author's abstract read)"]}
```
