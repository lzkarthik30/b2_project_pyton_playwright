
# import re

# import pytest
# from playwright.async_api import expect


# @pytest.mark.asyncio
# async def test_amazon_product_discovery(async_page):
#     page = async_page

#     # Open Amazon India
#     await page.goto(
#         "https://www.amazon.in/",
#         wait_until="domcontentloaded"
#     )

#     # Verify that the page has loaded
#     await expect(page).to_have_title(re.compile(r"Amazon", re.I))

#     # Search for a product
#     search_box = page.locator("#twotabsearchtextbox")
#     await expect(search_box).to_be_visible()

#     search_keyword = "wireless mouse"
#     await search_box.fill(search_keyword)
#     await search_box.press("Enter")

#     # Wait for search results
#     await expect(
#         page.locator('[data-component-type="s-search-result"]').first
#     ).to_be_visible(timeout=15000)

#     # Find a product by visible title, not by result position
#     product_cards = page.locator(
#         '[data-component-type="s-search-result"]'
#     )

#     selected_title = None
#     selected_link = None

#     for index in range(await product_cards.count()):
#         card = product_cards.nth(index)
#         title_locator = card.locator("h2 a")

#         if await title_locator.count() == 0:
#             continue

#         title = (await title_locator.first.inner_text()).strip()

#         if "wireless mouse" in title.lower():
#             href = await title_locator.first.get_attribute("href")

#             if title and href:
#                 selected_title = title
#                 selected_link = title_locator.first
#                 break

#     assert selected_title is not None, (
#         f"No product matching '{search_keyword}' "
#         "was found in the search results."
#     )

#     # Open the matched product
#     await selected_link.click()
#     await page.wait_for_load_state("domcontentloaded")

#     # Validate the detail page title
#     detail_title = page.locator("#productTitle")
#     await expect(detail_title).to_be_visible(timeout=15000)

#     actual_title = (await detail_title.inner_text()).strip()

#     assert actual_title, "Product detail page title is empty."

#     # The detail title should match the selected result title.
#     # Amazon may normalize whitespace or add minor title variations.
#     normalize = lambda value: " ".join(value.split()).casefold()

#     assert (
#         normalize(selected_title) == normalize(actual_title)
#         or normalize(selected_title) in normalize(actual_title)
#         or normalize(actual_title) in normalize(selected_title)
#     ), (
#         f"Product title mismatch. "
#         f"Search result: '{selected_title}', "
#         f"Detail page: '{actual_title}'"
#     )

#     # Capture product information for the execution report
#     price_locator = page.locator(
#         ".a-price .a-offscreen"
#     ).first

#     price = None
#     if await price_locator.count() > 0:
#         if await price_locator.is_visible():
#             price = (await price_locator.inner_text()).strip()

#     print(f"Selected product: {selected_title}")
#     print(f"Detail page title: {actual_title}")
#     print(f"Price when visible: {price or 'Not available'}")
#     print(f"Product URL: {page.url}")



import re

import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_amazon_product_discovery(async_page):
    page = async_page

    # Step 1: Open Amazon India
    await page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    await expect(page).to_have_title(
        re.compile("Amazon", re.IGNORECASE)
    )

    # Step 2: Search for a product
    search_keyword = "wireless mouse"

    search_box = page.locator("#twotabsearchtextbox")
    await expect(search_box).to_be_visible(timeout=15000)

    await search_box.fill(search_keyword)
    await search_box.press("Enter")

    
    # Step 3: Wait for search results
    product_cards = page.locator(
        '[data-component-type="s-search-result"]'
    )

    await expect(product_cards.first).to_be_visible(
        timeout=20000
    )

    print("\n========== PAGE DEBUG ==========")
    print("Current URL:", page.url)
    print("Page title:", await page.title())

    # Print the visible page text
    body_text = await page.locator("body").inner_text()
    print("\nPage text (first 3000 characters):")
    print(body_text[:3000])

    # Inspect the first result container
    first_card = product_cards.first

    print("\nFirst result HTML:")
    print((await first_card.inner_html())[:4000])

    # Save the page for inspection
    await page.screenshot(
        path="amazon_task1_debug.png",
        full_page=False
    )

    print("\nScreenshot saved: amazon_task1_debug.png")
    print("================================")
