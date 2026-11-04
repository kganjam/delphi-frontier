# Independent re-derivation (my own code, from the equations as stated in S32 sec.1 and inputs in sec.2)
import math
rw,ra,nu,g=1000.,1.225,1e-6,9.81
c6,CDf=2.55,0.08
Ub,Af,c,h=1.38,24e-6,6e-3,9e-3
Sc=0.7*c*h; Sl=Sc/2; Sw=192e-6; CLm=1.07; k=1/(math.pi*0.8*5)
def CD(U,mode):
    if mode=='const':return CDf
    Re=U*c/nu
    return CDf*math.sqrt(9560/Re) if Re>9560 else (CDf*math.sqrt(4780/Re) if Re<4780 else CDf)
def Gcal(Cdb,mode,Ucal=Ub):  # whole-fin thrust = body drag at burst peak
    return Cdb*Af/Sc*Ucal**2 + CD(Ucal,mode)*Ucal**2
def net(U,m,phi,G,mode,CD0,cth,dcos,Cdb_air=0.3):
    W=m*g; qa=.5*ra*U*U; qw=.5*rw*U*U
    CL=min(CLm,W/(qa*Sw)); L=qa*Sw*CL
    S=phi*Sl; d=phi*h/2
    need=max(0,W+2*.072*c*cth-L); CLz=need/(qw*S)
    Di=qw*S*CLz**2/(math.pi*0.8*2*d*d/S)
    T=.5*rw*S*(G-CD(U,mode)*U*U)
    return T-qa*Sw*(CD0+k*CL*CL)-qa*Cdb_air*Af-Di-2*.072*c*dcos, CLz
def run(m,phi,G,mode,CD0,cth,dcos,U0=1.38,f=52,dt=1e-5):
    U=U0;x=0;t=0;Vto=math.sqrt(2*m*g/(ra*Sw*CLm))
    hist=[]
    while t<5:
        F,CLz=net(U,m,phi,G,mode,CD0,cth,dcos)
        if CLz>1: return 'support fails',U,t,x,Vto,hist
        a=F/m
        if abs(a)<1e-3*g and t>0.01: return 'stall',U,t,x,Vto,hist
        if U>=Vto: return 'glide',U,t,x,Vto,hist
        hist.append((t,U,x)); U+=a*dt; x+=U*dt; t+=dt   # semi-implicit Euler (deliberately different integrator)
    return 'tmax',U,t,x,Vto,hist
def ueq(*a):
    lo,hi=0.5,30
    for _ in range(100):
        mid=(lo+hi)/2
        lo,hi=(mid,hi) if net(mid,*a)[0]>0 else (lo,mid)
    return lo
S={'GEN':(0.25e-3,1.0,0.3,'scaled',0.08,0,0),'CEN':(0.25e-3,0.5,0.2,'scaled',0.12,.5,.1),'STI':(0.40e-3,0.25,0.1,'const',0.20,1,.3)}
for n,(m,phi,Cdb,mode,CD0,cth,dcos) in S.items():
    G=Gcal(Cdb,mode)
    o,U,t,x,Vto,hist=run(m,phi,G,mode,CD0,cth,dcos)
    # strokes to within 1% of final
    t99=next((tt for tt,uu,xx in hist if uu>=0.99*U),None) if hist else None
    x99=next((xx for tt,uu,xx in hist if uu>=0.99*U),None) if hist else None
    print(n,'G=%.3f'%G,o,'U=%.3f'%U,'%.1f%%Vto'%(100*U/Vto),'t=%.3f s strokes=%.1f x=%.2f m'%(t,52*t,x),
          '| 99%%: t=%s strokes=%s x=%s'%(None if t99 is None else round(t99,3),None if t99 is None else round(52*t99,1),None if x99 is None else round(x99,2)))
# ceiling formula check
for fA in (0.33,0.45):
    for cd in (0.08,0.059):
        print('fA=%.2f CD=%.3f Umax=%.2f'%(fA,cd,fA*math.sqrt(c6/cd)))
# Attack: drag-augmented body Cd in calibration (swimming drag > rigid drag)
print('-- calibration body Cd sweep (GENEROUS otherwise) --')
for Cdb in (0.3,0.45,0.6,0.69,0.9):
    G=Gcal(Cdb,'scaled'); print('Cdb %.2f G %.3f Ueq %.2f'%(Cdb,G,ueq(0.25e-3,1.0,G,'scaled',0.08,0,0)))
# Attack: calibration speed (1.38 m/s input)
print('-- burst speed sweep (Cdb 0.3, scaled) --')
for Ucal in (1.0,1.38,1.8,2.0):
    G=Gcal(0.3,'scaled',Ucal); print('Ub %.2f Ueq %.2f'%(Ucal,ueq(0.25e-3,1.0,G,'scaled',0.08,0,0)))
# Attack: C_D extrapolation exponent (turbulent-like Re^-0.2 vs laminar Re^-0.5) at lobe Re ~1.7e4
for ex in (0.0,0.2,0.5,1.0):
    cd=0.08*(9560/17000)**ex; print('exp %.1f CD@Re1.7e4 %.3f'%(ex,cd))
print('-- low-end calibration speeds (Cdb 0.3 & 0.2, scaled), and outcome from 1.38 exit --')
for Ucal in (0.46,0.55,0.63,0.8,1.0):
  for Cdb in (0.3,0.2):
    G=Gcal(Cdb,'scaled',Ucal); o=run(0.25e-3,1.0,G,'scaled',0.08,0,0)
    print('Ub %.2f Cdb %.1f Ueq %.2f  from 1.38: %s U=%.2f'%(Ucal,Cdb,ueq(0.25e-3,1.0,G,'scaled',0.08,0,0),o[0],o[1]))
