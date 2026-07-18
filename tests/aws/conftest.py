import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("base_url") or os.environ.get("BASE_URL")
