
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
AUTH_DIR = PROJECT_ROOT / ".auth"
STATE_FILE = AUTH_DIR / "state.json"

BASE_URL = "https://demowebshop.tricentis.com/"


async def main():
    # Create the .auth folder if it doesn't exist
    AUTH_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Create a new browser context
        context = await browser.new_context()

        try:
            # Add a demo cookie before opening the website
            await context.add_cookies([
                {
                    "name": "task4_demo",
                    "value": "playwright_test",
                    "url": BASE_URL,
                }
            ])

            # Set localStorage before the page loads
            await context.add_init_script("""
                window.localStorage.setItem(
                    "task4_demo",
                    "playwright_test"
                );
            """)

            # Open the website
            page = await context.new_page()
            await page.goto(BASE_URL, wait_until="domcontentloaded")

            # Verify the cookie
            cookies = await context.cookies(BASE_URL)

            cookie_found = any(
                cookie["name"] == "task4_demo"
                and cookie["value"] == "playwright_test"
                for cookie in cookies
            )

            assert cookie_found, "Demo cookie was not found"

            # Verify localStorage
            local_storage_value = await page.evaluate(
                "() => localStorage.getItem('task4_demo')"
            )

            assert (
                local_storage_value == "playwright_test"
            ), "Demo localStorage value was not found"

            # Save cookies and localStorage
            await context.storage_state(path=str(STATE_FILE))

            print("Demo cookie verified successfully.")
            print("Demo localStorage verified successfully.")
            print("Browser storage state saved successfully.")
            print(f"Saved file: {STATE_FILE}")

        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
