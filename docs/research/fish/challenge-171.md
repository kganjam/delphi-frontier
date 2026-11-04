# Challenge 171: adversarial review of S10-D-D (the burst-verdict sensitivity claim)

Claim under review: `docs/research/fish/S10-D-deepen.md` on branch
`claude/deepen-s10-sensitive-input-k9dp4p` (harvest `deepen-s10-sensitive-input-k9dp4p`).
Recorded evidence level: derived. Verdict claimed: S10-D **stands**; f = 0.014–0.028 (central ~0.016).

Script: `docs/research/fish/challenge_171_calc.py`. **Every number from it is a calculation**, made with
the same Rankine–Froude hover model the claim uses (k = 1.2, ρ = 1.2 kg/m³, m = 0.4 g). Nothing in it is
an observation.

**Bottom line: WEAKENED.** The verdict (S10-D stands; flapping flight fails in both its burst and sustained forms) survives,
and on my reading it is slightly firmer than the author says. But two parts of the claim do not hold as
written:
1. The upper bracket f = 0.028 (and with it the "×2.7" low end of the revised enlargement factor)
   contradicts the ratio it is said to come from.
2. The bluegill 0.15–0.21 W/kg body figure is called "measured" and "f-independent". The source's
   abstract says it is an *estimate*, and it depends on bluegill's own muscle mass.

---

## 1. Independent arithmetic (calculation)

- W = 0.4e-3 × 9.81 = 3.924 mN. P_ind = 1.2 · √(W³ / (2ρπR²)) = **2.686 mW** at R = 4 cm.
- M · P_ind / m = **10.07 W/kg body** (M = 1.5). This matches the author's 10.1.
- Requirement per kg of muscle at f = 0.0138, 0.0164 and 0.0276 is 730, 614 and 365 W/kg. These match
  the author's figures.
- Shortfalls against 134.4 W/kg are ×5.43, ×4.57 and ×2.71. These also match.
- Body-mass flip factor: (134.4/730)² = 0.034. Matches.
- Bluegill check: 10.07 / 0.21 = ×48 and 10.07 / 0.15 = ×67. Matches.

**No arithmetic error found.**

## 2. Proxy check: the bracket on f is not internally consistent

I re-read the source (read-level: **abstract**, Europe PMC core record for PMID 17872996, fetched in
this session). The authors (Jones, Lucey & Ellerby 2007) write: "The maximal power output available from
the two largest pectoral fin adductor and abductor muscles, constituting half of the total pectoral girdle
muscle mass, was measured in vitro and used to estimate the muscle mechanical power output during maximal
labriform swimming (Pmech; 0.15–0.21 W kg⁻¹ body mass)."

What follows is my inference. If the "two largest = half of girdle" rule is carried over to *Abudefduf*
(Mansuit & Herrel 2021 Table 1, as quoted by the author: 0.13 / 0.23 / 0.15 / 0.18 % per fin, total 0.69):

| Pair taken as "the two largest" | Girdle total (%/fin) | f (both fins) | Consistent? |
|---|---|---|---|
| abd. profundus + add. profundus (actually the two largest) | 0.82 | 0.0164 | yes |
| abd. profundus + add. superficialis | 0.76 | 0.0152 | yes |
| abd. superficialis + abd. profundus | 0.72 | 0.0144 | yes |
| any pair summing to < 0.345 | < 0.69 | < 0.0138 | no (total below the four-group sum) |

- **Under that rule, the most the girdle total can be is 2 × (the largest pair) = 0.82 %/fin, so f = 0.0164.**
  The author's central value *is* the ceiling of the rule.
- The author's "upper bracket" assumes the four-group sum is half the girdle (1.38 %/fin). For
  *Abudefduf* that would make the two largest groups 0.41 / 1.38 = **30 %** of girdle mass, not the 50 %
  the source reports. So the upper bracket applies the cited ratio in a way the ratio itself rules out.
- The author does flag that the bluegill "half" ratio "may overcorrect". But the claim sentence still
  carries 0.028 and "×2.7" as results.
- The extra muscles the author worries about (arrector dorsalis and the other zebrafish fin muscles beyond
  four) are not a separate reason to go higher. The bluegill denominator is *total pectoral girdle muscle*,
  so it already includes them.

**Corrected bracket (calculation, proxy):** f ≈ **0.0138–0.0164**, both fins.
- Generous-case burst shortfall: ×4.6–5.4.
- Revised enlargement factor across the four geometries: ≈ **×4.6–14.5**, not ×2.7–14.5.
- An upper value above 0.0164 would need a source the claim does not have, for example a direct
  zebrafish dissection (the author's proposed measurement, §3d).

This correction makes the verdict *stronger*, not weaker.

## 3. Hidden assumptions, tested relaxed

- **"f-independent" sustained check.**
  - The abstract says Pmech was *estimated* from in-vitro power of only the two largest muscles, which are
    half the girdle mass.
  - So it is (a) a derived quantity, not a direct measurement, and (b) scaled by bluegill's own pectoral
    muscle mass. It is independent of the *damselfish proxy* f, not of muscle mass fraction in general.
  - Relaxed test (calculation): suppose the unmeasured other half of the girdle muscle doubled the power.
    The shortfall is then **×24–34** instead of ×48–67. The sustained "no" survives easily.
- **Labriform maximum ≠ muscle ceiling.** The author flags this, and I agree. The check bears on sustained
  flight, not burst.
- **Stacked generous errors (calculation).**
  - With my corrected ceiling f = 0.0164 plus the author's assumed forward-flight halving, the result is
    307 W/kg, **×2.28** short.
  - The author's closest approach, ×1.36, relied on the unsupported 0.0276.
  - So the "nearest flip" is further away than the claim says.
- **Muscle power at ~22 Hz is unknown** (the claim's own caveat). Flipping the generous case would need
  zebrafish fast muscle to reach ≥ 614 W/kg. That is about 4.6× the measured larval 134.4 W/kg.
  - I did not search for comparison values in other vertebrates. I give no number here rather than recall
    one unchecked.
- **Hover model.** Profile multiplier M = 1.5–2 at low Reynolds number, with no inertial power, is
  probably *generous* to flight. Relaxing it would raise the requirement.

## 4. Evidence-level honesty

- The overall level "derived" is honest. f is correctly labelled a proxy, and the calc file says every
  requirement is a calculation.
- **Defect:** the claim sentence calls Pmech "a measured, f-independent bluegill pectoral output". The
  source's abstract says "measured in vitro and **used to estimate**". Pmech is an author-derived estimate.
  The deepen file's body says this correctly ("measured in vitro, then scaled by the authors"); the
  headline sentence does not.

## 5. Counter-examples and regimes

- **Freshwater hatchetfishes (Gasteropelecidae)** have an enlarged pectoral girdle and are reported to beat
  their fins in air. They are the obvious counter-taxon. *My inference:* they illustrate the *enlarged*-f
  route that S10-D already treats as "requires enlargement". They do not show that present zebrafish
  anatomy suffices.
  - I did not retrieve a pectoral muscle mass fraction or a measured flight power for any gasteropelecid:
    `unknown`. Scope: no search was run for this in this session.
  - This is a gap the S10 chain should close, because it is the one living test case of the
    enlargement factor.
- **Flying fishes (Exocoetidae)** glide on caudal-fin taxiing, not pectoral flapping. They are not a
  counter-example to the burst-flapping "no". This is my statement from general knowledge, with no source
  retrieved this session.

## Verdict

**WEAKENED.**
- The verdict S10-D **stands** survives every relaxation I tried.
- But the claim's corrected value is overstated on the generous side:
  - f's supported range is 0.0138–0.0164, not up to 0.028.
  - The enlargement factor is ≈ ×4.6–14.5, not ×2.7–14.5.
- The f-independent check is an author-derived estimate, mislabelled "measured".

## Sources (read-levels)

- Jones EA, Lucey KS, Ellerby DJ (2007) *J Exp Biol* 210:3422–3429, PMID 17872996. **abstract** (Europe PMC
  REST, fetched this session).
- Mansuit R, Herrel A (2021) *Front Ecol Evol* 9:702576, Table 1. **listing**: values taken from the
  claim's quotation; I did not re-read the PDF.
- Mead et al. 2020 (134.4 W/kg): taken from the claim as given; **could-not-access** in this session (not
  attempted).
- Gasteropelecidae flight: no source retrieved (**could-not-access**; not searched).

```swarm-challenge
{"claim_id": 171, "outcome": "weakened",
  "reason": "Verdict 'stands' survives all relaxations, but the upper bracket f=0.028 contradicts the bluegill 'two largest = half girdle' ratio it cites (that ratio caps Abudefduf at 0.82%/fin, f=0.0164), so the x2.7 enlargement low end is unsupported, and the 0.15-0.21 W/kg body Pmech is an author-derived estimate scaled by bluegill muscle mass, not a measured f-independent value.",
  "corrected_value": "f = 0.0138-0.0164 (both fins, proxy); generous burst shortfall x4.6-5.4; enlargement factor ~x4.6-14.5",
  "depends_on": [
    "Jones, Lucey & Ellerby 2007 abstract: two largest pectoral adductor/abductor muscles = half of pectoral girdle muscle mass; Pmech 0.15-0.21 W/kg body estimated from in-vitro power",
    "Mansuit & Herrel 2021 Table 1 values for Abudefduf saxatilis (0.13/0.23/0.15/0.18 %/fin) as quoted by the claim",
    "assumption: bluegill girdle ratio transfers to Abudefduf/zebrafish",
    "Mead et al. 2020: 134.4 W/kg larval zebrafish fast muscle at 80 Hz (carried, not re-read)",
    "S10 hover model: Rankine-Froude, k=1.2, rho=1.2, m=0.4 g, R=2-4 cm, M=1.5-2",
    "assumption: forward-flight factor 0.5 tested only as a stress case",
    "unknown: fast-muscle power at ~22 Hz"
  ]}
```
