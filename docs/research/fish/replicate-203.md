# Replicate 203: [S10] "Sustained flapping is not supported"

Independent re-derivation. I was given the question with the answer removed, plus the pointer
`harvest:s10-tissue-flapping-power-2kag3x`.

## 0. What I could and could not see, in order

- No branch or file named `harvest:s10-tissue-flapping-power-2kag3x` or `S10-tissue` exists on this
  branch. I grepped for `flapping`, `harvest`, `2kag3x` across the whole working tree and found
  nothing. `git ls-remote` showed no branch with `harvest` in its name. So **the inputs were not
  available to me**, and I did not know the organism, mass or flight mode the claim assumes.
- The remote has related branches: `fish-flapping-power-challenge-*`, `deepen-s10-*`,
  `replicate-184-flapping-muscle-*` and `challenge-s10-d-*`. I listed **filenames only**
  (`git diff --stat`) and **did not read** them before finishing §1–§3 below.
- After §1–§3 were finished and the script had run, I read
  `docs/research/fish/challenge-203.md` (branch `claude/fish-flapping-power-challenge-bquvmd`).
  It quotes the recorded claim. That read is used only in §4–§5, and I flag every number that
  depends on it.

## 1. My framing (chosen blind)

Can sustainable ("aerobic", red/slow) fish muscle supply the **minimum mechanical power for level
flapping flight**? I tested a fish-sized vertebrate flier of 0.05–0.3 kg (flying-fish scale; my
assumption). I compared mechanical power with mechanical power, so efficiencies cancel.

Requirement per kg of flight muscle = (P_min / body mass) / f, where f is the flight-muscle mass
fraction.

## 2. Inputs

### Measured inputs (sustainable fish muscle power, per kg muscle)

| Value | What | Source | Read-level |
|---|---|---|---|
| 27.9 W/kg at 20 °C; 12.8 W/kg at 10 °C | scup red muscle, work-loop maximum | Rome & Swank 1992, *J. Exp. Biol.* 171:261 ("The influence of temperature on power output of scup red muscle during cyclical length changes") | search-summary |
| ~10 W/kg plateau at 3–5 Hz | largemouth bass red muscle, modelled from in-vivo strain plus work loops | "Modeling red muscle power output during steady and unsteady swimming in largemouth bass" (authors and year not confirmed) | search-summary |
| 27.5 → 16.4 W/kg (10 cm → 60 cm cod) | cod, steady-state maximum per kg wet muscle; fibre type not confirmed by me | source not identified in the summary (`unknown`) | search-summary |
| 79 (anterior) / 133 (posterior) W/kg | skipjack tuna red muscle (an endothermic, warm red-muscle specialist) | Syme & Shadwick 2002, *J. Exp. Biol.* 205:189 (DOI listing in results) | search-summary |
| Science 261:340–343 | Rome, Swank & Corda 1993 "How fish power swimming" | the paper itself; it gave me no W/kg values | listing |

### Cross-check (bird flight muscle, not used in the verdict)

| Value | What | Source | Read-level |
|---|---|---|---|
| 70.2 W/kg | pigeon pectoralis, level flight, 5–6 m/s, 8.7 Hz | Biewener, Corning & Tobalske 1998, *J. Exp. Biol.* 201:3293 | search-summary |
| 51 W/kg (level), 119 W/kg (take-off) | pigeon pectoralis | Dial & Biewener 1993 | search-summary |
| 16.1 W/kg **body** | pigeon slow level flight | cited in the same search results; primary paper not identified | search-summary |

Fetches of `cob.silverchair.com` (JEB PDFs) and `pubmed.ncbi.nlm.nih.gov` **failed**: those hosts
are outside this session's network allow-list. No source above was read in full text, so every
measured value is at search-summary level.

### Model constants (recalled from Pennycuick's flight model, not re-read: could-not-access)

- Induced factor k = 1.1–1.3.
- Body frontal area S_b = 0.00813·m^0.666 m².
- Body drag coefficient C_Db = 0.1–0.4.
- Profile power = X1 × absolute-minimum power, with X1 = 0.8–1.6.
- ρ = 1.225 kg/m³, g = 9.81 m/s².

### Assumed design inputs

- Mass m = 0.05, 0.1, 0.3 kg.
- Span b = 0.2, 0.3, 0.45 m.
- Flight-muscle fraction f = 0.05–0.25. Teleost pectoral-muscle fraction is `unknown` to me; I
  did not search for it. Birds sit around 0.15–0.25, which is my recollection and not sourced here.

## 3. Arithmetic (CALCULATED, not observed)

Script: `docs/research/fish/replicate-203_calc.py`.

P(V) = k·W²/(2ρ·S_d·V) + ½ρ·V³·S_b·C_Db, with S_d = πb²/4. This is minimised over V; then
P_min = P_am·(1 + X1).

Central case (m = 0.1 kg, b = 0.3 m, k = 1.2, C_Db = 0.1, X1 = 1.2):

- P_min = 1.63 W, which is **16.3 W/kg body**, at V_mp = 12 m/s.
- This matches the pigeon slow-flight figure of 16.1 W/kg body, which is an independent sanity
  check.
- Full 243-point grid: 4.3 – 21.6 (median) – 110.6 W/kg body. The top of the range is the
  0.3 kg / 0.2 m-span corner, which is unrealistic.

Required power per kg of flight muscle, central case:

| f | Required (W/kg muscle) | Grid range |
|---|---|---|
| 0.05 | 326 | 86 – 2212 |
| 0.10 | 163 | 43 – 1106 |
| 0.17 | 96 | 25 – 651 |
| 0.25 | 65 | 17 – 442 |

Available sustained power (central case, f = 0.17 → 96 W/kg needed):

- Ectothermic red muscle at 10–28 W/kg gives 1.7–4.8 W/kg body against 16.3 needed: a shortfall
  of **3.4–9.6×**.
- Even f = 0.25 with the best ectotherm value (27.9) gives 7.0 W/kg body: a **2.3× shortfall**.
- Skipjack red muscle (79–133 W/kg) × 0.17 gives 13–23 W/kg body, which **reaches or exceeds**
  16.3. So the conclusion depends on which muscle is taken as "fish aerobic muscle".

**My blind result:**

- Sustained level flapping at the minimum-power speed needs about **16 W/kg body**. The grid range
  is 4–110 and the plausible core is about 10–30.
- That is **≈ 65–165 W/kg flight muscle** at f = 0.25–0.10.
- Ectotherm fish red muscle (10–28 W/kg, search-summary) falls short by about 2–10×.
- Warm tuna red muscle (79–133 W/kg) does not fall short.
- So "not supported" holds for ordinary fish red muscle at flying-fish scale, but not universally.

## 4. Scale check after reading (NOT independent)

The claim, as quoted in `challenge-203.md`, concerns a **0.4 g** flier and a **hover** requirement.
That is a far smaller and different case from my blind framing. I re-ran my **unchanged** model
using only the mass and span taken from that framing. The hover formula is the standard momentum
form, which I wrote down independently:

| Case (0.4 g) | Body (W/kg) | Muscle at f = 0.3 (W/kg) |
|---|---|---|
| Forward flight, b = 8 cm, C_Db = 0.1–0.4 | 3.0–4.2 | **10–14** |
| Forward flight, b = 4 cm | 8.4–11.9 | 28–40 |
| Hover, R = 4 cm, k = 1.2, profile +50% | 6.6 (induced) | **33** |
| Hover, R = 2 cm | 13.3 (induced) | **66** |

The hover number reproduces the recorded ~34 W/kg. That is an arithmetic identity, given the same
formula and inputs, so it is **not independent evidence**.

## 5. Comparison with the recorded value

Recorded claim (quoted in `challenge-203.md`, which says it read `S10-tissue.md` in full):
"measured fish aerobic (red/slow) muscle gives 5–10 W/kg, below the computed hover requirement of
at least ~34 W/kg flight muscle even in the most generous case."

**DISAGREE** with the claim as worded, for two reasons.

1. **The sustained-power input.** My independent search found red-muscle maxima **above** the
   claim's 5–10 W/kg band:
   - scup 27.9 W/kg at 20 °C (Rome & Swank 1992);
   - small cod 27.5 W/kg;
   - skipjack 79–133 W/kg.

   These are all search-summary reads. The claim's band and mine disagree, and I am not averaging
   them. My inference, not data: at the zebrafish's ~28 °C, a scup-like red muscle at ≥ 28 W/kg
   would cover the 0.4 g forward-flight requirement (10–14 W/kg muscle at f = 0.3, calculated). It
   would also come within reach of the ideal-floor hover figure (~19 W/kg at f = 0.3 reported in
   the challenge; I did not recompute that floor). That means "not supported even in the most
   generous case" is not established.
2. **The flight mode.** "Sustained flapping" is wider than hover. Forward flight at the
   minimum-power speed is 2–3× cheaper (§4, calculated).

What would restore the claim:

- Red muscle loses power well above its 2–5 Hz optimum, and the wingbeat of a 0.4 g flier is much
  higher. The Rome & Swank summary itself notes that peak power sits below the frequencies scup use.
  Red-muscle power at ~20 Hz is `unknown`; I did not find a measurement.
- My blind framing (flying-fish scale) does support "not supported" for ectotherm red muscle, by
  2–10×.

So the direction agrees, but the claim's stated input band and its "even in the most generous case"
do not survive my sources.

Scope of negative searches:

- Three web searches (scup/Rome; pigeon pectoralis; fish red-muscle work loops). Two fetch attempts
  were blocked by the network allow-list.
- I did not search for teleost pectoral-muscle mass fraction, red-muscle power at ≥ 20 Hz, or any
  measured power of a flapping fish.

```swarm-replication
{"claim_id": 203, "my_value": "blind (0.05-0.3 kg flier, forward flight at V_mp): ~16 W/kg body (grid 4-110) = ~65-165 W/kg flight muscle at f=0.25-0.10; scale-matched post-read check at 0.4 g: hover ~33 W/kg muscle, forward flight ~10-14 W/kg muscle (f=0.3); available ectotherm red muscle 10-28 W/kg (search-summary)",
  "agrees": false,
  "note": "Direction agrees for ordinary red muscle at flying-fish scale, but my sources put fish red-muscle maxima up to ~28 W/kg (scup, 20 C) rather than 5-10, which with forward flight (10-14 W/kg muscle at 0.4 g, calculated) breaks 'not supported even in the most generous case'; red-muscle power at ~20 Hz wingbeat is unknown and could restore the claim."}
```
