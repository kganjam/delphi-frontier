# S43 (organ) — Decisive experiment 1, costed: a protocol to measure pectoral fin AREA in the *lat4a*^nr21/+; *kcnh2a*^lof/+ double heterozygote

Project: `zebrafish-flight`. Scale: organ. Written 2026-11-04.

**Evidence level of the answer in §4: `derived`.** No fish were measured for this document.
Every number in §3 is arithmetic I performed, labelled as such. The one number the protocol
turns on — the residual coefficient of variation of adult zebrafish pectoral fin area — is
**unknown in the literature** (negative search, scope in §2.4), which is why the answer is a
two-stage design whose first stage exists to measure it.

---

## 1. The question, restated precisely, with the numbers that make it hard

Daane et al. (2021) crossed *lat4a*^nr21/+ to *kcnh2a*^lof/+ zebrafish and reported that the
resulting trans-heterozygotes have overgrown **paired** fins, wild-type-sized **medial** fins,
and a hypocercal caudal fin — a fin bauplan they describe as resembling flying fishes. They
quantified **pectoral fin length normalized by standard length (SL)**.

They did not measure **area**. The string "area" does not occur anywhere in the full text of
that paper (§2.1). Area, not length, is the quantity that enters any lift calculation, so the
project's gliding argument rests on a measurement that has never been made in this genotype.

What makes it hard, in numbers:

1. **The project's own target effect is 5–10 %.** That is the band the rest of this project has
   been working to. Detecting a 5 % difference in a continuous morphological trait requires
   either a very small residual CV or a large *n*; which of those applies is not known in
   advance (point 3).
2. **The effect is a ratio, not an absolute.** Fin size scales with body size, and the whole
   claim is about *allometry*. So the measurement is not "area" but "area at a given SL", and
   the statistical object is a slope or an ANCOVA-adjusted mean, not a raw mean.
3. **The denominator of every power calculation is unavailable.** I could find no published
   value for adult zebrafish pectoral fin area, let alone its CV (§2.4). Without it, required
   *n* spans **3 to 434 per genotype** across the plausible range (§3.2) — a 145-fold spread
   that is the difference between a trivial experiment and one that breaks a facility.
4. **The measurement precision requirement is severe and is set by fin flattening, not optics.**
   On assumed fin geometry, a 5 % area change corresponds to a uniform outline displacement of
   ~26 µm (§3.3). Optical resolution reaches that easily; reproducibly spreading a living fin to
   within 26 µm of the same configuration twice is the actual bottleneck.
5. **The experiment cannot be fully blinded.** *kcnh2a*^lof/+ and *lat4a*^nr21/+ each have a
   visible fin phenotype (§2.1). A human measuring a fin cannot be blind to fin size. This is
   not fixable by protocol discipline; it is mitigated, not removed (§3.5).

---

## 2. What is measured — every value with source, year and read-level

### 2.1 Daane et al. 2021 — the primary source for the genotype

Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP.
"Modulation of bioelectric cues in the evolution of flying fishes." *Current Biology* 31(22):
5052–5061.e8, 2021. DOI 10.1016/j.cub.2021.08.054. PMID 34534441. PMCID PMC9172250.
**Read-level: full-text** — retrieved as NLM-DTD XML via NCBI E-utilities
(`efetch.fcgi?db=pmc&id=PMC9172250`, 202,692 bytes, retrieved 2026-11-04; the Europe PMC
`fullTextXML` endpoint returned HTTP 500 for the same article on the same day, and the record
reports `isOpenAccess: "N"` with an author-manuscript licence).

Verbatim, the authors' claim about the double heterozygote:

> "double mutants between kcnh2a lof /+ and lat4a nr21 /+ are viable and show specific,
> non-additive variation in proportion among fins: while all fins of kcnh2a lof /+ are overgrown
> and all fins of lat4a nr21 /+ are shortened, the lat4a nr21 /+ ; kcnh2a lof /+ fish show
> wild-type-sized medial fins, while the paired fins are overgrown"

and

> "the caudal fin of kcnh2a lof /+ ; lat4a nr21 /+ , while generally wild type in size, is
> hypocercal, with an elongated ventral lobe"

What they measured, verbatim from the Figure 4 legend:

> "(B and C) Pectoral fin length (B) and caudal fin length (C) suppression of overgrowth in
> medial fin by lat4a mutation. In (B) and (C), length normalized by SL."

Statistics, verbatim:

> "The statistical association between genotype and fin size was performed using one-way ANOVA,
> with all pairwise comparisons subsequently analyzed using Tukey Honest Significant Difference
> (TukeyHSD) ( Figures 3B , 3D , 4B – 4E , S2B , and S2I ). Unless otherwise indicated, n refers
> to the number of individual fish used in the experiment."

**My inference, separated from their claim:** because the quantity reported is *length* and the
word "area" does not appear in the full text (literal string count: 0 occurrences of "area",
0 of "ImageJ", 0 of "Fiji" in the de-tagged full text), pectoral fin **area** is unmeasured in
this genotype, and the imaging hardware and tracing software used for the Figure 4B lengths are
not stated in the paper. Both are therefore **unknown** and must be specified de novo.

Per-genotype *n* for Figure 4B: **unknown.** The legend does not state it, and the values sit in
the plotted figure and in Data S1, which I could not retrieve (supplementary files are not served
through the E-utilities full-text route I had).

Husbandry and age definition, verbatim:

> "For all experiments, adult stages were defined by reproductively mature fish ≥3 months old.
> Males and females were used together in analyses as both sexes showed comparable overgrowth and
> growth regulation."

Husbandry conditions are deposited at protocols.io, DOI 10.17504/protocols.io.mrjc54n.
**Read-level: could-not-access** (protocols.io does not resolve from this session; see §2.5).

### 2.2 Allele and line identities — verbatim from the Key Resources Table (read-level: full-text)

| Line | Designation in paper | Source / repository |
|---|---|---|
| *lof*^dt2 | `lof dt2` | van Eeden et al. / Haffter et al.; **ZIRC ZL86** |
| *lof*^j6e1 | `lof Df(Chr02:csnk1g2a,rnf2,kifap3b)j6g1/j6g1` | Iovine and Johnson; **ZIRC ZL1494** |
| *lat4a*^nr21 | `lat4 nr21` | **"This paper"; internal designation `dmh26`; no repository ID given** |
| *lat4a*^del | `lat4a del` | "This paper"; internal designation `mh152` |

Molecular nature of the two alleles, verbatim:

- *lat4a*^nr21: "the predicted T200K substitution of nr21"; an in-cis frameshift revertant
  "(L106Rfs39, nr21 )" also exists.
- *kcnh2a*^lof: "we identified an inversion on chromosome 2 in lof with break points between 5′
  prrx1a and 5′ kcnh2a without affecting the coding region of either gene"; "the lof mutation
  results in an upregulation of kcnh2a in fins"; the *lof* allele "imparts a gain-of-function
  effect."

A directly relevant availability warning, verbatim, about the revertant lines:

> "These lines are no longer maintained nor frozen, thus are used for confirmation of mapping
> only."

**My inference:** *lof*^dt2 is obtainable from a stock centre (ZL86). *lat4a*^nr21 is not listed
at any repository in this paper and must be requested from the originating lab; whether it is
currently held, and whether it is cryopreserved, is **unknown**. The sentence above shows this
group has let related lines lapse, so the risk is not hypothetical. **No genotyping primers for
either *nr21* or the *lof* inversion appear in the Key Resources Table**, and the inversion
breakpoint coordinates are in Figure S3, which I could not retrieve — so breakpoint-spanning
primer design is blocked on a figure I have not read.

A second inference worth stating plainly: **a double-heterozygous stock cannot exist as a stock.**
The genotype is produced fresh by crossing the two single-heterozygote lines each generation.
The subproblem's phrase "the existing double heterozygote" is therefore slightly wrong in a way
that helps: what exists is two single-het lines plus a demonstrated cross, and that cross yields
all four genotypes as **siblings in one clutch at 1:1:1:1**, which is the strongest possible
control structure for this measurement (§3.1).

### 2.3 Facility per diem rates — the only unit costs I could source

**Read-level: search-summary.** Direct fetches of the facility fee schedules failed: every
candidate host (`zebrafishfacility.wustl.edu`, `bu.edu`, `urmc.rochester.edu`) failed DNS
resolution from this session, which this environment reports for hosts outside the session's
allowed network domains. I therefore quote these as search-summary and they must be re-verified
against a current local schedule before being used in a budget.

| Facility | Rate | Vintage |
|---|---|---|
| Washington University fish facility | $0.09 (1.1 L), **$0.24 (3.5 L)**, $0.47 (8 L) per tank per day, adult room; $0.18 / $0.48 / $0.95 in nursery and quarantine rooms | schedule stated effective Sep 2024 |
| Boston University | **$1.48** per zebrafish tank per day, FY2025, rising to $1.67 by FY2029 | FY25 memo, eff. 2024-07-01 |
| University of Rochester | $0.475 per zebrafish tank, FY25; $0.523 FY26 (described as subsidised) | FY25 memo |
| Montana State | $2.05 per cage per day (Zebtec system), $2.67 (static) | FY24/25 |

**Disagreement preserved, not averaged:** these span **$0.24 to $2.67 per tank per day**, an
11-fold range, because they price different tank volumes, different room types, and different
degrees of subsidy. Washington University is the relevant anchor for one sense — Johnson SL's
laboratory is at Washington University and some of the Daane fish were housed there (the paper
states "Similar conditions were present at Washington University Medical School (SLJ lab)") — so
I carry the WUSTL 3.5 L adult rate as the low bound and the BU flat rate as the high bound, and I
report both totals rather than a single figure.

### 2.4 The missing number — negative result, with its scope

**No published value for adult zebrafish pectoral fin area, or its coefficient of variation, was
found.**

Scope of the negative search, stated precisely:

- Europe PMC REST `search` endpoint, three independent query formulations
  (`zebrafish pectoral fin area mm2 morphometric`; `zebrafish fin area Fiji planimetry adult`;
  `zebrafish pectoral fin allometry area standard length`), 8 results each, 2026-11-04. Every
  returned record was off-target (medaka osteotoxicity, cichlid development, conference abstract
  collections). **Read-level: listing** for all returned records.
- One general web search for zebrafish pectoral fin area / CV / morphometrics. It returned
  fin-**length** allometry material only: a ZFIN figure record for Perathoner et al. 2014
  reporting fin length normalized to SL with an allometric coefficient *k* from linear
  regression, and a Silic et al. 2020 figure comparing caudal fin length to SL with *k* = 1.5 in
  mutants versus *k* = 1.0 in isometric wild-type siblings. **Read-level: search-summary.** I did
  not reach the underlying papers: `zfin.org` returned HTTP 503 twice, and the ZFIN mirrors
  (`franklin.zfin.org`, `crick.zfin.org`) plus `repository.library.noaa.gov` all failed DNS
  resolution from this session.
- Within Daane et al. 2021 itself (full text): zero occurrences of "area".

What this negative does **not** establish: that no such measurement exists. It establishes that
it is not discoverable by three Europe PMC queries and one web search, and that the one paper
that made this genotype did not make it. The *k* ≈ 1.0 isometry figure for wild-type caudal fin
length vs SL is the closest anchor available and it is for the wrong fin and the wrong dimension.

### 2.5 Hosts that could not be reached

`zfin.org` (HTTP 503), `franklin.zfin.org`, `crick.zfin.org`, `repository.library.noaa.gov`,
`zebrafishfacility.wustl.edu`, and protocols.io all failed from this session — the mirrors and
facility hosts by DNS non-resolution, which this environment reports for hosts outside the
session's allowed network domains. They would have to be allowed in the session's network
settings to be read. `eutils.ncbi.nlm.nih.gov` and `www.ebi.ac.uk` did resolve, which is how the
primary source was obtained in full.

---

## 3. What I computed — arithmetic, assumptions, all marked as computation

Everything in this section is **computation**, not observation. Script: inline `python3` runs
recorded in this session; all inputs are stated here.

### 3.1 The design the cross gives you for free

A single-pair cross *lat4a*^nr21/+ × *kcnh2a*^lof/+ (both verified as single hets by PCR) yields
Mendelian **1:1:1:1** wild-type : *lat4a*^nr21/+ : *kcnh2a*^lof/+ : double het. **Computation:**
these four groups are full siblings, same clutch, same tank, same age, same water — which removes
clutch, batch, tank-density and age as confounders without any statistical adjustment. This is
why the primary experiment is one cross, not four lines compared across tanks.

Multinomial check, 20,000 simulated draws, seed 0 (**simulation**): the probability that all four
genotype cells reach *n* ≥ 30 is 0.900 at 160 genotyped adults, 0.990 at 180, and >0.999 at 200.
**So genotype 200 to guarantee 30 per cell.**

### 3.2 Power calculation — and the amplification that makes area the better measurement

**Derivation, marked as computation.** If the fin scales isotropically, an *x* % increase in fin
length implies a (1+*x*)² − 1 increase in area:

| length effect | implied area effect |
|---|---|
| +5.0 % | **+10.25 %** |
| +7.5 % | +15.56 % |
| +10.0 % | +21.00 % |

**This is the single most useful thing in this document.** The project's 5–10 % target was set on
a linear dimension. Measuring *area* roughly doubles the percentage effect, and because required
*n* scales as 1/effect², it cuts required *n* by about **four-fold** at the same CV. The
recommendation to measure area is therefore not merely more aerodynamically relevant than
measuring length; it is the statistically cheaper measurement. The caveat is that this holds only
if the measurement CV of area is not itself much larger than that of length — which is exactly
what the pilot in §4 must check, since area requires fin flattening and length does not.

**Required *n* per genotype** (two-sided two-sample comparison of means on log-area,
Bonferroni α = 0.05/3 = 0.0167 for the three contrasts against wild-type siblings, Guenther
small-sample correction +z²α/4; Dunnett would be marginally less conservative):

| residual CV | area effect 5 % | 10 % | 10.25 % | 21 % |
|---|---|---|---|---|
| 0.05 | 23 / 29 | 7 / 9 | 7 / 8 | 3 / 3 |
| 0.08 | 56 / 71 | 15 / 19 | 15 / 18 | 5 / 6 |
| **0.10** | 86 / 110 | 23 / 29 | **22 / 28** | 7 / 8 |
| 0.15 | 190 / 245 | 49 / 63 | 47 / 60 | 13 / 16 |
| 0.20 | **337 / 434** | 86 / 110 | 82 / 105 | 21 / 26 |

(cells are *n* per genotype at power 0.80 / power 0.90)

### 3.3 Why precision, not resolution, is the binding constraint

**Computation on assumed geometry — the geometry is an assumption, not a measurement, because
§2.4 found no published fin area.** Assume an adult pectoral fin bounding box 4.0 × 1.5 mm and a
lamina filling 75 % of it: area ≈ 4.50 mm², perimeter ≈ 8.65 mm (ellipse-equivalent perimeter
×1.15 for the elongate outline).

- A 5.00 % area change = 0.225 mm², which a uniform outline displacement of **26.0 µm** produces.
- A 10.25 % area change = 0.461 mm², i.e. **53.3 µm**.

A flatbed scanner at 4800 dpi is 5.3 µm/px; a stereomicroscope at 2 µm/px is routine. **So optics
are not the constraint by an order of magnitude.** The constraint is reproducibly abducting and
flattening a living fin to within ~26 µm of the same configuration, and any systematic difference
in how hard a fin is spread between genotypes becomes a direct, uncorrectable area bias. This is
the reason the protocol below spends its effort on repeated measures and a terminal flat-mount
validation rather than on better cameras.

### 3.4 The protocol

**Stage 0 — pilot (the gate). This is the actual recommendation.**

Purpose: estimate the residual CV of normalized pectoral fin area and the measurement-error
component of it. Nothing downstream can be sized until this exists.

- If adult fish of the four genotypes are already held anywhere: image *n* = 10–12 per genotype,
  two sessions, both fins. **~2 weeks, imaging and tracing labour only.**
- If they must be bred: one cross, *n* ≈ 12 per genotype, ~50 genotyped adults, 6 tanks.
  **~26 weeks** (rearing-dominated) and, at the per diem bounds of §2.3,
  6 × 190 = 1,140 tank-days → **$274 (WUSTL 3.5 L) to $1,687 (BU)**, plus
  60 × 2 × $3.00 = $360 genotyping, plus ~60 h labour.

**Decision rule, pre-specified:** if the pilot's residual CV ≤ 0.10, proceed with *n* = 30 per
genotype (Stage 1 as costed). If 0.10 < CV ≤ 0.15, *n* = 60. If CV > 0.15 and the observed effect
is below ~15 %, stop and report the measurement as not practical at the 5 % level — see §6.

**Stage 1 — the measurement.**

1. **Lines.** Obtain *lof*^dt2 from ZIRC (ZL86). Obtain *lat4a*^nr21 (`dmh26`) from the Harris
   laboratory — no repository ID exists for it (§2.2). Verify both by sequencing before crossing.
2. **Genotyping assays, designed de novo** (none are published, §2.2). *lat4a*^nr21: allele-specific
   PCR or dCAPS at the T200K codon, confirmed by Sanger on a 10 % subsample. *kcnh2a*^lof:
   breakpoint-spanning PCR across the chr2 inversion junction — **blocked until the breakpoint
   coordinates in Figure S3 are read**; fallback is a copy-number or linkage assay, or the ZIRC
   *lof*^j6e1 deletion (ZL1494) as a complementation reagent. Validate both assays on known
   carriers and known wild-types before any cross.
3. **Cross.** One pair, *lat4a*^nr21/+ × *kcnh2a*^lof/+, single clutch where possible; a second
   independent pair as a clutch replicate, entered as a random effect.
4. **Rearing.** Raise to adult at a **fixed, equal stocking density across all tanks** (10 fish
   per 3.5 L), because density affects growth and growth affects fin allometry. Genotype is
   unknown to the husbandry schedule: do **not** sort by phenotype at any point before genotyping.
5. **Imaging.** Anesthetise in buffered tricaine (MS-222) at the facility's IACUC-approved
   immersion dose — the specific concentration is **unknown** to me, since the Daane husbandry
   collection at protocols.io was unreachable (§2.5), and should be taken from local protocol.
   Place the fish dorsal-side-up in a shallow dish, abduct the pectoral fin with a blunt probe,
   flatten under a glass coverslip, and image perpendicular to the coverslip with a
   **telecentric or long-working-distance** lens at fixed working distance, with a stage
   micrometer in the **same focal plane** in every frame. A 4800 dpi flatbed scanner under glass
   is an acceptable low-cost substitute (§3.3 shows resolution is not limiting). Image **both
   fins** of every fish in **two independent sessions** per timepoint → 4 area estimates per fish
   per timepoint, which makes the measurement-error variance estimable rather than assumed.
   Record SL in the same frame.
6. **Timepoints.** Image at SL ≈ 12, 18, 24 and 30 mm rather than at one fixed age. The claim
   under test is allometric, so the deliverable is the **slope of log(area) on log(SL) per
   genotype**, not a single ratio. Repeated measures on the same fish also recover *n*.
7. **Tracing.** Automated threshold segmentation with manual correction, on file-renamed,
   randomised images; every image traced twice by two operators; report inter-operator and
   intra-operator agreement.
8. **Terminal validation subset.** At the end, euthanise 10 fish per genotype, dissect the
   pectoral fin, flat-mount between slides, and image. Regress the live estimate on the
   flat-mount estimate and report bias and Bland-Altman limits of agreement. **This is what
   bounds the flattening error identified in §3.3**, and without it the live measurements have an
   unquantified bias.
9. **Analysis.** ANCOVA on `log(fin area) ~ genotype + log(SL) + sex + (1 | clutch) + (1 | fish)`,
   three pre-registered contrasts against wild-type siblings, Dunnett or Bonferroni correction.
   **Disagreement with the source's method, preserved:** Daane et al. normalized length by SL as a
   ratio. Ratios to a covariate can create or hide apparent allometric differences when the
   scaling exponent is not 1; I recommend the log-log ANCOVA and recommend reporting the ratio
   alongside it so the two methods can be compared directly against the published Figure 4B.

### 3.5 The limit that cannot be engineered away

*kcnh2a*^lof/+ and *lat4a*^nr21/+ have visible fin phenotypes (§2.1). An operator tracing a fin
outline therefore cannot be blind to the trait being measured, however the files are named. The
mitigations in step 7 (automated segmentation, randomised filenames, duplicate tracing across
operators) reduce the expected bias but do not eliminate it, and the honest form of the result is
to report the automated-only segmentation as primary and the manually corrected version as a
sensitivity analysis.

### 3.6 Cost — arithmetic, from the unit prices in §2.3 and the assumptions flagged here

Tank-days for Stage 1 at *n* = 30 per genotype (200 genotyped adults):

| item | tanks × days | tank-days |
|---|---|---|
| parental stock and crosses | 6 × 220 | 1,320 |
| nursery, 0–30 dpf | 6 × 30 | 180 |
| grow-out, 30–190 dpf, 10 fish per 3.5 L | 20 × 160 | 3,200 |
| **total** | | **4,700** |

Per diem (4,520 adult-rate tank-days + 180 nursery-rate tank-days):

- WUSTL 3.5 L schedule: 4,520 × $0.24 + 180 × $0.48 = **$1,171**
- BU flat FY25 rate: 4,700 × $1.48 = **$6,956**

Consumables — **unit prices here are my assumptions, not sourced; they are the weakest numbers in
this document and should be replaced with local quotes:**

- genotyping, 200 fish × 2 loci × $3.00 per reaction (Taq, primers, gel) = **$1,200**
- assay design and validation = **$200**
- tricaine, slides, clip tools, misc = **$250**

Labour — **hours are my estimates; the rate is an assumption:**

| task | hours |
|---|---|
| genotyping 200 fish × 2 loci | 40 |
| imaging, 4 sessions × 200 fish × 2 fins | 54 |
| blind tracing, ~3,200 traces | 54 |
| researcher husbandry beyond per diem | 20 |
| analysis and write-up | 40 |
| **total** | **208 h ≈ 5.2 FTE-weeks** |

At an assumed $45/h loaded technician rate: **$9,360**.

| | low-rate facility | high-rate facility |
|---|---|---|
| non-labour | **$2,821** | **$8,606** |
| with labour | **$12,181** | **$17,966** |

**Not included, because it is unknown and I will not invent it:** line import and shipping fees
from ZIRC and from the Harris laboratory; IACUC protocol amendment cost; and the capital cost of
a calibrated stereomicroscope and camera if the facility has none. Those must be quoted locally.
I assume the imaging hardware already exists, which is true of most zebrafish facilities but is an
assumption, not a finding.

### 3.7 Weeks

| phase | weeks | cumulative |
|---|---|---|
| assay design, line verification, IACUC amendment | 3 | 3 |
| set crosses, nursery to 30 dpf | 4 | 7 |
| grow-out with imaging at SL ≈ 12/18/24/30 mm | 20 | 27 |
| terminal validation subset, genotype confirmation | 2 | 29 |
| analysis and write-up | 3 | 32 |

**32 weeks ≈ 7.4 months**, from a standing start at a facility that already holds both lines. Add
8–14 weeks if the lines must be imported, quarantined and bred up to produce single-het adults of
crossing age — which, given that *lat4a*^nr21 has no repository ID (§2.2), is the likely case.

A single-timepoint variant (one imaging session at SL ≈ 24 mm, no allometric slope) reduces this
to ~20 weeks and roughly halves the imaging and tracing labour, at the cost of abandoning the
allometric statistic that is the actual scientific object.

---

## 4. The answer

**Evidence level: `derived`.** This is a protocol and a budget computed from one full-text source
plus explicitly stated assumptions. Nothing here was observed.

> **The experiment is practical at a standard facility, and the protocol is a two-stage design.**
> Stage 0 is a 10–12 fish-per-genotype pilot whose only job is to measure the residual CV of
> normalized pectoral fin area, because that number does not exist in the literature. Stage 1,
> sized by the pilot, is **one single-pair cross of *lat4a*^nr21/+ × *kcnh2a*^lof/+, 200 genotyped
> F1 siblings giving n = 30 in each of the four Mendelian genotype classes, imaged at four
> standard lengths by calibrated flat-field stereomicroscopy (or 4800 dpi flatbed) of both
> abducted pectoral fins in two independent sessions, with a 10-per-genotype terminal
> flat-mount validation subset, analysed as log-log ANCOVA of area on SL — costing $2,800–$8,600
> in per diem and consumables, $12,200–$18,000 with labour, over 32 weeks** (40–46 weeks if the
> lines must be imported).

**Key number:** ***n* = 30 per genotype (120 measured fish, 200 genotyped)** — this is the
*n* that gives 90 % power at Bonferroni-corrected α to detect the **10.25 % area effect implied
by a 5 % length effect**, assuming residual CV = 0.10.

Two secondary results that matter as much as the headline:

1. **Measuring area rather than length buys a ~4× reduction in required *n***, because a 5 %
   length effect is a 10.25 % area effect and *n* scales as 1/effect² (§3.2). The project's top
   recommendation is better-founded than the project knew.
2. **The project's assumed 5–10 % effect is probably conservative for this genotype.** Daane et
   al. describe the double het's paired fins as "overgrown" and show them as visibly elongated in
   Figure 4A — a qualitative claim about a visible difference, which is their claim, not my
   measurement. **My inference:** an effect large enough to be visible in a published figure is
   unlikely to sit at 5 %, so the realistic *n* is nearer the 21 %-effect column of the §3.2
   table (*n* = 3–26 per genotype) than the 5 % column. The design is sized at *n* = 30 anyway,
   because the project's stated target is 5–10 % and because the pilot has not been run.

---

## 5. What this does NOT establish

- **It does not measure anything.** No fin was imaged. No fish exists for this document. Every
  numeric claim in §3 is arithmetic on stated assumptions. If this file is cited downstream as
  evidence about fin area in this genotype, that is a misreading.
- **The power table is only as good as a CV nobody has measured.** The whole §3.2 table is
  conditional on a residual CV I could not source (§2.4). At CV = 0.20 and a true 5 % area effect
  the requirement is *n* = 434 per genotype — 1,736 genotyped adults — which is the regime that
  would refute the recommendation (§6). I have no basis for excluding that regime; I only have a
  design that measures its way out of the uncertainty rather than assuming past it.
- **The fin geometry in §3.3 is invented for the purpose of the calculation.** The 4.0 × 1.5 mm
  bounding box and 75 % fill are my assumptions, chosen to be plausible at a 4 cm body length.
  They are not a published measurement — §2.4 found none. The 26 µm edge-displacement figure
  therefore has the status of an order-of-magnitude argument, not a specification.
- **The isotropy assumption behind the length→area doubling may be wrong, and if it is wrong it
  is wrong in an interesting direction.** The *lof* phenotype is fin *elongation*. If the double
  het's pectoral fin grows mostly in length and not in width, the area effect approaches the
  length effect rather than its square, the 4× *n* saving evaporates, and required *n* reverts to
  the 5–10 % columns. Worse, anisotropic growth changes fin **aspect ratio**, which matters more
  for lift than area does — so this assumption is also a scientific result waiting to be
  measured, not just a nuisance parameter.
- **It does not establish that the lines are obtainable.** *lat4a*^nr21 has no repository
  accession in the source paper. Whether the Harris laboratory still holds it, and whether it is
  cryopreserved, is **unknown** — and the same paper states that related *lof* revertant lines
  "are no longer maintained nor frozen". A failure here makes the whole protocol moot and would
  require re-deriving the allele by CRISPR, which is a different experiment at a different cost.
- **The *kcnh2a*^lof genotyping assay is not designed.** It is blocked on inversion breakpoint
  coordinates in Figure S3, which I did not read. I have named a fallback but not costed the
  possibility that breakpoint-spanning PCR proves hard.
- **The costs are a budget, not a quote.** The per diem rates are search-summary read-level from
  four institutions that disagree 11-fold (§2.3); the genotyping and labour unit prices are my
  assumptions with no source at all. Shipping, IACUC and capital costs are excluded as unknown.
  The dollar range should be read as "low five figures", not as the stated digits.
- **It does not establish detectability of the *aerodynamically relevant* quantity.** Area at a
  given SL is necessary for a lift estimate and nowhere near sufficient: span, aspect ratio,
  camber, spanwise stiffness, and the fin's ability to hold a loaded posture are all unaddressed
  here. A confirmed area increase would license no flight claim by itself.
- **It does not resolve the normalization disagreement it identifies.** I recommend log-log
  ANCOVA over Daane's ratio-to-SL. I have not shown that the two methods would give different
  answers on this data, because I have no data. Both should be reported.
- **Blinding is not achieved, only mitigated** (§3.5). Any effect in the 5 % range from
  manually corrected outlines should be treated as suspect on those grounds alone.
- **Per-genotype *n* in the published Figure 4B is unknown to me**, so I cannot say whether the
  existing length measurement was itself adequately powered, nor use it to back out a CV. That is
  the single most valuable missing datum, and it is sitting in a supplementary file I could not
  fetch (§2.1).

---

## 6. What would change the answer

**The one thing that would refute the recommendation, stated as a threshold.** If the Stage 0
pilot returns a residual CV of normalized pectoral fin area **> 0.15** *and* the point estimate of
the double-het effect is below ~15 %, then detecting the project's 5 % target needs **190–434 fish
per genotype**, i.e. **760–1,736 genotyped adults** and, at 10 fish per 3.5 L tank, **76–174
dedicated grow-out tanks held for five months**. That is beyond a single project's allocation at a
typical facility even where the facility could in principle house it, and the honest conclusion
would be that the 5 % level is not measurable this way. The project's own top recommendation would
then need re-specification — not abandonment, because the three escapes below remain.

**What would move the answer, in descending order of value per unit effort:**

1. **Retrieve Daane et al.'s Data S1 and the Figure 4B source values.** This yields the
   per-genotype *n* and the spread of pectoral-fin-length/SL in exactly these genotypes, from
   which the CV can be estimated directly. It would replace the entire conditional §3.2 table
   with one row, before any fish is bred, at zero marginal cost. It needs network access to the
   Cell Press supplementary files or an email to the corresponding author. **Do this first.**
2. **Read Figure S3 for the inversion breakpoints.** Unblocks the *kcnh2a*^lof genotyping assay,
   which is currently the only step in the protocol with no designed method.
3. **Confirm *lat4a*^nr21 (`dmh26`) availability and cryopreservation status** with the Harris
   laboratory. A negative here invalidates the schedule, not the design.
4. **Measure area and span/aspect ratio in the same images rather than area alone.** Marginal
   cost: zero, since both come from the same traced outline. If the fin grows anisotropically
   (§5), aspect ratio will show it, and aspect ratio is the quantity the project's gliding
   argument actually needs.
5. **Switch the primary statistic from a single-timepoint mean to the log-log allometric slope
   across four standard lengths.** Already in the protocol; it is the change that most increases
   power per fish, because it uses repeated measures and because the slope is the quantity the
   flying-fish comparison is about.
6. **If the CV turns out high because of fin-flattening variance rather than biological variance,
   go terminal.** Dissected flat-mounted fins remove the flattening error entirely at the cost of
   one measurement per fish and no longitudinal data. The terminal validation subset in step 8
   exists precisely to tell these two sources of variance apart; if it shows flattening dominates,
   a fully terminal single-timepoint design with *n* = 60 is likely cheaper and more sensitive
   than the longitudinal one.

---

```swarm-result
{"subproblem": "S43", "evidence": "derived",
  "answer": "Pectoral fin area in the lat4a^nr21/+; kcnh2a^lof/+ double heterozygote is measurable at a standard facility by a two-stage protocol — a 10-12 fish/genotype pilot to estimate the unpublished residual CV, then one single-pair cross yielding 200 genotyped F1 siblings (n=30 per Mendelian genotype class) imaged at four standard lengths by calibrated flat-field stereomicroscopy of both abducted fins with a terminal flat-mount validation subset — for $12,200-$18,000 including labour over 32 weeks, and measuring area rather than length cuts the required n about four-fold because a 5% length effect is a 10.25% area effect.",
  "key_number": "n = 30 fish per genotype (120 measured, 200 genotyped) for 90% power at Bonferroni-corrected alpha=0.0167 against a 10.25% area effect, assuming residual CV = 0.10",
  "blocked_on": "The residual coefficient of variation of adult zebrafish pectoral fin area is unpublished (negative search: 3 Europe PMC queries + 1 web search, 2026-11-04; zero occurrences of 'area' in the Daane et al. 2021 full text), so required n spans 3-434 per genotype until the pilot runs; Daane et al. Data S1, the Figure 4B per-genotype n and the Figure S3 kcnh2a inversion breakpoint coordinates could not be retrieved (zfin.org HTTP 503; franklin.zfin.org, crick.zfin.org, repository.library.noaa.gov, zebrafishfacility.wustl.edu and protocols.io failed DNS from this session); lat4a^nr21 (dmh26) has no repository accession and its current availability is unknown."}
```
