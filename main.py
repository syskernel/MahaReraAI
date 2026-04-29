from playwright.async_api import async_playwright
import asyncio
import pandas as pd
import os

projects = []

df = pd.read_excel("Rera_Dec.xlsx")

def save_file():
    filename = "RERAFINAL.xlsx"
    new_df = pd.DataFrame(projects)
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.drop_duplicates(subset=["RERA NUMBER"], inplace=True)
        updated_df.to_excel(filename, index=False)
        print("Data appended successfully!")
    else:
        new_df.to_excel(filename, index=False)
        print("File created and saved successfully!")

async def project_address(pg):
    await pg.wait_for_timeout(2000)
    add = ""
    try:
        cell1 = await pg.locator("//label[text()='Address']").count()
        if cell1 != 0:
            address = (await pg.locator("//label[text()='Address']/following-sibling::div/div").inner_text()).strip()
            add += f"{address}, "
        cell2 = await pg.locator("//label[text()='Street Name']").count()
        if cell2 != 0:
            street = (await pg.locator("//label[text()='Street Name']/following-sibling::div/div").inner_text()).strip()
            add += f"{street}, "
        cell3 = await pg.locator("//label[text()='Locality']").count()
        if cell3 != 0:
            locality = (await pg.locator("//label[text()='Locality']/following-sibling::div/div").inner_text()).strip()
            add += f"{locality}, "
        cell4 = await pg.locator("//label[text()=' Taluka ']").count()
        if cell4 != 0:
            taluka = (await pg.locator("//label[text()=' Taluka ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"taluka-{taluka}, "
        cell5 = await pg.locator("//label[text()=' Village ']").count()
        if cell5 != 0:
            village = (await pg.locator("//label[text()=' Village ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"village-{village}, "
        cell6 = await pg.locator("//label[text()=' District ']").count()
        if cell6 != 0:
            district = (await pg.locator("//label[text()=' District ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"district-{district} "
        cell7 = await pg.locator("//label[text()=' Pin Code ']").count()
        if cell7 != 0:
            pin_code = (await pg.locator("//label[text()=' Pin Code ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"{pin_code}"
        return add
    except Exception as e:
        print(f"Couldn't find project address: {e}")

async def promoter_address(pg):
    add = ""
    await pg.wait_for_timeout(2000)
    try:
        cell1 = await pg.locator("//label[text()=' Unit Number ']").count()
        if cell1 != 0:
            unit = (await pg.locator("//label[text()=' Unit Number ']/following-sibling::div/div").inner_text()).strip()
            add += f"{unit} "
        cell2 = await pg.locator("//label[text()=' Building Name ']").count()
        if cell2 != 0:
            building = (await pg.locator("//label[text()=' Building Name ']/following-sibling::div/div").inner_text()).strip()
            add += f"{building}, "
        cell3 = await pg.locator("//label[text()=' Street Name ']").count()
        if cell3 != 0:
            street = (await pg.locator("//label[text()=' Street Name ']/following-sibling::div/div").inner_text()).strip()
            add += f"{street}, "
        cell4 = await pg.locator("//label[text()=' Locality ']").count()
        if cell4 != 0:
            locality = (await pg.locator("//label[text()=' Locality ']/following-sibling::div/div").inner_text()).strip()
            add += f"{locality}, "
        cell5 = await pg.locator("//label[text()=' Taluka ']").count()
        if cell5 != 0:
            taluka = (await pg.locator("//label[text()=' Taluka ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"taluka-{taluka},  "
        cell6 = await pg.locator("//label[text()=' Village ']").count()
        if cell6 != 0:
            village = (await pg.locator("//label[text()=' Village ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"village-{village},  "
        cell7 = await pg.locator("//label[text()=' District ']").count()
        if cell7 != 0:
            district = (await pg.locator("//label[text()=' District ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"district-{district},  "
        cell8 = await pg.locator("//label[text()=' Pin Code ']").count()
        if cell8 != 0:
            pin_code = (await pg.locator("//label[text()=' Pin Code ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"{pin_code}, "   
        cell9 = await pg.locator("//label[text()=' Landmark ']").count()
        if cell9 != 0:
            landmark = (await pg.locator("//label[text()=' Landmark ']/following-sibling::div/div").first.inner_text()).strip()
            add += f"Landmark-{landmark} "
        return add
    except Exception as e:
        print(f"Couldn't find promoter address: {e}")

async def total_apartments(pg):
    await pg.wait_for_timeout(2000)
    try:
        cells = await pg.locator("//th[text()='Total']").count()
        if cells == 0:
            return "N/A"
        else:
            direct = (await pg.locator("//th[text()='Total']/following-sibling::th[3]").inner_text())
            return direct
    except Exception as e:
        print(f"Issue with the no of apartmets: {e}")

async def fetch_data(page, context):
    try:
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
        promoter = await promoter_address(new_page)

        await new_page.close()

        return date, type, apartment, add, promoter
    except Exception as e:
        print(f"Can't fetch data: {e}")


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

        try:
            for i,row in df.iterrows():
                if row.get("STATUS") == "done":
                    continue
                rera_num = row["RERA NUMBER"]
                await page.locator("input#edit-project-name.leftBdrRadius.form-text").fill(rera_num) 
                await page.wait_for_load_state("load")
                await page.locator("input#edit-submit--2.btn-default.me-2.button.js-form-submit.form-submit").click()

                command = await asyncio.to_thread(input, "Enter command: ")
                if command == "next":
                    continue
                elif command == "fetch":
                    date, type, unit, add, promoter = await fetch_data(page, context)
                    projects.append({
                            "PROJECT NAME": row["PROJECT NAME"],
                            "LOCATION": add,
                            "REGISTRATION DATE": date,
                            "RERA NUMBER": row["RERA NUMBER"],
                            "PROMOTER NAME": row["PROMOTER NAME"],
                            "COMPLETION DATE": "31-12-2026",
                            "PROJECT TYPE": type,
                            "UNITS": unit,
                            "ADDRESS": promoter
                    })
                    print(f"{i} Succesfully appended list!")
                    df.at[i, "STATUS"] = "done"
                    df.to_excel("Rera_Dec.xlsx", index=False)
                else:
                    break
        except Exception as e:
            print(F"Can't configure excel file: {e}")
        finally:
            save_file()
        await browser.close()

asyncio.run(main())