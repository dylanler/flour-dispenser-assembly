// Canonical V3.2 order. Both the live assembly and full HTML guide use this data.
export const chapters = [
 ['Identify the V3.2 repair prints','Use the latest repair plate; reuse the stand, lid and both locking clips.',[
  'New prints: 08 hopper, 09 gate, optional 0.4 / 0.8 / 1.6 mm packing and the removable 0.6 mm assembly strip.',
  'A1, 0.4 mm nozzle, matching PETG preset, 0.20 mm layers, 3 walls, 5 top/bottom layers, 15% gyroid, supports off.',
  'Remove stringing from the case pocket, tail relief, gate grooves and clip interfaces. Do not use the old hopper or old gate.'],
  'The repair plate contains six pieces including optional aids. The stand, lid and clips are retained parts, not additional reprints. Physical fit remains unverified.'],
 ['Prepare the retained stand','Place the existing wide stand upright, with its hopper pocket facing up.',[
  'Keep the open front accessible. The 200 mm bay accepts the illustrated 105 × 125 × 17 mm scale on the table.',
  'Remove both locking clips and set them aside. Assemble the hopper/servo/gate off the stand first.',
  'Keep the scale independent of the stand; leave USB and the external 5V brick unplugged.'],
  'The animation holds the head above the stand as an exploded illustration; it is not a self-supporting assembly position.'],
 ['Mount the servo in the new hopper','Insert the SG90 boss and shaft down through the V3.2 hopper opening.',[
  'The small gearbox tail points toward the long case side and farther ear support. The rectangular case enters the shallow clearance pocket.',
  'Rest both ears flat on the original-height supports. Do not add servo-ear shims or spacers.',
  'Use one tie through each same-side slot pair. Upper runs bear on the case edges; lower runs sit in the longitudinal underside channels. Keep ties off the shaft.'],
  'The new opening clears the boss and shaft, not the horn. The horn installs below the hopper later. Do not pull a tight fit together with zip ties.'],
 ['Attach the vibration module','Mount the existing 5V PWM driver module on the outside of the hopper.',[
  'Use thin firm tape and insulate exposed solder joints. Keep the motor outside the flour path.',
  'Face the connector outward and route slack away from the moving gate.',
  'Leave module VCC (W09) and IN (W11) disconnected during initial servo-only tests.'],
  'The module supply is 5V. Its actual input circuit must be checked separately for ESP32 3.3V control. No new driver or bare motor is substituted.'],
 ['Mount the breadboard and ESP32','Use the outside walls of the retained stand for the electronics.',[
  'Tape the 400-point breadboard to the right outer wall, long edge front-to-back, around 50 mm above the table.',
  'Use insulating mounting tape for the USB-C ESP32 on the left outer wall; leave the USB connector accessible.',
  'Use A–E rows 1, 3, 5 and 7 as the four junctions. Long edge rails are unused.'],
  'Verify actual five-hole strip continuity while unpowered. The ESP32 is mounted separately, not squeezed across the breadboard.'],
 ['W01–W02: connect and check 5V','Use only the adapter terminals marked +5V/VCC/VBUS and GND.',[
  'With the brick unplugged, W01 goes from adapter +5V to A1; W02 from adapter GND to A3.',
  'Leave D+ and D− empty. Support the USB-A adapter and brick on the bench; do not modify the brick.',
  'With only W01/W02 fitted, verify about +5V from row 1 to row 3. Unplug again before adding component leads.'],
  'Read actual terminal labels. D− is data, not ground. The adapter’s 300V/8A listing is not the USB output specification.',
  [['W01 · adapter +5V','A1 · M–M / solid-ended'],['W02 · adapter GND','A3 · M–M / solid-ended']]],
 ['W03–W05: ground and control','Connect the ESP32 headers to the three separate breadboard strips.',[
  'W03: ESP32 GND → B3, joining computer ground to external supply ground.',
  'W04: GPIO18 / D18 → A5. W05: GPIO19 / D19 → A7.',
  'Female jumper ends cover the ESP32 male headers; male ends enter the breadboard. External +5V does not enter ESP32 VIN, 3V3, GPIO or USB power.'],
  'Use labelled GPIO18 and GPIO19, not the eighteenth and nineteenth physical header positions. Diagrams are logical label maps, not a verified purchased-board pin order.',
  [['W03 · ESP32 GND','B3 · F–M'],['W04 · ESP32 GPIO18','A5 · F–M'],['W05 · ESP32 GPIO19','A7 · F–M']]],
 ['W06–W08: connect the servo','Keep the servo’s existing three-hole female socket and factory wires.',[
  'W06: red → B1. W07: brown/black → C3.',
  'W08: orange/yellow → B5. A5/B5 share one strip, completing GPIO18 → servo signal.',
  'Use three male–male leads: one end in each correctly identified servo-socket cavity, the other in its named breadboard hole. Keep inserted pins insulated and seated.'],
  'The servo receives external 5V, not GPIO power. Module VCC/IN stay disconnected for this first test. The USB-C cable separately powers/programs the ESP32.',
  [['W06 · servo red','B1 · M–M'],['W07 · servo brown/black','C3 · M–M'],['W08 · servo orange/yellow','B5 · M–M']]],
 ['Install the MicroPython controller','Use your MacBook and USB-C data cable; Arduino IDE is not needed.',[
  'Keep external servo/motor power disconnected while flashing. Use the software guide for classic ESP32-WROOM firmware and port selection.',
  'Run the Python setup tool and copy the controller files. Flashing replaces firmware already on the board.',
  'The controller starts disarmed, with vibration disabled. Leave the horn and gate off the shaft.'],
  'The software instructions target the purchased classic ESP32, not ESP32-C3/S3. The USB-C plug shape alone does not identify the chip.'],
 ['Center with the horn removed','Apply the checked external 5V supply and electronically center the bare servo.',[
  'Connect to FlourProto, password FlourTest26, and open 192.168.4.1.',
  'Press Center with horn removed. Keep fingers and loose leads away from the output shaft.',
  'Disconnect both external power and USB before attaching the horn or gate.'],
  'The nominal pulse is 1500 µs. Real open/closed limits are calibrated after assembly; geometric drawing angles are not raw servo commands.'],
 ['Seat the supplied horn first','Fit the SG90’s supplied double-arm horn directly onto the centered shaft, below the hopper.',[
  'Fully seat its spline socket without forcing it. The horn never passes through the hopper opening.',
  'Gently secure the horn with its supplied centre screw. Do not use the screw to pull a partly seated or interfering horn into place.',
  'Keep the printed gate separate for now. The centre opening of the new gate leaves access to this screw later.'],
  'The pictured horn/socket is a reference with assumed dimensions, not proof of the purchased unit’s seating. Do not trim the horn or alter its spline to match this illustration.'],
 ['Fit the new gate and optional packing','Lift the V3.2 gate around the already seated horn, then secure the horn arms to its pocket floor.',[
  'Start with no packing. Put the arms in the long pocket, with their flat outer faces toward the floor; align a closed gate position before fastening.',
  'Aim for a free 0.4–0.8 mm gate gap. If it rubs, remove the gate and add the smallest needed combination of 0.4 / 0.8 / 1.6 mm packing under the arms. Packing lowers the gate; it is not a servo-ear spacer.',
  'Use two ties in the gate’s upper/lower cross-grooves to clamp the arms and any packing. Tighten evenly without bowing the gate; keep the horn fully seated.'],
  'The 0.6 mm strip is a removable reference aid, not a required installed part or pass/fail gauge: a valid 0.5 mm gap will not admit it. Do not add packing merely to force the strip in. Remove it before movement.'],
 ['Seat the completed hopper head','Lower the hopper flange into the retained stand pocket with the gate attached beneath it.',[
  'Guide all leads outside the frame. The flange should sit flat without trapping a wire or packing piece.',
  'Place the collection cup on the scale under the outlet, clear of the stand and gate.',
  'The scale and cup stay on the table and must not touch the frame. Cup plus flour must remain within the stated 500 g scale capacity.'],
  'The latest gate is thicker than the original. Nominal underside height is about 178.3 mm at a 0.6 mm gap; check real screw/tie clearance. The cup is an assumed Ø60 × 80 mm example.'],
 ['Refit both printed locking clips','Insert the retained clips at the front-left and rear-right notches.',[
  'Upper jaws capture the hopper flange; lower jaws pass under the stand ledge.',
  'Push until each lower hook engages its recess, then gently tug-check retention.',
  'For removal, unplug power, press the release tab down and slide the clip out. No retaining bands or frame screws.'],
  'Use the clips you already printed. Actual PETG flex, retention force and fatigue are not established by the animation. Do not force an overly tight clip.'],
 ['Finish wiring and secure the cables','Add the motor connections only after its actual input compatibility has been established.',[
  'W09: module VCC → C1; W10: module GND → D3. W11: verified module IN/S → B7, sharing row 7 with GPIO19 at A7.',
  'If input compatibility remains unresolved, leave W09 and W11 disconnected and continue servo-only operation.',
  'Use the 11-wire guide for both ends and connector types. Secure service loops outside the gate, clip tabs, scale and front collection approach.'],
  'The motor’s 5V supply does not establish 3.3V logic compatibility. A low IN voltage reading alone is insufficient. W11 is conditional, not an instruction to connect an unknown input.',
  [['W09 · module VCC','C1 · F–M'],['W10 · module GND','D3 · F–M'],['W11 · verified module IN/S','B7 · F–M · conditional']]],
 ['Calibrate empty, then fit the lid','Check the assembled gate using small powered calibration movements before adding flour.',[
  'Verify no rubbing, trapped tie, stalled servo or unseated horn. Set actual open/closed limits in the controller.',
  'CAD uses 0° aligned-open and 60° nominal closed; the 14 mm holes already stop overlapping near 23.1° relative rotation.',
  'Only after empty checks, add a small flour charge and the retained lid. Enable vibration only after its input check.'],
  'This is a clearance gate, not a powder-tight seal or mechanically fail-closed valve. Never force the shaft by hand or use more servo travel to overcome binding.'],
 ['Run a short dose and weigh','Arm a short supervised dose, then close the gate and let the scale settle.',[
  'Start small. The controller limits a dose to 5 seconds and disarms after 60 seconds.',
  'Stop vibration before reading the scale. It has no electronic connection to the ESP32; dosing remains timed.',
  'Record actual delivery before pursuing larger doses with ±10 mg accuracy. The visual motion is not a powder-flow simulation.'],
  'Neither a 0.01 g display increment nor the animation proves ±10 mg accuracy. Flour bridging, late dribble, supply performance and real robot/cup pickup remain untested.']
].map((c,i)=>({id:i,title:c[0],description:c[1],points:c[2],note:c[3],connections:c[4]||[],duration:[5,6,7,11,14].includes(i)?14:10}));
export const totalDuration=chapters.reduce((s,c)=>s+c.duration,0);
export const startTime=i=>chapters.slice(0,i).reduce((s,c)=>s+c.duration,0);
export function chapterAt(time){let start=0;for(const c of chapters){if(time<start+c.duration||c.id===chapters.length-1)return{chapter:c,progress:Math.min(1,Math.max(0,(time-start)/c.duration))};start+=c.duration;}}
