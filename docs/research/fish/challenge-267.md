# Challenge 267 — bluegill pectoral ray EI from Alben et al. (claim S25-D)

**Claim under review (verbatim, condensed).** Replacing the unsourced 1–2 mm solid-rod proxy with
Alben et al.'s measured cantilever stiffness (1.98 N/m, L = 40.3 mm) gives a *calculated* clamped
EI of 5.4e-6 to 4.3e-5 N m² (1.28e-5 at the load point), and 1.07e-6 N m² with one hemitrich free.
So 3.8e-6 N m² is physically consistent, and 565e-6 N m² is 13–105× too stiff. 565e-6 remains
the abstract's printed value, but S25's conclusion that it is the relaying to trust "falls".

**Verdict: SURVIVED**, with three framing caveats. None of them changes the conclusion.

## Sources and read-levels

| Source | Read-level | What I took from it |
|---|---|---|
| Alben, Madden & Lauder, *J R Soc Interface* 4:243–256, doi:10.1098/rsif.2006.0181 (PMC2359861; online Nov 2006, issue dated 2007) | full-text (PMC HTML, read through a fetch-and-summarise tool, so passages are quoted second-hand) | Fig. 7 caption: both bases clamped, slope 1.98 N/m, "about 12 times the value when one hemitrich is free"; point force "at two-thirds of the distance" along a horizontally clamped ray; "maximum ray length = 40.3 ± 0.8 mm, mean ± s.e."; three-point bending gives E ≈ 1e8–1e9 N/m² and I ≈ 1e-6 cm⁴; "measured B = EI ≈ 1e-6–1e-5"; B is defined as the bending rigidity of *a hemitrich* |
| Flammang, Alben, Madden & Lauder 2013, *J Morph* 274:1044–1059 | search-summary only | the abstract reports flexural stiffness "calculated to be 565×10⁻⁶ N m²". I did not read the methods for how it was calculated (`unknown`). Fetching the full text failed: sites.harvard.edu and deepblue.lib.umich.edu are outside this session's allowed network |
| Lauder group SPIE 2007 conference report | search-summary only | across rays, stiffness spans nearly two orders of magnitude; proximal stiffness is up to 30× distal |

I could not trace where 3.8e-6 comes from. A search snippet found no 3.8e-6 in the Flammang 2013
abstract. Scope of that search: one web search plus two blocked fetches. I take the number as the
claim gives it, as S25's alternative relaying.

## 1. Arithmetic, redone independently

Uniform Euler–Bernoulli cantilever with a point load at distance a: k = 3EI/a³, so EI = k·a³/3.
Inputs: k = 1.98 N/m, L = 0.0403 m.

| load point a | EI (N m²), calculated |
|---|---|
| L/2 | 5.40e-6 |
| 2L/3 (the paper's stated load point) | 1.28e-5 |
| L | 4.32e-5 |
| 2L/3, one hemitrich free (k ≈ 1.98/12 = 0.165 N/m) | 1.07e-6 |

565e-6 divided by 4.32e-5 is 13.1, and by 5.40e-6 is 104.6. The arithmetic matches the claim.
All the EI values in this note are **calculated** from a measured k. None of them is an observation.

## 2. Proxies

- **L = 40.3 mm is a proxy for the length of the tested ray.** It is the mean *maximum* ray length
  across the morphology sample, not the length of the ray loaded in Fig. 7. The tested ray's length
  is `unknown` from my read. Fig. 2 shows ray 4 of 13, which need not be the longest. Since EI ∝ a³,
  a shorter ray *lowers* the calculated EI, so the 565e-6 gap only *widens*. The proxy is
  conservative in the direction that matters.
- **"Authors state EI ~1e-6 to 1e-5".** Strictly, the authors' B is a *hemitrich* rigidity, not the
  whole clamped ray. The point still holds independently: their own three-point-bending E and I
  (1e8–1e9 N/m² × 1e-14 m⁴) give a whole-structure EI of 1e-6–1e-5 N m². That is a second
  measurement route that agrees with the cantilever calculation. To reach 565e-6 with I ≈ 1e-14 m⁴
  you would need E ≈ 5.7e10 N/m², which is above the usual range for bone (my inference from
  general knowledge; I did not source it in this note).

## 3. The hidden assumption relaxed: a uniform beam

Rays taper, with proximal stiffness up to about 30× distal. I tested whether 565e-6 could be a
*base* value that is compatible with the measured k. For a cantilever, compliance at the load point
is weighted by (a − x)², so the stiff base dominates. Calculated case: EI(x) = 565e-6·exp(−ln30·x/L),
load at 2L/3. This gives an effective EI of 2.9e-4 N m², which is still about 22× the measured-k
value of 1.28e-5. Tapering cannot reconcile 565e-6 with Alben's k as a whole-ray value. It could
only be a very local value at the extreme base, and the claim's argument would then not be about it
at all.

Excision and boundary conditions: in vivo the bases are held by muscle and tendon, between the two
cases tested. That spans 1.07e-6 to 1.28e-5 (or 4.3e-5 at most), and both ends are far below 565e-6.

## 4. Evidence level

The claim's sentence says the EI values are "calculated from measured k". That is honest. The
recorded level `literature` with value `n/a` is acceptable only because no derived number is
written into the value field. If the 1.28e-5 is ever entered there, it must be labelled
calculated/derived, not literature.

## 5. Overstatement and possible counter-examples

- "3.8e-6 is physically consistent" is slightly loose. 3.8e-6 is *below* the fully clamped band
  (5.4e-6 at minimum) and above the one-free value (1.07e-6). It is consistent with partial base
  constraint or a shorter tested ray, not with the clamped calculation as stated. This does not
  rescue 565e-6.
- Ray-to-ray variation is about 100× (SPIE 2007, search-summary). A stiff middle ray could exceed
  the Fig. 7 ray, but reaching 565e-6 needs about 44× the calculated clamped value at the paper's
  load point, and I found no measured bluegill value that high. Scope of that negative: the two
  Lauder-group sources above plus the Alben full text. No wider literature search was done.
- Whether 565e-6 is an exponent misprint (for example 5.65e-6) or a calculation for a fused solid
  section: `unknown`. The Flammang methods could not be accessed.

## Conclusion

The arithmetic reproduces, the load-point choice matches the paper, and the one proxy (L) is biased
in the direction that strengthens the claim. Relaxing the uniform-beam assumption also fails to
bring 565e-6 into agreement with the measured k. An independent measurement route (three-point E·I)
agrees on 1e-6–1e-5 N m². I could not break the claim. The caveats: L is the maximum ray length,
not the tested ray's; the authors' B is a hemitrich quantity; and 3.8e-6 sits just below the
clamped band.

```swarm-challenge
{"claim_id": 267, "outcome": "survived", "reason": "Independent recalculation (EI = k a^3/3, k = 1.98 N/m) reproduces 5.4e-6 to 4.3e-5 N m^2; relaxing the uniform-beam assumption with a 30x taper still leaves 565e-6 about 22x stiffer than the measured k allows, and Alben's separate three-point-bending E and I also give 1e-6 to 1e-5 N m^2, so 565e-6 is not supported as a whole-ray bluegill EI (caveats: L = 40.3 mm is mean maximum ray length, which is conservative; 3.8e-6 sits just below the clamped band).", "corrected_value": null, "depends_on": ["Alben et al. 2007 Fig. 7: k = 1.98 N/m both bases clamped, about 12x the one-hemitrich-free value", "Alben et al. 2007: load applied at about 2/3 of ray length", "Alben et al. 2007: maximum ray length 40.3 +/- 0.8 mm used as proxy for tested-ray length", "Alben et al. 2007: three-point bending E about 1e8-1e9 N/m^2, I about 1e-6 cm^4", "Euler-Bernoulli cantilever relation k = 3EI/a^3", "SPIE 2007 (search-summary): proximal stiffness up to 30x distal, used for taper test", "Flammang et al. 2013 abstract (search-summary): 565e-6 N m^2 calculated flexural stiffness"]}
```
