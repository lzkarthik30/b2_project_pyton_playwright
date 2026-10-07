# from playwright.async_api import async_playwright
# import pytest


# @pytest.mark.asyncio
# def test_diff_pages(async_page):

# import pytest
# from playwright.async_api import async_playwright


# @pytest.mark.asyncio
# async def test_diff_browser():  # diff browser context

#     async with async_playwright() as p:

#         # Chrome Browser
#         chrome_browser = await p.chromium.launch(headless=False)

#         # User Context
#         user_context = await chrome_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("http://google.com")

#         # Admin Context
#         admin_context = await chrome_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://www.facebook.com/")

#         # Firefox Browser
#         firefox_browser = await p.firefox.launch(headless=False)

#         # User Context
#         user_context = await firefox_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("http://google.com")

#         # Admin Context
#         admin_context = await firefox_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://www.facebook.com/")


# import pytest
# from playwright.async_api import async_playwright


# @pytest.mark.asyncio
# async def test_diff_browser():

#     async with async_playwright() as p:

#         # Chrome Browser
#         chrome_browser = await p.chromium.launch(headless=False)

#         # User Context
#         user_context = await chrome_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("https://www.google.com/")

#         # Admin Context
#         admin_context = await chrome_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://www.google.com/")

#         # Firefox Browser
#         firefox_browser = await p.firefox.launch(headless=False)

#         # User Context
#         user_context = await firefox_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("https://www.google.com/")

#         # Admin Context
#         admin_context = await firefox_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://www.google.com/")

# import pytest
# from playwright.async_api import async_playwright


# @pytest.mark.asyncio
# async def test_diff_browser():

#     async with async_playwright() as p:

#         # Chrome Browser
#         chrome_browser = await p.chromium.launch(headless=False)

#         # User Context → Google
#         user_context = await chrome_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("https://www.google.com/")

#         # Admin Context → Example
#         admin_context = await chrome_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://example.com")

#         # Firefox Browser
#         firefox_browser = await p.firefox.launch(headless=False)

#         # User Context → Google
#         user_context = await firefox_browser.new_context()
#         page = await user_context.new_page()
#         await page.goto("https://www.google.com/")

#         # Admin Context → Example
#         admin_context = await firefox_browser.new_context()
#         page = await admin_context.new_page()
#         await page.goto("https://example.com")

# import pytest
# from playwright.async_api import async_playwright


# @pytest.mark.asyncio
# async def test_diff_browser():

#     async with async_playwright() as p:

#         # Launch Chromium Browser
#         chrome_browser = await p.chromium.launch(headless=False)

#         # User Context → Google
#         user_context = await chrome_browser.new_context()
#         user_page = await user_context.new_page()
#         await user_page.goto("https://www.google.com/")

#         # Admin Context → Example.com
#         admin_context = await chrome_browser.new_context()
#         admin_page = await admin_context.new_page()
#         await admin_page.goto("https://example.com/")

import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_diff_browser():

    async with async_playwright() as p:

        chromeBrowser = await p.chromium.launch(headless=False)

        user_context = await chromeBrowser.new_context()
        page = await user_context.new_page()
        await page.goto("https://google.com")

        admin_context = await chromeBrowser.new_context()
        page = await admin_context.new_page()
        await page.goto("https://example.com/")

        await chromeBrowser.close()
    