# UI CRUD flows. Writes to the DB — local only.
import uuid
from playwright.sync_api import Page, expect


def test_create_note_appears_in_list(page: Page, base_url):
    title = f"e2e-{uuid.uuid4().hex[:8]}"

    page.goto(base_url)
    page.get_by_label("Title").fill(title)
    page.get_by_label("Body").fill("created by playwright")
    page.get_by_role("button", name="Save note").click()

    expect(page.get_by_role("heading", name=title)).to_be_visible()


def test_delete_note_removes_it_from_list(page: Page, base_url):
    title = f"doomed-{uuid.uuid4().hex[:8]}"

    page.goto(base_url)
    page.get_by_label("Title").fill(title)
    page.get_by_role("button", name="Save note").click()

    note_heading = page.get_by_role("heading", name=title)
    expect(note_heading).to_be_visible()

    note_item = note_heading.locator("xpath=ancestor::li")
    note_item.get_by_role("button", name="Delete").click()

    expect(note_heading).not_to_be_visible()
