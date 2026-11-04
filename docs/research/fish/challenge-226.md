# Challenge 226: "POWER PASSES"

**Claim under review** (S29, `docs/research/fish/S29-organism.md` on branch `claude/s29-launch-energy-2iuixr`, line 12, §6 table, swarm-result):

> POWER PASSES: a 5–14 ms release needs 7,400–18,400 W/kg muscle. That is 1.3–3.2× beyond measured fish LaMSA (5,795 W/kg, pipefish) but WITHIN measured insect LaMSA (36,000–74,000 W/kg, froghopper).

Recorded evidence level: derived. Value: 18,400 W/kg muscle.

**Verdict: WEAKENED.**
- The arithmetic is correct.
- The fish ratio compares the S29 **mean** demand with a pipefish figure that is a **peak instantaneous** value. Matched peak to peak, the gap is **2.0–6.3×, not 1.3–3.2×**.
- The insect comparison is mean against mean and survives.
- The headline conclusion survives: power is not the binding term.

---

## 1. Independent arithmetic

I recomputed from the stated inputs without reusing the S29 script's code path (my own one-off Python):
- m = 0.40 g, V = 4.37 m/s.
- ρ = 1000 kg m⁻³, Cd = 0.2, A = 24 mm².
- η_h = 0.37.
- Constant acceleration, so t = 2s/V.
- One side of the axial muscle, f = 0.30 of body mass, i.e. 0.12 g.

| Stroke s | t | KE + drag work | ÷ η_h (spring output) | Mean power | Per kg muscle (f = 0.30) |
|---|---|---|---|---|---|
| 1.09 cm | 4.99 ms | 3.819 + 0.250 = 4.069 mJ | 11.00 mJ | 2.205 W | **18,372 W/kg** |
| 3.00 cm | 13.73 ms | 3.819 + 0.688 = 4.507 mJ | 12.18 mJ | 0.887 W | **7,393 W/kg** |

Results:
- This reproduces the claim's 7,400–18,400 W/kg exactly.
- It also matches the S29 script's printed output, which I ran (`S29_launch_energy.py`, section 5).
- 18,372 / 5,795 = 3.17 and 7,393 / 5,795 = 1.28, which is the claim's 1.3–3.2×.
- 18,372 / 36,000 = 0.51 and 7,393 / 74,000 = 0.10.

**There is no arithmetic error.**

## 2. The defect: peak compared with mean

The claim's 7,400–18,400 is the **mean** power over the release. The S29 script calls it `p_mean`, and the S29 §6 table says "mean".

I checked how each literature value is defined.

### Pipefish, 5,795 W/kg: a peak value
Van Wassenbergh et al., J. R. Soc. Interface 5:285 (PMC2607401). Read level: **full-text, via a WebFetch extraction**, so the quotes passed through a summarising model.
- The paper states: *"A peak instantaneous muscle-mass-specific power requirement of 5795 W kg−1 was calculated by the model"*.
- The peak is reached 1.5 ms into the strike.
- The paper reports no mean over the rotation.
- S29's own table labels this value "(instantaneous)" but then divides a mean by it.

### Froghopper, 36,000–74,000 W/kg: a mean value
Burrows 2003, Nature 424:509. Read level: **search-summary**. I did not open the PDF.
- The figure is the jump energy (49 µJ average, 100 µJ best) divided by a conservatively assumed 1 ms acceleration time, normalised to the depressor muscles (~11 % of body mass).
- That makes it a mean over take-off, so the claim's insect comparison is like for like.

### The like-for-like fish comparison
S29 itself assumes constant force, under which peak = 2 × mean. A linear spring released into an inertial load gives peak = (π/2) × mean instead. This is my inference from P ∝ sin 2ωt over a quarter period.

| Release | Mean (claim) | Peak, π/2 profile | Peak, 2× (S29 assumption) | Peak ÷ pipefish peak |
|---|---|---|---|---|
| 13.7 ms | 7,393 | 11,613 | 14,786 | **2.0–2.6×** |
| 5.0 ms | 18,372 | 28,858 | 36,743 | **5.0–6.3×** |

**Corrected fish ratio: 2.0–6.3× beyond pipefish, not 1.3–3.2×.** The understatement is about 1.6–2×.
- It does not reverse the claim's direction: the demand is beyond fish LaMSA either way.
- It does widen the step a zebrafish would need to take beyond any measured fish system.

## 3. Hidden assumption: muscle-mass normalisation (f)

The claim normalises by one side of the axial muscle only (f = 0.30). Van Wassenbergh normalised by **both epaxial and hypaxial muscle** (32.2 + 16.5 mg in their largest fish), i.e. all of the muscle that could load the spring.

If I relax to f = 0.60 (all skeletal muscle, the S29 break-even case), the mean demand is **3,697–9,186 W/kg**:
- Mean ÷ pipefish peak: 0.64–1.59×. At a 14 ms release the demand is then *below* the pipefish peak.
- Peak ÷ pipefish peak: 1.0–3.2×.

So the fish ratio depends on f as much as on the peak/mean basis. The full honest range is roughly **1.0–6.3×**, set by f (0.30–0.60) and force profile.

The insect conclusion holds at every f. Even the worst case (f = 0.30, 5 ms) is a mean of 18,372 W/kg, against froghopper means of 36,000–74,000.

## 4. Other relaxations tested

**Mass-consistent target speed.** S29 itself says that at 0.40 g the S28 fin needs 5.53 m/s. Keeping t fixed, I get:
- **29,899 W/kg** mean at 5 ms.
- **12,318 W/kg** at 13.7 ms.

Both are still below the froghopper mean (36,000). "Within insect LaMSA" survives. The peak-matched fish gap rises to about 4–10×.

**Proxy check.** Muscle-normalised power is a **proxy**.
- It is the literature convention: the power muscle would need if it drove the movement directly.
- What actually limits a LaMSA release is how fast the spring and latch can release energy (Ilton et al. 2018 framing, not read by me).
- I computed spring-mass-specific output from the S29 spring volumes, with an **assumed** tendon density of 1,120 kg m⁻³:
  - **0.13–0.50 MW/kg spring** for mammal-grade tendon (3.9–15.6 mm³).
  - **22–40 kW/kg spring** at tuna-tendon strains (49–91 mm³).
- S29 cites mantis shrimp at 3.8 MW/kg spring (Patek 2023 review, ABSTRACT per S29). **I did not verify that figure.**
- On that basis, the right quantity also does not look binding. The proxy does not overturn the conclusion.

**Release time.** Whether a fish body axis loaded against water can actually release in 5–14 ms is **unknown**. I found no measurement and did not search beyond the two queries above. The claim takes the range as given.

## 5. Evidence level

"Derived" is honest. The 18,400 W/kg is computed, not measured, and S29 says so.

The defect is in the comparison, not the label: a derived mean is set against a measured peak. The headline wording "needs … W/kg muscle" also says nothing about it being a mean or about f = 0.30. The S29 §6 table states both; the claim text drops them.

## 6. Counter-examples searched

Scope: two web searches (Van Wassenbergh 2008; Burrows 2003) and one full-text fetch (PMC2607401).

- I found no fish LaMSA power density above 5,795 W/kg that would close the fish gap.
- I did not survey other insect, flea or click-beetle values. Burrows 2003 says click beetles are higher than froghoppers, which only strengthens "within insect".

## Sources

| Source | Read level |
|---|---|
| Van Wassenbergh et al., J. R. Soc. Interface 5:285 — [PMC2607401](https://pmc.ncbi.nlm.nih.gov/articles/PMC2607401) | full-text, via WebFetch summary |
| Burrows 2003, Nature 424:509 — [doi:10.1038/424509a](https://doi.org//10.1038/424509a), [PDF copy](https://www.olin.edu/sites/default/files/froghopper-burrows.pdf) | search-summary |
| S29-organism.md and S29_launch_energy.py (branch `claude/s29-launch-energy-2iuixr`) | full-text; script run |

```swarm-challenge
{"claim_id": 226, "outcome": "weakened", "reason": "Arithmetic reproduces exactly, but the 1.3-3.2x fish ratio divides the S29 MEAN demand by the pipefish PEAK instantaneous 5795 W/kg; peak-to-peak it is 2.0-6.3x (and 1.0-3.2x if normalised over all muscle as Van Wassenbergh did), while the insect within-range conclusion (mean vs mean) and 'power not binding' survive.",
  "corrected_value": "demand 7400-18400 W/kg muscle mean (unchanged); 2.0-6.3x beyond pipefish peak-matched at f=0.30 (not 1.3-3.2x)",
  "depends_on": ["S29 inputs: m=0.40 g, V=4.37 m/s, Cd=0.2, A=24 mm2, eta_h=0.37 (Frith-Blake), f=0.30 one-side muscle", "VanWassenbergh2008 5795 W/kg defined as peak instantaneous, normalised to epaxial+hypaxial mass", "Burrows2003 36-74 W/g as energy / assumed 1 ms mean", "peak/mean = pi/2 (spring) to 2 (S29 constant-force assumption)"]}
```
