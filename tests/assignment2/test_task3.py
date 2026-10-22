
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_amazon_search_autosuggest(async_page):
    page = async_page

    # Step 1: Open Amazon India
    await page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Step 2: Locate the search box
    search_box = page.locator("#twotabsearchtextbox")
    await expect(search_box).to_be_visible(timeout=20000)

    # Step 3: Enter the search keyword
    await search_box.fill("wireless mouse")

    # Step 4: Wait for auto-suggestions dynamically
    suggestions = page.locator(
        "div.s-suggestion"
    )

    await expect(suggestions.first).to_be_visible(
        timeout=15000
    )

    # Step 5: Print available suggestions
    suggestion_count = await suggestions.count()
    print(f"\nSuggestions found: {suggestion_count}")

    for index in range(min(suggestion_count, 10)):
        text = (
            await suggestions.nth(index).inner_text()
        ).strip()

        if text:
            print(f"{index + 1}. {text}")

    # Step 6: Find a suggestion matching the keyword
    matching_suggestion = suggestions.filter(
        has_text="wireless mouse"
    ).first

    if await matching_suggestion.count() == 0:
        raise AssertionError(
            "No suggestion containing 'wireless mouse' "
            "was found."
        )

    selected_text = (
        await matching_suggestion.inner_text()
    ).strip()

    print(f"\nSelected suggestion: {selected_text}")

    # Step 7: Click the matching suggestion
    await matching_suggestion.click()

    # Step 8: Verify that search results are displayed
    await expect(
        page.locator(
            '[data-component-type="s-search-result"]'
        ).first
    ).to_be_visible(timeout=20000)

    print(f"Search results URL: {page.url}")
