# Challenge 169: adversarial review of [S20-D-D], the guppy-class exit-speed comparator

**Outcome: WEAKENED.** The conclusion stands: no route I can build from the stated inputs reaches the
3.13 m/s that a 1 m launch requires. The central number (1.37 m/s) reproduces. Three secondary
numbers do not: the route band "1.02–1.37 m/s", the "3.7x" ceiling, and the "11 cm" lower hop. Each
one comes from mixing an unscaled 18.5 mm guppy value into a band that is supposed to be scaled to a
33 mm fish.

The S20-D source document is not in this repository. I searched the whole checkout for
"guppy" and "S20-D" in `*.md` files and found nothing. I therefore judge the claim only against its
stated inputs and the two primary papers.

## Sources and read-levels

| Source | Read-level | What I took from it |
|---|---|---|
| Soares & Bierman 2013, *PLoS ONE* 8:e61617 (PMC3629028) | full-text (via a fetch tool's extraction, so verbatim quotes were relayed rather than read line by line) | SL 1.85 ± 0.35 cm. Maximum velocity in water 102.36 ± 33.75 cm/s, peaking "right before or at the moment the fishes' head broke the water/air interface"; highest single value 128 cm/s. Maximum velocity in air 123.57 ± 30.0 cm/s, at about ¾–1 BL out; highest single value 150 cm/s. Jump height 6.54 ± 1.92 cm (3.52 ± 0.96 BL); highest jump 8.2 cm. Aerial phase: n = 20 jumps by 5 males. The Discussion gives 100.16 ± 33.9 cm/s for the water speed, which conflicts with Table 1. I record the conflict and do not resolve it. |
| Chang et al. 2019, *J R Soc Interface* 16:20190014 (PMC6451394) | full-text (same caveat) | H/L ~ L^-1/3, equivalent to U ~ L^1/3. It assumes P ∝ M, Cd = 0.05, isometry, neutral buoyancy, and complete exits. The interspecific fit slope is −0.35 ± 0.12 with r² = 0.57. The paper has no zebrafish or *Danio* data. |

## 1. Independent arithmetic

I computed each value from the stated inputs. All of them are **calculated, not observed**.

- Size factor: (33 / 18.5)^(1/3) = **1.213**.
- Required speed: √(g · 1 m) = **3.13 m/s**. That is the drag-free speed for a 1 m *range* at a 45°
  launch. A 1 m *height* would need √(2g · 1 m) = 4.43 m/s. The claim's 3.13 therefore implies that S20
  priced horizontal range. I cannot check that against S20 itself. Either way, 3.13 is the most
  favourable reading for the fish, so it does not weaken the conclusion.
- S20-D's original value: √(2g · 3.5 × 0.033 m) = 1.51 m/s. **This reproduces**, and so does the claim's
  account of how S20-D got it.

| Route (guppy value → ×1.213) | Scaled speed | Speed shortfall vs 3.13 m/s | 45° range |
|---|---|---|---|
| Mean water-exit speed, 1.024 m/s | 1.24 m/s | 2.5x | 15.7 cm |
| Mean air speed, 1.236 m/s | 1.50 m/s | 2.1x | 22.9 cm |
| Mean of water and air speeds, 1.130 m/s | **1.37 m/s** | 2.3x | 19.1 cm |
| Speed implied by mean height, √(2g · 0.0654) = 1.133 m/s | **1.37 m/s** | 2.3x | 19.2 cm |
| Speed implied by highest jump, √(2g · 0.082) = 1.27 m/s | 1.54 m/s | 2.0x | 24.1 cm |
| Fastest single air speed, 1.50 m/s | **1.82 m/s** | 1.7x | 33.7 cm |

What reproduces:

- **1.37 m/s** comes out by two independent routes. One is the arithmetic mean of the water and air
  speeds. The other, which I think is the more defensible, is the ballistic speed implied by the
  measured mean jump height. Two different routes agree on the central value.
- **1.82 m/s** reproduces from the fastest single air speed.
- The **1.7x** floor reproduces as 3.13 / 1.82.

What does not reproduce:

- **Band "1.02–1.37 m/s".** The lower end, 1.02 m/s, is the guppy's *unscaled* water-exit speed. On the
  claim's own L^1/3 rule, water exit scaled to 33 mm is 1.24 m/s. The scaled routes span
  **1.24–1.50 m/s**. The upper end of that span is the scaled air speed, and it is essentially S20-D's
  original 1.51 m/s.
- **"3.7x".** 3.13 / 3.7 = 0.85 m/s. No stated input yields 0.85 m/s. The nearest arithmetic match is
  1.024 / 1.213 = 0.84, which divides by the size factor instead of multiplying. That match is my
  inference about where the number came from; I have not confirmed it. Even the unscaled water speed
  gives only 3.06x. The shortfall supported by the stated inputs is **1.7x–2.5x**, or 1.7x–3.1x if the
  unscaled 18.5 mm value is allowed.
- **Hop "11–19 cm".** 11 cm is the 45° range at the unscaled 1.02 m/s. The scaled band gives
  **16–23 cm** (mean routes), and the fastest single jump gives about 34 cm.

## 2. Proxy check

The quantity that matters is the effective ballistic launch speed of the centre of mass once the fish
is clear of the water. Each measured speed is a proxy for it, and each is biased in a different way:

- The in-water peak is measured before the fish stops adding thrust, so it understates launch speed.
- The in-air peak is measured at ¾–1 BL out, while the tail is still beating, so it may overstate the
  speed at which the fish leaves the water. The highest jump (8.2 cm) implies only 1.27 m/s. That is
  below the 1.50 m/s single-jump air peak. I infer from this that peak air speeds overstate ballistic
  performance. Part of the gap could instead be digitising-point or pairing effects, because the paper
  does not say which point velocity was computed from.

The height-implied speed is the best proxy available here, and it gives 1.37 m/s. The claim's
headline value is therefore sound in value even though its stated provenance (the water and air
speeds) is not the best one. By this proxy the "extreme" comparator is about 1.54 m/s, not 1.82 m/s.
That makes the 1.7x floor conservative, not wrong.

A caveat on height: the paper does not say whether height is measured from the head or the centre of
mass. Head height would overstate centre-of-mass rise and inflate the implied speed. That would also
push in the conservative direction.

## 3. Hidden assumptions, tested relaxed

- **Exponent.** Chang's fitted slope of −0.35 ± 0.12 gives U ~ L^0.265 to L^0.385, so the size factor
  is 1.17 to 1.25. At the most generous end with the fastest single jump: 1.50 × 1.25 = 1.87 m/s, a 1.67x
  shortfall. The conclusion survives.
- **Interspecific transfer.** The scaling is a cross-taxon fit with r² = 0.57 and no *Danio* point.
  Guppy-like jumping in *Danio* is assumed, not shown. Matching 3.13 m/s would need a 33 mm fish to
  beat the guppy-scaled mean by 2.3x and the most extreme guppy-scaled jump by 1.7x. Nothing in either
  paper suggests scatter that large around the line. This is my inference, not a tested bound.
- **Length convention.** The guppy length is SL. I do not know whether the 33 mm zebrafish length is SL
  or TL. If it is TL, with SL of roughly 27 mm (my assumed ratio, not sourced), the size factor drops to
  about 1.13 and every comparator falls about 7%. That moves in the conservative direction.
- **Regime.** H/L ~ Fr² is stated for complete exits, and guppies do exit fully (3.5 BL). The regime
  is consistent.

## 4. Evidence level

The claim is recorded as "derived" and labels 1.37 m/s "calculated". That is honest. The table inputs
are correctly attributed as measured guppy values. One labelling defect: the 1.02 m/s lower bound of a
band headed "scaled to a 33 mm fish" is an unscaled measurement, so the band is mislabelled.

## 5. Counter-examples and regimes missed

Scope of search: the two cited papers only, plus a check of this repository. I did not run a
literature search for zebrafish or *Danio* jumping kinematics, so whether such data exist is
**unknown**. Chang et al. contain no *Danio* data. I found no counter-example. That is not evidence
that none exists.

## Verdict

**Weakened, not refuted.**

- The 1.37 m/s central comparator reproduces, and is best justified by the measured jump height.
- The verdict "stands" also holds: the best case is 1.82–1.87 m/s against 3.13 m/s.
- The secondary numbers are wrong and should be replaced:
  - the scaled band is **1.24–1.50 m/s**, not 1.02–1.37 m/s;
  - the shortfall is **1.7x–2.5x**, not 1.7x–3.7x, because 3.7x is not reproducible;
  - the reachable hop is **16–23 cm** at 45° range (up to about 34 cm for the fastest single jump), not
    11–19 cm.
- The scaled air-speed route returns essentially S20-D's own 1.51 m/s. The "replacement" therefore
  changes the central value by about 9%, not by a regime.

```swarm-challenge
{"claim_id": 169, "outcome": "weakened", "reason": "The 1.37 m/s central value and the 'stands' verdict reproduce, but the band's 1.02 m/s lower end, the 11 cm hop and the 3.7x ceiling come from unscaled or unreproducible values; scaled to 33 mm the band is 1.24-1.50 m/s and the shortfall 1.7x-2.5x.", "corrected_value": "1.37 m/s central (scaled band 1.24-1.50 m/s; extreme 1.82 m/s; shortfall vs 3.13 m/s = 1.7x-2.5x; 45-degree hop 16-23 cm)", "depends_on": ["Soares & Bierman 2013 Table 1: SL 18.5 mm, water-exit 102.36 cm/s, air 123.57 cm/s, max air 150 cm/s, height 6.54 cm", "Chang et al. 2019 H/L ~ L^-1/3 (U ~ L^1/3; fit slope -0.35 +/- 0.12)", "zebrafish length 33 mm (SL vs TL unknown)", "1 m launch interpreted as 1 m range at 45 deg, drag-free (3.13 m/s)"]}
```
