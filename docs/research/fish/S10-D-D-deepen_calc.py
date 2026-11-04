"""S10-D-D-D: attack S10-D-D's comparator, the muscle power density 134.4 W/kg.
Every printed number is a CALCULATION (Rankine-Froude hover, S10/S10-D/S10-D-D model;
forward flight as in challenge_77_calc.py). Measured inputs are labelled MEASURED with source."""
import math
g, rho, k, m = 9.81, 1.2, 1.2, 0.4e-3
W = m * g
# MEASURED, Mead et al. 2020 Biophys J 119:806 (PMC7451861, full-text): larval (5 dpf) zebrafish
# myotome, 28 C, 8% sinusoidal strain, one twitch per cycle, n=5.
WORK_40 = 2.63            # J/kg muscle per cycle at 40 Hz
P_80, P_100 = 134.4, 122.9  # W/kg at 80 and 100 Hz
SIGMA0 = 76e3             # Pa, max isometric stress
TW_TET = 0.91             # twitch/tetanus ratio
STRAIN = 0.08             # peak-to-peak strain used in the work loops
RHO_M = 1060.0            # kg/m^3, the density the authors used
W_80 = P_80 / 80

def p_hover(R, M, phi=math.pi):
    """phi = total stroke angle of the pair's swept sector; S10 used the full disc (phi = pi)."""
    A = phi * R**2
    return M * k * math.sqrt(W**3 / (2 * rho * A))

def design_freq(R, phi=2 * math.pi / 3, CL=1.5, AR=6):
    S = (2 * R)**2 / AR
    U = math.sqrt(2 * W / (rho * CL * S))
    return U / (2 * phi * 0.55 * R)       # S10 sec 3c

def p_fwd(R, CDp, Sb=2.2e-5, CDb=0.4, CLmax=1.5):
    S = (2 * R)**2 / 6; A = math.pi * R**2
    Vmin = math.sqrt(2 * W / (rho * CLmax * S)); best = None
    for i in range(1, 4000):
        V = i * 0.0025
        if V < Vmin: continue
        P = k * W**2 / (2 * rho * A * V) + 0.5 * rho * V**3 * (Sb * CDb + S * CDp)
        if best is None or P < best: best = P
    return best

def muscle_power(freq):
    """Three readings of measured Mead 2020 data at a design frequency (CALCULATIONS)."""
    if freq >= 80:
        Pm = P_80 + (P_100 - P_80) * (min(freq, 100) - 80) / 20   # linear interpolation
        return dict(plateau=Pm, linear=Pm, bound=Pm)
    if freq >= 40:
        Wc = WORK_40 + (W_80 - WORK_40) * (freq - 40) / 40   # inside the measured range
        return dict(plateau=Wc * freq, linear=Wc * freq, bound=Wc * freq)
    slope = (W_80 - WORK_40) / 40
    return dict(plateau=WORK_40 * freq,                       # work/cycle stops rising below 40 Hz
                linear=(WORK_40 - slope * (40 - freq)) * freq,  # 40-80 Hz trend continued
                bound=SIGMA0 * STRAIN / RHO_M * freq)           # rectangle: shortening force <= isometric

print("== 1. Design frequency per geometry (S10 sec 3c method, phi=120 deg, CL=1.5, AR=6)")
for R in (0.04, 0.02):
    fr = design_freq(R)
    print(f"  R={R*100:.0f} cm: {fr:.1f} Hz -> muscle power " +
          ", ".join(f"{kk}={v:.0f}" for kk, v in muscle_power(fr).items()) + " W/kg")
print(f"  work/cycle measured 40 Hz {WORK_40}; implied 80 Hz {W_80:.2f}; 100 Hz {P_100/100:.2f} J/kg")
print(f"  rectangle bound at 8% strain: tetanic {SIGMA0*STRAIN/RHO_M:.2f} J/kg, twitch {TW_TET*SIGMA0*STRAIN/RHO_M:.2f} J/kg")
print(f"  loop fill (measured/rectangle): 40 Hz {WORK_40/(SIGMA0*STRAIN/RHO_M):.2f}, 80 Hz {W_80/(SIGMA0*STRAIN/RHO_M):.2f}")

print("\n== 2. Sensitivity of S10-D-D's closest-to-flip cases to the comparator (x0.5 / x2)")
fs = {"S10-D 0.0138": 0.0138, "central 0.0164": 0.0164, "upper 0.0276": 0.0276}
for lab, f in fs.items():
    r = p_hover(0.04, 1.5) / (m * f)
    print(f"  hover R4 M1.5 f={lab}: req {r:.0f}; margin vs 134.4 x{r/134.4:.2f}, "
          f"vs 67.2 (x0.5) x{r/67.2:.2f}, vs 268.8 (x2) x{r/268.8:.2f}")
for CDp in (0.05, 0.1, 0.2):
    r = p_fwd(0.04, CDp) / (m * 0.0276)
    print(f"  fwd R4 CDpro={CDp} f=upper: req {r:.0f} W/kg; vs 134.4 x{r/134.4:.2f}; "
          f"ratio to hover(M1.5) {p_fwd(0.04, CDp)/p_hover(0.04, 1.5):.2f}")

print("\n== 3. Recompute S10-D-D grid with frequency-matched comparator")
for R, M in ((0.04, 1.5), (0.04, 2.0), (0.02, 1.5), (0.02, 2.0)):
    mp = muscle_power(design_freq(R))
    for lab, f in fs.items():
        r = p_hover(R, M) / (m * f)
        print(f"  hover R={R*100:.0f} M={M} f={lab}: req {r:5.0f} | x{r/134.4:.2f} vs 134.4 | "
              + " ".join(f"x{r/v:.2f} vs {kk} {v:.0f}" for kk, v in mp.items()))
mp4 = muscle_power(design_freq(0.04))
for CDp in (0.05, 0.1, 0.2):
    for lab, f in fs.items():
        r = p_fwd(0.04, CDp) / (m * f)
        print(f"  fwd R=4 CDpro={CDp} f={lab}: req {r:5.0f} | x{r/134.4:.2f} vs 134.4 | "
              + " ".join(f"x{r/v:.2f} vs {kk} {v:.0f}" for kk, v in mp4.items()))
mp2 = muscle_power(design_freq(0.02))
for CDp in (0.05, 0.2):
    r = p_fwd(0.02, CDp) / (m * 0.0276)
    print(f"  fwd R=2 CDpro={CDp} f=upper: req {r:.0f} vs {mp2['plateau']:.0f} -> x{r/mp2['plateau']:.2f}")

print("\n== 4. Design escape: shrink stroke angle to raise frequency (R=4 cm, M=1.5, f=0.0276)")
for deg in (180, 120, 90, 60, 45, 33):
    phi = math.radians(deg)
    fr = design_freq(0.04, phi=phi)
    r = p_hover(0.04, 1.5, phi=phi) / (m * 0.0276)
    mp = muscle_power(fr)
    print(f"  phi={deg:3d} deg: {fr:5.1f} Hz, req {r:4.0f} W/kg (swept sector), "
          f"muscle plateau {mp['plateau']:.0f} / bound {mp['bound']:.0f} -> x{r/mp['plateau']:.2f} / x{r/mp['bound']:.2f}")
for fill in (0.46, 0.6, 0.7, 1.0):
    for eps in (0.08, 0.12, 0.16):
        Wc = fill * SIGMA0 * eps / RHO_M
        print(f"  fill {fill:.2f}, strain {eps:.2f}: {Wc:.2f} J/kg -> {Wc*design_freq(0.04):.0f} W/kg at {design_freq(0.04):.1f} Hz")
need = p_fwd(0.04, 0.05) / (m * 0.0276)
print(f"  flip threshold for the most generous corner: {need:.0f} W/kg = {need/design_freq(0.04):.2f} J/kg/cycle "
      f"= fill {need/design_freq(0.04)/(SIGMA0*STRAIN/RHO_M):.2f} at 8% strain")
print(f"  note: S10's full-disc area at phi=120 deg understates hover power by x{math.sqrt(math.pi/(2*math.pi/3)):.2f}")
