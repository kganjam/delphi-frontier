### Review of Prior Fixes

1. **C-start treated as pitch:** **Yes.** 
   Stage 1 rotates horizontal azimuth `psi` (`psi_t = wrap(a_p + side * et)`), separating heading yaw from vertical pitch `gam` (`fast_start.py: simulate`).
2. **Discontinuity at glide release ($h_0 = 1\text{ m}$):** **Yes.** 
   Baseline after-taxi glide runs use `h0=H0_CONT` ($0.1\text{ m}$) with $\gamma_0 = 0$ (`fast_start.py: glide_ranges`).
3. **Missing taxi spray/wetted drag:** **Yes.** 
   Added `taxi_water_drag` accounting for strut spray drag ($0.24 \cdot \frac{1}{2}\rho V^2 t^2$) and residual wetted hull drag (`fast_start.py: taxi`, `caudal_cpg.py: taxi_water_drag`).
4. **Roll model combining dihedral with "otolith blind":** **Yes.** 
   The otolith output in lateral state-space is explicitly modeled as apparent side-force acceleration (`phi_oto = -Yb / (m * C.G)`), distinct from true bank (`phi_vis`) (`glide_stab.py: lat_ss`).
5. **Single shared delay for canal and vision:** **Yes.** 
   `closed_loop` and `mc` now track independent delay chains per sensor row (`nds = [int(round(t / dt)) for t in delays]`), allowing $\tau_v \neq \tau_c$ (`glide_stab.py: closed_loop`).

---

### New Bugs

1. **`fast_start.py: simulate` (Sign error in predator intercept trajectory):**
   ```python
   adv = np.minimum(s["u_pred_ms"] * t1, s["r0_m"])[:, None]
   pred = fish + (p0 - fish) * (1 - adv / s["r0_m"][:, None])
   ```
   At $t_1$, `pred` moves *toward* `fish`. However, during the step loop:
   ```python
   d = fish - pred
   pred = np.where(active[:, None], pred + dt * s["u_pred_ms"][:, None] * d / r[:, None], pred)
   ```
   Vector `d` is `fish - pred` (points predator $\to$ fish), so `pred + dt * u_pred * d / r` moves the predator toward the fish. But during initial initialization, `(p0 - fish)` points fish $\to$ predator; as `adv` increases, `(1 - adv/r0)` shrinks `p0 - fish`, correctly moving `pred` closer to `fish`, but if $e_p$ is negative (from below), $p_0$ was computed relative to fish at $-d_0$, but $p_0$ $z$-coordinate is `-s["d0_m"] + s["r0_m"] * np.sin(e_p)`, while fish is at `[0, 0, -s["d0_m"]]`, making $p_0 - \text{fish} = [x, y, r_0 \sin(e_p)]$, which incorrectly places the predator $r_0$ below `fish`, but `r0` is the 3D distance, yet $x, y$ are also multiplied by $\cos(e_p)$, which is geometrically consistent, but in:
   ```python
   psi = np.sign(psi_t) * np.minimum(np.abs(psi_t), cap)
   ```
   `psi_t` is an absolute angle wrapped to $[-\pi, \pi]$, not an angular increment from $\psi_0 = 0$. If $\psi_t = 3.0\text{ rad}$ and $\text{cap} = 0.5\text{ rad}$, $\psi$ turns to $+0.5\text{ rad}$, but if $\psi_t = -3.0\text{ rad}$, $\text{wrap}(\psi_t)$ is $-3.0$, and it clamps toward 0 rather than rotating the shortest direction from initial $\psi=0$.

2. **`glide_stab.py: long_ss` (Sign/formula error in $Z_\delta$):**
   ```python
   Zd = -qd * S * d["CLde"] / (m * V)
   ```
   In conventional stability axes, dimensional plunge control derivative $Z_{\delta_e} = -\frac{q S C_{L_{\delta_e}}}{m}$ (units $1/\text{s}^2$ or $\text{m}/(\text{s}^2\cdot\text{rad})$ for plunge velocity, or when state is $\alpha$, $Z_{\delta_e} / V = -\frac{q S C_{L_{\delta_e}}}{m V}$). Here state 1 is $\alpha$, so $\dot{\alpha}$ has dimension $1/\text{s}$, which matches. But in line 96:
   ```python
   A = np.array([..., [Zu, Za, 1, -C.G * sg / V], [Mad * Zu, Ma + Mad * Za, Mq + Mad, -Mad * C.G * sg / V], ...])
   B = np.array([0, Zd, Md + Mad * Zd, 0.0])
   ```
   The second row of $A$ has $q$-coupling as $+1$ ($\dot{\alpha} = Z_\alpha \alpha + q + \dots$). However, $M_{\dot{\alpha}}$ coupling into $\dot{q}$ appears as `Mad * Za` and `Md + Mad * Zd`. Because $\dot{\alpha} = Z_\alpha \alpha + \dots + Z_\delta \delta$, $\dot{q} = M_\alpha \alpha + M_{\dot{\alpha}} \dot{\alpha} + M_\delta \delta$ requires eliminating $\dot{\alpha}$. But `Mad` is defined as $\frac{q S c^2 C_{m_{\dot{\alpha}}}}{2 V I_{yy}}$, which has dimension $[1/\text{s}]$, while $Z_d$ has dimension $[1/\text{s}]$; their product `Mad * Zd` has dimension $[1/\text{s}^2]$, whereas $M_\delta = \frac{q S c C_{m_{\delta}}}{I_{yy}}$ has dimension $[1/\text{s}^2]$. While dimensions match, $M_{\dot{\alpha}}$ was defined with $2 V$ in the denominator; $C_{m_{\dot{\alpha}}}$ is nondimensionalized by $\frac{\dot{\alpha} c}{2 V}$. Thus, $\frac{\partial M}{\partial \dot{\alpha}} = \frac{q S c^2 C_{m_{\dot{\alpha}}}}{2 V I_{yy}} = M_{ad}$. But when substituting $\dot{\alpha}$, the term multiplying $q$ in the $\dot{q}$ equation must be $M_q + M_{\dot{\alpha}} (1)$, yet in $A[2, 2]$ it is `Mq + Mad`. `Mq` is defined as $\frac{q S c^2 C_{mq}}{2 V I_{yy}}$, which also has an extra factor of $1/(2V)$ relative to $C_{mq}$ non-dimensional time; however, $A[2, 3]$ includes `-Mad * C.G * sg / V`, which is missing the gravity pitch component: $g \sin(\gamma)$ instead of $g \cos(\gamma)$.

3. **`caudal_cpg.py: lobe_thrust` (Wrong sign on drag projection):**
   ```python
   return np.mean(q * (CL * np.sin(beta) - CD * np.cos(beta)), axis=1)
   ```
   $\beta = \arctan2(v, U)$ where $v$ is lateral velocity and $U$ is forward velocity. The hydrodynamic force along the forward flight direction ($x$) is $L \sin\beta - D \cos\beta$ only if $\beta$ is measured from the lateral axis. Here $\tan\beta = v/U$, meaning $\beta=0$ when $v=0$ (pure forward motion). For a foil moving forward at $U$ with lateral motion $v$, relative flow velocity vector is $\mathbf{W} = [-U, \mp v]$. The forward thrust component ($+x$) is $+L \sin\beta - D \cos\beta$ only if lift acts forward, but relative wind comes from ahead and side: forward projection of lift is $-L \sin\beta$ (retarding) and drag is $-D \cos\beta$, producing negative thrust rather than positive thrust. For a flapping foil producing thrust, lift tilts forward such that the forward force is $L \sin\beta - D \cos\beta$ ONLY when $\beta$ is the angle relative to the transverse direction ($\arctan2(U, v)$), not $\arctan2(v, U)$.
