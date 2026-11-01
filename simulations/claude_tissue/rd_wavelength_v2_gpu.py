"""Sim A v2: large-domain Schnakenberg wavelength sweep (fixes v1 resolution defect).
v1 used L=32 (dk = 2*pi/32 = 0.196, only ~3 wavelengths per side), so the selected wavenumber
was quantized coarser than its trend in d.  v2: L=128, N=256 (dx=0.5 as v1), dk=0.049,
10 diffusion ratios x 3 rate scales x 3 seeds (seeds batched), periodic, IMEX pseudo-spectral.
Convergence control built in: dominant k recorded at t=T/2 and t=T.
Runs on CUDA via torch if present, else CPU torch.  Results stream as JSON lines on stdout
(prefix 'RESULT ' / 'SNAP ') so a Nebius job log is the transport.  SIMULATED; dimensionless."""
import json, math, sys, time, base64, hashlib
import numpy as np
import torch

A, B = 0.1, 0.9
N = int(sys.argv[1]) if len(sys.argv) > 1 else 256
LX = float(sys.argv[2]) if len(sys.argv) > 2 else 128.0
T_END = float(sys.argv[3]) if len(sys.argv) > 3 else 400.0
DT = 0.02
DS = [10, 12, 14, 17, 20, 25, 30, 37, 45, 55]
GAMMAS = [0.5, 1.0, 2.0]
SEEDS = [11, 22, 33]
dev = "cuda" if torch.cuda.is_available() else "cpu"
torch.backends.cuda.matmul.allow_tf32 = False

def linear_kmax(d, g):
    u0 = A + B; v0 = B/u0**2
    J = g*np.array([[-1 + 2*u0*v0, u0**2], [-2*u0*v0, -u0**2]])
    ks = np.linspace(0.005, 3, 6000); lam = []
    for k in ks:
        lam.append(np.linalg.eigvals(J - k*k*np.diag([1.0, d])).real.max())
    lam = np.array(lam); i = lam.argmax()
    unstable = ks[lam > 0]
    return (float(ks[i]) if lam[i] > 0 else None, float(lam[i]),
            [float(unstable.min()), float(unstable.max())] if len(unstable) else None)

k1 = 2*math.pi*np.fft.fftfreq(N, d=LX/N)
KX, KY = np.meshgrid(k1, k1); K2np = KX**2 + KY**2; Kmag = np.sqrt(K2np)
DK = 2*math.pi/LX
BIN = np.rint(Kmag/DK).astype(int)          # radial shells of width dk
NB = BIN.max() + 1

def radial_spectrum(u):  # u: (S,N,N) torch
    F = torch.fft.fft2(u - u.mean(dim=(1, 2), keepdim=True)).abs()**2
    F = F.cpu().numpy().reshape(u.shape[0], -1)
    out = np.zeros((u.shape[0], NB))
    for s in range(u.shape[0]):
        out[s] = np.bincount(BIN.ravel(), weights=F[s], minlength=NB)
    return out

def peak_k(spec):
    i = int(spec[1:].argmax()) + 1
    # parabolic sub-shell refinement on log power
    if 1 < i < len(spec) - 1 and spec[i-1] > 0 and spec[i+1] > 0:
        y0, y1, y2 = np.log(spec[i-1]), np.log(spec[i]), np.log(spec[i+1])
        den = (y0 - 2*y1 + y2); off = 0.5*(y0 - y2)/den if den != 0 else 0.0
        off = max(-0.5, min(0.5, off))
    else:
        off = 0.0
    return float((i + off)*DK), float(i*DK)

def run(d, g):
    torch.manual_seed(0)
    u0 = A + B; v0 = B/u0**2
    gens = [np.random.default_rng(s) for s in SEEDS]
    u = torch.tensor(np.stack([u0 + 0.01*r.standard_normal((N, N)) for r in gens]), dtype=torch.float64, device=dev)
    v = torch.tensor(np.stack([v0 + 0.01*np.random.default_rng(s + 1000).standard_normal((N, N)) for s in SEEDS]), dtype=torch.float64, device=dev)
    K2 = torch.tensor(K2np, dtype=torch.float64, device=dev)
    Lu = 1/(1 + DT*K2); Lv = 1/(1 + DT*d*K2)
    nsteps = int(round(T_END/DT)); half = nsteps//2; mid = None
    for i in range(nsteps):
        uuv = u*u*v
        fu = g*(A - u + uuv); fv = g*(B - uuv)
        u = torch.fft.ifft2(Lu*torch.fft.fft2(u + DT*fu)).real
        v = torch.fft.ifft2(Lv*torch.fft.fft2(v + DT*fv)).real
        if i + 1 == half:
            mid = radial_spectrum(u)
    if not torch.isfinite(u).all():
        raise RuntimeError(f"non-finite field d={d} g={g}")
    return u, mid, radial_spectrum(u)

def snap_b64(u2d, n=64):
    a = u2d.cpu().numpy(); s = a.shape[0]//n
    a = a[:s*n, :s*n].reshape(n, s, n, s).mean((1, 3))
    lo, hi = a.min(), a.max(); q = ((a - lo)/(hi - lo + 1e-12)*255).astype(np.uint8)
    return base64.b64encode(q.tobytes()).decode(), float(lo), float(hi)

if __name__ == "__main__":
    t0 = time.time()
    meta = dict(model="Schnakenberg", a=A, b=B, N=N, L=LX, dx=LX/N, dk=DK, t_end=T_END, dt=DT, ds=DS, gammas=GAMMAS,
                seeds=SEEDS, device=dev, torch=torch.__version__, numpy=np.__version__,
                gpu=(torch.cuda.get_device_name(0) if dev == "cuda" else None),
                script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())
    print("META " + json.dumps(meta), flush=True)
    for g in GAMMAS:
        for d in DS:
            tc = time.time(); kth, lam, band = linear_kmax(d, g)
            u, smid, sfin = run(d, g)
            for j, s in enumerate(SEEDS):
                kp, kshell = peak_k(sfin[j]); kpm, kshm = peak_k(smid[j])
                amp = float(u[j].std())
                cen = float((np.arange(NB)*DK*sfin[j]).sum()/sfin[j].sum()) if sfin[j].sum() > 0 else None
                print("RESULT " + json.dumps(dict(d=d, gamma=g, seed=s, k_theory=kth, growth_rate_max=lam, unstable_band=band,
                      k_peak=kp, k_peak_shell=kshell, k_peak_half_time=kpm, k_shell_half_time=kshm,
                      converged_shell=bool(kshell == kshm), k_centroid=cen, amplitude=amp, patterned=bool(amp > 0.05),
                      wall_s=round(time.time() - tc, 2))), flush=True)
            if d in (10, 20, 45) or g == 1.0:
                b, lo, hi = snap_b64(u[0])
                print("SNAP " + json.dumps(dict(d=d, gamma=g, seed=SEEDS[0], n=64, lo=lo, hi=hi, u8=b)), flush=True)
    print("DONE " + json.dumps(dict(wall_s=round(time.time() - t0, 1))), flush=True)
