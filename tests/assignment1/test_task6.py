
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_environment_url(environment_config):
    env_name = environment_config["ENV_NAME"]
    base_url = environment_config["BASE_URL"]

    print(f"\nTesting environment: {env_name}")
    print(f"URL: {base_url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=environment_config["HEADLESS"]
        )

        try:
            page = await browser.new_page()

            page.set_default_timeout(
                environment_config["DEFAULT_TIMEOUT"]
            )
            page.set_default_navigation_timeout(
                environment_config["NAVIGATION_TIMEOUT"]
            )

            response = await page.goto(base_url)

            assert response is not None
            assert response.ok

            await expect(page).to_have_title("Example Domain")

        finally:
            await browser.close()
