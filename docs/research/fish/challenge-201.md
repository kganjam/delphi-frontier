# Challenge 201: [S7] pectoral girdle root bending moment

**Claim under review (author's words, summarized):** At design lift, the root bending moment is
2e-5 to 1.1e-4 N·m per fin for a 0.4 g fish (KEY: 1.1e-4 N·m at V = 3 m/s, n = 3, C_L = 0.78).
That moment needs only a ~0.12–0.35 mm solid-equivalent bone section, so girdle bone strength is
"probably not limiting". The unresolved constraint is the mobile fin–scapulocoracoid joint, which
must hold a 9–55× body-weight reaction through muscle or a lock. The zebrafish girdle section and
adductor PCSA that would close the comparison are unknown.

**Recorded evidence level:** derived. **Source:** `harvest:s7-organ-pectoral-girdle-xlxpkt`.
I could not find that harvest file or any related working in this repository. I searched every
tracked file except `site/` for "pectoral", "girdle", "scapulocoracoid", "zebrafish" and "s7-organ",
and got no matches. Read-level for the source: **could-not-access**. Everything below is worked
again from the inputs written in the claim.

**Verdict: WEAKENED.** The arithmetic survives. The conclusion that girdle bone is "probably not
limiting" relies on a proxy that ignores orientation (a solid round section), and that proxy is the
optimistic case.

All numbers below are **my calculations** (script in the appendix). None are observations.

---

## 1. Independent arithmetic

Inputs: m = 0.4 g, g = 9.81 m/s², n = 3, two fins sharing the load equally (my assumption; the
claim says "per fin").

- Body weight W = 3.92e-3 N. Design lift per fin L = nW/2 = **5.89e-3 N** (calculated).
- **Lever arm implied by the KEY moment:** 1.1e-4 / 5.89e-3 = **18.7 mm** to the spanwise centre of
  pressure. For an elliptic half-wing (ȳ = 4b/3π), that is a semispan of about **44 mm** on a fish of
  about 3 cm. The 2e-5 N·m lower bound implies a 3.4 mm arm (about 8 mm elliptic semispan).
- **Medium check (calculated):** at V = 3 m/s and C_L = 0.78, carrying L per fin needs
  S = L/(½ρV²C_L):
  - air (ρ = 1.2): **14 cm² per fin**. This fits a 44 mm semispan with about a 40 mm root chord.
  - water (ρ = 1000): **1.7 mm² per fin**. A fin that small has a centre-of-pressure arm of about
    1 mm or less, so M ≈ 6e-6 N·m, which is *below* the claimed range.

  So the KEY number holds together only for an **aerial, enlarged fin** (wing-like, about 14 cm²
  each). The claim does not state the medium. That should be explicit, because the same V and C_L
  in water would give a moment roughly 20× smaller.
- **Section size (solid circular, σ = 32M/πd³):**

  | σ_allow (assumed) | d at 2e-5 N·m | d at 1.1e-4 N·m |
  |---|---|---|
  | 25 MPa | 0.20 mm | 0.36 mm |
  | 50 MPa | 0.16 mm | 0.28 mm |
  | 100 MPa | 0.13 mm | 0.22 mm |
  | 150 MPa | 0.11 mm | 0.20 mm |

  Working back from the claimed endpoints gives an implied strength of about 118 MPa for the
  0.12 mm end and about 26 MPa for the 0.35 mm end. The 0.12–0.35 mm range therefore pairs the
  low moment with strong bone and the high moment with weak bone. That is a legitimate envelope and
  I **reproduce it**. The claim does not state which strength values it used. I did not look up a
  measured strength for zebrafish bone; that value is `unknown` here.
- **Joint reaction (9–55× W):** muscle force F = M / r_in. A 9× reaction at 2e-5 N·m implies
  r_in = 0.57 mm. A 55× reaction at 1.1e-4 N·m implies r_in = 0.51 mm. These are consistent with
  a single in-lever of about 0.5 mm. The peak force is 55W = **0.22 N per fin** (calculated). The
  extra L (1.5W) added to the joint reaction is small next to this.
- **Muscle check (my addition):** with a generic vertebrate isometric stress of 0.2–0.3 MPa (a
  textbook range I assumed; no specific source read), 0.22 N needs a PCSA of **about 0.7–1.1 mm² per
  fin**. The claim correctly gives the zebrafish adductor PCSA as unknown. I also do not know it.

**Result:** I could not break the numbers. KEY 1.1e-4 N·m is reproduced given an aerial fin of
about 14 cm² with its centroid about 18.7 mm out.

## 2. Proxy

**Proxy:** "solid-equivalent circular section diameter".
**Quantity that matters:** the section modulus Z of the real girdle elements (cleithrum and
scapulocoracoid), taken **about the axis the fin moment actually loads**.

Girdle elements are broadly plate-like (my general anatomical inference; I did not measure
zebrafish). The section modulus of a plate differs by about w/t between its two axes. The 0.35 mm
solid case needs Z = 4.2e-12 m³. For a plate of thickness t, calculated:

| t | width needed, strong-axis bending | width needed, weak-axis bending |
|---|---|---|
| 0.03 mm | 0.92 mm | 28 mm |
| 0.05 mm | 0.71 mm | 10 mm |
| 0.10 mm | 0.50 mm | 2.5 mm |
| 0.20 mm | 0.36 mm | 0.63 mm |

If the lift moment bends the plate in-plane, sub-millimetre widths are enough and the author's
"probably not limiting" holds. If it bends the plate out-of-plane, a thin plate (≤ 0.05 mm) would
need 10–28 mm of width. That cannot fit in a fish of about 3 cm, so bone *would* be limiting. The
round-section proxy ignores this difference and implicitly takes the favourable case. The claim
does say the girdle section is unknown. However, "probably not limiting" is a directional
conclusion, and nothing in the stated inputs supports that direction.

## 3. Hidden assumptions, relaxed

- **Load orientation relative to the girdle plate.** This is the assumption that carries the
  result; see §2.
- **No safety or fatigue factor beyond n = 3.** Because d ∝ σ^(-1/3), a 3× knock-down for fatigue
  or a safety factor raises 0.35 mm to about 0.50 mm. The conclusion is fairly robust to this.
- **Load path.** I checked whether the girdle carries more than the root moment. Treating the
  girdle as a free body, the muscle origin and the joint are both on the girdle, so the internal
  muscle couple cancels. The net load passed on to the body is about M_root + L·d, and L·d is about
  1.8e-5 N·m for a 3 mm offset (assumed). Locally, the bone between the muscle origin and the joint
  carries a couple of about M_root. **Using M_root is defensible, and I am not counting this as a
  fault.**
- **Even fin load split and steady load.** Gust, asymmetric (rolling) pull-up, or flapping inertia
  could put more than nW/2 on one fin. The claim does not quantify these, and neither do I.

## 4. Evidence level

"Derived" is honest. The claim says "computed" in the sentence and lists the zebrafish quantities
it would need as unknown. There is no defect here.

## 5. Missed regime

The KEY condition requires an aerial wing of about 14 cm² per fin (§1). At the same speed, water
has ρ about 830× higher. If any part of an extended aerial-sized fin touches water at 3 m/s (during
water exit, re-entry or taxiing), it sees loads that dwarf the n = 3 aerodynamic case. For example,
1% of the fin area wetted at C ≈ 1 gives about 0.03 N, roughly 5× the design lift per fin
(calculated). The claim does not cover water-contact load cases. This is a gap in the set of load
cases. It does not refute the calculated aerodynamic moment. I did not search the literature on
flying-fish fin folding for this review (negative-search scope: none performed).

---

## Summary

- **Survives:** the KEY moment of 1.1e-4 N·m, the 0.12–0.35 mm section envelope, the 9–55× W joint
  reaction (implied in-lever about 0.5 mm), the "derived" label, and the identification of the joint
  as an open constraint.
- **Weakened:** "girdle bone strength is probably not limiting." The solid-round proxy ignores
  orientation. For a thin plate-like girdle loaded out-of-plane, the required width (10–28 mm at
  t ≤ 0.05 mm) does not fit the animal. The correct statement is: "bone is not limiting *if* the fin
  moment bends the girdle elements about their strong axis or their thickness is ≥ about 0.2 mm;
  otherwise undetermined." Also, the medium (air) and the water-contact load case should be stated.

## Appendix: calculation script

```python
import math
m=0.4e-3;g=9.81;W=m*g;n=3;V=3;CL=0.78
Lf=n*W/2
for rho in (1.2,1000): print(rho, Lf/(0.5*rho*V**2*CL))           # area per fin, m^2
for M in (2e-5,1.1e-4): print(M, M/Lf, M/Lf/(4/(3*math.pi)))     # arm, elliptic semispan
d=lambda M,s:(32*M/(math.pi*s))**(1/3)                             # solid round section
Z=math.pi*(0.35e-3)**3/32
for t in (0.03e-3,0.05e-3,0.1e-3,0.2e-3): print(t, math.sqrt(6*Z/t), 6*Z/t**2)
```

```swarm-challenge
{"claim_id": 201, "outcome": "weakened", "reason": "The arithmetic reproduces (1.1e-4 N·m needs an aerial fin of about 14 cm² with its centroid about 18.7 mm out; 0.12–0.35 mm matches σ of about 26–118 MPa), but 'girdle bone probably not limiting' rests on a solid-round proxy that ignores orientation: a thin plate-like girdle bent out-of-plane would need 10–28 mm width at t ≤ 0.05 mm, so the bone question is undetermined, not favourable.", "corrected_value": null, "depends_on": ["m = 0.4 g", "n = 3, two fins sharing load equally", "V = 3 m/s and C_L = 0.78 in air (rho = 1.2 kg/m3), inferred from consistency", "KEY root moment 1.1e-4 N·m and range 2e-5 to 1.1e-4 N·m as stated", "solid circular section sigma = 32M/(pi d^3)", "assumed bone allowable stress 25-150 MPa (no zebrafish value read)", "plate-like girdle geometry (general anatomical inference, not measured)", "generic muscle stress 0.2-0.3 MPa (assumed)"]}
```
