# Replication 295 — S40: fin-mesenchyme membrane conductance required by a syncytial length-constant model

**Independent re-derivation.** I did not read the other agent's working. The harvest branch for
this claim, `claude/s40-cell-membrane-conductance-oar3jg`, exists on the remote; I saw its name in
`git ls-remote` and deliberately did not fetch, check out or read it. Nothing from it is used here.
The repository working tree contains no inputs for this claim (`seeds/frontier-data.json` has no
fin, mesenchyme or syncytium nodes), so every number below is either my own arithmetic or comes
from a cited source with its read-level marked.

---

## 1. What I derived

A **calculated** (not observed) feasibility window for the specific membrane conductance of a
gap-junction-coupled fin mesenchyme, if that syncytium is to sustain a ≥10 mV proximodistal
bioelectric difference:

| quantity | my value |
|---|---|
| feasible window, central parameter case | **7.4 × 10⁻⁸ – 7.1 × 10⁻⁶ S/cm²** |
| feasible window, full envelope over my parameter grid | **1.5 × 10⁻¹⁰ – 1.4 × 10⁻⁴ S/cm²** |
| log-centre of that envelope | **≈ 1.4 × 10⁻⁷ S/cm²** |
| implied length constant λ (central case) | 0.17 – 1.65 cm |

Uncertainty: the window spans ~4.9 orders of magnitude end to end. The ceiling scales as
σ_eff · β⁻¹ · L⁻², so it is dominated by the assumed domain length L (quadratically) and by the
assumed syncytial coupling σ_eff (linearly). I give the sensitivity explicitly in §2.4. This is a
feasibility envelope, not a measurement, and it is not a prediction of what fin mesenchyme actually
does — no such measurement exists (§4).

---

## 2. The model and the arithmetic in full

### 2.1 Model

Treat the coupled mesenchyme as a continuum (3-D syncytial cable). With

* σ_eff = effective syncytial conductivity of the tissue (S/cm), including junctional resistance,
* β = membrane area per unit tissue volume (cm⁻¹),
* g_m = specific membrane conductance (S/cm²),

the steady-state length constant is

    λ = sqrt( σ_eff / (β · g_m) )          … (1)

and a potential imposed at one end of a long domain decays as V(x) = V₀ · exp(−x / λ).

*This is my inference from standard cable theory, not an author's claim about fin.* Equation (1) is
the 3-D form of the one-dimensional λ = sqrt(a·R_m / 2ρ_i); β replaces the surface-to-volume
factor 2/a and σ_eff replaces 1/ρ_i.

### 2.2 The ≥10 mV requirement, two-sided

A proximodistal **difference** of at least 10 mV across a domain of length L requires two things of
the same λ, and they pull in opposite directions:

* **Signal must arrive.** V(L) ≥ 10 mV ⇒ exp(−L/λ) ≥ 10/V₀ ⇒ λ ≥ L / ln(V₀/10).
  Substituting into (1): **g_m ≤ σ_eff · ln²(V₀/10) / (β L²)** — a ceiling on conductance.
* **A gradient must exist.** V₀ − V(L) ≥ 10 mV ⇒ λ ≤ L / ln(V₀/(V₀−10)).
  Substituting into (1): **g_m ≥ σ_eff · ln²(V₀/(V₀−10)) / (β L²)** — a floor on conductance.

Too leaky and the signal dies before it crosses the field; too tight and the field is isopotential
and carries no ≥10 mV difference at all. Hence a two-sided window, which is why a lower bound
appears at all. (The requirement is satisfiable only if V₀ ≥ 20 mV.)

### 2.3 Inputs

| input | value used | basis | read-level |
|---|---|---|---|
| L, proximodistal domain | 0.16 – 1.0 cm; central 0.3 cm | adult zebrafish caudal-fin / regenerate proximodistal scale (mm to ~1 cm) | my assumption, order-of-magnitude anatomy; not measured here |
| σ_eff, syncytial conductivity | 1 × 10⁻⁴ – 2 × 10⁻³ S/cm; central 1 × 10⁻³ | ρ_eff 500–10 000 Ω·cm. Upper end = best-coupled excitable syncytium (cytoplasm ~100–200 Ω·cm plus junctions); lower end = weakly coupled mesenchyme | my assumption; **no fin value exists** (§4) |
| β, membrane area / tissue volume | 3000 – 7500 cm⁻¹; central 5000 | spheres of diameter 8–15 µm (6/d) at ~0.7 packing. 13–15 µm is the measured L-cell diameter (§3.1) | my calculation from an assumed geometry |
| V₀, available drive | 30 – 100 mV; central 60 mV | transmembrane drive of order a resting potential | my assumption |

No input in this table is a measurement of fin mesenchyme. That is the central weakness of the
model, and it is a property of the literature, not of my parameter choices.

### 2.4 Worked central case

L = 0.3 cm, σ_eff = 1 × 10⁻³ S/cm, β = 5000 cm⁻¹, V₀ = 60 mV.

    ln(60/10)      = 1.79176     ln²  = 3.21039
    ln(60/50)      = 0.182322    ln²  = 0.0332812
    β L²           = 5000 × 0.09 = 450 cm^-1 · cm^2 = 450 cm

    ceiling g_m = 1e-3 × 3.21039 / 450 = 3.21039e-3 / 450 = 7.134e-6  S/cm^2
    floor   g_m = 1e-3 × 0.0332812 / 450 = 3.32812e-5 / 450 = 7.396e-8 S/cm^2

    λ at the ceiling = sqrt(1e-3 / (5000 × 7.134e-6)) = sqrt(2.804e-2) = 0.1675 cm
    λ at the floor   = sqrt(1e-3 / (5000 × 7.396e-8)) = sqrt(2.704)    = 1.645 cm

Check: L/ln(60/10) = 0.3/1.79176 = 0.1674 cm ✓ and L/ln(60/50) = 0.3/0.182322 = 1.646 cm ✓.

**Central window: 7.4 × 10⁻⁸ – 7.1 × 10⁻⁶ S/cm².** Its log-centre is
sqrt(7.396e-8 × 7.134e-6) = 7.3 × 10⁻⁷ S/cm².

### 2.5 Envelope over the whole grid

Grid: L ∈ {0.16, 0.3, 0.5, 1.0} cm × σ_eff ∈ {2e-3, 1e-3, 3e-4, 1e-4} S/cm ×
β ∈ {3000, 5000, 7500} cm⁻¹ × V₀ ∈ {30, 60, 100} mV (144 combinations).

    highest ceiling: L=0.16, sigma=2e-3, beta=3000, V0=100
      = 2e-3 × ln(10)^2 / (3000 × 0.0256) = 2e-3 × 5.30190 / 76.8 = 1.381e-4 S/cm^2
    lowest floor:    L=1.0,  sigma=1e-4, beta=7500, V0=100
      = 1e-4 × ln(100/90)^2 / (7500 × 1.0) = 1e-4 × 0.0110979 / 7500 = 1.480e-10 S/cm^2

    envelope: 1.5e-10 .. 1.4e-4 S/cm^2 ;  log-centre sqrt(1.480e-10 × 1.381e-4) = 1.43e-7 S/cm^2

Sensitivity: halving L raises the ceiling 4×; a 20× range in σ_eff moves it 20×; the 2.5× range in
β moves it 2.5×; V₀ from 30 to 100 mV moves it 4.8×. L dominates, and L is the input the model is
least entitled to pick freely.

Script: `/tmp/claude-0/-workspace-delphi-frontier/16a39b9c-d9d5-5486-8197-b0863b5d1579/scratchpad/sweep2.py`
(scratch, not committed; all arithmetic above is reproducible by hand from §2.2).

---

## 3. The two measured surrogates

### 3.1 Mouse L-cell fibroblasts

Hosoi S, Slayman CL. *Membrane voltage, resistance, and channel switching in isolated mouse
fibroblasts (L cells): a patch-electrode analysis.* J Physiol 1985 Oct;367:267–290.
doi:10.1113/jphysiol.1985.sp015824. PMID 2414439, PMCID PMC1193063.
**Read-level: abstract** (PMC serves only the abstract plus references; the body is page images I
could not read. `pubmed.ncbi.nlm.nih.gov` and `physoc.onlinelibrary.wiley.com` do not resolve from
this session and would have to be allowed in the session's network settings.)

Authors' claim, quoted: "The associated slope conductivity of the cell membrane was 5-15
microS/cm2", on "assumed smooth-sphere geometry, cells 13-15 microns in diameter", with
"(zero-current) membrane potentials of -50 to -75 mV".

    g_m (L cells) = 5e-6 .. 1.5e-5 S/cm^2

Two scope caveats the abstract itself supplies, which I will not average away:

* It is a **slope** conductance near rest, K⁺-dominated, in an **isolated suspension-cultured**
  cell line — not a mesenchyme in situ.
* With ≥0.1 mM free Ca²⁺ in the pipette the same cells gave "slope conductivities of 200-400
  microS/cm2", i.e. **2 × 10⁻⁴ – 4 × 10⁻⁴ S/cm²** — forty-fold higher, and above every ceiling in
  §2. Whether resting fin mesenchyme sits in the low-Ca²⁺ or the high-Ca²⁺ state is not known, and
  the choice swings the comparison from "feasible in one corner" to "infeasible everywhere".

### 3.2 Cardiac fibroblasts in situ

The in-situ figure is not published as a conductance per unit area; I **calculated** it from a
measured resistance and a measured area.

Inputs, all from Quinn TA, Camelliti P, Rog-Zielinska EA, *et al.* / Kohl P *et al.* review
*"Fibroblast–myocyte electrotonic coupling: does it occur in native cardiac tissue?"*
(PMC4001130), **read-level: full-text** of the first 100 000 characters:

* in-situ fibroblast membrane resistance **0.5–1 GΩ**, the review citing Kohl et al. 1994
  (Exp Physiol) and Kamkin et al. 2002 (Am J Physiol Heart Circ Physiol) — *review's attribution,
  read-level for those primaries: could-not-access*;
* in-tissue surface area from an EM reconstruction of a rabbit sinoatrial-node fibroblast,
  "total surface area of this cell will have been 1500 μm2, or more", citing Demaziere et al. 1992;
* capacitance of isolated fibroblasts "typically 6–10 pF", citing Dawson et al. 2012 and
  Chilton et al. 2005.

Independent cross-check of the resistance, read-level **search-summary** only: a search result
quoted Kamkin et al. (Am J Physiol Heart 2001, postinfarction bradycardia) as "Em of –22±2 mV and
an input resistance of 510±10 MΩ" in rat atrial fibroblasts in tissue, vs 10–40 MΩ for myocytes.
That is consistent with the review's 0.5–1 GΩ and I could not read the paper itself
(`journals.physiology.org` does not resolve from this session).

Arithmetic, g_m = 1 / (R_m · A):

    EM in-tissue area  A = 1500 um^2 = 1.5e-5 cm^2
      R = 1e9  ohm : g_m = 1/(1e9  × 1.5e-5) = 6.67e-5 S/cm^2
      R = 5e8  ohm : g_m = 1/(5e8  × 1.5e-5) = 1.33e-4 S/cm^2
    area from capacitance at 1 uF/cm^2:  6 pF -> 600 um^2 = 6e-6 cm^2 ; 10 pF -> 1e-5 cm^2
      R = 1e9, A = 1e-5  : 1.00e-4 S/cm^2
      R = 5e8, A = 1e-5  : 2.00e-4 S/cm^2
      R = 1e9, A = 6e-6  : 1.67e-4 S/cm^2
      R = 5e8, A = 6e-6  : 3.33e-4 S/cm^2

    g_m (cardiac fibroblast in situ) = 6.7e-5 .. 3.3e-4 S/cm^2

The two area routes disagree by ~2.5× (EM-measured 1500 µm² in tissue vs 600–1000 µm² inferred from
isolated-cell capacitance) and the review says so explicitly — in-situ capacitance is hard to
measure and "stands to reason" it exceeds the isolated range, which would push g_m *down* toward
the EM end. I report the union, 6.7 × 10⁻⁵ – 3.3 × 10⁻⁴ S/cm², rather than picking one.

### 3.3 Comparison with the window

| | value (S/cm²) | vs central ceiling 7.1e-6 | vs widest ceiling 1.4e-4 |
|---|---|---|---|
| required window (central) | 7.4e-8 – 7.1e-6 | — | — |
| L cells, resting | 5e-6 – 1.5e-5 | at to ~0.3 order above | ~1.0–1.4 orders **below** → feasible |
| L cells, ≥0.1 mM Ca²⁺ | 2e-4 – 4e-4 | ~1.5–1.8 orders above | above → infeasible |
| cardiac fibroblast in situ | 6.7e-5 – 3.3e-4 | ~1.0–1.7 orders above | at to ~0.4 order above → infeasible |

So: **both surrogates sit at or above the central requirement** (the mesenchyme they stand for would
be too leaky to hold 10 mV over a 3 mm field at these coupling strengths). In the
narrow-domain/strong-coupling corner (L ≈ 1.6 mm, σ_eff = 2e-3 S/cm, β = 3000 cm⁻¹, V₀ = 100 mV)
the ceiling rises to 1.4e-4 and the **resting L-cell** value sits about 1.0–1.4 orders below it,
i.e. comfortably feasible; the cardiac in-situ value is still at or above it.

Consequence, my inference: the measured surrogates do **not** refute the claim from below. Nothing
measured shows mesenchyme to be *tighter* than the model needs, which is the direction that would
kill the gradient by making the tissue isopotential; and at least one surrogate falls inside the
window in a corner of parameter space that is not absurd. The claim is also not supported — see §4.

---

## 4. Negative searches, with their scope

* **Fin-mesenchyme membrane conductance (or specific membrane resistance, or resting potential by
  direct recording): not found.** Scope: WebSearch, extended mode, zebrafish fin mesenchyme /
  blastema patch clamp, membrane potential, resting conductance, electrophysiology. The nearest
  work is indirect: the blastema Ca²⁺ paper (PMC11370486 / PMC13078715, **read-level:
  search-summary**) uses GCaMP imaging, single-cell transcriptomics and channel blockers, and
  reports Ca²⁺ spikes on depolarization in isolated regenerating fin fibroblasts, but no whole-cell
  resting conductance; and *kcnk5b*/*alf* fin-size work (PLoS Genet 10.1371/journal.pgen.1004080,
  **read-level: search-summary**) reports a −90 to −100 mV shift for mutant channels in *Xenopus*
  oocytes, i.e. heterologous expression, not fin cells.
* **Fin gap-junction conductance in fin tissue: not found.** Scope: WebSearch, extended mode,
  zebrafish fin connexin / cx43 / *short fin* / cx40.8 coupling and conductance. All quantitative
  coupling data I located are heterologous: junctional conductance in paired *Xenopus* oocytes and
  qualitative dye coupling in HeLa cells for cx43 *sof* and *stp* alleles (Hoptak-Solga et al. 2007;
  Misu et al. 2016 — **read-level: search-summary** for both; the review's own words are that the
  dye assay "is strictly qualitative"). No σ_eff for fin mesenchyme follows from these.

Therefore σ_eff and β in §2.3 are unconstrained by fin data, and the model's requirement cannot be
confronted with a fin measurement at all. **C2 is not settled.**

Access limitations to record: `pubmed.ncbi.nlm.nih.gov`, `physoc.onlinelibrary.wiley.com`,
`europepmc.org` (403) and `journals.physiology.org` were unreachable from this session; they would
need to be allowed in the session's network settings. `www.ncbi.nlm.nih.gov/books` returned a
CAPTCHA page.

---

## 5. Comparison with the recorded value

The prompt carries the recorded range, so I can compare directly (the derivation above was
completed before writing this section and does not depend on it).

| | recorded | mine | gap |
|---|---|---|---|
| window, widest | 1 × 10⁻⁹ – 4.8 × 10⁻⁵ | 1.5 × 10⁻¹⁰ – 1.4 × 10⁻⁴ | 0.8 order lower at the floor, 0.5 order higher at the ceiling |
| central case | ~2 × 10⁻⁷ | 1.4 × 10⁻⁷ (log-centre of envelope); 7.3 × 10⁻⁷ (log-centre of the central-parameter window) | factor 1.4 to 3.6 |
| L cells | 5–15 µS/cm² | 5 × 10⁻⁶ – 1.5 × 10⁻⁵ S/cm² | identical |
| cardiac fibroblast in situ | ~1 – 3.3 × 10⁻⁴ | 6.7 × 10⁻⁵ – 3.3 × 10⁻⁴ | identical at the top; mine extends 0.2 order lower via the EM area |
| surrogates vs window | above, except one ~1 order below in the narrow/strong corner | above, except resting L cells 1.0–1.4 orders below in that corner | same conclusion |
| C2 status | not refuted from below, not settled | not refuted from below, not settled | same |

Note on the recorded "central case ~2e-7": sqrt(1e-9 × 4.8e-5) = 2.19e-7, so the recorded central
value appears to be the log-centre of the recorded endpoints rather than an independently computed
case. I therefore compared it against the log-centre of my own envelope (1.4e-7), which is where
the factor-1.4 agreement comes from.

**Verdict: AGREE.** The endpoints match within one order of magnitude on a window that is itself
~5 orders wide, both surrogate values reproduce (one exactly, one to the top of its range), the
sign of the comparison is the same in every corner, and both derivations reach the same two-part
conclusion: not refuted from below, not settled. I did not reconstruct the recorded parameter grid,
and my ceiling is more permissive than the recorded one mainly because I admit a 1.6 mm domain; a
grid that starts at ~2 mm reproduces 4.8e-5 closely. The agreement is on the result, not on the
grid.

What would settle C2, and nothing short of it: a whole-cell or sharp-electrode recording of
specific membrane conductance in fin mesenchyme in situ, plus a junctional conductance (or an
effective tissue conductivity) measured in fin tissue rather than in oocytes.

```swarm-replication
{"claim_id": 295, "my_value": "required g_m 1.5e-10 to 1.4e-4 S/cm2 (log-centre ~1.4e-7; central-parameter window 7.4e-8 to 7.1e-6 S/cm2)", "agrees": true,
  "note": "Independently re-derived the two-sided syncytial length-constant window and both surrogates; endpoints agree within one order on a ~5-order window, surrogates reproduce, and the same verdict follows: C2 not refuted from below and not settled, since no fin-mesenchyme membrane or gap-junction conductance exists."}
```
