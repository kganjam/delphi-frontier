# Challenge 182: adversarial review of claim S22-D (Daane et al. 2021, "phenocopy" of flying-fish fins)

**Claim under review** (written by someone else, source `harvest:deepen-s22-daane-fin-7dqlop`):

> Daane et al. measured pectoral and caudal length/SL only within zebrafish genotypes and never
> numerically compared the lat4a^nr21/+; kcnh2a^lof/+ value to flying-fish pectoral/SL, so the
> "phenocopy" is a qualitative cross-species match even for length, and the decisive zebrafish value
> remains unknown here. KEY: flying-fish target pectoral length about 0.65-0.77 x SL (E. volitans,
> search-summary, three sources disagree); zebrafish double-mutant pectoral/SL unknown (Fig 4B
> could-not-access). VERDICT: strengthens.
> Recorded evidence level: measured. Value: n/a.

**Outcome: WEAKENED.** The main factual statement holds up against the full text. Two things are
wrong with it: the evidence label, and the claim that one pectoral/SL number is "the decisive"
quantity.

## Sources and how much of each I read

| Source | Read-level | Notes |
|---|---|---|
| Daane JM et al. 2021, *Curr Biol* 31(22):5052–5061.e8, doi:10.1016/j.cub.2021.08.054, PMID 34534441, PMCID PMC9172250 (NIH author manuscript, PMC HTML) | **full-text** (text and figure captions) | I read the body text, all figure captions and the STAR Methods. |
| The same paper's figure images (Fig 1, Fig 4 JPGs on cdn.ncbi.nlm.nih.gov) | **could-not-access** | The proxy returned 403. I did not see the plotted points, axes or any reference lines. |
| Data S1A (museum fin and SL measurements of beloniforms) | **could-not-access** | Cell.com returned 403 and Europe PMC's full-text XML endpoint returned a 500 error. |
| Europe PMC metadata and abstract for PMID 34534441 | abstract | Confirms the abstract wording "closely phenocopies the observed fin proportions of flying fishes". |
| ZFIN figure pages (ZDB-PUB-210918-31) | search-summary | Live fetches failed: zfin.org gave a 503 and crick.zfin.org did not resolve. |
| NOAA repository copy (noaa/62581) | could-not-access | The host is outside the session's network allowlist. |

## 1. Arithmetic, redone independently

The claim does no arithmetic. The flying-fish range 0.65–0.77 × SL comes with no derivation, and I
found nothing to rebuild it from. Data S1A, which would hold the paper's own flying-fish fin and SL
values, could not be accessed. The flying-fish pectoral/SL ratio therefore stays **unknown** in my
review. I did not replace it with a number of my own.

## 2. What the full text says, against the claim

Quotes from the author manuscript, read in full:

- Fig 4 caption: "(B and C) Pectoral fin length (B) and caudal fin length (C) suppression of
  overgrowth in medial fin by lat4a mutation. In (B) and (C), length normalized by SL." The genotypes
  come from "a lat4a nr21/+ × kcnh2a lof/+ cross". Flying-fish data are not mentioned anywhere in
  the Fig 4 caption.
- Results ("Sufficiency of simple genetic changes…"): the double heterozygotes "show wild-type-sized
  medial fins, while the paired fins are overgrown… The overall fin phenotype… is thus remarkably
  similar to that of flying fishes, suggesting the interaction… is sufficient to phenocopy this key
  innovation". There is no number and no statistical test against flying fish.
- Flying-fish fin data appear only in Fig 1B/Data S1A. They are given as **static allometry**, not
  as a ratio: "we measured fin length as a function of body size (standard length)… the length of
  flying fish pectoral fins increases rapidly", and "the scaling of fin proportion may be fixed
  across all flying fishes".

**What survives (author's statement, checked against the text):** no sentence or caption in the full
text compares the double mutant's pectoral/SL with a flying-fish value. Fig 4B/C, as captioned,
normalize only within zebrafish genotypes. This conclusion rests on the text and captions only. I
could not see the Fig 4 image, so I cannot rule out a flying-fish reference line drawn on the plot
that the caption leaves out. Nothing in the caption suggests one.

## 3. Proxy check: the claim's "decisive value" is the wrong quantity (my inference)

The claim treats one zebrafish pectoral/SL number, compared with "0.65–0.77 × SL", as the decisive
test. I disagree, for three reasons:

- **The flying-fish metric is a slope.** The paper describes flying fish by how pectoral length
  scales with SL, and says that scaling "increases rapidly". Under positive allometry a single
  pectoral/SL ratio depends on body size. Comparing adult zebrafish (a few cm SL) with *E. volitans*
  (tens of cm SL) at one ratio mixes allometry with the phenotype. The better quantity is where the
  double mutant sits on a fin-length-vs-SL scaling relationship, or a ratio taken at matched
  ontogenetic stage. That is my inference. The paper does not run that analysis either.
- **The paper's "phenocopy" claim is about a pattern among fins.** The authors describe a
  non-additive, fin-type-specific pattern: paired fins overgrown, medial fins wild-type-sized, and a
  hypocercal caudal fin. That is a within-organism statement about proportions between fins, and the
  within-zebrafish Fig 4B/C measurements are the right kind of evidence for it. Calling a
  cross-species pectoral/SL value "decisive" judges the paper against a claim it does not clearly
  make. It does open that door with "closely phenocopies the observed fin proportions" in the
  abstract.
- **What does hold:** taken as a *quantitative* match of fin length to flying fish, the phenocopy is
  untested in the paper. The claim's "qualitative cross-species match even for length" is accurate
  on that narrower reading.

## 4. Evidence level: the label is wrong

The claim is recorded as **measured** with value n/a. That label is a defect:

- The claim is a statement about what a publication contains, so it is a literature reading, not a
  measurement. Its own source could not access Fig 4B.
- The only number in it, 0.65–0.77 × SL, is labelled **search-summary** with three sources that
  disagree. A search-summary range filed under "measured" is the defect the honesty floor names.
- Honest label: *literature read (full-text text and captions; figures and Data S1A
  could-not-access); the flying-fish ratio is search-summary and unverified here.*

The claim does keep the disagreement among its flying-fish sources ("three sources disagree")
instead of averaging it away. That part is correct.

## 5. Counter-examples and regimes missed

- **Within flying fishes:** the paper reports the same allometric scaling across two-wing and
  four-wing flying fishes. So a range given only for *E. volitans* is not obviously less
  representative, but the size-dependence point in §3 still applies.
- **Gliding halfbeaks:** *Euleptorhamphus* and *Oxyporhamphus* have intermediate scaling. If the
  double mutant's pectoral/SL fell in that intermediate range, "flying-halfbeak-like" would be a
  fairer description than "flying-fish-like". This cannot be decided without the Fig 4B values,
  which are **unknown**.
- **Other kinds of evidence:** I searched for a published quantitative zebrafish-vs-flying-fish fin
  comparison (one standard web search on "Daane flying fish kcnh2a lat4a zebrafish pectoral fin
  length standard length", plus the paper's own full text). Nothing turned up. That search was
  narrow; it does not show that no such comparison exists anywhere.

## Verdict

The core negative statement survives a full-text read of text and captions: the paper makes no
numerical cross-species comparison of pectoral/SL. The claim is **weakened** for two reasons:

1. its evidence level ("measured") misstates what is really a literature read containing a
   search-summary number;
2. it calls a single pectoral/SL ratio the "decisive" value. That ratio stands in for the right
   quantities: position on the allometric slope, which is how the paper actually describes flying
   fish, and the among-fin proportion pattern, which is what the paper's "phenocopy" claim is about.

The zebrafish double-mutant pectoral/SL remains **unknown**: the Fig 4 image and Data S1A could not
be accessed.

```swarm-challenge
{"claim_id": 182, "outcome": "weakened", "reason": "Full text confirms the paper makes no numerical zebrafish-vs-flying-fish pectoral/SL comparison, but the claim mislabels a literature read plus a search-summary range as 'measured' and treats a single size-dependent pectoral/SL ratio as decisive when the paper describes flying fish by allometric scaling and frames the phenocopy as a qualitative pattern of proportion among fins.", "corrected_value": null, "depends_on": ["Daane et al. 2021 Curr Biol 31:5052, PMC9172250 author manuscript: text and Fig 1/Fig 4 captions (full-text read)", "Fig 4 caption states B/C are length normalized by SL across zebrafish genotypes only (figure image could-not-access)", "Fig 1B/Data S1A present flying-fish pectoral length as static allometry vs SL (Data S1A could-not-access)", "Claim's own recorded evidence level 'measured' and its search-summary flying-fish range 0.65-0.77 x SL"]}
```
