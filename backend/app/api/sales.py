from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SalesData, PlatformAccount, PlatformType, Hotel
from app.schemas import SalesDataResponse, SalesPullRequest
from app.services.platform_service import pull_platform_data

router = APIRouter()


@router.get("/sales", response_model=list[SalesDataResponse])
def list_sales(
    hotel_id: Optional[int] = Query(None, description="酒店ID"),
    platform: Optional[str] = Query(None, description="平台类型"),
    start_date: Optional[date] = Query(None, description="起始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    query = db.query(SalesData)
    if hotel_id:
        query = query.filter(SalesData.hotel_id == hotel_id)
    if platform:
        query = query.filter(SalesData.platform == platform)
    if start_date:
        query = query.filter(SalesData.check_in >= start_date)
    if end_date:
        query = query.filter(SalesData.check_in <= end_date)
    return query.offset(skip).limit(limit).all()


@router.post("/sales/pull", status_code=200)
def pull_sales_data(request: SalesPullRequest, db: Session = Depends(get_db)):
    """手动拉取指定酒店的平台销售数据"""
    hotel = db.query(Hotel).filter(Hotel.id == request.hotel_id).first()
    if not hotel:
        raise HTTPException(404, "酒店不存在")

    platforms = db.query(PlatformAccount).filter(
        PlatformAccount.hotel_id == request.hotel_id,
        PlatformAccount.status == True,
    ).all()

    if not platforms:
        raise HTTPException(400, "该酒店未配置启用的平台账号")

    if request.platforms:
        platforms = [p for p in platforms if p.platform in request.platforms]

    start = request.start_date or date.today().replace(day=1)
    end = request.end_date or date.today()

    total_pulled = 0
    for platform_account in platforms:
        data = pull_platform_data(request.hotel_id, platform_account.platform, start, end)
        for item in data:
            sales = SalesData(**item)
            db.add(sales)
            total_pulled += 1
    db.commit()
    return {"pulled": total_pulled, "hotel_id": request.hotel_id, "start_date": str(start), "end_date": str(end)}
