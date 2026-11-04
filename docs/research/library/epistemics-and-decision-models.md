# Epistemics and decision models for a design swarm

**What this is for.** It specifies the scoring layer: how a graph of about 90 claims, each with an
evidence level, source read-levels, conflict and supersession edges, and challenge outcomes, becomes
(a) a belief with honest uncertainty, and (b) a ranking of where the next agent-hour goes.

**The short answer.**

1. **Aggregation.** Use a two-layer model. The discrete layer is a Dung argumentation framework built
   from the `challenge` table, with grounded semantics. The quantitative layer is a Beta evidence-count
   per claim, which is the same object as a binomial subjective-logic opinion and an
   imprecise-Dirichlet interval. Do not use Dempster's rule. Do not let agents choose priors.
2. **Weights.** A mapping from read-level to weight is defensible as a **declared, versioned policy
   with a sensitivity check**. As a calibrated quantity it is **invented precision**. The best
   clinical system, GRADE, has measured predictive validity of about C = 0.57, which is close to a coin.
3. **Priority.** `decisiveness × uncertainty × unblocking / cost` is **not** an approximation to EVPI.
   It is a different object wearing EVPI's clothes. It has the wrong functional form (EVPI is a `min`,
   not a product), it peaks in the wrong place, and it double-counts unblocking. Above all, it never
   asks whether the proposed work could change the decision. Replace it with a closed-form one-step
   EVSI (a knowledge-gradient step) per action, divided by expected agent-hours. Its inputs are two
   elicited regrets per decision-relevant claim, and everything else is derived from the graph.
4. **"JEV" does not exist** as a named value-of-information method in any source I could find
   (§3.2). I have not supplied a definition for it.
5. **Allocation.** Of Gittins, knowledge gradient, budgeted bandits and optimal stopping, only the
   **knowledge gradient** survives our setting: few arms, a fixed deadline, reward realised only in
   the final decision, and truth never observed directly. The stopping rule falls out of it.

The schema this targets is the one described in the task: `evidence_level ∈ {measured, simulated,
derived, literature, assumed, unknown}`, a read-level on every source, a `challenge` table with
outcomes `survived / weakened / refuted`, and supersession. **That schema is not in this repository.**
Here, `frontier/models.py` has `Evidence.evidence_kind ∈ {observed, predicted, simulated, formal,
source_assessment}` and an `Assessment` with seven reviewed dimensions. The read-level vocabulary
(`full-text`, `abstract only`, `could-not-access`, `full record`) comes from
`results/2026-10-31-oca2-exon21-molino-RESULT.md` §9. Field names below are therefore stated as
assumptions (§5.0).

---

## 0. Read-levels used in this document

This document uses the repository's convention so that nothing is quoted above its evidence.
Network access in this session was restricted: most publisher and CRAN hosts did not resolve. Most
references are therefore below `full-text`, and the levels say so.

| Level | Meaning here |
|---|---|
| `full-text` | Article body retrieved this session (via a summarising fetcher, so a quote is a near-quote) |
| `search-snippet` | Bibliographic details and specific numbers checked against search-engine abstracts and snippets this session; body not read |
| `recalled` | From prior knowledge and not re-checked this session. Treat the specific numbers as unverified. |

Every reference carries one of these levels in §7. Where a specific number carries argumentative
weight, its level is also given inline.

---

## 1. Evidence aggregation: six approaches compared

Two tests drive the comparison, because they are the ones the system needs most:

- **T1: Direct contradiction.** Two strong sources, one says *C*, the other says *¬C*. What comes out?
- **T2: Ignorance versus a 50/50 split.** Can the representation say "I have no evidence" in a form
  distinct from "the evidence balances at 0.5"?

### 1.1 Bayesian updating with explicit priors

**Mechanism.** Hold P(C), and update by Bayes' rule on the likelihood of each piece of evidence.

**T1.** Multiply the likelihoods. If both sources are treated as reliable and conditionally
independent, near-certain contradictory likelihoods produce a posterior driven almost entirely by
whichever hypothesis neither source ruled out. This is the same pathology as Zadeh's counterexample
(§1.2), and it shows the problem is **not specific to Dempster–Shafer**. The fix is the same in both
frameworks: model source reliability explicitly, with a latent "source is wrong" variable, before
combining.

**T2.** A point prior cannot pass T2: P(C) = 0.5 is the same number for both states. A second-order
prior can. Beta(1,1) and Beta(50,50) both have mean 0.5 but update very differently. There is a
subtlety that matters for §3. **For a single decision about a single binary event, only the mean
enters expected utility**, so the second-order spread is decision-irrelevant *now*. It becomes
relevant exactly when you ask how much a new observation would move you, which is EVSI. Bayes
represents "don't know" in the one place we need it, but only if it is hierarchical.

**What breaks when agents choose priors.**

- **The prior is a free parameter controlled by an interested party.** An agent proposing a claim
  sets the number that most affects that claim's ranking while evidence is thin. That is the regime
  all 90 claims are in.
- **"Ignorance" priors are not invariant.** A uniform prior over a quantity is non-uniform over its
  transforms. Bertrand's paradox and van Fraassen's cube factory are the standard demonstrations
  (`recalled`). So "the agent chose an uninformative prior" does not fix the problem.
- **Double counting.** Agents citing the same upstream paper are not independent likelihoods. The
  repository's `Evidence.source_dependence` field exists for this reason, and the aggregation must
  use it.
- **Unstated likelihoods.** Most of our evidence is not a measurement with a sampling model. Writing
  P(source says C | C) for a `literature, abstract-only` item is a second agent-chosen number,
  stacked on the first.

**The remedy is in the literature.** Use robust Bayes, i.e. report over a *class* of priors (Berger
1994, `recalled`), which is §1.4 under another name. Or **fix the prior by policy from an empirical
base rate**. We have one. `ledger/README.md` records our own novelty claims: zero of the candidate
headlines survived and one reproduction did. For the class "our own novelty claim", a base rate near
0.5 is contradicted by our own record.

### 1.2 Dempster–Shafer belief functions

**Mechanism.** A mass function m over subsets of a frame Θ. Bel(A) = Σ_{B⊆A} m(B), and
Pl(A) = 1 − Bel(¬A). Dempster's rule combines independent sources conjunctively and renormalises by
1 − K, where K is the mass the sources assign to disjoint sets (Dempster 1967; Shafer 1976, both
`recalled`).

**T2: yes, cleanly.** m(Θ) = 1 is total ignorance, [Bel, Pl] = [0, 1]. m({C}) = m({¬C}) = 0.5 gives
[0.5, 0.5]. This is the representation's main strength.

**T1: Zadeh's counterexample** (Zadeh 1984, 1986; `recalled` as to the source, numbers recomputed
here). Two doctors, Θ = {meningitis M, concussion C, tumour T}:

- Doctor 1: m₁(M) = 0.99, m₁(T) = 0.01.
- Doctor 2: m₂(C) = 0.99, m₂(T) = 0.01.

Only T∩T is non-empty, so K = 0.9999, and after normalisation **m(T) = 1.0**. Both experts thought
the tumour was nearly impossible, and the combination makes it certain. (Computed here: `nums.py`
in the session scratchpad reproduces K = 0.9999 and m(T) = 1.0000.)

**Is the criticism fatal? No, but it is fatal to one practice.**

- **The same arithmetic happens in Bayes** (§1.1). With a uniform prior and the doctors' reports
  treated as independent likelihoods, P(T) = 1 as well. What fails is the **assumption that two
  sources in total disagreement are both fully reliable**, which any conjunctive rule shares.
  Haenni (2005, `search-snippet`) argues that the surprise is due to the modelling rather than the
  rule. Dezert and colleagues dispute that Haenni addresses the original, exclusive-hypothesis
  version (`search-snippet`).
- **Discounting first fixes it.** Shafer discounting with reliability α = 0.9 (m′ = α·m, with
  1 − α moved to Θ) gives m(M) = m(C) = 0.469, m(T) = 0.010, m(Θ) = 0.053, and K = 0.81 (computed
  here). That is a sensible answer, with a large conflict mass that tells you something is wrong.
- **Alternatives move the conflict instead of normalising it away.** Yager's rule sends K to Θ,
  turning conflict into ignorance. Smets' transferable belief model keeps K on ∅ as an open-world
  signal. Dubois and Prade's disjunctive rule says "at least one is right" (all `recalled`).

**The lesson for us: never renormalise conflict away, and always report K.** Conflict is a finding.
In our setting, two strong sources disagreeing usually means one of them is wrong about scope
(ledger rows 8, 9, 13, 14). It does not mean the truth is halfway.

**What it costs.** For a binary claim the frame is {C, ¬C}, and a DS mass function on it is exactly
a triple (m(C), m(¬C), m(Θ)). That is a binomial subjective-logic opinion (§1.3). **Full DS buys
nothing extra unless claims have multi-way frames**, and the rule-choice controversy comes free with
it.

### 1.3 Subjective logic (Jøsang)

**Mechanism.** A binomial opinion ω = (b, d, u, a) with b + d + u = 1 and base rate a. The projected
probability is P = b + a·u. Opinions map one-to-one to Beta distributions via evidence counts r
(for) and s (against), with a non-informative prior weight W, conventionally 2:

  b = r/(r+s+W),  d = s/(r+s+W),  u = W/(r+s+W),  P = (r + W·a)/(r+s+W)

(Jøsang 2001; 2016 monograph; `recalled`.)

**T2: yes.** No evidence gives (0, 0, 1, a). Balanced strong evidence (r = s = 98) gives
(0.495, 0.495, 0.010). Both project to 0.5, and u separates them (computed here).

**T1: this is where it fails silently.** Cumulative fusion *adds evidence counts*. Fusing
(r=98, s=0) with (r=0, s=98) gives exactly the balanced-strong opinion above: **P = 0.5 with
u = 0.01, a confident 50/50.** The contradiction has become false precision. Subjective logic has a
separate degree-of-conflict measure, but the fused opinion does not carry it, so the system has to
compute and store it alongside. Dezert, Tchamova, Han and Tacnet (FUSION 2014, `search-snippet`)
argue that the opinion-to-Beta mapping and the fusion rules have foundational defects. I could not
retrieve their full text (onera.fr was unreachable from this session), so I do not restate their
specific examples.

**Does u earn its complexity? Yes, because it is not extra complexity.** This is the most useful
structural fact in §1. The binomial opinion with weight W is **the same object** as:

- a Beta(r + W·a, s + W·(1 − a)) distribution, i.e. hierarchical Bayes (§1.1);
- a DS mass function on a binary frame (§1.2);
- the **imprecise Dirichlet model** interval [r/(n+W), (r+W)/(n+W)], with n = r + s (Walley 1996,
  `recalled`). That interval is [b, b + u]. This identity is my derivation from the two definitions,
  not a quotation.

So the single representation **(r, s) evidence counts + W + a** gives a point (P), an interval
([b, b+u]), and an ignorance measure (u) at once. Its known weakness, conflict hidden by additive
fusion, is fixed by also storing the conflict (§5.2).

### 1.4 Imprecise probability and credal sets

**Mechanism.** Belief is a closed convex set of probability measures, summarised for a binary claim
by lower and upper probabilities [P̲, P̄] (Walley 1991; Levi 1974; Augustin et al. 2014; all
`recalled`).

**T2: yes, and it is the most principled answer.** Ignorance is [0, 1]. A 50/50 split is [0.5, 0.5].

**T1.** If you take the convex hull of two incompatible credal sets (the "one of them is right"
reading), you get a wide interval that is honest but uninformative. If you intersect them, you get
the empty set, which is an explicit inconsistency signal. Both are better than renormalisation.

**When is an interval the honest answer rather than a point?** In three cases:

1. When the weights are a policy, not a calibration (§2). Here the interval is the range of P over
   the plausible weight tables, and reporting a point would claim precision we do not have.
2. When evidence is thin enough that the choice of W or a moves P by more than the decision margin.
3. When sources conflict and we cannot yet say which one failed.

In all three, **the interval is what a downstream reader needs to see**. Whether to act on it is a
separate question.

**Costs.**

- **Decision rules multiply.** Γ-maximin, maximality and E-admissibility can disagree, and none is
  canonical (Troffaes 2007, `recalled`).
- **Dilation.** Conditioning on new evidence can *widen* every interval (Seidenfeld and Wasserman
  1993, `recalled`). A VOI computation over credal sets therefore has no single value.
- **Full credal VOI is not worth building for us.** Use the IDM interval from §1.3 for *display*,
  and the projected P for *decision*. That is a named approximation, and §5.6 gives its cost.

### 1.5 Argumentation frameworks (Dung; ASPIC+)

**Mechanism.** A Dung framework is a pair (A, R): arguments, and an attack relation R ⊆ A × A.
Semantics pick acceptable sets. The **grounded** extension is the least fixed point of "accept what
is defended by what is already accepted". It is unique, sceptical, and computable in polynomial
time (Dung 1995, `recalled`). Caminada's labellings give each argument IN, OUT or UNDEC (Caminada
2006, `recalled`).

ASPIC+ adds structure (Prakken 2010; Modgil and Prakken 2013, 2014; all `recalled`):

- arguments are built from premises and strict or defeasible rules;
- attacks come in three types: **undermining** a premise, **rebutting** a conclusion, **undercutting**
  an inference;
- a preference ordering turns attacks into **defeats**.

**T1.** Two claims that rebut each other with no preference between them both come out UNDEC under
grounded semantics. Under preferred semantics they form two extensions. This is the right
qualitative answer: "contested", not "0.5".

**T2: no, and this is the critical failure.** **An argument nobody has attacked is IN.** A claim at
`evidence_level = assumed` that nobody has challenged is accepted by grounded semantics. Under plain
Dung, *not having been looked at* is indistinguishable from *having survived*. UNDEC also conflates
"deadlocked" with "unresolved".

The repair is to require support: **evidential argumentation**, where arguments must trace to
evidence (Oren and Norman 2008, `recalled`), or bipolar frameworks with a support relation (Cayrol
and Lagasquie-Schiex 2005, `recalled`). In practice, that means a fourth label, UNSUPPORTED, applied
before the semantics run.

**Why we want argumentation anyway: reinstatement.** Twice in `ledger/README.md` a refutation was
itself defeated:

- Row 9: "the refutation was itself mis-operationalised".
- Row 14: "…and the original OLS refutation doesn't hold either" (retracted).

Dung semantics handle this natively. If B attacks A and C attacks B, then A is reinstated. No
weighting scheme does this without being told to.

**What it takes to make our `challenge` table a formal attack relation:**

1. **Nodes.** Arguments are claims *and* challenges. A challenge must be able to target a challenge,
   or reinstatement cannot be expressed: `challenge.target_kind ∈ {claim, challenge}`.
2. **Separate attack from defeat.** The structural attack is "this challenge asserts a contrary of
   the target", and it exists from the moment the challenge is filed. The **outcome** field is a
   resolved preference judgement in the ASPIC+ sense:
   - `refuted` means the attack succeeded as a **defeat**. Add the edge to R.
   - `survived` means the attack was made and failed (the target was not weaker). Record it, but keep
     it out of R. It feeds the quantitative layer as evidence of robustness.
   - `weakened` has **no Dung analogue**. Dung is all-or-nothing. It needs either gradual or
     quantitative bipolar semantics (Amgoud and Ben-Naim 2013; Baroni, Rago and Toni 2019; Rago et
     al. 2016, DF-QuAD; all `recalled`), or, more simply, it goes to the quantitative layer (§5.2).
3. **Add `attack_type ∈ {undermine, rebut, undercut}`.** It matters quantitatively. An *undercut*,
   such as a scope error (ledger row 8) or a vacuous theorem (row 6, `not_lt`), removes the support
   the attacked inference gave. It does **not** count as evidence for ¬C. A *rebut* is evidence for
   ¬C. An *undermine* zeroes the weight of the attacked source.
4. **Claim–claim conflict edges** become symmetric rebuttals.
5. **Supersession is not an attack.** It is versioning, so a superseded claim leaves the active
   framework. This matches the repository's position that dispute does not propagate
   (`specs/SPEC-002-contribution-review-lifecycle.md`, point 2).
6. **Not needed:** Caminada and Amgoud's rationality postulates (2007, `recalled`) and closure under
   strict rules. We have no strict rules worth closing over.

Probabilistic argumentation (Hunter 2013; Hunter and Thimm 2017; both `recalled`) would need a
probability on each argument that we cannot supply. Do not attempt it.

### 1.6 Hierarchy-based rating (GRADE / IPCC) as an aggregation method

These are rating systems more than combination rules, and §2 covers them as such. They appear here
because the IPCC scheme is the one place where T2 has been **institutionalised**. IPCC AR5 guidance
keeps *confidence*, a qualitative judgement from evidence × agreement, on a separate axis from
*likelihood*, a calibrated probability term (Mastrandrea et al. 2010, `recalled`). "About as likely
as not, low confidence" and "about as likely as not, high confidence" are distinct statements. That
is exactly our u versus P.

### 1.7 Summary table

| Approach | T1: direct contradiction | T2: "don't know" ≠ 50/50 | Inputs we lack | Verdict for us |
|---|---|---|---|---|
| Bayes, point prior | Product; pathological if both sources assumed reliable | **No** | Priors and likelihoods for non-measurement evidence | Reject as stated |
| Bayes, hierarchical (Beta) | Same pathology without a reliability model | Yes, via concentration, which matters only for EVSI | Likelihoods | **Keep, as evidence counts** |
| Dempster–Shafer | Renormalises conflict away (Zadeh) unless discounted | **Yes** | Reliability α per source | Use K as a diagnostic only |
| Subjective logic | Cumulative fusion yields confident 50/50 | **Yes** (u) | W, a | **Keep: it is the same object as Beta and IDM** |
| Credal / IDM | Hull: wide interval; intersection: empty | **Yes**, most principled | A decision rule | Use the interval for display only |
| Dung / ASPIC+ | UNDEC, i.e. "contested" | **No** (unattacked = IN) unless support is required | Nothing new | **Keep as the discrete layer** |

---

## 2. Evidence hierarchies and weighting

### 2.1 How the three traditions assign weight

**GRADE** (Guyatt et al. 2008; Balshem et al. 2011; `recalled`) **refuses numerical weights.**

- A body of evidence starts at *high* certainty if it comes from randomised trials, and at *low* if
  observational.
- It is rated down for risk of bias, inconsistency, indirectness, imprecision and publication bias.
- It is rated up for a large effect, a dose–response, or plausible confounding that would oppose the
  effect.
- The output is one of four ordinal levels, describing confidence that the true effect is close to
  the estimate.
- **The weights inside a meta-analysis are inverse-variance**, a statistical quantity. GRADE never
  turns its rating into a weight.

**IPCC** (Mastrandrea et al. 2010, `recalled`) has two separate axes:

- **Confidence** (very low … very high) from evidence type, amount, quality and consistency, crossed
  with agreement. It is qualitative.
- **Likelihood**, calibrated terms: virtually certain 99–100%, very likely 90–100%, likely 66–100%,
  about as likely as not 33–66%, unlikely 0–33%, very unlikely 0–10%, exceptionally unlikely 0–1%.
  The ranges are nested and overlapping by design.

**Systematic-review practice** (Cochrane Handbook, `recalled`):

- Weight by inverse variance within a meta-analysis.
- Assess risk of bias per study (RoB 2) and do not average it into a single quality score. Composite
  quality scores were abandoned because different scales gave contradictory rankings of the same
  trials (Jüni et al. 1999, `recalled`).
- Run sensitivity analyses excluding high-risk studies, rather than down-weighting them by a number.

### 2.2 What is measured about whether these work

**GRADE reliability is moderate, with training** (Mustafa et al. 2013, `search-snippet`). Inter-rater
reliability for two raters was about 0.66 with GRADE, against about 0.27–0.31 for intuitive
judgement, and about 0.80–0.84 with three or four raters pooled. (The snippets did not name the
statistic, so I do not call it kappa.)

**GRADE predictive validity is low** (Gartlehner et al. 2016, *J Clin Epidemiol* 70:52–60,
`search-snippet`). The test was whether the certainty grade predicts that an effect estimate stays
stable as new studies arrive:

- C-index 0.56–0.58, with 95% CIs reaching down to about 0.47 and 0.50;
- *high* grades were stable **less** often than producers and users expected;
- *low / insufficient* grades were stable **more** often than expected.

This is the single most important number in §2. **The most developed evidence-grading system in
existence discriminates future stability barely better than chance.**

**IPCC terms are misread** (Budescu, Broomell and Por 2009, *Psychol Sci* 20:299–308,
`search-snippet`). Readers' numerical interpretations of IPCC probability terms were regressive
toward 0.5 and deviated from the guideline ranges *even with the guidelines available*. Embedding
the numeric range in the sentence helped. A cross-national follow-up found the same pattern (Budescu
et al. 2014, *Nature Climate Change*, `recalled`).

**Performance-weighting experts does work, a little, out of sample** (Colson and Cooke 2017,
*Reliab Eng Syst Saf* 163:109–120, `search-snippet`). Across 33 studies, performance weights fitted
on calibration questions beat equal weights in-sample in 32 of 33. Under cross-validation there is
an **out-of-sample penalty** in statistical accuracy. On their combined accuracy × informativeness
index, performance weights win in 26 of 33.

**Known criticisms:**

- GRADE's validity evidence is thin; Kavanagh 2009 (*PLoS Med*, `recalled`) argued it lacked
  demonstrated validity and reliability.
- The start-high/start-low rule for randomised versus observational designs encodes a design
  hierarchy that comparative studies do not uniformly support (Concato et al. 2000, `recalled`).
- IPCC confidence and likelihood are applied inconsistently across working groups, and the two axes
  are often confused (Aven and Renn 2015, *Climatic Change*, `recalled`).
- Multiplying ordinal ratings, as in risk matrices, can rank risks worse than random (Cox 2008, *Risk
  Analysis* 28:497–512, `recalled`). This applies directly to §3.4.

### 2.3 Is a read-level → weight mapping defensible?

**As a calibrated quantity: no, it is invented precision.** Nothing measures how much less reliable
an `abstract-only` citation is than a `full-text` one, for our kind of claims. GRADE, with decades of
use, has C ≈ 0.57 for predictive validity. We have about 90 claims.

**As a declared policy: yes, if it meets four conditions.**

1. **It is ordinal at heart and coarse.** Three or four distinct levels, not a continuum.
2. **It contains hard rules, not just weights.** These are the parts that are actually defensible:
   - a `could-not-access` or `recalled` source contributes **zero**;
   - an `abstract-only` source may support only what its abstract states. This is a *cap on scope*,
     not a down-weight (cf. Protas et al. 2006 handled exactly this way in the oca2 result §9);
   - sources sharing an upstream count **once**, as GRADE counts bodies of evidence rather than
     citations.
3. **It is versioned** under `policy_version`, which the repository's `Assessment` already carries.
4. **Every reported belief comes with a sensitivity check.** Perturb each weight up and down by one
   level and report whether the claim's label or ranking changes. A claim whose status depends on the
   exact weight table is reported as an **interval** (§1.4, case 1).

**Evidence level is not a scalar quality either.** `derived` (a proof or calculation) can be certain
about a model and say nothing about the world. `CONTRIBUTING-VERIFICATION.md` makes exactly this
point: a Lean theorem "says nothing about an organism". Ledger row 6 is a compiled theorem that was
vacuous. GRADE handles this as *indirectness*, a separate axis. We should do the same: a `derived`
item contributes full weight only to claims *about the model*, and a reduced weight to claims about
the world.

**There is a route to earning the precision later.** Challenge outcomes and later `measured`
resolutions are observable. Once there are a few dozen resolved claims per evidence level, fit the
weights to predict refutation, for example with an ordinal logistic model, and report the
out-of-sample C-index. Expect something like GRADE's number. If the fit does not beat the declared
table, keep the table.

---

## 3. Value of information: the decision half

### 3.1 Definitions

Notation:

- d is a decision chosen from a set D;
- θ is all uncertain quantities, with current distribution p(θ);
- U(d, θ) is the payoff, in health economics usually net monetary benefit;
- θ = (φ, ψ), where φ is the subset of interest and ψ the rest;
- X is data from a proposed study.

All four definitions below follow Rothery et al. 2020, ISPOR VOI Task Force Report 2 (`full-text`,
via summariser), and the earlier sources it builds on (Raiffa and Schlaifer 1961; Claxton 1999; Ades,
Lu and Claxton 2004; `recalled`).

**EVPI: the value of resolving all uncertainty.**

  EVPI = E_θ[ max_d U(d, θ) ] − max_d E_θ[ U(d, θ) ]

- *Requires:* a decision set, a payoff function, and the joint distribution of θ.
- *Cheap:* one Monte Carlo loop over draws from p(θ). Monte Carlo draws are the "probabilistic
  sensitivity analysis" (PSA) sample in health-economics terms.

**EVPPI: the value of resolving the parameter subset φ only.**

  EVPPI(φ) = E_φ[ max_d E_{ψ|φ}[ U(d, φ, ψ) ] ] − max_d E_θ[ U(d, θ) ]

- *Requires:* everything EVPI needs, plus the conditional p(ψ | φ).
- *Costly:* a nested double loop, which is biased when the inner loop is small.
- EVPPI(φ) is an upper bound on the EVSI of any study informative only about φ.

**EVSI: the value of a specific study that yields data X.**

  EVSI = E_X[ max_d E_{θ|X}[ U(d, θ) ] ] − max_d E_θ[ U(d, θ) ]

- *Requires:* everything above, plus a **likelihood p(X | θ) for the proposed study**. This is a
  preposterior analysis.
- *Costly:* nested, and the inner step is a Bayesian update per simulated dataset.

**ENBS: the net value of a study.** ENBS = population EVSI − cost of the study, where cost includes
fixed, variable and opportunity costs. ENBS ≥ 0 is a necessary condition for doing the study.
Population scaling multiplies per-person VOI by the discounted beneficiary population over a time
horizon. Rothery et al. note that information "is not valuable indefinitely" and that the horizon is
among the hardest inputs to estimate.

**Two properties matter most for us:**

- **0 ≤ EVSI ≤ EVPPI ≤ EVPI.**
- **A study whose every possible result leaves the optimal decision unchanged has EVSI = 0, however
  uncertain θ is.**

### 3.2 "JEV" / "joint expected value"

**I could not find a value-of-information method by that name, and I do not believe one exists.**

Two searches (`extended`, then `standard`) for "JEV", "joint expected value" plus value of
information, and research prioritisation, returned the following:

- **The ISPOR task-force reports**, which define EVPI, EVPPI, EVSI and ENBS and use no "JEV".
- **"Joint EVPPI"** (also "group EVPPI"): EVPPI computed for a *set* of parameters jointly, as in
  SMDM course material listing "EVPPI for single parameters, joint EVPPI for groups of parameters,
  conditional EVPPI and sequential EVPPI" (`search-snippet`). This is the nearest real thing. It is
  EVPPI(φ) above with φ a vector, and it is **not additive**: the joint EVPPI of two parameters is
  generally not the sum of their single EVPPIs.
- **An unrelated arXiv paper** (arXiv:2609.24965, *Jev for Scientific Decisions: Evaluating Semantic
  Choices and Their Consequences*, Deng et al., 2026; abstract page fetched, so `abstract-only`). It
  names a *system configuration* "Jev" and never expands it. It is not a VOI method.

**The nearest real things, then:**

1. joint or group EVPPI;
2. EVSI for a portfolio of studies;
3. Glynn et al. 2024, *PharmacoEconomics* 42(9), a **rapid, judgement-based VOI** for research
   commissioning when there is no time for a full model (`search-snippet`). This is the closest real
   relative of our heuristic, and §3.4 uses it as the comparator.

If "JEV" is a term from an internal document, it should be defined there and not attributed to the
literature.

### 3.3 How VOI is computed in practice (health economics)

Per Rothery et al. 2020 (`full-text`, via summariser), Kunst et al. 2020 (`search-snippet`), and the
methods papers they cite:

- **EVPI** comes straight from the PSA sample. Thousands of draws are typical. It is cheap.
- **EVPPI.** The nested double loop is the reference method and is expensive. The standard
  approximation is **regression on the PSA sample**: regress net benefit on φ with a GAM or Gaussian
  process (Strong, Oakley and Brennan 2014, *Med Decis Making* 34:311–326, `search-snippet`) or with
  INLA for many parameters (Heath, Manolopoulou and Baio 2016, `recalled`). It needs no re-running of
  the model. Single-loop methods apply when the model is (multi)linear in ψ.
- **EVSI.** There are four standard approximations, compared in Kunst et al. 2020 (`search-snippet`):
  - regression on a summary statistic of simulated data (Strong et al. 2015, `recalled`);
  - importance sampling;
  - moment matching (Heath, Manolopoulou and Baio 2018, `search-snippet`);
  - Gaussian approximation (Jalal and Alarid-Escudero 2018, `search-snippet`). This one is biased for
    nonlinear models; Li, Jalal and Heath 2024 propose a correction (`search-snippet`).

  A companion comparison reports these running in **minutes to hours versus weeks** for nested Monte
  Carlo (`search-snippet`).

**What all of this presupposes is a validated decision model.** That means a payoff function over a
parameterised state, with a defensible joint distribution over the parameters. **The approximations
make computation cheap. They do nothing for missing inputs.** In our setting computation was never
the bottleneck: 90 binary claims evaluate in milliseconds in closed form. The bottleneck is entirely
that U(d, θ) and p(X | θ) do not exist.

### 3.4 The blunt question: is `decisiveness × uncertainty × unblocking / cost` an approximation to EVPI?

**No. It is a different thing wearing its clothes.** It shares EVPI's intuition, "stakes times doubt",
but it differs in form, in where it peaks, and in what it ignores. Take the simplest honest case: a
claim C that gates a binary choice, build on C or shelve it, with two regrets measured in agent-hours
of rework:

- L_FP is the cost of building on C when C is false;
- L_FN is the cost of shelving C when C is true;
- p is the current belief in C.

Then

  **EVPI(C) = min( (1 − p)·L_FP ,  p·L_FN )**

This is derived from §3.1: the expected loss of the best act under current information, against
zero under perfect information. The heuristic gets five things wrong.

**1. EVPI is a `min`, not a product, and it peaks at the indifference point, not at p = 0.5.**
EVPI is a tent with its apex at p* = L_FP / (L_FP + L_FN). Our regrets are typically asymmetric:
building on a false claim is expensive, as the 16 rows of `ledger/README.md` testify. With
L_FP = 10 and L_FN = 1, p* = 0.909. All values below are computed here:

| p | EVPI (agent-hours) | What "uncertainty", read as closeness to 0.5, says |
|---|---|---|
| 0.50 | 0.50 | maximal |
| 0.90 | 0.90 | low |
| 0.909 | **0.909**, the maximum | low |
| 0.95 | 0.50 | very low |

**The heuristic ranks these in the opposite order from EVPI over most of the range.**

**2. For one binary decision, EVPI does not depend on the second-order uncertainty u at all.** EVPI is
a function of p alone. If "uncertainty" means u (ignorance), it does not belong in EVPI. It belongs
in **EVSI**, where it governs how far one more check moves p. If it means closeness to 0.5, it belongs
in EVPI but with the wrong peak. Either way the product is not EVPI.

**3. It never asks whether the proposed work could change what we do.** This is the decisive defect.
With W = 2, a = 0.5, regrets 3 : 1 (so p* = 0.75), and a check worth 8 pseudo-counts, consider three
claims with the same projected p ≈ 0.67. All values are computed here:

| Claim evidence (r, s) | p | u | EVPI | EVSI of this check |
|---|---|---|---|---|
| (1, 0), thin | 0.667 | 0.667 | 0.667 | **0.424** |
| (3, 1) | 0.667 | 0.333 | 0.667 | **0.286** |
| (30, 14), heavy | 0.674 | 0.043 | 0.674 | **0.000** |

The same three claims checked with a **weak** check (2 pseudo-counts) all have EVSI = 0, because
neither outcome crosses p*. **Uncertainty is necessary for value, not sufficient.** The heuristic
would spend agent-hours on all of these. EVSI says which ones the specific action can resolve.

**4. Unblocking is double-counted.** In a decision model, a claim gating k downstream items raises
the regrets: the rework if C is wrong propagates to its dependants. If "decisiveness" already
reflects stakes, multiplying by an unblocking count counts the same thing twice. The right place for
it is **inside L**, computed from the typed edges.

**5. Products of ordinal agent judgements are not quantities.** Two agent-assigned 1–5 scores
multiplied together inherit the risk-matrix problem (Cox 2008, `recalled`). The ranking depends on
arbitrary scale spacing. The agents scoring decisiveness and uncertainty also often propose the work
themselves. That is the same conflict as agent-chosen priors (§1.1).

**What the heuristic is, charitably.** It is a **rapid, judgement-based research-priority score**, in
the family of Glynn et al. 2024 but without that paper's anchoring to a decision. Its virtue is that
it needs no model. Its vice is that it gives no warning when it is wrong.

**The fix keeps almost all of its cheapness.** Derive p and u from the evidence layer, elicit only
the two regrets, and compute EVSI in closed form (§5.3).

---

## 4. Sequential allocation under a deadline

**Our setting:**

- the arms are research actions on about 90 claims;
- an action's reward is *information*, realised only through better final decisions;
- truth is rarely observed; we see challenge outcomes and occasional measurements;
- arms are **correlated** through the claim graph;
- several agents run **in parallel** under leases (`specs/SPEC-003`);
- the budget **ends at a fixed time**.

| Method | Designed for | What breaks here | Verdict |
|---|---|---|---|
| **Gittins index** (Gittins 1979, `recalled`) | Infinite-horizon *discounted* reward, independent arms, one pull at a time, unplayed arms frozen, rewards observed | Not index-optimal under a fixed finite horizon (Berry and Fristedt 1985, `recalled`). Not optimal with multiple simultaneous plays. Arms are correlated. Rewards are delayed and partly unobservable. The objective is final decision quality, not cumulative reward. | **Does not survive.** Every optimality condition is violated. |
| **Budgeted bandits / bandits with knapsacks** (Tran-Thanh et al. 2010, 2012; Badanidiyuru, Kleinberg and Slivkins 2013; `recalled`) | Many pulls, cumulative reward, regret bounds | The guarantees are asymptotic in the number of pulls; we have tens of pulls over about 90 arms. The objective (cumulative reward) is wrong for us. Delay is a tractable extension (Joulani et al. 2013, `recalled`); unobservable reward is not. | **Does not survive** as a policy. Its fractional-knapsack intuition (rank by value per unit cost) does. |
| **Best-arm identification, fixed budget** (Audibert, Bubeck and Munos 2010; Russo 2020; `recalled`) | Pure exploration within a fixed budget | Closer: it optimises the end state. But the goal "identify the single best arm" is not ours. We want many claims each resolved enough for its own decision. | Partial. It confirms the objective should be the end state. |
| **Knowledge gradient** (Frazier, Powell and Dayanik 2008, 2009; Ryzhov, Powell and Frazier 2012; `recalled`) | Offline ranking and selection under a finite measurement budget, Bayesian beliefs, value = quality of the final decision. Has a correlated-beliefs version. | **Myopic.** The one-step value of information is non-concave: one small check can be worth zero while two are worth a lot (Radner and Stiglitz 1984; Frazier and Powell 2010, KG(*), `recalled`). Needs a belief model with a likelihood for the measurement. | **Survives.** KG *is* one-step EVSI. Patch the non-concavity with KG(*), §5.4. |
| **Optimal stopping** (Chow, Robbins and Siegmund 1971, `recalled`) | When to stop sampling one process | We stop per claim, not once. With KG the per-claim rule is "stop when max EVSI per hour falls below the opportunity cost of an hour elsewhere". This complements the preregistered stop rules already in use. | **Survives as a rule derived from KG**, not as a separate machine. |

**Parallel agents.** Greedy batch selection would send every free agent to the same top-ranked claim.
The standard heuristic is to *fantasise*: after leasing an action, update the claim's belief as if
the expected outcome had arrived, then re-rank. This is the "kriging believer" heuristic of
Ginsbourger et al. 2010 (`recalled`). It is cheap and good enough.

**The deadline.** Multiply each action's EVSI by P(completes before T) and charge its full expected
cost. Near T this automatically favours short, decisive checks, which is the behaviour we want.

**Delayed and unobservable reward.** We never learn the reward of an allocation. We learn only
whether a later challenge or measurement agreed with the belief at the time. So the policy cannot be
*learned* from its own reward. It can only be **checked for calibration**: claims scored at p ≈ 0.8
should survive later resolution about 80% of the time. That check is the only empirical test the
scoring layer gets, and it should be built in from the start (§5.5).

---

## 5. Recommendation, specified to implement

### 5.0 Assumed fields

The following are taken from the task description. The names are hypothetical; map them to the real
schema.

- `claim(id, evidence_level, status, superseded_by)`
- `source(id, claim_id, stance ∈ {supports, opposes}, read_level, upstream_key, evidence_level)`.
  `upstream_key` identifies a shared origin. This repository's `Evidence.source_dependence` is the
  analogue.
- `challenge(id, target_kind, target_id, outcome ∈ {survived, weakened, refuted}, attack_type, independent: bool)`.
  **`attack_type` and challenge-to-challenge targeting are new** (§1.5).
- `conflict(claim_a, claim_b)`
- `depends_on(downstream_id, claim_id)` typed edges.
- `decision(claim_id, L_fp_hours, L_fn_hours, elicited_by)`. **New.**
- `action(id, claim_id, kind, est_hours, weight_class)`. **New**, or derived from the existing action
  records.

### 5.1 Discrete layer: argumentation status

1. **Active framework.** Include claims with `superseded_by IS NULL`, plus all challenges.
2. **Support gate.** A claim with no source of positive weight (§5.2) is labelled **UNSUPPORTED** and
   excluded from the semantics. This is the repair for T2 (§1.5).
3. **Build R:**
   - (challenge → target) for each `outcome = refuted`;
   - both directions for each `conflict`.
   - `survived` and `weakened` do not enter R.
4. **Labelling.** Compute the grounded labelling by fixed point: an argument is IN if all its
   attackers are OUT; OUT if some attacker is IN; otherwise UNDEC. Report each claim as
   **ESTABLISHED (IN), DEFEATED (OUT), CONTESTED (UNDEC) or UNSUPPORTED.**

### 5.2 Quantitative layer: evidence counts

For each active claim, accumulate pseudo-counts r (for) and s (against).

**Sources.** Group by `upstream_key` and keep the maximum weight per group. Weight is a table indexed
by `evidence_level × read_level`, versioned as `policy_version`. **The numbers below are a starting
policy, not a calibration:**

| evidence_level \ read_level | full-text / full record | abstract-only | could-not-access / recalled |
|---|---|---|---|
| measured | 4 | 2 (scope-capped) | 0 |
| simulated | 2 | 1 | 0 |
| derived | 2 if the claim is about the model; 0.5 if about the world | 0.5 | 0 |
| literature | 2 | 1 (scope-capped) | 0 |
| assumed / unknown | 0 | 0 | 0 |

**Challenges.** Each challenge contributes by outcome and attack type, and only if `independent`:

- `survived`: r += 1. A failed attack is weak evidence of robustness.
- `weakened`:
  - rebut: s += 1;
  - undercut: multiply the r-contribution of the attacked inference by 0.5;
  - undermine: halve the attacked source's weight.
- `refuted`:
  - rebut: s += 4;
  - undercut: set the attacked inference's r-contribution to 0, and do **not** add to s;
  - undermine: set the attacked source's weight to 0.
- A challenge that is itself DEFEATED in §5.1 contributes nothing. This is reinstatement.

**Output per claim:**

- **P** = (r + W·a) / (r + s + W)
- **interval** = [r/(n+W), (r+W)/(n+W)], with n = r + s
- **u** = W/(n+W)
- **conflict** κ = 2·min(r, s)/(r + s), or 0 when n = 0

with W = 2. The base rate **a** is fixed *per claim class from our own record*, never by the
proposing agent. For "our own novelty claim", the ledger implies a low a. Set 0.5 elsewhere until
data exist.

**Display rule:**

- If u > 0.5, show "**insufficient evidence**", not P.
- If κ > 0.5 and n ≥ 4, show "**contested**", not P.
- Otherwise show P with its interval.

This is what makes "I don't know" and "50/50" look different on screen.

### 5.3 Priority: one-step EVSI per action

The ranking covers only claims that gate a recorded `decision`. Claims that gate nothing have zero
decision value. That is a finding, not a bug: list them separately as "unscored".

1. **Regrets.** Elicit L_FP and L_FN in agent-hours. Add downstream rework: for each claim
   transitively in `depends_on` below this one, add its own L, discounted by the probability the
   dependant would actually be pursued. This is where unblocking lives (§3.4, point 4).
2. **Current loss.** ℓ(p) = min((1 − p)·L_FP, p·L_FN).
3. **Update model.** An action of weight w (from its `weight_class`, using the same table as §5.2)
   comes out favourable with predictive probability P:
   - favourable: p⁺ = (r + w + W·a)/(n + w + W);
   - unfavourable: p⁻ = (r + W·a)/(n + w + W).
4. **EVSI(action)** = ℓ(P) − [ P·ℓ(p⁺) + (1 − P)·ℓ(p⁻) ].
5. **Priority** = EVSI · P(done before deadline) / est_hours.
6. **Tie to EVPI.** Report EVPI = ℓ(P) beside it as the ceiling. An action with EVSI ≈ 0 and
   EVPI ≫ 0 needs a *stronger* check, not abandonment.

### 5.4 Non-concavity patch (KG*) and parallelism

- **KG\*.** For each claim, also compute EVSI for m = 1…4 repetitions of the action, i.e. weight
  m·w. Use max_m EVSI(m)/(m·hours) as the priority. This prevents abandoning claims that a single
  weak check cannot flip.
- **Parallel leases.** When an action is leased, update that claim's (r, s) by the *expected* outcome
  for ranking purposes only, then re-rank for the next free agent (§4).

### 5.5 Calibration loop

This is the only empirical test the layer gets, so build it from the start.

- Log (claim, P, u, label, timestamp) whenever a claim's belief changes.
- When a claim is later resolved by a `measured` result, or by a refuting or surviving independent
  challenge, record the outcome.
- Report a reliability diagram and a Brier score per `policy_version`.
- Consider refitting the §5.2 weights only once there are enough resolved claims to estimate an
  out-of-sample C-index. Keep the declared table unless the fit beats it.

### 5.6 The approximations, and what each costs us

| Approximation | Replaces | Cost |
|---|---|---|
| A binary decision per claim (build/shelve) | A real decision model U(d, θ) | Misses decisions with more than two options and claims that matter only jointly. Joint EVPPI interactions are not captured. |
| Pseudo-count likelihood (an action adds w to r or s) | A real p(X \| θ) per action | The action is assumed to report on truth with reliability fixed by its weight class. A biased check (one that systematically survives, cf. ledger row 15's checker) inflates confidence. Mitigation: mutant controls, as the ledger already requires. |
| Declared weight table | Calibrated source reliabilities | Invented precision if anyone reads the numbers as measured. Mitigated by versioning, the sensitivity check (§2.3), and §5.5. |
| A per class, W = 2 | Agent priors | Wrong class assignment biases thin claims. W = 2 is a convention (Jøsang; IDM with s = 2), not a derivation. |
| Ignore second-order credal VOI | Credal-set decision theory | We act on P while displaying an interval. Under strong ambiguity aversion this is the wrong decision rule. Accepted, because no inputs exist for anything better. |
| One-step plus KG\* lookahead | The full dynamic programme | Can still be myopic over multi-claim sequences where a claim matters only after another resolves. |
| Fantasised outcomes for parallel leases | A joint batch-VOI optimisation | Mild over- or under-dispersion of agents. Harmless at our scale. |
| Elicited regrets L_FP, L_FN | Derived utilities | **The one irreducible judgement.** It is kept, but narrowed to two numbers in a common unit (agent-hours), visible and attributed (`elicited_by`), and auditable after the fact against actual rework. |

### 5.7 What NOT to attempt, because the inputs do not exist

- **Full EVPPI or EVSI by Monte Carlo** over a joint parameter distribution. There is no decision
  model and no joint distribution. Any such computation would be built on fabricated inputs, however
  rigorous the estimator. Regression, moment matching and INLA solve a computation problem we do not
  have.
- **Population scaling, discounting and time horizons** (ENBS in the health-economics sense). We have
  no beneficiary population.
- **Dempster's rule or Dempster–Shafer over multi-way frames.** On binary claims it adds nothing over
  §5.2 except the Zadeh controversy. Keep only κ (§5.2) as a conflict diagnostic.
- **Probabilistic or weighted argumentation** with numbers on arguments. No such numbers exist.
- **Gittins indices.** Every optimality condition is violated (§4).
- **Regret-bound bandit algorithms.** Wrong objective, wrong scale.
- **Agent-assigned priors, decisiveness scores or uncertainty scores** as inputs to the ranking. p and
  u are derived; only regrets are elicited.
- **Fitted weights** before §5.5 has the data to beat the declared table out of sample.

---

## 6. Honesty notes

- **"JEV"** was searched twice and not found as a VOI method (§3.2). The arXiv "Jev" is an unrelated,
  unexpanded system name.
- **The identity "binomial SL opinion = Beta = IDM interval = binary DS mass"** (§1.3) is my
  derivation from the standard definitions. I believe it is correct, but I am not quoting it.
- **All numbers marked "computed here"** come from a short script (the session's scratchpad
  `nums.py`, not committed). It recomputes Zadeh's K and m(T), the discounted combination, the
  subjective-logic fusion example, and the EVPI and EVSI tables. They are arithmetic, not data.
- **Unreachable sources.** onera.fr (the Dezert et al. full text) and cran.r-project.org (the `dst`
  Zadeh vignette) did not resolve from this session's network. Claims depending on them are held at
  `search-snippet`.
- **Most references are `recalled`.** Before any of them is cited as `full-text` in a downstream
  document, it needs fetching. Priorities, by how much weight they carry above: Zadeh 1986, Frazier
  et al. 2008, Mastrandrea et al. 2010, Cox 2008, Seidenfeld and Wasserman 1993.

## 7. References, with read-levels

**Aggregation**

- Dempster AP (1967). Upper and lower probabilities induced by a multivalued mapping. *Ann Math
  Stat* 38:325–339. `recalled`
- Shafer G (1976). *A Mathematical Theory of Evidence*. Princeton UP. `recalled`
- Zadeh LA (1984). Review of Shafer's *A Mathematical Theory of Evidence*. *AI Magazine* 5(3).
  `recalled`
- Zadeh LA (1986). A simple view of the Dempster–Shafer theory of evidence and its implication for
  the rule of combination. *AI Magazine* 7(2):85–90. `recalled`
- Haenni R (2005). Shedding new light on Zadeh's criticism of Dempster's rule of combination. *Proc.
  Int. Conf. Information Fusion* (7th or 8th; secondary sources disagree on the numbering).
  `search-snippet`
- Jøsang A (2001). A logic for uncertain probabilities. *Int J Uncertainty, Fuzziness and
  Knowledge-Based Systems* 9(3):279–311. `recalled`
- Jøsang A (2016). *Subjective Logic: A Formalism for Reasoning Under Uncertainty*. Springer.
  `recalled`
- Dezert J, Tchamova A, Han D, Tacnet J-M (2014). Can we trust subjective logic for information
  fusion? *FUSION 2014*, Salamanca, pp. 1–8. `search-snippet` (full text unreachable)
- Walley P (1991). *Statistical Reasoning with Imprecise Probabilities*. Chapman & Hall. `recalled`
- Walley P (1996). Inferences from multinomial data: learning about a bag of marbles. *JRSS B*
  58(1):3–57. `recalled`
- Levi I (1974). On indeterminate probabilities. *J Philosophy* 71:391–418. `recalled`
- Augustin T, Coolen FPA, de Cooman G, Troffaes MCM (eds) (2014). *Introduction to Imprecise
  Probabilities*. Wiley. `recalled`
- Troffaes MCM (2007). Decision making under uncertainty using imprecise probabilities. *Int J
  Approx Reasoning* 45:17–29. `recalled`
- Seidenfeld T, Wasserman L (1993). Dilation for sets of probabilities. *Ann Stat* 21(3):1139–1154.
  `recalled`
- Berger JO (1994). An overview of robust Bayesian analysis. *Test* 3:5–124. `recalled`
- Dung PM (1995). On the acceptability of arguments and its fundamental role in nonmonotonic
  reasoning, logic programming and n-person games. *Artif Intell* 77(2):321–357. `recalled`
- Caminada M (2006). On the issue of reinstatement in argumentation. *JELIA 2006*, LNCS 4160.
  `recalled`
- Caminada M, Amgoud L (2007). On the evaluation of argumentation formalisms. *Artif Intell*
  171:286–310. `recalled`
- Prakken H (2010). An abstract framework for argumentation with structured arguments. *Argument &
  Computation* 1(2):93–124. `recalled`
- Modgil S, Prakken H (2013). A general account of argumentation with preferences. *Artif Intell*
  195:361–397. `recalled`
- Modgil S, Prakken H (2014). The ASPIC+ framework for structured argumentation: a tutorial.
  *Argument & Computation* 5(1):31–62. `recalled`
- Cayrol C, Lagasquie-Schiex M-C (2005). On the acceptability of arguments in bipolar argumentation
  frameworks. *ECSQARU 2005*. `recalled`
- Oren N, Norman TJ (2008). Semantics for evidence-based argumentation. *COMMA 2008*. `recalled`
- Amgoud L, Ben-Naim J (2013). Ranking-based semantics for argumentation frameworks. *SUM 2013*.
  `recalled`
- Rago A, Toni F, Aurisicchio M, Baroni P (2016). Discontinuity-free decision support with
  quantitative argumentation debates. *KR 2016*. `recalled`
- Baroni P, Rago A, Toni F (2019). From fine-grained properties to broad principles for gradual
  argumentation. *Int J Approx Reasoning* 105:252–286. `recalled`
- Hunter A (2013). A probabilistic approach to modelling uncertain logical arguments. *Int J Approx
  Reasoning* 54:47–81. `recalled`
- Hunter A, Thimm M (2017). Probabilistic reasoning with abstract argumentation frameworks. *JAIR*
  59:565–611. `recalled`

**Evidence hierarchies**

- Guyatt GH et al. (2008). GRADE: an emerging consensus on rating quality of evidence and strength
  of recommendations. *BMJ* 336:924–926. `recalled`
- Balshem H et al. (2011). GRADE guidelines: 3. Rating the quality of evidence. *J Clin Epidemiol*
  64(4):401–406. `recalled`
- Mustafa RA et al. (2013). The GRADE approach is reproducible in assessing the quality of evidence
  of quantitative evidence syntheses. *J Clin Epidemiol* 66(7):736–742. `search-snippet`
- Gartlehner G et al. (2016). The predictive validity of quality of evidence grades for the
  stability of effect estimates was low: a meta-epidemiological study. *J Clin Epidemiol* 70:52–60.
  `search-snippet`
- Kavanagh BP (2009). The GRADE system for rating clinical guidelines. *PLoS Med* 6(9):e1000094.
  `recalled`
- Jüni P, Witschi A, Bloch R, Egger M (1999). The hazards of scoring the quality of clinical trials
  for meta-analysis. *JAMA* 282:1054–1060. `recalled`
- Concato J, Shah N, Horwitz RI (2000). Randomized, controlled trials, observational studies, and
  the hierarchy of research designs. *NEJM* 342:1887–1892. `recalled`
- Mastrandrea MD et al. (2010). *Guidance Note for Lead Authors of the IPCC Fifth Assessment Report
  on Consistent Treatment of Uncertainties*. IPCC. `recalled`
- Budescu DV, Broomell S, Por H-H (2009). Improving communication of uncertainty in the reports of
  the Intergovernmental Panel on Climate Change. *Psychol Sci* 20(3):299–308. `search-snippet`
- Budescu DV, Por H-H, Broomell SB, Smithson M (2014). The interpretation of IPCC probabilistic
  statements around the world. *Nature Climate Change* 4:508–512. `recalled`
- Aven T, Renn O (2015). An evaluation of the treatment of risk and uncertainties in the IPCC
  reports. *Climatic Change*. `recalled`
- Colson AR, Cooke RM (2017). Cross validation for the classical model of structured expert
  judgment. *Reliab Eng Syst Saf* 163:109–120. `search-snippet`
- Cox LA Jr (2008). What's wrong with risk matrices? *Risk Analysis* 28(2):497–512. `recalled`

**Value of information**

- Raiffa H, Schlaifer R (1961). *Applied Statistical Decision Theory*. Harvard. `recalled`
- Claxton K (1999). The irrelevance of inference: a decision-making approach to the stochastic
  evaluation of health care technologies. *J Health Econ* 18:341–364. `recalled`
- Ades AE, Lu G, Claxton K (2004). Expected value of sample information calculations in medical
  decision modeling. *Med Decis Making* 24:207–227. `recalled`
- Rothery C, Strong M, Koffijberg H, et al. (2020). Value of information analytical methods: Report
  2 of the ISPOR Value of Information Analysis Emerging Good Practices Task Force. *Value Health*
  23(3):277–286. PMC7373630. `full-text` (via summariser, first ~100k of ~104k characters)
- Strong M, Oakley JE, Brennan A (2014). Estimating multiparameter partial expected value of perfect
  information from a probabilistic sensitivity analysis sample: a nonparametric regression approach.
  *Med Decis Making* 34(3):311–326. `search-snippet`
- Heath A, Manolopoulou I, Baio G (2016). Estimating the expected value of partial perfect
  information in health economic evaluations using integrated nested Laplace approximation. *Stat
  Med* 35:4264–4280. `recalled`
- Heath A, Manolopoulou I, Baio G (2018). Efficient Monte Carlo estimation of the expected value of
  sample information using moment matching. *Med Decis Making* 38:163–173. `search-snippet`
  (preprint arXiv:1611.01373)
- Jalal H, Alarid-Escudero F (2018). A Gaussian approximation approach for value of information
  analysis. *Med Decis Making* 38:174–188. `search-snippet`
- Li, Jalal, Heath (2024). Estimating the EVSI with Gaussian approximations and spline-based series
  methods. *Med Decis Making* 44(7):787–801. `search-snippet`
- Kunst N, Wilson ECF, Glynn D, et al. (2020). Computing the expected value of sample information
  efficiently: practical guidance and recommendations for four model-based methods. *Value Health*
  23(6). `search-snippet`
- Glynn D et al. (2024). Rapid assessment of the need for evidence: applying the principles of value
  of information to research prioritisation. *PharmacoEconomics* 42(9). `search-snippet`
- Deng B, Fan S, Zhang H, Xie X (2026). Jev for scientific decisions: evaluating semantic choices
  and their consequences. arXiv:2609.24965. `abstract-only` (cited only to show it is not a VOI
  method)

**Sequential allocation**

- Gittins JC (1979). Bandit processes and dynamic allocation indices. *JRSS B* 41(2):148–177.
  `recalled`
- Berry DA, Fristedt B (1985). *Bandit Problems: Sequential Allocation of Experiments*. Chapman &
  Hall. `recalled`
- Frazier PI, Powell WB, Dayanik S (2008). A knowledge-gradient policy for sequential information
  collection. *SIAM J Control Optim* 47(5):2410–2439. `recalled`
- Frazier PI, Powell WB, Dayanik S (2009). The knowledge-gradient policy for correlated normal
  beliefs. *INFORMS J Comput* 21(4):599–613. `recalled`
- Frazier PI, Powell WB (2010). Paradoxes in learning and the marginal value of information.
  *Decision Analysis* 7(4):378–403. `recalled`
- Ryzhov IO, Powell WB, Frazier PI (2012). The knowledge gradient algorithm for a general class of
  online learning problems. *Oper Res* 60(1):180–195. `recalled`
- Radner R, Stiglitz JE (1984). A nonconcavity in the value of information. In Boyer and Kihlstrom
  (eds), *Bayesian Models in Economic Theory*. `recalled`
- Tran-Thanh L, Chapman A, Munoz de Cote E, Rogers A, Jennings NR (2010). Epsilon-first policies for
  budget-limited multi-armed bandits. *AAAI 2010*. `recalled`
- Tran-Thanh L, Chapman A, Rogers A, Jennings NR (2012). Knapsack based optimal policies for
  budget-limited multi-armed bandits. *AAAI 2012*. `recalled`
- Badanidiyuru A, Kleinberg R, Slivkins A (2013). Bandits with knapsacks. *FOCS 2013* (JACM 2018).
  `recalled`
- Joulani P, György A, Szepesvári C (2013). Online learning under delayed feedback. *ICML 2013*.
  `recalled`
- Audibert J-Y, Bubeck S, Munos R (2010). Best arm identification in multi-armed bandits. *COLT
  2010*. `recalled`
- Russo D (2020). Simple Bayesian algorithms for best-arm identification. *Oper Res* 68(6).
  `recalled`
- Chow YS, Robbins H, Siegmund D (1971). *Great Expectations: The Theory of Optimal Stopping*.
  Houghton Mifflin. `recalled`
- Ginsbourger D, Le Riche R, Carraro L (2010). Kriging is well-suited to parallelize optimization.
  In *Computational Intelligence in Expensive Optimization Problems*, Springer. `recalled`
