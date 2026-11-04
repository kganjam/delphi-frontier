# Biological design laws: a catalogue for checking designs against

Status: **seed content for the design library.** It is a literature catalogue. No experiment was run
and no data were fitted for it. The only computing done was the arithmetic in the worked examples,
which is shown in full.

Compiled 2026-11-04. Citations were checked against Crossref and Europe PMC records, and against
full text where the network allowed it. The access limits are in §0.3.

---

## 0. How to read this document

### 0.1 Provenance labels (CONTRIBUTING-VERIFICATION.md rules 3 and 9)

Every source carries a **read-level** stating what was retrieved *in this session*:

| read-level | meaning |
|---|---|
| `full-text` | the paper text was fetched and read |
| `full-text (preprint)` | an arXiv preprint was read, not the version of record |
| `abstract` | only the abstract was retrieved |
| `metadata` | only the bibliographic record (title, journal, volume, pages, DOI) was confirmed |
| `remembered` | not retrieved this session. It is cited from memory and must be checked before anyone leans on it |

Every **number** carries one claim label:

- **[R]** retrieved: quoted or read from a source at the read-level given.
- **[M]** remembered: from memory and not retrieved.
- **[D]** derived: computed here from other quantities. The arithmetic is shown, and the inputs keep their own labels.

A number marked [M] is a lead, not a fact. Several plausible-sounding [M] values were checked during
compilation and turned out wrong (see §0.2). Treat the rest of the [M] values with the same suspicion.

### 0.2 Corrections found during compilation

Each of these was a common belief, or a value in the brief, that the retrieved source contradicts.

1. **White & Seymour 2003 does not say "mammal BMR exponent 0.67, n = 619."** Across all 619 species
   without correction the exponent is **0.69**, and its 95% CI *excludes both 2/3 and 3/4* [R]. The
   2/3-compatible value (0.68) appears only after temperature correction, on 469 species [R].
2. **The DeLong et al. 2010 exponents are 1.7/2.0 (prokaryotes), 1.0/1.1 (protists) and 0.76/0.79
   (metazoans), each pair being active/inactive** [R]. The values ~1.96/1.06/0.79 in circulation are not in
   the text that was retrieved.
3. **Murray 1926 Part II (PNAS 12:299) is about oxygen exchange in capillaries, not branching angles.**
   The angle paper is in *J Gen Physiol* 9:835 [R metadata].
4. **The Huo & Kassab 2012 exponent of 2.33 is a flow–diameter exponent for whole stem–crown trees.**
   It is not a radius exponent at a single bifurcation, and the paper never writes "7/3" [R].
5. **The Frost 1987 mechanostat thresholds in the retrieved abstract are 1500–3000 µε (bone gain) and
   100–300 µε (bone loss)** [R]. The values "50–200" and "3000 µε microdamage" are not in it.
6. **Sato et al. 2009's "41 kg" is a limit for albatross-like *soaring* animals.** Its 95% CI is
   26–75 kg [R]. It is not a general limit on powered flight.
7. **The sunflower "1 in 5 non-Fibonacci" figure counts parastichy numbers: 136/768 = 18%.** It does
   not count flower heads (657 heads) [R].
8. **Strouhal conventions differ by a factor of 2.** One is St = fA/U with A the *peak-to-peak*
   amplitude; the other is St = 2fA/U with A the *semi-amplitude* (Usherwood 2025) [R]. The numbers
   agree only once the convention is fixed. See §4.2.
9. **Lighthill elongated-body theory fails for very elongate bodies (h/L < 0.1, eels and knifefish).**
   This contradicts the intuition that slender-body theory suits eels best (Eloy 2012) [R preprint].
10. **The Taylor, Heglund & Maloiy 1982 coefficient 10.7 is in J kg⁻¹ m⁻¹.** It is not in ml O₂ kg⁻¹ km⁻¹ [R].
11. **Wrong references in circulation, now corrected below:** Day & Taylor 1997 is doi 10.1086/285995.
    Facchetti et al. 2019 (cell-size variability) is in *Biophys J* 117:1728, not *Curr Biol*.
    Alexander 2005 is in *J Exp Biol* 208:1645, not *Integr Comp Biol*. Saadat et al. 2017 is titled
    "On the rules for aquatic locomotion". Pennycuick 1969 (Ibis) is doi 10.1111/j.1474-919x.1969.tb02566.x.
    Nelson, West & Goldberger 1990 is doi 10.1007/BF01951755. WBE 1999 "fourth dimension" is
    *Science* 284:1677; *Nature* 400:664 is a different WBE paper (plant vascular systems).
    Several DOIs reconstructed from memory resolved to unrelated papers. **Do not trust DOIs from memory.**

### 0.3 Access limits (why so many sources are `abstract` or `metadata`)

The session's network policy allowed only Crossref, the Europe PMC REST API, NCBI E-utilities, arXiv
PDFs and PMC HTML. Publisher hosts were blocked or paywalled: nature.com, cambridge.org,
journals.biologists.com, pnas.org, Wiley, Springer, rupress.org and royalsocietypublishing.org.

As a result, **almost every pre-2000 paper here (Kleiber, Murray, McMahon, Lighthill, Weis-Fogh,
Turing, Pennycuick 1968) is at `metadata` or `abstract` level.** Their equations are cited as
[M] textbook results. Upgrading those read-levels is the first job for whoever extends this file
(§9).

### 0.4 Field structure for each law

**Equation** (all symbols and units) · **Value** (with CI where reported) · **Mechanism** ·
**Domain** · **Breaks** · **Worked example** · **Sources** (with read-level).

---

## 1. Metabolic and allometric laws

### 1.1 Huxley allometry (the template for everything in §1)

- **Equation.** y = a·xᵇ, or log y = log a + b·log x.
  - x: a reference size, usually body mass M (kg or g).
  - y: a trait, in its own units.
  - a: the normalisation, in units of y·x⁻ᵇ.
  - b: the dimensionless allometric exponent.
  - b = 1 is isometry. Under geometric similarity, a length scales as M^{1/3} and an area as M^{2/3}.
- **Value.** None. This is a form, not a law; b is fitted case by case.
- **Mechanism.** Huxley's model treated relative growth as each part growing at a rate proportional to
  whole-body growth. That gives d ln y / d ln x = b, constant. The power form is the solution of that
  assumption; it is not a derived physical result [M].
- **Domain.** Ontogenetic (within an individual's growth), static (among adults of one species) and
  evolutionary (among species). These are different exponents and must not be pooled [M].
- **Breaks.**
  1. Curvature in log–log space. Mammal BMR is the documented case (§1.3, Kolokotrones et al. 2010) [R abstract].
  2. Breakpoints. Huxley's own *Uca pugnax* chela "break" was argued by Packard (2012) to be "an artifact
     caused by logarithmic transformation" [R abstract]. That paper was contested by Geraert 2013 [metadata].
  3. Statistics. Fitting by OLS, RMA or major-axis regression on logged data gives different b. Fitting on
     log scale also changes the error model.
- **Worked example.** Wing span against body mass in procellariiform seabirds (Sato et al. 2009, 22
  birds of 4 species, major-axis fit) [R full-text]:
  - span ∝ M^**0.37** (95% CI 0.34–0.40), where isometry predicts 1/3 (P = 0.03).
  - wing area ∝ M^**0.58** (95% CI 0.53–0.62), where isometry predicts 2/3 (P = 0.001).
  - So wing loading M/S ∝ M^{1 − 0.58} = M^**0.42** [D]. Isometry predicts M^{1/3}, so large seabirds are
    more heavily wing-loaded than scaled-up small ones.
  - The exponents do not add like that for their CIs. 0.42 is a point derivation; the paper does not
    state it.
- **Sources.**
  - Huxley JS 1932, *Problems of Relative Growth*, Methuen — `remembered`.
  - Huxley JS, Teissier G 1936, Terminology of relative growth, *Nature* 137:780–781,
    doi 10.1038/137780b0 — `metadata`. A secondary source (Stevens 2009, *J Biol*, PMC2687774,
    `full-text`) confirms Huxley "did not coin 'allometry' until 1936".
  - Packard GC 2012, Julian Huxley, *Uca pugnax* and the allometric method, *J Exp Biol* 215:569–573,
    doi 10.1242/jeb.061739 — `abstract`.
  - **No primary support was found for the widely quoted "*Uca* chela exponent ≈ 1.6".** Secondary
    values of 1.356 and 1.57 conflict. Do not use any of them.

### 1.2 Rubner's surface law

- **Equation.** B = c·S, with S ∝ M^{2/3}, so B ∝ M^{2/3}.
  - B: resting metabolic rate (W).
  - S: body surface area (m²).
  - c: heat flux per area (W m⁻²).
- **Value.** Exponent 2/3 by geometry [D].
- **Mechanism.** A homeotherm at rest in steady state must replace the heat it loses. Heat loss scales
  with surface area. For geometrically similar bodies, area scales as length², and mass as length³, so
  S ∝ M^{2/3} [D].
- **Domain.** Rubner's data were dogs of different sizes, i.e. within one species [M]. Priority is
  usually given to Sarrus & Rameaux 1839 [M].
- **Breaks.**
  1. Ectotherms, plants and unicells. They do not thermoregulate metabolically, so the mechanism does
     not apply, and their exponents are not 2/3 (§1.3, DeLong et al.).
  2. Bodies are not geometrically similar, and insulation and posture vary.
  3. Interspecifically the issue is contested (§1.3). Kleiber's re-analysis displaced 2/3 for decades,
     and White & Seymour later argued for it again.
- **Worked example.** Over a 10-fold mass range, surface rises by 10^{2/3} = 4.64× [D]. Mass-specific
  heat loss therefore falls to 4.64/10 = 0.46× [D].
- **Sources.**
  - Rubner M 1883, *Z Biol* 19:535 — `remembered`.
  - Sarrus & Rameaux 1839, *Bull Acad R Méd* 3:1094 — `remembered`.

### 1.3 Kleiber's law, the West–Brown–Enquist derivation, and the 2/3 vs 3/4 dispute

This section presents both sides and **does not resolve them.** The disagreement is about data,
statistics and mechanism at the same time.

- **Equation.** B = B₀·M^α.
  - B: basal or standard metabolic rate (W, kcal d⁻¹ or ml O₂ h⁻¹).
  - M: body mass (kg or g).
  - B₀: normalisation, in units of B·M^{−α}. It depends on temperature, taxon and metabolic state.
  - α: dimensionless exponent.
- **Value: the claims.**

  | Claim | α | Data | Source |
  |---|---|---|---|
  | Kleiber's original | ≈0.74 [M] | | Kleiber 1932 |
  | Kleiber's later value | 3/4 [M] | | Kleiber 1947 |
  | Kleiber's data re-fitted | 0.738 ± 0.016 | 13 points, 0.15–679 kg | Dodds et al. 2001 [R preprint] |
  | Same data, <10 kg | 0.667 ± 0.043 | | Dodds et al. 2001 [R preprint] |
  | Same data, >10 kg | 0.754 ± 0.048 | | Dodds et al. 2001 [R preprint] |

  White & Seymour 2003 note that Kleiber's set is "13 data points derived from eight species" [R].

  **3/4 side**
  - WBE 1997 derive exactly 3/4 (mechanism below).
  - Savage et al. 2004 report BMR exponents "whose confidence intervals include 3/4 and exclude 2/3".
    This comes from a search snippet of the abstract; the paper's own value and CI were **not** retrieved.
    The often-quoted "0.737" is [M].

  **2/3 side**
  - Dodds, Rothman & Weitz 2001 find "little evidence for rejecting α = 2/3 in favor of α = 3/4" [R].
    - Heusner's data, mammals ≤10 kg: α = **0.668**, 95% CI 0.643–0.693, n = 357 [R preprint, Table I].
    - Same data, all masses: α = 0.710, 95% CI 0.689–0.731, n = 391 [R].
    - Birds (Bennett & Harvey data): α = 0.666 ± 0.013, n = 398 [R].
    - Brody's 67 mammals give 0.73 ± 0.01. With 32 artificial points removed, 35 animals give 0.72 ± 0.02 [R].
  - White & Seymour 2003, 619 species and 19 orders, BMR in ml O₂ h⁻¹, M in g.
    - Uncorrected: α = 0.69, and its 95% CI **excludes both 2/3 and 3/4** [R].
    - After correction to 36.2 °C (Q₁₀ = 3.0), 469 species: interspecific 0.68 and interordinal 0.65.
      Both are significantly different from 3/4 and not from 2/3 [R].

  **Neither side**
  - Glazier 2005: "the '3/4-power scaling law' of metabolic rate is not universal, either within or
    among animal species" [R abstract]. Intraspecific exponents fall into types with b < 1, b = 1, and
    shifts with ontogeny.
  - Glazier 2010: the metabolic-level boundaries hypothesis "correctly predicts that the scaling slope
    should vary mostly between 2/3 and 1", in a U-shaped relation to activity level [R abstract].
    The hypothesis was already proposed in the 2005 abstract [R].
  - Kolokotrones et al. 2010: the mammal log–log relation "has convex curvature… not a pure power law,
    even after accounting for body temperature". The vascular-network model "fails this test" [R abstract].
  - DeLong et al. 2010, ectotherm data, RMA fits, each pair active/inactive [R]:

    | Group | α | Species (active / inactive) |
    |---|---|---|
    | Prokaryotes | 1.7 / 2.0 | 44 / 121 |
    | Protists | 1.0 / 1.1 | 51 / 52 |
    | Metazoans | 0.76 / 0.79 | 71 / 15 |

- **Mechanism, WBE 1997** [R abstract for assumptions; details M].
  - Resources move through "space-filling fractal networks of branching tubes". The model "assumes that
    the energy dissipated is minimized and that the terminal tubes do not vary with body size".
  - From these assumptions the 3/4 law follows, along with predicted cardiovascular, respiratory, plant
    vascular and insect tracheal scalings. Examples are aorta radius ∝ M^{3/8} and heart rate ∝ M^{−1/4} [M].
  - Related derivations:
    - Banavar, Maritan & Rinaldo 1999 obtain the bound from network geometry alone, "irrespective of
      dynamical or geometric assumptions" [R abstract].
    - Etienne, Apol & Olff 2006 obtain the WBE exponent with weaker assumptions, and "self-similarity of
      the network is not required" [R abstract].
- **Mechanism, the criticisms.**
  1. *Statistics.* Exponents near 3/4 depend on which species, how many large-bodied animals, and how
     temperature and non-basal measurements are handled (Dodds; White & Seymour; the figures above).
  2. *Mathematics and assumptions.* Kozłowski & Konarzewski 2004 argue the WBE model is internally
     inconsistent: size-invariant terminal units and the claimed blood-volume scaling cannot both hold
     as stated [M; the paper is at `metadata` level, so its argument is from memory].
     Brown, West & Enquist 2005 reply "Yes, West, Brown and Enquist's model… is both mathematically
     correct and biologically relevant" [R title].
  3. *Empirics.* Curvature (Kolokotrones), variation 2/3–1 (Glazier), and super-linear unicells (DeLong)
     are hard to reconcile with one universal exponent.
- **Domain.** Interspecific comparisons of resting rates in endotherms (mammals and birds). Each
  exponent holds only for the dataset, taxon, temperature correction and regression method it was
  fitted with.
- **Breaks.** These are measured failures, not open questions:
  1. Prokaryotes and protists (α ≈ 1–2, DeLong) [R].
  2. Intraspecific and ontogenetic scaling (Glazier 2005) [R].
  3. Active or maximal metabolism, whose exponents are higher (Glazier 2010) [R].
  4. The largest mammals: Dodds' >10 kg split, and Kolokotrones' curvature [R].
- **Worked example: why the dispute matters to a design check.** Take a 25 g mouse and a 4000 kg
  elephant, a mass ratio of 160,000 [D].
  - Under α = 3/4, the elephant's BMR is 160,000^{0.75} = **8,000×** the mouse's [D].
  - Under α = 2/3, it is 160,000^{0.667} = **2,947×** [D].
  - The two exponents disagree by a factor of **2.7** at the extremes. That is larger than most design
    margins.
  - With the often-quoted Kleiber normalisation B = 70·M^{0.75} kcal d⁻¹ (M in kg) — **this constant is
    [M]; no source for it was retrieved**:
    - mouse: 70 × 0.025^{0.75} = 70 × 0.0629 = **4.4 kcal d⁻¹** [D from M].
    - elephant: 70 × 4000^{0.75} = 70 × 503 = **35,200 kcal d⁻¹** [D from M].
- **Sources.**
  - Kleiber M 1932, Body size and metabolism, *Hilgardia* 6:315–353, doi 10.3733/hilg.v06n11p315 — `metadata`.
  - Kleiber M 1947, Body size and metabolic rate, *Physiol Rev* 27:511–541,
    doi 10.1152/physrev.1947.27.4.511 — `metadata`.
  - West GB, Brown JH, Enquist BJ 1997, A general model for the origin of allometric scaling laws in
    biology, *Science* 276:122–126, doi 10.1126/science.276.5309.122 — `abstract`.
  - Dodds PS, Rothman DH, Weitz JS 2001, Re-examination of the "3/4-law" of metabolism,
    *J Theor Biol* 209:9–27, doi 10.1006/jtbi.2000.2238 — `full-text (preprint)` arXiv physics/0007096v1, plus journal abstract.
  - White CR, Seymour RS 2003, Mammalian basal metabolic rate is proportional to body mass^{2/3},
    *PNAS* 100:4046–4049, doi 10.1073/pnas.0436428100, PMC153045 — `full-text`. Quotes were extracted by a
    summariser and not string-matched; re-check them before reuse.
  - Kozłowski J, Konarzewski M 2004, *Funct Ecol* 18:283–289, doi 10.1111/j.0269-8463.2004.00830.x — `metadata`.
  - Brown JH, West GB, Enquist BJ 2005, *Funct Ecol* 19:735–738, doi 10.1111/j.1365-2435.2005.01022.x — `metadata`.
  - Savage VM et al. 2004, The predominance of quarter-power scaling in biology, *Funct Ecol* 18:257–282,
    doi 10.1111/j.0269-8463.2004.00856.x — `metadata`.
  - Glazier DS 2005, *Biol Rev* 80:611–662, doi 10.1017/S1464793105006834 — `abstract`.
  - Glazier DS 2010, *Biol Rev* 85:111–138, doi 10.1111/j.1469-185X.2009.00095.x — `abstract`.
  - Banavar JR, Maritan A, Rinaldo A 1999, *Nature* 399:130–132, doi 10.1038/20144 — `abstract`.
  - Etienne RS, Apol MEF, Olff H 2006, *Funct Ecol* 20:394–399, doi 10.1111/j.1365-2435.2006.01136.x — `abstract`.
  - Kolokotrones T, Savage V, Deeds EJ, Fontana W 2010, Curvature in metabolic scaling,
    *Nature* 464:753–756, doi 10.1038/nature08920 — `abstract`.
  - DeLong JP, Okie JG, Moses ME, Sibly RM, Brown JH 2010, *PNAS* 107:12941–12945,
    doi 10.1073/pnas.1007783107, PMC2919978 — `full-text` (summariser-extracted; re-check).

---

## 2. Transport networks

### 2.1 Hagen–Poiseuille

- **Equation.** ΔP = 8μLQ/(πr⁴). Equivalently, hydraulic resistance R_h = 8μL/(πr⁴).
  - ΔP: pressure drop (Pa).
  - μ: dynamic viscosity (Pa s).
  - L: tube length (m).
  - Q: volume flow rate (m³ s⁻¹).
  - r: tube radius (m).
- **Value.** Exact under its assumptions. The r⁴ dependence is the load-bearing feature: halving the
  radius raises resistance 16× [D].
- **Mechanism.** The exact solution of the Navier–Stokes equations for steady, fully developed, laminar
  flow of a Newtonian fluid in a rigid circular tube with no-slip walls. The velocity profile is
  parabolic [M, textbook].
- **Domain.** Re ≲ 2000; Newtonian fluid; steady flow; entrance length small compared with L; rigid
  walls [M].
- **Breaks.**
  1. **Blood in small tubes.** Apparent viscosity depends on diameter (the Fåhræus–Lindqvist effect),
     with "a distinctive minimum at 6–7 µm" in glass tubes. Resistance in vivo exceeds the in vitro
     value, partly because of an endothelial surface layer "approximately 0.8–1 µm" thick in
     10–40 µm vessels (Pries & Secomb 2005) [R abstract].
     - Pries et al. 1992 measured tubes of 3.3–1,978 µm [R abstract].
     - The effect becomes appreciable below roughly 0.3 mm diameter [R, secondary: Farina et al. 2021 abstract].
  2. **Large arteries.** Flow there is pulsatile: "Poiseuille's law does not hold for the arterial
     system in vivo, because of the pulsat[ility]" (Reneman & Hoeks 2008) [R full-text].
  3. **Compliant walls, bends and entrance regions** [M].
- **Worked example: human aorta.** The inputs are [M]: r = 1.25 cm, ρ = 1060 kg m⁻³, μ = 3.5 mPa s,
  heart rate 1.2 Hz.
  - Mean flow (U = 0.2 m s⁻¹): Re = ρU(2r)/μ = 1060 × 0.2 × 0.025 / 0.0035 = **1,514** [D].
  - Peak systole (U = 1.0 m s⁻¹): Re = **7,570** [D], above the laminar threshold.
  - Womersley number α_W = r·√(ωρ/μ), with ω = 2π × 1.2 = 7.54 s⁻¹:
    √(7.54 × 1060 / 0.0035) = √(2.28 × 10⁶) = 1,511, and 0.0125 × 1,511 = **18.9** [D].
  - α_W ≫ 1 means the velocity profile is blunt and inertia-dominated, not parabolic. Poiseuille's
    assumptions fail in this vessel.
- **Sources.**
  - Pries AR, Neuhaus D, Gaehtgens P 1992, Blood viscosity in tube flow: dependence on diameter and
    hematocrit, *Am J Physiol* 263:H1770–H1778, doi 10.1152/ajpheart.1992.263.6.H1770 — `abstract`.
  - Pries AR, Secomb TW 2005, *Am J Physiol Heart Circ Physiol* 289:H2657–H2664,
    doi 10.1152/ajpheart.00297.2005 — `abstract`.
  - Reneman RS, Hoeks AP 2008, *Med Biol Eng Comput* 46:499–507, doi 10.1007/s11517-008-0330-2,
    PMC2441533 — `full-text`.
  - Fåhræus R, Lindqvist T 1931, *Am J Physiol* 96:562–568 — `remembered` (the citation was seen in two abstracts; not read).

### 2.2 Murray's law (minimum work) and its generalisation r_p^n = Σ r_c^n

- **Equation.**
  - Murray: r_p³ = Σ r_c³. Here r_p is the parent radius (m) and r_c are the daughter radii (m).
  - Equivalent statement: Q ∝ r³ in every segment.
  - Generalised (Hess–Murray form): r_p^n = Σ r_c^n, or Q ∝ r^n, with n fitted.
- **Mechanism.** Minimise the total power to run a segment of length L carrying flow Q:
  P(r) = 8μLQ²/(πr⁴) + b·πr²L.
  - The first term is viscous dissipation (Poiseuille).
  - The second is the metabolic cost of maintaining blood volume. b is a cost per unit volume per time,
    in W m⁻³.
  - Setting dP/dr = 0: −32μLQ²/(πr⁵) + 2bπrL = 0, so Q² = bπ²r⁶/(16μ), so **Q ∝ r³** [D; the cost
    function is M].
  - Conservation of mass at the junction (Q_p = ΣQ_c) then gives r_p³ = Σr_c³.
  - A corollary: wall shear stress τ = 4μQ/(πr³) is the same in every segment [D].
- **Value.** n = 3 exactly under the assumptions. Measured values:

  | System | n | Source |
  |---|---|---|
  | Coronary, pooled flow–diameter exponent | **2.39** (95% CI 2.24–2.54; I² = 99%) | meta-analysis of 18 studies, 1,070 trees, 372 humans and 112 animals (Taylor et al. 2024) [R full-text] |
  | Coronary stem–crown trees, flow–diameter | 2.33 theory vs 2.62 ± 0.65 measured | Huo & Kassab 2012 [R full-text] |
  | Coronary, volume–diameter | 2.96–3.00 | Huo & Kassab 2012 [R full-text] |
  | Epicardial bifurcations | 2.60 ± 0.64 | Zamir 1999, as tabulated by Taylor et al. 2024 [R] |
  | Pig coronary arterioles | "excellent agreement with Murray's law" | Kassab & Fung 1995 [R abstract] |
  | Aortic arch branches | "a 'square law'" (n ≈ 2) "rather than the classical cube law" | Zamir et al. 1992 [R abstract] |
  | Arterial tree overall | "possibly from 2 in larger arteries to about 3 in arterioles" | Reneman & Hoeks 2008 [R full-text] |
  | Angiosperm xylem | conforms "as long as [conduits] do not function additionally as supports" | McCulloh et al. 2003 [R abstract] |
  | Conifer wood | "rejected… where hydraulic function is coupled to mechanical support" | McCulloh et al. 2004 [R abstract] |
  | Lepidoptera wing veins | veins "above approximately 50 microns conform"; smaller ones less so (>1,000 wings, 667 species) | Schachat et al. 2021 [R full-text] |
  | Dermal lymphatic capillaries | ≈1.45 | Front Cardiovasc Med 2022 [R abstract] |

- **Domain.** Steady, laminar, Newtonian flow in a vessel that has no other function. The cost of
  maintaining the fluid must scale with volume.
- **Breaks.** This field is the reason Murray's law cannot be applied blindly.
  1. **Large arteries.** The measured exponent falls toward 2. Wall shear stress is *not* constant:
     infrarenal aortic mean wall shear stress runs "from 8.8 Pa in mice to 0.5 Pa in humans" (Reneman &
     Hoeks) [R]. Constant shear stress is the premise of Murray's law.
  2. **Turbulent or unsteady flow.** "When turbulent, unsteady flow and the rheological properties of
     blood are accounted for, an exponent between 2.0 and 3.0 is retrieved" (Taylor et al. 2024,
     citing Uylings 1977 among others) [R]. The specific turbulent value of 7/3 attributed to Uylings is [M].
  3. **Conduits that also carry mechanical load** (conifer tracheids) [R].
  4. **Diffusive rather than convective transport.** The claim that insect tracheae follow n = 2 is
     **unverified** [M], and no source was found for it.
  5. Lymphatic capillaries (n ≈ 1.45) [R].
- **Worked example: a symmetric bifurcation.** For a parent of diameter 10 mm splitting into two equal
  daughters, d_c = 10 × 2^{−1/n} [D]:
  - n = 3: 2^{−0.333} = 0.794, so d_c = **7.94 mm**.
  - n = 2.39 (pooled coronary value): 2^{−0.418} = 0.748, so d_c = **7.48 mm**.
  - n = 2 (aortic arch): d_c = **7.07 mm**. This is area-preserving.
  - A design that claims to be "Murray-optimal" can therefore be checked to within about 1 mm per
    branching at this scale. It must state which n it uses and why.
- **Sources.**
  - Murray CD 1926, The physiological principle of minimum work: I. The vascular system and the cost of
    blood volume, *PNAS* 12:207–214, doi 10.1073/pnas.12.3.207, PMC1084489 — `metadata`.
  - Murray CD 1926, … II. Oxygen exchange in capillaries, *PNAS* 12:299–304, doi 10.1073/pnas.12.5.299 — `metadata`.
  - Murray CD 1926, … applied to the angle of branching of arteries, *J Gen Physiol* 9:835–841,
    doi 10.1085/jgp.9.6.835 — `metadata`.
  - Hess WR, priority claim — `remembered`. The date is disputed between 1903 and 1914/1917 in
    secondary sources seen only as snippets, so it is not stated here.
  - Sherman TF 1981, On connecting large vessels to small: the meaning of Murray's law,
    *J Gen Physiol* 78:431–453, doi 10.1085/jgp.78.4.431, PMC2228620 — `abstract`.
  - Uylings HBM 1977, Optimization of diameters and bifurcation angles in lung and vascular tree
    structures, *Bull Math Biol* 39:509–520 — `metadata`. Crossref lists two DOIs:
    10.1016/S0092-8240(77)80054-2 and 10.1007/BF02461198.
  - Zamir M, Sinclair P, Wonnacott TH 1992, *J Biomech* 25:1303–1310, doi 10.1016/0021-9290(92)90285-9 — `abstract`.
  - Kassab GS, Fung YC 1995, *Ann Biomed Eng* 23:13–20, doi 10.1007/BF02368296 — `abstract`.
  - Huo Y, Kassab GS 2012, Intraspecific scaling laws of vascular trees, *J R Soc Interface* 9:190–200,
    doi 10.1098/rsif.2011.0270, PMC3223633 — `full-text` (summariser-relayed quotes).
  - Taylor DJ et al. 2024, Systematic review and meta-analysis of Murray's law in the coronary arterial
    circulation, *Am J Physiol Heart Circ Physiol* 327:H182–H190, doi 10.1152/ajpheart.00142.2024,
    PMC11380967 — `full-text`.
  - McCulloh KA, Sperry JS, Adler FR 2003, Water transport in plants obeys Murray's law,
    *Nature* 421:939–942, doi 10.1038/nature01444 — `abstract`.
  - McCulloh KA, Sperry JS, Adler FR 2004, Murray's law and the hydraulic vs mechanical functioning of
    wood, *Funct Ecol* 18:931–938, doi 10.1111/j.0269-8463.2004.00913.x — `abstract`.
  - Schachat SR et al. 2021, *BMC Biol*, doi 10.1186/s12915-021-01130-0, PMC8444497 — `full-text` (partial).
  - Dermal lymphatics: *Front Cardiovasc Med* 2022, doi 10.3389/fcvm.2022.840305 — `abstract`.

---

## 3. Mechanics and structure

### 3.1 Second moment of area, beam stiffness and span

- **Equations.** All are standard [M]; none is in dispute.
  - Solid circular section: I = πr⁴/4.
  - Tube: I = π(R⁴ − r_i⁴)/4.
  - I: second moment of area (m⁴). r, R: outer radius (m). r_i: inner radius (m).
  - Bending stiffness EI (N m²), with E Young's modulus (Pa).
  - End-loaded cantilever: tip deflection δ = FL³/(3EI). F: force (N); L: span (m).
  - Cantilever under its own weight: δ = qL⁴/(8EI), with q = ρgA the weight per unit length (N m⁻¹).
    For a solid round beam of diameter d, this gives δ/L ∝ ρgL³/(Ed²) [D].
- **Mechanism.** Bending strain grows linearly with distance from the neutral axis. Material far from
  the axis therefore contributes in proportion to distance squared, and a hollow tube gives the most
  stiffness per unit mass.
- **Consequence for span.** Hold the relative sag δ/L fixed with the same material. Then d² ∝ L³, so
  **d ∝ L^{3/2}** [D]. This is the same relation as McMahon's elastic similarity (§3.2).
  Scaling a beam up geometrically (d ∝ L) makes the relative sag grow ∝ L. That is why long spans in
  organisms (wing spars, necks, tree branches) are disproportionately thick or hollow.
- **Hollowness.** K is the ratio of internal to external diameter.
  - Currey & Alexander 1985: the optimum K depends on whether the bone is designed for yield/fatigue
    strength, ultimate strength, impact strength or stiffness, and on whether the cavity holds marrow
    or gas [R abstract]. No numbers were retrieved.
  - Taylor & Dirks 2012 [R full-text, secondary]: "optimum r/t value for mammals is 2 (based on
    strength) or 4 (based on stiffness)", and "most common value for land-based mammals is r/t = 2".
    Birds range 2–8.
  - If r is the outer radius, r/t = 2 corresponds to K = 0.5 [D]. That convention for r was not confirmed.
- **Worked example: a tube against a solid rod of equal mass.** Take a solid rod of radius 1. A tube
  with K = 0.5 and the same cross-sectional area has R² (1 − 0.25) = 1, so R = 1.155 [D].
  - Tube: I = π(R⁴ − (0.5R)⁴)/4 = (π/4) × 1.778 × 0.9375 = (π/4) × **1.667** [D].
  - Solid: I = (π/4) × 1.
  - At equal mass, the tube is **1.67× stiffer** in bending [D].
- **Breaks.**
  1. Thin walls buckle locally (Brazier ovalisation) before they yield [M].
  2. Bone is anisotropic and the cross-section is not circular [M].
  3. Small beams. Beam theory needs L ≫ d, and for small animals stiffness rather than strength may
     govern ("At smaller sizes, skeletal stiffness may be more critical than strength", Biewener 1990) [R].
- **Sources.**
  - Currey JD, Alexander RMcN 1985, The thickness of the walls of tubular bones, *J Zool* 206:453–468,
    doi 10.1111/j.1469-7998.1985.tb03551.x — `abstract`.
  - Taylor & Dirks 2012, *J R Soc Interface* 9:3480, doi 10.1098/rsif.2012.0567 — `full-text` via summariser.

### 3.2 Elastic vs geometric similarity (McMahon)

- **Equation.** Length l ∝ d^{2/3} (elastic similarity), so d ∝ l^{3/2}. For a body M ∝ l·d²:
  - l ∝ M^{1/4} and d ∝ M^{3/8} [D].
  - Geometric similarity, for comparison: l ∝ d ∝ M^{1/3}.
  - l: segment length (m). d: diameter (m). M: mass (kg).
- **Value.** McMahon 1973 derives forms in which "lengths increase as the (2/3) power of diameter".
  From that he obtains Kleiber's M^{3/4}, "frequencies… inversely as body weight to the (1/4) power",
  and "surface areas… (5/8) power" [R abstract].
- **Mechanism.** Every element is required to deflect, or to buckle, by the same *relative* amount
  under its own weight. This is the same algebra as §3.1.
- **Measured tests.**
  - **Mammal limb bones, 37 species from shrews to elephant:** "lengths… proportional to (body
    mass)^0.35 and the diameters to (body mass)^0.36, except in the family Bovidae in which the
    exponents for length are much nearer the value of 0.25 predicted by McMahon" (Alexander et al.
    1979) [R abstract]. That is **close to geometric similarity (0.33), not elastic similarity (0.25 /
    0.375)**, except in Bovidae.
  - **How large mammals cope instead:** "peak bone stress is independent of size (maintaining a safety
    factor of between 2 and 4)", achieved mainly through "a size-dependent change in locomotor limb
    posture" (Biewener 1989) [R abstract]. Peak stresses are "25 to 50% of their failure strength" over
    "0.1 to 300 kilograms" (Biewener 1990) [R abstract].
- **Domain.** McMahon's own supporting cases were tree trunks and ungulate (bovid) limbs [M for the
  1975 exponents, which were not retrieved].
- **Breaks.**
  1. Mammals in general (geometric, not elastic) [R].
  2. Above about 300 kg, where posture can no longer straighten further and bones become more robust [M].
  3. Small animals, where stiffness rather than strength may govern [R, Biewener 1990].
  - Elastic similarity is a *hypothesis that selection could use*. It is not an observed law of skeletons.
- **Worked example: limb bone of an animal 1,000× heavier.** Diameter grows by:
  - geometric: 1000^{0.333} = **10×** [D];
  - elastic: 1000^{0.375} = **13.3×** [D];
  - Alexander's measured exponent: 1000^{0.36} = **12.0×** [D].
  - Length grows by 10× (geometric), 1000^{0.25} = 5.6× (elastic), or 1000^{0.35} = 11.2× (measured) [D].
  - The measured length exponent is the one that rules out elastic similarity.
- **Sources.**
  - McMahon T 1973, Size and shape in biology, *Science* 179:1201–1204, doi 10.1126/science.179.4079.1201 — `abstract`.
  - McMahon TA 1975, Allometry and biomechanics: limb bones in adult ungulates, *Am Nat* 109:547–563,
    doi 10.1086/283026 — `metadata`.
  - McMahon TA, Kronauer RE 1976, Tree structures: deducing the principle of mechanical design,
    *J Theor Biol* 59:443–466, doi 10.1016/0022-5193(76)90182-X — `metadata`.
  - Alexander RMcN, Jayes AS, Maloiy GMO, Wathuta EM 1979, Allometry of the limb bones of mammals from
    shrews (*Sorex*) to elephant (*Loxodonta*), *J Zool* 189:305–314, doi 10.1111/j.1469-7998.1979.tb03964.x — `abstract`.
  - Biewener AA 1989, Scaling body support in mammals: limb posture and muscle mechanics,
    *Science* 245:45–48, doi 10.1126/science.2740914 — `abstract`.
  - Biewener AA 1990, Biomechanics of mammalian terrestrial locomotion, *Science* 250:1097–1103,
    doi 10.1126/science.2251499 — `abstract`.

### 3.3 Buckling-limited column height (Greenhill)

- **Equation.** H_crit = C·(E/(ρg))^{1/3}·D^{2/3}.
  - H_crit: the height at which a uniform vertical column buckles under its own weight (m).
  - E: Young's modulus (Pa). ρ: density (kg m⁻³). g = 9.81 m s⁻². D: basal diameter (m).
  - C: a dimensionless constant.
- **Value of C.** It was not retrieved from Greenhill. It is reconstructed here from the classical
  self-weight buckling result l_crit = (7.837·EI/(ρgA))^{1/3}, where the 7.837 coefficient is [M].
  With I/A = D²/16 for a solid circle: C = (7.837/16)^{1/3} = **0.788** [D]. This is consistent with
  the "≈0.79" usually quoted [M].
- **Mechanism.** Euler buckling under a distributed axial load (the column's own weight).
- **Measured.** Niklas 1994 studied 111 species with 0.03 cm ≤ D ≤ 3.0 m. Elastica and Greenhill
  estimates were "statistically indistinguishable", and "H_crit/H ≈ 4" [R abstract]. Plants therefore
  stand at roughly **one quarter of their buckling height**, which is a safety factor of about 4.
  McMahon 1973's similar claim for American trees was seen only in search summaries and is unverified.
- **Domain.** Self-supporting, roughly cylindrical, untapered stems. Green-wood E and ρ vary with
  density across 161 species (Niklas & Spatz 2010) [R abstract].
- **Breaks.**
  1. **The tallest trees are limited hydraulically, not mechanically.** The tallest measured tree was
     112.7 m, with a predicted "maximum tree height of 122–130 m barring mechanical damage" from
     water-transport limits (Koch et al. 2004) [R abstract]. The Greenhill limit for the same trunk is
     well above that (worked example). Buckling is therefore not the binding constraint at the top end.
  2. Tapered trunks, crown mass, wind loading (which usually dominates), and lianas and other
     non-self-supporting plants.
- **Worked example: coast redwood scale.** Inputs [M]: E = 10 GPa, ρ = 500 kg m⁻³, D = 4.84 m.
  - E/(ρg) = 10¹⁰ / (500 × 9.81) = 2.039 × 10⁶ m, and its cube root is **126.8 m^{1/3}** [D].
  - D^{2/3} = 4.84^{0.667} = **2.861 m^{2/3}** [D].
  - H_crit = 0.788 × 126.8 × 2.861 = **286 m** [D]. For D = 1 m, H_crit = **100 m** [D].
  - With assumed green-wood values (E = 8 GPa, ρ = 900 kg m⁻³), H_crit for D = 4.84 m is **218 m** [D].
  - Against a 112.7 m tree, the buckling safety factor is about 2–2.5. The hydraulic ceiling
    (122–130 m) bites first.
- **Sources.**
  - Greenhill AG 1881, Determination of the greatest height consistent with stability that a vertical
    pole or mast can be made…, *Proc Camb Philos Soc* 4:65–73 — `remembered` (no Crossref record of
    the original exists).
  - Niklas KJ 1994, Interspecific allometries of critical buckling height and actual plant height,
    *Am J Bot* 81:1275–1279, doi 10.1002/j.1537-2197.1994.tb11449.x — `abstract`.
  - Niklas KJ, Spatz H-C 2010, Worldwide correlations of mechanical properties and green wood density,
    *Am J Bot* 97:1587–1594, doi 10.3732/ajb.1000150 — `abstract`.
  - Koch GW, Sillett SC, Jennings GM, Davis SD 2004, The limits to tree height, *Nature* 428:851–854,
    doi 10.1038/nature02417 — `abstract`.

### 3.4 Wolff's law, the mechanostat, and dynamic strain similarity

- **Equation.** Wolff's law has none: as originally stated it is qualitative ("bone adapts to load").
  Frost's mechanostat gives the nearest thing to a quantitative rule, a set of strain thresholds:
  - ε below ~100–300 µε: remodelling removes bone (disuse).
  - ε above ~1500–3000 µε: modelling adds cortical bone.
  - In between: maintenance.
  - ε is peak strain, dimensionless (µε = 10⁻⁶).
- **Value.** "Strains in or above the 1500–3000 microstrain range cause bone modelling to increase
  cortical bone mass, while strains below the 100–300 microstrain range release BMU-based remodeling
  which then removes… bone" (Frost 1987, *Anat Rec*) [R abstract]. A separate ~3000 µε microdamage
  threshold is often attributed to Frost [M]; it is not in the retrieved abstract.
- **Dynamic strain similarity.**
  - Rubin & Lanyon 1984 (*J Theor Biol*) found axial force falling "from 6.9 G in a 7 kg turkey to
    2.8 G in a small (130 kg) horse… 0.8 G in a 2500 kg elephant", while peak stresses stayed
    "remarkably similar" across a 350× mass range [R abstract].
  - Peak strains of 2000–3000 µε "for all animals" [R, secondary: Life 2014 review, PMC4187165, full-text].
- **Dose–response (one species).** In Rubin & Lanyon's *J Bone Joint Surg* preparation (the species,
  turkey ulna, is [M]; the retrieved abstract excerpt did not name it), 36 loading cycles per day at 0.5 Hz raised bone mineral content to
  "133 and 143 per cent", and more cycles (up to 1800) gave no further gain [R abstract].
- **Mechanism.** Osteocytes sense strain and fluid flow. The mechanistic detail is outside this catalogue [M].
- **Breaks and critique.**
  1. Bertram & Swartz 1991 titled their critique "The 'law of bone transformation': a case of crying
     Wolff?" [R title]. Its content was not retrieved; that it argues the law is not a predictive law is [M].
  2. The thresholds shift with hormones, age and site (that is Frost's point about "nonmechanical
     agents") [R title].
  3. Strain similarity is a summary across sites and species measured with gauges at accessible
     locations [M].
- **Worked example.** If a structural element in a design sees a predicted peak working strain of
  400 µε, it sits in the maintenance band. Living bone in that situation would neither add nor remove
  mass, by Frost's retrieved numbers [D]. A design at 3,500 µε lies above the modelling threshold. It
  is also above the 2000–3000 µε peak strains measured across species, and so outside the observed
  envelope [D].
- **Sources.**
  - Wolff J 1892, *Das Gesetz der Transformation der Knochen*, Hirschwald, Berlin — `metadata` (from a reference list).
  - Frost HM 1987, Bone "mass" and the "mechanostat": a proposal, *Anat Rec* 219:1–9, doi 10.1002/ar.1092190104 — `abstract`.
  - Frost HM 1987, The mechanostat: a proposed pathogenic mechanism of osteoporoses…,
    *Bone Miner* 2:73–85, PMID 3333019 — `metadata`.
  - Rubin CT, Lanyon LE 1984, Dynamic strain similarity in vertebrates…, *J Theor Biol* 107:321–327,
    doi 10.1016/S0022-5193(84)80031-4 — `abstract` (PubMed truncates it at 250 words).
  - Rubin CT, Lanyon LE 1984, *J Bone Joint Surg Am* 66:397–402, doi 10.2106/00004623-198466030-00012 — `abstract`.
  - Bertram JEA, Swartz SM 1991, *Biol Rev* 66:245–273, doi 10.1111/j.1469-185X.1991.tb01142.x — `metadata`.

### 3.5 Ashby material-selection charts

- **Equation.** Performance index P = f(E, σ_f, ρ, …), with a different form for each loading mode
  [M, derivable]:
  - Light, stiff tie (tension): **E/ρ**.
  - Light, stiff beam (bending, section free to scale): **E^{1/2}/ρ**.
  - Light, stiff plate or panel: **E^{1/3}/ρ**.
  - Light, strong beam: σ_f^{2/3}/ρ.
  - E: modulus (Pa). σ_f: failure strength (Pa). ρ: density (kg m⁻³).
- **Mechanism.** Write the mass of the component that meets a stiffness or strength target, with the
  free geometric variable eliminated. The material properties then separate out as a single group,
  which is the index. On log–log axes, a line of constant index has slope 1, 2 or 3.
  - Derivation for a beam [D]: stiffness requires EI = E·d⁴/12 ≥ S·L³. So d ∝ (SL³/E)^{1/4}, and mass
    m = ρ·d²·L ∝ ρ·E^{−1/2}. **Minimising m means maximising E^{1/2}/ρ.**
- **Value.** Ashby et al. 1995 conclude that "many natural materials are superior to the man-made
  materials of engineering" [R abstract]. No property values were retrieved in this session.
- **Breaks.**
  1. Biological materials are anisotropic, hierarchical and hydrated, so one E per material is a
     simplification [M].
  2. The index assumes the shape can scale freely. Organisms are also constrained by growth and by
     the other functions a part serves (as with conifer xylem, §2.2).
- **Worked example.** Not given: no sourced E or ρ for bone, wood, chitin, keratin or silk was
  retrieved. The arithmetic itself is trivial, so the missing inputs, not the method, are what blocks it.
- **Sources.**
  - Ashby MF 1989, Overview No. 80: On the engineering properties of materials, *Acta Metall*
    37:1273–1293, doi 10.1016/0001-6160(89)90158-2 — `metadata`.
  - Ashby MF 1989, Materials selection in conceptual design, *Mater Sci Technol* 5:517–525,
    doi 10.1179/mst.1989.5.6.517 — `metadata`.
  - Ashby MF, Gibson LJ, Wegst U, Olive R 1995, The mechanical properties of natural materials.
    I. Material property charts, *Proc R Soc A* 450:123–140, doi 10.1098/rspa.1995.0075 — `abstract`.
  - Wegst UGK, Ashby MF 2004, The mechanical efficiency of natural materials, *Phil Mag* 84:2167–2186,
    doi 10.1080/14786430410001680935 — `metadata`.

---

## 4. Fluids and locomotion

### 4.1 Reynolds number

- **Equation.** Re = ρUL/μ = UL/ν.
  - ρ: fluid density (kg m⁻³). U: speed (m s⁻¹). L: characteristic length (m).
  - μ: dynamic viscosity (Pa s). ν = μ/ρ: kinematic viscosity (m² s⁻¹).
  - Values used here [M]: water at 20 °C, ν ≈ 1.0 × 10⁻⁶; air, ν ≈ 1.5 × 10⁻⁵.
- **Mechanism.** Re is the ratio of inertial to viscous forces. Below Re ≈ 1, flow is reversible and
  coasting is impossible (the setting of Purcell's scallop theorem, [M]). Above about 10³, inertia
  dominates and wakes, vortices and lift govern.
- **Values across organisms.**

  | Organism | U (m s⁻¹) | L (m) | Re | Status |
  |---|---|---|---|---|
  | *E. coli* | 3 × 10⁻⁵ | 2 × 10⁻⁶ | **6 × 10⁻⁵** | [D from M] |
  | Human sperm | 5 × 10⁻⁵ | 5 × 10⁻⁵ | **2.5 × 10⁻³** | [D from M] |
  | *Encarsia formosa* (wasp) | | | **10–20** | [R, Weis-Fogh 1973 abstract] |
  | *Drosophila* (wing) | ≈ 2 × Φ × R × n = 2 × 2.8 rad × 2.5 × 10⁻³ m × 200 Hz = 2.8 | chord 1 × 10⁻³ | **≈190** | [D from M]; retrieved value 100–200 (Lehmann et al. 2005 abstract) |
  | Goldfish | | | **7.1 × 10³** | [R, Eloy 2012 table] |
  | Bottlenose dolphin | | | **1.2 × 10⁷** | [R, Eloy 2012 table] |
  | Killer whale | | | **2.6 × 10⁷** | [R, Eloy 2012 table] |
  | Pigeon (wing) | 10 | chord 0.1 | **6.7 × 10⁴** | [D from M] |
  | Blue whale | 5 | 25 | **1.25 × 10⁸** | [D from M] |

  The *Drosophila* computed value agrees with the retrieved range.
- **Breaks.** Re is a regime indicator, not a law, so it does not "fail". But the choice of L (chord,
  body length or diameter) and of U (body speed or wing speed) changes the value by orders of
  magnitude. A design document must state both.
- **Sources.**
  - Purcell EM 1977, Life at low Reynolds number, *Am J Phys* 45:3–11, doi 10.1119/1.10903 — `metadata`.
  - Weis-Fogh 1973, Lehmann et al. 2005 and Eloy 2012: see §4.4 and §4.5.

### 4.2 Strouhal number and the 0.2–0.4 cruising band (load-bearing for the project)

- **Equation.** **St = f·A/U**.
  - f: tail-beat or wing-beat frequency (Hz).
  - A: amplitude (m). **In Taylor et al. 2003, Rohr & Fish 2004 and Eloy 2012, A is the *peak-to-peak*
    excursion of the tail tip or wingtip** [R: Eloy abstract, "A the peak-to-peak tail amplitude";
    Rohr & Fish use "peak-to-peak fluke amplitude"].
  - U: forward speed (m s⁻¹).
  - St is dimensionless.
  - **Convention trap:** some authors write St = 2fA/U with A the *semi*-amplitude. Usherwood 2025
    writes "St = 2fA/U, where animals are observed to cruise with St ≈ 0.2–0.4" [R]. The number is the
    same, but **mixing the convention with the wrong definition of A is a 2× error.** Every design check
    in this project must state "A = peak-to-peak" explicitly.
  - For birds, Nudds et al. 2004 use "A ≈ b·sin(θ/2)", with b wingspan and θ stroke angle [R].
- **Value.** Primary source: **Taylor, Nudds & Thomas 2003, *Nature* 425:707–711.** Verbatim abstract
  [R abstract]:

  > "Dimensionless numbers are important in biomechanics because their constancy can imply dynamic
  > similarity between systems, despite possible differences in medium or scale. A dimensionless
  > parameter that describes the tail or wing kinematics of swimming and flying animals is the Strouhal
  > number, St = fA/U, which divides stroke frequency (f) and amplitude (A) by forward speed (U). St is
  > known to govern a well-defined series of vortex growth and shedding regimes for airfoils undergoing
  > pitching and heaving motions. Propulsive efficiency is high over a narrow range of St and usually
  > peaks within the interval 0.2 < St < 0.4 (refs 3-8). Because natural selection is likely to tune
  > animals for high propulsive efficiency, we expect it to constrain the range of St that animals use.
  > This seems to be true for dolphins, sharks and bony fish, which swim at 0.2 < St < 0.4. Here we show
  > that birds, bats and insects also converge on the same narrow range of St, but only when cruising.
  > Tuning cruise kinematics to optimize St therefore seems to be a general principle of oscillatory
  > lift-based propulsion."

  **What is and is not established from this source at the read-level reached:**
  - **Retrieved:** the band 0.2 < St < 0.4; the definition St = fA/U; the restriction to *cruising*;
    the taxa (birds, bats and insects, plus dolphins, sharks and bony fish from earlier work).
  - **Not retrieved:** the species count; the fraction of species inside the band; any mean or CI; how
    "cruising" was defined in practice. A count of "42 bird, bat and insect species" circulates. The
    breakdown attached to it (22 birds + 20 bats + 2 insects) sums to 44, not 42. **Neither number is
    used here.** The paper reports no CI on the band that could be cited.
  - **The band is a *range observed to contain cruising animals*, motivated by foil experiments. It is
    not a fitted value with an error bar.**

  Supporting and refining measurements:

  | Source | Result | Status |
  |---|---|---|
  | Triantafyllou, Triantafyllou & Gopalkrishnan 1991 (foils) | thrust comes from "a reverse von Kármán street whose preferred Strouhal number is between 0.25 and 0.35, and… optimal foil efficiency is achieved within this Strouhal range" | [R abstract] |
  | Triantafyllou, Triantafyllou & Grosenbaugh 1993 | twelve species of dolphins, sharks, scombroids and other bony fishes; "most… swim in the interval 0.25 < St < 0.35" | [R via Eloy's full text; the 1993 paper itself is `metadata`] |
  | Rohr & Fish 2004, odontocetes | 248 St values from six species (*Tursiops truncatus*, *Pseudorca crassidens*, *Orcinus orca*, *Globicephala melaena*, *Lagenorhynchus obliquidens*, *Stenella frontalis*). "A greater proportion of Strouhal values occur between 0.20 and 0.30 (74%) than the 0.25–0.35 (55%) range"; "the greatest number… between 0.225 and 0.275 (44%)"; "slightly (approximately 20%) lower values than previously predicted" | [R abstract] |
  | Nudds, Taylor & Thomas 2004, 60 bird species | birds "converged on the lower end of the range 0.2 < St < 0.4"; St = 0.21 (direct fliers) and 0.25 (intermittent fliers); θ ≈ 67·b^{−0.24} (θ in degrees, b in m); f ≈ St·U/(b·sin(33.5·b^{−0.24})), "explaining 90% of the observed variance" | [R abstract] |
  | Eloy 2012, 53 species | "the optimal Strouhal number increases from 0.15 to 0.8 for animals spanning from the largest cetaceans to the smallest tadpoles"; the optimum scales as St ≈ 0.75·Li^{1/3}, where Li = (S/h²)·C_d/2 is a "Lighthill number"; "more than 85% of data points" lie in the acceptable range, defined as η > η_max − 0.1 | [R preprint] |

- **Mechanism.**
  - Wake: for heaving and pitching foils, thrust efficiency peaks where the shedding frequency matches
    the most unstable frequency of the reverse Kármán wake (Triantafyllou 1991, 1993) [R abstract/via
    Eloy]. Eloy reports that this band was obtained by "fitting the experimental results of
    Koochesfahani" [R preprint].
  - Selection: Taylor et al. argue selection tunes cruising animals to that efficient band [R].
  - Not settled: Usherwood 2025 argues "Observed Strouhal numbers for cruising animals appear too low
    for optimal mechanical efficiency" [R abstract]. The mechanism therefore remains under discussion,
    even though the observed band is robust.
- **Domain.** Cruising (steady, sustained forward) locomotion by oscillating lift-based propulsors,
  i.e. tails, flukes and wings, at Re of roughly 10⁴ and above. Covered taxa: cetaceans, sharks, bony
  fish, birds, bats and insects (Taylor 2003; Rohr & Fish; Nudds).
- **Breaks.** This is the most important field for the project.
  1. **Small, low-Re and elongate swimmers sit above 0.4.** From Eloy 2012, tables 1–3 [R preprint]:

     | Animal | St | Re |
     |---|---|---|
     | Goldfish | 0.54 | 7.1 × 10³ |
     | Bullfrog tadpole | 0.79 | |
     | West African lungfish | 1.02 | 7.0 × 10³ |
     | Hagfish | 0.56 | |
     | Longnose gar | 0.59 | |
     | European eel | 0.48–0.52 | |

     Eloy's model predicts this trend; the optimum is not a universal constant.
  2. **Cetaceans sit low (0.20–0.30), about 20% under the 0.25–0.35 foil band** (Rohr & Fish) [R].
     For whales and dolphins, 0.2–0.3 is a sharper check than 0.2–0.4.
  3. **Non-cruising flight.** Taylor et al. state the convergence holds "only when cruising" [R].
     Take-off, manoeuvring and acceleration are outside the band.
  4. **Hovering.** As U → 0, St → ∞ [D, definitional]. Strouhal number is the wrong descriptor there.
  5. **Convention errors** (above).
- **Worked examples.**
  - *Bottlenose dolphin* (Eloy 2012 table: L = 2.58 m, Re = 1.2 × 10⁷, St = 0.26, U/V = 0.52) [R]:
    - U = Re·ν/L = 1.2 × 10⁷ × 1.0 × 10⁻⁶ / 2.58 = **4.65 m s⁻¹** [D; assumes Eloy used ν = 10⁻⁶, not verified].
    - So f·A = St·U = 0.26 × 4.65 = **1.21 m s⁻¹** [D].
    - With Rohr & Fish's mid-range normalised amplitude A/L = 0.20 [R range 0.15–0.25]:
      A = 0.52 m and f = 1.21/0.52 = **2.3 Hz** [D].
    - This is a consistency reconstruction, not a measured kinematic record.
  - *Odontocete envelope from Rohr & Fish's normalised ranges* [R]: St = (fL/U)·(A/L).
    - Mid-range: 1.5 × 0.20 = **0.30** [D].
    - Extremes: 1 × 0.15 = **0.15** to 2 × 0.25 = **0.50** [D].
    - The ranges alone therefore permit values outside the observed 0.2–0.3 cluster; the clustering is a
      real constraint, not an artefact of those ranges.
  - *Saithe* (St 0.23, L 0.364 m) and *rainbow trout* (St 0.26, L 0.201 m) [R, Eloy table, from
    Videler & Hess 1984].
  - *A pigeon-sized bird, from Nudds et al.'s retrieved formula*. Inputs [M]: b = 0.65 m, U = 10 m s⁻¹,
    and St = 0.21 for a direct flier [R].
    - b^{−0.24} = 0.65^{−0.24} = 1.109, so θ/2 = 33.5 × 1.109 = **37.1°** [D].
    - A = b·sin(37.1°) = 0.65 × 0.604 = **0.393 m** [D].
    - f = 0.21 × 10 / 0.393 = **5.3 Hz** [D].
    - Pigeon cruising wingbeat frequencies of roughly 5–7 Hz are [M], so this is a plausibility check only.
- **Sources.**
  - **Taylor GK, Nudds RL, Thomas ALR 2003, Flying and swimming animals cruise at a Strouhal number
    tuned for high power efficiency, *Nature* 425:707–711, doi 10.1038/nature02000, PMID 14562101 —
    `abstract`.** The full text was paywalled. **Upgrading this to `full-text` is the top item in §9.**
  - Triantafyllou MS, Triantafyllou GS, Gopalkrishnan R 1991, Wake mechanics for thrust generation in
    oscillating foils, *Phys Fluids A* 3:2835–2837, doi 10.1063/1.858173 — `abstract`.
  - Triantafyllou GS, Triantafyllou MS, Grosenbaugh MA 1993, Optimal thrust development in oscillating
    foils with application to fish propulsion, *J Fluids Struct* 7:205–224, doi 10.1006/jfls.1993.1012 — `metadata`.
  - Rohr JJ, Fish FE 2004, Strouhal numbers and optimization of swimming by odontocete cetaceans,
    *J Exp Biol* 207:1633–1642, doi 10.1242/jeb.00948 — `abstract`.
  - Nudds RL, Taylor GK, Thomas ALR 2004, Tuning of Strouhal number for high propulsive efficiency
    accurately predicts how wingbeat frequency and stroke amplitude relate and scale with size and
    flight speed in birds, *Proc R Soc B* 271:2071–2076, doi 10.1098/rspb.2004.2838, PMC1691825 — `abstract`.
  - Eloy C 2012, Optimal Strouhal number for swimming animals, *J Fluids Struct* 30:205–218,
    doi 10.1016/j.jfluidstructs.2012.02.008 — `full-text (preprint)` arXiv 1102.0223v1.
  - Usherwood JR 2025, *J R Soc Interface* 22:20240730, doi 10.1098/rsif.2024.0730 — `abstract`.
  - Saadat M et al. 2017, On the rules for aquatic locomotion, *Phys Rev Fluids* 2:083102,
    doi 10.1103/PhysRevFluids.2.083102 — `metadata`. Its "St 0.2–0.4, A/L 0.1–0.3" was seen only in a
    search snippet and is unverified.
  - Wang ZJ 2000, Vortex shedding and frequency selection in flapping flight, *J Fluid Mech* 410:323–341,
    doi 10.1017/S0022112099008071 — `metadata`.

### 4.3 Swimming number (Gazzola, Argentina & Mahadevan 2014)

- **Equation.** Sw = ωAL/ν, with ω = 2πf (s⁻¹). The claimed scalings are Re ∼ Sw^{4/3} (laminar
  boundary layer) and Re ∼ Sw (turbulent).
- **Status.** The paper was reached only at `metadata` level. Everything here comes from search
  snippets: the prefactors Re ≈ 0.04·Sw^{4/3} and Re ≈ 0.43·Sw, a crossover near Re ≈ 3000, and "over
  1000 measurements". **None of it is verified. Do not use it as a design check until the paper is
  read.** It is listed because it is the main candidate for a speed-from-kinematics check that spans
  the laminar and turbulent regimes.
- **Source.** Gazzola M, Argentina M, Mahadevan L 2014, Scaling macroscopic aquatic locomotion,
  *Nat Phys* 10:758–761, doi 10.1038/nphys3078 — `metadata`.

### 4.4 Froude number (gait) and Froude efficiency (propulsion)

These two quantities share a name and nothing else.

**(a) Froude number for legged gait**

- **Equation.** Fr = U²/(gL).
  - U: speed (m s⁻¹). g: gravitational acceleration (m s⁻²).
  - L: leg length or hip height (m).
- **Value.**
  - Bipeds switch from walking to running "at approximately the same Froude number (0.5)", including at
    reduced gravity (Kram et al. 1997) [R abstract].
  - A theoretical maximum walking Fr = 1 follows from the inverted pendulum: at Fr = 1 the centripetal
    requirement equals g [D].
  - Quadruped walk–trot Fr ≈ 0.5 and trot–gallop Fr ≈ 2–3 are **[M]**. They are not in the retrieved
    abstract of Alexander & Jayes 1983.
- **Mechanism.** Dynamic similarity: animals moving at equal Fr have geometrically similar gaits
  (Alexander & Jayes 1983) [R abstract].
- **Domain.** The hypothesis is "tenable" for "cursorial" mammals, and "Most mammals of mass greater
  than 5 kg are of this type" (Alexander & Jayes) [R abstract].
- **Breaks.**
  1. Non-cursorial and small mammals (same source) [R].
  2. Race walkers exceed Fr = 1 by changing the mechanics, e.g. with pelvic motion [M].
  3. Equal Fr does not give equal *metabolic* cost.
- **Worked example: human, L = 0.9 m** [M].
  - Walk–run transition at Fr 0.5: U = √(0.5 × 9.81 × 0.9) = **2.10 m s⁻¹** [D].
  - Walking ceiling at Fr = 1: U = √(9.81 × 0.9) = **2.97 m s⁻¹** [D].
  - On Mars (g = 3.73 m s⁻²) [M], the transition falls to √(0.5 × 3.73 × 0.9) = **1.30 m s⁻¹** [D]. The
    reduced-gravity experiment of Kram et al. tests exactly this direction of prediction [R].

**(b) Froude propulsive efficiency**

- **Equation.** η_F = 2/(1 + V_j/U) = 2U/(U + V_j).
  - V_j: speed of the jet or wake (m s⁻¹). U: forward speed (m s⁻¹).
  - This is actuator-disc momentum theory [M].
  - Eloy's general definition is η = DU/(DU + ⟨E⟩), with D drag and ⟨E⟩ the mean power shed to the
    wake [R preprint, eq. 12].
- **Mechanism.** Thrust is ṁ(V_j − U). Kinetic energy wasted in the wake rises with (V_j − U)². So
  efficiency favours accelerating a large mass of fluid a little.
- **Breaks.** Unsteady and pulsed jets (squid, jellyfish) and vortex-ring propulsion are not captured
  by steady momentum theory [M].
- **Worked example.** V_j = 1.5U gives η_F = 2/2.5 = **0.80** [D]. V_j = 3U gives **0.50** [D].
- **Sources.**
  - Alexander RMcN, Jayes AS 1983, A dynamic similarity hypothesis for the gaits of quadrupedal
    mammals, *J Zool* 201:135–152, doi 10.1111/j.1469-7998.1983.tb04266.x — `abstract`.
  - Kram R, Domingo A, Ferris DP 1997, Effect of reduced gravity on the preferred walk–run transition
    speed, *J Exp Biol* 200:821–826, doi 10.1242/jeb.200.4.821 — `abstract`.

### 4.5 Lighthill elongated-body theory

- **Equation.**
  - Mean thrust: ⟨T⟩ = ⟨[m·w·ẏ − ½·m·w²·x′]_{s = tail}⟩.
  - Power shed to the wake: ⟨E⟩ = ⟨[½·m·w²·u]_{s = tail}⟩.
  - m = ρπh²: added mass per unit length at the trailing edge (kg m⁻¹), with h the tail half-span (m).
  - w: lateral velocity of the water relative to the body section (m s⁻¹). ẏ: lateral velocity of the tail (m s⁻¹).
  - The equations are as given by Eloy [R preprint, eq. 4].
  - Small-amplitude Froude efficiency: **η = (1 + U/V)/2**, where V is the backward body-wave speed
    (m s⁻¹) [M].
- **Mechanism.** In inviscid slender-body theory, thrust comes entirely from the momentum of the water
  shed at the trailing edge. Thrust requires V > U.
- **Value.**
  - Lighthill 1960 says to "pass a wave down its body at a speed of around 5/4 of the desired swimming
    speed, the amplitude increasing from zero over the front portion to a maximum at the tail"
    [R abstract]. That gives U/V = 0.8 and η = (1 + 0.8)/2 = **0.90** [D, from the M formula].
  - Bottlenose dolphin U/V = 0.52 [R, Eloy table] gives η = **0.76** [D]. The dolphin falls outside
    the theory's domain (see Breaks), so treat this as illustrative only.
- **Domain.** Slender bodies at high Re where the cross-section changes slowly. The theory applies "if
  the wavelength… exceeds 5s" (Lighthill 1970) [R abstract]. The large-amplitude extension covers
  "fish motions of arbitrary amplitude" (Lighthill 1971) [R abstract].
- **Breaks.**
  1. It "ceases to be applicable" for widened, swept-back lunate tails (Lighthill 1970) [R].
  2. Eloy: "elongated fish such as eels and knife-fish, for which h/L < 0.1, will not in general meet
     this criterion". It also fails "for scombrids, dolphins and sharks that share a large aspect-ratio
     tail" [R preprint]. So it is clean only for the middle range of carangiform shapes.
  3. Lighthill 1971 itself flags "substantial enhancement of drag… boundary-layer-thinning" in a dace
     comparison. Drag on an undulating body is not drag on a rigid one [R abstract].
  4. Rays, boxfish and other non-undulatory body plans: no retrieved source, but they lie outside the
     theory's geometric assumptions [M].
- **Sources.**
  - Lighthill MJ 1960, Note on the swimming of slender fish, *J Fluid Mech* 9:305–317, doi 10.1017/S0022112060001110 — `abstract`.
  - Lighthill MJ 1970, Aquatic animal propulsion of high hydromechanical efficiency,
    *J Fluid Mech* 44:265–301, doi 10.1017/S0022112070001830 — `abstract`.
  - Lighthill MJ 1971, Large-amplitude elongated-body theory of fish locomotion,
    *Proc R Soc B* 179:125–138, doi 10.1098/rspb.1971.0085 — `abstract`.
  - Eloy 2012 (§4.2) — `full-text (preprint)`.

### 4.6 Weis-Fogh clap-and-fling, and unsteady lift at low Re

- **Mechanism.** At the top of the stroke the wings clap together. They then fling apart by rotating
  about their trailing edges, so circulation of opposite sign builds on each wing *without* waiting for
  the Kutta-condition starting vortex that steady theory needs.
  - In Lighthill's inviscid analysis the circulations are "−0·69Ωc² and +0·69Ωc²" around the two wings,
    with Ω the fling angular velocity (rad s⁻¹) and c the chord (m) [R abstract].
- **Value.**
  - *Encarsia formosa*: at "low Reynolds number (10–20), the high lift coefficient of 2 or 3 is not
    possible with steady-state aerodynamics" (Weis-Fogh 1973) [R abstract].
  - Specific power: "1·3 and 4·7 W N⁻¹" [R]. The two values' attribution was not given in the abstract.
  - Robotic-wing measurements: wing–wing interaction "augmented total lift production by up to 17%,
    but depended strongly on stroke kinematics". It needs an angular separation of "no more than
    10–12°" (Lehmann, Sane & Dickinson 2005) [R abstract].
- **Domain.** Weis-Fogh 1973 [R abstract]:
  - The fling is "involved in the normal flight of butterflies and possibly of *Drosophila* and other
    small insects".
  - It is a "useful mechanism in birds and bats during take-off".
  - Hover-flies and Odonata rely "almost entirely upon the flip".
  - Ellington 1984 reports "a near fling and partial fling for the ladybird" [R abstract].
  - A 2025 robot modelled on *Cynopterus brachyotis* found an upstroke "clap" "significantly increases
    lift" at St = 0.2–0.4 [R abstract].
  - Clapping during pigeon take-off and in thrips is [M].
- **Breaks.**
  1. Clap-and-fling is one of several unsteady mechanisms and not the general explanation of insect lift.
     Dickinson et al. 1999 name "three distinct yet interactive mechanisms: delayed stall, rotational
     circulation, and wake capture" [R abstract].
  2. Ellington: "most, if not all, hovering animals do not rely on quasi-steady aerodynamics" [R].
  3. The benefit is kinematics-dependent and modest (≤17%) [R]. Repeated clapping also costs wing wear
     (a wear cost that is [M]).
- **Worked example.** The quasi-steady deficit: Weis-Fogh's *Encarsia* needs C_L of 2–3 [R]. Steady
  aerofoils at Re 10–20 cannot produce that [R]. The unexplained factor is therefore at least 2 relative
  to a steady C_L of about 1 [D; the steady C_L of about 1 is M].
- **Sources.**
  - Weis-Fogh T 1973, Quick estimates of flight fitness in hovering animals, including novel mechanisms
    for lift production, *J Exp Biol* 59:169–230, doi 10.1242/jeb.59.1.169 — `abstract`.
  - Lighthill MJ 1973, On the Weis-Fogh mechanism of lift generation, *J Fluid Mech* 60:1–17,
    doi 10.1017/S0022112073000017 — `abstract`.
  - Ellington CP 1984, The aerodynamics of hovering insect flight, I–VI, *Phil Trans R Soc B* 305:1–181.
    Part VI is doi 10.1098/rstb.1984.0054 — `abstract` (part VI only).
  - Dickinson MH, Lehmann F-O, Sane SP 1999, Wing rotation and the aerodynamic basis of insect flight,
    *Science* 284:1954–1960, doi 10.1126/science.284.5422.1954 — `abstract`.
  - Lehmann F-O, Sane SP, Dickinson MH 2005, The aerodynamic effects of wing–wing interaction in
    flapping insect wings, *J Exp Biol* 208:3075–3092, doi 10.1242/jeb.01744 — `abstract`.
  - Fan et al. 2025, *J R Soc Interface*, doi 10.1098/rsif.2024.0590 — `abstract`.

### 4.7 Cost of transport against body mass

- **Equation, terrestrial (Taylor, Heglund & Maloiy 1982)** [R abstract]:
  E_metab/M_b = **10.7·M_b^{−0.316}·v_g + 6.03·M_b^{−0.303}**.
  - E_metab/M_b: mass-specific metabolic power (W kg⁻¹).
  - M_b: body mass (kg).
  - v_g: ground speed (m s⁻¹).
  - The equation is based on 62 avian and mammalian species, with "1 ml O₂ = 20.1 J". In O₂ units:
    0.533·M_b^{−0.316}·v_g + 0.300·M_b^{−0.303} ml O₂ s⁻¹ kg⁻¹.
  - "Ninety per cent" of the data lie within 25% of the line.
  - **The slope 10.7·M_b^{−0.316} is the incremental (minimum net) cost of transport, in J kg⁻¹ m⁻¹.**
- **Value.**
  - Exponent −0.316 for the slope [R].
  - Alexander 2005 summarises running cost of transport as "proportional to (body mass)^−0.32" [R abstract].
  - Flight (Alexander 2005) [R abstract]: mechanical power at maximum-range speed ∝ M^{1.02}, against
    metabolic power ∝ M^{0.83}.
  - Fish modelled as submarines (Alexander 2005) [R abstract]: power ∝ M^{0.5}U^{2.5} (laminar) or
    M^{0.6}U^{2.8} (turbulent).
  - Schmidt-Nielsen 1972's three lines (swimming < flying < running at a given mass) are [M]: the
    paper is at `metadata` level and its exponents were not retrieved.
- **Mechanism.** It is debated. Proposals include muscle force-generation cost scaling with stride
  frequency, and the mechanics of small animals [M]. The regression itself is empirical.
- **Domain.** Steady level running in birds and mammals, about 0.01–250 kg in the 1982 dataset (the
  range is [M]). Speeds are where power is linear in speed.
- **Breaks.**
  1. Outside the linear power–speed range.
  2. Inclines and loads.
  3. Hopping kangaroos, whose cost is roughly constant with speed [M].
  4. Humans lie above the line [M].
  5. The 25% scatter band [R] is the stated limit of the regression.
- **Worked example: incremental cost of transport, 10.7·M^{−0.316} J kg⁻¹ m⁻¹** [D from R]:

  | Animal | Mass | Calculation | Cost (J kg⁻¹ m⁻¹) |
  |---|---|---|---|
  | Mouse | 0.03 kg | 0.03^{−0.316} = 3.03 | **32.4** |
  | Human-sized mammal | 70 kg | 70^{−0.316} = 0.261 | **2.79** |
  | Horse | 500 kg | 500^{−0.316} = 0.140 | **1.50** |

  - The mouse pays 21.6× more per kilogram per metre than the horse [D]. The ±25% band means any
    single animal could legitimately lie 0.75–1.25× off the line.
- **Sources.**
  - Taylor CR, Heglund NC, Maloiy GMO 1982, Energetics and mechanics of terrestrial locomotion. I.,
    *J Exp Biol* 97:1–21, doi 10.1242/jeb.97.1.1 — `abstract`.
  - Alexander RMcN 2005, Models and the scaling of energy costs for locomotion,
    *J Exp Biol* 208:1645–1652, doi 10.1242/jeb.01484 — `abstract`.
  - Schmidt-Nielsen K 1972, Locomotion: energy cost of swimming, flying, and running,
    *Science* 177:222–228, doi 10.1126/science.177.4045.222 — `metadata`.
  - Tucker VA 1970, Energetic cost of locomotion in animals, *Comp Biochem Physiol* 34:841–846,
    doi 10.1016/0010-406X(70)91006-6 — `metadata`.

---

## 5. Flight specifically

### 5.1 Pennycuick power curve

- **Equation** [M; standard form, not retrieved]: P(U) = P_ind + P_par + P_pro, where:
  - Induced power, P_ind = k·(mg)²/(2ρ·S_d·U). Here k is the induced-power factor (≈1.1–1.2, [M]),
    m is mass (kg), ρ is air density (kg m⁻³), S_d = πb²/4 is the disc area swept by wingspan b (m²),
    and U is airspeed (m s⁻¹).
  - Parasite power, P_par = ½·ρ·S_b·C_Db·U³. Here S_b is the body frontal area (m²) and C_Db is the
    body drag coefficient.
  - Profile power, P_pro: the drag of the wings themselves, often treated as roughly constant across
    cruise speeds [M].
- **Shape.** P_ind falls as 1/U and P_par rises as U³, so the total curve is U-shaped. Two speeds
  matter:
  - V_mp, the minimum-power speed, where P is lowest.
  - V_mr, the maximum-range speed, where P/U is lowest, i.e. the tangent from the origin.
- **Scaling.**
  - Under geometric similarity, V_mp ∝ m^{1/6} [M].
  - Pennycuick 1969 [R abstract]: "Small birds have a greater margin of power available over power
    required than large ones". Adding weight increases "both minimum-power speed, and maximum-range
    speed, in proportion to the square root of the weight, and… the corresponding powers in proportion
    to the three-halves power of the weight". "Birds up to about 750 g (fat-free) can double their
    fat-free mass, and still have sufficient power to fly at the maximum-range speed". "There is an
    upper limit to the mass of practicable flying birds, represented approximately by the Kori Bustard
    *Ardeotis kori*".
  - The size limit rests on power required rising faster with mass than power available (often quoted
    as m^{7/6} against m^{2/3}–m^{0.72}). **Those exponents are [M]; they are not in the abstract.**
- **Measured shape.** Tobalske et al. 2003 [R abstract]:
  - The magpie (*Pica pica*) curve "is relatively flat over intermediate velocities".
  - "the power curve for cockatiels is acutely concave, whereas that for doves is intermediate".
  - "wing-beat frequency and mechanical power output do not necessarily share minima".
- **Domain.** Steady, level, flapping flight by birds and bats. Taken from aircraft actuator-disc theory.
- **Breaks.**
  1. The *depth* of the U varies by species, and in the magpie it is nearly flat over intermediate
     speeds [R]. The curve's minimum is therefore a poor predictor of preferred speed in such species.
  2. Intermittent flight (bounding, flap-gliding), hovering, and very small fliers (insects), where
     unsteady mechanisms dominate (§4.6).
- **Worked example.** Under the [M] scaling V_mp ∝ m^{1/6}, a 10 kg swan against a 0.4 kg pigeon:
  (10/0.4)^{1/6} = 25^{0.1667} = **1.71** [D]. The swan's minimum-power speed should be about 1.7× the
  pigeon's. No retrieved V_mp values were available to check this.
- **Sources.**
  - Pennycuick CJ 1968, Power requirements for horizontal flight in the pigeon *Columba livia*,
    *J Exp Biol* 49:527–555, doi 10.1242/jeb.49.3.527 — `metadata`.
  - Pennycuick CJ 1969, The mechanics of bird migration, *Ibis* 111:525–556,
    doi 10.1111/j.1474-919x.1969.tb02566.x — `abstract`.
  - Pennycuick CJ 1975, Mechanics of flight, in *Avian Biology* vol 5 — `remembered`.
  - Pennycuick CJ 2008, *Modelling the Flying Bird* — `remembered`.
  - Tobalske BW, Hedrick TL, Dial KP, Biewener AA 2003, Comparative power curves in bird flight,
    *Nature* 421:363–366, doi 10.1038/nature01284 — `abstract`.

### 5.2 Wing loading against mass; Greenewalt's dimensional relations

- **Equation.** Wing loading W/S = mg/S (N m⁻²), with S wing area (m²). Under isometry, S ∝ m^{2/3}, so
  W/S ∝ m^{1/3} [D].
  - Flight speed for a given lift coefficient then scales as U ∝ (W/S)^{1/2} ∝ m^{1/6} [D], from
    lift = ½ρU²SC_L.
- **Value.**
  - The only retrieved, CI-bearing exponents are from Sato et al. 2009 for procellariiforms, given in
    §1.1: span M^{0.37} (CI 0.34–0.40), area M^{0.58} (CI 0.53–0.62), and the implied wing loading
    M^{0.42} [R/D].
  - Greenewalt 1962 and 1975 compiled the classic dimensional relations across birds, bats and insects,
    and Norberg & Rayner 1987 did the same for bats. **Their exponents were not retrieved.** Wing loading
    exponents near 0.28–0.33 that circulate for birds are [M], as is Tennekes's "Great Flight Diagram".
- **Domain.** Within a clade with a similar flight style. Pooling hummingbirds, soarers and insects
  mixes regimes.
- **Breaks.**
  1. Exponents differ by clade and flight mode; Greenewalt himself separated groups [M].
  2. Hummingbirds and insects depart from bird lines [M].
- **Sources.**
  - Greenewalt CH 1962, Dimensional relationships for flying animals, with special reference to
    hummingbirds, *Smithson Misc Coll* 144(2), 46 pp. (Smithsonian repository handle 10088/22978) — `metadata`.
  - Greenewalt CH 1975, The flight of birds, *Trans Am Philos Soc* 65(4) — `remembered`.
  - Norberg UM, Rayner JMV 1987, Ecological morphology and flight in bats…, *Phil Trans R Soc B*
    316:335–427, doi 10.1098/rstb.1987.0030 — `metadata`.
  - Sato et al. 2009 (§5.3) — `full-text`.

### 5.3 Maximum size for powered flight

There is no single limit. There are several limits for different flight modes and launch mechanics,
and they disagree.

| Claim | Value | Status / source |
|---|---|---|
| Upper limit for *albatross-like soaring* animals | **41 kg, 5.1 m span (95% CI 26–75 kg)** | [R full-text], Sato et al. 2009 |
| Upper limit for flying birds generally | approximately the Kori bustard, *Ardeotis kori* | [R abstract], Pennycuick 1969 |
| *Argentavis magnificens* | mass ≈70 kg; "probably too large… to be capable of continuous flapping flight or standing takeoff under its own muscle power"; glide angle about 3°; cruise 67 km/h | [R abstract], Chatterjee et al. 2007. The ~7 m span is [M] |
| *Pelagornis sandersi* | "Conservative wingspan estimates (∼6.4 m) exceed theoretical maximums based on extant soaring birds" | [R abstract], Ksepka 2014. The 6.06–7.38 m range is [M] |
| Giant azhdarchid pterosaurs (*Quetzalcoatlus northropi*) | "10–11 m wingspans and masses of 200–250 kg are the most reliable upper estimates"; launch "from a standing, quadrupedal start… vaulting over their forelimbs" | [R full-text], Witton & Habib 2010 |
| Largest Palaeozoic insects (*Meganeuropsis*) | ~0.71 m span [M] | The fossil record "makes it impossible to definitively accept or reject" the oxygen–size link [R abstract], Harrison et al. 2010 |
| Heaviest extant flappers (great bustard 16–18 kg; mute swan) | | [M] |
| Largest hovering bird (*Patagona gigas*, ~18–24 g) | | [M] |

- **Sato et al.'s method** [R full-text]. High and low flapping frequencies of 26 birds of 5 species
  scale as M^{−0.30} (CI −0.33 to −0.27) and M^{−0.18} (CI −0.20 to −0.16). Predictions were M^{−1/3}
  and M^{−1/6}. Above the mass where the lines cross, "Albatross-like animals larger than the limit
  will not be able to flap fast enough to stay aloft under unfavourable wind conditions".
- **Where it breaks.** The pterosaur figure is about 5× Sato's soaring limit. Witton & Habib explicitly
  reject bird-derived limits for pterosaurs, because quadrupedal launch changes the take-off power
  budget [R]. They also state that "fossil birds of much greater size than living bustards, such as
  Argentavis, appear to have been capable of launch and flight" [R].
  - **Size limits derived from extant-bird scaling therefore fail on taxa with a different launch
    mechanism.** Take-off, not cruise, is the binding constraint.
- **Worked example.** Using Sato's two fits with the crossing at 41 kg: the high-frequency limit falls
  faster than the low-frequency requirement by M^{−0.30 + 0.18} = M^{−0.12} [D]. At 2 × 41 = 82 kg, the
  available-over-required ratio is 2^{−0.12} = **0.92** of its value at the limit [D]. The gap is small
  per doubling, which is why the CI on the crossing is so wide (26–75 kg) [R].
- **Sources.**
  - Sato K et al. 2009, Scaling of soaring seabirds and implications for flight abilities of giant
    pterosaurs, *PLoS ONE* 4:e5400, doi 10.1371/journal.pone.0005400, PMC2670537 — `full-text`.
  - Witton MP, Habib MB 2010, On the size and flight diversity of giant pterosaurs…,
    *PLoS ONE* 5:e13982, doi 10.1371/journal.pone.0013982, PMC2981443 — `full-text`.
  - Chatterjee S, Templin RJ, Campbell KE 2007, The aerodynamics of *Argentavis*…,
    *PNAS* 104:12398–12403, doi 10.1073/pnas.0702040104 — `abstract`.
  - Ksepka DT 2014, Flight performance of the largest volant bird, *PNAS* 111:10624–10629,
    doi 10.1073/pnas.1320297111 — `abstract`.
  - Harrison JF, Kaiser A, VandenBrooks JM 2010, Atmospheric oxygen level and the evolution of insect
    body size, *Proc R Soc B* 277:1937–1946, doi 10.1098/rspb.2010.0001 — `abstract`.

---

## 6. Pattern and form

### 6.1 Turing reaction–diffusion instability

- **Equation.** For two species:
  - u_t = f(u,v) + D_u∇²u
  - v_t = g(u,v) + D_v∇²v
  - u, v: concentrations (mol m⁻³). D_u, D_v: diffusivities (m² s⁻¹).
  - f_u, f_v, g_u, g_v: entries of the reaction Jacobian at the homogeneous steady state (s⁻¹).
- **Conditions** [D; derived here from the dispersion relation, and **not** retrieved from Turing or
  Murray, whose texts were not read]:
  1. f_u + g_v < 0. The steady state is stable without diffusion.
  2. f_u·g_v − f_v·g_u > 0. Same reason.
  3. D_v·f_u + D_u·g_v > 0.
  4. (D_v·f_u + D_u·g_v)² > 4·D_u·D_v·(f_u·g_v − f_v·g_u).
  - Derivation: the perturbation e^{λt + ikx} gives det(J − k²D) = D_uD_v·k⁴ − (D_v f_u + D_u g_v)·k² +
    det J. Instability needs this to go negative for some k². Its minimum is at the critical wavenumber
    **k_c² = (D_v f_u + D_u g_v)/(2D_uD_v)** (m⁻²). The trace stays negative for all k, so instability
    can only come through the determinant.
  - Conditions 1 and 3 together force f_u and g_v to have opposite signs and D_v ≠ D_u, the classical
    "short-range activation, long-range inhibition".
- **Domain.** Linear stability of a homogeneous state. Pattern *wavelength* near onset is about 2π/k_c.
- **Breaks.** This field is load-bearing.
  1. **Linear instability is neither necessary nor sufficient for a pattern to form.** Subcritical
     patterns form where the linear analysis says the state is stable. That is this repository's own
     rule 4 in CONTRIBUTING-VERIFICATION.md, learned the hard way.
  2. **The unequal-diffusivity requirement holds for 2-species models only.** Marcon et al. 2016 show
     that "in the presence of cell-autonomous factors, networks can form a pattern with equally
     diffusing signals and even for any combination of diffusion coefficients" [R full-text]. They add
     that realistic systems use mechanisms "fundamentally different from the concepts of short-range
     activation and long-range inhibition based on differential diffusivity" [R].
  3. Robustness: Turing patterns are sensitive to parameters and domain size [M]. Not every periodic
     pattern is a Turing pattern; *Drosophila* segmentation is a hierarchical gene cascade, not Turing [M].
- **Organisms (what has actually been shown).**
  - Mouse digits: "the dose of distal Hox genes modulates the digit period or wavelength" (Sheth et al.
    2012) [R abstract]. "A Turing network implemented by Bmp, Sox9, and Wnt drives digit specification"
    (Raspopovic et al. 2014) [R abstract].
  - Palatal rugae: "FGF and Shh as components of an activator-inhibitor pair" (Economou et al. 2012) [R].
  - Angelfish *Pomacanthus*: "a reaction–diffusion wave is a viable mechanism for the stripe pattern"
    (Kondo & Asai 1995) [R abstract]. Note the word *viable*.
  - **None of these retrieved abstracts gives the kinetic parameters needed to check conditions 1–4
    numerically for a real organism.**
- **Worked example: a model system, not an organism.** Take f_u = 1, f_v = −1, g_u = 2, g_v = −1.5,
  D_u = 1 and D_v = d [D]:
  - tr J = −0.5 < 0 and det J = −1.5 + 2 = 0.5 > 0, so the system is stable without diffusion.
  - Condition 3: d − 1.5 > 0, so d > 1.5.
  - Condition 4: (d − 1.5)² > 2d, i.e. d² − 5d + 2.25 > 0. The roots are 0.5 and 4.5, so **d > 4.5**.
  - At d = 4.5: k_c² = (4.5 − 1.5)/9 = 0.333, and the wavelength is 2π/√0.333 = **10.9 length units**.
  - The inhibitor must diffuse at least 4.5× faster than the activator in this 2-species model. Per
    Marcon et al., adding an immobile third species removes that requirement.
- **Sources.**
  - Turing AM 1952, The chemical basis of morphogenesis, *Phil Trans R Soc B* 237:37–72,
    doi 10.1098/rstb.1952.0012 — `metadata`.
  - Gierer A, Meinhardt H 1972, A theory of biological pattern formation, *Kybernetik* 12:30–39,
    doi 10.1007/BF00289234 — `metadata`.
  - Kondo S, Miura T 2010, *Science* 329:1616–1620, doi 10.1126/science.1179047 — `abstract`.
  - Marcon L, Diego X, Sharpe J, Müller P 2016, *eLife* 5:e14022, doi 10.7554/eLife.14022, PMC4922859 — `full-text`.
  - Sheth R et al. 2012, *Science* 338:1476–1480, doi 10.1126/science.1226804 — `abstract`.
  - Raspopovic J et al. 2014, *Science* 345:566–570, doi 10.1126/science.1252960 — `abstract`.
  - Kondo S, Asai R 1995, *Nature* 376:765–768, doi 10.1038/376765a0 — `abstract`.
  - Economou AD et al. 2012, *Nat Genet* 44:348–351, doi 10.1038/ng.1090 — `abstract` (quoted from the
    abstract, although the full text was fetched).

### 6.2 D'Arcy Thompson transformations

- **Equation.** None in the original. Two related forms are drawn on a Cartesian grid by a smooth map
  (x, y) → (x′, y′) [M]. The quantitative successor is landmark-based geometric morphometrics:
  Procrustes superimposition and thin-plate splines (Bookstein 1991) [M].
- **Examples.** *Argyropelecus* → *Sternoptyx* and *Diodon* → *Orthagoriscus* (*Mola*) are both [M].
- **Breaks and status.** This is **descriptive**. It shows that a smooth map exists. It does not say why
  that map, and it does not constrain which maps are possible. It is not a design law.
- **Sources.**
  - Thompson DW 1917, *On Growth and Form*, Cambridge Univ Press, chapter "On the theory of
    transformations" — `remembered`.
  - Bookstein FL 1991, *Morphometric Tools for Landmark Data* — `remembered`.

### 6.3 Phyllotaxis and the golden angle

- **Equation.** Divergence angle ψ = 360°·(1 − 1/φ) = 360°/φ² = 180°·(3 − √5) = **137.5077640500°** [D].
  - φ = (1 + √5)/2.
  - Organs placed at this angle form parastichy spirals whose counts are consecutive Fibonacci numbers.
- **Mechanism.**
  - Douady & Couder 1992 and 1996 reproduce Fibonacci spirals as a self-organised growth process: each
    new primordium forms where the inhibitory fields of existing ones are weakest [M; the papers are at
    `metadata` level].
  - Molecular basis: "Auxin accumulation occurs only at certain minimal distances from existing
    primordia, defining the position of future primordia" (Reinhardt et al. 2003) [R abstract].
- **Value.** Sunflowers (Swinton, Ochu et al. 2016, citizen science, 657 heads) [R full-text]:
  - 768 parastichy numbers were evaluated. 565 were Fibonacci numbers, and a further 67 had a
    predefined Fibonacci-type structure.
  - In total, **632/768 (82%)** had Fibonacci structure and **136/768 (18%)** did not. The 136 split
    into Fibonacci − 1 (49), Fibonacci + 1 (17) and other (70).
  - Historical figures for comparison: Schoute 82%, Weisse 95%.
- **Domain.** Spiral phyllotaxis in the shoot apical meristem.
- **Breaks.**
  1. **Nearly 1 in 5 sunflower parastichy counts is not Fibonacci** [R].
  2. *Arabidopsis*: "organs are sometimes co-initiated in the meristem, leading randomly to
     post-meristematic organ order permutations in around half of the cases" (Refahi et al. 2016),
     measured against a perfect 137.5° spiral as reference [R full-text].
  3. Distichous (180°) and whorled phyllotaxis do not use the golden angle at all [M].
  - Jean's "~92% of spiral species are Fibonacci" is [M].
- **Worked example.** The quickest check of a design or simulation: successive organ angles modulo 360°
  should cluster at 137.5°. Two consecutive organs should be no closer than ψ apart [D]. And
  parastichy pairs should read (8, 13), (13, 21), (21, 34), (34, 55) and so on, with about 18% of
  counts allowed off-sequence before the result is unlike sunflowers [R].
- **Sources.**
  - Douady S, Couder Y 1992, Phyllotaxis as a physical self-organized growth process,
    *Phys Rev Lett* 68:2098–2101, doi 10.1103/PhysRevLett.68.2098 — `metadata`.
  - Douady S, Couder Y 1996, Phyllotaxis as a dynamical self organizing process. Part I: The spiral
    modes…, *J Theor Biol* 178:255–273, doi 10.1006/jtbi.1996.0024 — `metadata`.
  - Reinhardt D et al. 2003, Regulation of phyllotaxis by polar auxin transport,
    *Nature* 426:255–260, doi 10.1038/nature02081 — `abstract`.
  - Swinton J, Ochu E, MSI Turing's Sunflower Consortium 2016, Novel Fibonacci and non-Fibonacci
    structure in the sunflower: results of a citizen science experiment, *R Soc Open Sci* 3:160091,
    doi 10.1098/rsos.160091, PMC4892450 — `full-text`.
  - Refahi Y et al. 2016, *eLife* 5:e14093, doi 10.7554/eLife.14093, PMC4947393 — `full-text`.

### 6.4 Branching, Leonardo's rule and fractal dimension

- **Equation.** **Leonardo's rule:** d^Δ = Σ d_i^Δ, with d the parent branch diameter (m), d_i the
  daughter diameters (m), and Δ the dimensionless Leonardo exponent.
  - Δ = 2 means cross-sectional area is preserved. Compare Murray's Δ = 3 (§2.2).
  - **Fractal (box-counting) dimension:** D = −lim log N(ε)/log ε, where N(ε) is the number of boxes of
    side ε needed to cover the structure [M].
- **Value.**
  - "The available data indicate that the Leonardo exponent is in the interval 1.8 < Δ < 2.3 for a
    large number of species" (Eloy 2011) [R preprint].
  - Eloy's wind-stress model "gives 1.93 < Δ < 2.21 when 2 < D < 3". Eloy also notes that "The fractal
    dimension D has never been measured directly on real trees" [R preprint].
- **Mechanism.**
  1. Eloy 2011: self-similar trees designed so every branch has the same probability of breaking in
     wind give Leonardo's rule [R].
  2. Minamino & Tateno 2014: biomechanical models "deviated from da Vinci's rule as the weights and/or
     the branching angles of lateral daughter branches increased", but "this deviation was small for a
     branching pattern in nature" [R full-text]. *Fagus crenata* fitted the uniform-stress model best;
     *Abies homolepis* often agreed with da Vinci's rule [R]. No Δ is reported.
- **Domain.** Woody tree branching. The hydraulic conduits inside a tree follow a different rule
  (Murray, §2.2, McCulloh). Two exponents coexist in one organism, one mechanical and one hydraulic.
- **Breaks.**
  1. **Finite scale range.** "The finite nature of the lung ultimately limits the range over which
     self-similarity scaling characteristics are applicable" (Nelson, West & Goldberger 1990) [R abstract].
     The general claim that natural "fractals" span only 1–2 decades is Avnir et al. 1998 [M; `metadata`].
  2. **Corals.** Fractal-dimension values for coral outlines (1.1–1.5) are often quoted from Martin-Garin
     et al. 2007; they are [M]. The paper was blocked. **No coral D is given here as retrieved.**
  3. Δ varies by species and by branching angle and weight (Minamino & Tateno).
- **Worked example: a 10 cm branch splitting into two equal daughters.** d_c = 10 × 2^{−1/Δ} [D]:
  - Δ = 1.8: **6.80 cm**.
  - Δ = 2.0: **7.07 cm**.
  - Δ = 2.3: **7.40 cm**.
  - Murray's Δ = 3: **7.94 cm**.
  - The 0.6 cm gap between Δ = 2.3 and Murray's value is measurable, which is what makes Leonardo's rule
    and Murray's law distinguishable in data.
- **Sources.**
  - Eloy C 2011, Leonardo's rule, self-similarity, and wind-induced stresses in trees,
    *Phys Rev Lett* 107:258101, doi 10.1103/PhysRevLett.107.258101 — `full-text (preprint)` arXiv 1105.2591v2, plus Europe PMC abstract.
  - Minamino R, Tateno M 2014, Tree branching: Leonardo da Vinci's rule versus biomechanical models,
    *PLoS ONE* 9:e93535, doi 10.1371/journal.pone.0093535, PMC3979699 — `full-text`.
  - West GB, Brown JH, Enquist BJ 1999, The fourth dimension of life: fractal geometry and allometric
    scaling of organisms, *Science* 284:1677–1679, doi 10.1126/science.284.5420.1677 — `metadata`.
  - West GB, Brown JH, Enquist BJ 1999, A general model for the structure and allometry of plant
    vascular systems, *Nature* 400:664–667, doi 10.1038/23251 — `metadata`.
  - Nelson TR, West BJ, Goldberger AL 1990, The fractal lung, *Experientia* 46:251–254,
    doi 10.1007/BF01951755 — `abstract`.
  - Martin-Garin B et al. 2007, Use of fractal dimensions to quantify coral shape, *Coral Reefs*
    26:541–550, doi 10.1007/s00338-007-0256-4 — `metadata`.
  - Avnir D, Biham O, Lidar D, Malcai O 1998, Is the geometry of nature fractal?, *Science* 279:39–40,
    doi 10.1126/science.279.5347.39 — `metadata`.

---

## 7. Growth

### 7.1 von Bertalanffy

- **Equation** [M]:
  - dL/dt = K·(L∞ − L), so L(t) = L∞·(1 − e^{−K(t − t₀)}).
  - L: length (m). L∞: asymptotic length (m). K: growth coefficient (yr⁻¹). t₀: nominal age at zero length (yr).
  - In mass form: dm/dt = η·m^{2/3} − κ·m. Anabolism is assumed to scale with surface (m^{2/3}) and
    catabolism with mass (m¹).
- **Mechanism.** The anabolism/catabolism balance above. Those exponents are *assumptions*, and they are
  exactly the 2/3 vs 3/4 question of §1.3.
- **Domain.** Indeterminate growers, mainly fish, after maturity.
- **Breaks.**
  1. The equation "provides a good description of somatic growth after maturity, but not before"
     (Lester, Shuter & Abrams 2004) [R abstract]. They attribute the departure to the cost of
     reproduction.
  2. Day & Taylor 1997 is titled "Von Bertalanffy's growth equation should not be used to model age and
     size at maturity" [R title; content not retrieved].
  3. Determinate growers (birds, mammals) [M].
- **Competing model.** WBE 2001 base ontogenetic growth on "allocation of metabolic energy between
  maintenance of existing tissue and the production of new biomass", giving "a single parameterless
  universal curve" [R abstract]. Their equation dm/dt = a·m^{3/4}·[1 − (m/M)^{1/4}] is [M].
- **Worked example.** Parameters are illustrative only, because no organism's fitted K or L∞ was
  retrieved. With L∞ = 100 cm, K = 0.2 yr⁻¹, t₀ = 0:
  - L(5) = 100·(1 − e^{−1}) = **63.2 cm** [D].
  - L(10) = 100·(1 − e^{−2}) = **86.5 cm** [D].
  - Half of L∞ is reached at t = ln 2/K = **3.47 yr** [D].
- **Sources.**
  - von Bertalanffy L 1938, *Hum Biol* 10:181 — `remembered`.
  - von Bertalanffy L 1957, Quantitative laws in metabolism and growth, *Q Rev Biol* 32:217–231,
    doi 10.1086/401873 — `metadata`.
  - Lester NP, Shuter BJ, Abrams PA 2004, Interpreting the von Bertalanffy model of somatic growth in
    fishes: the cost of reproduction, *Proc R Soc B* 271:1625–1631, doi 10.1098/rspb.2004.2778 — `abstract`.
  - Day T, Taylor PD 1997, *Am Nat* 149:381–393, doi 10.1086/285995 — `metadata`.
  - West GB, Brown JH, Enquist BJ 2001, A general model for ontogenetic growth, *Nature* 413:628–631,
    doi 10.1038/35098076 — `abstract`.

### 7.2 Gompertz

- **Equation** [M]:
  - dN/dt = a·N·e^{−bt}, so N(t) = N₀·exp[(a/b)(1 − e^{−bt})].
  - The asymptote is N₀·e^{a/b}.
  - N: size or cell number. a: initial specific growth rate (time⁻¹). b: rate of decay of that growth
    rate (time⁻¹).
  - Gompertz's own use was human mortality (1825). Winsor 1932 applied the curve to growth.
- **Mechanism.** None is given. It is an empirical curve whose specific growth rate decays
  exponentially in time.
- **Domain.** Tumour growth (Laird 1964; that its fits are Gompertzian is [M]) and many organism growth
  curves.
- **Breaks.** It is a fitting function, so the question is whether it fits better than logistic or von
  Bertalanffy. No retrieved source tests this here.
- **Worked example.** Illustrative parameters a = 1, b = 0.2: the asymptote is N₀·e^{5} = **148·N₀**
  [D]. Half of the log-asymptote is reached when 1 − e^{−0.2t} = 0.5, i.e. t = ln 2/0.2 = **3.47** time
  units [D].
- **Sources.**
  - Gompertz B 1825, On the nature of the function expressive of the law of human mortality…,
    *Phil Trans R Soc Lond* 115:513–583, doi 10.1098/rstl.1825.0026 — `metadata`.
  - Winsor CP 1932, The Gompertz curve as a growth curve, *PNAS* 18:1–8, doi 10.1073/pnas.18.1.1 — `metadata`.
  - Laird AK 1964, Dynamics of tumour growth, *Br J Cancer* 18:490–502, doi 10.1038/bjc.1964.55 — `metadata`
    (the PMC copy is a scan with no text layer).

### 7.3 Cell size control: sizer, timer and adder

- **Equation.** The three canonical models, stated through the slope of division size against birth
  size:
  - **Sizer:** L_d = const, slope 0.
  - **Adder:** L_d = L_b + Δ, slope 1.
  - **Timer:** L_d = L_b·e^{λτ}, slope 2 at the mean.
  - L_b, L_d: length or volume at birth and at division (µm or µm³). Δ: added size (µm). λ: growth rate (h⁻¹). τ: cycle time (h).
- **Value.**
  - *Caulobacter crescentus* stalked cells: "no significant correlation (slope ~ 0, Kendall τ = −0.001)
    between ΔL and Lb", n = 565. *E. coli* was also studied (Campos et al. 2014) [R full-text].
  - *E. coli* and *B. subtilis*, "hundreds of thousands" of cells: "The distribution of the size added
    in each generation, Δ, is thus independent of the newborn cell size" (Taheri-Araghi et al. 2015) [R full-text].
  - Amir 2014 predicts a mother–daughter size correlation of 0.5 under the incremental model, against a
    measured "C = 0.55" for slow-growing *E. coli* [R preprint].
  - Budding yeast is "very well described by the incremental model", measured between budding events
    (Soifer, Robert & Amir 2016) [R abstract].
- **Mechanism.** Amir's version adds a constant volume per origin between replication initiations, not
  from birth to division [R preprint]. Wallden et al. 2016 have replication initiate "at a fixed volume
  per chromosome" [R abstract].
- **Domain.** Steady-state, balanced growth of rod-shaped bacteria at moderate to fast growth rates.
  For budding yeast, the domain is the budded phase.
- **Breaks.**
  1. **Slow growth in *E. coli*:** this is "the only known steady-state growth condition wherein *E. coli*
     significantly deviates from the adder", deviating "towards the sizer" (Si et al. 2019) [R full-text].
     The adder was restored at a doubling time of about 4 h by repressing clpX. Oscillating FtsZ
     "systematically break[s] the adder" [R]. Wallden et al. 2016 also "correctly predict deviations
     from the adder behavior at slow growth" [R].
  2. **Fission yeast (*S. pombe*):**
     - Division–birth length slope 0.25 ± 0.02 (Facchetti et al. 2019). A pure sizer would give 0.
     - Their analysis supports "pure sizer control" on surface area [R full-text].
     - A sizer "can in some circumstances reproduce the apparent adder behavior". **The adder signature
       alone does not identify the mechanism** [R].
     - Fantes 1977: deviations "are corrected within a single cycle" [R abstract].
  3. **Budding yeast daughters:** "Cell size control contributes significantly to G1 variability in
     daughter cells but not in mother cells". The CLN3-dependent step "extends G1 in small daughters"
     (Di Talia et al. 2007). Small daughters show a sizer-like G1 [R abstract].
- **Worked example: a symmetrically dividing adder cell born 30% oversized,
  L_b⁽⁰⁾ = 1.3·L̄, where L̄ = Δ at steady state.**
  - Each cycle: L_b⁽ⁿ⁺¹⁾ = (L_b⁽ⁿ⁾ + Δ)/2, so the deviation halves every generation [D].
  - The excess goes 30% → 15% → 7.5% → **3.75%** over three generations [D].
  - A sizer removes the excess in one cycle (as Fantes reports for *S. pombe*) [R].
  - A timer never corrects it, and noise accumulates [D].
- **Sources.**
  - Campos M et al. 2014, A constant size extension drives bacterial cell size homeostasis,
    *Cell* 159:1433–1446, doi 10.1016/j.cell.2014.11.022, PMC4258233 — `full-text`.
  - Taheri-Araghi S et al. 2015, Cell-size control and homeostasis in bacteria,
    *Curr Biol* 25:385–391, doi 10.1016/j.cub.2014.12.009, PMC4323405 — `full-text`.
  - Amir A 2014, Cell size regulation in bacteria, *Phys Rev Lett* 112:208102,
    doi 10.1103/PhysRevLett.112.208102 — `full-text (preprint)` arXiv 1312.6562v4.
  - Soifer I, Robert L, Amir A 2016, *Curr Biol* 26:356–361, doi 10.1016/j.cub.2015.11.067 — `abstract`.
  - Wallden M et al. 2016, *Cell* 166:729–739, doi 10.1016/j.cell.2016.06.052 — `abstract`.
  - Si F et al. 2019, Mechanistic origin of cell-size control and homeostasis in bacteria,
    *Curr Biol* 29:1760–1770.e7, doi 10.1016/j.cub.2019.04.062, PMC6548602 — `full-text`.
  - Facchetti G, Knapp B, Chang F, Howard M 2019, Reassessment of the basis of cell size control based
    on analysis of cell-to-cell variability, *Biophys J* 117:1728–1738, doi 10.1016/j.bpj.2019.09.031,
    PMC6838950 — `full-text`.
  - Fantes PA 1977, Control of cell size and cycle time in *Schizosaccharomyces pombe*,
    *J Cell Sci* 24:51–67, doi 10.1242/jcs.24.1.51 — `abstract`.
  - Di Talia S et al. 2007, *Nature* 448:947–951, doi 10.1038/nature06072 — `abstract`.

---

## 8. Synthesis: which laws can constrain a design?

An engineer needs a law that returns **a number and a tolerance** for a stated design. That number can
be compared and the design can fail the check. Most of the famous laws in this catalogue do not do that.

### 8.1 USABLE: they give a checkable number, with a stated regime

| Law | What you check | Tolerance or band | Read-level of the number | Do not use when |
|---|---|---|---|---|
| **Strouhal number** (§4.2) | St = fA/U of a cruising oscillatory propulsor, with **A peak-to-peak** | 0.2–0.4 for cruising animals [R abstract]. Sharper for cetaceans, 0.20–0.30 (74% of 248 values) [R abstract]. Birds 0.21–0.25 [R abstract] | abstract, plus preprint full text (Eloy) | Re ≲ 10⁴, elongate or small swimmers (optimum up to 0.8, Eloy) [R]; hovering; manoeuvring; A convention not stated |
| **Hagen–Poiseuille** (§2.1) | ΔP or Q for a tube | exact | textbook [M] | Re > ~2000; pulsatile (Womersley α ≫ 1); blood below ~0.3 mm (Fåhræus–Lindqvist) [R] |
| **Murray / Hess–Murray** (§2.2) | the branching exponent n in r_p^n = Σr_c^n | n = 3 for small, laminar, single-function vessels. Coronary pooled 2.39 (CI 2.24–2.54) [R full-text]. About 2 in the aortic arch [R] | full-text meta-analysis | large arteries, turbulent or pulsatile flow, conduits that also bear load (conifers), lymphatics [R] |
| **Reynolds number** (§4.1) | the flow regime | regime boundaries | derivable | never "fails", but you must state L and U |
| **Froude number, gait** (§4.4a) | the speed of the walk–run transition | Fr ≈ 0.5 for bipeds; Fr ≤ 1 for pendular walking [R abstract / D] | abstract | non-cursorial mammals [R]; quadruped gait boundaries are only [M] |
| **Froude efficiency** (§4.4b) | η = 2/(1 + V_j/U) | exact, within momentum theory | derivable | pulsed and vortex-ring jets [M] |
| **Lighthill efficiency** (§4.5) | η = (1 + U/V)/2 and the thrust sign (V > U) | model output | abstract / preprint | lunate tails, h/L < 0.1, rays and boxfish [R] |
| **Beam theory and I** (§3.1) | stiffness, sag, and the tube-against-rod gain | exact for slender beams | derivable | local buckling of thin walls; short beams |
| **Greenhill buckling** (§3.3) | H_crit for a column | plants stand at H/H_crit ≈ 1/4 (111 species) [R abstract] | abstract | tall trees, which hit the hydraulic limit (122–130 m) first [R]; wind loads |
| **Ashby indices** (§3.5) | rank materials for tie, beam or plate | exact given E, ρ, σ | derivable (no biological property values retrieved here) | anisotropic, hierarchical materials; shape that cannot scale freely |
| **Bone strain envelope** (§3.4) | peak working strain | 2000–3000 µε peak across species [R, secondary]. Frost bands 100–300 / 1500–3000 µε [R abstract] | abstract / secondary | hormonal and age shifts; the 3000 µε microdamage threshold is [M] |
| **Skeletal safety factor** (§3.2) | peak stress ÷ failure stress | 2–4 [R abstract], over 0.1–300 kg | abstract | above ~300 kg, and small animals where stiffness governs [R] |
| **Cost of transport** (§4.7) | incremental COT = 10.7·M^{−0.316} J kg⁻¹ m⁻¹ | ±25% for 90% of 62 species [R abstract] | abstract | non-linear speed ranges, hopping, inclines [M] |
| **Turing conditions** (§6.1) | whether a *given kinetic model* is linearly unstable, and k_c | exact for 2-species linear stability [D] | derived | **as a test of an organism.** Linear stability does not predict whether a pattern forms (subcritical patterns, repo rule 4). The diffusivity-ratio requirement disappears with ≥3 species [R] |
| **Golden angle** (§6.3) | divergence angle of a spiral organ array | 137.5077640500° [D]. About 18% non-Fibonacci parastichy counts are normal in sunflowers [R] | full-text | distichous and whorled systems; organ permutations in ~half of co-initiated cases in *Arabidopsis* [R] |
| **Soaring size limit** (§5.3) | mass of an albatross-like soarer | 41 kg (CI 26–75) [R full-text] | full-text | flapping fliers and alternative launch mechanics (pterosaurs reached 200–250 kg) [R] |
| **Adder** (§7.3) | slope of division size against birth size | 1 (adder), 0 (sizer), 2 (timer); *S. pombe* 0.25 ± 0.02 [R] | full-text | slow-growing *E. coli*; fission yeast; small budding-yeast daughters. **And the slope alone does not identify the mechanism** [R] |

### 8.2 DESCRIPTIVE: they cannot constrain a design

| Law | Why it cannot be used as a check |
|---|---|
| **Kleiber / 3/4 law** (§1.3) | It is an interspecific regression. It does not say what any single design must consume. The exponent itself is contested: 0.67–0.75 for mammals depending on data and method; ≈1–2 for unicells; curved over the full mammal range. Over the mouse–elephant range, the 2/3 vs 3/4 choice changes predictions by 2.7×. **Use it only to ask whether a design sits inside the observed scatter of real organisms, and quote the dataset.** |
| **WBE derivation** (§1.3) | It is a model of why the regression might hold. Its assumptions (invariant terminal units, a space-filling fractal network) are disputed on mathematical (Kozłowski & Konarzewski) and empirical (Kolokotrones; DeLong) grounds. The derivation cannot be used as a constraint while the observation it explains is in dispute. |
| **Rubner surface law** (§1.2) | It is a geometric argument for homeotherms at rest. It gives no tolerance, and it does not apply to ectotherms, plants or unicells. |
| **Huxley allometry** (§1.1) | It is a fitting form. Its exponent depends on the clade, the level (ontogenetic, static, evolutionary) and the regression method, and the log transform can create breakpoints that are not real (Packard). It becomes usable only once someone supplies a specific exponent with its CI and clade, e.g. Sato's seabird span M^{0.37 (0.34–0.40)}. |
| **Elastic similarity** (§3.2) | Mammal limb bones do **not** follow it (0.35/0.36 against 0.25/0.375) except in bovids. It is a hypothesis of a design rule; real animals achieve size-independent stress through posture instead. |
| **Wolff's law** (§3.4) | It is qualitative. Only Frost's threshold bands make it checkable, and those are in §8.1. |
| **D'Arcy Thompson transformations** (§6.2) | They show that a map exists between two forms. They predict nothing. |
| **Fractal dimension** (§6.4) | It holds over 1–2 decades of scale at best. Coral D values were not even retrievable here. It describes texture and cannot exclude a design. Leonardo's Δ in 1.8–2.3 is the exception, and it could be promoted to §8.1 as a loose check on mechanical branching. |
| **von Bertalanffy / Gompertz** (§7.1–7.2) | They are curve families with free parameters. They fit growth after it happens. von Bertalanffy demonstrably fails before maturity (Lester et al.). |
| **Pennycuick power curve** (§5.1) | It is a *model* that computes a number (V_mp, V_mr) once you supply k, S_b, C_Db and the profile power. That can be a design calculation, but it is not a biological check: measured curves range from acutely concave to flat. Use it to compute, not to validate. |
| **Wing loading scaling** (§5.2) | Its exponents depend on the clade and flight mode, and only one CI-bearing set was retrieved (procellariiforms). It describes; it does not constrain outside the clade it was fitted on. |
| **Gazzola swimming number** (§4.3) | It is potentially usable, but **it was not verified this session** (`metadata` only). Do not use it until it is read. |

### 8.3 The pattern behind the split

The laws that survive as constraints are **dimensionless groups and exact mechanics**: St, Re, Fr,
Poiseuille, beam theory, buckling, Ashby indices and linear stability. They are tied to a physical
mechanism with a known domain, so the regime where they break can be stated in advance.

The laws that do not survive are **interspecific regressions** (Kleiber, Huxley, wing loading) and
**curve families** (von Bertalanffy, Gompertz). They summarise what evolution produced, inside a
scatter band, for the taxa sampled. A regression can tell you that a design is *unlike* known
organisms. It cannot tell you that the design will *fail*.

---

## 9. Open items, in priority order

1. **Taylor, Nudds & Thomas 2003 to full text.** Retrieve the species count, the fraction of species
   inside 0.2–0.4, the operational definition of "cruising" and the exact definition of A. This is the
   project's load-bearing number, and it stands at `abstract` level today.
2. Triantafyllou et al. 1993 to full text, to confirm the 0.25–0.35 band directly rather than via Eloy.
3. Gazzola et al. 2014 (swimming number). Read it before using it in any check.
4. The Kleiber 1932/1947 text and the source of the "70 kcal d⁻¹ M^{0.75}" constant.
5. Murray 1926 and Uylings 1977, to confirm the cost function and the turbulent 7/3 directly.
6. Savage et al. 2004: its exponent and CI, needed so the 3/4 side carries a retrieved number of the same
   quality as the 2/3 side's.
7. Kozłowski & Konarzewski 2004: its argument from the text, not from memory.
8. Greenhill 1881 and McMahon 1973, for the buckling constant and the tree data.
9. Biological material property values (Wegst & Ashby 2004), so §3.5 can carry worked numbers.
10. Coral fractal dimensions (Martin-Garin et al. 2007).
11. The White & Seymour and DeLong quotes were extracted by a summariser. String-match them against the
    PMC XML.

Upgrading most of these needs nature.com, cambridge.org, journals.biologists.com, pnas.org, Wiley,
Springer, rupress.org and royalsocietypublishing.org allowed in the network policy, or institutional
access.
