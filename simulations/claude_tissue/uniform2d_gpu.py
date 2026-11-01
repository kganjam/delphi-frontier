"""Sim D5 (GPU): CONTROL for edge2d_gpu.py: the same fin fold grows UNIFORMLY along the proximo-distal axis
(every row stretches; dilution), instead of only at the distal edge.  Same kinetics, width, start/end length and
speeds (L_y = Y0 + v t), so the orientation index can be compared one-to-one: is proximo-distal stripe orientation
caused by edge growth specifically or by any growth along y?
Comoving coordinate eta = y / L_y(t) on a fixed grid; diffusion multiplier kx^2 + (k_eta / L_y)^2; dilution -(v/L_y) u.
No-flux boundaries via even mirror extension (field kept symmetric on a doubled periodic domain); implicit spectral
diffusion, explicit reaction.  Output lines match edge2d_gpu.py (RESULT/SNAP/FRAME) for the same collector.
SIMULATED; dimensionless."""
import json, math, sys, time, base64, hashlib
import numpy as np, torch

A_, B_ = 0.1, 0.9
X = int(sys.argv[1]) if len(sys.argv) > 1 else 96
Y0, Y1 = 8, int(sys.argv[2]) if len(sys.argv) > 2 else 192
NY = Y1                      # comoving rows (resolution 1 at the final length)
DT = 0.01
DS = [10, 20, 30]
SPEEDS = [0.4, 0.1, 0.04]
SEEDS = [1, 2, 3, 4]
RELAX = 300.0
SCALE_T = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
dev = "cuda" if torch.cuda.is_available() else "cpu"

def mirror(a):   # (S, NY, X) -> (S, 2NY, 2X) even extension
    a = torch.cat([a, torch.flip(a, [1])], 1); return torch.cat([a, torch.flip(a, [2])], 2)

def orientation(u):
    F = np.abs(np.fft.fft2(u - u.mean()))**2
    ky = np.fft.fftfreq(u.shape[0])[:, None]*2*np.pi; kx = np.fft.fftfreq(u.shape[1])[None, :]*2*np.pi
    ax_, ay_ = np.abs(kx) + 0*ky, np.abs(ky) + 0*kx
    Px = F[ax_ > ay_].sum(); Py = F[ay_ > ax_].sum()
    colspec = (np.abs(np.fft.rfft(u - u.mean(), axis=1))**2).sum(0); kxi = int(colspec[1:].argmax()) + 1
    flat = np.sort(F.ravel())[::-1]
    return float((Px - Py)/(Px + Py)) if Px + Py > 0 else 0.0, kxi, float(flat[:4].sum()/flat.sum())

def to_physical(u_c, Ly):
    """resample comoving rows to unit spacing in physical y for the orientation readout"""
    n = max(2, int(round(Ly))); eta = (np.arange(n) + 0.5)/n*NY - 0.5
    i0 = np.clip(np.floor(eta).astype(int), 0, NY - 1); i1 = np.clip(i0 + 1, 0, NY - 1); f = (eta - i0)[:, None]
    return u_c[i0]*(1 - f) + u_c[i1]*f

def run(d, v):
    u0 = A_ + B_; w0 = B_/u0**2; S = len(SEEDS)
    u = torch.tensor(np.stack([u0 + 0.01*np.random.default_rng(s).standard_normal((NY, X)) for s in SEEDS]), device=dev)
    w = torch.tensor(np.stack([w0 + 0.01*np.random.default_rng(s + 99).standard_normal((NY, X)) for s in SEEDS]), device=dev)
    kx = 2*math.pi*torch.fft.fftfreq(2*X, d=1.0, device=dev, dtype=torch.float64)[None, :]
    ke = 2*math.pi*torch.fft.fftfreq(2*NY, d=1.0/NY, device=dev, dtype=torch.float64)[:, None]   # per unit eta
    T = (Y1 - Y0)/v; nsteps = int((T + RELAX)*SCALE_T/DT); frames = []; fevery = max(1, nsteps//60)
    for i in range(nsteps):
        t = i*DT/SCALE_T; Ly = min(Y0 + v*t, Y1); g = v/Ly if t < T else 0.0
        K2 = kx**2 + (ke/Ly)**2
        uuw = u*u*w
        un = u + DT*((A_ - u + uuw) - g*u); wn = w + DT*((B_ - uuw) - g*w)
        u = torch.fft.ifft2(torch.fft.fft2(mirror(un))/(1 + DT*K2)).real[:, :NY, :X]
        w = torch.fft.ifft2(torch.fft.fft2(mirror(wn))/(1 + DT*d*K2)).real[:, :NY, :X]
        if i % fevery == 0 and d == 10 and v == 0.1:
            frames.append(to_physical(u[0].cpu().numpy(), Ly))
    if not torch.isfinite(u).all(): raise RuntimeError(f"non-finite d={d} v={v}")
    return u.cpu().numpy(), frames

def b64u8(a):
    lo, hi = float(a.min()), float(a.max()); q = ((a - lo)/(hi - lo + 1e-12)*255).astype(np.uint8)
    return base64.b64encode(q.tobytes()).decode(), lo, hi

if __name__ == "__main__":
    t0 = time.time()
    print("META " + json.dumps(dict(model="Schnakenberg 2-D, UNIFORM proximo-distal growth (control for edge growth)", a=A_, b=B_, X=X, Y0=Y0, Y1=Y1,
          dx=1.0, dt=DT, relax=RELAX, ds=DS, speeds=SPEEDS, seeds=SEEDS, scale_t=SCALE_T, device=dev, torch=torch.__version__, numpy=np.__version__,
          gpu=torch.cuda.get_device_name(0) if dev == "cuda" else None, script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())), flush=True)
    for d in DS:
        for v in SPEEDS:
            tc = time.time(); U, frames = run(d, v)
            for j, s in enumerate(SEEDS):
                P = to_physical(U[j], Y1); Aidx, kxi, top2 = orientation(P)
                print("RESULT " + json.dumps(dict(d=d, speed=v, static=False, growth="uniform", seed=s, ny=Y1, orientation_A=Aidx, stripes_across_width=kxi,
                      wavelength_x=X/kxi, top2_power_fraction=top2, amplitude=float(P.std()), wall_s=round(time.time() - tc, 1))), flush=True)
            P = to_physical(U[0], Y1)[::2, ::2]; b, lo, hi = b64u8(P)
            print("SNAP " + json.dumps(dict(d=d, speed=v, seed=SEEDS[0], shape=list(P.shape), lo=lo, hi=hi, u8=b)), flush=True)
            for k, fr in enumerate(frames):
                fr = np.vstack([fr, np.full((Y1 - fr.shape[0], X), np.nan)])[::2, ::2] if fr.shape[0] < Y1 else fr[::2, ::2]
                frn = np.nan_to_num(fr, nan=float(np.nanmin(fr))); b, lo, hi = b64u8(frn)
                print("FRAME " + json.dumps(dict(k=k, d=d, speed=v, shape=list(frn.shape), u8=b)), flush=True)
    print("DONE " + json.dumps(dict(wall_s=round(time.time() - t0, 1))), flush=True)
