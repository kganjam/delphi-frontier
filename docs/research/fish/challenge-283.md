# Challenge 283 — wing area vs dorsal silhouette (S15-dna.md §3.1–3.2)

**Claim under review (verbatim):** "Required wing area at a 2 m/s launch with an
assumed CL 0.8 is ~20 cm2, against a ~1.4 cm2 whole-body dorsal silhouette: a
~14x shortfall, falling to ~0.6x only if launch speed reaches 10 m/s."
Recorded evidence level: *derived*. Recorded value: *14 fold area shortfall*.
Source: `docs/research/fish/S15-dna.md` §3.1–3.2 (commit `acdef434`), read in full.

**Verdict: WEAKENED.** The arithmetic survives exactly. What does not survive is
the word *shortfall*: the 14× is a ratio against a proxy denominator (the body's
own dorsal outline), not against any lifting surface the animal has or could
have, and the speed variable is labelled "launch speed" when the equation needs
glide airspeed. Everything below that carries a number is **calculation**
(script: `challenge-283.py`) unless it says otherwise.

## 1. Independent arithmetic (calculation)

Inputs as stated by the author: m = 4.0×10⁻⁴ kg, g = 9.81 m s⁻², ρ = 1.225 kg m⁻³,
C_L = 0.8, lift = weight; silhouette = 4 cm × 0.5 cm × 0.7.

- W = 3.924 mN. S = 2W/(ρV²C_L).
- V = 2 m s⁻¹: S = 20.02 cm². Silhouette = 1.40 cm². Ratio = **14.3×** — reproduces.
- V = 10 m s⁻¹: S = 0.80 cm². Ratio = **0.57×** — reproduces ("~0.6×").
- The 1 and 5 m s⁻¹ rows of the source table (80.1, 3.20 cm²) also reproduce.

No arithmetic defect found.

One phrasing defect: "falling to ~0.6x **only if** launch speed reaches 10 m/s"
invites reading 10 m s⁻¹ as the threshold. Parity with the silhouette (ratio 1.0)
is reached at **7.56 m s⁻¹** (calculation, C_L 0.8). The sentence is literally
true about 0.6× but overstates the speed needed to stop being "larger than the
animal".

## 2. Proxy check — this is where the claim weakens

**Proxy:** whole-body dorsal silhouette, standing in for *the lifting area
available*. The recorded value calls the ratio a "shortfall", i.e. a deficit of
supply against demand. But the silhouette is not the supply:

- A glider's wings are not bounded by its body outline. The author's own §3.3
  sizes a candidate wing at span 8 cm (2 × body length), chord 2.5 cm → 20 cm²;
  i.e. the author's own geometry meets the 2 m s⁻¹ requirement with fins that
  project beyond the body. So "larger than the entire animal viewed from above"
  is a statement about wing proportions, not an impossibility.
- The quantity that matters is **required area ÷ achievable pectoral-fin
  planform area** (or, equivalently, required fold-growth of the pectoral fin).
  Its denominator — adult zebrafish pectoral fin area — is **unknown**; the
  author says so explicitly in S15 §2.6 and §3.2 ("I cannot convert either
  figure into 'how many fold must the pectoral fin grow'"). The source text is
  therefore more careful than the claim record; the defect is in the
  "14 fold area *shortfall*" label.
- I also tried to anchor the right comparison with a real glider's
  wing-to-body planform ratio: Fish (1990) Exocoetidae wing loading / aspect
  ratio is **could-not-access** for me as well (not retried beyond the author's
  report; no alternative numeric source found in one standard web search).
  So the correct ratio remains `unknown`.

Correct statement (my inference): *required area at 2 m s⁻¹, C_L 0.8 ≈ 20 cm²
≈ 14× the dorsal body outline; fold-growth required of the pectoral fins is
unknown.*

## 3. Hidden assumptions, relaxed (calculation)

| Relaxation | S at 2 m s⁻¹ | ratio to 1.4 cm² |
|---|---|---|
| As stated, C_L 0.8 | 20.0 cm² | 14.3× |
| C_L 1.2 | 13.4 cm² | 9.5× |
| C_L 1.5 (optimistic cambered membrane; no source) | 10.7 cm² | 7.6× |
| C_L 0.5 (pessimistic) | 32.0 cm² | 22.9× |
| Glide angle at L/D = 2 (L = W cos θ) | 17.9 cm² | 12.8× |

C_L and glide angle move the ratio by < 2×; neither rescues it. **The result is
carried by V** (S ∝ V⁻²), which the author already flags as the binding
uncertainty. Two problems with V:

1. **V is glide airspeed, not launch speed.** For a glide that is "sustained",
   S = 2W/(ρV²C_L) holds at the equilibrium glide speed, which the animal's
   wing loading sets; a fish leaving the water at 2 m s⁻¹ with smaller wings
   does not glide at 2 m s⁻¹, it fails to glide. The table is a valid
   *wing-loading ↔ glide-speed* map, but labelling the column "launch speed"
   conflates a take-off condition with a cruise condition.
2. **Where real flying fish sit on that map.** Makiguchi et al. 2013 (*Aquatic
   Biology* 18:105–111; read-level **abstract/search-summary**) report
   accelerometer-estimated **leap** speeds of 3.9–5.2 m s⁻¹ in *Cypselurus
   heterurus doederleini* — a measurement, by them. A secondary review PDF
   (read-level **search-summary**, not verified against Hertel 1966 / Fish 1990
   / Davenport) gives **maximum flight** speeds of ~10–20 m s⁻¹. These two
   sources disagree in kind (leap vs airborne max) and I do not reconcile them.
   At the measured leap range, the required area is 5.3–3.0 cm² = **3.8–2.1×**
   the silhouette (calculation, C_L 0.8); at the reported flight range it is
   below the silhouette.

Opposite direction: 2 m s⁻¹ is 50 body lengths s⁻¹ for a 4 cm fish. I searched
(one standard web search, "adult zebrafish maximum escape velocity m/s
fast-start") for a measured adult zebrafish burst speed and found **none**
(result: `unknown`). If zebrafish cannot reach 2 m s⁻¹, the 14× is optimistic,
not pessimistic — the 1 m s⁻¹ row gives 57×.

## 4. Evidence level

*derived* is **honest**: S15 labels §3 "computation, not observation" and flags
C_L and body width as assumptions. No defect on level. The defect is the value
label ("shortfall"), §2.

## 5. Regimes / counter-examples

- Ground effect (S15 itself cites up to 14 % drag reduction, search-summary):
  lift augmentation near the water is of order tens of percent at most in my
  inference — not enough to move a 14× ratio. No numeric source obtained.
- Freshwater hatchetfishes (Gasteropelecidae) are the obvious small-fish
  counter-example to check; I did not search them in this session (scope:
  none), so I make no claim about them.
- No published counter-example found that breaks the arithmetic; the scope of
  my search was the two standard web searches named above.

## Summary

Arithmetic: survives (20.0 cm², 14.3×, 0.57×). Proxy: the "14-fold shortfall"
is a ratio to the body outline, not a deficit of available lifting area; the
fold-growth that matters is unknown. Speed: the variable is glide airspeed;
silhouette parity is at 7.56 m s⁻¹, and at measured flying-fish leap speeds
(3.9–5.2 m s⁻¹, abstract-level) the ratio is 2–4×.

```swarm-challenge
{"claim_id": 283, "outcome": "weakened", "reason": "Arithmetic reproduces exactly (20.0 cm2, 14.3x, 0.57x), but the 14x is a ratio to a proxy (the body's dorsal outline), not a shortfall of available lifting area, and V is glide airspeed mislabelled as launch speed; silhouette parity is at 7.6 m/s, not 10.", "corrected_value": "required area 20 cm2 = 14x dorsal body outline at V=2 m/s, CL=0.8 (calculation); required pectoral-fin fold-growth unknown; ratio 2.1-3.8x at measured flying-fish leap speeds 3.9-5.2 m/s; parity at 7.56 m/s", "depends_on": ["m = 0.4 g (project premise)", "C_L = 0.8 (assumed, unsourced)", "dorsal silhouette 4 cm x 0.5 cm x 0.7 (author assumption)", "rho = 1.225 kg/m3", "Makiguchi et al. 2013 leap speed 3.9-5.2 m/s (abstract-level)", "adult zebrafish pectoral fin area (unknown)", "adult zebrafish burst speed (unknown)"]}
```
