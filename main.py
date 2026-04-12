from playwright.async_api import async_playwright
import asyncio
import pandas as pd

df = pd.read_excel("RERA_Mar.xlsx")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"height": 800, "width": 1280})
        page = await context.new_page()
        await page.set_extra_http_headers({
            "Accept-language": "en=US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        })

        await page.goto("https://maharera.maharashtra.gov.in/", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.locator("a.btn.btn-danger.advBtn").nth(0).click()

        for i,row in df.iterrows():
            rera_num = row["RERA NUMBER"]
            await page.locator("input#edit-project-name.leftBdrRadius.form-text").fill(rera_num) 
            await page.wait_for_load_state("load")
            await page.locator("input#edit-submit--2.btn-default.me-2.button.js-form-submit.form-submit").click()
            await page.locator("//a[text()='View Details']").click()

            command = await asyncio.to_thread(input, "Enter command: ")
            if command == "next":
                print("Reached here!")
                #reset
                #await page.locator
                continue
            elif command == "fetch":
                print(page.url)

        await context.close()
        await browser.close()

asyncio.run(main())