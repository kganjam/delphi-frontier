# Replicate 84: tail-beat frequency for a 4 cm zebrafish taxiing at 1.95 m/s, from Eloy's optimal Strouhal number

**Question as given:** "Replication", with the inputs on branch
`claude/strouhal-band-rederivation-ljqyv7`, file `replicate-52.md`. Claim 84 turned out to be the
result of `replicate-52.md`, so this file re-derives that result.

## 0. Independence disclosure (read this first)

**My derivation is not blind, and I am stating that up front.** The brief pointed me at
`replicate-52.md` as the place the inputs live. The first 30 lines of that file hold the author's
headline result: St ≈ 0.30–0.34 (bracket 0.26–0.42), 72–83 Hz (bracket 64–101 Hz), and
1.4–1.6× the 52 Hz maximum. I read those lines before I knew they held the answer. I stopped there
and did not read the rest of the file until §5.

What I did independently:
- I fetched Eloy 2012 myself and extracted its text.
- I verified Li = (S/h²)·C_d against Eloy's table rows.
- I wrote and ran my own script.
- I added a 28 °C viscosity case and a drag-multiplier case.

What is **not** independent:
- **The method.** Eloy's power law evaluated with eq. 16 was the method named in the headline I saw.
- **The tail-span bracket.** The h/L = 0.15–0.30 bracket matches the author's, and I cannot rule out
  anchoring.

So agreement here confirms the arithmetic and the primary-source transcription. It does **not**
confirm the choice of model.

## 1. Inputs

| Input | Value | Source | Read level |
|---|---|---|---|
| St definition | St = fA/U, A **peak-to-peak** | Eloy C (2012) J Fluids Struct 30:205–218, arXiv:1102.0223v1, abstract and §1 | full-text (arXiv preprint v1, not the version of record) |
| Lighthill number | Li = πD/(2mU²) = (S/h²)·C_d | Eloy 2012 eq. 5 (pdftotext garbled the fraction, so I checked it against the table: see below) | full-text (preprint) |
| Drag law | C_d = max(2×1.328 Re^-1/2, 0.072 Re^-1/5) | Eloy 2012 eq. 16 | full-text (preprint) |
| Wetted area | S = 0.4 L² "for most fishes (not elongated ones)" | Eloy 2012 §3.2 | full-text (preprint) |
| Optimum fit | St ≈ 0.75 Li^(1/3) | Eloy 2012 §3.3 | full-text (preprint) |
| Table check rows | trout 20.1 cm (S/h² 8.2, Re 1.1e5, Li 0.067); saithe; Atlantic silverside; bullfrog tadpole; juvenile trout | Eloy 2012 Tables 2–3 | full-text (preprint) |
| Law-library entry | `where_it_breaks` and `contested_by` | `library/laws/strouhal.yaml` on `origin/work/law-library` | full-text |
| TL | 0.04 m | S24-behaviour.md on `origin/claude/s24-surface-taxiing-launch-tsepbn` (line 24: "4 cm, 0.4 g zebrafish") | full-text |
| Target speed | 1.95 m/s (3-BL wing) | S24-behaviour.md lines 9 and 32 | full-text |
| A | 0.20 TL = 8 mm peak-to-peak. This is an S24 **assumption**, not a measurement | S24-behaviour.md §3.2 | full-text |
| Frequency ceiling | 52 Hz, the "maximal frequency reached during escape" | Kyriakatos et al. 2011, as relayed by S24 | could-not-access (relayed only) |
| ν | 1.004e-6 m²/s (20 °C), and 0.836e-6 m²/s (28 °C, a zebrafish husbandry temperature) | my **assumption**, standard water values from memory | — |
| Zebrafish tail span h/L | **unknown**. Bracketed as 0.15–0.30, central 0.20–0.25 | my **assumption**, inside Eloy's 0.05L–0.35L range. Not independent of replicate-52 (see §0) | I did not search for a measurement |

**Transcription check (calculated).** Eloy's eq. 16 times the table's S/h² reproduces the table's
Li:

| Row | Li, eq. 16 × S/h² | Li, table |
|---|---|---|
| trout 20.1 cm | 0.0657 | 0.067 |
| saithe | 0.0384 | 0.038 |
| silverside | 0.2220 | 0.224 |
| bullfrog tadpole | 0.1926 | 0.193 |
| juvenile trout | 0.1848 | 0.184 |

So Li = (S/h²)·C_d, with no factor of ½. The yaml's `contested_by` line writes "(S/h^2)*C_d/2",
which is a transcription error. My inference is that it would lower St by 2^(1/3).

**A second note on the yaml (my reading of Eloy's table).** The values listed in `where_it_breaks`
(goldfish 0.54, tadpole 0.79, lungfish 1.02 and so on) are the **observed** St column of Eloy's
tables. They are not Eloy's model optimum.
- The goldfish 0.54 row is the artificially selected Eggfish morph. For that row Eloy used Blake's
  high fitted drag (Li 0.538), not eq. 16.
- The yaml's "lungfish 1.02 (Re 7.0e3)" matches the table as printed. That is L = 55 cm at
  Re 7.0×10³.

## 2. Arithmetic (all CALCULATED, none observed)

Re = U·L/ν = 1.95 × 0.04 / 1.004e-6 = **7.77 × 10⁴** (20 °C), or 9.33 × 10⁴ (28 °C).

C_d at 20 °C:
- laminar term: 2.656/√77 700 = 2.656/278.7 = 0.00953
- turbulent term: 0.072/77 700^0.2 = 0.00757
- max: **0.00953**

C_d at 28 °C: 0.00870.

Then S/h² = 0.4/(h/L)², Li = (S/h²)·C_d, St = 0.75·Li^(1/3), and f = St·U/A = St × 1.95/0.008 = 243.75·St.

**20 °C, eq. 16 drag (k = 1):**

| h/L | S/h² | Li | St | f (Hz) | f/52 |
|---|---|---|---|---|---|
| 0.15 | 17.78 | 0.169 | 0.415 | 101 | 1.95 |
| 0.20 | 10.00 | 0.095 | 0.343 | 83.5 | 1.61 |
| 0.25 | 6.40 | 0.061 | 0.295 | 72.0 | 1.38 |
| 0.30 | 4.44 | 0.042 | 0.261 | 63.7 | 1.23 |

**Sensitivity (calculated):**
- **28 °C:** St is about 3% lower: 0.254–0.403, or 62–98 Hz.
- **Drag doubled (k = 2):** Eloy says eq. 16 "is usually an underestimate". With k = 2, St is
  0.33–0.52, or 80–127 Hz.

Script: `docs/research/fish/replicate-84_calcs.py` (run with `python3 -I`).

## 3. My value

**f ≈ 72–84 Hz central** (h/L 0.25–0.20), **bracket 62–101 Hz** (h/L 0.30–0.15, 20–28 °C, eq. 16
drag). That is **1.4–1.6×** the 52 Hz escape maximum (bracket 1.2–1.95×), from **St_opt ≈ 0.30–0.34**
(bracket 0.25–0.42) at Re ≈ 7.8 × 10⁴. All of this is CALCULATED.

Uncertainty not covered by the bracket:
- **Tail span.** It is unmeasured, and St scales as h^(-2/3).
- **Drag.** It is underestimated by eq. 16, which could push f up by ×1.26 or more.
- **The fit.** The power law is an approximation of Eloy's model curve. It is not the data.
- **Validity.** The model is applied outside its stated validity, because surface taxiing is not
  steady submerged cruising.

## 4. Author's claim vs my inference

**Eloy's claims:**
- St_opt rises with Li.
- St ≈ 0.75 Li^(1/3).
- The eq. 16 drag law and the S = 0.4 L² default.

**My inference:**
- Applying those to a zebrafish at 1.95 m/s gives the numbers above.
- Transplanting goldfish or tadpole observed St values to this operating point is not supported by
  Eloy's own scaling, because Li at Re ~8e4 is about 0.04–0.17, not ~0.5.

**What I did not test:** whether St_opt is the right quantity to call "required". See §5.

## 5. Comparison with the recorded value

Read only after §1–§4.

**Recorded claim 84** (quoted in `challenge-84.md` on `origin/claude/strouhal-challenge-84-xogjpb`,
full-text): "required tail-beat frequency at 1.95 m/s is 72-83 Hz (bracket 64-101), 1.4-1.6x the 52
Hz EMG max, from Eloy St_opt=0.75 Li^(1/3)=0.30-0.34 at Re 7.8e4 (calculated)". It is recorded as
`derived`, value 77.5 Hz. I then read `replicate-52.md` in full.

**Verdict: AGREE on the number.** At 20 °C I get 72.0 and 83.5 Hz central and 63.7–101 Hz for the
bracket, against the recorded 72–83 and 64–101. My 28 °C case extends the low end to 62 Hz. The
transcription of Eloy's eq. 5, eq. 16 and the S default is correct. The author also caught the
yaml's /2 error, which I found independently from the table check.

**Agreement is limited by two things:**
1. **Contamination (§0).** I saw the headline result, and my h/L bracket is the same as the
   author's. This is a check of the arithmetic and the transcription, not of the modelling choices.
2. **The meaning of "required" is challenged.** `challenge-84.md` argues that Eloy's St_opt is
   the *efficiency optimum*, not the *minimum* St at which thrust balances drag. It reports
   (calculated, its own numerical solution of Eloy's problem 9) thrust balance at 31–38 Hz, and the
   low edge of the acceptable band at 42–51 Hz. Both are at or below 52 Hz.
   - Eloy's text agrees with the premise: problem (9) minimises wasted power subject to T = D. That
     is my reading of the full text.
   - I did **not** reproduce the challenge's St_min numbers. Its small-angle closed form
     St_min = √(8Li/π³) gives 0.157 at Li 0.095, which I can check: √(0.761/31.0) = 0.157.
     That is consistent with the challenge, but I did not derive the formula myself.
   - So: the 72–83 Hz figure is right **as an efficient-gait frequency**. Whether it is "required"
     is disputed, and the disagreement is preserved here, not resolved.

**Negative-search scope:**
- I did not search for zebrafish caudal-fin span, zebrafish C_d, or zebrafish kinematics above 1 m/s.
- I did not read Kyriakatos 2011 or Mwaffo 2017.
- Sources consulted: Eloy arXiv:1102.0223v1, `library/laws/strouhal.yaml`, S24-behaviour.md, and
  (for §5 only) replicate-52.md and challenge-84.md.

```swarm-replication
{"claim_id": 84, "my_value": "72-84 Hz central (bracket 62-101 Hz) at 1.95 m/s, 1.4-1.6x the 52 Hz max, from Eloy St_opt=0.75 Li^(1/3)=0.30-0.34 (0.25-0.42) at Re 7.8e4; calculated, not observed", "agrees": true,
  "note": "Arithmetic and Eloy transcription reproduce (Li=(S/h^2)Cd verified on 5 table rows), but I saw the headline before deriving, so this confirms arithmetic not model choice, and St_opt is an efficiency optimum, not a minimum 'required' St (challenge-84, unresolved here)."}
```
