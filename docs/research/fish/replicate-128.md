# Replication 128: the flip threshold R* on the caudal-to-pectoral proxy ratio (S23-D-D)

Date: 2026-11-04. Branch: `claude/s23-d-ei-meas-ratio-5ec1bb`.
**Every number in §2 is calculated. None is an observation.**

## 0. What I read, and what I did not read

- **Parent S23-D**, `docs/research/fish/S23-deepen.md` and `S23-deepen-calc.py`, branch
  `origin/claude/deepen-s23-actinotrichia-bhvko5`. Read-level: `full-text`. This file is the
  source of the inequality and of every input except R.
- **Sibling S23-D-D**, `docs/research/fish/S23-D-deepen.md`, branch
  `origin/claude/deepen-s23-sensitive-input-hynbng`. Read-level: `full-text`. This is a
  *different* S23-D-D: it attacks actinotrichial span `a/L`, not `EI_meas`. I read it only as
  context. It does not contain R.
- **The claim's own working**, `docs/research/fish/S23-D-D-calc.py` on branch
  `origin/claude/s23-sensitive-input-melodp`. **I did not open it before deriving my value.**
  After deriving, I grepped it for the comparison in §4 only. That branch holds no `.md`
  write-up.

## 1. Inputs

| input | value | source | read-level | status |
|---|---|---|---|---|
| body mass m | 0.4 g | S23 design (via S23-D calc) | full-text (of S23-D) | design assumption |
| g | 9.81 m s⁻² | constant | — | — |
| semi-span L (lenient corner) | 2 cm | S23 design range 2–4 cm | full-text (of S23-D) | design assumption |
| tip-deflection tolerance (lenient) | 50 % | S23 design range 5–50 % | full-text (of S23-D) | design assumption |
| EI_meas (caudal, lenient) | 5×10⁻⁹ N m² | Puri et al. 2018 *J Exp Biol* 221:jeb171777, conclusions (abstract gives 1.5–4×10⁻⁹) | full-text **per S23-D**; I did not re-read it | measured, **caudal fin** |
| E_target | 10 GPa (silk-like) | S23/S23-D | full-text (of S23-D) | assumption |
| E0 | ≥ 0.35 GPa (350 ± 53 MPa wet RTT fibril) | S23-D §3, which reads it at `search-summary` | search-summary (2nd-hand) | conditional lower bound, proxy |
| f | 1 | S23-D | full-text | most favourable to gain-of-function |
| model | EI_req = (W/2)L²/(8·tol), gap closes iff R·EI_meas·C ≥ EI_req | S23-D | full-text | uniform-load cantilever |
| R ≡ EI_pectoral / EI_caudal | set to 1 implicitly in S23 and S23-D | my reading of S23-D: it uses caudal EI_meas as the wing EI with no conversion | full-text | **undeclared** |

**Bound on R.** Taft, Taft, Henck, Mehner 2018, "Variation in flexural stiffness of the
lepidotrichia within and among the soft fins of yellow perch under different preservation
techniques", *J Morphol* 279:1045–1057, doi:10.1002/jmor.20831. Read-level: **`abstract`**,
from Crossref's abstract field. A zendy.io copy was `could-not-access` (host not allowed in this
sandbox).
- Authors' claim, verbatim: "Pelvic‐fin rays were the stiffest, and pectoral fin rays the least
  stiff. The fin rays of the dorsal, anal, and caudal fins all had similar stiffness values,
  which were intermediate".
- **My inference:** if this per-ray ranking carries over to zebrafish and to whole-fin EI, then
  R ≤ 1. That needs three transfers the abstract does not license:
  - perch to zebrafish;
  - isolated-ray three-point bending to Puri's caudal-fin EI;
  - ray stiffness to fin stiffness, which also depends on ray count and spacing.
- The abstract gives no numbers. The magnitude of R is therefore `unknown`. Only the sign of
  ln R is suggested.

Search scope: one standard web search ("yellow perch fin ray flexural stiffness pectoral caudal
dorsal comparison") and one Crossref lookup. I made no search for zebrafish pectoral fin-ray EI.
So I make no claim that one does not exist.

## 2. Arithmetic (computed)

```
W       = 0.4e-3 kg × 9.81           = 3.924e-3 N
EI_req  = (W/2) L² / (8 tol)
        = 1.962e-3 × (0.02)² / (8 × 0.5) = 1.962e-3 × 4e-4 / 4 = 1.962e-7 N m²
S       = EI_req / EI_meas = 1.962e-7 / 5e-9          = 39.24
C       = E_target / E0   = 10 GPa / 0.35 GPa         = 28.571
With the pectoral wing EI = R · EI_meas:
margin(R) = EI_req / (R · EI_meas · C) = 39.24 / (28.571 R) = 1.3734 / R
Flip (margin < 1)  ⇔  R > R* = 1.3734
```

- **Central corner** (L = 4 cm, tol = 10 %, EI = 4×10⁻⁹): R* = 981 / 28.571 = **34.3**.
- **Uncertainty from E0 alone**, using 350 ± 53 MPa: R* spans **1.17 to 1.58** at the lenient
  corner. Because E0 ≥ 0.35 GPa is itself a *lower* bound, R* ≥ 1.373 holds conditionally on
  that bound.
- **Uncertainty from E_target:** with the 5 GPa dry-collagen target, C = 14.29 and
  R* = 2.75.
- **With R ≤ 1** (inferred from Taft 2018, abstract): margin(R) = 1.373/R ≥ 1.373. The parent's
  margins become lower bounds. The conclusion holds. The number does not move: an upper bound
  on R, with no lower bound, cannot raise the floor above the R = 1 value.

**My value:** R* = **1.37** (1.3734) at the lenient corner. Range 1.17–1.58 from the E0 spread.
2.75 with the 5 GPa target. 34.3 at the central corner. All dimensionless and all computed. A
pectoral/caudal EI error of **+37 %** (pectoral stiffer than caudal) flips the conclusion at
the lenient corner.

## 3. Qualitative findings I agree with independently

- EI_meas is a caudal-fin measurement used for a pectoral glide wing.
- Neither S23 nor S23-D declares a conversion ratio. That is R = 1 by default.
- Because every input enters as a multiplier, R has the same elasticity as E0. So the "weakest
  input" ranking turns on uncertainty, not on the model.
- The only same-species, same-method comparison I found (perch, `abstract`) points to R ≤ 1.
  That direction protects the conclusion.

## 4. Comparison with the recorded value (done only after §2)

- Recorded: R* = 1.35, "numerically unimproved at 1.353".
- Mine: R* = 1.373.
- **The cause is known.** After deriving, I grepped the claim's `S23-D-D-calc.py`. It
  hard-codes `C = 29` for "10 GPa / 0.35 GPa", which is a rounding of 28.571. Check:
  39.24 / 29 = 1.3531. That is exactly the recorded figure.
- S23-D's own prose gave the R = 1 margin as 1.37. That agrees with my value, not with 1.353.
  The flip error is therefore 37 %, not 35 %.
- The claim's definition of R (`EI_pectoral / EI_caudal`, flip at R > EI_req/(C·EI_caud)) is
  the same as mine.

**Verdict: AGREE** on the model, the definition of R, the direction of the bound, and the
conclusion (intact, margins become lower bounds, numerically unimproved). The 1.5 % numerical
difference lies well inside the E0 uncertainty band (1.17–1.58). It is still a real arithmetic
slip, not a disagreement about sources. The recorded 1.353 should read **1.373**, and "35
percent" should read **37 percent**.

```swarm-replication
{"claim_id": 128, "my_value": "R* = 1.373 (dimensionless; 1.17-1.58 over E0 = 350 +/- 53 MPa; 34.3 at central corner)", "agrees": true,
  "note": "Same model and conclusion; the recorded 1.353 comes from rounding C = 10/0.35 = 28.57 to 29 in the claim's script, so the correct lenient-corner flip threshold is 1.373 (a 37%, not 35%, error)."}
```
