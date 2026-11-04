# S26-D: Deepening S26, "Can active stiffening carry the load a passive ray cannot?"

**Status:** deepening pass. Calculation and literature work only. **Nothing here was measured by me.** Each
number is tagged *measured* (by the cited authors), *calculated* (by me, in
[`S26_deepen_calc.py`](S26_deepen_calc.py), run with `python3 -I`) or *assumption*.

## 0. What I was handed, and what I found upstream

The brief's "recorded answer" field arrived **empty**. I found the S26 document on another branch,
`origin/claude/active-fin-ray-stiffening-l53vks:docs/research/fish/S26-organ.md` (commit `6c78e686`), and read
it in full. Its answer:

> **No** on the measured evidence. The one measured hemitrich base-locking factor is ~12x (one bluegill ray,
> Alben et al. 2007). The brief's passive gap is 165x, from EI_req = 6.3e-4 N m^2 and an inferred
> EI_passive = 3.8e-6 N m^2. So a ray stays ~14x short. Even the modelled ~100x ceiling is 1.65x short.

S26 reported that it **could not find S6**. I found it, which S26 did not have:
`origin/claude/deepen-fin-ray-s6-cj2i2x:docs/research/fish/S6-deepen.md` (read in full), plus two challenges
and a replication of it (`challenge-72.md`, `challenge-74.md`, `replicate-72.md` on their own branches, read in
full). These settle two of S26's open premises:

1. **EI_req = 6.3e-4 N m^2 is per ray, for a 100 g fish with 12 cm rays and 14 rays per fin.** It is
   calculated by S6-D from four assumptions (m = 0.10 kg, N = 14, L = 0.12 m, n = 1), with failure set at
   δ/L > 0.10. It is not a zebrafish number. S26 §1 called the target "a zebrafish-sized ray". That is my
   reading of S26, and it does not match the upstream requirement.
2. **The load has already been divided across rays.** So S26's escape route C6 ("if the requirement is
   whole-fin, N ≥ 13.8 rays sharing closes it") **double-counts the 14 rays.** That escape route is closed.
3. **165x = 6.3e-4 / 3.8e-6.** The 3.8e-6 N m^2 is Puri et al. 2018 relaying Flammang et al. 2013 for a
   **bluegill** ray. S26 inferred it by division and did not know its source.

## 1. The input the answer is most sensitive to, shown by recomputing

The conclusion has one inequality: `F_a × EI_passive ≥ EI_req`. Here F_a is the active stiffening factor.
I perturbed each input by 2x (calculated, `S26_deepen_calc.py` §1):

| Perturbation | Measured path (F_a = 12): margin | Model-ceiling path (F_a = 100): margin |
|---|---|---|
| baseline | 0.072, fail | 0.60, fail |
| EI_req ×2 / ÷2 | 0.036 / 0.145, fail | 0.30, fail / **1.21, pass** |
| EI_passive ×2 / ÷2 | 0.145 / 0.036, fail | **1.21, pass** / 0.30, fail |
| F_a ×2 / ÷2 | 0.145 / 0.036, fail | **1.21, pass** / 0.30, fail |

(Margin > 1 means the actively stiffened ray meets the requirement. The S26 document rounded the
ceiling-path shortfall to 1.65x. I get 1/0.60 = 1.66x.)

Reading this honestly:

- **The measured-path "no" survives a factor-of-two error in any single input.** Its margin is 13.8x. The
  three inputs enter symmetrically, so a 2x test alone cannot rank them.
- **The ceiling-path "no" flips** on a 2x error in any of the three inputs.
- What ranks them is **how far each could actually be wrong**:
  - **F_a = 12x** (measured). The model bounds it above by ~100x (Alben 2007). It cannot plausibly be 14x
    higher.
  - **EI_req** (calculated from assumptions). The replication's 32-corner range is 1.1e-4 to 3.1e-3 N m^2,
    which is ±~5x. The load-distribution error bar is ×0.53 to ×1.47 (challenge-72).
  - **EI_passive.** Published candidates for the same species span **1e-6 to 5.65e-4 N m^2, a 565x range**
    (§2). At the top of that range the gap is 1.1x and 12x closes it with ~11x to spare (calculated).
    **The single most sensitive input is EI_passive**, the baseline the active factor multiplies.

## 2. How well is EI_passive established?

| Source | Value | What it is | Read-level |
|---|---|---|---|
| Puri et al. 2018, *J Exp Biol* 221:jeb171777, PMC5868929 | 3.8e-6 N m^2, "bending stiffness of bluegill rays" | a **relay** in the Conclusions, citing Flammang et al. 2013. Used to scale to zebrafish. The same paragraph says Flammang's measurements "reached a sensitivity of 10^-6 N m^2" | **full-text** (Europe PMC XML, read directly by me) |
| Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044, doi:10.1002/jmor.20161 | **565 × 10^-6 N m^2** | "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2", in the context of an in-vivo vortex-jet perturbation | **abstract** (Europe PMC REST, read directly). Full text **could-not-access**: sites.harvard.edu fails DNS in this session |
| Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, PMC2359861 | B = EI ≈ 1e-6 to 1e-5 "J m" (= N m^2) | from three-point bending: a composite E ≈ 1e8–1e9 Pa and I ≈ 1e-6 cm^4. **The base condition (clamped or free) is not stated** | **full-text, via an automated page summarizer** (Europe PMC fullTextXML returned HTTP 500) |
| Alben et al. 2007, same paper | 1.98 N m^-1 point-load stiffness, both bases clamped, "about 12 times the value when one hemitrich is free"; load at 2/3 of ray length | measured. The figure caption gives no n and no spread. The paper tested 24 rays in total but does not tie that count to this comparison. **Effectively n = 1 as reported** | full-text, via summarizer |

**Is it measured, a proxy, or a repeated assumption?** All three.

- **Proxy.** It is a **bluegill** ray, ≤ ~40 mm long (Alben's fish had a maximum pectoral ray length of
  40.3 ± 0.8 mm, measured). It is being compared against a requirement for a **120 mm** ray. EI is extensive:
  it scales with E·d^4 and, under isometry, with L^4. Challenge-74 raised this defect against the labrid
  comparison in S6-D. **It applies equally to S26's 165x**, and S26 did not apply it.
- **Repeated.** In S26, 3.8e-6 was a quotient of two numbers from the brief. Its origin is a one-sentence relay
  in another paper's Conclusions. The primary paper's only number I could read (565e-6) disagrees with it by
  ~150x.
- **Partly measured.** Alben 2007 is the same lab, the same species and an independent primary measurement.
  It puts bluegill ray EI at 1e-6 to 1e-5. My own back-calculation (below) also lands in that range.

**Improvement 1: a primary cross-check on the magnitude (calculated).** I treated Alben's measured
1.98 N m^-1 as a uniform cantilever with a point load at a = (2/3)L, so k = 3EI/a^3. I assumed the tested ray
has the group maximum length, 40.3 mm (*assumption*: the tested ray, "ray 4 of 13", may be shorter).

- EI_clamped = **1.28e-5 N m^2**
- EI_one-free = 1.28e-5 / 12 = **1.07e-6 N m^2**
- If the ray is 30 mm: EI_clamped = 5.3e-6. If 20 mm: 1.6e-6.

Both states sit inside Alben's stated 1e-6 to 1e-5. The relayed 3.8e-6 sits between them. **My inference,
not any author's claim:** the 3.8e-6 relay is consistent in magnitude with the primary excised-ray
measurements of the same lab. The 565e-6 abstract value is the outlier against excised rays, by 44x to 530x.
Possible reasons include an in-vivo state, a different ray region, or a different quantity in the inversion.
This **does not resolve** disagreement D1 from S26 / S6-D. I could not read Flammang's methods. **I preserve
it: 565e-6 vs 3.8e-6, unresolved.**

**Improvement 2: the real quantity.** The quantity S26 needs is the **passive EI of a ray of the length the
requirement is written for (120 mm)**. Nobody has measured it:

- No exocoetid ray EI. S6-D searched Europe PMC (35 hits, none relevant). Challenge-72 ran one web search.
- No zebrafish ray EI. My two standard web searches (Flammang 3.8e-6 provenance, and hemitrich
  locked-vs-sliding in trout/zebrafish/carp) found no zebrafish or cyprinid single-ray EI and no second
  locked-vs-sliding ratio in any species.
- Das et al. 2024, *Interface Focus* 14:20230072, PMC11285607 (full-text via summarizer) reports **no
  bonded-vs-sliding ratio for natural rays**. It gives a ~100 µm natural ray diameter (trout) and a 40%
  ligament effect in synthetic rays.
- Scope of these negatives: those two web searches, the one paper fetch, and the upstream searches cited.
  Google Scholar, Web of Science and ZFIN were not searched.

So the best available step is a **size correction**. It is an assumption, and I report it as one.

## 3. Recompute with the size-corrected input (all calculated)

Under isometric scaling of a bluegill-proportioned ray from L_src to 120 mm (`S26_deepen_calc.py` §3):

| L_src (bluegill ray tested) | EI scale ×(120/L_src)^4 | passive EI at 120 mm | active factor needed | margin of measured 12x |
|---|---|---|---|---|
| 40.3 mm (group max, Alben) | 78.6 | 3.0e-4 N m^2 | **2.1x** | **5.7x** |
| 30 mm | 256 | 9.7e-4 | 0.65x (passive already passes) | 18.5x |
| 20 mm | 1296 | 4.9e-3 | 0.13x | 94x |

The measured 12x closes the gap whenever the bluegill source ray was shorter than **62 mm**. Alben's bluegill
had no pectoral ray longer than ~41 mm. Flammang's specimen sizes are `unknown`.

Robustness at L_src = 40.3 mm (§4 of the script):

- The 12x passes at the S6-D nominal requirement, with a tip-heavy load (×1.47), at the replication's lower
  corner, and at its upper corner (3.1e-3 N m^2, needs 10.4x).
- **Halving the locking factor to 6x** still passes everywhere except the upper corner.
- At the Alben low end, EI_passive = 1e-6, the factor needed is 8x, which 12x still covers.

**Two other routes, recomputed:**

- **The size-uncorrected comparison, kept as S26 framed it.** A fully locked bluegill ray (1.28e-5,
  calculated from Alben's measurement) is **49x short**. This is worse than S26's 14x. Both are statements
  about a 40 mm ray against a 120 mm requirement.
- **C6 (load sharing).** This route is removed: the requirement is already per ray (§0).

## 4. Verdict: FALLS

S26's "no" rested on the 165x gap. That gap compares the **passive EI of a ≤40 mm bluegill ray** with the
**required EI of a 120 mm ray**. It is a size mismatch, not a property of passive rays.

- Under isometric scaling (an assumption), a passive bluegill-proportioned 12 cm ray is only **~2x short**.
  The single measured locking factor of ~12x (n = 1) carries the load with a **~5.7x margin**.
- So the answer moves from "no" to **"yes, conditionally".** It holds if:
  - a flying-fish-scale ray keeps bluegill cross-section proportions (outer diameter ~3–6 mm, from Puri's
    1–2 mm bluegill diameter ×3; *assumption*);
  - the 12x excised-ray clamping factor is reachable by muscle in vivo, and sustainable through a glide
    (*unmeasured*).
- Without the size correction, the comparison does not bear on the question, so it can support neither yes
  nor no.

**What this does NOT establish:**

- That flying-fish rays are isometric with bluegill rays. Allometry could go either way, and flying-fish
  pectoral rays are known to be long relative to the body.
- That muscles can hold full clamping. The ~10–15 mN holding force per 100 µm offset (M7 in S26) is
  search-summary level.
- Anything for an actual zebrafish. The upstream requirement is for a 100 g fish. A zebrafish-scale
  requirement was not derived by S6-D or here.
- Anything about the Flammang D1 disagreement beyond the magnitude cross-check above.

**What would settle it, and what it would cost** (cost estimates are my own, not sourced):

1. **Flammang 2013 full text** (methods: ray region, length, how 565e-6 was derived). Cost: library access
   only. It is blocked here by network policy (sites.harvard.edu needs to be allowed in this session's
   network settings).
2. **Three-point and cantilever bending on excised exocoetid pectoral rays**, with bases free, one free and
   both clamped. Add micro-CT for d, t and I. This measures EI_passive at the right size and a second
   locking factor directly, and removes both the isometry assumption and n = 1. Cost: a few person-weeks
   in a lab with a micro-mechanical tester. Specimens are a commercial fishery by-product. No quote obtained.
3. **Report n and spread for the 12x** across Alben's 24 rays, from the authors' data. Cost: one email.

```swarm-result
{"subproblem": "S26-D", "evidence": "derived: calculation on a cross-taxon proxy (bluegill ray EI, relayed full-text and primary full-text-via-summarizer), size-corrected under an isometric-scaling assumption; no exocoetid or zebrafish ray EI measured", "answer": "S26's 'no' falls: its 165x gap compares a <=40 mm bluegill ray's passive EI (3.8e-6 N m^2) with a per-ray requirement for a 120 mm ray (6.3e-4 N m^2), and under isometric L^4 scaling the passive gap shrinks to ~2.1x, which the single measured ~12x hemitrich-locking factor closes with ~5.7x margin (calculated), so active stiffening can carry the load conditional on isometry and on muscles achieving the excised-ray clamping factor in vivo.", "key_number": "passive EI of a bluegill-proportioned ray scaled to 120 mm: ~3.0e-4 N m^2 (calculated from 3.8e-6 N m^2 x (120/40.3)^4 = x78.6), giving a required active factor of ~2.1x, not 165x", "verdict": "falls", "depends_on": ["S26 answer: docs/research/fish/S26-organ.md on origin/claude/active-fin-ray-stiffening-l53vks (12x vs 165x, no)", "S6-D required EI 6.3e-4 N m^2 per ray, calculated from assumed m=0.10 kg, N=14 rays/fin, L=0.12 m, n=1, delta/L<=0.10 (docs/research/fish/S6-deepen.md on origin/claude/deepen-fin-ray-s6-cj2i2x)", "replicate-72 EI_req corner range 1.1e-4 to 3.1e-3 N m^2 (assumption-driven)", "challenge-72 load-distribution factor x0.53 to x1.47 on EI_req", "Puri et al. 2018 J Exp Biol jeb171777 relay: bluegill ray EI 3.8e-6 N m^2 citing Flammang 2013 (full-text)", "Flammang et al. 2013 J Morphol abstract: 565e-6 N m^2 calculated (disagrees ~150x with the relay; unresolved)", "Alben, Madden & Lauder 2007 J R Soc Interface: clamped stiffness 1.98 N/m, ~12x vs one-base-free, effectively n=1 (full-text via summarizer)", "Alben et al. 2007: bluegill ray B=EI ~1e-6 to 1e-5 N m^2 from three-point bending, base condition unstated", "Alben et al. 2007: bluegill max pectoral ray length 40.3 +/- 0.8 mm (6 fish)", "Alben et al. 2007 model: clamped/free ratio asymptote ~100 for G>1e5", "assumption: tested bluegill ray length = 40.3 mm (group max) for the 1.98 N/m back-calculation", "assumption: uniform Euler-Bernoulli cantilever, point load at 2/3 L, for back-calculating EI", "assumption: isometric scaling EI ~ L^4 from bluegill ray to 120 mm ray at constant modulus and proportions", "assumption: excised-ray clamping factor is achievable and sustainable by fin muscles in vivo", "Puri et al. 2018: bluegill ray diameter 1-2 mm (full-text)"]}
```
