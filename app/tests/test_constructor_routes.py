import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_constructor_standings():
    response = client.get("/api/constructors/standings")
    assert response.status_code == 200
    assert "standings" in response.json()
    assert "total_count" in response.json()

def test_get_constructor_results():
    response = client.get("/api/constructors/1/results")
    assert response.status_code == 200
    assert "constructor_results" in response.json()