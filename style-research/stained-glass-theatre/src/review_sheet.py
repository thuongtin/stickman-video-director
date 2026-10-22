#!/usr/bin/env python3
"""Run repository risk sheet with exact last-frame seek clamping for 12fps.
The repository clamps to duration-0.05, beyond the last 12fps timestamp.
No score/gate logic is changed. This wrapper fixes extraction bounds and
adds two explicitly selected wave-transition moments to the extraction plan.
"""
import importlib.util,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('risk',ROOT/'tools/risk_sheet/risk_sheet.py');risk=importlib.util.module_from_spec(s);s.loader.exec_module(risk)
original=risk.grab
original_plan=risk.plan
def plan(text,clip):
 moments=original_plan(text,clip)
 moments += [(6.3,"wave peak","Lumen waves with own-right hand clear of face","Lumen: R empty, L empty"),(7.5,"release","Lumen begins lowering own-right hand","Lumen: R empty, L empty")]
 return sorted(moments)
risk.plan=plan
video=OUT/'motion/demo.mp4'
x=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(video)]))
last=float(x['frames'][-1]['best_effort_timestamp_time'])
def grab(video,t,dest,width):return original(video,min(t,last-0.001),dest,width)
risk.grab=grab
out=OUT/'review/risk';out.mkdir(parents=True,exist_ok=True)
risk.run(OUT/'sample.md',1,video,out,8,.5)
(out/'extraction-note.json').write_text(json.dumps({'last_frame_timestamp':last,'seek_ceiling':last-.001,'method':'repository risk_sheet with presentation-timestamp clamp','gate_logic_changed':False,'supplemental_risk_times':[6.3,7.5]},indent=2))
