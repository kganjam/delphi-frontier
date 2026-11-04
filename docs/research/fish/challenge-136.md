# Challenge 136: adversarial review of S6-D-D (passive-ray verdict, size-normalised)

Date: 2026-11-04. **We ran no experiment and measured nothing.** Every number below is either *quoted*, with
the source's read-level stated, or *calculated* by us in [`challenge-136_calc.py`](challenge-136_calc.py). To
rerun it: `python3 docs/research/fish/challenge-136_calc.py`.

**The claim under review** (harvest `deepen-s6-d-sensitive-input-t6ch0y`; file `docs/research/fish/S6-D-deepen.md`
on branch `claude/deepen-s6-d-sensitive-input-t6ch0y`, read in full): S6-D's passive-ray verdict "stands in
direction". After isometric size transfer the passive bluegill ray is about 4.3× short (0.8–8×) instead of
166× short, and the 12× hemitrich locking measured by Alben would close the gap.

**Outcome: WEAKENED.** The arithmetic is correct. The *direction* of the verdict, however, rests on an
unsupported mapping: the author treats Alben's bench condition "one hemitrich free" as the natural passive ray.
The recorded evidence level, "measured", is also wrong.

---

## 1. The arithmetic, redone independently

We started from the stated inputs and did not reuse the author's code.

- **Per-ray load** (calculated): P = mg/(2N) = 0.1 × 9.81 / 28 = 0.03504 N.
- **Required stiffness** (calculated): EI_req = P·L²/(8 × 0.10) = **6.31×10⁻⁴ N·m²**. The size-normalised
  requirement is EI_req/L⁴ = **3.04 Pa**.
- **Back-calculated ray stiffness** (calculated): we took a uniform cantilever with the load at a = 2L/3,
  deflection read at the tip, k = 1.98 N/m and L = 40.3 mm.
  - Both bases clamped: EI = **2.24×10⁻⁵ N·m²**.
  - Divided by 12 (one base free): EI = **1.87×10⁻⁶ N·m²**. That gives EI/L⁴ = 0.708 Pa and **R_iso = 4.30**.
- **Alben's three-point E·I range**, 1×10⁻⁶ to 1×10⁻⁵ N·m² (calculated): EI/L⁴ = 0.38–3.79 Pa, so
  **R_iso = 8.0 to 0.80**.

All of the claim's numbers reproduce. **We found no arithmetic error.**

## 2. The hidden assumption that carries the direction: what "passive" means

We re-read the Alben, Madden & Lauder 2007 full text (PMC2359861, read-level **full-text**, fetched this
session).

- **The test.** In §2 the experiment compares "one hemitrich base is fixed and the second is free to slide"
  against both bases clamped. The Fig. 7 caption reads: "a slope of 1.98 N m⁻¹, about 12 times the value when
  one hemitrich is free".
- **What the paper does not say.** It does not say which clamp condition matches the intact ray in a fish. It
  treats the base offset as something set "directly using clamps or indirectly by muscle action" (§3.1.1).
- **What the author assumed (the author's mapping, not Alben's):**
  - "one hemitrich free" = passive ray;
  - "both clamped" = active "locking".
- **Why that mapping is doubtful (our inference).** In an intact fin, neither hemitrich base is free to slide.
  Both are tied into ligaments and the abductor and adductor musculature. A relaxed fish therefore sits
  somewhere between "free" and "clamped". It is not at "free".
  - "One base free" is a dissection condition. It is the *lower* bound on in-situ passive stiffness, not the
    central estimate.
  - "Both clamped" is not "active locking" either. It is a rigid base constraint. Alben measured no muscle
    force there.

**The result with the assumption relaxed** (calculated, isometric transfer, tip deflection, L_test = 40.3 mm):

| Base condition taken as the natural passive ray | R_iso | Passive ray |
|---|---|---|
| One hemitrich free (the author's choice) | 4.30 | fails |
| Intact ray in three-point bending (Alben E·I, geometric mean 3.2×10⁻⁶) | 2.54 | fails |
| Intact ray in three-point bending, upper end 1×10⁻⁵ | 0.80 | passes |
| Both bases clamped | 0.36 | passes |

**The sign of R − 1 depends on an unmeasured property:** how stiffly the in-situ base resists hemitrich sliding
when the muscles are relaxed. The claim's "stands in direction" holds only at its chosen end of the bracket.

It follows that "the measured 12× hemitrich locking" is not a measured *active-stiffening* capacity. It is a
ratio between two clamp conditions on dissected rays. Calling it a mechanism the fish can deploy goes beyond
the source.

## 3. Two further input ambiguities

Both are calculated, and neither flips the result on its own.

**Where deflection was read.** Alben is internally inconsistent here. §5.2 says "tip deflection". §5.1 has the
probe holding "vertical deflection to zero at this point", meaning the load point. If deflection was read at
the load point, then EI = k·a³/3:
- passive (one base free): EI = 1.07×10⁻⁶ N·m² and **R_iso = 7.5**;
- clamped: R_iso = 0.63.

The claim's 1.9×10⁻⁶ assumes tip deflection without noting the conflict. The tip reading is the reading that
favours the conclusion falling, so this ambiguity widens the passive range upward, to 4.3–7.5.

**Tested ray length.** The claim calls L_test = 40.3 mm an "upper bound" on EI. That is true for EI. For the
quantity that matters, EI/L⁴, a shorter tested ray *raises* the index, because the index scales roughly as k/L.
- At 30 mm: passive R_iso = 3.2 (tip reading) or 5.6 (load-point reading);
- at 30 mm, clamped: R_iso = 0.27.

So 40.3 mm is the length most *favourable* to the claim's "fails" direction. This is not a fault in the
claim's range, but the claim's wording obscures it.

## 4. Proxy check

- **Quantity that matters:** the in-vivo flexural stiffness of a roughly 120 mm exocoetid pectoral ray under
  glide load.
- **Proxy used:** a dissected roughly 40 mm bluegill ray in one bench boundary condition, scaled by an assumed
  L⁴ law.

The claim states the isometry assumption and the taxon transfer openly. Its §5 declines to claim them. What it
does *not* flag as an assumption is the boundary-condition proxy described in §2. Earlier passes treated that
proxy as a measured "passive" value, and it is the one that decides the sign.

## 5. Evidence level

- **Recorded level:** "measured".
- **The claim's own swarm-result** says "derived: calculation on … transferred … under an unmeasured
  isometric-scaling assumption".

The key number, EI/L⁴ ≈ 0.7 Pa against 3.0 Pa, is a calculation from measured inputs. The "passive EI 1.9×10⁻⁶"
is a back-calculation that also contains a ÷12 and a choice of beam geometry. **"Measured" is a defect.** The
correct level is *derived*. This defect is in the harvest record, not in the author's prose, which tags the
numbers correctly.

## 6. Counter-examples and missed regimes (negative search, scoped)

- **Exocoetid ray mechanics.** We did not repeat the author's Europe PMC search, which found no Exocoetidae
  ray mechanics or ray-EI allometry. We have no counter-example to add. Scope of our own searching this
  session: only the Alben full text was fetched. No new literature search was run.
- **Flammang 2013.** The 565×10⁻⁶ N·m² abstract value remains unresolved. We did not access its Methods.
- **One missed regime that we can name without new data.** The membrane and inter-ray coupling were not
  modelled. Adjacent rays and the fin web share load, so the equal-share independent-cantilever requirement is
  itself an assumption. The claim inherits it from S6-D and lists it.

## 7. Verdict

**WEAKENED.**

- **What survives:**
  - the arithmetic;
  - the main correction, which is that the 166× figure was an artifact of the unscaled cross-length comparison
    and the shortfall is at most a few-fold;
  - the two stated falsifiers (the Flammang value and the scaling exponent).
- **What does not survive:**
  - "stands in direction". Once the passive ray is bracketed between Alben's one-free and clamped base
    conditions, with the intact three-point E·I in between, R_iso runs from **0.27 to 7.5**. The sign is
    unresolved. The author's "fails" depends on the unsupported choice of "one hemitrich free" as the natural
    passive state.
  - the description of the 12× ratio as a "measured locking" mechanism;
  - the recorded evidence level, "measured". It is derived.

**Corrected statement:** the size-normalised passive-ray shortfall is R_iso ≈ 0.3–7.5 (calculated, isometric
assumption). That is O(1), and its sign depends on the unmeasured in-situ hemitrich base compliance. The
passive-ray verdict is **undetermined**, not "stands".

## Sources

| Source | Read-level |
|---|---|
| S6-D-deepen.md and s6_d_deepen_calc.py, branch `claude/deepen-s6-d-sensitive-input-t6ch0y` | full-text (repository) |
| Alben S, Madden PGA, Lauder GV 2007, *J R Soc Interface* 4:243–256, PMC2359861 | full-text (pmc.ncbi.nlm.nih.gov, fetched this session through a summarising fetch tool; quotes as returned) |
| Flammang et al. 2013, *J Morphol* 274:1044 | not accessed this session. The author reports abstract-level reading only |

```swarm-challenge
{"claim_id": 136, "outcome": "weakened", "reason": "Arithmetic reproduces, but 'stands in direction' rests on the author's unsupported mapping of Alben 2007's dissected 'one hemitrich free' bench condition to the natural passive ray (Alben equates neither clamp condition with the in-situ base); bracketing the in-situ base between one-free and clamped, with the intact three-point E*I between, gives R_iso 0.27-7.5, so the sign is undetermined, and the recorded evidence level 'measured' should be 'derived'.",
  "corrected_value": "size-normalised passive-ray shortfall R_iso ~0.3-7.5 (calculated; isometric assumption; sign undetermined), i.e. EI/L^4 ~0.4-11 Pa vs 3.04 Pa required",
  "depends_on": [
    "S6-D scenario assumptions m=0.10 kg, N=14, L=0.12 m, n=1, delta/L<=0.10, uniform-load equal-share cantilever",
    "Alben et al. 2007 full-text: clamped-base point-force slope 1.98 N/m at ~2/3 ray length, ~12x the one-hemitrich-free value",
    "Alben et al. 2007 full-text: no statement equating either clamp condition with the in-situ ray base; base offset set by clamps or muscle action",
    "Alben et al. 2007 full-text: deflection read at tip (s5.2) vs held zero at load point (s5.1), internally inconsistent",
    "Alben et al. 2007 full-text: three-point composite E ~1e8-1e9 Pa, I ~1e-6 cm^4; maximum ray length 40.3 +/- 0.8 mm; tested ray lengths not reported",
    "our inference: in-situ relaxed hemitrich base coupling lies between 'one free' and 'both clamped' (unmeasured)",
    "isometric EI ~ L^4 transfer bluegill -> exocoetid (assumption, inherited from the claim)"
  ]}
```
