# Replicate 159: [S26] active fin-ray stiffening, re-derived independently

**Context tag:** `harvest:active-fin-ray-stiffening-l53vks`
**Date:** 2026-11-04

## What I was given, and what I could not see

The question reached me as "[S26] No on current evidence", with the answer removed. I could not find the
full wording of S26 or its inputs anywhere in this repository. I searched every branch (`git grep` over all
refs) for `l53vks`, `S26`, `stiffen` and `fin ray`. The only matches were unrelated items in
`findings/gemini-triage-267-problems.json`: `spiny-fin-ray-origin`, plus zebrafish fin-ray regeneration
and joint patterning. **So I never came across the original derivation, and I have no recorded value to
compare against.**

Because I could not see the question, I had to guess what it asks. My reading is: *Is there evidence that
fish actively stiffen their fin rays, and how large is the change?* The sub-question that decides the
answer is: *has anyone measured an active stiffness change in a living fish?*

## Sources (each with its read-level)

| # | Source | Read-level | What it gives |
|---|--------|-----------|---------------|
| 1 | Alben S, Madden PGA, Lauder GV. "The mechanics of active fin-shape control in ray-finned fishes." *J R Soc Interface* 4(13):243–256 (online 2006, issue 2007). doi:10.1098/rsif.2006.0181. PMC2359861 | full-text (read through a WebFetch summariser; I checked the quoted passages but did not proof-read every line) | Bluegill (*Lepomis macrochirus*). Point-load cantilever test on **excised rays dissected from euthanised fish (MS-222), tested within 48 h**. With both hemitrich bases clamped, the slope was **1.98 N m⁻¹**, about **12×** the slope with one base free. Composite EI from three-point bending is about 10⁻⁶–10⁻⁵ J m. Authors' claim: stiffness can vary "over more than an order of magnitude depending on actuation". |
| 2 | Puri S et al. "In vivo quantification of mechanical properties of caudal fins in adult zebrafish." *J Exp Biol* 221: jeb171777 (2018), PMC5868929 | search-summary | Live, anaesthetised zebrafish. Bending stiffness of the caudal fin is about 1.5–4 × 10⁻⁹ N m². This is a **passive** measurement with no muscle actuation, so it says nothing about active stiffening. |
| 3 | Drexel doctoral dissertation, "Experimental technique to investigate compliance of…" (researchdiscovery.drexel.edu, record 991014632605604721) | search-summary | States that active fin-ray stiffness control "has not been confirmed through experiments with live fish during natural swimming". Uses vortex-ring perturbations on live bluegill. Fins at higher swimming speed responded like a stiffer foil. This is **indirect** evidence: a behavioural response matching a stiffer foil, not a measured stiffness. |
| 4 | Lauder, Madden, McHenry. SICB abstract "Fin rays of ray-finned fishes: biology and mechanics…" | could-not-access (sicb.org is not resolvable from this session's network) | Only a search-engine snippet: "preventing relative hemitrich displacement increased fin ray stiffness nearly 12 times". This agrees with source 1. |
| 5 | APS DFD 2021 Q13.4, "Active Control of Caudal Fin-Ray Stiffness and Propulsion" | could-not-access (meetings-archive.aps.org is not resolvable) | Title only. I do not know whether it used a model, a robot or live fish. |
| 6 | arXiv 1608.05891, "Curvature-induced stiffening of a fish fin" | listing | A theory paper: stiffness rises with curvature. It contains no in vivo measurement. |

## Derivation (arithmetic in full)

**Observed ex vivo, on excised rays (source 1):**
- k_clamped = 1.98 N m⁻¹ (reported).
- k_clamped / k_free ≈ 12 (reported ratio).
- **My calculation:** k_free = 1.98 / 12 ≈ **0.165 N m⁻¹**, which rounds to 0.17 N m⁻¹. This number is derived, not reported.
- So the stiffness change from blocking hemitrich sliding is about **12-fold, or log₁₀(12) ≈ 1.08 orders of magnitude**.

**Model (source 1, a calculated result, not an observation):** the authors fitted a linear elasticity model
that reproduces the 12× ratio at their fitted shear parameter (G ≈ 100, in the paper's non-dimensional
units). Their "more than an order of magnitude" range is model-supported.

**Interpretation (my inference, not the authors' claim):** the 12× figure compares a fully blocked base
with a completely free base, using clips on dead tissue. That is an **upper bound on what the mechanism
can do**. It is not a measurement of what a living fish's muscles actually achieve. Real muscles would put
a fish somewhere between the two extremes, at a point nobody has measured.

**In vivo active stiffening (the decisive sub-question):** I found no study that measured a change in
fin-ray stiffness caused by muscle activity in a living fish. Scope of that negative search: two
WebSearch queries (standard mode) on 2026-11-04; the full text of source 1; search summaries of sources
2 and 3. Two relevant hosts (sicb.org and meetings-archive.aps.org) could not be reached. Source 3
independently states that active control is not confirmed in live swimming fish. This search is narrow,
so a study published after about 2023, or one that is not indexed, could have been missed.

## My value

- **Answer to S26 (as I read it): No on current evidence.** There is no direct in vivo measurement of
  active fin-ray stiffening.
- **Quantitative bound:** a capacity of **about 12×**, with a range of roughly 10–12×. This comes from an
  ex vivo observation on excised bluegill rays, base clamped versus free, n not checked. The model in the
  same paper supports "more than one order of magnitude".
- **Uncertainty:** I give a single ratio because only one primary experimental source (source 1) gives a
  number. The SICB snippet (source 4) repeats about 12× but is probably the same group and data, so it is
  **not independent**. The in vivo magnitude is **unknown**.

## Comparison with the recorded value

The recorded value is shown only as the question label "No on current evidence". My conclusion matches
that label. However, I could not see the original's reasoning, its inputs, or any number it gave, so I
cannot check whether we agree for the same reasons or on the magnitude.

**Verdict: AGREE on the qualitative verdict; CANNOT TELL on any quantitative value.**

```swarm-replication
{"claim_id": 159, "my_value": "No on current evidence (no in vivo measurement found); ex vivo capacity ~12x stiffness, base clamped vs free (k ~1.98 vs ~0.17 N/m, excised bluegill rays, Alben et al. 2007)", "agrees": true,
  "note": "My independent reading of Alben et al. 2007 (full text) finds only ex vivo ~12x stiffening on excised rays and no in vivo active-stiffness measurement within a narrow two-query search, matching the 'No on current evidence' label; the original's numbers were not visible to compare."}
```
