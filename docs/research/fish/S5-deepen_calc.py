"""S5-D sensitivity calculations. Every number this script prints is CALCULATED.

Inputs and their status (see S5-deepen.md for sources and read-levels):
  p0   wild-type zebrafish pectoral length / SL. Figure-read plus inference, carried over from S22-D-D
       (Daane et al. 2018 Sci Rep Fig 1A): 0.208, bracket 0.173-0.260.
  f    pectoral length fold-change for a dominant bioelectric long-fin allele. kcnk5b alf/+ = 1.74,
       figure-read, D18 Fig 1A. Caudal alf/+ = 2.05 (P14 Fig 1E eye-read) is used only as an upper proxy.
  A0   wild-type zebrafish pectoral-fin aspect ratio, span^2/area (Fish 1990 definition). UNKNOWN.
       Swept here as an ASSUMPTION.
  alpha  area exponent: area scales as f**alpha. alpha=2 means isometric dilation (shape preserved),
         alpha=1 means rays lengthen but chord stays fixed. UNKNOWN. Swept here.
  Targets (carried over from the repo source cards, not re-read by me):
         Fish 1990 individual pectoral AR 3.0-16.9; Park & Choi 2010 Cypselurus hiraii 9.0-10.7.
"""
import math

P0 = {"60% resected": 0.173, "50% resected (adopted)": 0.208, "40% resected": 0.260}
F = {"alf/+ pectoral (measured proxy)": 1.74, "alf/+ caudal (upper proxy)": 2.05}
FISH90 = (3.0, 16.9)
PARK = (9.0, 10.7)


def reach(p0, f, A0, alpha):
    span = p0 * f                       # per-fin span in body lengths (span ~ fin length, upper bound)
    AR = A0 * f ** (2 - alpha)          # AR = span^2 / area, with area ~ f^alpha
    area = span ** 2 / AR               # per-fin area in SL^2
    return span, AR, area


print("== 1. Reachable per-fin span (SL), calculated: span = p0 * f")
for pk, p0 in P0.items():
    print(f"  {pk:24s} " + "  ".join(f"{fk}: {p0*f:.3f}" for fk, f in F.items()))

print("\n== 2. Reachable AR = A0 * f^(2-alpha); f = 1.74. A0 and alpha are ASSUMED.")
print("   A0   alpha=2.0  alpha=1.5  alpha=1.0   [Fish90 envelope 3.0-16.9; Park&Choi 9.0-10.7]")
for A0 in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
    row = [A0 * 1.74 ** (2 - a) for a in (2.0, 1.5, 1.0)]
    tag = lambda x: ("in-F90" if FISH90[0] <= x <= FISH90[1] else "below") + ("+PC" if PARK[0] <= x <= PARK[1] else "")
    print(f"  {A0:4.1f}  " + "  ".join(f"{x:5.2f} {tag(x):9s}" for x in row))

print("\n== 3. Factor-of-two test on each input (central p0=0.208, f=1.74, A0=2 assumed, alpha=2)")
base = reach(0.208, 1.74, 2.0, 2.0)
print(f"  base: span {base[0]:.3f} SL, AR {base[1]:.2f}, area {base[2]:.4f} SL^2")
for name, kw in [("p0 x2", dict(p0=0.416)), ("p0 /2", dict(p0=0.104)),
                 ("f x2", dict(f=3.48)), ("A0 x2", dict(A0=4.0)), ("A0 /2", dict(A0=1.0)),
                 ("alpha 2->1", dict(alpha=1.0))]:
    args = dict(p0=0.208, f=1.74, A0=2.0, alpha=2.0); args.update(kw)
    s, ar, S = reach(**args)
    print(f"  {name:11s} span {s:.3f} ({s/base[0]:.2f}x)  AR {ar:5.2f} ({ar/base[1]:.2f}x)  "
          f"area {S:.4f} ({S/base[2]:.2f}x)  AR in Fish90? {FISH90[0] <= ar <= FISH90[1]}")

print("\n== 4. Minimum A0 for the reachable fin to enter each target envelope (f = 1.74)")
for a in (2.0, 1.5, 1.0):
    m = 1.74 ** (2 - a)
    print(f"  alpha={a}: A0 >= {FISH90[0]/m:.2f} for Fish90 low end; A0 >= {PARK[0]/m:.2f} for Park&Choi low end")


def fan_AR(lengths, theta_deg, base=0.0):
    """AR of a fan of rays from a root of chordwise length `base` (assumed straight, along the body).
    Ray i leaves the root at chordwise position base*i/(n-1), angle phi_i swept back from spanwise 0 to theta.
    Planform = polygon root -> ray tips. Span = max spanwise reach. GEOMETRY MODEL, not a measured fin."""
    n = len(lengths)
    pts = [(0.0, 0.0)]
    for i, L in enumerate(lengths):
        phi = math.radians(theta_deg) * i / (n - 1)
        x0 = base * i / (n - 1)          # chordwise (rearward) root position
        pts.append((x0 + L * math.sin(phi), L * math.cos(phi)))   # (chordwise, spanwise)
    pts.append((base, 0.0))
    area = 0.5 * abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1]
                         for k in range(len(pts))))
    span = max(p[1] for p in pts)
    return span ** 2 / area


print("\n== 5. Fan geometry: AR is invariant under uniform ray elongation (root width neglected)")
n = 12                                   # zebrafish pectoral ray count 10-14 (search-summary); 12 assumed
for theta in (30, 60, 90):
    for r in (1.0, 0.6):                 # trailing/leading ray length ratio, ASSUMED
        L = [1 - (1 - r) * i / (n - 1) for i in range(n)]
        a1 = fan_AR(L, theta)
        a2 = fan_AR([1.74 * x for x in L], theta)
        print(f"  theta={theta:3d} deg, r={r:.1f}: AR {a1:5.2f} -> uniform x1.74 -> {a2:5.2f}")
print("  pure equal-ray sector AR = 2/theta(rad): theta for AR=3.0 ->",
      f"{math.degrees(2/3.0):.1f} deg; AR=9.0 -> {math.degrees(2/9.0):.1f} deg")

print("\n== 6. With a finite root (base = 0.25 x ray length, ASSUMED), uniform elongation dilutes the root")
for theta in (30, 60):
    L = [1.0] * n
    a1 = fan_AR(L, theta, base=0.25); a2 = fan_AR([1.74 * x for x in L], theta, base=0.25)
    print(f"  theta={theta}: AR {a1:.2f} -> {a2:.2f} ({a2/a1:.2f}x)")

print("\n== 7. Ray-differential overgrowth: leading ray x f*g, trailing ray x f, geometric in between")
print("   g = 1 is uniform. theta = 60 deg, r = 1.0 baseline (ASSUMED)")
L = [1.0] * n
a_base = fan_AR(L, 60)
for g in (1.0, 1.25, 1.5, 2.0, 3.0, 4.0):
    fi = [1.74 * g ** (1 - i / (n - 1)) for i in range(n)]
    a = fan_AR([x * y for x, y in zip(L, fi)], 60)
    print(f"  g={g:4.2f}: AR {a_base:.2f} -> {a:.2f} ({a/a_base:.2f}x)")
