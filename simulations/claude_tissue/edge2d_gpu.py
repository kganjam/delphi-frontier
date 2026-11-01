"""Sim D4 (GPU): 2-D Schnakenberg on a fin fold that grows only at its DISTAL edge.
Question: does distal (apical) growth orient the Turing pattern into proximo-distal stripes (ray-like), compared
with the same tissue patterned all at once (static control)?  1-D edge growth (edge_growth_rd.py) gave sequential
insertion; here the second dimension decides stripes vs spots and their orientation.
Domain: width X (x, no-flux), length y grows from Y0 to Y1 at speed v by activating rows at the distal edge
(new rows start at the homogeneous steady state).  Explicit finite differences, dx = 1, no-flux at all active
edges (mirror), seeds batched.  Readouts at the end, on the active region:
  orientation index A = (P_kx - P_ky)/(P_kx + P_ky), P_kx = spectral power with |kx| > |ky|  (A -> +1: stripes
  running along y = proximo-distal 'rays'; A ~ 0 isotropic spots/labyrinth; A -> -1 stripes parallel to the edge)
  stripe count across width from the dominant kx; spot-vs-stripe from the fraction of power in the top 2 modes.
Results stream on stdout as RESULT/SNAP/FRAMES JSON lines (Nebius log transport).  SIMULATED; dimensionless."""
import json, math, sys, time, base64, hashlib
import numpy as np, torch

A_, B_ = 0.1, 0.9
X = int(sys.argv[1]) if len(sys.argv) > 1 else 96
Y0, Y1 = 8, int(sys.argv[2]) if len(sys.argv) > 2 else 192
DT = 0.006
DS = [10, 20, 30]
SPEEDS = [0.4, 0.1, 0.04, 0.0]          # 0.0 = static control: full domain patterned at once
SEEDS = [1, 2, 3, 4]
RELAX = 300.0
SCALE_T = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0   # <1 for smoke tests
dev = "cuda" if torch.cuda.is_available() else "cpu"

def lap(f, ny):
    """5-point Laplacian with mirror (no-flux) boundaries on rows [0, ny) and all columns."""
    g = f[:, :ny]
    up = torch.cat([g[:, :1], g[:, :-1]], 1); dn = torch.cat([g[:, 1:], g[:, -1:]], 1)
    lf = torch.cat([g[:, :, :1], g[:, :, :-1]], 2); rt = torch.cat([g[:, :, 1:], g[:, :, -1:]], 2)
    return up + dn + lf + rt - 4*g

def orientation(u):     # u: (Y, X) numpy active region
    F = np.abs(np.fft.fft2(u - u.mean()))**2
    ky = np.fft.fftfreq(u.shape[0])[:, None]*2*np.pi; kx = np.fft.fftfreq(u.shape[1])[None, :]*2*np.pi
    ax_, ay_ = np.abs(kx) + 0*ky, np.abs(ky) + 0*kx
    Px = F[ax_ > ay_].sum(); Py = F[ay_ > ax_].sum()
    Aidx = float((Px - Py)/(Px + Py)) if Px + Py > 0 else 0.0
    colspec = (np.abs(np.fft.rfft(u - u.mean(), axis=1))**2).sum(0); kxi = int(colspec[1:].argmax()) + 1
    flat = np.sort(F.ravel())[::-1]; top2 = float(flat[:4].sum()/flat.sum())   # +-k pairs -> 4 entries for 2 modes
    return Aidx, kxi*u.shape[1]/u.shape[1], kxi, top2

def run(d, v):
    u0 = A_ + B_; v0 = B_/u0**2; S = len(SEEDS)
    gens = [np.random.default_rng(s) for s in SEEDS]
    u = torch.full((S, Y1, X), u0, dtype=torch.float64, device=dev); w = torch.full_like(u, v0)
    noise_u = torch.tensor(np.stack([0.01*g.standard_normal((Y1, X)) for g in gens]), device=dev)
    noise_w = torch.tensor(np.stack([0.01*np.random.default_rng(s + 99).standard_normal((Y1, X)) for s in SEEDS]), device=dev)
    u += noise_u; w += noise_w
    static = v == 0.0; ny = Y1 if static else Y0; T = 0.0 if static else (Y1 - Y0)/v
    tend = (T + RELAX)*SCALE_T if not static else (RELAX + 300.0)*SCALE_T
    nsteps = int(tend/DT); acc = 0.0; frames = []; fevery = max(1, nsteps//60)
    for i in range(nsteps):
        gu = u[:, :ny]; gw = w[:, :ny]; uuw = gu*gu*gw
        nu = gu + DT*((A_ - gu + uuw) + lap(u, ny)); nw = gw + DT*((B_ - uuw) + d*lap(w, ny))
        u[:, :ny] = nu; w[:, :ny] = nw
        if not static and i*DT < T*SCALE_T:
            acc += v/SCALE_T*DT
            while acc >= 1.0 and ny < Y1:
                acc -= 1.0; u[:, ny] = u0 + noise_u[:, ny]; w[:, ny] = v0 + noise_w[:, ny]; ny += 1
        if i % fevery == 0 and d == 10 and v == 0.1:
            frames.append(u[0].cpu().numpy())
    if not torch.isfinite(u).all(): raise RuntimeError(f"non-finite d={d} v={v}")
    return u[:, :ny].cpu().numpy(), ny, frames

def b64u8(a):
    lo, hi = float(a.min()), float(a.max()); q = ((a - lo)/(hi - lo + 1e-12)*255).astype(np.uint8)
    return base64.b64encode(q.tobytes()).decode(), lo, hi

if __name__ == "__main__":
    t0 = time.time()
    print("META " + json.dumps(dict(model="Schnakenberg 2-D, distal edge growth", a=A_, b=B_, X=X, Y0=Y0, Y1=Y1, dx=1.0, dt=DT, relax=RELAX,
          ds=DS, speeds=SPEEDS, seeds=SEEDS, scale_t=SCALE_T, device=dev, torch=torch.__version__, numpy=np.__version__,
          gpu=torch.cuda.get_device_name(0) if dev == "cuda" else None, script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())), flush=True)
    for d in DS:
        for v in SPEEDS:
            tc = time.time(); U, ny, frames = run(d, v)
            for j, s in enumerate(SEEDS):
                Aidx, _, kxi, top2 = orientation(U[j])
                print("RESULT " + json.dumps(dict(d=d, speed=v, static=v == 0.0, seed=s, ny=ny, orientation_A=Aidx, stripes_across_width=kxi,
                      wavelength_x=X/kxi, top2_power_fraction=top2, amplitude=float(U[j].std()), wall_s=round(time.time() - tc, 1))), flush=True)
            b, lo, hi = b64u8(U[0][::2, ::2])
            print("SNAP " + json.dumps(dict(d=d, speed=v, seed=SEEDS[0], shape=list(U[0][::2, ::2].shape), lo=lo, hi=hi, u8=b)), flush=True)
            if frames:
                for k, fr in enumerate(frames):
                    b, lo, hi = b64u8(fr[::2, ::2]); print("FRAME " + json.dumps(dict(k=k, d=d, speed=v, shape=list(fr[::2, ::2].shape), u8=b)), flush=True)
    print("DONE " + json.dumps(dict(wall_s=round(time.time() - t0, 1))), flush=True)
