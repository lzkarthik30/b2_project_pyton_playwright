

import os
import pytest
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()


@pytest.mark.asyncio
async def test_login():
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")
    base_url = os.getenv("BASE_URL")

    assert username, "APP_USERNAME is missing in .env"
    assert password, "APP_PASSWORD is missing in .env"
    assert base_url, "BASE_URL is missing in .env"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page()
            await page.goto(base_url)

            print("Page title:", await page.title())
            print("Current URL:", page.url)

            # List available form fields without printing values
            fields = await page.locator(
                "input"
            ).evaluate_all("""
                elements => elements.map(el => ({
                    type: el.type,
                    name: el.name,
                    id: el.id,
                    placeholder: el.placeholder,
                    ariaLabel: el.getAttribute('aria-label')
                }))
            """)

            print("Available input fields:", fields)

        finally:
            await browser.close()
