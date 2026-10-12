
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_multiple_locators():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open SauceDemo
            await page.goto("https://www.saucedemo.com/")

            # 2. Login
            await page.locator("#user-name").fill("standard_user")
            await page.locator("#password").fill("secret_sauce")
            await page.locator("#login-button").click()

            # Verify Products page
            await expect(page.locator(".title")).to_have_text("Products")

            # 3. Find all product name elements
            products = page.locator(
                '[data-test="inventory-item-name"]'
            )

            # 4. Count matching elements
            product_count = await products.count()
            print("Total products:", product_count)

            # 5. Verify expected number of products
            assert product_count == 6, (
                f"Expected 6 products, but found {product_count}"
            )

            # 6. Interact with the first matching element
            first_product = products.first
            first_name = await first_product.inner_text()

            print("First product:", first_name)
            await expect(first_product).to_be_visible()
            assert first_name == "Sauce Labs Backpack"

            # 7. Interact with the last matching element
            last_product = products.last
            last_name = await last_product.inner_text()

            print("Last product:", last_name)
            await expect(last_product).to_be_visible()
            assert last_name == "Test.allTheThings() T-Shirt (Red)"

            # 8. Interact with a specific element using nth(index)
            # Index starts from 0, so nth(2) is the third product
            third_product = products.nth(2)
            third_name = await third_product.inner_text()

            print("Third product:", third_name)
            await expect(third_product).to_be_visible()
            assert third_name == "Sauce Labs Bolt T-Shirt"

            # 9. Loop through all products and print their names
            print("\nAll product names:")

            for index in range(product_count):
                product = products.nth(index)
                name = await product.inner_text()
                print(f"{index + 1}. {name}")

            # 10. Verify all six products are displayed
            for index in range(product_count):
                await expect(products.nth(index)).to_be_visible()

            print("\nTask 14 multiple locators test passed!")

        finally:
            await browser.close()
