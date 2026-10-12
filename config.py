
# Task 4: Playwright Configuration

# # Website URL
# BASE_URL = "https://www.facebook.com/"

# # Browser settings
# BROWSER_NAME = "chromium"
# HEADLESS = False

# # Timeout settings (milliseconds)
# DEFAULT_TIMEOUT = 10000
# NAVIGATION_TIMEOUT = 30000



import os
from pathlib import Path
from dotenv import dotenv_values


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent


# Environment configuration files
ENV_FILES = {
    "dev": ".env.dev",
    "qa": ".env.qa",
    "staging": ".env.staging",
}


def get_config(env_name):
    env_name = env_name.lower()

    if env_name not in ENV_FILES:
        raise ValueError(
            "Invalid environment. Choose dev, qa, or staging."
        )

    env_file = PROJECT_ROOT / ENV_FILES[env_name]

    if not env_file.exists():
        raise FileNotFoundError(
            f"Environment file not found: {env_file}"
        )

    settings = dotenv_values(env_file)

    if not settings.get("BASE_URL"):
        raise ValueError("BASE_URL is missing from the environment file")

    return {
        "ENV_NAME": settings.get("ENV_NAME", env_name.upper()),
        "BASE_URL": settings["BASE_URL"],
        "HEADLESS": settings.get("HEADLESS", "true").lower() == "true",
        "DEFAULT_TIMEOUT": int(settings.get("DEFAULT_TIMEOUT", "10000")),
        "NAVIGATION_TIMEOUT": int(
            settings.get("NAVIGATION_TIMEOUT", "30000")
        ),
    }
