import sys,struct,collections
def blocks(b,start,end):
    p=start
    while p+12<=end:
        t,ds,ms=struct.unpack_from('<III',b,p)
        yield t,p+12,ds,ms
        p+=12+ds+(-ds%4)+ms+(-ms%4)
def s(b,p):
    n=struct.unpack_from('<H',b,p)[0]; return b[p+2:p+2+n].decode('latin1'),p+2+n
def walk(b,start,end,depth,out,verbose=False):
    for t,P,ds,ms in blocks(b,start,end):
        out.append((depth,t,P,ds))
        if t==0xFFFFFF14:
            name,q=s(b,P); ctype,attr=struct.unpack_from('<II',b,q); q+=8
            if attr&1: q+=16
            if attr&2: q+=24
            q+=(-(q-P))%4
            cnt=struct.unpack_from('<I',b,q)[0]; q+=4
            if verbose: print('  '*depth,'chain',repr(name),ctype,attr,cnt)
            walk(b,q,P+ds,depth+1,out,verbose)
def load(fn):
    b=open(fn,'rb').read(); out=[]; walk(b,0,len(b),0,out); return b,out
if __name__=='__main__':
    b=open(sys.argv[1],'rb').read(); out=[]; walk(b,0,len(b),0,out,True)
    print(collections.Counter(hex(t) for d,t,_,_ in out))
    for d,t,P,ds in out:
        if t in (0xFFFFFF31,0xFFFFFF3B,0xFFFFFF22,0xFFFFFF21,0xFFFFFF3C):
            print(d,hex(t),repr(s(b,P)[0]),ds)
