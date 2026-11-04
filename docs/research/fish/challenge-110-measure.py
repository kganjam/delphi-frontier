"""Challenge 110 image measurement (MY measurement from Ishizaka 2024 Movie S4; not author-reported).
Usage: ffmpeg -ss 12 -t 3 -i 41598_2024_74134_MOESM4_ESM.mp4 fa/f%03d.png ; python3 -I challenge-110-measure.py fa
Prints, for the 4 most edge-on frames, per 10% station along the long axis: envelope extent / filled grey thickness / red (distal-radial) pixels that may occlude grey."""
import sys,glob,numpy as np
from PIL import Image
um=100/124
best=[]
for f in sorted(glob.glob(sys.argv[1]+'/f*.png')):
    im=np.array(Image.open(f).convert('RGB')).astype(int); r,g,b=im[...,0],im[...,1],im[...,2]
    grey=(r>60)&(abs(r-g)<40)&(abs(r-b)<45); red=(r>100)&(g<90)&(r-g>50)
    for m in (grey,red): m[:150,:500]=False; m[1000:,:]=False
    ys,xs=np.where(grey); P=np.c_[xs,ys].astype(float); c=P.mean(0); w,v=np.linalg.eigh(np.cov((P-c).T)); a=v[:,1]; n=v[:,0]
    s=(P-c)@a; t=(P-c)@n; s0,s1=np.percentile(s,[0.5,99.5]); L=s1-s0
    ry,rx=np.where(red); R=np.c_[rx,ry].astype(float); rs=(R-c)@a
    st=[]
    for frac in np.arange(0.05,1.0,0.1):
        sel=np.abs(s-(s0+frac*L))<3; occl=(np.abs(rs-(s0+frac*L))<3).sum()
        if sel.sum()==0: st.append(None); continue
        st.append(((t[sel].max()-t[sel].min()+1)*um, sel.sum()/7*um, occl))
    tot=(np.percentile(t,99.5)-np.percentile(t,0.5))*um
    best.append((tot,f,st))
best.sort()
for tot,f,st in best[:4]:
    print(f.split('/')[-2:], f"whole perp-extent {tot:.0f}um")
    print('   station: extent/filled/redpx ', ' | '.join('-' if x is None else f"{x[0]:.0f}/{x[1]:.0f}/{x[2]}" for x in st))
