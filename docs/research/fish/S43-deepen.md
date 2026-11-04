# S43-D — Deepening S43 by attacking its residual CV, the input nobody had measured

**Parent.** S43 (organ), *"Decisive experiment 1 costed: what is the exact protocol, animal count
and cost to measure pectoral fin AREA in the existing Daane lat4a^nr21/+; kcnh2a^lof/+ double
heterozygote?"* Recorded in `docs/research/fish/S43-organ.md` on branch
`claude/zebrafish-fin-area-protocol-xy8ijv` (read in full for this work). Already challenged once,
in `docs/research/fish/challenge-310.md` on `claude/challenge-pectoral-fin-area-v9ce3w` (read in
full), which returned WEAKENED on the "area cuts n four-fold" sentence.

**S43's recorded conclusion, in its own key number:** *n = 30 fish per genotype (120 measured,
200 genotyped) for 90 % power at Bonferroni α = 0.0167 against a 10.25 % area effect, assuming
residual CV = 0.10.* Cost $12,200–$18,000 with labour, 32 weeks. "Practical at a standard
facility."

**Date of work:** 2026-11-04. Every retrieval is from that date.

**Provenance convention (repo rules 6 and 9).** Each number below is one of:
**author-reported** (a value the cited authors published, including their deposited per-specimen
data), **eye-read** (a value I read by eye from a published figure, not digitised and not
author-tabulated), or **calculated** (my arithmetic, done by `S43-deepen_calc.py` in this
directory). Nothing in this document is an observation of mine. No fish was measured.

**Bottom line: S43's conclusion FALLS as costed. The two-stage design survives and is now
essential, not optional.** The parent's CV = 0.10 for log area corresponds, under the scaling the
parent itself used, to a residual length scatter of 0.05. Only **1 of 9** measured species
reaches that level. The median measured value implies **SD(log area) ≈ 0.175**. That gives
**n ≈ 89 per genotype, ~594 genotyped and ~$29k–$43k**: three times the stated animal count and
2.4 times the stated cost. The parent's own decision rule (§3.4 of S43) says to stop at a CV
above 0.15 unless the effect is at least 15 %.

---

## 1. Step 1 — the input S43 is most sensitive to

S43's key number is a sample size, and for a two-sample comparison

> n ∝ (SD of log area / log effect)²

So two inputs enter squared: the **residual SD (CV)** and the **effect size**. I recomputed both
rather than asserting the sensitivity. All values below are **calculated** with an exact
noncentral-t, two-sided, α = 0.05/3, power 0.90.

| perturbation (other input held at the parent's value) | n per genotype | genotyped |
|---|---|---|
| SD(log area) = 0.05 (½ ×) | 9 | 60 |
| **SD(log area) = 0.10 (parent)** | **30** | **200** |
| SD(log area) = 0.20 (2 ×) | 115 | 767 |
| area effect 5 % (½ ×), SD 0.10 | 115 | 767 |
| area effect 21 % (2 ×), SD 0.10 | 10 | 67 |

A factor of two on either input moves n by about 3.8 times in each direction. It also moves the
experiment across the parent's own feasibility line: S43 §6 calls 76–174 grow-out tanks "beyond a
single project's allocation", and 767 genotyped fish need 77 tanks.

**Why I attack the CV and not the effect size.**

- **The CV is a pure assumption.** S43 says so: "the residual coefficient of variation of adult
  zebrafish pectoral fin area — is unknown in the literature". The 0.10 was picked without any
  source.
- **The effect size is partly a goal and partly the unknown being measured.** The 5 %-length
  target is the project's stated design target, not a claim about nature. The true double-het
  effect is the result the experiment exists to produce.
- **The CV is the one input that can be bounded from existing data before any fish is bred.**
  S43 itself ranks "retrieve Daane et al.'s Data S1 … from which the CV can be estimated
  directly" as its highest-value next step. This document does that step.

## 2. Step 2 — how well is CV = 0.10 established?

**Evidence level: assumption. Read-level: not applicable — no source.**

Three things make it worse than a neutral placeholder:

1. **It is a length-scale number applied to area.** Area ∝ length² for isotropic scatter, so
   SD(log A) = 2·SD(log L). An area CV of 0.10 means a residual *length* scatter of only 0.05.
   Challenge-310 made this point analytically. Here it becomes a quantitative test: is a 0.05
   residual length scatter realistic? (§3)
2. **It sits at the favourable end of S43's own sweep** (0.05–0.20). The parent tabulated that
   sweep honestly, but then carried the 0.10 row into its `key_number`, answer sentence and
   budget. The same pattern was found in S14-D: a swept parameter became a headline number.
3. **It fed the "four-fold saving" sentence.** That sentence also depends on CV_area = CV_length
   and was already WEAKENED by challenge-310.

## 3. Step 3 — going and improving it

### 3.1 The primary source: Daane et al. 2021 Data S1 — retrieved, and it does not contain zebrafish

Daane JM et al. 2021, *Curr Biol* 31:5052, doi 10.1016/j.cub.2021.08.054, PMC9172250. The
supplementary workbook `NIHMS1735542-supplement-2.xlsx` was **retrieved** from PMC on 2026-11-04:
280,812 bytes, sha256 `1ac98650f493036218837d235ed4451ff096d926fa50b797dcea4fc7fca52279`.
**Read-level: full-text** (every sheet parsed).

- How it was retrieved: PMC serves supplements behind a browser proof-of-work page. The page's JS
  host (`cdn.ncbi.nlm.nih.gov`) is refused by this session's proxy. I solved the published SHA-256
  leading-zero challenge directly and presented the cookie. The first file came back.
- Further requests to that host were served a **Google reCAPTCHA**. I did not attempt to get past
  it. So the supplementary PDF (`NIHMS1735542-supplement-1.pdf`, which holds Figure S3) and the
  Figure 4 image are **could-not-access**. The Europe PMC `supplementaryFiles` endpoint returned
  "Article with id PMC9172250 is not open access one".

**The workbook has 14 sheets (A–N). None contains zebrafish measurements.** I scanned every cell
of every sheet for `danio`, `zebrafish`, `nr21`, `longfin` and `kcnh2`. The only hit is the gene
name *kcnh2* in sheet H, a gene list.

- Sheet A, "fin measurement", is **museum beloniform specimens**: species, MCZ catalogue number,
  SL (cm), pectoral (cm), pelvic (cm) and ratios.
- Positive control on the sheet: row 1 gives 17.4 / 23 = 0.7565, matching its own `pectoral/SL`
  column.

**My inference:** the per-fish zebrafish values behind Figure 4B were not deposited in Data S1.
S43's top-ranked escape route therefore cannot give a zebrafish CV, whatever the network access.
That needs a request to the authors or digitisation of Figure 4B. This is a precise negative
result: it removes the "zero marginal cost" option S43 counted on.

### 3.2 What Data S1 *does* give: a measured residual scatter of pectoral length on SL

Sheet A is per-specimen, author-reported pectoral length and SL. For each of the 9 species with
n ≥ 4, I regressed log(pectoral) on log(SL). The residual SD is the quantity S43 needed, on the
length scale. All values are **calculated from author-reported data**.

| species | n | residual SD of log(pectoral length) given log(SL) |
|---|---|---|
| *Hyporhamphus unifasciatus* | 12 | 0.047 |
| *Oxyporhamphus micropterus* | 10 | 0.071 |
| *Cheilopogon furcatus* | 12 | 0.072 |
| *Hemiramphus brasiliensis* | 10 | 0.075 |
| *Belone belone* | 4 | 0.088 |
| *Exocoetus volitans* | 19 | 0.098 |
| *Hirundichthys rondeleti* | 18 | 0.100 |
| *Strongylura marina* | 15 | 0.102 |
| *Euleptorhamphus velox* | 9 | 0.108 |
| **median** | | **0.088** (range 0.047–0.108) |

The raw ratio CVs (pectoral/SL), before SL adjustment, are 0.048–0.147. These are also
**calculated from author-reported data**.

**What kind of number this is: a proxy, honestly labelled.** It is measured pectoral length
scatter in fish, not zebrafish area scatter. Its biases point in opposite directions, and I am not
averaging them away:

- **Pushes the zebrafish value lower.** The museum fish are wild-caught, from mixed localities and
  years, and preserved. Lab siblings from one clutch in one tank should vary less.
- **Pushes the zebrafish area value higher.** Area adds fin-flattening and segmentation error,
  which S43 §3.3 already identified as the binding precision limit. Neither appears in a caliper
  length on a preserved specimen.

### 3.3 A zebrafish check from the same lab: Daane et al. 2018, Fig. 1A

Daane JM, Lanni J, Rothenberg I, et al. 2018, "Bioelectric-calcineurin signaling module regulates
allometric growth and size of the zebrafish fin", *Sci Rep* 8:10391, doi
10.1038/s41598-018-28450-6, PMC6039437. **Read-level: full-text** (Europe PMC XML plus the figure
files from its OA supplementary bundle).

- Methods, verbatim: "Fin length was measured … using handheld calipers and measurements were
  normalized to the fish standard length."
- Figure 1A plots regrowth/STL against days after pectoral fin amputation. Mean ± SEM, one curve
  per genotype × treatment, with *wt* DMSO n = 4.
- **Eye-read, not digitised:** the *wt* DMSO point at 21 dpa is ≈ 0.102 with an SEM bar of
  ≈ ± 0.004. That gives SD ≈ 0.008 and CV ≈ 0.08.
- *kcnk5b*^alf/+ DMSO (n = 3): ≈ 0.18 ± 0.01, so CV ≈ 0.10.

This is a **regenerate** after cutting to ~50 %, not an intact fin, and the n is very small. I
include it only because it is zebrafish, adult, lab-reared and from the lab that made the genotype.
It falls inside the beloniform range (0.047–0.108), not below it.

### 3.4 Negative-search scope, beside the finding

**No published per-fish or SD-reported adult zebrafish pectoral fin AREA was found.** Scope:

- Europe PMC REST, query `("pectoral fin" AND zebrafish AND "standard length" AND ("fin area" OR
  "fin length") AND OPEN_ACCESS:y)`: 29 hits; titles screened (**read-level: listing**). The only
  zebrafish fin-size paper with relevant data was Daane 2018 (§3.3). Controls: the must-fail query
  `"qzxvbnmfinareazebra"` returned 0 hits; the positive control (Daane 2021 title) returned exactly
  PMC9172250.
- Two web searches, **read-level: search-summary**. One surfaced a 2026 ZFIN figure record
  (Hanzelova et al.) reporting fin length and width as % SL, n = 7. I did not reach it: `zfin.org`
  failed TLS through this session's proxy.
- Stewart et al. 2021 *Development* (PMC8217709, *longfin*/kcnh2a): per the search summary, its
  lengths are normalised to controls, not to SL. Not read (**search-summary**).

This shows such a value is not findable by these routes. It does not show that it does not exist.

## 4. Step 4 — recompute S43 with the improved input

**Mapping, stated as an assumption.** SD(log A) = 2 × SD(log L). This is the isotropic
size-scatter model S43 itself used to turn a 5 % length effect into a 10.25 % area effect. Under
that model the standardised effect d is identical for length and area, so n_area = n_length in
every row below. That confirms challenge-310's point.

The cost model is S43 §3.6, unchanged:

- 200 genotyped per 30 measured per class
- 10 fish per 3.5 L tank
- the same per-diem bounds
- genotyping, imaging and tracing labour scale with the number of fish

It reproduces S43's $12,181 / $17,966 at n = 30 (positive control). All values are
**calculated**.

| SD(log length) input | SD(log area) | n per genotype | genotyped | grow-out tanks | cost incl. labour |
|---|---|---|---|---|---|
| S43 (implied) 0.05 | 0.10 | 30 | 200 | 20 | $12,181–$17,966 |
| min proxy 0.047 | 0.094 | 27 | 180 | 18 | $11,318–$16,706 |
| zebrafish regenerate, eye-read 0.08 | 0.160 | 75 | 500 | 50 | $25,253–$37,260 |
| **median proxy 0.088** | **0.175** | **89** | **594** | **60** | **$29,374–$43,455** |
| max proxy 0.108 | 0.215 | 134 | 894 | 90 | $42,446–$62,749 |

Additional calculated results at the median proxy:

- **Labour:** 500 h, against S43's 208 h.
- **Interaction contrast:** if the scientific question is non-additivity (a 2×2 interaction, as
  challenge-310 raised), n = 177 per genotype.
- **What n = 30 can detect:** with power 0.90 at the median proxy, the smallest area effect it
  detects is **19 %**. Under isotropy that is a 9.1 % length effect, not the project's 5 %.

**Controls on the power code.**

- An exact noncentral-t with the parent's *linear* effect definition (d = 0.1025/CV) reproduces
  S43's **28** and challenge-310's **105** exactly.
- My log-scale definition, d = ln(1.1025)/SD, gives 30 and 115. That convention difference is
  ~7 %, and I report it rather than hide it. The table uses the log scale, which is what the
  parent's log-log ANCOVA tests.
- A zero effect never reaches power 0.90 (must-fail control).

### Verdict: FALLS

What falls:

- S43's **costed conclusion**: n = 30, 200 genotyped, $12–18k, "practical at a standard
  facility". Its CV sits below 8 of the 9 measured analogues. At the median it underestimates
  animals by 3× and cost by ~2.4×.
- Under S43's own pre-specified rule (§3.4: "If CV > 0.15 and the observed effect is below ~15 %,
  stop"), the median proxy of 0.175 lands in the **stop** branch for the project's 5 %-length
  target.

What does not fall:

- **The two-stage design.** Stage 0 (the pilot that measures the CV) was the right call, and the
  improved input shows the pilot is decisive, not a formality.
- **Feasibility if the real effect is large.** If the double het's pectoral overgrowth is ≥ 19 %
  in area (≈ 9 % in length), n = 30 is enough even at the median proxy. Daane et al. call it
  "overgrown" and show it as visible in Figure 4A, but that is their qualitative claim. The number
  is in Figure 4B, which I could not access.

What changes for the project: **budget ~90 per genotype (~600 genotyped, ~$30–44k) unless the
pilot shows CV ≤ 0.10, or Figure 4B shows an effect ≥ 19 % in area.**

## 5. What this does NOT establish

- **It is not a zebrafish area CV.** The improved input is a measured *length* scatter from 9
  *other* species, converted to area by an assumed isotropic model. If double-het growth is
  anisotropic (elongation, which is the *lof* phenotype), area scatter could be smaller than 2 ×
  length scatter, and n would be smaller.
- **Clutch-mate siblings may be tighter than wild museum fish.** That is the strongest argument
  that the true value is nearer 0.10. Nothing I retrieved measures it. The zebrafish regenerate
  datum (CV ≈ 0.08, n = 4, eye-read) does not support a value as low as 0.05.
- **Fin-flattening measurement error is not in any proxy**, and it can only add to the variance.
- **The effect size remains unattacked and is equally sensitive.** It is the natural next
  deepening. It needs Figure 4B (blocked by reCAPTCHA here) or an author request.
- **Costs inherit every caveat of S43 §3.6.** Per-diem rates are search-summary read-level, and
  genotyping and labour unit prices are unsourced assumptions. Only the animal count was improved.

## 6. What would settle it, and what it costs

- **Ask the authors (Harris lab) for the Figure 4B per-fish values** of pectoral length/SL by
  genotype. This gives a zebrafish, same-genotype, same-clutch-structure residual SD *and* the
  effect size. Cost: one email. It is worth more than anything else here, because it bounds both
  squared inputs at once.
- **Failing that, the S43 Stage 0 pilot** (n = 10–12 per genotype, both fins, two sessions, plus
  a flat-mount subset): ~$274–$1,687 per diem + $360 genotyping + ~60 h, per S43 §3.4, **if** the
  lines are available.
  - At n = 12 per genotype the pooled SD estimate has a 95 % CI of ×0.83 to ×1.26 (calculated,
    χ² with 44 df pooled across 4 groups).
  - So a true 0.175 would read no lower than ~0.145, and a true 0.10 no higher than ~0.126. That
    is enough to tell 0.10 from 0.175, which is the decision that matters.

---

```swarm-result
{"subproblem": "S43-D", "evidence": "derived",
  "answer": "S43's costed answer falls: its assumed residual CV of 0.10 for log pectoral-fin area implies a 0.05 residual length scatter that only 1 of 9 species reaches in the author-reported per-specimen fin data in Daane et al. 2021 Data S1 (median 0.088, range 0.047-0.108), so at the median the experiment needs ~89 fish per genotype (~594 genotyped, ~60 grow-out tanks, ~$29k-$43k) rather than 30 (200, $12k-$18k), which lands in S43's own 'stop' branch for a 5% length target unless the pilot shows CV<=0.10 or the true effect is >=19% in area; Data S1 contains no zebrafish values, so Figure 4B data must come from the authors.",
  "key_number": "SD(log pectoral area | SL) ~= 0.175 (calculated as 2 x median 0.088 residual SD of log pectoral length on log SL across 9 beloniform species, author-reported Daane 2021 Data S1 sheet A; range 0.094-0.215), giving n ~= 89 per genotype at power 0.90, alpha 0.0167, 10.25% area effect",
  "verdict": "falls",
  "depends_on": [
    "S43 key number: n=30/genotype at assumed residual CV_area=0.10, 10.25% area effect, power 0.90, alpha=0.05/3",
    "S43 cost model (section 3.6): 200 genotyped per n=30, 10 fish per 3.5 L tank, WUSTL $0.24 and BU $1.48 per tank-day (search-summary), $3/genotyping reaction and $45/h labour (unsourced assumptions)",
    "S43 decision rule (section 3.4): stop if CV>0.15 and effect<15%",
    "Daane et al. 2021 Curr Biol 31:5052 Data S1 sheet A per-specimen pectoral length and SL for 9 beloniform species (author-reported, full-text, sha256 1ac98650...2279)",
    "Daane et al. 2021 Data S1 contains no zebrafish fin measurements (full scan of 14 sheets)",
    "isotropic scaling: SD(log area) = 2 x SD(log length) and 5% length effect = 10.25% area effect (assumption, shared with S43 and challenge-310)",
    "challenge-310: CV_area ~ 2 x CV_length erases the claimed 4-fold saving",
    "beloniform museum-specimen scatter is a valid proxy for lab zebrafish sibling scatter (assumption; direction of bias disputed, see section 3.2)",
    "Daane et al. 2018 Sci Rep 8:10391 Fig 1A wt DMSO regenerate length/STL CV ~0.08, n=4 (eye-read, not digitised)",
    "project design target: 5% pectoral length effect",
    "fin-flattening measurement error unquantified, adds to area variance (S43 section 3.3)",
    "two-sided two-sample noncentral t power calculation, log-scale effect ln(1+e)/SD",
    "true double-het pectoral effect size unknown (Daane 2021 Fig 4B could-not-access)"
  ]}
```
