
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_state_persists_across_pages(async_page):
    page = async_page

    # Step 1: Open a demo website
    await page.goto(
        "https://www.saucedemo.com/",
        wait_until="domcontentloaded"
    )

    # Step 2: Store data in localStorage
    await page.evaluate("""
        () => localStorage.setItem(
            'test_username',
            'demo_user'
        )
    """)

    # Step 3: Verify the stored value
    stored_value = await page.evaluate("""
        () => localStorage.getItem('test_username')
    """)

    assert stored_value == "demo_user"

    print("State saved:", stored_value)

    # Step 4: Navigate to another page on the same origin
    await page.goto(
        "https://www.saucedemo.com/inventory.html",
        wait_until="domcontentloaded"
    )

    # Step 5: Verify the state persists
    persisted_value = await page.evaluate("""
        () => localStorage.getItem('test_username')
    """)

    assert persisted_value == "demo_user", (
        "localStorage state did not persist after navigation."
    )

    print("State persisted:", persisted_value)

    # Step 6: Verify the browser remains on the same origin
    assert await page.evaluate("() => location.origin") == (
        "https://www.saucedemo.com"
    )

    print("Task 6 completed successfully.")
