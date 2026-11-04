"""S22-D-D-D calculations. Every number printed is CALCULATED from the inputs below.
No input is a new observation. See S22-D-D-deepen.md for sources and read-levels."""

FF_LO, FF_HI = 0.65, 0.77            # flying-fish pectoral/SL, E. volitans (search-summary, carried over)
F_LO, F_HI = 1.74, 2.05              # alf/+ overgrowth proxy (S22-D-D: D18 Fig 1A pectoral; P14 Fig 1E caudal)

# The input under attack: wild-type zebrafish pectoral-fin length / SL (p0).
P0_S22DD = {"S22-D-D literal": (0.104, 0.104), "S22-D-D adopted (40-60% resected)": (0.173, 0.260)}
# Praveenraj et al. 2017, Table 1, pectoral-fin length %SL (search-summary; column mapping unknown).
PRAV = {"col a": (19.6, 22.5, 20.7), "col b": (18.0, 20.7, 19.3), "col c": (18.2, 25.8, 23.8)}

def row(label, lo, hi):
    need = (FF_LO / hi, FF_HI / lo)
    rz = (lo * F_LO, hi * F_HI)
    short = (FF_LO / rz[1], FF_HI / rz[0])
    print(f"{label:38s} p0 {lo:.3f}-{hi:.3f} | need {need[0]:.2f}-{need[1]:.2f}x | "
          f"Rz(proxy) {rz[0]:.2f}-{rz[1]:.2f} | shortfall {short[0]:.2f}-{short[1]:.2f}x")
    return short

print("Sensitivity: elasticity of Rz to p0 and to f is 1 each (Rz = p0*f).")
for k, (lo, hi) in P0_S22DD.items():
    row(k, lo, hi)
means = [v[2] / 100 for v in PRAV.values()]
mins = [v[0] / 100 for v in PRAV.values()]
maxs = [v[1] / 100 for v in PRAV.values()]
row("Praveenraj means (19.3-23.8 %SL)", min(means), max(means))
row("Praveenraj full ranges (18.0-25.8 %SL)", min(mins), max(maxs))

print("\nFactor-of-two test on p0 (central = Praveenraj means):")
for mult in (0.5, 2.0):
    lo, hi = min(means) * mult, max(means) * mult
    print(f"  p0 x{mult}: Rz {lo*F_LO:.2f}-{hi*F_HI:.2f} vs target {FF_LO}-{FF_HI}")
print("\nFactor-of-two test on f (same p0):")
for mult in (2.0,):
    print(f"  f x{mult}: Rz {min(means)*F_LO*mult:.2f}-{max(means)*F_HI*mult:.2f}")
print(f"\nf needed to reach FF_LO at Praveenraj means: {FF_LO/max(means):.2f}-{FF_LO/min(means):.2f}x")
print(f"literal reading 0.104 vs lowest Praveenraj minimum 0.180: ratio {0.180/0.104:.2f}")
