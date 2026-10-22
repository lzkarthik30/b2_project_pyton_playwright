
import pytest
from pathlib import Path
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_amazon_product_discovery_report(async_page):
    page = async_page

    # Step 1: Open Amazon India
    await page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Step 2: Search for a book
    search_box = page.locator("#twotabsearchtextbox")
    await expect(search_box).to_be_visible(timeout=20000)

    await search_box.fill("Book")
    await search_box.press("Enter")

    # Step 3: Wait for search results
    product_cards = page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(product_cards.first).to_be_visible(
        timeout=20000
    )

    # Step 4: Select the first product and capture its title
    selected_card = product_cards.first

    product_title = (
        await selected_card.locator("h2").inner_text()
    ).strip()

    print(f"\nSelected product: {product_title}")

    # Step 5: Open the product in a new tab
    product_link = page.locator(
        ".s-asin a:has(h2)"
    ).first

    await expect(product_link).to_be_visible(timeout=15000)

    async with page.expect_popup() as popup_info:
        await product_link.click()

    product_page = await popup_info.value

    await product_page.wait_for_load_state(
        "domcontentloaded"
    )

    # Step 6: Verify the product title
    title_locator = product_page.locator("#productTitle")

    await expect(title_locator).to_be_visible(timeout=20000)

    actual_title = (
        await title_locator.inner_text()
    ).strip()

    assert actual_title, "Product title is empty."

    print(f"Product details title: {actual_title}")

    # Step 7: Check whether a price is displayed
    price_locator = product_page.locator(
        ".a-price .a-offscreen"
    ).first

    if await price_locator.count() > 0:
        price_text = (await price_locator.inner_text()).strip()
        print(f"Displayed price: {price_text}")
    else:
        price_text = "Price not displayed"
        print(price_text)

    # Step 8: Capture a screenshot
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = (
        report_dir / "task12_product_details.png"
    )

    await product_page.screenshot(
        path=str(screenshot_path),
        full_page=True
    )

    print(f"Screenshot saved: {screenshot_path}")

    # Step 9: Final validation
    assert actual_title, "Product discovery failed."

    print("\nProduct discovery completed successfully.")
    print("No item added to cart and no order placed.")

    await product_page.close()
