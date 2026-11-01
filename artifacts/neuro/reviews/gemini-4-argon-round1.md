### Model M2 (`caudal_cpg.py`)

**1. Physics or biology errors, wrong signs, wrong formulas**
* **Wrong formula (`lock_analytic`):** You assert a unidirectional chain locks iff $|\Delta\omega_i - \Delta\omega_0| \le c$ for all $i$. False. In a cascade where segment $i$ only reads $i-1$, the steady-state frequency of every locked oscillator must equal the leader's ($\omega_0$). Thus, the phase difference across link $i$ must satisfy $c \sin(\psi_i - \text{lag}) = \omega_{i-1} - \omega_i$. With linear per-segment detuning ($\omega_i = \omega_0 + i \cdot \delta\omega$), the local frequency jump across *every* adjacent pair is identical: $\omega_{i-1} - \omega_i = -\delta\omega$. The true locking condition is $|\delta\omega| \le c$, and all intersegmental lags $\psi_i$ are identical. Your code computes `dw = 2*pi*detune * np.arange(1, N)`, comparing segment $i$ to segment 0 as if the topology were a star graph, overestimating the required coupling by a factor of $N-1=7$.
* **Hydrodynamic omission (`lobe_thrust`, `main` taxi loop):** During taxi, `lobe_thrust` computes foil induced and skin-friction drag, and `main` subtracts aerodynamic drag `Dair`. You completely omit **hydrodynamic wave and spray drag** (Froude drag) of the immersed lower lobe and caudal peduncle piercing the free surface, which dominates resistance at the air-water interface.
* **Uncoupled kinematics (`ebt_thrust`, `muscle_amp`):** You apply a muscle low-pass filter to tail amplitude $H(f)$, but treat body wavelength $\lambda$ as independent of $f$ and $H$. In real undulatory swimming, fluid-structure interaction with passive body stiffness causes $\lambda$ to drop as $f$ rises.

**2. Unacknowledged assumptions driving the headline result**
* Your headline claim that taxi is required because submerged speed is power-capped, whereas taxi reaches takeoff speed, is entirely driven by switching propulsive regimes from high-drag `drag_sub` to `lobe_thrust` while setting surface-piercing drag to zero and assuming a miraculous passive feathering limit (`alpha_feather_deg = 12.0`) that prevents caudal stall at 50–70 Hz.

**3. Overclaims**
* Calling `lock_analytic` an analytic solution to the reused chain when it solves the wrong graph topology, then masking the error in `main` by excluding a massive `border` region (`< 0.15`) where your formula fails against the numerical integration.

**4. Single most important fix**
* Fix `lock_analytic` to use adjacent-segment detuning `dw = 2 * math.pi * detune_Hz_per_seg` (constant across links), and add a hydrodynamic surface-piercing drag term to the taxi equilibrium.

---

### Model M1 (`fast_start.py`)

**1. Physics or biology errors, wrong signs, wrong formulas**
* **Kinematics/Neuroethology error (`simulate`):** C-starts are yaw turns executed in the horizontal plane via unilateral axial contraction. You take a 2D horizontal escape trajectory (`et`), add it to the predator's vertical elevation angle (`h1 = e_pred_deg + et`), fold it via `arcsin(sin(h1))`, and take `np.maximum(g1, g2)` to force an upward pitch angle `gam`. Fish cannot execute a C-start in pitch, nor do Mauthner cells compute `maximum(g1, g2)` to guarantee surface-ward steering.
* **Energy non-conservation (`simulate`):** At emergence, you set initial taxi speed to `V = Ue * cos(ge)`, throwing away the vertical kinetic energy $\frac{1}{2}m(U_e \sin\gamma_e)^2$ without converting it into an initial leap apex $h_0$. Then, in `glide_ranges`, you hardcode `h0 = 1.0 m` and `gam0 = 0.0` regardless of whether the fish barely cleared stall speed on the water surface or ballistic-leapt out of the water.

**2. Unacknowledged assumptions driving the headline result**
* The emergence probability (`P_emerge`) and time-to-surface are driven by `np.maximum(g1, g2)`, which rectifies random horizontal escape turns into deterministic upward climbs. Without this artificial rectification, half of the away-responses from a bottom-looming predator would dive deeper or stay horizontal.
* The glide range distribution (`glide_range_after_taxi_m`) is artificially inflated and compressed by gifting every fish a free 1.0 m altitude launch (`h0_m` from `C.ORG`) at the end of a surface taxi ($z=0$).

**3. Overclaims**
* Claiming that M1 "replaces [the glide model's] assumed fixed V0=12 m/s by a launch distribution" when the altitude `h0=1.0 m` and flight path angle `gam0=0` remain disconnected, hardcoded artifacts that violate continuity with the taxi phase ($z=0, \gamma=0$).

**4. Single most important fix**
* Enforce kinematic continuity at water exit: if the fish taxis on the surface ($z=0$), it must launch into `glide.integrate` from $h_0 \approx 0$ (requiring ground-effect aerodynamics or a positive launch pitch rate to climb), not teleport to $h_0 = 1.0\text{ m}$.

---

### Model M3 (`glide_stab.py`) & M4 (`NEURAL_IMPLEMENTATION.md`)

**1. Physics or biology errors, wrong signs, wrong formulas**
* **Inertia scaling error (`derivs`):** You compute dry + ballast pitch inertia `Iyy`, then multiply by `m / (m_dry + m_b)` to scale from 25 g to 50 g. That assumes the extra 25 g of mass is distributed at the exact same radius of gyration as the lead nose-ballast (`X_BALLAST = 0.015 m`). Worse, you compute `m_b` using `m_dry` instead of total mass `m`, violating CG trim for the 50 g fish.
* **Flight dynamics error (`roll_ss`, `simulate_nl`, M4):** You decouple roll into a 2-state $[\phi, p]$ system by assuming sideslip is instantaneously proportional to bank ($\beta = \kappa\phi$), then claim in `simulate_nl` and M4 that otoliths provide "~no bank information" because the glide is "coordinated" (`sens_gain = [0.1, 1.0]`). **A coordinated turn has $\beta = 0$ by definition.** If $\beta = 0$, the dihedral restoring moment $L_\beta \beta = L_\phi \phi$ is identically zero! Conversely, if the airframe relies on passive dihedral stability ($\beta = \kappa\phi \neq 0$), it is *side-slipping*, creating a lateral aerodynamic force $Y_\beta \beta$ that tilts the gravito-inertial vector out of the symmetry plane, which the otoliths *directly sense*. You cannot simultaneously give the plant dihedral restoring torque ($\beta \neq 0$) and starve the otolith sensor on the grounds of coordination ($\beta = 0$).

**2. Unacknowledged assumptions driving the headline result**
* The headline M3/M4 conclusion—that roll control fails without vision because otoliths are blind to bank in a coordinated glide—is entirely manufactured by hardcoding `sens_gain = [0.1, 1.0]` while retaining non-zero dihedral stiffness `Lphi` in `roll_ss`. 

**3. Overclaims**
* In M4, elevating the circular assumption (`sens_gain = 0.1`) into a biological finding ("**A bank reference that does not come from the otoliths alone...** Vision is needed").
* Claiming "exact" delay-stability boundaries while using a single shared delay buffer in `closed_loop_radius` (`nd = int(round(delay_s / dt))`), which forces the fast semicircular canal rate pathway and the slow visual attitude pathway to have the **exact same transport delay**, contradicting your own prose in M3/M4.

**4. Single most important fix**
* Replace the contradictory 2-state `roll_ss` with the standard 4-state lateral-directional state space $[\beta, p, r, \phi]$, compute the true gravito-inertial specific force $a_y = Y_\beta \beta / m$ at the otoliths, and assign separate delay buffers $\tau_{\text{canal}} \neq \tau_{\text{vision}}$ in `closed_loop_radius`.
