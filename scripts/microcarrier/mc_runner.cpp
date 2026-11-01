// mc_runner.cpp -- runner for the "Contractile tissue microcarrier" project
// (frontier project tissue-microcarrier). GENERIC soft-body voxel mechanics.
//
// Links Voxelyze (jonhiller/Voxelyze @ 4287e365e11416dd108f2f361e9ec4c5a011a16c),
// LGPL-3.0-or-later per its source headers. This file is our code, shipped as source.
//
// NOT biology: contraction is modelled as prescribed isotropic volumetric strain
// (Voxelyze thermal expansion, baseSize = size*(1+T*cte), VX_Voxel.h:88). The cited
// sources (Kriegman 2020, Blackiston 2021) report CILIARY locomotion; contraction is
// this project's own modelling choice. No parameter is calibrated to Xenopus tissue.
//
// Input: a pattern file (written by mc_patterns.py) with one line per voxel:
//   ix iy iz a phi       (a = relative amplitude, phi = phase in radians)
// and a header line "# nx ny nz voxel_m". Voxel i receives
//   T_i(t) = ampC * a_i * sin(2 pi f t + phi_i)   during the measurement window only.
// The runner does not know pattern families; it only executes the per-voxel table.

#include "Voxelyze.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <string>
#include <vector>
#include <algorithm>

static const double kPi = 3.14159265358979323846;

struct Cfg {
    std::string pattern, out="run";
    float E=2e4f, rho=1050.f, nu=0.35f, muS=1.0f, muK=0.8f;
    float zetaInt=1.0f, zetaGlob=0.1f, zetaColl=0.8f, cte=0.01f, ampC=10.0f, freq=10.0f;
    double gravity=0.047619;    // fraction of g: buoyant weight (1050-1000)/1050
    double settle=0.3;          // s, actuation off
    int cycles=6;               // measurement cycles (actuation on unless passive)
    double dtScale=0.5;
    int passive=0;              // 1 => actuation stays off during measurement window
    int samplesPerCycle=40;     // COM samples per cycle
    int dumpEvery=0;            // >0 => voxel positions every k COM samples
};

struct V3 { double x,y,z; };
static V3 comOf(const std::vector<CVX_Voxel*>& v){
    V3 c={0,0,0}; for(auto p: v){ Vec3D<double> q=p->position(); c.x+=q.x; c.y+=q.y; c.z+=q.z; }
    double n=v.size(); c.x/=n; c.y/=n; c.z/=n; return c;
}
static double maxSpeed(const std::vector<CVX_Voxel*>& v){
    double m=0; for(auto p: v){ double s=p->velocity().Length(); if(s>m) m=s; } return m;
}

int main(int argc, char** argv){
    Cfg c;
    for(int i=1;i<argc;i++){
        std::string a=argv[i]; size_t eq=a.find('=');
        if(a.rfind("--",0)!=0 || eq==std::string::npos){ fprintf(stderr,"bad arg %s\n",a.c_str()); return 2; }
        std::string k=a.substr(2,eq-2), s=a.substr(eq+1); double v=atof(s.c_str());
        if(k=="pattern")c.pattern=s; else if(k=="out")c.out=s;
        else if(k=="E")c.E=v; else if(k=="rho")c.rho=v; else if(k=="nu")c.nu=v;
        else if(k=="muS")c.muS=v; else if(k=="muK")c.muK=v;
        else if(k=="zetaInt")c.zetaInt=v; else if(k=="zetaGlob")c.zetaGlob=v; else if(k=="zetaColl")c.zetaColl=v;
        else if(k=="cte")c.cte=v; else if(k=="amp")c.ampC=v; else if(k=="freq")c.freq=v;
        else if(k=="gravity")c.gravity=v; else if(k=="settle")c.settle=v; else if(k=="cycles")c.cycles=atoi(s.c_str());
        else if(k=="dtScale")c.dtScale=v; else if(k=="passive")c.passive=atoi(s.c_str());
        else if(k=="samplesPerCycle")c.samplesPerCycle=atoi(s.c_str()); else if(k=="dumpEvery")c.dumpEvery=atoi(s.c_str());
        else { fprintf(stderr,"unknown key %s\n",k.c_str()); return 2; }
    }
    FILE* fp=fopen(c.pattern.c_str(),"r"); if(!fp){ fprintf(stderr,"no pattern file\n"); return 2; }
    int nx,ny,nz; double voxel; char line[512];
    if(!fgets(line,sizeof line,fp) || sscanf(line,"# %d %d %d %lf",&nx,&ny,&nz,&voxel)!=4){ fprintf(stderr,"bad header\n"); return 2; }
    struct PV{int ix,iy,iz; double a,phi;}; std::vector<PV> pv;
    while(fgets(line,sizeof line,fp)){ if(line[0]=='#') continue; PV p; if(sscanf(line,"%d %d %d %lf %lf",&p.ix,&p.iy,&p.iz,&p.a,&p.phi)==5) pv.push_back(p); }
    fclose(fp);

    CVoxelyze vx(voxel);
    CVX_Material* mat=vx.addMaterial(c.E,c.rho);
    mat->setPoissonsRatio(c.nu); mat->setStaticFriction(c.muS); mat->setKineticFriction(c.muK);
    mat->setInternalDamping(c.zetaInt); mat->setGlobalDamping(c.zetaGlob); mat->setCollisionDamping(c.zetaColl);
    mat->setCte(c.cte);
    std::vector<CVX_Voxel*> vox; std::vector<double> A, PH;
    for(auto& p: pv){ vox.push_back(vx.setVoxel(mat,p.ix,p.iy,p.iz)); A.push_back(p.a); PH.push_back(p.phi); }
    vx.setGravity((float)c.gravity); vx.enableFloor(true); vx.enableCollisions(false);

    double rec=vx.recommendedTimeStep(), dt=c.dtScale*rec;
    double period=1.0/c.freq;
    long nSettle=(long)std::ceil(c.settle/dt);
    long stepsPerCycle=(long)std::llround(period/dt);
    double dtEff=period/stepsPerCycle;            // exact integer steps per cycle
    long nMeas=stepsPerCycle*c.cycles;
    long sampleEvery=std::max(1L, stepsPerCycle/c.samplesPerCycle);

    FILE* fc=fopen((c.out+"-com.csv").c_str(),"w");
    fprintf(fc,"t_s,phase,com_x_m,com_y_m,com_z_m,max_speed_m_s\n");
    FILE* fv=NULL; if(c.dumpEvery>0){ fv=fopen((c.out+"-voxels.csv").c_str(),"w"); fprintf(fv,"t_s,i,ix,iy,iz,x,y,z,strain_drive\n"); }

    bool div=false; long divAt=-1; double t=0;
    long nPre=nSettle-(long)std::llround(0.05/dt); V3 cPre={0,0,0};   // COM 0.05 s before settle end
    V3 lo={1e9,1e9,1e9}, hi={-1e9,-1e9,-1e9};                          // COM envelope over last 0.05 s
    long chkEvery=std::max(1L,(long)std::llround(0.0005/dt));          // sampled every 0.5 ms
    for(long s=0;s<nSettle;s++){
        if(s==nPre) cPre=comOf(vox);
        if(s>=nPre && (s-nPre)%chkEvery==0){ V3 q=comOf(vox);
            lo.x=std::min(lo.x,q.x); lo.y=std::min(lo.y,q.y); lo.z=std::min(lo.z,q.z);
            hi.x=std::max(hi.x,q.x); hi.y=std::max(hi.y,q.y); hi.z=std::max(hi.z,q.z); }
        if(!vx.doTimeStep((float)dt)){div=true;divAt=s;break;} t+=dt; }
    { V3 q=comOf(vox); lo.x=std::min(lo.x,q.x); lo.y=std::min(lo.y,q.y); lo.z=std::min(lo.z,q.z);
      hi.x=std::max(hi.x,q.x); hi.y=std::max(hi.y,q.y); hi.z=std::max(hi.z,q.z); }
    double settleSpeed=maxSpeed(vox); V3 c0=comOf(vox);
    double bodyLenX=(nx-1)*voxel+voxel; // outer length
    std::vector<V3> strobe; strobe.push_back(c0);
    long samp=0; double tm=0; double maxPen=-1e9; double pathLen=0; V3 prev=c0;
    if(!div) for(long s=0;s<nMeas;s++){
        // sin^2 ramp over the declared transient cycle (cycle 1), then full amplitude
        double w = (tm < period) ? std::pow(std::sin(0.5*kPi*c.freq*tm),2) : 1.0;
        for(size_t i=0;i<vox.size();i++){
            float T = c.passive ? 0.f : (float)(w*c.ampC*A[i]*std::sin(2*kPi*c.freq*tm + PH[i]));
            vox[i]->setTemperature(T);
            double pen=vox[i]->floorPenetration(); if(pen>maxPen) maxPen=pen;
        }
        if(!vx.doTimeStep((float)dtEff)){div=true;divAt=nSettle+s;break;}
        t+=dtEff; tm=(s+1)*dtEff;
        if((s+1)%sampleEvery==0){
            V3 cm=comOf(vox); pathLen+=std::hypot(cm.x-prev.x,cm.y-prev.y); prev=cm;
            fprintf(fc,"%.7f,%.5f,%.12e,%.12e,%.12e,%.6e\n",t,std::fmod(tm*c.freq,1.0),cm.x,cm.y,cm.z,maxSpeed(vox));
            if(fv && (samp%c.dumpEvery)==0) for(size_t i=0;i<vox.size();i++){ Vec3D<double> q=vox[i]->position();
                fprintf(fv,"%.6f,%zu,%d,%d,%d,%.9e,%.9e,%.9e,%.5f\n",t,i,pv[i].ix,pv[i].iy,pv[i].iz,q.x,q.y,q.z,
                        c.passive?0.0:w*c.cte*c.ampC*A[i]*std::sin(2*kPi*c.freq*tm+PH[i])); }
            samp++;
        }
        if((s+1)%stepsPerCycle==0) strobe.push_back(comOf(vox));
    }
    fclose(fc); if(fv) fclose(fv);
    V3 c1=comOf(vox);
    FILE* fj=fopen((c.out+".json").c_str(),"w");
    fprintf(fj,"{\n \"schema\": \"frontier.microcarrier-run/1\",\n");
    fprintf(fj," \"engine\": {\"name\":\"Voxelyze\",\"commit\":\"4287e365e11416dd108f2f361e9ec4c5a011a16c\",\"licence\":\"LGPL-3.0-or-later (source headers)\"},\n");
    fprintf(fj," \"pattern_file\": \"%s\",\n \"mesh\": {\"nx\":%d,\"ny\":%d,\"nz\":%d,\"voxel_m\":%.9g,\"voxels\":%zu,\"body_len_x_m\":%.9g},\n",c.pattern.c_str(),nx,ny,nz,voxel,vox.size(),bodyLenX);
    fprintf(fj," \"params\": {\"E_Pa\":%g,\"rho\":%g,\"nu\":%g,\"muS\":%g,\"muK\":%g,\"zetaInt\":%g,\"zetaGlob\":%g,\"zetaColl\":%g,\"cte\":%g,\"ampC\":%g,\"freq_Hz\":%g,\"gravity_g\":%g,\"settle_s\":%g,\"cycles\":%d,\"passive\":%d},\n",
        (double)c.E,(double)c.rho,(double)c.nu,(double)c.muS,(double)c.muK,(double)c.zetaInt,(double)c.zetaGlob,(double)c.zetaColl,(double)c.cte,(double)c.ampC,(double)c.freq,c.gravity,c.settle,c.cycles,c.passive);
    fprintf(fj," \"numerics\": {\"recommended_dt_s\":%.9g,\"dt_scale\":%g,\"dt_settle_s\":%.9g,\"dt_measure_s\":%.9g,\"steps_settle\":%ld,\"steps_per_cycle\":%ld,\"diverged\":%s,\"diverged_at\":%ld},\n",
        rec,c.dtScale,dt,dtEff,nSettle,stepsPerCycle,div?"true":"false",divAt);
    fprintf(fj," \"settle\": {\"max_voxel_speed_m_s\":%.6e,\"max_speed_body_len_per_s\":%.6e,\"com_m\":[%.12e,%.12e,%.12e],\"last_0p05s_drift_m\":[%.6e,%.6e,%.6e],\"last_0p05s_peak_to_peak_m\":[%.6e,%.6e,%.6e]},\n",settleSpeed,settleSpeed/bodyLenX,c0.x,c0.y,c0.z,c0.x-cPre.x,c0.y-cPre.y,c0.z-cPre.z,hi.x-lo.x,hi.y-lo.y,hi.z-lo.z);
    fprintf(fj," \"strobe_com_xy_m\": [");
    for(size_t k=0;k<strobe.size();k++) fprintf(fj,"%s[%.12e,%.12e]",k?",":"",strobe[k].x,strobe[k].y);
    fprintf(fj,"],\n");
    double dx=c1.x-c0.x, dy=c1.y-c0.y;
    double dx2=0,dy2=0; if(strobe.size()>=2){ dx2=strobe.back().x-strobe[1].x; dy2=strobe.back().y-strobe[1].y; }
    fprintf(fj," \"result\": {\"net_dx_m\":%.12e,\"net_dy_m\":%.12e,\"net_disp_m\":%.12e,\"net_disp_body_len\":%.9e,"
               "\"post_transient_dx_m\":%.12e,\"post_transient_dy_m\":%.12e,\"post_transient_cycles\":%d,\"path_len_m\":%.9e,\"com_z_end_m\":%.9e,\"max_floor_penetration_voxel_frac\":%.6e}\n}\n",
        dx,dy,std::hypot(dx,dy),std::hypot(dx,dy)/bodyLenX,dx2,dy2,(int)strobe.size()-2,pathLen,c1.z,maxPen/voxel);
    fclose(fj);
    printf("%s disp=%.4e m (%.4e L) dx=%.4e dy=%.4e diverged=%d\n",c.out.c_str(),std::hypot(dx,dy),std::hypot(dx,dy)/bodyLenX,dx,dy,div?1:0);
    return div?3:0;
}
