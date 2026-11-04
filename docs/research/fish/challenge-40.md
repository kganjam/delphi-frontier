# Challenge 40: Daane et al. measured length/SL only, fin area was never reported, and no lift, glide or flight was tested

Reviewer date: 2026-11-04. Target: claim 40, recorded evidence level `literature`,
source `docs/research/fish/S22-dna.md` (branch `claude/s22-daane-fin-phenocopy-9l9y75`).

> **CLAIM:** "CRITICAL GAP: Daane et al. measured fin LENGTH normalised to standard
> length only. Fin AREA was never reported by the authors at all, and no lift,
> gliding or flight was measured. The one published genetic precedent does not
> supply the quantity the aerodynamics needs."

**Verdict: WEAKENED.** The core point holds. The zebrafish phenocopy is a linear
fin-length result, and the paper tests no aerodynamic or locomotor property. Two
parts of the wording go beyond the evidence:

1. "never reported … at all" turns a negative search that could not reach the
   figures or the supplement into a statement about the whole paper.
2. "normalised to SL only" is not literally true.

The claim also says area is "the quantity the aerodynamics needs". That is
itself a proxy. See the sections below.

---

## Sources and read-levels

| Source | What I did | Read-level |
|---|---|---|
| Daane et al. 2021, *Curr Biol* 31:5052–5061.e8, `10.1016/j.cub.2021.08.054`, PMC author manuscript PMC9172250 | Fetched both halves of the page (0–100k and 100k–149k characters). Searched for area, length, SL, Table S1, lift, glide, swimming, aspect ratio and ImageJ/Fiji. | **full-text** for the main text, the main figure legends and the STAR Methods. The text of supplementary figure legends S1–S4 and Table S1 is not in the manuscript. |
| Europe PMC `PMC9172250/supplementaryFiles` and `/fullTextXML` | REST API | **could-not-access**: "Article with id PMC9172250 is not open access one" / HTTP 500 |
| bioRxiv preprint `10.1101/2021.03.05.434157v1.full` | WebFetch, then curl | **could-not-access** in this session (HTTP 429 twice). S22 reports reading it. I did not re-verify that. |
| Europe PMC record PPR293816 (the same preprint) | search API | **listing**. The record is not open access and has no full text. |
| ZFIN `ZDB-FIG-221222-35` (Fig. 4), `-34` | WebFetch | **could-not-access** (HTTP 503). `franklin.zfin.org` is outside this session's allowed network domains. |
| ZFIN Fig. 4 legend snippets returned by web search | search | **search-summary**: "Panels B and C report pectoral fin length and caudal fin length … length normalized by SL"; D–E are qRT-PCR |
| Quanta Magazine, 2022-01-05, "Flying Fish and Aquarium Pets Yield Secrets of Evolution" | search | **search-summary** |
| Fish 1990, *J. Zool.* (wing design) | search | **search-summary** |

---

## 1. Arithmetic, redone independently

The claim itself contains no arithmetic. S22 §3 supplies the only numbers the
claim relies on. The author's stated inputs are a fractional fin-length increase
*f*, constant fin shape and fixed mass. Here are the results recomputed from those
inputs (a calculation, not an observation):

| *f* | area factor (1+*f*)² | wing-loading factor 1/(1+*f*)² |
|---|---|---|
| 0.25 | 1.5625 | 0.640 |
| 0.50 | 2.25 | 0.444 |
| 1.00 | 4.00 | 0.250 |

These match S22. The arithmetic is correct, and the problem lies in the assumption
behind it (§3 below).

## 2. Proxy check: is "fin area" the right quantity?

The claim treats fin area as *the* quantity the aerodynamics needs. That is itself
a proxy. The following is my inference from standard gliding aerodynamics and from
Fish 1990's definition of wing area (search-summary):

- **Wing loading uses total lifting area, not pectoral-fin area.** Fish 1990
  defines total wing area as pectoral area, plus pelvic area, plus the body
  rectangles between them. A pectoral-only area figure would therefore overstate
  the relative change in total wing area. A four-wing configuration also needs
  enlarged pelvic fins. Daane et al. report "elongated paired fins" in the Fig. 4A
  legend. The full-text main legend quantifies only pectoral and caudal fins
  (Fig. 4B–C). I could not check whether pelvic fins were quantified anywhere else.
- **Length is not aerodynamically irrelevant.** Pectoral fin length sets
  semi-span, and aspect ratio = span²/area. Glide ratio depends on aspect ratio
  through induced drag. Length is therefore one of the two inputs the aerodynamics
  needs, not a pure stand-in for area.
- **Area plus span is still not enough.** A glide also depends on body mass, how
  far the fin can be abducted, and whether the rays are stiff enough to hold a
  planform under load. The paper itself reports that `lat4a^nr21` has *smaller*
  lepidotrichial segments (full-text). That is a ray-architecture change whose
  effect on stiffness is unknown.

A better statement: aerodynamics needs **wing loading (mass ÷ total lifting area)
and aspect ratio (span² ÷ area)**. Daane et al. report a span-like quantity
(pectoral length/SL) and neither of the other two. So the gap is real, but it is
"no area, no mass, no planform", not "the wrong axis".

## 3. The hidden assumption, relaxed

S22's conversion from length to area assumes **constant fin shape**, so that area
scales as length². The claim's force, that a length-only result is far from what
is needed, partly rests on how big that conversion is.

I relaxed the assumption to **fixed chord**: rays lengthen while fin breadth stays
the same. My inference is that this is plausible, because ray-overgrowth mutants
lengthen rays distally. Daane et al. give no fin breadth or ray-count data for the
mutants (full-text: none in the main text). Under fixed chord, area scales as
(1+*f*). This is a calculation:

| *f* | area factor, constant shape | area factor, fixed chord | wing-loading factor, fixed chord |
|---|---|---|---|
| 0.25 | 1.56 | 1.25 | 0.80 |
| 0.50 | 2.25 | 1.50 | 0.67 |
| 1.00 | 4.00 | 2.00 | 0.50 |

These factors apply to pectoral area only. Wing loading against *total* lifting
area changes even less, because the body rectangles do not grow.

Relaxing the assumption **strengthens** the claim's conclusion: the same reported
length gain buys less area than S22's sensitivity table implies. The proportionality
model is unverified for these mutants either way. *f* itself is `unknown`, because
Table S1 and the Fig. 4B panel values were not accessible to S22 or to me.

## 4. Is the evidence level honest?

### "Fin AREA was never reported by the authors at all": overstated

S22's own scope is narrower than the claim. S22 says area was "not reported
anywhere in the text I could read". It lists figures, figure panels, supplementary
figure legends and Table S1 as **could-not-access**. The claim drops that scope and
asserts absence from the whole paper.

My own search (scope: the PMC9172250 main text, main figure legends and STAR
Methods, full-text) found **no occurrence of "area"** in a measurement sense. It
also found no image-analysis method that would produce area (no ImageJ/Fiji). That
makes "area was never reported" **likely**, but it remains unconfirmed for
Table S1 and the supplementary figure panels. Every route I tried to reach them
failed: Europe PMC (not open access), bioRxiv (HTTP 429), ZFIN (HTTP 503 /
blocked host). The correct statement is: *"Fin area does not appear in the
accessible main text, main legends or Methods. Table S1 and the supplementary
panels could not be accessed."* The claim's version is stronger than its evidence.

### "fin LENGTH normalised to standard length only": imprecise

Full-text read of the main manuscript:

- **Fig. 1B** plots *raw* paired-fin length against standard length, as an
  allometry across beloniform museum specimens ("we measured fin length as a
  function of body size (standard length)"; Methods: "Paired fin and standard fish
  lengths were measured from beloniform specimens in the Harvard Museum of
  Comparative Zoology"). These are comparative measurements of wild fishes, not of
  zebrafish.
- The **Fig. 3B** legend reads: "Comparison of fish standard length (SL) and
  caudal fin length in wild type, heterozygous …". That is a raw length-vs-SL
  comparison. Fig. 3D is the normalised version.
- **Lepidotrichial segment length** was compared between `nr21` and wild type
  (Fig. S2A–B per S22. The prose is full-text, the panel is could-not-access).
- Body size itself was tested ("does not have a statistically decreased body
  size").

Every measurement is still **linear**, so the substance of the claim (no area)
survives. "Normalised to SL only" is still wrong as a description. A more accurate
version: *linear lengths only (fin length raw and normalised to SL, segment
length, SL)*.

### "no lift, gliding or flight was measured": survives

Full-text: "lift", "swimming" and "aspect ratio" do not occur in the main text or
Methods. "Gliding" occurs only in describing wild flying fishes, halfbeaks and
reference titles, never as an experiment on zebrafish. Fig. 1A says the fins "act
as an airfoil to enable aerial gliding behavior", which is an authorial
description, not a measurement. No locomotor test was reported in the parts I
could read. The supplement remains unchecked, but nothing in the main-text
narrative refers to such a test.

## 5. Counter-example: is this "the one published genetic precedent"?

- A broad search returned no other genetic manipulation that phenocopies
  flying-fish fins in any fish (scope: one extended web search with the terms
  zebrafish, pectoral fin elongation, flying fish, gliding and genetic, for
  2022–2025, read at search-summary level).
- The Quanta Magazine piece (2022-01-05) appeared in the results summarised as a
  "2022 *Cell*" study by the Harris lab. My inference from its content (`lat4a`,
  potassium channel, long paired and short median fins) is that it describes the
  **same** Daane et al. 2021 *Current Biology* work. It is not a second precedent,
  and the "*Cell*" attribution is very likely a summarisation error.
- Other zebrafish long-fin genetics exists: `longfin`/`kcnh2a`,
  `another longfin`/`kcnk5b`, `schleier`/`kcnj13`. These are named in S22 and the
  paper. They elongate *all* fins and are not flying-fish phenocopies, so they do
  not undercut "the one precedent". If any of them reported fin *area*, that would
  be a partial source for an area/length scaling in ray-overgrowth mutants. I did
  not search for this. Status: `unknown`.

A search that is this narrow cannot prove that no other precedent exists. I found
none.

---

## What survives, and what changes

**Survives (full-text, main manuscript):**

- The zebrafish phenocopy (`kcnh2a^lof/+ ; lat4a^nr21/+`) is quantified as
  pectoral and caudal fin **length normalised by SL** (Fig. 4B–C).
- No lift, glide, flight, swimming or aspect-ratio measurement appears.
- Fin area appears nowhere in the accessible text.

**Corrected wording:**

> Daane et al. report only **linear** measurements: fin length raw and normalised
> to SL, lepidotrichial segment length, and SL. Fin area does not appear in the
> accessible main text, legends or Methods. Table S1 and the supplementary panels
> could not be accessed, so its total absence is likely but unconfirmed. No lift,
> gliding, flight or swimming performance was measured on zebrafish. The quantities
> aerodynamics needs are **wing loading (mass ÷ total lifting area, including pelvic
> fins and body) and aspect ratio**. Length/SL gives a span-like input, but not
> area, mass or planform.

**What would settle the remaining open point:** Table S1 and the Fig. 4B and S2
panels, obtained from the publisher with institutional access or from the lead
contact.

```swarm-challenge
{"claim_id": 40, "outcome": "weakened", "reason": "The substance holds (only linear lengths were measured and no lift, glide or flight was tested; full-text, main manuscript), but 'area never reported at all' outruns a negative search that could not reach Table S1 or the supplementary panels, 'normalised to SL only' ignores raw fin-length-vs-SL and segment-length data, and fin area is itself a proxy for wing loading (total lifting area incl. pelvic fins and body) plus aspect ratio, to which length/SL is a partial input.", "corrected_value": null}
```
