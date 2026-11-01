model: gemini-4-argon
utc: 2026-11-01T14:39:35Z
elapsed_s: 24
usage: {"promptTokenCount": 20916, "candidatesTokenCount": 1636, "totalTokenCount": 22552, "promptTokensDetails": [{"modality": "TEXT", "tokenCount": 20916}], "candidatesTokensDetails": [{"modality": "TEXT", "tokenCount": 1636}]}

### 1. Top Flaws & Overclaims

**Biomechanics & Physics (`common.py`)**
* **No Aquatic Trade-off (Fatal Flaw):** Enlarging pectoral fins ($p: 0.137 \to 0.674$) and asymmetrical tails ($c$) imposes massive hydrodynamic drag, energetic, and maneuverability costs during the >99% of life spent underwater. The model assumes `V_exit = 10.0 m/s` and `e_swim = 0.30` are constant across all phenotypes. Without a hydrodynamic cost to fin size, fitness is artificially monotone with wing area ($S$), which is why the Lande walk drives $p \to p_{\max}$ and $A \to 1.0$ (maximizing paddle area).
* **Ground Effect Omitted:** Flying fish glide within $\sim 0.05\text{--}0.5\text{ m}$ of the water surface (wingspan $b \approx 0.2\text{ m}$, so height-to-span $h/b < 1$). Induced drag in ground effect is reduced by 30–50%. Ignoring this while using a standard parabolic drag polar (`CD0=0.06, e=0.8`) miscalculates the optimal aspect ratio ($A$) and underestimates flight range.
* **Morphological & Aerodynamic Inconsistency:** The model fixes length-weight scaling (`a_LW = 0.00632`, halfbeak) across the evolutionary walk, yet computes target mass using `a_LW = 0.01354` (exocoetid). Consequently, the "target" phenotype on the grid has a distorted standard length ($SL \approx 17.4\text{ cm}$ instead of $13.5\text{ cm}$) and wing geometry. Furthermore, applying a fixed high-Reynolds airfoil polar to a small, low-$A$ ancestral paddle fin ($A=2$) overstates ancestral lift.
* **Control Rule Artifact:** `CL = min(CL_opt, CL_level)` forces fast, low-wing-loading fish to fly at suboptimal lift coefficients simply to avoid climbing at exit, throwing away kinetic energy that real gliders convert into altitude and range.

**Evolutionary Biology (`reachability.py`)**
* **Fitness Definition:** Fitness ($W$) is equated to *per-attack survival*, ignoring fecundity, foraging, and metabolic survival. 
* **Arbitrary $G$-Matrix:** Setting $G$ diagonal with $CV_A=0.05$ for $A, M$ and $0.05 \times \text{grid\_range}$ for $p, c$ is arbitrary and ignores developmental pleiotropy (e.g., bioelectric/allometric coupling between pectoral and caudal fins documented in Daane et al. 2021).
* **Grid Resolution & Drift:** Under $H_{\text{vis}}$, the bottleneck step is $\Delta W \approx 7 \times 10^{-5}$. Calling this "strictly improving" overclaims reachability; depending on effective population size ($N_e$), a selection coefficient $s < 10^{-4}$ is effectively neutral and subject to drift.

**Behavioural Ecology (`escape_ecology.py`, `collective.py`)**
* **In-Water Flee Speed (`U_flee = 1.7 m/s`):** In `collective.py`, alerted swimming fish flee at $1.7\text{ m/s}$, whereas in `common.py` all fish can burst to `V_exit = 10.0 m/s` to launch. Handicap-fixing the `swim` control to $1.7\text{ m/s}$ against a $10\text{ m/s}$ predator guarantees in-water capture and inflates the benefit of gliding.
* **Predator Telepathy & Teleportation:** In `collective.py`, when a target launches (`status == 1`), the predator immediately steers toward the *exact future landing coordinates* (`tpos = lpos1`). If the predator tracks the fish and `burst_left > 0`, it moves at `U_burst` ($10\text{ m/s}$) while the glider's horizontal speed decays below $10\text{ m/s}$, meaning the predator arrives at the landing spot *before* the fish lands and waits for it.

---

### 2. Circularities & Missing Controls

**Circularities**
1. **$H_{\text{vis}}$ Monotonicity:** $H_{\text{vis}}$ assumes $\ln P_{\text{reacquire}} \propto -d / d_{\text{vis}}$. Because any positive lift or taxi boost increases $d$ slightly, and there is no cost to fin size, a strictly improving path for $p$ and $c$ is baked into the algebra.
2. **Taxi Surrogate (`s(c) * phi`):** The model defines taxi speed gain as proportional to both tail asymmetry $s(c)$ and aerodynamic weight support $\phi$. This hard-codes the evolutionary order (pectoral fins $\phi$ must evolve before tail asymmetry $c$ has any gradient), making the "discovery" of the evolutionary trajectory circular.

**Missing Controls**
1. **Ballistic Leap Control ($S=0$):** A pure ballistic jump at $10\text{ m/s}$ and $15^\circ$ yields $d \approx 5.2\text{ m}$. You need a zero-lift control to separate how much of the ancestor's escape probability comes from swimming speed vs. actual aerodynamic lift.
2. **Swim-with-Alarm (`swim_sync`):** `collective.py` compares `glide_sync`, `glide_indep`, and `swim` (which has no alarm cascade? Actually, `swim` gets `alerted` via `hops` only if `mode == 'glide_sync'`). `hops` is set to `None` for `swim`! Thus, `glide_sync` vs. `swim` confounds *gliding* with *social alarm transmission*. You must include a `swim_sync` control.
3. **High-Speed In-Water Burst Control:** A swimming control where fish burst in-water at `V_exit` ($10\text{ m/s}$) with high maneuverability (jinking) rather than swimming in a straight line at $1.7\text{ m/s}$.

---

### 3. What Each Model Can and Cannot Establish

* **Model 1 (Reachability):** *Can* establish that under a threshold pursuit model ($H_{\text{chase}}$), short ancestral leaps lie on a fitness plateau, requiring an alternate selective gradient (like visual break, $H_{\text{vis}}$) to initiate evolution. *Cannot* establish why flying fish evolved high aspect ratios ($A$) or specific body masses ($M$), because it lacks hydrodynamic trade-offs and ground-effect physics.
* **Model 2 (Escape Ecology):** *Can* establish first-order kinematic bounds on predator burst speeds against which gliding is effective, and that single-launch kinetic costs are a small fraction of daily RMR. *Cannot* establish net ecological payoff without foraging/swimming drag costs of enlarged fins.
* **Model 3 (Collective ABM):** *Can* illustrate how dilution and confusion scale per-capita risk with group size $N$. *Cannot* isolate the collective benefit of gliding from social alarm cascades (due to the missing `swim_sync` control and handicapped `U_flee`), nor model realistic aerial pursuit.