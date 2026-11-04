import { chromium } from 'playwright-core';
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {setTimeout} from 'node:timers/promises';
if (process.env.DELPHI_CAPTURE_ACTIVE) throw new Error('Nested capture refused');
process.env.DELPHI_CAPTURE_ACTIVE='1';
if (!process.argv[2] || process.argv[2].startsWith('--')) throw new Error('Usage: node capture-deck.mjs NEW_OUTPUT_DIRECTORY [--animate]');
const out=path.resolve(process.argv[2]);
try { await fs.access(out); throw new Error('Output directory already exists; use a new directory.'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({executablePath:path.join(path.dirname(fileURLToPath(import.meta.url)),'capped-chromium.sh'),headless:true,args:['--single-process','--no-zygote','--disable-gpu','--renderer-process-limit=1'],timeout:30000});
try {
 const page=await browser.newPage({viewport:{width:1920,height:1200},deviceScaleFactor:1});
 await page.goto('https://delphibio.org/deck/',{waitUntil:'networkidle',timeout:30000});
 const manifest={source_url:page.url(),retrieved_at:new Date().toISOString(),scope:'New capture of the current public deck; distinct from archived November 3 source bytes.'};
 manifest.screenshots=[];
 for(const item of [{n:1,name:'Slide 1: Delphi: Lean for Biology'},{n:5,name:'Slide 5: A flying fish becomes a set of constraints.'},{n:6,name:'Slide 6: Where the same method goes next'}]) {
  await page.getByRole('button',{name:item.name,exact:true}).click();
  const slide=page.locator('#slide-'+item.n);
  const file='original-slide-'+item.n+'.png';
  await slide.screenshot({path:path.join(out,file),animations:'disabled'});
  manifest.screenshots.push({file,slide:item.n,sha256:crypto.createHash('sha256').update(await fs.readFile(path.join(out,file))).digest('hex'),bounds:await slide.boundingBox()});
  console.log(file);
 }
 if (process.argv.includes('--animate')) {
  await page.getByRole('button',{name:'Slide 1: Delphi: Lean for Biology',exact:true}).click();
  const slide=page.locator('#slide-1');
  await slide.screenshot({path:path.join(out,'original-slide-1.png'),animations:'disabled'});
  const clip=await slide.boundingBox();
  const framesDir=path.join(out,'sphere-frames');
  await fs.mkdir(framesDir,{recursive:true});
  const fps=15, count=180, started=performance.now(),times=[];
  for(let i=0;i<count;i++) {
   const delay=started+i*1000/fps-performance.now();
   if(delay>0) await setTimeout(delay);
   const file='frame-'+String(i).padStart(4,'0')+'.jpg';
   await page.screenshot({path:path.join(framesDir,file),clip,type:'jpeg',quality:90});
   times.push({file,elapsed_ms:performance.now()-started});
  }
  manifest.animation={source:'Actual live slide1 canvas animation',frames:count,fps,output_duration_seconds:count/fps,actual_capture_elapsed_ms:performance.now()-started,clip,frame_times:times};
  console.log(JSON.stringify({animationFrames:count,elapsed_ms:manifest.animation.actual_capture_elapsed_ms}));
 }
 await fs.writeFile(path.join(out,'provenance.json'),JSON.stringify(manifest,null,2)+'\n');
} finally {await browser.close();}
