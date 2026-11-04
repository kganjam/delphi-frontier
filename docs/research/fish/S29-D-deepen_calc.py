"""S29-D-D -- deepen S29-D by attacking ITS most sensitive input.

S29-D replaced S29's chain (0.93 x 0.37 = 0.323 KE_exit / E_stored) with the
Conte et al. 2010 value "around 10%" (KE_final / stored beam PE, latch-released
mechanical fish). This script tests how sensitive S29-D's conclusions are to that
number and recomputes them with every value found in this pass.

EVERYTHING PRINTED IS CALCULATED. Nothing here is a measurement by this project.
Inputs are copied from S29 / S29-D unless marked NEW.

Run: python3 docs/research/fish/S29-D-deepen_calc.py
"""
import math

# ------------------------------------------------------------- S29 / S29-D inputs (unchanged)
V = 4.37                       # S28 target exit speed, m/s
V_MASS = 4.37 * math.sqrt(0.40 / 0.25)  # S29's mass-consistent target, 5.53 m/s
M = 0.40e-3                    # body mass, kg
RHO_W, RHO_F = 1000.0, 1050.0
A, CD, S = 24e-6, 0.2, 0.0109
ETA_S, ETA_H = 0.93, 0.37
W = (32.0, 53.0, 81.0)         # J/kg muscle (Mendoza & Azizi 2021, via S29)
F_ONE, F_ALL = 0.30, 0.60
CHAIN_CONTE = 0.10             # Conte et al. 2010 abstract: "around 10%"

# ------------------------------------------------------------- NEW inputs (this pass)
# Watts 2006 MIT/WHOI SM thesis (chain pickerel mechanical fish), search-summary:
#   efficiency 11 %, peak velocity 0.96 m/s, "averaged maximum" velocity 0.80 m/s,
#   peak acceleration 48 m/s^2, beam 1095 spring steel cut to 14.75 in.
WATTS_ETA = 0.11
WATTS_V_PEAK, WATTS_V_AVG = 0.96, 0.80
WATTS_BEAM_L = 14.75 * 0.0254  # m
# Feng et al. 2011 IMECE2011-65035, SERVO-DRIVEN pike robot, search-summary: ~12 %,
#   peak velocity 0.09 m/s. Definition of efficiency: unknown.
FENG_ETA = 0.12
NU = 1.0e-6

line = "-" * 78


def h(t):
    print("\n" + line + "\n" + t + "\n" + line)


def sf_chain(chain, w=53.0, f=F_ONE, v=V):
    """Shortfall with chain = KE_exit / E_stored (drag and wake inside the chain), S29-D form."""
    return 0.5 * v ** 2 / (f * w * chain)


ke = 0.5 * V ** 2
wd = 0.5 * RHO_W * CD * A * V ** 2 * S / 2 / M
chain_s29 = ke * ETA_S * ETA_H / (ke + wd)

h("0. Reproduce S29-D section 4")
for c, tag in [(chain_s29, "S29 implied"), (CHAIN_CONTE, "Conte 0.10")]:
    print(f"{tag:12s} chain {c:.3f}: shortfall w32/53/81 = "
          + " / ".join(f"{sf_chain(c, w=w):.2f}" for w in W)
          + f"; all muscle @53 {sf_chain(c, 53, F_ALL):.2f} @81 {sf_chain(c, 81, F_ALL):.2f}"
          + f"; 5.53 m/s @53 {sf_chain(c, 53, v=V_MASS):.2f}")

h("1. Sensitivity of S29-D's conclusions to each input, x2 and /2 (central: chain 0.10, w 53, f 0.30)")
base = sf_chain(CHAIN_CONTE)
print(f"central shortfall {base:.3f}")
for name, fn in [("chain (0.10)", lambda k: sf_chain(CHAIN_CONTE * k)),
                 ("w (53 J/kg)", lambda k: sf_chain(CHAIN_CONTE, w=53 * k)),
                 ("f (0.30)", lambda k: sf_chain(CHAIN_CONTE, f=min(F_ONE * k, 1.0))),
                 ("V (4.37)", lambda k: sf_chain(CHAIN_CONTE, v=V * k))]:
    print(f"{name:14s} x2 -> {fn(2):6.2f}   /2 -> {fn(0.5):6.2f}")
print("f is physically capped at 0.60 (x2.00); V is the specification, not an input.")

h("2. Flip points: the chain value at which each S29-D claim fails")
claims = [
    ("all-muscle break-even reappears (f 0.60, w 81)", 0.5 * V ** 2 / (F_ALL * 81)),
    ("all-muscle break-even reappears (f 0.60, w 53)", 0.5 * V ** 2 / (F_ALL * 53)),
    ("one-side closes (f 0.30, w 81)", 0.5 * V ** 2 / (F_ONE * 81)),
    ("one-side closes (f 0.30, w 53)", 0.5 * V ** 2 / (F_ONE * 53)),
    ("'narrow' (<2x) restored (f 0.30, w 53)", 0.5 * V ** 2 / (2 * F_ONE * 53)),
    ("fish-tendon spring <= 25% body (E 1.2 GPa, 2% strain)", None),
]
v_body = M / RHO_F
u_tuna = 0.5 * 1.2e9 * 0.02 ** 2
for name, c in claims:
    if c is None:
        c = 0.5 * V ** 2 * M / (0.25 * v_body * u_tuna)
    print(f"{name:56s} chain >= {c:.3f}  (= Conte x {c/CHAIN_CONTE:.2f})")

h("3. Improve the input: what the second device (Watts 2006) implies, by definition of 'final' KE")
r = (WATTS_V_PEAK / WATTS_V_AVG) ** 2
print(f"(v_peak/v_avg)^2 = ({WATTS_V_PEAK}/{WATTS_V_AVG})^2 = {r:.3f}")
print(f"if Watts's 11% used v_avg 0.80 m/s, the PEAK-KE chain would be 0.11 x {r:.3f} = {WATTS_ETA*r:.3f}")
print(f"if Watts's 11% used v_peak 0.96 m/s, the peak-KE chain is 0.11")
print(f"if instead it used v_peak and S29 needs the mean, 0.11 / {r:.3f} = {WATTS_ETA/r:.3f} (not S29's need)")
print("S29 needs KE at the instant of water exit, i.e. the PEAK, so the relevant range is 0.10-0.158.")

h("4. Scale of the analogue (Re), conditional on body length ~ beam length (ASSUMED)")
print(f"Watts beam {WATTS_BEAM_L*100:.1f} cm at 0.96 m/s: Re = {0.96*WATTS_BEAM_L/NU:.2e}")
print(f"zebrafish 3.0 cm at 4.37 m/s: Re = {4.37*0.03/NU:.2e}; at 1.38 m/s: {1.38*0.03/NU:.2e}")
print(f"length ratio device/zebrafish = {WATTS_BEAM_L/0.03:.1f}x")

h("5. Recompute S29-D's conclusions with the improved chain range")
for c, tag in [(0.10, "Conte 0.10"), (0.11, "Watts 0.11 as reported"), (0.12, "Feng servo 0.12 (not a spring)"),
               (WATTS_ETA * r, "Watts at peak-KE 0.158"), (chain_s29, "S29 implied 0.323")]:
    print(f"{tag:32s}: one-side w32/53/81 = "
          + " / ".join(f"{sf_chain(c, w=w):.2f}" for w in W)
          + f" | all @53 {sf_chain(c, 53, F_ALL):.2f} @81 {sf_chain(c, 81, F_ALL):.2f}"
          + f" | 5.53 m/s @53 {sf_chain(c, 53, v=V_MASS):.2f}")
for c in (0.10, WATTS_ETA * r):
    stored = 0.5 * V ** 2 / c * M
    print(f"chain {c:.3f}: stored {stored*1e3:.1f} mJ; tuna tendon spring "
          f"{stored/(0.5*1.2e9*0.02**2)/v_body*100:.0f}-{stored/(0.5*0.65e9*0.02**2)/v_body*100:.0f}% body; "
          f"one-side contractions at w53 = {math.ceil(stored/(F_ONE*53*M))}")

h("6. Internal loss Conte's device would need for S29's chain to be right")
need_retained = CHAIN_CONTE / (ETA_H * ke / (ke + wd))
print(f"0.10 / (0.37 x KE/(KE+drag)) = {need_retained:.3f} retained -> {100*(1-need_retained):.0f}% lost internally")
need_retained_hi = WATTS_ETA * r / (ETA_H * ke / (ke + wd))
print(f"with the 0.158 upper chain: {need_retained_hi:.3f} retained -> {100*(1-need_retained_hi):.0f}% lost internally")
