# Hardware design requirements

Before any 3D-printed hardware design or revision, check manufacturer schematics, datasheets, and dimensioned drawings online. Verify the exact component variant, all mating protrusions/bosses, mounting geometry, shaft position and reach, tolerances, and assembled height stack. Document sources and unverified dimensions; nominal overall dimensions are not enough.

Do not label a hardware interface physically validated merely because meshes are watertight, collision checks pass, or a slicer completes. Use small interface tests before recommending a large print when component fit is unverified. Prioritize salvaging existing printed parts and minimizing reprinting.

Known issue: the original V3 hopper uses a round 14 mm servo opening that does not include the SG90 gearbox tail. The illustrated servo also omitted that tail. Do not recommend the original full plate as a verified SG90 fit. Consult docs/SERVO_FIT_AUDIT.md and the user's actual servo before issuing a repair or replacement.

Current repair: the user explicitly declined a separate fit test and requested wider relief. Use the V3.1 hopper-only replacement and document the unverified actual servo/horn stack. Keep other prints; do not force another test print or recommend the original full plate.
