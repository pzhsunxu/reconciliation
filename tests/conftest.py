import os
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.api import hotels, platforms, sales, expenses, reconciliation, reports


temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
temp_db.close()
DB_URL = f"sqlite:///{temp_db.name}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    """Truncate all tables before each test"""
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    yield
    engine.dispose()
    try:
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)
    except PermissionError:
        pass


def create_test_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(hotels.router, prefix="/api", tags=["酒店管理"])
    app.include_router(platforms.router, prefix="/api", tags=["平台账号"])
    app.include_router(sales.router, prefix="/api", tags=["销售数据"])
    app.include_router(expenses.router, prefix="/api", tags=["日常开支"])
    app.include_router(reconciliation.router, prefix="/api", tags=["对账任务"])
    app.include_router(reports.router, prefix="/api", tags=["对账报表"])
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
def client():
    app = create_test_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
