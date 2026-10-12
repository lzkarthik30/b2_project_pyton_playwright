
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_dynamic_waits_for_spa():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open SauceDemo
            await page.goto(
                "https://www.saucedemo.com/",
                wait_until="domcontentloaded"
            )

            # 2. Login
            await page.locator("#user-name").fill("standard_user")
            await page.locator("#password").fill("secret_sauce")
            await page.locator("#login-button").click()

            # 3. Wait for the inventory page state
            await page.wait_for_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".title")).to_have_text("Products")

            # 4. Locate the first product's Add to cart button
            add_to_cart = page.locator(
                '[data-test="add-to-cart-sauce-labs-backpack"]'
            )

            await expect(add_to_cart).to_be_visible()
            await expect(add_to_cart).to_be_enabled()

            # 5. Trigger the dynamic update
            await add_to_cart.click()

            # 6. Wait for the cart badge to appear
            cart_badge = page.locator('[data-test="shopping-cart-badge"]')
            await expect(cart_badge).to_be_visible()
            await expect(cart_badge).to_have_text("1")

            print("Cart badge appeared with count 1")

            # 7. Verify the button changes to Remove
            remove_button = page.locator(
                '[data-test="remove-sauce-labs-backpack"]'
            )
            await expect(remove_button).to_be_visible()

            # 8. Open the cart
            await page.locator('[data-test="shopping-cart-link"]').click()

            # 9. Wait for the cart page and verify dynamic state
            await page.wait_for_url(
                "https://www.saucedemo.com/cart.html"
            )
            await expect(page.locator(".title")).to_have_text("Your Cart")

            cart_item = page.locator(
                '[data-test="inventory-item-name"]'
            )
            await expect(cart_item).to_have_text("Sauce Labs Backpack")

            print("Cart contents verified successfully!")
            print("Task 16 dynamic waits test passed!")

        finally:
            await browser.close()
