# Scale and robot access

## Known dimensions

The supplied scale image states **125 × 105 × 17 mm**, maximum **500 g**. The model places its 105 mm side across the opening and 125 mm side front to back, controls facing forward. This represents the overall scale envelope, not a measured active weighing-platform area.

The robot should pick up the collection cup **under** the dispenser. It should not lift the hopper/stand. The V3 stand has an open front and rear, 200 mm between side walls, a 224 × 140 mm footprint and 190 mm top height. The gate underside is nominally 180.2 mm above the table; reserve about 5 mm more for the horn screw and dimensional variation. Measure actual hardware before setting robot waypoints.

The scale rests independently on the table. Center it under the outlet at CAD X = 0, Y = 0; do not center it under the asymmetrical hopper flange. It has 47.5 mm nominal clearance on each side when centered. Its 125 mm depth fits between the 140 mm front/back edges, but the open ends permit positioning adjustments. Neither the cup nor the scale may contact the stand, gate, cables or clip tabs during weighing.

## Cup assumption

The actual collection-container dimensions were not provided. The animation uses **Ø60 × 80 mm**. Its top is about 97–98 mm above the table on the scale. Using the conservative 175 mm hardware plane leaves about 77 mm of overhead room before lifting. Larger cups reduce that margin. The animation lifts 15 mm and moves forward 145 mm as a visual example, not a robot trajectory.

Keep **cup height + scale height + lift distance + a clearance margin below the real lowest hardware point**. For lateral clearance, include the closed gripper's outer width, fingertip thickness, wrist/camera and positioning error, not just the cup diameter. A wide opening alone does not guarantee reachability.

## Suggested physical check

1. With dispenser power disconnected, place the real scale and empty cup under the outlet. Check scale controls remain reachable and all parts are separate.
2. Approach from the open front. Keep wrist and cables out of the hopper/gate area. Test gripper opening/closing around the actual cup without moving the dispenser.
3. Check a small vertical lift and forward withdrawal at low speed, including fingers, wrist and any wrist camera. Retain clearance from the stand's lower edges, top frame and gate screw.
4. After robot access is established, run supervised dispensing. Stop vibration, wait for a stable reading, and check cup plus powder stays within the scale's 500 g rating before pickup.

The scale is manually read. No serial/Bluetooth scale interface, robot control, inverse kinematics or collision validation has been implemented.

## Why no exact YAM / SO-101 fit claim

The arm's gripper and tooling determine the actual envelope. The official [SO-101 description](https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-lab/latest/train-a-robot-arm/02-so101-robot.html) describes a five-joint arm and two-finger gripper. The [I2RT YAM model documentation](https://github.com/i2rt-robotics/i2rt/blob/main/i2rt/robot_models/arm/yam/v1/README.md) separates the arm-only model from the selected gripper. Neither establishes which fingers, camera, wrist pose or collection cup this build will use. The 200 mm bay is a design envelope to test, not a verified fit for every variant.
