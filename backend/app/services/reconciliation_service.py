from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import (
    Hotel, SalesData, ExpenseItem, ReconciliationJob, ReconciliationReport,
    CooperationType, JobStatus, ReportStatus, PlatformType,
)
from app.database import SessionLocal
from app.services.platform_service import pull_platform_data


def run_reconciliation(db: Session, job_id: int):
    """执行对账任务：拉取数据、计算、生成报表"""
    job = db.query(ReconciliationJob).filter(ReconciliationJob.id == job_id).first()
    if not job:
        return

    job.status = JobStatus.running
    db.commit()

    try:
        split_hotels = (
            db.query(Hotel)
            .filter(Hotel.cooperation_type == CooperationType.split, Hotel.status == True)
            .all()
        )
        job.hotels_count = len(split_hotels)
        db.commit()

        platforms = [PlatformType.meituan, PlatformType.ctrip, PlatformType.fliggy, PlatformType.douyin, PlatformType.pms]

        for hotel in split_hotels:
            # 拉取各平台销售数据
            for platform in platforms:
                data = pull_platform_data(hotel.id, platform, job.start_date, job.end_date)
                for item in data:
                    sales = SalesData(**item)
                    db.add(sales)
            db.commit()

            # 计算销售汇总
            sales_records = (
                db.query(SalesData)
                .filter(
                    SalesData.hotel_id == hotel.id,
                    SalesData.check_in >= job.start_date,
                    SalesData.check_in <= job.end_date,
                )
                .all()
            )
            total_sales = sum([s.amount for s in sales_records], Decimal("0"))
            total_commission = sum([s.commission for s in sales_records], Decimal("0"))
            total_net_income = total_sales - total_commission

            # 计算日常开支
            expenses = (
                db.query(ExpenseItem)
                .filter(
                    ExpenseItem.hotel_id == hotel.id,
                    ExpenseItem.expense_date >= job.start_date,
                    ExpenseItem.expense_date <= job.end_date,
                )
                .all()
            )
            total_expense = sum([e.amount for e in expenses], Decimal("0"))

            # 计算分润
            distributable = total_net_income - total_expense
            company_amount = round(distributable * Decimal(str(hotel.company_share)), 2)
            owner_amount = round(distributable * Decimal(str(hotel.owner_share)), 2)

            # 生成报表
            report = ReconciliationReport(
                job_id=job_id,
                hotel_id=hotel.id,
                period_start=job.start_date,
                period_end=job.end_date,
                total_sales=total_sales,
                total_commission=total_commission,
                total_net_income=total_net_income,
                total_expense=total_expense,
                company_amount=company_amount,
                owner_amount=owner_amount,
                status=ReportStatus.draft,
            )
            db.add(report)

        db.commit()
        job.status = JobStatus.completed
        job.completed_at = datetime.now()
        db.commit()

    except Exception as e:
        job.status = JobStatus.failed
        job.error_msg = str(e)
        db.commit()
        db.rollback()


def create_job(db: Session, job_type: str, start_date: date, end_date: date) -> ReconciliationJob:
    """创建对账任务"""
    job = ReconciliationJob(
        job_type=job_type,
        start_date=start_date,
        end_date=end_date,
        status=JobStatus.pending,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def run_auto_reconciliation():
    """自动对账定时任务入口"""
    db = SessionLocal()
    try:
        today = date.today()
        # 计算对账区间：上一次对账结束日+1天至今天
        last_job = (
            db.query(ReconciliationJob)
            .filter(ReconciliationJob.job_type == "auto")
            .order_by(ReconciliationJob.id.desc())
            .first()
        )
        if last_job:
            start_date = last_job.end_date.replace(day=1) + __import__("datetime").timedelta(days=1)
        else:
            start_date = today.replace(day=1)
        start_date = max(start_date, today.replace(day=1))
        end_date = today

        job = create_job(db, "auto", start_date, end_date)
        run_reconciliation(db, job.id)
    finally:
        db.close()
