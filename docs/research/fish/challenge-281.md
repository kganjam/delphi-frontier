# Challenge 281 — "enlarger plus suppressor, not uniform enlargement"

**Claim under review (verbatim, not mine):**
> "MECHANISTICALLY THIS IS ENLARGER PLUS SUPPRESSOR, not uniform enlargement. That is why the
> published result is about fin PROPORTIONS rather than fin size, and it means the design lever is
> differential allometry across fins rather than growth of one fin"

Recorded evidence level: `derived`. Recorded value: `n/a`. Recorded source: "inference from the allele
descriptions".

**Verdict: WEAKENED.** The two labels ("enlarger", "suppressor") are sound — in fact they are the
paper's own words rather than an inference, so the claim is *under*-credited, not over-credited. What
does not survive is the mechanistic step in the middle and the engineering conclusion at the end:
(a) two opposing whole-animal levers do not produce a proportion change on their own; the paper's own
text attributes the differential to *fin-specific* suppression, a third ingredient the claim's picture
omits; (b) "allometry" is a proxy — the zebrafish panels report fin-length/standard-length ratios at
adult stage, not scaling exponents; (c) there is no dosable suppressor to pull as a "design lever":
loss of lat4a has no fin phenotype at all, so only one specific gain-of-function allele suppresses, by
an unidentified mechanism.

## 0. What I read, and at what level

| Source | Read level |
| --- | --- |
| Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP. "Modulation of bioelectric cues in the evolution of flying fishes." *Curr Biol* 31 (2021). doi:10.1016/j.cub.2021.08.054 | **listing** — I did **not** open the PDF in this session. I read the 32 verbatim quotes and the structured chain recorded in this repository at `connectors/genomics/daane2021.py` and `daane2021_records.py` (branch `origin/work/nca-curriculum`), whose header states the PDF was read in full (19 pages) and whose harness fails the run if a quote is not found in the text. Every quote I rely on below is one of those, by its connector quote id. |
| Publisher supplement (Data S1A — the fin/body measurements; Figures S1–S4) | **could-not-access** — the connector itself records `"retrieved": false` for the supplement and notes it is not part of the 19-page PDF. I did not retrieve it either. |
| External literature on other zebrafish fin-overgrowth alleles (kcnk5b/`another longfin`, kcnj13) | **could-not-access in this session.** Scope of the negative: I ran no web or literature search at all here. Where that matters below I write `unknown` rather than guessing. |

So: nothing in this review is an observation of mine. The quotes are the paper's statements; the
arithmetic and the mechanistic reasoning are mine and are marked as such.

## 1. Arithmetic, redone independently

The claim contains **no arithmetic** — its recorded value is `n/a` and it is a mechanistic
proposition. There is therefore nothing to recompute, and I will not manufacture a number for it.

One adjacent figure was available to check independently, and I did check it because it is the only
quantitative hook near this claim. Connector quote `lof_breakpoints` gives the lof^dt2 inversion
breakpoint "between kcc4a and kcnh2a (24.075 Mb)" in Zv11/GRCz11; the connector separately records the
ZFIN GRCz11 start of kcnh2a as 24,080,694. My own subtraction: 24,080,694 − 24,075,000 = **5,694 bp
≈ 5.7 kb** upstream. The connector's prose says "about 5.6 kb". Both are consistent with "between
kcc4a and kcnh2a"; the ~0.1 kb difference is rounding of a figure the paper prints to three decimals
of a megabase (i.e. ±500 bp), so it is not a defect in either. This is a *calculated* distance from
two recorded inputs, not a measurement, and it does not bear on claim 281 either way — I report it
only to show the check was run rather than copied.

## 2. Is a proxy standing in for the quantity that matters?

**Yes, twice, and the second one is the serious one.**

**Proxy A — "proportions" is a ratio, "allometry" is a slope.** The paper's Figure 4 title (quote
`fig4_title`) says the intersection is "sufficient to phenocopy the evolved flying fish fin
**allometry**", and the repo's pin for Figure 4 records panels B and C as "pectoral and caudal fin
length / SL". My inference, not the paper's: a fin-length-to-standard-length *ratio* measured in adult
trans-heterozygotes is not an allometric coefficient. Allometry is the exponent *b* in
`fin = a · SL^b`, estimated from a size series; a single-size ratio is the quantity `fin/SL`, which
equals `a · SL^(b−1)` and therefore conflates the exponent with the size at which you happened to
measure. Two genotypes can share a ratio at one body length and have different slopes, or differ in
ratio while sharing a slope.

This matters because the flying-fish side of the comparison *is* a slope: quotes
`allometry_identical` ("The allometric relationship between body size and pectoral fin length was
identical across the two- and four-wing flying fishes") and `allometry_rapid` describe a relationship
across specimens, from the museum measurements in Data S1A. So the paper's headline compares a slope
(wild beloniforms) with what the pins describe as a ratio (zebrafish mutants).

**The right quantity:** per-fin log–log scaling exponents — slope of log(fin length) on log(SL),
fitted separately for pectoral, dorsal, anal and each caudal lobe, in each of the four genotypes
(wild type, nr21/+, lof/+, nr21/lof) across a deliberate size range, with confidence intervals on the
slope differences. Whether Figure 4B–C actually contains that, or only adult ratios, I record as
**unknown**: I have the pin description, not the panel. That is the first thing to check against the
figure before this claim's "differential allometry" wording is used anywhere load-bearing.

**Proxy B — "fin proportions" as a proxy for the trait the design lever is supposed to deliver.** The
connector is already explicit that the phenocopy is "relative fin proportions ... in a zebrafish
double mutant" and that flight, gliding and any aerodynamic or locomotor measurement are *not* in the
text read. The claim does not over-reach here — it correctly says "proportions rather than fin size" —
so I am not charging it with this. I note it because the claim's final clause ("the design lever is
differential allometry across fins") invites exactly that slide, and the honest scope is: a lever on a
length ratio, in one species, at one life stage.

## 3. The hidden assumption that carries the result, relaxed

The claim's middle step is a superposition model: one lever adds growth, the other subtracts it, and
*because* they are two opposing levers the output is a proportion change. Written out, that model is

```
fin_i(genotype) = baseline_i + E_i(enlarger) − S_i(suppressor)
```

and the claim's "not uniform enlargement" contrast implies the interesting structure comes from having
both terms. **Relax the hidden assumption that `E_i` and `S_i` are fin-independent (uniform across
fins) and the claim's reasoning collapses in both directions:**

- If `E_i` and `S_i` are both uniform, then two opposing uniform levers give a uniformly rescaled
  fish — i.e. a *size* change (possibly near-zero net), **not** a proportion change. Superposition of
  two global levers cannot by itself produce "elongated paired fins **and** a hypocercal caudal fin",
  which is a sign-flipped, fin-specific outcome (quote `fig4_transhet`). So the claim's stated
  mechanism does not entail its stated consequence.
- The paper supplies the missing ingredient explicitly, and it is not "two levers": quote
  `fig4_mechanism` reads "the mechanism of **fin-specific suppression** of lof by lat4a mutations is
  occurring downstream of bioelectric signaling signals". The differentiality is a property of the
  suppression itself. My inference: the proportion change is carried by `S_i` varying across fins
  (median fins suppressed, paired fins not), not by the arithmetic of having an enlarger and a
  suppressor at all.

A second hidden assumption, and the one that breaks the engineering conclusion: **that the suppressor
is a lever you can set.** Relax it against the paper's own controls:

- `lat4a_null`: "zebrafish lacking lat4a have no fin phenotype." Loss of function does nothing.
- `nr21_gof`: a cis frameshift reverts nr21, "indicating that the mutation in lat4a^nr21 results from
  a gain-of-function effect."
- `nr21_small_fins`: nr21 alone gives "small adult fins" — *all* fins, not median fins only.
- `fig4_qrt`: "kcnh2a expression does not vary significantly in pectoral or dorsal fins containing the
  nr21 mutation" — so the suppressor is not acting by turning the enlarger's level down.

Taken together (my inference from those four of the paper's statements): there is no endogenous
lat4a dial. The suppressor arm is one specific neomorphic substitution (T200K) acting by an
unidentified mechanism downstream of bioelectric signalling, whose *isolated* effect is uniform
shortening and whose *fin-specific* effect appears only in combination with lof. "Differential
allometry across fins" is a fair description of the observed outcome; it is not yet a lever, because
nothing in the text read tells you how to set it, dose it, or redirect it to a different fin. Calling
it a design lever presumes a tunability the paper does not demonstrate.

Two further practical constraints on the same clause, from the paper's own resource statements: the
alleles are not the flying-fish variants (laboratory T200K in zebrafish vs natural F326L in
beloniforms — different residues, and quote `f326l_caveat` is the authors' own caveat that the F326L
association may reflect incomplete lineage sorting or introgression), and quote `lof_not_maintained`
says the lof^dt2 line and its revertants "are no longer maintained nor frozen", against a key-resources
table that lists ZIRC ZL86. The repo preserves that disagreement rather than resolving it, and so do I.

## 4. Is the evidence level honest?

**It is honest, and in one respect too modest — which is itself worth correcting, because
under-labelling moves effort to the wrong place.**

Recorded as `derived`, "inference from the allele descriptions". But the two load-bearing labels are
printed in the paper:

- "suppressor" is not inferred. Figure 4A legend, quote `fig4_suppressor`: "lat4a is a fin
  **suppressor** of overgrowth caused by increased potassium channel function."
- "enlarger" is not inferred either. Quote `lof_ectopic`: "As ectopic expression of kcnh2a is
  sufficient to drive fin overgrowth"; quote `lof_cis_ref` (the title of ref. 21, Stewart et al. 2021):
  longfin "causes cis-ectopic expression of the kcnh2a ether-a-go-go K+ channel to autonomously
  prolong fin outgrowth".

So the first sentence of the claim is **author-stated** (read level: listing, via verified-verbatim
quotes), not derived. What *is* derived — and is mine as much as the claim's — is the superposition
reading of how those two produce a proportion change, and the "design lever" conclusion. The right
split is: sentence 1 `author-stated`; sentence 2's causal "that is why" `derived`; sentence 3
`derived, and currently unsupported` per §3. Nothing here presents a calculation as an observation,
and no number, citation, gene symbol, allele or accession in the claim is invented — every symbol it
leans on (lat4a/nr21/T200K, kcnh2a/lof^dt2) appears in the recorded quotes. Note separately that the
repo already flags `lat4a → slc43a2a` as **inferred, not the paper's stated identifier** (the paper
prints no ZFIN/Ensembl id in the text read, and UniProt's LAT4 protein name sits on the *paralog*
slc43a2b); claim 281 does not depend on that mapping, but anything built on top of it does.

## 5. Regime, taxon or counter-example the author missed

**The contrast class is the weak point.** "Not uniform enlargement" is only informative if the
alternative — a single enlarger — actually enlarges fins uniformly. The paper's Figure 3 pin records
"kcnh2a/kcnk5b/kcnj13 overexpression (panels H–J)" and quote `lof_ectopic` cites all three as
sufficient to drive overgrowth. Whether any single one of them scales all fins isometrically, or
already shifts proportions on its own, is **unknown to me**: I have the pin and the quote, not the
panels, and I ran no external search (scope stated in §0). If a single enlarger already changes
proportions — which is what I would expect of a channel acting on fin-ray outgrowth with a dorsal–
ventral or paired–median bias, though that expectation is a prediction and not evidence — then the
claim's dichotomy is a strawman, and "enlarger plus suppressor" would be one route to differential
proportions among several, not the mechanism.

Within the paper there is also one taxon that cuts against a clean two-lever story, and the claim does
not engage it: quote `sailfin` — "only one flying fish species in our dataset lacks the convergent
lat4a allele, the sailfin flying fish *Parexocoetus brachypterus*" — recorded in the repo as the
exception *with an elongated dorsal fin*. A species reaching an extreme fin proportion without the
lat4a allele is, on the claim's own logic, a counter-example to lat4a-type suppression being the
route to differential fin proportions. (Correlational, 35-species targeted capture, average 78.3% of
targets at 38.3-fold — quote `cap_coverage` — so it weakens the claim's generality; it does not refute
the zebrafish genetics.)

**Two checks that would settle this**, both inside material that exists but was not read here:
1. Figure 4B–C panels: are they per-genotype ratios at adult stage, or fitted slopes across a size
   series? That decides whether "allometry" is measured or proxied (§2).
2. Figure 3H–J single-enlarger overexpression: isometric across fins, or already differential? That
   decides whether the claim's contrast class is real (§5).

## What I could not break

The core labelling is solid, and I tried to break it. lat4a^nr21 is reported as a suppressor of
kcnh2a-driven overgrowth, in the paper's own words; kcnh2a^lof is reported as an enlarger, in the
paper's own words; the trans-heterozygote outcome is reported as a proportion pattern (elongated
paired fins, hypocercal caudal), not a size pattern; and the claim's refusal to call this "fin size"
is correct and matches the repo's own scoping. I found no fabricated number, symbol or citation. The
claim fails only where it moves from those labels to *why* proportions change, and from there to a
"design lever" — and on the second of those the paper's own `lat4a_null` control is the thing that
stops it.

```swarm-challenge
{"claim_id": 281, "outcome": "weakened", "reason": "The enlarger/suppressor labels are the paper's own words rather than a derived inference, but two opposing uniform levers cannot produce a proportion change — the paper attributes the differential to fin-specific suppression, an omitted third ingredient — while 'allometry' is proxied by adult fin/SL ratios and the suppressor is not a settable lever, since lat4a loss of function has no fin phenotype and only the T200K gain-of-function neomorph suppresses, by an unidentified mechanism.",
  "corrected_value": null,
  "depends_on": ["Daane et al. 2021 Curr Biol doi:10.1016/j.cub.2021.08.054, Figure 4A legend quote fig4_suppressor: 'lat4a is a fin suppressor of overgrowth caused by increased potassium channel function'", "quote lof_ectopic: 'As ectopic expression of kcnh2a is sufficient to drive fin overgrowth (Figure 3)'", "quote fig4_transhet: 'the nr21/lof trans-heterozygotes exhibit elongated paired fins and a hypocercal caudal fin'", "quote fig4_mechanism: 'the mechanism of fin-specific suppression of lof by lat4a mutations is occurring downstream of bioelectric signaling signals'", "quote lat4a_null: 'zebrafish lacking lat4a have no fin phenotype'", "quote nr21_gof: nr21 acts by gain of function (cis frameshift reverts it)", "quote nr21_small_fins: nr21 alone gives small adult fins (all fins)", "quote fig4_qrt: kcnh2a expression does not vary significantly in fins carrying nr21", "quote fig4_title: Figure 4 is titled as phenocopying flying fish fin ALLOMETRY", "repo pin for Figure 4 describing panels B and C as pectoral and caudal fin length / SL", "quote allometry_identical: the flying-fish comparison is an allometric relationship across specimens (Data S1A)", "quote sailfin: Parexocoetus brachypterus lacks the convergent lat4a allele yet has an elongated dorsal fin", "the verified-verbatim quote set in connectors/genomics/daane2021.py on branch origin/work/nca-curriculum (my read level: listing, not the PDF)"]}
```
