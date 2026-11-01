# Closed-loop experimental design for cross-scale biology: what the primary sources support

**Status:** source-only research brief, 2026-10-31. **No experiment was designed, run or proposed
here, and no laboratory protocol appears below.** Owner file; supports root SPEC-013 and the
native quantitative planner, and coordinates with
`docs/research/fish-regulatory-map-2026-10-31.md` for the regulatory layer. No UI edits.

**Read-level key:** `full-text` | `abstract` | `listing` | `could-not-access`. Each source carries
its own. **Everything below is at `abstract` level**; I read publisher or preprint abstract pages,
not full texts, and I say where that limits the claim.

---

## 1. Sources

| Source | Where | Read-level |
|---|---|---|
| **Foster A, Ivanova DR, Malik I, Rainforth T (2021).** *Deep Adaptive Design: Amortizing Sequential Bayesian Experimental Design.* ICML, PMLR **139**:3384–3395 | https://proceedings.mlr.press/v139/foster21a.html | `abstract` |
| **Foster A, Jankowiak M, Bingham E, Horsfall P, Teh YW, Rainforth T, Goodman N (2019).** *Variational Bayesian Optimal Experimental Design.* NeurIPS 2019 (per the arXiv Comments field). arXiv:1903.05480, v1 2019-03-13, v3 2020-01-14 | https://arxiv.org/abs/1903.05480 | `abstract` |
| **Brunton SL, Proctor JL, Kutz JN.** *Discovering governing equations from data: Sparse identification of nonlinear dynamical systems.* arXiv:1509.03580 v1 2015-09-11; related DOI 10.1073/pnas.1517384113 (PNAS) | https://arxiv.org/abs/1509.03580 | `abstract` — the PNAS page returned **HTTP 403** to me |
| **Kennedy MC, O'Hagan A (2001).** *Bayesian Calibration of Computer Models.* JRSS-B **63**(3):425–464, DOI 10.1111/1467-9868.00294 | https://academic.oup.com/jrsssb/article/63/3/425/7083410 | `abstract` — full text paywalled |

**One correction to the brief that commissioned this.** It referred to Kennedy & O'Hagan as
*"calibration confounding"*. **The 2001 abstract does not state a confounding or identifiability
result.** What it states is that the method *"attempts to correct for model inadequacy"* revealed
as a discrepancy between observations and predictions at best-fitting parameter values. The
framework therefore *introduces* a discrepancy term alongside calibration parameters; that the two
can be **confounded** is a widely-discussed consequence, but it is **not something I verified from
this paper at abstract level**, and nothing downstream should cite the 2001 abstract for it.

---

## 2. Identifiable contextual transfer functions

The object we actually want is a **transfer function with its context attached**: given an
intervention at scale *n* under stated conditions, what is the distribution of a readout at scale
*n+1*? Three constraints follow from the sources.

**Sparsity is an assumption, not a finding.** SINDy's central assumption, in the authors' own
framing, is that only a few terms govern the dynamics in a chosen library of candidate functions.
The abstract names neither how derivatives are obtained nor how noise is handled. So a recovered
form is **conditional on the library someone chose**, and the library is a modelling decision that
belongs in the record beside the result.

**Identifiability is a property of the design, not of the data volume.** More measurements of the
same contrast do not separate parameters that enter the model the same way. This is why the
*design* question and the *inference* question cannot be answered separately.

**Context is part of the function.** Our own regulatory map already shows this: predictors
calibrated in human and mouse contexts have **unknown calibration in fish**, and a chromatin
accessibility result does not establish the corresponding expression program. A transfer function
without its context is not reusable; it is just a number.

---

## 3. Intervention, readout, controls, biological replicate

These four are separate objects and the platform should type them separately.

- **Intervention** — what was changed, at which scale, by how much, against what baseline.
- **Readout** — what was measured, by which assay, with what denominator. An assay measures one
  thing; naming the construct it is taken to represent is a further claim.
- **Controls** — a positive control establishing the measurement can detect the effect, and a
  **must-fail control** establishing it can come back negative. Our own repository convention
  states the reason: *a search that cannot come back empty has not been tested.*
- **Biological replicate** — independent organisms or independent biological preparations, not
  repeated measurement of one preparation. Technical replication bounds measurement error;
  biological replication bounds the thing we usually want to generalise over. **Conflating them
  inflates confidence without adding evidence.** The regenerating-fin dataset our regulatory map
  cites records **two biological replicates per time point**, which is a real number and a small
  one.

---

## 4. Within-scale and cross-scale experiments

**Within-scale:** intervention and readout sit at the same level, and the inference is about a
mechanism at that level. These are the experiments the literature mostly supplies.

**Cross-scale:** the readout is at a different level from the intervention, and the inference
needs a bridge. **The bridge is where the evidence usually is not.** Our regulatory map names
exactly this for every row — epithelial state *"does not specify fin outgrowth"*; inferred
trajectories *"are not lineage tracing or an ECM modulus"*; inferred regulatory networks
*"need causal tests"*.

A cross-scale design is therefore two claims, not one: that the intervention does what it is
supposed to at its own level, **and** that the bridge carries it. A result that cannot separate
these is a result about the pair.

---

## 5. Multi-fidelity: simulator against wet lab

Kennedy & O'Hagan's framework is the right shape for our problem because it keeps **two** things
in the model at once: calibration parameters we are trying to learn, and a **discrepancy term**
for the model being wrong. Their stated gain is that predictions then account for all sources of
uncertainty, including remaining uncertainty about fitted parameters.

The practical consequence for us, stated as an inference and not as their claim: **a simulator
tuned to match data has not thereby been validated.** Fit can be bought either by moving the
parameters or by absorbing the mismatch into discrepancy, and a design that cannot tell those
apart will report a calibrated model where it has a flexible one. Our own repository already
records an instance of exactly this shape in a different guise: a *fit* to a sweep that turned out
to be the model supplying its own oxygen, which measured our assumed medium rather than the fish.

**What this says about fidelity tiers.** Cheap simulator runs are useful for *ordering* candidate
experiments. They are not a substitute for the expensive measurement, and the discrepancy term is
the honest place to keep the gap rather than hiding it in a tuned parameter.

---

## 6. Adaptive sampling by decision-relevant uncertainty and cost

Foster 2019 addresses the bottleneck that **estimating expected information gain is hard**, and
proposes faster EIG estimators built on amortized variational inference. Foster 2021 (DAD)
amortizes the *design policy itself*: a network trained up front maps past data to the next design
in a single forward pass, which the authors describe as taking milliseconds, trained with
contrastive information bounds and a symmetry-aware architecture.

Two things follow for us.

**Adaptive experimental design is established work, and we claim none of it.** This is a
well-developed field with public implementations. Nothing in our platform makes active learning
novel, and the pitch must not imply it does.

**Information gain is not the objective we actually have.** EIG measures reduction in uncertainty
about parameters. What a design studio needs is reduction in uncertainty **that changes a
decision**, divided by cost — and in cross-scale biology the costs differ by orders of magnitude
between a simulator sweep, an assay and an organism. A design that maximises information about a
parameter nobody acts on is efficient and useless. **We have not implemented a
decision-relevance-per-cost objective, and nothing here should be read as a claim that we have.**

---

## 7. The applied fish matrix

Scales, with the measurement types that would populate each and the unknowns that currently block
it. **This is a map of our own gaps for this organism. It is not a claim about biology in
general.** Rows draw on `docs/research/fish-regulatory-map-2026-10-31.md`; the mechanics rows
draw on this repository's own artifacts.

| # | Scale | Intervention type | Readout / measurement type | What is actually missing |
|---|---|---|---|---|
| 1 | **Regulatory** | enhancer or promoter edit; sequence design | ATAC-seq accessibility; paired nuclear RNA/ATAC | Predictors are calibrated in **human/mouse** contexts; **fish calibration unknown**. Accessibility ≠ expression |
| 2 | **Expression** | perturbation of a named regulator | scRNA-seq; per-compartment state annotation | Inferred GRNs and in-silico perturbations **need causal tests**; trajectories are not lineage tracing |
| 3 | **Protein activity** | channel or enzyme variant | conductance, gating, enzymatic rate | Our structure prediction is **PREDICTED only** — >50% of residues below pLDDT 50 — and establishes **no conductance or gating** |
| 4 | **Cell program** | signalling perturbation in a compartment | marker-defined state; proliferation; differentiation | Immune participation **does not prove** developmental growth control; boundary signalling and geometry uncalibrated |
| 5 | **ECM / tissue EI** | matrix composition or mineralisation change | stiffness, modulus, ray section geometry | **No sourced flying-fish EI profile has been established.** Mineralisation, ray segmentation and stiffness need independent measurement |
| 6 | **Fin shape** | geometry or ray-count variation | morphometry; meristics | Counts and outlines are sourced; **camber and dihedral remain assumed** |
| 7 | **Aero / behaviour** | launch condition; load case | force coefficients; glide path; kinematics | Fins are **sub-grid at every completed resolution**; the sphere reference gate **failed**; **no glide simulation and no flight** |

**The bridges, not the rows, are the research programme.** 1→2 needs accessibility-to-expression
in fish. 2→3 needs expression-to-activity. 3→5 needs activity-to-modulus. 5→6 needs modulus and
geometry to shape. 6→7 needs resolved fluid–structure coupling, which our own grid does not yet
provide. **Each arrow is an unpinned transfer function, and that is the honest statement of where
this stands.**

---

## 8. What the platform contributes, stated narrowly

**Not claimed:** that active learning, Bayesian optimal design, sparse system identification or
model calibration are novel. They are published, implemented and in wide use.

**Claimed, and only this:** that an experiment is more reusable when the **claim it consumes, the
protocol it froze, the artifacts it produced, the review it received and the dispute it is still
under** travel with it as typed, versioned records — and that **experiment planning is one more
record of that kind** rather than a separate tool. A planned design that cites the claim licensing
its prior, the cost model it assumed and the decision it was meant to change is auditable by
someone who was not there.

This repository already has one worked instance of the reuse half: an exact stiffness Claim
consumed before two leased computations, independently re-derived three ways, and **still disputed
for want of non-computational replication**. The planning half does not yet have one.

---

## 9. Limits of this brief

- **Every source is at `abstract` level.** No full text was read. Method details — estimator
  variance, noise handling in SINDy, the discrepancy prior's form in Kennedy & O'Hagan — are
  **not** established here.
- The PNAS page for SINDy returned **HTTP 403**; the arXiv version was read instead.
- The Kennedy & O'Hagan **confounding** point is not supported by the abstract I read (§1).
- **No design is proposed, no protocol is written, and no result is predicted.** Section 7 is a
  map of gaps, not a plan.
- Negative scope: I did not survey the cross-scale-design literature systematically, so **nothing
  here should be read as a claim that no suitable method exists**.

## 10. Revisions

- **2026-10-31** — created. Four sources verified from primary pages the same day. Corrected the
  commissioning brief's attribution of a confounding result to the Kennedy & O'Hagan abstract.
  While checking SINDy I first retrieved **PMC4812707**, which is a **bioprinting paper**, not
  SINDy; cited the arXiv record instead.
