from fastapi.testclient import TestClient
from datetime import date


def test_create_manual_reconciliation(client: TestClient):
    today = date.today().isoformat()
    res = client.post("/api/reconciliations", json={"start_date": today, "end_date": today})
    assert res.status_code == 201
    data = res.json()
    assert data["job_type"] == "manual"
    assert data["start_date"] == today


def test_list_reconciliations(client: TestClient):
    today = date.today().isoformat()
    client.post("/api/reconciliations", json={"start_date": today, "end_date": today})
    res = client.get("/api/reconciliations")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_get_reconciliation(client: TestClient):
    today = date.today().isoformat()
    created = client.post("/api/reconciliations", json={"start_date": today, "end_date": today}).json()
    res = client.get(f"/api/reconciliations/{created['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == created["id"]


def test_reconciliation_not_found(client: TestClient):
    res = client.get("/api/reconciliations/999")
    assert res.status_code == 404


def test_filter_reconciliations_by_type(client: TestClient):
    today = date.today().isoformat()
    client.post("/api/reconciliations", json={"start_date": today, "end_date": today})
    res = client.get("/api/reconciliations", params={"job_type": "manual"})
    assert len(res.json()) >= 1
    for item in res.json():
        assert item["job_type"] == "manual"
