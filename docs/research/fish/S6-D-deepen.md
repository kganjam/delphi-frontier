# S6-D-D: Deepening S6-D by attacking its weakest input

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.

**Status:** calculation and literature work only. **No experiment was run, and we measured nothing.**
Every number carries one of three tags: *quoted*, meaning reported by the cited authors, with the source's
read-level; *calculated*, meaning computed by us in [`s6_d_deepen_calc.py`](s6_d_deepen_calc.py), which you can
rerun with `python3 docs/research/fish/s6_d_deepen_calc.py`; or *assumption*, meaning ours and unsourced.

---

## 0. What we are deepening, and a scope problem found on the way

**The S6-D answer.** It sits on branch `claude/deepen-fin-ray-s6-cj2i2x`, file `docs/research/fish/S6-deepen.md`,
and we read it in full. It concludes that **the passive-ray mechanism "falls"**. In its reference scenario a
lepidotrichial ray is modelled as a passive cantilever:
- The scenario inputs are assumptions: m = 0.10 kg, N = 14 rays per fin, L = 0.12 m, n = 1, failure at
  δ/L > 0.10.
- The ray needs EI ≥ 6.3×10⁻⁴ N·m² (calculated).
- The S6-D answer treats the reported ray stiffnesses as ≤ 3.8×10⁻⁶ N·m². At that value δ/L ≈ 17. That is
  166× short of the requirement.

**Scope problem.** S6-D says the S6 answer "arrived empty". It therefore *reconstructed* an S6 answer about a
**100 g flying fish** and attacked that. The real S6 answer does exist, on branch `claude/s6-fin-ray-load-kqweu7`
(`docs/research/fish/S6-organ.md`, read in full). It is about a **0.4 g zebrafish**. It used a **measured**
zebrafish whole-caudal-fin stiffness (Puri et al. 2018, EI 1.5–4×10⁻⁹ N·m²) and concluded "No, a 9–196×
shortfall".

So S6-D did not test the S6 conclusion. Nothing below bears on the zebrafish S6 result either. The flaw we
identify, an unscaled cross-species EI, is absent from S6 because S6 used zebrafish data. This document deepens
S6-D's own conclusion, the flying-fish passive-ray verdict, because that is the answer we were handed.

## 1. The input S6-D's conclusion is most sensitive to, shown by recomputing

S6-D's verdict comes down to one ratio, R = EI_req / EI_ray. R > 1 means the ray fails. At EI_ray = 3.8×10⁻⁶,
R = **166** (calculated). Every input was perturbed by a factor of two (calculated, §1 of the script):

| Perturbation | R | Verdict |
|---|---|---|
| baseline | 166 | fails |
| EI ×2 / ÷2 | 83 / 332 | fails |
| L ×2 / ÷2 | 664 / 41.5 | fails |
| m ×2 / ÷2 | 332 / 83 | fails |
| N ×2 / ÷2 | 83 / 332 | fails |

**No factor-of-two change in any input flips the conclusion.** S6-D's own sensitivity table was computed around
565×10⁻⁶ N·m², the value its conclusion does *not* rest on, so it showed flips that do not apply to the 166×
verdict.

Two changes to the *EI input* do move R across 1. Both are much larger than a factor of two:

1. **Source choice.** The value is 565×10⁻⁶ N·m² in the Flammang et al. 2013 abstract and 3.8×10⁻⁶ N·m² as
   relayed by Puri et al. 2018. That is a factor of **148.7**. R moves from 166 to 1.12 (calculated).
2. **Size transfer.** The candidate EIs are measured on bluegill or labrid rays a few centimetres long. The
   requirement is for a **120 mm** ray. EI is extensive, scaling as E·d⁴. If ray diameter scales with length,
   a 40.3 mm ray scaled to 120 mm gains (120/40.3)⁴ = **79×** in EI (calculated). S6-D applied **no** size
   correction. Challenges 72 and 74 both raised this qualitatively.

**The weakest input is therefore the EI of a 120 mm lepidotrichium.** S6-D did not use it. It used the
*absolute* EI of a much shorter ray of a different species, with no size transfer.

## 2. How well is that input established?

- **The real quantity: unmeasured.** That is the EI of an exocoetid pectoral ray about 12 cm long. We
  re-searched Europe PMC with `("flying fish" OR Exocoetidae OR Cypselurus OR Cheilopogon OR Exocoetus OR
  Hirundichthys) AND ("fin ray" OR pectoral) AND (stiffness OR flexural OR bending OR morphology OR "micro-CT")`.
  It returned 42 hits. We read every title and none is a ray-mechanics or ray-cross-section measurement.
  - Scope: Europe PMC only. Google Scholar, Web of Science and grey literature were not searched.
  - Controls: a must-fail nonsense query returned 0 hits.
- **Size scaling of ray EI: unmeasured.** Query: `("fin ray" OR lepidotrichia OR lepidotrichium) AND (allometry
  OR scaling OR "body size") AND (stiffness OR "flexural" OR "second moment")`. It returned 20 hits and none
  measures how ray EI scales with ray length, within or across species.
  - Positive control: the same query retrieved Alben et al. 2007, which is a known ray-mechanics paper.
  - Aiello et al. 2018 *J Morphol* (abstract, as quoted in challenge 72) says the second moment I "explained the
    majority of the variation" in EI. That supports, but does not measure, a d⁴ dependence.
- **The value S6-D used is a proxy with an untraced origin.** We re-read Puri et al. 2018 at **full-text**
  (pmc.ncbi.nlm.nih.gov, PMC5868929). The 3.8×10⁻⁶ sentence carries **no citation**:
  > "Previous measurements of bending stiffness of larger fish have reached a sensitivity of 10⁻⁶ N m² (Flammang
  > et al., 2013) … As there are 16–18 rays making up the entire zebrafish fin, the bending stiffness of bluegill
  > rays of 3.8×10⁻⁶ N m² would indicate…"

  The Flammang citation belongs to the previous sentence, which is about *sensitivity*. Attributing 3.8×10⁻⁶ to
  Flammang 2013 is S6-D's reading, and S25's. It is not something Puri states. S25 found 3.8×10⁻⁶ in no copy
  of the Flammang abstract.

**Honest rating.** In S6-D, EI is *a proxy for a different quantity*: a short bluegill ray standing in for a long
flying-fish ray. Its exact value is untraced, and it entered S6-D's headline with no size correction. It is a
proxy that has been repeated until it reads as measured.

## 3. Improving it

### 3a. A primary bluegill measurement at full text: Alben, Madden & Lauder 2007

Earlier passes disagreed about the read-level of this paper. S6-organ said full-text. S6-D said "abstract (PMC
copy is not open-access full text)". This session read the **full text** from pmc.ncbi.nlm.nih.gov
(PMC2359861), so the disagreement is resolved: the full text is reachable. Europe PMC's `fullTextXML` endpoint
returned HTTP 500, which is probably what S6-D hit.

Quoted from that full text:

- *Specimens:* six bluegill, "maximum ray length = 40.3 ± 0.8 mm, mean ± s.e.". Twenty-four rays were tested.
  The rays were dissected and submersed in water within 48 h of euthanasia.
- *Three-point bending:* "the 'composite' Young's modulus corresponding to the whole structure is E ≈ 10⁸–10⁹
  N m⁻², with the average area moment of inertia I ≈ 10⁻⁶ cm⁴". Calculated: EI = **1×10⁻⁶ to 1×10⁻⁵ N·m²**
  (order of magnitude).
- *Point-force test:* "a vertical point force is applied at two-thirds of the distance from the ray base to the
  tip". Force was measured against tip deflection. With both hemitrich bases clamped, "the force–displacement
  curve may be fit with a slope of 1.98 N m⁻¹, about 12 times the value when one hemitrich is free".

**Back-calculation (calculated, ours).** We assume a uniform cantilever with a point load at a = 2L/3:
δ_tip = F·a²(3L − a)/(6EI), so EI = k·a²(3L − a)/6. The tested length is not reported per ray, so we used the
40.3 mm *maximum*, which makes this an upper bound.
- Both bases clamped (locked): EI ≈ **2.2×10⁻⁵ N·m²**.
- One base free (passive, k/12): EI ≈ **1.9×10⁻⁶ N·m²**.
- At a tested length of 30 mm, these fall to 9.5×10⁻⁶ and 7.9×10⁻⁷ N·m².

These numbers agree with the authors' own E·I order of magnitude.

**Disagreement, preserved and not averaged:**

| Bluegill pectoral ray EI | Value (N·m²) | Read-level | Relation to Alben's E·I range |
|---|---|---|---|
| Alben et al. 2007, E·I | 1×10⁻⁶ – 1×10⁻⁵ | full-text | — |
| Alben et al. 2007, our back-calculation (passive / locked) | 1.9×10⁻⁶ / 2.2×10⁻⁵ | calculated from full-text values | inside / 2× above |
| Puri et al. 2018, relayed, no citation | 3.8×10⁻⁶ | full-text (Puri); origin untraced | inside |
| Flammang et al. 2013 abstract, "calculated" | 565×10⁻⁶ | abstract; full text **could-not-access** | **56–565× above** |

**Our inference, not any author's claim:** two full-text figures, one measured directly and one relayed, agree
on about 10⁻⁶–10⁻⁵ N·m² for a passive bluegill ray. Flammang's 565×10⁻⁶ is the outlier, even though it shares
authors (Madden, Lauder) with Alben 2007. It could describe a different quantity, region or state, for example
a proximal unsegmented section or a whole fin. We could not read its Methods. We tried the following hosts and
each failed:
- web.njit.edu, public.websites.umich.edu, sites.harvard.edu: no connection (proxy).
- onlinelibrary.wiley.com: 403.
- api.unpaywall.org, api.semanticscholar.org, api.openalex.org, scholar.archive.org: connection rejected by
  this session's network policy.

So we keep 565×10⁻⁶ as an unresolved alternative. We do not discard it.

### 3b. The size transfer, done explicitly

For a solid section, EI/L⁴ = E·(π/64)·(d/L)⁴. This index has units of Pa and does not depend on size for
geometrically similar rays. The requirement is EI_req/L⁴ = 6.3×10⁻⁴ / 0.12⁴ = **3.04 Pa** (calculated). We
transferred each bluegill value from L = 40.3 mm assuming **isometry (EI ∝ L⁴, same tissue modulus)**. That is
an assumption, and §2 shows nobody has measured it. b_flip is the scaling exponent in EI ∝ L^b above which the
scaled ray would meet the requirement.

| Bluegill candidate (L_ray = 40.3 mm) | EI/L⁴ (Pa) | R, unscaled (S6-D's method) | R, isometric | δ/L, isometric | b_flip |
|---|---|---|---|---|---|
| Alben E·I, low (1e-6) | 0.38 | 631 | 8.0 | 0.80 | 5.9 |
| Alben back-calculation, one base free (**passive**) | 0.71 | 338 | **4.3** | 0.43 | 5.3 |
| Puri-relayed 3.8e-6 (ray length assumed 40 mm) | 1.44 | 166 | 2.1 | 0.21 | 4.7 |
| Alben E·I, high (1e-5) | 3.79 | 63 | 0.80 | 0.08 | 3.8 |
| Alben back-calculation, both bases clamped (**locked**) | 8.49 | 28 | **0.36** | 0.036 | 3.1 |
| Flammang abstract 565e-6 (ray length assumed 40 mm) | 214 | 1.1 | 0.014 | 0.001 | ≈0.1 |

Adding challenge 72's load-distribution band (×0.53 to ×1.47 on EI_req) to the passive isometric case gives
R = **2.3–6.3** for the back-calculation and 0.43–11.8 across Alben's full E·I range (calculated).

A cross-check on slenderness (calculated):
- Alben's I = 10⁻¹⁴ m⁴ corresponds to a solid-equivalent diameter of 0.67 mm, which is d/L = **1.67 %** of a
  40.3 mm ray.
- The requirement corresponds to d/L = **1.58 %** at E = 1 GPa and **2.81 %** at E = 0.1 GPa.

So an isometrically scaled bluegill ray sits right at the requirement's slenderness. Which side it lands on
depends on E, which Alben gives only to within a factor of 10.

### 3c. What would settle it, and what it would cost

| Step | Measurement | What it removes | Cost |
|---|---|---|---|
| 1, cheapest | Read the Flammang 2013 Methods: specimen, ray, region, and how "calculated" was done | The 565×10⁻⁶ outlier (×149 swing) | Library access only. Could-not-access here (network policy) |
| 2 | Micro-CT of one or two exocoetid pectoral fins (a museum specimen is enough) for I(s) of the leading and mid rays, plus ray length and count | The size-transfer exponent and three of S6-D's four scenario assumptions (L, N, and ray d/L); E still comes from bluegill | One micro-CT session plus a specimen loan. No quote obtained; cost `unknown` |
| 3, decisive | Three-point and cantilever bending of fresh exocoetid rays (Aiello 2017/2018 protocol), with one hemitrich base free vs both clamped (Alben 2007 protocol) | EI_ray directly, passive and locked | S6-D estimated weeks of lab time (its own unsourced estimate). Not re-costed |

## 4. Recomputed conclusion

**S6-D's conclusion was:** a passive lepidotrichial ray cannot carry an equal share of glide lift (166×
short), so flight has to rely on unmeasured stiffening or on a stiffer flying-fish ray.

With the improved input, calculated:

- **Without size transfer** (S6-D's method, now with full-text Alben values): R = 28–631. The passive ray fails
  by more. Only the Flammang abstract value (R = 1.1) comes close, and it is now an outlier against two
  full-text figures.
- **With isometric size transfer** (the physically motivated null; it is an assumption): the passive bluegill-type
  ray is short by **R ≈ 4.3** (back-calculation). The span is 0.8–8 across Alben's E·I range and 2.3–6.3 with
  the load-distribution band. In most of that range **it still fails**, but by ~2–8×, not 166×. Two other things
  change:
  - The **measured** bluegill base-locking effect (12×, Alben 2007, full-text) would **close** the gap
    (R = 0.36). This contradicts S26's "active stiffening does not close the gap". S26 used the same unscaled
    absolute EI, so its conclusion inherits the flaw described here. That is our inference; S26 has not been
    re-run.
  - The "stiffer flying-fish ray" that S6-D's escape route needs is only 2–8× stiffer than an isometrically
    scaled bluegill ray. Equivalently, EI would need to scale with ray length at b ≥ 4.7–5.3 instead of 4. That
    is well inside what nobody has measured.

**Verdict: STANDS, with its margin cut by one to two orders of magnitude.** The direction holds: a *passive*,
bluegill-proportioned lepidotrichium falls short under every central estimate, scaled or not. The size of the
shortfall does not hold. The 166× figure came from comparing absolute EI across a threefold length difference.
After the size transfer, the shortfall is a few-fold. A factor of 1.5–2 in the assumed ray length L, or the
measured 12× hemitrich locking, would erase it. Two things would make the conclusion **fall**:
- the Flammang 565×10⁻⁶ value turning out to describe a passive whole ray of about 40 mm; or
- flying-fish ray EI scaling faster than about L^4.7.

## 5. What this does not establish

1. **Nothing about zebrafish.** S6's zebrafish answer rests on a measured zebrafish fin and is untouched here.
   §0 explains why S6-D did not test it.
2. **Not that isometric scaling holds.** It is the null assumption, and it is unmeasured for lepidotrichia
   (§2). Flying-fish rays could be relatively thinner or thicker.
3. **Not a precise bluegill EI.** Alben's E and I are order-of-magnitude figures. Our back-calculation assumes a
   uniform beam and a tested length equal to the 40.3 mm maximum. Real rays taper and are segmented over most
   of their length, so a uniform-beam EI is an effective value.
4. **Not that bluegill tissue modulus transfers to Exocoetidae.**
5. **Not the Flammang Methods.** The 149× disagreement is narrowed (two full-text figures sit near 10⁻⁶–10⁻⁵),
   not resolved.
6. **Not that the shared failure criterion (δ/L ≤ 0.10) is right.** It is S6-D's assumption and also S6's.

## Sources

| Source | Read-level (this session) |
|---|---|
| S6-organ.md, branch `claude/s6-fin-ray-load-kqweu7` | full-text |
| S6-deepen.md and s6_deepen_calc.py, branch `claude/deepen-fin-ray-s6-cj2i2x` | full-text |
| S25-organ.md (branch `claude/s25-flammang-fin-ray-stiffness-gkwnb4`), S26-organ.md (`claude/active-fin-ray-stiffening-l53vks`), challenge-72/73/74 | full-text (repository) |
| Alben S, Madden PGA, Lauder GV 2007, *J R Soc Interface* 4:243–256, doi:10.1098/rsif.2006.0181, PMC2359861 | **full-text** (pmc.ncbi.nlm.nih.gov HTML) |
| Puri S et al. 2018, *J Exp Biol* 221:jeb171777, PMC5868929 | **full-text** (pmc.ncbi.nlm.nih.gov HTML) |
| Aiello BR, Westneat MW, Hale ME 2017, *PNAS* 114:4459, PMC5410822: labrid EI at 50 % ray length 20–40 and 190–210 ×10⁻⁹ N·m², SL 7.3–13.2 cm | **full-text** (pmc.ncbi.nlm.nih.gov HTML). Ray lengths not given in the text we read, so this was not used in the size transfer |
| Flammang BE, Alben S, Madden PGA, Lauder GV 2013, *J Morphol* 274:1044–1059, doi:10.1002/jmor.20161 | abstract (Europe PMC); full text **could-not-access** |
| Aiello BR et al. 2018, *J Morphol* 279, doi:10.1002/jmor.20830 | abstract, as quoted in challenge 72; not re-read this session |

```swarm-result
{"subproblem": "S6-D-D", "evidence": "derived: calculation on bluegill ray stiffness read at full text (Alben 2007), transferred to a 120 mm ray under an unmeasured isometric-scaling assumption; scenario load inputs remain S6-D assumptions; no Exocoetidae ray measured",
  "answer": "S6-D's passive-ray verdict stands in direction but its 166x margin was an artifact of comparing absolute EI of ~40 mm bluegill rays against a 120 mm ray requirement: with full-text Alben 2007 values (passive EI ~1.9e-6 N m^2 back-calculated from 1.98 N/m clamped / 12, at 40.3 mm) transferred isometrically, the passive ray is ~4x short (0.8-8x across Alben's E*I range), the measured 12x hemitrich locking would close it, and the conclusion would fall if the Flammang-2013 565e-6 N m^2 abstract value (56-565x above Alben, Methods unread) describes a passive ~40 mm ray or flying-fish ray EI scales faster than ~L^4.7.",
  "key_number": "size-normalised passive bluegill ray stiffness EI/L^4 ~0.7 Pa (0.4-3.8 Pa) vs 3.0 Pa required, i.e. shortfall ~4.3x (0.8-8x) rather than 166x; passive ray EI ~1.9e-6 N m^2 at L = 40.3 mm",
  "verdict": "stands",
  "depends_on": [
    "S6-D conclusion and scenario (docs/research/fish/S6-deepen.md, branch claude/deepen-fin-ray-s6-cj2i2x): m=0.10 kg, N=14 rays/fin, L=0.12 m, n=1, two pectoral fins share lift equally (assumptions)",
    "failure criterion delta/L <= 0.10 (assumption, shared with S6)",
    "uniform Euler-Bernoulli cantilever under uniform load (model assumption; challenge-72 load-distribution factor 0.53-1.47)",
    "Alben, Madden & Lauder 2007 full-text: bluegill max pectoral ray length 40.3 +/- 0.8 mm (measured)",
    "Alben et al. 2007 full-text: composite E ~1e8-1e9 N m^-2 and I ~1e-6 cm^4 from three-point bending and microCT (measured, order of magnitude)",
    "Alben et al. 2007 full-text: clamped-base point-force stiffness 1.98 N/m at 2/3 ray length, ~12x the one-base-free value (measured)",
    "back-calculation assumption: tested ray length = 40.3 mm maximum, uniform beam, load at 2L/3, tip deflection",
    "isometric size transfer EI ~ L^4 at constant tissue modulus from bluegill to a 120 mm exocoetid ray (assumption, unmeasured)",
    "bluegill tissue modulus transferable to Exocoetidae (assumption)",
    "Puri et al. 2018 full-text: bluegill ray EI 3.8e-6 N m^2 stated without citation (relayed, origin untraced)",
    "Flammang et al. 2013 abstract: EI 565e-6 N m^2 'calculated' (abstract only; Methods could-not-access)",
    "S25: 3.8e-6 absent from Flammang 2013 abstract (abstract-level)",
    "negative search: no Exocoetidae fin-ray mechanics or ray-EI allometry in Europe PMC (scope: Europe PMC only, 42 and 20 hits screened by title)"
  ]}
```
