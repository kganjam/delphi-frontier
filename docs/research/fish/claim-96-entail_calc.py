"""Claim 96 entailment arithmetic. Every output here is CALCULATED, not measured.
Inputs are tagged with their source in the companion markdown file."""
import math

g = 9.81
# Upstream (S6-D / S26-D) inputs -- assumptions or relays, see claim-96-entail.md
m, N, L, n = 0.10, 14, 0.12, 1.0          # kg, rays/fin, m, load factor (assumptions)
EI_p_src = 3.8e-6                          # N m^2, bluegill ray (Puri 2018 relaying Flammang 2013)
EI_p_alben_free = 1.07e-6                  # N m^2, S26-D back-calc from Alben 2007 (one base free)
L_src = 0.0403                             # m, Alben 2007 max bluegill pectoral ray length
F_lock = 12.0                              # Alben 2007 measured clamped/one-free ratio (n = 1)
d_bluegill = (1e-3, 2e-3)                  # m, Puri 2018 bluegill ray diameter

P = n * m * g / (2 * N)
EI_req = P * L**2 / (8 * 0.10)
M_base = P * L / 2
print(f"[C0] per-ray load P = {P:.4f} N, EI_req = {EI_req:.3e} N m^2, base moment = {M_base:.2e} N m")

# C1: minimum passive EI and its scaling consequences
EI_min = EI_req / F_lock
print(f"[C1] passive EI needed at L=0.12 m for 12x to suffice: {EI_min:.3e} N m^2")
for name, ei in [("relay 3.8e-6", EI_p_src), ("Alben one-free 1.07e-6", EI_p_alben_free)]:
    ratio = EI_min / ei
    b = math.log(ratio) / math.log(L / L_src)
    dfac = ratio ** 0.25  # constant E, EI ~ d^4
    print(f"     baseline {name}: EI must rise x{ratio:.1f}; exponent b(EI~L^b) >= {b:.2f} (isometry = 4);"
          f" diameter must rise >= x{dfac:.2f} -> d_120 >= {dfac*d_bluegill[0]*1e3:.2f}-{dfac*d_bluegill[1]*1e3:.2f} mm")

# C2: hemitrich couple force at the base when locked, and muscle cross-section implied
s = L / L_src
for frac_label, frac in [("full diameter", 1.0), ("centroid sep ~0.7 d (bone ~30% of thickness, Alben 2007)", 0.7)]:
    seps = [frac * dd * s for dd in d_bluegill]
    F = [M_base / x for x in seps]
    print(f"[C2] isometric d_120 = {d_bluegill[0]*s*1e3:.1f}-{d_bluegill[1]*s*1e3:.1f} mm; {frac_label}:"
          f" couple force F = {min(F):.2f}-{max(F):.2f} N per ray")
F_lo, F_hi = M_base / (d_bluegill[1] * s), M_base / (0.7 * d_bluegill[0] * s)
for label, sig in [("white max 289 kPa (dogfish)", 289e3), ("red min 57 kPa (marlin)", 57e3), ("red 142 kPa (dogfish)", 142e3)]:
    print(f"     muscle stress {label}: CSA per ray {F_lo/sig*1e6:.1f}-{F_hi/sig*1e6:.1f} mm^2;"
          f" both pectoral fins ({2*N} rays) {2*N*F_lo/sig*1e6:.0f}-{2*N*F_hi/sig*1e6:.0f} mm^2")
print(f"     total tension across {2*N} rays: {2*N*F_lo:.1f}-{2*N*F_hi:.1f} N vs body weight {m*g:.2f} N")
print(f"     Lauder SICB 10-15 mN per 100 um (bluegill actuation) scaled x s^2 = x{s**2:.1f}: {10e-3*s**2*1e3:.0f}-{15e-3*s**2*1e3:.0f} mN")

# C3: glide duration from Fish 1990 distances and speeds
dist = (15, 92); v = (10, 20)
print(f"[C3] single-glide duration {dist[0]/v[1]:.2f}-{dist[1]/v[0]:.1f} s (15-92 m at 10-20 m/s)")

# C4: Fish 1990 regressions at M = 0.1 kg
for genus, (aL, bL), (aS, bS) in [("Cypselurus", (0.460, 0.355), (0.651, 0.375)),
                                   ("Exocoetus", (0.462, 0.347), (0.774, 0.380))]:
    SL = aL * m**bL; span = aS * m**bS
    print(f"[C4] {genus} @0.1 kg: SL = {SL*1e3:.0f} mm, span = {span*1e3:.0f} mm, semispan = {span/2*1e3:.0f} mm,"
          f" 0.79*SL = {0.79*SL*1e3:.0f} mm")
print(f"     unit check, Danichthyes 0.53 kg span = {0.622*0.53**0.310:.3f} m (paper text: 0.51 m)")
for Lx in (0.10, 0.12, 0.137, 0.161):
    EIp = EI_p_src * (Lx / L_src)**4
    EIr = P * Lx**2 / 0.8
    print(f"     L = {Lx*1e3:.0f} mm: isometric passive EI {EIp:.2e}, EI_req {EIr:.2e}, margin of 12x = {F_lock*EIp/EIr:.1f}")

# C5: load-factor headroom
margin = F_lock * EI_p_src * (L / L_src)**4 / EI_req
for share in (1.0, 0.918, 0.760):
    print(f"[C5] pectoral share of weight {share:.3f}: margin {margin:.2f} -> tolerable load factor n <= {margin/share:.1f}")
