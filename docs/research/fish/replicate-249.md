# Replication 249: independent re-derivation of bluegill pectoral fin-ray flexural stiffness (EI)

**Claim being replicated (answer withheld from me):** S25-D ("deepen") says the S25 conclusion falls. S25 had concluded that the 565 × 10⁻⁶ N m² value is the one to trust, over a relayed 3.8 × 10⁻⁶ N m².

**Branch the inputs live on:** `claude/deepen-flammang-fin-ray-stiffness-vvpk2v` (`docs/research/fish/S25-deepen.md`).

## Disclosure: what I saw before deriving

When I listed the deepen branch with `git show --stat`, its **commit message** was printed. It contains the recorded result: Alben et al. 2007's 1.98 N/m, a calculated clamped EI of 5.4e-6 to 4.3e-5 N m², and "13-105x below the 565e-6 abstract value". I did not choose to see this, and it came before my own arithmetic. So this replication is **not fully blind**. It tells me which primary source they used, and roughly what number they got.

I did **not** open `S25-deepen.md` or `S25_deepen_calc.py`. A repository-wide grep for "Flammang" started listing other agents' fin-ray write-ups (`challenge-128/134/135/159`, `S26-organ`). I stopped it and read none of them.

## Sources and read-levels

| # | Source | Read-level | What I took from it |
|---|---|---|---|
| S1 | Flammang BE, Alben S, Madden PGA, Lauder GV (2013) *Functional morphology of the fin rays of teleost fishes.* J Morphol 274:1044–1059. doi:10.1002/jmor.20161, PMID 23720195 | **abstract** (Europe PMC REST API). Full text: **could-not-access**. The Harvard lab PDF (sites.harvard.edu) and Deep Blue (deepblue.lib.umich.edu) are both blocked by this session's network policy. Not open access on Europe PMC. | Authors' claim: "Flexural stiffness of the fin ray was calculated to be 565 × 10⁻⁶ Nm²". Also: 67 ± 2.3 mN impact force; maximum curvature 9.38 mm⁻¹ under vortex impact; curvature ≤0.029 mm⁻¹ (proximal) and ≤0.065 mm⁻¹ (distal) in normal swimming. **How** they calculated the 565e-6 is unknown, because the methods are not in the abstract. |
| S2 | Alben S, Madden PG, Lauder GV (2007) *The mechanics of active fin-shape control in ray-finned fishes.* J R Soc Interface 4:243–256. doi:10.1098/rsif.2006.0181, PMC2359861 | **full-text** (PMC HTML) | Bluegill (*Lepomis macrochirus*) pectoral rays; maximum ray length 40.3 ± 0.8 mm (mean ± s.e., n = 6 fish); 24 rays tested. Three-point bending gave a "composite" E ≈ 10⁸–10⁹ N m⁻², with average I ≈ 10⁻⁶ cm⁴, so "the measured B = EI ≈ 10⁻⁶–10⁻⁵ J m" (authors' own statement). A scaling estimate gives B ≈ 10⁻⁶. In the cantilever test, a point force is applied about 2/3 of the way along the ray and the force is "measured as a function of tip deflection". The slope is 1.98 N m⁻¹ with both hemitrich bases clamped, which is "about 12 times the value when one hemitrich is free". |
| S3 | Lauder et al. SPIE conference report 2007 | **search-summary** only | "Fin rays … elastic modulus of about 1 GPa." This is consistent with the top of S2's E range. I did not use it numerically. |
| S4 | Wrasse pectoral fin-ray study, JEB 221 jeb163360 (Aiello et al. 2018, per the URL) | **search-summary** only | The search summary says fin-ray EI spans 0.0001–1.5 µN m² (1e-10 to 1.5e-6 N m²) across two wrasse species. That is a different taxon; I list it for order of magnitude only and did not verify it. |
| — | The "3.8 × 10⁻⁶ N m²" relay | **unknown** | I could not identify which secondary source relays this number. One web search for secondary citations of the Flammang EI found nothing that gives 3.8e-6. |

## Derivation (all values below are **calculated** from S2's measurements, not observed)

### Route A: Alben's direct E × I (the authors' own product)
- E = 1e8 to 1e9 Pa (measured, S2)
- I = 1e-6 cm⁴ = 1e-6 × (1e-2 m)⁴ = 1e-14 m⁴ (measured average, S2)
- EI = 1e8 × 1e-14 = **1.0e-6 N m²** up to 1e9 × 1e-14 = **1.0e-5 N m²**
- This matches S2's stated "B = EI ≈ 10⁻⁶–10⁻⁵".

### Route B: back-calculation from the cantilever slope (my inference)
I treat the ray as a uniform Euler–Bernoulli cantilever: clamped at the base, length L, point load F at a = 2L/3.
- Deflection at the load point: δ_a = F a³ / (3EI), so EI = k a³ / 3
- Deflection at the tip (S2 says deflection was measured at the tip): δ_tip = F a² (3L − a) / (6EI), so EI = k · (28/27) L³ / 6 = 0.1728 · k L³

Inputs: k = 1.98 N/m (both bases clamped, S2). k = 1.98/12 = 0.165 N/m (one base free; "about 12×", S2). L = 40.3 mm, the fish-mean *maximum* ray length (S2). The tested ray's own length is **unknown**, so I also ran L = 30 mm as a lower bracket.

| L (mm) | k (N/m) | EI, load-point δ (N m²) | EI, tip δ (N m²) |
|---|---|---|---|
| 40.3 | 1.98 (clamped) | 1.28e-5 | 2.24e-5 |
| 40.3 | 0.165 (one free) | 1.07e-6 | 1.87e-6 |
| 30 | 1.98 | 5.28e-6 | 9.24e-6 |
| 30 | 0.165 | 4.4e-7 | 7.7e-7 |

Arithmetic for the central case (L = 40.3 mm, tip deflection):
- L³ = 6.545e-5 m³
- 0.1728 × 1.98 × 6.545e-5 = **2.24e-5 N m²**

Caveats (my inference):
- The clamped-base slope includes the hemitrich shear-coupling stiffening that S2 models. It is an *effective* whole-ray EI, not the bony material EI. The one-free-base value is closer to the bending-only resistance.
- A tapered ray and a load point that is only approximately at 2/3 make this an order-of-magnitude check, not a measurement.

### Route C: can the 565e-6 be reproduced from Flammang's own abstract numbers?
No. EI = M/κ with M = F·l. With F = 0.067 N and κ = 9.38 mm⁻¹ = 9380 m⁻¹, EI = 5.65e-4 would need a lever arm l = EI·κ/F ≈ 79 m. That is physically impossible. The 9.38 mm⁻¹ figure is local buckling, so linear beam theory does not apply to it. The method behind 565e-6 therefore remains **unknown** without the full text.

## Result

**My value:** whole-ray EI of a bluegill pectoral fin ray ≈ **1e-6 to 2e-5 N m²**. This is calculated. Its two anchors:
- Alben's direct E·I: 1e-6 to 1e-5.
- Back-calculation from the clamped cantilever: 1.3e-5 to 2.2e-5 at L = 40 mm, down to about 5e-6 at L = 30 mm.

I put the uncertainty at about ±1 order of magnitude, because E itself is only bracketed to a factor of 10.

**Against 565 × 10⁻⁶ N m²:**
- 565e-6 / 2.2e-5 ≈ 26×
- 565e-6 / 1e-5 ≈ 57×
- 565e-6 / 1e-6 ≈ 565×

So the abstract value of Flammang et al. 2013 (the authors' claim) sits 26–565× **above** every EI I can derive from the same lab's earlier full-text measurements on the same species and fin. The 3.8e-6 relay (source unknown) falls **inside** my range.

**Inference:** the S25 conclusion that 565e-6 is the value to trust is not supported by the independent primary data. On the evidence I could access, it falls.

Disagreement I keep open:
- I cannot rule out that Flammang et al. measured something different, such as a different ray, the unsegmented proximal region, or a different load case. I cannot read their methods.
- Their number could also be correct, with Alben's E range being low. The two primary sources disagree by more than an order of magnitude, and I have not averaged them.

Negative-search scope:
- Flammang 2013 full text: tried Harvard lab PDF (blocked), Deep Blue (blocked), Europe PMC (abstract only, not OA).
- The 3.8e-6 relay: one standard web search, no source found.

## Comparison with the recorded value
These figures come from the deepen commit message only; I did not open the file.
- The recorded calculation is clamped EI of 5.4e-6 to 4.3e-5 N m², from the same 1.98 N/m, and 13–105× below 565e-6. The conclusion is that S25 falls.
- My Route B clamped range (5.3e-6 to 2.4e-5) shares their lower end. Their upper end (4.3e-5) is about 2× higher than mine; the reason is unknown, possibly different L or load-geometry assumptions, and I did not check.
- My Route A (1e-6 to 1e-5) uses the E·I statement directly, which their commit message does not mention.
- Both derivations put 565e-6 well over an order of magnitude too high.

**AGREE on the conclusion** (565e-6 is not the value to trust). There is minor disagreement on the upper bound of the range. Agreement is weakened because the recorded result and its source were visible to me before I derived.

```swarm-replication
{"claim_id": 249, "my_value": "EI ≈ 1e-6 to 2e-5 N m^2 (calculated from Alben et al. 2007 full text: E·I and 1.98 N/m cantilever), 26-565x below 565e-6", "agrees": true,
  "note": "Independent primary data (Alben 2007 full text) puts bluegill pectoral ray EI at 1e-6 to 2e-5 N m^2, so the S25 conclusion trusting 565e-6 falls; not fully blind because the deepen commit message exposed the recorded range before derivation."}
```
