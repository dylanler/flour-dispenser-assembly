import './fit-check.css';
import * as T from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { fitState, outletOverlapArea } from './fit-math.js';
import { powerLayout } from './power-layout.js';
const $=s=>document.querySelector(s), base=import.meta.env.BASE_URL+'hardware/';
const scene=new T.Scene();scene.background=new T.Color('#e9ede4');
const camera=new T.PerspectiveCamera(34,1,.05,2500);camera.up.set(0,0,1);
const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.localClippingEnabled=true;renderer.outputColorSpace=T.SRGBColorSpace;$('#viewport').prepend(renderer.domElement);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;orbit.minDistance=12;orbit.maxDistance=1100;
scene.add(new T.HemisphereLight('#ffffff','#788873',2.4));
const light=new T.DirectionalLight('#fff5e4',3);light.position.set(100,-180,350);scene.add(light);
const fill=new T.DirectionalLight('#dce9ff',1.7);fill.position.set(-160,100,150);scene.add(fill);
const cut=new T.Plane(new T.Vector3(1,0,0),-35), materials=[];
function material(color,options={}){const m=new T.MeshStandardMaterial({color,roughness:.65,metalness:.05,side:T.DoubleSide,...options});materials.push(m);return m;}
function mesh(geometry,color,parent=scene,options={}){const m=new T.Mesh(geometry,material(color,options));parent.add(m);return m;}
function box(w,d,h,color,p,parent=scene){const m=mesh(new T.BoxGeometry(w,d,h),color,parent);m.position.set(...p);return m;}
function cylinder(r,h,color,p,parent=scene,r2=r){const g=new T.CylinderGeometry(r2,r,h,64);g.rotateX(Math.PI/2);const m=mesh(g,color,parent);m.position.set(...p);return m;}
function tube(points,color,parent=scene,r=.65){return mesh(new T.TubeGeometry(new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p))),50,r,6,false),color,parent);}
function ring(ro,ri,z,h,color,parent){const shape=new T.Shape();shape.absarc(0,0,ro,0,Math.PI*2,false);const hole=new T.Path();hole.absarc(0,0,ri,0,Math.PI*2,true);shape.holes.push(hole);const g=new T.ExtrudeGeometry(shape,{depth:Math.max(.001,h),bevelEnabled:false,curveSegments:64});g.translate(0,0,z);return mesh(g,color,parent);}
const floor=box(1200,1000,1,'#e4e8de',[0,0,-1]);const grid=new T.GridHelper(600,24,'#c0caba','#d4dccf');grid.rotation.x=Math.PI/2;grid.position.z=-.4;scene.add(grid);
const printed=[],reference=[],labels=[];
function addLabel(text,point,visible=()=>true){const el=document.createElement('div');el.className='part-label';el.textContent=text;$('#labels').append(el);labels.push({el,point,visible});}
const loader=new STLLoader();async function stl(path,color,parent=scene){return mesh(await loader.loadAsync(base+path),color,parent);}
const servo=new T.Group(), gateRoot=new T.Group(), hornRoot=new T.Group(), tieRoot=new T.Group(), electronics=new T.Group(), scaleGroup=new T.Group(), aux=new T.Group();scene.add(servo,gateRoot,hornRoot,tieRoot,electronics,scaleGroup,aux);
let stand,hopper,lid,clips=[],report,state,playing=false,lastTime=0,tick=0,xray=false,section=false,currentView='interface';
const hornGeo=new T.Group();hornRoot.add(hornGeo);const tieGeo=new T.Group();tieRoot.add(tieGeo);
let packingMeshes=[],unusedPacking=[],armGeometry={};
function disposeChildren(group){for(const child of [...group.children]){group.remove(child);child.traverse(o=>{if(o.geometry)o.geometry.dispose();if(o.material){const ix=materials.indexOf(o.material);if(ix>=0)materials.splice(ix,1);o.material.dispose();}});}}
function readState(){return fitState({extension:+$('#extension').value,mouthGap:+$('#mouth').value,socketDepth:+$('#depth').value,packing:+$('#packing').value});}
function modelHorn(s){
 disposeChildren(hornGeo);disposeChildren(tieGeo);
 const length=+$('#horn-size').value,P=s.contact,M=s.mouth,B=s.bottom,hb=s.hubBottom;
 // Conservative straight-arm envelope. Socket is a smooth proxy, not real teeth.
 const arms=mesh(armGeometry[length].clone(),'#f4efd8',hornGeo);arms.position.z=P+6.5;
 ring(5,1.1,hb,B-hb,'#f4efd8',hornGeo);ring(5,2.4,B,M-B,'#f4efd8',hornGeo);
 // Screw geometry is illustrative and intentionally enters the shaft; excluded from audit.
 cylinder(.9,5,'#929b93',[0,0,hb+1.8],hornGeo);cylinder(2,.8,'#777f79',[0,0,hb-.4],hornGeo);
 const top=P+2,bottom=s.gateBottom-.25;
 for(const x of [-13,13]){
  box(2.5,16.4,.8,'#414d43',[x,0,top+.4],tieGeo);
  box(2.5,16.4,.8,'#414d43',[x,0,bottom+.4],tieGeo);
  for(const y of [-8.2,8.2])box(2.5,.8,top-bottom+.8,'#414d43',[x,y,(top+bottom+.8)/2],tieGeo);
 }
 let z=1.4;const selected=Math.round(+$('#packing').value/.4);
 packingMeshes.forEach((m,i)=>{m.visible=!!(selected&(1<<i));m.position.set(0,0,z);if(m.visible)z+=[.4,.8,1.6][i];unusedPacking[i].visible=!m.visible;});
 hornGeo.traverse(o=>{if(o.material)o.material.clippingPlanes=section?[cut]:[];});tieGeo.traverse(o=>{if(o.material)o.material.clippingPlanes=section?[cut]:[];});
}
function sync(){
 state=readState();modelHorn(state);
 for(const id of ['extension','mouth','depth'])$('#'+id+'-value').textContent=(+$('#'+id).value).toFixed(1)+' mm';
 $('#gap').textContent=state.gap.toFixed(2)+' mm';$('#engagement').textContent=state.overlap.toFixed(2)+' mm';$('#tip-gap').textContent=state.tipClearance.toFixed(2)+' mm';
 $('#gap').classList.toggle('bad-value',!state.gapInRange);$('#tip-gap').classList.toggle('bad-value',state.shaftBottomsOut);
 const errors=[];if(state.gateInterference)errors.push('gate overlaps hopper plane');else if(!state.gapInRange)errors.push('gate gap outside 0.4–0.8 mm');if(state.shaftBottomsOut)errors.push('shaft bottoms out in assumed socket');if(state.bossInterference)errors.push('horn mouth overlaps boss face');if(!state.screeningEngagementPass)errors.push('overlap below assumed 2 mm screening threshold');
 if(report.unintended_interferences.length)errors.push('reference collision audit failed');
 const failed=state.gateInterference||state.shaftBottomsOut||state.bossInterference||report.unintended_interferences.length>0;
 const verdict=$('.verdict');verdict.classList.toggle('bad',failed);verdict.classList.toggle('warn',!failed&&errors.length>0);
 $('#verdict').textContent=failed?'INTERFERENCE / SEATING CONFLICT':errors.length?'PARAMETER CHANGE NEEDS REVIEW':'REFERENCE FIT CLEAR · HORN VALUES ASSUMED';
 $('#verdict-detail').textContent=errors.length?errors.join('; '):'Default solid-intersection sweep passed. Full physical fit and actual horn seating remain unverified.';
 gateRoot.children[0]?.material?.color.set(state.gateInterference?'#bd4f39':'#d1aa53');
 hornGeo.traverse(o=>{if(o.material&&o.material.color&&o.material.color.getHexString()==='f4efd8'&&failed)o.material.color.set('#ce6b49');});
 window.fitSimulation.state={...state};
}
function view(name){
 currentView=name;for(const b of document.querySelectorAll('[data-view]'))b.classList.toggle('active',b.dataset.view===name);
 xray=name==='interface';$('#xray').classList.toggle('active',xray);
 if(name==='whole'){camera.position.set(450,-560,360);orbit.target.set(40,-25,115);$('#lid').checked=true;}
 if(name==='interface'){camera.position.set(110,-105,205);orbit.target.set(35,0,186);$('#lid').checked=false;}
 if(name==='under'){camera.position.set(95,-110,95);orbit.target.set(33,0,181);$('#lid').checked=false;}
 orbit.update();
}
function updatePose(){
 const e=+$('#explode').value,angle=+$('#angle').value*Math.PI/180;
 $('#angle-value').textContent=(+$('#angle').value).toFixed(0)+'°';$('#explode-value').textContent=Math.round(e*100)+'%';
 $('#aperture').textContent=outletOverlapArea(+$('#angle').value).toFixed(2)+' mm²';
 $('#mode-note').textContent=e>0?'EXPLODED · CHECKS REFER TO ASSEMBLED MODEL':section?'OPEN HALF-SECTION · CUT AT SHAFT AXIS':'ASSEMBLED · MILLIMETRES';
 hopper.position.z=186.3+e*12;servo.position.z=186.3+e*55;lid.position.z=246.7+e*100;
 gateRoot.position.set(35,0,186.3+state.gateBottom-e*48);hornRoot.position.set(35,0,186.3-e*17);tieRoot.position.set(35,0,186.3-e*34);
 gateRoot.rotation.z=hornRoot.rotation.z=tieRoot.rotation.z=angle;
 clips.forEach((c,i)=>c.position.y=(i?1:-1)*e*32);
 stand.visible=clips.every(()=>$('#stand').checked);clips.forEach(c=>c.visible=$('#stand').checked);lid.visible=$('#lid').checked;electronics.visible=$('#electronics').checked;scaleGroup.visible=$('#cup').checked;aux.visible=$('#aux').checked;
 printed.forEach(m=>{m.material.transparent=xray;m.material.opacity=xray?(m===gateRoot.children[0] ? 0.65 : 0.18):1;m.material.depthWrite=!xray;});
}
try{
 report=await (await fetch(base+'simulation/assembly_collision_report.json')).json();
 for(const length of [32,35])armGeometry[length]=await loader.loadAsync(base+'simulation/horn_arms_'+length+'.stl');
 stand=await stl('stl/01_wide_cradle.stl','#9bb7a9');stand.rotation.x=Math.PI;stand.position.z=190;
 hopper=await stl('servo-fit/08_HOPPER_ORIGINAL_SERVO_HEIGHT_V3_2.stl','#c8805e');
 lid=await stl('stl/04_lid.stl','#ddbc78');lid.rotation.x=Math.PI;
 const gate=await stl('servo-fit/09_GATE_ADJUSTABLE_HORN_V3_2.stl','#d1aa53',gateRoot);
 for(const n of ['front','rear'])clips.push(await stl('simulation/'+n+'_clip_assembled.stl','#9f7846'));
 printed.push(stand,hopper,gate,lid,...clips);
 for(const n of ['case','ears','boss','shaft']){const m=await stl('simulation/servo_'+n+'.stl',n==='shaft'?'#e5e4d1':'#3c6fbd',servo);reference.push(m);}
 await stl('simulation/servo_ties_reference.stl','#414d43',servo);
 for(const [i,tag] of ['0p4','0p8','1p6'].entries()){
  packingMeshes.push(await stl('servo-fit/10_HORN_PACKING_'+tag+'_V3_2.stl','#86a890',gateRoot));
  const u=await stl('servo-fit/10_HORN_PACKING_'+tag+'_V3_2.stl','#86a890',aux);u.position.set(150,30+i*20,0);unusedPacking.push(u);
 }
 const spacer=await stl('servo-fit/11_ASSEMBLY_GAP_SPACER_0p6_V3_2.stl','#c9825a',aux);spacer.position.set(138,100,0);
 // Electronics are dimensioned placement illustrations, not validated purchased CAD.
 box(8,82,55,'#edece3',[118,0,55],electronics);box(.3,74,2,'#b35e45',[122.2,0,77],electronics);box(.3,74,2,'#4978a1',[122.2,0,34],electronics);
 const holes=new T.InstancedMesh(new T.SphereGeometry(.5,5,4),material('#6d796e'),300);electronics.add(holes);let hi=0;const matrix=new T.Matrix4();
 for(let row=0;row<30;row++)for(const side of [-1,1])for(let j=0;j<5;j++){matrix.makeTranslation(122.2,-36.8+row*2.54,55+side*(4+j*2.54));holes.setMatrixAt(hi++,matrix);}
 box(3,28,52,'#254236',[-116,0,65],electronics);box(3,18,20,'#9da99e',[-119,0,78],electronics);box(7,8,5,'#aeb8ae',[-119,-17,44],electronics);
 for(const z of [42,47,52,57,62,67,72,77,82])for(const y of [-12,12])box(3,1,1,'#d6b767',[-119,y,z],electronics);
 box(23,1.6,21,'#345d43',[0,-25,216],electronics);const coin=cylinder(5,3.4,'#a8b2aa',[0,-28,216],electronics);coin.rotation.x=Math.PI/2;
 box(10,4,3,'#2b3830',[0,-27,205],electronics);
 // Reuse the reviewed adapter orientation/routing: Y-up illustration -> Z-up.
 const yup=new T.Group();yup.rotation.x=Math.PI/2;electronics.add(yup);
 function yupBox(w,h,d,color,p){const m=mesh(new T.BoxGeometry(w,h,d),color,yup);m.position.set(...p);return m;}
 yupBox(...powerLayout.brickSize,'#eeeadd',powerLayout.brickCenter);yupBox(.6,8,15,'#29382e',powerLayout.portCenter);
 const [px,py,pz]=powerLayout.adapterOrigin;
 yupBox(11,4.5,12,'#adb8af',[px-14.5,py,pz]);yupBox(20,9,18,'#303c35',[px,py,pz]);yupBox(14,10,24,'#70a287',[px+17,py,pz]);
 for(const z of [-7.5,-2.5,2.5,7.5]){const m=mesh(new T.CylinderGeometry(1.7,1.7,.6,16),'#b7bfb7',yup);m.position.set(px+17,py+5.25,pz+z);}
 powerLayout.routes.forEach(r=>tube(r.points,r.color,yup));
 for(const [dy,color] of [[0,'#b85d43'],[3,'#334638']])tube([[41,12+dy,207],[80,24+dy,226],[137,40+dy,210],[135,45+dy,80],[123,15+dy,65]],color,electronics);
 tube([[45,18,207],[60,40,235],[-136,50,225],[-139,28,90],[-119,8,55]],'#d4b563',electronics);
 tube([[-119,-17,44],[-146,-65,30],[-160,-100,3],[-230,-130,3]],'#616f64',electronics,1.3);
 tube([[0,-28,205],[-35,-40,225],[-135,-50,210],[-139,-30,80],[-119,-8,55]],'#59778d',electronics);
 for(const [dx,color] of [[-3,'#b85d43'],[3,'#334638']])tube([[dx,-28,205],[50+dx,-45,230],[138,-48+dx,200],[136,-35+dx,90],[123,-12+dx,60]],color,electronics);
 tube([[-119,0,50],[-142,-70,22],[135,-70,22],[123,0,60]],'#334638',electronics);
 box(105,125,17,'#3f4a40',[0,0,8.5],scaleGroup);box(101,96,1,'#b5beb4',[0,12,16.5],scaleGroup);box(46,14,.6,'#6790ad',[0,-48,17.3],scaleGroup);
 ring(30,28.5,18.5,78.5,'#b8c6ab',scaleGroup);cylinder(30,1.5,'#b8c6ab',[0,0,17.75],scaleGroup);
 addLabel('SG90 · dimensioned reference',()=>new T.Vector3(35,6,servo.position.z+28));
 addLabel('Horn · socket values assumed',()=>new T.Vector3(47,-12,hornRoot.position.z+state.contact),()=>currentView!=='whole');
 addLabel('V3.2 hopper · actual STL',()=>new T.Vector3(-25,-35,hopper.position.z+8));
 addLabel('V3.2 gate · actual STL',()=>new T.Vector3(62,-22,gateRoot.position.z+4),()=>currentView!=='whole');
 addLabel('400-point breadboard · illustration',()=>new T.Vector3(124,0,88),()=>currentView==='whole'&&electronics.visible);
 addLabel('USB-C ESP32 · illustration',()=>new T.Vector3(-122,0,98),()=>currentView==='whole'&&electronics.visible);
 addLabel('USB-A adapter · 5V + GND only',()=>new T.Vector3(215,-120,22),()=>currentView==='whole'&&electronics.visible);
 addLabel('105 × 125 × 17 mm scale',()=>new T.Vector3(0,-60,24),()=>currentView==='whole'&&scaleGroup.visible);
 addLabel('Removed spacer + unused packing',()=>new T.Vector3(158,80,5),()=>currentView==='whole'&&aux.visible);
 const total=report.reference_static_checks.length+report.sweep.reduce((n,r)=>n+r.pairs_checked,0);$('#audit-count').textContent=`${total.toLocaleString()} pair checks / ${report.sweep.length} gate positions. ${report.unintended_interferences.length} unintended intersections in the nominal reference model.`;
 window.fitSimulation={state:null,report,setView:view,setValues(values){for(const [id,value] of Object.entries(values))$('#'+id).value=value;sync();updatePose();},get camera(){return camera;}};
 for(const id of ['extension','mouth','depth','packing','horn-size'])$('#'+id).addEventListener('input',sync);
 for(const id of ['angle','explode','stand','lid','electronics','cup','aux','label-toggle'])$('#'+id).addEventListener('input',updatePose);
 document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));
 $('#play').onclick=()=>{playing=!playing;$('#play').textContent=playing?'Ⅱ Pause sweep':'▶ Sweep 0–60°';};
 $('#section').onclick=()=>{section=!section;$('#section').classList.toggle('active',section);materials.forEach(m=>m.clippingPlanes=section?[cut]:[]);if(section){camera.position.set(-35,-75,195);orbit.target.set(35,0,184);orbit.update();}};
 $('#xray').onclick=()=>{xray=!xray;$('#xray').classList.toggle('active',xray);updatePose();};
 $('#reset').onclick=()=>{playing=false;section=false;xray=false;materials.forEach(m=>m.clippingPlanes=[]);$('#section').classList.remove('active');$('#xray').classList.remove('active');$('#play').textContent='▶ Sweep 0–60°';$('#extension').value=2;$('#mouth').value=.6;$('#depth').value=2.8;$('#packing').value=0;$('#horn-size').value=35;$('#explode').value=0;$('#angle').value=60;sync();view('interface');};
 new ResizeObserver(()=>{const w=$('#viewport').clientWidth,h=$('#viewport').clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}).observe($('#viewport'));
 sync();view('whole');$('#loading').hidden=true;
 function frame(now){const dt=Math.min(.1,(now-lastTime)/1000||0);lastTime=now;if(playing){tick+=dt;$('#angle').value=30-30*Math.cos(tick*1.2);}updatePose();orbit.update();
  for(const {el,point,visible} of labels){const v=point().project(camera);const show=$('#label-toggle').checked&&visible()&&v.z<1&&v.z>-1&&Math.abs(v.x)<.95&&Math.abs(v.y)<.95;el.hidden=!show;if(show){el.style.left=(v.x*.5+.5)*$('#viewport').clientWidth+'px';el.style.top=(-v.y*.5+.5)*$('#viewport').clientHeight+'px';}}
  renderer.render(scene,camera);requestAnimationFrame(frame);
 }requestAnimationFrame(frame);
}catch(error){$('#loading').textContent='Unable to load fit view: '+error.message;console.error(error);}
