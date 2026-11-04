m_fish=0.400  # g
mstar=0.039; lo=0.0085; hi=0.173  # g
print("central ratio", m_fish/mstar)
print("ratio at hi m*", m_fish/hi, " at lo m*", m_fish/lo)
print("linear overshoot (ratio^(1/3))", (m_fish/mstar)**(1/3))
# map m* band to standard length, isometric, ref 0.400 g at 33 mm SL
L=33.0
for m in (lo,mstar,hi):
    print(f"m*={m*1000:7.1f} mg -> SL {L*(m/m_fish)**(1/3):5.1f} mm")
# sensitivity of headline ratio to zebrafish adult mass band 0.28-0.45 g
for mf in (0.28,0.34,0.45):
    print(f"adult mass {mf} g -> ratio {mf/mstar:.1f}x, linear {(mf/mstar)**(1/3):.2f}x")
# aerial drag-to-weight for 0.4 g, L=33mm, v=2 m/s
rho=1.2; Cd=0.2; A=1.5e-5; v=2.0; g=9.81
print("drag/weight at takeoff:", 0.5*rho*Cd*A*v**2/(0.4e-3*g))
# work-limited specific energy -> takeoff speed, Sutton numbers
for e,label in ((15.0,"muscle 15 J/kg"),(4.2,"LaMSA 4.2 J/kg")):
    print(label, "v =", (2*e)**0.5, "m/s ; ballistic height v^2/2g =", e/g, "m")
