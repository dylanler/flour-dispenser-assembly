"""Hopper-only revision requested without a separate physical test print.

Source: the detailed SG90 dimension drawing supplied by the user, audited in
docs/SERVO_FIT_AUDIT.md. The exact purchased unit and horn stack remain unverified.
"""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET
import numpy as np
import manifold3d as mf
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/hardware/servo-fit'
OUT.mkdir(exist_ok=True,parents=True)
def box(x,y,z,dx,dy,dz):return mf.Manifold.cube((dx,dy,dz)).translate((x,y,z))
def cyl(x,y,z,r,h,r2=-1):return mf.Manifold.cylinder(h,r,r2,96).translate((x,y,z))
def from_stl(name):
    m=trimesh.load(ROOT/'public/hardware/stl'/name)
    return mf.Manifold(mf.Mesh(m.vertices.astype(np.float32),m.faces.astype(np.uint32)))
def mesh(p):
    m=p.to_mesh();t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
    assert t.is_watertight and t.is_winding_consistent
    return t

# Flange, outlet, cone and tie positions are identical to the printed V3 hopper.
hopper=box(-35,-52,0,124,104,3)+cyl(0,0,2.8,10,55.2,33)
hopper-=cyl(0,0,-1,7,4.2)+cyl(0,0,3,7,55.2,30.08)
# Integrate the nominal 1 mm height correction and extend support beneath the ears.
hopper+=box(26,-17,2.8,18,10.7,5.2)
hopper+=box(26,17.3,2.8,18,11.7,5.2)
for x in [23,47]:
    for y in [0,12]:hopper-=box(x-1.8,y-3,-1,3.6,6,5)
# A generous keyhole: 15 mm main diameter, 8 mm-wide tail to +11 mm from axis.
opening=cyl(35,0,-1,7.5,11)+box(31,0,-1,8,7,11)+cyl(35,7,-1,4,11)
hopper-=opening
assert len(hopper.decompose())==1
new=mesh(hopper)
new.export(OUT/'07_HOPPER_SG90_RELIEF_V3_1.stl')

# Constrain changes to the servo interface; the stand/clip/outlet interfaces stay.
old=from_stl('02_hopper_with_servo_mount.stl')
change_roi=box(20,-19,-1,30,50,11)
assert ((old-hopper)-change_roi).volume()<.005
assert ((hopper-old)-change_roi).volume()<.005
stand=from_stl('01_wide_cradle.stl').rotate((180,0,0)).translate((0,0,190))
assert (hopper.translate((0,0,186.3))^stand).volume()<.005
gate=from_stl('03_rotary_gate.stl')
# Nominal complete reference case, ears, boss and shaft from the supplied drawing.
case_face=8-(22.7-18.4)
case=box(35-5.9,-5.9,case_face,11.8,22.5,22.7)
ears=box(35-5.9,-10.6,8,11.8,4.7,2.5)+box(35-5.9,16.6,8,11.8,4.7,2.5)
boss=(cyl(35,0,case_face-4,5.9,4)+cyl(35,6.3,case_face-4,2.5,4)).hull()
shaft=cyl(35,0,case_face-7.2,2.3,3.2)
reference=case+ears+boss+shaft
assert (reference^hopper).volume()<.005
# Boss profile alone with the drawing's +1.5% XY allowance.
boss_tol=boss.translate((-35,0,0)).scale((1.015,1.015,1)).translate((35,0,0))
assert (boss_tol^hopper).volume()<.005
for angle in range(-70,71,5):
    g=gate.rotate((0,0,angle)).translate((35,0,-6.1))
    assert (g^hopper).volume()<.005
    assert (g^reference).volume()<.005

plate=new.copy();plate.apply_translation((101,128,0))
assert np.all(plate.bounds[0]>=0) and np.all(plate.bounds[1]<=[256,256,256])
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
model=ET.Element('{'+ns+'}model',{'unit':'millimeter'})
ET.SubElement(model,'{'+ns+'}metadata',{'name':'Title'}).text='V3.1 HOPPER ONLY - enlarged SG90 opening and tail relief; physical fit not verified'
res=ET.SubElement(model,'{'+ns+'}resources');obj=ET.SubElement(res,'{'+ns+'}object',{'id':'1','type':'model','name':'07_HOPPER_SG90_RELIEF_V3_1'})
me=ET.SubElement(obj,'{'+ns+'}mesh');vs=ET.SubElement(me,'{'+ns+'}vertices');fs=ET.SubElement(me,'{'+ns+'}triangles')
for v in plate.vertices:ET.SubElement(vs,'{'+ns+'}vertex',dict(zip(('x','y','z'),[f'{q:.6f}' for q in v])))
for f in plate.faces:ET.SubElement(fs,'{'+ns+'}triangle',dict(zip(('v1','v2','v3'),map(str,f))))
build=ET.SubElement(model,'{'+ns+'}build');ET.SubElement(build,'{'+ns+'}item',{'objectid':'1'})
with zipfile.ZipFile(OUT/'PRINT_THIS_HOPPER_ONLY_V3_1.3mf','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
report={'version':'V3.1 hopper only','user_choice':'User explicitly declined a separate test print and requested a wider hole with relief margin.','reference':'Detailed SG90 drawing supplied by user; exact purchased servo is not verified.','opening_mm':{'main_diameter':15,'tail_width':8,'shaft_center_to_tail_tip':11,'nominal_drawing_tail_tip':8.8,'extra_tip_clearance':2.2},'ear_supports':{'top_z':8,'height_above_flange_top':5,'increase_over_original':1,'near_y':[-17,-6.3],'far_y':[17.3,29]},'unchanged':['124 x 104 x 3 mm flange','Powder outlet and cone','Servo shaft centre at x35,y0','Zip-tie slots','Stand/clip interfaces','Gate, lid, clips and stand do not need reprinting for this change.'],'checks':'Watertight connected mesh; changes confined to servo interface; nominal complete reference servo and +1.5% XY boss profile clear; gate sweep and stand clearance checked.','physical_fit_verified':False,'unverified':['Exact purchased servo dimensions and vertical tolerance stack','Supplied horn socket depth and full seating','Physical PETG fit and flow performance']}
(OUT/'replacement_hopper_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
