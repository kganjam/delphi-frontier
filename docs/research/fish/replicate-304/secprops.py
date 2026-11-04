import sys, numpy as np
sys.path.insert(0,sys.argv[0].rsplit('/',1)[0]); from slice import slice_mesh
from scipy import ndimage
def raster(S, ax_u, ax_v, box, h):
    """even-odd scanline fill of slice segments; S (k,2,3); returns mask, u-grid, v-grid"""
    u0,u1,v0,v1=box
    U=S[:,:,ax_u]; Vv=S[:,:,ax_v]
    keep=(Vv.max(1)>v0)&(Vv.min(1)<v1)
    U=U[keep]; Vv=Vv[keep]
    nu=int((u1-u0)/h); nv=int((v1-v0)/h)
    uc=u0+(np.arange(nu)+.5)*h; vc=v0+(np.arange(nv)+.5)*h
    M=np.zeros((nv,nu),bool)
    for j,v in enumerate(vc):
        a=Vv[:,0]-v; b=Vv[:,1]-v; m=(a*b)<0
        if not m.any(): continue
        t=a[m]/(a[m]-b[m]); us=np.sort(U[m,0]+t*(U[m,1]-U[m,0]))
        if len(us)%2: us=us[:-1]
        for k in range(0,len(us),2):
            if us[k+1]<u0 or us[k]>u1: continue
            M[j,(uc>us[k])&(uc<us[k+1])]=True
    return M,uc,vc
def props(M,uc,vc,h):
    """section properties; bending axis parallel to v-axis => I = sum (u-ubar)^2 dA ; also about u-parallel axis and principal"""
    jj,ii=np.nonzero(M); u=uc[ii]; v=vc[jj]; dA=h*h; A=len(u)*dA
    ub,vb=u.mean(),v.mean()
    Iv=((u-ub)**2).sum()*dA + len(u)*dA*h*h/12   # about axis parallel to v (depth along u)
    Iu=((v-vb)**2).sum()*dA + len(u)*dA*h*h/12
    Iuv=((u-ub)*(v-vb)).sum()*dA
    cu=np.abs(u-ub).max()+h/2; cv=np.abs(v-vb).max()+h/2
    Imin=(Iu+Iv)/2-np.sqrt(((Iu-Iv)/2)**2+Iuv**2); Imax=(Iu+Iv)/2+np.sqrt(((Iu-Iv)/2)**2+Iuv**2)
    return dict(A=A,ub=ub,vb=vb,Iv=Iv,cu=cu,Zv=Iv/cu,Iu=Iu,cv=cv,Zu=Iu/cv,Imin=Imin,Imax=Imax,ext_u=np.ptp(u)+h,ext_v=np.ptp(v)+h)
