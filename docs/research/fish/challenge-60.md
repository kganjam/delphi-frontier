# Challenge 60: "LAWENTRY muscle-power-density dispatched"

- **Claim under attack:** "LAWENTRY muscle-power-density dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_01QbcBRb7bupimBU4QmG5DfJ`
- **Challenger:** adversarial cloud review, 2026-11-04
- **Verdict: WEAKENED.** The dispatch is real. It produced `library/laws/muscle-power-density.yaml`,
  which passes the dimension gate, and the gate also rejects a mutant of it. Most of its arithmetic
  reproduces. However, the delivered entry has four defects:
  1. It **crashes the library's page builder**. Because of this one entry, `build_pages.py`
     currently fails for every page, not just this one.
  2. One where-it-breaks sentence ("exceed every muscle ceiling above by 5-15x") is contradicted by
     the entry's own numbers.
  3. The scup data are mislabelled for frequency. The stated Q10 does not match the stated powers.
  4. It is unmerged.

  On their own wording the claim is only "dispatched", and that part holds. What a reader would infer
  from it, that a usable library entry exists, is only partly true.

## What the claim asserts

The claim records an operation. It contains no number. "Dispatched" stands in for what actually
matters: whether the library now holds a correct, gated and renderable entry that gives a W/kg ceiling
for vertebrate muscle by fibre type. I tested the operation, and then I tested that quantity.

## 1. Was it dispatched, and did it deliver? (observed, from git and tool output)

| Check | Method | Result | Kind |
|---|---|---|---|
| Delivering commit | `git log --all --grep`, `git show --stat` | **`ee469aeb`** (2026-11-04 08:19:54 UTC), "Law library: maximum mass-specific power of vertebrate muscle, by fibre type". It adds only `library/laws/muscle-power-density.yaml` (+268). Its `Claude-Session` trailer matches the claim's source session. | observation (git record) |
| Where it lives | `git branch -r --contains ee469aeb` | Only `origin/claude/muscle-power-density-thmr16` | observation |
| Merged? | `git merge-base --is-ancestor ee469aeb origin/main` | **NOT merged**. `origin/main` has no `library/` directory at the root listing I printed. | observation |
| Dimension gate | `library/tools/check_laws.py --dir library/laws` at `ee469aeb` | `ok muscle-power-density.yaml`, 3 entries, 0 problems | observation (tool output) |
| My negative control | I dropped `/ rho` from the equation and re-ran the gate | **Rejected**: "'P_m' is L^2·T^-3, other side is M^1·L^-1·T^-3". The gate does bite on this entry. | observation (tool output) |
| Page build | `library/tools/build_pages.py --check` at `ee469aeb` | **Crash**: `ValueError: Unknown format code 'g' for object of type 'str'` in `fmt_interval`. The builder stops, so no page can be built while this entry is in the directory. | observation (tool output) |
| Cause of the crash | `yaml.safe_load` of the entry | `sigma_0.interval` loads as `['1.5e5', '4.0e5']`, which are **strings**. PyYAML (YAML 1.1) resolves a float with an exponent only when the exponent has a sign, as in `1.5e+5`. With that one change the builder runs and reports only `stale: muscle-power-density.md, index.md`. | observation (tool output) plus my diagnosis |
| Source session transcript | not attempted. Challenges 47 and 53 record that this route returns not-found. | could-not-access (not tried) | — |

The gate passes because `check_laws.py` checks the equation's dimensions. It does not check that
intervals are numeric. So the most uncertain constant in the entry, `sigma_0`, has its only numbers
stored as text. Any downstream tool that reads `interval` will either break or compare strings.
`sigma_0.value` is the string `unknown`, which is acceptable and honest, but it also renders as text.
Smaller point: the inferred and scup constants use `value_soleus`, `value_EDL`, `value_20C` and
`value_10C` instead of `value`. The builder therefore prints them as `unknown`, even though the entry
holds numbers for them. That is my reading of `fmt_interval`; I did not render it.

## 2. Arithmetic, redone independently (all CALCULATED by me, not observed)

| Entry states | My result | Match |
|---|---|---|
| Hill power ratio W_r: maximum of f·v on (f+k)(v+k) = k(1+k), with k = a/P0 = 0.25 | 0.0955, at v = f = 0.309 | yes |
| Interval for k from 0.10 to 0.50 | 0.0537 to 0.134 | yes. The entry gives [0.054, 0.134]. |
| "Power maximum at roughly a third of V_max and of F0" | 0.23 to 0.37 over that k range | yes, as an approximation |
| Isotonic values inferred from mouse cyclic power: 92/0.70 and 247/0.70 | 131.4 and 352.9 W/kg | yes |
| V_max = 353·1060/(0.095·2.5e5) | 15.75 L/s | yes |
| The same with σ0 = 1.5e5 Pa | 26.26 L/s. The ratio to the previous line is 1.67. | yes (the entry says 1.7x) |
| Frog jump ratio: 2000/461 and 2000/260 | 4.34 and 7.69 | yes |
| Dimensions: W_r·σ0·V_max/ρ, with V_max in 1/s | Pa·s⁻¹·m³/kg = W/kg = L²T⁻³ | yes (the gate agrees) |
| **Scup red muscle: Q10 = 2.29 from 12.8 W/kg (10 °C) and 27.9 W/kg (20 °C)** | (27.9/12.8)^(10/10) = **2.18**. A Q10 of 2.29 would need 29.3 W/kg at 20 °C. | **no** (see §5) |

**Where-it-breaks (1), "Jumps measured or estimated at 1100-2000+ W/kg ... exceed every muscle
ceiling above by 5-15x".** I tested this against the entry's own constants (my arithmetic):

| Jump power | against quail cyclic 390 | against frog isotonic 260 to 461 | against the reported instantaneous record 1200 |
|---|---|---|---|
| Galago, 1100 W/kg | 2.8x | 2.4x to 4.2x | **0.92x, i.e. it does not exceed it** |
| Frog, 1644 W/kg | 4.2x | 3.6x to 6.3x | 1.37x |
| Frog, 2000 W/kg | 5.1x | 4.3x to 7.7x | 1.67x |

None of these ratios reaches 15x. The galago value does not exceed every ceiling. The entry's own
frog worked example gives 4.3 to 7.7, which overlaps "5-15x" only in part. The 15x is Aerts' (1998)
amplification factor relative to the galago's own estimated muscle capacity. It is not a ratio to the
ceilings listed in this entry. The physics conclusion survives (jumps need elastic power
amplification), but the stated range is wrong as written. A corrected statement from the entry's own
numbers would be "about 2.4x to 7.7x above the cyclic and isotonic ceilings, and at or below about
1.7x the unverified 1200 W/kg instantaneous figure". The entry already flags that 1200 W/kg figure
as unverified, which softens the defect but does not remove "every".

## 3. Proxy

The equation gives an **instantaneous isotonic** peak. For a swimming fish, the quantity that matters
is **cyclic work-loop power at the tail-beat frequency and the body temperature**. The entry says this
openly. Its domain notes say to multiply by about 0.7 and to expect less away from the optimal
frequency, and break (3) gives the toadfish net-power cut-offs. So the proxy is declared, not hidden.
The 0.7 ratio, however, comes from **mouse at 37 °C at the optimal frequency** only (Askew & Marsh
1997, search-summary). Applying it to fish muscle is an untested transfer. That is my inference, and
the entry does not claim otherwise.

## 4. Hidden assumption, relaxed: "σ0 is roughly fibre-type independent, so the ceiling orders as V_max"

The mechanism derives the 10:5:1 IIX:IIA:I ordering from V_max. According to the entry's own reading
of Bottinelli 1996, the abstract states only that P0/CSA does not differ between IIA and IIB. The entry
does not claim that type I matches. If type-I σ0 is lower, part of the 10× is force, not velocity. The
entry flags the attribution as its own inference. The σ0 dispute it keeps unresolved (Medler about
150 kN/m² against Weis-Fogh & Alexander 250 to 400) moves the inferred V_max by 1.67x, and I
reproduced that factor. The entry neither hides this assumption nor resolves it. That is acceptable,
and I score no defect here.

## 5. Evidence level, and regimes the author missed

**Evidence level.** `unknown` overstates nothing. The accurate description is "operational record,
verified from the git trailer and tool output". Inside the entry, the labels are mostly honest:
- W_r is marked CALCULATED, with an interval that the author chose.
- The mouse isotonic values are marked INFERRED.
- The worked V_max is `evidence: derived`.
- The 1200 W/kg figure is flagged as not found in the primary abstracts.
- Every JEB source is search-summary, because the host was unreachable.
- Disputes are kept rather than averaged, including the quail raw 80 W/kg against the 350 to 400
  W/kg corrected figure.

I found no derived number presented as measured.

**Scup frequency and Q10 (fish-specific, the regime that matters for this folder).** The entry says
the scup red muscle reaches its "max at about 2.5 Hz" and quotes values for 10 °C and 20 °C. Rome &
Swank's abstract, at **search-summary** level from a web search on 2026-11-04, reports that maximum
power came at 5 Hz at 20 °C and at 2.5 Hz at 10 °C. It also reports that Q10 at a *fixed* frequency
ran from about 1 at 1 Hz to about 5 at 7.5 Hz. Later papers cite a Q10 of about 2.3 for optimised
power, also at search-summary level.

- **The 2.5 Hz label.** Applied to both temperatures, it is wrong for 20 °C.
- **The Q10.** The entry's own two powers give 2.18, not 2.29. I cannot tell which number is the
  primary's: one of the two power values may be mis-transcribed, or the 2.29 may be computed
  differently. I preserve the disagreement and do not choose between them.
- **What follows for design.** The Q10 at a fixed frequency spans roughly 1 to 5. So break (2)
  ("temperature") understates the problem for a fish swimming at a fixed tail-beat frequency. A single
  Q10 is not portable even within one muscle.

**Fish white muscle.** The entry's only fish ceiling is slow red muscle, at 12.8 to 27.9 W/kg. Fast
white muscle, which drives fast-starts, is listed as `unknown`. The entry states this scope honestly.
It means the entry gives **no fish burst ceiling**, so a fish design check must borrow the mouse or
quail fast-muscle values outside their taxon and temperature. I did not search for fish white-muscle
work-loop power in this review. My read level for it is **could-not-access (not tried)**, and I
supply no number.

**Published counter-examples.** I searched for nothing beyond the single Rome & Swank query. The
author's remaining citations keep the read levels the author recorded. My own read level for each is
could-not-access, because I did not try.

## Corrected value

There is no single corrected value. The claim carries none, and the defects are structural and textual:
- The `sigma_0` interval should be written `[1.5e+5, 4.0e+5]`.
- The break (1) range should read "about 2.4x to 7.7x above the cyclic and isotonic ceilings".
- The scup entry should read "maximum at 2.5 Hz at 10 °C and 5 Hz at 20 °C", with the 2.18 against
  2.29 conflict recorded.

## Sources

- Git history of `kganjam/delphi-frontier`: commit `ee469aeb` on
  `origin/claude/muscle-power-density-thmr16`, and `origin/main`, as fetched on 2026-11-04. Read
  level: full-text.
- `library/laws/muscle-power-density.yaml`, `library/tools/check_laws.py` and
  `library/tools/build_pages.py` at `ee469aeb`. Read level: full-text.
- `docs/research/fish/challenge-53.md` and the commit messages of challenges 42 and 51 (precedent and
  format). Read level: full-text.
- Rome LC, Swank D (1992) J Exp Biol 171:261-281, through a web search on 2026-11-04 that returned
  the JEB landing page and later papers quoting it
  (<https://cob.silverchair.com/jeb/article/171/1/261/6442/The-influence-of-temperature-on-power-output-of>).
  Read level: search-summary.
- Source session transcript. Read level: could-not-access (not attempted).

```swarm-challenge
{"claim_id": 60, "outcome": "weakened", "reason": "Dispatch confirmed (commit ee469aeb, matching Claude-Session trailer; check_laws.py passes and rejects a no-rho mutant; arithmetic reproduces), but the entry is unmerged, its sigma_0 interval [1.5e5, 4.0e5] loads as YAML strings and crashes build_pages.py for the whole library, its break (1) claim that jumps 'exceed every muscle ceiling above by 5-15x' contradicts its own numbers (2.4-7.7x, and galago 1100 W/kg is below the 1200 W/kg record), and its scup data give Q10 2.18 not the stated 2.29 and mislabel 20 C optimum frequency (5 Hz, not 2.5 Hz).", "corrected_value": null,
  "depends_on": ["commit ee469aeb on origin/claude/muscle-power-density-thmr16 and its Claude-Session trailer", "check_laws.py and build_pages.py behaviour at ee469aeb", "PyYAML 1.1 float resolution (exponent requires sign)", "entry's own constants: 260-461 W/kg frog isotonic, 390 W/kg quail, 1200 W/kg instantaneous record, 1100/1644/2000 W/kg jump powers", "entry's scup values 12.8 W/kg at 10 C and 27.9 W/kg at 20 C", "Rome & Swank 1992 abstract at search-summary: optimum 2.5 Hz at 10 C, 5 Hz at 20 C", "Aerts 1998 15x as amplification relative to galago muscle (author's search-summary reading)"]}
```
