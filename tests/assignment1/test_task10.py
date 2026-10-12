
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_typing_filling_keyboard_actions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open SauceDemo
            await page.goto("https://www.saucedemo.com/")

            # 2. Locate a text input
            username = page.locator("#user-name")
            await expect(username).to_be_visible()

            # 3. Enter data using fill()
            await username.fill("standard_user")
            await expect(username).to_have_value("standard_user")
            print("Fill action passed")

            # 4. Clear and replace the existing value
            await username.clear()
            await username.fill("locked_out_user")
            await expect(username).to_have_value("locked_out_user")
            print("Clear and replace passed")

            # 5. Demonstrate a keyboard shortcut: Ctrl+A
            await username.press("Control+A")
            await username.press_sequentially("standard_user")
            await expect(username).to_have_value("standard_user")
            print("Ctrl+A keyboard shortcut passed")

            # 6. Use press() for a keyboard action
            password = page.locator("#password")
            await password.fill("secret_sauce")
            await password.press("Enter")

            # 7. Validate successful login
            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".title")).to_have_text("Products")

            print("Enter key action passed")
            print("Task 10 completed successfully!")

        finally:
            await browser.close()
