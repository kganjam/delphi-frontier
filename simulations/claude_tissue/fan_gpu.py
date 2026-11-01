"""Sim D6 (GPU): Turing pattern on a FAN-shaped fin fold (annular sector) growing at its distal arc.
Fin rays radiate from the base and the fin widens distally; on a widening fan, a stripe pattern with fixed spacing
must add stripes (insertion or branching) as the arc length r*Theta grows.  Question: in the stripe regime that gave
proximo-distal stripes on a rectangle (edge2d/uniform2d), do stripes follow the radial direction, and how does the
stripe count along the arc scale with radius: tracking r*Theta/lambda (insertion/branching) or frozen at the base count?
Polar grid (r, theta): r in [R0, R(t)], theta in [0, THETA]; new radial rows activated at the distal arc at speed v.
Laplacian u_rr + u_r/r + u_thth/r^2, no-flux on all active edges (mirror), explicit; seeds batched.
Readouts at the end: peaks along theta at several radii (count vs r*THETA/lambda), radial orientation index
A_r = (P_theta-dominated - P_r-dominated)/(sum) computed on the (r, theta*r_mid) map.  SIMULATED; dimensionless."""
import json, math, sys, time, base64, hashlib
import numpy as np, torch

A_, B_ = 0.1, 0.9
R0 = 30.0
NR_END = int(sys.argv[1]) if len(sys.argv) > 1 else 160      # final radial rows (dr = 1): R_end = R0 + NR_END
NTH = int(sys.argv[2]) if len(sys.argv) > 2 else 160
THETA = 1.2
SCALE_T = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
DS = json.loads(sys.argv[4]) if len(sys.argv) > 4 else [10, 20]
SPEEDS = json.loads(sys.argv[5]) if len(sys.argv) > 5 else [0.4, 0.1, 0.0]
SEEDS = [1, 2, 3, 4]
NR0 = 8; RELAX = 300.0
DTH = THETA/NTH
dev = "cuda" if torch.cuda.is_available() else "cpu"
LAMBDA_STAR = {10: 10.7, 20: 11.2, 30: 12.0}   # simulated wavelength at gamma=1 from rd-wavelength v2 (2*pi/k_peak)

def lap(f, nr, r):
    g = f[:, :nr]; rr = r[:nr][None, :, None]
    up = torch.cat([g[:, :1], g[:, :-1]], 1); dn = torch.cat([g[:, 1:], g[:, -1:]], 1)
    lf = torch.cat([g[:, :, :1], g[:, :, :-1]], 2); rt = torch.cat([g[:, :, 1:], g[:, :, -1:]], 2)
    return (up + dn - 2*g) + (dn - up)/(2*rr) + (lf + rt - 2*g)/(rr*DTH)**2

def peaks_along(row):
    c = row.mean(); thr = 0.25*(row.max() - row.min())
    return int(sum(1 for i in range(1, len(row) - 1) if row[i] > row[i-1] and row[i] >= row[i+1] and row[i] - c > thr))

def run(d, v, dt):
    u0 = A_ + B_; w0 = B_/u0**2; NR = NR_END
    r = torch.tensor(R0 + np.arange(NR) + 0.5, device=dev)
    nu_ = torch.tensor(np.stack([0.01*np.random.default_rng(s).standard_normal((NR, NTH)) for s in SEEDS]), device=dev)
    nw_ = torch.tensor(np.stack([0.01*np.random.default_rng(s + 99).standard_normal((NR, NTH)) for s in SEEDS]), device=dev)
    u = u0 + nu_; w = w0 + nw_
    static = v == 0.0; nr = NR if static else NR0; T = 0.0 if static else (NR - NR0)/v
    nsteps = int(((T + RELAX) if not static else 600.0)*SCALE_T/dt); acc = 0.0
    for i in range(nsteps):
        g = u[:, :nr]; h = w[:, :nr]; uuw = g*g*h
        un = g + dt*((A_ - g + uuw) + lap(u, nr, r)); wn = h + dt*((B_ - uuw) + d*lap(w, nr, r))
        u[:, :nr] = un; w[:, :nr] = wn
        if not static and i*dt < T*SCALE_T:
            acc += v/SCALE_T*dt
            while acc >= 1.0 and nr < NR:
                acc -= 1.0; u[:, nr] = u0 + nu_[:, nr]; w[:, nr] = w0 + nw_[:, nr]; nr += 1
    if not torch.isfinite(u).all(): raise RuntimeError(f"non-finite d={d} v={v}")
    return u[:, :nr].cpu().numpy(), nr

def to_cart(U, nr, n=128):
    """render the sector into a square image (nearest neighbour) for snapshots/video"""
    Rm = R0 + nr; xs = np.linspace(-Rm*math.sin(THETA/2), Rm*math.sin(THETA/2), n); ys = np.linspace(R0*math.cos(THETA/2) - 2, Rm, n)
    X, Y = np.meshgrid(xs, ys); rr = np.hypot(X, Y); th = np.arctan2(X, Y) + THETA/2
    ir = np.floor(rr - R0).astype(int); it = np.floor(th/DTH).astype(int)
    ok = (ir >= 0) & (ir < nr) & (it >= 0) & (it < NTH)
    img = np.full((n, n), np.nan); img[ok] = U[ir[ok], it[ok]]; return img

def b64u8(a):
    lo, hi = float(np.nanmin(a)), float(np.nanmax(a)); q = np.nan_to_num((a - lo)/(hi - lo + 1e-12)*255, nan=0).astype(np.uint8)
    return base64.b64encode(q.tobytes()).decode(), lo, hi

if __name__ == "__main__":
    t0 = time.time()
    print("META " + json.dumps(dict(model="Schnakenberg on a fan (annular sector) growing at its distal arc", a=A_, b=B_, R0=R0, NR0=NR0, NR_END=NR_END,
          NTH=NTH, THETA=THETA, ds=DS, speeds=SPEEDS, seeds=SEEDS, relax=RELAX, scale_t=SCALE_T, lambda_star=LAMBDA_STAR, device=dev,
          torch=torch.__version__, gpu=torch.cuda.get_device_name(0) if dev == "cuda" else None,
          script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())), flush=True)
    for d in DS:
        dt = 0.8*(R0*DTH)**2/(4*d*(1 + (R0*DTH)**2))       # explicit stability on the innermost arc
        for v in SPEEDS:
            tc = time.time(); U, nr = run(d, v, dt)
            radii = [int(f*(nr - 1)) for f in (0.1, 0.3, 0.5, 0.7, 0.9)]
            for j, s in enumerate(SEEDS):
                cnt = [peaks_along(U[j, ir]) for ir in radii]
                exp = [(R0 + ir + 0.5)*THETA/LAMBDA_STAR.get(d, 11.0) for ir in radii]
                F = np.abs(np.fft.fft2(U[j] - U[j].mean()))**2
                kr = np.abs(np.fft.fftfreq(U[j].shape[0]))[:, None]; kt = np.abs(np.fft.fftfreq(NTH, d=(R0 + nr/2)*DTH))[None, :]
                Pt = F[(kt + 0*kr) > (kr + 0*kt)].sum(); Pr = F[(kr + 0*kt) > (kt + 0*kr)].sum()
                print("RESULT " + json.dumps(dict(d=d, speed=v, static=v == 0.0, seed=s, nr=nr, dt=dt, radii=[R0 + ir + 0.5 for ir in radii],
                      peaks_along_arc=cnt, expected_r_theta_over_lambda=exp, radial_orientation_A=float((Pt - Pr)/(Pt + Pr)),
                      amplitude=float(U[j].std()), wall_s=round(time.time() - tc, 1))), flush=True)
            b, lo, hi = b64u8(to_cart(U[0], nr))
            print("SNAP " + json.dumps(dict(d=d, speed=v, seed=SEEDS[0], shape=[128, 128], lo=lo, hi=hi, u8=b)), flush=True)
    print("DONE " + json.dumps(dict(wall_s=round(time.time() - t0, 1))), flush=True)
