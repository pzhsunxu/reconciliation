from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models import ReconciliationJob, JobStatus
from app.schemas import ReconciliationCreate, ReconciliationResponse
from app.services.reconciliation_service import create_job, run_reconciliation

router = APIRouter()


@router.get("/reconciliations", response_model=list[ReconciliationResponse])
def list_jobs(
    job_type: Optional[str] = Query(None, description="任务类型"),
    status: Optional[str] = Query(None, description="任务状态"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(ReconciliationJob)
    if job_type:
        query = query.filter(ReconciliationJob.job_type == job_type)
    if status:
        query = query.filter(ReconciliationJob.status == status)
    return query.order_by(ReconciliationJob.id.desc()).offset(skip).limit(limit).all()


@router.post("/reconciliations", response_model=ReconciliationResponse, status_code=201)
def create_manual_job(
    data: ReconciliationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    job = create_job(db, "manual", data.start_date, data.end_date)
    background_tasks.add_task(run_reconciliation, db, job.id)
    return job


@router.get("/reconciliations/{job_id}", response_model=ReconciliationResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(ReconciliationJob).filter(ReconciliationJob.id == job_id).first()
    if not job:
        raise HTTPException(404, "对账任务不存在")
    return job
