from pathlib import Path
import json,math,zipfile,xml.etree.ElementTree as ET,shutil
import numpy as np,manifold3d as mf,trimesh
O=Path(__file__).resolve().parents[1]; R=O.parent.parent; O.mkdir(exist_ok=True)
(O/'stl').mkdir(exist_ok=True)
def box(x,y,z,dx,dy,dz):return mf.Manifold.cube((dx,dy,dz)).translate((x,y,z))
def cyl(x,y,z,r,h,r2=-1):return mf.Manifold.cylinder(h,r,r2,96).translate((x,y,z))
def tm(a):
    m=a.to_mesh();return trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
# Cradle printed inverted: pocket mouth on bed, walls grow upward. Its retaining
# ledge grows inward at 45 degrees, rather than printing a suspended top plate.
cx=27
cradle=box(cx-67,-57,0,134,114,12)
opening=box(cx-62.5,-52.5,-1,125,105,4.2)
# A tapered rectangular hole: use a convex hull of two thin rectangles.
lower=box(cx-62.5,-52.5,3.2,125,105,.01)
upper=box(cx-55,-45,10.7,110,90,.01)
opening+=(lower+upper).hull()
opening+=box(cx-55,-45,10.7,110,90,3)
cradle-=opening
cradle+=box(cx-67,-57,11.8,134,6,80.2)
cradle+=box(cx-67,51,11.8,134,6,80.2)
# End webs are local to the ledge, never a ceiling across the cup opening.
cradle+=box(cx-67,-51,11.8,5,102,10)
cradle+=box(cx+62,-51,11.8,5,102,10)

hopper=box(cx-62,-52,0,124,104,3)
hopper+=cyl(0,0,2.8,10,55.2,33)
hopper-=cyl(0,0,-1,7,4.2)
hopper-=cyl(0,0,3,7,55.2,30.08)
hopper-=cyl(35,0,-1,7,5)
# SG90 is above the flange, output shaft down: no lower servo platform.
# Ears sit on these two blocks; cardboard packing adjusts clone shaft height.
for yy in (-17,20):hopper+=box(26,yy,2.8,18,9,4.2)
for xx in (23,47):
    for yy in (0,12):hopper-=box(xx-1.8,yy-3,-1,3.6,6,5)

gate=cyl(0,0,0,44,5.5)-cyl(-35,0,-1,7,8)-cyl(0,0,-1,3.4,8)
gate-=box(-16,-4.5,2.1,32,9,4.4)
for xx in (-10,10):
    for yy in (-6.4,6.4):gate-=box(xx-1.6,yy-1.4,-1,3.2,2.8,8)
    gate-=box(xx-1.6,-8,0,3.2,16,1.3)
lid=cyl(0,0,0,35,2.4)+cyl(0,0,2.2,34.6,5)-cyl(0,0,2.4,33.5,6)
parts={'01_drop_in_cradle':cradle,'02_hopper_with_servo_mount':hopper,'03_rotary_gate':gate,'04_lid':lid}
for name,part in parts.items():
    m=tm(part)
    assert m.is_watertight and m.is_winding_consistent and len(part.decompose())==1,name
    m.export(O/'stl'/f'{name}.stl')
layout=[('01_drop_in_cradle',54,69),('02_hopper_with_servo_mount',65,190),('03_rotary_gate',203,65),('04_lid',204,158)]
plate=[]
for name,x,y in layout:
    m=tm(parts[name]);m.apply_translation((x,y,0));plate.append(m)
    assert np.all(m.bounds[0]>=-1e-5) and np.all(m.bounds[1]<=[250,250,250])
for i,m in enumerate(plate):
    for n in plate[:i]:
        assert not np.all(np.minimum(m.bounds[1,:2],n.bounds[1,:2])>np.maximum(m.bounds[0,:2],n.bounds[0,:2]))
trimesh.util.concatenate(plate).export(O/'A1_SIMPLE_V2_ONE_PLATE.stl')
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
model=ET.Element('{'+ns+'}model',{'unit':'millimeter'})
ET.SubElement(model,'{'+ns+'}metadata',{'name':'Title'}).text='Flour v2 - four parts - geometry only'
res=ET.SubElement(model,'{'+ns+'}resources');build=ET.SubElement(model,'{'+ns+'}build')
for i,((name,x,y),m) in enumerate(zip(layout,plate),1):
    obj=ET.SubElement(res,'{'+ns+'}object',{'id':str(i),'type':'model','name':name});me=ET.SubElement(obj,'{'+ns+'}mesh')
    vs=ET.SubElement(me,'{'+ns+'}vertices');fs=ET.SubElement(me,'{'+ns+'}triangles')
    for v in m.vertices:ET.SubElement(vs,'{'+ns+'}vertex',dict(zip(('x','y','z'),map(lambda q:f'{q:.6f}',v))))
    for f in m.faces:ET.SubElement(fs,'{'+ns+'}triangle',dict(zip(('v1','v2','v3'),map(str,f))))
    ET.SubElement(build,'{'+ns+'}item',{'objectid':str(i)})
with zipfile.ZipFile(O/'A1_SIMPLE_V2_ONE_PLATE.3mf','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))

# Validate assembled printed geometry. Top face of inverted cradle is z=92;
# hopper flange seats 3.2 mm into it, with slight clearance at the mouth.
assembled=[cradle.rotate((180,0,0)).translate((0,0,92)),hopper.translate((0,0,88.3)),gate.translate((35,0,82.2)),lid.rotate((180,0,0)).translate((0,0,148.7))]
for i,a in enumerate(assembled):
    for j,b in enumerate(assembled[:i]):
        assert (a^b).volume()<.02,(i,j,(a^b).volume())
for angle in range(-70,71,5):
    g=gate.rotate((0,0,angle)).translate((35,0,82.2))
    assert all((g^a).volume()<.02 for a in assembled[:2]),angle
trimesh.util.concatenate([tm(a) for a in assembled]).export(O/'assembled_reference_do_not_print.stl')
report={'status':'Digital mesh and assembly checks passed; not physically tested','printed_parts':4,'structural_screws':0,'servo_horn_screws':1,
    'plate_bounds_mm':trimesh.util.concatenate(plate).bounds.tolist(),'gate_top_clearance_mm':.6,'rotor_sweep_checked_degrees':[-70,70],
    'drop_in_pocket_mm':[125,105],'hopper_flange_mm':[124,104],
    'limitations':['Hopper is gravity-seated, not latched: two retaining bands required before powered testing','SG90 horn height requires packing adjustment','Flour flow, vibration and shutoff are untested','Gate is not sealed or fail-closed']}
(O/'validation.json').write_text(json.dumps(report,indent=2))
