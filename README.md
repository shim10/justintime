# JustInTime – FloatFry Manufacturing Resource Planning

CUH601CMD Software Engineering group project (Scrum, six weekly Sprints).

## Architecture (Sprint 1 draft)
Four layers derived from the Marketing Director's interview: presentation (role-based web views) → service layer (REST + WebSocket) → data integration (ORM + machine data ingestion) → data sources (PostgreSQL, telemetry, simulated machines). See `docs/diagrams/`.

## Tech stack
| Layer | Choice | Reason |
|---|---|---|
| Backend | Python, FastAPI | Async support for real-time machine data (WebSocket); auto-generated API docs |
| Data | PostgreSQL + SQLAlchemy | Relational model fits orders, BOM and scheduling; managed PaaS option on major clouds |
| Frontend | React | Component-based role views |
| Cloud | PaaS (app service + managed DB) | Scales without managing servers; supports the multi-plant plan (Q3 2027) |
| CI | GitHub Actions | Runs tests on every push and PR |

## Run locally
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload     # API docs at http://localhost:8000/docs
pytest -v
```

## Repository layout
```
backend/        FastAPI service, data model, tests
frontend/       React app (Sprint 2+)
simulator/      Machine telemetry simulator (Sprint 4)
docs/diagrams/  Use case, architecture, ERD (source + PNG)
```
