# SG90 fit issue: salvage the existing print

**Do not print the original full V3 plate again to fix this.** A user has physically reported that the SG90 gearbox tail does not clear the circular hole. The old hardware illustration omitted that tail. Prior mesh and slicer checks did not validate servo fit, and the earlier recommendation to commit to the full print was too confident.

Keep the stand, gate, lid and clips. The current repair replaces only the hopper, as requested by the user without a separate test print. Older diagnostic and hand-fit options below are optional historical alternatives. No physical fit is claimed.

## Sources and variant limits

- [Tower Pro's SG90 Analog specification](https://towerpro.com.tw/product/sg90-analog/) gives an overall envelope of 23 × 12.2 × 29 mm. Its own configuration table uses other reference dimensions. An overall envelope does not specify the full gearbox profile.
- A Tower Pro-branded [dimensioned sheet](https://www.mantech.co.za/Datasheets/Products/SMY-SG90.pdf), visually reviewed, shows the secondary gearbox lobe and a different set of overall dimensions. It is a reference, not proof of this purchased unit.
- The user supplied a **detailed SG90/Addicore drawing** with the critical dimensions below and a stated ±1.5% deviation. This is the reference for the small test kit. It has not been established as the exact WWZMDiB unit's drawing.
- The user's other six-letter A–F diagram has a different vertical stack and a 14.7 g weight. Do not combine its dimensions with the detailed 9 g drawing or silently average them.

## What the detailed drawing establishes

| Feature | Drawing value |
|---|---:|
| Main blue gearbox boss | Ø11.8 mm |
| Shaft centre to far tip of small tail | 8.8 mm |
| Small tail width | 5.0 mm |
| Boss above rectangular case face | 4.0 mm |
| White shaft above boss | 3.2 mm |
| Shaft diameter | Ø4.6 mm |
| Rectangular case | 22.5 × 11.8 × 22.7 mm |
| Ear faces above case bottom | 15.9 and 18.4 mm |
| Case face beyond ear face toward shaft | 22.7 − 18.4 = **4.3 mm** |

The original hole is Ø14 mm, or 7 mm from its centre. The nominal tail reaches **1.8 mm beyond that radius**. The reference gauge retains the 14 mm circle and adds only a 6.4 mm-wide tail relief reaching 9.7 mm from the shaft centre. The added clearance is deliberate; it is not a measured dimension of the actual unit.

The current pedestals rise 4 mm above the hopper plate. On this reference drawing, seating the ears directly on them would put the rectangular case face approximately **0.3 mm into the plate**. Thus a tail notch alone may not solve the entire height stack. The existing pads also support only limited portions of the reference ear envelope. Candidate bridge spacers extend inward beneath the ears while remaining outside the reference case outline.

## Small test before touching the printed hopper

Download **[SG90_SMALL_FIT_TEST_KIT.3mf](../public/hardware/servo-fit/SG90_SMALL_FIT_TEST_KIT.3mf)**. It contains five tiny pieces: one 3 mm-thick boss gauge and near/far ear-bridge pairs in **1.0 mm** and **1.4 mm** heights. These are alternatives, not a stack. The file has geometry/layout only, not a filament preset.

Use A1 / the actual 0.4 mm nozzle, matching PETG preset, 0.20 mm layers, 3 walls, 5 top/bottom layers and no supports. Keep all parts flat as supplied. This is a few grams, not another large part. A successful slice does not confirm real fit.

With the servo unpowered and the horn removed, try the gauge over the blue boss. The round portion and tail must enter without force and the plate must sit square. A pass confirms only this clearance profile, not ear height, horn reach or gate function. If it does not fit, do not cut the original hopper; the actual unit needs further inspection.

Also test the supplied horn in the **existing gate recess** by itself. Do not alter the servo spline, blue case or horn socket to force a match.

## Conditional zero-full-reprint repair

Only after the small gauge fits:

1. Remove the hopper from the stand and keep all electronics disconnected. Orient the servo shaft-down as intended, with the tail/long case side pointing toward the pedestal farther from the hole. Use the actual part/gauge to mark the tail's interference; do not guess which side to cut.
2. With a fine hand file, gradually create **only the small tail notch** at the existing opening. The gauge profile is the limit/reference: 6.4 mm wide, no farther than 9.7 mm from the existing circle centre. This adds at most about 2.7 mm past the old rim on that side. Stop as soon as the real boss clears. **Do not enlarge the whole hole**, move its centre, cut the servo, remove the mounting pedestals, or cut the powder outlet. Avoid a freehand drill catching the edge of the existing hole.
3. Remove debris and rough edges. Keep filings out of the servo and powder path. If a notch would reach another feature or the printed part cracks, stop rather than forcing it.
4. Dry-fit the **1.0 mm bridge pair** on the original pedestals. The shorter piece goes on the pad nearer the hole; the longer piece on the farther pad. The inward extensions support the reference ears. They must not go under or touch the rectangular case body. Use a small piece of thin tape only to prevent sliding; tape thickness changes the stack.
5. Check that both ears sit flat, the case face clears the hopper plate, the complete boss enters the relief, and the shaft stays centred on the original hole. If the body still contacts the plate or the blue boss rubs the gate, try the **1.4 mm pair instead**, not on top. Use the lowest pair that gives clearance and still permits the supplied horn to seat fully. Do not keep adding height if the shaft cannot reach the horn.
6. Thread the two existing zip ties across the rectangular body using opposite slots at the same longitudinal position. Tighten evenly after checking the ears and spacers remain seated. Do not use tie force to bend the hopper, pull the servo through interference or press the boss against the gate.
7. Center the servo with the horn removed using the existing setup procedure. Disconnect external power again, then fit the horn/gate and supplied screw. The horn must engage the splines fully; do not use the screw to pull an unseated horn into place. Verify the gate has approximately 0.4–0.8 mm clearance from the hopper and no boss/horn interference. Recalibrate the actual assembly empty before adding flour.

If either bridge pair cannot satisfy both ear support and horn/gate seating, stop. These candidate dimensions are not enough for that unit; further photos/measurements or a different small adapter are needed. **A full stand reprint is not the next step.**

## What remains unverified

No physical check has yet been made with the user's servo. The purchased unit's exact boss, mounting geometry, shaft/horn engagement, spacer stability under vibration, and gate movement remain unverified. The small kit is explicitly a physical-fit test. It does not retroactively validate the original V3 files or establish that the whole dispenser works.


## Current V3.1 replacement: user declined a separate test print

The user explicitly requested a wider hole with relief margin rather than another test print. `scripts/build_replacement_hopper.py` produces `07_HOPPER_SG90_RELIEF_V3_1.stl` and the single-object `PRINT_THIS_HOPPER_ONLY_V3_1.3mf`. The original hopper and full plate are preserved as legacy geometry; do not print them to obtain the correction.

- Main opening Ø15 mm versus the reference boss Ø11.8 mm: 1.6 mm nominal radial relief.
- Tail opening 8 mm wide, reaching 11 mm from the unchanged shaft centre versus the reference 5 mm width and 8.8 mm reach: 2.2 mm extra end clearance.
- Both ear supports now end at z8 rather than z7, 5 mm above the flange, and extend beneath the reference ears. No separate bridge spacers are included or required by this revision.
- Original outlet, cone, flange outline, clip interfaces, tie slots and shaft centre remain unchanged. Keep all other printed parts.

Digital checks include a watertight single component, changes confined to the servo interface, nominal complete reference servo clearance, +1.5% boss XY clearance, gate sweep and stand clearance. These do not validate the purchased unit or its horn socket depth. The detailed supplied drawing is the dimensional reference; Tower Pro sources above do not establish the exact WWZMDiB variant. Assemble unpowered after printing and check the case, boss, horn seating and freely moving gate before operating.

Bambu Studio Generic PETG reference slice: 61.33 g, 8639 seconds (about 2 h 24 min), A1 0.4 mm, 0.20 mm layers, 3 walls, 5 top/bottom layers, 20% gyroid, no supports or brim, textured PEI. Use the matching preset for the actual PETG spool. The 3MF is geometry/layout only.

## 2026-11-09 shaft/horn review: print recommendation on hold

The V3.1 geometry has not changed. The earlier print recommendation is withdrawn: full horn seating remains unresolved. No separate test print is requested.

Hopper flange underside z0, upper surface z3; gate top z-0.6, horn arm recess floor z-4.0. Reference drawing calculations:

| Support raise | Case clearance above flange | Boss face z | Shaft tip z | Shaft tip below gate top |
|---|---:|---:|---:|---:|
| Original, 0 mm | -0.3 mm (interference) | -1.3 | -4.5 | 3.9 mm |
| V3.1, +1 mm | +0.7 mm | -0.3 | -3.5 | 2.9 mm |

Reach into the gate region does not establish spline engagement. The gate has a central through-hole, so the arm-recess floor is not the socket bottom. The actual horn socket entrance, axial stop and arm contact plane are needed. The animation used an assumed solid horn, without its socket.

The 1 mm raise is an allowance for the nominal 0.3 mm conflict, not a manufacturer requirement or proof of necessity for the actual servo. Online sources rechecked: Tower Pro SG90 Analog specification and Aus Electronics Direct TA0132 supplier drawing, including horn dimensions. Neither establishes the purchased WWZMDiB horn seating geometry. Do not combine their different variants as verified dimensions. See [calculation report](../public/hardware/servo-fit/shaft_stack_review.json).


## Current V3.2 best-effort repair (2026-11-09)

User authorized a best shot from available drawings, with no separate test print. The horn is installed after the servo is through the hopper; it never has to pass through the hopper opening. Their approximately 2 mm added horn height is an estimate with an unspecified datum. Do not silently turn it into a socket-depth specification.

V3.2 keeps the original ear height (4 mm over the flange). Instead of raising the servo, a 1 mm-deep local rectangular case recess leaves 2 mm of flange below it and provides nominal 0.7 mm body clearance. The boss opening is a modest diameter 14.4 mm, 6.6 mm tail width, tip reach 9.8 mm. Flange/clip/outlet interfaces and shaft XY location remain unchanged.

The replacement gate is 7.4 mm thick with a 37 x 12 mm horn arm pocket and 11.2 mm central through-hole, plus a 22 mm x 2 mm upper counter-relief for the stationary boss sweep. It checks both 32 and 35 x 10 x 2 mm arm envelopes. The hub OD allowance of 10 mm is assumed from the image, not a supplied dimension. The original 32 x 9 mm gate pocket is superseded; a new gate is required for this adjustable route.

The arm pocket floor is 1.4 mm above the gate bottom. Included packing rings 0.4/0.8/1.6 mm combine to 0...2.8 mm in 0.4 mm steps. Seat the real supplied horn completely first; select packing below its arms to obtain 0.4...0.8 mm gate gap. Packing lowers the gate without changing spline engagement. No need to invent a socket depth or partly unseat the horn. It is a finite adjustment allowance, not a guarantee. The included 0.6 mm strip is a removable assembly aid.

Nominal stack, hopper bottom z0: ear plane z7, case face z2.7, boss face z-1.3, shaft tip z-4.5. At 0.6 mm gate gap, gate top z-0.6, bottom z-8.0. For arm outer contact plane P and packing S, gate gap = S - P - 6.0 mm. The available S values cover P=-6.8...-3.6 at some gap in 0.4...0.8. Thus they accommodate 2.3 mm beyond to 0.9 mm short of the nominal bare shaft tip. If the user's 2 mm means arm outer face beyond shaft tip, P=-6.5, S=0 yields a 0.5 mm gap. If it refers to another face, that example is invalid.

Validated digitally: watertight connected pieces, plate bounds and separation, change confined to servo interface, nominal complete servo clearance, +1.5% boss XY envelope, gate sweep at 0.4/0.6/0.8 mm gaps against hopper/servo/stand, both horn arm envelopes and packing combinations, outlet open/closed coverage. Full horn socket geometry is not modeled; actual horn seating is preserved by assembly order, with bounded gate adjustment. Physical PETG fit, clip force, motor input logic, electronics supply, flour flow/leakage and robot pickup remain unverified. No stand reprint or new electronics is called for.

Source lookup refreshed before modeling: [Tower Pro manufacturer specifications](https://towerpro.com.tw/product/sg90-analog/) and [TA0132 supplier drawings](https://www.auselectronicsdirect.com.au/assets/brochures/TA0132.pdf). Neither is treated as a verified WWZMDiB drawing. Detailed user-provided servo dimensions drive the reference model; the latest user image drives the larger horn-arm envelope. The earlier 360-degree label is not treated as proof of the actual purchased servo type.

Generic PETG A1 0.4 slice: 86.64 g / 12129 seconds (~3 h 22 min), 6 objects, no supports, 0.20 mm layers, 3 walls, 5 top/bottom, 20% gyroid, textured PEI. See the current report and repair guide.

V3.2 tie-routing review: hopper has 3.6 x 18 x 1.2 mm longitudinal underside channels for same-side slot pairs. The 3.6 mm channel roof is a short bridge in the flange-down print orientation. Gate tie bands moved to x=+/-13 mm, outside the stationary boss envelope, with upper grooves down to the horn-pocket floor and lower 0.6 mm grooves. Explicit 2.5 x 0.8 mm tie envelopes clear the gate and nominal servo sweep. Actual tie dimensions and restraint force remain unverified; upper servo runs must bear on case side edges rather than cross the shaft.
