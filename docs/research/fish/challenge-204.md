# Challenge 204 — adversarial review of [S16] pectoral-restricted regulatory element

**Claim under review (S16), verbatim:**

> No pectoral-restricted regulatory element adequate to drive the edits is published: of four named
> elements with pectoral reporter activity, tbx5a CNS12 also drives dorsal eye and is dispensable for
> fin formation, hand2 reagents also drive pre-anal fin fold and pelvic fin, prrx1a reporters also
> label pharyngeal arch, and the best candidate (mouse Prx1 / zebrafish prrx1a CNEs, alleles
> ib4Tg/ib5Tg) has specificity demonstrated only to ~30 hpf with signal fading by 3 dpf and no
> published caudal- or median-fin negative control.
> KEY: 0 named elements with published specificity tested explicitly against caudal and median fins

Recorded evidence level: `literature`; value `n/a`; source `harvest:s16-pectoral-regulatory-element-czmhrn`.

**Verdict: WEAKENED.** The headline survives — I could not find a pectoral-restricted element either.
The KEY metric does not survive: it is false under the reading that does any work, and tautological
under the reading that is true. Two of the four item-level disqualifications also rest on a
necessity/sufficiency conflation and on an unstated developmental stage.

---

## 0. Scope of this review, and what I could not read

**The source harvest is not in this repository.** `grep -ril` for `czmhrn`, `S16]`, `pectoral`,
`prrx1`, `tbx5a` across the whole working tree returned nothing outside `.git`. So I could not read
the author's working, the author's search scope, or — importantly — **what "the edits" are or at what
stage they are to be delivered.** Everything below is an independent reconstruction from the claim's
stated inputs, which is what the instructions ask for, but it means I cannot check the author's
arithmetic against the author's notes, only against the literature.

**Negative-search scope (mine).** Web search only, 2026-11-04, nine queries: `tbx5a CNS12 enhancer`;
`prrx1a ib4Tg ib5Tg`; `Letelier 2018 shh paired/unpaired`; `hand2 enhancer pectoral/pelvic/PAFF`;
`Haro LARM1 LARM2 Lmx1b`; and three variants of `zebrafish pectoral-fin-specific enhancer reporter
median/caudal fin negative`. No ZFIN expression-database enumeration, no ChIP/ATAC atlas sweep, no
VISTA/Enhancer Browser query, no non-teleost reporter screens. **A pectoral-restricted element could
exist in literature my nine queries did not reach.** My failure to find one is weaker evidence than
the author's KEY implies its own search was.

**Read-levels, per source.** Several publisher hosts are outside this session's allowed network
domains and could not be fetched — `anatomypubs.onlinelibrary.wiley.com`, `pubmed.ncbi.nlm.nih.gov`
and `www.sciencedirect.com` all failed DNS resolution, and `zfin.org` returned HTTP 503. Those would
need to be allowed in the session's network settings to go further.

| Source | Read-level |
|---|---|
| Adachi et al. 2016 PNAS (`10.1073/pnas.1609997113`), CNS12 | **search-summary** |
| Cell Reports 2018, CNS12sh knockout (PMC6034701) | **search-summary** |
| Hernández-Vega & Minguillón 2011, *Dev Dyn* 240:1977–1988, `10.1002/dvdy.22678` | **search-summary** (Wiley host blocked) |
| ZFIN ZDB-FIG-110804-50 / ZDB-TGCONSTRCT-111115-31 | **search-summary** (direct fetch 503) |
| Nature 2023, `s41586-023-06100-w`, hand2:EGFP median fin | **search-summary** |
| hand2 Cre/CreERT2 knock-ins (PMC11643050) | **search-summary** |
| Haro et al. 2017 *Development* 144:2009–2020 / 2021 *Nat Commun* LARM1-2 | **search-summary** |
| Hawkins et al., bioRxiv 2025.07.02.662459 (PMC12236613) | **full-text**, chars 0–100k only |
| bioRxiv 2026.02.08.704681, LARM dorso-ventral patterning | **full-text**, chars 0–200k of 272k |
| *Current Biology* `S0960-9822(26)00651-2` | **could-not-access** (403, then host blocked) |

I did **not** verify the PMID given for the 2011 paper by a search result, and I do not restate it as
fact. I did **not** independently verify "prrx1a reporters also label pharyngeal arch" at figure
level; a review cited by search summary says the two prrx1 co-orthologs overlap in "pectoral fin buds,
head mesenchyme, and branchial arches," which is consistent with the author but is corroboration at
search-summary level, not confirmation.

---

## 1. Arithmetic, redone independently: "four named elements" does not reconcile

I recounted from the claim's own four list items without reference to the author's total.

- Item 1 — `tbx5a` CNS12. A named cis-regulatory element. **Counts.** (Two named variants exist in the
  literature, CNS12 and the shortened CNS12sh; the claim collapses them, which is fine.)
- Item 2 — "hand2 reagents." **Names no element.** The hand2 reagents in the literature my searches
  reached are a *BAC* transgene (`hand2:EGFP`) and *CRISPR Cre/CreERT2 knock-ins at the locus*. A BAC
  and a locus knock-in are gene-level reagents; they are not named cis-regulatory elements and they
  carry no delimited sequence one could use as a driver. The closest actual named hand2 element I
  found — a putative enhancer ~28 kb upstream, used in a 2023 bioRxiv preprint — was characterised in
  **myocardium**, not fin. So item 2 does not populate the category the sentence declares ("four named
  elements with pectoral reporter activity").
- Item 3 — "prrx1a reporters." Counts.
- Item 4 — "mouse Prx1 / zebrafish prrx1a CNEs, alleles ib4Tg/ib5Tg." **ZFIN lists `ib4Tg` and `ib5Tg`
  as the lines carrying the `Tg(prrx1a:EGFP)` construct.** Those are the prrx1a reporters of item 3.
  Item 4 is item 3 re-described with a different caveat attached, plus the mouse Prx1 enhancer bundled
  in as though it were the same entity — it is a separate element from a separate species.

**Independent recount: 4 is not reproducible either way.** Counting distinct named cis-regulatory
elements with reported pectoral reporter activity among the claim's inputs, I get **three loci**
(`tbx5a`, mouse `Prx1`, zebrafish `prrx1`) and — because Hernández-Vega & Minguillón report **three**
conserved non-coding elements, not one — **at least five named elements** (CNS12, mouse Prx1 limb
enhancer, 3 × prrx1 CNEs). Counting as the sentence enumerates, I get **two** genuine distinct entries
(CNS12, prrx1/Prx1) after removing the hand2 non-element and merging the duplicated prrx1a.

This is not a nitpick about a tally. "Four named elements, each individually disqualified" reads as a
*survey*, and a survey is what licenses the leap to "none is published." A list that double-counts one
locus and pads with a non-element is a survey of two things presented as a survey of four, and it
silently drops the two additional prrx1 CNEs that were never individually assessed at all.

## 2. The proxy: a documentation standard standing in for tissue specificity

The quantity that matters for "adequate to drive the edits" is **does this element drive expression in
pectoral fin and not in the structures the experiment must not perturb, at the stage of delivery.**

The KEY measures something else: **whether authors performed and reported an explicit negative control
against caudal and median fins.** That is a reporting-practice metric, not a specificity metric. The
two come apart in both directions:

- **Absent documentation ≠ absent specificity.** Zebrafish reporter papers overwhelmingly image whole
  mounts. A whole-mount lateral image of a 2–5 dpf larva *contains* the median fin fold and the caudal
  fin fold in frame. An author who writes "expression restricted to the pectoral fin bud" over such an
  image has made a median-fin observation whether or not they labelled it a control. The KEY scores
  that as 0.
- **Present documentation ≠ specificity.** Conversely, the elements that *have* been explicitly scored
  against median fins mostly scored **positive**: `and1`/`actinodin1` regulatory element recapitulates
  expression in median *and* pectoral fins; `m-Inta11` (hoxa13a-linked) activates in median *and*
  pectoral fins; `2Pand1` is expressed in pectoral *and* median fin fold, differing by cell type
  rather than presence; `cx43E24` drives trunk musculature, fin fold *and* pectoral fin bud. (All
  search-summary.) So explicit testing is not rare in this literature — it is just that the answer
  keeps coming back "shared." That is a much more interesting and better-supported statement than "0
  elements tested," and it is the statement the claim should be making.

**The right metric** is something like: *number of named elements for which published imaging at ≥48
hpf shows pectoral signal with no median-fin-fold or caudal-fin-fold signal.* I cannot compute it from
the sources I could read at the read-levels I could reach, and I will not invent it. But it is
computable, and it is not what the KEY reports.

## 3. The hidden assumption that carries the result: necessity is being read as sufficiency

This is the load-bearing defect in the item-level reasoning.

The claim disqualifies CNS12 partly because it "is dispensable for fin formation." Dispensability is a
**necessity** result: delete the element, fins are still normal (the 248-bp CNS12sh deletion gives
homozygotes with normal pectoral fins). "Adequate to drive the edits" is a **sufficiency** question.
These are independent. A redundant element — one whose loss is buffered — can be an excellent driver,
and in a shadow-enhancer-rich locus redundancy is the expected finding, not a demerit.

**Relaxed, the assumption reverses the item.** The very paper that defines CNS12 reports that
`CNS12sh` driving `tbx5a` **partially rescued pectoral fin formation in the `heartstrings` mutant**,
which otherwise lacks fins (Adachi et al. 2016, search-summary). That is a direct functional
demonstration that this element drives enough `tbx5a` in pectoral fin to reconstitute an organ. For a
driver-selection question, a rescue is *the* relevant sufficiency datum — stronger than any reporter.
The claim cites the necessity result against the element and omits the sufficiency result that points
the other way.

Note also that the claim's standard **flips between items without saying so**: CNS12 is held to a
necessity standard ("dispensable"), while prrx1a/Prx1 is held to a reporter-sufficiency standard
("specificity demonstrated only to ~30 hpf"). An element cannot be fairly ranked against a standard
that changes between entries.

## 4. A regime the author missed: the named off-targets are not co-temporal with the pectoral window

"Also drives pre-anal fin fold and pelvic fin" is offered as disqualifying with no stage attached. But
in zebrafish the pectoral fin bud forms at roughly 1–2 dpf, whereas **pelvic fins and the adult
dorsal/anal/caudal fins appear at metamorphosis, around three weeks post-fertilisation.** If the edits
are delivered in embryos or early larvae, pelvic-fin activity and adult-median-fin activity are
*temporally* unreachable and cannot be off-targets at all. The live larval confounders are the median
fin fold and the pre-anal fin fold (PAFF) — and only the PAFF item survives this filter.

Because the harvest is not in the repo, **I cannot tell what stage "the edits" target, and neither,
from the text, can a reader.** The claim's adequacy verdict is stage-dependent and states no stage.
That is a defect in the claim independent of whether its conclusion is right.

One point *in the author's favour* that the author did not make: the Nature 2023 paper reports the
PAFF and the caudal fin fold have **different lineages** (PM-derived mesenchyme in the caudal fold but
not the PAFF, search-summary), so a caudal-fold negative does not license a PAFF negative. The two are
not interchangeable controls. That strengthens the author's demand for both — and makes the KEY's
lumping of "caudal and median fins" into one conjunction imprecise, since caudal fin *is* a median
fin and the fold that matters at larval stage is a third thing again.

## 5. The published counter-example the author missed: the LARM hub at `lmx1b`

Hawkins et al. (bioRxiv 2025.07.02.662459 / PMC12236613, **full-text, first 100k chars**) and the
companion bioRxiv 2026.02.08.704681 (**full-text, chars 0–200k**) report the `LARM` cis-regulatory
modules (`LARM1`, `LARM2`, the 6.8 kb "holo-LARM") controlling `lmx1bb`. From the full text:

- **Pectoral reporter sufficiency, in zebrafish.** "LARM orthologues from several gnathostomes drove
  GFP expression in zebrafish pectoral fins," and "the reporter assays, however, only report pectoral
  fin activity."
- **An explicit median-fin negative, which the claim says does not exist.** holo-LARM deletion
  abolishes `lmx1bb` in pectoral fins but "in holo-LARM deletion zebrafish, `lmx1bb` expression in the
  dorsal fin was unaffected, and the dorsal fin skeleton was normal"; the paper "concludes that LARM
  regulation is not used in median fins." The companion preprint adds, for `LARM1–LARM2`, `LARM1` and
  `LARM2` deletions, that they "did not significantly affect dsRed fluorescence in the dorsal or anal
  fins," with "no difference in the number of rays or skeletal morphologies," against a significant
  reduction in pelvic fins (p<0.01) and a pelvic splint phenotype (p=0.0105).
- **In mouse, the same hub is reported limb-specific**, and the 2017/2021 Haro et al. work reports
  transgenic LARM1 as limb-restricted with dorsal bias and LARM2 as tightly dorsal-limb in 5/5 embryos
  (search-summary).

**Consequence for the KEY.** The KEY admits two readings, and fails on both:

- *Reading A* — "elements that are specific **and** were tested against caudal+median." Then 0 follows
  trivially from the headline "no element is specific," and the KEY carries no information beyond the
  sentence it is supposed to quantify. A metric that cannot come out any other way is not a metric.
- *Reading B* — "elements whose specificity was explicitly tested against caudal and median fins."
  Then **the answer is not 0.** The LARM hub was tested explicitly against median fins (dorsal and
  anal), by two methods, with negative results reported as such. Caudal fin specifically is still
  untested — "caudal fin" does not appear in the 200k characters of the 2026 preprint I read.

So the honest corrected figure separates the two conjuncts the claim fused: **≥1 named element with an
explicit published median-fin negative; 0 with a caudal-fin test; and still 0 pectoral-restricted.**

**Why this does not refute the headline.** LARM is a **paired-appendage** module, not a pectoral one —
required in pelvic fins too, explicitly. And its specificity rests mainly on *deletion* data; the
reporter assays report pectoral activity but the papers I read do not report a reporter median-fin
negative, so LARM has the mirror-image gap to CNS12's (strong necessity-specificity, unreported
sufficiency-specificity). The claim's conclusion stands; its stated justification does not.

**Disagreement to preserve, not average.** The 2026 preprint's own shark multiome data link `LARM1` to
`lmx1b` in shark **dorsal** (median) fins, which the authors themselves flag as "contrary to
predictions based on zebrafish." And "LARM1-LARM2 deletion removes most but not all reporter
expression, so the restriction is not complete." So the paired-fin restriction of LARM may be a
teleost-lineage property rather than a general one, and is incomplete even in zebrafish. I am not
reconciling these with the zebrafish result; both stand.

A related element worth recording for the opposite reason: Letelier et al. 2018 (*Nat Genet*
50:504–509) showed the `shh` ZRS — the canonical "limb-bud-posterior" enhancer — **also works in
median fins**, and ZRS+sZRS deletion removes dorsal, pelvic and pectoral fin elements alike
(search-summary). That is the strongest single piece of support for the claim's headline direction,
and the author did not cite it. Shared paired/median regulation at `shh` is the background expectation
this whole question sits against.

## 6. Is the evidence level honest?

Partly not. `literature` / `n/a` is right for the prose. But **the KEY is a number — a count — and it
is the output of the author's own negative literature search**, presented without the scope, date, or
databases of that search, in a record whose value field says `n/a`. A search-derived count is a
*derived* quantity. Reported bare as "0," with no scope line, it reads as a settled fact about the
literature rather than as the result of one person's queries, and it is exactly the kind of figure that
goes stale the moment a preprint posts — as it has: both LARM papers postdate nothing in the claim and
one of them was posted in February 2026.

The count is also, as shown in §5, **wrong on the reading that makes it informative.** That is the
compounding failure: a derived number presented as measured, and the derivation does not hold.

---

## Summary of findings

| # | Finding | Severity |
|---|---|---|
| 1 | "Four named elements" not reproducible: item 4 duplicates item 3 (`ib4Tg`/`ib5Tg` **are** `Tg(prrx1a:EGFP)`); item 2 names no element (BAC + locus knock-ins); the 3 prrx1 CNEs are never individually assessed. Independent recount: 2 distinct entries as enumerated, ≥5 named elements across 3 loci if counted properly. | enumeration defect; weakens the survey framing |
| 2 | KEY is a reporting-practice proxy for tissue specificity. Explicit median-fin testing is **not** rare in this literature (`and1`, `m-Inta11`, `2Pand1`, `cx43E24`); it mostly returns *positive*. | proxy substitution |
| 3 | CNS12 disqualified by a **necessity** result while the same paper's **sufficiency** result — CNS12sh driving `tbx5a` partially rescues fins in `heartstrings` — is omitted. Standard also flips between items. | reasoning defect; load-bearing |
| 4 | Pelvic / adult-median off-targets are not co-temporal with the pectoral window (~1–2 dpf vs ~3 wpf). Claim states no stage for "the edits," so adequacy cannot be adjudicated as written. | unstated-assumption defect |
| 5 | Missed counter-example: **LARM hub at `lmx1bb`** (Hawkins et al.) — zebrafish pectoral GFP reporter activity **plus** explicit dorsal- and anal-fin negatives by deletion. KEY=0 is false under its informative reading. | KEY refuted |
| 6 | KEY is a search-derived count presented as measured, with no search scope, in a record whose value is `n/a`. | evidence-level defect |
| — | Headline "no pectoral-restricted element adequate to drive the edits is published" — my own nine-query search found none either; LARM is paired, not pectoral. | **survives** |

## What would settle it

1. Read `Hernández-Vega & Minguillón 2011` full text and the ZFIN figure annotations for
   `ZDB-TGCONSTRCT-111115-31`. The search summary lists Fig. 5 EGFP labelling as covering "fin
   mesenchyme, the fin bud, fin cartilage, **the fin fold**, and the scapulocoracoid." ZFIN
   distinguishes *median fin fold* from *pectoral fin fold* as separate anatomy terms. **Which one is
   annotated decides whether the best candidate has an unreported median-fin positive** — which would
   make the claim's conclusion stronger and its stated reason ("no negative control") simply the wrong
   reason. Requires `zfin.org` (503 at time of review) and `anatomypubs.onlinelibrary.wiley.com`
   (blocked) to be reachable.
2. Score the LARM reporter lines of Hawkins et al. against the **larval median fin fold** at 2–5 dpf.
   Their published negative is at juvenile/adult dorsal and anal fin, which is a different structure
   from the larval fold.
3. State the stage window of "the edits." Without it, finding 4 cannot be closed.

```swarm-challenge
{"claim_id": 204, "outcome": "weakened", "reason": "The headline survives my independent search, but the KEY count of 0 is false under its informative reading — the LARM/lmx1bb hub (Hawkins et al.) has published zebrafish pectoral reporter activity plus explicit dorsal- and anal-fin negatives — and two item-level disqualifications rest on reading a necessity result as sufficiency (CNS12's omitted heartstrings rescue) and on off-targets that are not co-temporal with the pectoral window.",
  "corrected_value": "KEY corrected: >=1 named element with published explicit median-fin (dorsal+anal) negative data (LARM1/LARM2/holo-LARM at lmx1bb); 0 named elements tested against caudal fin; 0 pectoral-restricted elements (headline unchanged). Element count '4' not reproducible: 2 distinct entries as enumerated, >=5 named elements across 3 loci if counted properly.",
  "depends_on": ["harvest:s16-pectoral-regulatory-element-czmhrn", "adachi-2016-pnas-tbx5a-CNS12-reporter-dorsal-eye-and-heartstrings-rescue", "cell-reports-2018-CNS12sh-deletion-dispensable-for-pectoral-fin", "hernandez-vega-minguillon-2011-devdyn-prrx1-CNEs-three-elements-ib4Tg-ib5Tg-30hpf-window", "zfin-ZDB-TGCONSTRCT-111115-31-and-ZDB-FIG-110804-50-fin-fold-annotation-ambiguity", "nature-2023-s41586-023-06100-w-hand2-EGFP-PAFF-positive-caudal-negative-and-PAFF-vs-caudal-distinct-lineage", "hand2-cre-creert2-knockin-PMC11643050-pelvic-and-PAFF-labeling", "hawkins-et-al-biorxiv-2025.07.02.662459-PMC12236613-LARM-zebrafish-pectoral-GFP-and-dorsal-fin-negative", "biorxiv-2026.02.08.704681-LARM1-LARM2-deletion-pelvic-requirement-dorsal-anal-negative-shark-dorsal-fin-discordance", "haro-2017-development-and-2021-natcommun-LARM1-LARM2-mouse-limb-specificity", "letelier-2018-natgenet-shh-ZRS-active-in-median-and-paired-fins", "zebrafish-developmental-timing-pectoral-bud-1-2dpf-vs-pelvic-and-adult-median-fins-~3wpf", "unstated-stage-window-of-the-edits-in-S16"]}
```
