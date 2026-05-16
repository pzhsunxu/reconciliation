from fastapi.testclient import TestClient
from app.models import Hotel, CooperationType
from sqlalchemy.orm import Session


def test_create_hotel(client: TestClient):
    res = client.post("/api/hotels", json={
        "name": "测试酒店",
        "location": "北京",
        "cooperation_type": "split",
        "company_share": 0.6,
        "owner_share": 0.4,
    })
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "测试酒店"
    assert data["cooperation_type"] == "split"
    assert data["company_share"] == 0.6


def test_list_hotels(client: TestClient):
    client.post("/api/hotels", json={"name": "A酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4})
    client.post("/api/hotels", json={"name": "B酒店", "cooperation_type": "full"})
    res = client.get("/api/hotels")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_list_hotels_filter_by_name(client: TestClient):
    client.post("/api/hotels", json={"name": "北京酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4})
    client.post("/api/hotels", json={"name": "上海酒店", "cooperation_type": "full"})
    res = client.get("/api/hotels", params={"name": "北京"})
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "北京酒店"


def test_get_hotel(client: TestClient):
    created = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    res = client.get(f"/api/hotels/{created['id']}")
    assert res.status_code == 200
    assert res.json()["name"] == "测试酒店"


def test_get_hotel_not_found(client: TestClient):
    res = client.get("/api/hotels/999")
    assert res.status_code == 404


def test_update_hotel(client: TestClient):
    created = client.post("/api/hotels", json={"name": "原酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    res = client.put(f"/api/hotels/{created['id']}", json={"name": "新酒店"})
    assert res.status_code == 200
    assert res.json()["name"] == "新酒店"


def test_delete_hotel(client: TestClient):
    created = client.post("/api/hotels", json={"name": "删除酒店", "cooperation_type": "full"}).json()
    res = client.delete(f"/api/hotels/{created['id']}")
    assert res.status_code == 204
    res = client.get(f"/api/hotels/{created['id']}")
    assert res.status_code == 404


def test_filter_by_cooperation_type(client: TestClient):
    client.post("/api/hotels", json={"name": "分润酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4})
    client.post("/api/hotels", json={"name": "全租酒店", "cooperation_type": "full"})
    res = client.get("/api/hotels", params={"cooperation_type": "split"})
    assert len(res.json()) == 1
    assert res.json()[0]["cooperation_type"] == "split"
