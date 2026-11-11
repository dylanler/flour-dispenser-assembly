import './style.css';
import {chapters,chapterAt,startTime,totalDuration} from './assembly-steps.js';
import {makeScene} from './scene-v32.js';
const $=s=>document.querySelector(s),base=import.meta.env.BASE_URL;
const fmt=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
const wireStages=new Set([5,6,7,14]),wireImages={};
const wireReady=Promise.all([...wireStages].map(id=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{wireImages[id]=image;resolve();};image.onerror=()=>reject(new Error('Missing current wiring diagram '+id));image.src=base+`hardware/assembly-v3-2/wiring-stage-${id}.svg`;})));
let time=0,playing=false,speed=1,current=-1,last=performance.now(),model,recorder,recordCanvas,ctx,chunks=[];
$('#duration').textContent=fmt(totalDuration);$('#total-duration').textContent=fmt(totalDuration);$('#timeline').max=totalDuration;
chapters.forEach(c=>{const li=document.createElement('li'),button=document.createElement('button');button.innerHTML=`<span>${String(c.id+1).padStart(2,'0')}</span>${c.title}`;button.onclick=()=>seek(startTime(c.id));li.append(button);$('#chapter-list').append(li);});
function seek(t){time=Math.max(0,Math.min(totalDuration,t));paint();}
function play(value){playing=value;$('#play').innerHTML=value?'Ⅱ <span>Pause</span>':'▶ <span>Play V3.2</span>';}
function paint(){
 const{chapter:c}=chapterAt(time);$('#elapsed').textContent=fmt(time);$('#timeline').value=time;if(current===c.id)return;current=c.id;
 $('#step-counter').textContent=`${String(c.id+1).padStart(2,'0')} / ${chapters.length}`;$('#step-title').textContent=c.title;$('#step-description').textContent=c.description;
 $('#step-points').replaceChildren(...c.points.map(t=>{const p=document.createElement('p');p.textContent=t;return p;}));$('#step-note').textContent=c.note;
 if(c.id===13){const a=document.createElement('a');a.href=base+'hardware/clip_detail_v3.svg';a.target='_blank';a.rel='noopener';a.textContent='View the retained clip interface ↗';a.style.display='block';$('#step-note').append(a);}
 $('#connections').replaceChildren(...c.connections.map(([from,to])=>{const tr=document.createElement('tr'),a=document.createElement('a');a.href=base+'hardware/wiring/WIRING_GUIDE.html#'+from.slice(0,3);a.target='_blank';a.rel='noopener';a.textContent=from;const td=document.createElement('td');td.append(a);const dest=document.createElement('td');dest.textContent=to;tr.append(td,dest);return tr;}));$('#connection-box').hidden=!c.connections.length;
 const wiring=wireStages.has(c.id);$('#wiring-overlay').hidden=!wiring;if(wiring){$('#wiring-figure').src=base+`hardware/assembly-v3-2/wiring-stage-${c.id}.svg`;$('#wiring-figure').alt=c.title+' — highlighted end-to-end wire paths';$('#wiring-detail').href=base+'hardware/wiring/WIRING_GUIDE.html#'+c.connections[0][0].slice(0,3);}
 $('#scene-mode').textContent=wiring?'EXACT WIRING MAP · MATCH ACTUAL LABELS':c.id===0?'CURRENT V3.2 REPAIR PLATE':c.id<10?'ASSEMBLY + SETUP':c.id<14?'HORN FIRST · THEN GATE':'EMPTY CHECKS + FIRST DOSE';
 $('#geometry-note').textContent=wiring?'Four five-hole strips · long rails unused':'Actual V3.2 print meshes · reference hardware';
 $('#chapter-list').querySelectorAll('button').forEach((b,i)=>{b.classList.toggle('active',i===c.id);b.setAttribute('aria-current',i===c.id?'step':'false');});
}
$('#timeline').oninput=e=>seek(+e.target.value);$('#play').onclick=()=>{if(time>=totalDuration)seek(0);play(!playing);};$('#previous').onclick=()=>seek(startTime(Math.max(0,current-1)));$('#next').onclick=$('#step-next').onclick=()=>seek(startTime(Math.min(chapters.length-1,current+1)));$('#speed').onchange=e=>speed=+e.target.value;$('#focus-view').onclick=()=>document.body.classList.toggle('large');
document.addEventListener('keydown',e=>{if(/INPUT|SELECT|TEXTAREA|BUTTON/.test(e.target.tagName))return;if(e.code==='Space'){e.preventDefault();play(!playing);}if(e.code==='ArrowRight')seek(time+5);if(e.code==='ArrowLeft')seek(time-5);});
function lines(text,width){const result=[];let line='';for(const word of text.split(' ')){const next=line?line+' '+word:word;if(ctx.measureText(next).width>width&&line){result.push(line);line=word;}else line=next;}if(line)result.push(line);return result;}
function drawRecording(){if(!ctx)return;const c=chapters[current],source=wireImages[current]||model.renderer.domElement;ctx.fillStyle='#eceee5';ctx.fillRect(0,0,1280,960);const sw=source.naturalWidth||source.width,sh=source.naturalHeight||source.height,scale=Math.min(1280/sw,720/sh),w=sw*scale,h=sh*scale;ctx.drawImage(source,(1280-w)/2,(720-h)/2,w,h);ctx.fillStyle='#f6f4ee';ctx.fillRect(0,720,1280,240);ctx.fillStyle='#a75d3e';ctx.font='15px sans-serif';ctx.fillText(`FLOUR / V3.2     STEP ${current+1} / 17     ${fmt(time)}`,30,746);ctx.fillStyle='#293f34';ctx.font='bold 24px sans-serif';ctx.fillText(c.title,30,780);ctx.font='16px sans-serif';lines(c.description+' '+c.points.join(' '),1220).slice(0,5).forEach((t,i)=>ctx.fillText(t,30,805+i*20));ctx.fillStyle='#97623c';ctx.font='12px sans-serif';lines(c.note,1220).slice(0,2).forEach((t,i)=>ctx.fillText(t,30,918+i*15));ctx.fillText('Actual V3.2 print geometry · horn/socket assumptions and electronics illustrative · physically untested',30,952);}
async function record(){
 if(recorder?.state==='recording'){recorder.stop();return;}await wireReady;
 if(!window.MediaRecorder||!HTMLCanvasElement.prototype.captureStream){$('#record-status').hidden=false;$('#record-status').textContent='Video export needs Chrome/Edge with MediaRecorder.';return;}
 recordCanvas=document.createElement('canvas');recordCanvas.width=1280;recordCanvas.height=960;ctx=recordCanvas.getContext('2d');seek(0);drawRecording();chunks=[];
 const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'].find(t=>MediaRecorder.isTypeSupported(t));recorder=new MediaRecorder(recordCanvas.captureStream(24),{mimeType:mime,videoBitsPerSecond:2200000});recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recorder.onstop=()=>{const blob=new Blob(chunks,{type:mime}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='flour-v3-2-assembly.webm';a.click();setTimeout(()=>URL.revokeObjectURL(url),60000);ctx=null;recordCanvas=null;$('#record').textContent='↓ Export V3.2 video';$('#record-status').textContent='Latest V3.2 sequence exported, including the numbered wiring maps.';};
 speed=+$('#speed').value;play(true);recorder.start(1000);$('#record').textContent='■ Finish export';$('#record-status').hidden=false;
}
$('#record').onclick=record;
try{
 [model]=await Promise.all([makeScene($('#canvas-host')),wireReady]);$('#loading').hidden=true;$('#record').disabled=false;$('#reset-view').onclick=model.reset;
 const requested=Number(new URLSearchParams(location.search).get('step'));if(Number.isInteger(requested)&&requested>=0&&requested<chapters.length)time=startTime(requested);
 paint();function frame(now){const dt=Math.min(.15,(now-last)/1000);last=now;if(playing){time=Math.min(totalDuration,time+dt*speed);if(time>=totalDuration){play(false);if(recorder?.state==='recording')recorder.stop();}}paint();const{chapter,progress}=chapterAt(time);model.update(chapter.id,progress,time);drawRecording();if(recorder?.state==='recording')$('#record-status').textContent=`Recording V3.2 ${fmt(time)} / ${fmt(totalDuration)} at ${speed}×`;requestAnimationFrame(frame);}requestAnimationFrame(frame);
 window.assembly={seek,play,record,step:(id,p=.85)=>seek(startTime(id)+chapters[id].duration*p),get time(){return time;},get model(){return model;},geometryVersion:model.geometryVersion,totalDuration};
}catch(error){$('#loading').hidden=true;$('#scene-error').hidden=false;$('#scene-error').textContent='Unable to start the current V3.2 view: '+error.message;console.error(error);}
