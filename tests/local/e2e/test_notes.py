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


def test_two_notes_both_appear_in_list(page: Page, base_url):
    title_a = f"pair-a-{uuid.uuid4().hex[:8]}"
    title_b = f"pair-b-{uuid.uuid4().hex[:8]}"

    page.goto(base_url)

    page.get_by_label("Title").fill(title_a)
    page.get_by_role("button", name="Save note").click()
    expect(page.get_by_role("heading", name=title_a)).to_be_visible()

    page.get_by_label("Title").fill(title_b)
    page.get_by_role("button", name="Save note").click()
    expect(page.get_by_role("heading", name=title_b)).to_be_visible()

    # Both are still visible after the second save.
    expect(page.get_by_role("heading", name=title_a)).to_be_visible()
    expect(page.get_by_role("heading", name=title_b)).to_be_visible()


def test_newest_note_appears_first(page: Page, base_url):
    # Backend orders by created_at DESC, so the last-created note should be
    # the first <li> in the notes list.
    title_older = f"older-{uuid.uuid4().hex[:8]}"
    title_newer = f"newer-{uuid.uuid4().hex[:8]}"

    page.goto(base_url)

    page.get_by_label("Title").fill(title_older)
    page.get_by_role("button", name="Save note").click()
    expect(page.get_by_role("heading", name=title_older)).to_be_visible()

    page.get_by_label("Title").fill(title_newer)
    page.get_by_role("button", name="Save note").click()
    expect(page.get_by_role("heading", name=title_newer)).to_be_visible()

    first_heading = page.locator("section.list ul li").first.get_by_role("heading")
    expect(first_heading).to_have_text(title_newer)


def test_form_clears_after_submit(page: Page, base_url):
    title = f"clearing-{uuid.uuid4().hex[:8]}"

    page.goto(base_url)
    page.get_by_label("Title").fill(title)
    page.get_by_label("Body").fill("some body text")
    page.get_by_role("button", name="Save note").click()

    expect(page.get_by_role("heading", name=title)).to_be_visible()
    expect(page.get_by_label("Title")).to_have_value("")
    expect(page.get_by_label("Body")).to_have_value("")


def test_note_appears_without_page_reload(page: Page, base_url):
    # SPA: adding a note updates the list in-place. We pin the load timestamp
    # via a window property and assert it survives after the save.
    title = f"spa-{uuid.uuid4().hex[:8]}"

    page.goto(base_url)
    page.evaluate("window.__spaMarker = 'still-here'")

    page.get_by_label("Title").fill(title)
    page.get_by_role("button", name="Save note").click()
    expect(page.get_by_role("heading", name=title)).to_be_visible()

    marker = page.evaluate("window.__spaMarker")
    assert marker == "still-here", "page reloaded during add-note (marker lost)"
