# S2-D-D: deepening S2-D by attacking its weakest input (the effective aspect ratio of a fin wing)

**Parent (S2-D, organism).** Branch `claude/deepen-s2-lift-drag-6xxrv3`, files
`docs/research/fish/S2-deepen.md` and `S2D_calcs.py`. I read both in full. The task prompt quoted the
S2-D answer as blank, so I took the answer from that file.

**What S2-D concluded** (its §5 and its swarm-result):
- With profile drag matched to Re, a fin-wing fish has a computed **whole-animal L/D of about 3–5**
  (4.1–5.5 at AR 4; 3.2–4.8 for AR 1.5–4).
- S2's "6–7 ceiling" is an insect-planform number. A fin would reach it only if its effective
  aspect ratio is about ≥ 4.
- Its most sensitive input, the effective aspect ratio **e·AR**, "remains an unmeasured assumption"
  (AR = 4, e = 0.7, so e·AR = 2.8).

**Kinds of number.** I ran no experiment. Every number below is one of three kinds, and the sentence
says which:
- quoted from a source, with its read-level;
- **computed** by `S2-D-deepen_calc.py` in this directory (run with
  `python3 -I docs/research/fish/S2-D-deepen_calc.py`);
- my **inference**, labelled as such.

The script copies S2-D's aerodynamic model unchanged. Control C1 asserts that it reproduces S2-D's
published 5.49 (baseline) and 4.80 (AR 4, λ = 1.4, capped CL). Both pass.

---

## 1. Which input is S2-D's answer most sensitive to? (computed)

I re-ran S2-D's ×0.5 / ×2 test rather than accept it:

| input | ×0.5 → whole-animal L/D | ×2 → whole-animal L/D | swing |
|---|---|---|---|
| **e·AR** | **3.88** | **7.76** | **2.00** |
| CD0_wing | 6.77 | 4.23 | 1.60 |
| body drag area | 5.98 | 4.78 | 1.25 |

Analytic control: with body drag set to zero, wing-alone L/D ∝ √(e·AR). Quadrupling e·AR (from ×0.5
to ×2) must therefore double L/D exactly, and it does, to 1e-12.

S2-D identified the right input. e·AR is the only one whose factor-of-2 error pushes the answer out
of the 3–5 band on both sides. It reaches 3.9 on one side and 7.8 on the other, which is above the
6–7 "ceiling".

e·AR has two factors:
- **AR** (planform), which can be looked up in the fish literature;
- **e** (span efficiency), which cannot.

I attacked AR, because it is the factor that can be measured from a photograph. I bracket e
separately in §4.

## 2. How well is the input established?

| factor | S2-D's value | evidence level | read-level | honest status |
|---|---|---|---|---|
| AR | 4 (two 3 × 1.5 cm fins) | **assumption** | n/a | S2 labelled it as assumed ("per-wing span/chord ≈ 2"). It has not been passed off as measured. |
| e | 0.7 | **assumption** | n/a | Never retrieved anywhere in the S2 chain. |
| zebrafish pectoral planform (span, area, AR) | none | **unmeasured in anything reached** | n/a | See the negative search in §3c. |

**Grade:** an assumption, labelled as one. It had **no anchor at all in any fish measurement.** S2-D
scanned AR from 1.5 to 8 but could not say where in that range a real fin sits.

## 3. Improving it: measured pectoral-fin aspect ratios

### 3a. Convention trap (my inference, from full text)

The fish ecomorphology literature reports pectoral-fin AR for **one fin**, as AR_fin = L²/A, where L
is the leading-edge length and A is that fin's area. The aerodynamic model needs AR of **both fins as
one wing**, b²/S. The two conventions differ by a factor of 2:
- with b = 2L and S = 2A, AR_wing = 4L²/2A = **2·AR_fin** (computed algebra).

The evidence for this is in Walker, Alfaro, Noble & Fulton 2013 (*PLoS ONE* 8:e75422, PMC3799785,
**full-text**). Verbatim: AR was "calculated … as 2*length²/area for pectoral fins … (the pectoral fin
AR is doubled to conform to the definition of AR for wings in the aerodynamics literature)". The
paper cites Fulton et al. 2005 for the method.
- **My inference:** the undoubled Fulton/Wainwright values are therefore AR_fin = L²/A.
- I could not read Fulton et al. 2005's own methods (abstract only), so this rests on Walker et al.'s
  description of it.
- **Why it matters:** this is exactly the factor of 2 that §1 shows can move the answer across the
  band. Reading the labrid maximum of 2.08 as a wing AR would understate L/D by about 1 unit: the §4
  table gives 3.70 at AR 1.82 against 4.88 at AR 4.16 (computed).

### 3b. What has been measured

| source | taxon | measured value | convention | read-level |
|---|---|---|---|---|
| Fulton, Wainwright, Hoey & Bellwood 2016, *Ecol Evol* 7, doi 10.1002/ece3.2624, PMC5214093 (Europe PMC XML, sha256 `45321787…`) | wrasses (Labridae): the top three species at each of 11 reef locations, 33 entries in Table 1 | Table 1 pectoral AR **0.91** (*Pseudocheilinus hexataenia*) to **2.08** (*Stethojulis bandanensis*). *Halichoeres* 1.29–1.54; *Thalassoma* 1.81–1.97. Text: 2.08 is "the upper extreme … for this family". | single fin, by "the exact method of Fulton et al. (2005)" (the convention is my inference, §3a) | **full-text** |
| Fulton et al. 2005, *Proc R Soc B* 272:827, doi 10.1098/rspb.2004.3029 | three reef-fish families | No numbers in the abstract | — | **abstract** |
| Park & Choi 2010, *J Exp Biol* 213:3269, doi 10.1242/jeb.046052 | flying fish *Cypselurus hiraii*, stuffed real specimens in a wind tunnel | "The pectoral fins … have an aspect ratio of 9.0∼10.7", "comparable to those of birds". Re = 1.9–2.2×10⁴ on mean pectoral chord. Authors' claim: "the induced drag by strong wing-tip vortices is one of the dominant drag components". **No numerical L/D appears in the text I could read**; the L/D values are in figures. | Span is defined as "the full span of the pectoral fins (see Fig. 2)". Fig. 2 was not readable, so tip-to-tip versus per-fin is **unconfirmed**. | **partial full-text**: publisher page, about 100k of 157k characters, with no figures or Table 1 |
| Jones et al. 2020, *Conserv Physiol* 8:coaa126, PMC7772615 | European minnow and topmouth gudgeon (cypriniform relatives of *Danio*) | Pectoral fin length/BL 0.174 and 0.137. Their "AR" (2.34, 2.65) is **caudal**, not pectoral: "a metric derived from the height and surface area of the caudal fin". | — | **full-text** |

Disagreement I preserve rather than average: the flying-fish 9.0–10.7 and the labrid 0.91–2.08
cannot be on the same convention unless flying-fish fins are about 5–10× more elongate than wrasse
fins.
- **My inference:** Park & Choi's figure is the wing convention, which makes the ratio about 2.2–2.6×
  (labrid max 4.16 against 9–10.7), because they compare it with birds.
- If it were per-fin instead, the wing AR would be 18–21. I judge that implausible but have not
  excluded it.
- I run 9.0–10.7 as a wing AR and flag this as an unconfirmed reading.

### 3c. Zebrafish itself: still unknown

Negative search, with its scope:
- Europe PMC REST, three queries (listing read-level, titles read):
  - `"pectoral fin" AND ("aspect ratio") AND (Cyprinidae OR cyprinid OR Danio OR minnow)`: 11 hits;
  - `"pectoral fin" AND (area OR "aspect ratio") AND zebrafish AND (planform OR morphometric OR "fin shape")`: 86 hits;
  - `TITLE:"pectoral fin" AND (shape OR morphology) AND zebrafish`: 32 hits.
- I opened full text for PMC7772615, PMC8840878 and PMC10918187.
- No source gives an adult *Danio rerio* pectoral fin area or AR.
- One web search (search-summary) found none either.
- Search controls:
  - positive: `TITLE:"Non-lethal measurement of pectoral fin aspect ratio"` returned the known 2011
    paper (1 hit);
  - must-fail: the gibberish query returned 0.
- This is a negative result about what I could reach. It is not a claim that the measurement does not
  exist.

Hosts not reachable from this session:
- `authors.library.caltech.edu`: Taira & Colonius 2009, the computed low-Re, low-AR flat-plate forces
  that would constrain **e**;
- `pmc-oa-opendata` has no copy of Fulton 2005.

The measurement that would settle the zebrafish value is the one S2-D already priced:
- photograph the spread pectoral fins of about 10 adults on a mm grid;
- compute L²/A per fin and double it;
- **hours, and under $100** (S2-D's estimate, not re-priced here).

**What the input is now:** a **measured proxy** (other teleosts, full-text). Before, it was an
**unanchored assumption**. It is still not the zebrafish quantity.

## 4. Recompute (computed)

There is one modelling change from S2-D. S2-D held the chord at 15 mm for every AR. Here the chord
follows the planform, c = √(S/AR), so a high-AR wing runs at a lower Re and pays for it in profile
drag. Everything else is S2-D's: S = 9 cm², λ = Blasius multiplier, CL capped at 0.9, e = 0.7.

| AR source | AR_wing | e·AR | whole L/D, λ 1.4 | whole L/D, λ 2.0 | wing-alone L/D, λ 1.4 |
|---|---|---|---|---|---|
| labrid minimum (0.91 ×2) | 1.82 | 1.27 | **3.70** | 3.19 | 4.38 |
| *Halichoeres* typical (≈1.38 ×2) | 2.76 | 1.93 | **4.25** | 3.65 | 4.96 |
| *Thalassoma* (≈1.9 ×2) | 3.80 | 2.66 | **4.71** | 4.07 | 5.45 |
| labrid maximum (2.08 ×2) | 4.16 | 2.91 | **4.88** | 4.19 | 5.66 |
| S2/S2-D assumption | 4.00 | 2.80 | 4.80 | 4.14 | 5.56 |
| flying fish (9.0–10.7, wing convention assumed) | 9.0–10.7 | 6.3–7.5 | **5.92–6.03** | 4.77–4.80 | 7.12–7.28 |

Bracketing e (still assumed) at λ = 1.4:
- labrid minimum AR: e = 0.5 / 0.7 / 0.9 gives **3.21 / 3.70 / 4.13**;
- labrid maximum AR: e = 0.5 / 0.7 / 0.9 gives **4.20 / 4.88 / 5.46**.

**A constraint S2-D did not apply: span (computed).** At S = 9 cm², the span each AR needs on a
3.2 cm SL fish is:
- AR 1.82: 0.57 SL per fin;
- AR 4: 0.87 SL per fin (S2's own planform);
- AR 9: 1.34 SL per fin;
- AR 10.7: 1.47 SL per fin.

The flying-fish pectoral is 0.65–0.77 SL (*E. volitans*, search-summary, carried over from S22-D).
For comparison, the wild-type zebrafish pectoral is about 0.21 SL (inferred in S22-D-D from a
figure-read).

So S2's assumed AR-4 wing already has fins longer than a flying fish's, relative to the body. The
flying-fish AR is only available on a fish this size if the wing area is reduced.

With span fixed at the flying-fish proportion (0.70 SL per fin, b = 4.9 cm) and S set by AR, the
computed whole-animal L/D is:

| AR | 2 | 3 | 4 | 6 | 9 |
|---|---|---|---|---|---|
| L/D | 3.95 | 4.30 | 4.58 | **4.84** | 4.73 |

L/D **saturates below 5**. Once span is the binding limit, raising AR only shrinks the wing. That
raises the flight speed and the share of body drag (inference from the computed trend; V rises from
3.1 to 5.2 m/s).

## 5. Verdict on S2-D: **STRENGTHENS**

- **S2-D's band of 3–5 for the whole animal strengthens.** Before, it was an AR scan with no
  anchor. Now it rests on measured pectoral-fin planforms.
  - Across the full measured labrid range, converted to wing convention, AR is 1.8–4.2. That gives a
    computed **whole-animal L/D of 3.2–4.9**, or 3.2–5.5 including e = 0.5–0.9.
  - S2's assumed AR of 4 turns out to sit at the **top of the measured wrasse range**, not in the
    middle. So S2/S2-D's central 4.8 is an optimistic point, not a typical one.
- **S2-D's conditional "rising toward 6 only if e·AR ≳ 4" stands.** At e·AR 6.3–7.5, flying-fish
  fins give 5.9–6.0.
  - Flying fish show, at partial-full-text level, that ray-and-membrane fins *can* reach that AR.
  - But on a 3.2 cm fish, that AR at 9 cm² needs fins about 1.3–1.5 SL long, roughly twice the
    flying-fish proportion. At flying-fish proportions, the computed L/D tops out at **≈ 4.8** for
    any AR.
  - **My inference:** for this animal, the binding variable is **span relative to body length**,
    not AR. This is the new sensitive input.
- **Not improved:**
  - e (span efficiency) is still assumed. It alone moves L/D by ±0.6 across 0.5–0.9.
  - The zebrafish's own pectoral AR is still `unknown`.
  - The Park & Choi convention is unconfirmed, and their L/D values are in figures I could not read.
  - The locust 6–7 is still relayed (S2-D: Jensen 1956 could-not-access).

**Next weakest input:** the achievable fin span per side as a fraction of SL. S2 assumed 0.87 SL.
The flying-fish value is 0.65–0.77 SL (search-summary). Wild-type zebrafish is about 0.21 SL
(inferred). The only measured long-fin allele gives 1.7–2× overgrowth (S22-D-D, proxy). Together these
imply a reachable per-fin span of about 0.36–0.43 SL, which is well under the flying-fish proportion
(inference from S22-D-D's numbers).

## Sources

| source | read-level |
|---|---|
| S2-deepen.md and S2D_calcs.py (branch `claude/deepen-s2-lift-drag-6xxrv3`) | full-text |
| S2-low-reynolds-aero.md (branch `claude/s2-low-reynolds-aero-acdwr7`): mass, SL range, planform assumption | full-text (the relevant sections) |
| S22-D-deepen.md (branch `claude/s22-d-sensitive-input-pwechp`): wild-type pectoral ≈ 0.21 SL; flying fish 0.65–0.77 SL | full-text. Those numbers are that document's inference and search-summary, which I relay. |
| Walker, Alfaro, Noble & Fulton 2013, PLoS ONE 8:e75422, doi 10.1371/journal.pone.0075422, PMC3799785 (sha256 `83ab57b3…`) | full-text |
| Fulton, Wainwright, Hoey & Bellwood 2016, Ecol Evol 7, doi 10.1002/ece3.2624, PMC5214093 (sha256 `45321787…`) | full-text |
| Fulton, Bellwood & Wainwright 2005, Proc R Soc B 272:827, doi 10.1098/rspb.2004.3029 | abstract |
| Park & Choi 2010, J Exp Biol 213:3269, doi 10.1242/jeb.046052 | partial full-text (publisher HTML, about 64% of the text; no figures or tables) |
| Jones et al. 2020, Conserv Physiol 8:coaa126, doi 10.1093/conphys/coaa126, PMC7772615 (sha256 `20b843de…`) | full-text |
| Non-lethal measurement of pectoral fin AR, J Fish Biol 2011, doi 10.1111/j.1095-8649.2011.03070.x | abstract (used only as a search control) |
| Taira & Colonius 2009, J Fluid Mech 623:187 | could-not-access (host not allowed) |
| Europe PMC listings in §3c | listing |

```swarm-result
{"subproblem": "S2-D-D", "evidence": "computed from measured proxy planforms: labrid pectoral-fin AR 0.91-2.08 per fin (full-text, Fulton et al. 2016 Table 1; convention L^2/A per fin inferred from Walker et al. 2013), flying-fish pectoral AR 9.0-10.7 (partial full-text, Park & Choi 2010, convention unconfirmed); zebrafish pectoral AR itself unknown; span efficiency e still assumed", "answer": "Measured teleost pectoral planforms give a wing aspect ratio of 1.8-4.2, so with S2-D's own Re-matched model the computed whole-animal L/D is 3.2-4.9, which places S2's assumed AR 4 at the top of the measured range. Flying-fish fins show AR 9-10.7 is anatomically possible, but on a 3.2 cm fish at flying-fish fin proportions the computed L/D saturates near 4.8 for any AR, so span per side relative to SL, not AR, is the binding input.", "key_number": "pectoral wing aspect ratio AR_wing = 2 x (L^2/A per fin) = 1.82-4.16 (labrids, measured, full-text); 9.0-10.7 (flying fish, measured, convention unconfirmed); e*AR = 1.3-2.9 at assumed e = 0.7", "verdict": "strengthens", "depends_on": ["S2-D whole-animal L/D 3-5 and its parabolic-polar model (S2D_calcs.py, branch claude/deepen-s2-lift-drag-6xxrv3)", "S2-D profile drag CD0 = lambda x Blasius, lambda 1.4-2.0, inferred from Wakeling & Ellington 1997 CD(alpha=0) 0.07-0.14 at Re 700-2400 (abstract)", "CL usable cap 0.9, about 85% of W&E 1997 steady CL,max 1.07 (abstract; margin assumed)", "Fulton et al. 2016 Ecol Evol Table 1 labrid pectoral AR 0.91-2.08 (full-text)", "inference: Fulton-method AR is L^2/A per single fin, so AR_wing = 2 x AR_fin (from Walker et al. 2013 PLoS ONE methods, full-text)", "Park & Choi 2010 JEB flying-fish pectoral AR 9.0-10.7, read as wing convention (partial full-text; convention unconfirmed)", "span efficiency e = 0.7 (assumed, bracketed 0.5-0.9)", "wing area S = 9 cm^2 (assumed, S2)", "mass 0.4 g (assumed, S2; inside relayed adult range 0.25-0.55 g)", "SL 3.2 cm (assumed, inside relayed 2.8-3.4 cm, S2)", "body drag area from assumed 32x7x4 mm ellipsoid, form factor 1.5, 2 cm^2 median fins (assumed, S2-D)", "flying-fish pectoral length 0.65-0.77 SL, E. volitans (search-summary, via S22-D)", "wild-type zebrafish pectoral about 0.21 SL (inferred from figure-read, S22-D-D)", "kcnk5b alf/+ pectoral overgrowth 1.7-2x (proxy, S22-D-D)", "zebrafish adult pectoral AR = unknown (negative search, scope in section 3c)"]}
```
