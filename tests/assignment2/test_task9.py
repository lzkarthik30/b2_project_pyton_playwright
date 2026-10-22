
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_conditional_product_availability(async_page):
    page = async_page

    # Step 1: Open Amazon India search results
    await page.goto(
        "https://www.amazon.in/s?k=wireless+mouse",
        wait_until="domcontentloaded"
    )

    # Step 2: Locate the product cards
    product_cards = page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(product_cards.first).to_be_visible(
        timeout=20000
    )

    # Step 3: Select a product by its visible title
    matching_card = product_cards.filter(
        has_text="Portronics Toad"
    ).first

    if await matching_card.count() == 0:
        pytest.skip(
            "The selected Portronics product was not found."
        )

    product_title = (
        await matching_card.locator("h2").inner_text()
    ).strip()

    print(f"\nSelected product: {product_title}")

    # Step 4: Check for an availability indicator
    card_text = (await matching_card.inner_text()).lower()

    unavailable_phrases = [
        "currently unavailable",
        "out of stock",
        "temporarily out of stock"
    ]

    is_unavailable = any(
        phrase in card_text
        for phrase in unavailable_phrases
    )

    # Step 5: Check whether Add to Cart is available
    add_to_cart = matching_card.get_by_role(
        "button",
        name="Add to cart"
    )

    add_button_exists = await add_to_cart.count() > 0

    if is_unavailable:
        print("Product appears to be unavailable.")
        print("Add-to-cart action will not be attempted.")

    elif add_button_exists:
        await expect(add_to_cart).to_be_visible()
        await expect(add_to_cart).to_be_enabled()

        print("Product appears available.")
        print("Add to Cart button is visible and enabled.")
        print("Button was NOT clicked to avoid modifying the cart.")

    else:
        print(
            "Availability could not be confirmed from the "
            "search result. No cart action was attempted."
        )

    print("Conditional availability check completed.")
