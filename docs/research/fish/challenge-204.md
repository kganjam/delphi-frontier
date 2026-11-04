# Challenge 204 — adversarial review of [S16] pectoral-restricted regulatory element

**Claim under review (verbatim):**

> "[S16] No pectoral-restricted regulatory element adequate to drive the edits is published: of four
> named elements with pectoral reporter activity, tbx5a CNS12 also drives dorsal eye and is
> dispensable for fin formation, hand2 reagents also drive pre-anal fin fold and pelvic fin, prrx1a
> reporters also label pharyngeal arch, and the best candidate (mouse Prx1 / zebrafish prrx1a CNEs,
> alleles ib4Tg/ib5Tg) has specificity demonstrated only to ~30 hpf with signal fading by 3 dpf and
> no published caudal- or median-fin negative control. KEY: 0 named elements with published
> specificity tested explicitly against caudal and median fins"

- recorded evidence level: `literature`; recorded value: `n/a`
- source: `harvest:s16-pectoral-regulatory-element-czmhrn`
- reviewer: adversarial, did not author the claim
- review date: 2026-11-04

**Verdict: WEAKENED.** The prose conclusion survives and is arguably strengthened. The KEY number
is refuted: at least one named element has a published explicit median-fin negative control, which
the author's census missed.

---

## 0. Read-levels of every source used

Honesty floor requires this up front. Scope of my own searching is stated in §5.

| Source | What I used it for | Read-level |
|---|---|---|
| *Current Biology* (2026), "The origin and evolution of dorsal determination mechanisms in vertebrate paired appendages", via PMC13348734 | LARM deletions, reporter assays, dorsal-fin control | **full-text, partial** (first ~100,000 chars of 157,957 retrieved) |
| bioRxiv 2025.07.02.662459, via PMC12236613 | LARM abstract + reporter/median-fin statements | **full-text, partial** (first ~100,000 chars of 142,884) |
| bioRxiv 2026.02.08.704681 ("Ancient origin of the dorso-ventral patterning system…") | LARM pectoral+pelvic deficit | **search-summary** |
| Letelier et al. 2018, *Nat Genet* 50:504 — "A conserved Shh cis-regulatory module highlights a common developmental origin of unpaired and paired fins" | ZRS / sZRS pectoral + median activity | **search-summary** (abstract-level; full text not accessed) |
| PNAS 2016, "Regulatory evolution of Tbx5 and the origin of paired appendages" | CNS12 size, dorsal-eye activity, *hst* rescue | **search-summary** |
| *Cell Reports* 2018, "Genomic Knockout of Two Presumed Forelimb Tbx5 Enhancers Reveals They Are Nonessential for Limb Development" | cns12sh deletion, normal fins | **search-summary** |
| Hernández-Vega & Minguillón 2011, *Dev Dyn* 240(8):1977–88, "The Prx1 limb enhancers…" | Prx1/prrx1a CNE reporters, stages | **search-summary only.** Publisher host `anatomypubs.onlinelibrary.wiley.com` does not resolve from this session (outside allowed network domains); needs allow-listing for a full-text check |
| ZFIN: construct `Tg(prrx1a:EGFP)` (ZDB-TGCONSTRCT-111115-31), figure ZDB-FIG-110804-50 | existence of `ib4Tg`/`ib5Tg`, annotated stage range | **listing** (via search summary of the ZFIN records; direct WebFetch of both ZFIN URLs returned HTTP 503) |
| hand2 Cre/CreERT2 knock-ins (2024, bioRxiv/journal) | labelled tissues incl. PAFF, pelvic fin | **search-summary** |
| *Nature* 2023, "A median fin derived from the lateral plate mesoderm and the origin of paired fins" | TgBAC(hand2:EGFP), PAFF vs caudal fold | **search-summary** |
| Chan et al. 2010, *Science* — stickleback *Pitx1* `Pel` enhancer | constructive lead only (§5) | **search-summary** |
| *actinodin1* (and1) ectodermal enhancer reports | median + pectoral fin fold ectoderm | **search-summary** |

Nothing below is an observation I made. Every statement is either (a) the author's claim,
(b) something a cited source reports, at the read-level above, or (c) **my inference**, labelled as
such in the sentence.

---

## 1. Arithmetic, redone independently from the stated inputs

The claim contains two numbers: "four named elements" and "KEY: 0".

**Recount of "four".** I enumerate from the claim's own text, without copying its total:

1. `tbx5a` CNS12
2. `hand2` reagents
3. `prrx1a` reporters
4. mouse Prx1 / zebrafish `prrx1a` CNEs, alleles `ib4Tg`/`ib5Tg`

That is four *list items*, so the stated total is internally consistent. But items 3 and 4 are not
independent: ZFIN attributes `ib4Tg` and `ib5Tg` to construct `Tg(prrx1a:EGFP)` annotated to
Hernández-Vega & Minguillón 2011 (read-level: listing), and that is the same study that reports the
mouse Prx1 enhancer lines and the zebrafish `prrx1a` CNE. **My inference:** the census counts one
paper's element set twice, so the number of distinct *loci* surveyed is three (`tbx5a`, `hand2`,
`prrx1`), not four. This does not change the direction of the conclusion; it does mean "four"
overstates the breadth of the survey behind a KEY of zero.

**Recount of "0".** This is the number that breaks. See §2 and §5 — I find **≥1** named element with
a published explicit median-fin negative control, and the author's own framing is what makes it
count.

**A third number, checked independently.** The claim says specificity is "demonstrated only to
~30 hpf with signal fading by 3 dpf". ZFIN's annotation for the `ib4Tg`/`ib5Tg` figure records a
stage range of **Prim-5 to Protruding-mouth** (read-level: listing). Converting independently from
Kimmel et al. 1995 staging rather than from the author's figure: Prim-5 = 24 hpf,
Protruding-mouth = 72 hpf. So the annotated window is **24–72 hpf**, i.e. ~3 days, and expression is
still annotated *at* protruding-mouth — which is 3 dpf, the stage at which the claim says signal has
faded. Separately, a search summary of the 2011 figure data describes `zfprrx1a` CNE line #2 imaged
at **27 hpf** with EGFP "faintly expressed in the pectoral fins", not ~30 hpf.

**I am not calling this a refutation.** ZFIN stage annotations record where a curator saw signal, not
where the authors claimed demonstrated *specificity*, and the two can legitimately differ; and I
could not reach the 2011 full text (host blocked, §0). **Flagged discrepancy requiring full-text
resolution:** the claim's "only to ~30 hpf" versus a 24–72 hpf curated annotation. If the annotation
is right about signal persisting to protruding-mouth, the temporal half of the claim's disqualifier
for its own best candidate is wrong.

---

## 2. The proxy problem — three substitutions, one of them a non-sequitur

### 2a. Reporter domain stands in for the domain in which an edit is driven

This is the central proxy. The quantity that matters for "adequate to drive the edits" is the
**cumulative set of cells in which the edit is actually made** — for Cre/CreERT2 the recombined
lineage, for Cas9 the set of cells reaching editing-competent nuclease levels. The claim measures
instead the **instantaneous reporter expression domain at the stages imaged**. These diverge in both
directions, and the claim gets one in each direction wrong:

- Against the elements: a *transient* off-target domain becomes a *permanent* label under a
  recombinase. CNS12's dorsal-eye activity is a worse problem for a Cre driver than the claim's
  phrasing implies, because lineage recording does not care that the activity was brief.
- For the elements: "signal fading by 3 dpf" is close to **irrelevant** to a recombinase-based
  strategy, which has already written the edit by then. The claim deploys fading as a disqualifier
  without stating which driver modality it is disqualifying. It is a real objection for direct
  Cas9/transactivator approaches and a weak one for Cre.

**The right quantity, and its status:** a published fate-map of each element's *recombined* domain,
scored in caudal and median fins. **I found none for any element in the claim's list** (scope in
§5). My inference: that is a cleaner and stronger statement of the gap than the reporter census is,
because it is uncontaminated by the modality ambiguity above.

### 2b. Dispensability stands in for inadequacy — this one is a non-sequitur

The claim disqualifies `tbx5a` CNS12 partly because it "is dispensable for fin formation". That is a
**necessity** result; "adequate to drive the edits" is a **sufficiency** question. Deleting an
element and seeing normal fins (*Cell Reports* 2018: the zebrafish `cns12sh` element, reported as a
~200 bp region, deletion mutants with normal pectoral fins; read-level: search-summary) says nothing
about whether that element can drive a payload.

And the published evidence on CNS12 points the *other* way on sufficiency: the PNAS 2016 work
reports that CNS12 driving `tbx5a` **partially rescues the *heartstrings* (*hst*) mutant**, which
lacks pectoral fin and girdle (read-level: search-summary). **My inference:** that is a direct
published demonstration that this element can drive a functional transgene in pectoral fin tissue
well enough to change morphology — which is exactly the capability "adequate to drive the edits"
asks about. The dispensability clause should be struck; CNS12 is disqualified by its dorsal-eye
activity alone, and its sufficiency credential is better than the claim lets on.

Note also an unreconciled size disagreement I am preserving rather than averaging: PNAS describes
CNS12 as a **3,108 bp** element (the gar sequence tested in zebrafish); *Cell Reports* describes
`cns12sh` as **~200 bp**, ~100 kb downstream. Both read-level search-summary. Whether these are the
same element at two resolutions is not settled by anything I could access.

### 2c. Endogenous gene expression stands in for reporter activity

The claim states "prrx1a reporters also label pharyngeal arch". What I could verify is that the
**endogenous** gene is arch-expressed: at 24 hpf `prrx1a` expression is reported in pectoral fin buds
and in a rostral domain corresponding to the branchial arches (read-level: search-summary). I could
**not** verify at any read-level that the `prrx1a` **CNE reporter** drives arch expression; the
sources I reached describe the CNE lines as fin reporters, and one states that pectoral expression
driven by the `zfprrx1b1` CNE is indistinguishable from that driven by `zfprrx1a`. The 2011 full text
is behind a host this session cannot resolve (§0).

**Status: unverified, not refuted.** The claim may well be right — an enhancer of an arch-expressed
gene plausibly carries arch activity. But as recorded, this disqualifier reads as a reporter result
and the evidence I can reach is a gene-expression result. That is the same proxy slip as 2a, applied
to a different element.

---

## 3. The hidden assumption that carries the result, relaxed

**The assumption:** that adequacy is established by, and only by, a published negative control in
caudal and median fins.

Relaxed, it fails in both directions:

- **Insufficient.** An element can clear a perfect specificity bar and still be inadequate on
  **output level, onset timing, mosaicism, or copy number**. The *Current Biology* work supplies a
  published instance of exactly this: zebrafish `LARM1s` (164 bp) drives pectoral fin expression, but
  **two copies in tandem increased fin GFP signal over a single copy** (read-level: full-text
  partial). My inference: single-copy output from a short pectoral element can be marginal, so a
  specificity-only screen does not measure adequacy at all. The claim's "adequate" is doing work its
  evidence does not reach.
- **Unnecessary.** Whether leaky median-fin activity is disqualifying depends on the readout. If the
  experiment scores pectoral morphology or a pectoral molecular phenotype and uses median fins as
  *internal* controls, median activity is a confound only where the edit acts on tissue the assay
  reads. The claim applies an absolute specificity bar without naming the readout it is a bar for.

**Consequence for the record:** "0 adequate" is not a measurement. It is the conjunction of a
specificity census with an **unstated adequacy threshold**. Both conjuncts need stating for the
number to mean anything, and neither is in the recorded claim.

**The terminological wrinkle that matters:** the caudal fin *is* a median fin. "Caudal and median
fins" is therefore redundant on its face, and the only coherent reading is that "median" here means
dorsal + anal. I adopt that reading below, and it is the reading under which the KEY number is
testable at all.

---

## 4. Is the evidence level honest?

`literature` is the right *kind* of level. Two defects in the record regardless:

1. **A derived census number carried as `value: n/a`.** The KEY is a number — 0 — produced by a
   literature survey. The record reports `n/a`, which hides that a count is being asserted. Under
   this project's floor, a count produced by searching is derived, and should say so.
2. **No search scope stated beside a negative.** The floor says "state the scope of every negative
   search beside the finding". The claim states none: no databases, no date cut, no query set, no
   statement of which gene loci were swept. **My inference, and it is the load-bearing one in this
   review:** the scope was narrow, and specifically appears to have been restricted to elements at
   *fin-initiation* genes (`tbx5`/`hand2`/`prrx1`). It missed elements at *patterning* genes (`shh`,
   `lmx1b`) and at *fin-fold* genes (`and1`). I reached the decisive counter-example within two
   queries from a cold start (§5), which is weak but real evidence that the original sweep was not
   exhaustive over the indexed literature.

---

## 5. The counter-examples the author missed

**Scope of my search, stated as required:** WebSearch (US index) in "extended" mode, 2026-11-04,
eight queries, English only, targeting zebrafish/mouse pectoral-fin enhancers and reporter lines by
gene symbol (`tbx5a`, `hand2`, `prrx1a`/`Prx1`, `shh`/ZRS, `lmx1b`/LARM, `fgf24`, `sp9`, `dlx5a`,
`and1`, `Pitx1`) plus ZFIN records. Full text reached for two sources only (§0). **This is not a
systematic review.** Non-teleost taxa (skate, catshark, lamprey) were not swept; a wider or
full-text sweep could surface further elements in either direction.

### 5a. LARM / holo-LARM — the one that breaks the KEY number

A named, published cis-regulatory module at `lmx1bb` with **both** pectoral reporter activity **and**
an explicit median-fin negative control.

From the *Current Biology* 2026 paper (read-level: full-text, partial):

- **Pectoral reporter activity.** LARM orthologues from several gnathostome species, cloned upstream
  of a minimal promoter driving GFP, drove reporter expression "in a similar pattern in the
  developing pectoral fins". Zebrafish `LARM1s` "contains regulatory information to drive pectoral
  fin expression". The authors counted an enhancer verified only when **≥3 independent stable lines**
  showed consistent expression — a stricter specificity standard than the 2011 Prx1 work the claim
  calls its best candidate.
- **Pectoral requirement.** A 6,845 bp holo-LARM deletion (chr8:33400177–33407021, 8 bp scar)
  abolishes pectoral `lmx1bb` at 48 hpf and produces double-ventral pectoral fins with ectopic dorsal
  flanges (n=10, 100%).
- **The median-fin negative control.** "dorsal fin lmx1bb expression was unaffected in LARM
  Δ6.8kb/Δ6.8kb zebrafish", and "the skeletal form of the dorsal fin in the mutants was also
  unaffected". The authors state the specificity conclusion themselves: LARM regulation is specific
  to paired appendages.

**Therefore the KEY count of 0 is false under the only coherent reading of its own words.** A named
element has had its activity tested explicitly against a median fin, with a published negative
result, in the same figure series as its positive pectoral result.

**What the counter-example does *not* do — and I am being careful here, because this is where a
manufactured kill would sit:**

- LARM is **not pectoral-restricted**. It is paired-appendage. The 2026 bioRxiv version reports the
  `lmx1b` deficit in **pectoral and pelvic** fins (read-level: search-summary). Zebrafish have pelvic
  fins, so LARM fails the claim's headline requirement for the same reason the claim's own `hand2`
  entry does.
- The median-fin negative is a **deletion/necessity** negative, not a **reporter/sufficiency**
  negative. The *Current Biology* text reports reporter assays **in pectoral fin only**; no reporter
  activity was assayed in dorsal, anal or caudal fins. So the element has not been shown unable to
  *drive* in median fins — only that median fins do not *require* it.
- **Caudal fin was not examined**, at either read-level. The claim's caudal half stands.
- The authors themselves flag the alternative explanation: the absence of a dorsal/anal effect "may
  reflect lmx1b enhancer redundancy", a hypothesis they say still needs testing. A redundancy-masked
  negative is not a specificity demonstration.

**Disagreement between sources, preserved not averaged:** the 2025 bioRxiv abstract states LARM is
dispensable for the unpaired **dorsal and anal** fins; the *Current Biology* full text I read reports
the zebrafish dorsal fin only and does not examine anal or caudal fins. I do not know which is
right and have not resolved it.

### 5b. shh ZRS + sZRS — a second missed element, and it goes the author's way

Letelier et al. 2018 *Nat Genet* (read-level: search-summary): deleting both ZRS and its shadow
enhancer sZRS abolishes `shh` and completely truncates pectoral fin formation; the authors conclude a
ZRS–Shh regulatory module is **shared by paired and median fins**. So this is a named element with
pectoral activity whose median-fin status was explicitly addressed — and the answer is that it is
*not* pectoral-restricted. Missing from the census; consistent with the conclusion; inconsistent with
the KEY count read as "0 tested".

### 5c. and1 (actinodin1) ectodermal enhancer — a third

Reported to drive expression in the ectoderm of **median and pectoral** fin folds (read-level:
search-summary). Again: median fins explicitly in scope, specificity explicitly fails.

**My inference across 5a–5c:** median-fin co-activity is the *published norm* for fin enhancers, not
an untested gap. That makes the author's prose conclusion more secure than the author argued for it,
while making the KEY framing ("nobody has tested") wrong. The honest statement is "tested repeatedly;
specificity fails every time it is tested", which is a different and better finding.

### 5d. A constructive lead the census shape rules out

Chan et al. 2010 *Science* (read-level: search-summary): the stickleback `Pitx1` `Pel` enhancer is a
tissue-specific enhancer for hindfin expression, and `Pel`-driven `Pitx1` restores pelvic development
in pelvic-reduced fish. This is **pelvic, not pectoral**, so it is not a counter-example to the claim.
I include it because it demonstrates that a *fin-type-restricted, functionally sufficient* enhancer is
an attainable object in fish, and because the search pattern that finds it — appendage-type-identity
genes, not fin-initiation genes — is the pattern the author's census did not run. I did not verify
whether `Pel` was ever scored in median fins.

---

## 6. What survives

The prose conclusion — **no published pectoral-restricted regulatory element is adequate to drive the
edits** — survives. I tried three routes to break it and all failed:

- The claim's "best candidate" is not the best candidate (LARM has a stricter verification standard
  and an actual median-fin control), but LARM is paired-appendage, so substituting it does not produce
  a pectoral-restricted element.
- CNS12's sufficiency credential is better than the claim allows (*hst* partial rescue), but its
  dorsal-eye activity is uncontested and is a lineage-permanent problem under a recombinase.
- No element I found has a published **caudal**-fin control, and none has a published reporter-level
  median-fin negative.

What does not survive is the KEY number and parts of the supporting argument.

## 7. Corrections the record needs

1. **KEY, corrected:** **≥1** named element (LARM / holo-LARM at `lmx1bb`) has a published explicit
   median-fin (dorsal fin) negative control; **0** have a published caudal-fin control; **0** have a
   published *reporter-level* median-fin negative; **0** are pectoral-restricted (LARM is
   paired-appendage, pelvic fin in scope). Count scope: the §5 search scope, which is not systematic.
2. **Strike the dispensability clause** from the CNS12 disqualifier — necessity does not bear on
   sufficiency — and record the *hst* partial-rescue result on the other side of the ledger.
3. **Downgrade the prrx1a arch disqualifier to unverified**, or re-source it: what I can reach is
   endogenous-gene arch expression, not CNE reporter arch activity.
4. **Resolve the 24–72 hpf ZFIN annotation against "only to ~30 hpf"** from the 2011 full text. Needs
   `anatomypubs.onlinelibrary.wiley.com` allow-listed in this session's network settings, or another
   full-text route.
5. **De-duplicate the census** (items 3 and 4 are one study) and **re-run it over patterning and
   fin-fold loci** (`shh`, `lmx1b`, `and1`), not only fin-initiation loci.
6. **Record the search scope beside the count**, and mark the KEY as derived rather than `n/a`.
7. **Restate the gap in the quantity that matters:** no published fate-map of any candidate element's
   *recombined* domain scored in caudal and median fins. That negative is cleaner than the reporter
   census and is not weakened by any counter-example I found.

```swarm-challenge
{"claim_id": 204, "outcome": "weakened", "reason": "The prose conclusion that no pectoral-restricted element adequate to drive the edits is published survives, but the KEY count of 0 is refuted: the LARM/holo-LARM module at lmx1bb has published pectoral reporter activity plus an explicit dorsal-fin (median) negative control the census missed, and two further disqualifiers in the claim are a necessity-for-sufficiency non-sequitur (CNS12 dispensability, against a published hst partial rescue) and an unverified gene-for-reporter substitution (prrx1a pharyngeal arch).",
  "corrected_value": "KEY corrected: >=1 named element (LARM/holo-LARM at lmx1bb) with a published explicit median-fin negative control; 0 with a published caudal-fin control; 0 with a reporter-level median-fin negative; 0 pectoral-restricted (LARM is paired-appendage, pelvic fin in scope). Count scope: 8 extended web searches, 2026-11-04, zebrafish/mouse, gene-symbol-targeted, 2 sources read at full text; not systematic.",
  "depends_on": ["harvest:s16-pectoral-regulatory-element-czmhrn", "lit:currentbiology-2026-dorsal-determination-larm-PMC13348734", "lit:biorxiv-2025.07.02.662459-larm-PMC12236613", "lit:biorxiv-2026.02.08.704681-larm-pectoral-pelvic", "lit:letelier-2018-natgenet-zrs-szrs-paired-median-fins", "lit:pnas-2016-tbx5-cns12-dorsal-eye-hst-rescue", "lit:cellreports-2018-cns12sh-knockout-nonessential", "lit:hernandez-vega-minguillon-2011-devdyn-prx1-limb-enhancers", "zfin:TGCONSTRCT-111115-31-prrx1a-EGFP-ib4Tg-ib5Tg", "zfin:FIG-110804-50-stage-range-prim5-protruding-mouth", "lit:hand2-cre-creert2-knockin-2024-lineage-labeling", "lit:nature-2023-median-fin-lpm-hand2-paff", "lit:and1-actinodin1-ectodermal-enhancer-median-pectoral", "lit:chan-2010-science-pitx1-pel-enhancer", "assumption:caudal-fin-is-a-median-fin-so-median-reads-as-dorsal-plus-anal", "assumption:adequacy-threshold-for-driving-edits-is-unstated-in-the-claim"]
}
```
