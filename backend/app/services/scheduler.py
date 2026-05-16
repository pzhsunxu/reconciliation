from apscheduler.schedulers.background import BackgroundScheduler

from app.config import AUTO_RECONCILIATION_DAYS, AUTO_RECONCILIATION_HOUR
from app.services.reconciliation_service import run_auto_reconciliation

_scheduler = BackgroundScheduler()


def init_scheduler():
    """初始化定时任务"""
    for day in AUTO_RECONCILIATION_DAYS:
        _scheduler.add_job(
            run_auto_reconciliation,
            "cron",
            day=day,
            hour=AUTO_RECONCILIATION_HOUR,
            minute=0,
            id=f"auto_reconciliation_{day}",
            name=f"自动对账(每月{day}号)",
            replace_existing=True,
        )
    _scheduler.start()
