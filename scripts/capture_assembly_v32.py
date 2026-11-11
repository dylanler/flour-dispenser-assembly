"""Capture current assembly figures and optionally record the current video."""
from pathlib import Path
import argparse,asyncio,json
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def run(args):
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,args=['--enable-webgl','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
        try:
            page=await browser.new_page(viewport={'width':1536,'height':1100},accept_downloads=True)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            await page.goto(args.url);await page.wait_for_function('window.assembly !== undefined')
            assert await page.evaluate('assembly.geometryVersion')=='V3.2'
            paths=await page.evaluate('assembly.model.loadedPaths')
            assert any('08_HOPPER' in x for x in paths) and any('09_GATE' in x for x in paths)
            assert not any('02_hopper' in x or '03_rotary' in x for x in paths)
            ids=await page.evaluate('assembly.model.wireIDs')
            assert all(f'W{i:02}' in ids for i in range(1,12)) and len(ids)==12
            await page.evaluate('document.body.classList.add("large")')
            out=ROOT/'public/hardware/assembly-v3-2';out.mkdir(exist_ok=True)
            for i in range(17):
                await page.evaluate('i=>{assembly.play(false);assembly.step(i,.86);}',i)
                await page.wait_for_timeout(180)
                if i==9:assert not await page.evaluate('assembly.model.components.hornRoot.visible')
                if i==10:
                    assert await page.evaluate('assembly.model.components.hornRoot.visible')
                    assert not await page.evaluate('assembly.model.components.gateRoot.visible')
                if i==11:
                    assert await page.evaluate('assembly.model.components.gateRoot.visible')
                    assert abs(await page.evaluate('assembly.model.components.gateRoot.position.y')+7.9)<1e-8
                if i in [5,6,7,14]:assert await page.locator('#wiring-overlay').is_visible()
                await page.locator('#viewer').screenshot(path=str(out/f'step-{i+1:02}.png'))
            manifest={'version':'V3.2','steps':17,'actual_print_meshes':paths,'jumper_ids':ids,'checked':'Horn absent at centering; fully seated horn shown before gate; current gate default pose; four numbered wiring stages','physical_fit_verified':False,'video_speed':2 if args.record or (ROOT/'public/flour-v3-2-assembly.webm').exists() else None}
            (out/'assembly_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
            await page.evaluate('assembly.step(11,.30)')
            await page.wait_for_timeout(180)
            await page.locator('#viewer').screenshot(path=str(out/'gate-approach.png'))
            if args.record:
                await page.locator('#speed').select_option('2');await page.locator('#speed').dispatch_event('change')
                async with page.expect_download(timeout=420000) as download:
                    await page.locator('#record').click()
                    for _ in range(80):
                        await page.wait_for_timeout(5000)
                        current=await page.evaluate('assembly.time');duration=await page.evaluate('assembly.totalDuration')
                        print(f'V3.2 recording: {current:.1f}/{duration:.1f}s',flush=True)
                        if current>=duration:break
                    video=await download.value
                await video.save_as(str(ROOT/'public/flour-v3-2-assembly.webm'))
            assert not errors,errors
            print('All 17 current assembly figures captured; ordering/mesh/wiring checks passed.')
        finally:await browser.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:4188/');parser.add_argument('--record',action='store_true')
    asyncio.run(run(parser.parse_args()))
