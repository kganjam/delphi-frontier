# Replication of claim 184 (S10-D): hover power per kg of pectoral muscle at a measured teleost muscle fraction

**What this is.** I re-derived the number myself and did not read the deriving agent's working. The branch `origin/claude/deepen-s10-flapping-muscle-wr33g7` holds `S10-deepen.md` and `S10_deepen_calc.py`. I saw only their file names, through `git diff --stat`, and opened neither. For the aerodynamic inputs I read §3a–3c of the *original* S10 file (`origin/claude/s10-tissue-flapping-power-2kag3x:docs/research/fish/S10-tissue.md`). That file computes the requirement for f = 0.1–0.3, not for the measured fraction. I checked the muscle-fraction value against the primary source myself.

## My value

**Computed, not observed:** with pectoral muscle at 1.38% of body mass (both fins of *Abudefduf saxatilis*), the hover requirement is **≈730–1950 W/kg of muscle**. The range spans S10's design cases, from the most generous (R = 4 cm, M = 1.5) to the least generous (R = 2 cm, M = 2.0).

That is **5.4–14.5×** the measured 134 W/kg of warm larval zebrafish fast muscle. It is also above the highest in-vitro vertebrate value in S10's list, 433 W/kg for quail pectoralis.

Uncertainty and extra cases, all computed:
- If the muscle of only one fin counts (0.69%), the range is 1460–3890 W/kg.
- Charging only the swept disc (stroke Φ = 120°, so A × 2/3) raises the most generous case from 730 to 894 W/kg.
- The aerodynamic model is momentum theory with an assumed profile multiplier M. Its uncertainty is not quantified beyond the M = 1.5–2.0 bracket.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Body mass m | 0.4 g (W = 3.924 × 10⁻³ N) | S10 design assumption (S10-tissue.md §3a) | full-text (repo file) |
| Air density ρ | 1.2 kg/m³ | standard value, used by S10 | n/a |
| Semispan R; disc A = πR² | 2 cm or 4 cm | S10 design assumption | full-text (repo file) |
| Induced-power factor k | 1.2 | S10 assumption | full-text (repo file) |
| Profile multiplier M | 1.5 or 2.0 | S10 assumption | full-text (repo file) |
| Pectoral muscle / body mass, *A. saxatilis* | abductor superficialis 0.13 + abductor profundus 0.23 + adductor superficialis 0.15 + adductor profundus 0.18 = **0.69% per appendage** (bold "Total") | Mansuit & Herrel 2021, *Front. Ecol. Evol.* 9:702576, Table 1. I read the table image (fevo-09-702576-t001.jpg) from frontiersin.org. The footnote says the bold values are the sum of the muscle groups "of the appendage". The article text says the fish values are "per appendage". | full-text (the table image itself, plus the JATS XML of the article) |
| Both fins | 2 × 0.69 = 1.38% → f = 0.0138 | my inference: it assumes bilateral symmetry | — |
| Warm zebrafish fast-muscle power | 134.4 ± 19.9 W/kg at 80 Hz, 28 °C, larval (5 dpf) myotome | Mead et al. 2020, *Biophys J* 119:806, PMC7451861. Quote: "maximal net power … was produced at 80 Hz (134.4 ± 19.9 W/kg)" | full-text (the first 100k of 120k characters, via an automated summarising fetch) |
| Quail pectoralis in vitro | 433 W/kg (highest value) | Askew & Marsh 2001, as listed in S10 | search-summary (S10's read-level; I did not re-check it) |

Table 1 also has a row for *Latimeria chalumnae* at 0.43% per pectoral appendage. The other fish rows give PCSA, not mass fractions. The table gives **no zebrafish (*Danio*) value**. I did not search separately for a zebrafish pectoral muscle mass, so the zebrafish value is `unknown`. Being a damselfish, *A. saxatilis* is a labriform (pectoral-fin) swimmer. My inference, not a measurement: zebrafish probably have a fraction no larger than this, which would make the requirement higher.

## Arithmetic

P_ind = k·√(W³/(2ρA)); required power per kg of muscle = M·P_ind/(m·f), with f = 0.0138.

- W³ = (3.924 × 10⁻³)³ = 6.04 × 10⁻⁸ N³
- R = 4 cm: A = 5.027 × 10⁻³ m². 2ρA = 1.206 × 10⁻². √(6.04 × 10⁻⁸ / 1.206 × 10⁻²) = 2.238 × 10⁻³ W. × 1.2 = **2.686 mW**, which is 6.71 W/kg body.
- R = 2 cm: A = 1.257 × 10⁻³ m², giving **5.371 mW**, which is 13.43 W/kg body.
- m·f = 0.4 × 10⁻³ × 0.0138 = 5.52 × 10⁻⁶ kg of muscle.

| R | M | W/kg muscle (f = 1.38%) | f = 0.69% (one fin) |
|---|---|---|---|
| 4 cm | 1.5 | 1.5 × 2.686 / 5.52 × 10⁻³ = **730** | 1460 |
| 4 cm | 2.0 | **973** | 1946 |
| 2 cm | 1.5 | **1460** | 2919 |
| 2 cm | 2.0 | **1946** | 3892 |

Ratios to 134 W/kg: 730 / 134 = 5.4 and 1946 / 134 = 14.5. To reach the requirement with 134 W/kg tissue, pectoral muscle mass would have to grow about 5.4–14.5×, to about 7.5–20% of body mass. That is a computed requirement, not a measured feasibility.

## Verdict (inference)

These are computed values. Even with the most generous geometry, the requirement is 5–15× the best measured warm fish fast muscle and above every listed vertebrate muscle. Sustained flapping is impossible: aerobic red muscle gives about 5–10 W/kg (S10 §2a, search-summary). Burst flapping also fails for present anatomy.

## Comparison with the recorded value

I compared only after finishing the work above. The recorded value appears in the question text: "~730–1950 W/kg muscle, 5–15× above measured warm zebrafish fast muscle". Mine is 730–1946 W/kg and 5.4–14.5×. **AGREE.**

Caveat on how independent this is. The aerodynamic inputs (m, R, k, M) are S10's design assumptions, which both derivations share, so this agreement tests the arithmetic and the f value, not the aerodynamic model. I did independently confirm the f input against the primary table: 0.69% per fin, and the sum of the four muscles matches.

```swarm-replication
{"claim_id": 184, "my_value": "730-1946 W/kg pectoral muscle (computed; f = 1.38% body mass, both fins of A. saxatilis; 5.4-14.5x the 134 W/kg warm zebrafish fast muscle)", "agrees": true,
  "note": "Re-checked Mansuit & Herrel 2021 Table 1 (0.69% per appendage = 0.13+0.23+0.15+0.18) and recomputed momentum-theory hover power on S10's shared geometry assumptions; the agreement checks the arithmetic and f, not the shared aerodynamic model."}
```
