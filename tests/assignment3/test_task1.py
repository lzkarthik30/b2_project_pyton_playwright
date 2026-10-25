
import logging

import pytest
from playwright.async_api import expect

logger = logging.getLogger("assignment2")


@pytest.mark.asyncio
async def test_practice_page_loads(async_page):
    logger.info("Opening the practice page")

    await async_page.goto(
        "https://demowebshop.tricentis.com/"
    )

    await expect(async_page).to_have_title(
        __import__("re").compile("Demo Web Shop")
    )

    logger.info("Practice page title verified")
