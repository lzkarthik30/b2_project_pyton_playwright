
import pytest
from playwright.async_api import expect


# Test 1: Smoke test - Verify Facebook page title
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_facebook_page_title(async_page):
    await async_page.goto("https://www.facebook.com/")
    await expect(async_page).to_have_title("Facebook")


# Test 2: Regression test - Verify browser context stores data
@pytest.mark.regression
@pytest.mark.asyncio
async def test_context_stores_data(async_page):
    await async_page.goto("https://www.facebook.com/")

    await async_page.evaluate(
        "() => localStorage.setItem('username', 'Karthik')"
    )

    username = await async_page.evaluate(
        "() => localStorage.getItem('username')"
    )

    assert username == "Karthik"


# Test 3: Regression test - Verify context isolation
@pytest.mark.regression
@pytest.mark.asyncio
async def test_context_data_isolation(async_page):
    await async_page.goto("https://www.facebook.com/")

    username = await async_page.evaluate(
        "() => localStorage.getItem('username')"
    )

    assert username is None
