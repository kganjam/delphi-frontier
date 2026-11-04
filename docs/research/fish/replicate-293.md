# Replication 293 — fitted voltage decay length in zebrafish fin tissue

**Task:** independently re-derive the fitted voltage decay length in zebrafish fin tissue, and
the factors separating it from the claimed 0.1–120 mm fin-ray range, without reading the
original deriver's working.

**Independence statement.** The harvest referenced as the input location
(`harvest:kcnh2a-gradient-decay-aticbh`) is **not present in this repository**. I searched the
full tree for `aticbh`, `kcnh2a`, `kcnk5b`, `293`, `zebrafish`, `danio` and `decay length`
(`grep -ril`, excluding `.git`). The only hits were two unrelated files
(`findings/gemini-triage-267-problems.json`, `findings/gemini-third-assessor-calibration.json`),
which concern a different problem set (267) and which I did not read for claim-293 content.
No prior derivation of this claim exists in the repo, so nothing was available to contaminate
this one. I did have the claim's own headline figures from the task prompt (`~0.19 mm`,
`186±39 / 197±22 µm`, `factor of 3`, `~26x`, `~632x`); I treat those as the *recorded value* for
the comparison section, and I derived my own numbers from primary sources before comparing.

---

## 1. My value

**Fitted characteristic (decay) length of the voltage gradient in zebrafish fin tissue:**

> **λ = 0.19 mm — specifically 0.191 ± 0.021 mm (95% CI), inverse-variance weighted across the
> two epithelial layers.** Unweighted mean 0.1965 mm. The two layer values individually are
> 0.187 mm and 0.206 mm, with fit CIs spanning ~0.16–0.25 mm.

This is a **fitted model parameter reported by the authors** (an exponential fit to a measured
fluorescence profile), **not a directly observed voltage**. No one measured millivolts per
micron; the quantity is a length constant extracted from a normalized fluorescence drop.

**Critically — and this is a scope limit, not a caveat:** this length describes an
**injury-induced transient**, not a standing gradient. The authors state the potential "relaxes
to a quasi–steady state over **100 ms**" after wounding, and the fitted quantity is explicitly a
*change from the uncut baseline* (−ΔF/F_uncut). It is therefore not a measurement of the
standing positional gradient the 0.1–120 mm claim is about. The two quantities differ in kind,
not merely in scale.

---

## 2. Inputs, with sources and read-levels

### 2.1 Primary source for the decay length

Liu J, Nerli E, Duclut C, Vishen AS, Berbee N, Kaufmann S, Pérez-Verdugo C, Arrenberg AB,
Jülicher F, Mateus R. **"Injury-induced electrochemical coupling triggers organ growth."**
*Science Advances* **12**(6), published 2026-02-06. doi:10.1126/sciadv.aec0687;
PMID 41637501; PMC12871474. **Read-level: full-text** (I downloaded the PMC article, stripped
tags locally, and grepped the raw text myself rather than relying on a summarizer; citation
metadata verified against the Crossref API).

| Quantity | Value | Location |
|---|---|---|
| Characteristic length *l*, apical epithelium | **206 ± 48 µm** | main text; Fig. 1K; fig. S4 C–F |
| Characteristic length *l*, basal epithelium | **187 ± 24 µm** | same |
| Meaning of ± | "95% confidence interval (CI) of parameter fits" | Fig. 1K legend |
| Λ, epithelial ion permeability | 0.05 s⁻¹ | main text, note S3 |
| Aqueous D (reference values) | Na⁺ 1334, K⁺ 1957, Cl⁻ 2032 µm²/s | main text |
| Stage / tissue | 2 dpf larval caudal **finfold** epithelium, UV-laser line wound | Methods |
| Fit | single exponential, nonlinear least squares (MATLAB) | Methods |
| Fit window | cells **30–150 µm** from cut (0–30 µm discarded as laser-damaged) | Methods |

Verbatim: *"we found that the spatial gradient of V_mem depolarization displays an exponential
profile with comparable characteristic lengths l for both epithelial layers (apical: 206 ± 48 μm,
basal: 187 ± 24 μm; Fig. 1K and fig. S4, C to F)."*

**This is the only fitted voltage decay length in any zebrafish fin tissue.** I verified this
within the paper (`characteristic length` occurs 4×, all referring to the same WT fit; no decay
length is fitted in any mutant) and across the literature (§2.4).

### 2.2 Adult caudal fin ray length

Cass AN, Kidd M, … McMenamin SK. **"Caudal fin shape imprinted during late zebrafish
embryogenesis is re-patterned by the Sonic hedgehog pathway."** *PLoS Biology* (2025).
doi:10.1371/journal.pbio.3003336. **Read-level: full-text, plus the authors' published raw-data
file (S1 Data, XLSX), downloaded and parsed directly.**

Adult WT, intact fins, pre-amputation, n = 10, 28–30 mm standard length; rays traced with
segmented lines in FIJI (= the proximodistal lepidotrich length):

| Ray | Mean | SD | Range |
|---|---|---|---|
| Peripheral (2nd dorsal, **longest**) | **7.55 mm** | 0.37 | 6.93–8.28 |
| Central (9th dorsal, **shortest**) | **5.40 mm** | 0.34 | 4.92–6.00 |

The per-fish mm values are the authors'; the mean/SD/range are **computed from their published
values**, not read off a figure. Scales at ~0.26 × SL across a 14 dpf → adult series in the same
file, which is an internal consistency check.

**There is no single "adult Danio ray length."** Within one fin, ray length varies ~35% from
peripheral to central. Cross-source whole-caudal-fin values for short-finned wild types span
**5.6–9.6 mm** (Wakamatsu et al. 2019 *Sci Rep* 9:16307, PMC6841939, full-text: AB 6.1 ± 0.3,
TU 5.6 ± 0.3, WIK 6.5 ± 0.3 mm — note this paper **contradicts itself**, its Fig. 5 legend saying
"~9 mm" and its Discussion "4~9 mm"; I preserve the disagreement rather than averaging. Plaut
2000 *J Exp Biol* 203:813, **abstract only / could-not-access full text**, gives 7.1–9.6 mm for
wild type *as quoted inside* Wakamatsu — second-hand, not verified at source).

Papers that report **no absolute mm** fin/ray length (checked, full-text): Perathoner et al. 2014,
Daane et al. 2018, Iovine & Johnson 2000, Cardeira et al. 2016.

### 2.3 The 0.1–120 mm range and the 120 mm design target

**Read-level: could-not-access / provenance unknown.** The figures `0.1 mm`, `120 mm` and the
"0.1–120 mm ray range" are given in the task prompt. I could not locate their primary provenance:
they do not appear in this repository (`grep` for `120`, `kcnk5b`, `kcnh2a`, `bioelectric`,
`longfin`, `fin ray` over `seeds/frontier-problems.json` and `seeds/frontier-data.json` returned
**0 hits each**), and the referenced harvest is absent. I therefore take 0.1 mm and 120 mm as
**given by the claim** and do not vouch for them. The 120 mm figure is used below purely as the
stated design target.

### 2.4 Negative search — has a standing gradient ever been measured?

**Finding: no.** No published, fitted, steady-state, *uninjured* spatial voltage or
transepithelial-potential profile along the proximodistal axis of a zebrafish fin ray exists, in
wild type or in *kcnk5b*/*kcnh2a* mutants.

What *does* exist, none of which is a standing gradient:

1. **Perathoner et al. 2014, Supplementary Fig. S4 only** (full-text) — the *only* voltage
   measurement in a *kcnk5b* mutant fin. Uncalibrated DiSBAC₂(3) dye intensity, reduced to **one
   scalar per fin** ("average pixel intensity of the fin in maximum intensity projections"), which
   by construction destroys spatial information. No mV values for fin tissue anywhere in the
   paper; spatial structure described only in prose ("discrete regions", "across the fin"). All
   quantitative Vmem in that paper is two-electrode voltage clamp in *Xenopus* oocytes.
2. **Jiang et al. 2024** *PLoS Biol* (full-text) — a *temporal* time course (32–56 hpf) of dye
   intensity in larval pectoral fin **buds**; Methods state the four sampled locations (distal,
   anterior, posterior, proximal) were **averaged** into one data point, so the design cannot
   report a proximodistal gradient.
3. **Liu et al. 2026** (§2.1) — the only rigorous fitted spatial voltage gradient, but
   injury-induced, millisecond-scale, 2 dpf larval finfold epithelium, measured as a change from
   the uncut baseline, and **not performed in a kcnh2a or kcnk5b mutant** (those mutants are used
   there for Ca²⁺ and proliferation readouts only).
4. **Le Bleu et al. 2025** *Development* (full-text) — Ca²⁺ imaging plus in vitro KCl
   depolarization of isolated fin fibroblasts; grep for `mV` returns **0 matches**.

Grep for voltage-dye / microelectrode / transepithelial / vibrating-probe terms returns **0
matches** in the full texts of Daane et al. 2018, Stewart et al. 2021, Lanni et al. 2019, Daane
et al. 2021 and Silic et al. 2020.

Three independent in-print confirmations from groups best placed to know:

- Silic et al. 2023 *Cells* 12:1148 (full-text): *"**Although direct evidence of bioelectricity in
  zebrafish fin development is still lacking**, indirect evidence came from several zebrafish fin
  mutants…"*
- Stewart et al. 2021 (full-text): *"**Key future steps include characterizing membrane potentials
  and putative depolarizing signals**…"*
- Liu et al. 2026 (full-text): *"Deciphering the electrochemical dynamics of V_mem and ion fluxes
  in the adult mesenchymal blastema … **is an exciting frontier to be explored.**"*

**Scope of the negative search.** Europe PMC REST (`search` + `fullTextXML`), all years, no date
filter, run 2026-11-04: voltage-dye terms (`DiBAC4(3)`, `DiSBAC2(3)`, voltage-sensitive dye) ×
zebrafish fin, 30 hits reviewed; GEVI terms (`Voltron`, `ASAP1`, `ArcLight`) × zebrafish fin, 15
hits; `vibrating probe`/`microelectrode`/`transepithelial potential` × zebrafish fin, 107 hits,
first 30 reviewed; `membrane potential`/`Vmem`/`resting potential` × caudal fin/fin ray/fin
regeneration, 137 hits, first 30 reviewed; `voltage gradient`/`potential gradient`/`electric
field` × zebrafish fin × measure*/imaging, 106 hits, first 30 reviewed; gene sweeps `kcnk5b` (57,
all titles), `kcnh2a` (54, all), `kcnh2a AND fin` (31, all); plus bioRxiv API and two WebSearch
passes. **Not covered:** Google Scholar, Web of Science, Scopus, bioRxiv full-text search, theses,
non-Europe-PMC conference abstracts, non-English literature, and **supplementary files of any
paper** — so a voltage profile buried in an unindexed supplement is not excluded.

### 2.5 What the primary authors claim about mechanism

**Authors who deny altering positional information — confirmed:**

- **Stewart et al. 2021**, *Development* 148:dev199384, doi:10.1242/dev.199384, PMC8217709
  (*kcnh2a* / *longfin*). **Read-level: full-text.** Abstract, verbatim: *"**We conclude ion
  signaling within the growth-determining mesenchyme lineage controls fin size by tuning outgrowth
  periods rather than altering positional information or cell-level growth potency.**"* Discussion,
  verbatim: *"**However, lof^t2 does not seem to change positional information established at the
  outset of fin regeneration** because inhibiting ectopic Kcnh2a during only the late outgrowth
  phase restores a normal sized fin … **elevated Kcnh2a and calcineurin inhibition appear to
  disrupt growth deceleration mechanisms tuned to interpret, rather than set, positional
  information.**"*
- **Daane et al. 2018**, *Sci Rep* 8:10391, PMC6039437. **Read-level: full-text.** Verbatim:
  *"**Thus, Kcnk5b/calcineurin signaling does not lead to lasting alterations in positional
  identity, but rather regulates rate of growth leading to enhanced fin proportions.**"*
- **Le Bleu et al. 2025**, *Development* dev204739, PMC13078715. **Read-level: full-text.**
  Verbatim: *"**bioelectricity does not produce a growth-determining pre-pattern … and therefore
  does not provide positional information itself.**"*

**But one primary author claims the opposite, and the claim's blanket attribution is wrong:**

- **Perathoner et al. 2014**, *PLoS Genet* 10:e1004080, PMC3894163 (*kcnk5b* / *alf*).
  **Read-level: full-text.** Discussion §"Ionic currents and positional information", verbatim:
  *"**We favor a model for size regulation in which modulation of ionic current by K⁺ channels
  within the organ shifts positional information, thereby setting a different register of size
  during development.**"*

  My inference, flagged as mine: the voltage gradient Perathoner invoke in support is from
  *amphibian embryo* literature (Shi & Borgens 1995; Metcalf et al. 1994), **not** a fin
  measurement — consistent with §2.4. The authors themselves concede *"the underlying mechanism of
  signaling from electrical fields is largely unknown."* Note also that it is a stated
  *preference* ("We favor a model…"), not a demonstrated result.

**Disagreements preserved, not averaged:**

1. **Positional information is contested, and the same lab changed position.** Harris is senior
   author on both Perathoner 2014 ("shifts positional information") and Daane 2018 ("does not lead
   to lasting alterations in positional identity"). Stewart 2021 (Stankunas lab) is the flat
   denial. Upstream, **Kujawski et al. 2014** *Dev Cell* 28:573 (**abstract-level**) made the
   positional claim the later papers argue against (*"a molecular switch between
   position-associated isometric and allometric growth programs"*), as did **Cao et al. 2021**
   *PNAS* 118:e2009539118 (**abstract-level**).
2. **Rate vs duration differs by gene.** For *kcnk5b*/*alf*, Perathoner report an increased growth
   **rate** (allometric coefficient k ≈ 2 vs wild-type 1.29). For *kcnh2a*/*lof^t2*, Stewart report
   **indistinguishable maximal growth rate** with a slower-decaying rate, i.e. a longer outgrowth
   **period**. So "outgrowth-duration tuning" is accurate for *kcnh2a* but **not** for *kcnk5b*.
3. **The sign of the voltage change is contested.** Perathoner's main text models
   hyperpolarization (from oocyte recordings) while their own Fig. S4 found *alf* fins
   **depolarized**; Jiang et al. 2024 find depolarization drives growth; Aramaki & Kondo
   (bioRxiv 2024.03.27.587111, v1 full-text / v2 abstract, **not peer-reviewed**) find
   optogenetic depolarization *decreases* fin size; and Liu et al. 2026 flag the conflict
   themselves (*"This apparent discrepancy with our larval fin findings could be due to
   differences in the cell types that respond to injury"*).

---

## 3. Arithmetic in full

### 3.1 Combining the two layers

```
apical : 206 ± 48 µm  (95% CI of fit)
basal  : 187 ± 24 µm  (95% CI of fit)

Unweighted mean   = (206 + 187) / 2 = 196.5 µm = 0.1965 mm

Inverse-variance weighted (SE = CI / 1.96):
  SE_apical = 48 / 1.96 = 24.490 µm
  SE_basal  = 24 / 1.96 = 12.245 µm
  w_a = 1 / 24.490² = 0.0016674
  w_b = 1 / 12.245² = 0.0066694
  numerator   = 206 × 0.0016674 + 187 × 0.0066694 = 1.590663
  denominator = 0.0016674 + 0.0066694            = 0.0083368
  weighted mean = 1.590663 / 0.0083368 = 190.80 µm
  SE = sqrt(1 / 0.0083368) = 10.95 µm  →  95% CI = ±21.5 µm

=> λ = 190.8 ± 21.5 µm = 0.191 ± 0.021 mm
```

Caveat (mine): apical and basal are two layers of the *same* embryos, not independent replicates
of one quantity, so the inverse-variance combination understates the true uncertainty. The honest
statement is **~0.19–0.20 mm central, fit CIs spanning ~0.16–0.25 mm.**

### 3.2 Independent check of the cable-theory relation

The paper prints the relation as `l = D/Λ`. **That is dimensionally wrong**: µm²/s ÷ s⁻¹ = µm², an
area, not a length. The dimensionally correct form — and the one the claim states — is
**λ = sqrt(D/Λ)**. I verified this is the intended relation by reproducing the authors' own
parameter from their own numbers:

```
λ = sqrt(D / Λ),  Λ = 0.05 s⁻¹
  D(Na⁺)            = 1334 µm²/s → sqrt(1334/0.05) = sqrt(26680) = 163.3 µm
  D(mean Na⁺,Cl⁻)   = 1683 µm²/s → sqrt(1683/0.05) = sqrt(33660) = 183.5 µm
  D(K⁺)             = 1957 µm²/s → sqrt(1957/0.05) = sqrt(39140) = 197.8 µm
  D(Cl⁻)            = 2032 µm²/s → sqrt(2032/0.05) = sqrt(40640) = 201.6 µm

Model-predicted range 163–202 µm brackets the fitted 187–206 µm. ✓

Inverting, Λ = D/λ² with D = 1683 µm²/s:
  λ = 190.8 µm → Λ = 0.0462 s⁻¹
  λ = 206   µm → Λ = 0.0397 s⁻¹
  λ = 187   µm → Λ = 0.0481 s⁻¹
versus the authors' stated Λ = 0.05 s⁻¹. ✓
```

This is a **calculation**, not an observation. It confirms the square-root form is the real
relation (the printed `l = D/Λ` is a typesetting/notation error) and that the paper is internally
consistent.

### 3.3 The three comparisons

```
λ = 0.1908 mm

A) vs the 0.1 mm lower end of the claimed range
   0.1908 / 0.1 = 1.91×        → within a factor of 2, hence within a factor of 3 ✓

B) vs an adult Danio caudal fin ray
   central ray    5.40 / 0.1908 = 28.3×   (range over individuals 25.8–31.4×)
   peripheral ray 7.55 / 0.1908 = 39.6×   (range over individuals 36.3–43.4×)
   full span across ray identity and individuals: 26×–43×
   ray length required to give exactly 26×: 26 × 0.1908 = 4.96 mm

C) vs the 120 mm design target
   120 / 0.1908 = 628.9×
   (120 / 0.19 = 631.6× ; 120 / 0.1965 = 610.7×)
   95% CI span: 565×–709×
   log10(628.9) = 2.80 → 2.8 orders of magnitude
```

---

## 4. Comparison with the recorded value

The harvest record itself is absent from the repo, so I compare against the claim text quoted in
the task prompt.

| Element | Recorded | Mine | Verdict |
|---|---|---|---|
| Decay length | ~0.19 mm | **0.191 ± 0.021 mm** | **AGREE** |
| Input values | apical 186±39, basal 197±22 µm | apical **206±48**, basal **187±24** µm | **DISAGREE** (see below) |
| Source status | "Liu et al. 2025 preprint" | peer-reviewed *Sci Adv* 12(6), 2026-02-06 | **superseded** |
| `λ = sqrt(D/Λ)` | as stated | confirmed, and more correct than the paper's own `l = D/Λ` | **AGREE** |
| Within factor 3 of 0.1 mm | yes | 1.91× — within factor 2 | **AGREE** |
| vs adult ray | ~26× | **28×–40×** (26–43× full span) | **DISAGREE** (understated) |
| vs 120 mm | ~632× | **629×** | **AGREE** |
| No standing gradient ever measured | yes | confirmed, scope in §2.4 | **AGREE** |
| Authors deny positional information | "the primary authors" | true of Stewart 2021 & Daane 2018; **false of Perathoner 2014** | **PARTLY DISAGREE** |
| Outgrowth-duration tuning | yes | true for *kcnh2a*; *kcnk5b* is a **rate** change (k≈2) | **PARTLY DISAGREE** |

**Overall: AGREE on the headline value and on the central negative result.** My independent
derivation reproduces ~0.19 mm, confirms it is the only fitted voltage decay length in zebrafish
fin tissue, and confirms that no standing kcnh2a/kcnk5b-driven gradient has ever been measured.
The claim's core conclusion — that the sole available length scale is ~2.8 orders of magnitude
short of a 120 mm design target, and that the enabling measurement does not exist — stands, and
my work strengthens rather than weakens it.

Four corrections the record should carry:

1. **The input numbers are superseded.** The claim's apical 186±39 / basal 197±22 µm do not appear
   in the peer-reviewed paper, which gives apical 206±48 / basal 187±24 µm. The claim's apical and
   basal are also **inverted in rank** relative to the published values (claim has apical < basal;
   published has apical > basal). The bioRxiv API confirms only **one** preprint version existed
   (v1, 2025-04-08, now published as 10.1126/sciadv.aec0687), so this is a peer-review revision
   rather than a mis-citation of a v2. **I could not verify v1's exact numbers: bioRxiv is
   Cloudflare-blocked (error 1015) from this session via both WebFetch and curl across four URL
   forms, and Europe PMC holds the record (PPR1001145) with no open full text.** Read-level for
   preprint v1: **could-not-access.** Fortunately the headline conclusion is insensitive to this —
   both versions give ~0.19–0.20 mm.
2. **"~26× short of an adult ray" is understated.** 26× requires a 4.96 mm ray, which is the
   *shortest central ray of the smallest adult* in the only dataset that reports absolute ray
   lengths. Against the *longest* ray it is ~40×. The defensible statement is **28×–40×**,
   depending on ray identity.
3. **"The primary authors … explicitly deny changing positional information" is true for
   *kcnh2a*, not for *kcnk5b*.** Perathoner et al. 2014 explicitly *favor* a positional-information
   model for *kcnk5b*. The claim lumps the two genes; the literature does not. (This cuts
   **against** the claim's framing but does not rescue the feasibility case, since Perathoner's
   positional model rests on amphibian-embryo voltage gradients and an uncalibrated,
   spatially-averaged dye measurement — not on a measured fin gradient.)
4. **A methodological caveat I did not find flagged anywhere.** The exponential was fitted only to
   cells **30–150 µm** from the cut, yet the fitted decay length is **187–206 µm** — longer than
   the spatial window of the data it was fitted to. The decay length is therefore an extrapolation
   beyond its own fitting range and is weakly constrained from above. (My inference from their
   Methods, not an author statement.) This makes ~0.19 mm a *soft* upper-bounded estimate, and it
   is the single biggest reason not to treat the third significant figure as meaningful.

**The strongest point in the claim's favour, which the claim understates:** the ~0.19 mm length is
an **injury-induced transient** in 2 dpf larval finfold epithelium that relaxes over 100 ms, and
is defined as a change from the uncut baseline. A standing positional gradient is a different kind
of object. So the mismatch is not merely "0.19 mm vs 120 mm"; there is **no measured standing
gradient to scale up at all**, and the authors of the one rigorous measurement say so in print.
Liu et al. further report that their perturbations *"did not influence developmental proliferation
or length of uninjured larval fins"* — i.e. in uninjured fins, no effect.

```swarm-replication
{"claim_id": 293, "my_value": "0.191 +/- 0.021 mm (95% CI; apical 206+/-48 um, basal 187+/-24 um, peer-reviewed Sci Adv 2026)", "agrees": true,
  "note": "Independently reproduced ~0.19 mm and confirmed it is the only fitted voltage decay length in fin tissue and that no standing kcnh2a/kcnk5b gradient has ever been measured; but the claim's input values are superseded by the peer-reviewed version (206+/-48/187+/-24, apical-basal rank inverted), the adult-ray factor is 28-40x rather than 26x, and 'authors deny positional information' holds for kcnh2a (Stewart 2021) but not kcnk5b (Perathoner 2014 explicitly favours a positional-information model)."}
```
