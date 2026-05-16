from enum import Enum

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Numeric as Decimal, Text, Enum as SQLEnum, JSON
from sqlalchemy.sql import func

from app.database import Base


class CooperationType(str, Enum):
    split = "split"
    full = "full"


class PlatformType(str, Enum):
    meituan = "meituan"
    ctrip = "ctrip"
    fliggy = "fliggy"
    douyin = "douyin"
    pms = "pms"


class DataSource(str, Enum):
    auto = "auto"
    manual = "manual"


class ExpenseCategory(str, Enum):
    utility = "utility"
    labor = "labor"
    maintenance = "maintenance"
    cleaning = "cleaning"
    other = "other"


class JobType(str, Enum):
    auto = "auto"
    manual = "manual"


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class ReportStatus(str, Enum):
    draft = "draft"
    reviewed = "reviewed"


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    cooperation_type = Column(SQLEnum(CooperationType), nullable=False)
    company_share = Column(Float, default=1.0)
    owner_share = Column(Float, default=0.0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class PlatformAccount(Base):
    __tablename__ = "platform_accounts"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    platform = Column(SQLEnum(PlatformType), nullable=False)
    account_name = Column(String(100), nullable=False)
    account_id = Column(String(100))
    api_config = Column(JSON)
    status = Column(Boolean, default=True)


class SalesData(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    platform = Column(SQLEnum(PlatformType), nullable=False)
    order_no = Column(String(100))
    check_in = Column(Date)
    check_out = Column(Date)
    room_no = Column(String(50))
    room_type = Column(String(50))
    amount = Column(Decimal(asdecimal=True), nullable=False)
    commission = Column(Decimal(asdecimal=True), default=0)
    net_amount = Column(Decimal(asdecimal=True), nullable=False)
    source = Column(SQLEnum(DataSource), default=DataSource.auto)
    pulled_at = Column(DateTime, server_default=func.now())


class ExpenseItem(Base):
    __tablename__ = "expense_items"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    category = Column(SQLEnum(ExpenseCategory), nullable=False)
    amount = Column(Decimal(asdecimal=True), nullable=False)
    description = Column(String(500))
    expense_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String(50))


class ReconciliationJob(Base):
    __tablename__ = "reconciliation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(SQLEnum(JobType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.pending)
    hotels_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)
    error_msg = Column(Text)


class ReconciliationReport(Base):
    __tablename__ = "reconciliation_reports"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("reconciliation_jobs.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_sales = Column(Decimal(asdecimal=True), default=0)
    total_commission = Column(Decimal(asdecimal=True), default=0)
    total_net_income = Column(Decimal(asdecimal=True), default=0)
    total_expense = Column(Decimal(asdecimal=True), default=0)
    company_amount = Column(Decimal(asdecimal=True), default=0)
    owner_amount = Column(Decimal(asdecimal=True), default=0)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.draft)
    reviewer = Column(String(50))
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
