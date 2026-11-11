"""Check the deployed/local numbered wiring guide; requires optional Playwright."""
import asyncio,argparse,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def run(url):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        try:
            page=await browser.new_page(viewport={'width':1536,'height':1000})
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            await page.goto(url);await page.wait_for_function('window.wiringGuide?.wires.length===11')
            assert await page.locator('#wire-table tr').count()==11
            await page.locator('#prev').click();assert await page.locator('#wire-select').input_value()=='W11'
            for i in range(1,12):
                wire=f'W{i:02}'
                await page.locator('#wire-select').select_option(wire)
                assert await page.locator('#overview .selected').count()==1
                assert await page.locator('#overview .faded').count()==10
                assert wire in await page.locator('#step').inner_text()
            assert 'LEAVE DISCONNECTED' in await page.locator('#step').inner_text()
            await page.locator('#all').click();assert await page.locator('#overview .faded').count()==0
            await page.locator('#overview').screenshot(path=str(ROOT/'test-results/wiring-all.png'))
            await page.locator('img[src="breadboard.svg"]').screenshot(path=str(ROOT/'test-results/wiring-breadboard.png'))
            for relative in ['wires.json','breadboard.svg','end_to_end.svg','netlist_check.json','../servo-fit/REPAIR_GUIDE.html','../../fit-check.html']:
                response=await page.request.get(url.rsplit('/',1)[0]+'/'+relative)
                assert response.status==200,relative
            await page.set_viewport_size({'width':390,'height':844})
            assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            await page.screenshot(path=str(ROOT/'test-results/wiring-mobile.png'),full_page=True)
            assert not errors,errors
            print(json.dumps({'wires':11,'individual_highlights':11,'conditional_W11_notice':True,'mobile_overflow':False,'page_errors':errors}))
        finally:await browser.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:4188/hardware/wiring/WIRING_GUIDE.html')
    asyncio.run(run(parser.parse_args().url))
