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

**When two unrelated framings hit a wall, the wall belongs to the problem.** The barrier is a
property of *single-impulse launch from water at this size* — not of any one mechanism, and not of
our imagination. That is a far stronger claim than "bigger fins did not work", and it is the result
the project exists to have produced.

Worth noting for its own sake: changing representation moved the shortfall from **≥10× to 1.9×**.
The reframe was right even though it still fails.

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
  the full-length product.

An implementer working from standard sources **fails twice before designing a guide RNA**.

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
- S30 — the body mass at which the launch budget *does* close — is still running. Until it returns,
  "too small" has no threshold attached.
