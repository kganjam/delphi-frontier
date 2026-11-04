// U3D (ECMA-363) bitstream decoder subset: base-mesh faces, positions only, single shading, no normals.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t U32;
static unsigned char *D; static size_t DLEN; static size_t bitpos;
static U32 low=0, high=0xFFFF, underflow=0, code=0;
static int getbit(size_t k){ size_t B=k>>3; if(B>=DLEN) return 0; return (D[B]>>(k&7))&1; }
// dynamic context (single: cShading)
static U32 *cnt=NULL,*cum=NULL; static U32 csize=0;
static void ensure(U32 n){ if(n<=csize) return; U32 ns=n+32; cnt=realloc(cnt,ns*4); cum=realloc(cum,ns*4);
  for(U32 i=csize;i<ns;i++){cnt[i]=0;cum[i]=0;} if(csize==0){cnt[0]=1;cum[0]=1;} csize=ns; }
static void addsym(U32 s){ if(s>=0xFFFF) return; ensure(s+1);
  if(cum[0]>=0x1FFF){ U32 acc=0; for(int i=csize-1;i>=0;i--){cnt[i]>>=1; acc+=cnt[i]; cum[i]=acc;} cnt[0]++; cum[0]++; }
  cnt[s]++; for(U32 i=0;i<=s;i++) cum[i]++; }
static U32 dtotal(){ return csize? cum[0]:1; }
static U32 dcumf(U32 s){ if(!csize) return 0; if(s<csize) return cum[0]-cum[s]; return cum[0]; }
static U32 dfreq(U32 s){ if(!csize) return s==0?1:0; return s<csize? cnt[s]:0; }
static U32 dsymfromf(U32 f){ if(!csize) return 0; U32 acc=0; for(U32 i=0;i<csize;i++){ if(f<acc+cnt[i]) return i; acc+=cnt[i]; } return 0; }
static void fillcode(){ code=getbit(bitpos); size_t p=bitpos+1+underflow; U32 v=0; for(int i=0;i<15;i++) v=(v<<1)|getbit(p+i); code=(code<<15)|v; }
static void renorm(U32 L,U32 H){
  U32 bc=0; U32 ml=0x8000&L, mh=0x8000&H;
  while(((ml|mh)==0)||((ml==0x8000)&&(mh==0x8000))){ L=(0x7FFF&L)<<1; H=((0x7FFF&H)<<1)|1; ml=0x8000&L; mh=0x8000&H; bc++; }
  U32 sl=ml, sh=mh; if(bc>0){ bc+=underflow; underflow=0; }
  ml=0x4000&L; mh=0x4000&H; U32 uf=0;
  while((ml==0x4000)&&(mh==0)){ L&=0x3FFF; H&=0x3FFF; L+=L; H+=H; H|=1; ml=0x4000&L; mh=0x4000&H; uf++; }
  underflow+=uf; L|=sl; H|=sh; low=L; high=H; bitpos+=bc; }
static U32 readstatic(U32 total){ fillcode(); U32 range=high+1-low; U32 f=(U32)(((uint64_t)total*(1+code-low)-1)/range);
  U32 L=low, H=low-1+(U32)((uint64_t)range*(f+1)/total); L=low+(U32)((uint64_t)range*f/total); renorm(L,H); return f+1; }
static U32 readdynamic(){ fillcode(); U32 range=high+1-low; U32 total=dtotal(); U32 f=(U32)(((uint64_t)total*(1+code-low)-1)/range);
  U32 s=dsymfromf(f); U32 cf=dcumf(s), fr=dfreq(s);
  U32 H=low-1+(U32)((uint64_t)range*(cf+fr)/total); U32 L=low+(U32)((uint64_t)range*cf/total);
  addsym(s); renorm(L,H); return s; }
static U32 swap8(U32 v){ U32 r=0; for(int i=0;i<8;i++) if(v&(1u<<i)) r|=1u<<(7-i); return r; }
static U32 readU8(){ U32 s=readstatic(256); return swap8(s-1); }
static U32 readU32(){ U32 v=0; for(int i=0;i<4;i++) v|=readU8()<<(8*i); return v; }
static U32 readCompU32dyn(){ U32 s=readdynamic(); if(s) return s-1; U32 v=readU32(); addsym(v+1); return v; }
static U32 readCompU32static(U32 range){ if(range < 0x3FFF) return readstatic(range)-1; return readU32(); }
int main(int argc,char**argv){
  // args: file offset(bytes,start of face data) length(bytes to end of block) nfaces npos out
  FILE*f=fopen(argv[1],"rb"); fseek(f,0,SEEK_END); size_t n=ftell(f); fseek(f,0,SEEK_SET); unsigned char*all=malloc(n); fread(all,1,n,f); fclose(f);
  size_t off=atol(argv[2]); DLEN=atol(argv[3]); D=all+off; U32 F=atol(argv[4]); U32 Np=atol(argv[5]);
  FILE*o=fopen(argv[6],"wb"); U32 bad=0, shadnz=0;
  for(U32 i=0;i<F;i++){ U32 sh=readCompU32dyn(); if(sh) shadnz++; U32 t[3]; for(int c=0;c<3;c++){ t[c]=readCompU32static(Np); if(t[c]>=Np) bad++; } fwrite(t,4,3,o); }
  fclose(o);
  fprintf(stderr,"faces %u bad_idx %u shading_nonzero %u bits_used %zu of %zu (bytes %.2f of %zu) underflow %u\n",F,bad,shadnz,bitpos,DLEN*8,bitpos/8.0,DLEN,underflow);
  return 0; }
