"""Minimal ECMA-363 (U3D) bitstream decoder: block walk, strings, CLOD base mesh."""
import struct, sys
STATIC=0x400
REV15=[int(format(i,'015b')[::-1],2) for i in range(1<<15)]
REV8=[int(format(i,'08b')[::-1],2) for i in range(256)]
class Hist:
    __slots__=("f","tot")
    def __init__(s): s.f={0:1}; s.tot=1
class BS:
    def __init__(s,data):
        s.d=data; s.nbits=len(data)*8; s.pos=0
        s.low=0; s.high=0xFFFF; s.uf=0; s.h={}
        s.d=bytes(data)+b"\0"*8
    def bit(s,p):
        return (s.d[p>>3]>>(p&7))&1
    def bits15(s,q):
        b=q>>3
        return (int.from_bytes(s.d[b:b+3],"little")>>(q&7))&0x7FFF
    def total(s,c):
        if c>=STATIC: return c-STATIC
        return s.h.setdefault(c,Hist()).tot
    def sym(s,c):
        p=s.pos
        code=s.bit(p)
        q=p+1+s.uf
        v=s.bits15(q)
        # reverse 15 bits (stream order first bit -> MSB)
        r=REV15[v]
        code=(code<<15)|r
        T=s.total(c); rng=s.high+1-s.low
        cf=(T*(1+code-s.low)-1)//rng
        if c>=STATIC:
            sv=cf+1; cum=sv-1; fr=1
        else:
            H=s.h[c]; acc=0
            for k in sorted(H.f):
                if acc+H.f[k]>cf: sv=k; cum=acc; fr=H.f[k]; break
                acc+=H.f[k]
            else: raise ValueError("ctx")
        hi=s.low-1+rng*(cum+fr)//T
        lo=s.low+rng*cum//T
        if c<STATIC:
            H=s.h[c]; H.f[sv]=H.f.get(sv,0)+1; H.tot+=1
            if H.tot>0x1FFF:
                tot=0
                for k in list(H.f):
                    H.f[k]>>=1
                    if k==0 and H.f[k]==0: H.f[k]=1
                    tot+=H.f[k]
                H.tot=tot
        nb=0
        while ((lo&0x8000)|(hi&0x8000))==0 or ((lo&0x8000) and (hi&0x8000)):
            lo=(lo&0x7FFF)<<1; hi=((hi&0x7FFF)<<1)|1; nb+=1
        sl=lo&0x8000; sh=hi&0x8000
        if nb>0: nb+=s.uf; s.uf=0
        u=0
        while (lo&0x4000) and not (hi&0x4000):
            lo&=0x3FFF; hi|=0x4000
            lo=(lo&0x7FFF)<<1; hi=((hi&0x7FFF)<<1)|1; u+=1
        s.uf+=u
        s.low=lo|sl; s.high=hi|sh
        s.pos=p+nb
        return sv
    def u8(s):
        v=s.sym(STATIC+256)-1
        return REV8[v]
    def u16(s): return s.u8()|(s.u8()<<8)
    def u32(s): return s.u16()|(s.u16()<<16)
    def f32(s): return struct.unpack("<f",struct.pack("<I",s.u32()))[0]
    def string(s):
        n=s.u16(); return bytes(s.u8() for _ in range(n)).decode("latin1")
    def cu32(s,c):
        if c!=0 and c<STATIC+0x3FFF:
            v=s.sym(c)
            if v!=0: return v-1
            if c<STATIC:
                val=s.u32(); H=s.h[c]; H.f[val+1]=H.f.get(val+1,0)+1; H.tot+=1; return val
            return s.u32()
        return s.u32()

def blocks(d,o=0,end=None):
    end=len(d) if end is None else end
    while o+12<=end:
        t,ds,ms=struct.unpack_from("<III",d,o)
        yield t,d[o+12:o+12+ds],o
        o+=12+((ds+3)&~3)+((ms+3)&~3)

if __name__=="__main__":
    d=open(sys.argv[1],"rb").read()
    for t,b,o in blocks(d):
        if t==0x443355: continue
        bs=BS(b)
        try: name=bs.string()
        except Exception as e: name=f"<{e}>"
        print(hex(t),len(b),repr(name[:80]))
