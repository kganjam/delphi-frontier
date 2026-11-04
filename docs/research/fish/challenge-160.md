# Challenge 160: adversarial review of [S25], Flammang et al. 2013 fin-ray flexural stiffness

**Claim under review (verbatim):** "[S25] Flammang et al. 2013 report 565e-6 N m^2 in their abstract (read at abstract level in Europe PMC and PubMed; the authors call it 'calculated'); 3.8e-6 N m^2 is not in the abstract, could not be traced to any source, and is not a power-of-ten unit conversion of 565e-6 (ratio 148.7), but the full text, and with it the method, specimen and ray region, could not be read. KEY: 565e-6 N m^2 (5.65e-4 N m^2), bluegill pectoral fin ray, abstract-level"

Recorded evidence level: literature. Source: harvest:s25-flammang-fin-ray-stiffness-gkwnb4

**Verdict: WEAKENED.** The claim reads the abstract correctly. But its statement that 3.8e-6 N m^2 "could not be traced to any source" is false. The value appears in a peer-reviewed open-access paper, which attributes it to bluegill rays and places it in a sentence that cites Flammang et al. 2013. The two values therefore disagree inside the literature. They should be recorded as two conflicting reports, not as one real value and one stray number.

## Sources and read levels

| # | Source | Read level | How |
|---|--------|-----------|-----|
| A | Flammang BE, Alben S, Madden PGA, Lauder GV (2013). Functional morphology of the fin rays of teleost fishes. *J Morphol* 274(9):1044–1059. doi:10.1002/jmor.20161, PMID 23720195 | **abstract** | Europe PMC REST API, `resultType=core`. I read the abstract text myself. |
| A-full | The same paper, full text | **could-not-access** | Tried web.njit.edu (author PDF), public.websites.umich.edu (Alben PDF) and researchgate. The network policy blocked each one (DNS failure or proxy 403). The paper has no PMCID, so Europe PMC has no full text. pubmed.ncbi.nlm.nih.gov was also blocked, so **I did not re-check PubMed**, though the claim says it did. |
| B | Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018). In vivo quantification of mechanical properties of caudal fins in adult zebrafish. *J Exp Biol* 221: jeb171777. doi:10.1242/jeb.171777, PMC5868929 | **full-text** | Europe PMC `fullTextXML`. I read the relevant passages myself. |
| C | Esposito CJ, Tangorra JL, Flammang BE, Lauder GV (2012). A robotic fish caudal fin. *J Exp Biol* 215:56–67. PMID 22162853 | **abstract** | Europe PMC. The full-text PDF host (sites.harvard.edu) was blocked. |
| D | Aiello BR et al. (2018). The relationship between pectoral fin ray stiffness and swimming behavior in Labridae. *J Exp Biol* 221: jeb163360. PMID 29162638 | **abstract** | Europe PMC. |
| E | Alben S, Madden PGA, Lauder GV (2007). The mechanics of active fin-shape control in ray-finned fishes. *J R Soc Interface* | **could-not-access** | Host blocked. It reports three-point bending of bluegill rays (search-summary only), so it is the most likely independent check, but I could not read it. |

## 1. Arithmetic, redone independently

- The abstract (source A, my own read) says: "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2." That equals 5.65 × 10⁻⁴ N m². The claim's KEY value is correct, and so is its note that the authors call it "calculated".
- 565e-6 / 3.8e-6 = **148.68**. The claim's ratio of 148.7 is correct. The nearest powers of ten are 100 and 1000, so the gap is not a unit or prefix conversion, as the claim says. Note that 1 N mm² = 10⁻⁶ N m², so "565 × 10⁻⁶ N m²" could also be read as "565 N mm²". That changes nothing here.
- **My inference, not the authors':** I checked whether a solid circular bone rod could produce each value. I used the bluegill ray diameter of 1–2 mm given in source B and I = πd⁴/64.
  - For EI = 565e-6 N m², the implied E is 11.5 GPa at d = 1 mm, 2.3 GPa at 1.5 mm and 0.72 GPa at 2 mm.
  - For EI = 3.8e-6 N m², the implied E is 77 MPa at 1 mm, 15 MPa at 1.5 mm and 4.8 MPa at 2 mm.
  - The 565e-6 value implies a modulus in the range expected for bone. The 3.8e-6 value implies a material softer than bone by two to three orders of magnitude.
  - Real rays are paired hemitrichia, distally segmented and not solid, so the effective EI should fall *below* the solid-rod value. That makes a low measured value less surprising than this test suggests. **This test cannot decide which value is right.** It only shows that neither value is ruled out by physics.

## 2. The "untraceable" 3.8e-6 N m² does have a source (the defect)

Puri et al. 2018 (source B, full text), Conclusions section, verbatim:

> "Previous measurements of bending stiffness of larger fish have reached a sensitivity of 10 −6 N m 2 (Flammang et al., 2013), which in that case was sufficient because of the larger dimensions of the fins and rays of bluegill sunfish. … As there are 16–18 rays making up the entire zebrafish fin, the bending stiffness of bluegill rays of 3.8×10 −6 N m 2 would indicate a bending stiffness for a zebrafish fin of between 2×10 −9 and 5×10 −9 N m 2"

- **Puri's claim:** bluegill rays have a bending stiffness of 3.8×10⁻⁶ N m². In the same paragraph, the only bluegill source cited is Flammang et al. 2013. The sentence that gives the number does not itself carry a citation.
- **My inference:** 3.8e-6 is most likely Puri's reading of Flammang 2013's full text. That would mean the full text reports a value different from the abstract's 565e-6. It could be a different ray region, such as the distal segmented portion, a different method, or a different specimen. It is also possible that Puri made a transcription or derivation error. I cannot tell which without the Flammang full text, so this point is **unknown**.
- **Side check, my arithmetic:** I tried to reproduce Puri's step from bluegill to zebrafish. With a diameter ratio of 1/10 (d⁴ factor 10⁻⁴) and 16–18 rays, 3.8e-6 gives 6.1–6.8 × 10⁻⁹ N m², not the 2–5 × 10⁻⁹ they state. Puri's working is not fully shown, so their 3.8e-6 may come from a non-obvious derivation. It should be treated as a **secondary citation**, not a measurement.
- Puri's search scope: I found it with a Europe PMC citation search (`CITES:23720195_MED`, 31 citing records, 5 with PMC full text). I did not search for the 3.8e-6 value in the non-open-access citing papers.

## 3. Is a proxy standing in for the quantity that matters?

Yes. Flammang's 565e-6 is described as *calculated*. A search snippet (not read by me) describes it as coming from the deflection of the fin ray under a vortex perturbation, not from a direct bending test. The abstract reports a 67 mN impact force and a maximum local curvature of 9.38 mm⁻¹, but it gives no lever arm or loading geometry. **I could not rederive EI from the abstract's inputs.**

The direct quantity would be the cantilever or three-point-bending EI of an excised ray at a stated region. Source E (Alben et al. 2007) reportedly measured that for bluegill, but I could not read it. Source C says the robotic rays were made "150 to 2000 times the stiffness of biological fin rays," but its abstract gives no absolute biological value.

## 4. Hidden assumption

The KEY value is labelled "bluegill pectoral fin ray", as if it were a single property of the ray. The abstract itself says the proximal 40% of the ray is unsegmented and the distal 60% is segmented, with different curvature ceilings (0.029 vs 0.065 mm⁻¹). Labrid three-point-bending data (source D, abstract) show "flexural stiffness decreased exponentially along the proximodistal span." So a single EI per ray is not a safe assumption.

If that assumption is dropped, 565e-6 and 3.8e-6 could both be correct for different regions. **This is a hypothesis, not a finding.** That possibility is another reason not to dismiss 3.8e-6.

## 5. Comparison with another taxon

Aiello et al. 2018 (labrids *Gomphosus varius* and *Halichoeres bivittatus*, measured by three-point bending, abstract) report 0.0001–1.5109 µN m², which is 1 × 10⁻¹⁰ to 1.51 × 10⁻⁶ N m².

- Bluegill 565e-6 is about **374×** the labrid maximum.
- Bluegill 3.8e-6 is about **2.5×** the labrid maximum.

The species, fish sizes and methods differ, so this does not refute 565e-6. Still, measured data on fin rays of similar build sit much closer to 3.8e-6, so the larger value should be treated with caution.

## 6. Evidence level

- The claim's own level ("literature", abstract-level) is honest. It correctly says the value is calculated and does not present it as measured.
- One gap: the claim says it read PubMed. I could not reach PubMed to confirm that, but Europe PMC carries the same abstract text.
- The defect is in the **negative search**. "could not be traced to any source" was stated without saying where the author searched. A citation search of open-access papers that cite Flammang 2013 finds the source.

## What should change

- Keep the KEY value: 565 × 10⁻⁶ N m², from the Flammang et al. 2013 abstract, described there as *calculated*, read at abstract level.
- Replace "could not be traced to any source" with: "3.8 × 10⁻⁶ N m² is stated for bluegill rays in Puri et al. 2018 (JEB 221:jeb171777, full text), in a paragraph citing Flammang et al. 2013. It is a secondary citation, 149× below the abstract value, and unreconciled. The method, region and specimen behind each value are unknown until the Flammang full text is read."
- Keep both values. Do not average them.

```swarm-challenge
{"claim_id": 160, "outcome": "weakened", "reason": "The 565e-6 N m^2 abstract reading holds, but the claim that 3.8e-6 N m^2 'could not be traced to any source' is false: Puri et al. 2018 (J Exp Biol 221:jeb171777, PMC5868929, full text) states 'the bending stiffness of bluegill rays of 3.8x10^-6 N m^2' in a paragraph citing Flammang et al. 2013, so the two values are an unreconciled disagreement in the literature.",
  "corrected_value": null,
  "depends_on": ["Flammang et al. 2013 J Morphol 274:1044 abstract via Europe PMC (abstract-level): 'calculated to be 565 x 10(-6) Nm2'", "Puri et al. 2018 J Exp Biol 221:jeb171777 PMC5868929 full text: 'bending stiffness of bluegill rays of 3.8x10^-6 N m^2' with Flammang et al. 2013 cited in same paragraph", "Aiello et al. 2018 J Exp Biol 221:jeb163360 abstract: labrid fin ray EI 0.0001-1.5109 uN m^2 (context only)"]}
```
