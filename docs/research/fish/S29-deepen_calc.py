"""S29-D -- deepen S29 (LaMSA launch energy) by attacking its weakest input.

Every number in docs/research/fish/S29-deepen.md is printed by this script.
Everything printed is CALCULATED. Nothing here is a measurement.
Inputs are copied from S29 (docs/research/fish/S29_launch_energy.py on branch
claude/s29-launch-energy-2iuixr, commit 44ed2195) unless marked NEW.

Run: python3 docs/research/fish/S29-deepen_calc.py
"""
import math

# ------------------------------------------------------------------ S29 inputs (unchanged)
V = 4.37            # S28 target exit speed, m/s (derived by S28 at 0.25 g)
V_MASS = 4.37 * math.sqrt(0.40 / 0.25)   # S29's own mass-consistent target, 5.53 m/s
M = 0.40e-3         # body mass, kg
RHO_W, RHO_F = 1000.0, 1050.0
A = 24e-6           # frontal area, m^2 (S28)
CD, S = 0.2, 0.0109 # assumed Cd and stroke length (S29 central)
ETA_S = 0.93        # spring return (Ker 1981, via S29)
ETA_H = 0.37        # pike C-start hydromechanical efficiency (Frith & Blake, via S29)
W = (32.0, 53.0, 81.0)  # J/kg muscle stored in series tendon (Mendoza & Azizi 2021, via S29)
F_ONE, F_ALL = 0.30, 0.60

# ------------------------------------------------------------------ NEW inputs found in S29-D
# Each is a value reported by the cited authors; none was measured by this project.
ETA_H_PIKE_RANGE = (0.16, 0.39)   # Frith & Blake 1995 JEB 198:1863, abstract: "range from 0.16 to 0.39",
                                  # CALCULATED by the authors from the Weihs model on filmed kinematics
ETA_H_CARP_RANGE = (0.19, 0.38)   # Wakeling et al. 2000 AJP 279:R657, abstract: rises 0.19 -> 0.38 with
                                  # acute temperature 10 -> 20 C; carp 9.5-69 mm. Model-derived.
CHAIN_CONTE = 0.10   # Conte et al. 2010 Bioinsp. Biomim. 5:035004, abstract: final KE / stored beam PE
                     # "around 10%" for a latch-released (line-cut) pre-bent elastic mechanical fish. MEASURED by the authors.
CHAIN_WATTS = 0.11   # Watts, MIT thesis, chain pickerel mechanical fish, 11% -- search-summary only

line = "-" * 78


def h(t):
    print("\n" + line + "\n" + t + "\n" + line)


ke = 0.5 * V ** 2                                   # J/kg body
wd = 0.5 * RHO_W * CD * A * V ** 2 * S / 2 / M      # drag work during stroke, J/kg body
need_body = ke + wd                                 # J/kg body, S29 central


def shortfall(eta_h=ETA_H, w=53.0, f=F_ONE, eta_s=ETA_S, v=V, cd=CD):
    k = 0.5 * v ** 2
    d = 0.5 * RHO_W * cd * A * v ** 2 * S / 2 / M
    return (k + d) / (f * w * eta_s * eta_h)


def shortfall_chain(chain, w=53.0, f=F_ONE, v=V):
    """chain = KE_exit / E_stored, the quantity Conte et al. measured (drag and wake losses inside it)."""
    return 0.5 * v ** 2 / (f * w * chain)


h("0. Reproduce S29 central")
print(f"KE {ke:.3f} J/kg, drag work {wd:.3f} J/kg, need at body {need_body:.3f} J/kg")
print(f"S29 shortfall at w=32/53/81: " + " / ".join(f"{shortfall(w=w):.3f}" for w in W))

h("1. Sensitivity: shortfall when each input is x2 or /2 (all else at S29 central = 1.859)")
base = shortfall()
rows = [
    ("eta_h (0.37)", lambda k: shortfall(eta_h=ETA_H * k)),
    ("w muscle work (53 J/kg)", lambda k: shortfall(w=53 * k)),
    ("f muscle fraction (0.30)", lambda k: shortfall(f=F_ONE * k)),
    ("eta_spring (0.93)", lambda k: shortfall(eta_s=ETA_S * k)),
    ("Cd (0.2)", lambda k: shortfall(cd=CD * k)),
    ("V target (4.37 m/s)", lambda k: shortfall(v=V * k)),
]
print(f"{'input':28s} {'x2':>8} {'/2':>8} {'elasticity':>11} {'factor that flips (<1)':>24}")
for name, fn in rows:
    up, dn = fn(2.0), fn(0.5)
    el = math.log(up / base) / math.log(2.0)
    print(f"{name:28s} {up:8.3f} {dn:8.3f} {el:11.2f}", end="")
    if "V target" in name:
        print(f"   V / {math.sqrt(base):.3f} (need and drag both scale with V^2)")
    elif "Cd" in name:
        print("   cannot flip: drag is 6.5% of need")
    elif "spring" in name:
        print(f"   needs eta_s = {ETA_S*base:.2f} > 1, impossible")
    else:
        print(f"   x{base:.3f}")
print("Physical ceilings: f <= 0.60 (all skeletal muscle) so f can rise at most x2.00;"
      " eta_s <= 1 so at most x1.08.")

h("2. Break-even eta_h for one-side muscle at each w (challenge 227 reproduced)")
for w in W:
    print(f"w {w:4.0f} J/kg: break-even eta_h = {need_body/(F_ONE*w*ETA_S):.3f}")

h("3. Recompute with every eta_h value found (eta_s 0.93 kept; S29 chain)")
for tag, eh in [("pike low (F&B 1995)", ETA_H_PIKE_RANGE[0]), ("carp 10 C (Wakeling 2000)", ETA_H_CARP_RANGE[0]),
                ("S29 pike central", ETA_H), ("carp 20 C (Wakeling 2000)", ETA_H_CARP_RANGE[1]),
                ("pike high (F&B 1995)", ETA_H_PIKE_RANGE[1])]:
    print(f"{tag:28s} eta_h {eh:.2f}: shortfall w=32/53/81 = "
          + " / ".join(f"{shortfall(eta_h=eh, w=w):.2f}" for w in W)
          + f" ; all muscle @81 = {shortfall(eta_h=eh, w=81, f=F_ALL):.2f}")

h("4. The chain S29 implies vs the chain measured on a spring-released fish")
chain_s29 = ke * ETA_S * ETA_H / need_body        # KE_exit / E_stored implied by S29
print(f"S29 implied KE/E_stored = 0.93*0.37*KE/(KE+drag) = {chain_s29:.3f}")
print(f"Conte 2010 measured ~{CHAIN_CONTE:.2f}; ratio S29/Conte = {chain_s29/CHAIN_CONTE:.2f}x")
print(f"Watts thesis ~{CHAIN_WATTS:.2f}; ratio S29/Watts = {chain_s29/CHAIN_WATTS:.2f}x")
print(f"eta_h equivalent to Conte if eta_s 0.93 and drag as S29: "
      f"{CHAIN_CONTE*need_body/(ke*ETA_S):.3f}")

h("5. Recompute S29 with the measured spring-release chain")
for chain, tag in [(chain_s29, "S29 implied"), (CHAIN_WATTS, "Watts 0.11"), (CHAIN_CONTE, "Conte 0.10")]:
    stored = 0.5 * V ** 2 / chain
    print(f"{tag:12s} chain {chain:.3f}: stored {stored:6.2f} J/kg body = {stored*M*1e3:5.2f} mJ; shortfall "
          + " / ".join(f"w{w:.0f} {shortfall_chain(chain, w=w):.2f}" for w in W)
          + f"; ALL muscle @53 {shortfall_chain(chain, w=53, f=F_ALL):.2f}, @81 {shortfall_chain(chain, w=81, f=F_ALL):.2f}"
          + f"; at 5.53 m/s @53 {shortfall_chain(chain, w=53, v=V_MASS):.2f}")
# muscle fraction needed with Conte chain
for w in W:
    f_req = (0.5 * V ** 2 / CHAIN_CONTE) / w
    print(f"Conte chain, w {w:.0f}: muscle fraction of body needed = {f_req*100:.0f}%")

h("6. Knock-on: spring volume and loading contractions with Conte chain")
stored_conte = 0.5 * V ** 2 / CHAIN_CONTE * M        # J
v_body = M / RHO_F
for name, u in [("tendon 100 MPa, E 1.65 GPa", 100e6 ** 2 / (2 * 1.65e9)),
                ("tendon 75 MPa, E 1.65 GPa", 75e6 ** 2 / (2 * 1.65e9)),
                ("tendon 50 MPa, E 1.65 GPa", 50e6 ** 2 / (2 * 1.65e9)),
                ("tuna tendon E 1.2 GPa, 2% strain", 0.5 * 1.2e9 * 0.02 ** 2),
                ("tuna tendon E 0.65 GPa, 2% strain", 0.5 * 0.65e9 * 0.02 ** 2)]:
    vol = stored_conte / u
    print(f"{name:36s} u {u/1e6:5.2f} MJ/m3: {vol*1e9:6.1f} mm3 = {vol/v_body*100:5.1f}% body")
for w in W:
    per = F_ONE * w * M  # J stored per one-side contraction
    print(f"w {w:.0f}: one-side contractions to fill the spring = {stored_conte/per:.2f} -> {math.ceil(stored_conte/per)}")

h("7. Reynolds numbers (context for transfer)")
nu = 1.0e-6
print(f"zebrafish 30 mm at 4.37 m/s: Re = {4.37*0.030/nu:.2e}; at 1.38 m/s: {1.38*0.030/nu:.2e}")
print("Conte mechanical fish at 1.2 m/s: length not in abstract -> Re unknown")
