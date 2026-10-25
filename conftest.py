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


# import logging
# from datetime import datetime
# from pathlib import Path

# import pytest
# import pytest_asyncio
# from playwright.async_api import async_playwright


# # Project paths
# PROJECT_ROOT = Path(__file__).resolve().parents[2]

# LOG_DIR = PROJECT_ROOT / "logs"
# SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "screenshots"
# TRACE_DIR = PROJECT_ROOT / "artifacts" / "traces"

# for directory in (LOG_DIR, SCREENSHOT_DIR, TRACE_DIR):
#     directory.mkdir(parents=True, exist_ok=True)


# # Timestamped logging to console and file
# log_file = LOG_DIR / "pytest.log"

# logger = logging.getLogger("assignment2")
# logger.setLevel(logging.INFO)
# logger.propagate = False

# if not logger.handlers:
#     formatter = logging.Formatter(
#         "%(asctime)s | %(levelname)s | %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )

#     file_handler = logging.FileHandler(
#         log_file, encoding="utf-8"
#     )
#     file_handler.setFormatter(formatter)

#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(formatter)

#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)


# # Record each test's result for fixture teardown
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     setattr(item, f"rep_{report.when}", report)


# # Async browser, context, page and tracing fixture
# @pytest_asyncio.fixture
# async def async_page(request):
#     test_name = request.node.name
#     safe_name = "".join(
#         char if char.isalnum() or char in "-_" else "_"
#         for char in test_name
#     )
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#     async with async_playwright() as playwright:
#         browser = await playwright.chromium.launch(
#             headless=False
#         )

#         context = await browser.new_context()
#         page = await context.new_page()

#         page.set_default_timeout(10000)
#         page.set_default_navigation_timeout(30000)

#         # Record failed HTTP responses where practical
#         page.on(
#             "response",
#             lambda response: logger.warning(
#                 "HTTP %s | %s",
#                 response.status,
#                 response.url,
#             )
#             if response.status >= 400
#             else None,
#         )

#         await context.tracing.start(
#             screenshots=True,
#             snapshots=True,
#             sources=True,
#         )

#         logger.info("START TEST: %s", test_name)

#         try:
#             yield page

#         finally:
#             failed = (
#                 getattr(request.node, "rep_call", None)
#                 is not None
#                 and request.node.rep_call.failed
#             )

#             try:
#                 if failed:
#                     screenshot_path = (
#                         SCREENSHOT_DIR
#                         / f"{safe_name}_{timestamp}.png"
#                     )
#                     trace_path = (
#                         TRACE_DIR
#                         / f"{safe_name}_{timestamp}.zip"
#                     )

#                     try:
#                         await page.screenshot(
#                             path=str(screenshot_path),
#                             full_page=True,
#                         )
#                         logger.error(
#                             "Failure screenshot: %s",
#                             screenshot_path,
#                         )
#                     except Exception:
#                         logger.exception(
#                             "Could not capture failure screenshot"
#                         )

#                     logger.error(
#                         "TEST FAILED: %s | URL: %s",
#                         test_name,
#                         page.url,
#                     )

#                     await context.tracing.stop(
#                         path=str(trace_path)
#                     )
#                     logger.error(
#                         "Failure trace: %s",
#                         trace_path,
#                     )

#                 else:
#                     await context.tracing.stop()
#                     logger.info(
#                         "TEST PASSED: %s",
#                         test_name,
#                     )

#             finally:
#                 await context.close()
#                 await browser.close()
