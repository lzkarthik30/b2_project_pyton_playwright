
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_assertions_expect_and_pytest():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open SauceDemo
            await page.goto("https://www.saucedemo.com/")

            # 2. Verify page title using expect()
            await expect(page).to_have_title("Swag Labs")

            # 3. Verify URL using expect()
            await expect(page).to_have_url(
                "https://www.saucedemo.com/"
            )

            # 4. Verify element visibility
            username = page.locator("#user-name")
            await expect(username).to_be_visible()

            # 5. Verify element text
            heading = page.locator(".login_logo")
            await expect(heading).to_have_text("Swag Labs")

            # 6. Verify input value
            await username.fill("standard_user")
            await expect(username).to_have_value("standard_user")

            # 7. Verify element enabled/disabled
            login_button = page.locator("#login-button")
            await expect(login_button).to_be_enabled()

            # The username field should also be enabled
            await expect(username).to_be_enabled()

            # 8. Use pytest assert for an extracted/calculated value
            username_value = await username.input_value()
            username_length = len(username_value)

            print("Username:", username_value)
            print("Username length:", username_length)

            assert username_value == "standard_user"
            assert username_length == 13

            # 9. Login and verify the Products page
            await page.locator("#password").fill("secret_sauce")
            await login_button.click()

            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".title")).to_have_text("Products")

            print("Task 12 assertions test passed!")

        finally:
            await browser.close()
