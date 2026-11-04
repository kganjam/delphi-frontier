# Challenge 183: adversarial review of S20-D (zebrafish flight, sensitive input)

Claim under review: S20-D, `docs/research/fish/S20-deepen.md` on branch
`origin/claude/deepen-s20-zebrafish-flight-9smifx` (harvest id `deepen-s20-zebrafish-flight-9smifx`).
I read it in full from that branch, along with its script.

Independent arithmetic: `docs/research/fish/challenge-183_calc.py`. Run it from the repository root.
I wrote it separately and did not copy the author's working. Every number below that is not
attributed to a source is a **calculation** from that script. Date: 2026-11-04.

**Verdict: WEAKENED.** Three parts of the claim hold:

- exit speed is the most sensitive input;
- the arithmetic on 0.84 m/s reproduces;
- the 1 m launch S20 priced is out of reach.

Two parts of the headline do not hold:

1. **The key number is not the adult peak escape speed. It is the lower of two disagreeing
   sources.** A measured adult *D. rerio* escape maximal speed exists: 157 ± 27 cm/s (mean ± SD;
   Demesmay et al. 2025, full text re-read this session). That is 1.86× the Re inversion. On it,
   the reachable 45° hop is about 25 cm and 0.23 s, not 7 cm and 0.12 s.
2. **"The 0.1–1 m escape … out of reach by at least 2.1× in speed" is false as worded.**
   - The 2.1× applies only to the 1 m end, and even there it is 2.08× against the guppy-class
     value.
   - The 0.1 m end needs 0.99 m/s. That is only 1.18× above the claim's own 0.84 m/s.
   - The 0.1 m end is *exceeded* by the guppy-class comparator (1.51 m/s), which the claim itself
     cites, and by the measured adult mean (1.57 m/s).
   - The author's body text says this correctly ("falls at its 1 m end. What remains is
     6–10 cm"). The one-line claim drops it.

The direction of the claim's verdict, "strengthens", survives for the 1 m end. The quantitative
headline does not.

---

## 1. Arithmetic, redone from the stated inputs

These are drag-free calculations from the water surface: R = v² sin 2α / g. The glide area comes
from S = 2mg / (ρ C_L v²), with m = 0.4 g, ρ = 1.2 and C_L = 1.

| Quantity | Mine | Claim |
|---|---|---|
| U = Re·ν/L = 27 800 × 10⁻⁶ / 0.033 | 0.842 m/s (0.778–0.907 at ±1 s.e.m.) | 0.84 (0.78–0.91) |
| 45° range at 0.842 | 7.2 cm | 7.2 cm |
| Time aloft | 0.121 s | 0.12 s |
| Apex at 45° | 1.81 cm | 1.8 cm |
| Glide area | 92 cm² | 93 cm² |
| Launch cost, η = 0.10, SMR 15–37 J/day | 3.8×10⁻⁵ – 9.5×10⁻⁵ of daily SMR | ~1×10⁻⁴ |
| v needed for 1 m | 3.132 m/s | 3.13 |
| v needed for 0.10 m | 0.990 m/s | (not in claim) |
| Guppy-class comparator, √(2g·3.5·0.033) | 1.505 m/s | 1.51 |
| 1 m deficit vs guppy-class | **×2.081** | "at least 2.1×" |
| 1 m deficit vs 0.842 | ×3.72 | 3.7× (body) |

All the arithmetic reproduces. "At least 2.1×" rounds 2.08 up, so as a floor it should read "at
least 2.08×". That is cosmetic, but a floor should not be rounded upward. Energy scaling as v² is
correct, and so is the claim that range scales with v². The claim says required glide area also
scales "as v²". Strictly it scales as **v⁻²**; the author's table uses it correctly. The claim's
wording is loose here, not wrong in substance.

## 2. Proxy check: is 0.84 m/s "adult peak burst speed"?

**It is one proxy among two that disagree, and it is the lower one.** The author treats the Re
inversion from Danos & Lauder 2012 as "the best available number". It is not the only adult
measurement.

**Demesmay et al. 2025, *PLoS Biol* 23(11):e3003484 (PMC12604801).** I fetched the Europe PMC
`fullTextXML` independently this session. Read-level: **full-text**. Verbatim author claims:

- "the calculated maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants)";
- the Fig 4C legend: "Graphs represent mean ± SD with individual values";
- the methods: escape videos "at … 240 frames/s (escape response, 1 s long videos)".

Sibling challenge-143 reports more methods detail, which I did not re-check: manual Fiji tracking,
a dropped-object stimulus, fish 2.6–3.6 cm, and "3.8 ± 0.8 cm" covered in the first 40 ms.

**The disagreement, kept separate and not averaged.**

| Source | v (m/s) | What kind of number | 45° range | 1 m deficit | Reaches 0.1 m? |
|---|---|---|---|---|---|
| Danos & Lauder 2012, Re inversion (N = 5, 1000 fps) | 0.842 | calculated from a reported Re; read-level relayed (abstract only this session, via S20-D) | 7.2 cm | ×3.72 | no (×1.18 short) |
| Demesmay 2025, control mean (n ≥ 11, 240 fps) | 1.57 | measured (author claim, full-text) | 25.1 cm | ×1.99 | yes |
| Demesmay 2025, control +2 SD | 2.11 | calculated from mean and SD | 45.4 cm | ×1.48 | yes |
| Demesmay 2025, mean over first 40 ms (3.8 cm / 40 ms) | 0.95 | calculated from a measured distance | 9.2 cm | ×3.30 | no |

1.57 / 0.842 = ×1.86 in speed, or ×3.5 in range.

**Possible reasons for the disagreement (my inference, untested).**

- The two studies may use different tracked points. A head point overstates CoM speed.
- Manual 240 fps tracking may inflate the maximum through frame noise.
- The Danos & Lauder Re may be defined on a time-averaged or stage-1 speed.
- The Danos & Lauder Re may use a different length basis. If it used SL (≈ 27 mm,
  hypothetical), U would rise to 1.03 m/s.

I could not open Danos & Lauder Table 1 or Fig. 3 (see §5), so I cannot tell which reading is
right. Note that Demesmay's 40-ms *average* (0.95 m/s) is close to the Re inversion, which is
consistent with the Re reflecting a mean rather than a peak. That is my inference.

**Consequence.** The claim's KEY figure, "adult peak burst speed 0.84 m/s … giving a 7.2 cm
maximum ballistic range", presents the lower source as the adult peak. The only directly reported
adult *peak* speed is 1.57 m/s mean, which gives a 25 cm hop. "Caps the reachable aerial phase at
about 7 cm and 0.12 s" is therefore not a cap. Across the two sources the range is **7–25 cm at
the mean, and up to ~45 cm at +2 SD**.

## 3. Hidden assumptions, relaxed

- **"0.1–1 m" treated as one block.** This assumption carries the headline's "out of reach". The
  low end of S20's range, 0.1 m, needs 0.99 m/s, and every line below shows it is not out of
  reach:
  - it sits within ×1.18 of the claim's own number;
  - it is inside the claim's own ±1 s.e.m. band if Re used SL;
  - it is exceeded by the guppy-class comparator the claim cites;
  - it is exceeded by the measured adult mean.

  Only the upper part of the range (above ~0.25–0.45 m) is out of reach.
- **Submerged burst peak = exit speed.** The author argues this makes the value an upper bound,
  because the fish must reorient and break the interface. The guppy data relayed in challenge-169
  (Soares & Bierman 2013: water exit 1.02 m/s, airborne 1.24 m/s; I did not re-read this source)
  show that a jumping fish can be *faster* at or after exit than its in-water speed. So "upper
  bound" is not established in either direction.
- **Drag-free.** Drag only raises the speed needed (≈ 2% of g at 3.13 m/s per challenge-143), so
  relaxing it does not help the fish.
- **Feasibility standing in for payoff (a framing proxy).** The capability gap shows a *current*
  zebrafish cannot make a 1 m launch. The question S20 asked is whether flight *would pay*, which
  is an evolutionary cost–benefit question. Any evolved trait starts out absent. In my reading, the
  gap does not show the benefit is small. It shows the true cost is not ~10⁻⁴ SMR but the
  morphological investment needed to raise exit speed ≥ 1.5–2× (cf. hypocaudal lobes in
  exocoetids, challenge-24). That does push toward "would not pay", so "strengthens" is defensible.
  But the mechanism is "the cost was mispriced", not "the option is unavailable".

## 4. Is the evidence level honest?

Yes, at the level of `derived`. The claim calls 0.84 m/s "calculated" in the sentence, and the
body states that the Re was relayed from replicate-21 and not re-read. The one defect is the label
"adult peak burst speed" on the KEY number. It reads as the measured adult peak when it is a
calculated inversion that sits 1.86× below the one directly reported adult peak (§2).

## 5. Access record and negative-search scope

| Source | Read-level this session |
|---|---|
| S20-deepen.md and S20-deepen_calc.py (claim) | full-text (repository branch) |
| Demesmay et al. 2025, *PLoS Biol* 23:e3003484, PMC12604801, Europe PMC fullTextXML | **full-text**: three quoted passages checked verbatim |
| Danos & Lauder 2012, *J Exp Biol* 215:1854 | not re-attempted. Read-level is S20-D's: abstract, with figures relayed from replicate-21. Its length basis for Re is `unknown` |
| challenge-143.md, challenge-169.md (sibling repository notes) | full-text (repository). Their Soares & Bierman 2013 and Chang et al. 2019 figures are relayed, not re-read by me |

I ran no new web searches. The Demesmay counter-example was located through sibling note
challenge-143 and then verified at the primary source. I did not search for further adult
*D. rerio* jump or exit-speed measurements. Any absence of such measurements rests on S20-D's and
challenge-143's searches (2–3 queries each, search-summary).

## 6. What survives

- Exit speed is the dominant input, and the energetic "almost free" sub-claim stands under either
  source (≤ ~6×10⁻⁴ of daily SMR even at 2.11 m/s: 9.5×10⁻⁵ × (2.11/0.842)², a calculation).
- The 1 m launch is out of reach under every line of evidence, by ×1.48 (at +2 SD) to ×3.7.
- Gliding is not available at any of these speeds. At 2.11 m/s the area needed is still ~15 cm²,
  compared with roughly 3 cm² of body planform. That is a calculation using the claim's
  planform estimate.

## Corrected statement

Adult exit speed is the sensitive input. The two adult sources disagree:

- 0.84 m/s, calculated by Re inversion from Danos & Lauder 2012;
- 1.57 ± 0.27 m/s (SD), measured by Demesmay et al. 2025.

The reachable 45° hop is therefore 7–25 cm at the mean (≤ ~45 cm at +2 SD), not capped at 7 cm.
The 0.1 m end of S20's range is reachable. The 1 m end is out of reach by ×1.48–×3.7 in speed.
The direction "strengthens" survives only for the upper part of S20's range.

```swarm-challenge
{"claim_id": 183, "outcome": "weakened", "reason": "Arithmetic and the 1 m out-of-reach direction reproduce, but the key 0.84 m/s is the lower of two disagreeing adult sources (Demesmay et al. 2025 measured 1.57 +/- 0.27 m/s SD, full-text, giving a 25 cm hop), and the 0.1 m end of the '0.1-1 m' range needs only 0.99 m/s, which the claim's own guppy-class comparator and the measured adult mean exceed, so 'out of reach by at least 2.1x' holds only for 1 m and there is 2.08x (guppy) or 1.48-1.99x (Demesmay).",
  "corrected_value": "adult exit speed 0.84 m/s (Re inversion, calculated) vs 1.57 +/- 0.27 m/s (measured, Demesmay 2025); 45-deg hop 7-25 cm at the mean (up to ~45 cm at +2 SD); 1 m launch speed deficit x1.48-x3.7; 0.1 m launch (0.99 m/s) not out of reach",
  "depends_on": ["Demesmay et al. 2025 PLoS Biol 23:e3003484 control escape maximal speed 157 +/- 27 cm/s, mutant 161 +/- 33 cm/s (author claim, full-text re-read this session)", "Demesmay et al. 2025 Fig 4C legend: mean +/- SD (author claim, full-text)", "Demesmay et al. 2025 distance in first 40 ms 3.8 +/- 0.8 cm (relayed via challenge-143, not re-checked)", "Danos & Lauder 2012 Re 27800 +/- 2140 s.e.m., TL 33 mm, 1 mPa s (relayed via S20-D/replicate-21; length basis of Re unknown)", "Soares & Bierman 2013 guppy water-exit 1.02 vs air 1.24 m/s (relayed via challenge-169, not re-read)", "guppy-class comparator 3.5 BL vertical jump scaled to 33 mm (S20-D's construction from Chang et al. 2019)", "law: drag-free ballistic range R = v^2 sin(2a)/g from the surface", "S20 framing: 0.1-1 m aerial range at 45 deg as the escape being priced", "S20 inputs m = 0.4 g, eta = 0.10, SMR 15-37 J/day"]}
```
