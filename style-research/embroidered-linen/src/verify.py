#!/usr/bin/env python3
"""Verify delivered artifacts; does not grade aesthetics or imply approval."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parents[1]
r=subprocess.run([sys.executable,str(ROOT/'tools/posture_gate/posture_gate.py'),'check','--json',str(P/'motion/track.json')],capture_output=True,text=True,check=True);gate=json.loads(r.stdout);assert gate['clips'][0]['frames_checked']==120;assert gate['clips'][0]['errors']==0 and gate['clips'][0]['warnings']==0;(P/'motion/gate.json').write_text(r.stdout)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,nb_frames,codec_name,r_frame_rate','-of','json',str(P/'motion/demo.mp4')]))
assert float(meta['format']['duration'])==10 and len(meta['streams'])==1
v=meta['streams'][0];assert (v['width'],v['height'],int(v['nb_frames']))==(960,540,120)
subprocess.run(['ffmpeg','-v','error','-i',str(P/'motion/demo.mp4'),'-f','null','-'],check=True)
(P/'motion/metadata.json').write_text(json.dumps(meta,indent=2))
names=['start','listen','opening','open','welcome','lower','rest'];out=Image.new('RGB',(960,650),'#f0efe9');d=ImageDraw.Draw(out)
for i,n in enumerate(names):
 im=Image.open(P/f'gallery/{n}.png');im.thumbnail((310,180));x=(i%3)*320;y=(i//3)*215;out.paste(im,(x,y+22));d.text((x+8,y+5),n,fill='#101828')
out.save(P/'gallery/contact-sheet.jpg',quality=92)
# Coverage checks concern the exported/drawn rig, not visual appeal.
track=json.loads((P/'motion/track.json').read_text())
selected={'start':0,'listen':15,'opening':40,'open':65,'welcome':75,'lower':96,'rest':119}
for name,index in selected.items():
 state=json.loads((P/f'gallery/{name}.json').read_text())
 assert state['frames'][0]==track['frames'][index]
 assert (P/f'gallery/{name}.png').read_bytes()==(P/f'motion/frames/{index:04}.png').read_bytes()
for side in ('l','r'):
 ankle=track['frames'][0]['joints']['ankle_'+side]
 assert all(frame['joints']['ankle_'+side]==ankle for frame in track['frames'])
assert any(frame['joints']['neck']!=track['frames'][0]['joints']['neck'] for frame in track['frames'])
checks=['src/render.py','src/review_sheet.py','motion/demo.mp4','motion/track.json','concept/options.png','sample.md','gallery/contact-sheet.jpg']
(P/'review/manifest.json').write_text(json.dumps({f:{'bytes':(P/f).stat().st_size,'sha256':hashlib.sha256((P/f).read_bytes()).hexdigest()} for f in checks},indent=2))
print('Artifact checks passed:120frame geometry,960x540,10s,fulldecode,hashes. Not an aesthetic approval.')
