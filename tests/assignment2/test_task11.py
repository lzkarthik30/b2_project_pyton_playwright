
import json
import pytest
from pathlib import Path
from playwright.async_api import async_playwright, expect


STATE_FILE = Path("tests/assignment2/demo_state.json")


@pytest.mark.asyncio
async def test_reuse_browser_session():
    # Step 1: Handle a missing state file
    if not STATE_FILE.exists():
        pytest.skip(
            f"Storage state not found: {STATE_FILE}. "
            "Run Task 10 first to create it."
        )

    # Step 2: Check that the state file contains valid JSON
    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            state_data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        pytest.fail(f"Storage state file is invalid: {error}")

    # Step 3: Launch browser and load saved state
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        context = await browser.new_context(
            storage_state=state_data
        )

        page = await context.new_page()

        # Step 4: Open the same origin used in Task 10
        await page.goto(
            "https://example.com/",
            wait_until="domcontentloaded"
        )

        # Step 5: Check whether the saved demo state exists
        saved_value = await page.evaluate("""
            () => localStorage.getItem("demo_username")
        """)

        if saved_value != "test_user":
            await context.close()
            await browser.close()

            pytest.fail(
                "Saved session data was not restored. "
                "The state file may be stale or incorrect."
            )

        print("Saved demo state was restored successfully.")

        # Step 6: Verify the page loaded
       
        await expect(
          page.locator("body")
        ).to_contain_text(
    "This domain is for use in documentation examples"
)

        print("Page loaded successfully.")
        print("Session reuse check completed.")

        await context.close()
        await browser.close()
