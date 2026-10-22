
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_multistep_form_persistence(async_page):
    page = async_page

    # Step 1: Create a demo multi-step form
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Step Form Demo</title>
    </head>
    <body>
        <h1>Registration Form</h1>

        <section id="step1">
            <h2>Step 1: Personal Details</h2>
            <label for="full_name">Full Name</label>
            <input id="full_name" type="text">

            <label for="email">Email</label>
            <input id="email" type="email">

            <button id="next" type="button">Next</button>
        </section>

        <section id="step2" hidden>
            <h2>Step 2: Preferences</h2>
            <label for="city">City</label>
            <input id="city" type="text">

            <button id="back" type="button">Back</button>
            <button id="submit" type="button">Submit</button>
        </section>

        <p id="result"></p>

        <script>
            const step1 = document.getElementById("step1");
            const step2 = document.getElementById("step2");

            document.getElementById("next").onclick = () => {
                step1.hidden = true;
                step2.hidden = false;
            };

            document.getElementById("back").onclick = () => {
                step2.hidden = true;
                step1.hidden = false;
            };

            document.getElementById("submit").onclick = () => {
                document.getElementById("result").textContent =
                    "Form submitted successfully";
            };
        </script>
    </body>
    </html>
    """

    # Step 2: Load the demo form
    await page.set_content(html)

    await expect(
        page.get_by_role("heading", name="Registration Form")
    ).to_be_visible()

    # Step 3: Fill in Step 1
    await page.locator("#full_name").fill("Test User")
    await page.locator("#email").fill("test@example.com")

    # Step 4: Move to Step 2
    await page.locator("#next").click()

    await expect(
        page.get_by_role("heading", name="Step 2: Preferences")
    ).to_be_visible()

    # Step 5: Fill in Step 2
    await page.locator("#city").fill("Bengaluru")

    # Step 6: Return to Step 1
    await page.locator("#back").click()

    await expect(
        page.get_by_role("heading", name="Step 1: Personal Details")
    ).to_be_visible()

    # Step 7: Verify Step 1 data is preserved
    await expect(page.locator("#full_name")).to_have_value(
        "Test User"
    )
    await expect(page.locator("#email")).to_have_value(
        "test@example.com"
    )

    print("Personal details persisted successfully.")

    # Step 8: Return to Step 2 and verify its data
    await page.locator("#next").click()

    await expect(page.locator("#city")).to_have_value(
        "Bengaluru"
    )

    print("Preferences persisted successfully.")

    # Step 9: Submit the demo form
    await page.locator("#submit").click()

    await expect(page.locator("#result")).to_have_text(
        "Form submitted successfully"
    )

    print("Task 8 completed successfully.")
