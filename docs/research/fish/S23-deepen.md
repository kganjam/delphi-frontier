# S23-D — Deepening S23 by attacking its weakest input

Parent: `S23` (protein), *"Can actinotrichia be stiffened by gain-of-function, given only
loss-of-function is demonstrated?"*. The parent answer is in commit `6d1b84ed` on branch
`claude/s23-actinotrichia-stiffness-protein-wwp5m2`, file `docs/research/fish/S23-protein.md`
(read in full for this work). The task prompt passed the recorded answer as an empty string, so I
worked from that file.

Date of work: 2026-11-04. Reproduction: `python3 docs/research/fish/S23-deepen-calc.py`.
**Everything in §1 and §4 is computation, not observation.**

---

## 0. The parent conclusion, as an inequality

S23 concluded that protein-level stiffening of actinotrichia cannot close the stiffness gap S6
needs. Put as arithmetic, it claims

```
margin  =  S / C  >  1
S = EI_req / EI_meas          (shortfall: required vs measured fin bending stiffness)
C = E_target / E0             (material ceiling: best plausible modulus / actinotrichial modulus now)
EI_req = (W/2) L^2 / (8 * tol)   (uniform-load cantilever, tip deflection = tol * L)
```

(The parent also discounts by `f`, the actinotrichial share of fin `EI`: gain = `1 + f(C−1)`.
Because `f ≤ 1`, setting `f = 1` is the case most favourable to gain-of-function. I use `f = 1`
throughout, so any result that holds here holds for every `f`.)

## 1. Which input is the answer most sensitive to? (computed)

Every input enters `S/C` as a multiplicative factor, so on a log scale **each has the same
elasticity**. A factor-of-two error in any single one changes the margin by exactly 2× (`L`
by 4×, because it enters squared). Recomputed from the parent's central case (`L` = 4 cm,
tol = 10 %, `EI_meas` = 4×10⁻⁹ N·m², `C` = 25):

| perturbation (factor 2) | margin `S/C` | flips? |
|---|---|---|
| none (parent central case) | 39.2 | — |
| `EI_meas` ×2 | 19.6 | no |
| tolerance ×2 | 19.6 | no |
| body mass ÷2 | 19.6 | no |
| semi-span `L` ÷2 | 9.8 | no |
| `C` ×2 (i.e. `E0` ÷2) | 19.6 | no |

So at the central case **no single factor-of-two error flips it**. Sensitivity therefore has
to be judged by asking which input is uncertain by much more than 2×. To flip the central case
an input has to be wrong by about 39×. In the most lenient corner the parent itself names
(`L` = 2 cm, tol = 50 %, and the upper value 5×10⁻⁹ N·m² given in Puri 2018's conclusions),
`S` falls to 39 and the margin is close to 1. That makes it **sensitive to factors of 2**:

| `E0` → `E_target` | `C` | margin, lenient corner | margin, central case |
|---|---|---|---|
| 0.5 GPa → 5 GPa | 10 | 3.92 | 98.1 |
| 0.2 GPa → 5 GPa (parent's choice) | 25 | **1.57** | 39.2 |
| 0.2 GPa → 10 GPa | 50 | **0.785 — flips** | 19.6 |
| 10 MPa → 10 GPa | 1000 | 0.039 — flips | **0.98 — flips** |
| 1.2 MPa → 5 GPa | 4167 | 0.009 — flips | 0.24 — flips |

How uncertain is each input?

- `EI_meas` is **measured**: Puri et al. 2018, read at `full-text` (re-read for this work). The
  paper reports two slightly different ranges, 1.5–4×10⁻⁹ N·m² in the abstract and 2–5×10⁻⁹
  N·m² in the conclusions. I keep both. The spread is about 3×.
- `L`, tolerance and mass are **design assumptions**. They are soft, but the parent states their
  range (2–4 cm, 5–50 %), which spans 40×.
- `E0`, the actinotrichial modulus, is **neither measured nor bounded**. The parent took it
  from AFM work on generic collagen fibrils, read at `search-summary`. The values it carried
  run from 1.2 MPa to 0.5 GPa, a ~400× spread. That spread **straddles the flip threshold**,
  which is computed here as `E0* = E_target / S`: 5–10 MPa at the central case and 127–255 MPa
  at the lenient corner.

**`E0` is the weakest input.** It is the only one whose stated range crosses the flip
threshold even at the central case. A factor-two error in it (0.2 → 0.1 GPa, or a
silk-grade target instead of dry collagen) flips the lenient corner.

**A finding about the parent, computed from its own ranges:** the parent's headline,
"one to two orders of magnitude short", **does not hold across the ranges the parent states**.
At its own lenient corner, pairing `E0` = 0.2 GPa with its own 10 GPa silk-like target gives a
margin of 0.785. That means the parent's arithmetic, carried through, allows gain-of-function
to close the gap there. The parent got its ceiling of 20–25× by pairing the low `E0` with the
low target and the high `E0` with the high target. It never computed the low–high pairing
(50×).

## 2. How well is `E0` established? (honest read)

- **Evidence level for `E0` in the parent: `assumption via proxy`.** No study of actinotrichia
  or elastoidin was used. The number is a generic type-I collagen fibril modulus from AFM
  studies that the parent read only at `search-summary` (PMC2257912, PMC4213719,
  encyclopedia.pub 21308). It is a **proxy**, and repetition makes it read as measured.
- **Direct measurement of actinotrichial modulus: none found.** Scope of this negative, from my
  own searches on 2026-11-04 (web index only, English, extended mode):
  `actinotrichia stiffness measured Young's modulus zebrafish fin fold atomic force microscopy
  2023 2024 2025` and `ceratotrichia elastoidin tensile strength Young's modulus shark fin
  mechanical`. Neither turned up a modulus for actinotrichia. I did not query PubMed, Web of
  Science or bioRxiv systematically. The parent's §2.5 negative (five queries, same index)
  stands as it was.
- **The proxy measures the wrong quantity (my inference, from the method descriptions).** The
  MPa-scale values (Yadavally 1.2 MPa with a Hertzian fit, 5–10 MPa with DMT) are **AFM
  indentation** moduli. Indentation loads a fibril *transversely*. Bending a rod depends on the
  *axial* (tensile) modulus, and collagen fibrils are strongly anisotropic. I take this as a
  physical reason to set aside the MPa branch for an `EI` calculation. It is an inference: I did
  not read those papers beyond search summaries, and I have not checked each one's loading
  geometry.

## 3. Improving it: the real material is elastoidin

Actinotrichia are elastoidin. The parent cites ZFIN ZDB-PUB-110425-4 and reviews for this, all
at `search-summary`. Shark ceratotrichia are the same material class and, unlike zebrafish
actinotrichia, have been tested in tension.

- **Rajaram A, Sanjeevi R, Ramanathan N (1981). *J. Biosci.* 3(3):303–309.** I could not
  confirm the title (see below). Read-level: **`search-summary`**. Both `www.ias.ac.in` (the
  full text) and `link.springer.com` returned `ENOTFOUND` from this sandbox. They need to be
  allowed in the session's network settings before the paper can be read.
  - **Authors' claim (as given in the search summary):** elastoidin fibres were *stronger* than
    rat-tail tendon when dry and *weaker* when wet, and "**elastoidin was stiffer than tendon
    whether dry or wet**". Hydrated elastoidin has "comparatively low tensile strength".
    Elastoidin is about 80 % collagen.
  - **Sources disagree on wet strength vs stiffness, and both are kept:** wet elastoidin is
    *weaker* than tendon but *stiffer*. That is coherent. Strength and modulus are different
    quantities, and `EI` depends only on modulus.
  - I could not get the actual modulus value. It is **`unknown`**.
- **The comparison tissue, wet rat-tail tendon, axial tensile modulus.** Read-level:
  `search-summary`, from a search for wet and dry rat-tail tendon tensile modulus on 2026-11-04.
  Fibril tangent modulus is **350 ± 53 MPa wet** and 2720 ± 840 MPa dry. Fibre-level wet
  specimens are cited at 0.48–0.57 GPa. I do not know which tendon preparation the 1981 study
  used.
- **Arumugam V, Sanjeevi R (1987). "Effect of strain rate on the mode of fracture in
  elastoidin." *J Mater Sci* 22:2691–2694.** Read-level: `search-summary` (abstract text only).
  It shows that dry and native (wet) elastoidin have been tensile-tested. The summary gave no
  number.

**Improved input (my inference, conditional):** if the 1981 "stiffer than tendon, wet" claim
applies to a tendon whose wet axial modulus is at least the fibril value of about 0.35 GPa, then

```
E0 (elastoidin, wet, axial)  ≳  0.35 GPa        — lower bound, not a measurement
```

This is a **proxy-species lower bound** (shark ceratotrichia, not zebrafish actinotrichia). It
rests on a qualitative claim that I read only at `search-summary` level. It is still a better
input than the parent's, for three reasons. It concerns the right material (elastoidin, not
generic collagen). It concerns the right loading mode (axial tension, not indentation). And two
independent lines (§2 last bullet, §3) both rule out the MPa branch that flipped the central
case.

Its weaknesses, listed again in full: ceratotrichia are far larger than zebrafish
actinotrichia, and the actinotrichial diameter is `unknown` to this analysis. The
non-collagenous partner proteins in shark and zebrafish elastoidin may differ, and I have no
sequence comparison. The tendon reference value is assumed, not read.

## 4. Recompute (computed)

With `E0 ≥ 0.35 GPa` and the parent's two targets, the ceiling is `C` ≤ 14 (dry-collagen 5 GPa)
or ≤ 29 (silk-like 10 GPa), at `f` = 1:

| case | `S` | `C` (max) | margin | verdict on the inequality |
|---|---|---|---|---|
| central (4 cm, 10 %, 4×10⁻⁹) | 981 | 29 | **34.3** | holds |
| lenient corner (2 cm, 50 %, 5×10⁻⁹) | 39.2 | 29 | **1.37** | holds, barely |
| lenient corner, dry-collagen target | 39.2 | 14 | 2.75 | holds |
| flip requires `E0` below | — | — | 255 MPa (lenient) / 10 MPa (central) | improved bound is above both |

- At the central case the conclusion now holds with a margin of about 34×, against about 39×
  in the parent, but the branch that could flip it is gone.
- At the lenient corner the conclusion holds at about 1.4×, where the parent's own ranges
  allowed it to fail (0.785). The headline "**1–2 orders of magnitude short**" is still
  **not supported** at that corner. The honest statement is: short by about 1.4× to about 34×,
  depending on design assumptions S23 does not control. This is a lower bound on the margin
  only while `E0 ≥ 0.35 GPa` holds.
- `f < 1` makes every margin larger. Nothing here relies on `f`.

## 5. What measurement would settle `E0`, and what it would cost

- **Measurement:** the axial tensile or bending modulus of single hydrated zebrafish
  actinotrichia. Isolate them from larval fin folds or regenerating adult fin margins, by
  collagenase-free dissection or as fin-fold "needles". Then either test them by AFM
  three-point bending of a fibre suspended across a micro-fabricated trench (a standard
  single-fibril method), or by microtensile testing in buffer. Report the hydration state, and
  report diameter by SEM or TEM.
- **Decision rule (computed above):** the conclusion falls at the lenient corner if
  `E0` < 255 MPa and at the central case if `E0` < 10 MPa (silk-like target).
- **Cost:** my estimate, not sourced. It needs about one to three person-months of a postdoc
  with AFM access, wild-type larvae (no new line), and core-facility AFM time. That is likely
  on the order of US$10⁴. The cheaper first step costs nothing: read Rajaram et al. 1981 in full
  once `www.ias.ac.in` is reachable, and record its wet elastoidin modulus. That number would
  replace the inequality in §3.

## 6. Verdict

**STANDS.** Recomputed with the improved `E0` (a conditional lower bound of ≥ 0.35 GPa for wet
elastoidin), protein-level stiffening of actinotrichia still does not close the S6 stiffness
gap, even at `f` = 1 and at the most lenient design corner. I do not call it *strengthens*,
for three reasons:
1. The improved input is a `search-summary`-level qualitative claim plus an assumed reference
   value, not a number I read.
2. The parent's stated magnitude ("1–2 orders short") **falls** at its own lenient corner. The
   surviving margin there is about 1.4×.
3. The input is still a proxy species.

The *direction* of the parent answer stands, and its *magnitude* claim has to be narrowed.

## Sources

- Parent: `docs/research/fish/S23-protein.md` @ `6d1b84ed`. Read-level: `full-text`.
- [Puri et al. 2018, *J Exp Biol* 221:jeb171777, PMC5868929](https://pmc.ncbi.nlm.nih.gov/articles/PMC5868929/).
  Read-level: `full-text` (main text, re-read 2026-11-04). Supplementary Fig. S5:
  `could-not-access`. No numeric ray modulus appears in the main text.
- [Rajaram, Sanjeevi, Ramanathan 1981, *J. Biosci.* 3:303–309](https://www.ias.ac.in/article/fulltext/jbsc/003/03/0303-0309).
  Read-level: `search-summary`. Direct fetch: `could-not-access` (host not resolvable from the
  sandbox).
- [Elastoidin tensile/fracture record, Springer BF02702941](https://link.springer.com/article/10.1007/BF02702941).
  Read-level: `listing`. Direct fetch: `could-not-access`. I could not confirm the title or
  authors.
- Arumugam & Sanjeevi 1987, *J Mater Sci* 22:2691–2694. Read-level: `search-summary`.
- Wet and dry rat-tail tendon moduli:
  [ScienceDirect 0142961289900070](https://www.sciencedirect.com/science/article/abs/pii/0142961289900070),
  [ScienceDirect S175161611830897X](https://www.sciencedirect.com/science/article/abs/pii/S175161611830897X).
  Read-level: `search-summary`. I cannot say which source supplied which number in the summary.
- Collagen fibril AFM moduli (the parent's proxy): PMC2257912, PMC4213719, encyclopedia.pub
  21308. Read-level: `search-summary` (as recorded in the parent; not re-read).

```swarm-result
{"subproblem": "S23-D", "evidence": "derived",
  "answer": "The answer is most sensitive to the actinotrichial baseline modulus E0, the only input whose stated range (1.2 MPa-0.5 GPa) crosses the computed flip threshold (10-255 MPa); replacing the generic-collagen AFM proxy with an elastoidin lower bound (wet elastoidin reported stiffer than wet tendon, search-summary) keeps the conclusion that protein-level stiffening cannot close the S6 gap, but only by ~1.4x at the lenient design corner, so the parent's '1-2 orders short' magnitude is overstated.",
  "key_number": "E0 (wet elastoidin, axial) >= ~0.35 GPa, conditional lower bound inferred from a qualitative search-summary claim plus a wet rat-tail-tendon fibril modulus of 350 +/- 53 MPa; flip threshold 255 MPa (lenient) / 10 MPa (central)",
  "verdict": "stands"}
```
