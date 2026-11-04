# S5-D — Deepening S5: what pectoral-fin planform is reachable by genetic enlargement?

**Date:** 2026-11-04. **Status:** desk research. No experiment was run.

Every number below is one of four kinds, and its sentence says which:
- **quoted**: from a source, with a read-level;
- **figure-read**: read off a published figure, method stated;
- **carried over**: from an earlier note in this project, with that note's read-level;
- **calculated**: by me, in [`S5-deepen_calc.py`](S5-deepen_calc.py) (`python3 -I S5-deepen_calc.py`).

---

## 0. What answer is being deepened

**The recorded S5 answer was handed to me empty.** I also found no `S5` research note on any branch.
Scope of that search: `git ls-tree` over every one of the 240 remote refs for `docs/research/fish/S5*`
(0 hits), and `git grep` for "pectoral fin planform" / "S5" across all refs.

The only S5 record is the seed row in `db/designswarm/0004_seed_fish_frontier.sql` (branch
`origin/claude/adder-cell-size-law-5baqub`). It sets:
- **acceptance:** *"Span and area reachable, expressed in body lengths, derived from measured
  fold-changes in real zebrafish long-fin alleles rather than assumed."*
- **falsifier:** *"A measured allele exceeding the stated ceiling, or evidence the overgrowth does not
  apply to pectorals."*

So I deepen the answer that the project's own measured inputs already imply. That answer was built in
the S22 chain: S22-D-D (`claude/s22-d-sensitive-input-pwechp`) and Challenge 147
(`claude/challenge-147-pectoral-fin-pbn0gm`). Written as S5's acceptance asks, it reads:

> **A (implied S5 answer):** a dominant bioelectric long-fin allele lengthens the zebrafish pectoral fin
> about 1.74× (`kcnk5b^alf/+`). Wild-type pectoral length is about 0.21 SL. The reachable per-fin span
> is therefore about **0.36 SL** (0.30–0.45). Overgrowth preserves the fin's organisation, so the
> reachable planform is the **wild-type zebrafish planform, dilated**: area grows about f², and aspect
> ratio is unchanged.

The parts of A are of different kinds:
- **span** is calculated from carried-over figure-reads;
- **area ∝ f²** is an assumption that nobody in the project has tested;
- **"AR unchanged"** follows from that assumption.

## 1. The input A is most sensitive to, shown by recomputing it

S5's acceptance asks for span **and area**. The question it serves is whether the reachable fin is a
flying-fish *planform*, and planform is aspect ratio (AR = span² / area, the Fish 1990 definition).
I wrote reachable AR as

`AR_reach = A0 · f^(2−α)`, with `area ∝ f^α`.

- `A0` is the wild-type zebrafish pectoral AR.
- `α = 2` is shape-preserving dilation; `α = 1` is rays lengthening at a fixed chord.
- Targets (carried over from `data/research/flying-fish-source-cards.json`; the repo records them as
  full-text; I did not re-read them):
  - individual flying-fish pectoral AR **3.0–16.9** (Fish 1990, p.395; Table III up to 19.9, an
    unresolved text-versus-table contradiction);
  - **9.0–10.7** for *Cypselurus hiraii* (Park & Choi 2010).

**Factor-of-two test.** All values calculated, §3 of the script. Central case: p0 = 0.208, f = 1.74,
A0 = 2 (an assumed value), α = 2.

| Input changed ×2 | span | AR | area | Is AR inside Fish 1990's 3.0–16.9? |
|---|---|---|---|---|
| none (base) | 0.362 SL | 2.00 | 0.066 SL² | no |
| p0 ×2 or ÷2 | ×2 / ×0.5 | **×1.00** | ×4 / ×0.25 | no (unchanged) |
| f ×2 | ×2 | **×1.00** | ×4 | no (unchanged) |
| **A0 ×2** | ×1 | **×2.00** | ×0.5 | **yes (flips)** |
| A0 ÷2 | ×1 | ×0.50 | ×2 | no |
| α 2 → 1 | ×1 | ×1.74 | ×0.57 | yes (flips) |

**What this shows (calculated):**
- Doubling or halving the two inputs the S22 chain worked hardest on, `p0` and `f`, changes span and
  area by 2× and 4×. It **does not move the planform at all.** Under dilation, AR is scale-free.
  (Area still matters for wing loading, but that is S3's question, not this one.)
- The planform verdict depends on two inputs: **A0**, linearly, and the **shape-preservation premise
  α**. Of these, A0 is the single most sensitive: it enters at power 1 whatever α is, while α can move
  AR by at most f = 1.74×.
- Minimum A0 needed to enter each envelope (calculated, §4):

  | Premise | Fish 1990 low end (3.0) | Park & Choi (9.0) |
  |---|---|---|
  | α = 2 | A0 ≥ 3.00 | A0 ≥ 9.0 |
  | α = 1 | A0 ≥ 1.72 | A0 ≥ 5.2 |

**The input to attack is A0, the wild-type adult zebrafish pectoral-fin aspect ratio.** The premise
that turns A0 directly into the answer (α ≈ 2, uniform dilation) comes next.

## 2. How well is A0 established?

**A0 is unknown, and nobody in this project has measured, sourced or even assumed a value for it.**
A builds in "AR unchanged" without ever saying what the AR is. This is not a repeated assumption. It is
a gap that the span-only framing of S22 hid, because length/SL comparisons never need it. That is my
inference from reading the S22-D, S22-D-D and Challenge 147 notes.

What I tried, with scope:

| Attempt | Result | Read-level |
|---|---|---|
| Daane et al. 2018 *Sci Rep* 8:10391 (PMC6039437) full text: string search for area / width / breadth / surface / ray number | 0 hits for fin area or width. Ray-count text absent | full-text (PMC S3 `.txt`, sha256 `78de1309…`) |
| Perathoner et al. 2014 *PLoS Genet* (PMC3894163), same search | 0 hits for fin area or width | full-text (PMC S3 `.txt`, sha256 `245faa42…`) |
| Daane et al. 2021 *Curr Biol* (PMC9172250), same search | 0 hits. Fig 4 measures length/SL only (agrees with S22-D) | full-text (PMC S3 `.txt`, sha256 `8192f58b…`) |
| D18 Fig 1B photographs (WT, WT+FK506, *sof*+FK506, *alf*+FK506; dorsal view, 2 mm bars), from the Europe PMC supplementaryFiles zip | Opened and inspected. **The pectoral fins are folded back against the body, not spread**, so span² / area cannot be read. Shape is qualitatively similar between WT and *alf* (my eye-read, not a measurement) | figure image, full |
| Web search: "zebrafish pectoral fin aspect ratio adult area span" (one standard, one extended) | The extended-search summary said Higham et al. 2018 *J Morphol* measured adult **zebrafish** pectoral span, area and AR. **That is false.** A follow-up search identifies Higham et al. 2018 *J Morphol* 279:1408 (doi:10.1002/jmor.20876) as a study of the **spotted ratfish *Hydrolagus colliei***. The PDF host (biomechanics.ucr.edu) is outside this session's network allowlist. I record this so the misattribution does not get carried forward | search-summary (both); paper could-not-access |
| bioRxiv 10.1101/2021.04.02.437283 (zebrafish pectoral-fin vascular anatomy), as a possible source of spread adult-fin images | HTTP 429 (rate-limited) | could-not-access |
| Ray count | 10–14 pectoral rays in adult zebrafish, from a search-result summary of a Tohoku University skeletal study. Not opened | search-summary |

**Negative-search scope.** Two web searches, English only. Three primary full texts string-searched.
One figure set inspected. **Not searched:** ZFIN anatomy and phenotype images, Grandel &
Schulte-Merker 1998, Hale-lab adult pectoral biomechanics papers, the Daane 2021 supplementary PDF
(could-not-access in S22-D), or any museum or morphometric database.

**Evidence level of A0:** `unknown`. A structural caveat applies too. My calculation (§5 of the
script, a geometry model and not a fin) shows that for a fan of rays, AR depends on how far the fin is
spread:
- an equal-ray sector has AR = 2/θ;
- reaching AR 3.0 needs θ ≤ 38°, and AR 9.0 needs θ ≤ 12.7° (calculated).

So A0 is not purely a morphological constant. It has to be measured at a stated, standardised spread,
and for the comparison to be fair, the same convention as Fish 1990's preserved specimens. How Fish
1990 spread the fins is **unknown** to me (not re-read).

## 3. Improving it

### 3a. A0 itself: not improved. It stays unknown

I could not find a measured value, and I will not supply one from memory.

**The measurement that settles it** (cost and time are my estimates, not sourced):
1. Anaesthetise adult fish, about 20 each of WT, `kcnk5b^alf/+`, `kcnh2a^lof/+` (ZIRC ZL86) and
   `lat4a^nr21/+; kcnh2a^lof/+` if the Harris lab will share it.
2. Spread one pectoral fin to its maximal natural extent on a slide, or excise it post-mortem and pin
   it flat, and photograph it with a scale bar.
3. Measure span (base to farthest tip, perpendicular to the base), area (polygon in Fiji) and each
   ray's length.

This gives A0, AR_reach and the ray-wise fold-change profile `g` (§3b) directly. It takes about one
week of imaging once adults are in hand and needs no new equipment: roughly US$1–3 k beyond husbandry,
or about 3 months if the lines must be raised. A cheaper partial step is to digitise spread pectoral
fins from existing published images with scale bars. I found none in the sources I could open.

### 3b. The premise that makes A0 the answer (α ≈ 2, uniform dilation): improved from unstated to sourced, with a counter-example

| Source | What it says | Read-level | Bearing on α / uniformity |
|---|---|---|---|
| Perathoner 2014 (PMC3894163) | *"The mutant another longfin develops proportionally larger fins and barbels."* *"Overgrown fins and barbels in alf mutants retain their general organization"*. *"the overgrown structures in the mutants preserve tissue organization and patterning"* | full-text | Authors' claim of **proportional** enlargement. No shape metric is reported. "Proportional" here means fin relative to body; whether ray-to-ray proportions hold is my inference, not their measurement |
| Daane 2018 (PMC6039437) | Calcineurin inhibition *"is not sufficient to re-specify positional memory of size of the fin"*. Kcnk5b/calcineurin *"regulates rate of growth"*. Growth rate during regeneration *"is dependent on the amount of tissue lost"* | full-text | Supports a **position-scaled rate**. If every ray's rate is scaled by the same factor, the ray-length profile dilates uniformly (α ≈ 2). That last step is my inference |
| Stewart et al. 2021 *Development* 148:dev199384 (PMC8217709) | *"rather than altering positional information"*. Overgrowth is *"due to an extended outgrowth period"* with *"indistinguishable maximal growth rates"* | full-text, read through a fetch-tool extraction of the first 100 k of 120 k characters | Duration, not pattern, changes. Consistent with α ≈ 2 if extra duration acts on position-scaled rates (my inference) |
| Stewart 2021, chimera and crispant results | *"Several fins had strong EGFP+ overgrown rays flanked by intermediate length rays"*. *"21.8% of kcnh2a crispants showed partial regionalized fin overgrowth"*. *"one pectoral fin rescued to wild-type length with the other exhibiting pronounced overgrowth"* | same | **Counter-evidence to obligatory uniformity.** Overgrowth is ray-autonomous, so a mosaic or ray-restricted expression pattern can change ray-to-ray proportions. Direct pectoral evidence covers left versus right asymmetry; within-pectoral ray mosaics are shown for "fins" without a fin type I could confirm |
| Daane 2021 (PMC9172250) | Double mutant: paired fins overgrown, medial fins wild-type size. The caudal fin is *"hypocercal, with an elongated ventral lobe"* | full-text | **A germline genotype does produce within-fin differential growth**, in the caudal fin. Whether it does in the pectoral is **unknown** (Fig 4A could-not-access, as in S22-D) |

**Disagreement preserved:**
- The single-allele sources (Perathoner, Daane 2018, Stewart's germline results) describe proportional,
  pattern-preserving overgrowth.
- Stewart's mosaics and Daane 2021's hypocercal caudal show that differential, shape-changing
  overgrowth is genetically reachable.

These do not contradict each other. They describe different genotypes. But nobody has measured which
regime the pectoral fin of any genotype is in.

**How much shape change the counter-evidence could buy** (calculated, §7; fan model with θ = 60° and
equal baseline rays, both assumed). Here `g` is the extra fold-change of the leading ray over the
trailing ray:

| g | 1.0 | 1.25 | 1.5 | 2.0 | 3.0 | 4.0 |
|---|---|---|---|---|---|---|
| AR multiplier | 1.00× | 1.24× | 1.46× | 1.85× | 2.48× | 2.97× |

Taking a low-AR fan into the Park & Choi band would therefore need a leading-to-trailing overgrowth
ratio of several-fold, on top of f. No measured allele shows this. A finite fin root, with rays
elongating uniformly, adds only 1.14–1.25× (calculated, §6, root = 0.25 ray length, assumed).

## 4. Recomputed conclusion

**Span, in body lengths** (calculated from carried-over figure-reads, unchanged by this note):

| p0 reading | alf/+ pectoral f = 1.74 (measured proxy) | alf/+ caudal f = 2.05 (upper proxy) |
|---|---|---|
| 0.173 (60 % resected) | 0.30 SL | 0.36 SL |
| **0.208 (adopted)** | **0.36 SL** | 0.43 SL |
| 0.260 (40 % resected) | 0.45 SL | 0.53 SL |

**Area** = span² / AR_reach. It cannot be stated in SL² because AR_reach needs A0, which is unknown.
Under uniform dilation, area is (wild-type area) × f² ≈ **3.0×** wild-type (calculated, f = 1.74).
Wild-type area itself is unknown.

**Planform:**
- The improved premise (α ≈ 2 for germline single alleles, supported by authors' claims in three
  full-text sources) confirms A's structural statement: **the reachable planform is the zebrafish
  planform dilated, and AR is not changed by enlargement**.
- So the question "is it a flying-fish planform?" reduces exactly to whether **A0 ≥ 3.0** (Fish 1990
  envelope) or **A0 ≥ 9.0** (*Cypselurus*). A0 is **unknown**.
- Differential overgrowth is the only route to a higher-AR planform. It has been shown in other fins
  and in mosaics, but **not measured in any pectoral fin**.

**Falsifier check against S5's seed:**
- "Evidence the overgrowth does not apply to pectorals": **not met.** Pectoral overgrowth is measured:
  `alf/+` 1.74× (D18 Fig 1A, figure-read, carried over). Daane 2021 reports paired-fin overgrowth, and
  Stewart 2021 shows pectoral overgrowth in chimeras (quoted).
- "A measured allele exceeding the stated ceiling": none found. No pectoral fold-change for
  `kcnh2a^lof/+` was found in any source opened by this note or by S22-D-D.

**Verdict: STANDS.**
- A's span ceiling (about 0.36 SL, 0.30–0.45) and its structural claim (dilation, AR preserved) stand.
- The shape-preservation premise moves from unstated to supported by authors' claims, though not by a
  shape measurement.
- **But A cannot answer its own question.** The input that decides whether the dilated fin is a
  flying-fish planform, A0, is unmeasured, and I could not improve it.

This is a precisely stated negative result. The project knows how long a genetically enlarged
zebrafish pectoral fin can be. It does not know its aspect ratio, and enlargement as measured so far
will not change it. About a week of photographing spread fins (§3a, my estimate) would settle it.

---

## Sources and read-levels

- Daane JM et al. 2018. *Sci Rep* 8:10391, PMC6039437. **full-text** (S3 txt) plus **figure images**
  (Fig 1, 4 inspected).
- Perathoner S et al. 2014. *PLoS Genet* 10:e1004080, PMC3894163. **full-text** (S3 txt).
- Daane JM et al. 2021. *Curr Biol* 31:5052, PMC9172250. **full-text** (S3 txt). Figures:
  **could-not-access** (carried over from S22-D).
- Stewart S et al. 2021. *Development* 148:dev199384, PMC8217709. **full-text** (fetch-tool
  extraction, first 100 k / 120 k characters; quotes are as returned by that extraction).
- Fish FE 1990 and Park & Choi 2010: AR envelopes **carried over** from
  `data/research/flying-fish-source-cards.json` on `origin/main`. The repo records them as full-text;
  **not re-read by me**.
- Higham TE et al. 2018. *J Morphol* 279:1408, doi:10.1002/jmor.20876. **search-summary**. It is a
  ratfish study, misattributed to zebrafish by one search summary.
- S22-D-D (`claude/s22-d-sensitive-input-pwechp`) and Challenge 147
  (`claude/challenge-147-pectoral-fin-pbn0gm`). **full-text** (repo notes). Source of p0 and f.
- S5 seed row, `db/designswarm/0004_seed_fish_frontier.sql`. **full-text**.

```swarm-result
{"subproblem": "S5-D", "evidence": "calculated (geometry and sensitivity) on carried-over figure-reads (p0, f) + full-text author claims of pattern-preserving overgrowth; decisive input (wild-type zebrafish pectoral AR) unknown", "answer": "Genetic enlargement with measured long-fin alleles reaches a per-fin span of ~0.36 SL (0.30-0.45, calculated) by dilating the wild-type zebrafish pectoral planform, which leaves aspect ratio unchanged, so whether the reachable fin is a flying-fish planform (AR >= 3.0, Fish 1990; 9.0-10.7, Park & Choi) depends entirely on the wild-type zebrafish pectoral AR, which has not been measured.", "key_number": "wild-type adult zebrafish pectoral-fin aspect ratio A0 (span^2/area): unknown; reachable AR = A0 under uniform dilation; A0 >= 3.0 needed for Fish 1990 envelope, >= 9.0 for Cypselurus; reachable span 0.36 SL (0.30-0.45)", "verdict": "stands", "depends_on": ["S5 seed acceptance/falsifier (db/designswarm/0004_seed_fish_frontier.sql)", "S5 recorded answer (empty as delivered)", "S22-D-D: wild-type zebrafish pectoral/SL p0 = 0.208 (0.173-0.260), figure-read of Daane 2018 Fig 1A plus resection-fraction inference", "S22-D-D: f = 1.74 kcnk5b alf/+ pectoral fold-change (Daane 2018 Fig 1A figure-read), proxy for kcnh2a lof/+", "Perathoner 2014 Fig 1E: alf/+ caudal ~2.05x (eye-read), upper proxy for f", "Challenge 147: p0 sources disagree (Islam 2025 0.094-0.168 vs Praveenraj 2017 0.18-0.26)", "Fish 1990: individual flying-fish pectoral AR 3.0-16.9, Table III to 19.9 (carried over, not re-read)", "Park & Choi 2010: Cypselurus hiraii pectoral AR 9.0-10.7 (carried over, not re-read)", "Perathoner 2014 PMC3894163: alf fins proportionally enlarged, retain organization (author claim, no shape metric)", "Daane 2018 PMC6039437: calcineurin/Kcnk5b changes growth rate, does not re-specify positional memory (author claim)", "Stewart 2021 PMC8217709: lof prolongs outgrowth period, same peak rate, does not alter positional information (author claim, fetch-extraction)", "Stewart 2021 PMC8217709: ray-autonomous mosaic overgrowth and pectoral L/R asymmetry in chimeras (counter-evidence to obligatory uniformity)", "Daane 2021 PMC9172250: double mutant caudal hypocercal (within-fin differential growth); pectoral shape unknown, Fig 4 could-not-access", "assumption: area scales as f^alpha with alpha ~ 2 (uniform dilation) for germline single alleles", "assumption: span ~ fin length (leading ray spanwise)", "model: fan-of-rays planform geometry (S5-deepen_calc.py), AR depends on spread angle", "unknown: wild-type adult zebrafish pectoral-fin aspect ratio A0 and spread convention", "unknown: kcnh2a lof/+ and double-mutant pectoral fold-change and ray-wise profile g", "unknown: Fish 1990 fin-spread convention for AR measurement"]}
```
