"""S29 -- can launch energy be engineered by latch-mediated spring actuation (LaMSA)?

Every number in docs/research/fish/S29-organism.md is printed by this script.
Inputs are labelled MEASURED (with source), PROJECT (inherited from S28) or ASSUMED.
Run: python3 docs/research/fish/S29_launch_energy.py
"""
import math

# ---------------------------------------------------------------- inputs
V_EXIT = 4.37          # PROJECT: required water-exit speed (S28, case C, derived at m = 0.25 g)
V_BURST = 1.38         # MEASURED: max adult zebrafish burst, Miln et al. 2021 (via S28)
M = 0.40e-3            # brief: 0.4 g body (S28 used 0.25 g; J/kg results are mass-independent)
RHO_W = 1000.0         # water density
RHO_FISH = 1050.0      # ASSUMED body density (near-neutral teleost)
A_FRONT = 24e-6        # PROJECT: frontal area 24 mm^2 (S28)
CD_BODY = (0.1, 0.2, 0.3)  # ASSUMED body drag coefficient in water on frontal area
ETA_H = 0.37           # MEASURED: hydromechanical efficiency, pike C-start (Frith & Blake 1995), best case
ETA_SPRING = 0.93      # MEASURED: tendon returns ~93% (Ker 1981: ~7% dissipated)
W_MUSCLE = (32.0, 53.0, 81.0)  # MEASURED: J per kg muscle stored in series tendon, Cuban tree frog
                               # (Mendoza & Azizi 2021; range 32-81, mean 53)
F_MUSCLE_TOTAL = 0.60  # SECONDARY: zebrafish skeletal muscle ~60% of adult body mass (review, primary not read)
F_ONE_SIDE = 0.30      # ASSUMED: one side of the axial musculature (half of 0.60) drives one stroke
F_JUMPER = (0.10, 0.20)  # SECONDARY: jumping-muscle fraction of body mass in Sutton et al. 2019 data set

line = "-" * 78


def h(t):
    print("\n" + line + "\n" + t + "\n" + line)


# ---------------------------------------------------------------- 1. required energy
h("1. Kinetic energy at water exit")
for m, v, tag in [(M, V_EXIT, "0.40 g @ 4.37"), (0.25e-3, V_EXIT, "0.25 g @ 4.37 (S28 mass)"),
                  (M, 4.37 * math.sqrt(0.40 / 0.25), "0.40 g @ 5.53 (S28 case-C fin re-scaled to 0.4 g)"),
                  (M, V_BURST, "0.40 g @ 1.38 measured burst")]:
    ke = 0.5 * m * v * v
    print(f"{tag:52s} KE = 0.5*{m*1e3:.2f}e-3*{v:.2f}^2 = {ke*1e3:.3f} mJ = {ke/m:.2f} J/kg")
ke = 0.5 * M * V_EXIT ** 2
ke_sp = ke / M
print(f"energy ratio 4.37/1.38 squared = {(V_EXIT/V_BURST)**2:.2f}x")

# ---------------------------------------------------------------- 2. distance & time
h("2. Delivery distance, time, acceleration, mean power (constant acceleration, in water)")
print(f"{'s (cm)':>7} {'t (ms)':>7} {'a (m/s2)':>9} {'a (g)':>6} {'P_mean body W/kg':>17} {'P_peak W/kg':>12}")
for s in (0.005, 0.0109, 0.015, 0.030):
    t = 2 * s / V_EXIT
    a = V_EXIT ** 2 / (2 * s)
    pm = ke_sp / t
    print(f"{s*100:7.2f} {t*1e3:7.2f} {a:9.0f} {a/9.81:6.0f} {pm:17.0f} {2*pm:12.0f}")
print("(5 ms release -> s = 4.37*0.005/2 = 1.09 cm; peak power = 2x mean for constant force)")

# drag work during the stroke and coast-down below the surface
h("2b. Drag work during the stroke  W_d = 0.5*rho*Cd*A*v_f^2*s/2  (v^2 linear in x)")
for cd in CD_BODY:
    for s in (0.0109, 0.030):
        wd = 0.5 * RHO_W * cd * A_FRONT * V_EXIT ** 2 * s / 2
        print(f"Cd {cd:.1f} s {s*100:.2f} cm: W_d = {wd*1e3:.3f} mJ = {wd/ke*100:.1f}% of KE")
for cd in CD_BODY:
    D = 0.5 * RHO_W * cd * A_FRONT * V_EXIT ** 2
    a = D / M
    v_after_1cm = math.sqrt(V_EXIT ** 2 - 2 * a * 0.01)
    print(f"Cd {cd:.1f}: drag at 4.37 m/s = {D*1e3:.1f} mN = {D/(M*9.81):.1f} body weights; "
          f"decel {a:.0f} m/s2; coast 1 cm -> {v_after_1cm:.2f} m/s")

# central case
CD_C, S_C = 0.2, 0.0109
wd_c = 0.5 * RHO_W * CD_C * A_FRONT * V_EXIT ** 2 * S_C / 2
ideal = ke                       # floor: no drag, no wake loss
body_work = ke + wd_c            # work actually delivered to body
spring_out = body_work / ETA_H   # spring output needed with measured best C-start efficiency
stored = spring_out / ETA_SPRING  # energy that must be stored
stored_ideal = ideal / ETA_SPRING

h("3. Energy that must be STORED in the spring")
print(f"floor (eta_h=1, no drag):    {ideal*1e3:.3f} mJ out -> stored {stored_ideal*1e3:.3f} mJ "
      f"= {stored_ideal/M:.2f} J/kg body")
print(f"central (Cd 0.2, s 1.09 cm): body work {body_work*1e3:.3f} mJ; /eta_h {ETA_H} = {spring_out*1e3:.3f} mJ; "
      f"/0.93 = {stored*1e3:.3f} mJ = {stored/M:.2f} J/kg body")

# ---------------------------------------------------------------- 4. spring volume
h("4. Spring volume as a fraction of body volume")
v_body = M / RHO_FISH
print(f"body volume = {M*1e3:.2f} g / {RHO_FISH:.0f} = {v_body*1e9:.0f} mm^3")
materials = [
    # name, energy density J/m^3, basis
    ("tendon, Ker 1981 E=1.65 GPa at 100 MPa (sigma^2/2E)", (100e6) ** 2 / (2 * 1.65e9), "derived from measured E"),
    ("tendon, Ker 1981 E=1.65 GPa at  50 MPa", (50e6) ** 2 / (2 * 1.65e9), "derived from measured E"),
    ("tuna caudal tendon, E=1.2 GPa at 2% strain (0.5 E eps^2)", 0.5 * 1.2e9 * 0.02 ** 2, "measured E and burst strain"),
    ("tuna caudal tendon, E=0.65 GPa at 2% strain", 0.5 * 0.65e9 * 0.02 ** 2, "measured E and burst strain"),
    ("resilin, toughness to FAILURE 4 MJ/m3 (Gosline 2002)", 4e6, "upper bound, not working"),
    ("collagen tendon, toughness to FAILURE 6 MJ/m3 (Gosline 2002)", 6e6, "upper bound, not working"),
]
print(f"{'material':62s} {'u MJ/m3':>8} {'floor mm3':>9} {'%body':>6} {'central mm3':>11} {'%body':>6}")
for name, u, basis in materials:
    v1, v2 = stored_ideal / u, stored / u
    print(f"{name:62s} {u/1e6:8.3f} {v1*1e9:9.2f} {v1/v_body*100:6.2f} {v2*1e9:11.2f} {v2/v_body*100:6.2f}")

# ---------------------------------------------------------------- 5. power amplification
h("5. Power demanded vs. measured LaMSA power densities")
for s in (0.0109, 0.030):
    t = 2 * s / V_EXIT
    wd = 0.5 * RHO_W * CD_C * A_FRONT * V_EXIT ** 2 * s / 2
    out = (ke + wd) / ETA_H
    p_mean = out / t
    for f in (F_ONE_SIDE, F_MUSCLE_TOTAL):
        print(f"s {s*100:.2f} cm, t {t*1e3:.1f} ms: spring output {out*1e3:.2f} mJ, mean {p_mean:.3f} W; "
              f"per kg muscle (f={f:.2f}) mean {p_mean/(f*M):.0f}, peak {2*p_mean/(f*M):.0f} W/kg")
print("reference (measured, per kg muscle): vertebrate in-vitro max 1121; bluegill suction 321; "
      "snipefish 2800 (1090-5500); seahorse 3266-4263; pipefish 5795; froghopper 36000 (74000 best)")
for name, p in [("snipefish mean", 2800), ("seahorse max", 4263), ("pipefish", 5795),
                ("froghopper mean", 36000), ("froghopper best", 74000)]:
    print(f"amplification {name:16s}: {p}/1121 = {p/1121:.1f}x  ;  vs bluegill 321: {p/321:.1f}x")

# ---------------------------------------------------------------- 6. the energy SOURCE
h("6. Muscle work available per single loading stroke (the binding term)")
print("supply per kg BODY = f_muscle * w_muscle * eta_spring * eta_h  (compare to body KE+drag need)")
need_floor = ke / M
need_central = body_work / M
print(f"need at the body: floor {need_floor:.2f} J/kg ; central {need_central:.2f} J/kg")
for f, ftag in [(F_JUMPER[0], "jumper 10%"), (F_JUMPER[1], "jumper 20%"),
                (F_ONE_SIDE, "one-side axial 30%"), (F_MUSCLE_TOTAL, "ALL skeletal muscle 60%")]:
    for w in W_MUSCLE:
        sup = f * w * ETA_SPRING * ETA_H
        sup_ideal = f * w * ETA_SPRING
        print(f"{ftag:24s} w {w:4.0f} J/kg: supply eta_h=1 {sup_ideal:6.2f} (x{sup_ideal/need_floor:4.2f} of floor) | "
              f"eta_h=0.37 {sup:5.2f} J/kg (x{sup/need_central:4.2f} of central need)")

h("6b. Muscle fraction of body mass required to load the spring")
for w in W_MUSCLE:
    f_floor = stored_ideal / (w * M)
    f_cent = stored / (w * M)
    print(f"w {w:4.0f} J/kg muscle: floor f = {f_floor*100:5.1f}% ; central f = {f_cent*100:5.1f}% of body mass")

h("6c. Comparison with what the fish does today (measured burst, same efficiency chain)")
ke_b = 0.5 * M * V_BURST ** 2
print(f"KE at 1.38 m/s = {ke_b*1e3:.3f} mJ = {ke_b/M:.3f} J/kg body; "
      f"implied muscle work at eta_h 0.37 = {ke_b/ETA_H*1e3:.3f} mJ "
      f"= {ke_b/ETA_H/(F_ONE_SIDE*M):.2f} J/kg one-side muscle")
print(f"central requirement / today = {stored/(ke_b/ETA_H):.1f}x")

h("7. Verdict arithmetic")
best = F_ONE_SIDE * W_MUSCLE[1] * ETA_SPRING * ETA_H
print(f"central need {need_central:.2f} J/kg vs one-side axial @53 J/kg supply {best:.2f} J/kg -> short {need_central/best:.2f}x")
best81 = F_ONE_SIDE * W_MUSCLE[2] * ETA_SPRING * ETA_H
print(f"                         vs one-side axial @81 J/kg supply {best81:.2f} J/kg -> short {need_central/best81:.2f}x")
allm = F_MUSCLE_TOTAL * W_MUSCLE[1] * ETA_SPRING * ETA_H
print(f"                         vs ALL muscle @53 J/kg supply {allm:.2f} J/kg -> ratio {allm/need_central:.2f}")
jump = F_JUMPER[1] * W_MUSCLE[1] * ETA_SPRING * ETA_H
print(f"                         vs frog-like 20% @53 J/kg supply {jump:.2f} J/kg -> short {need_central/jump:.2f}x")
