# Read-only tests. Safe to run against the deployed API.
import os
import time
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:4000/api")


def test_health():
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_notes():
    r = requests.get(f"{BASE_URL}/notes", timeout=10)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_health_content_type_is_json():
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    assert r.status_code == 200
    ctype = r.headers.get("Content-Type", "")
    assert ctype.startswith("application/json"), f"unexpected Content-Type: {ctype!r}"


def test_health_responds_under_two_seconds():
    start = time.perf_counter()
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    elapsed = time.perf_counter() - start
    assert r.status_code == 200
    assert elapsed < 2.0, f"/health took {elapsed:.3f}s (>= 2s budget)"


def test_notes_items_have_expected_shape_when_present():
    r = requests.get(f"{BASE_URL}/notes", timeout=10)
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)
    if not items:
        return  # empty list is a valid prod state; nothing more to assert
    for item in items:
        for key in ("_id", "title", "createdAt"):
            assert key in item, f"note missing key {key!r}: {item!r}"
