"""Sequential capped media QA; no scientific computation or listening claim."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
from PIL import Image,ImageDraw
import render_video
from media_runtime import ffmpeg_command, probe as media_probe
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'.build';FILM=None

def ff(args):return subprocess.run(ffmpeg_command(args,loglevel='info'),capture_output=True,text=True,check=True)

def main():
 global ROOT,OUT,FILM
 parser=argparse.ArgumentParser();parser.add_argument('--profile',type=Path,required=True);parser.add_argument('--movie',type=Path);parser.add_argument('--font-config',type=Path);parser.add_argument('--all-shots',action='store_true');args=parser.parse_args()
 render_video.configure(args.profile,args.font_config)
 ROOT=render_video.OUTPUT_DIR;OUT=render_video.OUT;FILM=(args.movie or ROOT/f'{render_video.OUTPUT_STEM}.mp4').resolve()
 duration=render_video.DURATION;frame_count=round(duration*30);asset_stem=render_video.OUTPUT_STEM
 delivery=json.loads(render_video.AUDIO_MANIFEST.read_text());audio_duration=delivery['wav_duration_s']
 if os.environ.get('DELPHI_V2_QA_RUNNING')=='1':raise SystemExit('Nested QA refused')
 os.environ['DELPHI_V2_QA_RUNNING']='1'
 probe=media_probe(FILM)
 video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames']))==(1920,1080,'30/1',frame_count)
 assert float(probe['format']['duration'])==duration and float(video['duration'])==duration and float(video['start_time'])==0
 cuts=json.loads((OUT/'cutlist.json').read_text());cues=json.loads((OUT/'caption-cues.json').read_text())
 assert len(cuts)>0 and sum(s['end_frame']-s['start_frame'] for s in cuts)==frame_count
 for i,s in enumerate(cuts):assert s['end_frame']>s['start_frame'] and (i==0 or s['start_frame']==cuts[i-1]['end_frame'])
 assert cues[0]['start']>=0 and cues[-1]['end']<duration
 result=ff(['-i',str(FILM),'-af','ebur128=peak=true,volumedetect,silencedetect=noise=-45dB:d=0.15','-f','null','-'])
 (OUT/'final-decode-audio.log').write_text(result.stderr)
 peak=float(re.search(r'max_volume: ([-.\d]+) dB',result.stderr).group(1));integrated=float(re.findall(r'I:\s*([-.\d]+) LUFS',result.stderr)[-1]);true_peak=float(re.findall(r'Peak:\s*([-.\d]+) dBFS',result.stderr)[-1]);assert peak<0 and true_peak<0
 silence=[];start=None
 for line in result.stderr.splitlines():
  if 'silence_start:' in line:start=float(line.split('silence_start:')[1].split()[0])
  if 'silence_end:' in line and start is not None:
   end=float(line.split('silence_end:')[1].split()[0]);silence.append({'start':start,'end':end,'duration':end-start});start=None
 internal=[x for x in silence if x['start']>.3 and x['end']<audio_duration+.1]
 frames=OUT/'final-frames';frames.mkdir(exist_ok=True)
 indices=[round((s['start_frame']+s['end_frame'])/2) for s in cuts];indices[0]=60
 # Source color metadata can reinitialize FFmpeg's filter-local frame counter.
 # Seek by the final stream timestamp instead; every requested still is explicit.
 for i,n in enumerate(indices):
  ff(['-ss',str(n/30),'-i',str(FILM),'-frames:v','1',str(frames/f'frame-{i+1:02d}.png')])
 show=[0,2,3,8,9,11,12,15,21,24,25,26,27,30,31,33] if len(cuts)==34 else [round(i*(len(cuts)-1)/15) for i in range(16)]
 if args.all_shots:show=list(range(len(cuts)))
 sheet=Image.new('RGB',(1920,((len(show)+3)//4)*290),'#f2f5f8');d=ImageDraw.Draw(sheet);font=render_video.font(16)
 for i,j in enumerate(show):
  im=Image.open(frames/f'frame-{j+1:02d}.png');sheet.paste(im.resize((480,270)),((i%4)*480,(i//4)*290));d.text(((i%4)*480+10,(i//4)*290+270),f'{indices[j]/30:.1f}s · {cuts[j]["id"]}',fill='#142033',font=font)
 sheet.save(ROOT/f'{asset_stem}-contact-sheet.jpg',quality=95)
 Image.open(frames/'frame-01.png').save(ROOT/f'{asset_stem}-poster.png')
 report={'file':str(FILM),'sha256':hashlib.sha256(FILM.read_bytes()).hexdigest(),'size_bytes':FILM.stat().st_size,'duration_s':duration,'frames':frame_count,'video':'1920x1080 H.264 30fps','audio':'48kHz stereo AAC','full_decode_exit':result.returncode,'shot_count':len(cuts),'caption_cue_count':len(cues),'caption_font_px':52,'caption_max_words':7,'caption_timing':'Provider word timestamps, adjusted with the source audio tempo; matched source text','integrated_loudness_lufs':integrated,'sample_peak_dbfs':peak,'true_peak_dbfs':true_peak,'internal_quiet_gap_max_s_at_minus45db':max((x['duration'] for x in internal),default=0),'internal_quiet_gap_threshold_db':-45,'internal_quiet_gap_minimum_s':.15,'audio_source_duration_s':audio_duration,'audio_start_delay_s':.1,'inserted_between_scene_audio_padding_s':0,'human_listening_review':'Not performed in this tool session','scope':'Numerical and decode QA; scientific source caveats stay visible; biological validation is not claimed'}
 (OUT/'final-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
