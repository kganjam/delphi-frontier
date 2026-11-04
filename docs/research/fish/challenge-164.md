# Challenge 164 — adversarial review of [S22-D-D] "pectoral overgrowth falls short by ~1.5–2x"

Reviewer: adversarial pass, 2026-11-04. Claim under review is not mine.
Source of claim: `harvest:s22-d-sensitive-input-pwechp`. Recorded evidence level: unknown.

## The claim, restated

1. Wild-type zebrafish pectoral fin length / SL ≈ 0.21 (range 0.17–0.26), obtained by
   figure-reading Daane et al. 2018 *Sci Rep* Fig 1A and **doubling** a "regrowth target"
   of 0.104 SL at ~50% resection.
2. Flying-fish pectoral proportion target = 0.65–0.77 SL.
3. Therefore ~2.5–4.4x pectoral overgrowth is required.
4. The "only measured dominant bioelectric long-fin allele" (`kcnk5b` *alf*/+) gives ~1.7–2x
   (stated as 1.74x).
5. Therefore the Daane et al. "phenocopy" of flying-fish proportion most likely falls short by
   ~1.5–2x in pectoral length/SL.

Verdict recorded by the author: *strengthens*.

## 1. Arithmetic, redone independently from the stated inputs

All of the following are **my calculations from the claim's own stated numbers**, not observations.

Required fold `R = target / wild-type`:

| wild-type input | R at target 0.65 | R at target 0.77 |
|---|---|---|
| 0.21 (central) | 3.10 | 3.67 |
| 0.26 (stated max) | 2.50 | 2.96 |
| 0.17 (stated min) | 3.82 | 4.53 |

- The doubling reproduces: 0.104 × 2 = 0.208 → 0.21. ✓
- The claim's stated range "~2.5–4.4x" is **not** reproducible from the stated endpoints: the
  extreme corner is 0.77 / 0.17 = **4.53x**, not 4.4x (4.4x corresponds to a wild-type of 0.175).
  Trivial in consequence, but it means the published interval is not the interval its own inputs
  generate.

Implied shortfall `S = R / achieved`:

- central wild-type only: 3.10/2.00 = 1.55 up to 3.67/1.74 = **2.11** → 1.55–2.11x.
  The claim's "~1.5–2x" is right at the bottom of this and clips the top.
- propagating the claim's *full* stated wild-type range: 2.50/2.00 = **1.25** up to
  4.53/1.74 = **2.60** → **1.25–2.60x**.

So the headline "~1.5–2x" is the central band of a quantity whose own stated uncertainty runs
1.25–2.6x. At the permissive corner the gap (1.25x) is no larger than the error a size-confounded
single-figure pixel read plausibly carries, i.e. the *existence* of a shortfall is not comfortably
established at that corner, only at the centre. The author's own parenthetical
("calculated on a proxy, size-confounded, not observed") is honest about the kind of number but
the interval presented understates the spread the inputs imply.

## 2. The proxy — and it is the wrong one

Two proxies are stacked, and the second is a substantive defect.

**Proxy A (fold overgrowth): `kcnk5b` *alf*/+ standing in for the actual phenocopy genotype.**
The "Daane et al. phenocopy" of flying-fish bauplan is Daane et al. 2021 *Curr Biol*
31(22):5052–5061.e8, "Modulation of bioelectric cues in the evolution of flying fishes"
(read-level: **full text**, HTML body, via PMC9172250). That paper's phenocopy is
`lat4a`<sup>nr21</sup>/+ ; `kcnh2a`<sup>lof</sup>/+ **trans-heterozygotes** — an L-type amino-acid
transporter crossed to the dominant *longfin* potassium-channel allele — not *alf*/`kcnk5b`.
The paper states the medial fins of the trans-heterozygote are wild-type-sized while "the paired
fins are overgrown", and normalizes pectoral fin length by SL in Fig 4.

So the right quantity exists, is measured, is in the very paper being judged, and was not used:
**pectoral fin length / SL for `nr21`/`lof`, Daane et al. 2021 Fig 4B.** I could not read it
(see read-levels below), so I cannot say whether it reaches 0.65 SL. Substituting a different
allele's fold change when the target genotype's own normalized measurement is published is a
proxy that was not necessary.

**Proxy A′ (the 1.74x itself is unverified).** I searched for the value 1.74 (and 1.7x / 74%) for
*alf*/+ pectoral overgrowth. Perathoner et al. 2014 *PLoS Genet* (read-level: **full text**, via
PMC3894163) reports **no** pectoral fold-change in its text at all; its only quantitative fin
numbers are **caudal** allometric coefficients (wild type k = 1.29, R² = 0.92; *alf*/+ k "near 2",
R² = 0.95, p < 0.001). Daane et al. 2018 (read-level: **full text**, via PMC6039437) likewise
reports no fin-length/SL ratio and no *alf* fold-change in text. Scope of that negative: full text
of both papers plus four targeted web searches; I did not read either paper's figure images or
supplementary tables. So 1.74x is most likely a second figure-read, presented in the KEY line
without that label, and its provenance is `unknown` to me.

**Proxy B (the figure of merit).** Pectoral fin *length*/SL stands in for what a flying-fish
bauplan actually is: planform area, span and aspect ratio of a "wing" with elongated, broadened
rays, plus the hypocercal caudal. Daane et al. 2021 themselves report the double mutant's caudal
is hypocercal — a bauplan match on a second axis the length-ratio test cannot see. A length-only
test can fail while the morphological claim the authors made (fin *proportion* and bauplan)
stands.

## 3. The hidden assumption that carries the result: the ×2

The entire central value is `0.104 × 2`. Relax it and the claim moves by a factor of two.

Daane et al. 2018 Fig 1 legend (read-level: **full text of the legend, relayed**; the figure
*image* is **could-not-access**, see below) describes Fig 1A as regrowth of pectoral fins cut to
~50% of pre-cut length, normalized to SL, with **dashed lines marking the pre-cut length**.
A "regrowth target" in that panel is, by the legend's own wording, the **dashed pre-cut line** —
i.e. the *full* wild-type fin length, not the remnant. On that reading, wild-type pectoral/SL
≈ **0.104**, the doubling is a double-count, and:

- R = 0.65/0.104 = 6.25 to 0.77/0.104 = 7.40 → **6.3–7.4x** required;
- S = 6.25/2.00 = 3.1 to 7.40/1.74 = 4.3 → **~3–4x** shortfall.

On the author's reading (0.104 = post-resection remnant), R ≈ 3.1–3.7x and S ≈ 1.6–2.1x.

I cannot adjudicate between the two from the figure, and I will not average them. Two independent
considerations point in opposite directions:

- **For the author's doubling:** a congeneric taxonomic measurement. *Danio aesculapii* (sister
  species to *D. rerio*; Kullander & Fang 2009) reports pectoral-fin length as **24.0–26.8 % SL,
  mean 25.4, n = 9** (read-level: **search-summary** of the Zootaxa morphometric table only —
  `zenodo.org` and `www.mapress.com` both fail to resolve under this session's network policy, so
  I could not open the table itself). A Danio pectoral fin at 0.10 SL would be far outside that;
  at 0.21 SL it is low but on the same scale. This favours the doubling.
- **Against it:** the legend wording above, and the fact that caliper measurement of the fin
  blade in ventral view (Daane's method: "handheld calipers", length normalized to SL) need not
  use the taxonomic landmark (fin origin → tip of longest ray), so the two numbers may not be
  commensurable in either direction.

**Second relaxed assumption: that ~1.7–2x is a ceiling.** It is a snapshot, not a limit.
*lof*/`kcnh2a` overgrowth arises from a **prolonged outgrowth period** (Stewart et al. 2021
*Development* 148(11); read-level: **search-summary** + abstract), so the fold change depends on
the SL and age at measurement; Daane et al. 2021 states `kcnh2a`<sup>lof</sup> **homozygotes have
larger fins** than heterozygotes. A ratio measured at one body size in one allelic dose does not
bound what the pathway can do, and the claim's "needs 2.5–4.4x, gets 1.7–2x" treats it as if it
did.

**Third: multiplicativity.** The claim composes a ratio-of-ratios as if allele effect and target
proportion were commensurable scalars, while both are allometric functions of SL
(Daane 2021 Fig 1B: flying-fish pectoral length rises steeply with body size, halfbeaks only
subtly). The author flags "size-confounded"; the arithmetic nonetheless proceeds as if it were not.

## 4. Is the evidence level honest?

Mostly, with two defects.

- **Honest:** the claim says "calculated on a proxy, size-confounded, not observed" and labels the
  wild-type value "figure-read and inferred". That is the right disclosure and it is in the
  sentence.
- **Defect 1:** "~0.21 (0.17–0.26)" presents a derived number with a dispersion that *reads* as
  measurement spread. There is no sample behind it — a single pixel read, doubled, with an assumed
  tolerance. It should read "0.21, derived; tolerance assumed, n = 1 figure read".
- **Defect 2 (factual, not just labelling):** "the **only** measured dominant bioelectric long-fin
  allele". This is false. `kcnh2a`<sup>lof</sup> (*longfin*) is a dominant allele of an
  *ether-a-go-go*-related voltage-gated K⁺ channel, acting cell-autonomously in intra-ray
  mesenchyme (Stewart et al. 2021, read-level: abstract/search-summary; corroborated in
  Daane et al. 2021 full text). Daane et al. 2021 measures its fins normalized to SL. A dominant
  modifier of *lof* (*schleier*) also exists in the literature (read-level: **search-summary**
  only; I am not asserting its gene). The word "only" is what licenses using *alf*/+ as the
  ceiling, so this error is load-bearing, not cosmetic.

## 5. Regime / counter-example the author missed

- **The target paper itself.** Daane et al. 2021 does not, in its text, assert a *quantitative*
  pectoral-length/SL match. Its claims are "remarkably similar", fin *proportion*, and
  "sufficient to phenocopy this key innovation and organismal bauplan", supported by an
  allometric comparison (Fig 1B) and SL-normalized mutant measurements (Fig 4). Refuting a
  numerical proportion match attacks something stronger than the published text claims — though
  a reader could fairly take "phenocopies the observed fin proportions of flying fishes" as
  quantitative, so this is a partial, not total, strawman.
- **Allelic dose and rearing duration** (above) — a regime where the 1.7–2x figure does not bind.
- **Domesticated long-fin strains** (*Betta splendens*, veiltail goldfish) exceed 2x wild-type fin
  proportion by selection on polygenic backgrounds. Weak as a counter-example here, because the
  effect is mostly caudal/median and not a single dominant bioelectric allele — but it does
  undercut any general "fins cannot get that much longer" intuition.

## Read-levels (all sources used)

| Source | Read-level |
|---|---|
| Daane et al. 2018 *Sci Rep* 8:10391 (PMC6039437) | full text (HTML body + Fig 1 legend, relayed); **figure images could-not-access** |
| Daane et al. 2021 *Curr Biol* 31:5052 (PMC9172250) | full text (HTML body, first 100k chars); **Fig 1B / Fig 4B plot values and Data S1 could-not-access** |
| Perathoner et al. 2014 *PLoS Genet* (PMC3894163) | full text (first 100k chars) |
| Stewart et al. 2021 *Development* 148(11) | abstract / search-summary |
| *Danio aesculapii* morphometrics (Kullander & Fang 2009, Zootaxa 2164) | search-summary of table only |
| *Cheilopogon* spp. pectoral ratios (Plazi treatments) | search-summary |
| *schleier* dominant *lof* modifier (PMC7235970) | search-summary (gene not asserted) |

**Access failures, stated for scope:** `cdn.ncbi.nlm.nih.gov` and `media.springernature.com` return
403 at the session's egress proxy, so no figure image (Daane 2018 Fig 1A, Daane 2021 Fig 4B) could
be pixel-calibrated by me; `zenodo.org` and `www.mapress.com` do not resolve under this session's
network policy, so the *Danio aesculapii* table could not be opened directly; Europe PMC reports
PMC9172250 "not open access", so Data S1 (the flying-fish measurements) is unavailable. Those
four hosts would need to be allowed in the session's network settings to close the two
load-bearing gaps. **I therefore could not independently re-read the claim's single key input.**

## Independent check of the inputs I *could* test

- **Flying-fish target.** *Cheilopogon* taxonomic treatments give pectoral fin length as
  **1.35–1.7 in SL** → **0.59–0.74 SL** by my conversion (read-level: search-summary). The claim's
  0.65–0.77 is slightly high at the top end but broadly corroborated. Using 0.59–0.74 *lowers* R.
- **Wild-type anchor.** Congeneric 0.240–0.268 SL (see caveats). Substituting it:
  R = 0.65/0.268 = 2.43 to 0.77/0.240 = 3.21 → **2.4–3.2x**;
  S = 2.43/2.00 = 1.21 to 3.21/1.74 = **1.84** → **~1.2–1.8x** shortfall. Direction preserved,
  magnitude below the claim's band.

## Verdict

**WEAKENED**, not refuted.

What survives: the *direction*. On every branch I could test — the author's doubled read
(S ≈ 1.6–2.1x), the undoubled legend reading (S ≈ 3–4x), and the congeneric anchor
(S ≈ 1.2–1.8x) — a length-ratio gap remains between an *alf*/+-scale fold change and a
flying-fish pectoral proportion. That robustness-across-branches is a real result and I could not
break it.

What does not survive:

1. The magnitude. The central value rests entirely on one unreadable figure axis with two
   defensible interpretations a factor of 2 apart, and the stated input ranges admit
   S = 1.25–2.6x rather than "~1.5–2x". Supportable range across branches: **S ≈ 1.2–4.3x**.
2. "The only measured dominant bioelectric long-fin allele" is **false** (`kcnh2a`<sup>lof</sup>),
   and it is the premise that licenses the ceiling.
3. The proxy was avoidable: the phenocopy genotype is `lat4a`<sup>nr21</sup>/+ ; `kcnh2a`<sup>lof</sup>/+,
   whose SL-normalized pectoral length is published in Daane et al. 2021 Fig 4B. **The honest next
   action is to read that panel, not to re-derive from *alf*.**
4. The 1.74x input is itself unverified in the full text of either candidate source.

Corrected figure (calculated, not observed): required pectoral-length/SL overgrowth
**≈ 2.2–3.7x** (central branch, using congeneric and claim wild-type anchors and a 0.59–0.77 SL
target), implying a shortfall of **≈ 1.1–2.1x** — with an unresolved alternative branch at
6.3–7.4x required / ~3–4x shortfall if the 0.104 SL read is the pre-cut fin length.

```swarm-challenge
{"claim_id": 164, "outcome": "weakened", "reason": "Direction survives on every branch I could test, but the central magnitude hangs on one figure axis I could not re-read whose two defensible interpretations differ 2x, the 'only dominant bioelectric long-fin allele' premise is false (kcnh2a lof), and the avoidable proxy replaced a published SL-normalized measurement of the actual phenocopy genotype (Daane 2021 Fig 4B).",
  "corrected_value": "required pectoral length/SL overgrowth ~2.2-3.7x; implied shortfall ~1.1-2.1x (calculated, not observed; alternative branch 6.3-7.4x required / ~3-4x shortfall if 0.104 SL is pre-cut fin length)",
  "depends_on": ["D18-Fig1A-figure-read-0.104-SL-at-50pct-pectoral-resection (figure image could-not-access; interpretation ambiguous)", "assumption-that-0.104-SL-is-post-resection-remnant-not-pre-cut-length (the x2)", "claim-input-flying-fish-pectoral-0.65-0.77-SL", "Cheilopogon-pectoral-1.35-1.7-in-SL-approx-0.59-0.74-SL (Plazi, search-summary)", "Danio-aesculapii-pectoral-fin-length-24.0-26.8-pctSL (Kullander & Fang 2009, search-summary; zenodo/mapress unreachable)", "alf/+-pectoral-overgrowth-1.74x (unverified; absent from full text of Perathoner 2014 and Daane 2018)", "kcnh2a-lof-is-a-dominant-bioelectric-long-fin-allele-with-SL-normalized-measurements (Stewart 2021 abstract; Daane 2021 full text)", "Daane-2021-phenocopy-genotype-is-lat4a-nr21/+;kcnh2a-lof/+ (full text; Fig 4B values unread)", "pectoral-fin-length-as-the-figure-of-merit-rather-than-fin-area-or-aspect-ratio"]}
```
