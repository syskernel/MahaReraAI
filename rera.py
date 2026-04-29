from playwright.async_api import async_playwright
import asyncio
import pandas as pd

projects = []

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"height":800, "width":1280})
        page = await context.new_page()

        await page.set_extra_http_headers({
            "Accept-language": "en=US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        })

        await page.goto("https://maharera.maharashtra.gov.in/", timeout=30000)
        await page.wait_for_load_state("networkidle")

        await page.locator("a.btn.btn-danger.advBtn").nth(0).click()
        await page.locator("input#date.form-control.border-0.datepickerNew.form-text.hasDatepicker").fill("31-12-2026") 
        await page.locator("select#edit-project-division.form-select").select_option(value='5') 
        await page.wait_for_load_state("load")
        await page.locator("select#edit-project-district.form-select").select_option(value='521')
        await page.locator("input#edit-submit--2.btn-default.me-2.button.js-form-submit.form-submit").click()
        await page.wait_for_timeout(10000)

        n = 1
        while True:
            print(f"Currently on page {n}")
            await page.wait_for_selector("p.p-0")
            id_list = page.locator("p.p-0")
            name_list = page.locator("h4.title4")
            name_l = name_list.locator(":scope > strong")
            promoter_list = page.locator("p.darkBlue.bold")
            count = await id_list.count()
            print(f"Found {count} projects on this page")
            for i in range(count):
                num = (await id_list.nth(i).inner_text()).strip()
                name = (await name_l.nth(i).inner_text()).strip()
                promoter = (await promoter_list.nth(i).inner_text()).strip()
                projects.append({
                    "PROJECT NAME": name,
                    "RERA NUMBER": num,
                    "PROMOTER NAME": promoter
                })

            next_btn = page.locator("a.next")
            if await next_btn.is_visible():
                await next_btn.click()
                n += 1
            else:
                print("No more pages")
                break
        print("Script completed!")

        await context.close()
        await browser.close()
asyncio.run(main())

df = pd.DataFrame(projects)
df.to_excel("Rera_Dec.xlsx", index=False)