model: gemini-4-argon
utc: 2026-11-01T16:44:25Z

### 1. eco-reachability
* **(1) Artefact risk:** The monotonically improving path is an artefact of fixing water-exit speed (`V_exit = 10.0 m/s`) across all phenotypes and setting aquatic fin drag to zero (`kappa_fin = 0.0`). Because the ancestor gets a "free" 10 m/s launch and pays no swimming penalty for growing oversized pectoral fins, any aerodynamic surface area immediately extends the ballistic leap and increases `H_vis`, smoothing out the fitness valley.
* **(2) Unsupported claims:** You claim that in the `H_vis + H_chase` sensitivity rows, "the walk ends at p = 0.22–0.73 with broad fins (A about 2), never within 0.05 of the target." You only show aspect ratio data (`A = 1.87`) for the single default run; no numbers are shown to support the claim that `A` stays near 2 across the other 29 rows.
* **(3) Missing from `does_not_establish`:** That water-exit velocity (`V_exit`) is invariant with body mass, fin area, or caudal morphology during the transition.

### 2. eco-escape-ecology
* **(1) Artefact risk:** The step-change in `H_chase` escape probability (0.30 to 1.00) is an artefact of the `dV_taxi = 8.0 m/s` assumption. The model grants the target phenotype an extra 8 m/s of speed at takeoff *solely* by scaling with fin lift and asymmetry, rather than modelling hydrodynamic tail-thrust against water drag. This automatically pushes total airspeed (18 m/s) past the predator's 10 m/s burst speed.
* **(2) Unsupported claims:** The sensitivity claim that "the target's gain stays positive across the whole swept aerial hazard 0–0.40 /s" is asserted without showing the escape probability numbers at `beta_air = 0.40 /s`. 
* **(3) Missing from `does_not_establish`:** The mechanics and drag costs of surface-taxiing propulsion (speed gain is a kinematic parameter, not a solved force balance).

### 3. collective-school-escape
* **(1) Artefact risk:** The finding that alarm cascades help gliders (`0.773 -> 0.133`) but fail swimmers (`0.882 -> 0.953`) is an artefact of the massive, hard-coded speed asymmetry: gliders are granted an instantaneous jump to launch speeds (~10–18 m/s), whereas swimmers are capped at a sluggish `U_flee = 1.7 m/s` against a predator bursting at likely ≥10 m/s. Your own sensitivity check admits this: giving swimmers 10 m/s drops their capture rate to 0.03. It is a speed effect, not a gliding effect.
* **(2) Unsupported claims:** The claim lacks a stated predator burst speed in `parameter_unknowns` (it lists `r_burst`, `U_app`, and `U_flee`, but omits `U_burst`), making the 1.7 m/s vs. 10 m/s comparison impossible to fully verify from the text shown.
* **(3) Missing from `does_not_establish`:** That gliding is uniquely required for alarm-cascade efficacy (since fast sub-surface swimming achieves the same survival benefit), or the energetics/false-alarm costs of hair-trigger cascades.