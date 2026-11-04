# Replication 290: does the bandwidth argument against active attitude control fall? (S18-D)

Date: 2026-11-04. Evidence level: **derived**. This combines my arithmetic with literature. Nothing here is a new observation.

## What I read, and what I avoided

- I read S18's reference geometry and its key number in `docs/research/fish/S18-behaviour.md` on `origin/claude/zebrafish-aerial-attitude-k8hgr8`. I needed both as inputs.
- On `origin/claude/deepen-s18-zebrafish-air-3u64z4`, I read only §0–§1 of `S18-deepen.md` (lines 1–52) to get the problem setup.
  - **Disclosure:** §1 already contains the ratio table R = f_req / f_avail for several trial values of f_avail. So I saw the *form* of the argument before deriving anything. I had not seen which f_avail value the deepen document chose, or its sources.
  - I stopped there. I read §2 onward only after writing my value (see "Comparison").
- I did not open `claude/challenge-s18-vestibular-frequency-0vmw91`.

## Question as I framed it

S18 argued against active vestibular attitude control because the required control frequency is higher than the available one:

- **Required:** the airframe's pitch mode, f_req ≈ 1.9 Hz at 2 m/s.
- **Available:** the zebrafish vestibular frequency, f_avail = 0.5 Hz.

The argument falls if a defensible f_avail makes R = f_req / f_avail ≤ 1.

## Input 1: f_req (computation on assumed geometry)

S18's reference design is assumed, not measured. Read-level: full-text (repository file).

- m = 0.4 g, L = 4 cm, I_y = mL²/12 = 5.33 × 10⁻⁸ kg m²
- S_t = 1 cm², l_t = 2 cm, a_t = 1.6 rad⁻¹, ρ = 1.2 kg m⁻³

The model:

- M_α = ½ρV² · S_t · l_t · a_t
- ω_n = √(M_α / I_y), and f = ω_n / 2π

At V = 2 m/s:

- M_α = (0.5 × 1.2 × 2²) × 1 × 10⁻⁴ × 0.02 × 1.6 = 2.4 × 3.2 × 10⁻⁶ = 7.68 × 10⁻⁶ N m rad⁻¹
- ω_n = √(7.68 × 10⁻⁶ / 5.33 × 10⁻⁸) = √144 = 12.0 rad s⁻¹
- **f_req = 12.0 / 2π = 1.91 Hz**

At 1 m/s and 3 m/s, f_req is 0.95 Hz and 2.86 Hz (my run). The tail-only damping ratio is ζ = 0.06.

## Input 2: f_avail, from primary sources (my search, 2026-11-04)

| # | Finding (author's claim) | Source | Read-level |
|---|---|---|---|
| A | Toadfish horizontal-canal afferents were tested with sinusoidal rotation from **0.001–10 Hz**. Low-gain afferents are "relatively linear re: stimulus velocity across most of the frequency and amplitude spectra tested". High-gain afferents show "high-frequency gain enhancement and phase advance". No corner frequencies are given. | Boyle & Highstein 1990, *J Neurosci* 10(5):1557–1569, PMC6570080 | abstract |
| B | Toadfish hair cells under sinusoidal canal indentation at 0.1–20 Hz. Hair-cell voltage showed "relatively flat gain with very little phase lead over the physiological bandwidth". Hair-cell current gain and phase were "relatively flat over the entire frequency range tested". | Rabbitt, Boyle, Holstein, Highstein 2004/5, *J Neurophysiol* 93(1):424–436, PMC3000937 | full-text, first 100k of about 131k characters, via fetch-tool summary |
| C | Mechanical stimuli below 5 Hz give afferent responses that "closely correspond to those using actual head rotations". At 2 Hz, the afferent lags hair-cell voltage by only 4°. | Boyle, Rabbitt, Highstein 2009, *J Neurophysiol* 102(3):1513–1525, PMC2746798 | full-text, first 100k of about 111k characters, via fetch-tool summary |
| D | Goldfish sinusoidal VOR in darkness is close to compensatory, gain about 1 with phase about 180°, from about 1/32 to **2 Hz**. | Pastor et al. 1992, *J Neurophysiol* (PubMed 1491254) | **search-summary**. The host read.qxmd.com is DNS-blocked in this session, so it is unconfirmed. |
| E | Goldfish VOR latency is about **18 ms** (adducting eye) and 20 ms (abducting eye), from head-velocity steps. | Goldfish cerebellar VOR study; exact citation not retrieved | **search-summary**. The host data.zhenzhi.com is DNS-blocked. Unconfirmed. |
| F | Larval zebrafish (4 and 7 dpf) correct pitch in discrete bouts. The basal bout rate is about 0.50–0.51 Hz in controls. Bout probability is 0 for 250 ms after a bout, and bouts last 0.13–0.15 s. No tilt-to-bout latency is reported. | Hamling, Harmon, Kimura, Higashijima, Schoppik 2024, *J Neurosci* 44(30):e2315232024, PMC11270517 | full-text, first 100k of about 137k characters, via fetch-tool summary |

Negative searches, with their scope:

- "adult zebrafish semicircular canal VOR angular rotation frequency response" (one standard WebSearch) returned only larval studies and a goldfish study at 0.5 Hz. **Adult *Danio rerio* canal or angular-VOR frequency response: unknown.**
- **Adult zebrafish postural-loop latency: unknown.** I did not search further for it.
- pubmed.ncbi.nlm.nih.gov is DNS-blocked in this session, so I could not use it.

## Arithmetic

The ratio is R = f_req / f_avail. Three readings of f_avail give three different results.

1. **Peripheral angular-rate sensor (A–C, toadfish, cross-species).**
   - The sensor passes at least 10 Hz under rotation and at least 20 Hz under indentation. Both are lower bounds set by the test ranges.
   - With f_avail ≥ 10 Hz: R ≤ 0.095 / **0.19** / 0.29 at 1 / 2 / 3 m/s.
2. **Behavioural canal-driven reflex in an adult cyprinid (D, goldfish, search-summary).**
   - The reflex is close to unity gain up to the 2 Hz test limit, so f_avail ≥ 2 Hz.
   - R ≤ 0.48 / **0.95** / 1.43.
   - R stays at or below 1 at 2 m/s, but only just. At 3 m/s, R > 1 is still possible on this bound alone.
3. **Delay-limited loop (E, search-summary).** This is my inference, using a standard control rule of thumb.
   - A pure delay τ adds a phase lag of 360·f·τ degrees.
   - At f_req = 1.91 Hz with τ = 20 ms, the lag is **13.8°**. At 2.86 Hz it is 20.6°.
   - The crossover for 45° of phase margin, with integrator-like loop shaping, is about 1/(8τ) = **6.25 Hz**. That gives R ≈ 0.15 / **0.31** / 0.46.
4. **Larval bout-sampled postural loop (F, *Danio rerio* itself).**
   - With f_avail ≈ 0.5 Hz: R ≈ 1.9 / **3.8** / 5.7.
   - 0.5 Hz sampling is below 2 × f_req at every speed, so it cannot damp the mode.
   - This disagrees with readings 1–3, and I preserve that disagreement. It is the only measured *zebrafish* postural loop, but it is larval and bout-based. Whether it transfers to a 4 cm adult is unestablished.

## My value

**R at 2 m/s ≈ 0.19 at the level of the sensor (f_avail ≥ 10 Hz, toadfish), and R ≲ 0.3–0.95 at the level of a canal-driven loop (f_avail ≈ 2–6 Hz, goldfish, search-summary).**

So the bandwidth argument as S18 stated it ("sensor 2–10× too slow") **falls**. The 0.5 Hz figure was the highest stimulus frequency anyone had tested in larvae, not a measured cutoff. Every adult-teleost datum I found passes 1.9 Hz.

Uncertainty and limits:

- **Cross-species transfer.** The adult zebrafish value is unknown, and this is the biggest uncertainty.
- **Read-levels.** D and E are search-summary only.
- **Larval conflict.** The larval bout loop (R ≈ 3.8) conflicts with the adult-teleost readings.
- **Other legs untouched.** This addresses bandwidth only. It does not address reflex gain, or the loss of the utricle's gravity reference in free fall (S18 leg 1).

## Comparison with the recorded value (read after deriving the above)

S18-deepen §4 records:

- f_avail(peripheral) ≥ 10 Hz, from toadfish (Boyle & Highstein 1990; Rabbitt et al. 2004)
- R = 0.10 / 0.19 / 0.29
- verdict "FALLS"

My sensor-level R (0.095 / 0.19 / 0.29) matches it to rounding, and the verdict matches. **AGREE.**

Caveats on how independent this agreement is:

- My sensor-level value rests on **the same three toadfish papers** the deepen document used, so it is not independent on that input. Agreeing on R mostly confirms that the arithmetic and the reading of sources were done correctly.
- My partly independent addition is the goldfish behavioural VOR (≥ 2 Hz) and the latency of about 18–20 ms, both search-summary only. They support "falls" with a smaller margin (R ≤ 0.95 at 2 m/s).
- The deepen document did not use these. It lists adult latency as unknown.
- The larval bout loop is the remaining contrary datum. The deepen document reaches the same view of it.

```swarm-replication
{"claim_id": 290, "my_value": "R = f_req/f_avail ≈ 0.19 at 2 m/s (sensor-level, f_avail ≥10 Hz toadfish canal; 0.10–0.29 over 1–3 m/s); loop-level R ≲ 0.3–0.95 using goldfish VOR ≥2 Hz / ~20 ms latency (search-summary)", "agrees": true,
  "note": "Same R and 'falls' verdict as S18-D, but my sensor-level input rests on the same toadfish papers so independence is partial; goldfish VOR data (search-summary) independently support R<=1 at 2 m/s with a thin margin, and the larval 0.5 Hz bout loop remains contrary."}
```
