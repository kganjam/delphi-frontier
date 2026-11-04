# S6-D-D: Deepening S6-D by attacking its weakest input

**Status:** deepening pass. Calculation and literature work only. **Nothing here was measured by us.** Every
number carries one of three tags: *reported* (by the cited authors), *calculated* (by us, in
[`S6-D-deepen_calc.py`](S6-D-deepen_calc.py); run it with `python3 -I`), or *assumption* (by us, unsourced).

## 0. What is being deepened

The task brief left S6-D's recorded answer empty. I took it from the S6-D commit `cc30ccb5`
(`docs/research/fish/S6-deepen.md`, branch `origin/claude/deepen-fin-ray-s6-cj2i2x`), which I read in full:

> *S6-D answer (their words, condensed):* flying fish are observed to glide, but a lepidotrichial ray modelled
> as a passive cantilever fails to carry an equal share of glide lift. The independently reported ray
> stiffnesses (≤3.8×10⁻⁶ N·m²) give δ/L ≈ 17–42, against ~6.3×10⁻⁴ N·m² required. The 565×10⁻⁶ N·m²
> Flammang 2013 value passes only marginally. **Verdict: the passive-ray mechanism falls.**

Work done since then, which I read and build on:

- **Challenge 72** (`78d717cf`, full-text). Verdict: *weakened*. Its points:
  - S6-D left out the primary value.
  - S6-D compared absolute EI across fish of different size.
  - Load distribution moves EI_req by ×0.53–1.47.
- **Replicate 72** (`784f15b0`, full-text). It agrees on the direction of the result, and only partly blind.
- **S25** (`a7e70ebb`, full-text):
  - 565×10⁻⁶ N·m² is the number in the Flammang 2013 abstract.
  - 3.8×10⁻⁶ N·m² could not be traced to that paper, and is not a power-of-ten slip of 565×10⁻⁶.
  - The Flammang full text is still unread.
- **S26** (`b5ac55ae`, full-text). It relays Alben, Madden & Lauder 2007 (S26's read-level: full-text through
  an automated summarizer) and gives three measured values for one bluegill pectoral ray, which S6-D never used:
  - point-load stiffness 1.98 N m⁻¹ with both hemitrich bases clamped;
  - maximum ray length 40.3 ± 0.8 mm;
  - the paper's own EI estimate, 1×10⁻⁶ to 1×10⁻⁵ N·m².

## 1. The input the conclusion is most sensitive to, recomputed

S6-D's model is unchanged: an equal-share uniform-load Euler–Bernoulli cantilever, with
EI_req = P·L²/(8c), P = mg/(2N), c = 0.10. At its scenario values (m = 0.10 kg, L = 0.12 m, N = 14, all
*assumptions*), EI_req = **6.31×10⁻⁴ N·m²** (*calculated*). I asked a different question from S6-D's
factor-of-two table: **by what factor must each single input move to flip the verdict**, for each candidate
EI? (*calculated*, script §[1])

| Candidate ray EI (N·m²) | δ/L | EI must rise | L must shrink to | m, 1/N or c must move by |
|---|---|---|---|---|
| 5.65×10⁻⁴ Flammang 2013 abstract | 0.112 | ×1.12 | ×0.947 | ×0.90 |
| 4.3×10⁻⁵ Alben-k bound (§3a, new) | 1.46 | ×14.6 | ×0.26 | ×0.068 |
| 1×10⁻⁵ Alben 2007, upper | 6.3 | ×63 | ×0.13 | ×0.016 |
| 3.8×10⁻⁶ Puri 2018 relay (untraced) | 16.6 | ×166 | ×0.078 | ×0.006 |
| 1×10⁻⁶ Alben 2007, lower | 63 | ×631 | ×0.040 | ×0.002 |

What the table shows:

- **Excluding Flammang.** For every candidate except Flammang, a load-side input (m, L, N or c) must move by a
  factor of 4 to 600 to flip the verdict. §3b shows that sourced morphometrics move the whole load side by
  only ×17 end to end. So **the verdict is decided by the ray's EI, not by the load scenario.** That confirms
  S6-D's choice of weakest input, by recomputation.
- **Flammang alone** sits at the threshold. There, a 5% change in L flips the verdict.

But "EI" in S6-D is not one quantity. It is **the EI of a bluegill ray (maximum length 40.3 mm) carried over
unchanged to a flying-fish ray of ~105–160 mm**. The input the conclusion really rests on is that **transfer
across a ~3× change in ray length**. S6-D made the transfer implicitly with no size correction, which is
exponent β = 0 in EI ∝ L^β. §3c shows that this exponent alone decides the verdict.

## 2. How well established is that input?

| Component | Status | Evidence level / read-level |
|---|---|---|
| Bluegill ray EI, absolute value | Disputed by ~565× across sources: Flammang 5.65×10⁻⁴ (*reported*, authors' word "calculated", from in-vivo vortex-jet kinematics per S26) against Alben 1×10⁻⁶–1×10⁻⁵ (*reported*, excised-ray bending) | Flammang: **abstract** (re-read by me via Europe PMC). Alben: abstract read by me via Europe PMC, which does **not** contain the numbers. The numbers come from S26's full-text summary, so for me they are **relayed full-text**. Full text: **could-not-access** (Europe PMC `fullTextXML` returned HTTP 500 for PMC2359861. pmc.ncbi.nlm.nih.gov returned a reCAPTCHA page) |
| Flying-fish (Exocoetidae) ray EI | **unmeasured**. No value found | Negative-search scope: S6-D's Europe PMC query (35 hits, all titles read); my Europe PMC query `("flying fish" OR Exocoetidae OR Exocoetus OR Cheilopogon OR Hirundichthys OR Cypselurus) AND ("wing loading" OR "body mass" OR morphometr* OR "pectoral fin")`, 103 hits, first 60 titles read, none a ray-mechanics measurement; two web searches. Google Scholar, Web of Science and grey literature not searched |
| Scaling exponent β, bluegill → flying fish | **assumption**: never measured, never stated. S6-D used β = 0 without saying so. Challenge 72 objected to the size-uncorrected comparison but did not compute the exponent the verdict needs | none |

So the decisive input is **an unstated assumption that has been repeated until it reads as measured**. The
EI numbers are measured or calculated by their authors. Applying them, size-uncorrected, to a 3× longer ray is
an assumption.

## 3. Improving the input

### 3a. A new bound on the passive bluegill ray, from Alben's measured stiffness (*calculated*)

Alben et al. 2007 measured point-load stiffness k = 1.98 N m⁻¹ on one ray with both hemitrich bases clamped,
on a ray at most 40.3 mm long. This is the **actively locked**, stiffer state: S26 relays a ~12× clamped/free
ratio. For a cantilever with a rigid root, a point load at distance a gives k = 3EI/a³. The load point cannot
lie beyond the ray tip, so:

**EI ≤ k·L³/3 = 4.3×10⁻⁵ N·m²** (*calculated*, load at the tip). Load points of 10–30 mm give
6.6×10⁻⁷–1.8×10⁻⁵ N·m².

Two checks (*calculated*):

1. **Consistency.** Alben's stated range of 1×10⁻⁶–1×10⁻⁵ N·m² implies a load point at a = 11.5–24.7 mm.
   That lies inside the ray, so Alben's k and Alben's EI agree with each other.
2. **Exclusion.** For EI = 5.65×10⁻⁴ at k = 1.98 N m⁻¹, the load would have to sit 95 mm out, on a ray that is
   at most 40.3 mm long. Under this model, then, **565×10⁻⁶ N·m² cannot be the bending stiffness of Alben's
   excised, base-clamped bluegill ray**, even in the locked state.

This is my inference, not either author's claim. It fits S26's relay that Flammang inverted *in-vivo*
kinematics, and S25's finding that 565×10⁻⁶ cannot be rebuilt as an Euler–Bernoulli EI from the abstract's
force and curvature. In both readings, 565×10⁻⁶ is a different quantity from a passive ray's EI.

Caveats:

- The load point Alben used is `unknown` to me (full text not read).
- A compliant root would make the measured k under-read the beam's EI, so the bound is not strict if the
  root rotated.
- The bound rests on **one ray of one fish** (n = 1).

**Effect on S6-D at β = 0** (*calculated*): the best passive bluegill value is now ≤4.3×10⁻⁵, which gives
δ/L ≥ 1.46. The marginal "Flammang pass" is removed. **For a bluegill-sized ray, S6-D's verdict strengthens.**

### 3b. The load side, with sourced morphometrics (*calculated* from mostly search-summary inputs)

| Input | Range used | Source | Read-level |
|---|---|---|---|
| m | 89–188 g | *Hirundichthys affinis*, NE Brazil, TL 23.4–29.4 cm | **search-summary** (scielo.br refused by this session's network) |
| L | 105–160 mm | *Cypselurus hiraii* span 233–261 mm, SL 199–209 mm (Park & Choi group, as summarised in replicate-72), giving ~105–118 mm semi-span. Ceiling ≤0.78–0.79 SL (Davenport 1992) | search-summary / **abstract** |
| pectoral share s | 0.8–1.0 | replicate-72: pelvic fins ≈20% of wing area | search-summary |
| load distribution | ×0.53–1.47 | challenge-72 | calculated |
| N | 14 | no ray count found (FishBase refused) | **assumption**. N = 10 or 18 gives 8.8×10⁻⁴ or 4.9×10⁻⁴ |

Result (*calculated*): **EI_req = 1.8×10⁻⁴ to 3.1×10⁻³ N·m²**, with S6-D's 6.3×10⁻⁴ near the middle. S6-D's
load scenario stands, with a ±4–5× error bar it did not state. A measured flying-fish wing loading is still
`unknown`. Fish 1990 (199 specimens) and Davenport's tables were both refused by this session's network
(health-sciences.wcupa.edu, cambridge.org, scribd.com). Read-level for both: **search-summary**.

### 3c. The transfer exponent the verdict needs (*calculated*)

The scaled-proxy stiffness is EI_ff = EI_bg × (L_ff / 40.3 mm)^β. The β needed to reach EI_req:

| L_ff | λ = L_ff/L_bg | EI_req | β needed: Alben 1e-6 | Alben 1e-5 | k-bound 4.3e-5 |
|---|---|---|---|---|---|
| 105 mm | 2.61 | 4.8×10⁻⁴ | 6.5 | 4.1 | 2.5 |
| 120 mm | 2.98 | 6.3×10⁻⁴ | 5.9 | 3.8 | 2.5 |
| 160 mm | 3.97 | 1.1×10⁻³ | 5.1 | 3.4 | 2.4 |

Reference exponents (standard scaling models, not measured for fin rays):

- **β = 0**: S6-D's implicit choice, a flying-fish ray as thick as a bluegill ray.
- **β = 4**: isometry, with ray diameter proportional to length.
- **β = 6**: elastic similarity, with d ∝ L^1.5.

Under isometry, at L = 120 mm:

- Alben's range maps to 7.9×10⁻⁵–7.9×10⁻⁴ N·m², which straddles the requirement.
- The k-bound maps to 3.4×10⁻³ N·m², which passes ~5×.

**So the passive ray fails only if flying-fish rays are, relative to their length, markedly more slender
than a geometrically scaled-up bluegill ray (β ≲ 2.5–4).** Nothing I could find measures that. It is
plausible either way:

- Thin, high-aspect-ratio wings argue for slender rays.
- A load-bearing gliding fin argues for robust ones.

This is my inference. No source makes the argument.

Puri et al. 2018 (**full-text**, read by me via Europe PMC XML) do use a d⁴ scaling argument between species:
"Given the diameter of bluegill rays of 1–2 mm compared with 0.2 mm for zebrafish, one would expect zebrafish
rays to be more than four orders of magnitude more flexible". They treat EI as tracking ray diameter, not as a
species constant. That supports correcting for size. It does not tell us the flying-fish diameter.

### 3d. The measurement that settles it, and its cost

The question reduces to one number: **the base diameter, or better the second moment of area, of a load-bearing
flying-fish pectoral ray**. The solid-section diameter that meets EI_req is (*calculated*):

| E | d at EI_req = 1.8×10⁻⁴ | at 6.3×10⁻⁴ | at 3.1×10⁻³ |
|---|---|---|---|
| 0.24 GPa | 1.98 mm | 2.70 mm | 4.03 mm |
| 1.0 GPa | 1.39 mm | 1.89 mm | 2.82 mm |
| 3.7 GPa | 1.00 mm | 1.37 mm | 2.03 mm |

The E bracket 0.24–3.7 GPa is a **search-summary** value (attributed to the Lauder group), and S9-D argues that
fin-ray "modulus" is itself model-dependent. Real hemitrichia are hollow crescents, so their I is below the
solid value at the same outer diameter. The rough reading of a measurement:

- base diameter ≲1 mm: the passive ray fails across the whole bracket;
- ≳4 mm: it passes across the whole bracket;
- 1–4 mm: E and I must be measured too.

| Step | What | Cost (my estimate, not sourced) |
|---|---|---|
| 1 (cheapest, most informative) | Calipers or micro-CT on the leading 3–4 pectoral rays, near the base, of preserved museum Exocoetidae (any *Cheilopogon*, *Cypselurus*, *Hirundichthys*), with fish mass, ray length and ray count from the same specimens. This fixes I, L, m and N together and leaves only E | Hours, plus museum access. Micro-CT is roughly a day of scanner time |
| 2 | Three-point bending (Aiello 2018 protocol) on fresh or frozen excised rays, which gives EI directly | As S6-D estimated: weeks in a lab with a micro-mechanical tester |
| 3 | Read Alben 2007 and Flammang 2013 in full, for Alben's load point and Flammang's inversion method | Library access only. Blocked here by network policy |

## 4. Recomputed conclusion

| Case | Ray EI used | δ/L at 120 mm, central load | Passive ray carries? |
|---|---|---|---|
| S6-D as written (β = 0, Flammang counted as passive) | 5.65×10⁻⁴ | 0.11 | marginal |
| β = 0, best passive value (k-bound) | 4.3×10⁻⁵ | 1.46 | **no**. Falls, more firmly |
| β = 4 (isometric), Alben range | 7.9×10⁻⁵–7.9×10⁻⁴ | 0.80–0.08 | straddles |
| β = 4 (isometric), k-bound | 3.4×10⁻³ | 0.019 | **yes** |

All rows are *calculated*. None is an observation.

**Verdict on S6-D's conclusion: FALLS.**

S6-D's conclusion was "the passive-ray mechanism falls". That conclusion is not supported once its decisive
input is made explicit:

- It rested on transferring a 40 mm bluegill ray's absolute EI to a ~120 mm flying-fish ray with no size
  correction (β = 0). S6-D neither stated nor justified that.
- With the improved input (an Alben-k bound of ≤4.3×10⁻⁵ N·m² on the passive, base-locked bluegill ray), the
  fail **strengthens** for a bluegill-proportioned ray.
- It **reverses** under isometric scaling.
- The β needed to reach the requirement, ≥2.5 for the k-bound and ~3.8–5.9 across Alben's range, sits inside
  the plausible range of 0–6.

The honest statement is no longer "a passive ray fails". It is: **"a passive ray of bluegill proportions
fails. Whether a passive flying-fish ray fails depends on its unmeasured base cross-section; the threshold is a
solid-equivalent diameter of ~1.4–2.8 mm at E ≈ 1 GPa."** The organ-level observation, that flying fish glide
(Park & Choi 2010, **abstract**), is unaffected.

What does **not** change:

- The load scenario. It stands, with a ±4–5× band.
- The finding that 3.8×10⁻⁶ N·m² is untraced (S25).
- The disagreement between Flammang 2013 and Alben 2007 over bluegill EI. It is preserved, not averaged, and
  §3a argues the two describe different quantities.

## Sources

| Source | Read-level (this pass) |
|---|---|
| S6-deepen.md + s6_deepen_calc.py (commit cc30ccb5) | full-text |
| challenge-72.md (78d717cf), replicate-72.md (784f15b0), S25-organ.md (a7e70ebb), S26-organ.md (b5ac55ae) | full-text |
| Alben S, Madden PGA, Lauder GV 2007 *J R Soc Interface* 4:243, doi:10.1098/rsif.2006.0181 | abstract (Europe PMC, by me); k = 1.98 N m⁻¹, L = 40.3 mm and EI 1e-6–1e-5 are **relayed from S26's full-text summary**; full text could-not-access |
| Flammang BE, Alben S, Madden PGA, Lauder GV 2013 *J Morphol* 274:1044, doi:10.1002/jmor.20161 | abstract (Europe PMC, by me) |
| Aiello BR et al. 2018 *J Exp Biol* 221:jeb163360 | abstract (Europe PMC, by me) |
| Puri S et al. 2018 *J Exp Biol* 221:jeb171777, PMC5868929 | full-text (Europe PMC XML, by me) |
| Park H, Choi H 2010 *J Exp Biol* 213:3269, doi:10.1242/jeb.046052 | abstract (Europe PMC, by me; no mass or span in the abstract) |
| Davenport J 1992 *J Mar Biol Assoc UK* | abstract (relayed by S6-D) and search-summary |
| Fish FE 1990 *J Zool* 221:391 | search-summary (PDF host refused) |
| *Hirundichthys affinis* NE Brazil length–weight (Brazilian J Biol, scielo) | search-summary (host refused) |
| Park & Choi group IUTAM 2007 *C. hiraii* span/SL | search-summary (relayed by replicate-72) |
| Bluegill ray E 0.24–3.7 GPa (Lauder group) | search-summary (relayed by S26/S6-D) |

Hosts refused in this session: www.scribd.com, www.cambridge.org, www.scielo.br, health-sciences.wcupa.edu,
rcremote.wcupa.edu, typeset.io, www.fao.org, fishbase.se. Europe PMC full-text XML refused PMC2359861,
PMC5410822 and PMC9172250 (publisher does not allow XML download). Allowing those domains would let a later pass
read Fish 1990 (measured wing loading) and the *H. affinis* length–weight fit directly.

```swarm-result
{"subproblem": "S6-D-D", "evidence": "derived: calculation on reported bluegill ray stiffness (Alben 2007 measured k relayed at full-text via S26; Flammang 2013 at abstract) and search-summary flying-fish morphometrics; no Exocoetidae ray EI or cross-section measured; the decisive bluegill-to-flying-fish size-transfer exponent is an assumption", "answer": "S6-D's 'passive ray falls' verdict rested on transferring a 40 mm bluegill ray's absolute EI unchanged to a ~120 mm flying-fish ray (scaling exponent beta=0, unstated); Alben 2007's measured 1.98 N/m clamped-base stiffness bounds the passive bluegill ray at EI <= 4.3e-5 N m^2 (calculated), which rules out 565e-6 as a passive excised-ray value and makes a bluegill-proportioned ray fail more firmly (delta/L >= 1.46), but under isometric scaling the same bound gives 3.4e-3 N m^2 and passes against a required 1.8e-4 to 3.1e-3 N m^2, so whether a passive flying-fish ray carries glide load is unresolved and hinges on its unmeasured base cross-section (solid-equivalent threshold ~1.4-2.8 mm at E ~ 1 GPa).", "key_number": "passive bluegill pectoral ray EI <= 4.3e-5 N m^2 (calculated from Alben 2007 k = 1.98 N/m, L = 40.3 mm); size-transfer exponent beta >= 2.5 needed for a 120 mm flying-fish ray to reach EI_req = 6.3e-4 N m^2 (range 1.8e-4 to 3.1e-3)", "verdict": "falls", "depends_on": ["S6-D conclusion and model: equal-share uniform-load Euler-Bernoulli cantilever, delta/L <= 0.10 criterion (assumption), commit cc30ccb5", "S6-D scenario inputs m=0.10 kg, L=0.12 m, N=14, n=1 (assumptions)", "Alben, Madden & Lauder 2007 J R Soc Interface 4:243: point-load stiffness 1.98 N/m with both hemitrich bases clamped, one bluegill ray (measured; relayed full-text via S26)", "Alben 2007: bluegill max pectoral ray length 40.3 +/- 0.8 mm (measured; relayed via S26)", "Alben 2007: bluegill ray EI 1e-6 to 1e-5 N m^2 (reported; relayed via S26)", "Alben 2007: clamped/free stiffness ratio ~12x (measured, n=1; relayed via S26)", "assumption: Alben's load point lies within the ray length and the root is rigid (k = 3EI/a^3)", "Flammang et al. 2013 abstract: EI 565e-6 N m^2, 'calculated' (abstract)", "S26 relay: Flammang 2013 EI inverted from in-vivo vortex-jet kinematics (search-summary)", "S25: 3.8e-6 N m^2 untraced to Flammang 2013; not a unit slip", "Puri et al. 2018 full-text: bluegill ray diameter 1-2 mm; EI scales with d^4 across species", "Aiello et al. 2018 JEB abstract: labrid ray EI 0.0001-1.5109 uN m^2", "assumption: size transfer EI proportional to L^beta with beta unmeasured (0, 4, 6 as reference models)", "Hirundichthys affinis mass 89-188 g at TL 23.4-29.4 cm (search-summary)", "Cypselurus hiraii span 233-261 mm, SL 199-209 mm (search-summary via replicate-72)", "Davenport 1992 abstract: pectoral fin length <= 78-79% SL", "pectoral share of lift 0.8-1.0 from pelvic ~20% of wing area (search-summary via replicate-72)", "challenge-72: spanwise load-distribution factor x0.53-1.47 (calculated)", "fin-ray modulus bracket 0.24-3.7 GPa (search-summary, Lauder group)", "Park & Choi 2010 abstract: flying fish glide (observed, organ level)"]}
```
