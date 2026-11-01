# Digit patterning as a Turing system — simulation notes

**Everything in this directory is a SIMULATION.** No number, figure or phenotype class here is an
observation, a measurement, or a reproduction of published data. Nothing was fitted to data, and
no agreement with data is claimed anywhere.

Produced by `digit_turing.py`. Machine-readable results: `digit-turing.json`.
Figures: `digit-turing-normal.png`, `digit-turing-series.png`, `digit-turing-domain.png`,
`digit-turing.mp4`.

*Per the PubMed terms of use: article metadata below was retrieved from PubMed, and every cited
article carries its DOI link.*

---

## 0. The two negative results are load-bearing — keep them visible

Asked whether the two negative results should be rendered prominently rather than buried: **yes,
and they are the reason the rest of this is worth anything.** Both are stated at the top of the
JSON object they belong to, not in a footnote, and neither was softened.

1. **I could not reproduce a Turing instability from the published parameter set as I read it.**
   Scope of the negative, stated beside the finding: 51 gradient values across F ∈ [0, 1], *every*
   real homogeneous steady state at each (1–3 roots per value), 6001 wavenumbers across
   [0, 1.2]. Best growth rate found +3.58, and that state is unstable already at q = 0 — a uniform
   instability, not a Turing one. **This is NOT a claim that the published model is wrong.** The
   authors run it on a *growing* catshark-fin mesh whose absolute spatial scale I do not have, and
   their own Turing-space analysis is derived for the **linear** form of the model (`k1 = 0`, so
   `f_S = 0`) with `k3 = 1`, not for the cubic form with `k3 = 3`. My test is a static homogeneous
   domain and is not like-for-like. What it licenses is exactly one thing: the operating point
   used here is **mine**, and `alpha_W` is labelled `assumed` rather than `sourced`.
2. **Linear stability predicts 42.8 and the 2-D pattern measures 81.1 — a factor of 1.9 out — and
   the mechanism is named rather than tuned away.** The pattern coarsens after onset and the
   coarsening *arrests*: measured at t = 20, 40, 80, 160 and 320, the wavelength is unchanged from
   t ≈ 40 onwards. The linear prediction describes the fastest-growing mode *at onset*, which is a
   different quantity from the wavelength of the saturated pattern. The agreement that does hold
   is the one that should: in the linear regime, at t = 2, the simulation gives 45.5 against a
   predicted 42.8.

If either is cut for space, cut the study instead. A parameter set labelled `assumed` with no
stated reason reads as a shortcut; labelled with the search that failed and its scope, it reads as
what it is.

**A third one belongs with them, and it is the least flattering:** the *no-initial-perturbation*
control **failed** (§4). It is reported as failed, with the arithmetic that explains why the test
was unsound as designed, rather than quietly relabelled. It is in `controls` under
`no_initial_perturbation`, with `"result": "DID NOT STAY FLAT"`.

---

## 1. The model, and where each piece came from

A Bmp–Sox9–Wnt (BSW) reaction–diffusion system on a 2-D limb-bud-shaped domain, with a
proximodistal Fgf gradient modulating two of its edges.

```
dS/dt = beta * ( k2*B - k3*W - S^3 )
dB/dt = beta * ( alpha_B - (1 - kF*F)*k4*S - k5*B + D_B * lap(B) )
dW/dt = beta * ( alpha_W - k7*kF*F*S       - k9*W + D_W * lap(W) )
F(x_hat) = F_max * exp(-g * x_hat)     x_hat = normalised distance proximal from the margin
```

Sox9 (`S`) does not diffuse. Bmp (`B`) is long-range (`D_B = 160`); Wnt (`W`) is short-range
(`D_W = 25`). The only nonlinearity is the cubic `-S^3`. The instability runs through the
double-negative loop **Sox9 ⊣ Wnt ⊣ Sox9** (short-range self-activation) against
**Sox9 ⊣ Bmp → Sox9** (long-range inhibition). Fgf represses `k4` and boosts `k7`, which sweeps
the tissue through Turing space along the proximodistal axis.

### Read-levels — checked, not assumed

| Source | Read-level | How that was established |
|---|---|---|
| Raspopovic, Marcon, Russo & Sharpe (2014) *Science* 345:566–570. PMID 25082703, [DOI](https://doi.org/10.1126/science.1252960) | **abstract** | PMID and DOI resolved through the PubMed tool. Europe PMC reports `isOpenAccess=N`, `inEPMC=N`, no PMC id. Full text and supplement are subscription-only and were **not** read. |
| Sheth, Marcon, Bastida, Junco, Quintana, Dahn, Kmita, Sharpe & Ros (2012) *Science* 338:1476–1480. PMID 23239739, [DOI](https://doi.org/10.1126/science.1226804) | **abstract** | PMC4486416 is a PMC Canada author manuscript. The PubMed full-text tool returned an **empty body**; Europe PMC `fullTextXML` → HTTP 500; the rendered PDF → HTTP 403; NCBI `efetch db=pmc` returned front matter with **no `<body>`**. Only the abstract was read. |
| Onimaru, Marcon, Musy, Tanaka & Sharpe (2016) *Nat Commun* 7:11582. PMID 27211489, [DOI](https://doi.org/10.1038/ncomms11582) | **full-text** | Full-text XML from the Europe PMC REST endpoint (HTTP 200, 120 161 bytes). Equations are published as images; `ncomms11582-m22…m25.jpg` were downloaded from the PMC CDN and read directly. Parameter values read verbatim from the Methods paragraph *Mathematical analysis and numerical simulation*. |

**This is the crux of the provenance.** The paper whose model this is (Raspopovic 2014) could not
be read past its abstract. The equations and the numbers come from **Onimaru et al. 2016**, which
is open access, is from the same laboratory, and states in its own text that it uses *"the BSW
model"* of Raspopovic et al. (its reference 12) and that the Fgf gradient modulates the same
parameters as in the mouse model, *"repressing k4 and boosting k7"*. But Onimaru et al. apply it
to a **growing catshark pectoral fin**, where Sox9 forms spots. So: the equation form is well
sourced; the numbers are sourced but from the wrong animal; and the mouse parameter set is simply
not in my hands.

Sheth et al. 2012 is used for **one thing only** — the *direction* of the wavelength sweep
(progressive loss of distal Hox dose → more, thinner, densely packed digits → shorter
wavelength). **No quantitative value is taken from it.**

### Parameter provenance

**Sourced**, from Onimaru 2016 Methods, the Figs 4–5 parameter list, at full-text level:
`beta=8, k2=1, k3=3, k4=6, k7=2.4, k5=0.1, k9=0.1, kF=0.667, D_B=160, D_W=25, alpha_B=0.1`.

**Assumed**: `alpha_W` (below), `F_max=0.62`, `F_decay=4`, the paddle dimensions
(`L_PD=300`, `W_AP_half=220`), and the numerics (`dx=4`, `dt=0.01`, `T_end=60`,
`noise_amplitude=0.01`).

### The one sourced parameter I changed, and why

`alpha_W` is published as **1.2**. I use **0.0333**.

**With the published value my own linear stability analysis finds no Turing instability
anywhere.** Scope of that negative: 51 values of `F` across [0, 1]; *every* real homogeneous
steady state at each (1–3 roots); 6001 wavenumbers across [0, 1.2]. The largest growth rate found
is **+3.58**, and that state is already unstable at `q = 0` — a uniform instability, not a Turing
one. Diagnosis: with `alpha_W = 1.2` the steady state sits far from zero (`S*` between about
−5.8 and −0.58 on the branch continuous in `F`), so the cubic self-damping `−3·S*²` is large and
suppresses the instability.

`alpha_W = k2·alpha_B·k9 / (k3·k5) = 0.0333` puts the steady state exactly at `S* = 0`, where that
damping term vanishes and the paper's own **linear** Turing conditions apply.

**This is not a claim that the published model is wrong.** My test is not like-for-like with
theirs: they run on a *growing* mesh with per-step noise and an Fgf field whose absolute spatial
scale is set by a mesh I do not have, and their published Turing-space analysis is derived for the
**linear** model (`k1 = 0`, so `f_S = 0`) with `k3 = 1`, not for the cubic model with `k3 = 3`.
What it does mean is that I could not reproduce a Turing instability from the published numbers as
I read them, so the operating point used here is **mine**, and labelled assumed.

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

The agreement that *does* hold is in the **linear regime**: 45.5 against a predicted 42.8, in a
1-D uniform-domain run probed while the amplitude is still small. After onset the pattern
**coarsens**, and the coarsening **arrests**: measured at t = 20, 40, 80, 160 and 320 in a 1-D
control, the dominant wavelength is unchanged from t ≈ 40 onwards. So the saturated pattern has a
longer, nonlinearly selected wavelength than the fastest-growing linear mode. `T_end = 60` is past
arrest.

The 2-D measured spacing (81) is shorter than the 1-D saturated wavelength at F = 0.62 (125)
because the 2-D permissive band spans a *range* of F, not just its distal maximum, and is only
about one wavelength deep.

**`lambda_meas = 81` is the pattern's own wavelength and is what the critical domain size is
quoted in.**

### Turing window

The LSA gives a Turing-unstable window **0.175 < F < 0.679**. Below it the uniform state is
stable; above it it is unstable at `q = 0` — a uniform runaway, not a Turing pattern. `F_max` was
set to **0.62**, just below the upper edge, so no part of the bud sits in the uniform-instability
regime. `F_decay = 4` (vs the published square-domain value of 3) makes the permissive band about
one wavelength deep, which is what gives a single proximodistal row of elements rather than two.

---

## 3. The design sweeps

Wild type: **5, 4, 5, 4, 4, 3** elements over 6 fixed seeds = **4.2 ± 0.7**
(5.3 ± 0.9 under the original counting rule — see §5).

| knob | values → mean element count | reading |
|---|---|---|
| **diffusion scale** (λ ∝ √scale) | 0.25→9.0, 0.4→6.7, 0.6→6.0, 0.8→5.7, **1.0→4.7**, 1.5→3.3, 2.0→3.0 | shorter wavelength → **more, thinner** elements. This is the Sheth et al. direction. |
| **Fgf strength `kF`** | 0.30→7.7, 0.45→6.0, 0.60→5.3, **0.667→4.7**, 0.80→3.3, 0.95→3.7 | monotone down to kF ≈ 0.8, then flat/noisy. |
| **domain scale** (whole paddle) | 0.05→0, 0.08→0, 0.10→0, 0.12→0, 0.16→0, 0.20→0.3, 0.25→1.0, 0.30→1.3, 0.40→2.0, 0.50→2.3, 0.65→3.0, 0.80→3.3, **1.0→4.7**, 1.25→6.3 | count ≈ AP width / λ, down to zero. |
| **Bmp–Sox9 coupling, balanced** (`k2` and `alpha_W` scaled together) | 0.5→3.3, 0.7→2.7, 0.85→4.3, **1.0→4.7**, 1.5→6.0, 2.0→6.3, 3.0→7.7, 4.0→1.7, 5.0→**0**, 5.5→0, 6.0→0, 7.0→0 | **the criticality knob**; see below. |
| `k2` alone | 0.5→1, 0.85→1, **1.0→4.7**, 1.5→1, 3.0→1, 6.0→0 | *confounded* — see §6. |
| `alpha_W` alone | 0.6→1, 0.8→1, **1.0→4.7**, 1.3→1, 1.6→1 | *confounded* — see §6. |

### Critical domain size

**0.94 ± 0.10 wavelengths** of anteroposterior width (**0.44 ± 0.05** under the original counting
rule). At that point the proximodistal extent is 0.67 wavelengths. Both numbers are in the JSON;
**quote the range, not one end of it.**

Because the Fgf gradient scales with the bud, the permissive band shrinks with it, so both axes
run out together.

### One condition behind every route to zero

All three routes turn out to be the same geometric condition: **the Turing-permissive region must
be at least about one wavelength across.**

- *Domain route*: elements disappear below ≈ 0.9 λ of AP width.
- *Coupling route*: at coupling ×5 the LSA still reports a Turing instability (max growth +0.31
  per time unit) but the simulation forms **nothing** — because at that coupling the window has
  narrowed to F ∈ (0.596, 1.0), and with `F_max = 0.62`, `F = F_max·exp(−4·x̂)` and `L_PD = 300`
  the permissive strip is only about **3.0 model units deep against a wavelength of 18.6** — under
  a fifth of a wavelength, and narrower than one grid cell. At coupling ×4 the strip is ≈ 13.7
  units against λ = 24.9 (≈ 0.55 λ) and the counts are correspondingly marginal and seed-dependent
  (1, 3, 1).

So the simulated loss of pattern (×5) arrives **before** the formal loss of linear instability
(×5.5, where max Re σ goes negative). Both are reported; the simulated one is what would be
observable.

---

## 4. Seed spread, refinement, controls

**Seed spread.** Every sweep point is run from 3 fixed seeds (11, 23, 37); wild type from 6
(+51, 67, 83). The individual counts, not just the mean, are in `digit-turing.json`. Wild type
spans **3 to 5** elements across its six seeds. Turing patterns are seed-dependent and the spread
is the honest error bar.

**Refinement.**

| condition | dx 4.0 → 2.667 | dt 0.01 → 0.0025 |
|---|---|---|
| wild type | [5, 4] → [4, 4] | [5, 4] → [5, 4] |
| diffusion ×0.6 | [6, 6] → [5, 5] | [6, 6] → [6, 6] |
| domain ×0.3 | [1, 2] → [1, 1] | [1, 2] → [1, 2] |

**The dt arm changes nothing. The grid arm changes the count by 1 in all three conditions** — a
real and reported limitation, and the same one-element resolution that the minimum-size cut
produces. Separately, **dt = 0.02 was measured to be numerically unstable** (diverged to ~1e8);
dt = 0.01, 0.005 and 0.002 agree on the final field to 5 significant figures.

**Controls.**

- *No reaction* (couplings zeroed, diffusion/production/decay left in): amplitude **0.0386**,
  below the 0.05 gate, **0 elements**. Passes — this is the real flatness control.
- *Counter positive + negative control*: 4.17 mean on wild type, 0 on the no-reaction field.
  Passes.
- *Per-step noise* instead of a single t = 0 perturbation: counts [4, 4, 5] against [5, 4, 5] on
  the same seeds. No material change.
- *No initial perturbation*: **FAILED, and the failure is informative rather than fatal.** The
  field was started at the exact homogeneous steady state (verified analytically: all three time
  derivatives vanish at every point, whatever the local Fgf level) and it still patterned,
  amplitude 5.22. The state is linearly unstable with growth rate 8.18 per time unit over a
  60-unit run, so double-precision rounding at 1e-16 is amplified by roughly exp(490) and
  saturates. **A linearly unstable state cannot be held flat numerically**, so this arm cannot
  test what it was designed to test. What it does establish is the converse: the pattern is not an
  artifact of the injected noise, because it forms without any.

---

## 5. A counting rule I changed after the first run, and both sets of numbers

The element counter was declared **before** any sweep was run:

1. **Amplitude gate** — `p99(S) − p1(S) < 0.05`, or `p99(S) ≤ 0` → unpatterned, class `none`.
2. **Threshold** — Sox9-high = `{S > 0.25·p99(S)}`. The steady state is `S* = 0` by construction,
   so the threshold is referenced to a known baseline and the unpatterned background can never be
   counted.
3. **Minimum size** — 4-connected components with area ≥ `0.10·λ²`.
4. **Class** — 0 → `none`; 1 → `single element`, or `single fused domain` if that one component
   spans > 70% of the AP width; 2–4 → `reduced`; 5 → `normal digit number`; ≥ 6 → `increased
   (polydactyl-like)`.

**Step 3 originally used `lambda_lin` and I changed it to `lambda_meas` after the first full run.**
The reason is a defect in the specification, not a result I disliked: the linear wavelength is
about half the wavelength the saturated pattern actually has (§2), so `0.10·lambda_lin²` is four
times too small in area and admits slivers at the anterior and posterior ends of the band. The
revised scale is `lambda_meas_WT · lambda_lin(condition) / lambda_lin(WT)` — it uses the wild-type
measurement plus analytic ratios, and **never a measurement from the run being counted**.

**Every count under the original rule is kept**, as `element_counts_linear_rule` in each sweep row.
Wild type: **[5, 7, 6, 5, 5, 4]** (mean 5.33) original, **[5, 4, 5, 4, 4, 3]** (mean 4.17) revised.
The shape of every sweep is the same under both; the critical domain size moves by a factor ≈ 2.

**Treat one element as the resolution of this measurement.** The outermost condensations sit where
the paddle narrows and are genuinely smaller, so whether they count is a judgement call, and the
grid-refinement arm moves the count by the same one element.

---

## 6. What is wrong with this model, stated plainly

- **No growth.** The real limb bud grows while it patterns, and both published simulations run on
  growing meshes. On a static domain the elements form as condensations in a distal band rather
  than elongating into proximodistally running digit rays. **This study measures element NUMBER,
  not element SHAPE.** Do not read the shapes as digit morphology.
- **The five-element wild type is imposed, not predicted.** The paddle width was chosen to give
  about five elements. Only the *changes* across the sweeps are model predictions.
- **The assumed operating point is fragile.** Because `S* = 0` was obtained by balancing
  `k2·alpha_B/k5` against `k3·alpha_W/k9`, any change that breaks that balance moves `S*` off zero
  and switches the cubic damping back on. A 20% change in `alpha_W` alone, or a 15% change in `k2`
  alone, collapses the five-element pattern to a single fused domain. That is why the `k2`-alone
  and `alpha_W`-alone sweeps are flat at 1: they are **confounded** and are reported as such.
  `bmp_sox9_coupling_balanced` scales `k2` and `alpha_W` together, which leaves the balance — and
  therefore `S* = 0`, verified at every value — exactly intact; **that is the sweep to read for
  criticality.** The fragility is a property of my reparameterisation, not a claim about the
  published model.
- **The mouse parameter set was not obtainable.** The numbers are from a catshark fin simulation
  of the same network, and one of them had to be changed to get a Turing instability at all.
- **All lengths are model length units.** The model as published carries no physical length scale
  I can verify, so **no result here is in micrometres** and no statement is made about the real
  size of any limb bud.
- **One noise model, one domain shape, one gradient shape.** Element counts are sensitive to all
  three.
- The grid-refinement arm changes the count by 1; the counting rule changes it by about 1.

---

## 7. What this does NOT establish

- **It does not establish that any real limbless or limb-reduced animal, or any real mutant, lacks
  limbs because of a change in a Turing wavelength or a sub-critical patterning system.** No
  animal was measured here. This is a demonstration that the limbless phenotype is *reachable in a
  model of the pattern-forming system*, which is a statement about the model.
- It does not establish that the BSW network is the correct mechanism of mouse digit patterning.
  That is Raspopovic et al.'s claim, read here at **abstract level only**.
- It does not reproduce any published figure. No comparison to published data was made, so no
  agreement with data is claimed.
- **A simulated phenotype class is not a phenotype.** "normal digit number" here means "five
  counted components in this simulation".

---

## 8. An earlier snapshot of these files is in circulation — check which one you have

A copy of this directory taken between **12:33 and 13:24 on 2026-11-01** was integrated
downstream before the study was finished. It differs from the current files in ways that are
substantive, not cosmetic, so **re-copy all six deliverables rather than only `NOTES.md`.**
Tell them apart by `critical_domain_size.value`: **null = stale, 0.9377 = current.**

| | stale snapshot | current |
|---|---|---|
| `critical_domain_size.value` | `null` | **0.9377 ± 0.0987 wavelengths** |
| smallest domain scale swept | 0.12× (still produced an element, so the sweep never reached zero) | 0.05× |
| element outlines in the figures | **drawn in the wrong place** — a transposed `imshow` extent put the lime contours off the paddle | correct |
| panels in the series figure | each auto-scaled, so a smaller bud did not look smaller | one shared spatial scale |
| series sequence | 8 → 5 → 3 → 2 → 1 → 1 → 0 | **7 → 5 → 3 → 2 → 1 → 0 → 0** |
| sub-critical panel | `k2 = 6` alone — a confounded knob (§6) | Bmp–Sox9 coupling ×6, operating point held |
| criticality sweep | absent | `bmp_sox9_coupling_balanced` |
| minimum element size | `0.10·lambda_lin²` | `0.10·lambda_meas²`, with both sets of counts kept (§5) |
| `NOTES.md` | did not exist yet | this file |

**Why the critical size was genuinely unresolved in the stale copy and is resolved now.** It was
not an unfilled field. In that version the smallest bud swept was 0.12×, which still produced an
element, so the sweep never crossed zero and the midpoint was undefined — `null` was the correct
answer *for that sweep*. Resolving it needed two changes: adding the 0.05×, 0.08× and 0.10×
points so the curve actually reaches zero, and defining the threshold on a mean count of exactly
zero rather than on a modal phenotype class. So **the number is derivable and is now in the
file** — with the caveat from §3 that it moves by about a factor of two with the counting rule
(0.94 ± 0.10 revised, 0.44 ± 0.05 original). Quote the range.

**The headline string on the page needs updating**: the sequence is now
**7 → 5 → 3 → 2 → 1 → 0 → 0**, not 8 → 5 → 3 → 2 → 1 → 1 → 0. Two panels changed: the shortest-
wavelength panel reads 7 rather than 8, and the truncated bud (0.16×) reads 0 rather than 1,
because the larger minimum element size no longer counts a partial condensation in a bud too
small to hold a whole one. The argument is unchanged and slightly cleaner — the truncated bud
and the sub-critical network now both reach zero by different routes.

---

## 9. Running it

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 digit_turing.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 digit_turing.py --figures   # redraw from cache
```

Measured on this shared 8-core host: **179 simulations on 5 worker processes, 437 s to the end of
the sweeps, 488 s in total** including figures and the movie. Redrawing from the cached results
takes about 52 s. Run under
`systemd-run --user --scope -p MemoryMax=6G -p MemorySwapMax=0 -p TasksMax=256`. Fully
deterministic: all seeds are fixed and recorded in the JSON.
