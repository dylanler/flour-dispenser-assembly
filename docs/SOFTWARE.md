# Python setup, no Arduino IDE

The device runs MicroPython; the computer setup/control tools use ordinary Python. The assembly animation uses JavaScript/Three.js. Wi-Fi control is implemented; Bluetooth is not.

## 1. Check the board

These instructions target the **classic ESP32-WROOM** 30-pin USB-C CH340 board, with at least 4 MiB flash. Read its metal module label. ESP32-C3/S3/S2 require different firmware and may need different GPIOs. A USB-C connector alone does not identify the chip. Do not proceed with the classic firmware on those variants.

Disconnect external 5V to the servo/motor before flashing. Use a USB-C **data** cable. A charge-only cable will power the board but not provide a serial port. If no CH340 serial port appears, first try another known data cable. Many recent Macs recognize it without an extra driver. If a driver is required, obtain the driver for your operating system from [WCH](https://www.wch-ic.com/), the chip manufacturer.

## 2. Install computer tools on your MacBook

Plug the ESP32 directly into your MacBook using a USB-C **data** cable. This supplies the ESP32 for programming and normal operation. Keep that cable intact. The servo and vibration module use your **5V USB-A power brick through a separate spare cut USB-A cable**, with secure insulated joints and common ground. No terminal adapter is included. This build does not route their power through the ESP32 USB/5V pin; that board's power-path rating is unverified. See [Wiring](WIRING.md) for preparing the cut lead; the "power junction" is just the breadboard buses.

From the repository folder in Terminal, with Python 3.10 or newer installed:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/setup_device.py --list
```

Choose the ESP32's reported `/dev/cu.*` port, such as `/dev/cu.usbserial-XXXX` or `/dev/cu.wchusbserialXXXX`. Use the actual reported name in every command; the examples are placeholders. Unplug/replug the board and compare the list if needed. If Python is missing, install it from [python.org](https://www.python.org/downloads/macos/). No Arduino IDE or Node.js is needed to program or operate the dispenser.

Windows alternative: use `python -m venv .venv`, `.venv\Scripts\python.exe` instead of `.venv/bin/python`, and the reported `COM` port instead of `/dev/cu.*`. Linux uses `.venv/bin/python` and the reported `/dev/ttyUSB*` device.

## 3. Download and flash MicroPython

Download a **stable standard ESP32_GENERIC `.bin`** from the [official ESP32/WROOM download page](https://micropython.org/download/ESP32_GENERIC/). Do not use a C3/S3, OTA, or SPIRAM-only variant by accident. This repo does not redistribute the firmware binary. The official page's classic ESP32 installation address is `0x1000`; `setup_device.py` uses it.

Replace the example firmware path with the real downloaded filename:

```sh
.venv/bin/python scripts/setup_device.py --port /dev/cu.usbserial-XXXX --firmware "$HOME/Downloads/ESP32_GENERIC-version.bin" --erase
```

`--erase` explicitly acknowledges erasing the ESP32's existing firmware/files. The script calls esptool to erase/flash, then mpremote to copy `controller.py` and `main.py` and reset. If connection fails, hold BOOT while the tool connects, then release; close other serial-terminal programs. Retry at `--baud 115200` if flashing is unreliable.

For later code-only updates without erasing MicroPython:

```sh
.venv/bin/python scripts/setup_device.py --port /dev/cu.usbserial-XXXX
```

## 4. Center and assemble

Reconnect regulated external 5V and common ground with the **horn removed**. Connect to Wi-Fi **FlourProto**, password **FlourTest26**, and open **http://192.168.4.1**. The phone/computer may warn this network has no internet; stay connected.

Choose **Center with horn removed**. It outputs 1500 µs. Disconnect external power, then install the horn/gate in the closed position and insert the supplied screw. Adjust the servo ear packing for free gate clearance. Fit both printed locking clips and secure the cables before movement tests.

On the setup page, adjust open/closed pulse widths in small increments with an **empty hopper**. The initial closed/open values are 1500/1000 µs. They are starting values, not a guarantee of exact angles or outlet alignment. The animation shows an illustrative 60° travel; real servo pulse-to-angle response varies. Avoid driving a hard stop. `Test open pulse` deliberately moves and holds the gate for calibration, with the motor off; press Stop when done. Keep hands clear.

Apply the calibrated values. Motor control remains disabled until you verify the module input and explicitly enable it. Settings reset at reboot; reapply your measured values before every session. An empty test with vibration duty 0 is allowed while verification is pending.

## 5. Python control over Wi-Fi

After joining the access point:

```sh
python3 scripts/control.py status
python3 scripts/control.py center
python3 scripts/control.py config --closed-us 1500 --open-us 1000
python3 scripts/control.py arm
python3 scripts/control.py dose --ms 500 --duty 0
python3 scripts/control.py stop
```

After the input check, apply your calibration and motor verification explicitly:

```sh
python3 scripts/control.py config --closed-us 1500 --open-us 1000 --motor-verified
python3 scripts/control.py arm
python3 scripts/control.py dose --ms 500 --duty 30
```

Those example pulse values still require calibration. The client uses only Python's standard library. `stop` closes/disarms and turns vibration off. Doses accept 100–5000 ms and integer duty 0–100%. Arming lasts 60 seconds; each completed dose disarms. A positive duty gives a 50 ms full-duty startup kick before dropping to the requested level. This cannot increase the supply voltage.

## USB and recovery

USB-C supports flashing and a MicroPython REPL using `.venv/bin/python -m mpremote connect /dev/cu.usbserial-XXXX repl`. Ctrl-C interrupts the program and executes the stop cleanup if Python is still responsive. This is a programming console, not the Wi-Fi command API. There is no separate continuous USB control protocol in this version.

The supervisor checks deadlines every 10 ms; an 8-second watchdog resets a stalled interpreter. Neither is a substitute for disconnecting power if the mechanism misbehaves. Loss of Wi-Fi does not prolong an already timed dose, but loss of power does not mechanically close the gate.

Default AP credentials are public. Change them in `firmware/main.py` if desired. The local API has no additional login/TLS and should remain on its isolated prototype network.

References: [MicroPython PWM](https://docs.micropython.org/en/latest/library/machine.PWM.html), [ESP32 quick reference](https://docs.micropython.org/en/latest/esp32/quickref.html), [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), [esptool flashing](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/flashing-firmware.html).
