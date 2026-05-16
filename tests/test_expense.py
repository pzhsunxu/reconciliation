from fastapi.testclient import TestClient
from datetime import date


def test_create_expense(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    res = client.post("/api/expenses", json={
        "hotel_id": hotel["id"],
        "category": "utility",
        "amount": 500.00,
        "expense_date": date.today().isoformat(),
        "description": "电费",
        "created_by": "张三",
    })
    assert res.status_code == 201
    data = res.json()
    assert float(data["amount"]) == 500.00
    assert data["category"] == "utility"


def test_list_expenses(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    client.post("/api/expenses", json={"hotel_id": hotel["id"], "category": "utility", "amount": 300, "expense_date": date.today().isoformat()})
    client.post("/api/expenses", json={"hotel_id": hotel["id"], "category": "labor", "amount": 1000, "expense_date": date.today().isoformat()})
    res = client.get("/api/expenses", params={"hotel_id": hotel["id"]})
    assert len(res.json()) == 2


def test_update_expense(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    created = client.post("/api/expenses", json={"hotel_id": hotel["id"], "category": "utility", "amount": 200, "expense_date": date.today().isoformat()}).json()
    res = client.put(f"/api/expenses/{created['id']}", json={"amount": 350})
    assert res.status_code == 200
    assert float(res.json()["amount"]) == 350


def test_delete_expense(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    created = client.post("/api/expenses", json={"hotel_id": hotel["id"], "category": "utility", "amount": 100, "expense_date": date.today().isoformat()}).json()
    res = client.delete(f"/api/expenses/{created['id']}")
    assert res.status_code == 204


def test_filter_expenses_by_category(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    client.post("/api/expenses", json={"hotel_id": hotel["id"], "category": "utility", "amount": 100, "expense_date": date.today().isoformat()})
    client.post("/api/expenses", json={"hotel_id": hotel["id"], "category": "labor", "amount": 200, "expense_date": date.today().isoformat()})
    res = client.get("/api/expenses", params={"hotel_id": hotel["id"], "category": "utility"})
    assert len(res.json()) == 1
    assert res.json()[0]["category"] == "utility"
