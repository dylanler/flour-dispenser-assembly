# Flour / V2

A four-piece, one-plate flour dispenser prototype with an SG90 rotary gate, a **5V PWM Vibration Motor Switch Module (9000 RPM)**, a USB-C classic ESP32, and a breadboard. No Arduino IDE, frame screws or buffer chip. The chosen cut-USB power lead needs secure insulated joints: existing suitable connectors, or solder and insulation.

**[Watch the interactive assembly film](https://dylanler.github.io/flour-dispenser-assembly/)** · [Download the rendered video](https://dylanler.github.io/flour-dispenser-assembly/flour-v2-assembly.webm) · [Build guide](public/hardware/BUILD_GUIDE_V2.html) · [Mac/Python setup](docs/SOFTWARE.md) · [Wiring](docs/WIRING.md) · [Parts](docs/PARTS.md)

![Four-part prototype](public/hardware/assembly_preview.png)

## Print and assemble

1. Download [the A1 one-plate 3MF](public/hardware/A1_SIMPLE_V2_ONE_PLATE.3mf). It contains geometry, not printer settings. Open in Bambu Studio, select A1 / 0.4 mm nozzle, and inspect the preview. Use 0.2 mm layers, 3 walls, 5 top/bottom layers, 20% gyroid, no supports. Keep the supplied orientation. Prior slicer estimate: 220.75 g / 6 h 31 min; actual settings change this.
2. Follow the 17-step animation or [printable HTML guide](public/hardware/BUILD_GUIDE_V2.html). The servo sits **above** the flange, shaft downward. Two zip ties hold the servo, two hold its supplied double-arm horn, and its supplied horn screw secures the gate.
3. Seat the hopper in the cradle and **fit both retaining bands** before powered testing. The drop-in pocket alone is not a latch.
4. Tape the 400-point breadboard to one outer cradle leg; foam-tape the ESP32 to the opposite outer leg with USB-C accessible sideways. The USB-A brick and cut power lead stay supported on the bench. See the animation for cable routing.
5. Install MicroPython using Python and USB-C. Center the servo before fitting the horn, calibrate empty, then try one teaspoon of flour over a cup.

## Electrical design

Your **5V USB-A brick → spare cut USB-A cable → secure insulated joints to solid jumpers → breadboard buses → servo + vibration module**. Your **MacBook USB-C → ESP32**, for both programming and power. No terminal adapter is required. Grounds are common. The "power junction" means the breadboard buses, not an additional module. **GPIO18 → servo signal; GPIO19 → module IN**, conditional on confirming the module accepts 3.3V logic with its 5V supply. Do not connect external +5V to the ESP32 3V3 pin, GPIOs, or USB supply.

Similar three-pin modules have documented 3.3V control, but the exact Amazon board lacks a verified threshold/schematic. Keep the module you bought; check it on arrival. A high-impedance IN voltage reading is a screening check, not proof of compatibility. If IN is near 5V, do not connect it to an ESP32 pin until the input circuit is identified. See [research and limitations](docs/RESEARCH.md).

Firmware boots disarmed with the motor disabled. `motor_ready` must be explicitly enabled after electrical checks; it resets every reboot. Gate-only tests use duty 0. A dose is limited to 5 seconds and arming expires after 60 seconds. A 50 ms full-duty motor startup pulse precedes the requested duty. Servo calibration and motor verification are deliberately not persisted: repeat/apply them after each reboot.

## Run the animation locally

Use Node.js **22.12+** and npm:

```sh
npm ci
npm run dev
```

Open the printed localhost URL. Play, pause, scrub, select a chapter, drag to orbit, or export a captioned WebM video. Export records in real time; keep the tab visible. The Three.js scene loads the actual printable STL meshes. Electronics dimensions and cable positions are illustrative, not fabrication templates. The final gate motion illustrates operation rather than measured dispensing.

```sh
npm test
python -m unittest discover -s tests -p "test_*.py"
npm run build
```

## What has been checked

The inherited meshes were checked for watertightness, one connected body per part, plate bounds, and nominal assembled gate clearance. Prior Bambu Studio slicing found all four objects within the A1 plate and used no supports. See `public/hardware/validation.json` and `slicer_validation.json`. The web app and Python state machine have automated tests; these do not establish physical compatibility or flour performance.

**Not physically tested:** servo clone/horn fit, retention-band strength, vibration strength, powder bridging, flow rate, or leakage. The gate has clearance rather than a seal and does not mechanically close on loss of power. Use this as a supervised prototype for small flour trials. Printed food-contact surfaces need your own material/cleanability assessment; this is not certified food equipment. This design is scoped to flour, not metallic powders.

## Repository map

- `src/`: Three.js scene, chapter text, playback and video export.
- `public/hardware/`: printable parts, source CAD, generated assembly guide and digital validation reports.
- `firmware/`: MicroPython device controller and local Wi-Fi interface.
- `scripts/`: computer-side Python upload/control tools and guide generator.
- `docs/`: purchasing, wiring, software and research details.
- `tests/`: timeline, timeout, calibration and motor-enable checks.

Wi-Fi control is implemented. USB-C is used for flashing, the MicroPython REPL, and programming; Bluetooth control is not implemented. The default local AP credentials are public prototype defaults: `FlourProto` / `FlourTest26`. Change them in `firmware/main.py` before use in a shared environment.

MIT license. No endorsement or affiliation with the hardware vendors.
