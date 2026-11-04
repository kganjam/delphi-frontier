# Replicate claim 237: exocoetid flight is a multi-stroke task

**What this is:** an independent re-derivation of how much of an exocoetid's take-off energy a single impulse can supply. I worked from the inputs listed in S30-organism.md §1–§2. S30 sits on branch `claude/s30-launch-budget-mass-k71prf`, commit `59f421da`.

**What I did not read:** I stopped before S30 §3.2–§3.3, which state S30's own result. I read them only after finishing §1–§4 below. I found a file called `docs/research/fish/challenge-237.md` on branch `claude/exocoetid-flight-challenge-fnngf6` and did not open it.

**Every number below is CALCULATED unless it is labelled otherwise. None of them is an observation.**

## 1. The question as I reconstructed it

The question text I was given was truncated after "one launch, one impulse -- does". I took the quantity at stake to be this: **the fraction of the required take-off kinetic energy that one impulse supplies to a real exocoetid**, R = supply/need, and the number of impulses that implies, N ≈ 1/R.

- If R is well below 1 across exocoetid masses, the claim "multi-stroke, not single impulse" holds.
- The relevant mass range is 3–530 g, from Fish 1990 as transcribed by the project.

## 2. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Single-impulse supply ÷ need at the anchor, R₀ (LaMSA, one-sided axial muscle) | 0.324 / **0.538** / 0.822 for w = 32 / 53 / 81 J/kg muscle; 1.076 with all muscle | S30 §2.1, from S29; the muscle work figures are from Mendoza & Azizi 2021 | listing (I took S30's numbers as given; I did not read S29 or Mendoza & Azizi) |
| Anchor mass m₀ (LaMSA) | 0.25 g | S30 §2.1, from S28 | listing |
| Muscle-only R₀ at 0.40 g | 0.0853, which is (1.38/4.73)² | S30 §2.3; Miln 2021 via S28 | listing |
| Need exponent β (V_to² ∝ wing loading ∝ m^β) | 1/3 geometric; 0.360–0.533 measured | Fish 1990 Tables I–II, as transcribed by the project | listing (via S30; the paper itself was not read) |
| Supply exponent α | 0 for LaMSA; 0–0.222 for muscle | Sutton et al. 2019 via S30; the 2/9 upper bound is derived in S30 | listing |
| Exocoetid masses | 3–530 g | Fish 1990 via S30 | listing |
| Taxiing exists: the tail beats in the water at up to 50 beats s⁻¹, with the fins spread, until take-off speed | — | Davenport 1994, "How and why do flying fish fly", quoted in a search result | search-summary |
| Tail-beat rate of 50–70 s⁻¹ during taxiing; peak speed ~15–20 m/s | — | bioRxiv 10.1101/765560 | search-summary (full text not opened) |
| Tail on the water surface at 13.5 Hz | — | APS March Meeting 2024 abstract s27/13 | search-summary |
| Wing loading of a 0.30 m *Cypselurus*: 176 N m⁻²; CL_max 1.07 (an assumption) | — | S30 §3.2, used only to check S30's arithmetic | listing |

The tail-beat sources disagree: 50–70 Hz against 13.5 Hz. I have kept both figures. Either rate means many strokes per take-off.

## 3. Arithmetic

R(m) = R₀ · (m/m₀)^(α−β), and N = 1/R.

All values below are CALCULATED:

| Route | β | R at 3 g | N at 3 g | R at 300 g | R at 530 g | N at 530 g |
|---|---|---|---|---|---|---|
| LaMSA, w = 53 (central) | 1/3 | **0.235** | **4.3** | **0.051** | **0.042** | **24** |
| LaMSA, w = 53 | 0.533 | 0.143 | 7.0 | 0.012 | 0.0091 | 110 |
| LaMSA, w = 32 | 0.533 | 0.086 | 11.6 | 0.0074 | 0.0055 | 183 |
| LaMSA, w = 81 | 1/3 | 0.359 | 2.8 | 0.077 | 0.064 | 15.6 |
| LaMSA, all muscle | 1/3 | **0.470** | **2.1** | 0.10 | 0.084 | 11.9 |
| Muscle, α = 0 | 0.533 | 0.029 | 34 | 0.0025 | 0.0018 | 541 |
| Muscle, α = 0.222 | 1/3 | 0.068 | 14.7 | 0.041 | 0.038 | 26 |

How to read the table:
- The central value is LaMSA with w = 53 and β = 1/3. At 3 g: R = 0.538 × (3/0.25)^(−1/3) = 0.538 / 2.289 = 0.235.
- At 530 g: 0.538 / 2120^(1/3) = 0.538 / 12.85 = 0.042.
- **The bound across the whole envelope:** R ≤ 0.47 at 3 g, which is the most generous combination, and R ≤ 0.10 at 300–530 g.

Check on what one stroke can reach (CALCULATED):
- One-stroke supply under the S29 budget is about 5.5 J/kg, which gives V = √(2 × 5.5) ≈ **3.3 m/s**.
- With all muscle it is about 10.9 J/kg, which gives ≈ **4.7 m/s**.
- Neither changes with mass on the LaMSA route.

## 4. My value

**One impulse supplies R ≈ 0.04–0.24 of the required take-off kinetic energy for a 3–530 g exocoetid.** This is calculated, with the central case at the ends of the mass range.

- Full envelope: 0.002–0.47.
- So a real exocoetid needs about **4–24 single-impulse equivalents** (envelope 2–540).
- R < 1 at every combination of inputs, so the qualitative claim holds robustly. The numerical value is uncertain to about an order of magnitude.
- N = 1/R counts only energy. It ignores drag losses between strokes, so the real number of strokes would be higher than these counts.

There is observational support that the mechanism is multi-stroke, though only at search-summary level: surface taxiing at tail-beat rates of tens per second (Davenport 1994, bioRxiv 765560). I found no source on how the smallest exocoetids (1–3 g) take off. That search was two web searches, standard mode.

## 5. Comparison with the recorded value (read after §1–§4)

S30 §3.2 gives "**One stroke delivers (10/16.4)² = 37 %** of the needed KE" for a 300 g *Cypselurus*. Its §3.3 then concludes that the task is multi-stroke.

- **S30's arithmetic checks out (CALCULATED):** √(2 × 176 / (1.225 × 1.07)) = 16.39 m/s, and (10/16.39)² = 0.372.
- **The qualitative conclusion matches:** one impulse falls short of what is needed, so take-off is multi-stroke. **AGREE.**
- **The number does not match:**
  - My calculated single-impulse fraction at 300 g is **0.051** in the central case, with an envelope of 0.0025–0.10. That is about 7× below 37 %.
  - S30's 37 % rests on a "~10 m/s underwater speed before exit". That figure is search-summary level, and it is not a single-impulse quantity. Under S29's own budget, one stroke reaches only about 3.3–4.7 m/s. Reaching 10 m/s takes about 50 J/kg, which is roughly 5–9 strokes' worth.
  - So the 10 m/s exit speed is itself very likely the product of many underwater tail beats. Labelling (10/16.4)² as "one stroke delivers" conflates *exit speed* with *one-stroke speed*. **This is my inference, not something S30 states.**
  - Correcting it strengthens the claim rather than weakening it.
- **Verdict:** I AGREE with the claim (multi-stroke). I DISAGREE with the 37 % one-stroke figure as stated; my value is about 5 % at 300 g, envelope 0.25–10 %.

## Sources

- S30-organism.md, branch `claude/s30-launch-budget-mass-k71prf`. Read-level: full-text for §1–§2 and §3.1 before deriving; §3.2–§3.3 read after.
- Davenport 1994, quoted in a search result: https://www.biorxiv.org/content/10.1101/765560.full.pdf. Read-level: search-summary.
- APS March Meeting 2024, s27/13: https://meetings-archive.aps.org/mar/2024/s27/13. Read-level: search-summary.
- Park & Choi 2010, J. Exp. Biol. 213:3269. Read-level: search-summary. No number from it is used.

```swarm-replication
{"claim_id": 237, "my_value": "one impulse supplies ~0.04-0.24 of required take-off KE for 3-530 g exocoetids (central; envelope 0.002-0.47), i.e. ~5% (0.25-10%) at 300 g -> ~4-24 impulse-equivalents needed (calculated)", "agrees": true,
  "note": "Agree that exocoetid take-off is multi-stroke (R<1 everywhere); disagree with S30's '37% from one stroke' because its 10 m/s exit speed is itself multi-stroke, and the single-impulse budget gives ~5% at 300 g."}
```
