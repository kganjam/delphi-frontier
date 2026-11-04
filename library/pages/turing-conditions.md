---
title: Turing's conditions for diffusion-driven instability, and when real tissue meets them
label: law-turing-conditions
---

:::{important}
**Descriptive** — this law describes a pattern and does not constrain a design.
:::

## The law

:::{math}
:label: eq-turing-conditions
\begin{aligned} &(1)\; f_u + g_v < 0 \qquad (2)\; \det J = f_u g_v - f_v g_u > 0 \\ &(3)\; D_v f_u + D_u g_v > 0 \qquad (4)\; (D_v f_u + D_u g_v)^2 > 4 D_u D_v \det J \\ &k_c^2 = \frac{D_v f_u + D_u g_v}{2 D_u D_v},\qquad \frac{D_v}{D_u} > d_c = \left(\frac{\sqrt{\det J} + \sqrt{-f_v g_u}}{f_u}\right)^{2},\qquad \lambda_c\big|_{\text{onset}} = 2\pi\left(\frac{D_u D_v}{\det J}\right)^{1/4} \end{aligned}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `lambda_c` | L | m | critical (first-unstable) pattern wavelength at the onset of instability, where condition (4) holds with equality |
| `D_u` | L^2/T | m^2/s | effective diffusivity of the activator u (the species with f_u > 0) |
| `D_v` | L^2/T | m^2/s | effective diffusivity of the inhibitor v |
| `f_u` | 1/T | 1/s | partial derivative of the u reaction rate with respect to u, at the homogeneous steady state (self-activation) |
| `f_v` | 1/T | 1/s | partial derivative of the u reaction rate with respect to v (inhibition of u by v when negative) |
| `g_u` | 1/T | 1/s | partial derivative of the v reaction rate with respect to u |
| `g_v` | 1/T | 1/s | partial derivative of the v reaction rate with respect to v (self-decay of the inhibitor when negative) |
| `det_J` | 1/T^2 | 1/s^2 | determinant of the reaction Jacobian, f_u*g_v - f_v*g_u |
| `d_c` | 1 | dimensionless | critical diffusivity ratio D_v/D_u that must be exceeded for instability |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `D_eff_cyclops_zebrafish` | 0.7 (interval 0.5 to 0.9) um^2/s | Observation (FRAP, Cyclops-GFP in the zebrafish blastula), Müller et al. 2012. The interval is the reported value +/- 0.2 (paper's error), not a confidence interval we computed. |
| `D_eff_squint_zebrafish` | 3.2 (interval 2.7 to 3.7) um^2/s | Observation (FRAP, Squint-GFP), Müller et al. 2012; interval is the reported +/- 0.5. |
| `D_eff_lefty1_zebrafish` | 11.1 (interval 10.5 to 11.7) um^2/s | Observation (FRAP, Lefty1-GFP), Müller et al. 2012; interval is the reported +/- 0.6. |
| `D_eff_lefty2_zebrafish` | 18.9 (interval 15.9 to 21.9) um^2/s | Observation (FRAP, Lefty2-GFP), Müller et al. 2012; interval is the reported +/- 3.0. |
| `clearance_rate_nodal_lefty` | unknown (interval 5.3e-05 to 0.000122) 1/s | Observation (Dendra2 photoconversion), Müller et al. 2012: Lefty1 0.53e-4, Lefty2 0.69e-4, Squint 1.00e-4, Cyclops 1.22e-4 per second. The authors give half-lives of 95-218 min; our arithmetic ln2/k reproduces that range (94.7-218 min). |
| `inhibitor_activator_diffusivity_ratio_measured` | about 14 (authors' normalised ratio); 3.5-27 (our ratios of the raw effective D values) dimensionless | Two different numbers from the same paper, recorded side by side and not reconciled. Müller et al. 2012 state the ratio of NORMALISED Lefty:Nodal diffusivities is approximately 14 and speak of a 5- to 15-fold ratio. Dividing the four raw effective D values pairwise (our calculation, not the authors') gives 3.5 (Lefty1/Squint) to 27 (Lefty2/Cyclops). This is a measured ratio of EFFECTIVE (hindered) diffusivities, not of free diffusivities; no FCS free-diffusion values are in that paper. |

## Why it holds

Turing (1952) showed that a homogeneous steady state that is STABLE without diffusion (conditions 1 and 2) can be destabilised BY diffusion if the two species diffuse at sufficiently different rates (conditions 3 and 4). Linearising the two-species system u_t = f(u,v) + D_u lap(u), v_t = g(u,v) + D_v lap(v) about the steady state and substituting modes exp(sigma t + i k x) gives a dispersion relation whose growth rate sigma(k) becomes positive in a finite band of wavenumbers once condition (4) holds; the first mode to go unstable has k_c^2 = (D_v f_u + D_u g_v)/(2 D_u D_v), and exactly at onset k_c^4 = det J/(D_u D_v), which is the equation checked above. Conditions (1) and (3) together force f_u and g_v to have opposite signs and require D_v/D_u > d_c > 1: the self-enhancing species must be the slower one ("local activation, long-range inhibition", Gierer & Meinhardt 1972). This is standard linear-stability algebra (derived here; matches the textbook form, e.g. Murray, Mathematical Biology). It is a statement about ONSET only: which pattern (spots, stripes, labyrinths) and what final wavelength the nonlinear system settles into are not given by these inequalities.

## Where it holds

- **model class**: exactly two diffusing species, constant isotropic diffusivities, no advection, near the homogeneous steady state (linear onset)
- **domain size**: domain at least of order one critical wavelength; below it no unstable mode fits (exact threshold depends on boundary conditions)
- **timescale**: domain growth slow compared with the pattern growth time 1/sigma_max
- **demonstrated in**: ['CIMA chlorite-iodide-malonic acid reaction in a gel reactor (Castets et al. 1990)', 'engineered Nodal-Lefty circuit in HEK293 cells (Sekine et al. 2018)']
- **proposed in tissue**: ['mouse digit patterning (Sheth et al. 2012; Raspopovic et al. 2014)', 'zebrafish trunk pigment stripes (Nakamasu et al. 2009)']
- **notes**: The four inequalities are a mathematically exact criterion INSIDE the model class. Applying them to tissue requires the four Jacobian entries f_u, f_v, g_u, g_v at the steady state. In none of the sources read for this entry were all four measured in a living tissue (scope: the searches and sources listed below, Nov 2026); the Müller et al. 2012 zebrafish Nodal/Lefty work measured the diffusivities and clearance rates, which bound D and the decay parts of f_u and g_v but not the cross-coupling f_v*g_u.


:::{danger} Where it breaks
(1) MORE THAN TWO SPECIES OR ANY IMMOBILE COMPONENT -- the differential-diffusivity requirement demonstrably fails as a NECESSARY condition. Marcon et al. (2016, calculated/analytical screen) report that once cell-autonomous (non-diffusing) factors are present, networks can pattern with EQUALLY diffusing signals and even for any combination of diffusion coefficients. Raspopovic et al. (2014) model mouse digits with a three-node Bmp-Sox9-Wnt network. So "D_v/D_u > d_c" must not be used to REJECT a candidate tissue mechanism or a synthetic design with three or more components: it would rule out patterning networks that work. For real tissue, where signalling networks almost always include cell-autonomous transcription factors, this is the dominant failure. (2) ROBUSTNESS, NOT EXISTENCE, IS THE BINDING CONSTRAINT. Scholes et al. (2019, calculated over 7,625 two- and three-node networks) report that >61% of network design space can produce Turing patterns, but that these are sensitive to even subtle changes in parameters, network structure and regulatory mechanism. Meeting the inequalities at one parameter point therefore does not certify that a tissue or a built circuit will pattern under biological variation; the inequalities can say "possible", not "reliable". (3) PARAMETERS ARE NOT MEASURED IN TISSUE. Our inference from the sources read: since the Jacobian cross-terms are unmeasured in every tissue case found, the criterion cannot currently be checked as a number against any real tissue; claims that a tissue "satisfies Turing's conditions" in the literature read here rest on network topology, perturbation phenotypes (e.g. wavelength shifts with Hox dose, Sheth et al. 2012) and simulation, not on measured inequalities. (4) DIFFERENTIAL DIFFUSIVITY IN TISSUE IS EFFECTIVE, NOT INTRINSIC. Proteins of similar size have similar free diffusivities; the 5- to 15-fold Lefty:Nodal difference is in EFFECTIVE diffusivity. Müller et al. (2012) raise differential binding as a possibility (hypothesis, their word); Sekine et al. (2018) report Nodal is confined beneath cells via its finger-1 domain and that moving this domain into Lefty abolishes patterning. Our inference: D_u and D_v in the criterion must be the hindered, tissue-specific values, so a diffusivity measured in solution or in another tissue is not transferable. (5) MEASURED DIFFERENTIAL DIFFUSIVITY DOES NOT IMPLY A TURING PATTERN. Zebrafish Nodal/Lefty has the measured activator-inhibitor diffusivity contrast, but Müller et al. (2012) do not claim it forms a periodic pattern in the embryo; it is described as supporting the activator/inhibitor reaction-diffusion model of the mesendoderm signalling range. The inequalities are necessary (for two species), not sufficient evidence of a periodic pattern in vivo. (6) PATTERNS WITHOUT DIFFUSING MORPHOGENS. Shyer et al. (2017) report that avian feather-follicle primordia arise from contractility-driven dermal cell aggregation that mechanically activates beta-catenin -- a periodic pattern with no reaction-diffusion pair required. Zebrafish pigment stripes arise from contact- and projection-mediated interactions between pigment CELLS (Nakamasu et al. 2009), with iridophores at the horizontal myoseptum initiating and orienting the stripes (Frohnhöfer et al. 2013). A Turing-like interaction network can exist without any molecule satisfying the diffusion-based conditions; conversely a periodic pattern is not evidence the conditions are met. (7) GROWTH, SMALL DOMAINS AND PREPATTERNS. The linear criterion assumes a fixed domain larger than about one wavelength and no imposed gradient. Raspopovic et al. (2014) required morphogen-gradient modulation to reproduce digit Sox9 patterns, i.e. the bare homogeneous-state analysis does not reproduce the observed limb pattern by itself (author's model claim). We did not locate a measured minimum domain size for any tissue (scope: searches listed under sources).
:::

## Worked examples

**Toy two-species Jacobian (illustrative, NOT a measured tissue)**

```
f_u = 1e-4, f_v = -1e-4, g_u = 2e-4, g_v = -1.5e-4 (1/s); tr J = -0.5e-4 < 0; det J = 0.5e-8 s^-2 > 0; d_c = ((sqrt(0.5) + sqrt(2))/1)^2 = 4.5; with D_u = 0.7 um^2/s (the measured Cyclops value), D_v must exceed 3.15 um^2/s; at onset lambda_c = 2*pi*(0.7*3.15/0.5e-8)^(1/4) um = 911 um
```

- value: `911`

- CALCULATED, entirely hypothetical kinetics chosen by us to sit on the 1e-4 /s scale of the measured Nodal/Lefty clearance rates. It shows the scale arithmetic only -- micron^2/s diffusivities with hour-scale kinetics give sub-millimetre-to-millimetre wavelengths -- and must not be read as a prediction of any zebrafish pattern.

- evidence: **derived**

**Danio rerio blastula, Nodal and Lefty**

```
decay length sqrt(D_eff/k): Cyclops sqrt(0.7/1.22e-4) = 76 um; Squint 179 um; Lefty1 458 um; Lefty2 523 um
```

- value range: `[76, 523]`

- CALCULATED by us from the OBSERVED D_eff and clearance rates of Müller et al. 2012. These are single-species source-sink ranges, not a Turing wavelength (that needs the unmeasured cross-coupling). They show the activator's range is roughly 3-7 times shorter than the inhibitor's, the qualitative pre-condition the law needs.

- evidence: **derived**

**CIMA reaction in a starch-loaded gel reactor**

- Observation (Castets et al. 1990): first sustained standing Turing-type chemical pattern with an intrinsic wavelength. The activator's transport was slowed by binding to the starch matrix, the chemical analogue of hindered diffusion in tissue (mechanism as summarised by Müller et al. 2012).

- evidence: **literature**

**Mus musculus limb, distal Hox dose on a Gli3-null background**

- Observation plus model (Sheth et al. 2012): progressively lowering Hoxa13/Hoxd11-13 dose gives progressively more, thinner, more densely packed digits, which the authors read as Hox dose tuning the wavelength of a Turing-type mechanism. The activator and inhibitor were not identified in that paper (as noted by a Genome Biology research highlight, read at search-summary level).

- evidence: **literature**

:::{seealso} Contested
- Marcon et al. (2016), analytical screen: differential diffusivity of the mobile signals is NOT required when cell-autonomous factors are present. Treat as a different model class from Turing's two-species case, not a correction of the two-species algebra (which remains exact).
- Scholes et al. (2019), calculated: Turing-capable networks are common (>61% of 2-3 node design space) but not robust to parameter or structural change -- the opposite emphasis to the long-standing view that Turing patterns need fine-tuned, rare parameter sets. Both views are recorded; this entry does not reconcile them.
- Zebrafish trunk stripes: Nakamasu et al. (2009) report the pigment-cell interaction network has the properties needed for a Turing pattern; Frohnhöfer et al. (2013) report iridophores, previously treated as passive in Turing-type reasoning, are required and initiate stripes at the horizontal myoseptum, though the process is then self-organising. A Watanabe & Kondo response disputing that the Turing-type model needs modification was seen only as a search-summary mention; its citation was not retrieved.
- Feather-follicle spacing: Shyer et al. (2017) attribute primordium formation to dermal-cell mechanics; reaction-diffusion accounts of the same skin appendages exist. The search summary seen did not show Shyer et al. explicitly ruling out reaction-diffusion; whether the two mechanisms compete or combine is recorded here as unresolved.
:::

## Sources

| Citation | Read-level |
|---|---|
| Turing AM (1952) The chemical basis of morphogenesis. Phil Trans R Soc Lond B 237(641):37-72 | `search-summary` |
| Gierer A, Meinhardt H (1972) A theory of biological pattern formation. Kybernetik 12:30-39 (volume and pages NOT verified in this session) | `search-summary` |
| Murray JD, Mathematical Biology (Springer), chapters on spatial pattern formation | `could-not-access` |
| Castets V, Dulos E, Boissonade J, De Kepper P (1990) Experimental evidence of a sustained standing Turing-type nonequilibrium chemical pattern. Phys Rev Lett 64:2953-2956. doi:10.1103/PhysRevLett.64.2953 | `search-summary` |
| Müller P, Rogers KW, Jordan BM, Lee JS, Robson D, Ramanathan S, Schier AF (2012) Differential diffusivity of Nodal and Lefty underlies a reaction-diffusion patterning system. Science 336(6082):721-724. doi:10.1126/science.1221920 | `full-text` |
| Sekine R, Shibata T, Ebisuya M (2018) Synthetic mammalian pattern formation driven by differential diffusivity of Nodal and Lefty. Nat Commun 9:5456. doi:10.1038/s41467-018-07847-x | `search-summary` |
| Marcon L, Diego X, Sharpe J, Müller P (2016) High-throughput mathematical analysis identifies Turing networks for patterning with equally diffusing signals. eLife 5:e14022 | `search-summary` |
| Scholes NS, Schnoerr D, Isalan M, Stumpf MPH (2019) A comprehensive network atlas reveals that Turing patterns are common but not robust. Cell Systems 9(3):243-257 | `search-summary` |
| Sheth R, Marcon L, Bastida MF, Junco M, Quintana L, Dahn R, Kmita M, Sharpe J, Ros MA (2012) Hox genes regulate digit patterning by controlling the wavelength of a Turing-type mechanism. Science 338:1476-1480. doi:10.1126/science.1226804 | `search-summary` |
| Raspopovic J, Marcon L, Russo L, Sharpe J (2014) Digit patterning is controlled by a Bmp-Sox9-Wnt Turing network modulated by morphogen gradients. Science 345(6196):566-570. doi:10.1126/science.1252960 | `search-summary` |
| Nakamasu A, Takahashi G, Kanbe A, Kondo S (2009) Interactions between zebrafish pigment cells responsible for the generation of Turing patterns. PNAS 106(21):8429-8434 | `search-summary` |
| Frohnhöfer HG, Krauss J, Maischein HM, Nüsslein-Volhard C (2013) Iridophores and their interactions with other chromatophores are required for stripe formation in zebrafish. Development 140(14):2997-3007. doi:10.1242/dev.096719 | `abstract` |
| Shyer AE, Rodrigues AR, Schroeder GG, Kassianidou E, Kumar S, Harland RM (2017) Emergent cellular self-organization and mechanosensation initiate follicle pattern in the avian skin. Science 357(6353):811-815. doi:10.1126/science.aai7868 | `search-summary` |


---

*Generated from [`library/laws/turing-conditions.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/turing-conditions.yaml). Do not edit this page; edit the YAML.*
