# NOTES — "Design a coral: for heat, for shape, or for the reef"

Working notes for whoever writes the prose. Written 2026-11-02 by ds-coral.

Everything in `raw/` was researched by a previous agent and I did not redo it. Those six
blocks are good: they carry read levels per source, they state the scope of every
negative, and they drop PMIDs that did not resolve rather than guessing. I built on them
and checked them in the places listed under **Corrections** below.

---

## 1. What is here

| File | What it is |
|---|---|
| `routes.json` | 45 routes across 9 scales, 142 evidence items, 98 distinct PMIDs |
| `bleaching-dynamics.json` + 3 figures | Host–symbiont model under thermal stress |
| `colony-morphology.json` + 2 figures | Accretive growth; **partly a negative result** |
| `settlement-recruitment.json` + 2 figures | Sensitivity analysis over stated unknowns |
| `index-fragment.json` | The index the build reads |
| `code/` | Everything above is reproducible from here |
| `external/coRal/` | Cloned reference model (MIT), read not modified |
| `logs/` | R reference trajectories, run logs |

Builders validate rather than just emit. `build_routes.py` refuses to write `routes.json`
if a cited PMID is outside the verified set or if a route claims a direct-phenotype tier
with no source read above "listing". `build_index.py` refuses to write
`index-fragment.json` if a declared figure is missing from disk or a caption does not
open by saying what the figure is. Both refusals fired during this session and both were
fixed by correcting the content, not the check.

---

## 2. The framing, and the one thing I would make sure survives

The question "could you engineer a coral" bundles four different animals, and the page's
first move is to separate them. I would make sure **the recruitment point survives
editing**, because it is the one that changes what someone would actually fund:

> Restoration does not usually fail because adult corals die. It fails at recruitment.
> In the best-documented larval seeding experiment, 47 colonies survived from roughly
> 900,000 larvae. First-year survival of settlers spreads over more than tenfold across
> sites, devices and thermal years. A heat-tolerant coral that cannot recruit is a
> heat-tolerant coral you have to keep planting by hand.

And the denominator, which belongs on the same page as any intervention: the median
coral restoration project covers **100 square metres**. Covering one square kilometre at
that median takes ten thousand projects.

---

## 2b. Cross-genus transfer: more than half this table rests on it

The team lead caught the thing that made this section necessary. Cunning, Silverstein &
Baker 2015 — the shuffling reconciliation paper the whole severity-dependence argument
leans on — is in **Orbicella faveolata**, a massive Caribbean coral. The CRISPR
precedent, the assisted-evolution programme and most of the morphology work are
**Acropora**-centred. Transfer between them is an assumption, and it was invisible on the
page until every route got a `species_of_evidence` and an `evidence_transfer` field.

The count, from `routes.json` `provenance.evidence_transfer`:

| transfer | routes |
|---|---|
| same species | 6 |
| same genus, different species | 14 |
| different coral genus | 10 |
| different genus AND growth form | 5 |
| a stony coral that does not build reefs | 2 |
| an anemone or Nematostella, not a coral | 5 |
| not an organism-level claim | 3 |

**22 of 42 organism-level routes rest on cross-genus transfer or weaker**, and
**7 rest on evidence from something that is not a reef-building coral at all**:
`mol-coral-atac-first, gene-slc26a11-symbiosis, gene-knockdown-toolkit-astrangia, cell-soft-body-refuge, sym-durusdinium-inoculation, sym-heat-evolved-ss8, sym-feed-the-host-to-pay-for-the-symbiont`. Where a route's evidence spans several taxa the WEAKEST applicable
value is recorded, because that is the assumption the route actually rests on.

Three worth naming in the prose:
- **`sym-shuffle-by-induced-bleaching`** mixes Orbicella (severity rule), Montastraea
  (persistence) and Acropora (degrees of tolerance) — two growth forms and two oceans.
- **`larval-acoustic-enrichment`** has **no Acropora value at all**; both verified results
  are Caribbean, from one laboratory group, with no independent replication found.
- **`sym-durusdinium-inoculation`** carries three different transfer levels in one route:
  the thermal gain and growth penalty from *A. millepora*, the calcification figure from
  unnamed Caribbean hosts, and the *mechanism* from an anemone.

---

## 3. Things I would get wrong if I were writing the prose

**(a) The Cunning 2015 "conflict" is not an open disagreement — it is a resolved
conditional, and there is a *separate* genuine gap next to it.** The brief asked me to
preserve a conflict about symbiont shuffling durability. The actual shape is:

- Cunning, Silverstein & Baker 2015 (PMID 26041354) is itself **the reconciliation
  paper**. Its finding is that the *direction* depends on severity: the heat-tolerant
  proportion "dramatically increased following severe experimental bleaching, especially
  in a warmer recovery environment, but tended to decrease if bleaching was less severe".
  The authors say in the abstract that they "help reconcile this conflict".
- The separate, still-open gap: **no verified multi-year Durusdinium→Cladocopium
  reversion time course exists in anything the research blocks could reach.** The longest
  verified persistence horizons are 3 months (shuffled state, Silverstein 2015), 5 months
  to ~2 years (inoculated SS8 in *Galaxea*), and 1.5 years (in an anemone).

So: write the severity-dependence as a *finding*, and the multi-year durability as a
*hole*. Writing them as one unresolved controversy would be wrong in both directions.
`PMID 41877353` (2026, Glob Chang Biol, "Persistent Legacy Effects of Marine Heatwaves on
Coral Symbioses") is the most likely source on durability and is **title-only** — nobody
has read it.

**(b) Do not write "CRISPR works in corals" without the qualifier that does the work.**
It does work, in *Acropora millepora*, and that is recent and real. But every published
coral edit is in the **injected generation** — mosaic larvae or juveniles. There is no
stable germline coral line anywhere in this literature, generation time runs to years,
spawning is seasonal, and editing adult colonies has not been shown. Counted from the sources
read here, **six** genes have been targeted by CRISPR in a reef-building coral — *FGF1a*,
*GFP* and *RFP* (Cleves 2018, chosen to show the method works), *HSF1* (Cleves 2020),
*SLC4γ* (Tinoco 2023) and *SLC26A11* (Maruyama 2026, reported in Aiptasia and in a
reef-building coral). Only the last three carry an informative trait phenotype, and all
three are **loss** of function: knocking out *HSF1* makes a coral worse at heat, knocking
out *SLC4γ* breaks its skeleton, and knocking out *SLC26A11* costs it its symbiosis. None
of them tells you how to make a coral better.

**(c) "Heat-evolved symbionts work" is three claims with different strengths.** Buerger
2020's headline is 3 of 10 strains improved the holobiont — but the full text (which I
read) says: *"no significant differences between larvae inoculated with any of the SS
strains and those inoculated with WT2"*. The 3-of-10 is a comparison against **one** of
two wild-type strains; against the other it is a non-significant trend. And in anemones,
two of six heat-evolved strains were *among the most thermosensitive*, with the
unevolved parent second-best. SS8 is a lineage that works, not a method that works.

**(d) Do not convert Buerger 2020's challenge into degree heating weeks.** The text gives
31 °C for 7 days after holding at 27 °C. That is +4 °C for a week, which would be ~4
degree-Celsius-weeks arithmetically — but the holding temperature is **not stated to be a
climatological maximum**, and degree heating weeks are defined against one. The research
block flags this explicitly and I have kept the flag.

**(e) The growth cost of Durusdinium is itself disputed, and the page should not pick a
side.** Jones & Berkelmans 2010 measured 29% (lab) and 38% (field) slower growth; Pettay
2015 reports calcification "reduced by nearly half". But Kemp et al. 2023 report *no*
ambient nutrient-exchange difference and maintained transfer under heat, and say so
pointedly: "This discovery differs from the prevailing notion that these mutualisms
inevitably suffer trade-offs." Nutrient flux is not calcification, so they do not
strictly contradict — and no single experiment reconciles them.

**(f) The regulatory material is the weakest content on the page.** No primary legal text
was read by anyone. Two things *were* verified by direct fetch and can be stated: the
United States signed but never ratified the Convention on Biological Diversity, and
neither the US nor Australia is a Party to the Cartagena Protocol. Everything else —
Australian gene-technology law, Marine Park permits, the Endangered Species Act, FDA
jurisdiction — is a search summary or an inference, and is labelled that way inside the
route. Please keep the labels.

**(g) "No assisted-evolution product has been deployed on the Great Barrier Reef" is an
absence of evidence from a limited search**, not a verified negative. Scope: one web
search, two programme pages read at page-summary level, plus PubMed and Consensus. The
programme's reports index and its own published papers were not read.

**(h) The 1.2 million corals per year figure is not the programme's.** It came from a
third-party website and could not be found on the programme's own pages. Do not use it.

---

## 4. Corrections I made to the inherited material

**The DHW attribution was wrong in the predecessor's code.** `bleaching_dynamics.py` as
inherited cited *"Liu et al. 2014, Remote Sensing 6:11579-11606"* as the source for the
MMM+1 convention and the 4 and 8 degree-heating-week thresholds. The research block
explicitly records that paper as **not reached**: "I could not reach Liu et al. (CRW) or
Glynn & D'Croz 1990 or Eakin et al. 2010 and confirm a PMID. The only attribution is the
NOAA page itself." I re-attributed everything to the NOAA Coral Reef Watch product page
at `read_level: web-page` and said in the result file that the primary methods papers
were not obtained. This is exactly the failure mode the honesty rules name: a citation
that reads as provenance and only fails when someone tries to resolve it.

**I re-verified 12 PMIDs myself** with `get_article_metadata`: 28782552, 33168726,
37276409, 16928632, 32426508, 37913765, 34389536, 32551200, 23326222, 24894390, 33232367,
32703979. All titles matched the research blocks exactly. Those 12 carry
`pmid_reverified_here: true` and a DOI in `routes.json`. The other 86 are relayed from
the research blocks at the level those blocks state — which under the project's own rules
makes them **source-only**, not independently verified by me.

**The predecessor had written `code/bleaching_dynamics.py` (41 KB) but never run it** —
`figures/` and `logs/` were empty and no result JSON existed. It was structurally
complete and well-written. I kept its thermal forcing, its degree-heating-week
accounting, its sweep and additivity structure and its figure scaffolding, and replaced
its **invented** ODE core with the coRal port. The reason is recorded in §5.

---

## 5. coRal, and the thing the brief did not anticipate

The brief said to clone `jrcunning/coRal` and that reusing a published structure beats
inventing one. I did, and the result is better than expected in one way and awkward in
another.

**Better:** R 4.3.3 is installed on this box, so I could run the author's own code and
check my Python port against it rather than merely asserting fidelity. The port
reproduces it to **5×10⁻¹⁵ relative error** across three environments (healthy,
light-limited, fed), on six variables each. That turns 24 published parameter values with
units and provenance into something I can use, and the bleaching study's parameter table
is now 28 sourced against 14 assumed.

**Awkward:** **coRal contains no temperature variable at all.** Searching the whole
cloned repository for `temp`, `thermal`, `heat`, `degC` and `dhw` returns zero hits. In
Cunning et al.'s published model, bleaching is driven by **light** — absorbed light that
photochemistry cannot use and non-photochemical quenching cannot dissipate drives ROS,
and ROS drives symbiont turnover. So "a host–symbiont ODE under thermal stress" cannot be
had by reusing it unchanged. I added temperature through exactly one parameter (the
ceiling on symbiont carbon fixation), warranted by Warner, Fitt & Schmidt 1999's PSII
damage result, and flagged it as an addition everywhere it matters. A different coupling
would give different thresholds.

One more thing worth knowing from reading the code: **the quantity that reaches a steady
state is S/H, not S or H.** Both biomasses grow or shrink exponentially without bound,
because the model is biomass-specific and has no size limit. I measured this by running
the unmodified R code over a 4×5 light-by-DIN grid. Every readout is defined on the
ratio, and "the colony died" is not representable — the model has no mortality.

---

## 6. Two results I did not go looking for

**The ambient cost of a heat-tolerant symbiont falls out of the model unprompted, with
the right sign and the wrong size.** Raising the symbiont's thermal optimum by 2 °C is
the *only* one of the four knobs that costs anything at ambient temperature: −1.7% host
specific growth. The other three all *improve* ambient growth, because they reduce an
oxidative burden the control is already carrying. That is the right sign for the measured
Durusdinium trade-off and about an order of magnitude too small.

Pushing on it: I asked what reduction in the symbiont's carbon-fixation ceiling would
reproduce Jones & Berkelmans' measured penalty. **The model has no steady state with it.**
Host growth falls continuously only to about −22%, and below that the holobiont drops
into the bleached alternate state with negative growth. So this model does not support a
shifted thermal optimum as the explanation of the measured cost — which points at the
alternatives the literature already offers (Sproles' reduced carbon translocation per
cell, measured in an anemone), while Kemp 2023 disputes that the ambient cost exists at
all. **The model is not adjudicating this and should not be written as if it were.**

**The thermal knob is not a free knob, and encoding that changed the study.** The lead
pointed out that the same Cunning 2015 abstract carries a *sourced* trade-off I had left
as prose: "higher proportions of heat-tolerant symbionts linearly increased bleaching
resistance but reduced photochemical efficiency". That is a coupling, not a note, so it
is now in the model — the linearity and the sign are sourced to PMID 26041354, the slope
is not given in the abstract and is therefore swept rather than set.

Two things came out of encoding it, and the first is a mistake worth keeping on the
record. **My first encoding had the wrong sign**, and not through a typo: I put the
coupling on `yCL`, coRal's own named quantum yield, which looks like the obvious home for
"photochemical efficiency". But excess excitation energy in coRal is `jeL = jL − jCP/yCL`,
so *lowering* the quantum yield makes each unit of fixed carbon consume more photons,
which *reduces* the excess and therefore reduces ROS. Measured: raising the coupling from
0 to 0.3 improved both the thermal gain (+2.000 → +2.137 °C) and the ambient cost
(−1.65% → −0.10%) — the trade-off made the coral *better*. Putting it on `jCPm`, the
ceiling on carbon fixation, gives the intended direction. The trap is in the published
model's photon accounting, and anyone else extending coRal will meet it.

The second: **the break-even analysis cannot be completed, and that is the finding.** The
thermal gain from +2 °C falls to zero at a coupling strength of 0.39. But the coupling
strength that would reproduce the *measured* 29% growth penalty does not exist: the worst
steady-state cost the model will produce is −14.4%, and past that the holobiont drops into
the bleached alternate state rather than settling at a larger penalty. The independent
Durusdinium arm — scaling the carbon-fixation ceiling directly rather than through the
thermal optimum — reaches the same wall at −22.3%. Two routes, same gap, so it is the
model's bistability and not either arm's parameterisation. Either the alternate-stable-
state transition is too abrupt, or the measured Durusdinium penalty is not a
carbon-fixation effect at all.

**The model bleaches on cooling too.** Nothing was tuned for it; it follows from the fact
that anything lowering carbon fixation raises excess excitation energy. Silverstein,
Cunning & Baker 2017 cooled *Montastraea cavernosa* and found C3-hosting corals lost 94%
of their symbionts while D1a-hosting ones did not. Same sign. I have written this as a
weak consistency check and nothing more — no magnitude was compared, and degree heating
weeks have no cold analogue so no threshold is reported.

---

## 7. Failures, reported as failures

**The bleaching study's step-halving check FAILS, at 9.3%.** I did not move the declared
5% criterion. coRal integrates with explicit Euler and so does the port, and a
first-crossing readout inherits that slow convergence. What I did instead: publish the
full convergence table over four step sizes, give a Richardson estimate of the limit, and
then test the thing the study actually claims — **the knob ranking is identical at
dt = 0.1, 0.05 and 0.025**. The absolute threshold is not converged. The ranking and the
additivity verdict are.

**The settlement study's ranking was sitting on point estimates, and the lead was right
about which half survives.** I sampled the biology 20,000 times and then ranked
interventions by effort units I had invented — the structure the study exists to avoid.
Sampling those too (400 draws, unbiased lognormal perturbation of every cost) gives
exactly the prediction the lead made before the run: **sediment screening and mass larval
enrichment hold the top two slots in 94% of draws, and the order within them is 58/41 —
a coin flip.** So "those two are in a different class from the rest" is quotable and
"site screening beats larval enrichment" is not. There is now a `quotable` block in the
result file saying which numbers may be cited and why.

**The morphology study does not do what it was built to do.** It was meant to span
branching through plating through massive. It spans compact mound through open *lobed
mound*, and reaches neither branching nor plating. Four further settings were tried
beyond the sweep (lower interface regularisation, a larger lattice with a proportionally
larger colony, a steeper growth response) and all gave the same qualitative form. The
diagnosis is in the result file: the regularisation that makes the interface isotropic on
a cubic lattice is also what suppresses fingering, and at these system sizes the two
could not be separated. **The flow and light routes in `routes.json` must not cite this
study as showing that a growth model reproduces branching.** It does not.

**The route-outcome tagging by regex was wrong about ten times in forty-five**, and I
replaced it. See §8.

---

## 8. The methodological lesson, which is the most transferable thing here

Three separate times in this session, a check that *looked* like it was working was
measuring something else.

**(a) The morphology metrics could not see a lattice artefact.** Two voxel growth rules
were dominated by the lattice rather than by the physics: six-connected growth produced
square-based **octahedra**, twenty-six-connected growth produced **cubes** and hollow
square boxes. Through both of those, surface-to-volume, box-counting dimension and
bounding-box fill all varied **smoothly and plausibly** with the control parameter.
Declaring the metrics before looking — which I did, and which is right — protects against
choosing the metric that flatters the result. It does **not** protect against measuring an
artefact. Nothing except looking at the pictures did.

Two more failures in the same study had the same character: pinning the far field on all
six lattice faces let the colony reach a wall and feed on it (a flat mat at every
parameter value), and over-smoothing produced *the same compact mound to three
significant figures at every Damköhler number from 0.02 to 80* — which reads exactly like
"the control parameter does nothing".

**(b) The obvious bleaching readout was confounded with one of the knobs.** "Degree
heating weeks until the coral loses half its symbionts" cannot answer "which knob
dominates", because one of the four knobs *is* the coefficient converting oxidative
stress into symbiont loss. Asking whether it dominates is close to asking whether `b`
equals `b`. The tell was quantitative: **1,868 of 2,401 map cells censored** on that
readout. The fix was a second readout (host carbon balance) in which that knob does not
appear. The two then disagreed in a way worth writing up: on symbiont loss all four knobs
look comparable, but on host carbon balance the thermal optimum moves the threshold about
six times further than the other three. Three of the four interventions buy a coral that
**still looks brown while it starves**.

**(c) Tagging routes by running a regex over my own prose classified the prose.** The
HSF1 knockout came out as "recruitment" because its phenotype is in larvae; the
Durusdinium route came out as "skeleton" because the cost it pays is calcification; the
flow-plasticity route came out as "skeleton" because the sentence explaining it mentions
skeleton already laid down. All ten errors looked plausible. Outcomes are now declared per
route as a field; the regexes are kept only as an audit, and the 18 disagreements are
published in `routes.json` under `provenance.outcome_tagging` because they say something
about how a route is written.

There is also a fourth, smaller one: **degree heating weeks cannot see a sub-1 °C
failure, by construction**, because NOAA sums HotSpots only above MMM+1. A failure mode
that bites below that reads as zero. Worth a sentence for anyone using DHW as a design
currency.

---

## 9. Source disagreements to preserve (not an exhaustive list)

1. **Durusdinium's cost.** Jones & Berkelmans 2010 (−29% lab, −38% field), Little 2004
   (juvenile C 2–3× faster than D), Pettay 2015 (calcification "nearly half") **against**
   Kemp 2023 (no ambient difference, transfer maintained under heat).
2. **Is D even the tolerant partner?** Abrego 2008: *A. tenuis* juveniles did better with
   C1 than D, explicitly challenging "speculations that associations with type D are
   universally most robust". The conflict is between host species, not within one.
3. **Heat-evolved strains.** 10/10 better in vitro, 3/10 in larvae (and that 3 is against
   one of two wild types); SS8 good in adult *Galaxea* with no growth penalty; SS5 and
   SS9 among the most thermosensitive in anemones; mutagenesis lineages with growth and
   nutrient-uptake costs.
4. **Does flow change colony form?** Kaandorp & Sloot 2001 and Chindapol 2013 say yes;
   Merks 2003 says "We did not find an effect of flow" and that the earlier evidence "may
   not be conclusive". Unresolved between modelling groups.
5. **Is branching a liability under heat?** Loya 2001 (finely branched most susceptible)
   **against** McCowan 2012 (within families the pattern is inconsistent; branching
   faviids bleach *less* than massive ones) and Burn 2023 (massive *Porites* moved from
   among the least to among the most susceptible as severity rose).
6. **Methylation and acclimatisation.** Liew 2018 reads methylation change as
   acclimatisation; Abbott 2024's title is "Modifications to gene body methylation do not
   alter gene expression plasticity in a reef-building coral". Different species,
   different stressors, neither reports on the other.
7. **Herbivory.** Webster 2015: caging (macroalgae-dense) cut recruit survival 79%.
   Penin 2011: excluding predators and grazers did **not** change total mortality, it
   changed the cause. Do not model herbivory as monotonic protection.
8. **Heritability of thermal tolerance.** Bairos-Novak 2021's meta-analysis headline
   (high, some above 0.5) **against** Humanes 2024's directly measured 0.2–0.3 with no
   genetic correlation across stress regimes, and Lachs 2026's finding that a rapid
   heat-shock assay is *genetically uncorrelated* with heatwave tolerance. The trait
   definition drives the answer.
9. **Hybrids.** Chan 2018 (some hybrid groups better) **against** Lamb 2024 (hybrids did
   not outperform both parents; the purebred did best; the reciprocal cross failed).
10. **Does restoration scale?** Mula 2025 and Hughes 2023 (no) **against** Anthony 2020
    (a portfolio is needed whatever the emissions trajectory). Lockie 2025 is a
    social-science critique *of the critics* and is itself one side.
11. **Calcifying-fluid chemistry.** Dye imaging, microelectrodes and boron-isotope proxies
    give different absolute values and are measured on different things (tissue-level
    extracellular pH against skeleton-derived proxy). **Do not average across methods.**

---

## 10. Gaps I did not fill, and the cheapest way to fill them

- **Fuller et al. 2020's variance explained.** Nobody has read it. Do not quote an R² for
  a coral polygenic score from this page; the abstract has no number and two attempts at
  the full text failed.
- **Sevilgen et al. 2019's numeric calcifying-fluid values.** Abstract gives none.
- **Madin et al. 2023's demography dataset** (PMID 36882893) holds eggs-per-polyp and
  planar area for nine *Acropora* species at Lizard Island and is stated to be
  unrestricted. Downloading it would replace this page's single worst parameter —
  "polyps per colony", a 25-fold invented range that is the third-largest contributor to
  the recruitment spread.
- **Doropoulos 2016's stage-specific survival.** The Dryad dataset exists
  (doi 10.5061/dryad.rj653 per a web search); the paper itself 403s.
- **Connolly & Baird 2010 and Moneghetti 2019** hold fitted larval mortality and
  competence rate parameters in tables nobody reached.
- **PMID 41877353**, on multi-year symbiont legacy effects — title only, and it is the
  single most load-bearing gap on the symbiont route.
- **A coral ATAC-seq or Hi-C dataset**, if one exists as a preprint or data release.
  bioRxiv and GEO were not searched.

---

## 11. Things in `raw/` I deliberately did **not** carry onto the page

- **Bay et al. 2016's pre-stress D:C ratio of 0.003.** It is a good number and I kept it
  *inside* the shuffling route — but flagged, because its PMID could not be verified, a
  title search returned zero hits, and it was read at web-page level through a
  summariser. It is second-hand. Verify in the full text before anyone puts it in a
  figure.
- **The "five interventions" of van Oppen 2015.** The 2015 abstract does not enumerate
  them and the 2017 paper names four. The research block marks the fifth as unverified
  memory. I did not use the count.
- **Any per-coral cost figure.** The two real money figures in the literature (USD 35.20
  per surviving colony at 35 months in the Philippines; USD 334–577 per surviving coral
  at two years on the GBR) are from different species, years, accounting methods and
  survival horizons. They are in the page as separate facts and are **not** compared,
  because comparing them is the error the recruitment study exists to avoid.

---

## 12. Compute

Everything ran locally, capped (`systemd-run --scope -p MemoryMax -p MemorySwapMax=0
-p TasksMax`, `nice -n 19`). **No Nebius job was submitted.** The accretive-growth
morphospace was the candidate the brief named, and it did not need a GPU: the expensive
part is a Laplace solve, which parallelises across parameter sets on four local cores and
completed in well under an hour. Sending it to a shared 16-core H100 would have bought
wall-clock and spent somebody else's GPU hour on a job that does not use a GPU. If the
morphology study is ever pushed to the mesh-based implementation that would actually
produce branching, that is the job worth sending.
