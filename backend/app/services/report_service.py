from datetime import datetime

from sqlalchemy.orm import Session

from app.models import ReconciliationReport, ReportStatus


def review_report(db: Session, report_id: int, reviewer: str) -> ReconciliationReport:
    """复核报表"""
    report = db.query(ReconciliationReport).filter(ReconciliationReport.id == report_id).first()
    if not report:
        return None
    report.status = ReportStatus.reviewed
    report.reviewer = reviewer
    report.reviewed_at = datetime.now()
    db.commit()
    db.refresh(report)
    return report
