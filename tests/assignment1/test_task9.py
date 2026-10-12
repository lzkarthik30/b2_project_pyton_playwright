
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_locator_strategies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open SauceDemo login page
            await page.goto("https://www.saucedemo.com/")

            # 1. CSS selector
            username = page.locator("#user-name")
            await username.fill("standard_user")
            await expect(username).to_have_value("standard_user")
            print("CSS selector test passed")

            # 2. XPath
            password = page.locator('xpath=//*[@id="password"]')
            await password.fill("secret_sauce")
            await expect(password).to_have_value("secret_sauce")
            print("XPath test passed")

            # 3. Visible text
            login_text = page.get_by_text("Swag Labs", exact=True)
            await expect(login_text).to_be_visible()
            print("Visible text locator test passed")

            # 4. get_by_role()
            login_button = page.get_by_role(
                "button", name="Login"
            )
            await expect(login_button).to_be_visible()
            await login_button.click()

            # Verify successful login
            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".title")).to_have_text("Products")
            print("get_by_role() test passed")

            # 5. get_by_label()
            # Verify the product sort dropdown using its accessible name
            sort_dropdown = page.get_by_role(
                "combobox", name="Sort products"
            )
            await expect(sort_dropdown).to_be_visible()

            await sort_dropdown.select_option("za")
            await expect(sort_dropdown).to_have_value("za")
            print("Accessible form-control locator test passed")

            print("Task 9 locator strategies test passed!")

        finally:
            await browser.close()
