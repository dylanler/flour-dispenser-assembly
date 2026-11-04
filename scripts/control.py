"""Wi-Fi control using only the Python standard library."""
import argparse
import json
import urllib.request
import urllib.error


def main():
    p = argparse.ArgumentParser(description='Connect your computer to FlourProto Wi-Fi first')
    p.add_argument('command', choices=['status', 'arm', 'stop', 'center', 'dose', 'config', 'calibrate'])
    p.add_argument('--host', default='192.168.4.1')
    p.add_argument('--ms', type=int, default=500)
    p.add_argument('--duty', type=int, default=0)
    p.add_argument('--closed-us', type=int, default=1500)
    p.add_argument('--open-us', type=int, default=1000)
    p.add_argument('--pulse-us', type=int, default=1500)
    p.add_argument('--motor-verified', action='store_true')
    a = p.parse_args()
    data = {}
    if a.command == 'dose': data = dict(duration_ms=a.ms, duty=a.duty)
    if a.command == 'config': data = dict(closed_us=a.closed_us, open_us=a.open_us, motor_ready=a.motor_verified)
    if a.command == 'calibrate': data = dict(pulse_us=a.pulse_us)
    payload = None if a.command == 'status' else json.dumps(data).encode()
    request = urllib.request.Request('http://%s/api/%s' % (a.host, a.command), data=payload, headers={'Content-Type': 'application/json'})
    # Bypass OS HTTP proxies for this direct local access-point connection.
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with client.open(request, timeout=4) as result: print(result.read().decode())
    except urllib.error.HTTPError as error:
        raise SystemExit(error.read().decode())


if __name__ == '__main__': main()
