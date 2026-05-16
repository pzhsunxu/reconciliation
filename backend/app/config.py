import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'reconciliation.db')}"

AUTO_RECONCILIATION_DAYS = [12, 28]
AUTO_RECONCILIATION_HOUR = 2
