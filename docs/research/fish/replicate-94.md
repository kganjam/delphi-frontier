# Replication of claim 94 — S2-D-D: does S2-D's whole-animal L/D band of 3–5 fall?

**Independent re-derivation.** I was shown the question with the answer removed. I derived the
number below from the primary source before looking at any recorded result. I did not open
`docs/research/fish/S2-D-deepen.md` (the S2-D-D working, on branch `claude/deepen-s2-d-imobtp`)
until my own arithmetic was finished; §6 records what I found there and the comparison. I did read
`S2D_calcs.py` from that branch first — that file is S2-D's *model*, the object under test and the
premise of the question, not the S2-D-D answer.

---

## 1. My value

| quantity | my value |
|---|---|
| Measured whole-animal L/D_max of a real gliding fish | **4.37 at α = 0°, Re = 2.0 × 10⁴** (MEASURED, Park & Choi 2010 Table 2, full-text) |
| S2-D's model applied to that same measured animal | **L/D_max = 10.3–17.7, i.e. 2.4–4.1× too high** (COMPUTED) |
| Effective span efficiency the measurement implies | **e_eff ≈ 0.125, bracket 0.125–0.375** at the measured AR 10.7, versus S2-D's assumed 0.7 (COMPUTED, by inverting the polar) |
| **S2-D's zebrafish-scale glider, L/D re-derived with that calibration** | **≈ 2.3 whole-animal (dimensionless), range 2.0–3.1, widening to 3.7 under the most generous apportionment** (COMPUTED) |
| **Verdict on S2-D's band of 3–5** | **FALLS** — the re-derived value sits below the band, touching only its bottom edge in the most generous case |

The headline number for the replication record is the recalibrated whole-animal L/D: **≈ 2.3
(dimensionless), 2.0–3.1 central, 1.96–3.67 full bracket.** Not 3–5.

**Direction of the failure matters, and is easy to misread.** The measured 4.37 *itself* lies inside
3–5. The band does not fall because no animal reaches it. It falls because the model that generated
it over-predicts by 2.4–4.1× on the one animal with a measurement, and because the animal that
*does* achieve 4.37 has an aspect ratio of 10.7 at Re 2 × 10⁴, while S2-D's postulated glider has
AR 4 at Re ≈ 3 × 10³ — three times worse planform and nearly a decade less Reynolds number. S2-D's
band puts the smaller, blunter, slower glider at or above the measured champion.

---

## 2. Inputs, with source and read-level

### Measured (MEAS)

All from **Park, H. & Choi, H. (2010) "Aerodynamic characteristics of flying fish in gliding
flight", J. Exp. Biol. 213:3269–3279, doi:10.1242/jeb.046052.**
**Read-level: full-text** (publisher PDF retrieved and text-extracted locally; Table 1 and Table 2
read as text, not from figure images).

| input | value | where |
|---|---|---|
| Whole-animal L/D_MAX | **4.37**, at α = 0° | Table 2, row "Flying fish (*Cypselurus hiraii*)", model L3 |
| C_D,MIN | **0.055**, at α = −10° | Table 2, same row |
| C_L,MAX | 0.78, at α = 35° | Table 2, same row |
| Reynolds number | **2.0 × 10⁴** (Table 2); 1.9–2.2 × 10⁴ in the text, on mean pectoral chord | Table 2; Methods |
| Aspect ratio, AR = S²/A₁ (pectoral fins only) | **10.7** for L3 (9.0–10.7 across models) | Table 1 |
| Pectoral fin area A₁ | 6377 mm² (L3) | Table 1 |
| Pelvic fin area A₂ | 1837 mm² (L3) | Table 1 |
| Body planform area A₃ | 4474 mm² (L3) | Table 1 |
| Mean pectoral chord c | 24 mm (L3) | Table 1 |
| Standard length | 203 mm (L3); body mass 0.06 kg | Table 1 |
| Reference area for all coefficients | A = A₁ + A₂ + A₃ (fins **and body**) | Results, definition of coefficients |
| Authors' claim (theirs, not my inference) | "the induced drag is one of the dominant drag components of the gliding flying fish (Re ∼ 10⁴)"; L/D is maximum at α = −5 to 0°; gliding performance "comparable to those of bird wings such as the hawk, petrel and wood duck" | Results; Summary |

Two points about 4.37 that matter for the comparison, and are mine, not the authors':

1. **L/D is reference-area independent.** Lift and drag are divided by the same area A, so the ratio
   does not depend on whether A is fins-only or fins-plus-body. Since Park & Choi measured forces on
   a whole stuffed fish (fins *and* body in the flow), 4.37 is a **whole-animal** L/D — directly
   comparable to S2-D's "whole-animal L/D", with no body-drag bookkeeping needed. *My inference.*
2. **Table 2's footnote states that the comparison rows from previous studies "are based on a wing
   only without the body".** So the fish is the only whole-animal entry in that table; the
   hawk/petrel/wood-duck values (3.8, 4.0, 3.8) it is "comparable to" are wing-only and therefore
   flattered relative to it. *Authors' footnote; the implication for the comparison is my inference.*

### S2-D's own model inputs (the premise under test)

From `docs/research/fish/S2D_calcs.py` on `claude/deepen-s2-d-imobtp` (read-level: full-text, source
file; it is a verbatim copy of S2-D's model). Every one of these is tagged ASSUMED or MODEL in that
file itself — none is a measurement:

- Parabolic polar `C_D = C_D0 + C_L²/(π e AR)`; `L/D_max = 1/(2√(C_D0 · k))`, `k = 1/(π e AR)`. MODEL.
- Span efficiency **e = 0.70**. ASSUMED ("typical low-AR value; not retrieved").
- Fin **AR = 4** (span 6 cm, S = 9 cm², two 30 × 15 mm fins). ASSUMED.
- Profile drag **C_D0 = λ × Blasius two-sided** = λ × 2 × 1.328/√Re, with λ ∈ {1.0, 1.4, 2.0}. MODEL
  + inference from Wakeling & Ellington 1997 (that paper's C_D 0.07–0.14 at Re 700–2400 reaches
  S2-D at **abstract** read-level, via S2-D; I did not re-retrieve it).
- Mass 0.4 g, body 32 × 7 × 4 mm ellipsoid, form factor 1.5, median fins 2.0 cm². ASSUMED.
- Operating point solved self-consistently: V from wing loading at C_L*, Re from V. MODEL.

I re-ran S2-D's model unchanged to confirm I reproduce its band before attacking it: at AR 4,
λ = 1.0/1.4/2.0 it gives whole-animal **L/D = 5.48 / 4.79 / 4.10** (COMPUTED). That is S2-D's 3–5
band, so I am testing the right object.

---

## 3. The arithmetic, in full

### 3a. S2-D's model run at the measured animal's geometry (COMPUTED)

`L/D_max = 1/(2√(C_D0 · k))`, `k = 1/(π · 0.7 · 10.7) = 1/23.527 = 0.042504`.

Blasius two-sided at Re = 2.0 × 10⁴: `2 × 1.328/√20000 = 2.656/141.421 = 0.018781`.

| λ | C_D0 | √(C_D0·k) | L/D_max | ÷ measured 4.37 |
|---|---|---|---|---|
| 1.0 | 0.018781 | 0.028253 | **17.70** | 4.05× |
| 1.4 | 0.026293 | 0.033434 | **14.96** | 3.42× |
| 2.0 | 0.037562 | 0.039956 | **12.51** | 2.86× |
| — using the **measured** C_D,min 0.055 in place of Blasius | 0.055 | 0.048366 | **10.34** | 2.37× |

So S2-D's polar over-predicts the only measured gliding fish by **2.4–4.1×**. Even handing the model
the animal's own measured minimum drag coefficient — removing every profile-drag modelling choice —
leaves it 2.4× high. The residual therefore cannot be blamed on λ; it is in the `C_L²/(π e AR)` term.

### 3b. Inverting the polar for the effective efficiency (COMPUTED)

With `C_D0 = 0.055` (measured) and `L/D_max = 4.37` (measured):

```
k = 1/(4 · C_D0 · (L/D)²) = 1/(4 × 0.055 × 19.0969) = 1/4.2013 = 0.23802
e·AR = 1/(π k) = 1/(π × 0.23802) = 1.3373
e     = 1.3373 / 10.7 = 0.1250
```

S2-D assumed **e·AR = 0.7 × 4 = 2.80**. The measured animal, at a geometric AR of 10.7, behaves as
if its **e·AR were 1.34** — less than half S2-D's assumed value, at two and a half times the
geometric aspect ratio. *My inference from the authors' measured numbers; the authors do not fit a
polar or report e.*

**This e is a floor, and I say so explicitly.** The inversion dumps the entire shortfall into the
induced-drag term. In reality C_D,min is measured at α = −10° while L/D_max occurs at α = 0°, so
profile drag at the L/D_max point is ≥ C_D,min and part of the shortfall belongs there. Scanning
that apportionment (§3d) is how I get my uncertainty band.

### 3c. Transferring the calibration to S2-D's glider (COMPUTED)

S2-D's own self-consistent loop (its `ld_max` with its body-drag model, Re from flight speed), AR 4,
e replaced by 0.125:

| λ | e = 0.70 (S2-D) | e = 0.125 (measurement-anchored) |
|---|---|---|
| 1.0 | 5.48 (C_L* 0.80, V 3.01 m/s, Re 3009) | **2.62** (C_L* 0.30, V 4.92 m/s, Re 4922) |
| 1.4 | 4.79 (C_L* 0.92, V 2.81 m/s, Re 2814) | **2.29** (C_L* 0.34, V 4.60 m/s, Re 4603) |
| 2.0 | 4.10 (C_L* 1.07, V 2.60 m/s, Re 2603) | **1.96** (C_L* 0.40, V 4.26 m/s, Re 4258) |

### 3d. Apportionment sensitivity — my uncertainty band (COMPUTED)

Allowing the profile drag at the L/D_max point to exceed the measured C_D,min by a factor m, which
moves shortfall out of the induced term and raises the implied e:

| C_D0 at the L/D_max point | implied e·AR | implied e at AR 10.7 | S2-D's glider at AR 4, λ 1.4 |
|---|---|---|---|
| 0.055 (1.0× C_D,min) | 1.34 | 0.125 | **2.29** |
| 0.083 (1.5×) | 2.01 | 0.187 | **2.72** |
| 0.110 (2.0×) | 2.67 | 0.250 | **3.08** |
| 0.165 (3.0×) | 4.01 | 0.375 | **3.67** |

Taking λ 1.0–2.0 together with m 1.0–2.0 as the defensible core: **L/D ≈ 2.0–3.1, point estimate
2.3.** Stretching m to 3.0 — attributing three times the measured minimum drag to profile losses at
the best-glide point, which I regard as generous — reaches 3.67, the only case that enters the 3–5
band at all, and only its bottom edge.

### 3e. Controls (known-answer checks that ran and passed)

- Round-trip: rebuilding `L/D_max` from the inverted `k` and the measured `C_D0` returns 4.37 to
  within 1 × 10⁻⁹. Passed.
- Must-fail: lowering e never raises L/D (`e` 0.2 vs 0.7 at AR 4). Passed.
- Reproduction: S2-D's model, re-run unchanged, returns its published 5.48/4.79/4.10. Passed.
- Rejected extreme: attributing the *whole* shortfall to profile drag instead (keeping e = 0.7)
  requires C_D0 = 0.308, which is 5.6× the animal's measured C_D,min — unphysical, so the
  induced-drag attribution is the better-supported end. COMPUTED; the rejection is my inference.

Script: `/tmp/claude-0/-workspace-delphi-frontier/30b8730a-d776-59dc-a6f8-0fbac473fe8d/scratchpad/s2d/mine.py`
(session scratchpad, not committed; all of its output is reproduced above).

---

## 4. Disagreement between sources, preserved

- **4.37 (Park & Choi 2010, Table 2, full-text, model L3, whole animal, α = 0°, Re 2.0 × 10⁴)** vs
  **≈ 4.4 (Park & Choi IUTAM 2007 conference version, search-summary: "The maximum lift-to-drag
  ratio is about 4.4 (model 3)")**. These agree, and the 2007 figure is plainly the same measurement
  at lower precision. I use the full-text 4.37.
- **5.9** appears in a search-summary of a 2010 Britannica blog interview with Choi, described there
  as an estimate "for the fins". **Read-level: search-summary; I did not open the page.** It does not
  match Table 2, and Table 2's own swallowtail-butterfly value (3.58) matches the same summary's
  butterfly figure — so the 5.9 is not Table 2's whole-animal number. It is plausibly a fins-only
  figure or a different configuration. I do not average it in; I record it as an unreconciled
  higher value whose provenance I could not verify.
- **4.7** is a CFD maximum L/D from Deng et al. 2019 (*Bioinspir. Biomim.* 15:016005,
  doi:10.1088/1748-3190/ab23e6), **read-level: search-summary** — a *simulation*, not an
  observation, and I could not reach it (§5). It sits 7% above the measurement and would not change
  the verdict.

Note that if the correct measured anchor were as high as 5.9, §3a's over-prediction factor becomes
1.8–3.0× and §3c's recalibrated value rises; the band would still not reach 5, but the margin
narrows. The verdict rests on 4.37 being right, which is now a full-text reading rather than an
inference.

---

## 5. Scope of the negative searches

Hosts that **could-not-access** in this session (DNS does not resolve — outside the session's
allowed network domains, not evidence the material is absent): `typeset.io`,
`pubmed.ncbi.nlm.nih.gov`, `flair.monash.edu` (the IUTAM 2007 Park proceedings PDF),
`iopscience.iop.org` (Deng et al. 2019), `researchgate.net` (not attempted after the pattern was
clear). `journals.biologists.com` resolved, and its article PDF carried Tables 1 and 2 as extractable
text, which is what made this derivation possible.

**Not retrieved, and therefore not used:** Wakeling & Ellington 1997 (reaches me only through S2-D at
abstract level); any measured span efficiency for a low-AR fin at Re 10³–10⁴; any measured
whole-animal L/D for a fish other than *Cypselurus hiraii*. The negative result is specific: **I
found exactly one measured whole-animal lift-to-drag ratio for any fin-winged fish in the accessible
literature, and the search covered the hosts listed above.**

---

## 6. Comparison with the recorded value

Read only after the above was complete. The recorded S2-D-D working
(`docs/research/fish/S2-D-deepen.md`, branch `claude/deepen-s2-d-imobtp`, commit `c584a1e`) records
verdict **falls**, with key number "effective span efficiency e_eff = 0.10–0.18 … resulting
whole-animal L/D at AR 4 = 1.2–2.7".

| | recorded | mine |
|---|---|---|
| Verdict on the 3–5 band | falls | falls |
| Measured flying-fish L/D_max | ≈ 4.4, **search-summary** (states explicitly: "the numeric maximum L/D is not in the text. It sits in Table 2 or Fig. 7, which are images I [could not read]"); also carries 5.9 as relayed | **4.37, full-text** (Table 2 read as text) |
| Model over-prediction factor | ~2–4× | 2.4–4.1× |
| Back-solved e_eff | 0.10–0.18 | 0.125 (0.125–0.375 across apportionment) |
| Recalibrated L/D at AR 4 | 1.2–2.7 | 2.0–3.1 core, 2.3 point, 3.67 outer |

**AGREE** on the verdict and on the mechanism — that S2-D's unvalidated e = 0.7 is where its band
comes from, and that the only measured animal cannot support it. My recalibrated band is somewhat
*less* severe than the recorded one (2.0–3.1 vs 1.2–2.7); both lie below 3, so the direction is the
same and neither reaches S2-D's 4–5.

Two things my pass adds. First, the recorded working flagged its own reversal condition: "If the
Park & Choi Table 2 value turns out to be ≥ ~8, this verdict reverses." **I read Table 2: it is
4.37.** The reversal condition is not met, and the anchor is upgraded from search-summary to
full-text. Second, the 5.9 that the recorded working carried as a live alternative is, on my
reading, not Table 2's whole-animal number — though I could not verify its provenance, so I leave
the disagreement standing rather than discarding it.

Where I would push back on the recorded working: its lower bound of 1.2 comes from the more
aggressive end of the e_eff back-solve, and the inversion that produces a small e_eff is a floor by
construction (§3b) — it charges all unexplained drag to induced losses. Stating the apportionment
scan (§3d) alongside the point value makes the band's bottom edge, 3, a genuine edge case rather
than a clear miss. "Falls" survives that softening; "falls by a factor of three" would not.

---

## Sources

| source | read-level |
|---|---|
| Park & Choi 2010, *J. Exp. Biol.* 213:3269–3279, doi:10.1242/jeb.046052 — Tables 1 and 2, Methods, Results, Summary | **full-text** (publisher PDF, text-extracted) |
| `S2D_calcs.py`, branch `claude/deepen-s2-d-imobtp` — S2-D's model, re-run unchanged | full-text (source file) |
| Park & Choi IUTAM 2007 proceedings, max L/D ≈ 4.4 (model 3) | search-summary (`flair.monash.edu` could-not-access) |
| Choi interview, Britannica blog 2010, "5.9" | search-summary (page not opened) |
| Deng et al. 2019, *Bioinspir. Biomim.*, doi:10.1088/1748-3190/ab23e6, CFD max L/D 4.7 | search-summary (`iopscience.iop.org` could-not-access) |
| Wakeling & Ellington 1997 (λ bracket, C_L cap) | abstract, **via S2-D**; not re-retrieved |
| `S2-D-deepen.md`, branch `claude/deepen-s2-d-imobtp` — the recorded result | full-text, **read only after §1–§5 were final** |

```swarm-replication
{"claim_id": 94, "my_value": "whole-animal L/D ~2.3 (dimensionless; 2.0-3.1 core, 1.96-3.67 full bracket) for S2-D's AR-4 zebrafish-scale glider once span efficiency is anchored on the measured flying fish (L/D_max 4.37 at Re 2.0e4, full-text), versus S2-D's 3-5", "agrees": true,
  "note": "Independently falls: S2-D's polar overpredicts the one measured fin-winged glider by 2.4-4.1x even when handed that animal's own measured CD,min, back-solving to e_eff ~0.125 rather than the assumed 0.7; I also upgraded the flying-fish anchor from search-summary to full-text (Park & Choi 2010 Table 2 = 4.37), which closes the recorded working's stated reversal condition of >=8."}
```
