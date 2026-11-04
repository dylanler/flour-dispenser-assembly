"""Classic ESP32 / MicroPython. Local Wi-Fi control; no Arduino IDE required."""
import asyncio
import json
import network
from machine import Pin, PWM, WDT
from controller import Controller

# Motor is held low before network setup. Servo seeks nominal closed on boot.
motor = PWM(Pin(19, Pin.OUT, value=0), freq=200, duty_u16=0)
servo = PWM(Pin(18), freq=50, duty_ns=1500000)
device = Controller(servo, motor)
watchdog = WDT(timeout=8000)

PAGE = """<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flour prototype</title>
<style>body{font:16px system-ui;max-width:620px;margin:30px auto;padding:20px;background:#f5f3ed;color:#263d32}button,input{font:inherit;margin:5px;padding:12px}button{cursor:pointer}#stop{background:#b8422b;color:white}label{display:block;margin:12px 0}pre{white-space:pre-wrap}</style>
<h1>Flour / V2</h1><p>Physically untested prototype. Keep fingers and cables clear. Stop is software control, not a power disconnect.</p>
<button onclick="send('/api/arm')">Arm for 60 seconds</button><button id="stop" onclick="send('/api/stop')">STOP + CLOSE</button>
<label>Dose milliseconds <input id="ms" type="number" value="500" min="100" max="5000"></label>
<label>Vibration % <input id="duty" type="number" value="0" min="0" max="100"></label>
<button onclick="send('/api/dose',{duration_ms:+ms.value,duty:+duty.value})">Run timed dose</button>
<details><summary>Assembly and calibration</summary><p>Center with the horn removed. Disconnect external power before installing the horn.</p>
<button onclick="send('/api/center')">Center with horn removed</button>
<label>Closed pulse, microseconds <input id="closed" type="number" value="1500" min="700" max="2300"></label>
<label>Open pulse, microseconds <input id="opened" type="number" value="1000" min="700" max="2300"></label>
<button onclick="send('/api/calibrate',{pulse_us:+document.getElementById('closed').value})">Test closed pulse</button><button onclick="send('/api/calibrate',{pulse_us:+document.getElementById('opened').value})">Test open pulse</button>
<label><input id="ready" type="checkbox">I checked the module accepts 3.3V control with its 5V supply, with no incompatible voltage on IN.</label>
<button onclick="send('/api/config',{closed_us:+document.getElementById('closed').value,open_us:+document.getElementById('opened').value,motor_ready:document.getElementById('ready').checked})">Apply for this boot</button>
<p>Settings reset on reboot. Add these checks to your startup procedure. Calibration can move the gate; adjust in small increments.</p></details><pre id="status">Connecting...</pre>
<script>const statusBox=document.getElementById('status');async function send(path,data={}){try{const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});statusBox.textContent=JSON.stringify(await r.json(),null,2)}catch(e){statusBox.textContent=e.message}}setInterval(async()=>{try{const r=await fetch('/api/status');if(r.ok)document.title=(await r.json()).dispensing?'Dispensing...':'Flour prototype'}catch(e){}},1000);fetch('/api/status').then(r=>r.json()).then(s=>statusBox.textContent=JSON.stringify(s,null,2));</script></html>"""


def dispatch(path, data):
    if path == '/api/stop': device.stop()
    elif path == '/api/arm': device.arm()
    elif path == '/api/center': device.center()
    elif path == '/api/calibrate': device.calibrate(data.get('pulse_us'))
    elif path == '/api/config': device.configure(**data)
    elif path == '/api/dose': device.dose(data.get('duration_ms'), data.get('duty'))
    else: raise ValueError('Unknown command')
    return device.status()


async def read_header(reader):
    # MicroPython Stream supports readexactly/readline, not CPython readuntil.
    header = bytearray()
    while len(header) < 2048:
        header.extend(await reader.readexactly(1))
        if header[-4:] == b'\r\n\r\n': return header
    raise ValueError('Headers too large')


async def handle(reader, writer):
    code, content_type, body = '200 OK', 'application/json', ''
    try:
        header = await asyncio.wait_for(read_header(reader), 2)
        first, *headers = header.decode().split('\r\n')
        method, path, _ = first.split(' ')
        length = 0
        for h in headers:
            if h.lower().startswith('content-length:'): length = int(h.split(':', 1)[1])
        if not 0 <= length <= 512: raise ValueError('Body too large')
        if method == 'GET' and path == '/':
            body, content_type = PAGE, 'text/html; charset=utf-8'
        elif method == 'GET' and path == '/api/status': body = json.dumps(device.status())
        elif method == 'POST' and path.startswith('/api/'):
            raw = await asyncio.wait_for(reader.readexactly(length), 2)
            data = json.loads(raw or b'{}')
            if not isinstance(data, dict): raise ValueError('Expected a JSON object')
            body = json.dumps(dispatch(path, data))
        else: code, body = '404 Not Found', json.dumps({'error': 'Not found'})
    except Exception as error:
        code, body = '400 Bad Request', json.dumps({'error': str(error)})
    try:
        data = body.encode()
        writer.write(('HTTP/1.0 %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\nCache-Control: no-store\r\n\r\n' % (code, content_type, len(data))).encode() + data)
        await asyncio.wait_for(writer.drain(), 2)
    except Exception: pass
    finally:
        writer.close()
        try: await writer.wait_closed()
        except Exception: pass


async def supervise():
    while True:
        device.tick()
        watchdog.feed()
        await asyncio.sleep_ms(10)


async def run():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='FlourProto', password='FlourTest26', authmode=network.AUTH_WPA_WPA2_PSK)
    print('FlourProto / FlourTest26. Open http://' + ap.ifconfig()[0])
    server = await asyncio.start_server(handle, '0.0.0.0', 80)
    await supervise()

try: asyncio.run(run())
finally: device.stop()
