import sys, re, pypdf
pdf,out=sys.argv[1],sys.argv[2]
raw=open(pdf,'rb').read()
nums=sorted(set(int(m.group(1)) for m in re.finditer(rb'(\d+) 0 obj\s*<<[^>]*?/Subtype\s*/U3D',raw)))
r=pypdf.PdfReader(pdf)
for i,n in enumerate(nums):
    d=r.get_object(n).get_data(); open(f'{out}_{i+1}.u3d','wb').write(d); print(n,len(d))
