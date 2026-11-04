"""Independent re-derivation for claim 72 (S6-D). Calculation only; nothing measured."""
import itertools, math
g = 9.81
def ei_req(m, share, n, L, dl):
    F = m*g*share/2/n          # lift per ray, one pectoral fin, uniform load
    return F*L**2/(8*dl)       # cantilever, uniform load: delta = F L^3/(8EI)
nom = dict(m=0.15, share=0.8, n=14, L=0.11, dl=0.10)
print("nominal F per ray [N] =", nom['m']*g*nom['share']/2/nom['n'])
print("nominal EI_req [N m^2] = %.3e" % ei_req(**nom))
grid = dict(m=[0.10,0.20], share=[0.7,0.9], n=[16,12], L=[0.09,0.13], dl=[0.2,0.05])
vals = [ei_req(*c) for c in itertools.product(*grid.values())]
print("corner range EI_req: %.2e .. %.2e" % (min(vals), max(vals)))
E = 1.34e9
for d in [0.2e-3,0.4e-3,1.0e-3]:
    I = math.pi*(d/2)**4/4
    print("solid rod d=%.1f mm, E=1.34 GPa: EI=%.2e" % (d*1e3, E*I))
d_need = (4*ei_req(**nom)/E/math.pi)**0.25*2
print("solid diameter needed at E=1.34 GPa: %.2f mm" % (d_need*1e3))
for name, EI in [("Flammang2013 abstract 565e-6", 565e-6), ("Aiello/Puri max 1.5109e-6", 1.5109e-6)]:
    print(name, "EI/EI_req = %.3g" % (EI/ei_req(**nom)), " range %.3g..%.3g" % (EI/max(vals), EI/min(vals)))
