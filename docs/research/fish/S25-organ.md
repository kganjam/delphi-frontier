# S25 (organ): Flammang 2013 fin-ray flexural stiffness, 3.8e-6 or 565e-6 N m²?

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.

**Short answer.** The paper's abstract, read in two independent indexes, prints **565 × 10⁻⁶ N m²**
(= 5.65 × 10⁻⁴ N m²) and calls it *calculated*. I found **3.8 × 10⁻⁶ N m²** in no copy of Flammang
et al. 2013 that I could read. I could **not** read the full text: every host carrying a PDF
refused the connection from this session. So the method, the specimen and how "calculated" was
done are still unknown, and the question as posed ("read the primary paper at full text") is
**not settled**. Evidence level: `literature`, at abstract read-level.

---

## 1. The question, restated

Flammang, Alben, Madden & Lauder (2013), "Functional morphology of the fin rays of teleost
fishes", *J. Morphol.* 274(9):1044–1059, doi:10.1002/jmor.20161, PMID 23720195.

The project quotes two values for the flexural stiffness (EI) of one bluegill (*Lepomis
macrochirus*) pectoral fin ray, both attributed to this paper:

| Relayed value | In N m² |
|---|---|
| A | 3.8 × 10⁻⁶ |
| B | 565 × 10⁻⁶ = 5.65 × 10⁻⁴ |

The ratio B/A is 148.7, which is 10^2.17 (computed in §3). The two values cannot both be the
paper's number. The brief says the S6 verdict flips between them. I did not have S6's text and
cannot say at what threshold it flips. A search of this repository (`grep` for
"Flammang", "565", "3.8e-6" in every `*.md`) found no S6 document and no earlier use of either value.

## 2. What is measured, or reported

| # | Value | Source | Year | Read-level | What the source says |
|---|---|---|---|---|---|
| 1 | **565 × 10(-6) Nm2** | Flammang et al., abstract, via Europe PMC REST API (`DOI:10.1002/jmor.20161`, resultType=core) | 2013 | **abstract** | "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2." |
| 2 | **565 × 10(-6) Nm2** | Same abstract, via NCBI E-utilities efetch (PubMed 23720195, text) | 2013 | **abstract** | Identical wording. This is a second, independent index of the same abstract. |
| 3 | 67 ± 2.3 mN (s.e.), force at vortex impact; vortex jet ≈ 1 m s⁻¹ | Same abstract | 2013 | abstract | Perturbation experiment on a live bluegill fin |
| 4 | max curvature 9.38 mm⁻¹ under the vortex perturbation | Same abstract | 2013 | abstract | — |
| 5 | curvature ≤ 0.029 mm⁻¹ proximal (unsegmented), ≤ 0.065 mm⁻¹ distal (segmented), normal swimming | Same abstract | 2013 | abstract | — |
| 6 | distal 60% of the ray is segmented | Same abstract | 2013 | abstract | — |
| 7 | 565 × 10⁻⁶ N m² | Web-search engine summaries of the Harvard, NJIT and UMich PDF copies | — | **search-summary** | They repeat the abstract figure. One summary says the paper compares the value to "highly flexible segmented fin rays from other species". I could not check that against the text. |
| 8 | 3.8 × 10⁻⁶ N m² | — | — | **could-not-find** | Not in either abstract copy. Two web searches (standard and extended), one aimed at "3.8" "10-6" with bluegill fin-ray terms, returned no source giving this value for this paper or for any bluegill ray. |

**Who says "calculated".** The authors' own word is "calculated", not "measured". From the
abstract alone I cannot tell whether EI came from E × I with a material modulus and ray geometry,
or from the force–curvature data of the perturbation experiment. That is my reading of what the
abstract leaves open, not a claim by the authors.

**Full-text attempts, all failed (could-not-access):**

| Host / route | Result |
|---|---|
| sites.harvard.edu (Lauder lab PDF) | proxy CONNECT 403; WebFetch: host not resolvable in this session |
| web.njit.edu/~flammang (author PDF) | CONNECT 403; WebFetch not resolvable |
| public.websites.umich.edu/~alben (co-author PDF) | CONNECT 403; WebFetch not resolvable |
| deepblue.lib.umich.edu (repository) | CONNECT 403; WebFetch not resolvable |
| onlinelibrary.wiley.com (publisher) | Cloudflare challenge page, no content |
| Europe PMC full text | not open access ("Subscription required") |
| Unpaywall, Semantic Scholar, scholar.archive.org, core.ac.uk | CONNECT 403 |
| Related papers that might print a bluegill EI table: Lauder et al. 2011 *Smart Mater. Struct.* (Harvard wpmucdn PDF); Tangorra et al. 2010 *JEB* | 403 on both |

These failures come from the session's network policy. They say nothing about whether the
paper is available.

## 3. What I computed (computation, not observation)

**3a. Is A a unit slip of B?** 565e-6 / 3.8e-6 = **148.7** (log₁₀ = 2.17). Unit mistakes
between N m², N mm² and N cm² move a value by an exact power of ten (10², 10⁴, 10⁶...). 148.7 is
not a power of ten, so A is **not** a plain unit conversion of B. A transcription error that
changes the digits too (for example, a value taken from a different row or paper) is not ruled
out. This is arithmetic. It does not show where A came from.

**3b. Geometric plausibility.** For a solid circular rod, I = πd⁴/64 and EI = E·I. Fin-ray bone
moduli in the literature are around 1–10 GPa. One search summary gave 3.67–8.40 GPa, mean
6.48 GPa, but did not say which study it came from, so I use it only as a bracket. The diameters
each EI would need:

| EI (N m²) | E = 1 GPa | E = 6.48 GPa | E = 10 GPa |
|---|---|---|---|
| 5.65 × 10⁻⁴ (B) | d = 1.84 mm | 1.15 mm | 1.04 mm |
| 3.8 × 10⁻⁶ (A) | d = 0.53 mm | 0.33 mm | 0.30 mm |

Assumptions: a solid, uniform, circular section. Real lepidotrichia are paired hemitrichia
around a soft core, so the real I is below the solid-rod value for the same outer diameter. Under
this model, B needs a ≈1–2 mm solid bony rod. A needs ≈0.3–0.5 mm. I did not get bluegill ray
diameters from any source I could read, so this table **does not choose** between A and B. It
only says what each value implies about the ray.

**3c. Can B be rebuilt from the abstract's force and curvature?** Using M = EI·κ with
EI = 5.65 × 10⁻⁴ N m²:

- κ = 9.38 mm⁻¹ = 9380 m⁻¹ gives M = 5.30 N m. With F = 0.067 N, the lever arm would be 79 m,
  which is physically impossible.
- κ = 0.065 mm⁻¹ gives M = 0.037 N m and a 0.55 m lever. κ = 0.029 mm⁻¹ gives 0.016 N m and a
  0.24 m lever. Both levers are longer than a bluegill.

So B is **not** an Euler–Bernoulli EI back-calculated from the abstract's impact force and peak
curvature. That fits the abstract's own statement that the impact caused local **buckling**, which
simple beam theory does not cover. I infer that the paper computed EI by another route, most
likely from geometry and modulus, but that is a guess I could not check. Also, F/κ = 0.067 /
9380 = 7.1 × 10⁻⁶. That has the same order of magnitude as A but does not equal it, and F/κ is
not dimensionally EI (EI needs N m², F/κ gives N m). I record this only to say that I tried it
and it does **not** reproduce A.

## 4. The answer

**565 × 10⁻⁶ N m² is the value Flammang et al. 2013 print in their abstract.** This is the
authors' claim, read at abstract level in two independent indexes (Europe PMC, PubMed).
**3.8 × 10⁻⁶ N m² is not in the abstract.** I could not trace it to this paper or to any other
source. It is not a power-of-ten unit conversion of 565 × 10⁻⁶ (computed, §3a).

Evidence level: **`literature`** (abstract read-level). It is **not** `measured`: I did not read
the full text, and the authors call the value "calculated".

So the relay **"565e-6 N m², Flammang 2013" matches the paper's abstract**. The relay
**"3.8e-6 N m², Flammang 2013" has no support I could find and should be treated as a
misattribution until someone finds its source.**

## 5. What this does NOT establish

- **It does not give the method, specimen or units in the paper's own Methods.** The brief asked
  for these at full text. I did not get them. I do not know the fish's size, which ray (number
  and position), the sample size, whether EI is for the proximal unsegmented section, the distal
  segmented section or the whole ray, or which E and I were used.
- **It does not show that 565e-6 N m² is physically right**, only that the authors report it.
  §3b shows it needs a solid bony rod of about 1–2 mm under simple assumptions. That is at or above
  what I would expect for a bluegill pectoral ray, but I have no measured diameter to compare.
  An error in the paper itself (for example, a mis-scaled I) is **not** ruled out. Readers who
  doubt the number should check whether the full text's E and I multiply to 565e-6.
- **It does not identify where 3.8e-6 came from.** Possible sources I could not check: Lauder et
  al. 2011 (table of bluegill EI, E, I by ray and region), Alben, Madden & Lauder 2007, Tangorra
  et al. 2010, Taft & Taft (sculpin rays), Aiello et al. 2018 (labrids), or a per-segment or
  distal value inside Flammang 2013 itself. Any one of these could legitimately give a smaller EI
  for a different ray, region or species. A could be a **correct number with the wrong citation**,
  not a wrong number.
- **It does not settle the disagreement in the sense that matters for S6.** If the design needs
  the EI of a *distal, segmented* ray region, a value near 10⁻⁶ might be the more relevant one even
  if it is not Flammang's headline number. Fin-ray stiffness varies along the ray and between rays.
  One search summary (search-summary level) says Lauder et al. 2011 found stiffness falls from
  proximal to distal and varies by nearly two orders of magnitude across rays. A ~150× spread may
  partly be **real biological variation**, not an error.
- **Nothing here transfers to zebrafish.** Bluegill is a ~15–20 cm centrarchid. Danio rerio is
  4 cm. EI scales roughly as d⁴ (for fixed E), so if ray diameter scales with body length, a
  ~4–5× smaller zebrafish ray would be ~250–600× less stiff. That is a computation under an
  isometric-scaling assumption I have not tested. No zebrafish fin-ray EI was searched for in this
  subproblem.
- Scope of the negative search for 3.8e-6: two web-search queries plus the two abstract
  indexes. I did not search Google Scholar full text, and I did not read any paper on fin-ray
  mechanics in full.

## 6. What would change the answer

1. **Reading the full text of Flammang et al. 2013** (Methods and Results on flexural stiffness).
   This would confirm or correct 565e-6 and give the method, specimen and region. The quickest
   route is to add `web.njit.edu`, `public.websites.umich.edu` or `sites.harvard.edu` to this
   environment's allowed network domains. All three host author copies.
2. **Finding 3.8e-6 in a primary source** (most likely Lauder et al. 2011 Table 1, or a regional
   value inside Flammang 2013). That would turn A from "misattributed" into "correct number,
   different ray or region or paper", and would make the S6 question one of *which region's EI
   applies*, not *which relay is right*.
3. **Finding that the full text's E × I does not equal 565e-6** (for example, an I off by a power
   of ten). That would flip the answer: the published headline value would itself be in error.
4. For the project, **a direct zebrafish pectoral fin-ray EI measurement** (three-point bending or
   cantilever, with µCT cross-sections) would make this whole bluegill-to-zebrafish relay
   unnecessary.

---

Sources:
- Europe PMC record, doi:10.1002/jmor.20161 (abstract), `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1002/jmor.20161&format=json&resultType=core`. Read-level: abstract.
- PubMed 23720195 via NCBI efetch, `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=23720195&rettype=abstract&retmode=text`. Read-level: abstract.
- Author PDF copies (could-not-access): `https://web.njit.edu/~flammang/publications/Flammang.etal.2013.JMorph_finrays.pdf`, `https://public.websites.umich.edu/~alben/jmor20161.pdf`, `https://sites.harvard.edu/glauder/files/2022/03/Flammang.etal_.2013.JMorph_finrays.pdf`.

```swarm-result
{"subproblem": "S25", "evidence": "literature", "answer": "Flammang et al. 2013 report 565e-6 N m^2 in their abstract (read at abstract level in Europe PMC and PubMed; the authors call it 'calculated'); 3.8e-6 N m^2 is not in the abstract, could not be traced to any source, and is not a power-of-ten unit conversion of 565e-6 (ratio 148.7), but the full text, and with it the method, specimen and ray region, could not be read.", "key_number": "565e-6 N m^2 (5.65e-4 N m^2), bluegill pectoral fin ray, abstract-level", "blocked_on": "full text of Flammang et al. 2013 (doi:10.1002/jmor.20161): every PDF host (njit.edu, umich.edu, harvard.edu, Wiley) refused this session's network; also the source of the 3.8e-6 value"}
```
