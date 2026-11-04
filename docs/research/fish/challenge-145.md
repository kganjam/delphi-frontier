# Challenge 145: adversarial review of S24-D-D (the 52 Hz frequency ceiling)

**Claim under review** (S24-D-D, branch `claude/deepen-s24-sensitive-input-ls0g3m`,
`docs/research/fish/S24-D-deepen.md`, recorded evidence level *derived*). S24-D's 3-BL verdict is
most sensitive to the 52 Hz ceiling. Read at source, 52 Hz is an EMG maximum across 8 adults of
18–30 mm, measured at an unreported temperature. Two cross-checks agree with it. The improved
ceiling for a 40 mm fish is ~36–52 Hz, and the taxi shortfall widens from 1.2–1.6× to 1.2–2.3×.
Verdict: strengthens.

**Outcome: WEAKENED.** The verdict direction survives: S24-D's "not shown to close" is not
undermined, and I found one more fact that supports it (§3). The **key number** does not survive as
stated:

- The low end of the "~36–52 Hz ceiling" (36 Hz) comes from a frequency a fish *achieved*, not from
  a ceiling.
- One of the "two cross-checks that agree" carries no information on the project's own stride range.
- "Escapes typically 30 to slightly >40 Hz" is the range of one animal.

So the upper end of the widened shortfall, 2.3×, is not established.

This was a desk review. I ran no experiment. Every number is tagged **measured** (literature, with
read-level), **calc** (my own arithmetic, redone independently with Python one-liners) or
**assumed**.

## 1. Arithmetic, redone independently (all calc)

I recomputed from the stated inputs: U = 1.95 m/s, L = 0.040 m, λ = 0.6–0.8 L/beat, f_req = U/(λL).

- **f_req** = 60.9 Hz (λ 0.8) and 81.25 Hz (λ 0.6). The ratio to 52 Hz is 1.17–1.56. **Matches.**
- **Break-even f_max** = 61–81 Hz, a rise of 17–56 %. **Matches.**
- **Break-even λ** = U/(52·L) = 0.94. **Matches.** At λ = 1.0, f_req = 48.75 Hz. **Matches.**
- **Ratio at f_max 36 Hz** = 1.69–2.26. At 30 Hz, 2.03–2.71. At 42 Hz, 1.45–1.93. At 45 Hz,
  1.35–1.81. **All match.**
- **Size correction**: 52·(30/40)^b = 52 / 45.0 / 39.0 Hz, and 52·(18/40)^b = 52 / 34.9 / 23.4 Hz,
  for b = 0 / 0.5 / 1. **Matches.**
- **Q10 needed** = (f_req/52)^(10/ΔT): 1.22 (61 Hz, ΔT 8 °C) up to 2.10 (81 Hz, ΔT 6 °C).
  **Matches 1.2–2.1.**
- **Danos & Lauder speed**: Re·ν/L = 27,800 × 10⁻⁶ / 0.033 = 0.842 m/s (TL). Using SL ≈ 0.8 TL =
  26.4 mm (assumed ratio) gives 1.053 m/s. **Matches 0.84 / 1.05.**

I found no arithmetic error.

## 2. Faults

### 2.1 Check A does not bound the ceiling, and on the project's own λ range it gives 26–66 Hz (calc)

Check A divides a measured peak speed by an *assumed* stride. That produces a frequency the fish
*reached*. It is not a frequency the fish *cannot exceed*, so it cannot confirm a ceiling. A
peak-speed-implied frequency can only be a lower bound on the ceiling (assuming the stride holds).

The author restricts λ to 0.6–0.8. The project's sourced range, accepted in challenge 85 and quoted
in the S24-D-D document itself, is λ 0.48–1.0. Over that range, check A gives:

- TL basis (0.842 m/s, 33 mm): 0.842/(1.0·0.033) to 0.842/(0.48·0.033) = **25.5–53.2 Hz**;
- SL basis (1.053 m/s, physical stride per 33 mm TL): **31.9–66.5 Hz**.

These are calc. The 66 Hz end is above 52 Hz and inside the 61–81 Hz requirement band.

There is a second ambiguity. If the 0.6–0.8 stride is read per *SL*, the same length the Re was
computed on, then check A at λ 0.6–0.8 gives **49.9–66.5 Hz** (calc).

The S24-D-D document concedes that check A is "not independent of λ". The claim still lists it as
one of "two cross-checks [that] agree". It does not agree. It is uninformative about the ceiling.

### 2.2 The 36 Hz floor of the "improved ceiling" is check A's value

The table in S24-D-D §4 takes its 36 Hz row from check A at λ 0.7, TL basis. Per §2.1, that is an
achieved frequency under an assumed stride. The other values below 52 Hz have weak bases too:

- 42 Hz and 30 Hz describe **one animal's** distribution (Fig. 4D) and its bottom. They are not
  ceilings.
- 39–45 Hz is the size correction with an **assumed** exponent b. I verified that b is unsourced:
  the S24-D-D document says it found no zebrafish exponent.

The only *measured* ceiling is 52 Hz, a maximum across animals. Everything below it rests on an
assumed b or on a non-ceiling statistic.

**Corrected key number:** adult zebrafish escape EMG burst frequency ceiling **≤ 52 Hz** (measured
upper bound, 18–30 mm fish, temperature unreported). Its value at 40 mm is **unknown** within about
23–52 Hz. That range is the assumed-b span of 0–1, taken over the unknown body size (18–30 mm) of
the fish that produced the 52 Hz reading. The 36 Hz floor is not established. The shortfall is
therefore **≥ 1.17–1.56×** at the recording temperature (calc), and its upper end is unbounded by
the evidence. "1.2–2.3×" presents an assumption-driven span as an improved estimate.

### 2.3 Wording: "escapes typically 30 to slightly >40 Hz"

**Measured** (Kyriakatos et al. 2011, PMC HTML, read-level full-text, my own read):

- "ranging from 30 to slightly >40 Hz (Fig. 4D, black bars)" refers to the single-animal panel. The
  caption reads "Distribution of the burst frequency ... in a single an[imal]".
- Across the 8 animals, escape ran "from ∼30 Hz toward faster frequencies", with a maximum of 52 Hz.

The S24-D-D body says "example animal". The claim's summary upgrades this to "typically". That is a
minor defect, but it is the step that lets a single-animal range stand in for a typical ceiling.

## 3. Proxy and hidden assumption, tested

- **Proxy.** 52 Hz is an EMG burst frequency standing in for tail-beat frequency. I verified at
  source that the electrodes were placed "caudal and dorsal to the pectoral fin", which is anterior
  myotome, not the tail.
  - *Inference, mine:* this gives the cycle frequency of the body wave, but it cannot show
    tail-tip amplitude at that frequency. The S24-D-D document says the same. This is not a new
    fault.
- **New fact the author missed, which supports the verdict direction.** Kyriakatos et al. 2011
  (full-text, my read) state that escape sequences "consisted of a few, in general three to five,
  short cycles".
  - S24 §3.4 needs the frequency held for 12–46 beats. That figure is inherited and I did not
    re-derive it.
  - The 52 Hz maximum therefore comes from bursts of 3–5 cycles. *Inference, mine:* no measured
    value shows any frequency of 30 Hz or more being held for 12 beats or longer.
  - This supports "not shown to close" more strongly than any of the S24-D-D cross-checks.
- **Temperature.** I verified that the temperature is not reported for the in vivo recordings. The
  only temperature in the paper is "fish saline at 20–22°C" for the in vitro preparation. The
  20–22 °C used for the Q10 corner is therefore an **assumption**, as S24-D-D says.
- **Published Q10s the author did not search for** (author's scope: "did not search for it
  specifically"). A search summary (read-level: **search-summary**, primary not read) of a sculpin
  fast-start study (pure.uhi.ac.uk record, "Swimming kinematics of fast starts are altered by
  temperature acclimation") reports two kinds of Q10:
  - an acclimation Q10 of 2.2 for stage-1 duration;
  - acute-change Q10s of about 1.1–1.2.

  With those inputs I calculated:
  - acute Q10 of 1.1–1.2 over 6–8 °C: 52 Hz rises only to 55–60 Hz, short of the 61 Hz break-even;
  - acclimation Q10 of 2.2: 52 Hz rises to 83–98 Hz, which clears it.

  Both rates are from another taxon, and they disagree. I preserve the disagreement and do not
  average it. The temperature corner is therefore **two-sided and unresolved**. It is not "a Q10 of
  only 1.2–2.1". The S24-D-D statement that "not refuted" rests on temperature remains accurate.

## 4. Counter-example search (scope)

I ran two standard web searches:

- "adult zebrafish tail beat frequency temperature Q10 swimming kinematics";
- "adult zebrafish C-start escape kinematics high-speed video tail beat frequency Hz".

I also read the full text of Kyriakatos 2011 (PMC HTML). Europe PMC XML returned HTTP 500, and
jneurosci.org was blocked by the proxy.

**No adult zebrafish kinematic tail-beat frequency above 52 Hz was found, and no adult zebrafish
Q10 for tail-beat frequency was found**, within those two searches. The results were larval
(cyclic swimming up to 100 Hz, not applicable to adults), other species, or adult approach
behaviour. I did not search Web of Science, Google Scholar or theses. I did not re-read Idoux 2022
or Danos & Lauder 2012; for those I used the read-levels stated in S24-D-D.

## 5. Evidence level

*Derived* is honest for the claim as a whole. Within it:

- **Measured:** 52 Hz (cross-animal maximum) and 18–30 mm.
- **Assumed:** 20–22 °C as the recording temperature; the b exponent.
- **Calc under an assumption:** 36 Hz.

The claim labels the shortfall "(calc)". It does not mark the 36 Hz floor of its key number as
assumption-driven, and that floor is the defect.

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| 1 | S24-D-deepen.md and S24-D-deepen_calc.py, branch `claude/deepen-s24-sensitive-input-ls0g3m` | full-text | the claim and its inputs |
| 2 | Kyriakatos et al. 2011, *J. Neurosci.* 31:8422, PMC6623330 (pmc.ncbi.nlm.nih.gov HTML) | full-text | quotes verified; 3–5 cycle escapes; in vivo temperature not reported; electrode site |
| 3 | Sculpin fast-start temperature study, pure.uhi.ac.uk record | search-summary | Q10 2.2 (acclimation) vs 1.1–1.2 (acute), other taxon |
| 4 | Danos & Lauder 2012; Idoux et al. 2022 | not re-read; S24-D-D's read-levels relayed | Re 27,800, TL 33 mm; Ca²⁺ half-fusion 53 Hz |

```swarm-challenge
{"claim_id": 145, "outcome": "weakened", "reason": "The arithmetic and the Kyriakatos quotes check out, and the verdict direction survives (escapes were only 3-5 cycles, which supports it further), but the key number's 36 Hz floor comes from an achieved frequency under an assumed stride, not from a ceiling: over the project's own lambda range of 0.48-1.0, check A gives 26-66 Hz (calc) and so does not 'agree', and '30 to >40 Hz' is one animal's range, so the 1.2-2.3x shortfall overstates what is established.", "corrected_value": "adult zebrafish escape EMG burst-frequency ceiling <= 52 Hz (measured upper bound, 18-30 mm fish, temperature unreported); value at 40 mm unknown, about 23-52 Hz under an assumed size exponent b 0-1; 3-BL taxi shortfall >= 1.17-1.56x (calc), upper end not established", "depends_on": ["Kyriakatos 2011 J Neurosci 31:8422 full-text: 52 Hz max across 8 animals, single-animal 30 to >40 Hz, fish 18-30 mm, escapes of 3-5 cycles, in vivo temperature not reported", "S24-D f_req = U/(lambda*L) with U = 1.95 m/s, L = 40 mm, lambda 0.6-0.8 (inherited)", "project stride range lambda 0.48-1.0 (challenge 85)", "Danos & Lauder 2012 Re 27,800, TL 33 mm (relayed via S24-D-D, not re-read)", "assumption: SL ~ 0.8 TL for the SL-basis speed", "assumption: size exponent b 0-1 (unsourced)", "S24 section 3.4 requirement of 12-46 sustained beats (inherited)", "sculpin fast-start Q10 2.2 acclimated vs 1.1-1.2 acute (search-summary, other taxon)"]}
```
