# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hotel reconciliation system that manages sales data across multiple booking platforms (Meituan, Ctrip, Fliggy, Douyin, PMS) for 100+ hotels. Supports two cooperation models: profit-split (分润) and full-rental (全租). Runs auto-reconciliation twice monthly (12th/28th) and allows manual reconciliation.

## Stack

- **Backend**: Python FastAPI + SQLAlchemy 2.0 + SQLite + APScheduler 3.11
- **Frontend**: Vue 3 + Element Plus + Vite 5.4
- **Test**: pytest + httpx TestClient

## Quick Start

```bash
# Backend (port 8001)
cd backend && pip install -r requirements.txt && python main.py

# Frontend (port 5173)
cd frontend && npm install && npm run dev

# Tests
pytest tests/ -v

# Single test file
pytest tests/test_reconciliation.py -v

# API docs (when backend is running)
# http://localhost:8001/docs
```

## Key Architecture Details

### Backend structure (`backend/app/`)

- `main.py` — FastAPI app with `lifespan` context manager (NOT `@app.on_event`). Auto-registers all routers under `/api`. Dashboard stats endpoint lives here directly.
- `models.py` — 6 SQLAlchemy models. Note: `Numeric` is imported as `Decimal` (`from sqlalchemy import Numeric as Decimal`). The raw `Float` type is used for `company_share`/`owner_share`, so always convert with `Decimal(str(value))` before arithmetic.
- `database.py` — SQLite via `SessionLocal()`. Database file: `reconciliation.db` in the backend directory.
- `api/` — One router per domain. All routers have their own prefix (e.g., `/hotels`), and main.py adds `/api` when including.
- `services/reconciliation_service.py` — Core reconciliation logic. Only processes profit-split (`split`) hotels. Full-rental (`full`) hotels are skipped.
- `services/platform_service.py` — Currently generates mock sales data. The `pull_platform_data()` function is the integration point for real platform APIs.
- `services/scheduler.py` — APScheduler uses `day` parameter (not `day_of_month`) for v3.11. Jobs use `id` parameter (not `job_id`).
- `schemas.py` — All Pydantic models use `model_config = ConfigDict(from_attributes=True)`.

### Reconciliation flow

1. Job created → status `pending`
2. Background task starts → status `running`
3. For each split-mode hotel: pull sales data from all 5 platforms → calculate totals → generate report (status `draft`)
4. Job complete → status `completed`
5. User reviews report → status `reviewed`, records reviewer name and timestamp

### Frontend structure (`frontend/src/`)

- `router/index.js` — 7 routes: Dashboard, Hotels, Platforms, Sales, Expenses, Reconciliation, Reports
- `components/Layout.vue` — Persistent sidebar layout; all views are rendered inside it
- `App.vue` — Contains all global styles: dark tech theme via CSS variables (`--accent-cyan`, `--bg-card`, etc.), Element Plus overrides, grid background, neon glow effects. Fonts: Orbitron (headings), Share Tech Mono (numbers). Any new UI components inherit these variables.
- `main.js` — Has a critical overlay cleanup workaround: Element Plus leaves invisible `.el-overlay` elements that stack up and block clicks on rapid dialog open/close. A `setInterval` + `MutationObserver` clean them up. If dialogs become unclickable, check this cleanup.
- `vite.config.js` — Proxies `/api` to `http://localhost:8001`

### Test setup (`tests/conftest.py`)

Uses a temp file SQLite database (not in-memory) to avoid Windows shared memory issues. Creates a test app without the scheduler. Each test gets a fresh database.
