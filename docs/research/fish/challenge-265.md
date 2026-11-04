# Challenge 265: adversarial review of S13-D-D (hemiray tissue modulus)

**Claim under review:** S13-D-D (`harvest:s13-d-sensitive-input-6wvjgv`). The claim says the
feasibility negative strengthens. The required pure-protein modulus becomes 1.0–5.2 TPa, which is
34–172× above 30 GPa. The fin is soft because its hemitrichs are uncoupled, not because its bone is
soft. The coupling route has a ~12× lever and leaves a 20–54× gap.

**Recorded evidence level:** derived. **Date:** 2026-11-04.

**Read:**
- `docs/research/fish/S13-D-deepen.md` and `S13-D-D-deepen_calc.py` on branch
  `claude/s13-d-sensitive-input-6wvjgv` (`full-text`, repo).
- I did **not** re-open Bohns et al. 2020 myself. I take their E_r values as the author reported
  them (read-level for me: `could-not-access`, not attempted; relayed via the author's `full-text`
  read).

Everything below marked "calculated by me" is a calculation, not an observation.

## 1. Arithmetic, redone independently

These are my calculations from the stated inputs: m = 0.4 g, semi-span 2 cm, uniform load,
10% tip deflection, Puri EI 1.5–4×10⁻⁹ N·m², E_r 4.57–8.68 GPa, ν = 0.3.

| Quantity | Mine | Author |
|---|---|---|
| EI_req | 9.81×10⁻⁷ N·m² | same |
| EI gap | 245–654× | same |
| E = (1−ν²)E_r | 4.16–7.90 GPa | 4.2–7.9 |
| Required E | 1.02–5.17 TPa | 1.0–5.2 |
| Margin over 30 GPa | 34–172× | same |
| Per-ray structural I (16–18 rays) | 1.06–6.0×10⁻²⁰ m⁴ | same |
| Gap after 12× | 20.4–54.5× | 20–54 |

**The arithmetic is correct.** The ceiling-leg result (34–172×) survives on its stated inputs.

## 2. Defect A: the 20–54× residual prices the coupling lever alone

The author treats two levers separately:
- **Material stiffening:** capped by the 30 GPa ceiling.
- **Hemitrich coupling:** a measured ~12×.

They do not stack them. Flexural rigidity is EI = E·I, so the two levers multiply. Raising the
tissue from 4.2–7.9 GPa to the 30 GPa protein ceiling is itself a 3.8–7.2× lever (calculated by me).
That lever is available to the pure-protein route the claim is pricing. Combined with 12× coupling,
the stacked lever is **46–87×** (calculated by me).

Residual gap of the stacked route, calculated by me (S13 model; the tolerance is S13's assumption):

| Tip-deflection tolerance | EI gap | Residual after stacked lever |
|---|---|---|
| 10% (S13 default) | 245–654× | **2.8–14×** |
| 20% | 123–327× | 1.4–7.2× |
| 30% | 82–218× | 0.94–4.8× (best corner closes) |
| 80% (S13-D lenient) | 31–82× | 0.35–1.8× |

So the protein route the claim says "does not rescue" is short by **2.8–14×, not 20–54×**, at the
default tolerance. Its best corner closes at a 30% tolerance. That is inside the 5–80% range that
S13-D itself tested.

The negative still holds at S13's default inputs. But it now rests on a margin of ~3–14×, against
inputs (tolerance, mass, span) that S13-D says each carry 2–3× uncertainty. The word "strengthens"
fits the pure-material ceiling leg only. It does not fit the claim's statement about the best
protein route.

Two caveats push in opposite directions, and I keep both:
- **Against stacking.** The 12× is a sunfish clamping upper bound (search-summary). Whether a
  30 GPa protein can also form the coupling tissue is `unknown`.
- **Against the claim.** The geometric coupling ceiling is 245–2360× (author's calculation). The
  12× is a measurement of one clamping experiment, not a proven biological maximum.

## 3. Defect B: "nearly uncoupled, not soft bone" is not identified by the data

The author's own number puts the per-ray structural I **1.4–8× below** the fully uncoupled-plate
bound (8.4×10⁻²⁰ m⁴). A perfectly uncoupled ray of 4–8 GPa tissue would therefore still be stiffer
than measured. Some other compliance must make up the 1.4–8× difference. The candidates are:

- segment-joint compliance (the author names this)
- ray taper and branching: Puri's EI is a whole-fin fit, while D = 150 µm and t = 15 µm describe
  one location, and plate I ∝ t³
- an effective tissue modulus lower than the nanoindentation value

On the third candidate, my inference, not measured: 100 nm Berkovich indents on unpolished
cryosections of unstated hydration can overstate the bulk wet modulus. A 1.4–8× overstatement
would explain the deficit with no appeal to coupling at all. The data cannot tell "uncoupled" from
"joints" from "softer tissue than indented". The causal sentence should be downgraded to: the data
are *consistent with* low coupling plus some unidentified compliance.

This does not touch the ceiling leg. If the effective tissue E is lower, required E falls, but the
flip threshold (46–122 MPa) is still ~35× below.

## 4. Proxy and evidence level

- **Proxy.** Using the tissue modulus as E_base is the right quantity for a fixed-architecture
  material swap, and the author argues this correctly. One residual proxy remains: nanoindentation
  E_r stands in for the bulk axial modulus. The authors' SDs are 57–100%, and n = 1 fin per group.
  The author flags this.
- **Evidence level.** `derived` is honest. The E_r is measured by cited authors; everything
  downstream is calculated, and the claim labels it that way. The 12× is correctly tagged
  search-summary. No defect here.

## 5. Counter-examples and regimes not covered

- **Challenge-181's 4 cm span** quadruples EI_req, which makes the stacked residual 11–57×. That
  would restore a robust negative. The two spans disagree, and I preserve the disagreement rather
  than choose one.
- I ran no new literature search, so I offer no new taxon counter-example. Negative-search scope:
  none performed by me.

## Verdict: WEAKENED

- The arithmetic and the ceiling leg (34–172×) survive.
- The claim's statement that the coupling route leaves a 20–54× gap omits the multiplicative
  stacking of material stiffening (to the 30 GPa ceiling) with coupling. Stacked, the residual is
  2.8–14× at a 10% tolerance (calculated by me), and its best corner closes at 30%.
- The causal claim "soft because uncoupled, not because bone is soft" is not identified, because
  the measured EI lies below even the uncoupled bound.

```swarm-challenge
{"claim_id": 265, "outcome": "weakened", "reason": "Arithmetic and the 34-172x ceiling margin reproduce, but the 20-54x residual omits multiplicative stacking of the 3.8-7.2x material lever (tissue to 30 GPa ceiling) with the 12x coupling lever, which leaves only 2.8-14x at 10% tolerance (closing at ~30%), and the 'uncoupled not soft bone' cause is unidentified because measured EI lies 1.4-8x below even the uncoupled bound.",
  "corrected_value": "best protein route (material to 30 GPa x 12x coupling) residual gap 2.8-14x at 10% tip tolerance (calculated), not 20-54x",
  "depends_on": [
    "S13 feasibility model: cantilever UDL, m=0.4 g, semi-span 2 cm, tip deflection 10% (assumed, S13-protein.md)",
    "Puri et al. 2018 whole caudal fin EI 1.5-4e-9 N m^2, 16-18 rays (full-text via S13)",
    "Bohns et al. 2020 hemiray reduced modulus 4.57-8.68 GPa (author's full-text read; not re-read by me)",
    "Poisson ratio 0.3 (assumed)",
    "protein-solid modulus ceiling 30 GPa (search-summary via S13)",
    "sunfish hemitrich clamping ~12x (search-summary)",
    "challenge-175 uncoupled flat-plate I 8.44e-20 m^4 at D=150 um t=15 um (calc by sibling)",
    "S13-D tolerance range 5-80% (calc, S13-deepen.md)"
  ]}
```
