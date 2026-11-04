# S5-D-D: deepening S5-D by attacking its weakest input

**Date:** 2026-11-04. **Status:** desk research. No experiment was run.

Every number below is one of four kinds, and its sentence says which:
- **quoted**: from a source, with a read-level;
- **figure-read**: read off a published figure, method stated;
- **carried over**: from an earlier note or artifact in this project, with that item's recorded read-level;
- **calculated**: by me, in [`S5-D-deepen_calc.py`](S5-D-deepen_calc.py) (`python3 -I S5-D-deepen_calc.py`).

---

## 0. The answer being deepened

S5-D (`docs/research/fish/S5-deepen.md`, branch `claude/deepen-s5-pectoral-fin-ajxurw` @ `fbaa4b7`, read in
full) concluded:

> Genetic enlargement with measured long-fin alleles dilates the wild-type zebrafish pectoral planform
> (f = 1.74, `kcnk5b^alf/+`), so aspect ratio is unchanged. Whether the reachable fin is a flying-fish
> planform therefore depends entirely on the wild-type zebrafish pectoral AR, **A0**. The bars are
> **A0 ≥ 3.0** (Fish 1990 low end) and **A0 ≥ 9.0** (Park & Choi 2010, *Cypselurus hiraii*). A0 is unknown.

S5-D named A0 as the most sensitive input and could not improve it. Both a value and a threshold enter
that conclusion. I attacked both: I made a fresh attempt on A0 (§2), and I found that the threshold
side has a factor-of-two problem that can be fixed (§1, §3).

## 1. The most sensitive input, shown by recomputing

The verdict S5-D draws is a comparison: "is A0 ≥ T?". A0 is measured in one convention (S5-D §3a protocol:
a single fin's span from base to farthest tip, and that one fin's area). T is quoted from Fish 1990 in
**Fish's** convention. Write `T_Fish = k · AR_single`, where k converts a single-fin semispan²/area into
the number Fish reports. **S5-D implicitly set k = 1.** The verdict depends only on the product k·A0.

Factor-of-two test (calculated, §2 of the script; "in" means k·A0 ≥ 3.0, Fish 1990 low end):

| A0 (single fin) | k = 1 (S5-D) | k = 2.03 | k = 2.64 |
|---|---|---|---|
| 1.00 | out | out | out |
| 1.25 | out | out | **in** |
| 1.50 | out | **in** | **in** |
| 2.00 | out | **in** | **in** |
| 3.00 | in | in | in |

Doubling k has exactly the same effect on the verdict as doubling A0, because k and A0 enter only as
their product. So **the convention factor k is as sensitive as A0**. Unlike A0, it can be fixed from
material the project already holds. It is the input I attacked.

**Is k = 1 defensible a priori? No.** For a pair of fins with zero body width, tip-to-tip span is twice
the semispan and pair area is twice one fin's area. So (2L)²/(2A) = 2·L²/A, which makes k = 2 by
construction. That is a geometric identity, not a measurement. The search summary for Wainwright et al.
2002 (*Env Biol Fish* 65:47) said the authors "multiplied AR values by two" to compare single fins with
two-wing animals, so the literature does use the doubling. Read-level: search-summary only, because the
PDF host (fishlab.ucdavis.edu) was refused by this session's proxy.

## 2. How well established is each leg?

### 2a. A0, the zebrafish leg: still `unknown`. Fresh attempts, with scope

| Attempt | Result | Read-level |
|---|---|---|
| Europe PMC full-text search for `"pectoral fin" AND "aspect ratio" AND (zebrafish OR "Danio rerio")` | 14 hits, none reporting a zebrafish pectoral AR. Two were opened: PMC8840878 (Ecol Evol 2022) measures **caudal** AR only; PMC4097112 (Hale 2014 ICB) discusses AR only generically and its figures are larval and juvenile | listing (14); full-text (2) |
| Europe PMC: `"pectoral fin area"`, `"pectoral fin width/span/shape"` + zebrafish + adult; `"pectoral fin aspect ratio"` (13 hits, all reef fishes, wrasses, bluegill or rays); `"aspect ratio" AND "pectoral fin" AND (Danio OR cyprinid)` | No zebrafish or cyprinid pectoral AR. PMC10918187 (Schizothoracinae trait dataset) records pectoral **length/body length** (0.12–0.21) and caudal AR, not pectoral AR | listing; PMC10918187 full-text |
| Xu, Zeng et al. 2026 *Commun Biol* (PMC13316074), a pectoral-fin breeding-tubercle study in 16 species including *D. rerio*. Main Figs 1–2 and Suppl. Fig 1 (PMC open-data S3, suppl. PDF sha256 `4f944b7f…`) | Every panel is a **crop of the inter-ray region**. No whole fin outline, so span and area cannot be read. Fig 2A's full-fin drawing is a schematic, not a measurement | full-text plus figures, inspected |
| Daane et al. 2018 suppl. Fig S1 (sha256 `c4dab59a…`) | S1A–C are ray close-ups. S1D is a **schematic** of folded pectoral fins | figure, inspected |
| Perathoner et al. 2014 Fig 1A at full resolution (2031×1154 px, from the PMC PDF, sha256 `a289fe0d…`) | Lateral whole-fish photographs. The WT pectoral fin is translucent and folded behind the operculum, so no outline can be read | figure, inspected |
| Web search (extended): "adult zebrafish pectoral fin aspect ratio span area" | Its summary **again** credited Higham et al. 2018 *J Morphol* with zebrafish pectoral AR. Crossref metadata for doi:10.1002/jmor.20876 gives the title *"The ontogenetic scaling of form and function in the spotted ratfish, Hydrolagus colliei"*. **The misattribution is confirmed twice; do not carry it forward** | search-summary; Crossref listing |

**Negative-search scope:**
- Europe PMC queries: 7, English only, with full text for the open-access subset.
- Web searches: 2.
- Figure sets inspected: 3.

**Not searched:**
- ZFIN image database;
- Grandel & Schulte-Merker 1998;
- Paulissen et al. 2022 *Development* (PMC8959142). Europe PMC returned no full text and the PMC S3 bucket had no figures;
- Daane 2021 and Stewart 2021 figures (absent from the PMC S3 bucket);
- museum collections.

**Evidence level of A0: still `unknown`.** I did not estimate it.

### 2b. T and k, the flying-fish leg: an unexamined convention presented as a measured threshold

- Fish 1990's text is carried over from `data/research/flying-fish-source-cards.json` and
  `docs/research/frontier-multiscale-substrate.md` §4c (origin/main @ `7b5ba52c`; recorded there as
  full-text, re-read by the project with pdftotext):
  - p.394 defines AR generically as *"wing span squared / wing area"*;
  - p.395: *"The aspect ratios (AR) of individual flying fish pectoral fins range from 3.0 to 16.9"*.
- The text does not say which span goes into an *individual* fin's AR. `docs/printing.md` (origin/main)
  says so directly: *"Which span and area enter it is not settled here."*
- I tried to read Fish 1990 myself. The WCUPA host is outside this session's network allowlist, so the
  source is **could-not-access** for me. My statements about it are carried over, not re-read.

So S5-D's "3.0" and "9.0" are measured numbers in an **undeclared convention**. Comparing them with a
single-fin A0 assumes k = 1. Nobody stated that assumption, and §1 shows it is the least plausible value.

## 3. Improving k: the primary numbers already in the repo

The project's flying-fish print designs (origin/main `artifacts/print/design/C-four-wing-glider.json`,
sha256 `bd97309f…`; `B-two-wing-glider.json`, sha256 `c9cdd477…`) hold fin geometry built from the
following inputs:
- **Fish 1990 Table I** reduced-major-axis fits of wing span *b* and wing area *S*, evaluated at 0.1 kg
  (carried over, full-text per `docs/printing.md`);
- **Table IV** pectoral share of S (carried over, full-text);
- one assumed body width *w* at the fins (`design_assumption`).

The single-fin semispan is L = (b − w)/2, and one fin's area is A = share·S/2. **Fish's Table III AR-on-mass
fit** at the same mass is also stored there (carried over). I re-derived each convention (calculated, §1):

| at 0.1 kg | single fin L²/A | pair b²/(2A) | whole wing b²/S | Fish Table III fit | **k = Table III / single** |
|---|---|---|---|---|---|
| *Cypselurus* | 4.30 | 11.15 | 8.47 | 8.74 | **2.03** |
| *Exocoetus* | 5.66 | 13.58 | 12.47 | 14.94 | **2.64** |
| miss vs Table III, single fin | −51 % / −62 % | +28 % / −9 % | −3 % / −17 % | | |

**What this shows (calculated from carried-over measured fits):**
- Fish's own Table III AR values are **2.0–2.6×** larger than the single-fin semispan²/area implied by
  his own Table I span and area fits for the same mean fish.
- The single-fin convention is the **worst** match of the three for both genera.
- So k ≈ 2.0–2.6, not 1.

**Caveats, kept rather than averaged away:**
1. Table I and Table III are separate regressions. Comparing them at one mass compares fitted means,
   not individual fish.
2. No single convention fits both genera (the project's `docs/printing.md` already reports this).
   Whole-wing fits *Cypselurus*; the pectoral-pair convention fits *Exocoetus*. So I carry k as a
   **range**, 2.03–2.64, not a point.
3. There is an alternative reading I cannot exclude without Fish's methods: if Fish measured individual-fin
   "span" along the **leading ray** of a swept fin, rather than as a perpendicular semispan, the
   single-fin AR would rise. Reaching k ≈ 2 needs a length ratio of √2, i.e. a ~45° sweep. That is my
   inference. Fish's spread and measurement convention is **unknown** to me.
4. Park & Choi 2010's convention is carried over as "the same quantity" as Fish's
   (`frontier-multiscale-substrate.md` §4c). I did not verify that. Its single-fin equivalent below
   assumes it.

**Improved thresholds**, in the single-fin convention that S5-D's measurement protocol produces (calculated, §3):

| Bar | S5-D said | Improved (single-fin) |
|---|---|---|
| Fish 1990 low end (3.0) | A0 ≥ 3.0 | **A0 ≥ 1.14–1.48** |
| Park & Choi low end (9.0), if same convention | A0 ≥ 9.0 | **A0 ≥ 3.4–4.4** |
| mean *Cypselurus* planform at 0.1 kg | (not stated) | **A0 ≥ 4.30** |
| mean *Exocoetus* planform at 0.1 kg | (not stated) | **A0 ≥ 5.66** |

**What the bars mean for a fan of equal rays.** This uses S5-D's geometry model (sector AR = 2/θ;
calculated, §4; a model, not a fin):
- reaching the Fish low end needs a spread θ ≤ 78–101°;
- matching the mean *Cypselurus* needs θ ≤ 27°;
- matching the mean *Exocoetus* needs θ ≤ 20°;
- S5-D's own bars needed θ ≤ 38° (3.0) and θ ≤ 12.7° (9.0).

## 4. Recomputed conclusion

**Unchanged** (no input in this note touches them):
- the span ceiling, about 0.36 SL (0.30–0.45), carried over from S5-D;
- the structural claim that uniform dilation preserves AR (S5-D's α ≈ 2 premise, rated there as an
  authors'-claim level of support).

**Corrected.** S5-D's numerical bars were stated in Fish's convention and applied to a single-fin
quantity. Corrected bars, single-fin convention, α = 2 (calculated, §5):
- **≥ 1.1–1.5** to enter Fish 1990's flying-fish envelope;
- **≥ 4.3** for a mean-*Cypselurus* planform;
- **≥ 5.7** for a mean-*Exocoetus* planform.

Under the α = 1 alternative, the bars become 0.65–0.85, 2.5 and 3.3.

**Consequence (my inference, from the fan model, not a measurement).**
- The Fish-envelope test, which S5-D treated as the decisive one, is now **weak**. Almost any fan
  spread below about 80° clears it, so "inside Fish 1990's range" no longer tells a zebrafish fin from
  a flying-fish fin.
- The informative test is against the genus-mean single-fin planform, about 4.3–5.7. That needs a
  narrow blade (spread about 20–27°).

**Verdict: STANDS.**
- S5-D's conclusion holds: the reachable planform is the dilated wild-type planform, and whether it is a
  flying-fish planform depends entirely on A0, which is still unmeasured.
- The conclusion holds even though the thresholds stated inside it fall by a factor of 2.0–2.6 and are
  replaced above.
- Anyone who measures A0 by S5-D's protocol must compare it with the **improved** bars, or with k·A0
  against Fish's numbers. Comparing a single-fin A0 with 3.0 or 9.0 directly would wrongly reject fins
  with single-fin AR between about 1.1–1.5 and 3.0.

**What would settle the remaining gaps.**
1. A0 needs S5-D's spread-fin imaging protocol (§3a there). That is unchanged.
2. k needs one page: Fish 1990's Methods, saying how individual-fin span was measured. The cost is one
   PDF read once the WCUPA host is allowed. Until then, k = 2.03–2.64 is a calculated inference from
   Fish's own fits.
3. An independent check on k: measure single-fin L²/A and the pair b²/(2A) on the same
   *Cypselurus* specimen.

---

## Sources and read-levels

- S5-D note, `docs/research/fish/S5-deepen.md` and `S5-deepen_calc.py` (`claude/deepen-s5-pectoral-fin-ajxurw`
  @ `fbaa4b7`). **full-text** (repo).
- `artifacts/print/design/{B-two-wing-glider,C-four-wing-glider}.json`, `docs/printing.md`,
  `data/research/flying-fish-source-cards.json`, `docs/research/frontier-multiscale-substrate.md`
  (origin/main @ `7b5ba52c`). **full-text** (repo). Their Fish 1990 values are recorded there as full-text.
- Fish FE 1990, *J Zool Lond* 221:391–403. **could-not-access** for me (WCUPA host refused). All values
  are carried over.
- Park & Choi 2010. **carried over**, not re-read.
- Wainwright PC, Bellwood DR, Westneat MW 2002, *Env Biol Fish* 65:47–62. **search-summary** (the
  "multiplied AR values by two" text). PDF host refused.
- Higham TE et al. 2018, *J Morphol* 279:1408. **listing** (Crossref title: spotted ratfish, not zebrafish).
- Xu Z, Zeng X et al. 2026, *Commun Biol* 9:873, PMC13316074. **full-text plus figures** (no whole-fin outline).
- Daane JM et al. 2018, *Sci Rep* 8:10391, suppl. PDF. **figure, inspected**.
- Perathoner S et al. 2014, *PLoS Genet* 10:e1004080, Fig 1A. **figure, inspected**.
- PMC8840878, PMC4097112, PMC10918187. **full-text** (string search). Other Europe PMC hits: **listing**.

```swarm-result
{"subproblem": "S5-D-D", "evidence": "calculated: AR-convention factor k re-derived from carried-over Fish 1990 Table I/III/IV fits (project design JSONs, recorded full-text; Fish 1990 could-not-access for me); A0 still unknown after a fresh scoped search", "answer": "S5-D's conclusion stands (the reachable planform is the dilated wild-type zebrafish planform and its flying-fish status depends entirely on the unmeasured wild-type pectoral AR A0), but its thresholds were in Fish 1990's convention, which is 2.0-2.6x the single-fin span^2/area that S5-D's protocol would measure, so the bars fall from A0 >= 3.0 / 9.0 to about A0 >= 1.1-1.5 (Fish envelope) and >= 4.3-5.7 (mean Cypselurus/Exocoetus single-fin planform).", "key_number": "convention factor k = Fish Table III AR / single-fin semispan^2/area = 2.03 (Cypselurus) - 2.64 (Exocoetus) at 0.1 kg, dimensionless; improved single-fin bars A0 >= 1.14-1.48 (Fish 1990 low end), >= 4.30 (Cypselurus), >= 5.66 (Exocoetus); A0 itself unknown", "verdict": "stands", "depends_on": ["S5-D conclusion and swarm-result (claude/deepen-s5-pectoral-fin-ajxurw @ fbaa4b7)", "S5-D: f = 1.74 kcnk5b alf/+ pectoral fold-change (Daane 2018 Fig 1A figure-read, via S22-D-D)", "S5-D: p0 = 0.208 (0.173-0.260) WT pectoral/SL, span 0.36 SL (0.30-0.45)", "S5-D premise: alpha ~ 2 uniform dilation (Perathoner 2014, Daane 2018, Stewart 2021 author claims)", "S5-D fan-of-rays geometry model (sector AR = 2/theta)", "unknown: wild-type adult zebrafish pectoral AR A0 and its spread convention", "Fish 1990 p.394 AR = wing span^2/wing area (carried over, could-not-access)", "Fish 1990 p.395 individual pectoral AR 3.0-16.9; Table III to 19.9 (carried over)", "Fish 1990 Table I r.m.a. fits of wing span and wing area at 0.1 kg (carried over via artifacts/print/design B and C JSONs)", "Fish 1990 Table IV pectoral share of wing area: Cypselurus 0.7599, Exocoetus 0.9183 (carried over)", "Fish 1990 Table III AR-on-mass fit at 0.1 kg: Cypselurus 8.74, Exocoetus 14.94 (carried over)", "design assumption: body width at the pectoral fins (C 0.0335 m, B 0.0279 m)", "assumption: Fish measured individual-fin span as perpendicular semispan, not leading-ray length (alternative not excluded)", "assumption: Park & Choi 2010 AR 9.0-10.7 is in the same convention as Fish 1990 (carried over, unverified)", "Wainwright et al. 2002 doubling of single-fin AR (search-summary)", "negative: Higham et al. 2018 J Morphol is a ratfish study (Crossref listing), not a zebrafish AR source", "negative search scope: 7 Europe PMC queries, 2 web searches, 3 figure sets (PMC13316074, Daane 2018 suppl, Perathoner 2014 Fig 1A)"]}
```
