# Challenge 205: the S9 claim on teleost fin-ray modulus

**Claim under review (author: harvest `s9-fin-ray-materials-t0royp`; recorded evidence level `literature`):**
> Teleost fin-ray (lepidotrichia) modulus is reported only from non-zebrafish bending tests (bluegill proximal mean 1.34 GPa, range 0.24-3.7; distal 0.11-0.67 GPa), bracketed by fish-bone values of 3.7-8.4 GPa (rib bending) to ~23-25 GPa (zebrafish vertebra nanoindentation); zebrafish fin-ray material modulus, fin-ray strength and density, and every actinotrichia property are unknown. KEY: 1.34 GPa.

**Verdict: WEAKENED.** The bluegill numbers hold up. The claim that nothing has been measured on zebrafish fin rays does not. A zebrafish fin-ray bending dataset exists, with an effective modulus derived from it, and so does a nanoindentation study of single zebrafish rays. The claim mentions neither.

## 1. Arithmetic and the cited values, checked independently

The claim contains no arithmetic to redo. I checked each number against a source instead.

| Claim value | What I found | Read level | Status |
|---|---|---|---|
| Bluegill proximal mean 1.34 GPa, range 0.24-3.7 | Lauder et al. 2011, *Smart Mater. Struct.* (Lauder, Madden, Tangorra, Anderson, Baker): "mean modulus for the proximal (basal) region … 1.34 GPa, but this varied from 0.24 to 3.7 GPa" | search-summary | Matches |
| Bluegill distal 0.11-0.67 GPa | Same paper: "moduli … varied from 0.11 to 0.67 GPa" | search-summary | Matches |
| Zebrafish vertebra ~23-25 GPa (nanoindentation) | Bohns et al. 2024 (Liverpool repository): control vertebrae 22.74 ± 1.60 GPa; alendronate-treated groups 25.68 ± 2.07 and 27.27 ± 1.59 GPa | search-summary | Roughly right. The untreated baseline is 22.7 GPa. The 25-27 GPa values come from drug-treated fish, so "~23-25" mixes two conditions. |
| Rib bending 3.7-8.4 GPa | Not located. One search found Cohen et al. 2012 (*JEB*, carp vs tilapia, cellular vs acellular bone: moduli "in the same range") and a 2020 *Materials* paper on rib three-point bending, but neither snippet gave these numbers. | search-summary | **unverified** (not refuted) |

The KEY value, 1.34 GPa (bluegill, not zebrafish), survives as stated.

## 2. Counter-example: zebrafish fin-ray mechanics have been measured

**Puri, Aegerter-Wilmsen, Jaźwińska & Aegerter 2018, *J. Exp. Biol.* 221: jeb171777, doi 10.1242/jeb.171777.** Read level: full text via PMC5868929, extracted by a fetch tool, so I saw quoted passages rather than reading every line. Fig. S5C was not read.
- They measured the bending stiffness of adult zebrafish caudal fins in vivo: "overall bending moments of 1.5×10⁻⁹–4×10⁻⁹ N m² along the proximal–distal axis". The paper writes "bending moments", but N m² are the units of bending stiffness (EI), and the Results treat the values that way.
- The authors conclude the rays dominate: the bending stiffness "predominantly relies on the mechanical properties of the rays". Removing the interray tissue did not noticeably change stiffness.
- They "calculated the effective Young's modulus by dividing the effective bending stiffness by" I_eff. The values appear only in Fig. S5C. **I did not obtain the number**, so it is `unknown` here. A secondary snippet (ResearchGate, could-not-access) attributes about 8 MPa (whole fin) and about 0.8 MPa to this line of work. I could not verify either figure and do not use them.
- They also report an interray tissue tensional modulus of 4 ± 2 kPa, which they call an upper bound.
- Their calibration values (steel 200 ± 10 GPa, polyimide 2.0-2.2 GPa) are instrument checks, not tissue values. One search summary listed a "198-209 GPa" figure next to fin work. That figure is the steel calibration, not a ray modulus.

**NTHU (National Tsing Hua University) thesis on nanoindentation and AFM-QNM of single regenerating zebrafish fin rays.** Read level: search-summary only. The host etd.lib.nthu.edu.tw did not resolve from this session.
- It reports that "reduced elastic modulus and hardness decline from the proximal to the distal regions of the single ray, and the center of ray was harder than the edge".
- This is a direct material-level (indentation) modulus measurement on zebrafish lepidotrichia. **Its absolute values are unknown to me.** I tried one fetch, which failed on DNS.

My inference: the phrase "reported only from non-zebrafish bending tests" is false as written. "Zebrafish fin-ray material modulus … unknown" holds only in the narrow sense that **I could not retrieve** a number. It does not hold in the sense that no measurement exists. The honest wording is "measured (Puri 2018 effective modulus; NTHU nanoindentation) but values not retrieved".

## 3. Proxy and hidden-assumption problems

1. **Effective modulus vs material modulus.** My inference: the bluegill 1.34 GPa is a beam-theory effective modulus. It is EI from bending divided by an assumed second moment of area for a bilaminar hemitrich ray, which is segmented distally and has a soft core between the hemitrichs. If the hemitrichs slide, or the cross-section is mis-specified, E moves a lot. The 0.24-3.7 GPa spread (about 15×) fits a structural value better than a material constant. If the second moment is relaxed to count only the mineralised hemitrich cortex, the inferred material E goes up. So 1.34 GPa is a lower-bound-type proxy for the mineral tissue's modulus, not that modulus itself.
2. **The bracket mixes methods.** My inference: whole-element bending moduli of a few GPa and nanoindentation tissue moduli of about 23 GPa are not on one axis. Indentation reads local, dry or near-dry tissue and usually comes out several-fold above the bending modulus of the same bone. "Bracketed by" implies one comparable scale, and there isn't one. Also, the top of the bluegill range (3.7 GPa) equals the bottom of the rib range (3.7 GPa), so the lower bracket bounds nothing.
3. **The sources disagree on bluegill ray stiffness.** Puri et al. cite a bluegill ray EI of 3.8×10⁻⁶ N m². Flammang et al. 2013 (*J. Morph.*, read level: search-summary) give 565×10⁻⁶ N m², about 150× higher. They probably describe different rays, positions or loading definitions. I am recording the disagreement, not averaging it. It means any modulus derived from EI depends heavily on the source.
4. **Taxon scope.** Other teleosts have measured fin-ray stiffness that the claim does not mention: yellow perch lepidotrichia (*J. Morph.*, doi 10.1002/jmor.20831; three-point bending; covers preservation effects), labrids (*JEB* 221: jeb163360), and shortnose gar (SICB abstract; gar is a non-teleost actinopterygian). All at search-summary/listing level. I did not get modulus values from them. Their existence weakens "only bluegill" as a picture of the field, but does not change the 1.34 GPa value.

## 4. Evidence level

`literature` is appropriate for the bluegill numbers. They are reported values, not my calculations, and the claim already says it read them at search-summary level. The defect is not mislabeling. It is that **a negative claim ("unknown", "only from non-zebrafish") was asserted without the search scope beside it**, and the search missed a directly relevant zebrafish paper in *JEB*.

## 5. What survives, what does not

- **Survives:** bluegill proximal mean 1.34 GPa (0.24-3.7), distal 0.11-0.67 GPa. The zebrafish vertebra nanoindentation value is about 23 GPa (control 22.74 GPa).
- **Weakened:** "reported only from non-zebrafish". Zebrafish in vivo fin EI of 1.5-4×10⁻⁹ N m² exists, with an effective modulus derived in Puri 2018 Fig. S5C (value not retrieved). A single-ray nanoindentation modulus exists in the NTHU thesis (values not retrieved).
- **Unverified:** rib 3.7-8.4 GPa.
- **Not tested:** zebrafish fin-ray strength and density, and actinotrichia properties. I ran no search on these, so I neither confirm nor refute "unknown".

## Search scope

- About 6 web searches, covering: zebrafish fin-ray modulus and bending; the bluegill 1.34 GPa source; Puri 2018 effective modulus; zebrafish hemiray nanoindentation; zebrafish vertebra nanoindentation; fish rib bending modulus.
- Fetches: PMC5868929 succeeded. cob.silverchair.com, etd.lib.nthu.edu.tw and researchgate.net failed DNS resolution in this session.
- The local repository holds no copy of the harvest `s9-fin-ray-materials-t0royp`. I could not compare against the author's working notes.

```swarm-challenge
{"claim_id": 205, "outcome": "weakened", "reason": "The bluegill 1.34 GPa (0.24-3.7) and distal 0.11-0.67 GPa values match Lauder et al. 2011, but 'reported only from non-zebrafish' is false: Puri et al. 2018 (JEB, jeb171777) measured zebrafish fin-ray-dominated bending stiffness in vivo (1.5-4e-9 N m^2) and derived an effective Young's modulus (Fig. S5C, value not retrieved), an NTHU thesis reports nanoindentation moduli of single zebrafish rays (values not retrieved), and the GPa 'bracket' mixes beam-theory effective moduli with nanoindentation tissue moduli.", "corrected_value": null, "depends_on": ["Lauder et al. 2011 Smart Mater. Struct. bluegill fin-ray modulus 1.34 GPa (0.24-3.7) proximal, 0.11-0.67 GPa distal [search-summary]", "Puri et al. 2018 J Exp Biol 221:jeb171777, PMC5868929: in vivo zebrafish caudal fin EI 1.5-4e-9 N m^2, rays dominate, effective Young's modulus computed in Fig. S5C [full-text via fetch extraction; Fig. S5C not read]", "NTHU thesis: nanoindentation/AFM-QNM reduced modulus of single zebrafish fin rays declines proximal-to-distal [search-summary]", "Bohns et al. 2024 zebrafish vertebra nanoindentation control 22.74 +/- 1.60 GPa [search-summary]", "Flammang et al. 2013 J Morph bluegill ray EI 565e-6 N m^2 vs Puri-cited 3.8e-6 N m^2 [search-summary]"]}
```
