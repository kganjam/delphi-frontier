# Challenge 93: adversarial review of S6-D-D (the passive-ray EI transfer)

**Claim under review** (written by another pass, branch `claude/deepen-s6-d-sensitive-input-fc1hm8`,
`docs/research/fish/S6-D-deepen.md`, commit `dc6acca2`, read in full along with `S6-D-deepen_calc.py`):

> S6-D's verdict rested on an unstated size-transfer exponent β = 0. Alben 2007's k = 1.98 N/m bounds passive
> bluegill EI ≤ 4.3×10⁻⁵ N·m². Isometric scaling gives 3.4×10⁻³, which passes against the required
> 1.8×10⁻⁴ to 3.1×10⁻³. Reaching 6.3×10⁻⁴ needs β ≥ ~2.5. Whether a passive flying-fish ray carries glide
> load is UNRESOLVED.
> Recorded evidence level: *derived*. Value: 4.3×10⁻⁵ N·m².

**Outcome: WEAKENED.** The arithmetic reproduces. The "unresolved" conclusion survives. But the number the
claim leads with is a loose bound built on a load-point assumption that the primary source contradicts, and
it is labelled "passive" when it is actually the base-locked (stiffest) state. Once both are corrected, the
favourable isometric case no longer clears the whole requirement band, and a strictly passive (free-base)
ray fails even under isometry. Every number below is **calculated by me**. Nothing here is an observation.

## 1. Independent arithmetic, from the stated inputs

I worked these from the inputs directly, not from the author's script.

| Quantity | Inputs | My result | Claim |
|---|---|---|---|
| EI_req = P L²/(8c), P = mg/(2N) | m = 0.10 kg, g = 9.81, N = 14, L = 0.12 m, c = 0.10 | P = 0.03504 N, EI_req = **6.31×10⁻⁴ N·m²** | 6.31×10⁻⁴ ✔ |
| Tip-load bound k L³/3 | k = 1.98 N/m, L = 40.3 mm | 0.0403³ = 6.545×10⁻⁵; ×1.98/3 = **4.32×10⁻⁵** | 4.32×10⁻⁵ ✔ |
| Isometric transfer λ⁴ | λ = 120/40.3 = 2.978, λ⁴ = 78.6 | 4.32×10⁻⁵ × 78.6 = **3.40×10⁻³** | 3.40×10⁻³ ✔ |
| β to reach 6.31×10⁻⁴ | ln(6.31e-4/4.32e-5)/ln 2.978 = 2.681/1.091 | **2.46** | 2.46 ✔ |

No arithmetic error. Every attack below is on inputs and framing.

## 2. Proxy and hidden assumption: the load point is in the primary source, and it is not the tip

The claim's key number is EI ≤ k·L³/3, which puts the point load at the ray tip (a = L). The author marked
Alben's load point `unknown` because the full text could not be opened.

I read Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243 (PMC2359861) at pmc.ncbi.nlm.nih.gov.
**Read-level: full-text, through an automated fetch-and-summarise tool.** It is not a verbatim read of the
PDF, so it should be re-checked. What that read reports:

- The force was applied **about two-thirds of the distance from the ray base to the tip** (Fig. 7a).
- The clamped-base force–displacement slope is **1.98 N m⁻¹**, about **12×** the slope with one hemitrich
  free. No numeric free-base slope is given.
- The maximum ray length is 40.3 ± 0.8 mm, across six fish.
- The authors' own estimate is E ≈ 10⁸–10⁹ Pa, I ≈ 10⁻⁶ cm⁴, giving EI ≈ 10⁻⁶–10⁻⁵ N·m².
- The paper gives **no bluegill body length or mass**.

Putting a = (2/3)·40.3 mm = 26.9 mm into k = 3EI/a³ (still assuming a rigid root and a uniform beam) gives
these values (**calculated**):

| State | EI (N·m²) | Isometric at 120 mm (×78.6) | β to reach 1.8e-4 / 6.31e-4 / 3.1e-3 |
|---|---|---|---|
| Claim: tip load, bases clamped | 4.32×10⁻⁵ | 3.40×10⁻³ | 1.31 / 2.46 / 3.92 |
| **Load at 2/3 L, bases clamped** | **1.28×10⁻⁵** | **1.01×10⁻³** | 2.42 / **3.57** / 5.03 |
| Load at 2/3 L, one base free (k/12) | 1.07×10⁻⁶ | 8.4×10⁻⁵ | 4.70 / **5.85** / 7.31 |
| Tip load, one base free (k/12) | 3.6×10⁻⁶ | 2.8×10⁻⁴ | 3.59 / 4.73 / 6.19 |

My reading of this table (inference):

- **Using the source's own load point, the bound is too loose by ×3.4.** The point estimate 1.28×10⁻⁵ is
  just above the top of Alben's stated range of 1×10⁻⁶–1×10⁻⁵ N·m². That is a better consistency check than
  the author's, which inferred a = 11.5–24.7 mm. The measured 26.9 mm sits just outside that span. It is close
  enough that the two still roughly agree, given that Alben's range is an order-of-magnitude estimate.
- **Even with this correction, the claim's headline "isometry passes" survives only partly.** At 120 mm the
  isometric value 1.01×10⁻³ beats the central 6.31×10⁻⁴, but not the top of the band (3.1×10⁻³). The β needed
  for the central case rises from 2.46 to 3.57, so the margin under isometry (β = 4) shrinks from ~5× to ~1.6×.
- One flaw in the claim's comparison: the band's upper end, 3.1×10⁻³, was computed at L = 160 mm, but the
  claim compares it with an isometric value computed at L = 120 mm. The values at each length should be
  compared with each other. That does not reverse anything, because the 160 mm isometric value also grows,
  but "passes against 1.8e-4 to 3.1e-3" mixes lengths.

## 3. "Passive" is mislabelled: the 1.98 N/m state is the base-locked state

The claim calls 4.3×10⁻⁵ the "passive bluegill EI upper bound". The author's own §3a says 1.98 N/m is the
**actively locked, stiffer** state, with both hemitrich bases clamped. The source confirms that the
one-base-free slope is ~12× lower.

- As an upper bound on a truly passive (free-base) ray, the number is correct but **loose by ~12× on top of
  the ×3.4 from the load point.**
- **For a passive ray in the strict sense** (no base-locking), the estimate is ~1.07×10⁻⁶ N·m². Scaled
  isometrically to 120 mm that gives 8.4×10⁻⁵, which **fails against the entire 1.8×10⁻⁴–3.1×10⁻³ band**.
  The β needed is 5.85, close to elastic similarity (β = 6).
- So the "unresolved" verdict holds only if "passive" is allowed to include a hemitrich base that is held
  locked statically during the glide. That is a mild active mechanism, and it belongs to S26's question
  (active stiffening), not to a passive-ray model.

My inference: the claim's split, "fails at β = 0, passes at isometry", is really a 2-D split. One axis is β.
The other is the base state (clamped vs free), which moves EI by ~12×, as much as a change in β of ~2.3. The
claim does not carry the second axis into its verdict.

## 4. Is "size transfer" the right frame? A shape transfer, not a body-size transfer

The claim frames β as a **size**-transfer exponent, with isometry meaning ray diameter ∝ ray length. A
bluegill-to-flying-fish ray-length ratio of ~3× does not imply a 3× body-size ratio:

- The flying-fish ray lengths used come from the author's search-summary morphometrics: *C. hiraii* SL
  199–209 mm, and a fin ceiling of ≤0.78 SL.
- Bluegill body length in Alben 2007 is **unknown**. The paper does not report it (full-text summary above).
  I did not search further.
- If the bluegill used were of similar body length to these flying fish, the 3× ratio would come from
  **fin elongation**, not body size. In that case "isometry" (d ∝ ray length) is not a neutral reference.
  It assumes a longer fin on the same-sized fish carries proportionally thicker rays. That is exactly the
  unmeasured biological question, and isometry gets no privilege over β = 0 as a prior.

This is a conditional I could not settle. It weakens the claim's implication that S6-D made a
size-correction *error*. It does not overturn "unresolved".

## 5. Evidence level

- Labelling **4.3×10⁻⁵ as "derived"** is honest. The author tags it *calculated* throughout and never
  presents it as measured. ✔
- **Defect.** The k input was relayed through S26's automated full-text summary, and the load-point
  assumption (tip) was chosen without the source. The source states a different load point. So the recorded
  key number is a derived value resting on an assumption the primary source contradicts. A better recorded
  value is **≈1.3×10⁻⁵ N·m² (base-clamped, load at 2/3 L, rigid root; calculated)**. For a strictly passive
  free-base ray it is **≈1×10⁻⁶ N·m² (calculated)**.
- My own read of Alben 2007 went through a summarising fetch tool. A verbatim check of Fig. 7a's caption
  would firm this up.
- Minor: Alben's own E ≈ 0.1–1 GPa sits at or below the low end of the 0.24–3.7 GPa bracket used in the
  claim's §3d. At E ≤ 1 GPa, the threshold diameters in §3d are the upper rows (≥1.4–4 mm), which makes the
  passive pass harder.

## 6. Counter-examples and regimes not considered

- **Compliant root.** If the root rotated in Alben's rig, k under-reads EI and every row above is a lower
  estimate. The author flagged this. It works in the claim's favour, and its size is `unknown`.
- **Hollow, tapering hemitrichs.** EI falls distally. A tip-load uniform-beam inversion and a uniform-load
  uniform-beam requirement are not the same beam. The direction of the error is `unknown` without a taper
  profile.
- **A published measurement of flying-fish ray cross-section or EI.** None was found. Scope: I ran no new
  literature search beyond fetching Alben 2007. I relied on the author's stated negative search (Europe PMC,
  two queries; Scholar and WoS not searched).

## 7. Verdict

**WEAKENED, not refuted.**

What holds:

- The arithmetic is correct.
- S6-D did transfer an absolute EI across a 3× ray-length change without saying so.
- The passive-ray question is not closed by the evidence S6-D used.

What does not hold:

- The headline bound of 4.3×10⁻⁵ is ×3.4 looser than the source's own load point allows: the load was at
  ~2/3 L, giving ≈1.28×10⁻⁵ N·m².
- That value belongs to the base-locked state. A strictly passive free-base ray is ≈1.1×10⁻⁶ N·m².
- With these corrections, the isometric case beats the central requirement by only ~1.6×, and it does not
  clear the top of the band.
- The β needed rises from 2.46 to 3.57 (clamped), or to 5.85 (free).
- **Under isometry, a free-base passive ray fails across the whole requirement band.** The claim's
  "unresolved" holds only if a statically locked base counts as passive, which is a definitional choice the
  claim does not make explicit.

Relations kept, not averaged:

- This challenge sits between claim 72 (S6-D falls) and S6-D-D (unresolved).
- Under the strict-passive reading, it sides with claim 72.
- Under the locked-base reading, it sides with S6-D-D.

## Sources

| Source | Read-level |
|---|---|
| S6-D-deepen.md and S6-D-deepen_calc.py, commit dc6acca2 | full-text |
| Alben S, Madden PGA, Lauder GV 2007 *J R Soc Interface* 4:243, PMC2359861 (pmc.ncbi.nlm.nih.gov) | full-text via automated summarising fetch (not a verbatim PDF read) |
| Challenge 72 (78d717cf), S26 (b5ac55ae) | listing only (commit headers); not re-read |

```swarm-challenge
{"claim_id": 93, "outcome": "weakened", "reason": "Arithmetic reproduces, but Alben 2007's full text puts the 1.98 N/m load at ~2/3 of ray length (not the tip) and in the base-clamped state, so the bound tightens to ~1.28e-5 N m^2 (beta needed 3.57, isometric margin ~1.6x and not clearing 3.1e-3) and a strictly passive free-base ray (~1.1e-6) fails even under isometry (beta needed 5.85), leaving 'unresolved' true only if a statically locked base counts as passive.", "corrected_value": "1.3e-05 N m^2 (base-clamped bluegill ray EI, load at 2/3 L, rigid root; calculated); ~1.1e-06 N m^2 for one hemitrich base free (calculated)", "depends_on": ["Alben, Madden & Lauder 2007 J R Soc Interface 4:243 (PMC2359861): clamped-base point-load slope 1.98 N/m applied ~2/3 of base-to-tip distance (full-text via automated summarising fetch)", "Alben 2007: clamped/one-free slope ratio ~12x (same read)", "Alben 2007: max ray length 40.3 +/- 0.8 mm; EI estimate 1e-6 to 1e-5 N m^2; no body size reported (same read)", "assumption: rigid root, uniform Euler-Bernoulli beam, k = 3EI/a^3", "assumption: EI_free ~ EI_clamped/12 (stiffness ratio applied to EI)", "S6-D scenario inputs m=0.10 kg, L=0.12 m, N=14, c=0.10 (assumptions, commit cc30ccb5)", "S6-D-D load band EI_req 1.8e-4 to 3.1e-3 N m^2 (calculated by claim author from search-summary morphometrics)", "assumption: size transfer EI proportional to L^beta, beta = 4 as isometric reference", "flying-fish ray length 105-160 mm (search-summary, via S6-D-D)"]}
```
