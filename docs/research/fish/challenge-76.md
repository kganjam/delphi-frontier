# Challenge 76: is the launch margin "~4–7x"?

**Claim under review (from `docs/research/fish/S21-deepen.md`, branch
`origin/claude/zebrafish-fast-start-velocity-pgqbck`, commit 9ae82754, read in full):**
"The launch margin should be read as ~4-7x rather than a single ~7x, because the measured population spans a
factor of three and 120 fps likely underestimates the instantaneous peak."
Recorded evidence level: *derived*. Recorded value: 4.2 (ratio).

**Verdict: WEAKENED.** The arithmetic holds. The interval does not. The claim's own two reasons do not support
a 4–7x range. The first gives a margin range of roughly 4–13x, and its 7x end is a median, which is not a
margin on a peak. The second, if true, pushes the margin *below* 4.2x, but the claim keeps 4.2x as the floor.
The honest reading of this evidence is a one-sided bound, **margin ≲ 4.2x**, not a two-sided 4–7x band.

---

## 1. Arithmetic, redone independently

I took the inputs as stated: threshold 5.84 m/s; S21's derived 0.842 m/s; the S21-D author's digitisation of
Miln et al. 2021 Fig. 1a, which gives a range of 0.45–1.38 m/s, a bulk of 0.55–1.15 m/s and a median of
about 0.70–0.85 m/s. All values below are **calculated** (python), not measured:

| Speed (m/s) | Which statistic | Threshold / speed |
|---|---|---|
| 1.38 | fastest of 50 fish | **4.23x** |
| 1.15 | top of "bulk" | 5.08x |
| 0.842 | S21 derived (Re proxy) | 6.94x |
| 0.80 | approx. median | 7.3x |
| 0.55 | bottom of "bulk" | 10.6x |
| 0.45 | slowest fish | **12.98x** |

Also calculated: the population spread is 1.38 / 0.45 = **3.07x**, so "spans a factor of three" is correct.
The length check 0.842 / 0.033 = 25.5 TL/s is also correct. The hypothetical row (1.38 × 2 = 2.76 m/s, giving
2.1x) is correct as arithmetic.

**The defect.** A population spanning 3x maps onto margins spanning 3x, which is 4.2–13x. The interval
"4–7x" spans only 1.65x. The claim cites the 3x spread as its reason but quotes an interval that drops two
thirds of it. The interval is built from two different statistics: the **maximum** sets the lower end
(4.2x), and the **median or the Re-proxy value** sets the upper end (about 7x). That makes it a hybrid, not
a range of anything.

## 2. Proxy check: what quantity should the margin be on?

S21 asks for the **peak** velocity of an adult zebrafish fast-start, compared against a refutation
threshold. The quantity that matters is therefore the species' attainable maximum, a capacity, not the
typical individual. My inference: the median fish (about 7x) is a proxy for the wrong quantity. The margin
on the peak is threshold ÷ (best attainable speed). For that, the fastest of 50 fish is itself only a
**lower bound** on the attainable peak, so 4.2x is an **upper bound on the margin**, not its lower end.
Three things would raise the true peak and so shrink the margin further:

- **Sample maximum.** The fastest of n = 50 underestimates the population's upper tail. Each fish already
  had the best of 4 trials taken (author's method, Miln et al. full text: "four escape responses were
  analysed for each fish and the fastest speed was used").
- **Temperature.** Trials ran at 23 °C, below the 28 °C husbandry standard, as S21-D notes. The size of the
  effect for adult zebrafish fast-start: `unknown`, because I did not find a source giving it.
- **Frame-rate smoothing.** This is the claim's own second reason.

Under the claim's own premises, then, the margin is at most about 4.2x and possibly lower. The "~7x" end is
not a margin on the peak at all.

## 3. Hidden assumption, tested relaxed: that "120 fps underestimates the peak"

The claim treats the bias direction as known ("likely underestimates"). I tested this against the methods
text of Miln et al. 2021 (read in full: Europe PMC PMC8025299 full-text XML, fetched in this session).
There are two effects pulling in opposite directions. Both are my inference from the methods; none of this
is the authors' claim:

1. **Downward bias (the author's point).** A speed taken from displacement over one 8.3 ms frame is an
   average over that window, so it cannot exceed the instantaneous peak *of the true trajectory*. This holds.
   How large it is depends on how sharp the velocity peak is. The S21-D author gave stage-1 durations of
   about 10–20 ms without a source. Peak centre-of-mass velocity in fast-starts is commonly reached late in
   stage 1 or in stage 2, where the curve may be broader. I could not find a number for adult zebrafish
   (`unknown`), so the size of this bias is unestablished.
2. **Upward bias (missed by the author).** Positions were digitised by hand in Tracker from a GoPro at
   120 fps, with a 300 mm ruler as scale, in a 405 × 600 mm arena (full text). Position error is divided by
   a short dt of 8.3 ms. The reported value is then a **maximum over frames, and then a maximum over 4
   trials**. Taking the maximum of noisy finite differences is biased upward. The tracked point is also a
   fixed body landmark at 0.35 BL from the snout (full text). During the C-bend, a body-fixed point picks up
   rotational velocity, so it can move faster than the true, shape-dependent centre of mass. The pixel
   scale and click error are not reported, so the size of this bias is also `unknown`. I give no number.

**Result:** once the assumption is relaxed, the direction of the net 120 fps bias is **not established**.
"Likely underestimates" is a plausible hypothesis, not a supported finding. This weakens the second reason
in the claim, separately from the logic error in §2. Note what follows either way. If the bias is downward,
the margin falls below 4.2x. If it is upward, the fastest fish's 1.38 m/s is inflated and the margin rises
above 4.2x. In **neither** case does the bias give a 4–7x band.

## 4. Is the evidence level honest?

- "derived" is the right label for the ratio, since it is threshold ÷ speed. The S21-D text also correctly
  presents the speeds as *the author's own digitisation*, not the paper's numbers. No mislabel there.
- **Fragility not reflected in the level.** S21-D says the ring detector "over-counts overlapping rings
  (54–142 rings per colour against 50 fish), so only the range is reliable." My inference: this is
  backwards. The extremes of a range are the statistics that a single spurious detection moves most. The
  recorded value, 4.2, depends entirely on the single most extreme ring (1.38 m/s). The cross-check is
  structural, and I could not verify it either: Fig. 1a plots the same 50 fast-start x-values once per day
  (days 1, 4 and 7, three colours), so a real 1.38 m/s fish should appear at the same x in all three colour
  series. S21-D does not report doing that check. The per-fish data (figshare doi:10.6084/m9.figshare.c.5359401)
  were **could-not-access** in this session too: the proxy returned a 403 on `api.figshare.com`, the same
  failure S21-D reported. So the 1.38 m/s endpoint is a digitised extreme of an over-counting detector,
  carried as one number. It is not wrong, but it is less secure than "derived" implies to a reader.
- **Untraceable denominator.** The 5.84 m/s threshold has no recorded provenance. S21-D says the S21 record
  is not in the repository, and I searched no further than reading that file. Every ratio here inherits that.

## 5. Missed regime or counter-evidence

- **Danos & Lauder 2012** (J Exp Biol 215:1854, doi:10.1242/jeb.068957). Read-level: **abstract**, from
  the Europe PMC REST API in this session (PMID 22573764; not open access, no PMC copy). It confirms 1000 fps
  video and a reported "maximum velocity of the center of mass" in normal water (1 mPa s) for zebrafish. The
  abstract gives no velocity value, and the full text was **could-not-access** (journals.biologists.com
  returned a Cloudflare 403 challenge). It is the one source that could test both bias directions in §3.
  I have no number from it, and I do not supply one.
- I found no published counter-example giving an adult zebrafish fast-start peak near 5.84 m/s. **Scope of
  that negative:** I made no new literature search beyond the two fetches above. I relied on S21-D's own
  search scope (Europe PMC, 996 hits, first 100 titles screened), which I did not re-run.

## What survives

- The arithmetic.
- The qualitative point that one ~7x number hid individual variation.
- The conclusion that the gap to 5.84 m/s is **not closed** by any measured value. The fastest fish would
  need about a 4.2x under-read (calculated), and nothing reviewed suggests that.

## What does not survive

- The two-sided "4–7x" band.
- The use of "120 fps underestimates" as a reason for it.

**Corrected reading:** the margin is ≲ 4.2x (calculated upper bound). It comes from the fastest of 50
adults, digitised from a 120 fps figure, with the direction of net measurement bias unestablished.

### Sources and read-levels
- `docs/research/fish/S21-deepen.md` (origin/claude/zebrafish-fast-start-velocity-pgqbck). **full-text**
- Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146, doi:10.1098/rsos.210146 (PMC8025299). **full-text** (methods and captions; Fig. 1 image not re-digitised by me)
- Danos & Lauder 2012, J Exp Biol 215:1854, doi:10.1242/jeb.068957. **abstract**
- Miln et al. figshare collection, doi:10.6084/m9.figshare.c.5359401. **could-not-access** (proxy 403)
- Original S21 record and the provenance of the 5.84 m/s threshold. **could-not-access** (not in repo, per S21-D; not independently searched)

```swarm-challenge
{"claim_id": 76, "outcome": "weakened", "reason": "The arithmetic is right, but the 4-7x band is not supported by its own reasons: a 3x population spread maps to 4.2-13x margins, the 7x end is a median rather than a margin on the peak, a 120 fps underestimate would push the margin below 4.2x rather than bound it there, and the bias direction is unestablished because max-of-noisy-frame-differences on a body-fixed landmark biases upward.", "corrected_value": "margin <= ~4.2x (threshold 5.84 m/s / fastest of 50 adults ~1.38 m/s; calculated upper bound, not a 4-7x range)", "depends_on": ["Miln et al. 2021 Fig. 1a fastest-fish ~1.38 m/s (S21-D digitisation, unverified against figshare)", "Miln et al. 2021 population range ~0.45-1.38 m/s (S21-D digitisation)", "refutation threshold 5.84 m/s (provenance unknown)", "S21 derived value 0.842 m/s", "Miln et al. 2021 methods: 120 fps GoPro, manual Tracker digitisation, landmark at 0.35 BL, best of 4 trials (full-text)"]}
```
