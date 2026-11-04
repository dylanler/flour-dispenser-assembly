import * as T from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { powerLayout } from './power-layout.js';

const colors = { cradle: '#9bbab0', hopper: '#d77857', gate: '#d8af57', lid: '#e3c79b', servo: '#365cba', pcb: '#23433d', red: '#b94a3f', black: '#33433c', signal: '#dca14d', pwm: '#437ea8' };
export async function makeScene(host) {
  const scene = new T.Scene(); scene.background = new T.Color('#eceee5');
  const camera = new T.PerspectiveCamera(35, 1, 1, 2500);
  const renderer = new T.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = T.PCFShadowMap; renderer.outputColorSpace = T.SRGBColorSpace;
  host.append(renderer.domElement);
  const orbit = new OrbitControls(camera, renderer.domElement); orbit.enableDamping = true; orbit.minDistance = 80; orbit.maxDistance = 900; orbit.maxPolarAngle = Math.PI * .85;
  scene.add(new T.HemisphereLight('#ffffff', '#9ba590', 2.8));
  const sun = new T.DirectionalLight('#fff6e3', 4); sun.position.set(-150, 300, 180); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -260, right: 260, top: 260, bottom: -260, far: 800 }); sun.shadow.bias = -.0005; scene.add(sun);
  const fill = new T.DirectionalLight('#ddeaff', 1.5); fill.position.set(200, 160, -200); scene.add(fill);
  const mat = color => new T.MeshStandardMaterial({ color, roughness: .7, metalness: .02 });
  function mesh(geo, color, parent = scene) { const m = new T.Mesh(geo, mat(color)); m.castShadow = m.receiveShadow = true; parent.add(m); return m; }
  function box(w, h, d, color, p, parent) { const m = mesh(new T.BoxGeometry(w, h, d), color, parent); m.position.set(...p); return m; }
  function cylinder(r, h, color, p, parent, r2 = r) { const m = mesh(new T.CylinderGeometry(r2, r, h, 48), color, parent); m.position.set(...p); return m; }
  function line(points, color, radius = .65, parent = scene) { const c = new T.CatmullRomCurve3(points.map(p => new T.Vector3(...p))); return mesh(new T.TubeGeometry(c, 64, radius, 6, false), color, parent); }
  const floor = box(1500, 2, 1500, '#e5e8dc', [0, -2, 0]); floor.receiveShadow = true;
  const grid = new T.GridHelper(600, 24, '#d1d8c9', '#dce1d5'); grid.position.y = -.95; scene.add(grid);
  const H = 190;
  const loader = new STLLoader(); const filenames = ['01_wide_cradle','02_hopper_with_servo_mount','03_rotary_gate','04_lid','05_locking_clip'];
  const geometries = await Promise.all(filenames.map(async name => { const g = await loader.loadAsync(`${import.meta.env.BASE_URL}hardware/stl/${name}.stl`); g.rotateX(-Math.PI / 2); g.computeVertexNormals(); return g; }));
  const cradle = mesh(geometries[0], colors.cradle);
  const head = new T.Group(); scene.add(head); const hopper = mesh(geometries[1], colors.hopper, head);
  const gateRoot = new T.Group(); head.add(gateRoot); const gate = mesh(geometries[2], colors.gate, gateRoot);
  const lid = mesh(geometries[3], colors.lid);
  const clipFront = mesh(geometries[4], '#b48b50');
  const clipRear = mesh(geometries[4], '#b48b50');
  const plate = box(256, 1, 256, '#d6dccd', [0, -.5, 0]);
  const servo = new T.Group(); head.add(servo);
  box(12.7, 22.5, 23.9, colors.servo, [35, 17.8, -5.6], servo);
  box(20.5, 2.4, 34, '#466bcc', [35, 8.2, -5.6], servo);
  cylinder(5.7, 5.8, '#4161b1', [35, 3.8, 0], servo); cylinder(2.4, 4.8, '#ece5d8', [35, -1.5, 0], servo);
  const servoTies = new T.Group(); servo.add(servoTies);
  for (const x of [23, 47]) line([[x,-1,-12],[x,31,-12],[x,31,0],[x,-1,0],[x,-1,-12]],'#3b4840',.65,servoTies);
  const horn = new T.Group(); gateRoot.add(horn); box(29, 1.8, 6.8, '#f5f1dc', [0, 3.1, 0], horn); cylinder(3.2, 3.4, '#f5f1dc', [0,4,0],horn);
  const hornTies = new T.Group(); horn.add(hornTies);
  for(const x of [-10,10]) line([[x,1,7],[x,4.3,7],[x,4.3,-7],[x,1,-7],[x,1,7]],'#3b4840',.48,hornTies);
  const screw = new T.Group(); gateRoot.add(screw); cylinder(1,7,'#969d97',[0,-.5,0],screw); cylinder(2.4,1.3,'#7c857d',[0,-4.5,0],screw);
  const motor = new T.Group(); head.add(motor); box(23, 21, 1.6, colors.pcb, [0,0,0],motor);
  const coin = cylinder(5.2,3.4,'#b7beb9',[0,0,2.5],motor); coin.rotation.x = Math.PI / 2;
  box(10,3,3,'#262e29',[0,-8,3],motor); for(const x of [-2.5,0,2.5])box(.7,4,.7,'#d4bc7c',[x,-11,3],motor);
  const electronics = new T.Group(); scene.add(electronics);
  const breadboard = new T.Group(); electronics.add(breadboard);
  box(82,55,8,'#f4f1df',[0,0,0],breadboard);
  box(77,2,.5,'#c7c9bb',[0,0,4.1],breadboard);
  // Ten connected-terminal strips and separate supply rails are schematic, not a pin map.
  for(let row=0;row<30;row++) for(let side of [-1,1]) for(let j=0;j<5;j++)box(1.05,1.05,.6,'#7b8277',[-36.8+row*2.54,side*(4+j*2.54),4.2],breadboard);
  for(const y of [-23,-20,20,23]){box(73,.35,.4,Math.abs(y)===23?colors.red:colors.pcb,[0,y,4.3],breadboard);}
  const esp = new T.Group(); electronics.add(esp); box(52,29,1.7,'#263b35',[0,0,0],esp); box(18,17,2,'#b4beb6',[9,1,-2],esp);box(11,19,1.2,'#25312b',[22,1,-2],esp);
  box(7.5,8,3.5,'#b7bdb6',[-27,0,-1],esp);box(5.5,6,.4,'#34473f',[-31,0,-1],esp);
  for(let i=0;i<15;i++) for(const y of [-13,13])box(.6,.6,6,'#cfba75',[-18+i*2.54,y,-3.5],esp);
  const power = new T.Group(); scene.add(power);
  // User's USB-A male -> four screw terminals. Dimensions/pin order are illustrative.
  // The plug enters the brick's +X side; wires exit the adapter's opposite (+X) end.
  box(11,4.5,12,'#b7c0b9',[-14.5,0,0],power);
  box(20,9,18,'#303c35',[0,0,0],power);
  box(14,10,24,'#70a287',[17,0,0],power);
  for (const z of [-7.5,-2.5,2.5,7.5]) {
    cylinder(1.7,.6,'#b4bdb6',[17,5.25,z],power);
    box(2.1,.15,.4,'#3b4940',[17,5.6,z],power);
    const entry=cylinder(1.25,.4,'#243c2d',[24.1,-.5,z],power);entry.rotation.z=Math.PI/2;
  }
  const brick = new T.Group();scene.add(brick);box(...powerLayout.brickSize,'#f1eee1',powerLayout.brickCenter,brick);box(.6,8,15,'#29382e',powerLayout.portCenter,brick);
  const scale = new T.Group();scene.add(scale);box(105,17,125,'#343f3a',[0,8.5,0],scale);box(101,1,96,'#b6bfbb',[0,17,-12],scale);box(46,.7,14,'#457ca9',[0,17.4,48],scale);
  for(const x of [-40,40])cylinder(5,.8,'#a8b4ac',[x,17.4,48],scale);
  const cup = new T.Group(); scene.add(cup); cylinder(30,80,'#c2cbb7',[0,58,0],cup); cylinder(28,1,'#687d67',[0,98,0],cup);
  const wires = new T.Group(); scene.add(wires);
  const wireSets=[];
  function wire(stage,points,color){const m=line(points,color,.65,wires);wireSets.push({m,stage});}
  powerLayout.routes.forEach(route=>wire(5,route.points,route.color));
  wire(5,[[-122,48,-15],[-140,15,-90],[145,12,-90],[123,70,0]],colors.black);
  wire(6,[[0,195,26],[50,223,40],[125,200,55],[138,130,50],[123,73,-10]],colors.red);
  wire(6,[[3,195,26],[55,219,44],[129,197,59],[142,125,55],[123,70,-10]],colors.black);
  wire(6,[[-3,195,26],[-40,220,45],[-140,220,85],[-138,100,65],[-122,55,5]],colors.pwm);
  wire(7,[[35,204,17],[80,230,25],[140,200,60],[142,110,50],[123,73,10]],colors.red);
  wire(7,[[37,204,17],[85,227,28],[144,196,65],[145,105,55],[123,70,10]],colors.black);
  wire(7,[[39,204,17],[50,235,-5],[-145,230,-75],[-140,100,-65],[-122,55,-10]],colors.signal);
  wire(8,[[-117,50,31],[-146,45,80],[-175,4,100],[-230,3,130]],'#717a71');
  const labels = document.querySelector('#callouts');
  const labelData=[['SG90 · shaft down',[35,224,0],2,3],['VCC · GND · IN',[0,211,37],3,3],['400-point breadboard',[124,83,0],4,8],['ESP32 · USB-C',[-123,76,0],4,8],['Side USB port → adapter → two power leads',[199,42,120],5,5],['GPIO19 → IN',[-80,230,70],6,6],['GPIO18 → servo',[80,240,10],7,7],['Supplied servo horn · not printed',[35,173,0],10,11],['Front locking clip',[-25,194,52],13,14],['Rear locking clip',[85,194,-52],13,14],['105 × 125 × 17 mm · 500 g scale',[0,22,55],12,16]];
  const labelEls=labelData.map(([text])=>{const e=document.createElement('div');e.className='callout';e.textContent=text;labels.append(e);return e;});
  function resize(){ const {width,height}=host.getBoundingClientRect(); renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix(); }
  new ResizeObserver(resize).observe(host); resize();
  let stage=-1, manual=false;orbit.addEventListener('start',()=>manual=true);
  const smooth=t=>t*t*(3-2*t);
  function setCamera(i){manual=false;
    const pos=i===0?[380,480,450]:i===2||i===3?[220,320,270]:i===4?[400,160,230]:i===5?[390,180,330]:i===8?[-360,180,270]:i===10?[200,290,170]:i===11?[250,180,65]:i===13?[300,290,340]:i===16?[300,170,420]:[365,285,430];
    const target=i===0?[0,55,0]:i===2||i===3?[15,210,0]:i===4?[20,75,0]:i===5?[170,38,78]:i===8?[-80,110,0]:i===10?[35,168,0]:i===11?[35,204,0]:i===13?[25,180,0]:i===16?[0,120,40]:[0,115,0];
    camera.position.set(...pos);orbit.target.set(...target);orbit.update();}
  function update(i,p,time){
    if(i!==stage){stage=i;setCamera(i);} const e=smooth(Math.min(1,p*2));
    plate.visible=i===0; cradle.visible=i!==10&&i!==11;cradle.material.transparent=i===16;cradle.material.opacity=i===16?.2:1;cradle.material.depthWrite=i!==16;cradle.rotation.set(0,0,0);cradle.position.set(0,H,0);cradle.rotation.x=Math.PI;
    head.position.set(0,H-3.7,0);head.rotation.set(0,0,0);gateRoot.position.set(35,-6.1,0);gateRoot.rotation.set(0,Math.PI/3,0);lid.rotation.set(Math.PI,0,0);lid.position.set(0,H+56.7,0);
    clipFront.rotation.set(0,0,Math.PI/2);clipFront.position.set(-21,H-13.6,58.6+(i===13?25*(1-e):0));
    clipRear.rotation.set(0,Math.PI,Math.PI/2);clipRear.position.set(81,H-13.6,-58.6-(i===13?25*(1-e):0));
    clipFront.visible=clipRear.visible=i===0||i>=13;
    if(i===0){cradle.rotation.x=0;cradle.position.set(-12,0,54);head.position.set(-87,0,-72);gateRoot.position.set(110,-.01,126);gateRoot.rotation.y=0;lid.rotation.x=0;lid.position.set(83,0,-72);clipFront.rotation.set(0,0,0);clipFront.position.set(-103,0,93);clipRear.rotation.set(0,0,0);clipRear.position.set(-80,0,93);}
    if(i===1){cradle.rotation.x=Math.PI*e;cradle.position.y=H*e;head.position.set(0,260,-155);lid.position.set(100,2,-140);}
    if(i>1&&i<12)head.position.y=H+20;
    if(i===12)head.position.y=H+20-23.7*e;
    hopper.visible=i!==10;servo.visible=i>=2&&i!==10;servoTies.visible=i>=2;servo.position.set(0,i===2?45*(1-e):0,0);
    motor.visible=i>=3&&i!==10;motor.position.set(0,20,21+(i===3?45*(1-e):0));motor.rotation.x=.396;
    electronics.visible=i>=4&&i!==10&&i!==11;breadboard.position.set(116+(i===4?55*(1-e):0),50,0);breadboard.rotation.y=Math.PI/2;esp.position.set(-116-(i===4?55*(1-e):0),50,0);esp.rotation.y=Math.PI/2;
    power.visible=i>=5;brick.visible=i>=5;power.position.set(...powerLayout.adapterOrigin);power.rotation.x=0;
    wires.visible=i>=5&&i!==10&&i!==11;wireSets.forEach(({m,stage:s})=>{m.visible=i>=s;const count=m.geometry.index.count;m.geometry.setDrawRange(0,i===s?Math.floor(count*e/3)*3:count);});
    gate.visible=i===0||i>=10;horn.visible=i>=10;hornTies.visible=i>=10;screw.visible=i>=11;
    if(i===10){gateRoot.position.set(35,-42,55*(1-e));horn.position.y=16*(1-e);}
    else horn.position.y=0;
    if(i===11){gateRoot.position.y=-42+35.9*e;screw.position.y=-20*(1-e);}else screw.position.y=0;
    lid.visible=i===0||i===1||i>=15;if(i===15)lid.position.y+=50*(1-e);
    scale.visible=i>=1&&i!==10&&i!==11;cup.visible=i>=12;cup.position.set(0,0,0);
    if(i===16){const phase=p<.2?0:p<.3?smooth((p-.2)/.1):p<.5?1:p<.6?1-smooth((p-.5)/.1):0;gateRoot.rotation.y=Math.PI/3*(1-phase);if(phase>.95)head.position.x=Math.sin(time*85)*.12;if(p>.8){const pickup=smooth((p-.8)/.2);cup.position.set(0,15*Math.min(1,pickup*5),145*pickup);}}
    labelData.forEach(([,pt,start,end],n)=>{const el=labelEls[n];el.hidden=i<start||i>end; if(!el.hidden){const v=new T.Vector3(...pt).project(camera);el.style.left=`${(v.x*.5+.5)*host.clientWidth}px`;el.style.top=`${(-v.y*.5+.5)*host.clientHeight}px`;}});
    if(!manual&&i===0)camera.position.x=380+Math.sin(time*.08)*12;
    orbit.update();renderer.render(scene,camera);
  }
  return {renderer, update, reset:()=>setCamera(stage), scene, camera};
}
