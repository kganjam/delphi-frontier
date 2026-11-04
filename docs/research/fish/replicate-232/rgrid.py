import sys,subprocess
from PIL import Image,ImageDraw
stem,box,view,out,scale,step=sys.argv[1:7]; scale=float(scale); step=float(step)
subprocess.run([sys.executable,'render.py',stem,box,view,out,str(scale)],check=True)
b=[float(v) for v in box.split(',')]; lo={'x':b[0],'y':b[2],'z':b[4]}; hi={'x':b[1],'y':b[3],'z':b[5]}
uv={'lat':('z','x'),'latR':('z','x'),'dors':('z','y'),'front':('y','x')}[view]
im=Image.open(out).convert('RGB'); d=ImageDraw.Draw(im)
for ai,a in enumerate(uv):
    v=(int(lo[a]/step)+1)*step
    while v<hi[a]:
        p=(v-lo[a])*scale
        if ai==0: d.line([(p,0),(p,im.height)],fill=(255,0,0)); d.text((p+2,2),f'{a}{v:.0f}',fill=(255,0,0))
        else: d.line([(0,p),(im.width,p)],fill=(0,0,255)); d.text((2,p+2),f'{a}{v:.0f}',fill=(0,0,255))
        v+=step
im.save(out)
