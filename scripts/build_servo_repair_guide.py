from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/hardware/servo-fit'
OUT.mkdir(parents=True,exist_ok=True)
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="580" viewBox="0 0 1050 580">
<style>text{font:17px Arial,sans-serif;fill:#293f34}.title{font-size:27px;font-weight:bold}.small{font-size:14px}</style>
<rect width="1050" height="580" fill="#f5f3ed"/>
<text x="35" y="42" class="title">SG90 repair candidate · keep the existing hopper</text>
<rect x="168" y="124" width="144" height="72" fill="#d8c5a1" stroke="#7d6844"/>
<rect x="168" y="420" width="144" height="72" fill="#d8c5a1" stroke="#7d6844"/>
<rect x="168" y="124" width="144" height="85.6" fill="none" stroke="#4d8297" stroke-width="3"/>
<rect x="168" y="398.4" width="144" height="93.6" fill="none" stroke="#4d8297" stroke-width="3"/>
<circle cx="240" cy="312" r="25.6" fill="#a8cdb5"/><rect x="214.4" y="260" width="51.2" height="52" fill="#a8cdb5"/>
<circle cx="240" cy="260" r="56" fill="#f5f3ed" stroke="#bc684e" stroke-width="3" stroke-dasharray="6 4"/>
<circle cx="240" cy="260" r="47.2" fill="none" stroke="#456b8a" stroke-width="2"/>
<circle cx="240" cy="310.4" r="20" fill="none" stroke="#456b8a" stroke-width="2"/>
<path d="M240 180v182M158 260h164" stroke="#839581" stroke-dasharray="3 4"/>
<text x="33" y="111" class="small">Near pad</text><path d="M112 108L168 150" stroke="#61745f"/>
<text x="35" y="522" class="small">Far pad / long case side</text><path d="M203 509L220 477" stroke="#61745f"/>
<text x="365" y="220" class="small">Original hole: Ø14 mm</text><path d="M355 218L294 235" stroke="#bc684e"/>
<text x="365" y="310" class="small">Relief: 6.4 mm wide</text><path d="M353 307L264 321" stroke="#55846b"/>
<text x="365" y="338" class="small">Tip: 9.7 mm from centre</text>
<text x="540" y="110" font-weight="bold">Test the tiny gauge before filing.</text>
<text x="540" y="151">Red dashed circle: existing opening</text>
<text x="540" y="183">Green: candidate tail relief only</text>
<text x="540" y="215">Blue outlines: candidate ear bridges</text>
<text x="540" y="267">The tail points toward the farther pad.</text>
<text x="540" y="299">Keep the original hole centre.</text>
<text x="540" y="331">Do not enlarge the entire circle.</text>
<text x="540" y="385">Spacers: 1.0 mm or 1.4 mm pairs.</text>
<text x="540" y="417">Use one pair, not both stacked.</text>
<text x="540" y="449">Case, boss, horn and gate must all clear.</text>
<text x="35" y="558" class="small">Reference drawing only; purchased servo not verified. Illustration is not a 1:1 cutting template. Actual dry fit is required.</text>
</svg>'''
(OUT/'repair_reference.svg').write_text(svg,encoding='utf-8')
estimate='a few grams'
report=OUT/'slicer_check.json'
if report.exists():
    data=json.loads(report.read_text())
    estimate=f"{data['predicted_grams']:.2f} g / about {round(data['predicted_seconds']/60)} minutes with the Generic PETG reference preset"
html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SG90 fit repair · keep your printed parts</title>
<style>body{{font:16px system-ui;line-height:1.65;background:#f5f3ed;color:#293f34;max-width:960px;margin:35px auto;padding:0 22px}}h1,h2{{line-height:1.2}}h1{{font-size:38px}}aside{{padding:16px 20px;border-left:4px solid #b95c40;background:#eee4d7}}a{{color:#a4462b}}img{{width:100%;height:auto}}li{{margin:12px 0}}.button{{display:inline-block;background:#304b3c;color:white;padding:12px 18px;border-radius:5px;margin:12px 0}}code{{font-size:14px}}@media print{{body{{font-size:11px}}.button{{display:none}}}}</style>
<h1>Keep your printed parts.<br>Test the SG90 interface first.</h1>
<aside><strong>The original V3 servo opening has a known fit problem.</strong> It models only a circle and misses the gearbox tail. The mounting-height stack also needs checking. Do not reprint the stand or original full plate. The older assembly animation/video is not a verified servo-fit reference.</aside>
<p>The detailed drawing you supplied has an Ø11.8 mm round boss, a 5 mm-wide tail reaching 8.8 mm from the shaft centre, and a case face 4.3 mm beyond the mounting-ear face. My hole reaches only 7 mm from centre and the existing pads rise 4 mm above the plate. These are two separate interference risks.</p>
<h2>Print only the small diagnostic kit</h2>
<a class="button" href="SG90_SMALL_FIT_TEST_KIT.3mf" download>Download the small SG90 fit-test kit</a>
<p>Five tiny parts: a 3 mm-thick profile gauge and two candidate near/far ear-bridge pairs, 1.0 and 1.4 mm thick. Estimate: <strong>{estimate}</strong>. Choose your actual A1 0.4 mm nozzle, matching PETG preset and textured plate, 0.20 mm layers, 3 walls, 5 top/bottom layers, supports off, brim none. Keep all pieces flat as supplied. The 3MF contains geometry/layout only.</p>
<p><strong>This kit is a fit test, not a guaranteed repair.</strong> It uses the supplied detailed drawing, not measurements of your exact WWZMDiB servo. The horn socket depth is unknown. No physical fit has been established yet.</p>
<ol><li>With the servo unpowered and horn removed, check that the complete boss enters the small gauge without force and the plate sits square. If it does not, do not alter the printed hopper.</li>
<li>Check your supplied double-arm horn in the existing gate recess by itself. Keep the original servo, horn and spline intact.</li>
<li>If the gauge fits, mark only the tail's interference on the existing hopper. A small hand-file relief may salvage it: the candidate profile is 6.4 mm wide, ending 9.7 mm from the original shaft centre, on the tail side. Do not enlarge the whole circle or move its centre. Stop as soon as the actual boss clears.</li>
<li>Try the 1.0 mm bridge pair on the existing pedestals: short piece on the nearer pad, long piece on the farther pad. Both ears must sit flat, with no spacer/body collision. The 1.4 mm pair is an alternative if needed, not another layer to stack.</li>
<li>The case must clear the hopper plate, the boss must clear the gate, and the shaft must still reach a fully seated horn. Use the lowest pair that satisfies all three. Do not use zip ties or the horn screw to pull interfering parts into place.</li>
<li>Only after the dry fit works, follow servo centering with the horn removed, then disconnect external power to install the horn/gate. Check free clearance and recalibrate empty. If these checks cannot all pass, stop and inspect the actual part further; another full stand print is not the solution.</li></ol>
<img src="repair_reference.svg" alt="Existing round opening, candidate tail relief and near/far ear bridge positions">
<p>The relief adds at most about 2.7 mm beyond the old rim on one side. It is deliberately larger than the drawing's nominal tail to provide test clearance. It must not be treated as a measured profile of the purchased unit.</p>
<p><a href="https://github.com/dylanler/flour-dispenser-assembly/blob/main/docs/SERVO_FIT_AUDIT.md">Detailed dimensional audit and repair checks</a> · <a href="fit_test_report.json">Reference model report</a> · <a href="slicer_check.json">PETG slicing report</a></p>
</html>'''
(OUT/'REPAIR_GUIDE.html').write_text(html,encoding='utf-8')
print('Created repair guide and reference illustration.')
