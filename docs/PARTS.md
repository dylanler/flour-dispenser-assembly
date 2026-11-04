# Parts and fit

Use your ordered items. Links below are the known listing or clearly labeled Amazon searches; search results may change and are not verified exact replacements.

| Part | Use | Link |
|---|---|---|
| Dorhea 30-pin ESP32 CH340 USB-C | One classic ESP32-WROOM board; inspect the module label | [Amazon search](https://www.amazon.com/s?k=Dorhea+ESP32+CH340+Type+C+30pin) |
| DIY-Module / GODIYMODULES 5V PWM vibration module, 9000 RPM | One **three-pin module with driver**, not a bare coin motor | [Amazon listing B0DY65KVQR](https://www.amazon.com/dp/B0DY65KVQR) |
| WWZMDiB SG90 servo pack | One servo, its double-arm horn and supplied center screw | [Amazon search](https://www.amazon.com/s?k=WWZMDiB+SG90+Micro+Servo+Motor+3+Pcs) |
| BOJACK 830/400-point breadboard + jumper kit | One 400-point board; the ESP32 mounts separately | [Amazon search](https://www.amazon.com/s?k=BOJACK+3+Values+130+Pcs+Solderless+Breadboard) |
| USB-A male to 4-pin screw-terminal adapter, two-pack shown by the user | One adapter plugs into the USB-A brick; only +5V and GND are wired | [Amazon search matching the shown type](https://www.amazon.com/s?k=USB+2.0+Type+A+Male+to+4+Pin+Screw+Terminal+Block+Connector) |

Home supplies to check: USB-C **data** cable for the MacBook/ESP32, regulated 5V USB-A brick, solid-ended breadboard jumper leads, multimeter, PLA, small zip ties, insulating foam tape, thin firm mounting tape, thin card shims, screwdriver, cutters and a cup. This version uses the four-terminal USB-A adapter shown by the user. No cut cable, splice connectors, soldering, MB102 module, SN74AHCT125N, 10k resistor or 0.1µF capacitor is required for the proposed wiring if the boards have headers fitted.

The brick supplies the servo and motor through the adapter. Check the brick's label for regulated **5V** output; **2A** gives useful headroom for servo peaks. The adapter is passive; it does not generate or regulate power. The listing's **300V / 8A** describes terminal hardware, not USB output. The exact SG90 clone stall current remains unmeasured.

With the brick unplugged, clamp two suitable solid jumper ends in **+5V / VCC / VBUS** and **GND / −**; tighten, tug-check and keep exposed metal from bridging terminals. Leave **D+ / D−** empty. Connect the jumper ends to the breadboard positive and ground buses. Existing male-to-male jumper ends can be used if the screws securely clamp them; otherwise use appropriately sized solid-core breadboard wire. Confirm the actual terminal labels and output polarity rather than copying a left/right position from the animation. Do not cut your USB-C programming cable or a USB-A cable.

The **power junction** is simply the breadboard +5V and ground buses. Support the brick/adapter beside the stand so cable tension does not load the USB connector. The adapter model is illustrative: the plug enters the brick's side port and leads leave the opposite end of the green block. The AC connection to the brick is omitted from the illustration; this build has no mains-side wiring instructions.

### Jumper ends and quantities

| Connection | Leads |
|---|---|
| ESP32 GND, GPIO18 and GPIO19 to breadboard | 3 female-to-male |
| Vibration-module VCC, GND and IN to breadboard | 3 female-to-male |
| SG90 three-hole socket to breadboard | 3 male-to-male |
| Adapter +5V and GND to breadboard | 2 suitable solid-ended male-to-male / solid-core wires |

Plan on **6 female-to-male** and **5 male-to-male** leads, plus any bridges needed for split breadboard rails. This assumes the ESP32 and module arrive with male headers fitted. Female sockets fit those headers; male ends fit the breadboard. The servo has a female socket, so it uses male jumper ends. The BOJACK kit may contain only male-to-male leads; check your existing wires. If needed: [Amazon search for pre-crimped male-to-female Dupont leads](https://www.amazon.com/s?k=male+to+female+dupont+jumper+wires). Female-to-female leads are optional if using breadboard junctions for both signal nets.

A multimeter is useful for identifying rail continuity, checking 5V output and screening the motor input before connection. Those checks cannot establish an undocumented input threshold by themselves. If the module circuit cannot be verified, leave its IN disconnected and use gate-only tests until resolved.

## Printed dimensions and placement

V3 stand footprint 224 × 140 mm; stand height 190 mm; assembled dispenser height about 247 mm. Hopper flange 124 × 104 mm fits a 125 × 105 mm pocket. Nominal gate gap is 0.6 mm. Parts fit in the supplied one-plate layout inside the A1 256 × 256 mm bed. Keep the nested layout.

The 400-point breadboard is illustrated at about 82 × 55 mm on the **right outer side wall**, long edge front to back, centered about 50 mm above the bench. The ESP32 sits on the **left outer side wall** with insulating foam tape and USB-C facing toward the front. Two printed locking clips capture the hopper at the front-left and rear-right notches. Print two copies of `05_locking_clip.stl` if printing individual parts; the V3 3MF already includes both. No bands or purchased clip hardware are required.

Your scale is modeled at 105 × 125 × 17 mm and 500 g maximum. The clear bay is 200 mm wide. The illustrated cup is diameter 60 mm × height 80 mm, an assumption until the real container is specified. The robot collects that cup from the open front; exact arm/gripper compatibility still needs testing. See [Robot clearance](ROBOT_CLEARANCE.md).

The clips use about a 0.6 mm nominal hook engagement in an underside recess. Print on the supplied broad side; do not rotate them upright. Inspect the hook, clear rough edges, and test the snap/release without forcing it. Clip strength and fatigue remain untested. The USB-A brick and four-terminal adapter stay beside the stand with strain relief.
