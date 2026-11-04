# Independent re-derivation for claim 194 (calculation, not observation).
# Fractional reduction of effective downward acceleration in leap ascent
# = L/W, with L = 0.5*rho*V^2*S*CL acting ~upward (normal to path), W = m g.
import math
rho, g = 1.225, 9.81
CL = 1.07                     # project-derived CL_max; also tried 0.8
for V in (0.45, 1.38):
  for m in (0.25e-3, 0.40e-3):
    for S_mm2 in (40, 80, 196):
      for cl in (0.8, CL):
        LW = 0.5*rho*V**2*(S_mm2*1e-6)*cl/(m*g)
        print(f"V={V} m={m*1e3:.2f}g S={S_mm2}mm2 CL={cl}: L/W exit={100*LW:5.1f}%  "
              f"apex(45deg)={100*LW*math.cos(math.radians(45))**2:4.1f}%  "
              f"mean over vertical ascent={100*LW/3:4.1f}%")

# Vertical NET aerodynamic force / W along a 45 deg ascent (case: S=196 mm2, m=0.25 g, V0=1.38 m/s).
# Path angle gamma from 45 deg at exit to 0 at apex. Lift is normal to the path (vertical part L cos g);
# drag is along -velocity (vertical part -D sin g, i.e. it ADDS to downward deceleration while climbing).
# Wing CD = CD0 + CL^2/(pi*0.8*AR), CD0=0.08, AR=5; body CD 0.3 on 24 mm2 frontal (generic choices).
print()
m, S, cl, AR, CD0 = 0.25e-3, 196e-6, 1.07, 5, 0.08
CDw = CD0 + cl**2/(math.pi*0.8*AR); W = m*g
for gam_deg, V in ((45, 1.38), (0, 1.38*math.cos(math.radians(45)))):
    q = 0.5*rho*V**2; gam = math.radians(gam_deg)
    L = q*S*cl; D = q*S*CDw + q*24e-6*0.3
    print(f"gamma={gam_deg:2d} V={V:.3f}: L/W={L/W*100:4.1f}%  vertical L/W={L*math.cos(gam)/W*100:4.1f}%  "
          f"vertical drag/W={-D*math.sin(gam)/W*100:5.2f}%  NET reduction={100*(L*math.cos(gam)-D*math.sin(gam))/W:4.1f}%")
