import os
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.api import hotels, platforms, sales, expenses, reconciliation, reports


temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
temp_db.close()
DB_URL = f"sqlite:///{temp_db.name}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    """Truncate all tables before each test"""
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    yield
    engine.dispose()
    try:
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)
    except PermissionError:
        pass


def create_test_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(hotels.router, prefix="/api", tags=["酒店管理"])
    app.include_router(platforms.router, prefix="/api", tags=["平台账号"])
    app.include_router(sales.router, prefix="/api", tags=["销售数据"])
    app.include_router(expenses.router, prefix="/api", tags=["日常开支"])
    app.include_router(reconciliation.router, prefix="/api", tags=["对账任务"])
    app.include_router(reports.router, prefix="/api", tags=["对账报表"])

    # Dashboard stats endpoint
    @app.get("/api/dashboard/stats")
    def get_dashboard_stats():
        from app.models import Hotel, ReconciliationJob, ReconciliationReport, SalesData, CooperationType, ReportStatus, JobStatus
        from app.schemas import DashboardStats
        from datetime import datetime
        from decimal import Decimal

        db = TestingSessionLocal()
        try:
            total_hotels = db.query(Hotel).count()
            split_hotels = db.query(Hotel).filter(Hotel.cooperation_type == CooperationType.split).count()
            total_jobs = db.query(ReconciliationJob).count()
            completed_jobs = db.query(ReconciliationJob).filter(ReconciliationJob.status == JobStatus.completed).count()
            pending_review = db.query(ReconciliationReport).filter(ReconciliationReport.status == ReportStatus.draft).count()
            reviewed_reports = db.query(ReconciliationReport).filter(ReconciliationReport.status == ReportStatus.reviewed).count()

            now = datetime.now()
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            sales_data = db.query(SalesData).filter(SalesData.check_in >= first_day).all()
            this_month_sales = sum([s.amount for s in sales_data], Decimal("0"))

            platform_sales = []
            for p in ["meituan", "ctrip", "fliggy", "douyin", "pms"]:
                total = sum([s.amount for s in sales_data if s.platform == p], Decimal("0"))
                platform_sales.append({"platform": p, "amount": float(total)})

            return DashboardStats(
                total_hotels=total_hotels,
                split_hotels=split_hotels,
                total_jobs=total_jobs,
                completed_jobs=completed_jobs,
                pending_review=pending_review,
                reviewed_reports=reviewed_reports,
                this_month_sales=float(this_month_sales),
                platform_sales=platform_sales,
            )
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
def client():
    app = create_test_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
