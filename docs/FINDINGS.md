# Can a zebrafish be engineered to fly?

**No. And the interesting part is how precisely no, and why two unrelated attempts fail for
different reasons.**

This is the top-level account. Every number below is recorded in the project graph with its
evidence level and source; the [subproblem board](../library/pages/project/board.md) shows what is
open and what each question is blocked on.

---

## The answer in one table

| | Required | Available | Short by |
|---|---|---|---|
| Water-exit speed | 4.37 m/s | 0.45–1.38 m/s *measured* | **3.2×** |
| Launch kinetic energy | 3.82 mJ | — | **10×** |
| Tail-beat for a taxi | 132–199 Hz | 52 Hz *measured* | **2.5–3.8×** |
| Pectoral muscle fraction | 7.5–20% | 1.4% *measured* | **5–15×** |
| Muscle energy per stroke (spring route) | 98.5 J/kg | 8.6 J/kg *delivered* | **1.9×** |

The best design buildable from **demonstrated** alleles is the zebrafish that already exists — the
Daane *lat4a^nr21/+; kcnh2a^lof/+* double heterozygote. Granting it an unmeasured one-body-length
wing, it produces **10% of body weight in lift at launch** and lengthens a 19.4 cm ballistic leap by
**3–6 mm**.

**The honest deliverable is a possibly detectable 5–10% reduction in ascent deceleration.** Not
flight, not a glide, not a meaningfully longer leap. Calling it flight would destroy the credibility
of everything else here.

---

## Why the negative is worth more than a maybe

Two **independent representations** were tried, and they fail on **different terms**:

1. **Build a better wing** — more span, more area, stiffer rays. Fails on **lift and launch speed**,
   by ≥10× on energy.
2. **Store the launch energy** — latch-mediated spring actuation, the mechanism fleas, froghoppers
   and mantis shrimp use to beat muscle power limits by orders of magnitude. Fails on **muscle
   energy per stroke**, by 1.9×.

The second route *removes the power wall entirely*: spring volume needs only **1–4% of body volume**,
and the required 7400–18400 W/kg sits **within measured insect LaMSA** (36,000–74,000 W/kg). It
still fails, because break-even needs essentially **all skeletal muscle loading one spring in a
single stroke**.

**When two unrelated framings hit a wall, the wall belongs to the problem.** Changing
representation moved the shortfall from **≥10× to 1.9×**, so the reframe was right even though it
still failed.

:::{danger} That conclusion was then refuted, and the refutation is the better result
**Superseded by S30.** The claim above continued *"the barrier is a property of single-impulse
launch from water at this size"*. **The sign is wrong**, and so is the framing.

Required specific energy scales as **m^0.36–0.53** (measured in exocoetids, Fish 1990), while
single-stroke LaMSA supply per kg is **size-independent** (Sutton 2019). Since the exponent on
demand exceeds the exponent on supply, the budget closes as mass **decreases**. The crossover is an
**upper** bound at **m\* = 39 mg**, which makes a 0.4 g zebrafish **~10× too LARGE** for
single-impulse launch, not too small.

And the hard reality check forced a reinterpretation rather than a tuning. The scaling predicts no
exocoetid of 3–530 g can reach glide speed in one stroke — and that is what is observed. A **300 g
*Cypselurus* needs 16.4 m/s, exits the water at only ~10 m/s (37% of the kinetic energy), and
taxis** to 15–20 m/s with the lower caudal lobe still immersed.

**So real fish gliders use a multi-stroke launch, and both results above modelled a single
impulse.** The smallest real glider is ~1–2 g needing 4.23 m/s — essentially the same speed the
zebrafish design requires. The difference is not the speed; it is the mode of reaching it.
:::

### The third route, modelled properly, closes it — and validates against a real animal

**S32** wrote the equations of motion for the phase real gliders actually use: body airborne, lower
caudal lobe still immersed, thrust applied over many strokes.

**Thrust passes.** Leaving the water cuts body drag by **816×** — exactly the water/air density
ratio — from 4.6 mN to 8 µN. Lobe thrust exceeds drag 3–40× and **speed genuinely rises**, doubling
in ~10 strokes. S24 had closed this prematurely on tail-beat frequency.

**But the taxi stalls at 2.2–2.9 m/s, 50–65% of the 4.41 m/s glide speed.** It does not fail to
accelerate; it accelerates to a ceiling below what is needed. From the low-end exit it fails earlier
still, on **weight support** rather than thrust.

The ceiling has a clean form, and the interesting part is what cancels:

```
U_max = f · A_pp · √(c6 / C_D(Re))
```

Measured foil thrust scales with *tail* speed squared, independent of forward speed; drag scales as
U². **Immersed area and body mass drop out entirely.** Only tail speed and lobe drag at Reynolds
number remain.

| | f·A_pp / V_to | lobe C_D | U_max / V_to |
|---|---|---|---|
| zebrafish, Re ~1e4 | 0.09–0.10 | 0.06–0.08 | **0.58–0.68** |
| exocoetid, Re ~3e5 | 0.09–0.10 | ~0.01 | **1.3–1.5** |

**They differ in exactly one quantity.**

**And the model validates against the animal that succeeds.** The same equations reproduce the
exocoetid taxi to 15 m/s, and Deng 2019's 36 W, **only with Reynolds-dependent lobe drag. With a
constant C_D a flying fish could not taxi at all.** So the Reynolds effect is not a fitted excuse
for our failure — it is what makes the model describe the real glider.

That is the strongest form this result can take: **one parameter explains both the success and the
failure.**

**Reopening condition, falsifiable:** an airborne zebrafish lobe beating at **1.4–2.2× its best
measured burst tail speed**, or surface-piercing lobe thrust at Re 1e4 measuring well above the 2-D
foil law.

---

## What is real, and what is not

**Real genetic precedent.** Daane et al. 2021 ([doi:10.1016/j.cub.2021.08.054](https://doi.org/10.1016/j.cub.2021.08.054))
phenocopied flying-fish **fin proportions** in zebrafish by crossing two dominant alleles. Our DOI
check resolves it to *"Modulation of bioelectric cues in the evolution of flying fishes."*

**And the gap that matters:** they measured fin **length** only. **Fin area was never reported**, and
no lift, glide or flight was tested. The physics needs area.

**Two build blockers, found by trying to build it:**

- The symbol `lat4a` **resolves to nothing** in UniProt or NCBI Gene. It is `slc43a2a`
  (GeneID 393221, chromosome 15) — identified from Daane's own chromosome mapping, with four
  positive controls proving the search worked.
- Every UniProt entry for `slc43a2a` is **153 aa** — too short to contain a residue 200, so **the
  T200K substitution is unrepresentable** in the standard references. Only Ensembl GRCz11 carries
  the full-length product: `ENSDARP00000138218` (577 aa) and `ENSDARP00000120945` (571 aa).

  **Both carry threonine at position 200**, which is what the allele name predicts — so the
  substitution is now confirmed against a reference rather than taken from the nomenclature, the
  1-based index convention is established rather than assumed, and the 153 aa UniProt entries are
  demonstrably **fragments** rather than a conflicting annotation. That last point matters for an
  implementer: the two sources do not disagree about the protein, one of them is simply partial.

An implementer working from standard sources **fails twice before designing a guide RNA**.

### The edit stack: two demonstrated alleles out of eight required slots

**S15** asked for a minimal stack where *every edit is individually demonstrated in zebrafish*.

**Two alleles** produce the fin allometry: `kcnh2a^lof(dt2)` (longfin, cis-ectopic *kcnh2a*,
coordinated fin overgrowth) crossed with `lat4a^nr21/dmh26` (dominant T200K — and notably a fin-size
**suppressor**). Their viable transheterozygote is the published flying-fish-like phenocopy.

That the mechanism is **enlarger + suppressor rather than uniform enlargement** is why the published
result concerns fin *proportions*. The design lever is differential allometry across fins, not
growth of one fin.

**Six required capabilities contain no demonstrated zebrafish edit at all:** membrane stiffness,
launch power, aerial stability, vestibular and visual function in air, aerial gas exchange, mass
reduction.

**A third fin allele exists and does NOT fit the stack, which is worth more than if it did.**
`cacna1g` homozygous mutants regenerate extraordinarily long fins (Le Bleu et al. 2025,
[doi:10.1242/dev.204739](https://doi.org/10.1242/dev.204739)) — a demonstrated zebrafish
loss-of-function long-fin model. But the authors state it **decouples developmental from
regenerative** outgrowth: the fin lengthens *while regenerating after amputation*. It is not a lever
for a larger fin in an intact animal, so it cannot be added to the stack as a third enlarger, and
counting it would have inflated two demonstrated slots to three on a misreading of what the allele
does.

**Two of eight slots is not a buildable stack**, and the subproblem refuted itself on the project's
own criterion rather than assembling something speculative. So the honest answer to *"can we get to
real genetic manipulations?"* is: **two of them, and six have never been done in this animal.**

An independent check: the required wing area at a 2 m/s launch is ~20 cm² against a ~1.4 cm²
whole-body dorsal silhouette — a **14× shortfall**, falling to 0.6× only at a 10 m/s launch. That
reproduces the launch-speed barrier from a completely different direction.

---

## Three decisive experiments, all cheap, all bench-scale

1. **Measure pectoral fin AREA in the existing Daane double heterozygote.** The authors measured
   length and never area — **the animal exists and the measurement does not.** It decides whether
   even the 5–10% phenotype is detectable.
2. **In-situ single-stroke spring-loading work of zebrafish fast myotomal muscle.** At or above
   **~99 J/kg** the energy term closes and the launch route reopens.
3. **Zebrafish C-start PIV efficiency**, which sets the 0.37 hydromechanical efficiency the whole
   launch budget rests on.

None is a programme. Each is a measurement.

---

## How much of this is measured

Of ~150 live claims: **23 measured**, 62 derived, 17 literature, 6 simulated, 1 assumed, the rest
unknown. Most of this project is *derived from* measurements rather than measured — legitimate for a
design study, and the number to probe first.

**231 challenges have been resolved**, and the base rate is uncomfortable and informative: 70%
weakened, 17% survived, 13% refuted. Sampling six weakened verdicts found all six substantive. The
recurring shape is *"the arithmetic reproduces, but the inference overreaches"* — so the low
survival rate is a finding **about us**, not about the challengers.

The grader producing those verdicts has been **calibrated**: 7/7 on a blind benchmark, 4/4 on
seeded defects spanning arithmetic, regime, scale and evidence-level inflation. **Two of the four
seeded defects are real errors this project made.**

---

## What this does not establish

- Fin **area** has never been measured in any enlarged-fin zebrafish, so the central geometric input
  is an extrapolation.
- The S26 active-stiffening margin rests on a boundary condition that **could not be verified**: the
  publisher blocks full text and the OA service 404s. The order of magnitude is confirmed by the
  paper's own abstract; the exact factor is not.
- No organism was built, no measurement was taken by us, and no simulation was validated against an
  experiment. Every number is literature, derivation, or model output, labelled as such.
- **Three routes have now failed on three different terms** — wings on lift, a single spring
  impulse on muscle energy density, and the multi-stroke taxi on Reynolds-limited lobe drag. The
  third is the best founded because it reproduces a real glider. None of this proves no route
  exists; it means the three that have been modelled do not work, each for a reason that can be
  checked independently.
- The headline 4.37 m/s **looks the most precise number here and is the most structurally
  dependent**: its ±0.11 propagates neither the wing area's total absence of an interval nor the two
  untested structural assumptions beneath it (steady lift, rigid wing).
