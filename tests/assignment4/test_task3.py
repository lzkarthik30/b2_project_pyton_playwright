
import logging
import re

import pytest
from playwright.async_api import expect


BASE_URL = "https://demowebshop.tricentis.com/"


# Log which conditional branch is executed
logger = logging.getLogger(__name__)


async def open_cart(page):
    """Open the Demo Web Shop shopping cart."""

    await page.goto(BASE_URL)

    cart_link = page.get_by_role(
        "link",
        name=re.compile(r"Shopping cart \(")
    )

    await expect(cart_link).to_be_visible()
    await cart_link.click()

    await expect(page).to_have_url(
        re.compile(r"/cart", re.IGNORECASE)
    )


@pytest.mark.asyncio
async def test_cart_conditional_execution(async_page):
    """Handle empty and populated cart states safely."""

    page = async_page

    # Step 1: Open the shopping cart
    await open_cart(page)

    # Step 2: Define locators for both possible states
    cart_rows = page.locator(".cart-item-row")
    empty_cart_message = page.locator(
        ".order-summary-content"
    )

    # Step 3: Check the UI state before deciding what to do
    if await cart_rows.count() > 0:
        # Branch 1: Cart contains items
        logger.info("BRANCH TAKEN: Cart contains items")

        await expect(cart_rows.first).to_be_visible()

        quantity_input = cart_rows.first.locator(
            "input.qty-input"
        )

        # Only interact with the quantity field if it is usable
        if await quantity_input.is_visible() and await quantity_input.is_enabled():
            current_quantity = await quantity_input.input_value()

            assert current_quantity.isdigit(), (
                f"Unexpected quantity value: {current_quantity}"
            )

            logger.info(
                "Quantity field is visible and enabled. "
                "Current quantity: %s",
                current_quantity,
            )

            # Do not modify the cart unnecessarily.
            # The state has been checked and recorded.

        else:
            logger.info(
                "Quantity field is hidden or disabled; "
                "skipping quantity interaction."
            )

    else:
        # Branch 2: Cart is empty
        logger.info("BRANCH TAKEN: Cart is empty")

        await expect(empty_cart_message).to_be_visible()
        await expect(empty_cart_message).to_contain_text(
            re.compile(r"empty", re.IGNORECASE)
        )

        logger.info("Verified the empty-cart message.")

    logger.info("Conditional cart-state test completed.")
