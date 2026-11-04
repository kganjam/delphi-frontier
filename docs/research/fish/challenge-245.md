# Challenge 245: adversarial review of the replication of claim 201 (S7 pectoral girdle)

**Claim under review (it is not mine).** "Replication: moment 2.1e-5..1.08e-4 N m per fin and bone d 0.12-0.35 mm reproduce; the joint reaction lower bound of 9x drops the V=5 m/s, n=1, r=1 mm case that is already in the moment range, giving 5.3x, so range is ~5.3-55x body weight. Qualitative conclusion stands."
Recorded evidence level: derived. Value: 5.3 × body weight (lower bound).

**Source.** `docs/research/fish/replicate-201.md` on branch `claude/rederive-s7-pectoral-girdle-r2hm12`, commit eb8f483. Read-level: full-text. I took the inputs from its §1 table. I did not read the original harvest file `S7-organ.md` or any other challenge branch.

**Verdict: SURVIVED, with two scope caveats.** I recomputed the claim independently and it holds. Neither caveat changes the stated correction from "9×" to "~5×". They limit how the number "5.3" should be read.

## 1. Independent arithmetic (calculated, not observed)

My script is `challenge-245.py` in this directory. I wrote it from the stated formulas and did not copy the replicator's code. Inputs:

- W = 0.4 g × 9.80665 = 3.923 mN
- ρ = 1.204 kg m⁻³, AR = 9, y₀ = 2.5 mm
- C_L = 0.78 (and 1.03 as a check)
- V ∈ {3, 5} m s⁻¹, n ∈ {1, 3}, r ∈ {0.5, 1.0} mm

The model, in order:

- Wing area: S = 2W/(ρV²C_L)
- Span: b = √(AR·S)
- Fin length: s = b/2 − y₀
- Lift centroid: ȳ = 4s/3π
- Root moment: M = (nW/2)·ȳ
- Bone diameter: d = (32M/πσ)^⅓
- Muscle force: F_m = M/r

| Quantity | My value | Claim | Match |
|---|---|---|---|
| M, V=3, n=3 (maximum) | 1.079×10⁻⁴ N·m | 1.08×10⁻⁴ | yes |
| M, V=5, n=1 (minimum) | 2.074×10⁻⁵ N·m | 2.1×10⁻⁵ | yes |
| d, max M at σ=25 MPa | 0.353 mm | 0.35 | yes |
| d, min M at σ=114 MPa | 0.123 mm | 0.12 | yes |
| F_m/W, V=3, n=1, r=1 mm | 9.17 | the original "9×" | yes |
| F_m/W, V=5, n=1, r=1 mm | 5.29 | 5.3 | yes |
| F_m/W, V=3, n=3, r=0.5 mm | 55.0 | 55 | yes |

The structural point also holds. The case V=5, n=1 sets the lower end of the claim-201 moment range (2.07×10⁻⁵, rounded to "2×10⁻⁵"). With r = 1 mm, the same case gives 5.3 W. So the original "9–55×" was internally inconsistent with its own moment range, and the replicator's correction is right.

## 2. Proxy: a muscle force is reported as the joint reaction

The 5.3× is **F_m**, the adductor force needed to balance the root moment. The quantity the claim names is the **articular reaction**, which is the vector sum of the muscle force and the fin's lift. The replicator discloses this but bounds the error at ±1.5 W. At n = 1, the case that sets the lower bound, the lift per fin is only nW/2 = 0.5 W. So in that case the error is ±0.5 W, not ±1.5 W.

The reaction depends on the lever class, and the lever geometry is **unknown**:

- **Muscle and lift on the same side of the joint** (class 3; the arrangement of the bird pectoralis). They are antiparallel, so R = F_m − L = **4.79 W**.
- **On opposite sides** (class 1). R = F_m + L = **5.79 W**.

These are my inferences from lever statics, not measured anatomy. So the honest lower bound for the articular reaction at this grid corner is **4.8–5.8 W**, not exactly 5.3 W. That is still "~5×", so the claim's "~5.3" survives as an approximation.

## 3. The hidden assumption: the lower bound is a corner of an assumed grid

"Lower bound" here means the minimum over the author's bracket of V, n and r. It is not a physical bound. I relaxed each input in turn (all values calculated):

- **C_L = 1.03.** This is the competing value, which the replicator confirmed at abstract level. The minimum F_m falls to **4.53 W**, and the class-3 reaction to **4.03 W**.
- **Faster glide.** V = 3–5 m s⁻¹ is the author's own bracket, not a measurement. The moment falls with V because the wing shrinks. Holding C_L = 0.78 and r = 1 mm, F_m/W = **3.6 at 7 m s⁻¹** and **2.4 at 10 m s⁻¹**. I did not verify the glide speeds of real flying fish in this session, so I cannot say whether they fall in this range. That is a scope limit, not a finding.
- **r > 1 mm.** F_m scales as 1/r, and r is a guess. Any larger moment arm lowers the bound in proportion.

Under these relaxations the lower bound moves down, never up. So the replicator's direction of correction (below 9×) is robust. The specific figure "5.3" is conditional on V ≤ 5 m s⁻¹, C_L = 0.78 and r ≤ 1 mm.

Relaxations do not threaten the upper bound of ~55× W or the qualitative conclusion. Under every relaxation I tried, the bone stays sub-millimetre and the joint load stays several times body weight.

## 4. Is the evidence level honest?

Yes. "Derived" is correct, and both the source file and the claim present the numbers as calculated, conditional on assumed inputs. "Not re-run by harvester" is a provenance statement, and I have no evidence against it. One wording defect: the recorded value says "joint reaction" for what is a muscle force (§2). The 0.5 W gap is within the "~".

## 5. Counter-examples

**Not searched.** I made no literature or database search for measured teleost girdle sections, adductor PCSA, or joint loads in flying fish or zebrafish. The real girdle section and adductor PCSA remain **unknown**, as the source also states. So I can neither confirm nor refute the claim against anatomy. My verdict covers only the arithmetic and its internal consistency.

## Bottom line

The claim reproduces exactly. The 9× lower bound was inconsistent with the moment range, and ~5× is correct on the stated inputs. The precise lower bound for the articular reaction is 4.8–5.8 W, not 5.3 W, and it falls further (to about 4 W, or below with faster glide or a longer lever) when unverified inputs are relaxed. None of this overturns the claim's statement.

```swarm-challenge
{"claim_id": 245, "outcome": "survived", "reason": "Independent recomputation reproduces M = 2.07e-5 to 1.08e-4 N m, d = 0.12-0.35 mm and a minimum muscle force of 5.29 W at V=5, n=1, r=1 mm, so the 9x lower bound was indeed inconsistent; the residual caveats (5.3 is a muscle force, the articular reaction is 4.8-5.8 W at n=1, and the bound is a grid corner that falls with C_L=1.03, faster V or larger r) are within the claim's '~' and do not reverse it.",
  "corrected_value": null,
  "depends_on": ["body mass 0.4 g", "C_L = 0.78 (unverified; 1.03 competing)", "V bracket 3-5 m/s (author assumption)", "AR = 9", "y0 = 2.5 mm", "load factor n = 1-3", "adductor moment arm r = 0.5-1.0 mm (guess)", "bone yield 25-114 MPa (assumed)", "elliptic fin-only lift distribution (Model A)", "lever class unknown (sets +/-0.5 W at n=1)"]}
```
