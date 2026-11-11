"""Single-source wiring netlist, SVG diagrams and assembly connection table.
Header order is deliberately logical: exact purchased board layouts unverified.
"""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'public/hardware/wiring';OUT.mkdir(exist_ok=True)
wires=[
 {'id':'W01','from':'USB-A adapter +5V / VCC / VBUS','to':'A1','net':'5V','type':'M–M / solid ended','color':'#bb493d','note':'Brick unplugged. Clamp one solid-ended lead in the terminal explicitly marked +5V, VCC or VBUS; male breadboard end into A1. Leave D+ and D− empty.'},
 {'id':'W02','from':'USB-A adapter GND / −','to':'A3','net':'GND','type':'M–M / solid ended','color':'#374b43','note':'Use the terminal explicitly marked GND. D− is a data terminal, not ground. Male breadboard end into A3.'},
 {'id':'W03','from':'ESP32 GND','to':'B3','net':'GND','type':'F–M','color':'#374b43','note':'Female jumper socket over a male header pin labelled GND. Male end into B3. This joins computer-powered ESP32 ground to external supply ground.'},
 {'id':'W04','from':'ESP32 GPIO18 / IO18 / D18','to':'A5','net':'SERVO','type':'F–M','color':'#b47b17','note':'Find the header label 18, IO18 or D18. This means GPIO18, not the eighteenth header pin. Female on the ESP32 header; male into A5.'},
 {'id':'W05','from':'ESP32 GPIO19 / IO19 / D19','to':'A7','net':'MOTOR','type':'F–M','color':'#397ab2','note':'Female on the ESP32 pin labelled 19 / IO19 / D19; male into A7. Keep the module IN lead (W11) disconnected until the actual module input circuit is verified.'},
 {'id':'W06','from':'SG90 red lead, female servo socket','to':'B1','net':'5V','type':'M–M','color':'#bb493d','note':'Insert one male jumper pin into the servo socket cavity attached to its red wire; other male end into B1. Do not cut the servo cable.'},
 {'id':'W07','from':'SG90 brown / black lead, female servo socket','to':'C3','net':'GND','type':'M–M','color':'#374b43','note':'Male jumper into the servo socket cavity attached to brown/black; other male end into C3. Keep the three inserted pins insulated and seated.'},
 {'id':'W08','from':'SG90 orange / yellow lead, female servo socket','to':'B5','net':'SERVO','type':'M–M','color':'#b47b17','note':'Male jumper into the servo socket cavity attached to orange/yellow; other male into B5. A5 and B5 share one strip, completing GPIO18 → servo signal.'},
 {'id':'W09','from':'Vibration module VCC / +','to':'C1','net':'5V','type':'F–M','color':'#bb493d','note':'Read the module label; its header order may differ from the diagram. Female on VCC / +; male into C1. This is a driver module, not a bare motor. For initial servo-only testing leave W09 unplugged so an unverified floating IN cannot start the motor.'},
 {'id':'W10','from':'Vibration module GND / −','to':'D3','net':'GND','type':'F–M','color':'#374b43','note':'Female jumper on the module header labelled GND / −; male end into D3.'},
 {'id':'W11','from':'Vibration module IN / S / signal','to':'B7','net':'MOTOR','type':'F–M','color':'#397ab2','conditional':True,'note':'LEAVE DISCONNECTED until the actual module accepts 3.3V control with its 5V supply, without exposing GPIO19 to 5V. A low IN voltage reading alone does not prove compatibility. If verified, power off, place female on IN / S and male into B7. A7 and B7 complete the GPIO19 PWM path.'}]
# Actual five-hole terminal strips, not the possibly split long edge rails.
expected={1:'5V',3:'GND',5:'SERVO',7:'MOTOR'}
assert len({w['to'] for w in wires})==len(wires)
assert all(w['to'][0] in 'ABCDE' and expected[int(w['to'][1:])]==w['net'] for w in wires)
assert sum(w['type']=='F–M' for w in wires)==6
assert sum(w['type'].startswith('M–M') for w in wires)==5
fw=(ROOT/'firmware/main.py').read_text(encoding='utf-8')
assert 'PWM(Pin(18)' in fw and 'PWM(Pin(19,' in fw
assert {w['id'] for w in wires if w['net']=='GND'}=={'W02','W03','W07','W10'}
assert {w['id'] for w in wires if w['net']=='5V'}=={'W01','W06','W09'}
(OUT/'wires.json').write_text(json.dumps({'wires':wires,'groups':{'A1–E1':'+5V only','A3–E3':'Common GND','A5–E5':'GPIO18 ↔ servo signal','A7–E7':'GPIO19 ↔ module IN, conditional'},'board':'400 point solderless board; use the A–E side only. First 8 rows shown. Verify actual strip continuity before power. Long edge rails unused.','header_positions_verified':False},indent=2),encoding='utf-8')
colors={'5V':'#bb493d','GND':'#374b43','SERVO':'#b47b17','MOTOR':'#397ab2'}
def start(w,h,title,sub):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(title)}"><style>text{{font:17px system-ui,sans-serif;fill:#293f34}}.title{{font-size:28px;font-weight:650}}.small{{font-size:13px}}.pin{{font-size:15px;font-weight:600}}.id{{font-size:12px;font-weight:750}}.wire{{cursor:pointer}}.wire path{{fill:none;stroke-linecap:round;stroke-linejoin:round}}.wire.faded{{opacity:.08}}.wire.selected path.colour{{stroke-width:6}}.wire.selected text{{font-size:15px}}</style><rect width="{w}" height="{h}" fill="#f6f4ee"/><text x="30" y="40" class="title">{title}</text><text x="30" y="70" class="small">{sub}</text>'
# Overview endpoints: logical label panels, never a claim about header pin order.
a=start(1420,960,'Every jumper, end to end','Logical label panels — match the labels on your actual boards. W11 is conditional. Wire crossings are not junctions.')
a+='<rect x="520" y="110" width="330" height="650" rx="12" fill="#e9e7dd" stroke="#a4afa0"/><text x="540" y="105" class="pin">Breadboard A–E side</text>'
xs=[560,610,660,710,760];ys={1:200,3:350,5:500,7:650}
for j,c in enumerate('ABCDE'):a+=f'<text x="{xs[j]-5}" y="150">{c}</text>'
for row,net in expected.items():
 y=ys[row];co=colors[net]
 a+=f'<rect x="542" y="{y-19}" width="237" height="38" rx="14" fill="{co}" opacity=".12"/><path d="M560 {y}H760" stroke="{co}" stroke-width="10" opacity=".22"/><text x="795" y="{y+5}" class="pin">{row}</text>'
 for x in xs:a+=f'<circle cx="{x}" cy="{y}" r="7" fill="#f6f4ee" stroke="{co}" stroke-width="2"/>'
 a+=f'<text x="540" y="{y+52}" class="small">Row {row}: '+{'5V':'+5V','GND':'common ground','SERVO':'GPIO18 / servo signal','MOTOR':'GPIO19 / IN (conditional)'}[net]+'</text>'
a+='<text x="540" y="795" class="small">One row = five connected holes.</text><text x="540" y="820" class="small">Different rows stay separate.</text><text x="540" y="845" class="small">Long power rails are not used.</text>'
a+='<rect x="30" y="150" width="260" height="270" rx="12" fill="#dce5dc" stroke="#97aa99"/><text x="50" y="185" class="pin">USB-C ESP32</text><text x="50" y="210" class="small">Separate from breadboard</text>'
a+='<path d="M75 105V150" stroke="#778a7b" stroke-width="9"/><text x="40" y="100" class="small">MacBook → USB-C data cable</text>'
a+='<text x="50" y="245">GND</text><text x="50" y="295">GPIO18 / D18</text><text x="50" y="345">GPIO19 / D19</text><text x="50" y="390" class="small">External +5V does not enter</text><text x="50" y="409" class="small">ESP32 VIN / 3V3 / GPIO.</text>'
a+='<rect x="30" y="520" width="260" height="235" rx="12" fill="#e7e4d7" stroke="#ada68d"/><text x="50" y="553" class="pin">5V brick + USB-A adapter</text><rect x="48" y="565" width="63" height="43" rx="4" fill="#f6f4ee" stroke="#777"/><text x="60" y="591" class="small">USB-A</text><rect x="111" y="576" width="22" height="21" fill="#b3bbb3"/><rect x="133" y="570" width="39" height="33" fill="#4b7057"/><text x="190" y="604" class="pin">+5V</text><text x="190" y="654" class="pin">GND</text><text x="50" y="698" class="small">D+ and D− stay EMPTY.</text><text x="50" y="727" class="small">Read real terminal markings.</text>'
a+='<rect x="1100" y="150" width="280" height="260" rx="12" fill="#dce3ec" stroke="#91a4b8"/><text x="1120" y="185" class="pin">SG90 factory cable/socket</text><text x="1120" y="234">Red → +5V</text><text x="1120" y="284">Brown/black → GND</text><text x="1120" y="334">Orange/yellow → signal</text><text x="1120" y="375" class="small">Male jumper pins go into</text><text x="1120" y="397" class="small">the existing female socket.</text>'
a+='<rect x="1100" y="520" width="280" height="235" rx="12" fill="#dce5dc" stroke="#97aa99"/><text x="1120" y="556" class="pin">5V vibration driver module</text><text x="1120" y="604">VCC / +</text><text x="1120" y="654">GND / −</text><text x="1120" y="704">IN / S  *</text><text x="1120" y="735" class="small">Header order NOT verified.</text>'
paths=[[(290,600),(360,600),(360,200),(560,200)],[(290,650),(390,650),(390,350),(560,350)],[(290,240),(420,240),(420,320),(610,320),(610,350)],[(290,290),(450,290),(450,500),(560,500)],[(290,340),(480,340),(480,650),(560,650)],[(1100,230),(970,230),(970,170),(610,170),(610,200)],[(1100,280),(1000,280),(1000,380),(660,380),(660,350)],[(1100,330),(1030,330),(1030,530),(610,530),(610,500)],[(1100,600),(940,600),(940,125),(660,125),(660,200)],[(1100,650),(910,650),(910,410),(710,410),(710,350)],[(1100,700),(880,700),(880,680),(610,680),(610,650)]]
for w,points in zip(wires,paths):
 assert points[-1]==(xs['ABCDE'.index(w['to'][0])],ys[int(w['to'][1:])]),w['id']
 d='M'+' L'.join(f'{x} {y}' for x,y in points);dash=' stroke-dasharray="9 6"' if w.get('conditional') else ''
 x0,y0=points[0];xe,ye=points[-1]
 a+=f'<g class="wire" data-wire="{w["id"]}"><title>{escape(w["id"]+": "+w["from"]+" → "+w["to"])}</title><path d="{d}" stroke="#f6f4ee" stroke-width="9"/><path class="colour" d="{d}" stroke="{w["color"]}" stroke-width="3.5"{dash}/><circle cx="{xe}" cy="{ye}" r="5" fill="{w["color"]}"/><text x="{x0+(8 if x0==290 else -47)}" y="{y0-8}" class="id" fill="{w["color"]}">{w["id"]}</text><text x="{xe-12}" y="{ye-13}" class="id">{w["id"]}</text></g>'
for x,c in zip(xs,'ABCDE'):a+=f'<rect x="{x-12}" y="132" width="24" height="24" fill="#f6f4ee"/><text x="{x-5}" y="150">{c}</text>'
a+='<text x="30" y="895" class="pin">* W11: leave IN disconnected until this module’s 3.3V control input compatibility is verified.</text><text x="30" y="927" class="small">Jumpers: 6 female–male + 5 male–male. Colours are suggestions; servo factory lead colours identify its three functions.</text></svg>'
(OUT/'end_to_end.svg').write_text(a,encoding='utf-8')
# Close-up: actual five-hole pattern and unused opposite bank.
b=start(1120,920,'Breadboard: exact hole assignment','Top 8 rows of the 400-point board, viewed from the component side. Use only A–E. Verify continuity before power.')
b+='<rect x="112" y="100" width="670" height="580" rx="12" fill="#e8e6db" stroke="#9da999"/><rect x="405" y="112" width="76" height="553" fill="#cdd3c5"/><text x="410" y="713" class="small">Centre gap</text>'
xb=[160,212,264,316,368,520,572,624,676,728]
for x,c in zip(xb,'ABCDEFGHIJ'):b+=f'<text x="{x-6}" y="128" class="pin">{c}</text>'
occupied={w['to']:w for w in wires}
for row in range(1,9):
 y=175+(row-1)*64;net=expected.get(row);co=colors.get(net,'#a4aea1')
 b+=f'<text x="91" y="{y+6}">{row}</text><path d="M160 {y}H368M520 {y}H728" stroke="{co}" stroke-width="13" opacity=".18"/>'
 for x,c in zip(xb,'ABCDEFGHIJ'):
  w=occupied.get(c+str(row));color=w['color'] if w else '#6d7c6c'
  b+=f'<circle cx="{x}" cy="{y}" r="7" fill="{color if w else "#f6f4ee"}" stroke="{color}" stroke-width="2"/>'
  if w:b+=f'<text x="{x-14}" y="{y-14}" class="id">{w["id"]}</text>'
 if net:b+=f'<text x="820" y="{y+5}" class="pin">Row {row}: '+{'5V':'+5V','GND':'common GND','SERVO':'servo signal','MOTOR':'module IN *'}[net]+'</text>'
b+='<text x="30" y="735" class="small">A1–E1 connect together.</text><text x="30" y="762" class="small">A3–E3 connect together.</text><text x="30" y="789" class="small">A5–E5 connect together.</text><text x="30" y="816" class="small">A7–E7 connect together.</text><text x="580" y="735" class="small">Different rows do NOT connect.</text><text x="580" y="762" class="small">E and F do NOT connect.</text><text x="820" y="625" class="small">* W11 conditional.</text><text x="30" y="885" class="small">Edge power rails and the remaining rows are unused. If markings differ, identify the matching five-hole strips first.</text></svg>'
(OUT/'breadboard.svg').write_text(b,encoding='utf-8')
(OUT/'netlist_check.json').write_text(json.dumps({'wires':11,'female_to_male':6,'male_to_male':5,'unique_holes':True,'power_and_signal_nets_separate':True,'firmware_gpio18_servo_gpio19_motor':True,'rails_used':False,'module_IN_connection_conditional':True,'physical_wiring_tested':False},indent=2),encoding='utf-8')
print('Generated 11-wire netlist, end-to-end SVG and exact breadboard diagram.')
(ROOT/'public/hardware/wiring.svg').write_text(a,encoding='utf-8')
