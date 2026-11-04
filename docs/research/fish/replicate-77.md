# Replicate 77: S10-D verdict "STRENGTHENS" (zebrafish flapping-flight muscle)

Branch `claude/s10-d-verdict-qcqxez`. This is an independent re-derivation from primary sources.

## Disclosure: I saw the recorded result before I finished

To find out what S10-D is about, I ran `grep` over `docs/research/fish/S10-deepen.md` (on branch
`origin/claude/deepen-s10-flapping-muscle-wr33g7`) for its headings and the word "Mansuit". That grep
also printed the verdict line and the summary block: ~1.4% pectoral muscle, **~730–1950 W/kg muscle**,
5–15× above zebrafish fast muscle, verdict STRENGTHENS. I stopped there. I did not read the rest of
that file, its `S10_deepen_calc.py`, or `S10-tissue.md`. So this re-derivation is **not blind to the
headline number**. Its inputs and arithmetic are my own, and they lead to a different number (below).

## The question as I reconstruct it

S10 asked whether zebrafish could fly by flapping their pectoral fins. S10-D tests the input the
answer depends on most: the fraction of body mass in the flight (pectoral) muscle, f. The question
is whether a measured value of f confirms ("strengthens") the S10 conclusion that sustained flapping
is impossible and burst flapping is out of reach.

## Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| 1 | Pectoral-fin muscle mass / body mass, *Abudefduf saxatilis* (sergeant major damselfish) | 0.13+0.23+0.15+0.18 = **0.69%** (the total matches the table) | Mansuit R & Herrel A (2021) *Front Ecol Evol* 9:702576, doi:10.3389/fevo.2021.702576, Table 1 | **full-text** (I downloaded the PDF from frontiersin.org and read Table 1 after `pdftotext -layout`) |
| 2 | Is 0.69% one fin or both? | **One fin** (inference) | Same paper, Results: "the summed muscle mass of each fin represents less than 1% of the total body mass" | full-text. This is the authors' wording; reading it as "per fin" is my inference. Mansuit & Herrel took the actinopterygian data from Thorsen & Westneat (2005), which I did **not** access |
| 3 | So f for both pectoral fins | **1.38%** (2 × 0.69). If 0.69% is actually both fins, f = 0.69% | arithmetic on 1–2 | — |
| 4 | Best vertebrate muscle power over a full cycle | ~390 W/kg muscle on average, ~530 W/kg in one bird; often quoted as "~400 W/kg, the highest measured" | Askew, Marsh & Ellington 2001 *J Exp Biol* 204:3601; Askew & Marsh 2001 *J Exp Biol* 204:3587 | **search-summary** only |
| 5 | Adult zebrafish body mass | assumed 0.25 / **0.4** / 0.6 g | **unknown** from primary sources. One standard web search found no table pairing mass with fin length. These are my assumed values, not observations | — |
| 6 | Pectoral fin length R | assumed 4 / **5** / 6 / 8 mm | **unknown** (same search). Assumed | — |
| 7 | Swept area A = Φ·R² for the fin pair | Φ = 2 rad, or π (a full disk) | modelling assumption | — |
| 8 | Ratio of real to ideal hover power, k (non-ideal induced power plus profile power) | 1.0 / **1.2** / 2.0 | modelling assumption | — |
| 9 | Air density ρ, gravity g | 1.2 kg/m³, 9.81 m/s² | standard | — |

## Arithmetic (a calculation, not an observation)

I used momentum (actuator-disk) theory for hovering:

- induced velocity v_i = √(m·g / (2ρA))
- power per kg of body P_b = k·g·v_i
- power per kg of muscle P_m = P_b / f

Central case: m = 0.4 g, R = 5 mm, Φ = π, so A = π·25e-6 = 7.85e-5 m².

- v_i = √(3.924e-3 / (2·1.2·7.85e-5)) = √20.8 = 4.56 m/s
- Ideal P_b = 9.81 × 4.56 = 44.8 W/kg body. With k = 1.2, P_b = 53.7 W/kg body
- P_m = 53.7 / 0.0138 = **3,890 W/kg muscle**

Full grid: 3 masses × 4 fin lengths × 2 values of Φ × 3 values of k. The script is `replicate-77_calc.py`.

- P_b ranges from 22 to 172 W/kg body
- With f = 1.38%: P_m = **1,600 – 12,400 W/kg muscle** (central 3,900)
- With f = 0.69% (if the table value is both fins): P_m = 3,200 – 24,900 W/kg muscle

Compared with ~400 W/kg (input 4, search-summary), the requirement is **~4× to ~30×** the best
vertebrate muscle at f = 1.38%. That means a ~4–30× larger pectoral muscle would be needed, even at
burst power. Every point in the grid is above 400 W/kg, so the conclusion does not depend on my
unsourced mass and fin-length guesses within these ranges.

**My value:** hover requirement ≈ 3.9 × 10³ W/kg pectoral muscle (range 1.6–12 × 10³ W/kg) at
f = 1.38% (calculated). Verdict: **STRENGTHENS**. The measured proxy for f confirms that flapping
hover is impossible with present anatomy.

## Comparison with the recorded value

- **Verdict: AGREE.** STRENGTHENS, the f ≈ 1.4% proxy, and the source table all match what I found.
  I confirmed independently that Table 1 gives 0.69% for *A. saxatilis*.
- **Number: partial DISAGREEMENT.** The recorded figure is ~730–1950 W/kg muscle. Mine is
  1,600–12,400 W/kg (central ~3,900). The ranges overlap only at 1,600–1,950. The recorded range
  implies about 10–27 W/kg of body for hover. To get that from actuator-disk theory, a 0.4 g fish
  would need a swept area roughly 3–20× larger than any of my geometries. Without reading the
  upstream inputs of S10 I cannot say whether they use different fin dimensions, partial weight
  support, or something else. I leave this disagreement open rather than averaging it.
  The two derivations disagree in the direction that makes infeasibility stronger, so this does not
  threaten the verdict.

## What this does not establish

- No zebrafish pectoral muscle mass was found. *A. saxatilis* is a labriform (pectoral-fin) swimmer
  and is a proxy species. Scope of the negative search: one standard web search for zebrafish body
  mass and pectoral-fin morphometrics. I did not search for zebrafish pectoral muscle mass
  specifically.
- Zebrafish body mass and fin length are assumptions, not sourced values.
- The muscle-power ceiling rests on a search-summary of the quail papers, not the full text.
- I did not check Thorsen & Westneat (2005), the underlying source for the 0.69% value.

## Sources

- Mansuit & Herrel 2021, https://www.frontiersin.org/articles/10.3389/fevo.2021.702576/pdf — full-text (Table 1, Results)
- Askew, Marsh & Ellington 2001, J Exp Biol 204:3601 — search-summary
- Askew & Marsh 2001, J Exp Biol 204:3587, https://cob.silverchair.com/jeb/article-split/204/21/3587/32912/The-mechanical-power-output-of-the-pectoralis — search-summary
- Thorsen & Westneat 2005 — could-not-access (not attempted)

```swarm-replication
{"claim_id": 77, "my_value": "~3.9e3 W/kg pectoral muscle required for hover (range 1.6e3-1.2e4 W/kg at f=1.38% from Mansuit & Herrel 2021 Table 1), >=4x the ~400 W/kg vertebrate ceiling; verdict STRENGTHENS", "agrees": true,
  "note": "Verdict and the 0.69%/fin proxy agree (independently read from Table 1), but my calculated power requirement is ~2-6x higher than the recorded 730-1950 W/kg, a disagreement in the direction that only strengthens infeasibility; I saw the recorded headline via grep before deriving."}
```
