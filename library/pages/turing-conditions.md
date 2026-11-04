---
title: Turing's conditions for diffusion-driven instability, and when real tissue meets them
label: law-turing-conditions
---

:::{important}
**Constraining** — this law yields a number a design is checked against.
:::

## The law

:::{math}
:label: eq-turing-conditions
\begin{aligned} &(1)\; f_u + g_v < 0 \qquad (2)\; f_u g_v - f_v g_u > 0 \\ &(3)\; D_v f_u + D_u g_v > 0 \qquad (4)\; (D_v f_u + D_u g_v)^2 > 4 D_u D_v (f_u g_v - f_v g_u) \\ &\text{onset: } D_v f_u + D_u g_v = 2\sqrt{D_u D_v \det J}, \quad k_c^2 = \sqrt{\det J / (D_u D_v)}, \quad \lambda_c = 2\pi / k_c \\ &d = D_v/D_u > d_c = \left(\frac{\sqrt{\det J} + \sqrt{-f_v g_u}}{f_u}\right)^2 \quad (f_u > 0) \end{aligned}
:::

### Symbols

| Symbol | Dimension | Units | Meaning |
|---|---|---|---|
| `D_u` | L^2/T | m^2/s | effective diffusivity of the activator (species u) |
| `D_v` | L^2/T | m^2/s | effective diffusivity of the inhibitor (species v) |
| `f_u` | 1/T | 1/s | Jacobian entry d(du/dt)/du at the homogeneous steady state; positive for an activator (self-enhancement) |
| `f_v` | 1/T | 1/s | Jacobian entry d(du/dt)/dv; the effect of the inhibitor on the activator |
| `g_u` | 1/T | 1/s | Jacobian entry d(dv/dt)/du; the effect of the activator on the inhibitor |
| `g_v` | 1/T | 1/s | Jacobian entry d(dv/dt)/dv; negative (inhibitor self-decay) |
| `det_J` | 1/T^2 | 1/s^2 | determinant of the reaction Jacobian, f_u*g_v - f_v*g_u |
| `tr_J` | 1/T | 1/s | trace of the reaction Jacobian, f_u + g_v |
| `k_c` | 1/L | 1/m | critical wavenumber at onset |
| `lambda_c` | L | m | critical pattern wavelength at onset, 2*pi/k_c |
| `d` | 1 | dimensionless | diffusivity ratio D_v/D_u |
| `d_c` | 1 | dimensionless | critical diffusivity ratio; instability requires d > d_c (two species, f_u > 0) |

### Measured constants

| Constant | Value | Note |
|---|---|---|
| `D_cyclops` | 7e-13 (interval 5e-13 to 9e-13) m^2/s | Cyclops-GFP (Nodal); 0.7 ± 0.2 um^2/s |
| `D_squint` | 3.2e-12 (interval 2.7e-12 to 3.7e-12) m^2/s | Squint-GFP (Nodal); 3.2 ± 0.5 um^2/s |
| `D_lefty1` | 1.11e-11 (interval 1.05e-11 to 1.17e-11) m^2/s | Lefty1-GFP; 11.1 ± 0.6 um^2/s |
| `D_lefty2` | 1.89e-11 (interval 1.59e-11 to 2.19e-11) m^2/s | Lefty2-GFP; 18.9 ± 3.0 um^2/s |
| `k_cyclops` | 0.000122 (interval 0.000109 to 0.000135) 1/s | extracellular clearance rate constant, Cyclops-Dendra2, (1.22 ± 0.13)e-4 /s |
| `k_squint` | 0.0001 (interval 9.4e-05 to 0.000106) 1/s | Squint-Dendra2, (1.00 ± 0.06)e-4 /s |
| `k_lefty1` | 5.3e-05 (interval 4.8e-05 to 5.8e-05) 1/s | Lefty1-Dendra2, (0.53 ± 0.05)e-4 /s |
| `k_lefty2` | 6.9e-05 (interval 6.2e-05 to 7.6e-05) 1/s | Lefty2-Dendra2, (0.69 ± 0.07)e-4 /s |
| `clearance_normalised_ratio_mueller` | 14 dimensionless | The authors' reported average of (D_inhibitor/k_inhibitor)/(D_activator/k_activator), quoted as "R ≈ 14"; no interval is given in the text I read. My recalculation (a calculation, not an observation) shows that 14 is the ratio of the AVERAGED Lefty and Nodal values: (15.0/0.61e-4)/(1.95/1.11e-4) = 14.0. The four individual Nodal–Lefty pairings give 6.5 (Squint/Lefty1), 8.6 (Squint/Lefty2), 36.5 (Cyclops/Lefty1) and 47.7 (Cyclops/Lefty2), and their arithmetic mean is 24.8. Which reduction is "the" ratio is a choice, not a measurement. |
| `d_c` | unknown | NOT a constant. d_c is set entirely by the reaction Jacobian, and d_c > 1 always holds for two species when conditions 1 and 2 hold. Rule-of-thumb thresholds circulate (Müller et al. 2012 quote "at least six-fold" from earlier models, and suggest "5- to 15-fold" as a possibly general feature), but the repo ledger (row 3) holds a machine-checked counterexample that is unstable at d = 1.1. No universal number exists. |

## Why it holds

A homogeneous steady state that is stable to spatially uniform perturbations (conditions 1–2) is made unstable to a band of spatial wavenumbers by diffusion alone. Linearising u_t = f(u,v) + D_u ∇²u, v_t = g(u,v) + D_v ∇²v about the steady state, a Fourier mode with wavenumber k grows when det(J − k² diag(D_u, D_v)) < 0. That determinant is a quadratic in k² whose minimum dips below zero exactly when conditions 3 and 4 hold. Condition 3 needs f_u and g_v of opposite sign (a self-enhancing activator and a self-limiting inhibitor) and D_v ≠ D_u. With f_u > 0 it needs d > 1 and, through condition 4, d > d_c. Physically: the activator must be held near its source (short range) while the inhibitor escapes (long range), which is Gierer and Meinhardt's "local activation, lateral inhibition". The wavelength at onset, λ_c = 2π (D_u D_v / det J)^(1/4), is set by diffusivities and reaction rates, NOT by tissue size. A bounded tissue of length ℓ with no-flux boundaries admits only k = nπ/ℓ, so it patterns only if one of those discrete modes falls inside the unstable band. Too small a tissue gives no pattern even when conditions 1–4 hold.

## Where it holds

- **model**: two diffusing species, deterministic, linear stability about a homogeneous steady state, fixed domain
- **species**: 2
- **noise**: negligible (large copy numbers)
- **domain**: static, larger than about half of lambda_c, with no-flux or periodic boundaries
- **notes**: The conditions are necessary and sufficient for LINEAR instability of THIS model. They say nothing about whether the nonlinear end state is spots, stripes or travelling waves. Applying them to tissue requires the four Jacobian entries, and these are essentially never measured in vivo. Diffusivities are now routinely measured (FRAP, FCS), so in practice only conditions 3–4's diffusion side is checked, and the Jacobian side is assumed.


:::{danger} Where it breaks
(a) MORE THAN TWO SPECIES, or ANY NON-DIFFUSING NODE. The requirement d > d_c > 1 is an artefact of the two-species model. Marcon et al. 2016 (eLife 5:e14022) report, from automated linear stability analysis of 3- and 4-node networks containing cell-autonomous (non-diffusing) factors, topologies that pattern with EQUAL diffusivities, and others that pattern with any combination of diffusivities (abstract-level read). The digit network actually proposed for the mouse limb (Raspopovic et al. 2014, Bmp–Sox9–Wnt) routes through the non-diffusing transcription factor Sox9. So measuring D_v/D_u ≈ 1 in a real tissue does NOT rule out a Turing mechanism, and measuring D_v/D_u ≫ 1 does not establish one. (b) INTRINSIC NOISE / SMALL COPY NUMBER. Karig et al. 2018 (PNAS 115:6572) built an E. coli activator–inhibitor circuit and report patterns whose spatial correlations match stochastic Turing theory. Per their abstract, that theory predicts patterns over a much wider parameter range than the deterministic conditions, with no severe requirement on the diffusivity ratio. The deterministic conditions therefore under-predict where patterns occur once fluctuations are large. (c) NO DIFFUSION AT ALL. In adult zebrafish skin the stripe-forming interactions are between pigment CELLS. Nakamasu et al. 2009 (PNAS 106:8429) measured them by laser ablation as short-range mutual exclusion plus a long-range effect on survival. Diffusivities D_u and D_v are undefined there. The authors call the result a Turing pattern. My inference: what carries over is only the short-range/long-range kernel shape, and the inequalities in this entry cannot be evaluated for that system. (d) MEETING THE DIFFUSIVITY CONDITION IS NOT USING IT. Zebrafish Nodal/Lefty meet the differential-diffusivity requirement: measured D ratios are 3.5–27 (Müller et al. 2012). Yet Rogers et al. 2017 (eLife 6:e28785) report that lefty mutants are rescued to healthy adults by spatially and temporally UNIFORM Nodal inhibitor drug, with reduced tolerance to perturbation. The authors' claim is that Lefty feedback is not required for patterning but buffers it. My inference: the mesendoderm Nodal pattern is not a Turing instability, even though the measured diffusivities satisfy the two-species ratio requirement. The pattern is graded, not periodic. (e) GROWING OR SMALL DOMAINS. Tissue smaller than about λ_c/2 admits no unstable mode. Growth changes which modes are admissible over time, so a fixed-domain analysis does not predict the final pattern of a growing tissue. I did not obtain a source in this session that quantifies the growing-domain case, and I state it as a property of the model, not as an observation. (f) PARAMETER ROBUSTNESS. Scholes et al. 2019 (Cell Syst 9:243) report, across 7,625 2- and 3-node networks, that more than 61% of network design space can pattern but is sensitive to small parameter changes (abstract-level read). In practice a design that sits just above d_c sits on a knife edge: the measured effective diffusivities in Müller et al. 2012 carry reported errors of 5–29% of the mean (Lefty1 ±0.6 on 11.1; Cyclops ±0.2 on 0.7 um^2/s), which is enough to cross d_c.
:::

## Worked examples

**none (nondimensional; repo ledger row 3 counterexample)**

```
J = [[1, -1], [1.011, -1.01]]. tr J = -0.010, det J = 0.001, -f_v g_u = 1.011. d_c = (sqrt(0.001) + sqrt(1.011))^2 / 1^2 = (0.0316 + 1.0055)^2 = 1.0756. At d = 1.1 (> d_c): condition 3 = 0.090 > 0, condition 4 = 0.0037 > 0, max growth rate 0.0088, fastest wavenumber 0.180 (wavelength 34.8). At d = 1.05 (< d_c): condition 4 = -0.0026, no growing mode.

```

- value: `1.0756`

- Calculated by me (scratch script, dispersion relation evaluated on a fine k grid), not observed. It agrees with the ledger's Lean counterexample, which is unstable at d = 1.1. It refutes any fixed "D ratio ≥ 5/6/10" rule: the threshold can sit arbitrarily close to 1 when f_u is large relative to sqrt(det J) and sqrt(-f_v g_u).

- evidence: **derived**

**Danio rerio blastula, Nodal (Cyclops, Squint) and Lefty (Lefty1, Lefty2)**

```
Raw D ratios from the measured means: Squint/Lefty1 3.47, Squint/Lefty2 5.91, Cyclops/Lefty1 15.9, Cyclops/Lefty2 27.0. Propagating the reported ± errors to their corners gives 2.8–4.3, 4.3–8.1, 11.7–23.4 and 17.7–43.8. Decay lengths sqrt(D/k): Cyclops 75.7 um, Squint 178.9 um, Lefty1 457.6 um, Lefty2 523.4 um. Half-lives ln2/k: 94.7, 115.5, 218.0 and 167.4 min.

```

- value range: `[3.47, 27.0]`

- Every number here is CALCULATED by me from Müller et al. 2012's measured means. d_c for this system is UNKNOWN, because the Nodal/Lefty reaction Jacobian has not been measured. I found no measurement of it in the sources read for this entry; scope: the six papers listed below, not a systematic search. So conditions 1, 2 and 4 cannot be checked from data, and "Nodal/Lefty meets Turing's conditions" is not established, only "meets the diffusivity side of condition 3". See where_it_breaks (d) for evidence that the pattern is not Turing in any case.

- evidence: **derived**

**none (illustrative; ASSUMED Jacobian, Cyclops-like activator diffusivity)**

```
Assumed f_u = 1e-4, f_v = -1e-4, g_u = 2e-4, g_v = -1.5e-4 per s. These are chosen to match the ~1e-4 /s order of the measured clearance rates and are not measured. tr J = -5e-5 /s, det J = 5e-9 /s^2, d_c = 4.50. With D_u = 0.7 um^2/s the inhibitor needs D_v > 3.15 um^2/s, and the onset wavelength is lambda_c = 2*pi*(0.7*3.15/5e-9)^(1/4) = 910 um. With D_v = 11.1 (Lefty1) or 18.9 (Lefty2) um^2/s the fastest-growing wavelength is about 1085 or 1185 um.

```

- value: `910`

- Calculated, not observed, and conditional on an invented Jacobian. It shows the design use: given a Jacobian, the entry yields a pass/fail threshold on D_v and a predicted wavelength to compare with tissue size. I did not check this wavelength against any measured tissue dimension.

- evidence: **derived**

:::{seealso} Contested
- Is differential diffusivity a general requirement? Müller et al. 2012 suggest a 5- to 15-fold inhibitor/activator diffusivity ratio may be a general feature of reaction-diffusion patterning. Marcon et al. 2016 report network topologies (with non-diffusing nodes) that pattern with equal diffusivities. Not reconciled here.
- Are Turing networks robust? Scholes et al. 2019 report that patterning networks are common (>61% of design space) but not robust to parameter changes. Marcon et al. 2016 frame some topologies as working for any combination of diffusivities, i.e. robust in the diffusion parameters. These are different robustness measures, and the sources do not agree on a verdict.
- Is zebrafish Nodal/Lefty a reaction-diffusion (Turing-type) system? Müller et al. 2012 present their diffusivity data as biophysical support for activator/inhibitor reaction-diffusion models. Rogers et al. 2017 report that uniform inhibitor rescues lefty mutants, i.e. Lefty's spatial feedback is dispensable. Not reconciled here.
:::

## Sources

| Citation | Read-level |
|---|---|
| Turing AM (1952) The chemical basis of morphogenesis. Phil. Trans. R. Soc. Lond. B 237:37-72 | `search-summary` |
| Gierer A, Meinhardt H (1972) A theory of biological pattern formation. Kybernetik (volume/pages not verified in this session) | `search-summary` |
| Müller P, Rogers KW, Jordan BM, Lee JS, Robson D, Ramanathan S, Schier AF (2012) Differential diffusivity of Nodal and Lefty underlies a reaction-diffusion patterning system. Science 336(6082):721-724. doi:10.1126/science.1221920 | `full-text` |
| Marcon L, Diego X, Sharpe J, Müller P (2016) High-throughput mathematical analysis identifies Turing networks for patterning with equally diffusing signals. eLife 5:e14022 | `abstract` |
| Raspopovic J, Marcon L, Russo L, Sharpe J (2014) Digit patterning is controlled by a Bmp-Sox9-Wnt Turing network modulated by morphogen gradients. Science 345(6196):566-570. doi:10.1126/science.1252960 | `search-summary` |
| Karig D et al. (2018; full author list not verified in this session) Stochastic Turing patterns in a synthetic bacterial population. PNAS 115(26):6572-6577 | `abstract` |
| Nakamasu A, Takahashi G, Kanbe A, Kondo S (2009) Interactions between zebrafish pigment cells responsible for the generation of Turing patterns. PNAS 106(21):8429-8434. doi:10.1073/pnas.0808622106 | `abstract` |
| Rogers KW, Lord ND, Gagnon JA, Pauli A, Zimmerman S, Aksel DC, Reyon D, Tsai SQ, Joung JK, Schier AF (2017) Nodal patterning without Lefty inhibitory feedback is functional but fragile. eLife 6:e28785. doi:10.7554/eLife.28785 | `abstract` |
| Scholes NS, Schnoerr D, Isalan M, Stumpf MPH (2019) A comprehensive network atlas reveals that Turing patterns are common but not robust. Cell Systems 9(3):243-257 | `abstract` |
| Sekine R, Shibata T, Ebisuya M (2018) Synthetic mammalian pattern formation driven by differential diffusivity of Nodal and Lefty. Nat. Commun. 9:5456. doi:10.1038/s41467-018-07847-x | `abstract` |
| Castets V, Dulos E, Boissonade J, De Kepper P (1990) Experimental evidence of a sustained standing Turing-type nonequilibrium chemical pattern. Phys. Rev. Lett. 64(24):2953-2956 | `listing` |
| delphi-frontier ledger/README.md row 3 (Lean counterexample, unstable at diffusion ratio 1.1) | `full-text` |


---

*Generated from [`library/laws/turing-conditions.yaml`](https://github.com/kganjam/delphi-frontier/blob/main/library/laws/turing-conditions.yaml). Do not edit this page; edit the YAML.*
