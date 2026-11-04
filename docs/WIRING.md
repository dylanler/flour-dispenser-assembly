# Wiring — existing 5V PWM module and cut USB-A power lead

Disconnect USB and external power while wiring. Match labels printed on your boards, not physical pin order in a drawing. The ESP32 is mounted separately from the breadboard so its width does not block terminal holes.

Your MacBook USB-C connection programs **and powers the ESP32**. Your USB-A power brick supplies the servo and motor through a **spare cut USB-A cable**: **verified +5V conductor → +5V bus; verified GND conductor → ground bus**. Check the brick is rated for 5V output; 2A gives useful headroom. Join ESP32 GND to the same ground bus. This design does not draw motor/servo current through the ESP32 board.

The breadboard buses are the "power junction," not a separate purchased component. **No terminal adapter is required.** Unplug before cutting the spare cable, strip the cut end and verify the conductors with a meter. Red/black are common +5V/GND colors but are not guaranteed. Insulate each unused conductor separately. Use proper insulated joints from the power conductors to solid jumper ends: connectors you already own, or solder plus insulation. Do not insert loose stranded cable ends into the breadboard or servo socket, and do not rely on twist-and-tape joints. If you lack suitable connectors, this approach requires soldering.

Use the servo's existing socket with jumper pins; its power can come from these breadboard buses without cutting the servo lead. Support and strain-relieve the cut cable on the bench. Before connecting any electronics, verify the brick/cable polarity and check that the buses are not shorted. Then unplug again while making connections.

| From | To |
|---|---|
| External regulated +5V | Breadboard positive bus |
| External supply GND | Breadboard ground bus |
| ESP32 GND | Same ground bus |
| Servo red | +5V bus |
| Servo brown/black | Ground bus |
| Servo orange/yellow | ESP32 GPIO18 |
| Vibration module VCC / + | +5V bus |
| Vibration module GND / − | Ground bus |
| Vibration module IN / S | GPIO19 **only after compatibility check** |
| ESP32 USB-C | Computer for flashing; USB power during use |

The external +5V bus does **not** connect to the ESP32 3V3 pin, any GPIO, or its USB/VIN supply. The two supply grounds must connect. Never power the motor or servo directly from a GPIO. This version uses the module's onboard driver.

![Schematic wiring overview](../public/hardware/wiring.svg)

## Breadboard details

On a typical 400-point board, each group of five terminal holes connects together; opposite sides of the center channel do not. Long edge rails are separate buses and may be split. Confirm continuity on the actual board with power disconnected. Label the +5V and ground buses. Bridge split sections only when necessary, with power disconnected, and recheck for a short before powering.

For signals, use a free five-hole group for each separate net: GPIO18 and servo signal in one group, GPIO19 and module IN in another. Do not join those groups to each other or to +5V. Male-to-female jumper leads connect male ESP32/module headers to the breadboard; male-to-male leads can connect the servo female socket to it. Secure leads so servo vibration cannot pull them out.

## Check the motor module before GPIO19 connection

1. Keep module IN disconnected from the ESP32. Verify the module's printed VCC/GND/IN labels.
2. Apply regulated 5V to VCC and GND. The specified 3.7V starting voltage concerns the motor supply, not the control signal.
3. Measure IN relative to GND. If it is near 5V, **do not connect it to a GPIO** until its input circuit is identified. A low reading alone does not prove compatibility. Confirm through the seller's input specification or inspection of the actual board's driver/input network that 3.3V is accepted and the ESP32 pin is not exposed to 5V.
4. With external power off, connect the verified IN to GPIO19 and join grounds. Upload the firmware first; it starts with motor PWM at zero.
5. After verification, tick the explicit motor checkbox in the setup page. Run a small supervised test, then press Stop. Leave vibration disabled if it runs with PWM zero, fails to start, or behaves erratically.

Research supports common modules accepting 3.3V logic; it does not prove the exact Amazon batch. If this module needs a driver/level adapter, that is a later hardware change. Do not substitute a bare 3V motor on GPIO19. Gate-only operation with `duty: 0` remains available.

## Mechanical wiring checks

Tape the board back, not conductive pins, to the leg. Use insulating foam tape behind the ESP32. Keep USB-C accessible, both band paths clear and all wires outside the rotating gate. Mount the vibration module firmly on the hopper exterior with its solder joints insulated. Route slack outward and secure it to the frame; no dangling leads beneath the gate.

If the servo causes resets or jitter, stop and inspect supply rating, cable resistance, ground connections and breadboard contacts. Extra power filtering or a separate servo power distribution arrangement may be necessary after testing; the current design has no added capacitor.
