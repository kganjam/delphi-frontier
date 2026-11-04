"""S7-D-D: deepen S7-D by attacking its weakest input (actual bending section of the
element that receives the pectoral-fin root moment).

Part A MEASURES (from published images, my measurement, not an author-reported number)
the wild-type proximal-radial row of an adult zebrafish from Ishizaka et al. 2024,
Sci. Rep., doi:10.1038/s41598-024-74134-9 (PMC11464670), Supplementary Movie S4
(Imaris render, 100 um scale bar) -- requires the Europe PMC supplementary zip:
  curl -L -o supp.zip https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11464670/supplementaryFiles
  python3 -I S7-D-deepen.py path/to/41598_2024_74134_MOESM4_ESM.mp4
Part B CALCULATES everything else. Every number printed by part B is a calculation.
"""
import glob, math, os, subprocess, sys, tempfile

# ---------------- Part A: image measurement (optional) ----------------
def measure(movie):
    import numpy as np
    from PIL import Image
    d = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", movie, "-vf", "fps=2", f"{d}/f%03d.png"], check=True)
    frames = sorted(glob.glob(f"{d}/f*.png"))
    # scale bar: longest bright horizontal run in bottom 15% of the first frame
    a = np.array(Image.open(frames[0]).convert("L")).astype(int)
    H = a.shape[0]; bar = 0
    for y in range(int(H * .85), H):
        cur = 0
        for v in list(a[y] > 200) + [False]:
            if v: cur += 1
            else: bar = max(bar, cur); cur = 0
    um_px = 100.0 / bar
    print(f"scale bar {bar} px = 100 um -> {um_px:.3f} um/px")
    rows = []
    for f in frames:
        im = np.array(Image.open(f).convert("RGB")).astype(int)
        r, g, b = im[..., 0], im[..., 1], im[..., 2]
        grey = (r > 60) & (abs(r - g) < 40) & (abs(r - b) < 45)   # proximal radials are grey
        grey[:150, :500] = False; grey[1000:, :] = False          # mask title text and scale bar
        xs = np.where(grey.any(0))[0]
        if len(xs) < 50: continue
        x0, x1 = xs.min(), xs.max(); L = x1 - x0
        mid = [grey[:, x].sum() * um_px for x in range(int(x0 + .3 * L), int(x0 + .8 * L), 10)]
        dist = [grey[:, x].sum() * um_px for x in range(int(x0 + .55 * L), int(x0 + .9 * L), 10)]
        rows.append((os.path.basename(f), L * um_px, float(np.median(mid)), float(np.median(dist))))
    long_axis = [r for r in rows if r[1] > 900]          # frames showing the full ~0.95 mm length
    face = max(r[2] for r in long_axis); edge = min(r[3] for r in long_axis)
    print(f"long-axis span ~{max(r[1] for r in rows):.0f} um")
    print(f"face-on summed radial width (max over frames of median column grey length): {face:.0f} um")
    print(f"edge-on projected thickness, distal half (min over frames): {edge:.0f} um  [upper bound on plate thickness]")

if len(sys.argv) > 1:
    measure(sys.argv[1])

# ---------------- Part B: calculations ----------------
g, rho = 9.81, 1.2
m = 0.4e-3; W = m * g
def M_root(V, n, CL=0.78, AR=9, hw=2.5e-3):
    S = 2 * W / (rho * V * V * CL); b = math.sqrt(AR * S); s = b / 2 - hw
    return n * W / 2 * 4 / (3 * math.pi) * s
cases = {"V3n3 (worst)": (3, 3), "V3n1": (3, 1), "V5n1": (5, 1), "V5n3": (5, 3)}
sig = 62.6e6   # herring IB yield, large fish (Fiedler 2019) -- carried from S7-D
sig_lo = 43.4e6
def d_eq(Z): return (32 * Z / math.pi) ** (1 / 3)

# measured inputs (Part A, rounded; brackets reflect frame choice / tilt)
SW = (0.36e-3, 0.40e-3, 0.44e-3)   # summed face-on width of radial row, m
H = (0.055e-3, 0.08e-3, 0.10e-3)   # plate thickness (edge-on projection, upper-bound-ish), m
Zs = {"low": SW[0] * H[0] ** 2 / 6, "mid": SW[1] * H[1] ** 2 / 6, "high": SW[2] * H[2] ** 2 / 6}
print("\nB1. Radial-row section modulus (plates side by side in fin plane, out-of-plane bending, solid, foramina ignored)")
for k, Z in Zs.items():
    print(f"  {k}: Z = {Z*1e9:.2e} mm^3, solid-rod-equivalent d = {d_eq(Z)*1e3:.3f} mm")

print("\nB2. Capacity/demand as a LOCKED cantilever (ratio <1 = yields), sigma_y = 62.6 MPa, no safety factor")
for name, (V, n) in cases.items():
    Mr = M_root(V, n); Zreq = Mr / sig
    print(f"  {name}: M = {Mr:.2e} N m, d_req = {d_eq(Zreq)*1e3:.3f} mm, ratios",
          {k: round(Z / Zreq, 2) for k, Z in Zs.items()},
          f"| stress/yield (mid) = {Zreq/Zs['mid']:.1f}")

print("\nB3. Sensitivity of the verdict to each input x0.5 / x2 (worst case, mid geometry): capacity/demand")
base = Zs["mid"] / (M_root(3, 3) / sig)
print(f"  base {base:.2f}")
print(f"  thickness h x0.5 / x2: {base*0.25:.2f} / {base*4:.2f}")
print(f"  summed width x0.5 / x2: {base*0.5:.2f} / {base*2:.2f}")
print(f"  sigma_y x0.5 / x2: {base*0.5:.2f} / {base*2:.2f}")
print(f"  load factor n x0.5 / x2: {base*2:.2f} / {base*0.5:.2f}")
for f in (0.5, 2):
    print(f"  speed V x{f}: {Zs['mid']/(M_root(3*f,3)/sig):.2f}")
print("  linear size of fish (isometric, Z ~ L^3) x1.25 / x1.5 / x1.6:",
      [round(base * k ** 3, 2) for k in (1.25, 1.5, 1.6)])
need = (1 / base) ** (1 / 3)
print(f"  isometric scale-up needed to reach ratio 1 (mid): x{need:.2f} in length -> scanned fish would have to be <= {40/need:.0f} mm if design fish is 40 mm")
needSF = (1.5 / base) ** (1 / 3)
print(f"  with SF 1.5: x{needSF:.2f} -> scanned fish <= {40/needSF:.0f} mm")
needhi = (1 / (Zs['high'] / (M_root(3, 3) / sig))) ** (1 / 3)
print(f"  most generous geometry: x{needhi:.2f} -> scanned fish <= {40/needhi:.0f} mm")

print("\nB4. Hinge (synovial) load path: radial row in compression from the muscle couple F = M/r")
A = SW[1] * H[1]
for r in (1.0e-3, 0.5e-3, 0.15e-3):
    F = M_root(3, 3) / r
    print(f"  r = {r*1e3:.2f} mm: F = {F*1e3:.0f} mN ({F/W:.0f} W), compressive stress on radial row (mid area {A*1e6:.3f} mm^2) = {F/A/1e6:.1f} MPa, adductor PCSA at 200 kPa = {F/200e3*1e6:.2f} mm^2")
