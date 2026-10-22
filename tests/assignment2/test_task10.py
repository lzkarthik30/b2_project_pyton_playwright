
import json
import pytest
from pathlib import Path
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_save_and_reuse_browser_state():
    state_file = Path("tests/assignment2/demo_state.json")

    async with async_playwright() as playwright:
        # Step 1: Launch a browser
        browser = await playwright.chromium.launch()

        # Step 2: Create the first browser context
        context1 = await browser.new_context()
        page1 = await context1.new_page()

        # Step 3: Open a local demo page with a stable origin
        await page1.goto("https://example.com/")

        # Step 4: Store demo data in localStorage
        await page1.evaluate("""
            () => localStorage.setItem(
                "demo_username",
                "test_user"
            )
        """)

        # Step 5: Save the browser storage state
        state_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        await context1.storage_state(path=str(state_file))

        print(f"Storage state saved to: {state_file}")

        await context1.close()

        # Step 6: Create a new context using the saved state
        context2 = await browser.new_context(
            storage_state=str(state_file)
        )
        page2 = await context2.new_page()

        # Step 7: Visit the same origin
        await page2.goto("https://example.com/")

        # Step 8: Verify localStorage was restored
        stored_username = await page2.evaluate("""
            () => localStorage.getItem("demo_username")
        """)

        assert stored_username == "test_user"

        print("Restored localStorage value:", stored_username)

        await context2.close()
        await browser.close()

    print("Task 10 completed successfully.")
