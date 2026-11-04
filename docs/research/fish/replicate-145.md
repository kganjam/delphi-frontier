# Replication of claim 145 (S24-D-D): the 52 Hz ceiling, re-derived independently

**My value (calc).** The adult escape-frequency ceiling for a 40 mm zebrafish is **~39–52 Hz**.
If the 52 Hz maximum came from a mid-sized fish (24 mm) and frequency scales as L^-1, the
floor drops to ~31 Hz. The 3-BL taxi shortfall f_req/f_max then widens from **1.17–1.56×** to
**1.17–2.1×**, or up to 2.6× at that most pessimistic floor. All of these are calculations.
None is an observation.

## What I did and did not read

- **Read** (inputs only): `docs/research/fish/S24-behaviour.md` and `S24_calcs.py` on branch
  `claude/s24-surface-taxiing-launch-tsepbn`. Section 3.2 gives the original S24 model.
- **Read** (inputs only): the claim-85 challenge (`challenge-85.md`, branch
  `claude/s24-deepen-verdict-challenge-j52cqu`). It fixes the S24-D stride model used here:
  f_req = U/(λL), with U = 1.95 m/s, L = 40 mm and λ = 0.6–0.8.
- **Not read:** `S24-D-deepen.md` and `S24-D-deepen_calc.py` on the context branch
  `claude/deepen-s24-sensitive-input-ls0g3m`, and `challenge-145.md`. I listed their file
  names only and stopped there.
- **Caveat on blindness.** The question text itself states the claimed values (36–52 Hz and
  1.2–2.3×). So this derivation is independent in its sources and arithmetic, but it was not
  blind to the target.

## Inputs, sources and read-levels

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| 1 | Max escape EMG frequency, intact adults | "Across animals, the maximal frequency reached during escape was 52 Hz" | Kyriakatos et al. 2011, *J. Neurosci.*, PMC6623330 | full-text (first 100,000 of 101,006 characters, via WebFetch summariser with quotes) |
| 2 | Typical escape frequency | "ranging from 30 to slightly >40 Hz"; "never ... lower than 29 Hz" | same | full-text (same) |
| 3 | Animal size | "8–15 weeks old (body length 18–30 mm)". The intact EMG set is n = 8 | same | full-text (same) |
| 4 | Temperature | Only the **in vitro** perfusion is given (20–22 °C). No water temperature is stated for the in vivo EMG recordings. The fish were held in a 0.35 × 0.25 × 0.25 m aquarium | same | full-text (same). A direct query found no in vivo temperature |
| 5 | Fast-fibre Ca²⁺ fusion | indo-1 ratio: half fusion at **53 ± 3 Hz**, 95 % at 156 ± 9 Hz. As [Ca²⁺]: 95 % at 186 ± 6 Hz. Room temperature 20–22 °C; fibres isolated from males aged 11–13 months, body size not reported | Idoux et al. 2022, *J. Gen. Physiol.* 154(9):e202213158, PMC9247716 | full-text (first 100,000 of 103,758 characters, via summariser). rupress.org is blocked by the network policy |
| 6 | Escape peak Reynolds number | 27,800 ± 2140 s.e.m. at 1 mPa·s; TL 33.0 mm | Danos & Lauder 2012, as recorded in S24-behaviour.md | **listing**: I took this from the repo table and did not re-read the paper |
| 7 | Stride per beat λ | 0.6–0.8 L | Wardle 1975, *Nature* 255:725 | search-summary |
| 8 | Size dependence | "contraction time increases with the length of the fish and decreases with increase of temperature" | secondary summaries of Wardle 1975 | search-summary. **I found no exponent**, so the exponent b below is an assumption |
| 9 | Taxi target | U = 1.95 m/s (3-BL wing), L = 40 mm | S24 project premise | repo |

## Arithmetic (calc)

**Required frequency, f_req = U/(λL)**, with 1.95 m/s and L = 0.040 m:

| λ | f_req |
|---|---|
| 0.8 | 60.9 Hz |
| 0.6 | 81.25 Hz |
| 1.0 (corner) | 48.75 Hz |

**Ceiling for a 40 mm fish.** I start from 52 Hz, which is measured in fish of 18–30 mm. I
scale it as (L_src/40)^b, where b is an assumption and not a measured value:

| L_src (fish that set the max) | b = 0 | b = 0.3 | b = 0.5 | b = 1.0 |
|---|---|---|---|---|
| 30 mm | 52 | 47.7 | 45.0 | 39.0 |
| 24 mm | 52 | 44.6 | 40.3 | 31.2 |
| 18 mm | 52 | 40.9 | 34.9 | 23.4 |

The paper reports "never lower than 29 Hz" across fish up to 30 mm. That makes the
18 mm / b = 1 corner (23 Hz) implausible (inference). The direction of the size effect comes
from input 8, so 52 Hz is an upper edge. I give **39–52 Hz** as the range, which assumes the
max came from a fish of about 30 mm and that b ≤ 1. The floor is soft, and could be as low as
~31 Hz.

**Cross-check A: Danos & Lauder.** U = Re·ν/L.
- With TL 33 mm, U = 0.842 m/s. Then f = U/(λL) = **31.9–42.5 Hz** for λ 0.8–0.6, or
  29.5–45.8 Hz across ±1 s.e.m.
- With the length taken as SL ≈ 26.4 mm, the same arithmetic gives 49.9–66.5 Hz.
- So this check only constrains the ceiling to ~30–67 Hz. It does not discriminate sharply.
  That is my reading, and it is weaker than "agrees".
- Stride λ during a C-start is not well defined (inference).

**Cross-check B: Idoux.** Fast-fibre Ca²⁺ half fusion is at 53 Hz at 20–22 °C. Cyclic
alternating activation should stay below substantial fusion. Force relaxation is slower than
Ca²⁺, so a force-based limit would be lower still. Both points are inference. This check
therefore bounds the ceiling from above at about 53 Hz at room temperature, consistent with
52 Hz. These fibres come from 11–13-month fish of unreported size.

**Shortfall f_req/f_max:**

| ceiling | λ 0.8 | λ 0.6 | λ 1.0 |
|---|---|---|---|
| 52 Hz | 1.17 | 1.56 | 0.94 (closes) |
| 45 Hz | 1.35 | 1.81 | 1.08 |
| 39 Hz | 1.56 | 2.08 | 1.25 |
| 31 Hz | 1.97 | 2.62 | 1.57 |

So the shortfall widens from 1.17–1.56× to **1.17–2.08×** (up to 2.6× at the soft floor). The
λ = 1.0 corner closes only if the ceiling is at least 48.75 Hz.

**Temperature (open, calc).** The in vivo temperature is unknown. Suppose the recordings were
made at about 20–22 °C (Idoux's cross-check temperature), while the fish operated at 26–28 °C,
a ΔT of 4–8 °C. Q10 values of 1.2–2.1 would then lift 52 Hz to **56–94 Hz**. With ΔT = 6 °C the
range is 58–81 Hz. That would reopen the case. This is untested: the temperature is
`unknown`, and I asked the full text for it directly.

## Comparison with the recorded value

The question states 36–52 Hz and a 1.2–2.3× shortfall.
- **Upper edge.** It is identical (52 Hz, 1.17×).
- **Lower edge.** Mine is 39 Hz (2.1×), against their 36 Hz (2.3×). Both lower edges depend
  on an assumed size or typical-escape discount, not on a measurement. 36 Hz lies inside my
  31–39 Hz soft-floor band.
- **Source facts.** I confirmed every factual input the claim cites at full-text level: n = 8
  intact animals, 18–30 mm, escapes 30 to slightly above 40 Hz, max 52 Hz, no in vivo
  temperature, and Ca²⁺ half fusion at 53 Hz.
- **One qualification.** The 53 Hz half fusion is an indo-1 ratio index measured in vitro at
  20–22 °C. The 95 % fusion values are 156–186 Hz.
- **Danos & Lauder.** My Danos-based range (32–43 Hz on TL, 50–67 Hz on SL) brackets their
  "~32–53 Hz" but does not match it exactly. I could not tell which length basis they used.
- **Verdict.** Their wording, "strengthening 'not shown to close'; 'not refuted' rests on
  temperature and the λ = 1.0 corner", follows from my numbers too.

**AGREE**, within the assumption-dependent lower bound.

```swarm-replication
{"claim_id": 145, "my_value": "ceiling ~39-52 Hz for a 40 mm fish (soft floor ~31 Hz); 3-BL taxi shortfall 1.17-2.1x (to 2.6x at floor), calc", "agrees": true,
  "note": "Same 52 Hz upper edge and the same source facts confirmed at full text; my lower edge (39 vs 36 Hz, 2.1x vs 2.3x) rests on an assumed size exponent, and the question text exposed the target, so the derivation was not blind."}
```
