from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok():
    with TestClient(app) as client:
        r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_roles_match_stakeholder_analysis():
    with TestClient(app) as client:
        roles = client.get("/api/v1/roles").json()
    assert set(roles) == {"Marketing", "ProdManager", "Prodee", "PO", "FloorManager", "Stamper"}
