# Challenge 238: is Sutton 2019's 2.5 g crossover kept apart from a feasibility threshold?

**Claim under review** (S30, `docs/research/fish/S30-organism.md` on branch
`origin/claude/s30-launch-budget-mass-k71prf`, §0 item 5 and §4):

> "Sutton 2019's 2.5 g crossover is a DIFFERENT quantity -- spring versus muscle energy per kg on rigid
> ground -- and is not a feasibility threshold. The two were kept apart rather than conflated."

Recorded evidence level: literature. Value: 2.5 g.

**Verdict: SURVIVED.** I found two minor defects. Neither touches the claim itself. Both sit in supporting
sentences, and both are listed in §5.

## Sources and read-levels

- **Sutton, Mendoza, Azizi, Longo & Olberding 2019**, *Integr. Comp. Biol.* 59:1609, PMC6907395,
  doi 10.1093/icb/icz145. Read-level: **full-text**.
  - The PMC HTML page returned a reCAPTCHA wall.
  - The full-text JATS XML came from the Europe PMC REST endpoint
    (`/europepmc/webservices/rest/PMC6907395/fullTextXML`, HTTP 200, 108,688 bytes). I stripped the tags
    and searched the text.
  - Every quotation below comes from that text. I did not use S30's quotations.
- **S30-organism.md** (the author's document). Read-level: full-text, from the git branch.
- I did not read any other source. Where I mention Ilton et al. 2018 or Longo et al. 2018, I am reporting
  only that Sutton cites them, nothing more.

## 1. Independent arithmetic

Inputs are taken from Sutton's text: muscle output 3.6 J/kg at 1 g and 11.25 J/kg at 1 kg; spring output
4.2 J/kg (28 % of 15.0 J/kg). All of the following is **calculated by me, not observed**.

| Quantity | My result | S30 / Sutton states | Agrees? |
|---|---|---|---|
| √(2·4.2) spring take-off speed | 2.898 m/s | 2.90 m/s | yes |
| √(2·3.6) muscle, 1 g | 2.683 m/s | 2.68 m/s; Sutton gives 2.7 | yes |
| √(2·11.25) muscle, 1 kg | 4.743 m/s | 4.74; Sutton gives 4.7 | yes |
| √(2·15) muscle ceiling | 5.477 m/s | 5.48 | yes |
| Two-point log slope ln(11.25/3.6)/ln 1000 | 0.1650 | 0.165 | yes |
| Mass where the power law reaches 4.2 J/kg | **2.55 g** | Sutton: 2.5 g | yes. The two-point interpolation reproduces Sutton's figure. |
| 4.37²/2 | 9.548 J/kg | 9.55 | yes |
| Water ceiling: 0.37 × 15 J/kg | 5.55 J/kg, which is < 9.55 | "neither reaches it" | yes, at every mass |
| Water spring: 0.37 × 4.2 J/kg | 1.55 J/kg, which is < 9.55 | same | yes |
| Mass where the power law reaches 9.55 J/kg | **≈ 370 g** | S30: "only above ~1 kg" | **no**. See defect A. |

## 2. Is the quantity what S30 says it is? Proxy check

Sutton defines the output as "the kinetic energy density of the jump (jump kinetic energy/mass)", which
equals ½v² = gh. Sutton states the crossover as: "For masses >2.5 g … the modeled mass specific output of a
muscle-actuated system is higher than that of a spring-actuated system."

That is a comparison between **two actuators**. No requirement appears anywhere in it. S30's description,
"spring versus muscle energy per kg", is accurate.

Sutton's own framing points the same way: the crossover is about which mechanism lets an animal "jump
higher". It is not about whether any task is achievable.

I looked for a proxy substitution in the opposite direction: does S30 anywhere use 2.5 g as a minimum mass
for launch? It does not.
- S30's answer (§5) gives its own task-based crossover (m\* ≈ 39 mg, LaMSA).
- It gives an empirical floor separately (~1–2 g, exocoetids).
- Its comparison table (§4) puts the two crossovers in separate columns, with different "Compares",
  "Question", "Requirement term" and "Medium" rows.

**The claim that the two were kept apart is borne out by the document.**

### Normalisation: a possible proxy issue that I checked and that does not break the claim

The model's J/kg values are per kg of *accelerated mass*: 11.25 J/kg ↔ 4.7 m/s fixes this. Sutton calls
15.0 J/kg "the energy density of the muscle". Taken alone, that phrase is ambiguous between per kg of
muscle and per kg of body.

Sutton's own validation removes the ambiguity in practice. Sutton overlays the model lines on body-mass
data, restricted to animals with "10–20% body mass … devoted to muscles that directly or indirectly power
jumps". The empirical limits it quotes match the model numbers. These conversions are calculated by me:
- 0.49 m (spring-driven insects) × g = 4.8 J/kg, against the model's 4.2.
- 1.54 m (*C. familiaris*) × g = 15.1 J/kg, against the model's 15.0.

So S30 treating 4.2 J/kg as a per-kg-body supply follows Sutton's usage.

Even the empirical spring maximum (4.8 J/kg) is half of 9.55 J/kg. The conclusion that the 2.5 g
crossover is not a feasibility threshold for this task does not depend on how the J/kg is normalised.

S30 separately flags a 12.6× discrepancy against Mendoza & Azizi's 53 J/kg. That point is outside this
claim, and S30 does not resolve it.

## 3. Hidden assumption, relaxed

The load-bearing assumption is that "better actuator" and "sufficient actuator" are logically
independent. I tested it by asking whether any parameter change could turn Sutton's crossover into a
feasibility boundary.

- Sutton states that activation dynamics, starting length and lever effects "would only move the location
  of the crossover point, but would not eliminate it". Sutton never ties the crossover to a performance
  requirement.
- The crossover could coincide with a feasibility boundary only if the required ½v² happened to equal the
  spring's output at exactly that mass. With S30's numbers (9.55 vs 4.2 J/kg on rigid ground) it does not.
  With η_h = 0.37 in water the gap widens to 1.55 vs 9.55.
- **Relaxing "rigid ground" does not rescue a conflation either.** In water the crossover mass itself is
  unknown. Spring and muscle push-offs differ in speed and duration, so hydrodynamic losses would not
  scale equally between them. That is my inference; I found no source for it. This is a reason *not* to
  import 2.5 g into water even as an actuator-choice boundary. S30's scoping ("on rigid ground") already
  covers it.

## 4. Is the evidence level honest?

"Literature" is accurate for provenance. But **2.5 g is a simulated number, not a measurement**:
- Sutton: "We indicate where this crossover point occurs based on modeling".
- S30 labels it correctly in its own text ("Model results cited: Sutton 2019 (FULL)"). The ledger tag
  "literature" alone does not say "model".

Sutton's own empirical test of the *location* is weak, and **S30 omits this**. Quoting Sutton:
"the simulation's prediction is that as body mass near the crossover point, jump height and energy
density would increase. However, the frog data does not follow this pattern across body masses."

Sutton's data support the *existence* of a crossover: dog 1.54 m against insects 0.49 m, a 3.1×
ratio. They do not pin it at 2.5 g.

This makes the 2.5 g *value* softer, which slightly strengthens the claim's point that it cannot serve as
a threshold. It does not refute the claim.

## 5. Defects found, none fatal to the claim

**A. S30 overstates the mass at which muscle exceeds 9.55 J/kg.** S30 says muscle exceeds 9.55 J/kg "only
above ~1 kg (11.25 J/kg)".
- Sutton's two points bracket 9.55 J/kg below 1 kg. The power-law interpolation that reproduces Sutton's
  2.5 g puts it at **≈ 370 g**. This is calculated, not read off Sutton's Fig. 1G, which I could not
  extract as data.
- Sutton describes a curve that approaches an asymptote. A saturating curve sits *above* the log-linear
  chord between the two anchor points, which would put the crossing at or below ~370 g. That is my
  inference.
- Corrected statement: "on rigid ground, muscle exceeds 9.55 J/kg somewhere below 1 kg (≈ 0.37 kg by
  two-point interpolation)".
- This does not affect the water conclusion: 0.37 × 15 = 5.55 J/kg is below 9.55 at every mass.

**B. S30 omits Sutton's admission that the frog data do not follow the predicted pattern near the
crossover** (see §4). It should be recorded beside the 2.5 g value.

## 6. Counter-examples and missed regimes

**Negative search.** Scope: the full text of Sutton 2019 only, for "water", "swim", "fluid" and "aquatic".
The only aquatic hit is a reference-list entry (Longo et al. 2018 on snipefish *Macroramphosus scolopax*).
That paper concerns feeding strikes, not body launch from water. The paper itself contains no
fluid-medium crossover.

I did not search other literature for an aquatic spring-versus-muscle crossover. Whether one exists is
`unknown`.

Sutton cites Ilton et al. 2018 for a motor-driven crossover. I did not read Ilton, so I make no claim
about what it shows at fish scales.

None of this produces a case where the 2.5 g figure acts as a feasibility threshold.

## Conclusion

**SURVIVED.**
- The 2.5 g crossover is, in Sutton's own words, a comparison of mass-specific output between two
  actuators on rigid ground.
- It carries no requirement term.
- S30 keeps it in a separate column from its own supply-against-requirement crossover. It does not use
  2.5 g as a launch floor anywhere.
- My independent arithmetic reproduces 2.5 g (2.55 g) and every take-off speed.
- The two defects (A: 1 kg should be ≈ 0.37 kg; B: the frog-data caveat is missing) are in supporting
  sentences and do not change the claim.

```swarm-challenge
{"claim_id": 238, "outcome": "survived", "reason": "Sutton 2019 (full text) defines the 2.5 g crossover as spring-vs-muscle mass-specific jump output with no requirement term, independent arithmetic reproduces it (2.55 g), and S30 never uses it as a feasibility floor; only side defects found (muscle passes 9.55 J/kg near ~0.37 kg, not ~1 kg; Sutton's frog-data caveat omitted).", "corrected_value": null, "depends_on": ["Sutton et al. 2019 ICB 59:1609 PMC6907395 full text: crossover definition, 3.6 J/kg at 1 g, 11.25 J/kg at 1 kg, 4.2 J/kg spring (28% of 15.0 J/kg), rigid-ground model", "S30 required launch energy 9.55 J/kg (4.37 m/s at 0.25 g anchor)", "S30/S29 hydromechanical efficiency eta_h = 0.37 (Frith & Blake, pike)", "S30-organism.md section 4 comparison table and section 5 answer"]}
```
