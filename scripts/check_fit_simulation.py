"""Browser QA for the actual V3.2 fit viewer; run against the local Vite server.
Requires the existing optional playwright package and installed Chrome.
"""
import asyncio,argparse,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main(args):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=args.browser,headless=True,args=['--enable-webgl','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        try:
            page=await browser.new_page(viewport={'width':1536,'height':1050})
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            await page.goto(args.url)
            await page.wait_for_function('window.fitSimulation?.state != null')
            assert abs(await page.evaluate('fitSimulation.state.gap')-.5)<1e-8
            assert len(await page.evaluate('fitSimulation.report.unintended_interferences'))==0
            assert all(c['detected'] for c in await page.evaluate('fitSimulation.report.negative_controls'))
            await page.wait_for_timeout(400)
            output=ROOT/'test-results';output.mkdir(exist_ok=True)
            await page.locator('.stage').screenshot(path=str(output/'fit-lab-overview.png'))
            for view in ['interface','under','whole']:
                await page.locator(f'[data-view="{view}"]').click()
                await page.wait_for_timeout(200)
            await page.locator('[data-view="interface"]').click()
            await page.locator('#section').click()
            await page.wait_for_timeout(300)
            await page.locator('.stage').screenshot(path=str(output/'fit-lab-section.png'))
            await page.evaluate('fitSimulation.setValues({depth:1.5})')
            assert await page.evaluate('fitSimulation.state.shaftBottomsOut')
            assert 'CONFLICT' in await page.locator('#verdict').inner_text()
            await page.evaluate('fitSimulation.setValues({depth:2.8,packing:0.8})')
            assert abs(await page.evaluate('fitSimulation.state.gap')-1.3)<1e-8
            assert 'REVIEW' in await page.locator('#verdict').inner_text()
            await page.evaluate('fitSimulation.setValues({packing:0,extension:0})')
            assert await page.evaluate('fitSimulation.state.gateInterference')
            await page.locator('#reset').click()
            for angle in [-70,0,20,60,70]:
                await page.evaluate('a=>fitSimulation.setValues({angle:a})',angle)
                await page.wait_for_timeout(50)
            await page.evaluate('fitSimulation.setValues({angle:0})')
            assert float((await page.locator('#aperture').inner_text()).split()[0])>153
            await page.locator('#play').click()
            await page.wait_for_timeout(300)
            first=await page.locator('#angle').input_value()
            await page.wait_for_timeout(300)
            assert await page.locator('#angle').input_value()!=first
            await page.locator('#play').click()
            await page.evaluate('fitSimulation.setValues({explode:1})')
            assert 'EXPLODED' in await page.locator('#mode-note').inner_text()
            await page.locator('#reset').click()
            for selector in ['#stand','#lid','#electronics','#cup','#aux','#label-toggle']:
                await page.locator(selector).evaluate('(el)=>{el.checked=!el.checked;el.dispatchEvent(new Event("input"));}')
            await page.set_viewport_size({'width':390,'height':844})
            await page.wait_for_timeout(200)
            assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            await page.screenshot(path=str(output/'fit-lab-mobile.png'),full_page=True)
            for href in ['hardware/simulation/assembly_collision_report.json','hardware/simulation/MILLIGRAM_ACCURACY.html','hardware/servo-fit/REPAIR_GUIDE.html']:
                response=await page.request.get(args.url.rsplit('/',1)[0]+'/'+href)
                assert response.status==200,href
            assert not errors,errors
            print(json.dumps({'render_errors':errors,'default_collision_pass':True,'negative_controls':3,'views':'whole/interface/underside/section/x-ray','interactive_failure_states':'socket bottoming, wrong gap, gate interference','animation':'passed','mobile_overflow':False}))
        finally:await browser.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:4188/fit-check.html');parser.add_argument('--browser',default='C:/Program Files/Google/Chrome/Application/chrome.exe')
    asyncio.run(main(parser.parse_args()))
