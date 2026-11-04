import sys, struct
d=open(sys.argv[1],'rb').read()
def s(b,o):
    L=struct.unpack_from('<H',b,o)[0]; return b[o+2:o+2+L].decode('latin1'), o+2+L
def walk(d,p,end,depth):
    while p+12<=end:
        t,ds,ms=struct.unpack_from('<III',d,p)
        body=d[p+12:p+12+ds]; info=''
        if t>=0xFFFFFF00 and t!=0xFFFFFF00:
            try: name,o=s(body,0); info=name
            except: pass
        print('  '*depth, hex(t), ds, info[:60])
        if t==0xFFFFFF14:
            name,o=s(body,0); ctype,attr=struct.unpack_from('<II',body,o); o+=8
            if attr&1: o+=16
            if attr&2: o+=24
            o+=(4-o%4)%4
            cnt=struct.unpack_from('<I',body,o)[0]; o+=4
            print('  '*depth,' chain',name,ctype,attr,cnt)
            walk(body,o,len(body),depth+1)
        p+=12+ds+((4-ds%4)%4)+ms+((4-ms%4)%4)
walk(d,0,len(d),0)
