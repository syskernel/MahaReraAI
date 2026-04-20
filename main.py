from playwright.async_api import async_playwright
import asyncio
import pandas as pd

df = pd.read_excel("RERA_Mar.xlsx")

async def total_apartments(pg):
    await pg.wait_for_timeout(2000)
    cells = await pg.locator("//th[text()='Total']").count()
    direct = (await pg.locator("//th[text()='Total']/following-sibling::th[3]").inner_text())
    if cells == 0:
        return "N/A"
    else:
        return direct

async def fetch_data(page, context):
    await page.locator("//a[text()='View Details']").click()
    await page.locator("//button[text()='Yes']").wait_for()
    async with context.expect_page() as new_page_info:
        await page.locator("//button[text()='Yes']").click()
    
    new_page = await new_page_info.value
    await new_page.wait_for_load_state("domcontentloaded")
    print(new_page.url)
    date = (await new_page.locator("//label[text()='Date of Registration']/following-sibling::label[1]").inner_text()).strip()
    type = (await new_page.locator("//div[text()=' Project Type ']/following-sibling::div[1]").inner_text()).strip()
    print(date)
    print(type)
    apartment = await total_apartments(new_page)
    print("no: ", apartment)

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
            #await page.locator("//a[text()='View Details']").click()

            command = await asyncio.to_thread(input, "Enter command: ")
            if command == "next":
                continue
            elif command == "fetch":
                await fetch_data(page, context)

        await context.close()
        await browser.close()

asyncio.run(main())