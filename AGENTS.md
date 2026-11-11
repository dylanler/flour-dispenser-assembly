# Hardware design requirements

Before any 3D-printed hardware design or revision, check manufacturer schematics, datasheets, and dimensioned drawings online. Verify the exact component variant, all mating protrusions/bosses, mounting geometry, shaft position and reach, tolerances, and assembled height stack. Document sources and unverified dimensions; nominal overall dimensions are not enough.

Do not label a hardware interface physically validated merely because meshes are watertight, collision checks pass, or a slicer completes. Use small interface tests before recommending a large print when component fit is unverified. Prioritize salvaging existing printed parts and minimizing reprinting.

Known issue: the original V3 hopper uses a round 14 mm servo opening that does not include the SG90 gearbox tail. The illustrated servo also omitted that tail. Do not recommend the original full plate as a verified SG90 fit. Consult docs/SERVO_FIT_AUDIT.md and the user's actual servo before issuing a repair or replacement.

Current repair: the user explicitly declined a separate fit test and requested wider relief. Use the V3.1 hopper-only replacement and document the unverified actual servo/horn stack. Keep other prints; do not force another test print or recommend the original full plate.

2026-11-09: V3.1 print recommendation withdrawn: full shaft-to-horn seating is unresolved. Refer to shaft_stack_review.json; do not recommend original or raised geometry as verified. The user wants review from existing schematics without a separate test print.

Current best-effort revision superseding V3.1: V3.2, requested after user said to check everything and give best shot. No servo support raise; shallow case recess, revised gate, optional gate-floor packing. User accepts no separate test print. No claim of physical validation. Use V3_2_REPAIR_PLATE_HOPPER_GATE_PACKING.3mf and repair_v3_2_report.json. Keep stand/lid/clips. User says horn adds around 2 mm; this is an estimate with ambiguous datum, not a socket-depth measurement. Horn goes on below hopper afterward: it need not pass through the hopper opening.
Current full assembly (2026-11-11): src/assembly-steps.js and src/scene-v32.js, shared with BUILD_GUIDE_V3_2.html. Seat horn on servo before gate. Packing is below horn arms, never under servo ears. The 0.6 mm strip is a reference, not a pass/fail gauge for every valid gap. Latest video: flour-v3-2-assembly.webm. Do not restore superseded V3 instructions. No print geometry changed.
