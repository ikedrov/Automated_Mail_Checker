# pyinstaller check_mail.py --onefile

import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch()
        context = await browser.new_context(storage_state=
        '/path_to_your/playwright/.auth/storage_state.json')
        page = await context.new_page()

        await page.goto('https://gmail.com')

        new_emails = []
        emails = page.locator('div.UI table tr')

        for email in await emails.all():
            is_new_email = await email.locator('td li[data-tooltip="Отметить как прочитанное"]').count() == 1

            if is_new_email:
                sender = await email.locator('td span[email]:visible').inner_text()
                title = await email.locator('td span[data-thread-id]:visible').inner_text()
                new_emails.append([sender, title])

        if not new_emails:
            print('No new emails.')
        else:
            print(f'{len(new_emails)} new emails.')
            print('-' * 20)
            for new_email in new_emails:
                print(f'{new_email[0]}: {new_email[1]}')
                print('-' * 20)

        await context.close()


asyncio.run(main())