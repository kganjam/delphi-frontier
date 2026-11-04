# S14-D-D — Deepening S14-D by attacking σ_V, the one input it never measured

**Parent subproblem (S14-D, protein).** *Deepen S14: attack its most sensitive input.*
Recorded in `docs/research/fish/S14-deepen.md` on branch
`claude/deepen-s14-potassium-channel-5miqg2`.

**S14-D's recorded conclusion.** The S14 answer **FALLS**. Its stated structural input
(pLDDT > 80) is misstated and not decision-relevant; the input the feasibility of
"graded, pectoral-restricted control" actually rests on is the measured ~2-fold
macroscopic K⁺ conductance window of the *alf* alleles, which buys 13–17 mV and
"~3.4 distinguishable setpoints at σ_V = 5 mV."

**Date of work:** 2026-11-04. Every retrieval below is from that date.

**Provenance convention (repo rule 9).** Everything load-bearing carries a read-level in
§5. Nothing in this document is an observation of mine. Three classes of number appear
and each is labelled at the point of use: **author-reported** (values the cited authors
published, including their deposited per-individual data), **digitized** (values I
extracted computationally from a published figure image — not author-reported), and
**calculated** (my arithmetic on either of the first two). Two parsing errors that the
controls caught are recorded in §3e rather than quietly fixed.

**Bottom line (§4d): S14-D's conclusion STRENGTHENS.** Its weakest input, σ_V = 5 mV,
was an unsourced assumption. Every measured or digitized estimate of that quantity is
larger — 7.8, 14.5 and 19.9 mV — so the parent's level count was **optimistic by 1.6× to
4×**, and the real figure is **~1.2 distinguishable setpoints: an on/off switch**. Three
independent readouts agree, and the verdict no longer flips within a factor of two.

---

## 1. Step 1 — the input S14-D is most sensitive to

### 1a. Its conclusion is a quotient, and only one term of it was ever measured

S14-D's decisive number is a count of distinguishable setpoints:

> levels = (Vm window opened by the conductance change) / σ_V

- The **numerator** is tied down from both ends. The conductance fold-change R = 2 is
  author-reported from a real experiment, and S14-D swept the one unstated model
  parameter (Vm_wt) across −20 to −60 mV, finding 13–17 mV throughout. That is proper
  work, and it leaves the numerator robust.
- The **denominator**, σ_V, is a number S14-D introduced itself. Its own §6 lists σ_V
  under "what I did not establish": *"σ_V, the within-tissue membrane-potential
  discrimination step … Unmeasured in any source I read."*

So the conclusion is a ratio of a well-bounded measured quantity to an unmeasured one.

### 1b. Showing the sensitivity by recomputing, not by asserting it

S14-D's own §4c sweep is the demonstration, and it is worth restating because it is the
reason this is the input to attack. Window fixed at 17.1 mV (**calculated**, S14-D's
parallel-conductance model, inherited unchanged so the two documents stay comparable):

```
   sigma_V =  2 mV ->  8.57 levels     comfortably graded
   sigma_V =  5 mV ->  3.43 levels     S14-D's headline: marginal
   sigma_V = 10 mV ->  1.71 levels     on/off switch
   sigma_V = 15 mV ->  1.14 levels     on/off switch
```

The level count is exactly inversely proportional to σ_V. R enters once and Vm_wt barely
at all, but σ_V sets the answer alone. S14-D says as much: *"It also flips on σ_V alone:
at σ_V = 10 mV the window holds 1.7 levels even with R = 2."* It identified the
vulnerability and then left it as a sweep. **A factor of two on σ_V moves the verdict
between "graded" and "switch", and nothing in the parent pins it down.** That is the
input.

### 1c. Why not the other candidates

- **R = 2.** Already attacked by S14-D; it is author-reported from a real experiment. I
  found nothing new on it (§3d), so re-attacking it would duplicate the parent.
- **E_B = 0 mV**, the assumed background-branch reversal potential. A real assumption,
  but it enters through the compressive transform and moves the window by a few mV, not
  by a factor of two.
- **The sign disagreement** between Perathoner 2014 and Jiang 2024. Decisive for the
  verdict but **not a number** — it cannot be wrong by a factor of two, so it is not what
  this exercise asks for. I report new evidence bearing on it in §3c anyway.

---

## 2. Step 2 — how well is σ_V = 5 mV established?

**Evidence level: assumption. Read-level: not applicable — it has no source.**

This is the honest answer and it is unflattering, because S14-D is work from this same
swarm. The 5 mV is not a proxy for a measured quantity and it is not a number repeated
until it reads as measured. It is a modelling placeholder, introduced inside a sweep,
which then propagated into the one quoted figure of the conclusion ("~3.4 levels"), into
the `key_number` field of the parent's `swarm-result`, and from there into any graph edge
that consumed it. **A swept parameter became a headline number between §4c and the
summary block.** The sweep was honest; the carry-through was not.

Two further things make 5 mV the specific value to distrust:

1. It sits at the **favourable end** of the parent's own sweep. The sweep ran 2–15 mV;
   the quoted conclusion used 5 mV, which yields the most generous level count short of
   2 mV. Nothing justified that choice over 10 mV, which the same table shows gives 1.71.
2. A membrane-potential *discrimination step* is not a quantity anyone measures directly.
   It is a stand-in for the scatter of Vm across cells or individuals at a fixed actuator
   setting. That scatter **is** measurable — and, it turns out, has been measured.

---

## 3. Step 3 — going and improving it

Two routes. The first finds the parent's own parameter in calibrated millivolts. The
second drops the millivolt model entirely and asks the question directly of the output
variable, using the authors' deposited per-individual data.

### 3a. Route one: σ_V in calibrated mV, digitized from Perathoner et al. Figure 5D

S14-D read Perathoner et al. 2014 at full text and quoted its Figure 5 caption, including
the phrase *"(D) Kcnk5b influences membrane potential (V_m) in oocytes. The mutant
variants tend to hyperpolarize the cell (each point represents one oocyte)."*

**Figure 5D is a per-individual, calibrated-mV membrane-potential scatter.** It plots Vm
[mV] against I50 [µA], one marker per oocyte, in three genotypes. It is the only
calibrated per-individual Vm dataset I found anywhere for this channel — and it contains,
directly, the within-group scatter that σ_V stands for.

**The authors published no numerical table for it.** *Scope: all PLOS supplementary slots
for doi 10.1371/journal.pgen.1004080, 2026-11-04 — s001–s004 return TIFF figure images
(Figures S1–S4, no numerical data); s005–s008 return HTTP 404.* So I recovered the values
from the figure image by colour-segmenting the markers and calibrating against detected
tick-mark pixels.

**These are digitized values, not author-reported values and not observations of mine.**
The digitizer is committed as `S14-D-D-digitize.py`; it prints the per-point table and its
own occlusion caveat. Result:

| Series | n recovered | Vm mean | Vm SD | Vm range |
| --- | --- | --- | --- | --- |
| `kcnk5b`(wt) | 5 | −25.6 mV | **14.5 mV** | −5.5 to −41.0 |
| `kcnk5b`(W169L) | 6 | −42.7 mV | 27.6 mV | −12.1 to −81.0 |
| `kcnk5b`(F241Y) | 9 | −35.0 mV | 16.1 mV | −12.1 to −61.0 |
| pooled | 20 | −35.0 mV | **19.9 mV** | −5.5 to −81.0 |

**The improved input: σ_V ≈ 14.5 mV** (within-wild-type SD), where S14-D assumed 5 mV.
Even the single most generous reading of this dataset, below, does not get near 5.

**The steelman against my own number, computed rather than waved at.** Much of that
spread is not noise: Vm covaries with I50, so part of it is variation in how much channel
each oocyte expressed — which a designed, expression-controlled system would remove. The
right generous estimate is therefore the residual scatter at *fixed* conductance. Pooled
OLS over all 20 digitized points (**calculated**): slope −2.046 mV/µA, **residual
SD = 7.8 mV**. Per series: 6.2 (wt), 8.1 (W169L), 7.4 (F241Y) mV.

**So the defensible range for σ_V is 7.8–19.9 mV, and the parent used 5.**

**Occlusion, stated in both directions.** My extraction recovers 5, 6 and 9 markers where
Figure 5C reports n = 8, 11 and 12 oocytes for the I–V curves; one 540-px blob is at least
two merged markers, so the true counts are higher than I recover. If the missing markers
sit in the dense middle of each cloud, my SDs are **overestimates**; if in the tails,
underestimates. §4c carries the unfavourable direction through to the verdict. Note that
the residual-SD figure of 7.8 mV already bounds that direction, and even it gives fewer
levels than the parent claimed.

**One consistency check that passes.** S14-D could not find a wild-type resting potential
and swept Vm_wt over −20 to −60 mV. The digitized wild-type mean is −25.6 mV — inside the
sweep. The parent's sweep was well chosen; it is only the denominator that was wrong.

### 3b. Route two: drop millivolts, and ask the authors' own per-individual data

σ_V in millivolts is itself a proxy. What "graded control" needs is distinguishable
setpoints **of the controlled output**, which is fin size. That is measurable without any
calibration, any E_K, any E_B and any parallel-conductance model, as the separation
between the two ends of the achievable manipulation in units of the biological variance:
Cohen's d. One unit of d is one setpoint spaced at 1 SD, where neighbouring settings still
misclassify about 31% of individuals; 2-SD spacing is the defensible engineering criterion.

Jiang et al. 2024 deposited the per-individual numbers behind every figure (S1–S7 Data,
XLSX). **The values are author-reported; the d's are my calculation on them**
(`S14-D-D-authordata.py`).

| Readout | Comparison | fold | **d** | setpoints at 2-SD |
| --- | --- | --- | --- | --- |
| Fin bud/eye area (**the output**) | AB vs GFP — **null control** @48 hpf | 1.03× | **0.17** | 0.09 |
| Fin bud/eye area | AB vs GFP — **null control** @32 / @56 hpf | 0.96× / 1.09× | 0.25 / 0.36 | 0.13 / 0.18 |
| Fin bud/eye area | GFP → kcnk5b @32 hpf | 1.50× | **2.60** | 1.30 |
| Fin bud/eye area | GFP → kcnk5b @48 hpf | 1.62× | **1.94** | 0.97 |
| Fin bud/eye area | GFP → kcnk5b @56 hpf | 1.63× | **2.56** | 1.28 |
| Fin bud/eye area | GFP → kcnk10 @48 hpf | 1.26× | 1.16 | 0.58 |
| DiSBAC₂(3) Vm proxy | mCherry → kcnk5b-Tg (Fig 5K) | 1.82× | **2.45** | 1.22 |
| DiSBAC₂(3) Vm proxy | mCherry → kcnk5b (Fig 5L) | 1.36× | **1.35** | 0.68 |
| Fin/eye ratio | AB: drug vs vehicle — **drug-only control** | 1.04× | 0.28 | 0.14 |
| Fin/eye ratio | AB → kcnk5b (Fig 5Q) | 1.32× | 1.18 | 0.59 |

The two null controls are what make this readable: two control genotypes imaged the same
way separate at d = 0.17–0.36, and a vehicle-versus-drug control at d = 0.28. So the floor
is real and small, and the d ≈ 2 against it is a real effect, not a measurement artifact.

**Three independent readouts, three answers in the same place.** The full kcnk5b
manipulation — the entire dynamic range anyone has demonstrated — separates at
**d ≈ 1.9–2.6 on the phenotype**, **d ≈ 1.35–2.45 on the fin-bud voltage proxy**, and
**d ≈ 0.60–0.75 on calibrated oocyte Vm** (digitized, §3a, wt vs F241Y and wt vs W169L).
Every one is at or below S14-D's 3.43, and the calibrated one is far below.

**I am preserving the spread, not averaging it.** Fig 5K and Fig 5L measure the same thing
in the same paper with the same dye and return d = 2.45 and d = 1.35. That is a factor of
1.8 of unexplained within-paper variation in the key discriminability, and it is itself
evidence about how tightly this system can be held.

**The caveat that cuts against my verdict, stated plainly.** d is a *per-individual*
quantity. If "graded control" means setting the mean of a population rather than the size
of a given animal, then averaging n animals improves separation by √n and far more than
three levels are resolvable. I take per-individual as the right reading — a controller
that cannot place one animal at a chosen size is not a controller — but the group-mean
reading is defensible and under it my conclusion weakens considerably.

**A second caveat.** These are embryonic pectoral fin buds at 32–56 hpf, where the
manipulation gives 1.5–1.8×. Adult median-fin *alf* phenotypes are visibly larger. If
adult pectoral dynamic range exceeds the bud range, d would rise. *Scope: Perathoner et
al. 2014 full text — the string `pectoral` occurs 0 times, so that paper supplies no adult
pectoral measurement; I found no adult pectoral fin-size series in any source I read.*

### 3c. New evidence on the ceiling, which the parent inferred but did not source

S14-D argued from its model that the Vm transform is compressive and therefore saturating.
There is direct experimental evidence for a saturating output that neither the parent nor
S14 cited, in a paper S14-D did read at full text.

*Sci Rep* 2018 (PMC6039437), on calcineurin inhibition during fin regeneration, their
words:

> "FK506-treatment of fish with gain-of-function of kcnk5b activity does not lead to an
> additional increase in the size of the regenerate or rate of its growth over untreated
> mutants"

> "All fins treated with FK506 regrow at comparably increased rates, regardless of
> genotype or previous size."

> "FK506-treated fins from cx43/sof mutants were indistinguishable from treated wild-type
> fins"

**That is the authors' report. My inference, stated separately:** three different starting
points — `cx43/sof` short-fin, wild type, and `kcnk5b/alf` long-fin — converge on one
treated size, and adding the drug on top of the channel gain-of-function adds nothing.
That is the behaviour of a switch into a single maximal-growth state, not of a settable
setpoint. It is independent of my d calculation and of the parent's model, and it points
the same way.

**And the evidence that cuts the other way, preserved rather than resolved.** The same
paper reports, citing its reference 26: *"Treatment of regenerating fins with the
calcineurin inhibitors FK506 and cyclosporin A led to dose-dependent coordinated
overgrowth of fin regenerates (Fig. S1E)."* **Dose-dependent** is precisely gradedness. So
within one paper: a pharmacological actuator that grades with dose, and an endpoint that
converges to a common ceiling regardless of genotype. I did not reach the per-dose
numbers (Fig. S1E is a figure; *scope: I did not retrieve Sci Rep supplementary files*),
so I cannot say how many dose levels were resolved, and I am not resolving the tension.
Note which side of the question each sits on: the gradable actuator is **calcineurin
inhibition**, not the channel — consistent with the parent's reframe that the workable
levers are the ones that bypass protein engineering.

### 3d. Negative searches, with scope stated

- *Scope: regular-expression search for the pattern `<number> ± <number> mV` across all
  four full texts retrieved (PMC3894163, PMC11018282, PMC6039437, PMC8110307),
  2026-11-04: **0 occurrences in each**.* No paper reports a membrane potential with a
  dispersion in the text. Fig 5D's scatter is the only per-individual Vm anywhere, and
  only as a figure.
- *Scope: PLOS supplementary slots s001–s008 for doi 10.1371/journal.pgen.1004080,
  2026-11-04.* Four TIFFs, then 404. Positive control: the equivalent slots for doi
  10.1371/journal.pbio.3002565 return seven XLSX files, so the method does find deposited
  data when it exists.
- *Scope: Europe PMC query `kcnk5b`, 2026-11-04 — hitCount 57*, byte-for-byte the count
  S14-D reported. I did not re-run the parent's refinements of it; its negative on
  single-channel conductance stands unchallenged and unimproved by me.
- **Nothing refines R = 2.** I found no replacement measurement of the conductance
  fold-change, so that input is exactly where the parent left it.

### 3e. Controls, including two parsing errors they caught (repo rule 8)

| Check | Positive control | Must-fail control | Verdict |
| --- | --- | --- | --- |
| Full-text retrieval | All four PMC full texts returned byte counts **identical** to those S14-D recorded (142,283 / 364,543 / 95,787 / 285,644) | — | **valid** — independent reproduction of the parent's retrievals |
| Fig 2C block bounds | Every group mean in 0.1–0.5 with CV < 30% | A read past row 25 yields mean 0.71, **CV 558%** | **valid** — assertion now in the script |
| PLOS supplementary fetch | pbio.3002565 s001–s007 → 7 XLSX | pgen.1004080 s005–s008 → HTTP 404, distinct from a 200 with empty content | **valid** — absence is distinguishable from failure |
| Figure digitizer | Tick detection recovers 4 evenly spaced y-majors (110.5 px apart) and 5 x-majors (135.25 px apart); marker blobs ~300 px | Legend swatches excluded by position; blobs < 120 px rejected as anti-aliasing; a 540-px blob **flagged as merged**, not silently counted as one | **valid, with the occlusion caveat in §3a** |

**Error 1, caught by the control, recorded rather than hidden.** My first read of Jiang's
`Fig. 2C` sheet ran each column to its end. The sheet stacks the fin-bud/eye **ratio**
block (rows 4–25) on top of per-genotype **raw pixel area** blocks (rows 29+) in the same
columns, so the read silently concatenated ratios of ~0.2 with areas of ~10⁵ and returned
a group mean of 0.71 with a CV of 558% and nonsense Cohen's d values of 0.11–0.13. The
plausibility control (ratios must be 0.1–0.5) caught it; the corrected parse uses explicit
row bounds and the committed script asserts the range.

**Error 2.** My first axis-tick detection found only two y-ticks and one x-tick, because
the threshold conflated major ticks (8 px) with minor ticks (4 px) and axis-label glyphs.
Separating by run length gave four y-majors at an exactly even 110.5 px spacing and five
x-majors at 135.25 px — the evenness is the control that the calibration is right.

### 3f. What measurement would settle it

Unchanged from S14-D's §3d, and now better specified by what the digitization shows.
The quantity is **calibrated resting membrane potential in pectoral fin-bud mesenchyme,
per cell, with its within-bud distribution reported** — the distribution, not the mean,
because the distribution *is* σ_V and it is the term that decides the question. The 2024
paper's own patch-clamp rig is described in its methods, though it was used on HEK293T
cells rather than fin-bud cells, so this is an extension of in-house capability.

The digitization adds a second, cheaper experiment that would sharpen σ_V immediately:
**report the per-oocyte Vm values behind Figure 5D as a table, together with expression
normalisation.** That data already exists; it was collected in 2014. Splitting its scatter
into expression-driven variation and irreducible scatter is exactly the 7.8-vs-14.5 mV
question, and it needs no new animals.

**Cost: `unknown`.** I have no costed proposal for either and will not invent a figure.
Both are single-rig electrophysiology on an established model organism; the second is a
data-release request, not an experiment.

---

## 4. Step 4 — recomputing S14-D's conclusion with the improved input

All numbers in this section are **calculated** by `S14-D-D-recompute.py`, which inherits
S14-D's model and R unchanged so the two are directly comparable.

### 4a. The level count, with σ_V measured instead of assumed

Window 17.1 mV (S14-D's worked example at Vm_wt = −40 mV):

```
   sigma_V =   5.0 mV  (S14-D assumed, no source          ) ->  3.43 levels
   sigma_V =   7.8 mV  (digitized residual at fixed I50   ) ->  2.20 levels
   sigma_V =  14.5 mV  (digitized wild-type within-group SD) ->  1.19 levels
   sigma_V =  19.9 mV  (digitized all-genotype pooled SD   ) ->  0.86 levels
```

And at the digitized wild-type resting potential of −25.6 mV, where the window is 15.2 mV
rather than 17.1 — the parent had to guess this and guessed generously:

```
   sigma_V =   5.0 mV ->  3.04 levels
   sigma_V =   7.8 mV ->  1.95 levels
   sigma_V =  14.5 mV ->  1.05 levels
   sigma_V =  19.9 mV ->  0.76 levels
```

**Every estimate grounded in data gives fewer levels than the assumption did.** The most
favourable grounded reading — residual scatter at fixed conductance, at the parent's own
more generous Vm_wt — is 2.20, and the central estimate is **1.19: one setpoint, which is
an on/off switch.**

### 4b. The factor-of-two test on the improved input

```
   sigma_V =  3.6 mV (0.25x digitized) ->  4.74 levels
   sigma_V =  7.2 mV (0.50x digitized) ->  2.37 levels
   sigma_V = 14.5 mV (1.00x digitized) ->  1.19 levels
   sigma_V = 28.9 mV (2.00x digitized) ->  0.59 levels
```

This is the key difference from the parent. S14-D's verdict flipped within a factor of two
of its input — it said so, and that was the honest weakness of its position. **With the
digitized input it does not.** Halving σ_V gives 2.37 levels, still below the ~3 the parent
treated as already marginal; doubling it gives 0.59. The conclusion is now stable across
the whole factor-of-two band, and it would take a **4× error** in my digitization,
all in one direction, to recover a graded reading. The occlusion caveat in §3a is the only
route to such an error and it is bounded well below 4× by the 7.8 mV residual figure.

### 4c. Carrying the unfavourable caveat through

Suppose the markers my digitizer missed all sit in the dense centre of each cloud, so that
the true wild-type SD is smaller than 14.5 mV. The residual-SD estimate of 7.8 mV is the
floor that assumption can reach, because it already removes the expression-driven spread
that is the main source of the width. At 7.8 mV the count is 2.20 levels at the parent's
Vm_wt and 1.95 at the digitized one. **Under the worst case for my argument, the parent's
3.43 still falls to ~2, and the answer is still not graded control.**

The independent route in §3b reaches the same place without any of this machinery: the
whole manipulation separates at d ≈ 1.9–2.6 on the output variable, which is 1.0–1.3
setpoints at 2-SD spacing.

### 4d. The verdict

**S14-D's conclusion STRENGTHENS.**

**What strengthens:**
- "The channel-engineering route is capped at ~3 levels." The cap is **~1.2 levels**, and
  ~2.2 under the reading most generous to the opposite case. S14-D was right about the
  direction and optimistic about the magnitude by 1.6× to 4×.
- "The verdict flips within a factor of two." It no longer does. With σ_V grounded, the
  conclusion survives the full factor-of-two band in both directions (§4b).
- "The transform saturates." The parent inferred this from its model. *Sci Rep* 2018
  reports three genotypes of different starting size converging on one treated size, and
  the drug adding nothing on top of the channel gain-of-function (§3c) — experimental
  evidence for a ceiling, which the parent did not have.
- The reframe — that the workable levers (optogenetic Vm setting, cell-type-specific
  promoters) bypass protein engineering — gains a third member: calcineurin inhibition
  grades with dose, and it too is not the channel.

**What is unchanged, because I did not touch it:**
- R ≈ 2. No source refines it; the parent's characterisation stands unimproved.
- The Perathoner/Jiang sign disagreement in pectoral tissue. I add no measurement to it.
  It remains unresolved and remains a reason the channel route is not costable.
- The absence of an experimental kcnk5b structure, and the misstatement of pLDDT. Not
  re-tested here; the parent's controls on those were sound.

**What weakens, and I am not hiding it:**
- S14-D's §4c presented "~3.43 levels" as its headline figure with σ_V = 5 mV chosen from
  inside its own sweep and never sourced. That specific number should not have been
  quoted as a result, and it propagated into the parent's `key_number`. The conclusion it
  supported survives — but it survives on inputs the parent did not have, not on the ones
  it offered.
- If "graded control" is read as control of a population mean rather than of an
  individual, √n averaging defeats this entire analysis (§3b). I take the per-individual
  reading; a reader who takes the other one should treat this verdict as not established.

A negative result, stated precisely: **the measured per-individual scatter of membrane
potential is large enough, relative to the entire window the alf alleles open, that the
kcnk5b conductance axis supports roughly one distinguishable setpoint.** Three readouts —
calibrated oocyte Vm (digitized), a fin-bud voltage dye, and fin-bud size (both
author-reported) — agree within a factor of about two and all sit below the parent's
assumption. This is not a claim that graded fin-size control is impossible; it is a claim
that the channel's own conductance range is not a usable control axis, now resting on a
measured dispersion rather than a placeholder.

---

## 5. Sources, with read-levels

| Source | Identifier | Read-level |
| --- | --- | --- |
| S14-D, the document deepened here | `docs/research/fish/S14-deepen.md`, branch `claude/deepen-s14-potassium-channel-5miqg2` | **full-text** (repository) |
| Perathoner et al. 2014, *PLoS Genet* 10(1), "Bioelectric signaling regulates size in zebrafish fins" | PMID 24453984, PMC3894163, doi 10.1371/journal.pgen.1004080 | **full-text** (Europe PMC `fullTextXML`, 142,283 bytes — matches the parent's byte count) |
| — its **Figure 5D**, the per-oocyte Vm scatter (σ_V source) | `journal.pgen.1004080.g005`, 1875×1123 PNG | **full-text** (figure image retrieved and digitized; **no numerical table exists** — see §3a) |
| — its supplementary slots | pgen.1004080 s001–s004 (TIFF), s005–s008 | **listing** / **could-not-access** (HTTP 404 for s005+) |
| Jiang et al. 2024, *PLoS Biol*, "The scale of zebrafish pectoral fin buds is determined by intercellular K+ levels…" | PMID 38527087, PMC11018282, doi 10.1371/journal.pbio.3002565 | **full-text** (364,543 bytes) |
| — its deposited per-individual data, S1–S7 Data | pbio.3002565 s001–s007, XLSX | **full-text** (all seven retrieved; Fig 2C, 5A, 5B, 5K, 5L, 5Q analysed) |
| *Sci Rep* 2018, "Bioelectric-calcineurin signaling module regulates allometric growth and size of the zebrafish fin" | PMID 29991812, PMC6039437 | **full-text** (95,787 bytes) |
| — its Fig. S1E, the FK506/cyclosporin A dose series | supplementary | **could-not-access** (not retrieved; per-dose numbers unknown) |
| *eLife* 2021, "A calcineurin-mediated scaling mechanism that controls a K+-leak channel…" | PMID 33830014, PMC8110307 | **full-text** (285,644 bytes) |
| Europe PMC literature sweep | query `kcnk5b`, hitCount 57 | **search-summary** (count only; the parent's refinements not re-run) |

All sources were reached over plain HTTPS on 2026-11-04. I hit no egress denials; the two
403s S14-D recorded (`alphafold.ebi.ac.uk/files/`, `search.rcsb.org`) are on paths this
deepening did not need.

## 6. What I did not establish

- **σ_V in pectoral fin-bud tissue.** My improved number is from *Xenopus* oocytes. It is
  a calibrated, per-individual measurement of the right quantity in the wrong tissue — an
  improvement on an unsourced assumption, not a measurement of the target. The DiSBAC
  route (§3b) is in the right tissue but uncalibrated, which is why I used it
  dimensionlessly.
- **The true marker count in Figure 5D.** My digitizer recovers 20 where Fig 5C's n's
  total 31. Occlusion direction is unknown; §4c carries the unfavourable case.
- **Whether adult pectoral dynamic range exceeds the embryonic bud range** (§3b). If it
  does substantially, d rises and my margin narrows.
- **How many dose levels the FK506/cyclosporin A series resolved** (§3c). I did not
  retrieve the supplementary figure, so "dose-dependent" stays qualitative in my hands.
- **Anything new about R ≈ 2**, the sign disagreement, single-channel conductance, or the
  absence of a kcnk5b structure. Those remain exactly as S14-D left them.
- **Which *alf* allele carries W169L and which F241Y** — still `unknown`; I read the same
  sentence the parent did and it does not say.

## 7. Reproducing this

Three dependency-light scripts are committed beside this file. Each prints every number
quoted above and states in its own header which class of number it produces.

```
docs/research/fish/S14-D-D-digitize.py     Fig 5D -> per-oocyte Vm (needs Pillow, numpy)
docs/research/fish/S14-D-D-authordata.py   Jiang S1-S7 Data -> Cohen's d (needs openpyxl)
docs/research/fish/S14-D-D-recompute.py    the level count and the verdict (stdlib only)
```

Inputs, all public and re-retrievable from the identifiers in §5:

```sh
curl -sSL "https://journals.plos.org/plosgenetics/article/figure/image?size=large&id=10.1371/journal.pgen.1004080.g005" -o g005.png
curl -sSL "https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.3002565.s002&type=supplementary" -o s002.xlsx
curl -sSL "https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.3002565.s005&type=supplementary" -o s005.xlsx

python3 -I docs/research/fish/S14-D-D-digitize.py g005.png
python3 -I docs/research/fish/S14-D-D-authordata.py s002.xlsx s005.xlsx
python3 -I docs/research/fish/S14-D-D-recompute.py
```

`S14-D-D-digitize.py` checks that the input image is the 1875×1123 "large" render and warns
if not, because its panel crop and tick rows are calibrated to that size.

Hashes of the committed script bytes:

```
S14-D-D-digitize.py    sha256 962f08b27c2c5969bce46a7b883cd0d61e84d6caa0db17f1d895959be2dfe6ef
                       git    c08fa8fb731e6fc25dfb6bf38f296216afaafdcf
S14-D-D-authordata.py  sha256 2aa80e0c4a53b7e011789af2d3a008b16e5bda373be26f7ebdbb991fa506d20d
                       git    35e212a77ce20bb0732730c47c53046bce0747d0
S14-D-D-recompute.py   sha256 beea2cc763209cd530cecf2b145a863cd99b3971c579de5fca1120ccb9116ccb
                       git    b4174e747ec65c49fd39425117b9693d185ef4ca
```

Retrieved full texts, the figure image and the XLSX inputs are in this session's
scratchpad at
`/tmp/claude-0/-workspace-delphi-frontier/29198ab4-a413-563d-b09e-f33a5bfc2227/scratchpad/s14dd`,
which is ephemeral; everything there is public and re-retrievable from the commands above
and the identifiers in §5.

```swarm-result
{"subproblem": "S14-D-D", "evidence": "full-text",
  "answer": "S14-D's verdict that the kcnk5b channel-engineering route cannot deliver graded control strengthens, because its one unsourced input -- sigma_V, the membrane-potential discrimination step, assumed at 5 mV and carried from inside a sweep into the headline -- is measurable and larger than assumed: digitizing the per-oocyte Vm scatter of Perathoner et al. 2014 Figure 5D, for which no numerical table was ever published, gives a within-wild-type SD of 14.5 mV (pooled 19.9 mV; 7.8 mV residual at fixed conductance, the reading most generous to the opposite case), so the 17.1 mV window holds 1.19 rather than 3.43 setpoints, the verdict no longer flips within a factor of two in either direction, and three independent readouts agree -- calibrated oocyte Vm at Cohen's d 0.60-0.75, a fin-bud voltage dye at d 1.35-2.45, and fin-bud size at d 1.94-2.60 against null controls of d 0.17-0.36 -- while Sci Rep 2018 adds experimental evidence for the ceiling the parent only inferred, reporting that short-fin, wild-type and alf fins all converge on one treated size and that the drug adds nothing atop the channel gain-of-function.",
  "key_number": "sigma_V = 14.5 mV (within-wild-type SD of per-oocyte resting membrane potential, digitized from Perathoner et al. 2014 PLoS Genet Fig 5D, n=5 recovered; range of defensible estimates 7.8-19.9 mV), replacing the assumed 5 mV and reducing the setpoint count from 3.43 to 1.19",
  "verdict": "strengthens",
  "depends_on": [
    "S14-D (docs/research/fish/S14-deepen.md) and its verdict that the recorded S14 answer falls",
    "S14-D's parallel-conductance model Vm = (gK*EK + gB*EB)/(gK+gB), inherited unchanged",
    "S14-D's assumption EB = 0 mV for the non-selective background branch",
    "EK = -100 mV, author-reported by Perathoner et al. 2014 for Xenopus oocytes",
    "R = 2.0, the almost two-fold macroscopic K+ current increase of the alf alleles, author-reported by Perathoner et al. 2014 (PMC3894163), never replicated and never decomposed into single-channel conductance, open probability and channel number",
    "S14-D's derived 17.1 mV Vm window at Vm_wt = -40 mV, and 15.2 mV at the digitized Vm_wt = -25.6 mV",
    "sigma_V = 14.5 mV, DIGITIZED (not author-reported) from Perathoner et al. 2014 Fig 5D; depends on my colour-segmentation and tick-pixel axis calibration, and on the occlusion assumption that the 20 markers recovered of a possible 31 are not concentrated in the cloud centres",
    "sigma_V = 7.8 mV, the pooled OLS residual at fixed I50, same digitization, used as the steelman floor",
    "the claim that Perathoner et al. 2014 published no numerical table for Fig 5D (scope: PLOS supplementary slots s001-s008 for doi 10.1371/journal.pgen.1004080, 2026-11-04)",
    "Jiang et al. 2024 (PMC11018282) deposited per-individual data S1-S7, specifically sheets Fig. 2C (fin bud-to-eye area ratio, ratio block rows 4-25 only), Fig. 5K, Fig. 5L and Fig. 5Q",
    "the null controls AB vs GFP (d = 0.17-0.36) and vehicle vs drug in AB (d = 0.28), which set the measurement floor for every d quoted",
    "the criterion that distinguishable setpoints are counted per individual at 1-SD or 2-SD spacing, NOT on group means (under group-mean averaging with n animals the conclusion does not hold)",
    "Sci Rep 2018 (PMC6039437) author-reported convergence of cx43/sof, wild-type and kcnk5b/alf fins to a common FK506-treated size, and no additional increase from FK506 atop kcnk5b gain-of-function",
    "Sci Rep 2018 author-reported dose-dependent overgrowth under FK506 and cyclosporin A, which cuts against the saturation reading and whose per-dose numbers I did not retrieve",
    "the unresolved sign disagreement between Perathoner et al. 2014 (hyperpolarization, calibrated clamp, oocytes) and Jiang et al. 2024 (depolarization, uncalibrated dye, pectoral fin buds), inherited from S14-D and untouched here",
    "the absence of any experimental kcnk5b structure, inherited from S14-D via UniProt xref_pdb with controls",
    "the assumption that fin size is monotonic in membrane potential, so that counting setpoints in Vm is meaningful at all"
  ]}
```
