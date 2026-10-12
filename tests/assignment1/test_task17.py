
import asyncio
import time

import pytest
from playwright.async_api import (
    async_playwright,
    expect,
    TimeoutError as PlaywrightTimeoutError,
)


async def wait_for_custom_condition(
    page, selector, expected_text, timeout=5000
):
    """Poll until an element contains the expected text."""
    locator = page.locator(selector)
    deadline = time.monotonic() + timeout / 1000

    while time.monotonic() < deadline:
        if await locator.count() > 0:
            if await locator.first.is_visible():
                actual_text = await locator.first.inner_text()

                if actual_text.strip() == expected_text:
                    return

        await asyncio.sleep(0.2)

    raise AssertionError(
        f"Custom wait failed: '{selector}' did not display "
        f"'{expected_text}' within {timeout} ms."
    )


@pytest.mark.asyncio
async def test_timeout_handling_and_custom_waits():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Configure reasonable timeouts
        page.set_default_timeout(5000)
        page.set_default_navigation_timeout(10000)

        try:
            # 2. Navigate with a separate navigation timeout
            await page.goto(
                "https://www.saucedemo.com/",
                wait_until="domcontentloaded"
            )

            await expect(page).to_have_title("Swag Labs")
            print("Page loaded successfully.")

            # 3. Intentionally wait for a missing element
            missing_element = page.locator(
                '[data-test="element-that-does-not-exist"]'
            )

            try:
                await missing_element.wait_for(
                    state="visible",
                    timeout=1500
                )
                pytest.fail(
                    "Expected the missing element to time out, "
                    "but it unexpectedly appeared."
                )

            except PlaywrightTimeoutError:
                print(
                    "Expected timeout handled: "
                    "the missing element did not appear."
                )

            # 4. Login successfully
            await page.locator("#user-name").fill("standard_user")
            await page.locator("#password").fill("secret_sauce")
            await page.locator("#login-button").click()

            await page.wait_for_url(
                "https://www.saucedemo.com/inventory.html"
            )
            await expect(page.locator(".title")).to_have_text("Products")

            # 5. Trigger a dynamic update by adding a product to the cart
            await page.locator(
                '[data-test="add-to-cart-sauce-labs-backpack"]'
            ).click()

            # 6. Custom polling: wait until cart badge text becomes "1"
            await wait_for_custom_condition(
                page,
                '[data-test="shopping-cart-badge"]',
                expected_text="1",
                timeout=5000
            )

            # 7. Verify the final dynamic state
            cart_badge = page.locator(
                '[data-test="shopping-cart-badge"]'
            )
            await expect(cart_badge).to_have_text("1")

            print("Custom wait succeeded: cart count is 1.")
            print("Task 17 timeout handling test passed!")

        finally:
            await browser.close()
