# S1-D — Deepening S1: can a 0.4 g zebrafish reach takeoff speed from water?

Status: desk analysis only. **No experiment was run.** Every number below is tagged
**[observed]** (measured by the cited authors), **[calculated]** (computed by me from the inputs
named, in `s1_deepen_calc.py` beside this file), or **[assumed]** (my input, not retrieved).
Provenance per CONTRIBUTING-VERIFICATION rule 9: **retrieved** or **remembered**.

## 0. What was there to deepen

The recorded S1 answer handed to this task was **empty**. I searched this repository on both
branches (`claude/zebrafish-takeoff-deepen-2gwq0o`, `work/frontier-foundation`) with
`git grep -il "zebrafish|takeoff|flying fish"`: the only hits are two triage JSON files in
`findings/`, neither containing an S1 answer. So I cannot report what S1 concluded. I reconstruct
the question in its two possible readings and deepen both:

- **Reading A — aerial takeoff.** "Takeoff speed" in the flying-fish sense: the airspeed at which
  the fish's own lifting surfaces support its weight, `v_req = sqrt(2mg / (rho_air · S · C_L))`.
- **Reading B — ballistic exit.** Can it leave the water at all, i.e. is its exit speed high
  enough to throw its body clear of the surface, `h = v² / 2g` (drag-free, no entrained water:
  an upper bound).

The reconstructed S1 conclusion I test is: **"No to A; plausibly yes to B."**

## 1. Which input is the answer most sensitive to? (recomputed, not asserted)

Inputs: mass `m = 0.4 g` (given by the question); air density 1.20 kg m⁻³ and g = 9.81 m s⁻²
(standard); lifting area `S` and lift coefficient `C_L` **[assumed]** — I could not retrieve a
measured zebrafish pectoral-fin or planform area, so I bracket S = 1–4 cm² and C_L = 0.5–1.5;
adult standard length 3.5 cm **[assumed]**; and the fish's **maximum speed at the surface**, `v`.

In the S1-era input set the only speed I can source is Plaut (2000)'s **U_crit = 0.56 m s⁻¹**
**[observed, retrieved]**. Results of perturbing each input by ×2 **[calculated]**:

| Input perturbed (×2) | Reading A: lift/weight at v (S=2 cm², C_L=1) | Reading B: ballistic height |
|---|---|---|
| baseline, v = 0.56 m/s | 0.010 (needs ×104 in S·C_L·v²) | 1.6 cm = 0.46 SL — **does not clear its own body** |
| v × 2 = 1.12 m/s | 0.038 | 6.4 cm = 1.8 SL — **clears** |
| v ÷ 2 = 0.28 m/s | 0.002 | 0.4 cm = 0.11 SL |
| S × 2 or C_L × 2 | 0.019 | no effect |
| m × 2 (0.8 g) | 0.005 | no effect (h independent of m in this model) |

Required takeoff airspeed across the whole S × C_L bracket is **3.3–11.4 m s⁻¹** **[calculated]**.

- **Reading A** is not flipped by a ×2 error in *any single* input; it needs ~×100 in S·C_L·v².
  The input with the most leverage is still `v`, because it enters squared.
- **Reading B** *is* flipped by a ×2 error in `v`: at U_crit the fish cannot throw its centre of
  mass one body length (needs 0.83 m s⁻¹ **[calculated]**); at 2 × U_crit it clears it by ~2×.

**So the weakest, most decision-relevant input is the maximum (burst) speed, `v`.**

## 2. How well established is that input?

U_crit 0.56 ± 0.048 m s⁻¹ (15.5 SL s⁻¹, wild-type, 28 °C, N = 21) is a real measurement
**[observed]** — Plaut 2000, *J Exp Biol* 203:813, PMID 10648223, doi:10.1242/jeb.203.4.813.
**Read-level: abstract** (via Europe PMC).

But it is a **proxy**. U_crit is a *sustained*, incremental-velocity swim-tunnel speed; the
quantity a takeoff or leap draws on is the *burst / fast-start* peak speed over tens of
milliseconds. Using U_crit for takeoff is a sustained-for-burst substitution, and the direction
of the error is known in principle: burst speeds exceed U_crit. (That last statement is my
inference from the definitions, not a number from a source.) **Evidence level of the S1 input
for this purpose: measured, but for a different quantity — a proxy.**

## 3. Improving it: the real quantity

### 3a. Primary source found

**Demesmay et al. 2025, "Zebrafish fast muscle contractions avoid the mammalian requirement for
voltage-gated Na⁺ channels", *PLOS Biology* 23(11): e3003484, doi:10.1371/journal.pbio.3003484,
PMC12604801. Read-level: full-text** (Europe PMC full-text XML; results, methods, Fig 4 legend
read). Author-reported, for adult wild-type (control) zebrafish **[observed]**:

- escape response to a 1 g object dropped from ~30 cm into a 1.6 L tank, 3–4 fish per tank;
- filmed at **240 frames s⁻¹** on a phone camera (Xiaomi Redmi Note 13 Pro+), manual tracking in Fiji;
- fish 4–12 months, body length 2.6 ± 0.2 cm (4 mo) and 3.6 ± 0.2 cm (12 mo); minimum 11 per genotype;
- **"calculated maximal speed" 157 ± 27 cm s⁻¹** (mean ± SD), reached 8 ± 4 ms after response onset;
- **distance covered in the first 40 ms: 3.8 ± 0.8 cm.**

### 3b. How much to trust it — the author's claim vs my inference

- *Author's claim:* peak escape speed 1.57 m s⁻¹.
- *My inference:* the peak is differentiated from manually tracked positions at a 4.2 ms frame
  interval, and peak latency (8 ms) is about two frames. Differencing position over ~2 frames
  amplifies tracking error, and a *maximum* over noisy differences is biased **upward**. I cannot
  quantify the bias: the pixel scale is not reported in what I read.
- *Robust lower bound* **[calculated]**: 3.8 cm in 40 ms is a mean of **0.95 m s⁻¹**, and the peak
  over that window cannot be below its mean. This bound uses an integrated distance, so it is far
  less noise-sensitive than the peak.
- So the improved input is **v_burst ∈ [0.95, ~1.6] m s⁻¹** — 1.7× to 2.8× the U_crit proxy.
  This is a direct measurement of the right *kind* of quantity (burst), but taken from a
  horizontal escape in a small tank, not a surface-directed exit. Body mass was not reported.
  The 0.4 g ↔ ~3–3.6 cm size match is my assumption.
- **Raw data check failed:** the S1 Data file is described as containing "numerical data of S1,
  2D, 3B, 4C, S7D and S8B Figs". I downloaded it (`pbio.3003484.s015`, sha256
  `725686f12c17993a1cad14e130c0bdbee0dd6f41eaa408ba5e48746034d4ac1d`). It has **one sheet,
  containing only the Fig S1 resting-potential values**. The per-fish Fig 4C speeds are **not in
  the deposited file**, so I could not recompute the 1.57 m s⁻¹ myself. The Zenodo deposit
  (doi:10.5281/zenodo.17290038) was unreachable from this session (host blocked).

### 3c. Sources that disagree or could not be used

- **Miln, Ward & Seebacher 2021**, *R Soc Open Sci* 8:210146, PMC8025299 — **full-text** read.
  This paper measures adult zebrafish fast-start speed (fastest of four escapes, 120 fps) and
  U₁₀ sprint speed, but reports the values **only in figures**. The figure image was
  **could-not-access** (PMC served a captcha) and the figshare data (doi:10.6084/m9.figshare.c.5359401)
  was blocked. Its fast-start value is `unknown` to me. It could confirm or contradict Demesmay;
  I have not averaged anything in.
- **Flying-fish comparison.** Makiguchi et al. 2013, *Aquatic Biology* 18:105–111,
  doi:10.3354/ab00494 — leap speeds of *Cypselurus heterurus doederleini* **3.9–5.2 m s⁻¹**,
  measured with accelerometer loggers. **Read-level: search-summary**: int-res.com and doaj.org
  were blocked, so the abstract was never read directly. Davenport 1994, *Rev Fish Biol Fish*,
  doi:10.1007/BF00044128 — **listing** only. Deng et al. 2019 (bioRxiv) assumed 10 m s⁻¹
  underwater and simulated 16.5 m s⁻¹. That is a **simulation**, **search-summary**.
  These numbers frame the order of magnitude a specialist reaches. They are not zebrafish inputs.
- **Park & Choi 2010**, *J Exp Biol* 213:3269, doi:10.1242/jeb.046052 — **abstract**: C_L of a
  flying-fish model peaks at 30–35° attack. The abstract gives no numeric C_L, so my
  C_L bracket stays **[assumed]**.

### 3d. Negative searches, with scope

- *Zebrafish water-exit velocity / leap height out of water:* **none found.** Scope: Europe PMC
  query `zebrafish AND (jump OR jumping OR leap) AND (air OR "out of water" OR terrestrial)`
  (769 hits; top 10 titles screened); web search for "zebrafish jumping out of water leap height
  velocity". The zebrafish jumping papers found (Bai et al. 2026, doi:10.1016/j.bbr.2026.116414;
  Reed & Minicozzi 2024, doi:10.1016/j.zool.2024.126145; both **abstract**) concern
  **terrestrial** tail-flip jumps on land, not exits from water.
- *Adult zebrafish fast-start speed given as a number in the text:* Europe PMC open-access query
  (`"Danio rerio" AND (fast start | escape response | sprint speed) AND adult`, 61 full texts
  downloaded and regex-scanned). **Only Demesmay 2025 reported an adult zebrafish peak speed in
  text.** Controls: the scan's positive control (Miln 2021's "0.19 m s⁻¹" sentence) was found.
  A must-fail gibberish query (`TITLE:"zzqxjv flying zebrafish"`) returned 0 hits. Plaut 2000 was
  retrieved by PMID as a positive control for the search endpoint.
- *Measured zebrafish pectoral-fin / planform area:* not searched to completion. It stays
  **[assumed]**, and section 4 shows it cannot matter.

### 3e. What measurement would settle it

Film adult wild-type zebrafish, with their mass measured, startling **toward the surface** under
a raised lid, using a high-speed camera at ≥1000 fps with a calibrated scale. Read the **exit
speed** and **apex height** directly. That replaces both the proxy and the horizontal-escape
substitution. The cost is a few days of bench time in any lab that already has a high-speed
camera. (That is my estimate, not a sourced figure.) A cheaper partial step: obtain the per-fish
Fig 4C values from the Demesmay authors or their Zenodo deposit, and Miln 2021's figshare data.

## 4. Recompute with the improved input [calculated]

| v (m s⁻¹) | L/W, S=2 cm², C_L=1 | L/W, S=4 cm², C_L=1.5 (generous) | Ballistic h_max |
|---|---|---|---|
| 0.56 (U_crit proxy) | 0.010 | 0.029 | 1.6 cm = 0.46 SL |
| **0.95 (40-ms mean, lower bound)** | 0.028 | 0.083 | 4.6 cm = 1.3 SL |
| **1.57 (author's peak)** | 0.075 | 0.226 | 12.6 cm = 3.6 SL |
| 1.84 (peak + 1 SD) | 0.104 | 0.311 | 17.3 cm = 4.9 SL |

- **Reading A — aerial takeoff: STANDS.** Even at peak + 1 SD with a generous 4 cm² and
  C_L = 1.5, lift is ≤ 31% of weight. At 1.57 m s⁻¹ and C_L = 1, the fish would need
  **26.5 cm²** of lifting surface **[calculated]**. That is roughly an order of magnitude more
  than any plausible silhouette of a ~3.5 cm fish, which is my estimate (**[assumed]**, not
  measured). The speed shortfall against the central case (S = 2 cm², C_L = 1, v_req = 5.7 m s⁻¹)
  is **3.6×**. The improved input *narrows* the margin, from ~10× to ~3.6× in speed. It does
  not close it. So the honest verdict is "stands", not "strengthens".
- **Reading B — ballistic exit: moves from marginal to supported.** With the U_crit proxy, the
  drag-free model says the fish cannot throw itself one body length (0.46 SL). With the
  noise-robust lower bound of 0.95 m s⁻¹, it clears 1.3 SL. These are upper bounds: water drag,
  the added mass of entrained water, and a non-vertical exit all reduce them. The burst
  measurement was horizontal, in a 1.6 L tank. So this reading is supported **[calculated]**,
  not observed. No zebrafish water-exit measurement was found.

**Overall verdict on the reconstructed S1 conclusion ("cannot reach aerial takeoff speed"):
STANDS.** The decisive input was a sustained-speed proxy. Replacing it with a measured burst
speed (0.95–1.57 m s⁻¹) raises it by 1.7–2.8×, and the conclusion survives with a ≥3.6× speed
gap. The input that remains unmeasured is the fish's actual water-exit speed, so the ballistic
reading should not be written up as observed.

```swarm-result
{"subproblem": "S1-D", "evidence": "measured-proxy-replaced: burst speed from one full-text primary study (Demesmay et al. 2025, 240 fps, n>=11), per-fish data not deposited; lift inputs assumed; result calculated", "answer": "No: replacing Plaut's sustained U_crit (0.56 m/s) with a measured adult escape burst speed (0.95 m/s robust lower bound, 1.57 m/s reported peak) still leaves a 0.4 g zebrafish ~3.6x short of the ~5.7 m/s airspeed its body could need to support its weight in air (calculated), although the same speed would, drag-free, suffice to throw it clear of the water (calculated, not observed).", "key_number": "adult zebrafish escape speed 0.95 m/s (40-ms mean, lower bound) to 1.57 +/- 0.27 m/s (reported peak)", "verdict": "stands"}
```
