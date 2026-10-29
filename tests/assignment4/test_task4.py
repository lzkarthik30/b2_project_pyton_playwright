
from pathlib import Path

from playwright.async_api import expect


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = PROJECT_ROOT / ".auth" / "state.json"

BASE_URL = "https://demowebshop.tricentis.com/"


async def test_reuse_saved_storage_state(async_page):
    # Create a new context using the saved storage state
    context = await async_page.context.browser.new_context(
        storage_state=str(STATE_FILE)
    )

    try:
        page = await context.new_page()
        await page.goto(BASE_URL, wait_until="domcontentloaded")

        # Verify the saved cookie
        cookies = await context.cookies(BASE_URL)

        assert any(
            cookie["name"] == "task4_demo"
            and cookie["value"] == "playwright_test"
            for cookie in cookies
        ), "Saved cookie was not restored"

        # Verify the saved localStorage
        local_storage_value = await page.evaluate(
            "() => localStorage.getItem('task4_demo')"
        )

        assert local_storage_value == "playwright_test", (
            "Saved localStorage value was not restored"
        )

    finally:
        await context.close()
