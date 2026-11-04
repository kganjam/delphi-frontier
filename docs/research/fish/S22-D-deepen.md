# S22-D-D: Deepening S22-D by attacking its weakest input (the zebrafish pectoral/SL)

**Parent (S22-D, dna):** *Deepen S22: attack its most sensitive input.*
**What S22-D recorded** (branch `claude/deepen-s22-daane-fin-7dqlop`, `docs/research/fish/S22-deepen.md`):
Daane et al. 2021 measured pectoral/SL and caudal/SL **only within zebrafish genotypes**. They never
compared the `lat4a^nr21/+; kcnh2a^lof/+` value numerically with flying-fish pectoral/SL, so even the
length "phenocopy" is a qualitative cross-species match. The flying-fish target is about 0.65–0.77 SL
(*E. volitans*, search-summary, three sources disagree). The zebrafish value is **unknown** (Fig 4B
could-not-access). S22-D's sensitivity grid, calculated over assumed wild-type `p0` = 0.10–0.25, gave a
required overgrowth of 1.4× to 7.7×. Verdict: STRENGTHENS.

I ran no experiment for this note. Every number below is one of three kinds, and the sentence says which:
(a) quoted from a source, (b) read off a published figure (**figure-read**, with the method stated), or
(c) **calculated**. The script that does the calculations is `S22-D-deepen_calc.py`, in this directory.

---

## 0. Sources and read-levels

| # | Source | Read-level | What I took from it |
|---|---|---|---|
| P1 | Daane JM et al. (2021) *Modulation of bioelectric cues in the evolution of flying fishes.* Curr Biol 31:5052. PMID 34534441, PMCID PMC9172250 | **full-text** (text only: PMC Open Data S3 `PMC9172250.1.txt`, sha256 `8192f58b…6a22`; `.xml` sha256 `4ecf32e8…54ce`; author manuscript, licence "TDM") | Re-checked the Fig 4 legend and the "Sufficiency…" paragraph |
| P1-fig4 / Data S1 | Fig 4B image, `NIHMS1735542-supplement-2.xlsx` | **could-not-access** (see §3) | Double-mutant pectoral/SL: **unknown** |
| P1-pre | Daane et al., bioRxiv preprint 10.1101/2021.03.05.434157 (Europe PMC PPR293816), titled *Novel regulators of growth identified in the evolution of fin proportion in flying fish* | **abstract** (Europe PMC). bioRxiv returned Cloudflare 1015 (rate-limited); Europe PMC fullTextXML returned HTTP 500 | Confirms a preprint exists. Whether its figure carries the same data is unknown |
| D18 | Daane JM, Lanni J, Rothenberg I, Seebohm G, Higdon CW, Johnson SL, Harris MP (2018) *Bioelectric-calcineurin signaling module regulates allometric growth and size of the zebrafish fin.* Sci Rep 8:10391. doi:10.1038/s41598-018-28450-6, PMC6039437 | **full-text** (PMC S3 `.txt`, sha256 `78de1309…a7da7`) **plus figure images** (Europe PMC supplementaryFiles zip: Fig 1–4 JPG and the ESM PDF; ESM PDF not read) | Wild-type and `kcnk5b^alf/+` pectoral fin length normalised to SL (Fig 1A). Same senior lab as P1, same caliper/SL protocol |
| P14 | Perathoner S, Daane JM, et al. (2014) *Bioelectric signaling regulates size in zebrafish fins.* PLoS Genet 10:e1004080. PMC3894163 | **full-text** (PMC S3 `.txt`, sha256 `245faa42…a58c`) **plus Fig 1 image** (journals.plos.org) | Caudal fin length/SL in wt and `alf/+` (Fig 1E). Allometric slopes, caudal: wt k = 1.29, alf/+ k = 1.88 (Fig 1D) |
| P2 | Stewart S et al. (2021) Development 148:dev199384, PMID 34061172 | **abstract** (not in the PMC open-data bucket) | `longfin^t2` is a regulatory `kcnh2a` allele; its fins are "dramatically elongated". **No fold-change number in the abstract** |
| C1–C4 | Flying-fish pectoral/SL sources carried over from S22-D (FAO ×2, fishesoftexas, Davenport JMBA) | **search-summary** (not re-read here) | Target 0.65–0.77 SL (*E. volitans*); sources disagree (0.65–0.70 / 0.70–0.75 / 0.73–0.77) |

---

## 1. The input S22-D's answer is most sensitive to

S22-D's conclusion, that the length "phenocopy" is qualitative and the gap to flying fishes is unknown
and possibly 3–7×, rests on one quantity:

> **Rz = pectoral-fin length / SL in adult `lat4a^nr21/+; kcnh2a^lof/+` zebrafish**, which is
> `p0` (wild-type pectoral/SL) × `f` (fold overgrowth of the pectoral fin in the double mutant).

**Factor-of-two test (calculated, `S22-D-deepen_calc.py`).** My central estimate below is Rz ≈ 0.36–0.43 SL.
If Rz is doubled (0.72–0.85), it lands inside or above the flying-fish range of 0.65–0.77, and "phenocopies
proportions" would become a quantitative truth. If Rz is halved (0.18–0.21), it is in the wild-type
range and the "paired-fin overgrowth" disappears. A factor of two on this one input flips the
conclusion in both directions. No other input does this. Halving or doubling the flying-fish target moves
the gap too, but the three disagreeing sources span only 0.65–0.77, a factor of 1.18.

S22-D's own grid let `p0` range over 0.10–0.25, a factor of 2.5. That `p0` range alone is what
produced the "1.4× to 7.7×" spread. So **`p0` is the weakest link**, and `f` comes right after it.

---

## 2. How well was that input established in S22-D?

- **Rz:** **unknown**. The authors measured it (author's claim: Fig 4B "length normalized by SL", with
  Tukey's HSD), but nobody in this project has read the value.
- **`p0`:** an **assumption**. S22-D chose grid values 0.10–0.25 and cited no source, and said so. It was
  not a proxy or a measurement.
- **`f`:** never addressed. The only quantitative constraint was that Rz/`p0` must reach FF/`p0`.

Honest grade: **unmeasured, held by an assumed grid**. Nothing upstream had dressed it up as measured,
which is to S22-D's credit.

---

## 3. Improving it

### 3a. The real quantity (Rz): still could-not-access. Attempts in this session:
- `pmc.ncbi.nlm.nih.gov/articles/PMC9172250/` and `/bin/nihms-1735542-f0004.jpg`: reCAPTCHA challenge page.
- `www.cell.com/current-biology/fulltext/S0960-9822(21)01142-8`: HTTP 403 Cloudflare challenge.
- PMC Open Data S3 bucket (`pmc-oa-opendata`, prefix `PMC9172250`): **text and XML only, no figures and
  no supplementary files**. This is how I obtained the full text (an improvement on S22-D's efetch route,
  same content).
- NCBI `oa.fcgi`: HTTP 404. The article's JSON metadata says `is_pmc_openaccess: false`.
- bioRxiv preprint 10.1101/2021.03.05.434157 (JATS XML, `.full`, `.full.pdf`): HTTP 429 "error code 1015"
  (Cloudflare rate-limit). Europe PMC `PPR293816/fullTextXML`: HTTP 500.
- Zenodo 10.5281/zenodo.5082978 (P1's only data deposit): proxy refused the connection (zenodo.org not
  reachable from this session). Per P1's key resources table it holds "Beloniformes assembled contigs",
  not morphometrics, so it would not contain Rz anyway.

Rz therefore stays **unknown**. I did not estimate it from P1's Fig 4A photograph because I could not
open that either.

### 3b. Replacing the assumed `p0` with a figure-read from the same lab: **improved**
D18 Fig 1A (open access, image read in full) plots pectoral-fin regrowth after amputation, in units
of "Growth/STL", for wild type (n = 4 DMSO, n = 5 FK506), `kcnk5b^alf/+` (n = 3 + 3) and `cx43^sof/sof` (n = 4 + 4).
Grey dashed lines mark each genotype's pre-cut reference.

**Figure-read (pixel-calibrated, not a reported number).** I located the dashed lines by scanning pixel
rows of the 750×547 JPEG. I calibrated the y-axis on the "0" and "0.18" tick labels (rows ≈501.7 and
≈186.7). Reads: **wt 0.104, alf 0.181, sof 0.043** (±≈0.003 from calibration). Visual check: the wt
DMSO curve ends at about 0.10 by day 21, the alf curves at about 0.18.

**Interpretation, which is my inference and has two readings.** The legend (author's text) says: "resection
to ~50% of pre-cut fin length … Dashed lines indicate pre-cut pectoral fin length. Data normalized to
standard length". The y-axis starts at 0 on the amputation day and plots *growth*.
- *Literal reading:* dashed = whole pre-cut fin/SL, so `p0` = 0.104. But then wild-type DMSO fins,
  cut to ~50%, would regrow 0.10 SL, which is twice the removed tissue. That contradicts the text ("regenerate back
  to their pre-amputation size", author's claim).
- *Consistent reading (the one I adopt):* the dashed line is the pre-cut length expressed as the growth
  needed to restore it, i.e. the resected part. Then `p0` = 0.104 / (fraction removed), which gives
  **`p0` ≈ 0.21 SL at 50%**, bracketed at **0.17–0.26** for 60%–40% removed (calculated). The
  legend's "~50%" is the only constraint on that fraction. In a different experiment, D18 Fig 2B starts
  at a regenerate/original of ≈0.35 at day 0, which hints that resection depth varied between
  experiments. I did not use that hint. The Fig 2B legend (author's text: "Dashed line, size of original
  pre-cut fin") uses a different y-metric (regenerate/original, with the dashed line at 1.0). It shows
  that "dashed line = pre-cut size" is the authors' wording for the restore-to target, which supports
  the consistent reading. Even so, this is an inference.
- Citation check: the D18 and P14 author lists, volumes and article numbers were confirmed against the
  Europe PMC records (PMID 29991812, 24453984).

I keep both readings in the table below and do not merge them.

### 3c. The fold overgrowth `f`: a proxy, stated as one
No source I could open gives the pectoral overgrowth of `kcnh2a^lof/+` (P2 abstract: "dramatically
elongated", no number). The nearest measured analogue is the other dominant bioelectric long-fin allele
from the same lab, `kcnk5b^alf/+`:
- Pectoral: 0.181 / 0.104 = **1.74×** (calculated from the D18 figure-reads; it does not depend on the resection
  fraction if that fraction was the same for both genotypes, which is an assumption).
- Caudal: P14 Fig 1E, eye-read (±≈0.02): wt (+/+;+/+) ≈ 0.19, alf/+ (+/+;alf/+) ≈ 0.39 → **≈2.05×**
  (calculated).

This is a **proxy**. `alf` is `kcnk5b`, not `kcnh2a`, and the double mutant also carries `lat4a^nr21/+`.
According to the author's text, `nr21/+` shortens all fins when alone, and in the double mutant it suppresses medial-fin overgrowth only.
Any shortening of the pectoral by `nr21/+` would make Rz *smaller* than the proxy predicts. The proxy
fails if `lof/+` overgrows pectoral fins by much more than about 2×. That is possible: P14 states that, unlike
alf, lof increases segment *number*, so it is a mechanistically different overgrowth (author's claim,
P14 text).

---

## 4. Recomputed (all calculated; inputs as in §3)

| `p0` reading | `p0` | Required fold FF/`p0` (FF 0.65–0.77) | Rz if `f` ≈ 1.74–2.05× (proxy) | Shortfall vs target |
|---|---|---|---|---|
| S22-D assumed grid | 0.10–0.25 | 1.4×* – 7.7× | — | — |
| Literal legend | 0.104 | 6.3× – 7.4× | 0.18 – 0.21 | 3.1× – 4.3× |
| 40% resected | 0.260 | 2.5× – 3.0× | 0.45 – 0.53 | 1.2× – 1.7× |
| **50% resected (adopted)** | **0.208** | **3.1× – 3.7×** | **0.36 – 0.43** | **1.5× – 2.1×** |
| 60% resected | 0.173 | 3.8× – 4.4× | 0.30 – 0.36 | 1.8× – 2.6× |

\*S22-D's 1.4× value used a halved target (0.35), not the flying-fish range.

What changes:
1. The required overgrowth narrows **from S22-D's 1.4–7.7× to about 2.5–4.4×** (calculated). With the
   literal legend reading it is 6.3–7.4×. S22-D's low end (1.4–1.75×) is no longer reachable with any
   `p0` read from D18.
2. The only *measured* dominant bioelectric pectoral overgrowth I could find (`alf/+`, a proxy) is
   **1.74×**. The caudal value is ≈2×. Even the most favourable row leaves a shortfall of ≥1.2×. The
   central row leaves 1.5–2.1×.
3. A **size confound** cuts the other way, and I could not quantify it. P1 (author's claim) shows that flying-fish
   pectoral/SL is allometric and rises with body size (Fig 1B). The 0.65–0.77 target comes from adult
   flying fishes many times longer than a ~3 cm zebrafish. The flying-fish value *at zebrafish SL* is
   **unknown** (P1 Data S1A could-not-access), and it would be lower than 0.65. A size-matched comparison could
   shrink the shortfall. I have no number for it.

**Verdict on S22-D: STRENGTHENS.** S22-D said the cross-species length match is verbal and could be off
by anywhere from "small" to 3–7×. With `p0` read from a same-lab figure instead of assumed, a flying-fish
proportion at adult flying-fish size needs about 3–4× pectoral overgrowth (calculated). The only measured
analogue of a single dominant bioelectric allele gives about 1.7–2×. So "closely phenocopies
proportions" is most likely a qualitative statement, short by roughly 1.5–2× in length/SL. This is an inference on a
proxy, not an observation. Two things could overturn it: (i) `kcnh2a^lof/+` pectoral overgrowth turns
out to be ≥3×, or (ii) a size-matched flying-fish comparator is far below 0.65. Both are unmeasured
here.

**What settles it, and the cost (my estimates):**
1. Read P1 Fig 4B and Data S1A from a browser that passes the PMC/Cell challenge (≤1 h). This gives Rz
   directly, plus flying-fish pectoral at small SL from the allometry. It costs nothing but access.
2. If the figure is unavailable, measure pectoral/SL in adult `lof^dt2/+` (ZIRC ZL86) and wild-type
   siblings: about 20 fish each, calipers, about one afternoon once fish are adult. This replaces the `alf` proxy for
   `f` and the inferred resection fraction for `p0`.

---

## Negative-search scope
- "No fold-change number for `kcnh2a^lof/+`": scope is the P2 abstract (Europe PMC), the P1 full text and
  the P14 full text (string search for "lof", "longfin", "fold"). Not searched: P2 full text, Iovine-lab
  papers, the ZFIN phenotype annotations (ZFIN unreachable through TLS in S22-D).
- "Rz unknown": scope is the access attempts listed in §3a.
- Flying-fish values were not re-checked in this pass. They remain search-summary as in S22-D.

```swarm-result
{"subproblem": "S22-D-D", "evidence": "figure-read from same-lab open-access primary figure (D18 Fig 1A, pixel-calibrated) for wild-type pectoral/SL; proxy allele (kcnk5b alf/+) for fold overgrowth; decisive double-mutant value still could-not-access; flying-fish target search-summary", "answer": "Replacing S22-D's assumed wild-type zebrafish pectoral/SL with a same-lab figure-read (~0.21 SL, range 0.17-0.26) means a flying-fish proportion (0.65-0.77 SL) needs ~2.5-4.4x pectoral overgrowth, while the only measured dominant bioelectric long-fin allele gives ~1.7-2x, so the Daane et al. 'phenocopy' most likely falls short by ~1.5-2x in pectoral length/SL (calculated on a proxy, size-confounded, not observed).", "key_number": "wild-type zebrafish pectoral fin length / SL ~0.21 (0.17-0.26), figure-read and inferred from Daane et al. 2018 Sci Rep Fig 1A regrowth target 0.104 SL at ~50% resection; alf/+ pectoral overgrowth 1.74x", "verdict": "strengthens", "depends_on": ["S22-D: Daane et al. 2021 never numerically compared zebrafish and flying-fish pectoral/SL (P1 full text)", "S22: genotype lat4a^nr21/+; kcnh2a^lof/+, length-only measurement (P1 Fig 4 legend)", "D18 Fig 1A dashed-line read: wt 0.104, alf/+ 0.181, sof 0.043 Growth/STL (pixel-calibrated figure-read)", "Interpretation that D18 Fig 1A dashed lines equal the resected part, not the whole pre-cut fin (my inference, contradicts literal legend)", "D18 legend: pectoral fins resected to ~50% of pre-cut length (author's claim; fraction bracketed 40-60%)", "Proxy assumption: kcnh2a^lof/+ pectoral overgrowth ~ kcnk5b^alf/+ overgrowth (1.74x pectoral, D18; ~2.05x caudal, Perathoner 2014 Fig 1E eye-read)", "Assumption: lat4a^nr21/+ does not shorten the pectoral fin in the double mutant (P1 text says nr21/+ alone shortens all fins)", "Equal resection fraction across genotypes in D18 Fig 1A (assumption)", "Flying-fish target pectoral/SL 0.65-0.77 for E. volitans (C1-C3, search-summary, sources disagree)", "Flying-fish pectoral/SL is allometric, rising with SL (P1 Fig 1B text); size-matched comparator unknown", "Double-mutant pectoral/SL Rz unknown (P1 Fig 4B could-not-access)"]}
```
