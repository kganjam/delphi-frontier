"""Challenge 225 -- independent recomputation of S29's spring-volume claim.
Run: python3 docs/research/fish/challenge_225.py
Every input is labelled: S29 (taken from S29 as stated), READ (search-summary of a source), ASSUMED (mine).
"""
M = 0.40e-3            # S29: body mass, kg
RHO_FISH = 1050.0      # S29 ASSUMED body density
W_STORED = 11.83e-3    # S29: energy stored in spring, central case, J (4.37 m/s target, 0.93 return)
RET_S29 = 0.93         # S29: spring return
KE_SCALE_553 = (5.53 / 4.37) ** 2   # S29 flags 5.53 m/s as the mass-consistent target; KE ratio (drag term scaled too: approximation)
BL = 0.030             # S29: 1 body length = 3.0 cm (its stroke table: 1.5 cm = 1/2 BL)
A_FRONT = 24e-6        # S29/S28: frontal area, m^2
SIG_ISO = 186e3        # READ (abstract, search-summary): cod fast skinned fibre max isometric tension 18.65 N/cm^2

v_body = M / RHO_FISH
print(f"body volume {v_body*1e9:.1f} mm^3")

def vol(u, w):
    v = w / u
    return v * 1e9, 100 * v / v_body

print("\n-- 1. independent redo of S29 rows (central, 4.37 m/s, return 0.93)")
E = 1.65e9
for s in (100e6, 75e6, 50e6, 13e6):
    u = s * s / (2 * E)
    mm3, pct = vol(u, W_STORED)
    print(f"tendon E 1.65 GPa @ {s/1e6:5.0f} MPa: u {u/1e6:.3f} MJ/m3 -> {mm3:6.1f} mm3 = {pct:5.1f} %   "
          f"[x1.60 target: {pct*KE_SCALE_553:5.1f} %]")
for Ef in (1.2e9, 0.65e9):
    u = 0.5 * Ef * 0.02 ** 2
    for ret in (0.93, 0.75):
        w = W_STORED * RET_S29 / ret
        mm3, pct = vol(u, w)
        print(f"fish tendon E {Ef/1e9:.2f} GPa @ 2% strain, return {ret}: stored {w*1e3:.2f} mJ -> "
              f"{mm3:6.1f} mm3 = {pct:5.1f} %   [x1.60 target: {pct*KE_SCALE_553:5.1f} %]")
print(f"KE scale factor 5.53 vs 4.37: {KE_SCALE_553:.3f}")

print("\n-- 2. packaging: a single series tendon loaded directly (no lever) by axial muscle")
for frac, tag in ((0.30, "one side ~30% of frontal area (ASSUMED)"), (1.0, "ENTIRE frontal area as muscle (upper bound)")):
    F = frac * A_FRONT * SIG_ISO
    delta = 2 * W_STORED / F           # linear spring loaded to peak force F stores F*delta/2
    for s in (75e6, 50e6):
        eps = s / E
        L = delta / eps
        A = F / s
        print(f"{tag:45s} F={F:5.2f} N, stretch {delta*1e3:5.1f} mm ({delta/BL*100:4.0f}% BL); "
              f"@{s/1e6:.0f} MPa: strain {eps*100:.1f}%, tendon L {L*1e3:6.0f} mm = {L/BL:4.1f} BL, A {A*1e6:.3f} mm2")
    eps = 0.02
    L = delta / eps
    print(f"{'':45s} fish tendon @2%: L {L*1e3:6.0f} mm = {L/BL:4.1f} BL")
