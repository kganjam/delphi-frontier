# Insect flight design space — working notes

For whoever writes the prose. This is what I did, what I could not do, every source
disagreement I found, and the things I think are easiest to get wrong writing this page up.

Written by the agent that finished the page. The first third — `hox-identity.json`,
`code/hox_identity.py`, its two figures, and the PMID verification scaffolding — was built by an
earlier agent; I verified it (see §6) and kept it.

---

## 1. What is here

| file | what it is |
|---|---|
| `routes.json` | 43 routes over 9 scales. Built by `code/build_routes.py`, not hand-written. |
| `hox-identity.json` | Study 1. Hox dose and the wing/haltere decision. Inherited; verified; annotated. |
| `venation.json` | Study 2. Venation as a reaction-diffusion problem. |
| `flight-performance.json` | Study 3. Lift, power, control authority, and attitude control with and without halteres. |
| `index-fragment.json` | The three studies with authored alt text and captions for every figure. |
| `data/pmid_verified.json` | 92 PMIDs resolved against NCBI esummary this session. One is a deliberate MISSING control. |
| `data/pmid_abstracts.json` | 91 abstracts, fetched so that read levels could be set honestly rather than guessed. |
| `data/paul2021-PMC8129201-fulltext.xml` | Full text of Paul et al. 2021, fetched to check study 1's four numbers. sha256 `4e12dc00acaf5c3d21f2e8690ec56f53646cc3a80b87c656c45dfc56b59c6d92`. |
| `data/deora2021-PMC8629423-fulltext.xml` | Full text of Deora et al. 2021. sha256 `6e88c4060414dd0cc8a608ba2e481fb03301e5bcd2f4411b9330debd65004643`. |
| `data/pmc_abstracts.json` | PMC abstract versions for four PMIDs. These are **not** the same text PubMed holds — see §5. |
| `code/check_quotes.py` | Checks every quoted fragment in `routes.json` against the stored sources. Exits non-zero on a mismatch; ships both controls. |
| `code/annotate_hox.py` | Re-applies the post-hoc verification block to `hox-identity.json`, which `hox_identity.py` rewrites on every run. |

Every figure is a simulation and every caption opens by saying so. Nothing on this page was
measured on an animal by us.

---

## 2. The story the page should tell, and the sentence it must not write

**The design intuition is wrong in the dipteran case for two independent reasons, and the
literature separates them cleanly.** This is the part worth leading with, because almost everyone
who asks "would four wings fly better" has only met the first half of the phenotype:

1. **The second pair of wings has almost no engine.** Fernandes et al. 1994 (PMID 7874495):
   in *abx bx3 pbx* flies "the adults have two pairs of wings, but the homeotically transformed T3
   (HT3) has only rudimentary indirect flight muscles". Roy et al. 1997 (PMID 9094307) give the
   cause: *Antp* keeps being expressed in the mesoderm of the transformed segment. The homeotic
   lesion transforms the **epidermis** and leaves the **motor** behind.
2. **And the rate gyros are gone with the halteres — but this half is weaker, and the page must
   say so.** It is tempting to pair the muscle finding with the flat sentence "haltere input is
   necessary for free flight". **Do not.** That sentence is an opening PREMISE in the papers that
   carry it — in Mureli & Fox 2015 it explains why their experiments are tethered, and in Lea et
   al. 2026 it introduces work on standing posture — and we found no free-flight ablation
   measurement behind it. What IS measured is narrower and graded: ablation abolishes the
   equilibrium reflexes in a tethered arena (Dickinson 1999); haltere-mediated feedback sets
   body-saccade amplitude on a magnetic tether while visual feedback does not (Bender &
   Dickinson 2006); haltereless flies cannot stabilise a WIDE-FIELD stimulus but fixate FIGURES
   with normal acuity and can still flap and steer (Mureli & Fox 2015); takeoff velocity and
   stability fall in Calyptratae and **not** in other flies (Yarger 2021).

**The asymmetry is itself worth a sentence.** The missing flight muscle is direct, quoted and
unambiguous. The sensory cost is real but graded, task-dependent and clade-dependent. A page that
says which of its two reasons is better evidenced is more convincing than one asserting two flat
failures — and `routes.json.not_claimed` carries the scope of the negative, including the
searches run and their positive control.

**The sentence the page must not write is "four wings are worse than two."** That is false as a
general claim and the comparative scale refuses it:

- Dragonflies and damselflies "have maintained their distinctive, independently controllable,
  four-winged form for over 300Myr", and fore-hind phasing "can improve aerodynamic efficiency by
  removing swirl" (Usherwood & Lehmann 2008, PMID 18477538).
- Jantzen & Eisner 2008 (PMID 18936482) cut the hindwings off moths and butterflies — "reducing
  their total wing surface, on average, by nearly one half" — and **they still flew**. What they
  lost was linear and turning acceleration, i.e. evasiveness. Turning *radius* was unaffected.

So the second pair buys **agility**, not lift, and the dipteran case is special because in flies
the hindwing has already been spent on something else. That framing is in `routes.json` under
`recommendation.the_answer_to_the_judges_question`.

---

## 3. The one route nobody seems to have tried

`act-restore-t3-flight-muscle`. Transform the T3 **mesoderm** as well as the epidermis, so the
extra wings have an engine. It is the only route on the page marked `proposed`, and both halves
are already published separately:

- T2 mesoderm is the one thoracic mesoderm that expresses **no** known Antp- or
  bithorax-complex selector; its muscle identity is specified entirely by induction from the
  ectoderm.
- "specific ectopic expression of Antp and other homeotic selector genes in the mesoderm of the
  second thoracic segment respecified its muscle pattern" — so the mesodermal switch is known to
  be sufficient *in the other direction*.
- Antp persists in transformed-T3 mesoderm, which Roy et al. call "a likely reason for the
  failure of flight muscle development in the transformed segment".

Both quotes are from PMID 9094307, read at abstract level. **I did not find a report of anyone
running the combination.** That is a statement about a PubMed search, not a survey of the field;
please keep that qualifier if you use the claim.

---

## 4. Source disagreements — preserve all four, do not reconcile

1. **How necessary are halteres, and to whom?** This is the one I got wrong first, so it is
   worth stating carefully. The flat claim appears in the literature as a PREMISE rather than a
   result — see §2 — so the live question is not "premise versus finding" but how the actual
   measurements vary. Yarger et al. 2021 (PMID 33434467) found haltere removal "decreased both
   velocity and stability in the takeoffs of Calyptratae, **but not other flies**", including "a
   closely related non-Calyptratae species" with an equally rapid takeoff. Hall et al. 2015
   (PMID 26601682) add that haltere kinematics themselves vary with phylogeny. Mureli & Fox 2015
   found the cost is task-specific — wide-field stabilisation yes, figure tracking no. So the
   measured picture is **graded along two axes at once, behaviour and clade**, and the page
   should present it that way. Route `comp-haltere-use-is-clade-dependent` carries it.
2. **Does fore-hind wing interaction help or hurt?** Usherwood & Lehmann say previous studies
   "have generally painted a rather disappointing picture" of interactions, and then show phasing
   can *improve* efficiency. Study 3 does not pick a side: it sweeps the interference term from
   −0.10 (beneficial) to +0.40 and reports the whole range. Please present it as a swept
   parameter, not as a value.
3. **Is the strepsipteran haltere homologous to the dipteran one?** Rokas et al. 1999
   (PMID 10620047) lay out both options explicitly — affiliation to Coleoptera "implies that
   dipteran halteres and strep-sipteran haltere-like organs evolved convergently", while a
   Diptera sister-group relationship would make them homologous with "a radical homeotic
   mutation" having switched their position. That paper's own evidence "does not indicate
   affinity with Diptera". Minelli 2009 (PMID 19558647) revisits it. **The page keeps this open.**
   If it is resolved somewhere I did not find it.
4. **The haltere is not only a gyroscope.** Dickerson et al. 2019 (PMID 31607538) argue it also
   functions "as an adjustable clock to set the spike timing of wing motor neurons". This
   *weakens the simple story the page starts from*, and study 3's limitations say so: modelling
   the haltere as a rate-feedback term **understates** what deleting one costs.

---

## 5. Read levels, and the negative control

`routes.json` carries 97 evidence rows: **4 full-text, 68 abstract, 25 listing.**

- A row marked `listing` has its `finding` replaced by an explicit NOT-READ note. The PubMed
  record resolves and the citation is right; I have read none of the paper's results. **Do not
  paraphrase a `listing` row as if it reported something.**
- Every `cite` string in `routes.json` is **assembled** by `code/build_routes.py` from
  `data/pmid_verified.json`, which holds what NCBI esummary returned. No citation was typed by
  hand, and an unverified PMID aborts the build.
- The verification run includes **PMID 99999999**, which resolves to MISSING as it must. A
  verifier that returns a record for everything is indistinguishable from one that is not running.
- **One cited source is a preprint** and its row says so: Teoh et al. 2025 on the tp1 steering
  muscle is a bioRxiv record, not peer reviewed.

### Every quoted fragment was checked against the stored source

`code/check_quotes.py` takes every single-quoted run of ≥12 characters inside an evidence row's
`finding` and requires it to appear **verbatim** in that PMID's stored title, abstract or full
text. It ships both controls, because a checker that passes everything looks exactly like a
checker that is not running: a sentence no paper contains must not be found, and a sentence
taken verbatim from a stored abstract must be. **It currently reports `checked 128 quoted
fragments … 0 fragments NOT found verbatim … PASS`, and it found six real errors getting there:**

- **A misattributed quote.** "halteres lack stout sensory bristles of the wing margin and veins"
  was attributed to Weatherbee et al. 1998. It is Pallavi & Shashidhara's (PMID 16815386). The
  row now carries the Weatherbee sentence that *is* in that abstract, and says in the row that
  the other quote belongs elsewhere.
- **Two spliced parentheses.** Both Paul et al. quotes closed a bracket the paper leaves open —
  the source reads "(2.5 times lower than endogenous Ubx, Fig. 7b-b′)". The parenthetical is now
  outside the quote marks.
- **A tense change inside quote marks** — "ha[d] yet to be directly demonstrated" for a source
  that says "has".
- **A unit written differently from the source** — "2 deg" for a source that says "2 degrees".

Run it after any edit to a `finding`: `python3 code/check_quotes.py` (exit 0 = pass).

**And a thing worth knowing: PubMed and PMC do not always hold the same abstract.** For Ristroph
et al. 2010 the PubMed record stops short of the sentence this whole page's control criterion
rests on — "recover their heading to within 2 degrees in < 60 ms" — which the PMC version
carries. The PubMed version ends at "…reacts to short time-scale disturbances." Both are stored
and both are searched. **If you quote Ristroph's 60 ms figure, it comes from the PMC abstract**
(`data/pmc_abstracts.json`), not from the PubMed record, and that distinction is the kind of
thing a reviewer checks.

### What I could not read, and how I know the absence is real

The Journal of Experimental Biology returns a Cloudflare bot challenge (I tried `r.jina.ai` as
well). Europe PMC's REST full-text endpoint returned HTTP 500 for **Fry et al. 2005, Ristroph et
al. 2010, Dickerson et al. 2019 and Yarger et al. 2021**. I did not report that as a finding
without a positive control: the same endpoint returned **164 kB** of full text for Deora et al.
2021 (PMC8629423), and 111 kB for Paul et al. 2021 (PMC8129201). So the endpoint works and those
four absences are real. That is why study 3's morphology and kinematics are `assumed`.

---

## 6. What I checked about the inherited study, and the one correction

Study 1 depends on four numbers attributed to Paul et al. 2021. **None of them is in that paper's
abstract**, so there was no way to take them on trust. The full text is open access; I fetched it
and **all four are confirmed verbatim**:

| claim in study 1 | the paper's own words |
|---|---|
| wing traits at 39% of endogenous Ubx | "wing-like phenotypic traits ... eventually appeared when the level decreased to 39% of endogenous Ubx" |
| haltere-like wing at 490% of endogenous Antp | "the wing resembled a haltere ... when the expression level corresponded to 490% of endogenous Antp" |
| Ubx:Antp = 18.5× by antibody | "Ubx was 18.5 times more strongly expressed than Antp" |
| Ubx:Antp = 10.5× by GFP | "Ubx expression levels were 10.5 times higher than Antp levels" |

**But study 1's framing of the 18.5× / 10.5× split is too pessimistic, and this is the one thing
in the inherited work I would change.** It calls them a disagreement that "propagates directly"
into the prediction. True arithmetically — but Paul et al. do **not** leave them in conflict.
They attribute the gap to antibody affinity and conclude "the Antp antibody is 1.85 times less
affine", which makes the **GFP-based 10.5× their own preferred measurement**. The GFP arm is also
the arm whose held-out prediction lands within 4%. So the model comparison and the paper's own
reasoning select the same number independently. **That is a stronger result than study 1
claimed, and the page should say so.**

There is also **independent observational support for the graded variant that the model never
used**: the paper reports, of both series, that "In both cases, intermediate levels led to
intermediary phenotypes". Intermediate organs at intermediate doses is what the graded variant
predicts and what the bistable one forbids.

I put both in an additive `post_hoc_verification` block in `hox-identity.json` and **changed no
number, control or conclusion** of the original study.

### The inherited result was stale, and re-running it changed the story

**This is the single most important thing in these notes.** I edited one line of
`code/hox_identity.py` — a figure axis limit — re-ran it, and diffed the output against the
`hox-identity.json` I had been handed. **70 of 428 leaves changed.** The code had been revised
and never re-run, so the emitted result described a superseded model. Specifically:

| | inherited (stale) | after re-running the code beside it |
|---|---|---|
| `controls.all_variants_pass` | `false` | `true` |
| bistable held-out prediction (GFP ratio) | 200 — i.e. it never crossed | **6.82** against a measured 4.90 |
| bistable relative error | 40× | **39.2%** |
| graded relative error | 4.0% | 4.0% (unchanged) |
| `hysteresis_test_model_independent` | absent | a whole new section |
| variant descriptions | "strong/weak self-activation" | rewritten, with the bistable parameters explicitly chosen to make it a fair opponent |

**The refreshed result is both correct and better.** The bistable variant now passes the same
controls the graded one does, with wild-type T2 and T3 sitting *outside* its bistable window, so
the comparison is a fair test rather than a strawman. The discrimination is 4.0% against 39.2%
rather than 4% against a factor of 40 — **smaller, and far more credible**.

**So do not write the "factor of 40" line.** It was in the file I inherited and it is wrong.

**And the strongest result in that study needs no model at all**, which I think is what the page
should lead the section with: the two published thresholds sit on *opposite branches* of the
switch, so their **ordering** tests hysteresis directly. A hysteretic switch requires the
haltere→wing transition to sit at a strictly *lower* Hox dose than the wing→haltere one. Under
both protein-ratio measurements the ordering is the one hysteresis forbids, and under the GFP
ratio the two doses are within 4% of each other — effectively a single threshold. That is the
earlier agent's own addition and it is better than the model comparison it sits next to.

I also fixed one figure defect in `code/hox_identity.py`: the control figure's y-axis was pinned
to (−0.03, 1.05) while the stale model's bistable wing branch settled at **1.61**, so that curve
ran off the top of the panel and the panel read as a missing curve rather than a high one. The
axis now follows the data. No model code was touched.

**`hox_identity.py` rewrites `hox-identity.json` from scratch on every run**, which would drop
the verification block. `code/annotate_hox.py` re-applies it — run it after any re-run.

---

## 7. Study 2 (venation): read the controls before the result

**Two of its four controls fail, and both failures are reported rather than repaired.**

- **C1 (positive control on the counter) passes** — 5 painted stripes count as 5, 9 as 9 — but it
  **failed on its first run**, counting 6 and 10. The fault was in the control's own *stimulus*,
  not in the counter: the painted field put a peak on both edges of the blade as well as in the
  interior, so it genuinely had n+1 stripes. I corrected the stimulus and left the counter
  untouched. The JSON records which side I changed, because a positive control debugged until it
  passes is worth nothing unless you say that.
- **C2 (negative control) passes**: with lateral inhibition removed the Turing condition fails and
  the field goes uniform.
- **C3 passes well**: the measured dominant wavelength matches the linear-stability prediction to
  **0.1%**.
- **C4 (pointwise steady state) FAILS** at the threshold declared in the docstring, and **C4b**,
  which I added afterwards to ask whether the *readout* had converged anyway, **also fails** —
  at least one seed's vein count still changes in the second half of the run. I did not lengthen
  the runs until it passed. Running 4× longer moved the residual only from 7.6e-3 to 3.8e-3.

**So part of the seed spread quoted in study 2 is convergence, not pattern formation.** Say that
if you quote a ± from it.

**The result itself.** The model gets the **spacing** right and the **count** wrong by one, every
time: across a 2.4-fold range of blade width the counted number falls short of the linear-theory
prediction by a near-constant ~1 vein, which is what two boundaries each suppressing half a
wavelength looks like. A constant offset rather than a proportional one is the tell.

**Two things not to overclaim.** First, the stripe *orientation* is imposed by anisotropic
diffusion — without it the same kinetics make labyrinths. In a real wing the orientation comes
from Hedgehog and Dpp positional information laid down *before* lateral inhibition refines
anything (Crozatier et al. 2003, PMID 12782270). This is the study's largest liberty and a
reviewer will go for it first. Second, in the three right-hand panels of `venation-series.png`
the pattern has **broken up**; the small counts there mean "no stripes" and not "fewer veins",
and the counting rule is out of its domain. The caption says this; please keep it.

---

## 8. Study 3 (flight performance): three traps

1. **The intact model recovers in 13 ms where a real fly takes under 60 ms.** The model is
   *faster* than the animal — optimistic about control — so it **understates** the cost of
   deleting halteres. Say this. A reader will otherwise assume the model was tuned to flatter the
   conclusion.
2. **Do not write an inertia story.** The four-wing bodies' recovery curves sit within 1% of the
   two-wing ones, because added wing inertia is negligible at a 0.5% wing-mass fraction. The
   four-winged fly's control problem is the **deleted sensor**, not the added rotational inertia.
   This is a genuine null and the page is better for stating it.
3. **18 of 24 parameters are `assumed`** and the JSON prints the counts. Every part-A result is a
   **ratio** to the two-wing arm precisely so the absolute scale cancels. Don't quote an absolute
   force or power from it.

**The number I would lead the section with.** Sweeping the feedback delay and giving **every**
delay the best gain in the declared family, the boundary is **3.0 wingbeats, about 14 ms** — a
loop slower than that cannot meet the measured 60 ms recovery **at any gain**. The haltere loop
(1 wingbeat, ~4.5 ms) is inside it; the visual loop (~30 ms) is well outside. That is the honest
version of "the haltere is a rate gyro": it is not that vision is weaker, it is that vision is
too slow to be turned up.

**Two failures kept in the record** (`controls.note` and the `BANDWIDTH_RULE_FAMILY` parameter):

- The first attitude model used haltere **rate** feedback alone. It damped the rotation and then
  parked the body 4.5° off heading for ever — correct for a rate loop, wrong for an animal that
  Ristroph et al. say "accurately return[s] to their original orientation". The controller became
  a delayed PD loop.
- The second declared a single gain rule (natural period = 4 × delay). That is marginally stable
  by construction — it puts ω_nτ at π/2 — and every arm chattered at ~2° for ever. Rather than
  pick a third number after seeing a failure, **the gain rule became a swept family** and each
  arm is given the member that minimises *its own* recovery time. That is deliberately generous
  to the arms without halteres, which is the point.

Study 2 has a parallel one: its first integration ran at a step **250× above** the explicit
scheme's stability limit and did not visibly blow up, because the code clipped the fields. It
produced a plausible-looking pattern from an unstable integration, and the steady-state control
is what caught it.

---

## 9. Things I did not do

- **No free-flight measurement of a four-winged fly exists in what I found.** This is the most
  important gap on the page. Every quantitative flight claim about four-winged *Drosophila* is an
  inference from the muscle phenotype plus haltere ablation in otherwise normal flies, plus our
  model. It is stated first in `routes.json.limitations` and should not be buried.
- **No Nebius job was submitted.** Nothing here needed a GPU: the two new studies are small
  numpy, and the venation study runs 160 simulations on 4 cores in about 9 minutes under a
  `systemd-run` scope. Submitting an H100 job to run them would have been theatre. If you want
  the venation sweep at higher resolution or more seeds, that is the one piece that would
  genuinely use the 16 vCPU preset.
- **I did not chase the non-PubMed literature.** No bioRxiv sweep beyond what PubMed indexes, no
  engineering-conference literature on flapping MAVs, no Google Scholar. The comparative
  aerodynamics of four-winged flappers almost certainly has more in the engineering literature
  than the three papers cited here.
- **No welfare framework for insects.** §`welfare` in `routes.json` says plainly that insects
  fall outside EU Directive 2010/63/EU and that this is a statement about the law, not an
  argument that the procedures are ethically free. I am not qualified to supply the framework and
  did not pretend to.
- **I did re-run study 1's model in the end**, and had to — see §6. I changed no model code; the
  only edit was a figure axis limit. Its controls now all pass, which the inherited file said
  they did not.

---

## 10. Small things that will bite

- `data/pmid_verified.json` has **92** entries, one of which is `null` (the 99999999 control).
  Anything iterating it must handle the null — `code/verify_pmids.py` does, and so does
  `build_routes.py`, which refuses to cite it.
- The route→scale assignment is editorial. Several routes act at more than one scale (the
  Ubx–dally–Dpp route is simultaneously cis-regulatory and a network perturbation) and are filed
  where a reader will look, not where they are most defensible. `routes.json.limitations` says so.
- **Every route carries a precomputed `outcome` field. Use it; do not re-run the regexes.**
  `outcome_classes` is still there because the schema asks for it, but the matching is fragile in
  a way worth recording. The first version matched each class against the route's **title and
  `predicted_phenotype`**, and got **six routes backwards**, because a title names the STARTING
  condition — "Drive the vestigial quadrant enhancer in a segment that has **no wing**" tagged as
  *fewer-wings* when the outcome is ectopic wing tissue — and because a later sentence in the body
  ("a fly with four halteres and **no wings**") outranked the leading phrase. The fix was to match
  `predicted_phenotype` **only**, **anchored at the start**, where each route leads with its
  outcome in capitals. All 43 are now tagged and every assignment was read by hand. This is the
  repo's own "a forbidden-string check cannot tell claiming from quoting" trap, in a new costume.
- Five routes carry a `study` key linking them to one of the three studies
  (`hox-identity`, `venation`, `flight-performance`). More than five routes are *relevant* to a
  study; the key is set only where the study genuinely bears on that route's prediction.
- Six verified PMIDs are cited by no route: `12702878`, `15939772`, `19359586`, `26347566`,
  `27413092`, `9744867`. The first three are used by study 3's parameter sources rather than by a
  route, which is intentional. The last three are leftovers from the earlier agent's candidate
  list and are simply unused.
