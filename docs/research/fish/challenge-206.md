# Challenge 206: adversarial review of claim S20 (energy cost and benefit of zebrafish "flight")

**Claim under review (author's words):** "Flight would be energetically almost free for a zebrafish (derived: ~2e-3 to 2e-2 J per 0.1-1 m launch, about 1e-4 to 1e-3 of daily standard metabolism), but no published evidence shows any predation benefit, wild predation rates are unmeasured, and the named predator field includes birds that strike from above, so the benefit that would make flight pay is unknown and probably absent."
Recorded evidence level: `unknown`. Source: `harvest:zebrafish-flight-ecology-z4f08c`.

**Verdict: WEAKENED.** The energy numbers come out the same when I redo them, within a factor of about 3. But launch energy as a share of daily SMR is the wrong measure of what flight costs. And "probably absent" claims more than the evidence supports.

## 0. Provenance check
- I could not find the source harvest `zebrafish-flight-ecology-z4f08c` in this repository: a recursive search of the working tree for "zebrafish" and "z4f08c" found nothing (read-level: could-not-access). So I could not see the author's inputs. I rebuilt them from what the claim says. Everything below is my own calculation unless it says otherwise.

## 1. Arithmetic, redone independently (all values below are **computed**, not observed)

Inputs I assumed:
- Adult mass 0.3-0.5 g. This is an assumption; I did not take it from a source.
- g = 9.81 m s^-2.
- Muscle-to-mechanical efficiency 0.2. I also tested an overall efficiency of 0.05, to cover propulsive loss in water. Both are assumptions.
- 13.6 J per mg O2. This is the standard oxycalorific coefficient.

| Quantity | 0.1 m | 1 m |
|---|---|---|
| Potential energy m·g·h, 0.3-0.5 g (vertical launch) | 2.9e-4 - 4.9e-4 J | 2.9e-3 - 4.9e-3 J |
| Kinetic energy at a 45° launch for horizontal range d (= ½·m·g·d) | 1.5e-4 - 2.5e-4 J | 1.5e-3 - 2.5e-3 J |
| Metabolic energy, η = 0.2 | 1.5e-3 - 2.5e-3 J | 1.5e-2 - 2.5e-2 J |
| Metabolic energy, η = 0.05 | 5.9e-3 - 9.8e-3 J | 5.9e-2 - 9.8e-2 J |

The author's 2e-3 to 2e-2 J is exactly m·g·h / 0.2 for a 0.4 g fish, so it matches my η = 0.2 row. If the author meant horizontal *range* rather than *height*, their figure is high by a factor of 2. It does not account for propulsive losses in water. With those losses it could be up to about 4× low.

Daily SMR:
- Inputs:
  - Lucas & Priede (1992, J Fish Biol), 364 mg O2 kg^-1 h^-1 at 24 °C for fish of 0.43-0.55 g (read-level: search-summary).
  - An allometric equation from doi 10.1111/jfb.12306: R_S = 0.273·M^0.965 at 28 °C (read-level: search-summary). I read it as whole-animal mg O2 h^-1 with M in g. That gives about 280 mg O2 kg^-1 h^-1 at 0.4 g. The unit reading is my inference.
- **Computed:** daily SMR is 27-59 J/day for a 0.3-0.5 g fish.
- **Computed:** a launch costs about 3e-5 to 7e-4 of daily SMR at η = 0.2, and up to about 4e-3 at η = 0.05.
- The author's 1e-4 to 1.3e-3 implies a daily SMR of roughly 15-20 J, which is lower than both sources above. Their ratio errs high, which is the conservative direction for a claim that the cost is small.
- The two KEY ranges in the claim (1e-4 to 1e-3 and 1e-4 to 1.3e-3) also disagree with each other. This is minor.

**Arithmetic outcome:** the conclusion holds that one launch costs far less than 1% of daily SMR. It is robust to a 4× change in efficiency and a 2× change in SMR.

## 2. The proxy problem (main defect)
The claim uses energy per launch as a share of daily SMR to stand for the cost of flight. That is a proxy, and it does not measure what limits flight:

1. **Takeoff speed and power, not energy, decide whether a zebrafish can do this at all.** Computed speeds needed at the water surface, ignoring drag in air:
   - 1.40 m/s to rise 0.1 m and 4.43 m/s to rise 1 m.
   - 0.99 m/s for a 0.1 m range at 45° and 3.13 m/s for a 1 m range.

   I found no published peak escape speed for *adult* zebrafish. Two web searches returned only larval data and a statement that adults approach prey "much slower than their maximum speed", so the value is `unknown`. The 1 m case needs about 90-130 body lengths per second for a 3.5 cm fish. That is my inference and I have not checked it against measurements. It may well be beyond what an unmodified zebrafish can do, which would make "almost free" an energy cost for something it cannot perform.

2. **The costs of true flight (gliding) are mostly structural, and the claim leaves them out.** Gliding fish (Exocoetidae) have greatly enlarged pectoral fins. Their costs are the drag of carrying those fins all the time, the cost of growing them, and possible trade-offs in swimming. A zebrafish does not have this morphology. Without it, a "0.1-1 m launch" is a ballistic leap, not flight.

3. **Risks after the leap are missing:**
   - stranding or landing on the bank;
   - exposure to birds striking from above, which the author mentions only on the benefit side;
   - recovery from anaerobic effort.

   None of these show up in a calculation of launch energy alone.

A better quantity would be the expected change in fitness per escape. That is P(predation | stay) minus P(predation | leap), weighed against stranding risk and the lifetime cost of whatever morphology makes the leap possible. Every term in it is `unknown` for wild zebrafish.

## 3. Hidden assumption, tested relaxed
The claim assumes the fish can physically reach the launch. If that is relaxed, so the fish must first reach 1.4-4.4 m/s, the 1 m case may be infeasible rather than cheap. The 0.1 m case (about 1-1.4 m/s) seems more likely to be within reach. That is my inference; there is no measured adult value. So "almost free" should apply only to the 0.1 m end, and only on the condition that the fish can reach the needed speed.

## 4. Evidence level
- The author labels the energy figure "derived" and "computed", which is honest.
- The recorded level of `unknown` fits the benefit side.
- **Overreach:** "probably absent" is inferred from an absence of evidence, and the author also says wild predation rates are unmeasured. On that evidence, the honest statement is "unknown".
- The bird argument cuts both ways (see §5). It is an inference, not evidence that there is no benefit.

## 5. Counter-examples and regimes the author did not consider
- **Flying fishes (Exocoetidae):** escaping predators is the standard explanation for why these fish glide. It is discussed in Davenport (1994), "How and why do flying fish fly?", Rev. Fish Biol. Fish. I cite this from memory; read-level: could-not-access in this session. So aerial escape *can* pay off in fish even where birds attack from above, which weakens the author's bird-based reasoning. That is my inference.
- **Freshwater hatchetfishes (Gasteropelecidae):** small freshwater fishes whose leaps out of the water are widely described as escape behaviour. I have not verified this against a primary source in this session (read-level: none, general knowledge). I am not stating that they have a measured predation benefit.
- **Scope of my negative search:** two standard web searches for adult zebrafish escape speed, one for zebrafish SMR, and a recursive search of this repository. I ran no literature-database search for zebrafish aerial or jumping escape. The author's "no published evidence" is neither confirmed nor refuted by my work.

## Sources
- Lucas & Priede 1992, zebrafish SMR at 24 °C. Read-level: search-summary.
- Zebrafish allometric respirometry at 28 °C, doi 10.1111/jfb.12306 (archimer.ifremer.fr/doc/00180/29113/88195.pdf). Read-level: search-summary.
- Searches for adult zebrafish fast-start speed (e.g. PMC3044078, arxiv 2301.02661, Gazzola et al. 2012 JFM). Read-level: search-summary. None gave an adult peak speed.
- Davenport 1994. Read-level: could-not-access (cited from memory).

```swarm-challenge
{"claim_id": 206, "outcome": "weakened", "reason": "The energy arithmetic holds (computed 1.5e-3 to 1e-1 J metabolic, about 3e-5 to 4e-3 of daily SMR), but energy as a share of daily SMR is a proxy that skips the binding constraints (a takeoff speed of 1.0-4.4 m/s against an unknown adult burst speed, the structural cost of wing-like fins, and stranding risk), and 'probably absent' overreaches when predation rates are admittedly unmeasured and flying fishes are a counter-example.",
  "corrected_value": "launch metabolic cost ~1.5e-3 to 2.5e-2 J (eta 0.2; up to ~0.1 J at eta 0.05) = ~3e-5 to 4e-3 of daily SMR (27-59 J/day, computed); required exit speed 1.0-4.4 m/s (computed); feasibility and predation benefit: unknown",
  "depends_on": ["adult zebrafish mass 0.3-0.5 g (assumed)", "muscle efficiency 0.2 / overall 0.05 (assumed)", "SMR 280-364 mg O2 kg-1 h-1 (Lucas & Priede 1992; doi 10.1111/jfb.12306; search-summary)", "oxycalorific 13.6 J/mg O2", "adult zebrafish peak escape speed (unknown)", "flying-fish predator-escape hypothesis (Davenport 1994; could-not-access)"]}
```
