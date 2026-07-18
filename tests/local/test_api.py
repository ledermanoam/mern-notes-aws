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
