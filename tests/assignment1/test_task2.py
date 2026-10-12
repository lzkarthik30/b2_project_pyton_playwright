
import pytest
from playwright.async_api import expect


# Test 1: Navigate to Facebook and validate the page title
@pytest.mark.asyncio
async def test_page_navigation(async_page):
    await async_page.goto("https://www.facebook.com/")

    await expect(async_page).to_have_title("Facebook")


# Test 2: Store data in the first browser context
@pytest.mark.asyncio
async def test_first_context_isolated(async_page):
    await async_page.goto("https://www.facebook.com/")

    await async_page.evaluate(
        "() => localStorage.setItem('username', 'Karthik')"
    )

    username = await async_page.evaluate(
        "() => localStorage.getItem('username')"
    )

    assert username == "Karthik"


# Test 3: Verify data is not shared with a new context
@pytest.mark.asyncio
async def test_second_context_isolated(async_page):
    await async_page.goto("https://www.facebook.com/")

    username = await async_page.evaluate(
        "() => localStorage.getItem('username')"
    )

    assert username is None
