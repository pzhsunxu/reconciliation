from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PlatformAccount
from app.schemas import PlatformCreate, PlatformUpdate, PlatformResponse

router = APIRouter()


@router.get("/platforms", response_model=list[PlatformResponse])
def list_platforms(
    hotel_id: Optional[int] = Query(None, description="关联酒店ID"),
    platform: Optional[str] = Query(None, description="平台类型"),
    status: Optional[bool] = Query(None, description="启用状态"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(PlatformAccount)
    if hotel_id:
        query = query.filter(PlatformAccount.hotel_id == hotel_id)
    if platform:
        query = query.filter(PlatformAccount.platform == platform)
    if status is not None:
        query = query.filter(PlatformAccount.status == status)
    return query.offset(skip).limit(limit).all()


@router.post("/platforms", response_model=PlatformResponse, status_code=201)
def create_platform(data: PlatformCreate, db: Session = Depends(get_db)):
    account = PlatformAccount(**data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/platforms/{platform_id}", response_model=PlatformResponse)
def get_platform(platform_id: int, db: Session = Depends(get_db)):
    account = db.query(PlatformAccount).filter(PlatformAccount.id == platform_id).first()
    if not account:
        raise HTTPException(404, "平台账号不存在")
    return account


@router.put("/platforms/{platform_id}", response_model=PlatformResponse)
def update_platform(platform_id: int, data: PlatformUpdate, db: Session = Depends(get_db)):
    account = db.query(PlatformAccount).filter(PlatformAccount.id == platform_id).first()
    if not account:
        raise HTTPException(404, "平台账号不存在")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account


@router.delete("/platforms/{platform_id}", status_code=204)
def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    account = db.query(PlatformAccount).filter(PlatformAccount.id == platform_id).first()
    if not account:
        raise HTTPException(404, "平台账号不存在")
    db.delete(account)
    db.commit()
