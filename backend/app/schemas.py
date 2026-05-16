from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class HotelCreate(BaseModel):
    name: str
    location: Optional[str] = None
    cooperation_type: str
    company_share: float = 1.0
    owner_share: float = 0.0
    status: bool = True


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    cooperation_type: Optional[str] = None
    company_share: Optional[float] = None
    owner_share: Optional[float] = None
    status: Optional[bool] = None


class HotelResponse(BaseModel):
    id: int
    name: str
    location: Optional[str]
    cooperation_type: str
    company_share: float
    owner_share: float
    status: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlatformCreate(BaseModel):
    hotel_id: int
    platform: str
    account_name: str
    account_id: Optional[str] = None
    api_config: Optional[dict] = None
    status: bool = True


class PlatformUpdate(BaseModel):
    hotel_id: Optional[int] = None
    platform: Optional[str] = None
    account_name: Optional[str] = None
    account_id: Optional[str] = None
    api_config: Optional[dict] = None
    status: Optional[bool] = None


class PlatformResponse(BaseModel):
    id: int
    hotel_id: int
    platform: str
    account_name: str
    account_id: Optional[str]
    api_config: Optional[dict]
    status: bool

    model_config = ConfigDict(from_attributes=True)


class SalesDataResponse(BaseModel):
    id: int
    hotel_id: int
    platform: str
    order_no: Optional[str]
    check_in: Optional[date]
    check_out: Optional[date]
    room_no: Optional[str]
    room_type: Optional[str]
    amount: Decimal
    commission: Decimal
    net_amount: Decimal
    source: str
    pulled_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SalesPullRequest(BaseModel):
    hotel_id: int
    platforms: Optional[List[str]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ExpenseCreate(BaseModel):
    hotel_id: int
    category: str
    amount: Decimal
    description: Optional[str] = None
    expense_date: date
    created_by: Optional[str] = None


class ExpenseUpdate(BaseModel):
    category: Optional[str] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    expense_date: Optional[date] = None
    created_by: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    hotel_id: int
    category: str
    amount: Decimal
    description: Optional[str]
    expense_date: date
    created_at: datetime
    created_by: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ReconciliationCreate(BaseModel):
    start_date: date
    end_date: date


class ReconciliationResponse(BaseModel):
    id: int
    job_type: str
    start_date: date
    end_date: date
    status: str
    hotels_count: int
    created_at: datetime
    completed_at: Optional[datetime]
    error_msg: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ReviewRequest(BaseModel):
    reviewer: str


class ReconciliationReportResponse(BaseModel):
    id: int
    job_id: int
    hotel_id: int
    period_start: date
    period_end: date
    total_sales: Decimal
    total_commission: Decimal
    total_net_income: Decimal
    total_expense: Decimal
    company_amount: Decimal
    owner_amount: Decimal
    status: str
    reviewer: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardStats(BaseModel):
    total_hotels: int
    split_hotels: int
    total_jobs: int
    completed_jobs: int
    pending_review: int
    reviewed_reports: int
    this_month_sales: Decimal
    platform_sales: List[dict]
