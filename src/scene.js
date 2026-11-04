import * as T from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';

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
  const loader = new STLLoader(); const filenames = ['01_drop_in_cradle','02_hopper_with_servo_mount','03_rotary_gate','04_lid'];
  const geometries = await Promise.all(filenames.map(async name => { const g = await loader.loadAsync(`${import.meta.env.BASE_URL}hardware/stl/${name}.stl`); g.rotateX(-Math.PI / 2); g.computeVertexNormals(); return g; }));
  const cradle = mesh(geometries[0], colors.cradle);
  const head = new T.Group(); scene.add(head); const hopper = mesh(geometries[1], colors.hopper, head);
  const gateRoot = new T.Group(); head.add(gateRoot); const gate = mesh(geometries[2], colors.gate, gateRoot);
  const lid = mesh(geometries[3], colors.lid);
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
  // USB-A plug and a cut power lead. The two enlarged sleeves depict insulated splices.
  box(12,7,4,'#b7c0b9',[-13,0,0],power);box(10,11,7,'#3f4941',[-4,0,0],power);
  line([[0,0,0],[5,0,0],[10,3,0],[18,5,0]],colors.red,.7,power);
  line([[0,0,0],[5,0,0],[10,-3,0],[18,-5,0]],colors.black,.7,power);
  box(8,2.4,2.4,'#a8493f',[13,5,0],power);box(8,2.4,2.4,'#35453d',[13,-5,0],power);
  const brick = new T.Group();scene.add(brick);box(45,28,36,'#f1eee1',[74,15,80],brick);box(.8,8,15,'#3b4940',[96.6,8,80],brick);
  const bands = new T.Group(); scene.add(bands);
  for(const x of [-25,85]) {
    const pts=[[x,1,59],[x,94,59],[x,94,-59],[x,1,-59],[x,1,59]];
    line(pts,'#b58d53',1.3,bands); for(const z of [-49,49])box(8,2,10,'#dfcfae',[x,92.5,z],bands);
  }
  const cup = new T.Group(); scene.add(cup); cylinder(21,30,'#c2cbb7',[0,16,0],cup); cylinder(19,1,'#687d67',[0,31,0],cup);
  const wires = new T.Group(); scene.add(wires);
  const wireSets=[];
  function wire(stage,points,color){const m=line(points,color,.65,wires);wireSets.push({m,stage});}
  wire(5,[[110,8,80],[90,5,94],[67,40,72],[56,61,64]],colors.red);
  wire(5,[[110,8,74],[90,5,87],[63,30,72],[56,58,64]],colors.black);
  wire(5,[[15,45,-65],[-44,23,-65],[-48,24,70],[0,20,64]],colors.black);
  wire(6,[[0,97,26],[-37,110,45],[-42,65,77],[38,61,64]],colors.red);
  wire(6,[[3,97,26],[-32,108,45],[-37,57,73],[38,58,64]],colors.black);
  wire(6,[[-3,97,26],[-48,120,41],[-51,55,-78],[30,45,-65]],colors.pwm);
  wire(7,[[35,106,17],[63,119,18],[95,100,70],[92,62,75],[25,61,64]],colors.red);
  wire(7,[[37,106,17],[66,117,19],[99,97,70],[96,59,75],[25,58,64]],colors.black);
  wire(7,[[39,106,17],[70,115,20],[105,100,67],[108,48,-75],[35,45,-65]],colors.signal);
  wire(8,[[54,40,-64],[110,38,-90],[125,5,-130],[190,3,-160]],'#717a71');
  const labels = document.querySelector('#callouts');
  const labelData=[['SG90 · shaft down',[35,126,0],2,3],['VCC · GND · IN',[0,113,37],3,3],['400-point breadboard',[27,32,70],4,8],['ESP32 · USB-C',[27,70,-65],4,8],['USB-A brick · cut cable · insulated joints',[100,35,85],5,7],['GPIO19 → IN',[0,120,40],6,6],['GPIO18 → servo',[70,124,10],7,7],['Horn + two ties',[35,70,0],10,11],['Both bands required',[85,95,55],13,14]];
  const labelEls=labelData.map(([text])=>{const e=document.createElement('div');e.className='callout';e.textContent=text;labels.append(e);return e;});
  function resize(){ const {width,height}=host.getBoundingClientRect(); renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix(); }
  new ResizeObserver(resize).observe(host); resize();
  let stage=-1, manual=false;orbit.addEventListener('start',()=>manual=true);
  const smooth=t=>t*t*(3-2*t);
  function setCamera(i){manual=false;const rear = i===4 || i===8 || i===14;
    // Look through the cradle's open end for the horn and moving gate.
    camera.position.set(...(i===0?[330,410,390]:i===10?[200,195,150]:i===11?[240,80,35]:i===16?[310,55,60]:rear?[250,175,-320]:[255,210,310]));orbit.target.set(...(i===0?[0,12,0]:i===10?[35,70,0]:i===11?[35,105,0]:i===16?[25,75,0]:[20,68,0]));orbit.update();}
  function update(i,p,time){
    if(i!==stage){stage=i;setCamera(i);} const e=smooth(Math.min(1,p*2));
    plate.visible=i===0; cradle.visible=i!==10&&i!==11;cradle.material.transparent=i===16;cradle.material.opacity=i===16?.2:1;cradle.material.depthWrite=i!==16;cradle.rotation.set(0,0,0);cradle.position.set(0,92,0);cradle.rotation.x=Math.PI;
    head.position.set(0,88.3,0);head.rotation.set(0,0,0);gateRoot.position.set(35,-6.1,0);gateRoot.rotation.set(0,Math.PI/3,0);lid.rotation.set(Math.PI,0,0);lid.position.set(0,148.7,0);
    if(i===0){cradle.rotation.x=0;cradle.position.set(-74,0,59);head.position.set(-63,0,-62);gateRoot.position.set(138,-.01,125);gateRoot.rotation.y=0;lid.rotation.x=0;lid.position.set(76,0,-30);}
    if(i===1){cradle.rotation.x=Math.PI*e;cradle.position.y=92*e;head.position.set(0,180,-155);lid.position.set(100,2,-140);}
    if(i>1&&i<12)head.position.y=112;
    if(i===12)head.position.y=112-23.7*e;
    hopper.visible=i!==10;servo.visible=i>=2&&i!==10;servoTies.visible=i>=2;servo.position.set(0,i===2?45*(1-e):0,0);
    motor.visible=i>=3&&i!==10;motor.position.set(0,20,21+(i===3?45*(1-e):0));motor.rotation.x=.396;
    electronics.visible=i>=4&&i!==10&&i!==11;breadboard.position.set(27,40,59+(i===4?55*(1-e):0));esp.position.set(27,40,-61-(i===4?55*(1-e):0));
    power.visible=i>=5;brick.visible=i>=5;power.position.set(110,8,80);power.rotation.x=0;
    wires.visible=i>=5&&i!==10&&i!==11;wireSets.forEach(({m,stage:s})=>{m.visible=i>=s;const count=m.geometry.index.count;m.geometry.setDrawRange(0,i===s?Math.floor(count*e/3)*3:count);});
    gate.visible=i===0||i>=10;horn.visible=i>=10;hornTies.visible=i>=10;screw.visible=i>=11;
    if(i===10){gateRoot.position.set(35,-42,55*(1-e));horn.position.y=16*(1-e);}
    else horn.position.y=0;
    if(i===11){gateRoot.position.y=-42+35.9*e;screw.position.y=-20*(1-e);}else screw.position.y=0;
    bands.visible=i>=13;bands.scale.y=i===13?.5+.5*e:1;
    lid.visible=i===0||i===1||i>=15;if(i===15)lid.position.y+=50*(1-e);
    cup.visible=i>=12;
    if(i===16){const phase=p<.25?0:p<.35?smooth((p-.25)/.1):p<.65?1:p<.75?1-smooth((p-.65)/.1):0;gateRoot.rotation.y=Math.PI/3*(1-phase);if(phase>.95)head.position.x=Math.sin(time*85)*.12;}
    labelData.forEach(([,pt,start,end],n)=>{const el=labelEls[n];el.hidden=i<start||i>end; if(!el.hidden){const v=new T.Vector3(...pt).project(camera);el.style.left=`${(v.x*.5+.5)*host.clientWidth}px`;el.style.top=`${(-v.y*.5+.5)*host.clientHeight}px`;}});
    if(!manual&&i===0)camera.position.x=330+Math.sin(time*.08)*12;
    orbit.update();renderer.render(scene,camera);
  }
  return {renderer, update, reset:()=>setCamera(stage), scene, camera};
}
