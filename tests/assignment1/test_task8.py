
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_saucedemo_navigation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open SauceDemo
            await page.goto(
                "https://www.saucedemo.com/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("Login page URL:", page.url)

            # 2. Verify login fields
            await expect(page.locator("#user-name")).to_be_visible()
            await expect(page.locator("#password")).to_be_visible()

            # 3. Enter login credentials
            await page.locator("#user-name").fill("standard_user")
            await page.locator("#password").fill("secret_sauce")

            # 4. Click Login
            await page.locator("#login-button").click()

            # 5. Verify successful login
            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".title")).to_have_text("Products")

            print("Login successful!")

            # 6. Open Sauce Labs Backpack details
            backpack = page.locator('[data-test="item-4-title-link"]')
            await expect(backpack).to_be_visible()
            await backpack.click()

            # 7. Verify product details
            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory-item.html?id=4"
            )
            await expect(
                page.locator(".inventory_details_name")
            ).to_have_text("Sauce Labs Backpack")

            print("Product details opened successfully!")

            # 8. Navigate backward
            await page.go_back()

            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".title")).to_have_text("Products")

            print("Back navigation successful!")

            # 9. Navigate forward
            await page.go_forward()

            await expect(page).to_have_url(
                "https://www.saucedemo.com/inventory-item.html?id=4"
            )
            await expect(
                page.locator(".inventory_details_name")
            ).to_have_text("Sauce Labs Backpack")

            print("Forward navigation successful!")

            # 10. Reload product details page
            await page.reload()

            await expect(
                page.locator(".inventory_details_name")
            ).to_have_text("Sauce Labs Backpack")

            print("Page reload successful!")
            print("Task 8 navigation test passed!")

        finally:
            await browser.close()
