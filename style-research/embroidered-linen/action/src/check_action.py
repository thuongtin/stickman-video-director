#!/usr/bin/env python3
"""Check world-space invariants, not aesthetic quality or owner acceptance."""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--name',default='animatic');a=ap.parse_args()
data=json.loads((P/f'motion/{a.name}-world.json').read_text());frames=data['frames'];fps=data['fps']
stance_drift=0.0;ground_gap=0.0;grip_error=0.0;max_bone_change=0.0
bones=[(f'{u}_{s}',f'{v}_{s}') for s in ('l','r') for u,v in [('hip','knee'),('knee','ankle'),('shoulder','elbow'),('elbow','wrist')]]
rest={bone:math.dist(frames[0]['joints'][bone[0]],frames[0]['joints'][bone[1]]) for bone in bones}
held_count=0;camera_cuts=[]
for i,f in enumerate(frames):
 for bone in bones:
  max_bone_change=max(max_bone_change,abs(math.dist(f['joints'][bone[0]],f['joints'][bone[1]])-rest[bone]))
 for side in f['contacts']:
  ground_gap=max(ground_gap,abs(f['feet'][side][1]-600))
  if i and side in frames[i-1]['contacts']:
   stance_drift=max(stance_drift,math.dist(f['feet'][side],frames[i-1]['feet'][side]))
 if f['holds']:
  held_count+=1;ball=f['props']['yarn_ball']
  for side,offset in [('r',(-13,10)),('l',(18,-16))]:
   target=[ball[0]+offset[0],ball[1]+offset[1]]
   grip_error=max(grip_error,math.dist(target,f['joints']['wrist_'+side]))
 if i and f['camera']['shot']!=frames[i-1]['camera']['shot']:
  camera_cuts.append({'time':f['time'],'from':frames[i-1]['camera']['shot'],'to':f['camera']['shot'],'world_pelvis_delta':math.dist(f['joints']['pelvis'],frames[i-1]['joints']['pelvis']),'facing_before':frames[i-1]['facing'],'facing_after':f['facing']})
assert max(stance_drift,ground_gap,grip_error,max_bone_change)<1e-8
assert len(camera_cuts)==2 and held_count>fps
assert len({round(f['camera']['cx'],2) for f in frames if f['camera']['shot']==3})>20
assert max(f['joints']['pelvis'][0] for f in frames)-min(f['joints']['pelvis'][0] for f in frames)>700
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,nb_frames,codec_name,r_frame_rate','-of','json',str(P/f'motion/{a.name}.mp4')]))
assert len(meta['streams'])==1
assert int(meta['streams'][0]['nb_frames'])==len(frames)
subprocess.run(['ffmpeg','-v','error','-i',str(P/f'motion/{a.name}.mp4'),'-f','null','-'],check=True)
result={'frames_checked':len(frames),'fps':fps,'duration_seconds':float(meta['format']['duration']),'stance_world_drift_max_px':stance_drift,'stance_ground_gap_max_px':ground_gap,'held_grip_constraint_error_max_px':grip_error,'bone_length_change_max_px':max_bone_change,'held_frames':held_count,'camera_cuts':camera_cuts,'camera_tracking_world_translation':True,'full_decode':'passed','visual_acceptance':'pending','video_sha256':hashlib.sha256((P/f'motion/{a.name}.mp4').read_bytes()).hexdigest()}
(P/f'review/{a.name}-invariants.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
