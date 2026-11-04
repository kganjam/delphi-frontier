# Replication of claim 228: the S29 launch-energy shortfall

**Status:** an independent re-derivation. Every number below is **calculated**, and none of it is a new measurement. Reproduce it with `python3 docs/research/fish/replicate_228_calc.py`.

**Claim under test (S29, `docs/research/fish/S29-organism.md` on branch `claude/s29-launch-energy-2iuixr`):** a latch-mediated spring (LaMSA) launch of a 0.40 g teleost to 4.37 m/s falls short on energy per stroke by about 1.86× (1.22–3.08×). Every wing route falls short by 10× or more.

## Blinding: what I saw, and when

- **The task prompt itself contained the headline value**, "~1.86x (1.22-3.08)". So I was not blind to the number, only to how it was reached.
- In `S29-organism.md` I first read only:
  - the title and the status/dependency lines;
  - §1.1, the muscle power table;
  - §2.1, which gives m = 0.40 g, V = 4.37 m/s, KE = 9.55 J/kg, and the 5.53 m/s mass-consistent caveat.
- I skipped §0 (the short answer), §2.3, §5 and §6, which hold their working. I read those only **after** my estimate and script were written; see "Comparison".
- §2.1 also stated S28's "10.03×" energy gap. I did not use it.

## Method (my own framing)

shortfall = (energy the spring must store, per kg body) / (energy one muscle contraction can load into the spring, per kg body)

shortfall = (KE / η) / (W · f)

- KE is the kinetic energy at the target speed.
- η is the overall efficiency from stored spring energy to body kinetic energy.
- W is the work one contraction can do per kg of muscle.
- f is the fraction of body mass that is muscle loading the spring.

Slow loading of a spring escapes the force–velocity penalty. So W is the single-contraction work, not fast-start cycle work. I nonetheless kept fish cycle work as the pessimistic end of the range.

## Inputs

| Input | Value used | Source | Read-level |
|---|---|---|---|
| Body mass m | 0.40 g | S29 §2.1 (brief) | full-text (repo) |
| Target speed V | 4.37 m/s (alt. 5.53 m/s) | S29 §2.1, from S28 | full-text (repo); S28 not read |
| KE | ½V² = **9.548 J/kg body** (3.819 mJ) | my arithmetic | calculated |
| W, frog plantaris single contraction | 26.6–31 J/kg muscle | Roberts & Marsh 2003, J Exp Biol 206:2567 | search-summary (silverchair PDF not fetched; PubMed host blocked by network policy) |
| W, Cuban tree frog, whole hindlimb | up to 60 J/kg muscle | Marsh (as returned by search) | search-summary |
| W, fish fast muscle, one C-start cycle | 142.7 W/kg ÷ 15 Hz = **9.51 J/kg muscle** | 142.7 W/kg: Wakeling & Johnston 1998, J Exp Biol 201:1505 (abstract text via search). 15 Hz C-start cycle frequency: an indexed abstract that the search tool flagged as possibly mixed with another paper | search-summary. **The division is my inference**: it assumes work-loop power = work × frequency at 15 Hz |
| f, myotomal muscle fraction | 0.30–0.60 (Webb 1978: up to 0.55; a 2009 J Fish Biol paper: c. 0.60; a review: 30–80 %) | as cited in search results | search-summary; primaries not read |
| η, spring → body KE | 0.5–0.9 | **ASSUMED** by me (elastic return ~0.9, less unquantified losses) | none. This is an assumption, not a sourced value |

## Arithmetic

KE = 0.5 × 4.37² = 0.5 × 19.097 = 9.548 J/kg body.

| Case | W (J/kg muscle) | f | η | Required KE/η (J/kg body) | Available W·f (J/kg body) | Shortfall |
|---|---|---|---|---|---|---|
| Central | 24 | 0.45 | 0.7 | 13.64 | 10.80 | **1.26×** |
| Frog plantaris | 31 | 0.45 | 0.7 | 13.64 | 13.95 | 0.98× |
| Fish cycle work | 9.51 | 0.45 | 0.7 | 13.64 | 4.28 | 3.19× |
| Optimistic | 60 | 0.60 | 0.9 | 10.61 | 36.00 | 0.29× |
| Pessimistic | 9.51 | 0.30 | 0.5 | 19.10 | 2.85 | 6.69× |

Monte Carlo (200,000 draws, seed 228) with W log-uniform on 9.51–60, f uniform on 0.30–0.60, and η uniform on 0.5–0.9:

| Target | Median | 5–95 % | P(shortfall ≥ 1) | P(shortfall ≥ 10) |
|---|---|---|---|---|
| 4.37 m/s | 1.30× | 0.51–3.39× | 0.64 | 0.000 |
| 5.53 m/s | 2.10× | 0.81–5.43× | 0.88 | 0.000 |

## My value

**About 1.3× short (5–95 %: 0.5–3.4×) at 4.37 m/s, and about 2.1× (0.8–5.4×) at 5.53 m/s.** Both are calculated, not observed.

On my inputs the launch-energy route is within a factor of ~3 of closing, and in a minority of draws it closes. I find no plausible input set that reaches 10×.

## Comparison with the recorded value (read only after the above)

S29 §5 and §6 use this structure:

supply = f · w · η_spring(0.93) · η_h(0.37)

- The need is 10.17 J/kg body. That is the 9.55 J/kg KE plus 0.250 mJ of drag work (0.625 J/kg).
- f = 0.30. They assume one side of a 60 % axial muscle mass.
- w = 53 J/kg muscle (range 32–81), from Mendoza & Azizi 2021.
- η_h = 0.37: pike C-start hydromechanical efficiency, Frith & Blake.
- Result: 10.17 / (0.30 × 53 × 0.93 × 0.37) = 10.17 / 5.47 = **1.86×**.

**My post-hoc check of their inputs:**
- **w:** I fetched Mendoza & Azizi 2021, J Exp Biol 224:jeb243180 (PMC10658917). Read-level: full-text, via an automated page summary. It gives Cuban tree frog **53 J/kg muscle, range 32–81**, bullfrog ~37 and cane toad ~22. So their w input is confirmed.
- **η_h:** I did not read Frith & Blake.
- **Arithmetic:** with my script at W = 53, f = 0.30, η = 0.93 × 0.37 = 0.344, I get 1.75×. Scaling by their drag-inclusive need (10.17 / 9.55) gives **1.86×**. Their arithmetic reproduces.

**Where we differ, and why:**

1. **Efficiency (the main difference).** My η = 0.5–0.9 ignored the loss from pushing off water. Their η_h = 0.37 is a measured value, though from pike, a much larger fish at higher Reynolds number. This one term roughly doubles the required energy.
   - Their author's point is that a fish has no rigid reaction surface. **My inference:** that is physically right, and my η range was too generous.
2. **Muscle work and fraction (pull the other way).**
   - My W centre (24) is lower than theirs (53). Mine was anchored on plantaris-model and fish-cycle values; theirs is the measured spring-loading value.
   - My f centre (0.45) is higher than theirs (0.30).
   - These two partly cancel: W·f is 10.8 for me and 15.9 for them.
3. **Combined.** With my W·f and their η, I get 13.64 × (0.7 / 0.344) / 10.8 ≈ 2.6×. Their 1.86× lies between my blind central (1.3×) and that figure.
4. **The lower bound differs.**
   - Their 1.22× floor comes from w = 81 and still assumes f = 0.30 and η_h = 0.37.
   - My lower tail falls below 1 because I allowed f up to 0.60 and η up to 0.9.
   - The author's own table also reaches 1.08× at f = 0.60, w = 53. So their stated range is conditional on the one-side, f = 0.30 assumption, not a full uncertainty band.

**Not checked:** the "≥10× for every wing route" comparator. I did not re-derive the wing routes (S28 and earlier), and only saw S28's 10.03× quoted in S29 §2.1. The comparison half of the claim therefore rests on their record, not on my work.

## Verdict

**I AGREE with the claim as framed: the shortfall is order 1–3×, and an order of magnitude closer than ≥10×.**

- My blind median of 1.3× (0.5–3.4×) overlaps their 1.86× (1.22–3.08×).
- I get P(shortfall ≥ 10) ≈ 0.
- I do **not** independently confirm that the route fails with certainty. Whether the shortfall exceeds 1 depends on the hydromechanical efficiency (their 0.37, from pike) and on the loading-muscle fraction (their 0.30, assumed). Neither is measured for a 0.4 g teleost.

## Sources

- Roberts & Marsh 2003, J Exp Biol 206:2567: https://cob.silverchair.com/jeb/article/206/15/2567/20246/Probing-the-limits-to-muscle-powered-accelerations (search-summary)
- Wakeling & Johnston 1998, J Exp Biol 201:1505: https://www.sciencegate.app/document/10.1242/jeb.201.10.1505 (search-summary)
- Mendoza & Azizi 2021, J Exp Biol 224:jeb243180: https://pmc.ncbi.nlm.nih.gov/articles/PMC10658917 (full-text via automated summary; read post-comparison)
- Fish muscle mass fraction (Webb 1978 as cited; J Fish Biol 2009): https://cob.silverchair.com/jeb/article-pdf/119/1/71/2435905/jexbio_119_1_71.pdf (search-summary)

```swarm-replication
{"claim_id": 228, "my_value": "~1.3x (5-95%: 0.5-3.4x) at 4.37 m/s; ~2.1x (0.8-5.4x) at 5.53 m/s", "agrees": true,
  "note": "Blind estimate overlaps 1.86x (1.22-3.08x) and is far below 10x; the difference in central value comes mainly from S29's measured pike push-off efficiency (0.37), which I omitted, offset by my lower muscle work, and the >1 'fails' conclusion is not independently confirmed."}
```
