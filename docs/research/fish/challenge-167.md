# Challenge 167 — adversarial review of claim [S14-D] (kcnk5b engineering)

**Claim under review (verbatim, abridged):** "[S14-D] Engineering kcnk5b itself for graded
pectoral-restricted control is unsupported: the recorded pLDDT>80 is both misstated (AlphaFold DB
reports 69.5 for the monomer and 62.82 for the homodimer, with 33.9% of residues below 50) and
quoted at filter motifs 98-102 and 203-207 that are not the causal alf residues W169 and F241 …
KEY: ~2.0-fold macroscopic K+ current … = 17.1 mV of a ~60 mV available Vm window = ~3.4
distinguishable setpoints at sigma_V = 5 mV. VERDICT: falls"

**Reviewer outcome: REFUTED.** Two of the claim's specific, checkable charges are false against
primary data, and its KEY number is not reproducible from its own stated inputs. The claim's
bottom-line conclusion may still be correct, but on one pillar only — and not for the reasons given.

A note on what follows: every pLDDT number below is a *retrieved computed value* from the AlphaFold
database — a record of a prediction, not an observation. Every mV and setpoint number I state is
*derived by me by calculation*, labelled as such. Perathoner's conductance ratio and oocyte membrane
potentials are *measurements reported by those authors*.

---

## 1. Pillar 1 — the pLDDT charge. REFUTED.

### What I retrieved

AlphaFold DB REST API, `GET /api/prediction/Q6PFU3` (kcnk5b, *Danio rerio*, 448 aa), entry
`AF-Q6PFU3-F1`, model v6, pipeline string **"AlphaFold Monomer v2.0"**:

| field | value |
|---|---|
| `globalMetricValue` (mean pLDDT) | **69.5** |
| `fractionPlddtVeryLow` (<50) | **0.339** |

I then downloaded the per-residue confidence array
(`AF-Q6PFU3-F1-confidence_v6.json`, key `confidenceScore`, n=448) and parsed it myself. My parse
reproduces the API's summary statistics exactly — mean 69.50, fraction <50 = 0.3393 — which
validates the parse.

So the claim's two global figures, 69.5 and 33.9%, are **correct**. I confirm them.

### Why that does not do the work the claim asks of it

The claim's own argument is that global numbers are the wrong thing to quote and that what matters
is the causal residues W169 and F241. I agree with the principle. So I applied it. Per-residue
pLDDT, from my own parse of the array:

| residue | pLDDT (retrieved) |
|---|---|
| **W169** (causal, *alf*) | **90.69** |
| **F241** (causal, *alf*) | **84.75** |
| 98–102 (filter motif 1, `TIGYG`) | mean 93.6 (min 90.0) |
| 203–207 (filter motif 2, `TVGFG`) | mean 94.0 (min 91.8) |

**Both causal residues exceed 80.** The record's ">80" is correct precisely at the residues the
claim says the record failed to quote. The claim rebuts a locally true statement with a globally
true but inapplicable statistic — the identical proxy error it accuses the record of committing,
run in the opposite direction.

The reason the global mean is 69.5 is visible once the chain is split:

| segment (derived by me from the retrieved array) | mean pLDDT |
|---|---|
| 1–260 (transmembrane / pore core) | 88.5 |
| 261–448 (C-terminal tail) | 43.3 |

The C-terminal tail is 188 of 448 residues (42% of the chain). The "33.9% of residues below 50" is
essentially that tail. It is a statement about an intrinsically disordered cytoplasmic extension and
carries no information about model confidence at a transmembrane pore residue. Overall, 48.9% of
residues are above 80 (derived).

### Sequence-numbering checks (both pass, in the claim's favour)

Against the AFDB sequence for Q6PFU3: residue 169 is **W**, residue 241 is **F** — the claim's
residue identities are right. 98–102 is `TIGYG` and 203–207 is `TVGFG`, i.e. the two K2P
selectivity-filter motifs (GYG at 100–102, GFG at 205–207) — the claim's motif coordinates are also
right, and it is right that these are not W169/F241. That sub-point stands; it is simply not
damaging, because the causal residues are confidently modelled too.

### The homodimer figure is misattributed

**I could not obtain 62.82 from AlphaFold DB, because AFDB does not serve a kcnk5b homodimer.**
Scope of that negative search: AFDB REST API `/api/prediction/` queried for both *Danio rerio*
kcnk5b accessions returned by UniProt (`gene:kcnk5b AND organism_id:7955`) — `Q6PFU3` returns the
single monomer entry above, pipeline "AlphaFold Monomer v2.0"; `A0A8M1PBI1` returns `{}` (no entry).
AFDB hosts monomer predictions for these accessions only. A homodimer pLDDT of 62.82 may well exist
from some AlphaFold-Multimer run, but it is **not** an AlphaFold DB value, and the claim attributes
it to AlphaFold DB. Read-level: full API responses retrieved; could-not-access for any source that
would actually support 62.82, because the claim names none.

---

## 2. Pillar 2 — the KEY arithmetic. Not reproducible, and built on a proxy.

### 2a. I cannot reproduce 17.1 mV

Computed independently from the stated input (2.0-fold), using the Nernst slope the claim's chain
implies, `RT/F · ln 2` (all derived by me):

| T | RT/F | × ln 2 |
|---|---|---|
| 20 °C (293.15 K) | 25.26 mV | **17.51 mV** |
| 25 °C (298.15 K) | 25.69 mV | **17.81 mV** |
| 28 °C (301.15 K, zebrafish) | 25.95 mV | **17.99 mV** |

To land on 17.1 mV requires RT/F = 24.67 mV, i.e. T = 286.4 K = **13.3 °C** — not a plausible
oocyte or zebrafish temperature. The defensible value is 17.5–18.0 mV. The discrepancy is small
(~3–5%) but the stated number is not derivable from the stated inputs, which is a reproducibility
defect in a line labelled KEY.

### 2b. `RT/F · ln 2` is the wrong conversion — it is a ceiling, not a value

Doubling *one* conductance in a cell that has others does not shift Vm by `RT/F · ln 2`. That is the
asymptote, approached only if the doubled conductance goes from negligible to total dominance. The
right form is the parallel-conductance relation, `Vm = (g_K·E_K + g_L·E_L)/(g_K + g_L)`.

Derived by me, taking E_K = −98 mV (consistent with the −90 to −100 mV the source paper gives for
*Xenopus* oocytes) and E_leak = 0 mV, then doubling g_K exactly:

| starting Vm | implied g_K/g_L | Vm after 2× g_K | **shift** |
|---|---|---|---|
| −40 mV | 0.69 | −56.8 mV | **16.8 mV** |
| −60 mV | 1.58 | −74.4 mV | **14.4 mV** |
| −80 mV | 4.44 | −88.1 mV | **8.1 mV** |

So a genuine 2× increase in g_K buys **8–17 mV**, saturating as Vm approaches E_K. The claim's
17.1 mV sits at the very top of the achievable band rather than being its typical value.

Note the direction: this error makes the claim's feasibility estimate *generous*. On the claim's own
2-fold input, its verdict survives a fortiori. The problem is the input.

### 2c. The proxy, named: macroscopic current ratio standing in for Vm authority

The quantity that matters is the membrane potential the channel can command. The claim substitutes a
macroscopic current ratio measured under voltage clamp at whatever cRNA dose was injected. These are
not the same quantity, and the source paper **measured the one that matters** in the same figure
series.

Perathoner et al. 2014 (PLoS Genetics 10(1):e1004080; read-level: full-text via PMC3894163) report
that the mutant channels "lead to stronger hyperpolarization causing a shift in the membrane
potential towards −90 to −100 mV", which they identify as E_K in oocytes. That is a measured Vm
endpoint sitting essentially *at* the potassium reversal potential.

Consistency check, derived by me: to hold Vm at −90 to −100 mV with E_K = −98 and E_leak = 0
requires g_K/(g_K+g_L) ≥ 90/98 = 0.918, i.e. **g_K/g_L ≥ 11.25**. Reaching 11.25 from the WT ratios
in the table above (0.69–1.58) requires a **7.1× to 16.3× increase**, not 2×.

The measured Vm endpoint and the "almost two-fold" current ratio are therefore not mutually
consistent under this model. One of three things is true: the macroscopic ratio understates the
physiological conductance change; the leak assumptions are wrong; or WT-Kcnk5b-injected oocytes were
already near −80 mV. **I cannot resolve which** — the Figure 5D panel values are not in the text I
read, and I did not obtain the figure data. But in every case the conclusion is the same: *the
macroscopic current fold-change is not a valid proxy for Vm authority*, and the claim's entire
feasibility number is built on it.

### 2d. The denominators are unsourced

- **σ_V = 5 mV** — the claim cites no measurement of membrane-potential variability in pectoral fin
  bud mesenchyme. None exists in the sources it names: both in-vivo measurements use DiSBAC2(3), a
  non-ratiometric dye that yields no mV at all.
- **"~60 mV available Vm window"** — the body states "40–80 mV"; 60 is the midpoint of an unsourced
  range, presented in the KEY line as a definite quantity.
- **"2.0-fold"** — the paper's wording is "an almost two-fold increase in K+ conductance over that
  of oocytes injected with wild type cRNA". **No numeric fold-change is given in the paper.** "~2.0"
  is a precise-looking rendering of a verbal "almost two-fold", and rounds the wrong way.

### 2e. Setpoint counting

The claim's own arithmetic does reproduce: 17.1/5 = 3.42 ≈ "3.4" ✓, and 3.42/2 = 1.71 ≈ "1.7" ✓.
But `N = range/σ` is a weak convention; reliable discrimination conventionally wants ≥2σ separation.
Derived by me, applied to the physically achievable 8–17 mV band: **0.8–1.7 setpoints at 2σ**, or
1.6–3.4 at 1σ. Every term in that quotient except the fold-change is an assumption.

---

## 3. Pillar 3 — the "unresolved disagreement" on sign. REFUTED as framed.

The claim asserts a conflict between Perathoner 2014 (hyperpolarization) and Jiang 2024
(depolarization). The full text of Perathoner 2014 reports **both**:

- Hyperpolarization, measured by clamp, **in *Xenopus* oocytes** (Fig 5D) — a heterologous
  expression system, not pectoral tissue.
- Depolarization **in *alf* fins**, by DiSBAC2(3): Fig S4 legend states wild-type fins show
  "hyperpolarization localized to discrete regions of the fin" while "*alf* fins in contrast show
  high levels of depolarization across the fin with variable patterns in different tissues." The
  Discussion concedes that depolarization-sensitive dye experiments "suggest that this might indeed
  be the case", and the authors state they cannot exclude that the mutation triggers depolarization
  in fin tissue.

So (a) the tension is **oocyte-versus-fin inside one paper**, not between two papers; and (b) on the
fin-tissue reading, Perathoner's Fig S4 and Jiang 2024 **agree** — both report depolarization by
dye. The claim assigns Perathoner's oocyte measurement to "the pectoral membrane-potential
response", a quantity that paper never measured.

Jiang et al. 2024 (PLoS Biology 22(3):e3002565; read-level: **abstract and figure legends only, via
search summary — I did not open the full text**) further proposes a mechanism that reconciles both
signs: Kcnk5b lowers intracellular K+ in the mesenchyme, and that drives depolarization via Na+
channels, then IP3R-mediated Ca²⁺ release and CaMKK. Under that model an immediate hyperpolarizing
K+ conductance and a downstream depolarized steady state are sequential steps, not contradictions.

**Preserving the disagreement that is real:** whether Jiang's reconciliation is correct is not
settled, and no calibrated pectoral Vm measurement in mV exists in any source I read — both in-vivo
datasets are uncalibrated dye. So the *magnitude and sign of the immediate in-vivo Kcnk5b effect
remains genuinely open.* What is false is the claim's specific framing of it as a flat
two-paper contradiction. That distinction is mine, drawn from the sources; the claim's framing is
the claim's.

---

## 4. Pillar 4 — redundancy with promoter/mosaic routes. Not broken, and the hidden assumption.

I did not verify the optogenetic demonstration the claim asserts; read-level **could-not-access** (I
did not search for it, having spent the budget on the three checkable pillars — stated so the gap is
visible rather than implied). Perathoner 2014 does report mosaic experiments indicating kcnk5b acts
within fin and barbel mesenchyme to set appendage size, which does support restricted control using
the unmodified allele.

**The hidden assumption, relaxed:** the claim treats the WT→*alf* conductance ratio as the whole
achievable dynamic range, so that setpoint count is bounded by 17 mV / 5 mV. But in the system as
actually published, graded output came from the *fraction of cells carrying the allele* — mosaicism
— and from expression dose, neither of which is bounded by a single mutant/WT conductance ratio.
Relaxed, the limiting quantity becomes clone-size and phenotype (fin-ray/segment) resolution, not a
2-fold conductance window. The claim's limiting quantity is therefore the wrong one, and its
"~3 setpoints" is an underestimate of achievable graded control by a route that does not require
protein engineering at all.

Note this cuts *toward* the claim's conclusion while invalidating its argument: engineering the
protein is plausibly unnecessary, which is a different proposition from its being infeasible on
conductance grounds.

---

## 5. Evidence-level honesty audit

The KEY line reads as one continuous measured chain — "~2.0-fold macroscopic K+ current (wild type
-> alf, Xenopus oocyte TEVC, Perathoner et al. 2014) = 17.1 mV … = ~3.4 distinguishable setpoints".
Only the first term is measured, and it is measured as a verbal "almost two-fold" rather than a
number. The mV conversion, the window, σ_V, and the setpoint count are all derived or assumed, under
a conversion model that is never stated and that is wrong (§2b). A derived number presented inside a
measured citation chain is a defect even where the number is close; here it is both mislabelled and
not reproducible.

The claim's recorded evidence level is "unknown", value "n/a". For a claim whose headline is a
specific mV figure and a specific setpoint count, "unknown" understates what is checkable — as this
review shows, the structural half was fully checkable against a public database in minutes, and
failed.

---

## 6. Verdict

**REFUTED.**

- Pillar 1 (pLDDT): refuted. W169 = 90.69, F241 = 84.75 — both >80, at the causal residues the claim
  itself says are the ones that matter. The 69.5 global mean is dominated by a disordered C-terminal
  tail (261–448, mean 43.3). The homodimer figure is attributed to a database that does not serve it.
- Pillar 2 (KEY arithmetic): refuted as stated. 17.1 mV not reproducible (17.5–18.0 from the implied
  slope); the slope is a ceiling, not a value (8–17 mV by parallel conductance); the fold-change is a
  proxy inconsistent with the paper's own measured Vm endpoint; σ_V and window unsourced.
- Pillar 3 (sign disagreement): refuted as framed. The tension is within Perathoner 2014
  (oocyte vs fin); the two dye measurements agree; Jiang 2024 offers a mechanistic reconciliation.
  The underlying in-vivo sign question does remain open — that part I preserve.
- Pillar 4 (redundancy): not broken, and the strongest thing in the claim.

The claim's conclusion — that engineering kcnk5b itself for graded pectoral-restricted control is
unsupported — **may well be correct, on pillar 4 alone**. I am not asserting the opposite, and this
review is not a feasibility finding. But three of four supporting pillars do not survive contact
with the primary data, and the headline KEY number is wrong in both halves. The claim as written
cannot carry its verdict.

## Sources and read-levels

- AlphaFold DB, entry `AF-Q6PFU3-F1` model v6 (kcnk5b, *Danio rerio*): **full data** — REST API
  prediction record and the complete 448-value per-residue confidence array, parsed independently.
  Retrieved 2026-11-04. Values are a record of a computational prediction, not an observation.
- UniProt REST, `gene:kcnk5b AND organism_id:7955`: **full data** — accessions Q6PFU3 (448 aa) and
  A0A8M1PBI1 (448 aa).
- Perathoner et al. 2014, "Bioelectric Signaling Regulates Size in Zebrafish Fins", PLoS Genetics
  10(1):e1004080: **full-text** via PMC3894163 (read in two passes; Figure 5D numeric panel values
  were not located in the text — that gap is flagged in §2c).
- Jiang et al. 2024, PLoS Biology 22(3):e3002565: **abstract and figure legends / search-summary
  only.** Full text not opened. The mechanism in §3 is as reported in those summaries.
- Optogenetic graded-control demonstration asserted by the claim: **could-not-access / not searched.**

```swarm-challenge
{"claim_id": 167, "outcome": "refuted", "reason": "Per-residue pLDDT at the causal alf residues is 90.69 (W169) and 84.75 (F241) — both above 80, refuting the misstatement charge, since the cited 69.5 global mean is dominated by the disordered C-terminal tail (261-448, mean 43.3); the 17.1 mV KEY figure is not reproducible from a 2-fold ratio (RT/F*ln2 = 17.5-18.0 mV) and that slope is an unreachable ceiling rather than a value (8-17 mV by parallel conductance); and the asserted Perathoner-vs-Jiang sign disagreement is misframed, since Perathoner 2014 itself reports fin depolarization by DiSBAC2(3) in Fig S4 in agreement with Jiang 2024.", "corrected_value": "pLDDT W169 = 90.69, F241 = 84.75 (AlphaFold DB AF-Q6PFU3-F1 v6, retrieved prediction, not observation); Vm shift from an exact 2-fold increase in g_K = 8-17 mV (derived, parallel conductance, E_K = -98 mV), not 17.1 mV; 0.8-1.7 distinguishable setpoints at a 2-sigma criterion with the claim's unsourced sigma_V = 5 mV", "depends_on": ["AlphaFold DB entry AF-Q6PFU3-F1 model v6 per-residue confidenceScore array (448 values) and globalMetricValue 69.5 / fractionPlddtVeryLow 0.339", "AlphaFold DB serving only monomer predictions for Danio rerio kcnk5b (Q6PFU3 monomer entry; A0A8M1PBI1 absent)", "UniProt Q6PFU3 448-aa sequence, on which residue 169 = W, residue 241 = F, 98-102 = TIGYG and 203-207 = TVGFG", "Perathoner et al. 2014 PLoS Genetics 10(1):e1004080 reporting an 'almost two-fold increase in K+ conductance' with no numeric fold-change stated", "Perathoner et al. 2014 reporting mutant oocyte Vm shifting towards -90 to -100 mV, and E_K in Xenopus oocytes as -90 to -100 mV", "Perathoner et al. 2014 Figure S4 reporting DiSBAC2(3) depolarization across alf fins, and the Discussion conceding possible fin depolarization", "Jiang et al. 2024 PLoS Biology 22(3):e3002565 reporting DiSBAC2(3) depolarization in pectoral fin buds via reduced intracellular K+ and Na+ channels (abstract/figure-legend read-level only)", "the claim's own unsourced sigma_V = 5 mV and 40-80 mV Vm window, used unchanged for comparability"]}
```
