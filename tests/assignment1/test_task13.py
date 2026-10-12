
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_saucedemo_soft_assertions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        failures = []

        # Helper function for non-blocking assertions
        async def soft_check(description, assertion):
            try:
                await assertion
                print(f"PASS: {description}")
            except Exception as error:
                message = str(error).splitlines()[0]
                failures.append(f"{description}: {message}")
                print(f"FAIL: {description}")

        try:
            # Open SauceDemo
            await page.goto("https://www.saucedemo.com/")

            # 1. Verify page title
            await soft_check(
                "Page title is Swag Labs",
                expect(page).to_have_title("Swag Labs")
            )

            # 2. Verify page URL
            await soft_check(
                "Login page URL is correct",
                expect(page).to_have_url(
                    "https://www.saucedemo.com/"
                )
            )

            # 3. Verify username field is visible
            username = page.locator("#user-name")
            await soft_check(
                "Username field is visible",
                expect(username).to_be_visible()
            )

            # 4. Verify password field is visible
            password = page.locator("#password")
            await soft_check(
                "Password field is visible",
                expect(password).to_be_visible()
            )

            # 5. Verify login button is enabled
            login_button = page.locator("#login-button")
            await soft_check(
                "Login button is enabled",
                expect(login_button).to_be_enabled()
            )

            # 6. Verify heading text
            heading = page.locator(".login_logo")
            await soft_check(
                "Heading text is correct",
                expect(heading).to_have_text("Swag Labs")
            )

            # Report all collected failures at the end
            print("\n========== SOFT ASSERTION REPORT ==========")

            if failures:
                print(f"Total failures: {len(failures)}")

                for number, failure in enumerate(failures, start=1):
                    print(f"{number}. {failure}")
            else:
                print("All soft assertions passed!")

            print("===========================================\n")

            # Fail the test only after all checks have run
            assert not failures, (
                f"{len(failures)} soft assertion(s) failed:\n"
                + "\n".join(failures)
            )

        finally:
            await browser.close()
