"""Generate hardware reference meshes and a full assembly collision audit.
These source-labelled geometric checks are not powder-flow/accuracy simulation.
"""
from pathlib import Path
import json,itertools
import numpy as np
import manifold3d as mf
import trimesh
ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'public/hardware';OUT=H/'simulation';OUT.mkdir(exist_ok=True)
def box(x,y,z,dx,dy,dz):return mf.Manifold.cube((dx,dy,dz)).translate((x,y,z))
def cyl(x,y,z,r,h):return mf.Manifold.cylinder(h,r,r,96).translate((x,y,z))
def load(path):
 t=trimesh.load(H/path)
 return mf.Manifold(mf.Mesh(t.vertices.astype(np.float32),t.faces.astype(np.uint32)))
def export(p,name):
 m=p.to_mesh();t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
 assert t.is_watertight,name
 t.export(OUT/(name+'.stl'))
# Servo is referenced to the hopper's lower face, z=0.
case=box(29.1,-5.9,2.7,11.8,22.5,22.7)
ears=box(29.1,-10.6,7,11.8,4.7,2.5)+box(29.1,16.6,7,11.8,4.7,2.5)
for y in [-8.3,19.0]:
 ears-=cyl(35,y,6,1,5)
# Open ear slots are illustrative; screw pitch is not validated for this unit.
boss=(cyl(35,0,-1.3,5.9,4)+cyl(35,6.3,-1.3,2.5,4)).hull()
shaft=cyl(35,0,-4.5,2.3,3.2)
for name,p in [('servo_case',case),('servo_ears',ears),('servo_boss',boss),('servo_shaft',shaft)]:export(p,name)
# Default horn assumption: 35 x 10 x 2 mm arms; OD10 hub, socket depth2.8,
# 0.6 boss-mouth gap, 4.8 smooth bore, arm outer face2mm beyond shaft tip.
P=-6.5;M=-1.9;B=-4.7;S=0;gate_z=P-1.4-S
arm=box(-17.5,-5,P,35,10,2)-cyl(0,0,P-1,5,4)
for length in [32,35]:
 export(box(-length/2,-5,P,length,10,2)-cyl(0,0,P-1,4.9,4),'horn_arms_'+str(length))
hub=cyl(0,0,P,5,M-P)-cyl(0,0,B,2.4,M-B+.1)-cyl(0,0,P-.1,1.1,M-P+.2)
horn=arm+hub
export(horn,'horn_assumed_reference')
# Full routed servo ties, thin square-section envelope. Flat width checked in
# build_repair_v3_2.py; these upper bends are illustrative, not a flex analysis.
def path_band(points,r=.4):
 result=mf.Manifold()
 for a,b in zip(points,points[1:]):
  result+=(box(a[0]-r,a[1]-r,a[2]-r,2*r,2*r,2*r)+box(b[0]-r,b[1]-r,b[2]-r,2*r,2*r,2*r)).hull()
 return result
servo_ties=mf.Manifold()
for x,topx in [(23,31),(47,39)]:
 servo_ties+=path_band([(x,0,.55),(x,0,26),(topx,0,26),(topx,12,26),(x,12,26),(x,12,.55),(x,0,.55)])
export(servo_ties,'servo_ties_reference')
gate_ties=mf.Manifold()
for x in [-13,13]:
 top=P+2
 gate_ties+=box(x-1.25,-8.2,top,2.5,16.4,.8)
 gate_ties+=box(x-1.25,-8.2,gate_z-.25,2.5,16.4,.8)
 for y in [-8.6,7.8]:gate_ties+=box(x-1.25,y,gate_z-.25,2.5,.8,top-(gate_z-.25)+.8)
export(gate_ties,'gate_ties_reference')
clip=load('stl/05_locking_clip.stl')
front=clip.rotate((0,-90,0)).translate((-21,-58.6,176.4))
rear=clip.rotate((0,-90,0)).translate((4,-58.6,176.4)).rotate((0,0,180)).translate((85,0,0))
export(front,'front_clip_assembled');export(rear,'rear_clip_assembled')
# Static parts in table/world coordinates.
static={
 'stand':load('stl/01_wide_cradle.stl').rotate((180,0,0)).translate((0,0,190)),
 'hopper':load('servo-fit/08_HOPPER_ORIGINAL_SERVO_HEIGHT_V3_2.stl').translate((0,0,186.3)),
 'lid':load('stl/04_lid.stl').rotate((180,0,0)).translate((0,0,246.7)),
 'clip_front':front,'clip_rear':rear,
 'servo_case':case.translate((0,0,186.3)),
 'servo_ears':ears.translate((0,0,186.3)),
 'servo_boss':boss.translate((0,0,186.3)),
 'servo_shaft':shaft.translate((0,0,186.3)),
 'servo_ties':servo_ties.translate((0,0,186.3)),
 'scale':box(-52.5,-62.5,0,105,125,17),
 'example_cup':(cyl(0,0,17,30,80)-cyl(0,0,18.5,28.5,80))}
gate=load('servo-fit/09_GATE_ADJUSTABLE_HORN_V3_2.stl')
fixed_checks=[];fails=[];threshold=.02
for (an,a),(bn,b) in itertools.combinations(static.items(),2):
 # Joining faces may have tiny STL quantisation overlaps below threshold.
 v=max(0,(a^b).volume());fixed_checks.append({'a':an,'b':bn,'overlap_mm3':round(v,6)})
 if v>threshold:fails.append(fixed_checks[-1])
sweep=[]
for angle in range(-70,71,5):
 moving={'gate':gate.translate((0,0,gate_z)), 'horn':horn,'gate_ties':gate_ties}
 moving={n:p.rotate((0,0,angle)).translate((35,0,186.3)) for n,p in moving.items()}
 checks=[]
 for an,a in moving.items():
  for bn,b in static.items():
   v=max(0,(a^b).volume());checks.append({'a':an,'b':bn,'overlap_mm3':round(v,6)})
 for (an,a),(bn,b) in itertools.combinations(moving.items(),2):
  # Horn/zip ties intentionally meet at surfaces; no overlap is expected.
  v=max(0,(a^b).volume());checks.append({'a':an,'b':bn,'overlap_mm3':round(v,6)})
 bad=[p for p in checks if p['overlap_mm3']>threshold]
 sweep.append({'angle_degrees':angle,'pairs_checked':len(checks),'maximum_overlap_mm3':max(p['overlap_mm3'] for p in checks),'interferences':bad})
 for pair in bad:fails.append({'angle_degrees':angle,**pair})
report={'scope':'Rigid geometric reference model, not physical fit/force/powder simulation','print_geometry':'Actual V3.2 STLs, unchanged','reference_horn':{'arm_length':35,'arm_width':10,'arm_thickness':2,'outer_contact_z':P,'hub_OD':10,'socket_mouth_z':M,'socket_depth':2.8,'socket_bottom_z':B,'socket_bore_diameter':4.8,'shaft_tip_z':-4.5,'shaft_overlap_mm':2.6,'shaft_tip_clearance_mm':.2,'all_horn_socket_values_are_assumptions':True},'default_gap_mm':.5,'default_packing_mm':0,'reference_static_checks':fixed_checks,'sweep':sweep,'collision_threshold_mm3':threshold,'unintended_interferences':fails,'physical_fit_verified':False,'excluded_from_numerical_collision_validation':['Illustrative ESP32, breadboard, vibration module, terminal adapter, brick, cables and servo screw','Example cup/scale geometry are simplified envelopes, not actual purchased product CAD'],'not_simulated':['Powder bridging, particles, discharge or dosing accuracy','PETG shrinkage, tolerances, fatigue, tie tension and clip bending','Servo backlash, supply peaks, motor drive compatibility','Real horn teeth, socket seating stop and thread engagement'],'precision_requirement':{'target':'Larger doses with +/-10 mg accuracy; supersedes earlier +/-1 mg target','supported_by_current_build':False,'reason':'Open-loop gravity gate and unconnected pocket scale cannot demonstrate this accuracy.'}}
# Conservative solids invariant under rotation cover the default moving parts.
# If these clear static geometry, no static collision is hidden between samples.
gate_env=cyl(0,0,0,44,7.4)-cyl(0,0,-1,5.6,10)-cyl(0,0,5.4,11,3)
horn_env=(cyl(0,0,P,18.3,2)-cyl(0,0,P-1,5,4))+hub
tie_env=cyl(0,0,gate_z-.25,18,P+2.8-(gate_z-.25))-cyl(0,0,gate_z-1,11.5,12)
envelopes={'gate':gate_env.translate((0,0,gate_z)),'horn':horn_env,'gate_ties':tie_env}
envelope_checks=[]
for name,p in envelopes.items():
 p=p.translate((35,0,186.3))
 for static_name,q in static.items():
  volume=max(0,(p^q).volume())
  envelope_checks.append({'moving_envelope':name,'static_part':static_name,'overlap_mm3':round(volume,6)})
assert all(x['overlap_mm3']<=threshold for x in envelope_checks),envelope_checks
report['continuous_default_rotation_check']={'method':'Rotationally invariant conservative envelopes versus all static solids; moving-part relative positions stay rigid. Applies only to documented default parameters.','checks':envelope_checks,'passed':True,'scope':'Rigid nominal geometry, not force/tolerance/flow validation'}

# Negative controls: the collision method must also reject known bad fits.
bad_gate_volume=(gate.translate((35,0,0))^load('servo-fit/08_HOPPER_ORIGINAL_SERVO_HEIGHT_V3_2.stl')).volume()
bad_bottom=M-1.5
short_hub=cyl(0,0,P,5,M-P)-cyl(0,0,bad_bottom,2.4,M-bad_bottom+.1)-cyl(0,0,P-.1,1.1,M-P+.2)
short_socket_volume=(short_hub.translate((35,0,0))^shaft).volume()
wide_arm=box(-20,-7.5,P,40,15,2)-cyl(0,0,P-1,5,4)
wide_arm_volume=(wide_arm^gate.translate((0,0,gate_z))).volume()
assert bad_gate_volume>1 and short_socket_volume>1 and wide_arm_volume>1
report['negative_controls']=[{'case':'Gate intentionally moved into flange','overlap_mm3':round(bad_gate_volume,4),'detected':True},{'case':'Socket depth reduced to1.5mm','overlap_mm3':round(short_socket_volume,4),'detected':True},{'case':'Horn arm enlarged to40x15mm','overlap_mm3':round(wide_arm_volume,4),'detected':True}]
report['excluded_from_numerical_collision_validation']=['Illustrative ESP32, breadboard, vibration module, terminal adapter, brick, cables and servo screw']
report['simplified_envelopes_included_in_collision_check']=['105x125x17mm scale box','Example cup OD60x80mm, not user-specified']

(OUT/'assembly_collision_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'static_pairs':len(fixed_checks),'sweep_positions':len(sweep),'total_pairs':len(fixed_checks)+sum(s['pairs_checked'] for s in sweep),'interferences':fails},indent=2))
assert not fails,'Reference assembly has unintended intersections; inspect report before publication.'
