# Replication 248: S23-D actinotrichial baseline modulus `E0` and the lenient-corner margin

Date: 2026-11-04. Reproduction: `python3 -I docs/research/fish/replicate-248-calc.py`.
**Everything in §3 and §4 is computation, not observation.**

## 0. Process disclosure (read this first)

- The task pointed to `replicate-181.md` on branch `claude/s23-d-actinotrichia-modulus-87c1ku`
  for the inputs. I read its **first 30 lines** to learn what the question was. Those lines exposed
  two things: the recorded value for *claim 181* (S23-D: flip threshold 10–255 MPa, margin ~1.4×),
  and the fact that replicate-181 says ~1.4× "does not" reproduce. **I stopped reading at that point.**
  I did not see replicate-181's own number, its table of inputs, or its arithmetic until §5 below.
- After that I read §0 of `S23-deepen.md` (lines 1–29), on branch
  `claude/deepen-s23-actinotrichia-bhvko5`, for the model. I did **not** read its sensitivity
  tables, its §1–§4, or its calc script.
- I read the parent `S23-protein.md` in full, on branch
  `claude/s23-actinotrichia-stiffness-protein-wwp5m2`, for the design grid and the measured inputs.
  The parent's own conclusion is in that file: a 20–25× ceiling, "1–2 orders short".
- I ran my own web searches for the elastoidin and wet-tendon moduli (§2).
- **Independence caveat.** My searches came back with the same 1981 *J. Biosci.* elastoidin
  abstract and the same 2019 *Front. Bioeng. Biotechnol.* review that replicate-181 cites (I found
  this out in §5). So my inputs are re-retrieved, not independently sourced. This agreement shows
  the arithmetic and the input choices can be reproduced. It does not show that the inputs are right.

## 1. Model (taken from S23-D §0, and the parent §3.1)

```
margin = S / C      (>1 means protein-level stiffening cannot close the S6 gap)
S      = EI_req / EI_meas
C      = E_target / E0      (f = 1, the case most favourable to gain-of-function)
EI_req = (W/2) L^2 / (8 tol)      (uniform-load cantilever, tip deflection = tol × L)
flip threshold: E0* = E_target / S   (the margin equals 1 here)
lenient corner = smallest S together with the largest C
```

## 2. Inputs

| input | value | source | read-level |
|---|---|---|---|
| mass | 0.4 g, so `W` = 3.924e-3 N | parent S6 premise | design assumption |
| `L` | 2, 4 cm | parent §3.1 | design assumption |
| `tol` | 5, 10, 20 % (50 % is mentioned in parent §5 as a sensitivity) | parent | design assumption |
| `EI_meas` | 1.5–4×10⁻⁹ N·m² | Puri et al. 2018 *J Exp Biol* 221:jeb171777, as the parent quotes it | `listing` for me (the parent reports `full-text`). I did not re-open the paper |
| `E_target` | 5 GPa (dry collagen), 10 GPa (silk-like) | parent §3.2 | `search-summary` (parent) |
| `E0`, generic collagen proxy | 1.2 MPa – 0.5 GPa (AFM, hydrated fibril; the spread is ~500× and I preserve it) | parent §2.6 | `search-summary` (parent) |
| elastoidin vs tendon | the authors claim elastoidin is stiffer than rat-tail tendon **both wet and dry**. No number reached me | Rajaram, Sanjeevi & Ramanathan 1981, *J. Biosci.* 3(3):303–309, doi:10.1007/BF02702941 | `search-summary`. Full text `could-not-access`: both `www.ias.ac.in` and `link.springer.com` gave ENOTFOUND from this sandbox |
| wet rat-tail tendon fibre | 0.57 GPa (Kato 1989); hydrated fibre 1.17 GPa (Gentleman 2003) | as cited in Front. Bioeng. Biotechnol. 2019, 10.3389/fbioe.2019.00085 | `search-summary` |
| tendon fascicle | 0.48, 0.55, 0.64 GPa (the snippet does not confirm hydration) | same review | `search-summary` |
| elastoidin or actinotrichia modulus as a number | **unknown** | searched "elastoidin Young's modulus fin ray shark ceratotrichia mechanical" (extended) and "elastoidin tensile modulus dry tail tendon J. Biosci. 1981" (extended), web index, 2026-11-04. The two full-text fetches failed (see above). Scope: web index only, no PubMed, no WoS | — |

**`E0` lower bound (my inference, not an observation).** Suppose the 1981 authors' claim holds,
that elastoidin is stiffer than tendon when wet (I have it only at search-summary level), and that
actinotrichia are elastoidin. Then `E0 ≥ E_wet tendon` ≈ **0.48 GPa** (fascicle, hydration not
confirmed) to **0.57 GPa** (fibre, wet). These two sources differ, and I do not average them.

## 3. Arithmetic (computed)

```
W          = 0.4e-3 × 9.81 = 3.924e-3 N ; W/2 = 1.962e-3 N
EI_req     = 1.962e-3 × L^2 / (8 tol)
  2 cm, 20 %: 1.962e-3 × 4e-4 / 1.6 = 4.905e-7 N m^2
  4 cm,  5 %: 1.962e-3 × 1.6e-3 / 0.4 = 7.848e-6 N m^2
S range    = 4.905e-7 / 4e-9 = 122.6   …   7.848e-6 / 1.5e-9 = 5232
Flip E0*   = E_target / S
  lenient (S=122.6): 10 GPa → 81.5 MPa ; 5 GPa → 40.8 MPa
  strict  (S=5232) : 5 GPa  → 0.96 MPa ; 10 GPa → 1.91 MPa
  (with tol = 50 %: S = 1.962e-7/4e-9 = 49.05 → E0* = 204 MPa at 10 GPa)
Lenient-corner margin = S_min × E0 / E_target  (E_target = 10 GPa)
  E0 = 0.48 GPa: C = 20.8 ; margin = 122.6/20.8 = 5.89
  E0 = 0.57 GPa: C = 17.5 ; margin = 122.6/17.5 = 6.99
  E0 = 1.17 GPa: C = 8.5  ; margin = 14.3
  (tol 50 %: 49.05/20.8 = 2.35 ; 49.05/17.5 = 2.80)
Generic AFM proxy instead of the elastoidin bound:
  E0 = 1.2 MPa → margin 0.015 ; 10 MPa → 0.12 ; 0.2 GPa → 2.45 ; 0.5 GPa → 6.13
```

## 4. My value

**Lenient-corner margin ≈ 6× (5.9–7.0×). This is computed, at the parent's grid corner: 2 cm,
20 % tolerance, `EI_meas` = 4×10⁻⁹ N·m², `E_target` = 10 GPa, `E0` ≥ 0.48–0.57 GPa.** If the
tolerance is extended to 50 %, the margin falls to 2.35–2.8×. On the parent grid the flip
threshold `E0*` is 0.96–81.5 MPa, and 204 MPa at 50 % tolerance.

Uncertainty. The margin is >1 only while `E0` stays above ~82 MPa (or 204 MPa at 50 %). The AFM
Hertz/DMT figures of 1.2–10 MPa would flip the sign, since they give a margin <1. My only reason
for putting `E0` near 0.5 GPa is a qualitative claim that I read at search-summary level. So the
sign is conditional on an unverified input.

## 5. Comparison with the recorded value (read only after §3–§4)

Replicate-181 records (§4 of that file) a lenient-corner margin of **≈2.4× (2.35–2.8×) at the
50 %-tolerance corner, or ≈6–7× (5.9–7.0×) at the parent's 20 % corner**, with `E0 ≥ 0.48–0.57 GPa`,
and a flip threshold of ≈1–204 MPa.

- 20 % corner: mine is 5.89 / 6.99 and theirs is 5.9 / 7.0. **Match.**
- 50 % corner: mine is 2.35 / 2.80 and theirs is 2.35–2.8. **Match.**
- Flip threshold: mine is 0.96 / 81.5 / 204 MPa and theirs is 0.96 / 81.5 / 204 MPa. **Match.**

**AGREE**, with the independence caveat from §0. Both of us found the same search-summary
sources, so this agreement checks the arithmetic and how the inputs were chosen. It does not
independently confirm the inputs. Replicate-181 records two disagreements with S23-D's ~1.37×
(`EI_meas` upper 5e-9 vs 4e-9, and wet-fibril floor 0.35 vs 0.48–0.57 GPa). I did not surface either
of S23-D's values, and I cannot settle that disagreement. I preserve it here.

## Sources

- `S23-protein.md` (parent), read in full. `S23-deepen.md` §0 only. `replicate-181.md` lines 1–30
  before I derived, the rest after.
- [Rajaram et al. 1981, J. Biosci. 3:303–309](https://www.ias.ac.in/article/fulltext/jbsc/003/03/0303-0309) / [doi:10.1007/BF02702941](https://link.springer.com/article/10.1007/BF02702941) — `search-summary`. Full text `could-not-access` (ENOTFOUND). `www.ias.ac.in` would have to be allowed in the session network settings.
- [Front. Bioeng. Biotechnol. 2019, 10.3389/fbioe.2019.00085](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2019.00085/pdf) — `search-summary`.
- Puri et al. 2018, *J Exp Biol* 221:jeb171777 — `listing` (through the parent).

```swarm-replication
{"claim_id": 248, "my_value": "lenient-corner margin S/C ≈ 5.9–7.0x (2 cm, 20 % tol, EI_meas 4e-9 N m², E_target 10 GPa, E0 ≥ 0.48–0.57 GPa); 2.35–2.8x at 50 % tol; flip threshold E0* 0.96–81.5 MPa (204 MPa at 50 %)", "agrees": true,
  "note": "Every number reproduces exactly, but my searches found the same search-summary sources for the wet-tendon E0 floor, so this confirms the arithmetic and input choices, not the inputs themselves."}
```
