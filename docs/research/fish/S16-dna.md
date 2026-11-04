# S16 — Is there a pectoral-restricted regulatory element to drive the edits?

Project: `zebrafish-flight`. Scale: **dna**. Date of search: 2026-11-04.

> **Access caveat, stated up front because it sets the ceiling on this whole file.**
> This session's network policy resolved `pubmed.ncbi.nlm.nih.gov`, `zfin.org`,
> `anatomypubs.onlinelibrary.wiley.com` and `www.pnas.org` to nothing
> (`getaddrinfo ENOTFOUND`). Every attempt at primary full text failed. **No source
> below is read at `full-text`.** Everything is `search-summary`: a web-search
> engine's summary of the page, including the passages it quoted verbatim from
> abstracts, ZFIN figure captions and ZFIN construct records. Quoted strings
> reproduced here are quotes *of the search summary's quote*, one indirection
> removed from the paper. Any number or specificity claim in this file needs
> re-reading at `full-text` before it is load-bearing.

---

## 1. The question, restated precisely

The design calls for enlarging the pectoral fin pair. The failure mode is not that the
edit does not work; it is that it works everywhere. Zebrafish fin-size mutants are the
proof: the two best-characterised fin-overgrowth alleles enlarge **all** fins at once.

So S16 is not "can fin size be increased" (it demonstrably can). S16 is a narrower
genetic-engineering question with three conjoined requirements, and the design is a
lethal unless all three hold:

1. **Spatial restriction.** An element driving in pectoral fin and *not* in the median
   fin fold, dorsal fin, anal fin, or caudal fin. Caudal and median fin overgrowth is
   the direct route to a fish that cannot swim — the caudal fin is the thrust surface.
2. **Temporal reach.** The pectoral fin reaches adult form at ~15 mm standard length
   ([Patterson et al. 2008](https://anatomypubs.onlinelibrary.wiley.com/doi/10.1002/dvdy.21400),
   `search-summary`: "by 15 mm, the zebrafish pectoral fin has largely developed into
   its adult form"). An element active only across the fin-bud window (~18–48 hpf) can
   change bud scale but cannot drive the *allometric* growth phase where a 30-fold area
   change would have to be paid for.
3. **Magnitude tolerance.** The element must sustain enough expression to carry a large
   area change, not merely mark the tissue for microscopy. Reporter-grade specificity
   and driver-grade output are different requirements and the literature below only
   ever tests the first.

**The numbers that make it hard.**

| Quantity | Value | Status |
|---|---|---|
| Body mass (project brief) | ~0.4 g | given |
| Body length (project brief) | ~4 cm | given |
| Wing area needed for a 3 m/s glide | 7.1 cm² total (see §3) | **computed** |
| Current adult pectoral fin planform area | **unknown** | see §2.6 |
| Required fold-change in pectoral area | **not computable** — denominator unknown | see §3 |
| Named elements found with any published pectoral reporter specificity | 4 | §2 |
| Of those, number with specificity demonstrated against caudal/median fins explicitly | **0** | §2.7 |
| Of those, number with specificity demonstrated beyond ~3 dpf | **0** | §2.7 |
| Of those, number shown to be *necessary* for pectoral fin formation | **0** (one shown *not* necessary) | §2.3 |

The last three rows are the answer to S16, and they are all zeroes.

---

## 2. What is measured

### 2.1 The Prx1/prrx1a limb enhancers — the strongest candidate

Hernández-Vega A, Minguillón C. "The Prx1 limb enhancers: targeted gene expression in
developing zebrafish pectoral fins." *Developmental Dynamics* 240(8):1977–88, 2011.
Read-level: **search-summary** (abstract text and ZFIN figure/construct captions, via
search; `anatomypubs.onlinelibrary.wiley.com` and `zfin.org` both unreachable).

**Author claims, as quoted by the search summary:**

- They "generated zebrafish lines that express enhanced green fluorescent protein
  (EGFP) driven by the mouse Prx1 enhancer in developing pectoral fins."
- They "identify three conserved non-coding elements (CNEs) that we use to generate
  fin-specific EGFP reporter lines."
- Reporter signal labels "the endoskeletal disc, the scapulocoracoid, and migrating
  mesenchymal cells in the pectoral fin fold," and is "much fainter by 3 dpf."
- "Expression in this transgenic line is very pectoral fin-specific until at least
  30 hpf."
- "Within the bud, expression is restricted to the posterior-most area of the fin bud
  mesenchyme."

**Identifiers, read-level `search-summary` and internally inconsistent across records:**

- Alleles: `ib4Tg`, `ib5Tg`. ZFIN stage range given as Prim-5 → Protruding-mouth.
- ZFIN construct record title: `Tg(prrx1a:EGFP)` (ZDB-TGCONSTRCT-111115-31).
- ZFIN figure caption for the same alleles: "The zfprrx1aCNE (cFos):EGFP transgenic
  lines" — i.e. a zebrafish *prrx1a* CNE on a cFos minimal promoter.
- A separate line, `Tg(mPrx1(cFos):EGFP)`, is described in other work as labelling
  "fin mesenchyme… driven by the mouse prx1 enhancer from 26 hpf onwards."

**Disagreement preserved:** the ZFIN construct name (`prrx1a:EGFP`) and the ZFIN figure
caption (`zfprrx1aCNE(cFos):EGFP`) describe different construct architectures for the
same two alleles, and the paper reports *both* a mouse Prx1 enhancer line and zebrafish
prrx1a CNE lines. **Which element sits in `ib4Tg` versus `ib5Tg` is `unknown` to me.**
I could not open the Methods. This is not a trivial bookkeeping gap: a cross-species
mouse enhancer and a native zebrafish CNE are different reagents with different
specificity risk.

### 2.2 Counter-evidence against prrx1a specificity: pharyngeal arch expression

This is the material that bears directly on the refutation criterion, and it is
substantial.

- *Nature Communications* 2026, alx gene family / frontonasal CNC study
  ([link](https://www.nature.com/articles/s41467-026-74434-w), `search-summary`):
  "the prrx1a:RFP expression boundary marks the frontonasal-to-pharyngeal arch one
  border," and the reporter "labels the maxillary region of arch one." Endogenous
  *prrx1a* is "strongly expressed across many cranial neural crest cells in the
  anterior and posterior arches."
- Competition between Jagged-Notch and Endothelin1 signaling, PMC4825933
  (`search-summary`): two-colour in situ at 36 hpf places *prrx1a* and *prrx1b* "in
  dorsal arch neural crest cells and the mesenchyme around the ear," plus a ventral
  arch domain.
- Posterior neural-crest single-cell atlas, *eLife* 2020
  ([link](https://elifesciences.org/articles/60005), `search-summary`): *prrx1a/b* is a
  mesenchymal marker with HCR signal "in the posterior arches and fin bud."

**My inference, not the authors' claim:** a `prrx1a:RFP` reporter labelling arch-one
maxillary mesenchyme is a reporter-level demonstration that *a* prrx1a regulatory
reagent drives non-pectoral expression. It does not by itself convict `ib4Tg`/`ib5Tg`,
because the `prrx1a:RFP` construct in the 2026 paper may contain different regulatory
sequence than the 2011 CNEs. **But it removes the right to assume prrx1a-derived
elements are appendage-restricted**, and it means the 2011 "very pectoral fin-specific"
claim has to be read as scoped to the stages and the construct that paper tested.

### 2.3 tbx5a CNS12 / cns12sh — named, and explicitly not fin-restricted

- Adachi N. et al., "Regulatory evolution of Tbx5 and the origin of paired appendages,"
  *PNAS* 2016 ([doi 10.1073/pnas.1609997113](https://www.pnas.org/doi/10.1073/pnas.1609997113)),
  read-level **search-summary** (`www.pnas.org` unreachable). The search summary
  reports: CNS12 is "a 3,108-bp fin enhancer downstream of Tbx5"; "CNS12 drove GFP
  expression in the **dorsal part of eye and pectoral fin**"; enhancer activity "is
  evolutionarily conserved among jawed vertebrates and is able to rescue the finless
  phenotype of tbx5a mutant zebrafish." Also: of four stable lines made from a
  CNS59-type element, "GFP expression was undetectable in the pectoral fin."
- *Cell Reports* 2018, "Genomic Knockout of Two Presumed Forelimb Tbx5 Enhancers
  Reveals They Are Nonessential for Limb Development"
  ([PDF link](https://www.cell.com/cell-reports/pdf/S2211-1247(18)30798-8.pdf)),
  read-level **search-summary**. CRISPR deletion of 772 bp including `cns12sh` (and a
  357-bp allele) left "normal forelimb buds." The authors' stated conclusion, as
  quoted: reporter transgenes "may not identify endogenous enhancers" and in vivo
  loss-of-function is required.

**This is the single most useful result in the file.** CNS12 is a *named* element with
*published* fin reporter activity — exactly what the "what would settle it" criterion
asked for — and the same literature reports (a) it also drives dorsal eye, so it is not
pectoral-restricted, and (b) deleting it does not affect fin development, so it is not
the endogenous controller of the trait being edited.

### 2.4 hand2 — pectoral fin included, restriction absent

- `TgBAC(hand2:EGFP)`: a BAC line, reported to "accurately recapitulate endogenous
  hand2 gene expression," with EGFP in larval pectoral fins at 2–3 dpf
  (*Nature* 2023 median-fin/LPM paper, [link](https://www.nature.com/articles/s41586-023-06100-w),
  `search-summary`).
- *Nature Communications* 2019 ([link](https://www.nature.com/articles/s41467-019-11561-7),
  `search-summary`): hand2:EGFP "demarcates the lateral-most PLPM domain plus parts of
  the ALPM-derived heart field and pectoral fin precursors."
- *Nature Communications* 2022, mesothelium/mesothelioma
  ([link](https://www.nature.com/articles/s41467-022-29311-7), `search-summary`):
  hand2 delineates mesothelium progenitors.
- hand2 Cre / CreERT2 CRISPR knock-ins, 2024
  ([preprint PDF](https://www.biorxiv.org/content/10.1101/2024.12.04.626907.full.pdf);
  [PMC11643050](https://pmc.ncbi.nlm.nih.gov/articles/PMC11643050/), `search-summary`):
  "strong GFP expression in the heart and fin buds at 2 dpf"; lineage includes
  "mesodermal components of the branchial arches, heart, pelvic fin and pre-anal fin
  fold."
- Yelon et al. 2000, *Development* 127(12):2573 (`search-summary`): the *hands off*
  locus encodes Hand2, required for both heart and pectoral fin.

**No restriction.** hand2 reagents label heart, mesothelium, branchial arches, pelvic
fin and pre-anal fin fold. The pre-anal fin fold hit is the design-relevant one: that
is median-fin territory. I searched specifically for a "−9.3 kb hand2 enhancer" or a
`Tg(-9.3hand2:GFP)` construct and **found no such element**; the fin-expressing hand2
reagents retrieved are BAC or knock-in, i.e. the whole locus, which is the opposite of
restricted.

### 2.5 fgf24 and the fin-initiation cascade — not restricted

`search-summary` throughout.

- fgf24 is "a marker of early pectoral fin bud mesenchyme," acts "downstream of tbx5 to
  activate fgf10 expression in the lateral plate mesoderm," and at 34 hpf is reported in
  "the AER/AF" rather than only mesenchyme
  ([*Development* 139:2916](https://journals.biologists.com/dev/article/139/16/2916/45235/Mechanism-of-pectoral-fin-outgrowth-in-zebrafish)).
- Draper et al. 2003 is titled "Zebrafish fgf24 functions with fgf8 to promote
  **posterior mesodermal** development" ([PMID 12925590](https://pubmed.ncbi.nlm.nih.gov/12925590/)) —
  a non-fin function named in the title.
- dlx5a/dlx6a: "essential for the induction of pectoral fin outgrowth, but are not
  required during median fin fold specification"
  ([PMC4032342](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4032342/)). Note this is a
  *requirement* asymmetry, not an expression restriction, and dlx5a/6a are also
  Meckel's-cartilage genes ([PMC10526740](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10526740/)).

**Negative search, scope stated:** I searched for fgf24 expression in median fin fold
and tail bud and retrieved no in situ panel either way. The ZFIN figure for Fischer
et al. 2003 lists only "pectoral fin bud ectoderm, pectoral fin bud mesenchyme" — but
that is one figure's annotation, not a whole-embryo negative. Given the 2003 title, I
treat fgf24 as **not** pectoral-restricted, and I mark that as my inference from a
title, which is weak evidence.

### 2.6 Whole-animal fin overgrowth: the failure mode, measured

- *another longfin* (`alf`) is a gain-of-function mutation in the two-pore K⁺ channel
  **kcnk5b**, producing allometric fin overgrowth; Perathoner et al. 2014,
  *PLOS Genetics* ([link](https://journals.plos.org/plosgenetics/article?id=10.1371%2Fjournal.pgen.1004080),
  `search-summary`). A non-conductive variant failed to produce overgrowth. Reported as
  "coordinated growth of fins **and barbels**."
- `longfin` (`lof^t2`) is a *different* channel: "cis-ectopic expression of kcnh2a"
  ([preprint PDF](https://www.biorxiv.org/content/10.1101/790329.full.pdf),
  `search-summary`).
- *Scientific Reports* 2018 ([link](https://www.nature.com/articles/s41598-018-28450-6),
  `search-summary`): local overexpression of wild-type kcnk5b "is also sufficient to
  induce overgrowth," with "localized fin and barbel overgrowth in mosaic clones."
- Loss of kcnk5b alone "had little effect on fin phenotype"
  ([bioRxiv 621243](https://www.biorxiv.org/content/10.1101/621243v1.full), `search-summary`).

**Disagreement preserved:** sources differ on whether kcnk5b overgrowth is uniform
across a fin or patterned within it. I do not average this; both readings are in the
literature and they imply different things about how cleanly a restricted driver would
translate into a specific shape.

**The mosaic result matters and cuts the other way from everything above.** If local
kcnk5b overexpression in a clone produces local overgrowth, then the *effector* is
cell-autonomous enough that a restricted driver would in principle suffice. The
bottleneck is therefore located squarely in the driver, not the effector. That is a
genuinely useful narrowing.

### 2.7 Pectoral fin planform area — unknown

I could not retrieve a measured adult pectoral fin area for *Danio rerio*.
**Scope of the negative search:** one `extended` web search on adult pectoral fin area /
morphometrics / fin size in mm², plus the incidental hits from six other searches. What
came back instead: fin-bud area normalised to eye area within the same embryo
([PMID 38527087](https://pubmed.ncbi.nlm.nih.gov/38527087/), `search-summary`); an adult
microCT morphometrics pipeline that measures standard length, lean volume and fineness
ratio but "doesn't address fin area"
([PMC13432094](https://pmc.ncbi.nlm.nih.gov/articles/PMC13432094/), `search-summary`);
and a methodological warning that "the depth and opacity make it difficult to image in
the adult" at the fin base
([*Development* 149:dev199676](https://journals.biologists.com/dev/article/149/5/dev199676/274591/Anatomy-and-development-of-the-pectoral-fin),
`search-summary`). Not searched: ZFIN's own measurement records (host unreachable),
morphometric theses, or fin-regeneration papers that may report baseline areas
incidentally. Marked `unknown`, not estimated.

---

## 3. What I computed

**This section is computation, not observation.** No value in it was measured by anyone.

### 3.1 Wing area required for a 3 m/s glide

Assumptions, all stated as assumptions:

- `W = m·g` with `m = 0.4 g = 4.0e-4 kg`, `g = 9.81 m/s²` → `W = 3.92e-3 N`.
- Air density at sea level, `ρ = 1.225 kg/m³`.
- `C_L = 1.0`. This is an *assumed* maximum lift coefficient for a thin, roughly flat
  membrane at the chord Reynolds numbers in play; it is not measured for fish fins and
  is, if anything, generous.
- Steady gliding, lift ≈ weight, rigid planform.

Lift equation `L = ½·ρ·V²·S·C_L`, set `L = W`, solve for `S`:

```
S = 2W / (ρ · V² · C_L)
  = 2 (3.92e-3 N) / (1.225 kg/m³ · (3 m/s)² · 1.0)
  = 7.84e-3 / (1.225 · 9.0)
  = 7.84e-3 / 11.025
  = 7.11e-4 m²
  = 7.11 cm²   (total, both wings)
  ≈ 3.6 cm² per side
```

### 3.2 The fold-change, which is the number S16 actually needs

```
fold-change = 7.11 cm² / (current pectoral planform area, both fins)
            = 7.11 cm² / unknown
            = NOT COMPUTABLE
```

I decline to supply a plausible-looking denominator. A 4 cm fish has pectoral fins on
the order of a few millimetres on a side, which would put the fold-change somewhere in
the tens; writing a specific number for it would be inventing a measurement, which the
honesty floor forbids. **The decisive magnitude is therefore blocked on one
measurement** (§6.1), and that measurement is cheap.

### 3.3 Temporal mismatch — arithmetic on the published windows

The one specificity claim with a stated bound is prrx1a: "very pectoral fin-specific
until at least 30 hpf," with reporter "much fainter by 3 dpf" (§2.1). Adult pectoral fin
form is reached by ~15 mm SL (§1), which in standard rearing is on the order of weeks,
and allometric fin growth continues past that.

```
window of demonstrated specificity:        ~30 hpf      = 1.25 d
window over which fin area must change:    ≳ 15 mm SL   = weeks
ratio of demonstrated to required duration: ~1.25 d / ~30 d  ≈ 4%
```

The "~30 d" figure is my own order-of-magnitude stand-in for time-to-15-mm, not a
sourced rearing curve, so the ratio is illustrative arithmetic only. The qualitative
conclusion survives any reasonable substitution: **the demonstrated specificity window
covers a small single-digit-to-low-double-digit percentage of the growth period the
design needs**, and the reporter is explicitly fading at the end of it.

---

## 4. The answer

**Evidence level: `literature` (negative).**

**No.** Named pectoral-fin regulatory elements exist in the published zebrafish
literature, but none of them is a pectoral-*restricted* driver in the sense this design
requires, and for every candidate the restriction claim either fails on the published
data or was never tested in the direction that matters.

Element by element:

| Element / reagent | Pectoral expression published? | Restricted? | Evidence against |
|---|---|---|---|
| `Tbx5`/`tbx5a` **CNS12** (3,108 bp, downstream) | yes | **no** | also drives **dorsal eye**; and `cns12sh` deletion leaves fins normal |
| mouse **Prx1 limb enhancer** (`Tg(mPrx1(cFos):EGFP)`) | yes, from ~26 hpf | partial, bounded | fades by 3 dpf; arch risk from prrx1a reagents |
| zebrafish **prrx1a CNEs** (`ib4Tg`, `ib5Tg`) | yes | **bounded to ≤30 hpf** | a `prrx1a:RFP` reporter labels arch-one maxillary mesenchyme |
| **hand2** BAC / Cre knock-ins | yes | **no** | heart, mesothelium, branchial arches, pelvic fin, **pre-anal fin fold** |
| **fgf24**, **dlx5a/6a** | yes | **no** | posterior mesoderm (fgf24); Meckel's cartilage (dlx5a/6a) |
| `CNS59`-type Tbx5 elements | **no** — 4 stable lines, GFP undetectable in fin | n/a | n/a |

The strongest honest statement the literature supports is the Prx1/prrx1a one, and it
is: *a mouse Prx1 limb enhancer and zebrafish prrx1a CNEs drive EGFP in pectoral fin
bud mesenchyme, reported as "very pectoral fin-specific until at least 30 hpf," with
signal much fainter by 3 dpf* — one paper, reporter-level, read at `search-summary`,
with the construct-to-allele mapping unresolved and with independent reports of
prrx1a-reporter expression in pharyngeal arch.

**Key number: 0** — the number of named elements with published specificity tested
*explicitly against caudal and median fins*, which is the test the design needs.

The refutation criterion set in the brief is met for the named elements, by the
literature itself: CNS12 drives dorsal eye; hand2 reagents drive pre-anal fin fold and
pelvic fin; prrx1a reporters drive pharyngeal arch. The brief said evidence of
non-pectoral expression would refute the answer. It does, and I am reporting that rather
than retaining a feasibility claim.

---

## 5. What this does NOT establish

This is the part I expect to be read hardest, so I will be generous with it.

1. **It does not establish that no such element exists.** It establishes that I did not
   find one in twelve web searches with zero full-text access. ZFIN — the single most
   likely place for a systematic answer, since it indexes expression by anatomical term
   and could in principle be queried for constructs annotated `pectoral fin` and *not*
   `caudal fin` — was unreachable. That query has not been run. An absence under this
   search is weak evidence of absence.

2. **It does not establish that the published elements are non-restricted, only that
   their restriction is unproven or contradicted.** Specifically: the 2026
   `prrx1a:RFP` arch result may involve different regulatory sequence from
   `ib4Tg`/`ib5Tg`. I could not check. Treating it as convicting those two alleles would
   overstate my evidence. What I claim is weaker and defensible: nobody has published
   the caudal/median-fin negative control for them.

3. **It does not establish the construct contents of any line named here.** Whether
   `ib4Tg` carries the mouse Prx1 enhancer or a zebrafish prrx1a CNE on a cFos promoter
   is `unknown` to me; ZFIN's construct title and its own figure caption disagree, and
   the paper's Methods were inaccessible. Do not order a reagent on the basis of this
   file.

4. **It does not establish that reporter specificity would transfer to a driver.** The
   *Cell Reports* 2018 authors make this point themselves about CNS12: reporter
   transgenes "may not identify endogenous enhancers." A fragment that is clean at
   reporter copy number and reporter expression level may not be clean when driving an
   effector hard enough to change organ size. There is no published test of that for any
   element here.

5. **It does not establish the required magnitude.** §3.2 is non-computable because
   adult pectoral planform area is `unknown`. The whole design may need a 10× area
   change or a 100× one, and those are different engineering problems with different
   specificity tolerances — a 100× change leaks phenotype much more readily.

6. **It does not address pelvic fins at all.** The hand2 lineage data mention pelvic
   fin. A driver that hit pectoral *and* pelvic is a different, possibly survivable
   design; I have not evaluated it, and S16 as posed did not ask.

7. **It says nothing about whether an enlarged pectoral fin would glide.** The 7.11 cm²
   in §3.1 is a lift-equation inversion under an assumed `C_L`, at a velocity (3 m/s)
   that I chose to make the arithmetic legible and that is **well above** any swimming
   speed a 4 cm zebrafish is reported to reach. Launch velocity is another subproblem's
   problem, and on the face of it a harder one than this one.

8. **It does not establish that the kcnk5b/kcnh2a route is the right effector.** §2.6 is
   cited to characterise the failure mode (all-fin overgrowth) and to locate the
   bottleneck in the driver. Whether a K⁺-channel effector, a Hox effector
   ([Hawkins, Henke & Harris 2021, *Cell* 184(4):899–911](https://www.cell.com/cell/fulltext/S0092-8674(21)00003-9),
   `search-summary` — activating `vav2`/`waslb` mutations produce Hox11-dependent
   "intermediate radials" in the pectoral fin), or something else is correct is outside
   S16.

9. **The Hawkins 2021 result is a caution, not a solution.** It reports a
   pectoral-*localised phenotype* from mutations in genes with no prior appendage
   association — i.e. restriction can arise from the pathway's own context-dependence
   rather than from a restricted driver. That is interesting and I flag it as the most
   promising unexplored direction, but a localised phenotype in a point mutant is not a
   reusable regulatory element, and I have not verified the phenotype's restriction
   against caudal fin at `full-text`.

10. **All read-levels are `search-summary`.** Including every quoted string. A single
    transcription error in a search engine's summary would propagate into this file
    undetected.

---

## 6. What would change the answer

Ordered by cost. The first three are cheap and two of them are blocked only by this
session's network policy.

1. **Measure adult pectoral fin planform area** (one fish, one calibrated photograph,
   ImageJ; the *Development* 2022 vascular paper warns the proximal base is the hard
   part of the outline). This unblocks §3.2 and converts the central magnitude from
   `not computable` to a number. Cheapest decisive action in this file.

2. **Run the ZFIN anatomy query that could not be run.** Enumerate transgenic constructs
   with expression annotated to `pectoral fin` / `pectoral fin bud` and *absent* from
   `caudal fin`, `median fin fold`, `dorsal fin`, `anal fin`. Requires `zfin.org` to be
   reachable. This is the one query that could turn the §4 answer from negative to
   positive, and it has not been attempted. **Until it is run, the answer here should be
   read as provisional.**

3. **Read four papers at `full-text`** and re-grade every claim above: Hernández-Vega &
   Minguillón 2011 (which construct is in which allele; what the non-fin expression
   actually looked like, and at which stages); Adachi 2016 (the CNS12 reporter-domain
   figures, specifically whether caudal/median fin was imaged); *Cell Reports* 2018 (the
   deletion alleles); Hawkins 2021 (whether the intermediate-radial phenotype is
   genuinely pectoral-exclusive). Requires PNAS, Wiley, Cell Press access.

4. **Publish the missing negative control.** For any candidate element, image the
   reporter line at ≥5 dpf and through juvenile stages with the caudal fin, dorsal fin,
   anal fin and median fin fold **in the same field**, and report absence quantitatively.
   This control is what the brief asked for and what the literature does not contain.
   Its absence, not its outcome, is why S16 answers no.

5. **Build what does not exist: an intersectional driver.** No single element needs to be
   clean if two dirty ones intersect. A `prrx1a`-CNE driver ∩ a pectoral-field-restricted
   second input (e.g. Cre/Flp split, or a `tbx5a`-dependent component) could be clean
   where neither part is. This moves the answer by changing the design rather than by
   finding a better element, and it is the route I would actually recommend. It is also
   the route for which I found no published zebrafish precedent in fin tissue — and I
   note that building and validating such a line is laboratory work requiring the usual
   institutional animal-research review, not something this document authorises.

6. **Settle the temporal problem separately from the spatial one.** Every element here
   fades by ~3 dpf. Even a perfectly pectoral-restricted embryonic element cannot pay for
   adult allometric growth. A juvenile/adult-active pectoral element is a distinct
   literature gap; my search for adult pectoral-restricted Cre drivers returned
   fin-*bud* gene-trap lines (`tud29Gt`, `tud35Gt`, CreERT2 in restricted fin-bud domains
   at 48 hpf, [*PLOS ONE* 2015](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0129072),
   `search-summary`) with no adult data, against a background that only "59 Cre/CreERT2
   driver lines" existed in zebrafish as of that paper. These two lines are the least-bad
   unexplored lead and should be checked at `full-text` for adult expression.

---

## Sources

All read at `search-summary`. Hosts marked ⛔ were unreachable from this session.

- ⛔ [Hernández-Vega & Minguillón 2011, *Dev Dyn* 240(8):1977–88](https://anatomypubs.onlinelibrary.wiley.com/doi/10.1002/dvdy.22678)
- ⛔ [Adachi et al. 2016, *PNAS*, Regulatory evolution of Tbx5](https://www.pnas.org/doi/10.1073/pnas.1609997113)
- [*Cell Reports* 2018, Genomic knockout of two presumed forelimb Tbx5 enhancers](https://www.cell.com/cell-reports/pdf/S2211-1247\(18\)30798-8.pdf)
- [Hawkins, Henke & Harris 2021, *Cell* 184(4):899–911](https://www.cell.com/cell/fulltext/S0092-8674\(21\)00003-9)
- [Yelon et al. 2000, *Development* 127(12):2573](https://journals.biologists.com/dev/article-abstract/127/12/2573/40865/The-bHLH-transcription-factor-Hand2-plays-parallel)
- [*Nat Commun* 2019, Conserved regulatory program initiates LPM emergence](https://www.nature.com/articles/s41467-019-11561-7)
- [*Nat Commun* 2022, Hand2 delineates mesothelium progenitors](https://www.nature.com/articles/s41467-022-29311-7)
- [*Nature* 2023, A median fin derived from the lateral plate mesoderm](https://www.nature.com/articles/s41586-023-06100-w)
- [hand2 Cre/CreERT2 knock-ins, bioRxiv 2024](https://www.biorxiv.org/content/10.1101/2024.12.04.626907.full.pdf) / [PMC11643050](https://pmc.ncbi.nlm.nih.gov/articles/PMC11643050/)
- [*Nat Commun* 2026, alx gene family and frontonasal CNC](https://www.nature.com/articles/s41467-026-74434-w)
- [*eLife* 2020, Atlas of posterior neural crest lineages](https://elifesciences.org/articles/60005)
- [PMC4825933, Jagged-Notch vs Endothelin1 in upper face](https://pmc.ncbi.nlm.nih.gov/articles/PMC4825933/)
- [PMC4032342, dlx5a/dlx6a in median fin and pectoral structures](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4032342/)
- [PMC10526740, dlx5a/dlx6a and Meckel's cartilage](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10526740/)
- [*Development* 139:2916, Mechanism of pectoral fin outgrowth](https://journals.biologists.com/dev/article/139/16/2916/45235/Mechanism-of-pectoral-fin-outgrowth-in-zebrafish)
- ⛔ [Draper et al. 2003, fgf24 with fgf8 in posterior mesoderm, PMID 12925590](https://pubmed.ncbi.nlm.nih.gov/12925590/)
- [Perathoner et al. 2014, *PLOS Genetics*, Bioelectric signaling regulates size in zebrafish fins](https://journals.plos.org/plosgenetics/article?id=10.1371%2Fjournal.pgen.1004080)
- [*Sci Rep* 2018, Bioelectric-calcineurin signaling module](https://www.nature.com/articles/s41598-018-28450-6)
- [bioRxiv 621243, Integrated K⁺ channel and K⁺-Cl⁻ cotransporter functions](https://www.biorxiv.org/content/10.1101/621243v1.full)
- [bioRxiv 790329, longfin / kcnh2a cis-ectopic expression](https://www.biorxiv.org/content/10.1101/790329.full.pdf)
- ⛔ [PMID 38527087, Scale of pectoral fin buds, K⁺/Ca²⁺/Rcan2/Kcnk5b](https://pubmed.ncbi.nlm.nih.gov/38527087/)
- ⛔ [Patterson et al. 2008, *Dev Dyn*, Growth in larval pectoral fin and trunk musculature](https://anatomypubs.onlinelibrary.wiley.com/doi/10.1002/dvdy.21400)
- [*Development* 149:dev199676, Pectoral fin vascular network](https://journals.biologists.com/dev/article/149/5/dev199676/274591/Anatomy-and-development-of-the-pectoral-fin)
- [PMC13432094, Automatic body morphometrics of adult zebrafish by microCT](https://pmc.ncbi.nlm.nih.gov/articles/PMC13432094/)
- [*PLOS ONE* 2015, Isolation of novel CreERT2-driver lines by gene trap](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0129072)
- ⛔ [ZFIN construct Tg(prrx1a:EGFP), ZDB-TGCONSTRCT-111115-31](https://zfin.org/ZDB-TGCONSTRCT-111115-31) and ⛔ [ZFIN figure ZDB-FIG-110804-50](https://zfin.org/ZDB-FIG-110804-50)

---

```swarm-result
{"subproblem": "S16", "evidence": "literature",
  "answer": "No pectoral-restricted regulatory element adequate to drive the edits is published: of four named elements with pectoral reporter activity, tbx5a CNS12 also drives dorsal eye and is dispensable for fin formation, hand2 reagents also drive pre-anal fin fold and pelvic fin, prrx1a reporters also label pharyngeal arch, and the best candidate (mouse Prx1 / zebrafish prrx1a CNEs, alleles ib4Tg/ib5Tg) has specificity demonstrated only to ~30 hpf with signal fading by 3 dpf and no published caudal- or median-fin negative control.",
  "key_number": "0 named elements with published specificity tested explicitly against caudal and median fins",
  "blocked_on": "ZFIN, PubMed, PNAS and Wiley were unreachable from this session (getaddrinfo ENOTFOUND), so all read-levels are search-summary and the decisive ZFIN query -- constructs annotated to pectoral fin and absent from caudal/median fins -- was never run; adult Danio rerio pectoral fin planform area is also unmeasured in my search, leaving the required fold-change non-computable"}
```
