from pathlib import Path
import json, zipfile, xml.etree.ElementTree as ET
import numpy as np
import manifold3d as mf
import trimesh

O=Path(__file__).resolve().parents[1]
H=190.0
def box(x,y,z,dx,dy,dz):return mf.Manifold.cube((dx,dy,dz)).translate((x,y,z))
def cyl(x,y,z,r,h,r2=-1):return mf.Manifold.cylinder(h,r,r2,96).translate((x,y,z))
def tm(a):
 m=a.to_mesh();return trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
cx=27
# Original tapered pocket, on a wider roof. The two side walls leave the front open.
cradle=box(-112,-70,0,224,140,12)
opening=box(cx-62.5,-52.5,-1,125,105,4.2)
opening+=(box(cx-62.5,-52.5,3.2,125,105,.01)+box(cx-55,-45,10.7,110,90,.01)).hull()
opening+=box(cx-55,-45,10.7,110,90,3)
cradle-=opening
for x in [-112,100]:cradle+=box(x,-70,11.8,12,140,H-11.8)
# Lightening window in the unused left roof; also holds both clips on the print plate.
cradle-=box(-98,-48,-1,55,96,15)
stand=cradle.rotate((180,0,0)).translate((0,0,H))
# Access notches make the flange and lower ledge accessible to removable C-clips.
for x,sign in [(-25,-1),(85,1)]:
 y=-71 if sign<0 else 51.7
 stand-=box(x-6,y,H-13,12,19.3,H+1-(H-13))
 y=-49 if sign<0 else 45.5
 stand-=box(x-4.6,y,H-12,9.2,3.5,1.2)
cradle=stand.rotate((180,0,0)).translate((0,0,H))

hopper=box(cx-62,-52,0,124,104,3)+cyl(0,0,2.8,10,55.2,33)
hopper-=cyl(0,0,-1,7,4.2)+cyl(0,0,3,7,55.2,30.08)+cyl(35,0,-1,7,5)
for y in [-17,20]:hopper+=box(26,y,2.8,18,9,4.2)
for x in [23,47]:
 for y in [0,12]:hopper-=box(x-1.8,y-3,-1,3.6,6,5)
gate=cyl(0,0,0,44,5.5)-cyl(-35,0,-1,7,8)-cyl(0,0,-1,3.4,8)-box(-16,-4.5,2.1,32,9,4.4)
for x in [-10,10]:
 for y in [-6.4,6.4]:gate-=box(x-1.6,y-1.4,-1,3.2,2.8,8)
 gate-=box(x-1.6,-8,0,3.2,16,1.3)
lid=cyl(0,0,0,35,2.4)+cyl(0,0,2.2,34.6,5)-cyl(0,0,2.4,33.5,6)
# Clip prints on its broad C-shaped side: flexure bends within the layers.
# Opening 11.7 mm captures an 11.3 mm stack, with a separate 0.8 mm locking hook.
clip=box(0,0,0,14.9,2.2,8)+box(0,1.8,0,1.4,16.3,8)+box(13.1,1.8,0,1.8,16.3,8)
clip+=box(1.35,10.1,0,.85,2,8)
clip+=(box(1.35,12.0,0,.85,.1,8)+box(1.35,13.1,0,.01,.01,8)).hull()
parts={'01_wide_cradle':cradle,'02_hopper_with_servo_mount':hopper,'03_rotary_gate':gate,'04_lid':lid,'05_locking_clip':clip}
for name,p in parts.items():
 assert len(p.decompose())==1,name
 m=tm(p);assert m.is_watertight and m.is_winding_consistent,name
 m.export(O/'stl'/f'{name}.stl')
# Optional small fit coupon, excluded from the six-piece full-build plate.
coupon=box(-6,-51.7,H-12,12,16.7,11.3)-box(-4.6,-49,H-12,9.2,3.5,1.2)
coupon=coupon.rotate((180,0,0)).translate((6,-35,H-.7))
tm(coupon).export(O/'stl/06_OPTIONAL_CLIP_FIT_COUPON.stl')
layout=[('01_wide_cradle',116,74),('02_hopper_with_servo_mount',41,200),('03_rotary_gate',151,74),('04_lid',211,200),('05_locking_clip',25,35),('05_locking_clip',48,35)]
positioned=[];meshes=[]
for name,x,y in layout:
 p=parts[name].translate((x,y,0));m=tm(p)
 assert np.all(m.bounds[0]>=0) and np.all(m.bounds[1]<=[256,256,256]),(name,m.bounds)
 for old in positioned:assert (p^old).volume()<.001,name
 positioned.append(p);meshes.append(m)
trimesh.util.concatenate(meshes).export(O/'A1_V3_WIDE_ONE_PLATE.stl')
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
model=ET.Element('{'+ns+'}model',{'unit':'millimeter'});ET.SubElement(model,'{'+ns+'}metadata',{'name':'Title'}).text='Flour V3 - wide robot bay and two locking clips - geometry only'
res=ET.SubElement(model,'{'+ns+'}resources');build=ET.SubElement(model,'{'+ns+'}build')
for i,((name,_,_),m) in enumerate(zip(layout,meshes),1):
 obj=ET.SubElement(res,'{'+ns+'}object',{'id':str(i),'type':'model','name':name});me=ET.SubElement(obj,'{'+ns+'}mesh');vs=ET.SubElement(me,'{'+ns+'}vertices');fs=ET.SubElement(me,'{'+ns+'}triangles')
 for v in m.vertices:ET.SubElement(vs,'{'+ns+'}vertex',dict(zip(('x','y','z'),[f'{q:.6f}' for q in v])))
 for f in m.faces:ET.SubElement(fs,'{'+ns+'}triangle',dict(zip(('v1','v2','v3'),map(str,f))))
 ET.SubElement(build,'{'+ns+'}item',{'objectid':str(i)})
with zipfile.ZipFile(O/'A1_V3_WIDE_ONE_PLATE.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
front=clip.rotate((0,-90,0)).translate((-21,-58.6,H-13.6))
rear=clip.rotate((0,-90,0)).translate((4,-58.6,H-13.6)).rotate((0,0,180)).translate((85,0,0))
assembled=[stand,hopper.translate((0,0,H-3.7)),gate.rotate((0,0,60)).translate((35,0,H-9.8)),lid.rotate((180,0,0)).translate((0,0,H+56.7)),front,rear]
for i,a in enumerate(assembled):
 for j,b in enumerate(assembled[:i]):assert (a^b).volume()<.02,(i,j,(a^b).volume())
for angle in range(-70,71,5):
 g=gate.rotate((0,0,angle)).translate((35,0,H-9.8))
 for i,a in enumerate([stand,assembled[1],front,rear]):assert (g^a).volume()<.02,(angle,i,(g^a).volume())
# Rigid-body checks: hooks block withdrawal and jaws block hopper lifting.
assert (front.translate((0,-1,0))^stand).volume()>.01
assert (rear.translate((0,1,0))^stand).volume()>.01
assert (assembled[1].translate((0,0,1))^front).volume()>.01
assert (assembled[1].translate((0,0,1))^rear).volume()>.01
scale=box(-52.5,-62.5,0,105,125,17)
assert all((scale^p).volume()<.001 for p in assembled)
for distance in range(0,146,5):
 cup=cyl(0,-distance,32,30,80)
 assert all((cup^p).volume()<.001 for p in assembled)
trimesh.util.concatenate([tm(a) for a in assembled]).export(O/'V3_ASSEMBLED_REFERENCE_DO_NOT_PRINT.stl')
report={'status':'Digital checks passed; no physical tests','version':3,'printed_pieces':6,'distinct_printed_models':5,'stand_outer_mm':[224,140,190],'clear_bay_width_mm':200,'scale_mm':[105,125,17],'gate_bottom_height_mm':180.2,'conservative_clearance_below_fastener_mm':175,'example_cup_mm':[60,60,80],'cup_size_assumed':True,'plate_bounds_mm':trimesh.util.concatenate(meshes).bounds.tolist(),'clip_hook_engagement_mm':.6,'clip_hook_height_mm':.8,'clip_gap_mm':11.7,'clamped_stack_mm':11.3,'gate_gap_mm':.6,'sweep_degrees':[-70,70],'retention':'Two printed C-clips with hooks engaging underside recesses; no retaining bands','limitations':['Clip insertion flex, retention force and durability not physically tested','Robot model/pose and real cup unspecified; no robot collision or reach validation','Scale must rest on table and not touch stand; stop vibration before weighing','Hardware fit, flour flow and shutoff remain untested']}
report['known_servo_fit_issue']='User reported SG90 gearbox tail interference. Original round opening and ear-height stack are not verified. Do not recommend the full plate as a confirmed servo fit; use the repair guide and small physical test.'
(O/'validation_v3.json').write_text(json.dumps(report,indent=2))
