# Challenge 164 — adversarial review of [S22-D-D]

**Claim under review (verbatim):** "[S22-D-D] Replacing S22-D's assumed wild-type zebrafish
pectoral/SL with a same-lab figure-read (~0.21 SL, range 0.17-0.26) means a flying-fish proportion
(0.65-0.77 SL) needs ~2.5-4.4x pectoral overgrowth, while the only measured dominant bioelectric
long-fin allele gives ~1.7-2x, so the Daane et al. 'phenocopy' most likely falls short by ~1.5-2x in
pectoral length/SL (calculated on a proxy, size-confounded, not observed)."

**Source:** `harvest:s22-d-sensitive-input-pwechp`. Recorded evidence level: unknown. Recorded value: n/a.

**Outcome: WEAKENED.** The claim's *direction* survives, and survives more robustly than the author
argues — it holds on both branches of an unresolved factor-of-two in its own key input. But the
headline interval `~1.5-2x` is not reproducible from the stated inputs, the upper required fold is
4.5x not 4.4x, the word "only" is false, and the wild-type anchor rests on a doubling that the
claim's own wording contradicts.

Nothing below is an observation of mine. Every number is either quoted from a source at the stated
read-level, or is my own arithmetic on the claim's stated inputs, labelled as such.

---

## 1. Arithmetic, redone independently from the stated inputs

Computed from the claim's stated inputs only (`python3`, shown in commit; I did not read the
author's working):

Required fold = (flying-fish pectoral/SL) ÷ (WT pectoral/SL).

| flying-fish | WT | required fold |
|---|---|---|
| 0.65 | 0.21 (central) | **3.095** |
| 0.77 | 0.21 (central) | **3.667** |
| 0.65 | 0.26 (favourable extreme) | **2.500** |
| 0.77 | 0.17 (adverse extreme) | **4.529** |

Shortfall = required fold ÷ 1.74:

| branch | shortfall |
|---|---|
| central, 0.65 | **1.779** |
| central, 0.77 | **2.107** |
| extreme favourable | **1.437** |
| extreme adverse | **2.603** |

Two discrepancies, both small but both in the same direction — the claim understates its own case:

1. The claim's required range is "~2.5-4.4x". The lower bound reproduces exactly (2.500). The upper
   bound is **4.529**, stated as 4.4 (−2.8%).
2. The claim's shortfall is "~1.5-2x". That is **neither** the central interval (1.78-2.11x) **nor**
   the full-extreme interval (1.44-2.60x). It is a narrower, lower blend of the two that I cannot
   reproduce by any consistent choice of inputs. In particular the lower bound 1.5 is unreachable at
   the central WT value: the minimum central shortfall is 1.78x. Getting to ~1.44 requires taking
   the favourable WT extreme (0.26) *and* the short flying-fish extreme (0.65) simultaneously, and
   that same consistency would push the upper bound to 2.60, not 2.

**This alone is a defect, not a quibble:** a stated interval that is not recoverable from the stated
inputs misreports the uncertainty, even though here it misreports it against the author's own thesis.
Corrected on the claim's own anchor: required **3.1-3.7x** central (**2.5-4.5x** extremes),
shortfall **1.8-2.1x** central (**1.4-2.6x** extremes).

---

## 2. The hidden assumption that carries the result: an unjustified ×2

The claim's WT anchor is `0.21 ≈ 2 × 0.104`, where 0.104 SL is described as the "**regrowth target**
0.104 SL at ~50% resection" in Daane et al. 2018 Fig 1A. The doubling is the load-bearing step, and
it is not stated as an assumption anywhere in the claim.

**Verified from the primary source** (Daane et al. 2018, *Sci Rep* 8:10391, PMC6039437; read-level:
**full-text** via PMC, figure caption quoted back verbatim): Fig 1A is "Regenerative growth of
zebrafish pectoral fins after resection to ~50% of pre-cut fin length at 0 days post amputation",
and "Data normalized to standard length (STL) of each fish." Resection was "to roughly 50% their
pre-cut length using standard surgical scissors", measured with handheld calipers, STL defined snout
tip to posterior caudal peduncle. **The paper states no numeric axis values for Fig 1A** — the only
numbers in the Fig 1 text are `F(2,23) = 27.89, p < 0.0001` and pairwise p-values. So the y-axis
values exist only in the figure image.

Fig 1A is therefore a *time course* of pectoral fin length/STL, rising from the resected state toward
restoration. That gives two incompatible readings of "0.104 SL":

- **(a) plateau/asymptote reading** — 0.104 is the length regrowth restores, i.e. **0.104 *is* the
  wild-type pectoral/SL**, and multiplying by 2 double-counts the resection, inflating WT by 2x.
- **(b) 0-dpa reading** — 0.104 is the immediately-post-resection value (~50% of full), and ×2
  correctly recovers 0.208.

The claim's own phrase, "**regrowth target**", denotes (a). A target is the endpoint regrowth aims
at, not the remaining stump. **On its own wording, the claim's doubling is unjustified.**

I could not settle which trace or time point 0.104 was read from. **Read-level for the figure image:
could-not-access.** Scope of that failure: `media.springernature.com` (proxy `connect_rejected`),
PMC image host `pmc.ncbi.nlm.nih.gov/articles/instance/...` (403 via proxy), `www.nature.com` PDF
(403), `biorxiv.org` PDF (HTTP 429), `digitalcommons.wustl.edu` mirror (403), ZFIN all-figure-view
(HTTP 503). So I **cannot assert that the author made an error** — only that the claim as written is
internally inconsistent, and that one of the two readings halves its anchor.

### Relaxed test — the result on the other branch

If WT pectoral/SL = 0.104 (plateau reading), from my arithmetic:

| | required fold | shortfall vs 1.74x |
|---|---|---|
| 0.65 SL | **6.250** | **3.592** |
| 0.77 SL | **7.404** | **4.255** |

The claim's *qualitative* verdict is **robust** to relaxing the assumption — it falls short either
way, and ~2x further short on the branch its own wording implies. But the claim quotes only the
*least adverse* branch as its headline number, without flagging that a branch exists.

**Independent plausibility note (my inference, not an observation, and uncited):** a pectoral fin at
0.21 SL would be about as long as the zebrafish caudal fin; in *Danio rerio* the pectoral fin is
conspicuously shorter than the caudal. That favours (a). **I could not locate a published numeric
adult wild-type pectoral-fin-length/SL value to settle it.** Scope of that negative search: WebSearch
(standard and extended) on zebrafish pectoral morphometrics; full-text reads of PMC13432094 (microCT
morphometrics — "not stated"), PMC11018282 (PLoS Biol pectoral fin buds — bud-area/eye-area only,
"not stated"), PMC3894163, PMC6039437; McHenry & Lauder 2006 (`bpb-us-e1.wpmucdn.com` does not
resolve in this session — would need network allowlisting). **So the single most decisive number for
this claim is, on my search, unpublished in accessible form — which is itself the finding.**

---

## 3. Proxies standing in for the quantity that matters

The claim flags "proxy, size-confounded" generically. Three specific substitutions, two of which the
flag does not cover:

### Proxy 1 — `alf/+` fold overgrowth, and a number-shaped trap

The claim attributes "1.74x" to `kcnk5b alf/+` pectoral overgrowth without naming the source figure.
Checking the obvious source: **Perathoner et al. 2014, *PLoS Genet* 10:e1004080** (PMC3894163;
read-level: **full-text**, first 100,000 of 118,025 chars):

- It reports **no fold-change for fin size at all**.
- It **does not mention pectoral fins** — "The article discusses caudal and dorsal fins and barbels."
- Its quantitative allometry is **caudal**: wild type `k = 1.29`; `alf` heterozygotes `k` "near 2".
- **The "almost two-fold" number in that paper is K⁺ conductance in oocytes, not fin size.**

That last point matters: a ~1.7-2x figure of exactly the claimed magnitude exists in the nearest
source and refers to **ion conductance**. I cannot determine whether 1.74x came from Daane 2018
Fig 1A (which does plot pectoral fins for `alf`), from a caudal allometric coefficient, or from the
conductance number. **The claim does not say, and the registry record carries evidence level
"unknown".** If it is the conductance or caudal number, the proxy is wrong in *kind*, not degree.

**The right quantity:** adult `alf/+` pectoral length/SL ÷ WT pectoral length/SL. It is available in
the same figure the claim already used. Reporting it as a same-figure ratio with *both* values given
would also have made the §2 doubling question self-evident — the ratio is invariant to it, the
denominator is not.

### Proxy 2 — a 1-D length ratio standing in for an aerofoil

A flying-fish pectoral is a load-bearing wing. The functional quantity is **wing area and aspect
ratio relative to body mass** (wing loading), not a length ratio. An allele scaling fin *length*
1.74x does not deliver an exocoetid wing. Independently, a NE Atlantic exocoetid morphometric study
reports a **maximum pectoral length of 78-79% SL before swimming is impaired**, and that the wing
leading edge is **fixed at 24% SL from the snout** (read-level: **search-summary** only; I did not
reach the paper). So the phenotype includes fin *insertion position* and geometry, which no `kcnk5b`
allele addresses. The claim's "size-confounded" caveat concerns scale, not dimensionality or position.

### Proxy 3 — fin/SL treated as scale-invariant across a ~10x body-size gap

Zebrafish SL is ~3 cm; exocoetids are ~20-30 cm. Zebrafish pectoral span/area scales **positively
allometrically** — McHenry & Lauder 2006 report a span exponent ≈1.44 (read-level: **search-summary**;
host unreachable, see §2). If fin/SL is not scale-invariant, the "required fold" is itself a function
of the body size at which it is evaluated, and the single-number comparison is ill-posed.

---

## 4. Is the evidence level honest?

Mostly yes, with four defects:

1. **The range "0.17-0.26" is presented inside the figure-read parenthesis**, but a pixel read of one
   plotted value cannot produce a band. Its provenance is unstated (it is ≈ ±20% around 0.208).
   Should be marked derived/assumed, not figure-read.
2. **"the only measured dominant bioelectric long-fin allele" is asserted flatly, unhedged, with no
   read-level.** An exclusivity claim is an empirical claim. It is false — see §5.
3. **The record carries `value: n/a` and `evidence level: unknown` while the claim text states a
   numeric verdict (~1.5-2x).** The load-bearing number lives only in prose. That is a record-level
   defect independent of the science.
4. **"same-lab figure-read" does rhetorical work** it cannot support — same-lab provenance does not
   convert a pixel read of an unlabelled axis into a measurement. The claim does say "not observed",
   which is to its credit.

---

## 5. Counter-examples the author missed

### The word "only" fails: at least one other dominant bioelectric long-fin allele

**`longfin` (`lof`)** — dominant, bioelectric, mechanistically distinct: cis-ectopic expression of
**`kcnh2a`** (ether-a-go-go K⁺ channel). Stewart et al. 2021, *Development* 148(11), "longfin causes
cis-ectopic expression of the kcnh2a ether-a-go-go K+ channel to autonomously prolong fin outgrowth"
(read-level: **search-summary** + ZFIN listing `ZDB-PUB-210602-7`; I did not reach the full text).
Reported mechanism: overgrowth comes from a **prolonged outgrowth period, not a higher maximal growth
rate**; and unlike `alf`, `lof` **adds segments** whereas `alf` elongates existing ones
(Perathoner 2014, full-text: "In contrast to other fin overgrowth mutants such as lof or rpz, the
number of segments is not increased in alf").

This is not a bookkeeping correction. The claim treats 1.74x as *the* biological ceiling. It is the
ceiling of **one** mechanism (rate/segment-length). A duration-limited mechanism has a different
ceiling, and the two are not obviously redundant. **I did not find a quantified `lof/+` pectoral
fold-change** (scope: the searches in §2 plus a targeted `lof`/`kcnh2a` search), so I cannot say
whether it exceeds 1.74x — only that the claim's ceiling is one allele's ceiling, presented as the
field's.

**`schleier` (`schl`)** — `kcc4a` (K⁺-Cl⁻ cotransporter) loss of function, "proportional overgrowth",
phenotypically close to `alf`, with `kcnk5b` required for the `schleier` effect (Lanni/Harris and
colleagues; read-level: **search-summary**; the bioRxiv full text `10.1101/621243` returned HTTP 429,
**could-not-access**). It is described as a missense/loss-of-function allele and **I could not confirm
dominance**, so I do **not** count it against the claim's wording. Flagged as unresolved.

### The claim's own source paper reports a route past the ceiling

Daane et al. 2018's headline result is that **calcineurin inhibition (FK506) overrides genetic size
specification** — "inhibition of calcineurin is able to bypass genetic instruction of size as seen in
sof and wild-type fins" (read-level: **full-text**/abstract via PMC). The claim takes its WT
denominator from that paper's figure while treating an allele's 1.74x as a hard ceiling, which sits
awkwardly with the paper's own conclusion. **No fold-change for FK506-driven overgrowth is stated in
the text I read** ("not stated"), so I cannot claim it reaches 3-7x. The point is narrower: the
ceiling argument is less settled than the claim presents it.

### Taxon regime: exocoetid pectoral/SL is not uniformly 0.65-0.77

FAO species identification sheets for Exocoetidae (read-level: **search-summary** of the FAO sheets;
I did not open the PDFs, and the search summary itself warns the species-to-value mapping is
fragmented and unverified) give a **spread, not a point**: ~55-60% SL for some genera, 65-70% for
others, and *Cheilopogon* at a ratio of "1.25 to 1.35 in standard length" ≈ 74-80% SL. Two-winged and
four-winged flying fish differ.

**Preserving the disagreement rather than averaging it:** 0.65-0.77 selects the long-winged end. At
the family floor of ~0.55 SL, my arithmetic gives required fold **2.62x** and shortfall **1.51x** on
the 0.21 anchor (or 5.29x / 3.04x on the 0.104 anchor). So the claim's ~1.5x lower bound *is*
reachable — but only by a taxon substitution the claim does not make, not by the WT range it cites.
This cuts both ways and is the strongest available defence of the claim's lower bound.

---

## Summary of what survives and what does not

| Component | Status |
|---|---|
| Direction: phenocopy falls short in pectoral length/SL | **Survives**, on both branches of §2 |
| Required fold "~2.5-4.4x" | Upper bound should be **4.5x** |
| Shortfall "~1.5-2x" | **Not reproducible**; central 1.8-2.1x, extremes 1.4-2.6x |
| WT anchor 0.21 = 2 × 0.104 | **Doubling unjustified on the claim's own wording**; branch unresolved (figure could-not-access) |
| Range "0.17-0.26" as figure-read | **Provenance unstated**; cannot be a figure read |
| "only measured dominant bioelectric long-fin allele" | **False** — `lof`/`kcnh2a` (Stewart 2021) |
| 1.74x attributed to `alf/+` pectoral | **Source unidentified**; nearest source has no pectoral data and a ~2x *conductance* number |
| Flying-fish 0.65-0.77 SL | **Corroborated** for long-winged taxa; family spread is wider (~0.55-0.80) |
| "calculated on a proxy, not observed" caveat | **Honest and correct** |

I did not break the claim's conclusion. I did break its number, its exclusivity clause, and the
provenance of its key input. Had the doubling gone the other way the claim would have been
*strengthened*, not refuted — which is why this is weakened rather than refuted.

```swarm-challenge
{"claim_id": 164, "outcome": "weakened", "reason": "Direction survives on both branches, but the stated shortfall interval ~1.5-2x is not reproducible from the stated inputs (central 1.8-2.1x, extremes 1.4-2.6x), the upper required fold is 4.5x not 4.4x, the WT anchor rests on a x2 of a value the claim itself calls a 'regrowth target' (which would already be full length, making the shortfall ~3.6-4.3x), and 'the only measured dominant bioelectric long-fin allele' is false since lof/kcnh2a is also dominant and bioelectric.",
  "corrected_value": "required overgrowth 3.1-3.7x central (2.5-4.5x extremes) and shortfall 1.8-2.1x central (1.4-2.6x extremes) IF WT pectoral/SL=0.21; shortfall 3.6-4.3x if 0.104 SL is the restored-length plateau as the claim's 'regrowth target' wording implies -- branch unresolved, figure image inaccessible",
  "depends_on": ["Daane et al. 2018 Sci Rep 8:10391 Fig 1A caption: zebrafish PECTORAL fins, resected to ~50% of pre-cut length, data normalized to STL, no numeric axis values in text (read-level: full-text via PMC6039437)", "the unverified figure-read value 0.104 SL from D18 Fig 1A, and which time point/trace it was read from (read-level: could-not-access for the figure image; springernature/nature/PMC-image/biorxiv/WUSTL/ZFIN all blocked, 403/429/503)", "flying-fish pectoral/SL = 0.65-0.77 (corroborated at search-summary level from FAO Exocoetidae identification sheets, which also give ~0.55-0.60 for some genera and ~0.74-0.80 for Cheilopogon)", "alf/+ pectoral fin overgrowth = 1.74x, source figure and fin unidentified by the claim", "Perathoner et al. 2014 PLoS Genet 10:e1004080 reports no fin-size fold change and does not mention pectoral fins; its 'almost two-fold' value is oocyte K+ conductance; caudal allometry k=1.29 (wt) vs near 2 (alf/+) (read-level: full-text, first 100k of 118k chars)", "Stewart et al. 2021 Development 148(11): longfin/lof is a dominant bioelectric (kcnh2a) long-fin allele acting by prolonged outgrowth duration rather than increased maximal rate (read-level: search-summary + ZFIN listing)", "the absence of any located published numeric adult wild-type zebrafish pectoral-fin-length/SL value (negative search scope stated in section 2)", "unresolved dominance of schleier/kcc4a (read-level: search-summary; bioRxiv 10.1101/621243 could-not-access, HTTP 429)", "Daane et al. 2018's own report that calcineurin inhibition bypasses genetic size specification, with no fold-change stated in the accessible text"]}
```
