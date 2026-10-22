# # from  playwright.async_api import async_playwright
# # import pytest_asyncio


# # @pytest_asyncio.fixture
# # async def async_page():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch (headless = False)
# #         page = await browser.new_page()
# #         yield page
# #         await browser.close()

# # import pytest_asyncio
# # from playwright.async_api import async_playwright


# # @pytest_asyncio.fixture
# # async def async_page():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(headless=False)
# #         page = await browser.new_page()

# #         yield page

# #         await browser.close()


# # import pytest_asyncio
# # from playwright.async_api import async_playwright


# # # 1. Browser fixture
# # @pytest_asyncio.fixture
# # async def browser():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(headless=False)

# #         yield browser

# #         await browser.close()


# # # 2. Custom BrowserContext fixture
# # @pytest_asyncio.fixture
# # async def custom_context(browser):
# #     context = await browser.new_context()

# #     yield context

# #     await context.close()


# # # 3. Page fixture from the custom context
# # @pytest_asyncio.fixture
# # async def async_page(custom_context):
# #     page = await custom_context.new_page()

# #     yield page


# # import pytest_asyncio
# # from playwright.async_api import async_playwright

# # from config import (
# #     BROWSER_NAME,
# #     HEADLESS,
# #     DEFAULT_TIMEOUT,
# #     NAVIGATION_TIMEOUT,
# # )


# # # Browser fixture
# # @pytest_asyncio.fixture
# # async def browser():
# #     async with async_playwright() as p:
# #         browser_type = getattr(p, BROWSER_NAME)
# #         browser = await browser_type.launch(headless=HEADLESS)

# #         yield browser

# #         await browser.close()


# # # BrowserContext fixture
# # @pytest_asyncio.fixture
# # async def custom_context(browser):
# #     context = await browser.new_context()

# #     yield context

# #     await context.close()


# # # Page fixture
# # @pytest_asyncio.fixture
# # async def async_page(custom_context):
# #     page = await custom_context.new_page()

# #     page.set_default_timeout(DEFAULT_TIMEOUT)
# #     page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)

# #     yield page



# import pytest
# from config import get_config


# def pytest_addoption(parser):
#     parser.addoption(
#         "--env",
#         action="store",
#         default="dev",
#         choices=["dev", "qa", "staging"],
#         help="Select environment: dev, qa, or staging",
#     )


# @pytest.fixture
# def environment_config(request):
#     env_name = request.config.getoption("--env")
#     settings = get_config(env_name)

#     print(f"\nSelected environment: {settings['ENV_NAME']}")
#     print(f"Base URL: {settings['BASE_URL']}")

#     return settings




import pytest_asyncio
from playwright.async_api import async_playwright


@pytest_asyncio.fixture
async def async_page():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        yield page

        await browser.close()

