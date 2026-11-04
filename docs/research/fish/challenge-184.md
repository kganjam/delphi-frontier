# Challenge 184: adversarial review of S10-D (flight-muscle fraction f)

**Claim under review** (author: `harvest:deepen-s10-flapping-muscle-wr33g7`, recorded evidence level `derived`):

> The answer is most sensitive to the flight-muscle fraction f, which S10 assumed at 0.1–0.3. The best measured teleost proxy (*Abudefduf saxatilis*, 0.69% body mass per pectoral fin, ~1.4% for both; Mansuit & Herrel 2021 Table 1, full-text) puts the computed hover requirement at ~730–1950 W/kg muscle. That is 5–15× above measured warm zebrafish fast muscle and above any listed vertebrate muscle. Sustained flapping therefore stays impossible, and burst flapping also fails for present anatomy, requiring a ~5–15× pectoral-muscle enlargement. (No zebrafish measurement exists in what was searched.)

Source note read: `docs/research/fish/S10-deepen.md` and `S10_deepen_calc.py` on branch `claude/deepen-s10-flapping-muscle-wr33g7`. Read-level: full-text.

My script: `docs/research/fish/challenge_184_calc.py`. **Every number below that comes from it is a calculation, not an observation.** I wrote it from the formula without reusing the author's code.

---

## 1. Independent arithmetic

Inputs, taken from S10:
- body mass m = 0.4 g
- air density ρ = 1.2 kg/m³
- induced-power factor k = 1.2
- disc area A = πR²
- profile multiplier M

Formula: P = M·k·W^1.5 / √(2ρA), with W = m·g. The requirement per kg of muscle is P / (m·f).

**One-fin sum (Table 1 row).** 0.13 + 0.23 + 0.15 + 0.18 = **0.69%**. Two fins give f = **0.0138**.

Hover results (calculation):

| R, M | P (mW) | Required W/kg muscle | ÷ 134.4 W/kg | f threshold |
|---|---|---|---|---|
| 4 cm, 1.5 | 4.03 | 730 | 5.4× | 0.075 |
| 4 cm, 2.0 | 5.37 | 973 | 7.2× | 0.100 |
| 2 cm, 1.5 | 8.06 | 1460 | 10.9× | 0.150 |
| 2 cm, 2.0 | 10.74 | 1946 | 14.5× | 0.200 |

**Marden threshold.** g / (54–63 N/kg) = 0.156–0.182. Clap-and-fling (86 N/kg) gives 0.114.

**Sustained flapping.** The f needed for 10 W/kg red muscle is 1.01 in the most generous geometry, which is impossible.

**All of the author's numbers reproduce.**

## 2. Is the proxy the right quantity?

**Table 1 checked against source.** I downloaded the Mansuit & Herrel PDF and ran pdftotext myself (read-level: full-text).
- The *Abudefduf* row reads 0.13 / 0.23 / 0.15 / 0.18 / total 0.69, with units M_muscle/M_body (%).
- The authors say "each appendage has a mass relative to the body mass inferior to 1%".
- So the per-fin reading and the doubling to 1.38% are correct.

**Kind of quantity.** Intrinsic pectoral abductor and adductor mass as a fraction of body mass is the right kind of quantity. It is the fish analogue of the bird flight-muscle ratio, since both cover the upstroke and downstroke muscles.

**Weakness 1: one species out of twelve.** Thorsen & Westneat (2005) is the primary source; read-level listing/search-summary, abstract only.
- It studied 12 labriform species and reports that muscle mass "varies widely" among them.
- Mansuit & Herrel carry only *Abudefduf*.
- The claim calls this the "best measured teleost proxy". It is actually one species picked by a secondary compilation, not the maximum of the measured labriform range.
- The other eleven values are `unknown` to me; I did not get the full text.
- To close the most generous hover gap, a species would need about 3.8% per fin (calculation).

**Weakness 2: teleosts with far larger fractions exist.**
- Freshwater hatchetfishes (Gasteropelecidae) are reported at **~25%** of body mass in pectoral muscle. Read-level: search-summary. The sources are secondary (Animal Diversity Web, a Wikipedia mirror, hobby sites), and none of them cites a primary measurement I could see.
- They are otophysans, a closer relative of zebrafish than a damselfish is.
- This does not refute the claim, which concerns *present zebrafish anatomy*. It does show that the "5–15× enlargement" lies inside the range teleosts have evolved.
- Even in hatchetfish, powered aerial flapping is reported as disproven: Wiest 1995, read-level search-summary via seriouslyfish.com. That is consistent with the claim, not against it.

**Direction of the zebrafish inference.** The author expects a body–caudal swimmer to sit at or below a labriform swimmer. I find that plausible, but it is unmeasured. The author labels it as inference, which is correct.

## 3. Hidden assumptions, relaxed

**(a) Body mass does not grow when muscle is added.** The author flagged this but did not iterate it. I held non-muscle mass fixed and solved for the f at which the requirement equals 134.4 W/kg (calculation):

| Geometry | f threshold, no feedback | f threshold, with feedback | Body mass | Muscle-mass enlargement |
|---|---|---|---|---|
| 4 cm, 1.5 | 0.075 (×5.4) | 0.077 | 0.428 g | **×6.0** |
| 4 cm, 2.0 | 0.100 (×7.2) | 0.105 | 0.441 g | ×8.4 |
| 2 cm, 1.5 | 0.150 (×10.9) | 0.163 | 0.471 g | ×13.9 |
| 2 cm, 2.0 | 0.200 (×14.5) | 0.225 | 0.509 g | **×20.8** |

The claim's "~5–15×" understates the needed muscle-mass enlargement at the realistic end. The correct range is **~6–21×** (calculation). That error makes the claim's conclusion *harder* to escape, not easier, so it does not threaten the verdict.

**(b) "Most sensitive to f."** In the formula, the requirement scales with R and f with elasticity −1 each, with M at +1 and with m at +0.5.
- f is therefore **tied** with R and M in local sensitivity, not uniquely highest. The author's own ±2× table shows identical values for R, M and f.
- The defensible statement is that f is the **least-established and widest-ranging** input. Its plausible range spans more than 10× (0.014 vs 0.1–0.3), which makes it dominate uncertainty-weighted sensitivity.
- This is a wording flaw. It does not change the result.

**(c) Hover only.** The claim scopes itself to the "computed hover requirement", but "burst flapping also fails" reads as general.
- In the generous geometry, forward flight would have to cut aerodynamic power to ≤ 0.184 of hover to close the gap (calculation).
- I did not compute a forward-flight model myself, so my verdict is scoped to hover.
- A separate review of this same result (challenge 77, branch `claude/challenge-s10-d-pectoral-muscle-vmlxc6`, read-level full-text) computed a forward-flight shortfall of 1.4–5.4×.
- I preserve that as that review's calculation, not mine. If it holds, burst flapping still fails in forward flight. But at the generous end the margin (1.4×) is within plausible proxy error, and the claim's "5–15×" is hover-specific.

**(d) Other inputs carried from S10 that I did not re-read:**
- the 134.4 W/kg larval zebrafish fast-muscle value (Mead et al. 2020)
- the quail value of 433 W/kg
- k = 1.2

Adult zebrafish fast-muscle power at 28 °C is `unknown` here. It would have to be more than 5× the larval value to rescue the generous case, so it cannot plausibly flip the claim.

## 4. Is the evidence level honest?

`derived` is correct. Three things combine:
- the f value is measured, but in a proxy species, and reached through a secondary compilation (primary source not read);
- the requirement is computed;
- Marden's figure is search-summary.

The claim's phrase "measured teleost proxy" is accurate as long as "proxy" is kept. Nothing calculated is presented as observed.

## 5. Verdict: SURVIVED (hover scope), with a corrected enlargement range

I tried to break the claim in four ways: the arithmetic, the source table, the proxy choice, and its assumptions. None of them reverses it.
- All the arithmetic reproduces independently.
- Table 1 matches the source PDF.
- Relaxing the un-iterated mass assumption makes the conclusion stronger.
- The plausible counter-taxa (other labriform species, unknown; hatchetfish ~25%, search-summary) bear on what an *engineered* fish could carry, not on present zebrafish anatomy.

Corrections I recommend:
1. Muscle-mass enlargement needed: ~5–15× → **~6–21×** with body-mass feedback (calculation).
2. "Most sensitive" → "least established, and dominant once its uncertainty range is weighted". R and M have equal local elasticity.
3. "Best measured teleost proxy" → "the only labriform species value carried in Mansuit & Herrel Table 1". The other 11 Thorsen & Westneat species are `unknown`.
4. State that the 5–15× shortfall is hover-only.

**Negative-search scope:**
- one fetch of the Mansuit & Herrel article page, plus a PDF download;
- one web search on Thorsen & Westneat 2005 muscle percentages (abstract-level only; full text not reached);
- one web search on hatchetfish pectoral muscle fraction (secondary sources only; no primary measurement found).

## Sources (read-levels)

- Mansuit R, Herrel A (2021) *Front Ecol Evol* 9:702576, https://www.frontiersin.org/articles/10.3389/fevo.2021.702576 — **full-text** (PDF via pdftotext; Table 1 read directly)
- Thorsen DH, Westneat MW (2005) *J Morphol* 263:133–150, doi:10.1002/jmor.10173 — **search-summary** (abstract content via search)
- Hatchetfish ~25% pectoral muscle: https://animaldiversity.org/accounts/Gasteropelecus_sternicla, https://www.seriouslyfish.com/species/gasteropelecus-sternicla — **search-summary**
- Wiest FC (1995), hatchetfish locomotion (no powered aerial flapping) — **search-summary** (via seriouslyfish.com)
- Marden JH (1987) *J Exp Biol* 130:235–258 — carried from S10-D (search-summary); not re-read
- Mead et al. 2020 (134.4 W/kg) and Askew & Marsh 2001 (433 W/kg) — carried from S10; not re-read
- Challenge 77 (`claude/challenge-s10-d-pectoral-muscle-vmlxc6`) — **full-text** (repository branch)

```swarm-challenge
{"claim_id": 184, "outcome": "survived", "reason": "Arithmetic (0.69%/fin x2 = 1.38%; hover 730-1946 W/kg = 5.4-14.5x over 134.4 W/kg; f thresholds 0.075-0.20; Marden 0.156-0.182) and Mansuit & Herrel Table 1 reproduce independently, and relaxing the un-iterated mass-feedback assumption strengthens rather than weakens the conclusion, though the needed muscle-mass enlargement is ~6-21x (not 5-15x), f is tied with R and M in local elasticity, and the margin is hover-only.", "corrected_value": "required pectoral muscle-mass enlargement ~6-21x (hover, with body-mass feedback; calculation)", "depends_on": ["Mansuit & Herrel 2021 Table 1 Abudefduf saxatilis 0.69% body mass per pectoral fin (full-text)", "S10 hover momentum model inputs: m=0.4 g, rho=1.2 kg/m3, k=1.2, R=2-4 cm, M=1.5-2.0", "Mead et al. 2020 larval zebrafish fast muscle 134.4 W/kg (carried from S10, not re-read)", "Marden 1987 54-63 N/kg max lift per flight-muscle mass (search-summary, carried from S10-D)", "assumption: zebrafish pectoral fraction <= labriform Abudefduf (inference, unmeasured)", "Gasteropelecidae ~25% pectoral muscle (search-summary)", "challenge_184_calc.py mass-feedback model: non-muscle mass held fixed"]}
```
