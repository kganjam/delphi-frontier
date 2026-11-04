# S10-D-D: deepening S10-D by attacking its weakest input

Parent chain:
- `S10` (tissue): `docs/research/fish/S10-tissue.md` on branch `claude/s10-tissue-flapping-power-2kag3x`
- `S10-D`: `docs/research/fish/S10-deepen.md` on branch `claude/deepen-s10-flapping-muscle-wr33g7`

Calculation script: `docs/research/fish/S10-D-deepen_calc.py`. **Every requirement number and every ratio in this file is a calculation** from the same Rankine–Froude hover model that S10 and S10-D used. None of them is an observation. Measured values are labelled as measured, and each carries a read-level.

## What S10-D concluded

S10-D replaced S10's assumed flight-muscle fraction (f = 0.1–0.3) with a proxy. The proxy is **f ≈ 0.0138** (both pectoral fins), from the damselfish *Abudefduf saxatilis*: 0.69% of body mass per fin (Mansuit & Herrel 2021, Table 1). With that proxy, S10-D computed that the hover requirement is 730–1946 W/kg of muscle. Measured warm zebrafish fast muscle gives 134.4 W/kg, so the shortfall is 5.4–14.5×. S10-D's conclusions were:
- sustained flapping: no;
- burst flapping with present anatomy: no;
- verdict on S10: **strengthens**.

---

## 1. Which input is S10-D's conclusion most sensitive to? (recomputed)

The deciding half of S10-D is the burst verdict. In its most generous geometry (R = 4 cm, M = 1.5, m = 0.4 g, f = 0.0138), the requirement is 730 W/kg muscle against a measured 134.4 W/kg. The table below shows what each input does when halved or doubled, and how far it would have to move to flip the verdict (**calculation**):

| Input | ×0.5 | ×2 | Multiplier on the input needed to flip burst to "yes" |
|---|---|---|---|
| body mass m | 516 | 1032 | ×0.034 (requirement ∝ m^½) |
| wing semispan R | 1460 | 365 | ×5.43 |
| profile multiplier M | 365 | 1460 | ×0.184 |
| **flight-muscle fraction f** | 1460 | **365** | **×5.43** |
| muscle power density (134.4 W/kg) | — | — | ×5.43 |

(requirements in W/kg flight muscle)

**Result of the recomputation:** S10-D's burst "no" does **not** flip under a factor-2 error in any single input. Doubling f, doubling R or halving M each leaves a 2.7× shortfall. The sustained "no" sits even further from the line: the requirement would have to fall by 70–150× (S10-D's own figure, recomputed here as 730 / 5–10).

f, R, M and muscle power all enter linearly, so on sensitivity alone they tie. I pick **f** as the input to attack, on evidence grounds:
- R and M are design choices that S1/S2 will fix.
- The 134.4 W/kg is a direct measurement (S10, full-text).
- f is the only biological input that is still a **proxy**: another species, read through a secondary compilation.
- f is the input most exposed to a *structural* error, namely which muscles get counted (§2).

## 2. How well is f established?

- **Evidence level:** proxy. It is not a zebrafish measurement.
- **The number itself is confirmed.** I re-downloaded the Mansuit & Herrel (2021) PDF and read Table 1 directly (read-level: **full-text**). The row reads: *Abudefduf saxatilis* [M_muscle/M_body (%)]: abductor superficialis 0.13, abductor profundus 0.23, adductor superficialis 0.15, adductor profundus 0.18, total 0.69. The authors state that the actinopterygian data were taken from Thorsen & Westneat (2005).
- **Structural weakness found: the 0.69% is a four-muscle sum.** Two sources show the pectoral system has more muscle than that:
  - *Authors' claim (Thorsen & Westneat 2005, abstract, read-level: abstract via Europe PMC):* labriform pectoral fins carry further muscles, including the arrector dorsalis, and muscle masses "show broad variation among species, particularly in the adductor profundus, abductor profundus, arrector dorsalis, and abductor superficialis". The table I can read has no arrector column. *My inference:* the 0.69% therefore probably **undercounts** the total pectoral fin muscle of *Abudefduf*.
  - *Authors' claim (Siomava, Shkil, Voronezhskaya & Diogo 2018, Sci Rep 8:14187, PMC6155031, read-level: **full-text** XML via Europe PMC):* in zebrafish "at 6.7 mm SL, all seven pectoral fin muscles are present and display the adult configuration". Zebrafish therefore has more than the four groups that were summed.
- **What S10-D got right:** it said the value "includes all four fin-muscle groups, but not girdle-to-body muscles". The gap is wider than that note implied, because *fin* muscles were also left out.

## 3. Improving it

### 3a. Search for a zebrafish value

**Result: no zebrafish pectoral muscle mass or mass fraction was found.**

What I searched:
- **Web searches (2):**
  - "Thorsen Westneat 2005 pectoral fin muscle mass percent body mass labriform"
  - "zebrafish adult pectoral fin abductor adductor muscle mass"
- **Europe PMC title and author searches:**
  - Thorsen & Westneat 2005
  - Thorsen & Hale 2005, *Development of zebrafish pectoral fin musculature*
  - Siomava (two zebrafish fin-muscle papers)
- **Full-text keyword scan** (mass / weigh / volume / percent / mg) of two papers:
  - PMC6155031: the word "mass" appears only as "muscle masses" in the anatomical sense. No weights or volumes are given.
  - PMC6443675: no muscle weights or volumes.
- **Abstract only:** Thorsen & Hale 2005 (anatomy and imaging; no mass in the abstract).

What I did not search: Web of Science, Scopus, micro-CT repositories, or the supplementary data of any paper.

**Hosts that failed to resolve from this session.** These would have to be allowed in the session's network settings before I could fetch from them:
- cob.silverchair.com (JEB full texts)
- sicb.org (bluegill muscle-power conference abstracts)
- biomechanics.ucr.edu (Foster & Higham 2010 PDF)

### 3b. Correcting the four-muscle undercount (nearest measured ratio)

**Jones, Lucey & Ellerby (2007)**, *J Exp Biol* 210:3422–3429, doi:10.1242/jeb.005744, PMID 17872996. Read-level: **abstract** (Europe PMC).

- *Authors' claim:* in bluegill sunfish, "the two largest pectoral fin adductor and abductor muscles" constitute "half of the total pectoral girdle muscle mass".
- *My inference, not the authors':* if the same ratio held in *Abudefduf*, there are two ways to apply it.
  - **Mid estimate.** Take the two largest groups, abductor profundus 0.23 and adductor profundus 0.18, and double them. That gives 0.82% per fin, so **f ≈ 0.0164** for both fins.
  - **Upper bracket.** Treat the whole four-group sum as only half of the girdle. That gives 1.38% per fin, so **f ≈ 0.0276**.
  - **Caveats:**
    - It is a cross-species ratio applied to another species.
    - "Pectoral girdle muscle" in bluegill may include muscles that do not move the fin.
    - The bluegill paper's specimen numbers are not in the abstract.

**Improved input:** f = **0.014–0.028** (both fins), with a central value of about **0.016**. It remains a proxy. Expected direction for zebrafish compared with the damselfish proxy: lower, because zebrafish fins are used for "swim initiation and maneuvering" (Thorsen & Hale 2005, authors' claim, abstract) rather than for labriform cruising. That is my inference; it has not been measured.

### 3c. An f-independent check: measured pectoral-system power per body mass

The same paper gives the quantity f was only ever a proxy for: how much mechanical power a fin-flapping teleost's pectoral system actually delivers per kg of body.

- *Authors' claim (measured in vitro, then scaled by the authors to swimming):* muscle mechanical power during maximal labriform swimming is **P_mech = 0.15–0.21 W/kg body mass**.
- *My calculation:* the generous hover requirement in body-mass terms is M·P_ind/m = **10.1 W/kg body**. That is **48–67×** the bluegill figure.
- *Caveat:* P_mech is the power used at the maximal *labriform* (sustained) speed. It is not the burst ceiling of the muscle. The check therefore bears directly on the **sustained** half, and only loosely on the burst half.

### 3d. The measurement that would settle it

- **The measurement:** dissect all seven pectoral fin muscles, plus the girdle muscles, on both sides of about 10 adult wild-type zebrafish, and weigh them against wet body mass.
- **Resolution needed:** about 0.01 mg. At 0.4 g body mass, 1% is 4 mg.
- **Effort and cost:** a few days for one person with a dissecting scope and a microbalance. The money cost is `unknown`, but it is small.
- **Without dissection:** segment existing contrast-enhanced micro-CT scans. I name no dataset, because I searched for none.

## 4. Recomputing S10-D with the improved input (calculation)

| f (both fins) | Basis | Requirement in the 4 geometries (W/kg) | Generous-case shortfall vs 134.4 (80 Hz) | vs 105 (40 Hz, from S10) |
|---|---|---|---|---|
| 0.0138 | S10-D, four groups | 730 / 973 / 1460 / 1946 | ×5.43 | ×6.94 |
| **0.0164** | bluegill ratio on the two largest groups (central) | 614 / 819 / 1228 / 1638 | **×4.57** | ×5.84 |
| 0.0276 | bluegill ratio on all four groups (upper) | 365 / 487 / 730 / 973 | ×2.71 | ×3.47 |

The four geometries are, in order: R = 4 cm, M = 1.5 / R = 4 cm, M = 2 / R = 2 cm, M = 1.5 / R = 2 cm, M = 2.

**Stacked generous errors.** Take the upper f (0.0276) and also assume forward flight halves the hover power. That second factor is an assumption; S10 never computed forward flight. The requirement then falls to 182 W/kg, still **×1.36** above the measured warm fast muscle. This is the closest any combination I tried comes to flipping the verdict, and it needs every generous choice at once.

**Independent thresholds still miss:**
- Marden's empirical takeoff threshold is f ≈ 0.114–0.182. This was carried from S10-D at search-summary read-level; I did not re-read it. The improved bracket falls short of it by ×4.1 to ×13.2.
- The f-independent whole-body comparison (§3c) leaves the sustained case short by roughly 50–70×.

### Verdict: **STANDS**

- **Sustained flapping is impossible.** Two independent routes now support this. One is muscle power density times f. The other is measured pectoral-system power per body mass (48–67× short), which does not depend on f at all.
- **Burst flapping with present anatomy also fails.** The correction moves the margin from S10-D's ×5.4 down to ×4.6 (central) or ×2.7 (upper bracket). It does not close.
- **Why "stands" and not "strengthens":** S10-D's f was biased low, so the gap narrows. S10-D's "×5–15 enlargement" figure should be revised to roughly **×2.7–14.5**, central ×4.6–12.
- **Why not "falls":** reversing the burst verdict needs the upper-bracket f, forward flight at below half the hover power, *and* fast-muscle power at the ~22 Hz design frequency equal to or above the 80 Hz value, all at once. The design-frequency value is `unknown`; S10 found no measurement at 20 Hz.

## 5. What this does not establish

- **There is still no zebrafish measurement.** The input is a damselfish value, corrected by a bluegill ratio. Both are other species, and both sources reached me at abstract or compiled-table level (the Thorsen & Westneat tables themselves were not read).
- **The bluegill "half" ratio may overcorrect.** If "pectoral girdle muscle" includes muscles that do not drive the fin, the upper bracket is too high. Then S10-D's original f is closer to right.
- **Recruiting trunk (axial) muscle through a linkage is outside this analysis.** It is a design escape from the f constraint, not a property of the present animal, and it belongs to an organ or design subproblem. I retrieved no source for the axial muscle fraction of zebrafish (`unknown`).
- **The requirement is still S10's hover model** (full-disc momentum theory, assumed M, no inertial power).
- **Muscle power at ~22 Hz is unknown.** The 134.4 W/kg was measured at 80 Hz in 5-dpf larvae. The 105 W/kg at 40 Hz is an S10 calculation from measured work per cycle.

## Sources (with read-levels)

- Mansuit R, Herrel A (2021) *Front Ecol Evol* 9:702576, doi:10.3389/fevo.2021.702576. Re-read for this file. **full-text** (PDF via pdftotext; Table 1 and Methods read directly)
- Thorsen DH, Westneat MW (2005) *J Morphol* 263:133–150, doi:10.1002/jmor.10173, PMID 15549721. **abstract** (Europe PMC); tables not read
- Jones EA, Lucey KS, Ellerby DJ (2007) Efficiency of labriform swimming in the bluegill sunfish (*Lepomis macrochirus*). *J Exp Biol* 210:3422–3429, doi:10.1242/jeb.005744, PMID 17872996. **abstract** (Europe PMC); full text could-not-access (cob.silverchair.com does not resolve)
- Siomava N, Shkil F, Voronezhskaya E, Diogo R (2018) Development of zebrafish paired and median fin musculature. *Sci Rep* 8:14187, doi:10.1038/s41598-018-32567-z, PMC6155031. **full-text** (Europe PMC XML; keyword scan plus the passage on the seven pectoral muscles)
- Shkil F, Siomava N, Voronezhskaya E, Diogo R (2019) hyperthyroidism and zebrafish appendicular muscles, *Sci Rep* 9:5413, PMC6443675. **full-text** (keyword scan only; no mass data found)
- Thorsen DH, Hale ME (2005) Development of zebrafish (*Danio rerio*) pectoral fin musculature. *J Morphol*, doi:10.1002/jmor.10374, PMID 16163704. **abstract**
- Carried over from S10 and S10-D without re-reading, at their read-levels:
  - Mead et al. 2020 (134.4 W/kg; 2.63 J/kg at 40 Hz; full-text in S10)
  - Marden 1987 (54–63 N/kg; search-summary)
  - red-muscle 5–10 W/kg (search-summary)
- Bluegill SICB conference abstracts (sicb.org/?p=29961, ?p=29963): **could-not-access** (host does not resolve)

```swarm-result
{"subproblem": "S10-D-D", "evidence": "derived",
  "answer": "S10-D's burst verdict is tied for sensitivity among f, R, M and muscle power, none of which flips it at x2, and f is the weakest by evidence; re-reading the proxy shows it is a four-muscle sum that undercounts the pectoral system (zebrafish has seven pectoral fin muscles; in bluegill the two largest are half the girdle muscle), so the improved f is 0.014-0.028 (central ~0.016), which narrows the generous burst shortfall from x5.4 to x4.6 (x2.7 at the upper bracket) without closing it, while a measured, f-independent bluegill pectoral output of 0.15-0.21 W/kg body leaves sustained hover (10.1 W/kg body, computed) 48-67x short, so S10-D stands with its enlargement factor revised to ~x2.7-14.5.",
  "key_number": "f = 0.014-0.028 (pectoral muscle mass / body mass, both fins; central ~0.016; Abudefduf saxatilis 0.69%/fin corrected by the bluegill 'two largest = half girdle mass' ratio) - proxy, no zebrafish measurement",
  "verdict": "stands",
  "depends_on": [
    "S10-D: f proxy 0.69% body mass per pectoral fin, Abudefduf saxatilis (Mansuit & Herrel 2021 Table 1, full-text; compiled from Thorsen & Westneat 2005, abstract only)",
    "Jones, Lucey & Ellerby 2007 (abstract): two largest pectoral adductor/abductor muscles = half of total pectoral girdle muscle mass in bluegill",
    "Jones, Lucey & Ellerby 2007 (abstract): Pmech 0.15-0.21 W/kg body during maximal labriform swimming",
    "Siomava et al. 2018 (full-text): adult zebrafish has seven pectoral fin muscles",
    "inference: zebrafish pectoral muscle fraction <= labriform damselfish (zebrafish fins used for maneuvering; Thorsen & Hale 2005 abstract)",
    "Mead et al. 2020: larval zebrafish fast muscle 134.4 W/kg at 80 Hz, 28 C (measured)",
    "S10 calculation: 105 W/kg at 40 Hz from measured 2.63 J/kg per cycle",
    "measured fish red/slow muscle 5-10 W/kg sustained (S10, search-summary)",
    "Marden 1987: 54-63 N/kg max lift per flight-muscle mass (search-summary), giving f threshold 0.114-0.182",
    "S10 hover model: Rankine-Froude momentum theory, k=1.2, full disc, no inertial power",
    "design assumptions R = 2-4 cm semispan, M = 1.5-2.0 profile multiplier (S1/S2 not yet fixed)",
    "body mass m = 0.4 g, air density 1.2 kg/m^3",
    "assumption: forward-flight power reduction factor unknown (tested at 0.5 only)",
    "unknown: fast-muscle power at ~22 Hz design frequency",
    "scope: only pectoral (not axial) muscle powers the wing"
  ]}
```
