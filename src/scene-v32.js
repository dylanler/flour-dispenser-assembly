import * as T from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {STLLoader} from 'three/addons/loaders/STLLoader.js';
import {powerLayout} from './power-layout.js';

// The assembly uses the same actual print meshes and source-labelled reference
// hardware as the fit laboratory. Horn socket and electronics remain assumptions.
export async function makeScene(host){
 const scene=new T.Scene();scene.background=new T.Color('#eceee5');
 const camera=new T.PerspectiveCamera(35,1,.1,2500);
 const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=T.SRGBColorSpace;host.append(renderer.domElement);
 const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;orbit.minDistance=35;orbit.maxDistance=1000;
 scene.add(new T.HemisphereLight('#ffffff','#92a18d',2.6));
 for(const [color,intensity,position] of [['#fff3df',3.2,[-140,350,200]],['#ddeaff',1.4,[200,180,-200]]]){const l=new T.DirectionalLight(color,intensity);l.position.set(...position);scene.add(l);}
 function material(color){return new T.MeshStandardMaterial({color,roughness:.7,metalness:.03,side:T.DoubleSide});}
 function mesh(g,color,parent=scene){const m=new T.Mesh(g,material(color));parent.add(m);return m;}
 function box(w,h,d,color,p,parent=scene){const m=mesh(new T.BoxGeometry(w,h,d),color,parent);m.position.set(...p);return m;}
 function cylinder(r,h,color,p,parent=scene){const m=mesh(new T.CylinderGeometry(r,r,h,64),color,parent);m.position.set(...p);return m;}
 function line(points,color,parent=scene,r=.6){return mesh(new T.TubeGeometry(new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p))),45,r,6,false),color,parent);}
 const loader=new STLLoader(),base=import.meta.env.BASE_URL+'hardware/',loadedPaths=[];
 async function geo(path){loadedPaths.push(path);const g=await loader.loadAsync(base+path);g.rotateX(-Math.PI/2);g.computeVertexNormals();return g;}
 const names={stand:'stl/01_wide_cradle.stl',hopper:'servo-fit/08_HOPPER_ORIGINAL_SERVO_HEIGHT_V3_2.stl',gate:'servo-fit/09_GATE_ADJUSTABLE_HORN_V3_2.stl',lid:'stl/04_lid.stl',front:'simulation/front_clip_assembled.stl',rear:'simulation/rear_clip_assembled.stl',horn:'simulation/horn_assumed_reference.stl',ties:'simulation/gate_ties_reference.stl',servoTies:'simulation/servo_ties_reference.stl',spacer:'servo-fit/11_ASSEMBLY_GAP_SPACER_0p6_V3_2.stl'};
 const entries=await Promise.all(Object.entries(names).map(async([k,p])=>[k,await geo(p)]));const g=Object.fromEntries(entries);
 const packingGeo=await Promise.all(['0p4','0p8','1p6'].map(tag=>geo('servo-fit/10_HORN_PACKING_'+tag+'_V3_2.stl')));
 box(1200,1,1200,'#e3e8dc',[0,-1,0]);const grid=new T.GridHelper(650,26,'#c6d0bd','#d7dece');scene.add(grid);
 const cradle=mesh(g.stand,'#9bbab0');cradle.rotation.x=Math.PI;cradle.position.y=190;
 const head=new T.Group();scene.add(head);const hopper=mesh(g.hopper,'#d18865',head);
 const servo=new T.Group();head.add(servo);
 for(const part of ['case','ears','boss','shaft'])mesh(await geo('simulation/servo_'+part+'.stl'),part==='shaft'?'#eee9d6':'#3c6fbd',servo);
 for(const[j,color]of ['#b94a3f','#33433c','#c39b3c'].entries())line([[33+j*2,22,-16.6],[33+j*2,25,-27],[33+j*2,27,-34]],color,servo,.45);box(8,3,8,'#303c33',[35,27,-38],servo);
 const servoTies=mesh(g.servoTies,'#37483a',head);
 const gateRoot=new T.Group(),hornRoot=new T.Group(),gateTiesRoot=new T.Group();head.add(gateRoot,hornRoot,gateTiesRoot);
 const gate=mesh(g.gate,'#d5b25c',gateRoot),horn=mesh(g.horn,'#f4efd8',hornRoot);mesh(g.ties,'#3c4b3d',gateTiesRoot);
 const screw=new T.Group();hornRoot.add(screw);cylinder(.9,5,'#969f96',[0,-4.7,0],screw);cylinder(2,.8,'#7b847b',[0,-6.9,0],screw);
 const lid=mesh(g.lid,'#dabb79');lid.rotation.x=Math.PI;
 const clips=[mesh(g.front,'#a78350'),mesh(g.rear,'#a78350')];
 const inventory=new T.Group();scene.add(inventory);box(256,1,256,'#d5ddcb',[0,-.5,0],inventory);
 const inventoryItems=[mesh(g.hopper,'#d18865',inventory),mesh(g.gate,'#d5b25c',inventory),...packingGeo.map(pg=>mesh(pg,'#88a990',inventory)),mesh(g.spacer,'#c58458',inventory)];
 [[62,65],[205,65],[40,150],[90,150],[140,150],[195,150]].forEach(([x,y],i)=>inventoryItems[i].position.set(x-128,.1,128-y));
 const optional=new T.Group();scene.add(optional);packingGeo.forEach((pg,i)=>{const m=mesh(pg,'#88a990',optional);m.position.set(103,207,-35+i*35);});const gapStrip=mesh(g.spacer,'#c58458',optional);gapStrip.position.set(95,207,65);
 const motor=new T.Group();head.add(motor);box(23,21,1.6,'#315b42',[0,0,0],motor);const coin=cylinder(5,3.4,'#aab5aa',[0,0,2.5],motor);coin.rotation.x=Math.PI/2;box(10,3,3,'#293e30',[0,-8,3],motor);
 const electronics=new T.Group();scene.add(electronics);
 const breadboard=new T.Group(),esp=new T.Group();electronics.add(breadboard,esp);
 box(82,55,8,'#f1eee2',[0,0,0],breadboard);box(76,2,.5,'#c3cdb9',[0,0,4.1],breadboard);
 const holes=new T.InstancedMesh(new T.SphereGeometry(.5,5,4),material('#77846e'),300);breadboard.add(holes);let n=0;const matrix=new T.Matrix4();for(let row=0;row<30;row++)for(const side of [-1,1])for(let j=0;j<5;j++){matrix.makeTranslation(-36.8+row*2.54,side*(4+j*2.54),4.2);holes.setMatrixAt(n++,matrix);}
 box(52,29,1.7,'#274334',[0,0,0],esp);box(18,17,2,'#b7c0b2',[9,1,-2],esp);box(7.5,8,3.5,'#b5c0b3',[-27,0,-1],esp);
 const power=new T.Group();scene.add(power);box(11,4.5,12,'#b7c0b9',[-14.5,0,0],power);box(20,9,18,'#303c35',[0,0,0],power);box(14,10,24,'#70a287',[17,0,0],power);
 for(const z of [-7.5,-2.5,2.5,7.5])cylinder(1.7,.6,'#b4bdb6',[17,5.25,z],power);
 const brick=new T.Group();scene.add(brick);box(...powerLayout.brickSize,'#f1eee1',powerLayout.brickCenter,brick);box(.6,8,15,'#29382e',powerLayout.portCenter,brick);
 const scale=new T.Group();scene.add(scale);box(105,17,125,'#37473a',[0,8.5,0],scale);box(101,1,96,'#b6c0b1',[0,16.5,-12],scale);box(46,.6,14,'#5b88a7',[0,17.3,48],scale);
 const cup=new T.Group();scene.add(cup);const wall=mesh(new T.CylinderGeometry(30,30,78.5,64,1,true),'#bdcbb1',cup);wall.position.y=57.75;const inner=mesh(new T.CylinderGeometry(28.5,28.5,78.5,64,1,true),'#bdcbb1',cup);inner.material.side=T.BackSide;inner.position.y=57.75;cylinder(30,1.5,'#bdcbb1',[0,17.75,0],cup);
 const wires=new T.Group();scene.add(wires);const wireSets=[];
 function wire(id,stage,points,color,headIndices=[]){const m=line(points,color,wires);m.name=id;wireSets.push({m,stage,points,color,headIndices,lastOffset:null});}
 powerLayout.routes.forEach((r,i)=>wire(i?'W02':'W01',5,r.points,r.color));
 wire('W03',6,[[-122,48,-15],[-140,15,-90],[145,12,-90],[123,70,0]],'#33433c');
 wire('W04',6,[[-122,55,-10],[-145,35,-65],[135,20,-65],[123,65,10]],'#c39b3c');
 wire('W05',6,[[-122,55,5],[-145,35,80],[138,20,80],[123,65,20]],'#437ea8');
 for(const [j,color]of ['#b94a3f','#33433c','#c39b3c'].entries())wire('W0'+(6+j),7,[[33+j*2,213.3,-42],[85,218,-50-j*3],[142,230,60+j*3],[143,110,50+j*3],[123,70,10+j*3]],color,[0,1]);
 wire('U1',8,[[-117,50,31],[-146,45,80],[-175,4,100],[-230,3,130]],'#717a71');
 for(const[j,color]of ['#b94a3f','#33433c','#437ea8'].entries())wire('W'+String(9+j).padStart(2,'0'),14,[[j*3,205,26],[55,228,44+j*3],[129,197,59+j*3],[142,125,55+j*3],[123,70,-10+j*3]],color,[0,1]);
 const labelData=[
  ['08 · new hopper',()=>new T.Vector3(-66,60,63),i=>i===0],['09 · new gate',()=>new T.Vector3(77,10,63),i=>i===0],
  ['0.4 / 0.8 / 1.6 mm · optional packing',()=>new T.Vector3(-38,8,-22),i=>i===0],['0.6 mm · removable aid',()=>new T.Vector3(77,8,-22),i=>i===0],
  ['SG90 · boss + shaft through opening',()=>new T.Vector3(35,head.position.y+28,0),i=>i===2||i===9],
  ['Original-height ears · no added shims',()=>new T.Vector3(35,head.position.y+7,15),i=>i===2],
  ['Horn fitted to shaft FIRST',()=>new T.Vector3(35,head.position.y-9,0),i=>i===10],
  ['New gate rises around seated horn',()=>new T.Vector3(65,head.position.y-8,20),i=>i===11],
  ['Optional pieces · none installed in reference',()=>new T.Vector3(108,215,40),i=>i===11],
  ['Retained printed locking clips',()=>new T.Vector3(-25,194,52),i=>i===13],
  ['ESP32 + breadboard · outside walls',()=>new T.Vector3(122,83,0),i=>i===4],
 ];
 const labels=labelData.map(([text])=>{const el=document.createElement('div');el.className='callout';el.textContent=text;document.querySelector('#callouts').append(el);return el;});
 let stage=-1,manual=false;orbit.addEventListener('start',()=>manual=true);const smooth=t=>t*t*(3-2*t);
 function setCamera(i){manual=false;const close=[2,3,9,10,11].includes(i);const position=i===0?[310,330,370]:i===10?[130,190,145]:i===11?[170,282,172]:close?[170,295,230]:i===4?[380,140,220]:i===13?[260,260,305]:[365,280,430];const target=i===0?[0,12,0]:close?[30,221,0]:i===4?[20,65,0]:[10,120,0];camera.position.set(...position);orbit.target.set(...target);orbit.update();}
 function update(i,p,time){
  if(i!==stage){stage=i;setCamera(i);}const e=smooth(Math.min(1,p*2)),join=smooth(Math.min(1,p/.65));
  inventory.visible=i===0;cradle.visible=i>0&&i!==10&&i!==11;head.visible=i>=2;
  head.position.set(0,i<12?218.3:i===12?218.3-32*e:186.3,0);
  servo.position.y=i===2?45*(1-e):0;servoTies.visible=i>=2&&(i!==2||p>.4);
  motor.visible=i>=3;motor.position.set(0,28,23+(i===3?40*(1-e):0));motor.rotation.x=.396;
  hopper.material.transparent=i===10||i===11;hopper.material.opacity=hopper.material.transparent?.18:1;hopper.material.depthWrite=!hopper.material.transparent;
  gateRoot.visible=i>=11;gateRoot.position.set(35,-7.9-(i===11?45*(1-join):0),0);hornRoot.visible=i>=10;hornRoot.position.set(35,i===10?-30*(1-e):0,0);
  gateTiesRoot.visible=i>11||(i===11&&p>.65);gateTiesRoot.position.set(35,0,0);screw.visible=i>10||(i===10&&p>.55);
  const angle=i===16?Math.PI/3*(1-(p>.2&&p<.6?smooth(Math.min((p-.2)/.12,(.6-p)/.12,1)):0)):Math.PI/3;
  for(const root of [gateRoot,hornRoot,gateTiesRoot])root.rotation.y=angle;
  optional.visible=i===11;clips.forEach((c,n)=>{c.visible=i>=13;c.position.z=i===13?(n?-1:1)*30*(1-e):0;});
  lid.visible=i>=15;lid.position.set(0,246.7+(i===15?45*(1-e):0),0);
  electronics.visible=i>=4;breadboard.rotation.y=esp.rotation.y=Math.PI/2;breadboard.position.set(116+(i===4?50*(1-e):0),50,0);esp.position.set(-116-(i===4?50*(1-e):0),50,0);
  power.visible=brick.visible=i>=5;power.position.set(...powerLayout.adapterOrigin);
  scale.visible=i>=12;cup.visible=i>=12;wires.visible=i>=5&&i!==10&&i!==11;wireSets.forEach(w=>{const{m,stage:s}=w;m.visible=i>=s;const offset=head.position.y-186.3;if(w.headIndices.length&&w.lastOffset!==offset){const points=w.points.map((p,n)=>new T.Vector3(p[0],p[1]+(w.headIndices.includes(n)?offset:0),p[2]));m.geometry.dispose();m.geometry=new T.TubeGeometry(new T.CatmullRomCurve3(points),45,.6,6,false);w.lastOffset=offset;}const count=m.geometry.index.count;m.geometry.setDrawRange(0,i===s?Math.floor(count*e/3)*3:count);});
  labelData.forEach(([,point,visible],n)=>{const v=point().project(camera);labels[n].hidden=!visible(i)||Math.abs(v.x)>.95||Math.abs(v.y)>.95||v.z>1;if(!labels[n].hidden){labels[n].style.left=(v.x*.5+.5)*host.clientWidth+'px';labels[n].style.top=(-v.y*.5+.5)*host.clientHeight+'px';}});
  orbit.update();renderer.render(scene,camera);
 }
 new ResizeObserver(()=>{const{width,height}=host.getBoundingClientRect();renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix();}).observe(host);
 return{renderer,update,reset:()=>setCamera(stage),scene,camera,geometryVersion:'V3.2',loadedPaths,wireIDs:wireSets.map(w=>w.m.name),components:{gate,horn,servo,head,gateRoot,hornRoot,inventory},manual};
}
