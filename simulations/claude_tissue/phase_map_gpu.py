"""Sim A3 (GPU): where does Schnakenberg give STRIPES (ray-like) vs SPOTS (scale/spot-like)?
Phase map over kinetic parameter b and diffusion ratio d (a = 0.1, gamma = 1), 2-D periodic, IMEX spectral,
N = 128, L = 80 (dx = 0.625), t = 800, 3 seeds batched.  This quantifies the mapping caveat of Sim A: which
part of parameter space could even produce a ray-like (striped) readout.
Classifier on the final field, threshold at the mean:
  component density  rho_c = n_components(u > mean) * lambda^2 / area  (periodic labelling)
  spots ~ hexagonal lattice -> rho_c ~ 1; stripes -> rho_c << 1 (few long components); also elongation of the largest
  component.  Linear theory (Turing unstable or not) is reported for every cell.
Streams RESULT/SNAP JSON lines on stdout.  SIMULATED; dimensionless."""
import json, math, sys, time, base64, hashlib
import numpy as np, torch
try:
    from scipy import ndimage
except Exception:
    ndimage = None

A_ = 0.1
BS = [0.3, 0.5, 0.7, 0.9, 1.1, 1.4, 1.8, 2.4]
DS = [6, 8, 10, 13, 17, 22, 30, 45]
SEEDS = [11, 22, 33]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 128
L = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
T = float(sys.argv[3]) if len(sys.argv) > 3 else 800.0
DT = 0.02
dev = "cuda" if torch.cuda.is_available() else "cpu"

def linear(d, b):
    u0 = A_ + b; v0 = b/u0**2
    J = np.array([[-1 + 2*u0*v0, u0**2], [-2*u0*v0, -u0**2]])
    ks = np.linspace(0.005, 4, 4000); lam = np.array([np.linalg.eigvals(J - k*k*np.diag([1.0, d])).real.max() for k in ks])
    i = lam.argmax(); stable_hom = np.linalg.eigvals(J).real.max() < 0
    return (float(ks[i]) if lam[i] > 0 else None), float(lam[i]), bool(stable_hom)

k1 = 2*math.pi*np.fft.fftfreq(N, d=L/N); KX, KY = np.meshgrid(k1, k1); K2np = KX**2 + KY**2
DK = 2*math.pi/L; BIN = np.rint(np.sqrt(K2np)/DK).astype(int)

def run(d, b):
    u0 = A_ + b; v0 = b/u0**2
    u = torch.tensor(np.stack([u0 + 0.01*np.random.default_rng(s).standard_normal((N, N)) for s in SEEDS]), device=dev, dtype=torch.float64)
    w = torch.tensor(np.stack([v0 + 0.01*np.random.default_rng(s + 7).standard_normal((N, N)) for s in SEEDS]), device=dev, dtype=torch.float64)
    K2 = torch.tensor(K2np, device=dev, dtype=torch.float64); Lu = 1/(1 + DT*K2); Lw = 1/(1 + DT*d*K2)
    for _ in range(int(T/DT)):
        uuw = u*u*w
        u = torch.fft.ifft2(Lu*torch.fft.fft2(u + DT*(A_ - u + uuw))).real
        w = torch.fft.ifft2(Lw*torch.fft.fft2(w + DT*(b - uuw))).real
    if not torch.isfinite(u).all(): raise RuntimeError("non-finite")
    return u.cpu().numpy()

def classify(u):
    amp = float(u.std())
    F = np.abs(np.fft.fft2(u - u.mean()))**2; spec = np.bincount(BIN.ravel(), weights=F.ravel())
    kp = int(spec[1:].argmax()) + 1; lam = 2*math.pi/(kp*DK)
    out = dict(amplitude=amp, k_peak=kp*DK, wavelength=lam)
    if ndimage is None or amp < 0.02:
        return out
    m = u > u.mean(); lab, n = ndimage.label(m)          # 4-connectivity, then merge across periodic edges
    par = list(range(n + 1))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a_, b_ in list(zip(lab[:, 0], lab[:, -1])) + list(zip(lab[0, :], lab[-1, :])):
        if a_ and b_: par[f(a_)] = f(b_)
    roots = np.array([f(x) for x in range(n + 1)]); sizes = np.bincount(roots[lab.ravel()], minlength=n + 1); sizes[0] = 0
    nc = int(len(set(roots[1:].tolist()))) if n else 0
    dens = nc*lam*lam/(L*L)
    out.update(n_components=nc, component_density=float(dens), largest_component_fraction=float(sizes.max()/(N*N)),
               label=("spots" if dens > 0.6 else "stripes/labyrinth"))
    return out

def b64u8(a):
    lo, hi = float(a.min()), float(a.max()); q = ((a - lo)/(hi - lo + 1e-12)*255).astype(np.uint8)
    return base64.b64encode(q.tobytes()).decode(), lo, hi

if __name__ == "__main__":
    t0 = time.time()
    print("META " + json.dumps(dict(model="Schnakenberg phase map", a=A_, bs=BS, ds=DS, seeds=SEEDS, N=N, L=L, t_end=T, dt=DT, device=dev,
          scipy=ndimage is not None, torch=torch.__version__, gpu=torch.cuda.get_device_name(0) if dev == "cuda" else None,
          script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())), flush=True)
    for b in BS:
        for d in DS:
            tc = time.time(); kth, gr, hom = linear(d, b)
            if kth is None or not hom:
                print("RESULT " + json.dumps(dict(b=b, d=d, turing_unstable=False, homogeneous_stable=hom, k_theory=kth, simulated=False)), flush=True); continue
            U = run(d, b)
            for j, s in enumerate(SEEDS):
                print("RESULT " + json.dumps(dict(b=b, d=d, seed=s, turing_unstable=True, homogeneous_stable=hom, k_theory=kth, growth_rate=gr, simulated=True,
                      wall_s=round(time.time() - tc, 1), **classify(U[j]))), flush=True)
            bb, lo, hi = b64u8(U[0][::2, ::2]); print("SNAP " + json.dumps(dict(b=b, d=d, n=N//2, lo=lo, hi=hi, u8=bb)), flush=True)
    print("DONE " + json.dumps(dict(wall_s=round(time.time() - t0, 1))), flush=True)
