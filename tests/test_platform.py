from fastapi.testclient import TestClient


def test_create_platform(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    res = client.post("/api/platforms", json={
        "hotel_id": hotel["id"],
        "platform": "meituan",
        "account_name": "美团账号",
        "account_id": "MT001",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["platform"] == "meituan"
    assert data["hotel_id"] == hotel["id"]


def test_list_platforms(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "meituan", "account_name": "美团"})
    client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "ctrip", "account_name": "携程"})
    res = client.get("/api/platforms")
    assert len(res.json()) == 2


def test_list_platforms_by_hotel(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "meituan", "account_name": "美团"})
    res = client.get("/api/platforms", params={"hotel_id": hotel["id"]})
    assert len(res.json()) == 1


def test_update_platform(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    created = client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "meituan", "account_name": "原账号"}).json()
    res = client.put(f"/api/platforms/{created['id']}", json={"account_name": "新账号"})
    assert res.status_code == 200
    assert res.json()["account_name"] == "新账号"


def test_delete_platform(client: TestClient):
    hotel = client.post("/api/hotels", json={"name": "测试酒店", "cooperation_type": "split", "company_share": 0.6, "owner_share": 0.4}).json()
    created = client.post("/api/platforms", json={"hotel_id": hotel["id"], "platform": "meituan", "account_name": "待删除"}).json()
    res = client.delete(f"/api/platforms/{created['id']}")
    assert res.status_code == 204
