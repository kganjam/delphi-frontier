import sys, struct
d=open(sys.argv[1],'rb').read()
def s(b,o):
    L=struct.unpack_from('<H',b,o)[0]; return b[o+2:o+2+L].decode('latin1'), o+2+L
p=0
while p+12<=len(d):
    t,ds,ms=struct.unpack_from('<III',d,p); body=d[p+12:p+12+ds]
    if t==0xFFFFFF14:
        name,o=s(body,0); o+=8; o+=(4-o%4)%4; o+=4
        t2,ds2,ms2=struct.unpack_from('<III',body,o)
        if t2==0xFFFFFF31:
            b=body[o+12:o+12+ds2]; nm,q=s(b,0)
            print('decl', nm, [hex(x) for x in struct.unpack_from('<%dI'%((len(b)-q)//4),b,q)])
    if t==0xFFFFFF3B:
        nm,o=s(body,0); ci=struct.unpack_from('<I',body,o)[0]; o+=4
        cnts=struct.unpack_from('<6I',body,o); o+=24
        print('base',nm,ci,'faces,pos,norm,diff,spec,tex=',cnts, 'offset',o,'size',ds)
        F,P,N,D,S,T=cnts
        raw=o+12*P+12*N+16*D+16*S+16*T
        print('bytes after arrays', ds-raw, 'per face', (ds-raw)/F if F else 0)
    p+=12+ds+((4-ds%4)%4)+ms+((4-ms%4)%4)
