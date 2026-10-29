
import pytest
from playwright.async_api import expect


FORM_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Multi-Step Travel Form</title>
</head>
<body>
    <h1>Travel Registration Form</h1>

    <form id="travel-form" novalidate>

        <section id="step-one">
            <h2>Step 1: Personal Details</h2>

            <label for="full-name">Full Name</label>
            <input id="full-name" type="text">
            <br><br>

            <label for="email">Email</label>
            <input id="email" type="email">
            <br><br>

            <p id="step-one-error" role="alert"></p>

            <button id="next-button" type="button">
                Continue
            </button>
        </section>

        <section id="step-two" hidden>
            <h2>Step 2: Travel Details</h2>

            <label for="destination">Destination</label>
            <input id="destination" type="text">
            <br><br>

            <label for="travel-date">Travel Date</label>
            <input id="travel-date" type="date">
            <br><br>

            <p id="step-two-error" role="alert"></p>

            <button id="back-button" type="button">
                Back
            </button>

            <button id="submit-button" type="submit">
                Submit
            </button>
        </section>

    </form>

    <section id="confirmation" hidden>
        <h2>Registration Successful</h2>
        <p id="confirmation-message" role="status"></p>
    </section>

    <script>
        const form = document.querySelector("#travel-form");
        const stepOne = document.querySelector("#step-one");
        const stepTwo = document.querySelector("#step-two");
        const confirmation = document.querySelector("#confirmation");

        const fullName = document.querySelector("#full-name");
        const email = document.querySelector("#email");
        const destination = document.querySelector("#destination");
        const travelDate = document.querySelector("#travel-date");

        const stepOneError = document.querySelector("#step-one-error");
        const stepTwoError = document.querySelector("#step-two-error");

        function validateStepOne() {
            stepOneError.textContent = "";

            if (!fullName.value.trim()) {
                stepOneError.textContent = "Full name is required.";
                return false;
            }

            const emailPattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;

            if (!emailPattern.test(email.value.trim())) {
                stepOneError.textContent = "Enter a valid email address.";
                return false;
            }

            return true;
        }

        document.querySelector("#next-button").addEventListener(
            "click", () => {
                if (!validateStepOne()) {
                    return;
                }

                stepOne.hidden = true;
                stepTwo.hidden = false;
            }
        );

        document.querySelector("#back-button").addEventListener(
            "click", () => {
                stepTwo.hidden = true;
                stepOne.hidden = false;
            }
        );

        form.addEventListener("submit", (event) => {
            event.preventDefault();
            stepTwoError.textContent = "";

            if (!destination.value.trim()) {
                stepTwoError.textContent = "Destination is required.";
                return;
            }

            if (!travelDate.value) {
                stepTwoError.textContent = "Travel date is required.";
                return;
            }

            stepOne.hidden = true;
            stepTwo.hidden = true;
            confirmation.hidden = false;

            document.querySelector(
                "#confirmation-message"
            ).textContent =
                "Thank you, " + fullName.value.trim() +
                "! Your trip to " + destination.value.trim() +
                " has been registered.";
        });
    </script>
</body>
</html>
"""


async def open_travel_form(page):
    """Load the local practice form."""

    await page.set_content(FORM_HTML)

    await expect(
        page.get_by_role("heading", name="Travel Registration Form")
    ).to_be_visible()

    await expect(
        page.get_by_role("heading", name="Step 1: Personal Details")
    ).to_be_visible()


@pytest.mark.asyncio
async def test_multistep_form_persists_data_and_submits(async_page):
    """Verify data persistence when navigating back and forth."""

    page = async_page

    # Step 1: Open the form
    await open_travel_form(page)

    # Enter personal details
    await page.locator("#full-name").fill("Test User")
    await page.locator("#email").fill("test.user@example.com")

    # Continue to Step 2
    await page.locator("#next-button").click()

    await expect(
        page.get_by_role("heading", name="Step 2: Travel Details")
    ).to_be_visible()

    # Enter travel details
    await page.locator("#destination").fill("Bengaluru")
    await page.locator("#travel-date").fill("2027-01-15")

    # Navigate back to Step 1
    await page.locator("#back-button").click()

    await expect(
        page.get_by_role("heading", name="Step 1: Personal Details")
    ).to_be_visible()

    # Verify Step 1 values persist
    await expect(page.locator("#full-name")).to_have_value("Test User")
    await expect(
        page.locator("#email")
    ).to_have_value("test.user@example.com")

    # Continue again
    await page.locator("#next-button").click()

    await expect(
        page.get_by_role("heading", name="Step 2: Travel Details")
    ).to_be_visible()

    # Verify Step 2 values persist too
    await expect(
        page.locator("#destination")
    ).to_have_value("Bengaluru")

    await expect(
        page.locator("#travel-date")
    ).to_have_value("2027-01-15")

    # Submit the form
    await page.locator("#submit-button").click()

    # Verify successful submission
    await expect(
        page.get_by_role("heading", name="Registration Successful")
    ).to_be_visible()

    await expect(
        page.locator("#confirmation-message")
    ).to_contain_text(
        "Thank you, Test User! Your trip to Bengaluru has been registered."
    )


@pytest.mark.asyncio
async def test_multistep_form_rejects_missing_and_invalid_input(async_page):
    """Verify invalid input prevents progression to Step 2."""

    page = async_page

    await open_travel_form(page)

    # Negative case 1: Submit without a name or email
    await page.locator("#next-button").click()

    await expect(
        page.locator("#step-one-error")
    ).to_have_text("Full name is required.")

    await expect(
        page.get_by_role("heading", name="Step 1: Personal Details")
    ).to_be_visible()

    # Negative case 2: Enter a name but an invalid email
    await page.locator("#full-name").fill("Test User")
    await page.locator("#email").fill("invalid-email")

    await page.locator("#next-button").click()

    await expect(
        page.locator("#step-one-error")
    ).to_have_text("Enter a valid email address.")

    # Verify the form does not proceed
    await expect(
        page.get_by_role("heading", name="Step 1: Personal Details")
    ).to_be_visible()

    await expect(
        page.locator("#step-two")
    ).to_be_hidden()
