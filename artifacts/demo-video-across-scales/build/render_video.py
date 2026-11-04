"""Function-first film: original deck compositions, actual outputs, continuous voice."""
from pathlib import Path
import argparse,functools,hashlib,json,math,os,re,subprocess
from PIL import Image,ImageDraw,ImageFont
import motion_layouts
from media_runtime import Fonts, check_pin, ffmpeg_command, load_assets, probe as media_probe, process_command, sha256_file
ROOT=Path(__file__).resolve().parent.parent
W,H,FPS=1920,1080,30
OUT=ROOT/'.build';WORK=OUT/'work'
DURATION=90;OUTPUT_DIR=OUT;OUTPUT_STEM='preview';SCRIPT_PATH=None
SOURCES={};SOURCE_POSTERS={};ASSET_PINS={};SHOTS=[]
ASSET_MANIFEST=None;AUDIO_MANIFEST=None;PROFILE_PATH=None;FONTS=None
PAPER='#f2f5f8';INK='#142033';BLUE='#2457d6';TEAL='#63d6c5'
@functools.lru_cache(maxsize=80)
def font(n,bold=False,serif=False,italic=False):
 return FONTS.get(n,bold=bold,serif=serif,italic=italic)
def put(d,xy,s,size=40,color=INK,bold=False,serif=False):
 for j,line in enumerate(s.split('\n')):d.text((xy[0],xy[1]+j*round(size*1.13)),line,font=font(size,bold,serif),fill=color)
def headline(d,xy,s,size=92):
 emphasis=s.get('headline_emphasis')
 if not emphasis:
  put(d,xy,s['headline'],size,INK,serif=True);return
 target=emphasis['text'];label=s['headline'];assert label.count(target)==1
 start,finish=label.split(target)
 normal=font(size,serif=True)
 marked=font(round(size*emphasis.get('scale',1)),bold=emphasis.get('bold',False),serif=True,italic=emphasis.get('italic',False))
 runs=[(start,normal,INK),(target,marked,emphasis.get('color',BLUE)),(finish,normal,INK)]
 x,y=xy;baseline=y+normal.getmetrics()[0]
 optical_gap=max(0,marked.getbbox(target)[2]-d.textlength(target,font=marked))+emphasis.get('gap_after_px',0)
 assert x+sum(d.textlength(t,font=f) for t,f,c in runs)+optical_gap<W-70
 for index,(text,f,color) in enumerate(runs):
  d.text((x,baseline),text,font=f,fill=color,anchor='ls');x+=d.textlength(text,font=f)
  if index==1:x+=optical_gap

def fit(src,box,cover=False):
 x,y,w,h=box;r=max(w/src.width,h/src.height) if cover else min(w/src.width,h/src.height)
 nw,nh=round(src.width*r),round(src.height*r);im=src.resize((nw,nh),Image.Resampling.LANCZOS)
 if cover:im=im.crop(((nw-w)//2,(nh-h)//2,(nw+w)//2,(nh+h)//2));return im,(x,y)
 return im,(x+(w-nw)//2,y+(h-nh)//2)
def paste(dst,src,box=(0,0,W,H),crop=None,cover=False):
 if crop:x,y,w,h=crop;src=src.crop((x,y,x+w,y+h))
 im,pos=fit(src,box,cover);dst.paste(im,pos)
@functools.lru_cache(maxsize=30)
def source_image(asset):
 path=SOURCE_POSTERS.get(asset,SOURCES[asset])
 return Image.open(path).convert('RGB')
def media_box(s):
 if s.get('box'):return s['box']
 if s.get('headline') and s.get('crop'):return (50,240,1820,675)
 return (0,100,W,820) if s.get('crop') else (0,0,W,H)

def graphic(s,phase=.5,caption=None):
 dark=s.get('dark',False) or s['asset']=='sphere';bg='#142033' if dark else PAPER
 layout=s.get('layout','full')
 if layout in {'hero','art','close','motion','camera','panels'}:bg='white'
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
 if layout=='motion':
  im=motion_layouts.render(s['motion'],phase,source_image,font);d=ImageDraw.Draw(im)
 elif layout=='camera':
  camera=s['camera'];p=motion_layouts.ease(phase)
  crop=[round(a+(b-a)*p) for a,b in zip(camera['from'],camera['to'])]
  paste(im,source_image(s['asset']),camera.get('box',(0,225,1920,700)),crop,cover=True)
 elif layout=='panels':
  for panel in s['panels']:
   paste(im,source_image(panel['asset']),panel['box'],panel.get('crop'))
   put(d,panel['label_xy'],panel['label'],panel.get('label_size',37),BLUE,serif=True)
 elif layout=='dna':
  obj=json.loads(SOURCES[s['asset']].read_text());rec=obj['original_record'];seq=rec['sequence']
  assert len(seq)==1000 and hashlib.sha256(seq.encode()).hexdigest()==rec['sha256']
  for r in range(12):
   a=(int(phase*350)//50*50)+r*50
   put(d,(90,270+r*48),f'{a+1:04}',23,'#63758a')
   for j,b in enumerate(seq[a:a+50]):put(d,(205+j*31,270+r*48),b,29,{'A':'#287e64','C':'#2457d6','G':'#976800','T':'#ae4264'}[b],True)
 elif layout=='close':
  paste(im,source_image('organoid'),(90,190,520,520));paste(im,source_image('lightweight-structure'),(700,190,520,520));paste(im,source_image('air-water-fish'),(1310,190,520,520))
  headline(d,(90,715),s,92);put(d,(95,838),'delphibio.org',41,BLUE,True)
 elif layout=='applications':paste(im,source_image('deck6'),(0,110,W,760),[75,350,1735,345])
 elif layout=='art':
  paste(im,source_image(s['asset']),(770,70,1060,900))
  lines=[];line=''
  for word in s.get('headline','').split():
   test=(line+' '+word).strip()
   if d.textlength(test,font=font(64,serif=True))>680 and line:lines.append(line);line=word
   else:line=test
  if line:lines.append(line)
  put(d,(85,310),'\n'.join(lines),64,INK,serif=True)
 elif layout=='hero':
  paste(im,source_image('fish'),(500,150,1400,880));put(d,(90,200),s['headline'],92,INK,serif=True)
 elif layout=='front':
  paste(im,source_image('front'))
  d.rectangle((0,0,W,112),fill=PAPER);d.rectangle((70,710,1010,1000),fill=PAPER)
  d.rectangle((1080,160,1420,208),fill='#142033')
  put(d,(85,745),'Evidence. Assumptions. Consequences.',38,BLUE,serif=True)
  d.rectangle((0,1003,W,H),fill=PAPER)
 elif layout=='deck':
  paste(im,source_image('deck5'));d.rectangle((0,0,W,112),fill=PAPER);d.rectangle((0,1020,W,H),fill=PAPER)
 else:
  asset=s['asset'];crop=s.get('crop')
  box=media_box(s)
  paste(im,source_image(asset),box,crop,cover=asset=='sphere')
 if s.get('headline') and layout not in {'art','hero','close','front','motion'}:
  if s['asset']=='sphere':put(d,(85,180),s['headline'],65,'#f7fbff',serif=True)
  elif layout not in {'dna','deck'}:put(d,(85,143),s['headline'],56,'#f7fbff' if dark else INK,serif=True)
  elif layout=='dna':put(d,(85,137),s['headline'],65,INK,serif=True)
 # Compact badges. This image is also used to create the transparent overlay.
 textcol='#f7fbff' if dark else INK
 d.rounded_rectangle((68,38,min(1810,100+int(d.textlength(s['tag'],font=font(34,True)))),100),radius=10,fill='#142033' if not dark else '#eef6ff')
 put(d,(86,45),s['tag'],34,'#f7fbff' if not dark else INK,True)
 if s.get('scope'):
  d.rectangle((0,925,W,978),fill=bg);put(d,(85,937),s['scope'],25,'#aebfd0' if dark else '#526178')
 if caption:
  d.rectangle((0,987,W,H),fill='#111e30');put(d,(85,1001),caption,35,'white')
 return im

def preview():
 OUT.mkdir(exist_ok=True);paths=[]
 for i,s in enumerate(SHOTS):
  p=OUT/f'preview-{i+1:02d}-{s["id"]}.png';graphic(s).save(p);paths.append(p)
 sheet=Image.new('RGB',(1920,270*math.ceil(len(paths)/4)),PAPER)
 for i,p in enumerate(paths):sheet.paste(Image.open(p).resize((480,270)),((i%4)*480,(i//4)*270))
 sheet.save(OUT/'storyboard-v2.jpg',quality=94)
 print(OUT/'storyboard-v2.jpg')

def ff(args):
 subprocess.run(ffmpeg_command(args),check=True)

def frame_dimensions(crop,box,cover=False):
 cw,ch=crop[2:];x,y,w,h=box;r=max(w/cw,h/ch) if cover else min(w/cw,h/ch)
 nw,nh=round(cw*r/2)*2,round(ch*r/2)*2
 return nw,nh,round((x+(w-nw)/2)/2)*2,round((y+(h-nh)/2)/2)*2

@functools.lru_cache(maxsize=20)
def probe(path):return media_probe(path)

def decorations(s,caption=None):
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 dark=s.get('dark',False) or s['asset']=='sphere';layout=s.get('layout','full');bg='#142033' if dark else PAPER
 if layout in {'hero','art','close','motion','camera','panels'}:bg='white'
 if layout=='front':
  d.rectangle((0,0,W,112),fill=PAPER);d.rectangle((70,710,1010,1000),fill=PAPER)
  d.rectangle((1080,160,1420,208),fill='#142033');d.rectangle((0,1003,W,H),fill=PAPER)
  put(d,(85,745),'Evidence. Assumptions. Consequences.',38,BLUE,serif=True)
 if layout=='panels':
  for panel in s['panels']:put(d,panel['label_xy'],panel['label'],panel.get('label_size',37),BLUE,serif=True)
 if s.get('headline') and layout not in {'art','hero','close','front','motion'}:
  if s['asset']=='sphere':put(d,(85,180),s['headline'],65,'#f7fbff',serif=True)
  elif layout not in {'dna','deck'}:put(d,(85,143),s['headline'],56,'#f7fbff' if dark else INK,serif=True)
 d.rounded_rectangle((68,38,min(1810,100+int(d.textlength(s['tag'],font=font(34,True)))),100),radius=10,fill='#142033' if not dark else '#eef6ff')
 put(d,(86,45),s['tag'],34,'#f7fbff' if not dark else INK,True)
 if s.get('scope'):
  d.rectangle((0,925,W,978),fill=bg);put(d,(85,937),s['scope'],25,'#aebfd0' if dark else '#526178')
 if caption:
  d.rectangle((0,987,W,H),fill='#142033')
  tw=d.textlength(caption,font=font(52));assert tw<=1800, f'Caption too wide: {caption}';put(d,((W-tw)/2,997),caption,52,'#ffffff')
 return im

def caption_cues(timing):
 words=timing['words'];sentences=[];sentence=[]
 for i,w in enumerate(words):
  sentence.append(w)
  if re.search(r'[.?!][”\"]?$',w['text']) or i==len(words)-1:
   sentences.append(sentence);sentence=[]
 groups=[]
 for sentence in sentences:
  n=math.ceil(len(sentence)/7);size=math.ceil(len(sentence)/n)
  groups.extend(sentence[i:i+size] for i in range(0,len(sentence),size))
 cues=[]
 for i,g in enumerate(groups):
  a=g[0]['start_s']+.1;b=g[-1]['end_s']+.1
  if i+1<len(groups):b=min(groups[i+1][0]['start_s']+.1,b+.1)
  phrase=' '.join(x['text'] for x in g)
  assert ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(phrase,font=font(52))<=1800,phrase
  cues.append({'start':a,'end':b,'text':phrase})
 return cues

def timeline(manifest_path):
 manifest=json.loads(manifest_path.read_text());script=SCRIPT_PATH.read_text()
 assert manifest['text']==script,'Narration text differs from current script; refusing stale render'
 assert hashlib.sha256(script.encode()).hexdigest()==manifest['text_sha256']
 audio=manifest_path.parent/manifest['wav_file'];timing_path=manifest_path.parent/manifest['timings_file']
 assert hashlib.sha256(audio.read_bytes()).hexdigest()==manifest['wav_sha256']
 assert hashlib.sha256(timing_path.read_bytes()).hexdigest()==manifest['timings_sha256']
 timing=json.loads(timing_path.read_text());shots=[]
 for s in SHOTS:
  pos=script.find(s['anchor']);assert pos>=0,f'Missing shot anchor: {s["id"]}'
  word=next(x for x in timing['words'] if x['source_char_begin']>=pos)
  frame=s.get('fixed_start_frame',round((word['start_s']+.1+s.get('anchor_offset',0))*FPS))
  shots.append({**s,'start_frame':frame})
 shots[0]['start_frame']=0
 for i,s in enumerate(shots):
  s['end_frame']=shots[i+1]['start_frame'] if i+1<len(shots) else round(DURATION*FPS)
  assert s['end_frame']>s['start_frame'],f'Nonpositive cut: {s["id"]}'
  s['start_s']=s['start_frame']/FPS;s['duration_s']=(s['end_frame']-s['start_frame'])/FPS
 cues=caption_cues(timing)
 (OUT/'cutlist.json').write_text(json.dumps(shots,indent=2)+'\n')
 (OUT/'caption-cues.json').write_text(json.dumps(cues,indent=2)+'\n')
 return shots,cues,audio

def cue_at(cues,seconds):return next((c['text'] for c in cues if c['start']<=seconds<c['end']),'')

def encode_native(s,cues,output):
 count=s['end_frame']-s['start_frame']
 cmd=ffmpeg_command(['-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-threads','2','-preset','fast','-x264-params','rc-lookahead=8:sync-lookahead=0','-crf','18','-pix_fmt','yuv420p',str(output)])
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for n in range(count):
   phase=n/count;copy=dict(s)
   if s['layout']=='hero':
    visible=max(0,min(len(s['headline']),int((n/FPS)/1.6*len(s['headline']))));copy['headline']=s['headline'][:visible]
   im=graphic(copy,phase)
   cap=cue_at(cues,(s['start_frame']+n)/FPS)
   im=Image.alpha_composite(im.convert('RGBA'),decorations(copy,cap)).convert('RGB')
   proc.stdin.write(im.tobytes())
  proc.stdin.close();rc=proc.wait(timeout=90)
  if rc:raise RuntimeError(f'Native encode failed {rc}')
 except BaseException:
  if proc.stdin and not proc.stdin.closed:proc.stdin.close()
  proc.wait(timeout=30);raise

def encode_shot(s,cues):
 output=WORK/f'{s["id"]}.mp4'
 if s.get('layout') in {'hero','dna','motion','camera'}:encode_native(s,cues,output);return output
 bounds={s['start_frame'],s['end_frame']}
 for c in cues:
  for t in [c['start'],c['end']]:
   n=round(t*FPS)
   if s['start_frame']<n<s['end_frame']:bounds.add(n)
 bounds=sorted(bounds);parts=[]
 background=WORK/f'{s["id"]}-base.png';graphic(s).save(background)
 path=SOURCES[s['asset']]
 media=s.get('panels',[{'asset':s['asset'],'crop':s.get('crop'),'box':media_box(s),'inpoint':s.get('inpoint',0)}])
 media=[m for m in media if SOURCES[m['asset']].suffix=='.mp4']
 for i,(a,b) in enumerate(zip(bounds,bounds[1:])):
  dur=(b-a)/FPS;part=WORK/f'{s["id"]}-{i:02d}.mp4';cap=cue_at(cues,(a+b)/2/FPS)
  overlay=WORK/f'{s["id"]}-{i:02d}-overlay.png';decorations(s,cap).save(overlay)
  args=['-loop','1','-framerate',str(FPS),'-threads','1','-thread_queue_size','2','-i',str(background)]
  filters=[];last='0:v';overlay_index=1
  for index,layer in enumerate(media,start=1):
   path=SOURCES[layer['asset']]
   src=probe(str(path));stream=next(x for x in src['streams'] if x['codec_type']=='video')
   total=float(src['format']['duration']);offset=((a-s['start_frame'])/FPS+layer.get('inpoint',0))%total
   args+=['-stream_loop','-1','-ss',str(offset),'-threads','1','-thread_queue_size','2','-i',str(path)]
   crop=layer.get('crop') or [0,0,stream['width'],stream['height']];box=layer['box']
   nw,nh,x,y=frame_dimensions(crop,box,layer['asset']=='sphere');cx,cy,cw,ch=crop
   filters.append(f'[{index}:v]crop={cw}:{ch}:{cx}:{cy},setpts=PTS-STARTPTS,fps=30,scale={nw}:{nh}:flags=lanczos,setsar=1[media{index}]')
   filters.append(f'[{last}][media{index}]overlay={x}:{y}:shortest=1[composite{index}]');last=f'composite{index}';overlay_index=index+1
  args+=['-loop','1','-framerate',str(FPS),'-threads','1','-thread_queue_size','2','-i',str(overlay)]
  filters.append(f'[{last}][{overlay_index}:v]overlay=0:0:shortest=1,format=yuv420p[out]')
  ff(args+['-filter_complex',';'.join(filters),'-map','[out]','-frames:v',str(b-a),'-r','30','-c:v','libx264','-threads','2','-preset','fast','-x264-params','rc-lookahead=8:sync-lookahead=0','-crf','18','-an',str(part)])
  parts.append(part)
 concat=WORK/f'{s["id"]}-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in parts))
 ff(['-f','concat','-safe','0','-i',str(concat),'-c','copy',str(output)])
 return output

def stamp(seconds):
 ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'

def render(manifest):
 shots,cues,audio=timeline(manifest);WORK.mkdir(exist_ok=True);parts=[]
 (OUT/'render-profile.json').write_text(json.dumps({'duration_s':DURATION,'script':str(SCRIPT_PATH),'audio_manifest':str(manifest),'output_dir':str(OUTPUT_DIR),'output_stem':OUTPUT_STEM,'shots':SHOTS},indent=2)+'\n')
 for s in shots:
  parts.append(encode_shot(s,cues));print(f'{s["id"]}: {s["duration_s"]:.2f}s',flush=True)
 concat=WORK/'film-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in parts))
 visual=WORK/'visual.mp4';ff(['-f','concat','-safe','0','-i',str(concat),'-c','copy',str(visual)])
 final=OUTPUT_DIR/f'{OUTPUT_STEM}.mp4'
 ff(['-i',str(visual),'-i',str(audio),'-map','0:v','-map','1:a','-af',f'adelay=100:all=1,apad,atrim=duration={DURATION}','-t',str(DURATION),'-c:v','copy','-bsf:v','setts=pts=round(PTS/512)*512:dts=round(DTS/512)*512:duration=512','-video_track_timescale','15360','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart',str(final)])
 (OUTPUT_DIR/f'{OUTPUT_STEM}.srt').write_text('\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}\n' for i,c in enumerate(cues)))
 used={s['asset'] for s in shots}
 for shot in shots:
  used.update(p['asset'] for p in shot.get('panels',[]))
  if shot.get('motion',{}).get('candidate'):used.add(shot['motion']['candidate'])
  if shot.get('layout')=='close':used.update(['organoid','lightweight-structure','air-water-fish'])
 sources={k:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in SOURCES.items() if k in used}
 (OUT/'source-manifest.json').write_text(json.dumps(sources,indent=2)+'\n')
 print('Final:',final,flush=True)

def preflight(manifest,assets_only=False):
 """Check all shared asset bytes and formats before rendering any frames."""
 checked={}
 for name,pin in ASSET_PINS.items():
  for role,item in [('source',pin),('poster',pin.get('poster'))]:
   if item is None:continue
   path=check_pin(ASSET_MANIFEST.parent,item)
   if item['path'] in checked:continue
   row={'bytes':item['bytes'],'sha256':item['sha256']}
   if path.suffix=='.mp4':
    info=probe(str(path));video=next(x for x in info['streams'] if x['codec_type']=='video')
    row.update(width=video['width'],height=video['height'],duration_s=float(info['format']['duration']))
   elif path.suffix=='.json':
    obj=json.loads(path.read_text())
    if name=='dna':
     record=obj['original_record'];assert len(record['sequence'])==record['length']==1000
     assert hashlib.sha256(record['sequence'].encode()).hexdigest()==record['sha256']
   else:
    with Image.open(path) as im:row.update(width=im.width,height=im.height);im.verify()
   checked[item['path']]=row
 for shot in SHOTS:
  names={shot['asset']}|{p['asset'] for p in shot.get('panels',[])}
  names.update(shot['motion'][k] for k in ['candidate','image'] if shot.get('motion',{}).get(k))
  if shot.get('layout')=='close':names.update(['organoid','lightweight-structure','air-water-fish'])
  assert names<=SOURCES.keys(),f'Missing assets for {shot["id"]}'
  source_image(shot['asset']) if shot.get('layout') not in {'dna','motion'} else None
 assert SHOTS[0]['fixed_start_frame']==0
 starts=[s['fixed_start_frame'] for s in SHOTS]+[round(DURATION*FPS)]
 assert all(a<b for a,b in zip(starts,starts[1:]))
 audio_checked=False
 if not assets_only:timeline(manifest);audio_checked=True
 versions=subprocess.check_output(process_command('ffmpeg',['-version']),text=True).splitlines()[0]
 report={'assets_checked':len(checked),'asset_bytes':sum(r['bytes'] for r in checked.values()),'files':checked,'fonts':FONTS.pins(),'ffmpeg':versions,'audio_checked':audio_checked,'shot_count':len(SHOTS),'duration_s':DURATION}
 (OUT/'preflight.json').write_text(json.dumps(report,indent=2)+'\n')
 print(f'Preflight: {len(checked)} pinned files, {len(SHOTS)} shots; audio checked={audio_checked}',flush=True)
 return report

def configure(profile_path,font_config=None):
 global DURATION,OUTPUT_DIR,OUTPUT_STEM,SCRIPT_PATH,OUT,WORK,SHOTS,SOURCES,SOURCE_POSTERS,ASSET_PINS,ASSET_MANIFEST,AUDIO_MANIFEST,PROFILE_PATH,FONTS
 PROFILE_PATH=profile_path.resolve();profile=json.loads(PROFILE_PATH.read_text())
 ASSET_MANIFEST=(PROFILE_PATH.parent/profile['assets_manifest']).resolve()
 ASSET_PINS,SOURCES,SOURCE_POSTERS=load_assets(ASSET_MANIFEST)
 FONTS=Fonts(font_config);source_image.cache_clear();font.cache_clear();probe.cache_clear()
 DURATION=float(profile['duration_s']);assert 0<DURATION<=180
 OUTPUT_DIR=(PROFILE_PATH.parent/profile['output_dir']).resolve()
 if not OUTPUT_DIR.is_relative_to(ROOT/'.build'):raise ValueError('Build output must stay under the ignored package .build/ directory')
 OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
 OUTPUT_STEM=profile['output_stem'];assert '/' not in OUTPUT_STEM
 SCRIPT_PATH=(PROFILE_PATH.parent/profile['script']).resolve()
 AUDIO_MANIFEST=(PROFILE_PATH.parent/profile['audio_manifest']).resolve()
 SHOTS=profile['shots'];assert len({s['id'] for s in SHOTS})==len(SHOTS)
 OUT=OUTPUT_DIR/profile.get('render_dir','render');OUT.mkdir(exist_ok=True);WORK=OUT/'work'

def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['preflight','preview','timeline','render']);p.add_argument('--profile',type=Path,required=True);p.add_argument('--audio-manifest',type=Path);p.add_argument('--font-config',type=Path);p.add_argument('--assets-only',action='store_true');a=p.parse_args()
 if os.environ.get('DELPHI_VIDEO_RUNNING')=='1':raise SystemExit('Nested renderer refused')
 os.environ['DELPHI_VIDEO_RUNNING']='1';configure(a.profile,a.font_config)
 manifest=a.audio_manifest or AUDIO_MANIFEST
 if a.command=='preflight':preflight(manifest,assets_only=a.assets_only)
 elif a.command=='preview':preview()
 elif a.command=='timeline':timeline(manifest)
 else:preflight(manifest);render(manifest)
if __name__=='__main__':main()
