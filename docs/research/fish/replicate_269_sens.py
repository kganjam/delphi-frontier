import sys; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from replicate_269_taxi import *
base=dict(m=0.25e-3,G=G_of(0.3),phi=1.0,CD0=0.08,mode='scaled',cth=0.,dcth=0.,d='prop')
def go(lbl,**kw):
    q=dict(base);q.update(kw);p=(q['m'],q['G'],q['phi'],q['CD0'],q['mode'],q['cth'],q['dcth'],q['d'])
    r=run(p);Uc=ceiling(p)
    s=f"{lbl:34s} {r[0]:8s} Ueq={r[1]:.3f} t_1mg={r[2]:.3f}s strokes={r[2]*52:.1f} x={r[3]:.2f}m"
    if Uc and r[0]!='CLz>1':
        tt,xx=t99(p,Uc); s+=f" | ceil={Uc:.3f} ({Uc/r[4]*100:.1f}%) 99%: {tt:.3f}s {tt*52:.1f} strokes {xx:.2f}m"
    print(s)
    F=forces(1.38,p); print("    at 1.38: net=%.3f mN CLz=%.3f T,Dw,Db,Di,Fs(mN)="%(F[0]*1e3,F[1]),[round(v*1e3,3) for v in F[2]])
go("GENEROUS")
go("GENEROUS, CD const",mode='const')
go("GENEROUS, sigma max (cos1, dcos0.3)",cth=1.,dcth=0.3)
go("GENEROUS, dcos 0.3 only",dcth=0.3)
go("GENEROUS, kappa 0.8",G=0.8*G_of(0.3))
go("GENEROUS, kappa 0.6",G=0.6*G_of(0.3))
go("GENEROUS, Cdb 0.2",G=G_of(0.2))
go("GENEROUS, CD0 0.20",CD0=0.2)
print("--- CENTRAL (defined by the original; run after my derivation)")
go("CENTRAL",G=G_of(0.2),phi=0.5,CD0=0.12,cth=0.5,dcth=0.1)
