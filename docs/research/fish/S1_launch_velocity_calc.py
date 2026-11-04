"""S1 launch-velocity arithmetic.  Pure arithmetic on stated inputs; no fitted or invented data.

Run:  python3 docs/research/fish/S1_launch_velocity_calc.py
Every input is named below with its provenance; change one and re-run.
"""
import json, math, pathlib

G = 9.81            # m/s^2
RHO_AIR = 1.225     # kg/m^3 (ISA sea level, given in the brief)
NU_AIR = 1.5e-5     # m^2/s, kinematic viscosity of air near 20 C (textbook value, inference-grade)
M = 0.4e-3          # kg, body mass from the brief (0.4 g)
L = 0.04            # m, body length from the brief (4 cm)
W = M * G           # N

SPAN_X = [1, 2, 3, 4, 5, 6]          # span as multiple of body length (brief)
AR = [3, 4, 5, 6, 7, 8]              # whole-wing aspect ratio b^2/S (brief)
CL = [0.6, 0.9, 1.2]                 # CL_max cases (brief; justification in the .md)

# Measured / reported speeds (see the .md for source and read-level of each).
SPEEDS = {
    "larva_5dpf_escape_example (Voesenek 2019, one start)": 0.15,
    "adult_Ucrit_Plaut2000_wildtype": 0.56,
    "adult_Ucrit_Palstra2010": 0.548,
}
# Inference-grade stretch value: the larval length-specific escape speed (~36-38 BL/s) applied
# to a 4 cm adult.  NOT a measurement; length-specific speed generally falls with size.
SPEEDS["INFERENCE_38BL/s_x_4cm (not measured)"] = 38 * L


def stall(S, cl):
    return math.sqrt(2 * W / (RHO_AIR * S * cl))


def grid():
    rows = []
    for k in SPAN_X:
        b = k * L
        for ar in AR:
            S = b * b / ar
            c = b / ar
            for cl in CL:
                v = stall(S, cl)
                rows.append({"span_x": k, "span_m": b, "AR": ar, "S_m2": S, "chord_m": c,
                             "WL_N_m2": W / S, "CL": cl, "V_stall": v, "Re": v * c / NU_AIR})
    return rows


def main():
    rows = grid()
    print(f"W = {W*1e3:.3f} mN\n")
    for cl in CL:
        print(f"== CL_max = {cl}:  V_stall (m/s) [Re]   rows span x L, cols AR")
        print("span  " + "".join(f"{'AR'+str(a):>15}" for a in AR))
        for k in SPAN_X:
            cells = [r for r in rows if r["span_x"] == k and r["CL"] == cl]
            print(f"{k}xL  " + "".join(f"{r['V_stall']:7.2f} [{r['Re']:5.0f}]" for r in cells))
        print()
    vmin = min(r["V_stall"] for r in rows)
    best = min(rows, key=lambda r: r["V_stall"])
    print("best cell:", {k: round(v, 5) for k, v in best.items()})
    print("\nratio measured/required in the best cell, and across the grid:")
    vmax = max(r["V_stall"] for r in rows)
    for name, v in SPEEDS.items():
        print(f"  {name:55s} v={v:.3f}  best-cell ratio={v/vmin:.3f}  worst-cell ratio={v/vmax:.3f}"
              f"  KE shortfall (best cell) = x{(vmin/v)**2:.1f}")
    # Ratio table for the measured adult Ucrit (the best-grounded adult number)
    vu = SPEEDS["adult_Ucrit_Plaut2000_wildtype"]
    for cl in CL:
        print(f"\n== ratio  0.56 m/s / V_stall,  CL_max = {cl}")
        print("span  " + "".join(f"{'AR'+str(a):>7}" for a in AR))
        for k in SPAN_X:
            cells = [r for r in rows if r["span_x"] == k and r["CL"] == cl]
            print(f"{k}xL  " + "".join(f"{vu/r['V_stall']:7.3f}" for r in cells))
    # Ballistic: exit speed v -> apex height; and what V_stall needs in specific energy.
    print("\nspecific kinetic energy V^2/2 (J/kg body):")
    for v in [0.15, 0.56, 1.52, vmin, 4.0, 10.0, 16.0, 20.0]:
        print(f"  V={v:6.2f} m/s  -> {v*v/2:8.3f} J/kg ; vertical ballistic apex {v*v/(2*G)*100:7.2f} cm")
    # Stride needed to swim at V_stall by tail beating: V = s * L * f
    print("\ntail-beat frequency needed to reach V by stride V = s*L*f (s = stride length in BL, ASSUMED):")
    for v in [vmin, 4.0]:
        for s in [0.5, 0.7, 1.0]:
            print(f"  V={v:.2f}  s={s}  f={v/(s*L):6.1f} Hz")
    # Hover (actuator-disk) induced power, ideal, for flapping from rest.
    print("\nideal actuator-disk induced power to support W at zero airspeed, per kg body:")
    for k in SPAN_X:
        A = math.pi * (k * L / 2) ** 2
        P = math.sqrt(W ** 3 / (2 * RHO_AIR * A))
        print(f"  span {k}xL={k*L:.2f} m  disk {A*1e4:6.1f} cm2  P_ideal={P*1e3:6.3f} mW = {P/M:5.2f} W/kg")
    # Fish 1990 wing-loading fits extrapolated to 0.4 g (outside the 0.003-0.53 kg measured range).
    tab = json.loads(pathlib.Path("data/fish-controls/fish1990_tables.json").read_text())
    print("\nFish 1990 Table II WL = a M^b EXTRAPOLATED to 0.4 g (measured range 0.003-0.53 kg):")
    for g in tab["table_II"]:
        wl = g["a"] * M ** g["b"]
        print(f"  {g['genus']:15s} WL={wl:6.2f} N/m2  S={W/wl*1e4:6.2f} cm2  "
              + "  ".join(f"V(CL={cl})={math.sqrt(2*wl/(RHO_AIR*cl)):.2f}" for cl in CL))
    wl = 11.7  # Fish 1990 text: smallest measured WL, a 0.001 kg Hirundichthys
    print(f"  smallest measured WL 11.7 N/m2 -> " + "  ".join(f"V(CL={cl})={math.sqrt(2*wl/(RHO_AIR*cl)):.2f}" for cl in CL))

    # Wing-mass sensitivity (ASSUMED areal densities; no measured fin areal density was retrieved).
    # m_total = M + sigma*S ; V = sqrt(2 g m_total / (rho S CL)); floor as S -> inf is sqrt(2 g sigma /(rho CL)).
    print("\nwing-mass sensitivity, best geometry (6xL span, AR3, S=192 cm2); sigma ASSUMED:")
    S = (6 * L) ** 2 / 3
    for sig_mg_cm2 in [0.5, 1, 2, 3, 5, 10]:
        sig = sig_mg_cm2 * 1e-6 / 1e-4   # kg/m^2
        mt = M + sig * S
        print(f"  sigma={sig_mg_cm2:4.1f} mg/cm2  wing mass={sig*S*1e3:6.3f} g  total={mt*1e3:6.3f} g  "
              + "  ".join(f"V(CL={cl})={math.sqrt(2*G*mt/(RHO_AIR*S*cl)):.2f}" for cl in CL)
              + f"   floor(CL=1.2)={math.sqrt(2*G*sig/(RHO_AIR*1.2)):.2f}")
    # Fish 1990 Table I span and length fits extrapolated to 0.4 g: what span/L does a flying fish have?
    t1 = {(r["genus"], r["dimension"]): r for r in tab["table_I"]}
    print("\nFish 1990 Table I span/length EXTRAPOLATED to 0.4 g:")
    for g in sorted({k[0] for k in t1}):
        if (g, "Wing span") in t1 and (g, "Length") in t1:
            sp = t1[(g, "Wing span")]["a"] * M ** t1[(g, "Wing span")]["b"]
            ln = t1[(g, "Length")]["a"] * M ** t1[(g, "Length")]["b"]
            print(f"  {g:15s} span={sp*100:5.2f} cm  SL={ln*100:5.2f} cm  span/SL={sp/ln:4.2f}")
    # Sanity check of the model on real flying fish: Cypselurus WL fit at in-range masses.
    print("\nsanity check, Cypselurus WL fit (in range) -> V_stall; compare taxi 10 -> 16-20 m/s (Fish 1990 p.397, relayed):")
    cy = [g for g in tab["table_II"] if g["genus"] == "Cypselurus"][0]
    for m in [0.01, 0.05, 0.1, 0.2, 0.4]:
        wl = cy["a"] * m ** cy["b"]
        print(f"  M={m:5.2f} kg WL={wl:6.1f} N/m2  " + "  ".join(f"V(CL={cl})={math.sqrt(2*wl/(RHO_AIR*cl)):5.2f}" for cl in CL))
    # What a stall-speed exit buys: ballistic apex and glide from it at ASSUMED L/D.
    print("\nexit at speed v, angle th: apex h = (v sin th)^2/2g ; glide from apex at L/D (ASSUMED 2-5):")
    for v in [0.56, 1.52]:
        for th in [30, 45, 60]:
            h = (v * math.sin(math.radians(th))) ** 2 / (2 * G)
            print(f"  v={v:.2f} th={th}  apex={h*100:5.2f} cm  glide L/D=2: {2*h*100:5.1f} cm  L/D=5: {5*h*100:5.1f} cm")


if __name__ == "__main__":
    main()
