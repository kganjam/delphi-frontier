"""S2 low-Reynolds aerodynamics: every COMPUTED number in S2-low-reynolds-aero.md.

Nothing here is a measurement. Inputs marked ASSUMED are design assumptions, not data.
Run:  python3 docs/research/fish/S2_calcs.py
"""
import math

NU = 1.5e-5      # m^2/s, air kinematic viscosity (given in the task)
RHO = 1.2        # kg/m^3, air density (ASSUMED, sea level ~20 C)
G = 9.81

# ---------------------------------------------------------------- 1. Re grid
def re_grid():
    cs = [0.005, 0.01, 0.015, 0.02, 0.03]
    vs = [0.5, 1, 2, 3, 5, 8]
    print("| chord \\ U | " + " | ".join(f"{v} m/s" for v in vs) + " |")
    print("|---|" + "---|" * len(vs))
    for c in cs:
        print(f"| {c*1000:.0f} mm | " + " | ".join(f"{v*c/NU:,.0f}" for v in vs) + " |")
    # control: a case whose answer is known by hand: 0.01 m * 1.5 m/s / 1.5e-5 = 1000
    assert abs(0.01 * 1.5 / NU - 1000) < 1e-9

# ---------------------------------------------------------------- 2. glide
M = 0.4e-3       # kg, ASSUMED adult zebrafish mass (retrieved range ~0.25-0.55 g)
BL = 0.04        # m, body length used for "body lengths" (task's 4 cm)

def glide(S, CL, LD, h0=0.5, vx0=0.0, vz0=0.0, dt=1e-5):
    """Point mass, fixed angle of attack (fixed CL and L/D), quasi-steady, still air,
    no ground effect, no body/fin added mass. Returns horizontal range (m)."""
    CD = CL / LD
    x, z, vx, vz = 0.0, h0, vx0, vz0
    while z > 0:
        v = math.hypot(vx, vz)
        if v < 1e-12:
            vz -= G * dt; z += vz * dt; continue
        q = 0.5 * RHO * v * v * S
        ux, uz = vx / v, vz / v
        ax = (-q * CD * ux - q * CL * uz) / M
        az = (-q * CD * uz + q * CL * ux) / M - G
        vx += ax * dt; vz += az * dt; x += vx * dt; z += vz * dt
    return x

def v_eq(S, CL, LD):
    gam = math.atan(1 / LD)
    return math.sqrt(2 * M * G * math.cos(gam) / (RHO * S * CL)), gam

def glide_table():
    print("\nEquilibrium glide speed and the drop needed just to reach it from rest")
    print("| S (cm^2) | CL | V_eq (m/s) | Re at 15 mm chord | v^2/2g (m) |")
    print("|---|---|---|---|---|")
    for S in (4.5e-4, 9e-4, 18e-4):
        for CL in (0.6, 0.9):
            V, _ = v_eq(S, CL, 1e9)
            print(f"| {S*1e4:.1f} | {CL} | {V:.2f} | {V*0.015/NU:,.0f} | {V*V/2/G:.2f} |")

    print("\nRange from h0 = 0.5 m, CL = 0.6 fixed")
    print("| S (cm^2) | L/D | launch | range (m) | range (body lengths, 4 cm) | ideal h0*L/D (m) |")
    print("|---|---|---|---|---|---|")
    for S in (4.5e-4, 9e-4, 18e-4):
        for LD in (2, 4, 6):
            for lab, vx0 in (("from rest", 0.0), ("2 m/s horizontal", 2.0)):
                x = glide(S, 0.6, LD, vx0=vx0)
                print(f"| {S*1e4:.1f} | {LD} | {lab} | {x:.2f} | {x/BL:.0f} | {0.5*LD:.1f} |")
            V, gam = v_eq(S, 0.6, LD)
            x = glide(S, 0.6, LD, vx0=V*math.cos(gam), vz0=-V*math.sin(gam))
            print(f"| {S*1e4:.1f} | {LD} | on glide path at V_eq={V:.1f} m/s | {x:.2f} | {x/BL:.0f} | {0.5*LD:.1f} |")

    # CONTROLS (known answers, both directions)
    # (a) no aerodynamic force -> ballistic range v0*sqrt(2h/g)
    xb = glide(9e-4, 1e-12, 1.0, vx0=2.0)
    assert abs(xb - 2.0 * math.sqrt(2 * 0.5 / G)) < 1e-3, xb
    # (b) start on the equilibrium glide path -> range must equal h0*L/D exactly
    for LD in (2, 4, 6):
        V, gam = v_eq(9e-4, 0.6, LD)
        x = glide(9e-4, 0.6, LD, vx0=V*math.cos(gam), vz0=-V*math.sin(gam))
        assert abs(x - 0.5 * LD) < 5e-3, (LD, x)
    # (c) must-fail: a wrong-sign lift would make range < ballistic; check it is not
    assert glide(18e-4, 0.6, 6, vx0=2.0) > xb
    print("\ncontrols passed: ballistic limit, equilibrium-glide-path = h0*L/D, lift extends range")

# ---------------------------------------------------------------- 3. hover frequency
def hover_freq():
    print("\nFlapping frequency needed to HOVER (weight support only, quasi-steady scaling)")
    print("W = 0.5 rho U^2 S CL, U = 2*Phi*f*r2, r2 = 0.55 R")
    print("| R one wing (m) | S both wings (cm^2) | Phi (deg) | CL | U needed (m/s) | f (Hz) | Re = U*c/nu, c=15 mm |")
    print("|---|---|---|---|---|---|---|")
    W = M * G
    for R, S in ((0.03, 9e-4), (0.04, 12e-4)):
        for Phi_deg in (90, 120):
            for CL in (1.0, 1.75):
                U = math.sqrt(2 * W / (RHO * S * CL))
                f = U / (2 * math.radians(Phi_deg) * 0.55 * R)
                print(f"| {R} | {S*1e4:.0f} | {Phi_deg} | {CL} | {U:.2f} | {f:.0f} | {U*0.015/NU:,.0f} |")

if __name__ == "__main__":
    re_grid(); glide_table(); hover_freq()
