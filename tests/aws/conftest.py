import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


def pytest_configure(config):
    # Default to headed mode locally so devs can see the browser.
    # CI sets CI=true (e.g. GitHub Actions), which keeps runs headless.
    if not os.environ.get("CI") and not config.getoption("headed"):
        config.option.headed = True


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("base_url") or os.environ.get("BASE_URL")
