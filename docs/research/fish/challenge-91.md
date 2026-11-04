# Challenge 91 — adversarial review of the S14-D "FALLS" verdict on kcnk5b

**Claim under review (claim_id 91).** "S14-D deepen FALLS: engineering kcnk5b for graded
pectoral-restricted control is unsupported. AFDB pLDDT is 69.5 (monomer) / 62.82 (homodimer),
33.9% of residues <50, not >80; quoted at filter motifs 98-102 and 203-207, not the causal alf
residues W169/F241. Single measured ~2-fold conductance window = 17.1 mV of ~60 mV = ~3.4
setpoints at sigma 5 mV (harvester recomputed 17.1/5=3.42). Sign of pectoral Vm response in
unresolved disagreement: Perathoner 2014 (hyperpolarization, calibrated oocyte clamp) vs Jiang
2024 (depolarization, uncalibrated dye). AFDB values not re-fetched."

**Recorded evidence level:** derived. **Recorded value:** 3.4 distinguishable setpoints.
**Source:** branch `claude/deepen-s14-potassium-channel-5miqg2`, `docs/research/fish/S14-deepen.md`.

**Date of this review:** 2026-11-04. Every retrieval below was made on that date by me, in this
session. I read the full S14-deepen.md source document before reviewing it.

**Verdict up front: REFUTED.** Two of the claim's three evidentiary legs are contradicted by the
primary records the claim itself cites, and the recorded value carries the wrong unit. The
claim's *conclusion* — that engineering kcnk5b itself for graded pectoral-restricted control is
unsupported — I did **not** overturn, and in one respect I strengthened it. But it does not stand
on the reasons given.

A note on direction, because it matters for how much weight to put on this review: of the four
attacks I mounted, **one failed outright** (§3.4) and I report that as prominently as the ones
that landed. Two of the three defects I do report were found by retrieving records the author
did not retrieve, not by rhetoric.

---

## 1. Independent arithmetic — redone from the stated inputs

I did not read `S14-recompute.py` before writing my own. I derived the two-branch divider from
the stated model and inverted it myself:

```
Vm(x) = (x·E_K + E_B)/(x + 1),   x ≡ g_K/g_B
x(Vm) = (Vm − E_B)/(E_K − Vm)
```

With `E_K = −100`, `E_B = 0`, `Vm_wt = −40`:

```
x₀ = (−40 − 0)/(−100 + 40) = −40/−60 = 2/3
R = 2  ⇒  x = 4/3
Vm    = ((4/3)(−100) + 0)/((4/3) + 1) = (−400/3)/(7/3) = −400/7 = −57.142857 mV
ΔVm   = −400/7 + 40 = −120/7 = −17.142857 mV
|ΔVm|/σ at σ = 5 mV = (120/7)/5 = 24/7 = 3.428571
```

**The author's arithmetic is exactly right.** 17.14 mV; 3.4286. The harvester's `17.1/5 = 3.42`
is also right. My script is committed beside this file as `challenge-91-recompute.py`
(dependency-free; `python3 -I docs/research/fish/challenge-91-recompute.py`). The whole Vm_wt
sweep reproduces to the digit: −13.33 / −16.15 / −17.14 / −16.67 / −15.00 mV at Vm_wt =
−20/−30/−40/−50/−60, and 16.67 / 23.08 / 28.57 / 33.33 / 37.50 % of the available swing. So does
the R-sensitivity table (R = 1.41 → 8.454 mV; R = 2.83 → 25.358; R = 4 → 32.727).

### 1.1 Defect 1 — the recorded value has the wrong unit (off by one)

`window/σ` is the number of **resolvable intervals**, not the number of **setpoints**. A window
of width *W* discriminated in steps of σ holds `W/σ` steps and therefore `W/σ + 1` distinguishable
positions, counting both ends. Computed (my script, §C):

| σ_V (mV) | intervals = W/σ | setpoints = W/σ + 1 |
| --- | --- | --- |
| 2 | 8.571 | 9.571 |
| **5** | **3.429** | **4.429** |
| 10 | 1.714 | 2.714 |
| 15 | 1.143 | 2.143 |

The ledger records **"3.4 distinguishable setpoints."** On the author's own model and parameters
the figure is **4.43 setpoints**, a 29% understatement. The source document is internally
consistent — it says "distinguishable **levels**", and its own `R = 1` row prints `0.00`, which is
correct for *intervals* and wrong for *setpoints* (R = 1 is one setpoint, not zero) — so the slip
is in the quantity being counted, and the claim as recorded inherits it under the word
"setpoints".

**This matters precisely where the author says the verdict turns.** The source document's
sensitivity argument reads: halve the window and "it is **1.7 levels: an on/off switch, not a
graded controller.**" In setpoints that case is **2.69** — a three-position controller, not a
switch. The factor-of-two demonstration the deepening was asked to produce is overstated by one
position at every point on the curve, and the rhetorical collapse to "on/off" does not occur.

**This is my inference from the author's stated model, not a new measurement.** It does not by
itself overturn "marginal": 4.4 setpoints is still few.

---

## 2. Is a proxy standing in for the quantity that matters?

The source document is unusually good on this and names its own proxy chain (macroscopic oocyte
TEVC current standing in for in-tissue g_K; g_K = N·i·P_o not decomposed). I agree with all of
it and will not re-litigate it. Three proxies it did **not** flag:

**2.1 `E_K = −100 mV` is an oocyte number applied to zebrafish fin-bud mesenchyme.** The source
document labels this "**from the source**", and it is — Perathoner et al. write "−90 to −100 mV,
the equilibrium potential for K⁺ in *Xenopus* oocytes" (verbatim, read-level **full-text**,
PMC3894163, 142,283 bytes, confirmed by me). But the quantity needed is E_K in fin-bud mesenchyme,
which no source I read reports. *Direction of the error, computed by me:* at `E_K = −85 mV`,
`Vm_wt = −40`, `E_B = 0`, a 2-fold g_K increase buys **14.4 mV**, i.e. 2.9 intervals rather than
3.43. The proxy transfer is therefore **mildly favourable to the author** — the real window is
probably narrower than 17.1 mV, not wider. Not a defect in the verdict's direction.

**2.2 `E_B = 0 mV` is flagged as an assumption, and relaxing it also favours the author.** My
sweep (script §E, `Vm_wt = −40`, `E_K = −100`):

| E_B (mV) | x₀ | ΔVm at R = 2 | intervals at σ = 5 |
| --- | --- | --- | --- |
| +20 | 1.000 | −20.00 | 4.00 |
| **0** | **0.667** | **−17.14** | **3.43** |
| −10 | 0.500 | −15.00 | 3.00 |
| −20 | 0.333 | −12.00 | 2.40 |
| −30 | 0.167 | −7.50 | 1.50 |

A real non-selective background branch in a somatic cell is a mixed Na⁺/Cl⁻ leak, i.e. negative,
not 0 mV. So the author's assumption sits at the **optimistic** end of its plausible range. I
tried to break the result here and the relaxation pushes the other way.

**2.3 The one proxy that does break: fin size, not Vm, is the controlled output.** See §3.3.

---

## 3. Hidden assumptions, relaxed

### 3.1 Defect 2 — σ_V is justified at its large end by the wrong statistic

σ_V is the parameter the source document says the verdict flips on by itself: "it also flips on
σ_V alone: at σ_V = 10 mV the window holds 1.7 levels even with R = 2." The document correctly
records σ_V as **unmeasured**. But it does recruit one piece of evidence for the large end, and
states the direction:

> "**My inference:** within-bud Vm heterogeneity is of the same order as the between-condition
> signal, which pushes the achievable number of grades toward the low end of the range computed
> in section 4."

The evidence is Jiang et al.'s report that their Vm averages "represented a broad distribution of
depolarization levels" — i.e. **cell-to-cell scatter within one fin bud**.

**My inference, stated as mine:** single-cell Vm scatter is not the discrimination step for a
tissue-level output. Fin size is produced by a bud of many cells; if growth responds to each
cell's own Vm, the tissue output tracks the *mean* Vm, whose sampling error is σ_cell/√N, not
σ_cell. The source document's own §4a makes the output variable explicit — "Fin size tracks
membrane potential ... so the controlled variable is Vm" — and fin size is a whole-tissue
integral. Computed (script §F), window = 17.14 mV:

| σ_cell (mV) | N = 1 | N = 10 | N = 100 | N = 1000 |
| --- | --- | --- | --- | --- |
| 5 | 3.43 | 10.84 | 34.29 | 108.42 |
| 10 | 1.71 | 5.42 | 17.14 | 54.21 |
| 15 | 1.14 | 3.61 | 11.43 | 36.14 |

(intervals; add 1 for setpoints)

At N = 1 these are the document's numbers. At any N a fin bud plausibly has, the window is not
the binding constraint at all. **I am not claiming 108 setpoints are achievable** — spatial
averaging is not free, there are non-averaging sources (animal-to-animal transgene variegation,
which Jiang et al. explicitly report as "variegated patterns high and low fluorescence"), and the
Vm → size transfer function has its own gain and noise that nobody has measured. My claim is
narrower and I think unavoidable: **the one piece of evidence the author recruits to push σ_V
toward 10–15 mV does not bear on σ_V as the author's own model uses it**, so the leg of the
sensitivity argument that "flips on σ_V alone" is unsupported. The honest statement is that σ_V
is unpinned in both directions, and therefore that the setpoint count is **indeterminate**, not
~3.4.

The right statistic — and the measurement nobody has made — is the **between-animal
reproducibility of fin size, converted into mV through the measured dVm/d(size) gain.** The
source document's §3d asks for the within-bud distribution; it should also ask for the
between-animal one.

### 3.2 The compressiveness result survives

Successive doublings from Vm_wt = −40 (my numbers, independent): −40.00 → −57.14 → −72.73 →
−84.21 → −91.43 → −95.52, steps −17.14 / −15.58 / −11.48 / −7.22 / −4.09. Reproduces exactly.
The saturation argument is sound and is a real property of the divider, not an artifact.

### 3.3 The output-variable proxy

The source document counts distinguishable setpoints **in Vm**. The thing a user of "graded
control" wants is distinguishable **fin sizes**. These differ by the gain of the Vm → size map,
which is nowhere measured, and the *alf* phenotype is a large one (whole-appendage overgrowth)
produced by this same 2-fold, which suggests high gain. I flag this as an unexamined link and
**do not assign it a direction**, because a high-gain map amplifies both signal and noise and I
have no measurement of either. Recording it as an open proxy rather than a fault.

### 3.4 An attack that FAILED — and the failure strengthens the author

My strongest numerical attack was that the window is **arbitrarily one-sided**. The source
document's own §3b retrieves the conductance series `{0 (GFG→AAA), 1.0 (wt), ~2.0 (W169L),
~2.0 (F241Y)}` and then dismisses the zero as "adding only a zero, not a grade." But in the
author's own divider, driving g_K to zero sends Vm to E_B = 0 mV — a **+40 mV** excursion from
Vm_wt = −40, more than twice the 17.14 mV available upward. Computed (script §D):

```
R = 0.00  → Vm =   0.00 mV        full two-sided window (R=0 … R=2)
R = 0.25  → Vm = −14.29 mV        = 57.14 mV
R = 0.50  → Vm = −25.00 mV        = 11.43 intervals at σ = 5
R = 1.00  → Vm = −40.00 mV        = 12.43 setpoints
R = 2.00  → Vm = −57.14 mV
```

12.4 setpoints is comfortably graded, and loss-of-function variants are far easier to design than
gain-of-function ones. Had this held, it would have refuted leg (b) outright.

**It does not hold.** Perathoner et al. report a revertant deletion allele of *kcnk5b* and state
(verbatim, read-level **full-text**):

> "The resulting protein is predicted to lack 3 of the 4 transmembrane (TM) domains ... This
> suggests that the revertant is a **null mutation** for *kcnk5b*. **Homozygotes harboring the
> deletion are viable and fertile**; thus, *kcnk5b* is not essential for zebrafish development.
> As *kcnk5b* has a close paralog in zebrafish, *kcnk5a* ... the **lack of a loss-of-function
> phenotype** in normal development may be due to functional redundancy between the paralogs."

**The downward arm is measured and phenotypically silent.** Reducing Kcnk5b below wild type
changes nothing about appendage size, because *kcnk5a* covers for it. The author's restriction of
the window to the gain-of-function arm [1, 2] is therefore **empirically correct** — on better
grounds than the author gave for it, and the author did not cite this passage in support of the
one-sided window. I record this as a point in the source document's favour.

(Caveat, stated: the null is silent *in normal development*; a designed graded controller would be
expressed on top of endogenous Kcnk5b *and* Kcnk5a, so a dominant-negative acting on both paralogs
is not excluded by this passage. No source I read tests that. It remains `unknown`, and it is not
enough to revive my attack.)

---

## 4. Is the evidence level honest?

**Recorded as "derived" — correct, and the source document's labelling is better than the claim
as recorded.** Every §4 number in S14-deepen.md is explicitly marked simulation, the parameter
provenance table distinguishes "from the source" / "my assumption" / "not stated in the source,
swept", and the author labels the K2P-dimer background fact as *remembered, not retrieved*. I
checked that last one: **`dimer` occurs 0 times in Perathoner et al. and 0 times in Jiang et
al.** (my string counts on tag-stripped full texts). The author was right to flag it as
unsourced. That is honest practice and I want it recorded as such.

Two labelling problems, both in the **claim as recorded** rather than in the source document:

1. **The "~3.4 setpoints" unit error** (§1.1) — the source says "levels", the claim says
   "setpoints", and only one of those is the quantity `17.1/5` computes.
2. **The hedge is stripped.** The source document says of the >80 figure: "It may well be true of
   the two filter motifs specifically; **I could not confirm that**." The claim as recorded states
   flatly "**not >80**". That is a material loss — see §5, where it becomes the central defect.

---

## 5. Defect 3 — the pLDDT leg is a category error, and the mislocation argument runs backwards

### 5.1 I re-fetched the AFDB values. They are exactly right.

The claim flags "AFDB values not re-fetched". I re-fetched them.

`https://alphafold.ebi.ac.uk/api/prediction/Q6PFU3` (HTTP 200, 2,371 bytes, read-level
**full-text**, complete API record): `entryId AF-Q6PFU3-F1`, `latestVersion 6`,
`globalMetricValue` **69.5**, `fractionPlddtVeryHigh` **0.353**, `fractionPlddtConfident`
**0.248**, `fractionPlddtLow` **0.060**, `fractionPlddtVeryLow` **0.339**, `uniprotEnd` 448,
`modelCreatedDate` 2025-08-01.

3D-Beacons (`https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/Q6PFU3.json`,
HTTP 200, 4,185 bytes, read-level **full-text**): `AF-0000000066331115`, provider **AlphaFold
DB**, `oligomeric_state` **HOMODIMER**, `confidence_avg_local_score` **62.82**, created
2025-12-25. The same record lists `AF-Q6PFU3-F1` as MONOMER at **69.5**, and a third
template-based AlphaFill model with no confidence score.

I also verified the sequence-level facts from the retrieved 448-aa sequence (AFDB and UniProt
sequences are byte-identical — I compared them): `TIGYG` occurs once, at **98–102**; `TVGFG` once,
at **203–207**; residue **169 = W**; residue **241 = F**. Every retrieval in the claim checks out.
The author's numbers are not the problem.

### 5.2 The problem: a whole-chain mean is being used to refute a motif-local statement

`globalMetricValue` 69.5 is the mean pLDDT over **all 448 residues**. The recorded answer being
challenged said pLDDT > 80 **at both selectivity filters** — ten residues. "69.5, not >80"
compares a global mean against a local claim. Those are different quantities, and the first
cannot refute the second.

**Arithmetic I did independently from the retrieved band fractions** (script not needed; shown in
full so it can be checked):

```
total pLDDT sum        = 69.5 × 448                        = 31,136
very-low residues      = 0.339 × 448                       = 151.9
that band is <50 by definition, so its sum  <  50 × 151.9  =  7,594
⇒ remaining 296.1 residues sum  >  31,136 − 7,594          = 23,542
⇒ mean pLDDT of the non-very-low 66.1% of the model  >  23,542/296.1  =  79.5
```

That is a **hard lower bound** from the claim's own retrieved numbers. And it is slack: for any
realistic mean of the very-low band the rest averages far higher —

| if the <50 band averages | the other 66.1% averages |
| --- | --- |
| 45 | 82.1 |
| 40 | 84.6 |
| 35 | **87.2** |
| 30 | **89.8** |

Further, `fractionPlddtVeryHigh` = 0.353 means **158 residues are above 90**. A model with 158
residues >90 has a well-determined core, and the two filter motifs are in it or they are nowhere.

**So the retrieved record is not merely consistent with ">80 at both filters" — it requires that
two-thirds of the model average about 80 or better.** The claim cites a number that, worked
through, supports the thing it is offered as refuting. **This is my inference from the retrieved
band fractions; it is not a measurement of filter pLDDT, which I could not obtain (§5.4).**

### 5.3 The mislocation argument runs backwards — retrieved topology

The claim's second clause is that confidence was "quoted at filter motifs 98-102 and 203-207, not
the causal alf residues W169/F241", with the source document adding: "Even a filter pLDDT of 100
would say nothing about the local accuracy at W169 or F241."

I retrieved something neither the claim nor the source document retrieved — the UniProt topology
annotation for Q6PFU3 (`https://rest.uniprot.org/uniprotkb/Q6PFU3.json?fields=ft_transmem,...`,
HTTP 200, 2,216 bytes, read-level **full-text**):

| Feature | Range |
| --- | --- |
| Transmembrane, Helical | 7–26 |
| Transmembrane, Helical | 116–137 |
| Transmembrane, Helical | **158–185** |
| Transmembrane, Helical | **229–250** |
| Region, **Disordered** | **382–448** |

**W169 lies inside the third TM helix (158–185). F241 lies inside the fourth (229–250).** The
local sequence context I extracted confirms both are mid-helix in strongly hydrophobic stretches:
`FICTIVFLLWGFLVHLIIPAF` (160–180, W at 169) and `YLGLAWLSLFFSWNVHMVV` (232–250, F at 241). This
independently corroborates Perathoner et al.'s own statement, which the source document quoted
but did not check against a topology record: "the affected amino acids are positioned in two
distinct TM domains."

**My inference, separated from the retrieved annotation:** transmembrane helices are the
best-determined elements of an AlphaFold model of a membrane protein, and the disordered region
that drags the global mean down is annotated at 382–448, 130+ residues away from both causal
residues. So the mislocation observation — true as stated — does **not** support the inference the
claim needs. It is not that confidence was vouched somewhere good while the causal residues sit
somewhere bad; the causal residues sit in the structurally *most* determined part of the chain.
The argument, followed through, weakens the critique rather than supporting it.

Supporting arithmetic on where the low-confidence mass sits: the last TM helix ends at 250, so the
cytoplasmic C-terminus is residues 251–448 = **198 residues (44.2% of the chain)**. The very-low
band is **152 residues (33.9%)**. The low-confidence mass fits inside the cytoplasmic tail with
46 residues to spare. **Inference, not measurement** — per-residue pLDDT would be needed to place
it, and I could not get it.

### 5.4 What I could not get either — scope of the negative

Per-residue pLDDT would settle ">80 at the filters" directly. I could not retrieve it, and I
tried five routes:

| Route | Result |
| --- | --- |
| `alphafold.ebi.ac.uk/files/AF-Q6PFU3-F1-confidence_v6.json` | **HTTP 403** (134-byte proxy error page) |
| `alphafold.ebi.ac.uk/files/AF-Q6PFU3-F1-model_v6.pdb` | **HTTP 403** |
| `alphafill.eu/v1/aff/Q6PFU3` (AlphaFill carries pLDDT in the B-factor column) | **CONNECT tunnel failed, 403** — host not allowed for this session |
| `rest.uniprot.org/alphafold/Q6PFU3` | HTTP 404 — no such endpoint |
| `ftp.ebi.ac.uk/pub/databases/alphafold/` | HTTP 404 / not reachable |

Read-level for per-residue pLDDT: **could-not-access**. I replicate the source document's gap
rather than closing it, and I therefore **cannot assert that filter pLDDT is >80 either.** What I
can assert is that the claim's stated evidence does not establish "not >80", and that the
arithmetic in §5.2 runs against it. A runner with egress to `alphafold.ebi.ac.uk/files/` or
`alphafill.eu` can settle this in one request.

### 5.5 On the 62.82 homodimer figure

Confirmed verbatim, and the author's use of it is defensible (K2P channels conduct as dimers — the
author correctly flagged that as remembered, and `oligomeric_state: HOMODIMER` on the AFDB record
is at least weak corroboration of the assembly). But it changes nothing: it is a model of the
same 448-aa chain including the same disordered tail, so the §5.2 band logic applies to it too,
and whether the 69.5 → 62.82 drop reflects genuinely worse modelling or inter-chain uncertainty
is **indeterminate from the summary record** — the per-chain bands are not published in the
3D-Beacons summary and the coordinate file is 403 to me.

---

## 6. Defect 4 — the sign is not in "unresolved disagreement"; the source resolves it

This is the claim's third leg and the one the source document's verdict leans on hardest:
"blocked by an unresolved sign in the target tissue."

The source document quotes Jiang et al. **naming** the paradox:

> "The observed increase in depolarization caused by *kcnk5b*, a leak channel that should promote
> hyperpolarization, suggested that other channels whose activity causes depolarization, such as
> Na⁺ channels, were involved."

and summarises: "Their proposed resolution is indirect: Kcnk5b lowers intracellular K⁺, which
recruits Na⁺-channel activity, which depolarizes. They test it with Na⁺-channel inhibitors."

I retrieved the same full text (`PMC11018282/fullTextXML`, HTTP 200, **364,543 bytes** — matching
the author's figure exactly; read-level **full-text**) and read the Discussion. Jiang et al. state
their resolution in these words:

> "We propose that the increased K⁺-channel activity **first hyperpolarizes** the membrane
> potential, and this increase in membrane potential **immediately activates Na⁺ channels** to
> depolarize the cells. This hypothesis fits with our findings that we impair the increase in
> depolarization (Fig 5J) as well as Kcnk5b-enhanced growth with Na⁺ channel inhibitors
> (Fig 5K–5O)."

and report the test:

> "We expressed either control mCherry or *kcnk5b*-mCherry and then treated these fish with the
> Na⁺-channel inhibitors Vinpocetine ... and Dibucane ... We observed that inhibition of Na⁺
> channels **decreased depolarization in the fin bud as well as prevented Kcnk5b-induced increase
> in depolarization**."

Two things follow, and I separate the author's claim from my inference:

**(a) The two papers agree on the channel-intrinsic sign.** Jiang et al. explicitly place
**hyperpolarization first** — the same sign Perathoner et al. measured and the same sign eLife
2021 states. The reported depolarization is a *downstream, secondary* response of a different
conductance, at a later step. These are two variables at two stages, not two incompatible
readings of one variable. Characterising them as an "unresolved disagreement" about "the sign of
the pectoral Vm response" — as the claim does — **misdescribes the source**.

**(b) The mechanism attributed to Jiang in the source document is not the mechanism Jiang
state.** S14-deepen.md §3a says the resolution is that "Kcnk5b **lowers intracellular K⁺**, which
recruits Na⁺-channel activity". Jiang's Discussion says the trigger is the **hyperpolarization
itself** ("this increase in membrane potential immediately activates Na⁺ channels"), not the K⁺
concentration change. The substitution is what erases the agreement on sign: under Jiang's actual
mechanism, hyperpolarization is a **required intermediate**, so their model *affirms* Perathoner's
sign rather than contradicting it. **This is my reading of the retrieved Discussion against the
author's summary of the same document; both sentences are quoted above so a third party can
adjudicate without re-fetching.**

**Where I agree with the author and preserve the difference.** The modality criticism stands and
I confirmed it: Jiang et al.'s *in vivo* Vm readout is DiSBAC₂(3) dye fluorescence, uncalibrated
(36 occurrences of `DiSBAC`), with the authors' own caveats about dye penetration. Their
patch-clamp work — which I checked, since 70 occurrences of `mV` looked like it might contain
calibrated in-tissue values — is in **transfected HEK293T cells**, voltage-clamped at −80 mV in
Tyrode's solution; the four numeric mV values in the paper (−80, −100, 70, 10) are command
potentials, not resting potentials. **So there is still no calibrated resting Vm in mV for fin-bud
mesenchyme in any source I read**, and the source document's §3d request for exactly that
measurement is well-placed and unaffected by this defect. What falls is "unresolved
disagreement", not "unmeasured in calibrated units".

**Scope of my negative:** two full texts (PMC3894163, PMC11018282) read at full-text level and
string-searched for `hyperpolariz` (13 / 3 occurrences), `depolariz` (8 / 36), `dimer` (0 / 0),
`pectoral` (0 / 81), `single-channel` (0 / 0). I did not re-read eLife 2021 (PMC8110307) or
Sci Rep 2018 (PMC6039437), and I did not attempt the bioRxiv preprint
`10.1101/2024.03.27.587111`, so the source document's §3b claims about cell-type-specific
promoters and the optogenetic result are **unreviewed by me** and I take no position on them.

---

## 7. What survives, re-verified

I re-ran the source document's structure-absence test with its own controls
(`rest.uniprot.org/uniprotkb/search?...&fields=accession,xref_pdb&format=tsv`, read-level
**full-text**):

| Accession | `xref_pdb` | |
| --- | --- | --- |
| `Q6PFU3` (kcnk5b) | *empty* | — |
| `O95279` (human KCNK5/TASK-2, reviewed) | *empty* | — |
| `Q9NYG8` (KCNK4/TRAAK) | 3UM7;4I9W;4RUE;4RUF;4WFE;4WFF;4WFG;4WFH;7LJ4;7LJ5;7LJA;7LJB | positive control, 12 |
| `ZZZZZZ` | `The 'accession' filter value 'ZZZZZZ' has invalid format` | must-fail control: errors distinctly |
| `P57789` (KCNK10/TREK-2) | 4BW5;4XDJ;4XDK;4XDL;8QZ1;8QZ2;8QZ3;8QZ4 | positive control, 8 |

**Reproduces exactly**, controls valid in both directions. No experimental structure of kcnk5b.
The source document's retraction of the PDBe `best_structures` method in its §2a was the right
call and I have nothing to add to it.

Also surviving, and confirmed by me: `pectoral` appears **0 times** in Perathoner et al.
(142,283-byte full text) — the founding paper is silent on the pectoral fin; `two-fold` appears
**once**, in the sentence quoted; the author's quotation of it is verbatim and in context. And
§3.4 above: the *kcnk5b* null is viable with no loss-of-function phenotype, which **strengthens**
the one-sided window the author used.

**And the conclusion itself I did not overturn.** Within the scope I reviewed, I found no
intermediate-conductance kcnk5b variant series (the measured set remains {0, 1.0, ~2.0, ~2.0}), no
calibrated in-tissue Vm, and no study restricting kcnk5b manipulation to the pectoral appendage.
A reader should take "engineering kcnk5b itself for graded pectoral-restricted control is
unsupported" as still standing — on §3.4, on the absent variant series and on the absent
calibrated measurement, **not** on pLDDT and **not** on a sign disagreement.

---

## 8. Sources and read-levels

| Source | Identifier | Read-level |
| --- | --- | --- |
| S14-deepen.md (the document under review) | branch `claude/deepen-s14-potassium-channel-5miqg2` | **full-text** |
| AlphaFold DB prediction record, monomer | `AF-Q6PFU3-F1` v6 (69.5; bands 0.353/0.248/0.060/0.339) | **full-text** (API record, HTTP 200, 2,371 B) |
| 3D-Beacons summary, incl. homodimer model | `AF-0000000066331115` (62.82, HOMODIMER) | **full-text** (HTTP 200, 4,185 B) |
| AlphaFold DB per-residue pLDDT / coordinates | `confidence_v6.json`, `model_v6.pdb`; AlphaFill; UniProt; EBI FTP | **could-not-access** (403 / 403 / 404 / 404 — five routes, §5.4) |
| UniProt Q6PFU3 topology + sequence | TM 7–26, 116–137, 158–185, 229–250; Disordered 382–448; 448 aa | **full-text** (HTTP 200, 2,216 B) |
| UniProt `xref_pdb` with both controls | `Q6PFU3`, `O95279` → empty; `Q9NYG8` → 12; `P57789` → 8; `ZZZZZZ` → distinct error | **full-text** |
| Perathoner et al. 2014, *PLoS Genet* 10(1) e1004080 | PMID 24453984, PMC3894163 | **full-text** (142,283 B) |
| Jiang et al. 2024, *PLoS Biol*, doi 10.1371/journal.pbio.3002565 | PMID 38527087, PMC11018282 | **full-text** (364,543 B) |
| eLife 2021; Sci Rep 2018; bioRxiv 10.1101/2024.03.27.587111 | PMC8110307; PMC6039437; PPR830054 | **not read by me** — §6 scope note |

Working files and raw API records are in this session's scratchpad at
`/tmp/claude-0/-workspace-delphi-frontier/7a5094d4-0e9a-5f33-8ad1-3d6209a32699/scratchpad`, which
is ephemeral; every source is public and re-retrievable from the identifiers above. My
recomputation is committed beside this file as `challenge-91-recompute.py`.

## 9. What I did not establish

- Whether filter pLDDT actually exceeds 80. **Both directions remain unproven.** The §5.2
  arithmetic makes >80 the strong expectation for two-thirds of the model; it is not a
  measurement at residues 98–102 and 203–207. Blocked by egress policy, not data availability.
- The pLDDT at W169 and F241. Same blocker. My TM-helix argument (§5.3) is an inference from a
  retrieved topology annotation, not a confidence value.
- σ_V in any form, single-cell or tissue-mean. Still unmeasured in every source I read — which is
  the point of §3.1: the count is indeterminate, and I am not substituting a number of my own.
- Whether a dominant-negative acting on both *kcnk5b* and its redundant paralog *kcnk5a* could
  open the downward arm that §3.4 closes. `unknown`; no source I read tests it.
- The gain and noise of the Vm → fin-size transfer function (§3.3).
- Anything about the source document's §3b claims (cell-type-specific promoters, the optogenetic
  result) — I did not retrieve the preprint and take no position.
- Which *alf* allele carries W169L and which F241Y. I did not attempt it; the author's `unknown`
  stands unexamined by me.

---

**Verdict: REFUTED.** The arithmetic is right and the retrievals are right — I reproduced all of
them, including the two AFDB values the claim notes were not re-fetched. What fails is what the
numbers are taken to mean. The pLDDT leg compares a whole-chain mean against a ten-residue claim,
and the retrieved band fractions force the non-disordered two-thirds of the model above 79.5;
the mislocation argument, followed through against a retrieved topology annotation, places both
causal residues inside transmembrane helices and so runs backwards. The sign leg is contradicted
by the Discussion of the very paper the claim cites, which puts hyperpolarization first and
tests the secondary Na⁺-channel step pharmacologically. The recorded value counts intervals and
labels them setpoints. The claim's negative conclusion survives — but on §3.4's null allele and
on the absent variant series, not on the three reasons given.

```swarm-challenge
{"claim_id": 91, "outcome": "refuted", "reason": "Arithmetic and all retrievals reproduce exactly (17.1429 mV, 3.4286; AFDB 69.5/62.82 re-fetched and confirmed), but the pLDDT leg sets a whole-chain mean against a ten-residue claim when the retrieved band fractions force the non-very-low 66.1% of the model above 79.5 pLDDT and retrieved UniProt topology places both causal residues W169/F241 inside TM helices 158-185 and 229-250 rather than in the disordered 382-448 region, while the sign leg is contradicted by Jiang 2024's own Discussion, which puts hyperpolarization first and tests the secondary Na+-channel depolarization with two inhibitors; the recorded value also counts intervals and labels them setpoints.",
  "corrected_value": "~4.4 distinguishable setpoints at sigma_V = 5 mV (17.14 mV window / 5 mV = 3.43 intervals, +1 for endpoints), and indeterminate overall because sigma_V is unmeasured and the one piece of evidence cited for its large end is single-cell scatter, which is not the discrimination step for a tissue-integrated output",
  "depends_on": ["AFDB record AF-Q6PFU3-F1 v6: globalMetricValue 69.5, fractionPlddtVeryLow 0.339, fractionPlddtVeryHigh 0.353, length 448 (re-fetched by me, HTTP 200)", "3D-Beacons record AF-0000000066331115: AlphaFold DB, HOMODIMER, confidence_avg_local_score 62.82 (re-fetched by me, HTTP 200)", "UniProt Q6PFU3 topology features: Transmembrane 7-26, 116-137, 158-185, 229-250; Region Disordered 382-448", "UniProt/AFDB Q6PFU3 448-aa sequence: residue 169=W, 241=F, TIGYG at 98-102, TVGFG at 203-207", "Perathoner et al. 2014 (PMC3894163, full-text): 'almost two-fold increase in K+ conductance'; E_K '-90 to -100 mV' in Xenopus oocytes; revertant null allele viable and fertile with no loss-of-function phenotype (kcnk5a redundancy); 0 occurrences of 'pectoral'", "Jiang et al. 2024 (PMC11018282, full-text): Discussion 'the increased K+-channel activity first hyperpolarizes the membrane potential, and this increase in membrane potential immediately activates Na+ channels to depolarize the cells'; Vinpocetine/Dibucane Na+-channel inhibitor experiments; in vivo Vm by uncalibrated DiSBAC2(3) dye; patch clamp in HEK293T cells only", "S14-D parallel-conductance model and its parameters: E_K=-100 mV, E_B=0 mV (assumed), Vm_wt=-40 mV (swept), sigma_V=5 mV (unmeasured)", "Per-residue pLDDT at residues 98-102, 203-207, 169 and 241: could-not-access (HTTP 403 on alphafold.ebi.ac.uk/files/ and alphafill.eu, 404 on three other routes) — so neither this verdict nor the claim can assert a filter-local pLDDT value"]}
```
