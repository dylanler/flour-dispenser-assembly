# Validation scope

## Software checks completed

- Production Vite build succeeded with Node 22.23.4; npm audit reported zero known vulnerabilities at installation time.
- Two JavaScript tests cover all timeline boundaries and presence of key assembly constraints.
- Eight CPython unit/integration tests exercise the actual controller and HTTP handler with mocked PWM hardware: boot state, unverified motor rejection, gate-only operation, startup kick, dose deadline, arm expiry, duplicate-dose rejection, input bounds, calibration, configuration and Stop.
- Headless Chrome loaded the actual STL scene with no page errors. All 17 chapter buttons, previous/next, playback/pause, desktop layout and 390 px mobile layout were checked. Browser control-page checks confirmed that calibration, motor verification and dose inputs produce the intended JSON requests.
- The app exported a captioned WebM walkthrough from its own Three.js renderer. Source geometry is the supplied print geometry; electronics/cable illustrations are approximate.

Optional reproducible browser checks are in `scripts/browser_check.py`; see its header for Playwright setup. They are separate from the hardware setup requirements. A development server must be running first.

## Inherited digital hardware checks

The mesh and slicer reports in `public/hardware/` describe the existing printable V2 model. They report watertight connected pieces, valid plate placement, nominal 0.6 mm gate gap and interference-free printed geometry through the checked sweep. Prior Bambu Studio slicing used A1 / 0.4 mm, 0.2 mm layers, 3 walls, 5 top/bottom layers, 20% gyroid, no supports; estimate 220.75 g and 23,459 seconds.

Those results do not include SG90 clone dimensions, mounting tape, wires or retention-band force. Source CAD regenerates the printable model; it does not regenerate a Bambu printer profile.

## Still requires the actual parts

This repository has not been flashed to the purchased ESP32. GPIO voltage compatibility of the exact vibration module, servo pulse mapping, horn/shim fit, USB/CH340 behavior, supply performance, adhesion, retaining bands, flour flow and sealing have not been physically tested. MicroPython code was syntax checked and exercised through hardware mocks, not executed on this ESP32.

Do not interpret a passing simulation, browser test or firmware test as a measured dispensing result. Follow the arrival checks and small supervised flour trial in the guide.
