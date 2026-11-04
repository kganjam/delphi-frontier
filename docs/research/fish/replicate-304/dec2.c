// Independent U3D (ECMA-363) base-mesh face decoder. Usage: dec file offset nfaces npos variant out.bin
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static uint8_t *buf; static long nbytes;
static uint64_t pos; static uint32_t lo=0, hi=0xFFFF, uf=0;
static int bit(uint64_t k){ return (k>>3)<(uint64_t)nbytes ? (buf[k>>3]>>(k&7))&1 : 0; }
static uint32_t f[2]={1,0}; static int variant;
// dynamic two-symbol histogram (escape=0, symbol1)
static long THR; static int GE, RUP, ESC, PRE;
static void resc(void){ uint32_t t=f[0]+f[1]; if(GE? t>=THR : t>THR){ if(ESC) f[0]=RUP?(f[0]+1)/2:(f[0]>1?f[0]/2:1); f[1]=RUP?(f[1]+1)/2:f[1]/2; } }
static void dyn_add(uint32_t s){ if(PRE) resc(); f[s]++; if(!PRE) resc(); }
// returns symbol; type 0 = static total T, type 1 = dynamic
static uint32_t readsym(int type, uint32_t T){
  uint32_t code = bit(pos)<<15;
  for(int i=0;i<15;i++) code |= bit(pos+1+uf+i)<<(14-i);
  uint32_t total = type? f[0]+f[1] : T;
  uint64_t range = (uint64_t)hi+1-lo;
  uint32_t cf = (uint32_t)(((uint64_t)total*(1+code-lo)-1)/range);
  uint32_t sym, cum, fr;
  if(!type){ sym=cf+1; cum=sym-1; fr=1; }
  else { if(cf < f[0]){sym=0;cum=0;fr=f[0];} else {sym=1;cum=f[0];fr=f[1];} }
  uint32_t nh = lo-1+(uint32_t)(range*(cum+fr)/total);
  uint32_t nl = lo+(uint32_t)(range*cum/total);
  lo=nl; hi=nh;
  if(type && (variant&1)) dyn_add(sym);
  uint32_t bc=0;
  while((lo&0x8000)==(hi&0x8000)){ lo=(lo&0x7fff)<<1; hi=((hi&0x7fff)<<1)|1; bc++; }
  if(bc){ bc+=uf; uf=0; }
  while((lo&0x4000) && !(hi&0x4000)){ lo=(lo&0x3fff)<<1; hi=((hi&0x3fff)<<1)|0x8001; uf++; }
  pos+=bc; return sym;
}
static uint8_t rev8(uint8_t x){ uint8_t r=0; for(int i=0;i<8;i++) if(x&(1<<i)) r|=1<<(7-i); return r; }
static uint32_t ru8(void){ return rev8((uint8_t)(readsym(0,256)-1)); }
static uint32_t ru32(void){ uint32_t a=ru8(), b=ru8(), c=ru8(), d=ru8(); return a|(b<<8)|(c<<16)|(d<<24); }
int main(int argc,char**argv){
  FILE*fp=fopen(argv[1],"rb"); fseek(fp,0,SEEK_END); nbytes=ftell(fp); rewind(fp);
  buf=malloc(nbytes); fread(buf,1,nbytes,fp); fclose(fp);
  long off=atol(argv[2]), F=atol(argv[3]), P=atol(argv[4]); variant=1; int vv=atoi(argv[5]); THR=atol(argv[7]); GE=vv&1; RUP=(vv>>1)&1; ESC=(vv>>2)&1; PRE=(vv>>3)&1;
  pos=(uint64_t)off*8;
  uint32_t *out=malloc(F*3*4); long bad=0, firstbad=-1;
  for(long i=0;i<F;i++){
    uint32_t s=readsym(1,0);
    if(s==0){ uint32_t v=ru32(); if(v!=0){ if(firstbad<0) firstbad=i; } else dyn_add(1); }
    for(int c=0;c<3;c++){ uint32_t v=ru32(); out[i*3+c]=v; if(v>=(uint32_t)P){ bad++; if(firstbad<0) firstbad=i; } }
  }
  fprintf(stderr,"thr %ld vv %d ",THR,vv); fprintf(stderr,"variant %d bad %ld firstbad %ld endbyte %llu of %ld\n",variant,bad,firstbad,(unsigned long long)(pos/8),nbytes);
  FILE*o=fopen(argv[6],"wb"); fwrite(out,4,F*3,o); fclose(o); return 0;
}
