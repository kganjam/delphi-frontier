# Challenge 246 — adversarial review of the S28 lift / ascent-deceleration replication

**Claim under review (246):** "lift/W 10 % at exit, 5 % at apex of a 45-degree leap reproduce, but the
upper 10 % of '5–10 % reduction' treats full lift at 45 degrees as vertical and ignores wing drag; net
vertical reduction ~5–6 % for the designed 196 mm² / 0.25 g / 1.38 m/s wing, 1–3 % for 40–80 mm² fins,
~0 for a vertical leap; conditional on a designed wing, not a measured Daane fin."
Recorded evidence level **derived**, value **5.5 % net vertical reduction**.
Source: branch `claude/replicate-194-rederivation-12i93y`, `replicate-194.md` (read full-text).

**Everything numeric below is a calculation on stated inputs. Nothing here is a measurement.** My own
script: `docs/research/fish/challenge-246-scripts/c246.py`.

---

## 1. Independent arithmetic

I re-derived from the stated inputs only (ρ_air 1.225 kg m⁻³, g 9.81 m s⁻², CL 1.07, CD0 0.08,
AR 5, e 0.8, m 0.25 g, V₀ 1.38 m/s, γ 45°), writing my own script before comparing. L/W = ½ρV²S·CL/(mg);
lift acts normal to the flight path, so its vertical part is L cos γ and the wing-drag vertical part is
−D sin γ.

| S | L/W exit | L/W apex (×cos²45°) | D/W exit | net vertical @ exit | **time-mean over ascent** |
|---|---|---|---|---|---|
| 196 mm² | 9.97 % | 4.99 % | 1.60 % | 5.93 % | **5.24 %** |
| 80 mm² | 4.07 % | 2.04 % | 0.65 % | 2.42 % | 2.14 % |
| 40 mm² | 2.04 % | 1.02 % | 0.33 % | 1.21 % | 1.07 % |

The time-mean column is mine, not the author's: with v_y falling linearly 0.976 → 0 m/s and u held at
0.976 m/s, vertical lift ∝ V and vertical drag ∝ V·v_y, giving mean lift 5.73 % W, mean drag −0.49 % W,
**net 5.24 % W**. Scalings also reproduce: m = 0.40 g → 6.23 % exit / 3.27 % mean; V₀ = 0.45 m/s →
1.06 % exit / 0.56 % mean.

**Result: the author's arithmetic replicates to the digit.** 10.0 % / 5.0 % lift ratios, 1.6 % wing drag,
5.9 % net at exit, 5.0 % at apex. My path-average (5.2 %) lands inside the author's 5–6 % band, which is
a stronger test than the two-point check the author ran — the band is not an artifact of evaluating only
at the endpoints.

Two second-order corrections the author omitted, both small and both in the same direction:

- On a climb, lift is tilted backward (its horizontal part is −L sin γ), so horizontal speed decays over
  the ascent. Integrating that plus drag gives u(apex) ≈ 0.95 u(exit), so **L/W at apex is ~4.7–4.9 %,
  not 5.0 %**. This does not move the 5–6 % band.
- The author quotes a "time-mean of L/W over a vertical deceleration = (L/W)_exit/3". For v_y linear in
  t, mean V² = v₀²/3 — correct, and I confirm it.

## 2. Is a proxy standing in? — yes, one the author fixed, and one they left

The author's whole contribution is catching the proxy in claim 194: L/W used where the quantity that
matters is net vertical force. That catch is right and I confirm the magnitude of the error (10.0 % →
5.9 % at exit).

But the author's own replacement quantity — "reduction in effective downward acceleration during the
ascent" — is itself a proxy for the thing a *deliverable phenotype* needs: a change in leap performance.
Carrying it through on the author's own numbers: g_eff = 0.948 g during the ascent, so apex height
v_y0²/(2g_eff) rises ~5.5 %. For a 3 cm fish whose 45° leap at 1.38 m/s apexes at
0.976²/(2·9.81) ≈ **48.6 mm**, that is **+2.7 mm**. Stating it as "a 5 % reduction in downward
acceleration" and stating it as "+2.7 mm of apex height, for a wing of 2.5× the body's planform area" are
the same calculation and read very differently. The right quantity is the second one. This is my
inference, not the author's claim; the author never converts to a performance delta.

## 3. The hidden assumption that carries the result: the drag polar at Re ≈ 500

The author flags S, V₀ and m as the uncertainty budget, in that order, and labels CD0 0.08 / AR 5 / e 0.8
as "generic choices". That ordering is wrong for the *net* number, because the net is a difference of two
terms and only the drag term is modelled. CD = 0.08 + 1.07²/(π·0.8·5) = 0.171, i.e. **L/D = 6.25**.

Geometry check from the stated inputs: at AR 5, a 196 mm² wing has span 31.3 mm and chord 6.26 mm, so
**Re ≈ 576** at 1.38 m/s (80 mm² → Re ≈ 368). A thin, flexible, ray-supported membrane at Re of a few
hundred is in the regime where profile drag dominates and CD0 0.08 with L/D 6.25 is optimistic; published
low-Re thin-wing and small-insect-wing performance sits nearer L/D 2–4 with CL_max well under 1. I did not
find a measured polar for a spread teleost pectoral fin in air (scope: two web searches, no hit; see §6),
so I treat this as a sensitivity rather than a sourced correction:

| CL | CD0 | L/D | L/W exit | net vert @ exit | path-mean |
|---|---|---|---|---|---|
| 1.07 | 0.08 (author) | 6.25 | 9.97 % | 5.93 % | 5.24 % |
| 1.07 | 0.20 | 3.68 | 9.97 % | 5.13 % | 4.90 % |
| 0.8 | 0.15 | 3.98 | 7.46 % | 3.95 % | 3.71 % |
| 0.6 | 0.20 | 2.62 | 5.59 % | 2.45 % | 2.56 % |
| 0.5 | 0.30 | 1.56 | 4.66 % | 1.19 % | 1.77 % |

Relaxed, the assumption moves the answer from 5.2 % to **1.8–4.9 %**. So the honest band for the designed
wing is **~2–6 %**, not 5–6 %, and the recorded point value 5.5 % is the optimistic corner of it. Note the
direction: relaxing this makes claim 194 *worse*, so it does not rescue the original.

## 4. One sub-claim is wrong in sign: the vertical leap is not "~0"

The claim says "~0 for a vertical leap". Run the author's own model at γ = 90°: lift is perpendicular to
the path, so its vertical component is exactly zero — but wing drag is then **entirely** vertical and
entirely downward. Net = **−1.6 % W** at exit (my calculation, author's inputs, author's drag polar), and
under the relaxed polars of §3 as much as −3 % W.

So for a vertical leap the spread fin does not do nothing; it makes the ascent marginally *worse*. The
author derived the −D sin γ term and then dropped it at the one angle where it is the only term. The
error is small in magnitude but it is a sign error, and it understates the case the author is making
against claim 194.

## 5. Is the evidence level honest?

**Yes, on level; no, on precision.** The source document opens with "Nothing here is a measurement",
labels the mass as assumed and back-solved, labels 40–80 mm² as "my own unsourced guess", records
Miln et al. 2021 as could-not-access, records the ZFIN figure as HTTP 503, and discloses that reading the
challenge-194 commit subject may have primed the vertical-component analysis. That disclosure of priming
is more than the honesty floor requires.

The defect is the recorded **value: 5.5 %**, a single number to two significant figures sitting on top of
(i) a fin area the author says is unknown and which scales the result linearly, (ii) an exit speed from a
paper neither the author nor I could locate, which scales it quadratically, and which is a *swimming
burst* speed being used as a water-exit speed, (iii) an assumed mass, and (iv) an unmodelled-regime drag
polar worth a factor of ~3 (§3). The prose hedges all of this; the recorded scalar does not. Anyone
reading the value field alone gets false precision. That is a defect in the record, not in the author's
reasoning.

I could not independently confirm V₀ = 1.38 m/s. Scope of my negative search: one standard web search for
"Miln 2021 zebrafish burst swimming speed 1.38 m/s"; no result named a 2021 Miln paper or that value.
Nearest hits were unrelated zebrafish burst-and-coast and PIV studies. Read-level: search-summary only.
The input remains unverified by me as well as by the author.

## 6. Regime / taxon / counter-example

I looked for a published case that would break the claim and did not find one that does; the comparative
literature cuts the other way.

- **Taxon.** Zebrafish are not aerial gliders. Fish that get real aerodynamic benefit from pectoral
  "wings" (Exocoetidae — flying fish) operate with wing loading orders of magnitude lower and exit speeds
  ~10–20 m/s, where L/W ≳ 1 rather than ≈ 0.1. A ~5 % effect is exactly what the comparative picture
  predicts for a 0.25 g fish at 1.38 m/s, so the claim is in the right regime.
- **Scale.** 196 mm² of total fin area on an ~18–25 mm SL fish is ~2.5× the body's own planform area.
  That is not a Daane phenotype and, I would add, is a strained design target. The claim already concedes
  "conditional on a designed wing, not a measured Daane fin" — which is the single most important thing in
  it, and it is correct: Daane et al. 2021 report pectoral ray length as plots of length/SL, never area
  (read-level: full-text; the figure values are not in the text, and the ZFIN figure page was
  inaccessible to the author at HTTP 503 — I did not retry it).
- **No counter-example found** that would raise the number back toward 10 %. Scope: the comparative
  reasoning above plus two web searches (low-Re fin/wing polars; Miln 2021). Read-level for the
  flying-fish comparison: background knowledge, not a document I opened in this session — treat it as
  unsourced context, not evidence.

## 7. Verdict

**The claim survives on its central assertion and is weakened on two subsidiary ones.**

Survives: the lift ratios replicate exactly; the proxy diagnosis against claim 194 is correct and the
10 % → 5.9 % correction is right; the path-averaged value (5.2 %, my calculation) confirms the author's
endpoint estimate rather than contradicting it; the conditionality on a designed rather than measured fin
is the right caveat and is stated.

Weakened: (a) "~0 for a vertical leap" is wrong in sign — the author's own model gives **−1.6 % W**,
a small net penalty, because drag becomes the only vertical term; (b) the 5–6 % band and the recorded
5.5 % rest on an unexamined L/D of 6.25 at Re ≈ 500, and the defensible band on a relaxed polar is
**~2–6 %**, with 5.5 % at its optimistic edge.

Neither weakening helps claim 194. Both push the fin's benefit down.

Sources (this challenge): [replicate-194.md, branch `claude/replicate-194-rederivation-12i93y`](https://github.com/kganjam/delphi-frontier/tree/claude/replicate-194-rederivation-12i93y) (full-text);
[Daane et al. 2021, PMC9172250](https://pmc.ncbi.nlm.nih.gov/articles/PMC9172250/) (not re-opened this session; read-level inherited from the author's full-text read, figure values unavailable as text);
Miln et al. 2021 (could-not-access; one web search, no match — see §5, nearest results
[PMC7809443](https://pmc.ncbi.nlm.nih.gov/articles/PMC7809443/figure/Fig2), [PeerJ 4041](https://peerj.com/articles/4041), [WUR edepot 516239](https://edepot.wur.nl/516239), all search-summary and none relevant).

```swarm-challenge
{"claim_id": 246, "outcome": "weakened", "reason": "The lift arithmetic, the proxy diagnosis and the 10%->5.9% vertical correction all replicate independently and a path-averaged 5.2% confirms the band, but 'approximately 0 for a vertical leap' is wrong in sign (-1.6% W, drag is the only vertical term) and the 5-6% band rests on an unexamined L/D of 6.25 at Re~500, which relaxes to ~2-6%.",
  "corrected_value": "~2-6 % net vertical reduction (5.2 % path-mean on the author's own drag polar; 1.8-4.9 % on low-Re polars) for the 196 mm2 / 0.25 g / 1.38 m/s designed wing; -1.6 % W (a small penalty, not ~0) for a vertical leap",
  "depends_on": ["claim 194 inputs: rho_air 1.225 kg/m3, g 9.81 m/s2", "CL 1.07 (project-derived, not re-derived here)", "CD0 0.08, AR 5, e 0.8 wing polar (author's assumption; the main thing my verdict relaxes)", "m = 0.25 g (assumed, back-solved in S28; unverified)", "V0 = 1.38 m/s attributed to Miln et al. 2021 (could-not-access; swimming burst, not water-exit speed)", "S = 196 mm2 designed wing area (project self-consistency value, not a measured Daane fin)", "launch angle 45 deg (assumption)", "Daane et al. 2021 PMC9172250 reports pectoral ray length/SL only, never fin area", "quasi-steady aerodynamics with lift normal to the flight path"]
}
```
