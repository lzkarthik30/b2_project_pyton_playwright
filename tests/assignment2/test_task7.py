
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_product_results_and_scrolling(async_page):
    page = async_page

    # Step 1: Open Amazon India search results
    await page.goto(
        "https://www.amazon.in/s?k=wireless+mouse",
        wait_until="domcontentloaded"
    )

    # Step 2: Locate product cards
    product_cards = page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(product_cards.first).to_be_visible(
        timeout=20000
    )

    # Step 3: Record the initial product count
    initial_count = await product_cards.count()
    print(f"\nInitial product count: {initial_count}")

    assert initial_count > 0, "No products found on the page."

    # Step 4: Scroll down to the bottom of the page
    await page.evaluate(
        "() => window.scrollTo(0, document.body.scrollHeight)"
    )

    # Step 5: Wait for scrolling to settle
    await page.wait_for_load_state("domcontentloaded")

    # Step 6: Count products after scrolling
    final_count = await product_cards.count()
    print(f"Product count after scrolling: {final_count}")

    # Amazon may use pagination instead of infinite scrolling.
    # Therefore, verify that the original products remain available.
    assert final_count >= initial_count, (
        "The number of visible product cards unexpectedly decreased."
    )

    # Step 7: Check for a next-page control
    next_page = page.get_by_role(
        "button",
        name="Go to next page, page 2"
    )

    if await next_page.count() > 0 and await next_page.is_visible():
        print("Next-page control is available.")
    else:
        print("Next-page button not found with this locator.")

    print("Scrolling and product listing check completed.")
