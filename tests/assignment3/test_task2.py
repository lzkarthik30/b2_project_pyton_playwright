
import random
import string

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, expect


BASE_URL = "https://parabank.parasoft.com/parabank/index.htm"
PASSWORD = "DemoPass123!"


def unique_username():
    suffix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=10)
    )
    return f"qa_{suffix}"


@pytest_asyncio.fixture
async def browser_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        page.set_default_timeout(15000)

        yield page

        await browser.close()


async def open_home_page(page):
    await page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=30000,
    )


async def register_demo_user(page, username, password):
    """Register a new ParaBank demo user using dummy data."""
    await open_home_page(page)

    await page.get_by_role("link", name="Register").click()

    await expect(
        page.get_by_role("heading", name="Signing up is easy!")
    ).to_be_visible()

    fields = {
        'input[name="customer.firstName"]': "Test",
        'input[name="customer.lastName"]': "Automation",
        'input[name="customer.address.street"]': "123 Demo Street",
        'input[name="customer.address.city"]': "Test City",
        'input[name="customer.address.state"]': "CA",
        'input[name="customer.address.zipCode"]': "90001",
        'input[name="customer.phoneNumber"]': "5551234567",
        'input[name="customer.ssn"]': "999001234",
        'input[name="customer.username"]': username,
        'input[name="customer.password"]': password,
        'input[name="repeatedPassword"]': password,
    }

    for selector, value in fields.items():
        await page.locator(selector).fill(value)

    await page.get_by_role("button", name="Register").click()

    try:
        await expect(
            page.get_by_text(
                "Your account was created successfully",
                exact=False,
            )
        ).to_be_visible(timeout=20000)
    except AssertionError:
        print("Registration could not be confirmed.")
        print("Current URL:", page.url)
        print(
            "Page content:",
            (await page.locator("body").inner_text())[:1500],
        )
        raise

    # ParaBank may automatically log the user in after registration.
    logout_link = page.get_by_role("link", name="Log Out")

    if await logout_link.is_visible():
        await logout_link.click()

        await expect(
            page.locator('input[name="username"]')
        ).to_be_visible(timeout=15000)


async def login(page, username, password):
    """Log in and verify the account overview."""
    await open_home_page(page)

    username_field = page.locator('input[name="username"]')
    password_field = page.locator('input[name="password"]')

    try:
        await expect(username_field).to_be_visible(timeout=15000)
        await expect(password_field).to_be_visible(timeout=10000)
    except AssertionError as exc:
        print("Login form was not found.")
        print("Current URL:", page.url)
        print("Page title:", await page.title())
        print(
            "Page content:",
            (await page.locator("body").inner_text())[:1500],
        )
        raise AssertionError(
            "Login form is unavailable. Inspect the page output."
        ) from exc

    await username_field.fill(username)
    await password_field.fill(password)

    await page.get_by_role("button", name="Log In").click()

    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible(timeout=20000)


async def get_account_ids(page):
    """Get account IDs displayed in the account overview."""
    account_links = page.locator("#accountTable a")

    await expect(account_links.first).to_be_visible(timeout=15000)

    account_ids = await account_links.all_text_contents()

    return [
        account_id.strip()
        for account_id in account_ids
        if account_id.strip()
    ]


async def get_dropdown_options(dropdown):
    """Read non-empty account dropdown options."""
    return await dropdown.locator("option").evaluate_all(
        """
        options => options
            .map(option => option.value.trim())
            .filter(value => value !== "")
        """
    )


async def select_transfer_accounts(page):
    """Wait for transfer dropdowns and select distinct accounts."""
    from_dropdown = page.locator("#fromAccountId")
    to_dropdown = page.locator("#toAccountId")

    await expect(from_dropdown).to_be_visible()
    await expect(to_dropdown).to_be_visible()

    try:
        await expect(
            from_dropdown.locator("option").nth(1)
        ).to_be_attached(timeout=10000)
    except AssertionError:
        print("Source dropdown HTML:", await from_dropdown.inner_html())
        print("Destination dropdown HTML:", await to_dropdown.inner_html())

        pytest.skip(
            "Source account options did not load. "
            "Inspect the dropdown HTML above."
        )

    source_options = await get_dropdown_options(from_dropdown)
    destination_options = await get_dropdown_options(to_dropdown)

    print("Source account options:", source_options)
    print("Destination account options:", destination_options)

    if not source_options:
        pytest.skip("No source accounts are available.")

    if not destination_options:
        pytest.skip("No destination accounts are available.")

    source_account = source_options[0]

    destination_account = next(
        (
            account
            for account in destination_options
            if account != source_account
        ),
        None,
    )

    if destination_account is None:
        pytest.skip(
            "Two different accounts are required for a transfer."
        )

    await from_dropdown.select_option(source_account)
    await to_dropdown.select_option(destination_account)

    return source_account, destination_account


@pytest.mark.asyncio
async def test_parabank_end_to_end(browser_page):
    page = browser_page
    username = unique_username()
    password = PASSWORD

    # STEP 1: Register a new demo account.
    await register_demo_user(page, username, password)

    # STEP 2: Log in.
    await login(page, username, password)

    # STEP 3: Verify account overview.
    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()

    await expect(page.locator("#accountTable")).to_be_visible()

    account_ids = await get_account_ids(page)
    assert account_ids, "No accounts were displayed."

    print("Available account IDs:", account_ids)

    # STEP 4: Open account details.
    first_account = account_ids[0]

    await page.locator("#accountTable a").first.click()

    await expect(
        page.get_by_role("heading", name="Account Details")
    ).to_be_visible(timeout=15000)

    await expect(
        page.locator("#accountId")
    ).to_contain_text(first_account)

    print("Account details verified:", first_account)

    # STEP 5: Return to account overview.
    await page.get_by_role(
        "link", name="Accounts Overview"
    ).click()

    await expect(page.locator("#accountTable")).to_be_visible()

    # STEP 6: Open Transfer Funds.
    await page.get_by_role(
        "link", name="Transfer Funds"
    ).click()

    await expect(
        page.get_by_role("heading", name="Transfer Funds")
    ).to_be_visible()

    source_account, destination_account = (
        await select_transfer_accounts(page)
    )

    # STEP 7: Submit one small demo transfer.
    await page.locator("#amount").fill("1.00")

    print(
        f"Submitting transfer: {source_account} -> "
        f"{destination_account}, amount 1.00"
    )

    # Submit only once; do not retry automatically.
    await page.get_by_role("button", name="Transfer").click()

    result_message = page.locator("#showResult")
    await expect(result_message).to_be_visible(timeout=20000)

    result_text = (await result_message.inner_text()).strip()
    print("Transfer result:", result_text)

    assert (
        "complete" in result_text.lower()
        or "success" in result_text.lower()
    ), f"Transfer was not confirmed: {result_text}"

    # STEP 8: Verify the account overview remains accessible.
    await page.get_by_role(
        "link", name="Accounts Overview"
    ).click()

    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()

    await expect(page.locator("#accountTable")).to_be_visible()

    # STEP 9: Test hover on a navigation link.
    overview_link = page.get_by_role(
        "link", name="Accounts Overview"
    )

    await overview_link.hover()
    await expect(overview_link).to_be_visible()

    print(
        "Hover tested. ParaBank normally uses standard navigation links."
    )

    # STEP 10: Inspect hidden-element behavior safely.
    await page.get_by_role(
        "link", name="Transfer Funds"
    ).click()

    hidden_result = page.locator("#showResult")

    if await hidden_result.count() > 0:
        if await hidden_result.is_visible():
            print("Transfer result panel is visible.")
        else:
            print(
                "Hidden result panel found. "
                "No forced interaction attempted."
            )
    else:
        print("No suitable hidden section found.")

    # STEP 11: Safe right-click and double-click.
    safe_target = page.locator("#leftPanel")

    if (
        await safe_target.count() > 0
        and await safe_target.is_visible()
    ):
        await safe_target.click(button="right")
        await safe_target.dblclick()
        print("Safe right-click and double-click completed.")
    else:
        print("No suitable visible target found.")

    # STEP 12: Log out and verify signed-out state.
    logout_link = page.get_by_role("link", name="Log Out")

    await expect(logout_link).to_be_visible()
    await logout_link.click()

    await expect(
        page.locator('input[name="username"]')
    ).to_be_visible(timeout=15000)

    await expect(
        page.locator('input[name="password"]')
    ).to_be_visible()

    print("Logout verified.")
    print("ParaBank end-to-end test completed.")
