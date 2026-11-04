import numpy as np
def slice_mesh(V,F,n,d):
    """Intersect closed mesh with plane n.x=d. Returns segments (k,2,3)."""
    s=V@n-d; s[s==0]=1e-9
    sf=s[F]; pos=sf>0; cnt=pos.sum(1)
    m=(cnt==1)|(cnt==2); Fm=F[m]; sm=sf[m]; pm=pos[m]
    # odd-one-out vertex
    odd=np.where(pm.sum(1)==1, np.argmax(pm,1), np.argmin(pm,1))
    a=Fm[np.arange(len(Fm)),odd]; b=Fm[np.arange(len(Fm)),(odd+1)%3]; c=Fm[np.arange(len(Fm)),(odd+2)%3]
    sa=s[a]; sb=s[b]; sc=s[c]
    p1=V[a]+(V[b]-V[a])*(sa/(sa-sb))[:,None]
    p2=V[a]+(V[c]-V[a])*(sa/(sa-sc))[:,None]
    return np.stack([p1,p2],1)
