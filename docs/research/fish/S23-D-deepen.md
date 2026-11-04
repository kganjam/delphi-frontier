# S23-D-D — Deepening S23-D by attacking its weakest input

Chain:
- `S23` (protein) asked whether actinotrichia can be stiffened by gain-of-function. File
  `docs/research/fish/S23-protein.md` @ `6d1b84ed`, branch
  `claude/s23-actinotrichia-stiffness-protein-wwp5m2`.
- `S23-D` deepened it. File `docs/research/fish/S23-deepen.md` @ `efff2517`, branch
  `claude/deepen-s23-actinotrichia-bhvko5`.

I read both files in full. The task prompt passed the recorded answer as an empty string, so
I worked from those two files.

Date of work: 2026-11-04. Reproduction: `python3 docs/research/fish/S23-D-deepen-calc.py`.
**Every number in §1, §3.3 and §4 comes from a calculation, not an observation.**

---

## 0. What S23-D concluded, and what it rests on

S23-D says protein-level stiffening of actinotrichia cannot close the S6 stiffness gap. It
argues this with the inequality `margin = S / C > 1`:

- `S = EI_req / EI_meas` is the stiffness shortfall.
- `C = E_target / E0` is the most the modulus could plausibly be raised.
- `f = 1` is the share of fin `EI` attributed to actinotrichia.

At its lenient design corner (`L` = 2 cm, tolerance 50 %, `EI_meas` = 5×10⁻⁹ N·m²) the margin
was **1.37**. That corner rests on a *conditional lower bound* `E0 ≥ 0.35 GPa`, built from:
- a qualitative claim, read at `search-summary`, that wet elastoidin is "stiffer than tendon";
- a wet rat-tail-tendon fibril modulus, also read at `search-summary`.

## 1. The most sensitive input — shown by recomputing (computed)

**Within S23-D's own framing.** At the lenient corner, the margin is 1.37. Halving `E0` to
0.175 GPa gives `C` = 10 GPa / 0.175 GPa = 57 and a margin of 39.2 / 57 = **0.69**. That
**flips** the conclusion. Doubling `E_target` flips it the same way. Every input enters as a
pure multiplier, so all of them have the same elasticity. Uncertainty decides which one is
weakest:
- `E0` is still a proxy-species inference with no number read.
- `EI_meas` is measured (Puri 2018, `full-text` per S23-D).
- `L` and tolerance are declared design choices.

So, inside the framing, **`E0` is the weakest input**, as S23-D said.

**The framing hides a stronger dependence.** `f = 1` means the actinotrichia carry the whole
measured fin `EI` along the whole span. It was chosen as "the case most favourable to
gain-of-function". It is favourable for the *share* of stiffness. It is silent on *where along
the span* that stiffness sits. In a cantilever, *where* matters more than *how much*.

**My inference:** the true most-sensitive input of S23-D is the **span fraction occupied by
actinotrichia, `a/L`**. `f = 1` sets it to 1 without saying so, and the `E0` sensitivity exists
only because of that hidden setting. This is a physical argument. §3.3 checks it numerically.

## 2. How well is that input established?

- **In S23 and S23-D: an unstated assumption, `a/L` = 1.** Neither file gives an extent for
  actinotrichia. S23-D treats the fin as a uniform beam stiffened end to end.
- **What the literature says, at stated read-levels.** This was found in this work through the
  Europe PMC full-text API.
  - Tanimoto, Miyamoto, Tamura, Kondo, Kuroda 2026, "A collagen orientation switch reshapes
    fin architecture", *iScience*, doi:10.1016/j.isci.2026.117464, PMC13573005. Read-level:
    **`full-text`**, by keyword extraction from the XML, not a linear read.
    - Authors' claim: "During the larval stage … AT are present throughout the fin. By
      contrast, in adults, fin rigidity is provided by fin bones, and AT are restricted to the
      growing tips of these bones."
    - Authors' observation: in adult wild-type fin tips, fibrous signal sits "in the terminal
      ∼200 μm region of each fin bone".
    - Actinotrichial diameter: "approximately 2–3 μm".
  - Hanzelova, Baird, Keshinro, Kadhom, Lalonde et al. 2026, "An essential role for
    actinotrichia in zebrafish fin patterning and courtship behavior", *Development*,
    doi:10.1242/dev.204990, PMC13120675. Read-level: **`full-text`**, keyword extraction.
    - Authors' claim: actinotrichia reach "up to 100 μm in larval zebrafish FFs … increasing
      in length during development to 200-300 μm at the tips of adult zebrafish caudal rays".
    - They cite Nakagawa et al. 2022 for this. I read Nakagawa et al. 2022 (*Dev Biol*,
      doi:10.1016/j.ydbio.2021.09.003) only at **`abstract`** level, which gives no length.
      So the 200–300 µm figure is, for me, a **secondary citation**.
  - The two sources **agree**: about 200 µm, and 200–300 µm. I keep the range **a = 200–300
    µm** and do not collapse it.
- **Evidence level of the improved input: `measured` (adult zebrafish, caudal fin), read at
  `full-text` for ~200 µm and as a secondary citation for 200–300 µm.** It is a direct
  observation in the target species. It is not a proxy. The caveats:
  - It is the caudal fin, not the pectoral fin S6 needs. I found no pectoral-fin actinotrichial
    length, so that value is `unknown`.
  - It is wild-type, not a gain-of-function line.

## 3. Improving it

### 3.1 The quantity S23-D actually needed

The quantity that matters is not `E0`. It is how much of the fin's tip compliance lies in the
segment that actinotrichia occupy. In adults, that segment is the distal ~0.2–0.3 mm of rays
that are centimetres long.

### 3.2 Does any gain-of-function move `a`? (a correction to S23's negative)

König, Page, Chassot, Jaźwińska 2018, "Dynamics of actinotrichia regeneration in the adult
zebrafish fin", *Dev Biol*, doi:10.1016/j.ydbio.2017.07.024. Read-level: **`abstract`**.
- Authors' claim: in a **gain-of-function `kcnk5b`** long-fin mutant, "the long-fin phenotype
  is associated with an extended size of actinotrichia during homeostasis and regeneration".

S23 §2.3 reported **no** gain-of-function experiment that raises actinotrichial *number or
stiffness*. That negative still holds, because this is *size*. It is still a demonstrated
gain-of-function that changes actinotrichia, and S23's search missed it. The size of the
extension is `unknown` to me (abstract only). Whether actinotrichia stay restricted to ray
tips in that mutant is also `unknown`. The calculation in §3.3 asks how big an extension would
have to be.

### 3.3 Recompute with `a/L` measured (computed)

Model: a uniform-load cantilever, as in S23/S23-D, with `EI(s)` and `s` measured from the tip.
The segment `s < a` contributes a share `φ = (a/L)⁴` of the tip deflection (uniform `EI`). Take
the most favourable case for gain-of-function: the actinotrichial segment is made **infinitely
rigid**, with `C = ∞`, so `E0`, `E_target` and `f` all drop out. The deflection then falls by at
most a factor of `1/(1−φ)`. S6 needs a factor of `S`.

| case | `S` | `a` | `a/L` | `φ` | best reduction | margin left |
|---|---|---|---|---|---|---|
| lenient (2 cm, 50 %, 5×10⁻⁹) | 39.2 | 200 µm | 0.010 | 1.0×10⁻⁸ | ×1.00000001 | **39.2** |
| lenient | 39.2 | 300 µm | 0.015 | 5.1×10⁻⁸ | ×1.00000005 | **39.2** |
| lenient | 39.2 | 3 mm (10× measured) | 0.15 | 5.1×10⁻⁴ | ×1.0005 | 39.2 |
| central (4 cm, 10 %, 4×10⁻⁹) | 981 | 300 µm | 0.0075 | 3.2×10⁻⁹ | ×1.000000003 | **981** |

To flip at the lenient corner, rigid actinotrichia would have to cover `a/L ≥ 0.9936`, that is
`a ≥ 19.9 mm` of a 20 mm span. That is about 66–100× the measured length. With a tip point load
instead of a uniform load, `φ = (a/L)³` and the requirement is `a/L ≥ 0.991`, which gives the
same answer.

**Robustness to taper (computed).** A real ray tapers, so the tip is softer than the root and
contributes more of the compliance. If `EI(s) ∝ sⁿ`, then `φ = (a/L)^(4−n)`.
- At a = 300 µm, the lenient corner flips only when `n ≥ 3.994`.
- `n = 4` makes tip compliance diverge, which is unphysical.
- For n = 3, φ = 0.015. For n = 3.5, φ = 0.12.

I did not find a measured taper exponent for zebrafish rays, so it is `unknown`. Only a taper at
the edge of physical possibility rescues the hypothesis.

**What this does to the S23-D inequality.** In adults, `E0` stops mattering. The S23-D margin of
1.37, and its factor-2 flip on `E0`, apply only to a fin whose actinotrichia run the full span,
as in a **larval fin fold**. That is a different design from the one S6 sizes (a 4 cm, 0.4 g
adult). There, the S23-D `E0` analysis still governs, and `E0` is still unmeasured.

## 4. Verdict on the original conclusion

**STRENGTHENS.** Protein-level stiffening of actinotrichia cannot close the S6 gap in an adult
fin. This now holds:
- even if actinotrichia became infinitely stiff;
- for every value of `E0`, `E_target` and `f`;
- at both the central and the lenient design corners.

The reason is that actinotrichia occupy only the distal ~200–300 µm of the ray, where a
cantilever has almost no bending moment. That length is measured, read at `full-text` and as a
secondary citation. The margin at the lenient corner is **39×**, the full shortfall, up from
S23-D's 1.37×. This is a calculation on a measured length, not an observed stiffness.

S23-D's "the magnitude must be narrowed to ~1.4×" was correct within its framing. That framing
assumed `a/L = 1`, which is false for adults.

Two claims come out weaker:
1. S23's negative "no gain-of-function on actinotrichia" needs a scope note. The `kcnk5b`
   gain-of-function enlarges actinotrichia (König 2018, `abstract`). The size of the effect is
   `unknown`.
2. For a **neotenic, full-span fin-fold design**, the conclusion still rests on S23-D's
   unmeasured `E0`, with a margin of about 1.4× at the lenient corner.

## 5. What would settle the remaining unknowns, and what it would cost

My estimates, not sourced.

- **Actinotrichial extent in a `kcnk5b` gain-of-function fin, and in the pectoral fin.** Use
  whole-mount DAF or And1 staining of adult wild-type and `kcnk5b` pectoral and caudal fins, and
  measure `a` and ray length `L`.
  - Decision rule (computed): the adult conclusion falls only if `a/L > 0.99`.
  - Cost: days of confocal time on existing lines, under ~US$2×10³.
  - First, at no cost: read König 2018 in full for the reported actinotrichial size.
- **Ray taper exponent `n`.** Use µCT of hemiray cross-sections along the span.
  - Decision rule: the conclusion falls only if `n > 3.99`.
  - Cost: one µCT session.
- **`E0`.** Only for the fin-fold variant. Use the AFM bending or microtensile test of single
  hydrated actinotrichia described in S23-D §5, about US$10⁴. Also read Rajaram et al. 1981 in
  full.

## 6. Searches and their scope

- **Europe PMC REST**, query `elastoidin OR ceratotrichia OR actinotrichia`, 397 hits, first 100
  titles read at `listing`. I then pulled full-text XML for PMC13573005, PMC13120675,
  PMC13543312, PMC11409509 and PMC10119692 and searched each for modulus, Pa/MPa/GPa,
  stiffness, diameter and length.
  - **None of the five reports a Young's modulus for actinotrichia or ceratotrichia.**
    PMC13543312 (chimaera ceratotrichia robotics) uses Ecoflex at 0.125 MPa as a model
    material, not a measured value.
  - Scope: those five papers only.
- **Crossref**, `query.bibliographic=elastoidin`, 26 records at `listing`. This confirmed:
  - the title of Rajaram, Sanjeevi, Ramanathan 1981, "The tensile properties and mode of
    fracture of elastoidin", *J. Biosci.* 3:303–309, doi:10.1007/BF02702941. S23-D could not
    confirm the title.
  - Arumugam & Sanjeevi 1987, doi:10.1007/BF01086458.
  - Crossref holds no abstract for either.
- **Rajaram 1981 full text: `could-not-access`.**
  - www.ias.ac.in: DNS not resolvable, and the egress proxy refused it.
  - link.springer.com: proxy 403.
  - OpenAlex and Semantic Scholar: proxy refused.
  - academia.edu copy of the 1987 paper: not resolvable.
  - A web search (extended) returned only the qualitative conclusions S23-D already had: wet
    elastoidin is weaker than tendon but stiffer. **The wet elastoidin modulus is still
    `unknown`.**
  - To read it, these hosts need to be allowed in the session's network settings.

## Sources

| source | read-level | used for |
|---|---|---|
| S23-protein.md @ 6d1b84ed | full-text | parent conclusion |
| S23-deepen.md @ efff2517 + calc | full-text | S23-D inequality, margins |
| Tanimoto et al. 2026, *iScience*, PMC13573005 | full-text (keyword extraction) | adult AT restricted to terminal ~200 µm; diameter 2–3 µm |
| Hanzelova et al. 2026, *Development*, PMC13120675 | full-text (keyword extraction) | adult AT 200–300 µm (citing Nakagawa 2022) |
| Nakagawa, Kuroda, Aramaki, Kondo 2022, *Dev Biol* 481 | abstract | original source of 200–300 µm (not verified by me) |
| König et al. 2018, *Dev Biol* | abstract | `kcnk5b` gain-of-function enlarges actinotrichia |
| Rajaram, Sanjeevi, Ramanathan 1981, *J. Biosci.* 3:303 | listing (Crossref) + search-summary; full text could-not-access | elastoidin "stiffer than tendon", no number |
| Puri et al. 2018, *J Exp Biol*, PMC5868929 | not re-read; full-text per S23-D | `EI_meas` |

```swarm-result
{"subproblem": "S23-D-D", "evidence": "derived",
  "answer": "S23-D's conclusion was most sensitive to E0 only because f=1 silently assumed actinotrichia span the whole fin; in adult zebrafish they occupy only the distal ~200-300 um of each ray, which carries <1e-7 of a uniform-load cantilever's tip compliance, so even infinitely stiff actinotrichia cannot reduce deflection by the required 39-981x and the conclusion holds independent of E0 (it flips only if a/L > 0.99 or ray taper exponent n > 3.99), while a full-span larval-fin-fold design remains governed by S23-D's unmeasured E0.",
  "key_number": "actinotrichial span a = 200-300 um at adult caudal ray tips (a/L = 0.010-0.015 at L = 2 cm); computed tip-compliance share phi = (a/L)^4 = 1e-8 to 5e-8; flip requires a >= 19.9 mm of a 20 mm span",
  "verdict": "strengthens",
  "depends_on": [
    "S23: EI_req = (W/2) L^2 / (8 tol) uniform-load cantilever model, m = 0.4 g",
    "S23: design ranges L = 2-4 cm semi-span, tip-deflection tolerance 5-50%",
    "Puri et al. 2018 measured adult caudal fin EI = 1.5-4e-9 (abstract) / 2-5e-9 (conclusions) N m^2",
    "S23-D: shortfall S = 39.2 (lenient) to 981 (central)",
    "Tanimoto et al. 2026 (PMC13573005): adult actinotrichia restricted to terminal ~200 um of each fin bone",
    "Hanzelova et al. 2026 (PMC13120675) citing Nakagawa et al. 2022: adult caudal actinotrichia 200-300 um long",
    "assumption: caudal-fin actinotrichial extent transfers to pectoral fin (pectoral value unknown)",
    "assumption: ray taper exponent n < 3.99 (unmeasured)",
    "assumption: gain-of-function does not extend actinotrichia to a/L > 0.99 (kcnk5b GoF enlarges them by an unknown amount, Konig et al. 2018 abstract)",
    "S23-D: E0 >= 0.35 GPa conditional lower bound (governs only the full-span larval-fin-fold variant)",
    "S23/S23-D: E_target 5-10 GPa (governs only the full-span variant)"
  ]}
```
