# Can a zebrafish be engineered to fly?

**No. And the interesting part is how precisely no, and why two unrelated attempts fail for
different reasons.**

This is the top-level account. Every number below is recorded in the project graph with its
evidence level and source; the [subproblem board](../library/pages/project/board.md) shows what is
open and what each question is blocked on.

---

## The answer in one table

| | Required | Available | Short by |
|---|---|---|---|
| Water-exit speed | 4.37 m/s | 0.45–1.38 m/s *measured* | **3.2×** *(vs the fastest of 50 fish; 9.7× vs the slowest)* |
| Launch kinetic energy | 3.82 mJ | — | **10×** |
| Tail-beat for a taxi | 132–199 Hz *(contested: see below)* | 52 Hz *measured* | **2.5–3.8×** *(or 1.4–1.6×)* |
| Pectoral muscle fraction | 7.5–20% | 1.4% *measured* | **5–15×** |
| Muscle energy per stroke (spring route) | 98.5 J/kg | 32–81 J/kg *measured spring-loading work* (mean 53) | **1.2–3.1×** |

:::{caution} The tail-beat row rests on a contested regime assignment
The 132–199 Hz figure comes from applying the Strouhal numbers of **small, low-Reynolds swimmers**
— goldfish **0.54 at Re 7.1×10³**, tadpole 0.79 — on the argument that a 4 cm zebrafish is that
case. A recovered replication recomputes Eloy's `St_opt = 0.75·Li^(1/3)` **at the taxi operating
point** and gets St ≈ 0.30–0.34, hence **72–83 Hz** and a **1.4–1.6×** shortfall.

**Both arithmetics are correct.** Checked here: St 0.54 → 131.6 Hz and St 0.30–0.34 → 73–83 Hz,
reproducing each side exactly. The dispute is entirely *which Strouhal applies*.

**And the operating point is not where the borrowed value was measured.** A 4 cm body at 1.95 m/s
in water is **Re ≈ 7.8×10⁴**; even the caudal lobe alone is ≈2×10⁴. The goldfish value was taken
at **7.1×10³**.

**Settled against claim 52 by this project's own law library.** `library/laws/strouhal.yaml`
declares `domain_of_validity: reynolds_min: 1.0e4`. The taxi point sits **inside** that domain.
The goldfish (0.54, Re 7.1×10³) and lungfish (1.02, Re 7.0×10³) figures claim 52 borrowed are
listed under `where_it_breaks` and are **below the law's own stated minimum** — so the claim
applied out-of-domain exceptions to an in-domain case.

The same file also gives Eloy's relation as `Li = (S/h²)·C_d/**2**`. The replication wrote it
without the `/2`, which would scale its St by 0.794 — to **0.24–0.27**, further into the band and
further from 0.54. **Both corrections push the same way.**

**Still not a full re-derivation** — S and h for a zebrafish were not retrieved, so the 72–83 Hz
figure itself is unverified. What is settled is that the 132–199 Hz figure rests on values the
project's own law file places outside the applicable regime.
:::

:::{warning} Corrected 2026-11-04 — the last row's arithmetic did not work
It read *"98.5 J/kg | **8.6 J/kg** delivered | 1.9×"*, and 98.5 / 8.6 is **11.45**, not 1.9.

**Both numbers were right; they came from different comparisons.** Claim 227 states a **11.5×**
gap against the 8.6 J/kg the muscle *"effectively delivers today"* **and** *"54–82 % of need"*
against the 53–81 J/kg spring-loading work. The table took its Available cell from the first and
its ratio from the second. A row about the **spring route** needs the spring comparator, so the
1.9× compares the requirement against the *best measured spring-loading work* — frog, 53–81 J/kg —
which claim 227 states as supplying *"only 54–82 % of need"*. That reproduces: 98.5/53 = 1.86 and
53/98.5 = 53.8 %.

8.6 J/kg is a different quantity that belongs elsewhere in the argument, not opposite a ratio
computed from a different comparator. Anyone checking the table's arithmetic — which is the first
thing a sceptical reader does — would have found it off by a factor of 6 and been right to
distrust the rest.
:::

The best design buildable from **demonstrated** alleles is the zebrafish that already exists — the
Daane *lat4a^nr21/+; kcnh2a^lof/+* double heterozygote. Granting it an unmeasured one-body-length
wing, it produces **10% of body weight in lift at launch** and lengthens a 19.4 cm ballistic leap by
**3–6 mm**.

**The honest deliverable is a possibly detectable ~5–7% reduction in ascent deceleration — ~6%
net.** Not flight, not a glide, not a meaningfully longer leap. Calling it flight would destroy the
credibility of everything else here.

:::{warning} Corrected 2026-11-04 — this read "5–10 %", and the 10 % was geometrically wrong
A recovered replication caught it. **Lift acts perpendicular to the flight path**, so on a 45°
leap its vertical component is `L·cos 45° = 0.707 L`. A lift/weight ratio of 10 % at exit therefore
buys **7.1 %** of vertical reduction, not 10 % — and ~**6 %** once wing drag is included. The
10 % upper end treated full lift at a 45° climb as though it acted vertically.

Two further conditions the figure carries and the sentence did not: it is for the **designed
196 mm² wing**, not any measured Daane fin (40–80 mm² fins give ~1–3 %), and it is **~0 for a
vertical leap**, where cos θ → 0.

The lift ratios themselves (10 % at exit, 5 % at apex) **replicate exactly**. Only the projection
onto the vertical was wrong.
:::

---

## Why the negative is worth more than a maybe

Two **independent representations** were tried, and they fail on **different terms**:

1. **Build a better wing** — more span, more area, stiffer rays. Fails on **lift and launch speed**,
   by ≥10× on energy.
2. **Store the launch energy** — latch-mediated spring actuation, the mechanism fleas, froghoppers
   and mantis shrimp use to beat muscle power limits by orders of magnitude. Fails on **muscle
   energy per stroke**, by 1.9×.

The second route *removes the power wall entirely*: spring volume needs only **1–4% of body volume**,
and the required 7400–18400 W/kg sits **within measured insect LaMSA** (36,000–74,000 W/kg). It
still fails, because break-even needs essentially **all skeletal muscle loading one spring in a
single stroke**.

**When two unrelated framings hit a wall, the wall belongs to the problem.** Changing
representation moved the shortfall from **≥10× to 1.9×**, so the reframe was right even though it
still failed.

:::{danger} That conclusion was then refuted, and the refutation is the better result
**Superseded by S30.** The claim above continued *"the barrier is a property of single-impulse
launch from water at this size"*. **The sign is wrong**, and so is the framing.

Required specific energy scales as **m^0.36–0.53** (measured in exocoetids, Fish 1990), while
single-stroke LaMSA supply per kg is **size-independent** (Sutton 2019). Since the exponent on
demand exceeds the exponent on supply, the budget closes as mass **decreases**. The crossover is an
**upper** bound at **m\* = 39 mg**, which makes a 0.4 g zebrafish **~10× too LARGE** for
single-impulse launch, not too small.

:::{note} The Sutton citation checked, 2026-11-04 — sound, with one scope caveat and one missed bound
Resolved via PubMed to Sutton, Mendoza, Azizi, Longo, Olberding, Ilton & Patek,
*Integr Comp Biol* 59(6):1609–1618, [doi:10.1093/icb/icz145](https://doi.org/10.1093/icb/icz145).
The size-independence premise is supported: the abstract states that length–tension properties
limit spring-actuated systems to **one third** of the work a muscle could produce, and muscle work
per kg is itself size-independent, so LaMSA supply per kg is too.

**The m\* = 39 mg crossover above is this project's own**, derived from the exponent comparison —
it is *not* the "size related crossover point" the Sutton abstract names, which is between spring-
and muscle-actuated *jumping*. The two are distinct and are not conflated here.

**Scope, stated because the citation does not carry it:** Sutton's subject is jumping animals and
the question of why large ones do not use springs. Applying its size-independence result to
**water exit in a fish** is a cross-domain transfer. The underlying muscle and spring physics is
the same, so the transfer is reasonable — but it is an inference this project makes, not a result
the paper states.

**A tighter bound looked available, and it was a double-count.** Sutton's one-third ceiling is
quantitative where the argument above uses only size-independence, which suggested the muscle
requirement is really ~**296 J/kg** — turning a 1.2–1.9× shortfall into 3.6–5.6×.

**It does not hold, and the source settles it.** The figures come from **Mendoza & Azizi 2021,
*"Tuned muscle and spring properties increase elastic energy storage"*, J Exp Biol 224(24),
[doi:10.1242/jeb.243180](https://doi.org/10.1242/jeb.243180)** — muscle stretching its own series
tendon in situ in Cuban tree frogs. These are **measurements of muscle work into a spring**, so
whatever length–tension limit Sutton quantifies is already reflected in them. Multiplying by three
on top counts the same limitation twice.

**But tracing it corrected the row in the other direction.** Mendoza & Azizi measured
**32–81 J/kg, mean 53** — and this table had been quoting **53–81**, i.e. mean-to-max, silently
dropping the low end. The source subproblem S29 states the shortfall as **1.2–3.1×**; the table
said 1.2–1.9×.

**So the spring route is worse than this document has been reporting, not better.** Corrected above.
:::

And the hard reality check forced a reinterpretation rather than a tuning. The scaling predicts no
exocoetid of 3–530 g can reach glide speed in one stroke — and that is what is observed. A **300 g
*Cypselurus* needs 16.4 m/s, exits the water at only ~10 m/s (37% of the kinetic energy), and
taxis** to 15–20 m/s with the lower caudal lobe still immersed.

**So real fish gliders use a multi-stroke launch, and both results above modelled a single
impulse.** The smallest real glider is ~1–2 g needing 4.23 m/s — essentially the same speed the
zebrafish design requires. The difference is not the speed; it is the mode of reaching it.
:::

### The third route, modelled properly, closes it — and validates against a real animal

**S32** wrote the equations of motion for the phase real gliders actually use: body airborne, lower
caudal lobe still immersed, thrust applied over many strokes.

**Thrust passes.** Leaving the water cuts body drag by **816×** — exactly the water/air density
ratio — from 4.6 mN to 8 µN. Lobe thrust exceeds drag 3–40× and **speed genuinely rises**, doubling
in ~10 strokes. S24 had closed this prematurely on tail-beat frequency.

**But the taxi stalls at 2.2–2.9 m/s, 50–65% of the 4.41 m/s glide speed** — and the source puts
the full uncertainty span at **1.9–2.9 m/s**, which this document had not carried. It does not fail to
accelerate; it accelerates to a ceiling below what is needed. From the low-end exit it fails earlier
still, on **weight support** rather than thrust.

The ceiling has a clean form, and the interesting part is what cancels:

```
U_max = f · A_pp · √(c6 / C_D(Re))
```

Measured foil thrust scales with *tail* speed squared, independent of forward speed; drag scales as
U². **Immersed area and body mass drop out entirely.** Only tail speed and lobe drag at Reynolds
number remain.

| | f·A_pp / V_to | lobe C_D | U_max / V_to |
|---|---|---|---|
| zebrafish, Re ~1e4 | 0.09–0.10 | 0.06–0.08 | **0.58–0.68** |
| exocoetid, Re ~3e5 | 0.09–0.10 | ~0.01 | **1.3–1.5** |

**They differ in exactly one quantity.**

**And the model validates against the animal that succeeds.** The same equations reproduce the
exocoetid taxi to 15 m/s, and Deng 2019's 36 W, **only with Reynolds-dependent lobe drag. With a
constant C_D a flying fish could not taxi at all.** So the Reynolds effect is not a fitted excuse
for our failure — it is what makes the model describe the real glider.

That is the strongest form this result can take: **one parameter explains both the success and the
failure.**

**Reopening condition, falsifiable:** an airborne zebrafish lobe beating at **1.4–2.2× its best
measured burst tail speed**, or surface-piercing lobe thrust at Re 1e4 measuring well above the 2-D
foil law.

---

## What is real, and what is not

**Real genetic precedent.** Daane et al. 2021 ([doi:10.1016/j.cub.2021.08.054](https://doi.org/10.1016/j.cub.2021.08.054))
phenocopied flying-fish **fin proportions** in zebrafish by crossing two dominant alleles. Our DOI
check resolves it to *"Modulation of bioelectric cues in the evolution of flying fishes."*

**And the gap that matters:** they measured fin **length** only. **Fin area was never reported**, and
no lift, glide or flight was tested. The physics needs area.

**Two build blockers, found by trying to build it:**

- The symbol `lat4a` **resolves to nothing** in UniProt or NCBI Gene. It is `slc43a2a`
  (GeneID 393221, chromosome 15) — identified from Daane's own chromosome mapping, with four
  positive controls proving the search worked.
- Every UniProt entry for `slc43a2a` is **153 aa** — too short to contain a residue 200, so **the
  T200K substitution is unrepresentable** in the standard references. Only Ensembl GRCz11 carries
  the full-length product: `ENSDARP00000138218` (577 aa) and `ENSDARP00000120945` (571 aa).

  **Both carry threonine at position 200**, which is what the allele name predicts — so the
  substitution is now confirmed against a reference rather than taken from the nomenclature, the
  1-based index convention is established rather than assumed, and the 153 aa UniProt entries are
  demonstrably **fragments** rather than a conflicting annotation. That last point matters for an
  implementer: the two sources do not disagree about the protein, one of them is simply partial.

An implementer working from standard sources **fails twice before designing a guide RNA**.

### And when they get there, the guide RNA is not the tool they expect

**Codon 200 is `ACA`.** Under the standard genetic code the minimum substitution distance from
Thr to Lys is **1**, but only from `ACA`→`AAA` or `ACG`→`AAG`; from `ACU` or `ACC` it is **2**. So
T200K is a **single base change** here: **C→A at codon position 2**.

**That single base cannot be written by a base editor.** C→A is a transversion. Cytosine base
editors make C→T and adenine base editors make A→G — a CBE at this site yields `ACA`→`ATA`, which
is **isoleucine, not lysine**. The edit needs **prime editing or HDR**, despite being one
nucleotide.

This is the kind of thing that is invisible at the allele-name level and decides the bench
protocol. `lat4a^nr21` reads like a point mutation, and it is one; it is just not a point mutation
the cheapest tool can make.

The substitution-distance law is kernel-backed (`Delphi.Genotype.claimed_substitutions_rules_out`,
pinned at commit `ba62f16`), and it was re-derived here against the three instances its own
statement commits to — Phe→Leu 1, Trp→Stop 1, Met→Trp 2 — all of which reproduce, so the code table
used matches the one the kernel checked. The reading frame carries its own control: the CDS is
1734 nt, 578 codons, starts `ATG`, ends `TGA`, and codon 200 translates to Thr.

**What the law does not say**, in its own third named hypothesis: reachability in the code is only
reachability. It does not say the substitution occurred, was favoured, or has the claimed effect.

### The protein scale, measured rather than asserted

Three independent routes now agree that **position 200 of the full-length product is threonine** —
the Ensembl sequence, the query row of the alignment search, and the folded structure. That is the
cheapest possible check on an off-by-one in the edit, and it is the only one available: a guide RNA
aimed at the wrong codon fails silently.

| | |
|---|---|
| PDB70 alignment depth at residue 200 | **0** (474 of 577 positions uncovered; max depth 2) |
| ESMFold2 pLDDT at residue 200 | **97.7** |
| mean pLDDT / pTM (577 aa, MSA-free) | 85.9 / 0.823 |
| window 190–210 vs whole protein | 95.1 vs 85.9 |

**The two rows that look contradictory are the result.** The alignment database has nothing to say
about residue 200, and an MSA-free model folds that exact region at the *highest confidence in the
molecule*. So low alignment depth here does **not** indicate a flexible or disordered region — had
the fold come back weak, the honest reading would have been *the alignment ran out*, and there is
no weak confidence to misread in the first place.

**What this does not license.** pLDDT is the model's confidence in itself, not an accuracy, and
there is no experimental structure for this protein to check it against. It says the model is
internally certain about a fold nobody has measured.

### T200K, folded separately: the fold survives, the effect is confined to the site

| | WT | T200K | Δ |
|---|---|---|---|
| mean pLDDT | 85.95 | 85.83 | **−0.11** |
| pTM | 0.823 | 0.824 | +0.001 |
| pLDDT at residue 200 | 97.7 | 87.7 | **−10.0** |
| window 190–210 mean | — | — | −0.79 |

**The −10.0 at residue 200 is the largest absolute shift anywhere in the protein — 0 of 577
residues move more — and it is 16.0 population standard deviations of the per-residue Δ.** Yet the
global numbers do not move at all.

So the substitution is **tolerated by the fold rather than fold-breaking**, which is the pattern
expected of a **dominant** allele acting by change- or gain-of-function rather than by loss of a
folded product. That is consistent with what `lat4a^nr21` is reported to be — a dominant fin-size
*suppressor*, not a null.

**Three things this does not show, and the first is the one most easily over-read.** A pLDDT drop
at a substituted position is *partly expected for any substitution*, because the local sequence
context changed; the informative part is that it stayed local, not that it happened. pLDDT is not a
stability measure and no ΔΔG was computed — `stab-ddg` turned out to be a binding-interface tool
and ESM-2 was paused platform-side. And nothing here touches transport function or the fin
phenotype.

The comparison carried its own control: the WT model contains **THR** at 200 and the mutant
contains **LYS**, asserted in the analysis, so the two runs demonstrably folded different sequences
rather than the same one twice.

### A second model class, and the control that deflated it

ProteinMPNN — structure-conditioned sequence design — was run on the same WT backbone and asked
what belongs at position 200. Raw result: **lysine rank 14 of 21, probability ≈ 0, against
threonine at rank 2** — a probability ratio of order 10¹⁵. Read alone, that looks like a strong
verdict against the substitution.

**It is not, and the control is the finding.** Lysine's *median* rank across all 577 positions of
this protein is **12**, and **64.8 %** of positions rank lysine at least as well as position 200
does. Lysine is simply a rarely-chosen residue throughout a hydrophobic membrane transporter. And
the model's whole-protein sequence recovery is **32.4 %** — the native residue is top-1 at only
32.8 % of positions — so a single-position disagreement carries almost no evidential weight by
construction.

**What survives:** the top six choices at 200 are **V, T, L, I, M, A** — all small and hydrophobic
— so the site sits in a buried-like environment where a charged residue is locally unusual. That is
weak, independent corroboration of the ESMFold2 result: **two different model classes agree the
site is locally perturbed, and neither says the protein breaks.**

This is what the raw number would have bought without its control: a dramatic-looking 10¹⁵ ratio
reported as evidence, when the same ratio holds at two thirds of the protein.

The parse carried its own control, and needed one: this writer orders `B_iso_or_equiv` at field 12
and `occupancy` at 13, and every occupancy is exactly `1.0` — so a positional parse written for a
standard mmCIF reports a mean pLDDT of **1.0** and looks fine. Reading the `_atom_site.` header
gives 85.9, matching the run's own `plddt_mean` of 0.8595.

### The edit stack: two demonstrated alleles out of eight required slots

**S15** asked for a minimal stack where *every edit is individually demonstrated in zebrafish*.

**Two alleles** produce the fin allometry: `kcnh2a^lof(dt2)` (longfin, cis-ectopic *kcnh2a*,
coordinated fin overgrowth) crossed with `lat4a^nr21/dmh26` (dominant T200K — and notably a fin-size
**suppressor**). Their viable transheterozygote is the published flying-fish-like phenocopy.

That the mechanism is **enlarger + suppressor rather than uniform enlargement** is why the published
result concerns fin *proportions*. The design lever is differential allometry across fins, not
growth of one fin.

:::{danger} The edited gene is not fin-specific, and nothing in this project had asked
`SLC43A2`/LAT4 — the human ortholog of the gene carrying T200K — has three **experimental**
UniProt function statements (Q8N370, entry v169):

- a uniporter for **L-phenylalanine, L-methionine and L-branched-chain amino acids**, which *"may
  control the transepithelial (re)absorption of neutral amino acid in **kidney and small
  intestine**"* (PMIDs 15659399, 30379325, 26305885);
- transport by facilitated diffusion, Na⁺/Cl⁻/pH-independent (PMID 15659399);
- **efflux of 3,3′-diiodo-L-thyronine (3,3′-T2) and 3-iodo-L-tyrosine** (PMID 26305885).

If the zebrafish paralog keeps either role, **T200K is a systemic intervention** — amino-acid
handling and thyroid-hormone-metabolite transport — not a fin-local one. The thyroid link is also
*mechanistically suggestive* rather than merely a side effect, since thyroid hormone drives
zebrafish fin development.

**Scope, and it is the whole caveat.** This is the **human** ortholog. Zebrafish `slc43a2a` has
**no curated function at all** — UniProt returns only the two unreviewed 153 aa fragments, neither
with a FUNCTION comment. Nothing here establishes that the zebrafish gene does any of this. It
establishes that **the question was never asked**, which is precisely what the registry's
pleiotropy-closure law (G2) exists to force.
:::

**Six required capabilities contain no demonstrated zebrafish edit at all:** membrane stiffness,
launch power, aerial stability, vestibular and visual function in air, aerial gas exchange, mass
reduction.

**A third fin allele exists and does NOT fit the stack, which is worth more than if it did.**
`cacna1g` homozygous mutants regenerate extraordinarily long fins (Le Bleu et al. 2025,
[doi:10.1242/dev.204739](https://doi.org/10.1242/dev.204739)) — a demonstrated zebrafish
loss-of-function long-fin model. But the authors state it **decouples developmental from
regenerative** outgrowth: the fin lengthens *while regenerating after amputation*. It is not a lever
for a larger fin in an intact animal, so it cannot be added to the stack as a third enlarger, and
counting it would have inflated two demonstrated slots to three on a misreading of what the allele
does.

**Two of eight slots is not a buildable stack**, and the subproblem refuted itself on the project's
own criterion rather than assembling something speculative. So the honest answer to *"can we get to
real genetic manipulations?"* is: **two of them, and six have never been done in this animal.**

An independent check: the required wing area at a 2 m/s launch is ~20 cm² against a ~1.4 cm²
whole-body dorsal silhouette — a **14× shortfall**, falling to 0.6× only at a 10 m/s launch. That
reproduces the launch-speed barrier from a completely different direction.

:::{caution} That 14× assumes C_L = 0.8, and this project's own claim 5 argues for ≤ 0.6
Area scales as `1/C_L`, so the assumption moves the shortfall directly:

| C_L | area at 2 m/s | shortfall vs 1.4 cm² |
|---|---|---|
| 0.5 *(flat plate, per a replication)* | 32.0 cm² | 22.9× |
| 0.6 *(claim 5's ceiling at Re 2–4×10³)* | 26.7 cm² | **19.1×** |
| **0.8** *(assumed, and used throughout)* | 20.0 cm² | **14.3×** |
| 1.0 *(cambered/corrugated, per the same replication)* | 16.0 cm² | 11.4× |

**The assumed 0.8 is above the ceiling one of this project's own claims argues for**, so the
headline 14× sits on the *optimistic* side of the internal evidence. At claim 5's ceiling it is
19×. A recovered replication disputes claim 5 in the other direction — ~1.0 for a
cambered/corrugated thin wing (snake section 1.1, dragonfly 0.93–1.07 at Re ~3×10³), 0.4–0.55 for
a flat plate — and a fin membrane is arguably neither.

**The conclusion is unaffected** — every value in that range leaves an order-of-magnitude
shortfall. What the spread shows is that the *precision* of "14×" is not earned: the honest range
is **11–23×**, and the figure quoted is the most favourable third of it.
:::

### A third check, formal, from a registry this project did not author

The **Delphi Lean law registry** (lawset 1.6.0, 53 laws with Lean theorems) was given the design —
*Danio rerio*, 0.4 g, 1.4 cm² lifting area, C_L,max 0.8, 4.41 m/s. It returned **exactly one
binding violation**: `C9 / thompson1917-ch02-06`, status `accepted`, band `proved`.

| | |
|---|---|
| v_min at 1.4 cm² | **7.56 m/s** vs the design's 4.41 — **1.71× too slow** |
| lifting area needed at 4.41 m/s | **4.12 cm²** vs 1.4 available — **2.94× short** |
| verdict | *lift cannot reach the weight even at C_L,max* |

**The agreement is the point.** Our own figure is ~20 cm² at a 2 m/s launch; lift area scales as
1/v², so propagated to 4.41 m/s that is **4.11 cm²**, against the registry's **4.12 cm²** — **0.06 %
apart**, from a separately derived formula in a registry we did not write.

**And it refused to over-reach, mechanically.** Seven rows came back `out-of-scope` rather than
violated, each because the constraint is calibrated against a single *Exocoetidae* reference
specimen and the design is *Danio rerio*. Each of those rows still records, in a separate
`evaluator_verdict` field, what the formula *would* have said — `violated` for five of them. So the
registry holds both facts without conflating them: **the arithmetic fails, and the law does not
apply here.**

That is precisely the distinction [two of our own entailment agents lost](architecture/cross-scale-constraints.md)
when they refuted zebrafish claims with exocoetid measurements. The registry gets it right by
construction, because scope is a *declared field on the law* rather than a judgement made per
verdict — which is the design lesson worth carrying back.

**Stated by the tool itself, not softened here:** this is a floating-point evaluation of
Lean-backed formulas, **not a kernel check**; kernel certificates exist only for recorded examples.
21 of 29 evaluated rows returned `cannot-evaluate` for missing inputs, so this is one constraint
genuinely tested, not a clean sweep.

---

## Three decisive experiments, all cheap, all bench-scale

1. **Measure pectoral fin AREA in the existing Daane double heterozygote.** The authors measured
   length and never area — **the animal exists and the measurement does not.** It decides whether
   even the ~5–7% phenotype is detectable.

   **Sizing, with one correction.** At CV_area = 0.10, 90 % power and α = 0.0167, **n ≈ 28 per
   genotype** — a figure an independent replication reproduces. But the claim that measuring
   *area* rather than *length* cuts the required n **four-fold is wrong**: it is **~1×**.

   Under isotropic scaling `area = length²`, so a 5 % length effect becomes a 10.25 % area effect
   — **and the CV doubles with it** (delta method: `d(L²)/L² = 2·dL/L`). Sample size scales as
   `(CV / effect)²`, so both transformations nearly cancel: 4.00 → 3.81, a reduction of **1.05×**.
   The four-fold figure comes from doubling the effect and **not** the noise.

   This does not weaken the recommendation — area is still the quantity the physics needs, and
   length cannot substitute for it. It removes a statistical argument that was never real.
2. **In-situ single-stroke spring-loading work of zebrafish fast myotomal muscle.** At or above
   **~99 J/kg** the energy term closes and the launch route reopens.
3. **Zebrafish C-start PIV efficiency**, which sets the 0.37 hydromechanical efficiency the whole
   launch budget rests on.

   **Quantified 2026-11-04.** The requirement is `10.17 / (0.30 · 0.93 · η_h)`, which reproduces
   98.5 J/kg at η_h = 0.37. But **0.37 is a point taken from a cited range of 0.34–0.39**, and the
   budget is linear in η_h, so the cited source alone puts the requirement at **93.5–107.2 J/kg**.
   The document has been quoting the midpoint as if it were the number.

   | η_h | required | shortfall vs 32–81 J/kg |
   |---|---|---|
   | 0.39 *(pike upper)* | 93.5 | 1.2–2.9× |
   | **0.37** *(the value used)* | **98.5** | **1.2–3.1×** |
   | 0.34 *(pike lower)* | 107.2 | 1.3–3.4× |
   | 0.25 *(hypothetical)* | 145.8 | 1.8–4.6× |

   **The other two inputs, traced the same day.** `98.5 = 10.17 / (0.30 · 0.93 · 0.37)`, and the
   0.30 is the one that matters:

   | input | what it is |
   |---|---|
   | 10.17 J/kg | derived energy need |
   | **0.30** | **an assumption** — S29 states *"the one-side 30 % is my assumption"*, taken as half of a 60 % whose own table is marked *"SECONDARY review figure; primary not read"* |
   | 0.93 | tendon return |
   | 0.37 | a point from a cited 0.34–0.39 pike range |

   | f_muscle | required | shortfall vs 32–81 J/kg |
   |---|---|---|
   | 0.60 *all skeletal muscle* | 49.3 | 0.6–1.5× |
   | **0.30** *the assumed one side* | **98.5** | **1.2–3.1×** |
   | 0.20 *upper jumper value* | 147.8 | 1.8–4.6× |

   **The source document is honest about this and the summary was not.** S29 flags the assumption
   in its own text and lists the dissected axial muscle fraction as a decisive experiment. This
   document carried neither caveat, and presented 98.5 as a number. **At 0.60 the row would read
   0.6×, i.e. the energy term closing** — so the headline rests on an assumption that, moved to
   the other end of its own stated range, reverses the finding.

   **And the value is pike** — a much larger fish at far higher Reynolds number — applied to a
   zebrafish. Whether a 0.4 g fish at Re ~10⁴ achieves the same hydromechanical efficiency is
   **not known and not asserted here in either direction**; it is listed as a decisive experiment
   precisely because nobody has measured it. What the table above establishes is only the
   **sensitivity**: a fifth off the efficiency adds half again to the requirement.

None is a programme. Each is a measurement.

---

## How much of this is measured

Of **295** live claims: **163 derived**, **56 measured**, 37 literature, **27 unknown**,
11 simulated, 1 assumed. Most of this project is *derived from* measurements rather than measured —
legitimate for a design study, and the number to probe first.

**`unknown` went from 90 to 27, and most of the recovery was a bug rather than a judgement.**
**55** of the 90 carried an explicit, valid evidence level *in their own text* — written there by
an earlier importer that put the agent's answer in prose instead of in the column. The current
harvester does it correctly, so this was one-off historical damage, not a live defect. Restoring
them is mechanical and was verified: all 55 stored levels match the text they were read from.
A further **8** were assigned by reading the full claim one at a time, each recording in its source
field why — and the rule used was *the level describes what the conclusion rests on, not the
strongest input in it*, which is why a figure-read input feeding a calculation lands as `derived`.

**The remaining 27 are mostly correct.** Reading 20 of the original 90 by hand: **9 are correctly
`unknown`** — a stated non-result (*"adult zebrafish fast-start
peak velocity is unknown"*), the scope of a negative (*"the lat4a absence is against UniProtKB and
NCBI Gene only"*), a source that could not be read (*"the table is image-only"*), a preserved
disagreement (*"relayed as 3.8e-6 by Puri 2018 and 565e-6 in the Flammang abstract"*), and
reproducibility or scope caveats. **An evidence level would be wrong for every one of those** —
there is no measurement to level.

The other **11 of 20 are factual claims whose level was genuinely lost**, including a direct
measurement (*"per-fish maximum fast-start speeds span ~0.45–1.38 m/s"*) sitting at `unknown`.

**The sample was 20 taken in id order, not at random, so early claims are over-represented** —
the split was indicative, not measured, and the eventual recovery rate (63 of 90) came out higher
than that sample implied.
Each of the 11 needs reading to assign a level; nothing can do it mechanically, because a classifier
that distinguishes *"X is unknown"* from *"X is 1.38 m/s"* by pattern is the same forbidden-string
check this project has documented failing three times.

**An earlier version of this passage called all 90 a quality gap.** That was asserted from a count
without reading the rows — the error this document exists to catch.

**Only 10 of 295 claims carry a `run_id`** — a command that reproduces them. The rest trace to an
agent's prose and no further. See [the empty set](architecture/the-empty-set.md) §4.

**753 challenges have been resolved**, and the base rate is uncomfortable and informative:
**70.4 % weakened, 22.7 % survived, 6.9 % refuted**. Sampling six weakened verdicts found all six
substantive. The recurring shape is *"the arithmetic reproduces, but the inference overreaches"* —
so the low survival rate is a finding **about us**, not about the challengers.

:::{note} An independent replication disputed these numbers, and the database settles it in their favour
A re-derivation of the original audit got **29.5 % survival** against the recorded 17 %, and
flagged in its own note that *"the database the claim counted was not accessible to settle which
record is wrong"*. Counted directly: the first 156 resolved challenges give 107 weakened,
**26 survived** — exactly as recorded — and 23 refuted, i.e. **16.7 %**. The original stands.

**The cause is a population mismatch worth knowing about.** Git holds **305** `swarm-challenge`
blocks; the database holds **843** challenge rows, 753 resolved. A row is created when the
generator *dispatches* a challenge; a block exists only where an agent *wrote the result up*. So
git blocks are a **biased subset**, not a proxy for the population, and any statistic taken from
them diverges systematically.

The replication was wrong and behaved correctly: it recomputed independently, reached a different
number, named exactly what would settle it, and declined to assert which record was in error.
:::

**The weakened rate is now a measurement rather than an impression.** At 231 challenges it was
70 %; at **753** — a 3.3× larger sample — it is **70.4 %**. A base rate that stable across that
much more evidence is not a small-sample artifact.

The other two moved, and in the direction that matters: **refuted roughly halved (13 % → 6.9 %)
while survived rose (17 % → 22.7 %)**. The most likely reading is that the early claims were the
easy targets and the graph has since been corrected toward statements that hold — but this is an
inference about a changing population, not a controlled comparison, and the challengers' prompts
were edited during that period.

The grader producing those verdicts has been **calibrated**: 7/7 on a blind benchmark, 4/4 on
seeded defects spanning arithmetic, regime, scale and evidence-level inflation. **Two of the four
seeded defects are real errors this project made.**

---

## An independent replication arm was running, and its output was being thrown away

`generate.py` describes replication as *"the cheapest hallucination detector there is"*: an agent
re-derives a claim's number **without being shown the original**. **134 such results were produced.
None was ever recorded.** The harvester's block regex matched four kinds and its dispatch had
three branches, so every `swarm-replication` block was parsed, counted in the "blocks found"
total, and dropped. Recovered 2026-11-04: **103 stored, 86 agreeing, 17 disagreeing.**

**Four of the 17 have been adjudicated. Two corrected this document; one is now openly contested;
one is a detail that changes nothing.**

| claim | the disagreement | outcome |
|---|---|---|
| 194 | the 10 % upper end treats full lift at a 45° climb as vertical | **replication right** — headline deliverable corrected to ~5–7 % |
| 310 | measuring area does not cut n four-fold | **replication right** — real reduction is 1.05×; isotropy doubles the CV too |
| 52 | the tail-beat row borrows a Strouhal measured 11× away in Re | **unresolved** — both arithmetics reproduce; the row now carries both |
| 298 | the AR convention factor mixes two of Fish 1990's tables | **unsettled, and immaterial** — both candidate bars leave the conclusion intact |
| 203 | fish red muscle reaches ~28 W/kg, not 5–10 | **original right, on method** — 28 is an *optimized isolated-tissue* value; Rome & Swank's own conclusion warns against using those to predict whole-animal performance |
| 5 | C_L,max is ~1.0, not ≤ 0.6 | **exposed an internal inconsistency** — the project assumes 0.8, above claim 5's own ceiling; honest shortfall range is 11–23×, not 14× |
| 232 / 304 | the girdle section modulus is ~1.0e-3, not 3.6–6.8e-3 mm³ | **unresolved and conclusion-relevant** — both numbers reproduce on *different sections*; if the dorsal cleithral limb is load-bearing the girdle **fails** at measured size (0.61×) and passes only after scaling to 40 mm |
| 31 | and2's cysteine depletion is z = −1.6, not −2.02 | **replication right, on method** — p flips 0.022 → 0.055 across the boundary, and z = −2.02 only appears at a window that fails the project's own control. The zero close-pairs and absent CxxC *do* reproduce |
| 207 | the challenger survival rate | **original right** — the replication counted git blocks, a biased subset of the database |

| 31 | and2's cysteine depletion is not significant | **replication right, on method** — p flips 0.022 → 0.055, and z = −2.02 only appears at a window failing the project's own control |
| 201, 260 | lower bounds and a pitch mode differ | **minor** — the replications state the conclusions stand; 201's moment and bone section *reproduce exactly* |
| 11 | the a3m holds 76 records, not 72 | **undecidable here** — the file was never committed ([claim 210](#)); the substantive part, that top hits are real K2P structures, is confirmed |
| 296, 181 | loop delay and actinotrichial modulus | **unresolved** — in both, the replication could not verify the inputs its own alternative needs |
| 29 | and1 does depart from the shuffle null | **source-only** — two replications agree and cite the claim's own table against it; not re-run here |

**All 17 have now been read.** They are stored as `artifact_signal` rows with `voter_kind: agent`.

**Final tally: the arm was right 4 times, wrong twice, raised 4 unresolved or immaterial
questions, and exposed one internal inconsistency.** Two of its correct findings were in this
document's headline material — the lead deliverable and the top recommended experiment.

**The uncomfortable summary:** the bug that discarded all of this was a dispatch with three
branches for four kinds. It ran for the project's entire life, and the harvester printed a
"blocks found" total that included the blocks it was dropping.

## What is and is not machine-checked in this document

A precise answer, because "every number is checked" is the kind of claim this document spends its
length refusing to accept from others. Of **49** bold numeric assertions:

| | count | how it is backed |
|---|---|---|
| **design arithmetic + audit ratios** | **23** | `analysis/headline_table.py` recomputes each from its own inputs and **exits non-zero on drift** |
| run outputs | 9 | a `run` row with a `code_sha` — ESMFold2 pLDDT, ProteinMPNN ranks, the shuffle p |
| graph statistics | 7 | live counts; **deliberately not pinned**, since a script asserting them would go stale the moment the graph moves |
| external lookups | 1 | a PubMed count, reproducible only by re-querying |
| everything else | 9 | counts about this document, and ratios whose inputs are run outputs |

**So the honest statement is: the design arithmetic and the recomputable audit ratios are
machine-checked; nine numbers are not.**

The audit ratios were the gap this section named an hour ago, and five of them are now checked —
the quotient that exposed the broken table row (`98.5/8.6 = 11.45`), the 45° lift projection
(`10·cos 45° = 7.07`), the one-third ceiling that was rejected as a double-count (`98.5×3 = 295.5`),
the 1/v² propagation (`20·(2/4.41)² = 4.11`), and the area-vs-length sample-size ratio (**1.05**,
where ignoring the CV doubling gives the 4.2 that was wrong).

The nine that remain are **counts about this document itself** and **ratios whose inputs are run
outputs** — a ProteinMPNN rank percentile, a sequence-recovery fraction. Those are backed by a
`run_id` rather than by recomputation, which is a different guarantee, not an absent one.

## Open items, stated so the next reader does not have to find them

Everything below is unresolved **and known to be unresolved**. Nothing here is a to-do list of
work that would obviously succeed; each is a specific question with a stated reason it is open.

### Could change a conclusion

| item | why it matters | what would settle it |
|---|---|---|
| **Which girdle limb carries the fin-root moment** about the AP axis | if the dorsal cleithral limb is binding, the girdle **fails** at measured size (0.61×) rather than passing at 2.1–3.9× | **a structural analysis nobody has done** — whether the limbs load in *series* (weakest section governs → fail) or *parallel* (stiffer ventral limb governs → pass). Tested for reachability three ways: both analyses already decoded the mesh and agree on the numbers; a morphology paper would not give a load path; and PubMed returns **0** for *"zebrafish cleithrum biomechanics"* against **64** for *"cleithrum"* alone, so that zero is a real absence |
| **The Strouhal regime for the taxi** | the headline table row is either **2.5–3.8×** or **1.4–1.6×** | re-derive Eloy's Lighthill number at the taxi operating point; both arithmetics already reproduce |
| ~~Whether `and1` departs from the shuffle null~~ | **CLOSED 2026-11-04** | re-run here: **p = 0.0050**, reproducing both replications. Claim 29 is refuted. Both controls pass — a planted repeat is caught at p = 0.0050, a shuffled copy of `and1` returns p = 0.607. The effect is **significant but small**: 0.1157 against a shuffle maximum of 0.1154 |

### Known weaknesses in numbers that are quoted

- **C_L = 0.8 is assumed and exceeds claim 5's own ≤ 0.6 ceiling.** The honest area-shortfall range
  is **11–23×**, not 14×.
- **η_h = 0.37 is a point from a cited 0.34–0.39 range**, and is a *pike* value applied to a
  zebrafish at Re ~10⁴. The requirement spans **93.5–107.2 J/kg** from the cited range alone.
- **f_muscle = 0.30 is an assumption** — half of a 60 % whose own table is marked *"SECONDARY
  review figure; primary not read"*. At 0.60 the energy term **closes**.
- **The 0.93 spring-return efficiency is the most favourable reading of its own sources.** Traced
  2026-11-04: S29 cites *"hysteresis ~7–10 % for tendon: **Ker 1981, ABSTRACT**; **Gosline 2002
  resilience 90–92 %, SECONDARY**"*. That gives 0.90–0.93 from Ker and 0.90–0.92 from Gosline, so
  **0.93 is the top of one range and above the other entirely**, and neither source was read in
  full. The effect is small — 98.5 → 101.8 J/kg at 0.90, a 3.3 % spread — but it is the **fourth
  input in a row** taken from the favourable end of its own evidence.

### Structural gaps in the record itself

- **Only 11 of 295 claims carry a `run_id`** — a command that reproduces them. The rest trace to
  an agent's prose and cannot be given one retroactively without inventing provenance.
- **11 of 21 mechanisms in the schema hold no rows at all** ([the empty set](architecture/the-empty-set.md)),
  so any rule quantified over them is vacuously true. `grade` and `rubric` are empty, which is why
  [SPEC-evaluation-kernel](specs/SPEC-evaluation-kernel.md) reads green: **grading never happened.**
- **20 literature claims have no `read_level`** and 10 subproblems no `answer_kind`. Both are left
  red deliberately — the agent never supplied the value, and inventing one is the fabrication those
  fields exist to prevent.
- **Formal verification reaches the organism scale and not the DNA scale.** The Delphi registry's
  five genotype laws (G1–G5) return `cannot-evaluate`; supplying `genotype_edits` cleared the
  `missing` list without producing a verdict.
- **The `kcnk5b` a3m was never committed**, so the MSA-depth result behind *"the alignment ran out,
  not disorder"* cannot be independently checked from this repository.

## What this does not establish

- Fin **area** has never been measured in any enlarged-fin zebrafish, so the central geometric input
  is an extrapolation.
- **Membrane stiffness has no computational route, not merely no demonstrated allele.** The
  actinotrichia proteins are actinodins — `and1` (E7F5V5, 570 aa), `and2` (A9JRX1, 508 aa), `and3`
  (Q7SZZ6, 295 aa). Measured here from primary sequence, they carry **no collagen triple-helix
  signature**: glycine fractions of 5.4 / 4.5 / 2.7 % and longest in-frame Gly-X-Y runs of **2, 2
  and 1** triplets, against a `col1a1a` positive control at **26.4 % glycine and a 339-triplet
  run**. That is a ~170× separation, so the assay discriminates and the negative is informative.
  It confirms the project's existing "not collagen-like despite being termed elastoidin" claim by
  an independent route.

  **But no model in reach predicts a modulus from a sequence.** ProteinMPNN designs sequences
  compatible with a *backbone*, not stiffer ones; ESMFold2 returns a structure and its own
  confidence. So a "stiffer actinodin variant" is not something this project can currently produce
  or evaluate, and any such design would be a claim with nothing behind it.

  **Folding it made that sharper: the question is at the wrong level of description.** MSA-free
  ESMFold2 on `and1` returns **pTM 0.202**, mean pLDDT **69.7**, only **2.8 %** of residues above
  90, and a longest ordered stretch of **49 residues**. The control is `slc43a2a` WT — same model,
  same settings, same day, 577 aa against 570 — at **pTM 0.823**, mean **85.9**, **58.1 %** above
  90, **477** residues above 70.

  | | slc43a2a (control) | and1 |
  |---|---|---|
  | pTM | 0.823 | **0.202** |
  | mean pLDDT | 85.9 | 69.7 |
  | residues > 90 | 58.1 % | **2.8 %** |
  | longest run > 70 | 477 | **49** |

  ESMFold2 is MSA-free, so **both got identical (absent) alignment treatment** — the difference is
  in the sequences, not an alignment-depth artifact. `and1` is predicted largely extended, with no
  compact tertiary structure: what an extracellular fibrillar protein should look like.

  So a fibrous protein's stiffness comes from **supramolecular assembly** — fibril packing and
  cross-linking — and a single-chain monomer prediction cannot address that *even in principle*.
  Adding a monomer stiffness predictor would not help. The honest status of this capability is
  **no demonstrated allele, no in-silico route, and the available route is at the wrong level**.
- The S26 active-stiffening margin rests on a boundary condition that **could not be verified**: the
  publisher blocks full text and the OA service 404s. The order of magnitude is confirmed by the
  paper's own abstract; the exact factor is not.
- No organism was built, no measurement was taken by us, and no simulation was validated against an
  experiment. Every number is literature, derivation, or model output, labelled as such.
- **Three routes have now failed on three different terms** — wings on lift, a single spring
  impulse on muscle energy density, and the multi-stroke taxi on Reynolds-limited lobe drag. The
  third is the best founded because it reproduces a real glider. None of this proves no route
  exists; it means the three that have been modelled do not work, each for a reason that can be
  checked independently.
- The headline 4.37 m/s **looks the most precise number here and is the most structurally
  dependent**: its ±0.11 propagates neither the wing area's total absence of an interval nor the two
  untested structural assumptions beneath it (steady lift, rigid wing).
