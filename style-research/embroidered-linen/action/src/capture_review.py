#!/usr/bin/env python3
"""Capture actual decoded video states and repository risk bursts; no auto sign-off."""
import hashlib, importlib.util, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).resolve().parents[1]; ROOT=P.parents[2]
video=P/'motion/demo.mp4'; out=P/'gallery';out.mkdir(exist_ok=True)
track=json.loads((P/'motion/demo-world.json').read_text());fps=track['fps']
states=[('approach',2),('plant-pickup',4.375),('grip',5.5),('lift',6.5),('carry',11),('plant-place',15.625),('place',17.2083333333),('settle',19.5)]
font=ImageFont.truetype('DejaVuSans.ttf',17); sheet=Image.new('RGB',(1920,600),(245,240,228));d=ImageDraw.Draw(sheet);manifest=[]
for k,(name,t) in enumerate(states):
 i=round(t*fps);row=track['frames'][i];dest=out/f'{name}.png'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select=eq(n\\,{i})','-frames:v','1',str(dest)],check=True)
 data={'name':name,'frame_index':i,'time':i/fps,'world_state':row,'decoded_image_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
 (out/f'{name}.json').write_text(json.dumps(data,indent=2));manifest.append(data)
 im=Image.open(dest);x=(k%4)*480;y=(k//4)*300;sheet.paste(im.resize((480,270)),(x,y));d.text((x+8,y+274),f'{name} | {i/fps:.3f}s | frame {i}',fill=(40,35,30),font=font)
sheet.save(out/'contact-sheet.jpg',quality=93)
(out/'manifest.json').write_text(json.dumps({'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'states':manifest,'selection':'eight distinct action milestones, not a required state quota'},indent=2))
s=importlib.util.spec_from_file_location('risk',ROOT/'tools/risk_sheet/risk_sheet.py');risk=importlib.util.module_from_spec(s);s.loader.exec_module(risk)
original_grab,original_plan=risk.grab,risk.plan
extras={1:[(3.9,'close foot','May closes the trailing foot before pickup','May: both empty'),(5.5,'grip','Both hands contact before lift','May: both holding ball'),(6.5,'lift','Ball clears pickup table','May: both holding ball'),(6.8,'camera cut','Same world action across tracking cut','May: both holding ball')],2:[(5.3,'close foot','May closes trailing foot before placement','May: both holding ball'),(7.2,'release','Ball settles inside basket before withdrawal','May: both releasing ball'),(8.4,'withdraw','Both hands clear the settled ball','May: both empty')]}
def plan(text,clip):return sorted(original_plan(text,clip)+extras[clip])
risk.plan=plan
for clip in (1,2):
 v=P/f'motion/clip{clip}.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str((clip-1)*10),'-i',str(video),'-t','10','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(v)],check=True)
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(v)]));last=float(meta['frames'][-1]['best_effort_timestamp_time'])
 def grab(video,t,dest,width):return original_grab(video,min(t,last-.001),dest,width)
 risk.grab=grab;dest=P/f'review/risk-clip{clip}';dest.mkdir(exist_ok=True);risk.run(P/'sample.md',clip,v,dest,8,.5)
 (dest/'extraction-note.json').write_text(json.dumps({'segment_video_sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'source_video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'source_world_offset_seconds':(clip-1)*10,'last_frame_timestamp':last,'seek_ceiling':last-.001,'method':'repository risk_sheet, plus explicitly selected transition moments; final seeks clamped to actual last presentation timestamp','gate_logic_changed':False,'manual_review':'pending; blank checklist is not a pass'},indent=2))
print('Decoded states and risk sheets captured. Manual visual review remains required.')
