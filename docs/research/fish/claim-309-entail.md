# Claim 309: what it requires at the cell and organ scales

**Source claim (tissue, measured):** the fast myotomal fibres of *Scorpaena notata*
(a scorpionfish, Scorpaenidae) produced a mean muscle-mass-specific power of
142.7 W kg⁻¹ at 20 °C. This was measured by work loop at in vivo strain and shortening
duration. The authors report that power predicted from swimming sequences matched the
work-loop power at all temperatures tested.

**Subject of every constraint below: *Scorpaena notata*, 20 °C, fast (white) myotomal muscle.**
This claim is not about zebrafish, and no constraint here is about zebrafish. Where I bring in
a number from another species, I name that species in the same sentence. A number like that
cannot satisfy or refute a constraint. It only shows the order of magnitude.

## Sources and read-levels

| # | Source | Read-level | Used for |
|---|---|---|---|
| S1 | Wakeling JM & Johnston IA (1998) Muscle power output limits fast-start performance in fish. *J Exp Biol* 201(10):1505–1526. doi:10.1242/jeb.201.10.1505 | **abstract** (journal page; full text paywalled, and silverchair PDF host refused by session proxy) | the claim itself; the organ-scale power match; mention of sonomicrometry / gearing ratios |
| S2 | Wakeling JM (2001) Biomechanics of fast-start swimming in fish. *Comp Biochem Physiol A* 131:31–40. PMID 11733164 | **search-summary** | strain uniformity along the body; "performance limited by maximum muscle power" |
| S3 | Johnston IA & Altringham JD (1985) *Pflügers Arch* 405:136–140. doi:10.1007/BF00584534 | **search-summary** (Springer refused by session network) | skinned-fibre force–velocity; species = icefish, cod, blue marlin, **not *Scorpaena*** |
| S4 | *Myoxocephalus scorpius* (short-horn sculpin) fibre Vmax values: skinned 1.54 L₀ s⁻¹ at 20 °C; and 8.7 vs 5.3 fibre lengths s⁻¹ at 20 °C in 15 °C- vs 5 °C-acclimated fish (JEB 198:193 and related sculpin papers) | **search-summary**. The search tool returned these numbers, and I could not open the papers to check which preparation (skinned or intact) each refers to. | cross-species order of magnitude only |
| S5 | Fish white-muscle PCr/ATP depletion during burst exercise (rainbow trout; Atlantic salmon; Pearson, Spriet & Stevens 1990 *J Exp Biol* 149:45) | **search-summary**. No concentration values were returned, and the PDF host was refused. | qualitative only |

Network note: these hosts were unreachable from this session: `cob.silverchair.com` (JEB PDFs),
`link.springer.com`, `ouci.dntb.gov.ua`, `www.sciencegate.app` and
`acnpsearch.tweb-dev.unibo.it`. Every figure from S1 that is not in its abstract is therefore
`unknown` here. That includes the in vivo strain, the shortening duration, the muscle mass
fraction and the hydrodynamic power values. It is not known to be absent from the paper.

---

## Constraints

### C1. Cell, `range`: the fibres' force–velocity product must be large enough

**Requirement.** Fast fibres must have an isometric stress P₀ and an unloaded shortening
velocity V_max whose product can deliver at least 142.7 W kg⁻¹. Power per unit volume is
stress × strain rate. For a Hill-type fibre, peak isotonic power is about k·P₀·V_max, with
k ≈ 0.1 (an *assumed* typical value for vertebrate fast muscle, not measured here). Muscle
density is ρ ≈ 1060 kg m⁻³ (assumed). The requirement is therefore:

  P₀·V_max ≥ 142.7 × 1060 / 0.1 ≈ **1.5 × 10⁶ N m⁻² s⁻¹** (that is, Pa · L₀ s⁻¹).

This is *derived* (calculated), not observed. It is a lower bound only. A work loop at in vivo
strain usually delivers less than peak isotonic power, so the true requirement is higher.
At P₀ = 150–300 kPa it needs V_max ≥ 10–5 L₀ s⁻¹ (calculated).

**Check.** I found no measurement of P₀ or V_max for *S. notata* fast fibres.
- Search scope: web searches for "Scorpaena" with fast muscle / skinned fibres / Vmax /
  temperature / Johnston, and for "Scorpaena notata" with work loop / twitch. Both searches
  returned nothing species-specific. This means "my searches did not find it". It does not
  mean "people looked and found nothing". S1's full text may contain fibre data I could not
  read.
- Cross-species numbers only:
  - *Myoxocephalus scorpius* (S4): V_max of 8.7 L s⁻¹ at 20 °C in 15 °C-acclimated fish. With
    P₀ ≥ ~175 kPa this would meet the bound (calculated).
  - The same species skinned gives 1.54 L₀ s⁻¹ at 20 °C. That would need P₀ ≈ 1 MPa, which
    is implausible.
  - These two sculpin numbers disagree by about 5×, and I do not average them. My inference
    is that the difference is skinned versus intact preparation, but I could not confirm the
    preparation for either.
  - S3: skinned fibres of icefish, cod and blue marlin.
- None of these is *Scorpaena*. **Status: open.**

### C2. Cell, `timescale`: activation and relaxation must fit inside the shortening phase

**Requirement.** Net positive work in a single fast-start shortening needs the fibre to switch
on and off quickly enough. The time for force to rise (activation) plus the time for force to
fall (relaxation) must be no longer than the in vivo shortening duration. As a ratio,
(t_activation + t_relaxation) / t_shortening ≤ ~1. If relaxation is slow, force persists into
re-lengthening and the net work falls toward zero. Mean power of 142.7 W kg⁻¹ would then not
be reachable at in vivo timing.

**Check.** The *S. notata* shortening duration at 20 °C is in S1, but only in the full text,
which I could not read (the abstract gives no ms values). I found no twitch or tetanic
time-course for *S. notata* fast fibres (same search scope as C1).
- There is a weak argument from S1's own result: a work loop *at in vivo shortening duration*
  produced 142.7 W kg⁻¹, which means the kinetics were fast enough in that preparation. That
  argument is circular, because it is the claim itself, so I do not count it as an independent
  satisfaction.
- **Status: open.**

### C3. Cell, `energetic`: ATP must be turned over fast enough

**Requirement.** Mechanical power of 142.7 W kg⁻¹ at a cross-bridge efficiency η of 0.2–0.5
(assumed range), with ΔG_ATP ≈ 55 kJ mol⁻¹ (assumed), requires:
- chemical power of 285–714 W kg⁻¹, and
- ATP turnover of about **5–13 mmol kg⁻¹ s⁻¹** (calculated).

That turnover must be met by stored ATP plus phosphocreatine (PCr) during the start. These
reserves turn over almost instantly, and glycolysis and oxidative metabolism are too slow to
contribute within a ~0.1 s event.

If the start lasted ~0.1 s (assumed; S1's real duration is unknown to me), total ATP needed is
about 0.5–1.3 mmol kg⁻¹ (calculated). Resting ATP + PCr in teleost white muscle is commonly
quoted in the tens of mmol kg⁻¹. I could not retrieve a source number in this session, so I
use that only as a statement of what to look up, not as evidence.

**Check.** For *S. notata* I found no ATP, PCr or myofibrillar ATPase data. S5 confirms
qualitatively that PCr is the first fuel used in teleost burst swimming (rainbow trout,
Atlantic salmon), but gave no values. **Status: open.** If a measured value is found, I expect
the constraint to be satisfied by a wide margin, but that is an expectation, not a check.

### C4. Organ, `energetic`: muscle power must balance the work done on the body and water

**Requirement.** Power is conserved at the whole-myotome level. Fast-muscle mass × 142.7 W kg⁻¹
must be at least the rate of work done on the water plus the rate of change of the body's
kinetic energy during the start. If the hydrodynamic and inertial demand were clearly larger,
the tissue measurement could not be the power source.

**Check.**
- *Authors' claim* (S1, abstract): "predicted power outputs from swimming sequences were similar
  to the muscle power outputs measured from work-loop experiments at all temperatures", for the
  same species in the same study.
- The swimming-sequence side is **calculated** from kinematics with a hydrodynamic model. It is
  not a direct measurement of power. So the balance is a measured muscle value matched to a
  calculated demand.
- S2 (search-summary) restates the authors' conclusion: maximum fast-start performance is
  limited by the maximum muscle power available.
- *My inference:* this is the same paper that produced the claim, so it is the study's own
  consistency check rather than independent confirmation. The muscle mass fraction and the
  absolute hydrodynamic power values are `unknown` to me (abstract only).

**Status: satisfied** (literature, abstract-level, same species, not independent).

### C5. Organ, `spatial`: fibre strain from body curvature must match the strain used in the work loop

**Requirement.** The in vivo strain imposed in the work loop has to be the strain the fibres
really undergo. That strain is body curvature × distance from the neutral axis, divided by the
gearing that comes from helical fibre geometry. It should agree with directly measured
(sonomicrometry) strain within a factor of ~1.5, and be broadly similar along the body. Other
requirements:
- Fibre length change per bend must stay within the working range of the sarcomere
  length–tension curve.
- If the true strain were much larger or smaller, the 142.7 W kg⁻¹ would be power at the
  wrong operating point.

**Check.**
- S1's abstract says that cross-validation with sonomicrometry studies let the authors calculate
  red-to-white gearing ratios. It does not say which species those sonomicrometry studies used.
  I could not confirm that they were *S. notata*, and the field's sonomicrometry fast-start work
  is mostly on sculpin and carp.
- S2 (search-summary): gearing ratios decrease toward the tail as muscle geometry changes, so
  white-fibre strains are similar in all myotomes. That is a general statement, and not tied to
  *S. notata* in the summary I saw.
- The strain amplitudes for *S. notata* are `unknown` (full text not accessible).
- **Status: open.**

---

## Summary

| # | Scale | Kind | Status | Why |
|---|---|---|---|---|
| C1 | cell | range | open | No *S. notata* P₀ or V_max found. Sculpin numbers disagree with each other (5×). |
| C2 | cell | timescale | open | Shortening duration is behind a paywall. No *S. notata* twitch kinetics found. |
| C3 | cell | energetic | open | The demand was calculated, but no *S. notata* ATP/PCr data was found. |
| C4 | organ | energetic | satisfied | Authors' own power match, same species. It is circular-adjacent, and the hydrodynamic side is calculated. |
| C5 | organ | spatial | open | The species behind the sonomicrometry is unconfirmed, and strain values are unknown. |

**Nothing is unsatisfiable.** No measured number I found contradicts any constraint. Every
cross-species number (sculpin, cod, icefish, marlin, trout, salmon) is explicitly about a
different animal from the claim, so none could have been used to refute it.

**What would decide the open ones.** In order:
1. Read the full text of S1, for *S. notata* strain, shortening duration and muscle fraction.
2. Find any *S. notata* fast-fibre force–velocity or twitch data.
3. Find a measured teleost white-muscle ATP/PCr value at rest.

```swarm-entail
{"source_claim": 309, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "range",
      "statement": "Fast myotomal fibres must have an isometric stress times unloaded shortening velocity product large enough that peak isotonic power (~0.1 P0 Vmax / rho) is at least the measured work-loop power",
      "quantity": "P0 * Vmax of Scorpaena notata fast fibres at 20 C", "lo": 1.5e6, "hi": null, "units": "N m^-2 s^-1 (Pa * L0/s)",
      "status": "open",
      "satisfied_by": "Not found for Scorpaena notata. Searched web for 'Scorpaena' + fast muscle/skinned fibres/Vmax/temperature/Johnston and 'Scorpaena notata' + work loop/twitch; no species-specific fibre mechanics returned. Cross-species only: Myoxocephalus scorpius Vmax 8.7 L/s at 20 C (15 C-acclimated) vs 1.54 L0/s skinned at 20 C -- these disagree ~5x and are not averaged.",
      "satisfied_evidence": "unknown",
      "note": "Bound is derived (calculated) assuming k=0.1 Hill power ratio and rho=1060 kg/m3; it is a lower bound since work-loop power < isotonic peak. Sculpin values: search-summary read-level, preparation (skinned vs intact) unconfirmed. Johnston & Altringham 1985 Pflugers Arch 405:136 (icefish, cod, marlin; search-summary). Negative = my searches did not find it, not that it was looked for and absent; Wakeling & Johnston 1998 full text unread."},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "Fibre activation plus relaxation time must not exceed the in vivo shortening duration, otherwise force persists into re-lengthening and net positive work collapses",
      "quantity": "(t_activation + t_relaxation) / t_shortening", "lo": null, "hi": 1, "units": "ratio",
      "status": "open",
      "satisfied_by": "No Scorpaena notata twitch/tetanus kinetics found (same search scope as C1). The in vivo shortening duration is in Wakeling & Johnston 1998 full text, not in the abstract, and was not accessible. The work loop succeeding at in vivo duration is the claim itself and is not counted as independent satisfaction.",
      "satisfied_evidence": "unknown",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505 -- abstract read-level only (paywall; PDF host refused by session proxy)."},
    {"target_scale": "cell", "kind": "energetic",
      "statement": "Phosphagen (ATP + phosphocreatine) turnover in fast fibres must supply chemical power of mechanical power / efficiency for the duration of the start",
      "quantity": "ATP turnover rate required for 142.7 W/kg at efficiency 0.2-0.5", "lo": 5, "hi": 13, "units": "mmol ATP kg^-1 s^-1",
      "status": "open",
      "satisfied_by": "Demand calculated (assumed efficiency 0.2-0.5, dG_ATP 55 kJ/mol). No Scorpaena notata ATP, PCr or myofibrillar ATPase data found. Teleost burst-exercise literature (rainbow trout, Atlantic salmon) confirms qualitatively that PCr is the first fuel used, but no concentrations were retrieved.",
      "satisfied_evidence": "derived",
      "note": "Range is calculated, not measured. Trout/salmon sources (e.g. Pearson, Spriet & Stevens 1990 J Exp Biol 149:45) search-summary only, different species. Expected to be satisfied by a wide margin if a stored-phosphagen value is found, but that is an expectation, not a check."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "Whole fast-myotome power (muscle mass x mass-specific power) must at least match the hydrodynamic plus body-inertial power demanded during the fast-start",
      "quantity": "ratio of measured muscle power to kinematics-predicted power demand", "lo": 1, "hi": null, "units": "ratio",
      "status": "satisfied",
      "satisfied_by": "Authors report predicted power outputs from swimming sequences were similar to work-loop muscle power outputs at all temperatures, same species (Scorpaena notata) and same study.",
      "satisfied_evidence": "literature",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505, abstract read-level. Demand side is calculated from kinematics with a hydrodynamic model, not measured. Same paper as the claim, so not independent. Muscle mass fraction and absolute hydrodynamic power values unknown (full text inaccessible). Wakeling 2001 CBP-A 131:31 (search-summary) restates that fast-start performance is limited by maximum muscle power."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "Fibre strain inferred from body-midline curvature, distance from the neutral axis and fibre-helix gearing must match directly measured fibre strain within about a factor of 1.5, and stay within the working range of the sarcomere length-tension relation",
      "quantity": "curvature-derived strain / directly measured strain", "lo": 0.67, "hi": 1.5, "units": "ratio",
      "status": "open",
      "satisfied_by": "Abstract states cross-validation with sonomicrometry studies allowed red-to-white gearing ratios to be calculated, but does not say which species the sonomicrometry was on; Scorpaena notata strain amplitudes not accessible. Wakeling 2001 (search-summary) says white-fibre strains are similar in all myotomes, as a general statement not tied to Scorpaena notata.",
      "satisfied_evidence": "unknown",
      "note": "Wakeling & Johnston 1998 (abstract); Wakeling 2001 Comp Biochem Physiol A 131:31-40 (search-summary). Field sonomicrometry fast-start data are mostly sculpin and carp -- different species, so cannot satisfy this. Factor-1.5 tolerance is my choice, not from a source."}
  ]}
```
