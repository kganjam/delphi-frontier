# S22-D-D-D: Deepening S22-D-D by attacking its weakest input (the wild-type pectoral/SL, `p0`)

**Parent (S22-D-D, dna):** *Deepen S22-D: attack its most sensitive input.*
**What S22-D-D recorded** (branch `claude/s22-d-sensitive-input-pwechp`, `docs/research/fish/S22-D-deepen.md`):
S22-D-D replaced S22-D's assumed `p0` grid (0.10–0.25) with a figure-read from Daane et al. 2018
Sci Rep Fig 1A. It took the wild-type dashed line (0.104 "Growth/STL") to be the *resected part* of
the fin, which gave **`p0` ≈ 0.21 SL (0.17–0.26)**. With that value, a flying-fish proportion
(0.65–0.77 SL) needs about 2.5–4.4× overgrowth, while the only measured dominant bioelectric allele
(`kcnk5b^alf/+`, used as a proxy) gives about 1.7–2.05×. Its conclusion was that the Daane et al. 2021
"phenocopy" most likely falls short by about 1.5–2× in pectoral length/SL. Verdict: STRENGTHENS.

I ran no experiment for this note. Every number below is (a) quoted from a source at the read-level
given, (b) carried over from S22-D-D with its original read-level, or (c) **calculated** by
`S22-D-D-deepen_calc.py` in this directory. Each sentence says which.

---

## 0. Sources and read-levels

| # | Source | Read-level | Used for |
|---|---|---|---|
| D18 | Daane JM et al. (2018) Sci Rep 8:10391, doi:10.1038/s41598-018-28450-6, PMC6039437 | **full-text** (PMC Open Data S3 `PMC6039437.1.txt`, sha256 `78de1309…a7da7`, re-downloaded and hash-matched to S22-D-D) | Re-read Fig 1A legend and Methods for the resection protocol |
| D18-fig | D18 Fig 1A image | **carried over** from S22-D-D (pixel-calibrated figure-read by S22-D-D, not re-read here) | Dashed-line reads: wt 0.104, alf/+ 0.181 |
| P1 | Daane JM et al. (2021) Curr Biol 31:5052, PMC9172250 | **full-text** (S3 `.txt`, sha256 `8192f58b…6a22`, hash-matched) | Confirmed that P1's text does not state a wild-type zebrafish pectoral/SL |
| PR17 | Praveenraj J, Kiruba R, Sibnarayan D, Lohith Kumar, Shailesh Kumar, Raymond Jesudoss, et al. (2017) *Danio rerio (Actinopterygii: Cypriniformes: Cyprinidae): A new record from Andaman Islands, India.* Acta Ichthyol. Piscat. 47(4):391–396, doi:10.3750/AIEP/02242 | **listing** (Crossref metadata: title, volume, pages, DOI, authors) + **search-summary** (Table 1 values, from a web-search summary of the ResearchGate copy). Full text **could-not-access**, see §3 | Independent pectoral-fin length %SL in wild *D. rerio* |
| P2 | Stewart S et al. (2021) Development 148:dev199384, PMC8217709 | **abstract** (carried over). Full text **could-not-access**: PMC S3 `PMC8217709.1/.2` returned 404, Europe PMC `fullTextXML` returned HTTP 500 | Whether `kcnh2a^lof/+` pectoral overgrowth is reported: **unknown** |
| C1–C4 | Flying-fish pectoral/SL (FAO ×2, fishesoftexas, Davenport) | **search-summary** (carried over, not re-read) | Target 0.65–0.77 SL; the sources disagree (0.65–0.70 / 0.70–0.75 / 0.73–0.77) |

---

## 1. The input S22-D-D's answer is most sensitive to

S22-D-D's conclusion rests on the predicted double-mutant pectoral/SL, `Rz = p0 × f`, compared against
the flying-fish target FF = 0.65–0.77. Because `Rz` is a product, its elasticity to `p0` and to `f` is
exactly 1 for each. Recomputing (calculated, with `p0` from §3 and `f` = 1.74–2.05):

- `p0` × 2 → `Rz` 0.67–0.98, which is **inside or above** the flying-fish range, so the "falls short"
  conclusion **flips**.
- `p0` × ½ → `Rz` 0.17–0.24, which is wild-type range, so the shortfall becomes about 3–4×.
- `f` × 2 → `Rz` 0.67–0.98, which also flips it.

So `p0` and `f` are **equally sensitive**. I attack `p0` first because it is the one whose recorded
value already carried an internal **factor-of-two ambiguity**. The *literal* legend reading gives
`p0` = 0.104. The *adopted* reading gives 0.21, which is 2.0× larger. S22-D-D chose the adopted
reading by inference, and that inference contradicts the literal legend wording. A factor of two on
this one input is exactly the difference between a shortfall of 1.5–2.1× and one of 3.1–4.3×.
The flying-fish target is less sensitive: its three disagreeing sources span only a factor of 1.18.

---

## 2. How well was `p0` established in S22-D-D?

- **Kind:** a **proxy with an interpretive step**. The measured quantity in D18 Fig 1A is *regrowth
  after ~50% resection, normalised to SL*. It is not whole-fin length/SL. To turn it into `p0`,
  S22-D-D had to (i) choose between two readings of the dashed line and (ii) divide by an assumed
  resection fraction (40–60%, from the legend's "~50%").
- **Read-level of the underlying number:** a pixel-calibrated figure-read, not a reported value.
- **What I re-confirmed (D18 full text, author's text):** the Methods say pectoral fins "were resected
  to roughly 50% their pre-cut length", measured "using handheld calipers", and "normalized to the fish
  standard length". The Results say fins "cut to 50% of their initial size … regenerate back to their
  pre-amputation size". These sentences support S22-D-D's adopted reading, but they do not prove it.
  The legend still says "Dashed lines indicate pre-cut pectoral fin length".
- **Honest grade:** **inferred from a single figure, with one unforced interpretive choice**. It was
  not an assumption repeated until it read as measured, because S22-D-D flagged the inference. But
  no direct whole-fin measurement of wild-type pectoral/SL backed it.

---

## 3. Improving it: finding a direct measurement of whole-fin pectoral length / SL

**Searches (scope stated):** three web searches ("adult zebrafish pectoral fin length standard length
ratio"; "Danio rerio pectoral-fin length % SL morphometric table"; a targeted search for PR17 Table 1),
plus string searches of the D18, P1 and P14 full texts. P14 contains **no** occurrence of "pectoral"
(string search of the S3 `.txt`). P1 gives no wild-type zebrafish pectoral/SL value in its text.
Developmental and microCT morphometrics papers returned by the searches report body ratios or larval
pectoral growth, not adult pectoral/SL (search-summary; not opened).

**Found: one independent direct measurement, at search-summary level.** Taxonomic descriptions report
"pectoral-fin length" as a percentage of SL, measured on whole, uncut fins. PR17 Table 1 is titled
"Morphometric and meristic characters of *Danio rerio* from Andaman Islands and topotypes" (title from
search-summary). It has three sample columns (North Andaman, Middle Andaman, mainland topotypes). The
search summary gives pectoral-fin length %SL as:

| Column (mapping to locality **unknown**; the search summary said the extracted layout was scrambled) | Range %SL | Mean ± SD |
|---|---|---|
| a | 19.6–22.5 | 20.7 ± 1.3 |
| b | 18.0–20.7 | 19.3 ± 0.9 |
| c | 18.2–25.8 | 23.8 ± 2.7 |

**Caveats, stated as caveats:**
1. **Read-level is search-summary.** I have not seen the table. The full text could not be accessed:
   `aiep.pensoft.net`, `doaj.org` and `krishi.icar.gov.in` were all refused by this session's network
   policy (CONNECT 403 or DNS not allowed). Europe PMC has no record (hitCount 0). Crossref confirmed
   only the bibliographic record. These numbers must be re-read from the PDF before anyone relies on
   them. The column-to-locality mapping and the n per column are **unknown**. The PR17 abstract
   (search-summary) says four Andaman specimens were collected, so n is small.
2. **Population differs.** These are wild Indian *D. rerio*, not the laboratory wild-type strain
   (AB/Tü-type) used in D18 and P1. Laboratory strains could differ. This is unmeasured here.
3. **Method differs.** Taxonomic "pectoral-fin length" is conventionally measured from the fin base to
   the tip of the longest ray. D18 used calipers on anaesthetised fish. That the two agree to within a
   few percent of SL is my inference. It is not a measured equivalence.
4. **Column c is odd.** A mean of 23.8 sits near the top of its 18.2–25.8 range, which is possible with
   small n but is also what a garbled extraction might produce. I keep it as reported and do not
   drop it.

**What it settles, as far as a search-summary can.** All three columns lie between 0.180 and 0.258 SL.
That is (calculated) inside S22-D-D's *adopted* bracket of 0.173–0.260. The *literal* reading (0.104)
sits below the lowest reported minimum by a factor of 1.73. My inference is that the literal reading of
D18 Fig 1A is very unlikely to be whole-fin pectoral/SL, and that S22-D-D's interpretive choice was
right. This inference rests on PR17 at search-summary level.

**What would fully settle `p0` and its cost (my estimates):**
- Read the PR17 PDF from a network that allows pensoft.net. This takes about 10 minutes and costs nothing.
- Better still, measure lab wild-type (the AB or Tü siblings used in P1) directly: pectoral-fin length
  and SL by calipers or photograph, in about 20 adults of 2.5–3.5 cm SL. That is about one afternoon
  in any zebrafish facility. It would also remove caveats 2 and 3.

**`f`, the other equally sensitive input, was not improved.** P2 (Stewart et al. 2021) is the paper that
would give a `kcnh2a^lof/+` overgrowth number. Its full text was could-not-access (S3 404, Europe PMC
500). A web search (scope: one standard search) returned only caudal-fin measurements for `lof`, and no
pectoral fold-change. `f` therefore remains the `alf/+` **proxy** (1.74× pectoral, ≈2.05× caudal), as in
S22-D-D.

---

## 4. Recomputed (all calculated by `S22-D-D-deepen_calc.py`)

| `p0` source | `p0` (SL) | Required fold FF/`p0` | `Rz` if `f` = 1.74–2.05 (proxy) | Shortfall vs 0.65–0.77 |
|---|---|---|---|---|
| S22-D-D literal reading | 0.104 | 6.25–7.40× | 0.18–0.21 | 3.05–4.26× |
| S22-D-D adopted (40–60% resected) | 0.173–0.260 | 2.50–4.45× | 0.30–0.53 | 1.22–2.56× |
| **PR17 means (search-summary)** | **0.193–0.238** | **2.73–3.99×** | **0.34–0.49** | **1.33–2.29×** |
| PR17 full ranges (search-summary) | 0.180–0.258 | 2.52–4.28× | 0.31–0.53 | 1.23–2.46× |

To reach even the low end of the flying-fish target at the PR17 means, `kcnh2a^lof/+` (with
`lat4a^nr21/+`) would need **2.7–3.4× pectoral overgrowth** (calculated). The only measured analogue
gives 1.74–2.05×.

**Verdict on S22-D-D: STANDS.** The independent value, wild *D. rerio* pectoral-fin length 18–26% SL
with means 19.3–23.8% (search-summary), falls inside S22-D-D's inferred 0.17–0.26. It excludes the
literal 0.104 reading. The recomputed shortfall, 1.3–2.3×, is essentially S22-D-D's 1.5–2.1×. I did
not grade this "strengthens" for two reasons. The corroborating source is only at search-summary level
with an unknown column mapping. And the other equally sensitive input, `f`, is still a proxy. This is a
calculation on a proxy and a search-summary value. It is not an observation of the double mutant,
whose pectoral/SL (P1 Fig 4B) is still **unknown**. The size confound that S22-D-D noted still applies,
unchanged: flying-fish pectoral/SL is allometric, so a size-matched comparator would be lower than 0.65
by an unknown amount.

**Next weakest input:** `f`, the `kcnh2a^lof/+` pectoral overgrowth. If it is ≥2.7–3.4×, the conclusion
falls. Settling it needs either P2's full text or Fig 4B of P1 read from a browser that passes the
PMC/Cell challenge, or caliper measurements of `lof/+` adults and their siblings.

---

## Negative-search scope
- "No direct lab-strain wild-type pectoral/SL": scope is three web searches (listed in §3), plus string
  searches of the D18, P1 and P14 full texts. Not searched: ZFIN phenotype data, Iovine-lab and
  Parichy-lab papers, FishBase morphometrics, or other *Danio* taxonomic revisions (Fang, Kullander).
  Those revisions are a likely further source of pectoral %SL for *D. rerio* comparison material.
- "No `kcnh2a^lof/+` pectoral fold-change": scope is one web search, plus the P2 abstract (carried over).
  P2's full text was not accessible.
- Flying-fish target values were not re-checked. They remain search-summary.

```swarm-result
{"subproblem": "S22-D-D-D", "evidence": "search-summary (independent wild D. rerio pectoral-fin length %SL, Praveenraj et al. 2017 Table 1, full text could-not-access, column mapping unknown) corroborating a same-lab pixel-calibrated figure-read (carried over); fold-overgrowth still a proxy allele; double-mutant value still could-not-access; all recomputation calculated", "answer": "An independent direct measurement of wild Danio rerio pectoral-fin length (18-26% SL, means 19.3-23.8%, search-summary) falls inside S22-D-D's inferred 0.17-0.26 SL and excludes the literal 0.104 reading, so the recomputed shortfall of the Daane et al. 2021 double mutant versus flying-fish pectoral/SL is ~1.3-2.3x (calculated on the alf/+ proxy), and S22-D-D's conclusion stands.", "key_number": "wild-type zebrafish pectoral-fin length / SL = 0.193-0.238 (column means; full range 0.180-0.258), Praveenraj et al. 2017 Acta Ichthyol. Piscat. 47:391 Table 1, search-summary", "verdict": "stands", "depends_on": ["Praveenraj et al. 2017 Table 1 pectoral-fin length %SL ranges 19.6-22.5, 18.0-20.7, 18.2-25.8 (search-summary, column mapping and n unknown)", "Assumption: wild Indian D. rerio pectoral/SL approximates lab wild-type strains (unmeasured)", "Assumption: taxonomic pectoral-fin length (base to longest ray tip) approximates D18 caliper fin length (unmeasured)", "S22-D-D: D18 Fig 1A dashed-line figure-read wt 0.104, alf/+ 0.181 Growth/STL (pixel-calibrated)", "S22-D-D inference: D18 Fig 1A dashed line equals resected part, not whole fin (now corroborated by PR17, search-summary)", "D18 Methods/legend: pectoral fins resected to ~50% of pre-cut length, caliper, normalised to SL (author's claim, full-text)", "Proxy: kcnh2a^lof/+ pectoral overgrowth ~ kcnk5b^alf/+ overgrowth 1.74x pectoral (D18) to ~2.05x caudal (Perathoner 2014 Fig 1E eye-read)", "Assumption: lat4a^nr21/+ does not shorten the pectoral fin in the double mutant (P1 text says nr21/+ alone shortens all fins)", "Equal resection fraction across genotypes in D18 Fig 1A (assumption, affects the 1.74x proxy)", "Flying-fish target pectoral/SL 0.65-0.77 for E. volitans (C1-C3, search-summary, sources disagree)", "Flying-fish pectoral/SL is allometric, rising with SL (P1 Fig 1B text); size-matched comparator unknown", "Double-mutant pectoral/SL Rz unknown (P1 Fig 4B could-not-access)", "S22-D: Daane et al. 2021 never numerically compared zebrafish and flying-fish pectoral/SL (P1 full text)", "S22: genotype lat4a^nr21/+; kcnh2a^lof/+, length-only measurement (P1 Fig 4 legend)", "Model: Rz = p0 * f (multiplicative, elasticity 1 in each)"]}
```
