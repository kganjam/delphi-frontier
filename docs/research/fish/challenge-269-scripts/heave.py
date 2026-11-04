import math
rw,ra,g=1000.,1.225,9.81
Ub,Af,c,h=1.38,24e-6,6e-3,9e-3; Sc=0.7*c*h; Sl=Sc/2; Sw=192e-6; CLm=1.07; k=1/(math.pi*0.8*5); f=52
def CT_heave(fApp,U,CD):
    St=fApp/U; fs=f*c/U; Us=1/math.sqrt(1+math.pi**2*St**2)
    return 3.52*St**2+3.69*St**2*fs*Us-CD
def CT_pitch(fApp,U,CD): St=fApp/U; return 2.55*St**2-CD
def cal(law,CD,Cdb):
    lo,hi=0.01,3
    for _ in range(100):
        m=(lo+hi)/2
        net=.5*rw*Sc*Ub**2*law(m,Ub,CD)-.5*rw*Cdb*Af*Ub**2
        lo,hi=(lo,m) if net>0 else (m,hi)
    return lo
def ueq(law,fA,CD,m=0.25e-3,phi=1.0,CD0=0.08):
    W=m*g
    def net(U):
        qa=.5*ra*U*U; qw=.5*rw*U*U; CL=min(CLm,W/(qa*Sw)); L=qa*Sw*CL; S=phi*Sl; d=phi*h/2
        CLz=max(0,W-L)/(qw*S); Di=qw*S*CLz**2/(math.pi*0.8*2*d*d/S)
        return qw*S*law(fA,U,CD)-qa*Sw*(CD0+k*CL*CL)-qa*0.3*Af-Di
    lo,hi=0.5,30
    for _ in range(100):
        mm=(lo+hi)/2; lo,hi=(mm,hi) if net(mm)>0 else (lo,mm)
    return lo
for Cdb in (0.1,0.2,0.3):
  for name,law,CD in (('pitch',CT_pitch,0.08),('heave',CT_heave,0.15),('heave CD0.08',CT_heave,0.08)):
    fA=cal(law,CD,Cdb); print('Cdb',Cdb,name,'fApp=%.3f'%fA,'Ueq(const CD)=%.2f'%ueq(law,fA,CD))
