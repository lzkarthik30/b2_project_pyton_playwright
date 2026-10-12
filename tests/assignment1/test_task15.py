
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_builtin_waits_and_page_load_states():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Navigate and wait for DOM content to load
            await page.goto(
                "https://www.saucedemo.com/",
                wait_until="domcontentloaded"
            )

            # 2. Wait for the username field to appear
            username = page.locator("#user-name")
            await username.wait_for(state="visible")

            # Verify the element is ready
            await expect(username).to_be_enabled()

            # 3. Use auto-waiting to fill the username
            await username.fill("standard_user")

            # 4. Wait for the password field to be visible
            password = page.locator("#password")
            await password.wait_for(state="visible")
            await password.fill("secret_sauce")

            # 5. Click Login
            # Playwright automatically waits for the button to be actionable
            login_button = page.locator("#login-button")
            await expect(login_button).to_be_enabled()
            await login_button.click()

            # 6. Wait for the URL to change to the inventory page
            await page.wait_for_url(
                "https://www.saucedemo.com/inventory.html"
            )

            # 7. Wait for the Products heading
            products_heading = page.locator(".title")
            await products_heading.wait_for(state="visible")
            await expect(products_heading).to_have_text("Products")

            print("Login and URL wait successful!")

            # 8. Wait for a product to be visible
            backpack = page.locator(
                '[data-test="item-4-title-link"]'
            )
            await backpack.wait_for(state="visible")

            # 9. Click the product using Playwright auto-waiting
            await backpack.click()

            # 10. Wait for the product details URL
            await page.wait_for_url(
                "https://www.saucedemo.com/inventory-item.html?id=4"
            )

            # 11. Verify product details are ready
            product_name = page.locator(".inventory_details_name")
            await product_name.wait_for(state="visible")
            await expect(product_name).to_have_text("Sauce Labs Backpack")

            print("Product details loaded successfully!")
            print("Task 15 waits and page load states test passed!")

        finally:
            await browser.close()
