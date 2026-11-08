"""Small diagnostic parts from the user's detailed SG90 drawing, not a proven unit fit.

Does not regenerate or replace the full hopper/stand. See docs/SERVO_FIT_AUDIT.md.
"""
from pathlib import Path
import json
import zipfile
import xml.etree.ElementTree as ET
import manifold3d as mf
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/hardware/servo-fit'
OUT.mkdir(parents=True,exist_ok=True)

def box(x,y,z,dx,dy,dz): return mf.Manifold.cube((dx,dy,dz)).translate((x,y,z))
def cyl(x,y,z,r,h): return mf.Manifold.cylinder(h,r,r,96).translate((x,y,z))
def mesh(solid):
    data=solid.to_mesh()
    result=trimesh.Trimesh(np.asarray(data.vert_properties)[:,:3],np.asarray(data.tri_verts),process=True)
    assert result.is_watertight and result.is_winding_consistent
    return result

# Circle stays the existing 14 mm diameter. Only the +Y tail side gains relief.
old_opening=cyl(0,0,-1,7,5)
relief=old_opening+cyl(0,6.5,-1,3.2,5)
relief+=box(-3.2,0,-1,6.4,6.5,5)
gauge=box(-15,-15,0,30,30,3)-relief
assert len(gauge.decompose())==1
parts={'01_BOSS_PROFILE_GAUGE_TEST_FIRST':gauge.translate((15,15,0))}
# These bridge only the ear regions; they must not protrude under the case body.
for height,label in [(1.,'1p0'),(1.4,'1p4')]:
    parts['02_NEAR_EAR_BRIDGE_'+label]=box(0,0,0,18,10.7,height)
    parts['03_FAR_EAR_BRIDGE_'+label]=box(0,0,0,18,11.7,height)

# Reference boss envelope derived from the supplied drawing, with its stated
# +1.5% tolerance. This does not identify the user's WWZMDiB unit.
nominal=(cyl(0,0,-.2,5.9,3.4)+cyl(0,6.3,-.2,2.5,3.4)).hull()
worst=nominal.scale((1.015,1.015,1))
assert (worst^gauge).volume()<.001
assert (nominal^(box(-15,-15,0,30,30,3)-old_opening)).volume()>.01

# Audit the known V3 interface against this drawing's complete rigid envelopes.
# This reference deliberately does not claim to model the user's horn socket.
old_mesh=trimesh.load(ROOT/'public/hardware/stl/02_hopper_with_servo_mount.stl')
old_hopper=mf.Manifold(mf.Mesh(old_mesh.vertices.astype(np.float32),old_mesh.faces.astype(np.uint32)))
repaired_hopper=old_hopper-relief.translate((35,0,0))
gate_mesh=trimesh.load(ROOT/'public/hardware/stl/03_rotary_gate.stl')
gate_solid=mf.Manifold(mf.Mesh(gate_mesh.vertices.astype(np.float32),gate_mesh.faces.astype(np.uint32)))
height_checks=[]
for height in [0.,1.,1.4]:
    ear_plane=7+height
    case_face=ear_plane-(22.7-18.4)
    case=box(35-5.9,-5.9,case_face,11.8,22.5,22.7)
    boss=(cyl(35,0,case_face-4,5.9,4)+cyl(35,6.3,case_face-4,2.5,4)).hull()
    shaft=cyl(35,0,case_face-7.2,2.3,3.2)
    ears=box(35-5.9,-10.6,ear_plane,11.8,4.7,2.5)+box(35-5.9,16.6,ear_plane,11.8,4.7,2.5)
    reference=case+boss+shaft+ears
    if height==0:
        assert (case^old_hopper).volume()>.01
        continue
    near=box(26,-17,7,18,10.7,height)
    far=box(26,17.3,7,18,11.7,height)
    assert (reference^repaired_hopper).volume()<.001
    assert (reference^near).volume()<.001 and (reference^far).volume()<.001
    for angle in range(-70,71,5):
        gate_pose=gate_solid.rotate((0,0,angle)).translate((35,0,-6.1))
        assert (reference^gate_pose).volume()<.001
    height_checks.append({'bridge_height_mm':height,'case_to_flange_top_clearance_mm':round(case_face-3,3),'boss_to_printed_gate_top_clearance_mm':round(case_face-4+.6,3),'shaft_tip_below_flange_bottom_mm':round(7.2-case_face,3),'horn_seating_verified':False})

layout=[('01_BOSS_PROFILE_GAUGE_TEST_FIRST',12,12),('02_NEAR_EAR_BRIDGE_1p0',50,12),('03_FAR_EAR_BRIDGE_1p0',50,30),('02_NEAR_EAR_BRIDGE_1p4',76,12),('03_FAR_EAR_BRIDGE_1p4',76,30)]
meshes=[]
for name,part in parts.items():mesh(part).export(OUT/(name+'.stl'))
for name,x,y in layout:
    m=mesh(parts[name].translate((x,y,0)))
    assert np.all(m.bounds[0]>=0) and np.all(m.bounds[1]<=[256,256,256])
    meshes.append(m)

ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',ns)
model=ET.Element('{'+ns+'}model',{'unit':'millimeter'})
ET.SubElement(model,'{'+ns+'}metadata',{'name':'Title'}).text='SG90 FIT TEST ONLY - boss gauge and candidate ear bridges; not physically verified'
resources=ET.SubElement(model,'{'+ns+'}resources');build=ET.SubElement(model,'{'+ns+'}build')
for i,((name,_,_),m) in enumerate(zip(layout,meshes),1):
    obj=ET.SubElement(resources,'{'+ns+'}object',{'id':str(i),'type':'model','name':name})
    me=ET.SubElement(obj,'{'+ns+'}mesh');vertices=ET.SubElement(me,'{'+ns+'}vertices');faces=ET.SubElement(me,'{'+ns+'}triangles')
    for vertex in m.vertices:ET.SubElement(vertices,'{'+ns+'}vertex',dict(zip(('x','y','z'),[f'{v:.6f}' for v in vertex])))
    for face in m.faces:ET.SubElement(faces,'{'+ns+'}triangle',dict(zip(('v1','v2','v3'),map(str,face))))
    ET.SubElement(build,'{'+ns+'}item',{'objectid':str(i)})
with zipfile.ZipFile(OUT/'SG90_SMALL_FIT_TEST_KIT.3mf','w',zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    archive.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    archive.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
report={'purpose':'Small fit diagnostics for the already-printed V3 hopper; not a full replacement or confirmed physical fit','source':'User-supplied detailed SG90/Addicore drawing, labelled tolerance +/-1.5%; exact WWZMDiB unit not verified','drawing_mm':{'round_boss_diameter':11.8,'shaft_center_to_tail_tip':8.8,'tail_width':5.,'boss_projection':4.,'shaft_projection':3.2,'case_length':22.5,'case_width':11.8,'case_height':22.7,'ear_top_from_case_bottom':18.4,'ear_bottom_from_case_bottom':15.9},'gauge_mm':{'main_hole_diameter':14,'relief_width':6.4,'shaft_center_to_relief_tip':9.7,'thickness':3},'bridge_candidates_mm':[1.,1.4],'reference_only_height_checks':height_checks,'geometry_checks':'Reference boss at +1.5% clears gauge; old circular profile collides. Nominal complete case/boss/shaft/ear envelopes clear relieved hopper and printed gate with either candidate bridge pair. Horn/socket omitted because dimensions are unknown. This is not a physical fit check.','solid_volume_mm3':sum(m.volume for m in meshes),'physical_tested':False,'unverified':['Purchased servo identity and actual dimensions','Horn socket depth and seating','Insertion force and print dimensional accuracy','Mounting ear, case, boss and gate clearance on assembled physical parts']}
(OUT/'fit_test_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
