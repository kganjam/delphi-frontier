# Digit patterning as a Turing system — simulation notes

**Everything in this directory is a SIMULATION.** No number, figure or phenotype class here is an
observation, a measurement, or a reproduction of published data. Nothing was fitted to data,
and no agreement with data is claimed anywhere.

Produced by `digit_turing.py`. Machine-readable results: `digit-turing.json`.

---

## 1. What the model is, and where each piece came from

A Bmp–Sox9–Wnt (BSW) reaction–diffusion system on a 2-D limb-bud-shaped domain, with a
proximodistal Fgf gradient that modulates two of its edges.

```
dS/dt = beta * ( k2*B - k3*W - S^3 )
dB/dt = beta * ( alpha_B - (1 - kF*F)*k4*S - k5*B + D_B * lap(B) )
dW/dt = beta * ( alpha_W - k7*kF*F*S     - k9*W + D_W * lap(W) )
F(x_hat) = F_max * exp(-g * x_hat)      x_hat = normalised distance proximal from the margin
```

Sox9 (`S`) does not diffuse. Bmp (`B`) is the long-range species (`D_B = 160`); Wnt (`W`) is the
short-range one (`D_W = 25`). The only nonlinearity is the cubic `-S^3`. The instability runs
through the double-negative loop Sox9 ⊣ Wnt ⊣ Sox9 (short-range self-activation) against the
loop Sox9 ⊣ Bmp → Sox9 (long-range inhibition).

### Read-levels (checked, not assumed)

| Source | Read-level | How that was established |
|---|---|---|
| Raspopovic et al. 2014, Science 345:566 (PMID 25082703, [DOI](https://doi.org/10.1126/science.1252960)) | **abstract** | PMID and DOI resolved via the PubMed MCP tool. Europe PMC: `isOpenAccess=N`, `inEPMC=N`, no PMC id. Full text and supplement are subscription-only and were **not** read. |
| Sheth et al. 2012, Science 338:1476 (PMID 23239739, [DOI](https://doi.org/10.1126/science.1226804)) | **abstract** | PMC4486416 is a PMC Canada author manuscript. The PubMed full-text tool returned an **empty body**; Europe PMC `fullTextXML` returned HTTP 500; the rendered PDF returned HTTP 403; NCBI `efetch db=pmc` returned front matter with **no `<body>`**. Only the abstract was read. |
| Onimaru et al. 2016, Nat Commun 7:11582 (PMID 27211489, [DOI](https://doi.org/10.1038/ncomms11582)) | **full-text** | Full text XML from the Europe PMC REST endpoint (HTTP 200, 120 161 bytes). Equations are published as images; `ncomms11582-m22..m25.jpg` were downloaded from the PMC CDN and read directly. Parameter values read verbatim from the Methods paragraph *Mathematical analysis and numerical simulation*. |

**This is the crux of the provenance.** The paper whose model this is (Raspopovic 2014) could not
be read past its abstract. The equations and numbers come from **Onimaru et al. 2016**, which is
open access, is from the same laboratory, and states in its own text that it uses *"the BSW
model"* of Raspopovic et al. (its reference 12) and that the Fgf gradient modulates the same
parameters as in the mouse model, *"repressing k4 and boosting k7"*. Onimaru et al. apply it to a
**growing catshark pectoral fin**, where Sox9 forms spots, not to the mouse limb. So the equation
form is well sourced; the numbers are sourced but from the wrong animal; and the mouse parameter
set is simply not in my hands.

### Parameter provenance

**Sourced** (Onimaru 2016 Methods, the Figs 4–5 parameter list, read at full-text level):
`beta=8, k2=1, k3=3, k4=6, k7=2.4, k5=0.1, k9=0.1, kF=0.667, D_B=160, D_W=25, alpha_B=0.1`.

**Assumed**: `alpha_W` (see below), `F_max`, `F_decay`, the paddle dimensions `L_PD`/`W_AP_half`,
and the numerical parameters `dx`, `dt`, `T_end`, `noise_amplitude`.

### The one sourced parameter I changed, and why

`alpha_W` is published as **1.2**. I use **0.0333**.

With the published value, **my own linear stability analysis finds no Turing instability
anywhere**: 51 values of `F` in [0,1], every real homogeneous steady state at each (1–3 roots),
6001 wavenumbers in [0, 1.2]. The largest growth rate found is +3.58, and that state is already
unstable at `q = 0`, which is a uniform instability, not a Turing one. The diagnosis is that with
`alpha_W = 1.2` the steady state sits far from zero (`S*` between about −5.8 and −0.58 on the
branch continuous in `F`), so the cubic self-damping `-3*S*^2` is large and suppresses the
instability.

`alpha_W = k2*alpha_B*k9/(k3*k5) = 0.0333` places the steady state exactly at `S* = 0`, where that
damping term vanishes and the paper's own **linear** Turing conditions apply — and those
conditions are derived in Onimaru's Methods for the linear model with `k1 = 0`, i.e. for
`f_S = 0`, and with `k3 = 1`, not for the cubic model with `k3 = 3`. So my test is not
like-for-like with theirs: they run on a growing mesh with per-step noise and an Fgf field whose
absolute spatial scale is set by a mesh I do not have. **This is not a claim that the published
model is wrong.** It is a statement that I could not reproduce a Turing instability from the
published numbers as I read them, so the operating point used here is mine and is labelled
assumed.

---

## 2. Linear stability vs simulation — the internal control

| Quantity | Value (model length units) |
|---|---|
| `lambda_lin` — LSA, fastest-growing mode at F = 0.62 | **42.8** |
| 1-D uniform-domain simulation, probed at t = 2 (still linear) | **45.5** |
| 1-D uniform-domain simulation, saturated (t = 160), F = 0.62 | **125.0** |
| same, F = 0.45 | 93.8 |
| same, F = 0.30 | 60.0 |
| `lambda_meas` — 2-D anteroposterior element spacing, 6 wild-type seeds | **81.1** |

**They disagree, by about a factor of two, and I am reporting the disagreement rather than tuning
until they agree.**

The agreement that *does* hold is in the linear regime: 45.5 against a predicted 42.8, in a 1-D
uniform-domain run probed while the amplitude is still small. After onset the pattern **coarsens**,
and the coarsening **arrests**: measured at t = 20, 40, 80, 160 and 320 in a 1-D control, the
dominant wavelength is unchanged from t ≈ 40 onwards. So the saturated pattern has a longer,
nonlinearly selected wavelength than the fastest-growing linear mode. The run length `T_end = 60`
is past arrest.

The 2-D measured spacing (81) is shorter than the 1-D saturated wavelength at F = 0.62 (125)
because the 2-D permissive band spans a *range* of F, not just its distal maximum, and is only
about one wavelength deep.

**`lambda_meas = 81` is the pattern's own wavelength and is the one the critical domain size is
quoted in.**

---

## 3. Turing window, and where the gradient puts the bud

The LSA gives a Turing-unstable window **0.175 < F < 0.679**. Below it the uniform state is
stable (no pattern); above it the state is unstable at `q = 0` — a uniform runaway, not a Turing
pattern. `F_max` was therefore set to **0.62**, just below the upper edge, so that no part of the
bud sits in the uniform-instability regime. `F_decay = 4` (against the published square-domain
value of 3) makes the permissive band about one wavelength deep, which is what gives a single
proximodistal row of elements rather than two rows.

---

## 4. Numerics

Semi-implicit IMEX: diffusion and linear decay of B and W implicit (one sparse LU factorisation
per condition, reused every step); the cubic in S treated semi-implicitly as `-S_new * S_old^2`,
which keeps S bounded; all couplings explicit. Zero-flux boundary on the masked domain. This
differs from Onimaru et al., who use an explicit Heun solver at dt = 0.002 on a growing triangular
finite-volume mesh.

**dt = 0.02 was measured to be numerically unstable** here (the solution diverged to ~1e8).
dt = 0.01, 0.005 and 0.002 agree on the final field to 5 significant figures. dt = 0.01 is the
default.

---

(Sections 5–8 — sweeps, seed spread, refinement, controls and what this does not establish —
are completed from the final run below.)
