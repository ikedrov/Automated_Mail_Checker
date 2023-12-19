import asyncio

from playwright.async_api import async_playwright


async def save_auth():
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://accounts.google.com', wait_until='domcontentloaded')

        email_input = page.locator('input#identifierId')
        await email_input.fill('email')
        await page.get_by_role('button', name='Next').click()

        password_input = page.get_by_label('Enter your password')
        await password_input.fill('password')
        await page.get_by_role('button', name='Next').click()

        await page.pause()

        await context.storage_state(path='your_path/playwright/.auth/storage_state.json')
        await context.close()

asyncio.run(save_auth())




