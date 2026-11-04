# S2-D-D: attacking the weakest input of S2-D (the effective aspect ratio of a fin wing)

**Parent.** S2-D, `docs/research/fish/S2-deepen.md` on branch `claude/deepen-s2-lift-drag-6xxrv3`
(commit `1ddc10bd`), read in full. Its parent is S2, `docs/research/fish/S2-low-reynolds-aero.md` on
`claude/s2-low-reynolds-aero-acdwr7`, also read in full.

The task prompt quoted S2-D's answer as blank. I took the answer from the S2-D file, not from the prompt.

**What S2-D concluded** (its swarm-result, verdict *stands*):
- With Re-matched profile drag, a fin-wing fish gets a **computed whole-animal L/D of about 3–5**:
  - 4.1–5.5 at AR 4;
  - 3.2–4.8 for AR 1.5–4.
- The "6–7 ceiling" is an insect-planform number. A fin wing reaches it only if its effective aspect
  ratio is ≳ 4.
- S2-D named its own weakest input as the **effective aspect ratio e·AR**, which was "still an assumption".

**Everything numerical below is computed** by `S2DD_calcs.py` in this directory
(`python3 -I docs/research/fish/S2DD_calcs.py`). That script imports S2-D's model, `S2D_calcs.py`,
which I copied verbatim from S2-D's branch so that the recompute is like-for-like. I ran no experiment.
No number here is an observation unless a source and read-level sit beside it.

---

## 1. Which input is S2-D's answer most sensitive to? (computed)

S2-D ran its ×0.5/×2 sensitivity on an *uncapped baseline* model. It then reported its answer from a
different, *final* model: Re-coupled CD0 = λ·Blasius with λ = 1.4, and CL capped at 0.9. I re-ran the
sensitivity on that final model. As a control, the script asserts that the baseline reproduces S2-D's
AR-4 value of 4.80, and it does.

| input (×0.5 / ×2) | whole-animal L/D at ×0.5 | at ×2 | swing |
|---|---|---|---|
| **e·AR (effective aspect ratio)** | 3.56 | **6.37** | **1.79** |
| λ (profile drag ÷ Blasius) | **6.22** | 3.50 | 1.78 |
| body drag area | 5.20 | 4.23 | 1.23 |
| mass (wing loading) | 4.38 | 5.29 | 1.21 |
| usable CL cap | 4.36 | 4.79 | 1.10 |

**e·AR and λ are tied** (1.79 vs 1.78). This corrects S2-D on one point. On the final model, **neither
input crosses both edges of the 3–5 band**:
- A ×2 error in e·AR pushes L/D above 5. A ×0.5 error stays inside the band.
- A ×0.5 error in λ pushes L/D above 5. A ×2 error stays inside the band.

S2-D's statement that e·AR is "the only input whose ×2 error crosses both edges" was true only of its
uncapped baseline.

I still pick **e·AR** as the input to attack, for two reasons:
- **λ is bounded from below by physics.** A flat plate cannot have less friction than laminar
  Blasius, so λ ≥ ~1. S2-D also already improved λ to abstract level. (Inference.)
- **e (span efficiency) has never been retrieved in S2 or S2-D.** It was set to 0.7 by assumption.

Both e and λ are really parts of one quantity: the **whole-animal drag polar of a fin wing**. The
cleanest way to improve them is to find a *measured* whole-animal L/D of a real fin wing and check the
model against it. That is what §3 does.

## 2. How well was e·AR established?

| Part | S2-D value | Evidence level | Status |
|---|---|---|---|
| AR (planform) | 4 (two 30 × 15 mm fins) | assumption (design choice) | Labelled as an assumption in S2 and S2-D |
| e (span efficiency) | 0.7 | **assumption** | "typical low-AR value; not retrieved" (S2-D script comment). It was never sourced. |
| The model form itself (parabolic polar, CD = CD0 + CL²/(π e AR)) | — | **assumption** | **Never checked against any measured fin-wing animal** in S2 or S2-D |

Honest grade: **an assumption inside an unvalidated model.** S2-D's only evidence for the model was that it
reproduced S2's own estimate. S2-D said so itself: "consistent with S2, does not validate either".

## 3. Improving it

### 3a. Measured planforms of teleost pectoral fins: improved (full-text)

S2-D found no zebrafish fin AR, and I found none either. Scope of my search:
- Europe PMC: `"pectoral fin" AND "aspect ratio" AND (labrid OR Labridae OR "fin shape") AND OPEN_ACCESS:y`
  returned 22 hits, read as a listing.
- Search-tool controls:
  - positive: `AUTH:"Kesel" AND TITLE:"aerodynamic"` returned 1 hit, the right one;
  - must-fail: `zzqxjv wqpzzk flurbo` returned 0 hits.

I did find **measured AR for the teleost fins that are most wing-like**. These are labrid wrasses, which
flap their pectoral fins to make lift. AR is defined as leading-edge length² ÷ fin area, from calibrated
images.

| Source | Read-level | Authors' numbers |
|---|---|---|
| Fulton, Wainwright, Hoey & Bellwood 2017, *Ecol Evol* 7:589, doi 10.1002/ece3.2624, PMC5214093 | **full-text** (Europe PMC XML) | Table 1: single-fin AR from 0.91 (*Pseudocheilinus hexataenia*) to **2.08** (*Stethojulis bandanensis*). Authors' claim: 2.08 is "the upper extreme … for this family". |
| Fulton, Johansen & Steffensen 2013, *PLoS One* 8:e54033, PMC3541231 | **full-text** | "paddle-shaped (aspect-ratio of 0.86 in *C. fasciatus*) to wing-shaped (2.01 in *S. bandanensis*)". Also *P. octotaenia* 0.76 and *G. varius* 1.75. |
| Park & Choi 2010, *J Exp Biol* 213:3269, doi 10.1242/jeb.046052 | **full-text** (body text via the DOI-resolved journals.biologists.com page; tables and figures are images and could not be read) | Flying-fish (*Cypselurus hiraii*) pectoral fins "have an aspect ratio of 9.0∼10.7". AR is defined in the symbol list as "S²/A1". |

**My inference.** S2's design fin (30 × 15 mm) has a single-fin AR of exactly 2.0 (computed). That puts
it **at the top of the measured labrid range**.
- S2's AR = 4 is two such fins tip-to-tip, with no body gap.
- A fin's leading edge is usually swept, so L²/A overstates span²/area. This makes AR 4 an optimistic
  wing AR for a labrid-shaped fin.
- Flying fish show that teleost fins *can* reach AR ≈ 9–10. **The AR of the planform is therefore not
  the binding constraint. What binds is what a fin wing actually delivers at a given AR**, which
  is the e/model question.

### 3b. The real quantity: a measured whole-animal L/D of a fin wing

Park & Choi 2010 is the **only wind-tunnel measurement of a real fin-derived wing** that I could reach.
I read the article body in full (see the read-level note above). From it:
- Specimens were *C. hiraii* at SL ≈ 200 mm. There were 5 models, with fins spread on preserved fish.
- The free stream was 12 m/s. Re = 1.9–2.2 × 10⁴, "based on the average wing chord length (c) of
  pectoral fin".
- α was swept from −15° to 45° in **5° steps**.
- "The lift-to-drag ratio is largest at α=–5∼0 deg".
- Authors' claim: "the induced drag is one of the dominant drag components of the gliding flying
  fish". The abstract also says "induced drag by strong wing-tip vortices is one of the dominant
  drag components".
- **The numeric maximum L/D is not in the text.** It sits in Table 2 or Fig. 7, which are images I
  could not read.

The number itself comes only through a search summary. The summary quotes the IUTAM 2007 proceedings
version (Park & Choi, "S1_Park.pdf") and a Korean-language conference version: **maximum L/D ≈ 4.4**,
for the model with pectoral and pelvic fins spread. **Read-level: search-summary.** Both host pages
could not be accessed: `eng-web77-v02.ocio.monash.edu` and `koreascience.kr` did not resolve in this
session.

**Disagreement preserved.** S2 relayed flying-fish L/D as "≈ 4.4–5.9" (read-level S). I carry **4.4 and
5.9** through the recompute separately and do not average them.

**Check (computed).** I ran S2-D's own model on the flying fish:
- inputs: chord 25 mm (implied by Re = 2×10⁴ at 12 m/s); AR 9.0 or 10.7; λ 1.0, 1.4 or 2.0; e 0.7 or 0.9;
- body: an assumed 200 × 25 or 200 × 35 mm ellipsoid.

The model predicts **L/D_max = 9.7–16.6**. The measured 4.4 is **0.27–0.45×** the prediction; 5.9
would be 0.36–0.60×. **S2-D's model overpredicts the only measured fin-wing animal by a factor of
about 2–4.**

**What would have to be true for the model to return 4.4 (computed back-solve, AR 9, λ 1.4):**
- (A) all of the gap is induced drag: **e·AR_eff = 0.91**, i.e. e_eff ≈ 0.10 instead of 0.7
  (for 5.9: e_eff ≈ 0.18);
- (B) all of the gap is wing profile drag: CD0_wing = 0.245, which is **9.3×** the model value
  (5.0× for 5.9);
- (C) all of the gap is body drag: the body CdA would be **22×** the model value. That equals a drag
  coefficient of **2.6** on the body's frontal area, or 1.3 for 5.9.
  - A flat plate held normal to the flow is about 1.2 (remembered textbook value, not retrieved).
  - So (C) alone is **not physical for 4.4**, and only marginally physical for 5.9.
  - The frontal area rests on my assumed 25 mm body diameter.
- The authors' own statement points at **(A) or a mix weighted toward it**. That is consistent with my
  back-solve, but the authors give no number for e.

**Limitations of this check. Each one is an inference unless marked otherwise.**
1. The 4.4 is at search-summary read-level.
2. The specimens were preserved fish with fins fixed in place, not a designed wing. This biases the
   measurement *against* fin wings.
3. The 5° α grid can miss the true peak, which also biases it low.
4. Whether strut drag was subtracted is `unknown`.
5. Wind-tunnel blockage correction is `unknown`.
6. The flying fish is at Re 2×10⁴. The zebrafish case is at ~3×10³, where viscous drag is a larger
   share. This biases the transfer *in favour of* the zebrafish case.

Items 2 and 3 bias the measurement low; item 6 biases the transfer high. I cannot say which effect dominates.

### 3c. Higher-quality sources tried and not reached (scope of the negative search)

The data that would settle e without the flying-fish detour is **measured polars of thin low-AR plates
at Re 10³–10⁴**. Here is what I tried:

| Target | Outcome |
|---|---|
| *Disappearance of Vortex Lift in Low-Aspect-Ratio Wings at Very-low Reynolds Numbers*, Trans JSASS 62(6), flat plates AR 0.5–2, Re 10³–10⁴ (the best-matched experiment found) | **could-not-access**: `www.jstage.jst.go.jp` does not resolve in this session. Search-summary only: CL_max falls with Re "due to the disappearance of vortex lift", and falls less at higher AR. **No L/D or e retrieved.** |
| Ananda, Sukumar & Selig 2015, *Aerosp Sci Technol* (flat-plate wings AR 2–6; their Re range was not confirmed from the source) | could-not-access (`m-selig.ae.illinois.edu` blocked) |
| Taira & Colonius 2009, *J Fluid Mech* 623:187 (AR 1–4, Re 300/500, simulation plus oil tow tank) | could-not-access (`authors.library.caltech.edu` blocked). Its Re is also below the fish's. |
| Smith & Taira 2024, arXiv 2408.04801 (sAR 2, NACA 0012, Re 600–10,000) | **full-text** (arXiv HTML). Simulation only. Forces appear **only in graphs; no numeric CL, CD or L/D in the text**. Authors' claim: force sensitivity to Re drops above Re ≈ 2,500. |
| Usherwood & Ellington 2002 (revolving-wing polars, mayfly to quail) | not reached (the DOI resolves to journals.biologists.com, which I did not fetch for this paper) |
| Jensen 1956 (locust L/D 6–7), Wakeling & Ellington 1997 L/D | not re-tried. S2-D recorded them as could-not-access and abstract-without-L/D respectively. |

Hosts that have to be allowed in the session's network settings to go further:
- `www.jstage.jst.go.jp`
- `m-selig.ae.illinois.edu`
- `authors.library.caltech.edu`
- `koreascience.kr`
- `eng-web77-v02.ocio.monash.edu`
- `ntrs.nasa.gov`
- `api.openalex.org`
- `export.arxiv.org`

**What measurement would settle it, and what it costs (inference):**
- **Drop-glide test of a zebrafish-scale fin-wing replica in still air.**
  - Setup: a 0.4 g body with two 30 × 15 mm ray-and-membrane fins, released from ≥ 2 m. S2 computed
    that reaching equilibrium needs 0.2–1.2 m of drop.
  - Record: the equilibrium glide angle γ on a phone camera at 240 fps against a grid. Then
    L/D = 1/tan γ, directly at the right Re, with no e/λ split needed.
  - Cost: hours, under $100.
  - This measures the **whole-animal** quantity S2's answer is about, and it is cheaper than S2-D's
    proposed flume polar.
- Reading Park & Choi Table 2 and the IUTAM table would raise the 4.4 from search-summary to full-text.
  The cost is network access only.

## 4. Recompute (computed)

I applied the flying-fish calibration to S2-D's zebrafish-scale model under each attribution. **Moving the
calibration from Re 2×10⁴ / SL 200 mm to Re ~3×10³ / SL 32 mm is an assumption.**

| attribution | AR 1.5 | AR 2 | AR 4 (S2) | AR 8 |
|---|---|---|---|---|
| S2-D as published (e 0.7, λ 1.4) | 3.15 | 3.56 | **4.80** | 6.37 |
| (A) e_eff from 4.4 | 1.37 | 1.55 | **2.09** | 2.81 |
| (B) wing CD0 × factor, from 4.4 | 0.98 | 1.05 | 1.17 | 1.25 |
| (C) body CdA × factor, from 4.4 (not physical; §3b) | 1.03 | 1.10 | 1.24 | 1.33 |
| (A) e_eff from 5.9 | 1.76 | 1.99 | **2.68** | 3.61 |
| (B) from 5.9 | 1.45 | 1.61 | 1.93 | 2.14 |
| (C) from 5.9 | 1.50 | 1.67 | 2.02 | 2.25 |

A control in the script confirms that every attribution lowers L/D.

**Calibrated whole-animal L/D at S2's AR 4 is 1.2–2.7** (computed). Over AR 1.5–8 it is
**1.0–3.6**. The upper end needs AR 8, which no labrid fin reaches.

**Downstream (computed, S2-D's integrator, 0.5 m drop, 2 m/s launch, S = 9 cm²):**

| L/D | range |
|---|---|
| 4.8 | 23.1 BL |
| 3.0 | 22.0 BL |
| 2.0 | 20.8 BL |
| 1.5 | 19.8 BL |
| wingless ballistic | 16.0 BL |

## 5. Verdict: **FALLS** (on a search-summary anchor, with an assumed transfer)

- **S2-D's headline band, whole-animal L/D ≈ 3–5: falls.**
  - When S2-D's model is checked against the only measured fin-wing animal, it overpredicts by about
    2–4×.
  - Carrying that calibration over puts a zebrafish-scale fin wing at **L/D ≈ 1–3.6, most likely ~2
    at AR 4**.
  - The model now has an e_eff ≈ 0.10–0.18 back-solved from the flying fish, in place of the assumed
    e = 0.7.
  - This conclusion is my inference. It rests on:
    - (i) a measured 4.4 read only at search-summary level;
    - (ii) the assumption that the flying-fish shortfall transfers down a decade of Re.
  - If the Park & Choi Table 2 value turns out to be ≥ ~8, this verdict reverses. The calculated
    model/measured ratio would then be about 0.5–0.8, so it would no longer clearly fall.
- **S2-D's sub-claim (a), that 6–7 is an insect number a fin reaches only at e·AR ≳ 4: strengthens.**
  Flying fish have AR 9–10.7 (full-text) and still measure ≈ 4.4–5.9 at a 7× higher Re. A fin wing
  does not reach 6–7 at AR 4 or at AR 10.
- **S2-D's and S2's claim (c), that L/D barely matters from 0.5 m: strengthens.** Dropping L/D from 4.8
  to 1.5 costs 3.3 body lengths: 23.1 → 19.8 BL, against 16.0 BL with no wing (computed). From that
  height the launch speed does the work, not the wing.
- **Planform AR: improved from assumption to a measured comparator.** S2's AR 4 corresponds to a
  single-fin AR of 2.0, at the measured labrid upper extreme of 2.08 (full-text). The zebrafish's own
  pectoral AR is still `unknown`.

**What remains weakest.**
- The numeric flying-fish L/D (Table 2) is search-summary.
- The split of the shortfall between induced and profile drag is inferred, not measured. The authors'
  text favours induced drag (A).
- The cheapest decisive measurement is the drop-glide test in §3c: hours, under $100.

## Sources

| Source | Read-level |
|---|---|
| S2-deepen.md and S2D_calcs.py (branch `claude/deepen-s2-lift-drag-6xxrv3`) | full-text |
| S2-low-reynolds-aero.md (branch `claude/s2-low-reynolds-aero-acdwr7`) | full-text |
| Park H, Choi H (2010) *J Exp Biol* 213:3269–3279, doi 10.1242/jeb.046052 (DOI-resolved URL https://journals.biologists.com/jeb/article/213/19/3269/9762/) | full-text (body text; tables and figures not readable) |
| Park & Choi IUTAM 2007 proceedings and Korean conference version (max L/D ≈ 4.4) | search-summary (hosts could-not-access) |
| Fulton CJ, Wainwright PC, Hoey AS, Bellwood DR (2017) *Ecol Evol* 7:589, PMC5214093 | full-text |
| Fulton CJ, Johansen JL, Steffensen JF (2013) *PLoS One* 8:e54033, PMC3541231 | full-text |
| Smith L, Taira K (2024) arXiv 2408.04801 | full-text (no numeric forces in the text) |
| Trans JSASS 62(6) "Disappearance of Vortex Lift in Low-Aspect-Ratio Wings at Very-low Reynolds Numbers" | search-summary (could-not-access) |
| Taira & Colonius 2009 JFM 623:187; Ananda, Sukumar & Selig 2015 | search-summary (could-not-access) |
| Europe PMC listings cited in §3a | listing |

```swarm-result
{"subproblem": "S2-D-D", "evidence": "computed: S2-D's own model checked against the only measured fin-wing animal (Park & Choi 2010 flying fish: AR 9.0-10.7 and Re 1.9-2.2e4 at full-text; max L/D ~4.4 at search-summary, 5.9 relayed by S2) plus measured labrid pectoral-fin AR 0.76-2.08 (full-text); transfer of the calibration to Re ~3e3 is an assumption", "answer": "S2-D's model overpredicts the measured flying-fish L/D by about 2-4x, which back-solves to an effective span efficiency of ~0.10-0.18 rather than the assumed 0.7, so a zebrafish-scale fin wing at AR 4 gets a computed whole-animal L/D of about 1.2-2.7 (1.0-3.6 over AR 1.5-8), not 3-5; S2-D's band falls while its 'insect-only 6-7 ceiling' and 'L/D barely matters from 0.5 m' sub-claims strengthen.", "key_number": "effective span efficiency e_eff = 0.10-0.18 (e*AR_eff = 0.91-1.63 at geometric AR 9), back-solved from flying-fish max L/D 4.4-5.9 (search-summary/relayed), replacing assumed e = 0.7; resulting whole-animal L/D at AR 4 = 1.2-2.7 (computed)", "verdict": "falls", "depends_on": ["S2-D: whole-animal L/D 3-5 from parabolic polar with e=0.7, lambda=1.4, CL cap 0.9 (S2D_calcs.py, branch claude/deepen-s2-lift-drag-6xxrv3)", "S2: assumed design geometry, 0.4 g fish, two 30x15 mm fins, S=9 cm^2, AR=4, 32x7x4 mm body", "Park & Choi 2010 J Exp Biol 213:3269: flying-fish max L/D ~4.4 (search-summary; Table 2 not read)", "S2 relayed flying-fish L/D 4.4-5.9 (read-level S)", "Park & Choi 2010: pectoral AR 9.0-10.7 defined S^2/A1 (full-text)", "Park & Choi 2010: Re 1.9-2.2e4 on mean pectoral chord at 12 m/s (full-text)", "Park & Choi 2010 authors' claim: induced drag is a dominant drag component (full-text)", "assumed flying-fish body 200 x 25-35 mm for the model check", "assumption: flying-fish model/measured shortfall transfers from Re 2e4 / SL 200 mm to Re ~3e3 / SL 32 mm", "assumption: preserved-specimen fins and 5-degree alpha grid do not bias the 4.4 by more than ~2x", "Fulton et al. 2017 Ecol Evol PMC5214093: labrid single-fin AR up to 2.08 (full-text)", "Fulton et al. 2013 PLoS One PMC3541231: labrid single-fin AR 0.76-2.01 (full-text)", "Wakeling & Ellington 1997: CD(alpha=0) 0.07-0.14 at Re 700-2,400 -> lambda 1.0-2.0 (abstract, via S2-D)", "Wakeling & Ellington 1997: steady CL,max 1.07 -> usable CL cap 0.9 (abstract, via S2-D; cap margin assumed)", "laminar Blasius flat-plate friction law (textbook model)", "flat plate normal-to-flow CD ~1.2 (remembered textbook value, used only to reject attribution C)", "S2/S2-D point-mass glide integrator, 0.5 m drop, 2 m/s launch"]}
```
