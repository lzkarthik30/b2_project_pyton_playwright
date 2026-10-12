
# # import pytest
# # from playwright.async_api import async_playwright, expect


# # @pytest.mark.asyncio
# # async def test_extracting_text_and_attributes():
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(headless=False)
# #         page = await browser.new_page()

# #         try:
# #             # 1. Open SauceDemo login page
# #             await page.goto("https://www.saucedemo.com/")

# #             # 2. Retrieve heading text
# #             heading = page.locator(".login_logo")
# #             heading_text = await heading.inner_text()

# #             print("Heading text:", heading_text)

# #             assert heading_text == "Swag Labs"
# #             await expect(heading).to_be_visible()

# #             # 3. Retrieve inner text from a container with multiple elements
# #             login_form = page.locator("form")
# #             container_text = await login_form.inner_text()

# #             print("Login form text:", container_text)

# #             assert "Login" in container_text
# #             assert "Username" in container_text
# #             assert "Password" in container_text

# #             # 4. Retrieve an input field's value
# #             username = page.locator("#user-name")
# #             await username.fill("standard_user")

# #             username_value = await username.input_value()

# #             print("Username input value:", username_value)
# #             assert username_value == "standard_user"

# #             # 5. Read HTML attributes
# #             username_placeholder = await username.get_attribute("placeholder")
# #             username_class = await username.get_attribute("class")

# #             login_button = page.locator("#login-button")
# #             login_button_type = await login_button.get_attribute("type")
# #             login_button_value = await login_button.get_attribute("value")

# #             print("Username placeholder:", username_placeholder)
# #             print("Username class:", username_class)
# #             print("Login button type:", login_button_type)
# #             print("Login button value:", login_button_value)

# #             # 6. Validate extracted attributes
# #             assert username_placeholder == "Username"
# #             assert username_class is not None
# #             assert login_button_type == "submit"
# #             assert login_button_value == "Login"

# #             print("Task 11 text and attribute extraction passed!")

# #         finally:
# #             await browser.close()


# import pytest
# from playwright.async_api import async_playwright, expect


# @pytest.mark.asyncio
# async def test_extracting_text_and_attributes():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()

#         try:
#             # 1. Open SauceDemo
#             await page.goto("https://www.saucedemo.com/")

#             # 2. Retrieve heading text
#             heading = page.locator(".login_logo")
#             heading_text = await heading.inner_text()

#             print("Heading text:", heading_text)
#             assert heading_text == "Swag Labs"
#             await expect(heading).to_be_visible()

#             # 3. Retrieve input value
#             username = page.locator("#user-name")
#             await username.fill("standard_user")

#             username_value = await username.input_value()
#             print("Username input value:", username_value)
#             assert username_value == "standard_user"

#             # 4. Read HTML attributes
#             username_placeholder = await username.get_attribute("placeholder")
#             username_class = await username.get_attribute("class")

#             print("Username placeholder:", username_placeholder)
#             print("Username class:", username_class)

#             assert username_placeholder == "Username"
#             assert username_class is not None

#             # 5. Login to SauceDemo
#             await page.locator("#password").fill("secret_sauce")
#             await page.locator("#login-button").click()

#             await expect(page.locator(".title")).to_have_text("Products")

#             # 6. Retrieve text from a container with multiple elements
#             product_container = page.locator("#inventory_container")
#             container_text = await product_container.inner_text()

#             print("Product container text:", container_text)

#             assert "Sauce Labs Backpack" in container_text
#             assert "Sauce Labs Bike Light" in container_text

#             # 7. Read two more HTML attributes
#             product_link = page.locator('[data-test="item-4-title-link"]')
#             product_href = await product_link.get_attribute("href")

#             sort_dropdown = page.get_by_role(
#                 "combobox", name="Sort products"
#             )
#             sort_value = await sort_dropdown.get_attribute("value")

#             print("Product link href:", product_href)
#             print("Sort dropdown value:", sort_value)

#             assert product_href == "#"
#             assert sort_value == "az"

#             print("Task 11 text and attribute extraction passed!")

#         finally:
#             await browser.close()



import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_extracting_text_and_attributes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # 1. Open SauceDemo login page
            await page.goto(
                "https://www.saucedemo.com/",
                wait_until="domcontentloaded"
            )

            # 2. Locate heading and retrieve its text
            heading = page.locator(".login_logo")
            heading_text = await heading.inner_text()

            print("Heading text:", heading_text)
            assert heading_text == "Swag Labs"
            await expect(heading).to_be_visible()

            # 3. Retrieve an input field's value
            username = page.locator("#user-name")
            await username.fill("standard_user")

            username_value = await username.input_value()

            print("Username input value:", username_value)
            assert username_value == "standard_user"

            # 4. Read HTML attributes
            username_placeholder = await username.get_attribute("placeholder")
            username_class = await username.get_attribute("class")

            print("Username placeholder:", username_placeholder)
            print("Username class:", username_class)

            assert username_placeholder == "Username"
            assert username_class is not None

            # 5. Log in
            await page.locator("#password").fill("secret_sauce")
            await page.locator("#login-button").click()

            # Verify successful login
            await expect(page.locator(".title")).to_have_text("Products")
            print("Login successful!")

            # 6. Extract text from the product container
            # Use the unique data-test attribute, not #inventory_container
            product_container = page.locator(
                '[data-test="inventory-container"]'
            )

            await expect(product_container).to_be_visible()

            container_text = await product_container.inner_text()

            print("Product container text:", container_text)

            assert "Sauce Labs Backpack" in container_text
            assert "Sauce Labs Bike Light" in container_text

            # 7. Read the product link's href attribute
            product_link = page.locator(
                '[data-test="item-4-title-link"]'
            )

            product_href = await product_link.get_attribute("href")

            print("Product link href:", product_href)
            assert product_href == "#"

            # 8. Read the sort dropdown's current value
            sort_dropdown = page.get_by_role(
                "combobox", name="Sort products"
            )

            sort_value = await sort_dropdown.input_value()

            print("Sort dropdown value:", sort_value)
            assert sort_value == "az"

            print("Task 11 text and attribute extraction passed!")

        finally:
            await browser.close()
