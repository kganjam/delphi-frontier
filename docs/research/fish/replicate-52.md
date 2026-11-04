# Replicate 52: what Strouhal number to use for S24's 4 cm zebrafish at 1.95 m/s

**Question, as given (with the answer removed):** "S24 applied the Strouhal CRUISING band
0.2-0.3, but the law library records that small, low-Reynolds swimmers sit ABOVE it (goldfish
0.54 at Re 7.1e3, tadpole 0…". The inputs were to be recomputed from
`library/laws/strouhal.yaml` `where_it_breaks` (Eloy 2012 values).

**What I derived.** I computed the Strouhal number appropriate to S24's operating point, and from
it the tail-beat frequency a 4 cm zebrafish needs to keep making thrust at 1.95 m/s. S24's inputs
are unchanged: A = 0.20 TL peak-to-peak and the 52 Hz measured escape maximum.

**Process note.** I derived this before looking for the recorded value. To find out what "S24"
was, I read S24-behaviour.md §3.2 and S24_calcs.py on `origin/claude/s24-surface-taxiing-launch-tsepbn`.
Those files hold S24's inputs and its own 0.2-0.4 table, not the claim under test. I found the
recorded claim and an existing challenge (`challenge-52.md`) only after §1-§3 below were computed.
I read them then, for §5 only.

## Result (all CALCULATED, none observed)

- **Optimal St for a 4 cm zebrafish at 1.95 m/s:** St ≈ **0.30-0.34** (central, tail span
  h = 0.20-0.25 L), with a bracket of **0.26-0.42** (h = 0.30-0.15 L). This comes from Eloy's
  model, St ≈ 0.75 Li^(1/3), evaluated with Eloy's own drag law.
- **Required tail-beat frequency at A = 8 mm:** **72-83 Hz** central, bracket **64-101 Hz**.
- **Against the 52 Hz measured maximum:** **1.4-1.6×** central, bracket **1.2-1.9×**.
- **Transplanted values don't fit.** Goldfish 0.54 (132 Hz), tadpole 0.79 (193 Hz) and lungfish
  1.02 (249 Hz) **do not apply** at this operating point, by Eloy's own model. The reason is
  that St_opt is a function of the Lighthill number Li. Li depends on body form and on Re through
  C_d. At 1.95 m/s the zebrafish's Re is 7.8 × 10⁴, about 11× the goldfish's 7.1 × 10³.

## 1. Inputs

| Input | Value | Source | Read level |
|---|---|---|---|
| Eloy optimum fit | St ≈ 0.75 Li^(1/3) | Eloy C (2012) J Fluids Struct 30:205-218, arXiv:1102.0223v1 §3.3 | full-text (arXiv preprint v1, not the version of record) |
| Lighthill number | Li = (S/h²)·C_d, h = **full** tail span ("0.05L < h < 0.35L") | Eloy 2012 eq. 5 and §4 | full-text (preprint) |
| Drag law | C_d = max(2·1.328 Re^-1/2, 0.072 Re^-1/5) | Eloy 2012 eq. 16 | full-text (preprint) |
| Wetted area | S = 0.4 L² ("for most fishes (not elongated ones)") | Eloy 2012 §3.2 | full-text (preprint) |
| Taxon values (goldfish, tadpoles, lungfish, eels, trout…) | Eloy Tables 1-3, columns L, S/h², Re, Li, St | Eloy 2012 | full-text (preprint) |
| Same values, as relayed | goldfish 0.54 (Re 7.1e3), tadpole 0.79, lungfish 1.02 … | `library/laws/strouhal.yaml` on `origin/swarm-architecture` | full-text |
| TL | 0.04 m | S24 project premise | full-text (S24-behaviour.md) |
| Target taxi speed | 1.95 m/s (3-BL wing) | S24 | full-text |
| Peak-to-peak tail amplitude | A = 0.20 TL = 8 mm | S24 **assumption** (calibrated at Ucrit with St 0.3) | full-text |
| Measured frequency maximum | 52 Hz (escape), 21 Hz (steady) | Kyriakatos et al. 2011, as cited by S24 | relayed by S24; not read by me |
| Kinematic viscosity | ν = 1.0 × 10⁻⁶ m²/s | my **assumption** (water ~20 °C) | — |
| Zebrafish tail span h/L | **unknown**. Bracketed as 0.15-0.30, central 0.20-0.25 | my **assumption**, inside Eloy's 0.05-0.35 range | I did not search for a zebrafish caudal-fin span measurement |

**Check on the transcription.** Eloy's eq. 16 with the table's S/h² reproduces the table's Li
for rainbow trout (0.066 vs 0.067), juvenile trout (0.185 vs 0.184), Atlantic silverside (0.222
vs 0.224) and bullfrog tadpole (0.193 vs 0.193). So Li = (S/h²)·C_d, with **no factor of ½**.
The library's `contested_by` line writes Li = (S/h²)·C_d/2, which is a transcription error in the
library entry. It changes St_opt by 2^(1/3) = 1.26×. For the goldfish-morph rows, Eloy states
that he used Blake's fitted drag instead. Eq. 16 gives 0.334 for the Eggfish, against the
table's 0.538. That is why those rows sit high: the morphs were "selected artificially for
aesthetic reasons, and as a result have a relatively large drag" (Eloy). They are poor analogues
for a wild-type fish.

## 2. Arithmetic, all calculated

Re = U·L/ν = 1.95 × 0.04 / 1e-6 = **7.80 × 10⁴**

C_d = max(2.656 / √78 000, 0.072 / 78 000^0.2) = max(2.656/279.3, 0.072/9.52) = max(0.00951, 0.00757) = **0.00951**

S/h² = 0.4 / (h/L)²

| h/L | S/h² | Li = (S/h²)·C_d | St = 0.75·Li^(1/3) | f = St·U/A (Hz) | f / 52 Hz |
|---|---|---|---|---|---|
| 0.15 | 17.78 | 0.169 | 0.415 | 101 | 1.94 |
| 0.20 | 10.00 | 0.095 | 0.342 | 83 | 1.60 |
| 0.25 | 6.40 | 0.061 | 0.295 | 72 | 1.38 |
| 0.30 | 4.44 | 0.042 | 0.261 | 64 | 1.23 |

The same model at S24's other speeds, at h/L = 0.20 (calc):

- **0.548 m/s** (Re 2.2e4): Li 0.179, St 0.42.
- **0.84 m/s** (Re 3.4e4): St 0.39.
- **5.84 m/s** (Re 2.3e5): St 0.30, so f = 215 Hz, or 4.1× the 52 Hz maximum.

So the model *does* put a slow-swimming zebrafish above the band, but not at taxi speed.

For comparison, these are frequencies that assume St does not depend on speed (calc, A = 8 mm,
U = 1.95 m/s): St 0.20 → 49 Hz; 0.30 → 73 Hz; 0.54 → 132 Hz; 0.79 → 193 Hz; 1.02 → 249 Hz.

Script: `docs/research/fish/replicate-52_calcs.py` (run `python3 -I` on it).

## 3. Uncertainty, and what it does not cover

- **Tail span is the dominant unknown.** St varies as h^(-2/3). The bracket 0.15-0.30 L is an
  assumption, not a measurement.
- **The fit is not the data.** The power law approximates Eloy's *model* optimum. Observed
  animals scatter around it. Eloy's "acceptable range" (efficiency within 0.1 of the maximum) is
  a band in his Fig. 4, but I did not read numbers off that figure. For example, the fit gives
  0.30 for 20 cm trout against an observed 0.26, and 0.45 for silverside against an observed 0.27.
- **Real drag is higher.** Eloy says eq. 16 "is usually an underestimate". A higher C_d raises
  Li and St. Doubling C_d raises St by 1.26×, which would put the central value at 0.37-0.43, or
  91-105 Hz.
- **The model is outside its stated validity.** Eloy's theory assumes steady cruising and an
  elongated body, but S24's case is surface taxiing with a partly submerged lobe, near the
  water's surface, during acceleration. No source I read covers that.
- **A stays fixed.** A = 8 mm is held as S24 had it, so that only St varies.

## 4. My inference, separated from the sources

Eloy's model, his drag law and his body-form defaults are all from Eloy. Applying them to a
zebrafish at 1.95 m/s is **my** step. From it I infer three things:

1. The correct move from "small swimmers sit above the band" is to recompute Li at the operating
   Re. Transplanting a taxon's St is not.
2. At 1.95 m/s that recomputation lands in the upper part of 0.2-0.4, not at 0.54-0.8.
3. S24's 49-73 Hz (St 0.2-0.3) is therefore a modest underestimate. It is not a 2-3× one.

S24's qualitative conclusion (a sustained 1.95 m/s taxi exceeds every measured adult tail-beat
frequency) is unchanged and slightly strengthened.

## 5. Comparison with the recorded value (read only after §1-§4)

**The recorded claim** (quoted in `challenge-52.md`, branch
`origin/claude/strouhal-zebrafish-challenge-a41f13`, read level full-text): "a 4 cm zebrafish is
that case, so the required tail-beat frequency is 132-199 Hz, not 49-73 Hz, and the shortfall
against the 52 Hz measured maximum is 2.5-3.8x". It is recorded as derived, value 2.5 (ratio).

**Mine:** 72-83 Hz (64-101 Hz), a ratio of 1.4-1.6× (1.2-1.9×).

**Verdict: DISAGREE.** My upper bracket (101 Hz, 1.9×) is below the claim's lower bound
(132 Hz, 2.5×).

My 132 Hz and 193 Hz rows (St 0.54 and 0.79) reproduce the claim's arithmetic. The disagreement
is over the input. The claim takes St from goldfish/tadpole rows at Re ~1e4. I take St from
Eloy's own Li-scaling at Re 7.8e4.

**Other evidence the challenge reports, kept separate.** The challenge independently reached a
partly overlapping position by another route. It got 75 Hz (1.4×) under the Palstra-Ucrit
calibration. It also notes that it did *not* compute Eloy's Li, "because I have no zebrafish
C_d". I used Eloy's own eq. 16 for C_d, which closes that gap. The two derivations differ in
method, and they agree only on the Palstra branch.

The challenge also reports a **measured** St for adult zebrafish of 0.366 (cruising) and 0.515
(burst) in the semi-amplitude convention, from Mwaffo et al. 2017 *PeerJ* 5:e4041, at Re ~1e3.
That is ≈ 0.73 and 1.03 peak-to-peak. I have **not read** Mwaffo, so for me it is
could-not-access (relayed by challenge-52 only). If correct, it shows real zebrafish exceed
Eloy's power law at low Re. Eloy's model gives ≈ 0.42-0.51 at Re 2e4 for h = 0.20-0.15 L.
Mwaffo's data do not measure St at 1.95 m/s, and neither does anything I read. That
disagreement is preserved, not averaged. The challenge's Wakamatsu-calibrated 173 Hz branch
sits inside the claim's range and outside mine. My method does not use Ucrit at all, so it
cannot adjudicate that branch.

**Negative-search scope.** I did not search for zebrafish caudal-fin span, zebrafish C_d, or any
zebrafish kinematics at U > 1 m/s. My sources were Eloy's arXiv preprint and S24's files. The
claim-id search across remote branches was stopped before it finished, and challenge-52 was
found by grepping `docs/research/fish/`, `findings/` and `ledger/` for "goldfish".

```swarm-replication
{"claim_id": 52, "my_value": "72-83 Hz required at 1.95 m/s (bracket 64-101 Hz), i.e. 1.4-1.6x (1.2-1.9x) the 52 Hz maximum, from Eloy St_opt = 0.75 Li^(1/3) = 0.30-0.34 (0.26-0.42) at Re 7.8e4; calculated, not observed", "agrees": false,
  "note": "Recomputing Eloy's Lighthill number at the taxi operating point (Re 7.8e4, Li=(S/h^2)Cd with Eloy's own Cd law) puts a 4 cm zebrafish at St ~0.3-0.34, not the goldfish/tadpole 0.54-0.8, so the required frequency is ~72-83 Hz rather than 132-199 Hz."}
```
