# Challenge 7 — "Daane et al. phenocopied flying-fish FIN PROPORTIONS in zebrafish — proportions only, not lift or glide performance"

Claim source: `docs/research/fish/zebrafish-fin-genetics.md` §4 (branch
`claude/zebrafish-fin-genetics-0ihfi1`, commit `278a29aa`), lines 231–232 and 259–260.
Recorded evidence level: `literature`. Value: n/a.
Reviewer date: 2026-11-04.

**Verdict: WEAKENED.** The "not lift or glide performance" half holds up when checked against
the primary text. The "phenocopied … fin proportions" half reports the authors' qualitative
judgement as if it were a measured result. What the main text supports is a fin-type-specific
growth **pattern**. It does not support a match to flying-fish **magnitudes**. The recorded
evidence level was also not earned by the source file, which marks its own Daane citation as
search-summary.

---

## Sources and read-levels

| Source | Read-level | What I got |
|---|---|---|
| Daane et al. 2021, *Curr Biol* 31(22):5052–5061.e8, doi `10.1016/j.cub.2021.08.054`, PMC9172250 (author manuscript) | **full-text** for main text, Results and figure legends, characters 0–100,000 of the page. The remaining 49,104 characters were read too: they are references and back matter only. | Verbatim phrases quoted below. I used a fetch tool that summarises the page, so the quotes passed through a summariser. Re-check them against the PDF before citing. |
| Same paper, supplementary files `NIHMS1735542-supplement-1.pdf` and `-supplement-2.xlsx` | **could-not-access** | PMC returned a captcha page (HTTP 200, about 21 kB of HTML, not the file). The Europe PMC `supplementaryFiles` API returned "not open access". |
| Same paper, ZFIN figure record `ZDB-FIG-221222-35` (Fig. 4) | **could-not-access** | The `crick.zfin.org` mirror failed DNS (outside the session's network policy). The earlier S22 attempt on `zfin.org` returned HTTP 503. |
| `S22-dna.md` (branch `claude/s22-daane-fin-phenocopy-9l9y75`) | full-text (internal doc) | Used only to locate access attempts. Every substantive point below was re-checked against PMC myself. |
| Web search "kcnh2a lat4a zebrafish … swimming OR glide OR lift follow-up" | search-summary | Results: [ZFIN fig](https://zfin.org/ZDB-FIG-221222-35), [ZFIN figure summary](https://crick.zfin.org/action/publication/ZDB-PUB-210918-31/all-figures), [oceanbites](https://oceanbites.org/how-did-flying-fish-get-their-wings/). No follow-up locomotor study was found. |

---

## 1. Arithmetic

The claim contains no arithmetic and no number, so there was nothing to redo. I checked the one
nearby computation in the source file instead: lift ∝ L², mass ∝ L³ (§4, line 253). That is a
standard isometric scaling statement and is correct as a scaling argument. It is not part of
claim 7.

## 2. Is a proxy standing in for the quantity that matters?

Yes, and it is a stack of two proxies.

- **What was measured:** fin **length normalised to standard length (SL)**, for the pectoral and
  caudal fins (Fig. 4B–C per the legend; read-level full-text). The text does not report pelvic
  fins as quantified in zebrafish. The prose says only that "the paired fins are overgrown."
- **What "proportions" implies to a reader:** the fins are the right size relative to the body,
  i.e. near the flying-fish range. External anchor, *not* from Daane et al.: *Exocoetus volitans*
  pectoral fin is about 70–75% of SL (FAO guide, search-summary, via S22).
- **What gliding actually needs:** fin area, giving wing loading in N·m⁻², plus aspect ratio and
  spar stiffness. **Fin area was not measured.** I found no area, aspect-ratio or wing-loading
  quantity in the accessible text. Scope of that negative: the PMC main text and legends only;
  supplements and figure panels could not be accessed.

The claim's own caveat ("not lift or glide performance") already concedes the second proxy gap,
from proportion to performance. It does not flag the first gap, from what was measured to what
"proportions" implies. That first gap is where the weakening is.

## 3. Hidden assumption: "phenocopied proportions" means the proportions were reproduced

These are the authors' words, quoted from PMC full text (italics stripped):

- Summary: the interaction "closely phenocopies the observed fin proportions of flying fishes."
- Results: "sufficient to phenocopy this key innovation and organismal bauplan of flying fishes";
  the phenotype is "remarkably similar to that of flying fishes."
- Fig. 4 title: "sufficient to phenocopy the evolved flying fish fin allometry."
- Phenotype, Results: "the lat4a nr21/+;kcnh2a lof/+ fish show wild-type-sized medial fins, while
  the paired fins are overgrown." The caudal fin, "while generally wild type in size, is
  hypocercal, with an elongated ventral lobe."

I relaxed the assumption by asking whether the paper shows a quantitative match to flying-fish
proportions. In the text I could read, **it does not:**

- No pectoral-fin/SL value appears in the text for wild type, either single heterozygote, or the
  double heterozygote. The values are in figure panels and supplements I could not access, so the
  magnitude is `unknown`.
- The text makes **no quantitative comparison** between the mutants' fin/SL and the flying-fish
  allometry data in Fig. 1B. The resemblance is stated qualitatively. Scope: main text and
  legends; figure panels not seen. A panel overlaying the two datasets could exist and I would
  not have seen it.

My inference, separate from the authors' claim: the experimental result is a **pattern**
phenocopy. Paired fins grow out while medial fins stay at wild-type size, and the caudal fin
becomes hypocercal. That fin-type-specific pattern is what separates a flying-fish body plan from
a generic *longfin* zebrafish, and it is a real and interesting result. It is not evidence that
the zebrafish reached flying-fish fin-to-body ratios. The claim's wording ("phenocopied … FIN
PROPORTIONS", stated as fact without attribution) lets a reader take it as the stronger,
magnitude-level statement. The source file encourages that reading at line 259: "fin *proportion*
differences can be reached by simple allelic combinations."

A secondary point on terminology. The authors' Fig. 4 title says "allometry", which strictly
means a scaling relationship across body sizes. In the text I found no description of a mutant
size series. The claim's word "proportions" is therefore *more* conservative than the authors'
own wording, and that part of the claim is fine.

## 4. Is the evidence level honest?

- **The source file did not earn `literature` for this claim.** `zebrafish-fin-genetics.md` lists
  its Daane citation at read-level **search-summary** (lines 67 and 325). Lines 48–49 say: "treat
  this entire file as *unread-source* tier. It is a map of where to look, not evidence." Recording
  the claim as `literature` with no read-level overstates what that file had.
- **After my check, `literature` is defensible**, at read-level full-text for main text and
  legends and could-not-access for figures and supplements. The non-performance half is now
  supported at full-text. The magnitude half is `unknown` at any read-level.
- No calculated value is presented as measured, because the claim contains no numbers.

## 5. Counter-examples, regimes, taxa

- **Lift or glide measured on these mutants?** None found. Scope: one web search (results listed
  above) plus the full PMC text, in which gliding and flight are discussed only for flying fishes
  and cited to prior work. This is a weak negative. A citation-forward search of Daane et al.
  2021 was not run, because Google Scholar and Semantic Scholar were not tried. If such a study
  exists, the "not performance" half would need updating. I found nothing that contradicts it.
- **Four-wing flying fishes** (enlarged pelvic fins, e.g. *Cypselurus*) are part of the
  phenotype being "phenocopied". The zebrafish text says "paired fins are overgrown" but
  quantifies only pectoral and caudal fins. Whether pelvic enlargement reaches four-wing
  proportions is `unknown`.
- **Genotype scope:** the result is the double **heterozygote** `kcnh2a^lof/+ ; lat4a^nr21/+`,
  made by crossing two existing laboratory alleles. No flying-fish allele (e.g. the convergent
  Lat4a substitution the authors report from comparative genomics) was installed in zebrafish, as
  far as the main text shows.
- **An inconsistency elsewhere in the source file, not in claim 7:** line 67 says `lat4a nr21/+`
  "shortens all fins". The paper's double heterozygote has wild-type-sized medial and caudal fins
  alongside overgrown paired fins. That is fin-type-specific suppression of the *lof* overgrowth,
  which line 67 also calls a "Medial-fin suppressor". I did not verify the single-mutant
  `nr21/+` phenotype in isolation and leave this flagged rather than called wrong.

## Corrected wording

> Daane et al. 2021 report (authors' qualitative claim) that `kcnh2a^lof/+ ; lat4a^nr21/+`
> zebrafish "closely phenocopy" flying-fish fin proportions. What the accessible text shows is a
> fin-type-specific *pattern*: paired fins overgrown, medial fins wild-type size, caudal fin
> hypocercal. It is measured as fin **length/SL** for pectoral and caudal fins only. The
> magnitude is `unknown` (figure panels and supplements not accessible), and there is no
> quantitative comparison to flying-fish fin/SL, no fin area, and no lift, glide or locomotor
> test. Read-level: full-text (main text and legends); could-not-access (figures, Table S1).

---

```swarm-challenge
{"claim_id": 7, "outcome": "weakened", "reason": "The not-performance half holds at full-text, but 'phenocopied fin proportions' states the authors' qualitative judgement as fact: the accessible text gives no fin-length/SL magnitude and no quantitative comparison to flying-fish proportions, only a fin-type-specific growth pattern measured as length/SL in pectoral and caudal fins, and the source file had the citation only at search-summary read-level.", "corrected_value": null}
```
