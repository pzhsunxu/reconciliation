from fastapi.testclient import TestClient


def test_dashboard_stats(client: TestClient):
    """测试仪表盘统计接口返回所有必要字段"""
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    # 验证所有字段存在
    assert "total_hotels" in data
    assert "split_hotels" in data
    assert "total_jobs" in data
    assert "completed_jobs" in data
    assert "pending_review" in data
    assert "reviewed_reports" in data
    assert "this_month_sales" in data
    assert "platform_sales" in data
    # 验证数据类型
    assert isinstance(data["total_hotels"], int)
    assert isinstance(data["split_hotels"], int)
    assert isinstance(data["total_jobs"], int)
    assert isinstance(data["completed_jobs"], int)
    assert isinstance(data["pending_review"], int)
    assert isinstance(data["reviewed_reports"], int)
    assert isinstance(data["platform_sales"], list)


def test_dashboard_platform_sales_format(client: TestClient):
    """测试平台销售额数据格式"""
    res = client.get("/api/dashboard/stats")
    data = res.json()
    platforms = [p["platform"] for p in data["platform_sales"]]
    expected = ["meituan", "ctrip", "fliggy", "douyin", "pms"]
    assert platforms == expected
    for item in data["platform_sales"]:
        assert "platform" in item
        assert "amount" in item
        assert isinstance(item["amount"], (int, float))
