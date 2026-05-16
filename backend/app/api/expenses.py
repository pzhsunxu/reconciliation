from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ExpenseItem, Hotel
from app.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter()


@router.get("/expenses", response_model=list[ExpenseResponse])
def list_expenses(
    hotel_id: Optional[int] = Query(None, description="酒店ID"),
    category: Optional[str] = Query(None, description="开支类别"),
    start_date: Optional[date] = Query(None, description="起始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    query = db.query(ExpenseItem)
    if hotel_id:
        query = query.filter(ExpenseItem.hotel_id == hotel_id)
    if category:
        query = query.filter(ExpenseItem.category == category)
    if start_date:
        query = query.filter(ExpenseItem.expense_date >= start_date)
    if end_date:
        query = query.filter(ExpenseItem.expense_date <= end_date)
    return query.offset(skip).limit(limit).all()


@router.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == data.hotel_id).first()
    if not hotel:
        raise HTTPException(404, "酒店不存在")
    expense = ExpenseItem(**data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseItem).filter(ExpenseItem.id == expense_id).first()
    if not expense:
        raise HTTPException(404, "开支记录不存在")
    return expense


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, data: ExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.query(ExpenseItem).filter(ExpenseItem.id == expense_id).first()
    if not expense:
        raise HTTPException(404, "开支记录不存在")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseItem).filter(ExpenseItem.id == expense_id).first()
    if not expense:
        raise HTTPException(404, "开支记录不存在")
    db.delete(expense)
    db.commit()
