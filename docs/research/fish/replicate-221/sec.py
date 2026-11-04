import sys,glob,numpy as np
from PIL import Image
from scipy import ndimage as nd
UM=150/152.0  # um per px (WT panel scale bar, measured 152 px)
def props(m):
    ys,xs=np.nonzero(m); x=(xs-xs.mean())*UM; y=(ys-ys.mean())*UM
    a=UM*UM; A=len(xs)*a
    Ixx=(y*y).sum()*a; Iyy=(x*x).sum()*a; Ixy=(x*y).sum()*a
    w,v=np.linalg.eigh(np.array([[Iyy,Ixy],[Ixy,Ixx]]))
    res=[]
    for k in range(2):
        # bending about principal axis k: distance measured along the other axis
        ax=v[:,1-k]; c=np.abs(x*ax[0]+y*ax[1]).max()+UM/2
        Z=w[k]/c; d=(32*Z/np.pi)**(1/3)
        res.append((w[k],c,Z,d))
    return A,res
for f in sorted(glob.glob(sys.argv[1]+'/*.png')):
    a=np.asarray(Image.open(f).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]
    yel=(R>150)&(G>130)&(B<110)&(abs(R-G)<70)
    m=yel[:,0:600].copy(); m[:120]=False; m[960:]=False
    m=nd.binary_closing(m,iterations=1)
    lab,n=nd.label(m)
    rows=[]
    for i in range(1,n+1):
        mm=lab==i
        if mm.sum()<150: continue
        A,res=props(mm)
        Ad=2*np.sqrt(A/np.pi)
        rows.append(f"A={A:6.0f}um2 dA={Ad:5.0f} dZmin={res[0][3]:5.0f} dZmax={res[1][3]:5.0f}")
    print(f.split('/')[-1],' | '.join(rows))
