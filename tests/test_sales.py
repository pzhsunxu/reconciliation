from fastapi.testclient import TestClient
from datetime import date


def test_pull_sales_data(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "meituan", "account_name": "美团"})
    res = client.post("/api/sales/pull", json={
        "hotel_id": hotel["id"],
        "start_date": date.today().isoformat(),
        "end_date": date.today().isoformat(),
    })
    assert res.status_code == 200
    assert res.json()["pulled"] > 0


def test_list_sales(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "meituan", "account_name": "美团"})
    client.post("/api/sales/pull", json={"hotel_id": hotel["id"], "start_date": date.today().isoformat(), "end_date": date.today().isoformat()})
    res = client.get("/api/sales", params={"hotel_id": hotel["id"]})
    assert res.status_code == 200
    assert len(res.json()) > 0


def test_list_sales_filter_by_platform(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "meituan", "account_name": "美团"})
    client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "ctrip", "account_name": "携程"})
    client.post("/api/sales/pull", json={"hotel_id": hotel["id"], "start_date": date.today().isoformat(), "end_date": date.today().isoformat()})
    res = client.get("/api/sales", params={"hotel_id": hotel["id"], "platform": "meituan"})
    assert res.status_code == 200
    for item in res.json():
        assert item["platform"] == "meituan"


def test_pull_sales_not_found_hotel(client: TestClient):
    res = client.post("/api/sales/pull", json={"hotel_id": 999, "start_date": date.today().isoformat(), "end_date": date.today().isoformat()})
    assert res.status_code == 404
