# Challenge 216 — adversarial review of CHALLENGER A (axmlig) on claims 91/167

**Claim under review (claim_id 216).** "CHALLENGER A (axmlig) on claims 91/167: arithmetic
reproduces (17.1429 mV, 3.4286; AFDB 69.5/62.82 re-fetched by challenger). But whole-chain mean
is set against a ten-residue claim; retrieved band fractions force the non-very-low 66.1% of the
model above 79.5; UniProt topology puts W169/F241 inside TM helices 158-185 and 229-250, not the
disordered 382-448 region; Jiang 2024 Discussion puts hyperpolarization first. Corrected: ~4.4
setpoints (3.43 intervals +1 endpoints) at sigma_V 5 mV; indeterminate since sigma_V unmeasured.
Harvester: 17.14/5=3.43 reproduces; per-residue pLDDT NOT re-fetched (AFDB /files endpoint
returned HTML to harvester)."

**Recorded evidence level:** derived. **Recorded value:** 4.4 setpoints.
**Source:** branch `claude/challenge-s14-falls-kcnk5b-axmlig`, `docs/research/fish/challenge-91.md`
(530 lines, plus `challenge-91-recompute.py`). I fetched that branch and read the full document
and the script before writing this. Read-level **full-text**.

**Date of this review:** 2026-11-04. Every retrieval below was made by me on that date, in this
session, from the identifiers given in §8.

---

## Verdict up front: WEAKENED

Everything the challenger says it reproduced, it reproduced, and I reproduced all of it again
independently. Three of its findings against claim 91 survive my attack. But the challenger
corrected a fencepost in the denominator while leaving the **numerator unexamined**, and the
numerator is where the error lives: the 17.14 mV window is a *simulated* quantity standing in for
a *measured* one that is reported in the very paper supplying the 2-fold input, and the two
disagree by a factor of several. Having argued the quantity is indeterminate, the challenger then
records a point value anyway, and records it as a non-integer count of discrete positions. Its
structured `outcome` field also contradicts its own prose.

I did not overturn the challenger's core findings against claim 91. I am weakening its corrected
value, three of its stated evidence bases, and its outcome token.

Two of my attacks **failed outright** (§6) and I report them as prominently as the ones that
landed.

---

## 1. Independent arithmetic — rederived, not copied

I did not read `challenge-91-recompute.py` or the challenger's §1 tables before deriving this. I
set up the two-branch divider from current balance myself:

```
I = g_K(Vm - E_K) + g_B(Vm - E_B) = 0
  => Vm = (g_K E_K + g_B E_B)/(g_K + g_B)
  => with x = g_K/g_B:  Vm(x) = (x E_K + E_B)/(x + 1),  x(Vm) = (Vm - E_B)/(E_K - Vm)
```

With `E_K = -100`, `E_B = 0`, `Vm_wt = -40`, in exact rationals (`fractions.Fraction`, so no
floating-point slack):

```
x0            = -40/-60                     = 2/3
x at R = 2    = 4/3
Vm            = (4/3 * -100)/(7/3) = -400/7 = -57.142857... mV
W = |dVm|     = 120/7                       =  17.142857... mV
W/sigma at 5  = 24/7                         =   3.428571...
W/sigma + 1                                  =   4.428571...
```

**The challenger's arithmetic is exactly right, and so is the harvester's `17.14/5 = 3.43`.** My
script is committed beside this file as `challenge-216-recompute.py` (dependency-free; run with
`python3 -I docs/research/fish/challenge-216-recompute.py`).

### 1.1 Defect 1 — the corrected value is not a count (and the +1 carries a convention)

The challenger's own diagnosis against claim 91 is that `W/sigma` counts **intervals** and was
labelled **setpoints**. I agree, and that finding survives. But the replacement value inherits a
milder form of the same error.

A number of distinguishable positions is a **count**. It is an integer. `4.4286` is not a count of
anything; it is a ratio plus one. From the challenger's own model and parameters the number of
distinguishable setpoints is

```
floor(W/sigma) + 1 = floor(3.4286) + 1 = 4
```

Not 4.4. The fractional part cannot be occupied.

Worse, the `+1` rests on an undeclared convention: that two setpoints separated by **1 sigma** are
distinguishable. That is a weak criterion — at 1 sigma separation two Gaussians overlap heavily
and single-trial discrimination is poor. The conventional resolvability threshold in
signal-detection terms is `d' = 2`, i.e. **2 sigma** spacing. Relaxing the hidden assumption (my
computation, exact rationals, §A of my script):

| spacing criterion | positions at sigma_V = 5 mV, W = 120/7 mV |
| --- | --- |
| 1 sigma (the challenger's implicit choice) | floor(3.4286) + 1 = **4** |
| 2 sigma (`d' = 2`, conventional resolvability) | floor(1.7143) + 1 = **2** |

**The spacing convention alone spans 2 to 4 setpoints — a wider range than the 3.43 -> 4.43
correction the challenger offers as its headline arithmetic finding.** The fencepost is real; it
is also the smallest of the three uncertainties in this number, and it is presented as the largest.

*This is my computation from the challenger's stated model, not a measurement.*

---

## 2. Defect 2 — the proxy the challenger missed: a simulated window standing in for a measured one

The challenger asked question 2 of its own brief ("is a proxy standing in for the quantity that
matters?") and answered with `E_K`, `E_B` and the Vm -> fin-size gain. It did not ask whether the
**window itself** is a proxy. It is.

`W = 17.14 mV` is an output of the divider simulation, driven by the "almost two-fold" conductance
figure. But Perathoner et al. also **measured** the membrane-potential consequence, and state it
in the body text (read-level **full-text**, PMC3894163, 142,283 bytes — byte count matches the
challenger's exactly; verbatim):

> "Consistently, the mutant channels lead to stronger hyperpolarization causing a shift in the
> membrane potential towards **-90 to -100 mV**, the equilibrium potential for K+ in *Xenopus*
> oocytes."

The challenger quotes the tail of this sentence — it uses it to source `E_K = -100` — and does not
notice that the head of the same sentence reports the measured Vm endpoint. **The simulation and
the measurement disagree.**

My computation, inverting the challenger's own divider at `R = 2`, `E_K = -100`, `E_B = 0`:

| measured endpoint | x required at mutant | implied x_wt | implied Vm_wt | implied W |
| --- | --- | --- | --- | --- |
| -90 mV | 9.0 | 4.50 | **-81.8 mV** | 8.2 mV |
| -95 mV | 19.0 | 9.50 | -90.5 mV | 4.5 mV |
| -99 mV | 99.0 | 49.50 | -98.0 mV | 1.0 mV |

The divider at `Vm_wt = -40` predicts a mutant endpoint of **-57.1 mV**. The measured endpoint is
**-90 to -100 mV**. To reach -90 on a 2-fold conductance change the wild-type-injected oocyte must
already sit near -82 mV, at which point the window is **8.2 mV, not 17.1** — i.e. `floor(1.63)+1 =
2` setpoints. If instead the measured shift is read against a non-expressing baseline, the window
is 40-60 mV and the count is 9 to 13 setpoints:

| baseline | endpoint | W | setpoints at sigma = 5 mV, 1-sigma spacing |
| --- | --- | --- | --- |
| -40 mV | -90 | 50 mV | 11 |
| -40 mV | -100 | 60 mV | 13 |
| -60 mV | -90 | 30 mV | 7 |
| -80 mV | -90 | 10 mV | 3 |

**So W is unpinned across roughly 8 to 60 mV — a factor of ~7 — before sigma_V is considered at
all.** The implied setpoint count brackets both the claim's 3.4 and the challenger's 4.4 from both
sides. *This is my inference from the retrieved sentence and the challenger's own model. The
numeric wild-type-injected oocyte Vm is in Figure 5D only; that panel's values are* **could-not-access**
*to me and I have not invented one — the table above sweeps the baseline rather than asserting it.*

**There is a mechanistic reason from the same paper not to trust the divider here.** Perathoner et
al. report (verbatim, full-text) that in the mutants the conductance increase "is accompanied by
**reduced outward rectification** (Figure 5C) suggesting that the change in K+ conductance results
from altered biophysical features of Kcnk5b rather than a simple increase in the number of
channels". A change in I-V *shape* cannot be represented by a scalar conductance ratio in a linear
two-branch divider. The single parameter `R = 2` is itself a proxy for a shape change, and reduced
outward rectification means relatively more K+ conductance at negative potentials — the direction
that makes the real resting-Vm effect **larger** than the scalar model predicts, which is what the
measured -90/-100 endpoint shows.

**Consequence for the recorded value.** The challenger's conclusion "indeterminate" is correct and
I uphold it — but the dominant term is `W`, not `sigma_V`, and the challenger's `corrected_value`
of "~4.4 setpoints at sigma_V = 5 mV" propagates a point estimate that its own cited source does
not support. A value field that carries both a number and the word "indeterminate" will be read
for the number.

---

## 3. Defect 3 — the 79.5 pLDDT bound is near-vacuous, and the inversion carries no weight

I re-fetched the AFDB record myself: `https://alphafold.ebi.ac.uk/api/prediction/Q6PFU3`, HTTP 200,
2,371 bytes, read-level **full-text**. `entryId AF-Q6PFU3-F1`, `latestVersion 6`,
`globalMetricValue` **69.5**, `fractionPlddtVeryHigh` **0.353**, `fractionPlddtConfident` **0.248**,
`fractionPlddtLow` **0.060**, `fractionPlddtVeryLow` **0.339** (sum exactly 1.000),
`uniprotEnd` 448, `modelCreatedDate` 2025-08-01. Every figure the challenger reports is confirmed.

I then redid its §5.2 bound from the band fractions alone:

```
total sum        = 69.5 * 448                       = 31,136
n(very low)      = 0.339 * 448                      =    151.872
that band is <50 by definition: its sum  <  50 * 151.872  =  7,593.6
remaining 296.128 residues sum  >  31,136 - 7,593.6       = 23,542.4
mean of the non-very-low 66.1%  >  23,542.4/296.128       =     79.5008
```

**Reproduces to four decimals.** The bound is arithmetically correct. It is also almost empty of
information, which the challenger does not check. The band *composition* alone — with no use of
the global mean whatsoever — already forces the non-very-low mean into a range, by the band
definitions:

```
min = (158.14*90 + 111.10*70 +  26.88*50)/296.128 = 78.8654
max = (158.14*100 + 111.10*90 + 26.88*70)/296.128 = 93.5250
```

**The global mean of 69.5 contributes 79.5008 - 78.8654 = 0.64 pLDDT.** Any protein with 35.3% of
residues above 90 and 24.8% between 70 and 90 has its non-very-low fraction averaging at least
78.9, whatever its global mean is. The challenger presents this as "a **hard lower bound** from the
claim's own retrieved numbers", and it is — but it is a restatement of the band definitions, not a
finding about this model.

And it cannot bear on the question at issue. From the same fractions: **178.8 residues (39.9% of
the chain) are below 70**, and as many as 289.9 (64.7%) could be below 90. Ten filter residues can
sit anywhere in that mass. A 296-residue mean is no more capable of speaking to residues 98-102 and
203-207 than the 448-residue mean the challenger correctly faults claim 91 for using. The sentence
"the two filter motifs are in it or they are nowhere" is rhetoric, not inference.

**What survives:** the challenger's actual finding against claim 91 — that "69.5, not >80" sets a
whole-chain mean against a ten-residue statement, and that the claim stripped the source
document's own hedge ("I could not confirm that") — is **sound and I uphold it**. The *inversion*
("the record ... supports the thing it is offered as refuting") adds nothing, and the structured
`reason` field leads with the inversion.

### 3.1 The right proxy for a dimeric selectivity filter is not per-residue pLDDT

Both claim 91 and the challenger argue over monomer per-residue pLDDT at the filter motifs. For an
obligate-dimeric K2P channel the conducting selectivity filter is assembled **across the subunit
interface** — P1 of one chain with P2 of the other — so the quantity that bears on filter accuracy
is **inter-chain** accuracy (PAE / ipTM) for the assembly, not per-residue pLDDT of a monomer. On
that reading the 62.82 homodimer figure, which the challenger dismisses in §5.5 as changing
nothing, is closer to the right quantity than the 69.5 it spends a section on.

**Read-level and honesty note, stated plainly: the K2P dimeric-filter architecture is remembered
structural biology, not retrieved.** I checked and `dimer` occurs **0 times in both papers**
(my string counts on tag-stripped full texts — 0/0, matching the challenger's). I could not
retrieve the homodimer coordinates or any PAE file (§6.2). So I flag this exactly as the original
S14-D author flagged their own K2P-dimer statement — as unsourced — and I draw no numeric
conclusion from it. It names a better proxy; it does not measure one.

I confirmed the homodimer record independently via two endpoints, and I preserve a discrepancy
between them rather than averaging it away: 3D-Beacons
(`www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/Q6PFU3.json`, HTTP 200, 4,185 bytes)
and `alphafold.ebi.ac.uk/api/uniprot/summary/Q6PFU3.json` (HTTP 200, 1,946 bytes) both give
`AF-0000000066331115`, provider AlphaFold DB, `oligomeric_state` **HOMODIMER**,
`confidence_avg_local_score` **62.82**, and both list `AF-Q6PFU3-F1` as MONOMER at **69.5**. They
give **different creation dates** for the homodimer — 2025-12-25 and 2026-02-19 — so the record has
churned since the challenger read it. Not material to any number here; recorded because it means
the figure is not frozen.

---

## 4. Defect 4 — "retrieved UniProt topology" is a prediction in an unreviewed entry

I fetched the same record: `rest.uniprot.org/uniprotkb/Q6PFU3.json` with topology and sequence
fields, HTTP 200, 2,363 bytes, read-level **full-text**. Every feature the challenger reports is
there, exactly:

| Feature | Range | Evidence |
| --- | --- | --- |
| Transmembrane, Helical | 7-26 | ECO:0000256, source **SAM** |
| Transmembrane, Helical | 116-137 | ECO:0000256, source **SAM** |
| Transmembrane, Helical | **158-185** | ECO:0000256, source **SAM** |
| Transmembrane, Helical | **229-250** | ECO:0000256, source **SAM** |
| Region, Disordered | **382-448** | ECO:0000256, source **SAM** |

And the sequence facts: 448 aa, **byte-identical to the AFDB sequence** (I compared them),
`TIGYG` once at 98-102, `TVGFG` once at 203-207, residue 169 = W, residue 241 = F. Local context
re-extracted by me: `FICTIVFLLWGFLVHLIIPAF` (160-180, W at 169), `YLGLAWLSLFFSWNVHMVV`
(232-250, F at 241).

**What the challenger does not disclose:** Q6PFU3 is `entryType` **"UniProtKB unreviewed
(TrEMBL)"**, and all five features carry **ECO:0000256** — "match to sequence model evidence used
in automatic assertion" — with source **SAM**, a sequence-analysis method. There is no curated or
experimental topology here. This is a predictor's output.

That matters for the specific inference drawn. The challenger's argument is: topology puts the
causal residues in TM helices, and "transmembrane helices are the best-determined elements of an
AlphaFold model of a membrane protein", therefore the mislocation argument runs backwards. But a
sequence-based TM predictor and AlphaFold draw on the **same** hydrophobicity and homology signal.
Using one to vouch for the local accuracy of the other is not independent corroboration. The
structured `reason` field says "retrieved UniProt topology puts W169/F241 inside TM helices", which
reads as a database fact of record.

**The placement itself survives, and I say so.** Perathoner et al. state it independently
(verbatim, read-level **full-text**): "These models revealed that the affected amino acids are
positioned in **two distinct TM domains** towards the cytoplasmic side of the protein (Figure 5A)."
The ordering is also the canonical two-pore arrangement — M1(7-26), P1 filter(98-102), M2(116-137),
M3(158-185), P2 filter(203-207), M4(229-250) — and both residues sit mid-helix in strongly
hydrophobic stretches, which I re-extracted above. And I reproduced the structure-absence test with
its controls (`rest.uniprot.org/uniprotkb/search?...&fields=accession,reviewed,xref_pdb&format=tsv`,
read-level **full-text**): `Q6PFU3` unreviewed, `xref_pdb` **empty**; `O95279` reviewed, empty;
`Q9NYG8` -> **12** PDB entries; `P57789` -> **8**; must-fail control `ZZZZZZ` -> HTTP **400** with
a distinct format error. Controls valid in both directions; no experimental structure of kcnk5b.

So this is an **evidence-level defect, not a factual one**: the conclusion is right, the
corroboration is two predictions rather than a retrieved record, and the claim as recorded does not
say so. Perathoner's own statement derives from homology models, so it is a third prediction — the
right read-level for "W169 is in a TM helix" is *strongly predicted, consistent across three
methods, never observed*.

---

## 5. Defect 5 — Jiang do not "resolve" the sign; they propose a mechanism they never measure

I fetched the same full text (`PMC11018282/fullTextXML`, HTTP 200, **364,543 bytes** — byte count
matches the challenger's exactly, read-level **full-text**) and ran my own counts on the
tag-stripped text (177,989 chars): `hyperpolariz` **3**, `depolariz` **36**, `dimer` **0**,
`pectoral` **81**, `DiSBAC` **36**, `Vinpocetine` **14**, `Dibuca` **9**. Every count the
challenger reports is reproduced.

Because there are only three, I can print **every** occurrence of `hyperpolariz` in Jiang et al.
and let a reader adjudicate without re-fetching:

1. "The observed increase in depolarization caused by *kcnk5b*, a leak channel that **should
   promote hyperpolarization**, suggested that other channels whose activity causes depolarization,
   such as Na+ channels, were involved." — *statement of the paradox.*
2. "In regards to the in vivo electrophysiology, since K+-leak channels generally result in the
   outward flow of K+ ions, **this should hyperpolarize** the membrane potential as the cytoplasmic
   side becomes more negatively charged..." — *statement of general expectation.*
3. "**We propose** that the increased K+-channel activity **first hyperpolarizes** the membrane
   potential, and this increase in membrane potential immediately activates Na+ channels to
   depolarize the cells." — *a proposal.*

The challenger's quotation of (3) is **verbatim and in context**; I confirm it. But all three
mentions are expectation or hypothesis. **Jiang et al. never measure hyperpolarization.** Their
measured in vivo signal is depolarization (36 mentions, by uncalibrated DiSBAC2(3) dye), and their
pharmacology (Vinpocetine/Dibucaine) tests the *downstream* Na+ step, not the hyperpolarizing first
step. A proposed intermediate supported by pharmacology on the step after it is a **reconciliation**,
not a resolution.

So the challenger's §6 heading ("the source resolves it") and its structured `reason` ("the sign
leg is **contradicted** by Jiang 2024's own Discussion") overstate the record. The accurate status
is: *the two papers' measurements are opposite in sign and in different systems; Jiang offer a
mechanism under which both are correct; the hyperpolarizing first step of that mechanism is
unmeasured in the target tissue.* Claim 91's phrase "unresolved disagreement" is the wrong phrase —
the challenger is right that the papers are not in conflict — but it is not **contradicted by a
measurement**, which is what the challenger's reason field asserts.

**A point FOR the challenger, on a basis it did not give.** I reproduced `pectoral` = **0** in
Perathoner et al., and I ran a scan the challenger did not: **zero** sentences in Jiang et al.
contain both `pectoral` and either `depolariz` or `membrane potential`. So there is not one
calibrated pectoral-fin Vm measurement in either paper, let alone two in disagreement. Claim 91's
"sign of pectoral Vm response in unresolved disagreement: Perathoner 2014 ... vs Jiang 2024"
attributes a pectoral measurement to a paper that never mentions the pectoral fin. **The
challenger's defect 4 is right in its conclusion and wrong in its stated basis** — the leg fails
because there is no pectoral measurement to disagree about, not because Jiang's Discussion resolved
anything.

*Scope of my negative:* two full texts (PMC3894163, PMC11018282) at full-text level, string-scanned
for the terms above. I did not read eLife 2021 (PMC8110307), Sci Rep 2018 (PMC6039437), or the
bioRxiv preprint 10.1101/2024.03.27.587111, so I take no position on anything resting on those —
including the challenger's §3.4 null-allele finding beyond the Perathoner passage I verified below.

---

## 6. Attacks that FAILED

### 6.1 I could not break the TM placement

My best shot was §4: the UniProt features are automatic (ECO:0000256/SAM) in an unreviewed entry,
so I tried to show the helix boundaries were unreliable and that W169 or F241 might fall outside
them — 158-185 is 28 residues, long for a single TM helix, which looked like a predictor merging
two elements. It held. The six-element order is the canonical K2P arrangement; both residues sit
mid-helix in uninterrupted hydrophobic stretches I re-extracted from the retrieved sequence; and
Perathoner et al. independently place them "in two distinct TM domains towards the cytoplasmic
side". **W169 in M3 and F241 in M4 stands.** I reduced the challenger's evidence level, not its
conclusion.

### 6.2 I could not get per-residue pLDDT either — six routes

This would settle ">80 at the filters" directly and end the whole dispute. Read-level:
**could-not-access**. Scope of the negative, every route I tried on 2026-11-04:

| Route | Result |
| --- | --- |
| `alphafold.ebi.ac.uk/files/AF-Q6PFU3-F1-model_v6.cif` | **HTTP 403**, 134-byte `<title>403</title>` proxy page |
| `alphafold.ebi.ac.uk/files/AF-Q6PFU3-F1-confidence_v6.json` | **HTTP 403**, same body |
| `alphafold.ebi.ac.uk/files/AF-Q6PFU3-F1-model_v6.pdb` | **HTTP 403**, same body |
| `alphafold.ebi.ac.uk/files/AF-0000000066331115-model_v1.cif` (homodimer, new route) | **HTTP 403** |
| `alphafill.eu/v1/aff/Q6PFU3` | connection failed, HTTP **000** — host not permitted |
| `www.ebi.ac.uk/pdbe/static/alphafold/AF-Q6PFU3-F1-model_v6.cif` (new route) | HTTP **404** |

The `/api/` paths on the same host return 200, so this is **egress policy, not data availability** —
the harvester's note that the "/files endpoint returned HTML" is the same 134-byte 403 page I got,
and it is correctly characterised. A runner with egress to `alphafold.ebi.ac.uk/files/` settles
this in one request, and the PAE file at `paeDocUrl` (same blocked path) would settle §3.1.
**I therefore cannot assert filter pLDDT in either direction, and neither can the challenger.**
Its §9 says so; its structured `reason` field does not.

### 6.3 A point in claim 91's favour that neither party noticed

I swept `Vm_wt` to see whether -40 mV was chosen to flatter the result. It is the **argmax**: over
`Vm_wt` in [-99.9, -0.1] mV the 2-fold window peaks at **17.157 mV at Vm_wt = -41.4 mV**, so
17.143 mV is essentially the **maximum attainable window**, not a typical one. That is generous to
the *feasibility* side, i.e. conservative for a FALLS verdict. Neither the S14-D author nor the
challenger states this, and it cuts in claim 91's favour. (It also means every entry in the
challenger's `Vm_wt` sweep lies below the headline — correct, and worth recording as the structural
reason why.)

---

## 7. Is the evidence level honest?

**"Derived" is the right level and the challenger's internal labelling is good.** It marks its
inferences as inferences in the prose, separates them from retrievals, states read-levels per
source, reports a failed attack (§3.4) prominently, and lists seven things it did not establish.
That is better practice than claim 91 as recorded. Three labelling faults, all in the structured
block rather than the prose:

1. **`corrected_value` asserts a number and indeterminacy in one field.** "~4.4 distinguishable
   setpoints at sigma_V = 5 mV ... and indeterminate overall" — one of those propagates downstream,
   and it will be the number. If the quantity is indeterminate the value field should say so and
   put the conditional figure in the reason.
2. **`outcome: "refuted"` contradicts the prose.** The document says the conclusion "survives", that
   it "did not overturn" it, that in one respect it "strengthened" it; the commit message says
   "**refuted as argued, not as concluded**". The single token says `refuted`, which a consumer will
   read as the FALLS verdict having fallen. For "value corrected, stated reasons fail, conclusion
   upheld and strengthened" the faithful token is **`weakened`**. This is the one defect of claim 216
   that changes what a downstream reader does.
3. **The `reason` field states as retrieved fact two things the prose correctly hedges** — the pLDDT
   inversion (§3) and "retrieved UniProt topology" (§4).

---

## 8. What survives, re-verified by me

- **All arithmetic.** 120/7 = 17.142857 mV; 24/7 = 3.428571; the pLDDT bound at 79.5008; the
  compressiveness sequence (my independent rerun: -40.00 -> -57.14 -> -72.73 -> -84.21 -> -91.43 ->
  -95.52, steps -17.14/-15.58/-11.48/-7.22/-4.09). Reproduces to the digit.
- **All retrievals.** Both AFDB values and all four band fractions; HOMODIMER at 62.82 from two
  endpoints; UniProt topology and sequence; the 448-aa sequence byte-identical between AFDB and
  UniProt; `TIGYG` at 98-102 and `TVGFG` at 203-207 each exactly once; residue 169 = W, 241 = F;
  both full-text byte counts to the byte; all nine string counts; the structure-absence test with
  both positive controls and a distinctly-failing must-fail control.
- **The pLDDT category error against claim 91** (a whole-chain mean cannot refute a ten-residue
  statement) and **the stripped hedge** — both sound, both upheld.
- **The TM placement of W169 and F241** — sound, on three mutually non-independent predictions.
- **That claim 91's "unresolved disagreement" misdescribes the record** — sound; see §5 for the
  corrected basis.
- **The null-allele point (challenger §3.4).** I verified the passage verbatim (full-text): the
  revertant `j131x8` is "predicted to lack 3 of the 4 transmembrane (TM) domains ... a **null
  mutation** for *kcnk5b*. **Homozygotes harboring the deletion are viable and fertile** ... the
  **lack of a loss-of-function phenotype** in normal development may be due to functional redundancy
  between the paralogs." The challenger reported this as an attack of its own that **failed**, and
  recorded it as a point for the author. I confirm the passage and the direction. Reporting one's
  own failed attack this prominently is the practice that made this document worth reviewing, and I
  want it recorded as such.
- **The conclusion of claim 91** — that engineering kcnk5b for graded pectoral-restricted control is
  unsupported — I did not overturn either. My §2 widens the window uncertainty in *both* directions
  (8 to 60 mV), which makes the arithmetic leg indeterminate rather than favourable; and there is
  still no intermediate-conductance variant series, no calibrated in-tissue Vm, and no pectoral-
  restricted manipulation in anything I read.

| Source | Identifier | Read-level |
| --- | --- | --- |
| challenge-91.md + challenge-91-recompute.py (under review) | branch `claude/challenge-s14-falls-kcnk5b-axmlig`, 530 + 61 lines | **full-text** |
| AlphaFold DB prediction record | `AF-Q6PFU3-F1` v6; 69.5; bands 0.353/0.248/0.060/0.339 | **full-text** (HTTP 200, 2,371 B) |
| 3D-Beacons summary | `AF-0000000066331115`, HOMODIMER, 62.82 | **full-text** (HTTP 200, 4,185 B) |
| AFDB uniprot summary (second endpoint) | same two models; homodimer date differs | **full-text** (HTTP 200, 1,946 B) |
| UniProt Q6PFU3 topology + sequence | unreviewed (TrEMBL); 5 features, all ECO:0000256/SAM | **full-text** (HTTP 200, 2,363 B) |
| UniProt `xref_pdb` + 2 positive + 1 must-fail control | Q6PFU3/O95279 empty; Q9NYG8 12; P57789 8; ZZZZZZ HTTP 400 | **full-text** |
| Per-residue pLDDT / PAE / coordinates (monomer and homodimer) | six routes, §6.2 | **could-not-access** (403 x4, 000, 404) |
| Perathoner et al. 2014, *PLoS Genet* 10(1) e1004080 | PMID 24453984, PMC3894163 | **full-text** (142,283 B) |
| Perathoner Figure 5D numeric oocyte Vm values | figure panel only | **could-not-access** |
| Jiang et al. 2024, *PLoS Biol* 22(3) e3002565 | PMID 38527087, PMC11018282 | **full-text** (364,543 B) |
| eLife 2021; Sci Rep 2018; bioRxiv 10.1101/2024.03.27.587111 | PMC8110307; PMC6039437 | **not read by me** — §5 scope note |
| K2P dimeric selectivity-filter architecture (§3.1) | none | **remembered, not retrieved** — `dimer` = 0/0 in both papers |

## 9. What I did not establish

- Filter pLDDT, in either direction. Blocked by egress (§6.2), not by data availability.
- Inter-chain accuracy (PAE/ipTM) for the homodimer — the quantity §3.1 argues is the right one.
  Same blocker. So I name a better proxy without measuring it.
- The wild-type-injected oocyte resting Vm, which would collapse the 8-60 mV window range in §2 to
  a single number. It is in Perathoner Figure 5D; `unknown` to me, and I did not invent one.
- `sigma_V` in any form. Still unmeasured in every source I read. I uphold "indeterminate" and
  substitute no number of my own.
- Whether a dominant-negative acting on both *kcnk5b* and *kcnk5a* reopens the downward arm the
  challenger's §3.4 closes. `unknown`; no source I read tests it.
- Anything resting on eLife 2021, Sci Rep 2018, or the bioRxiv preprint.

---

**Verdict: WEAKENED.** Every number and every retrieval in claim 216 reproduces independently, its
three findings against claim 91 survive in substance, and its practice — labelled inferences, stated
read-levels, a prominently reported failed attack — is better than the claim it reviews. What fails
is the corrected value and three of the stated bases. `4.4 setpoints` is not a count (4 at 1-sigma
spacing, 2 at the conventional 2-sigma criterion), and more importantly the window it divides is a
simulated 17.14 mV standing in for a measured endpoint of -90 to -100 mV in the same paper that
supplies the 2-fold input, leaving W unpinned from ~8 to ~60 mV — so the challenger corrected the
fencepost and left the larger error term, then recorded a point value anyway. The 79.5 pLDDT bound
is forced to within 0.64 by the band definitions alone and cannot speak to ten residues when 39.9%
of the chain sits below 70. The "retrieved UniProt topology" is an automatic annotation
(ECO:0000256/SAM) in an unreviewed entry, corroborated only by two further predictions. And Jiang
et al. **propose** hyperpolarization-first in a Discussion and never measure it, so the sign leg
fails for a different reason than the one given: there is no pectoral Vm measurement in either paper
to disagree about. The challenger's own conclusion — indeterminate — is right, on stronger grounds
than it gave; its `outcome: refuted` token contradicts its own prose and should read `weakened`.

```swarm-challenge
{"claim_id": 216, "outcome": "weakened", "reason": "Every number and retrieval in the challenge reproduces independently and its three findings against claim 91 survive in substance, but the corrected value fails on four counts: 4.4 is not a count of discrete positions (4 at 1-sigma spacing, 2 at the conventional 2-sigma d'=2 criterion); the 17.14 mV window it divides is a simulated quantity standing in for a measured endpoint of -90 to -100 mV reported in the same Perathoner sentence that supplies E_K, which under the challenger's own divider at R=2 requires Vm_wt = -81.8 mV and leaves W unpinned from ~8 to ~60 mV, a factor of 7 that dwarfs the fencepost correction; the 79.5 pLDDT bound is forced to within 0.64 pLDDT by the band definitions alone and cannot bear on ten residues when 39.9% of the chain is below 70; and the UniProt topology is an automatic ECO:0000256/SAM annotation in an unreviewed TrEMBL entry, not a retrieved record, while Jiang 2024 only PROPOSE hyperpolarization-first and never measure it, so that leg fails because neither paper contains a pectoral Vm measurement rather than because the Discussion contradicts the claim; outcome token should read weakened, matching the challenger's own prose that claim 91's conclusion survives.",
  "corrected_value": null,
  "depends_on": ["AFDB record AF-Q6PFU3-F1 v6: globalMetricValue 69.5, fractionPlddtVeryHigh 0.353, fractionPlddtConfident 0.248, fractionPlddtLow 0.060, fractionPlddtVeryLow 0.339, length 448 (re-fetched by me, HTTP 200, 2371 B)", "3D-Beacons and AFDB uniprot-summary records: AF-0000000066331115, AlphaFold DB, HOMODIMER, confidence_avg_local_score 62.82 (re-fetched by me from two endpoints, HTTP 200; the two endpoints give different creation dates, 2025-12-25 vs 2026-02-19)", "UniProt Q6PFU3 is entryType 'UniProtKB unreviewed (TrEMBL)' and all five topology features (Transmembrane 7-26, 116-137, 158-185, 229-250; Region Disordered 382-448) carry evidence ECO:0000256 source SAM, i.e. automatic annotation by a sequence-analysis method", "UniProt/AFDB Q6PFU3 448-aa sequence, byte-identical between the two: residue 169=W, 241=F, TIGYG once at 98-102, TVGFG once at 203-207, hydrophobic context FICTIVFLLWGFLVHLIIPAF at 160-180 and YLGLAWLSLFFSWNVHMVV at 232-250", "Perathoner et al. 2014 (PMC3894163, full-text, 142283 B): 'the mutant channels lead to stronger hyperpolarization causing a shift in the membrane potential towards -90 to -100 mV, the equilibrium potential for K+ in Xenopus oocytes'; 'almost two-fold increase in K+ conductance'; the increase 'is accompanied by reduced outward rectification (Figure 5C)'; 'the affected amino acids are positioned in two distinct TM domains towards the cytoplasmic side'; revertant j131x8 null viable and fertile with no loss-of-function phenotype (kcnk5a redundancy); 0 occurrences of 'pectoral'", "Jiang et al. 2024 (PMC11018282, full-text, 364543 B): all three occurrences of 'hyperpolariz' are expectation or hypothesis, the third being 'We propose that the increased K+-channel activity first hyperpolarizes the membrane potential...'; 36 'depolariz'; 36 'DiSBAC'; 14 'Vinpocetine'; 9 'Dibuca'; 0 sentences containing both 'pectoral' and 'depolariz'/'membrane potential'", "S14-D parallel-conductance model and its parameters: E_K=-100 mV, E_B=0 mV (assumed), Vm_wt=-40 mV (swept; I find it is the argmax of the 2-fold window, max 17.157 mV at -41.4 mV), sigma_V=5 mV (unmeasured)", "Per-residue pLDDT and PAE at residues 98-102, 203-207, 169 and 241, monomer and homodimer: could-not-access for me as for the challenger (HTTP 403 on four alphafold.ebi.ac.uk/files/ paths, HTTP 000 on alphafill.eu, HTTP 404 on ebi.ac.uk/pdbe/static/alphafold) - so no party to this dispute can assert a filter-local confidence value", "The 1-sigma-spacing distinguishability convention implicit in both W/sigma and W/sigma+1; under the conventional d'=2 (2-sigma) resolvability criterion the count is 2, not 4"]}
```
