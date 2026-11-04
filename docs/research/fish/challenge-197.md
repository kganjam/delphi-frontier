# Challenge 197 — adversarial review of S13 (fin-ray flexural rigidity / protein stiffness)

**Claim under review:** `harvest:s13-protein-fin-ray-e8y8d8`, recorded evidence level `derived`.
**Reviewer:** Claude Code (automated), 2026-11-04. I did not write the claim.
**Verdict: WEAKENED.** The headline negative survives, but the quantitative argument
stated as its reason is wrong by roughly two orders of magnitude, and the specific
"10¹–10² GPa vs 10–30 GPa ceiling" leg does not survive.

> Read-levels used below: `full-text` | `abstract` | `listing` | `search-summary` | `could-not-access`.
> Every number in §1 and §3 is **computed by me**; none is an observation. Arithmetic script:
> `docs/research/fish/challenge197_arith.py` (`python3 -I docs/research/fish/challenge197_arith.py`).

---

## 1. Independent arithmetic — reproduces, no defect here

Recomputed from the claim's stated inputs without consulting the author's working
(`m = 0.4 g`, `S = 4×10⁻⁴ m²`, `C_L = 0.8`, `ρ = 1.225`, `b/2 = 0.02 m`, cantilever UDL,
δ = 10% semi-span). **All computed:**

| Quantity | My value | Author's value | Agree? |
|---|---|---|---|
| `W` | 3.924×10⁻³ N | 3.924×10⁻³ N | ✓ |
| `V` | 4.474 m·s⁻¹ | 4.47 m·s⁻¹ | ✓ |
| `Re` (c = 0.01) | 2.98×10³ | ~2.98×10³ | ✓ |
| `w` | 0.0981 N·m⁻¹ | 0.0981 N·m⁻¹ | ✓ |
| `EI_req` | **9.810×10⁻⁷ N·m²** | 9.81×10⁻⁷ N·m² | ✓ |
| gap vs 1.5/2.75/4.0×10⁻⁹ | **654× / 357× / 245×** | 654/357/245× | ✓ |

The KEY number as recorded — `EI_req 9.8e-7 N m²` vs measured `1.5–4e-9 N m²`, a
245–654× gap — **survives independent recomputation.** The formula choice
(δ = wL⁴/8EI for a cantilever under UDL) is also correct. I found no arithmetic error.

The defect is not in the arithmetic. It is in the step *after* it.

---

## 2. The break: the GPa requirement is unit-inconsistent and double-counts

The claim moves from "245–654× in `EI`" to "would need a ray modulus of 10¹–10² GPa"
by multiplying the EI *ratio* by a ray-material modulus *baseline*:

- hydrated collagen fibril 0.3 GPa × 357 = 107 GPa
- teleost whole-ray ~1.0 GPa × 357 = 356 GPa

**This is not a valid operation, and it is self-contradictory against the claim's own
measured inputs.** `E_baseline × (EI_req/EI_measured)` equals the required modulus only
if the tissue *currently* achieves `E_baseline` at the measured `I_eff`. Test that
(computed by me):

| Assumed baseline `E` | Implied `EI` at measured `I_eff = 5×10⁻¹⁶` | vs measured mid 2.75×10⁻⁹ |
|---|---|---|
| 0.3 GPa | 1.50×10⁻⁷ N·m² | **55× too high** |
| 1.0 GPa | 5.00×10⁻⁷ N·m² | **182× too high** |

The measured pair (`EI = 1.5–4×10⁻⁹`, `I_eff = 3–7×10⁻¹⁶`, both Puri et al. 2018,
**read-level: full-text**, re-verified by me today) *forces* an effective modulus of
**2.1–13.3 MPa** — which the claim itself computes in its §3.4 and then sets aside.
So baselines of 0.3–1 GPa are incompatible with the measured state by 55–182×.
Multiplying them by 357 charges the material for the architectural loss **twice**.

**The unit-consistent requirement** is `E_req = EI_req / I_eff`, using Puri's own
measured `I_eff` (all computed by me):

| `I_eff` (measured, m⁴) | Required effective modulus |
|---|---|
| 7×10⁻¹⁶ (proximal) | **1.40 GPa** |
| 5×10⁻¹⁶ | **1.96 GPa** |
| 3×10⁻¹⁶ (distal) | **3.27 GPa** |

**≈1.4–3.3 GPa, not 10¹–10² GPa.** Compare the ceilings the claim itself cites
(its §2.4, read-level: search-summary): silk 1–10 GPa; dry collagen fibril 2–7 GPa,
5–11.5 GPa by nanoindentation; teleost whole-ray 0.24–3.7 GPa; single collagen triple
helix 0.35–25 GPa; amyloid 10–30 GPa. **The corrected requirement sits inside every
one of those ranges and about an order of magnitude below the amyloid ceiling.**

The "above the ~10–30 GPa ceiling for the stiffest protein solids" leg — the leg that
makes this a hard No and the one carried in the claim's answer sentence — **is refuted.**
It is an artifact of the ratio-times-baseline step, not a property of protein materials.

---

## 3. Hidden assumption, relaxed

The claim names its own most load-bearing arbitrary choice (δ = 10% of semi-span) and
is right to. Relaxing it (computed by me):

| Allowable tip deflection | `EI_req` | gap vs 1.5–4×10⁻⁹ | unit-consistent `E_req` (÷ I_eff 3–7×10⁻¹⁶) |
|---|---|---|---|
| 10% semi-span (claim) | 9.81×10⁻⁷ | 245–654× | 1.40–3.27 GPa |
| 20% | 4.91×10⁻⁷ | 123–327× | 0.70–1.64 GPa |
| 40% | 2.45×10⁻⁷ | 61–164× | 0.35–0.82 GPa |

At every deflection criterion the required *effective* modulus is ≤3.3 GPa. The claim's
own §6 says the answer "would start to wobble" at ~10–30×; under the corrected framing
it wobbles at the author's *chosen* criterion, not only at a relaxed one.

---

## 4. The proxy

**A proxy is standing in for the quantity that matters, in two places.**

**(a) Comparator.** `EI_req` is for a **wing spar**. The measured 1.5–4×10⁻⁹ N·m² is a
whole **caudal fin** — a propulsive membrane 5–8 mm wide whose compliance is functional,
measured transversely in vivo. Using a compliant propulsor's `EI` as the baseline a
load-bearing spar must be scaled up from inflates the apparent materials burden. The
right comparator is a **pectoral** fin ray (the actual wing candidate) or a designed spar.

**(b) The decisive baseline is absent, and the claim knows it.** The ray material's `E`
is `could-not-access`. I re-fetched Puri et al. 2018 (**full-text**, PMC5868929) today
and confirm: **no Young's modulus is reported for the bony ray material**; Fig. S5C is
referenced in the text only as showing that effective modulus "consistently showed a
peak," with no number. The 4 ± 2 kPa is interray tissue (authors call it an upper bound);
the 200 ± 10 GPa and 2.0–2.2 GPa figures are steel and polyimide **calibration
cantilevers**. The claim is correct to flag this trap and correct that the number is
unavailable.

---

## 5. Counter-examples the claim missed or mis-sourced

**(a) Published teleost fin-ray `EI` already meets or exceeds `EI_req`** (computed by me
from reported values):

| Reported value | Source / read-level | vs `EI_req` 9.81×10⁻⁷ |
|---|---|---|
| 3.8×10⁻⁶ N·m², bluegill rays | Puri et al. 2018 Conclusions, **full-text** | **3.9× the requirement** |
| 565×10⁻⁶ N·m², bluegill pectoral fin ray | Flammang et al. 2013 abstract, **abstract** (via search; full text unreachable) | **576× the requirement** |

**My inference, separate from any author's claim:** ordinary teleost fin rays — fish
collagen plus mineral, no novel protein — reach flexural rigidities at or above what this
glide load case demands. **Stated scope and caveat:** both values are *Lepomis macrochirus*,
a ~15 cm fish with much thicker rays, and `EI ∝ d⁴`. This therefore establishes that the
binding constraint is **size and geometry at zebrafish scale**, not the modulus ceiling of
protein materials. It does **not** establish that a zebrafish-scale ray can reach 9.81×10⁻⁷.

**(b) Sourcing correction to the claim's "150× discrepancy."** The claim reports Puri
et al. as "citing Flammang et al. 2013 for bluegill: 3.8×10⁻⁶ N·m²." Re-reading Puri
(**full-text**): the sentence citing Flammang is *"Previous measurements of bending
stiffness of larger fish have reached a **sensitivity** of 10⁻⁶ N m² (Flammang et al.,
2013)"* — that is instrument sensitivity, not a stiffness measurement. The 3.8×10⁻⁶
figure appears separately in Puri's Conclusions and **is not cited to Flammang there**.
So the claim's framing of this as two conflicting reports of one quantity is a misreading.
**Disagreement preserved, not averaged:** 565×10⁻⁶ (Flammang abstract) and 3.8×10⁻⁶
(Puri Conclusions) still differ ~150× and I could not resolve which structure each refers
to. **Negative-search scope:** I attempted the Flammang full text at two mirrors
(`web.njit.edu`, `public.websites.umich.edu`); both failed DNS resolution from this
session and would need allowing in its network settings. Not resolved.

**(c) Architecture multiplies stiffness without touching `E` — published.** Nguyen et al.,
"Curvature-induced stiffening of a fish fin" (arXiv:1608.05891, **read-level: abstract**;
the PDF is a 5.5 MB compressed stream I could not extract text from). The abstract states
*"changing the fin's curvature modulates its stiffness,"* by misalignment of principal
bending axes between neighbouring rays coupling ray bending to membrane stretching.
**No numerical factor is given in the abstract and I do not quote one.** This is direct
published support for the claim's "architecture-limited" observation — and simultaneously
evidence that the available lever is architectural, which is what makes the claim's
molecular-ceiling arithmetic the wrong test.

---

## 6. Is the evidence level honest?

`derived` is the right level for the mechanical argument, and the source document is
unusually scrupulous: it labels its computations as computations, marks AlphaFold output
as prediction, reports the Collagen Stability Calculator as `refused` by the environment
rather than fabricating a ΔTm, and invents no sequence. On the honesty floor it is
largely exemplary, and I want that on the record.

**One defect at the floor, in the claim sentence itself.** The claim says "against a
**measured** ~10–30 GPa ceiling for the stiffest protein solids." Per the claim's own
§2.4, the 18–30 GPa Aβ(1-40) figure is **modelling**, and the actual AFM *measurement*
cited there is an insulin fibril at **3.3 ± 0.4 GPa**. The source document flags this
(its §5, item 9: "partly computational in origin"); the harvested claim sentence does not,
and calls it measured. A partly-simulated ceiling presented as measured is a defect even
when the number is defensible — and here it matters doubly, because the real measured
value (3.3 GPa) is *below* my corrected requirement band's top (3.27 GPa), i.e. the
honest measured ceiling and the honest requirement are the same order of magnitude.

---

## 7. What survives

- The arithmetic, and the KEY number: `EI_req ≈ 9.8×10⁻⁷` vs measured `1.5–4×10⁻⁹`,
  **245–654×**. Fully reproduced.
- **"Architecture-limited rather than molecule-limited."** This survives and I
  strengthened it: the measured (`EI`, `I_eff`) pair forces `E_eff ≈ 2–13 MPa` against a
  molecular modulus ≥0.3 GPa, a ~10²× assembly loss; and Nguyen et al. (abstract)
  independently show curvature alone modulates fin stiffness.
- The narrow conclusion that **raising a collagen's molecular modulus is not the effective
  lever** therefore survives — but via the architecture leg, not the ceiling leg.
- Honest `unknown` on designability: no stability run was executed. I did not execute one
  either and report none.

## 8. What does not

- **"Would need a ray modulus of 10¹–10² GPa."** Refuted. Unit-consistent requirement is
  **1.4–3.3 GPa** (0.35–0.82 GPa at a 40% deflection criterion).
- **"Against a measured ~10–30 GPa ceiling … so a stiffer protein variant is
  insufficient."** The ceiling argument fails: the corrected requirement is inside the
  cited protein-solid ranges, so this reasoning cannot carry the negative.
- The robustness statement "any baseline ≥0.1 GPa fails" — the only *measured*
  modulus-like quantity at the right scale is the claim's own 2–13 MPa, which is
  **below** that floor and points the other way, as the claim's own §6 item 1 concedes.

**Why "weakened" and not "refuted":** the answer's direction ("no, not via a stiffer
protein molecule") is still defensible on the architecture leg, and the KEY number is
correct. But the claim should not be relied upon for the ceiling argument, and any
downstream work that cites "protein materials top out below what's needed" is citing a
refuted step. A corrected S13 would read: *the requirement is ~1.4–3.3 GPa effective,
which protein solids reach; the tissue is ~100× below that not because its molecules are
too soft but because its assembly dissipates stiffness, so the live levers are
architectural (cross-linking, segment fusion, curvature, mineral fraction) — some of
which are reachable by sequence change, making the protein route under-tested rather
than excluded.*

**I did not manufacture feasibility.** None of the above shows a zebrafish-scale glider is
achievable. It shows the specific impossibility argument offered does not hold, which
leaves the question open, not answered yes.

---

## Provenance

- Re-fetched today, **full-text**: Puri et al. 2018, *J Exp Biol* 221(4):jeb171777
  (PMC5868929) — confirmed `EI` 1.5–4×10⁻⁹ N·m², `I_eff` 7→3×10⁻¹⁶ m⁴, interray
  4 ± 2 kPa, the Flammang-sensitivity sentence, the 3.8×10⁻⁶ Conclusions figure, and that
  no ray-material modulus is given in text (Fig. S5C numberless in text).
- **abstract**: Flammang et al. 2013 *J Morphol* 274:1044–1059, 565×10⁻⁶ N·m² (via search
  summary of the abstract); Nguyen et al. arXiv:1608.05891.
- **Unreachable:** `web.njit.edu`, `public.websites.umich.edu` (DNS resolution failure —
  would need allowing in this session's network settings); arXiv PDF text extraction failed.
- All arithmetic reproducible from `docs/research/fish/challenge197_arith.py`.
- No number, citation, accession or gene symbol in this file was invented. Unavailable
  values are marked `could-not-access` or `unknown`.

```swarm-challenge
{"claim_id": 197, "outcome": "weakened", "reason": "Arithmetic and the 245-654x EI gap reproduce exactly, but the step to '10^1-10^2 GPa required' multiplies the EI ratio by a ray-material baseline that is itself 55-182x inconsistent with the measured EI/I_eff pair, double-counting the architectural loss; the unit-consistent requirement EI_req/I_eff is 1.4-3.3 GPa, inside the cited protein-solid moduli, so the 10-30 GPa ceiling leg fails while the architecture-limited leg survives.",
  "corrected_value": "E_eff required = 1.4-3.3 GPa (EI_req 9.81e-7 N m^2 / measured I_eff 3-7e-16 m^4); 0.35-0.82 GPa at a 40%-semispan deflection criterion. Not 10^1-10^2 GPa.",
  "depends_on": ["Puri et al. 2018 measured whole-caudal-fin EI = 1.5-4e-9 N m^2 (full-text, re-verified)", "Puri et al. 2018 measured effective area moment of inertia I_eff = 3-7e-16 m^4 (full-text, re-verified)", "zebrafish adult mass 0.4 g and g = 9.81 m/s^2", "glide load-case assumptions S = 4e-4 m^2, C_L = 0.8, rho = 1.225 kg/m^3, semi-span 0.02 m, cantilever under uniformly distributed load", "the 10%-of-semi-span allowable tip deflection criterion (author's choice, not biological)", "reported protein-solid Young's moduli: silk 1-10 GPa, dry collagen fibril 2-7 GPa, hydrated fibril 0.2-0.8 GPa, teleost whole-ray 0.24-3.7 GPa, amyloid 10-30 GPa (search-summary; the 18-30 GPa amyloid figure is modelling, the AFM measurement is 3.3 +/- 0.4 GPa)", "bluegill fin-ray EI values 3.8e-6 N m^2 (Puri Conclusions, full-text) and 565e-6 N m^2 (Flammang et al. 2013 abstract) - mutually unresolved by ~150x", "Nguyen et al. arXiv:1608.05891 curvature-induced stiffening, abstract only, qualitative"]}
```
