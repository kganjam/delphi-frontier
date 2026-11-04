# Challenge 197 — adversarial review of S13 (protein fin-ray stiffness)

**Claim under review (not mine):** "[S13] No: closing the ~245-654x flexural-rigidity
gap to a 0.4 g glider would need a ray modulus of 10^1-10^2 GPa against a measured
~10-30 GPa ceiling for the stiffest protein solids, and since hydrated collagen
fibrils are already softer than the triple helix the tissue is architecture-limited
rather than molecule-limited, so a stiffer protein variant is insufficient …
KEY: EI_req 9.8e-7 N m^2 vs measured 1.5-4e-9 N m^2 (245-654x gap)."
Recorded level: `derived`. Source: branch `claude/s13-protein-fin-ray-e8y8d8`,
`docs/research/fish/S13-protein.md` (read-level: full-text, the harvest file itself).

**Verdict: WEAKENED.** The EI gap is arithmetically right. The headline modulus is a
proxy error. Read against the claim's own measured `I_eff`, the 245–654× gap needs an
effective ray modulus of **1.4–3.3 GPa** (my computation). That is below the
claim's 10–30 GPa "ceiling", not above it. The conclusion that a stiffer protein
variant will not fix this still stands, but for a different reason from the one the
claim gives. The reason that holds is architecture, and the claim's own data
support it more strongly than the claim's own argument does.

## Sources and read-levels

| Source | Read-level | Used for |
|---|---|---|
| S13-protein.md + s13_arith.py (harvest branch) | full-text | all inputs below |
| Puri et al. 2018 *J Exp Biol* 221: jeb171777 (EI, I_eff, ray d, ray count) | **could-not-access directly** by me; I use the S13 author's transcription (author states full-text) | EI_meas, I_eff |
| Teleost ray moduli 0.11–3.7 GPa, protein-solid moduli table | search-summary (the author's level); I did not re-fetch | author's baselines only |

I ran no literature search of my own. Any statement that I "found no X" covers
only the S13 file and the arithmetic below.

## 1. Arithmetic, redone independently (`challenge_197_arith.py`)

W = 0.4e-3 × 9.81 = 3.92 mN. UDL on a half-span: w = 1.96e-3 / 0.02 = 0.0981 N/m.
Cantilever tip deflection δ = w L⁴ / 8EI, with δ = 2 mm → **EI_req = 9.81e-7 N m²**.
Dividing by 4e-9 gives **245×**, and dividing by 1.5e-9 gives **654×**. **Confirmed (computed).**

## 2. The proxy: the gap is multiplied onto the wrong modulus

The claim gets "10^1–10^2 GPa" by taking an *isolated-material* modulus as the
baseline and multiplying it by the gap: a teleost ray at ~1 GPa or a hydrated
fibril at 0.3 GPa (both search-summary, neither from zebrafish), times 245–654.
That step assumes the measured zebrafish EI equals (those material moduli) × (the
ray geometry). The claim's own measured numbers say otherwise:

- Puri et al. (as transcribed) report that interray tissue does not contribute to
  EI, so EI comes from the rays. They give I_eff = 3–7 × 10⁻¹⁶ m⁴.
- An independent check: 16–18 solid rays of d = 0.15 mm give I = 4.0–4.5 × 10⁻¹⁶
  m⁴ (computed), which matches I_eff.
- Effective ray modulus is therefore EI_meas / I_eff = **~2–13 MPa** (computed; the
  author gets the same number in §3.4). The author then discards it as "a plate
  modulus, not the ray material's modulus".
- If the rays acted as continuous solids at the ~1 GPa the claim uses as its
  baseline, EI would be ~4 × 10⁻⁷ N m² at d = 0.15 mm (computed). That is only
  **2.2–2.5× short** of EI_req, not 245–654× short. At d = 0.2 mm it would be above
  EI_req.

So the in-vivo zebrafish ray bends **~100–500× more easily** than its own geometry
plus a GPa-class material would allow (my inference, from computed numbers). The
likely cause is segmentation, hemiray sliding or low mineralisation, but which one
is `unknown`, because I did not test it. Most of the 245–654× gap lives in that
structural discount, not in the molecule. Applying the full gap a second time to a
GPa material modulus counts the discount twice.

**The right quantity** is the effective modulus the ray section must reach at the
measured I_eff: E_req = EI_req / I_eff = 9.81e-7 / (7e-16 … 3e-16) =
**1.4–3.3 GPa (computed)**. That is:
- below the claim's 10–30 GPa ceiling;
- inside the range of the claim's own table for silk (1–10 GPa) and dry collagen fibril (2–7 GPa);
- below the bone moduli (4–20 GPa) that fin models assume (search-summary).

**Consequence:** the claim's mechanism sentence ("would need 10^1–10^2 GPa … above
the ceiling") is refuted as stated. Its policy sentence ("a stiffer protein variant
is insufficient; the tissue is architecture-limited") survives. The fixed-I
analysis shows that materials which already exist would suffice *if* the ray
behaved as a continuous section. A stiffer collagen cannot be relied on to raise a
joint- or sliding-limited effective modulus. Whether it would do so in part is
`unknown`: no measurement links molecular modulus to segmented-ray EI.

## 3. Hidden assumption relaxed: the 10% tip-deflection criterion

δ = 10% of the semi-span was chosen, not measured. Relaxing it (computed):

| δ / semi-span | gap vs 4e-9 | gap vs 1.5e-9 |
|---|---|---|
| 10% | 245× | 654× |
| 20% | 123× | 327× |
| 30% | 82× | 218× |
| 50% | 49× | 131× |

Even on the claim's own route there is a crack. At the distal-ray baseline of
0.11 GPa, the 245× case needs 27 GPa, which sits *inside* the 10–30 GPa band and
not above it. At δ = 20% with the 0.24 GPa proximal minimum, the high-EI case needs
~29 GPa. "Above the ceiling" therefore does not hold for every baseline the
author cites.

## 4. Evidence-level and wording defects

- **"Measured ~10–30 GPa ceiling"**: the S13 table's 18–30 GPa amyloid figure is
  labelled *modelling*. The only AFM amyloid value listed is 3.3 ± 0.4 GPa. Part of
  the "measured" ceiling is computed. That is a level defect even though the
  conclusion does not depend on it.
- **"Hydrated fibrils already softer than the triple helix"**: by the author's own
  table, fibrils are 0.2–0.8 GPa and the helix is 0.35–25 GPa. The ranges overlap at
  the low end, and the helix range spans two orders of magnitude across methods. The
  ordering is method-dependent rather than established. The architecture argument
  in §2 above does not need it.
- **"10^1–10^2 GPa"**: on the author's own baselines the figures are 74–196 GPa
  (fibril) and 328–876 GPa (proximal ray mean 1.34 GPa), so even within the
  author's own logic the range is better written as 10^1–10^3.
- The overall `derived` label is honest. The design run is honestly reported as not
  executed.

## 5. Counter-examples and regimes

I did not search for a natural glider (e.g. Exocoetidae) at sub-gram mass. Scope:
no search was performed, so this is `unknown`. The arithmetic in §2 is enough on its
own to move the claim, without a taxon counter-example.

## Corrected statement

With the measured I_eff held fixed, the 245–654× EI gap corresponds to a required
effective ray modulus of ~1.4–3.3 GPa (computed). Existing protein and
mineralised-collagen solids already reach that. The zebrafish ray falls short
because its effective in-vivo modulus is only ~2–13 MPa (computed from measured EI
and I_eff). That points to architecture (segmentation, hemiray coupling or
mineralisation) as the limiter, so a stiffer protein variant alone is not a
justified route. It is not shown to be impossible on modulus-ceiling grounds.

```swarm-challenge
{"claim_id": 197, "outcome": "weakened", "reason": "The 245-654x EI gap is correct, but dividing EI_req by the measured I_eff gives a required effective ray modulus of only 1.4-3.3 GPa, within existing protein/bone moduli, so the '10^1-10^2 GPa above the ceiling' mechanism is a proxy error; the architecture-limited conclusion survives on different grounds.", "corrected_value": "required effective ray modulus 1.4-3.3 GPa at measured I_eff 3-7e-16 m^4 (computed); measured in-vivo effective ray modulus ~2-13 MPa (computed)", "depends_on": ["Puri et al. 2018 EI 1.5-4e-9 N m^2 (via S13 transcription)", "Puri et al. 2018 I_eff 3-7e-16 m^4 (via S13 transcription)", "Puri et al. 2018 finding that interray tissue does not contribute to EI", "ray diameter 0.1-0.2 mm and 16-18 rays per fin (via S13 transcription)", "S13 load model: 0.4 g, 2 cm semi-span cantilever, uniform load, 10% tip deflection", "S13 protein-solid modulus table (search-summary)"]}
```
