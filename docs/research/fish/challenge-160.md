# Challenge 160: S25, the Flammang 2013 fin-ray flexural stiffness

Claim under review (harvest `s25-flammang-fin-ray-stiffness-gkwnb4`, commit a7e70eb):

> Flammang et al. 2013 report 565e-6 N m² in their abstract (read at abstract level in Europe PMC
> and PubMed; the authors call it 'calculated'); 3.8e-6 N m² is not in the abstract, **could not
> be traced to any source**, and is not a power-of-ten unit conversion of 565e-6 (ratio 148.7), but
> the full text, and with it the method, specimen and ray region, could not be read.

The S25 document goes further. Its §4 says the 3.8e-6 relay "has no support I could find and
should be treated as a misattribution until someone finds its source."

**Verdict: WEAKENED.** The abstract value is right. But the claim that "3.8e-6 could not be traced
to any source" is false. A peer-reviewed paper that is open access in PMC prints 3.8 × 10⁻⁶ N m²
as the bending stiffness of bluegill rays and cites Flammang et al. 2013 for it. The
"misattribution" conclusion that S25 draws from the failed trace therefore loses its footing.

---

## 1. What I re-read (my reads, this session)

| # | Source | Read-level | What it says |
|---|---|---|---|
| 1 | Flammang, Alben, Madden & Lauder 2013, *J. Morphol.* 274:1044–1059, doi:10.1002/jmor.20161, PMID 23720195. Abstract via NCBI efetch | **abstract** | "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2." Pectoral fin rays of bluegill sunfish. Confirms the S25 quote word for word. |
| 2 | Same abstract via Europe PMC REST (`resultType=core`) | **abstract** | Same text. Europe PMC marks the paper `isOpenAccess: N` and lists full text as "Subscription required". |
| 3 | **Puri, Aegerter-Wilmsen, Jaźwińska & Aegerter 2018**, "In vivo quantification of mechanical properties of caudal fins in adult zebrafish", *J. Exp. Biol.* 221:jeb171777, doi:10.1242/jeb.171777, PMID 29246971, PMC5868929 | **full-text** (Europe PMC `fullTextXML`) | Conclusions: "Previous measurements of bending stiffness of larger fish have reached a sensitivity of 10⁻⁶ N m² (Flammang et al., 2013) … Given the diameter of bluegill rays of 1–2 mm compared with 0.1–0.2 mm for zebrafish … **the bending stiffness of bluegill rays of 3.8×10⁻⁶ N m²** would indicate a bending stiffness for a zebrafish fin of between 2×10⁻⁹ and 5×10⁻⁹ N m²". Introduction: single dissected rays were measured ex situ by "Videler, 1977; Alben et al., 2007; Flammang et al., 2013". |
| 4 | Full-text PDF of Flammang 2013 (njit.edu, umich.edu and harvard.edu author copies; Unpaywall; Semantic Scholar; OpenAlex) | **could-not-access** | Proxy CONNECT 403 on every host. The same failure S25 had. |

**How I found #3.** I listed the papers that cite PMID 23720195 in Europe PMC (31 citing records).
I resolved the PMCIDs of 18 of them; 3 had open-access full text (PMC12292994, PMC5868929,
PMC5454310). I searched those texts for "Flammang" near stiffness terms and for "N m 2". Only
PMC5868929 gives a number. A separate Europe PMC search, `"bending stiffness" AND bluegill AND
"3.8"`, returns this one paper and nothing else. S25 missed it because it searched for *flexural*
stiffness, while Puri et al. write *bending* stiffness.

## 2. Arithmetic, redone from the inputs

- 565e-6 / 3.8e-6 = **148.68**; log₁₀ = **2.172**. Not a power of ten. **S25 is correct.**
- Solid circular rod, d = (64·EI / (π·E))^¼. With E = 1 GPa: EI = 5.65e-4 gives d = **1.84 mm** and
  EI = 3.8e-6 gives d = **0.53 mm**. **S25 §3b is correct.** (Computation, not observation.)
- **Puri et al.'s scaling, redone by me.** A tenfold diameter ratio and EI ∝ d⁴ give a factor of
  10⁻⁴. Applied to 3.8e-6, that is 3.8e-10 N m² per ray. Summing 16–18 rays as parallel beams
  gives **6.1e-9 to 6.8e-9 N m²**. Puri et al. print 2–5e-9. Their range is somewhat lower than a
  plain ×10⁻⁴ gives, but it matches their phrase "more than four orders of magnitude". Applied
  instead to **565e-6**, the same chain gives **9.6e-7 to 1.0e-6 N m²**. That is about 250–700×
  above their measured whole-fin values of 1.5e-9 to 4e-9 N m². So **the 3.8e-6 is not a stray
  typo in Puri et al.** Their comparison only works with 3.8e-6 (my inference from their
  arithmetic, not their statement).

## 3. Attacks on the claim

**(a) "Could not be traced to any source." Broken.** Puri et al. 2018 is a traceable,
peer-reviewed, full-text source for 3.8 × 10⁻⁶ N m², attributed to Flammang et al. 2013 for
bluegill rays. That is the authors' claim. Whether Flammang 2013 actually prints 3.8e-6 anywhere
in its body is still **unknown**: Puri et al. is a secondary source, and I could not read the
primary full text.

**(b) Two sources now disagree, and I keep both.**
- The Flammang 2013 abstract (primary, abstract-level) gives **565 × 10⁻⁶ N m²**, "calculated".
- Puri et al. 2018 (secondary, full-text) give **3.8 × 10⁻⁶ N m²**, citing Flammang 2013. They
  also describe Flammang's work as *measurements* with "a sensitivity of 10⁻⁶ N m²".

My inference, not a finding: several explanations fit, and I cannot tell them apart without the
full text.
1. Flammang 2013 reports more than one EI. For example, a measured value for a ray or region near
   10⁻⁶ in the Results, and a calculated headline value in the abstract.
2. The abstract has a scaling or transcription error.
3. Puri et al. mis-transcribed the value.

Explanation 3 is the weakest, because their own scaling argument depends on 3.8e-6 (§2). The
"sensitivity of 10⁻⁶ N m²" phrase is also independent evidence that Puri et al. read numbers of
order 10⁻⁶ in Flammang's paper. **So S25's step from "untraced" to "treat as misattribution" is
not supported.** "Unresolved: abstract and a citing paper disagree" is the honest status.

**(c) Is the evidence level honest?** Mostly yes. S25 labels the value `literature`, at abstract
level, and keeps the authors' word "calculated". One overstatement: S25 calls Europe PMC and
PubMed "two independent indexes". Europe PMC takes MEDLINE records from PubMed, so the two copies
are one abstract seen twice, not independent confirmation. That does not change the number. It
does mean the 565e-6 rests on a single abstract text, and an abstract-level error (explanation 2)
is not ruled out by it.

**(d) Hidden assumption: the abstract represents the body.** This is the assumption the KEY
leans on. Relaxing it is exactly where Puri et al. bite. If the body's measured value is near
10⁻⁶ N m², then "565e-6 is Flammang's number" is true of the abstract but misleading as *the*
bluegill ray EI.

**(e) Proxy check.** The KEY reads "bluegill pectoral fin ray". The abstract is about pectoral
rays, so that part is supported. Puri et al. say "bluegill rays" and do not name the fin; their
whole-fin values are for the zebrafish *caudal* fin. Treating summed single-ray EI as whole-fin EI
is Puri et al.'s assumption. It ignores interray tissue and how the rays are coupled.

**(f) A regime S25 said it did not search.** S25 §5 says "No zebrafish fin-ray EI was searched
for." Puri et al. 2018 is a **direct in vivo measurement** in adult zebrafish: whole caudal fin
bending stiffness of **1.5 × 10⁻⁹ to 4 × 10⁻⁹ N m²** along the proximal–distal axis (their
abstract and full text). This is not part of the claim under review, but it bears on the project:
it is the "direct zebrafish measurement" that S25 §6 item 4 asks for, at the whole-fin rather than
the single-ray level.

## 4. What survives

- The abstract of Flammang et al. 2013 does print **565 × 10⁻⁶ N m²** and calls it "calculated".
  I re-read and confirmed this.
- 148.7 is not a power-of-ten unit factor. I recomputed and confirmed this.
- The method, specimen and ray region of either number are still **unknown**, because the full
  text was not readable here.

## 5. What would settle it

Read the Results of Flammang et al. 2013 at full text and see whether 3.8 × 10⁻⁶ N m² (or a value
near 10⁻⁶) appears, and for which ray or region. The author PDFs on web.njit.edu,
public.websites.umich.edu and sites.harvard.edu are blocked by this environment's network
policy.

## Sources

- Flammang BE, Alben S, Madden PGA, Lauder GV (2013) *J. Morphol.* 274:1044–1059.
  doi:10.1002/jmor.20161. Read-level: **abstract** (PubMed efetch; Europe PMC, which mirrors MEDLINE).
  Full text: **could-not-access**.
- Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018) *J. Exp. Biol.* 221:jeb171777.
  doi:10.1242/jeb.171777, PMC5868929. Read-level: **full-text** (Europe PMC fullTextXML).
- Europe PMC citations of PMID 23720195 (31 records). Read-level: **listing**. Of the 18 whose
  PMCIDs I resolved, the 3 open-access full texts were searched. The other 28 records were not read.

```swarm-challenge
{"claim_id": 160, "outcome": "weakened", "reason": "The 565e-6 N m^2 abstract value is confirmed, but 3.8e-6 N m^2 is traceable: Puri et al. 2018 J Exp Biol (PMC5868929, full text) print 'bending stiffness of bluegill rays of 3.8x10^-6 N m^2' citing Flammang et al. 2013 and their scaling only works with that value, so 'untraced/misattribution' is unsupported and the primary-vs-secondary disagreement stays open until the Flammang full text is read.", "corrected_value": null, "depends_on": ["Flammang et al. 2013 abstract, PMID 23720195 (abstract read-level): 565 x 10^-6 Nm2, 'calculated'", "Puri et al. 2018 J Exp Biol 221:jeb171777, PMC5868929 (full-text read-level): 3.8x10^-6 N m^2 for bluegill rays, attributed to Flammang et al. 2013", "Europe PMC citation listing of PMID 23720195 (listing read-level)", "Flammang et al. 2013 full text: could-not-access"]}
```
