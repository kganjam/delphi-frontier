import numpy as np
rng=np.random.default_rng(1);N=200000
rho=1.2;g=9.81;m=0.4e-3
L=rng.uniform(0.028,0.035,N)          # body length m
b=rng.uniform(0.04,0.07,N)            # engineered fin span m
c=rng.uniform(0.008,0.014,N)          # mean chord m
S=b*c;AR=b**2/S
a=2*np.pi*AR/(AR+2)                   # lift slope /rad (Helmbold-like)
CL=rng.uniform(0.5,1.0,N)
V=np.sqrt(2*m*g/(rho*S*CL))
q=0.5*rho*V**2
SM=rng.uniform(0.05,0.25,N)           # static margin, fraction of chord
Iyy=m*L**2/12*rng.uniform(1.0,1.3,N)  # body rod + fin/tail add-on
Malpha=q*S*c*a*SM
fsp=np.sqrt(Malpha/Iyy)/(2*np.pi)
# roll: body laterally compressed h~0.2L,w~0.1L, plus fins mass fraction 3-8%
h=0.2*L;w=0.1*L;mf=m*rng.uniform(0.03,0.08,N)
Ixx=(m-mf)*(h**2+w**2)/12+mf*b**2/12
Lp=rho*V*S*a*b**2/24                  # strip theory, rectangular
tau=Ixx/Lp
for n,x in [("V m/s",V),("f_pitch Hz",fsp),("tau_roll ms",tau*1e3),("Ixx",Ixx),("Iyy",Iyy)]:
  print(n,np.percentile(x,[5,50,95]))
# point case
