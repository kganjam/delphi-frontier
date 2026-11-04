# Programmable skin — notes, caveats and the verdict

Design space: **"Programmable skin: a cellular actuator you can address."**
Everything in this directory is a model, a measurement read out of someone else's
paper, or a statement about what is missing. Nothing here is an experiment we ran
on an animal.

---

## 1. The verdict: is this design space real, or premature?

**Premature as a cephalopod engineering programme. Real as a measurement programme,
and real as a design brief.** Written out, with the numbers that force it:

**The cephalopod half is blocked on one missing reagent.** Exactly two genetic
manipulations have been demonstrated in any cephalopod chromatophore system:
`tdo` knockout in *Doryteuthis pealeii* (Crawford et al. 2020, PMID 32735817) and
`tdo`+`ido` double knockout giving a heritable albino *Euprymna berryi* line
(Ahuja et al. 2023, PMID 37343558). Both **delete** a pigment gene. We found no
published instance of a transgene being **expressed** in a cephalopod at all. You cannot build an addressable skin by deleting things. Counted rather than
guessed, and computed in `routes.json`'s own `validation` block rather than
asserted here: of the **30** cephalopod-scale routes on this page, **twelve** are
ones nobody can currently take (`route_kind: model`, or `evidence_strength:
proposed`). One of those twelve is this step itself and one is our own
controller-sizing study, which needs no animal. **The other ten are downstream of
expressing a transgene** — and so is every future route of that kind. The ten are
named in `validation.cephalopod_routes_nobody_can_take.downstream_of_the_transgene_step`.

`routes.json` makes this countable rather than rhetorical. Each route carries a
`route_kind` and a boolean `addressable_runtime_control` — does it give a dial you
could use in a working skin, addressed to a place, changeable second by second.
Of 40 routes, **10** qualify. **Five are non-living devices.** Two are vertebrate,
one of which is a combination nobody has yet made and the other of which controls
where a pigment cell *goes* rather than what colour it is. **The three cephalopod
entries are all electrode stimulation of a dissected or opened preparation.** So
the honest state of the art in addressing a cephalopod chromatophore is a wire on
a nerve in a dish.

**The near-term substrate is not a cephalopod.** On the headline capability — skin
that changes appearance on command — the non-living route already wins. A 16x16
autonomously colour-matching optoelectronic sheet was built in 2014 and switches in
1–2 s (Yu et al., PMID 25136094), and a commercial electrophoretic panel runs at
300 ppi, about 85 µm pitch, comparable to a real chromatophore's 15–100 µm
diameter. If you want programmable skin in three years, buy that. If you want
*living, self-repairing, self-assembling, growing* programmable skin, the
vertebrate chromatophore is the tractable biology and the cephalopod is the thing
worth understanding.

**What is genuinely real here, and underexploited, is the control layer and the
developmental layer.** Both are measurable today with a camera and no genetics:
- A chromatophore is **not a pixel**. It is driven by **3.715 ± 1.211** independent
  sources, each innervating a contiguous petal of 3–16 of 36 angular sectors
  (Renard et al. 2026, PMID 42418335, n = 1829 cells). Sedation does not change it
  (3.683 ± 1.224 unsedated, p = 0.83).
- Real pattern transitions are **low-dimensional**: 85% of the variance in **9
  dimensions**, from 17,305 tracked chromatophores (Reiter et al. 2018,
  PMID 30333578).
- The array **grows a hundredfold** — a few thousand units in a hatchling to a few
  million — inserting new units daily into a stretching sheet while holding the
  light:dark ratio at 1.06 ± 0.19 : 1 across animals from 8 to 252 days old. No
  engineered display has to solve this and none does.

That last one is, we think, the most transferable idea in the whole space, and it
has the least engineering competition.

**The optical study is the one that produces something a builder can use, and
it splits a question people usually conflate.** Freezing the iridophore stack
costs 88% of the achievable chromaticity area, so the multilayer is what
*provides* the colour — but widening its measured 425–675 nm tuning range buys
**1%**, while raising the reflectin refractive index from the live-cell mean 1.405
to the measured maximum 1.44 buys **68%**, and a nearly transparent retracted state
buys **61%**. The layer that provides the gamut and the layer that limits it are
not the same layer. A synthetic version should spend its effort on index contrast
in the reflector and on a pigment actuator with a genuinely transparent off-state,
and not on a wider tunable range. Two side-findings came with it: removing the
leucophore costs nothing in chromaticity but drops peak luminance from 12 to 2.2,
so it is a brightness layer and not a colour layer; and **removing the yellow
pigment class makes the gamut bigger**.

**Study 3's result, and where the real animal sits on it.** With motor units at
the measured size of nine actuators, the diminishing-returns knee is at **579
channels** over a 4 x 4 mm patch of 3,904 actuators — about 36 channels per mm², or
one channel per 6.7 actuators. **Quote that as "between 306 and 1094, nearest grid
point 579", not as "579 ± 0".** The standard deviation across 30 runs really is
0.0, and it is a **grid artefact**: the channel count is swept on a 14-point
logarithmic grid, so a knee can only land on a grid point and all 30 landed on the
same one. What the agreement shows is that the knee is stable to within one grid
step — a weaker and true statement. The field `why_the_spread_is_zero` carries this
wherever the number goes.

**The animal is past the knee, by 2.78×.** Renard et al. 2026 resolved **754**
putative motor units driving **1,829** chromatophores. Those two counts are the
measurement; the ratio is ours — **754/1829 = 0.412 channels per actuator** is a
quotient we computed, not a figure the paper prints, and the page should not cite
it as though Renard published it. On our patch that is 1,609 channels against a
knee of 579, and it reaches 99–101% of the fidelity one channel per chromatophore
would give. So a cuttlefish is not economising on motoneurons: it carries nearly
three times the channel count the diminishing-returns point calls for, on these
targets and under our assumed observer acuity.

**What no channel count rescues: the per-target ceilings.** At the measured unit
size of nine, each target has a ceiling the array cannot pass however many channels
drive it. Measured at full channel count, n = K = 3,904 — more than twice what the
animal has — compact wiring, mean over five seeds:

| target | ceiling at n = K |
|---|---|
| edge | 0.9708 |
| square | 0.9611 |
| stripes_coarse | 0.9578 |
| mottle | 0.9503 |
| gravel_1f | 0.8970 |
| stripes_fine | 0.6439 |

**Define the ceiling as the value at n = K, not as the maximum anywhere in the
sweep**, and say which you mean: the two differ by up to 0.0054 (gravel_1f 0.8970
against 0.9024; stripes_fine 0.6439 against 0.6485) because a mid-sweep seed can
sit higher by chance. The n = K reading is the honest one for the claim it
supports, since the point is that saturating the channel count does not rescue fine
detail.

**140 rows are excluded from these means and must be**, out of 560 at m = 9
compact: the two uniform targets have zero spatial variance, so R² is undefined and
is returned as `null` rather than as a vacuous 1.0. Every one carries
`r2_undefined_zero_variance_target`. 140 = 2 targets × 5 seeds × 14 grid points. A
recomputation that does not filter them raises `TypeError` on `int + None`; one that
coerces them silently gets a different answer.

**The coverage hypothesis holds only for small units.** knee ÷ (K/m) is 1.00, 1.31,
1.33, 1.87 and **5.41** for unit sizes 1, 3, 9, 14 and 30. Below about 14 actuators
per unit the channel budget is set by covering the array at all; above it, the
pattern's spatial detail starts to bind instead.

**That last one is study 1's weak number reappearing as a design constraint in
study 2, and the cross-reference is the point.** The only sourced expansion ratio
is 2.55×, which is a startle response rather than a measured maximum. Feed it
through the coverage model and a *retracted* chromatophore still covers **52% of
the skin**. So every pigment layer is a permanent optical loss even when it is
off, and a layer whose absorption does not pay for that floor is worth deleting.
The single weakest measurement in the actuator study is therefore also what caps
the optical one, and a reader who only saw study 2 would read that 52% as a
modelling choice rather than as a consequence of a number nobody has measured
properly.

**Be clear about what our own models add.** They are honest about their own
weakness and they mostly deliver *negative* results: adding radial muscle fibres
buys almost nothing, widening the reflector's tuning range buys 1%, and the
kinetics model does not reproduce the measurement it was tested against. Negative
results are the useful part of a design space, but they are not progress on
building anything.

---

## 2. The one specific question: did the actuator control arm reproduce the
## measured expansion ratio and time constant?

**No. The control arm failed, and on re-reading the source it failed by more than
the file originally said. We did not tune it until it fit.**

`actuator-mechanics.json` fits exactly **one** parameter — the sacculus shear
modulus *G* — to exactly **one** measured number, the steady-state area ratio
**2.5506×** (from "+155.06% mean surface-area increase", so 1 + 1.5506 = 2.5506;
Hadjisolomou et al. 2021, PMID 34220538, *Doryteuthis pealeii*). Rise time is then
a free prediction.

| quantity | model | measured | verdict |
|---|---|---|---|
| area ratio | 1.73 peak | 2.5506 | **fitted at steady state, then broken by the damping fit** |
| rise time | 232 ms | **67–83 ms** (expansion phase) | **2.8–3.5× too slow** |
| retraction ÷ expansion | 1.27 (damping fitted to it) | **1.34** and **3.70** | **reached, but it costs 32% of the expansion ratio** |

**The comparator was wrong, and correcting it made the failure worse.** The file
originally scored the model's 215 ms rise against Hadjisolomou's rise time *tRt* of
117–150 ms. Table 1 of that paper (read in full text via PMC8250766) timestamps
*tRt* **from the flash**, so it contains the 50–67 ms response time *tR* — a
sensory and neural latency the model does not simulate, since its clock starts at
drive onset. The right comparator is the expansion **phase**, *tRt* − *tR*: 67 ms
(head/arms), 67 ms (fin), 83 ms (mantle). Against *tRt* the model was 1.4–1.8×
too slow; against the expansion phase it is **2.6–3.2×** too slow. The old numbers
are kept in the file under `control.SUPERSEDED_2026_11_02`.

**The asymmetry, and a claim of mine that was wrong.** Decomposing Hadjisolomou's
Table 1 per region — expansion phase = *tRt* − *tR*, retraction phase =
*rD* − (*tRt* − *tR*) — gives:

| region | expansion phase | retraction phase | retraction ÷ expansion |
|---|---|---|---|
| head/arms | 67 ms | 233 ms | 3.48 |
| mantle | 83 ms | 301 ms | 3.63 |
| fin | 67 ms | 267 ms | 3.99 |

Mean **3.70**, against Renard et al. 2026's **1.34** (contraction 5.90 ± 3.50 vs
expansion 4.41 ± 1.91 frames at 20 fps, *Euprymna berryi* and *Sepia officinalis*).
**Both exceed 1: retraction is slower than expansion.** There is no sign
disagreement between the sources; an earlier version of this file said there was.

**An earlier version also said a lumped elastic recoil was *structurally* incapable
of retraction slower than expansion, because no damping in the sweep crossed 1.0.
That was wrong, and wrong for a reason worth keeping.** The sweep ran from
c = 10⁻⁹ to 3.2×10⁻³ N·s/m and its maximum asymmetry sat **at its own upper
boundary** — which is precisely the condition under which "no value reaches X"
cannot be claimed, and I claimed it anyway. Extending the sweep to c = 10 shows the
asymmetry crosses 1.0 at **c = 0.1**. The model can reach either measured
asymmetry comfortably.

**Only the crossing point is quotable, and the distinction matters.** Above
c ≈ 2 the organ no longer returns 90% of the way within the 6 s simulation window,
so the sweep's *maximum* asymmetry is set by the window rather than by the physics.
It moved **4.5×** — 2.946 to 13.27 — between two versions of the *same correction*,
purely because the window was lengthened from 1.2 s to 6 s. It must not go in prose.

**The crossing did not move at all.** It is 0.1 under the 1.2 s window, 0.1 under
the 6 s window, and 0.1 after the NaN-filter fix. A quantity stable across three
different runs of the machinery is a property of the model; one that moves with the
machinery is a property of the run. `control.damping_sweep_reach.quotable` now says
not only which number is safe but why, and records that the safe one held while the
unsafe one quadrupled.

`control.damping_sweep_reach` records `extremum_at_boundary` on every run, so the
condition that invalidated the original claim is checked rather than assumed — and
**that guard was itself broken on its first version.** It filtered the sweep rows
with `if r["asymmetry..."]`, and **NaN is truthy in Python**, so the rows where the
organ never returned were never removed; the maximum was then compared against a
NaN and the guard reported the reassuring `false`. A gate that is off looks exactly
like a gate that passed, inside the gate written to stop that happening. It now
filters on `math.isfinite` and reports how many points failed to return.

**What is actually true is weaker, and is still a clear failure.** It is a
three-way incompatibility, not an impossibility. `control.joint_feasibility`:

| setting | peak area ratio (meas. 2.55) | 90% rise (meas. 67–83 ms) | asymmetry (meas. 1.34 / 3.70) |
|---|---|---|---|
| low damping | 2.06 | 215 ms | 0.49 |
| damping fitted to Renard's 1.34 | **1.73** | 232 ms | 1.27 |
| damping fitted to Hadjisolomou's 3.70 | **1.38** | 244 ms | 3.94 |
| 2 s drive, to recover the expansion | 2.18 | **1,674 ms** | 1.38 |

Two parameters are fitted to two measured quantities — stiffness to the
steady-state expansion ratio, damping to the asymmetry — and **the two fits are
mutually inconsistent**: at the damping that reproduces the asymmetry, the peak
expansion collapses 32% below the ratio the stiffness was fitted to. The one
genuinely free prediction, the rise time, fails by 2.8–3.5×. Recovering the
expansion magnitude on top needs a 2-second drive and a 1,674 ms rise — twenty
times the measured expansion phase, against a whole response that completes in
under 400 ms.

**This model is a one-constraint model being asked to meet three.** The next
version needs a mechanism that slows retraction *without* loading expansion — a
viscoelastic sacculus whose stress relaxes during the hold, or an active brake —
rather than more of the single knob this one has.

**The abstract invites the opposite conclusion, and that trap is worth naming.**
Hadjisolomou's abstract says "The response duration ranged from 217 ms (fin,
retraction) to 384 ms (heads/arms, expansion)", which reads as expansion being
slower than retraction. It is a minimum and a maximum across **two different
response populations and two different body regions**: 4,000 chromatophores in 166
trials that *expanded* to the flash, and **65** chromatophores in 19 trials that
*retracted* — an *n* differing by 60×. Region-matched, those whole-event durations
do all have the retraction response shorter (0.65–0.89), but a whole-event duration
of a retraction-type response is not the retraction phase of an expansion event,
and the two must not be compared. The same caution applies to the 155.06% and
40.46% magnitudes: they are peaks of those two separate populations, not
non-inverse phases of one event, and they are **not** evidence that the organ fails
to return to baseline — *rD* is defined as running to "the return to the pre-flash
state following the peak response".

**Why the parameters are so bad.** 5 sourced / 13 assumed / 1 nondimensional. Every
muscle property is an explicit **proxy** from *Doryteuthis pealeii* mantle circular
or funnel retractor muscle, because nobody has measured the contractile properties
of a chromatophore radial muscle. The sacculus shear modulus has never been measured
at all — it is the fitted parameter. The folklore "~7× diameter / ~50× area"
expansion figure was deliberately **not used**: the previous agent traced it to a
secondary teaching page citing Cloney & Florey 1968 and could not reach a primary
source. We agree and did not use it either.

**Three animals, not one.** The fit and the rise-time score are *Doryteuthis
pealeii*; the asymmetry comparison adds *Euprymna berryi* and *Sepia officinalis*;
the muscle proxies are a different tissue in *Doryteuthis*. `species_of_evidence`
in the result file says so, and every route in `routes.json` carries the same field.

## 3. Sourced-to-assumed ratios, reported as they are

| study | sourced | assumed | nondimensional |
|---|---|---|---|
| actuator-mechanics | 5 | 13 | 1 |
| optical-gamut | 9 | 8 | 1 |
| control-channels | see its own `parameter_counts` | | |

**The ratio is bad and it should be.** The one study where it is respectable —
the optical gamut — is respectable because the iridophore Bragg stack is the
best-measured object in this design space: layer count, both refractive indices,
both thicknesses and the full tuning range are published numbers from **live**
cells (Ghoshal et al. 2013, PMID 23740489, read in full text via PMC). Everything
about the pigment layer in the same study is assumed, because no measured
absorption spectrum for any cephalopod ommochrome was found.

---

## 4. Controls that failed, and what we did about them

We ran twelve declared controls across the three studies: one control arm in the
actuator study, four in the optical gamut, and seven in control-channels. **Three
failed.** All three are in the result files with `passed: false` and none was
quietly dropped. The exact tally is recomputable — each study's `controls` block
lists them with their verdicts.

**(a) `reproduce_published_tuning` — the failure is in the source.**
Ghoshal et al. 2013 state the tuning excursion as "*ca* 150 to 80 nm" for the
high-index lamellae and "*ca* 120 to 50 nm" for the inter-lamellar spaces, for a
measured peak moving 675 → 425 nm. Taking those four numbers literally with the
paper's own n_L = 1.34 and mean n_H = 1.405, the first-order Bragg condition
λ = 2(n_H d_H + n_L d_L) gives **743 nm and 359 nm**, not 675 and 425. No constant
index pair satisfies both endpoints: matching 675 nm at d_H = 150 needs n_L = 1.06,
and matching 425 nm at d_H = 80 needs n_L = 2.0. The quoted excursions are
evidently rounded. We therefore drive the model from the **measured peak range**
and hold the live-cell thickness ratio, rather than from the quoted endpoint
dimensions. The live-cell averages are internally consistent: d_H = 120, d_L = 95
give 592 nm, a green, inside the range.

**(b) `coverage_law_vs_exact_union` — our law is biased, and in the direction
opposite to what we wrote down first.** `1 − exp(−s)` under-estimates coverage by
**16% relative** when retracted and 8% when fully expanded, against an exact
rasterised disc union at 4× resolution. The prediction recorded in advance was that
a Poisson-**disc** array overlaps *less* than a Poisson one, so the law would
*over*-estimate. It under-estimates, because a hard-core array wastes less of its
disc area on mutual overlap and therefore covers *more*. The wrong prediction is
kept in the file rather than edited out. `coverage_law_sensitivity` then re-ran a
channel sweep under a law rescaled to the exact union: **the knee did not move**
(512 either way; max R² difference 0.061), because the declared metric scores a
target already mapped into the skin's own achievable range, so a uniform bias
largely cancels.

**(c) `tmm_vs_quarter_wave_closed_form` — failed first, and the error was ours.**
The transfer matrix disagreed with the closed form by 0.033. Reading it showed the
**closed form** was wrong: the admittance had been written as
(n_H/n_L)^2N · n_H²/(n_in n_L) instead of (n_H/n_L)^2N · n_out. Fixed, they agree
to 4e-16. It is recorded in the file as having failed first, because a control that
is itself wrong is precisely the failure this check exists to make visible.

**Two controls caught bugs that would have shipped as results**, and both are in
`control-channels`:
- The first optimiser used a globally normalised gradient, whose per-parameter step
  falls as 1/√N. It scored R² = 0.115 at one channel per actuator against a
  deconvolution baseline of 0.955. Replaced with Adam.
  *An earlier version of that control used a blur-ignoring direct synthesis that
  itself scored 0.0 — which the broken optimiser would have **passed**. The
  baseline was replaced for that reason.*
- `renard_like` wiring scored **0.0000** at N = K against 0.8169 at N = 1024 —
  more channels, worse result. Nine memberships per actuator started the array
  fully saturated, where the clamp has zero gradient. Fixed with a straight-through
  estimator and a membership-aware initialisation; `control_monotonicity` is the
  check that catches it and it is shipped.

**A fifth bug, and the most expensive thing that happened here: a completed
63-minute sweep thrown away unwritten.** The control functions had been *appended*
to `control_channels.py` after its `if __name__ == "__main__": main()` guard, so
`main()` ran before they existed. Nebius job `aijob-e00mz387dqe1bm2y5x` computed all
11,200 cells in 3,767 s and then died on the next line with `NameError: name
'run_controls' is not defined`, having written nothing. Two fixes: the guard is at
the end of the file, and — the one that matters — `main()` now **emits the sweep
before the controls run**, with the controls wrapped so a failure there is recorded
as a failed control instead of taking the sweep with it. Verified by stubbing
`run_controls` to raise deliberately: the sweep was emitted first and survived. The
rule is general and cheap: *commit an expensive result before letting anything
cheap run on it.* The lost run was redispatched as `aijob-e00rw4rhda4heq0xs5`.

**A fourth bug that no control caught, because it was in the figures.** Captions
were placed at a hand-guessed `y` with `va="top"` and a hand-guessed
`tight_layout(rect=...)`. Whenever the text wrapped to one more line than the
guess allowed, the last line ran off the bottom of the image and was simply gone —
in four figures, each time silently, and each time the *lost* line was the one
carrying the caveat rather than the claim. The fix is `figure_caption` in
`code/common.py`, which counts the wrapped lines and computes the space from the
figure's own height. Worth recording because the honesty rules here are all about
what a caption says, and a caption that is not fully rendered says something
different from the one that was written.

And one bug caught by a control that was *not* about it: the array generator
stopped Bridson sampling at the target count, which leaves the far corners of the
patch empty. The point **count** was exactly right (3904 of 3904), so nothing in
the summary statistics showed it; `array_uniformity` showed local coverage falling
to 7e-4 of the mean.

---

## 4b. Two rules, both learned the same way

### Rule: never hand-edit a generated file

**A hand-edit to a generated JSON is a correction with a timer on it.** The next
re-run silently reverts it and nothing fails. That happened here: the actuator
control-arm correction was first made by editing `actuator-mechanics.json`
directly, and the regenerating script still held the old constants, so one
`python3 code/actuator_mechanics.py` would have erased it without a word.

It was already worse than that before anyone re-ran anything. The JSON carried the
new comparators while `figures/actuator-datasheet.png` was still *drawing* the old
ones, because the figure reads module constants rather than the file. A reader
comparing the picture against the text would have seen two different studies and
had no way to tell which was current.

**The fix is to move the fact, not the conclusion.** Hadjisolomou's Table 1 is now
transcribed into `code/actuator_mechanics.py` as `HADJI_TABLE1`, and the expansion
phase, the retraction phase, the asymmetry, the headline, the control block, the
datasheet row and the figure's comparison bars are all *derived* from it. They
cannot disagree again, because there is only one place the number lives. If a
generated file is wrong, fix the generator and re-run; if that feels like too much
work for one number, that is the moment the timer gets set.

### Rule: a guard ships with a case it must flag, or it ships off

Three failures in one afternoon, and the common factor is not carelessness:

| failure | what it cost |
|---|---|
| damping sweep's maximum at its own boundary | a published claim of structural impossibility, wrong |
| `selftest()` appended after the `__main__` guard | a self-test reported as passing that could not run |
| NaN truthiness inside `extremum_at_boundary` | the guard written to prevent the first one, silently disabled |

**Every one of them was a check with no positive control.** None had ever been
shown to go red. The counter-example is the layout guard, and it held — because the
reviewer copied the file out, appended a `def` after the guard, and watched it
raise. That is the difference.

**The NaN one is worth stating at the level of the language**, because it is this
project's oldest lesson arriving as IEEE-754. `bool(float('nan'))` is `True`, so a
bare truth test keeps every NaN row. Every comparison against NaN is `False` — both
`nan > 5` and `nan < 5` — so `abs(amax - nan) < 1e-12` is `False`, which reads as
*"the extremum is not at the boundary"*: the reassuring verdict, whatever the data
says. And `max()` is order-dependent with a NaN present — `max([1,2,nan,3])` is
`3`, `max([nan,1,2,3])` is `nan` — so whether the NaN surfaced at all depended on
row order. **The guard was not merely wrong; it was incapable of returning the
alarming answer.** A search whose domain excludes the answer looks exactly like a
search that found nothing.

With the filter fixed, `extremum_at_boundary` is **`true`**: 3 of 41 points never
return within the window, and the maximum sits at the last finite point. The
earlier `false` was never a measurement.

### Rule: send the range and the extremum, not the verdict

This one is about what passes between two people, and it came out of the damping
error. I told the reviewer "no damping in a 27-point sweep crosses 1.0". They
endorsed it, called it the page's most interesting sentence, and relayed it onward
as a structural refutation. It was wrong: the sweep's maximum sat at its own upper
boundary, and extended two decades further the asymmetry crosses 1.0 easily.

The reviewer's share of it was not asking what the sweep's domain excluded. Mine
was larger and is the transferable half:

> I handed you a conclusion rather than the table, and a reviewer can only check
> what they are given. The fix on my side is to send the range and the extremum,
> not the verdict.

**The rule that follows: "no value reaches X" is not a statement at all until the
searched range is given and the extremum is shown to be interior to it.** An
extremum sitting at a sweep's own boundary is the most recognisable tell there is,
and it is invisible to anyone who receives only the conclusion.

`control.damping_sweep_reach.extremum_at_boundary` is that rule in mechanical form,
and it is reported on every run so the condition travels with the number instead of
staying in the author's head.

**A qualitative claim that resists being made numeric is often resisting because it
is not true.** This error was found by trying to make the refutation *stronger* —
by reporting the sweep's maximum as a number — and the act of quantifying it
revealed the maximum was the boundary. That is worth doing deliberately: before
publishing a negative, try to put a number on it, and treat difficulty in doing so
as evidence rather than as an inconvenience.

### Rule: a prose claim about your own data must be bound to the data

Three times in one afternoon a sentence quoted one of our own numbers that a
result file had since recomputed, and nothing failed:

| claim | where it lived | what the data said |
|---|---|---|
| 8 → 9 lamella pairs buys "13%" of gamut | `routes.json` | 15% |
| devices compared against "117–150 ms" as an actuator time | `routes.json`, two routes | from-flash, containing 50–67 ms of latency the model does not simulate |
| "about fifteen routes" downstream of the transgene step | `NOTES.md` and `routes.json` | ten |

The shape is identical every time: **a prose claim about our own data, sitting in a
different file from the data.** Code has callers. A number in a JSON has whatever
recomputed it. A sentence has nobody.

`code/check_claims.py` is the instrument. Each claim binds a literal string that
must appear in a named file to a function that recomputes the value it asserts, so
**either side drifting is a failure** — stale prose fails as a wrong number, deleted
prose fails as missing text. It currently carries 14 claims and passes.

Three things about it are deliberate and worth copying:

1. **It is a hand-maintained table, not a number scraper.** A scraper over every
   numeral in these files would flag hundreds of legitimate citations of other
   people's measurements, and a check with that false-positive rate gets switched
   off.
2. **It matches on normalised text.** Its own first run reported "52% of the skin"
   MISSING from `NOTES.md` when the file said exactly that, with a line break
   between "of" and "the". Whitespace and Markdown emphasis are collapsed before
   matching; the number and the wording still have to be right.
3. **It has a self-test, because a check whose subject includes the check is not a
   check.** `selftest()` perturbs a result value, then deletes a claim's prose, and
   requires the checker to fail in each case before accepting a clean run. Arms 1
   and 2 go red as intended; arm 3 caught a genuinely stale claim on its first real
   run, which is the tool working rather than a defect in it.

**The self-test was unreachable for its first two versions, and that is the point
of recording it.** `selftest()` was appended *after* the `if __name__ ==
"__main__"` guard, so the file as shipped could not run it and `--selftest` was
parsed by nothing — the identical mistake that had, an hour earlier, discarded a
completed 63-minute sweep by appending `run_controls` after that file's guard.
Having just written the lesson up did not prevent the repeat. So it is enforced
structurally now: `assert_entrypoint_guard_is_last()` parses the file's own AST and
raises if anything is defined after the guard, and it runs before every invocation.
**Its positive control was supplied by the reviewer, not by us** — they copied the
file to their own scratch, appended a trivial `def` after the guard, and got an
`AssertionError` before any claim was evaluated. A positive control from someone
other than the author is worth more than one from the author, and we had not
thought to write it.

**It also found a gap rather than an error**, which was not what it was built for:
`NOTES.md` did not state the optical gamut's central result at all. The claim for
"costs 88%" failed as missing text, and section 1 now carries the finding.

## 5. The PMID field, and what is deliberately empty

Much cephalopod optics and soft-robotics literature sits in physics, materials and
engineering journals that PubMed does not index. Where a source has no PubMed
record, **the `pmid` field is absent** from the evidence item and a DOI or URL
carries the citation instead. In the shipped `routes.json` this happens exactly
once — an E Ink product page — and the validator lists it explicitly rather than
letting it pass silently.

**Two sources recorded in the earlier survey as having no PMID in fact have one.**
The Rogers optoelectronic camouflage sheet is **PMID 25136094** and the Whitesides
microfluidic soft-machine skin is **PMID 22904008**. We found and verified both, so
those are now abstract-level PubMed reads rather than search-summaries. The lesson
is small but worth recording: "not in PubMed" was an untested assumption about
where a paper lives, not a search result.

### Method recommendation: generate citations, never type them

**Copy this.** Every `cite` string in `routes.json` is composed at build time from a
bibliographic record stored in `lit/library.json`, fetched from NCBI esummary by
`lit/fetch_esummary.py`. `code/build_routes.py` supplies only a PMID and a
read-level; the validator fails the build if a cited PMID is absent from the
library. In one afternoon that caught **three** real errors that every form of
review would have passed, because a wrong citation looks exactly like provenance:

1. **A fabricated-shaped author list.** The tilapia transparency paper was typed as
   "Klaassen/Chen"; it is **Liang G, Lu B, Dai S et al. 2025, N Biotechnol
   89:163-176** (PMID 40752587).
2. **A wrong first author.** PMID 24006348 was typed as Mäthger; the record says
   **DeMartini DG et al.**
3. **A wrong species, with downstream consequences** — see below.

A hand-typed citation that is wrong in the author field survives review precisely
because nobody re-derives it. Generating it from a stored record closes the hole
permanently, and costs one function.

### And the species error, which was not a tidy-up

PMID 36594460, "Molecular characterization of cell types in the squid", is
***Loligo vulgaris***, not *Euprymna berryi*. We had written the promoter-mining
route as "the published *Euprymna berryi* cell-type atlases", which reads as a fact
and which nobody re-checks. **It creates a real obstacle**: neither published
cephalopod cell-type atlas is in the species that has the germline route. The
cell-type atlas is *Loligo vulgaris*, the nervous-system atlas is a bobtail squid,
and the only heritable knockout line is *Euprymna berryi* — so a promoter mined
from one animal must be demonstrated in another before any downstream route works.
That is a concrete reason the ten-route subtree below the transgene step is further
away than it looks, and it is visible to any reviewer with one click. It is now
carried on `gen-find-the-promoter` itself.

To stop this recurring, **every route carries `species_of_evidence`**, and the
validator lists the distinct species cited. The page would otherwise silently merge
a cuttlefish, a bobtail squid, two loliginid squid and an octopus into one organism
— which is exactly what the actuator study was doing when it scored a *Doryteuthis*
fit against a *Euprymna*/*Sepia* asymmetry.

**Every citation string in `routes.json` is generated, not typed.** A first draft
wrote the tilapia transparency paper out by hand as "Klaassen/Chen"; it is **Liang
G, Lu B, Dai S et al. 2025, N Biotechnol 89:163-176, "Creation of colorless
transparent tilapia using CRISPR/Cas9 mediated multi-gene mutation"** (PMID
40752587). That draft was discarded. `lit/library.json` now holds 99 verified
bibliographic records fetched from NCBI esummary (`lit/fetch_esummary.py`), and
`code/build_routes.py` composes every `cite` from them. All 51 distinct PMIDs cited
in `routes.json` resolve in that library; the validator fails the build if one does
not.

---

## 6. Six routes were written, cut, and then restored

`routes.json` was specified at 25–40 routes and reached 46, so six were cut. That
range turned out to be a floor rather than a cap, and **all six are back**: the file
ships 46. They are kept in `code/build_routes.py` as `NEARLY_CUT` and each carries
an `editorial_note`, because the judgement and its reversal are together more
informative than either alone. The reasons each was nearly cut:

| route | why cut |
|---|---|
| `mol-swap-the-ommochrome` | `proposed`, and under-specified by our own admission: no measured cephalopod ommochrome absorption spectrum exists, so the target hues cannot be stated |
| `org-lamella-pair-count` | `model_only`, and subsumed by the reflectin-index route, which makes the same point with a bigger effect |
| `cell-muscle-coupling-between-organs` | `proposed`; the anatomy is described but the functional consequence is the source's own "could influence" |
| `dev-reinnervation-on-colour-change` | `proposed` hypothesis with indirect support; overlaps the insertion-rate route |
| `syn-microfluidic-dye` | weakest synthetic entry; we could not obtain a response time from the abstract |
| `syn-photomechanical-fluorescent-display` | redundant with the optoelectronic sheet, which carries better numbers |

Nothing was cut for being inconvenient to the argument, and in the end nothing was
cut at all. Re-reading them for restoration, the honest verdict is that the two
`model_only` optics routes (`org-lamella-pair-count`,
`mol-swap-the-ommochrome`) are the weakest things on the page and a reader should
treat them accordingly — which is a better outcome than their silent absence.

---

## 7. What we did not do, and the scope of each negative

- **No measured underwater illuminant.** The gamut is computed under CIE D65. We
  did not find a downwelling spectrum we could read and did not invent one.
  Seawater attenuates red strongly with depth, so a cephalopod's real gamut in its
  own light field is smaller than ours and shifted blue-green. We do not estimate
  by how much.
- **A human observer.** CIE 1931 2-degree. Cephalopods are colour-blind and their
  predators are fish. Gamut area in human u'v' is a common currency, not the
  quantity that matters to either animal.
- **Normal incidence only.** Iridophore reflectance is strongly angle-dependent and
  the lamellae are not parallel to the skin surface. We say nothing about the
  angular gamut.
- **No exogenous actuator has commanded melanosome transport in any vertebrate
  chromatophore**, as far as the previous survey's PubMed search reached. Scope:
  PubMed title/abstract searches on 2026-11-02 for `optogenetic melanophore` (1
  hit), `optogenetic chromatophore` (1 hit), `chemogenetic melanophore` (0),
  `channelrhodopsin melanosome` (0), `channelrhodopsin pigment cell` (15, first 6
  inspected). Preprints, patents, conference abstracts and full-text-only mentions
  were **not** searched. Positive control: the same searches returned
  PMID 30578760, a real optogenetic melanophore paper.
- **No melanosome-level time constant** was found in any abstract read, so the
  vertebrate-versus-cephalopod speed comparison rests on a whole-body teleost
  figure (4.44 s mean, Nassau grouper) against a single-organ cephalopod one
  (117–150 ms). Those are not the same measurement and the comparison is
  correspondingly loose. Positive control: the same searches returned relevant
  papers.
- **We did not survey** octopus papillae, deep-sea bioluminescent signalling, or
  behavioural camouflage in depth, although sources from each are in
  `lit/library.json`.

---

## 8. Compute

The control-channel sweep (11,200 cells: channel count × unit size × wiring ×
target × seed) ran on **Nebius**, job `aijob-e00mz387dqe1bm2y5x`, platform
`gpu-h100-sxm`, preset `1gpu-16vcpu-200gb`, image `python:3.12-slim`, 16 worker
processes. The code is pure NumPy; the H100 preset was used because it was the only
way to get 16 cores. Everything else ran locally under
`systemd-run --user --scope -p MemoryMax=6G -p MemorySwapMax=0 -p TasksMax=256 nice -n 19`.

`--volume s3://morphoswarm-designspaces:/output` was **rejected** by the API with
`spec.volumes[0].s3_config.endpoint: value is required`. The endpoint is
`https://storage.eu-north1.nebius.cloud`, but supplying it would not have helped:
the flag's full form is `s3://BUCKET:/path[:MODE[:PROFILE]]` where PROFILE is an
**AWS credentials profile**, so the mount needs an access key and secret for the
Nebius bucket. None exists in this environment, and provisioning one needs tenant
IAM we do not have. So the job emits its result to stdout as gzip+base64 and the
result is recovered from the job logs.

**That channel can truncate silently, so it is checked.** A log that is cut short
would decode to a shorter but still well-formed result, and a short result looks
exactly like a smaller sweep. The job prints the base64 length alongside the
marker (`BEGIN_RESULT_B64 len=N`) and `code/fetch_sweep_from_logs.py` **refuses to
write** unless the recovered blob is exactly N characters. That is a length check
rather than a digest: the job did not print a sha256 of its own payload, and we did
not retrofit one, so a corruption that preserved length would not be caught. The
decoded row count is reported beside every number taken from it.

---

## 9. File map

| file | what it is |
|---|---|
| `routes.json` | 40 routes across 8 scales, with a computed validation block |
| `actuator-mechanics.json` | study 1 — the chromatophore as a muscle. **Control arm failed.** |
| `optical-gamut.json` | study 2 — pigment over a tunable Bragg reflector |
| `control-channels.json` | study 3 — how many channels, and where the knee is |
| `index-fragment.json` | the three studies, with authored alt text and captions |
| `code/` | every model, every control, and the routes builder |
| `lit/library.json` | 99 verified bibliographic records |
| `data/` | CIE 1931 2-degree CMFs and CIE D65, from the CVRL database |
| `figures/` | all figures; every caption opens by saying what the picture is |
