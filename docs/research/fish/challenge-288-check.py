import numpy as np
rho,g,m=1.2,9.81,0.4e-3
# central case by hand, independent
b,c,L,CL=0.055,0.011,0.031,0.75
S=b*c;AR=b*b/S;a=2*np.pi*AR/(AR+2)
V=np.sqrt(2*m*g/(rho*S*CL));q=0.5*rho*V*V
print("S",S,"AR",AR,"a",a,"V",V,"q",q,"Re",V*c/1.5e-5)
Iyy=m*L**2/12*1.15
Za=q*S*a/(m*V)   # 1/s
print("Iyy",Iyy,"Za/mV",Za)
for SM in [0.02,0.05,0.10,0.15,0.25]:
  Ma=q*S*c*a*SM/Iyy
  for Cmq in [0,-1.6,-6]:   # per qhat=qc/2V ; 0=author's undamped, -1.6~thin-wing, -6~wing+tail
    Mq=-Cmq*q*S*c*(c/(2*V))/Iyy
    wn2=Ma+Za*Mq; wn=np.sqrt(wn2); z=(Za+Mq)/(2*wn)
    fd=wn*np.sqrt(max(0,1-z*z))/2/np.pi
    print(f"SM {SM:.2f} Cmq {Cmq:5.1f}  f_undamped {np.sqrt(Ma)/2/np.pi:4.2f} fn {wn/2/np.pi:4.2f} zeta {z:4.2f} fd {fd:4.2f}")
# roll
h,w,mf=0.2*L,0.1*L,0.05*m
Ixx=(m-mf)*(h*h+w*w)/12+mf*b*b/12
Lp=rho*V*S*a*b*b/24
print("Ixx",Ixx,"Lp",Lp,"tau ms",Ixx/Lp*1e3)
# radius of gyration sensitivity (fish taper: k/L 0.20-0.29)
for k in [0.20,0.25,0.289]:
  I=m*(k*L)**2; print("k/L",k,"f@SM0.15",np.sqrt(q*S*c*a*0.15/I)/2/np.pi)
print("inertia factor to bring 5Hz->3Hz",(5/3)**2,"->2Hz",(5/2)**2)
# slow modes the claim did not compute
print("phugoid period s (Lanchester)",np.pi*np.sqrt(2)*V/g)
