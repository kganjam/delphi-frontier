# Challenge 167 — adversarial review of the [S14-D] kcnk5b rebuttal

**Claim under review** (claim_id 167, source `harvest:deepen-s14-potassium-channel-5miqg2`): that engineering
kcnk5b for graded pectoral-restricted control is unsupported, because (a) the recorded pLDDT>80 is
"misstated" and quoted at the wrong residues, (b) the measured ~2-fold conductance window yields only
~13–17 mV and ~3 setpoints, (c) the sign of the pectoral Vm response is in unresolved disagreement between
Perathoner 2014 and Jiang 2024, and (d) graded and restricted control already exist optogenetically and via
cell-type-specific promoters. Recorded verdict: *falls*. Recorded evidence level: unknown.

**My verdict: REFUTED.** Two of the claim's four legs are contradicted by the primary sources. Its headline
evidential charge — that pLDDT>80 is a misstatement — is itself the misstatement, and its sign-disagreement
leg misreads the paper it cites. The claim's *conclusion* about S14-D may well be right, and leg (d) largely
survives, but it is right for reasons the claim does not establish, and the reasons it does give are wrong.

Every number below is labelled **measured**, **retrieved** or **calculated**. All computation was redone from
the stated inputs without reference to the author's working.

---

## 1. Arithmetic, redone independently

### 1.1 Where 17.1 mV comes from, and why it is the wrong formula

**Calculated.** The claim's KEY line asserts `~2.0-fold conductance = 17.1 mV`. Solving backwards,
17.1 mV = (RT/F)·ln 2 exactly when T = 13.1 °C:

| T (°C) | RT/F (mV) | (RT/F)·ln2 (mV) |
|---|---|---|
| 13.1 | 24.67 | **17.10** |
| 20 | 25.26 | 17.51 |
| 22 | 25.43 | 17.63 |
| 28 | 25.95 | 17.99 |

So the claim is applying a **Nernst slope** to a **conductance ratio**, at an unstated temperature of 13.1 °C
— which is neither zebrafish rearing temperature (28 °C) nor a plausible oocyte bench temperature (~20–22 °C).
Perathoner et al. 2014 reports **no recording temperature and no bath K⁺ concentration** (read-level:
full-text, PMC3894163), so neither input needed for this conversion is available from the cited source.

The deeper problem is the formula. `(RT/F)·ln(fold)` is the shift in *E*K for a *fold change in K⁺
concentration*. It is not the shift in *V*m for a fold change in K⁺ *conductance*. The latter requires GHK or
a conductance divider, where the shift saturates as *V*m approaches *E*K.

**Calculated** (GHK, 22 °C, Ko=2.5, Ki=140, Nao=145, Nai=12 mM; EK = −102.4 mV). Vm shift when PK doubles:

| PK/PNa | Vm before (mV) | Vm after (mV) | ΔVm (mV) |
|---|---|---|---|
| 2 | −16.9 | −33.2 | −16.3 |
| 10 | −53.8 | −67.9 | −14.0 |
| 20 | −67.9 | −79.6 | −11.8 |
| **30** | **−75.1** | **−85.2** | **−10.1** |
| 50 | −82.8 | −90.8 | −7.9 |
| 100 | −90.8 | −95.9 | −5.2 |

The maximum shift achievable over *all* PK/PNa is **16.3 mV**, at PK/PNa ≈ 2 — i.e. in a cell resting near
−17 mV, which is not a K⁺-dominated cell. `(RT/F)·ln2 = 17.63 mV` is a ceiling that is **never attained**. At
a physiological resting ratio (PK/PNa ≈ 20–50, Vm −68 to −83 mV) the shift is **8–12 mV**.

**Consequence for the claim:** its 17.1 mV sits *above* the physiologically realistic range and essentially at
the unattainable ceiling. The correct number is smaller, which makes the window *narrower* and the setpoint
count *lower*. The error is real but runs in the direction that favours the claim's own conclusion — so it is
a defect in the KEY value, not a reason the verdict flips.

### 1.2 Setpoint count

**Calculated.** 17.1 / 5 = 3.42, so "~3.4 distinguishable setpoints at σ_V = 5 mV" is just W/σ. Two issues:

- W/σ counts **intervals**, not **levels**. The number of distinguishable levels is W/σ + 1 = 4.42. The claim
  under-counts here, generously to itself.
- Requiring d′ = 2 rather than d′ = 1 for "distinguishable" halves it: 17.1/10 = 1.71. This reproduces the
  claim's own "collapsing to 1.7 if soft by a factor of two," so that arithmetic checks out.

Substituting the correct GHK window: W = 10.1 mV at PK/PNa = 30 gives 2.02 intervals (3.02 levels) at σ = 5,
and 1.01 at d′ = 2.

### 1.3 σ_V = 5 mV is unsourced — and this is the assumption that carries the result

The claim gives no provenance for σ_V = 5 mV. I could not find it attributed anywhere in the claim text
(scope: the claim as supplied). It is load-bearing: the entire setpoint count is W/σ.

**Relaxed, it breaks the result.** A tissue-level growth setpoint is not read out by one cell. If the readout
integrates over N cells, σ_eff = σ/√N:

| N cells | σ_eff (mV) | intervals at W = 10.1 | intervals at W = 17.1 |
|---|---|---|---|
| 1 | 5.00 | 2.0 | 3.4 |
| 10 | 1.58 | 6.4 | 10.8 |
| 100 | 0.50 | 20.2 | 34.2 |
| 1000 | 0.16 | 63.9 | 108.1 |

A fin bud contains far more than 100 mesenchymal cells, and growth integrates over days. Treating single-cell
Vm noise as the limit on a tissue-level setpoint is a choice the claim makes silently, and it is the choice
that produces "~3 setpoints". Relaxed, graded control becomes arithmetically unremarkable. **This is the
claim's weakest link**, and it is the opposite error from §1.1 — it pushes the conclusion the claim wants.

### 1.4 The proxy

**The fold-change is a proxy, and the claim does not say so.** What matters for graded control is the
achievable range of resting Vm in fin mesenchyme *in vivo*. What is measured is whole-oocyte macroscopic
current at a **+60 mV test potential** (measured; Perathoner 2014 Methods state currents were "averaged and
normalized" to wild-type at +60 mV, n = 5–26, SD error bars, no p-values reported). That conflates channel
density, surface expression and open probability in a heterologous system, and is measured ~150 mV away from
the resting potential the argument is about. The right quantity — calibrated resting Vm in pectoral fin
mesenchyme — **is not measured in either cited paper** (see §3). The claim builds a feasibility ceiling on a
proxy without flagging it.

Also: the paper says "an almost two-fold increase in K⁺ conductance" (measured, full-text). "~2.0-fold"
rounds that **up**.

---

## 2. The pLDDT leg is backwards — this is the refutation

**Retrieved** from the AlphaFold DB API and the deposited model. Zebrafish kcnk5b = UniProt **Q6PFU3**
(448 aa; `gene: kcnk5b`, `organismScientificName: Danio rerio`). AFDB entry **AF-Q6PFU3-F1**, v6.

AFDB whole-chain metrics, retrieved verbatim from `api/prediction/Q6PFU3`:

- `globalMetricValue`: **69.5**
- `fractionPlddtVeryLow`: **0.339**
- `isComplex`: **False**; `toolUsed`: **"AlphaFold Monomer v2.0 pipeline"**

So the claim's two retrieved numbers, 69.5 and 33.9%, are **correct**. But they are *whole-chain* statistics,
and the statement they are being used to refute is a *local* one.

**Measured from the deposited model** (per-residue pLDDT parsed from the `ma_qa_metric_local` loop of
`AF-Q6PFU3-F1-model_v6.cif`, sha256 `efc66b7ae7a21f7640ac46471ebbc3a8d59af92996550ee1e059949db3e3f2dd`):

| region | sequence | per-residue pLDDT | mean | all > 80? |
|---|---|---|---|---|
| 98–102 (P1 filter) | **TIGYG** | 95.8, 95.3, 93.7, 93.1, 90.0 | **93.6** | **yes** |
| 203–207 (P2 filter) | **TVGFG** | 95.2, 96.1, 93.9, 93.1, 91.8 | **94.0** | **yes** |
| W169 (*alf* W169L) | W | 90.7 | 90.7 | **yes** |
| F241 (*alf* F241Y) | F | 84.8 | 84.8 | **yes** |

Two controls, both passed: my parse reproduces the AFDB `globalMetricValue` to 69.50 vs 69.5, and
`fractionPlddtVeryLow` to 0.3393 vs 0.339 — so the per-residue values are being read correctly. A must-fail
control on the API returned HTTP 400 for the impossible accession `ZZZZZZ` against 200 for `Q6PFU3`, so the
endpoint can come back empty.

**Therefore:**

1. **S14-D's "pLDDT>80 at motifs 98–102 and 203–207" is correct.** Local pLDDT there is 90.0–96.1. The claim's
   charge of misstatement is produced entirely by substituting the whole-chain mean (69.5) for the local
   value — the exact proxy substitution this review protocol asks reviewers to catch. The 33.9% below 50 is
   real but sits in disordered termini and loops, not at the filter; quoting it against a filter-local claim
   is misleading.
2. **The "wrong residues" sub-charge does not rescue it.** The claim is right that 98–102 and 203–207 are not
   W169 and F241 (W169L/F241Y confirmed as the two *alf* missense alleles — retrieved, full-text PMC3894163;
   and independently confirmed at sequence level, since Q6PFU3 position 169 is indeed W and 241 is indeed F,
   a positive control that the accession and the numbering match the paper's). But pLDDT at W169 is 90.7 and
   at F241 is 84.8 — **also >80**. Whichever residues you choose, the confidence statement holds. The
   criticism identifies no error.
3. **98–102 and 203–207 are the canonical K⁺ selectivity-filter signatures** (T-I-G-Y-G and T-V-G-F-G, the P1
   and P2 pore domains of this two-pore-domain channel). For a claim about *ionic conduction*, these are
   arguably the *most* appropriate residues to report structural confidence at. "Not the causal residues" is
   not the relevant objection.
4. **"62.82 for the homodimer" is not an AlphaFold DB value.** AFDB hosts a monomer-only prediction for this
   protein (`isComplex: False`, `toolUsed: "AlphaFold Monomer v2.0 pipeline"`, sole entry AF-Q6PFU3-F1). Scope
   of negative search: I queried `api/prediction/` for both zebrafish kcnk5b accessions returned by the
   UniProt REST API — Q6PFU3 (200, monomer) and A0A8M1PBI1 (**404, no entry**) — and the AFDB search endpoint
   returned no complex entries in the form I queried. The claim attributes a number to a database that does
   not, as far as I can establish, contain it. If it came from a local or third-party multimer run, that is a
   different evidence level and should be stated. Read-level: full-text/API for AFDB; **could-not-access** for
   any source of 62.82.

---

## 3. The sign leg misreads its own primary source

The claim frames this as "unresolved disagreement between Perathoner 2014 (hyperpolarization, calibrated clamp
in oocytes) and Jiang 2024 (depolarization, uncalibrated dye in fin buds)."

**Jiang 2024 is characterised accurately.** Retrieved (full-text, PMC11018282): the dye is **DiSBAC2(3)**;
measurements are reported as "DiSBAC2(3) fluorescence intensity as counted photons" and "photon counts per
pixel", described by the authors as "relative differences in membrane potential", with dye penetration
explicitly not ruled out. So "uncalibrated dye in fin buds" is correct. Direction: "overexpression of
*kcnk5b*-mCherry significantly increased depolarization."

**Perathoner 2014 is not.** Retrieved (full-text, PMC3894163): that paper reports **both signs**.
Hyperpolarization in oocytes — "the mutant channels lead to stronger hyperpolarization causing a shift in the
membrane potential towards −90 to −100 mV" — **and** in vivo dye experiments (Fig S4) that "instead suggested
depolarization in *alf* fins", a discrepancy the authors themselves acknowledge.

This changes the structure of the disagreement entirely:

- The disagreement is **not between the two papers**. It is between **preparations** — heterologous oocyte vs
  in vivo fin — and it is already present *within* Perathoner 2014.
- **In vivo, the two papers agree.** Both report depolarization, both by uncalibrated dye. The claim asserts
  an unresolved inter-paper conflict where the in vivo measurements concur.
- Jiang 2024 further offers a mechanism that makes both signs true at different timescales: "the increased
  K⁺-channel activity first hyperpolarizes the membrane potential," and "this increase in membrane potential
  immediately activates Na⁺ channels to depolarize the cells." Na⁺ channel inhibitors reduced both the
  depolarization and the growth. The authors flag this as a hypothesis ("We propose"), so it is a proposed
  reconciliation, not a measured one — I am not averaging the disagreement away, and the steady-state
  pectoral Vm in absolute mV remains **unmeasured by anyone**. But the claim's specific framing is wrong.
- "Calibrated clamp" overstates Perathoner. Oocyte Vm was measured directly (Fig 5D) but the paper reports
  **no mV values for either group**, only a shift "towards −90 to −100 mV", and no temperature or bath K⁺.

**And this undercuts §1 retroactively.** If the in vivo Vm response is depolarizing via *secondary Na⁺
channel recruitment*, then the in vivo Vm change is not set by the K⁺ conductance ratio at all, and mapping a
2-fold K⁺ conductance onto a GHK Vm shift is the wrong model regardless of which formula is used. The KEY
number is computed from a mechanism that the one in vivo measurement contradicts.

---

## 4. The prior-art leg mostly survives — with a correction to my own first finding

**I initially recorded this leg as unsupported, and I was wrong.** Two targeted web searches
(scope: WebSearch, extended mode, queries on optogenetic/graded control of kcnk5b and fin size) returned **no
optogenetic study**, and I had written the optogenetic bypass down as unsourced. The bioRxiv API then
returned the abstract that contains it. Recording this because the direction matters: an unsupported
prior-art bypass would have *strengthened* the claim's "falls" verdict, which is exactly the kind of finding
Rule 9 says to check — and here the check went against my interim reading, not for it.

**Retrieved** (read-level: **abstract**, via `api.biorxiv.org/details/biorxiv/10.1101/2024.03.27.587111`;
full text **could-not-access**, HTTP 429 on two attempts):

> Aramaki, T.; Kondo, S. — v1 "Independent size regulation of bones and appendages in zebrafish" (2024-03-29);
> v2 "Cell-type-dependent bioelectric regulation of fin size and fin-ray segment length in zebrafish"
> (2026-08-24). `"published": "NA"`.
>
> "we expressed the hyperactive potassium channel mutant kcnk5bW169L or the dominant-negative connexin mutant
> Cx43T154A under a common set of cell-type-specific promoters. Cell-type-specific bioelectric manipulation in
> keratinocytes primarily affected fin size, whereas manipulation in osteoblasts preferentially altered
> fin-ray segment length. … Furthermore, optogenetic manipulation demonstrated that membrane potential itself
> can regulate fin size and fin-ray segment length."

So both bypasses are real. Four qualifications the claim does not state:

1. **They are one source, not two independent lines.** The claim says "both bypassing protein engineering" as
   though citing two demonstrations; they are two experiments in a single preprint by the same two authors.
2. **It is still a preprint.** `"published": "NA"` as of this query (2026-11-04), through a v2 posted
   2026-08-24 — not peer-reviewed after ~2.5 years.
3. **"Restricted" here means cell-type-restricted, not pectoral-restricted.** The promoters are keratinocyte
   and osteoblast. S14-D's target was *pectoral*-restricted control; the abstract does not mention pectoral
   fins. This is a different axis of restriction, and the claim elides the difference.
4. **"Graded" is stronger than the abstract supports.** The abstract says membrane potential "can regulate"
   size. It does not report dose-dependent or graded setpoints. At abstract read-level I cannot confirm
   graded control was demonstrated.

Net: leg (d) is the claim's strongest leg and is genuinely supported in outline, at preprint/abstract
read-level, for cell-type rather than pectoral restriction. It is also the leg that makes §1 moot — if light
can set Vm directly, kcnk5b's 2-fold conductance is not the constraint on graded control.

---

## 5. Evidence level

The claim's recorded evidence level is `unknown`, and that is not honest for what it contains. Specifically:

- `17.1 mV`, `~3.4 setpoints` and `1.7` are **calculated**, from an unstated temperature and an unstated
  noise model, and presented in a line labelled with a measurement citation ("Xenopus oocyte TEVC, Perathoner
  et al. 2014"). The `=` signs in the KEY line read as identities derived from the measurement. They are not;
  neither the temperature nor the ionic conditions needed for the conversion appear in that paper.
- `69.5` and `33.9%` are correctly **retrieved**, but deployed against a local statement they do not address.
- `62.82` is attributed to AlphaFold DB and I could not locate it there (scope in §2.4).
- The Perathoner characterisation is a **misreading of full text**, not a read-level problem.

## 6. Regime / taxon / counter-example

- **Regime the claim misses:** the N-cell averaging regime (§1.3). Its setpoint count holds only for a
  single-cell readout.
- **Regime that cuts the other way:** the GHK saturation regime (§1.1) — in a K⁺-dominated cell the window is
  ~8–12 mV, not 17 mV.
- **Counter-example to the mechanism the arithmetic assumes:** Jiang 2024's Na⁺-channel-dependent
  depolarization (§3), which is not a GHK response to the K⁺ conductance at all.
- **Published counter-example to the pLDDT charge:** the deposited AFDB model itself (§2).
- I did not find a taxon-level counter-example. Scope of that negative: searches were restricted to zebrafish
  / *Danio rerio* kcnk5b and the K2P fin-size literature; I did not search other teleosts or mammalian KCNK5.

---

## 7. What survives

- The underlying worry is legitimate: nobody has measured calibrated resting Vm in pectoral fin mesenchyme, in
  either cited paper, so a quantitative setpoint argument has no measured anchor. Stated precisely, that is a
  real negative result.
- The window, computed correctly, is *narrower* than the claim says (8–12 mV at physiological PK/PNa, not
  17.1 mV).
- Leg (d) is real in outline, at preprint/abstract read-level.
- The *verdict* "falls" on S14-D may therefore be correct. But a verdict is only as good as its stated
  reasons, and two of these four are contradicted by the primary sources.

I tried to let this claim stand and could not. The pLDDT leg is not a near-miss; it is backwards, and it is
the claim's lead charge.

```swarm-challenge
{"claim_id": 167, "outcome": "refuted", "reason": "The lead charge is backwards -- local pLDDT at the quoted motifs 98-102/203-207 is 93.6/94.0 and at W169/F241 is 90.7/84.8, all >80, so S14-D's pLDDT>80 is correct and the claim refutes it only by substituting the 69.5 whole-chain mean for a local value; the sign leg also misreads Perathoner 2014, which itself reported in vivo depolarization (Fig S4), so the two papers agree in vivo rather than disagreeing; and the 17.1 mV KEY applies a Nernst slope to a conductance ratio at an unstated 13.1 C.",
  "corrected_value": "local pLDDT 93.6 (98-102, TIGYG) and 94.0 (203-207, TVGFG), W169=90.7, F241=84.8, all >80 (AF-Q6PFU3-F1 v6); Vm window from a 2-fold K+ conductance increase = 8-12 mV at physiological PK/PNa by GHK, max 16.3 mV, not 17.1 mV",
  "depends_on": ["AlphaFold DB AF-Q6PFU3-F1 v6 per-residue pLDDT (UniProt Q6PFU3, zebrafish kcnk5b, 448 aa)", "AFDB globalMetricValue 69.5 and fractionPlddtVeryLow 0.339 for Q6PFU3", "AFDB hosts monomer-only prediction for Q6PFU3 (isComplex=False); no entry for A0A8M1PBI1", "Perathoner et al. 2014 PLoS Genet (PMC3894163) full text: 'almost two-fold increase in K+ conductance', normalization at +60 mV, n=5-26, no temperature or bath K+ reported", "Perathoner et al. 2014 Fig S4: in vivo dye suggested depolarization in alf fins, acknowledged by authors", "Perathoner et al. 2014: alf alleles W169L and F241Y", "Jiang et al. 2024 PLOS Biology (PMC11018282) full text: DiSBAC2(3) dye, photon counts, uncalibrated, depolarization, proposed K+-then-Na+ two-step mechanism", "Aramaki & Kondo bioRxiv 10.1101/2024.03.27.587111 v1/v2 abstract: kcnk5b-W169L under cell-type-specific promoters plus optogenetic manipulation; still a preprint (published=NA)", "GHK constant-field model with Ko=2.5/Ki=140/Nao=145/Nai=12 mM at 22 C (my calculation, not a measurement)", "sigma_V = 5 mV single-cell noise assumption (unsourced in the claim)"]
}
```
