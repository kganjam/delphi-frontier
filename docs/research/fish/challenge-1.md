# Challenge 1: "Stall speed for a 1-body-length span wing (AR 5, C_L 0.6) on a 0.4 g zebrafish is 5.84 m/s"

**Claim under attack.** It comes from `docs/research/fish/zebrafish-glide-physics.md` (§3 table, §4, §5)
and `zebrafish_glide_calc.py`, on branch `origin/claude/zebrafish-glide-physics-j176og`, commit
`e1a844e5`. The recorded evidence level is *derived* and the value is 5.84 m/s.

**Reviewer's status.** I ran no experiment. Every number below is labelled as one of: **calculated
by me**, **measured by others and relayed to me** (with a read-level), or **my inference**.

**Verdict: weakened.** The arithmetic is exact and the label *derived* is honest. What does not hold
is the word **"stall"**. A stall speed is defined at C_L,max. In this claim C_L = 0.6 is the author's
*design* value, not a known C_L,max. So the 5.84 m/s is a *design-point speed* standing in for a
stall speed. The measurements relayed for thin finite wings in the same Re band put C_L,max at
about 0.93–1.15. At those values the stall speed would be about 4.2–4.7 m/s (calculated). The
parent report's conclusion that launch speed is the hardest barrier is not affected.

---

## 1. Arithmetic, redone independently. It survives.

Inputs as given in the parent report: m = 0.4 g, span b = 1 BL = 0.04 m, AR = 5, C_L = 0.6,
ρ = 1.2 kg/m³, g = 9.81 m/s².

Calculated (mine):
- W = 4.0e-4 × 9.81 = 3.924e-3 N
- S = b²/AR = 0.0016 / 5 = 3.2e-4 m² = 3.2 cm²
- ρ·S·C_L = 1.2 × 3.2e-4 × 0.6 = 2.304e-4
- V = √(2W / (ρ S C_L)) = √(7.848e-3 / 2.304e-4) = √34.06 = **5.836 m/s**

That rounds to 5.84 m/s and **agrees with the author**. Self-consistency check (calculated): the
chord is c = b/AR = 8 mm, so Re = 5.836 × 0.008 / 1.5e-5 = 3,113. That is the same design Re the
author reports in §1, so the speed and the Re regime agree.

## 2. Proxy: a design C_L standing in for C_L,max

A stall speed is V_s = √(2W/(ρ S C_L,max)). The author's own text says C_L = 0.6 is "the central
design value", and that "the steady C_L,max at Re ≈ 3e3 for a fish-fin-like membrane is
**unknown**" (§1). In §4 the author writes that the power optimum "lands at the C_L cap, i.e. at
stall speed". That sentence treats the cap as C_L,max. The claim inherits that step.

The quantity that matters is the steady C_L,max of a thin, finite, membrane wing at Re ≈ 3e3. The
nearest values I could find are these. Disagreements are kept as they appear.

| Source | Re | Kind | C_L | Read-level |
|---|---|---|---|---|
| Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543–556, *Sympetrum sanguineum*, free glides | citing sources disagree: "700–2,400" or "2,400" | **observed** in glides | highest recorded **0.93**. The source says this is not necessarily the wings' maximum. | search-summary |
| Same paper, wind tunnel, real wings | same | **measured**, steady | C_L,max **1.07** (*S. sanguineum*), **1.15** (*Calopteryx splendens*) | search-summary |
| Laitone 1997 (the author's basis for 0.6) | ≈ 2.07e4 | measured | 0.455 → 0.59 | search-summary (author). `challenge-5.md` infers this is probably the NACA 0012 section, and I have not checked that inference independently. |

Stall speed for the same 1-BL, AR 5 wing (calculated by me; V ∝ C_L^-½):

| C_L,max assumed | V_s | ÷ Ucrit 0.548 m/s | KE ratio |
|---|---|---|---|
| 0.6 (author) | 5.84 m/s | 10.6× | 113× |
| 0.93 | 4.69 m/s | 8.6× | 73× |
| 1.07 | 4.37 m/s | 8.0× | 64× |
| 1.15 | 4.22 m/s | 7.7× | 59× |

(The author's "10.4×" divides by 0.56 m/s, not 0.548. Both denominators appear in their report. This
does not matter here.)

**Inference (mine):** dragonfly wings are corrugated, rigid-veined and of a different planform from
a ray-supported fin membrane. Their C_L,max is a neighbouring value, not the fin's value. The
fin-membrane C_L,max is still **unknown**. Even so, every steady thin-wing value I found in this Re
band is above 0.6. So 5.84 m/s is better described as an **upper-end** stall speed, conditional on
C_L,max = 0.6, than as *the* stall speed.

## 3. Other hidden assumptions, each relaxed (all calculated by me)

| Assumption | Relaxed to | V_s at C_L 0.6 | Direction |
|---|---|---|---|
| ρ = 1.2 kg/m³ | 1.172 kg/m³ (dry air at 28 °C, zebrafish husbandry temperature, sea-level pressure) | 5.91 m/s | +1 % |
| W excludes the wing | membrane adds 10 / 25 / 50 % to body mass (mass **unknown**) | 6.12 / 6.53 / 7.15 m/s | up |
| L = W (level flight) | glide at L/D 3 or 5, so L = W cos γ | 5.69 / 5.78 m/s | −3 % / −1 % |
| Body carries no lift | the body contributes lift | not computed: body planform lift coefficient is **unknown** | down |
| Free air | flight in ground effect over water | not computed: the magnitude for this geometry is **unknown** | probably down (inference) |

None of these moves the number as far as the C_L,max question does. The mass correction pushes the
other way and partly offsets it. Neither the author nor I have a value for it.

## 4. Is the evidence level honest?

Yes, for the number. 5.84 m/s is presented as calculated ("calc") throughout the parent report, and
it never appears as a measurement. *Derived* is correct. The defect is in the name, not the level:
"stall speed" implies an aerodynamic limit, but what was computed is the speed at an assumed design
coefficient. A precise statement would be: *"Speed at which a 1-BL, AR 5 wing carries 0.4 g at
C_L 0.6: 5.84 m/s (derived). This equals the stall speed only if C_L,max = 0.6, which is unknown at
Re ≈ 3e3."*

## 5. Regimes or counter-examples the author missed

- Thin finite insect wings at Re 7e2–2.4e3 measured C_L,max of 1.07–1.15, relayed at search-summary
  level (§2). This is the main counter-example. It has already been raised against the C_L ceiling
  in `challenge-5.md` (claim 5). Here it applies to the derived stall speed.
- Unsteady or high-α effects such as delayed stall or a leading-edge vortex during a launch
  manoeuvre would raise transient C_L above the steady value. That would lower the instantaneous
  speed needed, but not the steady glide speed. Per the search summary, Wakeling & Ellington's
  companion paper (Dragonfly Flight III) reports mean lift coefficients in flapping flight above
  the steady C_L,max. I did not retrieve that number.
- Negative search scope: I ran one web search, on Wakeling & Ellington 1997. I made no fetch
  attempts, and I relied on `challenge-5.md` for the other sources. I found no measured C_L,max for
  a fish-fin membrane in air. That search is not exhaustive.

## 6. Effect on the parent verdict

None on the ranking. Even at C_L,max = 1.15, the 1-BL wing needs 4.2 m/s, which is 7.7× the measured
Ucrit and 59× its kinetic energy (calculated). The launch-speed barrier remains the hardest barrier.

## Sources

| Source | Read-level | Used for |
|---|---|---|
| `zebrafish-glide-physics.md` and `zebrafish_glide_calc.py` (commit `e1a844e5`) | full-text | claim, inputs, the author's wording on C_L |
| `challenge-5.md` (commit `58ea94ca`) | full-text (repository document; its own sources are search-summary or secondary) | Laitone section inference; context |
| Wakeling, J.M. & Ellington, C.P. (1997) Dragonfly flight I. *J. Exp. Biol.* 200:543–556 | search-summary (citing pages and index listings; e.g. https://scilit.com/publications/e3a0ca31c95f0233cc7f26f0f2b55853, https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/3806905) | C_L 0.93 (glides), C_L,max 1.07 / 1.15 (tunnel) |
| Wakeling & Ellington (1997) Dragonfly flight III | search-summary (https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/3806925) | qualitative: unsteady mean C_L above steady C_L,max |

```swarm-challenge
{"claim_id": 1, "outcome": "weakened", "reason": "The arithmetic is exact (5.836 m/s) and 'derived' is honest, but C_L = 0.6 is an assumed design value, not a known C_L,max, so the figure is a design-point speed labelled as a stall speed; relayed steady C_L,max of 0.93–1.15 for thin finite wings at Re ~1e3 gives a stall speed of about 4.2–4.7 m/s, which leaves the launch-barrier verdict intact.", "corrected_value": "5.84 m/s at C_L = 0.6 (derived); stall speed ≈ 4.2–4.7 m/s if C_L,max = 0.93–1.15 (derived from relayed search-summary values); fin-membrane C_L,max unknown"}
```
