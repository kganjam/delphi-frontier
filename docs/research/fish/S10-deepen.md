# S10-D: deepening S10 (tissue) by attacking its weakest input

Parent: `docs/research/fish/S10-tissue.md` (branch `claude/s10-tissue-flapping-power-2kag3x`). S10 asked whether there is enough muscle power for flapping if gliding is insufficient. The recorded answer had two halves:

- **Sustained** flapping is not supported. Measured red/slow fish muscle gives 5–10 W/kg, against a computed requirement of at least ~34 W/kg of flight muscle.
- **Burst** flapping is "possibly" within reach of warm fast muscle (134 W/kg, larval zebrafish), but only if roughly 10–30% of body mass were pectoral flight muscle. S10 said present-day zebrafish anatomy is "nowhere near that", but gave no measured value.

Calculation script: `docs/research/fish/S10_deepen_calc.py`. **Every requirement number in this file is a calculation** (Rankine–Froude momentum theory, as in S10). None is an observation.

---

## 1. Which input is the answer most sensitive to? (recomputed)

S10's requirement per kg of flight muscle is

  P_req = M · k · √(W³ / (2ρπR²)) / (m · f)

so it scales as M · m^½ / (R · f). I halved and doubled each input around S10's most generous case (R = 4 cm, M = 1.5, f = 0.3, m = 0.4 g, requirement 33.6 W/kg). The output below is computed:

| Input changed | ×0.5 | ×2 | Sustained (≤10 W/kg) flips? | Burst (≤134 W/kg) flips? |
|---|---|---|---|---|
| body mass m | 23.7 | 47.5 | no | no |
| wing semispan R | 67.1 | 16.8 | no | no |
| profile multiplier M | 16.8 | 67.1 | no | no |
| **flight-muscle fraction f** | 67.1 | 16.8 | no | no |

(values in W/kg flight muscle)

What the recomputation shows (calculation):

- **The sustained "no" survives a factor-of-2 error in any single input.** For 10 W/kg red muscle to suffice in the most generous geometry, f would have to be 1.01. That means more than the whole body would have to be flight muscle, which is physically impossible. Only the red-muscle power density itself could flip it, and it would have to be wrong by more than 3×. S10 already flagged that possibility through the unresolved skipjack 79–133 W/kg conference abstract (§5).
- **The burst half is where the answer actually hinges, and f is the input it hinges on.** The f at which 134 W/kg fast muscle just suffices is **0.075** in the most generous geometry and **0.20** in the R = 2 cm, M = 2 geometry (computed). S10's own f range of 0.1–0.3 straddles that threshold. So S10's burst verdict "possibly" was a statement about an assumed f, not about the fish.
- **Why f and not R or M, which enter the formula just as strongly.** R and M are design choices, which S1/S2 will fix. f is a biological fact about the animal. S10 stated it as an assumption ("I have no measured value"), searched no source for it ("I did not search for it specifically"), and said the answer "depends on it most strongly". It is the weakest input: an assumption that read as a design parameter.

## 2. How well was f established in S10?

**Evidence level: assumption.** It was not measured or proxied, and no source was cited. The values 0.1 / 0.2 / 0.3 look like bird or insect flight-muscle ratios, but S10 did not retrieve those either. No zebrafish or fish value was used.

## 3. Improving it

### 3a. Primary-source search for a zebrafish value

- Search: "zebrafish pectoral fin muscle mass abductor adductor percentage body mass" (one web search). Result: **no zebrafish mass fraction found.** I did find anatomy:
  - Two pectoral-fin muscle masses (abductor and adductor) flank the endoskeletal disc.
  - Late-larval fin muscle is fast-fibre only (Patterson & Devoto 2008, Wesleyan PDF), read-level search-summary.
  - Abductor/adductor **fibre counts** at 5 dpf (Nord et al. 2021, ZFIN figure listings), read-level search-summary/listing. These are not masses.
- Zebrafish adult pectoral muscle mass fraction: **`unknown`.** Scope of the negative: one web search plus the ZFIN figure listings it returned. I searched no database (Web of Science, Scopus) and no micro-CT repositories.

### 3b. The nearest measured quantity: pectoral muscle mass in a fin-flapping teleost

**Mansuit R & Herrel A (2021)**, "The Evolution of Appendicular Muscles During the Fin-to-Limb Transition", *Front Ecol Evol* 9:702576, doi:10.3389/fevo.2021.702576. Read-level: **full-text**. I read the PDF through `pdftotext`; Table 1 was read directly.

Table 1 values, quoted as M_muscle / M_body (%):

| Species | Abd. superf. | Abd. prof. | Add. superf. | Add. prof. | **Total, one pectoral fin** |
|---|---|---|---|---|---|
| *Abudefduf saxatilis* (sergeant major, a damselfish) | 0.13 | 0.23 | 0.15 | 0.18 | **0.69** |
| *Latimeria chalumnae* (coelacanth) | 0.08 | 0.16 | 0.09 | 0.10 | **0.43** |
| *Alligator mississippiensis* (for contrast) | 0.86 | 0.20 | 0.45 | 0.24 | 1.76 |

- **Authors' claim:** in actinopterygians "each fin represents less than 1% of the total body mass". The authors say the actinopterygian mass data come from Thorsen & Westneat (2005, *J Morphol*, doi:10.1002/jmor.10173). I did **not** read Thorsen & Westneat itself (read-level: listing). The other two fish rows in the table (*Cryptopsaras*, *Antennarius*) are physiological cross-sectional area (PCSA), not mass, so I did not use them.
- **My inference, not the authors':** *Abudefduf* is a labriform swimmer, one that powers routine swimming with its pectoral fins. That is the teleost lifestyle most likely to enlarge pectoral muscle. Zebrafish swim mainly by body–caudal undulation. I would therefore expect the zebrafish fraction to be at or **below** the *Abudefduf* value, but that is not measured. Both pectoral fins together give **f ≈ 2 × 0.69% = 1.38% ≈ 0.014**. I use this as a generous upper-end proxy for zebrafish.
- Caveats I cannot resolve:
  - The specimen size of *Abudefduf* is not given in the table.
  - The table pools data across studies.
  - The value includes all four fin-muscle groups, but not girdle-to-body muscles that might also be recruited.

### 3c. Independent check: how much flight muscle do real fliers need?

**Marden JH (1987)**, "Maximum lift production during takeoff in flying animals", *J Exp Biol* 130:235–258. Read-level: **search-summary of the abstract**. The JEB host cob.silverchair.com and scilit.com both failed to resolve from this session, so I could not read the abstract page itself.

- **Author's claim (via summary):** maximum lift per kg of flight muscle is 54–63 N/kg across birds, bats and insects using conventional wingbeats, and 72–86 N/kg with clap-and-fling. Marden attributes differences in takeoff ability "primarily" to flight-muscle ratio. Measured ratios in his sample spanned 0.115–0.560.
- **My calculation from those figures:** lifting one's own weight needs f ≥ g / (lift per kg muscle). That gives 9.81/63 = **0.156** to 9.81/54 = 0.182, or 0.114 with clap-and-fling.
- This threshold is measured in flight muscle that is mostly better than fish fast muscle. Quail pectoralis delivers ~350–433 W/kg (S10 §2b), while larval zebrafish delivers 134 W/kg. Applied to fish muscle it is therefore a lower bound on the real requirement. That is an inference, and Marden says nothing about fish.

**Disagreement preserved.** S10's momentum-theory threshold for burst flight (f = 0.075–0.20, computed) and Marden's empirical takeoff threshold (f ≈ 0.11–0.18, from measured lift per muscle mass) are different kinds of estimate. The most generous momentum case sits below Marden's lowest figure. I have not reconciled them. Both place the threshold at about one-tenth to one-fifth of body mass.

### 3d. The measurement that would settle it

- **The measurement:** dissect and weigh the four pectoral-fin muscle groups on both sides of about 10 adult wild-type zebrafish, together with wet body mass. Tools are a dissecting scope and a microbalance readable to ~0.01 mg. At 0.4 g body mass, 1% is 4 mg. Expected effort: a few days for one trained person, using fish culled from a standard facility. I have not costed it in money; I put the cost as `unknown`, but small.
- **Non-destructive alternative:** segment existing contrast-enhanced micro-CT scans of adult zebrafish. I did not search for specific datasets, so I name none.

## 4. Recomputing S10 with the improved input (calculation)

With f = 0.0138 (two-fin *Abudefduf* proxy, likely generous for zebrafish):

| Geometry (from S10) | Required W/kg muscle | ÷ larval zebrafish fast (134.4, measured) | ÷ best quail in vitro (433, search-summary) |
|---|---|---|---|
| R = 4 cm, M = 1.5 (most generous) | **730** | 5.4× short | 1.7× short |
| R = 4 cm, M = 2.0 | 973 | 7.2× short | 2.2× short |
| R = 2 cm, M = 1.5 | 1460 | 10.9× short | 3.4× short |
| R = 2 cm, M = 2.0 | 1946 | 14.5× short | 4.5× short |

- **Sustained flapping:** S10's "no" **stands**, and it is now overwhelming. The most generous requirement is ~730 W/kg against 5–10 W/kg measured red muscle, a shortfall of about 70–150× (calculation). Even the unresolved skipjack 133 W/kg value would fall 5× short.
- **Burst flapping with present anatomy:** this was "possibly" in S10 and now **falls to no**. In every geometry the requirement exceeds the warm zebrafish fast muscle that has been measured. It also exceeds the highest cycle-averaged power from any vertebrate muscle listed in S10 (quail, 433 W/kg), and the top of the theoretical ceilings S10 listed (≤ 430 W/kg). This is a calculation on a proxied f.
- **Burst flapping as a design target:** reaching the burst threshold needs the pectoral flight muscle enlarged by **×5.4 (generous geometry) to ×14.5 (realistic)** with respect to S10's thresholds. Against Marden's empirical 0.156 it needs ×11.3 (calculation). Adding that muscle also adds body mass, which raises the requirement further (∝ m^½ per kg of muscle). I have not iterated that correction, so the true enlargement factor is somewhat larger.

**Verdict: STRENGTHENS.** S10's conclusion (sustained no; burst only with a pectoral muscle fraction of ~0.1–0.3 that zebrafish lack) is confirmed. The vague "nowhere near" is now a number: the best measured teleost proxy is ~1.4% of body mass, about an order of magnitude below the threshold. The one half of S10 that leaned toward feasibility, burst flapping, falls for the present animal and becomes a ×5–15 muscle-enlargement requirement for any engineered one. This rests on a proxy species, not a zebrafish measurement.

## 5. What this does not establish

- **No zebrafish measurement exists in what I found.** The improved input is a proxy from another species (*Abudefduf*), taken through a secondary compilation. The primary source (Thorsen & Westneat 2005) was not read. If zebrafish were, against my expectation, several-fold more pectorally muscled than a labriform damselfish, the burst gap would narrow, but it would need ≥ 5× to close even the generous case.
- **The requirement is still S10's hover model**, with all its assumptions: full-disc momentum theory, assumed M, no inertial power, and no forward flight. Forward flight at minimum-power speed could lower it by an unknown factor. To close the generous-case burst gap that factor would have to be ≤ 1/5.4 (calculation).
- **Recruiting axial (trunk) muscle to drive the fins** through some linkage is not modelled. Trunk muscle is roughly half of a fish's body mass in general fish physiology, but I did not retrieve a source for that in this deepening. This is the main escape route from the f constraint, and it belongs to an organ/design subproblem.
- **Negative-search scope:** one web search for zebrafish pectoral muscle mass; one for labriform pectoral muscle fractions; one for flying-fish pectoral muscle mass. The flying-fish search returned no muscle-mass value. A Davenport abstract (search-summary) says flying-fish take-off is likely anaerobic and powered by the body axis, not by the pectorals. I also ran one search for Marden 1987. JEB full texts were unreachable: cob.silverchair.com did not resolve from this session, and neither did scilit.com.

## Sources (with read-levels)

- Mansuit R, Herrel A (2021) *Front Ecol Evol* 9:702576. https://www.frontiersin.org/articles/10.3389/fevo.2021.702576 — **full-text** (PDF converted with pdftotext; Table 1 read directly)
- Thorsen DH, Westneat MW (2005) Diversity of pectoral fin structure and function in fishes with labriform propulsion. *J Morphol*, doi:10.1002/jmor.10173 — **listing** (title and abstract summary only; tables not read)
- Marden JH (1987) *J Exp Biol* 130:235–258 — **search-summary** (abstract; host could-not-access)
- Patterson SE, Devoto SH et al. (2008), zebrafish pectoral fin muscle development. https://sdevoto.web.wesleyan.edu/PDFsMovies/patterson_devoto2008.pdf — **search-summary**
- Nord et al. (2021), ZFIN figures of pectoral abductor/adductor fibre counts at 5 dpf. https://zfin.org/ZDB-FIG-220127-5 — **listing**
- Davenport J, flying-fish morphometrics and red muscle. https://www.cambridge.org/core/journals/journal-of-the-marine-biological-association-of-the-united-kingdom/article/wingloading-stability-and-morphometric-relationships-in-flying-fish-exocoetidae-from-the-northeastern-atlantic/1F8A2DC43BE7C90AB5AB85DB592AAA63 — **search-summary**
- The muscle power values (Mead et al. 2020: 134.4 W/kg; Askew & Marsh 2001: 433 W/kg; red muscle 5–10 W/kg) are carried over from S10 with S10's read-levels. I did not re-read them.

```swarm-result
{"subproblem": "S10-D", "evidence": "derived",
  "answer": "The answer is most sensitive to the flight-muscle fraction f, which S10 assumed at 0.1-0.3; the best measured teleost proxy (Abudefduf saxatilis, 0.69% body mass per pectoral fin, ~1.4% for both, full-text Mansuit & Herrel 2021 Table 1) puts the computed hover requirement at ~730-1950 W/kg muscle, 5-15x above measured warm zebrafish fast muscle and above any listed vertebrate muscle, so sustained flapping stays impossible and burst flapping also fails for present anatomy, requiring a ~5-15x pectoral-muscle enlargement (no zebrafish measurement exists in what was searched).",
  "key_number": "f ~0.014 (pectoral muscle mass / body mass, both fins; proxy species Abudefduf saxatilis, 0.69% per fin) vs 0.075-0.20 computed threshold and ~0.16 Marden empirical takeoff threshold",
  "verdict": "strengthens"}
```
