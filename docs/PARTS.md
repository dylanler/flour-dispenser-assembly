# Parts and fit

Use your ordered items. Links below are the known listing or clearly labeled Amazon searches; search results may change and are not verified exact replacements.

| Part | Use | Link |
|---|---|---|
| Dorhea 30-pin ESP32 CH340 USB-C | One classic ESP32-WROOM board; inspect the module label | [Amazon search](https://www.amazon.com/s?k=Dorhea+ESP32+CH340+Type+C+30pin) |
| DIY-Module / GODIYMODULES 5V PWM vibration module, 9000 RPM | One **three-pin module with driver**, not a bare coin motor | [Amazon listing B0DY65KVQR](https://www.amazon.com/dp/B0DY65KVQR) |
| WWZMDiB SG90 servo pack | One servo, its double-arm horn and supplied center screw | [Amazon search](https://www.amazon.com/s?k=WWZMDiB+SG90+Micro+Servo+Motor+3+Pcs) |
| BOJACK 830/400-point breadboard + jumper kit | One 400-point board; the ESP32 mounts separately | [Amazon search](https://www.amazon.com/s?k=BOJACK+3+Values+130+Pcs+Solderless+Breadboard) |

Home supplies to check: USB-C **data** cable for the MacBook/ESP32, regulated 5V USB-A brick, a **spare USB-A cable to cut**, suitable existing splice connectors or solder and insulation, solid breadboard jumpers, multimeter, PLA, small zip ties, two narrow retaining bands, insulating foam tape, thin firm mounting tape, thin card shims, screwdriver, cutters and a cup. No terminal adapter, MB102 module, SN74AHCT125N, 10k resistor, or 0.1µF capacitor is part of this version.

Your USB-A power brick supplies the servo and motor through the cut USB-A cable. Check the brick's label for regulated **5V** output; **2A** gives useful headroom for servo current peaks. A 2A supply does not force 2A through the motor. Exact SG90 clone stall current remains unmeasured.

The **power junction** is simply the breadboard +5V and ground buses; it is not another module to buy. This version follows the requested cut-cable approach. Its two power conductors need proper insulated joints to solid jumpers. Use suitable connectors already at home, or solder plus heat-shrink/equivalent insulation. It is not an entirely plug-in assembly anymore, and no-solder operation depends on having suitable connectors.

Unplug the spare USB-A cable before cutting. Keep the USB-A plug and strip the cut end. Identify +5V and GND with a meter or continuity to the connector contacts; colors alone are not proof. Connect only those verified conductors to the matching breadboard buses, through secure insulated joints and solid jumper ends. Insulate each unused conductor separately. Keep cut strands out of servo sockets and breadboard contacts. Support the cable on the bench and add strain relief so a tug cannot pull out the breadboard leads. Keep your ESP32 programming cable intact.

Check jumper **ends**, not just the count. The ESP32/module male headers need female sockets. Many BOJACK flexible jumper kits contain only male-to-male wires. If your home wires do not include female ends, pre-crimped male-to-female Dupont leads are the remaining wiring purchase: [Amazon search](https://www.amazon.com/s?k=male+to+female+dupont+jumper+wires). Signals can pass through spare breadboard terminal groups so male-to-female leads suffice; female-to-female leads are optional. Board headers must arrive fitted to avoid soldering those headers.

A multimeter is useful for identifying rail continuity, checking 5V output and screening the motor input before connection. Those checks cannot establish an undocumented input threshold by themselves. If the module circuit cannot be verified, leave its IN disconnected and use gate-only tests until resolved.

## Printed dimensions and placement

Cradle footprint 134 × 114 mm; total assembled height about 149 mm. Hopper flange 124 × 104 mm fits a 125 × 105 mm pocket. Nominal gate gap is 0.6 mm. Parts fit in the supplied 250 × 250 mm layout inside the A1 bed.

The 400-point breadboard is illustrated at about 82 × 55 mm on the **front outer leg**, long edge horizontal, centered about 40 mm above the bench. The ESP32 sits on the **rear outer leg** with insulating foam tape and USB-C sideways. Keep both bands outside the gate sweep, near CAD X −25 and +85 mm, at most 6 mm wide. Check actual component dimensions and tape adhesion before committing. The USB-A brick and insulated cable joints stay supported on the bench with strain relief.
