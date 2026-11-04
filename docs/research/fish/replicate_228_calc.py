"""Independent re-derivation for claim 228 (S29 launch-energy shortfall).
Shortfall = (energy the spring must store per kg body) / (energy one muscle
contraction can put into the spring per kg body). All values are calculated."""
import math, random
m, V = 0.40e-3, 4.37                     # kg, m/s  (S29/S28 inputs)
KE = 0.5 * V**2                          # J per kg body
print(f"KE = 0.5*{V}^2 = {KE:.3f} J/kg body ({KE*m*1e3:.3f} mJ at 0.40 g)")

def shortfall(W, f, eta, ke=KE):
    return (ke / eta) / (W * f)

# point cases
W_fish = 142.7 / 15                      # J/kg muscle per cycle, inferred
print(f"W_fish = 142.7/15 = {W_fish:.2f} J/kg muscle")
cases = {
  "central (W=24, f=0.45, eta=0.7)": (24, 0.45, 0.7),
  "frog plantaris (W=31, f=0.45, eta=0.7)": (31, 0.45, 0.7),
  "fish cycle work (W=9.51, f=0.45, eta=0.7)": (W_fish, 0.45, 0.7),
  "optimistic (W=60, f=0.60, eta=0.9)": (60, 0.60, 0.9),
  "pessimistic (W=9.51, f=0.30, eta=0.5)": (W_fish, 0.30, 0.5),
}
for k, (W, f, e) in cases.items():
    print(f"{k:45s} req={KE/e:6.2f}  avail={W*f:6.2f}  ratio={shortfall(W,f,e):.2f}x")

random.seed(228)
def lu(a, b): return math.exp(random.uniform(math.log(a), math.log(b)))
for label, ke in (("4.37 m/s", KE), ("5.53 m/s", 0.5*5.53**2)):
    xs = sorted(shortfall(lu(W_fish, 60), random.uniform(0.30, 0.60),
                          random.uniform(0.5, 0.9), ke) for _ in range(200000))
    q = lambda p: xs[int(p*len(xs))]
    print(f"MC {label}: median {q(.5):.2f}x  5-95% {q(.05):.2f}-{q(.95):.2f}x  "
          f"P(>=1)={sum(x>=1 for x in xs)/len(xs):.2f}  P(>=10)={sum(x>=10 for x in xs)/len(xs):.3f}")

# Post-comparison sensitivity (added AFTER reading S29 sec. 5; not part of the blind estimate)
print("--- post-comparison sensitivity ---")
for W in (22, 37, 53, 81):          # Mendoza & Azizi 2021 species means / OS range
    for f in (0.30, 0.45):
        for eta in (0.7, 0.93*0.37):
            print(f"W={W:3d} f={f:.2f} eta={eta:.3f} -> {shortfall(W,f,eta):.2f}x")
