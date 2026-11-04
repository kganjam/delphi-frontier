# Challenge 40: does Daane et al. 2021 supply fin area?

Date: 2026-11-04. Reviewer: adversarial challenge. Target: claim 40, source
`docs/research/fish/S22-dna.md` (branch `claude/s22-daane-fin-phenocopy-9l9y75`).

## The claim under review

> "CRITICAL GAP: Daane et al. measured fin LENGTH normalised to standard length only. Fin AREA was
> never reported by the authors at all, and no lift, gliding or flight was measured. The one
> published genetic precedent does not supply the quantity the aerodynamics needs"

Recorded evidence level: `literature`. Value: n/a.

The claim makes four assertions. I tested each one separately:

- (A) length/SL was the **only** measurement;
- (B) area was **never reported at all**;
- (C) no lift, gliding or flight was measured;
- (D) the precedent "does not supply the quantity the aerodynamics needs", where that quantity is
  implicitly area.

## Source read for this challenge

| Source | What I obtained | Read-level |
|---|---|---|
| Daane et al. 2021, *Curr Biol* 31:5052–5061.e8, doi:10.1016/j.cub.2021.08.054, PMC9172250 | NCBI efetch PMC XML (202 kB): abstract, main text, STAR Methods, Quantification section, main figure legends 1–4, key resources table | **full-text** (main text, Methods, main-figure legends) |
| Same paper, supplement `NIHMS1735542-supplement-1.pdf` (Figs S1–S4 and legends) | Tried three mirrors: pmc.ncbi.nlm.nih.gov returned a reCAPTCHA page, ncbi.nlm.nih.gov/pmc returned an HTML page, europepmc.org returned a Cloudflare challenge | **could-not-access** |
| Same paper, `NIHMS1735542-supplement-2.xlsx` (Data S1) | Not retrieved by the same routes | **could-not-access** |
| Zenodo deposit 10.5281/zenodo.5082978 (cited in the paper) | The egress proxy refused the connection (403) | **could-not-access** |
| Europe PMC REST full-text XML | HTTP 500 | **could-not-access** |

I did not use the S22 author's reading. All quotes below are from my own pass over the XML text.

## 1. Arithmetic, redone independently

S22 §3 assumes geometric similarity, so area scales as (1+f)² and wing loading as 1/(1+f)² for a
fractional length gain f. I recomputed both:

| f | (1+f)² | 1/(1+f)² |
|---|---|---|
| 0.25 | 1.5625 | 0.640 |
| 0.50 | 2.25 | 0.444 |
| 1.00 | 4.00 | 0.250 |

These match S22. **The arithmetic is correct.** It is a computation, not data, and S22 labels it
that way. The claim itself contains no arithmetic.

## 2. Testing each assertion against the full text

**(C) No lift, gliding or flight was measured. SURVIVES (full-text).**

- Every occurrence of "glid*" and "flight" in the text concerns the comparative and phylogenomic
  analysis or cited literature. None of them is a zebrafish measurement.
- The only "lift" hit is "lift the read alignment", which is bioinformatics.
- There is no word on body mass, swimming, kinematics or flow.
- Scope of this negative search: main text, STAR Methods and main-figure legends. The supplement
  was not read. However, the Quantification section lists every statistically analysed panel:
  Figs 2A, 2C, 3B, 3D, 4B–4E, S2B and S2I. None of these is a locomotor assay.

**(B) Area was never reported. SURVIVES in the main text. "At all" is over-scoped.**

- The text contains no instance of "area", "width", "aspect", "span" or "surface" applied to fins.
  ("Surface" occurs once, and it refers to the water surface for corneas.)
- The museum morphometrics on beloniforms are also length-only. Methods: "Paired fin and standard
  fish lengths were measured from beloniform specimens". So the authors did not report flying-fish
  fin area either.
- Two quantified supplementary panels are unread: **S2B and S2I**. The main text ties S2A–B to
  lepidotrichial segment length. The content of S2I is `unknown`. Data S1 is also unread.
- "Never reported … at all" is therefore a universal negative that rests on main text plus
  legends. The S22 body states this scope correctly (§2.4 says "figures and supplements not
  accessible"). Claim 40 dropped the qualifier.
- I think it is very unlikely that S2I is an area measurement (my inference). Still, the sentence
  should carry its scope.

**(A) "Length normalised to SL only". WEAKENED (full-text). The word "only" is literally wrong.**

The zebrafish morphometric endpoints in the text are:

- Fig 3B: **raw** standard length and **raw** caudal fin length, by genotype. Not normalised. The
  text uses it to say `nr21` "does not have a statistically decreased body size".
- Fig 3D: caudal fin length / SL.
- Fig 4B and 4C: pectoral fin length and caudal fin length, "length normalized by SL".
- Figs S2A–B: **lepidotrichial segment length** (`nr21` segments "smaller"; `lof` "elongate but
  regular").
- Fig 4A: a **qualitative** shape call, "hypocercal caudal fin", with no index reported.

So the authors measured lengths in several forms: normalised, raw, and segment-level. **The
substance survives:** every quantity is a length, and none is an area. "Only length normalised to
SL" is an imprecise description of a length-only dataset.

**(D) "Does not supply the quantity the aerodynamics needs". WEAKENED. This is a proxy error in the
claim itself.**

The claim treats area as *the* quantity and length as a mere proxy for it. That is incomplete:

- A glider's steady performance needs **span (b), planform area (S), mass (m)**, and the derived
  wing loading mg/S, span loading mg/b and aspect ratio AR = b²/S.
- Induced drag, D_i = (mg)² / (q·π·e·b²), depends on **span**, not on area.
- For a pectoral fin held out laterally, fin length sets the semispan. Fin length is therefore an
  aerodynamic input in its own right, not just a stand-in for area.

What Daane et al. fail to supply is three things, not one:

1. **Area** (or chord), so neither wing loading nor AR can be formed.
2. **Body mass**, which is reported nowhere in the text. Without it, even span loading cannot be
   formed from their data.
3. **The magnitude of the length change.** Fig 4B values are in a figure panel. The text gives no
   number.

The correct statement is that the precedent supplies, in principle, a **span-type quantity**
(pectoral length/SL) whose magnitude is not available in text. It supplies no area, no mass and no
AR. "Does not supply the quantity" undersells what length gives and also undersells what is
missing: mass is as absent as area.

## 3. The hidden assumption, relaxed

Both S22 and claim 40 frame area as "~ length²". That framing carries the "potentially the whole
gap" rhetoric in S22 §1, and it rests on **geometric similarity of the fin**.

- `lof` overgrowth is described in the text as ray elongation with "elongate but regular segmented
  lepidotrichia".
- The text reports no change in ray number. Whether ray number changes is `unknown`.
- If the base width and the ray fan angle are both unchanged, then fin area grows somewhere
  between:
  - ∝ L, if the rays are near-parallel and chord is fixed by ray count; and
  - ∝ L², if the rays radiate at a fixed angle, so the fin is a sector with area θL²/2.

Computation, using the same f values:

| f | Area factor if ∝ L | Area factor if ∝ L² |
|---|---|---|
| 0.25 | 1.25 | 1.56 |
| 0.50 | 1.50 | 2.25 |
| 1.00 | 2.00 | 4.00 |

**What this means (my inference):** a length result does not bound area to within a factor of 2 at
f = 1. Converting length to area is not just "unmeasured". It is *undetermined by shape*. This
supports the claim's conclusion that area is needed and strengthens the case for measuring it. It
also shows that AR, which falls when area grows faster than span², moves in a direction nobody has
measured.

## 4. Is the evidence level honest?

`literature` is appropriate. The claim reports what a paper did and did not contain, and it
presents no derived number as measured.

One defect is about read-level, not evidence level. The universal negative "never … at all" is
stated without the scope that S22 itself records (main text plus legends; supplement not
accessed).

**Separate defect found in the source, outside claim 40:** S22 §2.4 says "The Results direct the
reader to Table S1 for fin-length data". In the text I read, **Table S1 is the sequencing-sample
table** ("pooled DNA … from each of 35 different beloniform species (Table S1; Data S1B)"). The
beloniform fin-length data are in **Data S1A**. The text does not say which file holds the
zebrafish fin values. S22's access-attempt plan (§6 item 1, "Obtain Table S1") points at the
wrong file.

## 5. Counter-examples and missed regimes

- **"The one published genetic precedent".** I searched for another genetic manipulation reported
  to produce flying-fish-like fins, or any aerodynamic test of a fin-overgrowth fish. I found none.
  Scope: the reference list of Daane et al. and my own knowledge of the fin-size mutant literature
  (`alf`/`kcnk5b`, `lof`/`kcnh2a`, `sof`/`cx43`). I did no database search, so "one" is
  unrefuted, not verified.
- **Other fin-overgrowth papers measure length or segments, not area,** as far as I know. I give
  no specific citation or number for this, because I did not read those papers in this pass.
- **Four-wing regime.** Flying-fish "wing area" includes the **pelvic** fins (S22 §2.6, citing Fish
  1990 at search-summary). Daane et al. say "paired fins are overgrown" but quantify only pectoral
  and caudal fins. This is a second missing quantity that the claim does not name.
- **Data deposit.** The paper cites Zenodo 10.5281/zenodo.5082978. If raw images are deposited
  there, fin area could be *derived* from the authors' images without new fish. That would make
  area a derived quantity, not a reported one, but it is a cheaper route than S22 §6 lists. I
  could not reach Zenodo (proxy 403), so whether images are deposited is `unknown`.

## Verdict

**WEAKENED.**

The core of the claim survives at full-text for the main text and legends:

- Daane et al. report no fin area, for zebrafish or for flying fishes.
- They report no lift, glide, flight, swimming or body-mass measurement.

Two parts of the wording are defective:

1. **"Only length normalised to SL"** is wrong in detail. They also report raw SL and raw caudal
   length (Fig 3B), segment lengths (Fig S2B) and a qualitative hypocercal shape. "Never … at all"
   omits that S2I, Data S1 and the supplement were unread.
2. **The proxy framing is incomplete.** Fin length is not a mere proxy for area. It is the
   span-type input that induced drag depends on directly. The missing aerodynamic inputs are
   **area (or chord), body mass and the magnitude of the length change**, plus pelvic fins for a
   four-wing target. Area is not the only one.

### Corrected wording

> Daane et al. 2021 quantified zebrafish fins only as **lengths**: caudal and pectoral length/SL
> (Figs 3D, 4B–C), raw SL and caudal length (Fig 3B), and lepidotrichial segment length (Fig S2B).
> They gave a qualitative hypocercal call and no numeric effect size in text. No fin **area**,
> chord, aspect ratio or **body mass** appears in the main text, Methods or main-figure legends.
> Supplementary panel S2I and Data S1 were not accessible. No lift, glide, flight or swimming test
> was made. Pectoral length/SL is a span-type input, but without area and mass neither wing loading
> nor span loading can be formed. Read-level: full-text (main text, Methods, main legends);
> could-not-access (supplement, Data S1, Zenodo deposit).

```swarm-challenge
{"claim_id": 40, "outcome": "weakened", "reason": "The core negative (no fin area, no lift/glide/flight, also no body mass) survives at full-text for main text, Methods and legends, but 'length normalised to SL only' is wrong in detail (raw SL and caudal length in Fig 3B, segment length in Fig S2B), 'never at all' omits the unread supplement (S2I, Data S1), and treating length as a mere proxy for area misses that length is the span input the aerodynamics needs directly, while area, mass and effect magnitude are all missing.", "corrected_value": null}
```
