# Read-only UI checks. Safe to run against the deployed frontend.
import os
import pytest
from playwright.sync_api import Page, expect


def test_homepage_renders(page: Page, base_url):
    page.goto(base_url)
    expect(page.get_by_role("heading", name="Notes on the Cloud")).to_be_visible()
    expect(page.get_by_role("heading", name="Recent notes")).to_be_visible()


def test_shows_configured_api_url(page: Page, base_url):
    expected_api = os.environ.get("EXPECTED_API_URL")
    if not expected_api:
        pytest.skip("EXPECTED_API_URL not set")
    page.goto(base_url)
    expect(page.get_by_text(f"API: {expected_api}")).to_be_visible()
