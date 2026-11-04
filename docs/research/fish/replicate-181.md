# Replication 181 — S23-D: actinotrichial baseline modulus `E0` and the lenient-corner margin

Date: 2026-11-04. Reproduction: `python3 -I docs/research/fish/replicate-181-calc.py`.
**Everything in §3 and §4 is computation, not observation.**

## 0. Process disclosure

- The task said where the inputs live: branch `claude/deepen-s23-actinotrichia-bhvko5`. I read
  only §0 of `S23-deepen.md` there (lines 1–29). That section defines the inequality
  `margin = S/C`. **I stopped reading at that point**, before its sensitivity tables and its recompute.
- Then I read the **parent** file, `S23-protein.md` on `claude/s23-actinotrichia-stiffness-protein-wwp5m2`,
  for the design grid and the measured inputs. The parent's own result is in that file (20–25× ceiling, "1–2 orders short").
  I had to read it to get the inputs, so it is not hidden from me.
- I ran my own searches for the elastoidin and wet-tendon values, without help from the S23-D text.
- I read the S23-D calc script and §1–§4 **only after** finishing §3–§4 below, so I could do the comparison in §5.
- The question text itself states the recorded answer (flip threshold 10–255 MPa; margin ~1.4×). I could not avoid seeing it.

## 1. Model (taken from S23-D §0 and parent §3.1)

```
margin = S / C            (>1  ⇒ protein-level stiffening cannot close the S6 gap)
S      = EI_req / EI_meas
C      = E_target / E0     (f = 1, the case most favourable to gain-of-function)
EI_req = (W/2) L^2 / (8 tol)          uniform-load cantilever, tip deflection = tol·L
flip threshold:  E0* = E_target / S   (margin = 1)
```

## 2. Inputs, with source and read-level

| input | value(s) | source | read-level |
|---|---|---|---|
| body mass `m` | 0.4 g | parent S6 design premise | design assumption |
| `W` | 0.4e-3 × 9.81 = 3.924e-3 N | computed | — |
| semi-span `L` | 2 cm, 4 cm | parent §3.1 grid | design assumption |
| tip-deflection tolerance `tol` | 5, 10, 20 % (parent table); 50 % (parent §5 caveat) | parent | design assumption |
| `EI_meas` | 1.5–4×10⁻⁹ N·m² | Puri et al. 2018 *J Exp Biol* 221:jeb171777, as quoted in the parent | parent reports `full-text`. For me it is `listing` (via the parent). I did not re-open the paper |
| `E_target` | 5 GPa (dry collagen), 10 GPa (silk-like) | parent §2.6/§3.2 | `search-summary` (parent) |
| `E0`, generic proxy | 1.2 MPa – 0.5 GPa | parent §2.6 AFM table | `search-summary` (parent) |
| claim that elastoidin is stiffer than tendon, wet or dry | qualitative only, no number | 1981 tensile study of shark-fin elastoidin vs rat-tail tendon (*J. Biosci.* 3(3):303–309, ias.ac.in) | **`search-summary`**. Full text was `could-not-access`: `www.ias.ac.in` returned ENOTFOUND from this sandbox |
| wet rat-tail tendon (RTT) fibre modulus | 0.57 ± 0.08 GPa (Kato et al. 1989); hydrated fibre 1.17 ± 0.28 GPa (Gentleman et al. 2003) | cited in a 2019 *Front. Bioeng. Biotechnol.* review (10.3389/fbioe.2019.00085) | `search-summary` |
| RTT fascicle modulus | 0.48–0.64 GPa (hydration not confirmed in the snippet) | same review | `search-summary` |
| tendon collagen initial modulus | ~1.2 GPa | Gosline et al. elastic-proteins review table | `search-summary` |
| elastoidin modulus as a number | **unknown** | Searched "elastoidin tensile modulus wet tendon comparison shark fin ray" (standard) and "elastoidin mechanical properties stiffer than tendon collagen ceratotrichia" (extended), web index, 2026-11-04. Fetching the 1981 full text failed | — |

**Improved `E0` lower bound.** This is my inference, not an observation. The authors claim elastoidin is stiffer than tendon when wet (I have this only at search-summary). If that holds, then `E0 ≥ E_wet tendon`. The lowest wet-tendon axial value I found is **0.48 GPa** (fascicle, hydration not confirmed). The lowest value with hydration confirmed is **0.57 GPa** (fibre). I carry both. I also show 1.17 GPa. The sources disagree about 2×, and I do not average them.

## 3. Arithmetic (computed)

```
EI_req(L=2cm, tol)  = 1.962e-3 × 4e-4 / (8 tol) = 9.81e-8 / tol
   tol 20 % → 4.905e-7 N m²      tol 50 % → 1.962e-7 N m²
EI_req(L=4cm, tol 5 %) = 7.848e-6 N m²
```

Flip threshold `E0* = E_target / S`:

| corner | `S` | `E0*` |
|---|---|---|
| strictest (4 cm, 5 %, `EI_meas` 1.5e-9, `E_target` 5 GPa) | 5232 | **0.96 MPa** |
| parent's central (4 cm, 10 %, 4e-9) | 981 | 5.1 MPa (5 GPa) – 10.2 MPa (10 GPa) |
| lenient, parent grid (2 cm, 20 %, 4e-9, 10 GPa) | 122.6 | **81.5 MPa** |
| lenient, extended (2 cm, 50 %, 4e-9, 10 GPa) | 49.1 | **204 MPa** |

So my flip threshold runs from about **1 MPa to 82 MPa** on the parent's 5–20 % grid, and up to **204 MPa** if a 50 % tolerance is allowed. The proxy range of 1.2 MPa–0.5 GPa crosses this threshold in every case. That confirms `E0` is the input that can flip the sign, and it is the only one that can.

Margin with the elastoidin lower bound, `margin = S × E0 / E_target`:

| corner | `S` | `E0` | `C` | margin |
|---|---|---|---|---|
| lenient, parent grid (2 cm, 20 %, 4e-9, 10 GPa) | 122.6 | 0.48 GPa | 20.8 | **5.9** |
| same | 122.6 | 0.57 GPa | 17.5 | **7.0** |
| lenient, extended (2 cm, 50 %, 4e-9, 10 GPa) | 49.1 | 0.48 GPa | 20.8 | **2.35** |
| same | 49.1 | 0.57 GPa | 17.5 | **2.8** |
| strict (4 cm, 5 %, 1.5e-9, 5 GPa) | 5232 | 0.48 / 0.57 GPa | 10.4 / 8.8 | 502 / 596 |

## 4. My value

**Margin at the lenient design corner, with an elastoidin lower bound: ≈ 2.4× (range 2.35–2.8×) at the 50 %-tolerance corner, or ≈ 6–7× at the parent's own 20 % corner.** This is computed, not observed. It is a lower bound on the margin only while `E0 ≥ 0.48 GPa`, which rests on a qualitative claim I could read only at search-summary level.

The direction of the claim reproduces. Every margin is above 1, so protein-level stiffening does not close the S6 gap at `f = 1`. The magnitude part of the claim also reproduces qualitatively. At the lenient corner the margin is under one order of magnitude, so "1–2 orders short" is overstated there. At the strict corner it is about 2.7 orders.

## 5. Comparison with the recorded value (read only after §3–§4)

Recorded: flip threshold 10–255 MPa (central to lenient); lenient-corner margin about **1.37×** (S = 39.2, C = 28.6).

The recorded result differs from mine for two input reasons. The arithmetic itself checks: 1.962e-7/5e-9 = 39.2, then 10/0.35 = 28.6, then 39.2/28.6 = 1.37.

1. **`EI_meas` upper value.** S-D uses 5×10⁻⁹ N·m², which it attributes to Puri 2018's *conclusions* section ("2–5×10⁻⁹"). I used only the parent's 1.5–4×10⁻⁹. I did not re-read Puri, so I **cannot tell** which upper value is right. This is a disagreement between sections of one source, and I am not resolving it. With 5e-9, my S at the 50 % corner becomes 39.2. That matches theirs.
2. **Wet-tendon floor for `E0`.** S-D uses a wet RTT *fibril* tangent modulus of 0.35 ± 0.053 GPa (search-summary). My search did not surface that number. The lowest wet values I found were 0.48 GPa (fascicle) and 0.57 GPa (fibre). This is a real disagreement between sources, and I preserve it: 0.35 vs 0.48–0.57 GPa.

If I adopt both of S-D's inputs, I get its 1.37×. With my inputs I get 2.35–2.8× (50 % corner) or 5.9–7.0× (20 % corner). The flip threshold differs for the same reasons: their 255 MPa is 10 GPa / 39.2, and mine is 204 MPa at 4e-9. My strict-corner threshold of 0.96 MPa is lower than their 10 MPa "central" figure only because I quote the strictest corner rather than the central one. At the central corner I get 5–10 MPa, which matches theirs.

**Verdict: DISAGREE on the number, AGREE on the conclusion.** I reproduce the sign: the conclusion holds and "1–2 orders" is overstated at the lenient corner. I do not reproduce the ~1.4× margin from independently sourced inputs. I get about 2.4× at the same 50 % corner. The difference is about 1.7× and comes from two input choices that neither of us read at full text: the upper `EI_meas` and the wet-tendon floor. Their 1.4× is the more conservative of the two bounds. Mine does not show theirs is wrong. It shows that the value depends on inputs that are not settled.

## Sources

- Parent S23 file, `S23-protein.md` (commit on `claude/s23-actinotrichia-stiffness-protein-wwp5m2`). Read in full for the inputs.
- S23-D file `S23-deepen.md`, §0 read before deriving. §1–§4 and the calc script read only for §5.
- [J. Biosci. 3(3):303–309 (1981), elastoidin vs rat-tail tendon](https://www.ias.ac.in/article/fulltext/jbsc/003/03/0303-0309) — `search-summary`. Full text `could-not-access` (ENOTFOUND; `www.ias.ac.in` would need to be allowed in the session's network settings).
- [Front. Bioeng. Biotechnol. 2019, 10.3389/fbioe.2019.00085](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2019.00085/pdf) — `search-summary` (Kato 1989 0.57 GPa wet fibre, Gentleman 2003 1.17 GPa, fascicle 0.48–0.64 GPa).
- [Gosline et al., elastic proteins review](https://typeset.io/pdf/elastic-proteins-biological-roles-and-mechanical-properties-465yebuol9.pdf) — `search-summary` (tendon collagen ~1.2 GPa).
- Puri et al. 2018 *J Exp Biol* 221:jeb171777 — `listing` (taken from the parent; not re-opened).

```swarm-replication
{"claim_id": 181, "my_value": "lenient-corner margin S/C ≈ 2.4x (2.35–2.8x at 2 cm/50 %/4e-9 N m²/10 GPa; 5.9–7.0x at the parent's 20 % corner) with E0 ≥ 0.48–0.57 GPa; flip threshold E0* ≈ 1–204 MPa", "agrees": false,
  "note": "Sign and 'orders-of-magnitude overstated' reproduce, but ~1.4x does not from independently sourced inputs. It needs S-D's EI_meas=5e-9 and a 0.35 GPa wet-tendon floor, which I could not verify; I found 0.48–0.57 GPa."}
```
