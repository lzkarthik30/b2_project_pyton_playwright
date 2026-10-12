
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.parametrize(
    "browser_engine",
    ["chromium", "firefox", "webkit"],
    ids=["Chromium", "Firefox", "WebKit"]
)
@pytest.mark.asyncio
async def test_browser_navigation(browser_engine):
    async with async_playwright() as p:
        browser_type = getattr(p, browser_engine)
        browser = await browser_type.launch(headless=True)

        try:
            page = await browser.new_page()

            await page.goto("https://example.com")
            await expect(page).to_have_title("Example Domain")

            print(f"Navigation passed on {browser_engine}")

        finally:
            await browser.close()

