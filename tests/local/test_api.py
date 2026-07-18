import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:4000/api")


def test_health():
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_list_delete_note():
    created = requests.post(
        f"{BASE_URL}/notes",
        json={"title": "ci-test", "body": "hello from pytest"},
        timeout=10,
    )
    assert created.status_code == 201
    note = created.json()
    assert note["title"] == "ci-test"
    note_id = note["_id"]

    listed = requests.get(f"{BASE_URL}/notes", timeout=10)
    assert listed.status_code == 200
    assert any(n["_id"] == note_id for n in listed.json())

    deleted = requests.delete(f"{BASE_URL}/notes/{note_id}", timeout=10)
    assert deleted.status_code == 204


def test_create_note_requires_title():
    r = requests.post(f"{BASE_URL}/notes", json={"body": "no title"}, timeout=10)
    assert r.status_code == 400


def test_delete_nonexistent_note_returns_204():
    # Backend silently no-ops DELETE on a numeric id that doesn't exist.
    r = requests.delete(f"{BASE_URL}/notes/99999999", timeout=10)
    assert r.status_code == 204


def test_post_empty_body_returns_400():
    r = requests.post(f"{BASE_URL}/notes", json={}, timeout=10)
    assert r.status_code == 400


def test_post_whitespace_title_is_accepted_by_api():
    # Backend does NOT trim/reject whitespace titles (frontend trims client-side).
    # This test pins that behavior; if the backend ever validates, this test should be updated.
    r = requests.post(
        f"{BASE_URL}/notes",
        json={"title": "   ", "body": "x"},
        timeout=10,
    )
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == "   "
    # Clean up so we don't leave whitespace-titled rows lying around.
    requests.delete(f"{BASE_URL}/notes/{note['_id']}", timeout=10)


def test_list_returns_expected_note_shape_after_post():
    created = requests.post(
        f"{BASE_URL}/notes",
        json={"title": "shape-check", "body": "shape body"},
        timeout=10,
    )
    assert created.status_code == 201
    note_id = created.json()["_id"]

    listed = requests.get(f"{BASE_URL}/notes", timeout=10)
    assert listed.status_code == 200
    matching = [n for n in listed.json() if n["_id"] == note_id]
    assert len(matching) == 1
    item = matching[0]
    for key in ("_id", "title", "body", "createdAt"):
        assert key in item, f"missing key: {key}"
    assert item["title"] == "shape-check"
    assert item["body"] == "shape body"

    requests.delete(f"{BASE_URL}/notes/{note_id}", timeout=10)
