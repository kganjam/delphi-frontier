"""Challenge 175: independent recomputation. Every output is a CALCULATION, not an observation.
Inputs (read-level): EI_fin 1.5e-9..4e-9 N m^2, 16-18 rays, D 0.1-0.2 mm (Puri 2018, full-text);
t 11-16.5 um (hox13 PLoS Genet 2026 Fig 7E as read by the S9-D author; text confirms 'thickness of the bone', full-text).
Second moments are computed by numerical integration over a sampled cross-section, NOT by the S9-D closed forms."""
import numpy as np

EI_lo, EI_hi = 1.5e-9 / 18, 4e-9 / 16

def I_numeric(mask_fn, D, n=1500):
    # sample a square box of side D centred on the ray axis; y = out-of-fin-plane coordinate
    xs = np.linspace(-D / 2, D / 2, n); dA = (xs[1] - xs[0]) ** 2
    X, Y = np.meshgrid(xs, xs)
    m = mask_fn(X, Y)
    return m, X, Y, dA

def I_about_own_centroids(D, t, half_angle_deg, coupled):
    """Two hemitrichs = annular sectors of outer radius D/2, wall t, centred on +y and -y
    (each crescent bows away from the fin mid-plane). half_angle measured from the y axis."""
    R_o, R_i = D / 2, D / 2 - t
    a = np.radians(half_angle_deg)
    m, X, Y, dA = I_numeric(lambda X, Y: (np.hypot(X, Y) <= R_o) & (np.hypot(X, Y) >= R_i), D)
    ang = np.arctan2(np.abs(X), np.abs(Y))     # angle from the y axis
    m = m & (ang <= a)
    if coupled:   # bend about the fin mid-plane (y=0) as one section
        return np.sum(Y[m] ** 2) * dA
    tot = 0.0
    for s in (Y > 0, Y < 0):                    # each half about its own centroid
        mm = m & s
        yb = np.sum(Y[mm]) / np.sum(mm)
        tot += np.sum((Y[mm] - yb) ** 2) * dA
    return tot

def flat(D, t): return 2 * D * t ** 3 / 12
def rod(D): return np.pi * D ** 4 / 64

print(f"per-ray EI (calc): {EI_lo:.3e} .. {EI_hi:.3e} N m^2")
D, t = 150e-6, 15e-6
print(f"solid rod  I={rod(D):.3e}  E={EI_lo/rod(D)/1e6:.2f}..{EI_hi/rod(D)/1e6:.2f} MPa")
Ic = I_about_own_centroids(D, t, 90, True)
print(f"bonded tube (numeric) I={Ic:.3e}  E={EI_lo/Ic/1e6:.2f}..{EI_hi/Ic/1e6:.2f} MPa")
print(f"flat plates I={flat(D,t):.3e}  E={EI_lo/flat(D,t)/1e9:.2f}..{EI_hi/flat(D,t)/1e9:.2f} GPa")
for a in (90, 60, 45, 30):
    I = I_about_own_centroids(D, t, a, False)
    print(f"uncoupled crescent half-angle {a:2d} deg  I={I:.3e}  E={EI_lo/I/1e6:8.1f}..{EI_hi/I/1e6:8.1f} MPa")

print("\nEnvelope, flat plates, D 100-200 um, t 11-16.5 um:")
print(f"  min E = {EI_lo/flat(200e-6,16.5e-6)/1e9:.2f} GPa, max E = {EI_hi/flat(100e-6,11e-6)/1e9:.2f} GPa")
print("Envelope, semicircular crescents (90 deg), same D,t ranges:")
Imax = I_about_own_centroids(200e-6, 16.5e-6, 90, False); Imin = I_about_own_centroids(100e-6, 11e-6, 90, False)
print(f"  min E = {EI_lo/Imax/1e6:.1f} MPa, max E = {EI_hi/Imin/1e6:.1f} MPa")

print("\nThickness exponent: d ln E / d ln t between t=11 and 16.5 um, D=150 um")
for label, f in [("flat", lambda tt: flat(D, tt))] + [(f"crescent {a}deg", (lambda a: lambda tt: I_about_own_centroids(D, tt, a, False))(a)) for a in (90, 60, 45, 30)]:
    k = -np.log(f(16.5e-6) / f(11e-6)) / np.log(16.5 / 11)
    print(f"  {label:15s} E ~ t^{k:+.2f}")

# Order-of-magnitude composite-action check (Newmark partial interaction), ASSUMED parameters, not data.
print("\nNewmark partial-interaction parameter alpha*L (assumed E_bone, G_core; L = 10 mm):")
E_b = 10e9; b = D; d = D - t; EA = E_b * b * t; EI0 = E_b * b * t ** 3 / 12; h_c = D - 2 * t
for G in (1e6, 1e5, 1e4, 1e3):
    k = G * b / h_c
    alpha = np.sqrt(k * (2 / EA + d ** 2 / (2 * EI0)))
    print(f"  G_core={G:8.0e} Pa  alpha*L = {alpha*10e-3:7.2f}  (>>1: near-full coupling; <<1: uncoupled)")
