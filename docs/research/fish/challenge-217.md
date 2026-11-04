# Challenge 217 — adversarial review of the CHALLENGER B synthesis on claim 167

**Claim under review** (claim_id 217; recorded evidence level `derived`; recorded value **12 mV (midpoint of
8–17 range, derived)**; source: branches `claude/challenge-kcnk5b-claim-6ey3si`,
`claude/challenge-kcnk5b-claim-trw1cg`, both `docs/research/fish/challenge-167.md`):

> "CHALLENGER B (6ey3si + trw1cg, independent, agree on local pLDDT) on claim 167: local pLDDT 93.6/94.0 at
> motifs 98-102/203-207 and 90.7/84.8 (trw: 90.69/84.75) at W169/F241, all >80 (AF-Q6PFU3-F1 v6; 69.5 mean is
> dominated by disordered C-tail 261-448 mean 43.3); Perathoner 2014 Fig S4 itself reported depolarization so
> no sign conflict; 17.1 mV = Nernst slope*ln2 at 13.1 C (harvester recomputed 17.10 mV; 17.99 at 28 C) i.e. a
> ceiling not a value; Vm window 8-12 mV (GHK) / 8-17 mV (parallel conductance); 0.8-1.7 setpoints at a
> 2-sigma criterion. DISAGREES with challenger A on setpoints (4.4 vs 0.8-1.7) and with the deepen on pLDDT;
> all kept. Per-residue pLDDT not re-fetched by harvester."

**My verdict: WEAKENED.**

Every checkable factual assertion in this claim survived independent re-derivation and re-fetching. I could
not break any of them, and I tried: I re-downloaded the AlphaFold deposition the harvester explicitly did not
re-fetch, parsed it two independent ways, and re-read the Perathoner full text. The pLDDT numbers are exactly
right. The Nernst inversion is exactly right. The Fig S4 quote is real.

What does not survive is the claim's **recorded value** and two of its **framings**:

1. The headline value, 12 mV, does not follow from its own stated derivation (the midpoint of 8–17 is 12.5),
   is a midpoint taken *across two different models* the claim itself lists separately, and has as its upper
   endpoint a global ceiling that both source challengers explicitly disqualified as non-physiological.
2. The recorded "DISAGREES with challenger A on setpoints (4.4 vs 0.8–1.7)" is not a disagreement. It
   decomposes exactly into three stacked convention differences; on a common basis the two figures coincide
   to within rounding. Preserving a phantom disagreement propagates spurious uncertainty.
3. "no sign conflict" overstates what the source supports, and rests on a comparison across **different
   appendages and different life stages** that neither challenger nor the harvester noticed. Figure S4 of
   Perathoner 2014 is **caudal** fins of **juvenile** fish. Claim 167's charge was about the *pectoral* Vm
   response, which Perathoner never measured.

Labels used throughout: **calculated-by-me**, **retrieved** (a record of a computational prediction, not an
observation), **measured-by-the-authors**, **quoted** (verbatim from full text).

---

## 1. Arithmetic, redone from the stated inputs only

I did not read either challenger's working before computing. Script:
`/tmp/claude-0/-workspace-delphi-frontier/551b2f64-9ce8-5b5b-a3cc-7be2e7cedada/scratchpad/chk.py`.

### 1.1 The Nernst inversion — confirmed, and the claim picked the better of its two sources

**Calculated-by-me**, R = 8.314462618 J/mol/K, F = 96485.33212 C/mol:

| T (°C) | RT/F (mV) | (RT/F)·ln2 (mV) |
|---|---|---|
| **13.13** | 24.6697 | **17.0997** |
| 20 | 25.2617 | 17.5101 |
| 22 | 25.4341 | 17.6295 |
| **28** | 25.9511 | **17.9879** |

Inverting 17.10 mV: RT/F = 24.6701 mV → T = 286.284 K = **13.134 °C**.

So the claim's "13.1 C" is correct, "17.10 mV" is correct, and "17.99 at 28 C" is correct. ✔

**But note what this exposes.** Challenger trw1cg recorded **13.3 °C**; challenger 6ey3si recorded
**13.1 °C**. My inversion gives 13.134 °C, so 6ey3si is right and trw1cg is slightly off. The harvester
reports 13.1 and says "all kept" — it silently resolved a numerical disagreement between the two challengers
it describes as "independent, agree." The resolution happens to be correct, which is why this is a
bookkeeping defect and not an error: a record that says "all kept" should not quietly drop one of two
discrepant values.

### 1.2 "A ceiling not a value" — confirmed, and I can state the ceiling exactly

The claim's diagnosis is right, and stronger than it states. For a two-conductance cell
Vm = (x·E_K)/(x+1) with x = g_K/g_L and E_leak = 0, the shift on **exactly doubling** g_K is
(**calculated-by-me**, closed form):

    ΔVm(x) = |E_K| · x / ((2x+1)(x+1))

Maximising: d/dx of x/(2x²+3x+1) vanishes at 1 − 2x² = 0, so **x\* = 1/√2 = 0.7071**, and

    ΔVm_max = |E_K| · (3 − 2√2) = 0.171573 · |E_K|

At E_K = −98 mV this is **16.81 mV**, attained at resting Vm = **−40.6 mV**.

That is the decisive point. The top of the claim's own "8–17 mV" window is not an endpoint of a
physiological range — it is the **global maximum over all possible g_K:g_leak ratios**, and it occurs in a
cell resting at −41 mV, which is not a K⁺-dominated cell. Both source challengers said exactly this in their
own words (6ey3si: the 16.3 mV maximum sits "at PK/PNa ≈ 2 — i.e. in a cell resting near −17 mV, which is not
a K⁺-dominated cell"; trw1cg: "the claim's 17.1 mV sits at the very top of the achievable band rather than
being its typical value"). The harvester carried the number forward and dropped the disqualification.

**Calculated-by-me**, the same model across the K⁺-dominated resting band:

| resting Vm (mV) | ΔVm on doubling g_K (mV) |
|---|---|
| −68 | 12.29 |
| −70 | 11.67 |
| −75 | 9.97 |
| −80 | 8.09 |
| −83 | 6.88 |

The two challengers' models therefore **overlap at ~8–12 mV** for a K⁺-dominated cell — 6ey3si's GHK gives
7.9–11.8 mV at PK/PNa 20–50 (Vm −67.9 to −82.8), and the parallel-conductance model gives 6.9–12.3 mV over
Vm −68 to −83. That overlap, not the ceiling, is the defensible window.

### 1.3 The recorded value, 12 mV, fails on six counts

**(a) It is not the midpoint of its own stated range.** **Calculated-by-me**: (8 + 17)/2 = **12.5**, not 12.
(For completeness: midpoint of 8–16.8 is 12.4; of 8–16.3 is 12.15; of the GHK window 8–12 is 10.0.) The value
does not follow from the derivation printed beside it.

**(b) It averages across two models the claim itself lists as distinct.** The claim records "Vm window 8-12
mV (GHK) / 8-17 mV (parallel conductance)" — correctly preserving that two models give two answers — and then
the recorded value collapses them to a single midpoint of the wider one. That is averaging away a
disagreement the claim had just preserved.

**(c) Its upper endpoint is the disqualified global ceiling** (§1.2).

**(d) The parameter that selects a point inside the range is unmeasured.** Where you land in 8–17 mV is set
entirely by the cell's resting Vm (equivalently g_K:g_leak). No source measures resting Vm in pectoral fin
mesenchyme — both challengers say so, and I confirm it from the Perathoner full text (§3). A point value is
therefore not *derived*; it is *selected by an assumption*. The recorded level `derived` is the wrong label
for it.

**(e) The ceiling imports an oocyte E_K into fish tissue.** Perathoner states (**quoted**, full text) the
shift is "towards −90 to −100 mV, the equilibrium potential for K⁺ **in *Xenopus* oocytes**." The 17 mV
endpoint inherits that. **Calculated-by-me**, ceiling = 0.171573·|E_K|:

| E_K (mV) | ceiling (mV) |
|---|---|
| −80 | 13.73 |
| −90 | 15.44 |
| −98 | 16.81 |
| −100 | 17.16 |

E_K in fin mesenchyme is unmeasured in every source I read. The window's upper bound is an oocyte number
transplanted into a different tissue in a different phylum, and it moves by 3 mV under a plausible E_K change.

**(f) Every endpoint assumes an exact 2.0×.** The paper says (**quoted**, verbatim, full text): "oocytes
injected with either of both mutant cRNAs show an **almost two-fold** increase in K⁺ conductance over that of
oocytes injected with wild type cRNA." **No numeric fold-change appears in the paper.** "Almost two-fold" is
< 2, so every window endpoint is a slight overestimate. This is inherited from claim 167 and not flagged at
217.

### 1.4 The setpoint figures reproduce — and the recorded "disagreement" is not one

**Calculated-by-me**: 8/10 = 0.80 and 17/10 = 1.70. The claim's "0.8–1.7 setpoints at a 2-sigma criterion"
reproduces exactly. ✔

But the recorded "DISAGREES with challenger A on setpoints (4.4 vs 0.8-1.7)" does not describe a
disagreement. A's 4.4 is **calculated-by-me** as 17.1/5 + 1 = 4.42. The two figures differ in *three* stacked
conventions:

| | challenger A | challenger B |
|---|---|---|
| counts | **levels** (W/σ + 1) | **intervals** (W/σ) |
| criterion | d′ = 1 (σ = 5) | d′ = 2 (σ = 10) |
| window | W = 17.1 mV | W = 8–17 mV |

Put on one basis (**calculated-by-me**):

- **levels, 2σ:** A → 17.1/10 + 1 = **2.71**; B → **1.80–2.70**.
- **intervals, 1σ:** A → **3.42**; B → **1.60–3.40**.

On either common basis the two **coincide at the top and overlap throughout**. The apparent 5× spread
(4.4 vs 0.8) is produced entirely by comparing levels-at-1σ against intervals-at-2σ. The honest record is
that A and B agree on setpoint count once the criterion is fixed, and differ only on the window — which is
the §1.3 question, already recorded separately. Logging a definitional mismatch as a substantive
disagreement is the mirror image of averaging a real one away: it inflates the uncertainty a downstream
reader will carry.

Separately: **0.8 setpoints is not a coherent count.** It counts intervals, and a window narrower than the
discrimination criterion still affords one distinguishable state, not 0.8. The floor of a setpoint count is 1.

### 1.5 The dropped sensitivity — σ_V = 5 mV is single-cell, and the result is not robust to it

σ_V = 5 mV is unsourced in every document in this chain, and both challengers say so. Challenger 6ey3si made
the N-cell averaging regime its **headline weakest-link finding**. Claim 217 reports 0.8–1.7 with no mention
of it.

**Calculated-by-me**, σ_eff = 5/√N, 2σ criterion, on the claim's own 8–17 mV window:

| N cells | σ_eff (mV) | criterion (mV) | intervals at W = 8 | at W = 17 |
|---|---|---|---|---|
| 1 | 5.00 | 10.00 | 0.80 | 1.70 |
| 10 | 1.58 | 3.16 | 2.53 | 5.38 |
| 100 | 0.50 | 1.00 | 8.00 | 17.00 |

A 10× change in the recorded setpoint count from relaxing one unsourced assumption. Whether a tissue growth
setpoint is read out by one cell or by many is not established anywhere in this chain — so 0.8–1.7 is
conditional on a choice, and claim 217 records it unconditionally while one of its own two sources supplied
the caveat.

---

## 2. The pLDDT leg — I re-fetched what the harvester did not, and it holds exactly

Claim 217 honestly flags "Per-residue pLDDT not re-fetched by harvester." I re-fetched it.

**Retrieved** 2026-11-04. AlphaFold DB REST `GET /api/prediction/Q6PFU3` → HTTP 200:
`uniprotAccession` Q6PFU3, `uniprotId` Q6PFU3_DANRE, `organismScientificName` *Danio rerio*, 448 aa,
`modelEntityId` AF-Q6PFU3-F1, `latestVersion` **6**, `isComplex` **False**,
`toolUsed` "AlphaFold Monomer v2.0 pipeline", `globalMetricValue` **69.5**, `fractionPlddtVeryLow` **0.339**.

Note: the API record carries **no** `confidenceUrl` field (KeyError; `.get` → None), so the confidence JSON
has to be reached by a constructed URL. Both file fetches returned HTTP 403 to a bare curl and HTTP 200 with
a generic User-Agent — recording this because it is the kind of access artifact that silently produces an
empty parse.

Downloaded `AF-Q6PFU3-F1-model_v6.cif` (419,828 bytes, sha256
`efc66b7ae7a21f7640ac46471ebbc3a8d59af92996550ee1e059949db3e3f2dd` — **byte-identical to the hash 6ey3si
recorded**, so we read the same deposition) and `AF-Q6PFU3-F1-confidence_v6.json` (6,181 bytes). I parsed the
CIF `ma_qa_metric_local` loop and the JSON `confidenceScore` array separately.

**Controls, both passed:** my parse gives mean **69.505** against the API's 69.5, and fraction < 50 =
**0.3393** against the API's 0.339.

**Retrieved**, per-residue (1-indexed):

| region | sequence | per-residue pLDDT | mean | min | all > 80? |
|---|---|---|---|---|---|
| 98–102 (P1) | TIGYG | 95.75, 95.31, 93.69, 93.06, 90.00 | **93.56** | 90.00 | **yes** |
| 203–207 (P2) | TVGFG | 95.19, 96.06, 93.94, 93.06, 91.75 | **94.00** | 91.75 | **yes** |
| W169 | W | 90.69 | **90.69** | 90.69 | **yes** |
| F241 | F | 84.75 | **84.75** | 84.75 | **yes** |

| segment | n | mean |
|---|---|---|
| 1–260 | 260 | 88.47 |
| 261–448 | 188 | **43.28** |

Weighted recombination: (260·88.47 + 188·43.28)/448 = **69.505**, reproducing the global mean. So the claim's
diagnosis — "69.5 mean is dominated by disordered C-tail 261-448 mean 43.3" — is **arithmetically exact**,
and I confirm it two ways. Also **retrieved**: fraction > 80 across the whole chain = **0.4888**.

Sequence positive controls, all pass: residue 169 = **W**, residue 241 = **F**, 98–102 = **TIGYG**,
203–207 = **TVGFG**.

**Every pLDDT number in claim 217 is correct** (93.6, 94.0, 90.7/90.69, 84.8/84.75, 69.5, 43.3, "all > 80" —
which holds per-residue, not merely on the means, since the minima are 90.00 and 91.75). This leg survives
intact.

### 2.1 One qualification: "independent" is weaker than it reads — and I verified this rather than inferring it

The two challengers parsed **different files** (6ey3si the CIF `ma_qa_metric_local` loop; trw1cg the
`confidence_v6.json` array). I fetched both and compared element-wise: **448 values each, identical, maximum
absolute difference 0.0.**

So their agreement is a **parse-correctness check on a single deposited prediction**, not independent
corroboration of the structural confidence. The claim's phrase "independent, agree on local pLDDT" is true as
literally written but will be read as two-source support. One AlphaFold deposition read twice is one source.

Second qualification: pLDDT is a **retrieved record of a computational prediction, not an observation**.
Challenger trw1cg labelled it so explicitly. Claim 217's single recorded level `derived` does not distinguish
retrieved-prediction from calculated-by-the-author, and these are different things with different failure
modes.

---

## 3. The sign leg — the factual quote is real, but "no sign conflict" overreaches, and the appendage is wrong

**Read-level: full-text.** Europe PMC REST `PMC3894163/fullTextXML`, HTTP 200, 142,283 bytes, retrieved
2026-11-04 and scanned myself.

### 3.1 The quote is confirmed

Figure S4 legend, **quoted** verbatim:

> "**Figure S4 Polarization of fins during growth.** Voltage sensitive dyes were used to assess changes in
> overall polarization of growing **caudal** fins of wild type and *alf* **juvenile** fish. (A) DiSBAC₂(3)
> staining in wild type fins exhibited hyperpolarization localized to discrete regions of the fin with
> variable detection of distal regions of altered depolarization. (B) *alf* fins in contrast show high levels
> of depolarization across the fin with variable patterns in different tissues. (C) Quantification of average
> DiSBAC₂(3) fluorescence signal in wild type and mutant fins (average pixel intensity (12-bits) of the fin
> in maximum intensity projections). \*\*\*: p<0.001, N = 21–23."

And the Discussion, **quoted**:

> "Although we observed a hyperpolarizing effect of the *alf* mutation in *Xenopus* oocytes, we cannot exclude
> that this, in turn, triggers a depolarization, either at cellular level or in the surrounding tissues during
> development of the fin. In fact, experiments employing depolarization-sensitive dyes, **suggest that this
> might indeed be the case** (Figure S4)."

So **"Perathoner 2014 Fig S4 itself reported depolarization" is correct.** ✔ That half of the claim stands,
verified at full-text read-level by me.

### 3.2 But Figure S4 is CAUDAL fins in JUVENILES — and claim 167's charge was about the PECTORAL response

This is the fault none of the three documents in this chain caught. Both challengers wrote "in *alf* fins";
neither wrote **caudal**. The legend says caudal, and Methods confirm the stage: **quoted**, "wild type and
mutant juvenile fish (STL = 16–18 mm) were incubated in fluorescent dye."

Jiang 2024 measures **pectoral fin buds**. So the asserted agreement between Perathoner Fig S4 and Jiang 2024
is an agreement **across a different appendage and a different life stage**, both read out by the same
non-ratiometric dye.

Claim 167's charge, as both challengers quote it, concerned "the sign of the **pectoral** Vm response."
Perathoner 2014 never measured pectoral Vm. Therefore the supportable statement is **not** "no sign
conflict." It is:

> Perathoner's only in vivo polarization datum is caudal fin in juveniles, and it is depolarizing; the
> paper reports no pectoral Vm at all. There is no demonstrable pectoral sign conflict *because there is no
> pectoral datum in Perathoner to conflict with* — not because the two papers were shown to agree on the
> same quantity.

That is a weaker and different proposition, and it is the one the evidence supports. The distinction is mine,
drawn from the full text; the "no sign conflict" framing is the claim's.

### 3.3 And the claim drops the residual openness both its sources preserved

Both challengers explicitly kept a live disagreement open:

- 6ey3si: "the steady-state pectoral Vm in absolute mV remains **unmeasured by anyone**."
- trw1cg: "the magnitude and sign of the immediate in-vivo Kcnk5b effect **remains genuinely open**."

Claim 217 compresses both to "no sign conflict." That is averaging away a disagreement its sources took care
to preserve — against the standing instruction to preserve it.

Three further points from my own read that sharpen this:

- Perathoner's own in vivo language is hedged — "**suggest** that this **might** indeed be the case" — not an
  assertion.
- The dye is non-ratiometric and quantified as **12-bit pixel intensity**, so **neither** in vivo dataset
  yields a value in mV. The quantity claim 217 records a value for (12 mV) has never been measured in either
  tissue.
- The oocyte Vm is likewise reported without numbers: **quoted**, "The mutant variants **tend to**
  hyperpolarize the cell (each point represents one oocyte)," and the correlation is at "a constant voltage
  of 50 mV (Figure 5D)." No mV values for either group appear in the text.

### 3.4 Temperature: the claim's "ceiling not a value" diagnosis is vindicated

**Scope of negative search: the complete Europe PMC full text of PMC3894163, scanned by me for
"temperature".** The only hit is a generic statement that K2P channel function is modulated by "temperature,
oxygen, osmolarity and pH." **No recording temperature is reported anywhere in the paper.** Nor did I find a
bath K⁺ concentration in the electrophysiology text.

So the 13.13 °C that falls out of inverting 17.1 mV is an **artifact of the arithmetic, not a stated
experimental condition** — which is precisely what claim 217 says ("i.e. a ceiling not a value"). This leg is
correct and I confirm it independently.

---

## 4. Proxy (Q2): named, but the claim records a value from a model its own sources disavow

The quantity that matters is the achievable range of **resting Vm in pectoral fin mesenchyme in vivo**. What
the chain actually has is a macroscopic whole-oocyte current ratio in a heterologous system, verbally
reported as "almost two-fold." Both challengers named this proxy.

Claim 217 does not name it — and worse, it records **12 mV** as the headline value while one of its own two
sources states that the model producing that number does not apply in vivo. 6ey3si, on Jiang 2024's proposed
Na⁺-recruitment mechanism:

> "then the in vivo Vm change is not set by the K⁺ conductance ratio at all, and mapping a 2-fold K⁺
> conductance onto a GHK Vm shift is **the wrong model regardless of which formula is used**."

That reconciliation is a *proposal* by Jiang's authors, not a measurement, so it does not settle the question
either way — I am not treating it as established. But a synthesis should not promote to "value" a number
computed from a model that its own evidence base flags as possibly inapplicable, without recording the
condition. The claim's "8-12 mV (GHK) / 8-17 mV (parallel conductance)" at least shows its models; the
recorded value 12 mV shows neither.

Also worth recording from my full-text read, as support for the *other* side of this chain: Perathoner's own
Figure 5A legend labels "**GFG and GYG domains**" as "the selectivity pore of the channel." So reporting
structural confidence at 98–102 (TIGYG) and 203–207 (TVGFG) matches **the source paper's own structural
framing** — reinforcing, independently, that those motifs were a defensible choice of residues.

---

## 5. Hidden assumption (Q3), relaxed

Three load-bearing assumptions, in descending order of damage:

1. **Resting Vm (equivalently g_K:g_leak) of the target cell.** Carries the entire 12 mV. Unmeasured in all
   sources. Relaxed across the plausible band, the answer runs 6.9–16.8 mV and there is no principled
   midpoint (§1.2, §1.3d).
2. **σ_V = 5 mV is single-cell.** Carries the entire setpoint count. Relaxed to an N-cell readout, 0.8–1.7
   becomes 8–17 at N = 100 (§1.5).
3. **E_K = −98 mV, imported from *Xenopus* oocytes.** Carries the window's ceiling. Relaxed to −80 mV, the
   ceiling drops from 16.8 to 13.7 mV (§1.3e).

Relax any one and the recorded value moves materially. The claim records none of the three as conditions.

---

## 6. Evidence level (Q4)

The recorded level `derived` is **partly** honest and better than claim 167's `unknown`. It is right for the
mV and setpoint arithmetic, and the claim deserves credit for flagging "Per-residue pLDDT not re-fetched by
harvester" — a disclosure I was able to act on, and which turned out to be fine.

Three defects remain:

- **The recorded value is not derived, it is assumption-selected.** 12 mV requires a resting Vm no one has
  measured. "Derived" implies it follows from the inputs; it does not (and it does not even follow
  arithmetically from the stated range — §1.3a).
- **One level is used for three kinds of number.** pLDDT values are *retrieved records of a computational
  prediction*; the mV windows are *calculated-by-the-author*; the "almost two-fold" is *measured by
  Perathoner, and reported verbally with no number*. trw1cg drew these distinctions explicitly; the synthesis
  flattens them.
- **No read-levels are carried.** Claim 217 asserts the Perathoner Fig S4 content with no read-level
  attached. It happens to be right at full-text level — I verified it myself — but the claim as recorded does
  not say so, and a downstream reader cannot tell whether it came from full text or a search summary.

---

## 7. Regime, taxon, counter-example (Q5)

- **Regime the claim misses, running against it:** multi-cell averaging (§1.5). The setpoint count holds only
  for a single-cell readout.
- **Regime the claim misses, running toward it:** the ceiling structure of the conductance-divider response
  (§1.2). The maximum is |E_K|·(3−2√2) at g_K/g_leak = 1/√2 — so no amount of conductance tuning reaches the
  Nernst slope, which makes the window *narrower* than 17 mV, not wider.
- **Tissue/stage counter-example to the "no sign conflict" framing:** Figure S4 is caudal fin, juvenile; Jiang
  2024 is pectoral fin bud (§3.2). The two in vivo depolarization observations are not measurements of the
  same quantity.
- **Model counter-example:** Jiang 2024's *proposed* Na⁺-channel-dependent depolarization, under which the in
  vivo Vm change is not a conductance-divider response at all (§4). Proposed, not measured — preserved as
  open.
- **Taxon:** I did not find a taxon-level counter-example. **Scope of that negative: I did no new literature
  search in this review beyond re-fetching the two primary sources named in the claim (AlphaFold DB Q6PFU3
  and PMC3894163). I did not search other teleosts, mammalian KCNK5, or the Aramaki & Kondo preprint.** That
  gap is real and stated rather than implied.

---

## 8. What I could not break

Stated plainly, because it is most of the claim:

- **All seven pLDDT figures** (93.6, 94.0, 90.7/90.69, 84.8/84.75, 69.5, C-tail 43.3, "all > 80") —
  re-fetched, parsed two ways, two controls passed, CIF hash matches, per-residue minima 90.00 and 91.75 so
  "all > 80" holds residue-by-residue. **Confirmed.**
- **The C-tail diagnosis** — weighted recombination reproduces 69.505 exactly. **Confirmed.**
- **17.10 mV at 13.13 °C and 17.99 mV at 28 °C.** **Confirmed**, and the claim picked the more accurate of
  its two sources' temperatures.
- **"A ceiling not a value."** **Confirmed**, and vindicated by the paper reporting no temperature at all.
- **"Perathoner 2014 Fig S4 itself reported depolarization."** **Confirmed** at full-text read-level.
- **0.8 = 8/10 and 1.7 = 17/10.** **Confirmed.**
- **The GHK and parallel-conductance windows as windows** (8–12 / 8–17) — reproduced; my overlap calculation
  independently lands on ~8–12 mV for a K⁺-dominated cell.

The claim is substantially sound work. It fails on how it was *recorded*: a point value that does not follow
from its stated derivation, built on a disqualified endpoint and an unmeasured selecting parameter; a
convention mismatch logged as a disagreement; and a compression of "no demonstrable pectoral conflict" into
"no sign conflict" that loses both the appendage and the openness its sources preserved.

**This is not a feasibility finding.** I am not asserting that graded pectoral control is feasible or
infeasible. I am saying the recorded value cannot carry weight, and the honest record here is a range with
its unmeasured parameter named.

---

## 9. Sources and read-levels

| source | read-level |
|---|---|
| AlphaFold DB REST `api/prediction/Q6PFU3` | **full data**, HTTP 200, retrieved 2026-11-04 by me |
| `AF-Q6PFU3-F1-model_v6.cif` (419,828 B, sha256 `efc66b7a…f2dd`), `ma_qa_metric_local` loop | **full data**, parsed independently by me |
| `AF-Q6PFU3-F1-confidence_v6.json` (6,181 B), `confidenceScore` array | **full data**, parsed independently by me |
| Perathoner et al. 2014, *PLoS Genet* 10(1):e1004080, PMC3894163 (Europe PMC `fullTextXML`, 142,283 B) | **full-text**, retrieved and scanned by me 2026-11-04 |
| Jiang et al. 2024, *PLoS Biol* 22(3):e3002565 | **could-not-access — not fetched by me.** All Jiang content here is as reported by the two challengers (6ey3si: full-text; trw1cg: abstract/figure-legend only). Their read-levels differ and I preserve that. |
| Aramaki & Kondo bioRxiv 10.1101/2024.03.27.587111 | **not fetched by me.** Not load-bearing for claim 217. |
| Challenger branches `…-claim-6ey3si`, `…-claim-trw1cg`, `docs/research/fish/challenge-167.md` | **full text**, read from git |
| Challenger A's setpoint figure (4.4) | **could-not-access** — I did not locate challenger A's own document. I reconstructed 4.4 as 17.1/5 + 1 = 4.42, which matches exactly; the decomposition in §1.4 rests on that reconstruction, not on A's text. |

```swarm-challenge
{"claim_id": 217, "outcome": "weakened", "reason": "Every checkable assertion survived my independent re-derivation and re-fetch -- all seven pLDDT figures reproduce exactly from a freshly downloaded AF-Q6PFU3-F1 v6 (mean 69.505, frac<50 0.3393, C-tail 261-448 mean 43.28, per-residue minima 90.00/91.75 so 'all >80' holds residue-wise), 17.10 mV inverts to 13.134 C, and Perathoner's Fig S4 depolarization is verbatim at full-text -- but the recorded value 12 mV fails: the midpoint of 8-17 is 12.5, the midpoint is taken across two models the claim itself lists separately, its upper endpoint is the global ceiling |E_K|*(3-2*sqrt(2)) = 16.8 mV attained only at resting Vm = -41 mV in a non-K+-dominated cell which both sources explicitly disqualified, and the parameter selecting any point in the range (resting Vm in pectoral fin mesenchyme) is unmeasured everywhere; additionally the recorded 'DISAGREES with challenger A (4.4 vs 0.8-1.7)' is a three-way convention mismatch that coincides at 2.71 vs 1.80-2.70 on a common levels-at-2-sigma basis rather than a real disagreement, and 'no sign conflict' overreaches because Perathoner's Fig S4 is caudal fin in juveniles (STL 16-18 mm) while Jiang measured pectoral fin buds, so there is no pectoral datum in Perathoner to conflict with -- an appendage/stage mismatch neither challenger nor the harvester noted.",
  "corrected_value": "8-12 mV where both challengers' models overlap for a K+-dominated cell (resting Vm -68 to -83 mV); ceiling 16.8 mV = |E_K|*(3-2*sqrt(2)) at resting Vm = -41 mV, attainable only in a non-K+-dominated cell and inheriting an oocyte E_K of -98 mV (ceiling falls to 13.7 mV at E_K = -80 mV); no single point value is derivable, so 12 mV should be withdrawn in favour of the range -- resting Vm and E_K in pectoral fin mesenchyme are unmeasured in all cited sources and the source conductance change is a verbal 'almost two-fold' with no number, making every endpoint a slight overestimate. Setpoints: A and B agree at 1.8-2.7 levels on a common 2-sigma basis, not 4.4 vs 0.8-1.7; and the count rises to 8-17 intervals under a 100-cell readout.",
  "depends_on": ["AlphaFold DB AF-Q6PFU3-F1 model v6 per-residue pLDDT, re-fetched and parsed by me from both the CIF ma_qa_metric_local loop (sha256 efc66b7ae7a21f7640ac46471ebbc3a8d59af92996550ee1e059949db3e3f2dd) and confidence_v6.json, the two being per-residue identical (max abs diff 0.0)", "AlphaFold DB api/prediction/Q6PFU3 globalMetricValue 69.5, fractionPlddtVeryLow 0.339, isComplex False, toolUsed 'AlphaFold Monomer v2.0 pipeline', latestVersion 6", "UniProt Q6PFU3 448-aa sequence (res169=W, res241=F, 98-102=TIGYG, 203-207=TVGFG), as served in the AFDB prediction record", "Perathoner et al. 2014 PLoS Genet 10(1):e1004080 / PMC3894163 full text via Europe PMC fullTextXML: 'almost two-fold increase in K+ conductance' with no numeric fold-change", "Perathoner et al. 2014 Figure S4 legend naming CAUDAL fins of JUVENILE fish (Methods: STL 16-18 mm), DiSBAC2(3) quantified as 12-bit pixel intensity, depolarization across alf fins, N=21-23", "Perathoner et al. 2014 Discussion hedge 'suggest that this might indeed be the case' for in vivo depolarization", "Perathoner et al. 2014 reporting E_K as -90 to -100 mV explicitly for Xenopus oocytes, and reporting no recording temperature anywhere in the full text (scope: complete Europe PMC full text scanned by me)", "the parallel-conductance model Vm=(x*E_K)/(x+1) with E_leak=0, whose doubling shift maximises at x=1/sqrt(2) with value |E_K|*(3-2*sqrt(2)) (my closed-form derivation, not a measurement)", "challenger 6ey3si's GHK window 8-12 mV at PK/PNa 20-50 and its N-cell averaging sensitivity (sigma_eff = sigma/sqrt(N))", "challenger trw1cg's parallel-conductance window 8-17 mV at E_K = -98 mV", "the unsourced sigma_V = 5 mV single-cell noise assumption, used unchanged for comparability", "challenger A's setpoint figure 4.4, reconstructed by me as 17.1/5 + 1 = 4.42 because I could not access A's own document", "Jiang et al. 2024 PLoS Biol 22(3):e3002565 content ONLY as relayed by the two challengers at their differing read-levels (6ey3si full-text, trw1cg abstract/figure-legend) -- not fetched by me"]
}
```
