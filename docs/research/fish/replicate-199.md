# Replication 199: [S6] can a zebrafish fin ray carry gliding aerodynamic load?

Status: **independent re-derivation, calculated (not observed, not simulated).**
Script: [`replicate-199_calc.py`](replicate-199_calc.py). Run `python3 -I docs/research/fish/replicate-199_calc.py`.

## 0. What I saw before deriving (disclosure)

The question I was handed was truncated to "[S6] No". To recover it, I opened the inputs branch
`claude/s6-fin-ray-load-kqweu7` and read **only the first 12 lines** of `docs/research/fish/S6-organ.md`.
Those lines contain the title ("can a lepidotrichial fin ray carry aerodynamic load?"), the status line
("negative result (derived)"), and the first paragraph of §1, which gives the original author's fish (4 cm,
0.4 g, W = 3.92 × 10⁻³ N) and states that p = W/S does not depend on speed. **So I knew the sign of the
verdict in advance.** That is a contamination, and I am declaring it. I stopped reading at that point and
did not open `S6_calc.py` or any other part of the file until §4 below. I took my own mass from a separate source.

## 1. Question as I posed it

In a steady glide, lift equals weight, so the mean pressure on the lifting fins is p = W/S. Treat a fin as a
spanwise cantilever strip of span L, with flexural rigidity per unit width e = EI/b, loaded uniformly by p.
Then the tip deflection ratio is

δ/L = p·L³ / (8·e)    (Euler–Bernoulli, uniform load; the strip width cancels)

If δ/L is well above about 0.1, the fin cannot hold a lifting shape. **The 0.1 threshold is my assumption.**

## 2. Inputs

| Input | Value | Source | Read-level | Status |
|---|---|---|---|---|
| Body mass m | 364.8 ± 16.8 mg (adult males; SL 2.8 ± 0.5 cm) | PLoS ONE 2011, Table 1, PMC3116877 (pone.0021059.t001) | **search-summary** (I did not open the table myself) | measured by those authors |
| Whole caudal-fin bending stiffness EI | 1.5–4 × 10⁻⁹ N·m² measured; the authors also estimate "2 × 10⁻⁹ to 5 × 10⁻⁹ N m²" for the whole fin. **I used 2–5 × 10⁻⁹.** | Puri et al., *J. Exp. Biol.* 221:jeb171777 (2018), PMC5868929 | full-text, via a fetch summariser that quoted sentences; supplement **could-not-access** | measured in vivo, anaesthetised |
| Fin width at those positions | ~5–8 mm | Puri et al. 2018 | same | measured |
| Total lifting area S | 0.5, 1, 2 cm² | — | — | **ASSUMED bracket**. I found no zebrafish fin-area source; search scope is §5. |
| Fin span L | 5, 8, 10 mm | — | — | **ASSUMED bracket** |
| Water dynamic pressure for comparison | ½ρU², ρ = 1000 kg/m³, U = 0.1–0.3 m/s | — | — | assumed swimming speeds |

## 3. Arithmetic (calculated)

- W = 0.3648 × 10⁻³ kg × 9.81 m/s² = **3.579 × 10⁻³ N**
- e_low = 2 × 10⁻⁹ / 8 × 10⁻³ = **2.5 × 10⁻⁷ N·m**; e_high = 5 × 10⁻⁹ / 5 × 10⁻³ = **1.0 × 10⁻⁶ N·m**
- p = W/S = 71.6 Pa (S = 0.5 cm²), 35.8 Pa (1 cm²), 17.9 Pa (2 cm²)
- Worked central case: S = 1 cm², L = 8 mm, e = √(2.5e-7 × 1e-6) = 5 × 10⁻⁷ N·m:
  δ/L = 35.8 × (8 × 10⁻³)³ / (8 × 5 × 10⁻⁷) = 35.8 × 5.12 × 10⁻⁷ / 4 × 10⁻⁶ = **4.6**
- Over the full bracket (3 S × 3 L × 2 e = 18 cases), δ/L ranges from **0.28** (S = 2 cm², L = 5 mm, e_high) to **36** (S = 0.5 cm², L = 10 mm, e_low). The full table is the script output.
- Every case exceeds the assumed tolerance of 0.1. The best case misses by 2.8×, the central case by about 46×.
- Values of δ/L above about 0.3 are outside linear theory. They mean "folds", not a literal deflection.

**My value:** δ/L ≈ 5 (calculated; range 0.3–36 over the assumed geometry bracket). The verdict is **No**: at the
in-vivo measured stiffness, a lepidotrichial fin cannot hold its shape under 1 g gliding lift.

**A caveat I found that cuts the other way.** Water dynamic pressure at U = 0.1–0.3 m/s is 5–45 Pa (calculated), which
overlaps the glide pressures of 18–72 Pa. Fins in water are therefore not loaded far below gliding pressure at
burst speeds, and real fins are known to bend a lot in water (Puri et al. call the fin flexible). The answer
therefore turns on the shape-tolerance assumption, not only on the load. My tolerance of 0.1 is an assumption.

**Not established:** strength or failure (I found no fin-ray bone strength or usable ray modulus, so this is **unknown**),
flutter, pectoral-fin stiffness (EI comes from the **caudal** fin), and the effect of active muscle stiffening.

## 4. Comparison with the recorded value (read only after §1–3 were written)

After finishing, I read the rest of `S6-organ.md` on `claude/s6-fin-ray-load-kqweu7`. The recorded answer is
**"No"**. For square wings of 3–15 mm, its §3.3 gives δ/L = 0.92–20 at the measured stiffness, against a tolerance of 0.1, which is a
9–196× rigidity shortfall. It uses m = 0.4 g, D_w = 1.9 × 10⁻⁷ to 8.0 × 10⁻⁷ N·m (from 1.5–4 × 10⁻⁹ N·m²), and ties S to L
(S = 2L²). My D_w is about 25–30 % higher because I used the authors' 2–5 × 10⁻⁹ estimate rather than the
1.5–4 × 10⁻⁹ measured range. My mass is 9 % lower. My geometry is decoupled, so my bracket is wider. At the
nearest matching case (L = 5 mm, S = 0.5 cm²) I get δ/L = 1.1–4.5 and the record gives 1.5–6.5. That is consistent given those
input differences.

**AGREE** on the verdict (No) and on the order of magnitude of δ/L.

**Limits of this agreement:** both derivations rest on the **same single measurement** (Puri et al. 2018,
anaesthetised caudal fin). The beam formula is textbook. So this replication checks the arithmetic and the framing, not
the key input. I also knew the sign of the verdict before deriving (§0).

## 5. Search scope

I ran four web searches in standard mode: fin-ray EI by three-point bending; zebrafish fin-ray bending, modulus and nanoindentation;
adult zebrafish mass and SL; zebrafish pectoral and caudal fin length. I made one full-text fetch (Puri et al., PMC). I found no
zebrafish fin area, no pectoral fin span, and no fin-ray strength. Those values are **unknown** and were bracketed by assumption.

```swarm-replication
{"claim_id": 199, "my_value": "No — tip deflection/span ≈ 5 (calculated; range 0.3–36) vs assumed 0.1 tolerance at in-vivo EI 2–5e-9 N·m²", "agrees": true,
  "note": "Independent beam calculation from Puri 2018 stiffness reproduces the negative verdict and order-of-magnitude deflection, but shares the same single stiffness input and I saw the verdict's sign before deriving."}
```
