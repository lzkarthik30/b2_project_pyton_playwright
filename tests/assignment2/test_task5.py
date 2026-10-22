
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_ui_api_product_validation(async_page):
    page = async_page

    # Step 1: Open the sample product API
    api_response = await page.request.get(
        "https://dummyjson.com/products/1"
    )

    # Step 2: Validate the API response
    assert api_response.status == 200, (
        f"API request failed with status {api_response.status}"
    )

    api_data = await api_response.json()

    api_title = api_data["title"]
    api_price = api_data["price"]

    print(f"\nAPI product title: {api_title}")
    print(f"API product price: {api_price}")

    # Step 3: Open the corresponding sample product webpage
    await page.goto(
        "https://dummyjson.com/products/1",
        wait_until="domcontentloaded"
    )

    # The endpoint displays JSON, so validate its visible content.
    page_content = await page.locator("body").inner_text()

    assert api_title in page_content, (
        "Product title from the API was not found on the page."
    )

    assert str(api_price) in page_content, (
        "Product price from the API was not found on the page."
    )

    print("API title matches the displayed response.")
    print("API price matches the displayed response.")
    print("UI/API validation completed successfully.")
