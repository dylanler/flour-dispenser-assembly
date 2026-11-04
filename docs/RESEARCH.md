# Motor compatibility evidence

Decision: retain the purchased **5V PWM Vibration Motor Switch Module, 9000 RPM minimum**. Do not substitute a bare two-wire 3V coin motor for the module. The circuit below assumes the onboard module driver accepts 3.3V logic; the exact purchased board still needs checking on arrival.

## What the listing establishes

The user-provided specification gives 5V rated supply, 3–5.3V operating range, 3.7V starting voltage, up to 60mA running and 90mA starting current. It says a high input activates the motor. It does **not** supply a verified logic-high threshold, schematic, or guarantee against 5V on IN.

The review about starting at 3.7V is relevant if powering the motor from 3.3V. This build supplies the module from regulated **5V**. A 3.3V PWM signal is a command to its driver, not its motor power source. Raising duty cycle cannot raise a supply beyond its own voltage.

## Supporting sources

- [Simon42 forum: ESP32 vibration module](https://community.simon42.com/t/vibrationsmotor-mit-esp32-steuern/31861): the original poster reported success after connecting a similar AZ-Delivery three-pin module to 3.3V, ground and a digital output. This is firsthand evidence for that module, not the exact Amazon product or a 5V-powered test.
- [eBits module specification](https://ebits.dk/en/products/vibration-motor-modul): a similar supplier module explicitly separates its 3.7–5V supply from its 3–5.3V control input; it also lists 60mA operating, 90mA startup and 9000 RPM. Shared numbers suggest a common module family, but do not establish identical circuitry across sellers.
- [Precision Microdrives PWM application note](https://www.precisionmicrodrives.com/ab-012): explains separate PWM control, driver switching and duty cycle. [Discrete driver guidance](https://www.precisionmicrodrives.com/discrete-driver-circuits-for-vibration-motors) explains why a bare motor needs additional current-handling circuitry.
- [Reddit: vibration module and Pi Zero](https://www.reddit.com/r/raspberry_pi/comments/1risqaw/vibration_motor_module_and_pi_zero_2w/): remaining comments describe unexpected behavior and a reported high GPIO voltage. The original post is removed and the board/wiring are not established. This is a cautionary anecdote, not proof that the purchased module is incompatible.
- [Espressif ESP32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf): ESP32 GPIO is not a general 5V-tolerant input. Keep module power and logic voltage distinct.

## Practical conclusion

3.3V control is plausible and common for similar boards; exact compatibility remains unverified. No buffer chip is included. Check the actual board's input circuit/specification before attaching GPIO19. If verification is unavailable or IN has an unexplained near-5V voltage, leave it disconnected and motor control disabled. The firmware supports gate-only testing at duty 0.

Electrical compatibility also does not prove the motor can mobilize flour. RPM alone does not specify vibration force. Hopper loading, coupling stiffness, flour moisture and bridging determine useful output. Test a small amount first. The motor, servo, band retention and flour flow have not been physically tested with this printed prototype.
