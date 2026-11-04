# Challenge 231: is "the barrier is a property of single-impulse launch from water at this size" justified?

**Claim under review (S29, `docs/research/fish/S29-organism.md` §0 "deeper conclusion" and §6, on branch `claude/s29-launch-energy-2iuixr`, commit 44ed2195):**
> "THE DEEP CONCLUSION: the barrier is a property of SINGLE-IMPULSE LAUNCH FROM WATER AT THIS SIZE, not of any one mechanism. Two independent representations -- wing enlargement and spring-loaded launch -- fail on different terms, which makes the limit a property of the problem rather than of our framing."

**Recorded evidence level:** derived. **Value:** n/a.

**Verdict: WEAKENED.** The arithmetic holds when I redo it. The generalisation does not follow from it, for three reasons:
1. The two "representations" are not independent.
2. By S29's own account they fail on the same term, not on different terms.
3. The binding term comes from an unstated design assumption: the spring is loaded by one muscle contraction. That is not the same as a single-impulse launch. Relax the assumption and the energy term closes on S29's own numbers.

Everything below is my own calculation or reading. Nothing here is a new measurement.

Sources and read levels:
- `S29-organism.md` and `S29_launch_energy.py`: **full-text** (git, commit 44ed2195).
- `S28-organism.md`: **full-text**, grep-level sections only (branch `claude/s28-organism-design-5z0vjz`).
- Literature: listed in §5 with read levels.

---

## 1. Independent re-derivation of the arithmetic

My script uses only S29's stated inputs: m = 0.40 g, V = 4.37 m/s, Cd 0.2, A = 24 mm², stroke 1.09 cm, η_h = 0.37, η_spring = 0.93, one side = 30 % of body mass, w = 32/53/81 J/kg muscle.

| Quantity | S29 states | I get (calculated) |
|---|---|---|
| KE per kg body | 9.55 J/kg | 9.548 J/kg |
| Drag work during stroke | 0.250 mJ (6.5 %) | 0.624 J/kg = 0.250 mJ |
| Need at body | 10.17 J/kg | 10.173 J/kg |
| Stored per kg body | 29.56 J/kg | 29.56 J/kg |
| One-side supply at 53 J/kg | 5.47 J/kg | 5.471 J/kg |
| Shortfall at 32 / 53 / 81 J/kg | 3.08 / 1.86 / 1.22× | 3.080 / 1.859 / 1.217× |
| Mass-consistent 5.53 m/s target | ~3.0× | 3.02× (stroke time held at 5 ms) |
| Spring volume, 100 MPa tendon / tuna tendon at 2 % strain | 1.02 % / 12.9 % | 1.02 % / 12.9 % |

**The arithmetic survives.** I found no numerical error.

## 2. Proxy check: is the right quantity being compared?

The quantity that matters is **the energy delivered to the body at water exit, compared with ½V_to²**.

S29's binding term is "energy per stroke × η_h", where the stroke is the *loading* contraction. That is a proxy, and it only stands in for the real limit if the spring must be filled in one contraction. The real limit on a latched spring is:
- the energy the spring can hold (S29's own §2.4 shows this passes, at 1–24 % of body volume), and
- the total muscle work available before release.

A latch holds energy indefinitely. Muscle work per contraction caps the stored energy only if a single contraction loads the spring.

A second, smaller proxy issue: η_h = 0.37 is a pike C-start Froude-type efficiency (S29 cites it at ABSTRACT level). In actuator-disc terms, Froude efficiency falls as thrust loading rises. A 5 ms, 89 g impulsive stroke is more heavily loaded than a pike C-start, so the true η_h is plausibly *lower*. This is my inference and I have not quantified it. It cuts in S29's favour: it widens the gap and does not break the claim.

## 3. Hidden assumptions, each tested relaxed

### 3a. Single-contraction loading
The claim says "single-impulse launch". The calculation actually assumes a **single loading contraction**, and those are different things. A ratchet or catch latch lets the release stay single while the load builds over several contractions, the way a crossbow is spanned.

Calculated on S29's numbers, the loading contractions needed for one-side axial muscle are:

| w (J/kg muscle) | Contractions at 4.37 m/s | Contractions at 5.53 m/s |
|---|---|---|
| 53 | **2** (supply 10.94 vs need 10.17 J/kg) | 4 |
| 81 | 2 | — |
| 32 | 4 | — |

The spring that has to hold this energy is the same one S29 already sized at 1.0 % (mammal tendon) to 12.9 % (tuna-tendon strain) of body volume. So the energy term closes once multi-contraction loading is allowed.

What I have **not** shown:
- that any animal loads a locomotor spring by ratcheting several contractions. I did not search for a biological precedent; the scope of this negative is "not searched", and **whether one exists is unknown**;
- that a fish could hold the latch while contracting repeatedly.

This turns S29's limit into "single-contraction loading plus no latch". It does not show the organism is feasible, and it removes neither the latch problem nor the "invention, not modification" verdict. It does show that the barrier is not a property of **single-impulse launch** as such. It is a property of single-contraction loading, which is a feature of the mechanism the claim says it has transcended.

### 3b. Push-off medium
η_h is the term S29 says "belongs to the medium". The calculation assumes the launch reacts only against water. A small fish launching close to a rigid surface (substrate, vegetation, the tank floor in shallow water) is in a different regime.

Calculated: with η_h → 1, one-side supply at 53 J/kg is 14.79 J/kg against the 9.55 J/kg KE floor, a **1.55× surplus**. The claim's scope phrase "from water" arguably excludes this case. If it does, the conclusion partly restates its own premise (water push-off implies η_h < 1) rather than discovering it.

### 3c. The representations are taken one at a time
S28 defines V_to = 4.37 m/s *from the wing*: wing loading at AR 5, 192 mm², CL_max 1.07, at 0.25 g (S28 §1, full-text). The spring route's target is therefore a wing parameter. The two routes act on the same energy budget, one cutting demand (∝ 1/S) and the other raising supply, so their effects multiply.

Calculated: at S28's 0.25 g, enlarging the wing from 192 to about **357 mm²** at fixed CL_max would close the 1.86× gap. This ignores the extra fin drag in water during the stroke, which would push the area higher. S28 judges that 1925 mm² is "~10× the fish's own lateral area", which puts lateral area at roughly 190 mm², so 357 mm² is about 1.9× lateral area.

I do not claim this is buildable. The point is that **two separate failures do not show that their combination fails**, and the combination was never tested.

## 4. Is "independent … fail on different terms" accurate?

**No, on S29's own text.**
- **Not independent.** Both routes take S28's 4.37 m/s target, S28's 24 mm² frontal area and the 1.38 m/s measured burst. The spring route's target is literally the wing route's takeoff speed. A defect in S28's V_to would move both failures together.
- **Not different terms.** S28's row 1 is "3.2× speed / 10× KE" at water exit (full-text). S29 §0 then says: "S28's wall was not a wing problem … It is an energy-per-stroke × push-off-medium problem." So S29 itself re-reads the wing failure as the same energy-at-exit term. One constraint seen twice is not two independent representations converging. The claim's own sentence contradicts the paragraph it comes from.
- **What the evidence does support** (my inference): the shortfall shrinks from 10× to 1.2–3.1× when the power limit is removed, so whatever remains sits in muscle work per loading contraction, η_h and the target speed. That is narrower than "the problem itself".

## 5. Counter-examples and regimes

My search was two standard web searches. The scope of the negative is "small animals launching from water by a single impulse".

- **Pontellid copepods** (*Anomalocera ornata*) leap out of water as an escape (Gemmell et al. 2012, Proc. R. Soc. B; **search-summary** only). The summary reports 58–88 % of escape energy lost breaking the surface. A follow-up study on *A. patersoni* and *Pontella* reports about 1.25 m/s at the surface (**search-summary**). These animals are about 3 mm long, orders of magnitude lighter than the fish, and far below 4.37 m/s. **This is not a counter-example at this size.** It does show that S29's "optimism left in on purpose" (no surface-break penalty) may hide a large term, and that cuts in S29's favour.
- **Freshwater hatchetfish** (Gasteropelecidae) make ballistic leaps assisted by the pectoral fins at water exit (Wiest 1995, J. Zool. 236:571, and Saidel et al. 2004, both cited in an archerfish JEB paper; **listing/search-summary**, primary not read). **I found no measured takeoff speed**, so I cannot say whether any reaches 4.37 m/s. The value is `unknown`.
- I found **no published counter-example** of a ~0.4 g animal leaving water at ≥ 4.37 m/s from a single impulse. Within this narrow search, the claim's empirical side is not contradicted.

## 6. Evidence level

"Derived" is acceptable for the numbers. The deep conclusion itself, however, is an **inference or interpretation**. No calculation produces "the limit is a property of the problem". It should carry a level such as "inferred from two derived budgets". This is a minor labelling defect, not a falsification.

## 7. What survives and what does not

- **Survives (derived):** under single-contraction loading, water-only push-off and S28's target, the LaMSA route is short by 1.22–3.08× (1.86× central). The numbers reproduce exactly.
- **Does not survive:** the "two independent representations failing on different terms" premise, and the generalisation from it to "a property of single-impulse launch from water at this size".
- **Corrected statement (mine):** "Under single-contraction spring loading, push-off against water only (η_h ≈ 0.37) and S28's 4.37 m/s wing-derived target, the binding term is muscle work per loading contraction × η_h. Ratcheted multi-contraction loading (2 contractions at 53 J/kg, calculated), push-off against a rigid surface, or a wing–spring combination are untested and are not excluded by this analysis."

```swarm-challenge
{"claim_id": 231, "outcome": "weakened", "reason": "The arithmetic reproduces exactly (1.86x, 1.22-3.08x), but the two routes share S28's wing-derived 4.37 m/s target and by S29's own text fail on the same exit-energy term, and the binding term rests on an unstated single-contraction loading assumption that closes at 2 latched loading contractions (53 J/kg, calculated), so the barrier is shown for single-contraction loading with water push-off, not for single-impulse launch as such.", "corrected_value": null, "depends_on": ["S29-organism.md (commit 44ed2195) inputs: m 0.40 g, V 4.37 m/s, Cd 0.2, A 24 mm2, stroke 1.09 cm", "S28 V_to 4.37 m/s derived from wing loading (S28 section 1)", "Frith-Blake pike C-start eta_h 0.37 (via S29, abstract)", "Mendoza-Azizi2021 frog spring-loading 32-81 J/kg muscle (via S29)", "Ker1981 tendon return 0.93 (via S29)", "F_ONE_SIDE 0.30 assumed by S29", "S29 section 2.4 spring-volume table (capacity passes)"]}
```
