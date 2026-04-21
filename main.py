from playwright.async_api import async_playwright
import asyncio
import pandas as pd

df = pd.read_excel("RERA_Mar.xlsx")

async def project_address(pg):
    await pg.wait_for_timeout(2000)
    cell1 = await pg.locator("//label[text()='Address']").count()
    if cell1 != 0:
        address = (await pg.locator("//label[text()='Address']/following-sibling::div/div").inner_text()).strip()

    cell2 = await pg.locator("//label[text()='Street Name']").count()
    if cell2 != 0:
        street = (await pg.locator("//label[text()='Street Name']/following-sibling::div/div").inner_text()).strip()

    cell3 = await pg.locator("//label[text()='Locality']").count()
    if cell3 != 0:
        locality = (await pg.locator("//label[text()='Locality']/following-sibling::div/div").inner_text()).strip()

    cell4 = await pg.locator("//label[text()=' Taluka ']").count()
    if cell4 != 0:
        taluka = (await pg.locator("//label[text()=' Taluka ']/following-sibling::div/div").first.inner_text()).strip()

    cell5 = await pg.locator("//label[text()=' Village ']").count()
    if cell5 != 0:
        village = (await pg.locator("//label[text()=' Village ']/following-sibling::div/div").first.inner_text()).strip()

    cell6 = await pg.locator("//label[text()=' District ']").count()
    if cell6 != 0:
        district = (await pg.locator("//label[text()=' District ']/following-sibling::div/div").first.inner_text()).strip()

    cell7 = await pg.locator("//label[text()=' Pin Code ']").count()
    if cell7 != 0:
        pin_code = (await pg.locator("//label[text()=' Pin Code ']/following-sibling::div/div").first.inner_text()).strip()
    
    add = f"{address}, {street}, {locality}, taluka-{taluka}, village-{village}, district-{district} {pin_code}"
    return add

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
    date = (await new_page.locator("//label[text()='Date of Registration']/following-sibling::label[1]").inner_text()).strip()
    type = (await new_page.locator("//div[text()=' Project Type ']/following-sibling::div[1]").inner_text()).strip()
    apartment = await total_apartments(new_page)
    add = await project_address(new_page)
    print(new_page.url)
    print(date)
    print(type)
    print("no: ", apartment)
    print(f"Address: {add}")

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