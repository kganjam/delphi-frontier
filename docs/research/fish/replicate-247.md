# Replicate 247: blind re-derivation of claim 247 (replication of S10 "sustained flapping is not supported")

## 0. What I saw, and in what order

- The task pointed to `replicate-203.md` on branch `claude/s10-flapping-power-rederivation-ygs05k` as
  the place where the inputs live. That file **is** the prior derivation. I read **only its first
  30 lines**: the title, §0 (its access notes) and §1 (its framing). §1 told me the question:
  can sustainable red/slow fish muscle supply the minimum mechanical power for level flapping flight
  of a 0.05–0.3 kg flier? It also told me the method: requirement per kg muscle = (P_min/m)/f.
  **Once I reached its "## 2. Inputs" header I stopped reading** and saw no numbers from it.
  Contamination: my mass range (0.05–0.3 kg) and my per-kg-muscle framing come from that file. They
  are not independent choices.
- Nothing about S10 or flapping exists on this branch's working tree. I checked with `ls` on
  `docs/research/fish` (the directory does not exist on this branch) and a `grep` for `S10|flapping`
  over all `*.md` files, which found nothing.
- I finished §1–§3 and ran the script before searching for the recorded value (§4).

## 1. Method (all calculated, nothing observed)

I used the Pennycuick-style minimum-power model for level flight:

- Induced power: P_ind = k (mg)² / (2 ρ V S_d), with S_d = π b²/4.
- Parasite power: P_par = ½ ρ V³ S_b C_Db.
- I minimised P_ind + P_par over V (grid step 0.005 m/s), which gives V_mp.
- Profile power: P_pro = (8.4/AR) · P_am, where P_am = 1.05 k^¾ m^{3/2} g^{3/2} S_b^¼ C_Db^¼ / (ρ^½ b^{3/2}).
- Total: P_min = P_ind + P_par (at V_mp) + P_pro.
- Requirement per kg muscle = (P_min/m) / f.

I compared mechanical power with mechanical power, so muscle efficiency cancels out.

## 2. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| g, ρ | 9.81 m/s², 1.225 kg/m³ | standard sea-level constants | n/a |
| k (induced factor) | 1.2 | Pennycuick convention, recalled from training. Not fetched this session | could-not-access |
| Span b | 1.17 m^0.39 m (0.36–0.73 m over 0.05–0.3 kg) | Bird span allometry (Rayner/Norberg-type), recalled from training. **This is my assumption that the flier has bird-like wings.** | could-not-access |
| Body frontal area S_b | 0.00813 m^0.666 m² | Pennycuick 2008 *Modelling the Flying Bird*, recalled | could-not-access |
| C_Db | 0.10 | Pennycuick 2008, recalled | could-not-access |
| AR (profile-power factor) | 7 → 8.4/AR = 1.2 | Pennycuick convention, recalled | could-not-access |
| Muscle fraction f | 0.05, 0.10, 0.17, 0.25 | Bracket I chose. 0.17–0.25 is bird-like flight-muscle fraction (recalled). 0.05–0.10 is fish-like red-muscle fraction (recalled, not verified) | assumption |
| Available sustainable fish red-muscle power | **10–28 W/kg muscle** at 20 °C (bass slow fibres plateau ~10 W/kg at 3–5 Hz; scup red muscle 27.9 W/kg at 20 °C, 12.8 at 10 °C) | WebSearch summary of JEB work-loop papers (scup: Rome & Swank 1992, JEB 171:261; bass: Coughlin-type modelling study) | search-summary |
| Outlier: skipjack tuna deep red muscle | ~79–133 W/kg at 25 °C, 5 Hz | same WebSearch summary. Tuna are regionally endothermic, so this is not an ectotherm value | search-summary |
| Sanity check: mallard pectoralis in slow flight | 17 W/kg body, 131 W/kg muscle (3 m/s, not V_mp) | WebSearch summary of a JEB mallard study | search-summary |

All work-loop values are in-vitro **maxima** at optimal strain and phase. Sustained in-vivo output
is presumably lower; that is my inference, not something I measured or read.

## 3. Arithmetic and result

Output of `docs/research/fish/replicate-247_calc.py` (calculated):

```
m_kg  span_m  Vmp_m/s  Pmin_W  Pmin_W/kgbody  req_W/kgmuscle(f=0.05,0.10,0.17,0.25)
0.05  0.364    8.64   0.385     7.7      154      77      45      31
0.10  0.477    9.52   0.814     8.1      163      81      48      33
0.20  0.625   10.47   1.722     8.6      172      86      51      34
0.30  0.732   11.08   2.670     8.9      178      89      52      36
```

Worked example at 0.1 kg: P_min = 0.814 W, and 0.814 / 0.1 = 8.1 W/kg body.

- At f = 0.10: 81 W/kg muscle.
- At f = 0.25: 33 W/kg muscle.

**My value (calculated):**

- **The minimum power requirement is ≈ 8 W/kg body (7.7–8.9) for bird-proportioned wings.** I put
  the uncertainty at about ±40%, driven by k, C_Db and span. **Span dominates:** P_ind ∝ 1/b².
- That is ≈ 31–89 W/kg of flight muscle at f = 0.25–0.10.
- **Available ectotherm red-muscle power is 10–28 W/kg** (work-loop maxima, search-summary).
- **The shortfall is ×1.1–1.3 at f = 0.25 and ×2.9–8.9 at f = 0.10.**

**Inference:** sustained flapping is not supported for an ectotherm fish. At a bird-like 25% muscle
fraction, with generous bird-like wings, the gap is thin (~1.2×). Tuna-grade warm red muscle
(~133 W/kg) would close it at f ≥ ~0.07. That figure is search-summary only, and the muscle is
endothermic.

## 4. Comparison with the recorded value (searched only after §3)

I searched `git grep` over remote branches matching `flapping|s10|203|247`. On
`origin/claude/challenge-flapping-power-replication-afsgel`, `challenge-247.md` quotes claim 247:

> "Replication (blind): ~16 W/kg body = 65-165 W/kg flight muscle at f=0.10-0.25; at 0.4 g hover
> ~33 W/kg muscle, forward flight ~10-14 W/kg muscle; available ectotherm red muscle up to ~28 W/kg"

Recorded value: **28 W/kg** (fish red-muscle maximum, search-summary).

- **Comparator (28 W/kg): AGREE.** I got the same 27.9 W/kg scup figure. But I reached it through
  the same kind of search (search-summary), very likely from the same paper. So this agreement is
  **weak evidence**: two reads of one source, not two sources.
- **Requirement (W/kg body): DISAGREE by ×2.** I got ~8.1 W/kg body at 0.1 kg; the claim says ~16.
  - `challenge-247.md` lists the blind case as "0.1 kg, b = 0.3 m".
  - Re-running my own model with b fixed at 0.30 m gives **16.3 W/kg body, V_mp 12.0 m/s, and 163/65
    W/kg muscle at f = 0.10/0.25**. That reproduces the claim exactly. The sensitivity line was
    appended to the script after the comparison.
  - So the whole difference is the assumed span: 0.30 m (short, flying-fish-like) versus 0.48 m
    (bird allometry). Neither of us measured it. I do not have a measured flying-fish span-to-mass
    value; that is `unknown`, and I did not search for it.
- **Verdict ("sustained flapping not supported"): AGREE.** The two requirements disagree, but both
  exceed 28 W/kg in every case. Mine only just exceeds it at f = 0.25: 31–36 vs 28.
- **I did not re-derive the 0.4 g hover and forward-flight sub-claims** (33 and 10–14 W/kg muscle).
  I CANNOT TELL on those.

Overall: **AGREE** on the recorded value (28 W/kg) and on the verdict. I disagree on the
requirement's magnitude by ×2, which traces entirely to the span assumption. With bird-proportioned
wings, the margin at f = 0.25 shrinks from the claim's ~2.3× to ~1.2×.

## Sources

- [Rome & Swank, influence of temperature on power output of scup red muscle (JEB 171:261)](https://cob.silverchair.com/jeb/article/171/1/261/6442/The-influence-of-temperature-on-power-output-of) — search-summary
- [Modeling red muscle power output during steady and unsteady swimming in largemouth bass](https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/39544925) — search-summary
- [Tu & Daniel, power (skipjack red muscle)](https://faculty.washington.edu/danielt/Tu%26DanielPower.pdf) — search-summary
- [JEB 204:3 495 (mallard pectoralis power)](https://cob.silverchair.com/jeb/article-pdf/204/3/495/2609498/jexbio_204_3_495.pdf) — search-summary
- Pennycuick 2008, *Modelling the Flying Bird* (model constants) — could-not-access; recalled from training

```swarm-replication
{"claim_id": 247, "my_value": "requirement ~8.1 W/kg body (7.7-8.9, +/-40%) = 31-89 W/kg flight muscle at f=0.25-0.10 (calculated, bird-allometry span); available ectotherm red muscle 10-28 W/kg (search-summary)", "agrees": true,
  "note": "Agree on the 28 W/kg comparator (same scup source, so weak independence) and on the not-supported verdict, but my requirement is half the claim's 16 W/kg body because I assumed bird-allometric span (0.48 m) not 0.30 m; with b=0.30 m my model reproduces 16.3 W/kg body exactly, and at f=0.25 the margin shrinks to ~1.2x."}
```
