# S28-D: deepening S28 by attacking its weakest input

**Parent.** S28, `docs/research/fish/S28-organism.md`, commit e8ba4191 (branch `origin/claude/s28-organism-design-5z0vjz`). It is not on this branch; I read it with `git show`.

**Earlier reviews of S28 that I read in full** (repository, full-text):
- challenges 189, 190, 191, 192 (commit 85f2fb5c), 193, 194;
- S20-D-D-D, `S20-D-D-deepen.md` @ 17c6d933.

**Arithmetic.** `docs/research/fish/S28-deepen_calc.py`, run from the repository root (about 20 s).

**Status.** Every number here that has no source next to it is a **calculation** from that script. No number is an observation. I made no new measurement. Date: 2026-11-04.

**S28's recorded answer.** NEGATIVE. The best design buildable from alleles with a demonstrated phenotype is the existing Daane `lat4a^nr21/+ ; kcnh2a^lof/+` double heterozygote. It cannot fly, glide or skim, and it cannot meaningfully extend its leap. "The honest phenotype is a possibly detectable 5–10 % reduction in ascent deceleration."

**Challenge 194 already corrected the size of that phenotype.** The 5–10 % was the lift-to-weight ratio, not a reduction in deceleration. Integrated over the ascent, the effect is at most **≈ 4.5–4.9 %** (calculation; case C fin, 1.38 m/s exit, 45° launch). I take that corrected figure as the starting point.

---

## 1. Which input is the answer most sensitive to? (recomputed)

The answer has two parts. The negative is the four "cannot" clauses. The positive is the "honest phenotype". I set each input to ×0.5 and ×2, keeping everything else at S28's case C:
- 1.38 m/s exit, 45° launch;
- S = 192 mm², span 31 mm, AR 5;
- m = 0.25 g, CL 1.07, CD0 0.08.

Script section 1. All values are calculations.

| Input | L/W at exit | Ascent-decel reduction | Range gain at 45° | V_to (m/s) | Flight speed deficit |
|---|---|---|---|---|---|
| baseline (S28 case C) | 9.8 % | **4.87 %** | 2.1 % | 4.41 | ×3.20 |
| exit speed V ×0.5 / ×2 | 2.4 / 39 % | **1.27 / 16.3 %** | 0.6 / 4.3 % | 4.41 | ×6.4 / **×1.60** |
| **pectoral fin length ×0.5 / ×2** (area follows, AR-5 rule) | 3.1 / 34 % | **1.61 / 14.8 %** | 0.7 / 4.5 % | 7.82 / 2.36 | ×5.7 / ×1.71 |
| fin area S ×0.5 / ×2 (span held) | 4.9 / 19.5 % | 2.56 / 8.66 % | 1.3 / 2.1 % | 6.24 / 3.12 | ×4.5 / ×2.26 |
| body mass m ×0.5 / ×2 | 19.5 / 4.9 % | 9.21 / 2.50 % | 3.5 / 1.1 % | 3.12 / 6.24 | ×2.26 / ×4.5 |
| CL ×0.5 / ×2 | 4.9 / 19.5 % | 2.45 / 8.92 % | 1.0 / 2.7 % | 6.24 / 3.12 | ×4.5 / ×2.26 |
| launch angle 60° / 80° (not a ×2) | 9.8 % | 2.62 / 0.27 % | −2.3 / −14 % | 4.41 | ×3.20 |

What the table shows (my reading of the calculations):

1. **No single ×2 change flips the negative.**
   - The smallest flight deficit in the table is ×1.60 (exit speed doubled).
   - The largest range gain at a matched 45° launch is 4.5 %.
   - So "cannot fly, glide, skim or meaningfully extend its leap" is not sensitive to any one input at ×2.
2. **The phenotype clause is what moves.** Two inputs enter it quadratically and dominate:
   - **exit speed**, because lift ∝ V²;
   - **pectoral fin length**, because under S28's geometry span = 2·L_fin + body width and S = span²/AR, so S grows roughly as L_fin².
   - At ×0.5 either input takes the effect from ~5 % to ~1.3–1.6 %. At ×2 either takes it to ~15–16 %.
   - Mass, area at fixed span, and CL enter only linearly.
3. **Choosing between the two quadratic inputs.** The deciding question is which one could actually be wrong by ×2.
   - **Exit speed.** It already has a conspecific in-water measurement. Demesmay et al. 2025 report an adult escape peak of 1.57 ± 0.27 m/s. S28's 1.38 m/s sits 0.7 SD below that mean, within ×1.14. Halving or doubling it would need the fish to be 3.3–4.4 SD from the measured mean, which is implausible.
   - **Fin length.** S28's value of **0.45 SL per fin** has no measurement under it at all (§2). A factor of two either way is not excluded by anything in the record.
   - **So the weakest high-leverage input is pectoral fin length per fin, as a fraction of SL**, and with it the fin area that S28 derived from it.

## 2. How well is 0.45 SL per fin established?

**Evidence level: assumption. It is not measured, and it is not even a proxy.**

**S28's own words** (§2.2): "**EXTRAPOLATION.** 13.5 mm = 0.45 SL per fin. … I assume it to match the project's 1-BL span, and I have not taken it from the measured allele." S28 §1 adds: "I did not read the numeric values of Fig. 4B."

**How the number travels** (my reading of the chain):
- Daane et al. write "phenocopies flying-fish fin proportions". That is a qualitative statement.
- The project had a 1-BL span design target.
- S28 back-fitted 0.45 SL per fin so that the two would agree.
- That fin length, at an imposed AR 5, then gives S = 192 mm² (case C), the headline geometry.
- Challenges 190, 191 and 194 carried 192 mm² forward as "the unmeasured case-C area". They flagged it as unmeasured but never re-examined the fin length behind it.
- This is an assumption repeated until it reads as an input.

**What the primary source actually says.** I read Daane JM et al. 2021, *Curr Biol* 31:5052–5061.e8, doi:10.1016/j.cub.2021.08.054, PMC9172250. **Read-level: full-text** (NCBI efetch PMC XML, fetched this session). Author claims, verbatim:
- Fig. 4A legend: "As in flying fishes, the nr21/lof trans-heterozygotes exhibit elongated paired fins and a hypocercal caudal fin."
- Fig. 4B/C legend: "Pectoral fin length (B) and caudal fin length (C) suppression of overgrowth in medial fin by lat4a mutation. In (B) and (C), length normalized by SL."
- Results: "the lat4a nr21/+; kcnh2a lof/+ fish show wild-type-sized medial fins, while the paired fins are overgrown"; the interaction is "sufficient to phenocopy this key innovation and organismal bauplan of flying fishes".
- **The text contains no numeric pectoral-fin-length/SL value, no fin area, and no fin span.** Challenge 189 reached the same conclusion independently: "values do not appear in the text".

**My inference.** "Phenocopy the bauplan" is a statement about pattern: paired fins overgrown, median fins wild type, caudal fin hypocercal. It is not a statement that the zebrafish pectoral reaches any particular length/SL ratio. Reading it as 0.45 SL is S28's extrapolation, not the authors' claim.

## 3. Trying to improve it

### 3.1 Access record (this session)

| Target | Result | Read-level |
|---|---|---|
| Daane 2021 text (PMC XML via eutils efetch) | Read and searched. No fin-length numbers in text, legends or methods | **full-text** |
| Daane 2021 Fig. 4B image, `cdn.ncbi.nlm.nih.gov` (nihms-1735542-f0004.jpg) | Proxy refused the connection: host not allowed for this session | could-not-access |
| Same image via `europepmc.org/articles/…/bin/`, `pmc.ncbi.nlm.nih.gov/…/bin/` | 403 / 404 | could-not-access |
| Europe PMC fullTextXML for PMC9172250 | HTTP 500 | could-not-access |
| Cell Press figure / supplement host `ars.els-cdn.com` | Proxy refused the connection | could-not-access |
| ZFIN mirror of the figure (`zfin.org/ZDB-FIG-221222-34/35`, `ZDB-IMAGE-221222-34`), found by web search | WebFetch: HTTP 503. curl: TLS issuer verification failed with the session CA bundle (verification not disabled). `crick.zfin.org` does not resolve | could-not-access |
| Plaut 2000, *J Exp Biol* 203:813 (wild-type vs long-finned zebrafish) | Abstract only (paywall). It gives U_crit and says fin dimensions differ, **but gives no pectoral dimensions** | abstract |
| Gdf5 zebrafish fins preprint, bioRxiv 10.1101/2021.01.31.428959 (first 100k of 127k characters) | No adult wild-type pectoral-fin length reported | full-text (partial) |
| Web search, "zebrafish adult pectoral fin length relative to standard length ratio wild type measurement" (extended) | No published adult pectoral-length/SL ratio surfaced | search-summary |
| Web search, "Daane 2021 lat4a kcnh2a trans-heterozygote pectoral fin length normalized standard length…" | Only the figure legend (ZFIN) and the paper | search-summary |

**Negative finding, with its scope.** I found **no numeric value** for pectoral fin length/SL in either the Daane double heterozygote or adult wild-type zebrafish. Scope: two web searches, the Daane full text, the Plaut 2000 abstract, part of one bioRxiv preprint, and challenge 189's earlier searches. The one place the number is known to exist is the plotted data of Daane Fig. 4B, and I could not reach it. **The improved input is therefore `unknown`.** I do not replace S28's 0.45 with a guess.

### 3.2 What I can improve: the decision threshold

Since the value cannot be read, I computed what it would have to be for S28's phenotype to exist. This is the quantity that settles the question. Script sections 2–3; all calculations, 45° launch, generous AR-5 rule (rule C).

**Fin length per fin needed for a given mean ascent-deceleration reduction:**

| Body (SL, m) | Exit speed | ≥ 2 % needs | ≥ 5 % needs |
|---|---|---|---|
| 3.0 cm, 0.25 g (S28) | 1.38 m/s (Miln max) | **0.26 SL** | **0.46 SL** |
| 3.0 cm, 0.25 g | 1.57 m/s (Demesmay mean) | 0.22 SL | 0.39 SL |
| 3.6 cm, 0.43 g | 1.38 m/s | 0.29 SL | 0.51 SL |
| 3.6 cm, 0.43 g | 1.57 m/s | 0.25 SL | 0.44 SL |

Inputs and labels for that table:
- **SL 3.6 cm** is my calculation from Plaut 2000's abstract: 56.0 cm s⁻¹ ÷ 15.5 SL s⁻¹ = 3.61 cm for wild type, and 43.7 ÷ 12.5 = 3.50 cm for long-finned fish.
- **0.43 g** is S28's assumed 0.25 g scaled isometrically to that length. It is an inference, not a measured mass.
- With S ∝ SL² and m ∝ SL³, a larger fish has a lower lift/weight ratio.

**Full grid (calculation): effect vs fin length × exit speed, SL 3.0 cm / 0.25 g, rule C.** Each cell gives the reduction in ascent deceleration, then the apex rise in mm at a matched 45° launch.

| L_fin / SL | S (mm²) | 0.95 m/s | 1.38 m/s | 1.57 m/s | 2.11 m/s |
|---|---|---|---|---|---|
| 0.15 | 34 | 0.4 %, 0.1 | 0.9 %, 0.5 | 1.2 %, 0.8 | 2.1 %, 2.5 |
| 0.20 | 51 | 0.6 %, 0.2 | 1.4 %, 0.7 | 1.7 %, 1.2 | 3.1 %, 3.8 |
| 0.25 | 72 | 0.9 %, 0.2 | 1.9 %, 1.0 | 2.4 %, 1.6 | 4.3 %, 5.3 |
| 0.30 | 97 | 1.2 %, 0.3 | 2.5 %, 1.3 | 3.2 %, 2.2 | 5.7 %, 7.2 |
| 0.35 | 125 | 1.6 %, 0.4 | 3.2 %, 1.7 | 4.1 %, 2.8 | 7.2 %, 9.3 |
| **0.45 (S28)** | 192 | 2.4 %, 0.6 | **4.9 %, 2.6** | 6.2 %, 4.4 | 10.6 %, 14.4 |

The exit-speed columns are labelled as follows:
- **0.95** is the noise-robust floor from Demesmay's 3.8 cm in 40 ms;
- **1.38** is S28's Miln value;
- **1.57** and **2.11** are the Demesmay mean and mean + 2 SD.
- All of these are in-water escape peaks used as stand-ins for exit speed. Their read-levels are in §6.
- Under the length-only rule (rule A: chord fixed at 0.1 SL), every cell is smaller. The best case is 3.5 % at 0.45 SL and 2.11 m/s.
- The script also prints the 3.6 cm / 0.43 g grid, which is about 15–20 % lower throughout.

**Reading of the grid (my inference):**
- S28's "≈5 %" phenotype is not a central estimate. It is the corner where a fin-length assumption of 0.45 SL per fin meets the fastest fish of one dataset.
- If Fig. 4B shows a pectoral fin of **≤ 0.25 SL**, the effect is **≤ 2.4 %** across the in-species central speeds (1.38–1.57 m/s). That corresponds to an apex rise of ≤ 1.6 mm on a ~5 cm apex.
- A pectoral fin of ≥ 0.4 SL per fin is needed before 5 % appears at central speeds.

### 3.3 Is even the small effect "possibly detectable"? (calculation with assumed camera parameters)

S28 asserted detectability. Challenge 194 noted that it was never computed. Script section 5 gives a tracking-noise floor for one leap's fitted vertical acceleration. The model is a least-squares quadratic over a 100 ms ascent, with var(c₂) ≈ 180σ²/(N·T⁴).

| Camera (assumed) | σ_a per leap |
|---|---|
| 240 fps, 0.5 mm position noise | 2.8 % of g |
| 1000 fps, 0.5 mm | 1.4 % of g |
| 1000 fps, 0.2 mm | 0.55 % of g |

**My inference.**
- With a ≥ 1000 fps camera, tracking noise alone would not hide a 2 % effect once a few tens of leaps are averaged.
- Detectability is therefore limited by things nobody has measured:
  - whether the fish spreads its pectorals in air at all (S28: "never been observed");
  - body flexion moving the tracked point relative to the centre of mass;
  - variation in attitude from leap to leap.
- None of these can be quantified from the record.
- **"Possibly detectable" stays an unsupported claim.** It is not refuted, and it is not established.

## 4. What measurement would settle it, and what it would cost

1. **Read Daane Fig. 4B, or obtain its plotted values.**
   - Cost: minutes, from any network with access to `cdn.ncbi.nlm.nih.gov` or the Cell Press site, plus digitising; or one email to the corresponding author.
   - It gives the pectoral fin length/SL means for wild type, `lof/+`, `nr21/+` and the double heterozygote, with Tukey groupings.
   - Decision rule (from §3.2):
     - **≤ 0.25 SL**: the phenotype is ≤ 2.4 % even at the 1.57 m/s mean. Record it as below the 2 % threshold and treat the line as closed for aerodynamics.
     - **≥ 0.40 SL**: S28's ~5 % survives at central speeds.
2. **Photograph the spread pectoral fins of the existing double heterozygote** (S28's recommendation 1). This is still the most informative experiment.
   - Cost: hours. Anaesthetise, spread, take one calibrated image.
   - It measures length, span and area directly. That removes both the length assumption and the AR-5 assumption (rule C vs rule A differ by ×1.8–×3.4 in area at the same length).
3. **High-speed (≥ 1000 fps) surface-leap video**, WT vs double het, with a stimulus from below.
   - It answers whether the fins are spread in air, and gives the exit speed and the fitted ascent acceleration.
   - Cost: about 1–2 person-weeks. This is S20-D-D-D's estimate, and it is unsourced.

## 5. Recomputing S28 with the improved input

**What changed.** The improved input is not a new number. It is an honest relabelling, plus a threshold:
- S28's fin length moves from "extrapolation" to **`unknown`; S28's 0.45 SL is not supported by the primary source text**;
- the phenotype becomes a function of that unknown, with the decision thresholds in §3.2.

**The negative: STANDS.**
- No input moved by ×2 flips it (§1).
- Even at the swimming-impairing ceiling of 0.79 SL per fin (Davenport, search-summary via challenge 189) with the Demesmay +2 SD exit of 2.11 m/s, a stack that no measurement supports, the flight deficit is still ×1.26 (script section 4).
- At any fin length ≤ 0.45 SL, the deficit is ≥ ×2.09 even at 2.11 m/s, and ≥ ×2.8 at the 1.57 m/s mean.
- The best range gain anywhere in §1 is 4.5 %.

**The phenotype clause: FALLS as worded.**
- "A possibly detectable 5–10 % reduction in ascent deceleration" was already 4.5–4.9 % at most (challenge 194).
- It rests on an unsourced 0.45 SL fin.
- Across fin lengths of 0.15–0.45 SL and central in-species speeds of 1.38–1.57 m/s, the calculated range is **0.9–6.2 %**. It is ≤ 2.4 % for any fin ≤ 0.25 SL.
- Detectability is uncomputed beyond tracking noise.
- **Corrected wording:** "a calculated ≤ ~5 % (plausibly 1–3 %) reduction in ascent deceleration, conditional on an unmeasured pectoral length of ≥ 0.4 SL per fin for the upper value and on fin spreading in air, which has never been observed; detectability unestablished."

**Overall verdict: STANDS.**
- The organism-level answer (NEGATIVE: no flight, glide, skim, or meaningful leap extension) is unchanged and is robust to its most sensitive input.
- The one positive deliverable S28 offered shrinks and becomes explicitly conditional.
- That makes the negative more complete, not weaker.
- I do not call it "strengthens", because no new measurement was added. The fin-length value remains `unknown`.

## 6. Disagreements preserved

- **Exit speed.** These sources are not averaged:
  - Miln et al. 2021: per-fish maximum 1.38 m/s at 120 fps, n = 50. Read-level: listing, relayed via challenge 75/192; challenge 191 could not locate the paper.
  - Demesmay et al. 2025, *PLoS Biol* 23:e3003484: control mean 1.57 ± 0.27 m/s at 240 fps with manual tracking. Read-level for me: listing (repository relay of S20-D-D-D's full-text read; I did not re-read it this session).
  - Neither study measured a surface exit. No adult zebrafish exit speed is known in the record.
- **Fin geometry rule.**
  - S28 takes case C (AR 5) as its headline and case A (length-only) as "closest to what *longfin* is known to do".
  - Both are kept in the script. They differ by ×1.8–×3.4 in area at the same length (0.15–0.45 SL).
- **Body size.** S28 uses SL 3.0 cm and m 0.25 g (assumed, back-solved). Plaut 2000's abstract implies SL ≈ 3.5–3.6 cm. Challenge 189 cites adults "rarely exceed 0.5 g" (search-summary). No measured mass for the double heterozygote exists in the record.

## 7. Sources

| Source | Read-level |
|---|---|
| S28-organism.md and S28_organism.py @ e8ba4191 | full-text (repository) |
| Challenges 189, 190, 191, 192 (85f2fb5c), 193, 194; S20-D-D-deepen.md @ 17c6d933 | full-text (repository) |
| Daane JM et al. 2021, *Curr Biol* 31:5052, doi:10.1016/j.cub.2021.08.054, PMC9172250 | full-text (text and legends); **Fig. 4B data could-not-access** |
| Plaut I. 2000, *J Exp Biol* 203:813 | abstract |
| bioRxiv 10.1101/2021.01.31.428959 (Gdf5 in zebrafish fins) | full-text, first 100k characters only |
| Demesmay L et al. 2025, *PLoS Biol* 23:e3003484 | listing (via S20-D-D-D, which read it full-text) |
| Miln C et al. 2021, *R Soc Open Sci* 8:210146 | listing (via challenges 75/192) |
| Davenport 1992/1994 pectoral ceiling of 0.78–0.79 SL | search-summary (via challenge 189) |
| ZFIN figure records ZDB-FIG-221222-34/35 | could-not-access (503 / TLS failure) |

```swarm-result
{"subproblem": "S28-D", "evidence": "derived (calculation; the most sensitive input, pectoral fin length per fin, remains unmeasured: Daane 2021 full text contains no numeric value and Fig. 4B data could not be accessed)", "answer": "S28's negative (no flight, glide, skim or meaningful leap extension) stands under x2 changes to every input and is most sensitive, through its 'honest phenotype' clause, to pectoral fin length per fin (S proportional to roughly L_fin^2), which S28 extrapolated as 0.45 SL without any source; the calculated ascent-deceleration reduction is 0.9-6.2% across fin lengths of 0.15-0.45 SL at in-species exit speeds of 1.38-1.57 m/s, needs at least 0.39-0.51 SL per fin to reach 5%, and is at most 2.4% if Fig. 4B shows 0.25 SL or less, so the '5-10% possibly detectable' phenotype falls to a conditional, likely 1-3%, effect of unestablished detectability.", "key_number": "pectoral fin length per fin = unknown (S28's 0.45 SL is unsourced); threshold for a 5% ascent-deceleration reduction = 0.39-0.51 SL per fin, for 2% = 0.22-0.29 SL per fin (calculated, 45 deg, AR-5 rule)", "verdict": "stands", "depends_on": ["S28 conclusion and inputs: docs/research/fish/S28-organism.md @ e8ba4191", "S28 fin length 0.45 SL per fin (extrapolation, unsourced)", "S28 case-C geometry: AR 5 at span = 2*L_fin + 4 mm (assumption); case-A rule chord fixed (assumption)", "S28 body mass 0.25 g at SL 3.0 cm (assumed, back-solved)", "isometric scaling to SL 3.6 cm / 0.43 g (inference)", "Plaut 2000 J Exp Biol 203:813 U_crit 56.0 cm/s = 15.5 SL/s and 43.7 = 12.5 SL/s implying SL 3.5-3.6 cm (abstract)", "Daane et al. 2021 Curr Biol 31:5052: double het has overgrown paired fins, wild-type medial fins, 'phenocopy' of flying-fish bauplan; no numeric fin length in text (full-text)", "Daane et al. 2021 Fig. 4B pectoral length/SL values (could-not-access; unknown)", "Miln et al. 2021 burst max 1.38 m/s (listing)", "Demesmay et al. 2025 PLoS Biol adult escape peak 1.57 +/- 0.27 m/s, 40-ms floor 0.95 m/s (listing via S20-D-D-D full-text)", "assumption: exit speed ~= in-water escape peak (unmeasured)", "CL 1.07 quasi-steady (project-derived)", "CD0 0.08, Oswald e 0.8, body drag CD 0.3 on 24 mm2 scaled with SL^2 (assumptions)", "launch angle 45 deg (assumed; zebrafish leap angle unknown)", "assumption: fins held spread in air throughout ascent (never observed)", "challenge 194: S28 5-10% was L/W, true ascent-decel reduction <=4.9%", "challenge 190: L/W 10% is an upper bound (mass)", "challenge 191: leap-range gain +0.7 to +3.9%", "challenge 192: flight deficit 2.07-3.17x across burst datasets", "Davenport 1992/1994 pectoral length ceiling 0.78-0.79 SL (search-summary via challenge 189)", "tracking-noise model var(c2)=180 sigma^2/(N T^4) with assumed 240-1000 fps and 0.2-0.5 mm noise", "law: point-mass trajectory with quasi-steady lift L=0.5 rho V^2 S CL and drag CD0 + CL^2/(pi e AR)", "negative search: no numeric adult zebrafish pectoral fin length/SL found (scope: 2 web searches, Daane full text, Plaut abstract, partial Gdf5 preprint, challenge 189 searches)"]}
```
