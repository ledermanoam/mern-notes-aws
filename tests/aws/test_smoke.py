# Read-only tests. Safe to run against the deployed API.
import os
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
