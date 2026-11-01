# gemini-4-argon review of the xenomorph protocol and print pipeline (2026-11-01, ~08:50 PST)

Model: gemini-4-argon via generativelanguage.googleapis.com v1beta generateContent. Prompt: protocol.json + first 9000 chars of printable.py, asked for <=10 ranked issues. Raw answer follows, then what was changed.

---
Here is a critical review of your preregistered CPM protocol and 3D printing pipeline, ranked by severity.

### 1. Catastrophic Energetic Failure in the Refinement Arm (Severity: Critical)
* **Issue:** In `refinement`, you scale cell radius by $s$ (so $V_0 \propto s^3$ and surface area $\propto s^2$), but leave $J$, $T$, and volume strength $\lambda_V$ unchanged. In the CPM Hamiltonian, $H = \sum J + \lambda_V (V - V_0)^2$. At $s=1.25$, a single-voxel fluctuation near $V_0$ changes volume energy by $\Delta H_V \approx \lambda_V(2\Delta V) \propto s^3$, while surface energy scales as $s^2$. Holding $T$ constant means the system thermally freezes at $s=1.25$ and boils/dissociates at $s=0.75$. Furthermore, diffusive time rescaling ($t \propto s^2$) is indefensible for surface-tension-driven compaction (viscous/active coalescence scales linearly, $t \propto s$, or via boundary mobility) and fails completely when acceptance probabilities $\exp(-\Delta H/T)$ are unscaled.
* **Fix:** Scale $\lambda_V \propto s^{-3}$ (or use fractional volume constraint $\lambda_V(V-V_0)^2/V_0^2$) and adjust $J$ or $T$ to keep the dimensionless fluctuation ratio $\gamma a^2 / T$ invariant across scales. Calibrate time rescaling empirically from initial compaction rates rather than assuming $s^2$.

### 2. "Made of Cells" Print Claim is a Ball-and-Stick Artifact (Severity: Critical)
* **Issue:** Compacted CPM cells deform into space-filling polyhedra (voronoi-like), whose centroids are separated by roughly $2R_{\text{eq}}$. In `printable.py`, you replace actual cell voxel geometries with undeformed spheres of radius $R_{\text{eq}}$ (`CELL_RADIUS_FACTOR = 1.0`). When polyhedra are replaced by equal-volume spheres at their centroids, they barely kiss or don't touch at all. Your `NECK_MIN_RADIUS_MM = 1.25` requirement will fail for nearly all biological contacts, triggering `strut_edges` to lace the entire aggregate with artificial 2.5 mm cylinders. The print is not "made of cells"; it is a synthetic truss network.
* **Fix:** Generate `<id>-cells.stl` by running smoothed marching cubes on *individual* cell voxel masks (perhaps slightly eroded to create visible intercellular grooves), rather than substituting centroids with analytic spheres.

### 3. Neighborhood Mismatch Between Engine and Metrics (Severity: High)
* **Issue:** The Morpheus lattice uses `neighborhood_order: 2` (26-connectivity in 3D: faces, edges, corners) for energy calculations, yet `measurements_per_snapshot` defines contact area and `n_aggregates` strictly by shared *voxel faces* (6-connectivity, order 1). Cells interacting energetically via edges/corners in the CPM are registered as "disconnected" in your metrics.
* **Fix:** Align metric neighborhood definitions with the CPM Hamiltonian by using the same neighborhood order (or weighted boundary length estimator) as Morpheus.

### 4. Broken Refinement Verdict Rule & Underpowered Gate (Severity: High)
* **Issue:** `refinement.scales` tests `[0.75, 1.0, 1.25]`, but `verdict_rule` specifies comparing "between scale 1.0 and 1.5" (which doesn't exist). Furthermore, gating resolution stability on whether the shift is smaller than the `max-min` spread of $N=4$ seeds rewards noisy metrics: high stochastic variance makes it *easier* to pass the stability gate.
* **Fix:** Correct the typo to `0.75 and 1.25`. Gate stability on a fixed physical tolerance (e.g., $<5\%$ shift in mean) and increase replicates to $N \ge 10$.

### 5. Flawed `core_shell_index` and Centroid Definitions (Severity: Medium-High)
* **Issue:** `core_shell_index` and `rg_all` are computed about the centroid of *all* cells. If the DAH arm forms 2–3 separate sorted clusters (a known failure mode in finite-time CPM), measuring radial distance from the global centroid renders `core_shell_index` geometrically meaningless. Even in a single aggregate, incomplete engulfment (an A/B Janus droplet) yields a positive `core_shell_index` without forming a core-shell topology.
* **Fix:** Compute `core_shell_index` and `rg` strictly on the `largest_cluster`, and supplement with an explicit topological check (e.g., fraction of A-cell surface area exposed to Medium must be $< 0.05$).

### 6. Defensibility of the Zero-Adhesion Definition (Severity: Medium)
* **Issue:** While $J_{xy} = J_{xM} + J_{yM}$ ($J_{AA}=J_{BB}=J_{AB}=20, J_{xM}=10 \implies \gamma=0$) is algebraically correct under Glazier & Graner (1993), in a discrete 3D lattice at $T=3.0$, $J_{xM}=10$ creates a massive entropic/pinning barrier against surface fluctuations compared to $J_{xy}=J_{xM}=0$. Furthermore, jammed cells in a finite `noflux` box experience entropic depletion forces that can alter `rg_norm` by $>5\%$, risking a false FAIL on your $0.95 \times \text{initial}$ gate.
* **Fix:** Set $J_{AA}=J_{BB}=J_{AB}=J_{AM}=J_{BM}=0$ so interfacial energy is identically zero without artificial lattice pinning, or match the exact cell-medium interfacial tension $\gamma_{xM}$ of the active arms while setting $\gamma_{AB}=0$ and subtracting homotypic cohesion.

### 7. Incorrect `k_needed` Math in Print Connectivity (Severity: Medium)
* **Issue:** `connectivity()` reports `radius_factor_needed_to_join_all` via `D / (Ri + Rj)`, which calculates the factor needed for spheres to *kiss* (neck radius $= 0$). Yet your join rule requires `neck_radius >= NECK_MIN_RADIUS_MM` ($1.25\text{ mm}$). If a user scales by the reported `k_needed`, the solid will still fail the join check.
* **Fix:** Compute `k_needed` so that the intersection circle has radius $h = \text{NECK\_MIN\_RADIUS\_MM}$, i.e., for equal spheres $k = \sqrt{(D/2)^2 + h_{\min}^2} / R$.

### 8. Uncovered Failure Mode: Cell Fragmentation (Severity: Low-Medium)
* **Issue:** Standard CPM without an explicit connectivity constraint allows cells to split into disconnected voxel islands when $T / \gamma$ is high (such as in the `zero` arm where $\gamma=0$). `cell_table` blindly averages voxel coordinates (`cx, cy, cz`) per cell ID; if a cell fragments across the box, its centroid lands in empty space.
* **Fix:** Add a Morpheus `ConnectivityConstraint` plugin or verify in `measurements_per_snapshot` that each cell ID forms a single 6-connected component.

---
