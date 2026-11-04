import sys,numpy as np
sys.path.insert(0,sys.argv[1]); from slicer import slice_mesh,load
from secs import section
P,T=load(sys.argv[2]); k=0.968
ylo,yhi=map(float,sys.argv[3].split(',')); 
for x in map(float,sys.argv[4].split(',')):
    r=section(P,T,0,x,{1:(ylo,yhi),2:(0,40000)},1)  # no z crop: list every closed loop in y band
    out=[]
    for l in r['loops']:
        a=abs(0.5*(l[:-1,0]*np.roll(l[:-1,1],-1)-np.roll(l[:-1,0],-1)*l[:-1,1]).sum())*k*k/1e6
        if a<0.003: continue
        out.append(f"A={a:.4f} y[{l[:,0].min()*k/1e3:.2f},{l[:,0].max()*k/1e3:.2f}] z[{l[:,1].min()*k/1e3:.2f},{l[:,1].max()*k/1e3:.2f}]")
    print(x, 'cut',r['cut'],'\n   '+'\n   '.join(out))
