# Cross-scale constraints, and what it means to verify a multiscale model

*A claim at one scale entails requirements at its neighbours. Those requirements are the verification.*

---

## 1. The problem with "verifying" a multiscale model

The obvious approach is to simulate every scale and check the whole thing reproduces something.
That fails here for three reasons, and they are not fixable by better simulation:

1. **Most scales have no validated simulator.** We have structure prediction and some mechanics.
   We have nothing that takes a bioelectric gradient to a fin ray length.
2. **A full multiscale run has more free parameters than data.** It can be tuned to reproduce
   almost anything, which makes agreement uninformative.
3. **It answers the wrong question.** "Does the whole model reproduce the phenotype?" is not what a
   designer needs. They need "which part of this is load-bearing, and is it real?"

So the proposal: **do not verify by simulating up. Verify by propagating constraints down, and
checking whether anything at the adjacent scale can satisfy them.**

---

## 2. A claim at scale N entails requirements at N±1

This is the whole idea, and it is mechanical rather than clever.

> *"A bioelectric gradient patterns fin ray length."*

That sentence, if true, **necessarily** requires, at the cell scale:

- **a generator** — something that establishes the potential difference;
- **a maintainer** — a conductance/leak balance that holds the gradient against dissipation, which
  is a *quantitative* requirement, not an existence one;
- **a reader** — a voltage-sensitive transducer, or the gradient changes nothing;
- **an effector** — a route from that transducer to growth rate.

And at the tissue scale:

- **a length scale match** — the gradient's decay length must be comparable to the structure it
  patterns, or it is uniform across it and patterns nothing;
- **a timescale match** — gradient establishment must be fast relative to growth, or the pattern
  smears.

None of these names a molecule. **They are generic, and satisfiable in many ways** — which is
exactly what makes them *design* constraints rather than facts. A designer may satisfy "a reader"
with any voltage-sensitive transducer; the constraint says only that one must exist.

---

## 3. Six kinds, which is enough

| Kind | Form | Fails when |
|---|---|---|
| `existence` | something must exist that does X | nothing at that scale does X |
| `range` | a parameter must lie in [a, b] | measured values fall outside |
| `timescale` | process A must be fast/slow relative to B | the ratio inverts |
| `spatial` | a length scale must match within a factor | the structure is uniform or sub-resolution |
| `energetic` | power or energy must be available | the budget does not close |
| `conservation` | mass, charge or momentum must balance | the junction leaks |

`range`, `timescale` and `spatial` are the ones that bite, because they can be **checked against
measured values without any simulation at all**. `existence` is the one that most often turns out
unsatisfied, and it is the cheapest to test — you look.

---

## 4. The verification criterion

> **A multiscale claim is verified to the extent that every constraint it entails is satisfied by
> something real at the adjacent scale. A claim with an open `existence` constraint is not a weak
> model; it is a model with a missing part.**

Three honest outcomes, and the third is the valuable one:

- **satisfied** — a named mechanism, with its own evidence level.
- **unsatisfied** — nothing known satisfies it. The claim stands only as a scenario, and this is
  recorded, not hidden.
- **unsatisfiable** — the constraint contradicts a measured value. **The claim is refuted from
  below**, without simulating anything.

That last case is the prize. It refutes a high-scale claim using a low-scale measurement, which is
far cheaper than any simulation and far more decisive.

---

## 5. Constraints inform the simulation, which is the practical payoff

A simulation at scale N needs parameters. Constraints propagated from N+1 **supply the ranges**, and
a run outside them is answering a question nobody asked.

Concretely: if the tissue-scale pattern requires a decay length of ~200 µm, then at the cell scale
`sqrt(D/k)` ≈ 200 µm. That is a one-line constraint on the diffusion coefficient and the degradation
rate, and it immediately rules out candidate molecules whose measured D and k cannot reach it.

So the constraint set is both the **verification criterion** and the **parameter prior**. Those are
usually treated as separate problems, and they are the same object read in two directions.

---

## 6. The worked case: the bioelectric mechanism this project rests on

The Daane alleles are **potassium channels** — `kcnh2a` and `kcnk5b`. The mechanism, as published,
is bioelectric. So the chain is exactly §2's.

| # | Constraint | Scale | Status |
|---|---|---|---|
| C1 | A generator of a potential difference across fin mesenchyme | cell | **satisfied** — the channels themselves, demonstrated |
| C2 | Conductance/leak balance holding the gradient against dissipation | cell | **open** — no measured conductance for zebrafish fin mesenchyme found |
| C3 | **A voltage-sensitive transducer that reads the potential** | cell | **open — and this is the load-bearing gap** |
| C4 | A route from that transducer to ray growth rate | tissue | **open** |
| C5 | Gradient decay length comparable to ray length (~0.1–120 mm) | tissue | **open** |
| C6 | Gradient established fast relative to ray growth (days–weeks) | tissue | plausible, unmeasured |

**C3 is the one that matters.** The entire bioelectric story requires that *something reads the
membrane potential and changes behaviour*. If no voltage-sensitive transducer is known in fin
mesenchyme, then the published mechanism has an unsatisfied existence constraint at its centre —
and that is a far sharper statement than "the mechanism is not fully understood".

It is also **cheap to test**: it is a literature question, not an experiment.

Note what this did. It took a claim at the DNA scale, propagated it to the cell scale, and produced
**a specific, checkable, currently-open question that nobody in this project had asked** — without
running any simulation.

---

## 7. What this does not establish

- The constraint table in §6 is **derived by reasoning from the mechanism**, not extracted from the
  literature. C2–C6 are marked open because nobody has looked, which is different from having
  looked and found nothing.
- Six kinds (§3) is a guess at sufficiency from one worked example.
- A wrong or incomplete constraint set produces false confidence in exactly the way this document
  is meant to prevent. Entailment is now generated (§8) rather than hand-written, which changes who
  makes that mistake, not whether it can be made.
- The "refuted from below" case (§4) is the most valuable and **still has not happened**. §8 says
  how close it came.

---

## 8. Measured: what happened when entailment was actually run

Until 2026-11-04 this document described a mechanism nothing executed. The `constraint_entailed`
table existed with exactly the six kinds and four statuses specified above, and held **6 rows** —
the §6 worked example, entered by hand. The closing section said *"nothing automates entailment"*
and left it there.

It is now the swarm's fifth generator. Each live claim carrying a scale is propagated to its
neighbours, the agent writes 2–5 generic constraints, and then **checks each one against the
literature**. First measured pass, over 3 claims:

| | |
|---|---|
| constraints generated | **15** (plus the 6 hand-written) |
| `satisfied` | 10 |
| `open` | 7 |
| `unsatisfied` | 3 |
| `assumed` | 1 |
| **`unsatisfiable`** | **0** |

By kind: existence 10, range 5, conservation 2, spatial 2, timescale 1, energetic 1.

### The one that came closest, and why it was right not to claim it

Claim 283 — *required wing area at a 2 m/s launch is ~20 cm² against a ~1.4 cm² silhouette* —
entailed an **energetic** constraint at the tissue scale: the escape branch needs **~290–4800 W/kg
muscle**. The agent found the highest measured fish fast-muscle values it could: **142.7 W/kg**
work-loop mean (*Scorpaena notata*, 20 °C) and **307 W/kg** peak instantaneous (sculpin C-bend).
Both sit at or below the bottom of the required band.

That is the shape of a refutation from below, and the agent **declined to call it one**, for three
reasons it wrote down: the requirement depends on an *assumed* launch duration and muscle fraction,
the measurements come from other taxa, and elastic storage or a multi-stroke taxi bypasses the
muscle-power limit entirely — which is [the project's own S30 result](../FINDINGS.md), reached
independently.

**That is the correct verdict, and it is the result worth reporting from this pass.** `unsatisfiable`
requires a measured number to contradict a requirement that is itself firm. Here the requirement is
soft at both ends, so the comparison bounds nothing. An agent that had marked it `unsatisfiable`
would have produced this document's showcase outcome out of an assumption about launch duration.

The sources are labelled `search-summary` — leads, not evidence — and the negative carries its
scope: *"2 searches; no gasteropelecid muscle data searched beyond these."*

### What this changes, and what it does not

**Established:** the mechanism runs end to end, and the distribution is informative rather than
flat — two thirds of the generated constraints landed on something other than `satisfied`, and the
`existence` kind dominates (10 of 15), which matches §3's prediction that it is the kind most often
left unsatisfied.

**Not established:** 3 claims is not a sweep, and 0 `unsatisfiable` from 15 constraints is weak
evidence either way about how often the valuable case occurs. Nothing yet checks that a generated
constraint is *entailed* rather than merely related, which is the failure mode §7 names and which
generation makes cheaper to commit at scale, not rarer. And the one near-miss above turned on a
judgment call that a different agent could plausibly have made the other way — so the verdict
distribution is, for now, partly a measurement of the prompt.
