# POST-HOC perturbation ensemble (added after E3 failed; suggested by gemini-4-argon), UNMODIFIED engine, L40S
Job claude-voxgpu-ens-cilia-l40s-e2 (aijob-e00arkvn9b6qh733mk), batch ens_dt090: 216 bodies (9 patterns x 24 members), 1260.9 s, rc 0,
0 diverged, 0 invalid. Endpoint config (E=1e6, collision on, DtFrac 0.9). Member 0 unperturbed; members 1-23: every voxel phase
+ N(0, 1e-7 cycles), seed 20261101+7. Question: is the E3 mirror error the same size as sensitivity to an O(1e-7) unmirrored perturbation?

| pattern pair | mirror error of ensemble means | SE of that difference | member rms spread |
|---|---|---|---|
| wave_px / wave_mx (x) | 0.401 mm | 0.022 mm | 0.061 / 0.088 mm |
| split_px / split_mx (x) | 0.251 mm | 0.013 mm | 0.032 / 0.055 mm |
| wave_py / wave_my (y) | 0.793 mm | 0.007 mm | 0.032 / 0.012 mm |
| diag_pxpy / diag_pxmy (y) | 1.003 mm | 0.002 mm | 0.008 / 0.006 mm |

Reading: perturbation spread is 3-100x smaller than the mirror error, and the mirror error of the means is 18-500 SE. At this
perturbation scale the E3 failure is a SYSTEMATIC deterministic asymmetry of the discrete solver under contraction actuation, not
noise amplification. Caveats: one eps (1e-7 cycles); a larger perturbation could show larger spread; the asymmetry's size and sign
change with dt (E3 table), so it is a discretisation-dependent bias, not a fixed lattice-axis bias. The cilia arm shows the same
solver mirror-symmetric to ~2e-5 away from the friction threshold, so the bias is tied to the contraction/contact dynamics.
Cross-job determinism: member 0 equals the s1 endpoint run (other job, other node) bitwise for all 9 patterns.
