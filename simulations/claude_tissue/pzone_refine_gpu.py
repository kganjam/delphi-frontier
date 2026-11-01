"""Sim D7f (GPU, GRID-REFINEMENT variant of pzone_regional_gpu.py requested by the gemini-4-argon review of the zone-width rule).
Same physics at half the cell size: all grid lengths (X, Y0, Y1, Lp, v) are doubled by the caller, both diffusivities are
multiplied by DSCALE = 4 (argv[8]) and the time step is DT (argv[9], 0.0015 = 0.006/4).  Cell widths are still split above 2
grid units, i.e. 1 physical unit, so the zone is resolved by twice as many cells.  Original docstring follows.
Sim D7r (GPU, REGIONAL-metric variant of pzone_gamma_gpu.py: the whole-domain orientation A mixed the proximal region,
which keeps the pattern formed in the starting fold, with newly grown distal tissue.  Adds A for the distal half, the
proximal quarter, and for tissue descended from growth (cell origin tracked through splits).  Original docstring follows.)
Sim D7g (GPU, rate-scale variant of pzone_gpu.py: argv[7] = gamma; tests whether the zone width at which orientation
switches scales with the pattern wavelength, lambda ~ gamma^-1/2).  Original D7 docstring follows.
Sim D7 (GPU): proliferation-zone control requested by the gemini-4-argon review of the 2-D growth results.
Fin fold of width X grows along y by CONTINUOUS growth confined to a distal proliferation zone of width LP
(LP small ~ apical/edge growth; LP = whole length ~ uniform growth), starting from a fold LONGER than several
wavelengths (Y0 = 48, lambda ~ 11) to remove the quasi-1-D starting artefact.
Finite-volume grid in y with variable cell widths h_i (same geometry for all seeds): cells whose centre lies within
LP of the distal end grow at rate g = v/LP (total elongation rate v), concentrations diluted by the same factor;
cells wider than 2 split into two equal cells (conservative).  No row is ever inserted at steady state: new tissue
inherits the local field.  Diffusion: y flux between centres (h_i+h_{i+1})/2 apart, x uniform dx = 1, no-flux edges.
Readout: field resampled to unit spacing in physical y, orientation index A as in edge2d_gpu.py; 12 seeds.
SIMULATED; dimensionless."""
import json, math, sys, time, base64, hashlib
import numpy as np, torch

A_, B_ = 0.1, 0.9
X = int(sys.argv[1]) if len(sys.argv) > 1 else 96
Y0 = int(sys.argv[2]) if len(sys.argv) > 2 else 48
Y1 = int(sys.argv[3]) if len(sys.argv) > 3 else 192
SCALE_T = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
LPS = json.loads(sys.argv[5]) if len(sys.argv) > 5 else [2, 12, 48, 0]          # 0 = whole length (uniform)
SPEEDS = json.loads(sys.argv[6]) if len(sys.argv) > 6 else [0.1, 0.25, 0.4]
D = 10.0; DT = 0.006; RELAX = 300.0
GAMMA = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
DSCALE = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
DT = float(sys.argv[9]) if len(sys.argv) > 9 else DT
SEEDS = list(range(1, 13))
dev = "cuda" if torch.cuda.is_available() else "cpu"

def orientation(u):
    F = np.abs(np.fft.fft2(u - u.mean()))**2
    ky = np.fft.fftfreq(u.shape[0])[:, None]*2*np.pi; kx = np.fft.fftfreq(u.shape[1])[None, :]*2*np.pi
    ax_, ay_ = np.abs(kx) + 0*ky, np.abs(ky) + 0*kx
    Px = F[ax_ > ay_].sum(); Py = F[ay_ > ax_].sum()
    colspec = (np.abs(np.fft.rfft(u - u.mean(), axis=1))**2).sum(0); kxi = int(colspec[1:].argmax()) + 1
    return float((Px - Py)/(Px + Py)) if Px + Py > 0 else 0.0, kxi

def lap_x(f):
    lf = torch.cat([f[..., :1], f[..., :-1]], -1); rt = torch.cat([f[..., 1:], f[..., -1:]], -1); return lf + rt - 2*f

def div_y(f, h):
    dist = 0.5*(h[1:] + h[:-1])                                   # (n-1,)
    flux = (f[:, 1:] - f[:, :-1])/dist[None, :, None]             # (S, n-1, X)
    z = torch.zeros_like(f[:, :1]); fl = torch.cat([z, flux, z], 1)
    return (fl[:, 1:] - fl[:, :-1])/h[None, :, None]

def resample(U, h, n_out):
    edges = np.concatenate([[0], np.cumsum(h)]); centres = 0.5*(edges[1:] + edges[:-1]); L = edges[-1]
    yq = (np.arange(n_out) + 0.5)*L/n_out
    return np.stack([np.stack([np.interp(yq, centres, U[s, :, j]) for j in range(U.shape[2])], 1) for s in range(U.shape[0])])

def run(lp, v):
    u0 = A_ + B_; w0 = B_/u0**2; S = len(SEEDS)
    u = torch.tensor(np.stack([u0 + 0.01*np.random.default_rng(s).standard_normal((Y0 if v > 0 else Y1, X)) for s in SEEDS]), device=dev)
    w = torch.tensor(np.stack([w0 + 0.01*np.random.default_rng(s + 99).standard_normal((Y0 if v > 0 else Y1, X)) for s in SEEDS]), device=dev)
    h = torch.ones(u.shape[1], dtype=torch.float64, device=dev)
    orig = torch.ones(u.shape[1], dtype=torch.bool, device=dev)          # True = present in the starting fold
    T = (Y1 - Y0)/v if v > 0 else 0.0; nsteps = int(((T + RELAX) if v > 0 else 600.0)*SCALE_T/DT); splits = 0
    for i in range(nsteps):
        uuw = u*u*w
        u = u + DT*(GAMMA*(A_ - u + uuw) + DSCALE*(div_y(u, h) + lap_x(u)))
        w = w + DT*(GAMMA*(B_ - uuw) + DSCALE*D*(div_y(w, h) + lap_x(w)))
        if v > 0 and i*DT < T*SCALE_T:
            L = float(h.sum()); zone_w = L if lp == 0 else min(lp, L); g = (v/SCALE_T)/zone_w
            far = torch.cumsum(h, 0) - 0.5*h                     # centre positions
            m = (far >= L - zone_w).to(h.dtype)
            fac = 1 + g*DT*m; h = h*fac; u = u/fac[None, :, None]; w = w/fac[None, :, None]
            if i % 25 == 0 and bool((h > 2.0).any()):
                idx = torch.nonzero(h > 2.0).flatten().tolist(); hn, un, wn, on = [], [], [], []; last = 0
                for k in idx:
                    hn += [h[last:k], (h[k:k+1]/2).repeat(2)]; un += [u[:, last:k], u[:, k:k+1].repeat(1, 2, 1)]; wn += [w[:, last:k], w[:, k:k+1].repeat(1, 2, 1)]
                    on += [orig[last:k], torch.tensor([bool(orig[k]), False], device=dev)]; last = k + 1     # distal daughter counts as new tissue
                hn.append(h[last:]); un.append(u[:, last:]); wn.append(w[:, last:]); on.append(orig[last:])
                h = torch.cat(hn); u = torch.cat(un, 1); w = torch.cat(wn, 1); orig = torch.cat(on); splits += len(idx)
    if not torch.isfinite(u).all(): raise RuntimeError(f"non-finite lp={lp} v={v}")
    return u.cpu().numpy(), h.cpu().numpy(), splits, orig.cpu().numpy()

def b64u8(a):
    lo, hi = float(a.min()), float(a.max()); q = ((a - lo)/(hi - lo + 1e-12)*255).astype(np.uint8)
    return base64.b64encode(q.tobytes()).decode(), lo, hi

if __name__ == "__main__":
    t0 = time.time()
    print("META " + json.dumps(dict(model="Schnakenberg 2-D, continuous growth in a distal proliferation zone (finite volume)", a=A_, b=B_, d=D, gamma=GAMMA, dscale=DSCALE, X=X, Y0=Y0, Y1=Y1,
          dt=DT, relax=RELAX, lps=LPS, speeds=SPEEDS, seeds=SEEDS, scale_t=SCALE_T, device=dev, torch=torch.__version__,
          gpu=torch.cuda.get_device_name(0) if dev == "cuda" else None, script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())), flush=True)
    cases = [(lp, v) for lp in LPS for v in SPEEDS] + [(-1, 0.0)]          # (-1, 0) = static control at final length
    for lp, v in cases:
        tc = time.time(); U, h, nsp, og = run(max(lp, 0), v); L = float(h.sum())
        edges = np.concatenate([[0], np.cumsum(h)]); new_from = float(edges[np.nonzero(~og)[0].min()]) if (~og).any() else None
        P = resample(U, h, int(round(L)))
        for j, s in enumerate(SEEDS):
            Aidx, kxi = orientation(P[j]); n = P[j].shape[0]
            A_dist = orientation(P[j][n//2:])[0]; A_prox = orientation(P[j][:n//4])[0]
            A_new = orientation(P[j][int(new_from):]) [0] if (new_from is not None and n - int(new_from) >= 22) else None
            print("RESULT " + json.dumps(dict(gamma=GAMMA, lp=lp, lp_label=("static" if lp < 0 else ("uniform" if lp == 0 else lp)), speed=v, seed=s, length=L, cells=int(len(h)),
                  splits=nsp, orientation_A=Aidx, A_distal_half=A_dist, A_proximal_quarter=A_prox, A_new_tissue=A_new, new_tissue_from_y=new_from, stripes_across_width=kxi, amplitude=float(P[j].std()), wall_s=round(time.time() - tc, 1))), flush=True)
        b, lo, hi = b64u8(P[0][::2, ::2])
        print("SNAP " + json.dumps(dict(lp=lp, speed=v, seed=1, shape=list(P[0][::2, ::2].shape), lo=lo, hi=hi, u8=b)), flush=True)
    print("DONE " + json.dumps(dict(wall_s=round(time.time() - t0, 1))), flush=True)
