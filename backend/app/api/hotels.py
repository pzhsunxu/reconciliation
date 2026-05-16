from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Hotel
from app.schemas import HotelCreate, HotelUpdate, HotelResponse

router = APIRouter()


@router.get("/hotels", response_model=list[HotelResponse])
def list_hotels(
    name: Optional[str] = Query(None, description="酒店名称搜索"),
    cooperation_type: Optional[str] = Query(None, description="合作类型"),
    status: Optional[bool] = Query(None, description="启用状态"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(Hotel)
    if name:
        query = query.filter(Hotel.name.contains(name))
    if cooperation_type:
        query = query.filter(Hotel.cooperation_type == cooperation_type)
    if status is not None:
        query = query.filter(Hotel.status == status)
    return query.offset(skip).limit(limit).all()


@router.post("/hotels", response_model=HotelResponse, status_code=201)
def create_hotel(data: HotelCreate, db: Session = Depends(get_db)):
    hotel = Hotel(**data.model_dump())
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel


@router.get("/hotels/{hotel_id}", response_model=HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "酒店不存在")
    return hotel


@router.put("/hotels/{hotel_id}", response_model=HotelResponse)
def update_hotel(hotel_id: int, data: HotelUpdate, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "酒店不存在")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(hotel, key, value)
    db.commit()
    db.refresh(hotel)
    return hotel


@router.delete("/hotels/{hotel_id}", status_code=204)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "酒店不存在")
    db.delete(hotel)
    db.commit()
