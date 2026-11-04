# Replication 234: the sign of S29's "property of size" (flying-fish specific energy against mass)

**Status: independent re-derivation. Comparison with the recorded value: CANNOT TELL** (the recorded value and its inputs are not in this repository; see "Comparison").

## What I was asked

The question, with the answer removed: *"S29's 'property of size' conclusion is wrong in sign. Required specific energy scales as m^beta (beta 1/3 geometric, 0.36–0.53 measured in exocoetids, Fish 1990 …"*. The task said the inputs are in `S30-organism.md`.

## Search scope (negative results, stated precisely)

- I searched the repository at commit `3272d3e` for files whose names contain `S29` or `S30`, and for files containing the strings `property of size`, `exocoet`, `flying fish` and `S30` (`*.md` only). **Nothing matched.** `S30-organism.md` does not exist in this checkout. I therefore never saw the other derivation's inputs or its result. I did not have to stop reading anything.
- Fish (1990), *J. Zool., Lond.* 221:391–403, "Wing design and scaling of flying fish with regard to flight performance":
  - A web search returned the paper's listing and a search summary: 199 specimens, six exocoetid genera; wing area, span, wing loading and aspect ratio regressed on body size. **Read-level: search-summary.**
  - I tried to fetch the full-text PDF (health-sciences.wcupa.edu) and the ADS abstract (ui.adsabs.harvard.edu). Both hosts are blocked by this session's network policy. **Read-level: could-not-access.**
  - So **I could not verify the measured exponent range 0.36–0.53.** Below it is carried as *the question's stated input*, not as something I checked. The search summary also reports that Davenport (J. Mar. Biol. Assoc. UK), on north-east Atlantic exocoetids, finds wing loading rising with **positive allometry** against standard length. That source is at read-level search-summary, and the summary said the exponent was garbled in OCR, so I quote no number from it.

## Derivation (calculated, not observed)

**1. Speed needed to glide.** In steady gliding, lift supports weight:

  ½ ρ v² S C_L = m g  ⇒  v_min² = 2 (m g / S) / (ρ C_L,max)

Here ρ is air density, S is wing (pectoral plus pelvic fin) area, and C_L,max is the maximum lift coefficient. C_L,max is assumed independent of size: the Reynolds-number range is narrow, and this assumption is mine.

**2. Required specific energy.** To leave the water, the fish must reach v_min. The kinetic energy per unit mass this takes is

  e_req = v_min² / 2 = (m g / S) / (ρ C_L,max)  ∝  W/S (the wing loading)

The other terms are independent of size to first order (my inference):
- potential energy per unit mass, g·h, for a fixed glide height;
- glide distance, (L/D)·h, which depends on L/D and not on mass.

So **e_req ∝ m^β, where β is the exponent of wing loading on mass.**

**3. Geometric similarity.** S ∝ m^(2/3), so W/S ∝ m / m^(2/3) = **m^(1/3), giving β = +1/3.**

**4. Measured exponent (input from the question, unverified by me).** β = 0.36–0.53. All of these values are above 1/3, which is positive allometry. That agrees in direction with the Davenport search summary.

**5. Size of the effect** (arithmetic):

| β | over 10× mass (10^β) | over 100× mass (100^β) |
|---|---|---|
| 1/3 | 2.15 | 4.64 |
| 0.36 | 2.29 | 5.25 |
| 0.53 | 3.39 | 11.48 |

**6. Specific energy available (my inference from standard muscle scaling; I did not consult a source for it in this session).**
- Work per unit muscle mass per contraction is roughly size-independent, scaling as m^0 (stress × strain).
- Tail-beat frequency falls with size, roughly as m^(−1/4) to m^(−1/3). So specific power available during the taxiing run falls or stays flat.
- The ratio of required to available specific energy (or power) therefore scales as **m^(≥ β), with β > 0.**

## My value

**Required specific energy for take-off ∝ m^β, with β = +1/3 under geometric similarity. The question's stated measured range is +0.36 to +0.53, which I could not verify.** So the exponent is **positive**: larger flying fish need *more* energy per kilogram to get airborne, and they have no more (probably less) specific power with which to supply it. Size is a *handicap*, not an advantage, for this task.

Uncertainty:
- On the sign: robust. Any β > 0 gives it, and β > 0 holds whenever wing area grows more slowly than m¹.
- On the magnitude: β between 0.33 (geometric) and 0.53 (top of the question's stated measured range).

This rests on two assumptions of mine: that C_L,max is size-independent, and that the take-off cost is dominated by reaching v_min.

## Comparison

- The recorded value is not in this repository. I searched for it as described above and found nothing. Its exact form is also unknown to me: it might be an exponent, a sign, or a ratio.
- My result is consistent with the *framing* in the question: S29 is wrong in sign if it concluded that size *helps*. But S29's text is also not in this repository, so I cannot confirm what S29 actually concluded.
- **CANNOT TELL.**

```swarm-replication
{"claim_id": 234, "my_value": "required take-off specific energy ∝ m^beta with beta = +1/3 (geometric; dimensionless exponent), +0.36 to +0.53 if the question's unverified Fish 1990 range holds; sign positive, so larger fish are disadvantaged", "agrees": null, "note": "I derived e_req ∝ wing loading ∝ m^(+1/3) independently, but S29, S30-organism.md and the recorded value are absent from the repo and Fish 1990 full text was network-blocked, so I cannot compare."}
```
