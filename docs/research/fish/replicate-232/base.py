import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sys,struct,numpy as np
from u3dwalk import load,s
def basemesh(fn):
    b,out=load(fn)
    for d,t,P,ds in out:
        if t==0xFFFFFF3B:
            name,q=s(b,P)
            chain,F,Np,Nn,Nd,Ns,Nt=struct.unpack_from('<7I',b,q); q+=28
            pos=np.frombuffer(b,dtype='<f4',count=3*Np,offset=q).reshape(-1,3).copy(); q+=12*Np
            return dict(b=b,P=P,ds=ds,F=F,Np=Np,counts=(Nn,Nd,Ns,Nt),pos=pos,face_start=q)
if __name__=='__main__':
    for fn in sys.argv[1:]:
        m=basemesh(fn)
        if m is None: print(fn,'no base'); continue
        p=m['pos']; print(fn,'F',m['F'],'Np',m['Np'],m['counts'],'min',p.min(0).round(3),'max',p.max(0).round(3),'ext',(p.max(0)-p.min(0)).round(3),'face bytes',m['P']+m['ds']-m['face_start'])
