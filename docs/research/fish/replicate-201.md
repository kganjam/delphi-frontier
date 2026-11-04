# Replication of claim 201 (S7, pectoral girdle): an independent re-derivation

**Claim under test, as given to me with the answer removed.** At design lift, the root bending moment of a 0.4 g fish is 2×10⁻⁵ to 1.1×10⁻⁴ N·m per fin. That moment needs only a 0.12–0.35 mm solid-equivalent bone section, so bone strength is probably not limiting. The constraint is the mobile fin–scapulocoracoid joint, which must hold a reaction of 9–55× body weight.

## 0. Disclosure: what I saw before deriving

The only place the inputs exist is the harvest file `docs/research/fish/S7-organ.md` on branch `claude/s7-organ-pectoral-girdle-xlxpkt`. **That file is the original author's own working, not just a list of inputs.** I listed its headings and table rows with `grep "^#\|^|"`, and that output also printed the author's computed tables (§3b–3e: wing size, moments, section diameters, muscle forces). So I saw their numbers before computing mine.

- I did **not** read their prose arithmetic (§3 text), §4 "The answer", §5, §6 or the sources list.
- I did **not** open any of the `challenge-201-*`, `deepen-s7-*` or `replicate-s7-*` branches.

Because of that exposure, my agreement on the arithmetic is weaker evidence than a blind check would be. I also wrote my own code (below), including a second load-distribution model that the author did not use.

**This is a replication of the arithmetic, not of the inputs.** The load case (speed, aspect ratio, load factor, C_L) and the material and muscle constants are the author's assumptions. I re-used them, because the claim is conditional on them. I independently re-checked one input (C_L) against a primary source; the result is in §1.

## 1. Inputs

| # | Input | Value | Source | Read-level | Status |
|---|---|---|---|---|---|
| 1 | Body mass | 0.4 g; W = m·g = 3.923 mN (g = 9.80665 m s⁻²) | Project brief, via the harvest file A1 | listing (harvest file) | Given |
| 2 | Maximum lift coefficient | C_L = 0.78 | Harvest A2, citing Park & Choi 2010, *J. Exp. Biol.* 213:3269, doi:10.1242/jeb.046052 | **I read the abstract (Europe PMC).** It says lift is largest at 30–35°. **It does not state 0.78**, so I could not confirm that value. | Unverified by me |
| 2b | Competing C_L (CFD on the same morphology) | 1.03 | *Bioinspir. Biomim.* 2019, doi:10.1088/1748-3190/ab23e6 | abstract (Europe PMC). **Confirmed:** "maximum lift force coefficient of 1.03". | Disagreement kept. 0.78 gives the larger (conservative) moment. |
| 3 | Air density | ρ = 1.204 kg m⁻³ (20 °C); 1.225 (ISA sea level) run as a check | Standard atmosphere | n/a (physical constant) | Mine |
| 4 | Speed | V = 3 or 5 m s⁻¹ | Harvest A3 | listing | **Author's own bracket, not measured** |
| 5 | Aspect ratio (whole span) | 9 | Harvest A4 (flying fish range 9–10.7) | search-summary (the harvest author's read-level) | Assumed |
| 6 | Body half-width | y₀ = 2.5 mm | Harvest A5 | listing | Estimate, not measured |
| 7 | Load factor | n = 1 (steady glide), n = 3 (launch or pull-up) | Harvest A7 | listing | Engineering bracket |
| 8 | Bone yield stress | σ_y = 25–114 MPa (from E = 5–22.7 GPa × 0.5% yield strain) | Harvest A8. The 22.7 GPa is zebrafish **vertebral** nanoindentation (Bohns et al. 2024). | search-summary (per the harvest) | 0.5% strain and 5 GPa are assumed. Teleost bone strength itself is **unknown**. |
| 9 | Muscle isometric stress | 200 kPa | Harvest A9 | listing | Generic, assumed |
| 10 | Adductor moment arm about the articulation | r = 0.5–1.0 mm | Harvest A10 | listing | Guess, not measured |
| 11 | Zebrafish girdle cross-section; adductor PCSA | **unknown** | Harvest §2 records one web search with no hits. **I did not search further.** | n/a | Unknown |

## 2. Arithmetic (all calculated; nothing here is observed)

The script I ran is `s7.py` in the session scratchpad. It uses midpoint-rule integration with N = 2×10⁵.

**Wing size.** The wing is sized for a steady glide at C_L:

- S = 2W / (ρ V² C_L)
- b = √(AR · S)
- fin length s = b/2 − y₀

| V (m/s) | S (cm²) | b (cm) | Fin length s (mm) |
|---|---|---|---|
| 3 | 9.282 | 9.140 | 43.20 |
| 5 | 3.342 | 5.484 | 24.92 |

These use ρ = 1.204. Example for V = 3: S = 2(3.923×10⁻³) / (1.204 × 9 × 0.78) = 9.28×10⁻⁴ m².

**Root moment, Model A (the harvest's idealisation).** Each fin carries nW/2. The lift is elliptic over the fin length, so its centroid sits at ȳ = (4/3π)·s. That gives ȳ = 18.33 mm at 3 m/s and 10.58 mm at 5 m/s.

M = (nW/2)·ȳ

- V = 3, n = 1: (3.923×10⁻³ / 2)(0.01833) = **3.60×10⁻⁵ N·m**
- V = 3, n = 3: **1.08×10⁻⁴**
- V = 5, n = 1: **2.07×10⁻⁵**
- V = 5, n = 3: **6.22×10⁻⁵**

**Root moment, Model B (my own cross-check).** Here the lift is elliptic over the whole span, body included. The fin is the part outboard of y₀, and the moment is taken about y₀:

M = n ∫_{y₀}^{b/2} l(y)(y − y₀) dy, with l(y) = (4W/πb)·√(1 − (2y/b)²)

The body carries some of the lift, so each fin bears only 0.465 W (V = 3) or 0.442 W (V = 5) at n = 1. That makes the moments 7–12% lower:

- 3.33×10⁻⁵ and 9.99×10⁻⁵ at V = 3 (n = 1, 3)
- 1.82×10⁻⁵ and 5.46×10⁻⁵ at V = 5 (n = 1, 3)

**Bone, treated as a solid circular beam.** σ = 32M/(πd³), so d = (32M / πσ_y)^(1/3).

- Largest: M = 1.079×10⁻⁴, σ_y = 25 MPa. 32 × 1.079×10⁻⁴ / (π × 25×10⁶) = 4.40×10⁻¹¹ m³, so **d = 0.353 mm**.
- Smallest: M = 2.07×10⁻⁵, σ_y = 114 MPa. **d = 0.123 mm**.
- Model B gives 0.117–0.344 mm.

**Joint, with the moment held by the adductor.** F = M/r, and PCSA = F / 200 kPa.

| Case (Model A) | r = 0.5 mm | r = 1.0 mm |
|---|---|---|
| V=3, n=1 | 71.9 mN = 18.3 W, 0.36 mm² | 36.0 mN = **9.2 W**, 0.18 mm² |
| V=3, n=3 | 215.8 mN = **55.0 W**, 1.08 mm² | 107.9 mN = 27.5 W, 0.54 mm² |
| V=5, n=1 | 41.5 mN = 10.6 W, 0.21 mm² | 20.7 mN = **5.3 W**, 0.10 mm² |
| V=5, n=3 | 124.5 mN = 31.7 W, 0.62 mm² | 62.2 mN = 15.9 W, 0.31 mm² |

Under Model B the range is 4.6–50.9 W.

**Joint reaction compared with muscle force.** The figures above are the *muscle* force. The articular reaction is the vector sum of the muscle force and the fin's lift (nW/2, at most 1.5 W). Depending on the lever geometry, which is unknown, it is the muscle force ± ≤1.5 W. That inference is mine. The table therefore understates or overstates the true reaction by at most about 1.5 W.

Using ρ = 1.225 instead of 1.204 changes every result by less than 1%.

## 3. My value

All of these are calculated values, conditional on inputs 2–10:

- **Root bending moment per fin:** 2.1×10⁻⁵ to 1.08×10⁻⁴ N·m (Model A). Model B gives 1.8×10⁻⁵ to 1.0×10⁻⁴ N·m.
- **Solid-equivalent bone diameter:** 0.12–0.35 mm.
- **Muscle force at the joint, over the full V × n × r grid:** 5.3–55 W. Model B gives 4.6–51 W, and the articular reaction adds up to about ±1.5 W.

**Uncertainty.** This is dominated by inputs I could not verify, not by the arithmetic:

- r is a guess, and the muscle force scales as 1/r.
- V is the author's own bracket.
- C_L could be 0.78 (unconfirmed by me) or 1.03 (confirmed at abstract level). With 1.03 the span is about 13% shorter, so the moments are about 13% smaller.
- Fish bone strength is **unknown**. σ_y is an assumed 0.5% strain applied to vertebral modulus, and d scales only as σ_y^(−1/3).

## 4. Comparison with the recorded value

I compared against the claim text and the harvest tables I had already seen (§0).

- **Moment, 2×10⁻⁵ to 1.1×10⁻⁴ N·m: AGREE.** Model A reproduces it to 3 significant figures. My Model B is about 10% lower, which does not change the conclusion.
- **Bone section, 0.12–0.35 mm: AGREE.**
- **Joint reaction, 9–55× W: DISAGREE on the lower bound.**
  - The claim's moment range includes the V = 5, n = 1 case (2.1×10⁻⁵ N·m). That same case at r = 1.0 mm gives a muscle force of **5.3 W**, not 9 W.
  - The "9×" is the V = 3, n = 1, r = 1.0 case. So the claim pairs a moment range taken over the whole grid with a reaction range that silently drops its lowest case.
  - The figure is also a muscle force labelled as a joint reaction, though that matters by at most about 1.5 W.
  - The upper bound (55 W) agrees.
- **Qualitative conclusion: AGREE, as my inference.** On these inputs a sub-0.4 mm solid section suffices, which makes the bone an unlikely limit. A muscle force of ≥5–55 W across a sub-millimetre lever is the harder requirement.
- **Still unresolved:** whether a real zebrafish girdle section and adductor PCSA meet these numbers. Both remain **unknown**. I did not search ZFIN or μCT atlases.

**Overall verdict: DISAGREE in one number** (the lower bound of the joint reaction should be about 5× W, not 9× W). The moment, the bone section and the qualitative conclusion all agree.

```swarm-replication
{"claim_id": 201, "my_value": "M = 2.1e-5 to 1.08e-4 N·m per fin; solid bone d = 0.12-0.35 mm; joint muscle force 5.3-55 x body weight (calculated, same assumed inputs)", "agrees": false,
  "note": "Moment and bone-section values reproduce exactly. The 9-55x joint reaction drops the V=5 m/s, n=1, r=1 mm case already included in the moment range, which gives 5.3x, so the lower bound should be ~5x; the qualitative conclusion stands."}
```
