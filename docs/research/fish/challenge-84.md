# Challenge 84: adversarial review of the replication of claim 52 (S24 zebrafish taxi, Strouhal band)

**Claim under test (as recorded, author's words):** "Replication: required tail-beat frequency at
1.95 m/s is 72-83 Hz (bracket 64-101), 1.4-1.6x the 52 Hz EMG max, from Eloy St_opt=0.75
Li^(1/3)=0.30-0.34 at Re 7.8e4 (calculated). Disagrees with claim 52 (132-199 Hz). Harvester check:
implied amplitude St*U/f ~ 8 mm for both 52 (0.54-0.8) and this one; difference is the Strouhal
number alone. St choice NOT independently resolved."
Recorded as `derived`, value 77.5 Hz. Source: `replicate-52.md` on
`origin/claude/strouhal-band-rederivation-ljqyv7` (read level: full-text).

**Verdict: WEAKENED.** The arithmetic is correct, and the disagreement with claim 52 holds. The
word "required" does not hold. Eloy's St_opt is the Strouhal number of **maximum efficiency** for a
swimmer whose thrust balances drag. It is not the **minimum** Strouhal number at which thrust
balances drag. In Eloy's own model, using the claim's own inputs, thrust balance at 1.95 m/s is
reachable at **31-38 Hz** (calculated), and the low edge of Eloy's own "acceptable" efficiency band is
**42-51 Hz** (calculated). Both are at or below 52 Hz. The ">52 Hz" conclusion is only recovered if
real drag is about 1.6-3× Eloy's eq. 16, or if the fish is assumed to swim near peak efficiency.

## Sources

| Source | What I used | Read level |
|---|---|---|
| Eloy C (2012) "Optimal Strouhal number for swimming animals", arXiv:1102.0223v1 (preprint, not the version of record) | St = fA/U with A **peak-to-peak** (§1.1); eqs 4a-b, 5 (Li = πD/(2mU²) = (S/h²)C_d, m = ρπh²), 8-11, problem (9); eq. 16 drag law; the "η > η_max − 0.1 acceptable" definition (§2.1); the power law St ≈ 0.75 Li^(1/3) (§3.3); Table rows for beluga and bottlenose dolphin (S/h²) | full-text (PDF text extracted with pdftotext; Figures 2 and 4 are images, so I could not read numbers off them) |
| `replicate-52.md`, `replicate-52_calcs.py` | the claim, its inputs, its working (read only after my §1 recomputation) | full-text |
| Kyriakatos et al. 2011 (52 Hz maximum) | used as given | **could-not-access**: not read by me. It is relayed by S24 and by the replication. I did not check whether 52 Hz is an EMG burst rate or a kinematic tail-beat rate. The claim's label "EMG max" is the claim's own. |
| Mwaffo et al. 2017 PeerJ 5:e4041 (zebrafish St) | not used for the verdict | **could-not-access**: relayed by challenge-52 only. Not fetched. |

## 1. Independent arithmetic (calculated)

I recomputed from the stated inputs before reading the author's script: U = 1.95 m/s, L = 0.04 m,
ν = 1.0e-6 m²/s, S = 0.4 L², h/L = 0.15-0.30, and A = 0.20 L = 8 mm.

- Re = 1.95 × 0.04 / 1e-6 = 7.80 × 10⁴.
- √78000 = 279.3, so 2.656/279.3 = 0.00951. 78000^0.2 = e^(0.2 × 11.264) = 9.515, so 0.072/9.515 =
  0.00757. C_d = max = **0.00951**.
- h/L = 0.20: Li = 10 × 0.00951 = 0.0951, Li^(1/3) = 0.456, St = 0.342, f = 0.342 × 1.95/0.008 = **83.4 Hz** (1.60×).
- h/L = 0.25: Li = 0.0609, St = 0.295, f = **71.9 Hz** (1.38×).
- h/L = 0.15: St = 0.415, f = 101 Hz. h/L = 0.30: St = 0.261, f = 64 Hz.

**All of the claim's numbers reproduce.** The "harvester check" is true but tautological: A = 8 mm
is an input to both claims, so St·U/f must return 8 mm. It does not test anything independently.

**Span convention check.** Eloy writes m = ρπh². In Lighthill's theory, that expression is the added
mass of a plate of *semi*-span h. Eloy's table, however, gives S/h² = 7.3 (beluga) and 7.9
(bottlenose dolphin). With S ≈ 0.4-0.5 L², those values imply h ≈ 0.23-0.26 L, which is a
full-fluke-span value. This is my inference from the table, not from Fig. 2, which I could not read.
The power-law fit was made on that convention, so the claim's use of full span is internally
consistent. This is **not a defect.**

## 2. Proxy: St_opt stands in for "required St". Wrong quantity.

Eloy's problem (9) is "**min ⟨E⟩** such that ⟨T⟩ = D". St_opt is therefore the argmin of wasted
power among all gaits that balance thrust and drag. Many gaits with lower St also balance thrust,
at lower efficiency. The quantity S24 needs is the **lowest** tail-beat frequency that can sustain
1.95 m/s, which is St_min(Li)·U/A. It is not the efficient frequency.

I implemented Eloy's problem directly from eqs 2a-b, 4a-b, 5, 8a-b with the optimal-form kinematics
he reports (α = ψ = 0; θ = θ₀ cos ωt; ẏ = πSt U cos ωt), using full cos θ / sin θ rather than the
Bessel truncation. For each θ₀ I solved T = D for St, then took the minimum St, the band where
η > η_max − 0.1, and the optimum. Script: `challenge-84_calcs.py`.

**Validation (calc vs Eloy's fit):** at Li = 0.01 / 0.1 / 1.0, my optimum is 0.184 / 0.371 / 0.865,
against 0.75 Li^(1/3) = 0.162 / 0.348 / 0.750. My optimum runs 7-15% above the power law. The
likely cause is the harmonic truncation or the fit itself, but I have not resolved which. The
direction of the gap makes the claim's St_opt slightly *low*, not high.

**Results, all CALCULATED at U = 1.95 m/s and A = 8 mm.** k is a multiplier on eq. 16 drag.

| h/L | k | Li | St_min (thrust = drag) | St, low edge of acceptable band | St_opt (numeric) | f_min (Hz) | f_accept-low (Hz) | f_opt (Hz) |
|---|---|---|---|---|---|---|---|---|
| 0.20 | 1 | 0.095 | 0.157 | 0.210 | 0.365 | **38** | **51** | 89 |
| 0.25 | 1 | 0.061 | 0.125 | 0.173 | 0.315 | **31** | **42** | 77 |
| 0.15 | 1 | 0.169 | 0.209 | 0.270 | 0.443 | 51 | 66 | 108 |
| 0.30 | 1 | 0.042 | 0.104 | 0.147 | 0.282 | 25 | 36 | 69 |
| 0.20 | 2 | 0.190 | 0.222 | 0.284 | 0.461 | 54 | 69 | 112 |
| 0.25 | 2 | 0.122 | 0.177 | 0.234 | 0.395 | 43 | 57 | 96 |
| 0.20 | 3 | 0.285 | 0.271 | 0.340 | 0.533 | 66 | 83 | 130 |
| 0.25 | 3 | 0.183 | 0.217 | 0.280 | 0.456 | 53 | 68 | 111 |

For a cross-check, the small-angle closed form St_min = √(8 Li/π³) gives 0.209 / 0.157 / 0.125 /
0.104 for h/L = 0.15-0.30, which matches the numeric column exactly.

**What this shows (my inference).** With the claim's own inputs (k = 1, central h), the fish can
balance thrust at 31-38 Hz, and can stay within 0.1 of peak Froude efficiency at 42-51 Hz. Both are
below the 52 Hz maximum. The claim's 1.4-1.6× shortfall is a statement that the fish cannot swim at
**peak efficiency** at 1.95 m/s. It does not show that the fish cannot swim at 1.95 m/s.

## 3. Hidden assumptions, relaxed

1. **Efficiency optimum (above).** This is the assumption that carries the result. Relaxing it to
   Eloy's own acceptable band drops the central frequency below 52 Hz.
2. **Drag.** Eloy states that eq. 16 "is usually an underestimate", and cites sturgeon at 3.5×
   trout. S24's case is surface taxiing with a partly emerged body, so wave and spray drag are
   likely extra. I have no zebrafish or surface-taxi C_d; it is `unknown`, and I did not search for
   it. Break-even, interpolated from the table (calc): the acceptable-band low edge reaches 52 Hz at
   k ≈ 1.0 (h = 0.20 L) to k ≈ 1.6 (h = 0.25 L). St_min reaches 52 Hz at k ≈ 1.9 (0.20 L) to
   k ≈ 2.9 (0.25 L). The "exceeds 52 Hz" conclusion is therefore **drag-limited, not
   Strouhal-limited**. It stands or falls on an unmeasured drag multiplier of roughly 1.5-3.
3. **Amplitude.** A = 0.20 L is an S24 calibration assumption, and the claim acknowledges it. In
   Eloy's model the optimum fixes St and θ₀ but not A/L, so f = St·U/A is not closed by the model.
   At the claim's own St_opt (0.30-0.34), A = 0.30 L gives 48-56 Hz (0.9-1.1×), and A = 0.15 L gives
   96-111 Hz (calc). The 1.4-1.6× ratio holds only at A ≈ 0.2 L.
4. **Steady, deep, elongated-body regime.** The author already flagged this. Eloy's validity
   criterion (§2.2) and the "h ≪ L" assumption do not cover a surface-taxiing 4 cm fish. My
   numerical check inherits the same limitation, so it does **not** rescue or refute the regime
   question.

## 4. Evidence level

`derived` is honest. The replication labels every number as calculated, and the value 77.5 Hz is
the midpoint of 72-83 Hz. One defect remains in the claim sentence. "Required" presents an
efficiency-optimal frequency as a feasibility threshold, which is a mislabel of *what* was derived,
not of *how*. The claim's own caveat "St choice NOT independently resolved" is correct, and this
challenge resolves that caveat against the efficiency-optimal reading.

## 5. Counter-examples and regimes

- **Zebrafish measured St (Mwaffo et al. 2017).** As relayed by challenge-52, it is ≈ 0.73
  (cruise) and ≈ 1.03 (burst) peak-to-peak at Re ~1e3. I have **not read** this source
  (could-not-access by me; not fetched). If correct, it shows real zebrafish operating well above
  both St_opt and St_min at low Re. That cuts against my lower bound being *realised*, though not
  against it being *feasible* in Eloy's model. Measured St and modelled St disagree here, and I
  leave that disagreement standing rather than averaging it.
- **Negative-search scope:** I searched no literature beyond Eloy's arXiv preprint. I made no search
  for zebrafish caudal-fin span, zebrafish C_d, surface-taxi drag, or tail-beat kinematics above
  1 m/s. "Unknown" in §3 means not searched, not searched-and-absent.

## 6. What survives and what does not

- **Survives:** the arithmetic, the Re-dependent Li recomputation, the rebuttal of transplanting
  goldfish and tadpole St (so claim 52's 132-199 Hz is still contradicted), and the evidence label.
- **Weakened:** "required frequency 72-83 Hz, 1.4-1.6× the 52 Hz max". In Eloy's own model with the
  claim's own inputs, this is the *efficiency-optimal* frequency. The thrust-feasible minimum is
  31-38 Hz, and the near-optimal band starts at 42-51 Hz (calculated). Whether 1.95 m/s exceeds the
  52 Hz maximum then depends on an unmeasured drag multiplier (≳1.5-3× eq. 16) and on A = 0.2 L.
  It is not settled by the Strouhal number.

```swarm-challenge
{"claim_id": 84, "outcome": "weakened", "reason": "Arithmetic reproduces, but Eloy's St_opt is the efficiency optimum, not the minimum St for thrust=drag; in Eloy's own model with the claim's inputs the thrust-feasible frequency is 31-38 Hz and the acceptable-efficiency band starts at 42-51 Hz, so exceeding 52 Hz hinges on an unmeasured drag multiplier (~1.5-3x eq.16) and on A=0.2 TL, not on Strouhal.",
  "corrected_value": "efficiency-optimal 72-83 Hz (power law; 77-89 Hz by direct optimisation), but thrust-balance minimum 31-38 Hz and acceptable-band low edge 42-51 Hz at A=8 mm, h=0.20-0.25 L, eq.16 drag (all calculated)",
  "depends_on": ["Eloy 2012 arXiv:1102.0223v1 eqs 4-5, 8-11, problem (9), eq.16 and acceptable-band definition (full-text preprint)", "S = 0.4 L^2 (Eloy default)", "zebrafish tail span h/L = 0.20-0.25 (assumption, unmeasured)", "A = 0.20 TL = 8 mm (S24 assumption)", "nu = 1.0e-6 m^2/s", "52 Hz maximum (Kyriakatos et al. 2011, not read by me)", "drag multiplier k on eq.16 = 1 baseline (unknown; sensitivity k=2,3 given)", "challenge-84_calcs.py numerical optimisation (validated 7-15% above Eloy power law)"]}
```
