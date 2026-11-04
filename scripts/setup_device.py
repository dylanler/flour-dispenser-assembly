"""Run with CPython on your computer, not on the ESP32."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description='Flash/upload a classic ESP32 flour controller')
    parser.add_argument('--port', help='COM5 on Windows, /dev/ttyUSB0 on Linux')
    parser.add_argument('--list', action='store_true', help='List serial ports and exit')
    parser.add_argument('--firmware', type=Path, help='Official ESP32_GENERIC .bin downloaded from micropython.org')
    parser.add_argument('--erase', action='store_true', help='Confirm erasing all existing ESP32 files before flash')
    parser.add_argument('--baud', default='460800')
    args = parser.parse_args()
    if args.list:
        from serial.tools.list_ports import comports
        for port in comports(): print(port.device, port.description)
        return
    if not args.port: parser.error('--port is required (use --list to find it)')
    def run(*cmd): subprocess.run([sys.executable, '-m', *cmd], check=True)
    if args.firmware:
        if not args.erase: parser.error('Flashing erases the board. Add --erase after checking the module is classic ESP32-WROOM, not C3/S3')
        if not args.firmware.is_file() or not args.firmware.name.startswith('ESP32_GENERIC-') or args.firmware.suffix != '.bin': parser.error('Use a downloaded ESP32_GENERIC-*.bin for classic ESP32')
        run('esptool', '--chip', 'esp32', '--port', args.port, 'erase-flash')
        run('esptool', '--chip', 'esp32', '--port', args.port, '--baud', args.baud, 'write-flash', '0x1000', str(args.firmware.resolve()))
    for name in ['controller.py', 'main.py']:
        run('mpremote', 'connect', args.port, 'fs', 'cp', str(ROOT / 'firmware' / name), ':' + name)
    run('mpremote', 'connect', args.port, 'reset')
    print('Uploaded. Connect to FlourProto (password FlourTest26), then open http://192.168.4.1')


if __name__ == '__main__': main()
