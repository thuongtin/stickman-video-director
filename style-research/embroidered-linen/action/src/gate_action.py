#!/usr/bin/env python3
import argparse,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--name',default='animatic');a=ap.parse_args()
z=json.loads((P/f'motion/{a.name}-world.json').read_text());fps=z['fps']
for label,rows in [('full',z['frames']),('clip1',z['frames'][:10*fps]),('clip2',z['frames'][10*fps:])]:
 frames=[]
 for r in rows:
  f={k:r[k] for k in ('joints','facing','props','holds')};f['supported']=['ankle_'+s for s in r['contacts']];frames.append(f)
 track={'name':'May action '+label,'fps':fps,'profile':'rig','head_radius':47,'body_width':54,'hip_width':62,'limb_width':22,'hand_length':10,'rest':frames[0]['joints'],'frames':frames}
 path=P/f'motion/{a.name}-{label}-posture.json';path.write_text(json.dumps(track,indent=2))
 r=subprocess.run([sys.executable,str(ROOT/'tools/posture_gate/posture_gate.py'),'check','--json',str(path)],capture_output=True,text=True)
 (P/f'review/{a.name}-{label}-gate.json').write_text(r.stdout)
 data=json.loads(r.stdout);print(label,{k:v for k,v in data['clips'][0].items() if k!='issues'})
 if data['clips'][0]['issues']:print(data['clips'][0]['issues'][:8])

 if r.returncode or not data["passed"]:
  raise SystemExit(f"Repository posture gate failed for {label}")
