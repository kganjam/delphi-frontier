# Challenge 201: adversarial review of S7 (pectoral girdle)

Date: 2026-11-04. Reviewer did not write the claim.

**Claim under review** (S7, `docs/research/fish/S7-organ.md`, branch `claude/s7-organ-pectoral-girdle-xlxpkt`,
commit `a61c9688`, read in full from the repo): *"The computed root bending moment at design lift
(2e-5 to 1.1e-4 N·m per fin for a 0.4 g fish) needs only a ~0.12–0.35 mm solid-equivalent bone section, so
girdle bone strength is probably not limiting; the unresolved constraint is the mobile fin–scapulocoracoid
joint, which must hold a 9–55× body-weight reaction via muscle or a lock … KEY: 1.1e-4 N·m (V=3 m/s, n=3,
C_L=0.78)."* Recorded evidence level: derived.

**Verdict: WEAKENED (minor).** The headline moment and the bone-section range reproduce. Two things fail:
the joint-reaction range is wrong at its lower end when set against the claim's own moment range, and
"bone probably not limiting" is drawn against a comparator that nobody has measured. Every number in this
file is **calculated** (script below) unless a source is named. No experiment was run.

## 1. Independent arithmetic

I wrote a separate script (`c201.py`, scratchpad; its logic is reproduced here). It takes only the stated
inputs: m = 0.4 g, ρ = 1.2 kg m⁻³, C_L = 0.78, AR = 9, body half-width 2.5 mm, V ∈ {3, 5} m/s, n ∈ {1, 3},
σ_y ∈ {25, 114} MPa, and r ∈ {0.5, 1.0} mm at 200 kPa muscle stress.

| Quantity | Author | Recomputed (calculated) |
|---|---|---|
| W | 3.92 mN | 3.924 mN |
| S, b, s at V=3 | 9.32 cm², 9.16 cm, 4.33 cm | 9.32 cm², 9.16 cm, 4.33 cm |
| M, V=3, n=3 | 1.08e-4 N·m | 1.081e-4 N·m |
| M, V=5, n=1 (low end) | 2.08e-5 N·m | 2.079e-5 N·m |
| d range (solid rod, Z = M/σ_y) | 0.12–0.35 mm | 0.123–0.353 mm |
| Joint reaction, cases tabulated by author | 9–55 W | 9.2–55.1 W |
| **Joint reaction, full bracket the claim uses for M** | 9–55 W | **5.3–55.1 W** |
| Isometric stress ratio vs 61 g flying fish | 0.19 | 0.187 |

**Defect 1 (internal inconsistency).** The claim's moment range, 2e-5 to 1.1e-4 N·m, includes the case
V = 5 m/s, n = 1. The author's muscle table (§3e) leaves out that case. With r = 1 mm it gives
F = 20.8 mN = **5.3 W** (calculated). So the stated "9–55×" does not cover the bracket stated in the same
sentence. The correct range on the author's own inputs is **~5–55× body weight**. This does not change the
qualitative conclusion, but the number as written is wrong.

**Load-distribution check (author's error is conservative).** The author applied the elliptic centroid
factor 4/(3π) to the fin length alone, but assigned W/2 to each fin while the span includes the body. I
redid it with elliptic lift over the full span b and integrated the moment about the fin root
(y = 2.5 mm). The fin then carries 0.93 (V=3) or 0.88 (V=5) of W/2. The V=3, n=3 moment becomes
**1.00e-4 N·m** instead of 1.08e-4 (calculated, −7%). At V=5 it is −12%. The author's figure overstates
the moment, so it is the safe direction. This is not a fault.

## 2. Proxy check

The quantity that matters is the **stress in the actual element that receives the root moment**, at its
real section modulus. The claim stands in for that with the **diameter of a hypothetical solid circular
rod**, and the claim's own text admits the real section is unknown.

- Because d ∝ M^(1/3), the required number barely moves. The comparator is the problem: bone stress scales
  with (actual size)⁻³. So "only 0.12–0.35 mm" does not support "probably not limiting" until the real
  section is known. The word "so" in the claim turns a requirement into a verdict. *My inference.*
- The follow-up S7-D (branch `claude/deepen-s7-pectoral-girdle-b6j2hx`, read in full from the repo) reports
  that fin rays articulate through four proximal radials with the scapula, citing Keer et al. 2019
  (PMC6800157). **I did not read Keer 2019. This is relayed from S7-D, which itself says it read it through
  a summarising fetch.** If that is right, the first element to take the moment is smaller than the
  cleithrum the author was thinking of. That would make the proxy less generous, not more.

## 3. Hidden assumptions, relaxed (all calculated)

| Assumption | Relaxed to | M (N·m) | d at 25 / 114 MPa | Reaction (×W) |
|---|---|---|---|---|
| V ≥ 3 m/s (author's bracket) | V = 1.5 m/s, n = 3 | 2.23e-4 | 0.449 / 0.271 mm | 57–113 |
| σ_y = E × 0.5% (assumed) | S7-D's herring tensile yield, 62.6 MPa (Fiedler et al. 2019, **relayed, not read by me**) | 1.08e-4 | 0.26 mm | unchanged |
| Rod is solid and round | real element is a thin plate or radials | — | not computable: section unknown | — |
| Muscle-held joint loads bone as a beam | load enters as point forces of 5–55 W at the facets and the muscle origin | — | bearing and shear not computable: facet area unknown | — |

Lowering V puts the required section outside the claimed 0.12–0.35 mm range. But at 1.5 m/s the fin would
have to be 8.9 cm long on a 4 cm fish. The design would be absurd, so the author's speed bracket is
defensible as a design choice, though it is not measured. None of these relaxations flips the conclusion
on its own. The conclusion is still open because the comparator is unmeasured.

## 4. Evidence level

"Derived" is honest. The claim says "computed" and "probably", and it names the missing measurements.
The key number carries its conditions (V, n, C_L). C_L = 0.78 is at search-summary level in S7, and S7
reports a conflicting CFD value of 1.03. The claim uses the conservative value. **No defect here.**

## 5. Counter-examples and regimes

- In flying fish (Exocoetidae) and hatchetfish (Gasteropelecidae), girdles that bear glide or leap loads are
  *hypertrophied or fused* (S7's sources, at search-summary or listing level). That supports the claim's
  emphasis on the joint and lock. It does not count against it.
- I ran no new literature search, so this review adds no counter-example. **Scope of that negative: none
  searched. Only the two S7 documents were read.**
- Regime not covered by the claim: water-exit impact and repeated-launch fatigue. The author lists both as
  not analysed. Either could exceed the n = 3 bracket. Whether it does is **unknown**.

## 6. What survives

- Root moment ≈ 1.1e-4 N·m at V = 3, n = 3 (reproduced; 1.0e-4 N·m with lift over the full span).
- Required solid-equivalent section 0.12–0.35 mm (reproduced).
- Joint as the open constraint: survives, with the reaction range corrected to ~5–55× W.
- "Bone probably not limiting": an untested prior, not a finding, until the section of the radial, scapula
  or cleithrum is measured (S7-D points to MorphoSource project 000415918; not accessed by me).

```swarm-challenge
{"claim_id": 201, "outcome": "weakened", "reason": "Arithmetic reproduces (M=1.08e-4 N·m, d=0.12–0.35 mm), but the stated 9–55× joint reaction omits the V=5 m/s, n=1 case inside the claim's own moment range (true lower bound 5.3×), and 'bone probably not limiting' rests on an unmeasured girdle section that is compared against a solid-rod proxy.", "corrected_value": "joint reaction ~5–55× body weight (20.8–216 mN); root moment 1.08e-4 N·m stands (1.00e-4 N·m with elliptic lift over full span incl. body)", "depends_on": ["m=0.4 g (project brief)", "C_L=0.78 (Park & Choi 2010, search-summary)", "AR=9 (search-summary, unidentified source)", "V=3–5 m/s (assumed bracket)", "n=1–3 (assumed bracket)", "sigma_y=25–114 MPa (assumed E×0.5% construction)", "muscle stress 200 kPa (assumed)", "moment arm r=0.5–1.0 mm (assumed)", "body half-width 2.5 mm (assumed)", "zebrafish girdle section: unknown"]}
```
