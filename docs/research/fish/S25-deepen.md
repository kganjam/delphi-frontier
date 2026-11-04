# S25-D: deepening S25, the Flammang 2013 fin-ray stiffness (3.8e-6 or 565e-6 N m²)

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.
Parent: `docs/research/fish/S25-organ.md` (branch `claude/s25-flammang-fin-ray-stiffness-gkwnb4`, commit a7e70eb).
I also read the two challenges filed against it first: challenge-160 (branch
`claude/flammang-fin-ray-challenge-4hbgk4`) and challenge-73 (branch `claude/flammang-fin-ray-challenge-8i750r`).
Calculations: `docs/research/fish/S25_deepen_calc.py` (`python3 -I`). **Every number tagged "calculated" comes
from that script. None of them is an observation.**

## Short answer

S25 answered in two parts:

- **Part 1, the textual part.** The Flammang 2013 abstract prints 565 × 10⁻⁶ N m², and 149× is not a
  unit slip. This part **stands**. I re-checked it, and the sensitivity test in §1 shows it does not move.
- **Part 2, the interpretive part.** S25 said 565e-6 is the relaying to trust and that 3.8e-6 should be treated
  as a misattribution. This part **falls**.

The input that part 2 rests on is the **bending geometry of a bluegill pectoral ray**. S25 used a 1–2 mm solid
rod as its implicit bracket. A factor of 2 in diameter is a factor of 16 in EI, which is enough to move a ray from
one value to the other (calculated, §1). I replaced that proxy with the nearest primary measurement I could read.
Alben, Madden & Lauder 2007 measured a cantilever stiffness of **1.98 N m⁻¹** on bluegill pectoral rays of
**40.3 ± 0.8 mm**. That is the same species, the same fin and the same lab. Those authors also give an
order-of-magnitude **EI ≈ 10⁻⁶–10⁻⁵ N m²** (quoted, full-text via a page summarizer).

From the measured stiffness, the back-calculated EI is **5.4 × 10⁻⁶ to 4.3 × 10⁻⁵ N m²** with both bases clamped,
depending on the assumed load point (calculated). 3.8e-6 sits inside the measured envelope. 565e-6 sits
**13–105× above it**. Matching it would need a composite modulus of 56.5 GPa at Alben's I, or rays about 104 mm
long (calculated).

I still could not read the Flammang 2013 body text, so *why* the abstract prints 565e-6 remains **unknown**.

## 1. Which input is the answer most sensitive to? (calculated, recomputed, not asserted)

I perturbed each input of S25's conclusion by a factor of 2.

| Input | ×2 perturbation | Effect on the S25 conclusion |
|---|---|---|
| Either relayed value (the ratio test for a unit slip) | The ratio 148.7 becomes 74.3 or 297.4. Their log₁₀ values are 1.87 and 2.47, so neither is a power of ten. | None. The "not a unit conversion" finding is robust. |
| Composite modulus E | EI ×2 | Not decisive. A gap of 149× needs a factor of 149 in E. Bone-like E spans about 10⁸–10¹⁰ Pa, so E alone could reach that only by sitting at opposite ends of the range. |
| **Ray diameter d (or second moment I)** | **EI ×16** | **Decisive.** At E = 1 GPa, the diameter that gives 565e-6 is 1.84 mm. Halve it to 0.92 mm and EI = 3.5e-5, which is 9.3× A. Across Puri's quoted bluegill d = 1–2 mm at E = 1 GPa, a solid rod gives 4.9e-5 to 7.9e-4 N m². That range brackets **565e-6, not 3.8e-6**. So with a 1–2 mm solid rod as the geometry, B looks plausible. With a sub-millimetre effective section, A looks plausible. |
| Hemitrich (hollow) section instead of a solid rod | Alben 2007: the bony segments are about 30% of the thickness. A two-layer rectangle idealisation gives I_bony/I_solid = 0.657. | Modest. It cannot bridge 149× on its own. |

**So the most sensitive input is the ray's effective bending section, d or I.** The only number S25 and its
challengers had for it is Puri et al.'s "diameter of bluegill rays of 1–2 mm". That is a passing remark in a
zebrafish paper, and it gives no source or method.

## 2. How well established was that input?

| Input as used | Source | Read-level | Status |
|---|---|---|---|
| Bluegill ray d = 1–2 mm | Puri et al. 2018 *J Exp Biol* 221:jeb171777, PMC5868929: "Given the diameter of bluegill rays of 1–2 mm compared with 0.1–0.2 mm for zebrafish…" | full-text (Europe PMC fullTextXML, re-read this session) | **Proxy, unsourced in the text.** No citation, measurement method, ray number or fish size is given. It is an outer diameter. It is not the bending section of a paired-hemitrich ray. |
| Solid circular rod | S25 §3b, challenge-73, challenge-160 | (model) | **Assumption.** It has been repeated across three documents until it reads like a measurement. |
| E ≈ 1–10 GPa | S25 §3b ("one search summary", source unnamed) | search-summary | **Unsourced bracket.** |

Evidence level of the input before this pass: **assumption/proxy**, not measured.

## 3. Improving it: the primary measurement

**Flammang 2013 full text.** Could-not-access. WebFetch on `web.njit.edu` and `sites.harvard.edu` failed with
"host not resolvable in this session". curl through the proxy returned CONNECT 403 for `web.njit.edu`,
`public.websites.umich.edu`, `web.archive.org`, `api.openalex.org` and `api.semanticscholar.org`. Europe PMC
lists no PMC copy. These are network-policy failures, not evidence about the paper.

**Alben, Madden & Lauder 2007**, "The mechanics of active fin-shape control in ray-finned fishes", *J R Soc
Interface* 4:243–256, doi:10.1098/rsif.2006.0181, PMC2359861.

Read-level: **full-text, via an automated page summarizer** (WebFetch of `pmc.ncbi.nlm.nih.gov/articles/PMC2359861/`).
The Europe PMC fullTextXML endpoint returned HTTP 500 three times. NCBI efetch returned the abstract only, and the
record is not open access. The summarizer drops superscripts, so I am reconstructing the exponents, for example
"108–109" read as 10⁸–10⁹. That reading is consistent with the units and with each other value below.

Quoted, as returned:

- "Six fishes with fins of similar size (maximum ray length =40.3±0.8 mm, mean±s.e.)"; "24 separate rays";
  "ray 4 out of 13 in the pectoral fin of a bluegill sunfish".
- "The cantilevered ray was deflected by applying a point force about two-thirds of the way along the ray."
- "the force–displacement curve may be fit with a slope of 1.98 N m−1, about 12 times the value when one
  hemitrich is free."
- Composite "E≈10⁸–10⁹ N m−2"; "I≈10⁻⁶ cm⁴"; "B=EI≈10⁻⁶–10⁻⁵ J m" (J m = N m²); "From axial CT scans, we
  estimate that the bony segments take up about 30% of this thickness."

Why this is a better input than d = 1–2 mm:

1. It is a **force–displacement measurement**, so it bypasses d, I and E. Those enter only through the beam
   idealisation.
2. It uses the **same species and fin**, in the **same lab**. Alben, Madden and Lauder are all co-authors of
   Flammang 2013.
3. The authors' own I ≈ 10⁻¹⁴ m⁴ corresponds to a solid-equivalent diameter of **0.67 mm** (calculated). That is
   below Puri's 1–2 mm, as you would expect once the soft core and the two-layer construction are counted.

**Recomputation from the measured stiffness** (calculated). I treat the ray as a uniform cantilever with
k = 3EI/a³. The load point a is the least certain step, so I bracket it.

| Load point a | EI, both bases clamped | EI, one hemitrich free (÷12) | 565e-6 ÷ clamped | 3.8e-6 ÷ clamped |
|---|---|---|---|---|
| L/2 | 5.4e-6 | 4.5e-7 | 105× | 0.70× |
| **2L/3 (as quoted)** | **1.28e-5** | **1.07e-6** | **44×** | 0.30× |
| L | 4.3e-5 | 3.6e-6 | 13× | 0.09× |

The 2L/3 row reproduces challenge-134's 1.28e-5 and 1.07e-6. I derived it independently.

Other ways in (calculated):

- At Alben's I ≈ 10⁻¹⁴ m⁴, 565e-6 needs E = **56.5 GPa**. That is far above Alben's composite 10⁸–10⁹ Pa, and above
  the stiffest cortical bone I know of; I did not source that last comparison here.
- At the same I, 3.8e-6 needs E = **0.38 GPa**, which is inside Alben's range.
- For 565e-6 to be a clamped bluegill ray under isometric L⁴ scaling, the ray would have to be about
  **104 mm** long, 2.6× Alben's rays.
- Puri's zebrafish check, redone: 3.8e-6 gives 6.1–6.8e-9 N m² per fin, and 565e-6 gives 0.9–1.0e-6 N m².
  Puri measured "1.5×10⁻⁹–4×10⁻⁹ N m²" (quoted, full-text). Only A is within an order of magnitude.

Caveats on the improved input. These are my inferences, and each would move the numbers:

- Base compliance in a cantilever test makes the apparent k *lower* than the beam's true EI implies, so the
  true EI could be higher. A 13–105× compliance error is not plausible for a clamped test, but I have no measured
  value for it: **unknown**.
- Flammang 2013's fish size, ray number and method are **unknown**. If they used much larger bluegill, or computed
  EI for something other than a single ray (for example a whole fin, or per unit width), then 565e-6 and Alben's
  measurement are not the same quantity, and both can be right.
- One possibility is an abstract-level slip, for example 5.65 × 10⁻⁶ printed as 565 × 10⁻⁶. That would put the
  value inside Alben's envelope. **This is pure hypothesis.** I found no text that supports it, and I do not
  adopt it.

Scope of negative searches this session:

- Europe PMC `"565" AND "Flammang"`: 9 hits, none of them a fin-mechanics paper other than Flammang 2013 itself.
- Europe PMC `"fin ray" AND bluegill AND "flexural stiffness"`: 4 hits. Of these, PMC11424826 was read at full
  text and has no Flammang stiffness number. PMC5410822 had no full text available (the request returned an empty
  record). PMC3257170 was not read.
- Europe PMC `(REF:"23720195") AND "N m"`: 1 hit, Puri 2018.
- No source anywhere repeats 565e-6 outside the abstract itself.

## 4. Recompute the original conclusion

| Claim of S25 | Status with improved input |
|---|---|
| The Flammang 2013 abstract prints 565 × 10⁻⁶ N m², "calculated" | **Stands.** Textual fact at abstract level. (Challenge-160 noted that Europe PMC mirrors PubMed, so this is one abstract seen twice.) |
| 148.7 is not a power-of-ten unit slip | **Stands.** Robust to ×2 in either value (§1). |
| 3.8e-6 is untraced and should be treated as a misattribution | **Falls.** It is traced (Puri 2018, full-text). It is physically consistent with the measured stiffness of bluegill pectoral rays from the same lab. |
| 565e-6 is the relaying to carry as "the" bluegill pectoral ray EI | **Falls.** It is 13–105× above the measured clamped stiffness of 40 mm bluegill pectoral rays (calculated from Alben 2007's measured 1.98 N m⁻¹). It is 56–565× above those authors' own stated EI ≈ 10⁻⁶–10⁻⁵ N m². |

**Corrected statement.** 565e-6 N m² is what the Flammang 2013 abstract prints, but it should not be used as a
single bluegill pectoral ray's EI without the full text. Measured ray mechanics from the same lab put a 40 mm
bluegill pectoral ray at about 10⁻⁶–10⁻⁵ N m² (order 10⁻⁶ with one hemitrich free, order 10⁻⁵ with both clamped).
The Puri relay of 3.8e-6 is consistent with that range. Whether Flammang's body text prints 3.8e-6 is still
**unknown**.

Consequence for S6/S26 (inference, not re-run here): challenge-73 found that both values fail S6's δ/L ≤ 0.10
criterion. 565e-6 was the one that failed only marginally. If that value is discounted, the passive-ray fail
becomes **robust** (more than 10× short) rather than indeterminate.

## 5. What measurement would settle it

1. **Read Flammang 2013's Methods and Results.** This costs nothing: allow `web.njit.edu`,
   `public.websites.umich.edu` or `sites.harvard.edu` in this environment's network settings. It answers whether
   the body contains 3.8e-6, which fish and ray were used, and how 565e-6 was "calculated".
2. **Measure it directly.** Three-point bending or cantilever tests on excised bluegill pectoral rays 3–5, with
   µCT cross-sections to get I independently, so that E·I and the force–displacement EI can be cross-checked. This
   needs a standard micro-mechanical tester and a µCT scan. I have no cost figure: **unknown**.

## Sources

| Source | Read-level |
|---|---|
| Flammang BE, Alben S, Madden PGA, Lauder GV 2013, *J Morphol* 274:1044–1059, doi:10.1002/jmor.20161, PMID 23720195 | abstract (via parent S25 and challenge-160); body text **could-not-access** (network policy, this session) |
| Alben S, Madden PG, Lauder GV 2007, *J R Soc Interface* 4:243–256, doi:10.1098/rsif.2006.0181, PMC2359861 | full-text via automated page summarizer (exponents reconstructed); Europe PMC XML HTTP 500; NCBI efetch abstract only |
| Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM 2018, *J Exp Biol* 221:jeb171777, PMC5868929 | full-text (Europe PMC fullTextXML, this session) |
| S25-organ.md, challenge-160.md, challenge-73.md, challenge-134.md (repository branches named above) | full-text |
| Europe PMC search listings (queries in §3) | listing |

```swarm-result
{"subproblem": "S25-D", "evidence": "literature", "answer": "The answer is most sensitive to the ray's bending section (EI scales as d^4), which rested on an unsourced 1-2 mm solid-rod proxy; replacing it with Alben et al. 2007's measured 1.98 N/m cantilever stiffness of 40.3 mm bluegill pectoral rays gives a calculated clamped EI of 5.4e-6 to 4.3e-5 N m^2 (authors state EI ~1e-6 to 1e-5), so 3.8e-6 is physically consistent and 565e-6 is 13-105x too stiff: 565e-6 stays the abstract's printed value but S25's conclusion that it is the relaying to trust and 3.8e-6 a misattribution falls.", "key_number": "bluegill pectoral ray EI 1.28e-5 N m^2 both bases clamped (range 5.4e-6 to 4.3e-5 over load point L/2 to L), 1.07e-6 N m^2 one hemitrich free; calculated from measured k = 1.98 N/m, L = 40.3 mm", "verdict": "falls", "depends_on": ["Flammang et al. 2013 abstract, PMID 23720195 (abstract read-level): 565 x 10^-6 Nm2, 'calculated'", "Flammang et al. 2013 full text: could-not-access (method, fish size, ray unknown)", "Puri et al. 2018 J Exp Biol 221:jeb171777, PMC5868929 (full-text): 3.8e-6 N m^2 for bluegill rays citing Flammang 2013; bluegill ray diameter 1-2 mm (unsourced); zebrafish caudal fin 1.5e-9 to 4e-9 N m^2", "Alben, Madden & Lauder 2007 J R Soc Interface 4:243, PMC2359861 (full-text via summarizer, exponents reconstructed): k = 1.98 N/m both hemitrichs clamped, ~12x one-free, max ray length 40.3 +/- 0.8 mm, load ~2/3 L, E ~1e8-1e9 Pa, I ~1e-6 cm^4, EI ~1e-6 to 1e-5 N m^2, bony segments ~30% of thickness", "Euler-Bernoulli uniform cantilever model k = 3EI/a^3, load point bracketed L/2 to L", "Assumption: cantilever base compliance does not inflate the EI gap by 13-105x (unmeasured)", "Assumption: Flammang 2013's 565e-6 refers to a single pectoral ray of comparable size to Alben's 40 mm rays (unverified)", "Isometric L^4 scaling (used only for the 104 mm equivalent-length check)", "Solid circular rod and two-layer rectangle idealisations (used only in the sensitivity analysis)", "challenge-73 S6 scenario result that both values fail delta/L <= 0.10 (downstream consequence only)"]}
```
