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


def test_no_console_errors_on_load(page: Page, base_url):
    errors = []
    page.on(
        "console",
        lambda msg: errors.append(msg.text) if msg.type == "error" else None,
    )
    page.goto(base_url)
    # Wait for the app to render (title heading appears after React mounts).
    expect(page.get_by_role("heading", name="Notes on the Cloud")).to_be_visible()
    # Give any async fetch a moment to settle.
    page.wait_for_load_state("networkidle")
    assert errors == [], f"console errors on load: {errors}"


def test_notes_list_container_rendered(page: Page, base_url):
    # section.list renders whether the notes list is empty or populated,
    # so it's a safe selector for a read-only prod smoke test.
    page.goto(base_url)
    expect(page.locator("section.list")).to_be_visible()
    expect(page.get_by_role("heading", name="Recent notes")).to_be_visible()


def test_api_label_visible(page: Page, base_url):
    # Confirms the full render: the header "API: ..." span is always present.
    page.goto(base_url)
    expect(page.get_by_text("API:", exact=False)).to_be_visible()
