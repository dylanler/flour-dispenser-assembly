"""Exercise the actual request handler with mocked device hardware on localhost."""
import ast
import asyncio
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'firmware'))


class Pin:
    OUT = 1
    def __init__(self, *args, **kwargs): pass


class PWM:
    def __init__(self, *args, **kwargs): pass
    def duty_ns(self, value): self.pulse = value
    def duty_u16(self, value): self.duty = value


class Watchdog:
    def __init__(self, **kwargs): pass
    def feed(self): pass


def load_app():
    source = ast.parse((ROOT / 'firmware/main.py').read_text())
    # Skip only the top-level hardware run/finally; test the unchanged handler.
    assert isinstance(source.body[-1], ast.Try)
    source.body.pop()
    namespace = {'__name__': 'flour_http_test'}
    with patch.dict(sys.modules, {'machine': types.SimpleNamespace(Pin=Pin, PWM=PWM, WDT=Watchdog), 'network': types.SimpleNamespace()}):
        exec(compile(source, 'firmware/main.py', 'exec'), namespace)
    return namespace


class HttpTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.app = load_app()
        self.server = await asyncio.start_server(self.app['handle'], '127.0.0.1', 0)
        self.port = self.server.sockets[0].getsockname()[1]

    async def asyncTearDown(self):
        self.server.close()
        await self.server.wait_closed()

    async def request(self, path, payload=None, raw=None):
        reader, writer = await asyncio.open_connection('127.0.0.1', self.port)
        method = 'GET' if payload is None else 'POST'
        data = b'' if payload is None else json.dumps(payload).encode()
        writer.write(raw or (('%s %s HTTP/1.0\r\nContent-Length: %d\r\n\r\n' % (method, path, len(data))).encode() + data))
        await writer.drain()
        result = await asyncio.wait_for(reader.read(), 4)
        writer.close(); await writer.wait_closed()
        head, body = result.split(b'\r\n\r\n', 1)
        return int(head.split()[1]), body

    async def test_page_and_operating_sequence(self):
        code, body = await self.request('/')
        self.assertEqual(code, 200); self.assertIn(b'Center with horn removed', body)
        code, _ = await self.request('/api/dose', {'duration_ms': 500, 'duty': 0})
        self.assertEqual(code, 400)
        await self.request('/api/arm', {})
        code, body = await self.request('/api/dose', {'duration_ms': 100, 'duty': 0})
        self.assertEqual(code, 200); self.assertTrue(json.loads(body)['dispensing'])
        await asyncio.sleep(.12)
        _, body = await self.request('/api/status')
        self.assertFalse(json.loads(body)['dispensing'])
        self.assertEqual(self.app['motor'].duty, 0)
        self.assertEqual(self.app['servo'].pulse, 1500000)

    async def test_bad_requests_do_not_change_state(self):
        for raw in [b'POST /api/config HTTP/1.0\r\nContent-Length: 513\r\n\r\n', b'POST /api/config HTTP/1.0\r\nContent-Length: 2\r\n\r\n[]', b'GET / HTTP/1.0\r\nX: '+b'a'*2050+b'\r\n\r\n']:
            code, _ = await self.request('/', raw=raw)
            self.assertEqual(code, 400)
        self.assertFalse(self.app['device'].status()['armed'])

    async def test_config_and_stop(self):
        await self.request('/api/config', dict(closed_us=1450, open_us=1100, motor_ready=True))
        await self.request('/api/arm', {})
        code, _ = await self.request('/api/dose', dict(duration_ms=5000, duty=25))
        self.assertEqual(code, 200)
        await self.request('/api/stop', {})
        self.assertEqual(self.app['motor'].duty, 0)
        self.assertEqual(self.app['servo'].pulse, 1450000)


if __name__ == '__main__': unittest.main()
