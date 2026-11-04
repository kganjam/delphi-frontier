# Challenge 84: independent recomputation + Eloy (2012) elongated-body optimisation, eqs 4-11,
# optimal-form kinematics (alpha=psi=0): xdot=U, ydot=pi*St*U*cos(wt), theta=theta0*cos(wt).
# Units m=U=1. Constraint <T> = D  <=>  <T>/(m U^2) = 2 Li / pi   (eq 5). CALCULATED ONLY.
import numpy as np
def brentq(g, a, b, tol=1e-9):
    ga = g(a)
    for _ in range(200):
        m = 0.5*(a+b); gm = g(m)
        if (gm < 0) == (ga < 0): a, ga = m, gm
        else: b = m
        if b-a < tol: break
    return 0.5*(a+b)
ph = np.linspace(0, 2*np.pi, 4001)[:-1]; c = np.cos(ph)
def TE(St, th0):
    th = th0*c; yd = np.pi*St*c
    w = yd*np.cos(th) - np.sin(th); u = np.cos(th) + yd*np.sin(th)
    return np.mean(w*yd - 0.5*w*w*np.cos(th)), np.mean(0.5*w*w*u)
def St_for(th0, Li):  # St that gives thrust balance at given tail angle
    g = lambda St: TE(St, th0)[0] - 2*Li/np.pi
    hi = 0.01
    while g(hi) < 0:
        hi *= 1.5
        if hi > 50: return None
    return brentq(g, 1e-4, hi)
def scan(Li):
    rows = []
    for th0 in np.linspace(1e-3, np.pi/2, 400):
        St = St_for(th0, Li)
        if St is None: continue
        T, E = TE(St, th0); rows.append((th0, St, T/(T+E)))
    return np.array(rows)
def Cd(Re): return max(2*1.328*Re**-0.5, 0.072*Re**-0.2)
# validation against Eloy's power law
print("validation: Li, St_opt(numeric), 0.75Li^1/3")
for Li in (0.01, 0.03, 0.1, 0.3, 1.0):
    r = scan(Li); i = r[:,2].argmax(); print("  %.3f  %.3f  %.3f" % (Li, r[i,1], 0.75*Li**(1/3)))
U, L, nu = 1.95, 0.04, 1e-6; Re = U*L/nu; cd = Cd(Re)
print("Re=%.4g Cd=%.5f" % (Re, cd))
print("h/L k(drag mult) Li  St_min St_accept_lo St_opt etamax | f_min f_acc_lo f_opt (Hz, A=8mm) | f_opt at A=0.15/0.25/0.30 TL")
for hL in (0.15, 0.20, 0.25, 0.30):
    for k in (1, 2, 3):
        Li = k*0.4/hL**2*cd; r = scan(Li); i = r[:,2].argmax(); emax = r[i,2]
        ok = r[r[:,2] > emax-0.1]; smin = r[:,1].min(); slo = ok[:,1].min(); sopt = r[i,1]
        f = lambda St, A=0.2: St*U/(A*L)
        print("%.2f %d %.3f  %.3f %.3f %.3f %.2f | %5.0f %5.0f %5.0f | %4.0f %4.0f %4.0f" % (
            hL, k, Li, smin, slo, sopt, emax, f(smin), f(slo), f(sopt), f(sopt,.15), f(sopt,.25), f(sopt,.30)))
print("closed-form small-angle St_min = sqrt(8Li/pi^3):", [round(np.sqrt(8*0.4/h**2*cd/np.pi**3),3) for h in (0.15,0.2,0.25,0.3)])
