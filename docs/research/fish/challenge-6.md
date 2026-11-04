# Challenge 6 — *kcnk5b* gain-of-function: sufficiency, conductance-dependence, pectoral buds

**Claim under review (claim_id 6), quoted as recorded:**
> "kcnk5b gain-of-function is sufficient for fin overgrowth, is conductance-dependent, and enlarges
> pectoral BUDS"
>
> recorded evidence level: `literature`; value: `n/a`; source: `zebrafish-fin-genetics.md`

**Verdict: WEAKENED.** All three clauses have real published support, and I could not refute any of
them outright. But the claim as recorded is a *bundle* that (i) merges two different papers, two
different life stages and two different constructs into one sentence, (ii) attributes to a
gain-of-function allele a pectoral-bud result that was obtained by heat-shock overexpression of the
**wild-type** channel in a paper that studied no *alf* allele, and (iii) carries an evidence level
of `literature` that the source document itself forbids — `zebrafish-fin-genetics.md` §0 states
"**Nothing in this file has been read at full-text or abstract level**" and instructs the reader to
treat the whole file as unread-source tier. One clause (conductance-dependence) came out
*stronger* than recorded. Details and the corrected clause-by-clause wording are below.

**Read-levels achieved in this review (the source document could not reach any primary source; in
this session I could):**

| Source | Read-level here |
|---|---|
| Perathoner et al. 2014, *PLoS Genetics* 10(1):e1004080 — `alf`/*kcnk5b* | **full-text** (journals.plos.org + PMC3894163) |
| Jiang, Zhao, Sun, Song, Yi, Xiong, Wang, Yu, Chen, Liu, Yan & Antos 2024, *PLoS Biology* 22(3):e3002565 — pectoral fin **buds** | **full-text** (journals.plos.org + PMC11018282; long article, read in two windows) |
| Yi et al. 2021, *eLife* 10:e60691 — `Tg[hsp70:kcnk5b-GFP]`, calcineurin/S345 | **full-text**, first ~100 kB only (methods + Figs 1–6 narrative) |
| Silic et al. 2020, *Genetics* 215(4):1067 — dermomyotome bioelectricity | **full-text**, first ~100 kB only |
| Aramaki & Kondo 2024, bioRxiv 10.1101/2024.03.27.587111v1 — osteoblast-restricted `kcnk5b W169L` | **full-text**; **preprint, not peer-reviewed** |
| `pubmed.ncbi.nlm.nih.gov` | **could-not-access** — DNS failure in this session (`ENOTFOUND`). Would need allowing in the session's network settings. ZFIN was not attempted, so every allele ID remains `unknown`, as in the source. |

---

## 1. Arithmetic, redone independently

The claim's recorded value is `n/a`, so there is **no author arithmetic to re-derive**. Stating that
plainly rather than manufacturing a check.

There is, however, quantitative material in the primary sources that the claim's `n/a` throws away.
From Perathoner 2014 (full-text): wild-type caudal fin relative growth has allometric coefficient
*k* = 1.29; *alf* heterozygotes show "positive allometric growth … with an allometric coefficient
*k* near 2". Silic et al. 2020 (full-text) cite *k* = **1.88** for the *kcnk5b* mutant, attributing
it to Perathoner 2014 and Lanni et al. 2019. **I am preserving that disagreement rather than
averaging it:** "near 2" and 1.88 are not the same number and I did not see the figure source data
that would settle which is the measured value for which genotype.

**My calculation, not a measurement, flagged as such.** On the authors' own power law
(fin ∝ body^*k*), over a doubling of body length the *alf*/wild-type ratio of relative fin length is
2^(*k*<sub>alf</sub> − *k*<sub>wt</sub>):

- *k*<sub>alf</sub> = 2.00 → 2^0.71 ≈ **1.64×**
- *k*<sub>alf</sub> = 1.88 → 2^0.59 ≈ **1.51×**

So the published allometry implies roughly a 1.5–1.6× relative-fin-length divergence across a
body-length doubling. This is a **derived** number. It assumes a single power law holds across the
interval and that the two genotypes share an intercept at the interval's start — the second
assumption is not something I verified, and it is doing real work, so the figure is illustrative of
scale, not a fin measurement. The one molecular effect size the paper does state is "an almost
two-fold increase in K⁺ conductance" for either mutant cRNA over wild-type in oocytes (n = 5–26
recordings per condition).

---

## 2. Is a proxy standing in for the quantity that matters? Yes — two layers deep

The clause "**enlarges pectoral BUDS**" rests on Jiang et al. 2024, where the measured quantity is
**pectoral fin bud area at 32, 48 and 56 hpf, standardised to eye area** in the same embryo (the
supplementary design uses **otic vesicle area** as the normaliser instead). That is a proxy stacked
on a proxy:

1. **Normaliser proxy.** The `hsp70` driver is a *ubiquitous* heat-shock promoter, so the
   overexpression is not bud-restricted. A bud:eye ratio is only a size readout if eye growth is
   unaffected by the same manipulation. I found no test of that in the paper. **My inference, not
   the authors' claim:** a ubiquitous driver plus an organ-ratio readout cannot distinguish "bud
   grew" from "normaliser organ shrank or grew less", and the two normalisers used (eye, otic
   vesicle) are not cross-checked against each other in the text I read.
2. **Stage proxy.** An embryonic bud at 48 hpf is not an adult fin. The authors deliberately
   measured at 48 hpf "to avoid finfold growth". Nothing in the paper's visible text links the bud
   change to adult **pectoral** fin size; its adult data concern *rcan2*, caudal fins and
   regeneration.

**The quantity that matters** for the use this claim is put to in `zebrafish-fin-genetics.md` §5
(edit #2 of a candidate glider stack) is **adult pectoral fin ray length / planform area at a
standard body length**. Neither paper reports it for *kcnk5b*. Perathoner 2014 measured **caudal
and dorsal fins and maxillary barbels**; the word *pectoral* **does not appear in that paper at
all** (checked across the full text in two windows). Scope of that negative: full-text search of
Perathoner 2014 on journals.plos.org and PMC3894163, plus one targeted web search for adult *alf*
pectoral ray measurements, which returned none. That is a negative over four sources, not over the
literature.

---

## 3. The hidden assumptions, tested relaxed

**(a) "Gain-of-function" is carrying the claim, and it should not be.** Perathoner 2014's
sufficiency experiment used the *Xenopus* `ef1a` promoter to drive **wild-type or W169L** *kcnk5b*
with a DsRed co-marker: "In about 40% of the fish injected with plasmids encoding **wild type or
mutant** *kcnk5b* and showing DsRed positive cells in the fins we found a local overgrowth
phenotype", against 0/240 for DsRed alone. The paper reports **no separate per-construct counts in
the text** (they appear only in Figure 6H, which I did not read as source data) and no statistical
comparison between wild-type and mutant constructs. The same direction holds elsewhere: Yi et al.
2021 report that heat-shock induction of the wild-type-derived `Tg[hsp70:kcnk5b-GFP]` increased
larval finfold proportions, and Silic et al. 2020 report that overexpressing *kcnk9* — "another K2P
potassium channel similar to *kcnk5b*" — gave long fins (in 2/31 fish, 6%). Jiang et al. 2024 get
the same bud effect from `Tg[hsp70:kcnk10-GFP]` as from *kcnk5b*.

Relaxed, the assumption fails: the sufficient condition is **elevated K2P K⁺-leak conductance in
the right cells**, which *alf*-type GOF is one way (and ordinary overexpression another, and a
different channel another) of producing. Writing the claim as a property of "*kcnk5b*
gain-of-function" over-attributes it to that allele.

**(b) "Sufficient" hides penetrance and locality.** The 40% figure is the fraction of *injected,
DsRed-positive* mosaic fish showing **local** overgrowth — not a germline, whole-fin, fully
penetrant result; *kcnk9* overexpression managed 6%. "Sufficient" is defensible but should read
"sufficient to induce local overgrowth in a minority-to-plurality of mosaic clones".

**(c) Cell-type context is assumed irrelevant — and a counter-example says it is not.** See §5.

---

## 4. Is the evidence level honest? No

Two separate defects.

**(i) Tier inflation.** Recorded as `literature`. The source file's own §0 and §7 say every citation
in it is read-level `search-summary`, that **nothing** was read at full-text or even abstract level,
and that the file is *unread-source* tier per `CONTRIBUTING-VERIFICATION.md` §3. A claim lifted out
of that file and labelled `literature` with no read-level qualifier presents search-engine summaries
as read literature — exactly rule 3's failure mode. (The source document is scrupulous about this
internally; the defect is in the extracted claim record, not in the document's own prose.) This
review repairs it for the two load-bearing papers by reading them at full-text, so the *corrected*
record can legitimately read `full-text` — but it could not have before someone read them.

**(ii) Provenance conflation.** The three clauses do not come from one body of work:

| Clause | Actual source | Stage | Construct |
|---|---|---|---|
| sufficient for fin overgrowth | Perathoner 2014 | adult / mosaic injected | `ef1a:kcnk5b` **wild-type or W169L** |
| conductance-dependent | Perathoner 2014 | adult / mosaic injected | `kcnk5b`(GFG→AAA) pore-dead |
| enlarges pectoral **buds** | **Jiang et al. 2024** | embryo, 32–56 hpf | `Tg[hsp70:kcnk5b-GFP]`, **wild-type-derived** cDNA (Yi et al. 2021: "isolated by RT-PCR from regenerating adult fin cDNA library"; neither paper labels it *alf*/W169L) |

The bundling creates a false impression that one paper demonstrated all three, and silently
transfers the gain-of-function label onto a wild-type-overexpression embryonic result. It also drops
the authors' own hedge: Jiang et al. state in their Discussion that "the changes in fin bud size
caused by knockout or overexpression of *kcnk5b* or *rcan2* are **not large**, but they are
biologically significant". No percentage, ratio or P value for bud size appears in that paper's
running text (values sit in Figs 2C and 4E); the design is N ≥ 3 experiments × ≥ 3 fish, one bud per
embryo, two-tailed Student's *t*-test.

**On the one clause that got stronger:** conductance-dependence is better supported than the
source's summary-level note implied. Perathoner 2014 mutated the GFG selectivity filter to AAA,
confirmed by oocyte recording that the channel could not conduct K⁺, and found "no overgrowth …
in these fish" despite DsRed-positive fin tissue including fibroblasts (n = 32); their stated
conclusion is that "the increase in conductance of the Kcnk5b channel is essential for the
coordinated overgrowth". Yi et al. 2021 add an activity-graded series in the same direction (S345E,
elevated conductance, highest allometric regenerative growth; S345A, decreased conductance, lowest
growth rates), and the *kcnk9*/*kcnk10a* results above are what conductance-dependence predicts.
**The one caveat I can state honestly:** the paper reports no verification of the GFG→AAA protein's
expression or localisation in fin tissue, and a triple substitution in a K2P selectivity filter is
the kind of lesion that can also destabilise or mistraffic the protein — so a strict reading is
"no overgrowth from a channel shown not to conduct", with trafficking uncontrolled. The graded
S345 series is what rescues the inference, and it is in a different paper.

---

## 5. Counter-example the author missed

**Aramaki & Kondo 2024, bioRxiv 10.1101/2024.03.27.587111v1 — preprint, not peer-reviewed, flagged
as such.** They expressed the *kcnk5b* **W169L** gain-of-function channel under osteoblast-specific
promoters (*RUNX2*, early; *osterix*, mid-stage) and report bone segments "elongated (by 58% and
71%)" respectively while these transgenes "scarcely affect the overall size of fins" — their stable
*RUNX2* line gives 191% of wild-type segment length with a caudal fin at 113% of wild-type. (Those
two segment numbers, 58–71% and 191%, are **mutually inconsistent within the preprint**; I am
reporting the inconsistency, not picking one.) Their conclusion is that segment length is set by
osteoblasts while total fin size is set by keratinocytes.

If that holds, **GOF *kcnk5b* expression is not sufficient for fin overgrowth in all cell types** —
sufficiency is conditional on the expressing cell population. This does not contradict Perathoner
2014, whose mosaic clones were in intra-ray mesenchyme/fibroblasts, but it does break the
unqualified word "sufficient". Note the unresolved three-way disagreement on *which* cells carry
fin-size control, which I am preserving rather than reconciling: intra-ray mesenchyme (Perathoner
2014), keratinocytes for total size (Aramaki & Kondo 2024, preprint), dermomyotome for a different
channel and explicitly argued to be "independent of the previously reported fin-local regulation by
*kcnk5b* and *kcc4a*" (Silic et al. 2020).

**A regime limit worth recording separately:** every sufficiency result above is an *overexpression*
result. None of the papers I read tests a dose at which the effect saturates, and §1's allometry
does not extrapolate — so this claim supports no statement about how far fin size can be pushed.

---

## 6. Corrected claim, clause by clause

Replace the recorded one-liner with:

1. **Sufficiency (full-text, Perathoner 2014):** mosaic `ef1a`-driven overexpression of *kcnk5b* —
   **wild-type or W169L, with no per-construct comparison reported in text** — induced *local* fin
   and barbel overgrowth in ~40% of injected DsRed-positive fish (0/240 for marker alone). GOF is
   *one* sufficient route, not the operative variable; cell type matters (§5, preprint).
2. **Conductance-dependence (full-text, Perathoner 2014 + Yi et al. 2021):** supported, and more
   strongly than recorded — pore-dead GFG→AAA gave no overgrowth (n = 32 DsRed⁺ fins), and an
   S345 activity-graded series tracks growth monotonically. Caveat: GFG→AAA expression/trafficking
   in fin tissue not verified.
3. **Pectoral buds (full-text, Jiang et al. 2024 — *different paper, different stage, wild-type
   construct*):** ubiquitous heat-shock overexpression of wild-type Kcnk5b-GFP (and equally of
   Kcnk10-GFP) enhanced pectoral fin **bud** area normalised to eye area at 32/48/56 hpf; CRISPR
   knockout reduced it by 48 hpf. Authors call the changes "not large, but … biologically
   significant". **Not** demonstrated: that the bud change persists into adult pectoral fin size,
   and **not** demonstrated anywhere I read: adult pectoral fin enlargement by *kcnk5b* at all.
4. **Evidence level:** was `literature` on a source file that declares itself unread-source tier;
   now `full-text` for clauses 1–3 by this review, with the provenance split made explicit.

Nothing here changes the downstream conclusion of `zebrafish-fin-genetics.md` §5 — if anything the
bud/adult gap and the "not large" hedge make the glider stack weaker, not stronger. No ZFIN allele
ID was recovered; every one remains `unknown`. No number, citation, gene symbol or allele in this
file was invented.

```swarm-challenge
{"claim_id": 6, "outcome": "weakened", "reason": "All three clauses hold at full-text, but the record bundles two papers and mislabels provenance: the pectoral-BUD result is Jiang et al. 2024 PLoS Biology using ubiquitous heat-shock overexpression of WILD-TYPE Kcnk5b-GFP in 32-56 hpf embryos (effect the authors themselves call 'not large', normalised to eye area, never linked to adult pectoral fin size), not an alf gain-of-function result; Perathoner 2014 never mentions pectoral fins, got equal overgrowth from wild-type and W169L constructs in ~40% of mosaic fish, and an unreviewed preprint shows W169L in osteoblasts elongates segments without enlarging fins - while the recorded level 'literature' sits on a source file that declares itself unread-source tier.", "corrected_value": null}
```
