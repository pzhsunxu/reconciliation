from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ReconciliationReport
from app.schemas import ReconciliationReportResponse, ReviewRequest
from app.services.report_service import review_report
from app.utils.excel_export import export_report_to_excel

router = APIRouter()


@router.get("/reports", response_model=list[ReconciliationReportResponse])
def list_reports(
    hotel_id: Optional[int] = Query(None, description="酒店ID"),
    status: Optional[str] = Query(None, description="报表状态"),
    start_date: Optional[date] = Query(None, description="周期起始"),
    end_date: Optional[date] = Query(None, description="周期结束"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(ReconciliationReport)
    if hotel_id:
        query = query.filter(ReconciliationReport.hotel_id == hotel_id)
    if status:
        query = query.filter(ReconciliationReport.status == status)
    if start_date:
        query = query.filter(ReconciliationReport.period_start >= start_date)
    if end_date:
        query = query.filter(ReconciliationReport.period_end <= end_date)
    return query.order_by(ReconciliationReport.id.desc()).offset(skip).limit(limit).all()


@router.get("/reports/{report_id}", response_model=ReconciliationReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(ReconciliationReport).filter(ReconciliationReport.id == report_id).first()
    if not report:
        raise HTTPException(404, "报表不存在")
    return report


@router.post("/reports/{report_id}/review", response_model=ReconciliationReportResponse)
def review(report_id: int, data: ReviewRequest, db: Session = Depends(get_db)):
    report = review_report(db, report_id, data.reviewer)
    if not report:
        raise HTTPException(404, "报表不存在")
    return report


@router.get("/reports/{report_id}/excel")
def export_excel(report_id: int, db: Session = Depends(get_db)):
    excel_data = export_report_to_excel(db, report_id)
    if not excel_data:
        raise HTTPException(404, "报表不存在")
    return StreamingResponse(
        iter([excel_data]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment;filename=report_{report_id}.xlsx"},
    )
