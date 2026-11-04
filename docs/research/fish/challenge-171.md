# Challenge 171: adversarial review of S10-D-D (the improved pectoral-muscle fraction f)

**Claim under review.** Another agent wrote this claim; I did not. Source: `docs/research/fish/S10-D-deepen.md` on branch `claude/deepen-s10-sensitive-input-k9dp4p`.

> S10-D's burst verdict is tied for sensitivity among f, R, M and muscle power … the improved f is 0.014–0.028 (central ~0.016), which narrows the generous burst shortfall from ×5.4 to ×4.6 (×2.7 at the upper bracket) without closing it, while a measured, f-independent bluegill pectoral output of 0.15–0.21 W/kg body leaves sustained hover (10.1 W/kg body, computed) 48–67× short, so S10-D stands with its enlargement factor revised to ~×2.7–14.5.

- Recorded evidence level: derived.
- My script: `docs/research/fish/challenge_171_calc.py`. **Every number it prints is a calculation** using S10's Rankine–Froude hover model. None of them is an observation.

## Outcome: WEAKENED

**The verdict "S10-D stands" survives.** The key number does not hold up as derived.

The author raises f by transferring a bluegill muscle-mass ratio to *Abudefduf*, and the derivation has two problems:

- **The upper bracket (0.0276) contradicts the ratio it cites.** It treats the bluegill ratio as if four muscles made up half the girdle, when the ratio is about two muscles.
- **The central value (0.0164) depends on matching muscles by size rank.** It is not matched by muscle identity. If you match the same named muscles that bluegill uses as its main power muscles, the ratio gives *no* upward correction at all.

Both errors push f too high, which makes the burst case look closer than the evidence supports. The verdict therefore gets stronger, not weaker. But two of the claim's figures are not supported:

- "×2.7 at the upper bracket"
- the revised enlargement factor "×2.7–14.5"

---

## 1. Independent arithmetic

I wrote the hover formula from scratch: P_ind = k·W^1.5 / √(2ρπR²), with W = m·g, m = 0.4 g, ρ = 1.2 kg/m³ and k = 1.2. All results are calculations.

**Hover power per kg of body:**

| R | M | W/kg body |
|---|---|---|
| 4 cm | 1.5 | 10.07 |
| 4 cm | 2.0 | 13.43 |
| 2 cm | 1.5 | 20.14 |
| 2 cm | 2.0 | 26.86 |

This reproduces the claim's 10.1 W/kg body.

**Requirement per kg of muscle**, in the four geometries above in the same order, and the shortfall against 134.4 W/kg:

| f | Requirement (W/kg muscle) | Shortfall |
|---|---|---|
| 0.0138 | 730 / 973 / 1460 / 1946 | ×5.43–14.48 |
| 0.0164 | 614 / … / 1638 | ×4.57–12.18 |
| 0.0276 | 365 / … / 973 | ×2.71–7.24 |

**f-independent check:** 10.07 / 0.15 = 67× and 10.07 / 0.21 = 48×.

**Sensitivity:** the requirement scales linearly with M, 1/R, 1/f and 1/(power density), and with m^½. The "tie" among f, R, M and muscle power is correct, and none of them flips the verdict at ×2.

**Every one of the author's numbers reproduces.** The arithmetic has no errors. The faults below are in the inputs.

## 2. Proxy check: how the bluegill ratio was transferred

The quantity that matters is the total pectoral (fin plus girdle) muscle mass of adult zebrafish divided by body mass. That value is `unknown`. Neither the author nor I found a measurement; my own search scope is listed in §6.

The author's proxy has three parts:

- the *Abudefduf* four-group sum, 0.69% per fin;
- multiplied by a bluegill ratio;
- the ratio being: "the two largest pectoral fin adductor and abductor muscles, constituting half of the total pectoral girdle muscle mass" (Jones, Lucey & Ellerby 2007; I re-read the abstract myself, read-level **abstract**).

### Fault A: the upper bracket is inconsistent with the cited ratio

The author's "upper bracket" sets the girdle total to 2 × (four-group sum) = 1.38% per fin.

- On that total, *Abudefduf*'s two largest groups (0.23 + 0.18 = 0.41) would make up 0.41 / 1.38 = **30%** of the girdle (calculation).
- The bluegill ratio being transferred says they make up **50%**.

So the 0.0276 bracket does not apply the ratio. It replaces it with a different assumption that has no source behind it.

The only way to rescue it is to read "the two largest … adductor and abductor muscles" as meaning the whole abductor mass plus the whole adductor mass (superficialis and profundus combined). The next paragraph shows that this reading does not hold.

### Fault B: matching by rank versus matching by identity

**Which muscles are bluegill's main power muscles.** A sibling paper from the same lab names them:

- *Authors' claim (Kendall, Lucey, Jones, Wang & Ellerby 2007, J Exp Biol, abstract via Europe PMC, read-level **abstract**):* "the main upstroke (adductor profundus) and downstroke (abductor superficialis) muscles".
- Jones, Jong & Ellerby (2008, abstract) likewise ran work loops on the abductor superficialis.
- **My inference, not stated in Jones et al. 2007:** the "two largest" muscles in Jones et al. 2007 are the abductor superficialis and the adductor profundus. I could not confirm this from the full text: journals.biologists.com and doi.org both returned HTTP 403 from this session, and the paper is not in PMC.

**Two ways to transfer the ratio.** Rank matching takes whichever two muscles are largest in *Abudefduf*. Identity matching takes the same named muscles that bluegill uses.

| Reading | Abudefduf pair (% body per fin) | Pair's share of the four-group sum | Girdle total ×2 (per fin) | f (both fins) | Generous burst shortfall |
|---|---|---|---|---|---|
| Rank (the author's) | AbP 0.23 + AdP 0.18 = 0.41 | 0.59 | 0.82% | 0.0164 | ×4.57 |
| Identity (mine) | AbS 0.13 + AdP 0.18 = 0.31 | 0.45 | 0.62% | 0.0124 | ×6.04 |

**What the identity reading shows.** Under it, the bluegill ratio predicts a girdle total (0.62%) *smaller* than the four groups already measured (0.69%). That cannot be right: the muscles counted already exceed the predicted total. My inference is that the bluegill ratio does not transfer to *Abudefduf* at all, because the two species apportion their pectoral muscles differently. In bluegill, AbS is a main muscle. In *Abudefduf* it is the smallest of the four groups.

**What still stands.** The measured four-group sum, 0.0138, remains a floor. The muscles it leaves out (the arrector, girdle-to-body muscles, and the extra zebrafish muscles; the author's sources: Thorsen & Westneat 2005 abstract, Siomava et al. 2018 full text) are real. However, their mass is `unknown`. The bluegill ratio does not supply it.

**Corrected value.** The best-supported range is f ≥ 0.0138, with 0.0164 as a soft upper value that depends on the rank reading. The upper bracket of 0.0276 is unsupported. On that range, the generous burst shortfall is **×4.6–5.4**, not ×2.7. The enlargement factor across all geometries becomes about **×4.6–14.5**, not ×2.7–14.5 (calculation).

The author also expects zebrafish to fall *below* the labriform damselfish value. That is the author's inference, and nothing I found contradicts it. If it is right, the shortfall is larger again.

## 3. Hidden assumption: the "measured, f-independent" bluegill output

The claim calls 0.15–0.21 W/kg body "measured" and "f-independent". Neither label is accurate.

**Evidence level.**

- *Authors' claim (abstract):* the maximal power of the two largest muscles "was measured in vitro and **used to estimate** the muscle mechanical power output during maximal labriform swimming".
- So the number is an estimate derived from a measurement. The author's body text says this correctly ("measured in vitro, then scaled"). The summary claim drops the qualifier. That is a labelling defect.

**f-dependence.**

- Power per kg of body equals bluegill's muscle-specific power times *bluegill's own* pectoral muscle fraction. It does not depend on the *Abudefduf* proxy, but it does depend on f.
- Applying it to zebrafish assumes zebrafish has a pectoral fraction equal to that of a labriform specialist. That is a generous assumption, so it is a safe one for a "no" verdict.

**The assumption relaxed.**

- The abstract says the power came from the two muscles that form half the girdle. It is unclear whether Pmech counts only those two or was scaled up to the whole girdle; the full text could not be accessed.
- If it counts only those two, the whole girdle could deliver up to about 2× as much: 0.30–0.42 W/kg body. Sustained hover would then be **24–34×** short, not 48–67× (calculation). That is still nowhere near closing the gap.

**Is Pmech near the ceiling?** Kendall et al. 2007 (authors' claim, abstract) say that available pectoral power "was maximal at the gait transition point", and that bluegill change gait "to recruit additional muscle mass". So Pmech at the maximal labriform speed is near the ceiling of the pectoral system. The comparison is therefore fair for sustained hover. It says nothing about the burst ceiling, and the author already notes this.

## 4. Regimes and counter-examples

**Freshwater hatchetfish (Gasteropelecidae).** Pectoral muscles are reported at about 25% of body mass, and powered flight is reportedly not achieved (Wiest 1995). Both points come from challenge-77, at read-level **search-summary**; I did not re-read them.

- This is not a counter-example to "stands": a fish with a large f still does not fly.
- It does mean the enlargement factor is a necessary condition, not a sufficient one.

**Forward flight.** Challenge-77 computed a forward-flight minimum of 0.26–0.33 × hover (calculation, several assumed inputs), which gives a generous-case shortfall of ×1.4–1.8 at f = 0.0138.

- Combining that with the author's unsupported 0.0276 would take the requirement below 134.4 W/kg, and the burst verdict would flip.
- This is the practical consequence of Fault A. The upper bracket is the input that comes closest to overturning the burst "no", and it has no source.
- With f ≤ 0.0164, the forward-flight case stays above the measured muscle power: 1.4 × 0.0138 / 0.0164 ≈ ×1.2 (calculation, stacked assumptions). The margin is thin, and it depends on the forward-flight model, not on f.

## 5. Things I tried to break that held

- **The sensitivity tie and the ×2 non-flip:** confirmed by calculation.
- **f as the weakest input on evidence:** agreed. The 134.4 W/kg is measured (carried from S10), while f is a cross-species proxy.
- **The sustained "no":** it survives every relaxation I tried, with the shortfall staying at 24× or more.

## 6. Sources and scope

**Read by me for this review:**

- Jones EA, Lucey KS, Ellerby DJ (2007), *J Exp Biol* 210:3422, doi:10.1242/jeb.005744. **abstract** (Europe PMC). Full text **could-not-access**: HTTP 403 at journals.biologists.com and doi.org; not in PMC.
- Kendall JL, Lucey KS, Jones EA, Wang J, Ellerby DJ (2007), *J Exp Biol*, on gait transitions in bluegill. **abstract** (Europe PMC search result).
- Jones EA, Jong AS, Ellerby DJ (2008), *J Exp Biol*, on temperature and bluegill swimming. **abstract** (Europe PMC search result).

**Not re-read by me:**

- Mansuit & Herrel 2021, Table 1 values. Taken as quoted identically by the author and by challenge-77, both of which report a **full-text** read.
- Siomava et al. 2018 and Thorsen & Westneat 2005, at the author's read-levels.
- Mead et al. 2020 (134.4 W/kg), at S10's read-level.
- Wiest 1995 and the hatchetfish figures, **search-summary** via challenge-77.

**Negative search scope:**

- One Europe PMC query: `bluegill pectoral "abductor" muscle`, first 10 results.
- I searched for no zebrafish muscle mass data beyond what the author reported.
- I did not search Web of Science, Scopus, or any paper's supplements.

```swarm-challenge
{"claim_id": 171, "outcome": "weakened", "reason": "Arithmetic and the 'stands' verdict hold, but the f upper bracket 0.0276 contradicts the bluegill 'two largest = half' ratio it cites and the 0.0164 central value relies on rank-matching muscles, whereas identity-matching to bluegill's main power muscles (AbS + AdP, Kendall et al. 2007 abstract) predicts a total below the measured four-group sum, so the ratio supports no upward correction and the burst shortfall is x4.6-5.4, not x2.7, with the bluegill Pmech an estimate rather than a measurement.", "corrected_value": "f = 0.0138-0.0164 (both fins; 0.0138 is the measured four-group floor, upper value unknown, 0.0276 unsupported); generous burst shortfall x4.6-5.4; enlargement factor ~x4.6-14.5", "depends_on": ["Mansuit & Herrel 2021 Table 1: Abudefduf saxatilis AbS 0.13, AbP 0.23, AdS 0.15, AdP 0.18, total 0.69 % body mass per fin (full-text per author and challenge-77; not re-read by me)", "Jones, Lucey & Ellerby 2007 abstract: two largest pectoral adductor/abductor muscles = half of pectoral girdle muscle mass; Pmech 0.15-0.21 W/kg body estimated from in-vitro measurement", "Kendall et al. 2007 abstract: bluegill main upstroke muscle adductor profundus, downstroke abductor superficialis; pectoral power maximal at gait transition", "inference: Jones 2007 'two largest' = AbS + AdP (full text could-not-access)", "Mead et al. 2020: 134.4 W/kg larval zebrafish fast muscle, 80 Hz (via S10)", "S10 hover model: Rankine-Froude, k=1.2, m=0.4 g, rho=1.2, R=2-4 cm, M=1.5-2.0", "challenge-77 forward-flight calculation 0.26-0.33 x hover (assumed inputs)"]}
```
