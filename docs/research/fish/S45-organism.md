# S45 (organism scale) — refute-from-below sweep: does any high-scale claim have an entailed low-scale requirement that a published measurement already contradicts?

Project: `zebrafish-flight`. Date of this pass: 2026-11-04. Author: this agent.
Reproduce the arithmetic with `python3 -I docs/research/fish/S45_sweep_calc.py`.

**Headline: NO — the sweep found none.** This is a real negative and it is the deliverable. It is
stated in full in §4, with the sweep's scope in §2.1 and the seven candidates that failed, each with
its stated ground of failure, in §4.2. The one candidate I pursued to primary full text myself died
on my own arithmetic (§3.2).

---

## 1. The question, restated precisely

The cross-scale architecture asserts that its most valuable outcome is a **refutation from below**:
a claim made at a high scale (ecology, organism, organ) whose *entailed* requirement at a lower
scale (tissue, protein, DNA) is contradicted by a measurement that is already in the published
literature. Not a disagreement, not an unmeasured gap, not a reasoning error — a published number on
one side and an entailment on the other, pointing opposite ways.

The numbers that make this hard in this project:

| quantity | value | why it makes the search hard |
|---|---|---|
| claims in the project | 237 distinct `claim_id`s recorded in challenge blocks; 290+ by the project's own count | the sweep has to be stated as a scope, not implied |
| adversarial reviews already written | 232 distinct challenges (289 `swarm-challenge` blocks) | the easy contradictions are already consumed |
| recorded challenge outcomes | 212 `weakened`, 60 `survived`, **14 `refuted`** (in 10 distinct documents) | refutation is already the rare outcome, at ~5% |
| project conclusions that are negatives | the large majority (S1, S3, S6, S7, S9, S10, S13, S16, S18, S20, S21, S23, S24, S26, S28, S29, S30) | **this is the structural problem — see §3.3** |
| the animal | *Danio rerio*, 4 cm, ~0.4 g | nearly every decisive low-scale measurement exists only in another species |

The structural difficulty, stated once here because it governs the whole result: a high-scale claim
in this project is usually of the form *"X cannot be done, because the low-scale capability ceiling
is C."* Its entailment is an **upper bound**. A published measurement that comes in *above* C does
not refute the high-scale negative by arithmetic alone — it removes the stated reason for it. So the
target outcome is reachable here almost only through the narrow door of a negative that rests on an
explicitly stated low-scale ceiling. §4.2 candidate 2 is that door, and §4.2 says why it does not
open.

---

## 2. What is measured

### 2.1 Scope of the sweep (stated beside the negative, as required)

- **Corpus.** 760 remote branches of `kganjam/delphi-frontier` enumerated; every `*.md` under
  `docs/research/fish/` on every branch harvested — **862 files, 420 distinct documents**: 70
  S-scale documents (S1–S32 and their `-D`/`-D-D` deepen chains), 232 challenge reviews, 112
  replications, plus protein and physics notes. 100 `swarm-result` blocks and 289
  `swarm-challenge` blocks were parsed.
- **Method.** Every `swarm-result` answer, `key_number` and `verdict`, and every challenge
  `outcome`/`reason`/`corrected_value`, was read. I then went to the negative verdicts to classify
  *what* did the refuting — a published measurement, a reasoning error, an access failure, or a
  competing prediction. Precisely: 14 `"outcome": "refuted"` blocks, falling in **10 distinct
  challenge documents**, and **8** further challenge documents whose headline verdict reads
  `FALLS`/`falls`/`NEGATIVE`, were read **in full text**; the **13** S-scale documents carrying
  `"verdict": "falls"` (S2-D, S6, S6-D, S7-D, S9, S11, S14, S18, S22-D-D, S24, S25, S26, S30) were
  read at `swarm-result` level, and six of them — S6, S9, S14, S18, S25, S26 — in full text. The
  remaining seven were not read in full, which is a gap in this sweep.
- **Not covered, and this bounds the negative.** (a) The project's live claim server,
  `https://frontier.morphoswarm.ai/mcp`, is **could-not-access** from this session — the egress
  proxy answered `403` to `CONNECT` for `frontier.morphoswarm.ai:443`. So claims that exist only in
  that registry and were never written into a branch document were **not** swept. The project's own
  count ("290-plus") exceeds the 237 `claim_id`s I could see, so a residue of roughly 50 claims is
  outside this sweep. (b) I re-read exactly **one** primary source to full text myself (§2.2);
  every other measurement below is at read-level *via project document*, i.e. I am relying on
  another agent's read, and I say so at each use. (c) I ran no new literature search for
  measurements the project has never cited.

### 2.2 The one source I read myself, at full text

**Alben S, Madden PGA, Lauder GV (2007). "The mechanics of active fin-shape control in ray-finned
fishes." *J R Soc Interface* 4(13):243–256. doi:10.1098/rsif.2006.0181, PMC2359861.**
Read-level: **full-text** (PMC HTML, HTTP 200, 213,488 bytes, retrieved 2026-11-04 by me; text
extracted and quoted below). Species: bluegill sunfish *Lepomis macrochirus*.

Quotations — these are the authors' statements, not mine:

- §2: "Six fishes with fins of similar size (maximum ray length =40.3±0.8 mm, mean±s.e.) were
  euthanized."
- Fig. 7a caption: "The ray is clamped horizontally at the base, and a vertical point force is
  applied at two-thirds of the distance from the ray base to the tip … the force–displacement curve
  may be fit with a slope of 1.98 N m⁻¹, about 12 times the value when one hemitrich is free."
- §5.2: "a probe pushes down on the fin ray at approximately two-thirds of the distance from the
  base to the tip, and the force on the probe is measured as a function of **tip deflection** of the
  ray."
- §3.3: "In our experiment, we have found using three-point bending tests that the 'composite'
  Young's modulus corresponding to the whole structure is E ≈ 10⁸–10⁹ N m⁻², with the average area
  moment of inertia I ≈ 10⁻⁶ cm⁴. Hence, **the measured B = EI ≈ 10⁻⁶–10⁻⁵ J m**." (J·m = N·m².)

The §3.3 sentence is a **direct bending measurement of fin-ray flexural rigidity**, and it is the
measurement I took to be my best candidate refuter. It is cited in the project (S25-D, S26-D,
challenge-135, challenge-219, challenge-267, replicate-159, replicate-249 all quote it), so it is
not a new find; what I add is that I verified it against the publisher's text rather than a
summariser.

### 2.3 The measured values the candidate claims turn on, with disagreement preserved

| # | value | source, year | read-level | note |
|---|---|---|---|---|
| M1 | fin-ray EI = **1×10⁻⁶ to 1×10⁻⁵ N·m²**, three-point bending, bluegill pectoral ray, L = 40.3 ± 0.8 mm | Alben, Madden & Lauder 2007 §3.3 | **full-text, read by me** | a measurement |
| M2 | cantilever slope **1.98 N m⁻¹**, both hemitrich bases clamped, load at ~2/3 L, force vs **tip** deflection; ~**12×** the one-base-free slope | Alben et al. 2007 Fig. 7a, §5.2 | **full-text, read by me** | a measurement; it is a *transfer* stiffness, not a load-point stiffness |
| M3 | fin-ray EI = **565×10⁻⁶ N·m²** | Flammang et al. 2013, abstract | **via project document** (S25-organ records abstract-level; the authors themselves call it "calculated"; body text could-not-access for every project agent who tried) | **disagrees with M1 by 56–565×** |
| M4 | fin-ray EI = **3.8×10⁻⁶ N·m²**, attributed to Flammang 2013 as relayed by Puri 2018 | via Puri et al. 2018 | **via project document** (S25-organ: not in the Flammang abstract, "could not be traced to any source") | **disagrees with M3 by ~150×**; provenance unresolved |
| M5 | adult zebrafish whole caudal fin EI = **1.5–4×10⁻⁹ N·m²**, in vivo | Puri et al. 2018 | **via project document** (S9-D records full-text) | the one *Danio* fin-stiffness measurement in the project |
| M6 | zebrafish caudal-fin hemiray tissue reduced modulus **4.57–8.68 GPa**, nanoindentation | Bohns et al. 2020, JBMR Plus, PMC7872341 | **via project document** (S13-D records full-text; n = one fin per group, SD 57–100%) | — |
| M7 | toadfish (*Opsanus tau*) horizontal-canal afferents tested **0.001–10 Hz**; hair-cell microphonic **0.1–20 Hz**, "relatively flat" | Boyle & Highstein 1990; Rabbitt et al. 2004/05 | **via project document** (S18-D records abstract + two fetch-summarised full texts) | cross-species; no corner frequencies given |
| M8 | highest frequency at which any *zebrafish* vestibular reflex has been tested: **0.5 Hz** (larval/early-juvenile) | Sun et al. 2018; Burkhardt et al. 2026 | **via project document** (S18 records full-text via summariser) | S18's own doc states this is a **test-protocol ceiling**, and that no adult canal frequency response was found |
| M9 | within-wild-type SD of per-oocyte resting membrane potential **σ_V = 14.5 mV** | Perathoner et al. 2014, PLoS Genet, Fig. 5D | **via project document** (S14-D-D; digitised by that agent, n = 5 recovered) | *Xenopus* oocyte heterologous expression, not zebrafish fin fibroblast |
| M10 | only RefSeq protein for `slc43a2a` (GeneID 393221) is NP_956545.1, **153 aa** | NCBI RefSeq, accessed 2026-11-04 | **via project document** (challenges 82/90 record primary-record reads) | a database annotation, not a measurement; flagged provisional/frameshift-truncated |

**Disagreements I am not averaging away:** M1 vs M3 vs M4 are three values for "teleost fin-ray EI"
spanning 1×10⁻⁶ to 5.65×10⁻⁴ N·m², a factor of 565. M3's provenance is an abstract whose authors
call the number "calculated"; M4's provenance could not be traced by any project agent; M1 is the
only one of the three that the sweep could confirm as a direct bending measurement at full text.
They are not reconcilable from what is readable, and §3.2 shows the Alben cantilever measurement
cannot adjudicate between them.

---

## 3. What I computed

All of §3 is **computation by me**, in `docs/research/fish/S45_sweep_calc.py`. None of it is an
observation.

### 3.1 Inverting the measured cantilever slope (computation)

Euler–Bernoulli cantilever, point load P at s = a = 2L/3, L = 0.0403 m, k = 1.98 N m⁻¹ (M2):

- load-point convention, EI = k·a³/3 = **1.28×10⁻⁵ N·m²**
- tip-deflection convention (which is what Alben §5.2 states), EI = k·a²(3L−a)/6 = **2.24×10⁻⁵ N·m²**
- one-base-free, applying the paper's own 12× ratio: **1.07×10⁻⁶ to 1.87×10⁻⁶ N·m²**

The second line exceeds the top of the paper's own measured range M1 by 2.24×, which is consistent
with the authors' account that base locking adds shear-coupling stiffness the bending measurement
does not see. **Assumption, and it is load-bearing:** uniform EI and pure bending. The paper places
the real ray at non-dimensional shear modulus G ≈ 10², where it says shear, not bending, sets the
response — so these inversions are *apparent* stiffnesses, not bending rigidities.

### 3.2 The test that killed my best candidate (computation)

My candidate was: *the passive-ray feasibility branch of S6/S6-D survives only on M3
(565×10⁻⁶ N·m²), and M3 is contradicted by M1, a direct bending measurement of the same structure
that is 56–565× lower.* Ratios: M3/M1 = **56.5× to 565×**; M3 / my apparent locked EI = **25.2×**.

To test whether M3 can be rescued, I integrated the cantilever with a **stepped** EI — a stiff
unsegmented proximal section at 565×10⁻⁶ N·m² and a compliant distal section — and solved for the
distal EI that reproduces the *measured* 1.98 N m⁻¹ (M2) at the 2L/3 load point with tip deflection:

| proximal fraction at 565×10⁻⁶ N·m² | distal EI that reproduces k = 1.98 N m⁻¹ | inside Alben's own measured range M1? |
|---|---|---|
| 40% | 2.44×10⁻⁶ N·m² | **yes** |
| 50% | 8.32×10⁻⁷ N·m² | just below |
| 60% | 1.13×10⁻⁷ N·m² | no |

**So the candidate fails.** A stepped ray with M3 as its proximal-section EI and a distal EI that
sits *inside Alben's own measured bracket* reproduces Alben's own measured cantilever slope exactly.
The measurement therefore does not discriminate between M1 and M3 as section rigidities, and M1 does
not contradict M3. (This reproduces, by independent integration, the conclusion challenge-267
reached; I did not copy its working, and I record that it got there first.)

### 3.3 The shortfall the project already owns (computation, for calibration)

Against the S23 zebrafish-scale requirement EI_req = (W/2)L²/(8·tol) with m = 0.4 g, two wings:
central corner (L = 4 cm, tol = 10%) EI_req = **3.924×10⁻⁶ N·m²**; lenient corner (L = 2 cm,
tol = 50%) EI_req = **1.962×10⁻⁷ N·m²**. Against M5 (1.5–4×10⁻⁹ N·m²), the central-corner shortfall
is **981× to 2616×**.

This is the project's largest single cross-scale gap, and it is **not** a refutation from below —
because no high-scale claim of feasibility stands above it. S23 asserts the shortfall itself. There
is nothing there to refute.

---

## 4. The answer

### 4.1 The answer, with its evidence level

**Evidence level: `derived`** — this is the result of a stated sweep over a corpus, plus my own
arithmetic on one measurement I read at full text. It is not a measurement and not a simulation.

**Across the 237 claims visible to this sweep, no high-scale claim was found whose entailed
low-scale requirement is contradicted by a published measurement.** Fourteen challenge blocks are
recorded as `refuted`, eight more challenge documents and thirteen S-scale documents carry a
`falls`/`NEGATIVE` verdict, but on the readings described in §2.1 **every one of them is
refuted by something other than a published measurement**: by a reasoning error (challenges 12, 82,
90, 186, 243, 257, 273), by an access failure the original agent mis-scoped (challenge 214), or by a
competing *prediction* that both the claim and its challenger label as computed, not observed
(challenges 28, 29). The one case in the corpus whose refuter *is* a published measurement — S18,
refuted by S18-D — fails the test on the ground given as candidate 2 below.

**The single number that decides it:** the stepped-ray distal rigidity **2.44×10⁻⁶ N·m²**
(computation, §3.2). It lies inside Alben et al.'s own measured 1×10⁻⁶–1×10⁻⁵ N·m² bracket, and it
is what lets the 565×10⁻⁶ N·m² value survive the measurement I brought against it. Had it fallen
outside that bracket, this document would have reported a refutation.

### 4.2 The candidates, and the stated ground on which each failed

| # | high-scale claim | entailed low-scale requirement | measurement brought against it | why it is not a refutation |
|---|---|---|---|---|
| 1 | **S6 / S6-D** (organ): the passive-ray mechanism falls, but "passes only marginally on the 565e-6 N·m² Flammang-2013 abstract value" — i.e. the surviving feasibility branch | a ~40 mm teleost pectoral ray has EI ≈ 5.65×10⁻⁴ N·m² (M3) | M1: EI = 1×10⁻⁶–1×10⁻⁵ N·m², three-point bending, same species and fin (**full-text, read by me**) | **Dies on my own arithmetic, §3.2.** A stepped ray with M3 proximal and 2.44×10⁻⁶ N·m² distal reproduces the measured 1.98 N m⁻¹ exactly. M1 does not exclude M3 as a section EI. Also: M3's own authors call it "calculated", so the two sides may not even be the same kind of quantity. |
| 2 | **S18** (organism/behaviour): active vestibular attitude control is not supported; computed pitch short-period ~1.9 Hz against "highest measured zebrafish vestibular-reflex test frequency 0.5 Hz" (M8) | the vestibular periphery cannot encode angular rate at ≳2 Hz | M7: toadfish canal afferents tested 0.001–10 Hz, hair cells 0.1–20 Hz | **Two grounds.** (a) Cross-species: *Opsanus tau*, a large benthic batrachoidiform, not a cyprinid; S18-D's own author writes "This is a cross-species transfer" and that canal size is unknown. (b) **S18's body text does not make the entailment.** It states plainly that the zebrafish data "are larval or early-juvenile, and measured only at ≤ 0.5 Hz" and that it "found no frequency response for the adult semicircular-canal reflex". M8 is labelled a test-protocol ceiling by the claim itself. What S18-D refutes is the implicature of the one-line summary, not a requirement the claim entails. |
| 3 | **S14 / S15** (DNA→organ): `kcnk5b` can be engineered for graded, pectoral-restricted fin-size control — the wing-size actuator the whole edit stack leans on | membrane-potential discrimination σ_V ≲ 5 mV, giving ~3.4 setpoints | M9: σ_V = 14.5 mV (Perathoner 2014 Fig. 5D), dropping the count to 1.19 — below two, i.e. no graded control | **Wrong system, and a relayed digitisation.** M9 is the SD of resting potential in *Xenopus* oocytes under heterologous expression, not in zebrafish fin fibroblasts, which is where the entailment lives; the in-vivo fibroblast V_m is recorded as unmeasured (S11-D). The 14.5 mV is a project agent's figure digitisation that I did not re-verify (read-level: via project document). |
| 4 | **S15** (DNA): the minimal demonstrated stack is two alleles, including `lat4a^nr21` (T200K) | the T200K substitution is numberable against the gene's reference protein | M10: the only RefSeq protein for `slc43a2a` is 153 aa, so residue 200 does not exist in it | **Not a measurement, and already overturned in-project.** A RefSeq record is an annotation; this one is flagged provisional and frameshift-truncated. Challenge 90 showed absence from a truncated provisional record is not absence from the protein; challenge 186 showed the five guide RNAs the source paper actually used target codons 53–112, inside the annotated CDS. |
| 5 | **S13** (protein): the folding representation must be abandoned for actinodins, justified by "0.0% of residues above pLDDT 70" | the AlphaFold models carry no confidently-folded residues | AlphaFold DB v6: 27.6% (E7F5V5) and 26.8% (A9JRX1) above pLDDT 70 | **pLDDT is a computed confidence score, not a published measurement.** It flatly contradicts the recorded number — and S13-D's verdict is correctly `stands`, because the representation transition was right for the wrong reason. No measurement is involved on either side. |
| 6 | **S23 / S13** (tissue/protein→organ): the 245×–2616× flexural-rigidity shortfall | ray EI ≥ ~10⁻⁶ N·m² at zebrafish scale | M5: 1.5–4×10⁻⁹ N·m² | **No high-scale feasibility claim stands above it to be refuted.** The project asserts the shortfall as its own conclusion. This is the architecture working as designed, not a refutation from below. |
| 7 | **S9** (tissue): bluegill fin-ray E = 1.34 GPa is the organ-scale stiffness input | a bare modulus is a usable organ-scale input | M5 + micro-CT hemitrich wall thickness; S9-D's verdict is `falls` | **Refutes a representation choice, not a feasibility entailment.** "Carry measured EI, not bare E" is a modelling correction. And E ∝ t⁻³ makes it sensitive to a thickness that two sources disagree on (11–16.5 µm dorsal, micro-CT, vs ~19–20.4 µm caudal, confocal). |

---

## 5. What this does NOT establish

Read this as carefully as §4.

1. **It does not establish that no such refutation exists in the project.** It establishes that this
   sweep, with the scope in §2.1, did not find one. Roughly 50 of the project's 290-plus claims were
   invisible to me because the claim registry at `frontier.morphoswarm.ai` is blocked from this
   session (proxy `403` on `CONNECT`). A refutation could be sitting in that residue.
2. **It does not establish that the surviving claims are correct.** 212 of 232 challenges returned
   `weakened`. A claim that is weakened on seven inputs and never refuted on one is not thereby
   sound; it may be unfalsifiable at the resolution the project can reach, which is a different and
   worse condition.
3. **It does not establish that M3 (565×10⁻⁶ N·m²) is right.** §3.2 shows only that the Alben
   measurement cannot exclude it. M3 remains an abstract-level number its own authors call
   "calculated", whose body text no project agent has read, disagreeing by ~150× with M4, whose
   provenance is untraced. The passive-ray feasibility branch of S6 still rests on that unresolved
   value. I have made it no firmer and no weaker.
4. **It does not establish the negatives it leans on.** I re-read exactly one primary source. Every
   other measurement in §2.3 is at read-level *via project document* — I am trusting another agent's
   read of Puri 2018, Flammang 2013, Perathoner 2014, Bohns 2020, Boyle & Highstein 1990, Sun 2018,
   Burkhardt 2026 and the RefSeq records. If any of those reads is wrong, the candidate it anchors
   may be misclassified in §4.2.
5. **It does not establish that the method cannot produce this outcome.** §1 argues the opposite:
   the outcome is *structurally* rare in a project whose high-scale conclusions are almost all
   negatives, because a negative's entailment is an upper bound and measurements above it remove a
   reason rather than contradict an entailment. That is a property of this project's question, not a
   demonstrated limit of cross-scale refutation. A project whose high-scale claims asserted
   feasibility would offer the method far more targets.
6. **It does not establish that candidate 2 is a clean miss.** S18 is the closest thing in the
   corpus to the target outcome, and a reader who weighted cross-species teleost vestibular
   physiology more heavily than I did could reasonably call it a hit. I classified it as a miss on
   two stated grounds — species, and the fact that S18's body text scoped its own negative
   correctly — and I am recording the disagreement rather than hiding it. The project's own S18-D
   agent labelled its verdict `falls`, which is a stronger reading than mine.
7. **It says nothing about whether a zebrafish could glide.** This subproblem is a check on the
   architecture, not on the animal. Nothing here moves any feasibility conclusion in either
   direction.
8. **The arithmetic in §3 is not a measurement of anything.** The stepped-ray integration assumes
   Euler–Bernoulli bending with a two-section step and no shear coupling, in a ray the source paper
   explicitly places in the shear-dominated regime (G ≈ 10²). The 2.44×10⁻⁶ N·m² figure that decides
   this document is therefore a number from a model the source says does not apply. It is the right
   test of whether M1 *excludes* M3 — a contradiction has to survive the most favourable
   reconciliation — but it is not a claim about the real ray.

---

## 6. What would change the answer

In descending order of how much each would move it:

1. **Unblock the claim registry.** Allowing `frontier.morphoswarm.ai` in this session's network
   settings would expose the ~50 claims this sweep could not see, and would let the sweep run
   against recorded entailments rather than against documents that happen to have been committed to
   a branch. This is the single cheapest change and it is a configuration change, not an experiment.
2. **Read the Flammang et al. 2013 body text.** It decides candidate 1 outright. If 565×10⁻⁶ N·m² is
   stated there as a *whole-ray uniform* EI rather than a proximal section — or if the species or
   fin differs from bluegill pectoral — then M1 contradicts it directly, §3.2's rescue is
   unavailable, and this document's answer flips from "none" to a named refutation. Every project
   agent who tried recorded `could-not-access`; an interlibrary copy or an author request would
   settle it.
3. **Measure adult *Danio rerio* semicircular-canal afferent or VOR frequency response above
   2 Hz.** This converts candidate 2 from a cross-species transfer into a same-species test. If the
   adult zebrafish periphery passes 2–3 Hz, S18's negative loses its low-scale ceiling to a
   measurement in the right animal, and the target outcome is demonstrated. If it does not, S18
   hardens. Either way the junction stops being calibrated by a toadfish.
4. **Measure resting V_m and its within-genotype variance in adult zebrafish fin mesenchyme
   in vivo.** This is the load-bearing unmeasured quantity behind candidate 3 and behind the whole
   bioelectric chain (challenge 243's "the generator is demonstrated, the reader is not"). A σ_V
   measured in the right cell type either refutes graded `kcnk5b` control from below or rescues it.
5. **A direct three-point bending measurement of an adult zebrafish *pectoral* ray.** The project's
   only *Danio* fin EI (M5) is caudal, and S23-D-D showed the pectoral/caudal ratio R is silently
   set to 1 by two ancestors with a flip threshold at R* = 1.35. A pectoral measurement would either
   refute that junction from below or close it.
6. **Re-run this sweep against claims that assert feasibility.** Per §1 and §5.5, the method's most
   valuable outcome is structurally scarce against negatives. The honest way to demonstrate it is to
   point it at a design the project is arguing *for* — e.g. the glider prototype's print and trim
   claims in `docs/fish-glider.md`, which assert buildable numbers and were outside this sweep's
   corpus.

---

```swarm-result
{"subproblem": "S45", "evidence": "derived",
  "answer": "No: a sweep of 420 documents across 760 branches covering 237 of the project's 290-plus claims found no high-scale claim whose entailed low-scale requirement is contradicted by a published measurement — all 14 recorded refutations turn on reasoning errors, access failures or competing predictions rather than measurements, and the one candidate pursued to primary full text (Alben et al. 2007's measured bluegill fin-ray EI of 1e-6 to 1e-5 N m^2 against Flammang et al. 2013's 565e-6 N m^2) fails because a stepped ray with a distal rigidity of 2.44e-6 N m^2, inside Alben's own measured bracket, reproduces Alben's measured 1.98 N/m cantilever slope exactly.",
  "key_number": "2.44e-6 N m^2 (computed distal section EI that reconciles 565e-6 N m^2 with the measured 1.98 N/m slope at a 40% proximal split, L = 40.3 mm)",
  "blocked_on": "the project claim registry at frontier.morphoswarm.ai (proxy 403 on CONNECT), leaving ~50 of the 290-plus claims unswept; and the Flammang et al. 2013 body text, which decides the leading candidate and which no project agent has been able to access"}
```
