# Challenge 181: adversarial review of S23-D (actinotrichial modulus E0)

Claim under review (author: harvest `deepen-s23-actinotrichia-bhvko5`, file
`docs/research/fish/S23-deepen.md` @ `efff2517`, read in full along with `S23-deepen-calc.py`):

> The answer is most sensitive to E0, the only input whose stated range (1.2 MPa–0.5 GPa) crosses
> the computed flip threshold (10–255 MPa). Replacing the generic-collagen AFM proxy with an
> elastoidin lower bound keeps the conclusion, but only by ~1.4× at the lenient design corner.
> KEY: E0 ≥ ~0.35 GPa (conditional). VERDICT: stands.

Recorded evidence level: `derived`. Date of review: 2026-11-04.

**Outcome: WEAKENED.** All of the arithmetic reproduces. Two of the claim's statements go
further than the arithmetic supports: the word "only", and the "stands" verdict at the lenient
corner.

---

## 1. Independent arithmetic (computed, not observed)

I re-derived these from the stated model, not from the author's script. The model is
`EI_req = (W/2)L²/(8·tol)`, with `W = 0.4 g × 9.81`, `S = EI_req/EI_meas`, `C = E_target/E0`,
`margin = S/C`, and `f = 1`.

- W/2 = 1.962×10⁻³ N.
- Central case (L = 4 cm, tol = 10 %, EI_meas = 4×10⁻⁹ N·m²): EI_req = 3.924×10⁻⁶ N·m², so
  **S = 981**.
- Lenient corner (L = 2 cm, tol = 50 %, EI_meas = 5×10⁻⁹ N·m²): EI_req = 1.962×10⁻⁷ N·m², so
  **S = 39.24**.
- Flip threshold `E0* = E_target/S`:
  - 10 GPa target: 254.8 MPa (lenient) and 10.2 MPa (central).
  - 5 GPa target: 127 MPa (lenient) and 5.1 MPa (central).
- With E0 = 0.35 GPa and E_target = 10 GPa: C = 28.6. The margin is **1.373** (lenient) and
  **34.3** (central).
- The uniform-load cantilever relation is dimensionally correct. Tip deflection is
  wL⁴/(8EI) with w = (W/2)/L, so setting it equal to tol·L gives the form above.

**Every number in the claim reproduces.** I found no arithmetic error.

## 2. "The only input whose stated range crosses the flip threshold": false at the lenient corner

This is computed from the author's own ranges. With the parent's E0 = 0.2 GPa, the equivalent
threshold on the *target* modulus at the lenient corner is `E_target* = S·E0 = 7.85 GPa`. That
value lies inside the parent's stated target range of 5–10 GPa. The author's own §1 table shows
the same thing: the 0.2 → 10 GPa row flips at the lenient corner.

So at the lenient corner, both E_target and the design range (tol 5–50 % at L = 2 cm) cross the
threshold, not just E0. "Only" holds at the **central case** alone. There, E_target* would be
196 GPa, which is out of reach, and S ranges from 39 to 5232 at C = 25 without crossing 1.

This point is about how the claim is worded. It does not change the conclusion. E0 still has the
widest stated spread (~417×, against ~133× for S across every design and EI_meas corner).

## 3. The hidden assumption that carries the lenient-corner "stands"

The surviving margin of 1.37 means the conclusion at the lenient corner tolerates only a ~27 %
error in E0. E0 has to stay above 255 MPa, against a bound of 350 MPa. That bound rests on two
links, and the author flags both as unread:

1. **The qualitative claim that wet elastoidin is stiffer than tendon.** I confirmed this at
   `search-summary` level from the Journal of Biosciences abstract page. The search summary also
   says that wet specimens were tested in Ringer's solution. I could not read the figures. Both
   `www.ias.ac.in` and `link.springer.com` were refused by this session's egress proxy
   (`connect_rejected`). The elastoidin modulus value is therefore `unknown`.
2. **The reference value of ≥ 0.35 GPa for the 1981 study's own tendon.** This is where the
   proxy problem sits. The 350 ± 53 MPa figure is a wet *fibril* tangent modulus. Rajaram et al.
   tested macroscopic *fibres* in their own preparation, at their own strain rate, with their own
   way of estimating cross-section.
   - The author's own search summary gives fibre-level wet tendon values of 0.48–0.57 GPa. That
     already differs from the fibril value by about 1.4–1.6×, which is as large as the whole
     surviving margin.
   - The tendon modulus the 1981 study actually measured is `unknown`. I searched for wet
     rat-tail-tendon fascicle moduli measured in Ringer's solution (one standard web query,
     2026-11-04) and found no number. The summary did note that the calculated modulus depends on
     how cross-section is estimated and on loading rate.
   - If the 1981 tendon measured below ~255 MPa, "stiffer than tendon" no longer implies
     E0 > E0*, and the lenient corner flips.

**My inference:** the bound could plausibly move either way, by more than 1.37×. The direction
of the conclusion at the lenient corner is therefore **undetermined**, not "stands". The author
says the bound is "conditional". But the headline verdict ("stands … by ~1.4×") reports the
margin as if it survived, when it is smaller than the spread between the author's own two
reference values.

Other inputs show the same fragility at that corner (computed):

- Body mass is held at a single value, 0.4 g. At E0 = 0.35 GPa and a 10 GPa target, the lenient
  corner flips if mass is below **0.29 g**. I have no sourced zebrafish mass range, so I do not
  claim that this happens. I only note that the margin there has no room for any single input to
  be off by more than about 27 %.
- At tol = 20 % instead of 50 % (L = 2 cm), the margin is 3.4. The fragility is confined to the
  extreme corner.

## 4. Proxy check

- E0 is meant to be the **axial modulus of hydrated zebrafish actinotrichia in situ**. What is
  used is shark ceratotrichia (elastoidin) bounded against rat-tail tendon. That is still a proxy
  for both species and scale, and the author says so. I did not find a direct measurement, and I
  did not run a fresh literature search for one beyond the queries above. The author's negative
  search (web index only, two queries) stands with its stated scope.
- The author's §2 inference is that the MPa-scale AFM values are transverse indentation moduli
  and do not apply to bending. I find this physically sound, though I have not verified it
  against each source. It removes the branch that flips the central case, and it does not depend
  on the tendon reference value. The **central-case conclusion (margin ~34×, flips only if
  E0 < 10 MPa) is robust** to everything I tested.

## 5. Evidence level

`derived` is honest. The key number is labelled as a conditional lower bound and is not
presented as measured. Read-levels are given for every source. No defect here.

## 6. Counter-examples and regimes

- **Protein-only target ceiling.** To flip the lenient corner at E0 = 0.35 GPa, a protein
  material would need E_target ≥ **13.7 GPa** (computed). The parent's 10 GPa silk-like ceiling
  is already generous, because it is a dry value compared against a *wet* E0. I know of no
  hydrated, unmineralised protein material above that, but I did not search for one, so this is
  not a scoped negative.
- **Mineralisation would break the ceiling.** Lepidotrichia are bone. But mineralisation is not
  "protein-level stiffening", so it falls outside the claim's scope.

## Verdict

**WEAKENED.**

- The arithmetic and the central-case conclusion survive. Protein-level stiffening falls short
  by about 34×, and the conclusion holds for any E0 above 10 MPa.
- The parent's "1–2 orders" magnitude is correctly shown to be overstated.
- At the lenient corner, the claimed "stands by ~1.4×" rests on an unread tendon reference value.
  The author's own two reference values (fibril 0.35 GPa, fibre 0.48–0.57 GPa) differ by more
  than that margin. At that corner the outcome is **undetermined**.
- "Only input that crosses the threshold" holds at the central case only.

Settling it costs nothing: read the stress–strain figures in Rajaram et al. 1981 once
`www.ias.ac.in` is allowed in the session's network settings.

## Sources

- `docs/research/fish/S23-deepen.md` and `S23-deepen-calc.py` @ `efff2517`. Read-level:
  `full-text`.
- [Rajaram, Sanjeevi, Ramanathan 1981, J. Biosci. 3:303–309, abstract page](https://www.ias.ac.in/describe/article/jbsc/003/03/0303-0309).
  Read-level: `search-summary`.
  - [Full text](https://www.ias.ac.in/article/fulltext/jbsc/003/03/0303-0309): `could-not-access`
    (the proxy refused the connection).
- [The tensile properties and mode of fracture of elastoidin, Springer BF02702941](https://link.springer.com/article/10.1007/BF02702941).
  Read-level: `listing`. Fetch: `could-not-access`.
- [Arumugam & Sanjeevi 1987, Springer BF01086458](https://link.springer.com/article/10.1007/BF01086458).
  Read-level: `search-summary`.
- [Rosario & Roberts 2020, Front. Physiol., PMC7105874](https://pmc.ncbi.nlm.nih.gov/articles/PMC7105874).
  Read-level: `search-summary`. It gives no modulus value.

```swarm-challenge
{"claim_id": 181, "outcome": "weakened", "reason": "Arithmetic reproduces and the central-case conclusion (margin ~34x, flip only if E0<10 MPa) is robust, but the lenient-corner 'stands by ~1.4x' rests on an unread 1981 tendon reference modulus whose plausible spread (author's own fibril 0.35 vs fibre 0.48-0.57 GPa) exceeds the 1.37x margin, and E0 is not the only input crossing the threshold there (E_target* = 7.85 GPa lies inside the 5-10 GPa target range).", "corrected_value": "lenient-corner margin 1.37 (computed) is undetermined in sign-of-(margin-1); central-case margin 34.3 stands; flip thresholds E0* = 255 MPa (lenient) / 10.2 MPa (central) at a 10 GPa target", "depends_on": ["Puri 2018 EI_meas 4-5e-9 N m^2", "S23 design ranges L 2-4 cm, tol 5-50%, mass 0.4 g", "E_target 5-10 GPa (parent)", "Rajaram et al. 1981 qualitative 'wet elastoidin stiffer than tendon' (search-summary)", "wet rat-tail-tendon reference modulus 0.35 GPa fibril / 0.48-0.57 GPa fibre (search-summary)", "f = 1 (most favourable to gain-of-function)"]}
```
