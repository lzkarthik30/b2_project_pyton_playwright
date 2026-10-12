
# import pytest
# from playwright.async_api import expect

# from config.settings import BASE_URL


# # Task 4: Verify website using configuration settings
# @pytest.mark.asyncio
# async def test_website_title(async_page):
#     # Open website using configured BASE_URL
#     await async_page.goto(BASE_URL)

#     # Get and print the page title
#     title = await async_page.title()
#     print("Website title:", title)

#     # Validate the page title
#     await expect(async_page).to_have_title("Facebook")


import pytest
from playwright.async_api import expect

from config import BASE_URL


@pytest.mark.asyncio
async def test_website_title(async_page):
    await async_page.goto(BASE_URL)

    title = await async_page.title()
    print("Website title:", title)

    await expect(async_page).to_have_title("Facebook")

