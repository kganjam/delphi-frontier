# Challenge 126: adversarial review of S2-D-D (flying-fish calibration of fin-wing L/D)

**Claim under review** (from `harvest:deepen-s2-d-imobtp`; source file `docs/research/fish/S2-D-deepen.md`
on branch `claude/deepen-s2-d-imobtp`, commit `c584a1e`, read in full along with `S2DD_calcs.py` and
`S2D_calcs.py`):

> S2-D's model overpredicts the measured flying-fish L/D by about 2–4×. Back-solved, that gives an
> effective span efficiency of ~0.10–0.18 instead of the assumed 0.7. A zebrafish-scale fin wing at AR 4
> therefore gets a computed whole-animal L/D of about 1.2–2.7 (1.0–3.6 over AR 1.5–8), not 3–5.
> Recorded evidence level: **measured**.

**Verdict: WEAKENED.** The direction holds: S2-D's model overpredicts the flying fish, and the 3–5 band
does not survive on the 4.4 anchor. Three things in the claim are wrong or fragile:
- the evidence label;
- the lower bound of the L/D range;
- an upper bound that depends on an unexamined transfer rule.

Every number below that I produced is **computed** by `challenge-126_calcs.py` in this directory
(`python3 -I`; it needs the author's `S2DD_calcs.py` and `S2D_calcs.py` beside it). None is an
observation.

---

## 1. Independent arithmetic (computed)

I recomputed the flying-fish check by hand-coded formulas. I did not call the author's `ff_model`.
- Chord from Re: c = 2×10⁴ · 1.5×10⁻⁵ / 12 = **25.0 mm**.
- Wing profile drag: CD0_w = 1.4 · 2 · 1.328/√(2×10⁴) = **0.0263**.
- Body drag (200 × 25 mm body, on wing area): CD = **0.0104**.

| case | model L/D_max | e·AR needed for 4.4 | e_eff | e·AR for 5.9 | e_eff |
|---|---|---|---|---|---|
| AR 9, body Ø25 | 11.6 | 0.91 | 0.101 | 1.63 | 0.181 |
| AR 9, body Ø35 | 11.0 | 1.01 | 0.112 | 1.81 | 0.201 |
| AR 10.7, body Ø25 | 13.0 | 0.86 | 0.081 | 1.55 | 0.145 |
| AR 10.7, body Ø35 | 12.4 | 0.95 | 0.089 | 1.71 | 0.160 |

The author's AR-9 numbers reproduce exactly: e·AR 0.91 / 1.63, e_eff 0.10 / 0.18, and AR-4 L/D 2.09 / 2.68.
Over the author's own geometry bracket, e_eff spans **0.08–0.20**, not 0.10–0.18. This is a minor
widening. **No arithmetic error found.**

## 2. Evidence level is mis-recorded (defect)

The record says **measured**, but the claim contains no measurement:
- e_eff is **back-solved** (computed) from a parabolic polar.
- That polar uses an **assumed** flying-fish body (200 × 25–35 mm, not retrieved).
- The polar is anchored on L/D 4.4, which is **search-summary**. I confirmed this independently: my web
  search returned the same IUTAM 2007 / Korean-proceedings snippet "maximum lift-to-drag ratio is about
  4.4 (model 3)". That is still search-summary, because the hosts `eng-web77-v02.ocio.monash.edu`,
  `koreascience.kr` and `typeset.io` did not resolve in this session.
- The 5.9 figure is relayed from S2 at read-level S.
- The L/D values at AR 4 are a **computed transfer under an assumption**.

The author's own document labels all of this correctly. The record does not. The correct level is
**computed (on a search-summary anchor plus an assumed Re/scale transfer).**

## 3. Proxy: "span efficiency" is a lumped residual, and its value depends on the area convention

I read the Park & Choi 2010 *J Exp Biol* article page at journals.biologists.com. Read-level:
**full-text body via WebFetch summariser**. Tables and figures were not readable, and no numeric L/D
appears in the text. Two facts in it bear on the claim:
- Force coefficients are referenced to "the sum of the planform areas of the pectoral (A1) and pelvic
  (A2) fins and body (A3)".
- AR 9.0–10.7 uses S²/A1, where S is the full pectoral span and A1 is the pectoral area only.

The author's model puts all lifting area on the pectoral fins at AR 9. Pelvic fins and body planform
enter only as drag. My inference: the back-solved "e" is a **residual**. It lumps together induced drag
and everything else the polar leaves out:
- pelvic-fin and body lift;
- CL-dependent profile drag, such as laminar separation at Re 2×10⁴;
- fin–body interference.

Its numerical value depends on which area the AR is referenced to. The quantity that does not depend on
that convention is **e·AR_eff ≈ 0.9–1.8**, not e_eff. The claim's KEY number presents e_eff as a span
efficiency. It should be stated as a model-residual efficiency.

## 4. The lower bound 1.2 rests on an internally inconsistent attribution (computed)

The claim's AR-4 range "1.2–2.7" takes its floor from attribution (B), which puts all of the gap into
wing profile drag. Body drag (C) gives 1.24. In the flying-fish check, (B) is evaluated with **no CL cap**.
- Under (B), the model's L/D maximum sits at CL* = **2.25** for the 4.4 anchor and **1.68** for 5.9
  (computed).
- That exceeds the 0.9 cap S2-D itself imposes.
- It also conflicts with the authors' full-text statement that L/D peaks at α = −5 to 0°, which implies
  a low CL. CL at those angles is `unknown`: it was not readable.
- Under (A), the optimum falls at CL* = 0.32–0.48, which *is* consistent with a near-zero-α peak. This
  is my inference, and it supports the author's choice of (A).

If (B) is redone under the same CL ≤ 0.9 cap, the profile-drag factor is 5.8× for 4.4 and 3.9× for 5.9.
The zebrafish L/D at AR 4 becomes **1.72 and 2.33** (computed), not 1.17. With (C) already rejected as
unphysical, the floor of the AR-4 range is **~1.7, not 1.2**.

## 5. Hidden assumption: *how* the shortfall transfers to AR 4 (computed, relaxed)

The author's transfer applies the same multiplicative e (0.10 or 0.18) to the AR-4 zebrafish wing. That
gives e·AR = 0.40–0.72, below a circular disc at ideal loading (π/4·4/π ≈ 1.27). Whether the flying-fish
loss scales with AR or is a roughly fixed configuration loss is **not known**. I relaxed it:

| transfer rule (attribution A) | AR 4 L/D from 4.4 | from 5.9 |
|---|---|---|
| author: same e_eff, AR 9 reference | 2.08 | 2.68 |
| same e_eff, AR 10.7 reference | 1.93 | 2.49 |
| e referenced to total planform (pelvic + body add 30–100 % of A1, assumed range) | 2.16–2.60 | 2.77–3.34 |
| fixed absolute e·AR_eff (loss independent of geometric AR) | 2.95 | **3.79** |
| measured/model ratio 0.27–0.60 applied directly to S2-D's 4.80 | 1.30–2.16 | 1.73–2.88 |

Results:
- **On the 4.4 anchor**, every rule I tried stays below 3, giving 1.3–2.95 (the 1.3 is from the crude
  ratio rule). The claim's "not 3–5" holds there.
- **On the relayed 5.9 anchor**, two of the rules reach **3.0–3.8**, which overlaps S2-D's 3–5 band.
- The claim's upper bound of 2.7 is the author's single transfer rule, not a bound.

## 6. Counter-examples and regimes (scope stated)

- **Ground effect.** Park & Choi report a drag reduction of up to 14 % near a water surface (full-text,
  via summariser). It applies to near-surface glides only and does not change the free-stream calibration.
- **Insects.** Wakeling & Ellington 1997 (dragonfly gliding, Re 700–2,400) is the obvious taxon
  counter-example for fin-scale Re.
  - I found the abstract and listings only.
  - No glide L/D was retrieved; it is `unknown`.
  - Scope: one standard web search for "Wakeling Ellington 1997 dragonfly gliding glide angle lift drag
    ratio".
  - Park & Choi themselves say the flying-fish L/D "is better than that of flying insect wings" (at
    lower Re). That is mild support for the claim's "6–7 is insect-only" sub-claim being at least not
    contradicted by the flying-fish source. But it compares against insect *wings*, so it does not
    settle the claim.
- **Other teleost gliders.** I found no other measured fin-wing L/D. Scope: the two web searches above,
  plus the author's own searches, which I did not repeat.

## 7. What survives

- The model overpredicts by ×0.27–0.60 (recomputed).
- On the 4.4 anchor the 3–5 band falls under every transfer rule I tried.
- The direction of the downstream sub-claim ("L/D barely matters from 0.5 m") is untouched; I did not
  re-run the integrator.

## 8. Corrected statement

S2-D's polar overpredicts the flying-fish max L/D by ~2–4× (computed, on a search-summary 4.4 / relayed
5.9). The back-solved model-residual e·AR_eff is ~0.9–1.8 (e_eff 0.08–0.20, depending on the area
convention). Transferred to S2's AR-4 fin wing, the computed whole-animal L/D is:
- **~1.7–3.0 on the 4.4 anchor**, with the 1.3 crude-ratio floor noted;
- **~2.3–3.8 on the 5.9 anchor**.

The band falls only if 4.4 is the right anchor and the loss scales with AR. Evidence level: **computed**,
not measured.

## Sources

| Source | Read-level |
|---|---|
| S2-D-deepen.md, S2DD_calcs.py and S2D_calcs.py, branch `claude/deepen-s2-d-imobtp` | full-text |
| Park H & Choi H 2010 *J Exp Biol* 213:3269, doi 10.1242/jeb.046052, journals.biologists.com article page | full-text body via WebFetch summariser; tables and figures not readable; no numeric L/D in the text |
| Park & Choi IUTAM 2007 / Korean proceedings ("max L/D about 4.4, model 3") | search-summary (hosts could-not-access) |
| Wakeling & Ellington 1997 *J Exp Biol* 200:543 | search-summary (no L/D retrieved) |

```swarm-challenge
{"claim_id": 126, "outcome": "weakened", "reason": "Arithmetic reproduces and the 3-5 band does fall on the 4.4 anchor, but the record mislabels a back-solved, search-summary-anchored computation as measured, the 1.2 floor comes from an uncapped profile-drag attribution needing CL*~2.25 (1.7 when capped as S2-D does), and relaxing the e-transfer rule raises the AR-4 value to 3.0-3.8 on the 5.9 anchor.", "corrected_value": "whole-animal L/D at AR 4 ~1.7-3.0 (4.4 anchor) or ~2.3-3.8 (5.9 anchor), computed; model-residual e*AR_eff 0.9-1.8 (e_eff 0.08-0.20)", "depends_on": ["Park & Choi IUTAM 2007 / Korean proceedings: flying-fish max L/D ~4.4 (search-summary)", "S2 relayed flying-fish L/D 5.9 (read-level S)", "Park & Choi 2010 JEB: pectoral AR 9.0-10.7 = S^2/A1, Re 1.9-2.2e4 at 12 m/s, coefficients referenced to A1+A2+A3, L/D peak at alpha -5 to 0 deg (full-text body via summariser)", "S2-D model S2D_calcs.py / S2DD_calcs.py: parabolic polar, lambda 1.4 Blasius, CL cap 0.9, zebrafish geometry AR 4, 0.4 g (branch claude/deepen-s2-d-imobtp)", "assumed flying-fish body 200 x 25-35 mm (author's assumption, reused)", "assumption: pelvic+body planform adds 30-100% of pectoral area (my bracket, not retrieved)", "assumption: flying-fish shortfall transfers from Re 2e4 to Re ~3e3 (author's, reused)"]}
```
