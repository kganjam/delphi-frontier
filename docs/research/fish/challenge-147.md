# Challenge 147 — adversarial review of S22-D-D-D (wild-type zebrafish pectoral/SL)

**Claim under review (S22-D-D-D, harvest `deepen-s22-d-d-j5x0vq`, not written by me):**
> An independent direct measurement of wild *Danio rerio* pectoral-fin length (18–26% SL, means
> 19.3–23.8%, search-summary) falls inside S22-D-D's inferred 0.17–0.26 SL and excludes the literal
> 0.104 reading. So the recomputed shortfall of the Daane et al. 2021 double mutant against
> flying-fish pectoral/SL is about 1.3–2.3× (calculated on the alf/+ proxy), and S22-D-D's
> conclusion stands.

**Outcome: WEAKENED.** The direction of S22-D-D's conclusion survives every test I could run: the
double mutant falls short of flying-fish pectoral/SL. The sub-claim that does not survive as stated
is this one: "an independent direct measurement … excludes the literal 0.104 reading". I found a
second independent direct measurement of wild *D. rerio*. It disagrees with the first, and one of
its population means falls *below* 0.104. The author's narrow 1.3–2.3× therefore rests on one
source at search-summary level, chosen over a source that disagrees with it. Neither source is
good enough to choose between them.

I ran no experiment. Every number below is quoted at a stated read-level or **calculated** by me
from those quoted inputs. Each sentence says which.

---

## 1. Independent arithmetic (calculated)

I used the stated inputs: flying-fish target FF = 0.65–0.77 SL, `f` = 1.74–2.05 (alf/+ proxy),
`Rz = p0 × f`, and shortfall = FF / Rz taken across the extremes.

| `p0` input | `p0` (SL) | Rz | Shortfall | Matches author? |
|---|---|---|---|---|
| Praveenraj 2017 column means | 0.193–0.238 | 0.336–0.488 | 1.33–2.29× | yes |
| Praveenraj 2017 full ranges | 0.180–0.258 | 0.313–0.529 | 1.23–2.46× | yes |
| `f` needed for Rz = 0.65 at PR17 means | — | — | 2.73–3.37× | yes |

The containment test passes, but only by small margins (calculated): 0.180 ≥ 0.173 by 0.007 SL,
and 0.258 ≤ 0.260 by 0.002 SL. The author's arithmetic is correct. I found no arithmetic fault.

## 2. Proxies

- **`p0`.** The claim uses wild Indian *D. rerio* to stand in for lab-strain wild-type siblings,
  which are the fish actually compared in Daane et al. 2021. The author flags this. The right
  quantity is the wild-type sibling pectoral/SL in Daane 2021 Fig 4B. The double-mutant value
  itself would make `p0` and `f` unnecessary.
  - I tried to read Fig 4B and Data S1. The PMC article HTML loaded, but the figure CDN
    (`cdn.ncbi.nlm.nih.gov`) was refused by this session's proxy. The Data S1 xlsx on
    `pmc.ncbi.nlm.nih.gov` returned a JavaScript "Preparing to download" page, not the file.
    Europe PMC `fullTextXML` returned HTTP 500, and the europepmc.org bin link returned 403.
    The PMC S3 bucket holds only `.txt/.xml/.json`, with no figures.
  - Result: double-mutant pectoral/SL is **unknown** (could-not-access). I did confirm the P1
    full text myself (S3 `PMC9172250.1.txt`, sha256 `8192f58b…6a22`, matching the author's hash).
    Its Fig 4 legend says "(B) Pectoral fin length … normalized by SL". So the decisive number
    exists, but only in a figure I could not reach.
- **`f`.** This is the `kcnk5b^alf/+` overgrowth, standing in for `kcnh2a^lof/+` combined with
  `lat4a^nr21/+`. The author flags this too. I did not improve it. A single search (scope below)
  found no pectoral fold-change for `lof/+`.

## 3. Hidden assumption, relaxed: that the Praveenraj value is *the* wild-type value

The claim treats one source as "an independent direct measurement" that settles `p0`. I looked for
a second one and found it.

**Islam MK, Badruddoza M, Salam SB, Alam MS, Kabir MA, Rabbane MG (2025).** *Genetic variation of
three wild zebrafish population (Danio rerio) in Bangladesh.* Front. Ecol. Evol. 13:1582204,
doi:10.3389/fevo.2025.1582204. **Read-level: full-text, read through a fetch-tool extraction of
the HTML Table 2. I did not see the rendered table.** The extracted Table 2 gives, in cm, as
mean ± SD with n ≈ 3 per population:

| Population | SL | Pectoral-fin length | Pectoral/SL (calculated from the means) |
|---|---|---|---|
| Rangpur | 3.36 ± 0.10 | 0.563 ± 0.055 | 0.168 |
| Netrokona | 3.846 ± 0.047 | 0.363 ± 0.032 | **0.094** |
| Cumilla | 3.39 ± 0.06 | 0.476 ± 0.045 | 0.140 |

**The two sources disagree, and I keep both.** All three Islam ratios (calculated) lie *below*
S22-D-D's adopted bracket of 0.173–0.260. The Netrokona ratio, 0.094, is *below* the literal 0.104
reading that the claim says is excluded. Recomputed with the Islam means, `p0` = 0.094–0.168 gives
Rz = 0.164–0.343 and a shortfall of **1.89–4.69×** (calculated).

**Reasons to distrust Islam 2025. I state these, but I do not use them to discard the source.**
1. TL − SL is only 0.09–0.23 cm (calculated from its table). The zebrafish caudal fin is far
   longer than that. This is my inference from general anatomy, not a measured value. It points to
   an inconsistent length definition or measurement in the table.
2. The paper gives no measurement method (fetch extraction).
3. n is about 3 per site.

**Reasons to distrust Praveenraj 2017, all already stated by the author.** The table was read
through a search summary only. The extracted layout was scrambled. The column mapping and n are
unknown. Column c is odd: its mean of 23.8 sits near the top of an 18.2–25.8 range. I add one
risk the author did not name. Because the layout was scrambled, the 18–26 %SL values could belong
to a neighbouring row. In cyprinid tables head length often falls in a similar %SL band. This is
my inference and is unverified. I tried to read the table myself: `aiep.pensoft.net` failed DNS,
`krishi.icar.gov.in` and `researchgate.net` were refused by the proxy, and one web search returned
the bibliographic record but not the table values.

**Effect.** The claim's wording, "an independent direct measurement … excludes the literal 0.104
reading", overstates what the evidence shows. The direct whole-fin evidence for wild *D. rerio*
pectoral/SL is two low-quality sources that disagree: about 0.09–0.17 versus about 0.18–0.26.
That evidence neither confirms S22-D-D's adopted 0.17–0.26 nor excludes 0.104. Corroborating
the adopted reading over the literal one still depends on the D18 Methods wording ("resected to
roughly 50%"), as it did in S22-D-D.

## 4. Does this flip the conclusion? No.

Lowering `p0` *increases* the shortfall. Every `p0` value from either source is ≤ 0.258. So the
conclusion flips only if `f` ≥ 2.52 (calculated at 0.258), and at Islam values `f` would have to
be ≥ 3.9. The direction of "falls short" is therefore *more* robust to the source disagreement,
not less. It still rests entirely on the unverified `f` proxy and on the untested assumption that
the multiplicative model `Rz = p0 × f` holds. The author already named `f` as the next weakest
input, and I agree.

## 5. Evidence level

The claim text labels its levels honestly: search-summary, calculated, and proxy. **The ledger
record does not.** It shows `evidence level: unknown`, `value: n/a`. It should read
"search-summary (p0) + calculated (shortfall) + proxy (f)". This is a recording defect in the
ledger, not in the author's note.

## 6. Counter-examples and regimes

- Islam et al. 2025, above, is a published counter-example to the claim that the reading is
  "excluded".
- Lab versus wild strains: I found no direct lab-strain adult pectoral/SL value.
- Size or allometry: zebrafish of 3.3–3.9 cm SL (Islam 2025) are larger than many lab adults.
  The direction of any pectoral allometry in *D. rerio* is **unknown**.

## Negative-search scope
- Lab-strain wild-type adult pectoral/SL: two web searches (one standard, one extended). A 2024
  bioRxiv preprint ("Independent size regulation of bones and appendages in zebrafish",
  10.1101/2024.03.27.587111) was returned but could not be read (HTTP 429, two tries).
  Not searched: ZFIN, Fang/Kullander *Danio* revisions, FishBase morphometrics.
- Daane 2021 Fig 4B and Data S1: attempts listed in §2, all could-not-access.
- Praveenraj 2017 Table 1: attempts listed in §3, all could-not-access.
- Flying-fish target 0.65–0.77: not re-checked. It remains search-summary, carried over.

## Sources (read-levels)
- Daane et al. 2021 Curr Biol, PMC9172250. **Full-text** (S3 txt, hash-matched). Figure and
  Data S1: **could-not-access**.
- Praveenraj et al. 2017 Acta Ichthyol. Piscat. 47:391. **Listing** (Crossref, re-fetched) plus
  **search-summary** for the table values.
- Islam et al. 2025 Front. Ecol. Evol. 13:1582204. **Full-text**, read through a fetch-tool
  extraction.
- The S22-D-D-D note itself (`claude/deepen-s22-d-d-j5x0vq`). **Full-text**.

```swarm-challenge
{"claim_id": 147, "outcome": "weakened", "reason": "Arithmetic and the direction of the shortfall hold, but a second independent wild D. rerio measurement (Islam et al. 2025, pectoral/SL 0.094-0.168, calculated from table means, n~3/site, internally suspect) disagrees with the single search-summary source, so the claim that direct measurement excludes the literal 0.104 reading and pins the shortfall at 1.3-2.3x is overstated.", "corrected_value": "shortfall ~1.2-4.7x across disagreeing p0 sources (calculated on the alf/+ proxy; 1.23-2.46x with Praveenraj 2017, 1.89-4.69x with Islam 2025); wild-type pectoral/SL 0.09-0.26 SL, unresolved", "depends_on": ["Praveenraj et al. 2017 Table 1 pectoral-fin length %SL 18.0-25.8, means 19.3-23.8 (search-summary, column mapping unknown)", "Islam et al. 2025 Front Ecol Evol 13:1582204 Table 2 SL and pectoral-fin length means (full-text via fetch extraction, n~3/site, TL-SL inconsistency)", "Proxy f = kcnk5b alf/+ overgrowth 1.74-2.05x (carried over from S22-D-D)", "Flying-fish pectoral/SL 0.65-0.77 (search-summary, carried over)", "Model Rz = p0 * f (multiplicative)", "Daane et al. 2021 Fig 4B double-mutant pectoral/SL unknown (could-not-access)"]}
```
