# Arithmetic re-checks for the 10 sampled challenge documents. Every output is a CALCULATION.
from math import sqrt, pi, cos
phi = (1 + 5**.5) / 2
print('c62  golden angle 360/phi^2 =', 360/phi**2, '| Lucas 360/(2+phi) =', 360/(2+phi))
FF, p0, f = (.65, .77), (.173, .26), (1.74, 2.05)
print('c109 shortfall', FF[0]/(p0[1]*f[1]), FF[1]/(p0[0]*f[0]), '| break-even f', FF[0]/p0[1], FF[1]/p0[0])
b = 1.98*.0403**3/3
print('c135 k-bound kL^3/3 =', b, '| isometric x(120/40.3)^4 =', b*(.12/.0403)**4)
L = .5*1.225*1.38**2*192e-6*1.07; W = .25e-3*9.81
print('c190 L/W launch', L/W, '| apex (45 deg, no drag)', L/W*cos(pi/4)**2)
W = .4e-3*9.81; S = 2*W/(1.2*9*.78); s = sqrt(9*S)/2 - .0025; M = 3*(W/2)*(4/(3*pi))*s
d = (32*M/(pi*62.6e6))**(1/3)
print('c221 M', M, '| d_req mm', d*1e3, '| (d/0.163mm)^3', (d*1e3/.163)**3)
print('c140 sqrt(gR) R=1 m', sqrt(9.81), '| R=0.5 m', sqrt(9.81*.5))
print('c2   5.84/0.548 =', 5.84/.548, '| squared', (5.84/.548)**2)
Lp = 3*W/2
print('c201 lift/fin', Lp, '| arm mm', 1.1e-4/Lp*1e3, '| air area cm2', Lp/(.5*1.2*9*.78)*1e4)
print('CP 95% lower bound, 10/10:', .025**(1/10), '| 27/27:', .025**(1/27))
