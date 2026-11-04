# S10-D-D-D: deepening S10-D-D by attacking its weakest input

**Parent chain** (each one is on its own branch):

| Step | File | Branch |
|---|---|---|
| S10 | `docs/research/fish/S10-tissue.md` | `claude/s10-tissue-flapping-power-2kag3x` |
| S10-D | `docs/research/fish/S10-deepen.md` | `claude/deepen-s10-flapping-muscle-wr33g7` |
| S10-D-D | `docs/research/fish/S10-D-deepen.md` | `claude/deepen-s10-sensitive-input-k9dp4p` |

The S10-D-D file carries the heading "S10-D-D". Its filename is `S10-D-deepen.md`.

**Side material, read in full:**
- `challenge-77.md` on branch `claude/challenge-s10-d-pectoral-muscle-vmlxc6`. It contains a forward-flight calculation.
- `replicate-77.md` on branch `claude/s10-d-verdict-qcqxez`.

**Calculation script:** `docs/research/fish/S10-D-D-deepen_calc.py`.
- Every requirement, ratio, frequency and extrapolated muscle power in this file is a **calculation**. None of them is an observation.
- The hover model is the same Rankine–Froude model used by S10, S10-D and S10-D-D.
- The forward-flight model is the one in `challenge_77_calc.py`. I re-implemented it, and my numbers match its output (ratio to hover 0.26 / 0.33 / 0.46).
- Measured values are marked as measured and carry a read-level.

## What S10-D-D concluded

S10-D-D found that S10-D's flight-muscle fraction f understated the pectoral muscle. It replaced f with **f = 0.014–0.028, central value 0.016**. On that basis it kept the burst verdict:

- **Burst verdict:** "burst flapping with present anatomy fails".
- **Generous hover case** (R = 4 cm, M = 1.5): the shortfall is **×4.6** at central f and **×2.7** at upper f, measured against **134.4 W/kg**.
- **Closest approach to flipping:** S10-D-D said the closest case was ×1.36. That case used upper f with forward flight at 0.5 × hover power, and the 0.5 was an assumption.
- **Verdict: STANDS.**
- **Unknowns it flagged:** "fast-muscle power at ~22 Hz design frequency" was listed as `unknown`. The verdict would reverse only if that power were at least the 80 Hz value.

---

## 1. Which input is S10-D-D's conclusion most sensitive to? (recomputed)

S10-D-D's verdict is a ratio:

> requirement (W/kg muscle) = M · P_ind(m, R) / (m · f), set against the comparator P_muscle

Four inputs enter linearly: f, M, 1/R and P_muscle. On the formula alone they tie. They separate in two ways: in **how far each could plausibly be wrong**, and in **which case is actually closest to the line**.

### 1a. S10-D-D missed its own closest case

S10-D-D tested forward flight only through an assumed factor of 0.5. Challenge-77 had already *computed* forward flight for the same wing, giving 0.26–0.46 of hover power at R = 4 cm. I combined that with S10-D-D's upper f and its comparator of 134.4 W/kg (calculation):

| Case (R = 4 cm, f = 0.0276) | Requirement (W/kg muscle) | Versus 134.4 W/kg |
|---|---|---|
| hover, M = 1.5 | 365 | ×2.71 short |
| forward flight, C_D,pro = 0.20 | 168 | ×1.25 short |
| forward flight, C_D,pro = 0.10 | 121 | **×0.90: verdict flips** |
| forward flight, C_D,pro = 0.05 | 97 | **×0.72: verdict flips** |

So S10-D-D's "burst fails" verdict was **already falling** at its most generous corner once two pieces were put together:
- its own upper f;
- a forward-flight number that already existed in the repository.

### 1b. Factor-of-two test on the comparator (calculation)

Take S10-D-D's own headline cases, all R = 4 cm, M = 1.5, hover:

| f | Requirement | Shortfall vs 134.4 | vs 67.2 (×0.5) | vs 268.8 (×2) |
|---|---|---|---|---|
| 0.0138 | 730 | ×5.43 | ×10.9 | ×2.71 |
| 0.0164 | 614 | ×4.57 | ×9.14 | ×2.28 |
| 0.0276 | 365 | ×2.71 | ×5.43 | ×1.36 |

In the forward-flight corners of §1a, a ×2 change in P_muscle moves the result across the line in either direction. f and M do the same; this is the tie noted above.

### 1c. Why I attack P_muscle and not f

**First, P_muscle has a known structural mismatch.** Mechanical power is work per cycle × cycle frequency.
- The comparator, 134.4 W/kg, was measured at **80 Hz**.
- S10 computed a design frequency of **~22 Hz** for the R = 4 cm wing. That geometry is the one that sets every generous case.
- Comparing a 22 Hz requirement against an 80 Hz power is therefore a frequency proxy. It is wrong by about ×(80/22) unless work per cycle rises in proportion as frequency falls.
- This is a factor-of-two-sized error that has an identified cause. It is not a guess.

**Second, P_muscle can be improved from the primary source, and f cannot.**
- The f sources are behind hosts that return 403 to this session: onlinelibrary.wiley.com for Thorsen & Westneat 2005, and journals.biologists.com for Jones et al. 2007 and Kendall et al. 2007.
- The Mead et al. 2020 full text is readable on pmc.ncbi.nlm.nih.gov.

f is also still weak; §5 has an f note.

## 2. How well is P_muscle = 134.4 W/kg established?

- **The value itself is measured.** I re-read the full text of Mead et al. 2020 (PMC7451861, HTML from pmc.ncbi.nlm.nih.gov, read-level **full-text**).
  - *Authors' claim:* "maximal net power … was produced at 80 Hz (134.4 ± 19.9 W/kg) and remained high (122.9 ± 11.1 W/kg) at 100 Hz".
  - *Authors' claim:* "Net work per active work loop decreased with increasing cycle frequency from 2.63 ± 0.18 J/kg of muscle at 40 Hz to 0.43 ± 0.27 J/kg at 120 Hz".
- **Conditions,** all as stated by the authors (full-text):
  - tested at 40, 60, 80, 100 and 120 Hz only;
  - 28 °C;
  - 8% sinusoidal strain (myotome length 1.01–1.09 × starting length);
  - one 0.4 ms supramaximal twitch pulse per cycle, with its phase optimised;
  - n = 5 tails from **5-day-old larvae**;
  - muscle mass estimated as CSA × myotome length × 1.06 g/cm³;
  - maximal isometric stress 76 ± 3 mN/mm²;
  - twitch/tetanus ratio 0.91.
- **As a comparator for this problem, it is a proxy three times over:**
  1. **Frequency.** It was measured at 80 Hz, not about 22 Hz. **Nothing below 40 Hz was measured.**
  2. **Life stage.** It comes from larvae, not adults. No adult zebrafish work-loop value was found (§3d gives the search scope).
  3. **Muscle.** It is axial myotome, not pectoral fin muscle.
- **Repetition, not measurement.** S10 used the 80 Hz value as the burst comparator for a ~22 Hz wing, while noting the frequency gap. S10-D, S10-D-D and Challenge-77 then carried 134.4 forward. Each step mentions the mismatch. None of them corrected for it. So the number is measured, but its *use* at 22 Hz is an assumption.

## 3. Improving it

### 3a. The design frequency depends on geometry (calculation)

I used S10's §3c method (C_L = 1.5, Φ = 120°, aspect ratio 6, r₂ = 0.55R). The method gives frequency ∝ 1/R².

| R | Design frequency | Comparator from measured data |
|---|---|---|
| 4 cm | **21.9 Hz** | below the measured range: extrapolation needed |
| 2 cm | **87.8 Hz** | inside the measured range: interpolating 80→100 Hz gives **130 W/kg** |

**Consequence:** the 2 cm cases were already compared at about the right frequency, and the 4 cm cases were not. Every *generous* case S10-D-D relied on uses R = 4 cm.

### 3b. Muscle power at 21.9 Hz from the measured data (calculation, not measurement)

Measured work per cycle (J/kg muscle):
- 2.63 at 40 Hz (measured);
- 1.68 at 80 Hz (134.4 / 80, derived);
- 1.23 at 100 Hz (122.9 / 100, derived).

| Reading | Work per cycle at 21.9 Hz | Power at 21.9 Hz | Assumption it rests on |
|---|---|---|---|
| plateau | 2.63 J/kg | **58 W/kg** | work per cycle stops rising below 40 Hz |
| linear | 3.06 J/kg | **67 W/kg** | the 40–80 Hz trend continues to 22 Hz |
| loop fill 0.70 | 4.02 J/kg | 88 W/kg | the loop becomes 0.70 of rectangular (measured fill is 0.46 at 40 Hz and 0.29 at 80 Hz) |
| **strict upper bound** | 5.74 J/kg | **126 W/kg** | rectangular loop: shortening force ≤ isometric stress (76 kPa × 0.08 / 1060 kg/m³) |

**Why the bound holds.** During shortening, muscle force cannot exceed isometric force, and this is what makes the rectangle a ceiling at 8% strain. It is a bound, not an estimate. Reaching it needs instantaneous activation and relaxation.

**Basis for the plateau reading.**
- At 21.9 Hz the shortening half-cycle lasts about 23 ms.
- *Authors' claim (full-text):* the twitch "is complete within 25 ms".
- *My inference:* a single twitch therefore spans roughly one shortening phase. Work per cycle would sit near its low-frequency plateau rather than keep climbing.
- This is untested below 40 Hz.

**Improved input:** P_muscle at the R = 4 cm design frequency is **58–67 W/kg** (central), with a bracket of **58–88 W/kg** at the measured 8% strain and a hard ceiling of **126 W/kg**. All four figures are below 134.4.

**These are calculations from measured larval data, not measurements at 22 Hz.**

### 3c. What this improvement cannot fix

- **Strain.** Work per cycle scales roughly with strain amplitude. A wing muscle need not run at 8%. Calculated values:

  | Loop fill | Strain | Power at 21.9 Hz |
  |---|---|---|
  | 0.46 | 12% | 87 W/kg |
  | 0.46 | 16% | 116 W/kg |
  | 0.70 | 12% | 132 W/kg |

  - *Authors' claim (full-text):* more than 90% of peak twitch force is available only between 0.95 and 1.05 × starting length.
  - Force outside that range is `unknown`. So strains above about 10% may not keep the same stress.
  - Optimal strain at 22 Hz is `unknown`.
- **Life stage.**
  - The data come from 5 dpf larvae.
  - S10 carried, at search-summary read-level, that cod fast muscle power falls as body size rises.
  - *My inference:* adult zebrafish fast muscle is therefore more likely lower than higher. This is unmeasured.
- **Muscle identity.** Pectoral abductor and adductor muscles have not been characterised by work loop in zebrafish.
  - *Authors' claim (Kendall et al. 2007, abstract):* in bluegill, the pectoral adductor profundus and abductor superficialis deliver maximal power at the gait-transition fin-beat frequency of 2.79 Hz.
  - That frequency is an order of magnitude below 22 Hz, so the bluegill data cannot serve as a 22 Hz comparator.

### 3d. Search for a better (direct) value

**Europe PMC REST search, run 2026-11-04.** Queries and hit counts:

| Query | Hits |
|---|---|
| `"work loop" AND zebrafish` | 17 |
| `"work loop" AND "Danio rerio"` | 8 |
| `zebrafish AND "muscle power" AND adult` | 77 (first 25 titles screened) |
| `"pectoral fin" AND "work loop"` | 1 (Kendall et al. 2007, bluegill) |
| `"pectoral" AND "muscle mass" AND "labriform"` | 7 |

**Result:**
- No adult zebrafish work-loop measurement was found.
- No zebrafish measurement at 15–35 Hz was found.
- No zebrafish pectoral muscle work loop was found.
- The only zebrafish work-loop data in these results are Mead et al. 2020.
- Ravel et al. 2025 (iScience, PMID 40124491, abstract) gives eleutheroembryo escape power from CFD. That is a whole-body estimate, not a muscle work loop, and I did not use it.

**Not searched:** Web of Science, Scopus, Google Scholar, theses, or the supplement of Mead 2020.

**Hosts that returned 403 to this session:** journals.biologists.com, onlinelibrary.wiley.com.

**Hosts that did not answer:** api.unpaywall.org, api.semanticscholar.org.

### 3e. Measurements that would settle it

1. **Cheapest.** Repeat Mead et al.'s larval protocol at **15, 20, 25 and 30 Hz**, with 8% and 12% strain and with 1–3 stimulus pulses per cycle.
   - Same preparation, same rig.
   - This gives work per cycle at the design frequency directly.
   - Effort: days for a lab that already runs it. Money cost: `unknown`.
2. **Decisive.** Run work loops on **adult** zebrafish pectoral abductor/adductor bundles at 15–90 Hz and 28 °C, sweeping strain from 6% to 16%.
   - Effort: weeks.
   - It needs a dual-mode lever rig. Cost `unknown`; I quote no price.

## 4. Recomputing S10-D-D with the improved input (calculation)

### Hover

Comparators: 134.4 (S10-D-D) / 58 (plateau) / 67 (linear) / 126 (strict bound) for R = 4 cm. For R = 2 cm the comparator is 130 W/kg in every reading.

| R, M | f | Requirement | vs 134.4 | vs 58 | vs 67 | vs 126 |
|---|---|---|---|---|---|---|
| 4 cm, 1.5 | 0.0164 (central) | 614 | ×4.57 | **×10.6** | **×9.15** | ×4.88 |
| 4 cm, 1.5 | 0.0276 (upper) | 365 | ×2.71 | ×6.32 | ×5.44 | ×2.90 |
| 4 cm, 2.0 | 0.0164 | 819 | ×6.09 | ×14.2 | ×12.2 | ×6.51 |
| 2 cm, 1.5 | 0.0164 | 1228 | ×9.14 | ×9.45 (vs 130) | — | — |
| 2 cm, 2.0 | 0.0276 | 973 | ×7.24 | ×7.49 (vs 130) | — | — |

### Forward flight, R = 4 cm (challenge-77 model, inputs as listed in that file)

| C_D,pro | f | Requirement | vs 134.4 | vs 58 | vs 67 | vs 126 (bound) |
|---|---|---|---|---|---|---|
| 0.05 | 0.0276 | 97 | **×0.72 (flips)** | ×1.67 | ×1.44 | **×0.77 (flips)** |
| 0.10 | 0.0276 | 121 | **×0.90 (flips)** | ×2.09 | ×1.80 | **×0.96 (flips)** |
| 0.20 | 0.0276 | 168 | ×1.25 | ×2.92 | ×2.51 | ×1.34 |
| 0.05 | 0.0164 | 162 | ×1.21 | ×2.82 | ×2.42 | ×1.29 |

### Where the most generous corner flips

The corner is R = 4 cm, upper f, C_D,pro = 0.05. It flips if P_muscle(21.9 Hz) ≥ **97 W/kg**. That needs:
- ≥ 4.40 J/kg per cycle, which is a loop fill of **0.77 at 8% strain**; the measured fill is 0.46 at 40 Hz;
- or, alternatively, a larger strain at a fill near the measured one.

### A design escape that does not work (calculation)

Raising the wingbeat frequency toward the 80 Hz optimum by narrowing the stroke angle Φ shrinks the swept area, which raises the induced power. Calculated for R = 4 cm, M = 1.5, f = 0.0276, swept sector Φ·R²:

| Φ | Frequency | Shortfall (plateau reading) |
|---|---|---|
| 120° | 22 Hz | ×7.75 |
| 60° | 44 Hz | ×5.68 |
| 33° | 80 Hz | ×6.34 |

The gain in muscle power and the loss in swept area roughly cancel, so this route does not close the gap.

A side finding: S10's full-disc area at Φ = 120° **understates** hover power by ×1.22 (calculation). That works against flight, so it does not threaten the verdict.

### Verdict: **STRENGTHENS** (with one stated exception)

- **Hover, R = 4 cm.** These are the generous cases that carried S10-D-D's burst verdict. The margin roughly doubles: at central f it goes from ×4.6 to **×9.2–10.6**, and at upper f from ×2.7 to ×5.4–6.3. This holds whichever measured-data reading is used, and even the strict bound leaves it at ×4.9 and ×2.9.
- **Hover, R = 2 cm.** Essentially unchanged (×1.03), because that wing already beats near 80 Hz.
- **Forward flight.** The corners that **flipped** under S10-D-D's own 134.4 comparator become "fails" again under the measured-data readings (×1.44–2.09). This depends on the 22 Hz work loop being no fuller than 0.77 at 8% strain.
- **The exception.** At the **strict rectangular bound** of 126 W/kg, the two most generous forward-flight corners still flip (×0.77, ×0.96). They also flip if the wing muscle runs at ≥ ~14% strain with an ordinary loop shape. I am not ruling this out; it is unmeasured. So the verdict is strengthened for every case that uses measured loop shapes, and **open** for the corner (upper f, forward flight, low profile drag, large strain).
- **Why not "stands":** the improved input moves every R = 4 cm margin by ×2.0–2.3 in the direction of infeasibility.
- **Why not "falls":** no reading of the measured data reaches 97 W/kg at 22 Hz and 8% strain. Only an idealised bound or an unmeasured strain does.

## 5. What this does not establish, and disagreements I am preserving

- **No measurement exists below 40 Hz.** Every 22 Hz value here is extrapolated from five larval tails.
- **The f input is still a proxy, and may be overcorrected.**
  - *Authors' claim (Jones et al. 2007, abstract):* "the two largest pectoral fin adductor and abductor muscles" are half the girdle muscle mass.
  - *Authors' claim (Kendall et al. 2007, abstract, same lab):* the "main upstroke (adductor profundus) and downstroke (abductor superficialis)" muscles were studied.
  - *My inference:* those are probably the same two muscles. If so, the matching *Abudefduf* pair (Mansuit & Herrel 2021 Table 1, carried from S10-D-D at full-text) sums to 0.18 + 0.13 = 0.31% per fin. Doubled, that is 0.62% per fin, which is *below* the four-muscle 0.69%.
  - In that case the bluegill rule gives no upward correction at all, and S10-D-D's upper f (0.0276) has no support.
  - I could not read either full text, so this is unconfirmed. It would further strengthen the verdict: at f = 0.0138 the most generous forward corner needs 193 W/kg.
- **Replicate-77 disagrees on geometry, and I am not reconciling it.** It computed requirements 2–6× higher (1,600–12,400 W/kg) using a 4–8 mm fin length, not the 2–4 cm design wing used here. That disagreement concerns R (a design input), not P_muscle. It points the same way as this file.
- **The forward-flight values are challenge-77's model** and inherit its assumptions: frontal area, body drag coefficient 0.4, C_D,pro 0.05–0.2, C_L,max 1.5, aspect ratio 6. The wingbeat frequency in forward flight was kept at the hover value. That is an assumption.
- **Out of scope:**
  - take-off and climb, which cost more than forward flight;
  - fatigue duration of the burst;
  - inertial power;
  - axial-muscle linkages.

## Sources (with read-levels)

- Mead AF, Kennedy GG, Palmer BM, Ebert AM, Warshaw DM (2020) Mechanical characteristics of ultrafast zebrafish larval swimming muscles. *Biophys J* 119:806–820. PMID 32755560, PMC7451861, https://pmc.ncbi.nlm.nih.gov/articles/PMC7451861/. **full-text**: Methods (work loops, stress, mass estimate) and Results (Fig. 8 text) read directly. The Fig. 8D/E data points at 60 Hz were not read, because they are in the image only. The Europe PMC fullTextXML endpoint returned HTTP 500.
- Jones EA, Lucey KS, Ellerby DJ (2007) *J Exp Biol* 210:3422–3429, doi:10.1242/jeb.005744, PMID 17872996. **abstract** (Europe PMC). Full text **could-not-access** (journals.biologists.com 403).
- Kendall JL, Lucey KS, Jones EA, Wang J, Ellerby DJ (2007) Mechanical and energetic factors underlying gait transitions in bluegill sunfish. *J Exp Biol*, doi:10.1242/jeb.009498, PMID 18055615. **abstract** (Europe PMC).
- Ravel G et al. (2025) *iScience*, doi:10.1016/j.isci.2025.112056, PMID 40124491. **abstract**; not used for any number.
- Thorsen DH, Westneat MW (2005) *J Morphol*, doi:10.1002/jmor.10173. **could-not-access** (onlinelibrary.wiley.com 403).
- Carried over without re-reading, at their recorded read-levels:
  - Mansuit & Herrel 2021 Table 1 (full-text in S10-D-D and Challenge-77);
  - cod power falling with size (search-summary, in S10);
  - challenge-77 forward-flight model (full-text, repository file).

```swarm-result
{"subproblem": "S10-D-D-D", "evidence": "derived",
  "answer": "S10-D-D's burst verdict is most exposed to its comparator, 134.4 W/kg measured at 80 Hz in larval zebrafish myotome, which was being set against a ~22 Hz wing (R = 4 cm). With challenge-77's forward-flight power and S10-D-D's upper f, that comparator already flipped the verdict (97-121 W/kg required). Re-reading Mead et al. 2020 in full shows no data below 40 Hz and 2.63 J/kg per cycle at 40 Hz, so the frequency-matched power at 21.9 Hz is calculated as 58-67 W/kg (58-88 at the measured 8% strain; hard ceiling 126). That doubles every R = 4 cm hover margin (central x4.6 to x9.2-10.6) and restores 'fails' in the forward-flight corners. The exception is an idealised rectangular loop or an unmeasured large strain, under which the most generous forward-flight corner (upper f, CDpro <= 0.1) still flips.",
  "key_number": "P_muscle at the 21.9 Hz design frequency = 58-67 W/kg muscle (calculated from measured 2.63 J/kg/cycle at 40 Hz; bracket 58-88 W/kg at 8% strain; strict upper bound 126 W/kg), replacing 134.4 W/kg measured at 80 Hz",
  "verdict": "strengthens",
  "depends_on": [
    "S10-D-D: f = 0.014-0.028 (central 0.0164), proxy from Abudefduf saxatilis 0.69%/fin x bluegill 'two largest = half girdle' ratio",
    "Mansuit & Herrel 2021 Table 1: Abudefduf saxatilis pectoral muscles 0.13/0.23/0.15/0.18% body mass per fin (full-text, carried)",
    "Jones, Lucey & Ellerby 2007 (abstract): two largest pectoral adductor/abductor = half pectoral girdle muscle mass (bluegill)",
    "Kendall et al. 2007 (abstract): main bluegill pectoral muscles are adductor profundus and abductor superficialis; max power at 2.79 Hz",
    "inference: Jones 2007 'two largest' = Kendall 2007 adductor profundus + abductor superficialis (unconfirmed)",
    "Mead et al. 2020 (full-text): larval zebrafish myotome net work 2.63 J/kg/cycle at 40 Hz, 134.4 W/kg at 80 Hz, 122.9 W/kg at 100 Hz, 28 C, 8% strain, single twitch per cycle, n=5; no data below 40 Hz",
    "Mead et al. 2020 (full-text): max isometric stress 76 mN/mm2, twitch/tetanus 0.91, twitch complete within 25 ms, muscle density 1.06 g/cm3, >90% twitch force only within 0.95-1.05 starting length",
    "assumption: work per cycle below 40 Hz plateaus at or modestly above the 40 Hz value (plateau / linear-trend readings)",
    "bound: net work per cycle <= isometric stress x strain / density (rectangular loop)",
    "assumption: wing muscle strain ~8% as in the larval work loops (power scales ~linearly with strain; optimal strain at 22 Hz unknown)",
    "assumption: larval axial myotome power stands in for adult pectoral fin muscle (no adult or pectoral zebrafish work loop found)",
    "S10 calculation: design wingbeat frequency 21.9 Hz at R = 4 cm (CL = 1.5, stroke 120 deg, AR 6, r2 = 0.55R), 87.8 Hz at R = 2 cm",
    "S10 hover model: Rankine-Froude momentum theory, k = 1.2, full disc, M = 1.5-2.0, no inertial power",
    "challenge-77 forward-flight model: body frontal area 2.2e-5 m2, CD body 0.4, CD profile 0.05-0.2, CLmax 1.5, AR 6; minimum power 0.26-0.46 of hover at R = 4 cm",
    "assumption: wingbeat frequency in forward flight equals the hover design frequency",
    "design assumptions R = 2-4 cm semispan (S1/S2 not fixed); replicate-77 disagreement on fin size (4-8 mm) preserved, not reconciled",
    "body mass m = 0.4 g, air density 1.2 kg/m3, g = 9.81 m/s2",
    "cod fast-muscle power falls with body size (search-summary, via S10) - direction of the larval-to-adult correction only",
    "scope: only pectoral (not axial) muscle powers the wing; take-off/climb, fatigue and inertial power not modelled"
  ]}
```
