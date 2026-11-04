"""Optional browser QA and reproducible video recording; run against npm run dev.

pip install playwright
python -m playwright install chromium
python scripts/browser_check.py [--record]
"""
import argparse
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


async def run(args):
    async with async_playwright() as p:
        options = dict(headless=True, args=['--enable-webgl', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-background-timer-throttling', '--disable-renderer-backgrounding'])
        if args.browser: options['executable_path'] = args.browser
        browser = await p.chromium.launch(**options)
        try:
            page = await browser.new_page(viewport=dict(width=1536, height=1050), accept_downloads=True)
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            await page.goto(args.url)
            await page.wait_for_function('window.assembly !== undefined')
            for i in range(17):
                await page.locator('#chapter-list button').nth(i).click()
                assert await page.locator('#step-title').inner_text()
                assert await page.locator('#scene-error').is_hidden()
            await page.locator('#play').click()
            previous = await page.evaluate('assembly.time')
            await page.wait_for_timeout(400)
            assert await page.evaluate('assembly.time') > previous
            await page.locator('#play').click()
            await page.set_viewport_size(dict(width=390, height=844))
            await page.wait_for_timeout(200)
            assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            output = ROOT / 'test-results'
            output.mkdir(exist_ok=True)
            await page.screenshot(path=str(output / 'mobile.png'), full_page=True)
            await page.set_viewport_size(dict(width=1536, height=1050))
            await page.screenshot(path=str(output / 'desktop.png'), full_page=True)
            if args.record:
                async with page.expect_download(timeout=420000) as event:
                    await page.locator('#record').click()
                    duration = await page.evaluate('assembly.totalDuration')
                    for _ in range(70):
                        await page.wait_for_timeout(5000)
                        current = await page.evaluate('assembly.time')
                        print('Recording %.1f / %.1f seconds' % (current, duration), flush=True)
                        if current >= duration: break
                    download = await event.value
                await download.save_as(str(ROOT / 'public/flour-v3-assembly.webm'))
            assert not errors, errors
            print('Browser checks passed.')
        finally: await browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:5173/')
    parser.add_argument('--browser', help='Optional path to installed Chrome/Chromium')
    parser.add_argument('--record', action='store_true')
    asyncio.run(run(parser.parse_args()))
