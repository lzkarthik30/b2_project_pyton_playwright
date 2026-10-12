
from playwright.async_api import async_playwright, expect
import pytest


@pytest.mark.asyncio
async def test_page_title():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://example.com")

        title = await page.title()
        print("Page title:", title)

        await expect(page).to_have_title("Example Domain")

        await browser.close()
