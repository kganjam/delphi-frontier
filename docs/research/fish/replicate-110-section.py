import sys,glob,numpy as np
from PIL import Image
from scipy import ndimage as ndi
UM=150/153.0  # um per px, WT panel scale bar
def mask(f):
    im=np.array(Image.open(f).convert('RGB')).astype(int)[130:980,0:600]
    r,g,b=im[...,0],im[...,1],im[...,2]
    y=(r>120)&(g>110)&(r-b>50)&(g-b>40)
    y=ndi.binary_opening(y,iterations=1)
    return y
def props(pts):
    c=pts.mean(0); d=pts-c; C=d.T@d
    return c,d,C
out=[]
for f in sorted(glob.glob(sys.argv[1]+'/*.png')):
    y=mask(f)
    if y.sum()<500: continue
    lab,n=ndi.label(y)
    allp=np.argwhere(y)[:,::-1].astype(float)*UM
    c,d,C=props(allp); w,v=np.linalg.eigh(C); row=v[:,1]; nrm=v[:,0]
    # row direction = major axis of all yellow; also report
    A=0;Zsep=0;Isep=0;comps=[]
    for k in range(1,n+1):
        p=np.argwhere(lab==k)[:,::-1].astype(float)*UM
        if len(p)<150: continue
        a=len(p)*UM*UM
        ck=p.mean(0); t=(p-ck)@nrm  # distance perpendicular to row
        I=(t**2).sum()*UM*UM; cmax=np.abs(t).max()+UM/2
        s=(p-ck)@row; wid=s.max()-s.min(); th=t.max()-t.min()
        A+=a;Isep+=I;Zsep+=I/cmax;comps.append((round(a),round(wid),round(th)))
    tt=d@nrm; Ifused=(tt**2).sum()*UM*UM; Zf=Ifused/(np.abs(tt).max()+UM/2)
    deq=lambda Z:(32*Z/np.pi)**(1/3)
    out.append((f.split('/')[-1],A,Zsep,Zf,deq(Zsep),deq(Zf),comps))
    print(f.split('/')[-1],'A=%.4f mm2 Zsep=%.2e Zfused=%.2e mm3 d_eq_sep=%.3f d_eq_fused=%.3f mm'%(A/1e6,Zsep/1e9,Zf/1e9,deq(Zsep)/1e3,deq(Zf)/1e3),comps)
