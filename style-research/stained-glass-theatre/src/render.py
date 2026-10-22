#!/usr/bin/env python3
"""Original 2D stained-glass rig demo. Pillow only; no API, browser or network.
Uses repo pose math and exports the exact drawn joints for its posture gate.
Run from repo root: python3 style-research/stained-glass-theatre/src/render.py
"""
import importlib.util,json,math,random
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('lead',ROOT/'docs/lead-character/render.py'); rig=importlib.util.module_from_spec(spec);spec.loader.exec_module(rig)
rig.LEN.update(torso=60,head=25,upper_arm=32,forearm=30,thigh=45,shin=43,foot=12)
W,H,S=960,540,2; FPS=12; N=120; SCALE=2.15; INK=(16,25,38)
TEAL=[(41,159,172),(58,195,191),(30,104,144),(91,207,195)]
GOLD=[(239,183,81),(253,219,139),(198,131,47),(255,233,171)]
def ease(t):return .5-.5*math.cos(math.pi*max(0,min(1,t)))
def pts(ps):return [(int(x*S),int(y*S)) for x,y in ps]
def polygon(im,ps,color,width=2):
 d=ImageDraw.Draw(im);p=pts(ps)
 # Local tonal bands and stable tiny seeds approximate uneven transmitted glass.
 # A polygon mask keeps highlights inside each pane; lead remains opaque.
 xs=[x for x,y in p];ys=[y for x,y in p];x0,y0,x1,y1=min(xs),min(ys),max(xs)+1,max(ys)+1
 pw,ph=max(1,x1-x0),max(1,y1-y0);tile=Image.new('RGB',(pw,ph));td=ImageDraw.Draw(tile)
 for yy in range(ph):
  q=yy/max(1,ph-1);gain=.58+.55*(1-q)+.12*math.sin(q*math.pi*3)
  c=tuple(min(255,int(v*gain+19*(1-q))) for v in color);td.line((0,yy,pw,yy),fill=c)
 rng=random.Random(sum(color)+pw+ph)
 for _ in range(25):
  xx=rng.randrange(pw);yy=rng.randrange(ph);c=tuple(min(255,int(v*.92+25)) for v in color);td.ellipse((xx,yy,xx+S,yy+S),fill=c)
 mask=Image.new('L',(pw,ph));ImageDraw.Draw(mask).polygon([(x-x0,y-y0) for x,y in p],fill=255);im.paste(tile,(x0,y0),mask)
 d.line(p+[p[0]],fill=INK,width=max(1,int(width*S)),joint='curve')
def pane(im,ps,palette):
 cx=sum(x for x,y in ps)/len(ps);cy=sum(y for x,y in ps)/len(ps)
 for i in range(len(ps)):polygon(im,[ps[i],ps[(i+1)%len(ps)],(cx+2,cy-3)],palette[i%len(palette)],1.2)
 # A small translucent highlight is drawn within each pane, never an external brand motif.
 d=ImageDraw.Draw(im);p=pts(ps);d.line(p+[p[0]],fill=INK,width=3*S,joint='curve')
 for i,(x,y) in enumerate(ps):
  if i%2==0:d.line(pts([(x*.76+cx*.24,y*.76+cy*.24),(cx*.75+x*.25,cy*.75+y*.25)]),fill=(225,239,211),width=S)
def circle(im,p,r,c,outline=True):
 x,y=p;ImageDraw.Draw(im).ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=c,outline=INK if outline else None,width=2*S)
def segment(im,a,b,wide,palette):
 dx=b[0]-a[0];dy=b[1]-a[1];n=math.hypot(dx,dy);px=-dy/n*wide;py=dx/n*wide
 pane(im,[(a[0]+px,a[1]+py),(b[0]+px*.62,b[1]+py*.62),(b[0]-px*.62,b[1]-py*.62),(a[0]-px,a[1]-py)],palette)
def background(light):
 im=Image.new('RGB',(W*S,H*S));d=ImageDraw.Draw(im)
 for y in range(H*S):
  q=y/(H*S);d.line((0,y,W*S,y),fill=(int(10+9*q),int(19+10*q),int(40+14*q)))
 # Sparse theatre wings, not a borrowed window composition.
 for x in (55,905):d.line(pts([(x,0),(x,450)]),fill=(28,46,72),width=4*S)
 d.line(pts([(50,478),(910,478)]),fill=(69,90,110),width=S)
 glow=Image.new('RGB',im.size,(0,0,0));gd=ImageDraw.Draw(glow)
 gd.ellipse(pts([(300,55),(480,465)]),fill=(int(15*light),int(43*light),int(46*light)))
 glow=glow.filter(ImageFilter.GaussianBlur(30*S));gd=ImageDraw.Draw(glow)
 for i,c in enumerate([TEAL[1],GOLD[0],TEAL[2]]):
  x=550+i*115;gd.polygon(pts([(760,411),(x-100,485),(x+65,500)]),fill=tuple(int(v*light*.3) for v in c))
 from PIL import ImageChops
 im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(4*S)))
 return im

def draw(im,j,expr):
 for k in ('l','r'):
  segment(im,j['hip_'+k],j['knee_'+k],7*SCALE,TEAL);segment(im,j['knee_'+k],j['ankle_'+k],5*SCALE,GOLD)
  a=j['ankle_'+k];side=1 if k=='l' else -1;pane(im,[(a[0]-8,a[1]-3),(a[0]+8,a[1]-3),(a[0]+side*20,a[1]+8),(a[0]-side*8,a[1]+8)],TEAL)
 n,p=j['neck'],j['pelvis'];pane(im,[(n[0]-28,n[1]+4),(n[0]+28,n[1]+4),(p[0]+35,p[1]+9),(p[0]-35,p[1]+9)],TEAL)
 pane(im,[(n[0]-28,n[1]+4),(n[0],n[1]-4),(n[0]+28,n[1]+4),(n[0],n[1]+23)],GOLD)
 for k in ('l','r'):
  segment(im,j['shoulder_'+k],j['elbow_'+k],5*SCALE,GOLD);segment(im,j['elbow_'+k],j['wrist_'+k],4*SCALE,GOLD)
  for name in ('shoulder','elbow','knee'):circle(im,j[name+'_'+k],5*SCALE,(57,65,66));circle(im,j[name+'_'+k],1.5*SCALE,(193,196,170),False)
  wr=j['wrist_'+k];circle(im,wr,4*SCALE,(245,227,173))
  if k=='r':circle(im,wr,4.7*SCALE,(228,182,67));circle(im,wr,2.8*SCALE,(245,227,173),False)
 segment(im,j['neck'],j['head'],4,TEAL)
 cx,cy=j['head'];r=14*SCALE;poly=[(cx+math.cos(i*math.pi/6)*r,cy+math.sin(i*math.pi/6)*r*1.22) for i in range(12)];polygon(im,poly,GOLD[1]); polygon(im,[(cx-r*.87,cy-r*.5),(cx-r*.6,cy+r*.85),(cx-r*.15,cy+r*1.15),(cx-r*.43,cy-r*.92)],GOLD[0],1); polygon(im,[(cx+r*.65,cy-r*.8),(cx+r*.87,cy+r*.5),(cx+r*.6,cy+r*.85),(cx+r*.3,cy-r*1.12)],GOLD[3],1)
 for dx in (-9,9):circle(im,(cx+dx,cy-1),2.3,INK,False)
 d=ImageDraw.Draw(im)
 if expr=='surprise':circle(im,(cx,cy+13),4,INK,False)
 else:d.arc(((cx-9)*S,(cy+3)*S,(cx+9)*S,(cy+16)*S),15,165,fill=INK,width=2*S)

def lantern(im,light):
 x,y=760,412;polygon(im,[(x-33,y),(x+33,y),(x+33,470),(x-33,470)],(27,43,65));pal=[tuple(int(v*(.3+.7*light)) for v in c) for c in GOLD]
 pane(im,[(x-26,y-60),(x+26,y-60),(x+26,y),(x-26,y)],pal)
 pane(im,[(x-32,y-60),(x,y-83),(x+32,y-60)],TEAL)
 ImageDraw.Draw(im).arc(((x-8)*S,(y-101)*S,(x+8)*S,(y-80)*S),0,360,fill=(225,182,88),width=3*S)

def pose(frame):
 t=frame/FPS;a=rig.stand_front();a.update(abd_l=16,abd_r=16);state='notice';expr='surprise'
 if t<2.5:
  u=ease(t/2.5);a['abd_r']=16+48*u;a['elb_r']=8+45*u
 elif t<4:
  u=ease((t-2.5)/1.5);a['abd_r']=64-48*u;a['elb_r']=53-45*u;state='release';expr='smile'
 elif t<5.3:
  u=ease((t-4)/1.3);a['abd_r']=16+109*u;a['elb_r']=8+67*u;state='raise';expr='smile'
 elif t<7.5:
  a['abd_r']=125;a['elb_r']=75+8*math.sin((t-5.3)*math.pi*3);state='wave';expr='smile'
 elif t<9:
  u=ease((t-7.5)/1.5);a['abd_r']=125-109*u;a['elb_r']=75-67*u;state='lower';expr='smile'
 else:state='rest';expr='smile'
 return rig.front_pose(a,390,466,SCALE),state,expr

def main():
 frames=[];(OUT/'motion/frames').mkdir(parents=True,exist_ok=True)
 chosen={0:'notice',24:'reach',43:'release',62:'raise',76:'wave',101:'lower',119:'rest'}
 for f in range(N):
  j,state,expr=pose(f);light=.25+.75*ease((f/FPS-.5)/1.2);im=background(light);lantern(im,light);draw(im,j,expr);im=im.resize((W,H),Image.Resampling.LANCZOS)
  im.save(OUT/f'motion/frames/{f:04}.png')
  frame={'facing':'front','joints':j};frames.append(frame)
  if f in chosen:
   name=chosen[f];im.save(OUT/f'gallery/{name}.png');track={'name':name,'fps':FPS,'profile':'rig','head_radius':14*SCALE*1.22,'body_width':56,'hip_width':70,'limb_width':10*SCALE,'hand_length':5*SCALE,'source':'rig','rest':rig.front_pose(rig.stand_front(),390,466,SCALE),'frames':[frame]};(OUT/f'gallery/{name}.json').write_text(json.dumps(track,indent=2))
 track={'name':'Lumen','fps':FPS,'profile':'rig','head_radius':14*SCALE*1.22,'body_width':56,'hip_width':70,'limb_width':10*SCALE,'hand_length':5*SCALE,'source':'rig','rest':rig.front_pose(rig.stand_front(),390,466,SCALE),'frames':frames};(OUT/'motion/track.json').write_text(json.dumps(track,indent=2))
 print(f'Rendered {N} original frames and {len(chosen)} state snapshots')
if __name__=='__main__':main()
