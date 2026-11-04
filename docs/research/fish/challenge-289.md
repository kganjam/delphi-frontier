# Challenge 289: are the two challenge-273 refutations of the S32 exocoetid "validation" sound?

**Claim under review** (harvested summary of challenge 273, branches `claude/challenge-273-exocoetid-taxi-hid0nd` = A and `claude/challenge-273-exocoetid-taxi-x5n6z2` = B):

> "TWO INDEPENDENT challengers refute "model validates against a real animal": the 36 W check is C_D-independent. (A) Deng 2019 CFD pair 36 W @10 m/s / 350 W @16.5 m/s is matched at high speed by constant C_D (311 W) within 11% but missed 5.6x by Re-scaled C_D (62 W); constant C_D "cannot taxi" holds only because exocoetid tail amplitude was assumed 0.08-0.12 L, while 0.2 L gives equilibrium 14.0-16.4 m/s; foil power needed 72/311 W (constant) vs 18/62 W (Re-scaled). (B) 36 W matches neither branch (model needs C_D 0.037 at 10 m/s, 0.091 at 16.5 vs Re-scaled 0.016/0.012); scaling only the friction part of C_D leaves taxi ceiling 8-9 m/s. …"

Recorded evidence level: derived. Recorded value: 0.037, the C_D implied at 10 m/s (challenger B).

## Verdict: WEAKENED

- **The core refutation survives.**
  - The 36 W check contains no C_D term. I confirmed this by reading the code.
  - Within S32's own equations, no single drag branch fits both Deng points at any immersed fraction I tried.
- **Three parts of the summary are weaker than written:**
  1. **"Matched at high speed by constant C_D within 11 %."** This holds only at φ = 0.5. At φ = 0.25 the constant branch matches Deng's *low*-speed point instead, and misses the 350 W point by about 2×.
  2. **The recorded value 0.037.** It is conditional on φ and on extrapolating Floryan's power law. Over φ 0.25–1.0 it ranges from 0.019 to 0.071, which brackets both branches. So it does not single out either one.
  3. **"0.2 L gives equilibrium 14.0–16.4 m/s."** The arithmetic is correct. But for the 191 g fish, 13.9 m/s is below the glide speed V_to of 14.98 m/s. For the 300 g fish, 16.38 m/s is just under V_to 16.39 m/s. So relaxing the amplitude makes constant C_D taxi (accelerate from 10 m/s), but the constant-C_D fish still does not reach glide speed. Getting there needs A_pp ≥ 5.5 cm, which is 0.21 L.
- **"Two independent" means independent code, not independent evidence.** Both challengers use the same S32 geometry, the same Floryan coefficients (inherited, not re-read) and the same Deng abstract, read the same way (50 Hz, steady at 16.5 m/s). Their agreement to 0.1 W shows that the arithmetic replicates. It does not add a second line of evidence.

Everything below is **derived**: a calculation with S32's equations. Nothing here is a measurement. The script is `docs/research/fish/challenge-289_check.py` (`python3 -I docs/research/fish/challenge-289_check.py`). I wrote it from the S32 force equations myself. It does not import either challenger's script or `S32_taxi.py`.

## Sources and read levels

| Source | Read level | Used for |
|---|---|---|
| `S32_taxi.py` on `origin/claude/s32-multi-stroke-launch-qpq9g2` | full-text (read; equations reimplemented, not re-run) | force model, the power check at lines 273–278 |
| challenge-273.md on both branches (A, B) | full-text | the claims being judged |
| Deng et al. 2019, bioRxiv 10.1101/765560 | **not read by me.** I rely on A's and B's abstract-level paraphrase (36 W minimum for steady taxi at 10 m/s, 15°, 50 Hz; 16.5 m/s at 350 W). This is CFD, not an observation | target numbers |
| Floryan et al. 2017 (c₆ 2.55, C_D 0.08, c₈ 7.78, c₉ 4.89; measured at Re 4,780–9,560) | not read by me (via S32) | thrust and power laws |
| Fish 1990 allometries | not read by me (via S32, project-transcribed) | S_w, S_hypo, V_to |
| Wang, APS 2024 (13.5 Hz) | not read by me (B reports search-summary only) | frequency sensitivity only |

Negative search scope: I ran no literature searches. A measured exocoetid immersed fraction φ and a measured taxi tail amplitude remain **unknown**. Neither challenger nor S32 found them.

## 1. Arithmetic redone independently (191 g, c 2.5 cm, 50 Hz, φ 0.5 unless stated)

**Geometry.**
- S_w = 127.5 cm², S_hypo = 10.23 cm², V_to = 14.98 m/s.

**36 W check.**
- `S32_taxi.py` lines 273–278 compute P = ½ρU³S(c₈ + c₉f\*)St². No C_D appears in it.
- My values: 21.5 W at A_pp 2.0 cm, 36.3 W at 2.6 cm, 51.5 W at 3.1 cm. **This confirms the "C_D-independent" part of the claim.**

**Equilibrium speed U_eq** (my code):

| M | A_pp | U_eq, constant C_D | U_eq, Re-scaled C_D | V_to |
|---|---|---|---|---|
| 191 g | 2.0 cm | 4.99 | 11.11 | 14.98 |
| 191 g | 2.6 cm | 6.95 | 15.58 | 14.98 |
| 191 g | 5.1 cm (0.2 L) | **13.92** | 39.2 | 14.98 |
| 300 g | 6.0 cm (0.2 L) | **16.38** | 48.0 | 16.39 |

- These match A's numbers.
- With constant C_D, U_eq = V_to needs A_pp = 5.49 cm.

**Steady-state power** (amplitude solved so that net force = 0):

| Speed | Constant C_D | Re-scaled C_D |
|---|---|---|
| 10 m/s | 72.4 W | 18.3 W |
| 16.5 m/s | 311.1 W | 62.1 W |

These match A and B.

**C_D implied by Deng's power** (net force = 0 at Deng's power):
- 0.0367 at 10 m/s and 0.0906 at 16.5 m/s. This matches B.
- The Re-scaled values are 0.0156 and 0.0122, which also match.

## 2. Hidden assumption that carries the "which branch matches" detail: the immersed fraction φ

- The only geometric input that fixes how much foil area meets the water is φ = 0.5. It is an S32 assumption; S32 itself sweeps φ from 0.25 to 1.0 for the zebrafish.
- Relaxing it (derived):

| φ | P(10), const | P(16.5), const | P(10), scaled | P(16.5), scaled | ratio P16.5/P10 |
|---|---|---|---|---|---|
| 0.25 | **39.8 W** (+11 % vs 36) | 164 W (0.47× of 350) | 12.7 W | 39.7 W | 4.1 / 3.1 |
| 0.5 | 72.4 W | **311 W** (−11 %) | 18.3 W | 62.1 W | 4.3 / 3.4 |
| 1.0 | 140 W | 605 W | 31.2 W | 107 W | 4.3 / 3.4 |
| Deng (CFD, abstract) | 36 W | 350 W | | | **9.7** |

- **Implied C_D at 10 m/s by φ:** 0.071 (φ 0.25), 0.037 (φ 0.5), 0.019 (φ 1.0). At 16.5 m/s: 0.181, 0.091, 0.045.

**My inference.**
- Which Deng point the constant branch "matches" depends entirely on φ.
- A's "within 11 % at high speed" is therefore a φ = 0.5 artifact, not evidence for the constant branch.
- B's 0.037 is likewise not a discriminating number.
- What *is* robust across φ:
  - The model's power ratio is 3.1–4.3 for every branch and every φ, against Deng's 9.7.
  - The implied C_D rises with speed by a factor of about 2.5 at every φ. A Re^−½ law falls with speed.
  - The Re-scaled branch is 3.3–8.8× low at 16.5 m/s at every φ.
- So the conclusion that Deng's pair does not support the Re-scaled branch survives the relaxation. The specific "constant branch matches" point does not.

## 3. Second hidden assumption: Floryan's power law, extrapolated unscaled

- Both challengers turn Deng's watts into thrust using c₈ and c₉. These were measured at the same Re as C_D, about 26–43× below taxi Re.
- If the effective power per unit thrust were off by a factor k, the implied C_D would scale roughly as 1/k (derived):
  - at 10 m/s: 0.080 for k = 0.5, 0.051 for k = 0.75, 0.023 for k = 1.5;
  - at 16.5 m/s the factors are the same.
- S32's 36 W check uses the same unscaled power law, so this assumption does not rescue S32. It does mean the challengers' *absolute* corrected values (implied C_D, required watts) are only as good as an extrapolation that nobody has validated.

Frequency, by contrast, barely matters: over 13.5–100 Hz the implied C_D at 10 m/s spans only 0.034–0.039. The c₉f\* term is small because f\* = fc/U ≤ 0.25. So B's worry that Deng's 350 W run used a different frequency changes little *within this model*. It could still matter through different deflection or immersion in Deng's CFD, which I cannot check without the full text.

## 4. Proxy check

- **The quantity that matters:** whether the lobe drag law is right at Re 2.5–4×10⁵.
- **What the comparison actually tests:** Deng's whole-fish CFD power, read through the Floryan *power* law at low Re and an assumed φ.
- Three of those inputs are unvalidated extrapolations or assumptions. A comparison resting on them can falsify the claim that the animal *validates* the Re branch. It cannot establish a corrected C_D. The challengers' verdict uses it the first way, which is fine. The harvested value of 0.037 uses it the second way, which is not.

## 5. Evidence level

- "derived" is honest for every number in the claim.
- One fault is in sourcing: the harvested summary attributes "Deng 2019 CFD pair" without saying it rests on an abstract-level paraphrase. B fetched the abstract from biorxiv.org; A read it via Europe PMC through a summarising tool. Both challengers state this in their documents, but the summary drops it.
- The summary's own note, "S32 code not re-run by harvester", is accurate. I also did not run `S32_taxi.py`; I reimplemented the equations, and they agree to 0.01 m/s and 0.1 W.

## 6. What survives and what does not

- **Survives:**
  - The 36 W check is C_D-independent, so "ONLY with Reynolds-dependent C_D" is false.
  - No branch reproduces Deng's speed–power pair at any φ from 0.25 to 1.0.
  - "Constant C_D cannot taxi at all" depends on the assumed amplitude.
  - Friction-only scaling: B's ceiling of 8–9 m/s was not re-run by me, so I neither confirm nor dispute it.
- **Weakened:**
  - "matched at high speed by constant C_D within 11 %" (true only at φ 0.5);
  - 0.037 as a meaningful implied C_D (range 0.019–0.071 over φ, roughly inverse in the power-law factor);
  - "0.2 L gives 14.0–16.4 m/s" read as "constant C_D taxis to take-off": it falls short of V_to at both masses, by 7 % at 191 g.

```swarm-challenge
{"claim_id": 289, "outcome": "weakened", "reason": "All arithmetic reproduces independently and the core refutation holds (the 36 W check has no C_D term, and no drag branch fits Deng's 36 W/350 W pair at any immersed fraction 0.25-1.0, model power ratio 3.1-4.3 vs 9.7), but 'constant C_D matched within 11% at high speed' and the implied C_D 0.037 are artifacts of the assumed phi = 0.5 (at phi 0.25 constant C_D matches the 10 m/s point instead, implied C_D 0.019-0.071 across phi), and 0.2 L still leaves the constant-C_D fish below take-off speed (13.9 vs 14.98 m/s), so the two challengers share inputs rather than being independent evidence.", "corrected_value": "C_D implied by Deng 2019 steady 10 m/s/36 W in the S32 equations: 0.019-0.071 for phi 1.0-0.25 (0.037 only at phi 0.5); implied C_D 16.5/10 m/s ratio ~2.5 at every phi (derived)", "depends_on": ["S32_taxi.py force and power equations and exocoetid inputs (full-text read, reimplemented)", "Deng2019 bioRxiv 765560 abstract numbers 36 W steady @10 m/s and 350 W @16.5 m/s as paraphrased by challenge-273 A and B (not read by me)", "Floryan2017 c6 2.55, C_D 0.08, c8 7.78, c9 4.89 via S32 (not re-read)", "Fish1990 allometries via S32 (project-transcribed)", "immersed fraction phi swept 0.25-1.0 (S32 assumption range)", "S32 assumptions f 50 Hz, chord 2.5 cm, CL_max 1.07"]}
```
