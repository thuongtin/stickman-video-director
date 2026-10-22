#!/usr/bin/env python3
"""Action study: explicit foot plants, two-link IK, constrained prop and camera.
Draft is a flat animatic of the SAME geometry/timeline, not a separate motion.
"""
import argparse
import importlib.util
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1]
STYLE = OUT.parent
ROOT = STYLE.parents[1]
spec = importlib.util.spec_from_file_location('textile', STYLE / 'src/render.py')
art = importlib.util.module_from_spec(spec)
spec.loader.exec_module(art)
W, H, FLOOR, DURATION = 960, 540, 600, 20
UPPER_LEG, LOWER_LEG, UPPER_ARM, LOWER_ARM = 81.4, 81.4, 72, 68
NAVY, OCHRE, CREAM, BROWN = art.NAVY, art.OCHRE, art.CREAM, art.BROWN
DRAFT = False
# Skin embroidery remains visible without deep rope-like grooves.
_original_shade = art.shade
def soft_skin_shade(color, factor):
    if tuple(color) == tuple(CREAM):
        factor = 1 + (factor-1)*.38
    return _original_shade(color, factor)
art.shade = soft_skin_shade


def smooth(u):
    u = max(0, min(1, u))
    return u * u * (3 - 2 * u)


def mix(a, b, u):
    return [a[i] + (b[i] - a[i]) * u for i in range(2)]


def ik(a, b, first, second, bend):
    dx, dy = b[0] - a[0], b[1] - a[1]
    dist = math.hypot(dx, dy)
    if not abs(first-second) < dist < first+second:
        raise ValueError(f'Unreachable IK: {a}, {b}, distance {dist}')
    along = (first*first - second*second + dist*dist) / (2*dist)
    cross = math.sqrt(max(0, first*first - along*along))
    return [a[0] + dx/dist*along + bend*(-dy/dist)*cross,
            a[1] + dy/dist*along + bend*(dx/dist)*cross]


def gait(start, progress, steps, initial_right=None):
    """Alternating swing foot; every stance location is world-space constant."""
    g = max(0, min(steps, progress))
    n = min(steps-1, int(g))
    u = g-n
    pos = {'l': start, 'r': start-60 if initial_right is None else initial_right}
    for k in range(n):
        pos['r' if k % 2 == 0 else 'l'] = start + 60*(k+1)
    side = 'r' if n % 2 == 0 else 'l'
    before, target = pos[side], start + 60*(n+1)
    pos[side] = before + (target-before)*smooth(u)
    feet = {k: [x, FLOOR] for k,x in pos.items()}
    feet[side][1] -= 32 * math.sin(math.pi*u)
    contacts = [k for k in ('l','r') if abs(feet[k][1]-FLOOR) < 1e-6]
    return feet, contacts, g


def state(t):
    foot_angles = {'l':0, 'r':0}
    if t < 3.75:
        progress = .25+3.75*(1-(1-t/3.75)**1.4)
        feet, contacts, g = gait(160, progress, 4)
        x, base_y = 160+60*g, 445
        bob = -2*math.sin(math.pi*g)**2
        phase = 'walk_to_table'
    elif t < 4.35:
        u=smooth((t-3.75)/.6)
        feet={'l':[400,FLOOR],'r':[340+45*u,FLOOR-25*math.sin(math.pi*u)]}
        contacts=['l'] + (['r'] if u in (0,1) else [])
        x,base_y,bob,g,phase=400,445-13*u,0,4,'plant_for_pickup'
        foot_angles['r']=12*math.sin(2*math.pi*u)
    elif t < 7:
        feet={'l':[400,FLOOR],'r':[385,FLOOR]};contacts=['l','r']
        x,base_y,bob,g,phase=400,432+13*smooth((t-6.5)/.5),0,4,'pickup'
    elif t < 15:
        feet,contacts,g=gait(400,9*smooth((t-7)/8),9,initial_right=385)
        x,base_y,bob,phase=400+60*g,445,-2*math.sin(math.pi*g)**2,'carry'
    elif t < 15.6:
        u=smooth((t-15)/.6)
        feet={'r':[940,FLOOR],'l':[880+45*u,FLOOR-25*math.sin(math.pi*u)]}
        contacts=['r'] + (['l'] if u in (0,1) else [])
        x,base_y,bob,g,phase=940,445-13*u,0,9,'plant_for_place'
        foot_angles['l']=12*math.sin(2*math.pi*u)
    else:
        feet={'r':[940,FLOOR],'l':[925,FLOOR]};contacts=['l','r']
        x,base_y,bob,g,phase=940,432,0,9,'place_and_release'
    if phase in ('walk_to_table','carry'):
        active='r' if int(g)%2==0 else 'l'
        foot_angles[active]=12*math.sin(2*math.pi*(g-int(g)))
    lean,crouch=5,0
    if 4.35 <= t < 5.5:
        u=smooth((t-4.35)/1.15);lean,crouch=5+7*u,6*u
    elif 5.5 <= t < 6.5:
        u=smooth(t-5.5);lean,crouch=12-7*u,6*(1-u)
    elif 6.5 <= t < 7:
        lean=5+3*smooth((t-6.5)/.5)
    elif 7 <= t < 15.6:
        lean=8
    elif 15.6 <= t < 17.2:
        u=smooth((t-15.6)/1.6);lean,crouch=8+8*u,16*u
    elif t >= 17.2:
        u=smooth((t-17.2)/1.2);lean,crouch=16-14*u,16*(1-u)
    nod=7*math.sin(math.pi*max(0,min(1,(t-18.4)/1.2))) if t>=18.4 else 0
    pelvis=[x,base_y+bob+crouch]
    a=math.radians(lean);ha=math.radians(lean+nod)
    neck=[x+math.sin(a)*127.6,pelvis[1]-math.cos(a)*127.6]
    head=[neck[0]+math.sin(ha)*59.4,neck[1]-math.cos(ha)*59.4]
    j={'pelvis':pelvis,'neck':neck,'head':head}
    for side in ('l','r'):
        ankle=[feet[side][0],feet[side][1]-9]
        j['hip_'+side]=pelvis[:];j['ankle_'+side]=ankle
        j['toe_'+side]=art.rotate([ankle[0]+18,ankle[1]+8],ankle,foot_angles[side])
        j['knee_'+side]=ik(pelvis,ankle,UPPER_LEG,LOWER_LEG,-1)
        j['shoulder_'+side]=[neck[0]-math.sin(a)*10,neck[1]+math.cos(a)*10]
    ball=[490,432];held=5.5<=t<17.2
    if 5.5<=t<6.5:
        ball=mix([490,432],[465,395],smooth(t-5.5))
    elif 6.5<=t<15.6:
        ball=[x+65,395+bob*.5]
    elif 15.6<=t<17.2:
        ball=mix([1005,395],[1035,450],smooth((t-15.6)/1.6))
    elif t>=17.2:
        ball=[1035,450]
    grips={'r':[ball[0]-13,ball[1]+10],'l':[ball[0]+18,ball[1]-16]}
    for side in ('l','r'):
        swing=(1 if side=='r' else -1)*28*math.sin(math.pi*g)
        rest=[x+24+swing,pelvis[1]-12]
        if t<4.35:
            target=rest
        elif t<5.5:
            target=mix([x+24,pelvis[1]-12],grips[side],smooth((t-4.35)/1.15))
        elif t<17.2:
            target=grips[side]
        elif t<18.4:
            u=smooth((t-17.2)/1.2)
            target=mix(grips[side],[x+20,pelvis[1]+14],u)
            target[1]-=(35 if side=='l' else 12)*math.sin(math.pi*u)
        else:
            target=[x+20,pelvis[1]+14]
        j['elbow_'+side]=ik(j['shoulder_'+side],target,UPPER_ARM,LOWER_ARM,1)
        j['wrist_'+side]=target
    shot=1 if t<4.4 else 2 if t<6.8 else 3
    camera={'shot':shot,'scale':.75 if shot==1 else 1.4 if shot==2 else .95,
            'cx':640 if shot==1 else 460 if shot==2 else x+120,
            'cy':360 if shot==1 else 370 if shot==2 else 400}
    return j,ball,held,feet,contacts,phase,camera,lean


def poly(im, points, color, angle=0):
    if DRAFT:
        ImageDraw.Draw(im).polygon([art.pxy(p) for p in points],fill=color)
    else:
        art.satin(im,points,color,angle)


def oval(im, p, rx, ry, color, angle=0):
    if DRAFT:
        points=[art.rotate((p[0]+rx*math.cos(k*math.pi/18),p[1]+ry*math.sin(k*math.pi/18)),p,angle) for k in range(36)]
        ImageDraw.Draw(im).polygon([art.pxy(q) for q in points],fill=color)
    else:
        art.ellipse(im,p,rx,ry,color,angle)


def limb(im,a,b,r,color):
    if DRAFT:
        ImageDraw.Draw(im).line([art.pxy(a),art.pxy(b)],fill=color,width=round(2*r*art.SS))
        oval(im,b,r,r,color)
    else:
        art.limb(im,a,b,r,color)


def table(im,x,top,width):
    poly(im,[(x-width/2,top),(x+width/2,top),(x+width/2,top+12),(x-width/2,top+12)],BROWN,3)
    for dx in (-width/2+10,width/2-10):
        poly(im,[(x+dx-5,top+10),(x+dx+5,top+10),(x+dx+5,FLOOR-30),(x+dx-5,FLOOR-30)],BROWN,0)


def basket(im,front=False):
    x,y = 1035,485
    if not front:
        oval(im,(x,y-48),52,13,(120,85,45))
    else:
        poly(im,[(x-52,y-43),(x-42,y),(x+42,y),(x+52,y-43)],(160,118,67),0)
        for off in range(-36,37,12):
            art.cord(im,[(x+off,y-41),(x+off*.82,y-1)],(191,148,92),2)
        art.cord(im,[(x-51,y-44),(x,y-38),(x+51,y-44)],(193,148,86),5)


def yarn(im,p):
    oval(im,p,20,20,(168,68,39))
    for i in range(-3,4):
        curve=[]
        for k in range(15):
            u=k/14
            xx=-17+34*u
            yy=i*4+5*math.sin(math.pi*u)
            if xx*xx+yy*yy < 19*19:
                curve.append((p[0]+xx,p[1]+yy))
        if len(curve)>1:
            art.cord(im,curve,(205,107,66),1.5)


def arm(im,j,side):
    c = art.shade(NAVY,.83) if side=='l' else NAVY
    limb(im,j['shoulder_'+side],j['elbow_'+side],11,c)
    limb(im,j['elbow_'+side],j['wrist_'+side],9,c)
    oval(im,j['wrist_'+side],9,10,CREAM)
    if side=='r':
        q=j['wrist_r']
        art.cord(im,[(q[0]-7,q[1]-6),(q[0],q[1]-3),(q[0]+7,q[1]-6)],(174,86,40),2.5)


def character(im,j,lean,t):
    for side in ('l','r'):
        c=art.shade(OCHRE,.8) if side=='l' else OCHRE
        limb(im,j['hip_'+side],j['knee_'+side],11,c)
        limb(im,j['knee_'+side],j['ankle_'+side],10,c)
        q=j['ankle_'+side]
        angle=math.degrees(math.atan2(j['toe_'+side][1]-q[1],j['toe_'+side][0]-q[0]))-math.degrees(math.atan2(8,18))
        oval(im,art.rotate((q[0]+5,q[1]+3),q,angle),19,6,BROWN,angle)
    arm(im,j,'l')
    n,p=j['neck'],j['pelvis']
    poly(im,[(n[0]-19,n[1]+4),(n[0]+22,n[1]+11),(p[0]+32,p[1]+19),(p[0]-29,p[1]+19)],NAVY,8)
    limb(im,[n[0],n[1]+13],j['head'],8,CREAM)
    h=j['head']
    oval(im,h,30,39,CREAM,lean)
    # Facing right: one visible eye and a small profile nose, no front-view slide.
    oval(im,(h[0]+25,h[1]+5),10,5,CREAM)
    hp=[(-29,-17),(-30,-35),(-17,-46),(5,-46),(25,-36),(18,-25),(-2,-28)]
    poly(im,[(h[0]+x,h[1]+y) for x,y in hp],BROWN,-20)
    oval(im,(h[0]+15,h[1]-2),2,3,BROWN)
    art.cord(im,[(h[0]+15,h[1]+15),(h[0]+22,h[1]+18),(h[0]+27,h[1]+16)],BROWN,1.4)


def background():
    if DRAFT:
        im=Image.new('RGB',(1800*art.SS,800*art.SS),(227,215,188))
    else:
        art.W,art.H=1800,800
        im=art.background()
        # Historical background's old baseline is covered by a cloth tile.
        im.paste(im.crop((0,0,1800*art.SS,24*art.SS)),(0,464*art.SS))
    # The furniture feet stand in a rear depth lane. May walks in front.
    d=ImageDraw.Draw(im)
    d.rectangle((0,558*art.SS,1800*art.SS,625*art.SS),fill=(219,205,177))
    if not DRAFT:
        for x in range(0,1800*art.SS,6):
            d.line((x,558*art.SS,x,625*art.SS),fill=(212,198,170),width=2)
        for y in range(558*art.SS,625*art.SS,6):
            d.line((0,y,1800*art.SS,y),fill=(224,211,183),width=1)
    for x in range(20,1780,20):
        art.cord(im,[(x,FLOOR),(x+11,FLOOR)],(163,141,99),1.4)
    table(im,490,452,120)
    table(im,1035,485,135)
    for x in (440,540,977.5,1092.5):
        oval(im,(x,FLOOR-29),9,2,(162,140,100))
    return im


def camera_frame(im,c):
    s=c['scale']
    matrix=(1/s,0,(c['cx']-W/2/s)*art.SS,0,1/s,(c['cy']-H/2/s)*art.SS)
    return im.transform((W*art.SS,H*art.SS),Image.Transform.AFFINE,matrix,Image.Resampling.BICUBIC).resize((W,H),Image.Resampling.LANCZOS)


def main():
    global DRAFT
    ap=argparse.ArgumentParser()
    ap.add_argument('--draft',action='store_true')
    args=ap.parse_args()
    DRAFT=args.draft
    art.SS=1 if DRAFT else 2
    fps=12 if DRAFT else 24
    name='animatic' if DRAFT else 'demo'
    dest=OUT/'motion'/('draft-frames' if DRAFT else 'frames')
    dest.mkdir(parents=True,exist_ok=True)
    base=background()
    records=[]
    for f in range(DURATION*fps):
        t=f/fps
        j,ball,held,feet,contacts,phase,c,lean=state(t)
        im=base.copy()
        basket(im)
        character(im,j,lean,t)
        yarn(im,ball)
        arm(im,j,'r')
        basket(im,True)
        camera_frame(im,c).save(dest/f'{f:04}.png')
        records.append({'time':t,'joints':j,'facing':'right','props':{'yarn_ball':ball},
                        'holds':{'yarn_ball':['l','r']} if held else {},'contacts':contacts,
                        'feet':feet,'phase':phase,'camera':c})
    (OUT/'motion'/f'{name}-world.json').write_text(json.dumps({'fps':fps,'frames':records},indent=2))
    subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(fps),'-i',str(dest/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-movflags','+faststart',str(OUT/'motion'/f'{name}.mp4')],check=True)
    print(f'{name}: {len(records)} frames at {fps} FPS, {DURATION}s, three shots.')


if __name__=='__main__':
    main()
