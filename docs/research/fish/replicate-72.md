# Replication of claim 72: "S6-D verdict falls"

**What this is:** an independent re-derivation. It is a calculation only. **Nothing was measured by me.**
Script: [`replicate-72_calc.py`](replicate-72_calc.py). Run it with `python3 -I`.

## Disclosure: what I saw before deriving

- The recorded working is `docs/research/fish/S6-deepen.md` on branch `origin/claude/deepen-fin-ray-s6-cj2i2x`.
- Before deriving, I read only its title and §0, which is the problem statement. §0 reconstructs the S6 claim as:
  *"a lepidotrichial ray, treated as a passive bony cantilever, is stiff and strong enough to carry its share
  of glide lift."*
- To locate the file I also listed the branch's commit, and **the commit message was displayed to me.** It
  states the conclusion qualitatively: "the passive-beam mechanism falls" and "independent values fail the
  required EI by >100x". It also mentions a "~150x" disagreement between two readings of Flammang 2013.
- So I knew the direction of their verdict before I started. I did **not** know their required EI, their
  inputs, their model or their sources until after my numbers below were computed.
- Treat the agreement on the *direction* of the verdict as only partly independent. The *magnitude*, the
  required EI, was derived blind.

## The question as I posed it

Can one pectoral fin ray, modelled as a passive cantilever, carry an equal share of a flying fish's
steady-glide lift without excessive deflection? "Falls" means the measured ray EI is below the EI this requires.

## Model (calculated)

- **Load.** In a steady glide, lift = weight W = m·g.
  - A fraction `s` of the lift is carried by the two pectoral fins.
  - Each fin has N rays sharing the load equally, so the force per ray is `F = m·g·s / (2N)`.
- **Beam.** A uniform Euler–Bernoulli cantilever of length ℓ carrying a uniform distributed load.
  - Tip deflection is `δ = F·ℓ³ / (8·EI)`.
  - Setting a criterion `δ/ℓ ≤ c` gives the required stiffness `EI_req = F·ℓ² / (8·c)`.

## Inputs

| Input | Value (range) | Source | Read-level | Status |
|---|---|---|---|---|
| body mass m | 0.15 kg (0.10–0.20) | none found. Park & Choi say mass was measured, but no value appeared in any snippet | could-not-access (J Exp Biol 213:3269 host blocked) | **assumption** |
| ray length ℓ | 0.11 m (0.09–0.13) | Park & Choi group, IUTAM 2007 proceedings (as summarised by search): wing span 233–261 mm, SL 199–209 mm. I took ℓ ≈ (span − ~25 mm body) / 2 | search-summary | **assumption** anchored to a search-summary |
| pectoral share of lift s | 0.8 (0.7–0.9) | same IUTAM summary: "area of the pelvic fins is about 20% of the total wing area". I assume lift is proportional to area | search-summary | **assumption** |
| rays per pectoral fin N | 14 (12–16) | no count found. A 1962 BU thesis on *Cypselurus* has a pectoral-ray frequency table, but the numbers were not in the snippet | search-summary (no number) | **assumption** |
| deflection criterion c | δ/ℓ = 0.10 (0.05–0.20) | none. This is the conventional edge of small-deflection beam theory | — | **assumption** |
| g | 9.81 m s⁻² | standard | — | constant |
| ray EI, candidate 1 | 565 × 10⁻⁶ N m² (bluegill pectoral ray) | Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044. The search snippet of the NJIT record reads "565×10-6 Nm2". The authors call it *calculated* | search-summary (the Harvard PDF host was blocked) | author's value |
| ray EI, candidate 2 | 0.0001–1.5109 µN m² = 1×10⁻¹⁰ to 1.51×10⁻⁶ N m² (two labrids) | Aiello et al., *J Exp Biol* 221:jeb163360. Measured by three-point bending | search-summary (silverchair host blocked) | author's value |
| ray modulus E | 1.34 GPa mean, proximal (range 0.24–3.7) for bluegill | Lauder et al. 2011, *Smart Mater Struct* | search-summary | author's value. Used only for a geometry sanity check |

**Searches and their scope:**
- WebSearch (standard), 7 queries, on fin-ray EI, flying-fish wing loading, *Cypselurus* mass and ray count.
- WebFetch was refused for these hosts: sites.harvard.edu, health-sciences.wcupa.edu and cob.silverchair.com.
- I found **no measured EI for any exocoetid fin ray.** This negative covers web search snippets only. I did
  not search a bibliographic database.

## Arithmetic (calculated)

**Nominal case:**
- F = 0.15 × 9.81 × 0.8 / (2 × 14) = **0.0420 N per ray**
- EI_req = 0.0420 × 0.11² / (8 × 0.10) = 0.0420 × 0.0121 / 0.8 = **6.36 × 10⁻⁴ N m²**

**Range.** I took all 32 corners of the input ranges above. EI_req runs from **1.1 × 10⁻⁴ to 3.1 × 10⁻³ N m²**.

**Comparison of available EI with EI_req (calculated):**

| EI candidate | EI / EI_req, nominal | EI / EI_req, corner range | Reading |
|---|---|---|---|
| Flammang 2013 abstract, 5.65×10⁻⁴ | **0.89** (δ/ℓ = 0.112) | 0.18–5.2 | marginal. Passes or fails depending on the assumptions |
| Aiello labrid maximum, 1.51×10⁻⁶ | **0.0024** (≈ 420× short) | 0.0005–0.014 | fails at every corner, by 70× to 2000× |

**Geometry sanity check (calculated).** For a solid circular rod with E = 1.34 GPa:
- d = 0.4 mm gives EI = 1.7×10⁻⁶ N m².
- d = 1.0 mm gives EI = 6.6×10⁻⁵ N m².
- Meeting the nominal EI_req needs d ≈ **1.76 mm**, uniform along the whole 11 cm length.
- Tapering would raise this further.

**Strength check (calculated).** The base moment is M = Fℓ/2 = 2.3×10⁻³ N m. In a 1 mm solid rod this gives a
peak stress of about 23 MPa. That is below typical bone strength, though I found no measured lepidotrichia
strength (`unknown`). Stiffness, not strength, is the binding constraint.

**My inference, not any author's claim:** the Flammang abstract value is the only candidate near EI_req. It
corresponds to a ~1.7 mm solid rod at E ≈ 1.3 GPa. I could not confirm a bluegill ray diameter from any source
I read. Whether 565×10⁻⁶ describes a whole proximal ray, or is an exponent problem, is **unresolved from my
sources**.

## My value

- **Required ray EI ≈ 6 × 10⁻⁴ N m²**, uncertain to about one order of magnitude (1×10⁻⁴ to 3×10⁻³), and driven
  entirely by my assumptions.
- **Verdict: the passive single-ray cantilever falls** against every independently measured ray stiffness I
  found. Those are labrid values, at most 1.5×10⁻⁶ N m², roughly 400× short at nominal and at least 70× short
  at every corner.
- It is **marginal, not falling,** if the Flammang 2013 abstract value of 565×10⁻⁶ N m² is taken at face value.
- No exocoetid ray EI exists in what I could reach. Every comparison is cross-taxon: bluegill and labrid rays
  loaded in water.
- Flying fish gliding is an observation and is not in question. What falls is the passive-ray *mechanism*.

## Comparison with the recorded value (read only after the above was computed)

I then read S6-deepen.md §1–§4. Their figures, set against mine:

**Required EI**
- Recorded: **6.3 × 10⁻⁴ N m²**, from m = 0.10 kg, N = 14, L = 0.12 m, n = 1, δ/L > 0.10, with all lift on the
  pectorals.
- Mine: 6.36 × 10⁻⁴ N m², from different assumed m, ℓ and lift share that happen to offset.

**Flammang case**
- Recorded: δ/L = 0.112, which they call marginal.
- Mine: δ/ℓ = 0.112 as well.

**Verdict**
- Recorded: "falls", for the passive-ray mechanism, with independent EI values giving δ/L ≈ 17–42.
- Mine: falls on the labrid values, at about 400× short.

**Where we differ, preserved rather than averaged:**
1. **The 3.8 × 10⁻⁶ N m² value.** They cite Puri et al. 2018 (full-text) relaying Flammang 2013 at
   3.8 × 10⁻⁶ N m². I did not find or read that relay. My "independent" comparison rests on Aiello's labrid
   range, which gives a larger shortfall (about 420×, against their about 166×).
2. **Geometry inference.**
   - Theirs: Puri reports bluegill rays 1–2 mm across, so 565×10⁻⁶ is plausible for a whole ray.
   - Mine: I had no sourced diameter and left the question unresolved.
   - Their diameter is a full-text input that I lacked, so I defer to it on that point.
3. **Shared model.** Both derivations used the same textbook model: a uniform cantilever with δ/ℓ = 0.1 and
   an assumed load. Agreement on EI_req therefore tests the arithmetic and the order of magnitude of the
   morphometric guesses. It does **not** test whether the model is the right abstraction. Both of us flag
   multi-ray curvature, base locking and load concentration on the leading-edge rays as unmodelled.

**Result: AGREE.**
- Required EI is about 6×10⁻⁴ N m² in both derivations, within 1%, which is partly coincidental given the
  different inputs.
- The passive single ray falls on every independently measured stiffness. It is marginal only on the
  Flammang abstract value.
- My knowledge of the verdict's direction, from the commit message, makes this replication weaker than a fully
  blind one.

```swarm-replication
{"claim_id": 72, "my_value": "required ray EI ~6.4e-4 N m^2 (range 1.1e-4 to 3.1e-3, assumption-driven); available independent labrid EI <=1.51e-6 N m^2 is ~400x short (>=70x at every corner), so the passive-cantilever verdict falls; marginal (EI/EI_req = 0.89) only on the Flammang 2013 abstract value of 565e-6 N m^2", "agrees": true,
  "note": "Required EI matches the recorded 6.3e-4 N m^2 within 1% and the verdict 'falls' matches. Independence is weakened because the source commit message, which states the verdict direction, was seen before deriving, and because both derivations use the same uniform-cantilever model on assumed load inputs."}
```
