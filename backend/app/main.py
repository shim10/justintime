from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sprint 1: auto-create schema. Replaced by Alembic migrations in Sprint 2.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="JustInTime MRP API", version="0.1.0-sprint1", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "version": app.version}


@app.get("/api/v1/roles")
def list_roles():
    """Roles identified from stakeholder interviews; enforced by RBAC from Sprint 2."""
    return [r.value for r in models.Role]
