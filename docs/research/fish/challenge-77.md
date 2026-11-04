# Challenge 77: adversarial review of S10-D (pectoral-muscle fraction)

**Claim under review** (written by another agent, not by me):

> "S10-D VERDICT STRENGTHENS: the measured teleost pectoral-muscle fraction is ~1.4% of body mass for both fins (*Abudefduf saxatilis*, 0.69% per fin, Mansuit & Herrel 2021 Table 1, full text) against a computed threshold of 7.5–20%. Hover demand is 730–1950 W/kg, 5–15x above measured warm zebrafish fast muscle."

- Recorded evidence level: derived. Value: 0.014 muscle-mass fraction.
- Source file: `docs/research/fish/S10-deepen.md`, on branch `claude/deepen-s10-flapping-muscle-wr33g7`.
- My calculation script: `docs/research/fish/challenge_77_calc.py`. Every number it prints is a **calculation**.

**Outcome: SURVIVED.** The numbers reproduce and the cited table says what the claim says it does. The verdict also holds when I relax the hover assumption. The review did turn up two problems in how the claim is worded, and one result whose safety margin is thinner than its headline implies. These are set out in §2–§5.

---

## 1. Independent arithmetic

**The source table.** I downloaded the Mansuit & Herrel (2021) PDF myself from frontiersin.org and converted it with `pdftotext` (read-level: **full-text**). Table 1, row *Abudefduf saxatilis* [M_muscle/M_body (%)], gives:

- abductor superficialis 0.13
- abductor profundus 0.23
- adductor superficialis 0.15
- adductor profundus 0.18
- total 0.69

The claim quotes these correctly.

**The fraction.** 0.13 + 0.23 + 0.15 + 0.18 = 0.69% per fin. Doubling for two fins gives 1.38%, so f = 0.0138. This matches the claim.

**Hover requirement.** I used S10's own inputs (m = 0.4 g, ρ = 1.2 kg/m³, k = 1.2, full disc A = πR²). All values below are calculations:

| R | M | W/kg body | W/kg muscle at f = 0.0138 | Times 134.4 W/kg | f at which 134.4 W/kg is just enough |
|---|---|---|---|---|---|
| 4 cm | 1.5 | 10.07 | 730 | 5.4 | 0.075 |
| 4 cm | 2.0 | 13.43 | 973 | 7.2 | 0.100 |
| 2 cm | 1.5 | 20.14 | 1460 | 10.9 | 0.150 |
| 2 cm | 2.0 | 26.86 | 1946 | 14.5 | 0.200 |

Each figure in the claim reproduces: the 7.5–20% threshold, 730–1950 W/kg, and the 5–15× shortfall. I found no arithmetic error.

## 2. Proxy check

**First proxy: one damselfish standing in for "the teleost" and for zebrafish.** The quantity that actually matters is the adult zebrafish pectoral muscle mass divided by body mass. That value is `unknown`: S10-D did not find it, and I did not search for it again. *Abudefduf* is one labriform species from one compiled table, and specimen size is not given.

The author argues that a labriform swimmer probably sets an upper bound for a body–caudal swimmer like zebrafish. That is the author's inference. I think it is reasonable, but it is not measured.

**Counter-example inside teleosts: freshwater hatchetfishes (Gasteropelecidae, Characiformes).**

- Secondary sources say their pectoral muscles make up roughly 25% of body mass. These are Wikipedia, Animal Diversity Web (citing Hems 1983) and hobbyist pages, so the read-level is **search-summary**. I did not read a primary measurement.
- Hatchetfishes are otophysans, as zebrafish are, so they are a closer relative of zebrafish than *Abudefduf* is.
- Consequence: the phrase "**the** measured teleost pectoral-muscle fraction is ~1.4%" overgeneralises. Teleost values range from ~1.4% (*Abudefduf*, full-text) to roughly 25% (hatchetfish, search-summary only). I am not averaging these. They describe different animals.
- This does **not** change the estimate for present-day zebrafish. It does show that the zebrafish's own lineage can build pectoral muscle above the threshold.

**What hatchetfish suggest about the threshold.** According to secondary reports of Wiest FC (1995) *J Zool* 236:571–592 (read-level: **search-summary**; I did not read the paper), high-speed video showed that hatchetfish do *not* achieve powered flapping flight despite that muscle mass.

- My inference: an f above the computed 7.5–20% threshold is evidently not sufficient for powered flight.
- That supports S10-D's negative verdict.
- It also suggests that S10-D's "×5–15 muscle enlargement" design target is necessary but may not be sufficient.

**Second proxy: 134.4 W/kg standing in for zebrafish muscle at flapping frequency.** This value was measured in larval (5 dpf) myotomal muscle at 80 Hz and 28 °C (Mead et al. 2020, carried over from S10). A fin wing beats at ~22 Hz, according to S10's own calculation. S10 records the power at ~20 Hz as `unknown`.

Mass-specific power usually falls at frequencies well below a muscle's optimum, so 134.4 W/kg is more likely generous than stingy. That is my inference, and it is not measured. Either way, this proxy does not work against the claim.

## 3. Hidden assumption carrying the result: hover. Tested with that assumption relaxed.

The 5–15× gap is a **hover** figure, and the claim labels it as hover. S10-D says forward flight "could lower it by an unknown factor". The author also states the escape condition: to close the generous case, forward flight would have to cost ≤ 1/5.4 of hover power.

I computed minimum power in forward flight. Every input below is an assumption:

- body frontal area 2.2 × 10⁻⁵ m², C_D,body 0.4
- S10's wing, aspect ratio 6
- steady profile drag coefficient 0.05–0.2
- speed floor set by S10's C_L,max = 1.5
- same k

Results (calculation):

| R | C_D,pro | V | Power as a fraction of hover (M = 1.5) | W/kg muscle at f = 0.0138 | Times 134.4 |
|---|---|---|---|---|---|
| 4 cm | 0.05 | 2.02 m/s | 0.26 | 193 | 1.4 |
| 4 cm | 0.10 | 2.02 m/s | 0.33 | 241 | 1.8 |
| 4 cm | 0.20 | 2.02 m/s | 0.46 | 338 | 2.5 |
| 2 cm | 0.05 | 4.04 m/s | 0.30 | 434 | 3.2 |
| 2 cm | 0.20 | 4.04 m/s | 0.49 | 721 | 5.4 |

What this shows (calculation):

- **The verdict survives.** Forward flight saves at most a factor of ~0.26 (about 1/3.8). That does not meet the author's 1/5.4 escape condition. Every case remains above 134.4 W/kg.
- **The margin is much thinner.** In the most generous case the gap shrinks from 5.4× to **1.4×**. The f at which 134.4 W/kg would just suffice falls to ≈ 0.020, which is only ~1.4 times the *Abudefduf* proxy. A proxy error that size (zebrafish having 1.4× a damselfish's pectoral muscle) is not ruled out by any measurement. I expect it to go the other way, but that is inference.
- **Why the generous case is likely too generous.** It requires the fish to already be airborne at ~2 m/s. It uses a steady profile drag of 0.05, which is low for a flapping wing at Re ~10³, and it adds no take-off or climb cost. All three choices push the requirement down, so the true margin is probably wider than 1.4×. That is inference, not measured.
- **Overall:** the "order of magnitude below threshold" framing holds for hover. In forward flight the gap is roughly 1.4–5.4× (calculation).

## 4. Is the evidence level honest?

- **The recorded level, "derived", is correct.** The 0.69% is a measured value read from a secondary compilation. The authors take their actinopterygian data from Thorsen & Westneat (2005), which neither S10-D nor I read (read-level: listing). The 1.38% is that measured value doubled, so it is derived.
- **The claim sentence is not.** It calls the two-fin 1.38% "the measured teleost pectoral-muscle fraction". The number is right, but it is derived (×2), it comes from one species, and the source is a secondary compilation.
- **Wording correction:** "a derived two-fin fraction of ~1.4% (2 × 0.69% per fin, measured in one labriform teleost, *Abudefduf saxatilis*, via the Mansuit & Herrel 2021 compilation of Thorsen & Westneat 2005)".
- **The rest is labelled honestly.** The hover demand and threshold are explicitly computed. The 134.4 W/kg is a measurement, but in larval muscle at 80 Hz.

## 5. Regimes, taxa and counter-examples the author missed

| Item | Effect on the claim |
|---|---|
| Hatchetfish, ~25% pectoral muscle (search-summary) | Refutes the teleost-wide wording, not the zebrafish estimate. It also suggests f above the threshold is not sufficient for flight (Wiest 1995, search-summary). |
| Forward flight | Narrows the gap to 1.4–5.4× (calculation). Does not close it. |
| 134.4 W/kg measured at 80 Hz, not ~22 Hz | Probably makes the claim conservative (inference). |
| Recruiting axial muscle | Already flagged by the author as unmodelled. It is outside this claim's scope, which covers pectoral fraction only. |

**Scope of my negative searches:**

- Two web searches: one for hatchetfish pectoral muscle mass, one for Wiest 1995.
- One fetch of the Mansuit & Herrel HTML page; Table 1 is an image there, so it could not be read.
- One PDF download of Mansuit & Herrel, which was readable.
- I searched no bibliographic databases. I made no new search for a zebrafish value, which remains `unknown`. I did not read Thorsen & Westneat (2005) or Wiest (1995).

## Verdict

**SURVIVED.**

- The arithmetic reproduces exactly.
- The Table 1 values match the PDF.
- The negative conclusion (the burst/hover requirement is above measured warm zebrafish fast muscle for present anatomy) holds in hover. It also holds in a forward-flight relaxation I computed, which the author left uncomputed.

Two corrections are needed. Neither one flips the verdict:

1. "Measured teleost fraction ~1.4%" should read as derived, from a single species. Hatchetfish (~25%, search-summary) show that teleost values span more than an order of magnitude.
2. The 5–15× margin applies to hover only. In forward flight it is 1.4–5.4× (calculation). At the generous end, that is within plausible error in the proxy species.

## Sources (with read-levels)

- Mansuit R, Herrel A (2021) The evolution of appendicular muscles during the fin-to-limb transition. *Front Ecol Evol* 9:702576. https://www.frontiersin.org/articles/10.3389/fevo.2021.702576 — **full-text** (PDF via pdftotext; Table 1 read directly)
- Thorsen DH, Westneat MW (2005) *J Morphol*, doi:10.1002/jmor.10173 — **listing** (cited by Mansuit & Herrel as the source of the actinopterygian data; not read)
- Wiest FC (1995) The specialized locomotory apparatus of the freshwater hatchetfish family Gasteropelecidae. *J Zool* 236(4):571–592 — **search-summary** (citation and conclusion as reported by secondary sites)
- Gasteropelecidae pectoral muscle ~25% of body mass: https://en.wikipedia.org/wiki/Gasteropelecidae and https://animaldiversity.org/accounts/Gasteropelecus_sternicla (citing Hems 1983) — **search-summary**
- Mead AF et al. (2020) *Biophys J* 119:806–820 (134.4 W/kg, 80 Hz, 28 °C) — carried over from S10 with S10's read-level (full-text, partial). I did not re-read it.
- S10-tissue.md and S10-deepen.md (repository branches) — **full-text**

```swarm-challenge
{"claim_id": 77, "outcome": "survived", "reason": "Arithmetic (0.69%/fin x2 = 1.38%; thresholds 0.075-0.20; hover 730-1946 W/kg, 5.4-14.5x over 134.4 W/kg) and Mansuit & Herrel Table 1 reproduce exactly, and a computed forward-flight relaxation still leaves a 1.4-5.4x shortfall, but the 1.4% is derived from one species (not 'the measured teleost fraction'; hatchetfish ~25%, search-summary) and the 5-15x margin is hover-only.", "corrected_value": null, "depends_on": ["Mansuit & Herrel 2021 Table 1 Abudefduf saxatilis 0.69% per pectoral fin (full-text)", "S10 hover momentum model inputs: m=0.4 g, rho=1.2, k=1.2, R=2-4 cm, M=1.5-2.0", "Mead et al. 2020 larval zebrafish fast muscle 134.4 W/kg at 80 Hz, 28 C (carried from S10)", "forward-flight assumptions in challenge_77_calc.py: body frontal area 2.2e-5 m2, CDbody 0.4, CDpro 0.05-0.2, CLmax 1.5, AR 6", "Gasteropelecidae ~25% pectoral muscle (search-summary)", "Wiest 1995 no powered flapping flight in hatchetfish (search-summary)"]}
```
