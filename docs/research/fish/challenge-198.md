# Challenge 198 — adversarial review of [S23] actinotrichia stiffness

**Claim under review (verbatim):**

> [S23] No published gain-of-function raises actinotrichia at all, and the computed
> material-only ceiling for stiffening an unmineralised collagenous fibril (~20-25x) is
> one to two orders of magnitude short of the ~10^2-10^3x fin flexural-stiffness increase
> a 0.4 g glider needs, while actinotrichia-null adults still form rays with thicker
> hemirays - so actinotrichial stiffness is probably not what limits S6.
> KEY: shortfall factor 245x-2616x between required EI 9.8e-7 to 3.9e-6 N*m^2 (computed)
> and measured adult zebrafish caudal fin EI 1.5e-9 to 4e-9 N*m^2 (Puri et al. 2018)

Recorded evidence level: `derived`. Source: `harvest:s23-actinotrichia-stiffness-protein-wwp5m2`.

**Verdict: WEAKENED.** The headline conclusion survives — and is better supported by
evidence the author did not cite than by the author's own argument — but the KEY number
is not reproducible at its upper bound, the measured baseline is a proxy for the wrong
fin, and the central inference step does not follow as written.

---

## 1. Arithmetic, redone independently from the stated inputs

I recomputed the ratio from the four numbers printed in the KEY, without reference to
the author's working. These are *my* calculations, not observations:

| quantity | value |
|---|---|
| required EI (claim, computed) | 9.8e-7 to 3.9e-6 N·m² |
| measured EI (claim, Puri et al. 2018) | 1.5e-9 to 4e-9 N·m² |
| minimum ratio = 9.8e-7 / 4e-9 | **245.0** |
| maximum ratio = 3.9e-6 / 1.5e-9 | **2600.0** |
| like-for-like low/low = 9.8e-7 / 1.5e-9 | 653.3 |
| like-for-like high/high = 3.9e-6 / 4e-9 | 975.0 |

**Defect (minor, real):** the claim states the upper bound as **2616x**. From the stated
inputs it is **2600x**. 2616 requires a numerator of 3.924e-6 or a denominator of
1.491e-9 — neither of which appears in the KEY. The discrepancy is 0.6% and does not
move the "~10²–10³x" characterisation, but a KEY number that cannot be reproduced from
its own printed inputs is a reproducibility defect, and the published figure should be
corrected to **245x–2600x**.

The qualitative framing "~10^2-10^3x" is consistent with 245–2600 and survives.

## 2. Is a proxy standing in for the quantity that matters?

**Yes, two of them.**

**(a) Caudal fin standing in for the gliding surface.** Puri et al. 2018 measured the
**caudal** fin, clamped at the peduncle and loaded as a cantilever (full text read, see
§6). A 0.4 g glider's flexural-stiffness requirement is a requirement on the surface
that carries the aerodynamic load — in every extant gliding teleost that is the enlarged
**pectoral** fin (and in biplane gliders the pelvics), not the caudal. No zebrafish
pectoral-fin EI appears in the claim, and I could not find one published: **unknown**.
Searches run: Google-indexed web search for "Puri 2018 zebrafish caudal fin mechanical
properties flexural stiffness in vivo" and "bluegill sunfish pectoral fin ray flexural
stiffness N m^2 measured Lauder"; no zebrafish pectoral value returned. Direction of the
error: a zebrafish pectoral fin is much smaller than its caudal, so its EI is very
probably *lower*, which would make the shortfall *larger*. The proxy therefore does not
rescue the claim's opponent — but the KEY presents a caudal number as if it were the
baseline for the structure that must be stiffened, and that substitution is unlabelled.

**(b) "Material-only ceiling" standing in for a structural ratio.** The 245–2600x figure
is a ratio of **EI** (a structural quantity, N·m²). The ~20-25x ceiling is a ratio of
**E** (a material quantity, Pa). Comparing them directly silently fixes the second moment
of area *I*. That is the hidden assumption, tested in §3.

I could not locate the derivation or source of the ~20-25x material ceiling. It is
presented inside the claim as "computed" with no inputs shown, and the harvest record
`harvest:s23-actinotrichia-stiffness-protein-wwp5m2` is not present in this repository
(checked `kganjam/delphi-frontier` at the review commit by path listing and code search;
read-level: could-not-access). **Its provenance is unverified**, and it is the input my
§3 objection is most sensitive to.

## 3. The hidden assumption, relaxed

The claim's argument only refutes the stiffness route if geometry is held constant.
Relaxing that (my calculation, not an observation; EI = E·I, and for a beam of depth *t*,
I ∝ t³ for depth-only growth of a rectangular section and I ∝ t⁴ for isometric growth):

| material gain | total EI gain needed | residual geometric factor | thickness ×, I∝t³ | thickness ×, I∝t⁴ |
|---|---|---|---|---|
| 20x | 245x | 12.2 | 2.31 | 1.87 |
| 20x | 2600x | 130 | 5.07 | 3.38 |
| 25x | 245x | 9.8 | 2.14 | 1.77 |
| 25x | 2600x | 104 | 4.70 | 3.19 |

With geometry free, the whole 245–2600x gap closes with a **4.0x–7.2x** linear thickness
increase alone (I∝t⁴) or **6.3x–13.8x** (I∝t³), no material change at all. With the
author's own 20–25x material ceiling applied as well, the residual demand falls to a
**1.8x–5.1x** thickness increase.

So the premise "material alone is 1–2 OOM short" is true but does **not** license the
conclusion drawn from it. "A 20-25x material gain cannot close a 245-2600x structural
gap by itself" is logically compatible with "fin flexural stiffness is exactly what
limits S6, and material improvement is a useful but insufficient part of closing it."
As written, the claim's middle clause is a non sequitur in the direction it is used.

**What actually carries the conclusion** is the third clause plus two facts the author
did not cite (§4, §5): actinotrichia are not the dominant stiffness element of an adult
teleost fin, so *actinotrichial* stiffness specifically is not the binding constraint.
That conclusion survives; the stated route to it does not.

## 4. Evidence level — is it honest?

Mostly yes, with one unlabelled substitution and one unsourced input.

- "required EI 9.8e-7 to 3.9e-6 N*m^2 (computed)" — correctly labelled computed. I could
  not inspect the derivation (harvest record not in repo); I therefore take it as given
  and my verdict depends on it.
- "measured adult zebrafish caudal fin EI 1.5e-9 to 4e-9 N*m^2 (Puri et al. 2018)" —
  **confirmed measured, and correctly characterised as whole-fin EI.** Read-level:
  full-text (PMC5868929). The paper reports whole-fin bending stiffness of 1.5e-9 to
  4e-9 N·m² along the proximal–distal axis, measured in vivo on five caudal fins of
  6–12-month wild-type AB zebrafish, cantilevered at the peduncle, line-loaded at six
  positions with forces near 100 µN and deflections under 2 mm. No ray-level or
  per-unit-width stiffness is given, so the claim has not mistaken a per-ray number for a
  whole-fin one. Note the paper's own abstract calls these "bending moments"; the units
  (N·m²) are flexural rigidity, and the claim reads them correctly.
- The ~20-25x material ceiling — labelled "computed" but **unsourced and unreproducible
  from the claim text**. This is the honesty gap.
- The caudal→gliding-surface substitution is not flagged anywhere in the claim.
- Overall label `derived` is appropriate for the composite.

## 5. Regime, taxon and counter-examples the author missed

**(a) The strongest missing support — a real teleost already exceeds the requirement.**
Flammang, Alben, Madden & Lauder (2013, *J. Morphol.*; read-level: search-summary of the
abstract plus the hosted PDF listing) report flexural stiffness of **565 × 10⁻⁶ N·m²**
(5.65e-4 N·m²) for a **single** bluegill sunfish pectoral fin ray (third left ray, n = 6
fish). My calculation: that one ray is **145x to 577x stiffer than the claim's entire
required whole-fin EI** of 9.8e-7–3.9e-6 N·m². An ordinary, non-gliding teleost's
mineralised pectoral ray already clears the bar by two orders of magnitude. The required
stiffness is therefore a lepidotrichial geometry-and-mineralisation question, not an
actinotrichial material question — which supports the claim's conclusion far better than
the argument the claim actually makes.

**(b) Preserved disagreement in the literature.** Puri et al. cite a published bluegill
fin value of **3.8e-6 N·m²** and use it to scale an *estimated* zebrafish fin stiffness of
2e-9–5e-9 N·m² (explicitly an extrapolation, not a measurement). That bluegill figure is
~150x *smaller* than Flammang et al.'s single-ray figure, which is backwards if both
describe the same kind of structure. I am not averaging these: the published bluegill fin
stiffness spans roughly two orders of magnitude depending on source and on whether a whole
fin or one ray is meant, and the claim's "required EI" band sits inside that disputed
range. Whoever relies on the required-EI number should resolve which bluegill quantity it
was anchored to. Related: Lauder-group work reports EI varying up to 32-fold between rays
within one pectoral fin and up to 7.5-fold along a single ray (read-level: search-summary),
so a single scalar "fin EI" is itself a coarse descriptor.

**(c) The author's third clause checks out, but is reported selectively.** Hanzelova,
Baird, Keshinro, Kadhom, Lalonde & Akimenko, "An essential role for actinotrichia in
zebrafish fin patterning and courtship behavior," *Development* 153(16):dev204990 (2026);
PMCID PMC13120675; read-level: full-text. The paper confirms *and1−/−;and2−/−* double
mutants lack actinotrichia, that adults still form rays, and states verbatim that "the
double mutant hemirays were wider" and "each hemiray was thicker than in the wild type."
But the same paper reports the adult fins are substantially disrupted: shorter and wider
rays with irregularly spaced bone segments, a wavy appearance, rays that rarely or never
bifurcate, significantly reduced ray number, and cracked distalmost bone segments. The
paper reports **no mechanical testing of any kind** — so "thicker hemirays" is a
morphological observation and carries no measured stiffness consequence in either
direction. Citing the thickening without the disruption overstates how cleanly
actinotrichia-null fins are mechanically intact.

**(d) A regime where the claim's conclusion would not hold.** Actinotrichia are the *only*
skeletal element of the larval/embryonic fin fold, before lepidotrichia form, and in
intact adult fins they are confined to the distal tip. The homologous unmineralised
ceratotrichia constitute the fin web of elasmobranchs. So there is a developmental stage
and a taxon in which actinotrichia-type fibres plausibly do carry fin load. I found no
published measurement separating the ceratotrichial web's contribution to shark pectoral
fin EI (searches: "ceratotrichia shark fin unmineralized collagen fibers flexural
stiffness load bearing fin web"; the one relevant study, a Florida Atlantic conference
abstract modelling 21 shark species' pectoral fins as cantilevers, does not decompose the
web's contribution — read-level: search-summary). This is a scope condition, not a
refutation: if S6 targets a rayed adult fin, the claim's regime is the right one; if it
targets a larval or ray-less surface, the claim does not apply.

**(e) The gain-of-function negative holds, within a stated scope.** I found no published
study in which *and1*/*and2* (or any other manipulation) *increases* actinotrichia.
Searches run: "actinodin and1 and2 mutant zebrafish actinotrichia adult fin rays
overexpression" (extended) and "Zhang 2010 Nature actinodin and1 and2 knockdown fin fold
overexpression transgenic forced expression actinotrichia increase". The 2026 *Development*
paper (full text) performs only loss-of-function and cites no overexpression. Scope limit:
these were Google-indexed web searches plus one full text; I did **not** run a systematic
PubMed/ZFIN transgenic-line query (e.g. for heat-shock-driven *and1* lines), so the
negative is "none found in indexed web search and in the most recent primary paper," not
"none exists."

## 6. Sources and read-levels

| source | read-level |
|---|---|
| Puri, Aegerter-Wilmsen, Jaźwińska & Aegerter, *J. Exp. Biol.* 221(4):jeb171777 (2018), PMC5868929 | full-text |
| Hanzelova et al., *Development* 153(16):dev204990 (2026), PMC13120675 / PMID 41885168 | full-text (first 100k chars) |
| Flammang, Alben, Madden & Lauder, *J. Morphol.* (2013), fin-ray stiffness 565e-6 N·m² | search-summary (abstract) |
| Zhang et al., *Nature* 466:234–237 (2010), actinodin knockdown | search-summary |
| Alben/Madden/Lauder and Tangorra et al. fin-ray stiffness range | search-summary |
| Shark pectoral fin EI across 21 species (FAU conference abstract) | search-summary |
| `harvest:s23-actinotrichia-stiffness-protein-wwp5m2` (the claim's own derivation) | could-not-access — not present in `kganjam/delphi-frontier`; checked by path listing and code search at the review commit |

## 7. What I could not break

The conclusion itself. "Actinotrichial stiffness is probably not what limits S6" stands:
Puri et al. conclude from their own interray-disruption experiment that adult caudal fin
flexibility "predominantly relies on the mechanical properties of the rays"; actinotrichia
in intact adult fins are restricted to the distal tip while Puri's stiffness peak sits
2–4 mm from the proximal fixation; actinotrichia-null adults still build rays; and a
single ordinary bluegill pectoral ray already exceeds the required whole-fin EI by
145–577x. Four independent lines, three of them not cited by the author, point the same
way. I did not manufacture a refutation, because the conclusion is right.

What is wrong is the KEY number's upper bound, the unlabelled caudal-for-pectoral proxy,
the unsourced 20-25x ceiling, and the inference step that treats "material alone is
insufficient" as "stiffness is not a limit."

**Recommended corrected KEY:** shortfall factor **245x–2600x**, between a *computed*
required EI of 9.8e-7–3.9e-6 N·m² and the *measured whole-fin caudal* EI of 1.5e-9–4e-9
N·m² (Puri et al. 2018) — with an explicit note that the caudal fin is a proxy for the
gliding surface, that zebrafish pectoral-fin EI is unknown, and that the gap is closable
by geometry (a 4.0x–7.2x ray thickness increase at I∝t⁴, my calculation) without any
material change.

```swarm-challenge
{"claim_id": 198, "outcome": "weakened", "reason": "The conclusion survives and is reinforced by uncited evidence, but the KEY upper bound is 2600x not 2616x from its own stated inputs, the measured baseline is an unlabelled caudal-fin proxy for a pectoral gliding surface, the ~20-25x material ceiling is unsourced, and 'material alone is insufficient' does not entail 'stiffness is not the limiter' once geometry is free (a 4.0x-7.2x ray thickness increase closes the whole gap).",
  "corrected_value": "245x-2600x shortfall (whole-fin EI ratio); residual 1.8x-5.1x ray thickness increase if a 20-25x material gain is also applied",
  "depends_on": ["required fin EI 9.8e-7 to 3.9e-6 N*m^2 (claim's computed value, derivation not inspectable in this repo)", "measured adult zebrafish caudal fin whole-fin EI 1.5e-9 to 4e-9 N*m^2, Puri et al. 2018 J Exp Biol 221:jeb171777 (full-text)", "~20-25x material-only stiffening ceiling for an unmineralised collagenous fibril (unsourced in the claim; could not verify)", "Hanzelova et al. 2026 Development 153:dev204990 - and1/and2 double mutants lack actinotrichia, adults still form rays, hemirays wider and thicker, no mechanical testing (full-text)", "Flammang et al. 2013 J Morphol - bluegill pectoral fin ray flexural stiffness 565e-6 N*m^2 (abstract-level)", "Puri et al. 2018 conclusion that adult caudal fin flexibility depends predominantly on the rays, from interray-tissue disruption (full-text)", "EI = E*I beam relation with I proportional to t^3 (depth-only) or t^4 (isometric)", "negative search scope: Google-indexed web search plus one full text; no systematic PubMed/ZFIN transgenic-line query for actinodin gain-of-function"]
}
```
