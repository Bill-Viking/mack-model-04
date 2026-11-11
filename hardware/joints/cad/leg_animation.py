"""J04-L02-V01: offline CAD kinematic illustration, never a dynamics proof.

ASSUMES: rigid frames and benchmark pad geometry from placement A. Ground/slip
use the nominal pad centre in XY and its lowest rigid-box support in Z. This
keeps the prototype pad above the grid without claiming a no-slip contact patch.
Concept rounding is appearance only; its ground datum remains this same nominal
pad. No collision, stability, torque, speed or load acceptance is performed.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import random
import re

import build123d as cad
import numpy as np
import leg_packaging as lp

HERE = Path(__file__).resolve().parent
PARAMETERS = HERE/'j04-l02.candidate-A-under.json'
OUT = HERE/'exports/l02-animation'
SCENES = ('leg', 'overview', 'walk-prototype', 'walk-concept')
LEGS = {'FL': (1, 1, .25), 'FR': (1, -1, .75),
        'RL': (-1, 1, 0.), 'RR': (-1, -1, .5)}
TOL = 1e-5


def forward(m, q):
    """The model's Rx(a) Ry(b) Ry(c) chain, in neutral front-left coordinates."""
    a, b, c = q
    p2 = lp.add(m.P1, lp.rx(lp.sub(m.P2, m.P1), a))
    p3 = lp.add(p2, lp.rx(lp.ry([0, 0, -m.p['links']['L1']], b), a))
    p4 = lp.add(p3, lp.rx(lp.ry([0, 0, -m.p['links']['L2']], b+c), a))
    return np.array([p2, p3, p4])


def foot(m, q):
    a, b, c = q
    size = m.p['foot']
    centre = forward(m, q)[2]+lp.rx(lp.ry([0, 0, -size['Z']/2], b+c), a)
    ar, br = math.radians(a), math.radians(b+c)
    support = (abs(math.cos(ar)*math.sin(br))*size['X']/2
               +abs(math.sin(ar))*size['Y']/2
               +abs(math.cos(ar)*math.cos(br))*size['Z']/2)
    return np.array([centre[0], centre[1], centre[2]-support])


def solve(m, target, previous):
    q = np.array(previous, dtype=float)
    for _ in range(80):
        value = foot(m, q)
        error = np.array(target)-value
        if np.linalg.norm(error) <= TOL:
            return q, float(np.linalg.norm(error))
        h = .0001
        jac = np.column_stack([(foot(m, q+np.eye(3)[i]*h)-value)/h for i in range(3)])
        delta = jac.T@np.linalg.solve(jac@jac.T+np.eye(3)*.0025, error)
        delta *= min(1., 8./max(np.linalg.norm(delta), 1e-12))
        q += delta
    raise ValueError(f'IK did not converge: {np.linalg.norm(np.array(target)-foot(m, q)):.6f} mm')


def path(phase, stride):
    if phase < .2:
        s = phase/.2
        return -stride/2+stride*(1-math.cos(math.pi*s))/2, 10*math.sin(math.pi*s)**2, True
    return stride/2-stride*(phase-.2)/.8, 0., False


def phase_of(t):
    # Canonical boundaries prevent Python/JS remainder roundoff changing swing state.
    return round(t % 1, 12) % 1


def sway(t):
    for _, (_, sy, offset) in LEGS.items():
        phase = phase_of(t-offset)
        if phase < .2:
            return -sy*5*math.sin(math.pi*phase/.2)**2
    return 0.


def cycle(m, scene, n, stride):
    stance = np.array([m.p['poses']['stance'][k] for k in 'abc'])
    base = foot(m, stance)
    previous = {leg: stance.copy() for leg in LEGS}
    rows = []
    for index in range(n):
        t = index/n
        dy = sway(t) if scene.startswith('walk') else 0.
        dz = -15*math.sin(math.pi*t)**2 if scene == 'overview' else 0.
        row = dict(phase=t, body=[0., dy, dz], legs={}, label='')
        for leg, (sx, sy, offset) in LEGS.items():
            if scene == 'leg' and leg != 'FL':
                continue
            target = base.copy()
            swing = False
            if scene == 'leg':
                section, u = min(3, int(t*4)), phase_of(t*4)
                row['label'] = ('J1 hip spread', 'J2 hip swing', 'J3 knee', 'One step')[section]
                if section < 3:
                    q = stance.copy()
                    q[section] += (15, 25, 30)[section]*math.sin(2*math.pi*u)
                    target = foot(m, q)
                    error = 0.
                else:
                    dx, lift, swing = path(phase_of(u+.6), stride)
                    target += [dx, 0, lift]
                    q, error = solve(m, target, previous[leg])
            elif scene == 'overview':
                target[2] -= dz
                q, error = solve(m, target, previous[leg])
            else:
                dx, lift, swing = path(phase_of(t-offset), stride)
                target += [sx*dx, -sy*dy, lift]
                q, error = solve(m, target, previous[leg])
            previous[leg] = q
            row['legs'][leg] = dict(q=q.tolist(), target=target.tolist(), error=error, swing=swing)
        rows.append(row)
    return rows


def within(m, rows):
    return all(m.p['poses']['sweep'][axis][0]-1e-8 <= leg['q'][i] <= m.p['poses']['sweep'][axis][1]+1e-8
               for row in rows for leg in row['legs'].values() for i, axis in enumerate('abc'))


def check(m, stride):
    reports = {}
    for scene in SCENES:
        rows = cycle(m, scene, 60, stride)
        legs, ground_heights, tracks, all_slips = {}, [], [], []
        for name, (sx, sy, offset) in LEGS.items():
            samples = [row['legs'][name] for row in rows if name in row['legs']]
            if not samples:
                continue
            angles = np.array([s['q'] for s in samples])
            limits = {axis: m.p['poses']['sweep'][axis][:2] for axis in 'abc'}
            ranges = {axis: [float(angles[:, i].min()), float(angles[:, i].max())] for i, axis in enumerate('abc')}
            error = max(s['error'] for s in samples)
            slip = 0.
            stance_heights = []
            if scene.startswith('walk'):
                # A stance's absolute ground X has one constant for each unwrapped
                # local cycle. This also checks stance intervals crossing frame 0.
                base = foot(m, [m.p['poses']['stance'][k] for k in 'abc'])
                for row in rows:
                    leg = row['legs'][name]
                    if leg['swing']:
                        continue
                    t = row['phase']
                    point = foot(m, leg['q'])
                    local_cycle = math.floor(t-offset)
                    expected = np.array([sx*base[0]+stride/2+stride/.8*(offset+local_cycle+.2), sy*base[1]])
                    actual = np.array([sx*point[0]+stride/.8*t, sy*point[1]+row['body'][1]])
                    slip = max(slip, float(np.linalg.norm(actual-expected)))
                    stance_heights.append(float(point[2]-base[2]))
                all_slips.append(slip)
                ground_heights += stance_heights
            elif scene == 'overview':
                base = foot(m, [m.p['poses']['stance'][k] for k in 'abc'])
                stance_heights = [float(foot(m, row['legs'][name]['q'])[2]+row['body'][2]-base[2]) for row in rows]
                ground_heights += stance_heights
            legs[name] = dict(max_ik_error_mm=error, joint_ranges_deg=ranges, sweep_limits_deg=limits,
                              all_inside_sweep=all(limits[k][0]-1e-8 <= ranges[k][0] and ranges[k][1] <= limits[k][1]+1e-8 for k in 'abc'),
                              max_stance_slip_mm=slip if scene.startswith('walk') else None,
                              minimum_stance_foot_height_mm=min(stance_heights) if stance_heights else None,
                              maximum_stance_foot_height_mm=max(stance_heights) if stance_heights else None)
        for row in rows:
            if 'FL' in row['legs'] and 'FR' in row['legs']:
                tracks.append(float(foot(m, row['legs']['FL']['q'])[1]+foot(m, row['legs']['FR']['q'])[1]))
        report = dict(frames=60, legs=legs, max_ik_error_mm=max(v['max_ik_error_mm'] for v in legs.values()),
                      all_inside_sweep=within(m, rows),
                      foot_centre_track_width_mm=[min(tracks), max(tracks)] if tracks else None)
        if scene.startswith('walk'):
            report.update(stride_used_mm=stride, lift_mm=10, body_speed_mm_per_cycle=stride/.8,
                          max_stance_slip_mm=max(all_slips), minimum_stance_foot_height_mm=min(ground_heights),
                          max_absolute_stance_height_mm=max(abs(h) for h in ground_heights))
            assert report['max_stance_slip_mm'] < .2, 'Stance slip must be under 0.2 mm'
            assert report['max_absolute_stance_height_mm'] <= .2, 'Stance height must be within 0.2 mm of ground'
        assert report['max_ik_error_mm'] <= .05, 'IK error must be under 0.05 mm'
        assert report['all_inside_sweep'], f'{scene}: joint outside viewing sweep'
        reports[scene] = report
    return reports


def rounded(shape, radius):
    try:
        return cad.fillet(shape.edges(), radius)
    except (ValueError, RuntimeError):
        return shape


def concept(m):
    p = m.p
    parts = []
    def put(name, shape, frame, color, shared=False):
        parts.append((name, shape, frame, color, shared))
    dx, dy, height = p['body']['depth_X']/2, p['body']['width_Y']/2, p['body']['height_Z']
    shell = rounded(lp.box(-dx, dx, -dy, dy, 0, height), 3)
    shell -= lp.box(-dx+2, dx-2, -dy+2, dy-2, 2, height-2)
    shell -= lp.box(dx-2, dx+1, -26, 26, 59, 99)
    shell -= lp.box(dx-1, dx+1, -20, 20, 48, 49.5)
    put('concept_shell', shell, 'body', '#d8c6a6', True)
    put('concept_screen', lp.box(dx-1.9, dx-1.5, -26, 26, 59, 99), 'body', '#253139', True)
    put('concept_slot', lp.box(dx-.9, dx-.6, -20, 20, 48, 49.5), 'body', '#303b40', True)
    put('concept_skirt', rounded(lp.box(-dx, dx, -dy, dy, -6, 0), 2), 'body', '#c6b697', True)
    put('concept_spread_cap', lp.cyl(m.P1, [1, 0, 0], -4, 4, 9), 'body', '#586771')
    delta = lp.sub(m.P2, m.P1)
    put('concept_carrier', lp.cyl(m.P1, lp.mul(delta, 1/lp.norm(delta)), 0, lp.norm(delta), 5), 'carrier', '#bcae94')
    for name, point, frame in [('hip_cap', m.P2, 'carrier'), ('knee_cap', m.P3, 'upper')]:
        put('concept_'+name, lp.cyl(point, [0, 1, 0], -5, 5, 9), frame, '#586771')
    for name, start, end, frame in [('upper_bar', m.P2, m.P3, 'upper'), ('lower_bar', m.P3, m.P4, 'lower')]:
        x, y, _ = start
        bar = lp.box(x-7, x+7, y-4, y+4, end[2], start[2])
        put('concept_'+name, rounded(bar, 3), frame, '#c3b295')
    x, y, z = m.P4
    f = p['foot']
    put('concept_foot', rounded(lp.box(x-f['X']/2, x+f['X']/2, y-f['Y']/2, y+f['Y']/2, z-f['Z'], z), 2), 'lower', '#29353a')
    return parts


def meshes(parts):
    result = []
    for name, shape, frame, color, shared in parts:
        assert shape.is_valid and len(shape.solids()) > 0, name
        vertices, triangles = shape.tessellate(.25, .2)
        result.append(dict(name=name, frame=frame, color=color, shared=shared,
                           vertices=[[round(v.X, 6), round(v.Y, 6), round(v.Z, 6)] for v in vertices],
                           triangles=triangles))
    return result


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# The page retains the template's palette, orthographic camera, flat-lit shader
# and CPU poseVertex transforms. There are no libraries, external assets or fetches.
PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mack · Kinematic animation</title><style>/* BASE_STYLE */
main{display:block;max-width:1200px}.scene{height:auto;aspect-ratio:4/3;min-height:0}.workspace{padding:20px 24px}
button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.toolbar{justify-content:space-between}.scenes{display:flex;flex-wrap:wrap;gap:7px}.transport{display:flex;align-items:center;gap:8px}
.state{font:12px ui-monospace,monospace;color:var(--muted)}#failure{padding:14px 0;color:#824235}#failure:empty{display:none}
@media(max-width:600px){.workspace{padding:10px}.transport{flex-wrap:wrap}header{padding:16px}.state{font-size:11px}}
</style></head><body>
<header><div><div class="plate">M.A.C. Model 04 / Mechanical development</div><h1>Kinematic design study</h1><div class="muted">Placement A · direct knee · proposed dimensions</div></div><div class="badge">ILLUSTRATION ONLY<br>NO PHYSICAL TESTING</div></header>
<main><section class="workspace"><div class="scene"><canvas id="frame" tabindex="0" aria-label="Kinematic CAD illustration. Drag to rotate; arrow keys rotate; plus and minus zoom."></canvas></div>
<div class="toolbar"><div class="scenes" aria-label="Animation scenes">
<button data-scene="leg">One leg</button><button data-scene="overview">Four-leg layout</button><button data-scene="walk-prototype">Prototype walk</button><button data-scene="walk-concept">Concept walk</button></div>
<div class="transport"><button id="play" aria-pressed="true">Pause</button><button id="look">Show concept</button><button id="reset">Reset view</button></div></div>
<div class="state" id="state" role="status">Preparing the kinematic illustration…</div><div id="failure" role="alert"></div>
</section></main><footer>J04-L02-V01 · Offline · Viewing sweeps are not actuator limits · Drag to rotate · Scroll to zoom</footer>
<script>
'use strict';
const data=/* MODEL_DATA */;
/* MOTION_JS */
const titles={'leg':'How one leg moves','overview':'Proposed layout, four legs','walk-prototype':'First prototype layout: walk cycle','walk-concept':'Final-design concept: walk cycle'};
const query=new URLSearchParams(location.search),capture=query.has('capture');
const $=id=>document.getElementById(id);
function fail(error){const message=String(error.message||error);document.title='CAPTURE ERROR '+message;$('failure').textContent='The animation could not be drawn: '+message;$('state').textContent='Animation unavailable.';}
try{
const canvas=$('frame'),ctx=canvas.getContext('2d'),surface=document.createElement('canvas');
const gl=surface.getContext('webgl',{antialias:true,alpha:false,preserveDrawingBuffer:true});
if(!gl||!ctx)throw new Error('WebGL or 2D canvas unavailable');
/* SHADER_JS */
gl.disable(gl.CULL_FACE); // Both mirrored windings render with the template's two-sided lighting.
let width=800,height=600,scene='leg',frame=0,playing=true,drag=null,yawOffset=0,pitch=.3,zoom=1,cycleRows=[];
if(query.has('yaw'))yawOffset=parseFloat(query.get('yaw'))||0;if(query.has('zoom'))zoom=Math.max(.45,Math.min(2.5,parseFloat(query.get('zoom'))||1));
const normalFrames=240;
function setScene(name,n=normalFrames){
 if(!titles[name])throw new Error('Unknown scene '+name);
 scene=name;frame=0;cycleRows=makeCycle(name,n,data.stride);
 for(const button of document.querySelectorAll('[data-scene]'))button.setAttribute('aria-pressed',String(button.dataset.scene===scene));
 $('look').hidden=!scene.startsWith('walk');$('look').textContent=scene==='walk-concept'?'Show prototype':'Show concept';
 $('state').textContent=(playing?'Playing':'Paused')+' · '+titles[scene]+(scene.startsWith('walk')?' · '+data.stride+' mm stride · 10 mm lift':'');
}
function rotateAt(v,origin,axis,degrees){
 const t=degrees*Math.PI/180,co=Math.cos(t),si=Math.sin(t),q=v.map((x,i)=>x-origin[i]);
 const r=axis==='X'?[q[0],q[1]*co-q[2]*si,q[1]*si+q[2]*co]:[q[0]*co+q[2]*si,q[1],-q[0]*si+q[2]*co];
 return r.map((x,i)=>x+origin[i]);
}
function poseVertex(vertex,part,q){
 let v=vertex;
 if(part.frame==='lower')v=rotateAt(v,data.P3,'Y',q[2]);
 if(part.frame==='upper'||part.frame==='lower')v=rotateAt(v,data.P2,'Y',q[1]);
 if(part.frame==='carrier'||part.frame==='upper'||part.frame==='lower')v=rotateAt(v,data.P1,'X',q[0]);
 return v;
}
function draw(index){
 const row=cycleRows[index],t=row.phase,concept=scene==='walk-concept',parts=data.meshes[concept?'concept':'prototype'];
 const yaw=.72+yawOffset+(scene==='overview'?2*Math.PI*t:scene.startsWith('walk')?5*Math.PI/180*Math.sin(2*Math.PI*t):0);
 const span=285,centre=[0,0,(data.bodyHeight+data.ground)/2];
 function view(v){const x=Math.cos(yaw)*v[0]+Math.sin(yaw)*v[2],d=-Math.sin(yaw)*v[0]+Math.cos(yaw)*v[2];return [x,Math.cos(pitch)*v[1]-Math.sin(pitch)*d,Math.sin(pitch)*v[1]+Math.cos(pitch)*d];}
 function camera(v){return view([v[0]-centre[0],v[2]-centre[2],-v[1]+centre[1]]);}
 const scale=Math.min(width/(span*1.45),height/(span*1.3))*zoom;
 const project=p=>[2*p[0]*scale/width,2*(p[1]*scale-12)/height,-p[2]/(span*4)];
 gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
 const lines=[],grid=scene.startsWith('walk')?data.stride/.8:25;
 const shift=scene.startsWith('walk')?data.stride/.8*t:0,extent=grid*18;
 function line(a,b,color){for(const v of [a,b])lines.push(...project(camera(v)),...color);}
 // Scroll one grid spacing per loop; extra off-screen lines make the seam periodic.
 for(let i=-18;i<=19;i++){
  line([i*grid-shift,-extent,data.ground],[i*grid-shift,extent,data.ground],[.83,.85,.81]);
  line([-extent,i*grid,data.ground],[extent,i*grid,data.ground],[.83,.85,.81]);
 }
 if(scene==='leg'){
  const lo=[-data.bodyDepth/2,-data.bodyWidth/2,0],hi=[data.bodyDepth/2,data.bodyWidth/2,data.bodyHeight];
  for(let i=0;i<8;i++)for(let axis=0;axis<3;axis++)if(!(i&(1<<axis))){let a=[0,1,2].map(k=>i&(1<<k)?hi[k]:lo[k]),b=a.slice();b[axis]=hi[axis];line(a,b,[.75,.77,.72]);}
 }
 gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(lines),gl.DYNAMIC_DRAW);gl.drawArrays(gl.LINES,0,lines.length/6);
 const vertices=[];
 for(const part of parts){
  if(scene==='leg'&&part.shared)continue;
  const instances=part.shared?['FL']:Object.keys(row.legs);
  for(const name of instances){
   const [sx,sy]=LEGS[name],q=row.legs[name].q;
   const points=part.vertices.map(v=>{let p=part.shared?v:poseVertex(v,part,q);return camera([p[0]*(part.shared?1:sx),p[1]*(part.shared?1:sy)+row.body[1],p[2]+row.body[2]]);});
   for(const indices of part.triangles){
    const p=indices.map(i=>points[i]),u=p[1].map((v,i)=>v-p[0][i]),v=p[2].map((v,i)=>v-p[0][i]);
    const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],length=Math.hypot(...n);if(length<1e-9)continue;
    const light=.56+.36*Math.abs((-.3*n[0]+.5*n[1]+.81*n[2])/length);
    const rgb=[1,3,5].map(i=>Math.min(1,(parseInt(part.color.slice(i,i+2),16)*light+15)/255));
    for(const vertex of p)vertices.push(...project(vertex),...rgb);
   }
  }
 }
 gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(vertices),gl.DYNAMIC_DRAW);gl.drawArrays(gl.TRIANGLES,0,vertices.length/6);
 const status=gl.getError();if(status!==gl.NO_ERROR)throw new Error('WebGL draw error '+status);
 ctx.drawImage(surface,0,0,width,height);
 const margin=Math.max(18,width*.03),font='-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif';
 // Opaque quiet bands ensure the scope text survives every angle and PNG export.
 ctx.fillStyle='#f5f3e9';ctx.fillRect(0,0,width,83);ctx.fillRect(0,height-71,width,71);
 ctx.fillStyle='#5d6d70';ctx.font='11px '+font;ctx.fillText('M.A.C. MODEL 04 · J04-L02 · DESIGN STUDY',margin,27);
 ctx.fillStyle='#283c45';ctx.font='500 22px '+font;ctx.fillText(titles[scene],margin,56);
 if(scene==='leg'){ctx.font='14px '+font;ctx.fillStyle='#356c7a';ctx.fillText(row.label,margin,105);}
 ctx.fillStyle='#283c45';ctx.font='12px '+font;
 ctx.fillText('Kinematic animation from CAD. No physics. Nothing is built or tested yet.',margin,height-42);
 ctx.fillStyle='#5d6d70';ctx.fillText(concept?'Appearance concept only.':'Benchmark actuator blocks, not selected parts.',margin,height-21);
}
function size(w,h){width=w;height=h;canvas.width=surface.width=w;canvas.height=surface.height=h;gl.viewport(0,0,w,h);}
if(capture){
 // One zero-delay timer lets the DOM exist. There is no RAF, observer or other timer in capture mode.
 setTimeout(()=>{try{
  const read=(name,fallback,max)=>{const raw=query.get(name);const value=raw===null?fallback:Number(raw);if(!Number.isInteger(value)||value<1||value>max)throw new Error('Invalid '+name);return value;};
  const name=query.get('capture'),n=read('frames',60,600),w=read('w',800,2400),h=read('h',600,2400);
  if(w*h*n>384000000)throw new Error('Capture exceeds 384 million pixels');
  size(w,h);setScene(name,n);const images=[];
  for(let i=0;i<n;i++){draw(i);images.push(canvas.toDataURL('image/png'));}
  const payload=document.createElement('script');payload.type='application/json';payload.id='capture-frames';
  payload.textContent=JSON.stringify({scene:name,frames:n,w,h,fps:15,images});document.body.append(payload);
  document.title='CAPTURE DONE '+name+' '+n;$('state').textContent='Capture complete · '+n+' frames · 15 fps';
 }catch(error){fail(error);}},0);
}else{
 setScene('leg');
 function resize(){const r=canvas.getBoundingClientRect();size(Math.max(1,Math.round(r.width)),Math.max(1,Math.round(r.height)));draw(frame);}
 new ResizeObserver(resize).observe(canvas);
 for(const button of document.querySelectorAll('[data-scene]'))button.onclick=()=>{setScene(button.dataset.scene);draw(frame);};
 $('look').onclick=()=>{setScene(scene==='walk-concept'?'walk-prototype':'walk-concept');draw(frame);};
 $('play').onclick=()=>{playing=!playing;$('play').textContent=playing?'Pause':'Play';$('play').setAttribute('aria-pressed',String(playing));$('state').textContent=(playing?'Playing':'Paused')+' · '+titles[scene];};
 $('reset').onclick=()=>{yawOffset=0;pitch=.3;zoom=1;draw(frame);};
 canvas.addEventListener('pointerdown',e=>{drag={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);});
 canvas.addEventListener('pointermove',e=>{if(!drag||drag.id!==e.pointerId)return;yawOffset+=(e.clientX-drag.x)*.008;pitch=Math.max(-1.4,Math.min(1.4,pitch+(e.clientY-drag.y)*.008));drag.x=e.clientX;drag.y=e.clientY;draw(frame);});
 canvas.addEventListener('pointerup',()=>drag=null);canvas.addEventListener('pointercancel',()=>drag=null);
 canvas.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.45,Math.min(2.5,zoom*Math.exp(-e.deltaY*.001)));draw(frame);},{passive:false});
 canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-'].includes(e.key))return;e.preventDefault();if(e.key==='ArrowLeft')yawOffset-=.1;if(e.key==='ArrowRight')yawOffset+=.1;if(e.key==='ArrowUp')pitch=Math.min(1.4,pitch+.1);if(e.key==='ArrowDown')pitch=Math.max(-1.4,pitch-.1);if(e.key==='+'||e.key==='=')zoom=Math.min(2.5,zoom*1.1);if(e.key==='-')zoom=Math.max(.45,zoom/1.1);draw(frame);});
 let last=null,accumulator=0;
 function tick(now){try{if(last!==null&&playing){accumulator+=Math.min(100,now-last);while(accumulator>=1000/30){frame=(frame+1)%normalFrames;accumulator-=1000/30;}draw(frame);}last=now;requestAnimationFrame(tick);}catch(error){fail(error);}}
 resize();requestAnimationFrame(tick);
}
}catch(error){fail(error);}
</script></body></html>'''

MOTION_JS = r'''
const LEGS={FL:[1,1,.25],FR:[1,-1,.75],RL:[-1,1,0],RR:[-1,-1,.5]};
const add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]);
function rx(v,a){const t=a*Math.PI/180,c=Math.cos(t),s=Math.sin(t);return [v[0],v[1]*c-v[2]*s,v[1]*s+v[2]*c];}
function ry(v,a){const t=a*Math.PI/180,c=Math.cos(t),s=Math.sin(t);return [v[0]*c+v[2]*s,v[1],-v[0]*s+v[2]*c];}
function forward(q){const [a,b,c]=q,p2=add(data.P1,rx(sub(data.P2,data.P1),a)),p3=add(p2,rx(ry([0,0,-data.L1],b),a));return [p2,p3,add(p3,rx(ry([0,0,-data.L2],b+c),a))];}
function foot(q){const [a,b,c]=q,f=data.foot,centre=add(forward(q)[2],rx(ry([0,0,-f.Z/2],b+c),a)),ar=a*Math.PI/180,br=(b+c)*Math.PI/180;const support=Math.abs(Math.cos(ar)*Math.sin(br))*f.X/2+Math.abs(Math.sin(ar))*f.Y/2+Math.abs(Math.cos(ar)*Math.cos(br))*f.Z/2;return [centre[0],centre[1],centre[2]-support];}
function linear(A,b){const a=A.map((row,i)=>[...row,b[i]]);for(let i=0;i<3;i++){let pivot=i;for(let j=i+1;j<3;j++)if(Math.abs(a[j][i])>Math.abs(a[pivot][i]))pivot=j;[a[i],a[pivot]]=[a[pivot],a[i]];if(Math.abs(a[i][i])<1e-14)throw new Error('Singular IK matrix');const d=a[i][i];for(let k=i;k<4;k++)a[i][k]/=d;for(let j=0;j<3;j++)if(j!==i){const f=a[j][i];for(let k=i;k<4;k++)a[j][k]-=f*a[i][k];}}return a.map(row=>row[3]);}
function solve(target,previous){let q=previous.slice();for(let iteration=0;iteration<80;iteration++){const value=foot(q),error=sub(target,value),length=Math.hypot(...error);if(length<=1e-5)return {q,error:length};const h=.0001,jac=[0,1,2].map(i=>{const p=q.slice();p[i]+=h;return sub(foot(p),value).map(v=>v/h);});const A=[0,1,2].map(i=>[0,1,2].map(j=>jac.reduce((sum,col)=>sum+col[i]*col[j],0)+(i===j?.0025:0)));const y=linear(A,error),delta=jac.map(col=>col.reduce((sum,v,i)=>sum+v*y[i],0)),scale=Math.min(1,8/Math.max(Math.hypot(...delta),1e-12));q=q.map((v,i)=>v+delta[i]*scale);}throw new Error('IK did not converge');}
function path(phase,stride){if(phase<.2){const s=phase/.2;return [-stride/2+stride*(1-Math.cos(Math.PI*s))/2,10*Math.sin(Math.PI*s)**2,true];}return [stride/2-stride*(phase-.2)/.8,0,false];}
const mod=t=>Math.round((((t%1)+1)%1)*1e12)/1e12%1;
function sway(t){for(const [sx,sy,offset] of Object.values(LEGS)){const phase=mod(t-offset);if(phase<.2)return -sy*5*Math.sin(Math.PI*phase/.2)**2;}return 0;}
function makeCycle(scene,n,stride){const base=foot(data.stance),previous=Object.fromEntries(Object.keys(LEGS).map(name=>[name,data.stance.slice()])),rows=[];for(let index=0;index<n;index++){const t=index/n,dy=scene.startsWith('walk')?sway(t):0,dz=scene==='overview'?-15*Math.sin(Math.PI*t)**2:0,row={phase:t,body:[0,dy,dz],legs:{},label:''};for(const [name,[sx,sy,offset]] of Object.entries(LEGS)){if(scene==='leg'&&name!=='FL')continue;let target=base.slice(),swing=false,answer;if(scene==='leg'){const section=Math.min(3,Math.floor(t*4)),u=mod(t*4);row.label=['J1 hip spread','J2 hip swing','J3 knee','One step'][section];if(section<3){const q=data.stance.slice();q[section]+=[15,25,30][section]*Math.sin(2*Math.PI*u);target=foot(q);answer={q,error:0};}else{const [dx,lift,up]=path(mod(u+.6),stride);target=add(target,[dx,0,lift]);swing=up;answer=solve(target,previous[name]);}}else if(scene==='overview'){target[2]-=dz;answer=solve(target,previous[name]);}else{const [dx,lift,up]=path(mod(t-offset),stride);target=add(target,[sx*dx,-sy*dy,lift]);swing=up;answer=solve(target,previous[name]);}previous[name]=answer.q;for(let i=0;i<3;i++)if(answer.q[i]<data.limits[i][0]-1e-8||answer.q[i]>data.limits[i][1]+1e-8)throw new Error('Joint outside viewing sweep');row.legs[name]={...answer,target,swing};}rows.push(row);}return rows;}
'''


def main():
    p, variant = lp.read_parameters(PARAMETERS, 'direct')
    m = lp.Model(p, variant).build()
    print(f'1 of 4 · placement A built · {len(m.parts)} source solids', flush=True)
    rng = random.Random(402)
    errors = [float(np.max(np.linalg.norm(forward(m, q)-np.array(m.chain(*q)), axis=1)))
              for q in [[rng.uniform(*p['poses']['sweep'][k][:2]) for k in 'abc'] for _ in range(10)]]
    assert max(errors) < 1e-6, 'Forward chain disagrees with Model.chain'
    stride = 24
    reductions = []
    while stride >= 0:
        walk = cycle(m, 'walk-prototype', 240, stride)
        if within(m, walk):
            break
        reductions.append(stride)
        stride -= 2
    if stride < 0:
        raise ValueError('No stride satisfies viewing sweep')
    report = dict(scenes=check(m, stride), forward_chain_check=dict(random_poses=10, max_error_mm=max(errors)),
                  rejected_strides_mm=reductions, parameter_sha256=sha(PARAMETERS),
                  not_checked=['interference between parts in motion', 'static stability or centre of mass', 'joint torque or speed', 'any load'],
                  known_from_J04_L02_D01='the packaged leg has named overlaps in its hinge frames at sampled poses; this animation does not resolve them',
                  ground_reference='Nominal prototype rigid pad: centroid XY and lowest box support Z; slip is centroid XY in an unwrapped ground frame, not contact-patch slip. Concept rounding is appearance only and reuses the nominal pad datum.',
                  browser_proof='UNRUN here; page render, visual quality, WebGL, console and actual browser capture belong to caller.')
    report['known_from_J04-L02-D01'] = report.pop('known_from_J04_L02_D01')
    print(f'2 of 4 · 60-frame gait checks passed · stride {stride} mm', flush=True)
    prototype = [(name, sh, m.meta[name]['frame'], m.meta[name]['color'], name in ('body_envelope', 'cradle'))
                 for name, sh in m.parts.items() if not name.startswith('nb_')]
    stance = [p['poses']['stance'][k] for k in 'abc']
    data = dict(P1=m.P1, P2=m.P2, P3=m.P3, neutralFoot=m.P4,
                neutralFootCentre=lp.add(m.P4, [0, 0, -p['foot']['Z']/2]), stance=stance,
                limits=[p['poses']['sweep'][k] for k in 'abc'], L1=p['links']['L1'], L2=p['links']['L2'],
                foot=p['foot'], ground=float(foot(m, stance)[2]), bodyHeight=p['body']['height_Z'],
                bodyDepth=p['body']['depth_X'], bodyWidth=p['body']['width_Y'], stride=stride,
                meshes=dict(prototype=meshes(prototype), concept=meshes(concept(m))))
    template = (HERE/'leg-viewer-template.html').read_text()
    style = re.search(r'<style>(.*?)</style>', template, re.S).group(1)
    shader = template[template.index('function shader('):template.index('const $ =')]
    page = PAGE.replace('/* BASE_STYLE */', style).replace('/* SHADER_JS */', shader).replace('/* MOTION_JS */', MOTION_JS)
    page = page.replace('/* MODEL_DATA */', json.dumps(data, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c'))
    OUT.mkdir(parents=True, exist_ok=True)
    html = OUT/'animation.html'
    html.write_text(page)
    print(f'3 of 4 · offline page exported · {html.stat().st_size} bytes', flush=True)
    report['sha256'] = {str(path.relative_to(HERE)): sha(path) for path in (PARAMETERS, Path(__file__), HERE/'render_frames.py', html)}
    report['source_sha256'] = {name: sha(HERE/name) for name in ('leg_packaging.py', 'leg-viewer-template.html')}
    report['mesh_counts'] = {look: {'parts': len(parts), 'triangles': sum(len(p['triangles']) for p in parts)} for look, parts in data['meshes'].items()}
    (OUT/'gait-check.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print('4 of 4 · gait-check.json written · browser proof UNRUN', flush=True)


if __name__ == '__main__':
    main()
