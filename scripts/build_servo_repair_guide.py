from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/hardware/servo-fit'
OUT.mkdir(parents=True,exist_ok=True)
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="440" viewBox="0 0 900 440">
<style>text{font:18px Arial,sans-serif;fill:#293f34}.title{font-size:26px;font-weight:bold}</style><rect width="900" height="440" fill="#f5f3ed"/>
<text x="30" y="42" class="title">V3.1 · enlarged opening and integrated ear supports</text>
<rect x="120" y="85" width="180" height="55" fill="#d8c5a1"/><rect x="120" y="335" width="180" height="65" fill="#d8c5a1"/>
<path d="M135 220a75 75 0 1 1 115 63v7a40 40 0 0 1-80 0v-7a75 75 0 0 1-35-63" fill="#a8cdb5" stroke="#456b8a" stroke-width="3"/>
<path d="M210 125v220M110 220h200" stroke="#839581" stroke-dasharray="4 4"/>
<text x="370" y="125">Main opening: Ø15 mm</text><text x="370" y="165">Tail width: 8 mm</text><text x="370" y="205">Centre to tail tip: 11 mm</text><text x="370" y="245">Extra tail reach over drawing: 2.2 mm</text><text x="370" y="300">Both ear supports raised 1 mm</text><text x="370" y="340">No separate printed spacers</text><text x="30" y="428">Reference diagram only; not a cutting template or physical fit validation.</text></svg>'''
(OUT/'repair_reference.svg').write_text(svg,encoding='utf-8')
estimate='about 61 g / 2 hours 24 minutes'
report=OUT/'replacement_hopper_slicer.json'
if report.exists():
    data=json.loads(report.read_text())
    estimate=f"{data['predicted_grams']:.2f} g / about {round(data['predicted_seconds']/60)} minutes"
html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V3.1 · replacement hopper only</title>
<style>body{{font:16px system-ui;line-height:1.65;background:#f5f3ed;color:#293f34;max-width:960px;margin:35px auto;padding:0 22px}}h1,h2{{line-height:1.2}}h1{{font-size:38px}}aside{{padding:16px 20px;border-left:4px solid #b95c40;background:#eee4d7}}a{{color:#a4462b}}img{{width:100%;height:auto}}li{{margin:12px 0}}.button{{display:inline-block;background:#304b3c;color:white;padding:12px 18px;border-radius:5px;margin:12px 0}}@media print{{body{{font-size:11px}}.button{{display:none}}}}</style>
<h1>Print only the corrected hopper.</h1>
<aside><strong>Keep the stand, gate, lid and both clips.</strong> This V3.1 replacement enlarges the servo opening and integrates the ear-height correction. The original full plate still contains the faulty hopper; do not print it again for this repair.</aside>
<a class="button" href="PRINT_THIS_HOPPER_ONLY_V3_1.3mf" download>Download the hopper-only 3MF</a>
<p>Alternative: <a href="07_HOPPER_SG90_RELIEF_V3_1.stl" download>replacement hopper STL</a>. Both contain the same corrected geometry. No separate test print is required for this chosen route. The 3MF contains one object and its flat orientation/layout, without printer or filament presets.</p>
<h2>Bambu Studio settings</h2>
<p>Select <strong>Bambu Lab A1 / 0.4 mm nozzle</strong>, textured PEI plate, and the PETG preset matching your spool. Use <strong>0.20 mm Standard</strong>, 3 walls, 5 top and 5 bottom layers, 20% gyroid, supports off, brim none. Keep the large flat flange on the bed, funnel pointing up. Reference Generic PETG slice: <strong>{estimate}</strong>; actual PETG HF estimates may differ. Preview the slice before sending.</p>
<h2>What changed</h2>
<ul><li>The main round opening is now Ø15 mm, with an 8 mm-wide tail reaching 11 mm from the unchanged shaft centre. The supplied drawing shows an Ø11.8 mm boss and a 5 mm-wide tail reaching 8.8 mm: this adds 1.6 mm nominal radial clearance and 2.2 mm extra tail reach.</li>
<li>Both ear supports are raised 1 mm and extended under the reference ears. This addresses the case-to-flange interference in the original height stack. Do not add the older diagnostic spacer bridges to this hopper.</li>
<li>The flange outline, outlet, cone, tie slots, shaft centre and stand/clip interfaces are unchanged.</li></ul>
<img src="repair_reference.svg" alt="Replacement hopper servo interface with enlarged round opening, gearbox tail relief and raised ear supports">
<h2>Swap the hopper</h2>
<ol><li>Empty the dispenser and disconnect the brick and ESP32 USB cable. Photograph the existing wiring. Remove the horn screw, gate and servo gently; do not force the shaft or gearbox.</li>
<li>Release both locking clips and lift out the old hopper. Transfer the servo and vibration module to the new hopper. With the horn removed, insert the complete blue gearbox boss through the opening, tail toward the longer case side and farther ear support. Both ears must rest squarely on the supports; attach using the original tie positions.</li>
<li>Before power, check that the servo case clears the flange. Check the supplied horn fits the existing gate recess and seats fully on its spline. Do not tighten the screw or ties to pull an interference into place.</li>
<li>Seat the replacement hopper in the existing stand and reinstall both clips. Keep wiring outside the scale bay. Retain the original lid.</li>
<li>Center the servo using the existing software with the horn removed. Disconnect external power before installing the horn and gate at the calibrated closed position. Check the gate turns without rubbing the boss or hopper; do not force the servo by hand. Recheck clearance through a small empty powered movement before flour, then recalibrate opening and closing limits.</li></ol>
<aside><strong>Drawing-based revision, not physically verified.</strong> The detailed SG90 drawing supplied by you is the reference; it is not established as a drawing of your exact WWZMDiB servo. The supplied horn socket depth and actual assembled height remain unmeasured. The unpowered checks above are part of assembly, not a request for another test print. If something still catches, stop before powering.</aside>
<p>The digital checks cover a watertight connected mesh, changes confined to the servo interface, reference-case/ear/boss/shaft clearance, a +1.5% boss XY envelope, gate sweep and stand clearance. Slicing does not prove physical fit.</p>
<p><a href="replacement_hopper_report.json">Geometry report</a> · <a href="replacement_hopper_slicer.json">PETG slicing report</a> · <a href="https://github.com/dylanler/flour-dispenser-assembly/blob/main/docs/SERVO_FIT_AUDIT.md">Sources and dimensional audit</a></p>
<p>The older <a href="SG90_SMALL_FIT_TEST_KIT.3mf">small diagnostic kit</a> remains optional for a hand-fit salvage route; it is not needed for printing this replacement. The old assembly animation remains an illustrative reference and shows the original simplified servo.</p></html>'''
(OUT/'REPAIR_GUIDE.html').write_text(html,encoding='utf-8')
print('Created V3.1 hopper-only replacement guide.')
