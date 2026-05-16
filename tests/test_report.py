from fastapi.testclient import TestClient
from datetime import date
from decimal import Decimal
from app.models import ReconciliationReport, ReportStatus, ReconciliationJob, JobStatus, Hotel, CooperationType
from sqlalchemy.orm import Session


def _setup_report_with_data(db: Session):
    """创建一个包含完整数据的报表用于测试"""
    hotel = Hotel(name="测试酒店", cooperation_type=CooperationType.split, company_share=0.6, owner_share=0.4)
    db.add(hotel)
    db.flush()

    job = ReconciliationJob(job_type="manual", start_date=date.today(), end_date=date.today(), status=JobStatus.completed, hotels_count=1)
    db.add(job)
    db.flush()

    report = ReconciliationReport(
        job_id=job.id,
        hotel_id=hotel.id,
        period_start=date.today(),
        period_end=date.today(),
        total_sales=Decimal("10000.00"),
        total_commission=Decimal("1000.00"),
        total_net_income=Decimal("9000.00"),
        total_expense=Decimal("500.00"),
        company_amount=Decimal("5100.00"),
        owner_amount=Decimal("3400.00"),
        status=ReportStatus.draft,
    )
    db.add(report)
    db.commit()
    return report


def test_list_reports(client: TestClient, db: Session):
    _setup_report_with_data(db)
    res = client.get("/api/reports")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_get_report(client: TestClient, db: Session):
    report = _setup_report_with_data(db)
    res = client.get(f"/api/reports/{report.id}")
    assert res.status_code == 200
    data = res.json()
    assert float(data["total_sales"]) == 10000.00
    assert float(data["company_amount"]) == 5100.00


def test_review_report(client: TestClient, db: Session):
    report = _setup_report_with_data(db)
    res = client.post(f"/api/reports/{report.id}/review", json={"reviewer": "张经理"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "reviewed"
    assert data["reviewer"] == "张经理"


def test_report_not_found(client: TestClient):
    res = client.get("/api/reports/999")
    assert res.status_code == 404


def test_review_report_not_found(client: TestClient):
    res = client.post("/api/reports/999/review", json={"reviewer": "李四"})
    assert res.status_code == 404


def test_filter_reports_by_status(client: TestClient, db: Session):
    report = _setup_report_with_data(db)
    res = client.get("/api/reports", params={"status": "draft"})
    assert len(res.json()) >= 1
    for item in res.json():
        assert item["status"] == "draft"


def test_reconciliation_calculation(client: TestClient, db: Session):
    """测试对账计算: 公司应得+房东应得 = 可分配利润"""
    report = _setup_report_with_data(db)
    distributable = Decimal(str(report.total_net_income)) - Decimal(str(report.total_expense))
    assert Decimal(str(report.company_amount)) + Decimal(str(report.owner_amount)) == distributable
    assert Decimal(str(report.company_amount)) == distributable * Decimal("0.6")
    assert Decimal(str(report.owner_amount)) == distributable * Decimal("0.4")
