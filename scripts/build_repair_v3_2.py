"""V3.2 best-effort repair; reference drawing dimensions are not physical validation.
Keep original ear height; clear case locally; seat supplied horn fully before
selecting included gate packing. No additional purchased hardware/test print.
"""
from pathlib import Path
import json, zipfile, xml.etree.ElementTree as ET
import numpy as np
import manifold3d as mf
import trimesh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/hardware/servo-fit'
def box(x,y,z,dx,dy,dz):return mf.Manifold.cube((dx,dy,dz)).translate((x,y,z))
def cyl(x,y,z,r,h,r2=-1):return mf.Manifold.cylinder(h,r,r2,96).translate((x,y,z))
def tm(p):
 m=p.to_mesh();t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
 assert t.is_watertight and t.is_winding_consistent and len(p.decompose())==1
 return t
def old(name):
 t=trimesh.load(ROOT/'public/hardware/stl'/name)
 return mf.Manifold(mf.Mesh(t.vertices.astype(np.float32),t.faces.astype(np.uint32)))
# All flange/clip/outlet locations preserved from V3.
hopper=box(-35,-52,0,124,104,3)+cyl(0,0,2.8,10,55.2,33)
hopper-=cyl(0,0,-1,7,4.2)+cyl(0,0,3,7,55.2,30.08)
hopper+=box(26,-17,2.8,18,10.7,4.2)+box(26,17.3,2.8,18,11.7,4.2)
for x in [23,47]:
 for y in [0,12]:hopper-=box(x-1.8,y-3,-1,3.6,6,5)
# Recess each longitudinal same-side servo tie below the flange surface.
for x in [23,47]:hopper-=box(x-1.8,-3,0,3.6,18,1.2)
# A 1 mm shallow local case recess replaces raising the servo.
hopper-=box(28.4,-6.6,2,13.2,24,2)
# Diameter 14.4, tail 6.6 wide to 9.8 from the unchanged shaft centre.
hopper-=cyl(35,0,-1,7.2,10)+box(31.7,0,-1,6.6,6.5,10)+cyl(35,6.5,-1,3.3,10)
case_face=7-(22.7-18.4)
case=box(29.1,-5.9,case_face,11.8,22.5,22.7)
ears=box(29.1,-10.6,7,11.8,4.7,2.5)+box(29.1,16.6,7,11.8,4.7,2.5)
boss=(cyl(35,0,case_face-4,5.9,4)+cyl(35,6.3,case_face-4,2.5,4)).hull()
shaft=cyl(35,0,case_face-7.2,2.3,3.2)
reference=case+ears+boss+shaft
assert (reference^hopper).volume()<.005
assert (boss.translate((-35,0,0)).scale((1.015,1.015,1)).translate((35,0,0))^hopper).volume()<.005
roi=box(20,-19,-1,30,50,11)
original=old('02_hopper_with_servo_mount.stl')
assert ((original-hopper)-roi).volume()<.005
assert ((hopper-original)-roi).volume()<.005
# Fixed upper face, deeper pocket. The shaft/hub use a through-hole, not a
# fabricated printed spline. The original supplied horn remains the coupling.
gate=cyl(0,0,0,44,7.4)-cyl(-35,0,-1,7,10)-cyl(0,0,-1,5.6,10)
gate-=box(-18.5,-6,1.4,37,12,8)+cyl(0,0,1.4,8,8)
# Circular relief clears the entire stationary gearbox-tail envelope as gate turns.
gate-=cyl(0,0,5.4,11,3)
for x in [-13,13]:
 for y in [-8.2,8.2]:gate-=box(x-1.6,y-1.4,-1,3.2,2.8,10)
 gate-=box(x-1.6,-10,0,3.2,20,.6)
 gate-=box(x-1.6,-10,1.4,3.2,20,8)
# Optional packing rings, binary increments 0.4/0.8/1.6 -> 0...2.8 at 0.4 steps.
parts={'08_HOPPER_ORIGINAL_SERVO_HEIGHT_V3_2':hopper,'09_GATE_ADJUSTABLE_HORN_V3_2':gate}
for h,tag in [(.4,'0p4'),(.8,'0p8'),(1.6,'1p6')]:
 p=box(-18.3,-5.8,0,36.6,11.6,h)+cyl(0,0,0,7.7,h)
 p-=cyl(0,0,-1,5.7,h+2)
 parts['10_HORN_PACKING_'+tag+'_V3_2']=p
parts['11_ASSEMBLY_GAP_SPACER_0p6_V3_2']=box(0,0,0,20,8,.6)
# Check frame fit; packing does not shrink the central through-hole.
for name,p in parts.items():
 t=tm(p);t.export(OUT/(name+'.stl'))
 if 'PACKING' in name:
  placed=p.translate((0,0,1.4))
  assert (placed^gate).volume()<.005
# Nominal complete servo and gate sweep, including range of assembled clearances.
stand=old('01_wide_cradle.stl').rotate((180,0,0)).translate((0,0,190))
assert (hopper.translate((0,0,186.3))^stand).volume()<.005
for gap in [.4,.6,.8]:
 for angle in range(-70,71,5):
  g=gate.rotate((0,0,angle)).translate((35,0,-7.4-gap))
  assert (g^hopper).volume()<.005
  assert (g^reference).volume()<.005
  assert (g.translate((0,0,186.3))^stand).volume()<.005
# Reference arm envelopes up to 35 x 10, 2 mm thick fit the enlarged slot.
for length in [32,35]:
 for packing in np.arange(0,2.81,.4):
  arm=box(-length/2,-5,1.4+packing,length,10,2)-cyl(0,0,-1,2.3,12)
  assert (arm^gate).volume()<.005
# Explicit small-tie envelopes: 2.5 mm wide x 0.8 mm thick.
for x in [23,47]:
 tie=box(x-1.25,0,.15,2.5,12,.8)
 assert (tie^hopper).volume()<.005
for packing in np.arange(0,2.81,.4):
 ties=mf.Manifold()
 for x in [-13,13]:
  top=1.4+float(packing)+2
  ties+=box(x-1.25,-8.2,top,2.5,16.4,.8)
  ties+=box(x-1.25,-8.2,-.25,2.5,16.4,.8)
  for y in [-8.6,7.8]:ties+=box(x-1.25,y,-.25,2.5,.8,top+1.05)
 assert (ties^gate).volume()<.005
 for angle in range(-70,71,5):
  t=ties.rotate((0,0,angle)).translate((35,0,-7.8))
  assert (t^hopper).volume()<.005
  assert (t^(case+ears+boss)).volume()<.005

# Solve gate spacing without changing the fully seated horn's axial position.
# P = arm outer contact plane in hopper coordinates; S = packing thickness.
# Gate gap = S - P - 6.0 for this 7.4 mm gate / 1.4 mm floor.
solutions=[]
for contact in np.arange(-6.8,-3.599,.05):
 candidates=[(abs((float(h)-contact-6)-.6),float(h),float(h)-contact-6) for h in np.arange(0,2.801,.4) if .3999<=float(h)-contact-6<=.8001]
 assert candidates,contact
 _,packing,gap=min(candidates)
 solutions.append({'horn_contact_z':round(float(contact),3),'packing_mm':round(packing,1),'gate_gap_mm':round(float(gap),3)})
(OUT/'packing_selection_envelope_v3_2.json').write_text(json.dumps({'not_a_measurement':True,'assumed_horn_contact_range_z':[-6.8,-3.6],'solutions':solutions},indent=2),encoding='utf-8')
# Verify the working outlet opens at zero and is covered at the nominal 60 deg close.
for angle,expected in [(0,False),(60,True)]:
 g=gate.rotate((0,0,angle)).translate((35,0,-8))
 probe=cyl(0,0,-.7,6.95,.05)
 fraction=(g^probe).volume()/probe.volume()
 assert fraction>.999 if expected else fraction<.001
# One A1 plate. Everything is flat; the flange remains the hopper's bed surface.
positions=[(62,65),(205,65),(40,150),(90,150),(140,150),(195,150)]
meshes=[]
for (name,p),(x,y) in zip(parts.items(),positions):
 t=tm(p);t.apply_translation((x,y,0));assert np.all(t.bounds[0]>=0) and np.all(t.bounds[1]<=[256,256,256])
 for previous in meshes:
  # Their XY bounding boxes do not overlap.
  assert np.any(t.bounds[0,:2]>=previous.bounds[1,:2]) or np.any(previous.bounds[0,:2]>=t.bounds[1,:2])
 meshes.append(t)
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
model=ET.Element('{'+ns+'}model',{'unit':'millimeter'})
ET.SubElement(model,'{'+ns+'}metadata',{'name':'Title'}).text='V3.2 REPAIR ONLY - hopper, gate, optional packing and assembly spacer; physically untested'
res=ET.SubElement(model,'{'+ns+'}resources');build=ET.SubElement(model,'{'+ns+'}build')
for i,((name,p),t) in enumerate(zip(parts.items(),meshes),1):
 obj=ET.SubElement(res,'{'+ns+'}object',{'id':str(i),'type':'model','name':name});me=ET.SubElement(obj,'{'+ns+'}mesh');vs=ET.SubElement(me,'{'+ns+'}vertices');fs=ET.SubElement(me,'{'+ns+'}triangles')
 for v in t.vertices:ET.SubElement(vs,'{'+ns+'}vertex',dict(zip(('x','y','z'),[f'{q:.6f}' for q in v])))
 for f in t.faces:ET.SubElement(fs,'{'+ns+'}triangle',dict(zip(('v1','v2','v3'),map(str,f))))
 ET.SubElement(build,'{'+ns+'}item',{'objectid':str(i)})
with zipfile.ZipFile(OUT/'V3_2_REPAIR_PLATE_HOPPER_GATE_PACKING.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
report={'version':'V3.2 best-effort repair','physical_fit_verified':False,'servo_tie_channels_mm':[3.6,18,1.2],'gate_tie_width_thickness_checked_mm':[2.5,.8],'servo_support_raise_mm':0,'case_relief_depth_mm':1,'nominal_case_clearance_above_relief_mm':.7,'opening':{'round_diameter_mm':14.4,'tail_width_mm':6.6,'tail_reach_from_axis_mm':9.8},'gate':{'thickness_mm':7.4,'arm_pocket_mm':[37,12],'pocket_floor_mm':1.4,'hub_through_hole_mm':11.2,'boss_sweep_relief_mm':[22,2],'arm_thickness_assumption_mm':2,'arm_lengths_checked_mm':[32,35]},'packing_mm':[.4,.8,1.6],'packing_combinations_mm':[round(x,1) for x in np.arange(0,2.81,.4)],'target_gate_gap_mm':[.4,.8],'adjustable_horn_contact_plane_range_z':[-6.8,-3.6],'user_2mm_extension_example':{'status':'Assumption only: 2 mm is interpreted as outer arm face beyond bare shaft tip','horn_contact_z':-6.5,'packing_mm':0,'resulting_gate_gap_mm':.5},'nominal_height_stack_at_gap_0p6':{'case_face_z':2.7,'boss_face_z':-1.3,'shaft_tip_z':-4.5,'gate_top_z':-.6,'gate_bottom_z':-8,'horn_arm_contact_plane_range_z':[-6.6,-3.8],'shaft_tip_to_arm_outer_face_range_mm':[-.7,2.1]},'sources':['User detailed SG90 drawing: case 22.7, upper ear face 18.4, boss 4, shaft 3.2 mm; variant not confirmed.','User latest horn image: 35 x 10 mm envelope; earlier image 32 mm length.','User estimate: horn adds around 2 mm; axial datum not specified, not a measured socket depth.','https://towerpro.com.tw/product/sg90-analog/','https://www.auselectronicsdirect.com.au/assets/brochures/TA0132.pdf'],'checks':['Connected watertight meshes and separate non-overlapping one-plate layout','Unchanged original flange/clip/outlet interfaces outside servo region','Nominal complete case, ears, boss, shaft and +1.5% XY boss envelope clear','Gate sweep -70 to +70 deg with 0.4 to 0.8 mm gap clears hopper, servo and stand','32 and 35 x 10 x 2 mm horn arm envelopes clear gate for every packing combination','Servo underside tie runs and gate tie loops clear printed geometry; gate ties clear case and boss through sweep','Open outlet at 0 degrees and covered at 60 degrees','Packing selection spans contact planes -6.8 to -3.6 mm for target gap 0.4 to 0.8 mm'],'limits':['Exact servo/horn variant and socket depth unknown; use original horn fully seated rather than modeled printed spline','Gate adjustment covers stated finite range; actual arm plane may fall outside it','Horn hub diameter allowance 10 mm is an assumption from image, not a dimensioned hub drawing','PETG fit, clip retention, motor logic, flow and leakage remain physically untested'],'reuse':['Stand','Lid','Both locking clips','Servo with supplied horn and screw','Electronics and wiring'],'assembly':'Seat supplied horn fully first. Select packing under horn arms to obtain 0.4-0.8 mm gate gap; packing increases gap. Never pull an unseated horn in with its screw or tighten ties to remove interference.'}
(OUT/'repair_v3_2_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
def svg_section(part,z,cx,cy,scale):
    paths=[]
    for poly in part.slice(z).to_polygons():
        paths.append('M'+' L'.join(f'{cx+scale*x:.2f},{cy-scale*y:.2f}' for x,y in poly)+' Z')
    return ' '.join(paths)
hpath=svg_section(hopper,2.5,150,225,2.4)
gpath=svg_section(gate,6.4,720,225,2.4)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="520" viewBox="0 0 1000 520"><style>text{{font:17px Arial,sans-serif;fill:#293f34}}.title{{font-size:26px;font-weight:bold}}.small{{font-size:14px}}</style><rect width="1000" height="520" fill="#f5f3ed"/><text x="30" y="40" class="title">V3.2 · original servo height, local relief, adjustable gate</text><path d="{hpath}" fill="#d59c7a" stroke="#79523e" fill-rule="evenodd"/><path d="{gpath}" fill="#d7b35c" stroke="#79622f" fill-rule="evenodd"/><text x="60" y="95">Replacement hopper</text><text x="600" y="95">Replacement gate</text><text x="65" y="385">Case clearance pocket: 1 mm deep</text><text x="65" y="416">Boss hole only; horn installs afterward</text><text x="560" y="385">Horn pocket: 37 × 12 mm</text><text x="560" y="416">Packing below horn arms: 0–2.8 mm</text><text x="30" y="471" class="small">Actual CAD sections: hopper at z2.5 mm; gate at z6.4 mm from print bed. Not a horn socket drawing.</text><text x="30" y="498" class="small">Fully seat supplied horn first. Select packing for 0.4–0.8 mm gate gap; remove the 0.6 mm assembly strip.</text></svg>'''
(OUT/'repair_reference.svg').write_text(svg,encoding='utf-8')
print(json.dumps(report,indent=2))
