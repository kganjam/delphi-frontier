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
| C3 | **A voltage-sensitive transducer that reads the potential** | cell | **SATISFIED — see §10. Was recorded here as the load-bearing gap; that was wrong.** |
| C4 | A route from that transducer to ray growth rate | tissue | **open** |
| C5 | Gradient decay length comparable to ray length (~0.1–120 mm) | tissue | **open** |
| C6 | Gradient established fast relative to ray growth (days–weeks) | tissue | plausible, unmeasured |

**C3 is the one that matters.** The entire bioelectric story requires that *something reads the
membrane potential and changes behaviour*. If no voltage-sensitive transducer is known in fin
mesenchyme, then the published mechanism has an unsatisfied existence constraint at its centre —
and that is a far sharper statement than "the mechanism is not fully understood".

It is also **cheap to test**: it is a literature question, not an experiment.

:::{note} And when it was finally tested, the answer was that a reader exists
The paragraph above is kept because its *reasoning* is the reusable part — an existence constraint
at the centre of a mechanism really is sharper than vague doubt, and really is cheap to settle.
But its conclusion was wrong, and it was wrong for the reason it names: **nobody had looked.**
§10 records what looking found.
:::

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

**The pass continued, and §9 replaces these numbers.** Four `unsatisfiable` verdicts did arrive —
and reading them is what produced the more useful result.

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

---

## 9. The first refutations from below, and the two that were not

The pass widened to **26 claims and 173 constraints**: 71 `satisfied`, 50 `open`, 49 `unsatisfied`,
1 `assumed`, and **4 `unsatisfiable`** — the outcome §4 calls the prize and §7 said had never
happened.

**Two of the four were wrong, and the reason they were wrong is worth more than the two that were
right.**

### The defect: nothing checked that both sides were the same animal

Rows 93 and 125 both come from **S32, which models a zebrafish taxi**. Each was marked
`unsatisfiable` on an **exocoetid** measurement — Franzisket's 400 m in 30 s (≈13.3 m/s) and Fish
1990's 3–530 g body masses, against a ~0.4 g zebrafish.

The sharpest one refutes itself on inspection. **S32's own published result is that the same
equations reproduce the exocoetid taxi to 15 m/s**, and fail for the zebrafish only through
Reynolds-dependent lobe drag. So the flying-fish speed quoted to contradict the model is a number
the model *predicts*. That refutation was a confirmation, filed backwards.

**The error has a direction, which is why it is structural rather than careless.** This project's
claims are about zebrafish; almost all the literature is about flying fish. So the nearest
measurement to any claim is usually about the wrong animal, and an agent reaching for the closest
number reaches wrong *by default*. Both agents half-saw it — row 93 records *"if claim 269 models a
small or tank-confined fish, this becomes open"* — and wrote `unsatisfiable` anyway.

Both rows are now `open`, with the reason recorded in the row rather than deleted. The generator
prompt now requires the animal to be **named on both sides** before `unsatisfiable` may be written,
and says that a cross-species comparison can still be informative but is not a refutation.

This is §7's warning — *nothing checks that a constraint is entailed rather than merely related* —
arriving as a measurement instead of a caution, and one level deeper: the *constraint* was
entailed. The **evidence** was merely related.

### The two that hold

**Row 43 (`spatial`, claim 185, dna → protein).** A 12-transmembrane transporter must match its
orthologues' length within ~1.3×. UniProt `Q7ZUS0` is **153 aa with 2 annotated TM helices**, a
ratio of **0.27** against human SLC43A2 (569 aa, 12 TM) and zebrafish slc43a2b (592 aa, 12 TM).
Read full-text from the primary records and their feature tables.

Note what it refutes: **the 153 aa records as the functional protein, not the claim** — which
predicted exactly this truncation. The measurement is what turns *"153 aa"* from an observation into
the diagnosis *"fragment"*, and the agent said so in the row.

**Row 53 (`timescale`, claim 234, organism → behaviour).** Single-release take-off requires one
stroke; exocoetids taxi ~9 m at 50–70 beats/s, about **22–45 strokes**. It refutes applying
single-stroke LaMSA supply to exocoetids, **not** the β > α inequality itself, and it keeps a
conflicting 13.5 Hz figure visible rather than reconciling it.

### What this pass established

The mechanism produces real refutations from below, at roughly **2 sound verdicts per 173
constraints** — and the honest reading of that rate is that it is an estimate from one pass whose
error rate was **50% before review**.

**So the verdict is not the product; the reviewed verdict is.** Generation made it cheap to produce
four candidate refutations and free to produce two false ones, and nothing in the pipeline
distinguished them. A reader who had taken the table at face value would have recorded two
refutations of the project's own best result, using the number that result was validated against.

---

## 10. C3 is satisfied, and the project had been calling it the load-bearing gap

**A voltage-sensitive transducer in zebrafish fin mesenchyme is demonstrated.** Le Bleu et al.
2025, *Development* 152(23) ([doi:10.1242/dev.204739](https://doi.org/10.1242/dev.204739),
PMID 41321290; preprint [doi:10.1101/2024.08.21.608903](https://doi.org/10.1101/2024.08.21.608903)):

- **membrane depolarisation of isolated fin fibroblasts triggers voltage-gated Ca²⁺
  channel-dependent Ca²⁺ spikes** — the reader, measured directly;
- single-cell transcriptomics identifies `cacna1c` (L-type), `cacna1ba` (N-type) and `cacna1g`
  (T-type) as the candidate mediators;
- **`cacna1g` homozygous mutants regenerate extraordinarily long fins** through prolonged outgrowth;
- the authors' own conclusion is that *"bioelectricity for fin size control reflects
  voltage-modulated Ca²⁺ fluxes in fibroblast-lineage blastemal cells."*

So §6's table was wrong, and §7's warning about C2–C6 — *"marked open because nobody has looked,
which is different from having looked and found nothing"* — was the correct reading of its own
state. The entry that mattered most was the one nobody had checked.

### The catch, which is what a designer actually needs

**The effect is on REGENERATIVE outgrowth, not developmental.** The authors say `cacna1g` mutants
*"uniquely provide a genetic loss-of-function long-finned model that **decouples** developmental and
regenerative fin outgrowth."*

So this is **not** a lever for growing a larger fin in an intact animal. It lengthens a fin that is
regenerating after amputation. For a design whose whole premise is a fish that leaves the water
under its own power, an allele that requires amputating the fin first is a different intervention
from the Daane alleles, and cannot simply be added to the stack as a third enlarger.

**That distinction is the finding, not a footnote.** Had this been recorded from the abstract's
headline alone, the project would now hold a "third demonstrated fin-enlarging allele" that does
not do what the stack needs.

### How it was found, which says something about the machinery

Not by the entailment generator. **By an adversarial challenge to the entailment generator's own
verdict** — an agent attacking the `unsatisfied` row rather than the claim. Its output was labelled
`derived` and carried *"not re-read by harvester"*, so it arrived as a lead, and the citation was
then verified here against PubMed with both abstracts read in full.

**And it sat unread.** S31 was `answered` in substance while its row said `running` with no live
session, so it was invisible to every readiness query — the exact failure
[SPEC-subproblem-lifecycle §4](../specs/SPEC-subproblem-lifecycle.md) was written for, recurring
after the spec documented it. It surfaced only when a checker was finally written for that spec's
acceptance criteria and reported 5 violations of rule 3.

One correction to the agent's report: it named **cilnidipine** specifically. The abstract says only
*"small molecule inhibition"* of L- and/or N-type channels, so that drug name is **unverified** and
is not repeated as fact here.
