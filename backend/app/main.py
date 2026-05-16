from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.api import hotels, platforms, sales, expenses, reconciliation, reports
from app.services import scheduler

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app):
    scheduler.init_scheduler()
    yield
    scheduler._scheduler.shutdown()


app = FastAPI(title="对账系统", version="1.0.0", lifespan=lifespan)

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


@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models import Hotel, ReconciliationJob, ReconciliationReport, SalesData, CooperationType, ReportStatus, JobStatus
    from app.schemas import DashboardStats
    from datetime import datetime
    from decimal import Decimal

    db = SessionLocal()
    try:
        total_hotels = db.query(Hotel).count()
        split_hotels = db.query(Hotel).filter(Hotel.cooperation_type == CooperationType.split).count()
        total_jobs = db.query(ReconciliationJob).count()
        completed_jobs = db.query(ReconciliationJob).filter(ReconciliationJob.status == JobStatus.completed).count()
        pending_review = db.query(ReconciliationReport).filter(ReconciliationReport.status == ReportStatus.draft).count()
        reviewed_reports = db.query(ReconciliationReport).filter(ReconciliationReport.status == ReportStatus.reviewed).count()

        now = datetime.now()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        sales_data = (
            db.query(SalesData)
            .filter(SalesData.check_in >= first_day)
            .all()
        )
        this_month_sales = sum([s.amount for s in sales_data], Decimal("0"))

        platform_sales = []
        platforms_list = ["meituan", "ctrip", "fliggy", "douyin", "pms"]
        for p in platforms_list:
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
