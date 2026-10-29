
import re

import pytest
from playwright.async_api import expect


BASE_URL = "https://demowebshop.tricentis.com/"


async def search_product(page, search_term):
    """Open the home page, search for a product, and open its details."""

    await page.goto(BASE_URL)

    # Step 1: Verify home page
    await expect(page).to_have_title(
        re.compile("Demo Web Shop", re.IGNORECASE)
    )

    # Step 2: Search for a product
    search_box = page.locator("#small-searchterms")
    await expect(search_box).to_be_visible()
    await search_box.fill(search_term)

    await page.locator(
        "input.button-1.search-box-button"
    ).click()

    # Step 3: Verify search results
    product_items = page.locator(".product-item")
    await expect(product_items.first).to_be_visible()

    # Step 4: Find and open the matching product
    product_link = page.locator(
        ".product-item .product-title a"
    ).filter(
        has_text=re.compile(re.escape(search_term), re.IGNORECASE)
    ).first

    await expect(product_link).to_be_visible()
    await product_link.click()

    # Step 5: Verify product details page
    await expect(page.locator("div.product-name h1")).to_be_visible()

    return page


async def add_product_to_cart(page):
    """Capture product details and add the selected product to the cart."""

    # Capture product name
    product_name = (
        await page.locator("div.product-name h1").inner_text()
    ).strip()

    # Capture expected price
    price_locator = page.locator("div.product-price span").first
    await expect(price_locator).to_be_visible()

    expected_price = (await price_locator.inner_text()).strip()

    assert product_name, "Product name should not be empty."
    assert expected_price, "Product price should not be empty."

    # Add the product to the cart
    add_button = page.locator(
        'input[id^="add-to-cart-button-"], '
        'button[id^="add-to-cart-button-"]'
    ).first

    await expect(add_button).to_be_visible()
    await add_button.click()

    return product_name, expected_price


async def open_shopping_cart(page):
    """Open the header shopping cart and verify the cart page."""

    # Avoid the strict mode error caused by two matching cart links.
    cart_link = page.get_by_role(
        "link",
        name=re.compile(r"Shopping cart \(")
    )

    await expect(cart_link).to_be_visible()
    await cart_link.click()

    # Verify navigation to the cart
    await expect(page).to_have_url(
        re.compile(r"/cart", re.IGNORECASE)
    )

    # Verify the cart contains an item
    cart_row = page.locator(".cart-item-row")
    await expect(cart_row.first).to_be_visible()


@pytest.mark.asyncio
async def test_product_state_across_pages(async_page):
    """Verify product state across home, details, and cart pages."""

    page = async_page

    # Step 1: Search for a product and open its details
    await search_product(page, "Fiction")

    # Step 2: Save product state locally
    product_name, expected_price = await add_product_to_cart(page)

    print(f"\nSelected product: {product_name}")
    print(f"Expected price: {expected_price}")

    # Step 3: Navigate to the shopping cart
    await open_shopping_cart(page)

    # Step 4: Find the selected product in the cart
    cart_row = page.locator(".cart-item-row").filter(
        has_text=product_name
    )

    await expect(cart_row).to_be_visible()
    await expect(cart_row).to_contain_text(product_name)

    # Step 5: Verify the product price
    actual_price = (
        await cart_row.locator(".product-unit-price").inner_text()
    ).strip()

    assert actual_price == expected_price, (
        f"Price mismatch for '{product_name}': "
        f"expected {expected_price}, got {actual_price}"
    )

    # Step 6: Verify quantity
    quantity = cart_row.locator("input.qty-input")
    await expect(quantity).to_have_value("1")

    print(f"Actual cart price: {actual_price}")
    print("Product name verified successfully.")
    print("Product price verified successfully.")
    print("Product quantity verified successfully.")
